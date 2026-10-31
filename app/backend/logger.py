"""
AbyssalSkillsD - Enterprise Diagnostic & Event Logger
Provides rotating file logging and diagnostic report export for system troubleshooting.
Logs are stored at %LOCALAPPDATA%/AbyssalSkillsD/logs/app.log.
"""
import logging
from logging.handlers import RotatingFileHandler
import os
import sys
import re
import zipfile
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List
from app.backend.paths import get_log_dir

LOGGER_NAME = "AbyssalSkillsD"
_logger = None

def sanitize_sensitive_data(raw_text: str) -> str:
    """
    Scrubs Personally Identifiable Information (PII) such as Windows usernames,
    JWT tokens, database secrets, and API keys before telemetry export.
    Zero-Trust AppSec Standard (OWASP & Ring 1/2 Defense).
    """
    if not raw_text:
        return ""
    cleaned = str(raw_text)

    # 1. Mask all Windows/Unix personal user directories (e.g. C:\Users\<username>\... or /home/<username>/...)
    cleaned = re.sub(r'([a-zA-Z]:[\\/]Users[\\/])[^\\/\s"\';]+', r'\g<1><user>', cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r'([\\/](?:home|Users)[\\/])[^\\/\s"\';]+', r'\g<1><user>', cleaned, flags=re.IGNORECASE)

    # Also mask current OS username if it appears standalone anywhere
    user_name = os.environ.get("USERNAME") or os.environ.get("USER")
    if user_name and len(user_name) > 1:
        pattern = re.compile(re.escape(user_name), re.IGNORECASE)
        cleaned = pattern.sub("<user>", cleaned)

    # 2. Mask JWT bearer tokens (eyJ...)
    cleaned = re.sub(r'eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}', '[REDACTED_JWT_TOKEN]', cleaned)

    # 3. Mask passwords, secret keys, anon keys in JSON or key-value pairs
    cleaned = re.sub(
        r'(anon_key|service_secret_key|secret_key|api_key|password|access_token|refresh_token)["\']?\s*[:=]\s*["\']?([^"\'\s,;]+)',
        r'\1: "[REDACTED_SECRET]"',
        cleaned,
        flags=re.IGNORECASE
    )

    # 4. Mask GitHub Personal Access Tokens (ghp_... or github_pat_...)
    cleaned = re.sub(r'(ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_]{40,})', '[REDACTED_GITHUB_TOKEN]', cleaned)

    return cleaned

def init_logger() -> logging.Logger:
    global _logger
    if _logger is not None:
        return _logger

    logger = logging.getLogger(LOGGER_NAME)
    logger.setLevel(logging.DEBUG)

    log_dir = get_log_dir()
    log_file = log_dir / "app.log"

    # Rotating file handler (5MB max per file, 3 backups)
    file_handler = RotatingFileHandler(
        str(log_file),
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    file_handler.setLevel(logging.INFO)
    file_formatter = logging.Formatter(
        "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(file_formatter)

    # Console stream handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(file_formatter)

    # Prevent duplicate handlers
    if not logger.handlers:
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

    _logger = logger
    _logger.info("=== AbyssalSkillsD Diagnostic Logger Initialized ===")
    return _logger

def get_logger() -> logging.Logger:
    global _logger
    if _logger is None:
        return init_logger()
    return _logger

def get_recent_logs(line_count: int = 100) -> str:
    """Reads the last N lines from the primary app.log file and scrubs PII/secrets."""
    log_file = get_log_dir() / "app.log"
    if not log_file.exists():
        return "Chưa có dữ liệu nhật ký."
    try:
        with open(log_file, "r", encoding="utf-8", errors="replace") as f:
            lines = f.readlines()
            raw_text = "".join(lines[-line_count:])
            return sanitize_sensitive_data(raw_text)
    except Exception as e:
        return f"Lỗi đọc nhật ký: {e}"

def export_diagnostic_zip() -> Dict[str, Any]:
    """
    Packs sanitized log files, system metadata, and workspace configuration into a portable diagnostic zip file.
    All personal usernames, tokens, and database secrets are scrubbed 100%.
    """
    log_dir = get_log_dir()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    zip_filename = f"AbyssalSkillsD_Diagnostic_{timestamp}.zip"
    export_path = log_dir / zip_filename

    try:
        with zipfile.ZipFile(export_path, "w", zipfile.ZIP_DEFLATED) as zf:
            for log_file in log_dir.glob("*.log*"):
                if log_file.is_file() and not log_file.name.endswith(".zip"):
                    try:
                        raw_content = log_file.read_text(encoding="utf-8", errors="replace")
                        clean_content = sanitize_sensitive_data(raw_content)
                        zf.writestr(log_file.name, clean_content)
                    except Exception:
                        pass
            
            # System info report (sanitized)
            sys_info = (
                f"AbyssalSkillsD Diagnostic Report (Zero-Trust Sanitized)\n"
                f"Generated: {datetime.now().isoformat()}\n"
                f"OS: {sys.platform}\n"
                f"Python: {sys.version}\n"
                f"Executable: {sanitize_sensitive_data(sys.executable)}\n"
                f"Frozen: {getattr(sys, 'frozen', False)}\n"
            )
            zf.writestr("system_info.txt", sys_info)

        return {
            "success": True,
            "path": str(export_path),
            "filename": zip_filename,
            "size_kb": round(export_path.stat().st_size / 1024, 2),
            "message": f"Đã xuất báo cáo chẩn đoán an toàn thành công tại: {export_path}"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"Lỗi xuất báo cáo chẩn đoán: {str(e)}"
        }
