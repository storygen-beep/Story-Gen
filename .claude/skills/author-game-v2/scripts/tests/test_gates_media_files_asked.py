"""lint · media files asked for (references/media-blocks.md rule 8 "How many files a spot holds"; LO, 2026-11-18).

A pool with no `pool` aims for the engine default of 4, which is how first_term's release 1 asked for 1,808 files.
The lint counts what a harvest will be asked for and lists every non-explicit pool still at the default.
Fixtures are written here; nothing in games/ is read or written.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def blk(**props):
    return {"type": "image", "props": props}


def game(*blocks):
    return {"canvases": [{"id": "hub", "name": "Hub", "nodes": [{"id": "n", "blocks": list(blocks)}]}]}


def test_a_pool_without_a_size_counts_the_default_and_is_listed():
    total, by_tier, at_default = gates._media_files_asked_rows(game(blk(pool_dir="people/laura_kitchen_t0")))
    assert total == 4 and by_tier == {"t0": [1, 4]}
    assert at_default == ["hub#n: people/laura_kitchen_t0"]


def test_a_sized_pool_counts_its_size_and_is_not_listed():
    total, by_tier, at_default = gates._media_files_asked_rows(
        game(blk(pool_dir="people/laura_kitchen_t0", pool=1), blk(pool_dir="look/towel_t3", pool=2)))
    assert total == 3 and by_tier == {"t0": [1, 1], "t3": [1, 2]} and at_default == []


def test_an_explicit_pool_at_the_default_is_counted_but_not_listed():
    total, _, at_default = gates._media_files_asked_rows(game({"type": "video", "props": {"pool_dir": "sex/shower_t5"}}))
    assert total == 4 and at_default == []


def test_a_single_file_counts_one_and_one_asset_counts_once():
    total, by_tier, _ = gates._media_files_asked_rows(
        game(blk(file="scenes/wake_t0.jpg"), blk(file="scenes/wake_t0.jpg"), blk(pool_dir="life/x_t0", pool=1)))
    assert total == 2 and by_tier == {"t0": [2, 2]}


def test_a_bool_size_is_a_typo_not_a_count():
    total, _, at_default = gates._media_files_asked_rows(game(blk(pool_dir="life/x_t0", pool=True)))
    assert total == 4 and len(at_default) == 1
