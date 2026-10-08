"""Jake — steps 2-3 (Jake B 2-3; step 1 is Zoe's first party, step 4 is Laura's step 5), the date
pickup, the Saturday goodnight (the repeat), his hubs. Source: sheets/scenes/jake_*.md, people/npc_jake.md."""
from canv import *
from tomlw import tod, wd

J = "npc_jake"
R = "npc_ryan"
L = "npc_laura"
out = []

def done(n):
    return fset(f"jake_0{n}_done")

SKIRT = {"type": "worn_type", "operator": "eq", "value": "short_skirt"}
LAURA_DRESS = {"type": "clothing_item", "item_id": "laura_blue_dress", "operator": "equipped"}
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
            go("\"Hi.\"", node="kiss", mins=3),
            go("\"Not now.\"", node="no", mins=2),
        ]),
        node("kiss", "In front of them", [
            P("He kisses you right there, in front of all of them, his hand low on your back, low enough that it's on your ass by the end. Somebody whistles. He pulls back grinning."),
            D(J, "Again. They missed it."),
            T("He wants them to see you're his. You want them to see too."),
        ], [go("\"Again.\"", node="ask", mins=3, eff=[add("exhibitionism", 3)])]),
        node("ask", "Saturday", [
            P("You kiss him longer this time, long enough that the guys stop whistling and start looking at the grass."),
            ME("Saturday. Pick me up at the door."),
            D(J, "Saturday."),
        ], [go("\"Saturday.\"", loc="quad", mins=5, consumes=True,
               eff=[setv("jake_step", 2), nadd(R, "warmth", -5)], flags=[done(2), fset("jake_date_booked")])]),
        no_node("no", [D(J, "Later, then. I'll be here."), P("The guys jeer at him. He shoves the nearest one and grins after you all the way across the quad.")], "quad", 2),
    ]})

# ── step 3 · Jake B 3 · my boyfriend (the voice sample; every screen as signed) ──
out.append({
    "id": "jake_03_my_boyfriend", "name": "My boyfriend",
    "description": "Jake step 3 (Jake B 3), the voice sample: Saturday night at the front door after a date; she names him to the house. Ryan opens the door from inside.",
    "trigger": step_trigger(J, 3, retry_days=7),
    "nodes": [
        node("porch", "The porch", [
            P("Jake walks you up to the porch and stops under the light. The downstairs is dark. He looks past you at the windows, then up at the second floor. \"Is anyone up?\" He sounds like he hopes so. \"Nobody,\" you say. \"Not yet.\" Upstairs, Ryan's window is lit, right above the porch. He's home. You want him to look. \"Shame,\" Jake says. \"I want them to see you're mine, @player.\" His hand slides down your back and settles on your ass. You should move it, but you like being shown off. He leans in, and his mouth stops an inch from yours."),
        ], [
            go("Kiss him.", node="rail", mins=3),
            go("\"Goodnight, Jake.\"", node="no", mins=2),
        ]),
        node("rail", "The rail", [
            P("You kiss him first, right there under the porch light. Jake makes a low sound and lifts you onto the rail like you weigh nothing. Your legs lock round his waist. His hands sit on your hips, then slide down to grab your ass. \"God, @player,\" he breathes into your mouth. It gets hungry and loud, all teeth and breath. The rail creaks every time he pulls you closer. Anyone inside could hear it, but you don't care. You want more of his mouth. Then, behind you, the lock turns."),
        ], [go("\"Don't stop.\"", node="ryan", mins=3)]),
        node("ryan", "Ryan", [
            P("The front door opens behind you. Ryan stands in the doorway and stops dead. You're on the porch rail with your legs locked round Jake's waist, kissing him. Jake's hands are full of your ass. You don't climb down. You look straight at Ryan over Jake's shoulder and hold it. \"Ryan, this is Jake. My boyfriend.\" Ryan's jaw goes tight. His eyes drop to Jake's hands on you, then come back to your face. \"Great.\" Jake grins over his shoulder, not getting it. \"Your brother hates me.\" *Good. Look all you want, Ryan.* Ryan steps back inside without another word. The door slams hard."),
        ], [go("\"Goodnight, Jake.\"", node="after", mins=5, eff=[nadd(R, "warmth", -10), nadd(R, "want", 5)])]),
        node("after", "Next Saturday", [
            P("Jake goes off down the path, whistling. You let yourself in and climb the stairs. Ryan's door is shut, and his light is on under it. You stand outside it a second. You don't knock, but you don't move either. You wanted him to see. You said Jake's name to his face on purpose, and you're not sorry. Not even a little. Jake will want a next Saturday. You already know it. Your phone buzzes in your hand. It's Jake: \"Next Saturday?\" Under Ryan's door, the light goes out."),
        ], [go("Go to bed.", loc="home_ella_room", mins=5, consumes=True,
               eff=[setv("jake_step", 3)], flags=[done(3), funset("jake_date_booked")])]),
        node("no", "A kiss on the cheek", [
            P("You kiss his cheek, quick, and step back before he can turn it into more. Jake wanted the porch rail. It's all over his face, but he lets it go. \"Okay, @player. Next Saturday, then?\" He's disappointed, and somehow he's grinning harder than before. \"Next Saturday,\" you say, and your stomach flips. Jake walks backwards down the path, still grinning at your door."),
        ], [go("Go in.", loc="home_hall", mins=3, retry=7, flags=[funset("jake_date_booked")])]),
    ]})

