"""lint · a man in her picture (references/media-blocks.md rule 9 "A picture you can find"; LO, 2026-11-18).

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


def test_an_explicit_spot_is_not_this_lints_business():
    assert rows(blk("sex/walkin_tv_t5", "a man behind a couch staring, a girl on the couch", "video")) == []


def test_an_everyday_t0_spot_with_two_people_is_fine():
    assert rows(blk("people/couch_gaming_t0", "a young man and a young woman side by side on a couch with controllers")) == []


def test_a_single_file_look_counts_once():
    d = "an older man in a booth lowering his newspaper to watch a waitress walk past"
    assert len(rows(blk("look/booth_t3.jpg", d), blk("look/booth_t3.jpg", d))) == 1
