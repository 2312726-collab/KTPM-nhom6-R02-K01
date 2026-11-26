# BÁO CÁO PHẦN H — QUẢN TRỊ CẤU HÌNH, TÁI LẬP HỆ THỐNG VÀ TỔNG KẾT NGHIỆM THU

**Dự án mục tiêu:** Mealie `v3.28.0` (Commit SHA: `0552eaa4a80031b8572849cca0ed95d07f1be001`)  
**Kỹ thuật áp dụng:** Property-Based Testing (PBT) với thư viện `Hypothesis`  
**Người phụ trách:** Trần Quốc Quân (`2312726`) — Trưởng nhóm & Kiến trúc sư hệ thống  

---

## 1. Cố định cấu hình & Phiên bản (Configuration Pinning)

* **Hệ thống mục tiêu (SUT):** `mealie_src/` được ghim cứng tại release tag **`v3.28.0`** (SHA `0552eaa4a80031b8572849cca0ed95d07f1be001`), không chỉnh sửa bất kỳ dòng mã nguồn nào của Mealie.
* **Kho lưu trữ kiểm thử:** Nhánh `develop` hợp nhất đầy đủ cả 5 Properties PBT (`P1` → `P5`), hạ tầng Docker Test Runner (`Dockerfile.test`, `docker-compose.test.yml`) và toàn bộ báo cáo `bao_cao_phan_A.md` → `bao_cao_phan_H.md`, đóng gói tại tag **`v1.0-final`**.

---

## 2. Hướng dẫn tái lập 1-click trên máy mới

### Cách 1: Chạy trên Docker Test Runner (Python 3.14.10)
```bash
git clone --branch v3.28.0 --depth 1 https://github.com/mealie-recipes/mealie.git mealie_src
docker compose -f docker-compose.test.yml build test-runner
docker compose -f docker-compose.test.yml run --rm test-runner pytest tests/ -v --tb=long
```

### Cách 2: Chạy trong môi trường ảo Python nội bộ
```powershell
python -m pip install -r requirements-test.txt
python -m pytest tests/unit_tests/test_pbt_string_utils.py tests/unit_tests/test_pbt_unit_converter.py tests/unit_tests/test_pbt_ingredient_parser.py tests/unit_tests/test_pbt_fraction.py -v
python -m pytest tests/unit_tests/test_pbt_scaling.py -v
```

---

## 3. Thống kê giờ công & Đánh giá đóng góp cá nhân (Peer Evaluation)

| STT | MSSV | Họ và tên | Vai trò | Giờ công (giờ) | Tỷ lệ đóng góp | Đánh giá hoàn thành |
| :---: | :---: | :--- | :--- | :---: | :---: | :--- |
| 1 | `2312726` | Trần Quốc Quân | Trưởng nhóm & Kiến trúc sư (P4) | 40 | 20.9% | Hoàn thành 100% |
| 2 | `2312611` | Bùi Trung Hiếu | Test Architect & PBT Specialist (P2) | 39 | 20.4% | Hoàn thành 100% |
| 3 | `2312695` | Nguyễn Phạm Phú Nam | DevOps & Automation QA (P5) | 39 | 20.4% | Hoàn thành 100% |
| 4 | `2312719` | Trần Ngọc Bảo Phước | QA Automation Engineer 1 (P1) | 38 | 19.9% | Hoàn thành 100% |
| 5 | `2312687` | Võ Hùng Mạnh | QA Automation Engineer 2 (P3 & Phần G) | 35 | 18.4% | Hoàn thành 100% (sau khi hỗ trợ fix import) |
| **Tổng** | — | **Nhóm 6** | — | **191 giờ** | **100%** | **Đạt nghiệm thu** |

---

## 4. Bảng kiểm tiêu chí nghiệm thu (Exit Criteria)

| Tiêu chí nghiệm thu | Ngưỡng mục tiêu | Kết quả thực tế | Trạng thái |
| :--- | :--- | :--- | :---: |
| Không lỗi Collection trên môi trường kiểm thử | 0 collection errors | 0 errors trên cả Python 3.13.2 & Docker 3.14 | **ĐẠT** |
| Triển khai đủ 5 Properties PBT độc lập | ≥ 5 tệp `test_pbt_*.py` gắn `@pytest.mark.pbt` | Đủ 5/5 tệp (`P1`, `P2`, `P3`, `P4`, `P5`), không assertion giả | **ĐẠT** |
| Độ phủ mã nguồn trực tiếp trên module mục tiêu | ≥ 80% trên `parser_services` & `recipe_ingredient` | `string_utils` **100%**, `unit_utils` **99%**, `_base.py` **92%**, `recipe_ingredient` **84%** | **ĐẠT** |
| Phát hiện lỗi thật + Phân tích nguyên nhân gốc (RCA) | Có Defect Log & bản vá đề xuất | 5 defects đã xác minh (`DEF-01` → `DEF-05`), ghim `xfail(strict=True)` | **ĐẠT** |
| Đồng bộ tài liệu & Đóng gói Release | Đủ `bao_cao_phan_A..H.md` + tag `v1.0-final` | Đầy đủ `A..H`, gắn tag `v1.0-final` | **ĐẠT** |
