"""`manage.py check_media` must see media nested inside container blocks.

⚠️ `test_check_media_sees_media_inside_a_group` is the load-bearing one. This walk read
only DIRECT children of a node, so every media block inside a `group`, a `cascade` beat or
a `block_pool` was invisible — and that is exactly where the hottest content lives:
sex-loop finishers, opening/first-time sex, random-still pools.

Measured on vesper when this was written: **28 of 177 media blocks, 16%, missing from the
audit**, including both pools inside Marsh's `finish_soft` group chain. The failure mode is
the dangerous one — the audit says "found" while the beat ships blank.

The descent now lives once in `apps/common/media_blocks.iter_media_blocks`, imported by
both this command and `api/v1/game_review.py`. That is the third fix in this bug class
(`block_media_paths` was the first), so the test asserts the SHARED helper is what both
call, not that each happens to be right today.
"""
from apps.common.media_blocks import iter_media_blocks
from apps.game_generation.management.commands.check_media import Command


def _refs(toml_data):
    return Command()._extract_media_references(toml_data)


def _canvas(node_blocks):
    return {"canvases": [{"id": "c1", "name": "C1",
                          "nodes": [{"id": "n1", "blocks": node_blocks}]}]}


def test_check_media_sees_media_inside_a_group():
    """Sex-loop finishers live in group branches keyed on sex_finisher_type."""
    data = _canvas([
        {"type": "group", "props": {}, "blocks": [
            {"type": "paragraph", "content": "he finishes"},
            {"type": "video", "props": {"file": "sex/finish_facial.webm"}},
        ]},
        {"type": "group", "props": {}, "blocks": [
            {"type": "video", "props": {"pool_dir": "sex/finish_inside_t5", "pool": 4}},
        ]},
    ])
    paths = {r["file"] for r in _refs(data)}
    assert "sex/finish_facial.webm" in paths
    assert "sex/finish_inside_t5" in paths


def test_check_media_sees_media_inside_a_cascade_beat():
    data = _canvas([
        {"type": "cascade", "props": {"beats": [
            {"advance_text": "...", "blocks": [{"type": "paragraph", "content": "x"}]},
            {"advance_text": "...", "blocks": [
                {"type": "video", "props": {"file": "sex/opening_fuck.webm"}},
            ]},
        ]}},
    ])
    assert "sex/opening_fuck.webm" in {r["file"] for r in _refs(data)}


def test_check_media_sees_media_inside_a_block_pool():
    data = _canvas([
        {"type": "block_pool", "props": {"blocks": [
            {"type": "image", "props": {"file": "scenes/ambient_a.jpg"}},
        ]}},
    ])
    assert "scenes/ambient_a.jpg" in {r["file"] for r in _refs(data)}


def test_direct_children_still_work():
    data = _canvas([{"type": "image", "props": {"file": "locations/atrium.jpg"}}])
    assert "locations/atrium.jpg" in {r["file"] for r in _refs(data)}


def test_both_enumerators_call_the_same_shared_walker():
    """The drift guard. game_review's private name is an alias, not a second copy —
    if someone re-implements either walk, this fails before the audit goes blind again."""
    from api.v1.game_review import _iter_media_blocks
    assert _iter_media_blocks is iter_media_blocks

    import inspect
    from apps.game_generation.management.commands import check_media as cm
    src = inspect.getsource(cm.Command._extract_media_references)
    assert "iter_media_blocks" in src, "check_media stopped using the shared descent"
