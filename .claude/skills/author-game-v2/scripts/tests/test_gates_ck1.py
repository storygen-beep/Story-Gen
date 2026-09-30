"""CK1 (PRD v2, 2026-09-30): the ladder check.

  H1  · `[engine.daily_tick].traitEffects` is a farmable source, honouring each
        effect's `conditions`, and `_player_trait_raises` reads it.
  H2  · the door step (its canvas holds the declared door) skips the earnable check
        and is noted "the door — opens next release".
  H3  · a step with `fires_from = "opening"` skips the place, hours, person-present
        and counter-read checks, `shape.py` row 2, and the reachability filter;
        `playtest.reach_step` plays it from a new game.
  I24 · a separate row: the door's canvas must be re-enterable.

The fixture is written here; nothing in games/ is read or written. The played test
builds the fixture in a temp dir (about 20s). Run from the repo root:

    venv/bin/python -m pytest .claude/skills/author-game-v2/scripts/tests -q
"""
import copy
import os
import subprocess
import sys

import pytest

try:
    import tomllib
except ImportError:                      # py3.10
    import tomli as tomllib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402
import shape  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

# Three steps with Jo:
#   1 · the opening itself sets jo_stage = 1 (fires_from = "opening");
#   2 · jo_2 at the shed needs nights >= 3 — only the day roll adds to nights;
#   3 · jo_3 is the door step: trust >= 50, which nothing in this release raises.
#       Its locked choice "Ask for the key" is the declared door.
FIXTURE_TOML = '''
schema_version = "1.0"

[project]
id              = "ck1_fx"
title           = "CK1 Fixture"
description     = "A ladder whose first step is the opening and whose last holds the door."
starting_canvas = "opening"
quests_engine   = "v2"
version         = "0.1"

[time]
starting_hour = 17
starting_day  = "Monday"
starting_week = 1

[settings]
narration_person = "second"

[player]
id   = "player"
name = "Sam"

[player.core_traits]
jo_stage = 0
nights   = 0
trust    = 0
charm    = 0
money    = 10

[engine.daily_tick]
traitEffects = [
  { targetType = "player", trait = "nights", op = "add", value = 1 },
]

[[locations]]
id               = "yard"
name             = "Yard"
description      = "The yard behind the house."
navigation_order = ["shed"]

[[locations]]
id          = "shed"
name        = "Shed"
description = "The shed at the end of the yard."
entry_from  = "yard"

[[npcs]]
id          = "npc_jo"
name        = "Jo"
core_traits = { relation = 0 }
arc_stages  = ["Stranger", "Talking", "Close", "Hers"]

[[npcs.schedules]]
location   = "shed"
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "18:00"
end_time   = "22:00"

[[canvases]]
id   = "opening"
name = "Opening"
[canvases.trigger]
location      = "yard"
is_repeatable = false
is_active     = true
priority      = 100
[[canvases.nodes]]
id     = "base"
name   = "Opening"
blocks = [ { type = "paragraph", content = "Jo waves at you across the yard." } ]
[canvases.nodes.exit_block]
type = "location"
[canvases.nodes.exit_block.config]
locationId = "yard"
effects    = [
  { targetType = "player", trait = "jo_stage", op = "set", value = 1 },
  { targetType = "player", trait = "charm", op = "add", value = 5 },
]

[[canvases]]
id   = "jo_2"
name = "Jo, the second time"
[canvases.trigger]
location      = "shed"
is_repeatable = false
is_active     = true
npc           = "npc_jo"
priority      = 50
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "jo_stage", operator = "eq", value = 1 },
  { type = "trait", subject = "player", trait_key = "nights", operator = "gte", value = 3 },
] }
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "18:00"
end_time   = "22:00"
[[canvases.nodes]]
id     = "base"
name   = "Second"
blocks = [ { type = "dialog", content = "Three nights. You kept count.", props = { speaker = "npc", npcId = "npc_jo" } } ]
[canvases.nodes.exit_block]
type = "location"
[canvases.nodes.exit_block.config]
locationId = "shed"
effects    = [ { targetType = "player", trait = "jo_stage", op = "set", value = 2 } ]

[[canvases]]
id   = "jo_3"
name = "Jo, the third time"
[canvases.trigger]
location      = "shed"
is_repeatable = false
is_active     = true
npc           = "npc_jo"
priority      = 50
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "jo_stage", operator = "eq", value = 2 },
  { type = "trait", subject = "player", trait_key = "trust", operator = "gte", value = 50 },
] }
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "18:00"
end_time   = "22:00"
[[canvases.nodes]]
id     = "base"
name   = "Third"
blocks = [ { type = "dialog", content = "Not yet.", props = { speaker = "npc", npcId = "npc_jo" } } ]
[canvases.nodes.exit_block]
type = "choices"
[[canvases.nodes.exit_block.choices]]
text             = "Ask for the key"
targetType       = "location"
locationId       = "yard"
show_when_locked = true
locked_text      = "She doesn't trust you with it yet."
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "trust", operator = "gte", value = 80 },
] }
[[canvases.nodes.exit_block.choices]]
text       = "Sit with her"
targetType = "location"
locationId = "shed"
effects    = [ { targetType = "player", trait = "jo_stage", op = "set", value = 3 } ]
'''

