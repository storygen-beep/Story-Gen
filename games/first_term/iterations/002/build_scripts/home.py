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
        t["metadata"] = metadata
    return {"id": cid, "name": name, "description": desc, "trigger": t, "nodes": nodes}


def S(days, a, b):
    return [{"weekdays": days, "start_time": a, "end_time": b}]


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
               eff=[add("energy", -30)], flags=[funset("heavy_night")])]),
    ], sched=S(ALL, "19:00", "07:00"), prio=5,
    metadata={"show_when_blocked": True, "cooldown_message": "Too early for bed."}))

out.append(solo("room_nap", "Take a nap", "A daytime nap: two hours, energy +30. Once a day.", "home_ella_room", [
    node("nap", "A nap", [
        POOL(P("You lie down on top of the covers, one arm over your eyes. The light through the curtains goes orange behind your eyelids, and then it's gone."),
             P("You fall face-first into the pillow. Outside, a car door shuts, but you don't hear the next one.")),
    ], [go("Sleep two hours.", loc="home_ella_room", mins=120, eff=[{"targetType": "player", "trait": "energy", "op": "add", "value": 30, "cap": 100}]),
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
STRIP = [{"action": "unequip", "item_id": g} for g in ALL_GARMENTS if g not in ("sneakers", "towel")]
out.append(solo("bathroom_shower", "Take a shower",
    "Hygiene +50, 20 minutes, once a day. Who's near reads who is home. Not while Ryan has the room.",
    "home_bathroom", [
        node("shower", "The shower", [
            P("You lock the door, but the lock sticks halfway like always. You strip and step under the water while it's still cold. You gasp. Then it runs hot down your back and over your tits, and you stand there with your eyes shut and your hands flat on the tiles."),
            G(cond(here(R, "home_ryan_room")), P("Ryan's door opens across the hall. His steps stop outside the bathroom. The handle turns, catches on the lock, and lets go. \"Sorry,\" he says through the door, and doesn't move away from it for a long second.")),
            G(cond(here(M, "home_kitchen")), P("Downstairs, Mark shouts something about the hot water bill. The pipes knock, but you turn it up hotter.")),
            G(cond(here(L, "home_kitchen")), P("Laura's voice floats up the stairs. \"Leave some hot water, sweetheart!\"")),
            POOL(P("You soap yourself slowly, all of you, because the door's locked. Nobody can see, but you take your time like someone could. The steam fogs the glass until the room is white."),
                 P("You tip your head back and let the water fill your mouth. It runs off your chin, down between your tits. You should be quick, but you stay until your fingertips wrinkle."),
                 P("You wash your hair twice because it feels good. The water drums on your shoulders. For ten minutes the house can't get at you.")),
        ], [go("Wrap up in a towel.", loc="home_bathroom", mins=20,
               eff=[{"targetType": "player", "trait": "hygiene", "op": "add", "value": 50, "cap": 100}],
               wardrobe=STRIP + [{"action": "equip", "item_id": "towel"}])]),
    ], conds=[here(R, "home_bathroom", False)], prio=5, max_day=1))

out.append(solo("bathroom_mirror", "Look in the mirror", "The bathroom mirror: one line by what she has on, slot by slot.",
    "home_bathroom", [
        node("mirror", "The mirror", [
            GC(cond(TOWEL), P("Wet hair, pink skin, the towel tucked over your tits, stopping at the top of your thighs. One tug and it's on the floor. You look at the girl in the mirror. She looks right back.")),
            GC(cond(*NAKED), P("Naked. You turn sideways, then the other way. You cup your tits and let them go. The mirror is small, so you stand on your toes to see the rest of you.")),
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
            GC(cond(*UNDIES), P("Bra and panties in the hall, where every door off it could open.")),
            GC(cond(SKIRT, slot("underwear", False)), P("Nothing under the skirt, and the stairs are right there. Anyone at the bottom looking up gets everything.")),
            GC(cond(SKIRT, slot("underwear")), P("The skirt is short enough that the stairs are a problem. Anyone at the bottom looking up gets your panties. You tug it down. It doesn't help.")),
            # Iteration 002, part 8 (reader): the top only when there is one; "good girl" only in plain clothes.
            GC(cond(slot("bra", False), slot("top"), *COVERED), P("No bra. Your nipples show through your top, plain as anything in the hall light.")),
            GC(cond(slot("bra", False), slot("dress"), *COVERED), P("No bra under it. Your nipples show through the fabric, plain as anything in the hall light.")),
            GC(cond(*COVERED, {"type": "worn_corruption", "operator": "eq", "value": 0}, {"type": "worn_type", "operator": "neq", "value": "thin_top"}),
               P("Covered, neat, nothing anyone could say a word about. You look like Laura's good girl.")),
            GC(cond(*COVERED), P("Covered, technically. Nothing Laura would have bought you.")),
            GC(cond(*ANY), P("Half dressed in the hall. You check the doors before you check the mirror.")),
        ], [go("Go on.", loc="home_hall", mins=2)]),
    ], prio=2))

# ═════════════════════════════════════════════════════════════════════════════
# THE KITCHEN (home_kitchen.md): the drawer (A1-13), and the meals alone
# ═════════════════════════════════════════════════════════════════════════════
out.append(solo("kitchen_drawer", "Look through the drawer", "Reads rent_carried, knows_mark_debt and the letter home. Writes nothing.",
    "home_kitchen", [
        node("drawer", "The drawer", [
            P("The drawer by the fridge sticks, and you have to lift it to open it. Takeaway menus, dead batteries, a roll of tape, and under all of it the letters nobody wants to open."),
            G(cond(flag("rent_carried")), P("On top, a new one. Vance's handwriting on the envelope, already torn open. Inside, one line: OUTSTANDING, and a figure, underlined twice. Your short week is in that number.")),
            G(cond(flag("rent_carried", False), flag("knows_mark_debt", False)), P("Bills. Gas, water, the council, a phone contract in Mark's name. Two of them say FINAL in red, but nobody's opened those.")),
            G(cond(flag("rent_carried", False), flag("knows_mark_debt")), P("Three envelopes from Vance, all opened, all folded back the way they came. The top one says FINAL in red. Now you know what they're about: Mark owes him more than the rent, a lot more.")),
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
PASSERS = [[here(M, "home_kitchen")], [here(R, "home_ryan_room"), here(M, "home_kitchen", False)]]
out.append(solo("living_couch", "Lie on the couch",
    "Alone in the room. Who passes through reads what she has on; exhibitionism +1 once a day if Daring, in her underwear, and someone's home to pass.",
    "home_living_room", [
        node("couch", "The couch", [
            P("You stretch out on the couch, one knee up, the remote on your stomach."),
            G(cond(*UNDIES, here(M, "home_kitchen")), P("Mark comes through from the kitchen with a beer and stops behind the couch. You're in your underwear. He doesn't say cover up. He stands there drinking, looking down the length of you, and then he goes, slowly.")),
            G(cond(*UNDIES, here(R, "home_ryan_room")), P("Ryan comes down for a drink and sees you and stops on the last stair. \"Jesus, @player.nickname.\" He goes to the kitchen without looking again. He takes a long time getting that drink.")),
            G(cond(SKIRT), P("With your knee up, the skirt is nowhere. Anybody coming in from the hall would see straight up it.")),
            G(cond(*COVERED), P("Nobody looks twice at a girl on a couch in her clothes.")),
        ], [*[c for who in PASSERS for c in brake(
                go("Stay a while.", loc="home_living_room", mins=45, flags=[fset("couch_seen")],
                   cond_=cond(DARING, *UNDIES, *who),
                   eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 59}]),
                "couch_seen")],
            go("Get up.", loc="home_hall", mins=10)]),
    ], conds=LIVING_EMPTY, prio=3))

out += brake_canvas(solo("living_tv", "Watch TV",
    "TV alone: 60 min, energy +5 (home_life.md:69).",
    "home_living_room", [node("tv", "TV", [
        POOL(P("You flick through the channels and land on something with a lot of shouting. An hour goes by without asking, but you don't mind."),
             P("A cooking show, then an old film, then you've lost track. The couch has a dent exactly your shape.")),
    ], [go("Watch an hour.", loc="home_living_room", mins=60, flags=[fset("watched_tv")],
           eff=[{"targetType": "player", "trait": "energy", "op": "add", "value": 5, "cap": 100}]),
        go("Turn it off.", loc="home_hall")])],
    sched=S(ALL, "07:00", "02:00"), conds=LIVING_EMPTY), "watched_tv")

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
            P("Her wardrobe smells like her perfume. Work blouses, a winter coat, and at the back, in dry-cleaner plastic, dresses she hasn't worn since before Mark. Short ones. Tight ones. A red one with no back at all."),
            G(cond({"type": "clothing_item", "item_id": "laura_blue_dress", "operator": "owned"}, {"type": "clothing_item", "item_id": "laura_blue_dress", "operator": "unequipped"}),
              P("There's the gap on the rail where the blue one hung. It's in your room now. She gave it to you like it was nothing, and there's a whole rail of nothing back here.")),
            G(cond({"type": "clothing_item", "item_id": "laura_blue_dress", "operator": "equipped"}),
              P("There's the gap on the rail where the blue one hung. You're wearing it.")),
            POOL(P("You hold the red one against yourself in her long mirror. It would barely cover your ass. Laura wore this once, somewhere, for someone, and you stand there trying to picture her face when she did."),
                 P("In the drawer under the dresses: stockings, still in the packet, and a black lace bra that is not a mom's bra. You hold it up to your chest in her mirror and your nipples go hard."),
                 P("A photo, tucked in the frame of her mirror: Laura at twenty-something on someone's shoulders at a concert, her top off, laughing. You put it back exactly where it was.")),
        ], [go("Put it all back.", loc="home_hall", mins=20)]),
    ], conds=[nobody("home_master_bedroom")], prio=3, max_day=1))

out.append({"id": "master_asleep", "name": "Ease the door open",
    "description": "The door's 'Ease the door open' at night: one screen naming only who is asleep, then back to the hall (home_master_bedroom.md:47-54, Q58). Reached only by the door.",
    "trigger": {"location": "home_master_bedroom", "is_repeatable": True, "priority": 1, "is_active": True,
                "substitution_only": True},
    "nodes": [node("dark", "Their room at night", [
        P("You ease the handle down and open the door a hand's width. The room is dark and warm, and it smells of sleep."),
        G(cond(here(L, "home_master_bedroom"), here(M, "home_master_bedroom"), tod("22:00", "07:00")),
          P("Laura's asleep on her side, curled toward the wall, one bare shoulder out of the covers. Mark's on his back beside her, snoring.")),
        G(cond(here(L, "home_master_bedroom"), here(M, "home_master_bedroom", False), tod("22:00", "07:00")),
          P("Laura's asleep on her side, one bare shoulder out of the covers. Mark's half of the bed is empty.")),
        G(cond(here(M, "home_master_bedroom"), here(L, "home_master_bedroom", False), tod("22:00", "07:00")),
          P("Mark's asleep on his back, one arm flung across the bed. Laura's half is empty, the covers thrown back.")),
        P("You stand in the gap long enough to hear the breathing. Nobody stirs."),
    ], [go("Close the door.", loc="home_hall", mins=2),
        go("Go to the bed. (Needs Hungry)", node="hl_hungry", swl=True, cond_=cond(HUNGRY))]),
        hungry_node("home_hall")]})

# ═════════════════════════════════════════════════════════════════════════════
# THE GARAGE (home_garage.md): his things (A1-13, A1-21), the washer alone
# ═════════════════════════════════════════════════════════════════════════════
out.append(solo("garage_things", "Go through Mark's things",
    "When Mark is out. The debt papers: reads rent_carried; the loan is named only after knows_mark_debt. Once a day.",
    "home_garage", [
        node("bench", "Mark's bench", [
            P("His workbench, his radio, a fridge of beer that hums. The filing box under the bench has a padlock, and the key is on a nail above it, which tells you exactly how much Mark thinks of everybody in this house."),
            G(cond(flag("rent_carried")), P("On top of the folders, a new page in Mark's square capitals, a figure crossed out and written again, bigger. Your short week is in there. He's added it in red.")),
            G(cond(flag("rent_carried", False), flag("knows_mark_debt", False)), P("Folders of bank letters, payslips, the car's papers. Columns of numbers in his capitals that never seem to add up to enough.")),
            G(cond(flag("rent_carried", False), flag("knows_mark_debt")), P("A loan agreement with Vance's signature on every page, the house on the first one. Mark's been paying it off for years and the number at the bottom has barely moved.")),
            P("Under the folders, a magazine. Girls on the cover, bent over. You put it back where it was, square to the edge, the way he'd notice."),
        ], [go("Lock it up again.", loc="home_hall", mins=15)]),
    ], conds=[here(M, "home_garage", False)], prio=3, max_day=1))

out += brake_canvas(solo("garage_laundry", "Do your laundry",
    "The washer, alone: 30 min, energy −5 (home_life.md:71). With Mark here it is in his hub.",
    "home_garage", [node("washer", "The washer", [
        P("You sort your basket on the garage floor, darks and lights, and feed the old machine until it shudders and starts. It sounds like it's dying, but it always sounds like that."),
    ], [go("Load it.", loc="home_garage", mins=30, flags=[fset("did_laundry")], eff=[add("energy", -5)],
           costs=[{"trait": "energy", "value": 5}]),
        go("Later.", loc="home_hall")])],
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
        G(cond(tod("07:00", "19:00")), P("You drag the lounger into the one patch of sun and lie back with your eyes shut. The grass smells cut. The fence is low.")),
        G(cond(tod("19:00", "21:00")), P("You drag the lounger out and lie back in the last of the light, eyes shut. The grass smells cut. The fence is low.")),
        GC(cond(*TOPLESS), P("Topless, on your front, the sun on your back and the side of your tits pressed flat to the lounger.")),
        GC(cond(*BRA_ONLY), P("Your bra and nothing over it, the sun on your stomach.")),
        GC(cond(*ANY), P("In what you have on, face to the sky.")),
        G(cond(MARK_SEES), P("The garage door is open. Mark's radio is on in there, and once the radio goes quiet you know he's standing in the doorway.")),
        G(cond(RYAN_SEES), P("Ryan's window is open above you. His music stops.")),
    ], [
        *brake(go("Lie in the sun an hour.", loc="home_garden", mins=60, flags=[fset("sunned")], eff=[SUN_EFF],
                  cond_=cond(here(M, "home_garage", False), here(R, "home_ryan_room", False))), "sunned"),
        *brake(go("Lie in the sun an hour. Let Mark look.", loc="home_garden", mins=60, flags=[fset("sunned")],
                  cond_=cond(MARK_SEES), eff=[SUN_EFF, npc_add(M, "want", 1)]), "sunned"),
        *brake(go("Lie in the sun an hour. Wave up at Ryan.", loc="home_garden", mins=60, flags=[fset("sunned")],
                  cond_=cond(RYAN_SEES, here(M, "home_garage", False)), eff=[SUN_EFF, npc_add(R, "warmth", 1)]), "sunned"),
        *brake(go("Show off for whoever's looking.", node="sun_seen", mins=60, flags=[fset("sunned")],
                  cond_=cond(DARING, *TOPLESS, MARK_SEES),
                  eff=[SUN_EFF, {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 59}]), "sunned"),
        *brake(go("Show off for whoever's looking.", node="sun_seen", mins=60, flags=[fset("sunned")],
                  cond_=cond(DARING, *TOPLESS, RYAN_SEES, here(M, "home_garage", False)),
                  eff=[SUN_EFF, {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 59}]), "sunned"),
        go("Play up to Ryan's window.", node="sun_ryan", cond_=cond(RYAN_SEES, CURIOUS, trait("ryan_step", "gte", 3))),
        go("Play up to Mark in the garage door.", node="sun_mark", cond_=cond(MARK_SEES, CURIOUS, trait("mark_step", "gte", 3))),
        go("Go in.", loc="home_hall"),
    ]),
    node("sun_seen", "Seen", [
        P("You stay exactly as you are and let whoever's looking look. Your skin is hot and it isn't only the sun."),
    ], [go("Go in.", loc="home_hall")]),
    node("sun_ryan", "Ryan's window", [G(cond(RYAN_SEES), P("His window is open above you. He isn't pretending to look at his screen any more."))], [
        *brake(go("Stretch out for him.", node="sun_ryan_tease", flags=[fset("sunned")], eff=[npc_add(R, "want", 1)],
                  cond_=cond(*BRA_ONLY)), "sunned"),
        *brake(go("Call him down with the sun lotion.", node="sun_ryan_touch", flags=[fset("sunned")],
                  cond_=cond(BOLD, trait("ryan_step", "gte", 7)),
                  eff=[npc_add(R, "want", 1), {"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 59}]), "sunned"),
        go("Not today.", loc="home_garden")]),
    node("sun_mark", "The garage door", [G(cond(MARK_SEES), P("Mark's in the garage door with a beer, and he hasn't gone back in."))], [
        *brake(go("Stretch out for him.", node="sun_mark_tease", flags=[fset("sunned")], eff=[npc_add(M, "want", 1)],
                  cond_=cond(*BRA_ONLY)), "sunned"),
        *brake(go("Let him pay to look.", node="sun_mark_paid", flags=[fset("sunned"), fset("mark_paid_look")],
                  cond_=cond(BOLD, trait("mark_step", "gte", 7), flag("mark_paid_touch"), flag("mark_arrangement"), flag("sunned", False)),
                  eff=[{"targetType": "player", "trait": "money", "op": "add", "value": 20, "clamp": False}, npc_add(M, "want", 1),
                       {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 59}]), "mark_paid_look"),
        go("Not today.", loc="home_garden")]),
    node("sun_ryan_tease", "Ryan's window", [placeholder("sheets/people/npc_ryan.md:104", "Ryan, the garden: tease (Curious, Ryan A 4)")],
         [go("Done.", loc="home_garden", mins=30)]),
    node("sun_ryan_touch", "The sun lotion", [placeholder("sheets/people/npc_ryan.md:104", "Ryan, the garden: touch (Bold, Ryan A 8)")],
         [go("Done.", loc="home_garden", mins=30)]),
    node("sun_mark_tease", "The garage door", [placeholder("sheets/people/npc_mark.md:110", "Mark, the garden: tease (Curious, Mark A 3)")],
         [go("Done.", loc="home_garden", mins=30)]),
    node("sun_mark_paid", "The paid look", [placeholder("sheets/people/npc_mark.md:110", "Mark, the garden: the paid look (Bold, Mark A 7)")],
         [go("Done.", loc="home_garden", mins=30)]),
]
out.append(solo("garden_sun", "Lie in the sun",
    "The lounger: 60 min, energy +5; Daring and seen, exhibitionism +1 (home_garden.md:29-34). Mark sees from the garage door (his Saturday row), Ryan from his window (his weekend row). Their tease and touch lines are placeholders.",
    "home_garden", sun_nodes, prio=3))

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
                P("You sit on the front step with your knees up and watch the street. A car goes by slow. A guy walking his dog looks over, and keeps looking."),
                P("Two doors down a man is washing his car, and he stops washing it when you sit down."))),
            GC(cond(tod("21:00", "07:00")), P("The street is dark and quiet, the porch light on its timer. A car passes now and then, slow, headlights sliding over you, but nobody stops.")),
            G(cond(SKIRT, slot("underwear")), P("With your knees up in this skirt, anyone passing can see your panties. You could put your knees down. You don't, for a while.")),
            G(cond(SKIRT, slot("underwear", False)), P("There's nothing under the skirt. The air on the step is cool between your legs, and you keep your knees exactly where they are, because one inch is the whole street's business.")),
            G(cond(here("npc_vance", "vance_house")), P("Next door, Vance lowers his paper on the porch and watches you over the top of it. He doesn't wave.")),
        ], [go("Go back in.", loc="home_hall", mins=20)]),
    ], prio=2))

