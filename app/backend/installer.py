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
from pathlib import Path
from typing import List, Optional, Dict, Any
from .models import SkillItem, InstallRequest, InstallResult

class SkillInstaller:
    @classmethod
    def install(cls, skill: SkillItem, req: InstallRequest) -> InstallResult:
        installed_paths = []
        rules_paths = []
        errors = []
        home = Path.home()

        # 1. Prepare skill payload content
        # Write temporary directory or assemble files in memory
        for target in req.targets:
            try:
                if target == "antigravity":
                    base_dir = home / ".gemini" / "config" / "skills" / skill.id
                    res_path = cls._write_skill_to_dir(skill, base_dir)
                    installed_paths.append(str(res_path))

                    if req.enable_always_on:
                        r_paths = cls._install_antigravity_rules(skill, home)
                        rules_paths.extend(r_paths)

                elif target == "claude":
                    base_dir = home / ".claude" / "skills" / skill.id
                    res_path = cls._write_skill_to_dir(skill, base_dir)
                    installed_paths.append(str(res_path))

                    if req.enable_always_on:
                        r_paths = cls._install_claude_rules(skill, home)
                        rules_paths.extend(r_paths)

                elif target == "copilot":
                    base_dir = home / ".copilot" / "skills" / skill.id
                    res_path = cls._write_skill_to_dir(skill, base_dir)
                    installed_paths.append(str(res_path))

                elif target == "cursor":
                    ws = Path(req.workspace_path) if req.workspace_path else Path.cwd()
                    base_dir = ws / ".cursor" / "skills" / skill.id
                    res_path = cls._write_skill_to_dir(skill, base_dir)
                    installed_paths.append(str(res_path))

                    if req.enable_always_on:
                        r_paths = cls._install_cursor_rules(skill, ws, home)
                        rules_paths.extend(r_paths)

                elif target == "windsurf":
                    ws = Path(req.workspace_path) if req.workspace_path else Path.cwd()
                    base_dir = ws / ".codeium" / "windsurf" / "skills" / skill.id
                    res_path = cls._write_skill_to_dir(skill, base_dir)
                    installed_paths.append(str(res_path))

                    if req.enable_always_on:
                        r_paths = cls._install_windsurf_rules(skill, ws)
                        rules_paths.extend(r_paths)

                elif target == "aider":
                    ws = Path(req.workspace_path) if req.workspace_path else Path.cwd()
                    base_dir = ws / ".aider" / "skills" / skill.id
                    res_path = cls._write_skill_to_dir(skill, base_dir)
                    installed_paths.append(str(res_path))

                    if req.enable_always_on:
                        r_paths = cls._install_aider_rules(skill, ws)
                        rules_paths.extend(r_paths)

                elif target == "codex":
                    ws = Path(req.workspace_path) if req.workspace_path else Path.cwd()
                    base_dir = home / ".codex" / "skills" / skill.id
                    res_path = cls._write_skill_to_dir(skill, base_dir)
                    installed_paths.append(str(res_path))

                    if req.enable_always_on:
                        r_paths = cls._install_codex_rules(skill, home, ws)
                        rules_paths.extend(r_paths)

                elif target == "workspace":
                    ws = Path(req.workspace_path) if req.workspace_path else Path.cwd()
                    base_dir = ws / ".agents" / "skills" / skill.id
                    res_path = cls._write_skill_to_dir(skill, base_dir)
                    installed_paths.append(str(res_path))

                    if req.enable_always_on:
                        r_paths = cls._install_workspace_rules(skill, ws)
                        rules_paths.extend(r_paths)

            except Exception as e:
                errors.append(f"Target '{target}' failed: {str(e)}")

        # 2. Graphify CLI Integration
        graphify_status = "skipped"
        if req.with_graphify and (skill.has_graphify or "workspace" in req.targets):
            try:
                g_status = cls._run_graphify_integration(req)
                graphify_status = g_status
            except Exception as e:
                graphify_status = f"warning: {str(e)}"

        success = len(installed_paths) > 0 and len(errors) == 0
        message = (
            f"Đã cài đặt thành công '{skill.display_title}' vào {len(installed_paths)} vị trí."
            if success else f"Cài đặt hoàn tất với cảnh báo ({len(errors)} lỗi)."
        )

        return InstallResult(
            success=success,
            skill_id=skill.id,
            installed_paths=installed_paths,
            rules_paths=rules_paths,
            graphify_status=graphify_status,
            message=message,
            errors=errors
        )

    @classmethod
    def uninstall(cls, skill_id: str, targets: List[str], workspace_path: Optional[str] = None) -> Dict[str, Any]:
        """
        Gỡ bỏ sạch sẽ kỹ năng khỏi các công cụ AI được chỉ định.
        Xóa an toàn thư mục skill và dọn dẹp các liên kết liên quan.
        """
        removed_paths = []
        errors = []
        home = Path.home()
        active_ws = Path(workspace_path) if workspace_path else Path.cwd()

        target_dirs = {
            "antigravity": [
                home / ".gemini" / "config" / "skills" / skill_id,
                home / ".gemini" / "antigravity" / "skills" / skill_id
            ],
            "claude": [
                home / ".claude" / "skills" / skill_id
            ],
            "copilot": [
                home / ".copilot" / "skills" / skill_id
            ],
            "cursor": [
                active_ws / ".cursor" / "skills" / skill_id
            ],
            "windsurf": [
                active_ws / ".codeium" / "windsurf" / "skills" / skill_id
            ],
            "aider": [
                active_ws / ".aider" / "skills" / skill_id
            ],
            "codex": [
                home / ".codex" / "skills" / skill_id,
                active_ws / ".codex" / "skills" / skill_id
            ],
            "workspace": [
                active_ws / ".agents" / "skills" / skill_id
            ]
        }

        for target in targets:
            paths = target_dirs.get(target, [])
            for p in paths:
                if p.exists():
                    try:
                        if p.is_dir():
                            shutil.rmtree(p)
                        else:
                            p.unlink()
                        removed_paths.append(str(p))
                    except Exception as e:
                        errors.append(f"Không thể xóa {p}: {str(e)}")

        success = len(removed_paths) > 0 or len(errors) == 0
        return {
            "success": success,
            "skill_id": skill_id,
            "removed_paths": removed_paths,
            "errors": errors,
            "message": f"Đã gỡ bỏ thành công khỏi {len(removed_paths)} vị trí." if success else f"Có lỗi khi gỡ bỏ: {'; '.join(errors)}"
        }

    @classmethod
    def generate_skill_markdown(cls, skill: SkillItem) -> str:
        """Generates the canonical full markdown for a skill (YAML frontmatter + body)."""
        content_lines = ["---"]
        for k, v in skill.yaml_frontmatter.items():
            if isinstance(v, list):
                content_lines.append(f"{k}:")
                for item in v:
                    content_lines.append(f"  - {item}")
            else:
                content_lines.append(f"{k}: {v}")
        if not skill.yaml_frontmatter:
            content_lines.append(f"name: {skill.name}")
            content_lines.append(f"description: {skill.description}")
        content_lines.append("---")
        content_lines.append("")
        content_lines.append(skill.skill_content)
        return "\n".join(content_lines)

    @classmethod
    def _write_skill_to_dir(cls, skill: SkillItem, dest_dir: Path) -> Path:
        dest_dir.mkdir(parents=True, exist_ok=True)

        # Safe Backup: If SKILL.md already exists, create snapshot .bak
        skill_file = dest_dir / "SKILL.md"
        if skill_file.exists():
            try:
                bak_file = dest_dir / "SKILL.md.bak"
                shutil.copy2(skill_file, bak_file)
            except Exception:
                pass

        full_content = cls.generate_skill_markdown(skill)
        skill_file.write_text(full_content, encoding="utf-8")

        # Write references/
        if skill.references:
            ref_dir = dest_dir / "references"
            ref_dir.mkdir(parents=True, exist_ok=True)
            for ref in skill.references:
                ref_file = ref_dir / ref.filename
                ref_file.write_text(ref.content, encoding="utf-8")

        # Write rules/
        if skill.rules:
            rule_dir = dest_dir / "rules"
            rule_dir.mkdir(parents=True, exist_ok=True)
            for rule in skill.rules:
                rule_file = rule_dir / rule.filename
                rule_file.write_text(rule.content, encoding="utf-8")

        return dest_dir

    @staticmethod
    def _install_antigravity_rules(skill: SkillItem, home: Path) -> List[str]:
        installed = []
        rules_dir = home / ".gemini" / "config" / "rules"
        rules_dir.mkdir(parents=True, exist_ok=True)

        for rule in skill.rules:
            if "always-on" in rule.filename:
                target = rules_dir / "always-on-autopilot.md"
                target.write_text(rule.content, encoding="utf-8")
                installed.append(str(target))
            elif "GEMINI" in rule.filename:
                # Copy to ~/.gemini/GEMINI.md and ~/.gemini/config/GEMINI.md
                t1 = home / ".gemini" / "GEMINI.md"
                t2 = home / ".gemini" / "config" / "GEMINI.md"
                t1.parent.mkdir(parents=True, exist_ok=True)
                t2.parent.mkdir(parents=True, exist_ok=True)
                t1.write_text(rule.content, encoding="utf-8")
                t2.write_text(rule.content, encoding="utf-8")
                installed.extend([str(t1), str(t2)])

        return installed

    @staticmethod
    def _install_claude_rules(skill: SkillItem, home: Path) -> List[str]:
        installed = []
        claude_dir = home / ".claude"
        claude_dir.mkdir(parents=True, exist_ok=True)

        for rule in skill.rules:
            if "GEMINI" in rule.filename or "CLAUDE" in rule.filename:
                target = claude_dir / "CLAUDE.md"
                target.write_text(rule.content, encoding="utf-8")
                installed.append(str(target))
        return installed

    @staticmethod
    def _install_workspace_rules(skill: SkillItem, ws: Path) -> List[str]:
        installed = []
        ws_rules = ws / ".agents" / "rules"
        ws_rules.mkdir(parents=True, exist_ok=True)

        for rule in skill.rules:
            if "always-on" in rule.filename:
                # 1. Antigravity & Generic Workspace Agent rule
                target = ws_rules / "always-on-autopilot.md"
                target.write_text(rule.content, encoding="utf-8")
                installed.append(str(target))

                # 2. Cursor AI (.cursorrules & .cursor/rules/*.mdc)
                cursor_file = ws / ".cursorrules"
                cursor_file.write_text(rule.content, encoding="utf-8")
                installed.append(str(cursor_file))

                cursor_mdc_dir = ws / ".cursor" / "rules"
                cursor_mdc_dir.mkdir(parents=True, exist_ok=True)
                cursor_mdc = cursor_mdc_dir / "always-on-autopilot.mdc"
                cursor_mdc.write_text(rule.content, encoding="utf-8")
                installed.append(str(cursor_mdc))

                # 3. Windsurf (.windsurfrules)
                windsurf_file = ws / ".windsurfrules"
                windsurf_file.write_text(rule.content, encoding="utf-8")
                installed.append(str(windsurf_file))

                # 4. GitHub Copilot (.github/copilot-instructions.md)
                copilot_dir = ws / ".github"
                copilot_dir.mkdir(parents=True, exist_ok=True)
                copilot_file = copilot_dir / "copilot-instructions.md"
                copilot_file.write_text(rule.content, encoding="utf-8")
                installed.append(str(copilot_file))

                # 5. Aider (CONVENTIONS.md)
                aider_file = ws / "CONVENTIONS.md"
                aider_file.write_text(rule.content, encoding="utf-8")
                installed.append(str(aider_file))

                # 6. OpenAI Codex (CODEX.md & .codex/rules/always-on-autopilot.md)
                codex_file = ws / "CODEX.md"
                codex_file.write_text(rule.content, encoding="utf-8")
                installed.append(str(codex_file))

                codex_md_dir = ws / ".codex" / "rules"
                codex_md_dir.mkdir(parents=True, exist_ok=True)
                codex_rule = codex_md_dir / "always-on-autopilot.md"
                codex_rule.write_text(rule.content, encoding="utf-8")
                installed.append(str(codex_rule))

            elif "GEMINI" in rule.filename:
                t1 = ws / "GEMINI.md"
                t2 = ws / "AGENTS.md"
                t1.write_text(rule.content, encoding="utf-8")
                t2.write_text(rule.content, encoding="utf-8")
                installed.extend([str(t1), str(t2)])
        return installed

    @staticmethod
    def _install_cursor_rules(skill: SkillItem, ws: Path, home: Path) -> List[str]:
        installed = []
        for rule in skill.rules:
            if "always-on" in rule.filename:
                c_file = ws / ".cursorrules"
                c_file.write_text(rule.content, encoding="utf-8")
                installed.append(str(c_file))

                c_mdc_dir = ws / ".cursor" / "rules"
                c_mdc_dir.mkdir(parents=True, exist_ok=True)
                c_mdc = c_mdc_dir / "always-on-autopilot.mdc"
                c_mdc.write_text(rule.content, encoding="utf-8")
                installed.append(str(c_mdc))
        return installed

    @staticmethod
    def _install_windsurf_rules(skill: SkillItem, ws: Path) -> List[str]:
        installed = []
        for rule in skill.rules:
            if "always-on" in rule.filename:
                w_file = ws / ".windsurfrules"
                w_file.write_text(rule.content, encoding="utf-8")
                installed.append(str(w_file))
        return installed

    @staticmethod
    def _install_aider_rules(skill: SkillItem, ws: Path) -> List[str]:
        installed = []
        for rule in skill.rules:
            if "always-on" in rule.filename:
                a_file = ws / "CONVENTIONS.md"
                a_file.write_text(rule.content, encoding="utf-8")
                installed.append(str(a_file))
        return installed

    @staticmethod
    def _install_codex_rules(skill: SkillItem, home: Path, ws: Path) -> List[str]:
        installed = []
        # 1. Global ~/.codex/rules/
        global_codex_rules = home / ".codex" / "rules"
        global_codex_rules.mkdir(parents=True, exist_ok=True)
        # 2. Workspace .codex/rules/
        ws_codex_rules = ws / ".codex" / "rules"
        ws_codex_rules.mkdir(parents=True, exist_ok=True)

        for rule in skill.rules:
            if "always-on" in rule.filename:
                # Global always-on rule
                g_target = global_codex_rules / "always-on-autopilot.md"
                g_target.write_text(rule.content, encoding="utf-8")
                installed.append(str(g_target))

                # Workspace root CODEX.md instructions
                w_target = ws / "CODEX.md"
                w_target.write_text(rule.content, encoding="utf-8")
                installed.append(str(w_target))

                # Workspace .codex/rules/
                w_rule = ws_codex_rules / "always-on-autopilot.md"
                w_rule.write_text(rule.content, encoding="utf-8")
                installed.append(str(w_rule))
        return installed

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
        workspace_path: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Đồng bộ toàn bộ kho kỹ năng cho tất cả các công cụ AI được chỉ định.
        Mặc định: antigravity, claude, copilot, cursor, windsurf, codex, workspace.
        """
        if not targets:
            targets = ["antigravity", "claude", "copilot", "cursor", "windsurf", "codex", "workspace"]

        active_ws = Path(workspace_path) if workspace_path else Path.cwd()
        target_counts = {t: 0 for t in targets}
        all_installed_paths = []
        errors = []

        for skill in skills:
            req = InstallRequest(
                skill_id=skill.id,
                targets=targets,
                workspace_path=str(active_ws),
                enable_always_on=True,
                with_graphify=False
            )
            res = cls.install(skill, req)
            if res.success:
                for p in res.installed_paths:
                    all_installed_paths.append(p)
                    p_lower = p.lower()
                    if ".gemini" in p_lower:
                        target_counts["antigravity"] = target_counts.get("antigravity", 0) + 1
                    elif ".claude" in p_lower:
                        target_counts["claude"] = target_counts.get("claude", 0) + 1
                    elif ".copilot" in p_lower:
                        target_counts["copilot"] = target_counts.get("copilot", 0) + 1
                    elif ".cursor" in p_lower:
                        target_counts["cursor"] = target_counts.get("cursor", 0) + 1
                    elif ".codeium" in p_lower or "windsurf" in p_lower:
                        target_counts["windsurf"] = target_counts.get("windsurf", 0) + 1
                    elif ".codex" in p_lower or "codex" in p_lower:
                        target_counts["codex"] = target_counts.get("codex", 0) + 1
                    elif ".agents" in p_lower:
                        target_counts["workspace"] = target_counts.get("workspace", 0) + 1
            if res.errors:
                errors.extend(res.errors)

        return {
            "success": len(errors) == 0 or len(all_installed_paths) > 0,
            "total_skills": len(skills),
            "targets": targets,
            "target_counts": target_counts,
            "total_installed_files": len(all_installed_paths),
            "workspace_path": str(active_ws),
            "errors": errors[:5],
            "message": f"Đã đồng bộ thành công {len(skills)} kỹ năng vào {len(targets)} môi trường AI!"
        }

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
        active_ws = Path(workspace_path) if workspace_path else Path.cwd()
        if not active_ws.exists():
            active_ws.mkdir(parents=True, exist_ok=True)

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

        try:
            if "cursorrules" in rule_types:
                c_file = active_ws / ".cursorrules"
                c_file.write_text(rule_content, encoding="utf-8")
                created_files.append(str(c_file))

            if "windsurfrules" in rule_types:
                w_file = active_ws / ".windsurfrules"
                w_file.write_text(rule_content, encoding="utf-8")
                created_files.append(str(w_file))

            if "claude" in rule_types:
                cl_file = active_ws / "CLAUDE.md"
                cl_file.write_text(rule_content, encoding="utf-8")
                created_files.append(str(cl_file))

            if "copilot" in rule_types:
                gh_dir = active_ws / ".github"
                gh_dir.mkdir(parents=True, exist_ok=True)
                cp_file = gh_dir / "copilot-instructions.md"
                cp_file.write_text(rule_content, encoding="utf-8")
                created_files.append(str(cp_file))

            if "agent_rules" in rule_types:
                ag_dir = active_ws / ".agents" / "rules"
                ag_dir.mkdir(parents=True, exist_ok=True)
                ar_file = ag_dir / "always-on-autopilot.md"
                ar_file.write_text(rule_content, encoding="utf-8")
                created_files.append(str(ar_file))

            if "codex" in rule_types:
                cx_file = active_ws / "CODEX.md"
                cx_file.write_text(rule_content, encoding="utf-8")
                created_files.append(str(cx_file))

                cx_dir = active_ws / ".codex" / "rules"
                cx_dir.mkdir(parents=True, exist_ok=True)
                cx_rule = cx_dir / "always-on-autopilot.md"
                cx_rule.write_text(rule_content, encoding="utf-8")
                created_files.append(str(cx_rule))
        except Exception as e:
            errors.append(str(e))

        return {
            "success": len(created_files) > 0 and len(errors) == 0,
            "created_files": created_files,
            "workspace_path": str(active_ws),
            "errors": errors,
            "message": f"Đã khởi tạo thành công {len(created_files)} tệp quy tắc cho dự án!" if len(created_files) > 0 else f"Lỗi tạo quy tắc: {'; '.join(errors)}"
        }
