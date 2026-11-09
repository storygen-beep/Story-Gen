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


def by_level(meter, **lines):
    """Her line by band (register.md "One event, several levels"): keys good_girl, curious, bold, hungry. Write only the
    bands the scene can reach; the lowest one written also catches anything under it, so the screen is never silent."""
    bands = {"good_girl": (None, 20), "curious": (20, 40), "bold": (40, 60), "hungry": (60, None)}
    written = [k for k in bands if k in lines]
    rows = []
    for k in written:
        lo, hi = bands[k]
        items = ([trait(meter, "gte", lo)] if lo is not None and k != written[0] else []) + ([trait(meter, "lt", hi)] if hi is not None else [])
        rows.append(G(cond(*items), lines[k]))
    return rows


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
            *by_level("exhibitionism",
                      good_girl=T("He wants them to see you're his. You're not sure you want that, and your ears are burning."),
                      curious=T("He wants them to see you're his. You wonder what it would be like to let them."),
                      bold=T("He wants them to see you're his. You want them to see too."),
                      hungry=T("He wants them to see you're his. You want them to see a lot more than a kiss.")),
        ], [go("\"Again.\"", node="ask", mins=3, eff=[add("exhibitionism", 3, cap=79), add("campus_talk", 1, clamp=False)])]),
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
            P("Jake walks you up to the porch and stops under the light. The living room is dark. He looks past you at its dark windows. \"Is anyone up?\" He sounds like he hopes so. \"Nobody,\" you say. \"Not yet.\" Ryan's window is lit, right beside the porch. He's home. You want him to look. \"Shame,\" Jake says. \"I want them to see you're mine, @player.\" His hand slides down your back and settles on your ass. You should move it, but you like being shown off. He leans in, and his mouth stops an inch from yours."),
            *by_level("exhibitionism",
                      curious=T("What if someone looks out? You wonder, and you still don't move his hand."),
                      bold=T("Come on, Ryan. Come to the window. See where his hand is."),
                      hungry=T("You want Ryan's face in that window. You want him to watch that hand squeeze.")),
        ], [
            go("Kiss him.", node="rail", mins=3),
            go("\"Goodnight, Jake.\"", node="no", mins=2),
        ]),
        node("rail", "The rail", [
            P("You kiss him first, right there under the porch light. Jake makes a low sound and lifts you onto the rail like you weigh nothing. Your legs lock round his waist. His hands sit on your hips, then slide down to grab your ass. \"God, @player,\" he breathes into your mouth. It gets hungry and loud, all teeth and breath. The rail creaks every time he pulls you closer. Anyone inside could hear it, but you don't care. You want more of his mouth. Then, behind him, the lock turns."),
        # LO 2026-11-03: Want pays for what happened, never for a no. Ryan sees her on the rail when the door opens, so
        # his Love -15 and Want +5 sit on the way in, not on her goodnight
        ], [go("\"Don't stop.\"", node="ryan", mins=3, eff=[nadd(R, "warmth", -15), nadd(R, "want", 5)])]),
        node("ryan", "Ryan", [
            P("The front door opens behind Jake. Ryan stands in the doorway and stops dead. You're on the porch rail with your legs locked round Jake's waist, kissing him. Jake's hands are full of your ass. You don't climb down. You look straight at Ryan over Jake's shoulder and hold it. \"Ryan, this is Jake. My boyfriend.\" Ryan's jaw goes tight. His eyes drop to Jake's hands on you, then come back to your face. \"Great.\" Jake grins over his shoulder, not getting it. \"Your brother hates me.\" *Good. Look all you want, Ryan.* Ryan steps back inside without another word. The door slams hard."),
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
            G(cond(SKIRT), P("He stops talking when he sees the skirt. His eyes drop to your bare thighs, and he forgets to shut his mouth.")),
            D(J, "Ready? I've got a whole night planned. Don't laugh."),
            G(CURFEW_ON, T("You're grounded. Laura would know by morning, she always does.")),
        ], [
            # C4 (LO 2026-11-03): dirty, the date doesn't happen, and he says why
            go("Go out with him.", node="date", mins=10, cond_=cond(*NO_CURFEW["items"], trait("hygiene", "gte", 30)), flags=[fset("jake_date_went"), funset("jake_stood_up")]),
            go("Go out with him.", node="date", mins=10, cond_=cond(*NO_CURFEW["items"], trait("hygiene", "lt", 30), flag("hygiene_off")), flags=[fset("jake_date_went"), funset("jake_stood_up")]),
            go("Go out with him.", node="stink", mins=2, cond_=cond(*NO_CURFEW["items"], trait("hygiene", "lt", 30), flag("hygiene_off", False)), flags=[funset("jake_date_booked")]),  # Q73 (iteration 002: pulled forward from part 5 so Laura C 5 has its flag)
            go("\"I'm grounded. Next week.\"", node="grounded", mins=3, cond_=CURFEW_ON, flags=[funset("jake_date_booked")]),
            go("\"Not tonight, Jake.\"", node="no", mins=2),
        ]),
        node("date", "The date", [
            POOL(
                P("Dinner at the place with the candles. He talks about the team, and the coach, and a guy who threw up on the bus, and you laugh in the right places. He holds your hand on the table where the whole restaurant can see it. Afterwards he drives you home the long way, one hand on the wheel and one on your knee."),
                P("A film you don't watch. He has his arm round you from the trailers, and his hand on your knee from the first scene, and every time somebody comes down the aisle he kisses you so they'll see. He drives you home through the park, slowly."),
                pid="jake_date_lines"),
            # her line by her level (Corruption), beside his hand; the not-yet that follows answers it
            *by_level("corruption",
                      good_girl=ME("Jake. People can see your hand."),
                      curious=ME("What happens to that hand when we're not in public?"),
                      bold=ME("You could go a little higher, you know. Nobody's looking."),
                      hungry=ME("Higher, Jake. I don't care who's looking.")),
            # scene reader b03 (2026-11-03): the not-yet on the body (H4.3)
            P("His hand on your knee squeezes, and his thumb strokes the inside of it, but it never goes higher up your thigh. Not in public. Not yet."),
            D(J, "You're the best-looking girl in this whole town, you know that? Everyone was looking."),
            # next step: what he wants moves with his ladder (jake_03 is the door, jake_04 her room; reader: nothing read jake_step)
            G(cond(trait("jake_step", "eq", 2)), D(J, "So who's home at your place? I want them to see me bring you back.")),
            G(cond(trait("jake_step", "eq", 3)), D(J, "Your brother's seen me now. What I want to see is your room.")),
            G(cond(trait("jake_step", "gte", 4)), D(J, "I've been thinking about your bed all night. You know that, right?")),
        ], [go("Let him drive you home.", loc="home_front_door", mins=m, cond_=cond(tod(a, b))) for (a, b), m in BACK_AT_11]),
        node("stink", "Not like that", [
            P("He leans in to kiss you hello and stops halfway, his nose wrinkling."),
            D(J, "Gorgeous. Did you shower today? I booked the place with the candles. Go wash. I'll text you."),
            P("He goes back to his car. You can smell it on yourself now too."),
        ], [go("Close the door.", loc="home_front_door", mins=2)]),
        node("grounded", "Grounded", [
            D(J, "Grounded? For real? Okay, gorgeous. Next week, then. I can wait."),
            P("He looks you up and down once from the step, slowly, and then he goes back to his car, swinging his keys."),
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
        node("door", "Come in", [
            P("Jake walks you up to the porch and stops under the light. You don't let go of his hand. You open the front door and pull him in after you."),
            ME("Come in."),
            # reader pass 4 b4: Laura waits up in the living room Sat 22:00-00:00; the sneak-in passes her doorway
            G(cond(here_at(L, "home_living_room")), P("The living-room doorway flickers blue. Mom's on the couch in the dark with the TV on low, waiting up, her back to the hall. You get him past it on your toes, his hand on your ass the whole way.")),
            P("In the dark hall he catches your hip and his breath is hot on your ear."),
            D(J, "Your room. Now."),
            *by_level("corruption",
                      bold=T("If anyone hears you, you're dead. You keep pulling him down the hall anyway."),
                      hungry=T("You're already wet. You want him in your bed, and you're not sure you can be quiet.")),
        ], [go("\"Quiet.\"", node="bed", mins=5),
            go("\"Goodnight, Jake.\"", node="next_sat", mins=2)]),
        node("next_sat", "Next Saturday", [
            D(J, "Next Saturday, then. Your room."),
            P("He grins and backs out the front door, and walks backwards down the path, all the way to the car."),
        ], [go("Shut the door.", loc="home_hall", mins=2, retry=7, flags=[funset("jake_date_booked")])]),
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
            # reader a3 #22 (DECISIONS 131): the yes path points ahead. True: after step 4 the date end's "Come in." is his
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
#    step 4, "Come in." (a two-entry shuffle bag) with a near-catch on a 1-8 roll. Mark is asleep; Laura waits up. ──
CAP = lambda k, n, c: {"targetType": "player", "trait": k, "op": "add", "value": n, "cap": c}
CAR_PAY = lambda c: [CAP("corruption", 1, c), CAP("exhibitionism", 1, min(c, 39))]   # the car's Corruption gate holds nothing on Exhibitionism: it opens at 20 and stops at 39 (LO, 2026-11-04)
ROLL = lambda op, v: trait("jake_catch_roll", op, v)
# truth pass (2026-11-03): "Laura waits up with the TV" is true only while her row has her in the living room (Sat
# 22:00-00:00, not on the dark stairs after came_home_late, and never on a Wednesday, when she is in her bedroom), so
# that sentence and the next ("You look at it once.", the window) show behind her presence; the rest is the beat as signed.
def top_or_clothes(text):
    """canv.top_or_dress, plus every other outfit: 'Go out with him' has no clothes gate, so she can be in a uniform,
    a towel or a sleep shirt at the door (scene reader, 2026-11-04). A top, one of the two dresses, else "your clothes"."""
    if "your top" not in text:
        return [P(text)]
    return chain_by_sentence([
        (cond({"type": "clothing_slot", "slot": "top", "operator": "equipped"}, {"type": "clothing_slot", "slot": "dress", "operator": "unequipped"}), text),
        *[(cond({"type": "clothing_item", "item_id": d, "operator": "equipped"}), text.replace("your top", "your dress")) for d in DRESSES],
        (cond(*ANY_), text.replace("your top", "your clothes"))])

def car_hook(before_room, wednesday, saturday):
    return [G(cond(trait("jake_step", "eq", 3)), D(J, before_room)),
            G(cond(trait("jake_step", "gte", 4), wd(2)), D(J, wednesday)),
            G(cond(trait("jake_step", "gte", 4), wd(5)), D(J, saturday))]


CAR_LOW_LAURA = "Across the lawn the living-room window glows blue, where Laura waits up with the TV. You look at it once. "
_car_low = beat("jake_date_end", "car_low")
assert _car_low.count(CAR_LOW_LAURA) == 1
_cl_before, _cl_after = _car_low.split(CAR_LOW_LAURA)
CAR_LOW_BLOCKS = [*top_or_clothes(_cl_before.strip()),
                  G(cond(here_at(L, "home_living_room")), P(CAR_LOW_LAURA.strip())),
                  *top_or_clothes(_cl_after.strip())]
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
            G(cond(LAURA_DRESS), D(J, "Every guy in that place was looking at you tonight.")),
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
            go("\"Come in.\"", node="sneak", mins=5, cond_=cond(trait("jake_step", "gte", 4), wd(5),
                                                          {"type": "npc_at_location", "location_id": "home_hall", "npc_id": "npc_laura", "operator": "is_absent"}),   # pass 4 reader: never walk into Laura waiting in the hall
               costs=[{"trait": "energy", "value": 10}],   # he fucks her over her bed: it costs as the car does
               eff=[{"targetType": "player", "trait": "jake_catch_roll", "op": "set", "value": {"type": "random", "min": 1, "max": 8}}, {"targetType": "player", "trait": "hygiene", "op": "add", "value": -10, "clamp": True}]),
            go("\"Goodnight, Jake.\"", node="night", mins=2),
        ]),
        node("car_low", "The car", [*CAR_LOW_BLOCKS,
            VID("a couple making out in a parked car at night, windows fogging", "couple making out parked car night", "car makeout outside her house", pool_dir="sex/jake_car_low_t4"),
            D(J, "The whole street can see the windows fogging up."), ME("Then stop breathing so hard."),
            *car_hook("One of these Saturdays I'm not stopping at the car, gorgeous.",
                      "Saturday, gorgeous. Your room, not my car.",
                      "Wednesday, gorgeous. Then next Saturday, your room.")],
            [go("\"Goodnight, gorgeous.\"", loc="home_hall", mins=20, eff=CAR_PAY(39), flags=[funset("jake_date_booked")])]),   # car_low opens at 20 (G8)
        node("car_his", "His hand", [*top_or_clothes(beat("jake_date_end", "car_his")),
            VID("a guy fingering his girlfriend in a parked car under a street lamp", "fingering in parked car", "car fingering orgasm street lamp", pool_dir="sex/jake_car_his_t5"),
            D(J, "You're soaked. Right here under the street lamp, and you're soaked."), ME("Don't stop. Let them look."),
            *car_hook("One Saturday soon I want you in a bed, gorgeous. Your bed.",
                      "Saturday. I want to hear you do that in your bed.",
                      "Wednesday, the car. Next Saturday, your bed. I've got it all worked out.")],
            [go("\"Goodnight, gorgeous.\"", loc="home_hall", mins=20, eff=CAR_PAY(79), flags=[funset("jake_date_booked")])]),
        node("car_hers", "Your hand", [*top_or_clothes(beat("jake_date_end", "car_hers")),
            VID("a girl giving her boyfriend a handjob in a parked car, a passer-by looking", "handjob in parked car", "car handjob caught", pool_dir="sex/jake_car_hers_t5"),
            D(J, "Fuck. That guy saw. That guy totally saw."), ME("Good. Now he knows whose you are."),
            *car_hook("Do that again some Saturday, and I'm walking you to your room to finish.",
                      "Saturday I'm returning the favor, gorgeous. In your room.",
                      "Wednesday I'm returning the favor, gorgeous. Right here.")],
            [go("\"Goodnight, gorgeous.\"", loc="home_hall", mins=20, eff=CAR_PAY(79), flags=[funset("jake_date_booked")])]),
        node("sneak", "Down the hall", [   # Q7: one hall (the sheet beat reads "down the dark hall")
            POOL(P(beat("jake_date_end", "`sneak` a")), P(beat("jake_date_end", "`sneak` b")), pid="jake_sneak", bag=True),
            # (reader fix) Laura waits up in the living room on a Saturday night: her feet in the hall, not her door. Only while
            # her row has her there: at midnight she goes to the master bedroom (scene reader, 2026-11-04)
            G(cond(ROLL("eq", 1), here_at(L, "home_living_room")), P("In the living room the TV goes quiet. Laura's feet in the hall. You both stop breathing. They stop halfway, and go back."),
              D(J, "Your mom?"), ME("Shh.")),
            G(cond(ROLL("eq", 2), flag("ryan_knock_code")), P("Two knocks on the wall. Slow. Ryan's code."), D(J, "What was that?"), ME("Nothing. The pipes.")),
            VID("a couple having quiet sex in her bedroom at night", "sneaky sex her room at night", "boyfriend snuck in sex quiet", pool_dir="sex/jake_sneak_t5"),
            D(J, "Your bed's so loud. How is your bed this loud?"), ME("Then fuck me quieter next time."),
            D(J, "Next Saturday, then. I'm bringing earplugs for your brother."),
        ], [go("Let him out before dawn.", loc="home_ella_room", mins=300, eff=[CAP("corruption", 1, 59)], flags=[funset("jake_date_booked")])]),
        node("night", "Goodnight", [GC(cond(wd(2)), D(J, "Goodnight, gorgeous. Saturday?")), GC(cond(wd(5)), D(J, "Goodnight, gorgeous. Wednesday?")),
                                    ME("Goodnight, Jake. Text me when you're home."), D(J, "Already writing it."),
                                    P("He kisses your hand like an idiot and walks backwards down the path.")],
             [go("Go in.", loc="home_hall", mins=2, flags=[funset("jake_date_booked")])]),
    ]})

