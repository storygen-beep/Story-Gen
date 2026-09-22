#!/usr/bin/env python3
"""The generated half of rounds 1 and 2 of sheets/BASE.md — a SOURCE, not a probe.

    python3 games/the_balance/process/gen_week.py [sleep|chores|mum|all]

Three blocks of TOML are too repetitive to hand-write and too load-bearing to get
wrong, so they are generated from the tables below and spliced into the phase files
in place. Edit a table here and re-run; never hand-edit the output.

⚠️ THIS FILE IS IN process/ AND NOT IN THE SCRATCHPAD, for the reason
process/README.md O12 gives about the eight walkthrough scripts that were written
during slices 1-8 and wiped with the session: a generator whose table dies is a
block of TOML nobody can safely change again. The output carries a pointer back
here.

⚠️ AND IT IS ONE FILE ON PURPOSE. Her mum's chore hours are written down once, in
MUM_ROWS, and the canvases that offer to help her with a chore read their trigger
schedules straight off it. Two tables would drift, and the failure would be silent:
the help would be offered while she was in the bath.

The three blocks:

  sleep   her_week.md's alarm. One choice per (bedtime band, wake hour), because
          there is no sleep-until-hour key in the engine.
  chores  chores.md's nine, four room canvases plus one canvas per chore her mum
          does, the second gated to the hours she is actually on it.
  mum     her_mum.md's week. Fifty-odd [[npcs.schedules]] rows where there were two.
"""
import pathlib
import sys

REPO_ROOT = pathlib.Path(__file__).resolve().parents[3]
ACTIVITIES = REPO_ROOT / "games/the_balance/toml_phases/3_activities.toml"
PEOPLE = REPO_ROOT / "games/the_balance/toml_phases/1_metadata_and_locations.toml"

K, B, F, M, S = ("the_kitchen", "the_bathroom", "the_front_room",
                 "the_master_bedroom", "the_strip")
WARD, AFTER, SUN = [0, 2, 4], [1, 3, 5], [6]


# ─────────────────────────────────────────────────────────────────────────────
# Shared condition writers
# ─────────────────────────────────────────────────────────────────────────────

def c_flag(key, op):
    return (f'{{ type = "flag", subject = "player", flag_key = "{key}", '
            f'operator = "{op}" }}')


def c_window(start, end):
    return f'{{ type = "time_of_day", start_time = "{start}", end_time = "{end}" }}'


def c_npc_at(npc_id, room, op):
    return (f'{{ type = "npc_at_location", npc_id = "{npc_id}", '
            f'location_id = "{room}", operator = "{op}" }}')


def c_lynn(room, op):
    return c_npc_at("npc_lynn", room, op)


def c_tight(op, value):
    return (f'{{ type = "trait", subject = "player", trait_key = "fridays_missed", '
            f'operator = "{op}", value = {value} }}')


def conditions(items, key="conditions"):
    body = ",\n  ".join(items)
    return f'{key} = {{ version = "1.0", logic = "AND", items = [\n  {body},\n] }}\n'


def pool(paragraphs):
    out = ["[[canvases.nodes.blocks]]", 'type = "block_pool"', "blocks = ["]
    out += [f'  {{ type = "paragraph", content = "{p}" }},' for p in paragraphs]
    return "\n".join(out + ["]", ""])


def group(items, paragraphs):
    body = ",\n  ".join(items)
    out = ["[[canvases.nodes.blocks]]", 'type = "group"',
           f'props = {{ conditions = {{ version = "1.0", logic = "AND", items = [\n  {body},\n] }} }}',
           "blocks = ["]
    out += [f'  {{ type = "paragraph", content = "{p}" }},' for p in paragraphs]
    return "\n".join(out + ["]", ""])


def choice(text, room, minutes=None, items=None, effects=None, flags=None):
    out = ["[[canvases.nodes.exit_block.choices]]",
           f'text       = "{text}"',
           'targetType = "location"',
           f'locationId = "{room}"']
    if minutes is not None:
        out.append(f"time_progression_minutes = {minutes}")
    body = "\n".join(out) + "\n"
    if items:
        body += conditions(items)
    if effects:
        body += "effects     = [" + ", ".join(effects) + "]\n"
    if flags:
        body += "flagEffects = [" + ", ".join(flags) + "]\n"
    return body + "\n"


