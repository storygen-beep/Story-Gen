"""guidance_from_ladder.py and the --ship hint-per-step check (PRD IC5, LO 2026-09-27).
Uses the three-step `npc_jo` ladder from test_gates_ws4. Nothing in games/ is written."""
import copy
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gates  # noqa: E402
import guidance_from_ladder as gfl  # noqa: E402
from test_gates_ws4 import game, state  # noqa: E402

try:
    import tomllib
except ImportError:                                     # py3.10
    import tomli as tomllib


def generated():
    return tomllib.loads(gfl.generate(game(), state()))["quest_cards"]


def with_cards(cards):
    g = game()
    g["quest_cards"] = [c for c in g.get("quest_cards") or [] if c.get("npc_id") != "npc_jo"]
    g["quest_cards"] += cards
    return g


def test_one_card_per_step_plus_a_terminal_card():
    cards = generated()
    assert len(cards) == 4
    for n, c in enumerate(cards[:3], start=1):
        assert c["npc_id"] == "npc_jo" and c["ready_canvas"] == f"jo_{n}"
        assert c["when"] == [{"type": "trait", "subject": "player", "trait": "jo_stage",
                              "op": "eq", "value": n - 1}]
        assert c["tip"] == "Shed, every day 18:00–22:00"
        assert c["goals"][0]["value"] == n
    assert cards[3]["terminal"] is True and cards[3]["when"][0]["op"] == "gte"


def test_days_are_phrased_for_a_player():
    assert gfl.days_phrase(["Mon", "Tue", "Wed", "Thu", "Fri"]) == "weekdays"
    assert gfl.days_phrase([5, 6]) == "weekends"
    assert gfl.days_phrase(["Mon", "Wed"]) == "Mon, Wed"


def test_generated_cards_pass_guidance_exists_and_the_hint_check():
    g = with_cards(generated())
    checked, probs = gates.step_hint_problems(g, state())
    assert checked == 3 and probs == []
    model, g2 = gates.build(copy.deepcopy(g))
    r = next(r for r in gates.run_gates(model, g2, state()) if r["gate"] == "guidance exists")
    assert not any("npc_jo" in d for d in r["detail"]), r


def test_a_missing_card_is_listed_by_step():
    cards = generated()
    del cards[1]
    _, probs = gates.step_hint_problems(with_cards(cards), state())
    assert len(probs) == 1 and "step 2 (jo_2)" in probs[0] and "no card" in probs[0]


def test_a_tip_without_the_time_is_listed():
    cards = generated()
    cards[0]["tip"] = "The shed."
    cards[0]["goals"][0]["label"] = "Find Jo at the shed"
    _, probs = gates.step_hint_problems(with_cards(cards), state())
    assert len(probs) == 1 and "does not name the time" in probs[0]


def test_a_band_card_matches_its_one_step():
    cards = generated()
    cards[1]["when"] = [{"trait": "jo_stage", "subject": "player", "op": "gte", "value": 1},
                        {"trait": "jo_stage", "subject": "player", "op": "lt", "value": 2}]
    assert gates.step_hint_problems(with_cards(cards), state())[1] == []


def test_money_is_not_monday():
    cards = generated()
    cards[0]["tip"] = "The shed, with money."
    cards[0]["goals"][0]["label"] = "Bring money to the shed"
    _, probs = gates.step_hint_problems(with_cards(cards), state())
    assert any("the time" in p for p in probs)


def test_no_ladder_is_na_and_generates_nothing():
    st = {"board": {"characters": [{"id": "npc_jo"}]}}
    assert gates.step_hint_problems(game(), st) is None
    assert gfl.generate(game(), st) == ""


def test_out_inside_games_is_refused(capsys):
    rc = gfl.main(["ladder_fx", "--out", os.path.join(gfl.REPO, "games", "x.toml")])
    assert rc == 2 and "refused" in capsys.readouterr().out
    assert not os.path.exists(os.path.join(gfl.REPO, "games", "x.toml"))
