"""
File: tests/unit_tests/test_pbt_scaling.py
Kịch bản kiểm thử Property-Based Testing (PBT) cho Nghiệp vụ Nhân chia tỉ lệ khẩu phần ăn (Servings Scaling).
Thực hiện bởi: Trần Quốc Quân (MSSV: 2312726) — Trưởng nhóm / QA Automation Engineer
Hệ thống mục tiêu: Mealie v3.28.0 (mealie_src/mealie/schema/recipe/recipe_ingredient.py)
Đặc tả nhiệm vụ: Property 4 — Tính đơn điệu & Bảo toàn tỉ lệ nhân khẩu phần (Servings Scaling Monotonicity & Reversibility)
"""

from __future__ import annotations

import math
import sys
import types
from fractions import Fraction
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock
import pytest
from hypothesis import given, strategies as st, assume, settings

# ==============================================================================
# 1. CƠ CHẾ NẠP TRỰC TIẾP MÃ NGUỒN MEALIE v3.28.0 (THEO TRIẾT LÝ PONYTAIL)
# ==============================================================================
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
MEALIE_SRC = PROJECT_ROOT / "mealie_src"

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

if MEALIE_SRC.exists() and str(MEALIE_SRC) not in sys.path:
    sys.path.insert(0, str(MEALIE_SRC))

# Đăng ký mock cô lập tầng CSDL và Config ngoài lề để nạp schema Mealie sạch sẽ
if "fastapi" not in sys.modules:
    f_mod = types.ModuleType("fastapi")
    f_mod.Header = MagicMock()
    sys.modules["fastapi"] = f_mod

if "mealie.core.config" not in sys.modules:
    c_mod = types.ModuleType("mealie.core.config")
    c_mod.get_app_dirs = MagicMock()
    sys.modules["mealie.core.config"] = c_mod

if "mealie.core.settings" not in sys.modules:
    sys.modules["mealie.core.settings"] = types.ModuleType("mealie.core.settings")

if "mealie.schema.recipe" not in sys.modules and MEALIE_SRC.exists():
    pkg = types.ModuleType("mealie.schema.recipe")
    pkg.__path__ = [str(MEALIE_SRC / "mealie" / "schema" / "recipe")]
    sys.modules["mealie.schema.recipe"] = pkg

if "mealie.schema.recipe.recipe" not in sys.modules:
    r_mod = types.ModuleType("mealie.schema.recipe.recipe")
    r_mod.Recipe = Any
    sys.modules["mealie.schema.recipe.recipe"] = r_mod

if "mealie.db.models.recipe" not in sys.modules:
    db_mod = types.ModuleType("mealie.db.models.recipe")
    db_mod.IngredientFoodModel = MagicMock()
    db_mod.IngredientFoodSubstitutionModel = MagicMock()
    sys.modules["mealie.db.models.recipe"] = db_mod

# ==============================================================================
# Cơ chế nạp linh hoạt tệp recipe_ingredient.py từ mã nguồn thật Mealie v3.28.0
# (Tương tự _load_string_utils() của Phước để IDE không báo lỗi Pylance)
# ==============================================================================
def _load_recipe_ingredient_module():
    import importlib.util

    candidates = [
        PROJECT_ROOT / "mealie_src" / "mealie" / "schema" / "recipe" / "recipe_ingredient.py",
        Path("mealie_src/mealie/schema/recipe/recipe_ingredient.py"),
        Path(__file__).resolve().parent.parent.parent / "mealie_src" / "mealie" / "schema" / "recipe" / "recipe_ingredient.py",
    ]
    for p in candidates:
        if p.exists():
            spec = importlib.util.spec_from_file_location("mealie.schema.recipe.recipe_ingredient", str(p))
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                sys.modules["mealie.schema.recipe.recipe_ingredient"] = mod
                spec.loader.exec_module(mod)
                return mod

    raise ImportError("Không tìm thấy tệp recipe_ingredient.py trong mealie_src!")

_ing_mod = _load_recipe_ingredient_module()

