"""EN2a — the bill rises in stages, and the collector says so.

PRD_SKILL_TEST_FIXES_v2 §2 EN2a (D8c · I5). Before this, rent was one number for the
whole game: `setup.rent_amount`, read by RentDay for the greeting, the "Rent is" line,
the affordability check and the deduction, and by RentDay_Short for "You need".

Opt-in by `[settings.rent] stages = [{amount, after_total_paid}]` (+ `stage_lines`):

  * `$game_state.rent_state.total_paid` counts every payment;
  * `setup.currentRent()` is the amount of the last stage whose after_total_paid is
    reached, or `amount` before the first one — every read uses it;
  * when a payment moves the stage, the collector says `stage_lines[i]` on the pay
    screen (RentDay_Paid). A reload of that screen shows the same line.

A game without `stages` builds its three RentDay passages byte-identical to the engine
before EN2a (the golden in tests/data was written by that engine).

Old saves (§0 rule 8): the backfill gives `total_paid = 0`, so an old save restarts at
the first stage. Proven with a save string the pre-change build wrote.

    pytest apps/game_generation/tests/test_rent_stages.py -q
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
RENT_PASSAGES = ("RentDay", "RentDay_Paid", "RentDay_Short")
LINE_1 = "It's one-fifty from now on. The place costs more than you do."
LINE_2 = "Two hundred. Don't look at me like that, you knew it would climb."


def _raw():
    return parse_toml(FIXTURE)


def _unstaged():
    raw = _raw()
    del raw["settings"]["rent"]["stages"]
    del raw["settings"]["rent"]["stage_lines"]
    return raw


def _graph(raw):
    return build_game_graph(normalize(raw))


def _twee(raw):
    graph = _graph(raw)
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


def _rent_passages(twee):
    return "".join(
        "\n:: " + p
        for p in twee.split("\n:: ")
        if p.split("\n", 1)[0].split(" ")[0] in RENT_PASSAGES
    )


def _errors(raw):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        return validate(normalize(raw))


# ── 1. the hops: parser, dataclass, the one shared metadata writer ────────────


def test_the_keys_reach_the_template_and_the_graph():
    """Both paths write rent through `_assemble_project_metadata` (template_import.py;
    game_graph.py calls it), so the graph's project metadata is the DB writer's too."""
    t = normalize(_raw())
    assert t.rent_stages == [
        {"amount": 150, "after_total_paid": 100},
        {"amount": 200, "after_total_paid": 250},
    ]
    assert t.rent_stage_lines == [LINE_1, LINE_2]
    rs = _graph(_raw()).project.metadata["rent_settings"]
    assert rs["stages"] == t.rent_stages
    assert rs["stage_lines"] == [LINE_1, LINE_2]


def test_an_unstaged_game_writes_no_new_metadata():
    rs = _graph(_unstaged()).project.metadata["rent_settings"]
    assert "stages" not in rs and "stage_lines" not in rs


def test_the_fixture_is_clean():
    assert _errors(_raw()) == []


def _mutate(fn):
    raw = _raw()
    fn(raw["settings"]["rent"])
    return _errors(raw)


@pytest.mark.parametrize(
    "mutation, fragment",
    [
        (lambda r: r.update(stages=[{"amount": 0, "after_total_paid": 100}]),
         "stages[0].amount must be a positive integer"),
        (lambda r: r.update(stages=[{"amount": 150, "after_total_paid": -1}]),
         "stages[0].after_total_paid must be an integer >= 0"),
        (lambda r: r.update(stages=[{"amount": 150}]),
         "stages[0].after_total_paid must be an integer >= 0"),
        (lambda r: r.update(stages=[{"amount": 150, "after_total_paid": 100, "when": 1}]),
         "has unknown key(s) ['when']"),
        (lambda r: r.update(stages=[{"amount": 150, "after_total_paid": 250},
                                    {"amount": 200, "after_total_paid": 250}]),
         "must be greater than the stage before it (250)"),
        (lambda r: r.update(stages=["150"]), "stages[0] must be a table"),
        (lambda r: r.update(stages={"amount": 150}), "rent stages must be a list"),
        (lambda r: (r.pop("stages"), r.update(stage_lines=["x"])),
         "stage_lines is set but stages is not"),
        (lambda r: r.update(stage_lines=["a", "b", "c"]),
         "stage_lines has 3 lines for 2 stages"),
        (lambda r: r.update(stage_lines=["a", 2]), "stage_lines[1] must be a string"),
    ],
)
def test_misuse_is_an_error(mutation, fragment):
    errs = _mutate(mutation)
    assert any(fragment in e for e in errs), errs


# ── 2. emitted only when used ────────────────────────────────────────────────


def test_an_unstaged_game_has_the_rent_passages_it_had_before():
    """§0 rule 7. The golden is the three RentDay passages the engine BEFORE EN2a
    generated for this fixture with stages/stage_lines removed (`git archive HEAD` of
    419d7ec, run from scratch)."""
    golden = read_data("en2a_rentday_unstaged_golden.txt")
    assert _rent_passages(_twee(_unstaged())).strip() == golden


def test_an_unstaged_game_emits_none_of_the_staged_pieces():
    twee = _twee(_unstaged())
    for piece in ("setup.currentRent", "setup.rent_stages", "recordRentPayment",
                  "rentStageLine", '"total_paid"'):
        assert piece not in twee, piece


def test_a_staged_game_reads_the_current_rent_everywhere():
    passages = _rent_passages(_twee(_raw()))
    assert "setup.rent_amount" not in passages
    assert passages.count("setup.currentRent()") == 2  # RentDay + RentDay_Short


# ── 3. behaviour, in the real engine ─────────────────────────────────────────


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    return build(FIXTURE, tmp_path_factory.mktemp("en2a") / "out")


@pytest.fixture(scope="module")
def unstaged_html(tmp_path_factory):
    # The fixture's own text minus the two keys (no TOML writer is installed).
    text = re.sub(r"^stages\s*=.*?\]\n", "", open(FIXTURE).read(), flags=re.S | re.M)
    text = re.sub(r"^stage_lines\s*=.*?\]\n", "", text, flags=re.S | re.M)
    assert "stages" not in text.split("[settings.rent]")[1].split("[[npcs]]")[0]
    out = tmp_path_factory.mktemp("en2a_plain")
    toml = out / "fixture.toml"
    toml.write_text(text)
    return build(toml, out / "out")


def _rent_day(g, money=1000):
    """Make rent due and walk into a location, as the day roll + intercept do."""
    g.js("""(m) => { const v = SugarCube.State.variables;
        v.flags.rent_on = true; v.player.core_traits.money = m;
        v.game_state.rent_state.is_due = true; }""", money)
    g.play("Location_loc_home", settle=300)
    assert g.passage() == "RentDay"


def _text(g):
    return g.js("() => document.querySelector('.passage').innerText")


def _pay(g, amount):
    g.click(f"Pay ${amount} rent")
    assert g.passage() == "RentDay_Paid"


@needs_browser
def test_the_bill_climbs_100_150_200_and_the_collector_says_so(html):
    with open_game(html) as g:
        expected = [(100, 100, LINE_1), (150, 250, LINE_2), (200, 450, None), (200, 650, None)]
        for amount, total, line in expected:
            _rent_day(g)
            assert g.js("() => SugarCube.setup.currentRent()") == amount
            text = _text(g)
            assert f"Rent. ${amount}." in text and f"Rent is ${amount}." in text
            _pay(g, amount)
            assert g.sv("player.core_traits.money") == 1000 - amount
            assert g.sv("game_state.rent_state.total_paid") == total
            paid = _text(g)
            if line:
                assert f"Tobin {line}" in paid
            else:
                assert LINE_1 not in paid and LINE_2 not in paid
        assert g.errors == []


@needs_browser
def test_a_reload_of_the_pay_screen_keeps_the_line(html):
    with open_game(html) as g:
        _rent_day(g)
        _pay(g, 100)
        g.play("RentDay_Paid")
        assert LINE_1 in _text(g)
        assert g.sv("game_state.rent_state.total_paid") == 100  # a render never pays
        assert g.errors == []


@needs_browser
def test_the_short_screen_quotes_the_current_rent(html):
    with open_game(html) as g:
        _rent_day(g)
        _pay(g, 100)
        _rent_day(g, money=20)
        g.click("Tell them you can't pay")
        assert g.passage() == "RentDay_Short"
        assert "You need: $150." in _text(g)
        assert g.errors == []


@needs_browser
def test_without_stages_the_bill_stays_fixed(unstaged_html):
    with open_game(unstaged_html) as g:
        for _ in range(3):
            _rent_day(g)
            _pay(g, 100)
            assert g.sv("player.core_traits.money") == 900
            assert g.sv("game_state.rent_state.total_paid") is None
        assert g.js("() => typeof SugarCube.setup.currentRent") == "undefined"
        assert g.errors == []


@needs_browser
def test_a_save_made_before_en2a_restarts_at_the_first_stage(html):
    """§0 rule 8. The save string was written by the PRE-change engine: `git archive
    HEAD` of this repo at 419d7ec (EN1, before EN2a), the fixture built with it minus
    stages/stage_lines, then played headless — the start canvas, rent made due with
    money 500, Location_loc_home (redirects to RentDay), "Pay $100 rent", then
    Save.serialize() on RentDay_Paid. Its rent_state has no total_paid."""
    with open_game(html) as g:
        assert g.load_save(read_data("en2a_pre_change_save.txt")) is True
        assert g.passage() == "RentDay_Paid"
        assert g.sv("player.core_traits.money") == 400
        assert g.sv("game_state.rent_state.total_paid") == 0  # backfilled
        assert g.sv("game_state.rent_state.stage") == 0
        assert LINE_1 not in _text(g)
        assert g.js("() => SugarCube.setup.currentRent()") == 100
        _rent_day(g)
        _pay(g, 100)
        assert g.sv("game_state.rent_state.total_paid") == 100
        assert LINE_1 in _text(g)
        assert g.errors == []
