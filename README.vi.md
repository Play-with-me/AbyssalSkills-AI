<p align="center"><img src="app/frontend/assets/logo/github-banner.svg" alt="AbyssalSkillsD" width="100%"></p>

# AbyssalSkillsD

Trình quản lý tệp kỹ năng AI bằng Python/PyWebView. Giữ 36 mục thư viện: 7 kỹ năng Skill-AI và 29 mục từ Addy Osmani (gồm 4 persona). Tác giả: Lâm Nhựt Hải Đăng (Kyuu449977).

Bản 1.1.0 đang nghiệm thu Windows; chưa công bố là bản phát hành đã nghiệm thu đầy đủ. Xem [kết quả kiểm chứng](docs/VERIFICATION-1.1.0.vi.md).

### Tải Về & Cài Đặt Bản Mới Nhất
- **Bản Cài Đặt Windows (.exe - Khuyên dùng):** [Tải Bản Cài Đặt Mới Nhất](https://github.com/Play-with-me/AbyssalSkills-AI/releases/latest/download/AbyssalSkillsD-Setup.exe)
- **Bản Di Động (Portable .zip):** [Tải Bản Portable Mới Nhất](https://github.com/Play-with-me/AbyssalSkills-AI/releases/latest/download/AbyssalSkillsD-Portable.zip)
- **Cài đặt 1 dòng lệnh PowerShell:**
  ```powershell
  irm https://raw.githubusercontent.com/Play-with-me/AbyssalSkills-AI/main/scripts/install.ps1 | iex
  ```

## Chức năng

- Thư viện, tìm kiếm, chọn dự án, Studio lưu trên máy và yêu thích.
- Ghi SKILL.md, reference, rule cho các đích được hỗ trợ. “Đã ghi tệp” chỉ chứng minh tệp tồn tại; hãy kiểm tra skill trong chính công cụ AI.
- Diff theo từng tệp/đích, chặn bản xem trước lỗi thời; snapshot riêng trước khi thay tệp. Sao lưu lỗi thì dừng. Gỡ giữ bản cài trong `.abyssal-removed`, giữ phần rules tự chỉnh.
- Git cache phân biệt URL và kiểm tra origin; cập nhật kho dựa trên commit. Cần Git ngoài.
- Community dùng Supabase thật, phân trang 24; đọc/cài không cần đăng nhập. Đăng bài, sửa/gỡ bài của mình, yêu thích và báo cáo yêu cầu đăng nhập. Quản trị viên xem báo cáo và ẩn bài.
- GitHub OAuth đã thử thật. Google hiện chưa bật trên dự án; ứng dụng báo chưa khả dụng. Email cần xác nhận; chưa nghiệm thu luồng email toàn trình.
- Refresh token lưu Windows Credential Manager; access token trong bộ nhớ, không trả token hoặc khóa quản trị cho JavaScript.
- Chẩn đoán có xem trước, tự nhập thông báo, xuất ZIP và chủ động gửi khi đăng nhập. Không tự gửi hoặc tự gửi lại. Bản chờ đã làm sạch dùng cùng request ID khi thử lại. Lọc thông tin nhạy cảm là hỗ trợ, người gửi vẫn phải kiểm tra nội dung.

## Chạy và kiểm tra

```powershell
uv sync --frozen --extra dev
uv run python tests/test_verification.py
uv run python main.py
```

Cần Windows 10/11 x64 và WebView2. Node cần cho kiểm tra cú pháp JavaScript. Graphify cần cài riêng và chỉ phân tích khi yêu cầu; đồ thị trong repository có thể cũ. Chưa xác minh macOS/Linux.

```powershell
uv run python scripts/build_distribution.py
uv run python tests/check_distribution.py
```

Build tạo portable, setup khi có Inno Setup, manifest commit/hash và SHA256SUMS. Không đóng gói session, log, cache Git hoặc chẩn đoán chờ. Không chạy installer trên máy chính để thay cho nghiệm thu Windows sạch.

## Cloud

Migration: `supabase/migrations/202611010001_reliable_cloud.sql`. Đã áp dụng lên dự án hiện tại sau backup và xác nhận của chủ dự án. Các kiểm tra quyền A/B/ẩn danh ở `supabase/tests/cloud_acceptance.sql` chạy trong transaction rollback; không phải bằng chứng hai phiên desktop đăng nhập khác nhau.

Quyền quản trị nằm trong bảng riêng do quản trị cơ sở dữ liệu cấp. Profile công khai không có email; client không được tự sửa role/bộ đếm. Không nhập service-role key vào app. Không tự đăng dữ liệu local cũ lên cloud.

## Giới hạn bằng chứng

Bộ kiểm thử mới kiểm tra hành vi và tệp đầu ra trong thư mục tạm, chặn mạng mặc định. Các tuyên bố “28/28”, “100% operational”, tương thích mọi hệ điều hành và AI đã tự nạp skill từ tài liệu cũ không còn là kết luận nghiệm thu.
