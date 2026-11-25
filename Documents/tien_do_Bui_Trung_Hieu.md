# BẢNG THEO DÕI TIẾN ĐỘ CÁ NHÂN — THÀNH VIÊN 3: BÙI TRUNG HIẾU
## ĐỒ ÁN MÔN HỌC: KIỂM THỬ PHẦN MỀM — NHÓM 6
* **Họ và tên:** Bùi Trung Hiếu
* **MSSV:** `2312611` *(GitHub username: `2312611-Hieu`)*
* **Vai trò trong nhóm:** Test Architect & PBT Methodology Specialist
* **Nhánh Git làm việc riêng:** `2312611-Hieu`
* **Giai đoạn trọng tâm:** **PHẦN 1 — Phân tích hệ thống và thiết lập môi trường (Mốc Giữa kỳ 20/10)**

---

### 1. PHẠM VI NHIỆM VỤ ĐƯỢC PHÂN CÔNG TRONG PHẦN 1 (MỐC 20/10)

Căn cứ vào đề bài của Giảng viên (`ban_phan_cong_de_tai.md`), quy tắc dự án (`quy_tac_du_an.md`) và bảng phân công nguyên tử (`phan_cong_nhiem_vu_thanh_vien.md`), thành viên **Bùi Trung Hiếu** phụ trách đúng 1 nhóm công việc trong Phần 1:

👉 **NHÓM VIỆC H1: KHẢO SÁT MODULE, ĐỀ CƯƠNG GIỮA KỲ & THẨM ĐỊNH PHẦN C (Hạn chót: 18/10)**

---

### 2. CHI TIẾT TỪNG ĐẦU VIỆC, TRẠNG THÁI & BẰNG CHỨNG THỰC TẾ

| Mã đầu việc | Nội dung công việc được giao | Trạng thái | Bằng chứng thực nghiệm / Kết quả kiểm tra thực tế | Sản phẩm bàn giao |
| :---: | :--- | :---: | :--- | :--- |
| **H1.1.1** | Đọc và khảo sát cấu trúc module `mealie/services/parser_services/`. | **[x] ĐẠT** | Đã đối chiếu trực tiếp mã nguồn Mealie `v3.28.0` (commit SHA `0552eaa4a80031b8572849cca0ed95d07f1be001`) trong thư mục `mealie_src`. Cấu trúc module gồm: `_base.py`, `ingredient_parser.py`, `brute/`, `openai/`, `parser_utils/string_utils.py`, `parser_utils/unit_utils.py`. | Mục 2 trong đề cương giữa kỳ |
| **H1.1.2** | Xác định phạm vi kiểm thử: 3 file cốt lõi. | **[x] ĐẠT** | Xác định chính xác 3 file ranh giới theo triết lý Ponytail: <br/>1. `ingredient_parser.py` (Lớp `BruteForceParser.parse_one()` xử lý bất đồng bộ `async def`).<br/>2. `parser_utils/string_utils.py` (Xử lý chuỗi, footnote, ngoặc, phân số Unicode).<br/>3. `parser_utils/unit_utils.py` (Lớp `UnitConverter` dùng `pint.UnitRegistry`). | Bảng phân tích rủi ro trong đề cương |
| **H1.1.3** | Soạn thảo Đề cương Kế hoạch kiểm thử PBT sơ bộ nộp Trưởng nhóm Quân đưa vào Báo cáo Giữa kỳ. | **[x] ĐẠT** | Hoàn thành tài liệu đề cương đạt chuẩn yêu cầu mốc 20/10: Bản chất PBT vs EBT, 4 bước vận hành Hypothesis, phạm vi module mục tiêu, ma trận 5 properties dự kiến, tiêu chí Pass/Fail và quản lý rủi ro Flaky test. | File `Documents/de_cuong_kiem_thu_pbt_giua_ky.md` |
| **H1.2.1** | Tiếp nhận tài liệu On-boarding từ Nam trên nhánh `2312695-NguyenPhamPhuNam-Phan1`. | **[x] ĐẠT** | Đã tiếp nhận và đối chiếu commit SHA `600a16ebf66cbb167dde9c6b832adc3afa2df77f` của Nam (gồm `Documents/bao_cao_phan_C.md`, `mealie_docker/docker-compose.yml`, `mealie_docker/seed/`). | Biên bản thẩm định chéo Mục 1 |
| **H1.2.2** | Cài đặt thử nghiệm Mealie từ đầu trên máy cá nhân theo đúng từng dòng lệnh trong tài liệu Nam. | **[ ] ĐÃ THỬ** | Đã thử, bị chặn do Docker; chưa cài đặt thành công ở lần chạy đầu. Sau đó đã thực nghiệm kỹ thuật cài bằng Docker Compose trên dữ liệu riêng, kiểm tra khởi động, truy cập 200 OK, thiết lập admin theo đúng thứ tự tài liệu, đăng nhập và seed data thành công. Giữ trạng thái `[ ]` chờ hoàn tất thẩm định cài đặt thực tế chính thức. | Biên bản thẩm định chéo Mục 2 |
| **H1.2.3** | Lập biên bản phản hồi (lỗi phát sinh, bước đạt, bước chưa thực hiện) gửi lại Nam cập nhật. | **[x] ĐẠT** | Hoàn thành biên bản thẩm định trung thực, chi tiết: xác nhận bỏ kiến nghị đổi cổng (vì Nam đã cấu hình 9925:9000), tách biệt dependency test `pint` khỏi Docker Mealie, ghi nhận hướng dẫn khắc phục sự cố Docker Daemon và kết quả thực nghiệm. | File `Documents/bien_ban_tham_dinh_cheo_onboarding.md` |
| **H1.2.4** | Đóng gói sản phẩm Phần 1, commit và push lên nhánh `2312611-Hieu`. | **[x] ĐẠT** | Commit trên nhánh `2312611-Hieu` và push lên GitHub đầy đủ. | Nhánh `2312611-Hieu` trên GitHub |

