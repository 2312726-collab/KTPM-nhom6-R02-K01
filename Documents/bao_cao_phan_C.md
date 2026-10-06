# PHẦN C — HƯỚNG DẪN CÀI ĐẶT & VẬN HÀNH MÔI TRƯỜNG KIỂM THỬ

**Đồ án: Kiểm thử Phần mềm — Nhóm 6**
**Hệ thống: Mealie v3.28.0 (Recipe Manager & Meal Planner)**
**Người thực hiện: Nguyễn Phạm Phú Nam — Vai trò: DevOps & Automation QA**
**Môi trường đã kiểm chứng: Windows 11 + Docker Desktop**

---

## C.1 — Yêu cầu môi trường

### Hệ điều hành đã kiểm chứng

| Thành phần | Phiên bản đã thử | Ghi chú |
|---|---|---|
| Windows | 11 (Build 22H2 trở lên) | Môi trường chính đã kiểm chứng |
| Docker Desktop for Windows | 4.28.0+ | Cần WSL 2 backend hoặc Hyper-V |
| Docker Engine | 26.0+ | Đi kèm Docker Desktop |
| Docker Compose | v2 (plugin) | Đi kèm Docker Desktop |
| Git | 2.40+ | Để clone repo và quản lý nhánh |
| Python | 3.11+ | Để chạy seed data và test |

> **Lưu ý Linux:** Nếu dùng Linux, thay `host.docker.internal` trong `HTTP_ALLOW_LIST` bằng địa chỉ IP cầu nội bộ Docker (`172.17.0.1` hoặc output của `ip route | grep default | awk '{print $3}'`). Cấu hình này chưa được kiểm chứng trong dự án.

### Phiên bản Mealie đã pin

- **Tag:** `v3.28.0`
- **Source SHA:** `0552eaa4a80031b8572849cca0ed95d07f1be001`
- **Image:** `ghcr.io/mealie-recipes/mealie:v3.28.0`
- **Ngày chốt:** 06/10/2026

### Cổng sử dụng

| Dịch vụ | Cổng host | Cổng container | Mục đích |
|---|---|---|---|
| Mealie Web UI | **9925** | 9000 | Giao diện chính |
| Mock Recipe Server | **9926** | 9926 | Server công thức mẫu cho import URL |

Đảm bảo hai cổng trên **không bị chiếm** trước khi khởi động.

### Tài khoản demo

| Loại | Email | Mật khẩu |
|---|---|---|
| Admin | `admin@nhom6.test` | `Admin123@` |
| Người dùng thường | `test@nhom6.test` | `User123@` |

> Tài khoản Admin **không có sẵn** trong image Mealie gốc. Phải tạo thủ công sau khi khởi động lần đầu (xem C.2).

---

## C.2 — Cài đặt chi tiết

### Bước 1: Clone repo đúng nhánh

```powershell
# Clone repo nhóm
git clone https://github.com/2312726-collab/KTPM-nhom6-K02-R01.git
cd KTPM-nhom6-K02-R01

# Checkout nhánh của Nam (chứa Docker, seed data và test P5)
git checkout feat/nam-property-5-fraction
```

### Bước 2: Tạo file `.env` từ mẫu

```powershell
# Chuyển vào thư mục mealie_docker
cd mealie_docker

# Sao chép mẫu cấu hình
Copy-Item .env.example .env
```

Nội dung mặc định của `.env`:

```env
MEALIE_PORT=9925
ALLOW_SIGNUP=true
BASE_URL=http://localhost:9925
LOG_LEVEL=DEBUG
DB_ENGINE=sqlite
HTTP_ALLOW_LIST=host.docker.internal
```

> `.env` là file local, **không được commit** vào Git.

### Bước 3: Khởi động Mealie bằng Docker Compose

```powershell
# Phải đứng trong thư mục mealie_docker/
cd mealie_docker

# Kéo image và khởi động container
docker compose up -d

# Kiểm tra container đang chạy
docker compose ps
```

Kết quả mong đợi:
```
NAME      IMAGE                                    STATUS    PORTS
mealie    ghcr.io/mealie-recipes/mealie:v3.28.0   running   0.0.0.0:9925->9000/tcp
```

### Bước 4: Kiểm tra log và trạng thái khởi động

```powershell
# Xem log khởi động (Ctrl+C để thoát)
docker compose logs -f mealie
```

