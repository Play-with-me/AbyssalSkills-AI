# AbyssalSkillsD Design System (`DESIGN.md`)
*Studio Grade: Linear / Raycast / shadcn-tailwind-artisan Dual-Theme Workbench with Abyssal Sky v2.0 Geometric Brand Identity*

---

## 1. Brand Essence & Aesthetic Philosophy
- **Archetype:** Linear / Raycast / Cursor Desktop Precision Workbench
- **Geometric Brand System:** Abyssal Sky v2.0 (`kyuu4-abyssal-sky-design-system` via `ip-as-logo` & `voltagent-awesome-design-md`)
- **Visual Motif:** Sacred Geometry & Architectural Blueprint Grid with Celestial Aurora Violet (`#7C3AED` -> `#C084FC`) and Electric Ocean Cyan (`#00B4D8` -> `#06D6A0`) on an Abyssal Void Canvas (`#050C1A`).
- **Component Standard:** `shadcn-tailwind-artisan` (Tailwind v4 Semantic Theme Tokens, Radix Primitives, 100% WAI-ARIA Keyboard Accessibility)
- **Asset Standard:** `web-assets-creative-vault` (Simple Icons brand logotypes, Lucide vector icons, Abyssal Sky vector SVG marks)
- **Theme Support:** Native Dual-Theme support (`[data-theme="dark"]` Abyssal Sky Obsidian default, `[data-theme="light"]` Vercel Crisp Daylight)
- **Design Law:** 100% Zero-Emoji Policy. All iconography uses uniform `1.5px` stroke vector SVGs.

---

## 2. Geometric Logo & Background Blueprint Specification (Abyssal Sky v4.0)

### A. The 4-Shape Complexity Budget (`ip-as-logo` & `C:\Logo\DESIGN.md`)
1. **Khối Bầu Trời (Celestial Sky Vault — Nửa trên):**
   - Vòm lăng kính dày, bo tròn `R=28px`, vươn góc `120°`.
   - Gradient: Aurora Violet (`#7C3AED` -> `#C084FC`).
2. **Khối Đại Dương (Abyssal Wave Crest — Nửa dưới):**
   - Vòm sóng cuộn vòng ôm khối bầu trời theo tỉ lệ vàng $\Phi = 1.618$.
   - Gradient: Electric Ocean Cyan (`#00B4D8` -> `#06D6A0`).
3. **Tâm Điểm Cáo Âm Bản Ẩn Hiện (Emergent Negative-Space Fox Silhouette — Tâm điểm):**
   - Hình dáng đầu cáo tinh anh được khắc âm bản trực tiếp tại đường chân trời nơi Khối Sóng và Lăng Kính Bầu Trời giao thoa (tai vươn nhẹ lên bầu trời, mõm chạm vào đại dương).
   - Tuyệt đối không vẽ hoạt hình/esports phô trương, tôn trọng nguyên tắc Gestalt tối giản cao cấp.
4. **Khe Mắt Chân Trời Bí Ẩn (Whisper Horizon Eye Slits):**
   - Hai khe mắt ánh sáng quang học cực mỏng (`#00B4D8` Cyan và `#A855F7` Violet) lấp lánh nhẹ nhàng (`opacity: 0.9`), tạo thần thái sống động cho biểu tượng.
5. **Rãnh Chân Trời (Horizon Diagonal Channels):**
   - Rãnh âm bản rộng `26px` kết nối gò má cáo ra ngoài không gian, ngăn dính nét khi thu nhỏ `16px`.

### B. Persistent Application Geometric Background
- Element: `#geometric-background-canvas` / `.geometric-background-canvas`
- Structure:
  - Technical blueprint coordinate grid (`64x64px` major, `16x16px` micro hairpins)
  - Golden-ratio concentric orbit rings (`r="340"`, `r="260"`, `r="180"`, `r="100"`)
  - Watermark Abyssal Sky geometric monogram at opacity `0.32` (dark) / `0.18` (light)
  - `pointer-events: none` and pinned `fixed inset-0 z-0` so UI interaction is 100% unimpeded.

