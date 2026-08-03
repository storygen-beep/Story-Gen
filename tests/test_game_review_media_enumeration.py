"""Regression tests for the game-review missing-media enumerator.

The enumerator used to walk only a node's DIRECT child blocks, so any media
nested inside a `group`, `cascade`, or `block_pool` block was invisible to
find-media's "authoritative" missing list. That silently shipped the hottest
content without art — sex-loop finishers (group), opening/first-time sex
(cascade beats), random-still pools (block_pool) — while the audit reported
"0 missing". These tests lock the recursive descent so it matches the build.
"""

from api.v1.game_review import _iter_media_blocks, _extract_missing_media
from apps.common.media_blocks import block_media_paths, block_media_pool


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


# ── `files = [...]` pools ────────────────────────────────────────────────────
#
# A pool block declares N media paths for ONE slot and no singular `file`. The
# consumer read `props["file"]` only and `continue`d on empty, so every pool
# entry was invisible: a game could declare forty empty pool slots and the audit
# would report "0 missing". ~30 image pools in the_long_summer_test were dark.


def test_block_media_paths_expands_a_pool():
    assert block_media_paths({"files": ["a.webm", "b.webm", "c.webm"]}) == [
        "a.webm", "b.webm", "c.webm",
    ]


def test_block_media_paths_still_reads_a_singular_file():
    assert block_media_paths({"file": "a.webm"}) == ["a.webm"]


def test_block_media_paths_prefers_files_over_file():
    """Must match the generator, which renders the pool and ignores `file`."""
    assert block_media_paths({"files": ["a.webm"], "file": "b.webm"}) == ["a.webm"]


def test_block_media_paths_ignores_malformed_pools():
    for bad in ([], "notalist", [1, 2], None, [""], ["  "]):
        assert block_media_paths({"files": bad}) == []
    assert block_media_paths({}) == []
    assert block_media_paths(None) == []


def test_extract_missing_media_reports_every_pool_entry_as_its_own_row(tmp_path, monkeypatch):
    """Four empty slots are four files to hunt. Collapsing them to one row would
    let find-media install a single clip and mark the whole pool done."""
    import api.v1.game_review as gr
    monkeypatch.setattr(gr, "GAMES_ROOT", tmp_path)
    (tmp_path / "fakegame").mkdir()

    pool = ["sex/oral_1.webm", "sex/oral_2.webm", "sex/oral_3.webm", "sex/oral_4.webm"]
    data = {
        "canvases": [
            {"id": "c1", "name": "C1", "nodes": [
                {"id": "n1", "blocks": [
                    {"type": "video", "props": {
                        "files": pool,
                        "description": "d",
                        "search_queries": ["q"],
                    }},
                ]},
            ]},
        ],
    }
    res = gr._extract_missing_media(data, "fakegame")
    assert [m["file"] for m in res["missing"]] == pool
    # Each row carries the block's shared description + queries — one search
    # covering N clips is the whole economic argument for pools.
    assert all(m["search_queries"] == ["q"] for m in res["missing"])
    assert all(m["type"] == "video" for m in res["missing"])


# ── folder pools (`pool_dir`) ────────────────────────────────────────────────
#
# A folder pool yields ONE row for the whole block, keyed by the folder. Never one
# row per discovered filename: the options store, the review verdicts and the
# options-page URL all hang off that key, so keying on contents would re-key the
# shelf and orphan every verdict each time the human unselects a clip.


def test_block_media_pool_reads_dir_and_target():
    assert block_media_pool({"pool_dir": "sex/oral_t5", "pool": 3}) == {
        "dir": "sex/oral_t5", "target": 3,
    }


def test_block_media_pool_normalises_the_key():
    """Two spellings of one folder must not fork the shelf."""
    for spelling in ("sex/oral_t5/", "sex\\oral_t5", "  sex/oral_t5  "):
        assert block_media_pool({"pool_dir": spelling})["dir"] == "sex/oral_t5"


def test_block_media_pool_defaults_and_rejects_junk_targets():
    assert block_media_pool({"pool_dir": "a/b"})["target"] == 4
    for junk in (0, -2, "4", True, None):
        assert block_media_pool({"pool_dir": "a/b", "pool": junk})["target"] == 4


def test_block_media_pool_is_none_without_a_dir():
    assert block_media_pool({"file": "a.webm"}) is None
    assert block_media_pool({"files": ["a.webm"]}) is None
    assert block_media_pool({"pool_dir": "   "}) is None
    assert block_media_pool(None) is None


def test_pool_dir_wins_over_files_and_file_in_the_shared_reader():
    """Precedence declared once, here — every consumer inherits it."""
    props = {"pool_dir": "sex/oral_t5", "files": ["x.webm"], "file": "y.webm"}
    assert block_media_pool(props)["dir"] == "sex/oral_t5"
    assert block_media_paths(props) == [], "a folder pool declares no static paths"


