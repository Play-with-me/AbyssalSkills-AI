# AbyssalSkillsD — Living Project Memory (`.agents/PROJECT_MEMORY.md`)

## 1. Product Summary & Active UX Rules
- **Product:** AbyssalSkillsD (v1.1.4) — Standalone Windows Desktop App for AI Skill Management & Marketplace.
- **Brand Identity:** Abyssal Sky v2.0 (`#050814` Void, `#00B4D8` Ocean Cyan, `#7C3AED` Aurora Violet, `#1E2D4A` Hairline).
- **Background Aesthetic Law:** Luxury Studio Atmospheric Canvas. Zero fake sci-fi blueprint rings, zero crosshairs, zero giant watermarks.
- **UI/UX Guardrails:** Anti-overflow CSS (`min-h-0`, `min-w-0`), sub-250ms physics motion, zero blind actions, uncluttered headers, and collapsible guidance hubs.
- **Universal Multi-AI Ecosystem (7 Environments):** Google Antigravity, Claude Code, Cursor AI, Windsurf, GitHub Copilot, OpenAI Codex, and Aider/Workspace.
- **Aggregated Suites:** 36 Skills (7 Skill-AI Nucleus + 29 Addy Osmani Production Engineering).

## 2. Architecture & God Nodes (Graphify AST Audit)
- `RuntimePathResolver` (`app/backend/paths.py`): Frozen PyInstaller vs. dev mode path resolution with APPDATA fallback.
- `UpdateEngine` (`app/backend/updater.py`): GitHub Releases API, SemVer comparison, and in-place silent auto-updater.
- `DesktopAPI` (`app/backend/api.py`): JS-to-Python IPC bridge (34 methods).
- `SkillStorage` (`app/backend/storage.py`): Registry persistence, fast-path YAML hashing, and backup snapshot manager.
- `SkillInstaller` (`app/backend/installer.py`): Multi-target atomic file deployment engine.
- `DesktopBridge` (`app/frontend/js/bridge.js`): Frontend asynchronous bridge with backward compatibility.
- `UIComponents` (`app/frontend/js/components.js`): Executive header, bento cards, community marketplace, and diff viewer.
- `App` (`app/frontend/js/app.js`): View state, filtering, auto-update progress listener, and workspace router.

## 3. Recent Completed Changes
- [x] **Dynamic GitHub Release & 1-Click Install Script:**
  - `scripts/install.ps1` dynamically detects the latest release via GitHub API with fallback to `/releases/latest/download/AbyssalSkillsD-Setup.exe`. Zero hardcoded version debt.
  - `README.md` and `README.vi.md` upgraded with dynamic Shields.io release badges and permanent latest download links.
- [x] **100% Clean Uninstallation (Modern App Spec):**
  - Added `[UninstallDelete]` and Pascal script `CurUninstallStepChanged(usPostUninstall)` with `DelTree` in `installer/abyssalskillsd.iss`.
  - Automatically wipes `%APPDATA%\AbyssalSkillsD`, `%LOCALAPPDATA%\AbyssalSkillsD`, and `{app}` when uninstalled via Windows Settings or Control Panel.
- [x] **Community Cloud Bridge Backward-Compatibility:**
  - Fixed `DesktopBridge.communityGetSkills()` to handle both 0-arg and 1-arg backend signatures without throwing `DesktopAPI.community_get_skills() takes 1 positional argument but 2 were given`.
  - Fixed `undefined Tải lại` button icon reference (`Icons.refresh`).
- [x] **Luxury Studio Atmospheric Background:**
  - Removed all fake sci-fi blueprint graphics (orbit rings, compass crosshairs, dashed diagonal lines, giant fox watermark).
  - Implemented human-crafted deep obsidian mesh with organic cyan/violet ambient aurora lighting and subtle studio dot matrix (Linear/Raycast aesthetic).
- [x] **Project Tools Dropdown List (Consolidated Actions):**
  - Replaced the 4 horizontal buttons with a single glowing trigger: `[⚡ Thao Tác Dự Án ▾]`.
- [x] **UI Decluttering & Header Streamlining:**
  - Collapsed 3-card `hero-action-hub` by default into `[✨ Mở Gợi Ý Nhanh]`.
  - Replaced 7 static non-clickable sidebar rows with sleek `.sidebar-ai-health-card` ("7 Nền Tảng AI Sẵn Sàng").
- [x] **Workspace Isolation (Toolbar Leakage Fix):**
  - Isolated `#catalog-unified-toolbar` and `#workspace-project-bar` to `library` and `installed` views only.
- [x] **Cleaned Dist Binaries from Git Tracking:**
  - Untracked legacy v1.0.1 binaries from Git index so future GitHub Actions releases only upload new compilation assets.
