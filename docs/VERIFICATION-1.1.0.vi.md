# Nghiệm thu AbyssalSkillsD 1.1.0

Ngày kiểm tra: 01/11/2026. Nhánh `codex/reliable-windows-cloud`, nguồn gốc `b7e2ad3`. Đây là báo cáo chứng cứ, không phải tuyên bố mọi chức năng đã hoàn tất nghiệm thu.

## Bằng chứng đã chạy

- 30 kiểm thử độc lập qua `python tests/test_verification.py`: fixture tạm cho home/data/workspace/log, chặn kết nối mạng mặc định. Có kiểm tra tệp thực, junction Windows, lỗi backup/lưu, diff lỗi thời, reference, hủy batch, lưu đồng thời, OAuth sai lượt, refresh thất bại, Credential Manager thật và hợp đồng cloud bằng mock. Các test mock không chứng minh dịch vụ cloud hoạt động.
- PyWebView/WebView2 thật trên Windows: vào thư viện, tìm kiếm, Studio lưu, xem Markdown chứa HTML được escape; đăng nhập GitHub PKCE và nhận quyền admin từ server.
- Supabase thật `ldzgwlvhbomjmonxutyc`: backup trước migration; chạy migration kèm kiểm thử A/B/ẩn danh trong transaction rollback, sau đó áp dụng migration + admin đã được chủ dự án xác nhận. Giữ 2 user, 2 profile và 3 báo cáo cũ.
- Quyền A/B/ẩn danh: SQL chạy theo role/JWT claims trong transaction rollback kiểm tra quyền tác giả, chống đổi role, báo cáo/moderation, favorites, cài idempotent và diagnostics idempotent/cooldown. Chưa thay cho hai tài khoản desktop đăng nhập độc lập.
- Đăng bài thử qua Studio tới cloud thật; tiến trình Python ẩn danh độc lập tìm được và cài xuống workspace tạm, đọc lại SKILL.md đúng nội dung. Lượt cài được server xác nhận. Bài thử sau đó được gỡ công khai; không xóa bản đã cài.
- Kiểm tra phụ thuộc qua pip-audit: không phát hiện lỗ hổng trong tập phụ thuộc được kiểm tra tại thời điểm chạy. Đây không phải chứng nhận không có lỗ hổng.

Bằng chứng cục bộ trong `build/verification/`; backup cloud chứa dữ liệu riêng tư, không commit hoặc đóng gói.

## Đối chiếu phát hiện kiểm toán