WINDOW = {"days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
          "from": "18:00", "to": "22:00"}
DOOR = {"canvas": "jo_3", "choice": "Ask for the key"}


def ladder():
    return {"counter": "jo_stage", "steps": [
        {"n": 1, "canvas": "opening", "fires_from": "opening", "gate": []},
        {"n": 2, "canvas": "jo_2", "where": "shed", "when": dict(WINDOW),
         "gate": [{"trait": "nights", "op": "gte", "value": 3}]},
        {"n": 3, "canvas": "jo_3", "where": "shed", "when": dict(WINDOW),
         "gate": [{"trait": "trust", "op": "gte", "value": 50}]},
    ]}


def state(lad=None, door=DOOR, where="board"):
    s = {"board": {"characters": [{"id": "npc_jo", "ladder": lad or ladder()}]}}
    if door is not None:
        if where == "board":
            s["board"]["door"] = dict(door)
        else:
            s["release_page"] = {"door": dict(door)}
    return s


def game():
    return tomllib.loads(FIXTURE_TOML)


def canvas(g, cid):
    return next(c for c in g["canvases"] if c["id"] == cid)


def problems(g, st=None, notes=None):
    return gates.ladder_problems(g, st if st is not None else state(), notes=notes)[2]


def row(g, st, name):
    model, g2 = gates.build(copy.deepcopy(g))
    return next(r for r in gates.run_gates(model, g2, st) if r["gate"] == name)


def test_the_fixture_ladder_passes():
    assert problems(game()) == []


# ── H1 · the day roll is a farm ───────────────────────────────────────────────

def test_player_trait_raises_reads_the_daily_tick():
    assert "engine" in gates._player_trait_raises(game())["nights"]


def test_without_the_tick_the_nightly_meter_is_unearnable():
    g = game()
    del g["engine"]
    probs = problems(g)
    assert any("jo_2" in p and "nights gte 3" in p for p in probs), probs


def test_a_tick_whose_condition_can_never_hold_does_not_count():
    g = game()
    g["engine"]["daily_tick"]["traitEffects"][0]["conditions"] = {
        "version": "1.0", "logic": "AND",
        "items": [{"type": "flag", "subject": "player", "flag_key": "never_set",
                   "operator": "is_true"}]}
    assert any("nights gte 3" in p for p in problems(g))


def test_a_tick_that_holds_only_above_the_step_does_not_count():
    g = game()
    g["engine"]["daily_tick"]["traitEffects"][0]["conditions"] = {
        "version": "1.0", "logic": "AND",
        "items": [{"type": "trait", "subject": "player", "trait_key": "jo_stage",
                   "operator": "gte", "value": 5}]}
    assert any("nights gte 3" in p for p in problems(g))


def test_a_tick_that_holds_below_the_step_counts():
    g = game()
    g["engine"]["daily_tick"]["traitEffects"][0]["conditions"] = {
        "version": "1.0", "logic": "AND",
        "items": [{"type": "trait", "subject": "player", "trait_key": "jo_stage",
                   "operator": "lt", "value": 2}]}
    assert problems(g) == []


def test_a_tick_capped_below_the_gate_does_not_count():
    g = game()
    g["engine"]["daily_tick"]["traitEffects"][0]["cap"] = 2
    assert any("nights gte 3" in p for p in problems(g))


# ── H2 · the door step ────────────────────────────────────────────────────────

