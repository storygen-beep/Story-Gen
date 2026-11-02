"""pieces.py (2026-11-02): every piece is played by Claude in Chrome as it lands and by LO before a
release. Nothing blocks development; a public build waits for LO's note on every piece."""
import json
import os
import sys

import pytest

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))

import pieces  # noqa: E402

REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", "..", ".."))


@pytest.fixture
def root(tmp_path):
    game = tmp_path / "games" / "fx"
    game.mkdir(parents=True)
    (game / "v2_state.json").write_text(
        json.dumps({"slug": "fx", "phase": "sheets", "name": "Élla"}, indent=2,
                   ensure_ascii=False) + "\n", encoding="utf-8")
    (game / "DECISIONS.md").write_text("# Decisions\n\n## Answered\n\n| 1 | yes |\n")
    return str(tmp_path)


def _dec(root):
    return open(os.path.join(root, "games/fx/DECISIONS.md")).read()


def test_a_game_with_no_pieces_is_clear_for_release(root):
    assert pieces.release_check("fx", root)[1] == 0


def test_done_says_development_carries_on_and_asks_for_the_chrome_play(root):
    out = pieces.done("fx", "ryan-1-4", "Ryan's first four steps", root)
    assert "Development is not blocked" in out and "Claude in Chrome" in out
    assert "pieces.py chrome fx ryan-1-4" in out and "Is it hot?" in out
    p = pieces.load_state("fx", root)["build"]["pieces"][0]
    assert p["chrome"] is None and p["played"] is None


def test_the_ledger_keeps_its_formatting(root):
    pieces.done("fx", "p1", "one", root)
    text = open(os.path.join(root, "games/fx/v2_state.json"), encoding="utf-8").read()
    assert '"name": "Élla"' in text and text.endswith("}\n") and '\n  "slug"' in text


def test_a_chrome_play_is_recorded_but_does_not_clear_the_release(root):
    pieces.done("fx", "p1", "one", root)
    out = pieces.chrome("fx", "p1", "steps 1-3 fire; step 2 says 'tank top' in a dress", root)
    assert "still owed" in out
    assert pieces.load_state("fx", root)["build"]["pieces"][0]["chrome"]["report"].startswith("steps")
    assert "played by Claude in Chrome" in _dec(root)
    assert pieces.release_check("fx", root)[1] == 1


def test_the_release_waits_for_los_note_and_says_how(root):
    pieces.done("fx", "p1", "one", root)
    text, code = pieces.release_check("fx", root)
    assert code == 1 and "p1: one" in text and "played fx --all" in text


def test_one_lo_note_can_cover_every_piece(root):
    pieces.done("fx", "p1", "one", root)
    pieces.done("fx", "p2", "two", root)
    pieces.played("fx", "p1", "step 3 too tame", root)
    out = pieces.played("fx", "--all", "played release 1 to Bold, fine", root)
    assert "p2" in out and "release hold is clear" in out
    assert pieces.release_check("fx", root)[1] == 0
    dec = _dec(root)
    assert dec.count("· played by LO:") == 2 and '"step 3 too tame"' in dec
    assert dec.index("## Answered") < dec.index("## Play notes")
    notes = dec[dec.index("## Play notes"):].splitlines()
    assert notes[-2].startswith("- ") and notes[-1].startswith("- ")


def test_play_notes_go_before_a_later_heading(root):
    path = os.path.join(root, "games/fx/DECISIONS.md")
    open(path, "w").write("# D\n\n## Play notes\n\n- old line\n\n## Later\n\ntext\n")
    pieces.done("fx", "p1", "one", root)
    pieces.played("fx", "p1", "fine", root)
    dec = open(path).read()
    assert dec.index('"fine"') < dec.index("## Later") and "- old line\n- " in dec


def test_empty_notes_second_notes_and_reused_ids_are_refused(root):
    pieces.done("fx", "p1", "one", root)
    with pytest.raises(SystemExit):
        pieces.played("fx", "p1", "   ", root)
    with pytest.raises(SystemExit):
        pieces.chrome("fx", "p1", "", root)
    pieces.played("fx", "p1", "fine", root)
    with pytest.raises(SystemExit):
        pieces.played("fx", "p1", "again", root)
    with pytest.raises(SystemExit):
        pieces.played("fx", "--all", "nothing left", root)
    with pytest.raises(SystemExit):
        pieces.done("fx", "p1", "same id", root)


def test_the_blocking_hook_is_gone():
    # LO, 2026-11-02: "don't want development to be blocked by it."
    assert not os.path.exists(os.path.join(REPO, ".claude", "hooks", "play_gate.py"))
    settings = os.path.join(REPO, ".claude", "settings.json")
    assert not os.path.exists(settings) or "play_gate" not in open(settings).read()


def test_release_upload_refuses_while_lo_has_not_played(tmp_path, monkeypatch):
    sys.path.insert(0, os.path.join(REPO, "scripts"))
    import release_upload as ru
    monkeypatch.setattr(ru, "REPO_ROOT", tmp_path)
    (tmp_path / "games" / "g").mkdir(parents=True)
    (tmp_path / "games" / "g" / "v2_state.json").write_text("{}")
    calls = []

    class R:
        def __init__(self, rc):
            self.returncode = rc

    # --ship passes, the release check does not
    monkeypatch.setattr(ru.subprocess, "run",
                        lambda cmd, cwd=None: calls.append(cmd) or R(0 if "--ship" in cmd else 1))
    with pytest.raises(ru.ReleaseError, match="LO has not played"):
        ru.check_ship("g")
    assert "release-check" in calls[1]
