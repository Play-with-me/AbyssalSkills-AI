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
import re
import time
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
        for extra in getattr(skill, 'extra_files', []):
            rel = extra.rel_path.replace('\\', '/').lstrip('/')
            safe_child(Path.cwd(), rel)
            payload[rel] = extra.content
        return payload

    @classmethod
    def normalize_content(cls, text: str) -> str:
        """Normalizes line endings (CRLF to LF) and trims outer whitespace."""
        return text.replace('\r\n', '\n').strip()

    @classmethod
    def files_differ(cls, actual_text: str, expected_text: str, is_skill_md: bool = False) -> bool:
        """
        Determines whether two files differ semantically.
        Handles Windows/Linux line endings and YAML frontmatter line-wrapping variations.
        """
        if actual_text == expected_text:
            return False
        act_norm = cls.normalize_content(actual_text)
        exp_norm = cls.normalize_content(expected_text)
        if act_norm == exp_norm:
            return False
        if is_skill_md and act_norm.startswith('---') and exp_norm.startswith('---'):
            import re
            m_act = re.match(r'^---\n(.*?)\n---\n?(.*)$', act_norm, re.DOTALL)
            m_exp = re.match(r'^---\n(.*?)\n---\n?(.*)$', exp_norm, re.DOTALL)
            if m_act and m_exp:
                try:
                    fm_act = yaml.safe_load(m_act.group(1)) or {}
                    fm_exp = yaml.safe_load(m_exp.group(1)) or {}
                    if fm_act == fm_exp and cls.normalize_content(m_act.group(2)) == cls.normalize_content(m_exp.group(2)):
                        return False
                except Exception:
                    pass
        return True

    @classmethod
    def skill_differs_at(cls, skill, directory):
        for name, expected in cls.skill_payload(skill).items():
            path = safe_child(directory, name)
            if not path.exists():
                return True
            try:
                actual = path.read_text(encoding='utf-8')
                if cls.files_differ(actual, expected, is_skill_md=(name == 'SKILL.md')):
                    return True
            except (OSError, UnicodeDecodeError):
                return True
        return False

    @classmethod
    def clean_nested_skills(cls, root_dir: Path) -> List[str]:
        """
        Phát hiện và dọn dẹp các thư mục kỹ năng bị lồng nhau.
        Ví dụ: root/strict-architect-coder/ui-ux-design-master/SKILL.md
        Lưu trữ thư mục bị lồng vào .abyssal-removed để khôi phục khi cần.
        """
        cleaned = []
        if not root_dir.exists() or not root_dir.is_dir():
            return cleaned
        for skill_dir in list(root_dir.iterdir()):
            if not skill_dir.is_dir() or skill_dir.name.startswith('.'):
                continue
            if not (skill_dir / 'SKILL.md').is_file():
                continue
            for sub in list(skill_dir.iterdir()):
                if not sub.is_dir() or sub.name in {'examples', 'templates', 'scratch', 'references', 'rules', 'scripts', 'assets', 'evals', 'docs', 'hooks', '.abyssal-removed'}:
                    continue
                if (sub / 'SKILL.md').is_file():
                    archive_dir = root_dir / '.abyssal-removed' / f"nested-{skill_dir.name}-{sub.name}-{time.time_ns()}"
                    archive_dir.parent.mkdir(parents=True, exist_ok=True)
                    try:
                        shutil.move(str(sub), str(archive_dir))
                        cleaned.append(f"Lồng nhau: đã chuyển '{sub.name}' trong '{skill_dir.name}' vào {archive_dir.name}")
                    except Exception as e:
                        cleaned.append(f"Lỗi dọn thư mục lồng '{sub.name}': {e}")
        return cleaned

    @classmethod
    def deduplicate_target_dir(cls, target_root: Path) -> List[str]:
        """
        Dọn trùng lặp trong một thư mục đích:
        1. Dọn thư mục kỹ năng bị lồng.
        2. Hợp nhất các thư mục UUID hoặc trùng tên YAML frontmatter name vào slug chuẩn,
           chuyển thư mục trùng vào .abyssal-removed.
        """
        cleaned = cls.clean_nested_skills(target_root)
        if not target_root.exists() or not target_root.is_dir():
            return cleaned

        folder_info = []
        for folder in list(target_root.iterdir()):
            if not folder.is_dir() or folder.name.startswith('.'):
                continue
            skill_md = folder / 'SKILL.md'
            if not skill_md.is_file():
                continue

            skill_name = folder.name
            cloud_id = None
            try:
                content = skill_md.read_text(encoding='utf-8')
                if content.startswith('---'):
                    parts = content.split('---', 2)
                    if len(parts) >= 3:
                        meta = yaml.safe_load(parts[1])
                        if isinstance(meta, dict) and meta.get('name'):
                            skill_name = str(meta['name']).strip()
            except Exception:
                pass

            install_meta = folder / '.abyssal-install.json'
            if install_meta.is_file():
                try:
                    meta_json = json.loads(install_meta.read_text(encoding='utf-8'))
                    cloud_id = meta_json.get('cloud_id')
                except Exception:
                    pass

            is_uuid = bool(re.match(r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$', folder.name))
            norm_name = re.sub(r'[^a-zA-Z0-9_-]', '-', skill_name.lower()).strip('-')

            folder_info.append({
                'folder': folder,
                'name': skill_name,
                'norm_name': norm_name,
                'is_uuid': is_uuid,
                'cloud_id': cloud_id
            })

        grouped = {}
        for item in folder_info:
            grouped.setdefault(item['norm_name'], []).append(item)

        for norm_name, items in grouped.items():
            if len(items) > 1:
                items.sort(key=lambda x: (x['is_uuid'], x['folder'].name != norm_name))
                for duplicate in items[1:]:
                    archive = target_root / '.abyssal-removed' / f"dup-{duplicate['folder'].name}-{time.time_ns()}"
                    archive.parent.mkdir(parents=True, exist_ok=True)
                    try:
                        shutil.move(str(duplicate['folder']), str(archive))
                        cleaned.append(f"Trùng lặp: đã lưu trữ thư mục '{duplicate['folder'].name}' (kỹ năng '{norm_name}')")
                    except Exception as e:
                        cleaned.append(f"Lỗi lưu trữ '{duplicate['folder'].name}': {e}")
            elif len(items) == 1 and items[0]['is_uuid'] and items[0]['norm_name']:
                candidate = target_root / items[0]['norm_name']
                if not candidate.exists():
                    try:
                        items[0]['folder'].rename(candidate)
                        cleaned.append(f"Chuẩn hóa tên: '{items[0]['folder'].name}' -> '{items[0]['norm_name']}'")
                    except Exception:
                        pass
        return cleaned

    @classmethod
    def deduplicate_all_targets(cls, workspace_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Quét và dọn sạch trùng lặp toàn diện trên toàn bộ các môi trường AI và thư mục người dùng:
        - Dọn các thư mục lồng nhau, thư mục UUID và thư mục trùng tên.
        - Xử lý xung đột giữa ~/.agents/skills và thư mục công cụ cá nhân (~/.gemini, ~/.codex, ~/.claude).
        """
        home = Path.home()
        ws = assert_safe_workspace_path(workspace_path or Path.cwd())
        all_roots = [
            home / '.gemini' / 'config' / 'skills',
            home / '.claude' / 'skills',
            home / '.copilot' / 'skills',
            home / '.codex' / 'skills',
            ws / '.cursor' / 'skills',
            ws / '.codeium' / 'windsurf' / 'skills',
            ws / '.aider' / 'skills',
            ws / '.agents' / 'skills',
        ]
        home_agents = home / '.agents' / 'skills'

        cleaned_actions = []
        for root in dict.fromkeys(all_roots):
            if root.exists() and root.is_dir():
                actions = cls.deduplicate_target_dir(root)
                cleaned_actions.extend(actions)

        # Xử lý đụng độ ~/.agents/skills vs thư mục cá nhân của từng công cụ
        if home_agents.exists() and home_agents.is_dir() and ws.resolve() != home.resolve():
            tool_roots = [
                home / '.gemini' / 'config' / 'skills',
                home / '.codex' / 'skills',
                home / '.claude' / 'skills',
            ]
            installed_in_tools = set()
            for tr in tool_roots:
                if tr.exists():
                    for f in tr.iterdir():
                        if f.is_dir() and (f / 'SKILL.md').exists():
                            installed_in_tools.add(f.name.lower())

            for f in list(home_agents.iterdir()):
                if f.is_dir() and (f / 'SKILL.md').exists():
                    if f.name.lower() in installed_in_tools:
                        archive = home / '.agents' / '.abyssal-removed' / f"home-dup-{f.name}-{time.time_ns()}"
                        archive.parent.mkdir(parents=True, exist_ok=True)
                        try:
                            shutil.move(str(f), str(archive))
                            cleaned_actions.append(f"Trùng Personal: chuyển bản sao dư thừa '{f.name}' từ ~/.agents/skills vào kho lưu trữ")
                        except Exception as e:
                            cleaned_actions.append(f"Lỗi chuyển '{f.name}': {e}")

        return {
            'success': True,
            'status': 'success',
            'actions_count': len(cleaned_actions),
            'actions': cleaned_actions,
            'message': f'Đã quét và xử lý {len(cleaned_actions)} mục trùng lặp/chuẩn hóa.' if cleaned_actions else 'Hệ thống sạch, không có kỹ năng trùng lặp.'
        }

    @classmethod
    def install(cls, skill: SkillItem, req: InstallRequest) -> InstallResult:
        installed, rules, errors, results = [], [], [], []
        already_installed_targets = []
        try:
            destinations = cls.target_dirs(skill.id, req.workspace_path)
            cls.skill_payload(skill)
        except (ValueError, OSError) as error:
            return InstallResult(False, skill.id, message=str(error), errors=[str(error)])
        workspace = Path(req.workspace_path or Path.cwd())

        # Tránh ghi vào ~/.agents/skills khi workspace trỏ vào User Home và đã chọn công cụ cá nhân
        skip_home_workspace = (workspace.resolve() == Path.home().resolve()) and any(t in req.targets for t in ['antigravity', 'codex', 'claude'])

        for target in dict.fromkeys(req.targets):
            try:
                if target == 'workspace' and skip_home_workspace:
                    results.append({'target': target, 'status': 'skipped', 'message': 'Bỏ qua ghi ~/.agents/skills vì đã cài vào thư mục công cụ cá nhân (tránh trùng lặp)'})
                    continue
                if target not in destinations:
                    raise ValueError('Môi trường AI không được hỗ trợ: ' + str(target))
                destination = destinations[target]

                # Lưu trữ bất kỳ thư mục anh em nào trùng tên kỹ năng hoặc mã cloud_id
                if destination.parent.exists():
                    for sibling in list(destination.parent.iterdir()):
                        if sibling != destination and sibling.is_dir() and (sibling / 'SKILL.md').is_file():
                            s_name = sibling.name
                            try:
                                s_text = (sibling / 'SKILL.md').read_text(encoding='utf-8')
                                if s_text.startswith('---'):
                                    parts = s_text.split('---', 2)
                                    if len(parts) >= 3:
                                        m = yaml.safe_load(parts[1])
                                        if isinstance(m, dict) and m.get('name'):
                                            s_name = str(m['name']).strip()
                            except Exception:
                                pass
                            if s_name.lower() == skill.name.lower() or (skill.cloud_id and sibling.name == skill.cloud_id):
                                archive_sib = destination.parent / '.abyssal-removed' / f"sibling-dup-{sibling.name}-{time.time_ns()}"
                                archive_sib.parent.mkdir(parents=True, exist_ok=True)
                                try:
                                    shutil.move(str(sibling), str(archive_sib))
                                except Exception:
                                    pass

                # Kiểm tra bất biến: Đã cài đặt & khớp nội dung 100%
                is_installed = (destination / 'SKILL.md').is_file()
                content_differs = cls.skill_differs_at(skill, destination) if is_installed else True

                rule_paths = []
                shared = {}
                if req.enable_always_on:
                    shared = cls.shared_rule_payload(skill, target, workspace)
                    rule_paths = [str(path) for path in shared]

                if is_installed and not content_differs and not req.force_reinstall:
                    rules_differ = False
                    for r_path, r_content in shared.items():
                        if not r_path.exists() or cls.rule_block(r_path.read_text(encoding='utf-8'), skill.id) != cls.rule_block(r_content, skill.id):
                            rules_differ = True
                            break
                    if not rules_differ:
                        installed.append(str(destination))
                        rules.extend(rule_paths)
                        already_installed_targets.append(target)
                        results.append({'target': target, 'status': 'already_installed', 'path': str(destination), 'message': 'Đã có sẵn & khớp 100%'})
                        continue

                if is_installed and content_differs and not req.overwrite and not req.force_reinstall:
                    raise ValueError('Nội dung đã tồn tại khác với thư viện. Vui lòng xem khác biệt và xác nhận cập nhật.')

                payload = {safe_child(destination, name): content for name, content in cls.skill_payload(skill).items()}
                if req.enable_always_on:
                    payload.update(shared)

                if not req.overwrite and not req.force_reinstall:
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
                meta_install = {'rules': manifest}
                if skill.cloud_id:
                    meta_install['cloud_id'] = skill.cloud_id
                payload[safe_child(destination, '.abyssal-install.json')] = json.dumps(meta_install, ensure_ascii=False)
                cls.write_payload(payload)
                installed.append(str(destination))
                rules.extend(rule_paths)
                results.append({'target': target, 'status': 'success', 'path': str(destination)})
            except Exception as error:
                errors.append(f"{target}: {error}")
                results.append({'target': target, 'status': 'error', 'message': str(error)})

        effective_targets = [t for t in req.targets if not (t == 'workspace' and skip_home_workspace)]
        if already_installed_targets and len(already_installed_targets) == len(effective_targets) and not errors:
            return InstallResult(
                True, skill.id, installed_paths=installed, rules_paths=rules,
                message=f"Kỹ năng '{skill.display_title or skill.name}' đã được cài đặt đầy đủ và khớp 100% trên {len(installed)} môi trường (không ghi đè dư thừa).",
                errors=[], status='already_installed', results=results
            )

        success = bool(installed) and not errors
        status = 'success' if success else ('partial' if installed else 'error')
        return InstallResult(success, skill.id, installed_paths=installed, rules_paths=rules,
                             message=f'Đã ghi tệp ở {len(installed)}/{len(set(effective_targets))} môi trường.' + (' Có lỗi cần xử lý.' if errors else ''),
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
        return '---\n' + yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False, width=1000).rstrip() + '\n---\n\n' + skill.skill_content

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
        overwrite: bool = True,
        force_reinstall: bool = False
    ) -> Dict[str, Any]:
        """
        Đồng bộ toàn bộ kho kỹ năng cho tất cả các công cụ AI được chỉ định.
        Mặc định: antigravity, claude, copilot, cursor, windsurf, codex, workspace.
        """
        if not targets:
            targets = ["antigravity", "claude", "copilot", "cursor", "windsurf", "codex", "workspace"]

        active_ws = assert_safe_workspace_path(workspace_path or Path.cwd())
        
        # Dọn sạch các thư mục trùng lặp trước khi bắt đầu đồng bộ
        try:
            cls.deduplicate_all_targets(active_ws)
        except Exception:
            pass

        counts = {target: 0 for target in targets}
        results, errors, installed = [], [], []
        for skill in skills:
            if cancel_event is not None and cancel_event.is_set():
                break
            result = cls.install(skill, InstallRequest(skill.id, targets, str(active_ws), enable_always_on, False, overwrite=overwrite, force_reinstall=force_reinstall))
            installed.extend(result.installed_paths)
            errors.extend(result.errors)
            results.append({'skill_id': skill.id, 'status': result.status, 'results': result.results})
            for item in result.results:
                if item['status'] in ('success', 'already_installed'):
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