# ═════════════════════════════════════════════════════════════════════════════
# RANDOM EVENTS AT HOME (home_hall.md:36-49, Q59): 1 in 4 on entering the hall, kitchen, living
# room or bathroom, one a day. Each shows only when its person's row puts them there; with nobody
# there it is the room's quiet line. One brake flag across all of them, read 24 hours.
# ═════════════════════════════════════════════════════════════════════════════
def event(cid, name, loc, sched, conds, blocks, plain, raise_eff, curious=None, bold=None, ph_name=None):
    exits = [go(plain, loc=loc, mins=2, eff=raise_eff, flags=[fset("home_event")])]
    nodes = []
    for kind, spec, gate in (("curious", curious, [CURIOUS]), ("bold", bold, [BOLD])):
        if not spec:
            continue
        label, ref, extra = spec
        exits.append(go(label, node=f"ev_{kind}", cond_=cond(*gate, *extra), eff=raise_eff, flags=[fset("home_event")]))
        nodes.append(node(f"ev_{kind}", label.rstrip("."), [placeholder(ref, f"{ph_name or name}: {kind}")], [go("Go on.", loc=loc, mins=2)]))
    c = {"id": cid, "name": name, "description": f"Random event at home (home_hall.md): {name}. 1 in 4, one a day.",
         "trigger": {"location": loc, "is_repeatable": True, "priority": 4, "is_active": True,
                     "trigger_mode": "random", "chance": 0.25, "conditions": cond(*conds)},
         "nodes": [node("event", name, blocks, exits)] + nodes}
    if sched:
        c["trigger"]["schedules"] = sched
    return brake_canvas(c, "home_event")


