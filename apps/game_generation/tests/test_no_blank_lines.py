"""A screen has no empty lines the author didn't write.

SugarCube renders every line break in a passage's source as a <br>. The v2 generator
used to put its invisible macros on lines of their own: the line pool and the
condition-group chain joined `<<set>>` / `<<if>>` / `<<elseif>>` / `<</if>>` with
"\\n", and every node passage ended its content with "\\n\\n" plus one line each for
the current_canvas / current_node sets, markCanvasTriggered and visited_nodes. None of
those macros prints anything, but their line breaks did: first_term (2026-11-02) had
5,686 empty lines over its 593 canvas screens, up to 17 in a row, and Gary's booth
showed two above his one line and eight below it.

Now the glue is emitted with no line breaks. The only <br> left on a screen is the
one after each button inside the exits' <<nobr>> block (one button per line).

    pytest apps/game_generation/tests/test_no_blank_lines.py -q
"""
import re
import warnings

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml

from .headless import build, needs_browser, open_game

FIXTURE = "apps/game_generation/games_toml_files/engine_skill_test_fixes_2026_09_30.toml"


def _gen():
    g = TweeComprehensiveGeneratorV2()
    g.video_files = {}
    g.video_path = "./videos"
    g.current_canvas_id = "canvas_probe"
    g.options = {"game_folder": "probe"}
    return g


def _p(text):
    return {"type": "paragraph", "content": text}


COND = {"version": "1.0", "logic": "AND",
        "items": [{"type": "flag", "subject": "player", "flag_key": "x", "operator": "is_true"}]}


def test_a_line_pool_has_no_line_breaks():
    for memory in ({}, {"memory": "seen"}):
        pool = {"type": "block_pool", "props": {"blocks": [_p("one"), _p("two"), _p("three")], **memory}}
        out = _gen()._convert_blocks_to_game_html([_p("before"), pool, _p("after")])
        assert "<<if _bp is 0>>" in out and "<</if>>" in out
        assert "\n" not in out, out


def test_a_group_chain_has_no_line_breaks():
    groups = [
        {"type": "group", "props": {"conditions": COND, "blocks": [_p("shown when x")]}},
        {"type": "group", "props": {"blocks": [_p("otherwise")]}},
    ]
    out = _gen()._convert_blocks_to_game_html([_p("before"), *groups, _p("after")])
    assert "<<if setup.triggerConditionsSatisfied(" in out and "<<else>>" in out
    assert "\n" not in out, out


def _canvas_passages(twee):
    for chunk in twee.split("\n:: ")[1:]:
        title, _, body = chunk.partition("\n")
        if title.split(" ")[0].startswith("Canvas_"):
            yield title, body


def test_a_node_passage_has_no_line_break_before_its_exits():
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        graph = build_game_graph(normalize(parse_toml(FIXTURE)))
    for dev in (False, True):
        twee = TweeComprehensiveGeneratorV2().generate(graph.project, {"dev_mode": dev}, graph=graph)
        seen = 0
        for title, body in _canvas_passages(twee):
            head = body.split("<<nobr>>", 1)[0]  # the exits' block keeps its own line breaks
            assert "<<set $game_state.current_canvas" in head, title
            assert not re.search(r">\n+<", head), (title, head[:300])
            seen += 1
        assert seen > 0


@needs_browser
def test_no_empty_line_renders_outside_the_buttons(tmp_path):
    html = build(FIXTURE, tmp_path / "out")
    with open_game(html) as g:
        names = g.js("() => SugarCube.Story.lookupWith(p => p.title.startsWith('Canvas_')).map(p => p.title)")
        assert names
        for name in names:
            g.play(name)
            stray = g.js("""() => {
                const kids = [...document.querySelector('.passage').childNodes]
                    .filter(c => !(c.nodeType === 3 && !c.textContent.trim()));
                // a button: a link, or a locked choice's greyed span
                const isButton = (n) => n && n.nodeType === 1 && (n.tagName === 'A'
                    || (n.tagName === 'SPAN' && /locked-choice/.test(n.className)));
                return kids.filter((c, i) => c.nodeType === 1 && c.tagName === 'BR'
                    && !isButton(kids[i - 1])).length;
            }""")
            assert stray == 0, name
