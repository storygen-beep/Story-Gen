"""Ryan — steps 2-8 (Ryan A 3-9), his hubs, his things, the two-knocks repeat.
Source: sheets/scenes/ryan_0*.md, sheets/people/npc_ryan.md. Explicit screens pasted as signed."""
from canv import *
from sheetbeats import beat, pool
from tomlw import tod, wd
def cap(k, n, c):   # (DECISIONS 124) used by the steps above the hot repeatables too
    return {"targetType": "player", "trait": k, "op": "add", "value": n, "cap": c}

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
            P("His eyes find you in the mirror through the steam. They drop down your back to your ass and stay there. Then he catches himself, looks at the tiles, and turns to face the wall, fast, so you can't see the front of him. Then his phone buzzes on the edge of the sink, right by your hand. The screen lights up: a name, Kayla, and a heart, and a message that starts *can't wait for friday, sneak me in the back again*."),
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "worn_type", "operator": "eq", "value": "thin_top"}),
              P("In the steam your sheer blouse sticks to you. There's no bra under it, and the mirror shows him that too.")),
        ], [
            go("Read it.", node="read", mins=3, flags=[fset("knows_about_kayla"), fset("kayla_met")]),   # her texts and her photo: Kayla is known from here (the People page)
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
               eff=[nadd(R, "want", 5), setv("ryan_step", 2)], flags=[done(2)]),
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
            # the risk (ryan_03_shirt_off.md, signed 2026-11-01): Laura, nearly. Only when her row has her downstairs.
            G(cond({"type": "npc_at_location", "location_id": "home_kitchen", "npc_id": "npc_laura", "operator": "is_present"}),
              D("npc_laura", "Ryan? Is your sister in there?"),
              P("Her voice comes up the stairs. Ryan doesn't take his eyes off you."),
              D(R, "No.")),
            D(R, "Happy?"),
            P("Your mouth has gone dry. You make yourself look at all of him before you stand up, so he knows you did."),
            T("Your step-brother. You just made him strip for you, and you want to do it again."),
            ME("Two knocks. That's me. Open the door when you hear it."),
        ], [
            go("\"Two knocks. That's me.\"", loc="home_hall", mins=5, consumes=True,
               eff=[nadd(R, "want", 5), add("corruption", 1, cap=79), setv("ryan_step", 3)],
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
            D(R, "Mom's gone to bed. Mark's downstairs. Get in before someone sees."),
        ], [
            go("\"Feet up.\"", node="lap", mins=5, wardrobe=[{"action": "unequip", "item_id": "sneakers"}]),
            go("\"Just saying goodnight.\"", node="night", mins=2),
        ]),
        node("night", "Night", [
            D(R, "Yeah. Night, @player.nickname."),
            P("He doesn't shut his door until you're in your room."),
        ], [go("Go to bed.", loc="home_hall", mins=2, retry=1)]),
        node("lap", "His lap", [
            P(beat("ryan_04_feet_in_his_lap", "lap")),
            VID("a girl's bare foot pressed into a young man's lap on a bed, his hand holding her ankle, phone at his ear", "foot on his crotch on bed phone call", "girl foot rubbing guy lap on bed", pool_dir="sex/ryan_04_lap_t4"),
        ], [
            go("Keep your toes moving.", node="liar", mins=10),
        ]),
        node("liar", "Liar", [
            D("npc_kayla", "Who's there?"),
            P("Kayla's voice, small and sharp out of the phone. Ryan lets go of your foot like it burned him."),
            D(R, "No one. The TV."),
            P("He says it to the wall. He hangs up, and sits there breathing, and doesn't look at you."),
            T("He lied to her with your foot in his lap. He'd do it again."),
        ], [
            go("\"Liar.\"", loc="home_hall", mins=5, consumes=True,
               eff=[nadd(R, "want", 5), cap("corruption", 3, 79), setv("ryan_step", 4)], flags=[done(4)]),  # a Bold one-time step: +3, cap 79 (DECISIONS 124)
        ]),
    ]})

# Kayla is named on step 4's screens: read on the way, as set at step 2 (her texts; gates: no one is named before they're met)
require_present(out, "ryan_04_feet_in_his_lap", flag("kayla_met"))

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
            go("Put your headphones in.", node="headphones", mins=2),
        ]),
        node("headphones", "Headphones", [
            P("You jam your headphones in and turn the music up until the wall goes away. It takes three songs before you stop hearing it anyway, and you lie there with the volume too loud and your face still hot."),
        ], [go("Leave them in.", loc="home_ella_room", mins=15, retry=7)]),
        node("listen", "Listen", [
            P("The headboard thuds against the wall. Thud. Thud. Faster. You lie still and listen on purpose. Kayla moans, high and broken. \"Harder. Don't stop. Right there, Ryan, right there.\" Ryan groans her name, low and rough. That's your brother's voice. Your nipples go tight against the sheet. Your breath comes short. Heat pools between your thighs until you're wet. *That's Ryan. You should be grossed out.* You aren't, but that scares you less than how badly you want to hear more. The headboard speeds up. Kayla cries out. Your hand slides down your stomach and stops an inch above your clit, aching to keep going."),
            VID("in bed at night under a sheet, a girl listening to a couple through the wall, her hand on her stomach", "girl in bed at night listening through wall touching herself", "woman under sheet hand sliding down stomach dark bedroom", file="sex/ryan_05_listen_t4.webm"),
        ], [
            go("Touch yourself.", node="act", mins=10),
            go("Roll over.", node="roll_over", mins=2),
        ]),
        node("roll_over", "Roll over", [
            P("You roll over to face the door and pull the pillow over your head. The headboard still comes through it, slower now, then not at all. You lie there breathing slow, waiting for your heart to settle."),
        ], [go("Try to sleep.", loc="home_ella_room", mins=10, retry=7)]),
        node("act", "In time with him", [
            P("Your hand slides down under the sheet. Your fingers find your clit, and you're already wet. On the other side of the wall, Ryan's headboard knocks, slow and hard. You rub in time with it. Kayla moans his name. You picture his cock sinking into her, his hands full of her ass, her tits bouncing with every thrust. Your other hand finds a nipple and pinches. Your hips lift off the mattress. The headboard speeds up, so you speed up. Your thighs start to shake. Then Ryan groans through the wall, low and rough, and that does it. You come hard, biting the pillow, but a moan still gets out of you. The headboard stops dead, while your thighs clamp tight around your hand and your clit is still throbbing under your fingers."),
            VID("a girl in bed touching herself under the sheet, hips lifting, biting a pillow as she comes", "girl masturbating under sheet biting pillow orgasm", "woman fingering herself in bed at night hips arching", file="sex/ryan_05_act_t5.webm"),
        ], [
            go("Lie still.", node="after", mins=5, eff=[add("corruption", 1, cap=79), nadd(R, "want", 5)]),
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
            P(beat("ryan_06_after_the_shower", "look")),
            VID("a wet naked girl out of the shower, a guy in the bathroom doorway with his cock out, stroking", "naked girl shower guy in doorway jerking off", "guy masturbating watching naked wet woman bathroom", pool_dir="sex/ryan_06_look_t5"),
        ], [
            go("Watch him.", node="comes", mins=3, eff=[cap("exhibitionism", 3, 79), add("corruption", 1, cap=79)]),  # DECISIONS 124: cap 79
        ]),
        node("comes", "Babe?", [
            P(beat("ryan_06_after_the_shower", "comes")),
            VID("a guy in a bathroom doorway coming in his hand, a naked wet woman watching", "guy cums in hand watching naked woman bathroom", "man finishes jerking off bathroom doorway", pool_dir="sex/ryan_06_comes_t5"),
        ], [
            go("Take your time drying off.", node="after6", mins=15),
        ]),
        node("after6", "His door", [
            P("When you come out, his door is open a hand's width."),   # false lines a3 #6: no promise it stays open
        ], [
            go("Go to your room.", loc="home_hall", mins=2, consumes=True,
               eff=[nadd(R, "want", 5), setv("ryan_step", 6)], flags=[done(6), fset("kayla_met")], wardrobe=[{"action": "equip", "item_id": "towel"}]),
        ]),
    ]})