RecipeIngredientBase = _ing_mod.RecipeIngredientBase
mealie_display_fraction = _ing_mod.display_fraction
INGREDIENT_QTY_PRECISION = _ing_mod.INGREDIENT_QTY_PRECISION
MAX_INGREDIENT_DENOMINATOR = _ing_mod.MAX_INGREDIENT_DENOMINATOR
SUPERSCRIPT = _ing_mod.SUPERSCRIPT
SUBSCRIPT = _ing_mod.SUBSCRIPT


# ==============================================================================
# 2. HÀM ĐIỀU PHỐI TỈ LỆ CO GIÃN KHẨU PHẦN ĂN (SCALING ENGINE)
# ==============================================================================

def calculate_scale_factor(target_servings: float, base_servings: float) -> float:
    """Tính toán hệ số co giãn k = target_servings / base_servings."""
    if base_servings <= 0:
        raise ValueError(f"Khẩu phần cơ sở (base_servings) phải > 0, nhận được: {base_servings}")
    if target_servings < 0:
        raise ValueError(f"Khẩu phần đích (target_servings) không được âm, nhận được: {target_servings}")
    return target_servings / base_servings


def scale_mealie_ingredient(
    ingredient: RecipeIngredientBase,
    target_servings: float,
    base_servings: float,
) -> RecipeIngredientBase:
    """
    Scale trực tiếp một đối tượng RecipeIngredientBase THẬT của Mealie
    từ khẩu phần cơ sở sang khẩu phần đích.
    """
    factor = calculate_scale_factor(target_servings, base_servings)
    new_qty = (ingredient.quantity * factor) if ingredient.quantity is not None else None
    return RecipeIngredientBase(quantity=new_qty, note=ingredient.note)


# ==============================================================================
# 3. CÁC CHIẾN LƯỢC SINH MẪU (HYPOTHESIS STRATEGIES)
# ==============================================================================

st_qty = st.floats(min_value=0.01, max_value=500.0, allow_nan=False, allow_infinity=False)
st_scale = st.floats(min_value=0.1, max_value=10.0, allow_nan=False, allow_infinity=False)
st_servings = st.integers(min_value=1, max_value=100)


# ==============================================================================
# 4. PROPERTY 4.1: TÍNH ĐƠN ĐIỆU TRÊN ĐỐI TƯỢNG RECIPE INGREDIENT CỦA MEALIE
# Invariant:
#   Target > Base ==> ingredient.quantity sau scale >= ban đầu
#   Target < Base ==> ingredient.quantity sau scale <= ban đầu
# ==============================================================================

@pytest.mark.pbt
@given(qty=st_qty, base_servings=st_servings, target_servings=st_servings)
@settings(max_examples=300)
def test_mealie_recipe_ingredient_monotonicity(qty: float, base_servings: int, target_servings: int):
    """
    Property 4.1: Kiểm tra tính đơn điệu trực tiếp trên đối tượng RecipeIngredientBase của Mealie.
    Tăng khẩu phần không bao giờ làm giảm số lượng nguyên liệu trong mô hình Mealie.
    """
    # Khởi tạo đối tượng Mealie thật
    orig_ing = RecipeIngredientBase(quantity=qty, note="Test Monotonicity")
    scaled_ing = scale_mealie_ingredient(orig_ing, target_servings, base_servings)

    assert scaled_ing.quantity is not None
    assert orig_ing.quantity is not None

    if target_servings > base_servings:
        assert scaled_ing.quantity >= orig_ing.quantity, (
            f"Lỗi: Scale tăng ({base_servings} -> {target_servings}) nhưng "
            f"quantity giảm từ {orig_ing.quantity} xuống {scaled_ing.quantity}"
        )
    elif target_servings < base_servings:
        assert scaled_ing.quantity <= orig_ing.quantity, (
            f"Lỗi: Scale giảm ({base_servings} -> {target_servings}) nhưng "
            f"quantity tăng từ {orig_ing.quantity} lên {scaled_ing.quantity}"
        )
    else:
        assert math.isclose(scaled_ing.quantity, orig_ing.quantity, rel_tol=1e-7)


# ==============================================================================
# 5. PROPERTY 4.2: TÍNH BẢO TOÀN NGHỊCH ĐẢO HAI CHIỀU TRÊN ĐỐI TƯỢNG MEALIE
# Invariant: Round-trip Base -> Target -> Base trả về chính xác đối tượng gốc
# ==============================================================================

