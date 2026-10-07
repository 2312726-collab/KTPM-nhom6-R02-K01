# BẢNG THEO DÕI TIẾN ĐỘ CÔNG VIỆC — NGUYỄN PHẠM PHÚ NAM
## ĐỒ ÁN KIỂM THỬ PHẦN MỀM (NHÓM 6 — R02 + K01)
### PHẠM VI: PHẦN 1 — PHỤC VỤ ĐÁNH GIÁ GIỮA KỲ (MỐC 20/10)

> **Thành viên:** Nguyễn Phạm Phú Nam — MSSV: 2312695
> **Vai trò:** DevOps & Automation QA
> **Nhánh làm việc chính thức:** `2312695-NguyenPhamPhuNam-Phan1` (tách riêng cho Phần 1, xây dựng trên nền `origin/develop`)
> **Nguyên tắc quản lý:** Tiến độ được theo dõi trong file riêng này; không tự ý chỉnh sửa bảng phân công chung của nhóm để đưa dấu tích lên `main`.

---

## 📊 TỔNG HỢP TIẾN ĐỘ PHẦN 1 (GIỮA KỲ 20/10)

| Nhóm việc | Nội dung chính | Tổng số mục | Đã hoàn thành | Chờ thẩm định | Trạng thái |
|---|---|:---:|:---:|:---:|:---:|
| **N1** | Thiết lập môi trường Docker Mealie SQLite v3.28.0 | 8 | 8 | 0 | **Đạt 100%** |
| **N2** | Nạp dữ liệu mẫu (Seed Data) & Minh chứng 3 luồng | 7 | 7 | 0 | **Đạt 100%** |
| **N3** | Soạn thảo Báo cáo On-boarding Phần C | 4 | 3 | 1 | **Chờ Hiếu thẩm định** |
| **Tổng cộng** | **Phần 1 phục vụ Giữa kỳ 20/10** | **19** | **18** | **1** | **Sẵn sàng nghiệm thu Giữa kỳ** |

---

## 1. NHÓM VIỆC N1: THIẾT LẬP MÔI TRƯỜNG DOCKER MEALIE
**Mục tiêu:** Dựng thành công Mealie v3.28.0 SQLite trên cổng 9925 bằng Docker Compose, thiết lập quyền Admin và ghi nhận minh chứng.

- [x] **N1.1.1** — Tạo thư mục `mealie_docker/` trong repo.
  - *Bằng chứng / File:* Thư mục [`mealie_docker/`](mealie_docker/).
  - *Kết quả kiểm tra:* Thư mục tồn tại, độc lập với thư mục gốc, cấu trúc sạch sẽ.
  - *Việc còn thiếu:* Không.

- [x] **N1.1.2** — Tạo file `mealie_docker/docker-compose.yml` (SQLite) và `mealie_docker/.env.example` mở cổng `9925`.
  - *Bằng chứng / File:* [`mealie_docker/docker-compose.yml`](mealie_docker/docker-compose.yml), [`mealie_docker/.env.example`](mealie_docker/.env.example).
  - *Kết quả kiểm tra:* Image `ghcr.io/mealie-recipes/mealie:v3.28.0`, port host 9925 -> container 9000, biến môi trường mẫu đầy đủ.
  - *Việc còn thiếu:* Không.

- [x] **N1.1.3** — Chạy container: `docker compose up -d`.
  - *Bằng chứng / File:* Container `mealie` chạy ở chế độ nền trên Docker Engine 29.7.2.
  - *Kết quả kiểm tra:* Trạng thái container `Up (healthy)`.
  - *Việc còn thiếu:* Không.

- [x] **N1.1.4** — Kiểm tra log: `docker compose logs -f mealie` xác nhận FastAPI khởi động mượt mà.
  - *Bằng chứng / File:* Log Docker ghi nhận `Application startup complete` và `Uvicorn running on http://0.0.0.0:9000`.
  - *Kết quả kiểm tra:* Khởi động thành công, không phát sinh ngoại lệ runtime.
  - *Việc còn thiếu:* Không.

