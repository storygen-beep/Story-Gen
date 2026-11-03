"""The system floors and the price of a paid act (World and Systems PRD, Phase 6B, 2026-10-02).
Both WARNs: scored gates, never `--ship` blocks.

  a system meets its floors — a daily card's pool holds ≥20 canvases that exist in the build; a
      lewd ladder has ≥4 rungs and each rung ≥2 acts. n/a with no card.
  sex for pay names the amount — a paying choice on an explicit canvas of a declared sex-for-pay
      system card (`"sex_for_pay": true`, its `pool[]`) sits in a scene that names a figure or an
      amount in words. n/a when no card is declared or no such choice exists (C7 c + S11).
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gates  # noqa: E402
import test_gates_system_cards as sc  # noqa: E402
import test_gates_ws6 as ws6  # noqa: E402

RUNG = {"gate": "start", "acts": ["a look", "a word"]}


def floors(card, extra=0):
    g = ws6.green_game()
    for k in range(extra):
        g["canvases"].append({"id": f"p{k}", "trigger": {"location": "work"},
                              "nodes": [{"id": "n", "blocks": []}]})
    model, _ = gates.build(g)
    return gates._system_floors(model, sc.state_with(card))


def test_a_full_card_passes():
    card = sc.card(daily=True, pool=[f"p{k}" for k in range(20)], lewd_ladder=[RUNG] * 4)
    assert floors(card, extra=20)[0] is True


def test_a_daily_pool_counts_only_built_canvases():
    card = sc.card(daily=True, pool=[f"p{k}" for k in range(25)], lewd_ladder=[RUNG] * 4)
    ok, _, d = floors(card, extra=19)
    assert ok is False and "19 built" in d[0]


def test_few_rungs_and_thin_rungs_warn():
    ok, _, d = floors(sc.card(lewd_ladder=[RUNG, {"gate": "late", "acts": ["one"]}]))
    assert ok is False and "2 lewd rung(s)" in d[0] and "late" in d[1]


def test_not_daily_skips_the_pool_and_no_card_is_na():
    assert floors(sc.card(lewd_ladder=[RUNG] * 4))[0] is True
    model, _ = gates.build(ws6.green_game())
    assert gates._system_floors(model, sc.state_with())[0] is None


def paid(said):
    """`said` is a line of the scene before the paying choice (C7 c, LO 2026-11-03: the price
    is in the scene, never on the button). The backroom is a declared sex-for-pay scene."""
    g = sc.hot_game()
    node = g["canvases"][-1]["nodes"][0]
    node["blocks"].insert(0, {"type": "paragraph", "content": said})
    node["exit_block"] = {"choices": [
        {"text": "Say yes.", "effects": [{"trait": "money", "op": "add", "value": 100}]}]}
    model, g2 = gates.build(g)
    card = sc.card(id="backroom_trade", pool=["backroom"], sex_for_pay=True)
    return gates._paid_choice_names_amount(model, g2, {"board": {"economy": {"currency": "money"},
                                                                 "systems": [card]}})


def test_a_paid_scene_with_an_amount_passes_in_figures_or_words():
    assert paid("He holds out the $100.")[0] is True
    assert paid("A hundred, like the note says.")[0] is True
    assert paid("Ten bucks and he's done.")[0] is True


def test_a_paid_scene_with_no_amount_warns():
    ok, _, d = paid("He holds out his money.")
    assert ok is False and "names no price" in d[0]


def test_no_paid_choice_is_na_and_neither_is_a_block():
    model, g = gates.build(ws6.green_game())
    assert gates._paid_choice_names_amount(model, g, None)[0] is None
    assert not {"a system meets its floors", "sex for pay names the amount"} & set(gates.SHIP_BLOCK_GATES)