def test_without_a_declared_door_step_three_is_unearnable():
    probs = problems(game(), state(door=None))
    assert any("jo_3" in p and "trust gte 50" in p for p in probs), probs


def test_the_door_step_skips_the_earnable_check_and_is_noted():
    notes = []
    assert problems(game(), state(), notes=notes) == []
    assert notes == ["npc_jo step 3 (jo_3): the door — opens next release"]


def test_the_door_is_read_from_the_release_page():
    notes = []
    assert problems(game(), state(where="release_page"), notes=notes) == []
    assert notes and "the door — opens next release" in notes[0]


def test_the_door_step_still_gets_its_other_checks():
    lad = ladder()
    lad["steps"][2]["where"] = "yard"
    assert any("jo_3" in p and "declared at yard" in p for p in problems(game(), state(lad)))


def test_the_ladder_row_headline_names_the_door():
    r = row(game(), state(), "ladders move forward")
    assert "the door — opens next release" in r["headline"]


# ── H3 · a step that fires from the opening ───────────────────────────────────

def test_an_opening_step_without_fires_from_fails_place_hours_and_counter():
    lad = ladder()
    del lad["steps"][0]["fires_from"]
    probs = problems(game(), state(lad))
    assert any("step 1" in p and "`when` must be a window" in p for p in probs), probs
    assert any("step 1" in p and "declared at None" in p for p in probs), probs
    assert any("step 1" in p and "does not read the counter" in p for p in probs), probs


def test_fires_from_opening_must_be_step_one():
    lad = ladder()
    lad["steps"][1]["fires_from"] = "opening"
    probs = problems(game(), state(lad))
    assert any("step 2" in p and "can only be step 1" in p for p in probs), probs


def test_fires_from_opening_must_name_a_canvas_the_opening_plays():
    lad = ladder()
    lad["steps"][0]["canvas"] = "jo_2"
    probs = problems(game(), state(lad))
    assert any("the opening never plays jo_2" in p for p in probs), probs


def test_an_unknown_fires_from_value_fails():
    lad = ladder()
    lad["steps"][0]["fires_from"] = "morning"
    assert any("the only value is" in p for p in problems(game(), state(lad)))


def test_an_opening_step_skips_the_person_present_check():
    g = game()
    canvas(g, "opening")["trigger"]["npc"] = "npc_jo"      # Jo is at the shed, never the yard
    assert problems(g) == []


def test_an_opening_canvas_with_no_place_still_counts_as_a_setter():
    g = game()
    del canvas(g, "opening")["trigger"]["location"]
    lad = ladder()
    lad["steps"][1]["gate"].append({"trait": "charm", "op": "gte", "value": 5})
    canvas(g, "jo_2")["trigger"]["conditions"]["items"].append(
        {"type": "trait", "subject": "player", "trait_key": "charm",
         "operator": "gte", "value": 5})
    assert problems(g, state(lad)) == []
    assert not gates._ladder_reachable(canvas(g, "opening"))
    assert gates._ladder_reachable(canvas(g, "opening"), frozenset({"opening"}))


def _shape_state(lad):
    return {"phase": "idea", "board": {"locations": [{"id": "shed"}, {"id": "yard"}],
                                       "characters": [{"id": "npc_jo", "ladder": lad}]}}


def test_shape_row_two_skips_an_opening_step():
    r = {n: ok for n, ok, _h, _d in shape.check(_shape_state(ladder()), True)[0]}
    assert r["a step's hours are a window"] is True
    lad = ladder()
    del lad["steps"][0]["fires_from"]
    r = {n: ok for n, ok, _h, _d in shape.check(_shape_state(lad), True)[0]}
    assert r["a step's hours are a window"] is False


# ── I24 · the door can be seen again ──────────────────────────────────────────

def test_a_door_on_a_one_time_canvas_is_seen_once():
    r = row(game(), state(), "the door can be seen again")
    assert r["pass_"] is False and not r["na"]
    assert "the door is seen once" in r["detail"][0]


def test_a_door_on_a_repeatable_canvas_passes():
    g = game()
    canvas(g, "jo_3")["trigger"]["is_repeatable"] = True
    assert row(g, state(), "the door can be seen again")["pass_"] is True


def test_a_door_on_an_en1_canvas_passes_when_the_door_does_not_consume():
    g = game()
    canvas(g, "jo_3")["trigger"]["consume_on"] = "exit"
    assert row(g, state(), "the door can be seen again")["pass_"] is True


