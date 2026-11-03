"""Jake — steps 2-3 (Jake B 2-3; step 1 is Zoe's first party, step 4 is Laura's step 5), the date
pickup, the Saturday goodnight (the repeat), his hubs. Source: sheets/scenes/jake_*.md, people/npc_jake.md."""
from canv import *
from tomlw import tod, wd
from sheetbeats import beat
CURIOUS = trait("corruption", "gte", 20)
BOLD = trait("corruption", "gte", 40)

J = "npc_jake"
R = "npc_ryan"
L = "npc_laura"
out = []

def done(n):
    return fset(f"jake_0{n}_done")

SKIRT = {"type": "worn_type", "operator": "eq", "value": "short_skirt"}
LAURA_DRESS = {"type": "clothing_item", "item_id": "laura_blue_dress", "operator": "equipped"}
ANY_ = [{"type": "worn_exposure", "operator": "gte", "value": 0}]   # always true: a chain's else
ZOE_DRESS = {"type": "clothing_item", "item_id": "zoe_party_dress", "operator": "equipped"}
NO_CURFEW = cond(NO_CURFEW_ITEM)

# ── step 2 · Jake B 2 · the kiss on the quad ──
out.append({
    "id": "jake_02_kiss_on_the_quad", "name": "The kiss on the quad",
    "description": "Jake step 2 (Jake B 2): a kiss in front of his team; the first date booked. Ryan's Warmth -5 (choosing Jake).",
    "trigger": step_trigger(J, 2, retry_days=2),
    "nodes": [
        node("team", "His team", [
            P("Jake's on the grass with four guys from the team, all of them in the same jacket. He sees you crossing the quad and gets up and jogs over, and puts his arm round you, and walks you back to them like he's bringing a trophy."),
            D(J, "Guys, this is @player."),
            G(cond(SKIRT), D(J, "Guys. Look at her."), P("He says it to the team, and they look.")),
        ], [
            go("\"Hi.\"", node="kiss", mins=3, cond_=cond(trait("corruption", "gte", 20))),
            go("\"Hi.\"", node="kiss", mins=3, cond_=cond(trait("corruption", "lt", 20), trait("exhibitionism", "gte", 20))),
            go("\"Not now.\"", node="no", mins=2),
        ]),
        node("kiss", "In front of them", [
            P("He kisses you right there, in front of all of them, his hand low on your back, low enough that it's on your ass by the end. Somebody whistles. You feel him hard against your hip, but you move his hand back up to your waist. Not in front of them. Not yet. He pulls back grinning, red to the ears."),
            D(J, "Again. They missed it."),
            T("He wants them to see you're his. You want them to see too."),
        ], [go("\"Again.\"", node="ask", mins=3, eff=[add("exhibitionism", 3, cap=79)])]),
        node("ask", "Saturday", [
            P("You kiss him longer this time, long enough that the guys stop whistling and start looking at the grass."),
            ME("Saturday. Pick me up at the door."),
            D(J, "Saturday."),
        ], [go("\"Saturday.\"", loc="quad", mins=5, consumes=True,
               eff=[setv("jake_step", 2)], flags=[done(2), fset("jake_date_booked")])]),
        no_node("no", [D(J, "Later, then. I'll be here."), P("The guys jeer at him. He shoves the nearest one and grins after you all the way across the quad.")], "quad", 2,
                label="Leave him with the guys."),
    ]})

