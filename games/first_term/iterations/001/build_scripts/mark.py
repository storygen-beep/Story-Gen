"""Mark — steps 1-9 (Mark A 1-9), the Sunday table (the repeat), Vance's knock, the twist's
offer, his hubs. Source: sheets/scenes/mark_0*.md, sheets/people/npc_mark.md,
sheets/systems/money_pressure.md. Explicit screens pasted as signed."""
import os
from canv import *
from tomlw import tod, wd

M = "npc_mark"
V = "npc_vance"
out = []
HERE = os.path.dirname(os.path.abspath(__file__))

def done(n):
    return fset(f"mark_0{n}_done")

HIS = ntrait(M, "power", "gte", 50)   # his version (M)
HERS = ntrait(M, "power", "lt", 50)   # her version (E)
SHORT = flag("rent_carried")
FULL_ITEMS = [flag("rent_carried", False), flag("ryan_covered", False), flag("mark_money_week", False)]
BROKEN = cond(flag("rent_carried"), flag("ryan_covered"), flag("mark_money_week"), logic="OR")
SLEEP_SHIRT = {"type": "worn_type", "operator": "eq", "value": "sleep_shirt"}
COUNT_CLEAR = [funset("ryan_covered"), funset("mark_money_week"), fset("sunday_counted_today"), funset("grades_seen")]

def count_exits(text, dest, mins, eff=(), flags=(), consumes=False, node_=None):
    """The Sunday count's three exits: a clean Sunday adds to the streak (the fourth sets
    pays_her_own_way); a carried Sunday, Ryan's money or Mark's money breaks it."""
    kw = dict(mins=mins, consumes=consumes)
    if node_:
        kw["node"] = node_
    else:
        kw["loc"] = dest
    base_f = list(flags) + COUNT_CLEAR
    return [
        go(text, cond_=cond(*FULL_ITEMS, trait("paid_full_streak", "lt", 3)),
           eff=list(eff) + [add("paid_full_streak", 1, clamp=False), nadd(M, "power", -3)], flags=base_f, **kw),
        go(text, cond_=cond(*FULL_ITEMS, trait("paid_full_streak", "gte", 3)),
           eff=list(eff) + [add("paid_full_streak", 1, clamp=False), nadd(M, "power", -3)],
           flags=base_f + [fset("pays_her_own_way")], **kw),
        go(text, cond_=BROKEN, eff=list(eff) + [setv("paid_full_streak", 0), nadd(M, "power", 3)], flags=base_f, **kw),
    ]

STREAK_LINES = [
    G(cond(trait("paid_full_streak", "eq", 1)), P("One Sunday paid your way. He writes a small 1 on the back of the envelope and doesn't say anything about it.")),
    G(cond(trait("paid_full_streak", "eq", 2)), P("Two Sundays in a row, your own money. He notices. He doesn't like noticing.")),
    G(cond(trait("paid_full_streak", "gte", 3)), P("Sunday after Sunday, all of it, from your own pocket. He counts it like he's hoping it's wrong.")),
]

# ── step 1 · Mark A 1 · count it slowly ──
out.append({
    "id": "mark_01_count_it_slowly", "name": "Count it slowly",
    "description": "Mark step 1 (Mark A 1), her first Sunday at the table. The engine took the rent at midnight; this is Mark counting it with her there. Reads rent_carried. Counts the Sunday for the streak.",
    "trigger": step_trigger(M, 1),
    "nodes": [
        node("table", "The kitchen table", [
            IMG("scenes/mark_01_table.jpg", "a man in his forties at a kitchen table with an envelope of cash and a coffee, Sunday morning light",
                "man counting cash kitchen table morning", "stepfather kitchen table envelope of money"),
            P("Mark is at the kitchen table with the envelope of rent in front of him and a coffee going cold. Sunday. Laura's still upstairs. He looks up when you come in and his eyes go straight to your bare legs, and stay."),
            G(cond(SLEEP_SHIRT), P("You came down in your sleep shirt. It stops mid-thigh. He watches the hem the whole way to the table.")),
            D(M, "Sit. I count it in front of you. That way nobody says I took more than I did."),
            G(cond(flag("ryan_hall_seen")), P("Ryan leans in the doorway with a bowl of cereal, watching his father watch you.")),
        ], [
            go("\"Here.\"", node="count", mins=5),
            go("\"Let me get dressed first.\"", node="dressed", mins=5),
        ]),
        node("count", "The count", [
            G(cond(SHORT),
              P("He licks his thumb and counts the bills out onto the table, one at a time, slow. Slower than he needs to. You're short and you both know it, and he makes you sit through every bill of it."),
              D(M, "Seventy-five, I said.")),
            G(cond(flag("rent_carried", False)),
              P("You lean back in the chair and watch him lick his thumb and count. It's all there. Every bill."),
              ME("Count it slowly, Mark. Take your time."),
              P("He looks up. He doesn't like your tone. He counts slower anyway, and his eyes keep leaving the money.")),
        ], [
            go("\"Can you just — count it?\"", node="short", mins=3, cond_=cond(SHORT)),
            go("Watch him count.", node="short", mins=3, cond_=cond(flag("rent_carried", False))),
        ]),
        node("short", "I am counting", [
            D(M, "I am counting."),
            G(cond(SHORT), P("He writes the gap on the back of the envelope in pencil and taps it twice."), D(M, "The rest waits a week. Vance doesn't.")),
            G(cond(flag("rent_carried", False)), D(M, "That's the week. Same again Sunday.")),
            G(cond(SLEEP_SHIRT), D(M, "And not the shirt, next time.")),
            *STREAK_LINES,
            T("He counted you as much as the money."),
        ], count_exits("\"Fine.\"", "home_hall", 5, eff=[nadd(M, "want", 10), setv("mark_step", 1)], flags=[done(1)], consumes=True)),
        node("dressed", "Suit yourself", [
            D(M, "Suit yourself."),
            P("You go up and put clothes on and come back down. He's counted it without you. He pushes the envelope at you to look at, and doesn't look at you at all."),
            G(cond(SHORT), D(M, "Short. The rest waits a week.")),
        ], count_exits("Go back upstairs.", "home_hall", 15, eff=[setv("mark_step", 1)], flags=[done(1)], consumes=True)),
    ]})

