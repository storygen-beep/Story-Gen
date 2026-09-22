#!/usr/bin/env python3
"""Ten routes through The Balance, one per slice, driven in a real browser.

Run from the repo root:

    venv/bin/python games/the_balance/process/walks.py [--headed] [route ...]

    venv/bin/python games/the_balance/process/walks.py opening friday

WHY THIS EXISTS, AND WHY IT IS HERE AND NOT IN THE SCRATCHPAD
-------------------------------------------------------------
Eight of these existed during slices 1-8 and lived in the session scratchpad. The
scratchpad was wiped and all eight went with it. `playtest.py` still answers the
universal questions — every canvas renders, every location resolves, no page errors
— but nothing walked a ROUTE: take a shift, get paid on Friday, go live, open a
door. A structural change can break any of those while every instrument reads green.

⚠️ `.claude/agents/v2-player.md:75-79` says probe scripts belong in the scratchpad
and never in `games/`. This file is a deliberate override of that rule, recorded as
O12 in process/README.md §4. The rule is right about throwaway probes; it is wrong
about a regression suite, because a check that dies with the session is not a check.

THE ONE RULE
------------
ASSERT ON STATE, NEVER ON A RENDERED LABEL. playtest.py:37-43 records four false
alarms and zero real findings from label assertions, which is why it ships no
`assert_text` helper. `body()` may answer WHICH variant rendered; only `sv()` may
answer WHETHER a mechanic fired. Canvases with an npc on the trigger render as the
person's name, canvases without render as the canvas name, and a random ambient can
take the screen on arrival — three false failures during the build came from exactly
that.
"""

import re
import sys
import pathlib

sys.path.insert(0, ".claude/skills/author-game-v2/scripts")

from playtest import (  # noqa: E402
    open_game, enter_game, sv, traits, flags, body, links, locked,
    click, play, goto, passage, set_time, advance_time, stand_at,
    apply_effect, snapshot, npcs_at, npc_at, Report,
)

BUILD = "games/the_balance/output/index.html"


# ── the one helper playtest.py does not carry ────────────────────────────────

def apply_flag(page, flag, op="set", target="player", npc_id=None):
    """Set a flag through the engine, so `flags_meta.set_day` gets written.

    POSITIONAL — `applyFlagEffect(targetType, npcId, flag, op)` (v2.py:6069).

    ⚠️ Never poke `State.variables.flags.x = true` instead. Only the engine's own
    path writes `flags_meta`, and `days_since_flag` fails CLOSED when `set_day` is
    missing (v2.py:3979). A flag set by hand makes every day-counting condition in
    the game read false, and the route then blames the game.
    """
    return page.evaluate(
        """(a) => { window.applyFlagEffect(a[0], a[1], a[2], a[3]);
                    return SugarCube.State.variables.flags[a[2]]; }""",
        [target, npc_id, flag, op])


def cash(page):
    return traits(page).get("cash")


def offered(page, loc, cid):
    """Would this room offer this canvas, standing here right now?

    ⚠️ NOT `play()`. play() jumps straight to the passage and proves only that the
    passage exists — it walks past the trigger schedule, the conditions and the
    `requires_npc` resolution, which are the whole of what a fence IS. This asks the
    engine the same question the room asks when it draws its card list.
    """
    return bool(page.evaluate(
        """(a) => {
            var L = SugarCube.setup.help_data.locationCanvases[a[0]] || [];
            for (var i = 0; i < L.length; i++) {
                if (L[i].id !== a[1]) continue;
                return !!SugarCube.setup.isCanvasSelectable(L[i]);
            }
            return false;
        }""", [loc, cid]))


def start(page, day="Monday", hour=12, where="her_room"):
    """Put her somewhere at a time, past the opening, ready to act."""
    apply_flag(page, "opening_done", "set")
    set_time(page, day, hour)
    stand_at(page, where)


def dice_off(page):
    """Pin Math.random high, so no roll in the engine ever lands.

    Every chance in v2 is `Math.random() < chance` — the random ambients' listing
    (v2.py:5291), their auto-fire on arrival (:5761) and substitutions (:5871) — and
    this build seeds no PRNG, so the page's own Math.random is the one they read.
    ⚠️ EVERY ROUTE SHARES ONE PAGE. Always pair it with dice_on, in a `finally`.
    """
    page.evaluate("() => { if (!window.__realRandom) window.__realRandom = Math.random;"
                  " Math.random = () => 0.999999; }")


def dice_on(page):
    page.evaluate("() => { if (window.__realRandom) { Math.random = window.__realRandom;"
                  " delete window.__realRandom; } }")


# ── the routes ───────────────────────────────────────────────────────────────

def walk_opening(page, rep):
    """Slice 1 — the three opening screens, the chore, and the job."""
    # ⚠️ The opening canvas is emitted with the StartingCanvas prefix (v2.py:700),
    # which play() cannot build — it hardcodes "Canvas_" (playtest.py:265).
    goto(page, "StartingCanvas_canvas_opening_Node_wake")
    rep.check("the opening canvas is reachable",
              "canvas_opening" in passage(page), passage(page))

    # ⚠️ THE CHORE PAYS NOTHING, 2026-09-23. LO removed the chore money and the
    # fridge list, so this probe is inverted: it used to assert the purse GREW on
    # this node and now asserts it does not move. The purse is read before entering
    # because the old payment landed on node ENTRY.
    before = cash(page)
    goto(page, "StartingCanvas_canvas_opening_Node_chore")
    rep.check("the opening chore pays nothing", cash(page) == before,
              f"cash {before} -> {cash(page)}")

    # has_job is set by a flagEffect on the LAST exit of the chain, not by landing
    # on the `hired` node. Walk it.
    play(page, "canvas_ask_owen")
    click(page, "Ask about the card in the window")
    click(page, "Take it")
    click(page, "Back out to the floor")
    rep.check("finishing the ask sets has_job", flags(page).get("has_job") is True,
              f"has_job = {flags(page).get('has_job')}")


def clock(page):
    """The clock as minutes past midnight, and the day name with it."""
    ts = sv(page)["game_state"]["time_state"]
    return ts["current_day"], ts["current_hour"] * 60 + ts["current_minute"]


def walk_week(page, rep):
    """sheets/systems/her_week.md — five shifts a day, and which of them a class day can reach.

    ⚠️ REPLACED walk_shift ON 2026-09-20. The old route asserted with play(), which
    jumps to the passage and walks straight past the trigger schedule — it started
    at 18:00 and passed against a roster that ran 12:00-17:00. The roster was never
    under test. Everything here asks `offered()` instead.

    ⚠️ DICE OFF FOR THE WHOLE ROUTE. `picked_quad` and `picked_stop` auto-fire on
    arrival and REPLACE the location screen, so an undiced run clicks "The bus home"
    into a canvas that does not have it and the clock silently never moves. Caught
    live on 2026-09-20; the same trap walk_travel already carries.
    """
    dice_off(page)
    try:
        _week(page, rep)
    finally:
        dice_on(page)


def _week(page, rep):
    apply_flag(page, "has_job", "set")

    # ── the five clock-on windows, every day of the week
    for day in ("Monday", "Saturday"):
        for hour in (7, 10, 13, 16, 19):
            start(page, day, hour, "the_cafe")
            rep.check(f"{day[:3]} {hour:02d}:00 is a shift",
                      offered(page, "the_cafe", "shift_floor") is True)

    start(page, "Monday", 7, "the_cafe")
    set_time(page, "Monday", 7, 19)
    rep.check("07:19 still clocks on", offered(page, "the_cafe", "shift_floor") is True)
    set_time(page, "Monday", 7, 20)
    rep.check("07:20 does not — the window is end-exclusive",
              offered(page, "the_cafe", "shift_floor") is False)
    set_time(page, "Monday", 14, 30)
    rep.check("he does not take her at half two",
              offered(page, "the_cafe", "shift_floor") is False)

    # ── three hours, three dollars, one a day
    start(page, "Monday", 16, "the_cafe")
    before, (_, t0) = cash(page), clock(page)
    rep.check("the floor shift opens", play(page, "shift_floor") is True)
    click(page, "Clock off")
    _, t1 = clock(page)
    rep.check("a shift pays three dollars", cash(page) - before == 3,
              f"cash {before} -> {cash(page)}")
    rep.check("a shift is three hours", t1 - t0 == 180, f"{t0} -> {t1} minutes")
    set_time(page, "Monday", 19, 0)
    rep.check("and it is one a day", offered(page, "the_cafe", "shift_floor") is False)

    # ── the class day. her_week.md: "On a class day the 16-19 shift is the only one
    # that fits." Walked at the EARLIEST possible arrival — stand_at skips the bus
    # stop's five-minute entry cost and every three-minute nav hop, so real play is
    # later than this and the case only gets stronger.
    start(page, "Tuesday", 10, "the_classroom")
    set_time(page, "Tuesday", 10, 30)
    play(page, "class_4")
    click(page, "Sit through it")
    _, out = clock(page)
    rep.check("the ten thirty class puts her out at twelve", out == 12 * 60,
              f"{out // 60:02d}:{out % 60:02d}")

    # ⚠️ stand_at only writes current_location (playtest.py:330) — the passage has to
    # be rendered too, or click() finds no links and the clock never moves.
    stand_at(page, "the_quad")
    goto(page, "Location_the_quad")
    click(page, "The bus home")       # opens bus_back_quad — the fare is the CHOICE
    click(page, "Home. $2")
    stand_at(page, "the_bus_stop")
    goto(page, "Location_the_bus_stop")
    click(page, "Get the bus")
    click(page, "Into town")
    _, arrive = clock(page)
    rep.check("campus to the cafe is eighty minutes at best",
              arrive >= 13 * 60 + 20, f"{arrive // 60:02d}:{arrive % 60:02d}")
    stand_at(page, "the_cafe")
    rep.check("so the one o'clock is gone",
              offered(page, "the_cafe", "shift_floor") is False)
    set_time(page, "Tuesday", 16, 0)
    rep.check("and the four o'clock is the one that fits",
              offered(page, "the_cafe", "shift_floor") is True)

    # ── the late one puts her on the street after his rule. 19:00 + 180 = 22:00,
    # plus the walk home; `in_after_ten` watches the street from 22:15.
    rep.check("the last shift ends at ten", 19 * 60 + 180 == 22 * 60)


def walk_alarm(page, rep):
    """sheets/systems/her_week.md — she sets the alarm, and rest is the hours she slept."""
    # ⚠️ REST IS READ AFTER THE MIDNIGHT DECAY, which is the whole point. The choice
    # sets rest BEFORE advanceTime (v2.py:13923), so a sleep that crosses midnight is
    # decayed by [player.trait_decay] straight afterwards and the pre-midnight bands
    # set twenty over. What the player sees is what her_week.md's table says.
    start(page, "Thursday", 22, "her_room")
    set_time(page, "Thursday", 22, 30)
    play(page, "sleep")
    offers = links(page)
    rep.check("in at half ten, four alarms and no alarm",
              len([x for x in offers if "Set it for" in x]) == 4, str(offers))
    # "twelve and a half hours" exists only in the eight o'clock band, so its absence
    # is proof the bands do not leak into each other.
    rep.check("and no other band's is on the screen",
              not any("twelve and a half" in x for x in offers), str(offers))

    click(page, "Set it for seven")
    day, now = clock(page)
    rep.check("seven is seven", now == 7 * 60, f"{now // 60:02d}:{now % 60:02d}")
    rep.check("and the day rolled", day == "Friday", day)
    rep.check("eight and a half hours is a hundred",
              traits(page).get("rest") == 100, f"rest = {traits(page).get('rest')}")

    # Half eleven to six is six and a half hours: 81 on the page's table.
    start(page, "Thursday", 23, "her_room")
    set_time(page, "Thursday", 23, 30)
    apply_effect(page, "rest", "set", 40, clamp=False)
    play(page, "sleep")
    click(page, "Set it for six")
    _, now = clock(page)
    rep.check("six is six", now == 6 * 60, f"{now // 60:02d}:{now % 60:02d}")
    rep.check("six and a half hours is eighty-one",
              traits(page).get("rest") == 81, f"rest = {traits(page).get('rest')}")

    # After midnight the decay has already fired, so the band sets the plain number —
    # and the sleep does not cross midnight, so the day is not spent by rolling over.
    # That is the one case where "one a day" is observable.
    start(page, "Friday", 1, "her_room")
    set_time(page, "Friday", 1, 30)
    play(page, "sleep")
    click(page, "Set it for six")
    day, now = clock(page)
    rep.check("bed at half one, up at six, same day", day == "Friday", day)
    rep.check("four and a half hours is fifty-six",
              traits(page).get("rest") == 56, f"rest = {traits(page).get('rest')}")

    # ⚠️ THE CAP IS PER CALENDAR DAY, NOT PER NIGHT. Sleeping at half one spends
    # Friday's, so Friday evening has none left and she has to wait out the midnight.
    # her_week.md: staying up is allowed and it costs.
    set_time(page, "Friday", 22, 0)
    goto(page, "Location_her_room")
    rep.check("bed at half one spends that whole day's sleep",
              not any(x.strip() == "Sleep" for x in links(page)), str(links(page))[:120])

    # Nothing under four hours is on the screen at all.
    start(page, "Friday", 3, "her_room")
    set_time(page, "Friday", 3, 30)
    play(page, "sleep")
    offers = links(page)
    rep.check("at half three only the two that clear four hours are offered",
              len([x for x in offers if "Set it for" in x]) == 2, str(offers))


