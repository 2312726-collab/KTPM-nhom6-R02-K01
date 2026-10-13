# BÁO CÁO CÔNG VIỆC CÁ NHÂN: TRẦN NGỌC BẢO PHƯỚC

> **Môn học:** Kiểm thử phần mềm | **Học kỳ:** Đồ án Giữa kỳ  
> **Họ và tên:** Trần Ngọc Bảo Phước  
> **Mã số sinh viên (MSSV):** `2312719`  
> **Nhóm thực hiện:** Nhóm 6  
> **Tổ hợp đề tài:** **Mealie (R02 - v3.28.0)** + **Property-Based Testing với Hypothesis (K01)**  
> **Vai trò trong nhóm:** **QA Automation Engineer 1 — Test Harness & String Engine Verification**  
> **Báo cáo chuyên môn phụ trách chính:** **Phần F** (Bộ kiểm thử tự động, cấu hình Test Harness & Hướng dẫn tái lập)  
> **Kịch bản Code PBT trực tiếp:** **Property 1 (Idempotence & String Utils)** trong file `tests/unit_tests/test_pbt_string_utils.py`  
> **Kho lưu trữ GitHub:** [https://github.com/2312726-collab/KTPM-nhom6-R02-K01](https://github.com/2312726-collab/KTPM-nhom6-R02-K01)  
> **Nhánh phát triển:** [`2312719-TranNgocBaoPhuoc`](https://github.com/2312726-collab/KTPM-nhom6-R02-K01/tree/2312719-TranNgocBaoPhuoc)

---

## 🎯 1. MỤC TIÊU TRỌNG TÂM CỦA GIỮA KỲ

Giai đoạn giữa kỳ tập trung vào việc hoàn thành **Phần 1: Phân tích hệ thống và thiết lập môi trường (System Analysis & Setup)** kết hợp với việc **Lập kế hoạch áp dụng kỹ thuật kiểm thử nâng cao cho giai đoạn tiếp theo**:

- **Triển khai & Vận hành:** Đóng gói và chạy thành công toàn bộ hệ thống Mealie v3.28.0 trên môi trường máy cá nhân thông qua Docker Compose; thực thi và kiểm chứng 03 luồng nghiệp vụ cốt lõi với dữ liệu mẫu (seed data).
- **Phân tích Kiến trúc & On-boarding:** Khảo sát cây thư mục hai tầng Backend/Frontend, xây dựng sơ đồ kiến trúc C4 Container, mô hình hóa 3 sơ đồ luồng dữ liệu (Data Flow Diagrams), và lập tài liệu On-boarding đảm bảo tính tái lập 100% trên máy sạch.
- **Hoạch định Chiến lược Kiểm thử nâng cao (K01 - PBT):** Thiết lập nền tảng lý thuyết Property-Based Testing với thư viện Hypothesis, khoanh vùng phạm vi kiểm thử theo triết lý Ponytail vào module `mealie/services/parser_services/`, phân tích giả định - rủi ro, và hiện thực bộ kiểm thử PBT Property 1 đạt tiêu chí Pass/Fail 100%.

---

## 📦 2. CÁC NỘI DUNG CỤ THỂ THỰC HIỆN VÀ NỘP (DELIVERABLES)

### a. Demo hệ thống chạy thành công trên máy tính
- **Môi trường vận hành Docker Compose:**
  - Hình ảnh hệ thống: `ghcr.io/mealie-recipes/mealie:v3.28.0` (cố định theo `mealie_version.md`).
  - Ánh xạ cổng dịch vụ: `9925:9000` (truy cập Web UI tại `http://localhost:9925`).
  - Lưu trữ bền vững: Volume `mealie-data:/app/data/` bảo toàn cơ sở dữ liệu SQLite và tài nguyên media.
- **Thực thi và minh chứng 03 luồng nghiệp vụ cốt lõi (kèm Seed Data):**
  1. *Luồng 1 (Recipe Management):* Tạo công thức món ăn `"Pho Bo Ha Noi"` (slug: `pho-bo-ha-noi`, ID: `94e3df6c-7053-4ae4-8efc-987e35ad8d64`) với đầy đủ 4 nguyên liệu mẫu và 3 bước hướng dẫn.
  2. *Luồng 2 (Meal Planning):* Lập kế hoạch bữa ăn tối (dinner) ngày `2026-10-11` gắn liền với công thức phở bò (Meal Plan ID: `1`), hiển thị chính xác trên Meal Calendar.
  3. *Luồng 3 (Shopping List Management):* Tạo danh sách mua sắm `"Đi chợ cuối tuần"` (ID: `1bda8992-a2bd-46e5-93cb-78274287d3ad`), thêm 2 mặt hàng và đánh dấu hoàn thành mặt hàng `"500g Bánh phở tươi"`.

---

### b. Trình bày Sơ đồ kiến trúc & Tài liệu On-boarding
- **Phân tích mã nguồn:** Đọc hiểu và phân tích cấu trúc cây thư mục Mealie (FastAPI backend + Nuxt 4/Vue 3 frontend); nhận diện chính xác các thư viện phụ thuộc cốt lõi (`FastAPI`, `Pydantic`, `SQLAlchemy`, `Uvicorn`, `Nuxt 4`, `Vuetify`, `Axios`).
- **Sơ đồ kiến trúc mức Container / Component (Mô hình C4):** Mô hình hóa phân tầng ranh giới từ Client Layer $\to$ Nuxt 4 SPA $\to$ FastAPI Backend $\to$ Controllers $\to$ Services $\to$ Repositories $\to$ SQLite Database.
- **Sơ đồ luồng dữ liệu (Data Flow Diagrams):** Xây dựng sơ đồ tuần tự (Sequence Diagrams) chi tiết từ giao diện người dùng xuống cơ sở dữ liệu cho cả 3 nghiệp vụ: Recipe Management, Meal Planning, và Shopping List.
- **Tài liệu On-boarding:** Soạn thảo tài liệu hướng dẫn khởi động 3 bước chi tiết tại `Documents/Bao_cao_cong_viec_Phuoc/HUONG_DAN_KHOI_DONG.md`, đảm bảo bất kỳ ai từ máy sạch chỉ cần 1 lệnh `docker compose up -d` là dựng lại toàn bộ hệ thống.

---

### c. Báo cáo kế hoạch áp dụng kỹ thuật kiểm thử nâng cao (K01 - PBT)
- **Cơ sở lý thuyết:** Trình bày nguyên lý sinh dữ liệu tự động, kiểm tra tính chất bất biến (Invariant), ưu thế tìm kiếm ca biên (Edge cases) và cơ chế thu hẹp phản ví dụ (Shrinking) của thư viện `Hypothesis`.
- **Xác định phạm vi (Scope):** Giới hạn chặt chẽ theo triết lý Ponytail vào module xử lý chuỗi và phân số `mealie/services/parser_services/parser_utils/string_utils.py`, cô lập khỏi sự phụ thuộc vào database và UI.
- **Giả định & Rủi ro:** Xây dựng cơ chế nạp module thông minh (`importlib.util` / fallback) cho phép chạy test độc lập; giải quyết rủi ro flaky test bằng 3 Hypothesis Profiles (`dev`, `ci`, `thorough`).
- **Tiêu chí đánh giá (Pass/Fail) & Thiết kế Properties:** Thiết kế và hiện thực thành công 7 hàm kiểm thử tự động PBT:
  - *Tính lũy đẳng (Idempotence):* $f(f(s)) = f(s)$ cho `remove_footnote_markers`, `move_parens_to_end`, `convert_vulgar_fractions_to_regular_fractions`.
  - *Tính bền bỉ (Crash-free):* Hàm không bao giờ quăng Unhandled Exception với mọi chuỗi `st.text()`.
  - *Tính hoàn chỉnh (Completeness):* Không còn ký tự phân số unicode sau chuyển đổi.
  - *Bảo toàn định lượng:* Giá trị số học của hỗn số và phân số được bảo toàn trong sai số $\epsilon \le 10^{-4}$.
  - *Kết quả thực thi:* Đạt **100% (7/7 Tests Passed)** trong 3.69 giây.

---

## 📋 3. BẢNG TỔNG KẾT ĐÓNG GÓP THEO PHÂN CÔNG NHIỆM VỤ (P1 $\to$ P4)

| Nhóm việc | Nội dung thực hiện | Sản phẩm bàn giao | Trạng thái |
| :---: | :--- | :--- | :---: |
| **P1** | Phân tích module `string_utils.py` và hỗ trợ giữa kỳ | `Documents/Bao_cao_cong_viec_Phuoc/PHAN_TICH_HE_THONG_VA_KIEN_TRUC.md` | **Hoàn thành** |
| **P2** | Thiết lập Test Harness, Docker Compose & Pytest/Hypothesis | `docker-compose.yml`, `pytest.ini`, `tests/conftest.py` | **Hoàn thành** |
| **P3** | Lập trình kiểm thử PBT Property 1 (7 hàm test PBT) | `tests/unit_tests/test_pbt_string_utils.py` | **Hoàn thành** |
| **P4** | Biên soạn hướng dẫn thực thi, tái lập & báo cáo Phần F | `tests/README.md`, `HUONG_DAN_KHOI_DONG.md`, `BAO_CAO_CONG_VIEC.md` | **Hoàn thành** |
