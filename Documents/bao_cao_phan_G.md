# BÁO CÁO PHẦN G — KẾT QUẢ THỰC THI KIỂM THỬ, ĐỘ BAO PHỦ VÀ PHÂN TÍCH LỖI (DEFECT LOG & RCA)

**Dự án mục tiêu:** Mealie `v3.28.0` (Commit SHA: `0552eaa4a80031b8572849cca0ed95d07f1be001`)  
**Kỹ thuật áp dụng:** Property-Based Testing (PBT) với thư viện `Hypothesis`  
**Người phụ trách chính:** Võ Hùng Mạnh (`2312687`) — QA Automation Engineer 2 & Defect Analyst  

---

## 1. Kết quả thực thi bộ kiểm thử tự động

Sau khi hoàn thiện cô lập môi trường phụ thuộc trên Python 3.13.2 (`.venv`) và gắn `@pytest.mark.xfail(strict=True)` cho các lỗi thật đã xác minh của Mealie `v3.28.0`:

* **Chạy nhóm 4 tệp PBT (`P1`, `P2`, `P3`, `P5`):**
  * Lệnh: `pytest tests/unit_tests/test_pbt_string_utils.py tests/unit_tests/test_pbt_unit_converter.py tests/unit_tests/test_pbt_ingredient_parser.py tests/unit_tests/test_pbt_fraction.py -v`
  * Kết quả: **48 passed, 4 xfailed in 31.38s** (0 errors, 0 failed).
* **Chạy riêng `P4` (`test_pbt_scaling.py`):**
  * Kết quả: **10 passed, 1 xfailed** (ghim lỗi `DEF-01` tại `shopping_lists.py:403`).

---

## 2. Kết quả đo lường độ bao phủ mã nguồn (Code Coverage)

Đo trực tiếp trên mã nguồn thật `mealie_src/mealie/` bằng `pytest-cov`:

| Module mã nguồn Mealie `v3.28.0` | Tổng Statements | Miss | Độ phủ (Coverage) | Ghi chú |
| :--- | :---: | :---: | :---: | :--- |
| `mealie/services/parser_services/parser_utils/string_utils.py` | 56 | 0 | **100%** | Bao phủ toàn diện bởi `P1` + `P5` |
| `mealie/services/parser_services/parser_utils/unit_utils.py` | 81 | 1 | **99%** | Bao phủ bởi `P2` |
| `mealie/services/parser_services/_base.py` | 117 | 9 | **92%** | Bao phủ bởi `P3` & `M1` |
| `mealie/schema/recipe/recipe_ingredient.py` | 322 | 53 | **84%** | Bao phủ bởi `P4` & `P3` |
| `mealie/services/parser_services/brute/process.py` | 136 | 37 | **73%** | Bao phủ bởi `P3` (`BruteForceParser`) |
| `mealie/services/parser_services/ingredient_parser.py` | 168 | 111 | **34%** | Bao phủ phần `BruteForceParser` (phần còn lại là `OpenAIParser`, `NLPParser`) |
| `mealie/services/household_services/shopping_lists.py` | 294 | 235 | **20%** | Tập trung đúng vào logic scaling (`dòng 323–418`) |

---

## 3. Hồ sơ lỗi thật phát hiện trên Mealie `v3.28.0` (Defect Log & RCA)

| Mã Defect | Mức độ | Vị trí trong Mealie `v3.28.0` | Mô tả hiện tượng & Phản ví dụ | Nguyên nhân gốc (Root Cause) & Đề xuất vá | Trạng thái ghim Test |
| :---: | :---: | :--- | :--- | :--- | :--- |
| **DEF-01** | **S2** (Major) | `mealie/services/household_services/shopping_lists.py:403` | Khi thêm công thức vào Shopping List với `scale != 1`, nếu có 2 dòng nguyên liệu trùng khớp (`1 cup sugar` và `2 cup sugar`), dòng 2 bị cộng thẳng không nhân `scale`. | Nhánh cập nhật gộp viết `existing_item.quantity += ingredient.quantity` thiếu `* scale`.<br>**Đề xuất vá:** Sửa thành `existing_item.quantity += ingredient.quantity * scale`. | Đã ghim `@pytest.mark.xfail(strict=True)` trong `test_pbt_scaling.py` |
| **DEF-02** | **S3** (Minor) | `mealie/services/parser_services/parser_utils/string_utils.py:9-20` | Gọi `move_parens_to_end()` liên tiếp trên `"1 (aa) (bb) "` làm đảo vị trí ngoặc và nhân đôi khoảng trắng vô hạn. | Regex không kiểm tra ngoặc đã ở cuối chuỗi hay chưa.<br>**Đề xuất vá:** Dùng regex không trùng lặp hoặc kiểm tra điểm dừng. | Đã ghim `@pytest.mark.xfail(strict=True)` trong `test_pbt_string_utils.py` |
| **DEF-03** | **S1** (Critical) | `mealie/services/parser_services/brute/process.py:152` | `BruteForceParser.parse_one("")` hoặc `"   "` ném `IndexError: list index out of range`. | Truy cập `tokens[0]` tại dòng 152 khi danh sách `tokens` rỗng.<br>**Đề xuất vá:** Thêm `if not tokens: return ...` ngay đầu hàm. | Đã ghim `@pytest.mark.xfail(strict=True)` trong `test_pbt_ingredient_parser.py` |
| **DEF-04** | **S3** (Minor) | `mealie/schema/recipe/recipe_ingredient.py:372-374` | `_format_quantity_for_display()` chạy chậm $O(N)$ khi định lượng lớn. | Dùng vòng `while` trừ dần thay vì chia lấy nguyên `//`.<br>**Đề xuất vá:** Thay bằng `qty.numerator // qty.denominator`. | Đã xác minh trong mã nguồn |
| **DEF-05** | **S3** (Minor) | `mealie/core/settings/settings.py:29` | Import `mealie.schema.recipe` trên Python $\le 3.13$ văng `NameError: ScraperProxyMode`. | Thiếu `from __future__ import annotations` (chỉ chạy nhờ PEP 649 trên Python 3.14+). | Đã cô lập trong `conftest.py` và các file test |
