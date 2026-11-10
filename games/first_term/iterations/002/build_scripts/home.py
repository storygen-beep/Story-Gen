"""Life at home, alone: every house room's own rows, the master bedroom at night, the random
events at home. Iteration 002, part 2. Replaces the house half of 3_activities.toml (0.1's piece 1).

Sources: sheets/systems/home_life.md, sheets/places/home_*.md (signed 2026-10-09).
The items with a person are choices inside that person's hub (laura.py, mark.py, ryan.py, via
home_items.item); an item here is the ALONE version, shown only while nobody is in the room.
Sweep fixes folded in: A1-03 (the shower strips her), A1-04/05/06 (clothes named by slot, not by
exposure), A1-13 (the debt named only after knows_mark_debt), A1-14 (Ryan's music only when he's
in), A1-16 (the couch sees who's there), A1-21, A1-22 (the step by the clock), A1-23 (the step's
way back is the hall), A1-25 (the bed's closed line), A1-31 (the room at night names only who is
there). Removed: room_feed and room_selfie (the phone owns them, wardrobe.md "On the phone"),
hall_home_late (LO, 2026-10-09, Q75).
"""
from canv import *
from tomlw import tod, wd
from home_items import *
from sheetbeats import beat   # (DECISIONS 124) the door crack reads its low-Want screens from its sheet

out = []
L, M, R = "npc_laura", "npc_mark", "npc_ryan"
ALL = [0, 1, 2, 3, 4, 5, 6]


def slot(s, on=True):
    return {"type": "clothing_slot", "slot": s, "operator": "equipped" if on else "unequipped"}


TOWEL = {"type": "worn_type", "operator": "eq", "value": "towel"}
NOT_TOWEL = {"type": "worn_type", "operator": "neq", "value": "towel"}
SLEEP_SHIRT = {"type": "worn_type", "operator": "eq", "value": "sleep_shirt"}
SKIRT = {"type": "worn_type", "operator": "eq", "value": "short_skirt"}
NAKED = [slot("top", False), slot("bottom", False), slot("dress", False), slot("bra", False), slot("underwear", False)]
UNDIES = [slot("bra"), slot("underwear"), slot("top", False), slot("bottom", False), slot("dress", False)]
LACE_SET = [{"type": "clothing_item", "item_id": "lace_bra", "operator": "equipped"}, {"type": "clothing_item", "item_id": "lace_panties", "operator": "equipped"}]   # DECISIONS 208
COVERED = [{"type": "worn_exposure", "operator": "eq", "value": 0}]
ANY = [{"type": "worn_exposure", "operator": "gte", "value": 0}]          # always true: the chain's else


def solo(cid, name, desc, loc, nodes, sched=None, conds=(), prio=3, max_day=None, metadata=None):
    t = {"location": loc, "is_repeatable": True, "priority": prio, "is_active": True}
    if max_day:
        t["max_triggers_per_day"] = max_day
    if conds:
        t["conditions"] = cond(*conds)
    if sched:
        t["schedules"] = sched
    if metadata:
        # S5 (skill, 2026-11-03): show_when_blocked and cooldown_message are trigger keys; under
        # [canvases.trigger.metadata] the importer drops them (the-clock.md), so they go on the trigger itself
        t.update(metadata)
    return {"id": cid, "name": name, "description": desc, "trigger": t, "nodes": nodes}


def S(days, a, b):
    return [{"weekdays": days, "start_time": a, "end_time": b}]


def her_thought_bands(meter, bounded, top):
    """Her thought by her band: `bounded` is [(upper bound, line)], `top` the line above them. One if/elseif chain, so
    the blocks on either side of it must not be groups. Only the bands the scene can reach get a line."""
    return [GC(cond(trait(meter, "lt", hi)), T(t)) for hi, t in bounded] + [GC(cond(*ANY), T(top))]


# ═════════════════════════════════════════════════════════════════════════════
# HER ROOM (home_ella_room.md): sleep, nap, study, make-up, tidy
# ═════════════════════════════════════════════════════════════════════════════
LATE_CLEAR = [funset(f) for f in ("came_home_late", "late_party", "late_shift", "late_date")]
SLEEP_EFF = [setv("energy", 100)]
buckets = [("19:00", "20:00", 690), ("20:00", "21:00", 630), ("21:00", "22:00", 570), ("22:00", "23:00", 510),
           ("23:00", "00:00", 450), ("00:00", "01:00", 390), ("01:00", "02:00", 330), ("02:00", "03:00", 270),
           ("03:00", "04:00", 210), ("04:00", "05:00", 150), ("05:00", "06:00", 90), ("06:00", "07:00", 30)]
out.append(solo("room_sleep", "Go to bed",
    "Her bed: energy back to full, the clock to about 07:00, and every late flag cleared (home_ella_room.md:30, Q69).",
    "home_ella_room", [
        node("bed", "Your bed", [
            POOL(P("You get under the covers. The sheets are cold for a second, but only a second, and then your body goes heavy all at once."),
                 P("You lie on your back in the dark with your phone on your chest until the screen goes black on its own. The house ticks around you. You meant to think about tomorrow, but you let yourself sink."),
                 P("You curl onto your side with the duvet up to your ear and listen to the house settle. You're asleep before you've decided to be.")),
            G(cond(here(R, "home_ryan_room"), tod("19:00", "00:00")), P("Through the wall, Ryan's music thumps low.")),
            G(cond(trait("energy", "lt", 30)), P("Your legs ache. Your eyes sting. You were running on nothing, and you know it now that you've stopped.")),
        ], [go("Sleep till morning.", node="wake", mins=m, cond_=cond(tod(a, b)), eff=SLEEP_EFF, flags=LATE_CLEAR)
            for a, b, m in buckets] + [go("Not yet. Get up.", loc="home_hall")]),
        node("wake", "Morning", [
            G(cond(flag("heavy_night")), P("You wake with your head pounding and your mouth like sand. The light through the curtains is an insult. You lie there a long time before you can face standing up.")),
            G(cond(flag("heavy_night", False)), P("Morning. You stretch until your toes crack and lie there a minute, warm, listening to the house wake up around you.")),
        ], [go("Get up.", loc="home_ella_room", cond_=cond(flag("heavy_night", False))),
            go("Get up, slowly.", loc="home_ella_room", cond_=cond(flag("heavy_night")),
               eff=[add("energy", -30) | {"clamp": True}], flags=[funset("heavy_night")])]),   # clamp: energy floors at 0
    ], sched=S(ALL, "19:00", "07:00"), prio=5,
    metadata={"show_when_blocked": True, "cooldown_message": "Every day, 7 PM-7 AM",   # pass 3 H31: the hours, a bare phrase (C5)
              # Q2 (LO, 2026-11-04): Ryan's step 5 is her in bed on a Friday night, so it opens from going to bed,
              # not on entry, and her room's wardrobe link always shows
              "substitutions": [on_activity("ryan_05_thin_walls", flag("opening_done"))]}))

out.append(solo("room_nap", "Take a nap", "A daytime nap: two hours, energy +30. Once a day.", "home_ella_room", [
    node("nap", "A nap", [
        POOL(P("You lie down on top of the covers, one arm over your eyes. The light through the curtains goes orange behind your eyelids, and then it's gone."),
             P("You fall face-first into the pillow. Outside, a car door shuts, but you don't hear the next one.")),
    # pass 3 H28: the button reads "Sleep (2h)." (canv.with_duration)
    ], [go("Sleep.", loc="home_ella_room", mins=120, eff=[{"targetType": "player", "trait": "energy", "op": "add", "value": 30, "cap": 100}]),
        go("Get up again.", loc="home_hall")]),
], sched=S(ALL, "07:00", "19:00"), prio=4, max_day=1))

SUBJECTS = [("grade_psych", "Psychology"), ("grade_business", "Business"), ("grade_bio", "Biology"), ("grade_art", "Figure drawing")]
out += brake_canvas(solo("room_study", "Study at your desk",
    "Study at the desk: 60 min, energy −10, one subject's grade +1 (home_ella_room.md:32). Alone, plain.",
    "home_ella_room", [
        node("desk", "Your desk", [
            P("You clear a space on the desk, push the clothes off the chair and open your notes. It's dull, but the exams read it."),
        ], [go(f"{name}.", node="studied", mins=60, flags=[fset("studied_home")],
               eff=[add("energy", -10), {"targetType": "player", "trait": key, "op": "add", "value": 1, "cap": 100}],
               costs=[{"trait": "energy", "value": 10}]) for key, name in SUBJECTS] + [go("Not now.", loc="home_hall")]),
        node("studied", "An hour", [
            POOL(P("An hour of it. Your eyes hurt, but some of it went in."),
                 P("You read the same page three times, then a fourth, and on the fourth it makes sense.")),
        ], [go("Close the books.", loc="home_ella_room")]),
    ]), "studied_home")

out += brake_canvas(solo("room_makeup", "Do your make-up and hair",
    "Make-up and hair at her mirror: 15 min, made_up set; Laura reads it for 10 hours (home_ella_room.md:33).",
    "home_ella_room", [
        node("mirror", "Your mirror", [
            P("You sit at your mirror with your make-up bag tipped out and do your face properly: skin, eyes, lips. Then your hair, until it falls the way you want."),
            G(cond(trait("exhibitionism", "gte", 20)), P("Darker on the eyes than you'd wear for class. You know exactly who you're doing it for: anybody who looks.")),
        ], [go("Done.", loc="home_ella_room", mins=15, flags=[fset("made_up"), fset("made_up_today")]), go("Not now.", loc="home_hall")]),
    ], prio=3), "made_up_today")

out.append(solo("room_tidy", "Tidy your room",
    "30 min, energy −5, room_tidy set; Laura reads it at Sunday dinner and clears it (home_ella_room.md:41).",
    "home_ella_room", [
        node("tidy", "Your room", [
            P("Clothes off the floor and into the basket, the bed made, the mugs carried down, the desk you can see again. It takes half an hour, but it looks like somebody's room again instead of a floordrobe."),
        ], [go("Done.", loc="home_ella_room", mins=30, eff=[add("energy", -5)], flags=[fset("room_tidy")],
               costs=[{"trait": "energy", "value": 5}]),
            go("Not now.", loc="home_hall")]),
    ], conds=[flag("room_tidy", False)], prio=2))

# ═════════════════════════════════════════════════════════════════════════════
# THE BATHROOM (home_bathroom.md): the shower strips her (A1-03), the mirror by slot (A1-05)
# ═════════════════════════════════════════════════════════════════════════════
STRIP = [REMEMBER] + [{"action": "unequip", "item_id": g} for g in ALL_GARMENTS if g not in ("sneakers", "towel")]
out.append(solo("bathroom_shower", "Take a shower",
    "Hygiene +50, 20 minutes, once a day. Who's near reads who is home. Not while Ryan or Laura has the room.",
    "home_bathroom", [
        node("shower", "The shower", [
            # C4 (DECISIONS 147): while `shower_unlocked` is set she left the lock off, and every line about the lock says so
            GC(cond(flag("shower_unlocked", False)), P("You lock the door, but the lock sticks halfway like always. You strip and step under the water while it's still cold. You gasp. Then it runs hot down your back and over your tits, and you stand there with your eyes shut and your hands flat on the tiles.")),
            GC(cond(flag("shower_unlocked")), P("You don't touch the lock. You left it off last time, and you leave it off now. You strip and step under the water while it's still cold. You gasp. Then it runs hot down your back and over your tits, and you stand there with your eyes shut and your hands flat on the tiles. Anybody could open that door.")),
            # DECISIONS 124: a weekday shower started 06:25-06:45 runs into Ryan's 06:45 row: he bangs on the door
            G(cond(flag("shower_unlocked", False), here(R, "home_ryan_room"), wd(5, 6), ntrait(R, "want", "lt", 40)), P("Ryan's door opens across the hall. The bathroom handle turns, and the sticky lock gives an inch before it catches. You open your eyes. Through the gap Ryan is looking at you, naked and wet, your tits bare under the water. He looks at the floor and turns side-on, one hand in front of his shorts."), D(R, "Sorry. Shit. I thought it was empty."), ME("Ryan! Shut the door!"), D(R, "Sorry."), P("He doesn't move away from the door for a long second.")),
            G(cond(flag("shower_unlocked"), here(R, "home_ryan_room"), wd(5, 6), ntrait(R, "want", "lt", 40)), P("Ryan's door opens across the hall. The bathroom handle turns, and the door swings open a hand's width. Nothing stops it. You open your eyes. Through the gap Ryan is looking at you, naked and wet, your tits bare under the water. He looks at the floor and turns side-on, one hand in front of his shorts."), D(R, "Sorry. Shit. I thought it was empty."), ME("Ryan! Shut the door!"), D(R, "Sorry."), P("He doesn't shut it for a long second.")),
            # false lines a3 #1 (DECISIONS 129): at want 40 the peek itself has him keep looking; no "This time" after "He looks at the floor"
            G(cond(flag("shower_unlocked", False), here(R, "home_ryan_room"), wd(5, 6), ntrait(R, "want", "gte", 40)), P("Ryan's door opens across the hall. The bathroom handle turns, and the sticky lock gives an inch before it catches. You open your eyes. Through the gap Ryan is looking at you, naked and wet, your tits bare under the water. He doesn't look at the floor. He turns side-on, one hand in front of his shorts, and keeps looking."), ME("Ryan! Do you mind?"), D(R, "Not really. Sorry."), P("He doesn't sound sorry. He doesn't look away until the door clicks shut.")),
            G(cond(flag("shower_unlocked"), here(R, "home_ryan_room"), wd(5, 6), ntrait(R, "want", "gte", 40)), P("Ryan's door opens across the hall. The bathroom handle turns, and the door swings open a hand's width. Nothing stops it. You open your eyes. Through the gap Ryan is looking at you, naked and wet, your tits bare under the water. He doesn't look at the floor. He turns side-on, one hand in front of his shorts, and keeps looking."), ME("Ryan! Do you mind?"), D(R, "Not really. Sorry."), P("He doesn't sound sorry. He doesn't look away until he pulls the door to.")),
            G(cond(flag("shower_unlocked", False), here(R, "home_ryan_room"), wd(0, 1, 2, 3, 4), tod("06:45", "06:25"), ntrait(R, "want", "lt", 40)), P("Ryan's door opens across the hall. The bathroom handle turns, and the sticky lock gives an inch before it catches. You open your eyes. Through the gap Ryan is looking at you, naked and wet, your tits bare under the water. He looks at the floor and turns side-on, one hand in front of his shorts."), D(R, "Sorry. Shit. I thought it was empty."), ME("Ryan! Shut the door!"), D(R, "Sorry."), P("He doesn't move away from the door for a long second.")),
            G(cond(flag("shower_unlocked"), here(R, "home_ryan_room"), wd(0, 1, 2, 3, 4), tod("06:45", "06:25"), ntrait(R, "want", "lt", 40)), P("Ryan's door opens across the hall. The bathroom handle turns, and the door swings open a hand's width. Nothing stops it. You open your eyes. Through the gap Ryan is looking at you, naked and wet, your tits bare under the water. He looks at the floor and turns side-on, one hand in front of his shorts."), D(R, "Sorry. Shit. I thought it was empty."), ME("Ryan! Shut the door!"), D(R, "Sorry."), P("He doesn't shut it for a long second.")),
            G(cond(flag("shower_unlocked", False), here(R, "home_ryan_room"), wd(0, 1, 2, 3, 4), tod("06:45", "06:25"), ntrait(R, "want", "gte", 40)), P("Ryan's door opens across the hall. The bathroom handle turns, and the sticky lock gives an inch before it catches. You open your eyes. Through the gap Ryan is looking at you, naked and wet, your tits bare under the water. He doesn't look at the floor. He turns side-on, one hand in front of his shorts, and keeps looking."), ME("Ryan! Do you mind?"), D(R, "Not really. Sorry."), P("He doesn't sound sorry. He doesn't look away until the door clicks shut.")),
            G(cond(flag("shower_unlocked"), here(R, "home_ryan_room"), wd(0, 1, 2, 3, 4), tod("06:45", "06:25"), ntrait(R, "want", "gte", 40)), P("Ryan's door opens across the hall. The bathroom handle turns, and the door swings open a hand's width. Nothing stops it. You open your eyes. Through the gap Ryan is looking at you, naked and wet, your tits bare under the water. He doesn't look at the floor. He turns side-on, one hand in front of his shorts, and keeps looking."), ME("Ryan! Do you mind?"), D(R, "Not really. Sorry."), P("He doesn't sound sorry. He doesn't look away until he pulls the door to.")),
            G(cond(wd(0, 1, 2, 3, 4), tod("06:25", "06:45")), P("The door shakes in its frame. Ryan, banging."), D(R, "Some of us have work, @player.nickname! Out!")),
            G(cond(here(M, "home_kitchen")), P("From the kitchen, Mark shouts down the hall."), D(M, "That's my hot water you're burning, @player! Five minutes!"), P("The pipes knock, but you turn it up hotter.")),
            G(cond(here(L, "home_kitchen")), P("Laura's voice comes down the hall from the kitchen. \"Leave some hot water, sweetheart!\"")),
            POOL(P("You soap yourself slowly, all of you. The lock's no use, and you take your time like someone could walk in. The steam fogs the glass until the room is white."),
                 P("You tip your head back and let the water fill your mouth. It runs off your chin, down between your tits. You should be quick, but you stay until your fingertips wrinkle."),
                 P("You wash your hair twice because it feels good. The water drums on your shoulders, and you stay under it longer than you should.")),
        ], [go("Wrap up in a towel.", loc="home_bathroom", mins=20,
               cond_=cond(tod("06:45", "06:25")),
               eff=[{"targetType": "player", "trait": "hygiene", "op": "add", "value": 50, "cap": 100}],
               wardrobe=STRIP + [{"action": "equip", "item_id": "towel"}]),
            go("Wrap up in a towel.", loc="home_bathroom", mins=20,
               cond_=cond(wd(5, 6), tod("06:25", "06:45")),
               eff=[{"targetType": "player", "trait": "hygiene", "op": "add", "value": 50, "cap": 100}],
               wardrobe=STRIP + [{"action": "equip", "item_id": "towel"}]),
            go("Wrap up and get out.", loc="home_hall", mins=20,
               cond_=cond(wd(0, 1, 2, 3, 4), tod("06:25", "06:45")),
               eff=[{"targetType": "player", "trait": "hygiene", "op": "add", "value": 50, "cap": 100}],
               wardrobe=STRIP + [{"action": "equip", "item_id": "towel"}]),
            # C4 (DECISIONS 147): Exhibitionism 5, +1 cap 19; the shower is once a day, so is the pay. The door stays
            # unlocked (`shower_unlocked`) until "Lock it again."; while it is, the walk-ins here roll 0.5 (walkins.py B1).
            # pass 3 D44 (the-surfaces.md R9): leaving the lock off ends on a screen of her body, not a toast
            go("Leave the door unlocked.", node="unlocked", mins=20, swl=True, cond_=cond(trait("exhibitionism", "gte", 5)),
               eff=[{"targetType": "player", "trait": "hygiene", "op": "add", "value": 50, "cap": 100},
                    {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 19}],
               flags=[fset("shower_unlocked")], wardrobe=STRIP + [{"action": "equip", "item_id": "towel"}]),
            go("Lock it again.", loc="home_hall", mins=20, cond_=cond(flag("shower_unlocked")),
               eff=[{"targetType": "player", "trait": "hygiene", "op": "add", "value": 50, "cap": 100}],
               flags=[funset("shower_unlocked")], wardrobe=STRIP + [{"action": "equip", "item_id": "towel"}]),
            go("\"Five minutes.\"", loc="home_hall", mins=30,
               cond_=cond(wd(0, 1, 2, 3, 4), tod("06:25", "06:45")),
               eff=[{"targetType": "player", "trait": "hygiene", "op": "add", "value": 50, "cap": 100}, npc_add(R, "warmth", -1)],
               wardrobe=STRIP + [{"action": "equip", "item_id": "towel"}])]),
        node("unlocked", "The lock off", [
            P("You towel off with the lock off and the door open a crack, your nipples hard in the draft from the hall. Anybody coming down the hall gets the lot, and you take your time drying between your legs."),
        ], [go("Go out in the towel.", loc="home_hall")]),
    ], conds=[here(R, "home_bathroom", False), here(L, "home_bathroom", False)], prio=5, max_day=1))

