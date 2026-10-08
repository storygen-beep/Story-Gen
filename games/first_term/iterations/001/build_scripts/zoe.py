"""Zoe — her meeting, steps 1-4 (Zoe A 1-4; step 1 = Jake B 1), her hubs, the meeting nudge.
Source: sheets/scenes/zoe_0*.md, people/npc_zoe.md. Explicit screens pasted as signed."""
from canv import *
from tomlw import tod, wd

Z = "npc_zoe"
J = "npc_jake"
out = []

def done(n):
    return fset(f"zoe_0{n}_done")

PARTY_DRESS = {"type": "clothing_item", "item_id": "zoe_party_dress", "operator": "equipped"}
CURIOUS = trait("corruption", "gte", 20)

# ── her meeting on the quad ──
out.append({
    "id": "zoe_00_quad_meeting", "name": "The girl from Biology",
    "description": "Meets Zoe on the quad, the first time she's there in Zoe's hours. Sets zoe_met (opens her apartment) and zoe_number. Both answers meet her.",
    "trigger": {"location": "quad", "requires_npc": Z, "is_repeatable": False, "priority": 10, "is_active": True,
                "schedules": [{"weekdays": [1, 3, 4], "start_time": "14:30", "end_time": "18:00"}],
                "conditions": cond(flag("opening_done"), flag("zoe_met", False))},
    "nodes": [
        node("wave", "On the grass", [
            IMG("scenes/zoe_00_quad.jpg", "a laughing college girl lying on the grass of a campus quad waving someone over, sunglasses, afternoon",
                "college girl lying on grass quad waving", "girl on campus lawn sunglasses laughing"),
            P("The girl from your Biology class, the one who whispers through the slides, is lying on the grass on her elbows with her sunglasses pushed up in her hair. She sees you and waves both arms over her head like you're a plane she's landing."),
            WHO("Hey. You. Biology. Sit."),
        ], [
            go("Sit with her.", node="zoe", mins=5),
            go("\"Can't, I've got a shift.\"", node="later", mins=2),
        ]),
        node("zoe", "Zoe", [
            P("You sit. She rolls over and puts her head straight in your lap like you've known each other for years, and looks up at you upside down."),
            D(Z, "Zoe. You're the one who sits at the back and pretends not to know the answers. I like you. Do you party?"),
            P("She talks fast, about everything, Biology and the TA who blushes and a guy on the team with an ass you could bounce coins off. She looks at you a beat too long while she says it, and laughs."),
            G(cond(flag("college_for_fun")), D(Z, "You look like fun. You look like you've been waiting for someone to ask.")),
        ], [go("\"Party?\"", node="friday", mins=10, flags=[fset("zoe_met")])]),
        node("friday", "Friday", [
            D(Z, "Friday. My place. Wear something short."),
            P("She takes your phone out of your hand without asking and types her number into it, and her address, and a row of devil emojis."),
            D(Z, "Or don't, and I'll lend you something shorter."),
            T("You've known her ten minutes. You're going."),
        ], [go("\"Friday.\"", loc="quad", mins=5, flags=[fset("zoe_number")])]),
        node("later", "Run, then", [
            D(Z, "Fine, run! Friday, my place!"),
            P("She shouts the address after you across the whole quad. Three people turn round. She doesn't care. You've got her name by the time you reach the gate, because she shouted that too: Zoe."),
        ], [go("Go.", loc="campus", mins=2, flags=[fset("zoe_met"), fset("zoe_number")])]),
    ]})

