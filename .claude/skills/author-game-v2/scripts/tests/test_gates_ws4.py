"""The ladder check (PRD WS4, 2026-09-26): each declared step matches its canvas, each
unlock is earnable, the step really fires in a built game, G7 no longer credits an
`is_false` read, and the growth lint. The fixture game is written and BUILT in a temp
dir (about 20s); nothing in games/ is read or written. Run from the repo root:

    venv/bin/python -m pytest .claude/skills/author-game-v2/scripts/tests -q
"""
import copy
import json
import os
import shutil
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

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))

# Three steps with Jo at the shed, each gated on something else the player has to earn:
#   1 · intro_done (the opening sets it)
#   2 · charm >= 4 (the repeatable `chat` adds 2 a visit)
#   3 · note_found (the one-time `the_note` in the yard) — and the counter moves only on
#       the second screen, so the search has to pick "Stay" over "Go back".
FIXTURE_TOML = '''
schema_version = "1.0"

[project]
id              = "ladder_fx"
title           = "Ladder Fixture"
description     = "A three-step ladder, built to be played by a test."
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
charm    = 0
money    = 10

[[locations]]
id               = "yard"
name             = "Yard"
description      = "The yard behind the house."
navigation_order = ["shed"]

[[locations]]
id               = "shed"
name             = "Shed"
description      = "The shed at the end of the yard."
entry_from       = "yard"

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
blocks = [ { type = "paragraph", content = "You are in the yard." } ]
[canvases.nodes.exit_block]
type = "location"
[canvases.nodes.exit_block.config]
locationId  = "yard"
flagEffects = [ { targetType = "player", flag = "intro_done", op = "set" } ]

[[canvases]]
id   = "chat"
name = "Talk to Jo"
[canvases.trigger]
location      = "shed"
is_repeatable = true
is_active     = true
npc           = "npc_jo"
conditions = { version = "1.0", logic = "AND", items = [
  { type = "flag", subject = "player", flag_key = "intro_done", operator = "is_true" },
] }
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "18:00"
end_time   = "22:00"
[[canvases.nodes]]
id     = "base"
name   = "Talk"
blocks = [ { type = "dialog", content = "Hey.", props = { speaker = "npc", npcId = "npc_jo" } } ]
[canvases.nodes.exit_block]
type = "location"
[canvases.nodes.exit_block.config]
locationId = "shed"
effects    = [ { targetType = "player", trait = "charm", op = "add", value = 2 } ]

[[canvases]]
id   = "the_note"
name = "A note"
[canvases.trigger]
location      = "yard"
is_repeatable = false
is_active     = true
conditions = { version = "1.0", logic = "AND", items = [
  { type = "flag", subject = "player", flag_key = "intro_done", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "note_found", operator = "is_false" },
] }
[[canvases.nodes]]
id     = "base"
name   = "The note"
blocks = [ { type = "paragraph", content = "A note is pinned to the gate." } ]
[canvases.nodes.exit_block]
type = "location"
[canvases.nodes.exit_block.config]
locationId  = "yard"
flagEffects = [ { targetType = "player", flag = "note_found", op = "set" } ]

[[canvases]]
id   = "jo_1"
name = "Jo, the first time"
[canvases.trigger]
location      = "shed"
is_repeatable = false
is_active     = true
npc           = "npc_jo"
priority      = 50
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "jo_stage", operator = "eq", value = 0 },
  { type = "flag", subject = "player", flag_key = "intro_done", operator = "is_true" },
] }
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "18:00"
end_time   = "22:00"
[[canvases.nodes]]
id     = "base"
name   = "First"
blocks = [ { type = "dialog", content = "You again.", props = { speaker = "npc", npcId = "npc_jo" } } ]
[canvases.nodes.exit_block]
type = "location"
[canvases.nodes.exit_block.config]
locationId = "shed"
effects    = [ { targetType = "player", trait = "jo_stage", op = "set", value = 1 } ]

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
  { type = "trait", subject = "player", trait_key = "charm", operator = "gte", value = 4 },
] }
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "18:00"
end_time   = "22:00"
[[canvases.nodes]]
id     = "base"
name   = "Second"
blocks = [ { type = "dialog", content = "Sit down, then.", props = { speaker = "npc", npcId = "npc_jo" } } ]
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
  { type = "flag", subject = "player", flag_key = "note_found", operator = "is_true" },
] }
[[canvases.trigger.schedules]]
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "18:00"
end_time   = "22:00"
[[canvases.nodes]]
id     = "base"
name   = "Third"
blocks = [ { type = "dialog", content = "You read it.", props = { speaker = "npc", npcId = "npc_jo" } } ]
[canvases.nodes.exit_block]
type = "choices"
[[canvases.nodes.exit_block.choices]]
text       = "Go back to the yard"
targetType = "location"
locationId = "yard"
[[canvases.nodes.exit_block.choices]]
text       = "Stay"
targetType = "node"
nodeId     = "stay"
[[canvases.nodes]]
id     = "stay"
name   = "Stay"
blocks = [ { type = "dialog", content = "Good.", props = { speaker = "npc", npcId = "npc_jo" } } ]
[canvases.nodes.exit_block]
type = "location"
[canvases.nodes.exit_block.config]
locationId = "shed"
effects    = [ { targetType = "player", trait = "jo_stage", op = "set", value = 3 } ]
'''