out.append(solo("bathroom_mirror", "Look in the mirror", "The bathroom mirror: one line by what she has on, slot by slot.",
    "home_bathroom", [
        node("mirror", "The mirror", [
            GC(cond(TOWEL), P("Wet hair, pink skin, the towel tucked over your tits, stopping at the top of your thighs. One tug and it's on the floor. You look at the girl in the mirror. She looks right back.")),
            GC(cond(*NAKED), P("Naked. You turn sideways, then the other way. You cup your tits and let them go. The mirror is small, so you stand on your toes to see the rest of you.")),
            # more clothes, round 2 (DECISIONS 208): the lace set she bought for herself
            GC(cond(*UNDIES, *LACE_SET), P("The black lace set. Your nipples show dark through the lace, and at the back it's a string and nothing else. You bought it for nobody. You turn round to look at your bare ass in it, and think about who you'd let see it.")),
            GC(cond(*UNDIES), P("Bra and panties, and the door doesn't lock properly. You look at yourself the way someone walking in would.")),
            GC(cond(*COVERED), P("Dressed. You fix your hair, check your teeth, smooth yourself down.")),
            GC(cond(*ANY), P("Half dressed, half not. You look at what's missing first, the way anyone walking in would.")),
        ], [go("Done.", loc="home_hall")]),
    ], prio=2))

# ═════════════════════════════════════════════════════════════════════════════
# THE HALL (home_hall.md): the mirror by the coats
# ═════════════════════════════════════════════════════════════════════════════
out.append(solo("hall_mirror", "Check your clothes in the hall mirror", "One line by what she has on. Writes nothing.",
    "home_hall", [
        node("mirror", "The hall mirror", [
            GC(cond(TOWEL), P("A towel, in the hall, where anyone can come out of any door. Your heart beats in your throat.")),
            GC(cond(*NAKED), P("Naked in the hall. Every door off it could open.")),
            GC(cond(*UNDIES, *LACE_SET), P("The black lace set, in the hall, your nipples dark through the lace and your ass bare round the string. Any door off it could open, and you're not sure you'd mind.")),
            GC(cond(*UNDIES), P("Bra and panties in the hall, where every door off it could open.")),
            GC(cond(SKIRT, slot("underwear", False)), P("Nothing under the skirt, and the hall is right there. Bend for anything out there, and anyone behind you gets everything.")),
            GC(cond(SKIRT, slot("underwear")), P("The skirt is short enough that the hall is a problem. Bend for anything out there, and anyone behind you gets your panties. You tug it down, but it doesn't help.")),
            # reader pass 4 b1: worn_exposure is 0 with a top or a bottom missing, so half-dressed says so before "covered"
            GC(cond(slot("top", False), slot("dress", False), slot("bottom"), slot("bra")), P("No top, just your bra, in the hall where every door off it could open.")),
            GC(cond(slot("top", False), slot("dress", False), slot("bottom"), slot("bra", False)), P("Topless in the hall. Your bare tits are out, and every door off it could open.")),
            GC(cond(slot("bottom", False), slot("dress", False), slot("top"), slot("underwear")), P("A top and your panties and nothing else, in the hall where every door off it could open.")),
            GC(cond(slot("bottom", False), slot("dress", False), slot("top"), slot("underwear", False)), P("A top and nothing under it. Your bare ass is out in the hall, where every door off it could open.")),
            # Iteration 002, part 8 (reader): the top only when there is one; "Laura would approve" only in plain clothes.
            GC(cond(slot("bra", False), slot("top"), *COVERED), P("No bra. Your nipples show through your top, plain as anything in the hall light.")),
            GC(cond(slot("bra", False), slot("dress"), *COVERED), P("No bra under it. Your nipples show through the fabric, plain as anything in the hall light.")),
            GC(cond(*COVERED, {"type": "worn_corruption", "operator": "eq", "value": 0}, {"type": "worn_type", "operator": "neq", "value": "thin_top"}),
               P("Covered, neat, nothing anyone could say a word about. Laura would approve.")),
            # scene reader b03 (2026-11-03): the blue dress is Laura's own, so "nothing Laura would have bought you" can't be its line
            GC(cond(*COVERED, {"type": "clothing_item", "item_id": "laura_blue_dress", "operator": "equipped"}),
               P("Laura's blue dress, and it's tighter on your tits and your ass than it ever was on her. Covered, technically.")),
            GC(cond(*COVERED), P("Covered, technically. Nothing Laura would have bought you.")),
            GC(cond(*ANY), P("Half dressed in the hall. You check the doors before you check the mirror.")),
        ], [go("Go on.", loc="home_hall", mins=2)]),
    ], prio=2))

# ═════════════════════════════════════════════════════════════════════════════
# THE KITCHEN (home_kitchen.md): the drawer (A1-13), and the meals alone
# ═════════════════════════════════════════════════════════════════════════════
out.append(solo("kitchen_drawer", "Look through the drawer", "Reads rent_short, knows_mark_debt and the letter home. Writes nothing.",
    "home_kitchen", [
        node("drawer", "The drawer", [
            P("The drawer by the fridge sticks, and you have to lift it to open it. Takeaway menus, dead batteries, a roll of tape, and under all of it the letters nobody wants to open."),
            G(cond(flag("rent_short")), P("On top, a new one. Vance's handwriting on the envelope, already torn open. Inside, one line: OUTSTANDING, and a figure, underlined twice. Your short week is in that number.")),
            G(cond(flag("rent_short", False), flag("knows_mark_debt", False)), P("Bills. Gas, water, the council, a phone contract in Mark's name. Two of them say FINAL in red, but nobody's opened those.")),
            G(cond(flag("rent_short", False), flag("knows_mark_debt")), P("Three envelopes from Vance, all opened, all folded back the way they came. The top one says FINAL in red. Now you know what they're about: Mark owes him more than the rent, a lot more.")),
            G(cond(flag("letter_home"), since("letter_home", "gte", 24)), P("And one from the college, with your name on it, opened. Laura's read it. The dean's signature is at the bottom.")),
        ], [go("Shut the drawer.", loc="home_hall", mins=5)]),
    ], prio=2))

KITCHEN_EMPTY = [nobody("home_kitchen")]
out += brake_canvas(solo("kitchen_breakfast", "Make breakfast",
    "Breakfast alone: 15 min, energy +10 (home_life.md:63). With Laura or Mark it is in their hub.",
    "home_kitchen", [node("eat", "Breakfast", [
        POOL(P("Toast at the counter, standing up, crumbs in the sink. The kitchen's yours, and somebody left the radio on."),
             P("Cereal, the last of the milk, the radio on low for company.")),
    ], [go("Eat.", loc="home_kitchen", mins=15, flags=[fset("ate_breakfast")],
           eff=[{"targetType": "player", "trait": "energy", "op": "add", "value": 10, "cap": 100}]),
        go("Not hungry.", loc="home_hall")])],
    sched=S(ALL, "06:30", "10:00"), conds=KITCHEN_EMPTY), "ate_breakfast")

out += brake_canvas(solo("kitchen_coffee", "Make a coffee",
    "A coffee alone: 10 min, energy +5 (home_life.md:67).",
    "home_kitchen", [node("coffee", "Coffee", [
        P("The kettle, the jar, two sugars. You drink it at the window and watch the street go by. It's too hot, but you drink it anyway."),
    ], [go("Drink it.", loc="home_kitchen", mins=10, flags=[fset("had_coffee")],
           eff=[{"targetType": "player", "trait": "energy", "op": "add", "value": 5, "cap": 100}]),
        go("Leave it.", loc="home_hall")])],
    sched=S(ALL, "06:30", "11:00"), conds=KITCHEN_EMPTY), "had_coffee")

out += brake_canvas(solo("kitchen_dinner", "Eat dinner",
    "Dinner alone: 30 min, energy +15 (home_life.md:64). With anyone at the table it is in their hub.",
    "home_kitchen", [node("eat", "Dinner", [
        POOL(P("A plate of whatever's in the fridge, eaten at the empty table. The food's fine, but the kitchen clock is loud."),
             P("You heat up leftovers and eat them out of the pan, standing, because nobody's here to tell you not to.")),
    ], [go("Eat.", loc="home_kitchen", mins=30, flags=[fset("ate_dinner")],
           eff=[{"targetType": "player", "trait": "energy", "op": "add", "value": 15, "cap": 100}]),
        go("Not hungry.", loc="home_hall")])],
    sched=S(ALL, "18:00", "20:00"), conds=KITCHEN_EMPTY), "ate_dinner")

out += brake_canvas(solo("kitchen_dishes", "Do the dishes",
    "Dishes alone: 20 min, energy −5 (home_life.md:66).",
    "home_kitchen", [node("dishes", "The dishes", [
        P("The sink's full again. You run it hot and work through the pile, plates, the pan, somebody's mug with the teabag still in it. You hate it, but it's done in twenty minutes."),
    ], [go("Done.", loc="home_kitchen", mins=20, flags=[fset("did_dishes")], eff=[add("energy", -5)],
           costs=[{"trait": "energy", "value": 5}]),
        go("Leave them.", loc="home_hall")])],
    sched=S(ALL, "19:00", "21:00"), conds=KITCHEN_EMPTY), "did_dishes")

