# PHẦN E: THIẾT KẾ CHI TIẾT KỊCH BẢN KIỂM THỬ PROPERTY-BASED TESTING (5 PROPERTIES)
## ĐỒ ÁN MÔN HỌC: KIỂM THỬ PHẦN MỀM — NHÓM 6
* **Hệ thống mục tiêu (R02):** [Mealie v3.28.0](https://github.com/mealie-recipes/mealie)
* **Kỹ thuật kiểm thử (K01):** Property-Based Testing (PBT) với `Hypothesis`
* **Người thiết kế (Test Architect):** **Bùi Trung Hiếu** *(MSSV: 2312611)*
* **Tài liệu bàn giao căn cứ:** Dành cho toàn bộ 5 thành viên nhóm thực hiện lập trình kiểm thử độc lập (Sprint 4)

---

### E.1. TỔNG QUAN MA TRẬN 5 KỊCH BẢN KIỂM THỬ CHUẨN HÓA

Nhóm 6 xây dựng 5 kịch bản kiểm thử PBT độc lập, phân bổ đều cho 5 thành viên, bao phủ toàn bộ các góc cạnh xử lý dữ liệu của Mealie:

| Mã | Tên tính chất kiểm thử (Property) | Loại bất biến | Module mục tiêu trong Mealie | Thành viên phụ trách | File mã nguồn kiểm thử |
| :---: | :--- | :--- | :--- | :---: | :--- |
| **P1** | **Tính lũy đẳng khi làm sạch chuỗi (String Idempotence)** | Idempotence: $f(f(x)) == f(x)$ | `mealie/services/parser_services/parser_utils/string_utils.py` | Trần Ngọc Bảo Phước | `tests/unit_tests/test_pbt_string_utils.py` |
| **P2** | **Tính bảo toàn hai chiều khi đổi đơn vị (Unit Round-trip)** | Round-trip: $f^{-1}(f(x)) \approx x$ | `mealie/services/parser_services/parser_utils/unit_utils.py` | **Bùi Trung Hiếu** | `tests/unit_tests/test_pbt_unit_converter.py` |
| **P3** | **Tính bền vững bất khả sập (Parser Crash-free Invariant)** | Robustness / Crash-free | `mealie/services/parser_services/ingredient_parser.py` | Võ Hùng Mạnh | `tests/unit_tests/test_pbt_ingredient_parser.py` |
| **P4** | **Tính đơn điệu khi nhân tỉ lệ khẩu phần (Scaling Monotonicity)** | Monotonicity & Reversibility | `mealie/services/recipe/recipe_service.py` & Schema | Trần Quốc Quân | `tests/unit_tests/test_pbt_scaling.py` |
| **P5** | **Tính bảo toàn giá trị phân số (Fraction Normalization)** | Numeric Preservation | `mealie/services/parser_services/parser_utils/string_utils.py` | Nguyễn Phạm Phú Nam | `tests/unit_tests/test_pbt_fraction.py` |

---

### E.2. BẢNG ĐẶC TẢ CHI TIẾT PROPERTY 1: TÍNH LŨY ĐẲNG CỦA CHUỖI (PHƯỚC PHỤ TRÁCH)

#### 1. Mô tả bài toán nghiệp vụ
Trong Mealie, khi người dùng nhập chuỗi nguyên liệu hoặc import từ website, hàm `remove_footnote_markers()` loại bỏ dấu sao footnote (ví dụ `"salt*"` $\to$ `"salt"`) và hàm `move_parens_to_end()` di chuyển thông tin trong ngoặc về cuối chuỗi. Các hàm làm sạch dữ liệu này phải có tính chất **lũy đẳng (Idempotent)**: gọi nhiều lần liên tiếp không làm biến đổi thêm dữ liệu.

#### 2. Bảng đặc tả kỹ thuật

| Trường thông tin | Đặc tả chi tiết |
| :--- | :--- |
| **Hàm kiểm thử** | `remove_footnote_markers(ing_str: str) -> str`<br/>`move_parens_to_end(ing_str: str) -> str` |
| **Công thức toán học** | $\forall s \in \text{Domain}_{\text{String}}, \quad f(f(s)) = f(s)$ |
| **Chiến lược sinh mẫu (Strategies)** | `st.text(min_size=0, max_size=500)` bao gồm ký tự ASCII, ký tự Unicode đa ngôn ngữ, dấu hoa thị `*`, dấu ngoặc đơn lồng nhau `()`. |
| **Tiền điều kiện (`assume`)** | Không cần lọc bỏ, chấp nhận mọi chuỗi ký tự hợp lệ của Python. |
| **Hành vi kỳ vọng (Assertion)** | `once = f(s)`<br/>`twice = f(once)`<br/>`assert once == twice` |
| **Ca biên kỳ vọng kiểm tra Shrinking** | Chuỗi toàn dấu sao `"***"`, chuỗi ngoặc rỗng `"()"`, chuỗi có dấu sao xen kẽ khoảng trắng `"salt * * "`. |

---

### E.3. BẢNG ĐẶC TẢ CHI TIẾT PROPERTY 2: TÍNH BẢO TOÀN HAI CHIỀU QUY ĐỔI ĐƠN VỊ (HIẾU PHỤ TRÁCH)

#### 1. Mô tả bài toán nghiệp vụ
Lớp `UnitConverter` sử dụng thư viện `Pint` để thực hiện chuyển đổi các đơn vị đo lường trong công thức nấu ăn. Một hệ thống đo lường vật lý chính xác phải đảm bảo tính chất **bảo toàn hai chiều (Round-trip)**: khi đổi từ đơn vị $A$ sang $B$ rồi đổi ngược lại từ $B$ về $A$, giá trị thu được phải tương đương giá trị ban đầu trong giới hạn sai số dấu phẩy động.

#### 2. Bảng đặc tả kỹ thuật

| Trường thông tin | Đặc tả chi tiết |
| :--- | :--- |
| **Lớp và phương thức** | `UnitConverter.convert(quantity: float, unit: str, to_unit: str) -> tuple[float, Unit]` |
| **Công thức toán học** | Với hai đơn vị tương thích $U_1, U_2$ cùng thứ nguyên:<br/>$| \text{convert}(\text{convert}(Q, U_1, U_2)[0], U_2, U_1)[0] - Q | \le 10^{-4}$ |
| **Chiến lược sinh mẫu (Strategies)** | - Khối lượng: $Q \in \text{st.floats}(\text{min\_value}=0.001, \text{max\_value}=100000, \text{allow\_nan}=\text{False}, \text{allow\_infinity}=\text{False})$<br/>- Cặp đơn vị khối lượng: `("gram", "kilogram")`, `("ounce", "gram")`, `("pound", "kilogram")`<br/>- Cặp đơn vị thể tích: `("milliliter", "liter")`, `("teaspoon", "tablespoon")`, `("fluid_ounce", "cup")` |
| **Tiền điều kiện (`assume`)** | `assume(quantity > 0)` và `assume(converter.can_convert(u1, u2))` |
| **Kiểm tra ngoại lệ (Controlled Exception)** | Khi đổi giữa 2 đơn vị không cùng thứ nguyên (ví dụ: `gram` sang `liter` mà không có tỷ trọng, hoặc đơn vị không tồn tại), hệ thống phải ném ra `pint.DimensionalityError` hoặc `UnitNotFound`, tuyệt đối không phát sinh lỗi bất ngờ. |
| **Ca biên kỳ vọng kiểm tra Shrinking** | Số thực cực nhỏ tiệm cận $0.001$, số lượng cực lớn $100000.0$, các đơn vị có tỷ lệ chuyển đổi vô tỉ. |

---

### E.4. BẢNG ĐẶC TẢ CHI TIẾT PROPERTY 3: TÍNH BỀN VỮNG BẤT KHẢ SẬP (MẠNH PHỤ TRÁCH)

#### 1. Mô tả bài toán nghiệp vụ
Hàm `BruteForceParser.parse_one()` là hàm bất đồng bộ (`async def`) bóc tách chuỗi nguyên liệu tự do thành đối tượng `ParsedIngredient`. Người dùng có thể copy-paste bất kỳ ký tự dị biệt nào từ internet vào ô nhập liệu. Hàm parser này tuyệt đối **không được gây sập server (Zero Unhandled Exception / No HTTP 500)**.

#### 2. Bảng đặc tả kỹ thuật

| Trường thông tin | Đặc tả chi tiết |
| :--- | :--- |
| **Hàm kiểm thử** | `BruteForceParser.parse_one(ingredient_string: str) -> ParsedIngredient` |
| **Công thức bất biến** | $\forall s \in \text{st.text()}, \quad \text{await parse\_one}(s) \not\to \text{Unhandled Exception}$ |
| **Chiến lược sinh mẫu (Strategies)** | `st.text(max_size=500)` kết hợp các ký tự đặc biệt, ký tự điều khiển ASCII, null byte, emoji và bảng chữ cái tượng hình (tiếng Trung, tiếng Ả Rập). |
| **Cơ chế Mock cô lập** | Sử dụng `unittest.mock.MagicMock` giả lập phiên làm việc SQLAlchemy `Session` để cô lập hoàn toàn truy vấn database. |
| **Hành vi kỳ vọng (Assertion)** | Kết quả trả về phải là một instance của `ParsedIngredient` (dù không bóc tách được cũng phải trả về `food` là toàn bộ chuỗi gốc), không ném unhandled exception ra ngoài. |

---

### E.5. BẢNG ĐẶC TẢ CHI TIẾT PROPERTY 4: TÍNH ĐƠN ĐIỆU KHI SCALE KHẨU PHẦN (QUÂN PHỤ TRÁCH)

#### 1. Mô tả bài toán nghiệp vụ
Khi người dùng tăng số phần ăn (ví dụ làm bánh cho 8 người thay vì 4 người), số lượng nguyên liệu phải tăng tỉ lệ thuận (Monotonicity). Khi điều chỉnh trở lại số phần ban đầu, giá trị số lượng phải được khôi phục chính xác (Reversibility).

#### 2. Bảng đặc tả kỹ thuật

| Trường thông tin | Đặc tả chi tiết |
| :--- | :--- |
| **Hàm / Logic kiểm thử** | Thuật toán tỉ lệ số lượng nguyên liệu theo công thức: $Q_{\text{scaled}} = Q \times \text{factor}$ |
| **Công thức toán học** | 1. Đơn điệu: Nếu $\text{factor} > 1.0 \implies Q_{\text{scaled}} > Q$; nếu $\text{factor} < 1.0 \implies Q_{\text{scaled}} < Q$<br/>2. Nghịch đảo: $| (Q_{\text{scaled}} / \text{factor}) - Q | \le 10^{-4}$ |
| **Chiến lược sinh mẫu (Strategies)** | $Q \in \text{st.floats}(\text{min\_value}=0.01, \text{max\_value}=1000.0)$<br/>$\text{factor} \in \text{st.floats}(\text{min\_value}=0.1, \text{max\_value}=10.0)$ |
| **Tiền điều kiện (`assume`)** | `assume(factor > 0 and qty > 0)` |

---

### E.6. BẢNG ĐẶC TẢ CHI TIẾT PROPERTY 5: TÍNH BẢO TOÀN GIÁ TRỊ PHÂN SỐ (NAM PHỤ TRÁCH)

#### 1. Mô tả bài toán nghiệp vụ
Người dùng công thức thường ghi số lượng dưới dạng phân số thông thường (`"1/2"`, `"3/4"`), phân số Unicode ký tự đơn (`"½"`, `"¼"`, `"¾"`), hoặc hỗn số (`"1 1/2"`). Khi bóc tách và chuyển đổi sang số thực, giá trị toán học phải được bảo toàn tuyệt đối không bị mất mát hay làm méo mó giá trị dinh dưỡng.

#### 2. Bảng đặc tả kỹ thuật

| Trường thông tin | Đặc tả chi tiết |
| :--- | :--- |
| **Hàm kiểm thử** | `convert_vulgar_fractions_to_regular_fractions(text: str)` và `extract_quantity_from_string(source_str: str)` trong `string_utils.py` |
| **Công thức toán học** | Với tử số $N \ge 1$, mẫu số $D \ge 1$:<br/>$| \text{parse}(f"{N}/{D}") - (N / D) | \le 10^{-6}$ |
| **Chiến lược sinh mẫu (Strategies)** | $N \in \text{st.integers}(1, 99)$, $D \in \text{st.integers}(1, 99)$<br/>Kèm cặp bảng phân số Unicode ánh xạ: `{"½": 0.5, "¼": 0.25, "¾": 0.75, "⅓": 0.3333...}` |
| **Tiền điều kiện (`assume`)** | `assume(denominator != 0)` |

---

### E.7. KẾ HOẠCH BÀN GIAO VÀ HƯỚNG DẪN VIẾT CODE CHO 5 THÀNH VIÊN (SPRINT 4)

1. **Quy tắc đặt tên file test:**
   Tất cả các file test của 5 thành viên phải đặt tên theo đúng tiền tố chuẩn: `tests/unit_tests/test_pbt_<tên_module>.py`.
2. **Kế thừa Test Fixture:**
   Tất cả test cases tự động kế thừa cấu hình Hypothesis đa profile (`dev`, `ci`, `thorough`) đã thiết lập trong `tests/conftest.py`.
3. **Lệnh thực thi đơn nhất:**
   Chạy riêng từng property:
   ```bash
   pytest tests/unit_tests/test_pbt_<tên>.py -v
   ```
   Chạy đồng thời toàn bộ 5 properties:
   ```bash
   pytest tests/unit_tests/test_pbt_*.py -v
   ```