| Phát hiện / cam kết | Triển khai | Bằng chứng | Kết luận hiện tại |
|---|---|---|---|
| F01 Mở giao diện | Sửa cú pháp components.js | Node parse và native WebView2 | Đã chứng minh mở được nguồn |
| F02 Ghi/xóa an toàn | paths.py kiểm tra ID, traversal, reserved names, liên kết | Test traversal/reference/junction/alias Windows | Đã chứng minh các trường hợp kiểm thử |
| F03 Không mất tùy chỉnh | installer.py snapshot trước ghi, giữ rules chia sẻ, scaffold quản lý theo block | Backup-failure, shared-rule, scaffold tests | Có bảo vệ; không bảo đảm mọi lỗi phần cứng/TOCTOU ngoài tiến trình |
| F04 Studio lưu đúng | storage.py atomic write, lỗi truyền lên; khóa lưu đồng thời | Failed-save, corrupt-registry, concurrent-save, native Studio | Đã chứng minh nguồn |
| F05 Đăng nhập thật | auth.py PKCE nonce/verifier, xác minh user, bỏ demo | GitHub thật, callback sai lượt/refresh-fail unit tests | GitHub đã chứng minh; Google/email chưa đủ nghiệm thu |
| F06 Bảo vệ secret/session | secure_storage.py Credential Manager, public session không token | Credential Manager roundtrip, safe-config/public-session tests | Đã chứng minh Windows trong phạm vi test |
| F07 Lọc chẩn đoán | logger.py sanitizer, telemetry allowlist và preview | Sanitizer/preview tests | Hỗ trợ có điều kiện; bỏ cam kết lọc tuyệt đối |
| F08 Không tự nâng quyền | private.admin_users, RLS/grants/RPC | SQL thật A/B, quyền cột và admin đã xác nhận | Đã chứng minh ranh giới được kiểm thử |
| F09 Chợ cloud thật | community.py RPC, UUID riêng, cache có nhãn, 24/trang | Studio đăng + tiến trình ẩn danh tìm/cài thực | Đã chứng minh luồng cơ bản; hai desktop A/B còn thiếu |
| F10 Telemetry | payload thống nhất, manual send, request ID/cooldown server | Unit + SQL thật; xem mục còn thiếu cho desktop | Đã chứng minh server; nghiệm thu UI đang thực hiện |
| F11 Kết quả đồng bộ | Kết quả từng mục/đích, partial/error/cancelled | Unknown-target và cancel tests | Có điều kiện theo tệp ghi được |
| F12 Trạng thái AI | Chỉ báo hiện diện tệp; không suy ra AI đã nạp | Scan nhiều đích và Aider, native nhãn mới | Đã sửa mức cam kết |
| F13 Graphify | Không số liệu mặc định, phân biệt chưa phân tích/cache/lỗi | Empty-graph test, code review | Chưa nghiệm thu CLI Graphify thực |
| F14 Hồ sơ thật | Profile và số đóng góp server; bỏ số mẫu | GitHub profile thật, RPC/RLS | Chưa nghiệm thu đầy đủ sửa hồ sơ trên desktop |
| F15 Gỡ/diff | Reference/rule theo đích, manifest rule, lưu archive khi gỡ | Reference/diff/stale/uninstall tests | Đã chứng minh các luồng backend |
| F16 Git đúng nguồn | Hash URL và đối chiếu origin trước pull | Code review; cần thêm kho thực nghiệm thu | Có điều kiện, chưa đủ bằng chứng end-to-end |
| F17 Yêu thích | Local persisted; cloud server count | Unit local và SQL cloud | Đã chứng minh backend |
| F18 Cập nhật/phân phối | Commit comparison, unknown thay fake latest; manifest/checksum/allowlist Windows | Kiểm tra build riêng bên dưới | Chưa coi build thành công là setup đã chạy |

## Còn thiếu để hoàn tất kế hoạch

- Google đang Disabled trên Dashboard; cần chủ dự án cấu hình OAuth client hợp lệ. Không tạo provider giả.
- Email đăng ký/xác nhận, hai phiên desktop A/B thực, đổi tài khoản/đăng xuất và mạng lỗi OAuth chưa đủ nghiệm thu toàn trình.
- Kiểm tra portable và setup trong Windows sạch dùng một lần; không chạy installer trên máy chính. macOS/Linux chưa kiểm chứng.
- Graphify CLI chưa chạy; đồ thị repository cũ không phải bằng chứng nguồn mới.
- Diagnostics UI/cloud acceptance và artifact checks được cập nhật theo kết quả thực, không đánh dấu hoàn tất trước khi chạy.

## Kiểm tra thủ công

1. Mở app, chọn dự án thử, tìm một skill, cài vào workspace. Xem vị trí tệp và hướng dẫn kiểm tra riêng trong AI.
2. Sửa reference ngoài app, mở diff đúng tệp/đích; sửa thêm sau khi mở diff phải bị từ chối áp dụng bản cũ.
3. Studio lưu local phải đọc lại được; khi thư mục không ghi được, giữ nội dung để thử lại.
4. Đăng nhập GitHub, đăng bài; phiên khác tải lại chợ, tìm/cài; chủ bài sửa/gỡ, người khác không được sửa/gỡ.
5. Chẩn đoán: xem trước, kiểm tra nội dung rồi bấm gửi; lỗi giữ nút thử lại và cùng request ID. Không có tác vụ gửi tự động.