WINDOW = {"days": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
          "from": "18:00", "to": "22:00"}


def ladder():
    return {"counter": "jo_stage", "steps": [
        {"n": 1, "canvas": "jo_1", "where": "shed", "when": dict(WINDOW),
         "gate": [{"flag": "intro_done"}]},
        {"n": 2, "canvas": "jo_2", "where": "shed", "when": dict(WINDOW),
         "gate": [{"trait": "charm", "op": "gte", "value": 4}]},
        {"n": 3, "canvas": "jo_3", "where": "shed", "when": dict(WINDOW),
         "gate": [{"flag": "note_found"}]},
    ]}


def state(lad=None, **extra):
    s = {"board": {"characters": [{"id": "npc_jo", "ladder": lad or ladder()}]}}
    s.update(extra)
    return s


def game():
    return tomllib.loads(FIXTURE_TOML)


def canvas(g, cid):
    return next(c for c in g["canvases"] if c["id"] == cid)


def problems(g, st=None):
    return gates.ladder_problems(g, st if st is not None else state())[2]


def verdict(g, st, name):
    model, g2 = gates.build(copy.deepcopy(g))
    r = next(r for r in gates.run_gates(model, g2, st) if r["gate"] == name)
    # These fixtures test the gate's LOGIC on a handful of cases. "too few to judge"
    # (PRD IC21) means the logic passed on a sample under 5, so it reads as True here;
    # the sample-size rule itself is tested in test_gates_ic21.py.
    return None if r["na"] else (r["pass_"] or r.get("few", False)), r


# ── the static gate ──────────────────────────────────────────────────────────

def test_three_step_ladder_passes():
    assert problems(game()) == []
    ok, r = verdict(game(), state(), "ladders move forward")
    assert ok is True, r


def test_no_ladder_is_na():
    ok, r = verdict(game(), {"board": {"characters": [{"id": "npc_jo"}]}}, "ladders move forward")
    assert ok is None


def test_removing_step_twos_counter_set_fails():
    g = game()
    canvas(g, "jo_2")["nodes"][0]["exit_block"]["config"]["effects"] = []
    p = problems(g)
    assert any("step 2" in x and "no exit sets jo_stage to 2" in x for x in p), p
    ok, _ = verdict(g, state(), "ladders move forward")
    assert ok is False


def test_schedule_mismatch_fails():
    lad = ladder()
    lad["steps"][1]["when"]["to"] = "21:00"
    p = problems(game(), state(lad))
    assert any("step 2" in x and "hours are 18:00-22:00" in x for x in p), p
    lad = ladder()
    lad["steps"][2]["when"]["days"] = ["Fri"]
    p = problems(game(), state(lad))
    assert any("step 3" in x and "declared days" in x for x in p), p


def test_place_mismatch_fails():
    lad = ladder()
    lad["steps"][0]["where"] = "yard"
    assert any("step 1" in x and "fires at shed" in x for x in problems(game(), state(lad)))


