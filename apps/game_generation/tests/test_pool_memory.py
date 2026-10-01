"""E2 (World and Systems PRD) — event pools that remember what she has seen.

Before this, a `block_pool` picked `random(0, n-1)` on every render and a random
canvas rolled its flat `chance` for ever, so a pool of twenty events showed the same
three twice before the other seventeen once. Two opt-in keys:

  * `block_pool` props `memory = "seen"` (optional `seen_weight`, default 0.1): an entry
    already shown weighs `seen_weight` against 1 for a fresh one. What she has seen is
    kept in `$game_state.pool_seen[key]` (index -> times shown), keyed by the pool's
    `id`, else a hash of its entries (the `_media_pool_key` idea).
  * a random canvas's `trigger.seen_weight`: once it has fired
    (`trigger_history[id].total > 0`) its `chance` is multiplied by it.

Old saves: `pool_seen` is in the skeleton (and so `setup.stateDefaults`) only for a game
that has a remembering pool, and the :passagestart backfill fills it into a save written
before. Proven by loading a save string a pre-change build wrote
(tests/data/e2_pre_change_save.txt; how it was made is in that test's docstring).

    pytest apps/game_generation/tests/test_pool_memory.py -q
"""
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

FIXTURE = "apps/game_generation/games_toml_files/engine_ws_batch1_2026_10_01.toml"
PLAIN = "apps/game_generation/games_toml_files/engine_prd_phase2_2026_04_29.toml"


def _raw(path=FIXTURE):
    return parse_toml(path)


def _canvas(raw, cid):
    return next(c for c in raw["canvases"] if c["id"] == cid)


def _twee(raw=None, path=FIXTURE):
    graph = build_game_graph(normalize(raw if raw is not None else parse_toml(path)))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def _errors(raw):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return validate(normalize(raw))


# ── 1. the field route ────────────────────────────────────────────────────────


def test_seen_weight_reaches_the_graph():
    graph = build_game_graph(normalize(_raw()))
    trig = {c.metadata.get("slug"): c.trigger for c in graph.canvases
            if getattr(c, "trigger", None) is not None}
    assert trig["random_seen"].metadata["seen_weight"] == 0.5
    assert "seen_weight" not in trig["random_plain"].metadata


def test_both_writers_carry_seen_weight():
    for mod in (game_graph, template_import):
        assert '"seen_weight": c.trigger.seen_weight' in inspect.getsource(mod), mod.__name__


def test_the_payload_carries_seen_weight_only_where_set():
    twee = _twee()
    assert twee.count('"seenWeight": 0.5') == 1


def test_the_remembering_pools_emit_the_weighted_pick():
    twee = _twee()
    assert 'setup.pickRememberedPoolEntry("home_pool", 3, 0.1)' in twee
    assert ', 2, 0.25)' in twee  # the hashed pool, its own weight
    assert "<<set _bp to random(0, 2)>>" in twee  # the control pool is untouched


def test_the_top_level_shape_remembers_too():
    """`blocks` may sit at the block's top level or in props; so may the memory keys."""
    raw = _raw()
    node = _canvas(raw, "pool_hashed")["nodes"][0]
    inner = node["blocks"][0]["props"]["blocks"]
    node["blocks"] = [{"type": "block_pool", "id": "top", "memory": "seen",
                       "seen_weight": 0.5, "blocks": inner}]
    assert _errors(raw) == []
    assert 'setup.pickRememberedPoolEntry("top", 2, 0.5)' in _twee(raw)


# ── 2. the validator ──────────────────────────────────────────────────────────


def test_the_fixture_is_clean():
    assert _errors(_raw()) == []


def _pool(raw, cid="pool_room", i=0):
    return _canvas(raw, cid)["nodes"][0]["blocks"][i]["props"]


@pytest.mark.parametrize(
    "mutation, fragment",
    [
        (lambda r: _canvas(r, "random_seen")["trigger"].update(seen_weight=0),
         "must be a number in (0, 1]"),
        (lambda r: _canvas(r, "random_seen")["trigger"].update(seen_weight=1.5),
         "must be a number in (0, 1]"),
        (lambda r: _canvas(r, "pool_room")["trigger"].update(seen_weight=0.5),
         'read only with trigger_mode = "random"'),
        (lambda r: _pool(r).update(memory="all"), 'memory must be "seen"'),
        (lambda r: _pool(r, i=1).update(seen_weight=0.5), 'read only with memory = "seen"'),
        (lambda r: _pool(r).update(seen_weight="low"), "must be a number in (0, 1]"),
    ],
)
def test_misuse_is_an_error(mutation, fragment):
    raw = _raw()
    mutation(raw)
    errs = _errors(raw)
    assert any(fragment in e for e in errs), errs


