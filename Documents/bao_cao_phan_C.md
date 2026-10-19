# PHẦN C — HƯỚNG DẪN CÀI ĐẶT & VẬN HÀNH MÔI TRƯỜNG KIỂM THỬ MEALIE

**Học phần:** Kiểm thử Phần mềm (Software Testing) — Mã lớp: CTK47-PM
**Đồ án:** Kiểm thử Hệ thống Quản lý Công thức & Kế hoạch Bữa ăn Mealie v3.28.0
**Nhóm thực hiện:** Nhóm 6
**Thành viên phụ trách:** Nguyễn Phạm Phú Nam (MSSV: 2312695) — Vai trò: DevOps & Automation QA
**Phạm vi phụ trách:** Nhiệm vụ N1, N2, N3 (Đóng gói Docker Compose, Kịch bản nạp dữ liệu mẫu Seed Data, Hướng dẫn On-boarding & Báo cáo Phần C)
**Nhánh làm việc:** `2312695-NguyenPhamPhuNam-Phan1` | **Pull Request:** #4 (nhánh đích `develop`)
**Môi trường kiểm chứng:** Windows 11 + Docker Desktop 29.7.2 (WSL 2 Backend) + Python 3.10–3.14

---

## MỤC LỤC BÁO CÁO PHẦN C

