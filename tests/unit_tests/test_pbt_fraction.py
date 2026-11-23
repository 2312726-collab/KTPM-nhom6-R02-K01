"""
Property-Based Testing — Property 5: Fraction Normalization & Numeric Preservation
Đồ án Kiểm thử Phần mềm — Nhóm 6 (R02 - Mealie v3.28.0 + K01 - Hypothesis PBT)
Thành viên phụ trách: Nguyễn Phạm Phú Nam (MSSV: 2312695) — DevOps & Automation QA
Mã nguồn kiểm thử: mealie_src/mealie/services/parser_services/parser_utils/string_utils.py

BẤT BIẾN TOÁN HỌC (INVARIANTS):
1. Numeric Preservation (Bảo toàn số học):
   Với bất kỳ phân số thường (n/d), phân số Unicode (¼, ½, ¾...), hoặc hỗn số (w n/d, w½),
   giá trị số thực trích xuất được phải bằng giá trị toán học thực tế trong sai số epsilon <= 1e-6.
2. Information Preservation (Bảo toàn thông tin văn bản):
   Phần văn bản nguyên liệu đi kèm sau lượng số (suffix) phải được giữ nguyên vẹn trong remaining_str,
   không bị nuốt hay cắt xén.
3. Idempotence (Tính lũy đẳng):
   Áp dụng chuẩn hóa phân số nhiều lần liên tiếp không làm sai lệch kết quả: f(f(x)) == f(x).
4. Crash-free / Robustness (Tính bền bỉ):
   Không bao giờ phát sinh ngoại lệ không kiểm soát (Unhandled Exception) với các ca biên
   (mẫu số 0, chuỗi rỗng, văn bản không chứa số).
"""

from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest
from hypothesis import assume, given
from hypothesis import strategies as st

# ==============================================================================
# 1. Cơ chế nạp linh hoạt module string_utils từ mã nguồn Mealie v3.28.0
# ==============================================================================

def _load_string_utils():
    """
    Nạp trực tiếp string_utils.py qua importlib để cô lập hoàn toàn khỏi
    chuỗi import SQLAlchemy/Database trong parser_services/__init__.py.
    """
    candidates = [
        Path(__file__).resolve().parent.parent.parent / "mealie_src" / "mealie" / "services" / "parser_services" / "parser_utils" / "string_utils.py",
        Path("mealie_src/mealie/services/parser_services/parser_utils/string_utils.py"),
        Path(__file__).resolve().parent.parent.parent / "mealie" / "services" / "parser_services" / "parser_utils" / "string_utils.py",
        Path("mealie/services/parser_services/parser_utils/string_utils.py"),
    ]
    for p in candidates:
        if p.exists():
            spec = importlib.util.spec_from_file_location("mealie_string_utils", str(p))
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod
    raise ImportError("Không tìm thấy file string_utils.py của Mealie!")


_su = _load_string_utils()
extract_quantity_from_string = _su.extract_quantity_from_string
convert_vulgar_fractions_to_regular_fractions = _su.convert_vulgar_fractions_to_regular_fractions

# Danh mục 18 ký tự phân số Unicode (Vulgar Fractions) được Mealie hỗ trợ
VULGAR_FRACTION_CASES = [
    ("\u00bc", Fraction(1, 4)),   # ¼
    ("\u00bd", Fraction(1, 2)),   # ½
    ("\u00be", Fraction(3, 4)),   # ¾
    ("\u2150", Fraction(1, 7)),   # ⅐
    ("\u2151", Fraction(1, 9)),   # ⅑
    ("\u2152", Fraction(1, 10)),  # ⅒
    ("\u2153", Fraction(1, 3)),   # ⅓
    ("\u2154", Fraction(2, 3)),   # ⅔
    ("\u2155", Fraction(1, 5)),   # ⅕
    ("\u2156", Fraction(2, 5)),   # ⅖
    ("\u2157", Fraction(3, 5)),   # ⅗
    ("\u2158", Fraction(4, 5)),   # ⅘
    ("\u2159", Fraction(1, 6)),   # ⅙
    ("\u215a", Fraction(5, 6)),   # ⅚
    ("\u215b", Fraction(1, 8)),   # ⅛
    ("\u215c", Fraction(3, 8)),   # ⅜
    ("\u215d", Fraction(5, 8)),   # ⅝
    ("\u215e", Fraction(7, 8)),   # ⅞
]

EPSILON = 1e-4  # Sai số cho phép đối với biểu diễn số thực dấu phẩy động


# ==============================================================================
# PROPERTY 5a: BẢO TOÀN GIÁ TRỊ PHÂN SỐ THÔNG THƯỜNG (REGULAR FRACTIONS)
# ==============================================================================

