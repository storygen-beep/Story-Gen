"""Ryan — steps 2-8 (Ryan A 3-9), his hubs, his things, the two-knocks repeat.
Source: sheets/scenes/ryan_0*.md, sheets/people/npc_ryan.md. Explicit screens pasted as signed."""
from canv import *
from tomlw import tod, wd

R = "npc_ryan"
out = []

def done(n):
    return fset(f"ryan_0{n}_done")

# ── step 2 · Ryan A 3 · his phone on the sink ──
out.append({
    "id": "ryan_02_phone_on_the_sink", "name": "His phone on the sink",
    "description": "Ryan step 2 (Ryan A 3). She learns about Kayla. Sets knows_about_kayla (causes his thread).",
    "trigger": step_trigger(R, 2),
    "nodes": [
        node("sink", "The sink", [
            IMG("scenes/ryan_02_sink.jpg", "steamy bathroom, a guy behind a fogged shower door, a phone buzzing on the sink, a girl brushing her teeth",
                "steamy bathroom shower door phone on sink", "girl brushing teeth bathroom guy in shower"),
            P("The shower's running and the door doesn't lock, so you go in anyway, because you have class and he's had the bathroom long enough. Ryan is a shape behind the fogged glass. You brush your teeth at the sink with your back to him."),
            D(R, "Seriously, @player.nickname? Two minutes."),
            P("His eyes find you in the mirror through the steam, and go away again too fast. Then his phone buzzes on the edge of the sink, right by your hand. The screen lights up: a name, Kayla, and a heart, and a message that starts *can't wait for friday, sneak me in the back again*."),
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "worn_type", "operator": "eq", "value": "thin_top"}),
              P("In the steam your sheer blouse sticks to you. There's no bra under it, and the mirror shows him that too.")),
        ], [
            go("Read it.", node="read", mins=3, flags=[fset("knows_about_kayla")]),
            go("Leave it.", loc="home_hall", mins=3, retry=1),
        ]),
        node("read", "Kayla", [
            P("You pick it up. You read the whole thing, out loud in your head, and the next one comes in while you're holding it: a photo, Kayla in his bed in one of his shirts."),
            P("The shower slams off. Ryan's arm comes out of the steam and grabs the phone out of your hand, too late, dripping on the floor."),
            D(R, "Give me that."),
        ], [
            go("\"Sneaking her in past Mom, huh?\"", node="secret", mins=2),
        ]),
        node("secret", "Don't", [
            P("He stands there in the steam with a towel round his waist and his phone against his chest, and for the first time since you moved in, he looks scared of you."),
            D(R, "Don't. Mom would lose it. She thinks Kayla's some girl from the yard. Don't."),
            P("You smile at him in the mirror and finish brushing your teeth, slowly, because you can."),
            T("Ryan has a secret, and now it's yours."),
        ], [
            go("\"Your secret's safe. For now.\"", loc="home_hall", mins=5, consumes=True,
               eff=[nadd(R, "want", 10), setv("ryan_step", 2)], flags=[done(2)]),
        ]),
    ]})

# ── step 3 · Ryan A 4 · shirt off ──
out.append({
    "id": "ryan_03_shirt_off", "name": "Shirt off",
    "description": "Ryan step 3 (Ryan A 4). Her price for his secret. Sets ryan_knock_code (the door's Two knocks).",
    "trigger": step_trigger(R, 3),
    "nodes": [
        node("door", "His door", [
            P("You knock. He opens it a crack, sees it's you, and opens it the rest of the way, wary, one hand still on the frame."),
            D(R, "If this is about Kayla—"),
            P("He looks at you a beat longer than he needs to. He's done that every day since you read her text."),
        ], [
            go("\"It's about Kayla.\"", node="price", mins=2),
            go("\"Never mind.\"", loc="home_hall", mins=2, retry=1),
        ]),
        node("price", "Her price", [
            P("You walk past him into his room and sit on the end of his bed like it's yours. He shuts the door so nobody downstairs hears."),
            ME("You saw me. In the hall. In a towel."),
            D(R, "That was an accident."),
            ME("So's this. Shirt off."),
            P("He laughs, and stops laughing when you don't."),
            D(R, "You're serious."),
            ME("Your secret's worth that much. Turn around. Slowly."),
        ], [
            go("\"Turn around. Slowly.\"", node="look", mins=3),
        ]),
        node("look", "Look", [
            IMG("scenes/ryan_03_shirt.jpg", "a fit young man pulling his t-shirt off over his head in a bedroom, lamp light",
                "guy pulling shirt off over head bedroom", "shirtless young man bedroom lamp light"),
            P("He pulls the T-shirt over his head and drops it on the floor. Broad shoulders, the yard's work in his arms, a trail of dark hair under his navel that disappears into his jeans. He turns, slowly, like you said, and his back is all muscle, and when he faces you again his jaw is tight."),
            D(R, "Happy?"),
            P("Your mouth has gone dry. You make yourself look at all of him before you stand up, so he knows you did."),
            T("Your step-brother. You just made him strip for you, and you want to do it again."),
            ME("Two knocks. That's me. Open the door when you hear it."),
        ], [
            go("\"Two knocks. That's me.\"", loc="home_hall", mins=5, consumes=True,
               eff=[nadd(R, "want", 10), add("corruption", 1), setv("ryan_step", 3)],
               flags=[fset("ryan_knock_code"), done(3)]),
        ]),
    ]})

