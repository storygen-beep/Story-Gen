"""Two switches on a location screen that used to do nothing.

A location renders two lists: `renderNpcPortraits` takes every canvas carrying
`npcId`, `renderSoloActivities` takes every canvas without one. Two author-facing
trigger fields were supposed to gate what appears there, and neither did.

  1. **`requires_npc`** — "only offer this while that character is here." It was read
     on exactly two paths, `trigger_mode = "random"` and `substitution_only`, so on an
     ordinary manual repeatable canvas it was INERT. Writing it and omitting it played
     identically, so authors omitted it: of 61 solo-lane canvases bound to a person
     corpus-wide, 7 declared it. It now gates the solo lane too, through
     `setup._npcPresentForCanvas`.

  2. **`is_active = false`** — the author's off switch. A real column on CanvasTrigger,
     written by both build paths, and read by NOTHING in this generator. Four canvases
     across two games shipped switched ON after their authors switched them off — one
     of them `forty_miles/canvas_back_room_key`, whose whole job was to stay dark so
     v0.1's back-room door stayed locked. Entering the stock room opened it. Now gated
     through `setup.isCanvasSelectable`.

⚠️ THE TRAP, and the reason `isCanvasValid` must stay clean. `is_active = false` means
"never surfaces on its own" — it does NOT mean unaddressable. `the_allowance`'s three
bathroom walk-ins declare the flag AND are substitution targets of `activity_wash`
(0.32/0.30/0.28). `_tryRule` resolves them through `setup.getCanvasById`, which builds
its map from `help_data.locationCanvases`. Drop an inactive canvas from that index, or
fold the check into the shared `isCanvasValid`, and three tier-4 explicit scenes stop
firing — silently, with no build error, invisible until somebody plays a wash. Tests 3
and 10 are the guards; do not delete them.

⚠️ `isCanvasValid` is also the auto-fire selector's validator, and 78 non-repeatable
one-shot meetings across 8 games hang off it. Presence lives in `_npcPresentForCanvas`,
the on/off switch in `isCanvasSelectable`, and neither belongs in `isCanvasValid`.

⚠️ Targets **v2** and the no-DB graph path, as `test_location_door.py` does — that is
the path a real build takes.

Run with an explicit path — pyproject sets testpaths = ["tests"], so app suites are
not collected by a bare `pytest`:

    pytest apps/game_generation/tests/test_canvas_presence_and_active.py -q
"""
import copy
import json
import os
import re

import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml

FIXTURE = "apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml"
KITCHEN = "loc_kitchen"
NPC = "npc_frank"


# ── fixture surgery ──────────────────────────────────────────────────────────
# The fixture has two locations, one NPC with NO schedules, and no canvas carrying
# either field, so every test injects what it needs.


def _raw():
    return parse_toml(FIXTURE)


def _scheduled(d, location=KITCHEN, start="06:00", end="10:00"):
    """`getNpcLocation` resolves nothing for an NPC with no declared schedule, so a
    presence gate on one would hide the row at every hour. Give Frank a window."""
    for npc in d["npcs"]:
        if npc["id"] == NPC:
            npc["schedules"] = [
                {
                    "location": location,
                    "start_time": start,
                    "end_time": end,
                    "weekdays": [0, 1, 2, 3, 4, 5, 6],
                }
            ]
    return d


def _canvas(cid, **trigger):
    trig = {"location": KITCHEN, "is_repeatable": True, "priority": 4, "is_active": True}
    trig.update(trigger)
    return {
        "id": cid,
        "name": cid.replace("_", " ").title(),
        "trigger": trig,
        "nodes": [
            {
                "id": "base",
                "name": "Base",
                "blocks": [{"type": "paragraph", "content": "A thing happens here."}],
                "exit_block": {
                    "type": "location",
                    "text": "Leave.",
                    "config": {"destinationType": "specific", "locationId": KITCHEN},
                },
            }
        ],
    }


def _twee(d):
    graph = build_game_graph(normalize(d))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def _location_canvases(twee):
    """The `locationCanvases` blob out of the emitted help_data, as Python."""
    i = twee.find('"locationCanvases"')
    assert i != -1, "no locationCanvases in the build"
    depth, start = 0, twee.index("{", i)
    for j in range(start, len(twee)):
        if twee[j] == "{":
            depth += 1
        elif twee[j] == "}":
            depth -= 1
            if depth == 0:
                return json.loads(twee[start : j + 1])
    raise AssertionError("unbalanced locationCanvases blob")


def _entry(twee, canvas_id):
    for rows in _location_canvases(twee).values():
        for row in rows:
            if row.get("id") == canvas_id:
                return row
    return None


def _fn_body(twee, name):
    """One `setup.<name> = function(...) {...}` body out of the emitted JS."""
    m = re.search(r"setup\.%s = function\([^)]*\) \{" % re.escape(name), twee)
    assert m, f"{name} not emitted"
    depth, start = 0, m.end() - 1
    for j in range(start, len(twee)):
        if twee[j] == "{":
            depth += 1
        elif twee[j] == "}":
            depth -= 1
            if depth == 0:
                return twee[start : j + 1]
    raise AssertionError(f"unbalanced body for {name}")


# ── 1. emission ──────────────────────────────────────────────────────────────


def test_both_fields_reach_the_payload():
    """Hop 4 — the field exists on the trigger and reaches help_data, on the graph
    path, which is the one a real build takes."""
    d = _scheduled(_raw())
    d["canvases"].append(_canvas("gated", requires_npc=NPC))
    row = _entry(_twee(d), "gated")
    assert row is not None
    assert row["requiresNpc"] == NPC
    assert row["isActive"] is True