# ── step 3 · Jake B 3 · my boyfriend (the voice sample; every screen as signed) ──
out.append({
    "id": "jake_03_my_boyfriend", "name": "My boyfriend",
    "description": "Jake step 3 (release 1; built Jake 3 and Jake 4 = Laura 5 merged): Saturday night at the front door after a date; she names him to the house; Ryan opens the door; Laura watches from the dark living room.",
    "trigger": step_trigger(J, 3, retry_days=7),
    "nodes": [
        node("porch", "The porch", [
            P("Jake walks you up to the porch and stops under the light. The front of the house is dark. He looks past you at the dark windows. \"Is anyone up?\" He sounds like he hopes so. \"Nobody,\" you say. \"Not yet.\" Ryan's window is lit, right beside the porch. He's home. You want him to look. \"Shame,\" Jake says. \"I want them to see you're mine, @player.\" His hand slides down your back and settles on your ass. You should move it, but you like being shown off. He leans in, and his mouth stops an inch from yours."),
        ], [
            go("Kiss him.", node="rail", mins=3),
            go("\"Goodnight, Jake.\"", node="no", mins=2),
        ]),
        node("rail", "The rail", [
            P("You kiss him first, right there under the porch light. Jake makes a low sound and lifts you onto the rail like you weigh nothing. Your legs lock round his waist. His hands sit on your hips, then slide down to grab your ass. \"God, @player,\" he breathes into your mouth. It gets hungry and loud, all teeth and breath. The rail creaks every time he pulls you closer. Anyone inside could hear it, but you don't care. You want more of his mouth. Then, behind you, the lock turns."),
        # LO 2026-11-03: Want pays for what happened, never for a no. Ryan sees her on the rail when the door opens, so
        # his Love -15 and Want +5 sit on the way in, not on her goodnight
        ], [go("\"Don't stop.\"", node="ryan", mins=3, eff=[nadd(R, "warmth", -15), nadd(R, "want", 5)])]),
        node("ryan", "Ryan", [
            P("The front door opens behind you. Ryan stands in the doorway and stops dead. You're on the porch rail with your legs locked round Jake's waist, kissing him. Jake's hands are full of your ass. You don't climb down. You look straight at Ryan over Jake's shoulder and hold it. \"Ryan, this is Jake. My boyfriend.\" Ryan's jaw goes tight. His eyes drop to Jake's hands on you, then come back to your face. \"Great.\" Jake grins over his shoulder, not getting it. \"Your brother hates me.\" *Good. Look all you want, Ryan.* Ryan steps back inside without another word. The door slams hard."),
            G(cond(here_at(L, "home_living_room")), P("Behind Jake's shoulder, in the dark living-room window, a shape on the couch hasn't moved.")),   # pass 4: only while she is on it
        ], [go("\"Goodnight, Jake.\"", node="after", mins=5)]),  # Ryan's -15 / +5 moved onto "Don't stop." (the moment he sees her)
        node("after", "Next Saturday", [
            P("Jake goes off down the path, whistling. You let yourself in."),
            # pass 4 reader (true on every visit): the window runs to 00:00 and this screen is 11 minutes in; at midnight
            # Laura leaves the living room (the hall, or asleep in her room), so where she is picks the line
            GC(cond(here_at(L, "home_living_room")),
               P("The living room is dark. Laura is on the couch with her knees pulled up and her hand at her throat, and she doesn't pretend she wasn't watching.")),
            GC(cond(here_at(L, "home_hall")),
               P("The hall lamp is off. Laura is on the bench by the coats with her knees pulled up and her hand at her throat. She came out of the dark living room when the door slammed, and she doesn't pretend she wasn't watching.")),
            GC(cond(*ANY_), P("The living room is dark and empty. Down the hall Laura's door is shut. The couch cushion at her end is still dented.")),
            *[blk for where in ("home_living_room", "home_hall") for blk in (
                G(cond(here_at(L, where)), D(L, "Was he any good?")),
                G(cond(here_at(L, where), LAURA_DRESS), ME("Better in your dress.")),
                G(cond(here_at(L, where), {"type": "clothing_item", "item_id": "laura_blue_dress", "operator": "unequipped"}), ME("Better with you watching.")),
                G(cond(here_at(L, where)), P("She makes a sound in her throat, but she doesn't get up.")))],
            P("You go down the hall. Ryan's door is shut, and his light is on under it. You stand outside it a second. You don't knock, but you don't move either. You wanted him to see. You said Jake's name to his face on purpose, and you're not sorry. Not even a little. Jake will want a next Saturday. You already know it. Your phone buzzes in your hand. It's Jake: \"Next Saturday?\" Under Ryan's door, the light goes out."),
            D(R, "Who's Jake, @player.nickname? Really. Who is he?"),
            P("He says it through the door, low, but he doesn't open it."),
        ], [go("Go to bed.", loc="home_ella_room", mins=5, consumes=True,
               eff=[setv("jake_step", 3)], flags=[done(3), funset("jake_date_booked")])]),
        node("no", "A kiss on the cheek", [
            P("You kiss his cheek, quick, and step back before he can turn it into more. Jake wanted the porch rail. It's all over his face, but he lets it go. \"Okay, @player. Next Saturday, then?\" He's disappointed, and somehow he's grinning harder than before. \"Next Saturday,\" you say, and your stomach flips. Jake walks backwards down the path, still grinning at your door."),
        ], [go("Go in.", loc="home_hall", mins=3, retry=7, flags=[funset("jake_date_booked")])]),
    ]})