- [x] **N1.1.5** — Truy cập `http://localhost:9925`, chụp ảnh Landing Page.
  - *Bằng chứng / File:* [`Documents/assets/01_mealie_landing.png`](Documents/assets/01_mealie_landing.png).
  - *Kết quả kiểm tra:* Ảnh chụp giao diện Landing page thật, kích thước 26.5 KB.
  - *Việc còn thiếu:* Không.

- [x] **N1.2.1** — Cấu hình tài khoản Admin (`admin@nhom6.test` / `Admin123@`).
  - *Bằng chứng / File:* Tài khoản quản trị khởi tạo từ giao diện Admin Panel sau khi đăng nhập ban đầu bằng `changeme@example.com` / `MyPassword`.
  - *Kết quả kiểm tra:* Đăng nhập thành công, có quyền quản trị tối cao (Admin).
  - *Việc còn thiếu:* Không.

- [x] **N1.2.2** — Đăng nhập Dashboard thành công, chụp ảnh Dashboard.
  - *Bằng chứng / File:* [`Documents/assets/02_mealie_dashboard.png`](Documents/assets/02_mealie_dashboard.png).
  - *Kết quả kiểm tra:* Ảnh chụp Dashboard thật, kích thước 38.3 KB.
  - *Việc còn thiếu:* Không.

- [x] **N1.2.3** — Commit cấu hình Docker Compose và credentials.
  - *Bằng chứng / File:* Commit `f66d491` trên nhánh `2312695-NguyenPhamPhuNam-Phan1`.
  - *Kết quả kiểm tra:* Đã push thành công lên `origin`.
  - *Việc còn thiếu:* Không.

---

## 2. NHÓM VIỆC N2: NẠP DỮ LIỆU MẪU & MINH CHỨNG 3 LUỒNG NGHIỆP VỤ
**Mục tiêu:** Tạo tài khoản kiểm thử, nạp 10 công thức mẫu đa dạng, thực đơn 7 ngày và thu thập bằng chứng 3 luồng cốt lõi.

- [x] **N2.1.1** — Tạo tài khoản kiểm thử thường (`test@nhom6.test` / `User123@`).
  - *Bằng chứng / File:* Tài khoản thường tạo qua API/Register, quyền hạn người dùng thông thường.
  - *Kết quả kiểm tra:* Xác nhận phân quyền đúng, không có quyền truy cập Admin Panel.
  - *Việc còn thiếu:* Không.

- [x] **N2.1.2** — Tạo 10 công thức mẫu đa dạng (nguyên liệu đơn giản, phân số thường, phân số unicode `½`, chú thích, nhiều bước).
  - *Bằng chứng / File:* [`mealie_docker/seed/recipes_nam.json`](mealie_docker/seed/recipes_nam.json), script [`mealie_docker/seed/seed_data.py`](mealie_docker/seed/seed_data.py).
  - *Kết quả kiểm tra:* Script idempotent, tự kiểm tra trùng lặp slug trước khi tạo/cập nhật; 10 công thức mẫu `NAM-01` đến `NAM-10` đã có trong CSDL.
  - *Việc còn thiếu:* Không.

- [x] **N2.1.3** — Tạo kế hoạch thực đơn (Meal Plan) 7 ngày tuần 06/10–12/10, chụp ảnh.
  - *Bằng chứng / File:* [`Documents/assets/03_meal_plan.png`](Documents/assets/03_meal_plan.png).
  - *Kết quả kiểm tra:* Ảnh hiển thị thực đơn bữa sáng và bữa tối đầy đủ 7 ngày liên tục, kích thước 95.6 KB.
  - *Việc còn thiếu:* Không.

- [x] **N2.2.1** — Luồng 1: Import công thức từ URL (nguồn mock server cục bộ).
  - *Bằng chứng / File:* Script mock server [`mealie_docker/seed/mock_recipe_server.py`](mealie_docker/seed/mock_recipe_server.py) và ảnh [`Documents/assets/04_recipe_import.png`](Documents/assets/04_recipe_import.png).
  - *Kết quả kiểm tra:* Import thành công công thức Phở Bò qua URL Schema.org JSON-LD cục bộ mà không phụ thuộc internet bên ngoài.
  - *Việc còn thiếu:* Không.

