"""
Property-Based Testing cho UnitConverter (Property 2 — Unit Conversion Round-trip).
Hệ thống mục tiêu: Mealie v3.28.0 (parser_utils/unit_utils.py).
Người thực hiện: Bùi Trung Hiếu (MSSV: 2312611).
"""

from __future__ import annotations

from dataclasses import dataclass
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
    merge_quantity_and_unit,
)

# Khởi tạo converter dùng chung để tối ưu hóa hiệu năng UnitRegistry (Pint)
converter = UnitConverter()


@dataclass
class _IngredientUnitStub:
    """Stub tối giản tương thích với thuộc tính runtime của CreateIngredientUnit."""

    name: str
    standard_quantity: float | None
    standard_unit: str | None


# ==============================================================================
# PROPERTY 2.1: ROUND-TRIP KHỐI LƯỢNG (MASS CONVERSION ROUND-TRIP)
# Invariant: | convert(convert(v, u1, u2), u2, u1) - v | < 1e-4
# ==============================================================================

@pytest.mark.pbt
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


@pytest.mark.pbt
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


@pytest.mark.pbt
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

@pytest.mark.pbt
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


@pytest.mark.pbt
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


@pytest.mark.pbt
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

@pytest.mark.pbt
@given(
    value=st.floats(min_value=0.1, max_value=1000.0, allow_nan=False, allow_infinity=False),
    volume_unit=st.sampled_from(["milliliter", "liter", "cup", "teaspoon", "tablespoon"]),
)
@settings(max_examples=150)
def test_ounce_resolves_to_fluid_ounce_with_volume(value: float, volume_unit: str):
    """
    Property 2.2d: Kiểm chứng cơ chế _resolve_ounce() của Mealie:
    Khi đi kèm đơn vị thể tích, 'ounce' được quy ước là 'fluid_ounce' và chuyển đổi 2 chiều hợp lệ.
    """
    assert converter.can_convert("ounce", volume_unit)
    assert converter.can_convert(volume_unit, "ounce")

    vol_val, _ = converter.convert(value, "ounce", volume_unit)
    back_oz, _ = converter.convert(vol_val, volume_unit, "ounce")
    relative_diff = abs(back_oz - value) / value
    assert relative_diff < 1e-4 or abs(back_oz - value) < 1e-4


# ==============================================================================
# PROPERTY 2.3: KIỂM SOÁT NGOẠI LỆ (CONTROLLED EXCEPTIONS)
# Invariant: Đổi giữa các đơn vị không tương thích phải phát sinh ngoại lệ có kiểm soát
# ==============================================================================