# ── the date: Jake picks her up at the door on a booked Wednesday or Saturday (W8, LO 2026-11-03: two dates a
#    week); the curfew refuses it ──
BACK_AT_11 = [(("19:00", "20:00"), 240), (("20:00", "21:00"), 180), (("21:00", "19:00"), 120)]   # catch-all (A4-02)
WENT_TONIGHT = {"type": "hours_since_flag", "subject": "player", "flag_key": "jake_date_went", "operator": "lt", "value": 6}
BOOKED_THIS_WEEK = {"type": "hours_since_flag", "subject": "player", "flag_key": "jake_date_booked", "operator": "lt", "value": 168}
out.append({
    "id": "jake_date_pickup", "name": "Jake's at the door",
    "description": "A booked Wednesday or Saturday: Jake picks her up; dinner, a film, the walk back. Lands her at the front door after eleven (where his steps and the goodnight play). The curfew refuses it (SYSTEMS §12).",
    "trigger": {"location": "home_front_door", "npc": J, "requires_npc": J, "is_repeatable": True, "priority": 6, "is_active": True,
                "max_triggers_per_day": 1,
                "schedules": [{"weekdays": [2, 5], "start_time": "19:00", "end_time": "21:00"}],
                "conditions": cond(flag("jake_date_booked"), BOOKED_THIS_WEEK, flag("jake_met"))},
    "nodes": [
        node("door", "The doorbell", [
            P("The doorbell goes. Jake's on the step in a clean shirt with his hair still wet, holding his car keys like a man in an advert."),
            G(cond(LAURA_DRESS), D(J, "Whoa. Okay. Everyone's going to be looking at you tonight.")),
            G(cond(SKIRT), P("His eyes go down your legs and stay there.")),
            D(J, "Ready? I booked the place with the candles. Don't laugh."),
            G(CURFEW_ON, T("You're grounded. Laura would know by morning, she always does.")),
        ], [
            # C4 (LO 2026-11-03): dirty, the date doesn't happen, and he says why
            go("Go out with him.", node="date", mins=10, cond_=cond(*NO_CURFEW["items"], trait("hygiene", "gte", 30)), flags=[fset("jake_date_went"), funset("jake_stood_up")]),
            go("Go out with him.", node="date", mins=10, cond_=cond(*NO_CURFEW["items"], trait("hygiene", "lt", 30), flag("hygiene_off")), flags=[fset("jake_date_went"), funset("jake_stood_up")]),
            go("Go out with him.", node="stink", mins=2, cond_=cond(*NO_CURFEW["items"], trait("hygiene", "lt", 30), flag("hygiene_off", False)), flags=[funset("jake_date_booked")]),  # Q73 (iteration 002: pulled forward from part 5 so Laura C 5 has its flag)
            go("\"I'm grounded. Next week.\"", loc="home_front_door", mins=5, cond_=CURFEW_ON, flags=[funset("jake_date_booked")]),
            go("\"Not tonight, Jake.\"", node="no", mins=2),
        ]),
        node("date", "The date", [
            POOL(
                P("Dinner at the place with the candles. He talks about the team, and the coach, and a guy who threw up on the bus, and you laugh in the right places. He holds your hand on the table where the whole restaurant can see it. Afterwards he drives you home the long way, one hand on the wheel and one on your knee."),
                P("A film you don't watch. He has his arm round you from the trailers, and his hand on your knee from the first scene, and every time somebody comes down the aisle he kisses you so they'll see. He drives you home through the park, slowly."),
                pid="jake_date_lines"),
            # scene reader b03 (2026-11-03): the not-yet on the body (H4.3)
            P("His hand on your knee squeezes, and his thumb strokes the inside of it, but it never goes higher up your thigh. Not in public. Not yet."),
            D(J, "You're the best-looking girl in this whole town, you know that? Everyone was looking."),
        ], [go("Let him drive you home.", loc="home_front_door", mins=m, cond_=cond(tod(a, b))) for (a, b), m in BACK_AT_11]),
        node("stink", "Not like that", [
            P("He leans in to kiss you hello and stops halfway, his nose wrinkling."),
            D(J, "Gorgeous. Did you shower today? I booked the place with the candles. Go wash. I'll text you."),
            P("He goes back to his car. You can smell it on yourself now too."),
        ], [go("Close the door.", loc="home_front_door", mins=2)]),
        node("no", "Not tonight", [D(J, "Oh. Okay. Next week?"), P("He stands on the step for a second with his keys, then goes. He texts you from the car before he's even started it.")],
             [go("Close the door.", loc="home_front_door", mins=2, flags=[funset("jake_date_booked")])]),
    ]})

