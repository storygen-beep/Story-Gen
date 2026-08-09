"""`picks` — what an install consumed, so a selected clip can still be traced.

Installing DROPS the option row (`_drop_option`), and that row held the only copy of
the clip's Google `docid`. Nothing downstream could recover it: a pool member is named
`c<md5(url)>` (one-way) and a single slot's file is named after the SLOT, carrying no
provenance at all. So the picker's ⇢ died the moment you chose a clip — the one action
meaning "I want this most" was also the only one that erased where it came from.

What is actually load-bearing here, in order:

  1. grab must COPY the row before dropping it. A pick with no docid is a dead ⇢.
  2. A single slot REPLACES its pick; a pool APPENDS. Get this backwards and either
     a pool loses every peer's provenance on the next Select, or a single slot
     accumulates rows pointing at files that were overwritten weeks ago.
  3. Undo must round-trip. `pool_unselect` and `_preserve_current_as_option` hand the
     pick back to the option they demote it into, or the shelf refills with the same
     dead `⇢ no id` tiles this exists to kill — 276 of them on vesper.
  4. Provenance is NEVER a gate. The bytes are on disk by the time any of this runs.

    pytest tests/test_media_finder_picks.py -q
"""
import json
from pathlib import Path
from unittest.mock import patch

import pytest
from django.test import RequestFactory

import api.v1.media_finder as mf


@pytest.fixture
def games_root(tmp_path, monkeypatch):
    monkeypatch.setattr(mf, "GAMES_ROOT", tmp_path)
    (tmp_path / "g" / "videos").mkdir(parents=True)
    return tmp_path


def _post(view, payload):
    req = RequestFactory().post(
        "/", data=json.dumps(payload), content_type="application/json"
    )
    return view(req)


def _get(view, qs):
    return view(RequestFactory().get("/?" + qs))


def _body(resp):
    return json.loads(resp.content)


def _ledger(games_root):
    return mf._read_options(games_root / "g")


def _picks(games_root, slot):
    return _ledger(games_root)["picks"].get(slot) or []


def _shelf(games_root, slot):
    return _ledger(games_root)["options"].get(slot) or []


def _fake_download(u, dest, extra_headers=None):
    Path(dest).write_bytes(b"\x00" * 60000)
    return True, None


def _stock(games_root, slot, url, **kw):
    """Put one option on a shelf, the way a harvest would."""
    body = {"game": "g", "file": slot, "url": url, "media_kind": "img"}
    body.update(kw)
    return _post(mf.options_add, body)


def _grab(games_root, slot, url, **kw):
    body = {"game": "g", "file": slot, "url": url}
    body.update(kw)
    with patch.object(mf, "download_direct", side_effect=_fake_download):
        return _post(mf.grab, body)


# ── grab records what it consumed ────────────────────────────────────────────


def test_grab_copies_the_consumed_rows_docid_onto_the_pick(games_root):
    _stock(
        games_root,
        "sex/a_t5.webm",
        "https://x.test/a.gif",
        query="kneeling gif",
        docid="FvF5n0MlBjcrfM",
        thumb="https://encrypted-tbn0.gstatic.com/images?q=t",
    )
    assert _body(_grab(games_root, "sex/a_t5.webm", "https://x.test/a.gif"))["success"]

    picks = _picks(games_root, "sex/a_t5.webm")
    assert len(picks) == 1
    assert picks[0]["url"] == "https://x.test/a.gif"
    assert picks[0]["docid"] == "FvF5n0MlBjcrfM"
    assert picks[0]["found_by"] == ["kneeling gif"]
    assert picks[0]["filename"] == "a_t5.gif"  # the extension the SOURCE resolved to
    # …and the option really is gone. The pick is a record, not a second shelf.
    assert _shelf(games_root, "sex/a_t5.webm") == []