# ── step 2 · Mark A 2 · the late notice ──
out.append({
    "id": "mark_02_late_notice", "name": "The late notice",
    "description": "Mark step 2 (Mark A 2), the kitchen drawer late at night, Mark on the phone next door. She learns his debt to Vance. Sets knows_mark_debt.",
    "trigger": step_trigger(M, 2, bind_npc=False),
    "nodes": [
        node("drawer", "The drawer", [
            P("You come down for water in the dark. The drawer by the fridge is open an inch, the way it never is. Under the takeaway menus there's a letter on thick paper, Vance's name printed at the top. LATE NOTICE, it says. And under it, a number with a lot of zeros."),
            P("Through the wall you can hear Mark in the living room, the TV low, his voice lower."),
        ], [
            go("Read it.", node="phone", mins=3, flags=[fset("knows_mark_debt")]),
            go("Shut the drawer.", loc="home_kitchen", mins=1, retry=2),
        ]),
        node("phone", "Friday, Frank", [
            P("You're on the second page when he comes into the doorway with his phone at his ear. He sees you. He sees what's in your hand. He doesn't hang up."),
            D(M, "Friday, Frank. I'll have it Friday. Yeah. Yeah. Friday."),
            P("He ends the call. He stands there with the phone at his side, looking at you, and for the first time in your life he looks like he's the one who owes."),
        ], [go("\"How late are we?\"", node="put", mins=2)]),
        node("put", "Put it back", [
            D(M, "Put it back."),
            P("He doesn't shout. He doesn't come for it. He just waits until you fold it along its creases and put it under the menus and shut the drawer, and then he goes back to his TV."),
            T("He knows you know. You've got something on him now."),
        ], [go("\"Okay.\"", loc="home_kitchen", mins=3, consumes=True,
               eff=[nadd(M, "want", 10), setv("mark_step", 2)], flags=[done(2)])]),
    ]})

# ── step 3 · Mark A 3 · shorts ──
SHORTS_ON = [{"action": "equip", "item_id": "tshirt"}, {"action": "equip", "item_id": "sleep_shorts"}]
out.append({
    "id": "mark_03_shorts", "name": "Shorts",
    "description": "Mark step 3 (Mark A 3), Sunday at the table: his dress rule. His version (Power 50+) asks; hers comes down in them first. The scene equips her sleep shorts. Sets mark_dress_rule.",
    "trigger": step_trigger(M, 3),
    "nodes": [
        node("start", "Sunday", [
            G(cond(HIS),
              P("Mark doesn't look up from the envelope when you come in."),
              D(M, "Not the shirt this time. Shorts. Since you're listening at doors now.")),
            G(cond(HERS),
              P("You come down in the shortest thing you own to sleep in, the pair that shows the curve of your ass when you walk. Mark looks up and stops with his thumb on a bill."),
              ME("Saved you asking.")),
        ], [
            go("\"Fine.\"", node="shorts", mins=5, cond_=cond(HIS), wardrobe=SHORTS_ON, eff=[nadd(M, "power", 3)]),
            go("\"I'm not changing for you.\"", node="no", mins=2, cond_=cond(HIS)),
            go("Sit down across from him.", node="shorts", mins=2, cond_=cond(HERS), wardrobe=SHORTS_ON, eff=[nadd(M, "power", -3)]),
        ]),
        node("shorts", "His count goes slow", [
            P("You sit. The chair is cold on the backs of your thighs. When you lean over to push the envelope at him, the shorts ride up and you feel his eyes go down the curve of your ass and stay there."),
            P("His count goes slow. He loses his place twice. He starts again."),
            D(M, "Every Sunday. Like that."),
            *STREAK_LINES,
        ], count_exits("\"Count, Mark.\"", "home_hall", 10,
                       eff=[nadd(M, "want", 10), add("exhibitionism", 3), setv("mark_step", 3)],
                       flags=[done(3), fset("mark_dress_rule")], consumes=True)),
        no_node("no", [D(M, "Suit yourself."), P("He counts it with his eyes on the money and not on you, and writes something on the back of the envelope that you don't get to see."), D(M, "Then the short stays on the tab, kid.")],
                "home_hall", 7, eff=[nadd(M, "power", -2)]),
    ]})

