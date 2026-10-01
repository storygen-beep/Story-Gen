"""The labels lint reads meters (World and Systems PRD S1b-code, 2026-10-01): `board.meters[]`,
plus any old meter-shaped `board.systems[]` entry (a `kind`, no card field). A system card in
`board.systems[]` is never read as a meter. Minimal fixtures built here; nothing in games/ is read.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

METER = {"id": "look", "kind": "sourced", "key": "grooming", "fed_at": ["office"],
         "labels": ["has_mirror"], "read_by": "x"}
CARD = {"id": "bar", "name": "The bar", "place": "office", "one_ladder": True,
        "people": ["npc_a"], "leads_to": ["npc_a"]}
ROOMS = [{"id": "office", "labels": ["has_mirror"]}]


def canvas(loc, sets=(), reads=()):
    return {"loc": loc, "sets": set(sets), "reads": set(reads), "raw": {}}


def run(board, model=()):
    return gates.lint_labels_and_systems(list(model), "fx", {"board": board})


def test_old_shape_systems_still_read_as_meters():
    summary, findings = run({"systems": [METER], "locations": ROOMS})
    assert summary.startswith("1 meters declared (1 sourced)")
    assert any("meter `look`: nothing at office writes `grooming`" in f for f in findings)


def test_board_meters_read():
    summary, findings = run({"meters": [METER], "locations": ROOMS})
    assert summary.startswith("1 meters declared (1 sourced)")
    assert any("meter `look`" in f for f in findings)


def test_card_is_not_a_meter():
    summary, findings = run({"systems": [CARD], "meters": [METER], "locations": ROOMS})
    assert summary.startswith("1 meters declared")
    assert not any("`bar`" in f for f in findings)


def test_fed_and_read_meter_is_clean():
    model = [canvas("office", sets=["grooming"]), canvas("street", reads=["grooming"])]
    summary, findings = run({"meters": [METER], "locations": ROOMS}, model)
    assert findings == []


def test_nothing_declared():
    summary, findings = run({"systems": [CARD]})
    assert summary.startswith("no board.meters[]") and findings == []
