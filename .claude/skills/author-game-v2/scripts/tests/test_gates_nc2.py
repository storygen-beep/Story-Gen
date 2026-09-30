"""NC2 (PRD v2 phase 4 · D7 · J3 · J4, 2026-09-30): her climb, `the-arc.md` A15.

A paid repeatable (an exit that adds money, an explicit beat naming an act) needs:
(a) an introduction the first time reads · (b) a first time that sets what it reads ·
(c) two live groups per act node reading a declared tier at different thresholds ·
(d) shut on a new save, with introduced → a step → first time · (e) a stop exit on each
act node that goes on to another act.

Fixtures are written here; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

HOT = "He fucks her against the wall, his cock deep in her cunt, her tits in his hands."
V1 = {"version": "1.0", "logic": "AND"}


def flag(key, op="is_true"):
    return {"type": "flag", "subject": "player", "flag_key": key, "operator": op}


def nerve(op, v):
    return {"type": "trait", "subject": "player", "trait_key": "nerve", "operator": op, "value": v}


def step(cid, reads, sets):
    t = {"location": "room", "is_repeatable": False}
    if reads:
        t["conditions"] = dict(V1, items=[flag(reads)])
    return {"id": cid, "trigger": t, "nodes": [{"id": "n", "blocks": [
        {"type": "paragraph", "content": "He asks."}], "exit_block": {"config": {
            "flagEffects": [{"flag": sets, "op": "set"}]}}}]}


def act_node(nid, voices=2, stop=True, on=None):
    groups = [{"type": "group", "conditions": dict(V1, items=[nerve("gte", 50)]),
               "blocks": [{"type": "paragraph", "content": HOT}]}]
    if voices == 2:
        groups.append({"type": "group", "conditions": dict(V1, items=[nerve("lt", 50)]),
                       "blocks": [{"type": "paragraph", "content": HOT}]})
    choices = []
    if on:
        choices.append({"text": "Keep going", "targetType": "node", "nodeId": f"sell.{on}"})
    if stop or not on:
        choices.append({"text": "Stop him", "targetType": "location", "locationId": "room",
                        "effects": [{"trait": "money", "op": "add", "value": 10}]})
    return {"id": nid, "blocks": groups, "exit_block": {"type": "choices", "choices": choices}}


def game(intro=True, middle=True, gated=True, voices=2, stop=True):
    chain = []
    if intro:
        chain.append(step("intro", None, "heard"))
    if middle:
        chain.append(step("ask", "heard" if intro else None, "asked"))
    chain.append(step("first", "asked" if middle else ("heard" if intro else None), "first_done"))
    t = {"location": "room", "is_repeatable": True}
    if gated:
        t["conditions"] = dict(V1, items=[flag("first_done")])
    sell = {"id": "sell", "trigger": t,
            "nodes": [act_node("mouth", voices, stop, on="fuck"), act_node("fuck", voices)]}
    return {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {"money": 0}},
            "locations": [{"id": "room"}], "canvases": chain + [sell]}


STATE = {"board": {"ascent_tiers": ["nerve"], "economy": {"currency": "money"}}}


def climb(g, state=STATE):
    return gates._her_climb(copy.deepcopy(g), state)


def test_the_full_climb_passes():
    ok, head, detail, n = climb(game())
    assert ok is True and n == 1, (head, detail)


def test_no_paid_repeatable_is_na():
    g = game()
    g["canvases"][-1]["nodes"] = [{"id": "n", "blocks": [{"type": "paragraph", "content": "Dishes."}]}]
    assert climb(g)[0] is None


def test_no_introduction_fails_a():
    ok, _h, detail, _n = climb(game(intro=False, middle=False))   # the first time reads nothing
    assert ok is False and any("(a)" in d for d in detail), detail


def test_no_step_between_intro_and_first_time_fails_d():
    ok, _h, detail, _n = climb(game(middle=False))
    assert ok is False and any("(d) no step between" in d for d in detail), detail


def test_open_on_a_new_save_fails_b_and_d():
    ok, _h, detail, _n = climb(game(gated=False))
    assert any("(b)" in d for d in detail) and any("(d) open on a new save" in d for d in detail)


def test_one_voice_fails_c():
    ok, _h, detail, _n = climb(game(voices=1))
    assert ok is False and any(d.startswith("sell.mouth: (c) 1 live group") for d in detail)


def test_a_dead_second_voice_does_not_count():
    g = game()
    for n in g["canvases"][-1]["nodes"]:
        n["blocks"][1]["conditions"] = dict(V1, items=[nerve("gte", 60)])   # dead under gte 50
    ok, _h, detail, _n = climb(g)
    assert ok is False and any("(c) 1 live group" in d for d in detail)


def test_no_stop_exit_fails_e():
    ok, _h, detail, _n = climb(game(stop=False))
    assert ok is False and any(d.startswith("sell.mouth: (e) no stop exit") for d in detail)


def test_without_tiers_c_is_noted_not_judged():
    ok, _h, detail, _n = climb(game(voices=1), {"board": {"economy": {"currency": "money"}}})
    assert ok is True and any("(c) not judged" in d for d in detail)


def test_the_gate_runs_in_the_scoreboard():
    model, g2 = gates.build(copy.deepcopy(game()))
    r = next(r for r in gates.run_gates(model, g2, STATE) if r["gate"] == "her climb")
    assert r["headline"].startswith("too few to judge") or r["pass_"] is True