# ── the booty call (reach audit 2026-11-09, playtest_study_20261109/12_reach_audit.md; LO "Go ahead" on Zoe and Jake):
#    after his step 4 he texts "you up?" on the nights there's no date (Sun, Mon, Tue, Thu, phone.py jake_booty_text);
#    her yes sets jake_coming (3 hours, people_data._LATCH_HOURS) and his row puts him at her front door 22:00-00:00.
#    The top games' shape: Course of Temptation's booty call, any night 18:00-24:00, once a day (REPORT.md section 2).
#    The act has its own two beats (jake_date_end.md `booty` a, b; they name no day); the near-catch is Mark's TV, whose row has him
#    in the living room 22:00-00:00 those nights, or Ryan's code on the wall. ──
out.append({
    "id": "jake_booty_call", "name": "Jake at your door",
    "description": "After Jake's step 4, on a night with no date: he texts \"you up?\", she answers \"door's unlocked\", and he's at the front door 22:00-00:00. Her room; Corruption +1, cap 59. Once a night.",
    "trigger": {"location": "home_front_door", "npc": J, "requires_npc": J, "is_repeatable": True, "priority": 5, "is_active": True,
                "max_triggers_per_day": 1,
                "schedules": [{"weekdays": [0, 1, 3, 6], "start_time": "22:00", "end_time": "00:00"}],
                "conditions": cond(flag("jake_coming"), trait("jake_step", "gte", 4))},
    "nodes": [
        node("door", "Your front step", [
            P("Jake's on your front step with his hood up and his hands shoved in his pockets, grinning like he's already got away with something."),
            D(J, "Told you twenty minutes, gorgeous."),
            ME("Shh. Keep your voice down."),
            D(J, "I'm whispering. This is me whispering."),
            T("He came across town because you typed two words. You want him in your bed before anyone hears the door."),
        ], [
            go("\"Come in.\"", node="sneak", mins=5,
               cond_=cond({"type": "npc_at_location", "location_id": "home_hall", "npc_id": "npc_laura", "operator": "is_absent"}),
               costs=[{"trait": "energy", "value": 10}],
               eff=[{"targetType": "player", "trait": "jake_catch_roll", "op": "set", "value": {"type": "random", "min": 1, "max": 8}},
                    {"targetType": "player", "trait": "hygiene", "op": "add", "value": -10, "clamp": True}]),
            go("\"Not tonight, Jake.\"", node="no", mins=2),
        ]),
        node("sneak", "Down the hall", [
            POOL(P(beat("jake_date_end", "`booty` a")), P(beat("jake_date_end", "`booty` b")), pid="jake_booty_sneak", bag=True),   # gate one pool, one place: its own beats
            G(cond(ROLL("eq", 1), here_at("npc_mark", "home_living_room")),
              P("Down the hall Mark's TV goes quiet. You both stop breathing. Then a laugh track, loud, and he hasn't moved."),
              D(J, "Your stepdad?"), ME("Shh.")),
            G(cond(ROLL("eq", 2), flag("ryan_knock_code")), P("Through the wall, two slow knocks, and then nothing."), D(J, "Is that your brother?"), ME("Ignore him. Don't stop.")),
            VID("a boyfriend snuck into her bedroom late, quiet sex on her bed", "boyfriend snuck in late quiet sex", "booty call sneak in her room", pool_dir="sex/jake_booty_t5"),
            D(J, "Your bed's so loud. How is your bed this loud?"), ME("Then fuck me quieter next time."),
            D(J, "Text me back next time too. I'll come running."),
        ], [go("Let him out before dawn.", loc="home_ella_room", mins=300, eff=[CAP("corruption", 1, 59)])]),
        node("no", "Not tonight", [
            D(J, "You made me drive over here to say no?"),
            ME("I made you drive over here. That's different."),
            P("He laughs, low, kisses you once on the step, hard enough that you nearly change your mind, and jogs back down the path to his car."),
        ], [go("Go in.", loc="home_hall", mins=2)]),
    ]})