def walk_cafe_climb(page, rep):
    """PARKED 2026-09-19 — slice 2 as it stood with the cafe climb in the build."""
    start(page, "Tuesday", 18, "the_cafe")
    before, worked = cash(page), traits(page).get("shifts_worked") or 0
    rep.check("the floor shift opens", play(page, "shift_floor") is True)
    click(page, "Clock off")
    rep.check("the shift pays", cash(page) > before, f"cash {before} -> {cash(page)}")
    rep.check("the shift is counted",
              (traits(page).get("shifts_worked") or 0) > worked,
              f"shifts_worked {worked} -> {traits(page).get('shifts_worked')}")
    rep.check("the counter is its own surface", play(page, "shift_counter") is True)


# key, canvas, room, the label, a day and hour inside its window, and one outside
#
# ⚠️ EVERY TIME HERE IS ONE HER MUM IS NOT IN THAT ROOM, and that is not fussiness.
# The solo chore choices are gated on `npc_lynn is_absent` — chores.md: "When her
# mum isn't on a chore, she can do it on her own" — so once her week went in, three
# of these probes started reading an empty screen and blaming the chore. Monday
# lunchtime belongs to her: she is in that kitchen 11:15 to 13:30.
CHORE_ROWS = [
    ("breakfast",        "chores_kitchen",     "the_kitchen",    "Cook breakfast",          "Monday",  (8, 45),  (10, 30)),
    ("breakfast_dishes", "chores_kitchen",     "the_kitchen",    "Do the breakfast dishes", "Monday",  (9, 30),  (11, 0)),
    ("lunch",            "chores_kitchen",     "the_kitchen",    "Cook lunch",              "Tuesday", (12, 0),  (15, 0)),
    ("lunch_dishes",     "chores_kitchen",     "the_kitchen",    "Do the lunch dishes",     "Tuesday", (14, 0),  (16, 0)),
    ("dinner",           "chores_kitchen",     "the_kitchen",    "Cook dinner",             "Monday",  (18, 0),  (21, 0)),
    ("dinner_dishes",    "chores_kitchen",     "the_kitchen",    "Do the dinner dishes",    "Monday",  (20, 30), (23, 0)),
    ("laundry",          "chores_bathroom",    "the_bathroom",   "Put the laundry on",      "Monday",  (10, 0),  (23, 0)),
    ("dusting",          "chores_front_room",  "the_front_room", "Do the dusting",          "Monday",  (10, 0),  (23, 0)),
    ("bins",             "chores_garage",      "the_garage",     "Take the bins out",       "Monday",  (7, 0),   (11, 0)),
]


def clear_chores(page):
    for key, *_ in CHORE_ROWS:
        apply_flag(page, f"chore_done_{key}", "unset")


def walk_chores(page, rep):
    """sheets/systems/chores.md — nine chores, each in its room at its hour.

    ⚠️ offered() CANNOT TEST THESE. The room canvases carry no trigger schedule on
    purpose, so the room always offers the card; the hour lives on each CHOICE. The
    thing under test is therefore what is in links() once the card is open.
    """
    dice_off(page)
    try:
        _chores(page, rep)
    finally:
        dice_on(page)


def _chores(page, rep):
    # ── each one is on the screen in its window and gone outside it
    for key, cid, room, label, day, inside, outside in CHORE_ROWS:
        clear_chores(page)
        start(page, day, inside[0], room)
        set_time(page, day, *inside)
        play(page, cid)
        rep.check(f"{key} is on the screen {day[:3]} {inside[0]:02d}:{inside[1]:02d}",
                  any(label in x for x in links(page)), str(links(page))[:150])

        set_time(page, day, *outside)
        play(page, cid)
        rep.check(f"{key} is gone by {outside[0]:02d}:{outside[1]:02d}",
                  not any(label in x for x in links(page)), str(links(page))[:150])

    # ── and when her mum IS on it, the chore is hers to help with, not to do alone
    clear_chores(page)
    start(page, "Monday", 7, "the_kitchen")
    set_time(page, "Monday", 7, 10)
    play(page, "chores_kitchen")
    rep.check("her mum on the breakfast takes it off the solo list",
              not any("Cook breakfast" in x for x in links(page)), str(links(page))[:150])
    rep.check("and puts it on her own card instead",
              offered(page, "the_kitchen", "mum_breakfast") is True)

    # ── no chore pays anything, and every one of them costs half an hour
    # ⚠️ INVERTED 2026-09-23. LO removed the chore money and the fridge list, so the
    # three probes that asserted a payment now assert the purse does not move.
    clear_chores(page)
    start(page, "Monday", 8, "the_kitchen")
    set_time(page, "Monday", 8, 30)
    before, (_, t0) = cash(page), clock(page)
    play(page, "chores_kitchen")
    click(page, "Cook breakfast")
    _, t1 = clock(page)
    rep.check("the first chore of the day pays nothing", cash(page) == before,
              f"cash {before} -> {cash(page)}")
    rep.check("and it costs half an hour", t1 - t0 == 30, f"{t0} -> {t1}")
    rep.check("and it is done for the day",
              flags(page).get("chore_done_breakfast") is True,
              f"chore_done_breakfast = {flags(page).get('chore_done_breakfast')}")

    play(page, "chores_kitchen")
    rep.check("done means gone from the room",
              not any("Cook breakfast" in x for x in links(page)), str(links(page))[:150])

    before = cash(page)
    rep.check("the next one is still there",
              any("Do the breakfast dishes" in x for x in links(page)), str(links(page))[:150])
    click(page, "Do the breakfast dishes")
    rep.check("and neither does the second one", cash(page) == before,
              f"cash {before} -> {cash(page)}")

    # ── a missed Friday no longer reaches the chores at all. It used to make every
    # one of them take an hour instead of half; that went with the money.
    clear_chores(page)
    start(page, "Monday", 8, "the_kitchen")
    set_time(page, "Monday", 8, 30)
    apply_effect(page, "fridays_missed", "set", 1, clamp=False)
    _, t0 = clock(page)
    play(page, "chores_kitchen")
    click(page, "Cook breakfast")
    _, t1 = clock(page)
    rep.check("a missed Friday does not lengthen a chore any more",
              t1 - t0 == 30, f"{t0} -> {t1}")
    apply_effect(page, "fridays_missed", "set", 0, clamp=False)

    # ── overnight, everything opens again
    clear_chores(page)
    start(page, "Monday", 8, "the_kitchen")
    set_time(page, "Monday", 8, 30)
    play(page, "chores_kitchen")
    click(page, "Cook breakfast")
    rep.check("the flag is set before midnight",
              flags(page).get("chore_done_breakfast") is True)
    advance_time(page, 20 * 60)
    rep.check("and it resets overnight",
              flags(page).get("chore_done_breakfast") is not True,
              f"done={flags(page).get('chore_done_breakfast')}")

    # ⚠️ THE HELP / TAKE-OVER PAIR IS NOT CHECKED HERE. Both are gated on her mum
    # standing in the room, and until her week is built she is only ever in the
    # kitchen 19:00-20:00, which no chore window covers. walk_mum picks them up.


def walk_mum(page, rep):
    """sheets/people/her_mum.md — three kinds of day, and the chores she is on."""
    dice_off(page)
    try:
        _mum(page, rep)
    finally:
        dice_on(page)


# day, hour, minute, where she should be (None = out of the house)
MUM_HOURS = [
    ("Monday",    7, 10, "the_kitchen"),        # doing breakfast before a ward night
    ("Monday",    9, 30, "the_strip"),          # out shopping — new, and reachable
    ("Monday",   16,  0, "the_master_bedroom"), # asleep, getting ahead of the night
    ("Monday",   20,  0, None),                 # on the ward
    ("Tuesday",   3,  0, None),                 # still on it
    ("Tuesday",  11,  0, "the_master_bedroom"), # asleep the morning off it
    ("Tuesday",  19, 30, "the_kitchen"),        # dinner, everybody in one room
    ("Sunday",   14,  0, "the_front_room"),     # the one afternoon she gets
    ("Sunday",    6,  0, "the_master_bedroom"), # Saturday night runs to quarter to eight
]


