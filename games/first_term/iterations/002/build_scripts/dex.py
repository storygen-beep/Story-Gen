"""Dex, the trainer at the street gym (LO, 2026-11-10: "Gym trainer too", "you can decide one", "Yes, go ahead";
DECISIONS 225). Source: sheets/people/npc_dex.md (signed 2026-11-10) and the ledger (v2_state.json board.characters
npc_dex). Five steps, his hub on the gym floor, the sessions ($15, or from his step 3 "another way") and after hours,
his repeat.

Every step and repeat opens from his portrait (DECISIONS 224): the steps bind him (npc set, priority 10, so his
portrait shows the step while it is ready); the sessions and after hours are buttons in his hub.

After hours: the gym shuts at 21:00 for her and a closed room can't be entered, so his after-hours button shows on
the floor 20:30-21:00 and the scene runs on past close inside one canvas, then lets her out onto the street. His
sheet's 21:00-22:00 locker-room row is built this way (the sheet's own note, gym.md "After closing").
"""
from canv import *
from tomlw import tod, wd
from gymkit import CHECKED_IN, kits, GYM_A, GYM_B
import doors   # DECISIONS 224: his repeat opens from his portrait

DX, J = "npc_dex", "npc_jake"
out = []
CURIOUS, BOLD, HUNGRY = trait("corruption", "gte", 20), trait("corruption", "gte", 40), trait("corruption", "gte", 60)
SESSION = flag("dex_session_today", False)
AFTER = flag("dex_after_today", False)
SHEER = {"type": "worn_type", "operator": "eq", "value": "sheer_leggings"}
SHORTS = {"type": "worn_type", "operator": "eq", "value": "gym_shorts"}
LEGGINGS = {"type": "worn_type", "operator": "eq", "value": "leggings"}
TRACK = {"type": "worn_type", "operator": "eq", "value": "track_pants"}
SPORTS_ALONE = [{"type": "clothing_item", "item_id": "sports_bra", "operator": "equipped"},
                {"type": "clothing_slot", "slot": "top", "operator": "unequipped"}]
ANY = [{"type": "worn_exposure", "operator": "gte", "value": 0}]
JAKE_HERE = {"type": "npc_at_location", "location_id": "gym_floor", "npc_id": J, "operator": "is_present"}
WORKOUT = [add("energy", -15)]
WORKOUT_COST = [{"trait": "energy", "value": 15}]
ACT_HYGIENE = {"targetType": "player", "trait": "hygiene", "op": "add", "value": -10, "clamp": True}


def pay(meter, cap):
    return {"targetType": "player", "trait": meter, "op": "add", "value": 1, "cap": cap}


def step_done(n):
    return [setv("dex_step", n), setv("dex_sessions", 0)]


# His line by what she trains in (npc_dex.md, "his line" rows). One chain, most showing first.
DEX_BY_CLOTHES = [
    GC(cond(SHEER), P("He looks at you in the sheer leggings for a long time before he says anything."),
       D(DX, "You know I can see everything through those."), ME("Yes."), D(DX, "Good. Squats.")),
    GC(cond(SHORTS), D(DX, "Those are going to ride up on every squat. Don't fix them.")),
    GC(cond(*SPORTS_ALONE), P("His eyes go to your tits in the sports bra and stay there."),
       D(DX, "Now I can see your core. Good.")),
    GC(cond(LEGGINGS), P("In the mirror his eyes go to your ass in the leggings and stay."),
       D(DX, "Those'll show me if your form's right.")),
    GC(cond(TRACK), D(DX, "Track pants. I like a girl who works. But I'd like to see what's under them.")),
    GC(cond(*ANY), D(DX, "Get changed. Then come and find me.")),
]
from gymkit import not_gym
# one wording per canvas (gate `one pool, one place`)
NOT_DRESSED_1 = not_gym("He wants you in gym clothes before he touches you.", G, T)
NOT_DRESSED_2 = not_gym("Not for the mats. The locker room first.", G, T)


