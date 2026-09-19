#!/usr/bin/env python3
"""A schedule row that puts somebody in a room with nothing in it — a LIST, never a score.

Run from the repo root:

    venv/bin/python games/the_balance/process/presence.py [slug]

WHY THIS EXISTS
---------------
LO played the 2026-09-16 build, saw Tasha's face on her bedroom door, walked in, and
found an empty room. The engine was innocent. The game asks "is she here?" in two
places and the two use different tests:

    the door / the map card   setup.getNpcsPresentAtLocation   v2.py:5056
        SCHEDULE ONLY. If a [[npcs.schedules]] row puts her here now, her portrait
        is on the card and on the threshold screen.

    inside the room           setup.renderNpcPortraits          v2.py:5222
        SCHEDULE **AND** A SELECTABLE CANVAS. The grid is canvas-gated on purpose —
        the comment at v2.py:5276 says so: "only offer a click where there is an
        interaction". A housemate showering has to show on the map and block the
        door without being clickable, and that is the shape this protects.

So the door is not lying by design; the room is empty by omission. At the commit
this file was written against, `tasha_room` held ZERO canvases while Tasha was
scheduled into it seven hours a day, and `the_front_room` held zero while Nate sat
on that sofa four evenings a week.

WHY NOT gates.py
----------------
`gates.py` G6 `standing surface` (gates.py:5282-5287) reads **10/10 PASS** on this
game and cannot see any of it. It asks two questions per NPC — does she have *any*
canvas bound to her anywhere, and *any* schedule row — and never asks whether those
two are in the same room at the same time. Tasha passes it on `tasha_walks_in`, a
`substitution_only` canvas that can never render a portrait at all.

Widening that gate is a skill edit, which this game does not do (process/README.md
§0), so the game carries its own check.

WHAT IT REPORTS
---------------
Every [[npcs.schedules]] row, classified. A row is BACKED four ways and only the
fifth is a defect:

    portrait      a repeatable, non-random, non-substitution canvas carrying this
                  NPC at this location, live on every weekday the row covers.
    covered       she SPEAKS on a screen that exists in this room. `dinner` is one
                  table holding Gil, Nate and Tasha — three rows, one surface, and
                  that is good writing, not a hole.
    substitution  a substitution_only canvas bound to her here whose HOST is live
                  in these hours. Real content that rides another activity; never
                  a portrait. A substitution whose host is shut backs nothing.
    occupancy     declared below, with its reason. The row exists to block a door,
                  to put a second body in a room, or to gate somebody else's scene.
    DEAD          none of the above, and the report names the exact weekdays.

⚠️ THE ROW IS JUDGED PER WEEKDAY, not as a whole. Asking only "does anything here
overlap this row at all" is what hides the Gil case — he is at the kitchen table
18:00-21:00 all seven nights, `friday_payment` is the only thing bound to him
there, and one Friday scores the whole row backed while six evenings stay dead.

Two more lists, both visible without a browser:

  STRANDED     a portrait canvas bound to a room its own NPC is never scheduled
               into. `renderNpcPortraits` filters on getNpcLocation().location
               === locationId, so it cannot render on any day at any hour.
  DAY-CAPPED   a portrait whose **trigger** carries `max_triggers_per_day`. That
               cap does not spend the act, it deletes the person — click Cara at
               the union once and she is gone from the screen while still sitting
               at the table. It belongs on the CHOICE, as a `_today` flag cleared
               in [engine.daily_tick] (engine.md §28). Same throttle, she stays.

HOW TO PROVE THIS FILE STILL WORKS
----------------------------------
A check that cannot catch the defect it was written for is decoration.

    git stash && git checkout 6e0bd9d
    venv/bin/python games/the_balance/process/presence.py

must report, at that commit:

    4 DEAD rows   — tasha_room ×2, the_front_room ×2
    4 day-capped  — union_cara, sam_talks, paige_is_nice, bree_takes_it_home
    1 stranded    — office_closer
    6 on a ladder — the arc steps and friday_payment, which are correct

At HEAD it must report **0 DEAD** and **0 day-capped**. `office_closer` stays
stranded and the two DEFERRED rows stay printed; both are named to LO and left by
his call, and they are reprinted every run so that deferring stays a decision
somebody made rather than something the instrument quietly stopped mentioning.
"""

import pathlib
import sys
import tomllib

DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


