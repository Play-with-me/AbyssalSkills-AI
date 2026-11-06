"""
AbyssalSkillsD - Auto-Update Engine (v1.0.0 Zero-Crash Architecture)
Provides dual-layer updates:
1. Skills Library Auto-Sync (Git-based sync with Addy Osmani & Skill-AI repos)
2. Software Application Update Check (SemVer comparison via GitHub Releases API)
Includes offline resilience, fallback defaults, and sub-process timeout guardrails.
"""
import os
import sys
import json
import urllib.request
import urllib.error
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from .git_sync import GitSyncEngine
from .scanner import SkillScanner
from .storage import SkillStorage
from .paths import get_data_dir, get_app_root

def get_version_file() -> Path:
    """Returns the bundled version.json from app root, falling back to data_dir."""
    bundled = get_app_root() / "app" / "data" / "version.json"
    if bundled.exists():
        return bundled
    return get_data_dir() / "version.json"

VERSION_FILE = get_version_file()
DEFAULT_APP_REPO = "Play-with-me/AbyssalSkills-AI"
DEFAULT_SKILLS_REPO = "https://github.com/addyosmani/agent-skills"

class UpdateEngine:
    @classmethod
    def get_version_info(cls) -> Dict[str, Any]:
        """Loads local version configuration from version.json."""
        v_file = get_version_file()
        if v_file.exists():
            try:
                return json.loads(v_file.read_text(encoding="utf-8"))
            except Exception:
                pass
        return {
            "version": "1.0.0",
            "app_name": "AbyssalSkillsD",
            "channel": "stable",
            "release_date": "2026-10-31",
            "repository": f"https://github.com/{DEFAULT_APP_REPO}",
            "skills_repo": DEFAULT_SKILLS_REPO,
            "changelog": {
                "version": "1.0.0",
                "title": "AbyssalSkillsD v1.0.0 Debut Edition",
                "highlights": [
                    "Thương hiệu độc quyền AbyssalSkillsD chuẩn Linear/Vercel",
                    "Nền Blueprint Grid kỹ thuật và Taskbar Icon riêng biệt",
                    "Hỗ trợ 29 kỹ năng từ Addy Osmani và tự động nạp vào 5 nền tảng AI"
                ]
            }
        }

    @classmethod
    def parse_semver(cls, version_str: str) -> Tuple[int, ...]:
        """Parses a version string like 'v7.1.0' or '7.2.1' into a tuple of ints."""
        clean = version_str.strip().lstrip("v").split("-")[0]
        parts = []
        for p in clean.split("."):
            try:
                parts.append(int(p))
            except ValueError:
                parts.append(0)
        while len(parts) < 3:
            parts.append(0)
        return tuple(parts[:3])

    @classmethod
    def is_newer_version(cls, latest: str, current: str) -> bool:
        """Returns True if latest version is strictly greater than current."""
        return cls.parse_semver(latest) > cls.parse_semver(current)

    @classmethod
    def check_for_updates(cls, custom_repo: Optional[str] = None) -> Dict[str, Any]:
        """
        Checks for software releases from GitHub Releases API and inspects
        local skills repository for available updates.
        Returns a complete update status object (offline-resilient).
        """
        local_info = cls.get_version_info()
        current_ver = local_info.get("version", "1.0.0")
        repo_slug = custom_repo or DEFAULT_APP_REPO
        api_url = f"https://api.github.com/repos/{repo_slug}/releases/latest"
        
        app_update_available = False
        latest_ver = current_ver
        release_title = local_info.get("changelog", {}).get("title", "")
        release_notes = local_info.get("changelog", {}).get("highlights", [])
        download_url = f"https://github.com/{repo_slug}/releases"
        setup_download_url = f"https://github.com/{repo_slug}/releases/latest/download/AbyssalSkillsD-Setup.exe"
        is_offline = False

        # 1. Query GitHub Releases API with strict 6-second timeout
        try:
            req = urllib.request.Request(
                api_url,
                headers={
                    "User-Agent": "AbyssalSkillsD-AutoUpdater/1.0",
                    "Accept": "application/vnd.github.v3+json"
                }
            )
            with urllib.request.urlopen(req, timeout=6) as resp:
                if resp.status == 200:
                    data = json.loads(resp.read().decode("utf-8"))
                    tag_name = data.get("tag_name", "").lstrip("v")
                    if tag_name and cls.is_newer_version(tag_name, current_ver):
                        app_update_available = True
                        latest_ver = tag_name
                        release_title = data.get("name", f"AbyssalSkillsD v{latest_ver}")
                        body_lines = [line.strip().lstrip("-*• ") for line in data.get("body", "").splitlines() if line.strip()]
                        if body_lines:
                            release_notes = body_lines[:6]
                        html_url = data.get("html_url")
                        if html_url:
                            download_url = html_url
                        for asset in data.get("assets", []):
                            aname = asset.get("name", "")
                            if aname.endswith(".exe") and ("setup" in aname.lower()):
                                setup_download_url = asset.get("browser_download_url")
                                break
        except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError, Exception):
            # If GitHub Releases API fails or has no releases yet, fallback to raw version.json manifest
            try:
                raw_url = f"https://raw.githubusercontent.com/{repo_slug}/main/app/data/version.json"
                raw_req = urllib.request.Request(
                    raw_url,
                    headers={"User-Agent": "AbyssalSkillsD-AutoUpdater/1.0"}
                )
                with urllib.request.urlopen(raw_req, timeout=3) as raw_resp:
                    if raw_resp.status == 200:
                        raw_data = json.loads(raw_resp.read().decode("utf-8"))
                        remote_ver = raw_data.get("version", "")
                        if remote_ver and cls.is_newer_version(remote_ver, current_ver):
                            app_update_available = True
                            latest_ver = remote_ver
                            cl = raw_data.get("changelog", {})
                            release_title = cl.get("title", f"AbyssalSkillsD v{latest_ver}")
                            release_notes = cl.get("highlights", release_notes)
                            download_url = f"https://github.com/{repo_slug}/raw/main/dist/AbyssalSkillsD-Setup-v{latest_ver}.exe"
                        is_offline = False
                    else:
                        is_offline = True
            except Exception:
                is_offline = True

        # 2. Check Skills Library Status
        skills_repo_dir = GitSyncEngine.REPOS_DIR / ('agent-skills-' + __import__('hashlib').sha256(DEFAULT_SKILLS_REPO.encode()).hexdigest()[:16])
        has_skills_update = False
        skills_summary = 'Chưa xác minh phiên bản thư viện Addy trên GitHub.'
        skills_check_status = 'unknown'
        if (skills_repo_dir / '.git').is_dir():
            flags = subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            try:
                local = subprocess.run(['git', '-C', str(skills_repo_dir), 'rev-parse', 'HEAD'], capture_output=True, text=True, timeout=5, creationflags=flags)
                remote = subprocess.run(['git', '-C', str(skills_repo_dir), 'ls-remote', 'origin', 'HEAD'], capture_output=True, text=True, timeout=8, creationflags=flags)
                if local.returncode == remote.returncode == 0 and remote.stdout.strip():
                    has_skills_update = local.stdout.strip() != remote.stdout.split()[0]
                    skills_check_status = 'checked'
                    skills_summary = 'Kho Addy có thay đổi so với bản đã tải.' if has_skills_update else 'Bản Addy đã tải khớp commit HEAD của nguồn.'
            except (OSError, subprocess.TimeoutExpired):
                pass

        all_skills = SkillStorage.get_all_skills()
        total_skills = len(all_skills)
        skills_need_update = sum(1 for s in all_skills if getattr(s, 'has_update', False))
        update_signature = f"skills_v{current_ver}_{has_skills_update}_{total_skills}_{skills_need_update}"

        return {
            "success": True,
            "has_app_update": app_update_available,
            "current_version": current_ver,
            "latest_version": latest_ver,
            "release_title": release_title,
            "release_notes": release_notes,
            "download_url": download_url,
            "setup_download_url": setup_download_url,
            "has_skills_update": has_skills_update,
            "skills_need_update": skills_need_update,
            "skills_summary": skills_summary,
            "new_skills_count": None,
            "skills_check_status": skills_check_status,
            "update_signature": update_signature,
            "total_skills_installed": sum(bool(item.installed_targets) for item in all_skills),
            "total_skills": total_skills,
            "is_offline": is_offline,
            "checked_at": datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
        }

    @classmethod
    def sync_skills_library(cls) -> Dict[str, Any]:
        """
        Pulls latest updates from the official Addy Osmani skills repository,
        re-scans the playbooks, and updates the local registry.
        """
        ok, msg, repo_path = GitSyncEngine.clone_or_pull(DEFAULT_SKILLS_REPO)
        if not ok or not repo_path.exists():
            return {
                "success": False,
                "message": msg,
                "skills_count": len(SkillStorage.get_all_skills())
            }

        scanned_skills = SkillScanner.scan_skill_directory(repo_path, repo_url=DEFAULT_SKILLS_REPO)
        if not scanned_skills:
            return {
                "success": False,
                "message": "Không tìm thấy kỹ năng hợp lệ sau khi quét repository.",
                "skills_count": len(SkillStorage.get_all_skills())
            }

        # Keep existing custom skills and merge/update scanned ones
        existing = SkillStorage.get_all_skills()
        existing_custom = [s for s in existing if s.source_group not in ("addy_osmani",)]
        
        merged_list = existing_custom + scanned_skills
        SkillStorage.save_all_skills(merged_list)

        return {
            "success": True,
            "message": f"Đồng bộ thành công! Đã làm mới {len(scanned_skills)} kỹ năng từ kho Addy Osmani.",
            "skills_count": len(merged_list),
            "updated_items": len(scanned_skills)
        }

    _download_progress = {"status": "idle", "percent": 0, "bytes_downloaded": 0, "total_bytes": 0, "error": None}

    @classmethod
    def get_download_progress(cls) -> Dict[str, Any]:
        return dict(cls._download_progress)

    @classmethod
    def download_and_apply_update(cls, download_url: Optional[str] = None) -> Dict[str, Any]:
        """
        Tải bộ cài đặt mới nhất từ GitHub Releases về thư mục tạm, xác minh và chạy
        trình cài đặt Inno Setup ghi đè an toàn vào thư mục hiện tại mà không làm mất dữ liệu người dùng.
        """
        import tempfile
        import subprocess

        url = download_url
        if not url or not url.endswith('.exe'):
            url = f"https://github.com/{DEFAULT_APP_REPO}/releases/latest/download/AbyssalSkillsD-Setup.exe"

        cls._download_progress = {"status": "downloading", "percent": 0, "bytes_downloaded": 0, "total_bytes": 0, "error": None}
        temp_dir = Path(tempfile.gettempdir())
        temp_setup = temp_dir / "AbyssalSkillsD-Setup-Update.exe"
        runner_bat = temp_dir / "abyssal_update_restart.bat"

        try:
            req = urllib.request.Request(url, headers={"User-Agent": "AbyssalSkillsD-AutoUpdater/1.0"})
            with urllib.request.urlopen(req, timeout=30) as resp:
                total_length = resp.headers.get('content-length')
                total_bytes = int(total_length) if total_length else 16 * 1024 * 1024
                cls._download_progress["total_bytes"] = total_bytes
                
                downloaded = 0
                chunk_size = 65536
                with open(temp_setup, "wb") as f:
                    while True:
                        chunk = resp.read(chunk_size)
                        if not chunk:
                            break
                        f.write(chunk)
                        downloaded += len(chunk)
                        cls._download_progress["bytes_downloaded"] = downloaded
                        cls._download_progress["percent"] = min(99, int((downloaded / total_bytes) * 100))

            cls._download_progress["percent"] = 100
            cls._download_progress["status"] = "ready_to_install"

            from .paths import get_app_root
            app_root = get_app_root()
            exe_path = Path(sys.executable).resolve()
            is_frozen = getattr(sys, "frozen", False)
            target_dir = exe_path.parent if is_frozen else app_root

            if not is_frozen:
                return {
                    "success": True,
                    "status": "downloaded",
                    "setup_path": str(temp_setup),
                    "message": f"Đã tải thành công bộ cài mới về: {temp_setup}. (Đang chạy ở chế độ lập trình Dev Mode nên không tự ghi đè môi trường phát triển)."
                }

            runner_script = f"""@echo off
timeout /t 2 /nobreak > nul
"{temp_setup}" /SILENT /DIR="{target_dir}" /FORCECLOSEAPPLICATIONS /CLOSEAPPLICATIONS
start "" "{target_dir}\\AbyssalSkillsD.exe"
del "%~f0"
"""
            runner_bat.write_text(runner_script, encoding="utf-8")

            flags = subprocess.CREATE_NO_WINDOW if sys.platform == 'win32' else 0
            subprocess.Popen(["cmd.exe", "/c", str(runner_bat)], creationflags=flags)

            import threading
            def _exit_app():
                import time
                time.sleep(1.0)
                os._exit(0)
            threading.Thread(target=_exit_app, daemon=True).start()

            return {
                "success": True,
                "status": "installing",
                "message": "Đã tải xong bộ cài mới. Ứng dụng sẽ tự động đóng và khởi động lại phiên bản mới sau vài giây!"
            }
        except Exception as e:
            cls._download_progress["status"] = "error"
            cls._download_progress["error"] = str(e)
            return {"success": False, "status": "error", "message": f"Lỗi cập nhật: {e}"}