# ═════════════════════════════════════════════════════════════════════════════
# THE LIVING ROOM (home_living_room.md): the couch (A1-16), TV and a film alone
# ═════════════════════════════════════════════════════════════════════════════
LIVING_EMPTY = [nobody("home_living_room")]
# Who can pass through to see her: Mark from the kitchen, or Ryan coming down from his room (the
# two the lines name). One set of choices per passer, the second only when Mark isn't the one.
# reader a3 #15 (DECISIONS 131): Laura in any room of the house (the couch is empty, so not the living room)
LAURA_IN_HOUSE = [here(L, x) for x in ("home_kitchen", "home_master_bedroom", "home_hall", "home_bathroom", "home_garden", "home_ella_room", "home_ryan_room", "home_garage", "home_front_door")]
PASSERS = [[here(M, "home_kitchen"), flag("mark_saw_her")], [here(R, "home_ryan_room"), here(M, "home_kitchen", False)]]   # Mark after his accident (H2, DECISIONS 124)
out.append(solo("living_couch", "Lie on the couch",
    "Alone in the room. Who passes through reads what she has on (in her underwear they look only from Daring, Mark also after his accident; below it she covers up); exhibitionism +1 once a day if Daring, in her underwear, and someone's home to pass.",
    "home_living_room", [
        node("couch", "The couch", [
            P("You stretch out on the couch, one knee up, the remote on your stomach."),
            # LO, 2026-11-04 (the-heat-ladder.md H1, H2): what she wears at home needs Exhibitionism 20, and for Mark his accident first
            G(cond(*UNDIES, here(M, "home_kitchen")),
              GC(cond(DARING, flag("mark_saw_her")), P("Mark comes through from the kitchen with a drink and stops behind the couch. You're in your underwear, but he doesn't say cover up. He looks down the length of you, at your legs, at your ass in your panties. The drink stops halfway to his mouth."), D(M, "Comfortable, @player?"), ME("Very."), D(M, "Hm."), P("Then he goes, slowly.")),
              GC(cond(*ANY), P("The kitchen door goes, and you grab the cushion and hold it over your bra. Mark comes through with a drink and sees your bare legs and the cushion. He catches himself and looks at the blank TV."), D(M, "Put some clothes on, @player."), ME("I was just getting up."), P("He goes, and he doesn't look back."))),
            # copy fix A17 (DECISIONS 125): his look by his Want band (npc_ryan.md:205 under 40; at 40 he stops pretending)
            G(cond(*UNDIES, DARING, here(R, "home_ryan_room"), ntrait(R, "want", "lt", 40)), P("Ryan comes out of his room for a drink and stops at the end of the hall. His eyes go straight to your tits in your bra. Then they go up to the ceiling. \"Jesus, @player.nickname.\" He goes to the kitchen without looking again.")),
            G(cond(*UNDIES, DARING, here(R, "home_ryan_room"), ntrait(R, "want", "gte", 40)), P("Ryan comes out of his room for a drink and stops at the end of the hall. His eyes go down you, your tits, your panties, and come back up slow. He doesn't pretend he wasn't looking. \"Jesus, @player.nickname.\"")),
            # reader 2026-11-04: her "Get me one too" goes while he is still on his way to the kitchen, before he comes back with the can
            G(cond(*UNDIES, trait("exhibitionism", "lt", 20), here(R, "home_ryan_room")), P("Ryan's door opens down the hall, and you drag the cushion across your chest. He comes out for a drink and stops at the end of the hall. He sees your bare legs and the cushion, goes red and looks at the ceiling."), D(R, "Warn a guy, @player.nickname."), ME("It's my couch too."), P("He gets his drink with his back to you.")),
            G(cond(*UNDIES, DARING, here(R, "home_ryan_room")), ME("Get me one too, Ryan."), D(R, "Get your own. And put some clothes on."), P("He takes a long time getting that drink. On the way back down the hall he holds the can in front of his shorts.")),   # pass 3 B4
            G(cond(SKIRT), P("With your knee up, the skirt is nowhere. Anybody coming in from the hall would see straight up it.")),
            G(cond(*COVERED, {"type": "worn_type", "operator": "neq", "value": "short_skirt"}), P("Nobody looks twice at a girl on a couch in her clothes.")),
        ], [*[c for who, stay in zip(PASSERS, ("stay_mark", "stay_ryan")) for c in brake(
                go("Stay a while.", node=stay, mins=5, flags=[fset("couch_seen")],   # reader a3 #15 (DECISIONS 131): a screen, not a jump back
                   cond_=cond(DARING, *UNDIES, *who),   # a Daring act stops at Daring's top (pass 3 G8)
                   eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 39}]),
                "couch_seen")],
            go("Get up.", loc="home_hall", mins=10)]),
        # reader a3 #15 (DECISIONS 131): he answers and holds back. "Your mother" only while Laura is in the house.
        # truth pass (2026-11-03): he comes back only while his row still has him in the kitchen (the choice in
        # reads it; this screen is 5 minutes on, and his weekday kitchen row ends at 19:00), so after her own
        # line every block carries it (canv.pin_blocks). The "your mother" pair is its own chain inside a G.
        node("stay_mark", "Stay a while", [
            P("You don't cover up. You stay on your back with one knee up, in your bra and panties, for whoever comes through next."),   # reader pass 3 b01: he may be gone by now; the pinned blocks say if he comes
            *pin_blocks([
                P("Ten minutes later Mark comes back through from the kitchen, and this time he stops. He stands over you at the end of the couch with the drink. His eyes go down your tits in your bra to your panties, and stay there. The front of his jeans is tight."),
                D(M, "You're asking for it, lying there like that."),
                ME("Asking for what?"),
                G(cond(*ANY), GC(cond(*LAURA_IN_HOUSE, logic="OR"), D(M, "Not with your mother home.")),
                              GC(cond(*ANY), D(M, "Your mother'll be back."))),
                P("He goes back to the kitchen. He doesn't come back, and you lie there with your nipples hard in your bra."),
            ], here(M, "home_kitchen")),
        ], [go("Get up.", loc="home_living_room", mins=40)]),
        # truth pass (2026-11-03): as stay_mark, by Ryan's room row (he comes down from it)
        node("stay_ryan", "Stay a while", [
            P("You don't cover up. You stay on your back with one knee up, in your bra and panties, for whoever comes through next."),   # reader pass 3 b01: he may be gone by now; the pinned blocks say if he comes
          *pin_blocks([
            GC(cond(ntrait(R, "want", "lt", 40)),
               P("Ten minutes later Ryan comes out again, for nothing, and stops at the end of the hall. He looks at your tits in your bra, at your panties, and goes red to the ears, but he doesn't look away.")),
            GC(cond(*UNDIES),
               P("Ten minutes later Ryan comes out again and sits on the arm of the couch, right by your feet. His eyes go down you slow, your tits, your panties, the inside of your raised knee. His cock is hard in his shorts, and he doesn't hide it.")),
            # its own chain: adjacent GCs would join the Want chain above
            G(cond(*ANY), GC(cond(*LAURA_IN_HOUSE, logic="OR"), D(R, "Not with Mom home, @player.nickname.")),
                          GC(cond(*ANY), D(R, "Mom'll be back, @player.nickname."))),
            P("He goes back down the hall with his hand in front of his shorts."),
          ], here(R, "home_ryan_room")),
        ], [go("Get up.", loc="home_living_room", mins=40)]),
    ], conds=LIVING_EMPTY, prio=3))

# The remote (DECISIONS 85-86, living_tv_channels.md): five channels, each with its own clip. The four
# plain channels keep TV's old pay, energy +5 once a day; channel 5, the adult channel Mark pays for,
# pays every time she watches (LO, 2026-10-29), up to five TV sessions a day (LO, 2026-10-30, DECISIONS 91).
LIVING_TV_WATCH = ("Channel 5 fills the screen. A woman rides a man on a leather couch. Her tits bounce with every drop of her hips. His hands grip her ass and pull her down hard. The camera cuts low. His cock slides out of her, shiny and thick, and sinks back in to the root. She moans loud. The speakers carry it through the room. You jab the remote and the volume drops. On screen she rides him faster. He grunts and squeezes her ass. Your face goes hot. Your nipples pull tight and ache. You are wet. Your clit throbs, and you squeeze your thighs together hard.")
LIVING_TV_TOUCH = ("The adult channel is on, the sound turned low. On the screen a man is taking her from behind on a couch like yours, his hands on her hips, his cock driving in deep. Her tits swing with every thrust. She moans through the speakers, low and steady. Your hand slides down your belly and inside your clothes. Your fingers find your clit, and you are already wet. You rub in time with him, hard when he drives in, slow when he pulls out. Your other hand squeezes your tit, your thumb on the nipple. One eye stays on the doorway to the hall. Anyone could walk in. You rub faster. He slams his cock into her, and you come on the couch, biting your lip. Your hips lift off the cushion while your fingers keep working your clit through it.")
# LO 2026-11-03 ("a line or two for each of the 17 silent people"): she is alone on the couch (LIVING_EMPTY), so the
# voice is the TV's, speaker "unknown". One line per pool entry, kept with its entry in a group (a pool entry is one block).
# The adult channel holds to the strangers-on-a-screen ceiling (living_tv_channels.md: no cunt, fuck, cum, pussy).
TV_VOICE = {
    "A reporter stands in the rain outside a courthouse. Then the weather: more rain.": "And there's more rain on the way, I'm afraid.",
    "The local news: a fire on the ring road, a lost dog, the council shouting about parking.": "Police are asking drivers to stay off the ring road.",
    "A chef with huge arms folds butter into pastry and won't stop talking about it.": "Cold butter, cold hands. Never, ever warm butter.",
    "Two women race to ice a cake before the clock runs out. One of them cries.": "Thirty seconds, ladies! Hands where I can see them!",
    "Football, a match nobody in this house cares about. Two-nil.": "And that's two! Two-nil, and they've earned it!",
    "Highlights: a man runs a very long way while the commentator loses his mind.": "Look at him go! He's still going!",
    "An old black-and-white film. A woman in a fur coat slaps a man, then kisses him.": "You're a brute, Johnny. Do it again.",
    "A cop film from the nineties. Everything explodes, twice.": "Get down! It's gonna blow!",
}
_ANYWAY = {"version": "1.0", "logic": "AND", "items": []}
tv_nodes = [node("remote", "The remote", [
        P("You drop onto the couch and pick up the remote. Five channels, and one of them is the one Mark pays for."),
    ], remote_choices("ch_", "adult") + [go("Turn it off.", loc="home_hall")])]
for cid, btn, lines, desc, qs, pool in CHANNELS:
    tv_nodes.append(node(f"ch_{cid}", btn.split(": ", 1)[1].rstrip(".").capitalize(), [POOL(*[GC(_ANYWAY, P(x), WHO(TV_VOICE[x])) for x in lines]), VID(desc, *qs, pool_dir=pool)],
        [*watch_plain("home_living_room"), go("Change the channel.", node="remote"), go("Turn it off.", loc="home_hall")]))
tv_nodes += [
    node("adult", "Channel 5", [P(LIVING_TV_WATCH),
        WHO("Oh God, your cock. Harder. Don't stop."),
        VID("a couple having sex on a TV screen in a dark living room, the woman riding the man", "porn on tv screen living room", "woman riding man on tv adult channel", pool_dir="sex/tv_adult_alone_t5")],
        [go("Keep watching.", loc="home_living_room", mins=30, eff=tv_pay(1, 19), cond_=cond(TV_GG)),
         go("Keep watching.", loc="home_living_room", mins=30, eff=tv_pay(1, 39), cond_=cond(TV_CUR)),
         go("Touch yourself.", node="touch", mins=5, cond_=cond(TV_CUR)),
         # C2 (DECISIONS 147): Corruption 10, +1 cap 19; it ends the session like "Keep watching." (DECISIONS 91). The sound
         # stays up for the day (`tv_loud`, cleared at midnight), and while it is the walk-ins here roll 0.5 (walkins.py B3).
         go("Turn the sound up.", node="loud", mins=1, swl=True, cond_=cond(trait("corruption", "gte", 10))),
         go("Change the channel.", node="remote"), go("Turn it off.", loc="home_hall")]),
    node("loud", "The sound up", [
        P("You thumb the volume up, and up again. Her moans fill the living room. The slap of his hips on her ass is loud as a hand clap. You can hear it bounce off the hall walls."),
        P("Anyone in the house can hear it now. Your nipples go hard. You squeeze your thighs together on the couch and leave it right where it is."),
        WHO("Harder. Oh God, harder. Don't stop."),
        VID("a couple having sex on a TV screen, the volume bar full, a girl on a couch", "porn on tv volume up living room", "loud porn on tv girl watching", pool_dir="sex/tv_adult_loud_t5")],
        [go("Keep watching.", loc="home_living_room", mins=30, eff=tv_pay(1, 19), flags=[fset("tv_loud")])]),
    node("touch", "On the couch", [
        G(cond(here(M, "home_kitchen")), P("In the kitchen a cupboard bangs. Mark is home.")),
        G(cond(here(R, "home_ryan_room")), P("Across the hall, Ryan's music thumps through his door.")),
        P(LIVING_TV_TOUCH),
        WHO("Yes. Give me that cock. Yes."),
        VID("a girl alone on a couch touching herself while porn plays on the TV", "girl masturbating on couch watching porn on tv", "woman fingering herself couch tv porn", pool_dir="sex/tv_adult_touch_t5")],
        [go("Fix your clothes.", loc="home_living_room", mins=25, eff=tv_pay(2, 39))]),
]
out.append(solo("living_tv", "Watch TV",
    "The remote alone (DECISIONS 85-86, 91): at most five sessions a day, then the row greys out. Five channels, each with a clip. The plain four: 30 min, energy +5 once a day. Channel 5: corruption +1 every watch, cap 19 at Good Girl, 39 at Curious; touch herself at Curious, +2, cap 39.",
    "home_living_room", tv_nodes, sched=S(ALL, "07:00", "02:00"), conds=LIVING_EMPTY,
    # Five sessions a day (LO, 2026-10-30, DECISIONS 91); the row greys out after. The grey row also shows
    # when the room is busy or it's past 02:00 (v2.py renderSoloActivities), so its text must be true then too.
    max_day=5))
out[-1]["trigger"].update({"show_when_blocked": True, "cooldown_message": "Every day, 7 AM-2 AM, five times a day"})   # pass 3 H31: true on every greyed visit (busy room, cap, hours)   # trigger keys, not metadata (template_import.py:2548)

out += brake_canvas(solo("living_film", "Put a film on",
    "A film alone: 120 min, energy +5 (home_life.md:70).",
    "home_living_room", [node("film", "A film", [
        P("You pick a film nobody else in this house would sit through, pull the blanket off the back of the couch and turn the lights off. It's long, but you love it."),
    ], [go("Watch it.", loc="home_living_room", mins=120, flags=[fset("movie_night")],
           eff=[{"targetType": "player", "trait": "energy", "op": "add", "value": 5, "cap": 100}]),
        go("Not tonight.", loc="home_hall")])],
    sched=S(ALL, "19:00", "00:00"), conds=LIVING_EMPTY), "movie_night")

# ═════════════════════════════════════════════════════════════════════════════
# THE MASTER BEDROOM (home_master_bedroom.md): her wardrobe while they're out; at night,
# "Ease the door open" (world_data.py's door) lands here: one screen naming who is asleep.
# ═════════════════════════════════════════════════════════════════════════════
out.append(solo("master_wardrobe", "Go through Laura's wardrobe",
    "When both are out. Try on her things in her mirror; reads laura_blue_dress. Once a day.",
    "home_master_bedroom", [
        node("wardrobe", "Laura's wardrobe", [
            P("Laura's wardrobe smells like her perfume. Work blouses, a winter coat, and at the back, in dry-cleaner plastic, dresses she never wears. Short ones. Tight ones. A red one with no back at all."),
            G(cond({"type": "clothing_item", "item_id": "laura_blue_dress", "operator": "owned"}, {"type": "clothing_item", "item_id": "laura_blue_dress", "operator": "unequipped"}),
              P("There's the gap on the rail where the blue one hung. It's in your room now. She gave it to you like it was nothing, and there's a whole rail of nothing back here.")),
            G(cond({"type": "clothing_item", "item_id": "laura_blue_dress", "operator": "equipped"}),
              P("There's the gap on the rail where the blue one hung. You're wearing it.")),
            POOL(P("You hold the red one against yourself in her long mirror. It would barely cover your ass. Laura wore this once, somewhere, for someone, and you stand there trying to picture her face when she did."),
                 P("In the drawer under the dresses: stockings, still in the packet, and a black lace bra that is not a mom's bra. You hold it up to your chest in her mirror and your nipples go hard."),
                 P("A photo, tucked in the frame of her mirror: Laura at twenty-something on someone's shoulders at a concert, her top off, laughing. You put it back exactly where it was.")),
            P("This wardrobe isn't going anywhere, but one of these days somebody's going to walk in and catch you at it."),   # writing pass: the hook (walkin_wardrobe_laura, walkin_wardrobe_mark)
        ], [go("Put it all back.", loc="home_hall", mins=20)]),
    ], conds=[nobody("home_master_bedroom")], prio=3, max_day=1))

