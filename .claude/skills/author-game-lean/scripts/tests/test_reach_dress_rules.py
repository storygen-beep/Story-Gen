"""Copied from author-game-v2/scripts/tests/test_gates_dress_rules.py (frozen at ea8f6465), 2026-11-19.
The gates.py tests are adapted to call reach directly; the not-applicable gate test is dropped (no gate here)."""
"""Gate `a dress rule keeps its word` and the lints `a scene few outfits reach` / `a dress exception that a dress slips
through` (LO, 2026-11-18). first_term's street let her out in a sports bra and a dress with no panties at
Exhibitionism 0 while its own message said that needs 40. Fixtures only; nothing in games/ is read."""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import reach  # noqa: E402


def _c(*items):
    return {"version": "1.0", "logic": "AND", "items": list(items)}


EXH = lambda op, v: {"type": "trait", "subject": "player", "trait_key": "exhibitionism", "operator": op, "value": v}  # noqa: E731
SPORTS = {"type": "clothing_item", "item_id": "sports_bra", "operator": "equipped"}
NO_TOP = {"type": "clothing_slot", "slot": "top", "operator": "unequipped"}
NO_DRESS = {"type": "clothing_slot", "slot": "dress", "operator": "unequipped"}


def game(sports_rule_items):
    return {
        "player": {"core_traits": {"exhibitionism": 0}},
        "traits": {"labels": [{"key": "exhibitionism", "label": "Exhibitionism"}]},
        "npcs": [],
        "clothing": [
            {"id": "sports_bra", "slot": "bra", "type": "sports_bra", "initial": True},
            {"id": "panties", "slot": "underwear", "type": "panties", "initial": True},
            {"id": "tshirt", "slot": "top", "type": "tshirt", "initial": True},
            {"id": "jeans", "slot": "bottom", "type": "jeans", "initial": True},
            {"id": "uniform", "slot": "dress", "type": "cafe_uniform", "initial": True},
        ],
        "locations": [{"id": "home"}, {"id": "street", "clothing_rules": [
            {"conditions": _c(*sports_rule_items), "slots_required": ["top"],
             "message": "Not in just the sports bra. Not yet. (Needs Exhibitionism 20.)"},
            {"conditions": _c(EXH("gte", 20)), "slots_required": ["underwear", "top", "bottom"],
             "message": "Not like this. Not yet. (No panties out of the house needs Exhibitionism 40.)"},
            {"slots_required": ["bra", "underwear", "top", "bottom"],
             "message": "Not like this. Not yet. (Going out without a bra needs Exhibitionism 20.)"}]}],
        "canvases": [{"id": "start", "trigger": {"location": "home"}, "nodes": [{"id": "a"}]},
                     {"id": "seen", "trigger": {"location": "street", "conditions": _c(
                         {"type": "clothing_slot", "slot": "underwear", "operator": "unequipped"})},
                      "nodes": [{"id": "a"}]}],
        "project": {"starting_canvas": "start"},
    }


HOLE = [SPORTS, NO_TOP, EXH("lt", 20)]
FIXED = [SPORTS, NO_TOP, NO_DRESS, EXH("lt", 20)]


def test_the_hole_is_found_and_the_fix_closes_it():
    # Adapted from v2's gate test (test_gates_dress_rules.py:55), which went through gates.py; this skill has none.
    holes = reach.dress_rule_holes(game(HOLE))
    assert any("uniform" in o and "No panties" in m for _p, m, _v, o, _by in holes)
    assert reach.dress_rule_holes(game(FIXED)) == []


def test_the_exception_without_no_dress_is_listed():
    assert reach.dress_exception_rows(game(HOLE)) == [("street", "Not in just the sports bra. Not yet. (Needs Exhibitionism 20.)")]
    assert reach.dress_exception_rows(game(FIXED)) == []


def test_a_scene_only_the_hole_opens_is_a_narrow_way():
    ways = reach.narrow_ways(game(HOLE))
    assert ways == [("seen", "street", ["bra sports_bra, dress uniform"])]


def test_once_fixed_the_scene_has_no_way_in_at_all():
    assert reach.narrow_ways(game(FIXED)) == []
    assert "seen" in reach.check(game(FIXED))["scenes"]