def test_a_grab_with_no_matching_option_still_records_the_url(games_root):
    """A hand-driven grab, or a url the shelf never held. There is no docid to
    recover, but the source url is still worth keeping — a later search that
    re-finds it attaches the id to the option, and the picker joins on the url."""
    assert _body(_grab(games_root, "sex/a_t5.webm", "https://x.test/a.gif"))["success"]
    picks = _picks(games_root, "sex/a_t5.webm")
    assert len(picks) == 1
    assert picks[0]["url"] == "https://x.test/a.gif"
    assert "docid" not in picks[0]


def test_a_pick_is_never_written_with_an_empty_url_key(games_root):
    """A local re-select carries no remote. `url` must then be ABSENT, not "" —
    the picker tests `pick.url` to decide whether a ⇢ can be offered at all, and an
    empty string would render a button that cannot possibly work."""
    prev = games_root / "g" / ".find-media" / "previous"
    prev.mkdir(parents=True)
    (prev / "old.gif").write_bytes(b"\x00" * 60000)
    _post(
        mf.grab,
        {
            "game": "g",
            "file": "sex/a_t5.webm",
            "url": "",
            "local_path": "g/.find-media/previous/old.gif",
        },
    )
    picks = _picks(games_root, "sex/a_t5.webm")
    assert len(picks) == 1 and "url" not in picks[0]


# ── single REPLACES, pool APPENDS ────────────────────────────────────────────


def test_a_single_slot_replaces_its_pick(games_root):
    _grab(games_root, "sex/a_t5.webm", "https://x.test/one.gif")
    _grab(games_root, "sex/a_t5.webm", "https://x.test/two.gif")
    picks = _picks(games_root, "sex/a_t5.webm")
    assert len(picks) == 1
    assert picks[0]["url"] == "https://x.test/two.gif"


def test_a_pool_appends_and_keeps_its_peers(games_root):
    for name in ("one", "two", "three"):
        _grab(
            games_root,
            "sex/pool_t5",
            f"https://x.test/{name}.gif",
            pool_dir="sex/pool_t5",
        )
    picks = _picks(games_root, "sex/pool_t5")
    assert len(picks) == 3
    assert {p["url"] for p in picks} == {
        "https://x.test/one.gif",
        "https://x.test/two.gif",
        "https://x.test/three.gif",
    }


def test_a_pool_regrab_of_the_same_url_leaves_exactly_one_pick(games_root):
    """The stem is md5(url), so a re-grab is idempotent on disk. The pick must be
    too, or the same clip accumulates a row per click."""
    for _ in range(3):
        _grab(games_root, "sex/pool_t5", "https://x.test/a.gif", pool_dir="sex/pool_t5")
    assert len(_picks(games_root, "sex/pool_t5")) == 1


def test_a_regrab_under_a_different_extension_leaves_exactly_one_pick(games_root):
    """The url is the identity; the filename is not. A source that resolved .gif
    once and .webm the next time changes the stem's extension, so matching on
    filename alone would leave a row pointing at a file that no longer exists."""
    url = "https://x.test/a.gif"
    _grab(games_root, "sex/pool_t5", url, pool_dir="sex/pool_t5")
    first = _picks(games_root, "sex/pool_t5")[0]["filename"]
    # grab reads the extension off the SOURCE url before it ever asks the server,
    # so this is the only lever that actually moves it. Patching the content-type
    # helper instead does nothing here and the test passes without testing anything.
    with patch.object(mf, "download_direct", side_effect=_fake_download), patch.object(
        mf, "get_extension_from_url", return_value="webm"
    ):
        _post(
            mf.grab,
            {"game": "g", "file": "sex/pool_t5", "url": url, "pool_dir": "sex/pool_t5"},
        )
    picks = _picks(games_root, "sex/pool_t5")
    assert picks[0]["filename"].endswith(".webm")   # the extension really moved
    assert picks[0]["filename"] != first
    assert len([p for p in picks if p["url"] == url]) == 1