# Sun 00:00-01:00 Mark and Laura are awake (DECISIONS 80): no "asleep" line may show then. The engine's
# conditions do not nest, so each "asleep" line is written once per piece of the night that skips it.
ASLEEP_HOURS = [(wd(0, 1, 2, 3, 4, 5), tod("22:00", "07:00")), (wd(6), tod("22:00", "00:00")), (wd(6), tod("01:00", "07:00"))]
# Laura is awake and alone Sun-Fri 22:00-23:00 (DECISIONS 82), so a line saying she is asleep skips that hour too.
LAURA_ASLEEP_HOURS = [(wd(0, 1, 2, 3, 4), tod("23:30", "07:00")), (wd(5), tod("22:00", "07:00")), (wd(6), tod("23:30", "00:00")), (wd(6), tod("01:00", "07:00"))]   # bedtime 23:30 (LO, 2026-11-09)
out.append({"id": "master_asleep", "name": "Ease the door open",
    "description": "The door's 'Ease the door open' at night: one screen naming only who is asleep, then back to the hall (home_master_bedroom.md:47-54, Q58). Reached only by the door.",
    "trigger": {"location": "home_master_bedroom", "is_repeatable": True, "priority": 1, "is_active": True,
                "substitution_only": True},
    "nodes": [node("dark", "Their room at night", [
        P("You ease the handle down and open the door a hand's width. The room is dark and warm, and it smells of sleep."),
        *[G(cond(here(L, "home_master_bedroom"), here(M, "home_master_bedroom"), *hrs),
          P("Laura's asleep on her side, curled toward the wall, one bare shoulder out of the covers. Mark's on his back beside her, snoring.")) for hrs in LAURA_ASLEEP_HOURS],
        *[G(cond(here(L, "home_master_bedroom"), here(M, "home_master_bedroom", False), *hrs),
          P("Laura's asleep on her side, one bare shoulder out of the covers. Mark's half of the bed is empty.")) for hrs in LAURA_ASLEEP_HOURS],
        *[G(cond(here(M, "home_master_bedroom"), here(L, "home_master_bedroom", False), *hrs),
          P("Mark's asleep on his back, one arm flung across the bed. Laura's half is empty, the covers thrown back.")) for hrs in ASLEEP_HOURS],
        P("You stand in the gap long enough to hear the breathing. Nobody stirs."),
    ], [go("Close the door.", loc="home_hall", mins=2)])]})


# ═════════════════════════════════════════════════════════════════════════════
# THE WALK-INS (DECISIONS 79-80, ryan_door_ajar.md, master_door_saturday_night.md): two Good Girl
# ways up, reached only by their doors (world_data.py). The look is an event and pays nothing;
# staying is her choice and pays corruption +1, cap 19. Nobody sees her; no ladder number moves.
# Each sets its seen flag on every exit; the door reads it as the brake.
# ═════════════════════════════════════════════════════════════════════════════
RYAN_CRACK = ("Ryan's door is open a crack, and his light is on. You mean to walk past, but you look in. Ryan is on his bed with his shorts shoved down. His cock is hard in his fist, and he is stroking it slowly. His other hand presses something to his face. It is a pair of panties from the laundry basket. They are yours. You know them. He breathes them in, and his hips lift off the bed. He has not seen you. Your face burns, but your body answers before you can stop it. Your nipples go tight and hard. Heat drops low in your belly, and you are wet. His fist slides up his cock and down again, slow, while your nipples ache.")
RYAN_WATCH = ("You stay. Your hand stays flat on the door frame. Ryan's fist moves faster on his cock. It is thick and red and wet at the tip. He lifts the panties to his face and breathes in. Then he groans under his breath. \"@player.nickname.\" Your name, in that voice. His hips jerk off the bed. He comes hard, in long white ropes across his own stomach. You watch every one. Your nipples go tight and ache. You are wet, all at once, and you never decided that. You grip the frame until your fingers hurt. You do not touch yourself. You want to. His chest heaves. His cock twitches in his hand. You back away from the door before he looks up, thighs pressed together, nipples still hard.")
out.append({"id": "ryan_door_ajar", "name": "His door's open a crack",
    "description": "Sun-Thu 22:00-00:00, Ryan in: his door open a crack, Ryan alone with her panties. Keep watching pays corruption +1, cap 19 (DECISIONS 79). Reached only by the door; once a night.",
    "trigger": {"location": "home_ryan_room", "is_repeatable": True, "priority": 1, "is_active": True,
                "substitution_only": True, "max_triggers_per_day": 1,
                # the door's own window, so a reader of the canvas sees when it can render
                "conditions": cond(here(R, "home_ryan_room"), wd(6, 0, 1, 2, 3), tod("22:00", "00:00"), trait("ryan_step", "gte", 0))},
    "nodes": [
        # DECISIONS 124 (H7): the scene reads his Want. Under 30, porn on his phone and her panties on the floor,
        # untouched; from 30, the panties to his face, as built (ryan_door_ajar.md).
        node("crack", "The crack in his door", [
            GC(cond(ntrait(R, "want", "lt", 30)), P(beat("ryan_door_ajar", "crack_low")),
               VID("through a door left ajar, a young man on his bed stroking his cock to porn on his phone, a pair of panties on the floor", "guy jerking off to porn on phone seen through door", "peeking at brother masturbating to phone door ajar", pool_dir="sex/ryan_door_crack_low_t5"),
               D(R, "Fuck. Come on. Come on, come on.")),   # pass 3 B4: to himself, under his breath
            GC(cond(ntrait(R, "want", "gte", 30)), P(RYAN_CRACK),
               VID("through a door left ajar, a young man on his bed stroking his cock, holding a pair of panties to his face", "guy jerking off with panties caught through door", "peeking at brother masturbating door ajar", pool_dir="sex/ryan_door_crack_t5"),
               D(R, "Fuck. Fuck, you smell so good. @player.nickname.")),],
            [go("Keep watching.", node="watch_low", mins=5, cond_=cond(ntrait(R, "want", "lt", 30)), flags=[fset("saw_ryan_alone"), fset("ryan_door_seen")]),
             go("Keep watching.", node="watch", mins=5, cond_=cond(ntrait(R, "want", "gte", 30)), flags=[fset("saw_ryan_alone"), fset("ryan_door_seen")]),
             go("Pull the door shut.", loc="home_hall", mins=2, flags=[fset("saw_ryan_alone"), fset("ryan_door_seen")])]),
        node("watch_low", "Keep watching", [P(beat("ryan_door_ajar", "watch_low")),
            VID("a young man on his bed coming over his stomach, his phone on his knee, seen through a door left ajar", "guy cumming to porn on phone seen through door", "voyeur watching man finish phone porn door crack", pool_dir="sex/ryan_door_watch_low_t5"),
            D(R, "Oh fuck. Oh, fuck, yes. Yes.")],
            [go("Back to your room.", loc="home_ella_room", mins=5, eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 19}], flags=[fset("saw_ryan_alone"), fset("ryan_door_seen")]),
             # C3 (DECISIONS 147): Corruption 15; its screen's exit pays +1, cap 19, and the button pays nothing: +1 a
             # night whichever way she goes (the-arc.md "+1 for an everyday act"; pass 3 G75)
             go("Stay until his light goes off.", node="light_off", mins=10, swl=True, cond_=cond(trait("corruption", "gte", 15)), flags=[fset("saw_ryan_alone"), fset("ryan_door_seen")])]),
        node("watch", "Keep watching", [P(RYAN_WATCH),
            VID("a young man on his bed coming over his stomach, seen through a door left ajar", "guy cumming jerking off seen through door", "voyeur watching man finish door crack", pool_dir="sex/ryan_door_watch_t5"),
            D(R, "Fuck. That's it. Fuck, I'm sick. I'm so fucking sick.")],
            [go("Back to your room.", loc="home_ella_room", mins=5, eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 19}], flags=[fset("saw_ryan_alone"), fset("ryan_door_seen")]),
             go("Stay until his light goes off.", node="light_off", mins=10, swl=True, cond_=cond(trait("corruption", "gte", 15)), flags=[fset("saw_ryan_alone"), fset("ryan_door_seen")])]),
        # C3: after he comes he cleans up and lies there; she stays in the dark of the landing until his lamp goes off
        node("light_off", "Until his light goes off", [
            P("You stay at the crack. Ryan lies there with his chest heaving and his cock going soft on his stomach, in the mess he made. He wipes himself off with a sock and drops it on the floor."),
            GC(cond(ntrait(R, "want", "lt", 30)), P("He picks up his phone again, scrolls, and puts it face down. Then he reaches over and clicks his lamp off.")),
            GC(cond(ntrait(R, "want", "gte", 30)), P("He lies there with the pair from the laundry basket balled in his fist against his chest. Then he reaches over and clicks his lamp off, and he doesn't let go of them.")),
            D(R, "Jesus Christ. What is wrong with me."),
            P("The hall goes black. You stand in the dark with your thighs pressed together, wet, and listen to his breathing go slow."),
            VID("a dark bedroom seen through a door left ajar, a young man lying back on his bed, the lamp just switched off", "dark bedroom door ajar guy lying in bed after", "peeking through door dark bedroom lamp off", pool_dir="sex/ryan_door_light_off_t4")],
            [go("Back to your room.", loc="home_ella_room", mins=5, eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 19}], flags=[fset("saw_ryan_alone"), fset("ryan_door_seen")])]),
    ]})

MASTER_GAP = ("Their door is open a hand's width. The lamp is on. The bed creaks, hard and fast. Through the gap you see Laura on her knees on the bed. Her nightdress is shoved up to her waist. Her ass is bare in the lamplight. Mark kneels behind her, gripping her hips. He thrusts into her, short and rough, grunting with each one. You see his cock slide out and drive back in. Laura's tits swing under her with every thrust. She stares at the headboard. Her face is flat and bored. She is waiting for him to finish. Neither of them looks at the door. Your face burns. Heat pools low in your belly. You are wet, and your nipples press hard and tight.")
MASTER_STAY = ("Through the gap you see all of it. Mark has Laura on her knees, her nightdress shoved up over her ass. His cock thrusts into her fast and hard. He grunts with every push. Her tits swing under her. Her face is turned sideways on the pillow, eyes open, bored. He gives one last grunt and rolls off her. A minute later he is snoring. Laura lies on her back, awake, the nightdress still bunched at her waist. Her hand slides down under the sheet, between her own thighs. It starts to move. Your nipples are hard and aching. You are wet. You press your thighs together and stay right there. Then a floorboard creaks under your foot. You freeze at the gap, wet, nipples still hard.")
out.append({"id": "master_door_saturday_night", "name": "Their door's ajar",
    "description": "Sun 00:00-01:00 (Saturday night), Laura and Mark both in and awake: through the gap, Mark takes Laura. Stay at the gap pays corruption +1, cap 19 (DECISIONS 79-80). Reached only by the door; once a week.",
    "trigger": {"location": "home_master_bedroom", "is_repeatable": True, "priority": 1, "is_active": True,
                "substitution_only": True, "max_triggers_per_day": 1,
                # the door's own window, so a reader of the canvas sees when it can render
                "conditions": cond(here(L, "home_master_bedroom"), here(M, "home_master_bedroom"), wd(6), tod("00:00", "01:00"))},
    "nodes": [
        node("gap", "Their door, ajar", [P(MASTER_GAP),
            G(cond(here(L, "home_master_bedroom"), here(M, "home_master_bedroom")), D(M, "Christ, that ass. Keep still."), D(L, "Are you nearly done?"), D(M, "I'll be done when I'm done. Push back."), D(L, "Mark. They'll hear.")),   # LO 2026-11-03: his grunt, her flat voice
            VID("through a bedroom door left ajar, a middle-aged man taking a woman from behind on the bed, lamp on", "couple sex seen through bedroom door ajar", "peeking at parents bedroom door gap", pool_dir="sex/master_door_gap_t5")],
            [go("Stay at the gap.", node="stay", mins=5, flags=[fset("saw_mark_and_laura"), fset("mark_laura_seen")]),
             go("Go back to bed.", loc="home_ella_room", mins=2, flags=[fset("saw_mark_and_laura"), fset("mark_laura_seen")])]),
        node("stay", "At the gap", [G(cond(here(L, "home_master_bedroom"), here(M, "home_master_bedroom")), D(M, "Ass up, Laura. Nearly there."), D(L, "Yes. Fine. Yes.")), P(MASTER_STAY),
            G(cond(here(L, "home_master_bedroom")), D(L, "Oh. Oh, God. Yes."), P("She says it into the pillow, so quiet it's almost nothing.")),
            VID("a woman lying awake in bed touching herself under the sheet while the man beside her sleeps", "wife masturbating next to sleeping husband", "woman touches herself after husband falls asleep", pool_dir="sex/master_door_stay_t5"),
            # scene reader b03 (2026-11-03): the hook (the canvas's window is every Saturday night, Sun 00:00-01:00)
            # reader pass 4 b4: her voice at her level; the stay pays to Corruption 19, so Good Girl gets her pushback
            G(cond(trait("corruption", "lt", 20)), T("Next Saturday night, after midnight, their door will be open a crack again. You swear you won't be out in that hall. You know you will.")),
            G(cond(CURIOUS), T("Next Saturday night, after midnight, their door will be open a crack again. You already know you'll be out in that hall."))],
            [go("Back to your room.", loc="home_ella_room", mins=5, eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 19}], flags=[fset("saw_mark_and_laura"), fset("mark_laura_seen")])]),
    ]})

