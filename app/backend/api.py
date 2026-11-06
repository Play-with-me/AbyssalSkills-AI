"""
AbyssalSkillsD - Desktop API Bridge
Exposed directly to Frontend via window.pywebview.api
Provides structured Graphify statistics, multi-target installation,
batch installation for the complete Skill-AI-private suite,
and Supabase Community Cloud integration.
"""
import os
import sys
import json
import re
import uuid
import hashlib
import subprocess
import threading
from pathlib import Path
from typing import Dict, Any, List, Optional
from .models import SkillItem, InstallRequest
from .storage import SkillStorage
from .installer import SkillInstaller
from .scanner import SkillScanner
from .git_sync import GitSyncEngine
from .auth import AuthEngine
from .updater import UpdateEngine
from .paths import get_log_dir, assert_safe_workspace_path, atomic_write, validate_skill_id
from .logger import get_logger, get_recent_logs, export_diagnostic_zip, sanitize_sensitive_data

class DesktopAPI:
    def __init__(self):
        SkillStorage.initialize()
        self.active_workspace = str(Path.cwd())
        self._cancel_install = threading.Event()
        self._batch_lock = threading.Lock()

    def get_active_workspace(self) -> Dict[str, Any]:
        """Returns the currently active coding project workspace."""
        p = Path(self.active_workspace)
        return {
            "success": True,
            "path": self.active_workspace,
            "workspace_path": self.active_workspace,
            "name": p.name or self.active_workspace,
            "exists": p.exists()
        }

    def set_active_workspace(self, data: Any) -> Dict[str, Any]:
        """Sets the active coding project workspace. Accepts a path string or dict {"path": ...}."""
        if isinstance(data, dict):
            path = data.get("path") or data.get("workspace_path", "")
        else:
            path = str(data) if data else ""

        if not path:
            return {"success": False, "message": "Đường dẫn không hợp lệ."}
        
        try:
            p = assert_safe_workspace_path(path)
        except Exception as e:
            return {"success": False, "message": f"Từ chối đường dẫn không an toàn: {str(e)}"}
        
        self.active_workspace = str(p)
        return {
            "success": True,
            "path": self.active_workspace,
            "workspace_path": self.active_workspace,
            "name": p.name,
            "message": f"Đã chuyển dự án làm việc sang '{p.name}'"
        }

    def get_skills(self, workspace_path: Optional[str] = None) -> List[Dict[str, Any]]:
        """Returns all skills for the main store/library."""
        ws = workspace_path or getattr(self, "active_workspace", str(Path.cwd()))
        skills = SkillStorage.get_all_skills(ws)
        return [s.to_dict() for s in skills]

    def get_skill(self, skill_id: str, workspace_path: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """Returns complete detail of a specific skill."""
        ws = workspace_path or getattr(self, "active_workspace", str(Path.cwd()))
        skill = SkillStorage.get_skill(skill_id, ws)
        return skill.to_dict() if skill else None

    def get_skill_diff(self, data: Any) -> Dict[str, Any]:
        """
        Loads both the current local version from disk and the registry version
        for side-by-side comparison before accepting updates.
        Computes structured diff chunks and synchronized row alignment.
        """
        import difflib
        skill_id = data if isinstance(data, str) else (data.get("skill_id") if isinstance(data, dict) else "")
        workspace_path = getattr(self, "active_workspace", str(Path.cwd()))
        if isinstance(data, dict) and data.get("workspace_path"):
            workspace_path = data["workspace_path"]

        skill = SkillStorage.get_skill(skill_id, workspace_path)
        if not skill:
            return {"success": False, "message": f"Không tìm thấy kỹ năng '{skill_id}'"}

        from app.backend.installer import SkillInstaller
        candidates = []
        for target in skill.installed_targets:
            if target not in SkillInstaller.TARGETS:
                continue
            for path, content in SkillInstaller.target_payload(skill, target, workspace_path).items():
                candidates.append({'target': target, 'path': str(path), 'content': content,
                                   'label': target + ' · ' + str(path)})
        if not candidates:
            return {'success': False, 'message': 'Chưa có bản cài để xem khác biệt.'}
        requested = data.get('file_path') if isinstance(data, dict) else None
        selected = next((item for item in candidates if item['path'] == requested), candidates[0])
        local_path_str = selected['path']
        new_content = selected['content']
        local_file = Path(local_path_str)
        local_content = local_file.read_text(encoding='utf-8') if local_file.exists() else ''
        view_token = uuid.uuid4().hex
        snapshot = {item['path']: hashlib.sha256(Path(item['path']).read_bytes()).hexdigest() if Path(item['path']).exists() else None for item in candidates}
        if not hasattr(self, '_diff_views'):
            self._diff_views = {}
        # Bounded, server-owned snapshots prevent client-supplied hashes from authorizing stale writes.
        if len(self._diff_views) >= 32:
            self._diff_views.pop(next(iter(self._diff_views)))
        self._diff_views[view_token] = {'skill_id': skill_id, 'workspace': workspace_path,
                                      'files': snapshot, 'expected': {item['path']: hashlib.sha256(item['content'].encode()).hexdigest() for item in candidates}, 'selected': local_path_str,
                                      'canonical': hashlib.sha256(json.dumps(candidates, sort_keys=True).encode()).hexdigest()}

        # Compute line-by-line diff and structured chunks
        local_lines = local_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)

        matcher = difflib.SequenceMatcher(None, local_lines, new_lines)
        opcodes = matcher.get_opcodes()

        chunks = []
        left_rows = []
        right_rows = []
        chunk_id = 0
        total_added = 0
        total_deleted = 0

        for tag, i1, i2, j1, j2 in opcodes:
            if tag == "equal":
                count = i2 - i1
                for k in range(count):
                    left_rows.append({
                        "type": "equal",
                        "line_num": i1 + k + 1,
                        "text": local_lines[i1 + k],
                        "chunk_id": None
                    })
                    right_rows.append({
                        "type": "equal",
                        "line_num": j1 + k + 1,
                        "text": new_lines[j1 + k],
                        "chunk_id": None
                    })
            else:
                # Find nearest Markdown header for contextual title
                title = ""
                for l in reversed(new_lines[:j1]):
                    if l.strip().startswith("#"):
                        title = l.strip().lstrip("#").strip()
                        break
                if not title:
                    for l in reversed(local_lines[:i1]):
                        if l.strip().startswith("#"):
                            title = l.strip().lstrip("#").strip()
                            break
                if not title:
                    title = f"Dòng {i1+1}-{max(i1+1, i2)}"
                else:
                    title = f"{title} (Dòng {i1+1}-{max(i1+1, i2)})"

                l_count = i2 - i1
                r_count = j2 - j1
                max_count = max(l_count, r_count)

                added = r_count if tag in ("insert", "replace") else 0
                deleted = l_count if tag in ("delete", "replace") else 0
                total_added += added
                total_deleted += deleted

                chunks.append({
                    "id": chunk_id,
                    "tag": tag,
                    "title": title,
                    "local_start": i1 + 1,
                    "local_end": i2,
                    "new_start": j1 + 1,
                    "new_end": j2,
                    "added": added,
                    "deleted": deleted
                })

                for k in range(max_count):
                    if k < l_count:
                        left_rows.append({
                            "type": "delete",
                            "line_num": i1 + k + 1,
                            "text": local_lines[i1 + k],
                            "chunk_id": chunk_id
                        })
                    else:
                        left_rows.append({
                            "type": "empty",
                            "line_num": "",
                            "text": "",
                            "chunk_id": chunk_id
                        })

                    if k < r_count:
                        right_rows.append({
                            "type": "add",
                            "line_num": j1 + k + 1,
                            "text": new_lines[j1 + k],
                            "chunk_id": chunk_id
                        })
                    else:
                        right_rows.append({
                            "type": "empty",
                            "line_num": "",
                            "text": "",
                            "chunk_id": chunk_id
                        })

                chunk_id += 1

        return {
            "success": True,
            "skill_id": skill.id,
            "display_title": skill.display_title or skill.name,
            "local_path": local_path_str,
            "revision_token": view_token,
            "files": [{'path': item['path'], 'label': item['label']} for item in candidates],
            "local_content": local_content,
            "new_content": new_content,
            "new_version": skill.version or "1.0.0",
            "has_update": skill.has_update,
            "targets": skill.installed_targets or ["antigravity"],
            "chunks": chunks,
            "diff_stats": {
                "total_chunks": len(chunks),
                "added_lines": total_added,
                "deleted_lines": total_deleted
            },
            "aligned_rows": {
                "left": left_rows,
                "right": right_rows
            }
        }

    def apply_skill_diff(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Applies either all changes or selectively chosen diff chunks to local skill.
        Automatically creates a snapshot backup (.bak) before modifying.
        """
        skill_id = data.get("skill_id")
        selected_chunks = data.get("selected_chunks", [])
        apply_all = data.get("apply_all", False)
        workspace_path = data.get("workspace_path") or getattr(self, "active_workspace", str(Path.cwd()))

        if not skill_id:
            return {"success": False, "message": "Thiếu skill_id để áp dụng cập nhật."}

        skill = SkillStorage.get_skill(skill_id, workspace_path)
        if not skill:
            return {"success": False, "message": f"Không tìm thấy kỹ năng '{skill_id}'"}

        from app.backend.installer import SkillInstaller
        view_token = data.get('revision_token')
        view = getattr(self, '_diff_views', {}).get(view_token)
        if not view or view['skill_id'] != skill_id or view['workspace'] != workspace_path:
            return {'success': False, 'status': 'error', 'error_code': 'DIFF_REQUIRED', 'message': 'Vui lòng mở lại so sánh trước khi cập nhật.'}
        candidates = {}
        for target in skill.installed_targets:
            if target in SkillInstaller.TARGETS:
                candidates.update({str(path): content for path, content in SkillInstaller.target_payload(skill, target, workspace_path).items()})
        for name, digest in view['files'].items():
            current = hashlib.sha256(Path(name).read_bytes()).hexdigest() if Path(name).exists() else None
            if current != digest:
                return {'success': False, 'status': 'error', 'error_code': 'STALE_DIFF', 'message': 'Tệp đã thay đổi sau khi mở so sánh. Hãy mở lại để bảo vệ chỉnh sửa mới.'}
        if any(name not in candidates or hashlib.sha256(candidates[name].encode()).hexdigest() != digest for name, digest in view['expected'].items()):
            return {'success': False, 'status': 'error', 'error_code': 'STALE_REGISTRY', 'message': 'Thư viện đã thay đổi. Hãy mở lại so sánh.'}
        local_path_str = view['selected']
        if local_path_str not in candidates:
            return {'success': False, 'status': 'error', 'message': 'Đích cập nhật đã thay đổi.'}
        local_file = Path(local_path_str)
        local_content = local_file.read_text(encoding='utf-8') if local_file.exists() else ''
        new_content = candidates[local_path_str]
        if apply_all:
            try:
                atomic_write(local_file, new_content, backup=True)
                self._diff_views.pop(view_token, None)
                return {'success': True, 'status': 'success', 'message': 'Đã cập nhật tệp đang xem và lưu snapshot bản cũ.'}
            except (OSError, ValueError) as error:
                return {'success': False, 'status': 'error', 'message': str(error)}

        import difflib
        local_lines = local_content.splitlines(keepends=True)
        new_lines = new_content.splitlines(keepends=True)

        matcher = difflib.SequenceMatcher(None, local_lines, new_lines)
        opcodes = matcher.get_opcodes()

        selected_set = set(selected_chunks) if isinstance(selected_chunks, (list, set, tuple)) else set()
        changes = sum(tag != 'equal' for tag, *_ in opcodes)
        if not selected_set or not selected_set.issubset(set(range(changes))):
            return {"success": False, "message": "Vui lòng chọn ít nhất một khối thay đổi hoặc bấm 'Giữ Lại Bản Cũ'."}

        merged_lines = []
        chunk_idx = 0
        for tag, i1, i2, j1, j2 in opcodes:
            if tag == "equal":
                merged_lines.extend(local_lines[i1:i2])
            else:
                if chunk_idx in selected_set:
                    merged_lines.extend(new_lines[j1:j2])
                else:
                    merged_lines.extend(local_lines[i1:i2])
                chunk_idx += 1

        merged_content = "".join(merged_lines)

        try:
            atomic_write(local_file, merged_content, backup=True)
        except Exception as e:
            return {"success": False, "status": "error", "message": f"Không thể sao lưu hoặc ghi tệp: {e}"}

        # 3. Update skill state
        if merged_content.strip() == new_content.strip():
            skill.has_update = False
        SkillStorage.upsert_skill(skill)

        return {
            "success": True,
            "message": f"✓ Đã áp dụng thành công {len(selected_set)} khối thay đổi cho kỹ năng '{skill.display_title or skill.name}'! (Snapshot bản cũ nằm cạnh tệp đã sửa)",
            "applied_chunks": len(selected_set)
        }

    def uninstall_skill(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Gỡ bỏ sạch sẽ kỹ năng khỏi các công cụ AI được chỉ định.
        """
        skill_id = data.get("skill_id")
        targets = data.get("targets", [])
        workspace_path = data.get("workspace_path") or getattr(self, "active_workspace", str(Path.cwd()))

        if not skill_id:
            return {"success": False, "message": "Thiếu skill_id để gỡ cài đặt."}
        if not targets:
            return {"success": False, "message": "Vui lòng chọn ít nhất một công cụ AI để gỡ bỏ."}

        res = SkillInstaller.uninstall(skill_id, targets, workspace_path)

        # Refresh skill installed_targets in storage
        skill = SkillStorage.get_skill(skill_id, workspace_path)
        if skill:
            skill.installed_targets = SkillScanner.detect_installed_targets(skill.id, workspace_path)
            SkillStorage.upsert_skill(skill)

        return res

    def install_skill(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Executes multi-target installation for a single skill.
        """
        skill_id = data.get("skill_id")
        workspace_path = data.get("workspace_path") or getattr(self, "active_workspace", str(Path.cwd()))
        skill = SkillStorage.get_skill(skill_id, workspace_path)
        if not skill:
            return {"success": False, "message": f"Không tìm thấy kỹ năng '{skill_id}'"}

        req = InstallRequest(
            skill_id=skill_id,
            targets=data.get("targets", ["antigravity"]),
            workspace_path=workspace_path,
            enable_always_on=data.get("enable_always_on", True),
            with_graphify=data.get("with_graphify", True),
            overwrite=bool(data.get("overwrite", False))
        )

        res = SkillInstaller.install(skill, req)
        
        skill.installed_targets = SkillScanner.detect_installed_targets(skill.id, workspace_path)
        skill.always_on_enabled = SkillScanner.detect_always_on_enabled()
        SkillStorage.upsert_skill(skill)

        return {
            "success": res.success,
            "status": res.status,
            "results": res.results,
            "message": res.message,
            "installed_paths": res.installed_paths,
            "rules_paths": res.rules_paths,
            "graphify_status": res.graphify_status,
            "errors": res.errors
        }

    def sync_all_ais(self, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Đồng bộ toàn bộ kho kỹ năng (36 kỹ năng) vào tất cả các môi trường AI trên máy.
        """
        data = data or {}
        workspace_path = data.get("workspace_path") or getattr(self, "active_workspace", str(Path.cwd()))
        targets = data.get("targets")
        skill_ids = data.get("skill_ids")
        overwrite = data.get("overwrite", True)

        skills = SkillStorage.get_all_skills(workspace_path)
        if skill_ids:
            skills = [s for s in skills if s.id in skill_ids]

        if not self._batch_lock.acquire(blocking=False):
            return {'success': False, 'status': 'error', 'error_code': 'BUSY', 'message': 'Một đợt cài đặt đang chạy.'}
        try:
            self._cancel_install.clear()
            return SkillInstaller.sync_all_ais(skills, targets, workspace_path, self._cancel_install, overwrite=overwrite)
        finally:
            self._batch_lock.release()

    def cancel_operation(self):
        self._cancel_install.set()
        return {'success': True, 'status': 'cancelled', 'message': 'Sẽ dừng sau mục đang xử lý; kết quả đã ghi vẫn được giữ.'}

    def generate_project_rules(self, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Tự động sinh giàn giáo các tệp quy tắc cho dự án (.cursorrules, .windsurfrules, CLAUDE.md...).
        """
        data = data or {}
        workspace_path = data.get("workspace_path") or getattr(self, "active_workspace", str(Path.cwd()))
        rule_types = data.get("rule_types")

        skills = SkillStorage.get_all_skills(workspace_path)
        return SkillInstaller.generate_rule_scaffold(workspace_path, rule_types, skills)

    def install_all_skills(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Batch-installs skills across targets (supports filtering by source_group or skill_ids).
        """
        targets = data.get("targets") or ["antigravity", "cursor", "windsurf", "claude", "copilot", "codex", "workspace"]
        enable_always_on = data.get("enable_always_on", True)
        with_graphify = data.get("with_graphify", True)
        workspace_path = data.get("workspace_path", str(Path.cwd()))
        source_group = data.get("source_group")
        skill_ids = data.get("skill_ids")
        only_new = data.get("only_new", False)
        overwrite = data.get("overwrite", True)

        skills = SkillStorage.get_all_skills(workspace_path)
        if skill_ids:
            skills = [s for s in skills if s.id in skill_ids]
        elif only_new:
            skills = [s for s in skills if not s.installed_targets]
        elif source_group:
            skills = [s for s in skills if s.source_group == source_group]

        if not self._batch_lock.acquire(blocking=False):
            return {'success': False, 'status': 'error', 'error_code': 'BUSY', 'message': 'Một đợt cài đặt đang chạy.'}
        try:
            self._cancel_install.clear()
            result = SkillInstaller.sync_all_ais(skills, targets, workspace_path, self._cancel_install, enable_always_on, overwrite=overwrite)
            result['count'] = sum(row['status'] == 'success' for row in result['results'])
            return result
        finally:
            self._batch_lock.release()

    def get_community_schema(self) -> Dict[str, Any]:
        """Returns the PostgreSQL & Supabase RLS schema for Phase 2 Community Hub."""
        schema_path = Path("app/data/supabase_community_schema.sql")
        if schema_path.exists():
            return {
                "success": True,
                "sql": schema_path.read_text(encoding="utf-8"),
                "tables": ["profiles", "skills", "skill_references"],
                "features": ["Row Level Security (RLS)", "Full-Text Search GIN Index", "Role-Based Access"]
            }
        return {"success": False, "message": "Schema file not found."}

    def save_skill(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Creates or updates a custom skill."""
        try:
            skill_id = data.get("id") or data.get("name", "").lower().replace(" ", "-")
            data["id"] = skill_id
            data["name"] = skill_id
            if not data.get("display_title"):
                data["display_title"] = skill_id.replace("-", " ").title()

            skill = SkillItem.from_dict(data)
            saved = SkillStorage.upsert_skill(skill)
            return {"success": True, "skill": saved.to_dict(), "message": "Đã lưu kỹ năng vào thư viện thành công!"}
        except Exception as e:
            return {"success": False, "message": f"Lỗi khi lưu kỹ năng: {str(e)}"}

    def delete_skill(self, skill_id: str) -> Dict[str, Any]:
        """Deletes a skill from library."""
        ok = SkillStorage.delete_skill(skill_id)
        return {"success": ok, "message": "Đã xóa kỹ năng khỏi thư viện." if ok else "Không tìm thấy kỹ năng để xóa."}

    def toggle_favorite(self, skill_id: str) -> Dict[str, Any]:
        """Toggles favorite state."""
        fav = SkillStorage.toggle_favorite(skill_id)
        return {"success": True, "is_favorite": fav}

    def import_from_github(self, repo_url: str) -> Dict[str, Any]:
        """Clones or pulls from GitHub repository and registers new skills."""
        ok, msg, skills = GitSyncEngine.import_from_github(repo_url)
        if ok:
            for s in skills:
                SkillStorage.upsert_skill(s)
            return {
                "success": True,
                "message": msg,
                "count": len(skills),
                "skills": [s.to_dict() for s in skills]
            }
        return {"success": False, "message": msg}

    def scan_local_folder(self, folder_path: str) -> Dict[str, Any]:
        """Scans a local directory and imports skills."""
        p = Path(folder_path.strip('"\' '))
        if not p.exists() or not p.is_dir():
            return {"success": False, "message": f"Đường dẫn '{folder_path}' không tồn tại hoặc không phải thư mục."}

        skills = SkillScanner.scan_skill_directory(p)
        if not skills:
            return {"success": False, "message": "Không tìm thấy file SKILL.md hợp lệ trong thư mục này."}

        for s in skills:
            SkillStorage.upsert_skill(s)

        return {
            "success": True,
            "message": f"Đã nạp thành công {len(skills)} kỹ năng từ thư mục máy tính.",
            "count": len(skills),
            "skills": [s.to_dict() for s in skills]
        }

    def pick_folder_dialog(self) -> Dict[str, Any]:
        """Opens native Windows folder selection dialog using PowerShell without blocking UI."""
        ps_script = """
        Add-Type -AssemblyName System.Windows.Forms
        $f = New-Object System.Windows.Forms.FolderBrowserDialog
        $f.Description = 'Chọn thư mục chứa Kỹ năng AI (SKILL.md)'
        $f.ShowNewFolderButton = $false
        if ($f.ShowDialog() -eq [System.Windows.Forms.DialogResult]::OK) {
            Write-Output $f.SelectedPath
        }
        """
        flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
        try:
            res = subprocess.run(
                ["powershell", "-NoProfile", "-Command", ps_script],
                capture_output=True,
                text=True,
                timeout=30,
                creationflags=flags
            )
            selected = res.stdout.strip()
            if selected and Path(selected).exists():
                return {"success": True, "path": selected}
            return {"success": False, "message": "Người dùng đã hủy chọn thư mục."}
        except Exception as e:
            return {"success": False, "message": f"Không thể mở hộp thoại chọn thư mục: {str(e)}"}

    def run_graphify(self, target_path: Optional[str] = None, force: bool = False) -> Dict[str, Any]:
        """
        Executes Graphify AST analysis on a workspace and returns structured metrics.
        Fast-path cache check prevents high CPU spikes and UI frame drops during app launch.
        """
        path_to_graph = target_path if target_path else str(Path.cwd())
        report_file = Path(path_to_graph) / "graphify-out" / "GRAPH_REPORT.md"
        graph_file = Path(path_to_graph) / "graphify-out" / "graph.json"
        
        # If cache exists and force is False, read instantly without spawning heavy subprocess
        # Fast-guard: never run heavy subprocess in background unless explicitly forced by user
        should_run_cmd = force
        res_output = ""
        res_success = False

        if should_run_cmd:
            flags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0
            try:
                cmd = ["uv", "run", "graphify", "update", path_to_graph, "--force"]
                res = subprocess.run(cmd, capture_output=True, text=True, timeout=25, creationflags=flags)
                res_success = res.returncode == 0
                res_output = res.stdout[:500] if res.stdout else (res.stderr[:500] if res.stderr else "")
            except Exception as e:
                res_success = False
                res_output = str(e)
        
        try:
            nodes_count = 0
            edges_count = 0
            communities_count = 0
            extraction_rate = None
            god_nodes = []
            report_text = ""

            if graph_file.exists():
                try:
                    g_data = json.loads(graph_file.read_text(encoding="utf-8"))
                    nodes_count = len(g_data.get("nodes", []))
                    edges_count = len(g_data.get("links", [])) or len(g_data.get("edges", []))
                except Exception:
                    pass

            if report_file.exists():
                report_text = report_file.read_text(encoding="utf-8", errors="replace")
                god_matches = re.findall(r"(\d+)\.\s+`([^`]+)`\s+-\s+(\d+)\s+edges", report_text)
                for rank, name, edges in god_matches[:8]:
                    god_nodes.append({
                        "rank": int(rank),
                        "name": name,
                        "edges": int(edges),
                        "percentage": min(100, int(int(edges) * 3.5))
                    })

                sum_match = re.search(r"(\d+)\s+nodes\s+·\s+(\d+)\s+edges\s+·\s+(\d+)\s+communities", report_text)
                if sum_match:
                    nodes_count = int(sum_match.group(1))
                    edges_count = int(sum_match.group(2))
                    communities_count = int(sum_match.group(3))

                rate_match = re.search(r"Extraction:\s+([\d\.]+%)\s+EXTRACTED", report_text)
                if rate_match:
                    extraction_rate = rate_match.group(1)

            return {
                "success": res_success if force else graph_file.exists(),
                "status": "success" if (res_success if force else graph_file.exists()) else "error",
                "message": "Đã đọc kết quả Graphify đã lưu." if graph_file.exists() else "Chưa có kết quả phân tích Graphify.",
                "has_report": report_file.exists(),
                "nodes_count": nodes_count,
                "edges_count": edges_count,
                "communities_count": communities_count,
                "extraction_rate": extraction_rate,
                "god_nodes": god_nodes,
                "report_raw": report_text,
                "output": res_output
            }
        except Exception as e:
            return {"success": False, "message": f"Lỗi chạy Graphify: {str(e)}"}

    def get_system_info(self) -> Dict[str, Any]:
        """Returns detected environment paths and status."""
        home = Path.home()
        return {
            "workspace": str(Path.cwd()),
            "antigravity_global": str(home / ".gemini" / "config" / "skills"),
            "claude_global": str(home / ".claude" / "skills"),
            "copilot_global": str(home / ".copilot" / "skills"),
            "always_on_active": SkillScanner.detect_always_on_enabled(),
            "graphify_available": True
        }

    def open_folder(self, folder_path: str) -> Dict[str, Any]:
        """Opens a folder in Windows Explorer."""
        try:
            os.startfile(folder_path)
            return {"success": True}
        except Exception as e:
            return {"success": False, "message": str(e)}

    # =========================================================================
    # Supabase Authentication & Secret Key Management (supabase-backend-architect)
    # =========================================================================
    def auth_sign_in(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Signs in user using email and password."""
        return AuthEngine.sign_in(data.get("email", ""), data.get("password", ""))

    def auth_sign_in_oauth(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Signs in user using OAuth provider (Google / GitHub)."""
        provider = data.get("provider", "google") if isinstance(data, dict) else "google"
        use_loopback = bool(data.get("use_loopback", False)) if isinstance(data, dict) else False
        if use_loopback:
            return AuthEngine.start_oauth(provider)
        return AuthEngine.sign_in_with_oauth(provider)

    def auth_check_oauth_status(self) -> Dict[str, Any]:
        """Checks if Desktop OAuth loopback received token from browser redirect."""
        return AuthEngine.check_oauth_status()

    def auth_sign_up(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Registers new user account."""
        return AuthEngine.sign_up(data.get("email", ""), data.get("password", ""), data.get("full_name", ""))

    def auth_sign_out(self) -> Dict[str, Any]:
        """Signs out and clears active session."""
        return AuthEngine.sign_out()

    def auth_get_session(self) -> Dict[str, Any]:
        """Retrieves active session if logged in."""
        return AuthEngine.get_session()

    def auth_get_config(self) -> Dict[str, Any]:
        """Retrieves Supabase URL and keys (with masked secret key)."""
        return AuthEngine.get_safe_config()

    def auth_save_config(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Saves custom Supabase URL and keys."""
        return AuthEngine.save_config(
            url=data.get("supabase_url", ""),
            anon_key=data.get("anon_key", ""),
            secret_key=data.get("service_secret_key", "")
        )

    def auth_refresh_token(self, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Refreshes expired access token."""
        refresh_token = ""
        if data and isinstance(data, dict):
            refresh_token = data.get("refresh_token", "")
        if not refresh_token:
            session = AuthEngine.get_session()
            refresh_token = session.get("refresh_token", "")
        return AuthEngine.refresh_token(refresh_token)

    def auth_update_profile(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Updates user profile information (full_name, bio, avatar_url)."""
        data = data or {}
        return AuthEngine.update_profile(
            full_name=data.get("full_name", ""),
            bio=data.get("bio", ""),
            avatar_url=data.get("avatar_url", "")
        )

    def auth_get_user_stats(self) -> Dict[str, Any]:
        """Calculates user skill engagement statistics and portfolio items."""
        skills = SkillStorage.get_all_skills(getattr(self, "active_workspace", None))
        installed = [s for s in skills if s.installed_targets]
        favorites = [s for s in skills if s.is_favorite]

        from .cloud_client import CloudClient, CloudError
        cloud_profile = {}
        cloud_available = False
        try:
            token = AuthEngine.get_access_token(required=False)
            if token:
                cloud_profile = CloudClient(token=token).rpc('get_my_cloud_profile') or {}
                cloud_available = True
        except CloudError:
            pass
        return {'success': True, 'status': 'success' if cloud_available else 'partial',
                'cloud_available': cloud_available, 'total_skills': len(skills), 'installed_count': len(installed),
                'favorites_count': len(favorites), 'contributed_count': cloud_profile.get('contributed_count', 0),
                'installed_skills': [{'id': s.id, 'title': s.display_title, 'category': s.category} for s in installed[:6]],
                'favorite_skills': [{'id': s.id, 'title': s.display_title, 'category': s.category} for s in favorites[:6]],
                'contributed_skills': []}

    # =========================================================================
    # Auto-Update Engine (v7.2 Dual-Layer Skills & Application Updates)
    # =========================================================================
    def updater_check(self, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Checks for application releases and skills library updates."""
        custom_repo = data.get("repo") if (data and isinstance(data, dict)) else None
        return UpdateEngine.check_for_updates(custom_repo=custom_repo)

    def updater_sync_skills(self) -> Dict[str, Any]:
        """Pulls and synchronizes latest skills from Addy Osmani repository."""
        return UpdateEngine.sync_skills_library()

    def updater_get_info(self) -> Dict[str, Any]:
        """Returns local version metadata and changelog."""
        return UpdateEngine.get_version_info()

    def updater_download_and_apply(self, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Downloads latest setup installer and executes safe in-place upgrade."""
        data = data or {}
        return UpdateEngine.download_and_apply_update(download_url=data.get("download_url"))

    def updater_get_progress(self) -> Dict[str, Any]:
        """Returns live download and installation progress for auto-updater."""
        return UpdateEngine.get_download_progress()

    # =========================================================================
    # Live Verification & Explorer Proof Engine (v1.1)
    # =========================================================================
    def open_skill_folder(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Opens Windows Explorer directly at the installed skill folder on disk.
        Provides undeniable physical proof that the skill exists on the machine.
        """
        skill_id = data.get("skill_id", "")
        target = data.get("target", "antigravity")
        try:
            workspace = data.get('workspace_path') or self.active_workspace
            paths = SkillInstaller.target_dirs(skill_id, workspace)
            if target not in paths or not paths[target].is_dir():
                return {'success': False, 'status': 'error', 'message': 'Không có thư mục cài đặt ở môi trường đã chọn.'}
            return self.open_folder(str(paths[target]))
        except (ValueError, OSError) as error:
            return {'success': False, 'status': 'error', 'message': str(error)}

    def verify_skill_active(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Performs deep verification of skill presence on disk across all AI tools
        and returns verifiable test prompts for the end-user.
        """
        skill_id = data.get("skill_id", "")
        skill = SkillStorage.get_skill(skill_id, data.get("workspace_path") or self.active_workspace)
        if not skill:
            return {"success": False, "message": f"Không tìm thấy kỹ năng '{skill_id}'"}

        workspace = data.get('workspace_path') or self.active_workspace
        verified_targets = []
        for target, directory in SkillInstaller.target_dirs(skill_id, workspace).items():
            if (directory / 'SKILL.md').is_file():
                verified_targets.append({'target': target, 'label': target, 'path': str(directory),
                                         'skill_file': str(directory / 'SKILL.md'), 'status': 'files_present'})
        rules_found = []

        # Generate starter test prompt based on skill capabilities
        starter_prompt = "Hãy giải thích cách kỹ năng này hoạt động và lập kế hoạch mẫu cho tôi."
        if skill.starter_prompts and len(skill.starter_prompts) > 0:
            starter_prompt = skill.starter_prompts[0].get("prompt", starter_prompt)
        elif "strict-architect" in skill_id:
            starter_prompt = "Hãy lập kế hoạch tạo chức năng đăng nhập cho người dùng /plan"
        elif "ui-ux" in skill_id:
            starter_prompt = "Hãy thiết kế bảng điều khiển Dashboard tuân thủ quy tắc DESIGN.md"
        elif "nextjs" in skill_id:
            starter_prompt = "Hãy tạo Server Action tải dữ liệu song song không gây giật lag"
        elif "playwright" in skill_id:
            starter_prompt = "Hãy viết kịch bản test Playwright kiểm tra nút bấm đăng ký"

        expected_behavior = (
            "AI sẽ bắt đầu câu trả lời bằng bảng phân tích chuyên sâu, tuân thủ nguyên tắc không code đại trà, "
            "hoặc khai báo chế độ làm việc chuẩn [MODE: DISCOVERY] / [MODE: BLUEPRINT]."
        )

        return {
            "success": True,
            "skill_id": skill_id,
            "skill_name": skill.display_title or skill.name,
            "is_installed": len(verified_targets) > 0,
            "verified_targets": verified_targets,
            "active_rules": rules_found,
            "test_prompt": starter_prompt,
            "expected_behavior": expected_behavior,
            "installed_count": len(verified_targets)
        }

    # ==========================================
    # Phase 3: Diagnostic & Health Logging
    # ==========================================
    def get_diagnostic_logs(self, line_count: int = 150) -> Dict[str, Any]:
        """Returns the recent log entries and system health summary."""
        logs = get_recent_logs(line_count)
        log_dir = get_log_dir()
        return {
            "success": True,
            "logs": logs,
            "log_dir": str(log_dir),
            "platform": sys.platform,
            "python_version": sys.version.split()[0],
            "active_workspace": self.active_workspace,
            "frozen": getattr(sys, "frozen", False)
        }

    def export_diagnostic_logs(self) -> Dict[str, Any]:
        """Exports a zipped bundle of diagnostic logs and environment telemetry."""
        logger = get_logger()
        logger.info(f"User requested diagnostic log export from workspace: {self.active_workspace}")
        return export_diagnostic_zip()

    def open_logs_folder(self) -> Dict[str, Any]:
        """Opens the %LOCALAPPDATA%/AbyssalSkillsD/logs folder in Windows Explorer."""
        log_dir = get_log_dir()
        try:
            if sys.platform == "win32":
                os.startfile(str(log_dir))
            else:
                subprocess.run(["xdg-open", str(log_dir)])
            return {"success": True, "path": str(log_dir)}
        except Exception as e:
            return {"success": False, "message": str(e)}

    # ==========================================
    # Phase 3: Community Cloud Hub (Live Sharing & Install)
    # ==========================================
    def _get_community_file(self) -> Path:
        from app.backend.paths import get_data_dir
        return get_data_dir() / "community_skills.json"

    def community_get_skills(self, data=None):
        from .community import CommunityService
        data = data or {}
        return CommunityService.list_skills(data.get('query', ''), data.get('category', ''), data.get('page', 0))

    def community_publish_skill(self, skill_data):
        from .community import CommunityService
        return CommunityService.publish(skill_data)

    def community_install_skill(self, data):
        from .community import CommunityService
        return CommunityService.install(data, self.active_workspace)

    def community_action(self, data):
        from .community import CommunityService
        return CommunityService.action(data.get('action'), data.get('payload') or {})

    def community_get_skill(self, skill_id):
        from .community import CommunityService
        from .cloud_client import CloudError, failure
        try:
            return {'success': True, 'status': 'success', 'skill': CommunityService.get_skill(skill_id)}
        except (CloudError, ValueError, OSError) as error:
            return failure(error)

    def get_pending_diagnostic(self):
        from .telemetry import TelemetryService
        return TelemetryService.pending()

    def prepare_diagnostic(self, payload):
        from .telemetry import TelemetryService
        return TelemetryService.prepare(payload)

    def report_system_error(self, payload):
        from .telemetry import TelemetryService
        return TelemetryService.send(payload.get('request_id'))

    def discard_diagnostic(self):
        from .telemetry import TelemetryService
        return TelemetryService.discard()

    def auth_cancel_oauth(self):
        from .auth import OAuthServerManager
        OAuthServerManager.stop_server()
        return {'success': True, 'status': 'cancelled', 'message': 'Đã hủy đăng nhập.'}
