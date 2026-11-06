"""Verify a built candidate against its source manifest; never executes the installer."""
import hashlib
import json
import subprocess
import zipfile
from pathlib import Path


def verify():
    root = Path(__file__).resolve().parents[1]
    version = json.loads((root / 'app/data/version.json').read_text(encoding='utf-8'))['version']
    archive = root / 'dist' / f'AbyssalSkillsD-v{version}-Portable.zip'
    with zipfile.ZipFile(archive) as package:
        names = package.namelist()
        data_root = 'AbyssalSkillsD/_internal/app/data/'
        allowed = {'skills_registry.json', 'supabase_config.json', 'version.json', 'build_manifest.json'}
        actual = {name.removeprefix(data_root) for name in names if name.startswith(data_root)}
        assert actual == allowed, f'Unexpected bundled runtime data: {actual - allowed}'
        assert not any('auth_session' in name or 'pending_diagnostics' in name or '/repos/' in name for name in names)
        manifest = json.loads(package.read(data_root + 'build_manifest.json'))
        assert manifest['commit'] == subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
        for name, digest in manifest['files'].items():
            assert hashlib.sha256((root / name).read_bytes()).hexdigest() == digest, f'Build input changed: {name}'
            archive_name = 'AbyssalSkillsD/_internal/' + name
            if archive_name in names:
                assert hashlib.sha256(package.read(archive_name)).hexdigest() == digest, f'Bundled input differs: {name}'
        config = json.loads(package.read(data_root + 'supabase_config.json'))
        assert 'service_secret_key' not in config
        registry = json.loads(package.read(data_root + 'skills_registry.json'))
        assert len(registry) == 36
        assert all(not item['installed_targets'] and item['installed_path'] is None for item in registry)
    setup = root / 'dist' / f'AbyssalSkillsD-Setup-v{version}.exe'
    assert setup.is_file() and setup.read_bytes()[:2] == b'MZ'
    print(f'PASS: {version} package provenance, source hashes, clean data allowlist, registry and Windows setup header.')


if __name__ == '__main__':
    verify()
