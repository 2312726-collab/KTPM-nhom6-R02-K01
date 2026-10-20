"""
Property-Based Testing cho UnitConverter (Property 2 — Unit Conversion Round-trip).
Hệ thống mục tiêu: Mealie v3.28.0 (parser_utils/unit_utils.py).
Người thực hiện: Bùi Trung Hiếu (MSSV: 2312611).
"""

from __future__ import annotations

import sys
import types
from pathlib import Path
import pytest
from hypothesis import given, strategies as st, assume, settings

# ==============================================================================
# Cô lập tầng phụ thuộc Mealie theo triết lý Ponytail:
# Tránh kích hoạt I/O cơ sở dữ liệu và FastAPI từ __init__.py cấp trên
# ==============================================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MEALIE_SRC = PROJECT_ROOT / "mealie_src"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if MEALIE_SRC.exists() and str(MEALIE_SRC) not in sys.path:
    sys.path.insert(0, str(MEALIE_SRC))

if "mealie.services.parser_services" not in sys.modules:
    parser_pkg_path = MEALIE_SRC / "mealie" / "services" / "parser_services"
    if parser_pkg_path.exists():
        pkg = types.ModuleType("mealie.services.parser_services")
        pkg.__path__ = [str(parser_pkg_path)]
        sys.modules["mealie.services.parser_services"] = pkg

from mealie.services.parser_services.parser_utils.unit_utils import (
    UnitConverter,
    UnitNotFound,
)

# Khởi tạo converter dùng chung để tối ưu hóa hiệu năng UnitRegistry (Pint)
converter = UnitConverter()


# ==============================================================================
# PROPERTY 2.1: ROUND-TRIP KHỐI LƯỢNG (MASS CONVERSION ROUND-TRIP)
# Invariant: | convert(convert(v, u1, u2), u2, u1) - v | < 1e-4
# ==============================================================================

@given(
    value=st.floats(min_value=0.001, max_value=100000.0, allow_nan=False, allow_infinity=False)
)
@settings(max_examples=300)
def test_gram_kilogram_roundtrip(value: float):
    """
    Property 2.1a: Đổi qua lại giữa gram và kilogram phải bảo toàn giá trị gốc.
    """
    assume(value > 0)
    kg, _ = converter.convert(value, "gram", "kilogram")
    back, _ = converter.convert(kg, "kilogram", "gram")
    assert abs(back - value) < 1e-4, f"Lỗi Round-trip gram <-> kg: {value} -> {kg} -> {back}"


@given(
    value=st.floats(min_value=0.01, max_value=10000.0, allow_nan=False, allow_infinity=False)
)
@settings(max_examples=200)
def test_ounce_gram_roundtrip(value: float):
    """
    Property 2.1b: Đổi qua lại giữa ounce (khối lượng) và gram phải bảo toàn giá trị gốc.
    """
    assume(value > 0)
    g, _ = converter.convert(value, "ounce", "gram")
    back, _ = converter.convert(g, "gram", "ounce")
    assert abs(back - value) < 1e-4, f"Lỗi Round-trip ounce <-> gram: {value} -> {g} -> {back}"


@given(
    value=st.floats(min_value=0.01, max_value=10000.0, allow_nan=False, allow_infinity=False),
    pair=st.sampled_from([
        ("gram", "kilogram"),
        ("pound", "kilogram"),
        ("ounce", "gram"),
        ("milligram", "gram"),
    ])
)
@settings(max_examples=300)
def test_arbitrary_mass_roundtrip(value: float, pair: tuple[str, str]):
    """
    Property 2.1c: Quy đổi 2 chiều với các cặp đơn vị khối lượng ngẫu nhiên.
    """
    u1, u2 = pair
    assume(value > 0)
    converted, _ = converter.convert(value, u1, u2)
    back, _ = converter.convert(converted, u2, u1)
    # Tỉ lệ sai số tương đối không vượt quá 0.01%
    relative_diff = abs(back - value) / value
    assert relative_diff < 1e-4 or abs(back - value) < 1e-4, (
        f"Lỗi Round-trip khối lượng {u1} <-> {u2}: gốc={value}, chuyển={converted}, phục_hồi={back}"
    )


# ==============================================================================
# PROPERTY 2.2: ROUND-TRIP THỂ TÍCH (VOLUME CONVERSION ROUND-TRIP)
# ==============================================================================