def _mum(page, rep):
    start(page, "Monday", 12, "her_room")

    for day, hour, minute, where in MUM_HOURS:
        set_time(page, day, hour, minute)
        rep.check(f"{day[:3]} {hour:02d}:{minute:02d} — "
                  + (where or "out of the house"),
                  npc_at(page, "npc_lynn") == where, str(npc_at(page, "npc_lynn")))

    # ── the night that crosses midnight is two rows, and both of them hold
    set_time(page, "Tuesday", 23, 50)
    rep.check("ten to midnight on a Tuesday she is in bed",
              npc_at(page, "npc_lynn") == "the_master_bedroom", str(npc_at(page, "npc_lynn")))
    set_time(page, "Wednesday", 0, 10)
    rep.check("and ten past, on the Wednesday, she still is",
              npc_at(page, "npc_lynn") == "the_master_bedroom", str(npc_at(page, "npc_lynn")))
    set_time(page, "Tuesday", 0, 10)
    rep.check("but ten past midnight on the TUESDAY she is on the ward — the weekday "
              "list is what a single wrapped row gets wrong",
              npc_at(page, "npc_lynn") is None, str(npc_at(page, "npc_lynn")))

    # ── her hour on a chore drops when the chore is already done
    apply_flag(page, "chore_done_laundry", "unset")
    set_time(page, "Monday", 13, 45)
    rep.check("half one on a Monday she is on the bathroom floor with the washing",
              npc_at(page, "npc_lynn") == "the_bathroom", str(npc_at(page, "npc_lynn")))
    apply_flag(page, "chore_done_laundry", "set")
    rep.check("do it yourself and she is sat down in the front room instead",
              npc_at(page, "npc_lynn") == "the_front_room", str(npc_at(page, "npc_lynn")))

    # ── and the offer to help is fenced to HER hours, not the chore's window
    # ⚠️ THIS IS THE CHECK THE FIRST BUILD OF THE CHORES FAILED. The help / take-over
    # pair started life on the room canvas behind `npc_lynn is_present` plus the
    # laundry's own 08:00-22:00 window, which offered to take the washing off her
    # while she was in the bath at six.
    apply_flag(page, "chore_done_laundry", "unset")
    set_time(page, "Monday", 13, 45)
    stand_at(page, "the_bathroom")
    rep.check("at her laundry hour the offer is there",
              offered(page, "the_bathroom", "mum_laundry") is True)
    set_time(page, "Monday", 18, 10)
    rep.check("in the bath, she is in the same room and the offer is NOT",
              npc_at(page, "npc_lynn") == "the_bathroom"
              and offered(page, "the_bathroom", "mum_laundry") is False,
              f"at {npc_at(page, 'npc_lynn')}, "
              f"offered={offered(page, 'the_bathroom', 'mum_laundry')}")

    # ── taking it over closes the chore and moves her, and pays nothing
    set_time(page, "Monday", 13, 45)
    before = cash(page)
    play(page, "mum_laundry")
    rep.check("help her, take it over, or leave her to it",
              len([x for x in links(page) if "Leave her" not in x]) == 2, str(links(page))[:160])
    click(page, "Tell her you'll do it")
    rep.check("taking it over pays nothing", cash(page) == before,
              f"cash {before} -> {cash(page)}")
    rep.check("and closes the chore", flags(page).get("chore_done_laundry") is True)
    rep.check("and moves her out of it",
              npc_at(page, "npc_lynn") == "the_front_room", str(npc_at(page, "npc_lynn")))

    # ── helping does not pay either. Nothing does.
    apply_flag(page, "chore_done_dusting", "unset")
    set_time(page, "Monday", 14, 40)
    stand_at(page, "the_front_room")
    before = cash(page)
    play(page, "mum_dusting")
    click(page, "Do it with her")
    rep.check("doing it with her pays nothing", cash(page) == before,
              f"cash {before} -> {cash(page)}")
    rep.check("but it is still done", flags(page).get("chore_done_dusting") is True)

    # ── the bathroom lock. canvas_opening promises it on the first screen of the game —
    # "the bathroom is gone until whoever is in there comes out" — and for eight slices
    # the player could walk in on her in the bath and be offered "Get in the shower".
    # ⚠️ THE LAUNDRY HOURS MUST STAY OPEN. mum_laundry is a card inside that room, so a
    # plain `npc_lynn is_absent` gate would have killed it. Both halves are checked.
    for day, hour, minute, shut, why in (
            ("Tuesday",  8, 45, True,  "she is in the bath off the ward"),
            ("Monday",  18, 15, True,  "her half hour"),
            ("Sunday",  20, 45, True,  "Sunday night"),
            ("Monday",  13, 45, False, "her LAUNDRY hour — mum_laundry lives in there"),
            ("Sunday",  10,  0, False, "the big wash"),
            ("Monday",   8, 45, False, "a bath hour on the clock, but she is out on the strip")):
        set_time(page, day, hour, minute)
        stand_at(page, "the_hall")
        locked = not page.evaluate("() => SugarCube.setup.navDestUnlocked('the_bathroom')")
        rep.check(f"{day[:3]} {hour:02d}:{minute:02d} — the bathroom is "
                  + ("SHUT" if shut else "open") + f" ({why})",
                  locked is shut, f"locked={locked}")

    # ── the master bedroom is reachable at every hour and now has a floor
    clear_chores(page)
    for day, hour, minute, cid in (("Tuesday", 12,  0, "mum_asleep"),
                                   ("Monday",  18, 35, "mum_changing"),
                                   ("Tuesday", 20, 50, "mum_in_bed")):
        set_time(page, day, hour, minute)
        stand_at(page, "the_master_bedroom")
        html = page.evaluate("() => SugarCube.setup.renderNpcPortraits('the_master_bedroom') || ''")
        # ⚠️ `in`, NOT `==`, SINCE 2026-09-23. The picks are PER NPC (v2.py:4943), and
        # @gil now has three cards of his own in this room — so at 20:50 on a Tuesday
        # this wall draws TWO portraits, hers and his, and a re.search for the first
        # one was asserting which of two correct answers came back first.
        got = re.findall(r'data-passage="Canvas_([a-z_]+)_Node', html)
        rep.check(f"{day[:3]} {hour:02d}:{minute:02d} — her room draws {cid}",
                  cid in got, str(got))

    # the wall is the only second node in her whole set, and it has to print something
    play(page, "mum_asleep")
    set_time(page, "Tuesday", 12, 0)
    click(page, "Read the shifts on the wall")
    rep.check("reading the wall prints her shifts", "shift" in body(page).lower()
              or "nights" in body(page).lower(), body(page)[:120])

    # ── and every one of her hours is HER, not a line of text
    # ⚠️ THE SECOND THING THIS BUILD SHIPPED WRONG. All eight of her canvases went in
    # without `npc` on the trigger, so v2.py:4953 dropped them out of the portrait
    # path and v2.py:5595 printed the canvas NAME as a solo link — the player read
    # "Your mum, on the breakfast dishes" in a room she was standing in, and Lynn was
    # the only named person in the game whose face never appeared anywhere. The
    # docstring at the top of this file already said which way round it works.
    # Asserts on the rendered BUCKET, not on a label: which of the two renderers
    # claims the canvas is the whole question, so it is the thing to read.
    apply_flag(page, "chore_done_breakfast", "unset")
    set_time(page, "Monday", 7, 10)
    stand_at(page, "the_kitchen")
    drawn = page.evaluate("""(loc) => {
        var s = SugarCube.setup;
        return { portraits: s.renderNpcPortraits(loc) || '',
                 solo: s.renderSoloActivities(loc) || '' };
    }""", "the_kitchen")
    rep.check("her chore hour draws her portrait, with her name on it",
              "npc-portrait-card" in drawn["portraits"] and "Lynn" in drawn["portraits"],
              drawn["portraits"][:120] or "(nothing drawn)")
    rep.check("and it is not a solo link reading the canvas name",
              "Your mum" not in drawn["solo"], drawn["solo"][:120] or "(no solo links)")

    # ── her ordinary hours have cards too, and the front room is the hard one
    # her_mum_cards.md, 2026-09-22. Twenty of her sixty-seven rows had a card; these
    # four carry twenty-eight more.
    for day, hour, minute, loc, cid in (
            ("Tuesday",  8,  5, "the_kitchen",    "mum_eating"),
            ("Tuesday", 17, 20, "the_front_room", "mum_sat_down"),
            ("Sunday",  13, 35, "the_front_room", "mum_sunday"),
            ("Monday",   9,  5, "the_strip",      "mum_strip")):
        clear_chores(page)
        set_time(page, day, hour, minute)
        stand_at(page, loc)
        rep.check(f"{cid} is offered at {day[:3]} {hour:02d}:{minute:02d}",
                  offered(page, loc, cid) is True, f"lynn at {npc_at(page, 'npc_lynn')}")

    # ⚠️ THE ONE COLLISION, AND IT IS SILENT WHEN IT BREAKS. She is in the front room
    # at half two on a Monday either way — on the dusting if it is not done, sat down
    # if it is — and both canvases cover that window. The portrait path keeps ONE
    # canvas per NPC per location and takes the highest priority among the SELECTABLE
    # ones (v2.py:4928), so mum_dusting is 5 and mum_sat_down is 4. Equal priorities
    # would drop one of them with no error anywhere.
    for done in (False, True):
        apply_flag(page, "chore_done_dusting", "set" if done else "unset")
        set_time(page, "Monday", 14, 35)
        stand_at(page, "the_front_room")
        want = "mum_sat_down" if done else "mum_dusting"
        html = page.evaluate("() => SugarCube.setup.renderNpcPortraits('the_front_room') || ''")
        got = re.search(r'data-passage="Canvas_([a-z_]+)_Node', html)
        got = got.group(1) if got else None
        rep.check(f"dusting {'done' if done else 'not done'}, the front room draws {want}",
                  got == want, str(got))


def walk_friday(page, rep):
    """Slice 3 — sleep rolls the day, and Friday charges the hundred and fifty."""
    start(page, "Thursday", 23, "her_room")
    before_day = sv(page)["game_state"]["time_state"]["current_day"]
    play(page, "sleep")
    click(page, "Sleep")
    after_day = sv(page)["game_state"]["time_state"]["current_day"]
    rep.check("sleep rolls the day", after_day != before_day,
              f"{before_day} -> {after_day}")

    start(page, "Friday", 18, "the_kitchen")
    # ⚠️ clamp=False. applyTraitEffect clamps to 100 by default, so `set 200` lands
    # on 100, the 150 choice is then unaffordable, and a correct charge reads wrong.
    # Verified the game itself does NOT clamp: 90 -> 200 -> 255 -> 310 over real shifts.
    apply_effect(page, "cash", "set", 200, clamp=False)
    play(page, "friday_payment")
    click(page, "Count it out on the table")
    click(page, "Go up")
    rep.check("paying Friday costs exactly 150", cash(page) == 50,
              f"cash 200 -> {cash(page)}")


def walk_stream(page, rep):
    """Slice 4 — clean is spendable and repairable, and going live pays."""
    start(page, "Tuesday", 13, "the_bathroom")
    apply_effect(page, "clean", "set", 20, clamp=False)
    play(page, "wash")
    click(page, "Dry off")
    rep.check("the shower repairs clean", (traits(page).get("clean") or 0) > 20,
              f"clean 20 -> {traits(page).get('clean')}")

    # ⚠️ PARKED 2026-09-19 (the climbs): the rungs, the followers they moved and the
    # landing week are out, so the session is the one a fresh save gets — sit and talk,
    # and the first pay band. The old walk is walk_stream_climb under PARKED_ROUTES.
    start(page, "Tuesday", 13, "her_room")
    apply_effect(page, "clean", "set", 90, clamp=False)
    apply_flag(page, "streamed_today", "unset")
    before = cash(page)
    play(page, "stream")
    rep.check("the stream opens when nothing blocks it",
              "stream" in passage(page), passage(page))
    click(page, "Set the phone up")
    click(page, "Sit and talk to them")
    click(page, "Count it")
    rep.check("going live pays", cash(page) > before, f"cash {before} -> {cash(page)}")
    rep.check("going live sets the day flag",
              flags(page).get("streamed_today") is True,
              f"streamed_today = {flags(page).get('streamed_today')}")

    start(page, "Tuesday", 13, "her_room")
    apply_effect(page, "clean", "set", 10, clamp=False)
    play(page, "stream")
    rep.check("too dirty to go live shuts the door",
              not any("phone up" in x for x in links(page)), body(page).strip()[:70])


def walk_stream_climb(page, rep):
    """PARKED 2026-09-19 — slice 4 as it stood with the stream's rungs in the build."""
    start(page, "Tuesday", 13, "the_bathroom")
    apply_effect(page, "clean", "set", 20, clamp=False)
    play(page, "wash")
    click(page, "Dry off")
    rep.check("the shower repairs clean", (traits(page).get("clean") or 0) > 20,
              f"clean 20 -> {traits(page).get('clean')}")

    start(page, "Tuesday", 13, "her_room")
    apply_effect(page, "clean", "set", 90, clamp=False)
    apply_effect(page, "nate_landing", "set", 0, clamp=False)
    followers = traits(page).get("followers")
    play(page, "stream")
    rep.check("the stream opens when nothing blocks it",
              "stream" in passage(page), passage(page))
    # Walk the rungs. Jumping straight to `payout` skips the rung flags the payout
    # reads, and the probe then reports a working surface as dead.
    click(page, "Set the phone up")
    click(page, "Take your top off")
    click(page, "Wind it up")
    click(page, "Count it")
    rep.check("going live moves followers",
              (traits(page).get("followers") or 0) != followers,
              f"followers {followers} -> {traits(page).get('followers')}")
    rep.check("going live sets the day flag",
              flags(page).get("streamed_today") is True,
              f"streamed_today = {flags(page).get('streamed_today')}")

    # The block must state the REAL reason, and there are TWO mechanisms. Assert on
    # state; the reason text is reported as DETAIL, never as the pass condition.
    #
    #  · too dirty  -> the engine's own requirement gate, before the canvas renders
    #  · him on the landing -> the canvas renders and the choice is shown-locked
    start(page, "Tuesday", 13, "her_room")
    apply_effect(page, "clean", "set", 10, clamp=False)
    apply_effect(page, "nate_landing", "set", 0, clamp=False)
    play(page, "stream")
    rep.check("too dirty to go live shuts the door",
              not any("phone up" in x for x in links(page)), body(page).strip()[:70])

    start(page, "Tuesday", 13, "her_room")
    apply_effect(page, "clean", "set", 90, clamp=False)
    apply_effect(page, "nate_landing", "set", 5, clamp=False)
    play(page, "stream")
    rep.check("him on the landing shows the door and keeps it shut",
              bool(locked(page)), " | ".join(locked(page))[:70])


def walk_doors(page, rep):
    """Slice 5 — his door costs a week of the stream; hers is spent on Friday."""
    start(page, "Wednesday", 23, "nate_room")
    landing = traits(page).get("nate_landing") or 0
    # ⚠️ EVERY ROUTE IN THIS FILE SHARES ONE PAGE AND ONE SAVE. `nate_seen` may
    # already be set by a route that ran earlier, and since the ambients pass the
    # week is charged on the FIRST walk-in only — so without this reset the route
    # takes the cheap repeat path and reports a working price as broken.
    apply_flag(page, "nate_seen", "unset")
    apply_effect(page, "nate_landing", "set", 0, clamp=False)
    landing = 0
    rep.check("his door opens after ten", play(page, "nate_door") is True, passage(page))
    # The cost is charged on the exit of the FOLLOWING node, not on the choice.
    click(page, "Get off the landing")
    click(page, "Your room")
    rep.check("his door costs the stream a week",
              (traits(page).get("nate_landing") or 0) > landing,
              f"nate_landing {landing} -> {traits(page).get('nate_landing')}")
    rep.check("and it is remembered", flags(page).get("nate_seen") is True,
              f"nate_seen = {flags(page).get('nate_seen')}")

    start(page, "Monday", 23, "the_master_bedroom")
    rep.check("the master bedroom opens", play(page, "master_bedroom") is True)