def test_a_door_that_consumes_its_en1_canvas_is_seen_once():
    g = game()
    canvas(g, "jo_3")["trigger"]["consume_on"] = "exit"
    canvas(g, "jo_3")["nodes"][0]["exit_block"]["choices"][0]["consumes"] = True
    r = row(g, state(), "the door can be seen again")
    assert r["pass_"] is False and "marked consumes" in r["headline"]


def test_no_declared_door_is_na():
    assert row(game(), state(door=None), "the door can be seen again")["na"] is True


def test_the_door_row_is_not_a_ship_block_row():
    assert "the door can be seen again" not in gates.SHIP_BLOCK_GATES


# ── H3 · played: reach_step starts the opening step from a new game ───────────

@pytest.fixture(scope="module")
def built(tmp_path_factory):
    pytest.importorskip("playwright")
    d = tmp_path_factory.mktemp("ck1_fx")
    src = d / "game.toml"
    src.write_text(FIXTURE_TOML)
    res = subprocess.run([os.path.join(REPO, "venv", "bin", "python"), "manage.py",
                          "package_from_toml", "--file", str(src), "--output", str(d / "out"),
                          "--gen-version", "v2"], cwd=REPO, capture_output=True, text=True)
    assert res.returncode == 0, res.stdout[-2000:] + res.stderr[-2000:]
    return str(d / "out" / "index.html")


def test_reach_step_reaches_an_opening_step_then_the_next(built):
    import playtest
    with playtest.open_game(built) as (page, errors):
        res = playtest.reach_step(page, game(), ladder(), 2)
        assert [r["reached"] for r in res] == [True, True], res
        assert playtest.traits(page)["jo_stage"] == 2
        assert not errors, errors


def test_reach_step_does_not_credit_an_opening_that_never_moves_the_counter(built):
    import playtest
    lad = {"counter": "trust", "steps": [
        {"n": 1, "canvas": "opening", "fires_from": "opening", "gate": []}]}
    with playtest.open_game(built) as (page, errors):
        res = playtest.reach_step(page, game(), lad, 1)
        assert [r["reached"] for r in res] == [False], res
        assert playtest.traits(page)["trust"] == 0


def test_the_ship_ladder_row_reads_the_door_too(tmp_path):
    root = tmp_path / "root"
    (root / "games" / "fx" / "output").mkdir(parents=True)
    ok, head, detail = gates._ship_ladders(str(root), "fx", game(), state(where="release_page"),
                                           ["npc_jo"], player=lambda *a: [])
    assert not any("trust gte 50" in d for d in detail), detail
    assert head == "no build to play"


def _ship_played(tmp_path, st):
    root = tmp_path / "root"
    out = root / "games" / "fx" / "output"
    out.mkdir(parents=True)
    (out / "index.html").write_text("stub")
    handed = []

    def player(build, g, lad):
        handed.append([s["n"] for s in lad["steps"]])
        return [{"n": s["n"], "canvas": s["canvas"], "reached": True} for s in lad["steps"]]
    return gates._ship_ladders(str(root), "fx", game(), st, ["npc_jo"], player=player), handed


def test_the_played_half_skips_the_door_step(tmp_path):
    (ok, head, detail), handed = _ship_played(tmp_path, state(where="release_page"))
    assert handed == [[1, 2]]
    assert ok is True, (head, detail)
    assert "not played, the door — opens next release: npc_jo step 3 (jo_3)" in head


def test_the_played_half_plays_every_step_without_a_door(tmp_path):
    g_state = state(door=None)
    g_state["board"]["characters"][0]["ladder"]["steps"][2]["gate"] = []   # static half green
    g = game()
    canvas(g, "jo_3")["trigger"]["conditions"]["items"].pop()
    root = tmp_path / "root"
    (root / "games" / "fx" / "output").mkdir(parents=True)
    (root / "games" / "fx" / "output" / "index.html").write_text("stub")
    handed = []
    ok, head, _ = gates._ship_ladders(
        str(root), "fx", g, g_state, ["npc_jo"],
        player=lambda b, gg, lad: handed.append([s["n"] for s in lad["steps"]]) or
        [{"n": s["n"], "reached": True} for s in lad["steps"]])
    assert handed == [[1, 2, 3]] and ok is True and "not played" not in head
