"""`media-review/reviews` — the findability colour (LO, 2026-11-28).

Green: the right media was easy to find on the shelf and matches. Yellow: hard to
find. Red: impossible. It is a finding about the SEARCH, so it lives beside the
verdict and never overwrites it, and the verdict buttons never wipe it.

    pytest tests/test_media_review_findability.py -q
"""
import json

import pytest
from django.test import RequestFactory

import api.v1.game_review as gr
import api.v1.media_review as mr

from tests.test_media_review_shelf_state import SINGLE, TOML


@pytest.fixture
def root(tmp_path, monkeypatch):
    monkeypatch.setattr(gr, "GAMES_ROOT", tmp_path)
    monkeypatch.setattr(mr, "GAMES_ROOT", tmp_path)
    r = tmp_path / "g"
    (r / "toml_phases").mkdir(parents=True)
    (r / ".find-media").mkdir(parents=True)
    (r / "videos").mkdir(parents=True)
    (r / "toml_phases" / "7_final_game.toml").write_text(TOML % SINGLE)
    return r


def _post(body):
    req = RequestFactory().post("/x?game=g", data=json.dumps(body), content_type="application/json")
    return mr.post_review(req)


def _ledger(root):
    return json.loads((root / ".find-media" / "media_reviews.json").read_text())["reviews"]["sex/a_t5.webm"]


def test_a_colour_is_saved_and_listed(root):
    assert _post({"file": "sex/a_t5.webm", "findability": "yellow"}).status_code == 200
    item = mr._enumerate("g", root)["items"][0]
    assert item["findability"] == "yellow"
    assert mr._enumerate("g", root)["counts"]["findability"] == {"green": 0, "yellow": 1, "red": 0}


def test_a_colour_never_clobbers_the_verdict_and_the_verdict_never_clobbers_the_colour(root):
    _post({"file": "sex/a_t5.webm", "status": "approved", "note": "good"})
    _post({"file": "sex/a_t5.webm", "findability": "red"})
    e = _ledger(root)
    assert (e["status"], e["note"], e["findability"]) == ("approved", "good", "red")
    _post({"file": "sex/a_t5.webm", "status": "disapproved", "note": "wrong act"})
    e = _ledger(root)
    assert (e["status"], e["note"], e["findability"]) == ("disapproved", "wrong act", "red")


def test_a_colour_can_be_cleared(root):
    _post({"file": "sex/a_t5.webm", "findability": "green"})
    _post({"file": "sex/a_t5.webm", "findability": None})
    assert _ledger(root)["findability"] is None


@pytest.mark.parametrize("body", [{"file": "sex/a_t5.webm", "findability": "blue"}, {"file": "sex/a_t5.webm"}])
def test_a_bad_colour_or_an_empty_save_is_refused(root, body):
    assert _post(body).status_code == 400