def splice(path, start_markers, end_markers, block):
    text = path.read_text()
    i = next(text.index(m) for m in start_markers if m in text)
    j = next(text.index(m) for m in end_markers if m in text)
    path.write_text(text[:i] + block + "\n" + text[j:])


# ─────────────────────────────────────────────────────────────────────────────
# 1 · SLEEP — the alarm she sets
# ─────────────────────────────────────────────────────────────────────────────

WAKE_WORD = {6: "six", 7: "seven", 8: "eight", 9: "nine"}
HALF_WORD = {4.5: "four and a half", 5.5: "five and a half", 6.5: "six and a half",
             7.5: "seven and a half", 8.5: "eight and a half", 9.5: "nine and a half",
             10.5: "ten and a half", 11.5: "eleven and a half", 12.5: "twelve and a half"}

# (band start, band end, the minute of the day the band is anchored on)
BANDS = [("20:00", "21:00", 20 * 60 + 30), ("21:00", "22:00", 21 * 60 + 30),
         ("22:00", "23:00", 22 * 60 + 30), ("23:00", "00:00", 23 * 60 + 30),
         ("00:00", "01:00", 30), ("01:00", "02:00", 90),
         ("02:00", "03:00", 150), ("03:00", "04:00", 210)]

DECAY = 20          # [player.trait_decay] rest — see the ⚠️ below
FLOOR_HOURS = 4     # her_week.md's table stops at four
NO_ALARM = "Don't set one. Sleep until you wake."

SLEEP_HEAD = '''# --- SLEEP · the alarm she sets, and what the hours are worth ----------------
# ⚠️ WITHOUT THIS FRIDAY IS UNREACHABLE. advanceDay() is what rolls the day name,
# the day counter, the week on a Monday, [player.trait_decay] and the
# [engine.daily_tick] clears — and the only thing that calls it is the clock
# crossing midnight. Before this canvas the sidebar's wait buttons were the sole
# way to get there, and rest decayed with nothing to refill it.
#
# her_week.md: "She goes to bed when she likes and sets the alarm herself." There
# is no sleep-until-hour key, so the alarm is built out of the two primitives that
# do exist — a `time_of_day` condition for when she got in, and a fixed
# time_progression_minutes on each choice. One choice per (band, wake hour). Only
# one band's worth ever renders, so she sees four buttons and a fifth for no alarm.
#
# ⚠️ REST IS THE HOURS SLEPT, NOT THE ALARM. Eight hours is 100 and it is about
# 12.5 an hour below that, which is the table on her_week.md. Nothing under four
# hours is offered. Over eight gives nothing.
#
# ⚠️ AND THE +20 ON EVERY PRE-MIDNIGHT BAND IS NOT A TYPO. A choice's effects are
# emitted BEFORE advanceTime (v2.py:13923), so a sleep that crosses midnight has
# its `set` immediately decayed by [player.trait_decay] rest = 20. The bands that
# cross compensate; the bands after midnight do not, because their decay already
# fired while she was awake. ⚠️ CHANGE trait_decay.rest AND EVERY NUMBER BELOW IS
# WRONG BY THE DIFFERENCE.
#
# ⚠️ ONE SLEEP A CALENDAR DAY, which is max_triggers_per_day and not a flag. Bed at
# one in the morning spends that day's sleep, so she cannot sleep again until the
# next midnight. That is her_week.md working — staying up is allowed and it costs.
#
# Generated by games/the_balance/process/gen_week.py. Edit the table there.

[[canvases]]
id   = "sleep"
name = "Sleep"
description = "She sets the alarm herself and the rest she gets is the hours she slept. Eight hours is full. The clock crossing midnight is what fires advanceDay, so this is still the week's only engine."

[canvases.trigger]
location      = "her_room"
is_repeatable = true
max_triggers_per_day = 1
priority      = 4
is_active     = true

[[canvases.nodes]]
id   = "base"
name = "Bed"

[[canvases.nodes.blocks]]
type = "block_pool"
blocks = [
  { type = "paragraph", content = "You put the phone face down on the books and get in. The landing light is still on under the door and somebody is still up, but neither of those things is going to keep you awake." },
  { type = "paragraph", content = "The alarm is the last thing you touch, and whatever you set it for is what you get. The house does its noises — the heating, a door, a car outside — but you sleep through all of it." },
  { type = "paragraph", content = "You are asleep before you have finished deciding what tomorrow costs. That is the one thing this room is reliably good for." },
  { type = "paragraph", content = "Shoes off, jeans on the chair, door pushed to. It is not shut, because his rule about the door is one you keep without thinking about it now." },
]

[canvases.nodes.exit_block]
type = "choices"

'''


