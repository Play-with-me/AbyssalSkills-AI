"""
AbyssalSkillsD - Multi-Target Installer Engine
Implements automated skill deployment across:
- Google Antigravity (~/.gemini/config/skills)
- Claude Code (~/.claude/skills)
- GitHub Copilot (~/.copilot/skills)
- Current Workspace (.agents/skills)
- Always-On Autopilot rules installation
- Graphify AST CLI installation & graph updates
"""
import os
import sys
import shutil
import subprocess
import json
import hashlib
import yaml
from .paths import safe_child, validate_skill_id, atomic_write, assert_safe_workspace_path
from pathlib import Path
from typing import List, Optional, Dict, Any
from .models import SkillItem, InstallRequest, InstallResult

class SkillInstaller:
    TARGETS = {
        'antigravity': ('home', '.gemini/config/skills'),
        'claude': ('home', '.claude/skills'),
        'copilot': ('home', '.copilot/skills'),
        'cursor': ('workspace', '.cursor/skills'),
        'windsurf': ('workspace', '.codeium/windsurf/skills'),
        'aider': ('workspace', '.aider/skills'),
        'codex': ('home', '.codex/skills'),
        'workspace': ('workspace', '.agents/skills'),
    }

    @classmethod
    def target_dirs(cls, skill_id, workspace_path=None):
        validate_skill_id(skill_id)
        workspace = assert_safe_workspace_path(workspace_path or Path.cwd())
        return {name: safe_child(Path.home() if scope == 'home' else workspace, relative + '/' + skill_id)
                for name, (scope, relative) in cls.TARGETS.items()}

    @classmethod
    def installed_skill_dirs(cls, skill_id, workspace_path=None):
        return [p for p in cls.target_dirs(skill_id, workspace_path).values() if (p / 'SKILL.md').is_file()]

    @classmethod
    def skill_payload(cls, skill):
        validate_skill_id(skill.id)
        payload = {'SKILL.md': cls.generate_skill_markdown(skill)}
        for folder, documents in [('references', skill.references), ('rules', skill.rules)]:
            for doc in documents:
                # Validation happens before any file is written.
                safe_child(Path.cwd(), doc.filename)
                payload[folder + '/' + doc.filename] = doc.content
        return payload

    @classmethod
    def skill_differs_at(cls, skill, directory):
        for name, expected in cls.skill_payload(skill).items():
            path = safe_child(directory, name)
            if not path.exists() or path.read_text(encoding='utf-8') != expected:
                return True
        return False

    @classmethod
    def install(cls, skill: SkillItem, req: InstallRequest) -> InstallResult:
        installed, rules, errors, results = [], [], [], []
        try:
            destinations = cls.target_dirs(skill.id, req.workspace_path)
            cls.skill_payload(skill)
        except (ValueError, OSError) as error:
            return InstallResult(False, skill.id, message=str(error), errors=[str(error)])
        workspace = Path(req.workspace_path or Path.cwd())
        for target in dict.fromkeys(req.targets):
            try:
                if target not in destinations:
                    raise ValueError('Môi trường AI không được hỗ trợ: ' + str(target))
                destination = destinations[target]
                if (destination / 'SKILL.md').exists() and cls.skill_differs_at(skill, destination) and not req.overwrite:
                    raise ValueError('Nội dung đã tồn tại khác với thư viện. Vui lòng xem khác biệt và xác nhận cập nhật.')
                payload = {safe_child(destination, name): content for name, content in cls.skill_payload(skill).items()}
                rule_paths = []
                if req.enable_always_on:
                    shared = cls.shared_rule_payload(skill, target, workspace)
                    payload.update(shared)
                    rule_paths = [str(path) for path in shared]
                if not req.overwrite:
                    for path, content in payload.items():
                        if path.exists() and path.read_text(encoding='utf-8') != content and path.is_relative_to(destination):
                            raise ValueError('Nội dung đã thay đổi. Vui lòng xem khác biệt trước khi cập nhật.')
                        if path.exists() and not path.is_relative_to(destination):
                            current = path.read_text(encoding='utf-8')
                            old = cls.rule_block(current, skill.id)
                            new = cls.rule_block(content, skill.id)
                            if old and old != new:
                                raise ValueError('Quy tắc đã thay đổi. Vui lòng xem khác biệt trước khi cập nhật.')
                manifest = {str(path): hashlib.sha256(cls.rule_block(content, skill.id).encode()).hexdigest()
                            for path, content in payload.items() if str(path) in rule_paths}
                payload[safe_child(destination, '.abyssal-install.json')] = json.dumps({'rules': manifest}, ensure_ascii=False)
                cls.write_payload(payload)
                installed.append(str(destination))
                rules.extend(rule_paths)
                results.append({'target': target, 'status': 'success', 'path': str(destination)})
            except Exception as error:
                errors.append(f"{target}: {error}")
                results.append({'target': target, 'status': 'error', 'message': str(error)})
        success = bool(installed) and not errors
        status = 'success' if success else ('partial' if installed else 'error')
        return InstallResult(success, skill.id, installed_paths=installed, rules_paths=rules,
                             message=f'Đã ghi tệp ở {len(installed)}/{len(set(req.targets))} môi trường.' + (' Có lỗi cần xử lý.' if errors else ''),
                             errors=errors, status=status, results=results)

    @classmethod
    def uninstall(cls, skill_id, targets, workspace_path=None):
        removed, errors = [], []
        try:
            destinations = cls.target_dirs(skill_id, workspace_path)
            for target in dict.fromkeys(targets):
                if target not in destinations:
                    raise ValueError('Môi trường không được hỗ trợ: ' + str(target))
                destination = destinations[target]
                if destination.exists():
                    manifest_file = destination / '.abyssal-install.json'
                    if manifest_file.is_file():
                        manifest = json.loads(manifest_file.read_text(encoding='utf-8'))
                        allowed = {str(path): path for paths in cls.rule_locations(target, workspace_path or Path.cwd()).values() for path in paths}
                        for name, expected_hash in manifest.get('rules', {}).items():
                            if name not in allowed or not allowed[name].is_file():
                                continue
                            path = safe_child(allowed[name].parent, allowed[name].name)
                            text = path.read_text(encoding='utf-8')
                            block = cls.rule_block(text, skill_id)
                            if block and hashlib.sha256(block.encode()).hexdigest() == expected_hash:
                                atomic_write(path, text.replace(block, '', 1), backup=True)
                    # Preserve the complete installation in a recoverable sibling archive.
                    import time
                    archive = safe_child(destination.parent, ".abyssal-removed/" + skill_id + "-" + str(time.time_ns()))
                    archive.parent.mkdir(parents=True, exist_ok=True)
                    destination.replace(archive)
                    removed.append(str(destination))
        except (ValueError, OSError) as error:
            errors.append(str(error))
        return {'success': not errors, 'status': 'error' if errors else 'success', 'skill_id': skill_id,
                'removed_paths': removed, 'errors': errors,
                'message': f'Đã gỡ thư mục skill tại {len(removed)} vị trí. Giữ lại nội dung tùy biến và các snapshot ngoài thư mục skill.' if not errors else '; '.join(errors)}

    @classmethod
    def generate_skill_markdown(cls, skill: SkillItem) -> str:
        """Generates the canonical full markdown for a skill (YAML frontmatter + body)."""
        metadata = skill.yaml_frontmatter or {'name': skill.name, 'description': skill.description}
        return '---\n' + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False).rstrip() + '\n---\n\n' + skill.skill_content

    @classmethod
    def _write_skill_to_dir(cls, skill: SkillItem, dest_dir: Path) -> Path:
        payload = {safe_child(dest_dir, name): content for name, content in cls.skill_payload(skill).items()}
        cls.write_payload(payload)
        return dest_dir

    @staticmethod
    def rule_block(content, skill_id):
        import re
        pattern = r'<!-- AbyssalSkillsD:' + re.escape(skill_id) + r' -->[\s\S]*?<!-- /AbyssalSkillsD:' + re.escape(skill_id) + r' -->'
        match = re.search(pattern, content)
        return match.group(0) if match else ''

    @staticmethod
    def rule_locations(target, workspace):
        home, ws = Path.home(), Path(workspace)
        locations = {
            'antigravity': {'always': [home / '.gemini/config/rules/always-on-autopilot.md'], 'context': [home / '.gemini/GEMINI.md', home / '.gemini/config/GEMINI.md']},
            'claude': {'context': [home / '.claude/CLAUDE.md']},
            'cursor': {'always': [ws / '.cursorrules', ws / '.cursor/rules/always-on-autopilot.mdc']},
            'windsurf': {'always': [ws / '.windsurfrules']},
            'aider': {'always': [ws / 'CONVENTIONS.md']},
            'codex': {'always': [home / '.codex/rules/always-on-autopilot.md', ws / 'CODEX.md', ws / '.codex/rules/always-on-autopilot.md']},
            'workspace': {'always': [ws / '.agents/rules/always-on-autopilot.md', ws / '.cursorrules', ws / '.cursor/rules/always-on-autopilot.mdc', ws / '.windsurfrules', ws / '.github/copilot-instructions.md', ws / 'CONVENTIONS.md', ws / 'CODEX.md', ws / '.codex/rules/always-on-autopilot.md'], 'context': [ws / 'GEMINI.md', ws / 'AGENTS.md']},
        }
        return locations.get(target, {})

    @classmethod
    def shared_rule_payload(cls, skill, target, workspace):
        payload = {}
        for rule in skill.rules:
            kind = 'always' if 'always-on' in rule.filename else 'context' if ('GEMINI' in rule.filename or 'CLAUDE' in rule.filename) else None
            for path in cls.rule_locations(target, workspace).get(kind, []):
                # Validate linked parents before reading or creating directories.
                safe_child(Path.home() if path.is_relative_to(Path.home()) and not path.is_relative_to(Path(workspace)) else Path(workspace), path.relative_to(Path.home() if path.is_relative_to(Path.home()) and not path.is_relative_to(Path(workspace)) else Path(workspace)).as_posix())
                old = payload.get(path, path.read_text(encoding='utf-8') if path.exists() else '')
                block = f'<!-- AbyssalSkillsD:{skill.id} -->\n{rule.content}\n<!-- /AbyssalSkillsD:{skill.id} -->'
                previous = cls.rule_block(old, skill.id)
                payload[path] = old.replace(previous, block, 1) if previous else old.rstrip() + ('\n\n' if old else '') + block + '\n'
        return payload

    @classmethod
    def target_payload(cls, skill, target, workspace):
        destination = cls.target_dirs(skill.id, workspace)[target]
        return {**{safe_child(destination, name): content for name, content in cls.skill_payload(skill).items()},
                **cls.shared_rule_payload(skill, target, Path(workspace))}

    @staticmethod
    def write_payload(payload):
        """Snapshot all changed files first, then replace; restore on write failure."""
        import time
        changed = {path: text for path, text in payload.items() if not path.exists() or path.read_text(encoding='utf-8') != text}
        original, snapshots = {}, {}
        for path in changed:
            safe_child(path.parent, path.name)
            original[path] = path.read_text(encoding='utf-8') if path.exists() else None
            if path.exists():
                snapshot = path.with_name(f'{path.name}.{time.time_ns()}.bak')
                shutil.copy2(path, snapshot)
                snapshots[path] = snapshot
        written = []
        try:
            for path, text in changed.items():
                atomic_write(path, text)
                written.append(path)
        except OSError:
            for path in reversed(written):
                if original[path] is None:
                    path.unlink(missing_ok=True)
                else:
                    atomic_write(path, original[path])
            raise

    @staticmethod
    def _run_graphify_integration(req: InstallRequest) -> str:
        """Runs Graphify integration commands."""
        target_path = req.workspace_path if req.workspace_path else "."
        try:
            # Run graphify update to generate graph.json and GRAPH_REPORT.md
            cmd = ["uv", "run", "graphify", "update", target_path, "--force"]
            flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=15, creationflags=flags)
            if res.returncode == 0:
                return "active (graph.json & GRAPH_REPORT.md updated)"
            else:
                return f"info: {res.stderr[:80] if res.stderr else 'graphify completed'}"
        except Exception as e:
            return f"skipped ({str(e)})"

    @classmethod
    def sync_all_ais(
        cls, 
        skills: List[SkillItem], 
        targets: Optional[List[str]] = None, 
        workspace_path: Optional[str] = None,
        cancel_event=None,
        enable_always_on=True,
        overwrite: bool = True
    ) -> Dict[str, Any]:
        """
        Đồng bộ toàn bộ kho kỹ năng cho tất cả các công cụ AI được chỉ định.
        Mặc định: antigravity, claude, copilot, cursor, windsurf, codex, workspace.
        """
        if not targets:
            targets = ["antigravity", "claude", "copilot", "cursor", "windsurf", "codex", "workspace"]

        active_ws = assert_safe_workspace_path(workspace_path or Path.cwd())
        counts = {target: 0 for target in targets}
        results, errors, installed = [], [], []
        for skill in skills:
            if cancel_event is not None and cancel_event.is_set():
                break
            result = cls.install(skill, InstallRequest(skill.id, targets, str(active_ws), enable_always_on, False, overwrite=overwrite))
            installed.extend(result.installed_paths)
            errors.extend(result.errors)
            results.append({'skill_id': skill.id, 'status': result.status, 'results': result.results})
            for item in result.results:
                if item['status'] == 'success':
                    counts[item['target']] += 1
        cancelled = cancel_event is not None and cancel_event.is_set()
        success = bool(installed) and not errors and not cancelled
        return {'success': success, 'status': 'cancelled' if cancelled else ('success' if success else ('partial' if installed else 'error')),
                'total_skills': len(skills), 'targets': targets, 'target_counts': counts,
                'total_installed_files': sum(sum(1 for f in Path(p).rglob('*') if f.is_file() and not f.name.endswith('.bak')) for p in installed),
                'workspace_path': str(active_ws), 'results': results, 'errors': errors,
                'message': f'Đã ghi {len(installed)} bản cài. {len(errors)} lỗi; xem chi tiết trước khi thử lại.'}

    @classmethod
    def generate_rule_scaffold(
        cls, 
        workspace_path: Optional[str] = None, 
        rule_types: Optional[List[str]] = None,
        skills: Optional[List[SkillItem]] = None
    ) -> Dict[str, Any]:
        """
        Tự động sinh giàn giáo tệp quy tắc cho dự án (Cursor, Windsurf, Claude, Copilot, Antigravity, Codex).
        """
        active_ws = assert_safe_workspace_path(workspace_path or Path.cwd())

        if not rule_types:
            rule_types = ["cursorrules", "windsurfrules", "claude", "copilot", "agent_rules", "codex"]

        created_files = []
        errors = []

        skill_names = [s.display_title or s.name for s in skills] if skills else [
            "Strict Architect Coder", "UI/UX Design Master", "shadcn/ui Artisan",
            "Next.js Fullstack Master", "Supabase Backend Architect", "Playwright Web Tester"
        ]
        skills_bullet = "\n".join([f"- **{name}**" for name in skill_names[:10]])

        rule_content = f"""# Always-On Engineering, Graphify & UI/UX Autopilot Rules

## 1. Automatic Skill & State Machine Activation
- Every coding, planning, architecture, or debugging request follows the `strict-architect-coder` protocol:
  - Start reply with current operating mode: `[MODE: DISCOVERY]`, `[MODE: BLUEPRINT]`, `[MODE: EXECUTE]`, or `[MODE: VERIFY]`.
- Every frontend, screen layout, button, or UI/UX turn follows the `ui-ux-design-master` protocol:
  - Enforce UX Psychology (zero blind actions, step badges, specific buttons), Vercel Web Interface Guidelines, Anti-Overflow CSS (`min-h-0`, `min-w-0`), 118 Anti-Slop rules, and sub-250ms physics motion.

## 2. Anti-Amnesia: 3 Persistent Project Memory Anchors
- `.agents/PROJECT_MEMORY.md`: Always check first to recall agreed product/UX rules, completed modules, and boundaries.
- `graphify-out/GRAPH_REPORT.md` & `graph.json`: Check before broad grep searches to locate subsystems and God Nodes.
- `DESIGN.md`: Check before styling UI components to keep tokens, colors, and typography 100% consistent.

## 3. Active Skills In Project
{skills_bullet}
"""

        locations = {
            'cursorrules': ['.cursorrules'], 'windsurfrules': ['.windsurfrules'],
            'claude': ['CLAUDE.md'], 'copilot': ['.github/copilot-instructions.md'],
            'agent_rules': ['.agents/rules/always-on-autopilot.md'],
            'codex': ['CODEX.md', '.codex/rules/always-on-autopilot.md'],
        }
        try:
            payload = {}
            for kind in rule_types:
                if kind not in locations:
                    raise ValueError('Loại quy tắc không được hỗ trợ: ' + str(kind))
                for relative in locations[kind]:
                    path = safe_child(active_ws, relative)
                    existing = path.read_text(encoding='utf-8') if path.exists() else ''
                    block = '<!-- AbyssalSkillsD:project-scaffold -->\n' + rule_content + '\n<!-- /AbyssalSkillsD:project-scaffold -->'
                    previous = cls.rule_block(existing, 'project-scaffold')
                    if previous and previous != block:
                        raise ValueError('Quy tắc đã có thay đổi. Hãy xem và sao lưu trước khi thay thế: ' + str(path))
                    payload[path] = existing if previous else existing + ('\n\n' if existing else '') + block + '\n'
            cls.write_payload(payload)
            created_files = [str(path) for path in payload]
        except (OSError, ValueError) as error:
            errors.append(str(error))

        return {
            "success": len(created_files) > 0 and len(errors) == 0,
            "status": "error" if errors else "success",
            "created_files": created_files,
            "workspace_path": str(active_ws),
            "errors": errors,
            "message": f"Đã khởi tạo thành công {len(created_files)} tệp quy tắc cho dự án!" if len(created_files) > 0 else f"Lỗi tạo quy tắc: {'; '.join(errors)}"
        }
