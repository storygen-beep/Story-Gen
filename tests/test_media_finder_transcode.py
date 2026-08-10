"""Auto-compress on install — `grab` squeezes a clip between download and install.

A harvested clip arrives in whatever the host served, usually GIF, which costs ~10x
what H.264 does for the same seconds. Compressing at install is what stops the shelf
re-inflating one pick at a time (measured on vesper: 1546 MB of GIF became 160 MB).

What is load-bearing here, in order:

  1. FAILURE MUST NOT LOSE THE CLIP. Every transcode failure — missing ffmpeg, a
     codec ffmpeg won't take, a timeout, an encode that comes out bigger — has to
     fall back to installing the original bytes. Compression is an optimisation;
     dropping a clip the human just chose would be a far worse bug than a fat file.
  2. The installed PATH must follow the new extension. `output_path` is computed
     from the source url before the transcode runs, so a hook that forgets to
     recompute it writes mp4 bytes to a `.gif` name — which the engine then renders
     through <img>, i.e. as nothing at all.
  3. `.mp4` sources are NOT re-encoded. H.264 -> H.264 loses a generation every time,
     and the "keep it if smaller" rule would accept that loss on every refetch.
  4. Stills are never touched. package_from_toml already downscales them.

    pytest tests/test_media_finder_transcode.py -q
"""
import json
from pathlib import Path
from unittest.mock import patch

import pytest
from django.test import RequestFactory

import api.v1.media_finder as mf

# ── fixtures ────────────────────────────────────────────────────────────────


@pytest.fixture
def game(tmp_path, monkeypatch):
    """A minimal games/<slug>/ tree with media_finder pointed at it."""
    root = tmp_path / "games"
    (root / "vesper" / "videos" / "scenes").mkdir(parents=True)
    (root / "vesper" / ".find-media").mkdir(parents=True)
    monkeypatch.setattr(mf, "GAMES_ROOT", root)
    return root / "vesper"


def _post(body):
    req = RequestFactory().post(
        "/api/v1/dev/media-finder/grab",
        data=json.dumps(body),
        content_type="application/json",
    )
    return json.loads(mf.grab(req).content)


def _fake_download(payload=b"ORIGINAL-BYTES"):
    """Stand in for download_direct: writes bytes to the staging path it is given."""

    def _dl(url, dest, extra_headers=None):
        Path(dest).write_bytes(payload)
        return True, None

    return _dl


# ── 1. the happy path ───────────────────────────────────────────────────────


def test_gif_is_installed_as_mp4(game):
    """A .gif url lands as .mp4, and the reported path carries the new extension."""

    def _fake_transcode(src, dst):
        Path(dst).write_bytes(b"MP4")  # smaller than the original
        return ""  # success

    with patch.object(mf, "download_direct", _fake_download()), patch.object(
        mf, "_transcode_to_mp4", _fake_transcode
    ):
        res = _post(
            {
                "game": "vesper",
                "file": "scenes/beat.webm",
                "url": "https://example.com/clip.gif",
            }
        )

    assert res["success"] is True
    assert res["transcoded"] is True
    assert res["file_path"].endswith("scenes/beat.mp4"), res["file_path"]
    assert (game / "videos" / "scenes" / "beat.mp4").read_bytes() == b"MP4"
    # the original extension must NOT survive beside it
    assert not (game / "videos" / "scenes" / "beat.gif").exists()


# ── 2. every failure falls back to the original ─────────────────────────────


@pytest.mark.parametrize(
    "reason",
    [
        "ffmpeg not found",
        "ffmpeg failed: Invalid data found when processing input",
        "transcode exceeded 300s",
        "not smaller than the original",
        "frame loss 240 -> 61",
    ],
)
def test_transcode_failure_installs_the_original(game, reason):
    """The clip always lands. A failed squeeze costs bytes, never the pick."""
    with patch.object(mf, "download_direct", _fake_download(b"ORIGINAL")), patch.object(
        mf, "_transcode_to_mp4", lambda s, d: reason
    ):
        res = _post(
            {
                "game": "vesper",
                "file": "scenes/beat.webm",
                "url": "https://example.com/clip.gif",
            }
        )

    assert res["success"] is True
    assert res["transcoded"] is False
    assert res["transcode_skipped"] == reason
    assert res["file_path"].endswith("scenes/beat.gif"), res["file_path"]
    assert (game / "videos" / "scenes" / "beat.gif").read_bytes() == b"ORIGINAL"


