"""Every case check must fail the untouched fixture, pass a correct edit, and fail the
logged mistake it was built from. Run: venv/bin/python -m pytest .claude/skill-evals/author-game/tests -q
"""
from __future__ import annotations

import copy
import importlib.util
import sys
from pathlib import Path

import pytest

EVAL_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(EVAL_DIR))
import lib  # noqa: E402

BASE_TOML = EVAL_DIR / "tests" / "fixture_7_final_game.toml"


@pytest.fixture(scope="session")
def base():
    return lib.load_game(BASE_TOML)


def load_check(case_id: str):
    path = EVAL_DIR / "cases" / case_id / "check.py"
    spec = importlib.util.spec_from_file_location(f"check_{case_id}", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod.check


CASES = sorted(p.name for p in (EVAL_DIR / "cases").iterdir() if p.is_dir())


# ── small builders ───────────────────────────────────────────────────────────

def cond(*items):
    return {"version": "1.0", "logic": "AND", "items": list(items)}


def para(text):
    return {"type": "paragraph", "content": text}


def say(npc_id, text):
    return {"type": "dialog", "props": {"speaker": "npc", "npcId": npc_id}, "content": text}


def choice(text, **kw):
    return {"text": text, "targetType": "location", "locationId": "kitchen", "time_progression_minutes": 5, **kw}


def canvas(cid, location, blocks, choices_=(), **trigger):
    return {"id": cid, "name": cid, "description": "", "trigger": {"location": location, **trigger},
            "nodes": [{"id": "n1", "name": "n1", "blocks": list(blocks),
                       "exit_block": {"type": "choices", "choices": list(choices_)}}]}


def cv(game, cid):
    return next(c for c in game["canvases"] if c["id"] == cid)


def add(game, *cs):
    game["canvases"].extend(cs)
    return game


# ── good and bad edits per case ──────────────────────────────────────────────

def good_bad(case_id: str, base: dict):
    g, b = copy.deepcopy(base), copy.deepcopy(base)
    if case_id == "01_first_meeting_new_npc":
        for x in (g, b):
            x["npcs"].append({"id": "npc_priya", "name": "Priya Shah", "schedules": [
                {"location": "firm", "weekdays": [0, 1, 2, 3, 4], "start_time": "09:00", "end_time": "17:00"}]})
        add(g, canvas("priya_01", "firm", [para("The senior paralegal who trains the interns waves you over."),
                                           say("npc_priya", "I'm Priya.")], npc="npc_priya"))
        add(b, canvas("priya_01", "firm", [say("npc_priya", "I'm Priya.")], npc="npc_priya"))
    elif case_id == "02_ambient_diane_outfit":
        add(g, canvas("amb_diane", "kitchen", [say("npc_diane", "Is that what you're wearing?")], requires_npc="npc_diane"))
        add(b, canvas("amb_diane", "kitchen", [say("npc_diane", "Is that what you're wearing?")]))
    elif case_id == "03_drink_price":
        for x, op in ((g, "add"), (b, "subtract")):
            ch = lib.choices(cv(x, "act_drink"))[0]
            ch["text"] = "Order a drink ($15)."
            ch["effects"] = [{"targetType": "player", "trait": "money", "op": op, "value": -15 if op == "add" else 15},
                             {"targetType": "player", "trait": "energy", "op": op, "value": -10 if op == "add" else 10}]
    elif case_id == "04_martin_study_gate":
        gate = {"type": "trait", "subject": "npc:npc_martin", "trait_key": "martin_stage", "operator": "gte", "value": 3}
        cv(g, "hub_martin_study")["nodes"][0]["exit_block"]["choices"].append(
            choice("Stay after he closes the door.", conditions=cond(gate)))
        cv(b, "hub_martin_study")["nodes"][0]["exit_block"]["choices"].append(
            choice("Stay after he closes the door.", conditions={"logic": "AND", "items": [gate]}))
    elif case_id == "05_diane_dialogue":
        for x, t in ((g, "dialog"), (b, "dialogue")):
            node = cv(x, "hub_diane_home")["nodes"][0]
            for line in ("You're late.", "Eat something.", "Martin asked about you."):
                blk = say("npc_diane", line)
                blk["type"] = t
                node["blocks"].append(blk)
    elif case_id == "06_breakfast_independent_line":
        present = {"type": "npc_at_location", "npc_id": "npc_diane", "location_id": "kitchen"}
        cv(g, "hub_martin_breakfast")["nodes"][0]["blocks"].append(
            {"type": "group", "props": {"conditions": cond(present), "blocks": [para("Diane pours the coffee.")]}})
        node = cv(b, "hub_martin_breakfast")["nodes"][0]
        node["blocks"] = [{"type": "group", "props": {"conditions": cond(present), "blocks": [para("Diane pours.")]}}]
    elif case_id == "07_locked_doors":
        nerve = {"type": "trait", "subject": "player", "trait_key": "nerve", "operator": "gte", "value": 10}
        shower = {"type": "flag", "subject": "player", "flag_key": "ethan_watched_shower", "operator": "is_true"}
        for x, shown in ((g, True), (b, False)):
            chs = cv(x, "hub_ethan_landing")["nodes"][0]["exit_block"]["choices"]
            chs.append(choice("Knock on his door.", conditions=cond(nerve), show_when_locked=shown))
            chs.append(choice("Go into his room.", conditions=cond(shower), show_when_locked=shown))
    elif case_id == "08_ethan_step3_no":
        add(g, canvas("ethan_03", "ethan_room", [say("npc_ethan", "Close the door.")],
                      [choice("Close it."), choice("Tell him no and leave.")], npc="npc_ethan"))
        add(b, canvas("ethan_03", "ethan_room", [say("npc_ethan", "Close the door.")], [choice("Close it.")], npc="npc_ethan"))
    elif case_id == "09_theo_previous_evening":
        cv(g, "hub_theo_bar")["nodes"][0]["blocks"].append(say("npc_theo", "You again."))
    elif case_id == "10_work_late":
        chs = cv(g, "act_work_shift")["nodes"][0]["exit_block"]["choices"]
        chs.append(choice("Work late. (2h)", time_progression_minutes=120))
        cv(b, "act_work_shift")["nodes"][0]["exit_block"]["choices"].append(
            choice("Work late.", time_progression_minutes=30))
    elif case_id == "11_tonight_with_diane":
        evening = {"type": "time_of_day", "start_time": "19:00", "end_time": "22:00"}
        cv(g, "hub_diane_home")["nodes"][0]["exit_block"]["choices"].append(
            choice("Sit up with Diane tonight.", conditions=cond(evening)))
        cv(b, "hub_diane_home")["nodes"][0]["exit_block"]["choices"].append(choice("Sit up with Diane tonight."))
    elif case_id == "12_bathroom_watch":
        add(g, canvas("bath_watch", "bathroom", [
            para("Through the steam you see his cock, hard, his fist moving on it. He moans and thrusts into his hand, his cock dripping."),
            para("You can't tell him you saw it.")]))
        add(b, canvas("bath_watch", "bathroom", [
            para("You see him naked in the steam. It makes you think about what this house has become.")]))
    elif case_id == "13_jade_hotel_hub":
        for x in (g, b):
            add(x, canvas("hub_jade_bar", "hotel_bar", [say("npc_jade", "Buy me one.")], npc="npc_jade",
                          requires_npc="npc_jade"))
        lib.npc(g, "npc_jade")["schedules"].append(
            {"location": "hotel_bar", "weekdays": [6], "start_time": "18:00", "end_time": "21:00"})
    elif case_id == "14_walkin_tip":
        pay = {"targetType": "player", "trait": "money", "op": "add", "value": 20}
        add(g, canvas("walkin_tip", "firm", [para("He leaves a twenty.")], [choice("Take it.", effects=[pay])]))
        add(b, canvas("walkin_tip", "firm", [para("He leaves a twenty.")], [choice("Take it.")]))
    elif case_id == "15_kitchen_more":
        add(g, *[canvas(f"kitchen_{i}", "kitchen", [para("x")]) for i in range(4)])
        add(b, *[canvas(f"kitchen_{i}", "kitchen", [para("x")]) for i in range(2)])
    elif case_id == "16_theo_friday_nights":
        lib.npc(g, "npc_theo")["schedules"] += [
            {"location": "hotel_bar", "weekdays": [4], "start_time": "22:00", "end_time": "00:00"},
            {"location": "hotel_bar", "weekdays": [5], "start_time": "00:00", "end_time": "02:00"}]
        lib.npc(b, "npc_theo")["schedules"].append(
            {"location": "hotel_bar", "weekdays": [4], "start_time": "22:00", "end_time": "02:00"})
    elif case_id == "17_theo_wednesday_firm":
        rows = lib.npc(g, "npc_theo")["schedules"]
        rows.append({"location": "firm", "weekdays": [2], "start_time": "14:00", "end_time": "19:00"})
        for r in rows:  # the bar row on Wednesday now starts when the firm row ends
            if r["location"] == "hotel_bar":
                r["weekdays"] = [1, 3]
        rows.append({"location": "hotel_bar", "weekdays": [2], "start_time": "19:00", "end_time": "21:00"})
        lib.npc(b, "npc_theo")["schedules"].append(
            {"location": "firm", "weekdays": [2], "start_time": "14:00", "end_time": "19:00"})
    elif case_id == "18_rent_friday_scene":
        add(g, canvas("rent_friday", "kitchen", [say("npc_martin", "Friday, Emma.")], npc="npc_martin"))
        take = {"targetType": "player", "trait": "money", "op": "add", "value": -250}
        add(b, canvas("rent_friday", "kitchen", [say("npc_martin", "Friday, Emma.")],
                      [choice("Hand it over.", effects=[take])], npc="npc_martin"))
    else:
        raise KeyError(case_id)
    return g, b


@pytest.mark.parametrize("case_id", CASES)
def test_untouched_fixture_fails(case_id, base):
    assert load_check(case_id)(copy.deepcopy(base), base), "the untouched fixture must not pass"


@pytest.mark.parametrize("case_id", CASES)
def test_good_edit_passes(case_id, base):
    good, _ = good_bad(case_id, base)
    assert load_check(case_id)(good, base) == []


@pytest.mark.parametrize("case_id", CASES)
def test_logged_mistake_fails(case_id, base):
    _, bad = good_bad(case_id, base)
    if case_id == "09_theo_previous_evening":
        pytest.skip("graded by the past_claim lint, not by check.py")
    assert load_check(case_id)(bad, base)


# ── valid answers found in the first v2 run that the original checks wrongly failed ──

def test_work_late_via_its_own_node_passes(base):
    """v2 routed 'Work late (6h)' to a new node whose exit spends 360 minutes."""
    g = copy.deepcopy(base)
    c = cv(g, "act_work_shift")
    c["nodes"][0]["exit_block"]["choices"].append(
        {"text": "Work late with your $70. (6h)", "targetType": "node", "nodeId": "act_work_shift.late"})
    c["nodes"].append({"id": "late", "name": "late", "blocks": [para("The floor empties.")],
                       "exit_block": {"type": "choices", "choices": [
                           choice("Shut the laptop and go.", time_progression_minutes=360)]}})
    assert load_check("10_work_late")(g, base) == []


def test_rent_page_rewrite_passes(base):
    """v2 rewrote the engine's own rent page text instead of authoring a charging canvas."""
    g = copy.deepcopy(base)
    g["settings"]["rent"].setdefault("text", {})["scene"] = "Martin holds out his hand."
    assert load_check("18_rent_friday_scene")(g, base) == []


def test_work_late_via_location_exit_passes(base):
    """v2's actual shape: the late node ends on a location exit with the minutes under `config`."""
    g = copy.deepcopy(base)
    c = cv(g, "act_work_shift")
    c["nodes"][0]["exit_block"]["choices"].append(
        {"text": "Work late with your $70. (6h)", "targetType": "node", "nodeId": "act_work_shift.late"})
    c["nodes"].append({"id": "late", "name": "late", "blocks": [para("The floor empties.")],
                       "exit_block": {"type": "location", "text": "Shut the laptop and go.",
                                      "config": {"destinationType": "specific", "locationId": "firm",
                                                 "time_progression_minutes": 360}}})
    assert load_check("10_work_late")(g, base) == []