clear_on_leave(out[-1], "jake_coming")

# ── his hubs: the quad (mornings), the canteen (lunch), Zoe's party ──
# One pool, one place (2026-11-04): each hub says these its own way. The quad keeps the first words, because its lap scene
# answers them ("Forget later. Guys. Look at her.", heat_a A3). Gates stay in jake_state, one place. Rows: quad Mon/Wed/Fri
# morning, canteen Mon-Fri lunch, class Tue/Thu morning and Wed afternoon, gym Tue/Thu 15:00-17:00, party Fri 19:00-00:00.
JAKE_HUB_LINES = {
    "quad": {
        "skirt": ("Guys. Look at her.",
                  "He says it to whoever's nearest, and his hand slides down onto your ass so they know whose legs they're looking at. His own eyes keep dropping to your hem.",
                  "Later. When they're not looking."),
        "zoe_dress": ("His eyes go down your legs and stay there.", "Later. When they're not looking."),
        "laura_dress": "Everyone's looking at you in that dress.",
        1: ("He puts his hand low on your back the second you're close enough.", "Hey, you. Sit with us.", "Just for a minute."),
        2: ("He keeps his hand on your back like he's already decided something about you.", "There she is. I was starting to think you were avoiding me.", "Maybe I was."),
        3: ("Your brother hates me. I could tell at the door.", "Ryan hates everyone. Don't take it personally.", "He looked at me like I'd stolen something."),
    },
    "canteen": {
        "skirt": ("Guys. Look who's eating with me.",
                  "He says it down the table with his mouth full, and his hand drops under it onto your ass so they all know who you're with. His eyes keep sliding down to your hem.",
                  "Later. When this table's finished staring."),
        "zoe_dress": ("He puts his fork down. He's looking at your legs in that black dress.", "Later. When I've finished looking."),
        "laura_dress": "The whole line's looking at you in that dress.",
        1: ("He shifts his tray with one hand and puts the other low on your back, pulling you in along the bench.", "Hey, you. Eat with us.", "One fry, then I'm gone."),
        2: ("He saves you the end of the bench and keeps one arm along the back of it, behind you, like you already said yes.", "Thought you'd found another table.", "Maybe I should."),
        3: ("Has your brother said anything about me?", "Ryan doesn't say anything to anyone.", "That door slammed pretty hard."),
    },
    "class": {
        "skirt": ("Hey. Draw this instead.",
                  "He says it to the guy at the next easel, and his hand brushes down over your ass on its way back to his charcoal. His eyes keep dropping to your hem.",
                  "Later. When there's no lecturer in the room."),
        "zoe_dress": ("He's holding his charcoal and not using it. He's looking at your legs in that black dress.", "Not in class. Later."),
        "laura_dress": "Nobody in here is looking at their easel. Not with that dress.",
        1: ("He reaches across from his easel and rests his hand low on your back, like it's there by accident.", "Hey, you. Stand here. Better light.", "Two minutes. Then I'm drawing."),
        2: ("He moves his stool an inch closer to your easel, then another inch, like he has a right to.", "I saved you this easel. Nobody else gets it.", "Did I ask you to?"),
        3: ("Think your brother would hit me? Honest answer.", "Honestly? Keep your hands where he can't see them.", "That's not a no."),
    },
    "gym": {
        "skirt": ("Hey, guys. Reps can wait. Look.",
                  "He says it across the rack, wiping his neck, and his damp hand lands on your ass so the team knows whose legs those are. He keeps looking down at your hem.",
                  "Later. When Coach has gone home."),
        "zoe_dress": ("He's looking at your legs in that black dress, and the guy behind him has to say his name twice.", "Not with the team here. Later."),
        "laura_dress": "That dress, in a gym? The whole team just lost count.",
        1: ("He comes over still breathing hard and rests one hot, sweaty hand low on your back.", "Hey, you. Watch me lift.", "Just one set."),
        2: ("He taps your hip with two fingers as he goes past, like he's checking you're still his.", "You're here to watch. Admit it.", "I'm here to lift."),
        3: ("I'm lifting extra, in case your brother wants to settle it.", "Ryan's not going to fight you.", "He looked like he wanted to, on that porch."),
    },
    "party": {
        "skirt": ("Hey. Hey, look who's in a skirt.",
                  "He says it over the music to the guys by the kitchen, and his hand slides onto your ass and stays. His eyes keep going to your hem, even while he's talking to them.",
                  "Later. Somewhere without the whole party."),
        "zoe_dress": ("He looks down your legs in that black dress, and his beer stops on the way to his mouth.", "Later. I mean it."),
        "laura_dress": "That dress. Half this party's forgotten their drink.",
        1: ("He gets a hand low on your back before you're even through the kitchen door.", "Hey, you. Drink with us.", "One drink."),
        2: ("His arm comes around your waist and stays there, and he doesn't stop talking to the guys.", "Took you long enough. I was about to come looking.", "You wouldn't have found me."),
        3: ("He still mad, your brother? About the porch?", "He's always mad. Drink your beer.", "I'm just saying. That door almost came off."),
    },
}


