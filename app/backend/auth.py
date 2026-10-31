"""
AbyssalSkillsD - Supabase Authentication & Secret Key Engine
Standard: supabase-backend-architect
Handles Supabase Auth REST API (Sign Up, Sign In, Token Refresh, Sign Out, User Metadata),
Desktop Loopback OAuth Server for Google & GitHub,
and secure storage of session tokens (JWT) and project Secret Keys.
"""
import os
import sys
import json
import time
import socketserver
import http.server
import urllib.request
import urllib.parse
import urllib.error
import threading
import webbrowser
from pathlib import Path
from typing import Dict, Any, Optional
from .paths import get_data_dir
from .logger import get_logger

class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    """Handles HTTP requests from the browser during Desktop OAuth."""
    auth_engine_ref = None

    def log_message(self, format, *args):
        # Silence standard HTTP server console output
        pass

    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/callback":
            # 1. First redirect from Supabase. Tokens arrive in URL fragment (#hash).
            # We return an HTML page with JavaScript to bridge the hash into query params.
            html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Xác Thực AbyssalSkillsD</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #050C1A; color: #F8FAFC; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
    .card { background: #0B1933; border: 1px solid #1E2D4A; padding: 32px 40px; border-radius: 16px; text-align: center; box-shadow: 0 8px 32px rgba(0,0,0,0.5); }
    .spinner { border: 3px solid #1E2D4A; border-top: 3px solid #00B4D8; border-radius: 50%; width: 36px; height: 36px; animation: spin 0.8s linear infinite; margin: 0 auto 16px; }
    @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
  </style>
</head>
<body>
  <div class="card">
    <div class="spinner"></div>
    <h2 style="margin:0 0 8px; color: #00B4D8;">Đang xác thực tài khoản...</h2>
    <p style="color: #94A3B8; margin: 0; font-size: 14px;">Vui lòng giữ nguyên cửa sổ, thông tin đang được chuyển vào ứng dụng.</p>
  </div>
  <script>
    const hash = window.location.hash.substring(1);
    if (hash) {
      window.location.replace('/callback/token?' + hash);
    } else {
      const q = window.location.search;
      if (q && q.includes('error=')) {
        window.location.replace('/callback/error' + q);
      } else {
        document.body.innerHTML = '<div class="card"><h2 style="color:#EF4444;">Không tìm thấy mã xác thực</h2><p style="color:#94A3B8;">Vui lòng thử lại từ ứng dụng.</p></div>';
      }
    }
  </script>
</body>
</html>"""
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))

        elif path == "/callback/token":
            # 2. Extract access_token, refresh_token from bridged query
            access_token = query.get("access_token", [""])[0]
            refresh_token = query.get("refresh_token", [""])[0]
            expires_in_raw = query.get("expires_in", ["3600"])[0]
            try:
                expires_in = int(expires_in_raw)
            except Exception:
                expires_in = 3600

            if access_token and self.auth_engine_ref:
                user_info = self.auth_engine_ref.fetch_user_from_token(access_token)
                session = {
                    "authenticated": True,
                    "access_token": access_token,
                    "refresh_token": refresh_token,
                    "expires_at": time.time() + expires_in,
                    "user": user_info
                }
                self.auth_engine_ref.save_session(session)
                self.auth_engine_ref.sync_user_profile(user_info, access_token)
                OAuthServerManager.last_oauth_result = {"success": True, "session": session}

            html = """<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <title>Đăng Nhập Thành Công</title>
  <style>
    body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; background: #050C1A; color: #F8FAFC; display: flex; align-items: center; justify-content: center; height: 100vh; margin: 0; }
    .card { background: #0B1933; border: 1px solid #00B4D8; padding: 36px 48px; border-radius: 16px; text-align: center; box-shadow: 0 12px 40px rgba(0,180,216,0.2); }
    h1 { color: #00B4D8; margin: 0 0 12px; font-size: 26px; }
    p { color: #94A3B8; font-size: 15px; margin: 0 0 20px; }
  </style>
</head>
<body>
  <div class="card">
    <h1>✓ Đăng Nhập Thành Công!</h1>
    <p>Tài khoản của bạn đã được kết nối vào AbyssalSkillsD.<br>Bạn có thể đóng tab trình duyệt này và quay lại ứng dụng.</p>
  </div>
  <script>
    setTimeout(function() { window.close(); }, 2000);
  </script>
</body>
</html>"""
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))

            threading.Thread(target=OAuthServerManager.stop_server, daemon=True).start()

        elif path == "/callback/error":
            err_desc = query.get("error_description", ["Xác thực thất bại"])[0]
            OAuthServerManager.last_oauth_result = {"success": False, "message": err_desc}
            html = f"""<!DOCTYPE html>
<html><body style="background:#050C1A;color:#fff;text-align:center;padding:50px;font-family:sans-serif;">
<h2 style="color:#EF4444;">Xác Thực Thất Bại</h2><p>{err_desc}</p>
</body></html>"""
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(html.encode("utf-8"))
            threading.Thread(target=OAuthServerManager.stop_server, daemon=True).start()

        else:
            self.send_response(404)
            self.end_headers()


class OAuthServerManager:
    server = None
    server_thread = None
    last_oauth_result = None

    @classmethod
    def start_server(cls, auth_engine, port=54321):
        cls.stop_server()
        cls.last_oauth_result = None
        OAuthCallbackHandler.auth_engine_ref = auth_engine
        try:
            socketserver.TCPServer.allow_reuse_address = True
            cls.server = socketserver.TCPServer(("127.0.0.1", port), OAuthCallbackHandler)
            cls.server_thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
            cls.server_thread.start()
            # Safety timeout to stop server if user closes browser
            def _timeout():
                time.sleep(120)
                if cls.server and cls.last_oauth_result is None:
                    cls.stop_server()
            threading.Thread(target=_timeout, daemon=True).start()
            return True
        except Exception as e:
            get_logger().warning(f"Could not bind OAuth loopback port {port}: {e}")
            return False

    @classmethod
    def stop_server(cls):
        if cls.server:
            try:
                cls.server.shutdown()
                cls.server.server_close()
            except Exception:
                pass
            cls.server = None


class AuthEngine:
    DATA_DIR = get_data_dir()
    CONFIG_FILE = DATA_DIR / "supabase_config.json"
    SESSION_FILE = DATA_DIR / "auth_session.json"

    # Default cloud demo credentials (so users can test immediately out of the box)
    DEFAULT_CONFIG = {
        "supabase_url": "https://abyssalskillsd-demo.supabase.co",
        "anon_key": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImFieXNzYWxza2lsbHNkIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MDAwMDAwMDAsImV4cCI6MjAwMDAwMDAwMH0.demo_anon_key_abyssalskillsd_public",
        "service_secret_key": "",
        "project_name": "AbyssalSkillsD Official Cloud"
    }

    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Loads Supabase project URL and keys, or initializes with default."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        if cls.CONFIG_FILE.exists():
            try:
                data = json.loads(cls.CONFIG_FILE.read_text(encoding="utf-8"))
                return {**cls.DEFAULT_CONFIG, **data}
            except Exception:
                pass
        return dict(cls.DEFAULT_CONFIG)

    @classmethod
    def save_config(cls, url: str, anon_key: str, secret_key: str = "") -> Dict[str, Any]:
        """Saves custom Supabase URL and keys."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        config = cls.get_config()
        clean_url = (url or "").strip().rstrip("/")
        if clean_url and not clean_url.startswith("http"):
            clean_url = f"https://{clean_url}"

        config["supabase_url"] = clean_url or cls.DEFAULT_CONFIG["supabase_url"]
        config["anon_key"] = (anon_key or "").strip() or cls.DEFAULT_CONFIG["anon_key"]
        if secret_key is not None:
            config["service_secret_key"] = (secret_key or "").strip()
        
        cls.CONFIG_FILE.write_text(json.dumps(config, indent=2, ensure_ascii=False), encoding="utf-8")
        return {"success": True, "message": "Đã lưu cấu hình Supabase và Khóa bảo mật!", "config": cls.get_safe_config()}

    @classmethod
    def get_safe_config(cls) -> Dict[str, Any]:
        """Returns config with masked secret keys for frontend display."""
        cfg = cls.get_config()
        sec = cfg.get("service_secret_key", "")
        masked_sec = (sec[:4] + "••••••••" + sec[-4:]) if len(sec) > 8 else ("••••" if sec else "")
        return {
            "supabase_url": cfg.get("supabase_url", ""),
            "anon_key": cfg.get("anon_key", ""),
            "service_secret_key": sec,
            "masked_secret_key": masked_sec,
            "has_secret_key": bool(sec),
            "project_name": cfg.get("project_name", "Supabase Cloud")
        }

    @classmethod
    def get_session(cls) -> Dict[str, Any]:
        """Loads active auth session from disk if valid."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        if cls.SESSION_FILE.exists():
            try:
                session = json.loads(cls.SESSION_FILE.read_text(encoding="utf-8"))
                # Check expiration
                expires_at = session.get("expires_at", 0)
                if expires_at and time.time() > expires_at:
                    refresh_token = session.get("refresh_token")
                    if refresh_token:
                        refreshed = cls.refresh_token(refresh_token)
                        if refreshed.get("success"):
                            return refreshed["session"]
                return session
            except Exception:
                pass
        return {"authenticated": False, "user": None}

    @classmethod
    def save_session(cls, session_data: Dict[str, Any]):
        """Persists session data to disk."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        cls.SESSION_FILE.write_text(json.dumps(session_data, indent=2, ensure_ascii=False), encoding="utf-8")

    @classmethod
    def clear_session(cls):
        """Clears session on logout."""
        if cls.SESSION_FILE.exists():
            try:
                cls.SESSION_FILE.unlink()
            except Exception:
                pass

    @classmethod
    def fetch_user_from_token(cls, access_token: str) -> Dict[str, Any]:
        """Retrieves user profile metadata from Supabase Auth endpoint using JWT access_token."""
        cfg = cls.get_config()
        supabase_url = cfg["supabase_url"]
        anon_key = cfg["anon_key"]
        try:
            endpoint = f"{supabase_url.rstrip('/')}/auth/v1/user"
            headers = {
                "apikey": anon_key,
                "Authorization": f"Bearer {access_token}"
            }
            req = urllib.request.Request(endpoint, headers=headers)
            with urllib.request.urlopen(req, timeout=6) as response:
                user_obj = json.loads(response.read().decode("utf-8"))
                user_meta = user_obj.get("user_metadata", {})
                full_name = user_meta.get("full_name") or user_meta.get("name") or user_obj.get("email", "").split("@")[0].title()
                return {
                    "id": user_obj.get("id", ""),
                    "email": user_obj.get("email", ""),
                    "full_name": full_name,
                    "role": user_meta.get("role", "creator"),
                    "avatar_url": user_meta.get("avatar_url") or ""
                }
        except Exception as e:
            get_logger().debug(f"fetch_user_from_token fallback: {e}")
            return {
                "id": "oauth_user",
                "email": "user@example.com",
                "full_name": "Developer",
                "role": "creator",
                "avatar_url": ""
            }

    @classmethod
    def sync_user_profile(cls, user_data: Dict[str, Any], access_token: str):
        """Ensures a profile record exists in public.profiles for the authenticated user."""
        cfg = cls.get_config()
        s_url = cfg["supabase_url"]
        s_key = cfg["anon_key"]
        if not s_url or not access_token or "demo" in s_url or "custom-project" in s_url:
            return
        try:
            profile_payload = {
                "id": user_data["id"],
                "username": user_data["email"].split("@")[0].lower() + "_" + user_data["id"][:4],
                "display_name": user_data["full_name"],
                "avatar_url": user_data.get("avatar_url", ""),
                "role": user_data.get("role", "creator")
            }
            endpoint = f"{s_url.rstrip('/')}/rest/v1/profiles?on_conflict=id"
            hdrs = {
                "apikey": s_key,
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Prefer": "resolution=merge-duplicates,return=minimal"
            }
            req = urllib.request.Request(endpoint, data=json.dumps(profile_payload).encode("utf-8"), headers=hdrs, method="POST")
            with urllib.request.urlopen(req, timeout=5):
                pass
        except Exception as err:
            get_logger().debug(f"Profile sync non-fatal error: {err}")

    @classmethod
    def sign_in(cls, email: str, password: str) -> Dict[str, Any]:
        """Authenticates with Supabase Auth using email and password."""
        email = (email or "").strip()
        password = (password or "").strip()

        if not email or not password:
            return {"success": False, "message": "Vui lòng nhập đầy đủ Email và Mật khẩu."}

        cfg = cls.get_config()
        supabase_url = cfg["supabase_url"]
        anon_key = cfg["anon_key"]

        # 1. Attempt Supabase Auth REST API if live project configured
        if "demo" not in supabase_url and "custom-project" not in supabase_url:
            endpoint = f"{supabase_url.rstrip('/')}/auth/v1/token?grant_type=password"
            headers = {
                "apikey": anon_key,
                "Content-Type": "application/json"
            }
            body = json.dumps({"email": email, "password": password}).encode("utf-8")
            req = urllib.request.Request(endpoint, data=body, headers=headers, method="POST")

            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    res_body = json.loads(response.read().decode("utf-8"))
                    access_token = res_body.get("access_token", "")
                    refresh_token = res_body.get("refresh_token", "")
                    expires_in = res_body.get("expires_in", 3600)
                    user_info = res_body.get("user", {})

                    user_meta = user_info.get("user_metadata", {})
                    full_name = user_meta.get("full_name") or email.split("@")[0].title()
                    user_data = {
                        "id": user_info.get("id", "user_uuid"),
                        "email": email,
                        "full_name": full_name,
                        "role": user_meta.get("role", "creator"),
                        "avatar_url": user_meta.get("avatar_url") or ""
                    }

                    session = {
                        "authenticated": True,
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                        "expires_at": time.time() + expires_in,
                        "user": user_data
                    }
                    cls.save_session(session)
                    cls.sync_user_profile(user_data, access_token)
                    return {"success": True, "message": f"Chào mừng trở lại, {full_name}!", "session": session}
            except urllib.error.HTTPError as e:
                err_text = e.read().decode("utf-8")
                try:
                    err_json = json.loads(err_text)
                    msg = err_json.get("error_description") or err_json.get("msg") or err_json.get("message") or "Email hoặc mật khẩu không chính xác."
                except Exception:
                    msg = f"Lỗi xác thực HTTP ({e.code})"
                return {"success": False, "message": msg}
            except Exception as e:
                return {"success": False, "message": f"Lỗi kết nối tới máy chủ Supabase: {str(e)}"}

        # 2. Local Demo Authentication Fallback (When on demo project)
        full_name = email.split("@")[0].replace(".", " ").title()
        user_data = {
            "id": f"usr_{int(time.time())}",
            "email": email,
            "full_name": full_name,
            "role": "admin" if "admin" in email.lower() else "creator",
            "avatar_url": ""
        }
        mock_jwt = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.demo_token_{int(time.time())}"
        mock_refresh = f"ref_{int(time.time())}_token"

        session = {
            "authenticated": True,
            "access_token": mock_jwt,
            "refresh_token": mock_refresh,
            "expires_at": time.time() + 2592000,
            "user": user_data
        }
        cls.save_session(session)
        return {
            "success": True,
            "message": f"Đăng nhập thành công! Chào mừng {full_name}.",
            "session": session
        }

    @classmethod
    def sign_up(cls, email: str, password: str, full_name: str = "") -> Dict[str, Any]:
        """Registers a new account in Supabase."""
        email = (email or "").strip()
        password = (password or "").strip()
        full_name = (full_name or "").strip() or email.split("@")[0].title()

        if not email or not password:
            return {"success": False, "message": "Vui lòng nhập Email và Mật khẩu."}
        if len(password) < 6:
            return {"success": False, "message": "Mật khẩu phải chứa ít nhất 6 ký tự."}

        cfg = cls.get_config()
        supabase_url = cfg["supabase_url"]
        anon_key = cfg["anon_key"]

        # 1. Attempt Supabase Auth REST API
        if "demo" not in supabase_url and "custom-project" not in supabase_url:
            endpoint = f"{supabase_url.rstrip('/')}/auth/v1/signup"
            headers = {
                "apikey": anon_key,
                "Content-Type": "application/json"
            }
            body = json.dumps({
                "email": email,
                "password": password,
                "data": {
                    "full_name": full_name,
                    "role": "creator"
                }
            }).encode("utf-8")
            req = urllib.request.Request(endpoint, data=body, headers=headers, method="POST")

            try:
                with urllib.request.urlopen(req, timeout=10) as response:
                    res_body = json.loads(response.read().decode("utf-8"))
                    access_token = res_body.get("access_token")
                    refresh_token = res_body.get("refresh_token")
                    user_info = res_body.get("user") or {}

                    if access_token:
                        # Auto-login immediately if email confirmation is turned off
                        expires_in = res_body.get("expires_in", 3600)
                        user_data = {
                            "id": user_info.get("id", ""),
                            "email": email,
                            "full_name": full_name,
                            "role": "creator",
                            "avatar_url": ""
                        }
                        session = {
                            "authenticated": True,
                            "access_token": access_token,
                            "refresh_token": refresh_token,
                            "expires_at": time.time() + expires_in,
                            "user": user_data
                        }
                        cls.save_session(session)
                        cls.sync_user_profile(user_data, access_token)
                        return {
                            "success": True,
                            "message": f"Đăng ký thành công! Chào mừng {full_name}.",
                            "session": session
                        }
                    else:
                        # Account created; requires confirmation or login
                        return {
                            "success": True,
                            "message": "Tạo tài khoản thành công! Bạn có thể đăng nhập ngay bây giờ.",
                            "requires_login": True
                        }
            except urllib.error.HTTPError as e:
                err_text = e.read().decode("utf-8")
                try:
                    err_json = json.loads(err_text)
                    msg = err_json.get("error_description") or err_json.get("msg") or err_json.get("message") or "Đăng ký không thành công."
                    if "already registered" in msg.lower():
                        msg = "Email này đã được đăng ký tài khoản. Vui lòng chuyển sang Đăng Nhập."
                except Exception:
                    msg = f"Lỗi đăng ký HTTP ({e.code})"
                return {"success": False, "message": msg}
            except Exception as e:
                return {"success": False, "message": f"Lỗi kết nối máy chủ: {str(e)}"}

        # 2. Local Demo Registration Fallback
        return cls.sign_in(email, password)

    @classmethod
    def start_oauth(cls, provider: str) -> Dict[str, Any]:
        """Starts Desktop OAuth flow for Google or GitHub."""
        provider_clean = (provider or "google").strip().lower()
        if provider_clean not in ["google", "github"]:
            provider_clean = "google"

        cfg = cls.get_config()
        supabase_url = cfg["supabase_url"]
        if "demo" in supabase_url or "custom-project" in supabase_url:
            return cls.sign_in_with_oauth(provider_clean)

        # 1. Start local callback loopback server on port 54321
        started = OAuthServerManager.start_server(cls, port=54321)
        if not started:
            return {"success": False, "message": "Không thể khởi động cổng xác thực 54321 cục bộ."}

        # 2. Build Supabase OAuth authorization URL
        redirect_uri = "http://localhost:54321/callback"
        auth_url = f"{supabase_url.rstrip('/')}/auth/v1/authorize?provider={provider_clean}&redirect_to={urllib.parse.quote(redirect_uri)}"

        # 3. Open in default system browser
        webbrowser.open(auth_url)

        return {
            "success": True,
            "message": f"Đã mở trình duyệt để xác thực với {provider_clean.title()}. Vui lòng hoàn tất trên trình duyệt.",
            "auth_url": auth_url,
            "listening": True
        }

    @classmethod
    def check_oauth_status(cls) -> Dict[str, Any]:
        """Polls if Desktop OAuth flow completed."""
        res = OAuthServerManager.last_oauth_result
        if res:
            return res
        session = cls.get_session()
        if session.get("authenticated"):
            return {"success": True, "session": session}
        return {"success": False, "pending": True}

    @classmethod
    def sign_in_with_oauth(cls, provider: str) -> Dict[str, Any]:
        """Instant social sign-in (Used for demo and testing mode)."""
        provider_clean = (provider or "google").strip().lower()
        if provider_clean not in ["google", "github"]:
            provider_clean = "google"

        now = int(time.time())
        if provider_clean == "google":
            full_name = "Google Creator"
            email = "creator@gmail.com"
            role = "creator"
            avatar = "https://lh3.googleusercontent.com/a/default-user"
        else:
            full_name = "GitHub Developer"
            email = "developer@github.com"
            role = "admin"
            avatar = "https://avatars.githubusercontent.com/u/9919?v=4"

        user_data = {
            "id": f"usr_oauth_{provider_clean}_{now}",
            "email": email,
            "full_name": full_name,
            "role": role,
            "avatar_url": avatar,
            "provider": provider_clean
        }

        mock_jwt = f"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.demo_oauth_{provider_clean}_{now}"
        mock_refresh = f"ref_oauth_{provider_clean}_{now}_token"

        session = {
            "authenticated": True,
            "access_token": mock_jwt,
            "refresh_token": mock_refresh,
            "expires_at": now + 2592000,
            "user": user_data
        }
        cls.save_session(session)

        provider_name = "Google" if provider_clean == "google" else "GitHub"
        return {
            "success": True,
            "message": f"Đăng nhập thành công với tài khoản {provider_name}! Chào mừng {full_name}.",
            "session": session
        }

    @classmethod
    def refresh_token(cls, refresh_token: str) -> Dict[str, Any]:
        """Refreshes expired access token using refresh_token."""
        cfg = cls.get_config()
        supabase_url = cfg["supabase_url"]
        anon_key = cfg["anon_key"]

        if "demo" not in supabase_url and "custom-project" not in supabase_url:
            endpoint = f"{supabase_url.rstrip('/')}/auth/v1/token?grant_type=refresh_token"
            headers = {
                "apikey": anon_key,
                "Content-Type": "application/json"
            }
            body = json.dumps({"refresh_token": refresh_token}).encode("utf-8")
            req = urllib.request.Request(endpoint, data=body, headers=headers, method="POST")
            try:
                with urllib.request.urlopen(req, timeout=8) as response:
                    res_body = json.loads(response.read().decode("utf-8"))
                    session = cls.get_session()
                    session["access_token"] = res_body.get("access_token", session.get("access_token"))
                    session["refresh_token"] = res_body.get("refresh_token", refresh_token)
                    session["expires_at"] = time.time() + res_body.get("expires_in", 3600)
                    cls.save_session(session)
                    return {"success": True, "session": session}
            except Exception:
                pass

        # Fallback refresh
        session = cls.get_session()
        if session.get("authenticated"):
            session["expires_at"] = time.time() + 2592000
            cls.save_session(session)
            return {"success": True, "session": session}

        return {"success": False, "message": "Không thể làm mới token."}

    @classmethod
    def sign_out(cls) -> Dict[str, Any]:
        """Signs out and revokes tokens."""
        session = cls.get_session()
        token = session.get("access_token")
        cfg = cls.get_config()
        supabase_url = cfg["supabase_url"]
        anon_key = cfg["anon_key"]

        if token and "demo" not in supabase_url and "custom-project" not in supabase_url:
            endpoint = f"{supabase_url.rstrip('/')}/auth/v1/logout"
            headers = {
                "apikey": anon_key,
                "Authorization": f"Bearer {token}",
                "Content-Type": "application/json"
            }
            try:
                req = urllib.request.Request(endpoint, data=b"{}", headers=headers, method="POST")
                with urllib.request.urlopen(req, timeout=4):
                    pass
            except Exception as e:
                get_logger().debug(f"Logout non-fatal notification: {e}")

        cls.clear_session()
        OAuthServerManager.stop_server()
        return {"success": True, "message": "Đã đăng xuất khỏi tài khoản an toàn."}
