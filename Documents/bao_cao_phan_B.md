# PHẦN B: KIẾN TRÚC HỆ THỐNG VÀ CÁC LUỒNG DỮ LIỆU CỐT LÕI (MEALIE v3.28.0)
## BÁO CÁO ĐỒ ÁN MÔN HỌC KIỂM THỬ PHẦN MỀM — NHÓM 6
* **Tổ hợp đề tài:** R02 (Mealie) — K01 (Property-Based Testing với Hypothesis)
* **Giảng viên hướng dẫn:** ThS. Nguyễn Thế Lâm
* **Sinh viên phụ trách chính Phần B:** Trần Quốc Quân (MSSV: `2312726` — Trưởng nhóm)
* **Phiên bản hệ thống mục tiêu:** Release Tag **`v3.28.0`** (Commit SHA: `0552eaa4a80031b8572849cca0ed95d07f1be001`)

---

## 🏛️ B.1. KIẾN TRÚC TỔNG THỂ HỆ THỐNG (C4 CONTAINER DIAGRAM)

### 1. Giới thiệu mô hình C4 Container
Mô hình C4 (Context, Containers, Components, Code) là một tiêu chuẩn công nghiệp được sử dụng rộng rãi nhằm trực quan hóa kiến trúc phần mềm theo các mức độ trừu tượng khác nhau. Ở cấp độ **Container Diagram (Cấp độ 2)**, mô hình tập trung mô tả:
* Ranh giới thực thi của hệ thống Mealie (`System Boundary`).
* Các khối phần mềm độc lập có thể triển khai hoặc chạy riêng biệt (Web Application, API Server, Database, File Storage).
* Các giao thức mạng, cổng kết nối và định dạng dữ liệu luân chuyển giữa các container.
* Sự tương tác giữa các tác nhân người dùng (**Home User**, **Administrator**) và các hệ thống dịch vụ bên ngoài (**External Recipe Sites**, **SMTP Server**, **AI/LLM Parser**).

---

### 2. Sơ đồ Kiến trúc C4 Container của Mealie v3.28.0

Dưới đây là sơ đồ kiến trúc tổng thể mức C4 Container của hệ thống Mealie:

![Sơ đồ kiến trúc C4 Container của Mealie v3.28.0](assets/kien_truc_container.png)

*Hình B.1: Sơ đồ kiến trúc mức C4 Container của hệ thống Mealie v3.28.0*

---

### 3. Bảng Phân tích và Đặc tả Chi tiết các Container

Dựa trên kết quả khảo sát trực tiếp từ mã nguồn `mealie_src` và tệp đóng gói `docker-compose.yml`, hệ thống được cấu thành bởi các container và phân hệ kỹ thuật sau:

| STT | Tên Container | Công nghệ & Thư viện sử dụng | Trách nhiệm kỹ thuật cốt lõi trong hệ thống | Giao thức / Định dạng giao tiếp |
| :---: | :--- | :--- | :--- | :--- |
| **1** | **Single-Page Application (SPA Frontend)** | `Vue.js 3`, `Nuxt 3`, `TypeScript`, `Pinia`, `Vuetify` | • Hiển thị giao diện đồ họa trực quan trên trình duyệt máy tính và thiết bị di động (PWA).<br>• Tiếp nhận dữ liệu người dùng nhập (chuỗi nguyên liệu, số lượng khẩu phần ăn, kế hoạch bữa ăn).<br>• Gọi API bất đồng bộ tới Backend và cập nhật giao diện mà không cần tải lại toàn bộ trang web. | • **Inbound:** HTTPS từ Web Browser.<br>• **Outbound:** REST API JSON qua HTTP/HTTPS tới Backend. |
| **2** | **API & Application Server (Backend)** | `Python 3.14+`, `FastAPI 0.141.1`, `Uvicorn 0.53.0` | • **Định tuyến REST API:** Cung cấp các endpoint `/api/recipes`, `/api/parser`, `/api/households`, `/api/auth`.<br>• **Tầng dịch vụ (Core Services):** Thực thi các thuật toán bóc tách nguyên liệu (`IngredientParserService`), tính toán nhân chia khẩu phần ăn (`RecipeService`), quản lý danh sách đi chợ.<br>• **Phục vụ SPA tĩnh:** Tự động mount thư mục tĩnh của Frontend qua `SPAStaticFiles` tại đường dẫn gốc `/`.<br>• **Tác vụ ngầm định kỳ:** Tích hợp `APScheduler` tự động dọn dẹp token hết hạn, kiểm tra webhook và đồng bộ sự kiện.<br>• **Xác thực & Kiểm thực:** Áp dụng `SessionMiddleware`, JWT token và `Pydantic V2` cho toàn bộ luồng dữ liệu vào/ra. | • **Inbound:** HTTP/HTTPS trên cổng `9000`.<br>• **Outbound:** Giao tiếp cơ sở dữ liệu qua SQLAlchemy, File I/O, và HTTP Scraper tới Internet. |
| **3** | **Database (RDBMS)** | `SQLite 3` (mặc định) / `PostgreSQL` | • Đảm bảo tính toàn vẹn (ACID) của dữ liệu quan hệ.<br>• Lưu trữ thông tin công thức nấu ăn, định lượng nguyên liệu, bảng quy đổi đơn vị đo lường, tài khoản người dùng và quyền hạn hộ gia đình.<br>• Được quản lý phiên thông qua `SQLAlchemy ORM 2.0` và đồng bộ cấu trúc bằng `Alembic 1.20`. | • **Giao thức:** Nhúng tệp cục bộ (SQLite) hoặc giao thức TCP PostgreSQL (Cổng 5432). |
| **4** | **File Storage (Media Volume)** | Hệ thống tệp Linux / Docker Volume (`/app/data/`) | • Lưu trữ tệp tin nhị phân: hình ảnh minh họa công thức nấu ăn, ảnh đại diện người dùng, bản xuất dữ liệu dự phòng định dạng `.zip`.<br>• Lưu trữ trực tiếp tệp cơ sở dữ liệu `mealie.db` khi sử dụng SQLite. | • **Giao thức:** Direct File System POSIX I/O. |
| **5** | **Hệ thống ngoài (External Services)** | `recipe-scrapers`, `SMTP`, `OpenAI API` | • **recipe-scrapers:** Phân tích mã nguồn HTML/Microdata của các website bên ngoài để tự động trích xuất công thức ẩm thực.<br>• **SMTP:** Phục vụ gửi thư kích hoạt tài khoản hoặc đặt lại mật khẩu người dùng.<br>• **AI / LLM API (Tùy chọn):** Cơ chế dự phòng xử lý bóc tách nguyên liệu đối với các chuỗi văn bản phi cấu trúc hoặc có độ phức tạp cao. | • **Giao thức:** HTTPS GET/POST (Scraper & AI API), SMTP/TLS (Thư điện tử). |

