"""Pool folders in the media-finder API — install, list, unselect.

A pool block names a FOLDER; everything inside it plays, cycling one clip per
visit. "Selected" is therefore not a field anywhere — it is simply *the file is in
the folder*. That makes select/unselect a move and leaves no second source of
truth to drift out of sync with the build.

⚠️ Two load-bearing tests here.

`test_two_pool_installs_coexist` — `grab`'s normal path deletes every same-stem file
in the target directory before writing (`media_finder.py`, the
`existing.stem == filename_base` loop) because a single slot holds exactly one file.
Run that against a pool and installing clip 2 silently deletes clip 1. If that guard
is ever removed, this file must go red.

`test_a_download_in_flight_is_invisible_to_the_pool` — `grab` stages its download in
`.find-media/incoming/`, never in the pool folder. It used to stage in place under a
`.incoming-<stem>` name, and every enumerator filters on SUFFIX ONLY, so the partial
was advertised as a real clip while it grew (measured: 3,350,528 -> 4,235,264 bytes
across consecutive polls) and it held tile #1 because "." sorts before "c". If staging
ever moves back into the pool folder, that test must go red.

    pytest tests/test_media_finder_pools.py -q
"""
import json
import threading
import time
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


def _grab(pool_dir="sex/oral_t5", url="https://x.test/a.webm", game="g"):
    """Drive `grab` with the network stubbed — download_direct writes the temp file."""
    def fake_download(u, dest, extra_headers=None):
        Path(dest).write_bytes(b"\x00" * 60000)
        return True, None

    with patch.object(mf, "download_direct", side_effect=fake_download):
        return _post(mf.grab, {
            "game": game, "file": pool_dir, "pool_dir": pool_dir, "url": url,
        })


def _members(games_root, pool_dir="sex/oral_t5"):
    d = games_root / "g" / "videos" / pool_dir
    return sorted(p.name for p in d.iterdir()) if d.is_dir() else []


# ── the dangerous one ────────────────────────────────────────────────────────

def test_two_pool_installs_coexist(games_root):
    """Installing clip 2 must NOT delete clip 1.

    This is the whole feature: a pool is many files in one folder. `grab`'s
    single-slot path unlinks every same-stem file before writing, which would make
    a pool permanently one clip deep, silently.
    """
    assert json.loads(_grab(url="https://x.test/one.webm").content)["success"]
    assert json.loads(_grab(url="https://x.test/two.webm").content)["success"]

    assert len(_members(games_root)) == 2, "the second install ate the first"


def test_three_installs_give_three_clips(games_root):
    for i in range(3):
        _grab(url=f"https://x.test/{i}.webm")
    assert len(_members(games_root)) == 3


def test_regrabbing_the_same_source_is_idempotent(games_root):
    """A refetch of the SAME url should replace, not pile up near-duplicates."""
    _grab(url="https://x.test/same.webm")
    _grab(url="https://x.test/same.webm")
    assert len(_members(games_root)) == 1


def test_pool_install_lands_inside_the_folder(games_root):
    _grab(pool_dir="sex/oral_t5")
    assert (games_root / "g" / "videos" / "sex" / "oral_t5").is_dir()
    assert _members(games_root)


def test_pool_install_does_not_clear_the_review_verdict(games_root):
    """Adding a fourth clip must not un-judge the three already approved."""
    with patch.object(mf, "_clear_review_status") as cleared:
        _grab()
    assert not cleared.called


# ── staging never touches the pool folder ────────────────────────────────────

def test_a_download_in_flight_is_invisible_to_the_pool(games_root):
    """A half-written download must be neither on disk in the pool nor in the API.

    The measured bug: the API advertised `.incoming-c14745ba3e2.gif` as a real pool
    member with its byte count climbing across consecutive polls, at tile #1 because
    "." sorts before "c". If staging ever moves back into the pool folder, this fails.
    """
    seen = {}

    def fake_download(u, dest, extra_headers=None):
        Path(dest).write_bytes(b"\x00" * 30000)          # half-downloaded, still open
        seen["on_disk"] = _members(games_root)            # unfiltered iterdir
        req = RequestFactory().get("/", {"game": "g", "dir": "sex/oral_t5"})
        seen["listed"] = json.loads(mf.pool_list(req).content)["items"]
        Path(dest).write_bytes(b"\x00" * 60000)          # ...and now it finishes
        return True, None

    with patch.object(mf, "download_direct", side_effect=fake_download):
        res = _post(mf.grab, {
            "game": "g", "file": "sex/oral_t5",
            "pool_dir": "sex/oral_t5", "url": "https://x.test/a.webm",
        })

    assert json.loads(res.content)["success"]
    assert seen["on_disk"] == [], "a partial download was sitting in the live pool"
    assert seen["listed"] == [], "the API advertised a partial download as a real clip"
    assert len(_members(games_root)) == 1, "the finished clip should be installed"


