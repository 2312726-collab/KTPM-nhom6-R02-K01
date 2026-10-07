# BIÊN BẢN THẨM ĐỊNH CHÉO TÀI LIỆU ON-BOARDING (CROSS-VALIDATION REPORT)
## ĐỒ ÁN MÔN KIỂM THỬ PHẦN MỀM — NHÓM 6

* **Người thực hiện thẩm định chéo:** **Bùi Trung Hiếu** *(MSSV: `2110037` | GitHub username: `2312611-Hieu` — Vai trò: Test Architect & Cross-validator)*
* **Đối tượng tiếp nhận phản hồi:** **Nguyễn Phạm Phú Nam** *(MSSV: `2312695` — Phụ trách On-boarding & Môi trường DevOps)*
* **Nguồn tài liệu & cấu hình thẩm định:**
  - Nhánh Git của Nam: **`2312695-NguyenPhamPhuNam-Phan1`** *(Không dùng nhánh `feat/nam-property-5-fraction` cũ)*
  - Commit SHA được thẩm định: **`600a16ebf66cbb167dde9c6b832adc3afa2df77f`** *(Commit hoàn thiện Báo cáo Phần C và tiến độ của Nam ngày 07/10/2026)*
  - Các tệp tài liệu và mã nguồn kiểm tra: `Documents/bao_cao_phan_C.md`, `mealie_docker/docker-compose.yml`, `mealie_docker/.env.example`, `mealie_docker/seed/seed_data.py`, `mealie_docker/seed/mock_recipe_server.py`.
* **Thời gian thực hiện thẩm định:** 07/10/2026
* **Môi trường máy cá nhân kiểm thử:**
  - Hệ điều hành: Windows 11 Pro 64-bit
  - Runtime: Python 3.14.0 64-bit
  - Nền tảng container: Docker Desktop v28.x (Service: `com.docker.service`)

---

### 1. ĐỐI CHIẾU CẤU HÌNH CỔNG VÀ PHÂN ĐỊNH RANH GIỚI HỆ THỐNG

#### 1.1. Đối chiếu cấu hình cổng Host / Container của Mealie
Trong file cấu hình `mealie_docker/docker-compose.yml` (commit `f66d491`) và `.env.example`:
```yaml
ports:
  - "${MEALIE_PORT:-9925}:9000"
```
- **Cổng trên máy Host:** Cố định là **`9925`** (`BASE_URL=http://localhost:9925`).
- **Cổng nội bộ Container:** Cố định là **`9000`** (FastAPI backend lắng nghe).
- **Kết luận đối chiếu:** Bạn Nam đã thiết lập cổng **`9925:9000`** chuẩn xác, độc lập hoàn toàn với các cổng dịch vụ web thông thường. Do đó, **bỏ kiến nghị "chờ đổi cổng"** do không còn lỗi cấu hình cổng.

#### 1.2. Phân định ranh giới giữa Mealie Docker và Dependency chạy Test
- **Mealie Docker Runtime:** Bản phân phối container `ghcr.io/mealie-recipes/mealie:v3.28.0` là một môi trường độc lập, đã đóng gói toàn bộ thư viện bên trong image. Việc chạy Docker không yêu cầu cài đặt thư viện ngoài trên máy host.
- **Dependency chạy test (`requirements-test.txt`):** Các thư viện như `pint`, `pytest`, `hypothesis` là phụ thuộc của bộ test automation PBT chạy trên môi trường Python của máy trạm hoặc CI runner, hoàn toàn tách biệt với dịch vụ Mealie chạy qua Docker Compose.

---

### 2. KẾT QUẢ THỰC THI KIỂM THỬ TỪ ĐẦU THEO TÀI LIỆU NAM (NHIỆM VỤ H1.2.2)

Quá trình thẩm định được thực hiện bằng cách chạy từng dòng lệnh trực tiếp trên máy cá nhân theo hướng dẫn tại Mục C.2 và C.4 trong `Documents/bao_cao_phan_C.md` của Nam:

| Bước thực hiện | Lệnh thực thi thực tế | Kết quả ghi nhận | Phân loại trạng thái | Ghi chú & Chi tiết lỗi thực tế |
| :---: | :--- | :--- | :---: | :--- |
| **B1: Chuẩn bị biến môi trường** | `Copy-Item mealie_docker/.env.example mealie_docker/.env` | Thành công tạo file `.env` với các tham số: `MEALIE_PORT=9925`, `BASE_URL=http://localhost:9925`, `HTTP_ALLOW_LIST=host.docker.internal`. | **ĐẠT** | Cấu hình tham số rõ ràng, dễ hiểu. |
| **B2: Khởi chạy container Mealie** | `docker compose -f mealie_docker/docker-compose.yml --env-file mealie_docker/.env up -d` | **Thất bại khi kết nối Daemon** | **LỖI** | Lỗi trả về: `unable to get image ... failed to connect to the docker API at npipe:////./pipe/dockerDesktopLinuxEngine... The system cannot find the file specified`. Dịch vụ Windows `com.docker.service` đang ở trạng thái `Stopped` sau khi khởi động lại máy. |
| **B3: Truy cập Web UI** | Mở trình duyệt tại `http://localhost:9925` | Chưa mở được do container chưa khởi chạy thành công ở Bước B2. | **CHƯA THỰC HIỆN** | Tạm hoãn chờ dịch vụ Docker Desktop sẵn sàng. |
| **B4: Đăng nhập Admin** | Đăng nhập tài khoản `admin@nhom6.test` / `Admin123@` | Chưa thực hiện được do phụ thuộc Bước B3. | **CHƯA THỰC HIỆN** | Chờ container hoạt động để kiểm tra. |
| **B5: Nạp dữ liệu mẫu (Seed Data)** | `& ".\.venv\Scripts\python.exe" mealie_docker/seed/seed_data.py` | Chưa thực hiện gọi API nạp 10 công thức và thực đơn do server Mealie chưa online. | **CHƯA THỰC HIỆN** | Đã rà soát mã nguồn script `seed_data.py`: cấu trúc gọi API Mealie v1 token authentication và recipe creation là chuẩn xác. |
| **B6: Khởi chạy Mock Recipe Server** | `& ".\.venv\Scripts\python.exe" mealie_docker/seed/mock_recipe_server.py` | Đã rà soát mã nguồn server chạy cổng 9926 trả về JSON-LD schema.org/Recipe. | **CHƯA THỰC HIỆN ĐẦY ĐỦ** | Chờ Mealie container chạy để test luồng Import URL thực tế qua `host.docker.internal:9926`. |

---

### 3. TỔNG HỢP PHẢN HỒI VÀ KHUYẾN NGHỊ BÀN GIAO CHO NAM (NHIỆM VỤ H1.2.3)

Gửi phản hồi chính thức tới bạn **Nguyễn Phạm Phú Nam**:

1. **Điểm đạt & Đánh giá cao:**
   - Cấu hình file `mealie_docker/docker-compose.yml` rất chuẩn mực, sử dụng cổng **`9925:9000`** tránh hoàn toàn xung đột cổng phổ biến.
   - Các script `seed_data.py` và `mock_recipe_server.py` được tổ chức bài bản, có tính tự động hóa cao và cơ chế kiểm tra idempotent tốt.
   - Tài liệu `Documents/bao_cao_phan_C.md` tại commit `600a16e` trình bày chi tiết, có ảnh minh chứng rõ ràng và đặc biệt là Mục C.5 (Xử lý sự cố thường gặp) đã dự liệu chính xác lỗi Docker Daemon (Lỗi 3).
2. **Khuyến nghị bổ sung:**
   - Khi bàn giao cho các thành viên khác trong nhóm thực hành on-boarding, Nam cần lưu ý nhắc các bạn mở **Docker Desktop** trước và đợi biểu tượng Docker chuyển sang màu xanh ổn định trước khi chạy lệnh `docker compose up -d`.
   - Bổ sung lệnh kiểm tra tình trạng container nhanh trong tài liệu:
     ```powershell
     docker compose -f mealie_docker/docker-compose.yml ps
     ```

---

### 4. KẾT LUẬN THẨM ĐỊNH

* **Trạng thái thẩm định:** **ĐÃ THẨM ĐỊNH TÀI LIỆU & CẤU HÌNH — CHỜ KHỞI ĐỘNG DOCKER DAEMON ĐỂ NGHIỆM THU RUNTIME (VERIFIED SPECIFICATION & CONFIGURATION, PENDING RUNTIME DEMO)**.
* **Đánh giá mức độ hoàn thiện:** Tài liệu Phần C và bộ cấu hình của Nam hoàn toàn đạt chuẩn về mặt kỹ thuật và thiết kế. Chưa kết luận 100% nghiệm thu cài đặt thực tế trên máy cá nhân do cần bật Docker Desktop để kiểm tra trọn vẹn luồng seed data.
* **Trạng thái bàn giao:** Đã lập biên bản phản hồi chính thức và chuyển giao cho bạn Nam tiếp nhận.