def walk_class(page, rep):
    """Slice 6 — attendance is a falling meter repaired by turning up."""
    start(page, "Monday", 10, "the_lecture_hall")
    apply_effect(page, "attend_1", "set", 60, clamp=False)
    apply_effect(page, "rest", "set", 100, clamp=False)
    play(page, "class_1")
    click(page, "Sit through it")
    rep.check("attending repairs that subject",
              (traits(page).get("attend_1") or 0) > 60,
              f"attend_1 60 -> {traits(page).get('attend_1')}")
    rep.check("the four subjects are four surfaces",
              all(play(page, f"class_{n}") is not None for n in (1, 2, 3, 4)))


def walk_crowd(page, rep):
    """Slice 7 — the picking-on fires, and nobody talks about a dare.

    ⚠️ PARKED 2026-09-19 (the climbs): the dares are out of the build, so the half of
    this route that did them is walk_dares under PARKED_ROUTES. What is left guards the
    other direction: no line about a dare leaks back into the crowd while there are none.
    """
    start(page, "Monday", 12, "the_quad")
    rep.check("the picking-on can fire", play(page, "picked_quad") is True)
    crowd_talk = set()
    for _ in range(16):
        play(page, "bree_takes_it_home")
        crowd_talk.add(body(page))
        play(page, "paige_is_nice")
        crowd_talk.add(body(page))
    rep.check("nobody refers to a dare",
              not any("knows, by the way" in b or "about the dare" in b for b in crowd_talk),
              f"{len(crowd_talk)} screens sampled")


def walk_dares(page, rep):
    """PARKED 2026-09-19 — slice 7 as it stood: the dares are a chain, and two is shut
    until one is done."""
    start(page, "Monday", 12, "the_quad")
    rep.check("the picking-on can fire", play(page, "picked_quad") is True)

    before = traits(page).get("dare_chain") or 0
    rep.check("the chain starts at nothing", before == 0, f"dare_chain = {before}")

    # ⚠️ NOBODY TALKS ABOUT A DARE THAT HAS NOT HAPPENED. Bree's "knows, by the
    # way" and Paige's "about the dare" used to be members of an unconditional
    # block_pool, so either could be the first thing that character ever said —
    # about an event the player had never seen. A pool cannot be gated
    # (v2.py:15088), so they are group rungs now. Sampled, because a pool answers
    # differently on every visit and one quiet visit proves nothing.
    crowd_talk = set()
    for _ in range(16):
        play(page, "bree_takes_it_home")
        crowd_talk.add(body(page))
        play(page, "paige_is_nice")
        crowd_talk.add(body(page))
    rep.check("before a dare, nobody refers to one",
              not any("knows, by the way" in b or "about the dare" in b for b in crowd_talk),
              f"{len(crowd_talk)} screens sampled at dare_chain 0")

    # Offering is not doing. dare_1_offer sends her to the union; the chain, the
    # standing and the quiet week are all set on dare_1_do's exit.
    play(page, "dare_1_offer")
    click(page, "Say yes")
    click(page, "The union, then")
    stand_at(page, "the_union")
    play(page, "dare_1_do")
    click(page, "Do it")
    click(page, "Back over to them")
    after = traits(page).get("dare_chain") or 0
    rep.check("doing dare one advances the chain", after > before,
              f"dare_chain {before} -> {after}")
    rep.check("and it buys the quiet week",
              (traits(page).get("quiet_week") or 0) > 0,
              f"quiet_week = {traits(page).get('quiet_week')}")

    # ...and once it HAS happened, the crowd has it. The other half of the gate:
    # a rung that never fires is as wrong as one that always does.
    stand_at(page, "the_quad")
    after_talk = set()
    for _ in range(16):
        play(page, "bree_takes_it_home")
        after_talk.add(body(page))
    rep.check("after a dare, it reaches her brother's year",
              any("knows, by the way" in b for b in after_talk),
              f"{len(after_talk)} screens sampled at dare_chain {after}")


def walk_house(page, rep):
    """Slice 8 — dinner, the ten o'clock rule, and the classroom door."""
    start(page, "Monday", 19, "the_kitchen")
    rep.check("dinner is reachable", play(page, "dinner") is True)

    start(page, "Monday", 23, "the_street")
    before = traits(page).get("home_after_ten") or 0
    play(page, "in_after_ten")
    click(page, "Go up")
    rep.check("coming in after ten is counted",
              (traits(page).get("home_after_ten") or 0) > before,
              f"home_after_ten {before} -> {traits(page).get('home_after_ten')}")

    start(page, "Tuesday", 13, "the_classroom")
    rep.check("the classroom door opens", play(page, "classroom_door") is True)


def walk_phone(page, rep):
    """Slice 9 — the phone arrives with the game.

    ⚠️ PARKED 2026-09-19 (the climbs): Cara's thread getting shorter ran on her relation,
    and the messages that read it are parked. Those checks are walk_cara_thread under
    PARKED_ROUTES.
    """
    start(page, "Monday", 12, "her_room")
    # It is game_state.phone — there is no top-level `phone_state`.
    phone = (sv(page).get("game_state") or {}).get("phone")
    rep.check("the phone is bought by finishing the opening", phone is not None,
              f"game_state.phone keys: {list(phone)[:5] if isinstance(phone, dict) else phone}")


def walk_cara_thread(page, rep):
    """PARKED 2026-09-19 — slice 9 as it stood: Cara's thread gets shorter, and that is
    the mechanic."""
    start(page, "Monday", 12, "her_room")
    # It is game_state.phone — there is no top-level `phone_state`.
    phone = (sv(page).get("game_state") or {}).get("phone")
    rep.check("the phone is bought by finishing the opening", phone is not None,
              f"game_state.phone keys: {list(phone)[:5] if isinstance(phone, dict) else phone}")

    rel = (sv(page)["npcs"].get("npc_cara") or {}).get("core_traits", {}).get("relation")
    rep.check("Cara carries a relation meter", rel is not None, f"relation = {rel}")

    apply_effect(page, "relation", "add", 5, target="npc", npc_id="npc_cara")
    warm = sv(page)["npcs"]["npc_cara"]["core_traits"]["relation"]
    apply_effect(page, "relation", "set", 0, target="npc", npc_id="npc_cara")
    cold = sv(page)["npcs"]["npc_cara"]["core_traits"]["relation"]
    rep.check("her relation moves both ways — the thread can shorten",
              warm > rel and cold == 0, f"{rel} -> {warm} -> {cold}")


def _travel(page, rep):
    """Slice 10 — the map itself. Every room can be left, and being broke never
    seals her into one.

    ⚠️ THIS IS THE ROUTE THAT WOULD HAVE CAUGHT THE SOFTLOCK, AND THAT IS WHY IT
    CLICKS INSTEAD OF TELEPORTING. Every other route here moves with stand_at +
    goto, so not one of them has ever traversed an exit LINK — which is exactly
    how a one-way room shipped. the_quad used to carry `costs = { time = 40,
    cash = 2 }`, the bus fare, and a location's entry cost is charged on ANY move
    into it (v2.py:16267), including the move back out of one of its own rooms.

    ⚠️ AND WHAT IT DID AT $0 WAS WORSE THAN A CLEAN BLOCK — it was a COIN FLIP.
    The intercept runs on `passagestart` and its `return` does not cancel the
    navigation, so the destination still rendered: if a random ambient auto-fired
    at the quad it took the screen and she got in FREE, uncharged; if nothing
    fired, the queued Engine.play("TravelBlock") won and the only link on it went
    back where she came from. Verified on the pre-fix build, both branches.

    ⚠️ THE DICE ARE OFF FOR THIS WHOLE ROUTE, ON PURPOSE. A random canvas taking the
    screen on arrival is the documented cause of three false failures in this
    file (see the module docstring), so this route removes the dice and asks
    `current_location` — state — whether she moved. It used to do that by setting
    `quiet_week`, which the ambients read; that counter went with the dares on
    2026-09-19, so walk_travel below pins Math.random instead (dice_off).
    """
    # --- broke, in the deepest room on campus --------------------------------
    start(page, "Monday", 11, "the_lecture_hall")
    apply_effect(page, "cash", "set", 0, clamp=False)
    goto(page, "Location_the_lecture_hall")
    before = sv(page)["game_state"]["time_state"]
    click(page, "Leave The Lecture Hall")
    rep.check("broke, she can still walk out of a lecture",
              sv(page)["player"]["current_location"] == "the_quad",
              f'{sv(page)["player"]["current_location"]} · {passage(page)}')

    after = sv(page)["game_state"]["time_state"]
    moved = ((after["current_hour"] * 60 + after["current_minute"])
             - (before["current_hour"] * 60 + before["current_minute"]))
    rep.check("crossing her own campus costs nothing and no time",
              cash(page) == 0 and moved == 0,
              f"cash {cash(page)}, clock moved {moved} minutes")

    # --- and off it, on foot, for nothing ------------------------------------
    # THE WALK IS ITS OWN LINK, and that is the check. LO killed the first version
    # of this, where one canvas offered "bus or walk" as choices on one screen:
    # "Walk are choice in the get the bus link. That's wrong." A canvas `name` is
    # the link label on the location screen, so two canvases means two links and
    # the choice is made before she opens either. Whether the free one is OFFERED
    # is the whole safety net, so this asks the rendered links.
    goto(page, "Location_the_quad")
    offered = links(page)
    rep.check("both ways home are their own link on the quad",
              any("bus home" in l.lower() for l in offered)
              and any("walk home" in l.lower() for l in offered), str(offered)[:130])
    rep.check("the free one opens", play(page, "walk_back_quad") is True)
    click(page, "Home. An hour")
    rep.check("broke, she can still get home",
              sv(page)["player"]["current_location"] == "the_street",
              f'{sv(page)["player"]["current_location"]} · {passage(page)}')

    # --- and the fare still bites when she has it ----------------------------
    start(page, "Monday", 9, "the_bus_stop")
    apply_effect(page, "cash", "set", 10, clamp=False)
    goto(page, "Location_the_bus_stop")
    offered = links(page)
    rep.check("both ways out are their own link at the stop",
              any("get the bus" in l.lower() for l in offered)
              and any("walk it" in l.lower() for l in offered), str(offered)[:130])
    rep.check("the bus is a thing she chooses", play(page, "catch_the_bus") is True)
    t0 = sv(page)["game_state"]["time_state"]
    click(page, "Up to the campus")
    rep.check("the bus goes to the campus",
              sv(page)["player"]["current_location"] == "the_quad",
              f'{sv(page)["player"]["current_location"]} · {passage(page)}')
    t1 = sv(page)["game_state"]["time_state"]
    mins = ((t1["current_hour"] * 60 + t1["current_minute"])
            - (t0["current_hour"] * 60 + t0["current_minute"]))
    rep.check("the bus charges two dollars and forty minutes",
              cash(page) == 8 and mins == 40,
              f"cash 10 -> {cash(page)}, {mins} minutes")

    # --- with nothing in her pocket the fare is shown, not hidden ------------
    # COUNTS, not label text: the labels carry the price as a numeral for
    # gates.py G21 and will be reworded again.
    apply_effect(page, "cash", "set", 0, clamp=False)
    stand_at(page, "the_bus_stop")
    play(page, "catch_the_bus")
    rep.check("broke, both fares grey out instead of vanishing",
              len(locked(page)) == 2, f"{len(locked(page))} locked: {str(locked(page))[:90]}")
    play(page, "walk_it")
    rep.check("broke, the walk is untouched on its own screen",
              not locked(page) and len(links(page)) == 3,
              f"{len(locked(page))} locked, {len(links(page))} live: {str(links(page))[:90]}")


def walk_travel(page, rep):
    """Slice 10 — the map itself, walked with the dice off. See _travel."""
    dice_off(page)
    try:
        _travel(page, rep)
    finally:
        dice_on(page)


