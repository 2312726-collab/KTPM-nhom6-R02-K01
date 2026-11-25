# BIÊN BẢN KIỂM TRA & PHÂN CÔNG SỬA LỖI TỪNG THÀNH VIÊN
## ĐỒ ÁN KIỂM THỬ PHẦN MỀM — NHÓM 6 (TỔ HỢP R02 — K01)

* **Hệ thống mục tiêu (R02):** `mealie-recipes/mealie` — Release Tag **`v3.28.0`** | Commit SHA **`0552eaa4a80031b8572849cca0ed95d07f1be001`**
* **Kỹ thuật kiểm thử (K01):** Property-Based Testing (PBT) với `Hypothesis` + `pytest`
* **Thời điểm rà soát:** Sau khi merge PR #11 (`2312695-NguyenPhamPhuNam-Phan1`) vào `develop` tại commit `d5d4b70`
* **Người lập & rà soát:** Trần Quốc Quân (MSSV: `2312726` — Trưởng nhóm)

---

## I. MỤC TIÊU CỐT LÕI CỦA DỰ ÁN KTPM NÀY

Căn cứ vào đề bài của Giảng viên ([`ban_phan_cong_de_tai.md`](ban_phan_cong_de_tai.md)) và bộ quy chuẩn kỹ thuật nhóm ([`quy_tac_du_an.md`](quy_tac_du_an.md)), dự án không chỉ dừng ở việc viết test ví dụ chạy cho qua mà phải đạt **5 mục tiêu bắt buộc**:

1. **Làm chủ hệ thống thật đúng phiên bản đã Pin (R02 — Phần 1):**
   - Đọc hiểu kiến trúc, luồng dữ liệu và cài đặt thành công Mealie đúng bản **`v3.28.0`** (Commit SHA `0552eaa4a80031b8572849cca0ed95d07f1be001`) để bảo đảm mọi nhóm và giảng viên đều tái lập chính xác 100% cùng một codebase.
2. **Kiểm thử trực tiếp trên mã nguồn THẬT của Mealie (Không tự viết lại logic để tự test):**
   - Mọi kịch bản kiểm thử PBT (`test_pbt_*.py`) bắt buộc phải gọi trực tiếp các hàm/lớp thực tế trong `mealie_src/mealie/` tại ranh giới tin cậy (`parser_services/`, `recipe_ingredient.py`, `household_services/shopping_lists.py`), không dùng logic tự viết lại mô phỏng bên ngoài để qua mắt bài test.
3. **Vận dụng đúng bản chất Property-Based Testing (K01 — Phần 2):**
   - Xác định **tính chất bất biến phổ quát (Universal Invariants)** (lũy đẳng, bảo toàn hai chiều, đơn điệu, bảo toàn số học, bền bỉ crash-free), để `Hypothesis` tự sinh hàng trăm đến hàng ngàn ca kiểm thử và dùng **Shrinking** thu nhỏ phản ví dụ lỗi.
   - Tuyệt đối không viết assertion giả (ví dụ `... or True`), không bọc điều kiện `if` khiến case cần kiểm tra bị bỏ qua âm thầm.
4. **Phát hiện lỗi thật hoặc chứng minh độ phủ (Coverage) + Root Cause Analysis (Phần G):**
   - Thu thập log chạy toàn bộ 5 suite bằng 1 lệnh duy nhất, đo độ phủ trực tiếp trên mã nguồn Mealie (không đo nhầm lên thư mục `tests/`), lập hồ sơ lỗi thật (Defect Log) kèm truy vết tận gốc (RCA) và đề xuất bản vá.
5. **Làm việc nhóm chuẩn Git & Tái lập 1-click (Phần F & H):**
   - Cả 5 thành viên đều có code test hợp lệ trên nhánh riêng và merge vào `develop` qua Pull Request; mọi tài liệu, MSSV, lệnh chạy trong `README.md`, `tests/README.md`, `Dockerfile.test` và `requirements-test.txt` phải đồng nhất và chạy xanh 100% từ đầu đến cuối.

---

## II. KIỂM TRA ĐỐI CHIẾU MEALIE PIN VERSION Ở ĐẦU `README.md`

