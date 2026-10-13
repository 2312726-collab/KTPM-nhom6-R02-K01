# PHÂN TÍCH HỆ THỐNG & SƠ ĐỒ KIẾN TRÚC MEALIE

---

## 1. PHÂN TÍCH MÃ NGUỒN VÀ CẤU TRÚC HỆ THỐNG

### 1.1. Tổng quan kiến trúc mã nguồn
Hệ thống **Mealie** được thiết kế theo mô hình phân tầng chặt chẽ (**Layered Architecture**) kết hợp mô hình **Repository - Service - Controller**, phân tách độc lập giữa tầng giao diện người dùng (Frontend SPA) và tầng xử lý nghiệp vụ/dịch vụ dữ liệu (Backend RESTful API).

```
f:\KTPM\mealie
├── mealie/                     # [BACKEND] Mã nguồn lõi Python FastAPI
│   ├── alembic/                # Database migrations (Alembic)
│   ├── core/                   # Cấu hình, bảo mật, jwt tokens, settings
│   ├── db/models/              # SQLAlchemy ORM Data Models
│   ├── repos/                  # Data Access Layer (Repository Pattern)
│   ├── routes/                 # API Controllers & Routers (FastAPI)
│   ├── schema/                 # Pydantic Schemas (In/Out/Create/Update)
│   ├── services/               # Business Logic Layer (Dịch vụ nghiệp vụ)
│   └── app.py / main.py        # Điểm khởi chạy ứng dụng backend
├── frontend/                   # [FRONTEND] Mã nguồn Nuxt 4 + Vue 3
│   ├── app/
│   │   ├── components/         # Giao diện Domain, Global, Layout
│   │   ├── composables/        # State Management, Auth, API Composables
│   │   ├── lib/api/            # Typed API Clients tương tác Backend
│   │   ├── pages/              # File-system routing (Nuxt Pages)
│   │   └── lang/               # Đa ngôn ngữ (i18n locales)
│   ├── package.json            # Quản lý dependencies Frontend
│   └── nuxt.config.ts          # Cấu hình Nuxt 4 framework
├── docker/                     # Cấu hình Dockerfile, entrypoint & dev compose
├── Taskfile.yml                # Tự động hóa các tác vụ (Build, Test, Lint, Migrate)
└── pyproject.toml              # Quản lý dependencies & metadata Backend (uv)
```

---

### 1.2. Nhận diện các Module và Dependency chính

#### A. Backend (Python 3.14 + FastAPI)
Quản lý tập trung qua `pyproject.toml` và `uv.lock`:

| Phân loại | Thư viện / Dependency chính | Vai trò kỹ thuật trong hệ thống |
| :--- | :--- | :--- |
| **Web Framework & API** | `fastapi==0.142.2`, `uvicorn[standard]==0.54.0` | Cung cấp RESTful API hiệu năng cao, dependency injection, xử lý bất đồng bộ (asyncio), tự động sinh Swagger/OpenAPI docs. |
| **Data Validation & DTO** | `pydantic==2.13.5`, `pydantic-settings==2.15.0` | Định nghĩa schemas, xác thực dữ liệu đầu vào/ra nghiêm ngặt (`*In`, `*Out`, `*Create`, `*Update`). |
| **Cơ sở dữ liệu & ORM** | `SQLAlchemy`, `alembic`, `psycopg2-binary` | Quản lý kết nối DB (SQLite / PostgreSQL), ánh xạ quan hệ thực thể (ORM), tự động chạy migration phiên bản CSDL. |
| **Bảo mật & Xác thực** | `bcrypt==5.0.0`, `pyjwt==2.15.1`, `authlib==1.8.0` | Mã hóa mật khẩu bảo mật cao, cấp phát và xác thực JSON Web Token (JWT), hỗ trợ OIDC & LDAP. |
| **Xử lý dữ liệu & Bóc tách** | `recipe-scrapers==15.12.0`, `beautifulsoup4`, `extruct` | Tự động phân tích và trích xuất công thức nấu ăn chuẩn cấu trúc schema.org từ đường link trang web bất kỳ. |
| **Xử lý ngôn ngữ tự nhiên** | `ingredient-parser-nlp==2.8.0`, `pint==0.26.1` | Chuẩn hóa, bóc tách nguyên liệu, định lượng và chuyển đổi đơn vị đo lường thông minh. |
| **Tối ưu hóa I/O** | `orjson==3.12.0`, `httpx==0.28.1` | Tối ưu tuần tự hóa JSON tốc độ cao, HTTP client bất đồng bộ cho tác vụ ngoại vi. |

#### B. Frontend (Nuxt 4 + Vue 3 + TypeScript)
Quản lý tập trung qua `frontend/package.json`:

