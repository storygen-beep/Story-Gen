"""`slot_key` — a media slot's STABLE identity, separate from its file path.

A shelf (stocked options) and a verdict (approve/disapprove) are filed under a
string. Filing them under the declared PATH means every edit that moves the path
orphans both — converting to a pool drops the extension, a tier retag rewrites it.
Measured live: 148 options stranded on the first pool conversion.

`slot_key` is that string, and it prefers an authored block `id`:

    authored `id`  ->  else `pool_dir`  ->  else `file`

Two properties are load-bearing and both are asserted here:

  1. **Opt-in.** ~560 media blocks exist repo-wide; almost none will ever carry an
     `id`. Everything must behave byte-identically without one, or this change is a
     migration instead of a feature.
  2. **`file` and `slot_key` are DIFFERENT JOBS.** `file` decides where the bytes
     go; `slot_key` decides which shelf is touched. Conflating them writes a slot's
     media to the wrong path — the one way this change can corrupt a game.

    pytest tests/test_slot_key.py -q
"""
import json
from pathlib import Path
from unittest.mock import patch

import pytest
from django.test import RequestFactory

import api.v1.media_finder as mf
from apps.common.media_blocks import block_slot_key


# ── the key itself ───────────────────────────────────────────────────────────

def test_authored_id_wins():
    block = {"type": "video", "id": "renner_oral",
             "props": {"file": "sex/renner_oral_t5.webm"}}
    assert block_slot_key(block) == "renner_oral"


def test_falls_back_to_pool_dir_then_file():
    assert block_slot_key({"type": "video", "props": {"pool_dir": "sex/a_t5", "pool": 4}}) == "sex/a_t5"
    assert block_slot_key({"type": "video", "props": {"file": "sex/a_t5.webm"}}) == "sex/a_t5.webm"
    assert block_slot_key({"type": "video", "props": {}}) == ""
    assert block_slot_key(None) == ""


def test_authored_id_survives_the_path_moving():
    """The whole point: same beat, three different paths, one stable key."""
    keys = {
        block_slot_key({"id": "x", "props": {"file": "sex/a_t4.webm"}}),   # before retag
        block_slot_key({"id": "x", "props": {"file": "sex/a_t5.webm"}}),   # after retag
        block_slot_key({"id": "x", "props": {"pool_dir": "sex/a_t5"}}),    # after pooling
    }
    assert keys == {"x"}


@pytest.mark.parametrize("positional", ["b0", "b3", "b0.b2", "b1.beat0.b2", "b12.b7"])
def test_positional_fallback_ids_are_refused(positional):
    """⚠️ The importer assigns every block a POSITIONAL id when the TOML has none
    (`str(b.get("id") or _bid)`). It shifts when a block is inserted above it, so
    keying a shelf on it would re-key on an unrelated edit — strictly WORSE than
    keying on the path. Raw TOML blocks never carry one, but the normalized dict
    does, and a caller will eventually pass one in."""
    block = {"id": positional, "props": {"file": "sex/a_t5.webm"}}
    assert block_slot_key(block) == "sex/a_t5.webm"


@pytest.mark.parametrize("ok", ["beat3", "b3x", "brothel", "b_3", "oral_b3"])
def test_real_ids_that_merely_look_positional_are_kept(ok):
    assert block_slot_key({"id": ok, "props": {"file": "a.webm"}}) == ok


# ── the enumerator emits it ──────────────────────────────────────────────────

def _extract(tmp_path, monkeypatch, blocks):
    import api.v1.game_review as gr
    monkeypatch.setattr(gr, "GAMES_ROOT", tmp_path)
    (tmp_path / "g").mkdir(exist_ok=True)
    data = {"canvases": [{"id": "c1", "name": "C1", "nodes": [{"id": "n", "blocks": blocks}]}]}
    res = gr._extract_missing_media(data, "g")
    return res["found"] + res["missing"]


def test_enumerator_emits_slot_key_from_an_authored_id(tmp_path, monkeypatch):
    rows = _extract(tmp_path, monkeypatch, [
        {"type": "video", "id": "renner_oral", "props": {"file": "sex/a_t5.webm"}},
    ])
    assert rows[0]["file"] == "sex/a_t5.webm"
    assert rows[0]["slot_key"] == "renner_oral"