def test_when_must_be_a_window():
    lad = ladder()
    lad["steps"][0]["when"] = {"days": ["Mon"]}
    assert any("must be a window" in x for x in problems(game(), state(lad)))


def test_gate_must_match_the_canvas_conditions():
    lad = ladder()
    lad["steps"][1]["gate"] = []                          # the canvas still needs charm >= 4
    assert any("also needs charm gte 4" in x for x in problems(game(), state(lad)))
    lad = ladder()
    lad["steps"][1]["gate"].append({"flag": "note_found"})   # declared, not checked
    assert any("which the canvas does not check" in x for x in problems(game(), state(lad)))


def test_counter_must_shut_the_step():
    g = game()
    it = canvas(g, "jo_1")["trigger"]["conditions"]["items"][0]
    it["operator"], it["value"] = "lt", 5                  # true at 0 and still true at 1
    assert any("still true at jo_stage = 1" in x for x in problems(g))


def test_person_must_be_there():
    g = game()
    g["npcs"][0]["schedules"][0]["weekdays"] = [0, 1, 2, 3, 4]
    p = problems(g)
    assert any("does not fully cover shed" in x and "Sat, Sun" in x for x in p), p   # CK8b wording


def test_unearnable_meter_fails():
    g = game()
    canvas(g, "chat")["nodes"][0]["exit_block"]["config"]["effects"] = []
    p = problems(g)
    assert any("step 2" in x and "charm gte 4" in x and "only to 0" in x for x in p), p


def test_one_time_raises_are_summed():
    g = game()
    ch = canvas(g, "chat")
    ch["trigger"]["is_repeatable"] = False                 # one visit: +2 of the 4 needed
    assert any("only to 2" in x for x in problems(g))


def test_unlock_that_opens_only_after_the_step_fails():
    g = game()
    canvas(g, "the_note")["trigger"]["conditions"]["items"].append(
        {"type": "trait", "subject": "player", "trait_key": "jo_stage",
         "operator": "gte", "value": 3})
    p = problems(g)
    assert any("step 3" in x and "note_found" in x and "sets it" in x for x in p), p


def test_dev_canvas_is_not_a_step():
    g = game()
    canvas(g, "jo_1")["trigger"]["conditions"]["items"].append(
        {"type": "flag", "subject": "player", "flag_key": "dev_mode_enabled",
         "operator": "is_true"})
    assert any("dev canvas" in x for x in problems(g))


# ── G7: an is_false read opens nothing ───────────────────────────────────────

def _g7_game(op):
    return {
        "project": {"id": "g7", "starting_canvas": "m1"},
        "locations": [{"id": "a"}],
        "canvases": [
            {"id": "m1", "trigger": {"location": "a", "is_repeatable": False},
             "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "It happens."}],
                        "exit_block": {"config": {"flagEffects": [{"flag": "x", "op": "set"}]}}}]},
            {"id": "hub", "trigger": {"location": "a", "is_repeatable": True, "conditions": {
                "version": "1.0", "logic": "AND", "items": [
                    {"type": "flag", "subject": "player", "flag_key": "x", "operator": op}]}},
             "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "Again."}]}]},
        ]}


def test_g7_does_not_credit_is_false():
    assert verdict(_g7_game("is_true"), None, "milestones open something")[0] is True
    assert verdict(_g7_game("is_false"), None, "milestones open something")[0] is False


def test_g7_still_credits_a_callback_line():
    g = _g7_game("is_false")
    g["canvases"][1]["nodes"][0]["blocks"].append(
        {"type": "group", "conditions": {"version": "1.0", "logic": "AND", "items": [
            {"type": "flag", "subject": "player", "flag_key": "x", "operator": "is_true"}]},
         "blocks": [{"type": "paragraph", "content": "You remember."}]})
    assert verdict(g, None, "milestones open something")[0] is True


# ── the growth lint ──────────────────────────────────────────────────────────

def _model():
    return gates.build(game())[0]


def test_growth_lint_first_release_prints_a_baseline():
    s, rows = gates.lint_repeatables_without_step(_model(), state())
    assert s.startswith("first release: 1 repeatables, 3 declared steps") and rows == []


