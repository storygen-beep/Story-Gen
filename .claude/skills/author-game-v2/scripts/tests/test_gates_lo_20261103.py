"""The gates changed by LO's decisions of 2026-11-03
(`~/Documents/Great_Games_Study_20260926/SKILL_DECISIONS_20261103.md`):

  C5 b · S7  ascent tiers expand the world — declared needs and `"performance": true`
             meters may close more than they open;
  W1 a       meter ceiling — a band above every cap the game pays is a later release's band;
  W12 a      a destination is never open and exit-only — a room whose screen says "nothing to
             do here right now" passes;
  S5 a       no canvas key is discarded — a key under [canvases.trigger.metadata] is flagged;
  S6         the screen-shape lint — a "Nothing happens." random event is not an event;
  C7 c · S11 sex for pay names the amount / her climb — only canvases in the pool of a card
             declared `"sex_for_pay": true` are read, and the price is in the scene;
  S12 b      ends on an opening — tested in test_gates_ws5.py (the cards, not a door).

`a chat is short and timed` (C6 b) is tested in test_gates_chat_short_timed.py.
Fixtures are written here; nothing in games/ is read or written.
"""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.dirname(HERE))
import gates  # noqa: E402
import test_gates_ck7 as ck7  # noqa: E402
import test_gates_nc2 as nc2  # noqa: E402
import test_gates_system_cards as sc  # noqa: E402

V1 = {"version": "1.0", "logic": "AND"}


def row(game, state, name):
    model, g2 = gates.build(copy.deepcopy(game))
    return next(r for r in gates.run_gates(model, g2, state) if r["gate"] == name)


def trait_cond(key, op, value):
    return dict(V1, items=[{"type": "trait", "subject": "player", "trait_key": key,
                            "operator": op, "value": value}])


# ── C5 b · S7: ascent tiers expand the world ─────────────────────────────────
ASCENT = "ascent tiers expand the world"


def descent_game():
    """`heat` opens two doors; `energy` and `grade` each shut two and open none."""
    canv = []
    for i, (key, op, v) in enumerate([("heat", "gte", 10), ("heat", "gte", 20),
                                      ("energy", "lt", 5), ("energy", "lt", 1),
                                      ("grade", "lt", 30), ("grade", "lt", 10)]):
        canv.append({"id": f"c{i}", "trigger": {"location": "room", "is_repeatable": True,
                                                 "conditions": trait_cond(key, op, v)},
                     "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "x"}]}]})
    return {"project": {"id": "fx", "name": "fx"},
            "player": {"core_traits": {"heat": 0, "energy": 50, "grade": 50}},
            "locations": [{"id": "room"}], "canvases": canv}


def test_an_undeclared_need_and_grade_still_fail_as_descents():
    r = row(descent_game(), {"board": {"ascent_tiers": ["heat"]}}, ASCENT)
    assert r["pass_"] is False
    assert any(d.startswith("energy is a player meter") for d in r["detail"])
    assert any(d.startswith("grade is a player meter") for d in r["detail"])


def test_a_declared_need_and_a_performance_meter_are_skipped():
    st = {"board": {"ascent_tiers": ["heat"], "needs": [{"key": "energy"}],
                    "meters": [{"id": "grade", "key": "grade", "kind": "sourced",
                                "performance": True}]}}
    r = row(descent_game(), st, ASCENT)
    assert r["pass_"] is True, r["detail"]


def test_the_old_kind_performance_spelling_is_still_skipped():
    st = {"board": {"ascent_tiers": ["heat"], "needs": [{"key": "energy"}],
                    "meters": [{"id": "grade", "key": "grade", "kind": "performance"}]}}
    assert row(descent_game(), st, ASCENT)["pass_"] is True


def test_a_sourced_grade_is_not_skipped():
    st = {"board": {"ascent_tiers": ["heat"], "needs": [{"key": "energy"}],
                    "meters": [{"id": "grade", "key": "grade", "kind": "sourced"}]}}
    r = row(descent_game(), st, ASCENT)
    assert r["pass_"] is False and any(d.startswith("grade is") for d in r["detail"])


# ── W1 a: meter ceiling ──────────────────────────────────────────────────────
CEILING = "meter ceiling"


def ceiling_game(cap):
    eff = {"targetType": "player", "trait": "heat", "op": "add", "value": 1}
    if cap is not None:
        eff["cap"] = cap
    return {"project": {"id": "fx", "name": "fx"}, "player": {"core_traits": {"heat": 0}},
            "locations": [{"id": "room"}],
            "sidebar_items": [{"trait": "heat", "bands": [
                {"min": 0, "max": 39, "label": "low"}, {"min": 40, "max": 79, "label": "mid"},
                {"min": 80, "label": "top"}]}],
            "canvases": [
                {"id": "earn", "trigger": {"location": "room", "is_repeatable": True},
                 "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "x"}],
                            "exit_block": {"type": "location", "config": {
                                "locationId": "room", "effects": [eff]}}}]},
                {"id": "mid", "trigger": {"location": "room", "is_repeatable": True,
                                          "conditions": trait_cond("heat", "gte", 40)},
                 "nodes": [{"id": "n", "blocks": [{"type": "paragraph", "content": "y"}]}]}]}


def test_an_uncapped_meter_still_promises_its_top_band():
    r = row(ceiling_game(None), None, CEILING)
    assert r["pass_"] is False and "promise something at 80" in r["detail"][0]


