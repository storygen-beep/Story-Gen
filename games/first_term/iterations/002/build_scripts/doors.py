"""doors.py: a scene done with a person opens from that person's portrait (LO's playtest, 2026-11-10, DECISIONS 224).

The engine's portrait shows ONE canvas per person per room, the highest priority (v2.py
selectNpcPortraitCanvasesForLocation). A second scene with the same person and only `requires_npc` (no `npc`)
fell into the solo-link bucket and showed as its own link beside her face ("Dare me, Zo." next to Zoe running).
LO: it "should be inside her npc portrait activity not a separate link". The skill's R1 (the-surfaces.md) already
says one canvas per person x when; the gate `a person's scene is inside their portrait` now checks it.

Each scene here keeps its canvas and its nodes. Its trigger is door-only (`hidden_from_location`: off the room's
screen, still reachable from another canvas). Its hub gets a button into the scene's first node, carrying
everything the trigger checked: the conditions, one button per schedule row (as weekday + clock conditions), and
the once-a-day cap as a `<scene>_today` flag set on every exit that leaves the scene (cleared by [engine.daily_tick]
in 0_systems_spec.toml). This module is the single source of those conditions: the scene's own file builds its
trigger from `trigger(sid)`, and the hub's file opens the doors with `apply(out)`.

The part scripts run as separate processes, and a scene's file is not always its hub's (pools.py holds two of
Zoe's scenes; zoe.py holds her hubs), so the data lives here and both import it.
"""
from tomlw import cond, flag, trait, fset, tod, wd

Z, R, M, H = "npc_zoe", "npc_ryan", "npc_mark", "npc_hale"
AT_PARTY = {"type": "hours_since_flag", "subject": "player", "flag_key": "party_went", "operator": "lt", "value": 8}

DOORS = {
    # zoe.py: her flash dare on the run. The canvas cap was once a day.
    "zoe_park_dare": dict(
        npc=Z, hub="hub_zoe_park", label="\"Dare me, Zo.\"", first="ask", today="zoe_park_dare_today",
        conds=[flag("zoe_met"), {"type": "clothing_slot", "slot": "top", "operator": "equipped"}],
        schedules=None),
    # pools.py: after the run with her (the "Run a lap with her" button, within the hour): park_hidden.md
    "park_hidden": dict(
        npc=Z, hub="hub_zoe_park", label="Let Zoe finger you off the path", first="pull", today="park_hidden_today",
        conds=[trait("corruption", "gte", 60), trait("zoe_step", "gte", 3), flag("ran_with_zoe"),   # strangers able to see: Hungry (DECISIONS 124)
               {"type": "hours_since_flag", "subject": "player", "flag_key": "ran_with_zoe", "operator": "lt", "value": 1}],
        schedules=[{"weekdays": [5, 6], "start_time": "08:00", "end_time": "09:30"}]),   # done before her park row ends at 10:00
    # pools.py: one dare a party night, after midnight, so the day roll (which clears zoe_dared) can't open a second
    # the same night. zoe_dared is its cap; no _today flag.
    "zoe_dares": dict(
        npc=Z, hub="hub_zoe_apartment", label="Take Zoe's dare", first="dare", today=None,
        conds=[AT_PARTY, flag("picks_the_dares"), flag("zoe_dared", False), flag("cocky_guy_met")],
        schedules=[{"weekdays": [5], "start_time": "00:00", "end_time": "01:50"}]),   # false lines a3: a yes is 10 minutes, the cocky guy leaves at 02:00
    # ryan.py: the repeat after his step 8. reach audit 2026-11-09 (12_reach_audit.md): nights, plus his weekend
    # mornings in his room (Saturday after Kayla goes at 10:00). The act names no hour. Once a day.
    "ryan_two_knocks": dict(
        npc=R, hub="hub_ryan_room", label="Lean back on his door.", first="door", today="ryan_two_knocks_today",   # reader pass 2: she is in his room; the knocks were on the way in
        conds=[trait("ryan_step", "eq", 8)],
        schedules=[{"weekdays": [0, 1, 2, 3, 6], "start_time": "22:00", "end_time": "00:00"},
                   {"weekdays": [5], "start_time": "10:00", "end_time": "14:00"},
                   {"weekdays": [6], "start_time": "08:00", "end_time": "14:00"}]),
    # mark.py: the Sunday table. Opens to 11:45, so the count's 15 minutes end before noon (truth pass 2026-11-03).
    "mark_sunday_table": dict(
        npc=M, hub="hub_mark_kitchen", label="Join him at the table.", first="table", today="mark_sunday_table_today",   # reader pass 2: the table screen sits her down
        conds=[trait("mark_step", "gte", 1), flag("sunday_counted_today", False), flag("rent_starts")],
        schedules=[{"weekdays": [6], "start_time": "08:00", "end_time": "11:45"}]),
    # hale.py: Thursday before Claire, his office hours on the other weekdays, and the booked morning hour (LO,
    # 2026-11-09 and 2026-11-10). The act names no day; the door and the goodbye do. Once a day.
    "hale_thursdays": dict(
        npc=H, hub="hub_hale_office", label="Earn your grade in Dr. Hale's office", first="door", today="hale_thursdays_today",
        conds=[trait("hale_step", "eq", 4), trait("corruption", "gte", 40), trait("exhibitionism", "gte", 40)],
        schedules=[{"weekdays": [3], "start_time": "18:30", "end_time": "19:05"},
                   {"weekdays": [0, 1, 2, 4], "start_time": "15:00", "end_time": "19:00"},
                   {"weekdays": [0, 1, 2, 4], "start_time": "10:00", "end_time": "12:00"}]),
}


def trigger(sid):
    """The trigger fields a door-only scene takes from DOORS. The scene keeps its location, requires_npc and priority."""
    d = DOORS[sid]
    t = {"hidden_from_location": True, "conditions": cond(*d["conds"])}
    if d["schedules"]:
        t["schedules"] = d["schedules"]
    return t


def buttons(sid):
    """The hub's buttons into the scene: one per schedule row, each carrying the scene's whole gate."""
    from canv import go
    d = DOORS[sid]
    base = list(d["conds"]) + ([flag(d["today"], False)] if d["today"] else [])
    rows = d["schedules"] or [None]
    return [go(d["label"], node=f"{sid}.{d['first']}", mins=0,
               cond_=cond(*base, *([wd(*r["weekdays"]), tod(r["start_time"], r["end_time"])] if r else [])))
            for r in rows]


def _leaves(choice):
    return choice.get("targetType") in ("location", "return")


def apply(out):
    """Seal the scenes in `out` (their _today flag on every exit that leaves) and open the doors in its hubs."""
    seen = set()
    for c in out:
        sid = c.get("id")
        if sid in DOORS:
            t = c.get("trigger") or {}
            assert t.get("hidden_from_location"), f"doors.py: {sid} must build its trigger from doors.trigger()"
            today = DOORS[sid]["today"]
            if today:
                for nd in c["nodes"]:
                    for ch in nd.get("choices") or []:
                        if _leaves(ch):
                            fl = ch.setdefault("flagEffects", [])
                            if fset(today) not in fl:
                                fl.append(fset(today))
        for s, d in DOORS.items():
            if sid == d["hub"]:
                first = c["nodes"][0]["choices"]
                # before the hub's first plain way out ("Let her run on.", "Stay a while."), else at the end
                at = next((i for i, ch in enumerate(first) if _leaves(ch) and not ch.get("conditions")), len(first))
                first[at:at] = buttons(s)
                seen.add(s)
    return seen