# ── step 7 · Kayla can't know (ryan_07_kayla_cant_know.md, signed 2026-11-01; replaces the first kiss, cut) ──
HUNGRY = trait("corruption", "gte", 60)
out.append({
    "id": "ryan_07_kayla_cant_know", "name": "Kayla can't know",
    "description": "Ryan step 7 (release 1): two knocks; her hand on him to the end while Kayla's photo lights up his phone. His phone is face-down every time after.",
    "trigger": step_trigger(R, 7, retry_days=7),
    "nodes": [
        node("knocks", "Two knocks", [
            # (reader fix) the measured beat knocks and opens the door itself: this screen only brings her to it
            P("An evening he's home. His light is on under his door, and you both know why you're here."),
        ], [
            go("Knock twice.", node="hand", mins=3),
            go("Leave him to it.", loc="home_hall", mins=2, retry=7),
        ]),
        node("hand", "Kayla's photo", [
            P(beat("ryan_07_kayla_cant_know", "hand")),
            VID("a girl's hand stroking a guy's cock on his bed, his phone lighting up beside him", "handjob on bed phone ringing", "girl jerking off boyfriend on bed phone call", pool_dir="sex/ryan_07_hand_t5"),
        ], [go("\"Don't answer it.\"", node="phone", mins=3)]),
        node("phone", "Don't answer it", [
            P(beat("ryan_07_kayla_cant_know", "phone")),
        ], [go("Make him come.", node="comes", mins=5)]),
        node("comes", "Voicemail", [
            P(beat("ryan_07_kayla_cant_know", "comes")),
            VID("a guy coming in a girl's hand on his bed, a phone buzzing next to them", "guy cums in her hand on bed", "handjob finish bed phone buzzing", pool_dir="sex/ryan_07_comes_t5"),
        ], [
            go("Wipe your hand on his shirt.", node="after7", mins=5),
        ]),
        node("after7", "Face-down", [
            P("You wipe your hand on his shirt and leave him lying there."),
            P("From now on his phone is face-down every time you knock."),
        ], [
            go("Go to your room.", loc="home_hall", mins=2, consumes=True,
               eff=[nadd(R, "want", 5), cap("corruption", 3, 79), setv("ryan_step", 7)], flags=[done(7)]),  # DECISIONS 124: cap 79
        ]),
    ]})

# ── step 8 · two knocks, the first time (ryan_08_two_knocks_first_sex.md, signed 2026-11-01). Sun-Thu, not
#    "any night but Friday": its screens put Laura across the hall (her room 22:00-23:00 awake, then asleep), and
#    on Saturday nights she waits up downstairs. Replaces the talk (cut); the terms move here, after. ──
def term_exit(text, flagname, final=False):
    extra = dict(final=True) if final else dict(consumes=True)
    # LO 2026-11-03: his Want pays for what happened, never for a no. The +5 is on the sex ("Lie there."); his
    # terms, and "(ends his path)", add 0.
    eff = [setv("ryan_step", 8)] if not final else [setv("ryan_step", -1, clamp=False)]
    flags = [fset(flagname), done(8)] + ([funset("ryan_knock_code"), fset("ryan_08_two_knocks_closed")] if final else [])
    return go(text, loc="home_hall", mins=5, eff=eff, flags=flags, wardrobe=DRESS_DAY, **extra)   # undressed on `undress` (DECISIONS 127)