| Phân loại | Thư viện / Dependency chính | Vai trò kỹ thuật trong hệ thống |
| :--- | :--- | :--- |
| **Framework & Engine** | `nuxt==4.4.6`, `vue==3.5.35`, `vite` | Xây dựng Single Page Application (SPA), routing tự động, Server-Sent Events (SSE), tối ưu bundling. |
| **Giao diện & Thành phần UI** | `vuetify==4.1.2`, `@mdi/js`, `vuetify-nuxt-module` | Thư viện Material Design UI responsive, bộ icon MDI, hỗ trợ Dark/Light theme. |
| **Quản lý trạng thái (State)** | Vue Composables, `@vueuse/core` | Quản lý trạng thái toàn cục (Auth, Household Context, Settings) không cần Vuex phức tạp. |
| **HTTP Client** | `axios==1.8.1` | Tương tác với FastAPI backend, gắn kèm JWT Bearer Token trong interceptors. |
| **Đa ngôn ngữ & Tiện ích** | `@nuxtjs/i18n`, `date-fns`, `fuse.js` | Hỗ trợ 35+ ngôn ngữ, định dạng ngày tháng theo locale, tìm kiếm mờ (fuzzy search) tại client. |

---

## 2. SƠ ĐỒ KIẾN TRÚC HỆ THỐNG

### 2.1. Sơ đồ kiến trúc mức Container / Component (C4 Model - Container Level)

Hệ thống được thiết kế theo cấu trúc mô-đun hóa với ranh giới phân tách rõ ràng giữa Client, Web Server, Controller, Service, Repository và Database:

```mermaid
flowchart TB
    subgraph ClientLayer["🖥️ Client Layer (User Interface)"]
        Browser["Trình duyệt Web (Desktop / Mobile PWA)"]
    end

    subgraph FrontendApp["🌐 Frontend Application (Nuxt 4 / Vue 3)"]
        UIComponents["Vue Components (Domain / Global / Layout)"]
        Composables["Composables (useMealieAuth, useUserApi)"]
        APIClient["Typed Axios API Client"]
        UIComponents --> Composables
        Composables --> APIClient
    end

    subgraph BackendApp["⚙️ Backend Application (FastAPI / Python 3.14)"]
        subgraph RouteLayer["Routing & Controllers (mealie/routes)"]
            AuthController["Auth Controller (/api/auth)"]
            RecipeController["Recipe Controller (/api/recipes)"]
            MealPlanController["MealPlan Controller (/api/households/mealplans)"]
            ShoppingController["ShoppingList Controller (/api/households/shopping)"]
        end

        subgraph ServiceLayer["Business Logic Layer (mealie/services)"]
            AuthService["Security & Token Service"]
            RecipeService["Recipe Data & Scraping Service"]
            MealPlanService["Meal Planning & Rules Service"]
            ShoppingService["Shopping List Service"]
            EventBus["Event Bus & Notification Service"]
        end

        subgraph RepoLayer["Data Access Layer (mealie/repos)"]
            RepoFactory["AllRepositories Factory"]
            RepoUsers["RepositoryUsers"]
            RepoRecipes["RepositoryRecipes"]
            RepoMeals["RepositoryMeals"]
            RepoShopping["RepositoryShoppingLists"]
        end
    end

    subgraph StorageLayer["💾 Data & Storage Layer"]
        DB[(Cơ sở dữ liệu: SQLite / PostgreSQL)]
        FileSystem["File System (/app/data: Images, OCR, Backups)"]
    end

    subgraph ExternalServices["🌍 External Services"]
        WebScraper["Website nấu ăn bên ngoài (Schema.org)"]
        SMTPMail["Dịch vụ Email / SMTP Server"]
    end

    %% Tương tác luồng
    Browser -->|HTTP/HTTPS REST & SSE| FrontendApp
    APIClient -->|JSON REST API Requests| RouteLayer

    AuthController --> AuthService
    RecipeController --> RecipeService
    MealPlanController --> MealPlanService
    ShoppingController --> ShoppingService

    RecipeService --> EventBus
    MealPlanService --> EventBus
    ShoppingService --> EventBus

    AuthService --> RepoFactory
    RecipeService --> RepoFactory
    MealPlanService --> RepoFactory
    ShoppingService --> RepoFactory

    RepoFactory --> RepoUsers
    RepoFactory --> RepoRecipes
    RepoFactory --> RepoMeals
    RepoFactory --> RepoShopping

    RepoUsers -->|SQLAlchemy ORM| DB
    RepoRecipes -->|SQLAlchemy ORM| DB
    RepoMeals -->|SQLAlchemy ORM| DB
    RepoShopping -->|SQLAlchemy ORM| DB

    RecipeService -->|Lưu ảnh món ăn| FileSystem
    RecipeService -.->|Bóc tách HTML/JSON-LD| WebScraper
    EventBus -.->|Gửi thông báo| SMTPMail
```

---