# ── step 4 · Mark A 4 · after she's asleep ──
out.append({
    "id": "mark_04_after_shes_asleep", "name": "After she's asleep",
    "description": "Mark step 4 (Mark A 4), the living room late: the ask. The introduction of his paid route (her climb).",
    "trigger": step_trigger(M, 4),
    "nodes": [
        node("start", "Late", [
            G(cond(HIS),
              P("Mark's on the couch with the TV low and a beer on his knee. Laura went up an hour ago. He doesn't look round when you come in, but he turns the TV down further."),
              D(M, "Come down after your mother's asleep. Some night. We'll talk about the rent.")),
            G(cond(HERS),
              P("Mark's on the couch with the TV low, the house dark round him. You sit on the arm of the couch beside him, close, your bare knee by his shoulder."),
              ME("What's the difference worth, Mark? Between what I pay and what you owe?")),
        ], [
            go("\"What for?\"", node="price", mins=5, cond_=cond(HIS), eff=[nadd(M, "power", 3)]),
            go("\"I'll pay it Sunday like everyone else.\"", node="no", mins=2, cond_=cond(HIS)),
            go("Wait for his answer.", node="price", mins=5, cond_=cond(HERS), eff=[nadd(M, "power", -3)]),
        ]),
        node("price", "The difference", [
            P("He looks at the ceiling, where Laura's asleep. Then he looks at your legs, for a long time, slowly, from your ankles up."),
            D(M, "You know what you're asking me, kid."),
            P("He doesn't answer it. Not yet. But he's thinking about a price, and he's letting you watch him think about it."),
            T("He's going to name a number. You want to hear it."),
        ], [go("\"Think about it.\"", loc="home_living_room", mins=5, consumes=True,
               eff=[nadd(M, "want", 10), setv("mark_step", 4)], flags=[done(4)])]),
        no_node("no", [P("He turns the TV back up without looking at you."), D(M, "Like everyone else. Sure, kid."), P("But he doesn't change the channel, and he doesn't stop watching you leave.")],
                "home_living_room", 3, eff=[nadd(M, "power", -2)]),
    ]})

# ── step 5 · Mark A 5 · a bill an inch (his voice sample; every screen as signed) ──
out.append({
    "id": "mark_05_a_bill_an_inch", "name": "A bill an inch",
    "description": "Mark step 5 (Mark A 5), his first paid touch: five an inch, cash, twenty tops. Two voices by his Power; a stop exit at ten. Sets mark_paid_touch.",
    "trigger": step_trigger(M, 5, retry_days=3),
    "nodes": [
        node("start", "Midnight", [
            G(cond(HIS),
              P("It's late, the house asleep, the TV muttering low. Mark sits on the couch with a folded bill between two fingers. \"You asked what the difference was worth, kid. Here it is.\" He pats the cushion beside him. \"Five for every inch my hand climbs your bare thigh. Cash. Twenty tops.\" His voice drops on the last word. He stares at your legs like a starving man. Then his eyes flick to the ceiling, where your mother sleeps. *He actually said it out loud.* You aren't scared of him, but you've already done the math. He holds the bill out and waits.")),
            G(cond(HERS),
              P("The house is asleep, but Mark is still on the couch, pretending to watch a TV he turned down low. You sit on the arm beside him. Then you put one bare leg across his lap. \"I asked what the difference was worth. Here's my answer,\" you say. \"Five for every inch your hand climbs. Cash. Twenty tops.\" He swallows. His eyes drop to your thigh and stay there. Then they go to the ceiling, where your mother is sleeping. \"Jesus, kid,\" he says, rough. He wants it, and it's all over his face. Your heart is pounding, but your leg stays put. You wait for his hand.")),
        ], [
            go("Sit down. ($5 an inch, to $20)", node="climb", mins=5, cond_=cond(HIS), eff=[nadd(M, "power", 3)]),
            go("\"Hands off, Mark.\"", node="no", mins=2, cond_=cond(HIS)),
            go("Let him. ($5 an inch, to $20)", node="climb", mins=5, cond_=cond(HERS), eff=[nadd(M, "power", -3)]),
            go("\"Not tonight.\"", node="no", mins=2, cond_=cond(HERS)),
        ]),
        node("climb", "Five. Ten.", [
            P("The TV mutters low. His rough palm settles on your bare knee, warm and heavy. \"Five,\" Mark breathes, and the hand slides up. Your breath goes quick and shallow. \"Ten.\" His thumb drags along the inside of your thigh, and your legs part a little for him. His cock is hard in his sweatpants, a thick ridge you can see from where you sit. Your nipples pull tight, and your tits ache with every short breath."),
            VID("a man's hand sliding up a girl's bare inner thigh on a couch at night, TV glow", "hand sliding up inner thigh couch night", "man paying to touch thigh living room tv glow", file="sex/mark_05_climb_t4.webm"),
        ], [
            go("\"Keep going.\" (to $20)", node="climb2", mins=3),
            go("\"That's far enough.\" ($10)", node="half", mins=2),
        ]),
        node("climb2", "Fifteen. Twenty.", [
            P("\"Fifteen.\" His fingers are shaking now, but they climb anyway, rough skin on soft. \"Twenty.\" He stops one inch short of the top of your thigh. His hand stays there, hot and trembling, while his cock twitches against the grey cotton."),
        ], [go("\"Keep going.\"", node="stop", mins=3)]),
        node("stop", "Not yet", [
            P("\"Keep going,\" you say. His hand stays where it is, one inch short of the top of your thigh. His jaw is tight. His cock strains against his sweatpants, hard and close enough to touch. His palm trembles on your skin, but it does not move up. \"Not yet, kid.\" Upstairs, a floorboard creaks. Your mother. You both freeze, his fingers still spread on your leg. He takes his hand back slowly. Then he lays four fives on your knee, right where his palm was. Your nipples are still hard, and your tits ache with it. Your legs stay open, and your thigh still burns where his hand was."),
            VID("four bills laid on a girl's bare knee on a couch at night, his hand pulling back", "money on bare knee couch night", "man pays girl lays cash on her thigh", file="sex/mark_05_stop_t4.webm"),
        ], [go("Take the money. ($20)", node="after", mins=2,
               eff=[{"targetType": "player", "trait": "money", "op": "add", "value": 20, "clamp": False}, add("corruption", 3), nadd(M, "want", 10)])]),
        node("half", "Ten", [
            P("You put your hand over his and press it still on your thigh. Mark freezes. His breath comes hard through his nose. Under his sweatpants his cock is a thick ridge, straining the cotton. He takes his hand back. He peels off two fives and lays them in your palm. Ten, not twenty. His eyes drop to your bare legs and stay there. Your tits ache, the nipples tight and hard. You keep your legs where they are a moment longer, on purpose. His cock jerks against the cotton."),
            VID("a girl presses a man's hand still on her thigh on a couch, two bills in her palm", "girl stops his hand on her thigh couch", "hand held still on bare thigh money in palm", file="sex/mark_05_half_t4.webm"),
        ], [go("Take it and go to bed. ($10)", loc="home_ella_room", mins=5, consumes=True,
               eff=[{"targetType": "player", "trait": "money", "op": "add", "value": 10, "clamp": False}, add("corruption", 3), nadd(M, "want", 10), setv("mark_step", 5)],
               flags=[done(5), fset("mark_paid_touch"), fset("mark_money_week")])]),
        node("after", "Twenty", [
            P("Four fives in your fist, still warm from Mark's wallet. He won't look at you. He turns the TV up until the room is only noise. \"Go to bed, kid,\" he says, rough. You climb the stairs and pass your mother's door. It's shut, but you walk past it slowly. *You just got paid to let your step-father touch you. It was the easiest twenty you ever made.* Sunday you pay your rent at the kitchen table with his own money. He'll sit across from you and count it, and you already want to know what he'll ask for next."),
        ], [go("Go to bed.", loc="home_ella_room", mins=5, consumes=True,
               eff=[setv("mark_step", 5)], flags=[done(5), fset("mark_paid_touch"), fset("mark_money_week")])]),
        node("no", "Hands off", [
            P("\"Hands off, Mark.\" His hand jerks off your thigh like it burned him. He folds the twenty and shoves it in his pocket. \"Suit yourself, kid. Rent's still Sunday.\" The no cost you twenty, nothing more. But he'll offer again, and you both know it. You walk to the stairs. His eyes follow you all the way up."),
        ], [go("Go to bed.", loc="home_ella_room", mins=3, retry=3)]),
    ]})

