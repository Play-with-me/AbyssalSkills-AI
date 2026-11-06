"""
AbyssalSkillsD - Runtime Path Resolver
Ensures seamless discovery of frontend assets, user data directories,
and icon files across development mode and packaged frozen PyInstaller executable mode.
"""
import sys
import os
import re
import shutil
import tempfile
import time
from pathlib import Path
from typing import Any, Optional, Union, Dict, List, Tuple


def validate_skill_id(value: str) -> str:
    if not isinstance(value, str) or not re.fullmatch(r'[a-zA-Z0-9][a-zA-Z0-9_-]{0,127}', value):
        raise ValueError('Mã kỹ năng chỉ được chứa chữ, số, dấu gạch ngang và gạch dưới.')
    if value.split('.')[0].upper() in {'CON', 'PRN', 'AUX', 'NUL', *(f'COM{i}' for i in range(1, 10)), *(f'LPT{i}' for i in range(1, 10))}:
        raise ValueError('Mã kỹ năng là tên dành riêng của hệ điều hành.')
    return value


def safe_child(root: Path, relative: str) -> Path:
    """Reject traversal and any existing symlink/junction, including parents."""
    rel = Path(relative)
    if rel.is_absolute() or rel.drive or not relative or any(p in ('..', '.') for p in rel.parts) or ':' in relative or '\\' in relative:
        raise ValueError('Đường dẫn tệp không an toàn.')
    reserved = {'CON', 'PRN', 'AUX', 'NUL', *(f'COM{i}' for i in range(1, 10)), *(f'LPT{i}' for i in range(1, 10))}
    if any(part.endswith((' ', '.')) or part.split('.')[0].upper() in reserved or any(c in part for c in '<>"|?*') for part in rel.parts):
        raise ValueError('Tên tệp không hợp lệ trên Windows.')
    candidate = root / rel
    for part in (candidate, *candidate.parents):
        if part.is_symlink() or (hasattr(part, 'is_junction') and part.is_junction()):
            raise ValueError('Không ghi hoặc xóa qua liên kết thư mục.')
    if not candidate.resolve().is_relative_to(root.resolve()):
        raise ValueError('Tệp nằm ngoài thư mục đích.')
    return candidate


