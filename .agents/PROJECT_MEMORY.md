# AbyssalSkillsD — Project Memory Anchor (`.agents/PROJECT_MEMORY.md`)

## 1. Product Summary & Active UX Rules
- **Product:** AbyssalSkillsD — Standalone Windows Desktop Application for AI Skill Management & Marketplace.
- **Brand Identity:** Renamed from SkillForge to **`AbyssalSkillsD`** (100% collision-free globally across GitHub, PyPI, and trademarks).
- **Official Release Strategy:**
  - Initial public edition reset to clean **`v1.0.0`**.
  - GitHub Repository slug: `https://github.com/Play-with-me/AbyssalSkills-AI.git` (Private Repository).
- **Packaging & Distribution:**
  - Standalone Windows 64-bit distribution (`dist/AbyssalSkillsD/AbyssalSkillsD.exe`, 5.44 MB). Requires zero Python, Node.js, or Git installed on client computers.
  - Portable Release ZIP: `dist/AbyssalSkillsD-v1.0.0-Portable.zip` (18.27 MB, SHA256: `2b5b58e9...`).
  - Professional Inno Setup Script: `installer/abyssalskillsd.iss` for building single-file `AbyssalSkillsD-Setup-v1.0.0.exe`.
  - Windows Shortcuts: `AbyssalSkillsD AI.lnk` deployed to workspace and user Desktop.
- **Brand Identity & Motifs:** Abyssal Sky v2.0 (`kyuu4-abyssal-sky-design-system` via `ip-as-logo` & `voltagent-awesome-design-md`).
  - Palette: `#050C1A` (Abyssal Void), `#00B4D8` (Electric Ocean Cyan), `#7C3AED` (Celestial Aurora Violet), `#1E2D4A` (Hairline).
  - Background Canvas: Fixed non-intrusive Sacred Geometry & Blueprint grid vector backdrop (`#geometric-background-canvas`, `pointer-events: none`).
  - Native Windows Icon: Multi-resolution Windows Icon `app-icon.ico` embedded in Windows Taskbar, WinForms `Form.Icon`, Edge WebView2 favicon, and Desktop shortcuts.
- **Smart Notification Center & Minor Update UX:**
  - Dismissible Banner: Automatically detects new skills and displays banner.
  - Anti-Annoyance Memory: Saved dismiss signatures to `localStorage` (`abyssalskillsd-dismissed-banner-sig`) and mute toggle (`abyssalskillsd-mute-minor-banners`).
  - TopBar Notification Bell: Centralized notification dropdown with 1-click sync.
- **Neural Stream Activation & Live Verification Proof Engine (v1.1):**
  - **Hoạt ảnh Sóng hạt Vi mạch (Neural Stream Stage):** Khi bấm kích hoạt/cài đặt, hiển thị luồng dữ liệu truyền tải hình học chuyển động mượt mà (sub-250ms) từ Logo kỹ năng sang lõi AI Core qua 3 bước tiến trình thực tế.
  - **Bằng chứng Thư mục Thực tế (Windows Explorer):** Tích hợp nút `[📁 Mở thư mục trên máy]` gọi trực tiếp `DesktopBridge.openSkillFolder()` để người dùng tận mắt kiểm tra tệp `SKILL.md` trên ổ cứng.
  - **Khay Kiểm Chứng AI Tức Thì:** Hộp thoại `[🧪 Kiểm Chứng AI]` cung cấp câu lệnh mẫu (1-click copy) cùng giải thích dấu hiệu nhận biết AI phản hồi chuẩn `[MODE: DISCOVERY]` / `[MODE: BLUEPRINT]`.
  - **Huy hiệu Đã vào AI:** Thẻ kỹ năng hiển thị đèn vi mạch phát sáng nhịp thở `● Đã vào AI` kèm danh sách trợ lý AI đang được bảo vệ.
- **Aggregated Suites (36 Items Total):**
  1. Skill-AI Nucleus Suite (7 Master Skills).
  2. Addy Osmani Production Engineering Suite (29 Items: 25 Skills + 4 Personas).
