"""first_term — the 21 people. Source: sheets/people/*.md and board.characters (schedules in
the sheets' order: the engine takes the first matching row)."""
from tomlw import *

M = [0]; T = [1]; W = [2]; R = [3]; F = [4]; SA = [5]; SU = [6]
WK = [0, 1, 2, 3, 4]
ALL = [0, 1, 2, 3, 4, 5, 6]

def row(loc, wds, a, b, act, when=None):
    r = {"location": loc, "weekdays": wds, "start_time": a, "end_time": b, "activity": act}
    if when:
        r["when"] = when
    return r

MET = lambda f: cond(flag(f))

PEOPLE = [
    dict(id="npc_ryan", name="Ryan", role="step-brother", age=22,
         relationship="Your step-brother, 22. Mark's son. The only one in this house who asks how your day was.",
         tags=["Says little", "You, and he's stopped hiding it", "Gym shirts", "Energy drinks"],
         core={"want": 20, "warmth": 50}, show=["warmth"],
         schedules=[
             row("home_bathroom", WK, "06:45", "07:30", "in the shower first (Laura's rule)"),
             row("home_ryan_room", [0, 1, 3, 4, 6], "18:00", "22:00", "home from the yard"),
             row("home_ryan_room", [5, 6], "07:30", "18:00", "home, weekend"),
             row("home_ryan_room", ALL, "22:00", "06:45", "in his room for the night"),
         ]),
    dict(id="npc_laura", name="Laura", role="mom", age=41,
         relationship="Your mom, 41. Wants a happy house, and wants you closer than she says.",
         tags=["Warm until she isn't", "Her good girl, close", "Dresses she doesn't wear", "White wine"],
         core={"want": 0, "warmth": 50}, show=["warmth"],
         schedules=[
             row("home_hall", ALL, "23:00", "02:00", "waiting on the dark stairs", when=MET("came_home_late")),
             row("home_kitchen", WK, "06:30", "08:00", "making breakfast before work"),
             row("home_kitchen", [0, 1, 3, 4, 6], "18:00", "22:00", "in the kitchen, evening"),
             row("home_master_bedroom", [6, 0, 1, 2, 3, 4], "22:00", "06:30", "asleep"),
             row("home_master_bedroom", SA, "00:00", "07:00", "asleep"),
             row("home_master_bedroom", SU, "00:00", "07:00", "asleep"),
             row("home_master_bedroom", SA, "17:00", "18:30", "dressing to go out"),
             row("home_living_room", SA, "22:00", "00:00", "waiting up in the dark"),
         ]),
    dict(id="npc_mark", name="Mark", role="step-father", age=46,
         relationship="Your step-father, 46. Collects the rent at the kitchen table, and owes Vance more than he says.",
         tags=["Counts slowly", "Control, and you", "Work boots", "Cheap beer"],
         core={"want": 0, "power": 50}, show=["power"],
         schedules=[
             row("home_living_room", [6, 0, 1, 2, 3, 4], "22:00", "00:00", "up late, Laura asleep"),
             row("home_living_room", [0, 1, 2, 3, 4, 5], "00:00", "02:00", "up late, Laura asleep"),
             row("home_master_bedroom", ALL, "02:00", "07:00", "asleep"),
             row("home_master_bedroom", SA, "22:00", "00:00", "asleep"),
             row("home_master_bedroom", SU, "00:00", "02:00", "asleep"),
             row("home_garage", [0, 1, 3, 4], "18:00", "22:00", "in the garage, evening"),
             row("home_kitchen", W, "18:00", "22:00", "cooking, Wednesday"),
             row("home_garage", SA, "09:00", "17:00", "in the garage, Saturday"),
             row("home_kitchen", SU, "08:00", "22:00", "the Sunday table"),
         ]),
    dict(id="npc_tom", name="Tom", role="café manager", age=31,
         relationship="The café manager, 31. Gives you shifts, sets the uniform rule, and closes late.",
         tags=["Names the price", "You behind the counter", "Rolled sleeves", "Espresso"],
         core={"want": 0, "power": 50}, show=["power"],
         schedules=[row("cafe", [0, 1, 2, 3, 4, 5], "08:00", "23:00", "running the café", when=MET("tom_met"))]),
    dict(id="npc_zoe", name="Zoe", role="college friend", age=19,
         relationship="Your college friend, 19. Pulls you out, dares you instead of asking.",
         tags=["Dares, never asks", "You, at her parties", "Fairy lights", "Vodka and lime"],
         core={}, show=[],
         schedules=[
             row("quad", [1, 3, 4], "14:30", "18:00", "lying on the grass", when=MET("zoe_met")),
             row("zoe_apartment", [0, 1, 2, 3, 4, 5], "18:00", "00:00", "at home", when=MET("zoe_met")),
             row("zoe_apartment", SA, "00:00", "02:00", "at home", when=MET("zoe_met")),
             row("canteen", WK, "11:45", "13:00", "at lunch", when=MET("zoe_met")),
             row("park", [5, 6], "08:00", "10:00", "on her weekend run", when=MET("zoe_met")),
         ]),
    dict(id="npc_hale", name="Dr. Hale", role="professor", age=39,
         relationship="Your Psychology professor, 39. Married. Watches to see how far you'll go.",
         tags=["Watches, then decides", "To see how far", "Tweed and a wedding ring", "Black coffee"],
         core={}, show=[],
         schedules=[
             row("lecture_hall", [0, 2, 4], "08:30", "10:00", "teaching Psychology", when=MET("hale_met")),
             row("lecture_hall", R, "13:00", "14:30", "teaching Psychology", when=MET("hale_met")),
             row("hale_office", R, "17:00", "19:30", "Thursday office hours", when=MET("hale_met")),
         ]),
    dict(id="npc_jake", name="Jake", role="campus guy", age=20,
         relationship="A guy from campus, 20. On the team. Wants a girlfriend he can show off.",
         tags=["Shows you off", "A girlfriend to be seen with", "Team jacket", "Protein shakes"],
         core={}, show=[],
         schedules=[
             row("quad", [0, 2, 4], "08:30", "11:45", "with the team", when=MET("jake_met")),
             row("zoe_apartment", F, "19:00", "00:00", "at Zoe's party", when=MET("jake_met")),
             row("canteen", WK, "11:45", "13:00", "at lunch", when=MET("jake_met")),
             row("home_front_door", SA, "22:00", "00:00", "walking you home",
                 when=cond(flag("jake_met"), flag("jake_date_booked"))),
         ]),
    dict(id="npc_vance", name="Mr. Vance", role="landlord", age=54,
         relationship="Your landlord, 54. Owns the house and lives next door.",
         tags=["Waits on his porch", "You, more each time", "Cardigan and slippers", "Pipe tobacco"],
         core={"want": 0, "power": 50}, show=["power"],
         schedules=[row("vance_house", ALL, "18:00", "22:00", "on his porch", when=MET("vance_met"))]),
    dict(id="npc_nadia", name="Nadia", role="Psychology classmate", age=20,
         relationship="A second-year in your Psychology class, 20. Saves you a seat. Knows Hale's history.",
         tags=["Knows things", "To see what Hale does", "Big glasses", "Tea"],
         core={}, show=[],
         schedules=[
             row("lecture_hall", [0, 2, 4], "08:30", "10:00", "beside you in Psychology", when=MET("nadia_met")),
             row("lecture_hall", R, "13:00", "14:30", "beside you in Psychology", when=MET("nadia_met")),
             row("library", [0, 1, 2, 4], "14:30", "18:00", "studying", when=MET("nadia_met")),
             row("canteen", WK, "11:45", "13:00", "at lunch", when=MET("nadia_met")),
         ]),
    dict(id="npc_gary", name="Gary", role="café regular", age=52,
         relationship="A café regular, 52. Booth four, a newspaper, and a wallet.",
         tags=["Pays for company", "Ten minutes of you", "Reading glasses", "Black tea"],
         core={}, show=[],
         schedules=[
             row("cafe", WK, "14:30", "18:00", "in booth four", when=MET("gary_met")),
             row("cafe", F, "20:00", "22:00", "in booth four", when=MET("gary_met")),
         ]),
    dict(id="npc_art_lecturer", name="The art lecturer", role="Figure drawing", age=45,
         relationship="Your Figure drawing lecturer, 45. Wants to draw you.",
         tags=["Looks for a living", "To draw you", "Charcoal on her hands", "Green tea"],
         core={}, show=[],
         schedules=[
             row("lecture_hall", [1, 3], "08:30", "10:00", "teaching Figure drawing", when=MET("art_lecturer_met")),
             row("lecture_hall", W, "13:00", "14:30", "teaching Figure drawing", when=MET("art_lecturer_met")),
             row("art_office", [0, 1, 3, 4], "14:30", "18:00", "office hours", when=MET("art_lecturer_met")),
         ]),
    dict(id="npc_business_lecturer", name="The Business lecturer", role="Business", age=50,
         relationship="Your Business lecturer, 50. Strict. Can't be bought.",
         tags=["By the book", "Your work, done", "Grey suit", "Instant coffee"],
         core={}, show=[],
         schedules=[
             row("lecture_hall", [0, 2], "10:15", "11:45", "teaching Business", when=MET("business_lecturer_met")),
             row("lecture_hall", T, "13:00", "14:30", "teaching Business", when=MET("business_lecturer_met")),
             row("business_office", [0, 2, 3, 4], "14:30", "18:00", "office hours", when=MET("business_lecturer_met")),
         ]),
    dict(id="npc_bio_ta", name="The Biology TA", role="Biology TA", age=28,
         relationship="Your Biology TA, 28. Shy. Looks, and hopes not to be caught looking.",
         tags=["Looks away too late", "To look, unseen", "Lab coat", "Vending-machine chocolate"],
         core={}, show=[],
         schedules=[
             row("lecture_hall", [1, 3], "10:15", "11:45", "teaching Biology", when=MET("bio_ta_met")),
             row("lecture_hall", M, "13:00", "14:30", "teaching Biology", when=MET("bio_ta_met")),
             row("ta_office", [1, 2, 3, 4], "14:30", "18:00", "office hours", when=MET("bio_ta_met")),
         ]),
    dict(id="npc_dean", name="The dean", role="dean", age=55,
         relationship="The dean, 55. Handles grades, complaints and probation. Wants to be obeyed.",
         tags=["Expects obedience", "The trouble gone", "Pressed shirt", "Mints"],
         core={}, show=[],
         schedules=[row("dean_office", WK, "09:00", "17:00", "in his office", when=MET("dean_met"))]),
    dict(id="npc_kayla", name="Kayla", role="Ryan's girlfriend", age=21,
         relationship="Ryan's girlfriend, 21. Wants the house to know about her.", tags=[], core={}, show=[],
         schedules=[]),
    dict(id="npc_claire", name="Claire", role="Hale's wife", age=38,
         relationship="Dr. Hale's wife, 38. Picks him up after office hours.", tags=[], core={}, show=[],
         schedules=[]),
    dict(id="npc_desk_guy", name="The guy beside you", role="the next desk", age=21,
         relationship="A guy who sits beside you in class, 21. Always needs help with something.", tags=[],
         core={}, show=[], schedules=[]),
    dict(id="npc_rival", name="The rival girl", role="rival classmate", age=21,
         relationship="A girl in your classes, 21. Would love to see you in trouble with the dean.", tags=[],
         core={}, show=[], schedules=[]),
    dict(id="npc_study_guy", name="The study guy", role="Business classmate", age=21,
         relationship="A guy in your Business and Biology classes, 21. Has the answers, wants your attention.",
         tags=[], core={}, show=[], schedules=[]),
    dict(id="npc_cocky_guy", name="The cocky guy", role="Jake's teammate", age=21,
         relationship="Jake's teammate, 21. In your Figure drawing class. Trades answers for a look.", tags=[],
         core={}, show=[],
         schedules=[
             row("zoe_apartment", F, "23:00", "00:00", "at Zoe's party", when=MET("cocky_guy_met")),
             row("zoe_apartment", SA, "00:00", "02:00", "at Zoe's party", when=MET("cocky_guy_met")),
         ]),
    dict(id="npc_figure_model", name="The figure-drawing model", role="life model", age=25,
         relationship="The model in Figure drawing, 25. Paid to be drawn, naked, every class.", tags=[],
         core={}, show=[], schedules=[]),
]