# ── step 4 · Sneak him in (jake_04_sneak_him_in.md, signed 2026-11-01), the top step: after a date, Sat 22:00-00:00,
#    it takes the date-end slot; up to her room past midnight. His late column (signed). ──
_t4 = step_trigger(J, 4, retry_days=7)
_t4["conditions"]["items"].append(WENT_TONIGHT)
_t4["priority"] = 9
RYAN_PAST_5 = trait("ryan_step", "gte", 5)
DOOR_UNLOCKED = flag("her_door_unlocked")
out.append({
    "id": "jake_04_sneak_him_in", "name": "Sneak him in",
    "description": "Jake step 4, the top step (release 1): she sneaks him up to her room; her headboard on Ryan's wall; the keyless door. Sets jake_first_time; Ryan's Lust +5.",
    "trigger": _t4,
    "nodes": [
        node("door", "Come up", [
            P("Jake walks you up to the porch and stops under the light. You don't let go of his hand. You open the front door and pull him in after you."),
            ME("Come up."),
            # reader pass 4 b4: Laura waits up in the living room Sat 22:00-00:00; the sneak-in passes her doorway
            G(cond(here_at(L, "home_living_room")), P("The living-room doorway flickers blue. Mom's on the couch in the dark with the TV on low, waiting up, her back to the hall. You get him past it on your toes, his hand on your ass the whole way.")),
            P("In the dark hall he catches your hip and his breath is hot on your ear."),
            D(J, "Your room. Now."),
        ], [go("\"Quiet.\"", node="bed", mins=5),
            go("\"Goodnight, Jake.\"", node="next_sat", mins=2)]),
        node("next_sat", "Next Saturday", [
            D(J, "Next Saturday, then. Your room."),
            P("He grins and walks backwards down the path, all the way to the car."),
        ], [go("Go in.", loc="home_hall", mins=2, retry=7, flags=[funset("jake_date_booked")])]),
        node("bed", "Your room", [P(beat("jake_04_sneak_him_in", "bed")),
            VID("a guy pinning a girl's wrists on her bed, pushing into her", "boyfriend pins her wrists sex bed", "first time sex her bedroom", pool_dir="sex/jake_04_bed_t5"),
            D(J, "God, you're tight. Is this okay? Tell me this is okay."), ME("It's okay. Don't you dare be gentle.")],
            [go("Harder.", node="wall", mins=10)]),
        node("wall", "Ryan's wall", [P(beat("jake_04_sneak_him_in", "wall")),
            VID("a headboard banging a wall during sex", "headboard banging wall sex", "loud sex headboard thin wall", pool_dir="sex/jake_04_wall_t5"),
            D(J, "Your bed's hitting the wall. Who's on the other side?"), ME("My brother. Don't stop.")],
            [go("Don't stop.", node="landing", mins=5, cond_=cond(DOOR_UNLOCKED)),
             go("Don't stop.", node="comes", mins=5, cond_=cond(flag("her_door_unlocked", False)))]),
        node("landing", "The hall", [
            P("A footstep in the hall. You both freeze. Your door has no key. Mark's still got it."),
            P("Jake's hand goes over your mouth. The footstep stops, and then goes on, and a door closes."),
            P("He doesn't pull out. He starts again, slower."),
            D(J, "Who was that?"), ME("Nobody. Keep going. Slow, like that."),
        ], [go("Don't stop.", node="comes", mins=5)]),
        node("comes", "Still", [P(beat("jake_04_sneak_him_in", "comes")),
            VID("a couple coming together, her hand over his mouth, still afterwards", "couple cum together quiet", "creampie boyfriend her bed", pool_dir="sex/jake_04_comes_t5"),
            D(J, "Fuck. Fuck, @player. I'm still inside you."), ME("Stay there. Don't move yet.")],
            [go("Lie there.", node="after", mins=10)]),
        node("after", "Through the wall", [
            # reader a3 #22 (DECISIONS 131): the yes path points ahead. True: after step 4 the date end's "Come up." is his
            # room visit on any Saturday with a date (jake_saturday_date).
            P("Jake pulls you in against his chest and mumbles it into your hair, already half asleep."),
            D(J, "Next Saturday. Same room."),
            P("He's asleep in under a minute, one arm heavy across you, taking up most of the bed."),
            G(cond(RYAN_PAST_5), P("Through the wall, very low, so low you might have dreamed it:"), D(R, "…@player.nickname?"), T("He heard. Every second.")),
        ], [go("Sleep.", loc="home_ella_room", mins=360, consumes=True,
               eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 3, "cap": 79}, setv("jake_step", 4), nadd(R, "want", 5)],   # a Bold one-time step (DECISIONS 124)
               flags=[fset("jake_04_done"), fset("jake_first_time"), funset("jake_date_booked")])]),
    ]})

