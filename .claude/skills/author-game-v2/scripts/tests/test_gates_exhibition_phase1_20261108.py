"""Exhibition phase 1 (LO, 2026-11-08): a climb starts on a choice; a description pays what it says; a slot word
means the whole slot. Fixtures are built here."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import gates  # noqa: E402
from test_gates_group2_checks import ch, cv, game, nd  # noqa: E402

STATE = {"board": {"ascent_tiers": ["show"]}}
PAY = [{"targetType": "player", "trait": "show", "op": "add", "value": 1, "cap": 19}]
NO_BRA = {"version": "1.0", "logic": "AND", "items": [{"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}]}
LEAVE = [{"slots_required": ["bra", "underwear", "top", "bottom"], "message": "Not like this."}]


def climb(*canvases, locations=None):
    g = game(*canvases)
    if locations:
        g["locations"] = locations
    return gates._climb_starts_on_a_choice(g, STATE)


def test_a_plain_daily_choice_passes():
    assert climb(cv("look", [nd("a", [ch("Let him look.", eff=PAY)])]))[0] is True


def test_only_a_walk_in_on_a_roll_fails():
    assert climb(cv("walkin", [nd("a", [ch("Don't grab it.", eff=PAY)])], substitution_only=True))[0] is False


def test_a_choice_the_leave_rules_refuse_fails():
    row = cv("run", [nd("a", [ch("Run braless.", eff=PAY, conds=[NO_BRA["items"][0]])])], location="park")
    assert climb(row, locations=[{"id": "park", "name": "Park", "clothing_rules": LEAVE}])[0] is False


def test_a_pay_behind_a_higher_button_fails():
    gated = {"type": "trait", "subject": "player", "trait_key": "show", "operator": "gte", "value": 60}
    row = cv("shift", [nd("a", [ch("Play along.", node="b", conds=[gated])]), nd("b", [ch("Clock out.", eff=PAY)])])
    assert climb(row)[0] is False


def test_a_choice_that_needs_progress_fails():
    met = {"type": "flag", "subject": "player", "flag_key": "zoe_met", "operator": "is_true"}
    assert climb(cv("dare", [nd("a", [ch("Run.", eff=PAY, conds=[met])])]))[0] is False


def test_a_description_that_claims_an_unpaid_meter_fails():
    row = cv("warn", [nd("a", [ch("Go.")])])
    row["description"] = "A warning. Show +1, once a day."
    ok, _, rows = gates._description_pays_what_it_says(game(row))
    assert ok is False and "warn" in rows[0]


def test_a_description_that_is_paid_passes():
    row = cv("look", [nd("a", [ch("Let him look.", eff=PAY)])])
    row["description"] = "A look. Show +1."
    assert gates._description_pays_what_it_says(game(row))[0] is True


def test_a_slot_word_means_the_whole_slot():
    g = {"clothing": [{"id": "low_top", "name": "Low-cut top", "slot": "top"},
                      {"id": "tshirt", "name": "T-shirt", "slot": "top"}]}
    by_noun, _ = gates._garment_vocab(g)
    assert by_noun["top"] == {"low_top", "tshirt"}