def rest_for(hours):
    """her_week.md: eight hours is 100, about 12.5 an hour below it, nothing above."""
    return min(100, int(12.5 * hours + 0.5))


def build_sleep():
    out = [SLEEP_HEAD]
    for start, end, anchor in BANDS:
        out.append(f"# In at about {start[:2]}:30.\n")
        for wake in (6, 7, 8, 9):
            minutes = (wake * 60 - anchor) % 1440
            hours = minutes / 60
            if hours < FLOOR_HOURS:
                continue
            crosses = anchor + minutes >= 1440
            value = rest_for(hours) + (DECAY if crosses else 0)
            out.append(choice(
                f"Set it for {WAKE_WORD[wake]} — {HALF_WORD[hours]} hours.",
                "her_room", minutes, [c_window(start, end)],
                [f'{{ targetType = "player", trait = "rest", op = "set", value = {value} }}']))
        out.append("\n")

    out.append("# No alarm — ten hours, whatever time she lies down. The two windows are one\n"
               "# button to the player; they differ only by whether the sleep crosses midnight,\n"
               "# and together they cover all twenty-four hours exactly once.\n")
    for window, value in ((("14:00", "00:00"), 100 + DECAY), (("00:00", "14:00"), 100)):
        out.append(choice(NO_ALARM, "her_room", 600, [c_window(*window)],
                          [f'{{ targetType = "player", trait = "rest", op = "set", value = {value} }}']))
    return "".join(out).rstrip() + "\n"


# ─────────────────────────────────────────────────────────────────────────────
# 2 · HER MUM'S WEEK — the table both the rows and the chore canvases read
# ─────────────────────────────────────────────────────────────────────────────

