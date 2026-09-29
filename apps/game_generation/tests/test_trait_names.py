"""EN5 + EN6 — one name per trait; locked buttons read a man's feeling.

PRD_SKILL_TEST_FIXES_v2 §2 EN5 + EN6 (D3a · D5). A trait's name came from a dozen
places that disagreed: the lock suffix and the toast printed `cap(key)`, the Stats page
and the sidebar dump the raw key, guidance the label — or "" for a hide-only entry.
Locked buttons dropped every NPC gate.

Now:
  * `setup.traitLabel(key)` — the [[traits.labels]] label, else the tidied key
    ("crowd_standing" -> "Crowd standing", LO 2026-09-30) — is every screen's name;
  * `[[traits.labels]] in_dump = false` keeps a trait out of the sidebar dump only;
    `hidden = true` still means a secret (no dump, no Stats page);
  * an NPC gate on a locked button prints "<Name>'s <Label> N+ (has M)"; a met item is
    not listed.

The fixture's `corr` is labelled "Corruption": no screen may print "corr".

Old saves (§0 rule 8): no new state. A save the pre-change build wrote loads and every
name renders from the label.

    pytest apps/game_generation/tests/test_trait_names.py -q
"""
import re
import warnings

import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml, validate

from .headless import build, needs_browser, open_game, read_data

FIXTURE = "apps/game_generation/games_toml_files/engine_skill_test_fixes_2026_09_30.toml"
BOARD = "Canvas_gate_board_Node_board"
NO_KEY = re.compile(r"\bcorr\b")  # the key, as a word — "Corruption" does not match


def _raw():
    return parse_toml(FIXTURE)


def _validate(raw):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return validate(normalize(raw))


def _twee(raw=None):
    graph = build_game_graph(normalize(raw or _raw()))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def _passage(twee, name):
    return next("\n:: " + p for p in twee.split("\n:: ") if p.split("\n", 1)[0].split(" ")[0] == name)


# ── 1. the hops and the validator ────────────────────────────────────────────


def test_in_dump_reaches_the_metadata_only_when_false():
    labels = build_game_graph(normalize(_raw())).project.metadata["trait_labels"]
    assert labels["stamina"]["in_dump"] is False
    assert "in_dump" not in labels["corr"]


def test_the_fixture_is_clean():
    assert _validate(_raw()) == []


def test_an_in_dump_only_entry_may_omit_its_label():
    raw = _raw()
    del raw["traits"]["labels"][1]["in_dump"]  # stamina: no label, no in_dump, no hidden
    assert any("traits.labels[stamina] missing required `label`" in e for e in _validate(raw))


def test_in_dump_must_be_a_bool():
    raw = _raw()
    raw["traits"]["labels"][1]["in_dump"] = "no"
    assert any("in_dump must be true or false" in e for e in _validate(raw))


def test_the_dump_skips_in_dump_false_and_hidden_but_the_stats_page_only_hidden():
    twee = _twee()
    assert "setup.dumpSkipTraits = [\"stamina\"];" in twee
    assert "setup.hiddenTraits = [];" in twee
    assert "setup.dumpSkipTraits.includes(_k)" in twee  # the playerTraits widget
    stats = _passage(twee, "StatsPage")
    assert "setup.hiddenTraits.includes(_tk)" in stats and "dumpSkipTraits" not in stats


def test_the_python_side_now_asks_for_an_npc_only_gates_suffix():
    board = _passage(_twee(), BOARD)
    npc_only = next(l for l in board.splitlines() if "Ask him to stay." in l and "locked-choice" in l)
    assert "setup.requirementSuffix(" in npc_only


# ── 2. behaviour, in the real engine ─────────────────────────────────────────


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("en5") / "out")


def _text(g, sel=".passage"):
    return g.js(f"() => (document.querySelector('{sel}') || {{}}).innerText || ''")


def _locked(g):
    return g.js("() => [...document.querySelectorAll('.passage .locked-choice')].map(e => e.innerText.trim())")


