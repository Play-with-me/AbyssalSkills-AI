# 🌌 AbyssalSkillsD (v1.0.0)

**Enterprise Standalone Desktop Application & Marketplace for AI Coding Skills**  
*Tương thích toàn diện với Google Antigravity, Claude Code, GitHub Copilot, Cursor AI, Windsurf và Aider.*

---

## 🌟 Tính Năng Cốt Lõi

1. **Bộ 36 Kỹ Năng Đỉnh Cao (Aggregated 36-Skill Suite):**
   - **Skill-AI Nucleus (7 Master Skills):** `strict-architect-coder`, `ui-ux-design-master`, `shadcn-tailwind-artisan`, `web-assets-creative-vault`, `nextjs-fullstack-master`, `supabase-backend-architect`, `playwright-web-tester`.
   - **Addy Osmani Production Engineering (29 Items):** 25 production skills + 4 chuyên gia persona (`frontend-ui-engineering`, `security-and-hardening`, `test-driven-development`, `performance-optimization`...).

2. **Kích Hoạt Nhanh Thông Minh & Chống Ghi Đè (Zero Silent Overwrites):**
   - **Tách biệt 2 luồng:** Kích hoạt 1-click cho kỹ năng mới, và Popup So Sánh 2 Cột (Side-by-Side Diff) cho kỹ năng có cập nhật.
   - **Bảo vệ tùy biến người dùng:** Tùy chọn `[Giữ Lại Bản Cũ Của Tôi]` hoặc `[Đồng Ý Cập Nhật]` với cơ chế sao lưu `.bak` tự động.

3. **Đồng Bộ Đám Mây & Chợ Kỹ Năng (Supabase Cloud Backend):**
   - Tích hợp sẵn cơ sở dữ liệu PostgreSQL và phân quyền bảo mật Row-Level Security (RLS) chuẩn Zero-Trust.
   - Chợ Kỹ Năng Cộng Đồng (Community Cloud) và Đăng tải 1-click từ Studio.
   - Trung tâm Telemetry báo lỗi tự động chống spam (`fingerprint` deduplication).

4. **Trải Nghiệm Thị Giác & Bản Quyền Thương Hiệu (Abyssal Sky v2.0):**
   - Biểu tượng thương hiệu: *Biển Trời Giao Hòa • Tâm Điểm Cáo Ẩn Hiện* (`#050C1A`, `#00B4D8`, `#7C3AED`).
   - Hoạt ảnh sóng vi mạch dữ liệu (Neural Stream Stage) với độ trễ phản hồi sub-250ms.
   - Khay kiểm chứng AI tức thì và mở thư mục thực tế trên ổ cứng (Windows Explorer).

---

## 📦 Bộ Cài Đặt & Phát Hành (Releases)

- **Trình Cài Đặt Tiêu Chuẩn Windows:**  
  `dist/AbyssalSkillsD-Setup-v1.0.0.exe` (16.95 MB) — Tự động thiết lập Desktop & Start Menu shortcut, tích hợp trình gỡ cài đặt trong Windows Settings.
- **Bản Di Động Portable (Chạy ngay không cần cài đặt):**  
  `dist/AbyssalSkillsD-v1.0.0-Portable.zip` (22.33 MB).

---

## 🛠️ Dành Cho Lập Trình Viên (Developer Setup)

### Yêu cầu môi trường:
- Windows 10/11 64-bit
- Python 3.12+ (khuyên dùng thông qua `uv`)

### Cài đặt và khởi chạy từ mã nguồn:
```powershell
# Cài đặt thư viện phụ thuộc
uv sync

# Chạy ứng dụng trực tiếp
uv run main.py
```

### Chạy bộ kiểm thử tự động (25 Cổng Chất Lượng):
```powershell
uv run python tests/test_verification.py
```

### Đóng gói ứng dụng:
```powershell
# 1. Đóng gói Standalone & Portable ZIP
uv run python scripts/build_distribution.py

# 2. Biên dịch trình cài đặt Inno Setup
& "C:\Users\kyuu4\AppData\Local\Programs\Inno Setup 6\ISCC.exe" "installer\abyssalskillsd.iss"
```

---

## 📄 Bản Quyền & Giấy Phép
Phát triển bởi **Kyuu4** & Đội ngũ Kiến trúc sư Kỹ năng AI. Giữ toàn quyền sở hữu trí tuệ thương hiệu Abyssal Sky v2.0.