def test_a_band_above_every_cap_is_a_later_release():
    assert row(ceiling_game(79), None, CEILING)["pass_"] is True


def test_a_cap_that_reaches_the_band_keeps_the_promise():
    assert row(ceiling_game(80), None, CEILING)["pass_"] is False


# ── W12 a: the room that says it has nothing to do ───────────────────────────
def test_an_empty_open_room_that_says_so_passes():
    loc = {"id": "toilet", "description": "Urinals and a mirror. There's nothing to do here "
                                          "right now."}
    r = ck7.row(ck7.game([loc, {"id": "shop"}], [ck7.canvas("browse", "shop")]))
    assert r["pass_"] is True, r["detail"]


def test_an_empty_open_room_that_does_not_say_so_still_fails():
    loc = {"id": "toilet", "description": "Urinals and a mirror."}
    r = ck7.row(ck7.game([loc, {"id": "shop"}], [ck7.canvas("browse", "shop")]))
    assert r["pass_"] is False and r["detail"][0].startswith("toilet: open with nothing to do")


# ── S5 a: [canvases.trigger.metadata] ────────────────────────────────────────
DISCARD = "no canvas key is discarded"


def test_a_trigger_key_under_metadata_is_flagged():
    c = ck7.canvas("shift", "cafe", metadata={"show_when_blocked": True,
                                              "cooldown_message": "No more shifts today."})
    r = row(ck7.game([{"id": "cafe"}], [c]), None, DISCARD)
    assert r["pass_"] is False
    assert any("`cooldown_message` under [canvases.trigger.metadata] is discarded" in d
               for d in r["detail"])
    assert any("`show_when_blocked`" in d and "move it up one level" in d for d in r["detail"])


def test_the_same_key_on_the_trigger_passes():
    c = ck7.canvas("shift", "cafe", show_when_blocked=True,
                   cooldown_message="No more shifts today.")
    assert row(ck7.game([{"id": "cafe"}], [c]), None, DISCARD)["pass_"] is True


# ── S6: a "Nothing happens." random event ────────────────────────────────────
def test_a_nothing_happens_event_is_not_an_event_and_is_listed():
    quiet = ck7.canvas("quiet", "hall", [{"type": "paragraph", "content": "Nothing happens. "
                                                                         "The fridge hums."}],
                       trigger_mode="random")
    real = ck7.canvas("towel", "hall", [{"type": "paragraph", "content": "He steps out wet."}],
                      trigger_mode="random")
    g = ck7.game([{"id": "hall"}, {"id": "kitchen"}],
                 [quiet, ck7.canvas("k_quiet", "kitchen", [{"type": "paragraph", "content":
                                                            "Nothing happens."}],
                                    trigger_mode="random")])
    model, g2 = gates.build(copy.deepcopy(g))
    summary, out = gates.lint_screen_shape(model, g2)
    assert "0/2 carry a random event" in summary
    assert {h["id"] for h in out if h["kind"] == "empty event"} == {"quiet", "k_quiet"}
    g["canvases"].append(real)
    model, g2 = gates.build(copy.deepcopy(g))
    assert "1/2 carry a random event" in gates.lint_screen_shape(model, g2)[0]


# ── C7 c · S11: sex for pay is a declared system ─────────────────────────────
def paid_state(pool=("backroom",)):
    card = sc.card(id="backroom_trade", pool=list(pool), sex_for_pay=True)
    return {"board": {"economy": {"currency": "money"}, "systems": [card]}}


def paid_game(scene="He fucks her, his cock deep in her wet cunt, and she comes.",
              button="Take it."):
    g = sc.hot_game()
    node = g["canvases"][-1]["nodes"][0]
    node["blocks"][0]["content"] = scene
    node["exit_block"] = {"choices": [
        {"text": button, "effects": [{"trait": "money", "op": "add", "value": 100}]}]}
    return g


def paid(game, state):
    model, g2 = gates.build(copy.deepcopy(game))
    return gates._paid_choice_names_amount(model, g2, state)


def test_no_declared_sex_for_pay_card_is_na():
    ok, head, _ = paid(paid_game(), {"board": {"economy": {"currency": "money"}}})
    assert ok is None and "sex_for_pay" in head


def test_a_wage_off_the_declared_pool_is_not_read():
    ok, head, _ = paid(paid_game(), paid_state(pool=("other_scene",)))
    assert ok is None and "no paid choice on a declared sex-for-pay scene" in head


def test_the_price_said_in_the_scene_passes():
    scene = ("\"A hundred,\" he says, before you answer. He fucks her, his cock deep in her "
             "wet cunt, and she comes.")
    assert paid(paid_game(scene=scene), paid_state())[0] is True


def test_a_price_only_on_the_button_does_not_count():
    ok, _, d = paid(paid_game(button="Take the $100."), paid_state())
    assert ok is False and "the scene names no price before her yes" in d[0]


def test_her_climb_is_na_with_no_sex_for_pay_card():
    ok, head, _d, _n = gates._her_climb(copy.deepcopy(nc2.game()), nc2.STATE_NO_SFP)
    assert ok is None and "sex_for_pay" in head


def test_her_climb_skips_a_paid_repeatable_off_the_pool():
    st = copy.deepcopy(nc2.STATE)
    st["board"]["systems"][0]["pool"] = ["elsewhere"]
    ok, head, _d, _n = gates._her_climb(copy.deepcopy(nc2.game()), st)
    assert ok is None and head.startswith("no paid repeatable")