# ── step 4 · Ryan A 5 · feet in his lap ──
out.append({
    "id": "ryan_04_feet_in_his_lap", "name": "Feet in his lap",
    "description": "Ryan step 4 (Ryan A 5). A touch while he lies to Kayla. Laura's step 4 reads this counter.",
    "trigger": step_trigger(R, 4),
    "nodes": [
        node("knocks", "Two knocks", [
            P("Two knocks. He opens on the second one, like he was waiting by the door. A game on the TV, the sound low, and his bed pushed against the wall with room left on it."),
            D(R, "Mom's asleep. Mark's downstairs. Get in before someone sees."),
        ], [
            go("\"Feet up.\"", node="lap", mins=5),
            go("\"Just saying goodnight.\"", loc="home_hall", mins=2, retry=1),
        ]),
        node("lap", "His lap", [
            P("You sit at the far end of his bed and put your bare feet in his lap without asking. He looks at them, then at you, and leaves them there. His hand settles on your ankle like it's nothing."),
            P("His phone rings. Kayla. He answers it with his hand still on you."),
            D(R, "Yeah, babe. Nah, just watching the game. I'm alone."),
        ], [
            go("Press your toes into his thigh.", node="liar", mins=10),
        ]),
        node("liar", "Liar", [
            P("You press your toes into the top of his thigh, slow, and his thumb finds your ankle bone and rubs it while he tells Kayla he misses her. His voice doesn't change. His thumb does. Through his shorts you can feel him getting hard under your heel."),
            P("He hangs up, and sits there breathing, and doesn't move your feet."),
            T("He lied to her with his hand on you. He'd do it again."),
        ], [
            go("\"Liar.\"", loc="home_hall", mins=5, consumes=True,
               eff=[nadd(R, "want", 10), setv("ryan_step", 4)], flags=[done(4)]),
        ]),
    ]})

