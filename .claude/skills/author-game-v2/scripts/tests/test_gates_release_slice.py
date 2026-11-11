"""Release slices (LO + advisor, 2026-11-11; first_term DECISIONS 230): ladders judged by the release being built,
a place declared locked, and the gate `every kept thing can happen`. Minimal game dicts; nothing in games/ is read."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402
import shape  # noqa: E402


def _cond(*items, logic="AND"):
    return {"version": "1.0", "logic": logic, "items": list(items)}


def _flag(k, on=True):
    return {"type": "flag", "subject": "player", "flag_key": k, "operator": "is_true" if on else "is_false"}


STATE = {"release_page": {"release": 1, "locked": ["gym"]},
         "board": {"characters": [{"id": "npc_ryan", "ladder": {"counter": "ryan_step", "steps": [
             {"n": 1, "canvas": "ryan_01"}, {"n": 2, "canvas": "ryan_02", "release": 2}]}}]}}


def test_ladders_read_only_this_release():
    (who, lad), = gates._declared_ladders(STATE)
    assert who == "npc_ryan" and [s["n"] for s in lad["steps"]] == [1]
    full = dict(STATE, release_page={})
    assert len(gates._declared_ladders(full)[0][1]["steps"]) == 2
    assert [s["n"] for s in shape._ladders(STATE)["npc_ryan"]["steps"]] == [1]


def test_locked_places():
    assert gates._locked_places(STATE) == {"gym"}
    assert gates._locked_places({}) == set()


def _game(*canvases, **extra):
    g = {"player": {"core_traits": {"corruption": 0}}, "npcs": [{"id": "npc_ryan"}], "canvases": list(canvases)}
    g.update(extra)
    return g


def test_a_flag_nothing_sets_is_red():
    g = _game({"id": "reader", "trigger": {"conditions": _cond(_flag("invite"))}, "nodes": []})
    ok, _h, rows = gates._every_kept_thing_can_happen(g, {})
    assert ok is False and "`invite`" in rows[0]


def test_set_flags_engine_flags_or_blocks_and_locks_pass():
    setter = {"id": "setter", "nodes": [{"id": "n", "exit_block": {"choices": [
        {"text": "x", "flagEffects": [{"flag": "invite", "op": "set"}]},
        {"text": "(Next release)", "show_when_locked": True,
         "conditions": _cond({"type": "trait", "subject": "player", "trait_key": "release_2_written",
                              "operator": "gte", "value": 1})}]}}]}
    g = _game(setter,
              {"id": "a", "trigger": {"conditions": _cond(_flag("invite"))}, "nodes": []},
              {"id": "b", "trigger": {"conditions": _cond(_flag("cheat_money"), _flag("setter_closed"))}, "nodes": []},
              {"id": "c", "trigger": {"conditions": _cond(_flag("never"), _flag("invite"), logic="OR")}, "nodes": []},
              {"id": "d", "trigger": {"conditions": _cond(_flag("never", on=False))}, "nodes": []},
              locations=[{"id": "gym", "entry_conditions": _cond(_flag("gym_open"))}])
    ok, head, rows = gates._every_kept_thing_can_happen(g, STATE)
    assert ok is True, rows


def test_a_trait_read_past_what_the_build_pays_is_red():
    g = _game({"id": "pay", "nodes": [{"id": "n", "exit_block": {"choices": [
                  {"text": "x", "effects": [{"targetType": "player", "trait": "corruption", "op": "add", "value": 1,
                                             "cap": 19}]}]}}]},
              {"id": "bold", "trigger": {"conditions": _cond({"type": "trait", "subject": "player",
                                                              "trait_key": "corruption", "operator": "gte",
                                                              "value": 40})}, "nodes": []},
              {"id": "roll", "nodes": [{"id": "n", "exit_block": {"choices": [{"text": "x", "effects": [
                  {"targetType": "player", "trait": "dice", "op": "set", "value": {"type": "random", "min": 1,
                                                                                   "max": 4}}]}]}}]},
              {"id": "dice", "trigger": {"conditions": _cond({"type": "trait", "subject": "player",
                                                              "trait_key": "dice", "operator": "eq", "value": 4})},
               "nodes": []})
    ok, _h, rows = gates._every_kept_thing_can_happen(g, {})
    assert ok is False and len(rows) == 1 and "corruption gte 40" in rows[0]


def test_a_closed_flag_of_a_cut_canvas_is_red():
    g = _game({"id": "b", "trigger": {"conditions": _cond(_flag("gone_step_closed"))}, "nodes": []})
    ok, _h, rows = gates._every_kept_thing_can_happen(g, {})
    assert ok is False and "gone_step_closed" in rows[0]


def test_dependencies_from_a_later_step_are_left_out():
    dep = {"from": {"npc": "npc_ryan", "step": 2}, "needs": {"npc": "npc_ryan", "step": 1}}
    assert shape._dep_in_release(dep, STATE) is False
    assert shape._dep_in_release(dict(dep, **{"from": {"npc": "npc_ryan", "step": 1}}), STATE) is True


def test_a_missing_person_is_red():
    g = _game({"id": "zoe", "trigger": {"requires_npc": "npc_zoe"}, "nodes": []})
    ok, _h, rows = gates._every_kept_thing_can_happen(g, {})
    assert ok is False and "npc_zoe" in rows[0]


def test_the_ledger_is_read_as_the_slice():
    """DECISIONS 231: cast, homes, loops, key clothes and the week's income are read for the release being built."""
    state = {"release_page": {"release": 1, "week_income": 300},
             "board": {"characters": [
                 {"id": "npc_ryan", "ladder": {"loop": ["ryan_loop"], "steps": [
                     {"n": 1, "canvas": "ryan_01"}, {"n": 2, "canvas": "ryan_02", "release": 2}]}},
                 {"id": "npc_zoe"}],
                 "map": {"homes": {"npc_ryan": "ryan_room", "npc_zoe": "zoe_bedroom"}},
                 "wardrobe": {"key_items": ["plain", "locked", "gone"]},
                 "economy": {"week_income": 848}}}
    g = {"npcs": [{"id": "npc_ryan"}], "canvases": [],
         "clothing": [{"id": "plain"},
                      {"id": "locked", "conditions": _cond(_flag("nobody_sets_this"))}]}
    b = gates._slice_state(g, state)["board"]
    assert [c["id"] for c in b["characters"]] == ["npc_ryan"]
    lad = b["characters"][0]["ladder"]
    assert [s["n"] for s in lad["steps"]] == [1] and lad["loop"].startswith("none:")
    assert b["map"]["homes"] == {"npc_ryan": "ryan_room"}
    assert b["wardrobe"]["key_items"] == ["plain"]
    assert b["economy"]["week_income"] == 300
    assert state["board"]["economy"]["week_income"] == 848          # the ledger itself is not touched
    assert gates._slice_state(g, dict(state, release_page={})) is not None
    full = dict(state, release_page={})
    assert gates._slice_state(g, full) is full                       # no release: the full ledger as before