@pytest.mark.pbt
@given(
    value=st.floats(min_value=1.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    incompatible_pair=st.sampled_from([
        ("gram", "liter"),
        ("kilogram", "teaspoon"),
        ("cup", "pound"),
        ("milliliter", "kilogram"),
    ])
)
@settings(max_examples=100)
def test_incompatible_units_handling(value: float, incompatible_pair: tuple[str, str]):
    """
    Property 2.3a: can_convert() phải trả về False và convert() bắt buộc ném Exception
    khi đổi giữa hai đơn vị khác thứ nguyên vật lý (mass vs volume).
    """
    u1, u2 = incompatible_pair
    assert not converter.can_convert(u1, u2)
    with pytest.raises(Exception):
        converter.convert(value, u1, u2)


@pytest.mark.pbt
@given(
    suffix=st.text(
        alphabet=st.characters(whitelist_categories=("Ll", "Lu", "Nd"), min_codepoint=48, max_codepoint=122),
        min_size=1,
        max_size=20,
    )
)
@settings(max_examples=100)
def test_unknown_unit_raises_unit_not_found(suffix: str):
    """
    Property 2.3b: Khi parse đơn vị lạ với strict=True phải ném UnitNotFound,
    và với strict=False / can_convert() phải xử lý an toàn không crash.
    """
    invalid_unit = f"unknown_unit_{suffix}"
    assert converter.parse(invalid_unit, strict=False) == invalid_unit
    assert not converter.can_convert(invalid_unit, "gram")
    with pytest.raises(UnitNotFound):
        converter.parse(invalid_unit, strict=True)


# ==============================================================================
# PROPERTY 2.4: TÍNH GIAO HOÁN & BẢO TOÀN ĐẠI LƯỢNG KHI GỘP ĐƠN VỊ (MERGE)
# ==============================================================================

@pytest.mark.pbt
@given(
    q1=st.floats(min_value=0.01, max_value=1000.0, allow_nan=False, allow_infinity=False),
    q2=st.floats(min_value=0.01, max_value=1000.0, allow_nan=False, allow_infinity=False),
    pair=st.sampled_from([
        ("gram", "kilogram"),
        ("milliliter", "liter"),
        ("teaspoon", "tablespoon"),
        ("ounce", "cup"),
    ]),
)
@settings(max_examples=200)
def test_merge_commutativity_and_conservation(q1: float, q2: float, pair: tuple[str, str]):
    """
    Property 2.4a: UnitConverter.merge() phải bảo toàn tổng lượng vật lý và
    bảo toàn tính giao hoán khi quy về cùng đơn vị.
    """
    u1, u2 = pair
    merged_12_q, merged_12_u = converter.merge(q1, u1, q2, u2)
    merged_21_q, merged_21_u = converter.merge(q2, u2, q1, u1)

    # Quy kết quả gộp (u2, u1) về đơn vị merged_12_u để so sánh giao hoán
    merged_21_in_12, _ = converter.convert(merged_21_q, merged_21_u, merged_12_u)
    assert abs(merged_12_q - merged_21_in_12) / max(merged_12_q, 1e-9) < 1e-4

    # Đối chiếu tổng vật lý bằng cách quy đổi riêng q2 từ u2 sang u1
    q2_in_u1, _ = converter.convert(q2, u2, u1)
    expected_in_u1 = q1 + q2_in_u1
    actual_in_u1, _ = converter.convert(merged_12_q, merged_12_u, u1)
    assert abs(actual_in_u1 - expected_in_u1) / max(expected_in_u1, 1e-9) < 1e-4


@pytest.mark.pbt
@given(
    q1=st.floats(min_value=0.01, max_value=500.0, allow_nan=False, allow_infinity=False),
    q2=st.floats(min_value=0.01, max_value=500.0, allow_nan=False, allow_infinity=False),
    pair=st.sampled_from([
        ("gram", 1.0, "kilogram", 1.0),
        ("milliliter", 1.0, "liter", 1.0),
        ("teaspoon", 1.0, "tablespoon", 1.0),
    ]),
)
@settings(max_examples=150)
def test_merge_quantity_and_unit_preserves_total(
    q1: float,
    q2: float,
    pair: tuple[str, float, str, float],
):
    """
    Property 2.4b: merge_quantity_and_unit() phải bảo toàn tổng đại lượng vật lý
    và chọn đơn vị lớn hơn nếu tổng >= 1 (ngược lại chọn đơn vị nhỏ hơn).
    """
    u1_name, u1_std_qty, u2_name, u2_std_qty = pair
    unit_1 = _IngredientUnitStub(name=u1_name, standard_quantity=u1_std_qty, standard_unit=u1_name)
    unit_2 = _IngredientUnitStub(name=u2_name, standard_quantity=u2_std_qty, standard_unit=u2_name)

    merged_q, merged_unit = merge_quantity_and_unit(q1, unit_1, q2, unit_2)
    assert merged_unit in (unit_1, unit_2)

    q2_in_u1, _ = converter.convert(q2 * u2_std_qty, u2_name, u1_name)
    expected_in_u1 = q1 * u1_std_qty + q2_in_u1
    actual_in_u1, _ = converter.convert(
        merged_q * (merged_unit.standard_quantity or 1.0),
        merged_unit.standard_unit or u1_name,
        u1_name,
    )
    assert abs(actual_in_u1 - expected_in_u1) / max(expected_in_u1, 1e-9) < 1e-4


@pytest.mark.pbt
@given(
    missing_qty=st.sampled_from([None, 0.0]),
)
@settings(max_examples=10)
def test_merge_quantity_and_unit_invalid_metadata_raises_value_error(missing_qty: float | None):
    """
    Property 2.4c: merge_quantity_and_unit() phải ném ValueError khi thiếu standard_quantity/standard_unit.
    """
    valid_unit = _IngredientUnitStub(name="gram", standard_quantity=1.0, standard_unit="gram")
    invalid_unit = _IngredientUnitStub(name="broken", standard_quantity=missing_qty, standard_unit="gram")

    with pytest.raises(ValueError):
        merge_quantity_and_unit(1.0, invalid_unit, 1.0, valid_unit)


@pytest.mark.unit
def test_private_registry_and_parsed_unit_idempotence():
    """Kiểm tra UnitConverter(private_registry=True) và parse() với pint.Unit đã parse sẵn."""
    private_conv = UnitConverter(private_registry=True)
    parsed = private_conv.parse("gram", strict=True)
    assert private_conv.parse(parsed, strict=True) is parsed