# ── step 6 · Mark A 6 · our arrangement ──
out.append({
    "id": "mark_06_our_arrangement", "name": "Our arrangement",
    "description": "Mark step 6 (Mark A 6), the garage: each holds the other's secret. Sets mark_arrangement.",
    "trigger": step_trigger(M, 6),
    "nodes": [
        node("start", "The garage", [
            P("Mark's at his workbench with the radio on and his hands black with oil. He's been off with you at dinner since the couch, eating with his eyes on his plate. He hears you come in and doesn't turn round."),
            G(cond(HIS), D(M, "Our arrangement. Your mother has enough to worry about. We understand each other.")),
            G(cond(HERS), ME("Vance's letter is in the drawer. And your hand was on my leg. So we each keep one.")),
        ], [
            go("\"Vance's letter is in the drawer.\"", node="keep", mins=5, cond_=cond(HIS), eff=[nadd(M, "power", -3)]),
            go("\"There's no arrangement.\"", node="no", mins=2, cond_=cond(HIS)),
            go("Wait for him to answer.", node="keep", mins=5, cond_=cond(HERS)),
        ]),
        node("keep", "We each keep one", [
            P("He wipes his hands on a rag, slowly, one finger at a time, and then he nods. Just once."),
            D(M, "Our arrangement."),
            T("Your secret for his. He thinks it's even. It isn't."),
        ], [go("\"Deal.\"", loc="home_hall", mins=3, consumes=True,
               eff=[nadd(M, "want", 10), setv("mark_step", 6)], flags=[done(6), fset("mark_arrangement")])]),
        no_node("no", [D(M, "There is now, kid. There has been since the couch."), P("He turns back to the bench. The radio fills the garage. You leave him to it, and your face is hot all the way up the stairs.")],
                "home_hall", 3, eff=[nadd(M, "power", 2)]),
    ]})

