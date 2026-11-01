"""
AbyssalSkillsD - Storage & Registry Manager
Maintains app/data/skills_registry.json and seeds both:
1. The complete 7-skill suite from the Skill-AI-private organization (~/.gemini/config/skills).
2. The 25 production engineering skills and 4 specialist personas from Addy Osmani (app/data/repos/agent-skills).
"""
import os
import json
import time
from pathlib import Path
from typing import List, Dict, Optional, Any
from .models import SkillItem, ReferenceDoc, RuleDoc
from .scanner import SkillScanner
from .paths import get_data_dir

class SkillStorage:
    DATA_DIR = get_data_dir()
    REGISTRY_FILE = DATA_DIR / "skills_registry.json"

    @classmethod
    def initialize(cls):
        """Initializes storage directory and seeds skills if missing or incomplete."""
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not cls.REGISTRY_FILE.exists() or cls.REGISTRY_FILE.stat().st_size < 10:
            cls.sync_all_local_skills()
        else:
            # Check if all official skills and addy osmani items are present (7 + 29 = 36)
            skills = cls.get_all_skills()
            personas = [s for s in skills if s.is_persona]
            if len(skills) < 36 or len(personas) < 4:
                # Only attempt sync if local source directories exist on disk to prevent wiping pre-seeded skills
                config_dir = Path.home() / ".gemini" / "config" / "skills"
                addy_dir = Path("app/data/repos/agent-skills")
                if config_dir.exists() or addy_dir.exists():
                    cls.sync_all_local_skills()

    @classmethod
    def sync_all_local_skills(cls) -> List[SkillItem]:
        """Scans ~/.gemini/config/skills and app/data/repos/agent-skills while preserving pre-seeded registry items."""
        skills: List[SkillItem] = []
        if cls.REGISTRY_FILE.exists() and cls.REGISTRY_FILE.stat().st_size > 10:
            try:
                raw = json.loads(cls.REGISTRY_FILE.read_text(encoding="utf-8"))
                skills = [SkillItem.from_dict(item) for item in raw]
            except Exception:
                skills = []

        def merge_or_append(s: SkillItem):
            for i, existing in enumerate(skills):
                if existing.id == s.id:
                    skills[i] = s
                    return
            skills.append(s)

        home = Path.home()
        config_skills_dir = home / ".gemini" / "config" / "skills"

        core_skill_ai_ids = {
            "strict-architect-coder", "ui-ux-design-master", "shadcn-tailwind-artisan",
            "web-assets-creative-vault", "nextjs-fullstack-master", "supabase-backend-architect",
            "playwright-web-tester"
        }

        # 1. Official Skill-AI Suite (strictly the 7 core skills)
        if config_skills_dir.exists() and config_skills_dir.is_dir():
            for folder in sorted(config_skills_dir.iterdir()):
                if folder.is_dir() and folder.name in core_skill_ai_ids:
                    scanned = SkillScanner.scan_skill_directory(folder)
                    for s in scanned:
                        merge_or_append(s)

        # 2. Addy Osmani Production Skills & Personas Suite (25 skills + 4 personas)
        addy_dir = Path("app/data/repos/agent-skills")
        if addy_dir.exists() and addy_dir.is_dir():
            addy_skills = SkillScanner.scan_skill_directory(addy_dir, repo_url="https://github.com/addyosmani/agent-skills")
            for s in addy_skills:
                merge_or_append(s)

        if skills:
            cls.save_all_skills(skills)
        return skills

    @classmethod
    def get_all_skills(cls, workspace_path: Optional[str] = None) -> List[SkillItem]:
        try:
            if not cls.REGISTRY_FILE.exists():
                return cls.sync_all_local_skills()
            raw = json.loads(cls.REGISTRY_FILE.read_text(encoding="utf-8"))
            skills = [SkillItem.from_dict(item) for item in raw]
            # Refresh installation markers with single-pass batch map (Zero I/O Thrashing)
            from app.backend.installer import SkillInstaller
            targets_map, paths_map = SkillScanner.get_installed_targets_and_paths(workspace_path)
            always_on = SkillScanner.detect_always_on_enabled()
            for s in skills:
                s.installed_targets = targets_map.get(s.id, [])
                s.always_on_enabled = always_on
                disk_path = paths_map.get(s.id)
                if disk_path and disk_path.exists():
                    s.installed_path = str(disk_path)
                    try:
                        disk_content = disk_path.read_text(encoding="utf-8", errors="replace").strip()
                        canonical_repo = SkillInstaller.generate_skill_markdown(s).strip()
                        s.has_update = (disk_content != canonical_repo)
                    except Exception:
                        s.has_update = False
                else:
                    s.installed_path = None
                    s.has_update = False
            return skills
        except Exception:
            try:
                if cls.REGISTRY_FILE.exists():
                    raw = json.loads(cls.REGISTRY_FILE.read_text(encoding="utf-8"))
                    return [SkillItem.from_dict(item) for item in raw]
            except Exception:
                pass
            return cls.sync_all_local_skills()

    @classmethod
    def get_skill(cls, skill_id: str, workspace_path: Optional[str] = None) -> Optional[SkillItem]:
        skills = cls.get_all_skills(workspace_path)
        for s in skills:
            if s.id == skill_id:
                return s
        return None

    @classmethod
    def save_all_skills(cls, skills: List[SkillItem]):
        cls.DATA_DIR.mkdir(parents=True, exist_ok=True)
        data = [s.to_dict() for s in skills]
        payload = json.dumps(data, indent=2, ensure_ascii=False)
        temp_file = cls.DATA_DIR / f"skills_registry_{os.getpid()}_{time.time_ns()}.tmp"
        try:
            temp_file.write_text(payload, encoding="utf-8")
            temp_file.replace(cls.REGISTRY_FILE)
        except Exception:
            for attempt in range(3):
                try:
                    cls.REGISTRY_FILE.write_text(payload, encoding="utf-8")
                    break
                except Exception:
                    time.sleep(0.05)
        finally:
            if temp_file.exists():
                try:
                    temp_file.unlink()
                except Exception:
                    pass

    @classmethod
    def upsert_skill(cls, skill: SkillItem) -> SkillItem:
        skills = cls.get_all_skills()
        found = False
        for i, s in enumerate(skills):
            if s.id == skill.id:
                skill.updated_at = time.time()
                skills[i] = skill
                found = True
                break
        if not found:
            skill.created_at = time.time()
            skill.updated_at = time.time()
            skills.append(skill)
        cls.save_all_skills(skills)
        return skill

    @classmethod
    def delete_skill(cls, skill_id: str) -> bool:
        skills = cls.get_all_skills()
        new_list = [s for s in skills if s.id != skill_id]
        if len(new_list) != len(skills):
            cls.save_all_skills(new_list)
            return True
        return False
