"""gates.py: the coverage list at `--ship` (SKILL.md "Never build an unknown on a guess";
`templates/sheets/coverage.md`).

  no unknown topic — a scored gate, a WARN by type (LO: warn, never block): red on any `unknown`
      topic, named; red on no `board.coverage` (an absence is not a pass), and a game still
      grandfathered past COVERAGE_SINCE is told it predates the list; n/a with no ledger at all.
      `--ship` lists it under `every other gate` with the unknown topics by name, never as a BLOCK.
  topics on thin ground — a --ship REPORT row: the placeholder and scouted topics, by name.

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

GATE = "no unknown topic"


def entry(topic, status, kind="scene", source="LO, 2026-10-02"):
    return {"topic": topic, "kind": kind, "status": status, "source": source}


def state_with(coverage=None, slug="new_game", releases=None):
    st = ws6.green_state()
    st["slug"] = slug
    if coverage is not None:
        st["board"]["coverage"] = coverage
    if releases is not None:
        st["releases"] = releases
    return st


def ship(tmp_path, monkeypatch, state):
    game = ws6.green_game()
    d = tmp_path / "games" / state["slug"]
    (d / "toml_phases").mkdir(parents=True, exist_ok=True)
    (d / "toml_phases" / "7_final_game.toml").write_text("# fixture\n")
    (d / "v2_state.json").write_text(json.dumps(state))
    monkeypatch.setattr(gates, "_load", lambda p: copy.deepcopy(game))
    monkeypatch.setattr(gates, "release_mode", lambda s: 0)
    monkeypatch.setattr(gates, "saves_mode", lambda s: 2)
    monkeypatch.setattr(gates, "_ship_ladders", lambda *a, **k: (True, "ok", []))
    return gates.ship_rows(state["slug"], root=str(tmp_path))


# ── the gate ─────────────────────────────────────────────────────────────────

def test_a_list_with_no_unknown_passes():
    ok, head, _d = gates._no_unknown_topic(state_with([entry("a party", "lo"), entry("rent", "covered")]))
    assert ok is True and "none unknown" in head


def test_an_unknown_is_red_and_named():
    ok, head, detail = gates._no_unknown_topic(state_with([entry("a party", "unknown"), entry("a car", "unknown")]))
    assert ok is False and "a party, a car" in head and len(detail) == 2


def test_no_list_is_red_never_na():
    ok, head, _d = gates._no_unknown_topic(state_with())
    assert ok is False and "list every topic first" in head


def test_no_list_on_a_grandfathered_game_says_it_predates_the_list():
    ok, head, _d = gates._no_unknown_topic(state_with(slug="members_only"))
    assert ok is False and "predates the list" in head
    shipped = state_with(slug="members_only", releases=[{"version": "0.3", "shipped": gates.COVERAGE_SINCE}])
    assert "predates" not in gates._no_unknown_topic(shipped)[1]


def test_no_ledger_is_na():
    assert gates._no_unknown_topic(None)[0] is None


def test_it_is_scored_and_never_a_ship_block():
    assert GATE not in gates.SHIP_BLOCK_GATES and GATE not in gates.SHIP_REPORT_GATES
    assert GATE not in {label for _since, label in gates.SHIP_SINCE.values()}


# ── --ship ───────────────────────────────────────────────────────────────────

def test_ship_names_the_unknowns_under_every_other_gate(tmp_path, monkeypatch):
    block, report = ship(tmp_path, monkeypatch, state_with([entry("a party", "unknown")]))
    other = next(r for r in report if r[0] == "every other gate")
    assert f"FAIL {GATE}: 1 unknown: a party" in other[3]
    assert GATE not in {r[0] for r in block}


def test_ship_does_not_block_on_an_unknown(tmp_path, monkeypatch):
    known = {r[0]: r[1] for r in ship(tmp_path, monkeypatch, state_with([entry("a party", "lo")]))[0]}
    unknown = {r[0]: r[1] for r in ship(tmp_path, monkeypatch, state_with([entry("a party", "unknown")]))[0]}
    assert known == unknown


def test_ship_reports_thin_ground_by_name(tmp_path, monkeypatch):
    cov = [entry("a party", "scouted", source="games/new_game/scout/a_party.md"),
           entry("the landlord", "placeholder", "mechanic", "release page"), entry("rent", "covered")]
    _block, report = ship(tmp_path, monkeypatch, state_with(cov))
    row = next(r for r in report if r[0] == "topics on thin ground")
    assert row[1] is None and "1 placeholder · 1 scouted of 3 topic(s)" in row[2]
    assert row[3] == ["placeholder: the landlord", "scouted: a party"]


def test_ship_reports_no_list(tmp_path, monkeypatch):
    _block, report = ship(tmp_path, monkeypatch, state_with())
    assert next(r for r in report if r[0] == "topics on thin ground")[2].startswith("no board.coverage")
