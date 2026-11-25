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
from uuid import uuid4
import pytest
from pydantic import BaseModel, UUID4
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

class _MealieRecipeStub(BaseModel):
    """Stub tối thiểu cho Recipe/RecipeSummary để hỗ trợ cả Pydantic và isinstance(..., Recipe)."""
    id: UUID4
    name: str = "Sub-recipe"
    recipe_ingredient: list[Any] = []


# Đăng ký mock cô lập tầng CSDL và Config ngoài lề để nạp schema & service Mealie sạch sẽ
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

if "mealie.core.exceptions" not in sys.modules:
    ex_mod = types.ModuleType("mealie.core.exceptions")

    class UnexpectedNone(Exception):
        pass

    ex_mod.UnexpectedNone = UnexpectedNone
    sys.modules["mealie.core.exceptions"] = ex_mod

if "mealie.repos.all_repositories" not in sys.modules:
    ar_mod = types.ModuleType("mealie.repos.all_repositories")
    ar_mod.get_repositories = MagicMock()
    sys.modules["mealie.repos.all_repositories"] = ar_mod

if "mealie.repos.repository_factory" not in sys.modules:
    rf_mod = types.ModuleType("mealie.repos.repository_factory")
    rf_mod.AllRepositories = Any
    sys.modules["mealie.repos.repository_factory"] = rf_mod

if "mealie.schema.recipe" not in sys.modules and MEALIE_SRC.exists():
    pkg = types.ModuleType("mealie.schema.recipe")
    pkg.__path__ = [str(MEALIE_SRC / "mealie" / "schema" / "recipe")]
    sys.modules["mealie.schema.recipe"] = pkg

if "mealie.schema.recipe.recipe" not in sys.modules:
    r_mod = types.ModuleType("mealie.schema.recipe.recipe")
    r_mod.Recipe = _MealieRecipeStub
    r_mod.RecipeSummary = _MealieRecipeStub
    sys.modules["mealie.schema.recipe.recipe"] = r_mod

if "mealie.db.models.recipe" not in sys.modules:
    db_mod = types.ModuleType("mealie.db.models.recipe")
    db_mod.IngredientFoodModel = MagicMock()
    db_mod.IngredientFoodSubstitutionModel = MagicMock()
    db_mod.RecipeModel = MagicMock()
    sys.modules["mealie.db.models.recipe"] = db_mod

if "mealie.db.models.household" not in sys.modules:
    hh_db_mod = types.ModuleType("mealie.db.models.household")
    hh_db_mod.ShoppingList = MagicMock()
    hh_db_mod.ShoppingListItem = MagicMock()
    hh_db_mod.ShoppingListMultiPurposeLabel = MagicMock()
    hh_db_mod.ShoppingListRecipeReference = MagicMock()
    sys.modules["mealie.db.models.household"] = hh_db_mod

if "mealie.db.models.users.users" not in sys.modules:
    u_db_mod = types.ModuleType("mealie.db.models.users.users")
    u_db_mod.User = MagicMock()
    sys.modules["mealie.db.models.users.users"] = u_db_mod

if "mealie.services.parser_services" not in sys.modules and MEALIE_SRC.exists():
    ps_pkg = types.ModuleType("mealie.services.parser_services")
    ps_pkg.__path__ = [str(MEALIE_SRC / "mealie" / "services" / "parser_services")]
    sys.modules["mealie.services.parser_services"] = ps_pkg

if "mealie.services.parser_services._base" not in sys.modules:
    ps_base = types.ModuleType("mealie.services.parser_services._base")

    class _StubDataMatcher:
        def __init__(self, repos, **kwargs):
            self.repos = repos
            self.units_by_id = {}

    ps_base.DataMatcher = _StubDataMatcher
    sys.modules["mealie.services.parser_services._base"] = ps_base

if "mealie.schema.household" not in sys.modules and MEALIE_SRC.exists():
    hh_pkg = types.ModuleType("mealie.schema.household")
    hh_pkg.__path__ = [str(MEALIE_SRC / "mealie" / "schema" / "household")]
    sys.modules["mealie.schema.household"] = hh_pkg

if "mealie.services.household_services" not in sys.modules and MEALIE_SRC.exists():
    hs_pkg = types.ModuleType("mealie.services.household_services")
    hs_pkg.__path__ = [str(MEALIE_SRC / "mealie" / "services" / "household_services")]
    sys.modules["mealie.services.household_services"] = hs_pkg