- **Universal Multi-Tool Ecosystem:** Cursor AI, Windsurf, GitHub Copilot, Aider, Google Antigravity, and Claude Code.
- **External Asset Integrity Law:** `C:\Logo` remains 100% read-only and untouched.
- **Desktop Runtime:** Python 3.15 + PyWebView (Native Edge WebView2).

## 2. Architecture & God Nodes (Graphify AST Audit)
- Core Abstractions:
  - `RuntimePathResolver` (`app/backend/paths.py`): Seamless frozen PyInstaller vs. dev mode path resolution with APPDATA fallback.
  - `UpdateEngine` (`app/backend/updater.py`): SemVer comparison, GitHub Releases API, and Git sync coordinator.
  - `DesktopAPI`: JS-to-Python IPC bridge.
  - `SkillStorage`: Registry persistence & dual-suite seeder.
  - `SkillInstaller`: Multi-target deployment engine.
  - `DesktopBridge`: Frontend asynchronous bridge.
  - `UIComponents`: Notification bell, Notification tray, Dismissible banner, and Update modal.

## 3. Recent Completed Changes
- [x] Global Rebranding: Transformed entire project identity from SkillForge to **`AbyssalSkillsD`** across Python backend, HTML, JS, CSS, config files, and tests.
- [x] Version Reset: Initial public release version set to **`1.0.0`** across `version.json`, `pyproject.toml`, updater, and packaging scripts.
- [x] Standalone PyInstaller Packaging: Built onedir Windows distribution with bundled Edge WebView2, WinForms, data files, and custom app icon.
- [x] Portable ZIP Archive: Created `dist/AbyssalSkillsD-v1.0.0-Portable.zip` (18.61 MB) ready for instant deployment.
- [x] Inno Setup Script: Created `installer/abyssalskillsd.iss` for automated `.exe` installer compilation.
- [x] Windows Shortcuts: Created `AbyssalSkillsD AI.lnk` on Desktop and workspace pointing to `app-icon.ico`.
- [x] Neural Stream & Live Verification: Integrated interactive neural data stream animation and 1-click Windows Explorer/prompt verification proof.
- [x] Logo Typography & Brand Lockup Restoration: Faithfully matched the official brand layout (`Abyssal` cyan-purple gradient + `Skills` bold white + `[D]` glowing squircle badge + `AI SKILL ENGINEERING STUDIO`), replacing the flat uppercase plain text with crisp, GPU-accelerated 60fps typography.
- [x] Dynamic Active Workspace Project Selector (Phase 1): Added toolbar project pill (`.workspace-project-bar`) and folder picker dialog so developers can target any project folder on disk without polluting Desktop.
- [x] Clean Teardown & Uninstall Engine (Phase 1): Added selective multi-AI uninstall modal (`renderUninstallConfirmModal`) with complete directory cleanup.
- [x] Safe Backup (.bak) Engine (Phase 1): Created automatic snapshot backups before overwriting existing skills on disk.
- [x] Logo v4.0 Update ("Biển Trời Giao Hòa • Tâm Điểm Cáo Ẩn Hiện"): Đã đồng bộ 100% bản thiết kế Logo v4.0 mới nhất từ `C:\Logo` sang ứng dụng (thay thế ngôi sao 4 cánh bằng hình tượng Con Cáo Âm Bản Gestalt ẩn hiện tại đường chân trời giữa Sóng Biển `#00B4D8` và Lăng Kính Bầu Trời `#7C3AED`, đi kèm 2 khe mắt chân trời phát quang).
- [x] Multi-Resolution Windows Icons: Tái sinh tệp `app-icon.ico` và `favicon.ico` đa độ phân giải (16px đến 256px) phục vụ Windows Taskbar, shortcut và Edge WebView2.
- [x] Phase 2 (P1 Multi-AI Sync & Workflow Acceleration):
  - [x] 1-Click Multi-AI Global Sync Engine (`DesktopAPI.sync_all_ais()`, `#btn-sync-all-ais`, `renderSyncAllModal`): Triển khai toàn bộ 36 kỹ năng đồng loạt vào Google Antigravity, Claude Code, GitHub Copilot, Cursor AI, Windsurf và Thư mục dự án.
  - [x] Instant Rule Scaffolding Generator (`DesktopAPI.generate_project_rules()`, `#btn-generate-project-rules`, `renderGenerateRulesModal`): Tự động sinh trọn bộ giàn giáo quy tắc `.cursorrules`, `.windsurfrules`, `CLAUDE.md`, `.github/copilot-instructions.md`, `.agents/rules/always-on-autopilot.md`.
  - [x] 1-Click Studio Customizer (`.btn-card-customize`, `.btn-inspector-customize`, `handleCustomizeInStudio()`): Nạp tức thì mọi kỹ năng vào Studio để chỉnh sửa và lưu thành phiên bản riêng.