# ── step 5 · Ryan A 6 · thin walls (the voice sample; every screen as signed) ──
SLEEP_TO_DAWN = [(("22:00", "23:00"), 480), (("23:00", "00:00"), 420), (("00:00", "01:00"), 360)]
out.append({
    "id": "ryan_05_thin_walls", "name": "Thin walls",
    "description": "Ryan step 5 (Ryan A 6), in her bed on a Friday night, seen from his room. Her first explicit act at home; Kayla in the hall at dawn. Sets ryan_heard_her.",
    "trigger": step_trigger(R, 5, bind_npc=False, retry_days=7),
    "nodes": [
        node("wall", "Through the wall", [
            P("Thump. Thump. Thump. Ryan's headboard hits the wall a foot from your pillow. Kayla moans through the plaster, high and breathless. Then Ryan's voice, low: \"Quiet. They'll hear.\" She doesn't get quiet. The knocking gets faster. You knew Kayla sneaks in on Fridays. You read her text on his phone. Knowing it and hearing it are not the same thing. Your face is hot. You pull the sheet up to your chin, but you don't cover your ears. *Turn over. Go to sleep.* Kayla gasps his name. You lie still and listen to every second of it."),
        ], [
            go("Listen.", node="listen", mins=5),
            go("Put your headphones in.", loc="home_ella_room", mins=5, retry=7),
        ]),
        node("listen", "Listen", [
            P("The headboard thuds against the wall. Thud. Thud. Faster. You lie still and listen on purpose. Kayla moans, high and broken. \"Harder. Don't stop. Right there, Ryan, right there.\" Ryan groans her name, low and rough. That's your brother's voice. Your nipples go tight against the sheet. Your breath comes short. Heat pools between your thighs until you're wet. *That's Ryan. You should be grossed out.* You aren't, but that scares you less than how badly you want to hear more. The headboard speeds up. Kayla cries out. Your hand slides down your stomach and stops an inch above your clit, aching to keep going."),
            VID("in bed at night under a sheet, a girl listening to a couple through the wall, her hand on her stomach", "girl in bed at night listening through wall touching herself", "woman under sheet hand sliding down stomach dark bedroom", file="sex/ryan_05_listen_t4.webm"),
        ], [
            go("Touch yourself.", node="act", mins=10),
            go("Roll over. Sleep.", loc="home_ella_room", mins=5, retry=7),
        ]),
        node("act", "In time with him", [
            P("Your hand slides down under the sheet. Your fingers find your clit, and you're already wet. On the other side of the wall, Ryan's headboard knocks, slow and hard. You rub in time with it. Kayla moans his name. You picture his cock sinking into her, his hands full of her ass, her tits bouncing with every thrust. Your other hand finds a nipple and pinches. Your hips lift off the mattress. The headboard speeds up, so you speed up. Your thighs start to shake. Then Ryan groans through the wall, low and rough, and that does it. You come hard, biting the pillow, but a moan still gets out of you. The headboard stops dead, while your thighs clamp tight around your hand and your clit is still throbbing under your fingers."),
            VID("a girl in bed touching herself under the sheet, hips lifting, biting a pillow as she comes", "girl masturbating under sheet biting pillow orgasm", "woman fingering herself in bed at night hips arching", file="sex/ryan_05_act_t5.webm"),
        ], [
            go("Lie still.", node="after", mins=5, eff=[add("corruption", 1), nadd(R, "want", 10)]),
        ]),
        node("after", "Silence", [
            P("The headboard doesn't start again. Through the wall, Kayla mumbles, \"What? ... Nothing?\" \"Nothing,\" Ryan says. \"Go to sleep.\" The bed creaks. Then, low, right against the wall by your head: \"...@player.nickname?\" You don't answer. You lie still, your heart slamming, the pillow damp where you bit it. *He heard all of it. Every second. And you're not sorry.* Kayla is still here in the morning. There's one bathroom, and all three of you need it."),
        ], [go("Sleep.", node="hall", mins=m, cond_=cond(tod(a, b)), flags=[fset("ryan_heard_her"), done(5)],
               eff=[setv("ryan_step", 5)], consumes=True) for (a, b), m in SLEEP_TO_DAWN]
          + [go("Knock back twice.", node="knock_back", mins=2, swl=True, cond_=cond(trait("corruption", "gte", 40)))]),
        node("knock_back", "Two knocks back", [
            P("You make a fist and knock on the wall, twice, right where his voice was. Silence. Then, so quiet you almost miss it, one knock back. Kayla says \"What was that?\" and Ryan says \"Pipes,\" and you lie there grinning in the dark with your hand still between your legs."),
        ], [go("Sleep.", node="hall", mins=m, cond_=cond(tod(a, b)), flags=[fset("ryan_heard_her"), fset("ryan_knocked_back"), done(5)],
               eff=[setv("ryan_step", 5)], consumes=True) for (a, b), m in SLEEP_TO_DAWN]),
        node("hall", "Saturday, dawn", [
            P("Ryan's door clicks open and a girl slips out barefoot. Kayla. She's in one of his T-shirts, and it barely covers her ass. She's sneaking for the bathroom before Mom is up. She sees you and stops. She looks a beat too long, and she's smiling. \"You must be @player.nickname.\" *She heard you. Or he told her.* \"I am,\" you say. \"Thin walls.\" Kayla laughs, low, like she just won something. \"Shower's free. Go on. I'm not going anywhere.\" Behind her, Ryan stands frozen in his doorway, red to the ears, and he can't look at you."),
        ], [
            go("Wait your turn, then take the shower.", loc="home_bathroom", mins=120, eff=[setv("energy", 100)], flags=[fset("kayla_met")]),
        ]),
    ]})

