"""EN1 — a one-time step is used only on its "yes"; a no is parked or final.

PRD_SKILL_TEST_FIXES_v2 §2 EN1 (D6 · I4 · Dr1). Before this, node 0 of a one-time
canvas marked it fired (v2.py `markCanvasTriggered`, emitted on node 0) and
`canTriggerCanvas` refused it for ever once `total >= 1` — so a "no" that parks the
step could not exist: the step was used up the moment it was seen.

Opt-in by the trigger key `consume_on = "exit"`. Node 0's fired mark is kept as it is
(it still drives the per-day/activity limits and decay contact); a separate record in
`$game_state.canvas_state` decides whether the step is used up:

  * `consumes = true` on a choice (the yes)   -> used up, never offered again
  * `final = true` (the warned final no)       -> used up + `<canvas>_closed` flag
  * `retry_after_days = N` (a parked no)       -> offered again after N days
  * leaving mid-scene with none of those       -> parked for the canvas's
                                                  `retry_after_days` (1 when absent)

Old saves (§0 rule 8): a save made before EN1 holds a fired step with no record. It
keeps that build's meaning — used up. Proven by loading a save string a pre-change
build actually wrote (tests/data/en1_pre_change_save.txt; how it was made is in the
test's docstring).

    pytest apps/game_generation/tests/test_step_consume_on_exit.py -q
"""
import copy
import inspect
import warnings

import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services import game_graph, template_import
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import normalize, parse_toml, validate

from .headless import build, needs_browser, open_game, read_data

FIXTURE = "apps/game_generation/games_toml_files/engine_skill_test_fixes_2026_09_30.toml"
PLAIN = "apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml"


def _raw():
    return parse_toml(FIXTURE)


def _canvas(raw, cid):
    return next(c for c in raw["canvases"] if c["id"] == cid)


def _graph(raw=None):
    return build_game_graph(normalize(raw if raw is not None else _raw()))


def _twee(raw=None, path=None):
    graph = build_game_graph(normalize(raw if raw is not None else parse_toml(path or FIXTURE)))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def _errors(raw):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return validate(normalize(raw))


# ── 1. the four hops: dataclass, parser, both writers ─────────────────────────


def test_the_keys_reach_the_graph():
    graph = _graph()
    trig = {c.metadata.get("slug"): c.trigger for c in graph.canvases
            if getattr(c, "trigger", None) is not None and hasattr(c, "trigger")}
    meta = trig["step_offer"].metadata
    assert meta["consume_on"] == "exit"
    assert meta["retry_after_days"] == 2
    assert "consume_on" not in trig["step_plain"].metadata
    assert "retry_after_days" not in trig["step_plain"].metadata


def test_the_choice_decisions_reach_the_graph():
    graph = _graph()
    offer = next(c for c in graph.canvases if c.metadata.get("slug") == "step_offer")
    ask = next(n for n in graph.node_by_id.values()
               if n.canvas is offer and (n.node_data or {}).get("slug") == "ask")
    by_text = {ch["text"]: ch for ch in ask.exit_block["choices"]}
    assert by_text["Yes."]["consumes"] is True
    assert by_text["Not tonight."]["retry_after_days"] == 3
    assert by_text["Never. (ends his path)"]["final"] is True
    undecided = by_text["Think about it"]
    assert not {"consumes", "final", "retry_after_days"} & set(undecided)


def test_both_writers_carry_every_key():
    """create_project_from_template (DB) and build_game_graph (no-DB) keep near-identical
    loops; a key forgotten in one evaporates with no error anywhere."""
    for mod in (game_graph, template_import):
        src = inspect.getsource(mod)
        for needle in (
            '"consume_on": c.trigger.consume_on or None',
            '"retry_after_days": c.trigger.retry_after_days',
            'ch_d["consumes"] = True',
            'ch_d["final"] = True',
            'ch_d["retry_after_days"] = ch.retry_after_days',
            "closed_step_flags(template)",
        ):
            assert needle in src, f"{mod.__name__} lacks {needle}"


def test_the_closed_flag_is_declared_false():
    graph = _graph()
    assert "step_offer_closed" in graph.player.flag_keys


# ── 2. the validator ──────────────────────────────────────────────────────────


def test_the_fixture_is_clean():
    assert _errors(_raw()) == []


def _mutate(fn):
    raw = _raw()
    fn(raw)
    return _errors(raw)