Đầu [`README.md`](../README.md#L8) ghi cố định: **Release Tag `v3.28.0` | Commit SHA `0552eaa4a80031b8572849cca0ed95d07f1be001`**.

| Thành phần kiểm tra | Trạng thái thực tế đã kiểm chứng | Kết luận |
| :--- | :--- | :---: |
| **`mealie_src/` (Local codebase)** | `git -C mealie_src rev-parse HEAD` = `0552eaa4a80031b8572849cca0ed95d07f1be001`; tag `v3.28.0` | **ĐẠT** |
| **`Documents/mealie_version.md`** | Ghi đúng tag `v3.28.0` và SHA `0552eaa4a80031b8572849cca0ed95d07f1be001` | **ĐẠT** |
| **`mealie_docker/docker-compose.yml`** | Image `ghcr.io/mealie-recipes/mealie:v3.28.0` | **ĐẠT** |
| **`Dockerfile.test`** | `FROM python:3.14-slim`, label `v3.28.0` và `0552eaa4a80031b8572849cca0ed95d07f1be001`, nhưng chỉ `COPY` mỗi `parser_utils/` | **CẦN BỔ SUNG** |
| **Python Runtime trên `.venv` host** | Đang dùng **Python `3.13.2`**, trong khi `mealie_src/pyproject.toml:7` yêu cầu `requires-python = ">=3.14,<3.15"` | **LỆCH RUNTIME** |
| **Dependencies trong `.venv` & `requirements-test.txt`** | `requirements-test.txt` thiếu `sqlalchemy`, `pydantic-settings`, `python-dotenv`, `pyhumps`, `python-slugify`, `rapidfuzz`, `text-unidecode`, `fastapi`. Trên `.venv` đang thiếu `rapidfuzz` | **THIẾU DEPS** |

> **Giải thích lỗi Runtime Python 3.13 vs 3.14:** Trong `mealie_src/mealie/core/settings/settings.py:29`, Mealie `v3.28.0` viết `def _missing_(cls, value: object) -> ScraperProxyMode:` mà không có `from __future__ import annotations`, vì hệ thống gốc chạy **Python 3.14** (hỗ trợ PEP 649 đánh giá annotation trễ). Khi chạy trên `.venv` Python 3.13.2 mà import thẳng `mealie.schema.recipe` sẽ ném `NameError: name 'ScraperProxyMode' is not defined`.

---

## III. TỔNG HỢP ĐÁNH GIÁ 5 PROPERTIES PBT SO VỚI MÃ NGUỒN MEALIE THẬT

Kết quả chạy `.venv\Scripts\pytest tests/unit_tests/ -v`: **Bị gãy ngay bước collect (`Interrupted: 1 error during collection`)** tại `tests/unit_tests/test_manh_m1_async_mock.py:26`. Khi bỏ qua file của Mạnh (`--ignore=tests/unit_tests/test_manh_m1_async_mock.py`), **51/51 test cases** của 4 file còn lại pass (`8.27s`), nhưng còn nhiều sai sót chuyên môn và kỹ thuật:

| Property | Thành viên | File code hiện tại | Có chạy code thật Mealie `v3.28.0`? | Coverage thực tế đo được | Đánh giá tổng quan |
| :---: | :--- | :--- | :--- | :--- | :---: |
| **P1** | **Trần Ngọc Bảo Phước** (`2312719`) | `tests/unit_tests/test_pbt_string_utils.py` | **CÓ** (`string_utils.py`) | Bị `CoverageWarning: module-not-measured` do rơi vào `except` nạp tên `"string_utils"` | **Cần sửa 4 điểm** |
| **P2** | **Bùi Trung Hiếu** (`2312611`) | `tests/unit_tests/test_pbt_unit_converter.py` | **CÓ** (`unit_utils.py`) | **59%** `unit_utils.py` (0% toàn bộ hàm `merge`) | **Cần sửa 5 điểm** |
| **P3** | **Võ Hùng Mạnh** (`2312687`) | *Chưa có `test_pbt_ingredient_parser.py`*; mới có `test_manh_m1_async_mock.py` | `test_manh_m1_async_mock.py` bị **Collection Error**, chưa có test Hypothesis PBT | **0%** (không collect được) | **Lỗi nghiêm trọng / Thiếu file chính** |
| **P4** | **Trần Quốc Quân** (`2312726`) | `tests/unit_tests/test_pbt_scaling.py` | **MỚI MỘT PHẦN** (đã test `RecipeIngredientBase` thật, nhưng `scale_mealie_ingredient` tự viết; chưa gọi `ShoppingListService` thật) | **68%** `recipe_ingredient.py`; **0%** `shopping_lists.py` | **Cần nâng cấp & sửa 3 điểm** |
| **P5** | **Nguyễn Phạm Phú Nam** (`2312695`) | `tests/unit_tests/test_pbt_fraction.py` | **CÓ** (`string_utils.py`) | Không gộp vào `--cov=mealie...string_utils` do nạp tên `"mealie_string_utils"` (chỉ đo riêng `--cov=mealie_string_utils` được 86%) | **Cần sửa 3 điểm** |

---

## IV. PHÂN CÔNG CHI TIẾT SỬA LỖI CHO TỪNG THÀNH VIÊN

### 1. Võ Hùng Mạnh (MSSV: `2312687`) — Ưu tiên CAO NHẤT (Đang chặn cả nhóm)

* **Vấn đề cốt lõi:** Toàn bộ `pytest tests/unit_tests/` đang không chạy được vì lỗi trong `test_manh_m1_async_mock.py` và thiếu hẳn file kiểm thử PBT Property 3 (`test_pbt_ingredient_parser.py`).
* **Danh sách việc phải sửa:**
  - [ ] **M-FIX-1 (Chặn luồng):** Sửa lỗi `NameError: name 'ScraperProxyMode' is not defined` và thiếu `rapidfuzz` ở `tests/unit_tests/test_manh_m1_async_mock.py:26`. Phối hợp với Phước & Nam bổ sung `rapidfuzz` (và `fastapi` hoặc stub cô lập settings tương thích Python 3.13/3.14 ở `tests/conftest.py`), **tuyệt đối không sửa file trong `mealie_src/`** để giữ nguyên SHA `0552eaa4a80031b8572849cca0ed95d07f1be001`.
  - [ ] **M-FIX-2 (Thiếu sản phẩm bắt buộc):** Tạo mới file **`tests/unit_tests/test_pbt_ingredient_parser.py`** (hiện chưa tồn tại!) kiểm thử **Property 3** bằng `Hypothesis` (`@pytest.mark.pbt`, `@given(st.text(...))`, ký tự điều khiển, null-byte `\x00`, chuỗi chỉ chứa ngoặc/dấu cách) gọi trực tiếp vào **`BruteForceParser.parse_one()`** thật của Mealie `v3.28.0` (kèm mock `Session`, `AllRepositories`, `Translator`).
  - [ ] **M-FIX-3 (Ghi nhận bug thật của Mealie `v3.28.0`):** Kiểm chứng và ghi nhận cả 2 lỗi `IndexError` thật của `BruteForceParser` (`brute/process.py:152` với `""`/`"   "` và `brute/process.py:199 -> 110` với chuỗi như `"a cup"` khi DB khớp đơn vị ở token cuối) bằng `@pytest.mark.xfail` hoặc tách characterization test rõ ràng, đưa vào Defect Log.
  - [ ] **M-FIX-4 (Báo cáo Phần G & Artifacts `logs/`):** Sau khi cả 5 suite chạy xanh, chạy tổng hợp và đo Coverage HTML toàn bộ `mealie_src/mealie/`, tạo **`Documents/bao_cao_phan_G.md`** chứa bảng thống kê test cases, ảnh chụp coverage, và hồ sơ Defect Log + Root Cause Analysis + Đề xuất bản vá cho **toàn bộ các lỗi thật nhóm tìm được** (Mục V bên dưới).

---

### 2. Bùi Trung Hiếu (MSSV: `2312611`) — Sửa lỗi logic Assert & Mở rộng Coverage Property 2

* **Vấn đề cốt lõi:** Có gọi `UnitConverter` thật của Mealie `v3.28.0`, nhưng có assertion vô hiệu (`or True`), hiểu sai hàm `_resolve_ounce` của Mealie, bị deselected khi chạy `-m pbt`, và mới đạt 59% coverage `unit_utils.py`.
* **Danh sách việc phải sửa:**
  - [ ] **H-FIX-1 (Assertion giả — Nặng):** Tại `tests/unit_tests/test_pbt_unit_converter.py:199-206` (`test_unknown_unit_raises_unit_not_found`), **xóa bỏ hoàn toàn `or True`** và khối `try...except` nuốt mất trường hợp không ném lỗi. Dùng strategy sinh tên đơn vị chắc chắn không tồn tại (ví dụ tiền tố `"unknown_unit_"` + `st.text(...)`) và khẳng định trực tiếp bằng `with pytest.raises(UnitNotFound): converter.parse(invalid_unit, strict=True)`.
  - [ ] **H-FIX-2 (Hiểu sai `_resolve_ounce` & điều kiện `if` che lỗi):** Tại `tests/unit_tests/test_pbt_unit_converter.py:164-184` (`test_incompatible_units_handling`):
    - Loại bỏ cặp `("milliliter", "ounce")` khỏi `incompatible_pair`, vì qua kiểm tra code thật `unit_utils.py:45-61`, Mealie cố tình thiết kế `_resolve_ounce()` để đổi `"ounce"` sang `"fluid_ounce"` khi đi kèm thể tích (`can_convert("milliliter", "ounce") == True`). Hãy viết 1 property test riêng kiểm chứng cơ chế `_resolve_ounce()` này của Mealie!
    - Trong `test_incompatible_units_handling`, bỏ bọc `if not converter.can_convert(u1, u2):` — phải `assert not converter.can_convert(u1, u2)` và bắt buộc `with pytest.raises(Exception): converter.convert(value, u1, u2)`.
  - [ ] **H-FIX-3 (Thiếu marker):** Thêm `@pytest.mark.pbt` cho toàn bộ các hàm kiểm thử PBT trong `test_pbt_unit_converter.py` để không bị bỏ sót khi chạy `pytest -m pbt`.
  - [ ] **H-FIX-4 (Nâng Coverage `unit_utils.py` từ 59% lên >85%):** Viết thêm PBT kiểm thử `UnitConverter.merge()` và `merge_quantity_and_unit()` (`unit_utils.py:117-170`) sử dụng `CreateIngredientUnit` thật của Mealie (kiểm tra tính giao hoán $merge(q_1, u_1, q_2, u_2) \approx merge(q_2, u_2, q_1, u_1)$ và bảo toàn thứ nguyên).
  - [ ] **H-FIX-5 (Đồng bộ MSSV & Tài liệu D/E):** Sửa MSSV `2110037` $\to$ `2312611` tại `Documents/tien_do_Bui_Trung_Hieu.md:4`; cập nhật `Documents/bao_cao_phan_E.md` cho khớp với code thực tế của P3, P4, P5 (sai số P5 `1e-4` hay `1e-6`, module P4); phối hợp Nam chốt xác nhận thẩm định chéo mục `H1.2.2`.

---

### 3. Trần Ngọc Bảo Phước (MSSV: `2312719`) — Sửa Test Harness, Coverage README & Strategy cho `move_parens_to_end`

* **Vấn đề cốt lõi:** Có test hàm thật trong `string_utils.py`, nhưng hướng dẫn đo coverage trong `tests/README.md` bị sai mục tiêu (`--cov=tests`), còn đường dẫn cứng ổ `F:`, fallback nạp sai tên module, và chưa bắt được bug thật trong `move_parens_to_end()`.
* **Danh sách việc phải sửa:**
  - [ ] **P-FIX-1 (Sai lệnh Coverage — Nặng):** Sửa `tests/README.md:35` từ `--cov=tests` thành đo trực tiếp trên mã nguồn Mealie thật (`--cov=mealie.services.parser_services.parser_utils.string_utils` cho P1 và lệnh tổng hợp `--cov=mealie_src/mealie/services/parser_services --cov=mealie_src/mealie/schema/recipe/recipe_ingredient` cho cả nhóm); sửa dòng 16 để hướng dẫn cài `pip install -r requirements-test.txt`.
  - [ ] **P-FIX-2 (Đường dẫn cứng cá nhân):** Xóa dòng `Path("f:/KTPM/mealie/...")` tại `tests/unit_tests/test_pbt_string_utils.py:26`.
  - [ ] **P-FIX-3 (Đồng bộ cơ chế nạp module & fix `CoverageWarning`):** Thống nhất với Nam và `tests/conftest.py` cách cô lập `mealie.services.parser_services` để cả P1 và P5 đều chạy trên đúng module name **`mealie.services.parser_services.parser_utils.string_utils`**, loại bỏ hoàn toàn `CoverageWarning: module-not-measured`.
  - [ ] **P-FIX-4 (Nâng cấp strategy kiểm tra `move_parens_to_end`):** Hiện `@given(s=st.text())` hầu như không bao giờ trúng regex `r"(.){1,6}\s\((.[^\(\)])+\)\s"` của `string_utils.py:14`. Cần thêm strategy sinh chuỗi nguyên liệu có chứa cụm ngoặc `(note)` (ví dụ chuỗi đa ngoặc `'1 (aa) (bb) '`) để thực sự đi qua nhánh hoán đổi ngoặc trong code Mealie thật — qua đó phát hiện và ghim bug vi phạm lũy đẳng của Mealie `v3.28.0` (chuyển Mạnh ghi RCA).
  - [ ] **P-FIX-5 (Cập nhật `bao_cao_phan_F.md`):** Sửa dòng 60 (`asyncio: STRICT`, không phải `auto`) và dòng 79 (P4 target đúng), đồng thời cập nhật lại kết quả log/coverage tổng hợp sau khi cả 5 thành viên sửa xong.

---

### 4. Trần Quốc Quân (MSSV: `2312726` — Trưởng nhóm) — Kết nối hàm Scaling thật `ShoppingListService`, sửa test & đồng bộ dự án

* **Vấn đề cốt lõi:** Đã test thật `RecipeIngredientBase`, `display_fraction`, `_format_quantity_for_display()` (68% `recipe_ingredient.py`), nhưng phần thuật toán scale `scale_mealie_ingredient` đang tự viết lại trong file test. Mã nguồn thật của Mealie `v3.28.0` **không có hàm scale trong `recipe_service.py`**, mà logic scale backend thật nằm ở **`ShoppingListService.get_shopping_list_items_from_recipe()`** (`mealie_src/mealie/services/household_services/shopping_lists.py:323-418`).
* **Danh sách việc phải sửa:**
  - [ ] **Q-FIX-1 (Bám sát logic Scaling thật của Mealie `v3.28.0`):** Bổ sung nhóm test PBT trong `tests/unit_tests/test_pbt_scaling.py` gọi trực tiếp **`ShoppingListService.get_shopping_list_items_from_recipe(..., scale=k)`** thật của Mealie (mock `AllRepositories` tương tự Mạnh):
    - Kiểm chứng tính đơn điệu, tỉ lệ tuyến tính khi scale danh sách nguyên liệu thật và scale đệ quy **sub-recipe** (`shopping_lists.py:351`).
    - Kiểm chứng bất biến khi công thức có 2 dòng nguyên liệu cùng `food_id` và `unit_id` để **bắt bug thật ở `shopping_lists.py:403`** (`existing_item.quantity += ingredient.quantity` quên nhân `* scale` — đánh dấu `@pytest.mark.xfail` nếu giữ test xanh hoặc tách Defect Characterization Test cho Phần G).
  - [ ] **Q-FIX-2 (Sửa lỗi logic tại `test_pbt_scaling.py:303-310`):** Hàm `test_mealie_ingredient_none_and_zero_quantity(factor: float)` đang nhận biến `factor` nhưng không dùng (hardcode `target_servings=8, base_servings=4`) và bỏ quên ca `quantity=0.0`. Phải truyền `target_servings=4 * factor, base_servings=4` và assert cả `quantity=None` lẫn `quantity=0.0`.
  - [ ] **Q-FIX-3 (Đồng bộ tài liệu Phần A, B, E):** Đính chính lại tên module trong `Documents/bao_cao_phan_A.md:279` (và phối hợp Hiếu cập nhật `bao_cao_phan_E.md:19,86`): Servings Scaling ở Backend Mealie `v3.28.0` thuộc `mealie/services/household_services/shopping_lists.py` và `mealie/schema/recipe/recipe_ingredient.py` (không phải `recipe_service.py`), còn Client-side thuộc `frontend/app/composables/recipes/use-scaled-amount.ts`.
  - [ ] **Q-FIX-4 (Hoàn tất git & tài liệu quản lý):**
    - Sửa dòng 45 `README.md` (`tests/pytest.ini` $\to$ `pytest.ini`), kiểm tra kỹ rồi commit bản sửa MSSV trong `README.md` vào `develop`.
    - Xóa file rác local `Documents/bao_cao_phan_D.md.bak`.
    - Cập nhật MSSV của Hiếu (`2110037` $\to$ `2312611`) và các ô checkbox thực tế trong `Documents/phan_cong_nhiem_vu_thanh_vien.md`.
    - Sau khi 5 thành viên hợp nhất xong PR sửa lỗi, tổng hợp `Documents/bao_cao_phan_H.md`, đánh giá Exit Criteria và gắn tag **`v1.0-final`**.

---

### 5. Nguyễn Phạm Phú Nam (MSSV: `2312695`) — Sửa `Dockerfile.test`, `requirements-test.txt` & chuẩn hóa `test_pbt_fraction.py`

* **Vấn đề cốt lõi:** Bài P5 đã test hàm thật của Mealie tốt và chạy pass 28/28, nhưng tên module khi load làm hụt coverage chung, dung sai docstring vs code bị lệch, và môi trường Docker Test Runner hiện mới chạy được riêng P5 (chưa chạy được cả 5 suite như tài liệu hướng dẫn).
* **Danh sách việc phải sửa:**
  - [ ] **N-FIX-1 (Đồng bộ Docker Test Runner cho cả nhóm):**
    - Phối hợp Phước & Mạnh bổ sung đầy đủ dependencies Mealie mà P3/P4 cần vào **`requirements-test.txt`** (`sqlalchemy`, `pydantic-settings`, `python-dotenv`, `pyhumps`, `python-slugify`, `rapidfuzz`, `text-unidecode`, `fastapi`).
    - Cập nhật **`Dockerfile.test:49-50`** để `COPY` đủ các thư mục mã nguồn thật cần thiết (`mealie_src/mealie/schema/`, `mealie_src/mealie/services/`, `mealie_src/mealie/lang/`, `mealie_src/mealie/db/`, `mealie_src/mealie/pkgs/`...) thay vì chỉ copy `parser_utils/`, sao cho lệnh ở dòng 16 (`docker compose -f docker-compose.test.yml run --rm test-runner pytest tests/ -v --tb=long`) chạy **PASS 100% toàn bộ 5 Properties** trong môi trường Python 3.14 sạch!
  - [ ] **N-FIX-2 (Chuẩn hóa module name đo Coverage):** Tại `tests/unit_tests/test_pbt_fraction.py:48`, thay `"mealie_string_utils"` bằng cơ chế nạp đúng tên **`mealie.services.parser_services.parser_utils.string_utils`** (dùng chung helper/cơ chế trong `conftest.py` với Phước) để coverage của P1 + P5 cộng gộp chính xác, không còn `CoverageWarning`.
  - [ ] **N-FIX-3 (Đồng nhất dung sai, assert & marker):**
    - Sửa `EPSILON = 1e-6` tại `test_pbt_fraction.py:81` cho khớp với docstring dòng 10 và `bao_cao_phan_E.md:103` (hoặc thống nhất `1e-4` ở cả 3 nơi — khuyến nghị `1e-6` vì `Fraction` cho sai số float `< 1e-9`).
    - Sửa dòng 267 (`test_p5g_zero_denominator_safe_handling`): thay `assert "1/0" in remaining or "cup" in remaining` thành kiểm tra chặt `assert "1/0" in remaining and "cup" in remaining`.
    - Đổi marker `@pytest.mark.pbt` ở 4 hàm deterministic unit test cố định (`test_p5g_zero_numerator_edge_case`, `zero_denominator`, `empty_and_whitespace`, `text_without_numbers`, dòng 254-283) sang `@pytest.mark.unit` (hoặc tham số hóa bằng Hypothesis).

---

## V. CÁC LỖI THẬT TRONG MEALIE `v3.28.0` ĐÃ XÁC MINH ĐỂ ĐƯA VÀO PHẦN G (DEFECT LOG & RCA)

Qua kiểm tra trực tiếp trên mã nguồn Mealie SHA `0552eaa4a80031b8572849cca0ed95d07f1be001`, nhóm đã xác minh được **5 lỗi / hạn chế kỹ thuật thực tế** dưới đây (Mạnh phụ trách tổng hợp vào `bao_cao_phan_G.md`, mỗi thành viên kiểm chứng tái hiện lỗi thuộc phần mình):

1. **Defect #1 (Servings Scaling — `mealie/services/household_services/shopping_lists.py:403`):**
   - *Hiện tượng:* Khi thêm công thức vào danh sách đi chợ với hệ số `scale != 1`, nếu công thức có **2 dòng nguyên liệu trùng khớp** (`can_merge == True`), dòng thứ nhất được nhân `ingredient.quantity * scale` (dòng 380), nhưng dòng thứ hai trở đi bị cộng trực tiếp `existing_item.quantity += ingredient.quantity` (dòng 403) — **quên nhân `* scale`!** Khi gỡ công thức ra khỏi danh sách (dòng 512), tổng bị trừ âm số lượng.
2. **Defect #2 (BruteForceParser — `mealie/services/parser_services/brute/process.py:199 -> 110`):**
   - *Hiện tượng:* Nếu chuỗi không bắt đầu bằng số và có đơn vị khớp DB nằm ở **token cuối cùng** (ví dụ `"a cup"` khi DB có unit `"cup"`), vòng lặp gọi `parse_ingredient(tokens[index + 1 :])` với mảng rỗng `[]`, truy cập `tokens[-1]` tại dòng 110 ném **`IndexError: list index out of range`** (bên cạnh lỗi `IndexError` tại dòng 152 với chuỗi rỗng `""`).
3. **Defect #3 (String Utils — `mealie/services/parser_services/parser_utils/string_utils.py:9-20`):**
   - *Hiện tượng:* Hàm `move_parens_to_end()` **vi phạm tính lũy đẳng** $f(f(x)) \neq f(x)$ với chuỗi có nhiều cặp ngoặc cách khoảng trắng như `'1 (aa) (bb) '`: lần 1 $\to$ `'1  (bb)  (aa)'`, lần 2 $\to$ `'1    (aa) (bb)'`, cứ gọi lại đảo vị trí hai ngoặc và sinh thêm khoảng trắng vô hạn.
4. **Defect #4 (Quantity Display — `mealie/schema/recipe/recipe_ingredient.py:372-374`):**
   - *Hiện tượng:* Hàm `_format_quantity_for_display()` dùng vòng lặp `while qty.numerator > qty.denominator: whole_number += 1; qty -= 1` có độ phức tạp $O(N)$ theo độ lớn số lượng (nên dùng phép chia lấy nguyên `//`), gây nghẽn CPU nếu scale số lượng cực lớn (ví dụ triệu đơn vị).
5. **Defect #5 (Runtime Compatibility — `mealie/core/settings/settings.py:29`):**
   - *Hiện tượng:* Thiếu `from __future__ import annotations` ở đầu file khiến tự tham chiếu kiểu trả về `-> ScraperProxyMode:` làm sập import với `NameError` trên Python 3.13 (chỉ chạy được trên Python 3.14+).

---

## VI. THỨ TỰ THỰC HIỆN ĐỀ XUẤT CHO NHÓM (GATE TRƯỚC KHI ĐÓNG GÓI `v1.0-final`)

1. **Bước 1 (Gỡ chặn & Đồng bộ hạ tầng):** Nam + Phước + Mạnh cập nhật `requirements-test.txt`, `tests/conftest.py` (nếu hỗ trợ Python 3.13) và `Dockerfile.test` (Python 3.14) để môi trường nhóm cài 1 lệnh chạy được toàn bộ codebase Mealie `v3.28.0`.
2. **Bước 2 (Sửa code & bổ sung PBT từng cá nhân qua nhánh riêng $\to$ PR vào `develop`):**
   - Mạnh hoàn thiện `test_manh_m1_async_mock.py` và tạo mới `test_pbt_ingredient_parser.py`.
   - Hiếu sửa `test_pbt_unit_converter.py` (xóa `or True`, sửa `_resolve_ounce`, thêm `@pytest.mark.pbt`, test `merge`).
   - Phước sửa `test_pbt_string_utils.py`, `tests/README.md`, `bao_cao_phan_F.md`.
   - Quân nâng cấp `test_pbt_scaling.py` (kết nối `ShoppingListService`, sửa ca `quantity=0` & `factor`), commit `README.md`, dọn `.bak`, sửa `bao_cao_phan_A.md`.
   - Nam cập nhật `test_pbt_fraction.py` (module name, `EPSILON`, marker, assert chặt) và `Dockerfile.test`.
3. **Bước 3 (Kiểm chứng hợp nhất 1-click):** Chạy `pytest tests/unit_tests/ -v` trên cả host và Docker Runner (`docker compose -f docker-compose.test.yml run --rm test-runner pytest tests/ -v`), đạt **0 collection errors, 100% pass (hoặc xfail có chủ đích cho defect đã ghim)**.
4. **Bước 4 (Thu thập Coverage & Hoàn thiện Phần G, H):** Mạnh xuất báo cáo Coverage HTML và viết `bao_cao_phan_G.md`; Quân tổng hợp `bao_cao_phan_H.md`, kiểm tra Exit Criteria và gắn Git Tag `v1.0-final`.