# ── 3. inert without the keys ─────────────────────────────────────────────────


def test_a_game_without_the_keys_has_no_pool_seen_and_no_seen_weight():
    twee = _twee(path=PLAIN)
    assert '"pool_seen"' not in twee
    assert '"seenWeight"' not in twee
    passages = [p for p in twee.split("\n:: ") if "[script]" not in p.split("\n", 1)[0]]
    assert not any("pickRememberedPoolEntry" in p for p in passages)


def test_the_pool_seen_default_reaches_the_backfill():
    twee = _twee()
    defaults = twee.split("setup.stateDefaults = ", 1)[1].split("\n", 1)[0]
    assert '"pool_seen": {}' in defaults


# ── 4. behaviour, in the real engine ─────────────────────────────────────────


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("e2") / "out")


def _text(g):
    return g.js("() => document.querySelector('.passage').textContent")


@needs_browser
def test_each_entry_is_shown_once_before_any_repeats(html):
    """Exact draws. A plain pool with draws 0.99, 0.95, 0.80 shows entry 2 three times
    (random(0, 2) = floor(x * 3)). The remembering pool shows 2, then 1, then 0: after
    entry 2 is seen it weighs 0.1, so 0.95 of the total (1.995 of 2.1) falls in entry 1's
    band, and 0.80 of 1.2 (0.96) in entry 0's."""
    with open_game(html) as g:
        picks = g.js("""() => {
            const draws = [0.99, 0.95, 0.80];
            Math.random = () => draws.shift();
            const s = SugarCube.setup;
            return [s.pickRememberedPoolEntry('k', 3, 0.1),
                    s.pickRememberedPoolEntry('k', 3, 0.1),
                    s.pickRememberedPoolEntry('k', 3, 0.1)];
        }""")
        assert picks == [2, 1, 0]
        assert g.sv("game_state.pool_seen.k") == {"0": 1, "1": 1, "2": 1}
        assert g.errors == []


@needs_browser
def test_playing_the_pool_records_the_entry_it_shows(html):
    with open_game(html) as g:
        for n in range(1, 5):
            g.play("Canvas_pool_room_Node_look")
            text = _text(g)
            shown = [i for i, m in enumerate(("REMEMBERED_A", "REMEMBERED_B", "REMEMBERED_C"))
                     if m in text]
            assert len(shown) == 1
            seen = g.sv("game_state.pool_seen.home_pool")
            assert sum(seen.values()) == n
            assert seen[str(shown[0])] >= 1
        assert g.errors == []


@needs_browser
def test_a_random_canvas_halves_once_seen(html):
    with open_game(html) as g:
        chance = "(id) => SugarCube.setup.canvasRollChance(SugarCube.setup.getCanvasById(id))"
        assert g.js(chance, "random_seen") == 1.0
        g.js("() => SugarCube.setup.markCanvasTriggered('random_seen')")
        assert g.js(chance, "random_seen") == 0.5
        g.js("() => SugarCube.setup.markCanvasTriggered('random_plain')")
        assert g.js(chance, "random_plain") == 1.0
        assert g.errors == []


@needs_browser
def test_a_save_made_before_e2_gets_pool_seen(html):
    """The save string was written by the PRE-change engine: `git archive` of the
    commit before E2 (72cb456), this fixture built with it (that engine ignores
    `memory` and `seen_weight`, so both pools are plain random), then played headless:
    Engine.play Canvas_pool_room_Node_look and Location_loc_home, then
    Save.serialize(). Its $game_state has no pool_seen."""
    with open_game(html) as g:
        assert g.load_save(read_data("e2_pre_change_save.txt")) is True
        assert g.passage() == "Location_loc_home"
        assert g.sv("game_state.pool_seen") == {}  # backfilled
        g.play("Canvas_pool_room_Node_look")
        seen = g.sv("game_state.pool_seen.home_pool")
        assert sum(seen.values()) == 1
        assert g.errors == []
