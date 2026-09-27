"""Fixtures for the honest scoreboard (PRD IC21, LO 2026-09-27): too few to judge, parked
content measured (the parked/ folder read automatically, the ledger adding more), the
tally's denominator, and --ship's parked BLOCK row. Nothing in games/ is read or written.
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

try:
    import tomllib as _toml
except ImportError:                                     # py3.10
    import tomli as _toml

EXPLICIT = "His cock is in her mouth and she sucks his cock hard, cum on her tits and her cunt wet."


def game(n_explicit_repeatable=1, with_npc=True):
    canvases = [{"id": f"loop_{i}", "trigger": {"location": "room_a", "is_repeatable": True},
                 "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": EXPLICIT}]}]}
                for i in range(n_explicit_repeatable)]
    g = {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {"money": 10}},
         "locations": [{"id": "room_a"}], "canvases": canvases}
    if with_npc:
        g["npcs"] = [{"id": "npc_a", "name": "A", "schedules": [
            {"location": "room_a", "weekdays": [0, 1, 2, 3, 4, 5, 6],
             "start_time": "18:00", "end_time": "20:00"}]}]
    return g


def result(g, name, state=None, game_dir=None):
    model, g2 = gates.build(copy.deepcopy(g))
    results, info = gates.score(model, g2, state, game_dir)
    return next(r for r in results if r["gate"] == name), results, info


# ── too few to judge ─────────────────────────────────────────────────────────
def test_one_explicit_repeatable_beat_is_too_few_not_pass():
    r, _, _ = result(game(1), "explicit in repeatable")
    assert r["few"] and not r["pass_"] and not r["na"]
    assert r["headline"].startswith("too few to judge (1 of 5)")


def test_five_cases_pass_normally():
    r, _, _ = result(game(5), "explicit in repeatable")
    assert r["pass_"] and not r["few"]


def test_a_fail_on_few_cases_stays_a_fail():
    r, _, _ = result(game(1), "an explicit beat carries a clip")   # 0/1 clipped
    assert not r["pass_"] and not r["few"] and not r["na"]


def test_every_share_prints_its_denominator():
    r, _, _ = result(game(1), "explicit in repeatable")
    assert r["n"] == 1 and "of 1" in r["headline"]


# ── the tally ────────────────────────────────────────────────────────────────
def test_parked_and_few_count_in_the_denominator():
    rows = ([dict(pass_=True, na=False)] * 29 + [dict(pass_=False, na=False)] * 15
            + [dict(pass_=False, na=False, parked=True)] * 3
            + [dict(pass_=False, na=False, few=True)] * 2 + [dict(pass_=False, na=True)] * 4)
    assert gates.tally_counts(rows) == (29, 15, 3, 2, 4, 49)


# ── parked, measured ─────────────────────────────────────────────────────────
PARKED_NPC = """
[[npcs]]
id = "npc_a"
name = "A"
[[npcs.schedules]]
location = "room_a"
weekdays = [0, 1, 2, 3, 4, 5, 6]
start_time = "18:00"
end_time = "20:00"
"""


def test_parked_folder_is_read_without_any_declaration(tmp_path):
    (tmp_path / "parked").mkdir()
    (tmp_path / "parked" / "people.toml").write_text(PARKED_NPC)
    live, _, _ = result(game(1, with_npc=False), "standing surface")
    assert live["na"]                                               # nobody live
    r, results, info = result(game(1, with_npc=False), "standing surface", None, str(tmp_path))
    assert r["parked"] and not r["pass_"] and not r["na"]
    assert r["headline"].startswith("parked, not judged")
    assert "parked/people.toml" in r["detail"][0]
    p, f, k, w, n, d = gates.tally_counts(results)
    assert k >= 1 and d == len(results) - n                         # counted, not dropped


def test_ledger_adds_paths_outside_the_folder(tmp_path):
    (tmp_path / "later").mkdir()
    (tmp_path / "later" / "people.toml").write_text(PARKED_NPC)
    state = {"parked": {"files": ["later/*.toml"]}}
    r, _, info = result(game(1, with_npc=False), "standing surface", state, str(tmp_path))
    assert r["parked"] and any(f.endswith("later/people.toml") for f in info["files"])


def test_other_folders_are_not_read_and_a_broken_fragment_is_reported(tmp_path):
    (tmp_path / "elsewhere").mkdir()
    (tmp_path / "elsewhere" / "people.toml").write_text(PARKED_NPC)
    (tmp_path / "parked").mkdir()
    (tmp_path / "parked" / "broken.toml").write_text("[[canvases]\nid = ")
    r, _, info = result(game(1, with_npc=False), "standing surface", None, str(tmp_path))
    assert r["na"] and not r.get("parked")                          # undeclared folder ignored
    assert info["errors"] and info["errors"][0][0].endswith("broken.toml")


def test_parking_never_raises_the_score(tmp_path):
    (tmp_path / "parked").mkdir()
    (tmp_path / "parked" / "people.toml").write_text(PARKED_NPC)
    _, before, _ = result(game(1, with_npc=True), "standing surface")
    _, after, _ = result(game(1, with_npc=False), "standing surface", None, str(tmp_path))
    rb, ra = gates.tally_counts(before), gates.tally_counts(after)
    assert ra[0] / ra[5] <= rb[0] / rb[5]


# ── --ship ───────────────────────────────────────────────────────────────────
def test_ship_parked_block_row_is_red_and_says_why(tmp_path, monkeypatch):
    d = tmp_path / "games" / "fx"
    (d / "toml_phases").mkdir(parents=True)
    (d / "toml_phases" / "7_final_game.toml").write_text("# fixture\n")
    (d / "parked").mkdir()
    (d / "parked" / "people.toml").write_text(PARKED_NPC)
    (d / "v2_state.json").write_text(json.dumps({}))
    live = game(1, with_npc=False)
    real_load = gates._load
    monkeypatch.setattr(gates, "_load", lambda p: copy.deepcopy(live)
                        if str(p).endswith("7_final_game.toml") else real_load(p))
    monkeypatch.setattr(gates, "release_mode", lambda slug: 0)
    monkeypatch.setattr(gates, "saves_mode", lambda slug: 2)
    monkeypatch.setattr(gates, "_ship_ladders", lambda *a, **k: (True, "stub", []))
    block, _ = gates.ship_rows("fx", root=str(tmp_path))
    row = next(b for b in block if b[0] == "no empty rooms")
    assert row[1] is False and "parked, not judged" in row[2]


# ── share gates only (LO 2026-09-27) ─────────────────────────────────────────
def test_an_all_or_nothing_gate_passes_on_one_case():
    g = game(5)
    g["canvases"][0]["trigger"]["npc"] = "npc_a"                   # her row now has a surface
    r, _, _ = result(g, "standing surface")                         # 1/1 rows, every item right
    assert r["n"] == 1 and r["pass_"] and not r["few"]


def test_too_few_is_only_ever_a_share_gate():
    _, results, _ = result(game(1, with_npc=True), "explicit in repeatable")
    assert all(r["gate"] in gates.SHARE_GATES for r in results if r.get("few"))


def test_every_share_gate_is_a_real_gate():
    src = open(gates.__file__).read()
    for name in gates.SHARE_GATES:
        assert f'gate("{name}"' in src, name
