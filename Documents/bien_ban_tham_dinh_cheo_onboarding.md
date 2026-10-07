# BIÊN BẢN THẨM ĐỊNH CHÉO TÀI LIỆU ON-BOARDING (CROSS-VALIDATION REPORT)
## ĐỒ ÁN MÔN KIỂM THỬ PHẦN MỀM — NHÓM 6

* **Đối tượng thẩm định:** Tài liệu hướng dẫn On-boarding & triển khai Docker Mealie (`Phần C`) do **Nguyễn Phạm Phú Nam** xây dựng.
* **Người thực hiện thẩm định chéo:** **Bùi Trung Hiếu** *(MSSV: 2312695 | GitHub: 2312611-Hieu — Vai trò: Test Architect & Cross-validator)*
* **Thời gian thẩm định:** 07/10/2026
* **Môi trường thực nghiệm:**
  - Hệ điều hành: Windows 11 Pro 64-bit
  - Docker Desktop: v28.x (Docker Engine active)
  - Python runtime: Python 3.14.0 64-bit

---

### 1. KẾT QUẢ THỬ NGHIỆM ĐỘC LẬP TỪ MÁY SẠCH (REPRODUCIBILITY CHECK)

Quá trình thẩm định thực hiện bằng cách làm theo từng bước hướng dẫn trong tài liệu của Nam từ một thư mục mới:

| Bước kiểm tra | Nội dung lệnh thực thi | Trạng thái | Ghi chú & Hiện tượng phát hiện |
| :---: | :--- | :---: | :--- |
| **B1** | Tạo môi trường ảo: `py -m venv .venv` | **THÀNH CÔNG** | Môi trường Python được khởi tạo chuẩn xác. |
| **B2** | Cài đặt phụ thuộc: `.\.venv\Scripts\pip install -r requirements-test.txt` | **THÀNH CÔNG** | Pytest 8.4.2, Hypothesis 6.168.5, Pydantic 2.13.5 đã cài đặt hoàn tất. |
| **B3** | Kiểm tra chạy Pytest: `.\.venv\Scripts\pytest --version` | **THÀNH CÔNG** | Pytest runner nhận diện đúng cấu hình `pytest.ini`. |
| **B4** | Khởi chạy Docker Mealie: `docker compose up -d` | **CÓ RỦI RO** | Phát hiện xung đột cổng (Port conflict) thực tế. |

---

### 2. CÁC PHÁT HIỆN KỸ THUẬT & DANH MỤC LỖI CẦN CẬP NHẬT GẤP (FEEDBACK TO NAM)

Sau khi chạy thực tế trên máy cá nhân, tôi ghi nhận 3 vấn đề kỹ thuật quan trọng gửi bạn **Nguyễn Phạm Phú Nam** để bổ sung vào tài liệu Phần C trước khi nộp Báo cáo Giữa kỳ:

#### ⚠️ Phát hiện 1: Nguy cơ xung đột cổng 9000 (Port 9000 Collision)
- **Hiện tượng thực tế:** Trong file `docker-compose.yml` gốc của dự án đang mở cổng `9000:9000`. Khi chạy thử nghiệm, máy trạm đang có các dịch vụ nền khác (cụ thể là container MinIO `culinaryblog-minio` hoặc Portainer) đã chiếm sẵn cổng `9000-9001`. Nếu người dùng gõ `docker compose up -d`, Docker sẽ quăng lỗi:
  ```text
  Error response from daemon: driver failed programming external connectivity on endpoint mealie_service: Bind for 0.0.0.0:9000 failed: port is already allocated
  ```
- **Khuyến nghị khắc phục:**
  - Thống nhất chuyển sang cổng **`9925`** như Nam đã dự kiến trong tài liệu Phần C (`ports: - "9925:9000"`).
  - Khuyến nghị sử dụng cú pháp tham số linh hoạt trong `docker-compose.yml`:
    ```yaml
    ports:
      - "${MEALIE_PORT:-9925}:9000"
    ```
  - Đồng thời cập nhật `BASE_URL=http://localhost:9925` trong file cấu hình `.env`.

---

#### ⚠️ Phát hiện 2: Thiếu thư viện phụ thuộc `pint` trong `requirements-test.txt`
- **Hiện tượng thực tế:**
  Khi kiểm tra khả năng chạy kiểm thử đơn vị đối với module `mealie/services/parser_services/parser_utils/unit_utils.py` (lớp `UnitConverter` do Hiếu phụ trách viết kịch bản Property 2):
  Lớp này gọi trực tiếp:
  ```python
  from pint import UnitRegistry, Unit, Quantity
  ```
  Tuy nhiên trong `requirements-test.txt` hiện tại **chưa có khai báo thư viện `pint`**. Khi chạy thử lệnh `python -c "import pint"` trong môi trường ảo `.venv` thì bị ném lỗi:
  ```text
  ModuleNotFoundError: No module named 'pint'
  ```
- **Khuyến nghị khắc phục:**
  Bổ sung ngay dòng sau vào file `requirements-test.txt`:
  ```text
  # Physical quantity and unit conversion
  pint>=0.23,<1.0.0
  ```

---

#### ⚠️ Phát hiện 3: Quyền hạn thư mục dữ liệu trên Windows (Permission / Volume Mount)
- **Hiện tượng:**
  Nếu người dùng map volume dạng bind-mount đường dẫn thư mục cục bộ của Windows (`./mealie-data:/app/data`), container Mealie chạy user UID 1000 có thể bị từ chối quyền ghi (Permission Denied) với database SQLite `mealie.db`.
- **Khuyến nghị khắc phục:**
  - Giữ nguyên cấu hình sử dụng Docker Named Volume (`mealie-data:`) như hiện tại vì Docker engine sẽ tự động quản lý quyền sở hữu tệp tin (ownership/permission), không bị vỡ trên cả Windows, macOS lẫn Linux.
  - Cần ghi chú rõ mục này vào mục **C.5: Xử lý sự cố thường gặp (Troubleshooting)** trong báo cáo Phần C.

---

### 3. KẾT LUẬN THẨM ĐỊNH
- **Đánh giá chung:** Tài liệu On-boarding và thiết kế container của Nam có cấu trúc rất tốt, dễ tiếp cận và khả thi.
- **Tình trạng nghiệm thu chéo:** **ĐẠT (PASSED WITH RECOMMENDATIONS)** — Sau khi Nam cập nhật 2 điểm lưu ý về cổng `9925` và bổ sung `pint` vào `requirements-test.txt`, tài liệu sẽ đạt tính tái lập 100% cho mọi thành viên và Giảng viên hướng dẫn.