Chờ xuất hiện dòng `Application startup complete` hoặc `Uvicorn running on` trước khi tiếp tục. Thường mất 15–30 giây.

### Bước 5: Truy cập và tạo Admin

Mở trình duyệt: **http://localhost:9925**

![Giao diện Landing của Mealie](assets/01_mealie_landing.png)

*Hình C.2.1 — Giao diện trang chủ Mealie lần đầu truy cập*

Khi đăng nhập lần đầu, Mealie yêu cầu tạo tài khoản đầu tiên (Admin):

1. Nhấn **Get Started** hoặc truy cập `/register`.
2. Điền:
   - **Email:** `admin@nhom6.test`
   - **Username:** `admin`
   - **Password:** `Admin123@`
   - **Confirm Password:** `Admin123@`
3. Nhấn **Create Account**.

> Nếu `ALLOW_SIGNUP=true` trong `.env`, trang đăng ký mở công khai. Tài khoản đầu tiên tạo ra sẽ là Admin.

Sau khi đăng nhập Admin, Dashboard hiển thị:

![Dashboard Mealie sau đăng nhập](assets/02_mealie_dashboard.png)

*Hình C.2.2 — Dashboard Mealie sau khi Admin đăng nhập thành công*

### Bước 6: Cài đặt môi trường Python cho seed/test

Từ **thư mục gốc repo**:

```powershell
# Tạo virtual environment
python -m venv .venv

# Kích hoạt (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Nếu bị lỗi execution policy:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Cài dependencies kiểm thử
pip install -r requirements-test.txt
```

---

## C.3 — Quản lý dịch vụ Docker

### Lệnh thường dùng

```powershell
# Phải đứng trong mealie_docker/ cho các lệnh compose
cd mealie_docker

# Khởi động (chế độ nền)
docker compose up -d

# Xem trạng thái container
docker compose ps

# Xem log realtime
docker compose logs -f mealie

# Xem log 100 dòng cuối
docker compose logs --tail=100 mealie

# Dừng container (giữ nguyên dữ liệu)
docker compose stop

# Dừng và xóa container (giữ volume dữ liệu)
docker compose down

# Restart container
docker compose restart mealie
```

### Named Volume và bảo toàn dữ liệu

Cấu hình trong `docker-compose.yml`:

```yaml
volumes:
  - mealie-data:/app/data/
```

Toàn bộ dữ liệu Mealie (công thức, thực đơn, tài khoản) được lưu trong **named volume** `mealie-data`. Volume này **tồn tại độc lập** với container:

| Lệnh | Tác động lên container | Tác động lên dữ liệu |
|---|---|---|
| `docker compose stop` | Container dừng | **Giữ nguyên** |
| `docker compose down` | Container + network bị xóa | **Giữ nguyên** |
| `docker compose up -d` | Tạo container mới | Nhận lại volume cũ |
| `docker compose down -v` | Container + network bị xóa | **XÓA TOÀN BỘ** |

> ⚠️ **KHÔNG chạy** `docker compose down -v` hoặc `docker volume rm mealie-data` như thao tác dừng thường lệ.

```powershell
# Xem danh sách volume
docker volume ls | findstr mealie
```

---

## C.4 — Seed Data và ba luồng nghiệp vụ cốt lõi

### Chuẩn bị

Đảm bảo:
1. Container Mealie đang chạy (`docker compose ps` → status `running`)
2. Tài khoản Admin `admin@nhom6.test` đã tạo (xem C.2 Bước 5)
3. Virtual environment đã kích hoạt (xem C.2 Bước 6)

Seed script đọc thông tin đăng nhập qua biến môi trường (mặc định dùng Admin):

| Biến | Giá trị mặc định | Ý nghĩa |
|---|---|---|
| `MEALIE_BASE_URL` | `http://localhost:9925` | URL Mealie |
| `MEALIE_EMAIL` | `admin@nhom6.test` | Tài khoản đăng nhập |
| `MEALIE_PASSWORD` | `Admin123@` | Mật khẩu |

### Chạy seed data

Từ thư mục gốc repo (`.venv` đã kích hoạt):

```powershell
# Chạy seed (idempotent — chạy lại không tạo trùng)
& ".\.venv\Scripts\python.exe" mealie_docker/seed/seed_data.py
```

Kết quả mong đợi:

