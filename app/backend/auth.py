"""Supabase authentication for the Windows desktop client. No demo authentication."""
import base64
import hashlib
import html
import http.server
import json
import secrets
import socketserver
import threading
import time
import urllib.parse
import webbrowser
from pathlib import Path
from .cloud_client import CloudClient, CloudError, failure
from .paths import get_data_dir, get_app_root, atomic_write
from .secure_storage import SecureStorage


class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    auth_engine_ref = None

    def log_message(self, *args):
        pass  # Callback URLs must never be logged.

    def do_GET(self):
        query = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        valid = (urllib.parse.urlparse(self.path).path == '/callback'
                 and OAuthServerManager.nonce
                 and secrets.compare_digest(query.get('app_state', [''])[0], OAuthServerManager.nonce))
        if not valid:
            self.send_error(400, 'Invalid authentication attempt')
            return
        try:
            if query.get('error'):
                raise CloudError('Bạn đã hủy hoặc nhà cung cấp từ chối đăng nhập.', 'OAUTH_CANCELLED')
            code = query.get('code', [''])[0]
            if not code or not OAuthServerManager.verifier:
                raise CloudError('Thiếu mã xác thực.', 'INVALID_CALLBACK')
            verifier = OAuthServerManager.verifier
            OAuthServerManager.verifier = None  # Consume this attempt once.
            response = CloudClient().request('auth/v1/token', 'POST',
                       {'auth_code': code, 'code_verifier': verifier}, {'grant_type': 'pkce'})
            session = self.auth_engine_ref.accept_session(response)
            result = {'success': True, 'status': 'success', 'session': session}
            message = 'Đăng nhập thành công. Bạn có thể quay lại ứng dụng.'
        except (CloudError, OSError, ValueError) as error:
            result = failure(error)
            message = str(error)
        OAuthServerManager.last_oauth_result = result
        self.send_response(200 if result['success'] else 400)
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Security-Policy', "default-src 'none'; style-src 'unsafe-inline'")
        self.end_headers()
        self.wfile.write(('<!doctype html><meta charset="utf-8"><title>AbyssalSkillsD</title><p>' + html.escape(message) + '</p>').encode())
        threading.Thread(target=OAuthServerManager.stop_server, daemon=True).start()


class OAuthServerManager:
    server = None
    server_thread = None
    last_oauth_result = None
    nonce = None
    verifier = None
    timer = None

    @classmethod
    def start_server(cls, auth_engine, port=54321):
        cls.stop_server()
        cls.last_oauth_result = None
        cls.nonce = secrets.token_urlsafe(32)
        cls.verifier = secrets.token_urlsafe(64)
        OAuthCallbackHandler.auth_engine_ref = auth_engine
        try:
            cls.server = socketserver.TCPServer(('127.0.0.1', port), OAuthCallbackHandler)
            cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
            cls.server_thread.start()
            cls.timer = threading.Timer(120, cls.expire)
            cls.timer.daemon = True
            cls.timer.start()
            return True
        except OSError:
            cls.nonce = cls.verifier = None
            return False

    @classmethod
    def expire(cls):
        cls.last_oauth_result = failure(CloudError('Đăng nhập đã hết thời gian chờ.', 'OAUTH_TIMEOUT'))
        cls.stop_server()

    @classmethod
    def stop_server(cls):
        if cls.timer:
            cls.timer.cancel()
            cls.timer = None
        server, cls.server = cls.server, None
        cls.nonce = cls.verifier = None
        if server:
            server.shutdown()
            server.server_close()