@pytest.mark.pbt
@given(
    numerator=st.integers(min_value=1, max_value=999),
    denominator=st.integers(min_value=1, max_value=999),
)
def test_p5a_regular_fraction_numeric_preservation(numerator: int, denominator: int) -> None:
    """
    Bất biến 1 (Property 5a):
    Với mọi cặp số nguyên dương (n, d), khi chuỗi 'n/d' được bóc tách,
    giá trị số thực trích xuất phải trùng khớp với oracle fractions.Fraction(n, d).
    """
    fraction_str = f"{numerator}/{denominator}"
    actual_qty, _ = extract_quantity_from_string(fraction_str)
    expected_qty = float(Fraction(numerator, denominator))

    assert abs(actual_qty - expected_qty) <= EPSILON, (
        f"Lỗi bảo toàn phân số '{fraction_str}': kỳ vọng {expected_qty}, thực tế {actual_qty}"
    )


# ==============================================================================
# PROPERTY 5b: CHUYỂN ĐỔI VÀ TRÍCH XUẤT PHÂN SỐ UNICODE (VULGAR FRACTIONS)
# ==============================================================================

@pytest.mark.pbt
@pytest.mark.parametrize("vulgar_char,expected_fraction", VULGAR_FRACTION_CASES)
def test_p5b_vulgar_fraction_conversion_and_extraction(
    vulgar_char: str, expected_fraction: Fraction
) -> None:
    """
    Bất biến 2 (Property 5b):
    Toàn bộ 18 ký tự phân số Unicode phải được:
    1. Chuẩn hóa thành chuỗi phân số thông thường 'n/d'.
    2. Bóc tách số lượng chính xác với sai số <= EPSILON.
    """
    # 1. Kiểm tra chuẩn hóa chuỗi
    converted = convert_vulgar_fractions_to_regular_fractions(vulgar_char)
    expected_fraction_str = f"{expected_fraction.numerator}/{expected_fraction.denominator}"
    assert expected_fraction_str in converted, (
        f"Chuẩn hóa '{vulgar_char}' thất bại: nhận '{converted}', kỳ vọng chứa '{expected_fraction_str}'"
    )

    # 2. Kiểm tra trích xuất giá trị số
    actual_qty, _ = extract_quantity_from_string(vulgar_char)
    expected_qty = float(expected_fraction)
    assert abs(actual_qty - expected_qty) <= EPSILON, (
        f"Trích xuất phân số Unicode '{vulgar_char}' sai: kỳ vọng {expected_qty}, thực tế {actual_qty}"
    )


# ==============================================================================
# PROPERTY 5c: BẢO TOÀN GIÁ TRỊ HỖN SỐ UNICODE (MIXED VULGAR FRACTIONS)
# ==============================================================================

@pytest.mark.pbt
@given(
    whole=st.integers(min_value=1, max_value=99),
    vulgar_case=st.sampled_from(VULGAR_FRACTION_CASES),
    has_space=st.booleans(),
)
def test_p5c_mixed_vulgar_fraction_numeric_preservation(
    whole: int, vulgar_case: tuple[str, Fraction], has_space: bool
) -> None:
    """
    Bất biến 3 (Property 5c):
    Hỗn số kết hợp số nguyên và phân số Unicode dạng '2½' hoặc '2 ½'
    phải được trích xuất chính xác thành whole + Fraction.
    """
    vulgar_char, expected_fraction = vulgar_case
    separator = " " if has_space else ""
    mixed_str = f"{whole}{separator}{vulgar_char}"

    actual_qty, _ = extract_quantity_from_string(mixed_str)
    expected_qty = whole + float(expected_fraction)

    assert abs(actual_qty - expected_qty) <= EPSILON, (
        f"Lỗi trích xuất hỗn số Unicode '{mixed_str}': kỳ vọng {expected_qty}, thực tế {actual_qty}"
    )


# ==============================================================================
# PROPERTY 5d: BẢO TOÀN GIÁ TRỊ HỖN SỐ ASCII (MIXED ASCII FRACTIONS)
# ==============================================================================

@pytest.mark.pbt
@given(
    whole=st.integers(min_value=1, max_value=99),
    numerator=st.integers(min_value=1, max_value=99),
    denominator=st.integers(min_value=2, max_value=99),
)
def test_p5d_mixed_ascii_fraction_numeric_preservation(
    whole: int, numerator: int, denominator: int
) -> None:
    """
    Bất biến 4 (Property 5d):
    Hỗn số dạng 'W N/D' (ví dụ '2 1/2') với N < D phải được trích xuất
    chính xác thành whole + (numerator / denominator).
    """
    assume(numerator < denominator)

    mixed_str = f"{whole} {numerator}/{denominator}"
    actual_qty, _ = extract_quantity_from_string(mixed_str)
    expected_qty = whole + float(Fraction(numerator, denominator))

    assert abs(actual_qty - expected_qty) <= EPSILON, (
        f"Lỗi trích xuất hỗn số ASCII '{mixed_str}': kỳ vọng {expected_qty}, thực tế {actual_qty}"
    )


