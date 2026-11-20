"""approve.py: a yes binds to the card's exact bytes; any edit after it reads as 'changed'."""
import json
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import approve  # noqa: E402

CARD = "PIECE p1 · <person>, step 1: <name>\nBuilds: canvas_a\n"


@pytest.fixture
def game(tmp_path):
    (tmp_path / "cards").mkdir()
    (tmp_path / "cards" / "p1.md").write_text(CARD, encoding="utf-8")
    return tmp_path


def test_no_record_is_missing(game):
    assert approve.status(game, "p1") == "missing"


def test_yes_is_recorded_with_hash_words_date(game):
    approve.approve(game, "p1", "yes", date="2026-11-19")
    data = json.loads((game / "approvals.json").read_text())
    assert data["limit"] == approve.LIMIT
    [rec] = data["approvals"]
    assert rec == {"card": "p1", "sha256": approve.card_hash(game, "p1"),
                   "words": "yes", "date": "2026-11-19"}
    assert approve.status(game, "p1") == "approved"


def test_planted_bug_card_edited_after_yes_is_changed(game):
    approve.approve(game, "p1", "yes")
    (game / "cards" / "p1.md").write_text(CARD + "Variants: 2. A, B\n", encoding="utf-8")
    assert approve.status(game, "p1") == "changed"


def test_planted_bug_one_byte_edit_is_changed(game):
    approve.approve(game, "p1", "yes")
    (game / "cards" / "p1.md").write_text(CARD.replace("step 1", "step 2"), encoding="utf-8")
    assert approve.status(game, "p1") == "changed"


def test_reapproval_appends_and_newest_counts(game):
    approve.approve(game, "p1", "yes")
    (game / "cards" / "p1.md").write_text(CARD + "x\n", encoding="utf-8")
    approve.approve(game, "p1", "yes to the change")
    data = json.loads((game / "approvals.json").read_text())
    assert len(data["approvals"]) == 2
    assert approve.status(game, "p1") == "approved"


def test_same_text_twice_is_a_no_op(game):
    approve.approve(game, "p1", "yes")
    assert approve.approve(game, "p1", "yes again").startswith("no change")
    assert len(json.loads((game / "approvals.json").read_text())["approvals"]) == 1


def test_refuses_empty_words(game):
    with pytest.raises(SystemExit):
        approve.approve(game, "p1", "   ")


def test_refuses_missing_card(game):
    with pytest.raises(SystemExit):
        approve.approve(game, "p9", "yes")
    assert not (game / "approvals.json").exists()


def test_deleted_card_is_missing(game):
    approve.approve(game, "p1", "yes")
    (game / "cards" / "p1.md").unlink()
    assert approve.status(game, "p1") == "missing"
