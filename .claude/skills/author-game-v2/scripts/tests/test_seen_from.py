"""A step seen from the next room (`seen_from`), checked in two halves.

  shape.py  `the person is there at the step's hour` — the person's rows at the step's place OR at
            its `seen_from` must cover the whole window (the ledger alone).
  gates.py  `a step is seen from the next room` — once the TOML exists, `seen_from` shares a parent
            (`entry_from`) with the step's place. A scored gate (never a --ship BLOCK). n/a: no step
            declares `seen_from`. Grandfathered games WARN until they ship since SEEN_FROM_SINCE;
            billable_hours is not grandfathered.

Fixtures are written here; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402
import shape  # noqa: E402

WIN = {"days": ["Mon", "Tue"], "from": "21:00", "to": "23:30"}


def ledger(seen_from=None, rows_at="ethan_room", slug="billable_hours", releases=None):
    step = {"n": 1, "canvas": "shower", "where": "bathroom", "when": dict(WIN), "hint": "…"}
    if seen_from:
        step["seen_from"] = seen_from
    st = {"slug": slug, "board": {"characters": [{
        "id": "npc_ethan",
        "schedule": [{"where": rows_at, "weekdays": ["Mon", "Tue"], "from": "21:00", "to": "23:30"}],
        "ladder": {"counter": "ethan_stage", "steps": [step]}}]}}
    if releases:
        st["releases"] = releases
    return st


# ── shape.py ────────────────────────────────────────────────────────────────

def there(state):
    return next((ok, d) for n, ok, h, d in shape.check(state, False)[0]
                if n == "the person is there at the step's hour")


def test_same_room_passes():
    assert there(ledger(rows_at="bathroom"))[0] is True


def test_seen_from_with_the_person_scheduled_there_passes():
    assert there(ledger(seen_from="ethan_room"))[0] is True


def test_seen_from_without_him_fails():
    ok, detail = there(ledger(seen_from="kitchen"))
    assert ok is False and "bathroom or kitchen" in detail[0]


def test_no_seen_from_and_him_next_door_fails_as_before():
    assert there(ledger())[0] is False


# ── gates.py ────────────────────────────────────────────────────────────────

def house():
    return {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {}},
            "locations": [{"id": "street"}, {"id": "house", "entry_from": "street"},
                          {"id": "kitchen", "entry_from": "house"},
                          {"id": "landing", "entry_from": "house"},
                          {"id": "bathroom", "entry_from": "landing"},
                          {"id": "ethan_room", "entry_from": "landing"}],
            "canvases": [{"id": "shower", "trigger": {"location": "bathroom"},
                          "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "Here."}]}]}]}


def row(state):
    model, g2 = gates.build(copy.deepcopy(house()))
    return next(r for r in gates.run_gates(model, g2, state)
                if r["gate"] == "a step is seen from the next room")


def test_a_sibling_room_passes():
    assert row(ledger(seen_from="ethan_room"))["pass_"] is True


def test_a_room_with_another_parent_is_red():
    r = row(ledger(seen_from="kitchen"))
    assert r["pass_"] is False and "not the room next door" in r["detail"][0]


def test_an_undeclared_room_is_red():
    assert row(ledger(seen_from="attic"))["pass_"] is False


def test_grandfathered_warns_then_blocks_once_shipped_since():
    r = row(ledger(seen_from="kitchen", slug="members_only"))
    assert r["pass_"] is True and r["detail"][0].startswith("warn (grandfathered")
    r = row(ledger(seen_from="kitchen", slug="members_only",
                   releases=[{"version": "0.4", "shipped": gates.SEEN_FROM_SINCE}]))
    assert r["pass_"] is False


def test_no_seen_from_is_na_and_it_is_not_a_ship_block():
    assert row(ledger())["na"] is True
    assert "a step is seen from the next room" not in gates.SHIP_BLOCK_GATES