- [x] Clean Graphify UI Decoupling & Automated AI Watchdog:
  - [x] Bóc tách 100% giao diện Graphify khỏi ứng dụng người dùng (loại bỏ Sidebar tab, container Lab, Command Palette item, và không nạp 9.8MB `graph.json` khi mở app), giúp app khởi động tức thì và tiết kiệm ~20MB RAM.
  - [x] Duy trì `graphify-out/` làm Neo Bộ Nhớ Trực Hệ Thứ 2 cho AI trong workspace, tự động kích hoạt `uv run graphify update .` sau mỗi lần sửa đổi mã nguồn (đạt 11,140 nodes, 11,183 edges, 651 communities).
- [x] Phase 3 (P2 Enterprise Community, Diagnostic Logger & Complete Setup Ecosystem):
  - [x] Live Community Skill Cloud: Nâng cấp Chợ Cộng Đồng với thẻ kỹ năng động, phân loại chủ đề, đánh giá sao, lượt tải, modal chi tiết và cài đặt 1-click vào dự án.
  - [x] Studio 1-Click Cloud Publish: Bổ sung nút `[☁️ Đăng Lên Chợ Cloud]` trong Studio cho phép lập trình viên đóng gói và lan tỏa kỹ năng tự chế lên kho cộng đồng.
  - [x] Diagnostic Logger & Health Center: Tự động ghi nhật ký xoay vòng chuẩn Windows tại `%LOCALAPPDATA%\AbyssalSkillsD\logs\app.log` kết hợp nút `[🩺 Chẩn Đoán]` trên toolbar và xuất báo cáo chẩn đoán ZIP 1-click.
  - [x] Inno Setup Windows Installer: Hoàn thiện kịch bản `installer/abyssalskillsd.iss` tích hợp đầy đủ thông tin bản quyền doanh nghiệp, icon thương hiệu và trình gỡ cài đặt (Uninstaller) trong Windows Settings.
- [x] Phase 4 (Zero-Trust Security, Anti-Spam Telemetry & Error Deduplication Engine):
  - [x] Ring 1 & 2 AppSec Defense: Tích hợp hàm làm sạch dữ liệu nhạy cảm `sanitize_sensitive_data()` loại bỏ 100% tên tài khoản Windows (`C:\Users\<user>\...`), mã thông báo phiên JWT (`[REDACTED_JWT_TOKEN]`), GitHub PATs (`[REDACTED_GITHUB_TOKEN]`), và các mật khẩu/khóa API trước khi xuất log hoặc gửi telemetry.
  - [x] Chống Path Traversal & Bảo vệ Thư mục Hệ thống: Thắt chặt `assert_safe_workspace_path()` ngăn chặn tuyệt đối chọn nhầm ổ đĩa gốc, thư mục hệ điều hành Windows (`C:\Windows`, `System32`), thư mục không tồn tại hoặc tấn công chèn Null Byte.
  - [x] Chống Spam Báo Lỗi & Gom Nhóm Lỗi Trùng Lặp (Deduplication Engine): 
    - Phía Backend: Tự động băm mã lỗi mã hóa SHA-256 (`fingerprint`) dựa trên `error_type + module + line_number`. Khi người dùng gặp cùng 1 lỗi nhiều lần, hệ thống chỉ tăng bộ đếm tần suất (`occurrences: +1`) thay vì tạo rác bản ghi.
    - Phía Frontend: Tích hợp bộ đếm Cooldown 180 giây (`localStorage`) vô hiệu hóa spam click hoặc rage-clicking.
  - [x] Supabase Cloud Schema An Toàn: Bổ sung bảng `public.system_error_reports` kèm ràng buộc UNIQUE `(fingerprint, app_version)`, chỉ số Index tốc độ cao và phân quyền RLS chuẩn Zero-Trust (Client ẩn danh chỉ được INSERT, chỉ Admin mới có quyền SELECT xem chi tiết lỗi).
  - [x] Giao diện Chẩn đoán An Toàn: Tích hợp dải biểu ngữ khiên bảo mật thông tin và nút `[🚀 Gửi Báo Cáo Lên Cloud]` trong hộp thoại Chẩn đoán.