# Laura alone (DECISIONS 82, laura_alone_in_bed.md): Sun-Fri 22:00-23:00, Mark downstairs. The same walk-in
# shape: the look pays nothing, "Keep watching." pays corruption +1, cap 19. Reached only by the door.
LAURA_HOUR = [here(L, "home_master_bedroom"), here(M, "home_master_bedroom", False), wd(6, 0, 1, 2, 3, 4), tod("22:00", "23:30")]   # bedtime 23:30 (LO, 2026-11-09)
LAURA_GAP_OPEN = trait("laura_step", "gte", 2)   # LO 2b (2026-11-01): her want is shown first, then the gap
LAURA_CRACK = ("Laura's door is open a hand's width. The bedside lamp is on low. Down the hall the TV mutters. Laura is alone in bed, the covers kicked down. Her nightdress is pushed up to her waist. Her knees are up and apart, her ass bare on the sheet. Two fingers rub slow circles on her clit. She is wet, and it shines in the lamplight. Her other hand squeezes her tit through the nightdress. Her nipple stands hard against the cotton. Her tits rise and fall faster. Her eyes are shut, her lip caught in her teeth. A small moan escapes her. Her hips lift into her fingers. She hasn't seen you. Your face burns. Heat pools low in your belly. You are wet, and your nipples go tight.")
LAURA_WATCH = ("You stay. Your hand stays flat on the door frame. Laura pushes two fingers inside herself. Her thumb rubs her clit, faster now. Her other hand squeezes her tit and pinches the nipple. Her hips lift off the mattress. She bites the back of her hand so Mark won't hear. Her fingers pump in and out, wet and loud in the quiet. Then she comes. Her whole body shakes. Her thighs clamp hard on her hand. A moan leaks out around her teeth. Your nipples go tight and ache. You are wet, all at once. You press your thighs together. You do not touch yourself. You want to. Laura goes still, breathing hard, two fingers still inside her. Her tits rise and fall. You back away from the door before she opens her eyes, thighs pressed tight, nipples still hard.")
out.append({"id": "laura_alone_in_bed", "name": "Laura's door's ajar",
    "description": "Sun-Fri 22:00-23:00, Laura awake and alone, Mark in the living room: through the gap she fingers herself. Keep watching pays corruption +1, cap 19 (DECISIONS 82). Reached only by the door; once a night.",
    "trigger": {"location": "home_master_bedroom", "is_repeatable": True, "priority": 1, "is_active": True,
                "substitution_only": True, "max_triggers_per_day": 1,
                # the door's own window, so a reader of the canvas sees when it can render
                "conditions": cond(*LAURA_HOUR, LAURA_GAP_OPEN)},
    "nodes": [
        node("crack", "Laura's door, ajar", [P(LAURA_CRACK),
            G(cond(here(L, "home_master_bedroom")), D(L, "Oh God. Oh, God, yes."), D(L, "Please. Just once. Please.")),   # LO 2026-11-03: a line for the silent; to herself, under her breath
            VID("through a bedroom door left ajar, a woman alone in bed in a nightdress touching herself, lamp low", "woman masturbating in bed seen through door", "peeking at mom touching herself in bed door ajar", pool_dir="sex/laura_alone_crack_t5")],
            [go("Keep watching.", node="watch", mins=5, flags=[fset("saw_laura_alone"), fset("laura_alone_seen")]),
             go("Pull the door to.", loc="home_hall", mins=2, flags=[fset("saw_laura_alone"), fset("laura_alone_seen")])]),
        # scene reader b02 (2026-11-03): her voice at her level: under Hungry she holds back; at Hungry her own hand moves
        # reader 2026-11-04: her words first; the beat ends with her come and Ella backing away from the door
        node("watch", "Keep watching", [G(cond(here(L, "home_master_bedroom")), D(L, "Mm. There. Right there."), D(L, "Don't stop. Don't you stop.")),
            GC(cond(trait("corruption", "lt", 60)), P(LAURA_WATCH)),
            GC(cond(trait("corruption", "gte", 60)), P(LAURA_WATCH.replace("You press your thighs together. You do not touch yourself. You want to.",
                "Your other hand is already inside your clothes. Two fingers on your clit, rubbing in time with hers, and you bite your lip so she won't hear you."))),
            VID("a woman alone in bed fingering herself to orgasm, biting her hand to stay quiet", "woman fingering herself orgasm quiet in bed", "milf masturbating to orgasm biting hand", pool_dir="sex/laura_alone_watch_t5")],
            [go("Back to your room.", loc="home_ella_room", mins=5, eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 19}, add("laura_gaps_watched", 1, clamp=False)], flags=[fset("saw_laura_alone"), fset("laura_alone_seen")])]),
    ]})
# reader a3 #2 (DECISIONS 131): her want for Ryan on her body before laura_04 says his name. Ungated: Ryan's row has
# him in his room every night 22:00-06:45, so his door is there to listen toward in the whole 22:00-23:00 window.
out[-1]["nodes"][0]["blocks"].insert(1, P("Her face is turned on the pillow toward the hall, toward Ryan's door. Her lips move around a word you can't hear, and her fingers go faster."))
# after her step 3 the crack names the dressed-up night (laura_alone_in_bed.md, changed 2026-11-01)
out[-1]["nodes"][0]["blocks"].insert(1, G(cond(flag("laura_lonely")), P("The good dress you zipped her into hangs on the wardrobe door.")))

# ── after Laura's step 4 (laura_alone_in_bed.md, "After her step 3 and step 4"): she knows; face to the wall,
#    quieter. The same door, pay, brake and no; "The door's ajar." opens this once laura_04_done is set. ──
from sheetbeats import beat
out.append({"id": "laura_alone_after", "name": "Laura's door's ajar",
    "description": "Sun-Fri 22:00-23:00 after Laura's step 4: she knows the door is open; face to the wall, quieter. Keep watching pays corruption +1, cap 19, and the gap counter. Reached only by the door; once a night.",
    "trigger": {"location": "home_master_bedroom", "is_repeatable": True, "priority": 1, "is_active": True,
                "substitution_only": True, "max_triggers_per_day": 1,
                "conditions": cond(*LAURA_HOUR, flag("laura_04_done"))},
    "nodes": [
        node("crack_after", "Laura's door, ajar", [P(beat("laura_alone_in_bed", "crack_after").replace("Her door is open", "Laura's door is open", 1)),   # pass 3 B13: her name before the pronoun (the sheet is signed; the build swaps it)
            G(cond(here(L, "home_master_bedroom")), D(L, "Oh God. Quiet. Quiet.")),   # LO 2026-11-03: to herself; watch_after's beat says "Laura says nothing."
            VID("through a bedroom door ajar, a woman on her side facing the wall, her hand between her thighs", "woman masturbating facing wall door ajar", "mom touches herself back to door", pool_dir="sex/laura_alone_after_crack_t5"),
            # writing pass: her voice at her level; laura_04_she_saw_you needs Corruption 20, so the lowest band is Curious
            *her_thought_bands("corruption", [(40, "She left it open. You want to know why."),
                                              (60, "She left this door open for somebody. You're not walking away from it.")],
                               "She wants you watching. You want to see her finish.")],
            [go("Keep watching.", node="watch_after", mins=5, flags=[fset("saw_laura_alone"), fset("laura_alone_seen")]),
             go("Pull the door to.", loc="home_hall", mins=2, flags=[fset("saw_laura_alone"), fset("laura_alone_seen")])]),
        node("watch_after", "Keep watching", [P(beat("laura_alone_in_bed", "watch_after")),
            P("She'll leave the door ajar for you again, another night after ten. She knows you'll look."),   # reader pass 3 b01: the hook (her rows: Sun-Fri 22:00-23:00)
            VID("a woman on her side coming silently into a pillow, her hand between her thighs", "woman silent orgasm into pillow", "mom cums quietly facing the wall", pool_dir="sex/laura_alone_after_watch_t5")],
            [go("Lie still.", loc="home_ella_room", mins=5, eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 19}, add("laura_gaps_watched", 1, clamp=False)], flags=[fset("saw_laura_alone"), fset("laura_alone_seen")])]),   # reader 2026-11-04: the beat has already put her in her room
    ]})

# ── the shower gap (laura_shower_gap.md, signed 2026-11-01): Saturday 16:30-17:00, Laura showering before she
#    dresses; the lock sticks halfway (the opening's fact), the door won't shut. Once a week (her Saturday row). ──
out.append({"id": "laura_shower_gap", "name": "The bathroom door won't shut",
    "description": "Saturday 16:30-17:00, Laura in the shower: through the steam her hand between her legs. Keep watching pays corruption +1, cap 19, and the gap counter (Laura's step 4).",
    "trigger": {"location": "home_bathroom", "npc": L, "requires_npc": L, "is_repeatable": True, "priority": 8, "is_active": True,
                "max_triggers_per_day": 1,
                # LO, 2026-11-09 ("Bath + later bedtime"): her shower before bed on her kitchen nights too; part of her loop.
                # The beats name no day; the hooks below say which.
                "schedules": [{"weekdays": [5], "start_time": "16:30", "end_time": "17:00"},
                              {"weekdays": [0, 1, 3, 4, 6], "start_time": "21:30", "end_time": "22:00"}],
                "conditions": cond(flag("opening_done"), LAURA_GAP_OPEN)},
    "nodes": [
        node("steam", "Steam", [P(beat("laura_shower_gap", "steam")),
            G(cond(here(L, "home_bathroom")), D(L, "Mm. God, yes."), D(L, "Fuck. I needed this.")),   # LO 2026-11-03: to herself, under the spray
            VID("through a bathroom door stuck open, a naked woman in a steamy shower touching herself", "woman masturbating in shower seen through door", "mom in shower hand between legs steam glass", pool_dir="sex/laura_shower_steam_t5"),
            # writing pass: her voice at her level; wants only, true whichever button she takes
            *her_thought_bands("corruption", [(20, "That's Mom. Step back. Step back right now."),
                                              (40, "What does she think about in there? You want to know."),
                                              (60, "You could stay till she finishes. Nobody would know.")],
                               "Don't stop, Mom. You want to see all of it."),
            # G, not GC: right after her thought bands, a GC would join their chain and never show
            G(cond(wd(5)), P("She showers at this time every Saturday.")),
            G(cond(wd(0, 1, 2, 3, 4, 6)), P("She showers at this time most nights, before bed."))],   # reader batch 4 (pass 3): the hook, her Saturday row
            # reader batch 4 (pass 3): the watch plays inside her half hour (fired at 16:56, a 5-minute button put the
            # watch screen at 17:01, when her row has her in the bedroom), so the minutes go on the way out instead
            [go("Keep watching.", node="watch", mins=0, flags=[fset("laura_shower_seen")]),
             go("Pull the door to.", loc="home_hall", mins=2, flags=[fset("laura_shower_seen")])]),
        node("watch", "Under the water", [G(cond(here(L, "home_bathroom")), D(L, "Right there. Oh God, right there.")), P(beat("laura_shower_gap", "watch")),
            # reader 2026-11-04: shocked is her first Saturday's voice, not her voice at every level; a VID follows, so the chain ends
            *her_thought_bands("corruption", [(20, "You just watched your mom come. You're shocked, and your legs are shaking."),
                                              (40, "You want to know what she thinks about in there, to come that hard."),
                                              (60, "You watched every second, and next time you'll stay longer.")],
                               "You wanted her to turn round. You wanted her to see how wet you are."),
            VID("a naked woman coming in the shower, forehead on the tiles, a moan under the spray", "woman orgasm in shower forehead on tiles", "mom cums in shower", pool_dir="sex/laura_shower_watch_t5"),
            GC(cond(wd(5)), P("Next Saturday she'll be in here again, and the lock will stick again.")),
            GC(cond(wd(0, 1, 2, 3, 4, 6)), P("Another night she'll be in here again, and the lock will stick again."))],   # reader batch 4 (pass 3): the hook
            [go("Back to your room.", loc="home_ella_room", mins=10, eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 19}, add("laura_gaps_watched", 1, clamp=False)], flags=[fset("laura_shower_seen")])]),
    ]})

# ── Laura's in there (LO playtest 2026-11-10, DECISIONS 223: "see how ryan bathroom works"): her face at the door
#    whenever her row has her in the bathroom, as Ryan's (ryan.py hub_ryan_bathroom). Pays nothing; the shower gap
#    (priority 8) still wins her face while it is open. The lock sticking is the opening's fact. ──
out.append({"id": "hub_laura_bathroom", "name": "Laura's in there",
    "description": "Laura in the bathroom (her rows: weeknights and Sunday 21:30-22:00, Saturday 16:30-17:00): the door, one line. Passing her robe pays her warmth +1 once a day (laura_robe_today).",
    "trigger": {"location": "home_bathroom", "npc": L, "requires_npc": L, "is_repeatable": True,
                "priority": 6, "is_active": True, "conditions": cond(flag("opening_done"))},
    "nodes": [
        node("door", "The bathroom door", [
            # reader 2026-11-10: the lock is the gap's fact ("the door stands open a few inches"), so this screen says it too
            G(cond(flag("laura_robe_today", False)), P("The shower's running. The lock has stuck halfway, the way it always does, so the door stands open a few inches and steam rolls out through the gap. Her robe hangs on the hook outside.")),
            # reader pass 2: after the robe, a second visit that window is not the first
            G(cond(flag("laura_robe_today")), P("The lock has stuck halfway, the way it always does, so the door stands open a few inches. The robe's gone from the hook. Behind the door she's humming over the running water.")),
            POOL(D(L, "Is that you, sweetheart? Give me a bit."),
                 D(L, "If that's Ryan, the answer's no, and go and wait your turn."),
                 D(L, "@player? Don't run the kitchen tap, honey, or I'll freeze in here."), pid="laura_bathroom_lines"),
            # her voice at her level (reader 2026-11-10): the gap means nothing to her under Curious
            G(cond(trait("corruption", "lt", 20)), T("You don't look through the gap. That's Mom in there.")),
            G(cond(trait("corruption", "gte", 20), flag("laura_shower_seen")), T("You know exactly what you'd see through that gap.")),
            G(cond(trait("corruption", "gte", 20), flag("laura_shower_seen", False)), T("You could look through the gap. You don't. Not yet.")),
        ], [go("Pass her the robe.", node="robe", mins=2, cond_=cond(flag("laura_robe_today", False)),
               eff=[nadd(L, "warmth", 1)], flags=[fset("laura_robe_today")]),
            go("Wait your turn.", loc="home_hall", mins=10), go("Leave her to her shower.", loc="home_hall")]),
        node("robe", "Her robe", [
            P("You lift the robe off the hook and hold it through the gap without looking. Her wet hand finds it. For a second the door swings wider, and you see her bare shoulder, beaded with water, and the soft side of her breast before she pulls the robe in against it."),
            D(L, "Thank you, sweetheart. You're an angel."),
            *her_thought_bands("corruption", [(20, "You look at the floor until the door's pulled to."),
                                              (40, "You saw more than you meant to. You don't mind as much as you should.")],
                               "Next time you'll hold it a little further back, so she has to open the door wider."),
        ], [go("Back to the hall.", loc="home_hall", mins=0)]),
    ]})

# Laura's hour after she watched (DECISIONS 84): one screen, pays nothing.
out.append({"id": "laura_alone_peek", "name": "Peek through the gap",
    "description": "Sun-Fri 22:00-23:00, after she has watched Laura that night: one screen, pays nothing. Reached only by the door.",
    "trigger": {"location": "home_master_bedroom", "is_repeatable": True, "priority": 1, "is_active": True,
                "substitution_only": True, "conditions": cond(*LAURA_HOUR)},
    "nodes": [node("peek", "Through the gap", [
        P("You ease the door a finger's width wider. The lamp is off now."),
        # reader pass 4 b1 (low heat is on the body): her body, Ella's reaction, the not-yet
        P("Laura lies on her side with the sheet kicked down to her knees, breathing slow. Her nightdress is still rucked up over her hip, her bare ass pale in the dark, and her hand is still tucked between her thighs."),
        # scene reader 2026-11-10: her want on the screen, and the next step
        P("Her lips move against the pillow, on a name you can't hear, her face turned toward the hall and Ryan's door."),
        # scene reader 2026-11-10 (DECISIONS 220): one step past the watch: the door moves, and she answers it without looking
        GC(cond(flag("laura_04_done", False)), P("The door creaks. Laura's hand goes still. Without opening her eyes she draws the sheet up over her bare hip, slow, and lies there, listening.")),
        GC(cond(flag("laura_04_done")), P("The door creaks. Laura doesn't reach for the sheet. She shifts her hip so the nightdress rides higher, and stays like that, her eyes shut.")),
        P("Your nipples go tight. You could go in. Not tonight."),
        P("Down the hall the TV mutters. You pull the door to without a sound."),
    ], [go("Close the door.", loc="home_hall", mins=2)])]})

