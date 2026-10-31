# -*- mode: python ; coding: utf-8 -*-
"""
AbyssalSkillsD PyInstaller Specification
Builds standalone Windows distribution with Microsoft Edge WebView2 and WinForms backend.
Zero Python runtime required on target machine.
"""
from pathlib import Path
import sys

block_cipher = None

# Asset data tuples: (source_path, dest_subfolder)
datas = [
    ('app/frontend', 'app/frontend'),
    ('app/data', 'app/data'),
]

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