# ⚠️ HAND-MAINTAINED, AND THAT IS THE POINT. An exemption the script works out for
# itself is an exemption that grows quietly. Writing the reason out loud is the
# whole value — each of these rows is doing a job that is not being clicked on.
#
# ⚠️ KEYED (npc, location, start_time) — BY THE ROW, NOT BY THE ROOM. It used to be
# (npc, location), which was fine while nobody slept anywhere. The sleep rows broke
# it: @nate is in nate_room twice now, awake 22:00-23:59 with `nate_door` behind it
# and asleep 00:00-07:00 with nothing, and a room-level exemption would have
# excused both. The awake row has to stay under scrutiny, so the key names the hour.
#
# ⚠️ AN OFFSCREEN LOCATION IS INVISIBLE TO THIS SCRIPT, AND THAT IS NOT A BUG WORTH
# FIXING HERE. The engine knows the property — `_loc_offscreen` at v2.py:20653 is
# what stops `the_gym` rendering a nav card — but this file never reads
# `location.properties`, so an offscreen row falls through to the "none of them
# hers" branch and reports every weekday dead. Teaching the script the property
# would be a real fix and it would also be a second place the rule lives; one
# written exemption, with the reason on it, is the same answer for less.
OCCUPANCY_ROWS = {
    # ⚠️ NINE ENTRIES LEFT ON 2026-09-19 WITH THE ROWS THEY EXCUSED. The sleep rows,
    # @nate at the gym, and five of her mum's rows all came from house passes that
    # were parked (games/the_balance/parked/README.md). Their written reasons are at
    # ff91336:games/the_balance/process/presence.py for when sheets/BASE.md puts
    # those hours back — a reason is worth reusing, a key for a row that is gone is not.
    ("npc_nate", "the_bathroom", "07:00"):
        "the shower in the opening. This row is what makes the bathroom taken — it "
        "blocks the door and shows him on the card, and there is nothing to click. "
        "v2.py:5270-5281 names exactly this case as intentional.",
    ("npc_gil", "the_master_bedroom", "21:00"):
        "the other half of the same door. The surface is `master_bedroom`, which is "
        "solo by design: she is looking, not talking to anybody.",
    ("npc_lynn", "the_kitchen", "19:00"):
        "she is the CONDITION for dinner, not a guest at it — `dinner`'s trigger is "
        "`npc_at_location npc_lynn is_present`, so this row is what makes that scene "
        "exist on the four nights she is off the ward. She does not speak in it and "
        "she is never touched.",
}

# Real holes, named to LO and deferred by him on 2026-09-16. They are printed every
# run so that deferring stays a decision somebody made rather than something the
# instrument quietly stopped mentioning.
DEFERRED_ROWS = {
    ("npc_cara", "the_quad"):
        "the 08:40-09:00 bench before class. the_cast.md:105 puts her there — 'in "
        "the ten minutes before class' — and no canvas uses it. A 20-minute window.",
}


def _mins(hhmm):
    h, _, m = str(hhmm).partition(":")
    return int(h or 0) * 60 + int(m or 0)


def live_days(row, canvas):
    """Which weekdays OF THIS ROW can this canvas actually appear on?

    ⚠️ DAY-PRECISE ON PURPOSE. Asking "do they overlap at all" is what hides the
    Gil case: he is at the kitchen table 18:00-21:00 all seven nights and
    `friday_payment` is the only thing bound to him there, on a Friday schedule.
    Any-overlap scores that row backed and loses the six evenings he is present
    and un-clickable. A canvas with no schedule of its own is live whenever its
    location is, so it backs the whole row.
    """
    days = set(row["weekdays"])
    if not canvas["schedules"]:
        return days
    live = set()
    for s in canvas["schedules"]:
        if (_mins(s.get("start_time", "00:00")) < _mins(row["end_time"])
                and _mins(row["start_time"]) < _mins(s.get("end_time", "23:59"))):
            live |= days & set(s.get("weekdays") or range(7))
    return live


def canvas_facts(canvas):
    """Flatten a canvas into the handful of things this check asks about."""
    t = canvas.get("trigger") or {}
    scheds = t.get("schedules") or ([t["schedule"]] if t.get("schedule") else [])
    return {
        "id": canvas.get("id"),
        "location": t.get("location") or canvas.get("location"),
        "npc": t.get("npc") or canvas.get("npc"),
        "repeatable": bool(t.get("is_repeatable", canvas.get("is_repeatable"))),
        "random": (t.get("trigger_mode", canvas.get("trigger_mode", "manual")) or "manual") == "random",
        "sub": bool(t.get("substitution_only", canvas.get("substitution_only"))),
        "active": t.get("is_active", canvas.get("is_active", True)) is not False,
        "max_per_day": t.get("max_triggers_per_day", canvas.get("max_triggers_per_day")),
        "gated": bool(t.get("conditions") or canvas.get("conditions")),
        "schedules": scheds,
        "speakers": speakers_of(canvas),
    }