# ── the date: Jake picks her up at the door on a booked Saturday; the curfew refuses it ──
BACK_AT_11 = [(("19:00", "20:00"), 240), (("20:00", "21:00"), 180)]
out.append({
    "id": "jake_date_pickup", "name": "Jake's at the door",
    "description": "A booked Saturday: Jake picks her up; dinner, a film, the walk back. Lands her at the front door after eleven (where his steps and the goodnight play). The curfew refuses it (SYSTEMS §12).",
    "trigger": {"location": "home_front_door", "is_repeatable": True, "priority": 6, "is_active": True,
                "max_triggers_per_day": 1,
                "schedules": [{"weekdays": [5], "start_time": "19:00", "end_time": "21:00"}],
                "conditions": cond(flag("jake_date_booked"), flag("jake_met"))},
    "nodes": [
        node("door", "The doorbell", [
            P("The doorbell goes. Jake's on the step in a clean shirt with his hair still wet, holding his car keys like a man in an advert."),
            G(cond(LAURA_DRESS), D(J, "Whoa. Okay. Everyone's going to be looking at you tonight.")),
            G(cond(SKIRT), P("His eyes go down your legs and stay there.")),
            D(J, "Ready? I booked the place with the candles. Don't laugh."),
            G(CURFEW_ON, P("Behind you, Laura's voice from the kitchen: \"She's grounded, Jake. Goodnight.\"")),
        ], [
            go("Go out with him.", node="date", mins=10, cond_=NO_CURFEW),
            go("\"I'm grounded. Next week.\"", loc="home_front_door", mins=5, cond_=CURFEW_ON, flags=[funset("jake_date_booked")]),
            go("\"Not tonight, Jake.\"", node="no", mins=2),
        ]),
        node("date", "The date", [
            POOL(
                P("Dinner at the place with the candles. He talks about the team, and the coach, and a guy who threw up on the bus, and you laugh in the right places. He holds your hand on the table where the whole restaurant can see it. Afterwards he walks you the long way home with his arm round your waist."),
                P("A film you don't watch. He has his arm round you from the trailers, and his hand on your knee from the first scene, and every time somebody comes down the aisle he kisses you so they'll see. You walk home through the park, slowly."),
                pid="jake_date_lines"),
            D(J, "You're the best-looking girl in this whole town, you know that? Everyone was looking."),
        ], [go("Walk home with him.", loc="home_front_door", mins=m, cond_=cond(tod(a, b))) for (a, b), m in BACK_AT_11]),
        node("no", "Not tonight", [D(J, "Oh. Okay. Next week?"), P("He stands on the step for a second with his keys, then goes. He texts you from the car before he's even started it.")],
             [go("Close the door.", loc="home_front_door", mins=2, flags=[funset("jake_date_booked")])]),
    ]})