# ── the end of a date (jake_date_end.md, signed 2026-11-01): reworks jake_saturday_date. The car by her stage; after
#    step 4, "Come up." (a two-entry shuffle bag) with a near-catch on a 1-8 roll. Mark is asleep; Laura waits up. ──
CAP = lambda k, n, c: {"targetType": "player", "trait": k, "op": "add", "value": n, "cap": c}
CAR_PAY = lambda c: [CAP("corruption", 1, c), CAP("exhibitionism", 1, c)]
ROLL = lambda op, v: trait("jake_catch_roll", op, v)
# truth pass (2026-11-03): "Laura waits up with the TV" is true only while her row has her in the living room (Sat
# 22:00-00:00, not on the dark stairs after came_home_late, and never on a Wednesday, when she is in her bedroom), so
# that sentence and the next ("You look at it once.", the window) show behind her presence; the rest is the beat as signed.
CAR_LOW_LAURA = "Across the lawn the living-room window glows blue, where Laura waits up with the TV. You look at it once. "
_car_low = beat("jake_date_end", "car_low")
assert _car_low.count(CAR_LOW_LAURA) == 1
_cl_before, _cl_after = _car_low.split(CAR_LOW_LAURA)
CAR_LOW_BLOCKS = [*top_or_dress(_cl_before.strip()),
                  G(cond(here_at(L, "home_living_room")), P(CAR_LOW_LAURA.strip())),
                  *top_or_dress(_cl_after.strip())]
