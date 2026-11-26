# BÁO CÁO PHẦN H — QUẢN TRỊ CẤU HÌNH, TÁI LẬP HỆ THỐNG VÀ TỔNG KẾT NGHIỆM THU

**Dự án mục tiêu:** Mealie `v3.28.0` (Commit SHA: `0552eaa4a80031b8572849cca0ed95d07f1be001`)  
**Kỹ thuật áp dụng:** Property-Based Testing (PBT) với thư viện `Hypothesis`  
**Người phụ trách:** Trần Quốc Quân (`2312726`) — Trưởng nhóm & Kiến trúc sư hệ thống  

---

## 1. Cố định cấu hình & Phiên bản (Configuration Pinning)

* **Hệ thống mục tiêu (SUT):** `mealie_src/` được ghim cứng tại release tag **`v3.28.0`** (SHA `0552eaa4a80031b8572849cca0ed95d07f1be001`), không chỉnh sửa bất kỳ dòng mã nguồn nào của Mealie.
* **Chuẩn Python mục tiêu:** **Python 3.14 (`>=3.14,<3.15`)** theo `mealie_src/pyproject.toml` và `Dockerfile.test` (`python:3.14-slim`). Ngoài ra, `tests/conftest.py` cung cấp hàm `ensure_mealie_parser_isolated()` tự động cô lập tương thích khi chạy trên máy trạm Python `< 3.14`.

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
python -m pytest tests/unit_tests/ --cov=mealie.services.parser_services --cov=mealie.schema.recipe.recipe_ingredient --cov=mealie.services.household_services.shopping_lists -v
python -m pytest -m pbt -v
```

---

## 3. Thống kê giờ công & Đánh giá đóng góp cá nhân (Peer Evaluation)

| STT | MSSV | Họ và tên | Vai trò | Giờ công (giờ) | Tỷ lệ đóng góp | Đánh giá hoàn thành |
| :---: | :---: | :--- | :--- | :---: | :---: | :--- |
| 1 | `2312726` | Trần Quốc Quân | Trưởng nhóm & Kiến trúc sư (`P4`) | 40 | 20.9% | Hoàn thành 100% |
| 2 | `2312611` | Bùi Trung Hiếu | Test Architect & PBT Specialist (`P2`) | 39 | 20.4% | Hoàn thành 100% |
| 3 | `2312695` | Nguyễn Phạm Phú Nam | DevOps & Automation QA (`P5`) | 39 | 20.4% | Hoàn thành 100% |
| 4 | `2312719` | Trần Ngọc Bảo Phước | QA Automation Engineer 1 (`P1`) | 38 | 19.9% | Hoàn thành 100% |
| 5 | `2312687` | Võ Hùng Mạnh | QA Automation Engineer 2 (`P3` & Phần G) | 35 | 18.4% | Hoàn thành 100% |
| **Tổng** | — | **Nhóm 6** | — | **191 giờ** | **100%** | **Đạt nghiệm thu** |

---

## 4. Bảng kiểm tiêu chí nghiệm thu (Exit Criteria)

| Tiêu chí nghiệm thu | Ngưỡng mục tiêu | Kết quả thực tế | Trạng thái |
| :--- | :--- | :--- | :---: |
| Chạy toàn bộ test suite bằng 1 lệnh không lỗi | 0 errors, 0 failed trên cả Docker 3.14 & Host | **65 passed, 6 xfailed** (full) và **49 passed, 3 xfailed** (`-m pbt`) trên cả Docker Python 3.14.10 & Host 3.13.2 | **ĐẠT** |
| Triển khai đủ 5 Properties PBT độc lập | ≥ 5 tệp `test_pbt_*.py` gắn `@pytest.mark.pbt` | Đủ 5/5 tệp (`P1`, `P2`, `P3`, `P4`, `P5`), không assertion giả | **ĐẠT** |
| Độ phủ mã nguồn trực tiếp trên module mục tiêu | ≥ 80% trên `parser_utils` & `recipe_ingredient` | `string_utils` **100%**, `unit_utils` **99%**, `_base.py` **92%**, `recipe_ingredient` **84%** | **ĐẠT** |
| Phát hiện lỗi thật + Phân tích nguyên nhân gốc (RCA) | Có Defect Log & bản vá đề xuất | 5 defects đã xác minh (`DEF-01` → `DEF-05`), ghim `xfail(strict=True)` | **ĐẠT** |
| Đồng bộ tài liệu & Đóng gói Release | Đủ `bao_cao_phan_A..H.md` + báo cáo cuối kỳ + tag release | Đầy đủ `A..H`, [BaoCaoCuoiKy_Nhom6.md](BaoCaoCuoiKy_Nhom6.md), đóng gói tag `v1.1-final` và merge `main` | **ĐẠT** |
