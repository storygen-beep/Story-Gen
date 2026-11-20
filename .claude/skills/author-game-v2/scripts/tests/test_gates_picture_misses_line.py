"""lint · a picture that misses its line (LO, 2026-11-18). Fixtures only; nothing in games/ is read."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402


def g(name, *blocks):
    return {"npcs": [], "canvases": [{"id": "c", "name": name, "nodes": [{"id": "n", "blocks": list(blocks)}]}]}


def pic(name, desc):
    return {"type": "image", "props": {"pool_dir": name, "description": desc}}


P = lambda t: {"type": "paragraph", "content": t}  # noqa: E731


def test_an_empty_lounger_under_her_body_is_listed():
    r = gates._picture_misses_line_rows(g("Lie in the sun", pic("life/lounger_t0", "a sun lounger in a small back garden"),
                                          P("Topless, on your front, the side of your tits pressed flat to the lounger.")))
    assert len(r) == 1 and "lounger_t0" in r[0][1]


def test_a_body_picture_on_the_screen_clears_it():
    assert gates._picture_misses_line_rows(g("Lie in the sun", pic("life/lounger_t0", "a sun lounger"),
                                             P("Topless, your tits pressed flat to the lounger."),
                                             pic("look/sun_t3", "A young woman, 18, topless on a lounger"))) == []


def test_a_mirror_scene_whose_picture_of_her_never_says_mirror():
    r = gates._picture_misses_line_rows(g("Check your clothes in the hall mirror",
                                          pic("sex/hall_t4", "a naked young woman, 18, standing in a house hallway")))
    assert len(r) == 1 and "mirror" in r[0][2]
    assert gates._picture_misses_line_rows(g("Check your clothes in the hall mirror",
                                             pic("sex/hall_t4", "a naked young woman, 18, at a hall mirror"))) == []
    # a reaction shot of him is not judged
    assert gates._picture_misses_line_rows(g("In the mirror", pic("sex/his_t4", "a young man in a doorway, hand on his bulge"))) == []
