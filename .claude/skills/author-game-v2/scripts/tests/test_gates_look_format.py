"""lint · a look's format (references/media-blocks.md rule 6: a moving look asks for a gif; LO, 2026-11-18).

Every non-explicit `_t3` look is listed, still ones first, marked by whether its search words ask for a gif. first_term's
keyword pass found 11 moving looks and a full read found 25, so the list is never cut. Fixtures only.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def blk(name, queries, kind="image"):
    key = "file" if "." in name.rsplit("/", 1)[-1] else "pool_dir"
    return {"type": kind, "props": {key: name, "description": "d", "search_queries": queries}}


def rows(*blocks):
    return gates._look_format_rows({"canvases": [{"id": "c", "name": "C", "nodes": [{"id": "n", "blocks": list(blocks)}]}]})


def test_a_gif_word_marks_gif_and_stills_come_first():
    r = rows(blk("look/a_walk_t3", ["girl walking away gif"]), blk("look/b_mirror_t3", ["girl at mirror"]))
    assert [(f, n) for f, n, _ in r] == [("still", "look/b_mirror_t3"), ("gif", "look/a_walk_t3")]


def test_gif_inside_a_word_is_not_a_gif():
    assert rows(blk("look/x_t3", ["gifted student"]))[0][0] == "still"


def test_explicit_and_everyday_spots_are_skipped():
    assert rows(blk("sex/x_t5", ["a"], "video"), blk("look/y_t4", ["a"]), blk("life/z_t0", ["a"])) == []


def test_every_look_is_listed_once():
    many = [blk(f"look/s{i}_t3.jpg", ["q"]) for i in range(30)]
    assert len(rows(*many, *many)) == 30