# ═════════════ step 1 · the free session (gym_floor, Mon-Sat 10:00-20:00) ═════════════
t1 = step_trigger(DX, 1)
out.append({
    "id": "dex_01_free_session", "name": "The trainer at the desk",
    "description": "Dex step 1 (npc_dex.md): he has watched her in the mirror and offers a free session; his hands on her hips at the squat rack in front of the mirror wall. Exhibitionism +1, cap 19. Meets Dex.",
    "trigger": t1,
    "nodes": [
        node("desk", "The trainer", [
            P("There's a man leaning on the end of the desk in a tight black staff tee with TRAINER across the back. Big, tanned, shaved head, tattoos down both forearms. He's been watching you in the mirror wall since you came in, and he doesn't pretend he hasn't."),
            P("He pushes off the desk and comes over."),
            D(DX, "Dex. I train people here. You've got the build, but I bet nobody's ever shown you how to squat."),
            D(DX, "First session's free. An hour. Let me show you."),
            *NOT_DRESSED_1,
            T("He was looking at your ass before you'd even checked in. Now he wants his hands on it."),
        ], [*kits(go("\"Okay. Show me.\"", node="rack", mins=0)),
            go("\"I'm fine on my own.\"", node="no", mins=0)]),
        node("rack", "The squat rack", [
            P("He stands right behind you at the rack, so close you feel the heat off him, and puts both hands on your hips."),
            D(DX, "Down. Slow. Push your ass back into me."),
            P("You go down. His hands stay on your hips the whole way, and at the bottom his crotch is an inch from your ass. In the mirror wall you can see all of it: his hands, your ass, his eyes on it. So can the guy on the bench, and the two at the cable machine."),
            P("On the way up he pulls your hips back into him, once, to show you. He's hard. He doesn't step away."),
            D(DX, "Better. Again."),
            GC(cond(trait("corruption", "lt", 20)), T("He's just doing his job. He's just very close while he does it.")),
            GC(cond(*ANY), T("Let him look. That's what he's paid for.")),
        ], [go("Do the set.", node="after", mins=60, costs=list(WORKOUT_COST), eff=WORKOUT + [pay("exhibitionism", 19)] + step_done(1),
               flags=[fset("dex_met"), fset("worked_out")], consumes=True)]),
        node("after", "First one's free", [
            P("Ten squats, his hands on your hips for every one. When you rack the bar your thighs are shaking and your face is hot, and it isn't the weight."),
            D(DX, "First one's free, @player. After that you pay."),
            D(DX, "Fifteen a session. I'm here every day but Sunday."),
        ], [go("Towel off.", loc="gym_floor", mins=5)]),
        node("no", "On your own", [
            D(DX, "Suit yourself. Your back, not mine."),
            P("He goes back to the desk. In the mirror wall he watches you do the next squat wrong."),
        ], [go("Do it your way.", loc="gym_floor", mins=2, retry=1)]),
    ]})


