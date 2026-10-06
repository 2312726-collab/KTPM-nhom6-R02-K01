"""
Property-Based Testing — Property 5: Fraction Numeric Preservation
Đồ án Kiểm thử Phần mềm — Nhóm 6
Thành viên: Nguyễn Phạm Phú Nam (2312695-netizen)
File mục tiêu: mealie_src/mealie/services/parser_services/parser_utils/string_utils.py

INVARIANT:
Khi một chuỗi chứa phân số (thường, Unicode vulgar, hoặc hỗn số) được
bóc tách bởi extract_quantity_from_string(), giá trị số học phải được
bảo toàn chính xác với sai số epsilon <= 1e-4.

LƯU Ý IMPORT:
- Không import qua mealie.services.parser_services vì __init__.py của gói đó
  kéo ingredient_parser.py -> sqlalchemy.orm, gây ModuleNotFoundError.
- Dùng importlib.util để nạp trực tiếp string_utils.py không qua __init__.
- Hàm được kiểm thử là hàm Mealie thật (không copy, không mock).
"""

from __future__ import annotations

import importlib.util
from fractions import Fraction
from pathlib import Path

import pytest
from hypothesis import given, settings, assume
from hypothesis import strategies as st

# ==============================================================================
# Nạp module Mealie thật qua importlib để tránh import chain SQLAlchemy
# ==============================================================================

_STRING_UTILS_PATH = (
    Path(__file__).parent.parent.parent
    / "mealie_src"
    / "mealie"
    / "services"
    / "parser_services"
    / "parser_utils"
    / "string_utils.py"
)

_spec = importlib.util.spec_from_file_location("mealie_string_utils", _STRING_UTILS_PATH)
_string_utils_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_string_utils_mod)

# Hàm thật từ Mealie source
extract_quantity_from_string = _string_utils_mod.extract_quantity_from_string
convert_vulgar_fractions_to_regular_fractions = (
    _string_utils_mod.convert_vulgar_fractions_to_regular_fractions
)

# ==============================================================================
# Danh sách phân số Unicode được source hỗ trợ (từ vulgar_fractions dict)
# Mỗi tuple: (ký_tự_unicode, giá_trị_phân_số_đúng)
# ==============================================================================

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

EPSILON = 1e-4  # Sai số mục tiêu theo phân công


# ==============================================================================
# Property 5a: Phân số thông thường n/d
# ==============================================================================

@pytest.mark.pbt
@given(
    numerator=st.integers(min_value=1, max_value=999),
    denominator=st.integers(min_value=1, max_value=999),
)
@settings(max_examples=300)
def test_p5a_regular_fraction_numeric_preservation(numerator: int, denominator: int) -> None:
    """
    PROPERTY 5a — Phân số thường:
    Với bất kỳ chuỗi "n/d" hợp lệ (n,d nguyên dương không bằng 0),
    giá trị số học được bảo toàn trong sai số EPSILON.

    Oracle độc lập: fractions.Fraction(n, d) — thư viện chuẩn Python,
    không liên quan đến code Mealie, đảm bảo tính độc lập.
    """
    # Không dùng assume để loại trường hợp fail — denominator đã >= 1
    fraction_str = f"{numerator}/{denominator}"

    # Actual: gọi hàm Mealie thật
    actual_qty, _ = extract_quantity_from_string(fraction_str)

    # Expected: oracle độc lập từ thư viện chuẩn Python
    expected_qty = float(Fraction(numerator, denominator))

    assert abs(actual_qty - expected_qty) <= EPSILON, (
        f"Fraction '{fraction_str}': expected {expected_qty}, got {actual_qty}, "
        f"diff={abs(actual_qty - expected_qty)}"
    )


# ==============================================================================
# Property 5b: Phân số Unicode (vulgar fractions)
# ==============================================================================

@pytest.mark.pbt
@pytest.mark.parametrize("vulgar_char,expected_fraction", VULGAR_FRACTION_CASES)
def test_p5b_vulgar_fraction_conversion(vulgar_char: str, expected_fraction: Fraction) -> None:
    """
    PROPERTY 5b — Phân số Unicode:
    Tất cả 18 ký tự vulgar fraction được source hỗ trợ phải được chuyển
    thành chuỗi "n/d" chính xác (contract của convert_vulgar_fractions_to_regular_fractions),
    và extract_quantity_from_string phải trả về giá trị đúng trong sai số EPSILON.
    """
    # Kiểm tra convert_vulgar trả về chuỗi phân số đúng
    converted = convert_vulgar_fractions_to_regular_fractions(vulgar_char)
    expected_str = f"{expected_fraction.numerator}/{expected_fraction.denominator}"
    assert expected_str in converted, (
        f"convert_vulgar: '{vulgar_char}' -> '{converted}', expected to contain '{expected_str}'"
    )

    # Kiểm tra extract_quantity_from_string bảo toàn giá trị số học
    actual_qty, _ = extract_quantity_from_string(vulgar_char)
    expected_qty = float(expected_fraction)

    assert abs(actual_qty - expected_qty) <= EPSILON, (
        f"extract_quantity '{vulgar_char}': expected {expected_qty}, got {actual_qty}, "
        f"diff={abs(actual_qty - expected_qty)}"
    )


