# PROJECT MEMORY — `AbyssalSkillsD` Desktop App Suite & Figma Workspace

## 1. Product Summary & Active UX/Brand Rules
- **Product Name**: `AbyssalSkillsD` (AI Skill Manager Workbench for Windows 10/11 x64, PyWebView).
- **Author**: Lâm Nhựt Hải Đăng (Kyuu449977).
- **Core Archetype**: Linear / Raycast / Cursor Desktop Precision Workbench.
- **Design Tokens & Theme**:
  - Obsidian Deep Dark Theme (`#050C1A` canvas, `#0A1428` surface, `#0D1933` cards/inputs, `#1E2D4A` borders).
  - Aurora Accents: Electric Ocean Cyan (`#00B4D8`), Celestial Violet (`#7C3AED` -> `#A78BFA`), Emerald Health (`#10B981`).
  - Zero-Emoji Policy: 100% Vector SVG iconography (1.5px/2px uniform stroke).
  - 118 Anti-Slop Rules & Sub-250ms physics motion (`cubic-bezier(0.16, 1, 0.3, 1)`).

## 2. Architecture & Figma Reference Canvas
- **Active Figma File URL**: `https://www.figma.com/design/NRBE8zh5RbhSob8pKHIKC7/Untitled`
- **Figma File Key**: `NRBE8zh5RbhSob8pKHIKC7`
- **Production Desktop Design**: Frame `11:2` (`AbyssalSkillsD · Quản lý Kỹ năng & AI`, `1440 × 900` px):
  1. **Topbar Header (`11:3`)**: Clean brand badge `v1.1.5`, Search Command input (`⌘ K`), View toggles, Notifications, Tools menu.
  2. **Activity Sidebar (`11:53`)**:
     - Dedicated Workspace box (`#workspace-project-bar`) moved to sidebar top with path preview and `#btn-change-workspace`.
     - 6 primary navigation destinations.
     - Vertical AI Ecosystem Health list (`11:93`) with status LED dots for all 7 platforms.
     - Help & shortcuts trigger (`11:110`, `⌘ ?`).
  3. **Center Catalog (`11:125`)**:
     - Breadcrumb navigation (`KHÔNG GIAN LÀM VIỆC / Thư viện kỹ năng`), main title `Kho Kỹ Năng`, count badge `36 kỹ năng`.
     - Needs filter chips (`Tất cả`, `Lập trình & Clean Code`, `Frontend & Giao diện`, `Kiểm thử & QA`).
     - Source tabs with active indicator and visible counter (`6 / 36 kỹ năng`).
     - Redesigned Bento Cards (`11:156`): Category label, title, version tag, LED dot, 2-line description, 3 tags (`# ...`), "Chi tiết" outline button, "Đồng bộ vào AI" gradient button.
     - Pagination Bar (`11:303`): `1, 2, 3 >`.
  4. **Inspector Drawer (`11:6`)**:
     - Header: Skill title, version badges (`● Đã cài vX.Y.Z` and `vX.Y.Z có sẵn`), close button.
     - 3 Horizontal Tabs: `Tổng quan` (`data-doc="guide"`), `So sánh Diff` (`data-doc="diff"`), `Quy tắc` (`data-doc="skill_md"`).
     - Side-by-side 2-column Diff viewer table with `+6 -2` metrics, code highlights, and safety summary card.
     - Pinned Action Footer: "Gỡ cài đặt" and "Áp dụng vào Dự án →".
  5. **Bottom Statusbar (`11:7`)**: Left system LED status, center last synced timestamp, right version `v1.1.5`.

## 3. Recent Completed Changes
- Successfully implemented 100% of the Figma Desktop Screen `11:2` design into the frontend (`index.html`, `js/components.js`, `css/app.css`, `js/app.js`).
- Preserved all project management actions in the Topbar Tools dropdown for complete accessibility and test safety.
- Retained all platform toggle switches inside a collapsible platform accordion in the Inspector drawer.
- Verified: All 39/39 automated reliability and backend unit tests pass without regressions (`OK (skipped=1)`).
- Hotfix & Polish (v1.1.6):
  1. **Sidebar Layout & Alignment**: Fixed `#workspace-project-bar` top and main rows (folder icon + label grouped on left, path + `[Đổi]` neatly aligned on one row). Fixed `.ai-platform-row` alignment across all 7 AI platforms (`Antigravity`, `Claude Code`, `Cursor AI`, `Windsurf`, `GitHub Copilot`, `OpenAI Codex`, `Workspace`) using `.platform-info` wrappers and clean right-aligned status badges.
  2. **Help & Shortcuts**: Wired up `#btn-sidebar-help` click, Enter/Space, and keyboard shortcuts (`Ctrl + /` or `?`) to open a rich modal featuring a complete Keyboard Shortcuts reference table (`Ctrl+K`, `Ctrl+/`, `Esc`, `↑/↓/Enter`).
  3. **Skill Activation Confirmation Modal (Zero Blind Actions)**: Routed single and batch activations (`handleApplyInstall`, `handleBatchInstallAll`, quick tryouts, topbar tools) through `UIComponents.renderActivationConfirmModal`. Displays target workspace, selectable/deselectable skills list with live counters, target AI platform checklist, and only proceeds to write files upon explicit user click of `[⚡ Xác Nhận Kích Hoạt Ngay]`.
  4. **Workspace Visibility Safety**: Preserved `#workspace-project-bar` in the persistent sidebar across all views (`library`, `installed`, `guide`, `studio`, `community`, `profile`), and correctly toggles `#catalog-header-area` and `#catalog-pagination-bar`.
  5. Verified runtime execution with PyWebView headless evaluation: 0 errors, 100% modal/button bindings passing.
  6. **Graphify Sync (v0.9.107 Upgrade)**: Upgraded CLI to `graphifyy v0.9.107` via uv tool. Updated `C:\Users\kyuu4\.gemini\config\skills\graphify\SKILL.md` (820 lines) and downloaded the complete set of 8 reference guides into `references/` (`query.md`, `update.md`, `extraction-spec.md`, `github-and-merge.md`, `add-watch.md`, `exports.md`, `hooks.md`, `transcribe.md`). Mirrored updated skill to `.agents/skills/graphify`, `.cursor/skills/graphify`, `.codeium/windsurf/skills/graphify`. Updated `graphify-knowledge-graph.md` playbooks in `strict-architect-coder` and `ui-ux-design-master`. Rebuilt project knowledge graph (601 nodes, 1446 edges, 24 communities) and verified instant BFS/DFS graph queries.