# Reader item 4 (LO, 2026-10-29, master_door_peek.md): the hour's other face. One screen, pays nothing.
out.append({"id": "master_door_peek", "name": "Peek through the gap",
    "description": "Sun 00:00-01:00, someone inside and 'The door's ajar.' off: after she has watched, or Mark alone while Laura waits up in the hall. One screen, pays nothing. Reached only by the door.",
    "trigger": {"location": "home_master_bedroom", "is_repeatable": True, "priority": 1, "is_active": True,
                "substitution_only": True,
                # the door's own window, so a reader of the canvas sees when it can render
                "conditions": cond(here(M, "home_master_bedroom"), wd(6), tod("00:00", "01:00"))},
    "nodes": [node("peek", "Through the gap", [
        P("You ease the handle down and open the door a finger's width. The lamp is still on."),
        G(cond(here(L, "home_master_bedroom"), here(M, "home_master_bedroom")),
          # pass 4 reader: no next step and no hook, as signed (LO, 2026-11-04). Reader 2026-11-04: awake or snoring (she may have stayed at the gap first), so no word on his breath
          P("It's over. Mark's flat on his back with one arm over his eyes. Laura lies awake beside him, staring at the ceiling, her nightdress still bunched up at her waist. Her hand slides down her bare stomach and stops, but it comes back. She hasn't had what she wanted.")),
        G(cond(here(M, "home_master_bedroom"), here(L, "home_master_bedroom", False)),
          P("Mark's sitting up against the headboard under the lamp, awake and alone, his phone lit in his hand. Laura's side of the bed is empty. The sheet is tented over his lap, and he's looking at her pillow, not the phone.")),
        P("Your face goes hot, and your nipples go tight. One creak from this hinge and you'd have to explain what you're doing at their door at this hour."),   # writing pass: low heat (H4), her body and the price
        P("Nobody looks at the door. You pull it to without a sound."),
    ], [go("Close the door.", loc="home_hall", mins=2)])]})

# ═════════════════════════════════════════════════════════════════════════════
# THE GARAGE (home_garage.md): his things (A1-13, A1-21), the washer alone
# ═════════════════════════════════════════════════════════════════════════════
out.append(solo("garage_things", "Go through Mark's things",
    "When Mark is out. The debt papers: reads rent_short; the loan is named only after knows_mark_debt. Once a day.",
    "home_garage", [
        node("bench", "Mark's bench", [
            P("Mark's workbench, his radio, a fridge of beer that hums. The filing box under the bench has a padlock, and the key is on a nail above it, which tells you exactly how much Mark thinks of everybody in this house."),
            G(cond(flag("rent_short")), P("On top of the folders, a new page in Mark's square capitals, a figure crossed out and written again, bigger. Your short week is in there. He's added it in red.")),
            G(cond(flag("rent_short", False), flag("knows_mark_debt", False)), P("Folders of bank letters, payslips, the car's papers. Columns of numbers in his capitals that never seem to add up to enough.")),
            G(cond(flag("rent_short", False), flag("knows_mark_debt")), P("A loan agreement with Vance's signature on every page, the house on the first one. Mark's been paying it off for years and the number at the bottom has barely moved.")),
            P("Under the folders, a magazine. Girls on the cover, bent over. You put it back where it was, square to the edge, the way he'd notice."),
        ], [go("Lock it up again.", loc="home_hall", mins=15)]),
    ], conds=[here(M, "home_garage", False)], prio=3, max_day=1))

out += brake_canvas(solo("garage_laundry", "Do your laundry",
    "The washer, alone: 30 min, energy −5 (home_life.md:71). With Mark here it is in his hub.",
    "home_garage", [node("washer", "The washer", [
        P("You sort your basket on the garage floor, darks and lights. The old machine sits there with its door hanging open."),
        # her voice at her level (Corruption, no floor): Mark's bench is right there, and he isn't
        G(cond(trait("corruption", "lt", 20)), T("Just laundry. You keep your underwear at the bottom of the basket, where nobody has to see it.")),
        G(cond(trait("corruption", "gte", 20), trait("corruption", "lt", 40)), T("Your underwear goes round in the drum, right next to his workbench. You wonder if he's ever looked.")),
        G(cond(trait("corruption", "gte", 40), trait("corruption", "lt", 60)), T("You could leave your smallest underwear on top of the machine, right by his bench. You could see what he does.")),
        G(cond(trait("corruption", "gte", 60)), T("You want to leave your underwear on his bench, still warm, and make him do something about it.")),
    # reader 2026-11-04: the machine starts after her yes, so "Later." doesn't leave it running
    ], [go("Load it.", node="loaded", mins=2, flags=[fset("did_laundry")], eff=[add("energy", -5)],
           costs=[{"trait": "energy", "value": 5}]),
        go("Later.", loc="home_hall")]),
       node("loaded", "The washer", [
        P("You feed the old machine until it shudders and starts. It sounds like it's dying, but it always sounds like that."),
       ], [go("Wait for the cycle.", loc="home_garage", mins=28)])],
    sched=S(ALL, "07:00", "21:00"), conds=[here(M, "home_garage", False)]), "did_laundry")