def test_a_failed_download_leaves_no_staging_file(games_root):
    def fake_download(u, dest, extra_headers=None):
        Path(dest).write_bytes(b"\x00" * 100)   # partial bytes on disk...
        return False, "boom"                     # ...but the fetch failed

    with patch.object(mf, "download_direct", side_effect=fake_download):
        res = _post(mf.grab, {
            "game": "g", "file": "sex/oral_t5",
            "pool_dir": "sex/oral_t5", "url": "https://x.test/a.webm",
        })

    assert json.loads(res.content)["success"] is False
    assert list(mf._incoming_dir(games_root / "g").iterdir()) == []
    assert _members(games_root) == []


def test_an_exception_mid_download_leaves_no_staging_file(games_root):
    """The `finally` must clean up even when nothing returned a response."""
    def explode(u, dest, extra_headers=None):
        Path(dest).write_bytes(b"\x00" * 100)
        raise RuntimeError("connection reset")

    with patch.object(mf, "download_direct", side_effect=explode):
        with pytest.raises(RuntimeError):
            _post(mf.grab, {
                "game": "g", "file": "sex/oral_t5",
                "pool_dir": "sex/oral_t5", "url": "https://x.test/a.webm",
            })

    assert list(mf._incoming_dir(games_root / "g").iterdir()) == []


def test_install_failure_returns_json_not_an_html_500(games_root):
    """find.html parses every response body, so an uncaught raise reads as
    "server unreachable" rather than the real reason."""
    def fake_download(u, dest, extra_headers=None):
        Path(dest).write_bytes(b"\x00" * 60000)
        return True, None

    with patch.object(mf, "download_direct", side_effect=fake_download):
        with patch.object(mf.os, "replace", side_effect=FileNotFoundError("gone")):
            res = _post(mf.grab, {
                "game": "g", "file": "sex/oral_t5",
                "pool_dir": "sex/oral_t5", "url": "https://x.test/a.webm",
            })

    body = json.loads(res.content)          # must parse — that is the point
    assert res.status_code == 500
    assert body["success"] is False
    assert "install failed" in body["error"]
    assert list(mf._incoming_dir(games_root / "g").iterdir()) == []


def test_stale_staging_is_reaped_but_a_fresh_one_is_not(games_root):
    import os as _os
    staging = mf._incoming_dir(games_root / "g")
    staging.mkdir(parents=True)
    old, fresh = staging / "old.part", staging / "fresh.part"
    old.write_bytes(b"x")
    fresh.write_bytes(b"x")
    seven_hours_ago = time.time() - 7 * 3600
    _os.utime(old, (seven_hours_ago, seven_hours_ago))

    _grab()

    assert not old.exists(), "a temp no live grab could own should be reaped"
    assert fresh.exists(), "a temp that could still be in flight must be left alone"


def test_staging_and_the_pool_share_a_filesystem(games_root):
    """os.replace is atomic only within one filesystem — the unstated precondition."""
    _grab()
    game_dir = games_root / "g"
    staging = mf._incoming_dir(game_dir)
    pool = game_dir / "videos" / "sex" / "oral_t5"
    assert staging.stat().st_dev == pool.stat().st_dev


def test_two_grabs_in_flight_at_once_stage_to_different_paths(games_root):
    """Two SIMULTANEOUS grabs must never share a staging path.

    `_pool_member_stem` is md5(url), so the same url grabbed into two different pools
    yields the same `filename_base`. Without the pid+tid suffix both would stage
    through one file and the first `os.replace` would move it out from under the
    second, whose own replace then raises FileNotFoundError — the exact failure
    `write_json_atomic` documents ("15 of 40 requests, measured").

    Sequential grabs on one thread legitimately reuse the path: the first one's
    `finally` has already removed it. Only overlap is dangerous, so the test forces
    overlap with a barrier rather than looping.
    """
    staged, both_inside = [], threading.Barrier(2, timeout=5)
    lock = threading.Lock()

    def fake_download(u, dest, extra_headers=None):
        with lock:
            staged.append(str(dest))
        both_inside.wait()          # neither returns until both have staged
        Path(dest).write_bytes(b"\x00" * 60000)
        return True, None

    def run(pool):
        _post(mf.grab, {
            "game": "g", "file": pool, "pool_dir": pool,
            "url": "https://x.test/same.webm",
        })

    with patch.object(mf, "download_direct", side_effect=fake_download):
        threads = [threading.Thread(target=run, args=(p,))
                   for p in ("sex/oral_t5", "sex/anal_t5")]
        for t in threads:
            t.start()
        for t in threads:
            t.join(timeout=10)

    assert len(staged) == 2
    assert staged[0] != staged[1], "two in-flight grabs shared one staging path"


