"""Gate 27 (PRD v2 phase 4 · D1 · D4, 2026-09-30): a banded meter is shown once.

The key stays out of the Traits dump (`in_dump = false`; `hidden` still accepted) AND the
item prints the number: `trait_words` + `show_value`, or `trait_bar` without `hide_value`.

Fixtures are written here; nothing in games/ is read or written.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_gates_ws5 import base_game, verdict  # noqa: E402

GATE = "a banded meter is shown once"
BANDS = [{"min": 0, "max": 100, "text": "Clean"}]


def g(item, label=None):
    game = base_game()
    game["player"]["core_traits"]["corruption"] = 0
    game["sidebar_items"] = [dict({"trait": "corruption", "bands": BANDS}, **item)]
    game["traits"] = {"labels": [dict({"key": "corruption", "label": "Corruption"},
                                      **(label if label is not None else {"in_dump": False}))]}
    return game


def test_trait_words_with_show_value_passes():
    assert verdict(g({"type": "trait_words", "show_value": True}), {}, GATE)[0] == "PASS"


def test_a_trait_bar_with_its_number_passes():
    assert verdict(g({"type": "trait_bar", "min": 0, "max": 100}), {}, GATE)[0] == "PASS"


def test_hidden_still_keeps_it_out_of_the_dump():
    assert verdict(g({"type": "trait_words", "show_value": True}, {"hidden": True}), {}, GATE)[0] == "PASS"


def test_words_without_the_number_fail():
    v, r = verdict(g({"type": "trait_words"}), {}, GATE)
    assert v == "FAIL" and "prints no number" in " ".join(r["detail"])


def test_a_bar_that_hides_its_value_fails():
    v, _r = verdict(g({"type": "trait_bar", "min": 0, "max": 100, "hide_value": True}), {}, GATE)
    assert v == "FAIL"


def test_status_text_prints_only_the_word_and_fails():
    v, _r = verdict(g({"type": "trait_status_text"}), {}, GATE)
    assert v == "FAIL"


def test_a_key_left_in_the_dump_still_fails():
    v, r = verdict(g({"type": "trait_words", "show_value": True}, {}), {}, GATE)
    assert v == "FAIL" and "declared without in_dump = false" in " ".join(r["detail"])


def test_an_item_that_names_its_trait_as_trait_key_is_not_read():
    # The engine and importer read `trait` only; a `trait_key` item names nothing.
    game = g({"type": "trait_words"})
    game["sidebar_items"][0]["trait_key"] = game["sidebar_items"][0].pop("trait")
    assert verdict(game, {}, GATE)[0] == "n/a"
