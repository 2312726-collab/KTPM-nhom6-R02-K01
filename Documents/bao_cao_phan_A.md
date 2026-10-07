# PHẦN A: MÔ TẢ HỆ THỐNG MỤC TIÊU (MEALIE v3.28.0)
## BÁO CÁO ĐỒ ÁN MÔN HỌC KIỂM THỬ PHẦN MỀM — NHÓM 6
* **Tổ hợp đề tài:** R02 (Mealie) — K01 (Property-Based Testing với Hypothesis)
* **Giảng viên hướng dẫn:** ThS. Nguyễn Thế Lâm
* **Sinh viên phụ trách chính Phần A:** Trần Quốc Quân (MSSV: `2312726` — Trưởng nhóm)
* **Phiên bản hệ thống mục tiêu:** Release Tag **`v3.28.0`** (Commit SHA: `0552eaa4a80031b8572849cca0ed95d07f1be001`)

---

## 📌 A.1. TỔNG QUAN HỆ THỐNG MEALIE

### 1. Giới thiệu và Bối cảnh bài toán
Trong đời sống gia đình hiện đại, việc quản lý dinh dưỡng và nấu nướng thường gặp phải tình trạng phân mảnh thông tin:
* Các công thức nấu ăn được lưu rải rác trên nhiều website ẩm thực, mạng xã hội, sách báo hoặc ghi chép tay.
* Định lượng nguyên liệu trong các công thức gốc thường được cố định cho một số lượng người ăn cụ thể (ví dụ: công thức cho 2 người), gây khó khăn khi cần nấu cho gia đình đông người hoặc các bữa tiệc (cần tăng lên 6–8 người).
* Các hệ thống đo lường ẩm thực trên thế giới thiếu tính đồng nhất: một số công thức dùng hệ đo lường Quốc tế (Metric: gram, kilogram, mililit), trong khi nhiều công thức phương Tây sử dụng hệ đo lường Anh-Mỹ (Imperial: pound, ounce, teaspoon, tablespoon, cup).

**Mealie** ra đời như một nền tảng mã nguồn mở tự lưu trữ (**Self-hosted Recipe Management System**) nhằm giải quyết toàn diện bài toán trên. Hệ thống cung cấp giải pháp trọn gói: từ việc tự động "cào" (scrape) dữ liệu công thức từ các trang web, bóc tách nguyên liệu thông minh bằng xử lý ngôn ngữ tự nhiên, tự động nhân chia khẩu phần ăn, cho đến lập kế hoạch thực đơn theo tuần và sinh danh sách mua sắm thực phẩm.

### 2. Mục tiêu và Phạm vi của hệ thống
* **Tự động hóa số hóa công thức:** Cho phép người dùng nhập đường dẫn (URL) của bất kỳ trang web ẩm thực phổ biến nào; hệ thống sẽ tự động trích xuất tiêu đề, hình ảnh, thời gian nấu, danh mục nguyên liệu và các bước thực hiện.
* **Xử lý ngôn ngữ tự nhiên đối với nguyên liệu ẩm thực:** Chuẩn hóa các chuỗi văn bản tự do do con người nhập vào (ví dụ: *"2 1/2 muỗng canh dầu ô liu (loại nguyên chất)"*) thành cấu trúc dữ liệu máy tính hiểu được: `{định lượng: 2.5, đơn vị: "muỗng canh", thực phẩm: "dầu ô liu", ghi chú: "loại nguyên chất"}`.
* **Tính toán khẩu phần ăn linh hoạt:** Tự động co giãn định lượng của tất cả nguyên liệu trong công thức khi người dùng thay đổi số lượng khẩu phần ăn (Servings).
* **Quản trị ẩm thực theo hộ gia đình:** Hỗ trợ mô hình đa người dùng (Multi-user) và hộ gia đình (Household), giúp các thành viên trong nhà cùng xem thực đơn và đi chợ.

### 3. Ngăn xếp công nghệ cốt lõi (Technology Stack)
Qua khảo sát trực tiếp từ tệp cấu hình đóng gói mã nguồn `mealie_src/pyproject.toml` phiên bản `v3.28.0`, hệ thống Mealie được xây dựng trên nền tảng kỹ thuật hiện đại:

