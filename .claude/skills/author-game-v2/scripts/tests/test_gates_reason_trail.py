"""gates.py: the reason trail and the rejection review (the-release.md "When LO rejects something").

  a skill rejection names a notebook entry — a scored WARN gate: each `release_page.rejections[]`
      has a known layer, and one whose layer is the skill (`skill_wrong`, `skill_silent`) names its
      notebook entry (`N<n>`) in `skill_fix`. n/a: no rejection recorded.
  choices marked guess — a --ship REPORT row: sheet table rows whose source cell starts "guess".

Fixtures are written here (ws6's green game); nothing in games/ is read or written.
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

GATE = "a skill rejection names a notebook entry"


def rejection(layer, skill_fix="", what="games/fx/toml_phases/3_canvases.toml:120"):
    return {"what": what, "source": "guess", "layer": layer, "game_fix": "moved the party",
            "skill_fix": skill_fix}


def state_with(*rejections):
    st = ws6.green_state()
    st.setdefault("release_page", {})["rejections"] = list(rejections)
    return st


def test_no_rejection_is_na():
    assert gates._skill_rejections_logged(ws6.green_state())[0] is None


def test_a_skill_gap_with_a_notebook_entry_passes():
    ok, head, _d = gates._skill_rejections_logged(state_with(
        rejection("skill_silent", "N22: the skill has no party rule"), rejection("lo_changed")))
    assert ok is True and "2 rejection(s), 1 in the skill" in head


def test_a_skill_gap_with_no_notebook_entry_fails():
    ok, _h, detail = gates._skill_rejections_logged(state_with(rejection("skill_wrong", "fix the card")))
    assert ok is False and "no notebook entry" in detail[0]


def test_an_unknown_layer_fails():
    ok, _h, detail = gates._skill_rejections_logged(state_with(rejection("the model")))
    assert ok is False and "layer 'the model'" in detail[0]


def test_it_is_scored_and_never_a_ship_block():
    assert GATE not in gates.SHIP_BLOCK_GATES and GATE not in gates.SHIP_REPORT_GATES


def _sheets(tmp_path, files):
    for rel, text in files.items():
        p = tmp_path / "games" / "fx" / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text)


def test_guess_rows_are_reported_by_file_and_choice(tmp_path):
    _sheets(tmp_path, {
        "sheets/people/npc_a.md": "| key choice | source |\n|---|---|\n"
                                  "| where he sleeps | guess |\n| his ladder | the-arc.md A3 |\n",
        "DECISIONS.md": "| key choice | source |\n|---|---|\n| the rent | Guess — nothing said |\n",
        "sheets/places/bar.md": "| <placeholder> | guess |\n"})
    name, ok, head, rows = gates._guess_row(str(tmp_path), "fx")
    assert name == "choices marked guess" and ok is None and head.startswith("2 key choice(s)")
    assert rows == ["DECISIONS.md: the rent", "sheets/people/npc_a.md: where he sleeps"]


def test_no_guess_says_so(tmp_path):
    _sheets(tmp_path, {"sheets/OPENING.md": "| key choice | source |\n| the goal | LO, 2026-10-02 |\n"})
    head = gates._guess_row(str(tmp_path), "fx")[2]
    assert 'no sheet marks a choice "guess" (1 sheet file(s) read)' == head


def test_ship_prints_the_guess_row_as_a_report(tmp_path, monkeypatch):
    game = ws6.green_game()
    d = tmp_path / "games" / "fx"
    (d / "toml_phases").mkdir(parents=True)
    (d / "toml_phases" / "7_final_game.toml").write_text("# fixture\n")
    (d / "v2_state.json").write_text(json.dumps(ws6.green_state()))
    monkeypatch.setattr(gates, "_load", lambda p: copy.deepcopy(game))
    monkeypatch.setattr(gates, "release_mode", lambda s: 0)
    monkeypatch.setattr(gates, "saves_mode", lambda s: 2)
    monkeypatch.setattr(gates, "_ship_ladders", lambda *a, **k: (True, "ok", []))
    block, report = gates.ship_rows("fx", root=str(tmp_path))
    assert "choices marked guess" in {r[0] for r in report}
    assert "choices marked guess" not in {r[0] for r in block}