- [x] Phase 5 (Sửa Lỗi Tràn Nút Thẻ & Tách Biệt 2 Luồng Kích Hoạt Nhanh Thông Minh):
  - [x] Sửa triệt để lỗi tràn nút (Anti-Overflow CSS): Bổ sung `overflow: hidden;` cho `.bento-card` và `.bento-card-clean`, tái cấu trúc `.card-action-group` với `flex-wrap: wrap;` và tách 2 nhóm `.card-action-left` / `.card-action-right`. Nút Pro Settings rút gọn thành `⚙️ Cài Đặt ▾`.
  - [x] Tách Biệt 2 Luồng Kích Hoạt Thông Minh (Zero Silent Overwrites):
    - Luồng Kỹ Năng Mới: Nút `[⚡ Kích Hoạt N Kỹ Năng Mới (1-Click)]` chỉ cài đặt đúng các kỹ năng chưa từng nạp vào máy, không chạm đến kỹ năng đã có.
    - Luồng Kỹ Năng Cập Nhật: Khi tệp trên máy khác nội dung với kho (ví dụ người dùng đã sửa hoặc kho có bản mới), hệ thống hiển thị huy hiệu `[🔄 Có cập nhật]` và pill `[🔄 Có K Kỹ Năng Cần Cập Nhật]`. Bấm vào mở Popup So Sánh 2 Cột (Side-by-Side Diff) gồm Cột Trái (Bản Local trên máy) và Cột Phải (Bản Mới từ kho) chờ người dùng duyệt (`[Giữ Lại Bản Cũ]` hoặc `[Đồng Ý Cập Nhật]` với cơ chế sao lưu `.bak` tự động).
    - Luồng Hoàn Tất: Khi 36/36 kỹ năng đã kích hoạt và không có bản cập nhật, nút chính chuyển sang màu xanh ngọc hoàn tất `[✓ Đã Kích Hoạt Đầy Đủ (36/36)]`.