# ═════════════ step 2 · the mats (Curious, two sessions after step 1) ═════════════
out.append({
    "id": "dex_02_the_mats", "name": "The mats",
    "description": "Dex step 2 (npc_dex.md): a $15 session ends on the mats, her leg on his shoulder and his hand on her inner thigh, higher every rep, two regulars watching. Corruption +1, cap 39.",
    "trigger": step_trigger(DX, 2, retry_days=2),   # its gate waits for a day with no session or workout yet (ledger)
    "nodes": [
        node("start", "Your session", [
            P("Dex is waiting by the mats with a towel over his shoulder."),
            D(DX, "@player.nickname. Session's on the mats today. Your hamstrings are tight."),
            *NOT_DRESSED_2,
            G(cond(trait("money", "lt", 15)), T("Fifteen dollars, and you haven't got it.")),
        ], [*kits(go("Pay him and lie down.", node="mats", mins=0, cond_=cond(trait("money", "gte", 15), SESSION))),
            go("\"Just the weights today.\"", node="no", mins=0)]),
        node("mats", "His hand", [
            P("You lie on your back on the mat. He kneels between your legs and lifts one onto his shoulder and leans into it, and the stretch burns all the way up."),
            P("His hand is flat on your inner thigh to hold you there. Every rep it's higher. By the fourth his thumb is right over your pussy through the cloth, and he presses."),
            D(DX, "You're tight here. Breathe out."),
            P("Two regulars on the bench by the rack have stopped lifting to watch his hand. You can see them over his shoulder. You don't move it."),
            GC(cond(trait("corruption", "lt", 40)), T("It's a stretch. People stretch.")),
            GC(cond(*ANY), T("His hand's on your inner thigh and you want it higher.")),
        ], [go("Breathe out.", node="after", mins=60, costs=list(WORKOUT_COST),
               eff=WORKOUT + [add("money", -15), pay("corruption", 39)] + step_done(2),
               flags=[fset("worked_out"), fset("dex_session_today")], consumes=True)]),
        node("after", "Same time next week", [
            P("He lets your leg down slow and stands up. The front of his shorts doesn't hide anything."),
            D(DX, "Fifteen next time, @player.nickname. Or we work something out."),
        ], [go("Towel off.", loc="gym_floor", mins=5)]),
        node("no", "The weights", [
            D(DX, "Your call. Mats'll be here."),
        ], [go("Go to the weights.", loc="gym_floor", mins=2, retry=2)]),
    ]})


# ═════════════ step 3 · another way (Bold, three sessions after step 2) ═════════════
HAND_JOB = ("The locker room door has no lock. He leans back against the lockers and pushes his shorts down, and his "
            "cock comes out thick and heavy, already hard, the head dark and wet. He takes your hand and wraps it round "
            "him. You stroke him slow while he watches the door over your shoulder, then fast when he tells you to, his "
            "hips pushing into your fist. He comes in under two minutes, hot over your fingers and onto the tiles.")
out.append({
    "id": "dex_03_another_way", "name": "Keep your money",
    "description": "Dex step 3 (npc_dex.md): before her session he tells her to keep her $15; the locker room, between clients, her hand on his cock until he comes. Corruption +1, cap 59. Opens \"another way\" on every session.",
    "trigger": step_trigger(DX, 3, retry_days=2),   # its gate waits for a day with no session or workout yet (ledger)
    "nodes": [
        node("ask", "Short this week?", [
            P("You go to pay him for the session and he puts his hand over yours, over the money."),
            D(DX, "Short this week?"),
            P("He hasn't looked at your card. He doesn't care."),
            D(DX, "Keep your money. Locker room. I've got ten minutes before my next client."),
            GC(cond(trait("corruption", "lt", 60)), T("Just this once, for fifteen dollars.")),
            GC(cond(*ANY), T("You'd have done it for free.")),
        ], [go("\"Okay. Keep it.\"", node="hand", mins=0),
            go("\"I'll pay the fifteen.\"", node="no", mins=0)]),
        node("hand", "Another way", [
            P(HAND_JOB),
            D(DX, "Fuck. Good girl."),
            P("He hands you a towel for your fingers, pulls his shorts up and checks the door."),
        ], [go("Wipe your hand.", node="after", mins=15, eff=[pay("corruption", 59), ACT_HYGIENE] + step_done(3),
               flags=[fset("dex_paid_another_way"), fset("dex_session_today")], consumes=True)]),
        node("after", "Every time", [
            D(DX, "Keep your money, @player.nickname. Every time."),
            D(DX, "I finish in the sauna most nights. It's empty by eight."),
        ], [go("Go back out to the floor.", loc="gym_floor", mins=2)]),
        node("no", "The fifteen", [
            P("He takes the money and shrugs."),
            D(DX, "Offer stands."),
        ], [go("\"Not today, Dex.\"", loc="gym_floor", mins=2, retry=2, eff=[add("money", -15)], cond_=cond(trait("money", "gte", 15))),
            go("\"Not today, Dex.\"", loc="gym_floor", mins=2, retry=2, cond_=cond(trait("money", "lt", 15)))]),
    ]})


