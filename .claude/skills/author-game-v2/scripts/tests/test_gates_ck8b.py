"""CK8b (PRD v2, 2026-09-30): counting fixes, and the first LO B since-dates.

  I9  · `_week_income` skips `substitution_only` canvases.
  I14 · `_school_split` counts `<npc>_stage` ladder counters on NEITHER side (LO: option 3).
  H9  · the ladder's person-present check wants FULL cover (`_window_uncovered`).
  H10 · a declared tier nothing reads yet is n/a per tier, with a note.
  H14 · "NOTHING is gated on money" says it is a warning only.
  LO B · H9 and I9 tighten `--ship` BLOCK rows, so a grandfathered game WARNS
         ("… blocks from your next release") where only the new rule is red.

Fixtures are written here; nothing in games/ is read or written.
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gates  # noqa: E402
import test_gates_ws6 as ws6  # noqa: E402


def cond(*items):
    return {"version": "1.0", "logic": "AND", "items": list(items)}


# ── I9 ────────────────────────────────────────────────────────────────────────

def income_game(sub):
    shift = {"id": "shift", "trigger": {"location": "bar", "max_triggers_per_day": 1},
             "nodes": [{"id": "n", "exit_block": {"config": {"effects": [
                 {"trait": "money", "op": "add", "value": 50}]}}}]}
    walkin = {"id": "walkin", "trigger": {"location": "bar", "max_triggers_per_day": 1,
                                          **({"substitution_only": True} if sub else {})},
              "nodes": [{"id": "n", "exit_block": {"config": {"effects": [
                  {"trait": "money", "op": "add", "value": 150}]}}}]}
    return {"canvases": [shift, walkin]}


def test_substitution_pay_is_not_income_of_its_own():
    assert gates._week_income(income_game(sub=True), "money")[0] == 350      # 50 × 7
    assert gates._week_income(income_game(sub=False), "money")[0] == 1400    # + 150 × 7


def test_the_legacy_rule_still_counts_it():
    gates._LEGACY_RULES.add("sub_income")
    try:
        assert gates._week_income(income_game(sub=True), "money")[0] == 1400
    finally:
        gates._LEGACY_RULES.discard("sub_income")


# ── I14 ───────────────────────────────────────────────────────────────────────

def stage_game():
    return {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {}},
            "locations": [{"id": "room"}], "npcs": [{"id": "npc_jo", "name": "Jo"}],
            "canvases": [{"id": "c", "trigger": {"location": "room", "conditions": cond(
                {"type": "trait", "subject": "player", "trait_key": "jo_stage",
                 "operator": "eq", "value": 1},
                {"type": "trait", "subject": "player", "trait_key": "nerve",
                 "operator": "gte", "value": 10})},
                "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "Here."}]}]}]}


def test_a_ladder_counter_counts_on_neither_side():
    player, npc = gates._school_split(stage_game(), {"board": {"ascent_tiers": ["nerve", "jo_stage"]}})
    assert npc == {}
    assert player == {"nerve": 1}


def test_the_climb_fail_says_a_ladder_counter_is_not_his_score():
    model, g2 = gates.build(copy.deepcopy(stage_game()))
    st = {"board": {"ascent_tiers": ["nerve"], "who_climbs": "cast"}}
    r = next(r for r in gates.run_gates(model, g2, st)
             if r["gate"] == "the climb is where you said it is")
    assert r["pass_"] is False
    assert any("a ladder counter is not his score; give him a meter of his own (D5)" in d
               for d in r["detail"]), r["detail"]


# ── H9 ────────────────────────────────────────────────────────────────────────

def ladder_game(rows):
    return {
        "player": {"core_traits": {"jo_stage": 0}},
        "npcs": [{"id": "npc_jo", "schedules": [
            {"location": "bar", "weekdays": [0], "start_time": a, "end_time": b} for a, b in rows]}],
        "canvases": [{"id": "jo_1", "trigger": {
            "location": "bar", "npc": "npc_jo", "is_repeatable": False,
            "schedules": [{"weekdays": [0], "start_time": "18:00", "end_time": "22:00"}],
            "conditions": cond({"type": "trait", "subject": "player", "trait_key": "jo_stage",
                                "operator": "eq", "value": 0})},
            "nodes": [{"id": "n", "exit_block": {"config": {"effects": [
                {"trait": "jo_stage", "op": "set", "value": 1}]}}}]}],
    }


LADDER = {"board": {"characters": [{"id": "npc_jo", "ladder": {"counter": "jo_stage", "steps": [
    {"n": 1, "canvas": "jo_1", "where": "bar",
     "when": {"days": ["Mon"], "from": "18:00", "to": "22:00"}, "gate": []}]}}]}}


def cover_problems(rows):
    return [p for p in gates.ladder_problems(ladder_game(rows), LADDER)[2] if "npc_jo" in p]


def test_a_partial_overlap_is_not_there():
    got = cover_problems([("20:00", "23:00")])
    assert got == ["npc_jo step 1 (jo_1): bound to npc_jo, whose schedule does not fully cover "
                   "bar 18:00-22:00 on Mon"], got


def test_full_cover_passes_and_rows_add_up():
    assert cover_problems([("17:00", "23:00")]) == []
    assert cover_problems([("18:00", "20:00"), ("20:00", "22:00")]) == []


def test_the_legacy_rule_passed_any_overlap():
    gates._LEGACY_RULES.add("full_cover")
    try:
        assert cover_problems([("20:00", "23:00")]) == []
    finally:
        gates._LEGACY_RULES.discard("full_cover")


# ── H10 ───────────────────────────────────────────────────────────────────────

def tier_row(state):
    g = {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {}},
         "locations": [{"id": "room"}],
         "canvases": [{"id": "c", "trigger": {"location": "room", "conditions": cond(
             {"type": "trait", "subject": "player", "trait_key": "nerve",
              "operator": "gte", "value": 10})},
             "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "Here."}]}]}]}
    model, g2 = gates.build(copy.deepcopy(g))
    return next(r for r in gates.run_gates(model, g2, state)
                if r["gate"] == "ascent tiers expand the world")


def test_an_unread_tier_is_na_for_that_tier():
    r = tier_row({"board": {"ascent_tiers": ["nerve", "heat"]}})
    assert r["pass_"] is True, r
    assert "`heat`: declared, no gate reads it this release — n/a for this tier" in r["detail"]


def test_only_unread_tiers_is_na():
    r = tier_row({"board": {"ascent_tiers": ["heat"]}})
    assert r["na"] is True, r


# ── H14 ───────────────────────────────────────────────────────────────────────

def test_the_money_lint_says_warning_only():
    s, _ = gates.lint_money_channel([], {"canvases": []},
                                    {"board": {"economy": {"currency": "money"}}})
    assert "warning only" in s


# ── LO B ──────────────────────────────────────────────────────────────────────

def ship(tmp_path, monkeypatch, slug, state=None, ladder=None, obligation=None):
    """ws6's harness, with the slug chosen and the two since-dated rows stubbed to read
    the legacy switch: red under the new rule, green under the old one."""
    game = ws6.green_game()
    state = state if state is not None else ws6.green_state()
    d = tmp_path / "games" / slug
    (d / "toml_phases").mkdir(parents=True, exist_ok=True)
    (d / "toml_phases" / "7_final_game.toml").write_text("# fixture\n")
    (d / "v2_state.json").write_text(json.dumps(state))
    monkeypatch.setattr(gates, "_load", lambda p: copy.deepcopy(game))
    monkeypatch.setattr(gates, "release_mode", lambda s: 0)
    monkeypatch.setattr(gates, "saves_mode", lambda s: 2)
    monkeypatch.setattr(gates, "_ship_ladders", ladder or (lambda *a, **k: (True, "ok", [])))
    if obligation:
        real = gates._block_gate_verdict

        def verdict(gname, r):
            if gname == "the obligation is charged":
                return obligation()
            return real(gname, r)
        monkeypatch.setattr(gates, "_block_gate_verdict", verdict)
    block, _ = gates.ship_rows(slug, root=str(tmp_path))
    return {n: (ok, h) for n, ok, h, _d in block}


def new_rule_red(rule):
    return lambda *a, **k: ((True, "old rule: green", []) if gates._legacy(rule)
                            else (False, "new rule: red", ["the detail"]))


def test_a_grandfathered_game_warns_on_the_ladder_rule(tmp_path, monkeypatch, capsys):
    b = ship(tmp_path, monkeypatch, "probation", ladder=new_rule_red("full_cover"))
    ok, head = b[gates.SHIP_LADDER_ROW]
    assert ok == "warn" and "blocks from your next release" in head and "full_cover" in head
    monkeypatch.setattr(gates, "ship_rows", lambda slug: (
        [(gates.SHIP_LADDER_ROW, "warn", head, [])], []))
    assert gates.ship_mode("probation") == 0
    assert "[WARN]" in capsys.readouterr().out


def test_a_release_shipped_since_the_rule_blocks(tmp_path, monkeypatch):
    st = ws6.green_state()
    st["releases"] = [{"version": "0.1", "shipped": "2026-10-02"}]
    b = ship(tmp_path, monkeypatch, "probation", state=st, ladder=new_rule_red("full_cover"))
    assert b[gates.SHIP_LADDER_ROW][0] is False


def test_an_older_release_still_warns(tmp_path, monkeypatch):
    st = ws6.green_state()
    st["releases"] = [{"version": "0.1", "shipped": "2026-09-01"}]
    b = ship(tmp_path, monkeypatch, "probation", state=st, ladder=new_rule_red("full_cover"))
    assert b[gates.SHIP_LADDER_ROW][0] == "warn"


def test_a_game_not_grandfathered_blocks(tmp_path, monkeypatch):
    b = ship(tmp_path, monkeypatch, "brand_new", ladder=new_rule_red("full_cover"))
    assert b[gates.SHIP_LADDER_ROW][0] is False


def test_red_under_the_old_rule_too_stays_a_fail(tmp_path, monkeypatch):
    b = ship(tmp_path, monkeypatch, "probation",
             ladder=lambda *a, **k: (False, "red either way", []))
    assert b[gates.SHIP_LADDER_ROW][0] is False


def test_the_income_rule_warns_when_grandfathered_and_blocks_when_not(tmp_path, monkeypatch):
    label = gates.SHIP_BLOCK_GATES["the obligation is charged"]
    ob = lambda: ((True, "old count: payable", []) if gates._legacy("sub_income")
                  else (False, "new count: unpayable", ["x"]))
    assert ship(tmp_path, monkeypatch, "vesper_two", obligation=ob)[label][0] == "warn"
    assert ship(tmp_path, monkeypatch, "new_game", obligation=ob)[label][0] is False


def test_the_legacy_switch_is_reset_after_ship():
    assert gates._LEGACY_RULES == set()