# ── step 1 · Zoe A 1 = Jake B 1 · the first party (one canvas, both counters) ──
DARE_NO = ["Not tonight, Zo."]
out.append({
    "id": "zoe_01_first_party", "name": "Your first party",
    "description": "Zoe step 1 = Jake step 1 (one canvas, it sets both). Zoe's dress, her first dare, and a guy who picks her out: Jake. Sets party_went, jake_met, jake_number.",
    "trigger": step_trigger(Z, 1),
    "nodes": [
        node("dress", "Zoe's bedroom", [
            P("Zoe drags you straight past the music into her bedroom and shuts the door. She pulls a black dress off the back of it, short, tight, straps like string."),
            D(Z, "Put it on. No, here. I want to see."),
            P("You change in front of her. She sits on the bed with her chin in her hands and doesn't look away once, not while you strip, not when you wriggle the dress down over your hips."),
            D(Z, "Turn around. Let me see."),
        ], [go("\"Zoe! Eyes up here.\"", node="party", mins=10,
               wardrobe=[{"action": "add", "item_id": "zoe_party_dress"}, {"action": "equip", "item_id": "zoe_party_dress"}])]),
        node("party", "The party", [
            IMG("scenes/zoe_01_party.jpg", "a crowded apartment party, fairy lights, red cups, a girl in a short black dress being pulled through the crowd by her friend",
                "apartment party fairy lights crowd college", "girl in short black dress house party"),
            P("The flat is packed: half of campus, the bass coming up through the floor, red cups on every surface. Zoe walks you through it with her arm round your waist like she's showing you off, and people look. At the dress. At you in it."),
            G(cond(flag("college_for_grades")), D(Z, "Grades, you told your mom? Babe. Tonight you're majoring in this.")),
            G(cond(flag("college_for_fun")), D(Z, "You said fun. This is fun. Drink.")),
            G(cond(flag("college_for_freedom")), D(Z, "Freedom, babe. No mom, no stepdad, no rules. Breathe it in.")),
            P("She puts her head on your shoulder on the couch and says it into your ear, like a secret:"),
            D(Z, "Kiss someone. Or don't, and I'll keep asking."),
        ], [
            go("\"Not tonight, Zo.\"", node="no_dare", mins=5, flags=[fset("party_went")], eff=[add("exhibitionism", 3)]),
            go("Kiss Zoe.", node="kiss_zoe", mins=5, cond_=cond(CURIOUS), flags=[fset("party_went")], eff=[add("exhibitionism", 3)]),
            go("Kiss the guy who's staring.", node="jake", mins=5, cond_=cond(CURIOUS), flags=[fset("party_went"), fset("jake_kissed")], eff=[add("exhibitionism", 3)]),
        ]),
        node("no_dare", "Not tonight", [D(Z, "Boring. Fine. I'll keep asking."), P("She steals your drink instead and dances off into the crowd. Across the room a guy in a team jacket is watching you. Not Zoe. You.")],
             [go("Look back at him.", node="jake", mins=15)]),
        node("kiss_zoe", "Zoe", [
            P("You turn your head and kiss her, right there on the couch. She makes a surprised little sound against your mouth, and then she kisses you back, harder, her hand in your hair. Somebody whoops. When she pulls back her eyes are huge."),
            D(Z, "Oh. Okay. Okay."),
            P("Across the room a guy in a team jacket is watching you. Not Zoe. You."),
        ], [go("Look back at him.", node="jake", mins=5)]),
        node("jake", "Across the room", [
            P("He's been watching you since you came in: tall, a team jacket, a beer he isn't drinking, standing with three guys who are all talking to each other while he looks at you. When he sees you see him, he doesn't look away. He comes over."),
            G(cond(flag("jake_kissed")), P("You meet him halfway and kiss him before he can say anything. He tastes of beer. His hand goes to the small of your back like it belongs there.")),
            ME("You've been staring since I came in."),
            D(J, "Wasn't planning to stop. I'm Jake."),
            G(cond(PARTY_DRESS), P("His eyes go down your legs in Zoe's dress and stay there.")),
            P("Zoe sits on the arm of the couch watching the two of you with her drink and an unreadable face."),
        ], [
            go("\"Here's my number.\"", loc="zoe_apartment", mins=30, consumes=True,
               eff=[setv("zoe_step", 1), setv("jake_step", 1)], flags=[done(1), fset("jake_met"), fset("jake_number")]),
            go("\"Not tonight.\"", node="jake_no", mins=2),
        ]),
        node("jake_no", "Not tonight", [D(J, "Wasn't planning to give up."), P("He grins and goes back to his team, but he looks over every time you laugh.")],
             [go("Back to the party.", loc="zoe_apartment", mins=20, consumes=True,
                 eff=[setv("zoe_step", 1), setv("jake_step", 1)], flags=[done(1), fset("jake_met")])]),
    ]})