def jake_state(where):
    say = JAKE_HUB_LINES[where]
    return [
        G(cond(SKIRT), D(J, say["skirt"][0]), P(say["skirt"][1]), D(J, say["skirt"][2])),
        # reader a3 #30-34 (DECISIONS 131): the not-yet the skirt branch has (and only once, if a skirt shows too)
        G(cond(ZOE_DRESS), P(say["zoe_dress"][0])),
        G(cond(ZOE_DRESS, {"type": "worn_type", "operator": "neq", "value": "short_skirt"}), D(J, say["zoe_dress"][1])),
        G(cond(LAURA_DRESS), D(J, say["laura_dress"])),   # false lines a3 #23-26: the day hubs are daytime, the party says its own
        G(cond(trait("jake_step", "eq", 1)), P(say[1][0]), D(J, say[1][1]), ME(say[1][2])),
        G(cond(trait("jake_step", "eq", 2)), P(say[2][0]), D(J, say[2][1]), ME(say[2][2])),
        G(cond(trait("jake_step", "eq", 3)), D(J, say[3][0]), ME(say[3][1]), D(J, say[3][2])),
    ]


# Each hub's own pool line and its own ask (his "Saturday?" is booked on his thread; the party is Friday night, so tomorrow).
JAKE_HUB_ASK = {
    "hub_jake_quad": ("C'mere. Sit on my knee. They don't believe me about you.", "Saturday? Say Saturday.", "You still owe me a date, you know. Saturday?"),
    "hub_jake_canteen": ("Move over, guys. C'mere. Eat off my tray, so they believe me.", "Saturday. You and me. Finish that and say yes.", "You left me sitting outside your house. You owe me Saturday."),
    "hub_jake_party": ("C'mere. Tell these guys I'm not making you up.", "Tomorrow night. Say you're free tomorrow night.", "You stood me up, remember? Tomorrow night. You owe me."),
}
# scene reader 2026-11-04 (the written no): while his ask stands, leaving is her no, in words, with his reply. No pay.
# (her no, his reply) to the ask, then (her no, his reply) after she stood him up, then the way out.
JAKE_HUB_NO = {
    "hub_jake_quad": ("Not Saturday, Jake.", "Not yet, you mean. I'll keep asking, gorgeous.",
                      "I don't owe you a thing, Jake.", "Sure you do, gorgeous. Ask me how long I sat out there.", "Walk off across the grass."),
    "hub_jake_canteen": ("No, Jake. Not Saturday. Eat your lunch.", "Not this one, then. I can wait, gorgeous.",
                         "Not happening, Jake. Eat your lunch.", "You still owe me, gorgeous. I can wait.", "Leave him to his tray."),
    "hub_jake_party": ("Not tomorrow, Jake.", "Fine. Go dance, gorgeous. I'll ask again next Friday.",
                       "You can keep asking, Jake.", "I will, gorgeous. Every Friday.", "Walk out on him."),
}
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
            POOL(D(J, "There she is."), D(J, JAKE_HUB_ASK[cid][0]), pid=f"{cid}_lines"),
            G(cond(flag("jake_date_booked", False), flag("jake_stood_up", False)), D(J, JAKE_HUB_ASK[cid][1])),
            # the no-show text sets it (phone.py jake_date_noshow); the next date clears it
            G(cond(flag("jake_date_booked", False), flag("jake_stood_up")), D(J, JAKE_HUB_ASK[cid][2])),
            *jake_state(cid.replace("hub_jake_", "")),
        ], [go("Stay with him a while.", loc=loc, mins=20),   # pass 3 D39 (R7)
            go("Leave him to the guys.", loc={"quad": "campus", "canteen": "campus"}.get(loc, "town"), cond_=cond(flag("jake_date_booked"))),
            go("Leave him to the guys.", node="no", cond_=cond(flag("jake_date_booked", False)))]),
            node("no", "Not Saturday", [
                G(cond(flag("jake_stood_up", False)), ME(JAKE_HUB_NO[cid][0]), D(J, JAKE_HUB_NO[cid][1])),
                G(cond(flag("jake_stood_up")), ME(JAKE_HUB_NO[cid][2]), D(J, JAKE_HUB_NO[cid][3])),
            ], [go(JAKE_HUB_NO[cid][4], loc={"quad": "campus", "canteen": "campus"}.get(loc, "town"))])]})

