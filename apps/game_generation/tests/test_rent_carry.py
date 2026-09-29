"""EN2b — carried debt, no game over.

PRD_SKILL_TEST_FIXES_v2 §2 EN2b (D8d). Before this, a short rent week gave a grace
warning, and the next one ended the game (`eviction_mode = "game_end"`) or set the
eviction flag (`"flag_set"`), RentDay_Short in v2.py.

Opt-in by `[settings.rent] on_short = "carry"`:

  * RentDay asks for this week's rent plus `$game_state.rent_state.owed`, and says
    "Owed from last week: N" when there is any;
  * she may pay what she has ("Pay the $N you have") or nothing; `setup.carryRent`
    takes it, writes the rest to `owed`, and sets the player flag `rent_carried`;
  * RentDay_Short only reports it — no warning count, no eviction, no GAME OVER;
  * a full payment clears `owed`.

`grace_periods` and `eviction_mode` are ignored under carry; the validator warns when
the TOML sets either. The `amount` error is relaxed when `stages` is given (then the first
stage must start at total 0).

The fixture is left without `on_short`, so the EN2a tests keep their grace screen; the
carry build is the fixture's own text with the one line added.

Old saves (§0 rule 8): `owed` and `short_paid` backfill as 0. Proven with a save the
pre-change build wrote after a grace warning.

    pytest apps/game_generation/tests/test_rent_carry.py -q
"""
import warnings

import pytest

from apps.game_generation.twee_comprehensive.generators.v2 import (
    TweeComprehensiveGeneratorV2,
)
from apps.projects.services.game_graph import build_game_graph
from apps.projects.services.template_import import (
    RENT_CARRIED_FLAG,
    normalize,
    parse_toml,
    rent_carries,
    validate,
)

from .headless import build, needs_browser, open_game, read_data
from .test_rent_stages import FIXTURE, LINE_1, _rent_day, _rent_passages, _text

CARRY_LINE = 'on_short         = "carry"\n'


def _carry_text():
    text = open(FIXTURE).read()
    anchor = 'start_after_flag = "rent_on"\n'
    assert text.count(anchor) == 1
    return text.replace(anchor, anchor + CARRY_LINE)


def _raw(carry=True):
    raw = parse_toml(FIXTURE)
    if carry:
        raw["settings"]["rent"]["on_short"] = "carry"
    return raw


def _validate(raw):
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        errors = validate(normalize(raw))
    return errors, [str(w.message) for w in caught]


def _twee(raw):
    graph = build_game_graph(normalize(raw))
    return TweeComprehensiveGeneratorV2().generate(graph.project, {}, graph=graph)


# ── 1. the hops ──────────────────────────────────────────────────────────────


def test_the_key_and_the_flag_reach_the_graph():
    t = normalize(_raw())
    assert t.rent_on_short == "carry" and rent_carries(t)
    graph = build_game_graph(t)
    assert graph.project.metadata["rent_settings"]["on_short"] == "carry"
    assert RENT_CARRIED_FLAG == "rent_carried"
    assert "rent_carried" in graph.player.flag_keys


def test_without_carry_nothing_new_is_written():
    t = normalize(_raw(carry=False))
    assert not rent_carries(t)
    graph = build_game_graph(t)
    assert "on_short" not in graph.project.metadata["rent_settings"]
    assert "rent_carried" not in graph.player.flag_keys
    twee = _twee(_raw(carry=False))
    for piece in ("carryRent", "rent_carried", '"owed"', "Owed from last week"):
        assert piece not in twee, piece


def test_without_carry_the_rent_passages_are_unchanged():
    """§0 rule 7: the fixture's three RentDay passages, as the engine before EN2b (EN2a,
    uncommitted at the time) generated them, are the golden."""
    golden = read_data("en2b_rentday_nocarry_golden.txt")
    assert _rent_passages(_twee(_raw(carry=False))).strip() == golden


def test_the_carry_fixture_is_clean():
    errors, warned = _validate(_raw())
    assert errors == [] and not any("on_short" in w for w in warned), (errors, warned)


# ── 2. the validator ─────────────────────────────────────────────────────────


def _rent_mutated(fn, carry=True):
    raw = _raw(carry)
    fn(raw["settings"]["rent"])
    return _validate(raw)


def test_an_unknown_on_short_is_an_error():
    errors, _ = _rent_mutated(lambda r: r.update(on_short="forgive"))
    assert any("on_short must be 'carry'" in e for e in errors), errors


@pytest.mark.parametrize("key, value", [("grace_periods", 2), ("eviction_mode", "flag_set")])
def test_a_key_carry_ignores_is_warned(key, value):
    errors, warned = _rent_mutated(lambda r: r.update({key: value}))
    assert errors == [], errors
    assert any(f"{key} is ignored when on_short" in w for w in warned), warned


