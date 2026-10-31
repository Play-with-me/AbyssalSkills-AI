# Graph Report - Manager Skills  (2026-10-31)

## Corpus Check
- 30 files · ~399,233 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 11 file(s) not represented in the graph (top: .ico 3, (none) 1, .lnk 1)

## Summary
- 463 nodes · 961 edges · 22 communities (9 shown, 13 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 41 edges (avg confidence: 0.95)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `273db996`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- api.py
- SkillItem
- abyssalskillsd
- with
- README.vi.md
- SkillForge AI Design System (`DESIGN.md`)
- DesktopBridge
- README.md
- UIComponents
- install.sh script
- app.js
- AuthEngine
- DesktopAPI
- test_all
- logger.py

## God Nodes (most connected - your core abstractions)
1. `DesktopAPI` - 57 edges
2. `DesktopBridge` - 46 edges
3. `SkillItem` - 36 edges
4. `UIComponents` - 33 edges
5. `SkillScanner` - 24 edges
6. `SkillInstaller` - 23 edges
7. `SkillStorage` - 19 edges
8. `test_all()` - 18 edges
9. `AuthEngine` - 15 edges
10. `UpdateEngine` - 14 edges

## Surprising Connections (you probably didn't know these)
- `2. Architecture & God Nodes (Graphify AST Audit)` --references--> `DesktopAPI`  [INFERRED]
  .agents/PROJECT_MEMORY.md → app/backend/api.py
- `2. Architecture & God Nodes (Graphify AST Audit)` --references--> `SkillInstaller`  [INFERRED]
  .agents/PROJECT_MEMORY.md → app/backend/installer.py
- `3. Recent Completed Changes` --references--> `sanitize_sensitive_data()`  [INFERRED]
  .agents/PROJECT_MEMORY.md → app/backend/logger.py
- `3. Recent Completed Changes` --references--> `assert_safe_workspace_path()`  [INFERRED]
  .agents/PROJECT_MEMORY.md → app/backend/paths.py
- `2. Architecture & God Nodes (Graphify AST Audit)` --references--> `DesktopBridge`  [INFERRED]
  .agents/PROJECT_MEMORY.md → app/frontend/js/bridge.js

## Import Cycles
- None detected.

## Communities (22 total, 13 thin omitted)

### Community 0 - "api.py"
Cohesion: 0.08
Nodes (7): GitSyncEngine, InstallResult, ReferenceDoc, RuleDoc, SkillScanner, get_file_sha256(), main()

### Community 1 - "SkillItem"
Cohesion: 0.16
Nodes (3): SkillInstaller, InstallRequest, SkillItem

### Community 3 - "with"
Cohesion: 0.06
Nodes (43): name, runs-on, steps, name, runs-on, steps, name, runs-on (+35 more)

### Community 4 - "README.vi.md"
Cohesion: 0.09
Nodes (22): 1. Kích Hoạt Nhanh Thông Minh & Trình So Sánh Diff Trực Quan, 🖥️ 1. Windows (Lệnh PowerShell hoặc File Cài Đặt), 2. Ma Trận Tương Thích Đa Nền Tảng (Universal Multi-Target Matrix), 🍎 2. macOS (Apple Silicon M-Series & Intel), 3. Kết Nối Đám Mây Supabase Cloud & Zero-Trust Telemetry, 🐧 3. Linux (Ubuntu, Debian, Fedora, Arch), 🛠️ 4. Chạy Từ Mã Nguồn (Dành Cho Lập Trình Viên Đa Hệ), 📄 BẢN QUYỀN & GIẤY PHÉP (LICENSE & CREDITS) (+14 more)

### Community 5 - "SkillForge AI Design System (`DESIGN.md`)"
Cohesion: 0.12
Nodes (15): 1. Brand Essence & Aesthetic Philosophy, 2. Geometric Logo & Background Blueprint Specification (Abyssal Sky v4.0), 3. Dual-Theme Palette & Semantic Tokens, 4. Typography, 5. Interactive Component Protocols, A. Command Palette (`Ctrl+K` / `Cmd+K`), A. Dark Mode Tokens (Abyssal Void — Default), A. The 4-Shape Complexity Budget (`ip-as-logo` & `C:\Logo\DESIGN.md`) (+7 more)

### Community 9 - "README.md"
Cohesion: 0.09
Nodes (22): 1. Smart 2-Flow Activation & Interactive Side-by-Side Diff, 🖥️ 1. Windows (PowerShell or 1-Click GUI), 🍎 2. macOS (Apple Silicon M-Series & Intel), 2. Universal Multi-Target Matrix, 🐧 3. Linux (Ubuntu, Debian, Fedora, Arch), 3. Supabase Cloud Backend & Zero-Trust Telemetry, 🛠️ 4. Run from Source (Cross-Platform Developer Mode), 🧪 AUTOMATED VERIFICATION SUITE (25 QUALITY GATES) (+14 more)

### Community 13 - "UIComponents"
Cohesion: 0.09
Nodes (6): 1. Product Summary & Active UX Rules, 3. Recent Completed Changes, AbyssalSkillsD — Project Memory Anchor (`.agents/PROJECT_MEMORY.md`), Icons, MarkdownRenderer, UIComponents

### Community 208 - "test_all"
Cohesion: 0.15
Nodes (4): 2. Architecture & God Nodes (Graphify AST Audit), SkillStorage, UpdateEngine, test_all()

### Community 350 - "logger.py"
Cohesion: 0.07
Nodes (13): _push_cloud(), export_diagnostic_zip(), get_logger(), get_recent_logs(), init_logger(), sanitize_sensitive_data(), assert_safe_workspace_path(), get_app_icon() (+5 more)

## Knowledge Gaps
- **1 isolated node(s):** `abyssalskillsd`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 192 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **13 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DesktopAPI` connect `DesktopAPI` to `api.py`, `SkillItem`, `.install_all_skills`, `.get_skill`, `.updater_check`, `.updater_get_info`, `.updater_sync_skills`, `test_all`, `AuthEngine`, `.install_skill`, `logger.py`?**
  _High betweenness centrality (0.248) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DesktopAPI` (e.g. with `2. Architecture & God Nodes (Graphify AST Audit)` and `AuthEngine`) actually correct?**
  _`DesktopAPI` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `abyssalskillsd` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `api.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07629288274449565 - nodes in this community are weakly interconnected._
- **Why does `2. Architecture & God Nodes (Graphify AST Audit)` connect `test_all` to `DesktopBridge`, `SkillItem`, `UIComponents`, `DesktopAPI`?**
  _High betweenness centrality (0.218) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `SkillItem` (e.g. with `DesktopAPI` and `GitSyncEngine`) actually correct?**
  _`SkillItem` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Should `with` be split into smaller, more focused modules?**
  _Cohesion score 0.05708245243128964 - nodes in this community are weakly interconnected._