# ── step 6 · Ryan A 7 · after the shower ──
out.append({
    "id": "ryan_06_after_the_shower", "name": "After the shower",
    "description": "Ryan step 6 (Ryan A 7), the bathroom on a Saturday morning, seen from his room. Naked by her choice; Kayla calls him away.",
    "trigger": step_trigger(R, 6, bind_npc=False, retry_days=7),
    "nodes": [
        node("door", "The shower", [
            P("You lock the door behind you, and the lock sticks halfway like it always does. You shower long and hot, because Kayla is somewhere in this house in Ryan's shirt and you want to take your time. You turn the water off. The towel is on the rail."),
            P("Then the handle turns, and the door swings open, and it's Ryan."),
        ], [
            go("Leave the towel.", node="look", mins=3, wardrobe=STRIP),
            go("Reach for the towel.", loc="home_hall", mins=5, retry=7, wardrobe=[{"action": "equip", "item_id": "towel"}]),
        ]),
        node("look", "Let him look", [
            P("You step out of the shower just as the door swings open. Ryan, in nothing but his shorts. Water runs down your tits and drips off your nipples, hard in the cold air. The towel hangs right there on the rail. You stay naked and leave it. His cock is already hard, straining the front of his shorts, and he can't stop looking. \"I heard you through the wall, @player.nickname. All of it.\" \"Good. Now you've seen it too.\" You reach past him, close enough to feel the heat off his chest, and turn the lock. You turn slowly so he gets your ass, pink from the hot water. A line of water slides down your spine and between your cheeks. Behind you his breathing goes rough. You look back over your shoulder. His hands are fists at his sides, but his cock jerks against the thin cotton."),
            VID("a wet naked girl stepping out of a shower, a guy in shorts in the bathroom doorway staring, his erection visible", "naked girl out of shower guy in doorway staring", "wet naked woman bathroom man watching hard in shorts", file="sex/ryan_06_look_t4.webm"),
        ], [
            go("Let him look.", node="kayla", mins=3, eff=[add("exhibitionism", 3), nadd(R, "want", 10)]),
        ]),
        node("kayla", "Ryan?", [
            D("npc_kayla", "Ryan? Babe? Are you up?"),
            P("Kayla, from the hall, right outside. Ryan shuts his eyes. He fumbles the lock open without turning his back on you, and goes, hard in his shorts, and you hear him say \"Just getting a towel\" in a voice that doesn't work."),
            T("He's going to think about this all day. Good."),
        ], [
            go("Take your time drying off.", loc="home_hall", mins=15, consumes=True,
               eff=[setv("ryan_step", 6)], flags=[done(6), fset("kayla_met")], wardrobe=[{"action": "equip", "item_id": "towel"}]),
        ]),
    ]})

# ── step 7 · Ryan A 8 · the first kiss ──
out.append({
    "id": "ryan_07_first_kiss", "name": "The first kiss",
    "description": "Ryan step 7 (Ryan A 8). She kisses him first; his no: \"I've got a girlfriend.\"",
    "trigger": step_trigger(R, 7, retry_days=3),
    "nodes": [
        node("knocks", "Two knocks", [
            P("Two knocks. He opens on the first one. His door's been open a hand's width every evening since the shower, and you both know why. Neither of you sits down."),
            D(R, "Kayla's not coming tonight."),
            ME("I didn't ask."),
        ], [
            go("Kiss him.", node="kiss", mins=5),
            go("\"Goodnight, Ryan.\"", loc="home_hall", mins=2, retry=3),
        ]),
        node("kiss", "Kiss", [
            P("You kiss him first. Ryan goes still for one second, but then his mouth opens hot on yours. His hands drop to your ass. He pulls you in hard against him. His cock is rigid through his jeans, pressed right where you want it. Your tits flatten on his chest. Your nipples go tight. \"@player.nickname,\" he says into the kiss, and his breath comes ragged in your mouth. You are wet already. You grind your hips into his cock, slow, until his fingers dig deeper into your ass."),
            VID("a couple kissing hard in a bedroom doorway, his hands on her ass, her hips pressed into him", "couple kissing hard hands on ass bedroom", "passionate kiss grinding against him bedroom door", file="sex/ryan_07_kiss_t4.webm"),
        ], [
            go("\"Don't stop.\"", node="text", mins=10),
        ]),
        node("text", "Her text", [
            P("His phone lights up on the desk behind him. KAYLA. A heart. He sees it over your shoulder and his whole body goes tight against you."),
            P("You reach past him and turn it face-down without breaking the kiss."),
        ], [
            go("\"Ignore it.\"", node="his_no", mins=3, eff=[add("corruption", 3), nadd(R, "want", 10)]),
        ]),
        node("his_no", "His no", [
            P("He ignores it for ten more seconds. Then he takes your face in both hands and pulls back, breathing like he ran up the stairs."),
            D(R, "@player.nickname. I've got a girlfriend."),
            ME("I know. I read her texts."),
            D(R, "That's not— I can't think when you do that."),
            T("He didn't let go of your face to say it."),
        ], [
            go("\"Then think about it.\"", loc="home_hall", mins=3, consumes=True,
               eff=[setv("ryan_step", 7)], flags=[done(7)]),
        ]),
    ]})

