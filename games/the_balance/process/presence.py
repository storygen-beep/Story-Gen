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

⚠️ SINCE THE TWO PARKS OF 2026-09-19 THE BASELINE IS NOT ZERO, AND THAT IS
EXPECTED. The undesigned content went first and the climbs went after it
(games/the_balance/parked/README.md), and every card either park took leaves its
row with nothing on it. After both, HEAD reports:

    13 DEAD       — Gil kitchen 18:00 and master bedroom · Owen's office · Nate's
                    kitchen, front room ×2 and room · Tasha ×3 · Lynn's master
                    bedroom · Jules on the quad and at the union
    0 day-capped · 0 stranded · 1 DEFERRED (Cara's bench)

Those rows are sheets/BASE.md's to decide: a row's card is block 2. Until then
they are listed every run, so that a dead row stays something LO can see rather
than something the instrument quietly stopped mentioning. The DEFERRED row is
LO's call from 2026-09-16 and is reprinted for the same reason.
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
    # ⚠️ PARKED 2026-09-19 (the climbs): ("npc_gil", "the_master_bedroom", "21:00"),
    # "the other half of the same door". Its surface, `master_bedroom`, went with the
    # house doors (games/the_balance/parked/climbs/), so the row is DEAD and says so.
    ("npc_lynn", "the_kitchen", "19:00"):
        "she is the CONDITION for dinner, not a guest at it — `dinner`'s trigger is "
        "`npc_at_location npc_lynn is_present`, so this row is what makes that scene "
        "exist on the four nights she is off the ward. She does not speak in it.",

    # --- her week, 2026-09-20 -------------------------------------------------
    # sheets/people/her_mum.md put fifty-odd rows where there were two. Most of them
    # are backed: every chore she does has a `mum_*` canvas carrying her own hours,
    # and every chore row has a twin that twin_rows() exempts structurally.
    #
    # What is below is the other kind — the rows whose whole job is to put her body
    # in a room. Asleep, changing, in the bath. A body asleep is never a thing to
    # click, and the two hours she has the bathroom door shut are block 4 of
    # sheets/BASE.md, not a gap somebody forgot.
    #
    # ⚠️ THE OLD REASONS AT ff91336 SAID "NEVER TOUCHED" AND THAT IS OVERRULED.
    # LO, 2026-09-19: "She is an npc that can be conquired too… Dont restrict it."
    # Her ladder is block 5. What these rows buy is written below; what they forbid
    # is nothing.
    ("npc_lynn", "the_master_bedroom", "00:00"):
        "asleep, the small hours of every night she is not on the ward.",
    ("npc_lynn", "the_master_bedroom", "06:45"):
        "up and dressing, the fifteen minutes before a ward day starts. Her clothes "
        "change in this room five times a day and each change is its own short row.",
    ("npc_lynn", "the_master_bedroom", "07:45"):
        "up and dressing on a Sunday, the one morning she gets an hour back.",
    ("npc_lynn", "the_master_bedroom", "08:30"):
        "changing into the coat she goes out in, before the strip.",
    ("npc_lynn", "the_master_bedroom", "09:00"):
        "changing into nightwear at nine in the morning, off a ward night.",
    ("npc_lynn", "the_master_bedroom", "09:15"):
        "asleep after a ward night, Tue/Thu/Sat, right through to three. THE ROW "
        "the_house_day.md has been asking for since it was written — her mum asleep "
        "down the hall on a weekday morning. What it buys is the quiet house her own "
        "page counts on; the scene that belongs in it is still unwritten.",
    ("npc_lynn", "the_master_bedroom", "11:00"):
        "back into home clothes with the shopping still in the hall.",
    ("npc_lynn", "the_master_bedroom", "15:00"):
        "asleep before a night shift on Mon/Wed/Fri, and up and dressing on "
        "Tue/Thu/Sat — two rows, one key, both of them a body and neither of them a "
        "surface. The afternoon sleep is what people who work nights actually do.",
    ("npc_lynn", "the_master_bedroom", "18:30"):
        "getting into the ward uniform. Fifteen minutes, three nights a week.",
    ("npc_lynn", "the_master_bedroom", "20:30"):
        "into nightwear, off a day at home.",
    ("npc_lynn", "the_master_bedroom", "20:45"):
        "in bed with the lamp on and the door not quite shut. The hour before she is "
        "asleep, and the second body behind that door.",
    ("npc_lynn", "the_master_bedroom", "21:30"):
        "changing into nightwear on a Sunday.",
    ("npc_lynn", "the_master_bedroom", "21:45"):
        "in bed on a Sunday, not asleep yet.",
    ("npc_lynn", "the_master_bedroom", "22:00"):
        "asleep, every night she is in this house. What it buys is the house her own "
        "page describes as asleep after ten.",
    ("npc_lynn", "the_bathroom", "08:30"):
        "in the bath, washing a ward night off. Same job as @nate's 07:00 shower row "
        "— it is what makes the bathroom taken. Walking in on it is block 4.",
    ("npc_lynn", "the_bathroom", "18:00"):
        "in the bath before a ward night, the half hour her own page calls the one "
        "that is hers. Walking in on it is block 4.",
    ("npc_lynn", "the_bathroom", "20:30"):
        "in the bath on a Sunday. Walking in on it is block 4.",
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
        "addressed": addressed_of(canvas),
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


def addressed_of(canvas):
    """Every NPC this canvas asks the engine about being HERE, anywhere in it.

    ⚠️ THE THIRD WAY A ROW CAN BE BACKED, ADDED 2026-09-20 WITH HER MUM'S WEEK.
    A row is backed when standing in that room while she is in it gives the player
    something that knows she is there. Two ways were already understood: the canvas
    is bound to her (`npc`), or she speaks on it (speakers_of). This is the third —
    a canvas that gates a choice or a prose band on
    `npc_at_location <her> is_present`.

    chores.md is what made it necessary. Her mum's fifty rows are backed by the four
    room chore canvases, whose help / take-it-over choices and prose bands appear
    only when she is standing at the chore. Nothing on those canvases carries an
    `npc` key and she does not speak on them, so without this every one of those
    rows reported dead and the instrument would have been describing its own model
    rather than the game.

    ⚠️ is_present ONLY. `is_absent` is the opposite claim — a screen that exists
    BECAUSE she is not there backs nothing about her being there.
    """
    found = set()

    def walk(node):
        if isinstance(node, dict):
            if (node.get("type") == "npc_at_location"
                    and node.get("operator") == "is_present"
                    and node.get("npc_id")):
                found.add(node["npc_id"])
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)

    walk(canvas)
    return found