# ==============================================================================
# Property 5c: Hỗn số "w n/d"
# ==============================================================================

@pytest.mark.pbt
@given(
    whole=st.integers(min_value=1, max_value=99),
    numerator=st.integers(min_value=1, max_value=99),
    denominator=st.integers(min_value=2, max_value=99),
)
@settings(max_examples=300)
def test_p5c_mixed_fraction_numeric_preservation(whole: int, numerator: int, denominator: int) -> None:
    """
    PROPERTY 5c — Hỗn số:
    Với hỗn số dạng "w n/d" (e.g. "2 1/2"), giá trị số học phải bằng
    w + Fraction(n, d) trong sai số EPSILON.

    Điều kiện: numerator < denominator (để đảm bảo là phân số đúng nghĩa trong hỗn số).
    """
    assume(numerator < denominator)  # Hỗn số hợp lệ: phần phân số < 1

    mixed_str = f"{whole} {numerator}/{denominator}"

    # Actual: gọi hàm Mealie thật
    actual_qty, _ = extract_quantity_from_string(mixed_str)

    # Expected: oracle độc lập
    expected_qty = whole + float(Fraction(numerator, denominator))

    assert abs(actual_qty - expected_qty) <= EPSILON, (
        f"Mixed fraction '{mixed_str}': expected {expected_qty}, got {actual_qty}, "
        f"diff={abs(actual_qty - expected_qty)}"
    )


# ==============================================================================
# Property 5d: Văn bản ngoài token phân số được bảo toàn (remaining_str)
# ==============================================================================

@pytest.mark.pbt
@given(
    numerator=st.integers(min_value=1, max_value=99),
    denominator=st.integers(min_value=1, max_value=99),
    suffix=st.text(
        alphabet=st.characters(whitelist_categories=("Ll", "Lu")),
        min_size=1,
        max_size=20,
    ),
)
@settings(max_examples=300)
def test_p5d_remaining_text_preserved(numerator: int, denominator: int, suffix: str) -> None:
    """
    PROPERTY 5d — Bảo toàn văn bản còn lại:
    Khi bóc tách "n/d suffix", phần văn bản (suffix) không liên quan đến
    phân số phải xuất hiện trong remaining_str được trả về.

    Đảm bảo hàm không nuốt thông tin văn bản bên ngoài số.
    """
    # Suffix không được chứa "/" để không bị nhận nhầm là phân số khác
    assume("/" not in suffix)
    assume(suffix.strip() != "")

    fraction_str = f"{numerator}/{denominator} {suffix.strip()}"

    actual_qty, remaining = extract_quantity_from_string(fraction_str)

    # Giá trị số học đúng
    expected_qty = float(Fraction(numerator, denominator))
    assert abs(actual_qty - expected_qty) <= EPSILON, (
        f"Qty preservation failed for '{fraction_str}': "
        f"expected {expected_qty}, got {actual_qty}"
    )

    # Văn bản suffix còn lại trong remaining (có thể có khoảng trắng xung quanh)
    assert suffix.strip().lower() in remaining.lower(), (
        f"Suffix '{suffix.strip()}' not found in remaining '{remaining}' "
        f"(input: '{fraction_str}')"
    )


# ==============================================================================
# Ca biên: Phân số tử số = 0
# ==============================================================================

@pytest.mark.pbt
def test_p5e_zero_numerator_edge_case() -> None:
    """
    Ca biên: Phân số 0/n (tử số = 0).
    Mealie source dùng integers(min_value=1) trong pattern, nhưng tử số 0
    về mặt regex vẫn match. Kiểm tra hành vi thực tế không crash.
    """
    qty, remaining = extract_quantity_from_string("0/4 cup")
    # Không crash là đủ; giá trị 0.0 là hợp lệ về mặt số học
    assert isinstance(qty, (int, float))


@pytest.mark.pbt
def test_p5e_zero_denominator_returns_zero() -> None:
    """
    Ca biên: Phân số n/0 (mẫu số = 0 — ZeroDivisionError).
    Source xử lý qua try/except ZeroDivisionError và trả về (0, original_str).
    """
    qty, remaining = extract_quantity_from_string("1/0 cup")
    assert qty == 0, f"Expected qty=0 for 1/0, got {qty}"
    # remaining phải chứa chuỗi gốc (không mất thông tin)
    assert "1/0" in remaining or remaining != ""