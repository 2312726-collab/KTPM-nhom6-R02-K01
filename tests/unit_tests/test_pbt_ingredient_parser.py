"""M2 — Property 3: BruteForceParser xử lý chuỗi Unicode mà không crash."""

import asyncio
import os
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from hypothesis import given, settings, strategies as st
from tests.conftest import isolate_mealie_recipe_parser

os.environ.setdefault("PRODUCTION", "false")

isolate_mealie_recipe_parser()

from mealie.schema.recipe.recipe_ingredient import IngredientUnit, ParsedIngredient
from mealie.services.parser_services.ingredient_parser import BruteForceParser


async def parse_with_mock_database(
    text: str, units: tuple[IngredientUnit, ...] = ()
) -> ParsedIngredient:
    repositories = MagicMock()
    repositories.ingredient_foods.page_all.return_value.items = []
    repositories.ingredient_units.page_all.return_value.items = list(units)
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


empty_tokens = pytest.mark.xfail(
    strict=True, raises=IndexError, reason="DEF-03: empty tokens indexed at brute/process.py:152"
)


@pytest.mark.pbt
@empty_tokens
@given(text=st.text(max_size=500))
@settings(max_examples=300)
def test_ingredient_parser_never_crashes(text):
    assert isinstance(asyncio.run(parse_with_mock_database(text)), ParsedIngredient)


@pytest.mark.unit
@pytest.mark.parametrize(
    "text",
    [
        pytest.param("", marks=empty_tokens, id="empty"),
        pytest.param("   ", marks=empty_tokens, id="whitespace-only"),
        pytest.param("±×÷√∞≠≤≥", id="math-symbols"),
        pytest.param("a" * 10_000, id="long-unbroken-token"),
        pytest.param("\x00", id="null-byte"),
    ],
)
def test_ingredient_parser_edge_cases(text):
    assert isinstance(asyncio.run(parse_with_mock_database(text)), ParsedIngredient)


@pytest.mark.pbt
@pytest.mark.xfail(
    strict=True,
    raises=IndexError,
    reason="DEF-03: a known trailing unit leaves no ingredient tokens (brute/process.py:199 -> 110)",
)
def test_ingredient_parser_known_unit_at_end():
    cup = IngredientUnit(id=uuid4(), name="cup", plural_name="cups")
    assert isinstance(asyncio.run(parse_with_mock_database("a cup", (cup,))), ParsedIngredient)