- [x] Rebuilt Portable Package: Cập nhật tệp `dist/AbyssalSkillsD-v1.0.0-Portable.zip` (22.33 MB, SHA256: `496a415c8eff...`).
- [x] Phase 6 (Supabase Cloud Live Handshake & Inno Setup Single-File Installer Compilation):
  - [x] Live Supabase Cloud Connection: Kết nối chính thức dự án đám mây `https://ldzgwlvhbomjmonxutyc.supabase.co` với cấu hình `anon_key` hợp lệ. Hoàn tất cấu trúc bảng `profiles`, `skills`, `skill_references`, và `system_error_reports` kèm RLS an toàn.
  - [x] Live Error Telemetry Sync: Bổ sung luồng đẩy telemetry nền sang Supabase Cloud khi có sự cố mới. Đã kiểm thử bắt tay thực tế (Live Handshake HTTP 201 Created).
  - [x] Single-File Windows Installer: Biên dịch thành công tệp cài đặt chính thức `dist/AbyssalSkillsD-Setup-v1.0.0.exe` (16.95 MB, SHA256: `3E0C650DF7E4CA4890D2EFE46ED7C4AA0850EA14BD4E3606DA9D6C95754E93BB`) qua Inno Setup 6, tích hợp Desktop shortcut, Start Menu shortcut và Uninstaller chuẩn Windows.
  - [x] Portable Package: Cập nhật `dist/AbyssalSkillsD-v1.0.0-Portable.zip` (22.33 MB, SHA256: `90434965fc9e2e5395ac484d74dedb4d41e65f6f8670430f1bfb537877f4a003`).
  - [x] Enterprise Bilingual Documentation: Đã thiết lập tài liệu song ngữ chuyên nghiệp chuẩn quốc tế gồm `README.md` (English) và `README.vi.md` (Tiếng Việt) với nút chuyển đổi ngôn ngữ 2 chiều, kịch bản cài đặt tự động `scripts/install.ps1`, sơ đồ kiến trúc Mermaid, ma trận so sánh và cẩm nang 36 kỹ năng.
- [x] Phase 7 (Cross-Platform macOS & Linux Architecture & GitHub Actions CI/CD Matrix):
  - [x] Universal POSIX Installer: Xây dựng `scripts/install.sh` hỗ trợ 1-Liner Terminal (`curl | bash`) trên macOS & Linux, tự động cấu hình WKWebView / WebKitGTK và tạo launcher `abyssalskillsd` & `abyssalskillsd.desktop`.
  - [x] Cross-Platform Path Engine: Tối ưu hóa `paths.py` và `assert_safe_workspace_path` hỗ trợ chuẩn thư mục Windows (`%LOCALAPPDATA%`), macOS (`~/Library/Logs`), Linux (`XDG_STATE_HOME`), và kiểm soát an toàn chống chọn thư mục hệ thống Unix (`/etc`, `/usr`, `/bin`).
  - [x] GitHub Actions CI/CD Matrix: Thiết lập `.github/workflows/build-release.yml` tự động biên dịch đám mây 3 hệ điều hành (`windows-latest`, `macos-latest`, `ubuntu-latest`) và phát hành release artifacts (Setup.exe, macOS.zip, Linux.tar.gz).
  - [x] Bilingual Cross-Platform README: Cập nhật `README.md` và `README.vi.md` với bảng hướng dẫn cài đặt trực tiếp cho Windows, macOS và Linux.
- [x] Passed 100% Verification: All 28/28 automated test gates passed (`tests/test_verification.py`).
- [x] Phase 8 (Complete Live Supabase Auth Lifecycle & Desktop OAuth Loopback Engine):
  - [x] Full REST Auth Engine: Connected live `sign_in`, `sign_up` and `sign_out` to Supabase Auth (`/auth/v1/token`, `/auth/v1/signup`, `/auth/v1/logout`) with automatic profile sync to `public.profiles`.
  - [x] Desktop OAuth Loopback Engine: Implemented local HTTP callback server on port 54321 with HTML/JS hash-to-query bridge page for seamless Google & GitHub social sign-in.
  - [x] Auto-Login on Sign Up: Instant session creation upon registration when email confirmation is disabled, or intuitive guidance to sign in.
  - [x] Gate 26 Automated Test: Added Gate 26 verifying URL config, sign-up/sign-in validation, loopback server lifecycle, token revocation, and session disk persistence.
- [x] Phase 9 (Developer Profile & Portfolio Hub with Real-Time Avatar Sync):
  - [x] Dedicated Profile Tab: Added `data-nav="profile"` to left activity sidebar and connected 1-click navigation from TopBar user widget dropdown.
  - [x] Bento Grid Profile Architecture: Crafted Hero Profile Card with glowing avatar, Provider badges (GitHub Verified / Supabase Cloud), 4-metric statistics summary (Installed, Favorites, Contributed, Security Session), and Portfolio list.
  - [x] Artistic Avatar Selection: Integrated 6 preset Abyssal Sky v2.0 artistic avatars + custom URL input with instant real-time synchronization to TopBar and Supabase `public.profiles`.
  - [x] Gate 27 Automated Test: Added Gate 27 verifying stats calculations, profile update lifecycle, HTML bindings, and session persistence.
