"""User-initiated diagnostics; retries reuse request IDs and never send in background."""
import hashlib
import json
import uuid
from .auth import AuthEngine
from .cloud_client import CloudClient, CloudError, failure
from .logger import sanitize_sensitive_data
from .paths import get_data_dir, atomic_write
from .updater import UpdateEngine


class TelemetryService:
    @staticmethod
    def file():
        return get_data_dir() / 'pending_diagnostics.json'

    @classmethod
    def pending(cls):
        try:
            record = json.loads(cls.file().read_text(encoding='utf-8'))
            return {'success': True, 'status': 'success', **record}
        except FileNotFoundError:
            return {'success': True, 'status': 'success', 'request_id': None}
        except (OSError, ValueError) as error:
            return failure(error)

    @classmethod
    def prepare(cls, payload):
        # A strict allowlist is the boundary; metadata and arbitrary machine paths are excluded.
        allowed = {key: sanitize_sensitive_data(str(payload.get(key) or ''))[:12000]
                   for key in ('error_type', 'error_message', 'module_name', 'traceback')}
        allowed['app_version'] = UpdateEngine.get_version_info()['version']
        allowed['fingerprint'] = hashlib.sha256(json.dumps([allowed['error_type'], allowed['module_name'], allowed['error_message']], ensure_ascii=False).encode()).hexdigest()
        record = {'request_id': str(uuid.uuid4()), 'payload': allowed}
        atomic_write(cls.file(), json.dumps(record, ensure_ascii=False))
        return {'success': True, 'status': 'success', **record, 'message': 'Nội dung xem trước; chưa gửi dữ liệu.'}

    @classmethod
    def send(cls, request_id):
        try:
            record = json.loads(cls.file().read_text(encoding='utf-8'))
            if record['request_id'] != request_id:
                raise ValueError('Bản xem trước đã thay đổi. Vui lòng xem lại trước khi gửi.')
            result = CloudClient(token=AuthEngine.get_access_token(required=True)).rpc('submit_diagnostic',
                       {'p_request': request_id, 'p_payload': record['payload']})
            cls.file().unlink(missing_ok=True)
            return {'success': True, 'status': 'success', **result, 'message': 'Máy chủ đã xác nhận nhận báo cáo.'}
        except (CloudError, OSError, ValueError, KeyError) as error:
            return {**failure(error), 'pending': cls.file().exists()}

    @classmethod
    def discard(cls):
        cls.file().unlink(missing_ok=True)
        return {'success': True, 'status': 'success', 'message': 'Đã xóa bản chờ trên máy.'}
