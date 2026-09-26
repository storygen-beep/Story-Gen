"""Fixtures for the four gates rewritten on 2026-09-26 (PRD WS5) and the fixes that
came with them. Each fixture is a minimal game dict built here — nothing in games/ is
read or written. Run from the repo root:

    venv/bin/python -m pytest .claude/skills/author-game-v2/scripts/tests -q
"""
import copy
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def verdict(game, state, name):
    model, g = gates.build(copy.deepcopy(game))
    for r in gates.run_gates(model, g, state):
        if r["gate"] == name:
            return "n/a" if r["na"] else ("PASS" if r["pass_"] else "FAIL"), r
    raise AssertionError(f"gate {name!r} not emitted")


def cond(*items):
    return {"version": "1.0", "logic": "AND", "items": list(items)}


def base_game():
    return {
        "project": {"id": "fx", "name": "fx", "starting_canvas": "opening",
                    "quests_engine": "v2"},
        "player": {"core_traits": {"money": 10}},
        "locations": [{"id": "room_a"}, {"id": "room_b"}, {"id": "work"}],
        "npcs": [{"id": "npc_a", "name": "A",
                  "schedules": [{"location": "room_a", "weekdays": [0, 1, 2, 3, 4, 5, 6],
                                 "start_time": "18:00", "end_time": "20:00"}]}],
        "canvases": [
            {"id": "opening", "trigger": {"location": "room_a", "is_repeatable": False},
             "nodes": [{"id": "n", "blocks": [], "exit_block": {"config": {
                 "flagEffects": [{"flag": "opening_done", "op": "set"}]}}}]},
        ],
        "quest_cards": [{"id": "card", "text": "Do the thing.",
                         "when": [{"flag": "opening_done", "op": "is_true"}]}],
    }


def hub(cid, loc, npc="npc_a", sched=None):
    t = {"location": loc, "npc": npc, "is_repeatable": True}
    if sched:
        t["schedules"] = sched
    return {"id": cid, "trigger": t, "nodes": [{"id": "n", "blocks": []}]}


# ── standing surface ─────────────────────────────────────────────────────────
def test_standing_surface_fails_when_her_scene_is_in_another_room():
    g = base_game()
    g["canvases"].append(hub("a_hub", "room_b"))
    v, r = verdict(g, None, "standing surface")
    assert v == "FAIL"
    assert any("DEAD npc_a @room_a" in d for d in r["detail"])
    assert any("STRANDED a_hub" in d for d in r["detail"])


def test_standing_surface_passes_when_her_scene_is_in_her_room():
    g = base_game()
    g["canvases"].append(hub("a_hub", "room_a"))
    assert verdict(g, None, "standing surface")[0] == "PASS"


def test_standing_surface_is_day_precise():
    g = base_game()
    g["canvases"].append(hub("a_hub", "room_a", sched=[{"weekdays": [4], "start_time": "18:00",
                                                       "end_time": "20:00"}]))
    v, r = verdict(g, None, "standing surface")
    assert v == "FAIL" and any("Mon Tue Wed Thu Sat Sun" in d for d in r["detail"])


def test_standing_surface_declared_occupancy_row_is_backed():
    g = base_game()
    state = {"board": {"characters": [{"id": "npc_a", "occupancy_rows": [
        {"location": "room_a", "start_time": "18:00", "reason": "asleep"}]}]}}
    assert verdict(g, state, "standing surface")[0] == "PASS"


def test_standing_surface_overnight_row():
    g = base_game()
    g["npcs"][0]["schedules"] = [{"location": "room_a", "weekdays": [0, 1, 2, 3, 4, 5, 6],
                                  "start_time": "23:00", "end_time": "08:00"}]
    g["canvases"].append(hub("a_hub", "room_a", sched=[{"weekdays": [0, 1, 2, 3, 4, 5, 6],
                                                       "start_time": "06:00",
                                                       "end_time": "07:00"}]))
    assert verdict(g, None, "standing surface")[0] == "PASS"


def test_standing_surface_day_capped_portrait():
    g = base_game()
    c = hub("a_hub", "room_a")
    c["trigger"]["max_triggers_per_day"] = 1
    g["canvases"].append(c)
    v, r = verdict(g, None, "standing surface")
    assert v == "FAIL" and any("DAY-CAPPED a_hub" in d for d in r["detail"])