## 3. PHÂN TÍCH & BIỂU DIỄN LUỒNG DỮ LIỆU (DATA FLOW) TRỌNG TÂM

Dưới đây là 04 luồng nghiệp vụ cốt lõi, phản ánh đầy đủ chu trình xử lý dữ liệu từ Client đến Database và là phạm vi trọng tâm cho công tác kiểm thử hệ thống.

---

### 3.1. Luồng 1: Xác thực & Đăng nhập người dùng (Authentication & Authorization)
*Mục tiêu*: Chứng thực danh tính người dùng bằng email/password, cấp phát JWT Access Token và thiết lập ngữ cảnh nhóm/hộ gia đình (Multi-tenancy context).

```mermaid
sequenceDiagram
    autonumber
    actor User as Người dùng
    participant UI as Nuxt Web Client
    participant AuthCtrl as Auth Controller (/api/auth/token)
    participant SecService as Security & Token Provider
    participant UserRepo as RepositoryUsers
    participant DB as Database (SQLite/PostgreSQL)

    User->>UI: Nhập Email/Username và Password
    UI->>AuthCtrl: POST /api/auth/token (form-data: username, password)
    AuthCtrl->>UserRepo: get_by_email_or_username(username)
    UserRepo->>DB: SELECT * FROM users WHERE email = ?
    DB-->>UserRepo: Trả về bản ghi User (Password hash, group_id, household_id)
    UserRepo-->>AuthCtrl: Đối tượng PrivateUser
    AuthCtrl->>SecService: verify_password(plain_password, hashed_password)
    SecService-->>AuthCtrl: Password hợp lệ (True)
    AuthCtrl->>SecService: generate_token(user_id, group_id, household_id)
    SecService-->>AuthCtrl: JWT Access Token (Thời hạn 48 giờ)
    AuthCtrl-->>UI: 200 OK: { access_token, token_type: "bearer" }
    UI->>UI: Lưu Token vào LocalStorage / Pinia Store
    Note over UI,AuthCtrl: Các Request sau sẽ đính kèm Header: Authorization: Bearer <Token>
```

---

### 3.2. Luồng 2: Quản lý & Tạo mới Công thức nấu ăn (Recipe Management)
*Mục tiêu*: Tạo mới món ăn, tự động tạo slug duy nhất, lưu trữ nguyên liệu, thời gian, khẩu phần và hướng dẫn chế biến.

```mermaid
sequenceDiagram
    autonumber
    actor User as Đầu bếp / Người dùng
    participant UI as Nuxt Recipe Form
    participant RecipeCtrl as Recipe Controller (/api/recipes)
    participant RecipeSvc as Recipe Data Service
    participant RecipeRepo as RepositoryRecipes
    participant EventBus as Event Bus
    participant DB as Database

    User->>UI: Điền tên món ("Pho Bo Ha Noi"), nguyên liệu, các bước nấu
    UI->>RecipeCtrl: POST /api/recipes { name: "Pho Bo Ha Noi" }
    Note over RecipeCtrl: FastAPI kiểm tra JWT Token & lấy current_user
    RecipeCtrl->>RecipeSvc: create_one(CreateRecipe data)
    RecipeSvc->>RecipeSvc: slugify("Pho Bo Ha Noi") -> "pho-bo-ha-noi"
    RecipeSvc->>RecipeRepo: create(new_recipe_dict)
    RecipeRepo->>DB: INSERT INTO recipes (id, slug, name, household_id) VALUES (...)
    DB-->>RecipeRepo: Commit thành công (id: 94e3df6c-...)
    RecipeRepo-->>RecipeSvc: Recipe Entity
    RecipeSvc-->>RecipeCtrl: Recipe Slug ("pho-bo-ha-noi")
    RecipeCtrl-->>UI: 201 Created: "pho-bo-ha-noi"

    UI->>RecipeCtrl: PUT /api/recipes/pho-bo-ha-noi (Update full details)
    RecipeCtrl->>RecipeSvc: update_one(slug, full_recipe_payload)
    RecipeSvc->>RecipeRepo: update(recipe_data)
    RecipeRepo->>DB: UPDATE recipes, recipe_ingredients, recipe_instructions
    DB-->>RecipeRepo: Commit thành công
    RecipeSvc->>EventBus: publish(recipe_updated)
    RecipeSvc-->>RecipeCtrl: Updated Recipe Object
    RecipeCtrl-->>UI: 200 OK: Trả về toàn bộ chi tiết món ăn đã lưu
```

---

### 3.3. Luồng 3: Lập Kế hoạch Bữa ăn (Meal Planning Flow)
*Mục tiêu*: Lên lịch bữa ăn theo ngày, liên kết với công thức món ăn đã có trong hệ thống và hiển thị lên lịch trình gia đình.

