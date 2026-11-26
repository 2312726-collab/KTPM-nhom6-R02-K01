# HƯỚNG DẪN THỰC THI & TÁI LẬP BỘ KIỂM THỬ PBT

> **Người phụ trách:** Trần Ngọc Bảo Phước (MSSV: 2312719) — QA Automation Engineer 1

## 1. Phạm vi

- **Test:** `tests/unit_tests/test_pbt_string_utils.py`
- **Module:** `mealie.services.parser_services.parser_utils.string_utils`
- Test import module bằng tên package chuẩn để pytest-cov gộp coverage chính xác.

## 2. Cài đặt

Dùng Python 3.14 và đảm bảo mã nguồn Mealie v3.28.0 đã được checkout tại `mealie_src/`, sau đó chạy tại thư mục gốc repo:

```powershell
python -m pip install -r requirements-test.txt
```

## 3. Lệnh chạy

Chạy Property 1:

```powershell
python -m pytest tests/unit_tests/test_pbt_string_utils.py -v
```

Chạy với profile `ci`:

```powershell
$env:HYPOTHESIS_PROFILE="ci"; python -m pytest tests/unit_tests/test_pbt_string_utils.py -v
```

Các test trong file này đặt tường minh `max_examples=300`; vì vậy đổi profile không làm thay đổi số examples của chúng.

Chạy toàn bộ các suite kiểm thử:

```powershell
python -m pytest tests/unit_tests/ -v
```

*(Lưu ý: Trên Windows PowerShell, dấu `*` trong `test_pbt_*.py` không tự bung tham số như Linux bash, nên dùng trực tiếp `tests/unit_tests/` hoặc lọc marker `-m pbt`).*

Đo coverage trực tiếp trên module Mealie được kiểm thử:

```powershell
python -m pytest tests/unit_tests/test_pbt_string_utils.py --cov=mealie.services.parser_services.parser_utils.string_utils -v
```

Coverage tổng hợp cho parser và ingredient schema:

```powershell
python -m pytest tests/unit_tests/test_pbt_*.py --cov=mealie_src/mealie/services/parser_services --cov=mealie_src/mealie/schema/recipe/recipe_ingredient -v
```

## 4. Đọc kết quả Hypothesis

- `PASSED`: test không tìm thấy đầu vào vi phạm tính chất trong lần chạy đó.
- `Falsifying example`: đầu vào cụ thể làm assertion thất bại; Hypothesis thường thu nhỏ đầu vào này.
- `Shrinking` / shrink trace: các bước Hypothesis thử rút gọn phản ví dụ. Chi tiết có thể hiện khi bật verbosity phù hợp, không nhất thiết xuất hiện trong log mặc định.

`test_move_parens_idempotent` được đánh dấu `XFAIL` có chủ đích để ghi nhận lỗi đã biết trong Mealie v3.28.0. `strict=True` sẽ làm test thất bại nếu lỗi được sửa mà dấu `xfail` chưa được gỡ.