| Thành phần | Công nghệ / Thư viện | Phiên bản | Vai trò kỹ thuật trong hệ thống |
| :--- | :--- | :---: | :--- |
| **Ngôn ngữ Backend** | Python | `>=3.14, <3.15` | Ngôn ngữ thực thi toàn bộ logic nghiệp vụ phía máy chủ. |
| **Web Framework** | `FastAPI` | `0.141.1` | Xây dựng RESTful API bất đồng bộ (Async), tự động sinh tài liệu Swagger UI (`/docs`). |
| **ASGI Server** | `Uvicorn` | `0.53.0` | Máy chủ web hiệu năng cao điều phối các kết nối HTTP/WebSocket. |
| **ORM / Data Access** | `SQLAlchemy` | `2.0.54` | Tầng ánh xạ đối tượng — cơ sở dữ liệu thế hệ 2 mới nhất. |
| **Database Migration** | `Alembic` | `1.20.0` | Quản lý lịch sử và đồng bộ các thay đổi lược đồ cơ sở dữ liệu. |
| **Cơ sở dữ liệu** | SQLite / PostgreSQL | — | Lưu trữ dữ liệu quan hệ (mặc định dùng SQLite nhẹ gọn, hỗ trợ PostgreSQL cho sản xuất). |
| **Kiểm thực dữ liệu** | `Pydantic` | `2.13.5` | Định nghĩa Schema, ép kiểu và kiểm tra tính hợp lệ dữ liệu vào/ra nghiêm ngặt. |
| **Phân tích nguyên liệu** | `ingredient-parser-nlp` | `2.7.0` | Mô hình NLP chuyên bóc tách thành phần ngữ nghĩa của chuỗi nguyên liệu. |
| **Quy đổi đơn vị** | `Pint` | `0.26.1` | Thư viện vật lý/toán học xử lý chuyển đổi giữa các hệ thống đo lường. |
| **Cào dữ liệu web** | `recipe-scrapers` | `15.12.0` | Engine bóc tách cấu trúc schema JSON-LD/Microdata từ hơn 100 website ẩm thực. |
| **Xử lý chuỗi nâng cao** | `RapidFuzz` & `text-unidecode` | `3.14.6` | So khớp chuỗi mờ và chuẩn hóa các ký tự Unicode phân số (`½`, `¼`, `¾`). |
| **Giao diện Frontend** | `Vue.js` (Nuxt) | 3.x | Ứng dụng trang đơn (SPA) tương tác mượt mà, giao tiếp với Backend qua REST API. |
| **Đóng gói triển khai** | `Docker` & `Docker Compose` | — | Đóng gói toàn bộ ứng dụng thành container chạy độc lập trên mọi hệ điều hành. |

---

## 👥 A.2. CÁC TÁC NHÂN TƯƠNG TÁC HỆ THỐNG (ACTORS)

Hệ thống Mealie phân định rõ ranh giới quyền hạn thông qua 2 tác nhân chính:

```text
       ┌──────────────────┐               ┌──────────────────┐
       │    Home User     │               │  Administrator   │
       │ (Người dùng nhà) │               │ (Quản trị viên)  │
       └────────┬─────────┘               └────────┬─────────┘
                │                                  │
    ┌───────────┴───────────┐          ┌───────────┴───────────┐
    │  Quản lý công thức    │          │  Cấu hình hệ thống    │
    │  Bóc tách nguyên liệu │          │  Quản lý tài khoản    │
    │  Co giãn khẩu phần    │          │  Sao lưu & phục hồi   │
    │  Lên thực đơn tuần    │          │  Tích hợp Email/OIDC  │
    └───────────────────────┘          └───────────────────────┘
```

### 1. Tác nhân "Người dùng gia đình" (Home User)
* **Định nghĩa:** Là người dùng thông thường trong gia đình, tham gia vào hoạt động nấu ăn, lên thực đơn và mua sắm thực phẩm.
* **Quyền hạn và Hành vi chính:**
  * Thêm mới công thức bằng cách dán đường dẫn trang web ẩm thực hoặc nhập trực tiếp.
  * Tùy biến thông số khẩu phần ăn (Servings) của từng món để xem định lượng nguyên liệu mới.
  * Lập kế hoạch bữa ăn theo ngày/tuần (gán món ăn vào bữa sáng, trưa, tối).
  * Đánh dấu các nguyên liệu cần mua vào Danh sách đi chợ (Shopping List).
  * Chia sẻ công thức nấu ăn với các thành viên khác trong cùng hộ gia đình (Household).