@pytest.mark.parametrize(
    "mutation, fragment",
    [
        (lambda r: _canvas(r, "step_offer")["trigger"].update(consume_on="enter"),
         'consume_on must be "exit"'),
        (lambda r: _canvas(r, "step_offer")["trigger"].update(is_repeatable=True),
         "needs is_repeatable = false"),
        (lambda r: _canvas(r, "step_offer")["trigger"].update(retry_after_days=0),
         "whole number of days >= 1"),
        (lambda r: _canvas(r, "step_plain")["trigger"].update(retry_after_days=2),
         "read only with consume_on"),
        (lambda r: _canvas(r, "step_plain")["nodes"][0].update(exit_block={
            "type": "choices",
            "choices": [{"text": "Yes", "targetType": "location",
                         "locationId": "loc_home", "consumes": True}]}),
         "is read only on a canvas whose trigger has"),
        (lambda r: _canvas(r, "step_offer")["nodes"][0]["exit_block"]["choices"][0]
         .update(final=True),
         "set only one of consumes / final / retry_after_days"),
        (lambda r: _canvas(r, "step_offer")["nodes"][0]["exit_block"]["choices"][1]
         .update(retry_after_days="3"),
         "whole number of days >= 1"),
    ],
)
def test_misuse_is_an_error(mutation, fragment):
    errs = _mutate(mutation)
    assert any(fragment in e for e in errs), errs


def test_a_step_nothing_uses_up_warns():
    raw = _raw()
    for ch in _canvas(raw, "step_offer")["nodes"][0]["exit_block"]["choices"]:
        ch.pop("consumes", None)
        ch.pop("final", None)
    with pytest.warns(UserWarning, match="never used up"):
        validate(normalize(raw))


# ── 3. inert without the key ──────────────────────────────────────────────────


def test_a_game_without_the_key_emits_none_of_the_per_game_pieces():
    twee = _twee(path=PLAIN)
    assert '"consumeOn": ' not in twee
    assert '"canvas_state"' not in twee
    assert "setup.parkLeftCanvasSteps(psg)" not in twee
    assert "setup.decideCanvasStep(" not in twee.split("setup.decideCanvasStep = ", 1)[-1]


def test_passages_are_unchanged_for_a_game_without_the_key():
    """§0 rule 7: the passage text of a game that does not use the key is unchanged.
    Only the engine script moved (the shared "done" helpers). Guarded by the fixture
    building with no decision script in any passage and no canvas_state in Start."""
    twee = _twee(path=PLAIN)
    passages = [p for p in twee.split("\n:: ") if "[script]" not in p.split("\n", 1)[0]]
    assert not any("decideCanvasStep" in p or "canvas_state" in p for p in passages)


def test_the_leave_default_is_one_day_when_absent():
    raw = _raw()
    del _canvas(raw, "step_offer")["trigger"]["retry_after_days"]
    twee = _twee(raw)
    assert '"consumeOn": "exit", "retryAfterDays": 1' in twee


# ── 4. behaviour, in the real engine ─────────────────────────────────────────


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("en1") / "out")


def _enter_step(g):
    assert g.play("Location_loc_bar") == "Canvas_step_offer_Node_ask"
    assert g.sv("game_state.canvas_state.step_offer.open") is True


def _offered(g):
    return g.js("() => SugarCube.setup.canTriggerCanvas('step_offer', false, null)")


def _today(g):
    return g.sv("game_state.time_state.day")


@needs_browser
def test_yes_uses_the_step_up_for_good(html):
    with open_game(html) as g:
        _enter_step(g)
        g.click("Yes.")
        assert g.passage() == "Canvas_step_offer_Node_after"
        g.click("Go home")
        rec = g.sv("game_state.canvas_state.step_offer")
        assert rec["consumed"] is True and rec["open"] is False and rec["retryDay"] is None
        g.advance_days(30)
        assert _offered(g) is False
        assert g.play("Location_loc_bar") == "Location_loc_bar"  # nothing auto-fires
        assert g.errors == []


@needs_browser
def test_a_parked_no_returns_after_its_days(html):
    with open_game(html) as g:
        _enter_step(g)
        day = _today(g)
        g.click("Not tonight.")
        assert g.passage() == "Location_loc_home"
        rec = g.sv("game_state.canvas_state.step_offer")
        assert rec["retryDay"] == day + 3 and rec["consumed"] is False
        g.advance_days(2)
        assert _offered(g) is False
        g.advance_days(1)
        assert _offered(g) is True
        assert g.play("Location_loc_bar") == "Canvas_step_offer_Node_ask"
        assert g.errors == []


@needs_browser
def test_leaving_by_nav_mid_scene_parks_for_the_canvas_default(html):
    with open_game(html) as g:
        _enter_step(g)
        day = _today(g)
        g.play("Location_loc_home")  # walk out without answering
        rec = g.sv("game_state.canvas_state.step_offer")
        assert rec["open"] is False and rec["retryDay"] == day + 2
        assert _offered(g) is False
        g.advance_days(2)
        assert _offered(g) is True