# ── step 8 · Ryan A 9 · two knocks: the release's door ──
HUNGRY = trait("corruption", "gte", 60)
def term_node(nid, name, blocks, flagname):
    return node(nid, name, blocks, [
        go("Go back to your room.", loc="home_hall", mins=5, consumes=True,
           eff=[setv("ryan_step", 8)], flags=[fset(flagname), done(8)]),
        go("Two knocks", node="next_release", swl=True, cond_=cond(HUNGRY), retry=1),
    ])

out.append({
    "id": "ryan_08_two_knocks", "name": "Two knocks",
    "description": "Ryan step 8 (Ryan A 9), the release's door: \"Two knocks\" shows locked, naming the stage it needs (Hungry, Corruption 60).",
    "trigger": step_trigger(R, 8, retry_days=1),
    "nodes": [
        node("ask", "What do I get", [
            P("Two knocks. He opens it, and his phone is already face-down on the desk. It's face-down every time you knock now."),
            ME("Kayla gets Fridays. What do I get?"),
        ], [go("Wait for his answer.", node="terms", mins=3)]),
        node("terms", "His terms", [
            P("He sits on the edge of his bed and rubs his face with both hands. When he looks up, he isn't pretending any more."),
            D(R, "Two knocks. Any night that isn't Friday."),
            G(cond(flag("jake_met")), D(R, "And Jake? The guy who walks you to the door?")),
            T("He's asking you to be his secret. He's asking you what the rules are."),
        ], [
            go("\"Keep Kayla. I like being the secret.\"", node="keep", mins=2),
            go("\"End it with her.\"", node="end", mins=2),
            go("\"Mom finds out when I want.\"", node="mom", mins=2),
            go("\"Your secret's safe. You're my brother, that's all.\" (ends his path)", node="final", mins=2),
        ]),
        term_node("keep", "The secret", [
            ME("Keep Kayla. I like being the secret."),
            P("He laughs, a short helpless sound, and pulls you down onto his knee by your wrist, and kisses your neck once, hard."),
            D(R, "You're going to get us killed."),
        ], "ryan_terms_keep_kayla"),
        term_node("end", "End it", [
            ME("End it with her."),
            P("He goes quiet. Then he picks up his phone, looks at Kayla's name for a long time, and puts it down again without typing anything."),
            D(R, "Give me a week. Two knocks, though. Starting now."),
        ], "ryan_terms_end_kayla"),
        term_node("mom", "Your call", [
            ME("Mom finds out when I want."),
            P("His face changes. That's the part that scares him, and he wants you anyway, and you can see both on him at once."),
            D(R, "Okay. Your call. Two knocks."),
        ], "ryan_terms_mine"),
        node("final", "Brother", [
            ME("Your secret's safe. You're my brother, that's all."),
            P("He nods slowly, like he expected it. He picks up his phone and turns it face-up again."),
            D(R, "Right. Goodnight, @player.nickname."),
            P("He doesn't open to two knocks after that. He opens to one, politely, like you're a guest."),
        ], [go("Go to your room. (ends his path)", loc="home_hall", mins=3, final=True,
               eff=[setv("ryan_step", -1, clamp=False)], flags=[fset("ryan_08_two_knocks_closed")])]),
        node("next_release", "Further", [
            P("You knock twice on his chest instead of his door, and he pulls you down onto the bed."),
            P("Ryan's next step (Ryan A 10) is in the next release of First Term."),
        ], [go("Go back to your room.", loc="home_hall", mins=3, retry=1)]),
    ]})