# ── step 2 · Zoe A 2 · bra through the sleeve ──
out.append({
    "id": "zoe_02_bra_through_the_sleeve", "name": "Through the sleeve",
    "description": "Zoe step 2 (Zoe A 2): a dress dare on the balcony, the room behind the glass. Her bra comes off. Sets party_house_invite (opens the party house).",
    "trigger": step_trigger(Z, 2, retry_days=7),
    "nodes": [
        node("balcony", "The balcony", [
            P("Zoe pulls you out onto the balcony, away from the noise. The glass door is behind you and the whole party is on the other side of it. She leans on the rail and looks at the strap on your shoulder and doesn't look anywhere else."),
            D(Z, "Bra off. Through the sleeve. Don't take anything else off. That's the dare."),
        ], [
            go("\"Watch me.\"", node="sleeve", mins=5, cond_=cond({"type": "clothing_slot", "slot": "bra", "operator": "equipped"})),
            go("\"I'm not wearing one, Zo.\"", node="already", mins=2, cond_=cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"})),
            go("\"Not tonight, Zo.\"", node="no", mins=2),
        ]),
        node("sleeve", "Through the sleeve", [
            G(cond(PARTY_DRESS), P("You reach up under Zoe's dress and unhook it at the back, and work one strap down your arm and through the armhole of the dress, then the other.")),
            G(cond({"type": "clothing_item", "item_id": "zoe_party_dress", "operator": "unequipped"}), P("You reach up the back and unhook it, and work one strap down your arm and out through your sleeve, then the other.")),
            P("It takes forever. Zoe watches every second. When it slides out of your sleeve your nipples are hard in the cold air, two points anyone could see, and inside, through the glass, a guy at the window puts two fingers in his mouth and whistles."),
        ], [go("\"Give it back.\"", node="mine", mins=3, eff=[add("exhibitionism", 3)],
               wardrobe=[{"action": "unequip", "item_id": "plain_bra"}, {"action": "unequip", "item_id": "sports_bra"}])]),
        node("already", "Already", [D(Z, "You're— oh my god. All night? Babe."), P("She looks at your chest for a long second, then laughs and leans on the rail next to you, close, her shoulder on your bare arm.")],
             [go("Laugh with her.", node="mine2", mins=3, eff=[add("exhibitionism", 3)])]),
        node("mine2", "Saturday", [D(Z, "There's a hot tub Saturday. At the party house. Just us. Well. Just us and some people."), T("She keeps looking at your chest. She keeps not asking.")],
             [go("\"Saturday.\"", loc="zoe_apartment", mins=5, consumes=True, eff=[setv("zoe_step", 2)], flags=[done(2), fset("party_house_invite")])]),
        no_node("no", [D(Z, "Boo. Fine. I'll think of a worse one."), P("She goes back inside and leaves the balcony door open behind her.")], "zoe_apartment", 7),
        node("mine", "Mine now", [
            P("Zoe takes it out of your hand and tucks it in her back pocket."),
            D(Z, "Nope. Mine now."),
            P("Then she leans on the rail next to you, close, her shoulder against your bare arm, and says it quieter."),
            D(Z, "There's a hot tub Saturday. At the party house. Just us. Well. Just us and some people."),
            T("She keeps looking at your chest. She keeps not asking."),
        ], [go("\"Saturday.\"", loc="zoe_apartment", mins=5, consumes=True,
               eff=[setv("zoe_step", 2)], flags=[done(2), fset("party_house_invite")])]),
    ]})

# ── step 3 · Zoe A 3 · the hot tub (the voice sample; every screen as signed) ──
HOME_AT_3 = [(("20:00", "21:00"), 400), (("21:00", "22:00"), 340), (("22:00", "23:00"), 280), (("23:00", "00:00"), 220)]
out.append({
    "id": "zoe_03_hot_tub", "name": "The hot tub",
    "description": "Zoe step 3 (Zoe A 3), the voice sample: the party house hot tub, her friends go in first; topless for Zoe alone and she kisses her. Home at three; Ryan at his door.",
    "trigger": step_trigger(Z, 3, bind_npc=False, retry_days=7),
    "nodes": [
        node("tub", "The hot tub", [
            P("Zoe drags you into the hot tub on the back deck, laughing. Steam rolls off the water. Music thumps through the glass. Three of her friends are already in, drinks on the rim. \"Make room, babe's here.\" She doesn't need room. She sits right against you, her knee pressed to yours under the water. When you talk, she watches your mouth. All term she has dared you instead of asking, but you know what she wants. \"Your tits are floating, babe,\" she says, grinning. Your face goes hot, and it isn't the water. One of her friends stands up, restless. \"Going in for more drinks.\""),
        ], [go("Stay in the water.", node="alone", mins=15)]),
        node("alone", "Just us", [
            P("The door slides shut behind her friends. Now it is just the two of you in the steam. Zoe goes quiet, and Zoe is never quiet. \"Take it off, babe,\" she says, low. \"Just for me. Nobody else is here.\" Her eyes drop to your chest and stay there. She bites her lip. Her breath comes short across the water. \"Everything on you is wet anyway. I can see your nipples, babe. I want to see your tits.\" Your heart pounds, because you want her to keep looking. Your hands drift up and stop. She waits for your answer."),
        ], [
            go("Take it off.", node="kiss", mins=3),
            go("\"Not tonight, Zo.\"", node="home_no", mins=60),
        ]),
        node("kiss", "Topless", [
            P("You pull it off and toss it on the deck. The steam rolls over your bare tits. The night air is cold on them, so your nipples go hard above the water. Zoe stares at them. \"Babe,\" she breathes. \"Look at you.\" You grab the back of her neck and pull her in. You kiss her hard, open-mouthed, until she moans into you. Her tits press flat against yours. Her nipples drag across your nipples, hard and wet. Her thigh slides between your thighs under the water. It presses up, slow and firm. Her breath catches. Your hands run down her slick back to her ass. You grab it with both hands and pull her tits tight against yours."),
            VID("two topless girls kissing in a steaming hot tub at night, breasts pressed together", "two girls topless kissing hot tub night", "lesbian kiss hot tub steam topless", file="sex/zoe_03_kiss_t5.webm"),
        ], [go("Hold her.", node="asked", mins=10, eff=[add("exhibitionism", 3), add("corruption", 3)])]),
        node("asked", "You could've asked", [
            P("Zoe pulls back, flushed and breathless, and laughs. \"Took you long enough, babe.\" \"You could've asked,\" you tell her. She goes quiet. She opens her mouth, but she doesn't answer that. Not yet. All term she dared you instead of asking for this. You liked every single dare. The sliding door bangs open. Your friends spill back out, shrieking. You sink to your shoulders in the hot water. Across the bubbles, Zoe is still looking at you. Next time you two are alone, somebody has to ask first."),
        ], [go("Go home.", node="home", mins=m, cond_=cond(tod(a, b)), consumes=True,
               eff=[setv("zoe_step", 3)], flags=[done(3)]) for (a, b), m in HOME_AT_3]),
        node("home_no", "Home", [D(Z, "Next Saturday, then. I'll ask again."), P("She doesn't sound annoyed. She sounds like she's counting. You go home with dry hair and the steam still in your clothes, and Ryan's door is shut.")],
             [go("Go to bed.", loc="home_ella_room", mins=5, retry=7)]),
        node("home", "Home at three", [
            P("You let yourself in. The house is dark, and your hair drips on the mat. You smell of chlorine, and Zoe's lipstick is still on your neck. Upstairs, Ryan's door is open a crack. He is awake. He sees you on the landing. His eyes stop on your wet hair, then drop to your neck and stay there. \"@player.nickname. Where've you been?\" \"Zoe's.\" You say nothing else, because you want him to wonder. Your face goes hot under his stare, but you hold it. Ryan's jaw tightens. He looks a beat too long, then his door closes slowly."),
        ], [go("Go to bed.", loc="home_ella_room", mins=5, retry=7, eff=[nadd("npc_ryan", "want", 5)])]),
    ]})

# ── step 4 · Zoe A 4 · I pick the dares ──
out.append({
    "id": "zoe_04_i_pick_the_dares", "name": "I pick the dares",
    "description": "Zoe step 4 (Zoe A 4), her couch any evening after the hot tub: she admits she dared instead of asking. Sets picks_the_dares (party nights are hers).",
    "trigger": step_trigger(Z, 4),
    "nodes": [
        node("couch", "Her couch", [
            P("Zoe's on her couch in a big T-shirt with her bare legs tucked under her, eating cereal out of the box. She doesn't offer you any. She doesn't look at you either, which for Zoe is the same as shouting."),
            D(Z, "You didn't need me in the hot tub. You were the dare."),
        ], [go("Sit down next to her.", node="asked", mins=5)]),
        node("asked", "So I wouldn't have to ask", [
            D(Z, "I dared you so I wouldn't have to ask. That's the whole thing. That's all the dares were. Pathetic, right?"),
            P("She says it to the cereal box. Her ears are red."),
            T("All term. Every dare. She wanted you and she made it a game so she'd never have to say it."),
        ], [
            go("\"From now on, I pick the dares.\"", node="first", mins=5),
            go("\"Okay.\"", loc="zoe_apartment", mins=5, retry=3),
        ]),
        node("first", "The first one", [
            ME("From now on, I pick the dares. First one: tell me what you want."),
            D(Z, "Not that one, babe."),
            P("She laughs, and puts the box down, and pulls her knees up, and looks at you properly for the first time tonight."),
            D(Z, "Give me another one. Any other one. I'll do it."),
            ME("Next one, then. Friday."),
        ], [go("\"Next one, then.\"", loc="zoe_apartment", mins=10, consumes=True,
               eff=[setv("zoe_step", 4)], flags=[done(4), fset("picks_the_dares")])]),
    ]})

# ── her hubs ──
ZOE_STATE = [
    G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), D(Z, "Now we're talking. Turn around.")),
    G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "worn_exposure", "operator": "eq", "value": 0}), D(Z, "Oh, you're ready for Friday.")),
    G(cond(PARTY_DRESS), P("She bites her lip at the strap of her own dress on you."), D(Z, "Nope. Eyes stay.")),
]
ZOE_LEAKS = [
    G(cond(trait("zoe_step", "eq", 1), {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}), P("Her eyes keep going to your bra strap.")),
    G(cond(trait("zoe_step", "eq", 2)), D(Z, "There's a hot tub Saturday. Just us. Don't forget.")),
    G(cond(trait("zoe_step", "eq", 3)), D(Z, "You didn't need me last time, babe.")),
]