@needs_browser
def test_leaving_through_an_undecided_choice_parks_too(html):
    with open_game(html) as g:
        _enter_step(g)
        day = _today(g)
        g.click("Think about it")
        assert g.passage() == "Canvas_step_offer_Node_think"
        assert g.sv("game_state.canvas_state.step_offer.open") is True  # still inside
        g.click("Go home")
        assert g.sv("game_state.canvas_state.step_offer.retryDay") == day + 2


@needs_browser
def test_an_info_page_is_not_a_leave(html):
    with open_game(html) as g:
        _enter_step(g)
        g.play("StatsPage")
        rec = g.sv("game_state.canvas_state.step_offer")
        assert rec["open"] is True and rec["retryDay"] is None


@needs_browser
def test_the_final_no_closes_and_sets_the_flag(html):
    with open_game(html) as g:
        _enter_step(g)
        assert g.sv("flags.step_offer_closed") is False
        g.click("Never. (ends his path)")
        rec = g.sv("game_state.canvas_state.step_offer")
        assert rec["consumed"] is True and rec["closed"] is True
        assert g.sv("flags.step_offer_closed") is True
        g.advance_days(30)
        assert _offered(g) is False
        assert g.js(
            "() => SugarCube.setup.isCanvasSelectable(SugarCube.setup.getCanvasById('after_closed'))"
        ) is True


@needs_browser
def test_the_done_readers_follow_the_record(html):
    """isCanvasNew and _isCanvasAvailable read the same rule as canTriggerCanvas."""
    with open_game(html) as g:
        c = "SugarCube.setup.getCanvasById('step_offer')"
        _enter_step(g)
        g.click("Not tonight.")
        assert g.js(f"() => SugarCube.setup.isCanvasNew('step_offer')") is True
        assert g.js(f"() => SugarCube.setup._isCanvasAvailable({c})") is False
        g.advance_days(3)
        assert g.js(f"() => SugarCube.setup._isCanvasAvailable({c})") is True
        g.play("Location_loc_bar")
        g.click("Yes.")
        assert g.js(f"() => SugarCube.setup.isCanvasNew('step_offer')") is False
        assert g.js(f"() => SugarCube.setup.canvasConsumedById('step_offer')") is True


@needs_browser
def test_a_plain_one_time_canvas_is_still_used_up_on_entry(html):
    """The control: no key, today's behaviour."""
    with open_game(html) as g:
        g.js("() => { SugarCube.State.variables.flags.started = true; }")
        assert g.play("Location_loc_home") == "Canvas_step_plain_Node_only"
        g.click("Back")
        g.advance_days(30)
        assert g.js("() => SugarCube.setup.canTriggerCanvas('step_plain', false, null)") is False
        assert g.sv("game_state.canvas_state.step_plain") is None


@needs_browser
def test_max_triggers_per_day_is_unchanged(html):
    with open_game(html) as g:
        can = "() => SugarCube.setup.canTriggerCanvas('after_closed', true, 1)"
        assert g.js(can) is True
        g.js("() => SugarCube.setup.markCanvasTriggered('after_closed')")
        assert g.js(can) is False
        # an opted-in step answers to the same per-day cap once it is offerable again
        g.js("() => { SugarCube.State.variables.game_state.trigger_history.step_offer ="
             " {total: 1, dayKey: SugarCube.setup.getCurrentDayKey(), dayCount: 1};"
             " SugarCube.State.variables.game_state.canvas_state.step_offer ="
             " {consumed: false, retryDay: null, closed: false, open: false}; }")
        assert g.js("() => SugarCube.setup.canTriggerCanvas('step_offer', false, 1)") is False
        assert g.js("() => SugarCube.setup.canTriggerCanvas('step_offer', false, null)") is True


@needs_browser
def test_a_save_made_before_en1_reads_the_fired_step_as_used_up(html):
    """§0 rule 8. The save string was written by the PRE-change engine: `git archive
    main` of this repo (before EN1), the fixture built with it (minus the
    after_closed canvas, whose flag the old engine cannot see), then played headless:
    Engine.play Location_loc_bar (step_offer fires: trigger_history total 2) and
    Location_loc_home, then Save.serialize(). It has no canvas_state at all."""
    with open_game(html) as g:
        assert g.load_save(read_data("en1_pre_change_save.txt")) is True
        assert g.passage() == "Location_loc_home"
        assert g.sv("game_state.trigger_history.step_offer.total") >= 1
        assert g.sv("game_state.canvas_state") == {}  # backfilled, no record
        g.advance_days(30)
        assert _offered(g) is False
        assert g.play("Location_loc_bar") == "Location_loc_bar"
        assert g.errors == []