# (weekdays, start, end, location, activity, chore key or None)
MUM_ROWS = [
    # ── the ward day. She slept here and she goes in tonight.
    (WARD, "06:45", "07:00", M, "up, getting into the clothes she does the house in", None),
    (WARD, "07:00", "07:30", K, "in home clothes, doing breakfast with the radio on", "breakfast"),
    (WARD, "07:30", "08:00", K, "eating standing up, one eye on the clock", None),
    (WARD, "08:00", "08:30", K, "at the sink with the breakfast things", "breakfast_dishes"),
    (WARD, "08:30", "08:45", M, "changing into the coat and the shoes she goes out in", None),
    # 08:45-09:00 is the walk to the stop. No row, so she is out of the house.
    (WARD, "09:00", "11:00", S, "out on the strip with a list, in her going-out coat", None),
    (WARD, "11:00", "11:15", M, "back into home clothes with the shopping still in the hall", None),
    (WARD, "11:15", "12:00", K, "putting the shopping away, tins first", None),
    (WARD, "12:00", "12:30", K, "doing lunch for whoever is in", "lunch"),
    (WARD, "12:30", "13:00", K, "sat down to eat for half an hour", None),
    (WARD, "13:00", "13:30", K, "at the sink again", "lunch_dishes"),
    (WARD, "13:30", "14:30", B, "sorting the washing out on the bathroom floor", "laundry"),
    (WARD, "14:30", "15:00", F, "going along the shelf with a cloth", "dusting"),
    (WARD, "15:00", "18:00", M, "asleep with the curtains shut, getting ahead of the night", None),
    (WARD, "18:00", "18:30", B, "in the bath with the door shut, the half hour that is hers", None),
    (WARD, "18:30", "18:45", M, "getting into the ward uniform", None),
    # 18:45 to 08:00 she is on the ward. No row at all — the ward is not a place in
    # this game and does not need to be. A gap reads as absent (v2.py:3737).

    # ── the morning after. She comes in off the ward and sleeps the day.
    (AFTER, "08:00", "08:30", K, "in off the ward, still in uniform, eating without tasting it", None),
    (AFTER, "08:30", "09:00", B, "in the bath, washing the shift off", None),
    (AFTER, "09:00", "09:15", M, "changing into nightwear with the light still on", None),
    (AFTER, "09:15", "15:00", M, "asleep, curtains shut against the morning", None),
    (AFTER, "15:00", "15:15", M, "up, into home clothes", None),
    (AFTER, "15:15", "15:45", K, "eating a late lunch on her own", None),
    (AFTER, "15:45", "16:45", B, "sorting the washing out on the bathroom floor", "laundry"),
    (AFTER, "16:45", "17:15", F, "going along the shelf with a cloth", "dusting"),
    (AFTER, "17:15", "18:00", F, "sat down with the TV on, her one hour off", None),
    (AFTER, "18:00", "19:00", K, "doing dinner for four", "dinner"),
    (AFTER, "19:00", "20:00", K, "at the table, everybody in one room", None),
    (AFTER, "20:00", "20:30", K, "at the sink with the dinner things", "dinner_dishes"),
    (AFTER, "20:30", "20:45", M, "into nightwear", None),
    (AFTER, "20:45", "22:00", M, "in bed with the lamp on and the door not quite shut", None),

    # ── Sunday. The one full day she is home.
    (SUN, "07:45", "08:00", M, "up, into home clothes", None),
    (SUN, "08:00", "08:30", K, "doing a proper breakfast for once", "breakfast"),
    (SUN, "08:30", "09:00", K, "at the table with whoever got up", None),
    (SUN, "09:00", "09:30", K, "at the sink", "breakfast_dishes"),
    (SUN, "09:30", "11:30", B, "the big wash, with the machine going twice", "laundry"),
    (SUN, "11:30", "12:00", F, "going along the shelf with a cloth", "dusting"),
    (SUN, "12:00", "12:30", K, "doing lunch", "lunch"),
    (SUN, "12:30", "13:00", K, "sat down to eat", None),
    (SUN, "13:00", "13:30", K, "at the sink", "lunch_dishes"),
    (SUN, "13:30", "18:00", F, "in the chair with the TV on, the one afternoon she gets", None),
    (SUN, "18:00", "19:00", K, "doing dinner for four", "dinner"),
    (SUN, "19:00", "20:00", K, "at the table, everybody in one room", None),
    (SUN, "20:00", "20:30", K, "at the sink with the dinner things", "dinner_dishes"),
    (SUN, "20:30", "21:30", B, "in the bath with the door shut", None),
    (SUN, "21:30", "21:45", M, "changing into nightwear", None),
    (SUN, "21:45", "22:00", M, "in bed, not asleep yet", None),

    # ── the nights, split at midnight. Mon/Wed/Fri she is on the ward and there is
    # nothing to split.
    #
    # ⚠️ "00:00" AND NOT "23:59". end_time is EXCLUSIVE (v2.py:4100), so a row ending
    # at 23:59 leaves her absent from her own bed for that one minute. An end of
    # 00:00 takes the wrap branch — `now >= 22:00 || now < 0` — which covers 23:59
    # and cannot bleed into the next day, because `now < 0` is never true.
    ([1, 3, 5, 6], "22:00", "00:00", M, "asleep, with the landing light off", None),
    ([0, 2, 4], "00:00", "06:45", M, "asleep, with the landing light off", None),
    (SUN, "00:00", "07:45", M, "asleep — Saturday night is the one she gets an hour back on", None),
]