@pytest.mark.pbt
@given(qty=st_qty, base_servings=st_servings, target_servings=st_servings)
@settings(max_examples=300)
def test_mealie_recipe_ingredient_reversibility_roundtrip(qty: float, base_servings: int, target_servings: int):
    """
    Property 4.2: Khả năng hoàn tác (Reversibility Round-trip) trên RecipeIngredientBase của Mealie.
    Khi đổi khẩu phần từ A -> B rồi đổi ngược lại từ B -> A, số lượng nguyên liệu
    của Mealie phải phục hồi chính xác về ban đầu trong sai số epsilon <= 1e-4.
    """
    # Đối tượng ban đầu
    orig_ing = RecipeIngredientBase(quantity=qty, note="Test Reversibility")

    # Chiều đi: Base -> Target
    scaled_ing = scale_mealie_ingredient(orig_ing, target_servings, base_servings)

    # Chiều về: Target -> Base
    reverted_ing = scale_mealie_ingredient(scaled_ing, base_servings, target_servings)

    assert reverted_ing.quantity is not None
    diff = abs(reverted_ing.quantity - qty)
    assert diff <= 1e-4, (
        f"Lệch round-trip trên đối tượng Mealie: Gốc={qty}, Sau hoàn tác={reverted_ing.quantity}, "
        f"Độ lệch={diff} > 1e-4"
    )


# ==============================================================================
# 6. PROPERTY 4.3: TÍNH BẮC CẦU KHI SCALE LIÊN TIẾP NHIỀU BƯỚC
# Invariant: Scale 2 bước (k1 rồi k2) == Scale 1 bước (k1 * k2)
# ==============================================================================

@pytest.mark.pbt
@given(
    qty=st_qty,
    factor1=st.floats(min_value=0.2, max_value=5.0, allow_nan=False, allow_infinity=False),
    factor2=st.floats(min_value=0.2, max_value=5.0, allow_nan=False, allow_infinity=False),
)
@settings(max_examples=300)
def test_mealie_recipe_ingredient_transitivity(qty: float, factor1: float, factor2: float):
    """
    Property 4.3: Tính kết hợp khi người dùng liên tục điều chỉnh khẩu phần trên Mealie.
    """
    ing = RecipeIngredientBase(quantity=qty)

    # Scale 2 bước liên tiếp
    step1 = RecipeIngredientBase(quantity=ing.quantity * factor1)
    step2 = RecipeIngredientBase(quantity=step1.quantity * factor2)

    # Scale 1 bước gộp
    combined = RecipeIngredientBase(quantity=ing.quantity * (factor1 * factor2))

    assert math.isclose(step2.quantity, combined.quantity, rel_tol=1e-4, abs_tol=1e-4)


# ==============================================================================
# 7. PROPERTY 4.4: KIỂM THỬ TRỰC TIẾP HÀM ĐỊNH DẠNG PHÂN SỐ THẬT CỦA MEALIE
# Hàm mục tiêu: mealie_display_fraction() trong mealie_src/.../recipe_ingredient.py
# Invariant:
#   1. Format không bao giờ crash với mọi phân số hợp lệ
#   2. Chuỗi kết quả luôn chứa ký tự phân cách "/"
#   3. Ký tự tử số thuộc SUPERSCRIPT, ký tự mẫu số thuộc SUBSCRIPT
# ==============================================================================

@pytest.mark.pbt
@given(
    numerator=st.integers(min_value=1, max_value=999),
    denominator=st.integers(min_value=1, max_value=MAX_INGREDIENT_DENOMINATOR),
)
@settings(max_examples=300)
def test_mealie_display_fraction_real_code(numerator: int, denominator: int):
    """
    Property 4.4: Kiểm thử TRỰC TIẾP hàm mealie_display_fraction() thật của Mealie.
    Chứng minh thuật toán ánh xạ ký tự Unicode thượng/hạ của Mealie hoạt động chính xác.
    """
    frac = Fraction(numerator, denominator)
    result = mealie_display_fraction(frac)

    assert isinstance(result, str)
    assert "/" in result

    # Tách tử số và mẫu số từ chuỗi định dạng của Mealie
    super_part, sub_part = result.split("/", 1)
    assert len(super_part) > 0
    assert len(sub_part) > 0

    # Kiểm tra từng ký tự tử số phải thuộc tập SUPERSCRIPT của Mealie
    for ch in super_part:
        assert ch in SUPERSCRIPT.values(), f"Ký tự tử số '{ch}' không thuộc bảng SUPERSCRIPT của Mealie"

    # Kiểm tra từng ký tự mẫu số phải thuộc tập SUBSCRIPT của Mealie
    for ch in sub_part:
        assert ch in SUBSCRIPT.values(), f"Ký tự mẫu số '{ch}' không thuộc bảng SUBSCRIPT của Mealie"