out.append({
    "id": "jake_saturday_date", "name": "The end of a date",
    "description": "The end of a Saturday date (release 1): the car outside the house by her stage, or after his step 4, her room. Both meters in the car (the street and Laura's window can see); Corruption behind her door. Once a date.",
    "trigger": {"location": "home_front_door", "npc": J, "requires_npc": J, "is_repeatable": True, "priority": 5, "is_active": True,
                "max_triggers_per_day": 1,
                "schedules": [{"weekdays": [2, 5], "start_time": "22:00", "end_time": "00:00"}],
                "conditions": cond(flag("jake_date_went"), WENT_TONIGHT, trait("jake_step", "gte", 3))},
    "nodes": [
        node("door", "The car", [
            # reader batch 5 (pass 3): the car beats (sheet jake_date_end) park him and kill the engine, so this line doesn't
            P("All the way home Jake's hand has been on your knee, and it's still there as he turns into your street."),
            G(cond(LAURA_DRESS), D(J, "Everyone was looking at you tonight.")),
            # pass 3 B4: the car talks
            D(J, "So. That was a good night. Right? Tell me that was a good night."),
            ME("It was a good night, Jake."),
            D(J, "Good. Because I'm not ready for it to be over yet."),
        ], [
            # DECISIONS 124: grinding in his lap is private contact (Bold); his hand or hers under the street lamp is sex strangers can see (Hungry).
            # jake_step gte 3, not eq 3: his step 4 takes the first Bold Saturday, so the car stays open after it.
            go("Kiss him.", node="car_low", mins=2, cond_=cond(BOLD, trait("corruption", "lt", 60), trait("jake_step", "gte", 3))),
            # pass 3 E95: the two sex acts in the car cost her 10 energy and lower hygiene (board.needs)
            go("\"Your hand. Now.\"", node="car_his", mins=2, cond_=cond(trait("corruption", "gte", 60), trait("jake_step", "gte", 3)), costs=[{"trait": "energy", "value": 10}], eff=[{"targetType": "player", "trait": "hygiene", "op": "add", "value": -10, "clamp": True}]),
            go("\"Lean back.\"", node="car_hers", mins=2, cond_=cond(trait("corruption", "gte", 60), trait("jake_step", "gte", 3)), costs=[{"trait": "energy", "value": 10}], eff=[{"targetType": "player", "trait": "hygiene", "op": "add", "value": -10, "clamp": True}]),
            # Saturday only: Laura waits up on Saturday nights (her rows), which the near-catch reads
            go("\"Come up.\"", node="sneak", mins=5, cond_=cond(trait("jake_step", "gte", 4), wd(5),
                                                          {"type": "npc_at_location", "location_id": "home_hall", "npc_id": "npc_laura", "operator": "is_absent"}),   # pass 4 reader: never walk into Laura waiting in the hall
               eff=[{"targetType": "player", "trait": "jake_catch_roll", "op": "set", "value": {"type": "random", "min": 1, "max": 8}}]),
            go("\"Goodnight, Jake.\"", node="night", mins=2),
        ]),
        node("car_low", "The car", [*CAR_LOW_BLOCKS,
            VID("a couple making out in a parked car at night, windows fogging", "couple making out parked car night", "car makeout outside her house", pool_dir="sex/jake_car_low_t4"),
            D(J, "The whole street can see the windows fogging up."), ME("Then stop breathing so hard.")],
            [go("\"Goodnight, gorgeous.\"", loc="home_hall", mins=20, eff=CAR_PAY(39), flags=[funset("jake_date_booked")])]),   # car_low opens at 20 (G8)
        node("car_his", "His hand", [*top_or_dress(beat("jake_date_end", "car_his")),
            VID("a guy fingering his girlfriend in a parked car under a street lamp", "fingering in parked car", "car fingering orgasm street lamp", pool_dir="sex/jake_car_his_t5"),
            D(J, "You're soaked. Right here under the street lamp, and you're soaked."), ME("Don't stop. Let them look.")],
            [go("\"Goodnight, gorgeous.\"", loc="home_hall", mins=20, eff=CAR_PAY(79), flags=[funset("jake_date_booked")])]),
        node("car_hers", "Your hand", [*top_or_dress(beat("jake_date_end", "car_hers")),
            VID("a girl giving her boyfriend a handjob in a parked car, a passer-by looking", "handjob in parked car", "car handjob caught", pool_dir="sex/jake_car_hers_t5"),
            D(J, "Fuck. That guy saw. That guy totally saw."), ME("Good. Now he knows whose you are.")],
            [go("\"Goodnight, gorgeous.\"", loc="home_hall", mins=20, eff=CAR_PAY(79), flags=[funset("jake_date_booked")])]),
        node("sneak", "Down the hall", [   # Q7: one hall (the sheet beat reads "down the dark hall")
            POOL(P(beat("jake_date_end", "`sneak` a")), P(beat("jake_date_end", "`sneak` b")), pid="jake_sneak", bag=True),
            # (reader fix) Laura is downstairs, waiting up, on a Saturday night: her feet on the stairs, not her door
            G(cond(ROLL("eq", 1)), P("In the living room the TV goes quiet. Laura's feet in the hall. You both stop breathing. They stop halfway, and go back."),
              D(J, "Your mom?"), ME("Shh.")),
            G(cond(ROLL("eq", 2), flag("ryan_knock_code")), P("Two knocks on the wall. Slow. Ryan's code."), D(J, "What was that?"), ME("Nothing. The pipes.")),
            VID("a couple having quiet sex in her bedroom at night", "sneaky sex her room at night", "boyfriend snuck in sex quiet", pool_dir="sex/jake_sneak_t5"),
            D(J, "Your bed's so loud. How is your bed this loud?"), ME("Then fuck me quieter. Don't stop."),
        ], [go("Let him out before dawn.", loc="home_ella_room", mins=300, eff=[CAP("corruption", 1, 59)], flags=[funset("jake_date_booked")])]),
        node("night", "Goodnight", [GC(cond(wd(2)), D(J, "Goodnight, gorgeous. Saturday?")), GC(cond(wd(5)), D(J, "Goodnight, gorgeous. Wednesday?")),
                                    ME("Goodnight, Jake. Text me when you're home."), D(J, "Already writing it."),
                                    P("He kisses your hand like an idiot and walks backwards down the path.")],
             [go("Go in.", loc="home_hall", mins=2, flags=[funset("jake_date_booked")])]),
    ]})

