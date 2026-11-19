"""
File: tests/unit_tests/test_pbt_scaling.py
Kịch bản kiểm thử Property-Based Testing (PBT) cho Nghiệp vụ Nhân chia tỉ lệ khẩu phần ăn (Servings Scaling).
Thực hiện bởi: Trần Quốc Quân (MSSV: 2312726) — Trưởng nhóm / QA Automation Engineer
Hệ thống mục tiêu: Mealie v3.28.0 (mealie/services/recipe/ & mealie/schema/recipe/recipe_ingredient.py)
Đặc tả nhiệm vụ: Property 4 — Tính đơn điệu & Bảo toàn tỉ lệ nhân khẩu phần (Servings Scaling Monotonicity & Reversibility)
"""

from __future__ import annotations

import math
from fractions import Fraction
from typing import Any
import pytest
from hypothesis import given, strategies as st, assume, settings

# ==============================================================================
# 1. HỆ THỐNG HÀM NGHIỆP VỤ SCALING ENGINE (THEO CHUẨN THUẬT TOÁN MEALIE)
# ==============================================================================

INGREDIENT_QTY_PRECISION = 3
MAX_INGREDIENT_DENOMINATOR = 32

SUPERSCRIPT = dict(zip("1234567890", "¹²³⁴⁵⁶⁷⁸⁹⁰", strict=False))
SUBSCRIPT = dict(zip("1234567890", "₁₂₃₄₅₆₇₈₉₀", strict=False))


def display_fraction(fraction: Fraction) -> str:
    """Format phân số theo ký tự Unicode thượng/hạ chuẩn Mealie."""
    return (
        "".join([SUPERSCRIPT[c] for c in str(fraction.numerator)])
        + "/"
        + "".join([SUBSCRIPT[c] for c in str(fraction.denominator)])
    )


def calculate_scale_factor(target_servings: float, base_servings: float) -> float:
    """
    Tính toán hệ số co giãn k = target_servings / base_servings.
    Ném ngoại lệ ValueError nếu khẩu phần cơ sở <= 0 hoặc khẩu phần đích < 0.
    """
    if base_servings <= 0:
        raise ValueError(f"Khẩu phần cơ sở (base_servings) phải > 0, nhận được: {base_servings}")
    if target_servings < 0:
        raise ValueError(f"Khẩu phần đích (target_servings) không được âm, nhận được: {target_servings}")
    return target_servings / base_servings


def scale_quantity(
    quantity: float | None,
    target_servings: float,
    base_servings: float,
) -> float | None:
    """
    Scale số lượng nguyên liệu theo tỉ lệ giữa khẩu phần đích và khẩu phần cơ sở.
    Nếu nguyên liệu không định lượng (quantity is None), giữ nguyên None.
    """
    if quantity is None:
        return None
    if quantity < 0:
        raise ValueError(f"Số lượng nguyên liệu không được âm: {quantity}")

    factor = calculate_scale_factor(target_servings, base_servings)
    return quantity * factor


def scale_by_factor(quantity: float | None, factor: float) -> float | None:
    """Scale số lượng nguyên liệu trực tiếp theo hệ số nhân factor."""
    if quantity is None:
        return None
    if quantity < 0:
        raise ValueError(f"Số lượng nguyên liệu không được âm: {quantity}")
    if factor < 0:
        raise ValueError(f"Hệ số scale không được âm: {factor}")
    return quantity * factor


def revert_scale(scaled_quantity: float | None, factor: float) -> float | None:
    """Phục hồi số lượng nguyên liệu ban đầu bằng phép chia nghịch đảo factor."""
    if scaled_quantity is None:
        return None
    if factor <= 0:
        raise ValueError(f"Hệ số scale nghịch đảo phải > 0: {factor}")
    return scaled_quantity / factor


def format_scaled_quantity_for_display(quantity: float | None, as_fraction: bool = True) -> str:
    """
    Mô phỏng chính xác thuật toán định dạng hiển thị nguyên liệu của Mealie:
    RecipeIngredientBase._format_quantity_for_display().
    """
    if quantity is None or quantity == 0:
        return "0"

    if not as_fraction:
        qty_dec = round(quantity, INGREDIENT_QTY_PRECISION)
        return str(int(qty_dec)) if qty_dec.is_integer() else str(qty_dec)

    qty_frac = Fraction(quantity).limit_denominator(MAX_INGREDIENT_DENOMINATOR)
    if qty_frac.denominator == 1:
        return str(qty_frac.numerator)

    if qty_frac.numerator <= qty_frac.denominator:
        return display_fraction(qty_frac)

    # Hỗn số (ví dụ: 11/4 -> 2 3/4)
    whole = qty_frac.numerator // qty_frac.denominator
    remainder = Fraction(qty_frac.numerator % qty_frac.denominator, qty_frac.denominator)
    return f"{whole} {display_fraction(remainder)}"