S = "ryan_08_two_knocks_first_sex"   # the step sheet its screens are read from
out.append({
    "id": "ryan_08_two_knocks_first_sex", "name": "Two knocks",
    "description": "Ryan step 8 (release 1), the top step: first sex in his room, his headboard on her wall, Laura's light coming on across the hall. Inside her or on her, her pick; then his terms. The repeat opens; step 9 shows locked.",
    "trigger": step_trigger(R, 8, retry_days=1),
    "nodes": [
        # DECISIONS 127 (LO, 2026-11-02, "rise from normal"): a talk, her doubt, a kiss, undressing, a no at each rung;
        # her picks in the sex (what first, how, Laura's light, the finish); her feeling after; then his terms.
        node("knocks", "Two knocks, late", [
            P("Two knocks, late. He opens on the first one, and his phone is already face-down on the desk. It's face-down every time you knock now."),
            D(R, "Kayla's at her mom's tonight."),
        ], [
            go("Come in.", node="talk", mins=3),
            go("\"Not tonight.\"", loc="home_hall", mins=2, retry=1),
        ]),
        node("talk", "His bed", [
            P("You sit on the edge of his bed. He sits too, a foot away, like there's a line down the mattress. Neither of you says what happened the last time you knocked."),
            D(R, "So. These walls, huh."),
            P("It's a joke, and it lands wrong, and you both laugh too loud and then stop. He rubs the back of his neck. He looks at the door, then at you."),
            D(R, "Last time. With Kayla calling. That can't happen again."),
            P("He says it, and he doesn't move away. His knee is an inch from yours."),
        ], [go("\"Then why did you open the door?\"", node="doubt", mins=3)]),
        node("doubt", "Ryan", [
            P("He doesn't answer. His knee touches yours and stays there. He's looking at your mouth and he isn't hiding it any more, and the front of his shorts isn't hiding anything either."),
            T("This is Ryan. You should go."),
        ], [
            go("Stay.", node="kiss", mins=2),
            go("Go.", loc="home_hall", mins=2, retry=1),
        ]),
        node("kiss", "The kiss", [
            P(beat(S, "kiss")),
            VID("a guy and a girl kissing on his bed at night, his hand under her top", "making out on bed hand under shirt", "kissing on bed he touches her tits through bra", pool_dir="sex/ryan_08_kiss_t4"),
        ], [
            go("Let him.", node="undress", mins=5),
            go("Stop. \"Not tonight.\"", loc="home_hall", mins=2, retry=1),
        ]),
        node("undress", "One piece at a time", [
            P(beat(S, "undress")),
            VID("a couple undressing each other on a bed, one piece at a time", "undressing each other slowly on bed", "he pulls her panties down slow", pool_dir="sex/ryan_08_undress_t4"),
        ], [
            go("Go down on him.", node="suck", mins=5, wardrobe=STRIP),
            go("Let him taste you.", node="lick", mins=5, wardrobe=STRIP),
            go("Get on him.", node="ride", mins=5, wardrobe=STRIP),
        ]),
        node("suck", "On your knees", [
            P(beat(S, "suck")),
            VID("a girl on her knees by a bed sucking a guy's cock, his hand in her hair", "blowjob kneeling by bed hand in hair", "she sucks his cock quietly", pool_dir="sex/ryan_08_suck_t5"),
        ], [
            go("Ride him.", node="ride", mins=5),
            go("On your back.", node="under", mins=5),
            go("Against the wall.", node="wall_back", mins=5),
        ]),
        node("lick", "His mouth", [
            P(beat(S, "lick")),
            VID("a guy eating a girl out on his bed, her hand over her mouth, thighs round his head", "he eats her pussy she covers mouth", "cunnilingus thighs around his head", pool_dir="sex/ryan_08_lick_t5"),
        ], [
            go("Ride him.", node="ride", mins=5),
            go("On your back.", node="under", mins=5),
            go("Against the wall.", node="wall_back", mins=5),
        ]),
        node("ride", "On top", [
            P(beat(S, "ride")),
            VID("a girl climbing onto a guy on his bed and sinking onto him, a headboard against the wall", "girl rides guy on bed first time", "riding him on his bed headboard", pool_dir="sex/ryan_08_bed_t5"),
        ], [go("\"Harder.\"", node="light", mins=5)]),
        node("under", "Under him", [
            P(beat(S, "under")),
            VID("missionary sex, slow, a guy on top looking at the girl's face", "slow missionary eye contact", "he fucks her slow on her back", pool_dir="sex/ryan_08_under_t5"),
        ], [go("\"Harder.\"", node="light", mins=5)]),
        node("wall_back", "Her wall", [
            P(beat(S, "wall_back")),
            VID("a girl kneeling on a bed with her palms on the wall, fucked from behind", "from behind hands on wall kneeling on bed", "doggy against bedroom wall", pool_dir="sex/ryan_08_wall_back_t5"),
        ], [go("\"Harder.\"", node="light", mins=5)]),
        node("light", "Laura's floorboards", [
            P(beat(S, "light")),
            VID("a couple fucking on a bed, the headboard banging the wall, both of them frozen, listening to the hall", "riding hard headboard banging wall", "girl on top fucking headboard knocking", pool_dir="sex/ryan_08_wall_t5"),
        ], [
            go("Keep going.", node="keep", mins=3),
            go("Freeze.", node="freeze", mins=5),
        ]),
        node("keep", "Keep going", [
            P(beat(S, "keep")),
            VID("a guy fucking a girl hard with his hand over her mouth", "hand over mouth fucking hard quiet", "he covers her mouth while fucking", pool_dir="sex/ryan_08_keep_t5"),
        ], [
            go("\"Inside me.\"", node="inside", mins=3),
            go("\"On me.\"", node="on", mins=3),
            go("\"In my mouth.\"", node="mouth", mins=3),
        ]),
        node("freeze", "Freeze", [
            P(beat(S, "freeze")),
            VID("a couple holding still mid-sex, listening, then moving again slow", "frozen mid sex listening quiet", "slow sex trying not to be heard", pool_dir="sex/ryan_08_freeze_t5"),
        ], [
            go("\"Inside me.\"", node="inside", mins=3),
            go("\"On me.\"", node="on", mins=3),
            go("\"In my mouth.\"", node="mouth", mins=3),
        ]),
        node("inside", "Inside", [
            P(beat(S, "inside")),
            VID("a guy coming inside a girl, holding her hips down", "creampie he holds her hips", "he cums inside her", pool_dir="sex/ryan_08_inside_t5"),
        ], [go("Lie there.", node="after", mins=10, eff=[nadd(R, "want", 5)])]),
        node("on", "On you", [
            P(beat(S, "on")),
            VID("a guy pulling out and coming on a girl's stomach and tits on his bed", "guy pulls out cums on her", "cum on tits after sex bed", pool_dir="sex/ryan_08_on_t5"),
        ], [go("Lie there.", node="after", mins=10, eff=[nadd(R, "want", 5)])]),
        node("mouth", "Your mouth", [
            P(beat(S, "mouth")),
            VID("a girl on her knees by a bed, a guy coming in her mouth, she swallows", "cum in mouth kneeling swallow", "he finishes in her mouth", pool_dir="sex/ryan_08_mouth_t5"),
        ], [go("Lie there.", node="after", mins=10, eff=[nadd(R, "want", 5)])]),
        node("after", "After", [
            P("You lie with your head on his chest. His heart is still going hard under your ear. Across the hall, Laura's room is quiet again. Your thighs are sticky and your lips are sore and every part of you knows whose bed this is."),
            T("That was your brother. You should feel sick."),
            P("You don't. You feel warm all the way down, and you're already thinking about the next time you knock. That's the part that scares you."),
        ], [go("Ask him.", node="terms", mins=5)]),
        node("terms", "His terms", [
            P("After, you lie on his chest in the dark. Across the hall Laura's room has gone quiet again. He rubs his face with one hand. When he speaks, he isn't pretending any more."),
            D(R, "So what is this?"),
            G(cond(trait("jake_step", "gte", 3)), D(R, "And Jake? The guy who walks you to the door?")),
            T("He's asking you what the rules are."),
        ], [
            term_exit("\"Keep Kayla. I'm the secret.\"", "ryan_terms_secret"),
            term_exit("\"Mom finds out when I want.\"", "ryan_terms_mine"),
            term_exit("\"You're my brother, that's all.\" (ends his path)", "ryan_path_closed", final=True),
            # S12 (LO 2026-11-03, reverses DECISIONS 130): no release door. Ryan's quest card says where his arc
            # ends this release ("More of Ryan in the next release."), so the "Further." button and its screen are gone.
        ]),
    ]})

# Kayla is named on step 8's screens ("Kayla's at her mom's", undress): read on the way, as on step 4
require_present(out, "ryan_08_two_knocks_first_sex", flag("kayla_met"),
                {"type": "clothing_item", "item_id": "towel", "operator": "unequipped"})   # undress pulls her clothes over her head (reader)