def walk_lock(page, rep):
    """Slice 11 — her own door, and the fact that it is now the gate on going live.

    ⚠️ THIS ROUTE EXISTS BECAUSE `walk_stream` CANNOT COVER IT. That route reaches
    the scene with play(), which is Engine.play() on the canvas passage and skips
    trigger conditions entirely (playtest.py:245). It proves the scene works and
    says nothing at all about whether the door is shut. From 2026-09-17 the door IS
    the gate, so the gate needs a route that goes the way a player goes.
    """
    # ⚠️ THIS WAS 14:00 UNTIL HER MUM'S WEEK WENT IN ON 2026-09-20, and the move is
    # the finding, not the fix: two o'clock on a Monday is no longer an empty house.
    # She is on the bathroom floor with the washing from half one to half two, and
    # the_house_day.md called that whole afternoon "her window". 10:00 is what is
    # left of it on a Monday — the two hours her mum is out on the strip.
    # `house_empty` feeds `her_door`'s prose only, not a gate, so nothing shut; the
    # hours it describes just got smaller, which is her week doing its job.
    start(page, "Monday", 10, "her_room")
    apply_flag(page, "door_locked", "unset")
    rep.check("the house is empty at two on a Monday",
              sv(page, "SugarCube.setup.triggerConditionsSatisfied("
                       "SugarCube.setup.stage_helpers_map['house_empty'].conditions)") is True,
              "house_empty helper")

    goto(page, "Location_her_room")
    rep.check("her door is a row in her own room",
              any("door" in x.lower() for x in links(page)), str(links(page))[:90])

    play(page, "her_door")
    rep.check("with nobody in, one way to shut it is offered",
              sum(1 for x in links(page) if "Shut the door" in x) == 1,
              str(links(page))[:110])
    click(page, "Shut the door")
    rep.check("shutting it sets the flag", flags(page).get("door_locked") is True,
              f"door_locked = {flags(page).get('door_locked')}")

    # ⚠️ PARKED 2026-09-19: the full-house half of this route. It shut the door with
    # @nate home at four and asserted `door_noticed` went up and stayed up. Both the
    # afternoon rows that put him home and the tally itself were parked
    # (games/the_balance/parked/README.md); the checks are at ff91336 in this file.

    rep.check("shut, the door offers the way back open",
              any("Open it again" in x for x in links(page)), str(links(page))[:110])
    click(page, "Open it again")
    rep.check("opening it clears the flag", not flags(page).get("door_locked"),
              f"door_locked = {flags(page).get('door_locked')}")

    # THE GATE ITSELF, asked of the engine rather than of a label.
    stream_ok = ("SugarCube.setup.triggerConditionsSatisfied((SugarCube.setup.help_data.locationCanvases"
                 "['her_room'].filter(function(c){return c.id==='stream';})[0]||{})"
                 ".conditions)")
    rep.check("door open, the stream is shut — at two on a Monday, inside its old window",
              sv(page, stream_ok) is False, "stream trigger conditions")
    apply_flag(page, "door_locked", "set")
    rep.check("door shut, the stream opens", sv(page, stream_ok) is True,
              "stream trigger conditions")

    # And the hours really are gone: Saturday morning was refused by the old
    # schedules and is the proof the clock no longer has anything to do with it.
    set_time(page, "Saturday", 9)
    rep.check("shut, it opens on a Saturday morning the old schedule refused",
              sv(page, stream_ok) is True, "Saturday 09:00")

    # The day tick puts the house back to his rule.
    advance_time(page, 60 * 20)
    rep.check("the door is open again by morning",
              not flags(page).get("door_locked"),
              f"door_locked = {flags(page).get('door_locked')}")


def walk_afternoon(page, rep):
    """Slice 12 — the hours the house used to hold nobody at all."""
    start(page, "Tuesday", 12, "the_kitchen")
    rep.check("at noon he is in the kitchen", npc_at(page, "npc_nate") == "the_kitchen",
              str(npc_at(page, "npc_nate")))
    rep.check("and there is a card for him",
              "Nate" in npcs_at(page, "the_kitchen") or npcs_at(page, "the_kitchen"),
              str(npcs_at(page, "the_kitchen"))[:90])

    start(page, "Tuesday", 14, "the_garage")
    rep.check("at two he is in the garage — a room that held nobody",
              npc_at(page, "npc_nate") == "the_garage", str(npc_at(page, "npc_nate")))
    play(page, "garage_nate")
    click(page, "Give him a hand")
    rep.check("helping him moves him", (snapshot(page).get(("npc_nate", "relation")) or 0) > 0,
              f"relation = {snapshot(page).get(('npc_nate', 'relation'))}")
    rep.check("and it costs her clean", (traits(page).get("clean") or 0) < 100,
              f"clean = {traits(page).get('clean')}")
    rep.check("one go at him a day, wherever it happens",
              flags(page).get("nate_today") is True,
              f"nate_today = {flags(page).get('nate_today')}")

    start(page, "Tuesday", 17, "the_garage")
    rep.check("at five it is @gil out there instead",
              npc_at(page, "npc_gil") == "the_garage" and npc_at(page, "npc_nate") != "the_garage",
              f"gil={npc_at(page, 'npc_gil')} nate={npc_at(page, 'npc_nate')}")

    # The fence on his afternoon door — the sleep-pass lesson, checked.
    start(page, "Tuesday", 16, "nate_room")
    play(page, "hub_nate_room")
    rep.check("his shut door is a surface at four", "hub_nate_room" in passage(page),
              passage(page))
    # ⚠️ THIS ASSERTION USED TO BE ITS OWN OPPOSITE. Until the ambients pass the
    # knock was fenced to the afternoon and `nate_door` owned the night. `nate_door`
    # is a random roll now, and a random canvas is skipped from every room list — so
    # without the knock covering these hours his room would render empty on a miss.
    start(page, "Tuesday", 23, "nate_room")
    rep.check("and it covers his night hours too, now the walk-in is a roll",
              "hub_nate_room" in str(sv(
                  page, "SugarCube.setup.help_data.locationCanvases['nate_room']"
                        ".filter(function(c){return SugarCube.setup.isCanvasSelectable(c);})"
                        ".map(function(c){return c.id;})")),
              "selectable at 23:00")

    # ⚠️ THIS BLOCK USED TO ASSERT THE OPPOSITE. Until the kitchen pass `dinner` was
    # gated on her mum and did not fire on a ward night, so `kitchen_nate` carried a
    # [0, 2, 4] 19:00 window to keep him from being a dead row. `dinner` runs all
    # seven nights now and that window came off, so what backs him at that table is
    # `dinner` itself — presence.py counts him because he SPEAKS in it.
    start(page, "Monday", 19, "the_kitchen")
    rep.check("on a ward night he is still at the table",
              npc_at(page, "npc_nate") == "the_kitchen", str(npc_at(page, "npc_nate")))
    rep.check("and the thing behind him there is dinner, not a second card",
              offered(page, "the_kitchen", "dinner")
              and not offered(page, "the_kitchen", "kitchen_nate"),
              "dinner offered, kitchen_nate not")


def walk_bathroom(page, rep):
    """Slice 13 — the threshold, the lock, and what is behind it.

    ⚠️ THE DOOR IS A PURE RENDER (v2.py:10078-10093). It writes no `current_location`
    and is whitelisted in isRerenderSafe, so the assertion every other route in this
    file uses — current_location == the slug — FAILS on a doored location and would
    report a working threshold as broken. Assert on `passage()` here instead.

    ⚠️ AND `start()` IS NOT ENOUGH ON ITS OWN. This build opens on
    CustomizeCharacters (v2.py:700 — any game with customizable NPCs does), and
    `stand_at` writes state without rendering a screen, so a click lands on the
    character-creation form. Every card click below is preceded by an explicit
    goto to the hall.

    ⚠️ AND NOTHING ELSE IN THIS FILE REACHES IT. `goto`, `stand_at` and `play` all
    address a passage directly and bypass the threshold entirely; only an
    engine-generated nav surface routes through it (v2.py:20601). That is why this
    route CLICKS the card.
    """
    # Empty room, mid-morning. One way through and it is the plain one.
    start(page, "Monday", 10, "the_hall")
    goto(page, "Location_the_hall")
    click(page, "The Bathroom")
    rep.check("the bathroom is a threshold now, not a room",
              passage(page) == "Door_the_bathroom", passage(page))
    rep.check("a pure render writes no location",
              sv(page)["player"]["current_location"] != "the_bathroom",
              str(sv(page)["player"]["current_location"]))
    rep.check("empty, the only way through is in",
              links(page) and all("Knock" not in x for x in links(page)),
              str(links(page))[:110])

    # @nate is in there at ten past seven and everybody locks it.
    start(page, "Tuesday", 7, "the_hall")
    apply_flag(page, "lock_broken", "unset")
    rep.check("at ten past seven the room is his",
              npc_at(page, "npc_nate") == "the_bathroom", str(npc_at(page, "npc_nate")))
    goto(page, "Location_the_hall")
    click(page, "The Bathroom")
    rep.check("locked, she can knock", any("Knock" in x for x in links(page)),
              str(links(page))[:110])
    # ⚠️ THE REFUSAL IS PROSE ON THE THRESHOLD, NOT A GREYED ROW. A shown-locked row
    # always renders, live or greyed, so no set of conditions gives "greyed while
    # locked, absent once broken" — the door says it in fiction instead.
    rep.check("locked, the threshold says so in its own words",
              "handle does not turn" in body(page), body(page)[:120])
    rep.check("and there is no way in offered at all",
              not any("Open it anyway" in x for x in links(page)), str(links(page))[:110])
    rep.check("the lock cannot be looked at with somebody behind it",
              not any("lock" in x.lower() for x in links(page)), str(links(page))[:110])

    click(page, "Knock")
    rep.check("being refused is what teaches her the lock",
              flags(page).get("knocked_once") is True,
              f"knocked_once = {flags(page).get('knocked_once')}")

    # Now the room is empty and she has been refused once.
    start(page, "Tuesday", 10, "the_hall")
    goto(page, "Location_the_hall")
    click(page, "The Bathroom")
    rep.check("empty and refused once, the lock is worth a look",
              any("lock" in x.lower() for x in links(page)), str(links(page))[:110])
    click(page, "proper look")
    click(page, "Turn the barrel round")
    rep.check("breaking it sticks", flags(page).get("lock_broken") is True,
              f"lock_broken = {flags(page).get('lock_broken')}")

    # @gil showers at six now, and the handle turns.
    start(page, "Tuesday", 18, "the_hall")
    rep.check("at six the bathroom is @gil's",
              npc_at(page, "npc_gil") == "the_bathroom", str(npc_at(page, "npc_gil")))
    goto(page, "Location_the_hall")
    click(page, "The Bathroom")
    rep.check("broken, both ways through are live",
              any("Knock" in x for x in links(page))
              and any("Open it anyway" in x for x in links(page)),
              str(links(page))[:130])
    rep.check("and the threshold stops saying it is shut",
              "handle does not turn" not in body(page), body(page)[:120])

    # The ladder. Corruption decides the menu; she still picks from it.
    apply_effect(page, "corruption", "set", 5, clamp=False)
    play(page, "bath_gil")
    rep.check("at five she can only get out", len(links(page)) == 1, str(links(page))[:110])
    apply_effect(page, "corruption", "set", 15, clamp=False)
    play(page, "bath_gil")
    rep.check("at fifteen she can stay", any("Stand there" in x for x in links(page)),
              str(links(page))[:110])
    click(page, "Stand there")
    rep.check("staying is one-time and it is recorded",
              flags(page).get("gil_bath_watched") is True,
              f"gil_bath_watched = {flags(page).get('gil_bath_watched')}")
    apply_effect(page, "corruption", "set", 30, clamp=False)
    play(page, "bath_gil")
    rep.check("at thirty the top rung opens",
              any("rest of the way" in x for x in links(page)), str(links(page))[:110])

    # ⚠️ HER MUM HAS TWO RUNGS AND NEVER A THIRD. DECISIONS.md, amended twice.
    start(page, "Tuesday", 8, "her_room")
    apply_effect(page, "corruption", "set", 95, clamp=False)
    apply_flag(page, "lynn_bath_watched", "set")
    play(page, "bath_lynn")
    rep.check("her mum is never seen seeing, at any corruption",
              not any("see you" in x.lower() or "catch you" in x.lower()
                      for x in links(page) + locked(page)),
              str(links(page) + locked(page))[:130])

    # Tasha locks it too, and opens it for her — her whole arc is behind a knock now.
    start(page, "Tuesday", 17, "the_hall")
    apply_effect(page, "corruption", "set", 5, clamp=False)
    rep.check("at five she has the bathroom",
              npc_at(page, "npc_tasha") == "the_bathroom", str(npc_at(page, "npc_tasha")))
    goto(page, "Location_the_hall")
    click(page, "The Bathroom")
    click(page, "Knock")
    rep.check("knocking on @tasha lands in her hub, not a refusal",
              "tasha_bath" in passage(page), passage(page))


