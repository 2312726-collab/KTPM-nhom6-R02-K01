# Phần G — Kết quả kiểm thử 5 Property

Võ Hùng Mạnh · 2312687 · Nhóm 6 · R02/K01

## Phạm vi và môi trường

Chạy năm file `tests/unit_tests/test_pbt_*.py` từ `develop` tại commit `17f81df` trên Mealie v3.28.0, SHA `0552eaa4a80031b8572849cca0ed95d07f1be001`. Lần chạy sử dụng Python 3.14.8, profile Hypothesis `thorough` và seed 0. Trong phiên Windows này, coroutine P3 đã mock I/O được chạy trực tiếp để tránh lỗi tạo socket của asyncio.

## Kết quả

| Property | Pass | XFail |
|---|---:|---:|
| P1 — String Utils | 3 | 1 |
| P2 — Unit Conversion | 13 | 0 |
| P3 — Ingredient Parser | 3 | 4 |
| P4 — Servings Scaling | 10 | 1 |
| P5 — Fraction Normalization | 28 | 0 |
| **Tổng** | **57** | **6** |

63 ca hoàn tất trong 46,59 giây, với 0 Fail. XFail là ca thất bại dự kiến cho lỗi đã biết. Xem [log lần chạy](../logs/coverage_parser_run.txt).

## Độ bao phủ parser

| Mô-đun | Dòng đã chạy | Cover của pytest-cov |
|---|---:|---:|
| `ingredient_parser.py` | 56/168 (33,33%) | 25% |
| `brute/process.py` | 67/136 (49,26%) | 45% |

Cột Cover gộp dòng và nhánh. Độ phủ gộp hai mô-đun là 34%. Mở [Coverage HTML](../logs/coverage_html/index.html) sau khi tải repo về để xem từng dòng và nhánh.

## Defect Log và RCA

| ID | Hiện tượng | Nguyên nhân và minh chứng |
|---|---|---|
| DEF-01 | Gộp nguyên liệu trùng cho ra tổng sai khi đổi khẩu phần. | Nhánh gộp tại `shopping_lists.py:403` cộng lượng của dòng thứ hai trước khi nhân hệ số. XFail P4. |
| DEF-02 | Chuẩn hóa lại chuỗi có nhiều cụm ngoặc làm thay đổi kết quả. | `move_parens_to_end()` xử lý một cụm ngoặc mỗi lượt. XFail P1. |
| DEF-03 | Parser ném `IndexError` với chuỗi rỗng, toàn khoảng trắng và `a cup` khi DB mock có đơn vị `cup`. | `process.py:152` đọc token đầu khi danh sách rỗng. Với `a cup`, dòng 199 truyền phần đuôi rỗng và dòng 110 đọc token cuối. Bốn XFail P3. |
| DEF-04 | Thời gian định dạng lượng có thể tăng tuyến tính theo phần nguyên. | `recipe_ingredient.py:372–374` lặp trừ từng đơn vị. Ghi nhận từ mã nguồn. |
| DEF-05 | Import settings có thể gây `NameError` trên Python 3.13. | Annotation của `ScraperProxyMode._missing_` tham chiếu tên lớp đang được định nghĩa. Đây là lỗi tương thích nhóm ghi nhận, ngoài phạm vi lần chạy Python 3.14.8 này. |
