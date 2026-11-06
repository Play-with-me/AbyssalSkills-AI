# AbyssalSkillsD — Living Project Memory (`.agents/PROJECT_MEMORY.md`)

## 1. Product Summary & Active UX Rules
- **Product:** AbyssalSkillsD (v1.1.2) — Standalone Windows Desktop App for AI Skill Management & Marketplace.
- **Brand Identity:** Abyssal Sky v2.0 (`#050C1A` Void, `#00B4D8` Ocean Cyan, `#7C3AED` Aurora Violet, `#1E2D4A` Hairline).
- **External Asset Integrity Law:** `C:\Logo` remains 100% read-only and untouched.
- **UI/UX Guardrails:** Anti-overflow CSS (`min-h-0`, `min-w-0`), sub-250ms physics motion, zero blind actions, uncluttered headers, and collapsible guidance hubs.
- **Universal Multi-AI Ecosystem (7 Environments):** Google Antigravity, Claude Code, Cursor AI, Windsurf, GitHub Copilot, OpenAI Codex, and Aider/Workspace.
- **Aggregated Suites:** 36 Skills (7 Skill-AI Nucleus + 29 Addy Osmani Production Engineering).

## 2. Architecture & God Nodes (Graphify AST Audit)
- `RuntimePathResolver` (`app/backend/paths.py`): Frozen PyInstaller vs. dev mode path resolution with APPDATA fallback.
- `UpdateEngine` (`app/backend/updater.py`): GitHub Releases API, SemVer comparison, and in-place silent auto-updater.
- `DesktopAPI` (`app/backend/api.py`): JS-to-Python IPC bridge (34 methods).
- `SkillStorage` (`app/backend/storage.py`): Registry persistence, fast-path YAML hashing, and backup snapshot manager.
- `SkillInstaller` (`app/backend/installer.py`): Multi-target atomic file deployment engine.
- `DesktopBridge` (`app/frontend/js/bridge.js`): Frontend asynchronous bridge.
- `UIComponents` (`app/frontend/js/components.js`): Executive header, bento cards, community marketplace, and diff viewer.
- `App` (`app/frontend/js/app.js`): View state, filtering, auto-update progress listener, and workspace router.

## 3. Recent Completed Changes (v1.1.2)
- [x] **UI Decluttering & Header Streamlining:**
  - Collapsed 3-card `hero-action-hub` by default into `[✨ Mở Gợi Ý Nhanh]`, increasing visible card area by 40%.
  - Replaced 7 static non-clickable sidebar rows with sleek `.sidebar-ai-health-card` ("7 Nền Tảng AI Sẵn Sàng").
- [x] **Workspace Isolation (Toolbar Leakage Fix):**
  - Isolated `#catalog-unified-toolbar` and `#workspace-project-bar` to `library` and `installed` views only, permanently eliminating unwanted toolbars from leaking into Community Cloud, Studio, and Guide.
- [x] **Card Ergonomics & Anti-Squish Refactoring:**
  - Bento skill cards streamlined to 2 primary actions (`[⚡ Lấy Lệnh Nhanh]` / `[🔄 Cập Nhật]` + `[⚙️ Chi Tiết ▾]`) and compact icon tool for Studio.
  - Community Cloud cards refactored with clean top icon tools and wide 2-tier buttons, preventing button clipping.
- [x] **Intelligent Diff Modal (0-Diff Clean State):**
  - When differences are 0, confusing bulk selectors and "Áp dụng (0 khối)" buttons are replaced by a clean `[✓ Đã Khớp 100% — Đóng Hộp Thoại]` completion badge.
- [x] **Verification & Release:**
  - Verified 100% passing across all 34 automated unit & service tests (`Ran 34 tests in 2.094s, OK`).
  - Bumped version to `1.1.2`, synced files to installed desktop directory, and pushed release tag `v1.1.2` to GitHub.
