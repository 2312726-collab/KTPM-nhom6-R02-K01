# BẢNG PHÂN CÔNG NHIỆM VỤ NGUYÊN TỬ — NHÓM 6
**Đề tài:** Mealie (R02) + Property-Based Testing với Hypothesis (K01)  
**Môn:** Kiểm thử phần mềm | **GVHD:** Nguyễn Thế Lâm  
**Kho lưu trữ GitHub:** [https://github.com/2312726-collab/KTPM-nhom6-R02-K01](https://github.com/2312726-collab/KTPM-nhom6-R02-K01)

---

> **Quy ước chung:**
> - Mỗi ô checkbox `[ ]` = 1 bước công việc độc lập, kiểm tra được ngay.
> - Mỗi nhóm bước lớn = 1 `git commit` riêng biệt.
> - Commit message chuẩn: `feat(test):`, `docs:`, `chore:`, `fix(test):`, `test:`.
> - **Nguyên tắc phân công cân bằng 5 thành viên:**
>   - **Trưởng nhóm Trần Quốc Quân** giữ vai trò kiến trúc sư chủ chốt: khởi tạo dự án ban đầu, định hình kiến trúc (Phần A, B), trực tiếp lập trình mã kiểm thử PBT (Property 4) và đóng gói nghiệm thu cuối kỳ (Phần H, Slide).
>   - **Cả 5 thành viên** đều có trách nhiệm rõ ràng ở cả 2 giai đoạn (Giữa kỳ và Cuối kỳ), mỗi người chủ biên 1 phần báo cáo lớn và trực tiếp tự tay lập trình đúng 1 kịch bản kiểm thử PBT độc lập (đảm bảo 100% thành viên đều có commit code test trên Git).

---
---

# 👤 THÀNH VIÊN 1: TRẦN QUỐC QUÂN
> **Vai trò:** Trưởng nhóm — Quản trị dự án, Kiến trúc sư hệ thống & Lập trình kiểm thử Property 4  
> **Báo cáo phụ trách chính:** Phần A, Phần B, Phần H + Slide thuyết trình  
> **Kịch bản Code PBT trực tiếp:** **Property 4 (Servings Scaling Monotonicity & Reversibility)** trong `tests/unit_tests/test_pbt_scaling.py`

---

## ✅ NHÓM VIỆC Q1: KHỞI TẠO NỀN TẢNG DỰ ÁN & THIẾT LẬP GIT
**Deadline: 30/9** *(Đã hoàn thành)*

### Q1.1 — Khởi tạo kho lưu trữ GitHub của nhóm
- [x] Q1.1.1 Tạo repository trên GitHub: `https://github.com/2312726-collab/KTPM-nhom6-R02-K01.git`.
- [x] Q1.1.2 Thiết lập file `README.md` ban đầu: Thông tin nhóm, đề tài Mealie + Hypothesis, bảng phân vai 5 thành viên.
- [x] Q1.1.3 Tạo file `.gitignore` chặn các thư mục môi trường và file tạm (`.venv`, `__pycache__`, `mealie-data`, `logs/`).
- [ ] Q1.1.4 Mời 4 thành viên vào repo (Settings → Collaborators → Add people) và xác nhận cả 4 bạn đã Accept.

### Q1.2 — Thiết lập quy tắc nhánh & Quy chuẩn phối hợp
- [x] Q1.2.1 Tạo nhánh `develop` từ `main` và đẩy cả 2 nhánh lên GitHub.
- [ ] Q1.2.2 Cấu hình bảo vệ nhánh `main`: Settings → Branches → Add classic branch protection rule → tick *"Require a pull request before merging"*.
- [x] Q1.2.3 Thống nhất quy chuẩn commit Tiếng Việt trong `Documents/quy_tac_du_an.md` và `README.md` (`thêm:`, `sửa:`, `cấu hình:`, `dọn dẹp:`).
- [ ] Q1.2.4 Phổ biến quy trình làm việc 4 bước (tạo nhánh `feat/*` từ `develop`, commit, push, tạo PR) cho các thành viên.

### Q1.3 — Cố định phiên bản Mealie (Pin Version)
- [x] Q1.3.1 Tạo file `Documents/mealie_version.md` ghim cố định: Release Tag **`v3.28.0`** và Commit SHA **`0552eaa4a80031b8572849cca0ed95d07f1be001`**.
- [x] Q1.3.2 Xác minh tag tồn tại trên repo chính thức của Mealie.
- [x] Q1.3.3 Tạo initial commit đứng tên tác giả Trưởng nhóm trên nhánh `main` và `develop`.

### Q1.4 — Thiết lập bảng Kanban theo dõi tiến độ
- [ ] Q1.4.1 Tạo GitHub Projects Board (Board view: Todo | In Progress | Review | Done).
- [ ] Q1.4.2 Tạo các Issues tương ứng cho 5 thành viên (Q1→Q4, N1→N4, H1→H4, P1→P4, M1→M4) và gán assignee.
- [ ] Q1.4.3 Điều phối cuộc họp nhóm ngắn 15 phút đầu tuần để kiểm tra tiến độ thẻ.

---

## ✅ NHÓM VIỆC Q2: PHÂN TÍCH KIẾN TRÚC HỆ THỐNG MEALIE (PHẦN A & B)
**Deadline: 18/10** | Đầu ra: `Documents/bao_cao_phan_A.md` + `Documents/bao_cao_phan_B.md`

### Q2.1 — Khảo sát cấu trúc mã nguồn Mealie
- [x] Q2.1.1 Clone Mealie đúng tag `v3.28.0` về máy cá nhân:
  ```bash
  git clone --branch v3.28.0 --depth 1 https://github.com/mealie-recipes/mealie.git mealie_src
  ```
- [ ] Q2.1.2 Đọc các file cấu trúc chính: `mealie/app.py`, `mealie/main.py`, `mealie/routes/`, `pyproject.toml`.

### Q2.2 — Soạn thảo Phần A: Mô tả hệ thống (`Documents/bao_cao_phan_A.md`)
- [ ] Q2.2.1 Viết mục tiêu hệ thống Mealie, các Actor chính (**Home User**, **Admin**) và 5 Use Case cốt lõi.
- [ ] Q2.2.2 Mô tả cây thư mục tổng thể của Mealie, tập trung vào `mealie/services/parser_services/`.
- [ ] Q2.2.3 Commit: `docs: add system description Phan A`.

### Q2.3 — Soạn thảo Phần B: Kiến trúc & Luồng dữ liệu (`Documents/bao_cao_phan_B.md`)
- [ ] Q2.3.1 Vẽ sơ đồ kiến trúc tổng thể C4 Container (`Browser → Vue Frontend → FastAPI Backend → SQLite`) lưu ảnh vào `Documents/assets/kien_truc_container.png`.
- [ ] Q2.3.2 Vẽ Data Flow 1: Nghiệp vụ bóc tách nguyên liệu (Ingredient Parsing).
- [ ] Q2.3.3 Vẽ Data Flow 2: Nghiệp vụ nhân chia tỉ lệ khẩu phần ăn (Servings Scaling).
- [ ] Q2.3.4 Vẽ Data Flow 3: Nghiệp vụ lên lịch thực đơn (Meal Planning).
- [ ] Q2.3.5 Phân tích chi tiết 3 module trọng tâm liên quan trực tiếp đến kiểm thử: `ingredient_parser.py`, `string_utils.py`, `unit_utils.py`.
- [ ] Q2.3.6 Commit: `docs: add architecture diagrams and data flows Phan B`.

---

## ✅ NHÓM VIỆC Q3: LẬP TRÌNH KIỂM THỬ PBT — PROPERTY 4 (SERVINGS SCALING)
**Deadline: 25/11** | File code: `tests/unit_tests/test_pbt_scaling.py`

### Q3.1 — Nghiên cứu thuật toán Scaling trong Mealie
- [ ] Q3.1.1 Đọc hàm scale khẩu phần trong `mealie/services/recipe/recipe_service.py` và schema `mealie/schema/recipe/recipe_ingredient.py`.
- [ ] Q3.1.2 Xác định Invariant toán học:
  - *Tính đơn điệu (Monotonicity):* Với số lượng $Q > 0$, nếu tỉ lệ $k > 1$ thì $Q \times k > Q$; nếu $k < 1$ thì $Q \times k < Q$.
  - *Tính bảo toàn nghịch đảo (Reversibility):* $(Q \times k) / k \approx Q$ với sai số dấu phẩy động $\epsilon \le 10^{-4}$.

### Q3.2 — Viết mã kiểm thử tự động PBT Property 4
- [ ] Q3.2.1 Tạo nhánh `feat/quan-property-4-scaling` từ `develop`.
- [ ] Q3.2.2 Tạo file `tests/unit_tests/test_pbt_scaling.py`.
- [ ] Q3.2.3 Viết test tính đơn điệu khi nhân khẩu phần:
  ```python
  from hypothesis import given, strategies as st, assume, settings

  @given(
      qty=st.floats(min_value=0.01, max_value=1000, allow_nan=False, allow_infinity=False),
      scale=st.floats(min_value=0.1, max_value=10.0, allow_nan=False, allow_infinity=False)
  )
  @settings(max_examples=300)
  def test_servings_scaling_monotonicity(qty, scale):
      assume(scale > 0 and qty > 0)
      scaled = qty * scale
      if scale > 1.0:
          assert scaled > qty, f"Scale {scale} > 1 nhưng {scaled} <= {qty}"
      elif scale < 1.0:
          assert scaled < qty, f"Scale {scale} < 1 nhưng {scaled} >= {qty}"
  ```
- [ ] Q3.2.4 Viết test tính bảo toàn nghịch đảo khi scale:
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
      assert abs(reverted - qty) < 1e-4, f"Sai lệch nghịch đảo: gốc={qty}, phục hồi={reverted}"
  ```
- [ ] Q3.2.5 Chạy kiểm thử: `pytest tests/unit_tests/test_pbt_scaling.py -v`.
- [ ] Q3.2.6 Commit & tạo Pull Request vào `develop`: `feat(test): add PBT Property 4 servings scaling monotonicity`.

---

## ✅ NHÓM VIỆC Q4: TỔNG HỢP BÁO CÁO, PHẦN H & SLIDE BẢO VỆ
**Deadline: 19/10 (Giữa kỳ) | 12/12 (Cuối kỳ)**

### Q4.1 — Tổng hợp Báo cáo Giữa kỳ (20/10)
- [ ] Q4.1.1 Thu nhận `bao_cao_phan_C.md` từ **Nam** và Đề cương kiểm thử từ **Hiếu**.
- [ ] Q4.1.2 Biên tập file `Documents/bao_cao_giua_ky.md`.
- [ ] Q4.1.3 Soạn Slide báo cáo Giữa kỳ (tối thiểu 12 slides).

### Q4.2 — Tổng hợp Báo cáo Cuối kỳ, Phần H & Điều phối Bảo vệ (Tháng 12)
- [ ] Q4.2.1 Thu nhận Phần D & E từ **Hiếu**, Phần F từ **Phước**, Phần G từ **Mạnh**.
- [ ] Q4.2.2 Biên tập cuốn Báo cáo Cuối kỳ hoàn chỉnh 8 phần từ A đến H.
- [ ] Q4.2.3 Soạn thảo Phần H: Lưu trữ commit SHA, gắn Git Tag `v1.0-final`, hướng dẫn nghiệm thu tái lập.
- [ ] Q4.2.4 Gắn Git Tag chính thức: `git tag v1.0-final && git push origin v1.0-final`.
- [ ] Q4.2.5 Soạn Slide bảo vệ cuối kỳ, phân vai thuyết trình và kịch bản demo live script kiểm thử.

---
---

# 👤 THÀNH VIÊN 2: NGUYỄN PHẠM PHÚ NAM
> **Vai trò:** DevOps & Automation QA — Môi trường Docker, Seed Data & Lập trình kiểm thử Property 5  
> **Báo cáo phụ trách chính:** Phần C (Tài liệu On-boarding & Bằng chứng hệ thống) + Dockerized Test Runner  
> **Kịch bản Code PBT trực tiếp:** **Property 5 (Fraction Normalization & Numeric Preservation)** trong `tests/unit_tests/test_pbt_fraction.py`

---

## ✅ NHÓM VIỆC N1: THIẾT LẬP MÔI TRƯỜNG DOCKER MEALIE
**Deadline: 15/10**

### N1.1 — Dựng Mealie bằng Docker Compose
- [x] N1.1.1 Tạo thư mục `mealie_docker/` trong repo.
- [x] N1.1.2 Tạo file `mealie_docker/docker-compose.yml` (phiên bản SQLite chuẩn) và `mealie_docker/.env` mở cổng `9925`.
- [x] N1.1.3 Chạy container: `docker-compose up -d`.
- [x] N1.1.4 Kiểm tra log: `docker-compose logs -f mealie` xác nhận FastAPI khởi động mượt mà.
- [x] N1.1.5 Truy cập `http://localhost:9925`, chụp ảnh Landing Page → lưu `Documents/assets/01_mealie_landing.png`.

### N1.2 — Đăng ký tài khoản Admin & Xác nhận Dashboard
- [x] N1.2.1 Đăng ký tài khoản Admin (`admin@nhom6.test` / `Admin123@`).
- [x] N1.2.2 Đăng nhập Dashboard thành công, chụp ảnh Dashboard → lưu `Documents/assets/02_mealie_dashboard.png`.
- [x] N1.2.3 Commit: `chore: setup docker-compose environment and initial admin credentials`.

---

## ✅ NHÓM VIỆC N2: CHUẨN BỊ SEED DATA & THỰC THI 3 LUỒNG NGHIỆP VỤ
**Deadline: 17/10**

### N2.1 — Nạp dữ liệu mẫu (Seed Data)
- [x] N2.1.1 Tạo tài khoản kiểm thử thường (`test@nhom6.test` / `User123@`).
- [x] N2.1.2 Tạo 10 công thức mẫu đa dạng (nguyên liệu đơn giản, phân số thường, phân số unicode `½`, chú thích trong ngoặc, công thức dài nhiều bước).
- [x] N2.1.3 Tạo kế hoạch thực đơn (Meal Plan) 7 ngày tuần 06/10–12/10, chụp ảnh → lưu `Documents/assets/03_meal_plan.png`.

### N2.2 — Thu thập bằng chứng 3 luồng nghiệp vụ cốt lõi
- [x] N2.2.1 Luồng 1 — Import công thức từ URL: Chụp ảnh công thức đã import → lưu `04_recipe_import.png`.
- [x] N2.2.2 Luồng 2 — Phân tích nguyên liệu (Ingredient Parsing): Nhập chuỗi bóc tách Qty, Unit, Food, Note → chụp `05_ingredient_parse.png`.
- [x] N2.2.3 Luồng 3 — Nhân tỉ lệ khẩu phần ăn (Servings Scaling): Đổi 4 thành 8 servings, kiểm tra nhân đôi → chụp `06_servings_scale.png`.
- [x] N2.2.4 Commit: `docs: seed test recipes and capture evidence for 3 core business flows`.

---

## ✅ NHÓM VIỆC N3: SOẠN THẢO TÀI LIỆU ON-BOARDING (PHẦN C)
**Deadline: 18/10**

### N3.1 — Soạn thảo `Documents/bao_cao_phan_C.md`
- [x] N3.1.1 Soạn thảo đầy đủ 5 mục chuẩn: C.1 Yêu cầu môi trường, C.2 Các bước cài đặt chi tiết, C.3 Quản lý dịch vụ docker, C.4 Hướng dẫn nạp Seed Data, C.5 Xử lý sự cố (xung đột port 9925, cấp quyền thư mục).
- [x] N3.1.2 Nhúng toàn bộ 6 ảnh minh chứng vào đúng vị trí trong báo cáo.
- [ ] N3.1.3 Bàn giao cho **Hiếu** cài đặt thẩm định chéo trên máy sạch, tiếp thu góp ý để hoàn thiện.
- [x] N3.1.4 Commit: `docs: complete onboarding guide Phan C with verified evidence`.

---

## ✅ NHÓM VIỆC N4: LẬP TRÌNH KIỂM THỬ PBT — PROPERTY 5 (FRACTION NORMALIZATION)
**Deadline: 25/11** | File code: `tests/unit_tests/test_pbt_fraction.py`

### N4.1 — Nghiên cứu logic xử lý phân số trong Mealie
- [x] N4.1.1 Đọc hàm chuẩn hóa phân số trong `mealie/services/parser_services/parser_utils/string_utils.py`.
- [x] N4.1.2 Xác định Invariant: Khi phân số dạng chuỗi (ví dụ `"1/2"`, `"3/4"`, hỗn số `"2 1/2"`) được bóc tách sang số thực, giá trị toán học phải được bảo toàn chính xác trong sai số $\epsilon \le 10^{-4}$.

### N4.2 — Viết mã kiểm thử tự động PBT Property 5
- [x] N4.2.1 Tạo nhánh riêng `2312695-NguyenPhamPhuNam-N4-Property5` (và nhánh lưu trữ `feat/nam-property-5-fraction`) từ `develop`.
- [x] N4.2.2 Tạo file `tests/unit_tests/test_pbt_fraction.py`.
- [x] N4.2.3 Viết kiểm thử bảo toàn giá trị toán học cho phân số:
  ```python
  from hypothesis import given, strategies as st, assume, settings
  from fractions import Fraction
  from mealie.services.parser_services.parser_utils.string_utils import convert_vulgar_fractions_to_regular_fractions

  @given(
      numerator=st.integers(min_value=1, max_value=99),
      denominator=st.integers(min_value=1, max_value=99)
  )
  @settings(max_examples=300)
  def test_fraction_numeric_preservation(numerator, denominator):
      assume(denominator != 0)
      fraction_str = f"{numerator}/{denominator}"
      expected_val = numerator / denominator
      parsed_val = float(Fraction(fraction_str))
      assert abs(parsed_val - expected_val) < 1e-6
  ```
- [x] N4.2.4 Đóng gói container chạy test độc lập: Tạo file `docker-compose.test.yml` để chạy toàn bộ suite test bên trong Docker.
- [x] N4.2.5 Chạy kiểm thử: `pytest tests/unit_tests/test_pbt_fraction.py -v` — **23 passed, 0 failed** trên cả host (Python 3.14.7, 0.79s) và Docker container độc lập (`ktpm_nhom6_test_runner`, Linux Python 3.14.8, exit code 0, 1.61s).
- [x] N4.2.6 Commit & tạo Pull Request vào `develop`: `feat(test): add PBT Property 5 fraction normalization and docker runner` — PR #1: https://github.com/2312726-collab/KTPM-nhom6-R02-K01/pull/1.

---
---

# 👤 THÀNH VIÊN 3: BÙI TRUNG HIẾU
> **Vai trò:** Test Architect & PBT Methodology Specialist  
> **Báo cáo phụ trách chính:** Phần D (Cơ sở lý thuyết PBT) + Phần E (Thiết kế kịch bản kiểm thử)  
> **Kịch bản Code PBT trực tiếp:** **Property 2 (Unit Conversion Round-trip)** trong `tests/unit_tests/test_pbt_unit_converter.py`

---

## ✅ NHÓM VIỆC H1: KHẢO SÁT MODULE, ĐỀ CƯƠNG GIỮA KỲ & THẨM ĐỊNH PHẦN C
**Deadline: 18/10**

### H1.1 — Khảo sát module mục tiêu & Lập đề cương kiểm thử
- [ ] H1.1.1 Đọc cấu trúc module `mealie/services/parser_services/`.
- [ ] H1.1.2 Xác định phạm vi kiểm thử: 3 file cốt lõi (`ingredient_parser.py`, `string_utils.py`, `unit_utils.py`).
- [ ] H1.1.3 Soạn thảo đề cương kế hoạch kiểm thử PBT sơ bộ nộp Trưởng nhóm Quân đưa vào Báo cáo Giữa kỳ.

### H1.2 — Thẩm định chéo (Cross-validation) tài liệu On-boarding
- [ ] H1.2.1 Tiếp nhận `bao_cao_phan_C.md` từ **Nam**.
- [ ] H1.2.2 Cài đặt thử nghiệm Mealie từ đầu trên máy cá nhân theo đúng từng dòng lệnh trong tài liệu.
- [ ] H1.2.3 Lập biên bản phản hồi (lỗi phát sinh, lệnh còn thiếu) gửi lại Nam cập nhật.
- [ ] H1.2.4 Commit: `docs: outline midterm PBT test strategy and cross-validate onboarding`.

---

## ✅ NHÓM VIỆC H2: NGHIÊN CỨU LÝ THUYẾT HYPOTHESIS & SOẠN PHẦN D
**Deadline: 30/10**

### H2.1 — Nghiên cứu tài liệu chính thức Hypothesis
- [ ] H2.1.1 Đọc Hypothesis Quickstart & Strategies Reference: `@given`, `strategies`, `assume()`, `@settings`.
- [ ] H2.1.2 Đọc cơ chế Shrinking: Hiểu cách Hypothesis tự động thu nhỏ phản ví dụ gây lỗi về dạng ngắn nhất.

### H2.2 — Soạn thảo `Documents/bao_cao_phan_D.md`
- [ ] H2.2.1 Viết Mục D.1: Bản chất của PBT và bảng so sánh chi tiết giữa Example-Based Testing và PBT.
- [ ] H2.2.2 Viết Mục D.2: Sơ đồ hóa 4 bước vận hành của Hypothesis (Generate → Check Invariant → Shrink → Report).
- [ ] H2.2.3 Viết Mục D.3 & D.4: Lý do chọn `parser_services` và ranh giới kiểm thử theo triết lý Ponytail.
- [ ] H2.2.4 Viết Mục D.5, D.6 & D.7: Giả định kỹ thuật, tiêu chí Pass/Fail và quản lý rủi ro Flaky test.
- [ ] H2.2.5 Commit: `docs: complete theoretical foundation and test methodology Phan D`.

---

## ✅ NHÓM VIỆC H3: THIẾT KẾ KỊCH BẢN KIỂM THỬ CHI TIẾT (PHẦN E)
**Deadline: 10/11**

### H3.1 — Soạn thảo `Documents/bao_cao_phan_E.md`
- [ ] H3.1.1 Thiết kế bảng đặc tả chuẩn hóa cho **Property 1 — Tính lũy đẳng (Idempotence)** (Phước code).
- [ ] H3.1.2 Thiết kế bảng đặc tả chuẩn hóa cho **Property 2 — Tính bảo toàn hai chiều (Round-trip)** (Hiếu code).
- [ ] H3.1.3 Thiết kế bảng đặc tả chuẩn hóa cho **Property 3 — Tính bền bỉ / Crash-free** (Mạnh code).
- [ ] H3.1.4 Thiết kế bảng đặc tả chuẩn hóa cho **Property 4 — Tính đơn điệu khi Scaling** (Quân code).
- [ ] H3.1.5 Thiết kế bảng đặc tả chuẩn hóa cho **Property 5 — Tính bảo toàn phân số** (Nam code).
- [ ] H3.1.6 Bàn giao tài liệu Phần E cho cả nhóm làm căn cứ viết code test.
- [ ] H3.1.7 Commit: `docs: design standardized PBT test scenarios for all 5 properties Phan E`.

---

## ✅ NHÓM VIỆC H4: LẬP TRÌNH KIỂM THỬ PBT — PROPERTY 2 (UNIT CONVERSION ROUND-TRIP)
**Deadline: 25/11** | File code: `tests/unit_tests/test_pbt_unit_converter.py`

### H4.1 — Nghiên cứu mã nguồn UnitConverter
- [ ] H4.1.1 Đọc class `UnitConverter` trong `mealie/services/parser_services/parser_utils/unit_utils.py`.
- [ ] H4.1.2 Xác định bảng danh mục các đơn vị đo lường (khối lượng: gram, kg; thể tích: ml, liter, tsp, tbsp).

### H4.2 — Viết mã kiểm thử tự động PBT Property 2
- [ ] H4.2.1 Tạo nhánh `feat/hieu-property-2-converter` từ `develop`.
- [ ] H4.2.2 Tạo file `tests/unit_tests/test_pbt_unit_converter.py`.
- [ ] H4.2.3 Viết kiểm thử Round-trip khối lượng (`gram` $\leftrightarrow$ `kilogram`):
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
- [ ] H4.2.4 Viết kiểm thử Round-trip thể tích (`milliliter` $\leftrightarrow$ `liter`, `teaspoon` $\leftrightarrow$ `tablespoon`).
- [ ] H4.2.5 Viết kiểm thử xác nhận Exception có kiểm soát khi đổi giữa hai đơn vị không tương thích.
- [ ] H4.2.6 Chạy kiểm thử: `pytest tests/unit_tests/test_pbt_unit_converter.py -v`.
- [ ] H4.2.7 Commit & tạo Pull Request vào `develop`: `feat(test): add PBT Property 2 unit conversion round-trip`.

---
---

# 👤 THÀNH VIÊN 4: TRẦN NGỌC BẢO PHƯỚC
> **Vai trò:** QA Automation Engineer 1 — Test Harness & String Engine Verification  
> **Báo cáo phụ trách chính:** Phần F (Bộ kiểm thử tự động, cấu hình Test Harness & Hướng dẫn tái lập)  
> **Kịch bản Code PBT trực tiếp:** **Property 1 (Idempotence & String Utils)** trong `tests/unit_tests/test_pbt_string_utils.py`

---

## ✅ NHÓM VIỆC P1: PHÂN TÍCH STRING UTILS & HỖ TRỢ GIỮA KỲ
**Deadline: 18/10**

### P1.1 — Phân tích mã nguồn bộ tiền xử lý chuỗi
- [ ] P1.1.1 Đọc file `mealie/services/parser_services/parser_utils/string_utils.py`.
- [ ] P1.1.2 Phân tích hành vi 3 hàm: `remove_footnote_markers`, `move_parens_to_end`, `convert_vulgar_fractions_to_regular_fractions`.
- [ ] P1.1.3 Lập danh mục các ca biên (Edge Cases): phân số unicode (`½`, `¼`, `¾...`), chuỗi rỗng, chuỗi chỉ chứa dấu cách, ngoặc lồng nhau.
- [ ] P1.1.4 Hỗ trợ Nam xác thực Luồng 2 (Ingredient Parsing) và Luồng 3 (Servings Scaling) ở Giai đoạn 1.
- [ ] P1.1.5 Commit: `docs: analyze string utils edge cases and parser pre-processing`.

---

## ✅ NHÓM VIỆC P2: THIẾT LẬP TEST HARNESS & CẤU HÌNH PYTEST / HYPOTHESIS
**Deadline: 15/11**

### P2.1 — Cấu hình file `pytest.ini` & Profiles trong `tests/conftest.py`
- [ ] P2.1.1 Cấu hình file `pytest.ini` chuẩn xác (`testpaths = tests`, `-v --tb=short`).
- [ ] P2.1.2 Xây dựng 3 profiles trong `tests/conftest.py`:
  - Profile `dev`: `max_examples=50` (chạy nhanh khi code).
  - Profile `ci`: `max_examples=300` (chạy CI).
  - Profile `thorough`: `max_examples=1000` (chạy sâu kiểm tra sức bền).
- [ ] P2.1.3 Cấu hình cache `.hypothesis/` và bổ sung vào `.gitignore`.
- [ ] P2.1.4 Kiểm tra nhận diện test runner: `pytest tests/ --collect-only`.
- [ ] P2.1.5 Commit: `chore: setup pytest harness and hypothesis multi-profile configuration`.

---

## ✅ NHÓM VIỆC P3: LẬP TRÌNH KIỂM THỬ PBT — PROPERTY 1 (IDEMPOTENCE STRING UTILS)
**Deadline: 25/11** | File code: `tests/unit_tests/test_pbt_string_utils.py`

### P3.1 — Hiện thực kịch bản kiểm thử Property 1
- [ ] P3.1.1 Tạo nhánh `feat/phuoc-property-1-stringutils` từ `develop`.
- [ ] P3.1.2 Tạo file `tests/unit_tests/test_pbt_string_utils.py`.
- [ ] P3.1.3 Viết test tính lũy đẳng (Idempotence) cho hàm `remove_footnote_markers`:
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
      assert once == twice, f"Vi phạm lũy đẳng: input={s!r}, once={once!r}, twice={twice!r}"
  ```
- [ ] P3.1.4 Viết test tính lũy đẳng cho hàm `move_parens_to_end`:
  ```python
  @given(st.text())
  @settings(max_examples=300)
  def test_move_parens_idempotent(s):
      once = move_parens_to_end(s)
      twice = move_parens_to_end(once)
      assert once == twice, f"Vi phạm di chuyển ngoặc: input={s!r}, once={once!r}, twice={twice!r}"
  ```
- [ ] P3.1.5 Viết test tính bền bỉ Crash-free cho `convert_vulgar_fractions_to_regular_fractions` với mọi `st.text()`.
- [ ] P3.1.6 Viết test xác nhận không còn ký tự phân số unicode (`½, ¼, ¾, ⅓, ⅔...`) sau khi chuyển đổi.
- [ ] P3.1.7 Chạy kiểm thử: `pytest tests/unit_tests/test_pbt_string_utils.py -v`.
- [ ] P3.1.8 Commit & tạo Pull Request vào `develop`: `feat(test): add PBT Property 1 string utils idempotence and completeness`.

---

## ✅ NHÓM VIỆC P4: BIÊN SOẠN HƯỚNG DẪN THỰC THI & TÁI LẬP (PHẦN F)
**Deadline: 30/11**

### P4.1 — Soạn thảo `Documents/bao_cao_phan_F.md` & `tests/README.md`
- [ ] P4.1.1 Trình bày cấu trúc toàn bộ suite test và vai trò của từng file test trong repo.
- [ ] P4.1.2 Cung cấp lệnh chạy test 1-click duy nhất: `pytest tests/unit_tests/test_pbt_*.py -v`.
- [ ] P4.1.3 Cung cấp lệnh chạy tích hợp đo độ bao phủ mã nguồn với `pytest-cov`.
- [ ] P4.1.4 Giải thích định dạng kết quả của Hypothesis (PASSED, Falsifying example, Shrink trace).
- [ ] P4.1.5 Mời Nam hoặc Hiếu chạy thử nghiệm từ máy sạch để xác nhận tính tái lập (Reproducibility).
- [ ] P4.1.6 Commit: `docs: complete automated test harness documentation Phan F`.

---
---

# 👤 THÀNH VIÊN 5: VÕ HÙNG MẠNH
> **Vai trò:** QA Automation Engineer 2 & Defect Analyst  
> **Báo cáo phụ trách chính:** Phần G (Log thực thi, Đo Code Coverage, Phân tích lỗi Root Cause Analysis - RCA & Đề xuất bản vá)  
> **Kịch bản Code PBT trực tiếp:** **Property 3 (Crash-free Ingredient Parser)** trong `tests/unit_tests/test_pbt_ingredient_parser.py`

---

## ✅ NHÓM VIỆC M1: PHÂN TÍCH ASYNC, CHUẨN BỊ MOCK FIXTURE & HỖ TRỢ GIỮA KỲ
**Deadline: 18/10**

### M1.1 — Phân tích kiến trúc Async của bộ Parser
- [ ] M1.1.1 Đọc mã nguồn `mealie/services/parser_services/ingredient_parser.py`.
- [ ] M1.1.2 Xác định hàm `BruteForceParser.parse_one(text)` là hàm bất đồng bộ (`async def`).
- [ ] M1.1.3 Xác định các tham số khởi tạo cần thiết: `session`, `group_id`, `household_id`.

### M1.2 — Thiết lập môi trường và fixture Mock
- [ ] M1.2.1 Cài đặt thư viện: `pip install pytest-asyncio pytest-cov`.
- [ ] M1.2.2 Cập nhật `pytest.ini` bổ sung: `asyncio_mode = auto`.
- [ ] M1.2.3 Tạo mock fixture trong `tests/conftest.py` dùng `unittest.mock.MagicMock` cô lập database.
- [ ] M1.2.4 Đóng góp nội dung phân tích kỹ thuật Async/Mock vào Báo cáo giữa kỳ của Trưởng nhóm Quân.
- [ ] M1.2.5 Commit: `chore: setup async test runner and parser mock fixtures`.

---

## ✅ NHÓM VIỆC M2: LẬP TRÌNH KIỂM THỬ PBT — PROPERTY 3 (CRASH-FREE INGREDIENT PARSER)
**Deadline: 25/11** | File code: `tests/unit_tests/test_pbt_ingredient_parser.py`

### M2.1 — Hiện thực kịch bản kiểm thử Property 3
- [ ] M2.1.1 Tạo nhánh `feat/manh-property-3-rca` từ `develop`.
- [ ] M2.1.2 Tạo file `tests/unit_tests/test_pbt_ingredient_parser.py`.
- [ ] M2.1.3 Viết test PBT kiểm tra tính bền bỉ Crash-free với mọi chuỗi Unicode ngẫu nhiên:
  ```python
  import pytest
  import asyncio
  from unittest.mock import MagicMock
  from hypothesis import given, strategies as st, settings
  from mealie.services.parser_services.ingredient_parser import BruteForceParser

  @given(st.text(max_size=500))
  @settings(max_examples=300)
  def test_ingredient_parser_never_crashes(text):
      """Property 3: Hàm parse_one không bao giờ được ném Unhandled Exception"""
      try:
          mock_session = MagicMock()
          parser = BruteForceParser(session=mock_session, group_id=None, household_id=None)
          result = asyncio.run(parser.parse_one(text))
          assert result is not None
      except Exception as e:
          pytest.fail(f"CRASH phát hiện với input {text!r}\nException type: {type(e).__name__}: {e}")
  ```
- [ ] M2.1.4 Viết test mở rộng với các tập dữ liệu biên đặc biệt (chuỗi chỉ chứa ký tự toán học, chuỗi cực dài không dấu cách, null byte `\x00`).
- [ ] M2.1.5 Chạy kiểm thử: `pytest tests/unit_tests/test_pbt_ingredient_parser.py -v`.
- [ ] M2.1.6 Commit & tạo Pull Request vào `develop`: `feat(test): add PBT Property 3 crash-free ingredient parser`.

---

## ✅ NHÓM VIỆC M3: THỰC THI TỔNG THỂ, THU THẬP LOG & ĐO CODE COVERAGE
**Deadline: 05/12**

### M3.1 — Chạy toàn bộ 5 test suites và thu thập Log
- [ ] M3.1.1 Chạy toàn bộ 5 file test PBT ở mức kiểm thử cao nhất (`max_examples=500`):
  ```bash
  pytest tests/unit_tests/test_pbt_*.py -v --tb=long > logs/test_run_final.txt 2>&1
  ```
- [ ] M3.1.2 Xác nhận `logs/test_run_final.txt` ghi lại chi tiết các ca test, thời gian và trạng thái hoàn thành.

### M3.2 — Đo lường độ bao phủ mã nguồn (Code Coverage)
- [ ] M3.2.1 Thực hiện lệnh đo Coverage tập trung vào module `parser_services`:
  ```bash
  pytest tests/unit_tests/test_pbt_*.py \
    --cov=mealie/services/parser_services \
    --cov-report=html:logs/coverage_html \
    --cov-report=term-missing > logs/coverage_summary.txt 2>&1
  ```
- [ ] M3.2.2 Mở báo cáo `logs/coverage_html/index.html` trên trình duyệt và chụp ảnh màn hình → lưu `Documents/assets/coverage_report.png`.
- [ ] M3.2.3 Lập bảng thống kê chi tiết tỷ lệ Line Coverage và Branch Coverage của từng file mục tiêu.
- [ ] M3.2.4 Commit: `test: execute comprehensive test suite, save execution logs and coverage artifacts`.

---

## ✅ NHÓM VIỆC M4: PHÂN TÍCH LỖI ROOT CAUSE ANALYSIS (RCA), ĐỀ XUẤT BẢN VÁ & SOẠN PHẦN G
**Deadline: 10/12**

### M4.1 — Soạn thảo `Documents/bao_cao_phan_G.md`
- [ ] M4.1.1 Trình bày bảng tổng kết số liệu thực nghiệm: Tổng số test cases sinh bởi Hypothesis, tỷ lệ Pass/Fail, bảng số liệu Coverage.

### M4.2 — Phân tích lỗi Root Cause Analysis (RCA) & Đề xuất bản vá
- [ ] M4.2.1 Trích xuất thông tin Falsifying Example từ log của Hypothesis.
- [ ] M4.2.2 Tái hiện lỗi độc lập trong môi trường Python tối giản và trích xuất traceback chi tiết từ dưới lên.
- [ ] M4.2.3 Phân loại và giải thích nguyên nhân cốt lõi (chia cho 0, lỗi ép kiểu, regex backtracking,...).
- [ ] M4.2.4 Soạn thảo đề xuất bản vá lỗi (Patch Proposal) chuẩn Ponytail dưới dạng mã diff.
- [ ] M4.2.5 *(Trường hợp không có bug):* Chứng minh độ tin cậy qua tỷ lệ Code Coverage $\ge 80\%$.
- [ ] M4.2.6 Hoàn thiện Phần G và bàn giao cho Trưởng nhóm Quân tích hợp vào báo cáo cuối kỳ.
- [ ] M4.2.7 Commit: `docs: complete test results, defect root cause analysis and patch proposals Phan G`.

---
---

# 🔍 CHECKLIST NGHIỆM THU CUỐI KỲ (Toàn nhóm tự kiểm tra trước khi nộp)

## Mốc Giữa kỳ — 20/10
- [x] Repo GitHub được khởi tạo chuẩn, có branch `main`, `develop` và pin version Mealie `v3.28.0` (Quân hoàn thành).
- [ ] Mealie chạy thành công demo trực tiếp qua Docker Compose trên cổng 9925 (Nam xác nhận).
- [ ] Đủ 6 ảnh chụp bằng chứng 3 luồng nghiệp vụ cốt lõi (Nam & Phước nghiệm thu).
- [ ] Tài liệu On-boarding `Documents/bao_cao_phan_C.md` chi tiết, đã được Hiếu cài đặt thẩm định thành công từ máy sạch độc lập.
- [ ] Sơ đồ kiến trúc tổng thể và Data Flow đầy đủ trong `Documents/bao_cao_phan_B.md` (Quân hoàn thành).
- [ ] Đề cương kế hoạch kiểm thử PBT rõ phạm vi và giả định kỹ thuật (Hiếu & Quân hoàn thành).
- [ ] Cấu hình async/mock cơ bản cho bộ parser sẵn sàng (Mạnh hoàn thành).
- [ ] **Cả 5 thành viên đều có ít nhất 1–2 commit Git hợp lệ trong Sprint 1 & 2.**

## Mốc Cuối kỳ — Tháng 12
- [ ] Cuốn báo cáo hoàn chỉnh đầy đủ 8 phần từ A đến H không thiếu mục nào (Quân tổng hợp).
- [ ] **Toàn bộ 5 file test PBT chạy tự động trơn tru bằng 1 lệnh duy nhất (`pytest tests/unit_tests/test_pbt_*.py -v`).**
- [ ] **Cả 5 thành viên đều có ít nhất 1 commit code kiểm thử (`feat(test):`) trực tiếp trên repo.**
- [ ] Test Runner biệt lập qua Docker chạy thành công trên mọi máy tính (Nam hoàn thành).
- [ ] Đã chỉ ra được ít nhất 1 lỗi thực tế kèm phân tích RCA và đề xuất bản vá HOẶC chứng minh Coverage đạt chuẩn $\ge 80\%$ (Mạnh hoàn thành).
- [ ] `tests/README.md` đã được kiểm thử chéo và tái lập thành công từ máy sạch độc lập (Phước & Hiếu xác nhận).
- [ ] Lịch sử Git thể hiện sự đóng góp tích cực, đều đặn của **cả 5 thành viên** xuyên suốt từ Sprint 1 đến Sprint 5.
- [ ] Đã ghim Commit SHA và gắn Git Tag `v1.0-final` vào repo nhóm (Quân hoàn thành).
- [ ] Slide bảo vệ chuẩn bị chỉn chu, phân vai thuyết trình rành mạch cho từng thành viên.
