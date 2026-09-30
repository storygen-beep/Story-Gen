"""Gate 42 + DC6b (PRD v2 phase 4 · D2 · J1, 2026-09-30): a locked door says why, once.

A number lock (the engine's `_wants_number` predicate) gets the engine's requirement suffix
and no `locked_text`; `locked_text` on it FAILS as doubled. A story lock (a flag, an `eq`, a
value of 1) still needs a line.

Fixtures are written here; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

V1 = {"version": "1.0", "logic": "AND"}


def trait(op, v, subject="player"):
    it = {"type": "trait", "subject": subject, "trait_key": "nerve", "operator": op, "value": v}
    if subject == "npc":
        it.update(npc_id="npc_vic", trait_key="trust")
    return it


FLAG = {"type": "flag", "subject": "player", "flag_key": "has_key", "operator": "is_true"}


def row(*choices):
    g = {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {"nerve": 0}},
         "locations": [{"id": "room"}],
         "canvases": [{"id": "c", "trigger": {"location": "room"}, "nodes": [{
             "id": "n", "blocks": [{"type": "paragraph", "content": "The door."}],
             "exit_block": {"type": "choices", "choices": list(choices)}}]}]}
    model, g2 = gates.build(copy.deepcopy(g))
    return next(r for r in gates.run_gates(model, g2, None) if r["gate"] == "a locked door says why")


def locked(item, **extra):
    ch = {"text": "Tell him no", "show_when_locked": True, "conditions": dict(V1, items=[item]),
          "targetType": "location", "locationId": "room"}
    ch.update(extra)
    return ch


def test_the_predicate_is_the_engines():
    assert gates._is_number_lock(dict(V1, items=[trait("gte", 40)]))
    assert gates._is_number_lock(dict(V1, items=[trait("gte", 20, "npc")]))     # EN6: his feeling
    assert not gates._is_number_lock(dict(V1, items=[trait("eq", 40)]))
    assert not gates._is_number_lock(dict(V1, items=[trait("gte", 1)]))
    assert not gates._is_number_lock(dict(V1, items=[FLAG]))


# ── pass ──────────────────────────────────────────────────────────────────────

def test_a_bare_number_lock_passes():
    r = row(locked(trait("gte", 40)))
    assert r["headline"].startswith("1 shown-locked · 1 say why once"), r["headline"]
    assert not r["detail"]


def test_a_story_lock_with_a_line_passes():
    r = row(locked(FLAG, locked_text="The door is locked."))
    assert not r["detail"]


def test_a_number_lock_with_a_threshold_toast_passes():
    assert not row(locked(trait("gte", 40), locked_text_threshold="40 nerve"))["detail"]


# ── fail ──────────────────────────────────────────────────────────────────────

def test_a_number_lock_with_locked_text_is_doubled():
    r = row(locked(trait("gte", 40), locked_text="Tell him no"))
    assert "1 doubled" in r["headline"] and "says it twice (J1)" in r["detail"][0]


def test_his_feeling_with_locked_text_is_doubled_too():
    r = row(locked(trait("gte", 20, "npc"), locked_text="He isn't there yet."))
    assert "1 doubled" in r["headline"]


def test_a_bare_story_lock_is_mute():
    r = row(locked(FLAG))
    assert "1 mute" in r["headline"]


def test_an_eq_or_value_one_lock_still_needs_a_line():
    assert "1 mute" in row(locked(trait("eq", 40)))["headline"]
    assert "1 mute" in row(locked(trait("gte", 1)))["headline"]
