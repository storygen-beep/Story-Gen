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


TWIN_ACTIVITY = "sat down in the front room, because it is already done"


def mum_rows_expanded():
    """Every row her schedule really gets, the twins included.

    ⚠️ THE CARDS READ THIS AND NOT MUM_ROWS. A twin is not in the table — it is made
    here — so a card list built straight off MUM_ROWS would miss nineteen rows, and
    the front room would be empty every single time the player did a chore for her.
    """
    for weekdays, start, end, loc, activity, chore in MUM_ROWS:
        yield weekdays, start, end, loc, activity, chore
        if chore:
            yield weekdays, start, end, F, TWIN_ACTIVITY, None


def build_mum():
    out = [MUM_HEAD]
    for weekdays, start, end, loc, activity, chore in mum_rows_expanded():
        days = ", ".join(str(d) for d in weekdays)
        row = ["[[npcs.schedules]]", f'location   = "{loc}"',
               f"weekdays   = [{days}]", f'start_time = "{start}"',
               f'end_time   = "{end}"', f'activity   = "{activity}"']
        if chore:
            row.append(conditions([c_flag(f"chore_done_{chore}", "is_false")], key="when").rstrip())
        out.append("\n".join(row) + "\n\n")
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
#
# ⚠️ THREE EACH, NOT ONE. Each of these cards comes up two or three times a week and
# the laundry comes up seven, and until 2026-09-22 every one of them carried a single
# paragraph — the same sentence every time. A pool is the only variety available here,
# because block_pool renders as `<<set _bp to random(0,N)>>` and cannot be gated.
MUM_AT = {
    "breakfast": [
        "Your mum is at the hob in her home clothes with two pans going, doing it at the speed of somebody who has done it every morning for years.",
        "Two pans, the kettle and the radio on low. She has the timing of all three in her head and has never once written any of it down.",
        "She is cooking for four at seven in the morning with a shift waiting at the end of the day, and her back is to you the whole time you stand there.",
    ],
    "breakfast_dishes": [
        "She is at the sink with her sleeves pushed up and the breakfast things stacked beside her, and she has not sat down once since she got up.",
        "Everything off the table is on the drainer in the order it came off it. She works down the stack without once looking at how much of it is left.",
        "The water has gone grey and she has not changed it. Four people ate and three of them are already in another room.",
    ],
    "lunch": [
        "Your mum is doing lunch for whoever is in the house, which today is you, and she has not asked whether you wanted any.",
        "She is making enough for two and putting the rest in a box for later, which is how half of what happens in this kitchen gets done twice.",
        "Lunch is whatever is nearest going off. She works that out standing at the open fridge and then just gets on with it.",
    ],
    "lunch_dishes": [
        "She is at the sink again. It is the third time she has stood at it today and it is not two o'clock yet.",
        "Two plates and a pan, which is no time at all, and she does it now because leaving it means doing it later on top of something else.",
        "Her hands are in the water before the table is properly cleared. Nobody carried anything through on their way out.",
    ],
    "dinner": [
        "Your mum is doing dinner for four with a shift already behind her, and she will be stood at this for an hour.",
        "Four of everything, and one of the four has not said what time he is in. She cooks as though he has.",
        "She came in off a night, slept the day, and is now making a meal she will eat last and clear up after on her own.",
    ],
    "dinner_dishes": [
        "The table is cleared and she is at the sink with all of it, and everybody else has gone through to the other room.",
        "The TV is on next door and she is out here with four plates and the pan it was all cooked in. Nobody offered on the way past.",
        "She stacks it, washes it, dries it and puts it away, and the whole thing takes half an hour that nothing else in this house notices.",
    ],
    "laundry": [
        "Your mum is down on the bathroom floor with the pile, pulling darks off the top of it and not looking up at you.",
        "Four people's washing in one heap by the bath, and she is going through it by hand into three piles on the tiles.",
        "She has the machine open and is loading it a handful at a time, checking pockets, because somebody in this house never does.",
    ],
    "dusting": [
        "Your mum is going along the shelf with a cloth, moving each thing and putting it back down on the same ring it left.",
        "She works the sill, then the shelf, then the tops of the frames — the places nobody looks at until they have not been done.",
        "Half an hour of lifting things and setting them back exactly where they were, in a room that will look identical when she finishes.",
    ],
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


# ── her mum, on the hours no chore covers — sheets/people/her_mum_cards.md ────
#
# ⚠️ WINDOWS COME OFF mum_rows_expanded(), NEVER OFF A SECOND TABLE. Same reason
# the chore cards read MUM_ROWS: an hour written down twice drifts, and the failure
# is silent — the card is simply not there in the room she is standing in.
#
# ⚠️ mum_sat_down IS priority 4 AND EVERYTHING ELSE OF HERS IS 5, and that is the
# whole of how the one real collision is handled. She is in the front room at 14:30
# on a Monday either way: on the dusting if it is not done, sat down if it is. Both
# canvases cover that window, and the portrait path keeps ONE canvas per NPC per
# location, highest priority among the SELECTABLE ones (v2.py:4928-4932). Dusting
# undone, mum_dusting is selectable and wins. Dusting done, its `chore_done_dusting
# is_false` fails and it is not a candidate at all, so mum_sat_down is. Correct both
# ways, and no condition is written twice.

SHOPPING = ("11:15", "12:00")     # the one hour of hers in the kitchen that is not a meal

EATING_AT = {
    "07:30": "She is eating standing up at the counter with one eye on the clock, next to @gil who is sat down with the paper. In half an hour she will be at the sink with both their plates.",
    "08:00": "She has come in off the ward and has not changed out of the uniform yet. She is eating at the table without tasting any of it, the way you eat when your day is already over.",
    "08:30": "Sunday, so she is sat down with whoever got up, and everything is on the table at once instead of going through one plate at a time.",
    "11:15": "The shopping is half on the floor and half on the counter and she is putting it away tins first, which is the order she has always done it in and has never explained.",
    "12:30": "She has sat down to eat and she has half an hour. It is the longest she sits down between getting up and the middle of the afternoon.",
    "15:15": "She is eating a late lunch on her own at the table, hours after everybody else did. The house is quiet, she has it to herself, and she does not look like somebody who wanted it.",
}

# (window, paragraphs). The four tile the whole day, so exactly one always renders —
# and ⚠️ adjacent [group] blocks MERGE into one if/elseif chain (v2.py:14971), which
# is the shape this wants: the bands are exclusive and only the live one prints.
SAT_BANDS = [
    (("00:00", "12:00"), [
        "She is sat down in the front room before nine, which she never is, because the thing she would have been stood at is already done.",
        "The TV is not on. She is in the chair with a cup, in the part of the morning that is usually the sink.",
    ]),
    (("12:00", "17:15"), [
        "She is in the chair in the middle of the afternoon with nothing in front of her. The room is done and she is not the one who did it.",
        "The cup is on the arm of the chair and the remote is next to it and she has not picked up either.",
        "She has the afternoon and no idea what to do with it, which is what an afternoon looks like when somebody hands you one.",
    ]),
    (("17:15", "18:00"), [
        "This is the hour her own week gives her, five until six, and it is the only one on it that is hers. She is sat down with the TV on low.",
        "Her one hour off, and she is in the chair for all of it. Tonight she is home, so there is nothing at the end of it to get ready for.",
    ]),
    (("18:00", "00:00"), [
        "She is sat down while the house is still going — the kettle through the wall, somebody on the stairs — and for once none of it is waiting on her.",
        "The evening is happening in the other rooms and she is in this one, in the chair, with her shoes off.",
    ]),
]

MUM_CARDS = {
    "eating": dict(
        cid="mum_eating", room=K, name="Your mum, eating",
        description=("Her six meals, each at its own hour — and the shopping, which is the one "
                     "hour of hers in this kitchen that is not one. Sit down with her or don't."),
        node="At the table"),
    "sat_down": dict(
        cid="mum_sat_down", room=F, name="Your mum, sat down",
        description=("Nineteen rows, and every one of them exists because the player took a chore "
                     "off her. Four bands by the hour. Priority 4 — see the note above."),
        node="In the chair", priority=4),
    "sunday": dict(
        cid="mum_sunday", room=F, name="Your mum, her Sunday afternoon",
        description=("Half one to six on a Sunday. Four and a half hours, the longest single "
                     "window in her week, and no class and five open shifts against it."),
        node="The one afternoon she gets", minutes=HOUR),
    "strip": dict(
        cid="mum_strip", room=S, name="Your mum, on the strip",
        description=("Nine to eleven, Monday Wednesday Friday. The only place in the game the "
                     "player meets her outside that house, and the cafe is on the same street."),
        node="In town", minutes=HOUR),
}

SUNDAY_POOL = [
    "Sunday afternoon, and she is in the chair with the TV on and four and a half hours in front of her. It is the only stretch in her week that is not before or after something else.",
    "She has the room, the chair and the afternoon, and she is using all three on a programme she is not really watching.",
    "Nobody in this house needs anything from her until six. She has sat down as though she does not entirely trust that.",
]

STRIP_POOL = [
    "Your mum is on the strip in the coat and shoes she only wears out of the house, going down the row with a list, at the speed of somebody working to a bus.",
    "She is outside the chemist with two bags already, checking the list against what is in them. She has two hours and the bus back is forty minutes of it.",
    "You see her before she sees you — your mum, in town, in her going-out coat, doing the week's shopping on the same street you work on.",
]


def card_of(loc, activity):
    """Which card covers a row of hers that no chore card does. None = not yet."""
    if "in the bath" in activity:
        # NOT A CARD — a LOCKED DOOR. the_house.md:20 and the bathroom's own
        # description both say the lock works, and canvas_opening already promises it:
        # "the bathroom is gone until whoever is in there comes out". See BATH_LOCK.
        return None
    if loc == M:
        # ⚠️ "in bed" IS TESTED FIRST. Her Sunday row reads "in bed, not asleep yet",
        # which contains the word asleep and was filed as sleeping until it was counted.
        if "in bed" in activity:
            return "in_bed"
        if "asleep" in activity:
            return "asleep"
        return "changing"
    if loc == S:
        return "strip"
    if loc == K:
        # Seven o'clock is the `dinner` canvas, which is the room's event and not
        # hers, and already requires her in the room.
        return None if "everybody in one room" in activity else "eating"
    if "one afternoon she gets" in activity:
        return "sunday"
    return "sat_down"


# ── the master bedroom, BASE ONLY — sheets/people/her_mum_cards.md, 2026-09-22 ──
#
# ⚠️ THE CLIMB IS NOT HERE AND THAT IS DELIBERATE. LO: "thats the climb. But we can
# build the base." Walking in on your mum asleep, changing, or in bed is a room you
# can already reach — no lock, no entry gate, the door on the landing at every one of
# these hours and the nav card printing her name. Until 2026-09-22 you walked in and
# got NOTHING. These three give the room a floor. What a rung on it looks like is
# block 5 and none of it is decided.

ASLEEP_POOL = [
    "She is asleep on her side with the curtains shut and the landing light off, and she does not move when the door goes. She sleeps like somebody who has learned to take it wherever it is.",
    "The room is dark and warm and she is under the covers with one arm out. Whatever woke you did not wake her.",
    "Asleep, and the alarm on her side is set for a time that is not morning. You have seen it go off from your own room.",
]

# the_two_doors.md: "Her mum's shift times are on the wall in that bedroom. She has
# read them a hundred times for ordinary reasons. Now they are a timetable for
# something else." The location description already puts them by the door.
WALL = [
    "Her shifts are on the wall by the door in her own handwriting, Mondays and Wednesdays and Fridays ringed, and the same four words under each one. You have read it a hundred times without reading it.",
    "The card by the door has her nights on it. It has been there since before you moved in and nobody has ever needed to change it.",
]

CHANGING_AT = {
    "06:45": "She is half into the clothes she does the house in, back to the door, and she does not stop when you come in. Neither of you says anything about it.",
    "07:45": "Sunday, so she is dressing slowly for once, and the door was not properly shut because on a Sunday nobody is going anywhere.",
    "08:30": "The coat and the shoes she only wears out of the house. She is doing the buttons in front of the mirror and checking the list in her other hand at the same time.",
    "09:00": "She is coming out of the uniform and into nightwear at nine in the morning with the light still on, which is what a night shift does to a day.",
    "11:00": "Back out of the coat and into home clothes, with the shopping still in the hall where she put it down.",
    "15:00": "Three in the afternoon and she is getting up, into home clothes, with the rest of the day to do in what is left of it.",
    "18:30": "She is getting into the ward uniform in front of the wardrobe, and the whole thing takes her four minutes because she has done it a thousand times.",
    "20:30": "Nightwear, the lamp already on, the door pushed to but not shut. She goes to bed while the house is still awake because she has to.",
    "21:30": "Sunday night. She is changing for bed with the TV still going downstairs, an hour before anybody else will think about it.",
}

IN_BED_POOL = [
    "She is in bed with the lamp on and the door not quite shut, not asleep yet, with the book she has been on for a month face down beside her.",
    "The lamp is on and she is propped up against the headboard with her eyes shut, which is not the same as asleep and she would tell you so.",
]

MUM_CARDS.update({
    "asleep": dict(
        cid="mum_asleep", room=M, name="Your mum, asleep",
        description=("Six rows. She is asleep and the room is reachable — it always was. The "
                     "base: the room, her in it, and the shifts on the wall by the door."),
        node="The room, dark"),
    "changing": dict(
        cid="mum_changing", room=M, name="Your mum, changing",
        description=("Nine rows and nine different moments — into house clothes, into the coat "
                     "she goes out in, into the ward uniform, into nightwear. Base only."),
        node="The wrong moment"),
    "in_bed": dict(
        cid="mum_in_bed", room=M, name="Your mum, in bed",
        description=("Two rows. The lamp is on and the door is not quite shut and she is not "
                     "asleep yet. The one hour in that room she can actually talk."),
        node="The lamp on"),
})


def card_windows():
    """{card: [(weekdays, start, end)]}, straight off her own rows."""
    out = {}
    for weekdays, start, end, loc, activity, chore in mum_rows_expanded():
        if chore:
            continue
        key = card_of(loc, activity)
        if key:
            out.setdefault(key, []).append((tuple(weekdays), start, end))
    return {k: sorted(set(v)) for k, v in out.items()}


def build_mum_cards():
    out = [
        "# --- HER MUM, ON HER OWN HOURS ----------------------------------------------\n"
        "# her_mum_cards.md, 2026-09-22. BASE.md rule 1: every row has a card. Twenty of\n"
        "# her sixty-seven rows had one. These four carry twenty-eight more — eating, sat\n"
        "# down once the player has done her chore for her, her Sunday afternoon, and her\n"
        "# two hours in town. They pay nothing: chores.md, \"what she gets is time with her\n"
        "# mum.\" The nineteen behind a shut door are her ladder and wait for block 5.\n"
        "#\n"
        "# Generated by games/the_balance/process/gen_week.py. Edit the tables there.\n\n"
    ]
    wins = card_windows()
    for key, spec in MUM_CARDS.items():
        room = spec["room"]
        parts = ["[[canvases]]", f'id   = "{spec["cid"]}"', f'name = "{spec["name"]}"',
                 f'description = "{spec["description"]}"', "",
                 "[canvases.trigger]", f'location      = "{room}"',
                 'npc           = "npc_lynn"',
                 "is_repeatable = true",
                 f'priority      = {spec.get("priority", 5)}', "is_active     = true",
                 conditions([c_lynn(room, "is_present")]).rstrip(), ""]
        for weekdays, start, end in wins[key]:
            parts += ["[[canvases.trigger.schedules]]",
                      "weekdays   = [" + ", ".join(str(d) for d in weekdays) + "]",
                      f'start_time = "{start}"', f'end_time   = "{end}"', ""]
        parts += ["[[canvases.nodes]]", 'id   = "base"', f'name = "{spec["node"]}"', ""]
        body = "\n".join(parts)

        if key in ("eating", "changing"):
            table = EATING_AT if key == "eating" else CHANGING_AT
            for start, _e in sorted({(s, e) for _w, s, e in wins[key]}):
                end = next(e for _w, s, e in wins[key] if s == start)
                body += group([c_window(start, end)], [table[start]])
        elif key == "sat_down":
            for (bs, be), paras in SAT_BANDS:
                body += group([c_window(bs, be)], paras)
        elif key == "asleep":
            body += pool(ASLEEP_POOL)
        elif key == "in_bed":
            body += pool(IN_BED_POOL)
        else:
            body += pool(SUNDAY_POOL if key == "sunday" else STRIP_POOL)

        body += '[canvases.nodes.exit_block]\ntype = "choices"\n\n'
        minutes = spec.get("minutes", HALF)
        if key == "eating":
            for start, end in sorted({(s, e) for _w, s, e in wins[key]}):
                w = [c_window(start, end)]
                if (start, end) == SHOPPING:
                    body += choice("Put it away with her.", room, HALF, w)
                else:
                    body += choice("Sit down and eat with her.", room, HALF, w)
                    body += choice("Take yours and go.", room, 5, w)
        elif key == "strip":
            body += choice("Walk round the shops with her.", room, minutes)
            body += choice("Say hello and let her get on.", room, 5)
        elif key == "asleep":
            # ⚠️ THE ONE SECOND NODE IN HER WHOLE SET, and it is here because the choice
            # would otherwise show nothing. the_two_doors.md: "Her mum's shift times are on
            # the wall in that bedroom. She has read them a hundred times for ordinary
            # reasons. Now they are a timetable for something else." A card that offers to
            # read the wall and then does not print it is a dead button.
            body += ("[[canvases.nodes.exit_block.choices]]\n"
                     'text       = "Read the shifts on the wall."\n'
                     'targetType = "node"\n'
                     f'nodeId     = "{spec["cid"]}.wall"\n'
                     "time_progression_minutes = 5\n\n")
            body += choice("Stand there a minute.", room, 5)
        elif key == "changing":
            body += choice("Say sorry and go.", room, 2)
            body += choice("Wait for her to finish.", room, HALF)
        elif key == "in_bed":
            body += choice("Say goodnight.", room, 5)
        else:
            body += choice("Sit down with her.", room, minutes)
        body += choice("Leave her to it.", room)
        if key == "asleep":
            body += ("[[canvases.nodes]]\n" 'id   = "wall"\n' 'name = "Her shifts"\n\n')
            body += pool(WALL)
            body += ('[canvases.nodes.exit_block]\n' 'type = "location"\n'
                     'text = "Go back out."\n\n'
                     "[canvases.nodes.exit_block.config]\n"
                     'destinationType          = "specific"\n'
                     f'locationId               = "{room}"\n'
                     "time_progression_minutes = 2\n\n")
        out.append(body)
    return "".join(out).rstrip() + "\n"


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
        parts += ["[[canvases.nodes]]", 'id   = "base"', 'name = "She is on it"', ""]
        body = "\n".join(parts) + pool(MUM_AT[key])
        body += '[canvases.nodes.exit_block]\ntype = "choices"\n\n'


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

    out.append("\n" + build_mum_cards())
    return "".join(out).rstrip() + "\n"



# ─────────────────────────────────────────────────────────────────────────────
# 5 · THE OTHER THREE — sheets/people/the_other_three.md, round 3 of BASE.md
# ─────────────────────────────────────────────────────────────────────────────
#
# Gil had three rows, Nate five, Tasha four, against her mum's sixty-seven. Five
# lines across four sheets put Gil in the garage and he had no garage row; the cast
# page puts Nate on campus and gave him no campus row; and all three of them
# vanished at midnight, so between midnight and half six there was nobody in that
# house but her mum.
#
# ⚠️ EVERY NIGHT THAT CROSSES MIDNIGHT IS TWO ROWS, split at midnight, and an end
# of "00:00" and never "23:59" — the weekday list is read against the day the clock
# is on, and an end time is exclusive. Both lessons come off her mum's week.

Q, U, NR, TR = "the_quad", "the_union", "nate_room", "tasha_room"
WD, WKND, ALL = [0, 1, 2, 3, 4], [5, 6], [0, 1, 2, 3, 4, 5, 6]
HOME, SAT, SUN_ = [1, 3, 5, 6], [5], [6]
DINNER_T = [1, 3, 6]     # Tasha at the table — not Saturday, she is out

GIL_ROWS = [
    (WD,   "00:00", "06:30", M, "asleep, with the door pushed to"),
    (WKND, "00:00", "07:30", M, "asleep — the one hour a week he gives himself"),
    (WD,   "06:30", "08:00", K, "at the table with the radio on and the paper folded to the part he wants"),
    (WKND, "07:30", "09:00", K, "at the table with the radio on, in no hurry about it"),
    (WKND, "09:00", "18:00", G, "out in the garage with the car, most of the day"),
    (ALL,  "18:00", "19:00", K, "back, still in what he went out in"),
    (HOME, "19:00", "20:00", K, "at the table, with everybody"),
    (HOME, "20:00", "20:45", G, "out at the car, or the look of being out at the car"),
    (HOME, "20:45", "22:00", M, "up with her mum, door pushed to"),
    (HOME, "22:00", "23:30", G, "back down, in the garage with the light on"),
    (WARD, "19:00", "23:30", G, "in the garage on his own, four and a half hours of it"),
    (ALL,  "23:30", "00:00", M, "in, and that is the house shut"),
]

NATE_ROWS = [
    (WD,    "00:00", "07:00", NR, "asleep, door shut for once"),
    (SAT,   "00:00", "11:00", NR, "asleep, and he will not be up before eleven"),
    (SUN_,  "02:00", "11:00", NR, "in late and asleep — Saturday is the one night he goes out"),
    (WD,    "07:00", "07:45", B,  "in the shower, taking his time about it"),
    (WD,    "07:45", "08:30", K,  "in and out, eating standing up"),
    (WD,    "12:00", "13:30", Q,  "on the wall by the doors with whoever is out there"),
    (WD,    "13:30", "15:30", U,  "at a table with people, in no hurry to be anywhere"),
    (WKND,  "11:00", "19:00", F,  "on the sofa, and he has been there since he got up"),
    (DINNER_T, "19:00", "20:00", K, "at the table, eating fast so he can get up"),
    (SAT,   "19:00", "20:00", K,  "at the table, already dressed to go out"),
    (DINNER_T, "20:00", "22:00", F, "on the sofa with the TV on"),
    (WARD,  "19:00", "22:00", F,  "on the sofa with the TV on"),
    ([0, 1, 2, 3, 4, 6], "22:00", "00:00", NR, "in his room with the door not quite shut"),
]

TASHA_ROWS = [
    (WD,       "00:00", "09:00", TR, "asleep, and she sleeps later than anyone in this house"),
    (WKND,     "02:00", "09:00", TR, "in at two and asleep, with her shoes where she stepped out of them"),
    (ALL,      "16:00", "17:00", TR, "home, lights on, door open"),
    (ALL,      "17:00", "18:00", B,  "doing her face with the door unlocked"),
    (DINNER_T, "18:00", "19:00", TR, "getting ready, whether or not she is going anywhere"),
    (DINNER_T, "19:00", "20:00", K,  "at the table with a story she is halfway through"),
    (DINNER_T, "20:00", "00:00", TR, "in, with music on"),
    ([0, 2],   "18:00", "00:00", TR, "in, with music on, and nobody to perform it at"),
]

THREE = [
    ("npc_gil", GIL_ROWS,
     "# ⚠️ HIS WEEK IS sheets/people/the_other_three.md, 2026-09-22. Three rows became\n"
     "# twelve. THE GARAGE IS THE POINT: five lines across four sheets put him out there\n"
     "# late and he had no garage row at all. He goes UP at quarter to nine on the nights\n"
     "# her mum is home, which is what the_two_doors.md needs, and comes BACK DOWN at ten,\n"
     "# which is what her_week.md and the_house_day.md need. Both pages were true and the\n"
     "# build served neither.\n"),
    ("npc_nate", NATE_ROWS,
     "# ⚠️ HIS WEEK IS sheets/people/the_other_three.md, 2026-09-22. Five rows became\n"
     "# thirteen. THE CAMPUS ROWS ARE THE POINT: the_cast.md:29 gives him a move that only\n"
     "# works on campus and he was never on it. Her class ends at twelve and he is on the\n"
     "# quad from twelve, so the ninety minutes she can stand there cost her the early bus.\n"),
    ("npc_tasha", TASHA_ROWS,
     "# ⚠️ HER WEEK IS sheets/people/the_other_three.md, 2026-09-22. Four rows became\n"
     "# eight. She is out until four and that stays NO ROW (BASE.md:97). What she gained is\n"
     "# a night: she used to end at 23:59 and vanish, and Friday and Saturday she is out\n"
     "# from six and back in her own bed at two.\n"),
]


def build_person(rows, head):
    out = [head + "#\n# Generated by games/the_balance/process/gen_week.py. Edit the table there.\n\n"]
    for weekdays, start, end, loc, activity in rows:
        out.append("\n".join([
            "[[npcs.schedules]]", f'location   = "{loc}"',
            "weekdays   = [" + ", ".join(str(d) for d in weekdays) + "]",
            f'start_time = "{start}"', f'end_time   = "{end}"',
            f'activity   = "{activity}"']) + "\n\n")
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
    # ⚠️ ONE SPLICE PER PERSON, EACH ENDING ON THE NEXT [[npcs]] HEADER. A
    # [[npcs.schedules]] table attaches to whichever [[npcs]] it follows, so a block
    # that overshoots its own person's end silently re-parents every row after it.
    "three": lambda: [splice(
        PEOPLE,
        [head.split("\n")[0], first],
        [f'[[npcs]]\nid          = "{nxt}"'],
        build_person(rows, head)) for (npc, rows, head), first, nxt in zip(
            THREE,
            ['[[npcs.schedules]]\nlocation   = "the_kitchen"\nweekdays   = [0, 1, 2, 3, 4]\nstart_time = "06:30"',
             '[[npcs.schedules]]\nlocation   = "the_bathroom"\nweekdays   = [0, 1, 2, 3, 4]\nstart_time = "07:00"',
             '[[npcs.schedules]]\nlocation   = "tasha_room"\nweekdays   = [0, 1, 2, 3, 4, 5, 6]\nstart_time = "16:00"'],
            ["npc_owen", "npc_tasha", "npc_lynn"])],
}

if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    for name in (JOBS if which == "all" else [which]):
        JOBS[name]()
        print(f"  {name}: spliced")