def walk_ambients(page, rep):
    """Slice 14 — the three rolls, and the cards they sit on top of.

    ⚠️ A RANDOM CANVAS CANNOT BE REACHED BY CLICKING, AND `play()` PROVES NOTHING
    ABOUT IT. play() is Engine.play() on the passage (playtest.py:245) — it would
    render the scene whatever the roll, the fence or the NPC's whereabouts said.
    What has to be asserted is SELECTABILITY: does the engine consider this canvas
    a candidate right now. That is `isCanvasSelectable` plus the requiresNpc check
    the random path applies on top of it (v2.py:5637-5648), asked directly.
    """
    def rollable(page, loc, cid):
        """Would the engine offer this random canvas here, right now?"""
        return sv(page, (
            "(function(){var L=SugarCube.setup.help_data.locationCanvases['%s']||[];"
            "for(var i=0;i<L.length;i++){var c=L[i];"
            "if(c.id!=='%s') continue;"
            "if(!SugarCube.setup.isCanvasSelectable(c)) return false;"
            "if(!c.requiresNpc) return true;"
            "var l=SugarCube.setup.getNpcLocation(c.requiresNpc);"
            "return !!(l && l.location==='%s');}"
            "return null;})()" % (loc, cid, loc)))

    start(page, "Tuesday", 16, "nate_room")
    rep.check("@nate's door is a roll now, not a one-shot",
              rollable(page, "nate_room", "nate_door") is True, "16:00 Tuesday")
    rep.check("and the room still offers the knock behind it",
              rollable(page, "nate_room", "hub_nate_room") is not None
              and play(page, "hub_nate_room") is True, passage(page))

    # THE FENCES. requires_npc alone would roll against a sleeping man.
    start(page, "Tuesday", 23, "nate_room")
    rep.check("it rolls at eleven at night as well",
              rollable(page, "nate_room", "nate_door") is True, "23:00")
    start(page, "Tuesday", 4, "nate_room")
    rep.check("he is in that room at four in the morning",
              npc_at(page, "npc_nate") == "nate_room", str(npc_at(page, "npc_nate")))
    rep.check("and it does NOT roll on him asleep",
              rollable(page, "nate_room", "nate_door") is False, "04:00")
    start(page, "Tuesday", 12, "nate_room")
    rep.check("nor when he is out of the room",
              rollable(page, "nate_room", "nate_door") is False, "12:00")

    # THE FIRST ONE IS WRITTEN FOR HER, AND IT IS THE ONLY ONE THAT COSTS A WEEK.
    start(page, "Tuesday", 23, "nate_room")
    apply_flag(page, "nate_seen", "unset")
    apply_effect(page, "nate_landing", "set", 0, clamp=False)
    play(page, "nate_door")
    rep.check("first time, no choice is offered", len(links(page)) == 1, str(links(page))[:110])
    click(page, "Get off the landing")
    click(page, "Your room")
    rep.check("the first one costs the week",
              (traits(page).get("nate_landing") or 0) == 7,
              f"nate_landing = {traits(page).get('nate_landing')}")

    apply_effect(page, "nate_landing", "set", 0, clamp=False)
    apply_effect(page, "corruption", "set", 5, clamp=False)
    play(page, "nate_door")
    rep.check("after that there is no choice she can afford yet",
              len(links(page)) == 1, str(links(page))[:110])
    click(page, "Get off the landing")
    rep.check("and the week does NOT come back",
              (traits(page).get("nate_landing") or 0) == 0,
              f"nate_landing = {traits(page).get('nate_landing')}")

    # HER AXIS.
    apply_effect(page, "corruption", "set", 15, clamp=False)
    play(page, "nate_door")
    rep.check("at fifteen she can stay", any("doorway" in x for x in links(page)),
              str(links(page))[:110])
    click(page, "Stay in the doorway")
    click(page, "Your room")
    apply_effect(page, "corruption", "set", 30, clamp=False)
    play(page, "nate_door")
    rep.check("at thirty she can let him see her",
              any("see you looking" in x for x in links(page)), str(links(page))[:110])

    # HIS AXIS — same screen, different man.
    apply_effect(page, "arousal", "set", 0, target="npc", npc_id="npc_nate", clamp=False)
    play(page, "nate_door")
    low = body(page)
    apply_effect(page, "arousal", "set", 12, target="npc", npc_id="npc_nate", clamp=False)
    play(page, "nate_door")
    rep.check("his arousal changes what he does about it", low != body(page),
              body(page)[:110])

    # THE PARENTS.
    start(page, "Tuesday", 21, "the_master_bedroom")
    rep.check("the parents' scene is a roll now",
              rollable(page, "the_master_bedroom", "master_bedroom") is True, "Tue 21:00")
    start(page, "Monday", 21, "the_master_bedroom")
    rep.check("and never on a ward night",
              rollable(page, "the_master_bedroom", "master_bedroom") is False, "Mon 21:00")
    rep.check("which is the night @gil has a card in there instead",
              play(page, "hub_gil_bed") is True, passage(page))
    start(page, "Tuesday", 22, "the_master_bedroom")
    rep.check("and her mum has one the other four", play(page, "hub_lynn_bed") is True,
              passage(page))

    # TASHA.
    start(page, "Tuesday", 20, "tasha_room")
    rep.check("@tasha's room rolls in the evening",
              rollable(page, "tasha_room", "tasha_caught") is True, "Tue 20:00")
    start(page, "Tuesday", 8, "tasha_room")
    rep.check("she is asleep in there at eight",
              npc_at(page, "npc_tasha") == "tasha_room", str(npc_at(page, "npc_tasha")))
    rep.check("and it does NOT roll on her asleep",
              rollable(page, "tasha_room", "tasha_caught") is False, "08:00")
    start(page, "Tuesday", 20, "tasha_room")
    apply_effect(page, "corruption", "set", 30, clamp=False)
    apply_flag(page, "tasha_caught_watched", "set")
    play(page, "tasha_caught")
    rep.check("her top rung is being caught wanting it",
              any("find you there" in x for x in links(page)), str(links(page))[:110])

    # AND THE SUBSTITUTION SURVIVED THE CONVERSION.
    rep.check("`master_caught` is still bound to its host",
              "master_caught" in str(sv(page, "SugarCube.setup.canvasSubstitutions")),
              "canvasSubstitutions")


def walk_kitchen(page, rep):
    """Slice 15 — the kitchen has three meals with people at them, and her mum
    has a week.

    ⚠️ WHAT THIS ROUTE EXISTS TO CATCH IS THE THING IT ALREADY CAUGHT ONCE. Her
    mum's first draft ran the house 09:00-14:00 and napped from 14:00, and between
    them those two rows left the house OCCUPIED EVERY MINUTE OF EVERY DAY — 17 empty
    hours a week went to zero. `house_empty` is read by `her_door`, so the branch
    where shutting her door costs nothing became unreachable and every stream in the
    game would have gone on @gil's count. The build was green. presence.py was
    green. gates.py was green. Four assertions in `lock` went red at once.
    """
    # ── the three meals ──────────────────────────────────────────────────────
    start(page, "Monday", 7, "the_kitchen")
    set_time(page, "Monday", 7, 50)
    here = npcs_at(page, "the_kitchen")
    rep.check("breakfast on a ward morning holds three of them",
              len(here) == 3, str(here))
    rep.check("and one of them is her mum, who used to be asleep or gone",
              npc_at(page, "npc_lynn") == "the_kitchen", str(npc_at(page, "npc_lynn")))
    rep.check("@nate is out of the shower and in the room",
              npc_at(page, "npc_nate") == "the_kitchen", str(npc_at(page, "npc_nate")))
    rep.check("her mum's breakfast card is offered",
              offered(page, "the_kitchen", "hub_lynn_kitchen"), "hub_lynn_kitchen")

    set_time(page, "Saturday", 7, 50)
    rep.check("at the weekend breakfast is @gil on his own",
              npcs_at(page, "the_kitchen") == ["npc_gil"], str(npcs_at(page, "the_kitchen")))
    rep.check("and he is there at all, which he was not before this pass",
              npc_at(page, "npc_gil") == "the_kitchen", str(npc_at(page, "npc_gil")))

    start(page, "Monday", 12, "the_kitchen")
    set_time(page, "Monday", 12, 30)
    rep.check("lunch has two people in it and needed no canvas to",
              sorted(npcs_at(page, "the_kitchen")) == ["npc_lynn", "npc_nate"],
              str(npcs_at(page, "the_kitchen")))

    start(page, "Tuesday", 19, "the_kitchen")
    set_time(page, "Tuesday", 19, 30)
    rep.check("dinner on a full night is four of them",
              len(npcs_at(page, "the_kitchen")) == 4, str(npcs_at(page, "the_kitchen")))
    rep.check("and dinner fires", offered(page, "the_kitchen", "dinner"), "dinner")
    rep.check("Tasha has a card at that table for the first time",
              offered(page, "the_kitchen", "hub_tasha_kitchen"), "hub_tasha_kitchen")

    start(page, "Monday", 19, "the_kitchen")
    set_time(page, "Monday", 19, 30)
    rep.check("on a ward night the table is two of them",
              len(npcs_at(page, "the_kitchen")) == 2, str(npcs_at(page, "the_kitchen")))
    rep.check("and dinner fires anyway, which it never used to",
              offered(page, "the_kitchen", "dinner"), "dinner")
    rep.check("Tasha's card is correctly absent on a night she is not there",
              not offered(page, "the_kitchen", "hub_tasha_kitchen"), "no hub_tasha_kitchen")

    # ── her mum's week ───────────────────────────────────────────────────────
    start(page, "Monday", 10, "the_kitchen")
    rep.check("at ten on a ward day she is doing the house",
              npc_at(page, "npc_lynn") == "the_kitchen", str(npc_at(page, "npc_lynn")))
    rep.check("and helping her is a card",
              offered(page, "the_kitchen", "chores_with_mum"), "chores_with_mum")

    start(page, "Monday", 14, "her_room")
    rep.check("at two she is out at the shop and the house is EMPTY",
              npc_at(page, "npc_lynn") is None
              and bool(sv(page, "SugarCube.setup.triggerConditionsSatisfied("
                             "SugarCube.setup.stage_helpers_map['house_empty'].conditions)")),
              f"lynn={npc_at(page, 'npc_lynn')}")

    start(page, "Monday", 16, "the_hall")
    rep.check("at four she is asleep before the shift",
              npc_at(page, "npc_lynn") == "the_master_bedroom", str(npc_at(page, "npc_lynn")))
    rep.check("and there is nothing to click on a sleeping woman",
              not offered(page, "the_master_bedroom", "hub_lynn_bed"), "occupancy only")

    start(page, "Tuesday", 16, "the_front_room")
    rep.check("the morning after a ward night she is on the sofa at four",
              npc_at(page, "npc_lynn") == "the_front_room", str(npc_at(page, "npc_lynn")))
    rep.check("and her sofa card covers the afternoon as well as the evening",
              offered(page, "the_front_room", "hub_lynn_sofa"), "hub_lynn_sofa at 16:00")

    start(page, "Sunday", 10, "the_kitchen")
    rep.check("Sunday is no longer twelve empty hours",
              npc_at(page, "npc_lynn") == "the_kitchen", str(npc_at(page, "npc_lynn")))

    # ── cooking ──────────────────────────────────────────────────────────────
    start(page, "Monday", 17, "the_kitchen")
    rep.check("on a ward night she can cook", offered(page, "the_kitchen", "cook"), "cook")
    rep.check("and her mum's version is correctly not offered",
              not offered(page, "the_kitchen", "cook_with_mum"), "no cook_with_mum")
    before = cash(page)
    play(page, "cook")
    click(page, "Make something proper")
    click(page, "Get out of the kitchen")
    rep.check("cooking sets the flag the table reads",
              flags(page).get("cooked_today") is True,
              f"cooked_today = {flags(page).get('cooked_today')}")
    # ⚠️ ASSERT THE DELTA, NOT THE BALANCE. Running the whole suite carries cash in
    # from `opening`, so a literal here reads as a failure on the second route and a
    # pass on its own — the exact false alarm this file's header warns about.
    rep.check("and it pays in @gil, never in cash",
              (snapshot(page).get(("npc_gil", "relation")) or 0) > 0
              and cash(page) == before,
              f"gil={snapshot(page).get(('npc_gil', 'relation'))} cash {before} -> {cash(page)}")
    rep.check("once it is made, the card is gone for the day",
              not offered(page, "the_kitchen", "cook"), "cook spent")

    start(page, "Tuesday", 18, "the_kitchen")
    rep.check("on her mum's night it is the other surface",
              offered(page, "the_kitchen", "cook_with_mum")
              and not offered(page, "the_kitchen", "cook"), "cook_with_mum only")
    rep.check("she is at the hob before @gil comes down",
              npc_at(page, "npc_lynn") == "the_kitchen", str(npc_at(page, "npc_lynn")))
    play(page, "cook_with_mum")
    click(page, "Help her with it")
    click(page, "Get it on the table")
    rep.check("helping her sets the same flag",
              flags(page).get("cooked_today") is True,
              f"cooked_today = {flags(page).get('cooked_today')}")
    rep.check("and it moves the one meter she has",
              (snapshot(page).get(("npc_lynn", "relation")) or 0) > 0,
              f"lynn relation = {snapshot(page).get(('npc_lynn', 'relation'))}")
    rep.check("one go at her mum a day, wherever it happens",
              flags(page).get("lynn_today") is True,
              f"lynn_today = {flags(page).get('lynn_today')}")

    # The cap is on HER, not on the hour — the house at ten spends the hob at six.
    start(page, "Sunday", 10, "the_kitchen")
    apply_flag(page, "lynn_today", "set")
    set_time(page, "Sunday", 18)
    # ⚠️ `locked()` is the right instrument here and `links()` is not — the row
    # renders greyed with its `locked_text`, it does not disappear (the-surfaces
    # R5, and the pattern `hub_gil_kitchen` has used since the afternoon pass).
    play(page, "cook_with_mum")
    # ⚠️ `locked()` RETURNS THE locked_text, NOT THE LABEL (playtest.py). So the
    # thing to look for is the refusal the author wrote, not the choice it replaced.
    rep.check("having helped in the morning, the evening greys out",
              any("go at your mum" in x for x in locked(page))
              and not any("Help her" in x for x in links(page)),
              f"locked={locked(page)}")

    # ── the kettle ───────────────────────────────────────────────────────────
    start(page, "Monday", 16, "the_kitchen")
    apply_effect(page, "rest", "set", 40)
    rep.check("the kitchen has a light thing at four in the afternoon",
              offered(page, "the_kitchen", "kettle"), "kettle")
    play(page, "kettle")
    click(page, "Stand and drink it")
    rep.check("standing in it repairs a little rest",
              (traits(page).get("rest") or 0) > 40, f"rest = {traits(page).get('rest')}")
    rep.check("and it is once a day", flags(page).get("kettle_today") is True,
              f"kettle_today = {flags(page).get('kettle_today')}")
    rep.check("spent, the room KEEPS the card — the cap is on the choice",
              offered(page, "the_kitchen", "kettle"), "kettle still offered")