class AuthEngine:
    DATA_DIR = get_data_dir()
    CONFIG_FILE = DATA_DIR / 'supabase_config.json'
    SESSION_FILE = DATA_DIR / 'auth_session.json'
    _session = None
    _session_project = None
    _lock = threading.RLock()

    @classmethod
    def get_config(cls):
        bundled = get_app_root() / 'app/data/supabase_config.json'
        config = {'supabase_url': '', 'anon_key': '', 'project_name': 'AbyssalSkillsD'}
        for file in dict.fromkeys([bundled, cls.CONFIG_FILE]):
            if file.is_file():
                saved = json.loads(file.read_text(encoding='utf-8'))
                config.update({key: saved[key] for key in config if key in saved})
        return config

    @classmethod
    def save_config(cls, url, anon_key, secret_key=''):
        if secret_key:
            return failure(CloudError('Không nhập khóa quản trị vào ứng dụng desktop.', 'ADMIN_KEY_FORBIDDEN'))
        url = (url or '').strip().rstrip('/')
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or parsed.path:
            return failure(CloudError('Địa chỉ Supabase phải là HTTPS hợp lệ.', 'INVALID_CONFIG'))
        config = {'supabase_url': url, 'anon_key': (anon_key or '').strip(), 'project_name': 'AbyssalSkillsD'}
        if not config['anon_key']:
            return failure(CloudError('Thiếu khóa công khai.', 'INVALID_CONFIG'))
        # Reject legacy JWT service-role keys as well as modern secret keys.
        key = config['anon_key']
        if key.startswith('sb_secret_'):
            return failure(CloudError('Chỉ được dùng khóa công khai.', 'ADMIN_KEY_FORBIDDEN'))
        try:
            if key.startswith('eyJ'):
                claims = json.loads(base64.urlsafe_b64decode(key.split('.')[1] + '==='))
                if claims.get('role') != 'anon':
                    raise ValueError('not public')
        except (ValueError, IndexError):
            return failure(CloudError('Khóa công khai không hợp lệ.', 'INVALID_CONFIG'))
        cls.clear_session()
        atomic_write(cls.CONFIG_FILE, json.dumps(config, ensure_ascii=False, indent=2))
        return {'success': True, 'status': 'success', 'config': cls.get_safe_config(), 'message': 'Đã lưu cấu hình công khai.'}

    @classmethod
    def get_safe_config(cls):
        config = cls.get_config()
        return {**{key: config.get(key, '') for key in ('supabase_url', 'anon_key', 'project_name')}, 'has_secret_key': False}

    @staticmethod
    def public_session(session):
        if not session:
            return {'authenticated': False, 'user': None}
        return {'authenticated': True, 'user': dict(session['user']), 'expires_at': session['expires_at']}

    @classmethod
    def fetch_user_from_token(cls, access_token):
        user = CloudClient(token=access_token).request('auth/v1/user')
        if not user or not user.get('id'):
            raise CloudError('Không xác minh được tài khoản.', 'INVALID_USER')
        metadata = user.get('user_metadata') or {}
        profile = {'id': user['id'], 'email': user.get('email', ''),
                   'full_name': metadata.get('full_name') or metadata.get('name') or 'Developer',
                   'avatar_url': metadata.get('avatar_url') or '', 'bio': '', 'role': 'creator',
                   'provider': (user.get('app_metadata') or {}).get('provider', 'email')}
        return profile

    @classmethod
    def accept_session(cls, response):
        if not response or not response.get('access_token') or not response.get('refresh_token'):
            raise CloudError('Máy chủ chưa cấp phiên đăng nhập hợp lệ.', 'INVALID_SESSION')
        user = cls.fetch_user_from_token(response['access_token'])
        session = {'access_token': response['access_token'], 'refresh_token': response['refresh_token'],
                   'expires_at': time.time() + max(1, int(response.get('expires_in', 3600))), 'user': user}
        cls.save_session(session)
        try:
            profile = CloudClient(token=session['access_token']).rpc('get_my_cloud_profile')
            if not profile:
                profile = cls.sync_user_profile(user, session['access_token'])
            if profile:
                session['user'].update({key: value for key, value in profile.items() if key in ('full_name', 'bio', 'avatar_url', 'role')})
        except CloudError:
            session['profile_sync_pending'] = True
        return cls.public_session(session)

    @classmethod
    def save_session(cls, session):
        project = cls.get_config()['supabase_url']
        SecureStorage.write(project, session['refresh_token'])
        cls._session = session
        cls._session_project = project
        # Only remove legacy plaintext after secure persistence succeeded.
        cls.SESSION_FILE.unlink(missing_ok=True)

    @classmethod
    def get_session(cls):
        with cls._lock:
            project = cls.get_config()['supabase_url']
            if cls._session_project != project:
                cls._session = None
            if cls._session and cls._session['expires_at'] > time.time() + 30:
                return cls.public_session(cls._session)
            try:
                refresh = SecureStorage.read(project)
                if not refresh and cls.SESSION_FILE.is_file():
                    legacy = json.loads(cls.SESSION_FILE.read_text(encoding='utf-8'))
                    refresh = legacy.get('refresh_token')
                if refresh:
                    result = cls.refresh_token(refresh)
                    if result['success']:
                        return result['session']
            except (OSError, ValueError):
                pass
            return {'authenticated': False, 'user': None}

    @classmethod
    def get_access_token(cls, required=True):
        if cls.get_session().get('authenticated'):
            return cls._session['access_token']
        if required:
            raise CloudError('Vui lòng đăng nhập để thực hiện thao tác này.', 'AUTH_REQUIRED', 401)
        return None

    @classmethod
    def clear_session(cls):
        cls._session = None
        cls._session_project = None
        SecureStorage.delete(cls.get_config()['supabase_url'])
        cls.SESSION_FILE.unlink(missing_ok=True)

    @classmethod
    def sign_in(cls, email, password):
        if not (email or '').strip() or not password:
            return failure(CloudError('Vui lòng nhập email và mật khẩu.', 'INVALID_INPUT'))
        try:
            response = CloudClient().request('auth/v1/token', 'POST', {'email': email.strip(), 'password': password}, {'grant_type': 'password'})
            return {'success': True, 'status': 'success', 'session': cls.accept_session(response), 'message': 'Đã đăng nhập.'}
        except (CloudError, OSError, ValueError) as error:
            return failure(error)

    @classmethod
    def sign_up(cls, email, password, full_name=''):
        if not email or len(password or '') < 6:
            return failure(CloudError('Nhập email và mật khẩu ít nhất 6 ký tự.', 'INVALID_INPUT'))
        try:
            response = CloudClient().request('auth/v1/signup', 'POST', {'email': email.strip(), 'password': password, 'data': {'full_name': full_name.strip()}})
            if response.get('access_token'):
                return {'success': True, 'status': 'success', 'session': cls.accept_session(response), 'message': 'Đã tạo tài khoản và đăng nhập.'}
            return {'success': True, 'status': 'success', 'requires_login': True, 'requires_confirmation': True,
                    'message': 'Hãy kiểm tra email để xác nhận tài khoản trước khi đăng nhập.'}
        except (CloudError, OSError, ValueError) as error:
            return failure(error)

    @classmethod
    def refresh_token(cls, refresh_token):
        with cls._lock:
            try:
                response = CloudClient().request('auth/v1/token', 'POST', {'refresh_token': refresh_token}, {'grant_type': 'refresh_token'})
                return {'success': True, 'status': 'success', 'session': cls.accept_session(response)}
            except (CloudError, OSError, ValueError) as error:
                cls._session = None
                return failure(error)

    @classmethod
    def start_oauth(cls, provider):
        if provider not in ('google', 'github'):
            return failure(CloudError('Nhà cung cấp không được hỗ trợ.', 'INVALID_PROVIDER'))
        try:
            settings = CloudClient().request('auth/v1/settings')
            if not settings.get('external', {}).get(provider):
                raise CloudError('Nhà cung cấp này chưa được cấu hình trên Supabase.', 'PROVIDER_UNAVAILABLE')
            if not OAuthServerManager.start_server(cls):
                raise CloudError('Cổng đăng nhập 54321 đang được sử dụng.', 'OAUTH_PORT_BUSY')
            redirect = 'http://localhost:54321/callback?app_state=' + OAuthServerManager.nonce
            challenge = base64.urlsafe_b64encode(hashlib.sha256(OAuthServerManager.verifier.encode()).digest()).decode().rstrip('=')
            url = cls.get_config()['supabase_url'] + '/auth/v1/authorize?' + urllib.parse.urlencode({
                'provider': provider, 'redirect_to': redirect, 'code_challenge': challenge, 'code_challenge_method': 's256'})
            if not webbrowser.open(url):
                OAuthServerManager.stop_server()
                raise CloudError('Không mở được trình duyệt đăng nhập.', 'BROWSER_UNAVAILABLE')
            return {'success': True, 'status': 'success', 'listening': True, 'message': 'Hoàn tất đăng nhập trong trình duyệt.'}
        except (CloudError, OSError) as error:
            return failure(error)

    @classmethod
    def sign_in_with_oauth(cls, provider):
        return cls.start_oauth(provider)

    @classmethod
    def check_oauth_status(cls):
        return OAuthServerManager.last_oauth_result or {'success': False, 'pending': True}

    @classmethod
    def sign_out(cls):
        token = cls._session.get('access_token') if cls._session else None
        revoked = True
        try:
            if token:
                CloudClient(token=token).request('auth/v1/logout', 'POST', {})
        except CloudError:
            revoked = False
        try:
            cls.clear_session()
        except OSError as error:
            return failure(error)
        OAuthServerManager.stop_server()
        return {'success': True, 'status': 'success', 'server_revoked': revoked,
                'message': 'Đã đăng xuất trên máy.' + ('' if revoked else ' Chưa xác nhận thu hồi trên máy chủ do lỗi mạng.')}

    @classmethod
    def sync_user_profile(cls, user_data, access_token):
        return CloudClient(token=access_token).rpc('save_my_profile', {'p_name': user_data['full_name'], 'p_bio': user_data.get('bio', ''), 'p_avatar': user_data.get('avatar_url', '')})

    @classmethod
    def update_profile(cls, full_name, bio='', avatar_url=''):
        try:
            token = cls.get_access_token()
            user = dict(cls._session['user'])
            user.update(full_name=full_name.strip() or user['full_name'], bio=bio.strip(), avatar_url=avatar_url.strip())
            cls.sync_user_profile(user, token)
            cls._session['user'] = user
            return {'success': True, 'status': 'success', 'session': cls.public_session(cls._session), 'message': 'Đã lưu hồ sơ trên cloud.'}
        except (CloudError, OSError, ValueError) as error:
            return failure(error)
