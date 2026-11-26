# BÁO CÁO PHẦN G — KẾT QUẢ THỰC THI KIỂM THỬ, ĐỘ BAO PHỦ VÀ PHÂN TÍCH LỖI (DEFECT LOG & RCA)

**Dự án mục tiêu:** Mealie `v3.28.0` (Commit SHA: `0552eaa4a80031b8572849cca0ed95d07f1be001`)  
**Kỹ thuật áp dụng:** Property-Based Testing (PBT) với thư viện `Hypothesis`  
**Người phụ trách chính:** Võ Hùng Mạnh (`2312687`) — QA Automation Engineer 2 & Defect Analyst  

---

## 1. Kết quả thực thi bộ kiểm thử tự động

Bộ kiểm thử hợp nhất đầy đủ 6 tệp (`M1` + `P1` → `P5`) đã được xác thực thành công bằng **1 lệnh duy nhất** trên cả hai môi trường: **Docker Test Runner chuẩn Python 3.14.10** (nạp 100% mã nguồn Mealie thật, không dùng fallback stub) và **Windows Host Python 3.13.2** (`.venv` qua `ensure_mealie_parser_isolated()` tại `tests/conftest.py`):

* **Trên Docker Test Runner (`python:3.14-slim`, Python 3.14.10):**
  * Toàn bộ `tests/` (`docker compose -f docker-compose.test.yml run --rm test-runner pytest tests/ -v --tb=long --cov=...`): **65 passed, 6 xfailed in 53.42s** (0 collection errors, 0 failed).
  * Lọc riêng marker PBT (`pytest -m pbt -v`): **49 passed, 3 xfailed in 50.39s** (52 selected, 19 unit tests deselected; 0 errors, 0 failed).
  * Tái hiện trực tiếp các lỗi đã ghim (`--runxfail`): **6 failed, 1 passed** (xác nhận toàn bộ 6 ca `xfail` đều tái hiện đúng lỗi thật trên `v3.28.0`).
* **Trên Windows Host (`.venv`, Python 3.13.2):**
  * Toàn bộ `tests/unit_tests/` (`pytest tests/unit_tests/ -v`): **65 passed, 6 xfailed in 76.81s** (0 errors, 0 failed).
  * Lọc riêng marker PBT (`pytest -m pbt -v`): **49 passed, 3 xfailed in 34.61s** (0 errors, 0 failed).

---

## 2. Kết quả đo lường độ bao phủ mã nguồn (Code Coverage)

Đo trực tiếp trên mã nguồn thật `mealie_src/mealie/` trong container Docker **Python 3.14.10** bằng `pytest-cov`:

| Module mã nguồn Mealie `v3.28.0` | Tổng Statements | Miss | Độ phủ (Coverage) | Ghi chú |
| :--- | :---: | :---: | :---: | :--- |
| `mealie/services/parser_services/parser_utils/string_utils.py` | 56 | 0 | **100%** | Bao phủ toàn diện bởi `P1` + `P5` |
| `mealie/services/parser_services/parser_utils/unit_utils.py` | 81 | 1 | **99%** | Bao phủ bởi `P2` (chỉ sót dòng 20) |
| `mealie/services/parser_services/_base.py` | 117 | 9 | **92%** | Bao phủ bởi `P3` & `M1` |
| `mealie/schema/recipe/recipe_ingredient.py` | 322 | 51 | **84%** | Bao phủ bởi `P4` & `P3` |
| `mealie/services/parser_services/brute/process.py` | 136 | 36 | **74%** | Bao phủ bởi `P3` (`BruteForceParser`) |
| `mealie/services/parser_services/ingredient_parser.py` | 168 | 111 | **34%** | Bao phủ luồng `BruteForceParser` (phần còn lại là `OpenAIParser`, `NLPParser`) |
| `mealie/services/household_services/shopping_lists.py` | 294 | 227 | **23%** | Tập trung đúng vào logic scaling (`dòng 323–418`) |

---

## 3. Hồ sơ lỗi thật phát hiện trên Mealie `v3.28.0` (Defect Log & RCA)

| Mã Defect | Mức độ | Vị trí trong Mealie `v3.28.0` | Mô tả hiện tượng & Phản ví dụ | Nguyên nhân gốc (Root Cause) & Đề xuất vá | Trạng thái ghim Test |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **DEF-01** | **S2** (Major) | `mealie/services/household_services/shopping_lists.py:403` | Khi thêm công thức vào Shopping List với `scale != 1`, nếu có 2 dòng nguyên liệu trùng khớp (`1 cup sugar` và `2 cup sugar`), dòng 2 bị cộng thẳng không nhân `scale`. | Nhánh cập nhật gộp viết `existing_item.quantity += ingredient.quantity` thiếu `* scale`.<br>**Đề xuất vá:** Sửa thành `existing_item.quantity += ingredient.quantity * scale`. | Đã ghim `@pytest.mark.xfail(strict=True)` trong `test_pbt_scaling.py` |
| **DEF-02** | **S3** (Minor) | `mealie/services/parser_services/parser_utils/string_utils.py:9-20` | Gọi `move_parens_to_end()` liên tiếp trên `"1 (aa) (bb) "` làm đảo vị trí ngoặc và nhân đôi khoảng trắng vô hạn. | Regex không kiểm tra ngoặc đã ở cuối chuỗi hay chưa.<br>**Đề xuất vá:** Dùng regex không trùng lặp hoặc kiểm tra điểm dừng. | Đã ghim `@pytest.mark.xfail(strict=True)` trong `test_pbt_string_utils.py` |
| **DEF-03** | **S1** (Critical) | `mealie/services/parser_services/brute/process.py:152` và `199 -> 110` | `BruteForceParser.parse_one("")`, `"   "` ném `IndexError` tại dòng 152; chuỗi `"a cup"` (khi DB đã có `"cup"`) ném `IndexError: list index out of range` tại `199 -> 110`. | Dòng 152 truy cập `tokens[0]` khi rỗng; dòng 199 cắt `tokens[index+1:]` rỗng truyền vào `parse_ingredient()` rồi truy cập `tokens[-1]` ở dòng 110.<br>**Đề xuất vá:** Chặn `if not tokens: return ...` ngay đầu hàm. | Đã ghim cả 2 nhánh bằng `@pytest.mark.xfail(strict=True)` trong `test_pbt_ingredient_parser.py` |
| **DEF-04** | **S3** (Minor) | `mealie/schema/recipe/recipe_ingredient.py:372-374` | `_format_quantity_for_display()` chạy chậm `O(N)` khi định lượng lớn. | Dùng vòng `while` trừ dần thay vì chia lấy nguyên `//`.<br>**Đề xuất vá:** Thay bằng `qty.numerator // qty.denominator`. | Đã xác minh trong mã nguồn |
| **DEF-05** | **S3** (Minor) | `mealie/core/settings/settings.py:29` | Import `mealie.schema.recipe` trên Python ≤ 3.13 văng `NameError: ScraperProxyMode`. | Thiếu `from __future__ import annotations` (chỉ chạy nhờ PEP 649 trên Python 3.14+). | Đã cô lập trong `tests/conftest.py` (`ensure_mealie_parser_isolated()`) cho Python `< 3.14` |
