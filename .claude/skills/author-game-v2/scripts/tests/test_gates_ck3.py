"""CK3 (PRD v2, 2026-09-30): meter ceiling for a falling meter.

The band that holds a meter's starting value is not a promise, and a meter declared
`falling = true` in [[traits.labels]] is not judged. A rising meter is judged as before.
The fixture is written here; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

FALLING_BANDS = [{"min": 0, "max": 39, "text": "filthy"}, {"min": 40, "max": 59, "text": "grubby"},
                 {"min": 60, "max": 89, "text": "fine"}, {"min": 90, "text": "spotless"}]
RISING_BANDS = [{"min": 0, "max": 14, "text": "a"}, {"min": 15, "max": 34, "text": "b"},
                {"min": 35, "max": 54, "text": "c"}, {"min": 55, "max": 74, "text": "d"},
                {"min": 75, "text": "e"}]


def game(key, start, bands, gate_at, labels=None, npc=None):
    """One sidebar meter, and one canvas gated at `key >= gate_at`."""
    subject = {"type": "trait", "subject": "npc" if npc else "player", "trait_key": key,
               "operator": "gte", "value": gate_at}
    if npc:
        subject["npc_id"] = npc
    g = {
        "project": {"id": "fx", "name": "fx"},
        "player": {"core_traits": {} if npc else {key: start}},
        "locations": [{"id": "room"}],
        "sidebar_items": [{"trait": key, "bands": bands, **({"npc_id": npc} if npc else {})}],
        "canvases": [{"id": "c", "trigger": {"location": "room", "conditions": {
            "version": "1.0", "logic": "AND", "items": [subject]}},
            "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "Here."}]}]}],
    }
    if npc:
        g["npcs"] = [{"id": npc, "name": "Jo", "core_traits": {key: start}}]
    if labels:
        g["traits"] = {"labels": labels}
    return g


def row(g):
    model, g2 = gates.build(copy.deepcopy(g))
    return next(r for r in gates.run_gates(model, g2, None) if r["gate"] == "meter ceiling")


def lines(g, key):
    return [d for d in row(g)["detail"] if d.startswith(f"{key}:")]


def test_the_band_holding_the_start_is_not_a_promise():
    assert lines(game("clean", 100, FALLING_BANDS, 60), "clean") == []


def test_a_falling_meter_is_still_judged_below_its_start():
    got = lines(game("clean", 100, FALLING_BANDS, 40), "clean")
    assert got == ["clean: bands promise something at 60, but the highest authored gate is 40"]


def test_a_rising_meter_is_still_judged_at_its_top_band():
    got = lines(game("heat", 0, RISING_BANDS, 55), "heat")
    assert got == ["heat: bands promise something at 75, but the highest authored gate is 55"]
    assert lines(game("heat", 0, RISING_BANDS, 75), "heat") == []


def test_a_meter_declared_falling_is_not_judged():
    labels = [{"key": "battery", "hidden": True, "falling": True}]
    assert lines(game("battery", 50, FALLING_BANDS, 10, labels=labels), "battery") == []
    assert lines(game("battery", 50, FALLING_BANDS, 10), "battery")      # undeclared: judged


def test_an_npc_meter_uses_the_npcs_starting_value():
    assert lines(game("trust", 100, FALLING_BANDS, 60, npc="npc_jo"), "trust") == []
    got = lines(game("trust", 0, FALLING_BANDS, 60, npc="npc_jo"), "trust")
    assert got == ["trust: bands promise something at 90, but the highest authored gate is 60"]
