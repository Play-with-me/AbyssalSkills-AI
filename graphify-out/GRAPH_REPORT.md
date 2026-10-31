# Graph Report - Manager Skills  (2026-10-31)

## Corpus Check
- 30 files · ~403,208 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 11 file(s) not represented in the graph (top: .ico 3, (none) 1, .lnk 1)

## Summary
- 496 nodes · 1049 edges · 24 communities (8 shown, 16 thin omitted)
- Extraction: 96% EXTRACTED · 4% INFERRED · 0% AMBIGUOUS · INFERRED: 44 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a2b4c695`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- api.py
- SkillItem
- abyssalskillsd
- with
- README.vi.md
- SkillForge AI Design System (`DESIGN.md`)
- SkillStorage
- UpdateEngine
- DesktopBridge
- README.md
- OAuthCallbackHandler
- UIComponents
- install.sh script
- app.js
- AuthEngine
- DesktopAPI

## God Nodes (most connected - your core abstractions)
1. `DesktopAPI` - 60 edges
2. `DesktopBridge` - 49 edges
3. `SkillItem` - 36 edges
4. `UIComponents` - 34 edges
5. `test_all()` - 30 edges
6. `SkillScanner` - 24 edges
7. `SkillInstaller` - 23 edges
8. `AuthEngine` - 21 edges
9. `SkillStorage` - 19 edges
10. `get_logger()` - 18 edges

## Surprising Connections (you probably didn't know these)
- `2. Architecture & God Nodes (Graphify AST Audit)` --references--> `DesktopAPI`  [INFERRED]
  .agents/PROJECT_MEMORY.md → app/backend/api.py
- `2. Architecture & God Nodes (Graphify AST Audit)` --references--> `SkillInstaller`  [INFERRED]
  .agents/PROJECT_MEMORY.md → app/backend/installer.py
- `3. Recent Completed Changes` --references--> `sanitize_sensitive_data()`  [INFERRED]
  .agents/PROJECT_MEMORY.md → app/backend/logger.py
- `3. Recent Completed Changes` --references--> `assert_safe_workspace_path()`  [INFERRED]
  .agents/PROJECT_MEMORY.md → app/backend/paths.py
- `2. Architecture & God Nodes (Graphify AST Audit)` --references--> `SkillStorage`  [INFERRED]
  .agents/PROJECT_MEMORY.md → app/backend/storage.py

## Import Cycles
- None detected.

## Communities (24 total, 16 thin omitted)

### Community 0 - "api.py"
Cohesion: 0.06
Nodes (18): GitSyncEngine, export_diagnostic_zip(), get_recent_logs(), init_logger(), sanitize_sensitive_data(), InstallResult, ReferenceDoc, RuleDoc (+10 more)

### Community 1 - "SkillItem"
Cohesion: 0.15
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
Cohesion: 0.08
Nodes (7): 1. Product Summary & Active UX Rules, 2. Architecture & God Nodes (Graphify AST Audit), 3. Recent Completed Changes, AbyssalSkillsD — Project Memory Anchor (`.agents/PROJECT_MEMORY.md`), Icons, MarkdownRenderer, UIComponents

### Community 22 - "AuthEngine"
Cohesion: 0.10
Nodes (6): _push_cloud(), AuthEngine, OAuthServerManager, _timeout(), get_logger(), test_all()

## Knowledge Gaps
- **1 isolated node(s):** `abyssalskillsd`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 208 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **16 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DesktopAPI` connect `DesktopAPI` to `api.py`, `SkillItem`, `.sync_all_ais`, `SkillStorage`, `UpdateEngine`, `.community_get_skills`, `UIComponents`, `.delete_skill`, `.import_from_github`, `AuthEngine`, `.get_skill`, `.install_skill`?**
  _High betweenness centrality (0.247) - this node is a cross-community bridge._
- **Are the 9 inferred relationships involving `DesktopAPI` (e.g. with `2. Architecture & God Nodes (Graphify AST Audit)` and `AuthEngine`) actually correct?**
  _`DesktopAPI` has 9 INFERRED edges - model-reasoned connections that need verification._
- **What connects `abyssalskillsd` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `api.py` be split into smaller, more focused modules?**
  _Cohesion score 0.056679151061173536 - nodes in this community are weakly interconnected._
- **Why does `2. Architecture & God Nodes (Graphify AST Audit)` connect `UIComponents` to `SkillItem`, `SkillStorage`, `UpdateEngine`, `DesktopBridge`, `DesktopAPI`?**
  _High betweenness centrality (0.220) - this node is a cross-community bridge._
- **Are the 5 inferred relationships involving `SkillItem` (e.g. with `DesktopAPI` and `GitSyncEngine`) actually correct?**
  _`SkillItem` has 5 INFERRED edges - model-reasoned connections that need verification._
- **Should `SkillItem` be split into smaller, more focused modules?**
  _Cohesion score 0.14942528735632185 - nodes in this community are weakly interconnected._