"""PRD v2 DC1 · E2 · E4 · H30: the pitch pack runs before a build (the idea phase reads the ledger,
WANT.md and IDEA.md), and only SHIPPED releases count as shipped. Everything is written to a temp dir;
nothing in games/ is read or written."""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import pitch_pack  # noqa: E402

STATE = {
    "phase": "want",
    "want": {"fantasy_shape": "rise_by_want",
             "places": [{"id": "bar", "name": "The Bar"}],
             "cast": [{"id": "npc_a", "age": 30, "keeps": "want + warmth"}],
             "why_this_person": {"npc_a": "he never looks away"}},
    "releases": [{"version": "0.1", "subject": "planned, not shipped", "moment_kind": "firsts"},
                 {"version": "0.0", "subject": "the one that shipped", "moment_kind": "being_seen",
                  "shipped": "2026-09-01"}],
}


def _game(tmp_path, monkeypatch, with_pages=True):
    d = tmp_path / "games" / "fx"
    d.mkdir(parents=True)
    (d / "v2_state.json").write_text(json.dumps(STATE))
    if with_pages:
        (d / "WANT.md").write_text("# The Want — fx\nShe wants the bar.\n")
        (d / "IDEA.md").write_text("# The idea — fx\nThe first step with one person.\n")
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["pitch_pack.py", "fx"])


def test_only_shipped_releases_count():
    counts, unrec, _ = pitch_pack._kinds_shipped(STATE["releases"])
    assert counts["being_seen"] == 1 and counts["firsts"] == 0 and unrec == 0
    assert [r["version"] for r in pitch_pack._shipped(STATE["releases"])] == ["0.0"]


def test_idea_phase_runs_without_a_build(tmp_path, monkeypatch, capsys):
    _game(tmp_path, monkeypatch)
    assert pitch_pack.main() == 0
    out = capsys.readouterr().out
    assert "idea phase: no build yet" in out
    assert "She wants the bar." in out and "The first step with one person." in out
    assert "bar" in out and "The Bar" in out
    assert "npc_a" in out and "age 30" in out and "he never looks away" in out
    assert "SHIPPED ALREADY — 1 release(s)" in out
    assert "the one that shipped" in out and "planned, not shipped" not in out


def test_idea_phase_json(tmp_path, monkeypatch, capsys):
    _game(tmp_path, monkeypatch)
    monkeypatch.setattr(sys, "argv", ["pitch_pack.py", "fx", "--json"])
    assert pitch_pack.main() == 0
    data = json.loads(capsys.readouterr().out)
    assert data["built"] is False and data["places"][0]["id"] == "bar"
    assert [r["version"] for r in data["releases"]] == ["0.0"]
    assert data["moment_kinds_shipped"]["firsts"] == 0


def test_missing_pages_are_named(tmp_path, monkeypatch, capsys):
    _game(tmp_path, monkeypatch, with_pages=False)
    assert pitch_pack.main() == 0
    out = capsys.readouterr().out
    assert "games/fx/WANT.md not found." in out and "games/fx/IDEA.md not found." in out


def test_nothing_at_all_is_not_found(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(sys, "argv", ["pitch_pack.py", "nope"])
    assert pitch_pack.main() == 2
    assert "not found" in capsys.readouterr().out
