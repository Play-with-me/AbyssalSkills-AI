<p align="center"><img src="app/frontend/assets/logo/github-banner.svg" alt="AbyssalSkillsD" width="100%"></p>

# AbyssalSkillsD

A Python/PyWebView desktop manager for AI skill files. Includes the original 36 library entries: 7 Skill-AI skills and 29 Addy Osmani entries (including four personas). Author: Lâm Nhựt Hải Đăng (Kyuu449977).

[Tiếng Việt](README.vi.md) · [Verification evidence and remaining acceptance work](docs/VERIFICATION-1.1.0.vi.md)

Version 1.1.0 is a Windows release candidate undergoing acceptance. macOS/Linux and clean-machine setup execution are not yet verified.

### Download & Installation
- **Windows Setup (Recommended):** [Download Latest Setup.exe](https://github.com/Play-with-me/AbyssalSkills-AI/releases/latest/download/AbyssalSkillsD-Setup.exe)
- **Portable Edition:** [Download Latest Portable.zip](https://github.com/Play-with-me/AbyssalSkills-AI/releases/latest/download/AbyssalSkillsD-Portable.zip)
- **1-Click PowerShell Install:**
  ```powershell
  irm https://raw.githubusercontent.com/Play-with-me/AbyssalSkills-AI/main/scripts/install.ps1 | iex
  ```

- Local library, search, workspace selection, Studio and favorites.
- Per-target skill/reference/rule installation; a file being present does not prove the AI loaded it.
- File-specific diff with stale-preview checks, immutable backups before replacement, preserved custom shared rules and recoverable uninstall archives.
- Git cache isolated by URL with origin checks. Git is an external prerequisite; Graphify is optional and separately installed.
- Real Supabase community browsing, pagination, publish/edit/remove, favorites, reporting and moderation. No sample catalog presented as cloud data.
- Real GitHub PKCE login tested. Google is not enabled on the current project. Email confirmation is supported but its complete journey has not been accepted yet.
- Refresh tokens use Windows Credential Manager. JavaScript never receives access/refresh tokens or administrator secrets.
- Diagnostics are previewed and explicitly sent by the user, with no automatic upload/retry. Redaction is best effort; review before sending.

```powershell
uv sync --frozen --extra dev
uv run python tests/test_verification.py
uv run python main.py
```

Windows 10/11 x64 and WebView2 are required. JavaScript syntax checks require Node. Build with `uv run python scripts/build_distribution.py` and check with `uv run python tests/check_distribution.py`. Inno Setup is required to compile Setup.exe. Packages contain source hashes, commit provenance and checksums; runtime sessions/logs/caches are excluded.

The production migration and rollback-only authorization tests are under `supabase/`. Existing user data is preserved; legacy local samples are never automatically published. Administrator privileges are assigned server-side, not from editable profile metadata.

The old “28/28” source-string gates and “100% operational” claims are superseded by isolated behavioral tests and the evidence report. Passing unit tests is not a claim that every cloud provider, AI integration or distribution has been exercised.