# ── the hot repeatables, one per stage (ryan_hot_repeatables.md, signed 2026-11-01). Lust +3 once a day across all
#    seven (ryan_hot_today, the daily tick); each a shuffle-bag pool of three; none with Laura in the room. ──
HOT_FREE = flag("ryan_hot_today", False)
HOT_PAY = [nadd(R, "want", 3)]
HOT_FLAG = [fset("ryan_hot_today")]
LAURA_NOT_HERE = lambda loc: {"type": "npc_at_location", "location_id": loc, "npc_id": "npc_laura", "operator": "is_absent"}
CUR, DAR, BOLD_, SHOW = (trait("corruption", "gte", 20), trait("exhibitionism", "gte", 20),
                         trait("corruption", "gte", 40), trait("exhibitionism", "gte", 40))
UNDRESS_TO_UNDERWEAR = [{"action": "unequip", "item_id": g} for g in ALL_GARMENTS
                        if g not in ("plain_bra", "sports_bra", "plain_panties")]
BRA_AND_PANTIES = [{"type": "clothing_slot", "slot": "bra", "operator": "equipped"},
                   {"type": "clothing_slot", "slot": "underwear", "operator": "equipped"}]
def cap(k, n, c):
    return {"targetType": "player", "trait": k, "op": "add", "value": n, "cap": c}
def hot_exit(text, loc, mins, eff, wardrobe=None):
    """A hot repeatable's exit, day-capped on its own conditions as well as the button's (gates: the climb is paid for)."""
    return go(text, loc=loc, mins=mins, cond_=cond(HOT_FREE), eff=HOT_PAY + eff, flags=HOT_FLAG, wardrobe=wardrobe)
def hot_node(n, name, media, exits, back="home_hall"):
    # + an exit with neither conditions nor costs (gates: a spent day still has a door)
    return node(f"hot{n}", name, [POOL(*[P(t) for t in pool("ryan_hot_repeatables", n)], pid=f"ryan_hot_{n}", bag=True), *media],
                exits + [go("Leave him to it.", loc=back)])
# C4 (LO 2026-11-03): hygiene colours, and its colour can work like a lock. Dirty, she still sees the button and
# still goes to him, but it doesn't happen: he says why. Clean is hygiene 30+, or the hygiene system switched off.
DIRTY = [trait("hygiene", "lt", 30), flag("hygiene_off", False)]
def hot_choice(n, label, gate, wardrobe=None):
    return [go(label, node=f"hot{n}", mins=0, cond_=cond(HOT_FREE, *gate, trait("hygiene", "gte", 30)), wardrobe=wardrobe),
            go(label, node=f"hot{n}", mins=0, cond_=cond(HOT_FREE, *gate, trait("hygiene", "lt", 30), flag("hygiene_off")), wardrobe=wardrobe),
            go(label, node="ryan_stink", mins=0, cond_=cond(HOT_FREE, *gate, *DIRTY))]
def stink_node(back):
    return node("ryan_stink", "Not like that", [
        P("You get as far as him, and Ryan pulls his head back."),
        D(R, "Jesus. When did you last shower? Go and wash. Then come back."),
        T("You can smell it on yourself now too."),
    ], [go("Go and shower.", loc=back, mins=2)])
DRESS_BACK = DRESS_DAY
HOT_ROOM = [  # his room, evenings he's home (Mon, Tue, Thu, Sun 19:00-22:00)
    (1, "Lean in his doorway.", [trait("ryan_step", "gte", 2), CUR, flag("ryan_hall_seen")], None,   # a first tease, Curious, after the hall accident (DECISIONS 124)
     [], [hot_exit("\"Night, Ryan.\"", "home_hall", 10, [cap("corruption", 1, 39)])]),
    (4, "Lie on his bed. He only watches.", [trait("ryan_step", "gte", 6), BOLD_, SHOW], STRIP,   # naked by choice for one: Bold (DECISIONS 124)
     [VID("a naked girl on a bed touching herself, a guy in a chair gripping it, watching", "girl masturbates on his bed he watches", "only watch no touching girl fingers herself", pool_dir="sex/ryan_hot4_t5")],
     [hot_exit("Get dressed.", "home_hall", 30, [cap("corruption", 1, 59), cap("exhibitionism", 1, 59)], wardrobe=DRESS_BACK)]),
    (5, "Stand naked in his room. Tell him when.", [trait("ryan_step", "gte", 6), BOLD_, SHOW], STRIP,   # it pays Corruption: Bold too (DECISIONS 124, reader)
     [VID("a naked girl watching a guy stroke his cock in his bedroom, telling him when", "naked girl watches guy jerk off", "she tells him when to cum", pool_dir="sex/ryan_hot5_t5")],
     [hot_exit("Get dressed.", "home_hall", 30, [cap("exhibitionism", 1, 59), cap("corruption", 1, 59)], wardrobe=DRESS_BACK)]),
]
HOT_COUCH = [  # the couch, Sat/Sun 14:00-18:00
    (2, "Put your feet in his lap.", [trait("ryan_step", "gte", 4), BOLD_],   # private contact: Bold (DECISIONS 124)
     [{"action": "unequip", "item_id": "sneakers"}],
     [VID("bare feet rubbing a guy's crotch through his shorts on a couch, a game on", "feet in his lap rubbing his cock couch", "footjob through shorts gaming couch", pool_dir="sex/ryan_hot2_t4")],
     [hot_exit("\"Watch the game.\"", "home_living_room", 30, [cap("corruption", 1, 59)])]),
    (3, "Watch his game in your underwear.", [trait("ryan_step", "gte", 4), DAR] + BRA_AND_PANTIES, UNDRESS_TO_UNDERWEAR,
     [VID("a girl in her bra and panties on a couch, a guy with a controller adjusting himself", "girl in underwear on couch guy hard", "watching tv in underwear he gets hard", pool_dir="sex/ryan_hot3_t4")],
     [hot_exit("Get dressed.", "home_living_room", 30, [cap("exhibitionism", 1, 39), cap("corruption", 1, 39)], wardrobe=DRESS_BACK)]),
    # row 6: Mark's TV in the next room is only true when his row has him in the kitchen (Sunday 08:00-22:00)
    (6, "Share the blanket.", [trait("ryan_step", "gte", 7), HUNGRY, DAR,   # the taboo act at home: Hungry (DECISIONS 124)
                              
                               {"type": "npc_at_location", "location_id": "home_kitchen", "npc_id": "npc_mark", "operator": "is_present"}], None,
     [VID("a handjob under a blanket on a couch, a film on, someone in the next room", "handjob under blanket couch", "secret handjob under blanket family home", pool_dir="sex/ryan_hot6_t5")],
     [hot_exit("\"Just the film.\"", "home_living_room", 60, [cap("corruption", 1, 79), cap("exhibitionism", 1, 79)])]),
]

