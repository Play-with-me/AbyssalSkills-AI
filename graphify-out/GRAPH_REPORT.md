# Graph Report - Manager Skills  (2026-11-12)

## Corpus Check
- 43 files · ~407,801 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 11 file(s) not represented in the graph (top: .ico 3, (none) 1, .lnk 1)

## Summary
- 601 nodes · 1446 edges · 24 communities (9 shown, 15 thin omitted)
- Extraction: 95% EXTRACTED · 5% INFERRED · 0% AMBIGUOUS · INFERRED: 73 edges (avg confidence: 0.94)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `a4f798ac`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- api.py
- SkillItem
- abyssalskillsd
- with
- Nghiệm thu AbyssalSkillsD 1.1.0
- SkillForge AI Design System (`DESIGN.md`)
- ReliabilityTests
- DesktopAPI
- DesktopBridge
- SkillInstaller
- UIComponents
- install.sh script
- SecureStorage
- app.js
- CloudError
- UpdateEngine

## God Nodes (most connected - your core abstractions)
1. `DesktopAPI` - 79 edges
2. `DesktopBridge` - 59 edges
3. `SkillInstaller` - 40 edges
4. `UIComponents` - 37 edges
5. `ReliabilityTests` - 37 edges
6. `SkillItem` - 36 edges
7. `CloudError` - 34 edges
8. `AuthEngine` - 32 edges
9. `SkillScanner` - 26 edges
10. `CloudClient` - 25 edges

## Surprising Connections (you probably didn't know these)
- `ReliabilityTests` --uses--> `DesktopAPI`  [INFERRED]
  tests/test_reliability.py → app/backend/api.py
- `ReliabilityTests` --uses--> `GitSyncEngine`  [INFERRED]
  tests/test_reliability.py → app/backend/git_sync.py
- `ReliabilityTests` --uses--> `SkillInstaller`  [INFERRED]
  tests/test_reliability.py → app/backend/installer.py
- `ServiceTests` --uses--> `SkillInstaller`  [INFERRED]
  tests/test_services.py → app/backend/installer.py
- `ReliabilityTests` --uses--> `SkillItem`  [INFERRED]
  tests/test_reliability.py → app/backend/models.py

## Import Cycles
- None detected.

## Communities (24 total, 15 thin omitted)

### Community 0 - "api.py"
Cohesion: 0.05
Nodes (20): GitSyncEngine, export_diagnostic_zip(), get_logger(), get_recent_logs(), init_logger(), sanitize_sensitive_data(), atomic_write(), get_app_icon() (+12 more)

### Community 1 - "SkillItem"
Cohesion: 0.19
Nodes (3): SkillItem, serialized(), SkillStorage

### Community 3 - "with"
Cohesion: 0.06
Nodes (30): env, PYTHONIOENCODING, PYTHONUTF8, jobs, windows, name, on, pull_request (+22 more)

### Community 4 - "Nghiệm thu AbyssalSkillsD 1.1.0"
Cohesion: 0.13
Nodes (13): Bằng chứng đã chạy, Còn thiếu để hoàn tất kế hoạch, Kiểm tra thủ công, Nghiệm thu AbyssalSkillsD 1.1.0, Đối chiếu phát hiện kiểm toán, AbyssalSkillsD, Core Features, Development & Verification (+5 more)

### Community 5 - "SkillForge AI Design System (`DESIGN.md`)"
Cohesion: 0.12
Nodes (15): 1. Brand Essence & Aesthetic Philosophy, 2. Geometric Logo & Background Blueprint Specification (Abyssal Sky v4.0), 3. Dual-Theme Palette & Semantic Tokens, 4. Typography, 5. Interactive Component Protocols, A. Command Palette (`Ctrl+K` / `Cmd+K`), A. Dark Mode Tokens (Abyssal Void — Default), A. The 4-Shape Complexity Budget (`ip-as-logo` & `C:\Logo\DESIGN.md`) (+7 more)

### Community 6 - "ReliabilityTests"
Cohesion: 0.06
Nodes (8): InstallRequest, InstallResult, ReferenceDoc, RuleDoc, SkillFileDoc, SkillScanner, _scan_folder_recursive(), ReliabilityTests

### Community 12 - "SkillInstaller"
Cohesion: 0.11
Nodes (3): SkillInstaller, assert_safe_workspace_path(), safe_child()

### Community 13 - "UIComponents"
Cohesion: 0.08
Nodes (7): 1. Product Summary & Active UX/Brand Rules, 2. Architecture & Figma Reference Canvas, 3. Recent Completed Changes, PROJECT MEMORY — `AbyssalSkillsD` Desktop App Suite & Figma Workspace, Icons, MarkdownRenderer, UIComponents

### Community 22 - "CloudError"
Cohesion: 0.05
Nodes (11): AuthEngine, OAuthCallbackHandler, OAuthServerManager, CloudClient, CloudError, failure(), NoCloudRedirect, CommunityService (+3 more)

## Knowledge Gaps
- **1 isolated node(s):** `abyssalskillsd`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 213 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **15 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `DesktopAPI` connect `DesktopAPI` to `api.py`, `SkillItem`, `ReliabilityTests`, `.auth_check_oauth_status`, `.get_skills`, `.install_all_skills`, `SkillInstaller`, `.scan_skill_directory`, `.open_skill_folder`, `CloudError`, `UpdateEngine`, `.delete_skill`?**
  _High betweenness centrality (0.194) - this node is a cross-community bridge._
- **Are the 14 inferred relationships involving `DesktopAPI` (e.g. with `AuthEngine` and `OAuthServerManager`) actually correct?**
  _`DesktopAPI` has 14 INFERRED edges - model-reasoned connections that need verification._
- **What connects `abyssalskillsd` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `api.py` be split into smaller, more focused modules?**
  _Cohesion score 0.05339805825242718 - nodes in this community are weakly interconnected._
- **Why does `SkillInstaller` connect `SkillInstaller` to `api.py`, `SkillItem`, `ReliabilityTests`, `DesktopAPI`, `CloudError`, `UpdateEngine`?**
  _High betweenness centrality (0.054) - this node is a cross-community bridge._
- **Are the 10 inferred relationships involving `SkillInstaller` (e.g. with `DesktopAPI` and `CommunityService`) actually correct?**
  _`SkillInstaller` has 10 INFERRED edges - model-reasoned connections that need verification._
- **Should `with` be split into smaller, more focused modules?**
  _Cohesion score 0.06451612903225806 - nodes in this community are weakly interconnected._