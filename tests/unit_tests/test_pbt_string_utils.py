"""
File: tests/unit_tests/test_pbt_string_utils.py
Kịch bản kiểm thử Property-Based Testing (PBT) cho Module tiền xử lý chuỗi: string_utils.py
Thực hiện bởi: Trần Ngọc Bảo Phước (MSSV: 2312719) — QA Automation Engineer 1
Đặc tả nhiệm vụ: Property 1 — Tính lũy đẳng (Idempotence), Tính hoàn chỉnh (Completeness) và Tính bền bỉ (Robustness)
"""

import importlib.util
from fractions import Fraction
from pathlib import Path
import pytest
from hypothesis import given, strategies as st, settings, assume

# ==============================================================================
# 1. Cơ chế nạp Module string_utils linh hoạt (hỗ trợ cả môi trường full & isolated)
# ==============================================================================
def _load_string_utils():
    try:
        from mealie.services.parser_services.parser_utils import string_utils as su
        return su
    except Exception:
        candidates = [
            Path(__file__).resolve().parent.parent.parent / "mealie_src" / "mealie" / "services" / "parser_services" / "parser_utils" / "string_utils.py",
            Path(__file__).resolve().parent.parent.parent / "mealie" / "services" / "parser_services" / "parser_utils" / "string_utils.py",
            Path("mealie_src/mealie/services/parser_services/parser_utils/string_utils.py"),
            Path("f:/KTPM/mealie/mealie/services/parser_services/parser_utils/string_utils.py"),
            Path("mealie/services/parser_services/parser_utils/string_utils.py"),
        ]
        for p in candidates:
            if p.exists():
                spec = importlib.util.spec_from_file_location("string_utils", str(p))
                mod = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(mod)
                return mod
        raise ImportError("Không tìm thấy file string_utils.py của Mealie!")

su = _load_string_utils()

VULGAR_FRACTION_CHARS = [
    "¼", "½", "¾", "⅐", "⅑", "⅒", "⅓", "⅔", "⅕", "⅖", "⅗", "⅘", "⅙", "⅚", "⅛", "⅜", "⅝", "⅞"
]

# ==============================================================================
# 2. PROPERTY 1.1: TÍNH LŨY ĐẲNG CỦA HÀM XÓA DẤU CHÚ THÍCH (remove_footnote_markers)
# Toán học: f(f(s)) == f(s) với mọi chuỗi ký tự s
# ==============================================================================
@pytest.mark.pbt
@given(s=st.text())
def test_remove_footnote_markers_idempotent(s: str):
    """
    Kiểm tra tính lũy đẳng (Idempotence):
    Hàm xóa dấu sao chú thích ở cuối chuỗi (*) nếu áp dụng một lần hay nhiều lần
    đều phải mang lại kết quả đồng nhất: f(f(s)) == f(s).
    """
    once = su.remove_footnote_markers(s)
    twice = su.remove_footnote_markers(once)
    assert once == twice, f"Vi phạm tính lũy đẳng: input={s!r}, once={once!r}, twice={twice!r}"


# ==============================================================================
# 3. PROPERTY 1.2: TÍNH LŨY ĐẲNG CỦA HÀM DI CHUYỂN NGOẶC (move_parens_to_end)
# Toán học: f(f(s)) == f(s) với mọi chuỗi ký tự s
# ==============================================================================
@pytest.mark.pbt
@given(s=st.text())
def test_move_parens_to_end_idempotent(s: str):
    """
    Kiểm tra tính lũy đẳng khi di chuyển thông tin trong ngoặc về cuối chuỗi:
    Sau khi ngoặc đã được chuyển về cuối, lần gọi thứ hai không được làm xáo trộn
    hoặc nhân đôi thông tin: f(f(s)) == f(s).
    """
    once = su.move_parens_to_end(s)
    twice = su.move_parens_to_end(once)
    assert once == twice, f"Vi phạm tính lũy đẳng khi di chuyển ngoặc: input={s!r}, once={once!r}, twice={twice!r}"