# ==============================================================================
# 2. CÁC CHIẾN LƯỢC SINH MẪU (HYPOTHESIS STRATEGIES)
# ==============================================================================

# Strategy sinh số lượng nguyên liệu thực tế (0.01 đến 10,000.0)
st_qty = st.floats(min_value=0.01, max_value=10000.0, allow_nan=False, allow_infinity=False)

# Strategy sinh hệ số nhân khẩu phần (0.05x đến 50.0x)
st_scale = st.floats(min_value=0.05, max_value=50.0, allow_nan=False, allow_infinity=False)

# Strategy sinh số phần ăn người dùng nhập thực tế (1 đến 200 người)
st_servings = st.integers(min_value=1, max_value=200)

# Strategy sinh nguyên liệu công thức nấu ăn tổng quát
st_ingredient = st.fixed_dictionaries({
    "name": st.text(min_size=1, max_size=30).filter(lambda x: x.strip() != ""),
    "quantity": st.one_of(st.none(), st_qty),
    "unit": st.sampled_from(["gram", "ml", "cup", "tbsp", "tsp", "kg", "piece"]),
})


# ==============================================================================
# 3. PROPERTY 4.1: TÍNH ĐƠN ĐIỆU KHI NHÂN KHẨU PHẦN (STRICT MONOTONICITY)
# Invariant:
#   k > 1.0  ==> Q_scaled >= Q
#   k == 1.0 ==> Q_scaled == Q
#   0 < k < 1.0 ==> Q_scaled <= Q
# ==============================================================================

@pytest.mark.pbt
@given(qty=st_qty, factor=st_scale)
@settings(max_examples=300)
def test_servings_scaling_monotonicity_by_factor(qty: float, factor: float):
    """
    Property 4.1.1: Tính đơn điệu nghiêm ngặt khi scale số lượng bằng factor.
    Tăng khẩu phần (factor > 1) không bao giờ làm giảm lượng nguyên liệu.
    Giảm khẩu phần (factor < 1) không bao giờ làm tăng lượng nguyên liệu.
    """
    assume(qty > 0 and factor > 0)

    scaled = scale_by_factor(qty, factor)
    assert scaled is not None

    if factor > 1.0:
        assert scaled >= qty, f"Hệ số {factor} > 1 nhưng lượng scale ({scaled}) < lượng gốc ({qty})"
    elif factor < 1.0:
        assert scaled <= qty, f"Hệ số {factor} < 1 nhưng lượng scale ({scaled}) > lượng gốc ({qty})"
    else:
        assert math.isclose(scaled, qty, rel_tol=1e-7), f"Hệ số = 1 nhưng {scaled} != {qty}"


@pytest.mark.pbt
@given(qty=st_qty, base_servings=st_servings, target_servings=st_servings)
@settings(max_examples=300)
def test_servings_scaling_monotonicity_by_servings(qty: float, base_servings: int, target_servings: int):
    """
    Property 4.1.2: Tính đơn điệu dựa trên số phần ăn thực tế người dùng nhập.
    Nếu target_servings > base_servings ==> Q_scaled >= Q.
    Nếu target_servings < base_servings ==> Q_scaled <= Q.
    """
    scaled = scale_quantity(qty, target_servings=target_servings, base_servings=base_servings)
    assert scaled is not None

    if target_servings > base_servings:
        assert scaled >= qty, f"Target {target_servings} > Base {base_servings} nhưng {scaled} < {qty}"
    elif target_servings < base_servings:
        assert scaled <= qty, f"Target {target_servings} < Base {base_servings} nhưng {scaled} > {qty}"
    else:
        assert math.isclose(scaled, qty, rel_tol=1e-7), f"Khẩu phần không đổi nhưng {scaled} != {qty}"


# ==============================================================================
# 4. PROPERTY 4.2: TÍNH BẢO TOÀN NGHỊCH ĐẢO HAI CHIỀU (REVERSIBILITY ROUND-TRIP)
# Invariant: | revert(scale(Q, k), k) - Q | <= 1e-4
# ==============================================================================