# ── his face in figure drawing, and at the gym (ledger L18, L27; campus_gym.md) ──
out.append({
    "id": "hub_jake_class", "name": "Jake, in figure drawing",
    "description": "Jake at the next easel in figure drawing (his lecture-hall rows, once she has his number).",
    "trigger": {"location": "lecture_hall", "npc": J, "requires_npc": J, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("jake_number"))},
    "nodes": [node("easel", "Jake, at his easel", [
        P("Jake has the easel next to yours and hasn't drawn a line. He's watching you set up instead."),
        POOL(D(J, "Draw me after. I'll hold still, I swear."), D(J, "I'm only in this class for the credits. And you."), pid="jake_class_lines"),
        *jake_state("class"),
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
            *jake_state("gym"),
            # the gym clothes (DECISIONS 198; GYM_CLOTHES_PLAN.md §6): what she trains in, read by the man she trains with.
            # Each group shuts out the others, so one line shows.
            G(cond({"type": "worn_type", "operator": "eq", "value": "sheer_leggings"}),
              P("His eyes drop to your ass through the sheer leggings and he forgets the bar is in his hands. Behind him the whole team has gone quiet."),
              D(J, "Are you trying to get me killed? Coach is right there.")),
            G(cond({"type": "worn_type", "operator": "eq", "value": "gym_shorts"}, {"type": "worn_type", "operator": "neq", "value": "sheer_leggings"}),
              P("He looks at your ass half out of the tiny shorts, then at the team looking at it, then back at your ass."),
              D(J, "You wore those here. On purpose. Jesus.")),
            G(cond({"type": "clothing_item", "item_id": "sports_bra", "operator": "equipped"}, {"type": "clothing_slot", "slot": "top", "operator": "unequipped"},
                   {"type": "clothing_slot", "slot": "dress", "operator": "unequipped"}, {"type": "worn_type", "operator": "neq", "value": "short_skirt"},
                   {"type": "worn_type", "operator": "neq", "value": "track_pants"},
                   {"type": "worn_type", "operator": "neq", "value": "gym_shorts"}, {"type": "worn_type", "operator": "neq", "value": "sheer_leggings"}),
              P("His eyes go straight to your tits in the sports bra and stay there while he talks.")),
            G(cond({"type": "clothing_item", "item_id": "gym_tank", "operator": "equipped"}, {"type": "worn_type", "operator": "neq", "value": "short_skirt"},
                   {"type": "worn_type", "operator": "neq", "value": "gym_shorts"}, {"type": "worn_type", "operator": "neq", "value": "sheer_leggings"}),
              P("He looks you up and down in the fitted gym tank."),
              D(J, "Nice. You actually came to train.")),
            G(cond({"type": "worn_type", "operator": "eq", "value": "track_pants"}, {"type": "clothing_item", "item_id": "tshirt", "operator": "equipped"}),
              D(J, "Track pants? You're hiding everything. Come on.")),
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