### 2. Tác nhân "Quản trị viên hệ thống" (System Administrator)
* **Định nghĩa:** Là người chịu trách nhiệm quản lý kỹ thuật, cấu hình và vận hành máy chủ Mealie.
* **Quyền hạn và Hành vi chính:**
  * Quản lý người dùng: Tạo tài khoản, kích hoạt/vô hiệu hóa người dùng, cấp quyền quản trị.
  * Thiết lập không gian làm việc: Tạo và phân bổ các Nhóm (Groups) và Hộ gia đình (Households).
  * Bảo trì dữ liệu: Thực hiện sao lưu định kỳ (Database & Image Backups) và phục hồi khi xảy ra sự cố.
  * Cấu hình dịch vụ máy chủ: Thiết lập máy chủ thư điện tử (SMTP), chứng thực một lần (SSO/OIDC), quản trị quyền riêng tư và đăng ký tài khoản tự do (Sign-up toggle).

---

## ⚙️ A.3. NĂM USE CASE CỐT LÕI CỦA HỆ THỐNG

Dưới đây là đặc tả chi tiết 5 trường hợp sử dụng (Use Case) quan trọng nhất đại diện cho toàn bộ luồng nghiệp vụ của Mealie:

```text
┌────────────────────────────────────────────────────────────────────────┐
│                        HỆ THỐNG MEALIE (v3.28.0)                       │
│                                                                        │
│   [Home User] ───────► (UC-01: Import & Quản lý công thức)            │
│       │                                                                │
│       ├──────────────► (UC-02: Phân tích chuỗi nguyên liệu - Parser)   │
│       │                      │ (Trọng tâm kiểm thử Property 1, 3, 5)   │
│       │                                                                │
│       ├──────────────► (UC-03: Co giãn khẩu phần ăn - Servings Scale)  │
│       │                      │ (Trọng tâm kiểm thử Property 4)         │
│       │                                                                │
│       ├──────────────► (UC-04: Lập kế hoạch thực đơn tuần)             │
│       │                                                                │
│       └──────────────► (UC-05: Quy đổi đơn vị đo lường)                │
│                              │ (Trọng tâm kiểm thử Property 2)         │
│                                                                        │
│   [Administrator] ───► (Quản trị hệ thống, Backup, Cấu hình)           │
└────────────────────────────────────────────────────────────────────────┘
```

### 1. UC-01: Thêm và Import công thức nấu ăn (Recipe Import & Management)
* **Mã Use Case:** `UC-01`
* **Tác nhân:** Home User
* **Mô tả:** Người dùng nhập một đường link từ internet; hệ thống tự động cào thông tin và lưu công thức thành một bản ghi hoàn chỉnh trong cơ sở dữ liệu.
* **Tiền điều kiện:** Người dùng đã đăng nhập vào hệ thống; đường dẫn URL hợp lệ và máy chủ Mealie có kết nối internet.
* **Luồng sự kiện chính (Main Flow):**
  1. Người dùng chọn chức năng *"Create Recipe from URL"* trên giao diện và dán đường link bài viết ẩm thực.
  2. Giao diện gửi yêu cầu `POST /api/recipes/create-url` kèm theo URL tới Backend.
  3. Module `mealie.services.scraper` sử dụng thư viện `recipe-scrapers` để tải mã HTML, trích xuất cấu trúc dữ liệu schema JSON-LD/OpenGraph.
  4. Hệ thống tải ảnh đại diện của món ăn, chuẩn hóa danh sách các bước thực hiện (instructions) và danh mục nguyên liệu (ingredients).
  5. Hệ thống lưu bản ghi vào bảng `recipes` trong cơ sở dữ liệu và trả về thông tin chi tiết công thức.
  6. Giao diện chuyển hướng người dùng đến trang chi tiết công thức vừa tạo thành công.
* **Hậu điều kiện:** Công thức mới được lưu trữ an toàn, hiển thị trong danh mục món ăn của gia đình.

---

### 2. UC-02: Phân tích & Bóc tách chuỗi nguyên liệu tự nhiên (Ingredient Parsing)
> **Ghi chú học thuật:** Đây là nghiệp vụ trọng tâm được nhóm chọn làm đối tượng kiểm thử chính cho kỹ thuật Property-Based Testing (**Property 1, Property 3 và Property 5**).