```
Logging in to http://localhost:9925 as admin@nhom6.test...
Processing recipe: [NAM-01] Cháo Yến Mạch Sáng...
  -> Created with slug: nam-01-chao-yen-mach-sang
...
Processing recipe: [NAM-10] Bò Xào Tiêu Đen Scaling Test...
  -> Created with slug: nam-10-bo-xao-tieu-den-scaling-test
Setting up 7-day Meal Plan (06/10/2026 - 12/10/2026)...
  -> Created meal plan on 2026-10-06 (breakfast): Bữa sáng ngày 06/10
...
Seed data completed successfully!
```

### Kiểm tra kết quả seed

**Tài khoản người dùng thường — tạo từ Admin:**

1. Đăng nhập Admin → **Admin Panel** → **Manage Users** → **Create User**
2. Điền Email: `test@nhom6.test`, Password: `User123@`, Role: User
3. Nhấn **Save**

**10 công thức NAM-01 đến NAM-10:**

Vào **Recipes** → kiểm tra 10 công thức có tiền tố `[NAM-` trong tên.

**Thực đơn 7 ngày:**

Vào **Meal Planner** → điều hướng đến tuần **06/10–12/10/2026** → xác nhận 14 bữa (2 bữa mỗi ngày: sáng + tối).

![Kế hoạch thực đơn 7 ngày](assets/03_meal_plan.png)

*Hình C.4.1 — Thực đơn 7 ngày tuần 06/10–12/10/2026 sau khi seed*

### Luồng 1 — Import công thức từ URL

Nhóm cung cấp server mẫu phục vụ công thức định dạng JSON-LD trên cổng **9926**.

**Bước 1:** Khởi động server mẫu (terminal riêng, giữ mở):

```powershell
# Terminal riêng, từ thư mục gốc repo
& ".\.venv\Scripts\python.exe" mealie_docker/seed/mock_recipe_server.py
```

Server chạy tại `http://localhost:9926`. Kiểm tra từ host:

```powershell
Invoke-WebRequest http://localhost:9926/recipe/pho-bo -UseBasicParsing | Select-Object StatusCode
```

**Bước 2:** Import trong Mealie UI:

1. Đăng nhập Mealie → **Recipes** → **Create** → **Import from URL**
2. Điền URL: `http://host.docker.internal:9926/recipe/pho-bo`
   - Container dùng `host.docker.internal` để trỏ về host (không phải `localhost`)
3. Nhấn **Import**

Kết quả: Công thức `Phở Bò Hà Nội` được tạo với 5 nguyên liệu, 3 bước và khẩu phần 4.

![Import công thức từ URL](assets/04_recipe_import.png)

*Hình C.4.2 — Công thức `pho-bo-ha-noi` đã import thành công từ mock server*

### Luồng 2 — Phân tích nguyên liệu (Ingredient Parsing)

1. Mở bất kỳ công thức → **Edit** → phần **Ingredients**
2. Nhấn **Parse All** hoặc nhập nguyên liệu và nhấn **Parse**
3. Nhập chuỗi: `1 onion (finely chopped)`

Kết quả parser bóc tách:

| Trường | Giá trị |
|---|---|
| Qty | 1 |
| Unit | (trống — không xác định đơn vị) |
| Food | onion |
| Note | finely chopped |

![Kết quả Ingredient Parsing](assets/05_ingredient_parse.png)

*Hình C.4.3 — Parser bóc tách `1 onion (finely chopped)` thành Qty=1, Food=onion, Note=finely chopped*

### Luồng 3 — Nhân tỉ lệ khẩu phần (Servings Scaling)

Sử dụng công thức **NAM-10** (`Bò Xào Tiêu Đen Scaling Test`) — được thiết kế với Food/Unit phù hợp.

1. Mở công thức NAM-10
2. Tại trường **Servings**, đổi từ **4** thành **8** (nhân đôi)
3. Mealie tự động nhân đôi tất cả lượng nguyên liệu:

| Nguyên liệu | Gốc (4 servings) | Sau scaling (8 servings) |
|---|---|---|
| Beef | 400g | 800g |
| Black pepper | 2 tbsp | 4 tbsp |
| Beef broth | 1/2 cup | 1 cup |
| Garlic | 4 cloves | 8 cloves |

![Scaling khẩu phần ăn](assets/06_servings_scale.png)

*Hình C.4.4 — NAM-10 scale từ 4 lên 8 servings — tất cả nguyên liệu nhân đôi chính xác*

---

## C.5 — Xử lý sự cố thường gặp

