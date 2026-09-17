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


def start(page, day="Monday", hour=12, where="her_room"):
    """Put her somewhere at a time, past the opening, ready to act."""
    apply_flag(page, "opening_done", "set")
    set_time(page, day, hour)
    stand_at(page, where)


# ── the routes ───────────────────────────────────────────────────────────────

def walk_opening(page, rep):
    """Slice 1 — the three opening screens, the chore, and the job."""
    # ⚠️ The opening canvas is emitted with the StartingCanvas prefix (v2.py:700),
    # which play() cannot build — it hardcodes "Canvas_" (playtest.py:265).
    goto(page, "StartingCanvas_canvas_opening_Node_wake")
    rep.check("the opening canvas is reachable",
              "canvas_opening" in passage(page), passage(page))

    # Read the purse BEFORE entering: the chore pays on node ENTRY, so a probe that
    # reads it after landing sees the payment already made and calls it a no-op.
    before = cash(page)
    goto(page, "StartingCanvas_canvas_opening_Node_chore")
    rep.check("the chore pays", cash(page) > before, f"cash {before} -> {cash(page)}")

    # has_job is set by a flagEffect on the LAST exit of the chain, not by landing
    # on the `hired` node. Walk it.
    play(page, "canvas_ask_owen")
    click(page, "Ask about the card in the window")
    click(page, "Take it")
    click(page, "Back out to the floor")
    rep.check("finishing the ask sets has_job", flags(page).get("has_job") is True,
              f"has_job = {flags(page).get('has_job')}")


def walk_shift(page, rep):
    """Slice 2 — the cafe is the first repeatable surface, and it pays."""
    start(page, "Tuesday", 18, "the_cafe")
    before, worked = cash(page), traits(page).get("shifts_worked") or 0
    rep.check("the floor shift opens", play(page, "shift_floor") is True)
    click(page, "Clock off")
    rep.check("the shift pays", cash(page) > before, f"cash {before} -> {cash(page)}")
    rep.check("the shift is counted",
              (traits(page).get("shifts_worked") or 0) > worked,
              f"shifts_worked {worked} -> {traits(page).get('shifts_worked')}")
    rep.check("the counter is its own surface", play(page, "shift_counter") is True)


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
    """Slice 7 — the dares are a chain, and two is shut until one is done."""
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
    """Slice 9 — Cara's thread gets shorter, and that is the mechanic."""
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


def walk_travel(page, rep):
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

    ⚠️ quiet_week SILENCES THE AMBIENTS ON PURPOSE. A random canvas taking the
    screen on arrival is the documented cause of three false failures in this
    file (see the module docstring), so this route removes the dice and asks
    `current_location` — state — whether she moved.
    """
    # --- broke, in the deepest room on campus --------------------------------
    start(page, "Monday", 11, "the_lecture_hall")
    apply_effect(page, "cash", "set", 0, clamp=False)
    apply_effect(page, "quiet_week", "set", 7, clamp=False)
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
    apply_effect(page, "quiet_week", "set", 7, clamp=False)
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


def walk_lock(page, rep):
    """Slice 11 — her own door, and the fact that it is now the gate on going live.

    ⚠️ THIS ROUTE EXISTS BECAUSE `walk_stream` CANNOT COVER IT. That route reaches
    the scene with play(), which is Engine.play() on the canvas passage and skips
    trigger conditions entirely (playtest.py:245). It proves the scene works and
    says nothing at all about whether the door is shut. From 2026-09-17 the door IS
    the gate, so the gate needs a route that goes the way a player goes.
    """
    # 14:00 Monday — inside the window the stream used to be scheduled for, and the
    # house is empty. If the schedules were still there this would pass on the clock.
    start(page, "Monday", 14, "her_room")
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
    rep.check("an empty house costs her nothing to shut it out",
              (traits(page).get("door_noticed") or 0) == 0,
              f"door_noticed = {traits(page).get('door_noticed')}")

    # The same act with somebody in. @nate is in his room 15:00-18:00 now, which is
    # the row that made the old schedule-gated stream wrong in the first place.
    start(page, "Monday", 16, "her_room")
    apply_flag(page, "door_locked", "unset")
    rep.check("at four he is home", npc_at(page, "npc_nate") == "nate_room",
              str(npc_at(page, "npc_nate")))
    play(page, "her_door")
    rep.check("with him in, still exactly one way to shut it",
              sum(1 for x in links(page) if "Shut the door" in x) == 1,
              str(links(page))[:110])
    click(page, "Shut the door")
    rep.check("shutting it on a full house is counted",
              (traits(page).get("door_noticed") or 0) == 1,
              f"door_noticed = {traits(page).get('door_noticed')}")

    rep.check("shut, the door offers the way back open",
              any("Open it again" in x for x in links(page)), str(links(page))[:110])
    click(page, "Open it again")
    rep.check("opening it clears the flag", not flags(page).get("door_locked"),
              f"door_locked = {flags(page).get('door_locked')}")
    rep.check("the tally does NOT come back down",
              (traits(page).get("door_noticed") or 0) == 1,
              f"door_noticed = {traits(page).get('door_noticed')}")

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

    # Ward nights: he is at that table and dinner does not fire.
    start(page, "Monday", 19, "the_kitchen")
    rep.check("on a ward night he is still at the table",
              npc_at(page, "npc_nate") == "the_kitchen", str(npc_at(page, "npc_nate")))
    play(page, "kitchen_nate")
    rep.check("and he has something behind him there", "kitchen_nate" in passage(page),
              passage(page))


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


ROUTES = {
    "opening": walk_opening,
    "shift": walk_shift,
    "friday": walk_friday,
    "stream": walk_stream,
    "lock": walk_lock,
    "afternoon": walk_afternoon,
    "bathroom": walk_bathroom,
    "ambients": walk_ambients,
    "doors": walk_doors,
    "class": walk_class,
    "crowd": walk_crowd,
    "house": walk_house,
    "phone": walk_phone,
    "travel": walk_travel,
}


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    headed = "--headed" in sys.argv
    wanted = args or list(ROUTES)
    unknown = [w for w in wanted if w not in ROUTES]
    if unknown:
        sys.exit(f"unknown route(s) {unknown}. known: {', '.join(ROUTES)}")
    if not pathlib.Path(BUILD).exists():
        sys.exit(f"no build at {BUILD} — run package_from_toml first")

    rep = Report("walks — one route per slice, asserting on state")
    with open_game(BUILD, headless=not headed) as (page, errors):
        for name in wanted:
            rep.note(f"── {name}")
            start(page, "Monday", 12, "her_room")
            try:
                ROUTES[name](page, rep)
            except Exception as exc:                      # a broken route is a red
                rep.check(f"{name} ran to the end", False, f"{type(exc).__name__}: {exc}")
        rep.check("no uncaught page errors", not errors, "; ".join(errors[:2]))
    return rep.done()


if __name__ == "__main__":
    sys.exit(main())