# ═════════════ step 4 · the sauna (Hungry, three sessions after step 3; Mon-Sat 20:00-20:45) ═════════════
SAUNA_FINGERS = ("The last regular picks up his towel and goes. The glass door swings shut behind him. Dex comes up to "
                 "the top bench and sits right against you, and opens your towel with one hand, all the way, like he's "
                 "unwrapping something he paid for. Your tits are bare and slick with sweat. He pushes two fingers "
                 "straight into your cunt. You're soaking. He fucks you with them hard and fast, his thumb on your clit, "
                 "his other hand on your tit, pinching your nipple, until you're grinding on his hand and biting your lip "
                 "to keep quiet. You come on his fingers with your thighs clamped round his wrist and your bare back "
                 "against the hot cedar.")
out.append({
    "id": "dex_04_the_sauna", "name": "The sauna, before close",
    "description": "Dex step 4 (npc_dex.md): just before close he ends his shift in the sauna; the last regular leaves, he opens her towel and fingers her until she comes. Corruption +1, cap 79.",
    "trigger": dict(step_trigger(DX, 4, retry_days=2), conditions=cond(*step_trigger(DX, 4)["conditions"]["items"], {"type": "worn_type", "operator": "eq", "value": "towel"})),
    "nodes": [
        node("heat", "Dex, in the heat", [
            P("The glass door opens and Dex comes in with a towel round his waist and nothing else. He sits on the bench below yours, between you and the last regular, and leans his head back against your knee."),
            D(DX, "Told you it empties out by eight."),
            P("The regular in the corner looks at the two of you, and at Dex's hand on your ankle, and starts gathering his things."),
            T("The last regular's nearly gone. Then it's just him."),
        ], [go("Open your knees.", node="fingers", mins=0),
            go("\"Not here. Someone could come in.\"", node="no", mins=0)]),
        node("fingers", "His fingers", [
            P(SAUNA_FINGERS),
            VID("a muscular trainer fingering a woman in a towel on a sauna bench, her head back against the cedar",
                "sauna fingering towel", "trainer fingers girl in sauna", pool_dir="sex/dex_sauna_t5"),
            D(DX, "Half eight, any night but Sunday. Stay when they lock up. I've got the key."),
        ], [go("Tuck the towel back up.", loc="gym_sauna", mins=20, eff=[pay("corruption", 79), ACT_HYGIENE,
               {"targetType": "player", "trait": "energy", "op": "add", "value": -10, "clamp": True}] + step_done(4),
               flags=[fset("sauna_today")], consumes=True)]),
        node("no", "Not here", [
            D(DX, "Then not here."),
            P("He takes his hand off your ankle and moves down to the far end of the bench, and shuts his eyes. The towel's low on his hips."),
        ], [go("Sit out the heat alone.", loc="gym_sauna", mins=20, retry=2, flags=[fset("sauna_today")])]),
    ]})


# ═════════════ step 5 · after hours (Hungry; the floor, 20:30-21:00, runs on past close) ═════════════
AFTER_FUCK = ("He locks the front doors at nine and kills the lights on the floor, and walks you back to the locker "
              "room in the dark. He bends you over the bench in front of your own locker, pulls your shorts and "
              "panties down to your knees in one go, and pushes his cock into your cunt from behind. Thick. All the "
              "way. You grab the edge of the bench. He fucks you hard, his hands on your hips the way they were at "
              "the squat rack, the bench banging the lockers on every stroke. You come with your face against the "
              "cold metal, and he pulls out and comes on your ass, hot, in long spurts.")
AFTER_EXITS = [go("Let him walk you out.", loc="street", mins=40, eff=[ACT_HYGIENE,
               {"targetType": "player", "trait": "energy", "op": "add", "value": -10, "clamp": True}])]