# ── the repeat it turns into: two knocks, any night but Friday (ryan_08 sheet) ──
out.append({
    "id": "ryan_two_knocks", "name": "Two knocks on his door",
    "description": "The repeat after Ryan step 8: kissing on his bed, his hands over her clothes. Not explicit in 0.1 (DECISIONS 29). Corruption +1 a night until she is past Bold. Once a night.",
    "trigger": {"location": "home_ryan_room", "requires_npc": R, "is_repeatable": True, "priority": 5,
                "is_active": True, "max_triggers_per_day": 1,
                "schedules": [{"weekdays": [0, 1, 2, 3, 5, 6], "start_time": "22:00", "end_time": "00:00"}],
                "conditions": cond(trait("ryan_step", "eq", 8))},
    "nodes": [
        node("bed", "His bed", [
            POOL(
                P("Two knocks. He's off the bed and opening it before the second one lands, and he locks it behind you. You're on his mattress with his mouth on yours before either of you says anything. He kisses like he's been waiting all day, because he has."),
                P("Two knocks. He opens it in a T-shirt and boxers and pulls you in by the waist. You fall onto the bed together, laughing, then not laughing, his mouth on your neck and his weight on you, the game still on with the sound off."),
                P("Two knocks. He leaves the lamp on. He wants to see you. You lie on his bed with your head on his pillow and he kisses you slowly, holding himself up on his arms, looking at you between kisses like he can't believe you're in here."),
                pid="ryan_two_knocks_open"),
            P("His hands go everywhere they're allowed. Over your clothes, down your sides, over your hips, up under your hair. He holds your waist like he's stopping himself. When he pulls you against him you can feel how hard he is, and he groans into your mouth and doesn't do anything about it."),
            G(cond(flag("ryan_terms_keep_kayla")), D(R, "She texted. I didn't answer. Come here.")),
            G(cond(flag("ryan_terms_end_kayla")), D(R, "I'm telling her this week. I swear. Don't stop.")),
            G(cond(flag("ryan_terms_mine")), D(R, "If Mom hears us, it's your call. Your call. Jesus.")),
            G(cond({"type": "npc_at_location", "location_id": "home_living_room", "npc_id": "npc_mark", "operator": "is_present"}),
              P("Mark's TV drones up through the floor. Every time it goes quiet, you both stop breathing.")),
            T("This is as far as he'll let himself go. For now."),
        ], [
            go("Kiss him until you can't breathe.", loc="home_hall", mins=60, eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 59}, {"targetType": "npc", "npcId": R, "trait": "warmth", "op": "add", "value": 1, "cap": 100}]),
            go("Take it further.", node="further", swl=True, cond_=cond(HUNGRY)),
            go("Just a goodnight kiss.", node="goodnight", mins=10, eff=[{"targetType": "npc", "npcId": R, "trait": "warmth", "op": "add", "value": 1, "cap": 100}]),
        ]),
        node("goodnight", "Goodnight", [
            P("You give him one kiss at the door, slow, and stop his hands with yours when they go to your waist. He groans and rests his forehead on yours."),
            D(R, "Tomorrow. Two knocks. Promise me."),
        ], [go("\"Tomorrow.\"", loc="home_hall", mins=2)]),
        node("further", "Further", [
            P("You push his hand down past your waistband and he stops dead and looks at you."),
            P("What happens next with Ryan is in the next release of First Term."),
        ], [go("Go back to your room.", loc="home_hall", mins=5)]),
    ]})

