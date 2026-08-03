"""Media pools that CYCLE — `files = [...]` on image and video blocks.

A repeatable beat (an activity, an ambient, a brothel loop) is what a player sees
most, and one fixed clip per beat goes stale fast. A pool holds N clips for one
slot and shows them in order: visit 1 -> clip 1, visit 2 -> clip 2, wrapping round.

Two properties are load-bearing and both are asserted here:

  1. It CYCLES. `either()`/`random()` over four clips repeats back-to-back 25% of
     the time, which is the staleness a pool exists to remove. The counter must
     therefore persist in $game_state, not in a `_temp` that dies with the render.
  2. The tag is chosen PER ENTRY. `_find_media_file` is extension-agnostic, so a
     pool asking for .webm can legitimately resolve to a .gif on disk — and
     `<video src="x.gif">` renders nothing. This is why the old image-pool
     `@src="_img"` single-tag approach could not be reused for clips.

⚠️ These target **v2 explicitly**. The five pre-existing image-pool tests in
apps/projects/tests.py instantiate TweeComprehensiveGeneratorV1 — the deprecated
generator — so v2's copy of the pool code had ZERO coverage and could be broken
outright while every one of them stayed green.

Run with an explicit path — pyproject sets testpaths = ["tests"], so app suites are
not collected by a bare `pytest`:

    pytest apps/game_generation/tests/test_media_pool_cycle.py -q
"""
import re
from unittest.mock import patch

import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)


def _gen(on_disk=(), debug=False, video_path="./videos"):
    """A generator primed with a fake media folder — no DB, no disk, no Tweego.

    `on_disk` are the media paths that "exist"; `_find_media_file` matches them
    extension-agnostically, exactly as it does against a real folder scan.
    """
    g = TweeComprehensiveGeneratorV2()
    g.video_files = {p: f"/fake/{p}" for p in on_disk}
    g.video_path = video_path
    g.debug = debug
    g.current_canvas_id = "canvas_probe"
    g.options = {"game_folder": "probe"}
    return g


def _video_pool(files, **props):
    return {"type": "video", "props": {"files": list(files), **props}}


def _image_pool(files, **props):
    return {"type": "image", "props": {"files": list(files), **props}}


TRIO = ["sex/loop_a.webm", "sex/loop_b.webm", "sex/loop_c.webm"]


# ── 1. it cycles, and the counter survives the render ────────────────────────

def test_video_pool_cycles_and_never_picks_at_random():
    """The whole point. A random pick would show the same clip twice in a row."""
    g = _gen(TRIO)
    out = g._convert_blocks_to_game_html([_video_pool(TRIO)])

    assert "<<if _mc is 0>>" in out
    assert "<<elseif _mc is 1>>" in out
    assert "<<else>>" in out and "<</if>>" in out
    # The two mechanisms this feature exists to replace.
    assert "random(" not in out
    assert "either(" not in out


def test_counter_lives_in_game_state_not_in_a_temp_variable():
    """A `_temp` dies with the render, so the cycle would restart every visit and
    the player would see clip 1 forever — a fixed clip wearing a pool's clothes."""
    g = _gen(TRIO)
    out = g._convert_blocks_to_game_html([_video_pool(TRIO)])

    assert "$game_state.media_cycle[" in out
    # `_mc` is only the read-back of the persisted value, set immediately before use.
    assert re.search(r'<<set _mc to \$game_state\.media_cycle\["[^"]+"\]>>', out)


def test_counter_is_ndef_guarded_so_old_saves_do_not_break():
    """setup.backfillStateDefaults only backfills flags / player.core_traits /
    npcs, so a NEW $game_state sub-map is `undefined` in every save written before
    this build. Without this guard, loading an existing save hits the pool and
    throws. Same class as the vesper 0.1.5 cover incident."""
    g = _gen(TRIO)
    out = g._convert_blocks_to_game_html([_video_pool(TRIO)])

    assert "<<if ndef $game_state.media_cycle>><<set $game_state.media_cycle to {}>><</if>>" in out


