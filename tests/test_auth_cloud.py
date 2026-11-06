import time
import unittest
from unittest.mock import patch
import test_reliability as reliability


class AuthTests(unittest.TestCase):
    def setUp(self):
        reliability.ReliabilityTests.setUp(self)
        from app.backend.auth import AuthEngine
        self.auth = AuthEngine
        self.enterContext(patch.object(AuthEngine, '_session', None))
        self.enterContext(patch.object(AuthEngine, '_session_project', None))
        self.enterContext(patch.object(AuthEngine, 'DATA_DIR', self.data))
        self.enterContext(patch.object(AuthEngine, 'CONFIG_FILE', self.data / 'config.json'))
        self.enterContext(patch.object(AuthEngine, 'SESSION_FILE', self.data / 'session.json'))

    def test_oauth_never_creates_demo_session(self):
        from app.backend.cloud_client import CloudError
        with patch('app.backend.cloud_client.CloudClient.request', side_effect=CloudError('offline')), patch('webbrowser.open', return_value=False):
            result = self.auth.sign_in_with_oauth('github')
        self.assertFalse(result.get('session', {}).get('authenticated', False))

    def test_safe_config_does_not_return_service_secret(self):
        with patch.object(self.auth, 'get_config', return_value={'supabase_url': 'https://example.supabase.co', 'anon_key': 'public', 'service_secret_key': 'SENSITIVE'}):
            self.assertNotIn('SENSITIVE', str(self.auth.get_safe_config()))

    def test_failed_refresh_does_not_make_session_valid(self):
        from app.backend.cloud_client import CloudError
        with patch('app.backend.cloud_client.CloudClient.request', side_effect=CloudError('offline')):
            result = self.auth.refresh_token('invalid')
        self.assertFalse(result['success'])

    def test_public_session_never_contains_tokens(self):
        public = self.auth.public_session({'user': {'id': 'test'}, 'expires_at': time.time() + 100,
                                           'access_token': 'PRIVATE_ACCESS', 'refresh_token': 'PRIVATE_REFRESH'})
        self.assertNotIn('PRIVATE_', str(public))

    def test_windows_credential_store_roundtrip(self):
        import sys
        import uuid
        from app.backend.secure_storage import SecureStorage
        if sys.platform != 'win32':
            with self.assertRaises(OSError):
                SecureStorage.read('test')
            return
        project = 'isolated-unit-test-' + uuid.uuid4().hex
        self.addCleanup(SecureStorage.delete, project)
        SecureStorage.write(project, 'fake-refresh-token-for-test')
        self.assertEqual(SecureStorage.read(project), 'fake-refresh-token-for-test')

    def test_callback_rejects_unrelated_attempt_before_token_exchange(self):
        import io
        from app.backend.auth import OAuthCallbackHandler, OAuthServerManager
        handler = object.__new__(OAuthCallbackHandler)
        handler.path = '/callback?app_state=wrong&code=FAKE'
        handler.send_error = unittest.mock.Mock()
        with patch.object(OAuthServerManager, 'nonce', 'expected'), patch('app.backend.cloud_client.CloudClient.request') as request:
            handler.do_GET()
        request.assert_not_called()
        handler.send_error.assert_called_once()


if __name__ == '__main__':
    unittest.main()