out.append({
    "id": "dex_05_after_hours", "name": "Stay after close",
    "description": "Dex step 5, his top step (npc_dex.md): she stays when the gym locks up; in the dark locker room he bends her over the bench and fucks her, cum on her ass. Corruption +1, cap 79. After hours becomes his repeat.",
    "trigger": step_trigger(DX, 5, retry_days=1),
    "nodes": [
        node("close", "Closing", [
            P("Closing time. The last few members are leaving, and the desk guy is counting the till. Dex comes over with his keys on his finger."),
            D(DX, "Desk's going home. I lock up. You staying?"),
            T("The whole gym dark, and him fucking you on the bench where you change."),
        ], [go("\"I'm staying.\"", node="dark", mins=30),
            go("\"Not tonight, Dex.\"", node="no", mins=0)]),
        node("dark", "After hours", [
            P(AFTER_FUCK),
            VID("a trainer fucking a woman from behind over a locker-room bench, the gym dark behind them",
                "fucked over locker room bench", "trainer fucks client after hours gym", pool_dir="sex/dex_after_hours_t5"),
            P("Somewhere down the hall the cleaner's cart rattles in through the back door."),
            D(DX, "Same time Thursday."),
        ], [dict(AFTER_EXITS[0], effects=AFTER_EXITS[0]["effects"] + [pay("corruption", 79)] + step_done(5),
                 flagEffects=[fset("dex_first_time"), fset("dex_after_today")], consumes=True)]),
        node("no", "Not tonight", [
            D(DX, "Your loss. Door's open till nine."),
        ], [go("Go home.", loc="street", mins=2, retry=1)]),
    ]})


# ═════════════ his hub on the gym floor: sessions, another way, after hours ═════════════
SESSION_LINES = POOL(
    P("He walks you round the floor, his hand on the small of your back between every machine, lower every time."),
    P("He spots you on the bench with his crotch over your face and his hands under the bar, and his eyes on your tits the whole set."),
    P("He corrects your deadlift from behind, both hands on your hips, and holds you at the bottom a second longer than the lift needs."),
    pid="dex_session_lines")
STRETCH_LINES = POOL(
    P("On the mats he puts your leg on his shoulder and leans in, and his hand rides your inner thigh up until his thumb is on your pussy through the cloth, pressing. You should stop him, but you open your leg wider."),
    P("He stretches you face down on the mat with his hand flat on your ass, holding you there, and you lie still and let him."),
    P("He sits behind you on the mat and pulls your knees apart for the hip stretch, and his fingers stay in the crease of your thighs the whole minute."),
    pid="dex_stretch_lines")
ANOTHER_LINES = POOL(
    P("Between his clients he takes you into the locker room and leans on the lockers with his shorts round his thighs, and you jerk his cock with your fist until he comes on the tiles. It takes him a minute, but you make it last longer than that."),
    P("In the locker room he sits on the bench and you kneel between his feet on the wet tiles. You get his cock out and stroke it with both hands while he watches the door, and he comes on your fingers with a grunt."),
    pid="dex_another_lines")
# his repeat (dex_after_hours, opened from his portrait by doors.py): one act a visit, from a bag
AFTER_LINES = POOL(   # between clients (10:00-20:30): the locker room, the door with no lock
    P("He walks you into the locker room and bends you over the bench by your locker, drags your bottoms and panties down and fucks your cunt from behind, hard and fast, the bench banging the lockers. You come before he does, but he isn't far behind, and he pulls out and comes on your ass."),
    P("He lies you on your back on the locker-room bench with your legs up over his shoulders, the stretch he gave you on the mats, and fucks you slow and deep with his cock until you come under him. He pulls out and comes on your stomach."),
    pid="dex_after_lines", bag=True)
CLOSE_LINES = POOL(   # after he locks up (20:30-21:00): the shared showers are empty (DECISIONS 227)
    P("He locks the doors and takes you into the empty showers, and fucks you against the tiles with the water running, your tits flat on the wet wall, his hand over your mouth. He comes inside you this time, and you let him."),
    P("He sends the last two people out of the showers, tells them the cleaners are coming, locks the door behind them, and fucks you in the middle of the shower room with the water off, your back on the cold tiles and your legs round his waist. Every slap of his hips echoes. He comes deep in your cunt and holds you there till it stops."),
    pid="dex_close_lines", bag=True)