```mermaid
sequenceDiagram
    autonumber
    actor User as Người dùng
    participant UI as Meal Planner UI
    participant MealCtrl as MealPlan Controller (/api/households/mealplans)
    participant MealRepo as RepositoryMeals
    participant EventBus as Event Bus
    participant DB as Database

    User->>UI: Chọn ngày (2026-10-11), chọn loại bữa (dinner), chọn món "Pho Bo Ha Noi"
    UI->>MealCtrl: POST /api/households/mealplans { date, entryType, recipeId, text }
    Note over MealCtrl: Kiểm tra user thuộc đúng household & group
    MealCtrl->>MealRepo: create_one(SavePlanEntry)
    MealRepo->>DB: INSERT INTO mealplans (date, entry_type, recipe_id, household_id, user_id)
    DB-->>MealRepo: Commit thành công (mealplan_id: 1)
    MealRepo-->>MealCtrl: ReadPlanEntry Object
    MealCtrl->>EventBus: publish(EventTypes.mealplan_entry_created)
    MealCtrl-->>UI: 201 Created: { id: 1, date: "2026-10-11", entryType: "dinner", recipe: {...} }
    UI->>UI: Render thẻ món ăn vào ô bữa tối trên giao diện Calendar
```

---

### 3.4. Luồng 4: Quản lý & Cập nhật Danh sách Mua sắm (Shopping List & Item Checking)
*Mục tiêu*: Quản lý danh sách nguyên liệu cần mua, đồng bộ trạng thái tick hoàn thành (Checked) khi đi chợ.

```mermaid
sequenceDiagram
    autonumber
    actor User as Người đi chợ
    participant UI as Shopping List UI
    participant ShopCtrl as Shopping Controller (/api/households/shopping)
    participant ShopSvc as Shopping List Service
    participant ShopRepo as RepositoryShoppingLists
    participant ItemRepo as RepositoryShoppingListItems
    participant DB as Database

    User->>UI: Tạo danh sách "Di cho cuoi tuan"
    UI->>ShopCtrl: POST /api/households/shopping/lists { name: "Di cho cuoi tuan" }
    ShopCtrl->>ShopSvc: create_one_list(ShoppingListCreate, user_id)
    ShopSvc->>ShopRepo: create(list_data)
    ShopRepo->>DB: INSERT INTO shopping_lists (...)
    DB-->>ShopRepo: Created (shopping_list_id: 1bda8992-...)
    ShopCtrl-->>UI: 201 Created (ShoppingListOut)

    User->>UI: Thêm mặt hàng ("500g Banh pho tuoi")
    UI->>ShopCtrl: POST /api/households/shopping/items { shoppingListId, note, checked: false }
    ShopCtrl->>ShopSvc: bulk_create_items([data])
    ShopSvc->>ItemRepo: create(item_data)
    ItemRepo->>DB: INSERT INTO shopping_list_items (...)
    DB-->>ShopCtrl: 201 Created (ShoppingListItemOut, id: item-123)

    User->>UI: Bấm tick vào ô "500g Banh pho tuoi" (Đã mua)
    UI->>ShopCtrl: PUT /api/households/shopping/items/item-123 { checked: true, note: "..." }
    ShopCtrl->>ItemRepo: update(item_id, { checked: true })
    ItemRepo->>DB: UPDATE shopping_list_items SET checked = 1 WHERE id = 'item-123'
    DB-->>ShopCtrl: Updated Success
    ShopCtrl-->>UI: 200 OK (Cập nhật giao diện: Gạch ngang chữ, chuyển sang nhóm Đã mua)
```

---

## 4. ĐÁNH GIÁ VÀ ĐỊNH HƯỚNG PHẠM VI KIỂM THỬ (TEST SCOPE)

Từ kiến trúc và các luồng dữ liệu trên, phạm vi kiểm thử trọng tâm bao gồm:

1. **Kiểm thử tích hợp API (Integration Testing)**:
   - Xác thực JWT token, phân quyền dữ liệu theo nhóm hộ gia đình (Household Multi-tenancy Isolation).
   - Kiểm tra ràng buộc dữ liệu Pydantic schema cho payload đầu vào của Recipes, Mealplans, Shopping Lists.
2. **Kiểm thử logic nghiệp vụ (Unit / Service Testing)**:
   - Đảm bảo tính toán thời gian, chuẩn hóa tên đơn vị/nguyên liệu (`ingredient-parser-nlp`).
   - Kiểm tra logic tự sinh slug món ăn không trùng lặp (`python-slugify`).
3. **Kiểm thử luồng dữ liệu liên thông (End-to-End Testing)**:
   - Luồng liên kết khép kín: **Công thức nấu ăn** -> Đưa vào **Kế hoạch bữa ăn** -> Tự động sinh nguyên liệu vào **Danh sách mua sắm** -> Đánh dấu hoàn tất khi mua hàng.