def test_no_staging_file_is_left_behind_on_fallback(game):
    """A failed transcode must not leak its half-written mp4 into .find-media/incoming."""

    def _half_written(src, dst):
        Path(dst).write_bytes(b"PARTIAL")
        return "ffmpeg failed: truncated"

    with patch.object(mf, "download_direct", _fake_download()), patch.object(
        mf, "_transcode_to_mp4", _half_written
    ):
        _post(
            {
                "game": "vesper",
                "file": "scenes/beat.webm",
                "url": "https://example.com/clip.gif",
            }
        )

    leftovers = list((game / ".find-media" / "incoming").glob("*"))
    assert leftovers == [], leftovers


# ── 3. what must NOT be transcoded ──────────────────────────────────────────


def test_mp4_source_is_not_re_encoded(game):
    """H.264 -> H.264 loses a generation for no win worth having."""
    called = []
    with patch.object(mf, "download_direct", _fake_download()), patch.object(
        mf, "_transcode_to_mp4", lambda s, d: called.append(1) or ""
    ):
        res = _post(
            {
                "game": "vesper",
                "file": "scenes/beat.webm",
                "url": "https://example.com/clip.mp4",
            }
        )

    assert called == [], "an .mp4 source was sent through the encoder"
    assert res["transcoded"] is False
    assert res["file_path"].endswith("scenes/beat.mp4")


def test_still_image_is_not_transcoded(game):
    """The packager already downscales stills; ffmpeg must never see them."""
    called = []
    with patch.object(mf, "download_direct", _fake_download()), patch.object(
        mf, "_transcode_to_mp4", lambda s, d: called.append(1) or ""
    ):
        res = _post(
            {
                "game": "vesper",
                "file": "scenes/still.jpg",
                "url": "https://example.com/photo.jpg",
            }
        )

    assert called == []
    assert res["transcoded"] is False
    assert res["file_path"].endswith("scenes/still.jpg")


# ── 4. pools ────────────────────────────────────────────────────────────────


def test_pool_member_lands_as_mp4_without_disturbing_peers(game):
    """A pool install ADDS. The transcode must not turn that into a replace."""
    pool = game / "videos" / "sex" / "loop_t5"
    pool.mkdir(parents=True)
    (pool / "cPEER.mp4").write_bytes(b"PEER")

    def _fake_transcode(src, dst):
        Path(dst).write_bytes(b"NEW")
        return ""

    with patch.object(mf, "download_direct", _fake_download()), patch.object(
        mf, "_transcode_to_mp4", _fake_transcode
    ):
        res = _post(
            {
                "game": "vesper",
                "file": "sex/loop_t5",
                "pool_dir": "sex/loop_t5",
                "url": "https://example.com/clip.gif",
            }
        )

    assert res["success"] is True and res["transcoded"] is True
    assert (pool / "cPEER.mp4").read_bytes() == b"PEER", "a peer was destroyed"
    assert res["file_path"].endswith(".mp4")
    assert len(list(pool.glob("*.mp4"))) == 2


# ── 5. the guard rails inside _transcode_to_mp4 itself ──────────────────────


def test_transcode_reports_missing_ffmpeg_rather_than_raising():
    with patch.object(mf, "find_ffmpeg", lambda: None):
        assert (
            mf._transcode_to_mp4(Path("/nope.gif"), Path("/nope.mp4"))
            == "ffmpeg not found"
        )


def test_mp4_is_absent_from_the_transcode_source_set():
    """Guards the rule directly, so a future edit to the set trips a test."""
    assert "mp4" not in mf._TRANSCODE_SOURCES
    assert "gif" in mf._TRANSCODE_SOURCES
    assert "webm" in mf._TRANSCODE_SOURCES
    assert not {"jpg", "jpeg", "png", "webp"} & mf._TRANSCODE_SOURCES