CLIENTS = tod("10:00", "20:30")
CLOSING = tod("20:30", "21:00")
out.append({
    "id": "dex_after_hours", "name": "The locker room with Dex",
    "description": "Dex's repeat after his step 5 (npc_dex.md; DECISIONS 225): from his portrait on the gym floor, Mon-Sat 10:00-21:00, once a day. Between clients the locker room door has no lock; from 20:30 he locks up. Hungry, Corruption +1 to cap 79.",
    "trigger": {"location": "gym_floor", "requires_npc": DX, "is_repeatable": True, "priority": 5, "is_active": True,
                **doors.trigger("dex_after_hours")},
    "nodes": [
        node("start", "Dex", [
            G(cond(CLIENTS), P("Dex looks at the clock, then at you, and tips his head at the locker room."),
              D(DX, "Fifteen minutes till my next one. Come on.")),
            G(cond(CLOSING), P("The desk guy is counting the till. Dex has his keys on his finger."),
              D(DX, "I'm locking up. You staying?")),
        ], [go("Go with him.", node="act", mins=0, costs=[{"trait": "energy", "value": 10}],
               eff=[pay("corruption", 79), ACT_HYGIENE]),
            go("\"Not today, Dex.\"", loc="gym_floor", mins=0)]),
        node("act", "The locker room", [
            G(cond(CLIENTS), AFTER_LINES),
            G(cond(CLOSING), CLOSE_LINES),
            VID("a muscular trainer of 34 fucking a woman in a gym locker room or its shower room", "fucked in gym locker room",
                "trainer fucks client locker room", pool_dir="sex/dex_locker_t5"),
            G(cond(CLIENTS), D(DX, "Back out there. My client's waiting. Next time, same fifteen minutes.")),
            G(cond(CLOSING), D(DX, "Next time, stay again.")),
        ], [go("Back out to the floor.", loc="gym_floor", mins=15, cond_=cond(CLIENTS)),
            go("Let him walk you out.", loc="street", mins=30, cond_=cond(CLOSING))]),
    ]})

hub_nodes = [
    node("dex", "Dex", [
        P("Dex is at the desk end of the floor with his clipboard, watching the mirror wall."),
        *DEX_BY_CLOTHES,
        # the rival (npc_dex.md "Jake and Dex"): Tue/Thu, the team training
        G(cond(JAKE_HERE, trait("jake_step", "gte", 2)), D(DX, "Your boyfriend's watching. Lift.")),
        # his next step, said by him (the leak and promise rows)
        G(cond(trait("dex_step", "eq", 1)), D(DX, "Fifteen a session, @player. You'll be back.")),
        G(cond(trait("dex_step", "eq", 2)), D(DX, "Fifteen. Or we work something out.")),
        G(cond(trait("dex_step", "eq", 3)), D(DX, "Sauna's empty by eight.")),
        G(cond(trait("dex_step", "eq", 4)), D(DX, "Half eight. Stay when they lock up.")),
        G(cond(trait("dex_step", "gte", 5)), D(DX, "Half eight, if you're staying.")),
    ], [
        *kits(go("Book a session with Dex ($15).", node="session", mins=60, costs=list(WORKOUT_COST),
                 eff=WORKOUT + [add("money", -15), add("dex_sessions", 1, clamp=False), pay("exhibitionism", 19)],
                 flags=[fset("dex_session_today"), fset("worked_out")],
                 cond_=cond(CHECKED_IN, SESSION, flag("worked_out", False), trait("money", "gte", 15),
                            trait("dex_step", "gte", 1), trait("dex_step", "lt", 2)))),
        *kits(go("Book a session with Dex ($15).", node="stretch", mins=60, costs=list(WORKOUT_COST),
                 eff=WORKOUT + [add("money", -15), add("dex_sessions", 1, clamp=False), pay("corruption", 39)],
                 flags=[fset("dex_session_today"), fset("worked_out")],
                 cond_=cond(CHECKED_IN, SESSION, flag("worked_out", False), trait("money", "gte", 15),
                            trait("dex_step", "gte", 2)))),   # step 2 needed Curious already
        go("\"Keep your money.\"", node="another", mins=15, costs=[{"trait": "energy", "value": 10}],
           eff=[add("dex_sessions", 1, clamp=False), pay("corruption", 59), ACT_HYGIENE],
           flags=[fset("dex_session_today")],
           cond_=cond(CHECKED_IN, SESSION, trait("dex_step", "gte", 3), tod("10:00", "20:30"))),   # step 3 needed Bold already   # reader: between clients, before he locks up
        go("Leave him to his clients.", loc="gym_floor"),
    ]),
    node("session", "A session", [SESSION_LINES, D(DX, "Good. Same again next time.")],
         [go("Towel off.", loc="gym_floor", mins=5)]),
    node("stretch", "The mats", [STRETCH_LINES, D(DX, "Breathe out, @player.nickname.")],
         [go("Towel off.", loc="gym_floor", mins=5)]),
    node("another", "Another way", [ANOTHER_LINES, D(DX, "Keep your money. Every time.")],
         [go("Go back out to the floor.", loc="gym_floor", mins=2)]),
]
out.append({
    "id": "hub_dex_gym", "name": "Dex",
    "description": "Dex's hub on the gym floor (npc_dex.md): his line by her clothes; $15 sessions (Exhibitionism +1 cap 19 at his step 1, Corruption +1 cap 39 from step 2, Curious); from step 3, Bold, \"Keep your money.\" (+1 cap 59); from step 5, Hungry, after hours 20:30-21:00 (+1 cap 79). Once a day each.",
    "trigger": {"location": "gym_floor", "npc": DX, "requires_npc": DX, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("dex_met"))},
    "nodes": hub_nodes})

