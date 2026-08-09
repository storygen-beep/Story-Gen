"""`manage.py backfill_picks` — recovering provenance by md5, never by search.

A pool member is NAMED after its source url (`_pool_member_stem` = "c" + md5(url)[:10]),
so a clip installed before the picks table existed can be traced back by hashing every
url still on a shelf and looking for the file with that stem. md5 is one-way, so this
is a JOIN, not a lookup — a match is a proven preimage.

Two things this file has to pin, because getting either wrong is silent:

  * **It must never guess.** An unmatched clip stays unmatched. Writing a plausible
    url would put a stranger's docid behind that clip's ⇢ and nothing would ever
    say so — the failure mode is a feature that quietly points at the wrong thing.
  * **It must never touch the network.** The whole reason LO approved this over the
    alternative is that it opens no socket. A regression that reintroduced a lookup
    would still pass a naive count assertion, so the socket is booby-trapped here.

    pytest tests/test_backfill_picks.py -q
"""
import hashlib
import json

import pytest
from django.core.management import call_command

import api.v1.game_review as gr
import api.v1.media_finder as mf
import api.v1.media_review as mr
import apps.game_generation.management.commands.backfill_picks as bp

TOML = """
schema_version = "1.0"

[project]
id = "fixture"
title = "Fixture"
starting_canvas = "c1"

[player]
id = "player"
name = "P"

[[locations]]
id = "loc"
name = "Room"

[[canvases]]
id = "c1"
name = "C1"

[canvases.trigger]
location = "loc"
is_active = true

[[canvases.nodes]]
id = "base"
name = "Base"
blocks = [
%s
]

[canvases.nodes.exit_block]
type = "location"
text = "Done."
"""

POOL = '  { type = "video", props = { pool_dir = "sex/a_t5", pool = 4, description = "d" } },'
SINGLE = '  { type = "video", props = { file = "sex/a_t5.webm", description = "d" } },'


def stem(url):
    return "c" + hashlib.md5(url.encode()).hexdigest()[:10]


@pytest.fixture
def game(tmp_path, monkeypatch):
    """A fixture game the test controls: TOML, ledger, and files on disk."""
    for module in (bp, mf, mr, gr):
        monkeypatch.setattr(module, "GAMES_ROOT", tmp_path, raising=False)
    root = tmp_path / "g"
    (root / "toml_phases").mkdir(parents=True)
    (root / ".find-media").mkdir(parents=True)
    (root / "videos").mkdir(parents=True)

    def write(blocks_toml, shelf=None, picks=None, pool_files=(), single_file=None):
        (root / "toml_phases" / "7_final_game.toml").write_text(TOML % blocks_toml)
        blob = {"game": "g", "options": shelf or {}}
        if picks is not None:
            blob["picks"] = picks
        (root / ".find-media" / "media_options.json").write_text(json.dumps(blob))
        if pool_files:
            pool = root / "videos" / "sex" / "a_t5"
            pool.mkdir(parents=True, exist_ok=True)
            for name in pool_files:
                (pool / name).write_bytes(b"\x00" * 2000)
        if single_file:
            (root / "videos" / "sex").mkdir(parents=True, exist_ok=True)
            (root / "videos" / "sex" / single_file).write_bytes(b"\x00" * 2000)
        return root

    return write


def _run(capsys, write=False):
    call_command("backfill_picks", game="g", write=write)
    return capsys.readouterr().out


def _picks(root, slot):
    blob = json.loads((root / ".find-media" / "media_options.json").read_text())
    return blob.get("picks", {}).get(slot) or []


def _options(root, slot):
    blob = json.loads((root / ".find-media" / "media_options.json").read_text())
    return blob.get("options", {}).get(slot) or []


URL = "https://x.test/kneeling.gif"


# ── the join ─────────────────────────────────────────────────────────────────


def test_a_pool_member_is_recovered_from_a_url_on_its_own_shelf(game, capsys):
    root = game(
        POOL,
        shelf={
            "sex/a_t5": [
                {"url": URL, "docid": "FvF5n0MlBjcrfM", "found_by": ["kneeling gif"]}
            ]
        },
        pool_files=[stem(URL) + ".gif"],
    )
    _run(capsys, write=True)
    picks = _picks(root, "sex/a_t5")
    assert len(picks) == 1
    assert picks[0]["url"] == URL
    assert picks[0]["docid"] == "FvF5n0MlBjcrfM"
    assert picks[0]["found_by"] == ["kneeling gif"]
    # Marked, because its found_by is the shelf's labels TODAY — searches that ran
    # after the install are in there too. True enough to seed a ⇢, not a record.
    assert picks[0]["recovered"] is True


def test_a_pool_member_is_recovered_from_ANOTHER_slots_shelf(game, capsys):
    """The cross-slot join is not a nicety. Measured on vesper: of the 101 clips
    whose url still exists anywhere, only 15 are on their own shelf."""
    root = game(
        POOL,
        shelf={"somewhere/else_t5": [{"url": URL, "docid": "FvF5n0MlBjcrfM"}]},
        pool_files=[stem(URL) + ".gif"],
    )
    _run(capsys, write=True)
    assert _picks(root, "sex/a_t5")[0]["url"] == URL


def test_a_row_carrying_an_id_wins_over_one_that_does_not(game, capsys):
    """The same url can sit on several shelves with only one enriched by a harvest
    that captured ids. Recovering the bare copy would recover a dead ⇢."""
    root = game(
        POOL,
        shelf={
            "a/1": [{"url": URL}],
            "b/2": [{"url": URL, "docid": "FvF5n0MlBjcrfM"}],
        },
        pool_files=[stem(URL) + ".gif"],
    )
    _run(capsys, write=True)
    assert _picks(root, "sex/a_t5")[0]["docid"] == "FvF5n0MlBjcrfM"


