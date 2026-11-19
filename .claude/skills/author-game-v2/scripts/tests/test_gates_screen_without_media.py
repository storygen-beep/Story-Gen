"""lint · a screen without media (references/media-blocks.md "By kind of screen"; LO, 2026-11-12, reworked 2026-11-18).

It lists only bare screens the rule wants a picture on — a sex screen, a one-time scene with no picture anywhere, a
person's hub opening bare — and counts every screen by kind beside the top games' share. A bare chore screen is not
listed. A block nested in a group or a pool counts for its screen. Fixtures only; nothing in games/ is read.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402

PIC = {"type": "image", "props": {"pool_dir": "people/x_t0"}}
CHORE = {"type": "paragraph", "content": "You run the sink hot and work through the plates, the pan and the mugs, "
                                          "one by one, until the rack is full and the water has gone grey and cold."}
SEX = {"type": "paragraph", "content": "His cock is in your mouth and your tits are wet, and he fucks your throat slow."}


def canvas(cid, *nodes, **trig):
    return {"id": cid, "name": cid, "trigger": trig, "nodes": list(nodes)}


def test_a_bare_chore_is_not_listed_but_is_counted():
    rows, kinds = gates._screen_without_media_rows({"canvases": [
        canvas("kitchen_dishes", {"id": "a", "blocks": [CHORE]}, is_repeatable=True)]})
    assert rows == [] and kinds["ordinary"] == [1, 0]


def test_a_bare_sex_screen_is_listed():
    rows, kinds = gates._screen_without_media_rows({"canvases": [
        canvas("walkin", {"id": "a", "blocks": [SEX]}, is_repeatable=True)]})
    assert rows == ["walkin#a: a sex screen with no clip"] and kinds["sex"] == [1, 0]


def test_a_one_time_scene_with_no_picture_anywhere():
    bare = canvas("meet", {"id": "a", "blocks": [CHORE]}, {"id": "b", "blocks": [CHORE]}, is_repeatable=False)
    one = canvas("meet2", {"id": "a", "blocks": [CHORE]}, {"id": "b", "blocks": [PIC, CHORE]}, is_repeatable=False)
    rows, _ = gates._screen_without_media_rows({"canvases": [bare, one]})
    assert rows == ["meet: a one-time scene with no picture on any screen"]


def test_a_person_hub_opening_bare():
    hub = canvas("hub_mark", {"id": "hub", "blocks": [CHORE]}, {"id": "beer", "blocks": [CHORE]},
                 npc="npc_mark", is_repeatable=True)
    rows, _ = gates._screen_without_media_rows({"canvases": [hub]})
    assert rows == ["hub_mark#hub: npc_mark's hub opens with no picture of them"]
    hub["nodes"][0]["blocks"].insert(0, PIC)
    assert gates._screen_without_media_rows({"canvases": [hub]})[0] == []


def test_a_block_inside_a_group_or_pool_counts():
    grouped = {"id": "a", "blocks": [{"type": "block_pool", "blocks": [{"type": "group", "blocks": [SEX, PIC]}]}]}
    rows, kinds = gates._screen_without_media_rows({"canvases": [canvas("x", grouped, is_repeatable=True)]})
    assert rows == [] and kinds["sex"] == [1, 1]


def test_alternative_lines_are_not_summed_into_a_sex_screen():
    """A pool renders one entry a visit: five variants with one explicit word each is not a sex screen."""
    one = lambda w: {"type": "paragraph", "content": f"A man at the counter watches your {w} while you pour, every time you lean in."}  # noqa: E731
    pool = {"id": "shift", "blocks": [{"type": "block_pool", "blocks": [one("ass"), one("tits"), one("tits"), one("ass"), one("tits")]}]}
    rows, kinds = gates._screen_without_media_rows({"canvases": [canvas("cafe_shift", pool, is_repeatable=True)]})
    assert rows == [] and "sex" not in kinds
