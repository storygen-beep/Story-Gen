"""lint · two people in her picture, formerly "a man in her picture" (references/media-blocks.md rule 9 "A picture you can find"; LO, 2026-11-18).

A look spot whose description names a man and her asks for two people and a glance in one real photo. first_term's
first pass found these by looking-verbs and missed 17 ("looks her over", "a man in the doorway"), so the check reads
who is in the frame. Fixtures are written here; nothing in games/ is read or written.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def blk(name, desc, kind="image"):
    key = "file" if "." in name.rsplit("/", 1)[-1] else "pool_dir"
    return {"type": kind, "props": {key: name, "description": desc}}


def rows(*blocks):
    return gates._man_in_her_picture_rows({"canvases": [{"id": "c", "name": "C", "nodes": [{"id": "n", "blocks": list(blocks)}]}]})


def test_a_look_without_a_looking_verb_is_still_listed():
    r = rows(blk("look/couch_bra_t3", "a girl lying on a couch in her bra and panties, a man in the doorway"))
    assert len(r) == 1 and "couch_bra_t3" in r[0]


def test_his_view_passes():
    assert rows(blk("look/couch_bra_t3", "Seen from a doorway: a young woman, 18, on a couch in her bra and panties.")) == []


def test_an_explicit_spot_framed_as_a_look_is_listed_since_2026_11_18():
    """Until 2026-11-18 explicit spots were skipped; a walk-in clip asking for one person staring at the other is the
    same unfindable frame as a look, so it is listed now. The act itself (two people having sex) is not."""
    assert len(rows(blk("sex/walkin_tv_t5", "a man behind a couch staring, a girl on the couch", "video"))) == 1


def test_an_everyday_t0_spot_with_two_people_is_fine():
    assert rows(blk("people/couch_gaming_t0", "a young man and a young woman side by side on a couch with controllers")) == []


def test_a_single_file_look_counts_once():
    d = "an older man in a booth lowering his newspaper to watch a waitress walk past"
    assert len(rows(blk("look/booth_t3.jpg", d), blk("look/booth_t3.jpg", d))) == 1


def test_a_woman_looking_at_her_is_two_people_too():
    """LO, 2026-11-18: the Biology TA's look sent the harvest to "lesbian milf" searches."""
    r = rows(blk("look/ta_door_look_t3", "a young woman of 28 in an office doorway holding a kettle, her eyes running down a student"))
    assert len(r) == 1 and "ta_door_look_t3" in r[0]
    assert rows(blk("look/ta_door_look_t3", "A shy young woman, 28, in an office doorway holding a kettle, blushing.")) == []


def test_a_named_person_counts_and_a_uniform_is_not_a_person():
    g = {"npcs": [{"id": "npc_laura", "name": "Laura"}], "canvases": [{"id": "c", "name": "C", "nodes": [{"id": "n", "blocks": [
        blk("look/towel_tuck_t3", "Laura, 41, tucking a bath towel over her adult daughter's chest"),
        blk("look/walk_t3", "Seen from behind a counter: a young woman's (18) ass in a waitress uniform as she walks away")]}]}]}
    r = gates._man_in_her_picture_rows(g)
    assert len(r) == 1 and "towel_tuck_t3" in r[0]


def test_an_explicit_walk_in_framed_as_a_look_is_listed_but_the_act_is_not():
    """LO, 2026-11-18: 14 walk-in clips asked for "a man in a doorway staring at a naked girl"."""
    look = rows(blk("sex/walkin_shower_mark_t4", "a middle-aged man at a bathroom sink watching a naked girl in the shower", "video"))
    assert len(look) == 1
    assert rows(blk("sex/master_door_gap_t5", "a man, 46, taking a woman, 41, from behind on the bed, the lamp on", "video")) == []
    assert rows(blk("sex/walkin_shower_mark_t4", "Seen in a bathroom mirror from the sink: a naked young woman, 18, in the shower.", "video")) == []
