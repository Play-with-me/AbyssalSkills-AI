"""Offline regression tests. Never installs into the user's home."""
import json
import os
import shutil
import socket
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


class ReliabilityTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.home = self.root / 'home'
        self.workspace = self.root / 'workspace'
        self.data = self.root / 'data'
        for directory in (self.home, self.workspace, self.data):
            directory.mkdir()
        self.enterContext(patch.dict(os.environ, {'ABYSSAL_DATA_DIR': str(self.data), 'LOCALAPPDATA': str(self.root / 'local')}))
        self.enterContext(patch.object(Path, 'home', return_value=self.home))
        self.enterContext(patch.object(socket.socket, 'connect', side_effect=RuntimeError('network forbidden in unit tests')))
        from app.backend.models import SkillItem, InstallRequest
        from app.backend.installer import SkillInstaller
        from app.backend.storage import SkillStorage
        self.installer, self.storage = SkillInstaller, SkillStorage
        self.enterContext(patch.object(SkillStorage, 'DATA_DIR', self.data))
        self.enterContext(patch.object(SkillStorage, 'REGISTRY_FILE', self.data / 'skills_registry.json'))
        self.skill = SkillItem('test-skill', 'test-skill', 'Test', '1', 'Test', 'Test', skill_content='# Test')
        self.request = InstallRequest(self.skill.id, ['workspace'], str(self.workspace), False, False)
        self.storage.save_all_skills([self.skill])

    def test_scaffold_preserves_custom_rules_and_rejects_changed_managed_block(self):
        rules = self.workspace / '.cursorrules'
        rules.write_text('MY OWN RULES\n', encoding='utf-8')
        result = self.installer.generate_rule_scaffold(str(self.workspace), ['cursorrules'], [self.skill])
        self.assertTrue(result['success'])
        self.assertIn('MY OWN RULES', rules.read_text(encoding='utf-8'))
        rules.write_text(rules.read_text(encoding='utf-8').replace('Active Skills', 'Customized Skills'), encoding='utf-8')
        previous = rules.read_bytes()
        self.assertFalse(self.installer.generate_rule_scaffold(str(self.workspace), ['cursorrules'], [self.skill])['success'])
        self.assertEqual(rules.read_bytes(), previous)

    def test_corrupt_registry_is_never_reseeded(self):
        self.storage.REGISTRY_FILE.write_text('{broken', encoding='utf-8')
        with self.assertRaises(ValueError):
            self.storage.get_all_skills()
        self.assertEqual(self.storage.REGISTRY_FILE.read_text(), '{broken')

    def test_windows_filename_aliases_rejected(self):
        from app.backend.paths import safe_child
        for name in ('NUL.md', 'file.', 'folder /file.md', 'bad?.md'):
            with self.subTest(name=name), self.assertRaises(ValueError):
                safe_child(self.workspace, name)

    def test_git_same_named_repositories_have_distinct_cache_and_content(self):
        import shutil
        if not shutil.which('git'):
            self.skipTest('Git unavailable; integration is not verified')
        from app.backend.git_sync import GitSyncEngine
        with patch.object(GitSyncEngine, 'REPOS_DIR', self.data / 'repos'):
            installed = []
            for owner in ('first', 'second'):
                repo = self.root / owner / 'same-name'
                repo.mkdir(parents=True)
                subprocess.run(['git', 'init', str(repo)], check=True, capture_output=True)
                (repo / 'content.txt').write_text(owner)
                subprocess.run(['git', '-C', str(repo), 'add', '.'], check=True, capture_output=True)
                subprocess.run(['git', '-C', str(repo), '-c', 'user.name=Test', '-c', 'user.email=test@example.invalid', 'commit', '-m', 'fixture'], check=True, capture_output=True)
                ok, message, cached = GitSyncEngine.clone_or_pull(repo.as_posix())
                self.assertTrue(ok, message)
                self.assertEqual((cached / 'content.txt').read_text(), owner)
                installed.append(cached)
            self.assertNotEqual(*installed)
            with patch('app.backend.git_sync.subprocess.run', side_effect=FileNotFoundError('git missing')):
                self.assertFalse(GitSyncEngine.clone_or_pull('https://example.invalid/missing/repo')[0])

    def test_javascript_parses(self):
        if not shutil.which('node'):
            self.skipTest('node runtime not available')
        for source in (Path(__file__).resolve().parents[1] / 'app/frontend/js').glob('*.js'):
            result = subprocess.run(['node', '--check', str(source)], capture_output=True, text=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)

    def test_traversal_rejected_before_writing(self):
        self.skill.id = '../../../escaped'
        result = self.installer.install(self.skill, self.request)
        self.assertFalse(result.success)
        self.assertFalse((self.root / 'escaped').exists())

    def test_backup_failure_preserves_existing_content(self):
        self.installer.install(self.skill, self.request)
        destination = self.workspace / '.agents/skills/test-skill/SKILL.md'
        destination.write_text('MY CUSTOM CONTENT', encoding='utf-8')
        self.request.overwrite = True
        with patch('shutil.copy2', side_effect=PermissionError('backup denied')):
            result = self.installer.install(self.skill, self.request)
        self.assertFalse(result.success)
        self.assertEqual(destination.read_text(), 'MY CUSTOM CONTENT')

    def test_failed_save_raises_and_preserves_registry(self):
        previous = self.storage.REGISTRY_FILE.read_bytes()
        with patch.object(Path, 'replace', side_effect=PermissionError('denied')):
            with self.assertRaises(OSError):
                self.storage.save_all_skills([])
        self.assertEqual(self.storage.REGISTRY_FILE.read_bytes(), previous)

    def test_unknown_target_not_success(self):
        result = self.installer.sync_all_ais([self.skill], ['unknown'], str(self.workspace))
        self.assertFalse(result['success'])

    def test_reference_change_detected(self):
        from app.backend.models import ReferenceDoc
        self.skill.references = [ReferenceDoc('ref', 'Ref', 'guide.md', 'original')]
        self.storage.save_all_skills([self.skill])
        self.installer.install(self.skill, self.request)
        (self.workspace / '.agents/skills/test-skill/references/guide.md').write_text('custom')
        self.assertTrue(self.storage.get_skill(self.skill.id, str(self.workspace)).has_update)

    def test_favorite_is_persisted(self):
        self.assertTrue(self.storage.toggle_favorite(self.skill.id))
        self.assertTrue(self.storage.get_skill(self.skill.id).is_favorite)

    def test_empty_graph_has_no_fabricated_metrics(self):
        from app.backend.api import DesktopAPI
        with patch.object(self.storage, 'initialize'):
            api = DesktopAPI()
        result = api.run_graphify(str(self.workspace))
        self.assertFalse(result['success'])
        self.assertEqual(result['nodes_count'], 0)

    def test_references_cannot_escape_install_directory(self):
        from app.backend.models import ReferenceDoc
        self.skill.references = [ReferenceDoc('x', 'x', '../../escaped.md', 'bad')]
        result = self.installer.install(self.skill, self.request)
        self.assertFalse(result.success)
        self.assertFalse((self.workspace / '.agents/skills/test-skill/SKILL.md').exists())

    def test_rule_install_and_uninstall_preserve_user_content(self):
        from app.backend.models import RuleDoc
        self.skill.rules = [RuleDoc('r', 'Rule', 'always-on-autopilot.md', 'APP RULE')]
        self.request.enable_always_on = True
        rule = self.workspace / '.cursorrules'
        rule.write_text('MY CONVENTIONS\n', encoding='utf-8')
        self.assertTrue(self.installer.install(self.skill, self.request).success)
        self.assertIn('MY CONVENTIONS', rule.read_text())
        self.assertIn('APP RULE', rule.read_text())
        self.assertTrue(self.installer.uninstall(self.skill.id, ['workspace'], str(self.workspace))['success'])
        self.assertIn('MY CONVENTIONS', rule.read_text())
        self.assertNotIn('APP RULE', rule.read_text())

    def test_multi_target_results_and_aider_detection(self):
        from app.backend.scanner import SkillScanner
        self.request.targets = list(self.installer.TARGETS)
        result = self.installer.install(self.skill, self.request)
        self.assertTrue(result.success)
        self.assertEqual(len(result.results), 8)
        detected = SkillScanner.get_installed_targets_map(str(self.workspace))
        self.assertIn('aider', detected[self.skill.id])

    def test_stale_diff_cannot_overwrite_new_edit(self):
        from app.backend.api import DesktopAPI
        self.installer.install(self.skill, self.request)
        with patch.object(self.storage, 'initialize'):
            api = DesktopAPI()
        api.active_workspace = str(self.workspace)
        view = api.get_skill_diff({'skill_id': self.skill.id})
        destination = Path(view['local_path'])
        destination.write_text('NEW EDIT', encoding='utf-8')
        result = api.apply_skill_diff({'skill_id': self.skill.id, 'apply_all': True, 'revision_token': view['revision_token']})
        self.assertFalse(result['success'])
        self.assertEqual(result['error_code'], 'STALE_DIFF')
        self.assertEqual(destination.read_text(), 'NEW EDIT')

    def test_diff_includes_references_and_applies_selected_file(self):
        from app.backend.api import DesktopAPI
        from app.backend.models import ReferenceDoc
        self.skill.references = [ReferenceDoc('r', 'Ref', 'guide.md', 'UPSTREAM')]
        self.storage.save_all_skills([self.skill])
        self.installer.install(self.skill, self.request)
        reference = self.workspace / '.agents/skills/test-skill/references/guide.md'
        reference.write_text('LOCAL', encoding='utf-8')
        with patch.object(self.storage, 'initialize'):
            api = DesktopAPI()
        api.active_workspace = str(self.workspace)
        view = api.get_skill_diff({'skill_id': self.skill.id, 'file_path': str(reference)})
        self.assertTrue(any(Path(item['path']).resolve() == reference.resolve() for item in view['files']))
        result = api.apply_skill_diff({'skill_id': self.skill.id, 'apply_all': True, 'revision_token': view['revision_token']})
        self.assertTrue(result['success'])
        self.assertEqual(reference.read_text(), 'UPSTREAM')

    def test_registry_contains_bundled_suite(self):
        data = json.loads((Path(__file__).resolve().parents[1] / 'app/data/skills_registry.json').read_text(encoding='utf-8'))
        self.assertEqual(len(data), 37)
        self.assertIn('honest-advisor', {item['id'] for item in data})
        self.assertEqual(sum(len(item.get('references', [])) for item in data), 237)
        self.assertEqual(sum(item.get('is_persona', False) for item in data), 4)

    def test_concurrent_saves_do_not_lose_skills(self):
        from concurrent.futures import ThreadPoolExecutor
        from dataclasses import replace
        with ThreadPoolExecutor(max_workers=4) as pool:
            list(pool.map(lambda index: self.storage.upsert_skill(replace(self.skill, id=f'parallel-{index}')), range(12)))
        self.assertEqual(len(self.storage.get_all_skills(str(self.workspace))), 13)

    def test_cancelled_batch_does_not_write_new_skills(self):
        import threading
        event = threading.Event()
        event.set()
        result = self.installer.sync_all_ais([self.skill], ['workspace'], str(self.workspace), event)
        self.assertEqual(result['status'], 'cancelled')
        self.assertFalse(result['success'])
        self.assertFalse((self.workspace / '.agents').exists())

    def test_junction_is_rejected_without_touching_destination(self):
        target = self.root / 'outside'
        target.mkdir()
        link = self.workspace / '.agents'
        if os.name == 'nt':
            result = subprocess.run(['cmd', '/c', 'mklink', '/J', str(link), str(target)], capture_output=True, timeout=10)
            self.assertEqual(result.returncode, 0)
        else:
            link.symlink_to(target, target_is_directory=True)
        result = self.installer.install(self.skill, self.request)
        self.assertFalse(result.success)
        self.assertEqual(list(target.iterdir()), [])

    def test_idempotent_install_skips_when_identical(self):
        # First install creates files
        res1 = self.installer.install(self.skill, self.request)
        self.assertTrue(res1.success)
        dest = self.workspace / '.agents' / 'skills' / self.skill.id / 'SKILL.md'
        self.assertTrue(dest.is_file())

        # Second install with identical content returns 'already_installed'
        res2 = self.installer.install(self.skill, self.request)
        self.assertTrue(res2.success)
        self.assertEqual(res2.status, 'already_installed')
        self.assertIn('khớp 100%', res2.message)

    def test_deduplicate_all_targets_cleans_nested_and_uuid(self):
        ws_skills = self.workspace / '.agents' / 'skills'
        ws_skills.mkdir(parents=True, exist_ok=True)
        
        # 1. Create a skill with nested subfolder
        parent = ws_skills / 'parent-skill'
        parent.mkdir()
        (parent / 'SKILL.md').write_text('---\nname: parent-skill\n---\n# Parent', encoding='utf-8')
        nested = parent / 'nested-child'
        nested.mkdir()
        (nested / 'SKILL.md').write_text('---\nname: nested-child\n---\n# Child', encoding='utf-8')

        # 2. Create a duplicate UUID folder with the same name as parent-skill
        uuid_folder = ws_skills / '01794859-a6f6-4f45-bfd2-618ddc1c13f4'
        uuid_folder.mkdir()
        (uuid_folder / 'SKILL.md').write_text('---\nname: parent-skill\n---\n# Duplicate', encoding='utf-8')

        dedup_res = self.installer.deduplicate_all_targets(str(self.workspace))
        self.assertTrue(dedup_res['success'])
        self.assertGreaterEqual(dedup_res['actions_count'], 2)

        # Verify nested child was removed from inside parent
        self.assertFalse((parent / 'nested-child').exists())

        # Verify duplicate UUID folder was removed/archived
        self.assertFalse(uuid_folder.exists())
        self.assertTrue((parent / 'SKILL.md').exists())

    def test_api_concurrency_lock_prevents_spam(self):
        from app.backend.api import DesktopAPI
        api = DesktopAPI()
        api.active_workspace = str(self.workspace)
        api._install_locks.add('test-skill')
        res = api.install_skill({'skill_id': 'test-skill'})
        self.assertFalse(res['success'])
        self.assertEqual(res['error_code'], 'ALREADY_INSTALLING')
        api._install_locks.clear()


if __name__ == '__main__':
    unittest.main()