# ── his hubs: the quad (mornings), the canteen (lunch), Zoe's party ──
JAKE_STATE = [
    G(cond(SKIRT), D(J, "Guys. Look at her."),
      P("He says it to whoever's nearest, and his hand slides down onto your ass so they know whose legs they're looking at. His own eyes keep dropping to your hem."),
      D(J, "Later. When they're not looking.")),
    # reader a3 #30-34 (DECISIONS 131): the not-yet the skirt branch has (and only once, if a skirt shows too)
    G(cond(ZOE_DRESS), P("His eyes go down your legs and stay there.")),
    G(cond(ZOE_DRESS, {"type": "worn_type", "operator": "neq", "value": "short_skirt"}), D(J, "Later. When they're not looking.")),
    G(cond(LAURA_DRESS), D(J, "Everyone's looking at you in that dress.")),   # false lines a3 #23-26: his hubs are daytime
    G(cond(trait("jake_step", "eq", 1)), P("He puts his hand low on your back the second you're close enough."), D(J, "Hey, you. Sit with us."), ME("Just for a minute.")),
    G(cond(trait("jake_step", "eq", 2)), P("He keeps his hand on your back like he's already decided something about you."), D(J, "There she is. I was starting to think you were avoiding me."), ME("Maybe I was.")),
    G(cond(trait("jake_step", "eq", 3)), D(J, "Your brother hates me. I could tell at the door."), ME("Ryan hates everyone. Don't take it personally."), D(J, "He looked at me like I'd stolen something.")),
]
for cid, loc, name, line in [("hub_jake_quad", "quad", "Jake, with the team", "Jake's on the grass with his team, a space on the grass beside him so they'll all see who it's for."),
                              ("hub_jake_canteen", "canteen", "Jake, at lunch", "Jake has a tray with three of everything on it. He pulls you onto the bench next to him."),
                              ("hub_jake_party", "zoe_apartment", "Jake, at the party", "Jake's by the kitchen with a beer, talking over the music.")]:
    out.append({
        "id": cid, "name": name,
        "description": f"Jake's hub ({loc}): he shows her off.",
        "trigger": {"location": loc, "npc": J, "requires_npc": J, "is_repeatable": True, "priority": 6, "is_active": True,
                    "conditions": cond(flag("jake_met"))},
        "nodes": [node("jake", name, [
            P(line),
            POOL(D(J, "There she is."), D(J, "C'mere. Sit on my knee. They don't believe me about you."), pid=f"{cid}_lines"),
            G(cond(flag("jake_date_booked", False), flag("jake_stood_up", False)), D(J, "Saturday? Say Saturday.")),
            # the no-show text sets it (phone.py jake_date_noshow); the next date clears it
            G(cond(flag("jake_date_booked", False), flag("jake_stood_up")), D(J, "You still owe me a date, you know. Saturday?")),
            *JAKE_STATE,
        ], [go("Stay with him a while.", loc=loc, mins=20), go("Leave him to the guys.", loc={"quad": "campus", "canteen": "campus"}.get(loc, "town"))])]})   # pass 3 D39 (R7)

# ── his face in figure drawing, and at the gym (ledger L18, L27; campus_gym.md) ──
out.append({
    "id": "hub_jake_class", "name": "Jake, in figure drawing",
    "description": "Jake at the next easel in figure drawing (his lecture-hall rows, once she has his number).",
    "trigger": {"location": "lecture_hall", "npc": J, "requires_npc": J, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("jake_number"))},
    "nodes": [node("easel", "Jake, at his easel", [
        P("Jake has the easel next to yours and hasn't drawn a line. He's watching you set up instead."),
        POOL(D(J, "Draw me after. I'll hold still, I swear."), D(J, "I'm only in this class for the credits. And you."), pid="jake_class_lines"),
        *JAKE_STATE,
    ], [go("Talk with him a while.", loc="lecture_hall", mins=10), go("Leave him to his easel.", loc="campus")])]})