# ═════════════════════════════════════════════════════════════════════════════
# THE GARDEN (home_garden.md): the sun, the washing line. Mark and Ryan are not in the garden;
# they see it from the garage door and his window, so their versions are choices here, read by
# their rows (home_garden.md:31-34).
# ═════════════════════════════════════════════════════════════════════════════
MARK_SEES = here(M, "home_garage")
RYAN_SEES = here(R, "home_ryan_room")
SUN_EFF = {"targetType": "player", "trait": "energy", "op": "add", "value": 5, "cap": 100}
TOPLESS = [slot("top", False), slot("dress", False), slot("bra", False)]
BRA_ONLY = [slot("top", False), slot("dress", False), slot("bra")]
sun_nodes = [
    node("sun", "The lounger", [
        # Iteration 002, part 8 (reader): the sun only while it's up; the garden is open to 21:00.
        G(cond(tod("07:00", "19:00")), P("You drag the lounger into the one patch of sun and lie down with your eyes shut. The grass smells cut. The fence is low.")),
        G(cond(tod("19:00", "21:00")), P("You drag the lounger out and lie down in the last of the light, eyes shut. The grass smells cut. The fence is low.")),
        GC(cond(*TOPLESS), P("Topless, on your front, the side of your tits pressed flat to the lounger.")),
        GC(cond(*BRA_ONLY), P("Your bra and nothing over it, your stomach bare.")),
        GC(cond(*ANY), P("In what you have on, face to the sky.")),
        G(cond(MARK_SEES), P("The garage door is open. Mark's radio is on in there, and once the radio goes quiet you know he's standing in the doorway."), D(M, "Is that what you call sunbathing?"), ME("It's what I call lying down, Mark.")),
        G(cond(RYAN_SEES), P("Ryan's window is open above you. His music stops."), D(R, "Seriously, @player.nickname? In the garden?"), ME("Close your curtains, then.")),
    ], [
        # pass 3 D44 (the-surfaces.md R9): the hour on her body, and the wave at Ryan, end on a screen, not a toast
        *brake(go("Lie in the sun.", node="sun_hour", mins=60, flags=[fset("sunned")], eff=[SUN_EFF],
                  cond_=cond(here(M, "home_garage", False), here(R, "home_ryan_room", False))), "sunned"),
        # reader a3 #10 (DECISIONS 131): a stage gate (Curious or Daring, two copies: conditions don't nest) and a screen
        *brake(go("Lie in the sun an hour. Let Mark look.", node="sun_mark_look", mins=5, flags=[fset("sunned")],
                  cond_=cond(MARK_SEES, flag("mark_saw_her"), CURIOUS), eff=[SUN_EFF, npc_add(M, "want", 1)]), "sunned"),
        *brake(go("Lie in the sun an hour. Let Mark look.", node="sun_mark_look", mins=5, flags=[fset("sunned")],
                  cond_=cond(MARK_SEES, flag("mark_saw_her"), DARING, trait("corruption", "lt", 20)), eff=[SUN_EFF, npc_add(M, "want", 1)]), "sunned"),
        *brake(go("Lie in the sun. Wave up at Ryan.", node="sun_wave", mins=60, flags=[fset("sunned")],
                  cond_=cond(RYAN_SEES, here(M, "home_garage", False)), eff=[SUN_EFF, npc_add(R, "warmth", 1)]), "sunned"),
        *brake(go("Show off for whoever's looking.", node="sun_seen", mins=60, flags=[fset("sunned")],
                  cond_=cond(SHOWING, *TOPLESS, MARK_SEES, flag("mark_saw_her")),   # topless by choice for one: Showing (DECISIONS 124)
                  eff=[SUN_EFF, {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 59}]), "sunned"),
        *brake(go("Show off for whoever's looking.", node="sun_seen", mins=60, flags=[fset("sunned")],
                  cond_=cond(SHOWING, *TOPLESS, RYAN_SEES, here(M, "home_garage", False)),
                  eff=[SUN_EFF, {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 59}]), "sunned"),
        # reader a3 #10 (DECISIONS 131): "Play up to..." only when its screen has a button: bra-only (the tease) or,
        # for Ryan, the lotion (Bold, his step 7). The lotion copies are split by "not bra-only" so one shows at a time.
        *[go("Play up to Ryan's window.", node="sun_ryan", cond_=cond(RYAN_SEES, CURIOUS, trait("ryan_step", "gte", 3), flag("sunned", False), *extra))
          # scene reader b02 (2026-11-03): the lotion choice itself needs no top and no dress (writer.CHOICES), so the
          # only other live copy is topless; the bra-and-top / bra-and-dress copies led to a screen of "Not today." alone
          for extra in (BRA_ONLY,
                        [BOLD, trait("ryan_step", "gte", 7), here(M, "home_garage", False), *TOPLESS])],   # the lotion needs Mark out of the garage door
        go("Play up to Mark in the garage door.", node="sun_mark", cond_=cond(MARK_SEES, CURIOUS, trait("mark_step", "gte", 3), flag("mark_saw_her"), flag("sunned", False), *BRA_ONLY)),   # after his accident (H2, DECISIONS 124)
        # reader 2026-11-04 (a solo button is a real act): Mark in the garage door and no look button open to her,
        # before his accident or under both her stages: the same hour and the same pay as her other sun button
        *brake(go("Lie in the sun.", node="sun_hour", mins=60, flags=[fset("sunned")], eff=[SUN_EFF],
                  cond_=cond(MARK_SEES, flag("mark_saw_her", False))), "sunned"),
        *brake(go("Lie in the sun.", node="sun_hour", mins=60, flags=[fset("sunned")], eff=[SUN_EFF],
                  cond_=cond(MARK_SEES, flag("mark_saw_her"), trait("corruption", "lt", 20), trait("exhibitionism", "lt", 20))), "sunned"),
        go("Go in.", loc="home_hall"),
    ]),
    node("sun_seen", "Seen", [
        # copy fix A5 (DECISIONS 125): one branch per watcher; both choices in need TOPLESS, and the sun node says "on your front"
        GC(cond(MARK_SEES), P("You stay on your front and push up on your elbows, slow, so from the garage door he gets your bare back and the curve of your ass. The radio stays off. When you look round, Mark is holding his beer low, in front of his jeans."),
           D(M, "Fence is low, @player."), ME("I'm not turning over, Mark. Not today.")),
        GC(cond(RYAN_SEES, here(M, "home_garage", False)), P("You roll onto your back, and your tits are bare to the sky and to his window. His music doesn't come back on. Ryan stands at the glass, then steps back fast, red to the ears."),
           ME("Want a better look, Ryan? Come down and ask me."), P("He doesn't come down. Not today.")),
        GC(cond(*ANY), P("You stay exactly as you are until whoever was looking has gone. Your skin is hot, but you don't cover up.")),
        # heat proposal A10 (DECISIONS 147): a _t4 pool on the show-off screen (nudity, not sex; media only)
        VID("a topless girl sunbathing on a lounger in a back garden, a man watching her from a doorway or a window",
            "topless sunbathing back garden watched", "topless girl on lounger neighbour watching", pool_dir="sex/garden_sun_seen_t4"),
    ], [go("Go in.", loc="home_hall")]),
    node("sun_hour", "An hour in the sun", [
        # scene reader b02 (2026-11-03): the garden is open to 21:00, so an hour that ends after 20:00 ends in the dusk
        GC(cond(tod("07:00", "20:00")), P("An hour later you sit up, slow and heavy. Your skin is hot, the lounger has printed its slats into you, and sweat has run down between your tits.")),
        GC(cond(*ANY), P("An hour later you sit up in the dusk, slow and heavy. The light has gone off the garden, the lounger has printed its slats into you, and the cool air has your nipples standing up hard.")),
    ], [go("Get up off the lounger.", loc="home_garden")]),
    node("sun_wave", "Wave up at Ryan", [
        # pass 4 reader: his line by the clock (the screen renders after the hour, so the sun is up till 20:00, as
        # sun_hour), and the flirt only from Curious (H1: a chosen flirt is stage 2), on her body, with its not-yet
        GC(cond(RYAN_SEES, tod("07:00", "20:00"), trait("corruption", "lt", 20)),
           P("You wave up at his window. Ryan jerks back from the glass, then comes back and lifts a hand, red to the ears. His eyes go down your legs on the lounger before he can stop them."),
           D(R, "Put some sun cream on. You'll fry."), ME("Yes, Mom."), P("He laughs and shuts the window. Every time you stretch, the curtain moves.")),
        GC(cond(RYAN_SEES, tod("07:00", "20:00"), CURIOUS),
           P("You wave up at his window. Ryan jerks back from the glass, then comes back and lifts a hand, red to the ears."),
           D(R, "Put some sun cream on. You'll fry."), ME("Come down and do it for me."),
           P("His eyes go down your body on the lounger, your tits, your stomach, your legs, and he grips the sill. He doesn't come down. Not yet."),
           P("All hour, every time you shift on the lounger and stretch, his curtain moves.")),
        GC(cond(RYAN_SEES, trait("corruption", "lt", 20)),
           P("You wave up at his window. Ryan jerks back from the glass, then comes back and lifts a hand, red to the ears. His eyes go down your legs on the lounger before he can stop them."),
           D(R, "You'll freeze out there, @player.nickname."), ME("Yes, Mom."), P("He laughs and shuts the window. Every time you stretch, the curtain moves.")),
        GC(cond(RYAN_SEES, CURIOUS),
           P("You wave up at his window. Ryan jerks back from the glass, then comes back and lifts a hand, red to the ears."),
           D(R, "You'll freeze out there in that, @player.nickname."), ME("Come down and warm me up, then."),
           P("His eyes go down your body on the lounger, your tits, your stomach, your legs, and he grips the sill. He doesn't come down. Not yet."),
           P("All hour, every time you shift on the lounger and stretch, his curtain moves.")),
        G(cond(here(R, "home_ryan_room", False)), P("You wave up at his window, and Ryan lifts a hand, red to the ears. By the end of the hour his window is empty.")),
    ], [go("Get up off the lounger.", loc="home_garden")]),
    # reader a3 #10 (DECISIONS 131): "Let Mark look." gets his reaction. Clothes by the same three slots the lounger names.
    node("sun_mark_look", "Let Mark look", [
        GC(cond(*TOPLESS), P("You stay on your front with your arms under your head. From the garage door he gets your bare back all the way down, and the side of your tit pressed flat to the lounger.")),
        GC(cond(*BRA_ONLY), P("You stretch your arms over your head so your tits push up in your bra, and you leave them there.")),
        GC(cond(*ANY), P("You stretch one leg out long and leave the other knee up, so the garage door gets the whole length of your legs.")),
        # truth pass (2026-11-03): Mark's look and lines only while his row still has him in the garage door
        # (the choice in reads MARK_SEES; the screen is 5 minutes on, and his Saturday garage row ends at 17:00)
        G(cond(MARK_SEES), P("The radio in the garage stays off. Mark leans in the doorway with his beer held low in front of his jeans and looks, slow, and doesn't go back in.")),
        GC(cond(tod("07:00", "19:00"), MARK_SEES), D(M, "You'll burn, @player.")),   # the sun only while it's up (the lounger's own split)
        GC(cond(*ANY, MARK_SEES), D(M, "Fence is low, @player.")),
        G(cond(MARK_SEES), ME("You can come out, you know. It's your garden."), D(M, "I can see fine from here.")),
        G(cond(MARK_SEES), P("He doesn't come out. After the hour he goes back to his bench, and the radio comes on loud.")),
    ], [go("Get up.", loc="home_garden", mins=55)]),
    node("sun_ryan", "Ryan's window", [G(cond(RYAN_SEES), P("His window is open above you. He isn't pretending to look at his screen any more."))], [
        *brake(go("Stretch out for him.", node="sun_ryan_tease", flags=[fset("sunned")], eff=[npc_add(R, "want", 1)],
                  cond_=cond(*BRA_ONLY)), "sunned"),
        *brake(go("Call him down with the sun lotion.", node="sun_ryan_touch", flags=[fset("sunned")],
                  cond_=cond(BOLD, trait("ryan_step", "gte", 7), here(M, "home_garage", False)),   # "Somebody's going to look out a window" is only true with Mark not in the garage door
                  eff=[npc_add(R, "want", 1), {"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 59}]), "sunned"),
        go("Not today.", node="sun_ryan_no")]),
    # writing pass (the written no; a solo button is a real act): her no is spoken, he answers, and she goes in. It pays nothing.
    dict(node("sun_ryan_no", "Not today", [
        ME("Not today, Ryan. Back to your screen."), D(R, "I didn't say anything."), ME("You didn't have to. Your curtain's been moving."),
        P("You get up off the lounger and walk to the back door with your back to his window, but his eyes stay on your ass all the way in."),
    ], [go("Go in.", loc="home_hall", mins=2)]), pin=[RYAN_SEES]),
    node("sun_mark", "The garage door", [G(cond(MARK_SEES), P("Mark's in the garage door with a beer, and he hasn't gone back in."))], [
        *brake(go("Stretch out for him.", node="sun_mark_tease", flags=[fset("sunned")], eff=[npc_add(M, "want", 1)],
                  cond_=cond(*BRA_ONLY)), "sunned"),
        # (release 1: Mark's paid look is cut, npc_mark.md)
        go("Not today.", node="sun_mark_no")]),
    # writing pass (the written no; a solo button is a real act): the same for Mark. It pays nothing.
    dict(node("sun_mark_no", "Not today", [
        ME("Not today, Mark. Your bench is that way."), D(M, "Didn't say a word, @player."),
        P("He stays in the door with his beer and looks at your bare stomach while you get up. He looks at your legs all the way across the grass."),
    ], [go("Go in.", loc="home_hall", mins=2)]), pin=[MARK_SEES]),
    # truth pass (2026-11-03): each writer screen is about the man at the window / the garage door, so the whole
    # screen carries his presence (`pin`, canv.pin_blocks, applied after writer.fill swaps the screen in)
    dict(node("sun_ryan_tease", "Ryan's window", [placeholder("sheets/people/npc_ryan.md:104", "Ryan, the garden: tease (Curious, Ryan A 4)")],
         [go("Done.", loc="home_garden", mins=30)]), pin=[RYAN_SEES]),
    dict(node("sun_ryan_touch", "The sun lotion", [placeholder("sheets/people/npc_ryan.md:104", "Ryan, the garden: touch (Bold, Ryan A 8)")],
         [go("Done.", loc="home_garden", mins=30)]), pin=[RYAN_SEES]),
    dict(node("sun_mark_tease", "The garage door", [placeholder("sheets/people/npc_mark.md:110", "Mark, the garden: tease (Curious, Mark A 3)")],
         [go("Done.", loc="home_garden", mins=30)]), pin=[MARK_SEES]),
]
# pass 4 reader (a solo button is a real act): every way onto the lounger is once a day (`sunned`), so after it the
# lounger is gone for the day, not a screen that says she lies down and offers only "Go in."
out += brake_canvas(solo("garden_sun", "Lie in the sun",
    "The lounger: 60 min, energy +5; Daring and seen, exhibitionism +1 (home_garden.md:29-34). Mark sees from the garage door (his Saturday row), Ryan from his window (his weekend row). Their tease and touch lines are placeholders. Once a day (sunned).",
    "home_garden", sun_nodes, prio=3), "sunned")

out += brake_canvas(solo("garden_washing", "Hang the washing",
    "The washing line, after a load: 15 min, alone and plain (home_garden.md:30).",
    "home_garden", [node("line", "The washing line", [
        P("You peg out the load in a row: jeans, towels, and your smalls on the end where the wind gets them. A gust takes one two gardens down, and you go and get it back with your face hot."),
        G(cond(MARK_SEES), P("Mark's in the garage doorway when you come back with it. He's seen.")),
        G(cond(here(M, "home_garage", False)), P("Nobody's watching.")),
    ], [go("Done.", loc="home_garden", mins=15, flags=[fset("hung_washing")]), go("Later.", loc="home_hall")])],
    conds=[flag("did_laundry"), since("did_laundry", "lt")], prio=2), "hung_washing")

# ═════════════════════════════════════════════════════════════════════════════
# THE FRONT DOOR (home_front_door.md): sit on the step (A1-22 by the clock, A1-23 back to the hall)
# ═════════════════════════════════════════════════════════════════════════════
out.append(solo("front_step", "Sit on the step", "Watch the street. Who passes reads the clock and what she has on. Writes nothing.",
    "home_front_door", [
        node("step", "The front step", [
            GC(cond(tod("07:00", "21:00")), POOL(
                GC({"version": "1.0", "logic": "AND", "items": []}, P("You sit on the front step with your knees up and watch the street. A car goes by slow. A guy walking his dog looks at your legs, and keeps looking until the dog drags him on."),
                   WHO("Now that's a lovely view."), ME("Keep walking. Looking's all you get.")),   # reader pass 3 b00: the pool runs 07:00-21:00, not only evenings
                GC({"version": "1.0", "logic": "AND", "items": []}, P("Two doors down a man is washing his car. He stops when you sit down, and his eyes go up your legs and stay there while the hose runs over his shoes."),
                   WHO("You want a job? I pay in ice cream."), ME("I'm good, thanks. Eyes on your car.")))),
            GC(cond(tod("21:00", "07:00")), P("The street is dark and quiet, the porch light on its timer. A car passes now and then, slow, headlights sliding over you.")),
            # LO 2026-11-03: the street speaks. G (a pool) breaks the clock chain above.
            G(cond(tod("07:00", "21:00")), WHO("Don't get up on my account.")),
            G(cond(tod("21:00", "07:00")), P("A window comes down on a passing car."), WHO("Hey, beautiful! Want a ride?"),
              ME("Not from you."), WHO("Your loss, legs."), P("He laughs, and the car pulls off, slow, his eyes on your legs in the mirror till the corner.")),   # reader pass 4 b4: the written no
            # DECISIONS 124: showing the street is showing a group, Watched (Exhibitionism 60); under it she keeps her knees down
            # reader a3 #9 (DECISIONS 131): the E60 lines only by day, beside a watcher, and each holds a not-yet
            G(cond(SKIRT, slot("underwear"), trait("exhibitionism", "gte", 60), tod("07:00", "21:00")), P("With your knees up in this skirt, anyone passing can see your panties. A man across the road stops with his keys in his hand and looks straight between your knees. You could put your knees down, but you don't. You don't open them for him either. Not yet.")),
            G(cond(SKIRT, trait("exhibitionism", "lt", 60)), P("In this skirt you sit with your knees together and your hands on the hem, but a car slows anyway, and you feel your face go hot.")),
            G(cond(SKIRT, slot("underwear", False), trait("exhibitionism", "gte", 60), tod("07:00", "21:00")), P("There's nothing under the skirt. The air on the step is cool between your legs. A car slows at the curb, and the driver's eyes drop to your knees. You keep them exactly where they are, because one inch is the whole street's business. Not yet.")),
            G(cond(here("npc_vance", "vance_house")), P("Next door, Vance lowers his paper on the porch and watches you over the top of it, but he doesn't wave.")),
        ], [go("Let the street see.", node="street_sees", mins=5, cond_=cond(SKIRT, trait("exhibitionism", "gte", 60), tod("07:00", "21:00"), flag("street_step_today", False)),   # reader a3 #3 (DECISIONS 131): the E60 showing choice, once a day
               eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 79}, add("laura_suspicion", 2)], flags=[fset("street_step_today")]),
            go("Go back in.", loc="home_hall", mins=20)]),
        # reader a3 #3 (DECISIONS 131): a passer-by's reaction and a price (the neighbor's phone: Mom's suspicion +2)
        node("street_sees", "Let the street see", [
            GC(cond(slot("underwear")), P("You let your knees fall open on the step. The skirt slides up your thighs, and your panties are right there for the street, the fabric pulled tight over your cunt.")),
            GC(cond(slot("underwear", False)), P("You let your knees fall open on the step. The skirt slides up your thighs, and there's nothing under it. Your cunt is bare to the street, and the air is cool on it.")),
            P("A man coming up the sidewalk with his shopping sees. He slows right down. His eyes go between your knees and stay there, and he walks into the gate post two doors down. He goes past twice."),
            WHO("Jesus. Sorry. Jesus Christ."),   # LO 2026-11-03
            ME("Watch where you're going."), WHO("I am. Believe me, I am."),
            G(cond(here("npc_vance", "vance_house")), P("Next door, Vance's paper is down in his lap. He doesn't pretend to read it.")),
            G(cond(here("npc_vance", "vance_house"), flag("vance_met")), D("npc_vance", "Mark's girl has good legs.")),   # his short-skirt line (npc_vance.md); she is in the skirt here
            P("Across the road a curtain moves. The woman at the window has her phone in her hand, and she knows your mother."),
            T("That'll get back to Mom, but you keep your knees open a minute longer anyway."),
        ], [go("Knees together. Go in.", loc="home_hall", mins=15)]),
    ], prio=2))

# ═════════════════════════════════════════════════════════════════════════════
# RANDOM EVENTS AT HOME (home_hall.md:36-49, Q59): 1 in 4 on entering the hall, kitchen, living
# room or bathroom, one a day. Each shows only when its person's row puts them there; with nobody
# there it is the room's quiet line. One brake flag across all of them, read 24 hours.
# ═════════════════════════════════════════════════════════════════════════════
def event(cid, name, loc, sched, conds, blocks, plain, raise_eff, curious=None, bold=None, ph_name=None, her_cap=None,
          record=(), pay_her=False, entry_eff=(), plain_after=None, chance=0.25):
    """entry_eff: his raise for what happened, paid on the way in: the event has no button into it, so it rides the
    trigger's `pre_substitution_effects`, which the engine runs unconditionally at the top of node 0
    (template_import.py:899-906, :2618-2622, :9404-9407; v2.py:16364-16397). His Want then pays for the moment and
    never for her no (the-heat-ladder.md H5; the-arc.md "the event's raise goes to him"). That hook takes trait
    effects only, so `record` (his flag for what happened) rides every exit alike: it records the moment, which
    happened whichever button she clicks. raise_eff rides every exit too (Laura's robe, a warmth beat on her side).
    pay_her: her go-further button also pays her Corruption +1, capped at the top of the stage it opens at
    (39 Curious, 59 Bold); recap.py then moves it one stage up (playtest 2026-11-09). `her_cap` overrides it
    for an event that opens higher than its gate says. The way out pays her nothing (pass 3 G12).
    plain_after: pass 3 D44 (the-surfaces.md R9): the plain answer's own short screen (his or her reaction), so the
    moment does not end on a toast. Appended last, so nodes[1] stays the curious screen."""
    rec = [fset(f) for f in record]
    exits = [go(plain, mins=2, eff=raise_eff, flags=[fset("home_event")] + rec,
                **(dict(node="ev_plain") if plain_after else dict(loc=loc)))]
    if plain_after:
        nodes_after = [node("ev_plain", plain.rstrip("."), list(plain_after[0]), [go(plain_after[1], loc=loc)])]
    else:
        nodes_after = []
    nodes = []
    for kind, spec, gate in (("curious", curious, [CURIOUS]), ("bold", bold, [BOLD])):
        if not spec:
            continue
        label, ref, extra = spec
        her = ([{"targetType": "player", "trait": "corruption", "op": "add", "value": 1,
                 "cap": her_cap or (59 if BOLD in gate + list(extra) else 39)}] if pay_her else [])
        exits.append(go(label, node=f"ev_{kind}", cond_=cond(*gate, *extra), eff=list(raise_eff) + her or None,
                        flags=[fset("home_event")] + rec))
        nodes.append(node(f"ev_{kind}", label.rstrip("."), [placeholder(ref, f"{ph_name or name}: {kind}")], [go("Go on.", loc=loc, mins=2)]))
    odds = "1 in 4" if chance == 0.25 else f"chance {chance}"
    c = {"id": cid, "name": name, "description": f"Random event at home (home_hall.md): {name}. {odds}, one a day.",
         "trigger": {"location": loc, "is_repeatable": True, "priority": 4, "is_active": True,
                     "trigger_mode": "random", "chance": chance, "conditions": cond(*conds)},
         "nodes": [node("event", name, blocks, exits)] + nodes + nodes_after}
    if sched:
        c["trigger"]["schedules"] = sched
    if entry_eff:
        c["trigger"]["pre_substitution_effects"] = list(entry_eff)
    return brake_canvas(c, "home_event")


out += event("home_event_ryan_towel", "Ryan out of the shower", "home_hall", S([0, 1, 2, 3, 4], "06:45", "07:30"),
             [here(R, "home_bathroom"), flag("opening_done")],
             # DECISIONS 124 (H3, H7): the accident names what her clothes show and his reaction, covered at stage 1
             [P("The bathroom door opens as you pass and Ryan steps out in a towel, wet, steam behind him. You nearly walk into his chest."),
              # copy fix A4 (DECISIONS 125): the towel and the sleep shirt with a bra get their own lines; the else names her tits
              GC(cond(TOWEL),
                 P("You're in your towel too. His eyes drop to the knot over your tits. They go down to your bare thighs and jump back to your face. He goes red. He turns side-on, one fist tight on the front of his towel.")),
              GC(cond({"type": "clothing_item", "item_id": "sleep_shirt", "operator": "equipped"}, {"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}),
                 P("You're in your sleep shirt, bare legs, no bra. His eyes drop to your tits, and he catches himself and looks at the ceiling. He turns sideways to get past you, the towel bunched in his fist at the front.")),
              GC(cond({"type": "clothing_item", "item_id": "sleep_shirt", "operator": "equipped"}),
                 P("His eyes drop down your sleep shirt to your bare legs and jump back to your face. He goes red. He turns side-on, one fist tight on the front of his towel.")),
              GC(cond(*ANY),
                 P("His eyes drop to your tits and jump back to your face. He goes red. He turns side-on, one fist tight on the front of his towel.")),
              D(R, "Sorry. Shit. Morning."), ME("Morning. You're dripping on me."), D(R, "Two more minutes. Go on. Go."),
              T("He's out of that bathroom at this time every weekday.")],   # reader a3 older: a hook
             # pass 3 G12: he sees her, so the moment raises his Want +2 (as the walk-ins do) on the way in, and records it
             # on every exit alike, so it is never a raise for her answer (C1, LO 2026-11-03; H5: a no adds 0); her bolder
             # buttons pay her
             "Step round him.", [], record=["ryan_saw_her_towel"], pay_her=True, entry_eff=[npc_add(R, "want", 2)],
             curious=("Walk past slowly.", "sheets/places/home_hall.md:44", [BOLD]),   # her tits brush his chest: a touch, Bold (DECISIONS 124)
             bold=("Let him look.", "sheets/places/home_hall.md:44", [trait("ryan_step", "gte", 3)]),
             # reach audit 2026-11-09 (playtest: "the towel slip timing"): she wakes about 07:00 and his row ends 07:30,
             # so at 1 in 4 most players never met him. It is his habit, not luck: 3 in 4, and his card says when.
             chance=0.75)
out += event("home_event_laura_robe", "Laura's robe", "home_kitchen", S([0, 1, 2, 3, 4], "06:30", "08:00"),
             [here(L, "home_kitchen"), flag("opening_done")],
             [P("Laura reaches up for the cereal on the top shelf and her robe slips open over her tits. She ties it again fast, pink to the ears."),   # reader a3 #11 (DECISIONS 131)
              D(L, "Don't look at me like that. It's early."), ME("I didn't see anything, Mom."), D(L, "Good. There's nothing to see before seven."),
              T("She's down here in that robe every weekday morning. So are you.")],   # reader a3 older: a hook
             "Look away.", [npc_add(L, "warmth", 1)],
             curious=("Don't look away.", "sheets/places/home_hall.md:45", []),
             plain_after=([P("You look at the kettle instead, hard. Behind you she lets out a breath and laughs, short, and pats your hip on her way past to the fridge."),
                           D(L, "Thank you, sweetheart. Coffee?"), ME("Two sugars?"), D(L, "You know me too well.")], "Make two."))
# copy fix A7 (DECISIONS 125): the signed screen for "Don't look away." in place of its PLACEHOLDER
_robe = out[-1]
assert _robe["id"] == "home_event_laura_robe" and _robe["nodes"][1]["id"] == "ev_curious"
_robe["nodes"][1]["blocks"] = [
    P("You don't look away. Laura's fingers are still on the knot, and your eyes are still on her chest, where the robe sat open a second ago. She sees where you're looking. The pink goes down her neck and into the robe."),
    D(L, "Eyes up, sweetheart."),
    ME("You look good, Mom."),
    P("She laughs, short, and pulls the robe tighter, but it doesn't help. The knot sits tight across her chest now, and you both know you're looking at it."),
    D(L, "Not before my coffee. Go on."),
    T("She didn't tell you to stop. She told you not yet."),
    G(cond(flag("laura_lonely"), flag("laura_04_done")), P("Tonight her bedroom door won't quite close. She knows you know it.")),   # reader a3 older: she knows only after step 4   # laura_06 sets it: "On weeknights now..."
]
out += event("home_event_mark_reach", "Mark reaching past", "home_kitchen", S([6], "08:00", "22:00"),
             [here(M, "home_kitchen")],
             [P("Mark reaches over you for a mug off the shelf, close, his arm past your face, his chest at your back for a second longer than the mug needs."),
              # reader a3 #12 (DECISIONS 131): under Bold (where "Lean back into him." can't show) he pulls away himself
              G(cond(trait("corruption", "lt", 40)), P("Then he steps back fast, his hips turned away from you, the mug held low in front of his jeans."),
                D(M, "Mind yourself, @player."), ME("You reached past me, Mark."), D(M, "My kitchen. My mugs. Stand somewhere else on a Sunday."), T("Next time he reaches past you, you'll know why.")),
              G(cond(trait("corruption", "gte", 40)), D(M, "Don't move, @player. I've nearly got it."), ME("Take your time, Mark. I'm not going anywhere."))],   # reader a3 older: a hook
             # pass 3 G12: his chest at her back is the moment: his Want +2 on the way in and a record on every exit alike
             # (C1 holds: nothing rides on her answer; H5: a no adds 0); "Lean back into him." pays her
             "Duck out of his way.", [], record=["mark_brushed_reach"], pay_her=True, entry_eff=[npc_add(M, "want", 2)],
             curious=("Lean back into him.", "sheets/places/home_hall.md:46", [BOLD]))   # a touch: Bold (DECISIONS 124)
out += event("home_event_mark_asleep", "Mark asleep, TV on", "home_living_room", S([0, 1, 2, 3, 4, 5], "00:00", "02:00"),
             [here(M, "home_living_room")],
             [P("Mark is slumped on the couch with the TV still on, eyes half shut, a beer going warm in his hand, his head tipped back."),
              D(M, "Mm. @player? That you?"), ME("Go to bed, Mark. You're asleep."), D(M, "Resting my eyes. Game's not over.")],
             # pass 3 G12 (round 2): she stands over him with the TV light on her, so the moment raises his Want +1 on the
             # way in, recorded on every exit alike (A4d: an accident pays him); her going further pays her
             "Turn the TV off and leave him.", [], record=["mark_asleep_seen"], pay_her=True,   # C1 (LO 2026-11-03)
             entry_eff=[npc_add(M, "want", 1)],
             curious=("Take the beer out of his hand.", "sheets/places/home_hall.md:47", []), ph_name="Mark dozing, TV on",
             plain_after=([P("You lean across him for the remote, and the screen goes black. In the dark his eyes are open a slit, on your tits a foot from his face, and he doesn't close them."),
                           D(M, "Leave it, @player. I'm watching."), ME("Watching what? It's off.")], "Leave him in the dark."))
out += event("home_event_ryan_door", "Ryan's door, a hand's width", "home_hall", S(ALL, "22:00", "00:00"),
             # reader pass 3 b01: Friday nights Kayla is in his room, so the door is not left open for her then
             [here(R, "home_ryan_room"), here("npc_kayla", "home_ryan_room", False), trait("ryan_step", "gte", 7)],
             [P("Ryan's door is open a hand's width. Light under it, music low."), D(R, "Door's open, @player.nickname. If you want.")],
             # C1 (LO 2026-11-03); pass 3 G12 (round 2): the door left open for her is the moment, so his Want +1 on the
             # way in and a record on every exit alike (A4d: an accident pays him); her look pays her
             "Go past.", [], record=["ryan_door_seen"], pay_her=True, entry_eff=[npc_add(R, "want", 1)],
             curious=("Stop and look in.", "sheets/places/home_hall.md:48", []),
             # playtest 2026-11-09 (gate `a pay can happen`): ryan_step 7 is only set from Corruption 60, so the look
             # opens at 60; capped at 39 it could never pay. 79 is this release's top.
             her_cap=79,
             # reader pass 3 b01 (the written no): his "If you want" gets her spoken no and his reaction
             plain_after=([ME("Not tonight, Ryan."), D(R, "Yeah. Course. Night, then."),
                           P("Behind you the music goes up a notch, and his door stays exactly where it is, open a hand's width.")], "Leave him to his music."))
# S6 (LO 2026-11-03, reverses DECISIONS 59's quiet events): "no we dont want nothing happens random events
# anywhere in the game." The four "Nothing happens." events at home are gone.

# ═════════════════════════════════════════════════════════════════════════════
# THE WALK-INS AT HOME (heat proposal B1-B8, DECISIONS 147): walkins.py holds the canvases and the router rules;
# the rules go on their host activities here (ryan_things, in ryan.py, takes its own).
# ═════════════════════════════════════════════════════════════════════════════
import walkins
_left = walkins.attach(out)
assert _left == {"ryan_things"}, _left
out += walkins.CANVASES

# ── exhibition phase 1 (LO, 2026-11-08; exhibition_study/PHASE1_PROPOSAL.md): stretching on the living-room
# floor. Stage 1 (the-heat-ladder.md H1): his look happens to her, and the pay is her letting it go on. Ryan or
# Mark has to be in the room; his Want moves on the way in, whatever she does (H5). Once a day.
_LEG = {"type": "worn_type", "operator": "eq", "value": "leggings"}
_LOWTOP = {"type": "clothing_item", "item_id": "low_top", "operator": "equipped"}
_RY_IN, _MK_IN = here("npc_ryan", "home_living_room"), here("npc_mark", "home_living_room")
_RY_OUT, _MK_OUT = here("npc_ryan", "home_living_room", False), here("npc_mark", "home_living_room", False)
_LA_IN, _LA_OUT = here("npc_laura", "home_living_room"), here("npc_laura", "home_living_room", False)
_E_LO = trait("exhibitionism", "lt", 20)
out += brake_canvas(solo("living_stretch", "Stretch on the living-room floor",
    "Leggings on, a mat by the couch, 20 min. With Ryan, or Mark once he has seen her, in the room and her under Daring, holding the stretch while he looks pays Exhibitionism +1 (cap 19). Once a day.",
    "home_living_room", [
        node("mat", "The mat", [
            P("You roll the mat out by the couch and start the routine, slow: hips up, back arched, one leg and then the other."),
            G(cond(_RY_IN), P("Ryan has stopped pretending to watch the TV. His eyes are on your ass every time you fold forward, and he hasn't blinked."),
              G(cond(_LOWTOP), P("When you come up, the low-cut top has slipped, and his eyes go straight to your tits."))),
            G(cond(_RY_OUT, _MK_IN, flag("mark_saw_her", False)), P("Mark's in the armchair behind his paper. He doesn't look up.")),
            # H7 (the-heat-ladder.md): a man she lives with covers his look at stage 1
            G(cond(_RY_OUT, _MK_IN, flag("mark_saw_her")), P("Mark's paper lowers an inch in the armchair every time you fold forward. When you look round, it goes back up. A minute later it lowers again."),
              G(cond(_LOWTOP), P("When you roll onto your back, the low-cut top gapes. The paper stops halfway up, and stays there."))),
            G(cond(_RY_OUT, _MK_OUT, _LA_IN), P("Mom's on the couch with her wine and the TV. She doesn't look up from her show.")),
            G(cond(_RY_OUT, _MK_OUT, _LA_OUT), P("Nobody's in. Just you, the mat and the ticking clock.")),
        ], [
            go("Hold the stretch.", node="held", mins=20, cond_=cond(_LEG, _E_LO, _RY_IN),
               eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 19}, nadd("npc_ryan", "want", 1)], flags=[fset("stretched_today")]),
            go("Hold the stretch.", node="held", mins=20, cond_=cond(_LEG, _E_LO, _RY_OUT, _MK_IN, flag("mark_saw_her")),
               eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 19}, nadd("npc_mark", "want", 1)], flags=[fset("stretched_today")]),
            go("Finish the routine.", node="done", mins=20, flags=[fset("stretched_today")]),
            go("Roll up the mat.", loc="home_living_room", mins=1),
        ]),
        node("held", "Hold it", [
            G(cond(_RY_IN), P("You hold it a breath longer than the routine says, your ass up in the air in those leggings. When you sit up, he's very busy with the remote and his face is red."),
              D("npc_ryan", "What? I'm watching the game.")),
            G(cond(_RY_OUT, _MK_IN, flag("mark_saw_her")), P("You hold it, longer than the routine says. The paper stays down in his lap. When you sit up, he clears his throat and turns a page he hasn't read."),
              D("npc_mark", "Don't pull anything.")),
            GC(cond(trait("exhibitionism", "lt", 5)), T("He was looking. You held it a second too long.")),
            GC(cond(trait("exhibitionism", "lt", 10)), T("You knew he was looking, and you held it anyway.")),
            GC(cond(trait("exhibitionism", "lt", 15)), T("You held it for him. You'll do the routine here again.")),
            GC(cond(trait("exhibitionism", "lt", 20)), T("Next time you'll hold it longer, and not pretend it's for the stretch.")),
            P("The mat lives behind the couch. Same time tomorrow, if he's in."),
        ], [go("Roll up the mat.", loc="home_living_room", mins=1)]),
        node("done", "The routine", [
            P("You finish the routine and sit back on your heels, warm all over. The mat lives behind the couch."),
            G(cond(_RY_IN), P("Ryan's eyes snap back to the TV the second you look round.")),
            G(cond(_RY_OUT, _MK_IN, flag("mark_saw_her")), P("Mark's paper goes back up.")),
        ], [go("Roll up the mat.", loc="home_living_room", mins=1)]),
    ], prio=2), "stretched_today")