MUM_HEAD = '''# ⚠️ HER WEEK IS sheets/people/her_mum.md, 2026-09-20. Fifty-odd rows where there
# were two. Three kinds of day — the ward day on Monday, Wednesday and Friday, the
# morning after on Tuesday, Thursday and Saturday, and Sunday. She is on the ward
# from 18:45 to 08:00 on ward nights, which is simply NO ROW: the ward is not a
# location in this game and a gap already reads as absent (v2.py:3737).
#
# ⚠️ HER CLOTHES LIVE IN THE ACTIVITY STRING. Home clothes, nightwear, the ward
# uniform and the coat she goes out in, changed in the master bedroom every time
# the next place needs a different set. Her PICTURE does not change with them — a
# row has no image of its own, and the page parks that as engine work.
#
# ⚠️ EVERY NIGHT IS TWO ROWS. isCurrentTimeSlot wraps past midnight correctly
# (v2.py:4097) but the weekday list is read against the day the clock is on, so a
# single 22:00-06:45 row on [1,3,5] would put her in bed at two in the MORNING on
# Tuesday instead of on Wednesday.
#
# ⚠️ A CHORE ROW IS FOLLOWED BY ITS TWIN. chores.md: do the laundry, or say "I'll
# do it", and "her mum's hour on it drops and she sits in the front room instead."
# The chore row carries `when` on that chore's flag; the row straight after it is
# the same window in the front room with no `when`, and the first match wins
# (v2.py:3661-3669). Delete a twin and she stands in a finished chore forever.
#
# ⚠️ npc_at_location IS REJECTED inside a `when` (template_import.py:3616) — it
# would recurse through getNpcLocation. Flags only, and `version = "1.0"` or the
# gate fails OPEN and the row is never really gated at all.
#
# Generated by games/the_balance/process/gen_week.py. Edit the table there.

'''


def build_mum():
    out = [MUM_HEAD]
    for weekdays, start, end, loc, activity, chore in MUM_ROWS:
        days = ", ".join(str(d) for d in weekdays)
        row = ["[[npcs.schedules]]", f'location   = "{loc}"',
               f"weekdays   = [{days}]", f'start_time = "{start}"',
               f'end_time   = "{end}"', f'activity   = "{activity}"']
        if chore:
            row.append(conditions([c_flag(f"chore_done_{chore}", "is_false")], key="when").rstrip())
        out.append("\n".join(row) + "\n\n")
        if chore:
            twin = ["[[npcs.schedules]]", f'location   = "{F}"',
                    f"weekdays   = [{days}]", f'start_time = "{start}"',
                    f'end_time   = "{end}"',
                    'activity   = "sat down in the front room, because it is already done"']
            out.append("\n".join(twin) + "\n\n")
    return "".join(out).rstrip() + "\n"


# ─────────────────────────────────────────────────────────────────────────────
# 3 · THE CHORES — four room canvases, plus one per chore her mum does
# ─────────────────────────────────────────────────────────────────────────────

# key, room, the label, the window the PLAYER can do it in
CHORES = [
    ("breakfast",        K, "Cook breakfast.",          "07:00", "09:00"),
    ("breakfast_dishes", K, "Do the breakfast dishes.",  "08:00", "10:00"),
    ("lunch",            K, "Cook lunch.",               "11:30", "13:00"),
    ("lunch_dishes",     K, "Do the lunch dishes.",      "13:00", "14:30"),
    ("dinner",           K, "Cook dinner.",              "17:30", "19:00"),
    ("dinner_dishes",    K, "Do the dinner dishes.",     "20:00", "21:30"),
    ("laundry",          B, "Put the laundry on.",       "08:00", "22:00"),
    ("dusting",          F, "Do the dusting.",           "08:00", "22:00"),
    ("bins",             G := "the_garage", "Take the bins out.", "06:00", "10:00"),
]

# chores.md: "The bins are only ever hers." Her mum is never on that one.
NO_MUM = {G}
PAY, HALF, HOUR = 5, 30, 60

