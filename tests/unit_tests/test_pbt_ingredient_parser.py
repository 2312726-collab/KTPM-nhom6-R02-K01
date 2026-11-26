"""M2 — Property 3: BruteForceParser xử lý chuỗi Unicode mà không crash."""

import asyncio
import os
import sys
import types
from pathlib import Path
from typing import Any
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from hypothesis import given, settings, strategies as st
from pydantic import BaseModel, UUID4

os.environ.setdefault("PRODUCTION", "false")

# Cô lập mealie.schema.recipe và các phụ thuộc tầng dưới để tránh lỗi PEP 649 trên Python <= 3.13
_MEALIE_SRC = Path(__file__).resolve().parent.parent.parent / "mealie_src"

class _MealieRecipeStub(BaseModel):
    id: UUID4
    name: str = "Sub-recipe"
    recipe_ingredient: list[Any] = []

if "fastapi" not in sys.modules:
    _fastapi_mod = types.ModuleType("fastapi")
    _fastapi_mod.Header = MagicMock()
    sys.modules["fastapi"] = _fastapi_mod

if "mealie.core.root_logger" not in sys.modules:
    _logger_mod = types.ModuleType("mealie.core.root_logger")
    _logger_mod.get_logger = MagicMock(return_value=MagicMock())
    sys.modules["mealie.core.root_logger"] = _logger_mod

if "mealie.db.models.recipe" not in sys.modules:
    _db_recipe_mod = types.ModuleType("mealie.db.models.recipe")
    _db_recipe_mod.__path__ = []
    _db_recipe_mod.IngredientFoodModel = MagicMock()
    _db_recipe_mod.IngredientFoodSubstitutionModel = MagicMock()
    _db_recipe_mod.RecipeModel = MagicMock()
    sys.modules["mealie.db.models.recipe"] = _db_recipe_mod

if "mealie.db.models.recipe.ingredient" not in sys.modules:
    _db_ing_mod = types.ModuleType("mealie.db.models.recipe.ingredient")
    _db_ing_mod.IngredientFoodModel = MagicMock()
    _db_ing_mod.IngredientUnitModel = MagicMock()
    sys.modules["mealie.db.models.recipe.ingredient"] = _db_ing_mod

if "mealie.schema.recipe" not in sys.modules:
    _recipe_pkg_path = _MEALIE_SRC / "mealie" / "schema" / "recipe"
    if _recipe_pkg_path.exists():
        _pkg = types.ModuleType("mealie.schema.recipe")
        _pkg.__path__ = [str(_recipe_pkg_path)]
        sys.modules["mealie.schema.recipe"] = _pkg

if "mealie.schema.recipe.recipe" not in sys.modules:
    _recipe_mod = types.ModuleType("mealie.schema.recipe.recipe")
    _recipe_mod.Recipe = _MealieRecipeStub
    _recipe_mod.RecipeSummary = _MealieRecipeStub
    sys.modules["mealie.schema.recipe.recipe"] = _recipe_mod

from mealie.schema.recipe.recipe_ingredient import IngredientUnit, ParsedIngredient, RecipeIngredient
sys.modules["mealie.schema.recipe"].RecipeIngredient = RecipeIngredient

if "mealie.repos" not in sys.modules:
    _repos_pkg = types.ModuleType("mealie.repos")
    _repos_pkg.__path__ = []
    sys.modules["mealie.repos"] = _repos_pkg

if "mealie.repos.all_repositories" not in sys.modules:
    _all_repos_mod = types.ModuleType("mealie.repos.all_repositories")
    _all_repos_mod.get_repositories = MagicMock()
    _all_repos_mod.AllRepositories = MagicMock()
    sys.modules["mealie.repos.all_repositories"] = _all_repos_mod

if "mealie.repos.repository_factory" not in sys.modules:
    _repo_fac_mod = types.ModuleType("mealie.repos.repository_factory")
    _repo_fac_mod.AllRepositories = MagicMock()
    sys.modules["mealie.repos.repository_factory"] = _repo_fac_mod

from mealie.services.parser_services.ingredient_parser import BruteForceParser


async def parse_with_mock_database(text: str, units: list[IngredientUnit] | None = None) -> ParsedIngredient:
    repositories = MagicMock()
    repositories.ingredient_foods.page_all.return_value.items = []
    repositories.ingredient_units.page_all.return_value.items = units or []
    translator = MagicMock()
    translator.t.side_effect = lambda key, **kwargs: key

    with patch(
        "mealie.services.parser_services._base.get_repositories",
        return_value=repositories,
    ):
        parser = BruteForceParser(
            group_id=uuid4(), session=MagicMock(), translator=translator
        )
        return await parser.parse_one(text)


@pytest.mark.pbt
@pytest.mark.xfail(
    strict=True,
    reason="Mealie v3.28.0 DEF-03: BruteForceParser.parse_one() ném IndexError khi chuỗi rỗng hoặc chỉ có khoảng trắng (brute/process.py:152).",
)
@given(text=st.text(max_size=500))
@settings(max_examples=300)
def test_ingredient_parser_never_crashes(text):
    assert isinstance(asyncio.run(parse_with_mock_database(text)), ParsedIngredient)


@pytest.mark.unit
@pytest.mark.parametrize(
    "text",
    [
        pytest.param(
            "",
            id="empty",
            marks=pytest.mark.xfail(
                strict=True,
                reason="Mealie v3.28.0 DEF-03: IndexError tại brute/process.py:152 với chuỗi rỗng.",
            ),
        ),
        pytest.param(
            "   ",
            id="whitespace-only",
            marks=pytest.mark.xfail(
                strict=True,
                reason="Mealie v3.28.0 DEF-03: IndexError tại brute/process.py:152 với chuỗi toàn khoảng trắng.",
            ),
        ),
        pytest.param("±×÷√∞≠≤≥", id="math-symbols"),
        pytest.param("a" * 10_000, id="long-unbroken-token"),
        pytest.param("\x00", id="null-byte"),
    ],
)
def test_ingredient_parser_edge_cases(text):
    assert isinstance(asyncio.run(parse_with_mock_database(text)), ParsedIngredient)


@pytest.mark.unit
def test_ingredient_parser_unit_at_end_bug():
    cup_unit = IngredientUnit(id=uuid4(), name="cup")
    result = asyncio.run(parse_with_mock_database("a cup", units=[cup_unit]))
    assert isinstance(result, ParsedIngredient)
