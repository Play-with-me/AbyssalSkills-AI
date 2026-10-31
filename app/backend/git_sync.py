"""
AbyssalSkillsD - Git Sync Engine
Handles cloning and updating skills directly from GitHub repositories.
Supports abort/cancellation and sub-process timeout management.
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List, Tuple
from .models import SkillItem
from .scanner import SkillScanner

class GitSyncEngine:
    REPOS_DIR = Path("app/data/repos")

    @classmethod
    def clone_or_pull(cls, repo_url: str) -> Tuple[bool, str, Path]:
        """
        Clones a git repo if not exists, or pulls latest changes.
        Returns: (success: bool, message: str, repo_path: Path)
        """
        cls.REPOS_DIR.mkdir(parents=True, exist_ok=True)
        
        # Determine repo folder name from URL
        clean_url = repo_url.strip().rstrip("/")
        repo_name = clean_url.split("/")[-1]
        if repo_name.endswith(".git"):
            repo_name = repo_name[:-4]

        target_dir = cls.REPOS_DIR / repo_name

        flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        try:
            if target_dir.exists() and (target_dir / ".git").exists():
                # Git pull
                cmd = ["git", "-C", str(target_dir), "pull", "--ff-only"]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=30, creationflags=flags)
                if res.returncode == 0:
                    return True, f"Đã cập nhật mới nhất cho '{repo_name}' từ GitHub.", target_dir
                else:
                    return False, f"Lỗi khi pull repo: {res.stderr.strip()}", target_dir
            else:
                # Git clone
                if target_dir.exists():
                    shutil.rmtree(target_dir, ignore_errors=True)

                cmd = ["git", "clone", "--depth", "1", clean_url, str(target_dir)]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=45, creationflags=flags)
                if res.returncode == 0:
                    return True, f"Đã tải thành công kho kỹ năng '{repo_name}' từ GitHub.", target_dir
                else:
                    return False, f"Lỗi khi clone repo: {res.stderr.strip()}", target_dir

        except subprocess.TimeoutExpired:
            return False, "Quá thời gian chờ tải từ GitHub (Timeout > 45s). Vui lòng thử lại.", target_dir
        except Exception as e:
            return False, f"Lỗi hệ thống khi tải: {str(e)}", target_dir

    @classmethod
    def import_from_github(cls, repo_url: str) -> Tuple[bool, str, List[SkillItem]]:
        """
        Clones or pulls from GitHub, then scans and extracts all skill items.
        """
        ok, msg, repo_path = cls.clone_or_pull(repo_url)
        if not ok or not repo_path.exists():
            return False, msg, []

        skills = SkillScanner.scan_skill_directory(repo_path, repo_url=repo_url)
        if not skills:
            return False, "Không tìm thấy file SKILL.md hợp lệ trong kho GitHub này.", []

        return True, f"Đã nhận diện thành công {len(skills)} kỹ năng từ {repo_path.name}.", skills