GYM_CAP = "jake_gym_today"   # once per window (the gym sheet): cleared at midnight
out.append({
    "id": "hub_jake_gym", "name": "Jake, training",
    "description": "Jake at team training in the gym, Tue and Thu afternoons (campus_gym.md): talk; Curious, his hands on her hips at the squat rack; Bold, after Jake B 2, a kiss against the lockers. Once a day.",
    "trigger": {"location": "campus_gym", "npc": J, "requires_npc": J, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("jake_number"))},
    "nodes": [
        node("rack", "Jake, at the rack", [
            P("Jake's at the squat rack with the team, in a tank top soaked through. He racks the bar when he sees you and doesn't pick it up again."),
            D(J, "You lift? Come here. I'll show you."),
            *JAKE_STATE,
        ], [
            go("Train with him.", node="spot", mins=30, cond_=cond(flag(GYM_CAP, False)), flags=[fset(GYM_CAP)]),
            # his hands on her with the team whistling: the touch pays Corruption (its gate), being seen pays Exhibitionism,
            # both capped at the top of the stage it opens at (pass 3 A48, G8)
            go("Let him fix your squat.", node="hips", mins=30, cond_=cond(flag(GYM_CAP, False), CURIOUS), flags=[fset(GYM_CAP)],
               eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 39},
                    {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 19},   # no Exhibitionism gate: stage 1 (G8)
                    add("campus_talk", 1, clamp=False)]),   # pass 4 E94: the team whistles, so campus talks; once a day (GYM_CAP)
            go("Pull him into the locker room.", node="lockers", mins=15, cond_=cond(flag(GYM_CAP, False), BOLD, trait("jake_step", "gte", 2)),
               flags=[fset(GYM_CAP)], eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 59}]),
            go("Leave him to his reps.", loc="campus"),
        ]),
        node("spot", "Spotting", [
            P("He spots you on the bench, counting your reps out loud, his hands an inch under the bar the whole time. The team pretends not to watch."),
            D(J, "Ten. Look at you. Ten."),
        ], [go("Done.", loc="campus", mins=5)]),
        node("hips", "His hands on your hips", [
            P("He stands behind you at the rack and puts his hands on your hips to show you how low to go. They stay there on the way down, and on the way back up, and on the next one too. On the third rep your ass brushes him and he's hard, and he steps back fast. Somebody on the team whistles."),
            D(J, "Lower. Like that. But not here. Not with them watching."),
        ], [go("Done.", loc="campus", mins=5)]),
        node("lockers", "Against the lockers", [
            P("You take his wrist and walk him into the empty locker room, and he lets you. He kisses you up against the lockers, hard enough that the metal rattles, his hands on your waist, until someone's voice just outside the locker room makes you both stop."),
            D(J, "You're going to get me thrown off the team."),
        ], [go("Done.", loc="campus", mins=5)]),
    ]})

cards = step_cards(J, {
    1: ("", ""),
    2: ("He's got your number. He hangs out on the quad with his team.", "A Monday, Wednesday or Friday morning on the quad, Jake and his team (Curious or Daring)"),
    3: ("Saturday. He picks you up at the door.", "Saturday night: a date with Jake, back to the front door after eleven (Curious, Daring)"),
    4: ("His car outside the house, Saturday after Saturday. He wants more than the car.", "Saturday night after a date: the front door (Bold)"),
}, met_flag="jake_met", terminal_text=("Wednesdays and Saturdays: a date. Saturdays, your room after.", "Jake, further. (Next release)"), skip=(1,))

text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · JAKE (sheets/scenes/jake_*.md, people/npc_jake.md)\n"
        "# Steps 2-3 (step 1 is zoe_01_first_party, step 4 is laura_05_jake_at_the_door), the date,\n"
        "# the Saturday goodnight, his hubs, his cards.\n"
        "# =============================================================================\n")
# Iteration 002, part 3: leaving this outing after 22:00 sets late_date and came_home_late (Q69,
# the street sheet "Why she's late"; canv.mark_late). Each is read for 4 hours; her bed clears them.
for _c in out:
    if _c["id"] in ['jake_03_my_boyfriend', 'jake_saturday_date', 'jake_04_sneak_him_in']:
        mark_late(_c, 'late_date', split=False)
require_present(out, "jake_03_my_boyfriend", here_at(L, "home_living_room"))
# heat proposal A1 (the gym) and A3 (the quad), DECISIONS 147 chunk 2: screens inside his hubs (heat_a.py)
import heat_a
heat_a.attach_jake(out)

# pass 4 E95: the one-time sex step takes energy and hygiene like the repeatable acts (board.needs)
sex_takes_needs(out, "jake_04_sneak_him_in", "comes", "Lie there.")
text += "".join(emit(c) for c in out) + "".join(emit_card(c) for c in cards)
open(__import__("sys").argv[1], "w").write(text)
print("jake:", len(out), "canvases,", len(cards), "cards")