out.append({
    "id": "hub_zoe_quad", "name": "Zoe, on the grass",
    "description": "Zoe's hub on the quad: her want shown first, her head in her lap.",
    "trigger": {"location": "quad", "npc": Z, "requires_npc": Z, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("zoe_met"))},
    "nodes": [node("grass", "The grass", [
        P("Zoe's on the grass with her shoes off. She doesn't say hello. She just puts her head in your lap and looks up at you, and when people look over, she says, \"Let them.\""),
        POOL(D(Z, "Tell me something bad you did."), D(Z, "That guy's been staring at your legs for ten minutes. Want me to make it twenty?"), D(Z, "Friday. You're coming. I'm not asking."), pid="zoe_quad_lines"),
        *ZOE_STATE, *ZOE_LEAKS,
    ], [go("Lie back with her a while.", loc="quad", mins=30), go("Leave her to the sun.", loc="quad")])]})

out.append({
    "id": "hub_zoe_canteen", "name": "Zoe, at lunch",
    "description": "Zoe at lunch in the canteen.",
    "trigger": {"location": "canteen", "npc": Z, "requires_npc": Z, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("zoe_met"))},
    "nodes": [node("lunch", "Lunch", [
        P("Zoe steals a fry off your tray before you've sat down and eats it looking straight at you."),
        *ZOE_LEAKS,
        G(cond(wd(3, 4)), D(Z, "Friday. Mine. Don't make me come and get you.")),
        POOL(D(Z, "Babe. You will not believe what the TA said to me."), D(Z, "Sit. You're with me."), D(Z, "Who's the guy? Don't say no guy. There's a guy."), pid="zoe_lunch_lines"),
        *ZOE_STATE,
    ], [go("Stay for lunch with her.", loc="canteen", mins=30), go("Go.", loc="canteen")])]})

