# BẢNG PHÂN CÔNG NHIỆM VỤ NGUYÊN TỬ — NHÓM 6
**Đề tài:** Mealie (R02) + Property-Based Testing với Hypothesis (K01)  
**Môn:** Kiểm thử phần mềm | **GVHD:** Nguyễn Thế Lâm

---

> **Quy ước chung:**
> - Mỗi ô checkbox `[ ]` = 1 bước công việc độc lập, kiểm tra được ngay.
> - Mỗi nhóm bước lớn = 1 `git commit` riêng biệt.
> - Commit message chuẩn: `feat(test):`, `docs:`, `chore:`, `fix(test):`, `test:`.
> - **Nguyên tắc phân công:** Khối lượng và độ phức tạp kỹ thuật được chia đều cho 4 thành viên (Nam, Hiếu, Phước, Mạnh) ở cả 2 giai đoạn (Giữa kỳ và Cuối kỳ); công việc quản trị, kiến trúc và điều phối của Trưởng nhóm Quân giữ nguyên vẹn.

---
---

# 👤 THÀNH VIÊN 1: TRẦN QUỐC QUÂN
> **Vai trò:** Trưởng nhóm — Quản trị dự án, Phân tích kiến trúc, Tổng hợp báo cáo  
> **Báo cáo phụ trách chính:** Phần A, Phần B, Phần H + Điều phối toàn bộ

---

## ✅ NHÓM VIỆC Q1: KHỞI ĐỘNG DỰ ÁN & THIẾT LẬP GIT
**Deadline: 30/9**

### Q1.1 — Tạo kho chứa Git của nhóm
- [x] Q1.1.1 Tạo repository mới trên GitHub: `https://github.com/2312726-collab/KTPM-nhom6-K02-R01.git`.
- [x] Q1.1.2 Thêm file `README.md` ban đầu: Tên nhóm, đề tài, danh sách 5 thành viên, link repo Mealie.
- [ ] Q1.1.3 Mời 4 thành viên còn lại vào repo (Settings → Collaborators → Add people).
- [ ] Q1.1.4 Xác nhận cả 5 thành viên đã Accept lời mời và thấy repo trên tài khoản GitHub của mình.

### Q1.2 — Thiết lập quy tắc nhánh Git
- [x] Q1.2.1 Tạo nhánh `develop` từ `main` và đẩy lên GitHub:
  ```bash
  git checkout -b develop
  git push -u origin develop
  ```
- [ ] Q1.2.2 Bảo vệ nhánh `main`: Settings → Branches → Add Rule → chọn `main` → tick *"Require pull request before merging"*.
- [x] Q1.2.3 Tạo file `.github/COMMIT_CONVENTION.md` với nội dung quy ước commit:
  - `docs: ...` — Thêm/sửa tài liệu
  - `feat(test): ...` — Thêm kịch bản kiểm thử mới
  - `fix(test): ...` — Sửa lỗi trong mã kiểm thử
  - `chore: ...` — Cấu hình, setup môi trường
  - `test: ...` — Chạy test, thu thập log/artifacts
- [x] Q1.2.4 Commit & push: `docs: add commit convention`.
- [ ] Q1.2.5 Gửi link repo cho cả nhóm qua chat: `https://github.com/2312726-collab/KTPM-nhom6-K02-R01`.

### Q1.3 — Cố định phiên bản Mealie (Pin Version)
- [x] Q1.3.1 Tạo file `Documents/mealie_version.md` ghi lại:
  - Repository: `https://github.com/mealie-recipes/mealie`
  - Release Tag: **`v3.28.0`**
  - Commit SHA: `0552eaa4a80031b8572849cca0ed95d07f1be001`
  - Ngày chốt phiên bản: 06/10/2026
- [x] Q1.3.2 Kiểm tra tag còn tồn tại: mở `https://github.com/mealie-recipes/mealie/tree/v3.28.0`.
- [x] Q1.3.3 Commit: `docs: pin mealie version v3.28.0`.

### Q1.4 — Thiết lập bảng quản lý công việc
- [ ] Q1.4.1 Tạo GitHub Project Board: Projects → New Project → Board view.
- [ ] Q1.4.2 Tạo 4 cột: **Todo | In Progress | Review | Done**.
- [ ] Q1.4.3 Tạo Issues tương ứng với các nhóm việc (Q1→Q3, N1→N5, H1→H4, P1→P4, M1→M4).
- [ ] Q1.4.4 Assign đúng Issue cho đúng thành viên phụ trách.
- [ ] Q1.4.5 Họp nhóm online 15 phút mỗi thứ Hai để cập nhật tiến độ thẻ.

---

## ✅ NHÓM VIỆC Q2: PHÂN TÍCH KIẾN TRÚC HỆ THỐNG MEALIE
**Deadline: 18/10** | Đầu ra: `Documents/bao_cao_phan_A.md` + `Documents/bao_cao_phan_B.md`

### Q2.1 — Clone mã nguồn và đọc cấu trúc thư mục
- [ ] Q2.1.1 Clone Mealie đúng tag về máy cá nhân:
  ```bash
  git clone --branch v3.28.0 --depth 1 https://github.com/mealie-recipes/mealie.git mealie_src
  ```
- [ ] Q2.1.2 Mở `mealie_src/` bằng VS Code, đọc qua toàn bộ thư mục gốc.
- [ ] Q2.1.3 Đọc `mealie/app.py` và `mealie/main.py` để hiểu điểm khởi động ứng dụng.
- [ ] Q2.1.4 Đọc `mealie/routes/` để liệt kê các nhóm API endpoint chính.
- [ ] Q2.1.5 Đọc `pyproject.toml` để liệt kê các dependency quan trọng (FastAPI, SQLAlchemy, Pydantic...).

### Q2.2 — Soạn thảo Phần A: Mô tả hệ thống
- [ ] Q2.2.1 Tạo file `Documents/bao_cao_phan_A.md`.
- [ ] Q2.2.2 Viết mô tả mục tiêu hệ thống Mealie (3–5 câu).
- [ ] Q2.2.3 Liệt kê 2 Actor: **Home User** (xem công thức, lập thực đơn) và **Admin** (quản lý người dùng, cài đặt).
- [ ] Q2.2.4 Liệt kê 5 Use Case chính:
  1. Thêm/import công thức nấu ăn.
  2. Phân tích chuỗi nguyên liệu (Ingredient Parsing).
  3. Nhân chia tỉ lệ khẩu phần ăn (Servings Scaling).
  4. Lập kế hoạch thực đơn (Meal Planning).
  5. Quy đổi đơn vị đo lường (Unit Conversion).