def twin_rows(scheds):
    """{index of a fallback row: what it falls back from}, for one NPC's rows.

    A row is a TWIN when an earlier row covers exactly the same weekdays and window,
    carries a `when`, and this one does not. The engine walks rows in order and takes
    the first match (v2.py:3661-3669), so the ungated one is precisely what happens
    when the gated one's condition fails — a fallback position, not a surface.

    ⚠️ STRUCTURAL, so it cannot be gamed by naming. The moment a twin stops matching
    its gated row's window it stops being a twin and goes back to being judged.
    """
    out = {}
    for i, s in enumerate(scheds):
        if s.get("when"):
            continue
        window = (tuple(s.get("weekdays", [])), s.get("start_time"), s.get("end_time"))
        for earlier in scheds[:i]:
            if not earlier.get("when"):
                continue
            if (tuple(earlier.get("weekdays", [])), earlier.get("start_time"),
                    earlier.get("end_time")) == window:
                out[i] = (f"{earlier.get('location')} {earlier.get('start_time')}"
                          f"-{earlier.get('end_time')}")
                break
    return out


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

    if row.get("_twin_of"):
        # ⚠️ A TWIN IS AN OCCUPANCY ROW BY CONSTRUCTION, AND IT IS EXEMPT AS A CLASS
        # RATHER THAN AS FORTY-ODD IDENTICAL SENTENCES. chores.md: do the laundry
        # yourself and "her mum's hour on it drops and she sits in the front room
        # instead." The twin is that row — same window, no `when`, so it catches her
        # the moment the chore row's gate fails. Its whole job is to put her body
        # somewhere; there is nothing to do at it and there was never meant to be.
        # ⚠️ The exemption is STRUCTURAL, not a name: twin_rows() below only marks a
        # row that really does sit behind a gated row on the same window. A twin that
        # stops matching its chore row stops being excused.
        return "occupancy", f"the row {row['_twin_of']} falls back to when it is done", set()

    want = set(row["weekdays"])
    backed, why, subs = set(), [], []
    portrait = False

    for c in here:
        if not c["active"]:
            continue
        mine = c["npc"] == npc["id"]
        if mine and c["sub"]:
            subs.append(c)
            continue
        if not c["repeatable"] or c["random"]:
            continue
        # A portrait needs the canvas bound to HER. Coverage only needs her to speak
        # on a screen that exists in this room (speakers_of), or the screen to ask
        # whether she is standing here (addressed_of).
        speaks = npc["id"] in c["speakers"]
        asks = npc["id"] in c["addressed"]
        if not (mine or speaks or asks):
            continue
        days = live_days(row, c)
        if days:
            backed |= days
            label = "" if mine else (" (speaks)" if speaks else " (asks for her)")
            why.append(f"{c['id']}{label}")
            if mine:
                portrait = True

    if not want - backed:
        return ("portrait" if portrait else "covered", ", ".join(why), set())

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
        twins = twin_rows(npc.get("schedules", []) or [])
        for i, sched in enumerate(npc.get("schedules", []) or []):
            row = {
                "location": sched.get("location"),
                "weekdays": sched.get("weekdays", list(range(7))),
                "start_time": sched.get("start_time", "00:00"),
                "end_time": sched.get("end_time", "23:59"),
                "_twin_of": twins.get(i),
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
