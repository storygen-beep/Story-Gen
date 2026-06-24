"""Regression tests for the game-review missing-media enumerator.

The enumerator used to walk only a node's DIRECT child blocks, so any media
nested inside a `group`, `cascade`, or `block_pool` block was invisible to
find-media's "authoritative" missing list. That silently shipped the hottest
content without art — sex-loop finishers (group), opening/first-time sex
(cascade beats), random-still pools (block_pool) — while the audit reported
"0 missing". These tests lock the recursive descent so it matches the build.
"""

from api.v1.game_review import _iter_media_blocks, _extract_missing_media


def _files(blocks):
    return [b["props"]["file"] for b in _iter_media_blocks(blocks)]


def test_iter_finds_direct_node_media():
    blocks = [
        {"type": "image", "props": {"file": "scenes/intro.jpg"}},
        {"type": "paragraph", "content": "..."},
        {"type": "video", "props": {"file": "sex/act.webm"}},
    ]
    assert _files(blocks) == ["scenes/intro.jpg", "sex/act.webm"]


def test_iter_descends_into_group_blocks():
    # Sex-loop finishers live inside group variant blocks: block["blocks"].
    blocks = [
        {"type": "group", "props": {"conditions": {}}, "blocks": [
            {"type": "paragraph", "content": "facial"},
            {"type": "video", "props": {"file": "sex/finish_facial.webm"}},
        ]},
        {"type": "group", "props": {"conditions": {}}, "blocks": [
            {"type": "video", "props": {"file": "sex/finish_inside.webm"}},
        ]},
    ]
    assert _files(blocks) == ["sex/finish_facial.webm", "sex/finish_inside.webm"]


def test_iter_descends_into_cascade_beats():
    # Opening / first-time sex lives in cascade beats: props["beats"][*]["blocks"].
    blocks = [
        {"type": "image", "props": {"file": "scenes/opening.jpg"}},
        {"type": "cascade", "props": {"beats": [
            {"advance_text": "...", "blocks": [{"type": "paragraph", "content": "x"}]},
            {"advance_text": "feel it", "blocks": [
                {"type": "video", "props": {"file": "sex/punishment_fuck.webm"}},
            ]},
            {"advance_text": "...", "blocks": [
                {"type": "video", "props": {"file": "sex/punishment_finish.webm"}},
            ]},
        ]}},
    ]
    assert _files(blocks) == [
        "scenes/opening.jpg",
        "sex/punishment_fuck.webm",
        "sex/punishment_finish.webm",
    ]


def test_iter_descends_into_block_pool():
    # Random-still pools nest under props["blocks"].
    blocks = [
        {"type": "block_pool", "props": {"blocks": [
            {"type": "image", "props": {"file": "scenes/a.jpg"}},
            {"type": "image", "props": {"file": "scenes/b.jpg"}},
        ]}},
    ]
    assert _files(blocks) == ["scenes/a.jpg", "scenes/b.jpg"]


def test_iter_handles_deep_and_mixed_nesting_in_order():
    # group inside a cascade beat — descent must be fully recursive, in doc order.
    blocks = [
        {"type": "cascade", "props": {"beats": [
            {"blocks": [
                {"type": "group", "props": {}, "blocks": [
                    {"type": "video", "props": {"file": "deep/nested.webm"}},
                ]},
            ]},
        ]}},
    ]
    assert _files(blocks) == ["deep/nested.webm"]


def test_iter_is_robust_to_malformed_blocks():
    blocks = [None, "junk", {"type": "image"}, {"type": "video", "props": {"file": "ok.webm"}}]
    # No crash; the file-less image is still yielded (caller skips empty file paths).
    out = list(_iter_media_blocks(blocks))
    assert {"type": "video", "props": {"file": "ok.webm"}} in out


def test_extract_missing_media_reports_nested_files_as_missing(tmp_path, monkeypatch):
    # End-to-end through _extract_missing_media: a group-nested video whose file is
    # absent on disk must land in `missing` (the bug shipped it as silently absent).
    import api.v1.game_review as gr
    monkeypatch.setattr(gr, "GAMES_ROOT", tmp_path)
    (tmp_path / "fakegame").mkdir()

    data = {
        "canvases": [
            {"id": "c1", "name": "C1", "nodes": [
                {"id": "n1", "blocks": [
                    {"type": "group", "props": {}, "blocks": [
                        {"type": "video", "props": {
                            "file": "sex/finish.webm",
                            "description": "d",
                            "search_queries": ["q"],
                        }},
                    ]},
                ]},
            ]},
        ],
    }
    res = gr._extract_missing_media(data, "fakegame")
    missing_files = [m["file"] for m in res["missing"]]
    assert "sex/finish.webm" in missing_files