- [C.1 — Giới thiệu tổng quan & Chuẩn bị môi trường](#c1--giới-thiệu-tổng-quan--chuẩn-bị-môi-trường)
  - [C.1.1 — Mục đích Phần C & Tổng quan cho người mới (Đọc 2 phút)](#c11--mục-đích-phần-c--tổng-quan-cho-người-mới-đọc-2-phút)
  - [C.1.2 — Hướng dẫn cài đặt nhanh (Quick Start 6 bước)](#c12--hướng-dẫn-cài-đặt-nhanh-quick-start-6-bước)
  - [C.1.3 — Bảng công cụ, nguồn tải chính thức và lệnh kiểm tra](#c13--bảng-công-cụ-nguồn-tải-chính-thức-và-lệnh-kiểm-tra)
  - [C.1.4 — Cố định phiên bản hệ thống (Pin Version Mealie v3.28.0)](#c14--cố-định-phiên-bản-hệ-thống-pin-version-mealie-v3280)
  - [C.1.5 — Quy hoạch cổng mạng & Danh mục tài khoản kiểm thử](#c15--quy-hoạch-cổng-mạng--danh-mục-tài-khoản-kiểm-thử)
- [C.2 — Hướng dẫn cài đặt chi tiết từng bước (Step-by-step Onboarding)](#c2--hướng-dẫn-cài-đặt-chi-tiết-từng-bước-step-by-step-onboarding)
  - [Trường hợp A — Cài đặt trên máy mới hoàn toàn (11 bước chi tiết kèm ảnh)](#trường-hợp-a--cài-đặt-trên-máy-mới-hoàn-toàn-11-bước-chi-tiết-kèm-ảnh)
  - [Trường hợp B — Mở lại Mealie sau khi tắt máy (Bảo toàn dữ liệu)](#trường-hợp-b--mở-lại-mealie-sau-khi-tắt-máy-bảo-toàn-dữ-liệu)
- [C.3 — Quản trị dịch vụ Docker & Bảo toàn dữ liệu SQLite](#c3--quản-trị-dịch-vụ-docker--bảo-toàn-dữ-liệu-sqlite)
  - [C.3.1 — Bảng lệnh Docker Compose thông dụng trong mealie_docker/](#c31--bảng-lệnh-docker-compose-thông-dụng-trong-mealie_docker)
  - [C.3.2 — Cơ chế Named Volume và Quy tắc bảo vệ cơ sở dữ liệu](#c32--cơ-chế-named-volume-và-quy-tắc-bảo-vệ-cơ-sở-dữ-liệu)
  - [C.3.3 — Cập nhật cấu hình môi trường (.env) an toàn](#c33--cập-nhật-cấu-hình-môi-trường-env-an-toàn)
- [C.4 — Dữ liệu mẫu (Seed Data) & Thực nghiệm Ba Luồng nghiệp vụ cốt lõi](#c4--dữ-liệu-mẫu-seed-data--thực-nghiệm-ba-luồng-nghiệp-vụ-cốt-lõi)
  - [C.4.1 — Danh mục 10 công thức mẫu NAM và Kế hoạch thực đơn 14 bữa](#c41--danh-mục-10-công-thức-mẫu-nam-và-kế-hoạch-thực-đơn-14-bữa)
  - [C.4.2 — Luồng 1: Import công thức tự động từ đường dẫn mạng (URL)](#c42--luồng-1-import-công-thức-tự-động-từ-đường-dẫn-mạng-url)
  - [C.4.3 — Luồng 2: Phân tích cú pháp nguyên liệu bằng NLP (Ingredient Parsing)](#c43--luồng-2-phân-tích-cú-pháp-nguyên-liệu-bằng-nlp-ingredient-parsing)
  - [C.4.4 — Luồng 3: Tự động co giãn tỉ lệ khẩu phần ăn (Servings Scaling)](#c44--luồng-3-tự-động-co-giãn-tỉ-lệ-khẩu-phần-ăn-servings-scaling)
- [C.5 — Sổ tay xử lý sự cố thường gặp (Troubleshooting Guide)](#c5--sổ-tay-xử-lý-sự-cố-thường-gặp-troubleshooting-guide)
- [C.6 — Kết luận trạng thái kiểm thử Phần 1 & Phụ lục minh chứng](#c6--kết-luận-trạng-thái-kiểm-thử-phần-1--phụ-lục-minh-chứng)
  - [C.6.1 — Bảng tổng hợp trạng thái các hạng mục (PASS / BLOCKED)](#c61--bảng-tổng-hợp-trạng-thái-các-hạng-mục-pass--blocked)
  - [C.6.2 — Phân định rõ ràng phạm vi kiểm chứng và kế hoạch bàn giao N3.1.3](#c62--phân-định-rõ-ràng-phạm-vi-kiểm-chứng-và-kế-hoạch-bàn-giao-n313)
  - [C.6.3 — Bảng kê khai minh bạch nguồn gốc và phân loại 16 hình ảnh](#c63--bảng-kê-khai-minh-bạch-nguồn-gốc-và-phân-loại-16-hình-ảnh)

---

## C.1 — Giới thiệu tổng quan & Chuẩn bị môi trường

### C.1.1 — Mục đích Phần C & Tổng quan cho người mới (Đọc 2 phút)

Chào bạn! Nếu bạn là thành viên nhóm hoặc giảng viên lần đầu tiếp cận dự án, phần tóm tắt ngắn gọn này giúp bạn nắm ngay mục đích và cách sử dụng tài liệu:

1. **Phần C này dùng để làm gì?**
   - Hướng dẫn bạn tự cài đặt và vận hành hệ thống **Mealie v3.28.0** trên máy tính cá nhân bằng Docker.
   - Nạp sẵn **10 công thức nấu ăn mẫu** và **lịch thực đơn 14 bữa ăn** để phục vụ việc kiểm thử đồ án môn học mà bạn không cần phải tự tạo dữ liệu bằng tay.

2. **Bạn cần chuẩn bị những phần mềm nào trước?**
   - **Git:** Để tải mã nguồn dự án từ GitHub.
   - **Docker Desktop (kèm WSL 2):** Để chạy Mealie khép kín trong container mà không làm ảnh hưởng phần mềm khác trên máy bạn.
   - **Python 3 (3.10 đến 3.14):** Để chạy kịch bản nạp dữ liệu mẫu tự động.

3. **Sau khi cài đặt thành công, bạn sẽ nhìn thấy gì?**
   - Mở trình duyệt gõ `http://localhost:9925` sẽ thấy giao diện web của Mealie.
   - Đăng nhập vào mục **Recipes** thấy đủ 10 món ăn có tiền tố `NAM-01` đến `NAM-10`.
   - Vào mục **Meal Planner** thấy lịch ăn 14 bữa trải dài trên 2 tuần lịch (tuần 06/10–12/10/2026).

4. **Các bước thực hiện tổng quát:**
   `Tải repo & chọn nhánh Nam` ➔ `Bật Docker Desktop` ➔ `Chạy Docker Compose` ➔ `Tạo tài khoản trên Web` ➔ `Chạy script nạp dữ liệu` ➔ `Kiểm tra kết quả`.

---

### C.1.2 — Hướng dẫn cài đặt nhanh (Quick Start 6 bước)

> [!TIP]
> Dành cho thành viên nhóm hoặc giảng viên đã quen thuộc với PowerShell, Git và Docker Desktop. Bạn chỉ cần thực hiện 6 bước ngắn gọn sau:

#### Bước Q1 — Tải mã nguồn và chuyển nhánh của Nam
Mở PowerShell tại thư mục học tập của bạn:
```powershell
# Clone repository (yêu cầu tài khoản GitHub đã được thêm Collaborator):
git clone https://github.com/2312726-collab/KTPM-nhom6-R02-K01.git
cd KTPM-nhom6-R02-K01

# Chuyển vào đúng nhánh làm việc của Nam:
git checkout 2312695-NguyenPhamPhuNam-Phan1
```

#### Bước Q2 — Khởi động Docker Desktop
Mở ứng dụng **Docker Desktop** trên Windows và chờ biểu tượng góc dưới bên trái chuyển sang màu xanh lá cây (*Engine running*).

#### Bước Q3 — Khởi động Mealie bằng Docker Compose
Chạy đoạn lệnh fail-safe dưới đây (tự động nhận diện thư mục `mealie_docker/`, ngăn chặn việc chạy nhầm compose ở thư mục gốc repo):
```powershell
# 1. Chuyển vào đúng thư mục cấu hình Docker của Nam:
if ((Test-Path "docker-compose.yml") -and (Test-Path ".env.example") -and (Test-Path "seed/seed_data.py")) {
    Write-Host 'Đang ở sẵn trong mealie_docker:' (Get-Location)
} elseif ((Test-Path "mealie_docker/docker-compose.yml") -and (Test-Path "mealie_docker/.env.example")) {
    cd mealie_docker
    Write-Host 'Đã chuyển vào:' (Get-Location)
} else {
    throw "LỖI: Hãy mở PowerShell tại thư mục gốc repository KTPM-nhom6-R02-K01!"
}

# 2. Tạo file cấu hình môi trường .env (nếu chưa có):
if (-not (Test-Path ".env")) { Copy-Item .env.example .env }

# 3. Khởi động Mealie v3.28.0 chạy nền:
docker compose up -d

# 4. Kiểm tra trạng thái container:
docker compose ps
```

#### Bước Q4 — Đăng nhập và tạo tài khoản Quản trị viên
1. Mở trình duyệt web truy cập: **`http://localhost:9925`**.
2. Đăng nhập bằng tài khoản mặc định ban đầu:
   - **Email:** `changeme@example.com` | **Password:** `MyPassword`
3. Vào **Admin Panel** (`/admin/manage/users`) ➔ Chọn **Create User**:
   - **Full Name:** Điền họ tên của bạn (bắt buộc)
   - **Username:** `admin_nhom6` *(Lưu ý: Không đặt là `admin` vì sẽ trùng với user gốc)*
   - **Email:** `admin@nhom6.test` *(hoặc email cá nhân của bạn)*
   - **Password:** `Admin123@` *(hoặc mật khẩu riêng bạn chọn)*
   - Bật cờ quyền **Admin: On**.
4. Đăng xuất tài khoản mặc định và đăng nhập lại bằng tài khoản mới vừa tạo.

#### Bước Q5 — Nạp dữ liệu mẫu (Seed Data)
Mở cửa sổ PowerShell mới tại **thư mục gốc repository**, chọn **1 trong 2 cách** sau:

* **Cách 1 (Khuyến nghị cho tài khoản bạn vừa tạo tại Bước Q4):**
  ```powershell
  $env:MEALIE_BASE_URL = "http://localhost:9925"
  $adminEmail = Read-Host -Prompt "Nhập email quản trị Mealie (ví dụ: admin@nhom6.test)"
  $env:MEALIE_EMAIL = $adminEmail.Trim()
  $securePass = Read-Host -Prompt "Nhập mật khẩu quản trị Mealie" -AsSecureString
  try {
      $env:MEALIE_PASSWORD = [System.Net.NetworkCredential]::new("", $securePass).Password
      python mealie_docker/seed/seed_data.py
  } finally {
      Remove-Item env:MEALIE_PASSWORD -ErrorAction SilentlyContinue
      $securePass = $null
  }
  ```

* **Cách 2 (Dành cho tài khoản demo mặc định `admin@nhom6.test` / `Admin123@`):**
  ```powershell
  python mealie_docker/seed/seed_data.py
  ```

#### Bước Q6 — Xác nhận dữ liệu trên Web
- Vào mục **Recipes**: Thấy đủ 10 món `NAM-01` đến `NAM-10`.
- Vào mục **Meal Planner**: Nhấn nút chuyển tuần (`>`) để xem đủ 14 bữa ăn trong 2 tuần lịch (từ 06/10 đến 12/10/2026).

---

### C.1.3 — Bảng công cụ, nguồn tải chính thức và lệnh kiểm tra

Trước khi tiến hành cài đặt, người thực hiện cần đảm bảo máy trạm đã cài đặt đầy đủ các phần mềm nền tảng từ nguồn chính thức:

| Công cụ | Nguồn tải chính thức | Lệnh PowerShell kiểm tra | Kết quả mong đợi |
|---|---|---|---|
| **Git** | [git-scm.com/download/win](https://git-scm.com/download/win) | `git --version` | `git version 2.x.x` |
| **Docker Desktop** | [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/) | `docker --version` | `Docker version 2x.x.x` |
| **Docker Compose** | Đi kèm bộ cài Docker Desktop | `docker compose version` | `Docker Compose version v2.x.x` trở lên |
| **WSL 2 Backend** | Đi kèm Docker Desktop / Microsoft WSL | `wsl -l -v` | Thấy distro `docker-desktop` chạy phiên bản 2 |
| **Python 3** | [python.org/downloads](https://www.python.org/downloads/) | `python --version` | `Python 3.10.x` đến `3.14.x` |

---

### C.1.4 — Cố định phiên bản hệ thống (Pin Version Mealie v3.28.0)

Nhóm 6 đã thống nhất cố định phiên bản hệ thống Mealie nhằm chống trôi mã nguồn và đảm bảo khả năng tái lập kết quả kiểm thử trên các môi trường tương thích:

- **Tên phần mềm mục tiêu:** Mealie (Recipe Manager and Meal Planner)
- **Kho lưu trữ chính thức:** [https://github.com/mealie-recipes/mealie](https://github.com/mealie-recipes/mealie)
- **Phiên bản cố định (Release Tag):** **`v3.28.0`**
- **Mã định danh commit nguồn (Git SHA):** **`0552eaa4a80031b8572849cca0ed95d07f1be001`**
- **Docker Image chính thức:** `ghcr.io/mealie-recipes/mealie:v3.28.0`
- **Tài liệu chốt phiên bản:** [Documents/mealie_version.md](mealie_version.md)

---

### C.1.5 — Quy hoạch cổng mạng & Danh mục tài khoản kiểm thử

#### Bảng quy hoạch cổng mạng trên máy Host:
| Dịch vụ | Cổng Host | Cổng Container | Giao thức | Mục đích sử dụng |
|---|:---:|:---:|:---:|---|
| **Mealie Web UI & API** | **`9925`** | `9000` | HTTP | Giao diện người dùng Web và REST API chính |
| **Mock Recipe Server** | **`9926`** | `9926` | HTTP | Server giả lập phục vụ kiểm thử Import URL (JSON-LD) |

#### Danh mục tài khoản phục vụ đồ án:
| Vai trò | Địa chỉ Email | Mật khẩu mẫu ban đầu | Quyền hạn | Mục đích sử dụng |
|---|---|---|:---:|---|
| **Default Admin (Gốc Mealie)** | `changeme@example.com` | `MyPassword` | Quản trị tối cao | Tài khoản gốc do Docker Mealie tự sinh khi database rỗng lần đầu |
| **Team Admin (Quản trị nhóm)** | `admin@nhom6.test` | `Admin123@` | Quản trị nhóm | Tài khoản quản trị chính dùng để chạy seed data và kiểm thử |
| **Standard User (Người dùng thường)** | `test@nhom6.test` | `User123@` | Thành viên gia đình | Tài khoản người dùng thường phục vụ kiểm chứng phân quyền RBAC |

> [!WARNING]
> **CẢNH BÁO BẢO MẬT:**
> Tài khoản `changeme@example.com` với mật khẩu `MyPassword` là tài khoản công khai mặc định của Mealie. Sau khi đăng nhập lần đầu, bạn bắt buộc phải tạo tài khoản quản trị mới và đổi mật khẩu hoặc vô hiệu hóa tài khoản mặc định này. Mọi thông tin tài khoản trên đây chỉ phục vụ kiểm thử nội bộ đồ án môn học.

---

## C.2 — Hướng dẫn cài đặt chi tiết từng bước (Step-by-step Onboarding)

### Trường hợp A — Cài đặt trên máy mới hoàn toàn (11 bước chi tiết kèm ảnh)

Dành cho thành viên nhóm hoặc máy chấm thi chưa từng chạy Mealie. Mỗi bước trả lời rõ: *Mở phần mềm nào? Thao tác ở đâu? Nhập lệnh gì? Kết quả mong đợi ra sao? Nếu bị lỗi thì xử lý thế nào?*

---

#### Bước 1 — Kiểm tra các công cụ nền tảng đã sẵn sàng
1. **Mở phần mềm:** Mở cửa sổ **Windows PowerShell** (không cần quyền Administrator).
2. **Thao tác ở đâu:** Tại bất kỳ thư mục nào trên máy tính.
3. **Nhập lệnh:**
   ```powershell
   git --version
   python --version
   docker --version
   docker compose version
   ```
4. **Kết quả đúng:** Tất cả 4 lệnh đều in ra số phiên bản hợp lệ, không có thông báo lỗi `is not recognized as an internal or external command`.
5. **Nếu không đúng:** Nếu thiếu phần mềm nào, hãy tải và cài đặt theo bảng C.1.3 (lưu ý tích chọn *"Add python.exe to PATH"* khi cài Python).

![Hình C.4 - Kiểm tra Docker Engine và Docker Compose](images_huong_dan_C/C04_docker_check.png)
*Hình C.4. [Trích xuất Console thực tế] Kết quả kiểm tra phiên bản Docker Engine và Docker Compose trên máy thật.*

---

#### Bước 2 — Khởi động và kiểm tra Docker Desktop Engine
1. **Mở phần mềm:** Nhấp đúp biểu tượng **Docker Desktop** trên màn hình Desktop hoặc mở từ Start Menu.
2. **Thao tác ở đâu:** Quan sát thanh trạng thái góc dưới bên trái của Docker Desktop chuyển sang màu xanh lá cây (*Engine running*).
3. **Nhập lệnh:** Mở PowerShell và chạy:
   ```powershell
   docker info --format 'ServerVersion: {{.ServerVersion}}'
   ```
4. **Kết quả đúng:** In ra số phiên bản Server (ví dụ: `ServerVersion: 29.7.2`) và không báo lỗi pipe.
5. **Nếu không đúng:** Nếu báo lỗi `cannot connect to pipe`, chờ Docker Desktop khởi động xong hoàn toàn hoặc xem mục C.5 Lỗi 2.

![Hình C.3 - Docker Desktop Engine sẵn sàng](images_huong_dan_C/C03_docker_desktop.png)
*Hình C.3. [Trích xuất Console thực tế] Docker Desktop Engine sẵn sàng hoạt động với WSL 2 backend.*

---

#### Bước 3 — Tải mã nguồn và chuyển đúng nhánh làm việc của Nam
1. **Mở phần mềm:** Mở Windows PowerShell.
2. **Thao tác ở đâu:** Di chuyển đến thư mục học tập của bạn (ví dụ: `C:\Workspace` hoặc `D:\Projects`).
3. **Nhập lệnh:**
   ```powershell
   # Clone repository:
   git clone https://github.com/2312726-collab/KTPM-nhom6-R02-K01.git
   cd KTPM-nhom6-R02-K01

   # Chuyển vào đúng nhánh làm việc của Nam:
   git checkout 2312695-NguyenPhamPhuNam-Phan1

   # Xác nhận nhánh:
   git status
   ```
   > [!IMPORTANT]
   > Kho lưu trữ `KTPM-nhom6-R02-K01` là kho riêng tư (Private). Bạn cần đăng nhập tài khoản GitHub đã được thêm quyền **Collaborator** trước khi clone.
4. **Kết quả đúng:** Thông báo: `On branch 2312695-NguyenPhamPhuNam-Phan1` và `working tree clean`.
5. **Nếu không đúng:** Nếu báo `Repository not found`, liên hệ quản trị nhóm để được thêm quyền truy cập.

![Hình C.1 - GitHub Repository và lựa chọn đúng nhánh](images_huong_dan_C/C01_github_branch.png)
*Hình C.1. [Trích xuất Console thực tế] Kiểm tra nhánh làm việc 2312695-NguyenPhamPhuNam-Phan1 trên GitHub.*

---

#### Bước 4 — Kiểm tra cấu trúc thư mục sau khi clone
1. **Mở phần mềm:** Windows PowerShell tại thư mục gốc repository vừa clone.
2. **Thao tác ở đâu:** Thư mục `KTPM-nhom6-R02-K01`.
3. **Nhập lệnh:**
   ```powershell
   Get-ChildItem -Path mealie_docker
   ```
4. **Kết quả đúng:** Thư mục `mealie_docker/` chứa `docker-compose.yml`, `.env.example` và thư mục con `seed/`.
5. **Nếu không đúng:** Kiểm tra lại xem bạn đã chuyển đúng nhánh `2312695-NguyenPhamPhuNam-Phan1` ở Bước 3 hay chưa.

![Hình C.2 - Cấu trúc thư mục dự án sau khi tải mã nguồn](images_huong_dan_C/C02_folder_structure.png)
*Hình C.2. [Trích xuất Console thực tế] Cấu trúc cây thư mục dự án đầy đủ file cấu hình.*

---

#### Bước 5 — Mở PowerShell đúng thư mục và kiểm tra cổng mạng
1. **Mở phần mềm:** Windows PowerShell.
2. **Thao tác ở đâu:** Chuyển vào thư mục `mealie_docker/` chứa Docker Compose của Nam và dò quét cổng `9925`.
3. **Nhập lệnh:**
   ```powershell
   # 1. Chuyển vào đúng mealie_docker (tự động kiểm tra vị trí):
   if ((Test-Path "docker-compose.yml") -and (Test-Path ".env.example") -and (Test-Path "seed/seed_data.py")) {
       Write-Host 'Đang ở sẵn trong mealie_docker:' (Get-Location)
   } elseif ((Test-Path "mealie_docker/docker-compose.yml") -and (Test-Path "mealie_docker/.env.example")) {
       cd mealie_docker
       Write-Host 'Đã chuyển vào:' (Get-Location)
   } else {
       throw "LỖI: Không tìm thấy mealie_docker! Hãy mở PowerShell tại thư mục gốc repository."
   }

   # 2. Kiểm tra cổng mạng 9925:
   netstat -ano | findstr :9925
   ```
4. **Kết quả đúng:** Lệnh `findstr :9925` không in ra dòng nào (cổng 9925 đang hoàn toàn trống).
5. **Nếu không đúng:** Nếu có dòng kết quả trả về với trạng thái `LISTENING`, cổng đang bị chiếm (xem cách đổi cổng tại C.5 Lỗi 1).

---

#### Bước 6 — Thiết lập file cấu hình môi trường `.env`
1. **Mở phần mềm:** Windows PowerShell trong thư mục `mealie_docker/`.
2. **Thao tác ở đâu:** Sao chép file mẫu `.env.example` thành file `.env`.
3. **Nhập lệnh:**
   ```powershell
   if (-not (Test-Path .env)) {
       Copy-Item .env.example .env
       Write-Host 'Đã tạo file .env thành công.'
   } else {
       Write-Host 'File .env đã sẵn sàng, giữ nguyên cấu hình.'
   }
   ```
4. **Kết quả đúng:** Thông báo đã tạo file `.env`, file chứa cấu hình cổng `9925`, SQLite và whitelist mạng.
5. **Nếu không đúng:** Nếu báo lỗi quyền truy cập file, kiểm tra xem có ứng dụng soạn thảo nào đang khóa file `.env` không.

![Hình C.5 - File .env và các biến cấu hình](images_huong_dan_C/C05_env_config.png)
*Hình C.5. [Trích xuất Console thực tế] Cấu trúc file cấu hình mealie_docker/.env chuẩn hóa.*

---

#### Bước 7 — Khởi động Mealie bằng Docker Compose
1. **Mở phần mềm:** Windows PowerShell trong thư mục `mealie_docker/`.
2. **Thao tác ở đâu:** Chạy container ở chế độ nền (`-d`).
3. **Nhập lệnh:**
   ```powershell
   docker compose up -d
   ```
4. **Kết quả đúng:** Docker tải image `ghcr.io/mealie-recipes/mealie:v3.28.0` và thông báo:
   ```
   [+] Running 2/2
    ✔ Network mealie_docker_default  Created
    ✔ Container mealie               Started
   ```
5. **Nếu không đúng:** Nếu báo lỗi trùng tên container, chạy `docker compose down` rồi thử lại (xem C.5 Lỗi 7).

![Hình C.6 - Lệnh Docker Compose khởi động thành công](images_huong_dan_C/C06_docker_up.png)
*Hình C.6. [Trích xuất Console thực tế] Docker Compose tạo mạng và khởi chạy container mealie thành công.*

---

#### Bước 8 — Kiểm tra trạng thái Container và Log khởi động
1. **Mở phần mềm:** Windows PowerShell trong thư mục `mealie_docker/`.
2. **Thao tác ở đâu:** Kiểm tra danh sách tiến trình container và log FastAPI.
3. **Nhập lệnh:**
   ```powershell
   docker compose ps
   docker compose logs --tail=25 mealie
   ```
4. **Kết quả đúng:** Container có trạng thái `Up (healthy)`, trong log xuất hiện dòng:
   ```
   INFO Application startup complete.
   INFO Uvicorn running on http://0.0.0.0:9000 (Press CTRL+C to quit)
   ```
5. **Nếu không đúng:** Nếu container bị restart liên tục, xem C.5 Lỗi 9.

![Hình C.7 - Container Mealie chạy trong Docker](images_huong_dan_C/C07_docker_running.png)
*Hình C.7. [Trích xuất Console thực tế] Container mealie chạy ổn định trên cổng host 9925.*

![Hình C.16 - Kết quả kiểm tra log container Mealie](images_huong_dan_C/C16_docker_logs.png)
*Hình C.16. [Trích xuất Console thực tế] Log ghi nhận FastAPI khởi động hoàn tất (Application startup complete).*

---

#### Bước 9 — Đăng nhập lần đầu và tạo tài khoản Quản trị viên
1. **Mở phần mềm:** Trình duyệt Web (Chrome, Edge hoặc Firefox).
2. **Thao tác ở đâu:** Truy cập địa chỉ: **`http://localhost:9925`**.
3. **Thao tác đăng nhập & tạo tài khoản:**
   - Nhấn nút **Login** ở góc trên bên phải.
   - Nhập tài khoản mặc định của Mealie: **Email:** `changeme@example.com` | **Password:** `MyPassword`.
   - Sau khi vào trong, bấm mục **Admin Panel** (`/admin/manage/users`) ➔ Chọn **Create User**:
     - **Full Name:** Điền họ tên của bạn (bắt buộc)
     - **Username:** `admin_nhom6` *(Lưu ý: Không nhập `admin` vì Mealie đã dùng tên này cho tài khoản gốc, nhập trùng sẽ báo lỗi HTTP 409 Conflict)*
     - **Email:** `admin@nhom6.test` *(hoặc email cá nhân của bạn)*
     - **Password:** `Admin123@` *(hoặc mật khẩu riêng bạn chọn)*
     - Bật cờ quyền **Admin: On**.
   - Nhấn **Save**. Tiến hành đổi mật khẩu hoặc vô hiệu hóa tài khoản mặc định `changeme@example.com` để bảo mật.
4. **Kết quả đúng:** Tài khoản mới được tạo thành công và xuất hiện trong danh sách người dùng.
5. **Nếu không đúng:** Nếu báo lỗi `Username already exists`, đổi username thành tên khác (ví dụ: `admin_nam`).

![Hình C.8 - Giao diện thiết lập tài khoản và đăng nhập](images_huong_dan_C/C08_mealie_login.png)
*Hình C.8. [Ảnh chụp giao diện Web thực tế] Màn hình đăng nhập Mealie v3.28.0 trên trình duyệt.*

---

#### Bước 10 — Đăng nhập và xác nhận giao diện Dashboard
1. **Mở phần mềm:** Trình duyệt Web tại `http://localhost:9925`.
2. **Thao tác ở đâu:** Đăng xuất khỏi tài khoản mặc định và đăng nhập lại bằng tài khoản Quản trị mới bạn vừa tạo ở Bước 9.
3. **Kết quả đúng:** Giao diện Dashboard hiển thị đầy đủ các mục menu: *Recipes*, *Meal Planner*, *Shopping Lists*, *Admin Panel*.
4. **Nếu không đúng:** Nếu không thấy menu *Admin Panel*, kiểm tra lại xem tài khoản của bạn đã được bật cờ quyền Admin chưa.

![Hình C.9 - Dashboard Mealie sau đăng nhập](images_huong_dan_C/C09_mealie_dashboard.png)
*Hình C.9. [Ảnh chụp giao diện Web thực tế] Dashboard Mealie sau khi đăng nhập thành công bằng tài khoản Admin.*

---

#### Bước 11 — Chạy kịch bản nạp dữ liệu mẫu (Seed Data)
Mục đích: Tự động nạp **10 công thức nấu ăn** (`NAM-01` đến `NAM-10`) và **14 bữa ăn thực đơn 7 ngày** vào Mealie.

> [!IMPORTANT]
> **Quy tắc chọn lệnh:** Bạn **CHỈ CHỌN VÀ CHẠY 1 TRONG 2 CÁCH DƯỚI ĐÂY** tại **thư mục gốc repository**:

##### CÁCH 1 (Khuyến nghị) — Cho tài khoản Quản trị bạn đã tạo tại Bước 9
Lệnh này yêu cầu bạn nhập email và mật khẩu thực tế (mật khẩu được ẩn an toàn khi gõ):
```powershell
# 1. Đảm bảo đứng ở thư mục gốc repository:
if (Test-Path "mealie_docker/seed/seed_data.py") {
    Write-Host 'Đang ở thư mục gốc repo:' (Get-Location)
} elseif ((Test-Path "seed/seed_data.py") -and (Test-Path "docker-compose.yml")) {
    cd ..
    Write-Host 'Đã lùi về thư mục gốc:' (Get-Location)
} else {
    throw "LỖI: Hãy mở PowerShell tại thư mục gốc repository!"
}

# 2. Thiết lập cấu hình và nhập thông tin an toàn:
$env:MEALIE_BASE_URL = "http://localhost:9925"
$adminEmail = Read-Host -Prompt "Nhập email quản trị Mealie (ví dụ: admin@nhom6.test)"
$env:MEALIE_EMAIL = $adminEmail.Trim()
$securePass = Read-Host -Prompt "Nhập mật khẩu quản trị Mealie" -AsSecureString

try {
    $env:MEALIE_PASSWORD = [System.Net.NetworkCredential]::new("", $securePass).Password
    python mealie_docker/seed/seed_data.py
} finally {
    Remove-Item env:MEALIE_PASSWORD -ErrorAction SilentlyContinue
    $securePass = $null
    Write-Host 'Đã hoàn thành và dọn sạch biến mật khẩu.'
}
```

##### CÁCH 2 — Dành riêng cho tài khoản demo mặc định (`admin@nhom6.test` / `Admin123@`)
Nếu tại Bước 9 bạn đặt đúng email `admin@nhom6.test` và mật khẩu `Admin123@`:
```powershell
python mealie_docker/seed/seed_data.py
```

*Kết quả mong đợi trong terminal:*
```
Logging in to http://localhost:9925 as admin@nhom6.test...
Processing recipe: NAM-01 Trứng Luộc Lòng Đào...
...
Setting up 7-day Meal Plan (06/10/2026 - 12/10/2026)...
Seed data completed successfully!
```

![Hình C.10 - Danh sách 10 công thức NAM sau khi nạp](images_huong_dan_C/C10_recipes_nam.png)
*Hình C.10. [Trích xuất Console thực tế] Danh sách 10 công thức NAM-01 đến NAM-10 được nạp thành công.*

![Hình C.11 - Meal Planner của tuần có dữ liệu thực đơn](images_huong_dan_C/C11_meal_planner.png)
*Hình C.11. [Ảnh chụp giao diện Web thực tế] Giao diện Meal Planner hiển thị lịch thực đơn 14 bữa ăn.*

> [!NOTE]
> **Mẹo xem đủ 14 bữa ăn trên Meal Planner:**
> Dữ liệu thực đơn mẫu chạy từ **Thứ Ba 06/10/2026 đến Thứ Hai 12/10/2026**. Vì giao diện Mealie hiển thị lịch từ Thứ Hai đến Chủ Nhật, nên:
> - **Tuần 1 (05/10 – 11/10):** Chứa 12 bữa ăn (Thứ Ba 06/10 đến Chủ Nhật 11/10).
> - **Tuần 2 (12/10 – 18/10):** Chứa 2 bữa còn lại (Thứ Hai 12/10: Sáng NAM-02, Tối NAM-03).
> 👉 Bạn chỉ cần bấm nút mũi tên chuyển tuần (`>`) trên web để xem trọn vẹn 14 bữa ăn.

---

### Trường hợp B — Mở lại Mealie sau khi tắt máy (Bảo toàn dữ liệu)

Dành cho những ngày làm việc tiếp theo khi bạn mở lại máy tính sau khi tắt nguồn.

> [!TIP]
> **Tuyệt đối KHÔNG chạy lại cài đặt hay seed data.** Cơ sở dữ liệu SQLite đã được lưu an toàn trong Docker Named Volume. Bạn chỉ cần 3 bước mở lại:

1. **Mở Docker Desktop:** Bật ứng dụng và chờ Docker Engine running xanh ổn định.
2. **Khởi động container (nếu chưa tự chạy):**
   Mở PowerShell và chạy lệnh:
   ```powershell
   if (Test-Path "mealie_docker/docker-compose.yml") { cd mealie_docker }
   docker compose up -d
   docker compose ps
   ```
3. **Mở trình duyệt truy cập:**
   Vào `http://localhost:9925` và đăng nhập bằng tài khoản Quản trị bạn đã tạo. Toàn bộ 10 công thức và thực đơn vẫn nguyên vẹn 100%.

---

## C.3 — Quản trị dịch vụ Docker & Bảo toàn dữ liệu SQLite

### C.3.1 — Bảng lệnh Docker Compose thông dụng trong mealie_docker/

| Lệnh PowerShell | Tác động lên Container | Tác động lên Dữ liệu SQLite | Khi nào nên dùng? |
|---|---|---|---|
| `docker compose up -d` | Khởi động container nền | **Giữ nguyên 100%** | Bắt đầu làm việc hoặc sau khi sửa `.env` |
| `docker compose ps` | Xem trạng thái | Không tác động | Kiểm tra container có đang chạy không |
| `docker compose logs -f mealie` | Xem log trực tiếp | Không tác động | Khi cần gỡ lỗi hoặc theo dõi hoạt động (`Ctrl+C` để thoát) |
| `docker compose stop` | Tạm dừng container | **Giữ nguyên 100%** | Khi muốn giải phóng RAM máy tính |
| `docker compose down` | Dừng và hủy container | **Giữ nguyên 100%** | Kết thúc phiên làm việc an toàn |
| ❌ `docker compose down -v` | Hủy container + **XÓA VOLUME** | ⚠️ **MẤT SẠCH DATABASE** | **CẤM DÙNG** (trừ khi cố tình muốn xóa sạch để test lại từ đầu) |

---

### C.3.2 — Cơ chế Named Volume và Quy tắc bảo vệ cơ sở dữ liệu

- Trong file `mealie_docker/docker-compose.yml`, thư mục dữ liệu `/app/data/` (chứa database SQLite `mealie.db` và ảnh món ăn) được gắn kết với **Named Volume** tên là **`mealie_docker_mealie-data`**.
- Vòng đời của Named Volume hoàn toàn độc lập với container. Do đó, dù bạn tắt máy hoặc chạy lệnh `docker compose down`, dữ liệu vẫn an toàn trên ổ đĩa.
- **Cảnh báo an toàn:** Tuyệt đối không chạy lệnh `docker system prune -a --volumes` hoặc `docker volume prune` vì sẽ xóa mất database của Mealie và các dự án khác trên máy bạn.

---

### C.3.3 — Cập nhật cấu hình môi trường (.env) an toàn

> [!WARNING]
> Không dùng `docker compose restart mealie` sau khi chỉnh sửa `.env` vì lệnh restart không nạp biến môi trường mới!
> Hãy chạy:
> ```powershell
> docker compose up -d
> ```
> Docker Compose sẽ tự động nhận diện thay đổi trong `.env` và tái tạo (recreate) container mới với biến môi trường mới, đồng thời tự gắn lại volume cũ nên dữ liệu không bao giờ bị mất.

---

## C.4 — Dữ liệu mẫu (Seed Data) & Thực nghiệm Ba Luồng nghiệp vụ cốt lõi

### C.4.1 — Danh mục 10 công thức mẫu NAM và Kế hoạch thực đơn 14 bữa

Tập dữ liệu mẫu trong `mealie_docker/seed/recipes_nam.json` được thiết kế có chủ đích cho các trường hợp kiểm thử định lượng:
- **NAM-01 (Trứng Luộc Lòng Đào):** Số nguyên đơn giản (`2 eggs`, `1 cup water`).
- **NAM-02 (Sữa Tươi Yến Mạch):** Số thập phân (`1.5 cups`, `2.25 tbsp`).
- **NAM-03 (Bánh Bông Lan Đường Mía):** Phân số ASCII (`1/2 cup`, `3/4 cup`).
- **NAM-04 (Sữa Nóng Mật Ong):** Phân số Unicode (`½ cup`).
- **NAM-05 (Canh Rong Biển):** Phân số Unicode phối hợp (`¾ tsp salt`, `½ tbsp oil`).
- **NAM-06 (Bánh Mì Bột Mì):** Hỗn số có dấu cách (`2 1/2 cups flour`).
- **NAM-07 (Trà Thảo Mộc):** Hỗn số Unicode dính liền (`2½ cups water`).
- **NAM-08 (Súp Hành Tây Pháp):** Bóc tách ghi chú trong ngoặc đơn (`1 onion (finely chopped)`).
- **NAM-09 (Salad Thập Cẩm):** Phối hợp đa định dạng nguyên liệu.
- **NAM-10 (Bò Sốt Tiêu Chuẩn):** Thử nghiệm nhân đôi khẩu phần Servings Scaling (từ 4 lên 8).

*Kế hoạch 14 bữa ăn tuần 06/10–12/10/2026:*
- Thứ Ba 06/10: Sáng NAM-01, Tối NAM-02
- Thứ Tư 07/10: Sáng NAM-03, Tối NAM-08
- Thứ Năm 08/10: Sáng NAM-04, Tối NAM-05
- Thứ Sáu 09/10: Sáng NAM-06, Tối NAM-10
- Thứ Bảy 10/10: Sáng NAM-07, Tối NAM-09
- Chủ Nhật 11/10: Sáng NAM-01, Tối NAM-10
- Thứ Hai 12/10: Sáng NAM-02, Tối NAM-03 *(thuộc tuần lịch kế tiếp trên web Mealie)*.

---

### C.4.2 — Luồng 1: Import công thức tự động từ đường dẫn mạng (URL)
- **Mục đích:** Kiểm tra tính năng tự động cào và bóc tách công thức nấu ăn từ website theo chuẩn dữ liệu Schema.org Recipe.
- **Cách thực hiện:**
  1. Mở một terminal riêng tại thư mục gốc repository để chạy Mock Server giả lập:
     ```powershell
     python mealie_docker/seed/mock_recipe_server.py
     ```
     *(Giữ nguyên cửa sổ terminal này, server sẽ lắng nghe tại cổng 9926).*
  2. Mở Mealie trên trình duyệt: `http://localhost:9925` ➔ Chọn mục **Recipes** ➔ Bấm nút **Create** (`+`) ➔ Chọn **Import from URL**.
  3. Dán đường dẫn nội bộ:
     ```
     http://host.docker.internal:9926/recipe/pho-bo
     ```
  4. Nhấn nút **Create** / **Import** và chờ vài giây.
- **Kết quả:** Mealie tự động bóc tách thành công món **Phở Bò Hà Nội** với đủ 5 nguyên liệu và 3 bước chế biến.

![Hình C.12 - Mock Recipe Server đang hoạt động](images_huong_dan_C/C12_mock_server.png)
*Hình C.12. [Trích xuất Console thực tế] Mock Recipe Server chạy tại cổng 9926 phục vụ dữ liệu cho Mealie.*

![Hình C.13 - Import công thức từ URL thành công](images_huong_dan_C/C13_recipe_import.png)
*Hình C.13. [Ảnh chụp giao diện Web thực tế] Giao diện Mealie sau khi import thành công công thức Phở Bò Hà Nội.*

---

### C.4.3 — Luồng 2: Phân tích cú pháp nguyên liệu bằng NLP (Ingredient Parsing)
- **Mục đích:** Kiểm tra khả năng tự động hiểu câu nguyên liệu tự nhiên thành các thành phần: Số lượng, Đơn vị, Tên nguyên liệu, Ghi chú.
- **Cách thực hiện:**
  1. Vào mục **Recipes** ➔ Mở công thức **NAM-08 Súp Hành Tây Pháp** ➔ Nhấn **Edit** ➔ Chọn tab **Ingredients**.
  2. Tìm dòng nguyên liệu `1 onion (finely chopped)` ➔ Bấm nút **Parse** (biểu tượng cây đũa thần).
- **Kết quả:** Mealie nhận diện chính xác:
  - **Số lượng (Quantity):** `1`
  - **Đơn vị (Unit):** *(trống)*
  - **Nguyên liệu (Food):** `onion`
  - **Ghi chú (Note):** `finely chopped` (đã tự bỏ ngoặc đơn)
  - Độ tin cậy trích xuất số lượng đạt 100%, độ tin cậy trung bình mô hình đạt 99.66%.

![Hình C.14 - Kết quả phân tích nguyên liệu bằng NLP](images_huong_dan_C/C14_ingredient_parse.png)
*Hình C.14. [Ảnh chụp giao diện Web thực tế] Modal phân tích nguyên liệu bóc tách chuỗi '1 onion (finely chopped)'.*

---

### C.4.4 — Luồng 3: Tự động co giãn tỉ lệ khẩu phần ăn (Servings Scaling)
- **Mục đích:** Kiểm tra tính năng tự động tính toán lại định lượng các nguyên liệu khi thay đổi số người ăn.
- **Cách thực hiện:**
  1. Vào mục **Recipes** ➔ Mở công thức **NAM-10 Bò Sốt Tiêu Khẩu Phần Chuẩn**.
  2. Tại ô **Servings** (khẩu phần gốc là `4`), đổi thành **`8`** (nhân đôi số người ăn).
- **Kết quả:** Toàn bộ nguyên liệu tự động nhân đôi chính xác ngay trên màn hình:
  - Thịt bò: `400 grams` ➔ **`800 grams`**
  - Tiêu đen: `2 tablespoons` ➔ **`4 tablespoons`**
  - Nước dùng bò: `1/2 cup` ➔ **`1 cup`**
  - Tỏi băm: `4 cloves` ➔ **`8 cloves`**

![Hình C.15 - Kết quả nhân tỉ lệ khẩu phần ăn](images_huong_dan_C/C15_servings_scale.png)
*Hình C.15. [Ảnh chụp giao diện Web thực tế] Định lượng nguyên liệu tự động nhân đôi khi tăng khẩu phần từ 4 lên 8.*

---

## C.5 — Sổ tay xử lý sự cố thường gặp (Troubleshooting Guide)

Nếu bạn gặp khó khăn trong quá trình thao tác, hãy tra cứu nhanh bảng dưới đây:

| Hiện tượng lỗi | Nguyên nhân phổ biến | Cách xử lý nhanh |
|---|---|---|
| **Trùng cổng 9925** (`address already in use`) | Có ứng dụng khác đang dùng cổng 9925. | Mở file `mealie_docker/.env`, sửa thành `MEALIE_PORT=9930` và `BASE_URL=http://localhost:9930`, rồi chạy lại `docker compose up -d`. |
| **Lỗi Docker daemon** (`cannot connect to pipe`) | Docker Desktop chưa được mở hoặc đang khởi động. | Mở Docker Desktop từ Start Menu, đợi icon chuyển sang màu xanh lá cây rồi chạy lại lệnh. |
| **Lỗi GitHub** (`Repository not found`) | Tài khoản GitHub chưa được cấp quyền vào repo riêng tư. | Báo quản trị nhóm thêm tài khoản của bạn làm Collaborator vào repo `2312726-collab/KTPM-nhom6-R02-K01`. |
| **Lỗi chạy sai thư mục** (`no configuration file provided`) | Bạn đang gõ lệnh Docker ở thư mục gốc repo thay vì vào `mealie_docker/`. | Gõ `cd mealie_docker` trước khi chạy lệnh docker compose; hoặc dùng các script tự chuyển thư mục đã cung cấp ở trên. |
| **Không vào được web** (`localhost:9925`) | Container Mealie chưa khởi động xong hoặc bị lỗi. | Chạy `docker compose ps` xem có trạng thái running không. Nếu đang restarting, chạy `docker compose logs --tail=30 mealie` để đọc lỗi. |
| **Lỗi tạo User** (`409 Conflict`) | Bạn đặt Username là `admin`. | Đổi Username thành tên khác (ví dụ: `admin_nhom6`) và nhớ điền trường `Full Name`. |
| **Seed báo lỗi 401 Unauthorized** | Sai email hoặc mật khẩu quản trị khi chạy script. | Nhập đúng email và mật khẩu tài khoản bạn đã tạo ở Bước 9 theo hướng dẫn Cách 1. |
| **Chỉ thấy 12 bữa ăn trên Meal Planner** | Bữa ăn Thứ Hai thuộc tuần kế tiếp. | Bấm nút mũi tên chuyển tuần (`>`) trên giao diện Mealie để xem 2 bữa còn lại của ngày 12/10. |
| **Import URL bị báo lỗi** | Container không kết nối được máy host. | Đảm bảo Mock Server đang chạy cổng 9926 và đường dẫn import dùng đúng bí danh: `http://host.docker.internal:9926/recipe/pho-bo`. |

---

## C.6 — Kết luận trạng thái kiểm thử Phần 1 & Phụ lục minh chứng

### C.6.1 — Bảng tổng hợp trạng thái các hạng mục (PASS / BLOCKED)

| STT | Hạng mục kiểm tra kỹ thuật | Phạm vi | Trạng thái | Nguồn bằng chứng đối chứng |
|:---:|---|---|:---:|---|
| 1 | Đóng gói Docker Compose Mealie v3.28.0 SQLite | N1 | **PASS** | Container `mealie` running cổng 9925 (*Hình C.6, C.7*) |
| 2 | Bảo toàn dữ liệu qua Named Volume `mealie_docker_mealie-data` | N1 | **PASS** | Tắt bật container dữ liệu SQLite không bị mất |
| 3 | Cấu hình an toàn biến môi trường `.env` | N1 | **PASS** | File `.env` hoạt động chuẩn, bảo vệ bởi `.gitignore` (*Hình C.5*) |
| 4 | Kịch bản nạp dữ liệu mẫu tự động `seed_data.py` | N2 | **PASS** | Nạp đủ 10 công thức NAM và 14 bữa meal plan (*Hình C.10, C.11*) |
| 5 | Tính Lũy đẳng của kịch bản Seed Data | N2 | **PASS** | Chạy lại lần 2 không sinh trùng lặp bản ghi (+0) |
| 6 | Phân quyền Quản trị vs Người dùng thường (RBAC) | N2 | **PASS** | Admin truy cập HTTP 200, User thường bị chặn HTTP 403 Forbidden |
| 7 | Nghiệp vụ 1: Import công thức qua Mock URL | N2 | **PASS** | Bóc tách thành công Phở Bò Hà Nội (*Hình C.12, C.13*) |
| 8 | Nghiệp vụ 2: NLP Ingredient Parsing | N2 | **PASS** | Bóc tách đúng `1 onion (finely chopped)`, độ tin cậy TB 99.66% (*Hình C.14*) |
| 9 | Nghiệp vụ 3: Servings Scaling (4 lên 8) | N2 | **PASS** | Định lượng nguyên liệu tự động nhân đôi chính xác (*Hình C.15*) |
| 10 | Bộ 16 hình ảnh hướng dẫn thực tế | N3 | **PASS** | Nhúng markdown hiển thị trực tiếp trên GitHub |
| 11 | **Thẩm định chéo độc lập trên máy sạch (N3.1.3)** | N3 | **BLOCKED** | **Chưa hoàn thành** (Đang chờ bạn Bùi Trung Hiếu thẩm định độc lập) |

---

### C.6.2 — Phân định rõ ràng phạm vi kiểm chứng và kế hoạch bàn giao N3.1.3

1. **Phạm vi kiểm chứng thực tế:**
   - **Docker & CLI Runtime:** Kiểm chứng thực tế qua Docker Compose, container running healthy, volume SQLite nguyên vẹn, script seed nạp thành công 10 công thức và 14 bữa ăn.
   - **API Backend & Data Model:** Kiểm chứng API OpenAPI chuẩn v3.28.0 (`POST /api/parser/ingredient`, `POST /api/recipes/create/url`), xác nhận các trường dữ liệu và độ tin cậy trung bình đạt 99.66%.
   - **Web UI:** Giao diện đăng nhập, Dashboard, Meal Planner, NLP Parser modal, Servings scaling tự động được ghi nhận bằng ảnh chụp trực tiếp từ trình duyệt ngày 07/10/2026.
2. **Kế hoạch bàn giao và nghiệm thu:**
   - Hạng mục **N3.1.3** tiếp tục được giữ nguyên trạng thái chưa hoàn thành `[ ]` để chờ bạn **Bùi Trung Hiếu** thực hiện cài đặt độc lập trên máy tính của Hiếu và gửi biên bản phản hồi/góp ý thực tế trước khi nghiệm thu chéo chính thức.

---

### C.6.3 — Bảng kê khai minh bạch nguồn gốc và phân loại 16 hình ảnh

Toàn bộ 16 ảnh trong thư mục `Documents/images_huong_dan_C/` được công khai xuất xứ rõ ràng:
- **Screenshot Web UI thật (6 ảnh):** Chụp trực tiếp từ giao diện trình duyệt thật ngày 07/10/2026 (`C08`, `C09`, `C11`, `C13`, `C14`, `C15`).
- **Trích xuất Console thực tế (10 ảnh):** Kết xuất đồ họa từ dữ liệu đầu ra thật của PowerShell và Docker CLI trên máy thật của Nam (`C01`, `C02`, `C03`, `C04`, `C05`, `C06`, `C07`, `C10`, `C12`, `C16`).

| Mã | Tên file ảnh | Phân loại | Nội dung ghi nhận |
|:---:|---|:---:|---|
| **C.1** | `C01_github_branch.png` | Console trích xuất | Kiểm tra nhánh làm việc `2312695-NguyenPhamPhuNam-Phan1` |
| **C.2** | `C02_folder_structure.png` | Console trích xuất | Cấu trúc cây thư mục repo và thư mục `mealie_docker/` |
| **C.3** | `C03_docker_desktop.png` | Console trích xuất | Docker Desktop Engine và context `desktop-linux` hoạt động |
| **C.4** | `C04_docker_check.png` | Console trích xuất | Kiểm tra phiên bản Docker Engine 29.7.2 và Compose v5.5.1 |
| **C.5** | `C05_env_config.png` | Console trích xuất | Cấu trúc file cấu hình môi trường `.env` an toàn |
| **C.6** | `C06_docker_up.png` | Console trích xuất | Docker Compose tạo network và khởi động container `mealie` |
| **C.7** | `C07_docker_running.png` | Console trích xuất | Trạng thái container running lành mạnh trên cổng host 9925 |
| **C.8** | `C08_mealie_login.png` | Screenshot Web thật | Giao diện đăng nhập Sign In Mealie v3.28.0 |
| **C.9** | `C09_mealie_dashboard.png` | Screenshot Web thật | Giao diện Dashboard sau khi đăng nhập tài khoản Quản trị |
| **C.10** | `C10_recipes_nam.png` | Console trích xuất | Danh sách 10 công thức nấu ăn NAM được nạp vào hệ thống |
| **C.11** | `C11_meal_planner.png` | Screenshot Web thật | Giao diện Meal Planner hiển thị lịch thực đơn 14 bữa ăn |
| **C.12** | `C12_mock_server.png` | Console trích xuất | Mock Recipe Server chạy tại cổng 9926 phục vụ JSON-LD |
| **C.13** | `C13_recipe_import.png` | Screenshot Web thật | Import thành công công thức Phở Bò từ Mock URL |
| **C.14** | `C14_ingredient_parse.png` | Screenshot Web thật | Modal NLP bóc tách chuỗi `1 onion (finely chopped)` |
| **C.15** | `C15_servings_scale.png` | Screenshot Web thật | Co giãn định lượng nguyên liệu khi tăng Servings từ 4 lên 8 |
| **C.16** | `C16_docker_logs.png` | Console trích xuất | Log container xác nhận `Application startup complete` |

---
*Tài liệu hướng dẫn do Nguyễn Phạm Phú Nam biên soạn và hoàn thiện — Đồ án Kiểm thử Phần mềm Nhóm 6.*
*Cập nhật lần cuối: 18/10/2026 — Kiểm chứng trực tiếp trên Mealie v3.28.0.*