# ==============================================================================
# 4. PROPERTY 1.3: TÍNH BỀN BỈ & HOÀN CHỈNH KHI CHUYỂN ĐỔI PHÂN SỐ UNICODE
# (convert_vulgar_fractions_to_regular_fractions)
# ==============================================================================
@pytest.mark.pbt
@given(s=st.text())
def test_convert_vulgar_fractions_crash_free_and_robust(s: str):
    """
    Kiểm tra tính bền bỉ Crash-free:
    Hàm chuyển đổi phân số unicode không bao giờ phát sinh ngoại lệ không mong muốn
    đối với bất kỳ chuỗi đầu vào nào (bao gồm ký tự điều khiển, emoji, khoảng trắng...).
    """
    result = su.convert_vulgar_fractions_to_regular_fractions(s)
    assert isinstance(result, str)


@pytest.mark.pbt
@given(s=st.text())
def test_convert_vulgar_fractions_completeness(s: str):
    """
    Kiểm tra tính hoàn chỉnh (Completeness / Post-condition):
    Sau khi xử lý, đảm bảo KHÔNG CÒN bất kỳ ký tự phân số unicode nào sót lại trong chuỗi.
    """
    result = su.convert_vulgar_fractions_to_regular_fractions(s)
    for vulgar_char in VULGAR_FRACTION_CHARS:
        assert vulgar_char not in result, f"Ký tự phân số unicode {vulgar_char!r} vẫn tồn tại trong chuỗi: {result!r}"


@pytest.mark.pbt
@given(s=st.text())
def test_convert_vulgar_fractions_idempotent(s: str):
    """
    Kiểm tra tính lũy đẳng của quá trình chuẩn hóa phân số unicode:
    f(f(s)) == f(s).
    """
    once = su.convert_vulgar_fractions_to_regular_fractions(s)
    twice = su.convert_vulgar_fractions_to_regular_fractions(once)
    assert once == twice, f"Vi phạm lũy đẳng chuẩn hóa phân số: once={once!r}, twice={twice!r}"


# ==============================================================================
# 5. PROPERTY 1.4: TÍNH BẢO TOÀN VÀ BẤT BIẾN KHI BÓC TÁCH ĐỊNH LƯỢNG
# (extract_quantity_from_string)
# ==============================================================================
@pytest.mark.pbt
@given(s=st.text())
def test_extract_quantity_crash_free_and_non_negative(s: str):
    """
    Kiểm tra tính bền bỉ và Invariant định lượng:
    - Không crash với bất kỳ chuỗi đầu vào nào (kể cả chứa mẫu số 0 - ZeroDivisionError).
    - Định lượng trả về luôn luôn là số không âm (quantity >= 0).
    - Chuỗi còn lại luôn là một chuỗi ký tự hợp lệ.
    """
    qty, remaining = su.extract_quantity_from_string(s)
    assert isinstance(qty, (int, float))
    assert qty >= 0, f"Định lượng trả về bị âm: {qty}"
    assert isinstance(remaining, str)


@pytest.mark.pbt
@given(
    whole=st.integers(min_value=1, max_value=100),
    num=st.integers(min_value=1, max_value=9),
    denom=st.integers(min_value=2, max_value=10),
    food_name=st.text(alphabet=st.characters(whitelist_categories=("Lu", "Ll")), min_size=3, max_size=15),
)
def test_extract_quantity_mixed_fraction_accuracy(whole: int, num: int, denom: int, food_name: str):
    """
    Kiểm tra độ chính xác khi phân tích hỗn số sinh ngẫu nhiên: 'W N/D food_name'
    Giá trị trích xuất phải đúng bằng: whole + (num / denom).
    """
    assume(denom > 0 and num < denom)
    input_str = f"{whole} {num}/{denom} {food_name}"
    expected_qty = float(whole + Fraction(num, denom))

    qty, remaining = su.extract_quantity_from_string(input_str)
    assert abs(qty - expected_qty) < 1e-4, f"Sai lệch định lượng: kỳ vọng {expected_qty}, thực tế {qty}"
    assert food_name in remaining
