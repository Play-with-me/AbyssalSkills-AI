# -*- mode: python ; coding: utf-8 -*-
"""
AbyssalSkillsD PyInstaller Specification
Builds standalone Windows distribution with Microsoft Edge WebView2 and WinForms backend.
Zero Python runtime required on target machine.
"""
from pathlib import Path
import sys
import json
import subprocess
import hashlib

block_cipher = None

# Asset data tuples: (source_path, dest_subfolder)
bundle_data = Path('build/package-data')
bundle_data.mkdir(parents=True, exist_ok=True)
registry = json.loads(Path('app/data/skills_registry.json').read_text(encoding='utf-8'))
for item in registry:
    item.update(installed_targets=[], installed_path=None, has_update=False, always_on_enabled=False, is_favorite=False)
(bundle_data / 'skills_registry.json').write_text(json.dumps(registry, ensure_ascii=False), encoding='utf-8')
config = json.loads(Path('app/data/supabase_config.json').read_text(encoding='utf-8'))
config = {key: config.get(key, '') for key in ('supabase_url','anon_key','project_name')}
(bundle_data / 'supabase_config.json').write_text(json.dumps(config), encoding='utf-8')
source_files = sorted([*Path('app/backend').glob('*.py'), *Path('app/frontend').rglob('*.js'), *Path('app/frontend').rglob('*.css'), Path('app/frontend/index.html'), Path('main.py'), Path('app/data/version.json'), Path('abyssalskillsd.spec'), Path('pyproject.toml'), Path('uv.lock')])
manifest = {'commit': subprocess.check_output(['git','rev-parse','HEAD'], text=True).strip(),
            'files': {file.as_posix(): hashlib.sha256(file.read_bytes()).hexdigest() for file in source_files}}
(bundle_data / 'build_manifest.json').write_text(json.dumps(manifest, indent=2), encoding='utf-8')
datas = [('app/frontend', 'app/frontend'),
         (str(bundle_data / 'skills_registry.json'), 'app/data'),
         (str(bundle_data / 'supabase_config.json'), 'app/data'),
         (str(bundle_data / 'build_manifest.json'), 'app/data'),
         ('app/data/version.json', 'app/data')]

# Hidden imports for PyWebView, Windows WinForms/Edge WebView2, and app backend
hidden_imports = [
    'webview',
    'webview.platforms.winforms',
    'clr',
    'System.Windows.Forms',
    'app',
    'app.backend',
    'app.backend.paths',
    'app.backend.api',
    'app.backend.storage',
    'app.backend.models',
    'app.backend.scanner',
    'app.backend.installer',
    'app.backend.git_sync',
    'app.backend.auth',
    'app.backend.updater',
    'app.backend.cloud_client',
    'app.backend.community',
    'app.backend.logger',
    'app.backend.secure_storage',
    'app.backend.telemetry',
]

a = Analysis(
    ['main.py'],
    pathex=['.'],
    binaries=[],
    datas=datas,
    hiddenimports=hidden_imports,
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['tkinter', 'test', 'unittest', 'IPython', 'pytest', 'matplotlib', 'scipy', 'numpy'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='AbyssalSkillsD',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='app/frontend/assets/logo/app-icon.ico',
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='AbyssalSkillsD',
)