def test_grab_refuses_a_dot_prefixed_local_path(games_root):
    prev = games_root / "g" / ".find-media" / "previous"
    prev.mkdir(parents=True)
    poisoned = prev / ".incoming-cabc-20260803-155509.gif"
    poisoned.write_bytes(b"GIF89a" + b"\x00" * 100)   # truncated, no trailer

    res = _post(mf.grab, {
        "game": "g", "file": "sex/oral_t5", "pool_dir": "sex/oral_t5",
        "local_path": "g/.find-media/previous/.incoming-cabc-20260803-155509.gif",
    })

    assert res.status_code == 400
    assert _members(games_root) == [], "a truncated staging file was installed"


# ── the single-slot path must be untouched ───────────────────────────────────

def test_single_slot_install_still_replaces(games_root):
    """No pool_dir => the old behaviour: one file per slot, incumbent removed."""
    def fake_download(u, dest, extra_headers=None):
        Path(dest).write_bytes(b"\x00" * 60000)
        return True, None

    videos = games_root / "g" / "videos" / "scenes"
    videos.mkdir(parents=True)
    (videos / "beat.webm").write_bytes(b"old")

    with patch.object(mf, "download_direct", side_effect=fake_download):
        res = _post(mf.grab, {
            "game": "g", "file": "scenes/beat.webm", "url": "https://x.test/new.webm",
        })

    assert json.loads(res.content)["success"]
    assert sorted(p.name for p in videos.iterdir()) == ["beat.webm"]
    assert list(mf._incoming_dir(games_root / "g").iterdir()) == []


# ── pool/list ────────────────────────────────────────────────────────────────

def test_pool_list_returns_members_in_natural_order(games_root):
    d = games_root / "g" / "videos" / "sex" / "oral_t5"
    d.mkdir(parents=True)
    # `.incoming-c1.gif` carries a real media suffix, so a suffix-only filter lets it
    # through — and "." sorts before "c", so it would take tile #1 and shift every
    # caption. `._clip.gif` is the macOS AppleDouble form of the same hole.
    for name in ("clip_10.webm", "clip_2.webm", "clip_1.webm", "notes.txt",
                 ".incoming-c1.gif", "._clip_1.webm"):
        (d / name).write_bytes(b"x")

    req = RequestFactory().get("/", {"game": "g", "dir": "sex/oral_t5"})
    body = json.loads(mf.pool_list(req).content)

    assert [i["filename"] for i in body["items"]] == [
        "clip_1.webm", "clip_2.webm", "clip_10.webm",
    ], "lexical sort would put clip_10 second"
    assert body["count"] == 3, "non-media and dot-prefixed files are not pool members"


def test_pool_list_on_an_absent_folder_is_empty_not_an_error(games_root):
    req = RequestFactory().get("/", {"game": "g", "dir": "sex/nothing_here"})
    res = mf.pool_list(req)
    assert res.status_code == 200
    assert json.loads(res.content)["items"] == []


def test_pool_list_marks_video_vs_image(games_root):
    d = games_root / "g" / "videos" / "p"
    d.mkdir(parents=True)
    (d / "a.webm").write_bytes(b"x")
    (d / "b.jpg").write_bytes(b"x")

    req = RequestFactory().get("/", {"game": "g", "dir": "p"})
    kinds = {i["filename"]: i["media_kind"] for i in json.loads(mf.pool_list(req).content)["items"]}
    assert kinds == {"a.webm": "video", "b.jpg": "img"}


# ── pool/unselect ────────────────────────────────────────────────────────────

def test_unselect_moves_the_clip_out_and_re_shelves_it(games_root):
    d = games_root / "g" / "videos" / "sex" / "oral_t5"
    d.mkdir(parents=True)
    (d / "gone.webm").write_bytes(b"x")

    res = _post(mf.pool_unselect, {"game": "g", "dir": "sex/oral_t5", "filename": "gone.webm"})
    assert json.loads(res.content)["success"]

    # It stops playing immediately — the folder IS the truth.
    assert _members(games_root) == []
    # ...and comes back as a one-click-reversible option on the POOL's shelf.
    opts = mf._read_options(games_root / "g")["options"]["sex/oral_t5"]
    assert len(opts) == 1
    assert opts[0]["origin"] == "previous"
    assert (games_root / opts[0]["local_path"]).is_file()