out += event("home_event_ryan_towel", "Ryan out of the shower", "home_hall", S([0, 1, 2, 3, 4], "06:45", "07:30"),
             [here(R, "home_bathroom"), flag("opening_done")],
             [P("The bathroom door opens as you pass and Ryan steps out in a towel, wet, steam behind him. You nearly walk into his chest."),
              D(R, "Sorry."), ME("Sorry.")],
             "Step round him.", [npc_add(R, "want", 1)],
             curious=("Walk past slowly.", "sheets/places/home_hall.md:44", []),
             bold=("Let him look.", "sheets/places/home_hall.md:44", [trait("ryan_step", "gte", 3)]))
out += event("home_event_laura_robe", "Laura's robe", "home_kitchen", S([0, 1, 2, 3, 4], "06:30", "08:00"),
             [here(L, "home_kitchen"), flag("opening_done")],
             [P("Laura reaches up for the cereal on the top shelf and her robe slips open at the front. She ties it again fast, pink to the ears."),
              D(L, "Don't look at me like that. It's early.")],
             "Look away.", [npc_add(L, "warmth", 1)],
             curious=("Don't look away.", "sheets/places/home_hall.md:45", []))
out += event("home_event_mark_reach", "Mark reaching past", "home_kitchen", S([6], "08:00", "22:00"),
             [here(M, "home_kitchen")],
             [P("Mark reaches over you for a mug off the shelf, close, his arm past your face, his chest at your back for a second longer than the mug needs.")],
             "Duck out of his way.", [npc_add(M, "want", 1)],
             curious=("Lean back into him.", "sheets/places/home_hall.md:46", []))
