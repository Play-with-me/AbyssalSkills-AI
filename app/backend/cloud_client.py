"""Bounded Supabase HTTP transport shared by authentication and cloud services."""
import json
import ssl
import urllib.error
import urllib.parse
import urllib.request


class CloudError(Exception):
    def __init__(self, message, code='CLOUD_UNAVAILABLE', status=0):
        super().__init__(message)
        self.code, self.status = code, status


class NoCloudRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        raise CloudError('Cloud chuyển hướng ngoài hợp đồng; đã dừng để bảo vệ phiên.', 'UNEXPECTED_REDIRECT')


class CloudClient:
    def __init__(self, config=None, token=None):
        if config is None:
            from .auth import AuthEngine
            config = AuthEngine.get_config()
        self.config, self.token = config, token

    def request(self, path, method='GET', payload=None, query=None):
        base = self.config.get('supabase_url', '').rstrip('/')
        parsed = urllib.parse.urlparse(base)
        key = self.config.get('anon_key', '')
        if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password or not key:
            raise CloudError('Chưa có cấu hình cloud HTTPS hợp lệ.', 'CLOUD_NOT_CONFIGURED')
        url = base + '/' + path.lstrip('/')
        if query:
            url += '?' + urllib.parse.urlencode(query)
        headers = {'apikey': key, 'Authorization': 'Bearer ' + (self.token or key),
                   'Content-Type': 'application/json', 'Accept': 'application/json'}
        data = json.dumps(payload, ensure_ascii=False).encode('utf-8') if payload is not None else None
        if data and len(data) > 2_000_000:
            raise CloudError('Nội dung vượt giới hạn 2 MB.', 'PAYLOAD_TOO_LARGE')
        request = urllib.request.Request(url, data=data, headers=headers, method=method)
        try:
            context = ssl.create_default_context()
            # P-256 keeps certificate verification and TLS 1.3 while avoiding the
            # large hybrid ClientHello that times out on the tested Windows network.
            context.set_ecdh_curve('prime256v1')
            opener = urllib.request.build_opener(NoCloudRedirect(), urllib.request.HTTPSHandler(context=context))
            with opener.open(request, timeout=12) as response:
                raw = response.read(8_000_001)
            if len(raw) > 8_000_000:
                raise CloudError('Phản hồi cloud vượt giới hạn.', 'RESPONSE_TOO_LARGE')
            return json.loads(raw) if raw else None
        except urllib.error.HTTPError as error:
            try:
                body = json.loads(error.read(8192))
            except (ValueError, OSError):
                body = {}
            code = str(body.get('code') or body.get('error_code') or 'HTTP_' + str(error.code))
            messages = {400: 'Yêu cầu không hợp lệ hoặc mã xác thực đã hết hạn.',
                        401: 'Phiên đăng nhập không hợp lệ. Vui lòng đăng nhập lại.',
                        403: 'Bạn không có quyền thực hiện thao tác này.',
                        404: 'Chức năng cloud chưa sẵn sàng hoặc nội dung không tồn tại.',
                        409: 'Dữ liệu đã thay đổi hoặc tên này đã được sử dụng.',
                        429: 'Bạn gửi quá nhanh. Vui lòng thử lại sau.'}
            raise CloudError(messages.get(error.code, 'Máy chủ chưa xử lý được yêu cầu.'), code, error.code) from None
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            raise CloudError('Không kết nối được cloud. Dữ liệu chưa được xác nhận gửi thành công.', 'NETWORK_ERROR') from error

    def rpc(self, name, payload=None):
        return self.request('rest/v1/rpc/' + name, 'POST', payload or {})


def failure(error):
    return {'success': False, 'status': 'error', 'error_code': getattr(error, 'code', 'OPERATION_FAILED'),
            'message': str(error)}