def speakers_of(canvas):
    """Every NPC who says something on any screen of this canvas.

    ⚠️ THIS, AND NOT A NAME IN THE PROSE, IS WHAT COVERAGE MEANS. `dinner` is the
    case that settles it: four people at one table, and its prose names none of
    them — it says "four of you" and "your mum". Gil, Nate and Tasha are in that
    room entirely through `dialog` blocks carrying `props.npcId`. Grepping the
    paragraphs for "@nate" scores that screen as covering nobody, which is how the
    first version of this file reported three rows dead that are properly written.

    Recurses, because a speaker can sit inside a `group` band or a `block_pool`.
    """
    found = set()

    def walk(node):
        if isinstance(node, dict):
            npc_id = (node.get("props") or {}).get("npcId")
            if npc_id:
                found.add(npc_id)
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(canvas.get("nodes") or [])
    return found


def classify(row, npc, here, hosts_of):
    """(verdict, detail, dead_days) for one schedule row.

    `dead_days` is the subset of the row's own weekdays that nothing backs — the
    row is a defect only on those days.

    ⚠️ A SUBSTITUTION IS ONLY AS LIVE AS ITS HOST. A substitution_only canvas has
    no hours of its own; it replaces a host on entry, so it can only reach the
    player during the hours that host is available. Tasha is the case that proved
    it: `tasha_walks_in` is bound to the bathroom and her own bathroom row is
    17:00-18:00, but it rides `wash`, which is shut 17:00-22:00. Scoring the row
    "substitution" on the canvas's own existence called an empty hour backed.
    """
    # ⚠️ Keyed by the ROW, not the room — start_time is part of it. @nate is in
    # nate_room twice (awake at 22:00, asleep at 00:00) and only the second is
    # exempt; a room-level key would have excused both.
    key = (npc["id"], row["location"], row["start_time"])
    if key in OCCUPANCY_ROWS:
        return "occupancy", OCCUPANCY_ROWS[key], set()

    want = set(row["weekdays"])
    backed, why, subs = set(), [], []

    for c in here:
        if not c["active"]:
            continue
        mine = c["npc"] == npc["id"]
        if mine and c["sub"]:
            subs.append(c)
            continue
        if not c["repeatable"] or c["random"]:
            continue
        # A portrait needs the canvas bound to HER. Coverage only needs her to
        # speak on a screen that exists in this room — see speakers_of().
        if not (mine or npc["id"] in c["speakers"]):
            continue
        days = live_days(row, c)
        if days:
            backed |= days
            why.append(f"{c['id']}{'' if mine else ' (speaks)'}")

    if not want - backed:
        return ("portrait" if any(" (speaks)" not in w for w in why) else "covered",
                ", ".join(why), set())

    if subs and not backed:
        live_subs = []
        for c in subs:
            for host in hosts_of.get(c["id"], []):
                if live_days(row, host):
                    live_subs.append(f"{c['id']} on {host['id']}")
                    break
        if live_subs:
            return "substitution", ", ".join(live_subs), set()
        dead_subs = ", ".join(c["id"] for c in subs)
        hosted = ", ".join(h["id"] for c in subs for h in hosts_of.get(c["id"], [])) or "no host"
        return "DEAD", (f"{dead_subs} is bound here but only runs as a substitution "
                        f"on {hosted}, which is not live in these hours"), want

    detail = (f"{len(here)} canvas(es) at {row['location']}"
              + (f"; backed only by {', '.join(why)}" if why else ", none of them hers"))
    return "DEAD", detail, want - backed