# ── Iteration 002: every schedule row comes from the ledger (board.characters[].schedule), in the
# ledger's order, because the engine takes the first matching row (v2.py:4304-4318). The rows above
# are iteration 001's hand copies and are replaced here, so the sheets and the build cannot drift.
# A row the ledger marks for a later release ("release": "later …") is not built.
# `when`: the ledger's own gate where it has one; otherwise the person's `<x>_met` flag, as 0.1
# built it (who_is_where.py counts a met-only `when` as an ordinary row).
import json as _json, os as _os
_LEDGER = _json.load(open(_os.path.join(_os.path.dirname(_os.path.abspath(__file__)),
                                        "..", "..", "..", "v2_state.json")))
_DAY = {"Mon": 0, "Tue": 1, "Wed": 2, "Thu": 3, "Fri": 4, "Sat": 5, "Sun": 6}

# What the Schedules page prints for each built row, in ledger order. "asleep" is the word the
# truth gates read as sleeping (gates.py _TR_SLEEP).
ACTIVITIES = {
    "npc_ryan": ["at dinner", "in the shower first (Laura's rule)", "home, weekend morning",
                 "in his room for the night", "home in his room, evening", "in his room with Kayla",
                 "watching TV, a film on"],
    "npc_laura": ["waiting on the dark stairs", "making breakfast before work", "in the kitchen, evening",
                  "asleep", "asleep", "asleep", "dressing to go out", "waiting up in the dark"],
    "npc_mark": ["at dinner", "in the garage, evening", "up late with the TV on", "up late with the TV on",
                 "asleep", "asleep", "asleep", "cooking, Wednesday", "in the garage, Saturday",
                 "the Sunday table"],
    "npc_tom": ["running the café", "closing up, the café shut"],
    "npc_zoe": ["at the party house", "at home", "at home, party night", "at home, the party after midnight",
                "going to bed", "lying on the grass", "at lunch", "on her weekend run",
                "in class: figure drawing, then Biology", "in class: Biology", "in class: figure drawing"],
    "npc_hale": ["teaching Psychology", "teaching Psychology", "Thursday office hours"],
    "npc_jake": ["with the team", "at Zoe's party", "at lunch", "picking you up", "walking you home",
                 "team training", "in class: figure drawing", "in class: figure drawing"],
    "npc_vance": ["at your front door", "on his porch"],
    "npc_nadia": ["beside you in Psychology", "beside you in Psychology", "studying", "at lunch"],
    "npc_gary": ["in booth four", "in booth four"],
    "npc_art_lecturer": ["teaching Figure drawing", "teaching Figure drawing", "office hours"],
    "npc_business_lecturer": ["teaching Business", "teaching Business", "office hours"],
    "npc_bio_ta": ["teaching Biology", "teaching Biology", "office hours"],
    "npc_dean": ["in his office"],
    "npc_cocky_guy": ["at Zoe's party", "at Zoe's party"],
}
# The household is home from the first screen: no met gate (0.1 built them with none).
_NO_MET = {"npc_ryan", "npc_laura", "npc_mark"}


