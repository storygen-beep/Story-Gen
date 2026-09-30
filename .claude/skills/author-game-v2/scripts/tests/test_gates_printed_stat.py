"""The printed-stat lint (PRD v2 phase 4 · D1b, 2026-09-30) and its --ship BLOCK row.

Only a `+X` whose X is no declared trait or flag is listed (D1: a real stat may be shown; the
toast shows it too). The old rule — every printed stat — runs in LO B's legacy re-run only.

Fixtures are written here; nothing in games/ is read or written.
"""
import copy
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402
import test_gates_ws6 as ws6  # noqa: E402


def game(text):
    return {"player": {"core_traits": {"trust": 0}},
            "canvases": [{"id": "c", "nodes": [{"id": "n", "blocks": [
                {"type": "paragraph", "content": text}]}]}]}


def test_a_real_stat_is_not_listed():
    assert gates.lint_printed_stat(game("She smiles. (+5 Trust)"))[1] == []


def test_an_unreal_stat_is_listed():
    hits = gates.lint_printed_stat(game("She smiles. (+5 Respect)"))[1]
    assert hits == ['c: "+5 Respect" names no declared trait or flag']


def test_the_old_rule_lists_the_real_one_too():
    gates._LEGACY_RULES.add("printed_stat")
    try:
        hits = gates.lint_printed_stat(game("She smiles. (+5 Trust)"))[1]
    finally:
        gates._LEGACY_RULES.discard("printed_stat")
    assert hits == ['c: "+5 Trust" prints a stat (old rule)']


def ship(tmp_path, monkeypatch, slug, text):
    g = ws6.green_game()
    g["canvases"][2]["nodes"][0]["blocks"][0]["content"] = text
    d = tmp_path / "games" / slug
    (d / "toml_phases").mkdir(parents=True, exist_ok=True)
    (d / "toml_phases" / "7_final_game.toml").write_text("# fixture\n")
    (d / "v2_state.json").write_text(json.dumps(ws6.green_state()))
    monkeypatch.setattr(gates, "_load", lambda p: copy.deepcopy(g))
    monkeypatch.setattr(gates, "release_mode", lambda s: 0)
    monkeypatch.setattr(gates, "saves_mode", lambda s: 2)
    monkeypatch.setattr(gates, "_ship_ladders", lambda *a, **k: (True, "ok", []))
    block, _ = gates.ship_rows(slug, root=str(tmp_path))
    return {n: ok for n, ok, _h, _d in block}[gates.SHIP_STAT_ROW]


def test_a_real_stat_no_longer_blocks(tmp_path, monkeypatch):
    assert ship(tmp_path, monkeypatch, "brand_new", "She reads. (+2 Money)") is True


def test_an_unreal_stat_blocks_a_new_game(tmp_path, monkeypatch):
    assert ship(tmp_path, monkeypatch, "brand_new", "She reads. (+2 Respect)") is False


def test_an_unreal_stat_still_blocks_a_grandfathered_game(tmp_path, monkeypatch):
    # Red under the old rule too, so LO B leaves it a FAIL.
    assert ship(tmp_path, monkeypatch, "probation", "She reads. (+2 Respect)") is False