def test_extract_missing_media_gives_a_pool_one_row_populated_from_disk(tmp_path, monkeypatch):
    import api.v1.game_review as gr
    monkeypatch.setattr(gr, "GAMES_ROOT", tmp_path)
    pool = tmp_path / "fakegame" / "videos" / "sex" / "oral_t5"
    pool.mkdir(parents=True)
    for name in ("clip_1.webm", "clip_2.webm", "clip_10.webm"):
        (pool / name).write_bytes(b"x")

    data = {"canvases": [{"id": "c1", "name": "C1", "nodes": [{"id": "n1", "blocks": [
        {"type": "video", "props": {"pool_dir": "sex/oral_t5", "pool": 4}},
    ]}]}]}
    res = gr._extract_missing_media(data, "fakegame")

    assert len(res["found"]) == 1 and res["missing"] == []
    row = res["found"][0]
    assert row["file"] == "sex/oral_t5", "the row's identity is the folder"
    assert row["pool_count"] == 3 and row["pool_target"] == 4
    # Natural order — lexical sort would put clip_10 second.
    assert [i["actual_file"] for i in row["pool_items"]] == [
        "clip_1.webm", "clip_2.webm", "clip_10.webm",
    ]
    assert row["pool_items"][0]["serve_path"] == "videos/sex/oral_t5/clip_1.webm"


def test_find_pool_ignores_dot_prefixed_files(tmp_path, monkeypatch):
    """A dot-prefixed name is staging or OS metadata, never a selected clip.

    `.incoming-c1.gif` carries a real media suffix, so a suffix-only filter lets it
    through — and "." sorts before "c", so it took tile #1 and shifted every ordinal
    caption on the review page while the file was still being written to.
    """
    import api.v1.game_review as gr
    monkeypatch.setattr(gr, "GAMES_ROOT", tmp_path)
    pool = tmp_path / "fakegame" / "videos" / "sex" / "oral_t5"
    pool.mkdir(parents=True)
    for name in ("clip_1.webm", "clip_2.webm", ".incoming-c1.gif", "._clip_1.webm"):
        (pool / name).write_bytes(b"x")

    data = {"canvases": [{"id": "c1", "name": "C1", "nodes": [{"id": "n1", "blocks": [
        {"type": "video", "props": {"pool_dir": "sex/oral_t5", "pool": 4}},
    ]}]}]}
    row = gr._extract_missing_media(data, "fakegame")["found"][0]

    assert [i["actual_file"] for i in row["pool_items"]] == ["clip_1.webm", "clip_2.webm"]
    assert row["pool_count"] == 2, "a partial download was counted as a pool member"


def test_an_empty_pool_folder_still_produces_a_row(tmp_path, monkeypatch):
    """The row comes from the TOML and is merely POPULATED from disk. Deriving it
    from disk contents would make an unstocked pool vanish from the audit — the
    exact bug apps/common/media_blocks.py was written to stop."""
    import api.v1.game_review as gr
    monkeypatch.setattr(gr, "GAMES_ROOT", tmp_path)
    (tmp_path / "fakegame").mkdir()

    data = {"canvases": [{"id": "c1", "name": "C1", "nodes": [{"id": "n1", "blocks": [
        {"type": "video", "props": {"pool_dir": "sex/oral_t5", "pool": 4,
                                    "search_queries": ["q"]}},
    ]}]}]}
    res = gr._extract_missing_media(data, "fakegame")

    assert [m["file"] for m in res["missing"]] == ["sex/oral_t5"]
    assert res["missing"][0]["pool_count"] == 0
    assert res["missing"][0]["search_queries"] == ["q"]


def test_pool_row_identity_is_never_empty(tmp_path, monkeypatch):
    """media_review.py dedupes on `file`; if a pool row left it unset, every pool
    in the game would collapse into one row keyed by None."""
    import api.v1.game_review as gr
    monkeypatch.setattr(gr, "GAMES_ROOT", tmp_path)
    (tmp_path / "fakegame").mkdir()

    data = {"canvases": [{"id": "c1", "name": "C1", "nodes": [{"id": "n1", "blocks": [
        {"type": "video", "props": {"pool_dir": "sex/a_t5"}},
        {"type": "video", "props": {"pool_dir": "sex/b_t5"}},
    ]}]}]}
    res = gr._extract_missing_media(data, "fakegame")

    keys = [m["file"] for m in res["missing"]]
    assert keys == ["sex/a_t5", "sex/b_t5"]
    assert len(set(keys)) == 2