def walk_three(page, rep):
    """sheets/people/the_other_three.md — Gil, Nate and Tasha's hours, round 3.

    ⚠️ THREE THINGS THE BUILD GOT WRONG UNTIL 2026-09-22, and each has a check below.
    Five lines across four sheets put @gil in the garage late and he had no garage row.
    the_cast.md:29 gives @nate a move that only works on campus and he was never on it.
    And all three of them ended at 23:59 or earlier and vanished, so the house between
    midnight and half six held nobody but her mum.
    """
    start(page, "Monday", 12, "her_room")

    # ⚠️ THE THREE, AND NOT HER MUM. She is on the ward from 18:45 on Monday, Wednesday
    # and Friday, so at four on a Thursday morning she is CORRECTLY nowhere — that is a
    # gap reading as absent, not a missing row. These three had no reason to be missing
    # and were, every night, from midnight.
    for day, hour in (("Monday", 3), ("Thursday", 4), ("Sunday", 5)):
        set_time(page, day, hour, 0)
        where = {n: npc_at(page, n) for n in ("npc_gil", "npc_nate", "npc_tasha")}
        rep.check(f"{day[:3]} {hour:02d}:00 — all three of them are in their own beds",
                  all(where.values()), str(where))

    # ⚠️ 22:45 AND NOT 23:00 SINCE 2026-09-23. His garage rows now end at eleven so
    # the bathroom can have him, and an end time is EXCLUSIVE — at 23:00 sharp he is
    # already through the door with the tap running. gil_cards.md.
    for day, hour, minute in (("Monday", 22, 45), ("Tuesday", 22, 30), ("Friday", 20, 0)):
        set_time(page, day, hour, minute)
        rep.check(f"{day[:3]} {hour:02d}:{minute:02d} — @gil is in the garage",
                  npc_at(page, "npc_gil") == "the_garage", str(npc_at(page, "npc_gil")))

    # ⚠️ THE CONTRADICTION THE PAGE RESOLVED. the_two_doors.md:18 needs @gil and her mum
    # behind one door before ten; her_week.md:109 and the_house_day.md:26 need him still
    # in the garage after it. He goes up at quarter to nine and comes back down at ten.
    set_time(page, "Tuesday", 21, 0)
    rep.check("nine on a Tuesday — @gil and her mum are behind the same door",
              npc_at(page, "npc_gil") == "the_master_bedroom"
              and npc_at(page, "npc_lynn") == "the_master_bedroom",
              f"gil {npc_at(page, 'npc_gil')}, lynn {npc_at(page, 'npc_lynn')}")
    set_time(page, "Tuesday", 22, 30)
    rep.check("and by half ten he is back down in the garage",
              npc_at(page, "npc_gil") == "the_garage", str(npc_at(page, "npc_gil")))

    set_time(page, "Monday", 12, 30)
    rep.check("half twelve on a Monday — @nate is on the quad, straight after her class",
              npc_at(page, "npc_nate") == "the_quad", str(npc_at(page, "npc_nate")))
    set_time(page, "Monday", 14, 0)
    rep.check("two o'clock — he has moved to the union",
              npc_at(page, "npc_nate") == "the_union", str(npc_at(page, "npc_nate")))
    set_time(page, "Monday", 10, 0)
    rep.check("but at ten, while she is in a lecture, he is nowhere she can go",
              npc_at(page, "npc_nate") is None, str(npc_at(page, "npc_nate")))

    set_time(page, "Friday", 20, 0)
    rep.check("Friday at eight, Tasha is out", npc_at(page, "npc_tasha") is None,
              str(npc_at(page, "npc_tasha")))
    set_time(page, "Saturday", 22, 0)
    rep.check("Saturday at ten, both of them are out",
              npc_at(page, "npc_nate") is None and npc_at(page, "npc_tasha") is None,
              f"nate {npc_at(page, 'npc_nate')}, tasha {npc_at(page, 'npc_tasha')}")
    set_time(page, "Sunday", 5, 0)
    rep.check("and by five on the Sunday they are both back in their own beds",
              npc_at(page, "npc_nate") == "nate_room" and npc_at(page, "npc_tasha") == "tasha_room",
              f"nate {npc_at(page, 'npc_nate')}, tasha {npc_at(page, 'npc_tasha')}")

    for day, hour, minute, who in (("Monday", 7, 30, "npc_nate"),
                                   ("Monday", 17, 30, "npc_tasha"),
                                   ("Monday", 18, 15, "npc_lynn")):
        set_time(page, day, hour, minute)
        inside = [n for n in ("npc_gil", "npc_nate", "npc_tasha", "npc_lynn")
                  if npc_at(page, n) == "the_bathroom"]
        rep.check(f"{hour:02d}:{minute:02d} — the bathroom holds exactly one person",
                  inside == [who], str(inside))



# ── @gil's base — sheets/people/gil_cards.md ────────────────────────────────
# day, hour, minute, where he should be. Every one of his nineteen rows is
# represented by one probe inside it; rows that differ only by weekday share a
# probe on each of their day shapes.
GIL_HOURS = [
    ("Monday",    3,  0, "the_master_bedroom"),  # asleep, weekday
    ("Sunday",    6, 30, "the_master_bedroom"),  # asleep, the weekend lie-in
    ("Monday",    6, 35, "the_master_bedroom"),  # changing, weekday
    ("Saturday",  7, 35, "the_master_bedroom"),  # changing, weekend
    ("Monday",    7,  0, "the_front_room"),      # the paper, weekday
    ("Saturday",  8,  0, "the_front_room"),      # the paper, weekend
    ("Monday",    7, 45, "the_kitchen"),         # breakfast, weekday
    ("Sunday",    8, 45, "the_kitchen"),         # breakfast, weekend
    ("Monday",   11,  0, "the_shop"),            # at work
    ("Friday",   16,  0, "the_shop"),            # at work, and the ride home hour
    ("Saturday", 12,  0, "the_garage"),          # the project, all weekend day
    ("Monday",   18, 30, "the_kitchen"),         # back at six
    ("Tuesday",  19, 30, "the_kitchen"),         # dinner, a home night
    ("Tuesday",  20, 15, "the_garage"),          # out at the car before he goes up
    ("Tuesday",  21, 30, "the_master_bedroom"),  # their door
    ("Tuesday",  22, 30, "the_garage"),          # back down
    ("Monday",   21,  0, "the_garage"),          # the long ward-night one
    ("Monday",   23, 15, "the_bathroom"),        # washing the day off
    ("Monday",   23, 35, "the_master_bedroom"),  # changing, last thing
    ("Monday",   23, 50, "the_master_bedroom"),  # the house shut
]

# canvas, room, a day and time inside its hours
GIL_CARDS = [
    ("hub_gil_paper",   "the_front_room",     "Monday",    7,  0),
    ("hub_gil_kitchen", "the_kitchen",        "Monday",    7, 45),
    ("hub_gil_kitchen", "the_kitchen",        "Monday",   18, 30),
    ("garage_gil",      "the_garage",         "Monday",   21,  0),
    ("hub_gil_shop",    "the_shop",           "Monday",   11,  0),
    ("hub_gil_bed",     "the_master_bedroom", "Monday",    3,  0),
    ("gil_changing",    "the_master_bedroom", "Monday",    6, 35),
    ("gil_their_door",  "the_master_bedroom", "Tuesday",  21, 30),
]