def test_is_active_defaults_true_when_unwritten():
    """A key nobody writes must not read as off. Every canvas in every existing game
    omits it."""
    d = _raw()
    c = _canvas("plain")
    del c["trigger"]["is_active"]
    d["canvases"].append(c)
    assert _entry(_twee(d), "plain")["isActive"] is True


def test_is_active_false_reaches_the_payload_as_false():
    d = _raw()
    d["canvases"].append(_canvas("switched_off", is_active=False))
    assert _entry(_twee(d), "switched_off")["isActive"] is False


def test_an_inactive_canvas_STAYS_in_locationCanvases():
    """⚠️ The substitution guard. `setup.getCanvasById` builds `_canvasByIdMap` from
    this index and `_tryRule` resolves substitution targets through it. Prune an
    inactive canvas from here and `the_allowance`'s three bathroom walk-ins — all
    three `is_active = false` AND substitution targets of `activity_wash` — stop
    firing for good, with no error anywhere."""
    d = _raw()
    d["canvases"].append(_canvas("switched_off", is_active=False))
    assert _entry(_twee(d), "switched_off") is not None


def test_an_inactive_canvas_still_has_its_passages():
    """Same reason: `_tryRule` returns `target.passageName` and the caller `<<goto>>`s
    it. No passage, no scene — and that one fails loudly, mid-play."""
    d = _raw()
    d["canvases"].append(_canvas("switched_off", is_active=False))
    assert "Canvas_switched_off_Node_base" in _twee(d)


# ── 2. the shape of the emitted engine ───────────────────────────────────────
# String assertions over generated JS: ugly, and exactly right for a generator whose
# output is JS inside f-strings. `test_location_door.py` uses the same idiom.

SRC = None


def _src():
    global SRC
    if SRC is None:
        SRC = _twee(_raw())
    return SRC


def test_the_solo_selector_checks_presence_after_the_npcId_split():
    body = _fn_body(_src(), "selectSoloActivityCanvasesForLocation")
    assert "_npcPresentForCanvas(c, locationId)" in body
    assert body.index("c.npcId") < body.index("_npcPresentForCanvas")


def test_the_solo_blocked_loop_hides_rather_than_explaining():
    """The guard sits above BOTH `showWhenBlocked` branches and the cost branch, so
    one line covers the affordable, the cost-blocked and the cooldown collections.
    "He is not here" is not a cooldown, and `cooldownMessage` defaults to "Available
    again later" — surfacing it there would be a lie."""
    body = _fn_body(_src(), "renderSoloActivities")
    assert "_npcPresentForCanvas(c, locationId)" in body
    # on the branch, not the word — the function's own doc comment names showWhenBlocked
    assert body.index("_npcPresentForCanvas") < body.index("if (c.showWhenBlocked)")


def test_isCanvasValid_stays_clean():
    """⚠️ The guard-rail for both no-touch rules. This is the shared chokepoint: the
    auto-fire selector calls it (78 one-shot meetings across 8 games would tighten at
    once) and so does `_tryRule` on a substitution target."""
    body = _fn_body(_src(), "isCanvasValid")
    assert "requiresNpc" not in body
    assert "isActive" not in body


def test_the_substitution_path_keeps_the_bare_validator():
    """⚠️ The asymmetry IS the design. `_tryRule` must call `isCanvasValid`, never
    `isCanvasSelectable`, or an inactive canvas stops being a substitution target."""
    src = _src()
    i = src.index("var _tryRule = function(s)")
    rule = src[i : i + 800]
    assert "setup.isCanvasValid(target)" in rule
    # the CALL, not the word — the comment beside it names what it must not call
    assert "setup.isCanvasSelectable(target)" not in rule


def test_every_selection_path_goes_through_isCanvasSelectable():
    """Six sites: auto-fire, portrait selector, solo selector, both inline blocked
    loops, and random encounters. Seventh occurrence is the delegation inside
    loops, and random encounters. The definition reads `= function(`, so it does not
    count as a call site."""
    src = _src()
    assert src.count("setup.isCanvasSelectable(") == 6


# ── 3. corpus guards ─────────────────────────────────────────────────────────
# skipif on the merged TOML, matching test_nodb_equivalence.py.

ALLOWANCE = "games/the_allowance/toml_phases/7_final_game.toml"
FORTY = "games/forty_miles/toml_phases/7_final_game.toml"


@pytest.mark.skipif(not os.path.exists(ALLOWANCE), reason="the_allowance not present")
def test_the_allowance_walkins_are_still_resolvable_substitution_targets():
    """The regression test for the whole design. All three carry `is_active = false`
    AND are targets of `activity_wash`. They must be off as standalone rows and still
    resolvable by id."""
    twee = _twee(parse_toml(ALLOWANCE))
    for cid in ("walkin_joss_wash", "walkin_gareth_wash", "walkin_martin_wash"):
        row = _entry(twee, cid)
        assert row is not None, f"{cid} was pruned — substitutions into it are dead"
        assert row["isActive"] is False


@pytest.mark.skipif(not os.path.exists(FORTY), reason="forty_miles not present")
def test_forty_miles_keeps_its_located_setter():
    """`canvas_back_room_key` ships inactive so v0.1's door stays shut, and exists at
    all so the flag-chain validator can resolve `back_room_key`. Suppressing it must
    not cost it that job — teaching `_build_flag_unlock_map` about `is_active` would
    hard-fail this build with `✗ back_room_key — NEVER SET`."""
    d = parse_toml(FORTY)
    graph = build_game_graph(normalize(d))
    gen = TweeComprehensiveGeneratorV2()
    twee = gen.generate(graph.project, {}, graph=graph)
    row = _entry(twee, "canvas_back_room_key")
    assert row is not None and row["isActive"] is False
    errors = [e for e in (gen.validate_flag_chains() or []) if "back_room_key" in str(e)]
    assert not errors, errors