out.append({
    "id": "hub_zoe_apartment", "name": "Zoe, at home",
    "description": "Zoe at home in the evenings: her couch, her flat.",
    "trigger": {"location": "zoe_apartment", "npc": Z, "requires_npc": Z, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("zoe_met"))},
    "nodes": [node("couch", "Her couch", [
        G(cond(wd(4), tod("19:00", "02:00")), P("The flat is loud and full. Zoe finds you in the crowd and hooks her finger in yours and pulls you in."),
          D(Z, "You came. Good girl. Drink.")),
        G(cond({"type": "weekday", "weekdays": [0, 1, 2, 3, 5]}), P("Zoe's on the couch in a big T-shirt with the TV on and her feet up. She shoves her feet off the cushion for you."),
          POOL(D(Z, "Stay. Watch trash with me."), D(Z, "Paint my nails. You've got steadier hands."), D(Z, "I'm bored. Dare me something."), pid="zoe_home_lines")),
        G(cond(flag("picks_the_dares")), D(Z, "Go on, then. What's tonight's dare?")),
        *ZOE_STATE, *ZOE_LEAKS,
    ], [go("Stay a while.", loc="zoe_apartment", mins=45), go("Go.", loc="zoe_apartment")])]})

out.append({
    "id": "hub_zoe_park", "name": "Zoe, running",
    "description": "Zoe on her weekend run in the park. Her dare from Curious: a flash on the path (Exhibitionism +1, once a day).",
    "trigger": {"location": "park", "npc": Z, "requires_npc": Z, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("zoe_met"))},
    "nodes": [
        node("path", "The path", [
            P("Zoe jogs up the path in tiny shorts and a sports top, earbuds in, cheeks pink. She runs on the spot in front of you and pulls one earbud out."),
            D(Z, "Run with me. Or don't, and stand there looking cute."),
            G(cond({"type": "clothing_item", "item_id": "sports_bra", "operator": "equipped"}, {"type": "clothing_slot", "slot": "top", "operator": "unequipped"}),
              D(Z, "Just the sports bra? Babe. Half the park's going to fall in the pond.")),
        ], [
            go("Run a lap with her.", loc="park", mins=30, costs=[{"trait": "energy", "value": 10}]),
            go("Go.", loc="park"),
        ]),
    ]})