def test_counter_wraps_modulo_the_pool_size():
    """4 clips must wrap 3 -> 0, not run off the end into an empty branch."""
    quad = TRIO + ["sex/loop_d.webm"]
    g = _gen(quad)
    out = g._convert_blocks_to_game_html([_video_pool(quad)])

    assert "% 4)" in out
    assert "<<elseif _mc is 2>>" in out


def test_first_visit_starts_at_clip_zero():
    """An unset counter must resolve to 0, not to NaN (undefined + 1)."""
    g = _gen(TRIO)
    out = g._convert_blocks_to_game_html([_video_pool(TRIO)])

    assert "=== undefined ? 0 :" in out


# ── 2. per-entry tag selection ───────────────────────────────────────────────

def test_mixed_webm_and_gif_each_get_the_correct_tag():
    """find-media installs both kinds into one slot and `_find_media_file` is
    extension-agnostic, so a pool WILL be mixed. `<video src="x.gif">` renders
    nothing — which is why one shared @src attribute-directive cannot serve a pool."""
    g = _gen(["sex/loop_a.webm", "sex/loop_b.gif"])
    out = g._convert_blocks_to_game_html([_video_pool(["sex/loop_a.webm", "sex/loop_b.gif"])])

    assert '<video src="./videos/sex/loop_a.webm"' in out
    assert '<img src="./videos/sex/loop_b.gif"' in out


def test_video_pool_resolves_extension_agnostically_like_the_singular_path():
    """TOML says .webm, disk holds .gif — the long-standing resolver behaviour."""
    g = _gen(["sex/loop_a.gif"])
    out = g._convert_blocks_to_game_html([_video_pool(["sex/loop_a.webm"])])

    assert '<img src="./videos/sex/loop_a.gif"' in out
    assert g.missing_media == []


def test_a_video_files_pool_no_longer_vanishes():
    """The documented trap this feature removes: a `files` list of clips used to
    resolve on disk, get dropped by the image-only filter, and render NOTHING —
    no error, nothing on the missing-media page."""
    g = _gen(TRIO)
    out = g._convert_blocks_to_game_html([_video_pool(TRIO)])

    for path in TRIO:
        assert path in out


# ── 3. degradation ───────────────────────────────────────────────────────────

def test_single_entry_pool_renders_bare_with_no_counter():
    """Nothing to cycle — don't burn a state key or emit a one-branch <<if>>."""
    g = _gen(["sex/only.webm"])
    out = g._convert_blocks_to_game_html([_video_pool(["sex/only.webm"])])

    assert '<video src="./videos/sex/only.webm"' in out
    assert "media_cycle" not in out
    assert "_mc" not in out


def test_partial_pool_cycles_over_the_survivors_only():
    """Slots get filled over time; a half-empty pool must still play."""
    g = _gen(["sex/loop_a.webm", "sex/loop_c.webm"])
    out = g._convert_blocks_to_game_html([_video_pool(TRIO)])

    assert "% 2)" in out
    assert "sex/loop_a.webm" in out and "sex/loop_c.webm" in out
    assert "sex/loop_b.webm" not in out
    assert [m["file"] for m in g.missing_media] == ["sex/loop_b.webm"]


def test_every_missing_pool_entry_gets_its_own_missing_media_row():
    """Four empty slots are four files to hunt, not one. If the pool collapsed to
    a single row, find-media would install one clip and call the slot done."""
    quad = TRIO + ["sex/loop_d.webm"]
    g = _gen()
    g._convert_blocks_to_game_html([_video_pool(quad, description="d", search_queries=["q"])])

    assert [m["file"] for m in g.missing_media] == quad
    assert all(m["type"] == "video" for m in g.missing_media)
    assert all(m["search_queries"] == ["q"] for m in g.missing_media)
    assert all(m["canvas_id"] == "canvas_probe" for m in g.missing_media)


def test_all_missing_pool_shows_a_placeholder_in_debug_builds():
    g = _gen(debug=True)
    out = g._convert_blocks_to_game_html([_video_pool(TRIO, description="a beat")])

    assert "[VIDEO POOL MISSING]" in out
    assert "(3 files)" in out
    assert "a beat" in out