def walk_gil(page, rep):
    """sheets/people/gil_cards.md — @gil's nineteen rows and his eight cards.

    ⚠️ HE HAD A FACE FOR FOUR HOURS A WEEK. `friday_payment`, Friday 17:00-21:00,
    was the only canvas in this game carrying `npc = "npc_gil"` that was not a
    substitution, and eight of his twelve rows were dead — every garage hour and
    every bedroom hour. This route is the check that the eight cards actually
    render, which `presence.py` reads off the TOML and cannot prove.
    """
    start(page, "Monday", 12, "her_room")

    # ── his week, row by row
    for day, hour, minute, where in GIL_HOURS:
        set_time(page, day, hour, minute)
        rep.check(f"{day[:3]} {hour:02d}:{minute:02d} — @gil is at {where}",
                  npc_at(page, "npc_gil") == where, str(npc_at(page, "npc_gil")))

    # ── the ten hours he is out are now nine and a half AT A PLACE, and the shop
    # is shut at the weekend because his own week shuts it, not because a rule does
    set_time(page, "Saturday", 11, 0)
    rep.check("Saturday at eleven — the shop is not somewhere he is",
              npc_at(page, "npc_gil") == "the_garage", str(npc_at(page, "npc_gil")))
    set_time(page, "Monday", 17, 45)
    rep.check("half five on a Monday — he has left the shop and is not home yet",
              npc_at(page, "npc_gil") is None, str(npc_at(page, "npc_gil")))

    # ── every card is offered in its own hours
    for cid, room, day, hour, minute in GIL_CARDS:
        set_time(page, day, hour, minute)
        stand_at(page, room)
        rep.check(f"{cid} is offered at {day[:3]} {hour:02d}:{minute:02d}",
                  offered(page, room, cid) is True,
                  f"gil at {npc_at(page, 'npc_gil')}")

    # ── ⚠️ THE ONE THE SELECTOR DECIDES. Three of his cards share the master
    # bedroom and only ONE canvas per NPC per location is ever drawn (v2.py:4943).
    # Their schedules are disjoint, so each of these three hours must draw its own.
    for day, hour, minute, cid in (("Monday",   3,  0, "hub_gil_bed"),
                                   ("Monday",   6, 35, "gil_changing"),
                                   ("Tuesday", 21, 30, "gil_their_door")):
        set_time(page, day, hour, minute)
        stand_at(page, "the_master_bedroom")
        html = page.evaluate(
            "() => SugarCube.setup.renderNpcPortraits('the_master_bedroom') || ''")
        got = re.findall(r'data-passage="Canvas_([a-z_]+)_Node', html)
        rep.check(f"{day[:3]} {hour:02d}:{minute:02d} — their room draws {cid}",
                  cid in got, str(got))

    # ── ⚠️ A FACE, NOT A LINK. All eight of her mum's canvases once shipped without
    # `npc` on the trigger and printed the canvas NAME as a solo link instead of a
    # portrait. Every one of @gil's carries it; this is the check that says so.
    for room, day, hour, minute in (("the_garage",         "Monday",   21,  0),
                                    ("the_front_room",     "Monday",    7,  0),
                                    ("the_kitchen",        "Monday",   18, 30),
                                    ("the_shop",           "Monday",   11,  0),
                                    ("the_master_bedroom", "Monday",    3,  0)):
        set_time(page, day, hour, minute)
        stand_at(page, room)
        drawn = page.evaluate("""(loc) => {
            var s = SugarCube.setup;
            return { portraits: s.renderNpcPortraits(loc) || '',
                     solo: s.renderSoloActivities(loc) || '' };
        }""", room)
        rep.check(f"{room} draws his portrait, with his name on it",
                  "npc-portrait-card" in drawn["portraits"] and "Gil" in drawn["portraits"],
                  drawn["portraits"][:110] or "(nothing drawn)")
        rep.check(f"and {room} does not print him as a solo link",
                  "Gil" not in drawn["solo"], drawn["solo"][:110] or "(no solo links)")

    # ── the bathroom at eleven holds exactly one person, and it is him
    set_time(page, "Monday", 23, 15)
    inside = [n for n in ("npc_gil", "npc_nate", "npc_tasha", "npc_lynn")
              if npc_at(page, n) == "the_bathroom"]
    rep.check("23:15 — the bathroom holds exactly @gil", inside == ["npc_gil"], str(inside))

    # ── ⚠️ AND THE DOOR IS SHUT ON HER. The gate is four stage helpers AND-ed as
    # negations (0_systems_spec.toml); the runtime would have nested them and the
    # IMPORTER refuses to, so this proves the four-helper shape actually locks.
    rep.check("and the door is shut against her",
              sv(page, "SugarCube.setup.navDestUnlocked('the_bathroom')") is False,
              str(sv(page, "SugarCube.setup.navDestUnlocked('the_bathroom')")))
    set_time(page, "Monday", 13, 45)
    rep.check("but her mum's laundry hour still lets her in",
              sv(page, "SugarCube.setup.navDestUnlocked('the_bathroom')") is True,
              f"lynn at {npc_at(page, 'npc_lynn')}")
    set_time(page, "Monday", 18, 15)
    rep.check("and her mum's bath still shuts it",
              sv(page, "SugarCube.setup.navDestUnlocked('the_bathroom')") is False,
              f"lynn at {npc_at(page, 'npc_lynn')}")

    # ── THE LIFT. ⚠️ THE WHOLE POINT OF THESE THREE CHECKS IS `cash`. Decision 105
    # (2026-09-16) fenced the travel system off — "no lift, nothing touches the bus
    # fare" — and LO lifted it on 2026-09-23 only for a lift that costs time alone.
    apply_flag(page, "lift_tomorrow", "unset")
    apply_flag(page, "gil_garage_today", "unset")
    set_time(page, "Monday", 21, 0)
    stand_at(page, "the_garage")
    play(page, "garage_gil")
    before = cash(page)
    rep.check("an hour in the garage is on the card",
              any("Hand him things" in x for x in links(page)), str(links(page))[:160])
    click(page, "Hand him things")
    rep.check("and it sets tomorrow's lift",
              flags(page).get("lift_tomorrow") is True,
              f"lift_tomorrow = {flags(page).get('lift_tomorrow')}")
    rep.check("and it costs her nothing but the hour", cash(page) == before,
              f"cash {before} -> {cash(page)}")

    # ⚠️ NOT CLEARED OVERNIGHT, AND THAT IS DELIBERATE. It is bought one evening and
    # spent the next morning, so a daily_tick reset would make it unspendable.
    advance_time(page, 10 * 60)
    rep.check("the lift survives the night",
              flags(page).get("lift_tomorrow") is True,
              f"lift_tomorrow = {flags(page).get('lift_tomorrow')}")

    set_time(page, "Tuesday", 7, 45)
    stand_at(page, "the_kitchen")
    play(page, "hub_gil_kitchen")
    before = cash(page)
    rep.check("and it is on the table in the morning",
              any("Get in with him" in x for x in links(page)), str(links(page))[:200])
    click(page, "Get in with him. He goes past the campus")
    # ⚠️ ON `current_location`, NOT ON THE PASSAGE. The lift lands her on the quad and
    # a random ambient can take the screen on arrival — `picked_quad` did, on the run
    # that caught this. The passage is a rendered result; where she IS is state, and
    # the rule at the top of this file is that only state answers whether a mechanic
    # fired.
    rep.check("it puts her on the quad",
              sv(page, "SugarCube.State.variables.player.current_location") == "the_quad",
              str(sv(page, "SugarCube.State.variables.player.current_location")))
    rep.check("for nothing — the fare is untouched", cash(page) == before,
              f"cash {before} -> {cash(page)}")
    rep.check("and it is spent", flags(page).get("lift_tomorrow") is not True,
              f"lift_tomorrow = {flags(page).get('lift_tomorrow')}")

    # ── the ride home, which costs nothing and is never offered
    set_time(page, "Monday", 17, 15)
    stand_at(page, "the_shop")
    play(page, "hub_gil_shop")
    before = cash(page)
    rep.check("at a quarter past five the ride home is there",
              any("Ride home" in x for x in links(page)), str(links(page))[:160])
    click(page, "Ride home with him")
    rep.check("and it puts her on her own street",
              sv(page, "SugarCube.State.variables.player.current_location") == "the_street",
              str(sv(page, "SugarCube.State.variables.player.current_location")))
    rep.check("also for nothing", cash(page) == before, f"cash {before} -> {cash(page)}")

    set_time(page, "Monday", 16, 0)
    stand_at(page, "the_shop")
    play(page, "hub_gil_shop")
    rep.check("at four it is not — he has an hour and a half left",
              not any("Ride home" in x for x in links(page)), str(links(page))[:160])

    # ── FRIDAY IN TWO ROOMS. ⚠️ His own week broke LO's "ALL EVENING" call: he is
    # in that kitchen for ONE hour on a Friday. The garage carries the other four.
    apply_flag(page, "friday_settled", "unset")
    apply_effect(page, "cash", "set", 300, clamp=False)
    set_time(page, "Friday", 18, 30)
    stand_at(page, "the_kitchen")
    rep.check("Friday at half six — the kitchen wants the money",
              offered(page, "the_kitchen", "friday_payment") is True,
              f"gil at {npc_at(page, 'npc_gil')}")
    set_time(page, "Friday", 20, 0)
    stand_at(page, "the_garage")
    rep.check("Friday at eight — so does the garage",
              offered(page, "the_garage", "friday_payment_garage") is True,
              f"gil at {npc_at(page, 'npc_gil')}")

    # ⚠️ AND SHE CANNOT PAY BOTH. Two canvases collecting the same $150 and a purse
    # with $300 in it is exactly how a debt gets paid twice.
    before = cash(page)
    play(page, "friday_payment_garage")
    click(page, "Count it out on the bench")
    click(page, "Go in")
    rep.check("paying in the garage takes the hundred and fifty once",
              before - cash(page) == 150, f"cash {before} -> {cash(page)}")
    rep.check("and it settles Friday", flags(page).get("friday_settled") is True,
              f"friday_settled = {flags(page).get('friday_settled')}")
    set_time(page, "Friday", 18, 30)
    stand_at(page, "the_kitchen")
    rep.check("so the kitchen will not collect it again",
              offered(page, "the_kitchen", "friday_payment") is False,
              f"gil at {npc_at(page, 'npc_gil')}")
    apply_flag(page, "friday_settled", "unset")

    # ── THE DINNER CALL. The only surface in this game that moves him.
    clear_chores(page)
    set_time(page, "Monday", 19, 30)
    stand_at(page, "the_kitchen")
    rep.check("a ward night with no dinner cooked offers nothing",
              offered(page, "the_kitchen", "ward_dinner") is False,
              f"chore_done_dinner = {flags(page).get('chore_done_dinner')}")
    apply_flag(page, "chore_done_dinner", "set")
    rep.check("cook it and there is a table to call people to",
              offered(page, "the_kitchen", "ward_dinner") is True)
    rep.check("and on a night her mum IS home it is the other card",
              offered(page, "the_kitchen", "ward_dinner") is True
              and npc_at(page, "npc_lynn") is None,
              f"lynn at {npc_at(page, 'npc_lynn')}")
    set_time(page, "Tuesday", 19, 30)
    rep.check("Tuesday is `dinner`, not the call",
              offered(page, "the_kitchen", "ward_dinner") is False
              and offered(page, "the_kitchen", "dinner") is True)
    clear_chores(page)

ROUTES = {
    "opening": walk_opening,
    "week": walk_week,
    "chores": walk_chores,
    "mum": walk_mum,
    "three": walk_three,
    "gil": walk_gil,
    "alarm": walk_alarm,
    "friday": walk_friday,
    "stream": walk_stream,
    "lock": walk_lock,
    "class": walk_class,
    "crowd": walk_crowd,
    "house": walk_house,
    "phone": walk_phone,
    "travel": walk_travel,
}

# ⚠️ PARKED 2026-09-19 WITH THE CONTENT THEY WALK. Each route below asserts on scenes
# and schedule rows that were taken out of the build (games/the_balance/parked/), so
# run against it they fail or, worse, pass on checks that never reach the scene. They
# are NOT run by default and are kept, not deleted, so a round in sheets/BASE.md that
# brings their content back gets its route back with it. Name one to run it anyway.
#   kitchen    19fee19 · the kitchen's three meals and her mum's week
#   afternoon  6801814 · @nate's afternoon, the garage
#   bathroom   972a27b · the bathroom door, the knock and the lock
#   ambients   2591a11 · the house happening to her
#
# The climbs, parked the same day (games/the_balance/parked/climbs/). These walked
# DESIGNED content, block 5 of sheets/BASE.md, and come back with their ladders.
#   cafe_climb    the shift counted, and the counter as its own surface
#   stream_climb  the top-off rung, followers moving, and the landing week's lock
#   doors         @nate's door and the master bedroom
#   dares         the chain, the quiet week, and the dare reaching Nate's year
#   cara_thread   Cara's relation moving both ways
PARKED_ROUTES = {
    "kitchen": walk_kitchen,
    "afternoon": walk_afternoon,
    "bathroom": walk_bathroom,
    "ambients": walk_ambients,
    "cafe_climb": walk_cafe_climb,
    "stream_climb": walk_stream_climb,
    "doors": walk_doors,
    "dares": walk_dares,
    "cara_thread": walk_cara_thread,
}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    headed = "--headed" in sys.argv
    wanted = args or list(ROUTES)
    runnable = {**ROUTES, **PARKED_ROUTES}
    unknown = [w for w in wanted if w not in runnable]
    if unknown:
        sys.exit(f"unknown route(s) {unknown}. known: {', '.join(ROUTES)}"
                 f" · parked: {', '.join(PARKED_ROUTES)}")
    if not pathlib.Path(BUILD).exists():
        sys.exit(f"no build at {BUILD} — run package_from_toml first")

    rep = Report("walks — one route per slice, asserting on state")
    with open_game(BUILD, headless=not headed) as (page, errors):
        for name in wanted:
            rep.note(f"── {name}")
            start(page, "Monday", 12, "her_room")
            try:
                runnable[name](page, rep)
            except Exception as exc:                      # a broken route is a red
                rep.check(f"{name} ran to the end", False, f"{type(exc).__name__}: {exc}")
        rep.check("no uncaught page errors", not errors, "; ".join(errors[:2]))
    return rep.done()


if __name__ == "__main__":
    sys.exit(main())
