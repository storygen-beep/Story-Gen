"""`media-review/list` — joining shelf depth onto the slot enumeration.

The review page has to tell three states apart, and until this join existed it
could only see the first:

  * something is installed          -> review it
  * nothing installed, shelf stocked -> the HUMAN owes a pick
  * nothing installed, shelf empty   -> the SEARCH hasn't run

The second state is the whole point. Under the find-media v3 flow nothing is
auto-installed — a run ends with a clean shelf and an empty slot — so without
`options_count` on the row, a fully-searched slot is indistinguishable from one
nobody has touched.

Two rules carry the weight here:
  * `origin: "previous"` entries are the slot's UNDO HISTORY, not candidates. A
    shelf holding only those is unworked, not ready.
  * A pool holding 1 of 4 clips is already `found`, so it is never "ready to
    pick" — it keeps the softer `n of target` signal instead of reading as
    unstarted.

    pytest tests/test_media_review_shelf_state.py -q
"""
import json

import pytest

import api.v1.game_review as gr
import api.v1.media_review as mr


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

SINGLE = '  { type = "video", props = { file = "sex/a_t5.webm", description = "d" } },'
POOL = '  { type = "video", props = { pool_dir = "sex/a_t5", pool = 4, description = "d" } },'
# The authored `id` sits on the BLOCK, not inside props — that is what
# apps.common.media_blocks.block_slot_key reads.
TAGGED = (
    '  { type = "video", id = "slot_a", props = { file = "sex/a_t5.webm", '
    'description = "d" } },'
)


@pytest.fixture
def game(tmp_path, monkeypatch):
    """A fixture game whose TOML + ledgers the test controls.

    GAMES_ROOT is patched on game_review — media_review imports the name from
    there, and _safe_game_dir resolves against that same module-level constant.
    """
    monkeypatch.setattr(gr, "GAMES_ROOT", tmp_path)
    monkeypatch.setattr(mr, "GAMES_ROOT", tmp_path)
    root = tmp_path / "g"
    (root / "toml_phases").mkdir(parents=True)
    (root / ".find-media").mkdir(parents=True)
    (root / "videos").mkdir(parents=True)

    def write(blocks_toml, *, shelf=None, pool_files=()):
        (root / "toml_phases" / "7_final_game.toml").write_text(TOML % blocks_toml)
        if shelf is not None:
            (root / ".find-media" / "media_options.json").write_text(
                json.dumps({"game": "g", "options": shelf})
            )
        for rel in pool_files:
            target = root / "videos" / rel
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b"\x00" * 64)
        return root

    return write


def _enumerate(root):
    return mr._enumerate("g", root)


def _only(result):
    """The single item these fixtures declare."""
    assert len(result["items"]) == 1, result["items"]
    return result["items"][0]


# ── shelf depth ──────────────────────────────────────────────────────────────

def test_options_count_excludes_undo_history(game):
    """`origin: "previous"` is a replaced asset parked for re-selection. Counting
    it as a candidate would report a searched shelf on a slot never searched."""
    root = game(SINGLE, shelf={"sex/a_t5.webm": [
        {"url": "u1"},
        {"url": "u2"},
        {"url": "old", "origin": "previous"},
    ]})
    item = _only(_enumerate(root))

    assert item["options_count"] == 2
    assert item["options_total"] == 3


def test_a_shelf_of_only_undo_history_reads_as_unworked(game):
    root = game(SINGLE, shelf={"sex/a_t5.webm": [{"url": "old", "origin": "previous"}]})
    result = _enumerate(root)

    assert _only(result)["options_count"] == 0
    assert result["counts"]["unworked"] == 1
    assert result["counts"]["ready_to_pick"] == 0


def test_shelf_is_read_under_the_authored_slot_key(game):
    """A block with an `id` keys its shelf on that, not on the path — the same
    convention the verdict merge already uses."""
    root = game(TAGGED, shelf={"slot_a": [{"url": "u1"}, {"url": "u2"}]})
    item = _only(_enumerate(root))

    assert item["slot_key"] == "slot_a"
    assert item["options_count"] == 2


def test_shelf_falls_back_to_the_file_path_when_untagged(game):
    root = game(SINGLE, shelf={"sex/a_t5.webm": [{"url": "u1"}]})
    assert _only(_enumerate(root))["options_count"] == 1


def test_a_missing_options_ledger_is_not_an_error(game):
    """Most games have never had a search run. That is a zero, not a 500."""
    root = game(SINGLE)
    item = _only(_enumerate(root))

    assert item["options_count"] == 0
    assert item["options_total"] == 0


def test_a_corrupt_options_ledger_degrades_to_zero(game):
    root = game(SINGLE)
    (root / ".find-media" / "media_options.json").write_text("{not json")

    assert _only(_enumerate(root))["options_count"] == 0


# ── the aggregate counts the filter bar renders ──────────────────────────────

def test_a_stocked_empty_slot_is_ready_to_pick(game):
    root = game(SINGLE, shelf={"sex/a_t5.webm": [{"url": "u1"}, {"url": "u2"}]})
    counts = _enumerate(root)["counts"]

    assert counts["ready_to_pick"] == 1
    assert counts["unworked"] == 0
    assert counts["missing"] == 1


def test_an_untouched_slot_is_unworked(game):
    root = game(SINGLE)
    counts = _enumerate(root)["counts"]

    assert counts["unworked"] == 1
    assert counts["ready_to_pick"] == 0


def test_an_empty_pool_with_a_shelf_is_ready_to_pick(game):
    root = game(POOL, shelf={"sex/a_t5": [{"url": "u1"}, {"url": "u2"}]})
    counts = _enumerate(root)["counts"]

    assert counts["ready_to_pick"] == 1
    assert counts["unworked"] == 0


def test_a_partially_filled_pool_is_neither_ready_nor_unworked(game):
    """1 of 4 renders a 3-short pool, not an unstarted one — it already plays,
    and its own `n of target` badge is the honest signal."""
    root = game(
        POOL,
        shelf={"sex/a_t5": [{"url": "u1"}, {"url": "u2"}]},
        pool_files=("sex/a_t5/clip1.webm",),
    )
    result = _enumerate(root)
    item = _only(result)

    assert item["found"] is True
    assert item["pool_count"] == 1
    assert result["counts"]["ready_to_pick"] == 0
    assert result["counts"]["unworked"] == 0


def test_an_empty_pool_with_no_shelf_is_unworked(game):
    root = game(POOL)
    counts = _enumerate(root)["counts"]

    assert counts["unworked"] == 1
    assert counts["ready_to_pick"] == 0


# ── reuse: one asset, one row, one shelf ─────────────────────────────────────

def test_a_file_reused_across_canvases_keeps_its_shelf_once(game):
    """Counts are attached BEFORE the dedupe-by-file pass, so the surviving row
    carries its own depth instead of losing it to the dropped duplicate."""
    two_canvases = TOML % SINGLE + """
[[canvases]]
id = "c2"
name = "C2"

[canvases.trigger]
location = "loc"
is_active = true

[[canvases.nodes]]
id = "base"
name = "Base"
blocks = [
  { type = "video", props = { file = "sex/a_t5.webm", description = "d" } },
]

[canvases.nodes.exit_block]
type = "location"
text = "Done."
"""
    root = game(SINGLE, shelf={"sex/a_t5.webm": [{"url": "u1"}, {"url": "u2"}]})
    (root / "toml_phases" / "7_final_game.toml").write_text(two_canvases)

    result = _enumerate(root)
    item = _only(result)

    assert item["options_count"] == 2
    assert result["counts"]["ready_to_pick"] == 1