def main():
    slug = sys.argv[1] if len(sys.argv) > 1 else "the_balance"
    merged = pathlib.Path(f"games/{slug}/toml_phases/7_final_game.toml")
    if not merged.exists():
        sys.exit(f"no merged TOML at {merged} — run merge_toml_phases.py first")

    game = tomllib.loads(merged.read_text(encoding="utf-8"))
    canvases = [canvas_facts(c) for c in game.get("canvases", [])]
    by_location = {}
    for c in canvases:
        by_location.setdefault(c["location"], []).append(c)

    # Where each NPC's schedule can ever put them — the mirror question.
    stands_at = {}
    for npc in game.get("npcs", []):
        stands_at[npc["id"]] = {s.get("location")
                                for s in (npc.get("schedules") or [])}

    # child canvas id -> the host canvases that name it as a substitution target.
    # The rule lives on the HOST (gates.py:3272-3283), never on the walk-in.
    hosts_of = {}
    for c in game.get("canvases", []):
        host = canvas_facts(c)
        for rule in ((c.get("trigger") or {}).get("substitutions") or []):
            tgt = rule.get("target_canvas_id")
            if tgt:
                hosts_of.setdefault(tgt, []).append(host)

    rows, dead, deferred, capped, ladder, stranded = [], [], [], [], [], []
    for npc in game.get("npcs", []):
        for sched in npc.get("schedules", []) or []:
            row = {
                "location": sched.get("location"),
                "weekdays": sched.get("weekdays", list(range(7))),
                "start_time": sched.get("start_time", "00:00"),
                "end_time": sched.get("end_time", "23:59"),
            }
            verdict, detail, dead_days = classify(
                row, npc, by_location.get(row["location"], []), hosts_of)
            entry = (npc["name"], npc["id"], row, verdict, detail, dead_days)
            rows.append(entry)
            if verdict == "DEAD":
                (deferred if (npc["id"], row["location"]) in DEFERRED_ROWS
                 else dead).append(entry)

    for c in canvases:
        if not (c["npc"] and c["repeatable"] and not c["sub"] and not c["random"]):
            continue
        # ⚠️ A CAP IS ONLY A DEFECT ON A SURFACE THAT IS MEANT TO STAND. Two things
        # make a canvas a dated event rather than a standing one, and both count:
        # trigger `conditions` that close it for good (`nate_door` is
        # `nate_seen is_false`; the dares chain on `dare_chain`), and a trigger
        # SCHEDULE that already narrows it (`friday_payment` fires on a Friday, and
        # once that Friday is correct). A capped canvas with neither is a person
        # who is supposed to be there every day and is deleted by her own first
        # click.
        if c["max_per_day"]:
            (ladder if (c["gated"] or c["schedules"]) else capped).append(c)
        # The mirror of a dead row: a portrait bound to a room its own NPC is
        # never scheduled into. renderNpcPortraits filters on
        # getNpcLocation(slug).location === locationId (v2.py:5281-5291), so this
        # canvas cannot render a portrait on any day at any hour.
        if c["location"] not in stands_at.get(c["npc"], set()):
            stranded.append(c)

    backed = len(rows) - len(dead) - len(deferred)
    print(f"\n  presence — {slug}")
    print(f"  {len(rows)} schedule row(s): {backed} backed, "
          f"{len(deferred)} deferred, {len(dead)} DEAD · "
          f"{len(capped)} standing portrait(s) day-capped, "
          f"{len(ladder)} on a ladder, {len(stranded)} stranded\n")

    if dead:
        print("  DEAD — her face is on the door and the room is empty")
        for name, _, row, _, detail, dead_days in dead:
            span = " ".join(DAYS[d] for d in row["weekdays"])
            print(f"    {name:6} {row['location']:20} "
                  f"{row['start_time']}-{row['end_time']}  [{span}]")
            print(f"           dead on: {' '.join(DAYS[d] for d in sorted(dead_days))}")
            print(f"           {detail}")
        print()
    else:
        print("  no dead rows — everybody scheduled into a room has something in it\n")

    if stranded:
        print("  STRANDED — bound to a room its own NPC is never scheduled into")
        for c in stranded:
            print(f"    {c['id']:20} @{c['location']:18} "
                  f"{c['npc']} never stands there — this portrait cannot render")
        print()

    if capped:
        print("  DAY-CAPPED ON THE TRIGGER — the cap deletes the person, not the act")
        for c in capped:
            print(f"    {c['id']:20} @{c['location']:18} "
                  f"max_triggers_per_day = {c['max_per_day']}  (no trigger conditions)")
        print("    (move it onto the choice as a `_today` flag cleared in "
              "[engine.daily_tick] — engine.md §28,")
        print("     and §28.1: the flag goes on the CHOICE, never on a node exit)")
        print()

    if ladder:
        print("  day-capped, and that is correct — an arc step or a dated event, not a")
        print("  standing surface. Reported so the distinction stays visible.")
        for c in ladder:
            why = "conditions" if c["gated"] else "a trigger schedule"
            print(f"    {c['id']:20} @{c['location']:18} narrowed by {why}")
        print()

    if deferred:
        print("  DEFERRED — real, and LO's call to leave (2026-09-16)")
        for name, npc_id, row, _, _, _ in deferred:
            days = " ".join(DAYS[d] for d in row["weekdays"])
            print(f"    {name:6} {row['location']:20} "
                  f"{row['start_time']}-{row['end_time']}  [{days}]")
            print(f"           {DEFERRED_ROWS[(npc_id, row['location'])]}")
        print()

    print("  A LIST, NEVER A SCORE. A schedule row needs a SURFACE, not necessarily a")
    print("  hub — a room scene covering several people at once counts, and so does an")
    print("  occupancy job. See process/README.md §6.\n")
    return 1 if (dead or capped or stranded) else 0


if __name__ == "__main__":
    sys.exit(main())