# ── the repeat after step 8: two knocks, a menu (hot repeatable 7; ryan_hot_repeatables.md "Row 7's menu", DECISIONS 127).
#    A normal start at the door (a bag of three), her pick of the act (more open as his Lust climbs: 70 / 80 / 90), a
#    shy or eager voice by her Corruption (split at 70), a near-catch screen (a bag of three), her pick of finish. ──
HR = "ryan_hot_repeatables"
# S2 (skill, LO 2026-11-03): every spoken line is a dialog block with its speaker. The signed beats write speech as
# quotes inside paragraphs; spoken() keeps every word and cuts the paragraph at each quote, in order, into
# narration and dialog (canv.speech; every other canvas goes through canv.voice_canvas and speech_table.py). The speakers are named per beat by hand ("R" Ryan, "ME" her, "L" Laura at the door).
SPEAKERS = {
    "7s_a": ["R"], "7s_b": ["R", "R"], "7s_c": ["R", "ME", "R", "R"],
    "7t_a": ["R", "R"], "7t_b": ["L", "R"], "7t_c": ["R", "R"],
    "7f_inside": ["R", "R", "ME", "ME"], "7f_on": ["R", "ME", "ME", "R"], "7f_mouth": ["R", "ME", "R"],
    "7suck_shy": ["R"], "7suck_eager": ["ME", "R", "ME"],
    "7ride_shy": ["ME", "ME"], "7ride_eager": ["R", "ME", "ME", "ME"],
    "7lick_shy": ["R"], "7lick_eager": ["ME", "ME", "ME"],
    "7wall_shy": ["R", "ME", "ME"], "7wall_eager": ["ME", "ME", "ME", "ME"],
}
def spoken(key):
    """One beat of the menu, cut into narration and dialog by canv.speech (the shared helper since 2026-11-03)."""
    return speech(beat(HR, key), [{"R": R, "L": "npc_laura"}.get(sp, sp) for sp in SPEAKERS.get(key, [])])
SHY_V, EAGER_V = trait("corruption", "lt", 70), trait("corruption", "gte", 70)
def voices(act):
    return [GC(cond(SHY_V), *spoken(f"7{act}_shy")), GC(cond(EAGER_V), *spoken(f"7{act}_eager"))]
TO_TWIST = [go("Don't stop.", node="twist", mins=10)]
FINISH_EXITS = [  # the day's pay split on ryan_hot_today, as built; dressed again for the hall
    go("Back to your room.", loc="home_hall", mins=20, cond_=cond(HOT_FREE), eff=[cap("corruption", 1, 79)] + HOT_PAY, flags=HOT_FLAG, wardrobe=DRESS_DAY),
    go("Back to your room.", loc="home_hall", mins=20, cond_=cond(flag("ryan_hot_today")), eff=[cap("corruption", 1, 79)], wardrobe=DRESS_DAY),
]
out.append({
    "id": "ryan_two_knocks", "name": "Two knocks on his door",
    "description": "The repeat after Ryan step 8 (hot repeatable 7): a menu. A normal start, her pick of the act (more open by his Lust 70/80/90), a shy or eager voice by her Corruption, a near-catch screen, her pick of finish. Corruption +1, cap 79; Lust +3 once a day.",
    "trigger": {"location": "home_ryan_room", "requires_npc": R, "is_repeatable": True, "priority": 5,
                "is_active": True, "max_triggers_per_day": 1,
                "schedules": [{"weekdays": [0, 1, 2, 3, 6], "start_time": "22:00", "end_time": "00:00"}],
                "conditions": cond(trait("ryan_step", "eq", 8))},
    "nodes": [
        node("door", "Two knocks", [P("Two knocks. His phone is face-down on the desk. It always is now.")], [
            go("Go in.", node="start", mins=2),
            go("\"Not tonight.\"", loc="home_hall", mins=2),
        ]),
        node("start", "His room", [POOL(*[GC({"version": "1.0", "logic": "AND", "items": []}, *spoken(f"7s_{k}")) for k in "abc"], pid="ryan_hot_7s", bag=True)], [
            go("Go down on him.", node="suck", mins=5, wardrobe=STRIP, cond_=cond(ntrait(R, "want", "gte", 70))),
            go("Ride him.", node="ride", mins=5, wardrobe=STRIP, cond_=cond(ntrait(R, "want", "gte", 70))),
            go("Let him taste you.", node="lick", mins=5, wardrobe=STRIP, swl=True, cond_=cond(ntrait(R, "want", "gte", 80))),
            go("Against the wall.", node="wall_back", mins=5, wardrobe=STRIP, swl=True, cond_=cond(ntrait(R, "want", "gte", 90))),
            go("Leave him to it.", loc="home_hall", mins=2),
        ]),
        node("suck", "On your knees", [*voices("suck"),
            VID("a girl on her knees by a bed sucking a guy's cock late at night", "blowjob kneeling by his bed night", "she sucks her stepbrother quietly", pool_dir="sex/ryan_hot7_suck_t5")], TO_TWIST),
        node("ride", "On top", [*voices("ride"),
            VID("a girl riding a guy on his bed, the headboard knocking the wall", "girl rides him headboard knocking", "quiet riding sex late night", pool_dir="sex/ryan_hot7_ride_t5")], TO_TWIST),
        node("lick", "His mouth", [*voices("lick"),
            VID("a guy eating a girl out on his bed, her hand over her mouth", "he eats her out she covers mouth", "cunnilingus quiet late night", pool_dir="sex/ryan_hot7_lick_t5")], TO_TWIST),
        node("wall_back", "Against the wall", [*voices("wall"),
            VID("a girl kneeling on a bed, palms on the wall, fucked from behind", "from behind palms on wall", "doggy against the bedroom wall", pool_dir="sex/ryan_hot7_wall_t5")], TO_TWIST),
        node("twist", "Late", [POOL(*[GC({"version": "1.0", "logic": "AND", "items": []}, *spoken(f"7t_{k}")) for k in "abc"], pid="ryan_hot_7t", bag=True),
            VID("a couple having sex in his bedroom late at night, keeping quiet", "quiet sex his bedroom late night", "sneaky sex step brother room", pool_dir="sex/ryan_hot7_twist_t5")], [
            go("\"Inside me.\"", node="f_inside", mins=3),
            go("\"On me.\"", node="f_on", mins=3),
            go("\"In my mouth.\"", node="f_mouth", mins=3),
        ]),
        *[node(f"f_{k}", "He comes", [*spoken(f"7f_{k}"),
            VID("a guy finishing, late at night in his bedroom", "he cums late night bedroom", "finish quiet sex", pool_dir="sex/ryan_hot7_finish_t5")], FINISH_EXITS)
          for k in ("inside", "on", "mouth")],
    ]})