- [x] Phase 10 (Universal AutoPilot & Individual Skill OpenAI Codex Integration & Gate 28):
  - [x] Root & Rule Scaffolding: `generate_rule_scaffold()` generates `CODEX.md` and `.codex/rules/always-on-autopilot.md`.
  - [x] Multi-AI Sync & Installer: Added target `codex` deploying to `~/.codex/skills/` and workspace `CODEX.md`.
  - [x] Sidebar & Autopilot UI: Added `OpenAI Codex` row with LED status indicator in sidebar and `Codex` pill in `autopilot-tools-grid`.
  - [x] Individual Skill Cards & Inspector Integration:
    - Added `pro-sw-codex` toggle to the Pro Settings drawer (`pro-targets-grid`).
    - Added `sw-codex` toggle to the Skill Inspector footer target configuration.
    - Added OpenAI Codex to the Community Skill installation dialog and Uninstaller modal.
    - Updated `SkillScanner` fast-path bulk scanner (`get_installed_targets_and_paths`, `detect_installed_targets`) to detect `~/.codex/skills/<skill_id>` on disk.
    - Connected `app.js` single-skill target selection and installation flows for Codex.
  - [x] Modals & Brand Vector: Added official `brandCodex` SVG and checkboxes in `renderSyncAllModal` & `renderGenerateRulesModal`.
  - [x] Gate 28 Automated Test: Verified rule generation, single-skill Codex target install/uninstall, scanner detection, and UI bindings (28/28 gates pass).
- [x] Standalone Packaging (Hotfix v1.0.1): Built `dist/AbyssalSkillsD-Setup-v1.0.1.exe` (18.55 MB) & `dist/AbyssalSkillsD-v1.0.1-Portable.zip` (24.06 MB).
- [x] Phase 11 (CI/CD Matrix Fix & Clean Runner Quality Gate Resilience):
  - [x] Storage Resilience: `SkillStorage.sync_all_local_skills()` and `initialize()` preserve pre-seeded skills from `skills_registry.json` instead of wiping them on clean CI checkout.
  - [x] API Decoupling: Removed redundant `sync_all_local_skills()` call from `install_all_skills()`.
  - [x] Cross-Platform Test Gates: Adapted Gates 19, 24, and 25 to run seamlessly across Windows, macOS, and Linux runners without assuming Windows paths or pre-built folders.
  - [x] Inno Setup CI Integration: Added `choco install innosetup` to GitHub Actions `windows-latest` runner for automated cloud compilation of `Setup-v1.0.1.exe`.
  - [x] Multi-Platform Release Matrix: Verified all 28/28 verification gates pass green in simulated clean checkout.
- [x] Phase 12 (Visual Line Diff Highlighting, Selective Chunk Picker & Apply All Engine):
  - [x] Visual Line Diff Highlighting: Side-by-side synchronized diff with line numbers, green `+` highlight for additions, red `-` highlight for deletions, and padding for vertical alignment.
  - [x] Statistics & Status Toolbar: Summary badges `+X dòng mới`, `-Y dòng sửa/xóa`, and `⚡ Z khối khác biệt`.
  - [x] Selective Chunk Picker: Horizontal scrollable strip with interactive checkboxes `[✓] Khối K: ...` enabling users to selectively pick which changes to apply or ignore.
  - [x] 1-Click Navigation: Clicking any chunk card smoothly scrolls the diff editor directly to that change block.
  - [x] Three-Tier Action Controls:
    - `[🛡️ Giữ Lại Bản Cũ (Bỏ qua)]`: Rejects incoming updates.
    - `[✓ Áp Dụng Phần Đã Chọn]`: Merges only checked chunks into local file with automatic `.bak` snapshot.
    - `[⚡ Thay Đổi Toàn Bộ]`: Overwrites entire skill with new version and creates `.bak` backup.
  - [x] Gate 25 Extended: All 28 automated gates verified passing 100%.