# ── what it refuses to do ────────────────────────────────────────────────────


def test_an_unmatched_pool_member_is_counted_and_left_alone(game, capsys):
    root = game(POOL, shelf={}, pool_files=[stem(URL) + ".gif"])
    out = _run(capsys, write=True)
    assert _picks(root, "sex/a_t5") == []
    assert "1 unmatched" in out


def test_a_hand_dropped_filename_is_never_matched(game, capsys):
    """No hash in the name means no proof. `clip1.gif` could be anything."""
    root = game(
        POOL,
        shelf={"sex/a_t5": [{"url": URL, "docid": "FvF5n0MlBjcrfM"}]},
        pool_files=["clip1.gif"],
    )
    _run(capsys, write=True)
    assert _picks(root, "sex/a_t5") == []


def test_a_single_slot_install_recovers_nothing(game, capsys):
    """grab names a single slot's file after the SLOT, so no join key was ever
    written and none can be derived. Reported, never guessed."""
    root = game(
        SINGLE,
        shelf={"sex/a_t5.webm": [{"url": URL, "docid": "FvF5n0MlBjcrfM"}]},
        single_file="a_t5.webm",
    )
    out = _run(capsys, write=True)
    assert _picks(root, "sex/a_t5.webm") == []
    assert "1 single-slot" in out


def test_an_existing_pick_is_never_overwritten(game, capsys):
    """A first-hand record beats a recovered one — its found_by is the search that
    really introduced the clip, not whatever the shelf says months later."""
    first_hand = {
        "filename": stem(URL) + ".gif",
        "url": URL,
        "found_by": ["the real one"],
    }
    root = game(
        POOL,
        shelf={
            "sex/a_t5": [{"url": URL, "docid": "FvF5n0MlBjcrfM", "found_by": ["later"]}]
        },
        picks={"sex/a_t5": [first_hand]},
        pool_files=[stem(URL) + ".gif"],
    )
    _run(capsys, write=True)
    picks = _picks(root, "sex/a_t5")
    assert len(picks) == 1
    assert picks[0]["found_by"] == ["the real one"]
    assert "recovered" not in picks[0]


# ── demoted options ──────────────────────────────────────────────────────────


def test_a_demoted_pool_clip_gets_its_source_url_back(game, capsys):
    """`pool_unselect` keeps the md5 stem when it moves the file aside, so the same
    join repairs the shelf tile — 276 of these were born dead on vesper."""
    local = f"g/.find-media/previous/{stem(URL)}-20260809-120000.gif"
    root = game(
        POOL,
        shelf={
            "sex/a_t5": [
                {"url": URL, "docid": "FvF5n0MlBjcrfM"},
                {"url": "/games/" + local, "local_path": local, "origin": "previous"},
            ]
        },
    )
    _run(capsys, write=True)
    demoted = [o for o in _options(root, "sex/a_t5") if o.get("origin") == "previous"][
        0
    ]
    assert demoted["source_url"] == URL
    assert demoted["docid"] == "FvF5n0MlBjcrfM"
    # Its own url is untouched: a re-select must install by COPY from the local
    # bytes, not re-download whatever the host serves today.
    assert demoted["url"] == "/games/" + local


def test_a_demoted_single_slot_clip_is_left_alone(game, capsys):
    """Named after the slot, stamped — no hash anywhere in it."""
    local = "g/.find-media/previous/a_t5-20260809-120000.gif"
    root = game(
        SINGLE,
        shelf={
            "sex/a_t5.webm": [
                {"url": URL, "docid": "FvF5n0MlBjcrfM"},
                {"url": "/games/" + local, "local_path": local, "origin": "previous"},
            ]
        },
    )
    _run(capsys, write=True)
    demoted = [
        o for o in _options(root, "sex/a_t5.webm") if o.get("origin") == "previous"
    ][0]
    assert "source_url" not in demoted


# ── the two guarantees ───────────────────────────────────────────────────────


def test_a_dry_run_writes_nothing(game, capsys):
    root = game(
        POOL,
        shelf={"sex/a_t5": [{"url": URL, "docid": "FvF5n0MlBjcrfM"}]},
        pool_files=[stem(URL) + ".gif"],
    )
    before = (root / ".find-media" / "media_options.json").read_bytes()
    out = _run(capsys)
    assert (root / ".find-media" / "media_options.json").read_bytes() == before
    assert not (root / ".find-media" / "media_options.json.bak").exists()
    assert "1 pick(s) recovered" in out and "dry run" in out


def test_a_write_backs_the_ledger_up_first(game, capsys):
    root = game(
        POOL,
        shelf={"sex/a_t5": [{"url": URL, "docid": "FvF5n0MlBjcrfM"}]},
        pool_files=[stem(URL) + ".gif"],
    )
    before = (root / ".find-media" / "media_options.json").read_bytes()
    _run(capsys, write=True)
    assert (root / ".find-media" / "media_options.json.bak").read_bytes() == before


def test_it_never_opens_a_socket(game, capsys, monkeypatch):
    """The load-bearing claim of the whole command. A count assertion would still
    pass if a lookup crept back in; this will not."""
    import socket

    def boom(*a, **k):
        raise AssertionError("backfill_picks opened a socket")

    monkeypatch.setattr(socket.socket, "connect", boom)
    monkeypatch.setattr(socket, "create_connection", boom)
    game(
        POOL,
        shelf={"sex/a_t5": [{"url": URL, "docid": "FvF5n0MlBjcrfM"}]},
        pool_files=[stem(URL) + ".gif"],
    )
    assert "1 pick(s) recovered" in _run(capsys, write=True)
