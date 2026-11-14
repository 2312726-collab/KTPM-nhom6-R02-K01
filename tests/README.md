# HƯỚNG DẪN THỰC THI & TÁI LẬP BỘ KIỂM THỬ PBT (TEST HARNESS)

> **Người phụ trách:** Trần Ngọc Bảo Phước (MSSV: 2312719) — QA Automation Engineer 1  
> **Mục tiêu:** Cung cấp hướng dẫn 1-click để thiết lập môi trường, thực thi và tái lập toàn bộ bộ kiểm thử tự động Property-Based Testing (Hypothesis + Pytest) trên mọi máy tính độc lập.

---

## 1. VỊ TRÍ FILE KIỂM THỬ PROPERTY 1
- **File kiểm thử:** `tests/unit_tests/test_pbt_string_utils.py`
- **Module được kiểm thử:** `mealie/services/parser_services/parser_utils/string_utils.py`

---

## 2. CÀI ĐẶT THƯ VIỆN CẦN THIẾT
```bash
pip install pytest hypothesis pytest-cov
```

---

## 3. CÁC LỆNH CHẠY KIỂM THỬ 1-CLICK

### 3.1. Chạy riêng kịch bản Property 1 (String Utils Idempotence)
```powershell
python -m pytest tests/unit_tests/test_pbt_string_utils.py -v
```

### 3.2. Chạy với profile CI (300 test cases sinh ngẫu nhiên)
```powershell
$env:HYPOTHESIS_PROFILE="ci"; python -m pytest tests/unit_tests/test_pbt_string_utils.py -v
```

### 3.3. Chạy đo độ bao phủ mã nguồn (Code Coverage)
```powershell
python -m pytest tests/unit_tests/test_pbt_string_utils.py --cov=tests -v
```

---

## 4. KẾT QUẢ THỰC THI THỰC TẾ
```text
tests/unit_tests/test_pbt_string_utils.py::test_remove_footnote_markers_idempotent PASSED [ 14%]
tests/unit_tests/test_pbt_string_utils.py::test_move_parens_to_end_idempotent PASSED [ 28%]
tests/unit_tests/test_pbt_string_utils.py::test_convert_vulgar_fractions_crash_free_and_robust PASSED [ 42%]
tests/unit_tests/test_pbt_string_utils.py::test_convert_vulgar_fractions_completeness PASSED [ 57%]
tests/unit_tests/test_pbt_string_utils.py::test_convert_vulgar_fractions_idempotent PASSED [ 71%]
tests/unit_tests/test_pbt_string_utils.py::test_extract_quantity_crash_free_and_non_negative PASSED [ 85%]
tests/unit_tests/test_pbt_string_utils.py::test_extract_quantity_mixed_fraction_accuracy PASSED [100%]

============================== 7 passed in 1.44s ==============================
```