# ── the towel at home (LO, 2026-10-31, DECISIONS 98): his reaction by his Lust, every visit, in his
#    hub's own bands (<40, 40-69, 70+); "Let it slip." (Daring) pays his Lust +2 and her Exhibitionism +1
#    once a day; "Drop it." needs Showing and his top band, no story step (LO, 2026-10-31). ──
from home_items import towel_set, TOWEL_CAUGHT, TOWEL_ON, DARING, SHOWING, EXH1, here, want as _want
RYAN_TOWEL_LEAD = [P("You loosen the tuck and let the towel slip. It drops to your waist before you catch it, and your tits are out, wet and bare, your nipples tight in the cold air.")]
RYAN_TOWEL_SLIP = [
    [P("Ryan turns his whole body away."), D(R, "Jesus, @player.nickname! Put it back!"),
     P("You pull it up. He doesn't turn round until you have, and his ears have gone red.")],
    [P("Ryan stops breathing. He looks at your tits for three whole seconds before you pull the towel back up, and he doesn't say a word."),
     P("His eyes stay on the knot after it's tied again.")],
    [P("Ryan's eyes go straight to your tits and stay there. He wets his lips."), D(R, "Leave it."),
     P("You hold the towel at your waist and let him look. His hand goes to the front of his shorts, and his cock is hard under it.")],
]
RYAN_TOWEL_DROP = [
    P("You pull the knot and let the towel fall to the floor. You're naked in front of him, still wet from the shower. Your tits are bare, your nipples hard. Your cunt is bare, and a drop of water runs down your thigh. Ryan's eyes go down your body and stop on your cunt. His cock is hard in his shorts, pushing the cotton out. He doesn't touch it. He doesn't touch you. He stares at your tits, at your cunt, at your tits again, breathing through his mouth."),
    P("You turn round slowly so he gets your ass too. You hear him swallow."),
    D(R, "Fuck, @player.nickname."),
    P("You bend and pick the towel up off the floor, slow, with your bare ass to him, and wrap it round your tits again."),
]


# reader a3 #7-8 (DECISIONS 131): "Hold the knot." after "One pull." (his Want 70+, her in the towel). "Not tonight."
# only in the evening and the night; his room's weekend mornings and the couch's afternoons get "Not now."
RYAN_TOWEL_NO = [
    P("You hold the knot over your tits with one hand and step back out of his reach."),
    GC(cond(tod("18:00", "06:00")), ME("Not tonight.")),
    GC(cond({"type": "worn_exposure", "operator": "gte", "value": 0}), ME("Not now.")),
    D(R, "Tease."),
    P("He grins, and he doesn't hide what the towel has done to the front of his shorts. His cock is hard under the cotton, and his eyes stay on the knot."),
]


def ryan_towel(hub, back, first_low, caught=True):
    return towel_set(
        hub, R, "want", 40, 70, "ryan_towel_today", [_want(R, 2), EXH1], back,
        lines=[
            [first_low,
             GC(cond(TOWEL_ON), P("Ryan looks at the ceiling, at the wall, at anything but you."), D(R, "Jesus. Put some clothes on, @player.nickname.")),
             P("He goes red to the ears and finds something very interesting on his phone.")],
            [P("His eyes go down the towel to your bare legs and come back up slow. He doesn't pretend he wasn't looking."),
             GC(cond(TOWEL_ON), D(R, "That towel's shrinking, @player.nickname."), P("He grins, and he doesn't look away.")),
             P("He looks at where it's tucked over your tits, and you watch him think about one tug.")],
            [GC(cond(TOWEL_ON), D(R, "You're doing this on purpose."), P("He's not asking. He's staring at the knot over your tits, and his shorts don't hide what it's doing to his cock.")),
             GC(cond(TOWEL_ON), P("He reaches out and runs one finger along the top of the towel, across your tits, and stops at the knot."), D(R, "One pull, @player.nickname.")),
             GC(cond(TOWEL_ON), D(R, "Mom's going to kill us both."), P("He says it to your tits, not your face."))],
        ],
        slip=RYAN_TOWEL_SLIP, slip_lead=RYAN_TOWEL_LEAD,
        slip_media=VID("a young woman in a bath towel letting it slip off her breasts in front of a young man, at home", "girl drops towel in front of guy", "towel slip flash at home", pool_dir="sex/towel_ryan_slip_t4"),
        drop=RYAN_TOWEL_DROP, drop_gate=[SHOWING],
        drop_media=VID("a young woman dropping her bath towel, standing naked in front of a young man in his room", "girl drops towel naked in front of him", "towel drop naked reveal", pool_dir="sex/towel_ryan_drop_t4"),
        caught_by="npc_laura" if caught else None, caught=TOWEL_CAUGHT,
        no=("Hold the knot.", RYAN_TOWEL_NO, "home_hall", "Go."))   # reader a3 #7-8 (DECISIONS 131, call A): his Want +1 once a day


# ── his hub: his room, every window (npc_ryan sheet: his lines by what she wears) ──
RT_ROOM = ryan_towel("hub_ryan_room", "home_ryan_room",
                     GC(cond(TOWEL_ON), D(R, "Door's free, @player.nickname."), P("His eyes drop and come back up.")))