@pytest.mark.pbt
@given(qty=st_qty, factor=st_scale)
@settings(max_examples=300)
def test_servings_scaling_reversibility_roundtrip(qty: float, factor: float):
    """
    Property 4.2.1: Khi scale khẩu phần rồi phục hồi ngược lại, giá trị
    thu được phải bằng giá trị ban đầu trong phạm vi sai số epsilon <= 1e-4.
    """
    assume(qty > 0 and factor > 0)

    scaled = scale_by_factor(qty, factor)
    assert scaled is not None

    reverted = revert_scale(scaled, factor)
    assert reverted is not None

    epsilon = 1e-4
    diff = abs(reverted - qty)
    assert diff <= epsilon, (
        f"Vi phạm tính bảo toàn nghịch đảo: Gốc={qty}, Factor={factor}, "
        f"Scaled={scaled}, Phục hồi={reverted}, Độ lệch={diff} > {epsilon}"
    )


@pytest.mark.pbt
@given(qty=st_qty, base_servings=st_servings, target_servings=st_servings)
@settings(max_examples=300)
def test_servings_scaling_reversibility_by_servings(qty: float, base_servings: int, target_servings: int):
    """
    Property 4.2.2: Round-trip giữa 2 khẩu phần bất kỳ:
    Scale từ Base -> Target -> Base phải trả về chính xác số lượng gốc.
    """
    # Chiều đi: Base -> Target
    scaled = scale_quantity(qty, target_servings=target_servings, base_servings=base_servings)
    assert scaled is not None

    # Chiều về: Target -> Base
    reverted = scale_quantity(scaled, target_servings=base_servings, base_servings=target_servings)
    assert reverted is not None

    assert math.isclose(reverted, qty, rel_tol=1e-4, abs_tol=1e-4), (
        f"Lệch round-trip qua khẩu phần: Gốc={qty}, Base={base_servings}, "
        f"Target={target_servings}, Phục hồi={reverted}"
    )


# ==============================================================================
# 5. PROPERTY 4.3: TÍNH BẮC CẦU VÀ KẾT HỢP (TRANSITIVITY / COMPOSITION)
# Invariant: | scale(scale(Q, k1), k2) - scale(Q, k1 * k2) | <= 1e-4
# ==============================================================================

@pytest.mark.pbt
@given(
    qty=st_qty,
    factor1=st.floats(min_value=0.2, max_value=5.0, allow_nan=False, allow_infinity=False),
    factor2=st.floats(min_value=0.2, max_value=5.0, allow_nan=False, allow_infinity=False),
)
@settings(max_examples=300)
def test_servings_scaling_transitivity(qty: float, factor1: float, factor2: float):
    """
    Property 4.3: Scale 2 lần liên tiếp (k1 rồi k2) phải tương đương với
    scale 1 lần duy nhất theo hệ số tích (k1 * k2).
    """
    assume(qty > 0 and factor1 > 0 and factor2 > 0)

    # Scale từng bước: S_1 -> S_2 -> S_3
    step1 = scale_by_factor(qty, factor1)
    step2 = scale_by_factor(step1, factor2)

    # Scale gộp một lần
    combined_factor = factor1 * factor2
    direct = scale_by_factor(qty, combined_factor)

    assert step2 is not None and direct is not None
    assert math.isclose(step2, direct, rel_tol=1e-4, abs_tol=1e-4), (
        f"Vi phạm tính kết hợp: Scale 2 bước={step2}, Scale gộp={direct}, "
        f"Lệch={abs(step2 - direct)}"
    )


# ==============================================================================
# 6. PROPERTY 4.4: BẢO TOÀN DANH SÁCH NGUYÊN LIỆU TRONG CÔNG THỨC (LIST HOMOGENEITY)
# Invariant:
#   len(scaled_list) == len(original_list)
#   Mọi nguyên liệu có định lượng đều được nhân đúng factor
#   Nguyên liệu không định lượng (None) được giữ nguyên None
# ==============================================================================

@pytest.mark.pbt
@given(
    ingredients=st.lists(st_ingredient, min_size=1, max_size=20),
    factor=st_scale,
)
@settings(max_examples=200)
def test_recipe_ingredients_batch_scaling_preservation(ingredients: list[dict[str, Any]], factor: float):
    """
    Property 4.4: Khi scale toàn bộ danh sách nguyên liệu của một Recipe:
    1. Số lượng phần tử danh sách không đổi (Length invariant).
    2. Tên và đơn vị của từng nguyên liệu không bị xáo trộn.
    3. Nguyên liệu không định lượng (None) vẫn là None.
    4. Nguyên liệu có định lượng được scale đồng nhất theo factor.
    """
    scaled_list = []
    for ing in ingredients:
        scaled_ing = dict(ing)
        scaled_ing["quantity"] = scale_by_factor(ing["quantity"], factor)
        scaled_list.append(scaled_ing)

    # 1. Bảo toàn độ dài
    assert len(scaled_list) == len(ingredients)

    # 2. Kiểm tra từng nguyên liệu
    for orig, scld in zip(ingredients, scaled_list, strict=True):
        assert orig["name"] == scld["name"], "Tên nguyên liệu bị biến dạng khi scale"
        assert orig["unit"] == scld["unit"], "Đơn vị nguyên liệu bị thay đổi khi scale"

        if orig["quantity"] is None:
            assert scld["quantity"] is None, "Nguyên liệu None bị gán giá trị sau khi scale"
        else:
            expected = orig["quantity"] * factor
            assert math.isclose(scld["quantity"], expected, rel_tol=1e-5), (
                f"Nguyên liệu {orig['name']}: Kỳ vọng {expected}, thực tế {scld['quantity']}"
            )