@needs_browser
def test_trait_label(html):
    with open_game(html) as g:
        lab = "(k) => SugarCube.setup.traitLabel(k)"
        assert g.js(lab, "corr") == "Corruption"
        assert g.js(lab, "stamina") == "Stamina"          # entry with no label
        assert g.js(lab, "crowd_standing") == "Crowd standing"
        assert g.js(lab, "money") == "Money"


@needs_browser
def test_the_locked_buttons_name_hers_and_his(html):
    with open_game(html) as g:
        g.play(BOARD)
        locked = _locked(g)
        assert "Kiss him. (Corruption 20+ (you have 5))" in locked
        assert "Ask him to stay. (Tobin's Trust 50+ (has 10))" in locked
        # the met half (his trust 10 >= 5) is not listed
        assert "Take him upstairs. (Corruption 20+ (you have 5))" in locked
        assert not any(NO_KEY.search(t) for t in locked)
        assert g.errors == []


@needs_browser
def test_format_canvas_conditions_names_the_same_way(html):
    with open_game(html) as g:
        fmt = """(items) => { const d = document.createElement('div');
            d.innerHTML = SugarCube.setup.formatCanvasConditions({version: '1.0', items: items});
            return d.innerText; }"""
        assert g.js(fmt, [{"type": "trait", "subject": "player", "trait_key": "corr",
                           "operator": "gte", "value": 20}]) == "Required: Your Corruption ≥ 20"
        assert g.js(fmt, [{"type": "trait", "subject": "npc", "npc_id": "tobin",
                           "trait_key": "trust", "operator": "gte", "value": 50}]) == "Required: Tobin's Trust ≥ 50"


@needs_browser
def test_the_toast_uses_the_label_and_shows_a_dump_skipped_trait(html):
    with open_game(html) as g:
        g.play(BOARD)
        g.click("Dance.")
        toast = g.js("() => [...document.querySelectorAll('.effect-toast')].map(e => e.innerText).join(' ')")
        assert "+2 Corruption" in toast and "+3 Stamina" in toast
        assert not NO_KEY.search(toast)
        assert g.errors == []


@needs_browser
def test_the_dump_and_the_stats_page(html):
    with open_game(html) as g:
        g.play("Location_loc_home")
        dump = _text(g, "#traits-widget")
        assert "Corruption" in dump and not NO_KEY.search(dump)
        assert "Stamina" not in dump                       # in_dump = false
        g.play("StatsPage")
        stats = _text(g)
        assert "Corruption" in stats and "Stamina" in stats  # only `hidden` removes it here
        assert not NO_KEY.search(stats)
        assert g.errors == []


@needs_browser
def test_guidance_label_has_no_empty_name(html):
    with open_game(html) as g:
        lab = "(item) => SugarCube.setup._labelForTrait(item)"
        assert g.js(lab, {"trait_key": "stamina", "subject": "player"}) == "Stamina"
        assert g.js(lab, {"trait_key": "corr", "subject": "player"}) == "Corruption"


@needs_browser
def test_a_trait_bar_with_no_label_names_the_trait(html):
    with open_game(html) as g:
        markup = ('<<set _item to {type: "trait_bar", trait: "corr", max: 100}>>'
                  '<<print _item.label || setup.traitLabel(_item.trait)>>')
        out = g.js("(m) => { const d = document.createElement('div');"
                   " new SugarCube.Wikifier(d, m); return d.innerText; }", markup)
        assert out == "Corruption"


@needs_browser
def test_the_cost_messages_use_the_name(html):
    with open_game(html) as g:
        msg = g.js("() => SugarCube.setup.getCostBlockedMessage([{trait: 'corr', value: 30}])")
        assert msg == "Requires 30 Corruption (you have 5)"


@needs_browser
def test_a_save_made_before_en5(html):
    """§0 rule 8. Written by the PRE-change engine (the EN4 tree, snapshotted to scratch)
    from the fixture with stamina given a label (the old validator requires one):
    Engine.play Location_loc_home, Save.serialize()."""
    with open_game(html) as g:
        assert g.load_save(read_data("en5_pre_change_save.txt")) is True
        assert g.passage() == "Location_loc_home"
        g.play(BOARD)
        assert "Ask him to stay. (Tobin's Trust 50+ (has 10))" in _locked(g)
        assert g.errors == []