# ── the obligation is charged ────────────────────────────────────────────────
def econ_state(**extra):
    e = {"currency": "money", "obligation": "rent on Friday", "obligation_amount": 150}
    e.update(extra)
    return {"board": {"economy": e}}


def pay(cid, amount, capped=True, rep=True):
    t = {"location": "work", "is_repeatable": rep}
    if capped:
        t["max_triggers_per_day"] = 1
    return {"id": cid, "trigger": t, "nodes": [{"id": "n", "blocks": [], "exit_block": {
        "config": {"effects": [{"trait": "money", "op": "add", "value": amount}]}}}]}


def charge(cid, amount, dev=False, rep=True):
    t = {"location": "room_a", "is_repeatable": rep, "max_triggers_per_day": 1}
    if dev:
        t["conditions"] = cond({"type": "flag", "flag_key": "dev_mode_enabled",
                                "operator": "is_true"})
    return {"id": cid, "trigger": t, "nodes": [{"id": "n", "blocks": [], "exit_block": {
        "config": {"effects": [{"trait": "money", "op": "add", "value": -amount}]}}}]}


def test_obligation_fails_when_the_week_cannot_pay():
    g = base_game()
    g["canvases"] += [pay("shift", 3), charge("friday", 150)]
    v, r = verdict(g, econ_state(), "the obligation is charged")
    assert v == "FAIL" and any("cannot pay" in d for d in r["detail"])


def test_obligation_passes_when_the_week_can_pay():
    g = base_game()
    g["canvases"] += [pay("shift", 40), charge("friday", 150)]
    assert verdict(g, econ_state(), "the obligation is charged")[0] == "PASS"


def test_obligation_signposted_move_is_not_a_failure_to_pay():
    g = base_game()
    g["canvases"] += [pay("shift", 3), charge("friday", 150)]
    st = econ_state(obligation_moves="week one she has no job yet")
    assert verdict(g, st, "the obligation is charged")[0] == "PASS"


def test_obligation_dev_only_charge_does_not_count():
    g = base_game()
    g["canvases"] += [pay("shift", 40), charge("friday", 150, dev=True)]
    v, r = verdict(g, econ_state(), "the obligation is charged")
    assert v == "FAIL" and any("nothing takes 150" in d for d in r["detail"])


def test_obligation_stale_declared_week():
    g = base_game()
    g["canvases"] += [pay("shift", 40), charge("friday", 150)]
    v, r = verdict(g, econ_state(week_income=900), "the obligation is charged")
    assert v == "FAIL" and any("stale" in d for d in r["detail"])


def test_obligation_alternatives_on_one_capped_canvas_are_not_summed():
    g = base_game()
    c = pay("bar", 0)
    c["nodes"] = [{"id": "n", "blocks": [], "exit_block": {"choices": [
        {"text": "small tip", "effects": [{"trait": "money", "op": "add", "value": 10}]},
        {"text": "big tip", "effects": [{"trait": "money", "op": "add", "value": 20}]}]}}]
    g["canvases"] += [c, charge("friday", 150)]
    v, r = verdict(g, econ_state(), "the obligation is charged")
    assert v == "FAIL"            # 20 × 7 = 140 < 150, not (10 + 20) × 7 = 210


# ── ends on an opening ───────────────────────────────────────────────────────
def door_game():
    g = base_game()
    g["canvases"].append({"id": "office", "trigger": {"location": "work", "is_repeatable": True},
                          "nodes": [{"id": "n", "blocks": [], "exit_block": {"choices": [
                              {"text": "Take the closing shift", "show_when_locked": True,
                               "conditions": cond({"type": "flag", "flag_key": "earned_it",
                                                   "operator": "is_true"})}]}}]})
    g["canvases"].append({"id": "earn", "trigger": {"location": "work", "is_repeatable": False},
                          "nodes": [{"id": "n", "blocks": [], "exit_block": {"config": {
                              "flagEffects": [{"flag": "earned_it", "op": "set"}]}}}]})
    return g


def test_door_undeclared_fails_when_a_ledger_exists():
    assert verdict(door_game(), {"board": {}}, "ends on an opening")[0] == "FAIL"


def test_door_is_na_without_a_ledger():
    assert verdict(door_game(), None, "ends on an opening")[0] == "n/a"