# ==============================================================================
# 7. PROPERTY 4.5: XỬ LÝ AN TOÀN CA BIÊN & DỮ LIỆU ĐẶC BIỆT (BOUNDARY & ROBUSTNESS)
# Invariant:
#   Zero Quantity: 0 * k == 0
#   Base Servings <= 0 ==> ValueError (không ZeroDivisionError unhandled)
#   Target Servings < 0 ==> ValueError
#   Extreme Scaling (0.001x, 1000.0x) ==> Không sinh NaN, không tràn số
# ==============================================================================

@pytest.mark.pbt
@given(factor=st_scale)
def test_zero_quantity_scaling(factor: float):
    """Property 4.5.1: Nguyên liệu với số lượng bằng 0 (nêm nếm) scale vẫn bằng 0."""
    scaled = scale_by_factor(0.0, factor)
    assert scaled == 0.0


@pytest.mark.pbt
@given(
    invalid_base=st.floats(max_value=0.0, allow_nan=False, allow_infinity=False),
    target=st.floats(min_value=1.0, max_value=20.0, allow_nan=False, allow_infinity=False),
)
def test_invalid_base_servings_raises_value_error(invalid_base: float, target: float):
    """Property 4.5.2: Khẩu phần cơ sở <= 0 phải ném ValueError có kiểm soát."""
    with pytest.raises(ValueError, match="base_servings"):
        calculate_scale_factor(target, invalid_base)


@pytest.mark.pbt
@given(
    base=st.floats(min_value=1.0, max_value=20.0, allow_nan=False, allow_infinity=False),
    invalid_target=st.floats(max_value=-0.0001, allow_nan=False, allow_infinity=False),
)
def test_negative_target_servings_raises_value_error(base: float, invalid_target: float):
    """Property 4.5.3: Khẩu phần đích < 0 phải ném ValueError có kiểm soát."""
    with pytest.raises(ValueError, match="target_servings"):
        calculate_scale_factor(invalid_target, base)


@pytest.mark.pbt
@given(
    qty=st.floats(min_value=1e-3, max_value=1e5, allow_nan=False, allow_infinity=False),
    extreme_factor=st.sampled_from([0.001, 0.01, 100.0, 1000.0]),
)
def test_extreme_scaling_numerical_stability(qty: float, extreme_factor: float):
    """Property 4.5.4: Scale ở các hệ số cực đoan không sinh NaN hay Infinity."""
    scaled = scale_by_factor(qty, extreme_factor)
    assert scaled is not None
    assert not math.isnan(scaled)
    assert not math.isinf(scaled)
    assert scaled > 0


# ==============================================================================
# 8. PROPERTY 4.6: BẢO TOÀN ĐỊNH DẠNG HIỂN THỊ SAU KHI SCALE (DISPLAY INTEGRATION)
# Invariant: Format chuỗi hiển thị không bao giờ rỗng và không gây sập runtime
# ==============================================================================

@pytest.mark.pbt
@given(qty=st_qty, factor=st_scale, as_fraction=st.booleans())
@settings(max_examples=200)
def test_display_formatting_after_scaling_robustness(qty: float, factor: float, as_fraction: bool):
    """
    Property 4.6: Số lượng sau khi scale khi đi qua hàm định dạng hiển thị
    (chuẩn Unicode hoặc thập phân của Mealie) luôn trả về chuỗi hợp lệ,
    không rỗng và không bao giờ gây sập runtime (Crash-free).
    """
    scaled = scale_by_factor(qty, factor)
    assert scaled is not None

    formatted = format_scaled_quantity_for_display(scaled, as_fraction=as_fraction)

    assert isinstance(formatted, str)
    assert len(formatted.strip()) > 0
    # Chuỗi hiển thị không được chứa các giá trị lỗi chuỗi đặc biệt
    assert "nan" not in formatted.lower()
    assert "inf" not in formatted.lower()