---

### 4. Ý nghĩa Kiến trúc C4 Container đối với Chiến lược Kiểm thử Phần mềm (PBT)
Việc phân rã rõ ràng ranh giới các Container giúp định vị chính xác phạm vi kiểm thử cho Đồ án:
1. **Cô lập logic thuần túy (Pure Logic Isolation):** Các module xử lý bóc tách nguyên liệu (`parser_services/`) và tính toán khẩu phần ăn (`recipe_service.py`) nằm hoàn toàn ở tầng nghiệp vụ của Backend FastAPI. Chúng là các hàm xử lý tính toán dựa trên dữ liệu đầu vào (Input) và trả về kết quả (Output) mà không phụ thuộc cứng vào tầng giao diện Vue hay cơ sở dữ liệu, tạo điều kiện lý tưởng để áp dụng **Property-Based Testing (PBT)** với thư viện **Hypothesis**.
2. **Khả năng kiểm thử hộp trắng độc lập:** Kiểm thử viên có thể import trực tiếp các module Python để sinh hàng nghìn ca kiểm thử ngẫu nhiên theo invariant toán học (như tính đơn điệu Monotonicity, tính bảo toàn nghịch đảo Reversibility) mà không cần phải khởi chạy toàn bộ container Docker hay giả lập trình duyệt nặng nề.

---

## 🔄 B.2. CÁC LUỒNG DỮ LIỆU CỐT LÕI (CORE DATA FLOWS)

### B.2.1. Luồng Dữ liệu 1: Nghiệp vụ bóc tách nguyên liệu ẩm thực (Ingredient Parsing)