def test_all_missing_pool_renders_nothing_in_a_normal_build():
    """A player must never see build scaffolding."""
    g = _gen(debug=False)
    out = g._convert_blocks_to_game_html([_video_pool(TRIO)])

    assert "POOL MISSING" not in out
    assert "<video" not in out and "<img" not in out


# ── 4. packaging + precedence ────────────────────────────────────────────────

def test_every_resolved_pool_file_is_tracked_for_packaging():
    """All N files must be copied into the build, not just the one showing first."""
    g = _gen(TRIO + ["sex/still.jpg"])
    g._convert_blocks_to_game_html([_video_pool(TRIO + ["sex/still.jpg"])])

    assert g.used_assets["external_videos"] == set(TRIO)
    assert g.used_assets["external_images"] == {"sex/still.jpg"}


def test_files_wins_over_file_when_both_are_present():
    g = _gen(TRIO + ["sex/single.webm"])
    out = g._convert_blocks_to_game_html([_video_pool(TRIO, file="sex/single.webm")])

    assert "sex/single.webm" not in out
    assert "sex/loop_a.webm" in out


@pytest.mark.parametrize("bad", [[], "notalist", [1, 2], None])
def test_malformed_files_falls_back_to_the_singular_path(bad):
    """A pool that isn't a non-empty list of strings must not swallow the block."""
    g = _gen(["sex/single.webm"])
    block = {"type": "video", "props": {"files": bad, "file": "sex/single.webm"}}
    out = g._convert_blocks_to_game_html([block])

    assert '<video src="./videos/sex/single.webm"' in out


# ── 5. pool identity ─────────────────────────────────────────────────────────

def test_two_different_pools_get_independent_counters():
    """Otherwise every pool in the game advances in lockstep."""
    other = ["sex/other_a.webm", "sex/other_b.webm"]
    g = _gen(TRIO + other)
    out = g._convert_blocks_to_game_html([_video_pool(TRIO), _video_pool(other)])

    keys = set(re.findall(r'\$game_state\.media_cycle\["([^"]+)"\]', out))
    assert len(keys) == 2


def test_pool_key_is_stable_across_rebuilds():
    """Derived from the declared TOML only — a rebuild must not reset the cycle."""
    g = _gen(TRIO)
    assert g._media_pool_key(TRIO) == g._media_pool_key(list(TRIO))
    assert g._media_pool_key(TRIO) != g._media_pool_key(TRIO[:2])


def test_pool_key_is_readable_enough_to_debug():
    """A bare hash in a save file is unusable when something goes wrong."""
    g = _gen(TRIO)
    assert g._media_pool_key(TRIO).startswith("loop_a_")


# ── 6. the image pool, which now shares the same machinery ───────────────────

def test_image_pool_also_cycles_instead_of_picking_at_random():
    stills = ["sex/still_1.jpg", "sex/still_2.jpg", "sex/still_3.jpg"]
    g = _gen(stills)
    out = g._convert_blocks_to_game_html([_image_pool(stills)])

    assert "<<if _mc is 0>>" in out
    assert "either(" not in out


def test_image_pool_no_longer_uses_the_unproven_at_src_directive():
    """No built game in the repo has ever emitted `<<set _img to either(`, so
    `@src="_img"` was never proven through Tweego into a real SugarCube build.
    The cycle chain uses literal src attributes instead — nothing to prove."""
    stills = ["sex/still_1.jpg", "sex/still_2.jpg"]
    g = _gen(stills)
    out = g._convert_blocks_to_game_html([_image_pool(stills)])

    assert "@src" not in out
    assert '<img src="./videos/sex/still_1.jpg"' in out


def test_image_pool_caption_renders_once_not_once_per_branch():
    stills = ["sex/still_1.jpg", "sex/still_2.jpg"]
    g = _gen(stills)
    out = g._convert_blocks_to_game_html([_image_pool(stills, caption="after")])

    assert out.count("<figcaption") == 1
    assert out.index("<figure") < out.index("<<if _mc is 0>>")