### Lỗi 1: Xung đột cổng (Port Conflict)

**Triệu chứng:**
```
Error response from daemon: Ports are not available:
  address already in use 0.0.0.0:9925
```

**Xử lý:**

```powershell
# Tìm tiến trình đang dùng cổng 9925
netstat -ano | findstr :9925

# Xem PID (cột cuối) rồi kill
taskkill /PID <PID> /F
```

Hoặc đổi cổng trong `mealie_docker/.env`:
```env
MEALIE_PORT=9930
BASE_URL=http://localhost:9930
```

Nếu cổng 9926 bị chiếm, đổi biến `PORT = 9926` trong `mock_recipe_server.py`.

### Lỗi 2: Quyền thư mục / Volume permission

**Triệu chứng:** Container không ghi được vào `/app/data/` hoặc dữ liệu không lưu.

**Xử lý:**
```powershell
# Kiểm tra volume
docker volume inspect mealie-data

# Nếu bị lỗi, tạo lại (CHỈ dùng trên máy cài mới — XÓA DỮ LIỆU)
docker compose down
docker volume rm mealie-data
docker compose up -d
```

### Lỗi 3: Docker Daemon chưa khởi động

**Triệu chứng:**
```
error during connect: This error may indicate that the docker daemon is not running.
```

**Xử lý:**
1. Mở **Docker Desktop** từ Start Menu
2. Chờ icon Docker ở taskbar ổn định (không còn spinning)
3. Chạy lại `docker compose up -d`

### Lỗi 4: Không đăng nhập được Mealie

**Triệu chứng:** Trang đăng nhập báo lỗi dù nhập đúng email/password.

**Xử lý:**
```powershell
# Kiểm tra container đang chạy
docker compose ps

# Xem log
docker compose logs --tail=50 mealie

# Thử restart
docker compose restart mealie
```

Nếu chưa tạo Admin: Truy cập `http://localhost:9925/register` và tạo theo C.2 Bước 5.

### Lỗi 5: Container không truy cập được mock server

**Triệu chứng:** Import URL `http://host.docker.internal:9926/recipe/pho-bo` trả về lỗi kết nối trong Mealie.

**Kiểm tra:**
```powershell
# Xác nhận mock server đang chạy từ host
Invoke-WebRequest http://localhost:9926/recipe/pho-bo -UseBasicParsing | Select-Object StatusCode

# Xác nhận cấu hình HTTP_ALLOW_LIST
docker inspect mealie | findstr HTTP_ALLOW_LIST
```

**Nguyên nhân thường gặp:**
1. Mock server chưa khởi động — chạy `mock_recipe_server.py` trong terminal riêng và giữ mở.
2. `HTTP_ALLOW_LIST` thiếu trong `.env` — thêm `HTTP_ALLOW_LIST=host.docker.internal` và restart container.
3. Trên Linux: `host.docker.internal` không tự resolve — dùng IP cầu Docker (xem ghi chú C.1).

### Lỗi 6: Seed script báo lỗi đăng nhập

**Triệu chứng:**
```
RuntimeError: POST /api/auth/token failed: 401 - ...
```

**Xử lý:**
```powershell
# Ghi đè biến môi trường nếu cần
$env:MEALIE_BASE_URL = "http://localhost:9925"
$env:MEALIE_EMAIL = "admin@nhom6.test"
$env:MEALIE_PASSWORD = "Admin123@"

# Chạy lại seed
& ".\.venv\Scripts\python.exe" mealie_docker/seed/seed_data.py
```

### Lỗi 7: pytest thu thập 0 test

**Triệu chứng:**
```
collected 0 items
exit code 5
```

**Giải thích:** Ở thời điểm báo cáo này, file `tests/unit_tests/test_pbt_fraction.py` chưa được tạo (N4 đang thực hiện). Exit code **5** là bình thường, không phải lỗi môi trường.

Sau khi N4 hoàn thành:
```powershell
& ".\.venv\Scripts\python.exe" -m pytest tests/unit_tests/test_pbt_fraction.py --collect-only -q
& ".\.venv\Scripts\python.exe" -m pytest tests/unit_tests/test_pbt_fraction.py -v --tb=long
```

---

*Tài liệu do Nguyễn Phạm Phú Nam biên soạn — cập nhật: 07/10/2026*
*Môi trường kiểm chứng: Windows 11 + Docker Desktop + Mealie v3.28.0*