#### 1. Bối cảnh và Mục tiêu nghiệp vụ
Trong bài toán quản lý ẩm thực, dữ liệu nguyên liệu ban đầu thường do người dùng nhập thủ công dưới dạng văn bản tự do không cấu trúc (Unstructured text) hoặc được trích xuất từ các trang web nấu ăn. Các chuỗi này mang tính đa dạng rất cao về ngôn ngữ, ký hiệu phân số, đơn vị đo lường và cách diễn đạt, ví dụ:
* `"2 1/2 cups all-purpose flour, sifted"` *(Hỗn số, đơn vị Anh-Mỹ, ghi chú sơ chế)*
* `"1½ tbsp olive oil (extra virgin)"* *(Phân số Unicode, đơn vị muỗng canh, ghi chú trong ngoặc)*
* `"3 large eggs*"` *(Số nguyên, kích cỡ, ký tự dấu sao chú thích cuối dòng)*

Mục tiêu của luồng dữ liệu này là tiếp nhận chuỗi ký tự thô, phân tích cú pháp và ngữ nghĩa để bóc tách thành một cấu trúc dữ liệu chuẩn hóa gồm 4 thành phần độc lập:
$$\text{Raw String} \longrightarrow \{\text{Định lượng } (Quantity), \text{ Đơn vị } (Unit), \text{ Thực phẩm } (Food), \text{ Ghi chú } (Note)\}$$

---

#### 2. Sơ đồ Tuần tự Luồng Dữ liệu (Sequence Diagram)

Dưới đây là sơ đồ tương tác tuần tự trực quan của luồng nghiệp vụ bóc tách nguyên liệu:

![Sơ đồ tuần tự nghiệp vụ bóc tách nguyên liệu ẩm thực](assets/data_flow_1_parsing.png)

*Hình B.2: Sơ đồ tương tác tuần tự (Sequence Diagram) luồng nghiệp vụ bóc tách nguyên liệu ẩm thực Mealie v3.28.0*

---

#### 3. Bảng Đặc tả Chi tiết các Bước Chuyển dịch Dữ liệu

| Bước | Thành phần Nguồn | Thành phần Đích | Dữ liệu Luân chuyển | Thao tác Xử lý Kỹ thuật & Thuật toán |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Trình duyệt người dùng | Vue SPA | Ký tự chuỗi văn bản tự do | Bắt sự kiện bàn phím/form submit từ ô nhập liệu trên Web UI. |
| **2** | Vue SPA | `IngredientParserController` | `POST /api/parser/ingredient` | Gửi HTTP Request mang JSON Payload: `{"ingredient": "...", "parser": "nlp"}` kèm JWT Bearer Token. |
| **3** | Controller | `IngredientParserService` | Tham số gọi hàm: `parse([str])` | Pydantic kiểm tra hợp lệ kiểu; Factory `get_parser()` nạp parser tương ứng theo cấu hình. |
| **4** | Service | `string_utils.py` | Chuỗi nguyên liệu thô | • Ánh xạ phân số Unicode sang dạng số: `"1½"` $\to$ `" 1 1/2"`.<br>• Dùng Regex bóc tách định lượng hỗn số, phân số đơn, số thực.<br>• Chuyển ngoặc đơn về cuối chuỗi và xóa ký tự dấu sao (`*`). |
| **5** | Service | `unit_utils.py` | Chuỗi đơn vị nhận diện | Khởi tạo `UnitConverter` dùng thư viện `Pint`; kiểm tra và phân giải đơn vị (ví dụ phân biệt `ounce` khối lượng và `fl oz` thể tích). |
| **6** | Service | `DataMatcher` (`_base.py`) | Cặp chuỗi `(unit, food)` | Tra cứu từ điển đơn vị và thực phẩm trong CSDL; áp dụng so khớp mờ (**RapidFuzz**) với ngưỡng tương đồng $\ge 70\%$ cho đơn vị và $\ge 85\%$ cho thực phẩm. |
| **7** | `DataMatcher` | `IngredientParserService` | Đối tượng Entity CSDL | Gán liên kết khóa ngoại ID; tính toán 4 chỉ số tin cậy (`quantity`, `unit`, `food`, `comment`) và lấy trung bình cộng. |
| **8** | Controller | Vue SPA | HTTP 200 OK Response | Trả về chuỗi JSON tuân thủ schema `ParsedIngredient` chứa định lượng số thực `2.5`, đơn vị chuẩn `cup`, tên thực phẩm và ghi chú. |
| **9** | Vue SPA | Trình duyệt người dùng | DOM Rendering | Render các thẻ tag nguyên liệu đã phân tách để người dùng kiểm tra hoặc chỉnh sửa. |

---

#### 4. Phân tích Góc nhìn Kiểm thử Property-Based Testing (PBT)
Luồng dữ liệu bóc tách nguyên liệu tiếp nhận không gian chuỗi ngôn ngữ tự nhiên không giới hạn từ người dùng. Sự biến thiên định dạng (phân số Unicode, hỗn số, ký tự đặc biệt) đặt ra thách thức lớn về tính ổn định và tính toàn vẹn dữ liệu. Đây là căn cứ thực tiễn để nhóm xây dựng 2 bộ kiểm thử PBT trọng tâm:
* **Property 1 (Thành viên Phước):** Kiểm định tính bất biến chuyển đổi phân số Unicode trong hàm `convert_vulgar_fractions_to_regular_fractions`.
* **Property 2 (Thành viên Hiếu):** Kiểm định tính bảo toàn định lượng số thực trong hàm `extract_quantity_from_string`.

*(Các thuộc tính toán học chi tiết như tính lũy suy Idempotence, tính không âm và tính thu hẹp chuỗi được phân tích sâu tại Mục B.3.2).*

### B.2.2. Luồng Dữ liệu 2: Nghiệp vụ nhân chia tỉ lệ khẩu phần ăn (Servings Scaling)

#### 1. Bối cảnh và Mục tiêu nghiệp vụ
Trong nấu ăn thực tế, các công thức ẩm thực chuẩn luôn được định lượng sẵn cho một số lượng người ăn cụ thể, gọi là **Khẩu phần gốc** ($S_{\text{gốc}}$, ví dụ: công thức 4 người ăn). Tuy nhiên, nhu cầu thực tế của người dùng rất đa dạng: có thể chỉ nấu cho 1–2 người ăn, hoặc nấu cho bữa tiệc gia đình từ 8–10 người ăn, gọi là **Khẩu phần đích** ($S_{\text{đích}}$).

Mục tiêu của luồng dữ liệu Servings Scaling là:
1. **Co giãn tỉ lệ tức thời trên giao diện (Reactive UI):** Cho phép người dùng điều chỉnh khẩu phần thông qua thanh trượt hoặc bộ điều khiển số lượng (stepper control), toàn bộ định lượng của các nguyên liệu lập tức được nhân với hệ số tỉ lệ $k = \frac{S_{\text{đích}}}{S_{\text{gốc}}}$ mà không cần gửi request tải lại trang web.
2. **Xử lý đệ quy công thức phụ (Recursive Sub-recipes):** Trong trường hợp món ăn chứa một công thức thành phần lồng nhau (ví dụ: món *"Bánh Hamburger"* chứa công thức phụ *"Sốt BBQ"*), hệ thống phải nhân dồn hệ số tỉ lệ để co giãn chính xác các nguyên liệu bên trong công thức con.
3. **Đồng bộ với Danh sách đi chợ (Shopping List Synchronization):** Khi người dùng lưu công thức đã scale vào danh sách mua sắm, hệ thống lưu trữ cả định lượng gốc ($Q_{\text{gốc}}$) và hệ số scale ($k$) để phục vụ việc cộng dồn hoặc hoàn tác khi cần thiết.

---

#### 2. Sơ đồ Tuần tự Luồng Dữ liệu (Sequence Diagram)

Dưới đây là sơ đồ tương tác tuần tự trực quan của luồng nghiệp vụ nhân chia khẩu phần ăn:

![Sơ đồ tuần tự nghiệp vụ nhân chia khẩu phần ăn](assets/data_flow_2_scaling.png)

*Hình B.3: Sơ đồ tương tác tuần tự (Sequence Diagram) luồng nghiệp vụ nhân chia khẩu phần ăn Mealie v3.28.0*

---

#### 3. Bảng Đặc tả Chi tiết các Bước Chuyển dịch Dữ liệu

| Bước | Thành phần Nguồn | Thành phần Đích | Dữ liệu Luân chuyển | Thao tác Xử lý Kỹ thuật & Thuật toán |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Người dùng | Vue SPA | Tương tác Slider / Input number | Thay đổi giá trị khẩu phần ăn mong muốn ($S_{\text{đích}}$). |
| **2** | Vue Store (Pinia) | DOM UI | State biến số nguyên liệu | • Tính $k = S_{\text{đích}} / S_{\text{gốc}}$.<br>• Lặp qua mảng nguyên liệu trên Client: $Q_{\text{mới}} = Q_{\text{gốc}} \times k$.<br>• Format số thập phân sang chuỗi phân số trực quan (ví dụ: `1.5` $\to$ `"1 1/2"`). |
| **3** | Vue SPA | `HouseholdRecipeActionsController` | `POST /api/households/recipe-actions` | Truyền payload JSON: `{"recipe_slug": "...", "recipe_scale": k}` kèm JWT Token. |
| **4** | Controller | `ShoppingListService` | Lời gọi hàm nội bộ Backend | Controller xác thực `household_id` và gọi `get_shopping_list_items_from_recipe(list_id, recipe_id, scale=k)`. |
| **5** | Service | Sub-recipe Handler | Cặp dữ liệu `(sub_recipe, sub_scale)` | Kiểm tra `isinstance(ingredient.referenced_recipe, Recipe)`. Nếu đúng, tính dồn $\text{sub\_scale} = (Q_{\text{gốc}} \text{ or } 1) \times k$ và gọi đệ quy. |
| **6** | Service | Bộ nhớ RAM (List DTO) | Thực thể `ShoppingListItemCreate` | Tính `quantity = ingredient.quantity * scale if ingredient.quantity else 0`. Gắn kèm tham chiếu gốc `ShoppingListItemRecipeRefCreate(recipe_scale=scale)`. |
| **7** | Service | Database (SQLAlchemy) | SQL Insert / Update Statements | • Ghi dữ liệu vào bảng `shopping_list_items` (lưu định lượng tổng sau khi scale).<br>• Ghi bảng `shopping_list_item_recipe_reference` (lưu vết $k$ và định lượng gốc). |
| **8** | Database | Vue SPA | HTTP 200 OK Response | Trả về danh sách mục đi chợ hoàn chỉnh dạng JSON DTO. |
| **9** | Vue SPA | Màn hình người dùng | UI Notification / Badge | Hiển thị thông báo cập nhật giỏ hàng và số lượng nguyên liệu mới. |

---

#### 4. Phân tích Góc nhìn Kiểm thử Property-Based Testing (Property 4 — Trưởng nhóm Trần Quốc Quân)
Luồng dữ liệu Servings Scaling là đối tượng nghiên cứu và lập trình kiểm thử trọng tâm của **Trưởng nhóm Trần Quốc Quân** với **Property 4** tại tệp mã nguồn `tests/unit_tests/test_pbt_scaling.py`. Các Invariant toán học được định nghĩa nghiêm ngặt:

1. **Thuộc tính Tính đơn điệu (Monotonicity Invariant):**
   * *Mô tả:* Khi tăng khẩu phần ăn ($k > 1$), định lượng nguyên liệu sau khi nhân **bắt buộc phải tăng nghiêm ngặt** so với định lượng ban đầu. Ngược lại, khi giảm khẩu phần ăn ($k < 1$), định lượng nguyên liệu **bắt buộc phải giảm**.
   * *Công thức toán học:*
     $$\forall Q > 0, k > 0: \begin{cases} k > 1.0 \implies Q \times k > Q \\ k < 1.0 \implies Q \times k < Q \\ k = 1.0 \implies Q \times k = Q \end{cases}$$
   * *Ý nghĩa thực tế:* Loại bỏ hoàn toàn lỗi logic nghiệp vụ mà ở đó việc tăng số lượng người ăn lại dẫn đến lượng thực phẩm chuẩn bị bị sụt giảm.

2. **Thuộc tính Tính bảo toàn nghịch đảo (Reversibility Invariant):**
   * *Mô tả:* Phép toán nhân tỉ lệ phải có tính khả nghịch. Nếu định lượng $Q$ được nhân lên $k$ lần rồi chia lại cho đúng $k$ lần, kết quả thu được phải phục hồi lại chính xác giá trị ban đầu $Q$ trong phạm vi sai số dấu phẩy động cho phép.
   * *Công thức toán học:*
     $$\forall Q > 0, k > 0: \left| \frac{Q \times k}{k} - Q \right| \le 10^{-4}$$
   * *Ý nghĩa thực tế:* Đảm bảo tính nhất quán dữ liệu khi người dùng liên tục tăng giảm khẩu phần nhiều lần trên ứng dụng mà không bị tích lũy sai số trôi dạt (drift error).

3. **Thuộc tính Bảo toàn Điểm 0 (Zero Preservation):**
   * *Mô tả:* Với các nguyên liệu nêm nếm gia vị không mang định lượng số ($Q = 0$ hoặc `None`), phép co giãn khẩu phần không được phép phát sinh ngoại lệ hoặc các giá trị không hợp lệ (NaN / Undefined Values).
   * *Công thức toán học:* $Q = 0 \implies Q \times k = 0, \forall k > 0$.

### B.2.3. Luồng Dữ liệu 3: Nghiệp vụ lên lịch thực đơn (Meal Planning)

#### 1. Bối cảnh và Mục tiêu nghiệp vụ
Lập kế hoạch thực đơn (Meal Planning) là tính năng cốt lõi giúp các hộ gia đình chủ động quản lý dinh dưỡng, phân bổ thời gian nấu nướng và tối ưu hóa việc mua sắm thực phẩm theo tuần hoặc tháng. Trong Mealie `v3.28.0`, nghiệp vụ này cho phép:
* **Lên lịch theo dòng thời gian (Calendar-based Scheduling):** Gán công thức nấu ăn vào một ngày cụ thể với từng bữa ăn xác định: bữa sáng (`breakfast`), bữa trưa (`lunch`), bữa tối (`dinner`), hoặc món phụ (`side`).
* **Gợi ý món ăn ngẫu nhiên thông minh (Rule-based Randomizer):** Cho phép tự động gợi ý món ăn ngẫu nhiên dựa trên bộ quy tắc gia đình (`PlanRulesDay`, ví dụ: Thứ Hai món chay, Thứ Sáu hải sản, tránh lặp lại món trong 7 ngày).
* **Tự động kích hoạt sự kiện nền (Event-driven Timeline & Scheduler):** Tích hợp với Event Bus nội bộ và bộ lập lịch `APScheduler` để tự động tạo sự kiện nhắc việc nấu ăn và cảnh báo chuẩn bị nguyên liệu sớm (ví dụ: rã đông thịt từ đêm hôm trước).

---

#### 2. Sơ đồ Tuần tự Luồng Dữ liệu (Sequence Diagram)

Dưới đây là sơ đồ tương tác tuần tự trực quan của luồng nghiệp vụ lên lịch thực đơn:

![Sơ đồ tuần tự nghiệp vụ lên lịch thực đơn](assets/data_flow_3_mealplan.png)

*Hình B.4: Sơ đồ tương tác tuần tự (Sequence Diagram) luồng nghiệp vụ lên lịch thực đơn Mealie v3.28.0*

---

#### 3. Bảng Đặc tả Chi tiết các Bước Chuyển dịch Dữ liệu

| Bước | Thành phần Nguồn | Thành phần Đích | Dữ liệu Luân chuyển | Thao tác Xử lý Kỹ thuật & Thuật toán |
| :---: | :--- | :--- | :--- | :--- |
| **1** | Người dùng | Vue SPA (Calendar) | Thao tác kéo thả / Chọn form | Chọn ô ngày trên lịch tháng/tuần, chọn loại bữa ăn (`entry_type`), gán công thức hoặc yêu cầu gợi ý món ngẫu nhiên. |
| **2** | Vue SPA | `GroupMealplanController` | `POST /api/households/mealplans` | Gửi HTTP Request mang JSON Payload: `CreatePlanEntry` gồm ngày, loại bữa và `recipe_id` kèm JWT Bearer Token. |
| **3** | Controller | `RepositoryMeals` | DTO thực thể nghiệp vụ | Controller kiểm thực qua Pydantic V2, ánh xạ gắn `group_id` và `user_id` của phiên người dùng hiện tại. |
| **4** | Repository | Database (SQLAlchemy) | SQL Insert Transaction | Chèn bản ghi mới vào bảng `meal_plan_entries`, ràng buộc khóa ngoại tới `recipes`, `groups` và `users`. |
| **5** | Database | Repository | Transaction Commit | Xác nhận ghi dữ liệu bền vững, sinh UUID định danh duy nhất cho mục thực đơn mới. |
| **6** | Controller | Vue SPA | HTTP 201 Created Response | Trả về đối tượng `ReadPlanEntry` DTO đầy đủ thuộc tính chi tiết món ăn (kèm phát sự kiện đồng bộ nền). |
| **7** | Vue SPA | Trình duyệt người dùng | DOM Calendar Re-render | Hiển thị thẻ món ăn cùng hình ảnh minh họa trên ô lịch ngày đã chọn. |

---

#### 4. Phân tích Góc nhìn Kiểm thử Property-Based Testing (PBT)
Nghiệp vụ Meal Planning liên quan trực tiếp đến dữ liệu chuỗi thời gian (Date/Time Temporal Constraints). Đây là phân hệ quan trọng để áp dụng PBT kiểm tra các tính chất toàn vẹn thời gian:

1. **Thuộc tính Giới hạn Thời gian và Tính duy nhất (Temporal Invariant):**
   * *Mô tả:* Kế hoạch thực đơn trong cùng một bữa ăn của một hộ gia đình phải thỏa mãn tính nhất quán; việc lọc bữa ăn theo khoảng ngày `[start_date, end_date]` phải luôn tuân thủ nguyên lý khoảng đóng toán học:
     $$\forall \text{entry} \in \text{Results}: \text{start\_date} \le \text{entry.date} \le \text{end\_date}$$
   * *Ý nghĩa:* Đảm bảo truy vấn phân trang thời gian không bao giờ trả về các bản ghi ngoài phạm vi lọc.
2. **Thuộc tính Bảo toàn Tính hợp lệ của Khóa ngoại:**
   * Mọi mục meal plan được tạo ra ngẫu nhiên với `recipe_id` phải luôn tham chiếu đến một công thức hợp lệ tồn tại trong CSDL của nhóm gia đình đó, ngăn chặn hiện tượng mồ côi dữ liệu (Orphaned Entries).

## B.3 Phân Tích Chi Tiết 3 Module Trọng Tâm Phục Vụ Kiểm Thử

Để chuẩn bị cơ sở lý thuyết và kỹ thuật cho việc xây dựng các bộ kiểm thử tự động dựa trên tính chất (**Property-Based Testing - PBT**) với thư viện Hypothesis, nhóm tiến hành mổ xẻ mã nguồn chi tiết 3 module hạt nhân nằm trong tầng xử lý phân tích cú pháp của Mealie (`mealie/services/parser_services/`):
1. `ingredient_parser.py`: Bộ điều phối phân tích chuỗi nguyên liệu tổng quát.
2. `string_utils.py`: Bộ tiện ích tiền xử lý chuỗi ký tự và bóc tách đại lượng số học.
3. `unit_utils.py`: Bộ công cụ quản lý và chuyển đổi đơn vị đo lường vật lý.

---

### B.3.1 Module `ingredient_parser.py` (Bộ điều phối phân tích cú pháp nguyên liệu)

#### 1. Định vị & Vai trò Kiến trúc
- **Đường dẫn tệp:** `mealie/services/parser_services/ingredient_parser.py`
- **Quy mô & Phụ thuộc:** 321 dòng mã lệnh; kế thừa lớp cơ sở `ABCIngredientParser` (`_base.py`); phụ thuộc vào `pydantic`, thư viện ngoài `ingredient_parser-nlp` (hoặc module regex nội bộ `brute`), `DataMatcher` và các DTO Pydantic (`ParsedIngredient`, `RecipeIngredient`, `IngredientConfidence`).
- **Nhiệm vụ cốt lõi:** Đóng vai trò là façade điều phối cấp cao nhất trong nghiệp vụ trích xuất nguyên liệu. Module tiếp nhận chuỗi mô tả tự nhiên từ người dùng (ví dụ: `"2 1/2 cups organic all-purpose flour, sifted"`), điều phối qua các parser chuyên biệt (`NLPParser`, `BruteForceParser`), sau đó chuẩn hóa và liên kết dữ liệu với cơ sở dữ liệu để trả về cấu trúc dữ liệu hoàn chỉnh.

#### 2. Cấu trúc Lớp & Phương thức Quan trọng

```
                         ┌───────────────────────┐
                         │  ABCIngredientParser  │
                         └───────────┬───────────┘
                                     │ (kế thừa)
                 ┌───────────────────┴───────────────────┐
                 ▼                                       ▼
       ┌───────────────────┐                   ┌───────────────────┐
       │ BruteForceParser  │                   │     NLPParser     │
       └───────────────────┘                   └───────────────────┘
