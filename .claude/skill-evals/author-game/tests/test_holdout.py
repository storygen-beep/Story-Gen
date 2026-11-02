"""Held-out checks: fail the untouched fixture, pass a correct edit, fail the logged mistake."""
from __future__ import annotations

import copy
import json
import importlib.util
import sys
from pathlib import Path

import pytest

EVAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EVAL_DIR))
sys.path.insert(0, str(EVAL_DIR / "tests"))
import lib  # noqa: E402
from test_checks import add, base, canvas, choice, cond, cv, para, say  # noqa: E402,F401

HOLDOUT = sorted(p.name for p in (EVAL_DIR / "cases_holdout").iterdir() if p.is_dir()
                 and json.loads((p / "case.json").read_text()).get("kind", "edit") == "edit")


def load_check(case_id: str):
    spec = importlib.util.spec_from_file_location(f"h_{case_id}", EVAL_DIR / "cases_holdout" / case_id / "check.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.check


def good_bad(case_id, base):
    g, b = copy.deepcopy(base), copy.deepcopy(base)
    if case_id == "h1_desk_drawer_locked":
        nerve = {"type": "trait", "subject": "player", "trait_key": "nerve", "operator": "gte", "value": 15}
        for x, shown in ((g, True), (b, False)):
            cv(x, "hub_martin_study")["nodes"][0]["exit_block"]["choices"].append(
                choice("Open his desk drawer.", conditions=cond(nerve), show_when_locked=shown))
    elif case_id == "h2_reputation_sidebar":
        for x in (g, b):
            x["sidebar_items"].append({"type": "trait_bar", "trait": "reputation", "label": "Reputation", "max": 100})
            add(x, canvas("rep_up", "club", [para("They watch you dance.")],
                          [choice("Bow.", effects=[{"targetType": "player", "trait": "reputation", "op": "add", "value": 2}])]))
        g["traits"]["labels"].append({"key": "reputation", "label": "Reputation"})
    elif case_id == "h3_suspicion_meter":
        raise_ = [{"targetType": "npc", "npcId": "npc_diane", "trait": "diane_suspicion", "op": "add", "value": 1}]
        for x in (g, b):
            add(x, canvas("flirt", "kitchen", [para("You laugh at Martin's joke.")], [choice("Touch his arm.", effects=raise_)]))
        read = {"type": "trait", "subject": "npc:npc_diane", "trait_key": "diane_suspicion", "operator": "gte", "value": 3}
        add(g, canvas("diane_asks", "kitchen", [say("npc_diane", "What's going on?")], conditions=cond(read)))
    elif case_id == "h4_club_regular_pays":
        pay = {"targetType": "player", "trait": "money", "op": "add", "value": 40}
        add(g, canvas("walkin_club_regular", "club", [para("He waves you over.")], [choice("Sit.", effects=[pay])]))
        add(b, canvas("walkin_club_regular", "club", [para("He waves you over.")], [choice("Sit.")]))
    elif case_id == "h5_daily_bus_fare":
        fare = {"targetType": "player", "trait": "money", "op": "add", "value": -10}
        floor = {"type": "trait", "subject": "player", "trait_key": "money", "operator": "gte", "value": 10}
        g["engine"]["daily_tick"]["traitEffects"] = [dict(fare, conditions=cond(floor))]
        b["engine"]["daily_tick"]["traitEffects"] = [fare]
    elif case_id == "h6_lodger_home":
        # Like every resident in the fixture, Ruth has no 02:00 row; the ledger says where she sleeps.
        for x in (g, b):
            x["locations"].append({"id": "spare_room", "name": "The Spare Room"})
            x["npcs"].append({"id": "npc_ruth", "name": "Ruth", "schedules": [
                {"location": "kitchen", "weekdays": [0, 1, 2, 3, 4, 5, 6], "start_time": "08:00", "end_time": "19:00"},
                {"location": "spare_room", "weekdays": [0, 1, 2, 3, 4, 5, 6], "start_time": "19:00", "end_time": "23:00"}]})
    return g, b


def ledgers(case_id):
    """(good, bad) ledgers. Only h6 reads one: the bad ledger declares no home for the new lodger."""
    good = {"board": {"map": {"homes": {"npc_ruth": "spare_room"}}}}
    bad = {"board": {"map": {"homes": {}}}}
    return good, bad


def call(check, game, base, ledger):
    return check(game, base, ledger) if check.__code__.co_argcount >= 3 else check(game, base)


@pytest.mark.parametrize("case_id", HOLDOUT)
def test_untouched_fixture_fails(case_id, base):
    assert call(load_check(case_id), copy.deepcopy(base), base, ledgers(case_id)[0])


@pytest.mark.parametrize("case_id", HOLDOUT)
def test_good_edit_passes(case_id, base):
    good, _ = good_bad(case_id, base)
    assert call(load_check(case_id), good, base, ledgers(case_id)[0]) == []


@pytest.mark.parametrize("case_id", HOLDOUT)
def test_logged_mistake_fails(case_id, base):
    _, bad = good_bad(case_id, base)
    assert call(load_check(case_id), bad, base, ledgers(case_id)[1])


def test_h6_hallway_home_fails(base):
    g, _ = good_bad("h6_lodger_home", base)
    assert call(load_check("h6_lodger_home"), g, base, {"board": {"map": {"homes": {"npc_ruth": "landing"}}}})