out.append({
    "id": "hub_dex_sauna", "name": "Dex, in the sauna",
    "description": "Dex in the sauna at the end of his shift (his step-4 row, 20:00-20:45): his line. His step 4 shows here instead while it is ready.",
    "trigger": {"location": "gym_sauna", "npc": DX, "requires_npc": DX, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("dex_met"))},
    "nodes": [node("heat", "Dex, in the heat", [
        P("Dex is on the bottom bench with a towel round his waist and his eyes shut. He opens one, and it goes to your tits under the wet towel."),
        D(DX, "Sit down, @player.nickname. It's empty soon."),
        T("He's looking at your thighs where the towel stops, and higher."),
    ], [go("Sit with him a while.", loc="gym_sauna", mins=10), go("Leave him to the heat.", loc="gym_locker")])]})

cards = step_cards(DX, {
    1: ("The trainer at the gym desk has been watching you in the mirror.", "The gym on your street, any day but Sunday, 10 to 8: check in at the desk, in gym clothes"),
    2: ("\"Fifteen a session. You'll be back.\"", "Book sessions with Dex at the gym, then the mats (Curious)"),
    3: ("\"Fifteen. Or we work something out.\"", "Book sessions with Dex at the gym; he'll stop taking your money (Bold)"),
    4: ("\"I finish in the sauna most nights. It's empty by eight.\"", "The gym sauna in a towel, 8 to quarter to 9, Monday to Saturday (Hungry)"),
    5: ("\"Nine o'clock tomorrow. Stay when they lock up.\"", "The gym floor at half past eight, Monday to Saturday, when Dex locks up"),
}, met_flag="dex_met", pointer=(1, "The trainer at the gym"),
   terminal_text=("After hours with Dex: the gym floor at half past eight, Monday to Saturday.", "Dex, further. (Next release)"))

text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · DEX (sheets/people/npc_dex.md, DECISIONS 225)\n"
        "# Steps 1-5, his hub on the gym floor (sessions, another way, after hours), his cards.\n"
        "# =============================================================================\n")
doors.apply(out)   # DECISIONS 224: seal his repeat and open its door in his hub
text += "".join(emit(c) for c in out) + "".join(emit_card(c) for c in cards)
open(__import__("sys").argv[1], "w").write(text)
print("dex:", len(out), "canvases,", len(cards), "cards")