# ── step 7 · Mark A 7 · twenty, and you can look ──
out.append({
    "id": "mark_07_twenty_and_you_can_look", "name": "Twenty, and you can look",
    "description": "Mark step 7 (Mark A 7), Sunday at the table, Laura out shopping: she sets the price herself. The price on the button.",
    "trigger": step_trigger(M, 7, retry_days=7),
    "nodes": [
        node("count", "The rent, counted", [
            P("Laura's out shopping. Ryan's at the yard. The rent sits counted on the table between you, and Mark counts the twenties twice. He does that now."),
            P("On the fridge behind him, Laura's calendar. Wednesday says WORK LATE in blue."),
            G(cond(HIS), D(M, "Something you want to say, kid?")),
            G(cond(HERS), P("You don't wait for him to ask.")),
            *STREAK_LINES,
        ], count_exits("\"Twenty, and you can look.\"", None, 3, node_="look")
          + [go("\"Just the rent.\"", node="no", mins=2, cond_=cond(flag("sunday_counted_today", False)))]),
        node("look", "Look", [
            P("The rent sits counted on the kitchen table. You lay one more twenty on top of it yourself. \"Twenty, and you can look.\" Mark slides his own twenty across the wood first. \"Go on then, kid.\" You bare your tits for him under the kitchen light, and nothing sits between them and his eyes. The cold hits them. Your nipples go hard, tight and pointed straight at him. His breath goes short. His hand lies flat on the table, pressing white. His cock is hard under his jeans, a thick ridge straining the denim. You arch your back so your tits lift for him. He looks as long as the twenty buys, and you let him, your nipples aching in the cold while his eyes stay on them."),
            VID("a girl at a kitchen table baring her breasts for a man across from her, money on the table, morning light", "girl flashes tits at kitchen table for money", "topless girl kitchen table man staring cash", file="sex/mark_07_look_t4.webm"),
        ], [go("\"Time's up.\" ($20)", loc="home_hall", mins=10, consumes=True,
               eff=[{"targetType": "player", "trait": "money", "op": "add", "value": 20, "clamp": False}, add("exhibitionism", 3), nadd(M, "want", 10), setv("mark_step", 7)],
               flags=[done(7), fset("mark_money_week")])]),
        no_node("no", [G(cond(HIS), P("He slides his twenty back across the table to you anyway."), D(M, "Keep your twenty. It'll be here next week.")),
                       G(cond(HERS), P("He nods and puts his wallet away, slower than he took it out."), D(M, "Next week, then.")),
                       P("He folds the rent into the envelope with Vance's name on it.")],
                "home_hall", 7, eff=[nadd(M, "want", 2)], flags=COUNT_CLEAR),
    ]})

# ── step 8 · Mark A 8 · the red circle ──
out.append({
    "id": "mark_08_the_red_circle", "name": "The red circle",
    "description": "Mark step 8 (Mark A 8), Sunday afternoon: she circles Laura's late Wednesday on the fridge calendar.",
    "trigger": step_trigger(M, 8),
    "nodes": [
        node("calendar", "The calendar", [
            P("The family calendar is on the fridge under a magnet shaped like a lemon. Laura's writing in blue: dentist, Mark's mother, WORK LATE on Wednesday. Ryan's in green: league, Wednesday. You find the red pen in the drawer."),
        ], [
            go("Circle Wednesday.", node="see", mins=3),
            go("Never mind.", loc="home_kitchen", mins=1, retry=7),
        ]),
        node("see", "You'll see", [
            P("You draw a slow red circle round Wednesday evening. When you turn round, Mark is at the table with his paper, watching you over the top of it. His chair's pulled out beside him for nobody."),
            D(M, "What's that for?"),
            ME("You'll see."),
            T("Laura late. Ryan out. Just him, and his chair."),
        ], [go("\"Wednesday.\"", loc="home_hall", mins=3, consumes=True,
               eff=[nadd(M, "want", 10), setv("mark_step", 8)], flags=[done(8)])]),
    ]})

# ── step 9 · Mark A 9 · his chair (goal 1's body route) ──
out.append({
    "id": "mark_09_his_chair", "name": "His chair",
    "description": "Mark step 9 (Mark A 9), Wednesday evening, Laura late, Ryan out: she takes his chair. Goal 1's body route: sets pays_her_own_way.",
    "trigger": step_trigger(M, 9),
    "nodes": [
        node("chair", "His chair", [
            P("He's cooking, Wednesday, his back to you. You sit down in his chair at the head of the table and cross your legs and put a neat fold of your own money in front of you, and wait."),
            G(cond(HIS), P("He turns round with the spatula in his hand and stops dead."), D(M, "My chair.")),
            G(cond(HERS), P("He turns round and sees you, and he puts the spatula down. He comes and stands by the table. He doesn't sit. You push the money across the wood to him."),
              ME("Count it slowly, Mark.")),
        ], [
            go("\"Count it slowly, Mark.\"", node="count", mins=5, cond_=cond(HIS), eff=[nadd(M, "power", -5)]),
            go("\"No. I count.\"", node="no", mins=2, cond_=cond(HIS)),
            go("Watch him count.", node="count", mins=5, cond_=cond(HERS)),
        ]),
        node("count", "He counts standing", [
            P("He counts it standing up, like a man at somebody else's table. His voice is rough on the numbers. He's hard in his jeans, right there at the edge of the table where you can see, and he doesn't try to hide it, and he doesn't sit down until you tell him he can."),
            D(M, "It's all there."),
            ME("I know."),
            T("It's your table now. He knows it. His lap is right there, waiting, and you're not ready to give him that. Not yet."),
        ], [go("\"Good.\"", loc="home_hall", mins=5, consumes=True,
               eff=[nadd(M, "want", 10), setv("mark_step", 9)], flags=[done(9), fset("pays_her_own_way")])]),
        no_node("no", [D(M, "You count, do you."), P("He stands over you until you get up. Then he sits in his chair, heavily, and eats his chilli, and doesn't look at you once."), T("Not yet. But he moved."),],
                "home_kitchen", 7, eff=[nadd(M, "power", 3)]),
    ]})