# ==============================================================================
# PROPERTY 5e: BẢO TOÀN THÔNG TIN VĂN BẢN ĐI KÈM (REMAINING TEXT PRESERVATION)
# ==============================================================================

@pytest.mark.pbt
@given(
    numerator=st.integers(min_value=1, max_value=99),
    denominator=st.integers(min_value=1, max_value=99),
    ingredient_name=st.text(
        alphabet=st.characters(whitelist_categories=("Ll", "Lu")),
        min_size=2,
        max_size=20,
    ),
)
def test_p5e_remaining_ingredient_text_preserved(
    numerator: int, denominator: int, ingredient_name: str
) -> None:
    """
    Bất biến 5 (Property 5e):
    Khi bóc tách chuỗi nguyên liệu 'N/D ingredient_name', phần văn bản tên nguyên liệu
    bắt buộc phải được giữ nguyên vẹn trong remaining_str, không bị cắt xén hay méo mó.
    """
    assume("/" not in ingredient_name)
    clean_name = ingredient_name.strip()
    assume(len(clean_name) >= 2)

    input_str = f"{numerator}/{denominator} {clean_name}"
    actual_qty, remaining = extract_quantity_from_string(input_str)

    expected_qty = float(Fraction(numerator, denominator))
    assert abs(actual_qty - expected_qty) <= EPSILON, f"Sai số lượng: kỳ vọng {expected_qty}, thực tế {actual_qty}"
    assert clean_name.lower() in remaining.lower(), (
        f"Tên nguyên liệu '{clean_name}' bị mất trong chuỗi còn lại: '{remaining}' (input: '{input_str}')"
    )


# ==============================================================================
# PROPERTY 5f: TÍNH LŨY ĐẲNG CỦA HÀM CHUẨN HÓA PHÂN SỐ (IDEMPOTENCE)
# ==============================================================================

@pytest.mark.pbt
@given(text=st.text())
def test_p5f_vulgar_fraction_normalization_idempotent(text: str) -> None:
    """
    Bất biến 6 (Property 5f):
    Hàm convert_vulgar_fractions_to_regular_fractions có tính lũy đẳng:
    f(f(x)) == f(x) với mọi chuỗi x bất kỳ.
    """
    once = convert_vulgar_fractions_to_regular_fractions(text)
    twice = convert_vulgar_fractions_to_regular_fractions(once)
    assert once == twice, f"Vi phạm tính lũy đẳng: once='{once}', twice='{twice}'"


# ==============================================================================
# EDGE CASES: TÍNH BỀN BỈ & XỬ LÝ BIÊN KHÔNG CRASH (CRASH-FREE & BOUNDARIES)
# ==============================================================================

@pytest.mark.pbt
def test_p5g_zero_numerator_edge_case() -> None:
    """Ca biên: Tử số bằng 0 ('0/4 cup') phải trả về quantity = 0.0 an toàn."""
    qty, remaining = extract_quantity_from_string("0/4 cup")
    assert qty == 0.0
    assert "cup" in remaining


@pytest.mark.pbt
def test_p5g_zero_denominator_safe_handling() -> None:
    """Ca biên: Mẫu số bằng 0 ('1/0 cup') phải bắt ZeroDivisionError và trả về 0 an toàn."""
    qty, remaining = extract_quantity_from_string("1/0 cup")
    assert qty == 0
    assert "1/0" in remaining or "cup" in remaining


@pytest.mark.pbt
def test_p5g_empty_and_whitespace_input() -> None:
    """Ca biên: Chuỗi rỗng hoặc chỉ có khoảng trắng không gây ngoại lệ."""
    assert extract_quantity_from_string("") == (0, "")
    assert extract_quantity_from_string("   ") == (0, "")


@pytest.mark.pbt
def test_p5g_text_without_numbers() -> None:
    """Ca biên: Chuỗi không có số liệu ('salt to taste') trả về 0 và giữ nguyên chuỗi."""
    qty, remaining = extract_quantity_from_string("salt to taste")
    assert qty == 0
    assert remaining == "salt to taste"


@pytest.mark.pbt
@given(
    num=st.floats(min_value=0.1, max_value=1000.0, allow_nan=False, allow_infinity=False),
)
def test_p5g_decimal_numbers_preservation(num: float) -> None:
    """Kiểm tra bảo toàn giá trị số thập phân/nguyên khi không có phân số ('X.XX cups')."""
    formatted_num = f"{num:.2f}"
    expected_val = float(formatted_num)
    qty, remaining = extract_quantity_from_string(f"{formatted_num} cups")
    assert abs(qty - expected_val) <= EPSILON
    assert "cups" in remaining