# ── undo round-trips the provenance ──────────────────────────────────────────


def test_unselecting_a_pool_clip_hands_its_provenance_to_the_demoted_option(games_root):
    _stock(
        games_root,
        "sex/pool_t5",
        "https://x.test/a.gif",
        query="kneeling gif",
        docid="FvF5n0MlBjcrfM",
    )
    _grab(games_root, "sex/pool_t5", "https://x.test/a.gif", pool_dir="sex/pool_t5")
    filename = _picks(games_root, "sex/pool_t5")[0]["filename"]

    res = _post(
        mf.pool_unselect, {"game": "g", "dir": "sex/pool_t5", "filename": filename}
    )
    assert _body(res)["success"]

    assert _picks(games_root, "sex/pool_t5") == []  # not installed any more
    demoted = [
        o for o in _shelf(games_root, "sex/pool_t5") if o.get("origin") == "previous"
    ]
    assert len(demoted) == 1
    # The remote goes in `source_url`, NEVER `url`: `url` is what a re-select
    # installs from, and a demoted pick must come back by COPY so the exact
    # approved bytes return rather than whatever the host serves today.
    assert demoted[0]["source_url"] == "https://x.test/a.gif"
    assert demoted[0]["docid"] == "FvF5n0MlBjcrfM"
    assert demoted[0]["url"].startswith("/games/")
    assert demoted[0]["local_path"]


def test_replacing_a_single_slot_hands_provenance_to_the_incumbent(games_root):
    _stock(
        games_root, "sex/a_t5.webm", "https://x.test/one.gif", docid="FvF5n0MlBjcrfM"
    )
    _grab(games_root, "sex/a_t5.webm", "https://x.test/one.gif")
    _grab(games_root, "sex/a_t5.webm", "https://x.test/two.gif")

    demoted = [
        o for o in _shelf(games_root, "sex/a_t5.webm") if o.get("origin") == "previous"
    ]
    assert len(demoted) == 1
    assert demoted[0]["source_url"] == "https://x.test/one.gif"
    assert demoted[0]["docid"] == "FvF5n0MlBjcrfM"


def test_a_demoted_pick_can_be_re_selected_and_keeps_its_provenance(games_root):
    """The full loop: select → unselect → re-select. The pick that comes back must
    still know the remote, or the round trip quietly launders it away."""
    _stock(games_root, "sex/pool_t5", "https://x.test/a.gif", docid="FvF5n0MlBjcrfM")
    _grab(games_root, "sex/pool_t5", "https://x.test/a.gif", pool_dir="sex/pool_t5")
    filename = _picks(games_root, "sex/pool_t5")[0]["filename"]
    _post(mf.pool_unselect, {"game": "g", "dir": "sex/pool_t5", "filename": filename})

    demoted = [
        o for o in _shelf(games_root, "sex/pool_t5") if o.get("origin") == "previous"
    ][0]
    _post(
        mf.grab,
        {
            "game": "g",
            "file": "sex/pool_t5",
            "pool_dir": "sex/pool_t5",
            "url": demoted["url"],
            "local_path": demoted["local_path"],
        },
    )
    picks = _picks(games_root, "sex/pool_t5")
    assert len(picks) == 1
    assert picks[0]["url"] == "https://x.test/a.gif"
    assert picks[0]["docid"] == "FvF5n0MlBjcrfM"


# ── provenance is bookkeeping, never a gate ──────────────────────────────────


def test_recording_a_pick_never_raises(games_root):
    """The bytes are already in videos/ by the time this runs. A raise here would
    turn a successful install into a 500, and the human would click again —
    installing twice over a swap that already happened.

    Note this is asserted on `_record_pick` directly, NOT through grab: `_drop_option`
    shares the same writer and is deliberately not fail-soft — dropping the consumed
    option is correctness, not bookkeeping, and it must still surface as an error.
    """
    with patch.object(mf, "_write_options", side_effect=OSError("disk full")):
        mf._record_pick(
            games_root / "g", "g", "sex/a_t5.webm", "a_t5.gif", "https://x.test/a.gif"
        )
    assert _picks(games_root, "sex/a_t5.webm") == []


