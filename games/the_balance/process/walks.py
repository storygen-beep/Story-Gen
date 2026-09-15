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
    apply_effect, Report,
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
    # Whether the way home is OFFERED is the whole safety net, so this one asks
    # the rendered links — play() alone would prove the canvas exists, not that a
    # player could ever reach it.
    goto(page, "Location_the_quad")
    rep.check("the way home is offered on the quad",
              any("bus home" in l.lower() for l in links(page)), str(links(page))[:120])
    rep.check("the way home opens", play(page, "bus_back_quad") is True)
    click(page, "Walk it")
    rep.check("broke, she can still get home",
              sv(page)["player"]["current_location"] == "the_street",
              f'{sv(page)["player"]["current_location"]} · {passage(page)}')

    # --- and the fare still bites when she has it ----------------------------
    start(page, "Monday", 9, "the_bus_stop")
    apply_effect(page, "cash", "set", 10, clamp=False)
    apply_effect(page, "quiet_week", "set", 7, clamp=False)
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
    # gates.py G21 and will be reworded again. Two paid choices grey out, the two
    # walks and the way out stay live.
    apply_effect(page, "cash", "set", 0, clamp=False)
    play(page, "catch_the_bus")
    rep.check("broke, the fare greys out instead of vanishing",
              len(locked(page)) == 2, f"{len(locked(page))} locked: {str(locked(page))[:90]}")
    rep.check("broke, the free routes stay live",
              len(links(page)) == 3, f"{len(links(page))} live: {str(links(page))[:90]}")


ROUTES = {
    "opening": walk_opening,
    "shift": walk_shift,
    "friday": walk_friday,
    "stream": walk_stream,
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