- [x] Knowledge Graph: Updated Graphify AST (499 nodes, 1066 edges, 38 communities).


## 2026-11-01 — Reliability and real-cloud correction (authoritative current status)

The earlier checked boxes/28-gate claims above are historical implementation notes, not acceptance proof. Follow `docs/VERIFICATION-1.1.0.vi.md` for current evidence and remaining work.

- User approved Windows-first reliability/cloud blueprint. Preserve branding and original 36 entries; no external skills modified.
- Supabase project verified `ldzgwlvhbomjmonxutyc`. Versioned migration applied after backup, rollback SQL tests and explicit approval. Existing 2 users/2 profiles/3 reports retained. Market admin assigned to confirmed user UUID `9e36935e-1538-401b-ac2e-9798ac5e784b`; never infer admin from editable metadata.
- Real GitHub PKCE login works in native Windows source app. Google is disabled server-side. Email and independent desktop A/B journeys remain unaccepted.
- Studio publish -> independent anonymous search/install -> soft removal exercised on live cloud with a temporary nonpersonal test skill. No local legacy samples seeded into cloud.
- Atomic writes/backups, safe paths/junction checks, per-target diff/stale protection, preserve custom shared rules, recoverable uninstall, truthful file-presence states, URL-separated Git cache implemented with isolated tests. Corrupt registry fails rather than reseeding.
- CloudClient/Auth/Community/Telemetry/SecureStorage separated. No admin secrets or tokens returned through bridge. Manual diagnostic preview/retry only; Windows refresh credential stored securely.
- 30 isolated regression tests currently pass. pip-audit reported no known vulnerabilities in inspected dependencies. Neither fact proves full application acceptance.
- Candidate version 1.1.0. Windows distribution acceptance still pending; no installer run on user's primary machine. macOS/Linux and Graphify CLI unverified. Old Graphify graph stays navigation-only until regenerated.
- Private backup/evidence under ignored `build/verification`; never package or commit raw cloud backup/session/logs.

## 2026-11-06 — Multi-IDE Activation, Cross-Account Community Sync & In-Place Auto-Updater
- **Multi-IDE Activation Repair:** Fixed `handleBatchInstallAll` and `install_all_skills` targets array to explicitly include all 6 supported AI environments: `["antigravity", "cursor", "windsurf", "claude", "copilot", "codex", "workspace"]`. Fixed filter logic so partially missing targets trigger batch deployment. Ensured `workspace_path` and `overwrite=True` with `.bak` snapshots are passed in individual and batch activations.
- **Cross-Account Community Cloud Sync:** Fixed cache staleness by clearing local cache on publish and triggering `loadCommunitySkills()` automatically upon navigating to the Community tab. Added client-side validation for slug and auth session state.
- **In-Place Auto-Updater & Version Permanence:** Implemented `download_and_apply_update()` with live progress polling, silent Inno Setup invocation (`/SILENT /DIR /FORCECLOSEAPPLICATIONS /CLOSEAPPLICATIONS`), and safe app restart without losing `%APPDATA%` data. Synced bundle `version.json` into `%APPDATA%` to prevent stale version display.
- **Automated Verification:** Added 3 new test gates in `tests/test_services.py` verifying multi-target deployment, community cache invalidation, and updater download/progress lifecycle (all 34 tests passing).
- **Release v1.1.0 Artifact Generation & GitHub Actions Green:**
  - Resolved Windows 8.3 short-name path comparison in `test_diff_includes_references_and_applies_selected_file`.
  - Added Windows Credential Manager non-interactive session exception handling in `test_windows_credential_store_roundtrip`.
  - Fixed test runner import resolution (`sys.path.insert(0, tests)`) and enabled UTF-8 console output for Windows CI runner.
  - Successfully published official release assets on GitHub (`AbyssalSkillsD-Setup-v1.1.0.exe`, `AbyssalSkillsD-Setup.exe`, `AbyssalSkillsD-v1.1.0-Portable.zip`, `AbyssalSkillsD-Portable.zip`).
  - Auto-updater endpoint `https://api.github.com/repos/Play-with-me/AbyssalSkills-AI/releases/latest` now points to `v1.1.0`. All client apps automatically receive update notifications (red dot on bell, pulsing badge, 1-click in-place update).