# ── the twist's offer, after goal 1 (DIRECTION §2 · money sheet: the answer stays parked) ──
out.append({
    "id": "debt_offer", "name": "How far behind",
    "description": "The twist's offer after goal 1 (pays_her_own_way): she learns how far the house is behind with Vance. Sets debt_offer_seen. Her answer stays parked until 0.2.",
    "trigger": {"location": "home_kitchen", "npc": M, "requires_npc": M, "is_repeatable": False,
                "priority": 11, "is_active": True, "consume_on": "exit", "retry_after_days": 7,
                "schedules": [{"weekdays": [6], "start_time": "08:00", "end_time": "22:00"},
                              {"weekdays": [2], "start_time": "18:00", "end_time": "22:00"}],
                "conditions": cond(flag("pays_her_own_way"), flag("debt_offer_seen", False))},
    "nodes": [
        node("letters", "The letters", [
            P("Mark has every letter out of the drawer, spread across the kitchen table in a fan. Vance's name on all of them. He doesn't hide them when you come in. He hasn't hidden anything from you for a while."),
            D(M, "You pay your way now. So you get to see what your way pays into."),
            P("He turns the last one round so you can read it. It isn't the rent. It's the house. Mark borrowed against it years ago, and the number at the bottom is bigger than anything you've ever seen written down."),
            D(M, "Vance could have it back any month he likes. He knows it. I know it. Now you know it."),
            T("Your rent every week is a drop in that. And he's asking you something without asking."),
        ], [
            go("\"Let me think about it.\"", loc="home_kitchen", mins=10, retry=7, flags=[fset("debt_offer_seen")]),
            go("\"It's not my debt, Mark.\"", node="refuse", mins=5),
        ]),
        no_node("refuse", [D(M, "No. It's not."), P("He gathers the letters into a pile and squares the edges against the table, one by one, and doesn't look at you."), D(M, "Rent's Sunday. Same as ever.")],
                "home_kitchen", 14, eff=[nadd(M, "power", 3)], flags=[fset("debt_offer_seen"), fset("debt_refused")]),
    ]})

# ── the Sunday table: the repeat (mark_09 sheet; money sheet: the count, his terms or hers) ──
HERS_LOOK = open(os.path.join(HERE, "beat_mark_table_look_hers.txt")).read().strip() if os.path.exists(os.path.join(HERE, "beat_mark_table_look_hers.txt")) else "PLACEHOLDER"
BOLD_HIS = open(os.path.join(HERE, "beat_mark_table_look_his_bold.txt")).read().strip()
BOLD_HERS = open(os.path.join(HERE, "beat_mark_table_look_hers_bold.txt")).read().strip()
out.append({
    "id": "mark_sunday_table", "name": "Sit down at the table",
    "description": "The Sunday count, the repeat after Mark's step 1: his terms or hers by his Power; the streak counts here when no step has counted it. From Bold, after his step 7: \"Twenty, and you can look\", two voices, a stop exit. Once a Sunday.",
    "trigger": {"location": "home_kitchen", "requires_npc": M, "is_repeatable": True, "priority": 5,
                "is_active": True, "max_triggers_per_day": 1,
                "schedules": [{"weekdays": [6], "start_time": "08:00", "end_time": "12:00"}],
                "conditions": cond(trait("mark_step", "gte", 1), flag("sunday_counted_today", False), flag("rent_starts"))},
    "nodes": [
        node("table", "The Sunday table", [
            G(cond(HIS), P("Mark's at the table with the envelope, the way he is every Sunday. He doesn't say good morning. He points at the chair across from him with his pen."),
              D(M, "Sit. Watch me count.")),
            G(cond(HERS), P("Mark's at the table with the envelope. He stands up when you come in, and he doesn't sit back down until you've sat."),
              D(M, "Morning. Go on, then.")),
            G(cond(flag("mark_dress_rule"), {"type": "worn_type", "operator": "eq", "value": "shorts"}),
              P("You're in the shorts. His rule. He sees them and his count slows before he's started.")),
            G(cond(flag("mark_dress_rule"), {"type": "worn_type", "operator": "neq", "value": "shorts"}),
              D(M, "That's not what I asked you to wear to my table.")),
            G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), D(M, "That's what you wear to my table?")),
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "worn_exposure", "operator": "eq", "value": 0}),
              D(M, "Sit down. You're making me lose count.")),
            G(cond({"type": "worn_exposure", "operator": "eq", "value": 1}, {"type": "worn_type", "operator": "neq", "value": "towel"}, {"type": "worn_type", "operator": "neq", "value": "sleep_shirt"}),
              D(M, "Your mother's upstairs."), P("He doesn't tell you to cover up.")),
            G(cond(SHORT), P("He counts it slow, and it's short, and he writes the gap on the envelope in pencil without a word.")),
            G(cond(flag("rent_carried", False)), P("It's all there. He counts it twice anyway, because he wants to sit here longer.")),
            *STREAK_LINES,
            D(M, "Next Sunday. Same table."),
        ], count_exits("\"Count it, Mark.\"", None, 15, eff=[nadd(M, "want", 2)], node_="counted")),
        node("counted", "Counted", [
            P("He folds the rent into the envelope with Vance's name on it and leaves his hand flat on top of it."),
            G(cond(trait("mark_step", "gte", 7)), P("His eyes go to you and stay. He counts the twenties in his wallet without taking them out.")),
        ], [
            go("\"Twenty, and you can look.\" ($20)", node="look_his", mins=3,
               cond_=cond(trait("mark_step", "gte", 7), trait("corruption", "gte", 40), HIS)),
            go("\"Twenty, and you can look.\" ($20)", node="look_hers", mins=3,
               cond_=cond(trait("mark_step", "gte", 7), trait("corruption", "gte", 40), HERS)),
            go("Leave him to his envelope.", loc="home_kitchen", mins=2),
        ]),
        node("look_his", "Look (his terms)", [
            G(cond(trait("corruption", "lt", 50)), P("The rent sits counted on the kitchen table. You lay one more twenty on top of it yourself. \"Twenty, and you can look.\" Mark slides his own twenty across the wood first. \"Go on then, kid.\" You bare your tits for him under the kitchen light, and nothing sits between them and his eyes. The cold hits them. Your nipples go hard, tight and pointed straight at him. His breath goes short. His hand lies flat on the table, pressing white. His cock is hard under his jeans, a thick ridge straining the denim. You arch your back so your tits lift for him. He looks as long as the twenty buys, and you let him, your nipples aching in the cold while his eyes stay on them.")),
            G(cond(trait("corruption", "gte", 50)), P(BOLD_HIS)),
            VID("a girl baring her breasts at a kitchen table for a man who pays first, Sunday morning", "girl topless kitchen table man pays to look", "flash tits for money kitchen stepfather", pool_dir="sex/mark_table_look_his_t4"),
        ], [
            go("\"Time's up.\" ($20)", loc="home_kitchen", mins=10,
               eff=[{"targetType": "player", "trait": "money", "op": "add", "value": 20, "clamp": False}, {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 59}],
               flags=[fset("mark_money_week")]),
            go("Cover up. Give him his twenty back.", node="cover", mins=2),
        ]),
        node("look_hers", "Look (your terms)", [
            G(cond(trait("corruption", "lt", 50)), P(HERS_LOOK)),
            G(cond(trait("corruption", "gte", 50)), P(BOLD_HERS)),
            VID("a girl in charge at a kitchen table baring her breasts, a man staring, money under her hand", "girl flashes breasts kitchen table takes his money", "topless young woman kitchen table older man staring", pool_dir="sex/mark_table_look_hers_t4"),
        ], [
            go("\"Time's up.\" ($20)", loc="home_kitchen", mins=10,
               eff=[{"targetType": "player", "trait": "money", "op": "add", "value": 20, "clamp": False}, {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 59}],
               flags=[fset("mark_money_week")]),
            go("Cover up. Give him his twenty back.", node="cover", mins=2),
        ]),
        node("cover", "Covered", [
            P("You cover up before the twenty's spent and push the bill back across the table. He stares at it, then at you."),
            D(M, "Your call, kid."),
            P("He doesn't pick the money up until you've left the room."),
        ], [go("Go.", loc="home_kitchen", mins=3, eff=[nadd(M, "want", 2)])]),
    ]})

