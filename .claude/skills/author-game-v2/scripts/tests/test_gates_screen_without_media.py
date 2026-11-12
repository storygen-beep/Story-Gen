"""lint · a screen without media (references/media-blocks.md "Every screen, not every scene"; LO, 2026-11-12).

A scene with a picture on its first screen still leaves its other screens bare; the list counts by screen. A block
nested in a group or a pool counts for its screen. Fixtures are written here; nothing in games/ is read or written.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

PIC = {"type": "image", "props": {"pool_dir": "people/x_t0"}}
P = {"type": "paragraph", "content": "Mark is on the couch."}


def game(*nodes):
    return {"canvases": [{"id": "hub_mark", "name": "Mark", "nodes": list(nodes)}]}


def test_a_scene_with_one_picture_still_lists_its_bare_screens():
    rows, n = gates._screen_without_media_rows(game({"id": "hub", "blocks": [PIC, P]}, {"id": "beer", "blocks": [P]}))
    assert n == 2 and rows == ["hub_mark#beer"]


def test_a_block_inside_a_group_or_pool_counts():
    grouped = {"id": "film", "blocks": [{"type": "block_pool", "blocks": [{"type": "group", "blocks": [P, PIC]}]}]}
    rows, n = gates._screen_without_media_rows(game(grouped))
    assert n == 1 and rows == []