---

### 3. CÁC CÔNG VIỆC CHỜ THẨM ĐỊNH PHỐI HỢP TRONG NHÓM

1. **Chờ Trưởng nhóm Trần Quốc Quân:**
   - Tiếp nhận nội dung từ `Documents/de_cuong_kiem_thu_pbt_giua_ky.md` để đưa vào cuốn Báo cáo Giữa kỳ chung (`Documents/bao_cao_giua_ky.md`) và slide thuyết trình mốc 20/10.
2. **Chờ bạn Nguyễn Phạm Phú Nam:**
   - Tiếp nhận biên bản phản hồi thẩm định chéo tại `Documents/bien_ban_tham_dinh_cheo_onboarding.md`.

---

### 4. GHI CHÚ RANH GIỚI VÀ PHÂN ĐỊNH GIAI ĐOẠN

- **Phần 1 (Giữa kỳ — Mốc 20/10):** Đã rà soát tài liệu H1; còn chờ hoàn tất xác nhận chính thức mục `H1.2.2` với Nam.
- **Phần 2 (Cuối kỳ — Tháng 12):** Đã hoàn thiện đầy đủ trên nhánh `2312611-Hieu`:
  - **H2 (`Documents/bao_cao_phan_D.md`):** Đủ `D.1`–`D.9` (đã bổ sung `H2.2.3b` Entry/Exit Criteria và `H2.2.3c` Ma trận Defect Severity S1→S4 chuẩn IEEE 1044 / ISTQB).
  - **H3 (`Documents/bao_cao_phan_E.md`):** Đủ ma trận 5 Properties kèm phân loại Priority High/Medium/Low (`H3.1.0`) và đặc tả đồng bộ module thật (`shopping_lists.py`, `unit_utils.py`); còn mục `H3.1.5b` chờ xác nhận họp Review chéo 5 thành viên.
  - **H4 (`tests/unit_tests/test_pbt_unit_converter.py`):** Đã hoàn thiện `H-FIX-1` → `H-FIX-4` (gắn `@pytest.mark.pbt`, bỏ `or True`, sửa `_resolve_ounce`, bổ sung `merge()` và `merge_quantity_and_unit()`), đạt **13/13 PASSED** và **99% coverage** `unit_utils.py`.
  - **Kiểm thử chéo `tests/README.md`:** Đã cài `requirements-test.txt` vào `.venv` và chạy toàn bộ `tests/unit_tests/` (64 test cases: **62 passed, 2 xfailed**, 0 lỗi collect). *Lưu ý:* Trên Windows PowerShell, lệnh dùng wildcard `test_pbt_*.py` không tự bung tham số như Linux bash, nên chạy `pytest tests/unit_tests/ -v` hoặc chỉ định từng file.