- [x] **N2.2.2** — Luồng 2: Phân tích nguyên liệu (Ingredient Parsing).
  - *Bằng chứng / File:* [`Documents/assets/05_ingredient_parse.png`](Documents/assets/05_ingredient_parse.png).
  - *Kết quả kiểm tra:* Đối chiếu trực tiếp với ảnh thật: Modal bóc tách chuỗi `1 onion (finely chopped)` trong công thức `NAM-08 Súp Hành Tây Pháp`, trích xuất chính xác `Quantity=1`, `Unit=None`, `Food=onion` (gợi ý Create missing food: onion), `Note=finely chopped` với `Confidence Score=100.00%`.
  - *Việc còn thiếu:* Không.

- [x] **N2.2.3** — Luồng 3: Nhân tỉ lệ khẩu phần ăn (Servings Scaling từ 4 lên 8).
  - *Bằng chứng / File:* [`Documents/assets/06_servings_scale.png`](Documents/assets/06_servings_scale.png).
  - *Kết quả kiểm tra:* Đối chiếu trực tiếp với ảnh thật: Công thức `NAM-10 Bò Sốt Tiêu Khẩu Phần Chuẩn` (gốc 4 servings: 400g beef, 2 tbsp black pepper, 0.5 cup beef broth, 4 cloves garlic), khi đổi sang 8 servings (hệ số 2.0x) giao diện hiển thị chính xác gấp đôi: 800g beef, 4 tbsp black pepper, 1 cup beef broth, 8 cloves garlic.
  - *Việc còn thiếu:* Không.

- [x] **N2.2.4** — Commit dữ liệu mẫu và minh chứng 3 luồng.
  - *Bằng chứng / File:* Commit `12681a3` trên nhánh `2312695-NguyenPhamPhuNam-Phan1`.
  - *Kết quả kiểm tra:* Đã push thành công lên `origin`.
  - *Việc còn thiếu:* Không.

---

## 3. NHÓM VIỆC N3: TÀI LIỆU ON-BOARDING PHẦN C
**Mục tiêu:** Soạn thảo hoàn chỉnh tài liệu hướng dẫn cài đặt và vận hành môi trường kiểm thử `Documents/bao_cao_phan_C.md`.

- [x] **N3.1.1** — Soạn thảo đầy đủ 5 mục chuẩn (C.1 Yêu cầu môi trường, C.2 Cài đặt chi tiết, C.3 Quản lý dịch vụ Docker, C.4 Nạp Seed Data, C.5 Xử lý sự cố).
  - *Bằng chứng / File:* [`Documents/bao_cao_phan_C.md`](Documents/bao_cao_phan_C.md).
  - *Kết quả kiểm tra:* Đủ 5 phần nội dung kỹ thuật, chính xác phiên bản máy thật, biến môi trường, đường dẫn và lệnh chạy.
  - *Việc còn thiếu:* Không.

- [x] **N3.1.2** — Nhúng toàn bộ 6 ảnh minh chứng vào đúng vị trí trong báo cáo.
  - *Bằng chứng / File:* 6 ảnh `01_mealie_landing.png` đến `06_servings_scale.png` nhúng trong [`Documents/bao_cao_phan_C.md`](Documents/bao_cao_phan_C.md).
  - *Kết quả kiểm tra:* Đường dẫn chính xác `assets/0x_*.png`, tất cả ảnh hiển thị hợp lệ.
  - *Việc còn thiếu:* Không.