def atomic_write(path: Path, content: str, backup: bool = False) -> None:
    """Backup must succeed before replacing a file. Never fall back to truncation."""
    for parent in (path, *path.parents):
        if parent.is_symlink() or (hasattr(parent, 'is_junction') and parent.is_junction()):
            raise ValueError('Không ghi qua liên kết thư mục.')
    path.parent.mkdir(parents=True, exist_ok=True)
    if backup and path.exists():
        previous = path.read_text(encoding='utf-8')
        if previous == content:
            return
        shutil.copy2(path, path.with_name(f'{path.name}.{time.time_ns()}.bak'))
    fd, temporary = tempfile.mkstemp(prefix=f'.{path.name}.', suffix='.tmp', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8', newline='') as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        Path(temporary).replace(path)
    finally:
        Path(temporary).unlink(missing_ok=True)

def get_app_root() -> Path:
    """
    Returns the root directory of the application.
    In frozen (PyInstaller) mode, uses sys._MEIPASS or executable directory.
    In development mode, resolves relative to this file.
    """
    if getattr(sys, "frozen", False):
        meipass = getattr(sys, "_MEIPASS", None)
        if meipass and (Path(meipass) / "app").exists():
            return Path(meipass).resolve()
        exe_dir = Path(sys.executable).resolve().parent
        if (exe_dir / "_internal" / "app").exists():
            return (exe_dir / "_internal").resolve()
        return exe_dir
    return Path(__file__).resolve().parent.parent.parent

def get_data_dir() -> Path:
    """Writable user state is separate from the read-only application bundle."""
    import json
    override = os.environ.get('ABYSSAL_DATA_DIR')
    if override:
        directory = Path(override).resolve()
    elif sys.platform == 'win32':
        directory = Path(os.environ.get('APPDATA', str(Path.home() / 'AppData/Roaming'))) / 'AbyssalSkillsD/data'
    else:
        directory = Path.home() / '.local/share/AbyssalSkillsD/data'
    directory.mkdir(parents=True, exist_ok=True)
    bundled = get_app_root() / 'app/data'
    if (bundled / 'version.json').is_file():
        atomic_write(directory / 'version.json', (bundled / 'version.json').read_text(encoding='utf-8'))
    for name in ('skills_registry.json', 'supabase_config.json', 'auth_session.json'):
        source, destination = bundled / name, directory / name
        if source.is_file() and not destination.exists():
            # Credentials from an older installation are validated and moved by AuthEngine.
            if name == 'supabase_config.json':
                config = json.loads(source.read_text(encoding='utf-8'))
                config = {key: config.get(key, '') for key in ('supabase_url', 'anon_key', 'project_name')}
                atomic_write(destination, json.dumps(config, ensure_ascii=False))
            else:
                atomic_write(destination, source.read_text(encoding='utf-8'))
    return directory


def get_frontend_html() -> Path:
    """Returns the absolute path to the main frontend index.html."""
    return get_app_root() / "app" / "frontend" / "index.html"

def get_app_icon() -> Path:
    """Returns the path to the official Abyssal Sky Windows .ico file."""
    return get_app_root() / "app" / "frontend" / "assets" / "logo" / "app-icon.ico"

def get_log_dir() -> Path:
    """
    Returns the persistent directory for application logs and diagnostics.
    - Windows: %LOCALAPPDATA%/AbyssalSkillsD/logs
    - macOS: ~/Library/Logs/AbyssalSkillsD
    - Linux: ~/.local/state/AbyssalSkillsD/logs (or XDG_STATE_HOME)
    """
    if sys.platform == "win32":
        local_app_data = os.environ.get("LOCALAPPDATA")
        if local_app_data:
            log_dir = Path(local_app_data) / "AbyssalSkillsD" / "logs"
        else:
            log_dir = get_data_dir() / "logs"
    elif sys.platform == "darwin":
        log_dir = Path.home() / "Library" / "Logs" / "AbyssalSkillsD"
    else:
        xdg_state = os.environ.get("XDG_STATE_HOME")
        if xdg_state:
            log_dir = Path(xdg_state) / "AbyssalSkillsD" / "logs"
        else:
            log_dir = Path.home() / ".local" / "state" / "AbyssalSkillsD" / "logs"
    
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except Exception:
        log_dir = get_data_dir() / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
    return log_dir

def assert_safe_workspace_path(path_input: Any) -> Path:
    """
    Validates and canonicalizes a workspace path to prevent Path Traversal and
    accidental modification of sensitive system directories (OWASP Top 10 / Ring 1 Defense).
    Cross-platform support for Windows, macOS, and Linux.
    """
    if not path_input:
        raise ValueError("Đường dẫn thư mục dự án không được để trống.")
    
    path_str = str(path_input).strip()
    if "\0" in path_str:
        raise ValueError("Phát hiện ký tự độc hại (null byte) trong đường dẫn.")
        
    resolved = Path(path_str).resolve()
    
    # 1. Must exist and be a directory
    if not resolved.exists():
        raise FileNotFoundError(f"Thư mục không tồn tại: {resolved}")
    if not resolved.is_dir():
        raise NotADirectoryError(f"Đường dẫn không phải là một thư mục: {resolved}")
        
    # 2. Block root drives (e.g. C:\ on Windows or / on Unix)
    if resolved.parent == resolved:
        raise PermissionError("Không được phép chọn thư mục gốc ổ đĩa làm dự án.")
        
    # 3. Allow legitimate temporary directories (e.g. testing scratch workspaces or CI runners under /tmp or /var/folders)
    import tempfile
    try:
        temp_root = Path(tempfile.gettempdir()).resolve()
        if resolved == temp_root or temp_root in resolved.parents:
            return resolved
    except Exception:
        pass

    # 4. Block sensitive OS system folders
    if sys.platform == "win32":
        win_dir = os.environ.get("WINDIR") or r"C:\Windows"
        if resolved == Path(win_dir).resolve() or Path(win_dir).resolve() in resolved.parents:
            raise PermissionError("Không được phép chọn thư mục hệ thống Windows.")
    else:
        blocked_unix = ["/etc", "/usr", "/bin", "/sbin", "/sys", "/proc", "/dev", "/boot", "/var"]
        for b in blocked_unix:
            b_path = Path(b).resolve()
            if resolved == b_path or b_path in resolved.parents:
                raise PermissionError(f"Không được phép chọn thư mục hệ thống Unix/Linux: {b}")
        
    return resolved
