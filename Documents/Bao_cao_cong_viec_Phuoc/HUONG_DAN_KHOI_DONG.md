# HƯỚNG DẪN KHỞI ĐỘNG VÀ VẬN HÀNH HỆ THỐNG MEALIE

Tài liệu này hướng dẫn chi tiết các bước khởi động, truy cập và vận hành hệ thống Mealie phục vụ công tác demo và đánh giá.

---

## 1. YÊU CẦU TIÊN QUYẾT
- Máy tính cá nhân đã cài đặt và đang chạy **Docker Desktop** (Windows / macOS) hoặc **Docker Engine** (Linux).
- Cổng mạng `9925` trên máy chưa bị chiếm dụng bởi ứng dụng khác.

---

## 2. KHỞI ĐỘNG HỆ THỐNG (BẰNG DOCKER COMPOSE)

### Bước 1: Mở Terminal / PowerShell tại thư mục dự án
Điều hướng đến thư mục chứa mã nguồn dự án:
```powershell
cd f:\KTPM\mealie
```

### Bước 2: Khởi chạy hệ thống bằng Docker Compose
Chạy lệnh sau để khởi động container ở chế độ chạy ngầm (background):
```powershell
docker compose up -d
```
*(Nếu trên máy có thiết lập đường dẫn riêng cho Docker Desktop, có thể dùng `& "C:\Program Files\Docker\Docker\resources\bin\docker.exe" compose up -d`)*

### Bước 3: Kiểm tra trạng thái container
Kiểm tra xem container `mealie` đã khởi chạy thành công:
```powershell
docker ps
```
Xem nhật ký hoạt động (logs) của container:
```powershell
docker logs mealie --tail 20
```
Khi xuất hiện thông báo `Application startup complete. Uvicorn running on http://0.0.0.0:9000`, hệ thống đã sẵn sàng phục vụ.

---

## 3. THÔNG TIN TRUY CẬP VÀ ĐĂNG NHẬP

- **Địa chỉ giao diện Web (UI)**: [http://localhost:9925](http://localhost:9925)
- **Tài liệu API tương tác (Swagger UI)**: [http://localhost:9925/docs](http://localhost:9925/docs)
- **Tài khoản Quản trị viên (Admin) mặc định**:
  - **Email / Username**: `changeme@example.com`
  - **Mật khẩu (Password)**: `MyPassword`
- *(Hệ thống cũng đã bật tính năng `ALLOW_SIGNUP=true`, bạn có thể bấm "Register" trên màn hình đăng nhập để tạo tài khoản mới nếu muốn).*

---

## 4. HƯỚNG DẪN TRẢI NGHIỆM 03 LUỒNG NGHIỆP VỤ DEMO TRÊN GIAO DIỆN

Hệ thống đã được nạp sẵn dữ liệu thực tế cho 03 luồng nghiệp vụ cốt lõi:

### 4.1. Luồng 1: Quản lý Công thức nấu ăn (Recipe Management)
1. Đăng nhập vào hệ thống tại `http://localhost:9925`.
2. Trên thanh điều hướng bên trái hoặc menu trên cùng, chọn mục **Recipes**.
3. Bạn sẽ nhìn thấy món ăn đã được tạo sẵn: **"Pho Bo Ha Noi"**.
4. Nhấp vào món ăn để xem chi tiết:
   - Thời gian chuẩn bị & nấu: `120 phút`.
   - Khẩu phần: `4 bát`.
   - Danh sách nguyên liệu chi tiết (Bánh phở, thịt bò thăn, xương ống, gia vị quế hồi gừng).
   - 3 bước hướng dẫn nấu ăn từng bước.
5. Bạn có thể nhấn biểu tượng **Edit** để chỉnh sửa thông tin hoặc bấm **+ Create** để tạo thêm món ăn mới.

### 4.2. Luồng 2: Lập Kế hoạch Bữa ăn (Meal Planning)
1. Trên menu chính, nhấp chọn mục **Meal Planner** (hoặc biểu tượng lịch).
2. Quan sát lịch ngày hiện tại (hoặc tuần hiện tại):
   - Bạn sẽ thấy ô **Bữa tối (Dinner)** đã được lên lịch sẵn với món **Pho Bo Ha Noi**.
3. Bạn có thể nhấp vào bữa ăn để xem chi tiết công thức, kéo thả để đổi ngày, hoặc nhấp vào ô ngày khác để lên thực đơn cho các ngày tiếp theo trong tuần.

### 4.3. Luồng 3: Quản lý Danh sách Mua sắm (Shopping List)
1. Trên menu chính, nhấp chọn mục **Shopping Lists**.
2. Chọn danh sách đã tạo sẵn: **"Di cho cuoi tuan"**.
3. Trong danh sách:
   - Mục **"500g Banh pho tuoi"** đang ở trạng thái đã gạch bỏ / đánh dấu tích (Đã mua).
   - Mục **"400g Thit bo than"** đang ở trạng thái chờ mua.
4. Bạn có thể bấm vào ô tick để chuyển đổi trạng thái đã mua/chưa mua, hoặc nhập thêm món cần mua vào ô bên dưới rồi nhấn Enter.

---

## 5. CÁC LỆNH QUẢN TRỊ VÀ BẢO TRÌ TIỆN ÍCH

### Xem nhật ký theo thời gian thực (Real-time logs)
```powershell
docker compose logs -f
```

### Dừng hệ thống
```powershell
docker compose stop
```

### Khởi động lại hệ thống
```powershell
docker compose start
```

### Dừng và gỡ bỏ container (Dữ liệu vẫn được giữ nguyên trong volume)
```powershell
docker compose down
```

---

## 6. PHƯƠNG ÁN KHỞI ĐỘNG LOCAL DEV (CHO LẬP TRÌNH VIÊN)
Nếu muốn phát triển mã nguồn trực tiếp không qua Docker container:
1. Cài đặt Python 3.14 và `uv`, Node.js 22+ và `pnpm`.
2. Cài đặt thư viện:
   ```powershell
   task setup
   ```
3. Chạy Backend (cổng 9000):
   ```powershell
   uv run python mealie/app.py
   ```
4. Chạy Frontend (cổng 3000):
   ```powershell
   cd frontend
   pnpm run dev --no-fork
   ```
5. Truy cập frontend tại `http://localhost:3000`.