- [ ] **N3.1.3** — Bàn giao cho **Bùi Trung Hiếu** cài đặt thẩm định chéo trên máy sạch, tiếp thu góp ý để hoàn thiện.
  - *Bằng chứng / File:* Đang chờ biên bản thẩm định chéo bước H1.2 từ Hiếu.
  - *Kết quả kiểm tra:* Tài liệu đã sẵn sàng để bàn giao cho Hiếu kiểm thử độc lập từ máy sạch.
  - *Việc còn thiếu:* **Chờ Hiếu thực hiện thẩm định chéo và phản hồi.** (Không tự ý tích hoàn thành).

- [x] **N3.1.4** — Commit tài liệu On-boarding Phần C và bảng tiến độ riêng.
  - *Bằng chứng / File:* Nhánh `2312695-NguyenPhamPhuNam-Phan1`.
  - *Kết quả kiểm tra:* Commit và push đúng quy trình.
  - *Việc còn thiếu:* Không.

---

## 4. PHẦN 2 (CUỐI KỲ — PROPERTY-BASED TESTING & RUNNER)
- **Trạng thái:** **TẠM DỪNG / CHƯA TRIỂN KHAI TRONG ĐỢT NÀY** (theo chỉ đạo tập trung hoàn thành Phần 1 phục vụ Giữa kỳ 20/10).
- **Lưu trữ an toàn:** Toàn bộ mã nguồn PBT Property 5 (`test_pbt_fraction.py`), Docker Test Runner (`Dockerfile.test`, `docker-compose.test.yml`) và lịch sử Git các nhánh cũ đã được đóng gói an toàn vào:
  - Git Bundle: `d:\Nam 4\Kiểm thử phần mềm CTK47-PM\backup_nam_ktpm_20261007\nam_repo_all_branches.bundle` (đã verify).
  - Thư mục sao lưu ngoài repo: `d:\Nam 4\Kiểm thử phần mềm CTK47-PM\backup_nam_ktpm_20261007\`.
- Sẽ mở lại và triển khai khi có yêu cầu chuyển sang Phần 2 sau mốc Giữa kỳ 20/10.

---

## 5. BẰNG CHỨNG KIỂM CHỨNG THỰC NGHIỆM ĐỘC LẬP (MÔI TRƯỜNG SẠCH)

Thực hiện kiểm chứng độc lập trên container `mealie-verify-clean` (cổng 9935, named volume hoàn toàn mới `mealie-verify-clean-volume`) để đảm bảo không phụ thuộc vào bất kỳ dữ liệu cũ nào:

### 5.1. Quy trình cài đặt mới và kiểm chứng phân quyền RBAC (Yêu cầu 1 & 4)
- **Quy trình:**
  1. Khởi động container Mealie v3.28.0 SQLite với named volume mới trên cổng host `9935`.
  2. Đăng nhập tài khoản ban đầu `changeme@example.com` / `MyPassword` (`HTTP 200`).
  3. Tạo tài khoản Quản trị viên `admin@nhom6.test` (`admin: True`) qua `POST /api/admin/users` (`HTTP 201`).
  4. Tạo tài khoản người dùng thường `test@nhom6.test` (`admin: False`) qua `POST /api/admin/users` (`HTTP 201`).
- **Kết quả đo đạc phân quyền qua API:**
  - `admin@nhom6.test`: admin flag = `True`. Gọi `GET /api/admin/users` -> **HTTP 200 OK** (trả về danh sách 3 tài khoản).
  - `test@nhom6.test`: admin flag = `False`. Gọi `GET /api/admin/users` -> **HTTP 403 Forbidden** (`{"detail":"Forbidden"}`).
  - `test@nhom6.test` gọi `POST /api/admin/users` (thử tạo user mới) -> **HTTP 403 Forbidden** (`{"detail":"Forbidden"}`).
  - *Kết luận:* Cơ chế RBAC kiểm soát quyền hạn chính xác; tài khoản thường không thể truy cập tài nguyên quản trị.

### 5.2. Kiểm chứng tính Idempotent của Seed Script qua 2 lần chạy liên tiếp (Yêu cầu 3)
Chạy script `seed_data.py` hai lần liên tiếp trên môi trường sạch và truy vấn trực tiếp API:

| Đối tượng đo đạc | Sau Lần 1 | Sau Lần 2 | Độ lệch (Tăng thêm) | Đánh giá |
|---|:---:|:---:|:---:|:---:|
| **Số tài khoản mẫu** | 3 users | 3 users | **+0** | Giữ nguyên danh sách người dùng |
| **Số công thức NAM** | 10 công thức | 10 công thức | **+0** | Không nhân đôi bản ghi (`NAM-01`..`NAM-10`) |
| **Số mục thực đơn** | 14 bữa ăn | 14 bữa ăn | **+0** | 7 ngày x 2 bữa không phát sinh trùng lặp |

*Kết luận:* Script seed đạt 100% tính lũy đẳng (idempotent), tự động đối chiếu slug và ngày trước khi ghi.

### 5.3. Kiểm chứng định lượng Servings Scaling của NAM-10 (Yêu cầu 4)
- **Công thức:** `NAM-10 Bò Sốt Tiêu Khẩu Phần Chuẩn` (khẩu phần mặc định: 4 servings).
- **Hệ số scale:** Đổi từ 4 lên 8 servings ($k = 8 / 4 = 2.0\times$).
- **Định lượng trước/sau:**
  - Thịt bò (Beef): `400 grams` -> `800 grams` ($2.0\times$).
  - Tiêu đen (Black pepper): `2 tablespoons` -> `4 tablespoons` ($2.0\times$).
  - Nước dùng bò (Beef broth): `1/2 cup` (`0.5 cup`) -> `1 cup` ($2.0\times$).
  - Tỏi (Garlic): `4 cloves` -> `8 cloves` ($2.0\times$).
- *Kết luận:* Giao diện Mealie tính toán tỷ lệ nhân 2 chính xác cho tất cả 4 nguyên liệu, khớp 100% với ảnh [`Documents/assets/06_servings_scale.png`](Documents/assets/06_servings_scale.png).

### 5.4. Đối chiếu 6 ảnh minh chứng trực tiếp (Yêu cầu 2)
1. `01_mealie_landing.png`: Giao diện Sign In Mealie v3.28.0 chuẩn.
2. `02_mealie_dashboard.png`: Dashboard người dùng Quản trị viên nhóm 6.
3. `03_meal_plan.png`: Thực đơn 7 ngày tuần 06/10–12/10 (bữa sáng + tối).
4. `04_recipe_import.png`: Import thành công món Phở Bò Hà Nội từ mock server cục bộ qua JSON-LD.
5. `05_ingredient_parse.png`: Bóc tách `1 onion (finely chopped)` trong `NAM-08 Súp Hành Tây Pháp` thành `Qty=1`, `Unit=None`, `Food=onion`, `Note=finely chopped` (Confidence: 100.00%). Khớp ảnh thật.
6. `06_servings_scale.png`: Món `NAM-10 Bò Sốt Tiêu Khẩu Phần Chuẩn` scale từ 4 lên 8 servings, nhân đôi 4 nguyên liệu. Khớp ảnh thật.

### 5.5. Kết luận trạng thái nghiệm thu Phần 1 (Yêu cầu 5)
- **Phần đã tự kiểm tra thực nghiệm đạt:**
  - Nhóm việc N1: Môi trường Docker Mealie SQLite v3.28.0, Admin setup, 2 ảnh minh chứng Landing/Dashboard.
  - Nhóm việc N2: Seed data 10 món NAM, thực đơn 7 ngày, 4 ảnh minh chứng 3 luồng, idempotent test đạt +0, scaling chính xác.
  - Nhóm việc N3: Tài liệu On-boarding C.1 đến C.5 đầy đủ, kết quả thực nghiệm môi trường sạch C.4.4.
- **Phần còn thiếu / Đang chờ:**
  - **N3.1.3:** Đang chờ bạn **Bùi Trung Hiếu** thẩm định chéo độc lập từ máy sạch theo phân công bước H1.2. Giữ nguyên ô trống `[ ]` cho đến khi có biên bản phản hồi chính thức.