# What she is doing, on the canvas that offers to take it off her.
MUM_AT = {
    "breakfast": "Your mum is at the hob in her home clothes with two pans going, doing it at the speed of somebody who has done it every morning for years.",
    "breakfast_dishes": "She is at the sink with her sleeves pushed up and the breakfast things stacked beside her, and she has not sat down once since she got up.",
    "lunch": "Your mum is doing lunch for whoever is in the house, which today is you, and she has not asked whether you wanted any.",
    "lunch_dishes": "She is at the sink again. It is the third time she has stood at it today and it is not two o'clock yet.",
    "dinner": "Your mum is doing dinner for four with a shift already behind her, and she will be stood at this for an hour.",
    "dinner_dishes": "The table is cleared and she is at the sink with all of it, and everybody else has gone through to the other room.",
    "laundry": "Your mum is down on the bathroom floor with the pile, pulling darks off the top of it and not looking up at you.",
    "dusting": "Your mum is going along the shelf with a cloth, moving each thing and putting it back down on the same ring it left.",
}

ROOMS = {
    K: dict(cid="chores_kitchen", name="The kitchen list", node="The fridge",
            description=("The six that happen in here, and the list on the fridge saying which "
                         "one pays. One paid a day, five dollars, half an hour each."),
            pool=[
                "Nine lines in @gil's handwriting and a date against one of them. The dated one is worth five dollars and the other eight still have to happen, which is the whole system.",
                "The list is where it always is, held on with the magnet from a tire place. The date is in a different pen from the rest of it, so it is the only thing on there he has looked at twice.",
                "Breakfast, dishes, lunch, dishes, dinner, dishes, then laundry and bins and dusting. One of them pays, and the sink does not care which one it is.",
            ]),
    B: dict(cid="chores_bathroom", name="The washing", node="The machine",
            description=("The laundry, in the room the machine is actually in. Half an hour, and "
                         "it pays if nothing else has today."),
            pool=[
                "The basket by the bath is everybody's and gets emptied by whoever looks at it long enough. The machine is under the window and it takes forty minutes to do its thirty.",
                "Four people's washing goes into one drum and comes back out needing sorting, and the sorting is the part nobody counts as the chore.",
            ]),
    F: dict(cid="chores_front_room", name="The dusting", node="The shelf",
            description=("The dusting, in the room it happens in. Half an hour, and it pays if "
                         "nothing else has today."),
            pool=[
                "The TV is off, so the room is at its most obvious — the shelf, the sill, the tops of the frames nobody looks at until somebody does.",
                "Half an hour of moving things and setting them back exactly where they were. @gil notices when it has not been done, but he has never once said anything when it has.",
            ]),
    G: dict(cid="chores_garage", name="The bins", node="Round the side",
            description=("The bins. Hers and nobody else's, in the morning, half an hour — and it "
                         "pays if nothing else has today."),
            pool=[
                "The bins are round the side and the truck comes at eight, so it is you dragging them to the front in whatever you already have on.",
                "Two of them, and the second one has a wheel that goes its own way. You do it anyway, because the alternative is a week of it getting mentioned.",
            ]),
}

CHORES_HEAD = '''# --- THE CHORES · nine of them, each in its own room at its own hour ---------
# sheets/systems/chores.md, 2026-09-20. The one button on the fridge became four
# room canvases. "She doesn't do chores from the list; she does each one in its
# own room." Half an hour each, one paid a day, five dollars.
#
# ⚠️ WHICH ONE PAYS IS PROSE, NOT MACHINERY, AND THAT IS DELIBERATE. The page has
# Gil dating one line on the list. A condition cannot read the weekday and there is
# no day counter, so a rotating pointer would take seven canvases to express — and
# it would buy nothing, because EVERY CHORE COSTS THE SAME HALF HOUR. There is no
# choice to exploit by picking. So the list says what the page says it says, and
# the mechanic is the one that was already here: the first chore she does each day
# is the one that pays, `chore_paid_today` closes it, and [engine.daily_tick]
# opens it again.
#
# ⚠️ NO max_triggers_per_day AND NO chore_paid_today ON THESE TRIGGERS. Either one
# shuts the whole room after the first chore of the day, and the kitchen has six.
# The per-chore `chore_done_*` flags are what stop a chore being done twice.
#
# ⚠️ HELPING HER IS A SEPARATE CANVAS, AND THAT IS THE WHOLE POINT OF IT. The first
# build of this put "Do it with her." on the room canvas behind
# `npc_at_location npc_lynn is_present` plus the chore's own window — which offered
# to help her with the laundry WHILE SHE WAS IN THE BATH, because the bathroom
# window is 08:00-22:00 and she is in that room for both. Her hours are per
# weekday, a choice cannot read the weekday, and a trigger schedule can: so each
# `mum_*` canvas below carries HER rows, copied off MUM_ROWS in gen_week.py so the
# two cannot drift.
#
# Generated by games/the_balance/process/gen_week.py. Edit the tables there.

'''


