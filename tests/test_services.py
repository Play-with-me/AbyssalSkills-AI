import json
import unittest
from unittest.mock import patch
from pathlib import Path
import sys
tests_dir = str(Path(__file__).resolve().parent)
if tests_dir not in sys.path:
    sys.path.insert(0, tests_dir)
import test_reliability as reliability


class ServiceTests(unittest.TestCase):
    def setUp(self):
        reliability.ReliabilityTests.setUp(self)
        import app.backend.paths as paths
        self.enterContext(patch.object(paths, 'get_data_dir', return_value=self.data))

    def test_sanitizer_covers_spaces_and_bearer(self):
        from app.backend.logger import sanitize_sensitive_data
        text = sanitize_sensitive_data('password="private long value" Authorization: Bearer opaque_token email=person@example.invalid')
        for secret in ('private', 'long value', 'opaque_token', 'person@example.invalid'):
            self.assertNotIn(secret, text)

    def test_preview_never_sends_and_retry_is_idempotent(self):
        from app.backend.telemetry import TelemetryService
        from app.backend.cloud_client import CloudError
        with patch('app.backend.telemetry.get_data_dir', return_value=self.data), patch('app.backend.telemetry.CloudClient.rpc') as rpc:
            preview = TelemetryService.prepare({'error_message': 'failure', 'traceback': 'fake trace', 'metadata': {'private': 'do not send'}})
            rpc.assert_not_called()
            self.assertNotIn('metadata', preview['payload'])
            with patch('app.backend.auth.AuthEngine.get_access_token', return_value='fake'):
                rpc.side_effect = CloudError('offline')
                first = TelemetryService.send(preview['request_id'])
                self.assertFalse(first['success'])
                self.assertTrue(TelemetryService.file().exists())
                rpc.side_effect = None
                rpc.return_value = {'accepted': True, 'occurrences': 1}
                self.assertTrue(TelemetryService.send(preview['request_id'])['success'])
                self.assertEqual(rpc.call_args.args[1]['p_request'], preview['request_id'])
                self.assertFalse(TelemetryService.file().exists())

    def test_catalog_failure_is_not_seeded_cloud_success(self):
        from app.backend.community import CommunityService
        from app.backend.cloud_client import CloudError
        with patch('app.backend.community.get_data_dir', return_value=self.data), patch.object(CommunityService, 'client', side_effect=CloudError('offline')):
            result = CommunityService.list_skills()
        self.assertFalse(result['success'])
        self.assertEqual(result['skills'], [])

    def test_publish_requires_valid_documents_and_server_ack(self):
        from app.backend.community import CommunityService
        from app.backend.cloud_client import CloudError
        with patch.object(CommunityService, 'client', side_effect=CloudError('offline')):
            result = CommunityService.publish({'id': 'test', 'content': '# Test'})
        self.assertFalse(result['success'])

    def test_multi_ide_sync_all_ais_deploys_to_all_environments(self):
        from app.backend.installer import SkillInstaller
        from app.backend.models import SkillItem
        skill = SkillItem('multi-ide-skill', 'multi-ide-skill', 'Multi IDE Skill', '1.0.0', 'Desc', 'Category', skill_content='# Test Content')
        all_targets = ["antigravity", "claude", "copilot", "cursor", "windsurf", "codex", "workspace"]
        res = SkillInstaller.sync_all_ais([skill], targets=all_targets, workspace_path=str(self.workspace), overwrite=True)
        self.assertTrue(res['success'], res.get('errors'))
        self.assertEqual(res['total_skills'], 1)
        for t in all_targets:
            self.assertEqual(res['target_counts'][t], 1, f"Target {t} count should be 1")
        # Verify files on disk
        destinations = SkillInstaller.target_dirs(skill.id, str(self.workspace))
        for t in all_targets:
            dest = destinations[t]
            self.assertTrue((dest / 'SKILL.md').exists(), f"SKILL.md missing at {dest}")

    def test_community_publish_clears_cache_and_refreshes_list(self):
        from app.backend.community import CommunityService
        from app.backend.paths import atomic_write
        cache_dir = self.data / 'community_cache'
        cache_dir.mkdir(parents=True, exist_ok=True)
        dummy_cache = cache_dir / 'test_old.json'
        atomic_write(dummy_cache, '{"old": true}')
        self.assertTrue(dummy_cache.exists())

        # Simulate publish success with mock client
        with patch('app.backend.community.get_data_dir', return_value=self.data), \
             patch.object(CommunityService, 'client') as mock_client:
            mock_client.return_value.rpc.return_value = {
                'id': 'cloud-uuid-123',
                'slug': 'test-skill',
                'display_title': 'Test Skill',
                'author_id': 'author-uuid'
            }
            res = CommunityService.publish({'id': 'test-skill', 'content': '# Hello World'})
            self.assertTrue(res['success'])
            # Cache file should be removed
            self.assertFalse(dummy_cache.exists())

    def test_updater_download_and_progress_flow(self):
        from app.backend.updater import UpdateEngine
        from unittest.mock import MagicMock
        mock_resp = MagicMock()
        mock_resp.headers = {'content-length': '1024'}
        mock_resp.read.side_effect = [b'X' * 512, b'Y' * 512, b'']
        mock_resp.__enter__.return_value = mock_resp
        with patch('urllib.request.urlopen', return_value=mock_resp):
            res = UpdateEngine.download_and_apply_update("https://example.invalid/Setup.exe")
            self.assertTrue(res['success'], res.get('message'))
            progress = UpdateEngine.get_download_progress()
            self.assertEqual(progress['percent'], 100)
            self.assertEqual(progress['status'], 'ready_to_install')


if __name__ == '__main__':
    unittest.main()