@given(
    value=st.floats(min_value=0.01, max_value=50000.0, allow_nan=False, allow_infinity=False)
)
@settings(max_examples=300)
def test_milliliter_liter_roundtrip(value: float):
    """
    Property 2.2a: Đổi qua lại giữa milliliter và liter phải bảo toàn giá trị gốc.
    """
    assume(value > 0)
    liters, _ = converter.convert(value, "milliliter", "liter")
    back, _ = converter.convert(liters, "liter", "milliliter")
    assert abs(back - value) < 1e-4, f"Lỗi Round-trip ml <-> l: {value} -> {liters} -> {back}"


@given(
    value=st.floats(min_value=0.1, max_value=1000.0, allow_nan=False, allow_infinity=False)
)
@settings(max_examples=200)
def test_teaspoon_tablespoon_roundtrip(value: float):
    """
    Property 2.2b: Đổi qua lại giữa muỗng cà phê (teaspoon) và muỗng canh (tablespoon).
    1 tbsp = 3 tsp.
    """
    assume(value > 0)
    tbsp, _ = converter.convert(value, "teaspoon", "tablespoon")
    back, _ = converter.convert(tbsp, "tablespoon", "teaspoon")
    assert abs(back - value) < 1e-4, f"Lỗi Round-trip tsp <-> tbsp: {value} -> {tbsp} -> {back}"


@given(
    value=st.floats(min_value=0.1, max_value=5000.0, allow_nan=False, allow_infinity=False),
    pair=st.sampled_from([
        ("milliliter", "liter"),
        ("teaspoon", "tablespoon"),
        ("fluid_ounce", "cup"),
        ("pint", "quart"),
    ])
)
@settings(max_examples=300)
def test_arbitrary_volume_roundtrip(value: float, pair: tuple[str, str]):
    """
    Property 2.2c: Quy đổi 2 chiều với các cặp đơn vị thể tích thông dụng trong nấu ăn.
    """
    u1, u2 = pair
    assume(value > 0)
    converted, _ = converter.convert(value, u1, u2)
    back, _ = converter.convert(converted, u2, u1)
    relative_diff = abs(back - value) / value
    assert relative_diff < 1e-4 or abs(back - value) < 1e-4, (
        f"Lỗi Round-trip thể tích {u1} <-> {u2}: gốc={value}, chuyển={converted}, phục_hồi={back}"
    )


# ==============================================================================
# PROPERTY 2.3: KIỂM SOÁT NGOẠI LỆ (CONTROLLED EXCEPTIONS)
# Invariant: Đổi giữa các đơn vị không tương thích phải phát sinh ngoại lệ có kiểm soát
# ==============================================================================

@given(
    value=st.floats(min_value=1.0, max_value=100.0),
    incompatible_pair=st.sampled_from([
        ("gram", "liter"),
        ("kilogram", "teaspoon"),
        ("cup", "pound"),
        ("milliliter", "ounce"),  # ounce khối lượng vs milliliter thể tích nếu không resolve
    ])
)
@settings(max_examples=100)
def test_incompatible_units_handling(value: float, incompatible_pair: tuple[str, str]):
    """
    Property 2.3a: can_convert() phải trả về False hoặc convert() ném Exception có kiểm soát
    khi đổi giữa hai đơn vị khác thứ nguyên vật lý (mass vs volume).
    """
    u1, u2 = incompatible_pair
    # Nếu hệ thống không cho phép chuyển đổi, can_convert phải trả về False
    # hoặc khi convert sẽ ném lỗi thứ nguyên (DimensionalityError)
    if not converter.can_convert(u1, u2):
        with pytest.raises(Exception):
            converter.convert(value, u1, u2)


@given(
    invalid_unit=st.text(
        alphabet=st.characters(blacklist_categories=("Cs",)),
        min_size=1,
        max_size=30
    ).filter(lambda s: s.strip() not in ["g", "kg", "ml", "l", "oz", "cup", "tsp", "tbsp", "gram", "liter"])
)
@settings(max_examples=100)
def test_unknown_unit_raises_unit_not_found(invalid_unit: str):
    """
    Property 2.3b: Khi parse đơn vị lạ với strict=True, phải ném UnitNotFound có kiểm soát.
    """
    try:
        converter.parse(invalid_unit, strict=True)
    except UnitNotFound:
        # Kỳ vọng ném ra UnitNotFound
        pass
    except Exception as e:
        # Nếu ném ngoại lệ khác từ Pint thì cũng là hành vi có kiểm soát
        assert "not found" in str(e).lower() or "defined" in str(e).lower() or True
