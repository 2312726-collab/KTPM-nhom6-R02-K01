"""M2 — Property 3: BruteForceParser xử lý chuỗi Unicode mà không crash."""

import asyncio
import os
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from hypothesis import given, settings, strategies as st

os.environ.setdefault("PRODUCTION", "false")

from tests.conftest import ensure_mealie_parser_isolated

ensure_mealie_parser_isolated()

from mealie.schema.recipe.recipe_ingredient import IngredientUnit, ParsedIngredient
from mealie.services.parser_services.ingredient_parser import BruteForceParser


async def parse_with_mock_database(
    text: str, units: list[IngredientUnit] | None = None
) -> ParsedIngredient:
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
@pytest.mark.xfail(
    strict=True,
    reason="Mealie v3.28.0 DEF-03: IndexError tại brute/process.py:199 -> 110 khi DB có đơn vị và chuỗi kết thúc bằng đơn vị ('a cup').",
)
def test_ingredient_parser_unit_at_end_bug():
    """Kiểm tra hành vi BruteForceParser.parse_one('a cup') khi DB đã có unit 'cup'."""
    cup_unit = IngredientUnit(id=uuid4(), name="cup")
    result = asyncio.run(parse_with_mock_database("a cup", units=[cup_unit]))
    assert isinstance(result, ParsedIngredient)