- [ ] Q2.2.5 Ghi lại cây thư mục chính của Mealie (tập trung vào `mealie/`, `frontend/`, `tests/`, `docker/`).
- [ ] Q2.2.6 Commit: `docs: add system description Phan A`.

### Q2.3 — Soạn thảo Phần B: Kiến trúc & Luồng dữ liệu
- [ ] Q2.3.1 Tạo file `Documents/bao_cao_phan_B.md`.
- [ ] Q2.3.2 Vẽ **sơ đồ kiến trúc tổng thể** (dùng draw.io hoặc Mermaid): `Browser → Frontend Vue → FastAPI Backend → SQLite/PostgreSQL`. Xuất ảnh lưu `Documents/assets/kien_truc_container.png`.
- [ ] Q2.3.3 Vẽ **Data Flow của nghiệp vụ Ingredient Parsing**:
  ```
  [User nhập chuỗi] → [API /parse] → [IngredientParserService]
  → [parser_utils: string_utils, unit_utils] → [Kết quả JSON]
  ```
- [ ] Q2.3.4 Vẽ **Data Flow của nghiệp vụ Servings Scaling**.
- [ ] Q2.3.5 Vẽ **Data Flow của nghiệp vụ Meal Planning**.
- [ ] Q2.3.6 Phân tích mô tả 3 module trọng tâm (mỗi module ~150 chữ):
  - `mealie/services/parser_services/ingredient_parser.py`
  - `mealie/services/parser_services/parser_utils/string_utils.py`
  - `mealie/services/parser_services/parser_utils/unit_utils.py`
- [ ] Q2.3.7 Chèn tất cả sơ đồ + mô tả vào `bao_cao_phan_B.md`.
- [ ] Q2.3.8 Commit: `docs: add architecture diagrams Phan B`.

---

## ✅ NHÓM VIỆC Q3: TỔNG HỢP BÁO CÁO & SLIDE
**Deadline: 19/10 (Giữa kỳ)** | **12/12 (Cuối kỳ)**

### Q3.1 — Báo cáo Giữa kỳ (20/10)
- [ ] Q3.1.1 Thu nhận `bao_cao_phan_C.md` từ **Nam** (hạn 18/10).
- [ ] Q3.1.2 Thu nhận đề cương kế hoạch kiểm thử từ **Hiếu** (hạn 18/10).
- [ ] Q3.1.3 Gộp thành 1 file `Documents/bao_cao_giua_ky.md`.
- [ ] Q3.1.4 Soạn Slide giữa kỳ (tối thiểu 12 slide): Bìa, Mục tiêu hệ thống, Kiến trúc, Data Flow, Demo hệ thống chạy, On-boarding tóm tắt, Kế hoạch PBT, Phân công nhóm, Timeline.

### Q3.2 — Báo cáo Cuối kỳ & Phần H (Tháng 12)
- [ ] Q3.2.1 Thu nhận toàn bộ Phần D, E từ **Hiếu** (hạn 10/11).
- [ ] Q3.2.2 Thu nhận Phần F từ **Phước** (hạn 30/11).
- [ ] Q3.2.3 Thu nhận Phần G từ **Mạnh** (hạn 10/12).
- [ ] Q3.2.4 Biên tập cuốn báo cáo cuối kỳ đầy đủ 8 phần A→H.
- [ ] Q3.2.5 Viết Phần H: Ghi lại Commit SHA của repo nhóm, tag `v1.0-final`, hướng dẫn người khác tái lập test từ đầu.
- [ ] Q3.2.6 Tạo Git Tag: `git tag v1.0-final && git push origin v1.0-final`.
- [ ] Q3.2.7 Soạn Slide cuối kỳ + điều phối buổi bảo vệ (phân vai thuyết trình cho từng thành viên).

---
---

# 👤 THÀNH VIÊN 2: NGUYỄN PHẠM PHÚ NAM
> **Vai trò:** DevOps & System On-boarding Specialist  
> **Báo cáo phụ trách chính:** Phần C (Tài liệu On-boarding & Bằng chứng hệ thống) + Mã kiểm thử Property 4 + Dockerized Test Runner

---

## ✅ NHÓM VIỆC N1: THIẾT LẬP MÔI TRƯỜNG CHẠY MEALIE (DOCKER COMPOSE)
**Deadline: 15/10**