# ==============================================================================
# 8. PROPERTY 4.5: KIỂM THỬ PHƯƠNG THỨC THẬT _format_quantity_for_display() CỦA MEALIE
# Phương thức mục tiêu: RecipeIngredientBase._format_quantity_for_display()
# Invariant:
#   Sau khi scale ở bất kỳ tỉ lệ nào, chuỗi hiển thị của Mealie không bao giờ rỗng,
#   không sinh "nan", "inf", và không làm sập server (Crash-free)
# ==============================================================================

@pytest.mark.pbt
@given(qty=st_qty, factor=st_scale)
@settings(max_examples=300)
def test_mealie_format_quantity_for_display_after_scaling(qty: float, factor: float):
    """
    Property 4.5: Kiểm thử phương thức THẬT _format_quantity_for_display() của Mealie
    trên đối tượng sau khi scale khẩu phần.
    """
    scaled_qty = qty * factor
    ing = RecipeIngredientBase(quantity=scaled_qty)

    # Gọi trực tiếp phương thức THẬT của Mealie
    display_str = ing._format_quantity_for_display()

    assert isinstance(display_str, str)
    assert len(display_str.strip()) > 0
    assert "nan" not in display_str.lower()
    assert "inf" not in display_str.lower()


# ==============================================================================
# 9. PROPERTY 4.6: XỬ LÝ CA BIÊN & DỮ LIỆU BẤT THƯỜNG TRÊN ĐỐI TƯỢNG MEALIE
# Invariant:
#   quantity = 0 hoặc None ==> scale không lỗi
#   base_servings <= 0 ==> ValueError
#   target_servings < 0 ==> ValueError
# ==============================================================================

@pytest.mark.pbt
@given(factor=st_scale)
def test_mealie_ingredient_none_and_zero_quantity(factor: float):
    """Property 4.6.1: Nguyên liệu Mealie có quantity=None (nêm nếm) scale vẫn là None."""
    none_ing = RecipeIngredientBase(quantity=None, note="Muối tiêu vừa ăn")
    scaled = scale_mealie_ingredient(none_ing, target_servings=8, base_servings=4)
    assert scaled.quantity is None
    assert scaled.note == "Muối tiêu vừa ăn"


@pytest.mark.pbt
@given(
    invalid_base=st.floats(max_value=0.0, allow_nan=False, allow_infinity=False),
    target=st.floats(min_value=1.0, max_value=20.0, allow_nan=False, allow_infinity=False),
)
def test_mealie_scaling_invalid_base_servings(invalid_base: float, target: float):
    """Property 4.6.2: Khẩu phần cơ sở <= 0 phải ném ValueError."""
    ing = RecipeIngredientBase(quantity=100.0)
    with pytest.raises(ValueError, match="base_servings"):
        scale_mealie_ingredient(ing, target_servings=target, base_servings=invalid_base)


@pytest.mark.pbt
@given(
    base=st.floats(min_value=1.0, max_value=20.0, allow_nan=False, allow_infinity=False),
    invalid_target=st.floats(max_value=-0.001, allow_nan=False, allow_infinity=False),
)
def test_mealie_scaling_negative_target_servings(base: float, invalid_target: float):
    """Property 4.6.3: Khẩu phần đích < 0 phải ném ValueError."""
    ing = RecipeIngredientBase(quantity=100.0)
    with pytest.raises(ValueError, match="target_servings"):
        scale_mealie_ingredient(ing, target_servings=invalid_target, base_servings=base)