def test_unselect_refuses_a_traversal_filename(games_root):
    d = games_root / "g" / "videos" / "p"
    d.mkdir(parents=True)
    secret = games_root / "g" / "videos" / "secret.webm"
    secret.write_bytes(b"x")

    res = _post(mf.pool_unselect, {"game": "g", "dir": "p", "filename": "../secret.webm"})
    assert res.status_code == 400
    assert secret.is_file()


def test_unselect_refuses_a_dot_prefixed_filename(games_root):
    """Unselecting a staging file re-shelved a TRUNCATED clip as a one-click option.

    Both halves matter: the file must stay put, AND nothing may be added to the shelf.
    Shelving is the actual damage — a 2 MB half-GIF sat at index 0 of a real slot.
    """
    d = games_root / "g" / "videos" / "p"
    d.mkdir(parents=True)
    staged = d / ".incoming-cabc.gif"
    staged.write_bytes(b"GIF89a" + b"\x00" * 100)

    res = _post(mf.pool_unselect, {
        "game": "g", "dir": "p", "filename": ".incoming-cabc.gif",
    })

    assert res.status_code == 400
    assert staged.is_file(), "the file was moved out despite the refusal"
    shelved = mf._read_options(games_root / "g")["options"]
    assert not shelved.get("p"), "a truncated staging file was shelved as an option"


def test_unselect_on_a_missing_file_is_404(games_root):
    res = _post(mf.pool_unselect, {"game": "g", "dir": "p", "filename": "nope.webm"})
    assert res.status_code == 404


# ── path handling ────────────────────────────────────────────────────────────

@pytest.mark.parametrize("raw,expected", [
    ("sex/oral_t5", "sex/oral_t5"),
    ("sex/oral_t5/", "sex/oral_t5"),
    ("/sex/oral_t5", "sex/oral_t5"),
    ("sex\\oral_t5", "sex/oral_t5"),
    ("videos/sex/oral_t5", "sex/oral_t5"),
    ("  sex/oral_t5  ", "sex/oral_t5"),
])
def test_clean_pool_dir_normalises(raw, expected):
    assert mf._clean_pool_dir(raw) == expected


@pytest.mark.parametrize("bad", ["", "   ", "../etc", "sex/../../etc", ".", None, 5])
def test_clean_pool_dir_rejects_traversal_and_junk(bad):
    assert mf._clean_pool_dir(bad) == ""


def test_clean_pool_dir_does_not_mangle_a_real_folder_name():
    """`parse_scene_path` would rewrite a dot to '_' and strip a media extension,
    producing a folder name that does not exist on disk — a permanently-missing
    pool with no error. `_clean_pool_dir` must preserve the name verbatim."""
    assert mf._clean_pool_dir("sex/oral.t5") == "sex/oral.t5"
    assert mf._clean_pool_dir("sex/clip.webm") == "sex/clip.webm"


# ── shelf ordering + re-select bookkeeping ───────────────────────────────────

def test_an_unselected_clip_goes_to_the_FRONT_of_the_shelf(games_root):
    """Appending buried it. media_lab's shelf is 148 deep, so a just-unselected
    clip landed at position 149 — "one click to undo" meant scrolling past
    everything first. Fresh candidates still append."""
    for i in range(5):
        mf._add_option(games_root / "g", "g", "p", url=f"https://x.test/{i}.gif")
    d = games_root / "g" / "videos" / "p"
    d.mkdir(parents=True)
    (d / "gone.webm").write_bytes(b"x")

    _post(mf.pool_unselect, {"game": "g", "dir": "p", "filename": "gone.webm"})

    opts = mf._read_options(games_root / "g")["options"]["p"]
    assert opts[0]["origin"] == "previous", "the undo is buried at the bottom again"
    assert len(opts) == 6


def test_reselecting_a_previous_pick_removes_it_from_the_shelf(games_root):
    """It is back in the slot, so listing it as an available option is a lie —
    and it is matched by local_path because a local re-select carries no url."""
    d = games_root / "g" / "videos" / "p"
    d.mkdir(parents=True)
    (d / "clip.webm").write_bytes(b"x" * 60000)
    _post(mf.pool_unselect, {"game": "g", "dir": "p", "filename": "clip.webm"})

    opt = mf._read_options(games_root / "g")["options"]["p"][0]
    assert opt["origin"] == "previous"

    _post(mf.grab, {"game": "g", "file": "p", "pool_dir": "p",
                    "local_path": opt["local_path"], "url": ""})

    assert mf._read_options(games_root / "g")["options"]["p"] == []