# ── his hub: his room, every window (npc_ryan sheet: his lines by what she wears) ──
SHY = trait("corruption", "lt", 20)
WARM = trait("corruption", "gte", 20)
out.append({
    "id": "hub_ryan_room", "name": "Ryan",
    "description": "Ryan's hub in his room. His Want and Warmth colour it; his lines read what she wears. Warmth gates his cover on a short weekend.",
    "trigger": {"location": "home_ryan_room", "npc": R, "requires_npc": R, "is_repeatable": True,
                "priority": 6, "is_active": True, "conditions": cond(flag("opening_done"))},
    "nodes": [
        node("room", "Ryan's room", [
            G(cond(trait("ryan_step", "lt", 0)),
              P("Ryan looks up from his phone, polite, like you're a guest."),
              D(R, "Need something?")),
            G(cond(trait("ryan_step", "gte", 0), ntrait(R, "want", "lt", 40)),
              P("Ryan is on his bed with his headphones round his neck and his phone in his hand. He sits up when you come in, and his eyes go to you and away too fast."),
              D(R, "What's up?")),
            G(cond(trait("ryan_step", "gte", 0), ntrait(R, "want", "gte", 40), ntrait(R, "want", "lt", 70)),
              P("Ryan puts his phone face-down when you come in. He looks at you, all of you, and doesn't pretend he isn't."),
              D(R, "Hey, @player.nickname. Shut the door.")),
            G(cond(trait("ryan_step", "gte", 0), ntrait(R, "want", "gte", 70)),
              P("Ryan's on his feet before you've shut the door. He stops an arm's length away, like that's the deal he made with himself."),
              D(R, "You can't keep walking in here looking like that.")),
            G(cond({"type": "worn_type", "operator": "eq", "value": "towel"}),
              D(R, "Door's free, @player.nickname."), P("His eyes drop and come back up.")),
            G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}),
              D(R, "You're wearing that downstairs?"), P("He doesn't look away from your ass when you turn.")),
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "worn_exposure", "operator": "eq", "value": 0}),
              P("He talks to your face, hard, and fails. Twice.")),
            G(cond({"type": "worn_exposure", "operator": "eq", "value": 1}, {"type": "worn_type", "operator": "neq", "value": "towel"}),
              D(R, "Jesus. Mom's home."), P("He goes and shuts his door, then stands there with his hand on it, not opening it again.")),
            G(cond(ntrait(R, "warmth", "gte", 70)),
              P("He's on your side. He'd cover for you with Laura in a heartbeat, and you both know it.")),
            G(cond(flag("knows_about_kayla"), trait("ryan_step", "gte", 0)),
              P("Kayla's hair tie is on his desk, next to his phone. He sees you see it.")),
            G(cond(SHY), T("You should knock first. You should stop looking at his arms.")),
            G(cond(WARM, trait("ryan_step", "gte", 0)), T("You like it when he looks. You like it more when he tries not to.")),
        ], [
            go("Sit and talk.", node="talk", mins=30, cond_=cond(flag("ryan_talk_today", False)),
               flags=[fset("ryan_talk_today")], eff=[{"targetType": "npc", "npcId": R, "trait": "warmth", "op": "add", "value": 2, "cap": 100}]),
            go("\"I'm short on the rent.\"", node="cover", mins=10,
               cond_=cond(wd(5, 6), tod("07:30", "12:00"), trait("money", "lt", 75), flag("rent_starts"),
                          flag("ryan_covered", False), flag("ryan_cover_today", False), ntrait(R, "warmth", "gte", 40), trait("ryan_step", "gte", 0)),
               flags=[fset("ryan_covered"), fset("ryan_cover_today")],
               eff=[{"targetType": "player", "trait": "money", "op": "add", "value": 25, "clamp": False}, nadd(R, "warmth", 5)]),
            go("Leave him to it.", loc="home_ryan_room"),
        ]),
        node("talk", "Talk", [
            POOL(
                P("You sit on the end of his bed and he tells you about the yard, about a guy who dropped a pallet on his own foot. You laugh. He watches you laugh."),
                P("He asks about college. Not like Mom does. He wants to know who's annoying and who's cute, and he goes quiet when you tell him who's cute."),
                P("You lie across the foot of his bed and talk about nothing for half an hour, about Mark mostly, and how much you both want out of this house."),
            ),
            D(R, "You're all right, you know. For a sister."),
        ], [go("Go.", loc="home_ryan_room", mins=5)]),
        node("cover", "Short", [
            P("He doesn't ask what you spent it on. He gets his wallet off the desk and counts out what he has and pushes it into your hand, and holds your hand a second too long."),
            D(R, "Don't tell Mark it came from me. He'll take it as a loan."),
            T("It's not your money. Sunday it'll look like yours, but it won't count."),
        ], [go("\"Thank you.\"", loc="home_ryan_room", mins=5)]),
    ]})

