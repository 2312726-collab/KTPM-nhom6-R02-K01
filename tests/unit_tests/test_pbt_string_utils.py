"""
Property-Based Testing for Mealie's string_utils module.
Owner: Tran Ngoc Bao Phuoc (2312719) — QA Automation Engineer 1.
"""

import pytest
from hypothesis import example, given, settings, strategies as st

from mealie.services.parser_services.parser_utils.string_utils import (
    convert_vulgar_fractions_to_regular_fractions,
    move_parens_to_end,
    remove_footnote_markers,
)

VULGAR_FRACTION_CHARS = (
    "¼",
    "½",
    "¾",
    "⅐",
    "⅑",
    "⅒",
    "⅓",
    "⅔",
    "⅕",
    "⅖",
    "⅗",
    "⅘",
    "⅙",
    "⅚",
    "⅛",
    "⅜",
    "⅝",
    "⅞",
)


@pytest.mark.pbt
@settings(max_examples=300)
@given(s=st.text())
def test_remove_footnote_idempotent(s: str):
    once = remove_footnote_markers(s)
    assert remove_footnote_markers(once) == once


@pytest.mark.pbt
@pytest.mark.xfail(
    strict=True,
    reason="Mealie v3.28.0 move_parens_to_end is not idempotent for repeated parenthetical notes.",
)
@settings(max_examples=300)
@given(
    s=st.one_of(
        st.text(),
        st.tuples(
            st.text(
                alphabet="abcdefghijklmnopqrstuvwxyz0123456789",
                min_size=1,
                max_size=6,
            ),
            st.text(
                alphabet="abcdefghijklmnopqrstuvwxyz",
                min_size=2,
                max_size=8,
            ),
            st.text(
                alphabet="abcdefghijklmnopqrstuvwxyz",
                min_size=2,
                max_size=8,
            ),
        ).map(lambda parts: f"{parts[0]} ({parts[1]}) ({parts[2]}) "),
    )
)
@example(s="1 (aa) (bb) ")
def test_move_parens_idempotent(s: str):
    once = move_parens_to_end(s)
    assert move_parens_to_end(once) == once


@pytest.mark.pbt
@settings(max_examples=300)
@given(s=st.text())
def test_convert_vulgar_fractions_crash_free(s: str):
    result = convert_vulgar_fractions_to_regular_fractions(s)
    assert isinstance(result, str)


@pytest.mark.pbt
@settings(max_examples=300)
@given(s=st.one_of(st.text(), st.text(alphabet=VULGAR_FRACTION_CHARS)))
@example(s="½ ¼ ¾ ⅓ ⅔")
def test_convert_vulgar_fractions_no_remaining_unicode(s: str):
    result = convert_vulgar_fractions_to_regular_fractions(s)
    assert all(char not in result for char in VULGAR_FRACTION_CHARS)