SHY = trait("corruption", "lt", 20)
WARM = trait("corruption", "gte", 20)
out.append({
    "id": "hub_ryan_room", "name": "Ryan",
    "description": "Ryan's hub in his room. His Want and Warmth colour it; his lines read what she wears. Warmth gates his cover on a short weekend.",
    "trigger": {"location": "home_ryan_room", "npc": R, "requires_npc": R, "is_repeatable": True,
                "priority": 6, "is_active": True, "conditions": cond(flag("opening_done"))},
    "nodes": [
        node("room", "Ryan's room", [
            G(cond(flag("ryan_08_two_knocks_closed")),
              P("You knock once. He opens it on the first knock and goes back to his bed. Two knocks was a different door.")),
            G(cond(trait("ryan_step", "lt", 0)),
              P("Ryan looks up from his phone, polite, like you're a guest."),
              D(R, "Need something?")),
            G(cond(trait("ryan_step", "gte", 0), ntrait(R, "want", "lt", 40)),
              P("Ryan is on his bed with his headphones round his neck and his phone in his hand. He sits up, and his eyes go to you and away too fast."),
              D(R, "What's up?")),
            G(cond(trait("ryan_step", "gte", 0), ntrait(R, "want", "gte", 40), ntrait(R, "want", "lt", 70)),
              P("Ryan puts his phone face-down. He looks at you, all of you, and doesn't pretend he isn't."),
              D(R, "Hey, @player.nickname. Shut the door.")),
            G(cond(trait("ryan_step", "gte", 0), ntrait(R, "want", "gte", 70)),
              P("Ryan's on his feet before you've shut the door. He stops an arm's length away, like that's the deal he made with himself."),
              D(R, "You can't keep walking in here looking like that.")),
            *RT_ROOM[0],
            G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}),
              D(R, "You're wearing that downstairs?"), P("He doesn't look away from your ass when you turn.")),
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "worn_exposure", "operator": "eq", "value": 0}),
              P("He talks to your face, hard, and fails. Twice.")),
            G(cond({"type": "worn_exposure", "operator": "eq", "value": 1}, {"type": "worn_type", "operator": "neq", "value": "towel"}),
              D(R, "Jesus, @player.nickname."), P("He goes and shuts his door, then stands there with his hand on it, not opening it again.")),
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
               cond_=cond(wd(5), tod("07:30", "12:00"), trait("money", "lt", 75), flag("rent_starts"),
                          flag("ryan_covered", False), flag("ryan_cover_today", False), ntrait(R, "warmth", "gte", 40), trait("ryan_step", "gte", 0)),
               flags=[fset("ryan_covered"), fset("ryan_cover_today")],
               eff=[{"targetType": "player", "trait": "money", "op": "add", "value": 25, "clamp": False}, nadd(R, "warmth", 5)]),
            # (reader fix) on Sunday only before Mark's count: "At the table it'll look like yours"
            go("\"I'm short on the rent.\"", node="cover", mins=10,
               cond_=cond(wd(6), tod("07:30", "12:00"), trait("money", "lt", 75), flag("rent_starts"), flag("sunday_counted_today", False),
                          flag("ryan_covered", False), flag("ryan_cover_today", False), ntrait(R, "warmth", "gte", 40), trait("ryan_step", "gte", 0)),
               flags=[fset("ryan_covered"), fset("ryan_cover_today")],
               eff=[{"targetType": "player", "trait": "money", "op": "add", "value": 25, "clamp": False}, nadd(R, "warmth", 5)]),
            *RT_ROOM[1],
            # the hot repeatables in his room (1, 4, 5), evenings he's home
            *[c for n, label, gate, wardrobe, _m, _x in HOT_ROOM for c in hot_choice(n, label, gate + [wd(0, 1, 3, 6), tod("19:00", "22:00")], wardrobe)],
            go("Leave him to it.", loc="home_hall"),
        ]),
        *RT_ROOM[2],
        *[hot_node(n, label, media, exits) for n, label, gate, wardrobe, media, exits in HOT_ROOM],
        stink_node("home_hall"),
        node("talk", "Talk", [
            POOL(
                P("You sit on the end of his bed and he tells you about the yard, about a guy who dropped a pallet on his own foot. You laugh. He watches you laugh."),
                P("He asks about college. Not like Mom does. He wants to know who's annoying and who's cute, and he goes quiet when you tell him who's cute."),
                P("You lie across the foot of his bed and talk about nothing for half an hour, about Mark mostly, and how much you both want out of this house."),
            ),
            D(R, "You're all right, you know. For a sister."),
        ], [go("Go.", loc="home_hall", mins=5)]),
        node("cover", "Short", [
            P("He doesn't ask what you spent it on. He gets his wallet off the desk and counts out what he has and pushes it into your hand, and holds your hand a second too long."),
            D(R, "Don't tell Mark it came from me. He'll take it as a loan."),
            G(cond(wd(5)), T("It's not your money. Sunday it'll look like yours, but it won't count.")),
            G(cond(wd(6)), T("It's not your money. At the table it'll look like yours, but it won't count.")),
        ], [go("\"Thank you.\"", loc="home_hall", mins=5)]),
    ]})

# ── his everyday hubs (iteration 002, part 2): dinner in the kitchen, TV on weekend afternoons ──
# npc_ryan.md:94-107; home_life.md. Plain lines are the sheet's; the tease and touch screens are
# placeholders (LO, 2026-10-09). Raise: Warmth +1 plain, Want +1 a tease, once a day per item.
from home_items import *
RS = "sheets/people/npc_ryan.md"
L_ = "npc_laura"
M_ = "npc_mark"
RYAN_DRESS_LINES = [
    G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}),
      D(R, "You're wearing that downstairs?"), P("He doesn't look away from your ass when you turn.")),
    G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "worn_exposure", "operator": "eq", "value": 0}),
      P("He talks to your face, hard, and fails. Twice.")),
    G(cond({"type": "worn_type", "operator": "eq", "value": "cafe_uniform"}),
      D(R, "Huh. The uniform."), P("He takes his time looking at it.")),
]
K = "home_kitchen"
LOW_LOOK = P("His eyes drop to the towel and come back up.")
RT_KITCHEN = ryan_towel("hub_ryan_kitchen", K, LOW_LOOK)
kc, kn = item("dinner", "Sit down to dinner.", [tod("18:00", "19:00")], "ate_dinner", K,
    [P("He eats like he's late for something."), D(R, "Pass the bread, @player.nickname."),
     G(cond(here(L_, K)), P("Laura asks him about the yard and gets three words.")),
     G(cond(here(M_, K)), P("Mark reads the paper at the head of the table and doesn't look up."))],
    [energy(15), warm(R)], 30,
    tease={"label": "Find his foot under the table.", "ref": f"{RS}:106", "gate": [CURIOUS, trait("ryan_step", "gte", 3)],
           "eff": [energy(15), want(R)], "what": "Ryan, dinner: tease (Curious, Ryan A 4)"})
out.append({
    "id": "hub_ryan_kitchen", "name": "Ryan, at dinner",
    "description": "Ryan at the dinner hour in the kitchen (Mon, Tue, Thu, Sun 18:00-19:00, Q54): dinner with him (home_life). With Laura there, the tease is as far as it goes (npc_ryan.md:106).",
    "trigger": {"location": K, "npc": R, "requires_npc": R, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("opening_done"))},
    "nodes": [node("table", "Ryan, at dinner", [
        P("Ryan's at the table in a gym shirt, already on his second plate."),
        POOL(D(R, "Hey."), D(R, "Mom made the good potatoes. Sit."), D(R, "You look tired, @player.nickname.")),
        *RYAN_DRESS_LINES, *RT_KITCHEN[0],
    ], kc + RT_KITCHEN[1] + [go("Leave him to it.", loc="home_hall")]), *kn, *RT_KITCHEN[2]]})

LR = "home_living_room"
RT_LIVING = ryan_towel("hub_ryan_living_room", LR, LOW_LOOK)
lc, ln = item("tv", "Play his game with him.", [], "watched_tv", LR,
    [P("His game, your turn. You lose in under a minute."), D(R, "You're terrible, @player.nickname.")],
    [energy(5), warm(R)], 60)   # its tease and touch are hot repeatables 2 and 6 now (release 1)
fc, fn = item("film", "Watch a film with him.", [], "movie_night", LR,
    [P("He lets you pick and complains about it, but he watches the whole thing."), D(R, "Fine. That was good. Don't tell anyone.")],
    [energy(5), warm(R)], 120)
