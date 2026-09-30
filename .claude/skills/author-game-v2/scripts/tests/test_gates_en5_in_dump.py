"""EN5 (2026-09-30): G27 (now "a banded meter is shown once") takes `in_dump = false`.

`in_dump = false` keeps a key out of the sidebar's Traits dump only; `hidden = true` (a
secret trait, name-keyed across the player and every NPC) still passes, and neither
fails with the new fix line. Nothing in games/ is read or written.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from test_gates_ws5 import base_game, verdict  # noqa: E402

GATE = "a banded meter is shown once"   # renamed in phase 4 (Gate 27)


def banded(label=None):
    g = base_game()
    g["player"]["core_traits"]["corruption"] = 0
    g["sidebar_items"] = [{"type": "trait_words", "trait": "corruption", "show_value": True,
                           "bands": [{"min": 0, "max": 100, "text": "Clean"}]}]
    if label is not None:
        g["traits"] = {"labels": [{"key": "corruption", "label": "Corruption", **label}]}
    return g


def test_in_dump_false_passes():
    assert verdict(banded({"in_dump": False}), {}, GATE)[0] == "PASS"


def test_hidden_still_passes():
    assert verdict(banded({"hidden": True}), {}, GATE)[0] == "PASS"


def test_neither_fails_and_names_in_dump():
    v, r = verdict(banded({}), {}, GATE)
    assert v == "FAIL"
    text = " ".join(r["detail"])
    assert "declared without in_dump = false" in text and "set in_dump = false" in text
