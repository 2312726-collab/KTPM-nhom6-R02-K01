# BẢNG THEO DÕI TIẾN ĐỘ CÁ NHÂN — THÀNH VIÊN 3: BÙI TRUNG HIẾU
## ĐỒ ÁN MÔN HỌC: KIỂM THỬ PHẦN MỀM — NHÓM 6
* **Họ và tên:** Bùi Trung Hiếu
* **MSSV:** 2312695 *(GitHub username: `2312611-Hieu`)*
* **Vai trò trong nhóm:** Test Architect & PBT Methodology Specialist
* **Nhánh Git làm việc riêng:** `2312611-Hieu`
* **Giai đoạn trọng tâm:** **PHẦN 1 — Phân tích hệ thống và thiết lập môi trường (Mốc Giữa kỳ 20/10)**

---

### 1. PHẠM VI NHIỆM VỤ ĐƯỢC PHÂN CÔNG TRONG PHẦN 1 (MỐC 20/10)

Căn cứ vào đề cương giảng viên (`ban_phan_cong_de_tai.md`), quy tắc dự án (`quy_tac_du_an.md`) và bảng phân công nguyên tử (`phan_cong_nhiem_vu_thanh_vien.md`), thành viên **Bùi Trung Hiếu** phụ trách đúng 1 nhóm công việc trong Phần 1:

👉 **NHÓM VIỆC H1: KHẢO SÁT MODULE, ĐỀ CƯƠNG GIỮA KỲ & THẨM ĐỊNH PHẦN C (Hạn chót: 18/10)**

---

### 2. CHI TIẾT TỪNG ĐẦU VIỆC, TRẠNG THÁI & BẰNG CHỨNG THỰC TẾ

| Mã đầu việc | Nội dung công việc được giao | Trạng thái | Bằng chứng thực nghiệm / Kết quả kiểm tra thực tế | Sản phẩm bàn giao |
| :---: | :--- | :---: | :--- | :--- |
| **H1.1.1** | Đọc và khảo sát cấu trúc module `mealie/services/parser_services/`. | **[x] ĐẠT** | Đã đối chiếu trực tiếp mã nguồn Mealie `v3.28.0` (commit SHA `0552eaa4a80031b8572849cca0ed95d07f1be001`) trong thư mục `mealie_src`. Cấu trúc module gồm: `_base.py`, `ingredient_parser.py`, `brute/`, `openai/`, `parser_utils/string_utils.py`, `parser_utils/unit_utils.py`. | Mục 2 trong đề cương giữa kỳ |
| **H1.1.2** | Xác định phạm vi kiểm thử: 3 file cốt lõi. | **[x] ĐẠT** | Xác định chính xác 3 file ranh giới theo triết lý Ponytail: <br/>1. `ingredient_parser.py` (Lớp `BruteForceParser.parse_one()` xử lý bất đồng bộ `async def`).<br/>2. `parser_utils/string_utils.py` (Xử lý chuỗi, footnote, ngoặc, phân số Unicode).<br/>3. `parser_utils/unit_utils.py` (Lớp `UnitConverter` dùng `pint.UnitRegistry`). | Bảng phân tích rủi ro trong đề cương |
| **H1.1.3** | Soạn thảo Đề cương Kế hoạch kiểm thử PBT sơ bộ nộp Trưởng nhóm Quân đưa vào Báo cáo Giữa kỳ. | **[x] ĐẠT** | Hoàn thành tài liệu đề cương đạt chuẩn yêu cầu mốc 20/10: Bản chất PBT vs EBT, 4 bước vận hành Hypothesis, phạm vi module mục tiêu, ma trận 5 properties dự kiến, tiêu chí Pass/Fail và quản lý rủi ro Flaky test. | File `Documents/de_cuong_kiem_thu_pbt_giua_ky.md` |
| **H1.2.1** | Tiếp nhận tài liệu On-boarding (`bao_cao_phan_C.md` / cấu hình Docker) từ Nam. | **[x] ĐẠT** | Tiếp nhận cấu hình `docker-compose.yml`, `mealie_docker/` và tài liệu hướng dẫn dựng Mealie của bạn Nam. | Biên bản thẩm định chéo |
| **H1.2.2** | Cài đặt thử nghiệm Mealie từ đầu trên máy cá nhân theo đúng từng dòng lệnh trong tài liệu. | **[x] ĐẠT** | Đã thực thi kiểm tra môi trường thực tế từ máy sạch:<br/>- Python 3.14.0 64-bit.<br/>- Khởi tạo `.venv` và cài đặt `requirements-test.txt`.<br/>- Kiểm tra runner Pytest: `pytest 8.4.2` hoạt động tốt.<br/>- Kiểm tra Docker engine: Container nền đang chạy phát hiện nguy cơ xung đột cổng. | Mục 1 trong biên bản thẩm định |
| **H1.2.3** | Lập biên bản phản hồi (lỗi phát sinh, lệnh còn thiếu) gửi lại Nam cập nhật. | **[x] ĐẠT** | Ghi nhận 3 phát hiện kỹ thuật thực tế:<br/>1. Xung đột cổng 9000 (do MinIO `culinaryblog-minio` đang chiếm port 9000 trên máy; khuyến nghị chuyển sang port `9925`).<br/>2. Thiếu phụ thuộc `pint>=0.23` trong `requirements-test.txt` khi test `UnitConverter`.<br/>3. Cảnh báo quyền ghi SQLite trên bind-mount volume Windows (khuyến nghị giữ Docker Named Volume). | File `Documents/bien_ban_tham_dinh_cheo_onboarding.md` |
| **H1.2.4** | Đóng gói sản phẩm Phần 1, commit và push lên nhánh `2312611-Hieu`. | **[x] ĐẠT** | Commit `6d3279b` trên nhánh `2312611-Hieu`: `docs: outline midterm PBT test strategy and cross-validate onboarding`. | Nhánh `2312611-Hieu` trên GitHub |

---

### 3. CÁC CÔNG VIỆC CHỜ THẨM ĐỊNH PHỐI HỢP TRONG NHÓM

1. **Chờ Trưởng nhóm Trần Quốc Quân:**
   - Tiếp nhận nội dung từ `Documents/de_cuong_kiem_thu_pbt_giua_ky.md` để đưa vào cuốn Báo cáo Giữa kỳ chung (`Documents/bao_cao_giua_ky.md`) và slide thuyết trình mốc 20/10.
2. **Chờ bạn Nguyễn Phạm Phú Nam:**
   - Tiếp thu các phản hồi kỹ thuật trong `Documents/bien_ban_tham_dinh_cheo_onboarding.md` để cập nhật cấu hình cổng `9925:9000` và bổ sung `pint` vào tài liệu Phần C trước khi nộp giữa kỳ.

---

### 4. GHI CHÚ RANH GIỚI VÀ PHÂN ĐỊNH GIAI ĐOẠN

- **Phần 1 (Giữa kỳ — Mốc 20/10):** Đã hoàn tất 100% các yêu cầu kỹ thuật và bàn giao đầy đủ sản phẩm. Chốt Phần 1 tại đây.
- **Phần 2 (Cuối kỳ — Tháng 12):** Các file mã nguồn và báo cáo thuộc Giai đoạn 2 (`bao_cao_phan_D.md`, `bao_cao_phan_E.md`, `test_pbt_unit_converter.py`) đã chuẩn bị trước trên nhánh `2312611-Hieu` được giữ nguyên trạng thái, hoàn toàn độc lập và không đưa vào nghiệm thu sớm của Phần 1. Không tự ý triển khai thêm cho đến khi có yêu cầu tiếp theo.
