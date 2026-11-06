"""Launch native PyWebView using isolated state and target directories."""
import os
import sys
from pathlib import Path
from unittest.mock import patch

root = Path(__file__).resolve().parents[1]
sandbox = root / 'build/native-smoke'
for folder in ('home', 'workspace', 'data', 'local'):
    (sandbox / folder).mkdir(parents=True, exist_ok=True)
os.environ['ABYSSAL_DATA_DIR'] = str(sandbox / 'data')
os.environ['LOCALAPPDATA'] = str(sandbox / 'local')
sys.path.insert(0, str(root))
sys.argv[0] = str(Path(__file__).resolve())
os.chdir(sandbox / 'workspace')
with patch.object(Path, 'home', return_value=sandbox / 'home'):
    from app.backend.secure_storage import SecureStorage
    import webview
    import main
    original_create = webview.create_window
    def create(*args, **kwargs):
        kwargs['title'] = 'AbyssalSkillsD — Kiểm thử cô lập 1.1.0'
        return original_create(*args, **kwargs)
    with patch.object(SecureStorage, 'read', return_value=None), patch.object(webview, 'create_window', side_effect=create):
        main.main()