def test_forgetting_a_pick_never_raises(games_root):
    _grab(games_root, "sex/a_t5.webm", "https://x.test/a.gif")
    with patch.object(mf, "_write_options", side_effect=OSError("disk full")):
        assert (
            mf._forget_pick(games_root / "g", "g", "sex/a_t5.webm", "a_t5.gif") is None
        )
    # The write failed, so the pick is still there — the caller gets no provenance
    # to hand on, which is exactly the pre-picks behaviour rather than a corruption.
    assert len(_picks(games_root, "sex/a_t5.webm")) == 1


def test_forgetting_a_pick_that_does_not_exist_is_a_clean_none(games_root):
    assert mf._forget_pick(games_root / "g", "g", "sex/pool_t5", "nope.gif") is None


def test_recording_a_pick_with_no_filename_is_a_no_op(games_root):
    mf._record_pick(games_root / "g", "g", "sex/a_t5.webm", "", "https://x.test/a.gif")
    assert _picks(games_root, "sex/a_t5.webm") == []


# ── the wire ─────────────────────────────────────────────────────────────────


def test_options_list_carries_the_picks(games_root):
    _grab(games_root, "sex/a_t5.webm", "https://x.test/a.gif")
    body = _body(_get(mf.options_list, "game=g&file=sex/a_t5.webm"))
    assert len(body["picks"]) == 1
    assert body["picks"][0]["url"] == "https://x.test/a.gif"


def test_picks_are_keyed_by_slot_key_not_by_file(games_root):
    """A tagged block's shelf lives under its `id` while the bytes still land at the
    declared path. The pick has to follow the SHELF, or the picker looks it up under
    a key nothing ever wrote."""
    with patch.object(mf, "download_direct", side_effect=_fake_download):
        _post(
            mf.grab,
            {
                "game": "g",
                "file": "sex/renner_oral_t5.webm",
                "slot_key": "renner_oral",
                "url": "https://x.test/a.gif",
            },
        )
    assert _picks(games_root, "renner_oral")
    assert _picks(games_root, "sex/renner_oral_t5.webm") == []


# ── interaction with queries/remove ──────────────────────────────────────────


def test_deleting_a_search_strips_the_label_but_keeps_the_pick(games_root):
    """A pick is a file in the GAME. Deleting the search that found it cannot
    un-install it — but it must not keep crediting a search that no longer exists."""
    _stock(games_root, "sex/a_t5.webm", "https://x.test/a.gif", query="kneeling gif")
    _grab(games_root, "sex/a_t5.webm", "https://x.test/a.gif")
    _post(
        mf.queries_remove,
        {"game": "g", "file": "sex/a_t5.webm", "query": "kneeling gif"},
    )

    picks = _picks(games_root, "sex/a_t5.webm")
    assert len(picks) == 1
    # POPPED, not emptied — same invariant the options hold: no row anywhere in the
    # store ever carries `found_by: []`.
    assert "found_by" not in picks[0]
    assert picks[0]["url"] == "https://x.test/a.gif"


def test_deleting_one_of_two_searches_leaves_the_other_on_the_pick(games_root):
    _stock(games_root, "sex/a_t5.webm", "https://x.test/a.gif", query="one")
    _stock(games_root, "sex/a_t5.webm", "https://x.test/a.gif", query="two")
    _grab(games_root, "sex/a_t5.webm", "https://x.test/a.gif")
    _post(mf.queries_remove, {"game": "g", "file": "sex/a_t5.webm", "query": "one"})
    assert _picks(games_root, "sex/a_t5.webm")[0]["found_by"] == ["two"]
