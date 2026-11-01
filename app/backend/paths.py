"""
AbyssalSkillsD - Runtime Path Resolver
Ensures seamless discovery of frontend assets, user data directories,
and icon files across development mode and packaged frozen PyInstaller executable mode.
"""
import sys
import os
from pathlib import Path
from typing import Any, Optional, Union, Dict, List, Tuple

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
    """
    Returns the persistent data directory for skills, configs, and sessions.
    Creates the directory if it does not exist.
    In frozen mode, gracefully falls back to %APPDATA%/AbyssalSkillsD/data
    if installed in a read-only directory like C:\\Program Files.
    """
    root = get_app_root()
    data_dir = root / "app" / "data"

    if getattr(sys, "frozen", False):
        try:
            data_dir.mkdir(parents=True, exist_ok=True)
            test_file = data_dir / ".write_test"
            test_file.touch()
            test_file.unlink()
            return data_dir
        except (PermissionError, OSError):
            if sys.platform == "win32":
                app_data = os.environ.get("APPDATA")
                if app_data:
                    user_data_dir = Path(app_data) / "AbyssalSkillsD" / "data"
                else:
                    user_data_dir = Path.home() / ".abyssalskillsd" / "data"
            elif sys.platform == "darwin":
                user_data_dir = Path.home() / "Library" / "Application Support" / "AbyssalSkillsD" / "data"
            else:
                xdg_data = os.environ.get("XDG_DATA_HOME") or (Path.home() / ".local" / "share")
                user_data_dir = Path(xdg_data) / "AbyssalSkillsD" / "data"

            user_data_dir.mkdir(parents=True, exist_ok=True)
            for item in data_dir.glob("*.json"):
                dest = user_data_dir / item.name
                if not dest.exists():
                    try:
                        import shutil
                        shutil.copy2(item, dest)
                    except Exception:
                        pass
            return user_data_dir

    data_dir.mkdir(parents=True, exist_ok=True)
    return data_dir

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