out.append({
    "id": "hub_ryan_living_room", "name": "Ryan, on the couch",
    "description": "Ryan on weekend afternoons in the living room (Sat, Sun 14:00-18:00, Q55): his game or a film with him (home_life).",
    "trigger": {"location": LR, "npc": R, "requires_npc": R, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("opening_done"))},
    "nodes": [node("couch", "Ryan, on the couch", [
        P("Ryan's sprawled on the couch with a controller, the TV loud, a bag of crisps open on his chest."),
        POOL(D(R, "Want next game?"), D(R, "Sit. You're blocking the screen."), D(R, "There's a film on after this if you want.")),
        *RYAN_DRESS_LINES, *RT_LIVING[0],
    ], lc + fc + RT_LIVING[1]
       + [c for n, label, gate, wardrobe, _m, _x in HOT_COUCH for c in hot_choice(n, label, gate + [LAURA_NOT_HERE(LR)], wardrobe)]
       + [go("Leave him to it.", loc="home_hall")]),
       *ln, *fn, *RT_LIVING[2],
       *[hot_node(n, label, media, exits) for n, label, gate, wardrobe, media, exits in HOT_COUCH], stink_node("home_living_room")]})

# ── Laura opens the door (ryan_laura_opens_the_door.md, signed 2026-11-01; moved from Laura's ladder, was laura_04):
#    the first Saturday afternoon on the couch with her feet in his lap while Laura is home, dressing upstairs. Once. ──
out.append({
    "id": "ryan_laura_opens_the_door", "name": "Laura comes in",
    "description": "After Ryan's step 4: Laura comes into the living room on Ella's feet in Ryan's lap. \"Mark doesn't need to hear about this.\" Sets laura_knows_ryan (she is the witness his step 8 names).",
    "trigger": {"location": LR, "npc": R, "requires_npc": R, "is_repeatable": False, "priority": 8, "is_active": True,
                "schedules": [{"weekdays": [5], "start_time": "17:00", "end_time": "18:00"}],
                "conditions": cond(trait("ryan_step", "gte", 4), flag("laura_knows_ryan", False),
                                   {"type": "npc_at_location", "location_id": "home_master_bedroom", "npc_id": "npc_laura", "operator": "is_present"})},
    "nodes": [
        node("couch", "The couch", [
            P("You're on the couch with your feet in Ryan's lap and his game on loud. His hand is round your ankle like it lives there."),
            P("The stairs creak. Laura comes in half dressed for tonight, an earring in her hand, and stops in the doorway. She looks at your feet. She looks at his hand. Ryan doesn't move it fast enough."),
        ], [go("Leave your feet where they are.", node="laura", mins=2)]),
        node("laura", "Mark doesn't need to hear", [
            P("You don't move them. Laura looks at you for a long second, and something in her face decides."),
            D("npc_laura", "Mark doesn't need to hear about this."),
            P("She goes back up to finish dressing. Ryan breathes out like he's been underwater."),
            T("Laura knows. And she's keeping it."),
        ], [go("\"Okay, Mom.\"", loc=LR, mins=5, flags=[fset("laura_knows_ryan")])]),
    ]})

# ── his bathroom window: "Ryan's in there." (weekday mornings, Laura's rule) ──
# In the towel at the door (DECISIONS 98): no lines (he can't see her through it), one knock-and-slip.
RT_BATH = towel_set("hub_ryan_bathroom", R, "want", 40, 70, "ryan_towel_today", [_want(R, 2), EXH1], "home_hall",
    slip=RYAN_TOWEL_SLIP, slip_label="Knock, and let the towel slip.",
    slip_lead=[P("You knock. The water stops, and the door opens a crack. Ryan looks out, wet, the steam behind him."), *RYAN_TOWEL_LEAD],
    slip_media=VID("a young woman in a bath towel letting it slip off her breasts at a steamy bathroom door, a young man looking out", "girl drops towel bathroom door guy", "towel slip bathroom door", pool_dir="sex/towel_ryan_door_slip_t4"))
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
        ], [*RT_BATH[1], go("Wait your turn.", loc="home_hall", mins=10), go("Leave.", loc="home_hall")]),
        *RT_BATH[2],
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
            go("Put it all back.", loc="home_hall", mins=15, cond_=cond(flag("ryan_things_found", False)), flags=[fset("ryan_things_found")]),
            go("Put it all back.", loc="home_hall", mins=15, cond_=cond(flag("ryan_things_found"))),
        ]),
    ]})

cards = step_cards(R, {
    1: ("Ryan, in the hall, on your first morning.", "Your first morning: out of the shower, the hall"),
    2: ("Ryan looks at you, then away too fast. He showers first on weekday mornings, and his phone is always on the sink.", "Go into the bathroom while Ryan showers, a weekday morning"),
    3: ("You know about Kayla. He knows you know. His secret has a price.", "Knock on Ryan's door on an evening he's home (Curious)"),
    4: ("Two knocks, and he opens. He leaves room on the bed.", "Two knocks on Ryan's door late at night, not Friday or Saturday (Curious)"),
    5: ("Kayla stays over on Fridays. Your bed is against his wall.", "Be in your bed on a Friday night (Curious)"),
    6: ("He heard you through the wall. Kayla's still in the house on Saturday morning.", "Take a shower on Saturday morning (Showing)"),
    7: ("Since the shower, you both know why you'd knock.", "Two knocks on Ryan's door on an evening he's home (Bold)"),
    8: ("His phone is face-down every time you knock now.", "Two knocks on Ryan's door late, Sunday to Thursday (Bold)"),
}, terminal_text=("Two knocks, late, Sunday to Thursday. His room, after ten.", "More of Ryan in the next release."),
   closed_text="He's your brother now, polite and cold. Nothing more.", skip=(1,))

text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · RYAN (sheets/scenes/ryan_0*.md, sheets/people/npc_ryan.md)\n"
        "# Steps 2-8 (Ryan A 3-9), his hubs, his things, the two-knocks repeat, his cards.\n"
        "# Step 1 is the opening (2_one_shots.toml). Explicit screens pasted as signed.\n"
        "# =============================================================================\n")
# Iteration 002, part 7: "Mom's gone to bed. Mark's downstairs." (was "asleep" until DECISIONS 83) holds only while they are (gate: a named person is where the line says)
require_present(out, "ryan_04_feet_in_his_lap", here_at("npc_laura", "home_master_bedroom"), here_at("npc_mark", "home_living_room"))
# Knocking clears her "coming" (phone.py ryan_two_knocks_text, DECISIONS 87).
for _c in out:
    if _c["id"] == "ryan_two_knocks":
        clear_on_leave(_c, "ryan_knock_booked")
text += "".join(emit(c) for c in out) + "".join(emit_card(c) for c in cards)
open(__import__("sys").argv[1], "w").write(text)
print("ryan:", len(out), "canvases,", len(cards), "cards")
