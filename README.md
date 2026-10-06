# ĐỒ ÁN CUỐI KỲ — MÔN KIỂM THỬ PHẦN MỀM
## TRƯỜNG ĐẠI HỌC ĐÀ LẠT — KHOA CÔNG NGHỆ THÔNG TIN

---

### 📌 THÔNG TIN ĐỀ TÀI
* **Tổ hợp đăng ký:** **R02 — K01**
  * **Hệ thống mục tiêu (Repo R02):** [Mealie](https://github.com/mealie-recipes/mealie) *(Phiên bản cố định: Release Tag `v3.28.0` | Commit SHA: `0552eaa4a80031b8572849cca0ed95d07f1be001`)*
  * **Kỹ thuật kiểm thử nâng cao (K01):** **Property-Based Testing (PBT)**
  * **Công cụ chủ đạo:** `Hypothesis` (Python) tích hợp cùng test runner `pytest`
* **Giảng viên hướng dẫn:** Nguyễn Thế Lâm
* **Nhóm thực hiện:** **Nhóm 6**
* **Kho lưu trữ GitHub:** [https://github.com/2312726-collab/KTPM-nhom6-R02-K01](https://github.com/2312726-collab/KTPM-nhom6-R02-K01)

---

### 👥 MA TRẬN PHÂN VAI & ĐÓNG GÓP CỦA 5 THÀNH VIÊN

| STT | Họ và tên | MSSV | Báo cáo phụ trách chính | Kịch bản Code PBT trực tiếp |
| :---: | :--- | :---: | :--- | :--- |
| 1 | **Trần Quốc Quân** | `2312726` | **Trưởng nhóm** — Phần A, Phần B, Phần H + Slide | **Property 4** (Servings Scaling Monotonicity & Reversibility) |
| 2 | **Nguyễn Phạm Phú Nam** | `2111874` | **Phần C** (Tài liệu On-boarding & Bằng chứng 3 luồng) | **Property 5** (Fraction Normalization & Numeric Preservation) + Docker Runner |
| 3 | **Bùi Trung Hiếu** | `2110037` | **Phần D & E** (Lý thuyết PBT & Thiết kế 5 kịch bản) | **Property 2** (Unit Conversion Round-trip) |
| 4 | **Trần Ngọc Bảo Phước** | `2111883` | **Phần F** (Test Harness & Hướng dẫn tái lập `README.md`) | **Property 1** (String Utils Idempotence & Robustness) |
| 5 | **Võ Hùng Mạnh** | `2111867` | **Phần G** (Log, Đo Coverage HTML & Phân tích RCA) | **Property 3** (Crash-free Ingredient Parser with Async Mock) |

---

### 🗂️ CẤU TRÚC THƯ MỤC DỰ ÁN

```text
DoAnCuoiKy_Nhom6/
├── .github/                      # Quy ước commit & cấu hình CI/CD
├── Documents/                    # Tài liệu báo cáo chính thức (Phần A -> Phần H)
│   ├── quy_tac_du_an.md          # Bộ quy tắc kỹ thuật chuẩn Ponytail
│   ├── ke_hoach_lo_trinh_thuc_hien.md  # Lộ trình 5 Sprint & Ma trận RACI
│   ├── phan_cong_nhiem_vu_thanh_vien.md # Bảng phân công nguyên tử theo thành viên
│   ├── mealie_version.md         # Tài liệu ghim cố định tag v3.28.0 & commit SHA
│   └── assets/                   # Bằng chứng thực nghiệm, sơ đồ kiến trúc
├── mealie_docker/                # [Nam phụ trách] Cấu hình Docker Compose chạy Mealie
│   ├── docker-compose.yml
│   └── .env
├── tests/                        # Toàn bộ mã nguồn kiểm thử tự động PBT của cả 5 bạn
│   ├── conftest.py               # [Phước & Mạnh] Cấu hình Hypothesis đa profile & Mock fixtures
│   ├── pytest.ini                # Cấu hình Pytest runner
│   ├── README.md                 # [Phước] Hướng dẫn tái lập và chạy test với 1 lệnh
│   └── unit_tests/
│       ├── test_pbt_string_utils.py       # [Phước] Property 1: Tính lũy đẳng (Idempotence)
│       ├── test_pbt_unit_converter.py     # [Hiếu]  Property 2: Tính bảo toàn hai chiều (Round-trip)
│       ├── test_pbt_ingredient_parser.py  # [Mạnh]  Property 3: Tính bền bỉ (Crash-free)
│       ├── test_pbt_scaling.py            # [Quân]  Property 4: Tính đơn điệu khi nhân khẩu phần
│       └── test_pbt_fraction.py           # [Nam]   Property 5: Tính bảo toàn giá trị phân số
├── logs/                         # [Mạnh] File log thực thi kiểm thử và báo cáo Coverage HTML
├── .gitignore
└── README.md
```

---

### 🗺️ LỘ TRÌNH THỰC HIỆN DỰ ÁN (5 SPRINTS)

1. **Sprint 1 (18/9 – 30/9): Khởi động & Cố định phiên bản**
   - Thiết lập Git repo, phân chia nhánh `main` / `develop`, ghim cố định tag Mealie `v3.28.0`.
2. **Sprint 2 (01/10 – 20/10): On-boarding & Báo cáo Giữa kỳ**
   - Dựng Docker Mealie, chạy thực nghiệm 3 luồng nghiệp vụ, vẽ sơ đồ kiến trúc, lập đề cương PBT.
   - 🎯 **Cột mốc 1: Báo cáo Giữa kỳ (20/10)**.
3. **Sprint 3 (21/10 – 10/11): Nghiên cứu lý thuyết & Thiết kế kịch bản PBT**
   - Soạn thảo cơ sở lý thuyết Hypothesis (Phần D), thiết kế chi tiết 5 Properties (Phần E).
4. **Sprint 4 (11/11 – 30/11): Lập trình bộ kiểm thử tự động**
   - Dựng Test Harness, code toàn bộ 5 file test PBT (mỗi thành viên tự code và commit 1 file test), kiểm thử khả năng thu nhỏ ca lỗi (Shrinking).
5. **Sprint 5 (01/12 – Bảo vệ): Phân tích lỗi, Đo Coverage & Tổng kết**
   - Chạy toàn bộ test suite, đo độ bao phủ mã nguồn với `pytest-cov`, thực hiện Root Cause Analysis (RCA) nếu có bug, đóng gói báo cáo 8 phần A→H và Slide thuyết trình.
   - 🎯 **Cột mốc 2: Bảo vệ Cuối kỳ (Tháng 12)**.