def test_image_pool_drops_a_clip_but_warns_about_it_now():
    """It used to `continue` in silence: not rendered, not recorded as missing,
    not copied — the file simply vanished from the build with no diagnostic.

    Asserts on the logger call rather than caplog: the `apps` logger is configured
    with propagate=False, so records never reach the root handler caplog installs.
    """
    g = _gen(["sex/still_1.jpg", "sex/clip.webm"])
    mod = "apps.game_generation.twee_comprehensive.generators.v2"
    with patch(f"{mod}.logger") as mock_logger:
        out = g._convert_blocks_to_game_html([_image_pool(["sex/still_1.jpg", "sex/clip.webm"])])

    assert "sex/clip.webm" not in out
    assert mock_logger.warning.called, "a dropped pool entry must not pass unnoticed"
    emitted = " ".join(str(a) for a in mock_logger.warning.call_args.args)
    assert "sex/clip.webm" in emitted


def test_video_pool_accepts_stills_where_the_image_pool_refuses_clips():
    """Asymmetric on purpose: the video handler has always rendered a .gif through
    <img>, so a video pool needs no format filter at all."""
    mixed = ["sex/a.webm", "sex/b.jpg"]
    g = _gen(mixed)
    out = g._convert_blocks_to_game_html([_video_pool(mixed)])

    assert "sex/a.webm" in out and "sex/b.jpg" in out


# ── 6b. folder pools (`pool_dir`) — the preferred shape ──────────────────────
#
# The author names a FOLDER; its contents are discovered from disk. The count is
# never hardcoded, so the human curates by adding/removing files in the review UI
# instead of editing TOML. `pool = N` is a TARGET for find-media, not a manifest —
# the folder is the truth.

POOL_DIR = "sex/brothel_oral_t5"
POOL_FILES = [f"{POOL_DIR}/1.webm", f"{POOL_DIR}/2.webm", f"{POOL_DIR}/3.webm"]


def _dir_pool(dir_=POOL_DIR, target=4, **props):
    return {"type": "video", "props": {"pool_dir": dir_, "pool": target, **props}}


def test_pool_dir_discovers_folder_contents_and_cycles():
    g = _gen(POOL_FILES)
    out = g._convert_blocks_to_game_html([_dir_pool()])

    assert "<<if _mc is 0>>" in out
    assert "% 3)" in out, "cycle length comes from the folder, not from `pool`"
    for path in POOL_FILES:
        assert path in out


def test_pool_dir_matches_on_a_path_boundary_only():
    """`sex/oral_t5` must not swallow `sex/oral_t5_alt/` — a prefix match without
    the separator silently merges two unrelated pools."""
    g = _gen(POOL_FILES + ["sex/brothel_oral_t5_alt/1.webm"])
    out = g._convert_blocks_to_game_html([_dir_pool()])

    assert "% 3)" in out
    assert "_alt" not in out


def test_pool_dir_orders_naturally_not_lexically():
    """Lexical sort puts _10 before _2 and silently reorders the rotation."""
    many = [f"{POOL_DIR}/clip_{i}.webm" for i in (1, 2, 10)]
    g = _gen(many)
    out = g._convert_blocks_to_game_html([_dir_pool()])

    assert out.index("clip_1.webm") < out.index("clip_2.webm") < out.index("clip_10.webm")


def test_pool_dir_key_is_the_folder_so_curating_never_resets_the_player():
    """The load-bearing one. Contents change every time the human selects or
    unselects a clip; keying the counter on them would reset $game_state.media_cycle
    and snap every player back to clip 1."""
    g = _gen(POOL_FILES)
    two = _gen(POOL_FILES[:2])

    key_a = re.findall(r'media_cycle\["([^"]+)"\]', g._convert_blocks_to_game_html([_dir_pool()]))[0]
    key_b = re.findall(r'media_cycle\["([^"]+)"\]', two._convert_blocks_to_game_html([_dir_pool()]))[0]

    assert key_a == key_b
    assert "brothel_oral_t5" in key_a, "the key should stay readable for debugging"


def test_empty_pool_dir_still_reports_as_missing():
    """An unstocked pool must NEVER silently vanish from the missing list — that is
    the exact regression apps/common/media_blocks.py was written to stop."""
    g = _gen()
    out = g._convert_blocks_to_game_html([_dir_pool(search_queries=["q"])])

    assert out == "" or "<video" not in out
    assert [m["file"] for m in g.missing_media] == [POOL_DIR]
    assert g.missing_media[0]["search_queries"] == ["q"]