* **Mã Use Case:** `UC-02`
* **Tác nhân:** Home User, hoặc tự động kích hoạt bởi UC-01.
* **Mô tả:** Bóc tách một chuỗi văn bản tự do chứa ngôn ngữ tự nhiên thành các thành phần định lượng có cấu trúc rõ ràng.
* **Ví dụ nghiệp vụ:**
  * Chuỗi đầu vào: `"2 1/2 cups of all-purpose flour, sifted (organic)"`
  * Dữ liệu bóc tách mong đợi:
    * **Quantity (Định lượng):** `2.5` (chuyển đổi từ hỗn số `"2 1/2"`).
    * **Unit (Đơn vị):** `"cup"`.
    * **Food (Thực phẩm):** `"all-purpose flour"`.
    * **Note (Ghi chú):** `"sifted (organic)"`.
* **Luồng sự kiện chính (Main Flow):**
  1. Người dùng nhập một danh sách dòng nguyên liệu thô vào khung soạn thảo.
  2. Backend chuyển giao chuỗi ký tự qua tầng tiền xử lý chuỗi `string_utils.py`:
     * Loại bỏ các dấu chú thích footnote (ví dụ: `[1]`, `*`).
     * Chuyển đổi các ký tự phân số Unicode (`½` ➔ `1/2`).
     * Di chuyển các đoạn đóng mở ngoặc `(...)` về cuối chuỗi để tránh làm nhiễu đơn vị đo.
  3. Module `ingredient_parser.py` kết hợp mô hình NLP và biểu thức chính quy (Regex) để nhận diện biên ngữ nghĩa của số lượng, đơn vị và tên thực phẩm.
  4. Hệ thống trả về đối tượng `ParsedIngredient` chuẩn hóa dưới dạng JSON.
* **Hậu điều kiện:** Dữ liệu nguyên liệu được cấu trúc hóa, sẵn sàng cho việc tính toán dinh dưỡng, co giãn khẩu phần và tự động đi chợ.

---

### 3. UC-03: Tự động co giãn tỉ lệ khẩu phần ăn (Servings Scaling)
> **Ghi chú học thuật:** Đây là nghiệp vụ được lập trình kiểm thử chuyên sâu tại **Property 4** (do Trưởng nhóm Trần Quốc Quân trực tiếp phụ trách).

* **Mã Use Case:** `UC-03`
* **Tác nhân:** Home User
* **Mô tả:** Tự động tính toán lại định lượng của tất cả các nguyên liệu trong công thức nấu ăn khi thay đổi số lượng người ăn.
* **Công thức toán học:**
  $$\text{Hệ số co giãn } k = \frac{\text{Số khẩu phần mong muốn (Target Servings)}}{\text{Số khẩu phần gốc (Original Servings)}}$$
  $$\text{Định lượng mới } Q_{\text{mới}} = Q_{\text{gốc}} \times k$$
* **Luồng sự kiện chính (Main Flow):**
  1. Người dùng mở trang chi tiết một món ăn (ví dụ: công thức gốc thiết kế cho $4$ người ăn).
  2. Người dùng nhấn nút tăng khẩu phần lên $8$ người ăn ($k = 8/4 = 2.0$).
  3. Hệ thống duyệt qua toàn bộ danh sách nguyên liệu của công thức:
     * Lấy giá trị định lượng gốc $Q_{\text{gốc}}$.
     * Thực hiện phép nhân số thực: $Q_{\text{mới}} = Q_{\text{gốc}} \times 2.0$.
     * Cập nhật hiển thị số lượng mới trên giao diện (ví dụ: $200\text{g đường}$ ➔ $400\text{g đường}$).
  4. Nếu khẩu phần ăn bị giảm về $2$ người ($k = 2/4 = 0.5$), số lượng đường tự động giảm còn $100\text{g}$.
* **Hậu điều kiện:** Người nấu nắm được chính xác khối lượng nguyên liệu cần chuẩn bị mà không cần phải tự tính nhẩm thủ công.

---

### 4. UC-04: Lập kế hoạch thực đơn tuần (Meal Planning)
* **Mã Use Case:** `UC-04`
* **Tác nhân:** Home User
* **Mô tả:** Cho phép người dùng lên lịch các món ăn sẽ nấu cho từng ngày trong tuần (từ Thứ Hai đến Chủ Nhật), phân chia theo các bữa ăn trong ngày.
* **Luồng sự kiện chính (Main Flow):**
  1. Người dùng truy cập trang *"Meal Planner"*, chọn khoảng thời gian tuần cần lên kế hoạch.
  2. Người dùng kéo thả (drag & drop) hoặc chọn công thức từ thư viện món ăn vào từng ô thời gian cụ thể (Bữa sáng, Bữa trưa, Bữa tối).
  3. Hệ thống lưu thông tin kế hoạch vào bảng `mealplans` kèm theo ngày thực hiện (`entry_date`).
  4. Người dùng bấm nút *"Add to Shopping List"*, hệ thống tự động tổng hợp tất cả nguyên liệu của các món ăn trong tuần và gom vào danh sách mua sắm.