out.append({
    "id": "zoe_park_dare", "name": "\"Dare me, Zo.\"",
    "description": "Zoe's dare on her run (the park sheet, Curious): a flash on the path. Exhibitionism +1, once a day.",
    "trigger": {"location": "park", "requires_npc": Z, "is_repeatable": True, "priority": 4, "is_active": True, "max_triggers_per_day": 1,
                "conditions": cond(flag("zoe_met"), CURIOUS, {"type": "clothing_slot", "slot": "top", "operator": "equipped"})},
    "nodes": [
        node("ask", "Her dare", [D(Z, "Flash me. Right here. Two seconds. There's a guy on the bench, so make it count.")],
             [go("Do it.", node="dare", mins=1), go("\"Not here, Zo.\"", node="no", mins=1)]),
        node("dare", "Her dare", [
            P("You check the path both ways, pull everything up for one long second, and drop it. Zoe shrieks. The guy on the bench drops his coffee."),
            D(Z, "Oh my god. I love you. Run! Next weekend I've got a worse one."),
        ], [go("Run.", loc="park", mins=10, eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 59}])]),
        node("no", "Not here", [D(Z, "Chicken."), P("She laughs and sprints off up the path, and you have to run to catch her.")], [go("Run after her.", loc="park", mins=10, flags=[fset("park_cool_zoe")])]),
    ]})

cards = step_cards(Z, {
    1: ("Zoe's party, Friday, at her place. She has a dress for you.", "Friday evening: Zoe's party at her apartment"),
    2: ("Her eyes keep going to your bra strap. She has a dare.", "A Friday party at Zoe's, out on the balcony (Curious, Daring)"),
    3: ("\"There's a hot tub Saturday. Just us.\"", "Saturday night: the hot tub at the party house (Bold, Showing)"),
    4: ("\"You didn't need me in the hot tub.\" She still won't ask.", "An evening at Zoe's apartment, on her couch (Bold)"),
}, met_flag="zoe_met", terminal_text=("Party nights are your call now. You pick Zoe's dares.", "Zoe's next step comes in the next release."))

story = [{"group": "story_goals", "priority": 15, "text": "Someone from your Biology class hangs out on the quad in the afternoons.",
          "tip": "The quad, on Tuesday, Thursday or Friday afternoon.",
          "when": [{"flag": "opening_done", "op": "is_true"}, {"days_since_flag": "opening_done", "op": "gte", "value": 1},
                   {"flag": "zoe_met", "op": "is_false"}],
          "goals": [{"flag": "zoe_met", "op": "is_true", "label": "Find the girl from Biology on the quad, Tuesday, Thursday or Friday afternoon"}]}]

text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · ZOE (sheets/scenes/zoe_0*.md, people/npc_zoe.md)\n"
        "# Her meeting, steps 1-4 (step 1 is also Jake's step 1), her hubs, her cards, the meeting nudge.\n"
        "# =============================================================================\n")
text += "".join(emit(c) for c in out) + "".join(emit_card(c) for c in cards + story)
open(__import__("sys").argv[1], "w").write(text)
print("zoe:", len(out), "canvases,", len(cards) + len(story), "cards")