# ── exhibition phase 1 (LO, 2026-11-08): the bridge at each stage's top (the-heat-ladder.md H6). Every act pays only
# to the top of its stage (DECISIONS 188), so 19, 39 and 59 need one step over. Alone in her room, her own beat turns
# what happened into a wish, and that carries her into the next stage (the bathroom mirror; her room is the wardrobe
# room, gate `nothing one-time at the shop or wardrobe`). One time each, fires on entry, sober only
# (a drink's +20 counts in the check, so the window reads 'lt' her next stage and fails while she's Tipsy).
for _lo, _name, _beat, _wish in [
    (19, "The mirror, after Covered",
     [P("In the bathroom mirror you count up who looked at you this week, and how you let every one of them."),
      P("You picture walking out tomorrow with no bra on: your tits loose, your nipples showing through whatever you wear, and every one of them looking.")],
     "Tomorrow you could leave it off."),
    (39, "The mirror, after Daring",
     [P("In the mirror you think about panties like they're the last thing in the way."),
      P("You picture the street tomorrow in a short skirt with nothing under it, the breeze on your bare ass, and whoever's on the street turning round. Your face is hot, and you don't stop picturing it.")],
     "Tomorrow, nothing under it."),
    (59, "The mirror, after Showing",
     [P("You picture yourself naked in front of the mirror, turning slowly, the way you'd turn if someone was watching."),
      P("One man at a time isn't enough any more. You want a room looking, all at once, and you want to know you let them.")],
     "Next time, let a whole room watch."),
]:
    out.append({"id": f"exh_bridge_{_lo + 1}", "name": _name,
        "description": f"One time, at the bathroom mirror, at Exhibitionism {_lo} (sober): her own beat turns the looks into a wish. Exhibitionism set to {_lo + 1}, into the next stage.",
        "trigger": {"location": "home_bathroom", "is_repeatable": False, "priority": 9, "is_active": True,
                    "conditions": cond(flag("opening_done"), trait("exhibitionism", "gte", _lo), trait("exhibitionism", "lt", _lo + 1),
                                       *[here(n, "home_bathroom", False) for n in ("npc_ryan", "npc_mark", "npc_laura")])},
        "nodes": [node("mirror", _name.split(",")[0].replace("The mirror", "The mirror"), [*_beat, T(_wish)],
                       [go("Look a while longer.", loc="home_bathroom", mins=10,
                           # `set`, not `add`: the daily cap counts adds, and this one-time step must not be eaten by it
                           eff=[{"targetType": "player", "trait": "exhibitionism", "op": "set", "value": _lo + 1}],
                           flags=[fset(f"exh_wish_{_lo + 1}")])])]})   # H6: the wish is recorded

text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · HOME (iteration 002, part 2): every house room's alone rows,\n"
        "# the master bedroom at night, the random events at home. sheets/systems/home_life.md,\n"
        "# sheets/places/home_*.md. Source: iterations/002/build_scripts/home.py.\n"
        "# =============================================================================\n")
text += "".join(emit(c) for c in out)
open(__import__("sys").argv[1], "w").write(text)
print("home:", len(out), "canvases")