def test_extract_missing_media_finds_a_pool_nested_in_a_group(tmp_path, monkeypatch):
    """Both blind spots at once: nested container AND a pool inside it."""
    import api.v1.game_review as gr
    monkeypatch.setattr(gr, "GAMES_ROOT", tmp_path)
    (tmp_path / "fakegame").mkdir()

    data = {
        "canvases": [
            {"id": "c1", "name": "C1", "nodes": [
                {"id": "n1", "blocks": [
                    {"type": "group", "props": {}, "blocks": [
                        {"type": "image", "props": {"files": ["a.jpg", "b.jpg"]}},
                    ]},
                ]},
            ]},
        ],
    }
    res = gr._extract_missing_media(data, "fakegame")
    assert [m["file"] for m in res["missing"]] == ["a.jpg", "b.jpg"]


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


# ── content band on every entry ──────────────────────────────────────────────
#
# The band is attached at the same choke point as `slot_key`, and for the same
# reason: six categories build entries independently, so banding at any one of
# them means a seventh ships unbanded. See apps/common/media_band.py.


def test_every_entry_carries_a_band_whatever_category_built_it(tmp_path, monkeypatch):
    import api.v1.game_review as gr
    monkeypatch.setattr(gr, "GAMES_ROOT", tmp_path)
    (tmp_path / "fakegame").mkdir()

    data = {
        "locations": [{"id": "l1", "name": "Atrium", "image": "locations/atrium.jpg"}],
        "clothing": [{"id": "c1", "name": "Bra", "slot": "bra", "image": "clothing/bra.jpg"}],
        "npcs": [{"id": "n1", "name": "Mercer", "portrait": "mercer.jpg"}],
        "player_portrait": {"default_image": "portraits/w.jpg",
                            "naked_image": "portraits/w_naked.jpg"},
        "phone": {"posts": [{"id": "p1", "image": "phone/post.jpg", "caption": "hi"}]},
        "canvases": [
            {"id": "c1", "name": "C1", "nodes": [
                {"id": "n1", "blocks": [
                    {"type": "video", "props": {"file": "sex/act_t5.webm"}},
                ]},
            ]},
        ],
    }
    res = gr._extract_missing_media(data, "fakegame")
    entries = res["missing"] + res["found"]
    assert entries, "fixture built nothing"
    for e in entries:
        assert e.get("band"), f"{e['file']} has no band"
        assert e.get("band_source"), f"{e['file']} has no band_source"

    by_file = {e["file"]: e for e in entries}
    assert by_file["sex/act_t5.webm"]["band"] == "explicit"
    assert by_file["locations/atrium.jpg"]["band"] == "clean"
    assert by_file["mercer.jpg"]["band"] == "clean"
    # The player portrait undresses; the NPC face does not. Banded from the state
    # key the engine already parses, so no authoring is required.
    assert by_file["portraits/w_naked.jpg"]["band"] == "nudity"
    assert by_file["portraits/w_naked.jpg"]["band_source"] == "portrait_state"


def test_an_authored_tier_on_a_block_overrides_the_derived_band(tmp_path, monkeypatch):
    """Nothing in the repo authors a tier yet. This is the escape hatch that lets a
    human correct a wrong derivation without renaming the file or moving the folder."""
    import api.v1.game_review as gr
    monkeypatch.setattr(gr, "GAMES_ROOT", tmp_path)
    (tmp_path / "fakegame").mkdir()

    data = {"canvases": [
        {"id": "c1", "name": "C1", "nodes": [
            {"id": "n1", "blocks": [
                # Path says nothing; the author says it is explicit.
                {"type": "image", "props": {"file": "scenes/quiet.jpg", "tier": "t5"}},
                # Path says sex/, the author overrules it downward.
                {"type": "image", "props": {"file": "sex/establishing.jpg", "tier": "t2"}},
            ]},
        ]},
    ]}
    by_file = {e["file"]: e for e in gr._extract_missing_media(data, "fakegame")["missing"]}
    assert by_file["scenes/quiet.jpg"]["band"] == "explicit"
    assert by_file["scenes/quiet.jpg"]["band_source"] == "authored"
    assert by_file["sex/establishing.jpg"]["band"] == "clean"


def test_a_pool_row_is_banded_from_its_folder(tmp_path, monkeypatch):
    """A pool's `file` IS the folder, so the tier suffix on the dir does the work."""
    import api.v1.game_review as gr
    monkeypatch.setattr(gr, "GAMES_ROOT", tmp_path)
    game = tmp_path / "fakegame"
    (game / "videos" / "sex" / "oral_t5").mkdir(parents=True)
    (game / "videos" / "sex" / "oral_t5" / "a.webm").write_bytes(b"x")

    data = {"canvases": [
        {"id": "c1", "name": "C1", "nodes": [
            {"id": "n1", "blocks": [
                {"type": "video", "props": {"pool_dir": "sex/oral_t5", "pool": 4}},
            ]},
        ]},
    ]}
    row = gr._extract_missing_media(data, "fakegame")["found"][0]
    assert row["pool_dir"] == "sex/oral_t5"
    assert (row["band"], row["band_source"]) == ("explicit", "tier_suffix")