def test_the_same_keys_without_carry_are_not_warned():
    _, warned = _rent_mutated(lambda r: r.update(grace_periods=2), carry=False)
    assert not any("is ignored when on_short" in w for w in warned)


def test_stages_from_zero_need_no_amount():
    def drop_amount(r):
        del r["amount"]
        r["stages"] = [{"amount": 100, "after_total_paid": 0},
                       {"amount": 150, "after_total_paid": 100}]
    errors, _ = _rent_mutated(drop_amount)
    assert errors == [], errors


def test_no_amount_and_a_first_stage_above_zero_is_an_error():
    errors, _ = _rent_mutated(lambda r: r.pop("amount"))
    assert any("stages[0].after_total_paid must be 0" in e for e in errors), errors


def test_no_amount_and_no_stages_is_still_an_error():
    def drop_both(r):
        del r["amount"], r["stages"], r["stage_lines"]
    errors, _ = _rent_mutated(drop_both)
    assert any("rent amount must be a positive integer" in e for e in errors), errors


def test_a_negative_amount_is_still_an_error():
    errors, _ = _rent_mutated(lambda r: r.update(amount=-5))
    assert any("rent amount must be a positive integer" in e for e in errors), errors


# ── 3. behaviour, in the real engine ─────────────────────────────────────────


@pytest.fixture(scope="module")
def html(tmp_path_factory):
    out = tmp_path_factory.mktemp("en2b")
    toml = out / "fixture.toml"
    toml.write_text(_carry_text())
    return build(toml, out / "out")


def _short(g):
    assert g.passage() == "RentDay_Short"
    text = _text(g)
    assert "GAME OVER" not in text
    return text


@needs_browser
def test_a_short_pay_carries_then_a_full_pay_clears_it(html):
    with open_game(html) as g:
        assert g.sv("flags.rent_carried") is False
        _rent_day(g, money=30)
        assert "Pay $100 rent" not in _text(g)
        g.click("Pay the $30 you have")
        text = _short(g)
        assert "You paid: $30. Carried to next week: $70." in text
        assert g.sv("player.core_traits.money") == 0
        assert g.sv("game_state.rent_state.owed") == 70
        assert g.sv("game_state.rent_state.total_paid") == 30
        assert g.sv("flags.rent_carried") is True

        _rent_day(g, money=1000)
        text = _text(g)
        assert "Rent is $170." in text and "Owed from last week: $70." in text
        g.click("Pay $170 rent")
        assert g.passage() == "RentDay_Paid"
        assert g.sv("player.core_traits.money") == 830
        assert g.sv("game_state.rent_state.owed") == 0
        assert g.sv("game_state.rent_state.total_paid") == 200  # past 100: stage 1
        assert LINE_1 in _text(g)
        assert g.sv("flags.rent_carried") is True  # a record, never cleared

        _rent_day(g, money=1000)
        assert "Owed from last week" not in _text(g)
        assert g.errors == []


@needs_browser
def test_three_empty_weeks_pile_up_and_never_end_the_game(html):
    with open_game(html) as g:
        for owed in (100, 200, 300):
            _rent_day(g, money=0)
            assert "Pay the $" not in _text(g)  # nothing to pay with
            g.click("Tell them you can't pay")
            text = _short(g)
            assert f"Carried to next week: ${owed}." in text
            assert g.sv("game_state.rent_state.owed") == owed
            assert g.sv("game_state.rent_state.is_due") is False
        assert g.errors == []


@needs_browser
def test_a_reload_of_the_short_screen_charges_nothing(html):
    with open_game(html) as g:
        _rent_day(g, money=30)
        g.click("Pay the $30 you have")
        g.play("RentDay_Short")
        _short(g)
        assert g.sv("player.core_traits.money") == 0
        assert g.sv("game_state.rent_state.owed") == 70
        assert g.sv("game_state.rent_state.total_paid") == 30
        assert g.errors == []


@needs_browser
def test_a_save_made_before_en2b_carries_instead_of_ending(html):
    """§0 rule 8. Written by the PRE-change engine (EN2a, the working tree before EN2b,
    snapshotted to scratch): the fixture without `on_short` built with it, then played
    headless: rent_on, money 20, rent due, Location_loc_home (RentDay), "Tell them you
    can't pay" (the grace warning: warnings 1), "Continue your day", then Save.serialize()
    on Location_loc_home. Under the old rules its next short week is the eviction."""
    with open_game(html) as g:
        assert g.load_save(read_data("en2b_pre_change_save.txt")) is True
        assert g.passage() == "Location_loc_home"
        assert g.sv("game_state.rent_state.warnings") == 1
        assert g.sv("game_state.rent_state.owed") == 0  # backfilled
        assert g.sv("game_state.rent_state.short_paid") == 0
        _rent_day(g, money=20)
        g.click("Pay the $20 you have")
        assert "Carried to next week: $80." in _short(g)
        assert g.sv("flags.rent_carried") is True
        assert g.errors == []