```

* **Lớp `BruteForceParser`:**
  * `parse_one(ingredient_string: str) -> ParsedIngredient`: Sử dụng thuật toán bóc tách dựa trên luật Heuristic và Regular Expression thuần túy trong submodule `brute`. Dùng trong trường hợp hệ thống không tải được mô hình NLP học máy hoặc cấu hình chế độ tiết kiệm tài nguyên.
  * Tự động tính toán điểm tin cậy trung bình (`IngredientConfidence`) dựa trên sự hiện diện của số lượng (`quantity`), đơn vị (`unit`), tên thực phẩm (`food`) và ghi chú (`note`).
* **Lớp `NLPParser`:**
  * `parse_one(ingredient_string: str) -> ParsedIngredient`: Gọi thư viện NLP `parse_ingredient()` kết hợp truyền từ điển đơn vị tùy chỉnh lấy từ CSDL (`custom_units=database_units`).
  * `_convert_ingredient(ingredient: IngredientParserParsedIngredient) -> ParsedIngredient`: Xử lý phân rã các thành phần phân tích phức hợp (`CompositeIngredientAmount`), tách biệt lượng chính và lượng phụ, bóc tách tên thực phẩm (`food`), đơn vị (`unit`), số lượng (`qty`) và ghi chú (`note`).
  * `_extract_quantity(ingredient_amount: IngredientAmount) -> tuple[float, float]`: Chuyển đổi an toàn giá trị số lượng từ dạng phân số chuỗi hoặc số thực, trả về bộ `(qty, confidence)`. Bắt ngoại lệ `ValueError` để tránh crash và hạ điểm tin cậy về 0.
  * `_extract_unit(ingredient_amount: IngredientAmount) -> tuple[str, float]`: Chuẩn hóa đơn vị đo lường và điểm tin cậy đi kèm.
  * `_extract_note(...)`: Tổng hợp các trường kích thước (`size`), cách sơ chế (`preparation`), bình luận (`comment`), mục đích (`purpose`) thành chuỗi ghi chú thống nhất.
  * `_convert_extra_ingredients(...)`: Tự động nhận diện nguyên liệu thay thế (ví dụ: `"1 cup stock or broth"` $\to$ trích xuất `broth` thành `RecipeIngredientSubstitution`).
* **Hàm khởi tạo dạng Factory `get_parser`:**
  * `get_parser(parser: RegisteredParser, group_id: UUID4, session: Session, translator: Translator) -> ABCIngredientParser`: Khởi tạo đúng parser tương ứng với cấu hình hệ thống (`RegisteredParser.nlp`, `RegisteredParser.brute` hoặc `RegisteredParser.openai`).

#### 3. Các Rủi ro Tiềm ẩn & Ý nghĩa Kiểm thử PBT
* **Xử lý chuỗi nhập tùy ý (Arbitrary Input Robustness):** Người dùng có thể nhập các chuỗi cực đoan (chuỗi rỗng, khoảng trắng, ký tự Unicode đặc thù, chuỗi dài hàng nghìn ký tự, thẻ HTML/Script). Parser không bao giờ được phép phát sinh Unhandled Exception làm sập tiến trình FastAPI.
* **Tính bảo toàn chuỗi gốc (Original Text Preservation Invariant):**
  $$\text{result.ingredient.original\_text} \equiv \text{input\_string}$$
  Bảo đảm hệ thống không bao giờ làm mất hoặc cắt gọt chuỗi nguyên thủy của người dùng.
* **Tính chặn của độ tin cậy (Confidence Range Invariant):**
  $$\forall c \in \{\text{average}, \text{quantity}, \text{unit}, \text{food}, \text{comment}\}: 0.0 \le c \le 1.0$$

---

### B.3.2 Module `string_utils.py` (Bộ tiện ích tiền xử lý chuỗi và số học)

#### 1. Định vị & Vai trò Kiến trúc
- **Đường dẫn tệp:** `mealie/services/parser_services/parser_utils/string_utils.py`
- **Quy mô & Phụ thuộc:** 122 dòng mã lệnh; phụ thuộc thư viện chuẩn Python `re` (Regular Expressions) và `fractions.Fraction`.
- **Nhiệm vụ cốt lõi:** Cung cấp các thuật toán cấp thấp (low-level primitives) phục vụ tiền xử lý chuỗi văn bản công thức món ăn: chuẩn hóa phân số Unicode (Vulgar Fractions), bóc tách số lượng từ chuỗi hỗn số/phân số/số thực, và lọc bỏ các ký tự phụ trợ (dấu ngoặc đơn, ký tự footnote).

#### 2. Chi tiết các Hàm Nòng cốt & Thuật toán

##### a) `convert_vulgar_fractions_to_regular_fractions(text: str) -> str`
* **Cơ chế:** Ánh xạ từ điển 18 ký tự phân số Unicode cổ điển sang chuỗi phân số ASCII chuẩn:
  * Phân số 1 chữ số: `¼` $\to$ `" 1/4"`, `½` $\to$ `" 1/2"`, `¾` $\to$ `" 3/4"`, `⅓` $\to$ `" 1/3"`, `⅔` $\to$ `" 2/3"`...
  * Phân số mẫu số lớn: `⅐` $\to$ `" 1/7"`, `⅛` $\to$ `" 1/8"`, `⅑` $\to$ `" 1/9"`, `⅒` $\to$ `" 1/10"`...
* **Kỹ thuật chống lỗi dính số:** Hàm chủ động chèn thêm một khoảng trắng (`" "`) phía trước phân số chuẩn (`f" {regular_fraction}"`). Điều này ngăn chặn lỗi nghiêm trọng khi chuyển đổi hỗn số dạng `"1½"`: nếu không có khoảng trắng, chuỗi sẽ biến thành `"11/2"` (tức 5.5 thay vì 1.5).

##### b) `extract_quantity_from_string(source_str: str) -> tuple[float, str]`
* **Cơ chế nhận dạng phân tầng (Hierarchical Regex Matching):**
  1. *Bước 1:* Gọi `convert_vulgar_fractions_to_regular_fractions` để chuẩn hóa toàn bộ ký tự phân số Unicode thành ASCII.
  2. *Bước 2 (Hỗn số):* Khớp mẫu `mixed_fraction_pattern = re.compile(r"(\d+)\s+(\d+)/(\d+)")`. Nếu khớp (ví dụ `"1 1/2"`), tính $Q = \text{whole} + \frac{\text{num}}{\text{den}}$ thông qua `fractions.Fraction`.
  3. *Bước 3 (Phân số đơn):* Khớp mẫu `fraction_pattern = re.compile(r"(\d+)/(\d+)")`. Nếu khớp (ví dụ `"3/4"`), tính $Q = \frac{\text{num}}{\text{den}}$.
  4. *Bước 4 (Số nguyên / Thập phân):* Khớp mẫu `number_pattern = re.compile(r"\d+(\.\d+)?")`. Chuyển đổi trực tiếp qua `float()`.
* **Phần dư chuỗi (Remaining String):** Cắt bỏ đoạn substring chứa số lượng và trả về phần còn lại đã được `.strip()`.
* **Bảo vệ lỗi chia cho 0:** Bọc trong khối `try ... except ZeroDivisionError` để trả về an toàn `(0, source_str)` nếu gặp phân số dị thường như `"1/0"`.

##### c) `move_parens_to_end(ing_str: str) -> str` & `remove_footnote_markers(ing_str: str) -> str`
* `move_parens_to_end`: Sử dụng biểu thức chính quy để nhận diện và dời cụm ghi chú trong ngoặc `(...)` ra cuối chuỗi (ví dụ: `"flour (sifted) 200g"` $\to$ `"flour 200g (sifted)"`).
* `remove_footnote_markers`: Xóa bỏ các ký tự hoa thị tham chiếu cuối chuỗi (ví dụ: `"olive oil*"` $\to$ `"olive oil"`).

#### 3. Các Tính chất Toán học & Mục tiêu Kiểm thử PBT (Property-Based Testing)
Module `string_utils.py` là đối tượng hoàn hảo nhất cho kỹ thuật kiểm thử dựa trên thuộc tính (PBT):
1. **Tính Lũy suy (Idempotence Property):**
   Phép chuyển đổi phân số Unicode là một hàm lũy suy, tức áp dụng nhiều lần liên tiếp không làm biến đổi kết quả:
   $$f(f(\text{text})) \equiv f(\text{text}) \quad \text{với } f = \text{convert\_vulgar\_fractions\_to\_regular\_fractions}$$
2. **Tính Hợp lệ & Chặn Dưới của Số lượng (Non-negativity Property):**
   $$\forall s \in \text{ArbitraryStrings}: \text{extract\_quantity\_from\_string}(s)[0] \ge 0.0$$
3. **Tính Thu hẹp Chuỗi (String Contraction Invariant):**
   Phần chuỗi còn lại sau khi bóc tách số lượng không bao giờ dài hơn chuỗi ban đầu:
   $$\text{len}(\text{remaining\_str}) \le \text{len}(\text{source\_str})$$
4. **Tính Bất biến Không sập (Crash-Freedom Invariant):**
   Với bất kỳ chuỗi Unicode ngẫu nhiên nào sinh bởi Hypothesis, hàm không bao giờ ném ngoại lệ chưa xử lý (`ZeroDivisionError`, `IndexError`, `ValueError`).

---

### B.3.3 Module `unit_utils.py` (Bộ quản lý và quy đổi đơn vị đo lường)

#### 1. Định vị & Vai trò Kiến trúc
- **Đường dẫn tệp:** `mealie/services/parser_services/parser_utils/unit_utils.py`
- **Quy mô & Phụ thuộc:** 171 dòng mã lệnh; tích hợp sâu với thư viện vật lý `pint` (`UnitRegistry`, `Unit`, `Quantity`), `functools.lru_cache`, và schema `mealie.schema.recipe.recipe_ingredient`.
- **Nhiệm vụ cốt lõi:** Quản lý không gian đơn vị đo lường trong công thức ẩm thực, kiểm tra tính tương thích thứ nguyên (Dimensionality Compatibility), thực hiện quy đổi đơn vị khối lượng/thể tích và cộng gộp số lượng nguyên liệu trong giỏ đi chợ.

#### 2. Cấu trúc Lớp & Phương thức Quan trọng

##### a) Singleton Cache `_shared_unit_registry()`
* Việc khởi tạo đối tượng `UnitRegistry` trong thư viện `pint` tốn chi phí CPU và bộ nhớ rất lớn (nạp định nghĩa hàng nghìn đơn vị vật lý quốc tế).
* Module sử dụng decorator `@lru_cache(maxsize=1)` để lưu trữ một singleton `UnitRegistry` dùng chung cho toàn bộ ứng dụng:
  ```python
  @lru_cache(maxsize=1)
  def _shared_unit_registry() -> UnitRegistry:
      from pint import UnitRegistry
      return UnitRegistry()
  ```

##### b) Lớp `UnitConverter`
* Hỗ trợ cờ `private_registry: bool`: Nếu cần định nghĩa các đơn vị tùy biến cục bộ (ví dụ đơn vị tùy biến của Mealie `_mealie_unit_1`), hệ thống khởi tạo registry riêng biệt để tránh làm ô nhiễm không gian tên đơn vị dùng chung.
* **Heuristic giải quyết xung đột Ounce (`_resolve_ounce`):**
  * Trong ngữ cảnh ẩm thực, `"ounce"` thường bị dùng lẫn lộn giữa Ounce khối lượng (Avoirdupois ounce - thứ nguyên `[mass]`) và Ounce chất lỏng (Fluid ounce - thứ nguyên thể tích `[length] ** 3`).
  * Hàm tự động phát hiện: nếu một đơn vị là `"ounce"` và đơn vị đối ứng mang thứ nguyên thể tích, hàm sẽ tự động ép kiểu `"ounce"` thành `"fluid_ounce"`.
* **Phương thức `parse(unit: str | Unit, strict: bool = False) -> str | Unit`:**
  * Phân giải chuỗi sang `pint.Unit`. Nếu `strict=False`, khi gặp đơn vị không tồn tại trong từ điển vật lý (ví dụ: `"củ"`, `"nhánh"`, `"quả"`), hàm trả về nguyên vẹn chuỗi gốc mà không gây lỗi. Nếu `strict=True`, hàm ném ngoại lệ `UnitNotFound`.
* **Phương thức `can_convert(unit, to_unit) -> bool`:**
  * Kiểm tra tính tương thích thứ nguyên (`unit.is_compatible_with(to_unit)`). Ví dụ: `gram` có thể đổi sang `kilogram`, nhưng không thể đổi sang `ml` nếu không có khối lượng riêng.
* **Phương thức `convert(quantity: float, unit, to_unit) -> tuple[float, Unit]`:**
  * Thực hiện phép nhân đại lượng $Q \times U$, sau đó chuyển đổi sang đơn vị đích thông qua `qty.to(to_unit)`. Trả về `(magnitude, units)`.
* **Phương thức `merge(quantity_1, unit_1, quantity_2, unit_2) -> tuple[float, Unit]`:**
  * Cộng gộp hai đại lượng cùng thứ nguyên: $Q_{\text{merged}} = Q_1 \cdot U_1 + Q_2 \cdot U_2$.

##### c) Hàm `merge_quantity_and_unit[T: CreateIngredientUnit](qty_1, unit_1, qty_2, unit_2) -> tuple[float, T]`
* Hỗ trợ gộp nguyên liệu có đơn vị tùy chỉnh đã lưu trong CSDL Mealie. Tự động định nghĩa đơn vị ảo tạm thời vào Pint (`ureg.define`), thực hiện phép cộng, sau đó tự động chuẩn hóa về đơn vị lớn hơn nếu tổng lượng $\ge 1$, hoặc đơn vị nhỏ hơn nếu $< 1$ (ví dụ: $0.2 \text{ kg} \to 200 \text{ g}$).

#### 3. Các Tính chất Toán học & Mục tiêu Kiểm thử PBT (Property-Based Testing)
Module `unit_utils.py` cung cấp các tính chất toán học hoàn hảo để kiểm thử PBT:
1. **Tính Bảo Toàn Chuyển Đổi Hai Chiều (Round-Trip Invariant):**
   Chuyển đổi một đại lượng từ đơn vị $A$ sang $B$ rồi chuyển ngược lại từ $B$ về $A$ phải bảo toàn giá trị ban đầu (với sai số dấu phẩy động $\epsilon$):
   $$\forall Q > 0, (U_A \sim U_B): \left| \text{convert}\left(\text{convert}(Q, U_A, U_B)[0], U_B, U_A\right)[0] - Q \right| < 10^{-5}$$
2. **Tính Tuyến Tính & Cộng Tính (Additivity / Commutativity):**
   Phép gộp hai đại lượng cùng đơn vị phải có tính giao hoán và cộng tính:
   $$\text{merge}(Q_1, U, Q_2, U)[0] \equiv Q_1 + Q_2$$
   $$\text{merge}(Q_1, U_1, Q_2, U_2)[0] \approx \text{merge}(Q_2, U_2, Q_1, U_1)[0]$$
3. **Tính An Toàn Ngoại Lệ (Exception Safety & Strictness Contract):**
   Với chế độ `strict=False`, hàm `parse(unit)` luôn luôn trả về một giá trị hợp lệ (`pint.Unit` hoặc chuỗi gốc `str`), không bao giờ phát sinh ngoại lệ dù đầu vào là bất kỳ chuỗi dị thường (malformed string) nào.

---

### B.3.4 Tổng Kết Mối Liên Kết Giữa 3 Module và Kế Hoạch Kiểm Thử Nhóm 6

| Module | Vị trí Kiến trúc | Chức năng Cốt lõi | Thuộc tính PBT Trọng tâm (Hypothesis) | Độ phức tạp Xử lý |
| :--- | :--- | :--- | :--- | :---: |
| `ingredient_parser.py` | Orchestration Layer | Façade điều phối NLP & Heuristic, tính điểm tin cậy | • Crash-freedom với chuỗi ngẫu nhiên<br/>• Bảo toàn `original_text`<br/>• Chặn khoảng $0 \le \text{confidence} \le 1$ | Trung bình - Cao |
| `string_utils.py` | Core Data Manipulation | Chuẩn hóa phân số Unicode, bóc tách số lượng | • Idempotence của phân số Unicode<br/>• Không âm $Q \ge 0$<br/>• An toàn với chia cho 0 (`ZeroDivisionError`) | Cao (Đại số & Chuỗi) |
| `unit_utils.py` | Physical Dimension Engine | Quản lý Pint registry, kiểm tra thứ nguyên, quy đổi | • Round-trip bảo toàn giá trị đại lượng<br/>• Cộng tính đại lượng cùng thứ nguyên<br/>• An toàn khi `strict=False` | Cao (Vật lý & Thứ nguyên) |

Sự kết hợp chặt chẽ của 3 module này hình thành nên bộ khung xử lý dữ liệu nguyên liệu của Mealie. Việc phân tích chuyên sâu cấu trúc mã nguồn và các tính chất bất biến trên là cơ sở lý thuyết trực tiếp để nhóm triển khai các file kiểm thử Property-Based Testing trong Nhóm việc Q3 (`tests/unit_tests/test_pbt_scaling.py` và các bộ test PBT liên quan).