def test_enumerator_defaults_slot_key_to_the_path(tmp_path, monkeypatch):
    """The back-compat guarantee — ~560 untagged blocks rely on it."""
    rows = _extract(tmp_path, monkeypatch, [
        {"type": "video", "props": {"file": "sex/a_t5.webm"}},
    ])
    assert rows[0]["slot_key"] == rows[0]["file"] == "sex/a_t5.webm"


def test_a_legacy_files_pool_keys_each_entry_by_its_own_path(tmp_path, monkeypatch):
    """`files = [...]` declares N separate slots, so one block id cannot key them
    all — they would collapse onto a single shelf."""
    rows = _extract(tmp_path, monkeypatch, [
        {"type": "video", "id": "x", "props": {"files": ["a.webm", "b.webm"]}},
    ])
    assert [r["slot_key"] for r in rows] == ["a.webm", "b.webm"]


def test_non_canvas_categories_still_get_a_slot_key(tmp_path, monkeypatch):
    """Locations/clothing/phone/portraits have no block to tag; their key is the
    path. Defaulted in one place so a new category can't ship without one."""
    import api.v1.game_review as gr
    monkeypatch.setattr(gr, "GAMES_ROOT", tmp_path)
    (tmp_path / "g").mkdir(exist_ok=True)
    res = gr._extract_missing_media({"locations": [{"id": "l", "image": "loc/room.jpg"}]}, "g")
    rows = res["found"] + res["missing"]
    assert rows and all(r["slot_key"] == r["file"] for r in rows)


# ── the API: default is byte-identical, and grab splits its two jobs ──────────

@pytest.fixture
def games_root(tmp_path, monkeypatch):
    monkeypatch.setattr(mf, "GAMES_ROOT", tmp_path)
    (tmp_path / "g" / "videos").mkdir(parents=True)
    return tmp_path


def _post(view, payload):
    req = RequestFactory().post("/", data=json.dumps(payload), content_type="application/json")
    return view(req)


def test_options_add_without_slot_key_keys_on_file(games_root):
    _post(mf.options_add, {"game": "g", "file": "sex/a_t5.webm", "url": "https://x.test/a.gif", "media_kind": "img"})
    assert "sex/a_t5.webm" in mf._read_options(games_root / "g")["options"]


def test_options_add_with_slot_key_keys_on_it(games_root):
    _post(mf.options_add, {"game": "g", "file": "sex/a_t5.webm", "slot_key": "renner_oral",
                           "url": "https://x.test/a.gif", "media_kind": "img"})
    opts = mf._read_options(games_root / "g")["options"]
    assert "renner_oral" in opts and "sex/a_t5.webm" not in opts


def test_grab_writes_to_the_PATH_and_drops_from_the_KEY_shelf(games_root):
    """⚠️ THE one that matters. `file` decides where the bytes go; `slot_key`
    decides which shelf. Swap them and a slot tagged `renner_oral` writes its media
    to videos/renner_oral.gif — the game then renders a hole and the real file is
    orphaned on disk."""
    _post(mf.options_add, {"game": "g", "file": "sex/a_t5.webm", "slot_key": "renner_oral",
                           "url": "https://x.test/c.webm", "media_kind": "video"})

    def fake_download(u, dest, extra_headers=None):
        Path(dest).write_bytes(b"\x00" * 60000)
        return True, None

    with patch.object(mf, "download_direct", side_effect=fake_download):
        res = _post(mf.grab, {"game": "g", "file": "sex/a_t5.webm", "slot_key": "renner_oral",
                              "url": "https://x.test/c.webm"})
    body = json.loads(res.content)
    assert body["success"], body

    # bytes -> the PATH
    assert body["file_path"].startswith("g/videos/sex/a_t5"), body["file_path"]
    assert not (games_root / "g" / "videos" / "renner_oral.webm").exists()
    # shelf -> the KEY (the consumed option was dropped from it)
    assert mf._read_options(games_root / "g")["options"].get("renner_oral") == []


def test_grab_without_slot_key_is_unchanged(games_root):
    def fake_download(u, dest, extra_headers=None):
        Path(dest).write_bytes(b"\x00" * 60000)
        return True, None

    with patch.object(mf, "download_direct", side_effect=fake_download):
        res = _post(mf.grab, {"game": "g", "file": "sex/a_t5.webm", "url": "https://x.test/c.webm"})
    assert json.loads(res.content)["file_path"].startswith("g/videos/sex/a_t5")