# Laura's stairs row reads came_home_late for 4 hours, as the ledger writes it (L20). Since LO's
# 2026-10-09 answer (DECISIONS 75) the street never sets it; each late outing does, with its own flag
# (canv.mark_late, iteration 002 part 3).
# A latch the ledger writes as a bare flag is read by hours since (gate: a latch flag is cleared): Jake's
# booking lapses after a week (Q73), the night he took her out lasts 6 hours (jake_saturday_date sheet),
# Vance knocks the Monday after a short Sunday (the rent is taken Sunday 00:00).
_LATCH_HOURS = {"jake_date_booked": 168, "jake_date_went": 6, "rent_carried": 48}


def _ledger_when(w):
    if isinstance(w, str) and w in _LATCH_HOURS:
        return cond(flag(w), {"type": "hours_since_flag", "subject": "player", "flag_key": w, "operator": "lt",
                              "value": _LATCH_HOURS[w]})
    if not w:
        return None
    if isinstance(w, str):
        return cond(flag(w))
    return w  # a full v1.0 condition block, written that way in the ledger


def _ledger_schedules(pid):
    ch = next(c for c in _LEDGER["board"]["characters"] if c["id"] == pid)
    rows = [r for r in ch.get("schedule", []) if "later" not in str(r.get("release", ""))]
    acts = ACTIVITIES.get(pid, [])
    assert len(acts) == len(rows), f"{pid}: {len(rows)} ledger rows, {len(acts)} activities"
    out = []
    for r, act in zip(rows, acts):
        when = _ledger_when(r.get("when"))
        if when is None and pid not in _NO_MET:
            when = MET(pid.replace("npc_", "") + "_met")
        out.append(row(r["where"], [_DAY[d] for d in r["weekdays"]], r["from"],
                       "00:00" if r["to"] == "24:00" else r["to"], act, when=when))
    return out


for _p in PEOPLE:
    _p["schedules"] = _ledger_schedules(_p["id"])