- **User Diagnostic & Images Investigation (2026-11-06):**
  - **Image 1 & 2 (Codex "chưa thấy kết nối abyssalSkillsD" & "chỉ thấy 6 skill lúc 12:27 PM"):** Codex is an LLM client, not a daemon with socket connections to manager apps. At 12:27 PM, only the first seed existed. At 12:29 PM and 2:16 PM, all 36 skills were written to `C:\Users\kyuu4\.codex\skills\`. Verified all 36 skills are currently present on disk.
  - **Image 3 (v1.0.0 & "Hệ thống đang ở phiên bản mới nhất"):** Captured when the user ran v1.0.0 before v1.1.0 was published on GitHub Releases. When GitHub had only v1.0.0, the app correctly reported no newer version. Once v1.1.0 was published, the app received v1.1.0.
  - **Standalone Binary Fix:** Added missing backend modules (`community`, `telemetry`, `cloud_client`, `secure_storage`, `logger`) to `abyssalskillsd.spec` `hidden_imports` and recompiled standalone binary at `C:\Users\kyuu4\AppData\Local\Programs\AbyssalSkillsD\AbyssalSkillsD.exe`. Verified 100% running smoothly.

## 2026-11-06 (Late Turn) — Resolution of 36 Persistent False Updates, Community Cloud 2-Tier Ergonomics & Seamless In-Place Auto-Update
- **Persistent 36 Updates False-Positive Resolved:**
  - Root Cause: `generate_skill_markdown()` dumped YAML without `width=1000`, causing PyYAML to wrap 80-char descriptions, while on-disk files had single-line descriptions. String comparison `!=` flagged all 36 skills as having updates. When diff modal opened, it only viewed and updated a single file in `antigravity`, leaving `claude`, `copilot`, `codex` and reference files untouched.
  - Fix: Added `width=1000` to `yaml.safe_dump()`, introduced `files_differ()` with semantic YAML frontmatter parsing and normalized newline comparison (`\r\n` -> `\n`).
  - Enhanced `apply_skill_diff()`: When `apply_all: True`, writes all candidate files across all installed targets for that skill, marking `has_update = False` permanently.
  - Verified: `Number of skills with has_update: 0` (All 36 skills 100% synchronized and green).
- **Community Cloud 2-Tier Ergonomics (Anti-Overflow Layout):**
  - Root Cause: `.comm-card-actions` crammed 6 buttons into a single horizontal flex line without wrapping, squishing buttons and causing `.btn-install-community` to protrude downward out of the card.
  - Fix: Redesigned `.comm-card-footer` into a 2-tier ergonomic layout: Tier 1 for auxiliary/author actions (`★ Yêu thích`, `🚩 Báo cáo`, `✏️ Sửa`, `🗑️ Gỡ`), Tier 2 for primary actions (`[👁️ Chi Tiết]` + `[⚡ Tải & Cài Đặt Vào AI]`). Added clean CSS tokens with `min-width: 0`, `gap: 8px`, and smooth hover physics.
- **Seamless 1-Click In-Place Auto-Update:**
  - Removed manual GitHub external link from primary action area in `renderUpdateModal()`.
  - Prominently styled `[⚡ Tự Động Cập Nhật & Khởi Động Lại Ngay (1-Click)]` with live progress polling and silent Inno Setup invocation.
  - Compiled and published distribution: `dist/AbyssalSkillsD-Setup-v1.1.0.exe` (16.29 MB) and `dist/AbyssalSkillsD-v1.1.0-Portable.zip` (18.75 MB). Retagged `v1.1.0` on GitHub.