---

## 3. Dual-Theme Palette & Semantic Tokens

### A. Dark Mode Tokens (Abyssal Void — Default)
- `--bg-canvas`: `#050C1A` (Abyssal Void)
- `--canvas-deep`: `#010308` (Deep Space)
- `--bg-surface`: `#0A1428`
- `--bg-card`: `#0F1D38`
- `--bg-card-hover`: `#16284C`
- `--bg-elevated`: `#1E2D4A`
- `--bg-input`: `rgba(255, 255, 255, 0.04)`
- `--border-subtle`: `#1E2D4A`
- `--border-hover`: `#2E446E`
- `--border-focus`: `#00B4D8`
- `--specular-top`: `inset 0 1px 0 rgba(255, 255, 255, 0.08)`
- `--text-primary`: `#F8FAFC`
- `--text-secondary`: `#CBD5E1`
- `--text-muted`: `#64748B`

### B. Light Mode Tokens (`[data-theme="light"]` — Crisp Daylight)
- `--bg-canvas`: `#F8FAFC`
- `--bg-surface`: `#FFFFFF`
- `--bg-card`: `#FFFFFF`
- `--bg-card-hover`: `#F1F5F9`
- `--bg-elevated`: `#FFFFFF`
- `--bg-input`: `#F8FAFC`
- `--border-subtle`: `#E2E8F0`
- `--border-hover`: `#CBD5E1`
- `--border-focus`: `#7C3AED`
- `--specular-top`: `none`
- `--text-primary`: `#050C1A`
- `--text-secondary`: `#475569`
- `--text-muted`: `#94A3B8`

### C. Semantic Brand Accents (`kyuu4-abyssal-sky-design-system`)
- `--ocean-cyan`: `#00B4D8` (Primary depth accent)
- `--ocean-secondary`: `#06D6A0` (Emerald secondary)
- `--sky-violet`: `#7C3AED` (Celestial sky accent)
- `--sky-highlight`: `#C084FC` (Aurora highlight)
- `--brand-antigravity`: `#4285F4` (Google Blue)
- `--brand-claude`: `#D97706` (Anthropic Terracotta / Amber)
- `--brand-copilot`: `#8B5CF6` (Copilot Purple)
- `--brand-nextjs`: `#000000` / `#FFFFFF`
- `--brand-tailwind`: `#06B6D4` (Tailwind Cyan)
- `--brand-supabase`: `#3ECF8E` (Supabase Emerald)
- `--brand-playwright`: `#45BA4B` (Playwright Green)
- `--led-success`: `#10B981` (Emerald active indicator)

---

## 4. Typography
- **Display:** `Syne, SF Pro Display, -apple-system, sans-serif`
- **Body & UI:** `Space Grotesk, Inter, system-ui, sans-serif`
- **Monospace & Code:** `JetBrains Mono, Fira Code, monospace`

---

## 5. Interactive Component Protocols

### A. Command Palette (`Ctrl+K` / `Cmd+K`)
- Center overlay dialog (`max-width: 580px`), animated entry (`scale 0.98 -> 1`, `150ms`).
- Direct keyboard navigation (`ArrowUp`, `ArrowDown`, `Enter`, `Escape`).
- Grouped into "Hành động nhanh" and "Nhảy tới kỹ năng".

### B. Organization Hero Banner (`Skill-AI-private`)
- Clean hairline bordered banner highlighting the 7 core skills and 26 reference playbooks.
- Prominent `1-Click Batch Install` button to activate the entire suite on the host machine.

### C. Community Cloud Hub (`supabase-backend-architect`)
- Live preview of the PostgreSQL + RLS schema with syntax highlighting and 1-click SQL copy.

### D. Skill Artisan Studio & Template Drawer
- Step-by-step assistant for beginners and full raw SKILL.md Markdown editor for advanced engineers.
- Interactive template drawer with production-grade templates from `addyosmani/agent-skills`.