# ── his bathroom window: "Ryan's in there." (weekday mornings, Laura's rule) ──
out.append({
    "id": "hub_ryan_bathroom", "name": "Ryan's in there",
    "description": "Ryan in the bathroom on weekday mornings: the door, one line.",
    "trigger": {"location": "home_bathroom", "npc": R, "requires_npc": R, "is_repeatable": True,
                "priority": 6, "is_active": True, "conditions": cond(flag("opening_done"))},
    "nodes": [
        node("door", "The bathroom door", [
            P("The shower's running. The door doesn't lock properly, but it's shut, and his towel is gone from the rail in the hall."),
            POOL(D(R, "Two minutes!"), D(R, "Mom's rule, @player.nickname. Wait your turn."), D(R, "You can come in if you want to brush your teeth. I won't look."), pid="ryan_bathroom_lines"),
            G(cond(flag("ryan_heard_her")), D(R, "Don't stand right outside the door. I can hear you breathing.")),
            G(cond(trait("jake_step", "eq", 2)), D(R, "Who's Jake? Some guy's texting you. Your phone was on the sink.")),
        ], [go("Wait your turn.", loc="home_hall", mins=10), go("Leave.", loc="home_hall")]),
    ]})

# ── his things, while he's out (the place sheet: first find sets a memory flag) ──
out.append({
    "id": "ryan_things", "name": "Go through his things",
    "description": "While Ryan is out. Once a day. The first find sets ryan_things_found.",
    "trigger": {"location": "home_ryan_room", "is_repeatable": True, "priority": 3, "is_active": True,
                "max_triggers_per_day": 1,
                "conditions": cond({"type": "npc_at_location", "location_id": "home_ryan_room", "npc_id": R, "operator": "is_absent"})},
    "nodes": [
        node("things", "His things", [
            P("His room smells like him: deodorant, the yard, something warm. His bed isn't made. You open his drawers one at a time, quietly, listening for the front door."),
            POOL(
                P("Under his socks, a box of condoms, opened, half gone. You count them. You put them back exactly where they were."),
                P("A hoodie on the chair that's softer than anything you own. You put your face in it before you can stop yourself."),
                P("In the bedside drawer, a photo strip from a booth: Ryan and a girl with long dark hair, kissing in the last frame. On the back, in pen, a heart and a K."),
                P("His laptop is open on the desk, locked. The wallpaper is a beach somewhere he's never been. There's a sticky note on the screen in his writing: *money for the car, not for Mark*."),
            ),
        ], [
            go("Put it all back.", loc="home_ryan_room", mins=15, cond_=cond(flag("ryan_things_found", False)), flags=[fset("ryan_things_found")]),
            go("Put it all back.", loc="home_ryan_room", mins=15, cond_=cond(flag("ryan_things_found"))),
        ]),
    ]})

cards = step_cards(R, {
    1: ("Ryan, in the hall, on your first morning.", "Your first morning: out of the shower, the hall"),
    2: ("Ryan looks at you, then away too fast. He showers first on weekday mornings, and his phone is always on the sink.", "Go into the bathroom while Ryan showers, a weekday morning (Daring)"),
    3: ("You know about Kayla. He knows you know. His secret has a price.", "Knock on Ryan's door on an evening he's home (Curious, Daring)"),
    4: ("Two knocks, and he opens. He leaves room on the bed.", "Two knocks on Ryan's door late at night, not Friday"),
    5: ("Kayla stays over on Fridays. Your bed is against his wall.", "Be in your bed on a Friday night (Curious, Showing)"),
    6: ("He heard you through the wall. Kayla's still in the house on Saturday morning.", "Take a shower on Saturday morning (Bold, Showing)"),
    7: ("Since the shower, his door is open a hand's width every evening.", "Two knocks on Ryan's door on an evening he's home (Bold)"),
    8: ("He said he's got a girlfriend. He didn't let go of you when he said it.", "Two knocks on Ryan's door, an evening after the kiss (Bold)"),
}, terminal_text=("Two knocks, any night but Friday. His room, after ten.", "Ryan's next step comes in the next release."),
   closed_text="He's your brother now, polite and cold. Nothing more.", skip=(1,))

text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · RYAN (sheets/scenes/ryan_0*.md, sheets/people/npc_ryan.md)\n"
        "# Steps 2-8 (Ryan A 3-9), his hubs, his things, the two-knocks repeat, his cards.\n"
        "# Step 1 is the opening (2_one_shots.toml). Explicit screens pasted as signed.\n"
        "# =============================================================================\n")
text += "".join(emit(c) for c in out) + "".join(emit_card(c) for c in cards)
open(__import__("sys").argv[1], "w").write(text)
print("ryan:", len(out), "canvases,", len(cards), "cards")