# ── Vance's knock after a short Sunday (money sheet: the next evening; once per carried week) ──
out.append({
    "id": "vance_knock", "name": "Answer the door",
    "description": "Vance at the front door the evening after a short Sunday. Clears rent_carried; Vance's Power +10 (each carried Sunday). At Power 60 he asks for her, not Mark.",
    "trigger": {"location": "home_front_door", "is_repeatable": True, "priority": 6, "is_active": True,
                "schedules": [{"weekdays": [0, 1, 2, 3, 4, 5], "start_time": "18:00", "end_time": "22:00"}],
                "conditions": cond(flag("rent_carried"), flag("vance_met")), "max_triggers_per_day": 1},
    "nodes": [
        node("knock", "Vance", [
            P("Three knocks, slow and heavy, the way a man knocks on a door he owns. Mr. Vance is on the step in his cardigan, with an envelope in his hand."),
            G(cond(ntrait(V, "power", "lt", 60)),
              D(V, "Evening, Miss. Is your stepfather in? Tell him I came by about Sunday. He'll know."),
              P("He hands you the envelope. His fingers stay on it a second after yours close.")),
            G(cond(ntrait(V, "power", "gte", 60)),
              D(V, "I didn't come for Mark. I came for you, Miss. You're the one who pays in that house now, aren't you?"),
              P("He looks past you into the hall, then back at you, slow, all the way down and up."),
              D(V, "Come and see me one evening. We'll talk about what's owed.")),
            G(cond(ntrait(V, "want", "gte", 30)), P("He doesn't look at your face once while he says it.")),
            T("A short week, and it comes to the door."),
        ], [
            go("\"Mark will pay.\" Close the door.", node="shut", mins=5, eff=[nadd(V, "power", 10)], flags=[funset("rent_carried")]),
            go("\"Maybe one evening.\"", node="maybe", mins=5, cond_=cond(ntrait(V, "power", "gte", 60)),
               eff=[nadd(V, "power", 10), nadd(V, "want", 3)], flags=[funset("rent_carried")]),
        ]),
        node("shut", "The door", [D(V, "He'd better, Miss."), P("He touches the brim of a hat he isn't wearing and goes back down the path, slow. You lock the door. Through the glass you watch him stop on his own porch and look back.")],
             [go("Go back in.", loc="home_front_door", mins=3)]),
        node("maybe", "One evening", [D(V, "Maybe's a start."), P("He smiles like you've signed something, and goes. The envelope in your hand is warm from his fingers.")],
             [go("Go back in.", loc="home_front_door", mins=3)]),
    ]})