# ── the Saturday goodnight at the door: the repeat (jake_saturday_date sheet) ──
out.append({
    "id": "jake_saturday_date", "name": "Kiss Jake goodnight",
    "description": "The goodnight at the front door after a date. Curious: a long kiss on the rail; Bold: his hands, her turning him so the dark room can see. Who notices rotates by who is home. Clears the booking. Corruption +1 until past Bold.",
    "trigger": {"location": "home_front_door", "requires_npc": J, "is_repeatable": True, "priority": 5, "is_active": True,
                "max_triggers_per_day": 1,
                "schedules": [{"weekdays": [5], "start_time": "22:00", "end_time": "00:00"}],
                "conditions": cond(flag("jake_date_booked"), trait("jake_step", "gte", 1))},
    "nodes": [
        node("door", "The porch light", [
            P("Jake walks you up to the porch and stops under the light, and doesn't let go of your hand."),
            G(cond(LAURA_DRESS), D(J, "Everyone was looking at you tonight.")),
            G(cond(trait("corruption", "lt", 40)),
              P("He kisses you on the step, slow, then not slow, and lifts you onto the porch rail, and you lock your legs round him and kiss him until the rail creaks.")),
            G(cond(trait("corruption", "gte", 40)),
              P("You kiss him hard on the step and turn him, slowly, so his back is to the street and the dark living-room window can see the two of you. His hands go down to your ass and squeeze, and you push into them.")),
            G(cond(SKIRT, trait("corruption", "gte", 40)), P("His hands slide up under the hem of your skirt, and you let them.")),
        ], [
            go("Kiss him.", node="watch", mins=10),
            go("\"Goodnight, Jake.\"", node="night", mins=2),
            go("Take him round the side of the house.", node="wall", swl=True, cond_=cond(trait("corruption", "gte", 60))),
        ]),
        node("watch", "Who's watching", [
            G(cond({"type": "npc_at_location", "location_id": "home_living_room", "npc_id": L, "operator": "is_present"}),
              P("In the dark living-room window, a shape on the couch hasn't moved. Laura, waiting up. She doesn't look away, and Jake doesn't know.")),
            G(cond({"type": "npc_at_location", "location_id": "home_ryan_room", "npc_id": R, "operator": "is_present"}),
              P("Ryan's light is on above the porch. His curtain moves.")),
            D(J, "Same time next Saturday?"),
        ], [go("Let them look.", loc="home_hall", mins=5, flags=[funset("jake_date_booked")],
               eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 59}])]),
        node("night", "Goodnight", [D(J, "Goodnight, gorgeous. Same time next week."), P("He kisses your hand like an idiot and walks backwards down the path.")],
             [go("Go in.", loc="home_hall", mins=2, flags=[funset("jake_date_booked")])]),
        node("wall", "Further", [
            P("You take his hand and pull him round the side of the house, where the porch light doesn't reach."),
            P("What happens next with Jake is in the next release of First Term."),
        ], [go("Go in.", loc="home_hall", mins=5, flags=[funset("jake_date_booked")])]),
    ]})

# ── his hubs: the quad (mornings), the canteen (lunch), Zoe's party ──
JAKE_STATE = [
    G(cond(SKIRT), D(J, "Guys. Look at her."), P("He says it to whoever's nearest.")),
    G(cond(ZOE_DRESS), P("His eyes go down your legs and stay there.")),
    G(cond(LAURA_DRESS), D(J, "Everyone was looking at you tonight.")),
    G(cond(trait("jake_step", "eq", 1)), P("He puts his hand low on your back the second you're close enough.")),
    G(cond(trait("jake_step", "eq", 2)), D(J, "Your brother hates me. I can tell from here.")),
    G(cond(trait("jake_step", "eq", 3)), D(J, "Is your mom up, when I bring you home? She seems cool.")),
]
for cid, loc, name, line in [("hub_jake_quad", "quad", "Jake, with the team", "Jake's on the grass with his team. He waves you over without getting up, so they'll all see you come."),
                              ("hub_jake_canteen", "canteen", "Jake, at lunch", "Jake has a tray with three of everything on it. He pulls you onto the bench next to him."),
                              ("hub_jake_party", "zoe_apartment", "Jake, at the party", "Jake's by the kitchen with a beer, watching the door for you.")]:
    out.append({
        "id": cid, "name": name,
        "description": f"Jake's hub ({loc}): he shows her off.",
        "trigger": {"location": loc, "npc": J, "requires_npc": J, "is_repeatable": True, "priority": 6, "is_active": True,
                    "conditions": cond(flag("jake_met"))},
        "nodes": [node("jake", name, [
            P(line),
            POOL(D(J, "There she is."), D(J, "C'mere. Sit on my knee. They don't believe me about you."), D(J, "Saturday? Say Saturday."), pid=f"{cid}_lines"),
            *JAKE_STATE,
        ], [go("Stay with him a while.", loc=loc, mins=20), go("Go.", loc=loc)])]})

cards = step_cards(J, {
    1: ("", ""),
    2: ("He's got your number. He hangs out on the quad with his team.", "A Monday, Wednesday or Friday morning on the quad, Jake and his team (Curious, Daring)"),
    3: ("Saturday. He picks you up at the door.", "Saturday night: a date with Jake, back to the front door after eleven (Curious, Daring)"),
    4: ("\"Is your mom up?\" She waits up on Saturdays.", "Saturday night after a date: kiss Jake goodnight at the front door (Bold, Showing; Laura's step 4 first)"),
}, met_flag="jake_met", terminal_text=("Saturdays: a date, the door, and whoever's watching.", "Jake's next step comes in the next release."), skip=(1,))

text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · JAKE (sheets/scenes/jake_*.md, people/npc_jake.md)\n"
        "# Steps 2-3 (step 1 is zoe_01_first_party, step 4 is laura_05_jake_at_the_door), the date,\n"
        "# the Saturday goodnight, his hubs, his cards.\n"
        "# =============================================================================\n")
text += "".join(emit(c) for c in out) + "".join(emit_card(c) for c in cards)
open(__import__("sys").argv[1], "w").write(text)
print("jake:", len(out), "canvases,", len(cards), "cards")