# ==============================================================================
# Cơ chế nạp linh hoạt các module thật từ mã nguồn Mealie v3.28.0
# ==============================================================================
def _load_mealie_module(module_name: str, rel_parts: tuple[str, ...]):
    import importlib.util

    candidates = [
        PROJECT_ROOT / "mealie_src" / Path(*rel_parts),
        Path("mealie_src") / Path(*rel_parts),
        Path(__file__).resolve().parent.parent.parent / "mealie_src" / Path(*rel_parts),
    ]
    for p in candidates:
        if p.exists():
            spec = importlib.util.spec_from_file_location(module_name, str(p))
            if spec and spec.loader:
                mod = importlib.util.module_from_spec(spec)
                sys.modules[module_name] = mod
                spec.loader.exec_module(mod)
                return mod

    raise ImportError(f"Không tìm thấy tệp {'/'.join(rel_parts)} trong mealie_src!")

_ing_mod = _load_mealie_module(
    "mealie.schema.recipe.recipe_ingredient",
    ("mealie", "schema", "recipe", "recipe_ingredient.py"),
)
_load_mealie_module(
    "mealie.schema.household.group_shopping_list",
    ("mealie", "schema", "household", "group_shopping_list.py"),
)
_sl_mod = _load_mealie_module(
    "mealie.services.household_services.shopping_lists",
    ("mealie", "services", "household_services", "shopping_lists.py"),
)

RecipeIngredientBase = _ing_mod.RecipeIngredientBase
RecipeIngredient = _ing_mod.RecipeIngredient
IngredientFood = _ing_mod.IngredientFood
IngredientUnit = _ing_mod.IngredientUnit
mealie_display_fraction = _ing_mod.display_fraction
INGREDIENT_QTY_PRECISION = _ing_mod.INGREDIENT_QTY_PRECISION
MAX_INGREDIENT_DENOMINATOR = _ing_mod.MAX_INGREDIENT_DENOMINATOR
SUPERSCRIPT = _ing_mod.SUPERSCRIPT
SUBSCRIPT = _ing_mod.SUBSCRIPT
ShoppingListService = _sl_mod.ShoppingListService


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
    """Property 4.6.1: Nguyên liệu Mealie có quantity=None hoặc 0.0 khi scale bất kỳ factor nào vẫn giữ nguyên."""
    target_servings = 4.0 * factor
    none_ing = RecipeIngredientBase(quantity=None, note="Muối tiêu vừa ăn")
    scaled_none = scale_mealie_ingredient(none_ing, target_servings=target_servings, base_servings=4.0)
    assert scaled_none.quantity is None
    assert scaled_none.note == "Muối tiêu vừa ăn"

    zero_ing = RecipeIngredientBase(quantity=0.0, note="Gia vị tùy thích")
    scaled_zero = scale_mealie_ingredient(zero_ing, target_servings=target_servings, base_servings=4.0)
    assert scaled_zero.quantity == 0.0
    assert scaled_zero.note == "Gia vị tùy thích"


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


# ==============================================================================
# 10. PROPERTY 4.7–4.9: KIỂM THỬ TRỰC TIẾP HÀM SCALING BACKEND THẬT CỦA MEALIE
# Service mục tiêu: ShoppingListService.get_shopping_list_items_from_recipe()
# ==============================================================================

def _build_mock_shopping_service() -> ShoppingListService:
    mock_repos = MagicMock()
    return ShoppingListService(mock_repos)


@pytest.mark.pbt
@given(qty=st_qty, base_servings=st_servings, target_servings=st_servings)
@settings(max_examples=200)
def test_mealie_shopping_list_scaling_monotonicity_real_service(
    qty: float, base_servings: int, target_servings: int
):
    """
    Property 4.7: Gọi trực tiếp ShoppingListService.get_shopping_list_items_from_recipe()
    của Mealie v3.28.0 để kiểm chứng tính đơn điệu và lưu vết scale khi co giãn khẩu phần.
    """
    service = _build_mock_shopping_service()
    factor = target_servings / base_servings
    food = IngredientFood(id=uuid4(), name="flour")
    unit = IngredientUnit(id=uuid4(), name="cup")
    ing = RecipeIngredient(quantity=qty, food=food, unit=unit)

    items = service.get_shopping_list_items_from_recipe(
        list_id=uuid4(),
        recipe_id=uuid4(),
        scale=factor,
        recipe_ingredients=[ing],
        skip_on_hand=False,
    )

    assert len(items) == 1
    scaled_item = items[0]
    expected_base = ing.quantity  # RecipeIngredient tự làm tròn 3 chữ số thập phân (INGREDIENT_QTY_PRECISION)

    if target_servings > base_servings:
        assert scaled_item.quantity >= expected_base
    elif target_servings < base_servings:
        assert scaled_item.quantity <= expected_base
    else:
        assert math.isclose(scaled_item.quantity, expected_base, rel_tol=1e-7)

    assert scaled_item.recipe_references[0].recipe_scale == factor
    assert scaled_item.recipe_references[0].recipe_quantity == expected_base