def solo_variants(key, room, verb, start, end):
    """Her, on her own. chores.md: "When her mum isn't on a chore, she can do it on her own." """
    done = c_flag(f"chore_done_{key}", "is_false")
    base = [done, c_window(start, end)]
    if room not in NO_MUM:
        base.append(c_lynn(room, "is_absent"))
    unpaid = c_flag("chore_paid_today", "is_false")
    paid = c_flag("chore_paid_today", "is_true")
    cash = [f'{{ targetType = "player", trait = "cash", op = "add", value = {PAY} }}']
    set_done = f'{{ targetType = "player", flag = "chore_done_{key}", op = "set" }}'
    set_paid = '{ targetType = "player", flag = "chore_paid_today", op = "set" }'
    return [
        choice(verb, room, HALF, base + [unpaid, c_tight("lt", 1)], cash, [set_done, set_paid]),
        choice(verb, room, HOUR, base + [unpaid, c_tight("gte", 1)], cash, [set_done, set_paid]),
        choice(verb, room, HALF, base + [paid], None, [set_done]),
    ]


def build_chores():
    out = [CHORES_HEAD]

    for room in (K, B, F, G):
        spec = ROOMS[room]
        parts = ["[[canvases]]", f'id   = "{spec["cid"]}"', f'name = "{spec["name"]}"',
                 f'description = "{spec["description"]}"', "",
                 "[canvases.trigger]", f'location      = "{room}"',
                 "is_repeatable = true", "priority      = 4", "is_active     = true", ""]
        if room == K:
            parts += ['# the_house_day.md: "@gil notices things there — the chores, the hours she',
                      '# keeps, whether Friday got paid." He is in that room morning and evening.',
                      "[[canvases.trigger.substitutions]]",
                      'target_canvas_id = "gil_notices"', "chance = 0.3",
                      conditions([c_npc_at("npc_gil", K, "is_present")]).rstrip(), ""]
        parts += ["[[canvases.nodes]]", 'id   = "base"', f'name = "{spec["node"]}"', ""]
        body = "\n".join(parts)
        if room == K:
            body += group([c_tight("gte", 1)],
                          ["Two more lines on the list than there were, and neither of the new "
                           "ones has a date against it. Neither of them pays, but they are on "
                           "there, so they get done."])
        body += pool(spec["pool"])
        body += "[canvases.nodes.exit_block]\ntype = \"choices\"\n\n"
        for key, r, verb, start, end in CHORES:
            if r != room:
                continue
            body += f"# {key} — {start} to {end}\n"
            body += "".join(solo_variants(key, r, verb, start, end))
        body += choice("Leave it.", room)
        out.append(body)

    # ── one canvas per chore her mum does, carrying HER hours
    out.append(
        "# --- HER MUM, ON ONE OF THEM ------------------------------------------------\n"
        "# chores.md: help her (no five dollars, because it is her job), say you'll do it\n"
        "# (it pays if nothing else has today), or leave her to it. Taking it over sets\n"
        "# the same flag the chore itself sets, which is what drops her row and puts her\n"
        "# in the front room — the `when` on her schedule reads it.\n\n")

    for key, room, verb, _s, _e in CHORES:
        if room in NO_MUM:
            continue
        hours = [(w, s, e) for w, s, e, loc, _a, c in MUM_ROWS if c == key]
        assert hours, f"no MUM_ROWS entry for {key}"
        parts = ["[[canvases]]", f'id   = "mum_{key}"',
                 f'name = "Your mum, on the {key.replace("_", " ")}"',
                 f'description = "She is on it, in {room}, in the hours her own week puts her '
                 f'there. Help, take it over, or leave her to it."', "",
                 "[canvases.trigger]", f'location      = "{room}"',
                 # ⚠️ `npc` is the whole difference between her FACE and a line of text.
                 # A canvas carrying an npcId is dropped from the solo-link bucket
                 # (v2.py:4953) and picked up by the portrait selector instead
                 # (v2.py:5436), which renders her portrait card with her name on it.
                 # Without it these eight were links reading "Your mum, on the dishes"
                 # in a room she was standing in — she was the only named person in the
                 # game with no portrait anywhere. Safe because the portrait path keeps
                 # exactly ONE canvas per NPC per location (v2.py:4928) and these eight
                 # windows never overlap in any of the three rooms.
                 'npc           = "npc_lynn"',
                 "is_repeatable = true", "priority      = 5", "is_active     = true",
                 conditions([c_lynn(room, "is_present"),
                             c_flag(f"chore_done_{key}", "is_false")]).rstrip(), ""]
        for weekdays, s, e in hours:
            parts += ["[[canvases.trigger.schedules]]",
                      "weekdays   = [" + ", ".join(str(d) for d in weekdays) + "]",
                      f'start_time = "{s}"', f'end_time   = "{e}"', ""]
        parts += ["[[canvases.nodes]]", 'id   = "base"', 'name = "She is on it"', "",
                  "[[canvases.nodes.blocks]]", 'type    = "paragraph"',
                  f'content = "{MUM_AT[key]}"', "",
                  "[canvases.nodes.exit_block]", 'type = "choices"', ""]
        body = "\n".join(parts)

        set_done = f'{{ targetType = "player", flag = "chore_done_{key}", op = "set" }}'
        set_paid = '{ targetType = "player", flag = "chore_paid_today", op = "set" }'
        cash = [f'{{ targetType = "player", trait = "cash", op = "add", value = {PAY} }}']
        unpaid = c_flag("chore_paid_today", "is_false")
        paid = c_flag("chore_paid_today", "is_true")

        body += choice("Do it with her.", room, HALF, None, None, [set_done])
        body += choice("Tell her you'll do it.", room, HALF,
                       [unpaid, c_tight("lt", 1)], cash, [set_done, set_paid])
        body += choice("Tell her you'll do it.", room, HOUR,
                       [unpaid, c_tight("gte", 1)], cash, [set_done, set_paid])
        body += choice("Tell her you'll do it.", room, HALF, [paid], None, [set_done])
        body += choice("Leave her to it.", room)
        out.append(body)

    return "".join(out).rstrip() + "\n"


# ─────────────────────────────────────────────────────────────────────────────

JOBS = {
    "sleep": lambda: splice(
        ACTIVITIES,
        ["# --- SLEEP · the alarm she sets", "# --- SLEEP · the only thing that turns the week"],
        ["# --- THE CHORES · nine of them", "# --- THE CHORE LIST · the rule that can be tightened"],
        build_sleep()),
    "chores": lambda: splice(
        ACTIVITIES,
        ["# --- THE CHORES · nine of them", "# --- THE CHORE LIST · the rule that can be tightened"],
        ["# --- THE SHOWER · the only tap `clean` has"],
        build_chores()),
    "mum": lambda: splice(
        PEOPLE,
        ["# ⚠️ HER WEEK IS sheets/people/her_mum.md", "# ⚠️ NEVER TOUCHED. She is the price"],
        ["# --- the two on campus who want nothing from her"],
        build_mum()),
}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for name in (JOBS if which == "all" else [which]):
        JOBS[name]()
        print(f"  {name}: spliced")