# ── his hubs: the living room late, the garage, the kitchen ──
MARK_STATE_LINES = [
    G(cond(SLEEP_SHIRT), P("His thumb rubs the edge of whatever he's holding. His eyes are on the hem of your sleep shirt.")),
    G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), D(M, "That's what you wear in my house?")),
    G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "worn_exposure", "operator": "eq", "value": 0}), D(M, "Sit down. You're making me lose my place.")),
    G(cond({"type": "worn_exposure", "operator": "eq", "value": 1}, {"type": "worn_type", "operator": "neq", "value": "towel"}, {"type": "worn_type", "operator": "neq", "value": "sleep_shirt"}),
      D(M, "Your mother's upstairs."), P("He doesn't tell you to cover up.")),
]
LEAKS_LATE = [
    G(cond(trait("mark_step", "eq", 1)), P("His eyes go to your hem and back to the TV, every time you move.")),
    G(cond(trait("mark_step", "eq", 3)), P("He stays up later than he used to. Laura's been asleep an hour.")),
    G(cond(trait("mark_step", "eq", 4)), P("There's a folded bill on the arm of the couch, under his hand. Waiting.")),
]
LEAKS_GARAGE = [
    G(cond(trait("mark_step", "eq", 5)), P("He can't hold your look. He hasn't been able to since the couch.")),
]
LEAKS_KITCHEN = [
    G(cond(trait("mark_step", "eq", 2)), P("His eyes go to your hem and stay, the way they did at the first count.")),
    G(cond(trait("mark_step", "eq", 7)), P("His chair is pulled out from the table for nobody.")),
    G(cond(trait("mark_step", "eq", 8)), P("He keeps looking at the fridge. At the red circle.")),
]
def mark_hub(cid, loc, name, setting, extra=(), awake=True, leaks=()):
    return {"id": cid, "name": name,
            "description": f"Mark's hub: {setting}. His Want and Power colour it; his lines read what she wears.",
            "trigger": {"location": loc, "npc": M, "requires_npc": M, "is_repeatable": True, "priority": 6,
                        "is_active": True, "conditions": cond(flag("opening_done"))},
            "nodes": [node("hub", name, [*extra] + ([*MARK_STATE_LINES, *leaks,
                G(cond(ntrait(M, "power", "lt", 40)), P("He doesn't give you orders any more. He waits to hear what you want.")),
                G(cond(ntrait(M, "power", "gte", 60)), P("He looks at you like you're one more thing in this house that's his.")),
                G(cond(ntrait(M, "want", "gte", 50)), T("He wants you. He's stopped trying to hide it from you, only from her.")),
            ] if awake else []), [go("Leave him to it.", loc=loc)])]}

out.append(mark_hub("hub_mark_living_room", "home_living_room", "Mark, up late", "the living room late", [
    P("Mark is on the couch with the TV low and a beer on his knee. Laura's asleep upstairs."),
    POOL(D(M, "Can't sleep, kid?"), D(M, "Shut the door. Your mother's sleeping."), D(M, "Sit if you're sitting. Don't hover."), pid="mark_late_lines"),
], leaks=LEAKS_LATE))
out.append(mark_hub("hub_mark_bedroom", "home_master_bedroom", "Mark, asleep", "their bed, at night", [
    P("Mark is asleep on his back on his side of the bed, snoring, one arm flung out. Even asleep he takes up most of it."),
], awake=False))
out.append(mark_hub("hub_mark_garage", "home_garage", "Mark, in the garage", "the garage", [
    P("Mark's at his bench with the radio on, doing something to an engine part that doesn't need doing."),
    POOL(D(M, "Hand me that wrench. No, the other one."), D(M, "Don't touch anything."), D(M, "What do you want? I'm busy."), pid="mark_garage_lines"),
], leaks=LEAKS_GARAGE))
out.append(mark_hub("hub_mark_kitchen", "home_kitchen", "Mark, in the kitchen", "the kitchen", [
    G(cond(wd(2)), P("Wednesday. Mark's cooking, badly, with a beer on the counter and the extractor fan roaring."), D(M, "It's chilli. It's always chilli.")),
    G(cond(wd(6)), P("Sunday. Mark's at the table with the paper and his coffee, in the chair at the head of it."), D(M, "Morning.")),
], leaks=LEAKS_KITCHEN))

cards = step_cards(M, {
    1: ("Sunday. Mark counts the rent at the kitchen table.", "Sunday morning: the kitchen, while Mark counts the rent"),
    2: ("His eyes were on your hem at the count. He's on the phone a lot, late.", "Late at night: the kitchen drawer, Mark next door"),
    3: ("\"Friday, Frank.\" He knows you heard. Sunday's coming.", "Sunday morning at the table (Curious, Daring)"),
    4: ("He stays up after Laura's asleep.", "Late at night in the living room, Laura asleep (Bold)"),
    5: ("\"What's the difference worth?\" He's thought about it.", "Late at night in the living room, close to midnight (Bold)"),
    6: ("He can't look at you at dinner. He wants to talk terms.", "An evening in the garage, while Mark is out there (Bold)"),
    7: ("He counts the twenties twice now.", "Sunday morning at the table, Laura out (Bold, Showing)"),
    8: ("The fridge calendar has Laura's late Wednesday on it.", "Sunday afternoon in the kitchen, at the fridge (Bold)"),
    9: ("Wednesday. Laura late, Ryan out. His chair.", "Wednesday evening in the kitchen: take Mark's chair (Bold, Showing)"),
}, terminal_text=("The Sunday table is yours: his terms or yours, and his lap waiting.", "Mark's next step comes in the next release."),
   closed_text="You told him you'd tell Mom. The rent is strict now, every Sunday, and nothing else.")
for c in cards:
    c["when"].append({"flag": "opening_done", "op": "is_true"})

text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · MARK (sheets/scenes/mark_0*.md, people/npc_mark.md, systems/money_pressure.md)\n"
        "# Steps 1-9, the Sunday table, Vance's knock, the twist's offer, his hubs, his cards.\n"
        "# =============================================================================\n")
text += "".join(emit(c) for c in out) + "".join(emit_card(c) for c in cards)
open(__import__("sys").argv[1], "w").write(text)
print("mark:", len(out), "canvases,", len(cards), "cards", "(her table voice:", "placeholder" if HERS_LOOK == "PLACEHOLDER" else "written", ")")