### N1.1 — Cài đặt và xác minh Docker Desktop
- [ ] N1.1.1 Tải và cài đặt Docker Desktop từ [https://www.docker.com/products/docker-desktop/](https://www.docker.com/products/docker-desktop/).
- [ ] N1.1.2 Mở terminal kiểm tra: `docker --version` (yêu cầu Docker version 24.x trở lên).
- [ ] N1.1.3 Chạy container kiểm tra: `docker run hello-world` → in ra `Hello from Docker!`.

### N1.2 — Dựng Mealie bằng Docker Compose
- [ ] N1.2.1 Tạo thư mục `mealie_docker/` trong repo nhóm.
- [ ] N1.2.2 Tạo file `mealie_docker/docker-compose.yml` (bản SQLite chính thức của Mealie):
  ```yaml
  version: "3.8"
  services:
    mealie:
      image: ghcr.io/mealie-recipes/mealie:v3.28.0
      container_name: mealie_service
      restart: always
      ports:
        - "9925:9000"
      deploy:
        resources:
          limits:
            memory: 1000M
      volumes:
        - mealie-data:/app/data/
      environment:
        - ALLOW_SIGNUP=true
        - PUID=1000
        - PGID=1000
        - TZ=Asia/Ho_Chi_Minh
        - BASE_URL=http://localhost:9925
  volumes:
    mealie-data:
  ```
- [ ] N1.2.3 Tạo file `mealie_docker/.env` lưu biến cấu hình chuẩn.
- [ ] N1.2.4 Thêm `mealie-data/` vào `.gitignore`.
- [ ] N1.2.5 Khởi chạy dịch vụ: `docker-compose up -d`.
- [ ] N1.2.6 Kiểm tra log container: `docker-compose logs -f mealie` để đảm bảo FastAPI khởi động không lỗi.
- [ ] N1.2.7 Mở trình duyệt truy cập `http://localhost:9925`. Chụp ảnh màn hình Landing page → lưu `Documents/assets/01_mealie_landing.png`.

### N1.3 — Đăng ký tài khoản Admin và xác nhận Dashboard
- [ ] N1.3.1 Đăng ký tài khoản Admin đầu tiên: Email `admin@nhom6.test`, Password `Admin123@`.
- [ ] N1.3.2 Đăng nhập vào Dashboard quản trị thành công. Chụp ảnh màn hình Dashboard → lưu `Documents/assets/02_mealie_dashboard.png`.
- [ ] N1.3.3 Commit: `chore: setup docker-compose environment and initial admin credentials`.

---

## ✅ NHÓM VIỆC N2: CHUẨN BỊ SEED DATA & THỰC THI 3 LUỒNG NGHIỆP VỤ
**Deadline: 17/10**

### N2.1 — Tạo tài khoản kiểm thử và nạp dữ liệu mẫu
- [ ] N2.1.1 Tạo tài khoản người dùng kiểm thử thông thường: Settings → Manage Users → Add User (Email: `test@nhom6.test`, Password: `User123@`).
- [ ] N2.1.2 Tạo 10 công thức mẫu (Recipes) có độ phức tạp tăng dần:
  - Công thức 1–2: Nguyên liệu đơn giản (`2 cups flour`, `3 eggs`).
  - Công thức 3–4: Phân số thông thường (`1/2 tsp salt`, `2/3 cup sugar`).
  - Công thức 5–6: Phân số unicode đặc thù (`½ cup milk`, `¼ tsp pepper`, `¾ cup water`).
  - Công thức 7–8: Nguyên liệu kèm ghi chú trong ngoặc đơn (`2 cups flour (sifted)`, `1 egg (beaten)`).
  - Công thức 9–10: Công thức phức tạp nhiều bước nấu, nhiều đơn vị đo lường đan xen.
- [ ] N2.1.3 Tạo kế hoạch thực đơn (Meal Plan) cho 7 ngày trong tuần từ 06/10 đến 12/10. Chụp ảnh Meal Plan → lưu `Documents/assets/03_meal_plan.png`.

### N2.2 — Thực thi và thu thập bằng chứng 3 luồng nghiệp vụ cốt lõi
- [ ] N2.2.1 **Luồng 1 — Import công thức từ URL ngoài:**
  - Vào Recipes → Add Recipe → Import from URL. Nhập URL công thức chuẩn và thực hiện Import.
  - Chụp ảnh công thức đã import thành công → lưu `Documents/assets/04_recipe_import.png`.
- [ ] N2.2.2 **Luồng 2 — Phân tích chuỗi nguyên liệu (Ingredient Parsing):**
  - Trong Recipe Editor, nhập chuỗi `2 1/2 cups all-purpose flour, sifted` vào mục Ingredients.
  - Xác nhận Mealie tự động bóc tách thành: Quantity = `2.5`, Unit = `cup`, Food = `all-purpose flour`, Note = `sifted`.
  - Chụp ảnh kết quả phân tích → lưu `Documents/assets/05_ingredient_parse.png`.
- [ ] N2.2.3 **Luồng 3 — Nhân chia tỉ lệ khẩu phần ăn (Servings Scaling):**
  - Mở chi tiết 1 công thức đang có khẩu phần 4 servings. Thay đổi khẩu phần thành 8 servings.
  - Xác nhận số lượng các nguyên liệu tự động nhân gấp đôi theo đúng tỉ lệ.
  - Chụp ảnh kết quả nhân tỉ lệ → lưu `Documents/assets/06_servings_scale.png`.
- [ ] N2.2.4 Commit: `docs: seed test recipes and capture evidence for 3 core business flows`.

---

## ✅ NHÓM VIỆC N3: SOẠN THẢO TÀI LIỆU ON-BOARDING (PHẦN C)
**Deadline: 18/10**

### N3.1 — Soạn thảo `Documents/bao_cao_phan_C.md`
- [ ] N3.1.1 Tạo file `Documents/bao_cao_phan_C.md` gồm 5 nội dung chuẩn theo quy định:
  - **Mục C.1: Yêu cầu môi trường tối thiểu** (Hệ điều hành, Docker >= 24.0, Docker Compose >= 2.0, RAM >= 4GB, Dung lượng đĩa >= 5GB).
  - **Mục C.2: Quy trình cài đặt từng bước** (Clone mã nguồn, cấu hình `.env`, lệnh khởi chạy).
  - **Mục C.3: Quản lý dịch vụ** (Lệnh bật, dừng, khởi động lại, kiểm tra trạng thái và xem log container).
  - **Mục C.4: Hướng dẫn nạp Seed Data** (Cách tạo user, nhập 10 công thức mẫu và tạo Meal Plan).
  - **Mục C.5: Xử lý sự cố thường gặp** (Xung đột cổng 9925, lỗi cấp quyền thư mục volume, lỗi hết bộ nhớ).
- [ ] N3.1.2 Nhúng toàn bộ 6 ảnh minh chứng (`01_mealie_landing.png` đến `06_servings_scale.png`) vào các mục tương ứng trong báo cáo.
- [ ] N3.1.3 Bàn giao file cho **Hiếu** để kiểm thử chéo trên máy sạch độc lập. Tiếp nhận ý kiến đóng góp và chỉnh sửa hoàn thiện.
- [ ] N3.1.4 Commit: `docs: complete onboarding guide Phan C with verified evidence`.

---

## ✅ NHÓM VIỆC N4: CODE TEST PBT — PROPERTY 4 (SERVINGS SCALING MONOTONICITY)
**Deadline: 25/11**

### N4.1 — Nghiên cứu logic Scaling và thiết lập file test
- [ ] N4.1.1 Đọc logic nhân tỉ lệ khẩu phần trong `mealie/services/recipe/recipe_service.py` và schema `mealie/schema/recipe/recipe_ingredient.py`.
- [ ] N4.1.2 Xác định quy tắc: Khi scale factor $k > 1$, số lượng nguyên liệu mới $Q_{new} = Q \times k$ phải lớn hơn $Q$; khi $k < 1$, $Q_{new}$ phải nhỏ hơn $Q$; phép nghịch đảo $Q_{new} / k$ phải xấp xỉ bằng $Q$ ban đầu.
- [ ] N4.1.3 Tạo file `tests/unit_tests/test_pbt_scaling.py`.

### N4.2 — Hiện thực kịch bản kiểm thử Property 4
- [ ] N4.2.1 Viết kiểm thử tính đơn điệu (Monotonicity) khi scale khẩu phần:
  ```python
  from hypothesis import given, strategies as st, assume, settings

  @given(
      qty=st.floats(min_value=0.01, max_value=1000, allow_nan=False, allow_infinity=False),
      scale=st.floats(min_value=0.1, max_value=10.0, allow_nan=False, allow_infinity=False)
  )
  @settings(max_examples=300)
  def test_servings_scaling_monotonicity(qty, scale):
      assume(scale > 0 and qty > 0)
      scaled_qty = qty * scale
      if scale > 1.0:
          assert scaled_qty > qty, f"Scale {scale} > 1 nhưng {scaled_qty} <= {qty}"
      elif scale < 1.0:
          assert scaled_qty < qty, f"Scale {scale} < 1 nhưng {scaled_qty} >= {qty}"
  ```
- [ ] N4.2.2 Viết kiểm thử tính bảo toàn nghịch đảo (Reversibility of Scaling):
  ```python
  @given(
      qty=st.floats(min_value=0.01, max_value=1000, allow_nan=False, allow_infinity=False),
      scale=st.floats(min_value=0.1, max_value=10.0, allow_nan=False, allow_infinity=False)
  )
  @settings(max_examples=300)
  def test_servings_scaling_reversibility(qty, scale):
      assume(scale > 0 and qty > 0)
      scaled = qty * scale
      reverted = scaled / scale
      assert abs(reverted - qty) < 1e-4, f"Sai lệch nghịch đảo: ban đầu={qty}, phục hồi={reverted}"
  ```
- [ ] N4.2.3 Chạy kiểm thử: `pytest tests/unit_tests/test_pbt_scaling.py -v`.
- [ ] N4.2.4 Ghi nhận phản ví dụ nếu phát hiện sai số làm tròn số thực dấu phẩy động vào `Documents/ket_qua_test.md` và thông báo cho **Mạnh**.
- [ ] N4.2.5 Commit: `feat(test): add PBT Property 4 scaling monotonicity and reversibility`.

---

## ✅ NHÓM VIỆC N5: ĐÓNG GÓI DOCKERIZED TEST RUNNER ĐẢM BẢO TÁI LẬP
**Deadline: 02/12**

### N5.1 — Xây dựng môi trường chạy test biệt lập trong Docker
- [ ] N5.1.1 Tạo file `docker-compose.test.yml` để chạy toàn bộ suite test Python độc lập trên mọi máy tính mà không cần cài đặt Python thủ công:
  ```yaml
  version: "3.8"
  services:
    test-runner:
      image: python:3.11-slim
      working_dir: /workspace
      volumes:
        - .:/workspace
      command: >
        sh -c "pip install -e '.[dev]' hypothesis pytest pytest-cov &&
               pytest tests/unit_tests/test_pbt_*.py -v --tb=short"
  ```
- [ ] N5.1.2 Chạy thử nghiệm container kiểm thử: `docker compose -f docker-compose.test.yml run --rm test-runner`.
- [ ] N5.1.3 Xác nhận kết quả test chạy thành công và báo cáo được xuất đúng vào thư mục `logs/` tại máy host.
- [ ] N5.1.4 Bổ sung phần hướng dẫn chạy test qua Docker vào `tests/README.md` (phối hợp với Phước).
- [ ] N5.1.5 Commit: `chore: add docker-compose test runner for isolated reproducible testing`.

---
---

# 👤 THÀNH VIÊN 3: BÙI TRUNG HIẾU
> **Vai trò:** Test Architect & PBT Methodology Specialist  
> **Báo cáo phụ trách chính:** Phần D (Cơ sở lý thuyết PBT & Kế hoạch kiểm thử) + Phần E (Thiết kế kịch bản kiểm thử) + Mã kiểm thử Property 2 (Unit Conversion Round-trip)

---

## ✅ NHÓM VIỆC H1: NGHIÊN CỨU MODULE, ĐỀ CƯƠNG GIỮA KỲ & THẨM ĐỊNH PHẦN C
**Deadline: 18/10**

### H1.1 — Khảo sát module mục tiêu và lập đề cương kiểm thử
- [ ] H1.1.1 Đọc cấu trúc mã nguồn trong thư mục `mealie/services/parser_services/`.
- [ ] H1.1.2 Xác định rõ phạm vi kiểm thử: 3 file cốt lõi (`ingredient_parser.py`, `string_utils.py`, `unit_utils.py`).
- [ ] H1.1.3 Soạn thảo đề cương kế hoạch kiểm thử PBT sơ bộ cho mốc Giữa kỳ (mục tiêu PBT, công cụ Hypothesis, 3 properties dự kiến) bàn giao cho Trưởng nhóm Quân.

### H1.2 — Thẩm định chéo (Cross-validation) tài liệu On-boarding
- [ ] H1.2.1 Tiếp nhận file `Documents/bao_cao_phan_C.md` từ **Nam**.
- [ ] H1.2.2 Thực hiện cài đặt Mealie từ đầu trên máy cá nhân theo đúng từng dòng lệnh trong tài liệu On-boarding.
- [ ] H1.2.3 Xác nhận thời gian cài đặt, tính chính xác của các cổng mạng và khả năng đăng nhập Dashboard.
- [ ] H1.2.4 Lập bảng ghi nhận góp ý (lệnh nào thiếu, bước nào cần chú thích thêm) gửi lại Nam cập nhật.
- [ ] H1.2.5 Commit: `docs: outline midterm PBT test strategy and cross-validate onboarding`.

---

## ✅ NHÓM VIỆC H2: NGHIÊN CỨU LÝ THUYẾT HYPOTHESIS & SOẠN THẢO PHẦN D
**Deadline: 30/10**

### H2.1 — Nghiên cứu tài liệu chính thức của Hypothesis
- [ ] H2.1.1 Đọc [Hypothesis Quickstart](https://hypothesis.readthedocs.io/en/latest/quickstart.html): Nắm vững decorator `@given`, các `strategies`, cú pháp `assume()`, và cấu hình `@settings`.
- [ ] H2.1.2 Đọc [Strategies Reference](https://hypothesis.readthedocs.io/en/latest/data.html): Ghi chép 10 strategies cốt lõi (`st.text`, `st.integers`, `st.floats`, `st.lists`, `st.sampled_from`, `st.composite`,...).
- [ ] H2.1.3 Đọc [Shrinking Mechanism](https://hypothesis.readthedocs.io/en/latest/details.html#shrinking): Hiểu cách Hypothesis tự động tối giản hóa ca lỗi (counterexample) để báo cáo input ngắn nhất.

### H2.2 — Soạn thảo `Documents/bao_cao_phan_D.md`
- [ ] H2.2.1 Tạo file `Documents/bao_cao_phan_D.md`.
- [ ] H2.2.2 Viết **Mục D.1: Bản chất của Property-Based Testing**: So sánh chi tiết EBT vs PBT bằng bảng đối chiếu (nguồn dữ liệu, số lượng ca test, khả năng phát hiện lỗi biên, chi phí viết test).
- [ ] H2.2.3 Viết **Mục D.2: Cơ chế vận hành của Hypothesis**: Sơ đồ hóa 4 bước (Generate Data → Run Invariant Check → Shrink on Failure → Report Counterexample).
- [ ] H2.2.4 Viết **Mục D.3: Lý do chọn module `parser_services`**: Xử lý dữ liệu chuỗi phi cấu trúc, độ phức tạp cao, dễ phát sinh lỗi với input bất thường.
- [ ] H2.2.5 Viết **Mục D.4: Ranh giới phạm vi kiểm thử (Scope Boundary)**: Tập trung vào chuỗi nguyên liệu và quy đổi đơn vị theo triết lý Ponytail.
- [ ] H2.2.6 Viết **Mục D.5: Giả định kỹ thuật & Điều kiện tiên quyết** (Số lượng thực dương, độ dài chuỗi tối đa 500 ký tự).
- [ ] H2.2.7 Viết **Mục D.6 & D.7: Tiêu chí nghiệm thu Pass/Fail & Quản lý rủi ro** (Cách khắc phục Flaky test do floating-point, độ trễ sinh chuỗi unicode).
- [ ] H2.2.8 Commit: `docs: complete theoretical foundation and test methodology Phan D`.

---

## ✅ NHÓM VIỆC H3: THIẾT KẾ KỊCH BẢN KIỂM THỬ CHI TIẾT (PHẦN E)
**Deadline: 10/11**

### H3.1 — Soạn thảo `Documents/bao_cao_phan_E.md`
- [ ] H3.1.1 Tạo file `Documents/bao_cao_phan_E.md`.
- [ ] H3.1.2 Thiết kế bảng đặc tả chuẩn hóa cho **Property 1 — Tính lũy đẳng (Idempotence)**:
  - Hàm mục tiêu: `remove_footnote_markers(s)` và `move_parens_to_end(s)` trong `string_utils.py`.
  - Invariant toán học: $f(f(x)) == f(x)$ với mọi chuỗi văn bản $x$.
  - Hypothesis Strategy: `st.text()`.
  - Tiêu chí vi phạm: $f(f(x)) \neq f(x)$.
- [ ] H3.1.3 Thiết kế bảng đặc tả chuẩn hóa cho **Property 2 — Tính bảo toàn hai chiều (Round-trip)**:
  - Hàm mục tiêu: `UnitConverter.convert(val, from_unit, to_unit)` trong `unit_utils.py`.
  - Invariant toán học: $\text{convert}(\text{convert}(x, u_1, u_2), u_2, u_1) \approx x$ với sai số $\epsilon \le 10^{-4}$.
  - Hypothesis Strategy: `st.floats(min_value=0.001, max_value=100000, allow_nan=False)`.
  - Pre-condition: $x > 0$.
  - Tiêu chí vi phạm: $|\text{reverted} - x| > 10^{-4}$ hoặc phát sinh Exception.
- [ ] H3.1.4 Thiết kế bảng đặc tả chuẩn hóa cho **Property 3 — Tính bền bỉ / Bất khả sập (Crash-free Invariant)**:
  - Hàm mục tiêu: `BruteForceParser.parse_one(text)` trong `ingredient_parser.py`.
  - Invariant: Không bao giờ quăng ra Unhandled Exception với bất kỳ chuỗi Unicode nào.
  - Hypothesis Strategy: `st.text(max_size=500)`.
  - Tiêu chí vi phạm: Xuất hiện unhandled exception (500 Error, AttributeError, Regex error).
- [ ] H3.1.5 Thiết kế bảng đặc tả chuẩn hóa cho **Property 4 — Tính đơn điệu & Bảo toàn tỉ lệ (Scaling Monotonicity)**:
  - Hàm mục tiêu: Quy trình tính toán nhân khẩu phần ăn.
  - Invariant: Tính đơn điệu theo tỉ lệ scale và tính nghịch đảo $(Q \times k) / k \approx Q$.
- [ ] H3.1.6 Bàn giao tài liệu Phần E cho Phước, Nam và Mạnh làm căn cứ lập trình test.
- [ ] H3.1.7 Commit: `docs: design standardized PBT test scenarios for all 4 properties Phan E`.

---

## ✅ NHÓM VIỆC H4: CODE TEST PBT — PROPERTY 2 (UNIT CONVERSION ROUND-TRIP)
**Deadline: 25/11**

### H4.1 — Nghiên cứu mã nguồn UnitConverter
- [ ] H4.1.1 Đọc file `mealie/services/parser_services/parser_utils/unit_utils.py`.
- [ ] H4.1.2 Xác định class `UnitConverter` và danh sách các bảng quy đổi đơn vị (khối lượng, thể tích).
- [ ] H4.1.3 Tạo file `tests/unit_tests/test_pbt_unit_converter.py`.

### H4.2 — Hiện thực kịch bản kiểm thử Property 2
- [ ] H4.2.1 Viết kiểm thử Round-trip cho đơn vị khối lượng (`gram` $\leftrightarrow$ `kilogram`):
  ```python
  from hypothesis import given, strategies as st, assume, settings
  from mealie.services.parser_services.parser_utils.unit_utils import UnitConverter

  converter = UnitConverter()

  @given(st.floats(min_value=0.001, max_value=100000, allow_nan=False, allow_infinity=False))
  @settings(max_examples=300)
  def test_gram_kilogram_roundtrip(value):
      assume(value > 0)
      kg = converter.convert(value, "gram", "kilogram")
      back = converter.convert(kg, "kilogram", "gram")
      assert abs(back - value) < 1e-4, f"Lỗi Round-trip: {value} -> {kg} -> {back}"
  ```
- [ ] H4.2.2 Viết kiểm thử Round-trip cho các đơn vị thể tích thông dụng (`milliliter` $\leftrightarrow$ `liter`, `teaspoon` $\leftrightarrow$ `tablespoon`).
- [ ] H4.2.3 Viết kiểm thử xác nhận ngoại lệ có kiểm soát: Quy đổi giữa 2 đơn vị không cùng hệ đo lường (ví dụ `gram` sang `milliliter` khi không khai báo khối lượng riêng) phải ném ngoại lệ rõ ràng, không gây crash bất thường.
- [ ] H4.2.4 Chạy kiểm thử: `pytest tests/unit_tests/test_pbt_unit_converter.py -v`.
- [ ] H4.2.5 Ghi lại kết quả và phản ví dụ (nếu có lỗi sai số làm tròn số thực) vào `Documents/ket_qua_test.md` cho **Mạnh**.
- [ ] H4.2.6 Commit: `feat(test): add PBT Property 2 unit conversion round-trip`.

---
---

# 👤 THÀNH VIÊN 4: TRẦN NGỌC BẢO PHƯỚC
> **Vai trò:** QA Automation Engineer 1 — Test Harness & String Engine Verification  
> **Báo cáo phụ trách chính:** Phần F (Bộ kiểm thử tự động, cấu hình Test Harness & Hướng dẫn tái lập) + Mã kiểm thử Property 1 (Idempotence & String Utils)

---

## ✅ NHÓM VIỆC P1: PHÂN TÍCH STRING UTILS & HỖ TRỢ GIỮA KỲ
**Deadline: 18/10**

### P1.1 — Phân tích mã nguồn bộ tiền xử lý chuỗi
- [ ] P1.1.1 Đọc kỹ file `mealie/services/parser_services/parser_utils/string_utils.py`.
- [ ] P1.1.2 Phân tích hành vi của 3 hàm then chốt: `remove_footnote_markers`, `move_parens_to_end`, `convert_vulgar_fractions_to_regular_fractions`.
- [ ] P1.1.3 Lập danh sách các ca biên (Edge Cases): Phân số unicode đặc thù (`½`, `¼`, `¾`, `⅓`, `⅔`, `⅛`, `⅜`, `⅝`, `⅞`), chuỗi rỗng, chuỗi chỉ chứa ký tự xuống dòng, chuỗi có ngoặc lồng nhau `(a (b) c)`.
- [ ] P1.1.4 Hỗ trợ Nam xác thực Luồng 2 (Ingredient Parsing) và Luồng 3 (Servings Scaling) ở Giai đoạn 1 để kiểm tra chuỗi thực tế từ giao diện người dùng.
- [ ] P1.1.5 Tổng hợp ghi chú phân tích logic chuỗi gửi cho Hiếu đưa vào Đề cương kiểm thử giữa kỳ.
- [ ] P1.1.6 Commit: `docs: analyze string utils edge cases and parser pre-processing`.

---

## ✅ NHÓM VIỆC P2: THIẾT LẬP TEST HARNESS & CẤU HÌNH PYTEST / HYPOTHESIS
**Deadline: 15/11**

### P2.1 — Cấu hình file `pytest.ini`
- [ ] P2.1.1 Tạo hoặc cập nhật file `pytest.ini` chuẩn xác tại thư mục gốc kiểm thử:
  ```ini
  [pytest]
  addopts = -v --tb=short
  testpaths = tests
  filterwarnings =
      ignore::DeprecationWarning
  ```
- [ ] P2.1.2 Xác nhận `pytest` nhận diện đúng cấu hình qua lệnh: `pytest --version`.

### P2.2 — Xây dựng cấu hình Profile Hypothesis trong `tests/conftest.py`
- [ ] P2.2.1 Tạo file `tests/conftest.py` thiết lập 3 chế độ chạy (Profiles):
  ```python
  from hypothesis import settings, Verbosity

  # Profile chạy nhanh trong quá trình phát triển
  settings.register_profile("dev", max_examples=50, verbosity=Verbosity.normal)

  # Profile chạy tích hợp CI
  settings.register_profile("ci", max_examples=300, deadline=1000)

  # Profile chạy kiểm thử sâu toàn diện trước khi phát hành
  settings.register_profile("thorough", max_examples=1000, deadline=2000)

  # Mặc định sử dụng profile dev
  settings.load_profile("dev")
  ```
- [ ] P2.2.2 Cấu hình lưu trữ bộ nhớ đệm ca lỗi của Hypothesis (`.hypothesis/`) và bổ sung `.hypothesis/` vào `.gitignore`.
- [ ] P2.2.3 Kiểm tra khả năng nhận diện test runner: `pytest tests/ --collect-only` đảm bảo không có lỗi cú pháp hoặc import.
- [ ] P2.2.4 Commit: `chore: setup pytest harness and hypothesis multi-profile configuration`.

---

## ✅ NHÓM VIỆC P3: CODE TEST PBT — PROPERTY 1 (IDEMPOTENCE STRING UTILS)
**Deadline: 25/11**

### P3.1 — Tạo file và chuẩn bị môi trường test
- [ ] P3.1.1 Tạo file `tests/unit_tests/test_pbt_string_utils.py`.
- [ ] P3.1.2 Import các hàm từ `mealie.services.parser_services.parser_utils.string_utils`.

### P3.2 — Hiện thực kịch bản kiểm thử Property 1
- [ ] P3.2.1 Viết kiểm thử tính lũy đẳng (Idempotence) cho hàm `remove_footnote_markers`:
  ```python
  from hypothesis import given, strategies as st, settings
  from mealie.services.parser_services.parser_utils.string_utils import (
      remove_footnote_markers,
      move_parens_to_end,
      convert_vulgar_fractions_to_regular_fractions,
  )

  @given(st.text())
  @settings(max_examples=300)
  def test_remove_footnote_idempotent(s):
      once = remove_footnote_markers(s)
      twice = remove_footnote_markers(once)
      assert once == twice, f"Vi phạm tính lũy đẳng: input={s!r}, once={once!r}, twice={twice!r}"
  ```
- [ ] P3.2.2 Viết kiểm thử tính lũy đẳng cho hàm `move_parens_to_end`:
  ```python
  @given(st.text())
  @settings(max_examples=300)
  def test_move_parens_idempotent(s):
      once = move_parens_to_end(s)
      twice = move_parens_to_end(once)
      assert once == twice, f"Vi phạm di chuyển ngoặc: input={s!r}, once={once!r}, twice={twice!r}"
  ```
- [ ] P3.2.3 Viết kiểm thử tính bền vững (Crash-free) cho hàm chuyển đổi phân số `convert_vulgar_fractions_to_regular_fractions`:
  ```python
  @given(st.text())
  @settings(max_examples=300)
  def test_vulgar_fractions_never_crashes(s):
      result = convert_vulgar_fractions_to_regular_fractions(s)
      assert isinstance(result, str)
  ```
- [ ] P3.2.4 Viết kiểm thử tính triệt để: Xác nhận sau khi chuyển đổi, chuỗi không còn chứa bất kỳ ký tự phân số unicode nào:
  ```python
  VULGAR_CHARS = ["½", "¼", "¾", "⅓", "⅔", "⅛", "⅜", "⅝", "⅞"]

  @given(st.text())
  @settings(max_examples=300)
  def test_vulgar_chars_removed_completely(s):
      result = convert_vulgar_fractions_to_regular_fractions(s)
      for char in VULGAR_CHARS:
          assert char not in result, f"Ký tự phân số {char!r} vẫn còn sót trong chuỗi: {result!r}"
  ```
- [ ] P3.2.5 Chạy kiểm thử: `pytest tests/unit_tests/test_pbt_string_utils.py -v`.
- [ ] P3.2.6 Nếu phát hiện ca lỗi vi phạm (ví dụ regex xử lý ngoặc bị lặp vô hạn hoặc sót phân số), ghi lại counterexample vào `Documents/ket_qua_test.md` và chuyển giao cho **Mạnh**.
- [ ] P3.2.7 Commit: `feat(test): add PBT Property 1 string utils idempotence and completeness`.

---

## ✅ NHÓM VIỆC P4: BIÊN SOẠN HƯỚNG DẪN THỰC THI & TÁI LẬP (PHẦN F)
**Deadline: 30/11**

### P4.1 — Soạn thảo `Documents/bao_cao_phan_F.md` & `tests/README.md`
- [ ] P4.1.1 Tạo file `Documents/bao_cao_phan_F.md` và file `tests/README.md`.
- [ ] P4.1.2 Trình bày cấu trúc tổ chức mã nguồn kiểm thử (giải thích vai trò của từng file trong thư mục `tests/unit_tests/`).
- [ ] P4.1.3 Cung cấp lệnh thực thi 1-click duy nhất để chạy toàn bộ bộ kiểm thử tự động:
  ```bash
  pytest tests/unit_tests/test_pbt_*.py -v
  ```
- [ ] P4.1.4 Cung cấp lệnh thực thi tích hợp đo độ bao phủ mã nguồn (Code Coverage):
  ```bash
  pytest tests/unit_tests/test_pbt_*.py --cov=mealie/services/parser_services --cov-report=html:logs/coverage_html
  ```
- [ ] P4.1.5 Viết hướng dẫn giải thích các chỉ số hiển thị của Hypothesis: PASSED, FAILED, Falsifying example, Shrink trace.
- [ ] P4.1.6 Nhờ **Nam** hoặc **Hiếu** thực hiện chạy thử toàn bộ test theo hướng dẫn trên môi trường máy sạch để xác nhận tính tái lập (Reproducibility).
- [ ] P4.1.7 Hoàn thiện Phần F và bàn giao cho Trưởng nhóm Quân.
- [ ] P4.1.8 Commit: `docs: complete automated test harness documentation Phan F`.

---
---

# 👤 THÀNH VIÊN 5: VÕ HÙNG MẠNH
> **Vai trò:** QA Automation Engineer 2 & Defect Analyst  
> **Báo cáo phụ trách chính:** Phần G (Log thực thi, Đo Code Coverage, Phân tích lỗi Root Cause Analysis - RCA & Đề xuất bản vá) + Mã kiểm thử Property 3 (Crash-free Ingredient Parser)

---

## ✅ NHÓM VIỆC M1: PHÂN TÍCH ASYNC, CHUẨN BỊ MOCK FIXTURE & HỖ TRỢ GIỮA KỲ
**Deadline: 18/10**

### M1.1 — Phân tích kiến trúc Async của bộ Parser
- [ ] M1.1.1 Đọc mã nguồn `mealie/services/parser_services/ingredient_parser.py`.
- [ ] M1.1.2 Xác định phương thức then chốt: `BruteForceParser.parse_one(text)` là hàm bất đồng bộ (`async def`).
- [ ] M1.1.3 Xác định các tham số khởi tạo cần thiết của `BruteForceParser`: `session` (SQLAlchemy async session), `group_id`, `household_id`.

### M1.2 — Thiết lập môi trường và fixture Mock
- [ ] M1.2.1 Cài đặt các thư viện bổ trợ:
  ```bash
  pip install pytest-asyncio pytest-cov
  ```
- [ ] M1.2.2 Cập nhật file `pytest.ini` bổ sung chế độ chạy bất đồng bộ tự động:
  ```ini
  asyncio_mode = auto
  ```
- [ ] M1.2.3 Xây dựng mock fixture nhẹ nhàng trong `tests/conftest.py` sử dụng `unittest.mock.MagicMock` hoặc `AsyncMock` để cô lập logic parser không phụ thuộc vào database thực tế.
- [ ] M1.2.4 Đóng góp phần phân tích cơ chế Async và Mock vào Báo cáo giữa kỳ của Trưởng nhóm Quân.
- [ ] M1.2.5 Commit: `chore: setup async test runner and parser mock fixtures`.

---

## ✅ NHÓM VIỆC M2: CODE TEST PBT — PROPERTY 3 (CRASH-FREE INGREDIENT PARSER)
**Deadline: 25/11**

### M2.1 — Hiện thực kịch bản kiểm thử Property 3
- [ ] M2.1.1 Tạo file `tests/unit_tests/test_pbt_ingredient_parser.py`.
- [ ] M2.1.2 Viết test PBT kiểm tra tính bền bỉ / Bất khả sập (Crash-free Invariant) với mọi chuỗi Unicode ngẫu nhiên:
  ```python
  import pytest
  import asyncio
  from unittest.mock import MagicMock
  from hypothesis import given, strategies as st, settings
  from mealie.services.parser_services.ingredient_parser import BruteForceParser

  @given(st.text(max_size=500))
  @settings(max_examples=300)
  def test_ingredient_parser_never_crashes(text):
      """Property 3: Hàm parse_one không bao giờ được quăng Unhandled Exception"""
      try:
          mock_session = MagicMock()
          parser = BruteForceParser(session=mock_session, group_id=None, household_id=None)
          result = asyncio.run(parser.parse_one(text))
          assert result is not None
      except Exception as e:
          pytest.fail(f"CRASH phát hiện với input {text!r}\nException type: {type(e).__name__}: {e}")
  ```
- [ ] M2.1.3 Viết kiểm thử mở rộng với các tập dữ liệu biên đặc biệt: Chuỗi chỉ chứa số và ký tự toán học, chuỗi cực dài không chứa khoảng trắng, chuỗi chứa ký tự null byte `\x00` hoặc thẻ HTML/Markdown.
- [ ] M2.1.4 Chạy thử nghiệm: `pytest tests/unit_tests/test_pbt_ingredient_parser.py -v`.
- [ ] M2.1.5 Nếu phát hiện lỗi (Exception sập chương trình): Lưu vết ngay lập tức toàn bộ input tối giản (Falsifying example) và traceback vào file `Documents/ket_qua_test.md`.
- [ ] M2.1.6 Commit: `feat(test): add PBT Property 3 crash-free ingredient parser`.

---

## ✅ NHÓM VIỆC M3: THỰC THI TỔNG THỂ, THU THẬP LOG & ĐO LƯỜNG CODE COVERAGE
**Deadline: 05/12**

### M3.1 — Chạy toàn bộ bộ test và thu thập Log
- [ ] M3.1.1 Chạy toàn bộ 4 file test PBT ở mức kiểm thử cao nhất (`max_examples=500`):
  ```bash
  pytest tests/unit_tests/test_pbt_*.py -v --tb=long > logs/test_run_final.txt 2>&1
  ```
- [ ] M3.1.2 Xác nhận file `logs/test_run_final.txt` ghi lại chi tiết các ca test, thời gian thực thi và trạng thái hoàn thành.

### M3.2 — Đo lường độ bao phủ mã nguồn (Code Coverage)
- [ ] M3.2.1 Thực hiện lệnh đo Coverage tập trung vào module mục tiêu `parser_services`:
  ```bash
  pytest tests/unit_tests/test_pbt_*.py \
    --cov=mealie/services/parser_services \
    --cov-report=html:logs/coverage_html \
    --cov-report=term-missing > logs/coverage_summary.txt 2>&1
  ```
- [ ] M3.2.2 Mở báo cáo `logs/coverage_html/index.html` trên trình duyệt.
- [ ] M3.2.3 Chụp ảnh màn hình tổng quan tỷ lệ bao phủ của các file mục tiêu → lưu `Documents/assets/coverage_report.png`.
- [ ] M3.2.4 Lập bảng thống kê chi tiết tỷ lệ dòng lệnh được bao phủ (Line Coverage) và rẽ nhánh (Branch Coverage) của từng file: `ingredient_parser.py`, `string_utils.py`, `unit_utils.py`.
- [ ] M3.2.5 Commit: `test: execute comprehensive test suite, save execution logs and coverage artifacts`.

---

## ✅ NHÓM VIỆC M4: PHÂN TÍCH LỖI ROOT CAUSE ANALYSIS (RCA), ĐỀ XUẤT BẢN VÁ & SOẠN PHẦN G
**Deadline: 10/12**

### M4.1 — Soạn thảo `Documents/bao_cao_phan_G.md`
- [ ] M4.1.1 Tạo file `Documents/bao_cao_phan_G.md`.
- [ ] M4.1.2 Trình bày bảng tổng kết số liệu thực nghiệm: Tổng số test cases được sinh ra bởi Hypothesis, số ca Passed/Failed, bảng số liệu Coverage.

### M4.2 — Phân tích nguyên nhân gốc rễ (RCA) cho từng lỗi phát hiện được
- [ ] M4.2.1 Trích xuất thông tin Falsifying Example từ log của Hypothesis.
- [ ] M4.2.2 Tái hiện lỗi độc lập trong môi trường Python tối giản và lưu traceback đầy đủ.
- [ ] M4.2.3 Đọc traceback từ dưới lên để xác định chính xác tên file và số dòng code trong Mealie bị sập.
- [ ] M4.2.4 Phân loại và giải thích nguyên nhân cốt lõi (Lỗi chia cho 0, lỗi ép kiểu dữ liệu chuỗi sang số, lỗi regex backtracking khi gặp chuỗi unicode đặc biệt,...).
- [ ] M4.2.5 Soạn thảo đề xuất bản vá (Patch Proposal) dưới dạng mã diff hoặc đoạn code chuẩn chỉnh theo nguyên tắc Ponytail (sửa tại gốc, không sửa tạm bợ).
- [ ] M4.2.6 Trình bày phân tích theo cấu trúc chuẩn trong `bao_cao_phan_G.md`:
  ```markdown
  ### LỖI PHÁT HIỆN #1: [Tên ngắn gọn]
  - **Property vi phạm:** Property 3 (Tính bền bỉ) / Property 1...
  - **Phản ví dụ tối giản (Falsifying Example):** `text = "..."`
  - **Loại ngoại lệ (Exception):** `AttributeError` / `ZeroDivisionError`...
  - **Vị trí phát sinh:** `mealie/services/parser_services/ingredient_parser.py:dòng_xyz`
  - **Nguyên nhân gốc rễ (Root Cause):** [Giải thích tường tận]
  - **Đề xuất bản vá (Patch Proposal):**
    ```diff
    - code_cu()
    + code_moi_da_kiem_tra_dieu_kien()
    ```
  ```
- [ ] M4.2.7 *(Trường hợp không phát sinh bug):* Phân tích lý do hệ thống hoạt động ổn định, chứng minh qua độ bao phủ kiểm thử cao ($\ge 80\%$) và khả năng chống chịu của các bộ try-catch có sẵn trong Mealie.
- [ ] M4.2.8 Hoàn thiện toàn bộ Phần G và bàn giao cho Trưởng nhóm Quân để tích hợp vào báo cáo tổng kết cuối kỳ.
- [ ] M4.2.9 Commit: `docs: complete test results, defect root cause analysis and patch proposals Phan G`.

---
---

# 🔍 CHECKLIST NGHIỆM THU CUỐI KỲ (Toàn nhóm tự kiểm tra trước khi nộp)

## Mốc Giữa kỳ — 20/10
- [ ] Mealie chạy thành công demo trực tiếp trên máy (Nam xác nhận).
- [ ] Đủ 6 ảnh chụp bằng chứng 3 luồng nghiệp vụ cốt lõi (Nam & Phước nghiệm thu).
- [ ] Tài liệu On-boarding `Documents/bao_cao_phan_C.md` chi tiết, đã được Hiếu cài đặt thẩm định thành công từ máy sạch độc lập.
- [ ] Sơ đồ kiến trúc tổng thể và Data Flow đầy đủ trong `Documents/bao_cao_phan_B.md` (Quân hoàn thành).
- [ ] Đề cương kế hoạch kiểm thử PBT rõ phạm vi và giả định kỹ thuật (Hiếu & Quân hoàn thành).
- [ ] Cấu hình async/mock cơ bản cho bộ parser sẵn sàng (Mạnh hoàn thành).
- [ ] **Cả 5 thành viên đều có ít nhất 1–2 commit Git hợp lệ trong Sprint 1 & 2.**

## Mốc Cuối kỳ — Tháng 12
- [ ] Cuốn báo cáo hoàn chỉnh đầy đủ 8 phần từ A đến H không thiếu mục nào (Quân tổng hợp).
- [ ] Toàn bộ 4 file test PBT chạy tự động trơn tru bằng 1 lệnh duy nhất (`pytest tests/unit_tests/test_pbt_*.py -v`).
- [ ] Test Runner biệt lập qua Docker chạy thành công trên mọi máy tính (Nam hoàn thành).
- [ ] Đã chỉ ra được ít nhất 1 lỗi thực tế kèm phân tích RCA và đề xuất bản vá HOẶC chứng minh Coverage đạt chuẩn $\ge 80\%$ (Mạnh hoàn thành).
- [ ] `tests/README.md` đã được kiểm thử chéo và tái lập thành công từ máy sạch độc lập (Phước & Hiếu xác nhận).
- [ ] Lịch sử Git thể hiện sự đóng góp tích cực, đều đặn của **cả 5 thành viên** xuyên suốt từ Sprint 1 đến Sprint 5.
- [ ] Đã ghim Commit SHA và gắn Git Tag `v1.0-final` vào repo nhóm (Quân hoàn thành).
- [ ] Slide bảo vệ chuẩn bị chỉn chu, phân vai thuyết trình rành mạch cho từng thành viên.