out += event("home_event_mark_asleep", "Mark asleep, TV on", "home_living_room", S([0, 1, 2, 3, 4, 5], "00:00", "02:00"),
             [here(M, "home_living_room")],
             [P("Mark is slumped on the couch with the TV still on, eyes half shut, a beer going warm in his hand, his head tipped back.")],
             "Turn the TV off and leave him.", [npc_add(M, "want", 1)],
             curious=("Take the beer out of his hand.", "sheets/places/home_hall.md:47", []), ph_name="Mark dozing, TV on")
out += event("home_event_ryan_door", "Ryan's door, a hand's width", "home_hall", S(ALL, "22:00", "00:00"),
             [here(R, "home_ryan_room"), trait("ryan_step", "gte", 7)],
             [P("Ryan's door is open a hand's width. Light under it, music low.")],
             "Go past.", [npc_add(R, "want", 1)],
             curious=("Stop and look in.", "sheets/places/home_hall.md:48", []))
QUIET = {"home_hall": "Nothing happens. The fridge hums downstairs, and the stairs creak once on their own.",
         "home_kitchen": "Nothing happens. The fridge hums.",
         "home_living_room": "Nothing happens. The cushions still have somebody's shape in them.",
         "home_bathroom": "Nothing happens. The tap drips."}
for loc, line in QUIET.items():
    out += event(f"home_event_quiet_{loc.replace('home_', '')}", "The house, quiet", loc, None,
                 [nobody(loc), flag("opening_done")], [P(line)], "Go on.", [])

text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · HOME (iteration 002, part 2): every house room's alone rows,\n"
        "# the master bedroom at night, the random events at home. sheets/systems/home_life.md,\n"
        "# sheets/places/home_*.md. Source: iterations/002/build_scripts/home.py.\n"
        "# =============================================================================\n")
text += "".join(emit(c) for c in out)
open(__import__("sys").argv[1], "w").write(text)
print("home:", len(out), "canvases")