@pytest.mark.pbt
@given(
    sub_qty=st.floats(min_value=0.5, max_value=10.0, allow_nan=False, allow_infinity=False),
    ing_qty=st_qty,
    parent_scale=st_scale,
)
@settings(max_examples=150)
def test_mealie_shopping_list_subrecipe_recursive_scaling(
    sub_qty: float, ing_qty: float, parent_scale: float
):
    """
    Property 4.8: Kiểm chứng tính nhân dồn đệ quy (Recursive Sub-recipe Scaling)
    tại ShoppingListService.get_shopping_list_items_from_recipe() (shopping_lists.py:348-360).
    """
    service = _build_mock_shopping_service()
    food = IngredientFood(id=uuid4(), name="sugar")
    unit = IngredientUnit(id=uuid4(), name="gram")
    inner_ing = RecipeIngredient(quantity=ing_qty, food=food, unit=unit)
    sub_recipe = _MealieRecipeStub(id=uuid4(), name="Sauce", recipe_ingredient=[inner_ing])
    parent_ing = RecipeIngredient(quantity=sub_qty, referenced_recipe=sub_recipe)

    items = service.get_shopping_list_items_from_recipe(
        list_id=uuid4(),
        recipe_id=uuid4(),
        scale=parent_scale,
        recipe_ingredients=[parent_ing],
        skip_on_hand=False,
    )

    assert len(items) == 1
    expected_qty = inner_ing.quantity * (parent_ing.quantity * parent_scale)
    assert math.isclose(items[0].quantity, expected_qty, rel_tol=1e-6, abs_tol=1e-6)


@pytest.mark.pbt
@pytest.mark.xfail(
    strict=True,
    reason="Bug thật của Mealie v3.28.0 tại shopping_lists.py:403: gộp 2 nguyên liệu giống nhau quên nhân scale cho dòng thứ 2",
)
@given(
    qty1=st.floats(min_value=1.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    qty2=st.floats(min_value=1.0, max_value=100.0, allow_nan=False, allow_infinity=False),
    scale=st.floats(min_value=1.5, max_value=10.0, allow_nan=False, allow_infinity=False),
)
@settings(max_examples=50)
def test_mealie_shopping_list_duplicate_ingredient_scaling_bug(qty1: float, qty2: float, scale: float):
    """
    Property 4.9 (Defect Characterization): Khi công thức có 2 dòng cùng food & unit,
    tổng lượng sau khi scale phải bằng (qty1 + qty2) * scale.
    Thực tế Mealie v3.28.0 ở shopping_lists.py:403 cộng `existing_item.quantity += ingredient.quantity`
    (thiếu `* scale`).
    """
    service = _build_mock_shopping_service()
    food = IngredientFood(id=uuid4(), name="sugar")
    unit = IngredientUnit(id=uuid4(), name="cup")
    ing1 = RecipeIngredient(quantity=qty1, food=food, unit=unit)
    ing2 = RecipeIngredient(quantity=qty2, food=food, unit=unit)

    items = service.get_shopping_list_items_from_recipe(
        list_id=uuid4(),
        recipe_id=uuid4(),
        scale=scale,
        recipe_ingredients=[ing1, ing2],
        skip_on_hand=False,
    )

    assert len(items) == 1
    expected_total = (ing1.quantity + ing2.quantity) * scale
    assert math.isclose(items[0].quantity, expected_total, rel_tol=1e-4, abs_tol=1e-4), (
        f"Lỗi Scaling Mealie tại shopping_lists.py:403: kỳ vọng {expected_total}, thực tế {items[0].quantity}"
    )