def test_growth_lint_lists_repeatables_added_with_no_step():
    st = state(releases=[{"version": "0.1", "repeatables": [], "ladder_steps": 3}])
    s, rows = gates.lint_repeatables_without_step(_model(), st)
    assert "no declared step" in s and rows == ["chat"]


def test_growth_lint_quiet_when_a_step_was_added():
    st = state(releases=[{"version": "0.1", "repeatables": [], "ladder_steps": 2}])
    s, rows = gates.lint_repeatables_without_step(_model(), st)
    assert "1 steps added" in s and rows == []


# ── the --ship row ───────────────────────────────────────────────────────────

def ship_row(tmp_path, st, player=None, built=None):
    root = tmp_path / "root"
    out = root / "games" / "fx" / "output"
    out.mkdir(parents=True, exist_ok=True)
    if built:
        shutil.copy(built, out / "index.html")
    return gates._ship_ladders(str(root), "fx", game(), st, ["npc_jo"], player=player)


def test_ship_row_red_without_a_ladder(tmp_path):
    ok, head, detail = ship_row(tmp_path, {"board": {"characters": [{"id": "npc_jo"}]}})
    assert ok is False and "no board.characters[].ladder" in detail[0]


def test_ship_row_red_on_a_static_problem_and_not_played(tmp_path):
    lad = ladder()
    lad["steps"][1]["when"]["to"] = "21:00"
    played = []
    ok, head, _ = ship_row(tmp_path, state(lad), player=lambda *a: played.append(a) or [])
    assert ok is False and "not played" in head and not played


def test_ship_row_red_when_a_step_does_not_fire(tmp_path):
    stub = lambda b, g, lad: [{"n": 1, "canvas": "jo_1", "reached": True},
                              {"n": 2, "canvas": "jo_2", "reached": False, "why": "not offered"}]
    ok, head, detail = ship_row(tmp_path, state(), player=stub, built=__file__)
    assert ok is False and "reached 1 of 3" in detail[0]


def test_ship_row_na_when_the_page_names_nobody(tmp_path, monkeypatch):
    sys.path.insert(0, HERE)
    import test_gates_ws6 as ws6
    st = ws6.green_state()
    st["release_page"]["people"] = []
    b, block, _ = ws6.rows(tmp_path, monkeypatch, state=st, ladder=None)
    assert b[gates.SHIP_LADDER_ROW] is None
    assert b["the build matches the release page"] is False


# ── the built fixture, played ────────────────────────────────────────────────

@pytest.fixture(scope="module")
def built(tmp_path_factory):
    pytest.importorskip("playwright")
    d = tmp_path_factory.mktemp("ladder_fx")
    src = d / "game.toml"
    src.write_text(FIXTURE_TOML)
    res = subprocess.run([os.path.join(REPO, "venv", "bin", "python"), "manage.py",
                          "package_from_toml", "--file", str(src), "--output", str(d / "out"),
                          "--gen-version", "v2"], cwd=REPO, capture_output=True, text=True)
    assert res.returncode == 0, res.stdout[-2000:] + res.stderr[-2000:]
    return str(d / "out" / "index.html")


def test_reach_step_reaches_step_three(built):
    import playtest
    with playtest.open_game(built) as (page, errors):
        res = playtest.reach_step(page, game(), ladder(), 3)
        assert [r["reached"] for r in res] == [True, True, True], res
        assert playtest.traits(page)["jo_stage"] == 3
        assert res[2]["path"] == [1]          # "Stay", not "Go back"
        assert not errors, errors


def test_reach_step_never_jumps_the_counter(built):
    import playtest
    lad = ladder()
    lad["steps"][1]["where"] = "yard"         # step 2 cannot be offered there
    with playtest.open_game(built) as (page, errors):
        res = playtest.reach_step(page, game(), lad, 3)
        assert [r["reached"] for r in res] == [True, False], res
        assert "does not offer jo_2" in res[1]["why"]
        assert playtest.traits(page)["jo_stage"] == 1


def test_ship_row_green_on_the_built_fixture(tmp_path, built):
    ok, head, detail = ship_row(tmp_path, state(), built=built)
    assert ok is True, (head, detail)