def test_door_declared_locked_and_openable_passes():
    st = {"board": {"door": {"canvas": "office", "choice": "Take the closing shift"}}}
    assert verdict(door_game(), st, "ends on an opening")[0] == "PASS"


def test_door_that_can_never_open_fails():
    g = door_game()
    g["canvases"] = [c for c in g["canvases"] if c["id"] != "earn"]
    st = {"board": {"door": {"canvas": "office", "choice": "Take the closing shift"}}}
    v, r = verdict(g, st, "ends on an opening")
    assert v == "FAIL" and any("never come true" in d for d in r["detail"])


def test_door_on_a_missing_choice_fails():
    st = {"board": {"door": {"canvas": "office", "choice": "No such choice"}}}
    assert verdict(door_game(), st, "ends on an opening")[0] == "FAIL"


# ── guidance exists ──────────────────────────────────────────────────────────
GUIDE_STATE = {"board": {"characters": [{"id": "npc_a"}]}}


def guide_game():
    g = base_game()
    g["quest_cards"].append({"id": "a_card", "npc_id": "npc_a", "text": "Find A in room A."})
    return g


def test_guidance_quests_engine_under_settings_fails():
    g = guide_game()
    del g["project"]["quests_engine"]
    g["settings"] = {"quests_engine": "v2"}
    v, r = verdict(g, GUIDE_STATE, "guidance exists")
    assert v == "FAIL" and "[settings]" in r["headline"]


def test_guidance_quests_engine_under_project_passes():
    assert verdict(guide_game(), GUIDE_STATE, "guidance exists")[0] == "PASS"


def test_guidance_card_that_can_never_show_fails():
    g = guide_game()
    g["quest_cards"][1]["when"] = [{"flag": "nobody_sets_this", "op": "is_true"}]
    v, r = verdict(g, GUIDE_STATE, "guidance exists")
    assert v == "FAIL" and any("never shows" in d for d in r["detail"])


def test_guidance_card_with_no_words_fails():
    g = guide_game()
    g["quest_cards"][1]["text"] = "   "
    v, r = verdict(g, GUIDE_STATE, "guidance exists")
    assert v == "FAIL" and any("renders no words" in d for d in r["detail"])


# ── one reading of is_repeatable ─────────────────────────────────────────────
def test_absent_is_repeatable_is_repeatable_everywhere():
    assert gates._rep_of({}) is True
    assert gates._rep_of({"is_repeatable": False}) is False
    g = base_game()
    # a canvas with NO is_repeatable key and a mute person on it: the engine treats it
    # as repeatable, so it is not a one-time step and must not be reported as a mute one.
    g["canvases"].append({"id": "chat", "trigger": {"location": "room_a", "npc": "npc_a"},
                          "nodes": [{"id": "n", "blocks": [
                              {"type": "paragraph", "content": "She says nothing at all."}]}]})
    _summary, mute = gates.lint_one_time_speaks(g)
    assert not any("chat" in m for m in mute)


# ── --json exit code ─────────────────────────────────────────────────────────
def test_json_mode_exits_with_the_verdict(tmp_path):
    d = tmp_path / "games" / "fx" / "toml_phases"
    d.mkdir(parents=True)
    g = base_game()
    g["canvases"].append(hub("a_hub", "room_b"))       # standing surface fails
    lines = ['[project]', 'id = "fx"', 'name = "fx"', 'starting_canvas = "opening"']
    (d / "7_final_game.toml").write_text("\n".join(lines) + "\n" + _toml_rest(g))
    script = os.path.join(os.path.dirname(HERE), "gates.py")
    rc = subprocess.run([sys.executable, script, str(d / "7_final_game.toml"), "--json"],
                        capture_output=True, text=True).returncode
    assert rc == 1


def _toml_rest(g):
    """Just enough TOML for the --json exit test: one NPC, two canvases."""
    return """
[[locations]]
id = "room_a"
[[locations]]
id = "room_b"

[[npcs]]
id = "npc_a"
name = "A"
[[npcs.schedules]]
location = "room_a"
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "18:00"
end_time = "20:00"

[[canvases]]
id = "opening"
[canvases.trigger]
location = "room_a"
is_repeatable = false
[[canvases.nodes]]
id = "n"
blocks = []

[[canvases]]
id = "a_hub"
[canvases.trigger]
location = "room_b"
npc = "npc_a"
is_repeatable = true
[[canvases.nodes]]
id = "n"
blocks = []
"""