* **Hậu điều kiện:** Lịch trình ăn uống của gia đình được thiết lập rõ ràng, hạn chế lãng phí thực phẩm.

---

### 5. UC-05: Quy đổi đơn vị đo lường ẩm thực (Unit Conversion)
> **Ghi chú học thuật:** Đây là nghiệp vụ được lập trình kiểm thử chuyên sâu tại **Property 2** (do Bùi Trung Hiếu phụ trách).

* **Mã Use Case:** `UC-05`
* **Tác nhân:** Home User, hoặc được kích hoạt tự động khi tổng hợp danh sách mua sắm.
* **Mô tả:** Chuyển đổi định lượng nguyên liệu giữa các đơn vị đo lường tương đương hoặc khác hệ thống đo lường (Metric $\leftrightarrow$ Imperial).
* **Luồng sự kiện chính (Main Flow):**
  1. Người dùng có công thức nấu ăn xuất xứ từ Mỹ sử dụng đơn vị Imperial (ví dụ: $2\text{ cups sữa}$ hoặc $16\text{ oz bột mì}$).
  2. Người dùng kích hoạt tính năng chuyển đổi sang hệ đo lường Quốc tế (Metric).
  3. Lớp `UnitConverter` (trong `mealie/services/parser_services/parser_utils/unit_utils.py`) sử dụng thư viện `Pint` để thực hiện phép ánh xạ:
     * Kiểm tra hai đơn vị có cùng thứ nguyên vật lý hay không (ví dụ: cùng là thể tích hoặc cùng là khối lượng).
     * Áp dụng hệ số chuyển đổi chuẩn (ví dụ: $1\text{ cup} \approx 236.588\text{ ml}$; $1\text{ kg} = 1000\text{ gram}$).
  4. Hệ thống trả về kết quả quy đổi chính xác kèm đơn vị mới.
* **Hậu điều kiện:** Người dùng có thể dễ dàng chuẩn bị nguyên liệu bằng các dụng cụ cân đong sẵn có tại gia đình.

---

## 🌳 A.4. KHẢO SÁT CÂY THƯ MỤC MÃ NGUỒN MEALIE (v3.28.0)

Qua việc clone và khảo sát trực tiếp mã nguồn trong thư mục `mealie_src/`, cây thư mục tổng thể của Mealie được tổ chức rất chặt chẽ theo mô hình **Kiến trúc phân tầng (Layered Architecture)**:

```text
mealie_src/
├── pyproject.toml                 # Khai báo dependency, packaging, metadata của Mealie v3.28.0
├── Taskfile.yml                   # Cấu hình các lệnh tự động hóa phát triển (build, lint, test)
│
├── frontend/                      # TOÀN BỘ GIAO DIỆN NGƯỜI DÙNG (VUE.JS / NUXT SPA)
│   ├── components/                # Các thành phần UI giao diện tái sử dụng
│   ├── pages/                     # Các trang màn hình: recipes, mealplanner, settings
│   └── package.json               # Khai báo thư viện JavaScript/NodeJS
│
└── mealie/                        # TOÀN BỘ MÃ NGUỒN BACKEND (PYTHON / FASTAPI)
    ├── main.py                    # Entry point kích hoạt máy chủ Uvicorn
    ├── app.py                     # Khởi tạo FastAPI application, middlewares, scheduler, router
    │
    ├── routes/                    # TẦNG TIẾP NHẬN & ĐIỀU HƯỚNG API (API ROUTING LAYER)
    │   ├── __init__.py            # Gom toàn bộ route con dưới tiền tố "/api"
    │   ├── recipe.py              # API quản lý công thức, hình ảnh và khẩu phần ăn (/api/recipes)
    │   ├── parser.py              # API tiếp nhận chuỗi nguyên liệu để bóc tách (/api/parser)
    │   ├── unit_and_foods.py      # API quản lý danh mục thực phẩm & đơn vị đo (/api/units)
    │   ├── households.py          # API phân quyền không gian gia đình
    │   └── auth.py & users.py     # API chứng thực JWT và thông tin người dùng
    │
    ├── services/                  # TẦNG XỬ LÝ NGHIỆP VỤ CỐT LÕI (CORE BUSINESS SERVICES)
    │   ├── recipe/                # Nghiệp vụ quản lý công thức, tính toán khẩu phần ăn (Scaling)
    │   ├── scraper/               # Engine cào dữ liệu từ URL ẩm thực bên ngoài
    │   ├── scheduler/             # Lập lịch tác vụ chạy nền (Cron jobs, dọn dẹp token)
    │   │
    │   └── parser_services/       # TÂM ĐIỂM KIỂM THỬ CỦA ĐỒ ÁN (PARSER & UTILS)
    │       ├── _base.py           # Interface và lớp cơ sở cho các bộ parser
    │       ├── ingredient_parser.py # Lớp BruteForceParser bóc tách chuỗi nguyên liệu tự nhiên
    │       │
    │       └── parser_utils/      # BỘ TIỆN ÍCH XỬ LÝ CHUỖI & ĐƠN VỊ ĐO LƯỜNG
    │           ├── string_utils.py  # Xử lý chuỗi, phân số vulgar, footnote, dấu ngoặc
    │           └── unit_utils.py    # Lớp UnitConverter quy đổi thứ nguyên đo lường
    │
    ├── schema/                    # TẦNG KHUÔN MẪU DỮ LIỆU (PYDANTIC SCHEMAS)
    │   ├── recipe/                # Schema công thức, nguyên liệu (RecipeIngredient, IngredientBase)
    │   └── parser/                # Schema kết quả phân tích (ParsedIngredient)
    │
    ├── db/ & repos/               # TẦNG TRUY XUẤT CƠ SỞ DỮ LIỆU (DATA ACCESS LAYER)
    │   ├── init_db.py             # Khởi tạo kết nối DB, tự động chạy migration khi khởi động
    │   └── models/                # Các lớp thực thể ánh xạ bảng SQLAlchemy (ORM Models)
    │
    └── core/                      # CẤU HÌNH HỆ THỐNG & TIỆN ÍCH CHUNG
        ├── config.py              # Đọc biến môi trường, thiết lập ứng dụng
        └── root_logger.py         # Cấu hình hệ thống ghi log chi tiết
```

### Điểm nhấn kiến trúc phục vụ kiểm thử PBT (Hypothesis):
* Nhóm nhận thấy rằng toàn bộ module **`mealie/services/parser_services/`** và logic scaling trong **`mealie/services/recipe/`** được thiết kế dưới dạng **các hàm thuần túy (Pure Functions / Stateless Services)**:
  * Nhận dữ liệu đầu vào (chuỗi ký tự, con số tỉ lệ).
  * Thực hiện phép biến đổi chuỗi và tính toán toán học.
  * Trả về kết quả đầu ra có cấu trúc mà không cần phụ thuộc vào database bên ngoài hay giao diện người dùng.
* Đây chính là môi trường lý tưởng nhất để áp dụng kỹ thuật **Property-Based Testing (K01)**, cho phép nhóm sinh hàng chục nghìn bộ dữ liệu đầu vào ngẫu nhiên và dị biệt để kiểm tra tính toàn vẹn và độ bền vững của mã nguồn hệ thống.

---

## 🎯 TỔNG KẾT PHẦN A
Phần A đã phác họa bức tranh toàn cảnh về hệ thống Mealie `v3.28.0`:
1. **Mục tiêu rõ ràng:** Một nền tảng quản lý ẩm thực toàn diện, giải quyết triệt để vấn đề phân mảnh công thức và tính toán khẩu phần.
2. **Stack công nghệ mạnh mẽ:** Nền tảng hiện đại với Python FastAPI, SQLAlchemy, Pydantic và Vue.js.
3. **5 Use Case cốt lõi:** Định hình rõ các luồng nghiệp vụ quan trọng, trong đó làm nổi bật 3 nghiệp vụ trọng tâm sẽ được kiểm thử bằng PBT: *Bóc tách nguyên liệu*, *Quy đổi đơn vị*, và *Co giãn khẩu phần ăn*.
4. **Cấu trúc mã nguồn tường minh:** Xác định chính xác vị trí các module mục tiêu tại `mealie/services/parser_services/`, tạo tiền đề vững chắc cho việc vẽ **Sơ đồ kiến trúc C4 Container và 3 Luồng dữ liệu (Data Flow)** tại **Phần B** tiếp theo.