def test_empty_pool_dir_placeholder_names_the_folder_and_the_target():
    g = _gen(debug=True)
    out = g._convert_blocks_to_game_html([_dir_pool(target=4)])

    assert "[VIDEO POOL MISSING]" in out
    assert "sex/brothel_oral_t5/ (0 of 4)" in out


def test_partial_pool_dir_cycles_what_is_there_and_is_not_missing():
    """2 of a target 4 still renders. The shortfall is the audit's job, not a hole."""
    g = _gen(POOL_FILES[:2])
    out = g._convert_blocks_to_game_html([_dir_pool(target=4)])

    assert "% 2)" in out
    assert g.missing_media == []


def test_single_file_pool_dir_renders_bare():
    g = _gen(POOL_FILES[:1])
    out = g._convert_blocks_to_game_html([_dir_pool()])

    assert "media_cycle" not in out
    assert f'<video src="./videos/{POOL_DIR}/1.webm"' in out


def test_pool_dir_wins_over_files_and_file():
    """Precedence is declared once in apps/common/media_blocks.py; the generator
    must not disagree with it."""
    g = _gen(POOL_FILES + ["sex/legacy.webm", "sex/single.webm"])
    block = {"type": "video", "props": {
        "pool_dir": POOL_DIR, "files": ["sex/legacy.webm"], "file": "sex/single.webm",
    }}
    out = g._convert_blocks_to_game_html([block])

    assert "sex/legacy.webm" not in out
    assert "sex/single.webm" not in out
    assert f"{POOL_DIR}/1.webm" in out


def test_image_block_also_takes_a_pool_dir():
    stills = [f"{POOL_DIR}/a.jpg", f"{POOL_DIR}/b.jpg"]
    g = _gen(stills)
    out = g._convert_blocks_to_game_html([{"type": "image", "props": {"pool_dir": POOL_DIR}}])

    assert "<<if _mc is 0>>" in out
    assert '<img src="./videos/' in out


# ── 7. the block-dispatch trap ───────────────────────────────────────────────

def test_pool_does_not_swallow_the_block_that_follows_it():
    """`i += 1` runs BEFORE the type dispatch, so a handler that increments again
    silently eats the next block. Cheap to get wrong, invisible in the output."""
    g = _gen(TRIO)
    blocks = [
        _video_pool(TRIO),
        {"type": "paragraph", "content": "after the pool"},
    ]
    out = g._convert_blocks_to_game_html(blocks)

    assert "after the pool" in out


# ── 8. the media index that decides what SHIPS ───────────────────────────────

def test_load_media_files_ignores_dot_prefixed_files(tmp_path):
    """A dot-prefixed file must never enter the index the build plays from.

    `_load_media_files` scans with rglob('*'), which DOES return dotfiles, and it
    filters on suffix alone. `_resolve_pool_dir` then prefix-matches that index to
    decide what the shipped game cycles — so find-media's staging file, an editor
    swap file, or a macOS AppleDouble (`._clip.webm`, a real media suffix) would ship
    a partial clip to a player.

    Every other test in this file injects `video_files` directly and never touches
    disk, so this blind spot had no coverage at all.
    """
    pool = tmp_path / "sex" / "oral_t5"
    pool.mkdir(parents=True)
    for name in ("clip_1.webm", "clip_2.webm", ".incoming-c1.webm", "._clip_1.webm"):
        (pool / name).write_bytes(b"x")

    g = TweeComprehensiveGeneratorV2()
    g.video_files = {}
    g.video_folder = str(tmp_path)
    g._load_media_files()

    assert sorted(g.video_files) == ["sex/oral_t5/clip_1.webm", "sex/oral_t5/clip_2.webm"]
    # The path that actually reaches the player.
    assert g._resolve_pool_dir("sex/oral_t5") == [
        "sex/oral_t5/clip_1.webm", "sex/oral_t5/clip_2.webm",
    ], "a partial download would have been cycled in the shipped game"
