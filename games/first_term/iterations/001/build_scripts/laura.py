"""Laura — steps 1-8 (Laura C 1-8; step 5 = Jake B 4), her hubs, the catch, the curfew call.
Source: sheets/scenes/laura_0*.md, sheets/people/npc_laura.md. Explicit screens pasted as signed."""
from canv import *
from tomlw import tod, wd

L = "npc_laura"
J = "npc_jake"
out = []

def done(n):
    return fset(f"laura_0{n}_done")

def susp(n):
    return add("laura_suspicion", n)

CURFEW_SET = [fset("curfew")]
LATE_CLEAR = funset("came_home_late")
DRESS_ON = {"type": "clothing_item", "item_id": "laura_blue_dress", "operator": "equipped"}

# ── step 1 · Laura C 1 · the blue dress (fires in her room; the kitchen line is on her hub) ──
out.append({
    "id": "laura_01_blue_dress", "name": "The blue dress",
    "description": "Laura step 1 (Laura C 1), Tuesday evening, in the master bedroom (seen from the kitchen: her hub there says 'Come upstairs'). Adds and equips laura_blue_dress. Sets laura_01_done (her thread).",
    "trigger": step_trigger(L, 1, bind_npc=False),
    "nodes": [
        node("upstairs", "Her room", [
            P("Laura is right behind you on the stairs, still in her kitchen apron, drying her hands on it. She shuts her bedroom door and goes straight to the wardrobe and reaches into the back, past the work blouses, to something in dry-cleaner plastic."),
            D(L, "I was saving this. I don't know what for. Here. Try it."),
            P("It's a dress, blue, soft, short enough that she must have been very young when she wore it. She holds it against you and her eyes go somewhere far away."),
        ], [go("Try it on.", node="mirror", mins=10,
               wardrobe=[{"action": "add", "item_id": "laura_blue_dress"}, {"action": "equip", "item_id": "laura_blue_dress"}])]),
        node("mirror", "The mirror", [
            IMG("scenes/laura_01_mirror.jpg", "a mother behind her adult daughter in a long bedroom mirror, the daughter in a short tight blue dress, the mother's hands smoothing it at the hips",
                "mother behind daughter mirror blue dress", "woman fixing young woman's dress in bedroom mirror"),
            P("It's tight across your chest. It stops high on your thighs. In her long mirror you look like someone older, someone who goes out. Laura stands behind you and smooths the fabric down over your hips with both hands, slowly, and keeps her hands there a second longer than she needs to."),
            P("Her eyes in the mirror aren't on the dress. They're on you."),
            T("She's looking at you like a stranger would. You don't hate it."),
        ], [
            go("\"Is that bad?\"", node="no", mins=3),
            go("\"I can't take this.\"", node="give", mins=3),
        ]),
        node("no", "It never fit me like that", [
            ME("Is that bad?"),
            D(L, "It never fit me like that."),
            P("She says it quietly, to the mirror. Then she laughs, too bright, and takes her hands off you."),
            D(L, "No. No, sweetheart. It's not bad."),
        ], [go("\"Thank you, Mom.\"", loc="home_ella_room", mins=5, consumes=True,
               eff=[nadd(L, "want", 10), add("exhibitionism", 3), setv("laura_step", 1)], flags=[done(1)])]),
        node("give", "Keep it", [
            ME("I can't take this. It's yours."),
            D(L, "Keep it. Wear it somewhere."),
            P("She won't take it back. She folds your hands round the hanger and holds them there, and her thumb strokes the back of your wrist."),
            D(L, "Somebody should look at you in it."),
        ], [go("\"Okay.\"", loc="home_ella_room", mins=5, consumes=True,
               eff=[nadd(L, "want", 10), nadd(L, "warmth", 3), add("exhibitionism", 3), setv("laura_step", 1)], flags=[done(1)])]),
    ]})

# ── step 2 · Laura C 2 · home late: the first catch ──
LOW_WARMTH = cond(ntrait(L, "warmth", "lt", 40), trait("laura_suspicion", "gte", 50), logic="OR")
HIGH_WARMTH = cond(ntrait(L, "warmth", "gte", 40), trait("laura_suspicion", "lt", 50))
out.append({
    "id": "laura_02_home_late", "name": "Home late",
    "description": "Laura step 2 (Laura C 2): the first catch on the dark stairs. Low Warmth (or suspicion 50+): the curfew. High: \"Did anyone look at you in it?\"",
    "trigger": step_trigger(L, 2),
    "nodes": [
        node("stairs", "The dark stairs", [
            P("You've got your shoes in your hand and you're halfway to the stairs when the lamp on the landing clicks on. Laura is sitting on the third step from the top in her robe, arms round her knees. She's been there a while."),
            G(cond(trait("laura_suspicion", "lt", 30)), D(L, "Where were you?")),
            G(cond(trait("laura_suspicion", "gte", 30)),
              P("She comes down to you without a word and takes your chin in her hand and turns your face to the lamp. She smells your hair. She looks you up and down, slowly, like she's reading it off you."),
              D(L, "Smoke. Somebody's cologne. Where were you?")),
            G(cond(DRESS_ON), P("Her eyes stop on the blue dress. Her dress. She doesn't say anything about it, but she looks at it for a long time.")),
        ], [
            go("Wait for it.", node="low", mins=2, cond_=LOW_WARMTH, eff=[susp(5)]),
            go("Wait for it.", node="high", mins=2, cond_=HIGH_WARMTH, eff=[susp(5)]),
        ]),
        node("low", "Grounded", [
            D(L, "You're grounded. A week. No parties, no late shifts, no boys at the door. I mean it, @player."),
            P("Her voice shakes. She's angry and she's scared, and you can't tell which is winning."),
            T("A week. She means every second of it."),
        ], [
            go("\"Fine.\"", loc="home_ella_room", mins=3, retry=1, flags=CURFEW_SET + [LATE_CLEAR], eff=CURFEW_EFF),
            go("\"I was at Zoe's.\" (she'll know)", node="lie", mins=2),
        ]),
        node("lie", "She knows", [
            P("Her mouth goes thin. She knows where Zoe's is and she knows what time it is and she knows when you're lying, and she's always known."),
            D(L, "Bed. Now."),
        ], [go("\"Goodnight, Mom.\"", loc="home_ella_room", mins=3, retry=1,
               eff=[nadd(L, "warmth", -5), susp(5)] + CURFEW_EFF, flags=CURFEW_SET + [LATE_CLEAR])]),
        node("high", "Did anyone look", [
            P("She doesn't shout. She pats the step beside her, and you sit, and she looks at you sideways in the lamplight like she did in her mirror."),
            D(L, "I'm not angry. I was nineteen once. Just— did you have fun?"),
            ME("Yeah."),
            G(cond(DRESS_ON), D(L, "Did anyone look at you in it?")),
            G(cond({"type": "clothing_item", "item_id": "laura_blue_dress", "operator": "unequipped"}), D(L, "Did anyone look at you?")),
        ], [go("\"Everyone.\"", loc="home_ella_room", mins=5, consumes=True,
               eff=[nadd(L, "want", 10), setv("laura_step", 2)], flags=[done(2), LATE_CLEAR])]),
    ]})

# ── step 3 · Laura C 3 · wine in the kitchen ──
out.append({
    "id": "laura_03_wine_in_the_kitchen", "name": "Wine in the kitchen",
    "description": "Laura step 3 (Laura C 3): her secret, and Mark hasn't looked at her like that since the wedding.",
    "trigger": step_trigger(L, 3),
    "nodes": [
        node("glass", "Sit with me", [
            P("The kitchen's dark except the light over the stove. Laura's at the table with a bottle of white and two glasses, one of them already poured. Her robe is open at the collar. She's been waiting for somebody, and it wasn't Mark."),
            D(L, "Sit with me. Just for a bit."),
        ], [
            go("\"Pour me one.\"", node="story", mins=10),
            go("\"I'm tired, Mom.\"", node="no", mins=2),
        ]),
        node("story", "Her mother's dress", [
            P("She pours, and you clink, and she drinks half of hers like it's water. Then she tells you, out of nowhere, staring at the stove."),
            D(L, "When I was nineteen I used to climb out of my window in my mother's dress. Red one. Backless. She never knew. I'd come home at four with my shoes in my hand and sit on the stairs so the stairs wouldn't creak."),
            P("She laughs into her glass."),
            D(L, "I used to get looked at, sweetheart. Like you get looked at."),
        ], [go("\"Mom!\"", node="mark", mins=10)]),
        node("mark", "Since the wedding", [
            D(L, "Don't \"Mom\" me. I had a body."),
            P("She tips the glass at you, smiling, and then the smile goes."),
            D(L, "Mark hasn't looked at my body like that since the wedding."),
            P("She says it to the wine. Then she looks at you, at your mouth, at your throat, and away, fast."),
            T("She wants somebody to look at her. She's telling you."),
        ], [go("\"He should.\"", loc="home_hall", mins=5, consumes=True,
               eff=[nadd(L, "want", 10), setv("laura_step", 3)], flags=[done(3)])]),
        no_node("no", [P("She nods and pours the second glass back into the bottle, carefully, so none spills."), D(L, "Go on, then. Bed."), P("She drinks the rest of hers alone, looking at the stove.")],
                "home_hall", 2, eff=[nadd(L, "warmth", -1)]),
    ]})

# ── step 4 · Laura C 4 · Ryan's door ──
out.append({
    "id": "laura_04_ryans_door", "name": "Ryan's door",
    "description": "Laura step 4 (Laura C 4), in Ryan's room (seen from the kitchen): Laura opens the door on her feet in his lap, and keeps the secret. Reads ryan_step >= 4.",
    "trigger": dict(step_trigger(L, 4, bind_npc=False), npc="npc_ryan", requires_npc="npc_ryan", priority=9),
    "nodes": [
        node("door", "The door opens", [
            P("You're on Ryan's bed with your bare feet in his lap, the way it is now, and his hand is wrapped round your calf. The game's on with the sound off. Neither of you is watching it."),
            P("The door opens without a knock. Laura, with a basket of folded laundry. She stops. She looks at your feet. She looks at his hand on your leg. Ryan doesn't move it fast enough."),
            D(L, "@player. My room. Now, please."),
        ], [go("\"Mom—\"", node="room", mins=3)]),
        node("room", "Her room", [
            P("She doesn't sit across from you. She sits right beside you on the end of her bed, so close her knee is against yours, and she looks at your bare feet, and then at your face."),
            D(L, "What was that?"),
            T("She isn't shouting. She's asking like she wants the real answer."),
        ], [
            go("\"Then don't tell him.\"", node="secret", mins=5),
            go("\"It's nothing.\" (she'll know)", node="lie", mins=3),
        ]),
        node("secret", "A secret", [
            P("Laura breathes out. She puts her hand on your knee and squeezes, once."),
            D(L, "Mark doesn't need to hear about this."),
            P("It's not a warning. It's a promise. It's the first secret you've ever had with her, and she's the one who made it."),
        ], [go("\"Goodnight, Mom.\"", loc="home_ella_room", mins=3, consumes=True,
               eff=[nadd(L, "want", 10), setv("laura_step", 4)], flags=[done(4), fset("laura_saw_ryan")])]),
        node("lie", "Don't", [
            D(L, "Don't. Don't do that."),
            P("She gets up and leaves you sitting on her bed, and she doesn't take the secret with her."),
        ], [go("Go to your room.", loc="home_ella_room", mins=3, retry=2,
               eff=[nadd(L, "warmth", -5), susp(5)])]),
    ]})

# ── step 5 · Laura C 5 = Jake B 4 · Jake at the door (one canvas, both counters) ──
out.append({
    "id": "laura_05_jake_at_the_door", "name": "Jake at the door",
    "description": "Laura step 5 = Jake step 4 (one canvas, it sets both counters). Saturday night after a date: the goodnight kiss at the front door, Laura watching from the dark living room.",
    "trigger": dict(step_trigger(L, 5, bind_npc=False), npc=J, requires_npc=J),
    "nodes": [
        node("porch", "The doorstep", [
            P("Jake walks you up the path with his hand low on your back. The porch light is off. The living-room window is dark, but not empty: there's a shape on the couch behind the glass, sitting very still."),
            D(J, "Everyone was looking at you tonight."),
            G(cond(DRESS_ON), D(J, "In that dress? I couldn't eat.")),
            D(J, "Is your mom up?"),
            T("She is. She's watching. He doesn't know."),
        ], [
            go("\"Kiss me.\"", node="kiss", mins=3),
            go("\"Goodnight, Jake.\"", node="no", mins=3),
        ]),
        node("kiss", "Higher", [
            G(cond(DRESS_ON),
              P("Jake kisses you on the doorstep, hard, with his mouth open. His hands slide down your back and under the hem of your mother's dress. They close on your ass and pull your hips into his. His cock is hard behind his jeans, pressed right against you. Your tits flatten on his chest. \"Everyone was looking at you tonight,\" he says into your mouth. You turn him slowly, until the dark living-room window can see you both. In the glass, Laura's shape stands still, her hand at her own throat. \"Higher,\" you tell him. \"Don't stop.\" His hands squeeze higher on your ass, and his cock grinds into your hips.")),
            G(cond({"type": "clothing_item", "item_id": "laura_blue_dress", "operator": "unequipped"}),
              P("Jake kisses you on the doorstep, hard, with his mouth open. His hands slide down your back and close on your ass and pull your hips into his. His cock is hard behind his jeans, pressed right against you. Your tits flatten on his chest. \"Everyone was looking at you tonight,\" he says into your mouth. You turn him slowly, until the dark living-room window can see you both. In the glass, Laura's shape stands still, her hand at her own throat. \"Higher,\" you tell him. \"Don't stop.\" His hands squeeze higher on your ass, and his cock grinds into your hips.")),
            VID("a couple kissing hard on a dark front doorstep, his hands squeezing her ass, a figure watching from a dark window", "couple kissing doorstep night hands on ass", "goodnight kiss front door grinding hands under dress", file="sex/laura_05_doorstep_t4.webm"),
        ], [go("\"Higher. Don't stop.\"", node="couch", mins=10, flags=[funset("jake_date_booked")])]),
        node("couch", "Was he any good", [
            P("Jake goes down the path walking like a man who won something. You let yourself in. The living room is dark. Laura is on the couch with her knees pulled up and her hand still at her throat, and she doesn't pretend she wasn't watching."),
            D(L, "Was he any good?"),
            G(cond(DRESS_ON), ME("Better in your dress.")),
            G(cond({"type": "clothing_item", "item_id": "laura_blue_dress", "operator": "unequipped"}), ME("Better with you watching.")),
            P("She makes a sound in her throat. She doesn't get up."),
        ], [go("Go up to bed.", loc="home_hall", mins=5, consumes=True,
               eff=[nadd(L, "want", 10), setv("laura_step", 5), setv("jake_step", 4)],
               flags=[done(5), fset("jake_04_done")])]),
        no_node("no", [P("You kiss his cheek and step back. Jake shrugs, grinning, and walks backwards down the path."), D(J, "Next Saturday, then."), P("In the dark window the shape on the couch hasn't moved. When you let yourself in, Laura's already gone up.")],
                "home_front_door", 7, eff=[nadd(L, "want", 2)], flags=[funset("jake_date_booked")]),
    ]})

# ── step 6 · Laura C 6 · take me with you ──
out.append({
    "id": "laura_06_take_me_with_you", "name": "Zip me up",
    "description": "Laura step 6 (Laura C 6), Saturday early evening, Laura dressing: \"Take me with you one night.\" Sets laura_asked_to_come.",
    "trigger": step_trigger(L, 6),
    "nodes": [
        node("zip", "Zip me up", [
            P("Her bedroom door is open. It's always open now when she dresses. Laura is in front of the long mirror in a dress you've never seen, holding it to her chest, the zip open all the way down to the small of her back."),
            D(L, "Zip me up, sweetheart? Mark's useless at it."),
        ], [
            go("\"Hold still.\"", node="lean", mins=3),
            go("\"Ask Mark.\"", node="no", mins=2),
        ]),
        node("lean", "Her back", [
            P("You take the zip in your fingers and pull it up slowly, and your knuckles slide up her bare back the whole way, over her spine, between her shoulder blades. Her skin is warm. She breathes in. When it's done she doesn't step away. She leans back into your hands, and your fingers end up on her ribs, and she covers them with her own."),
            P("In the mirror her cheeks are pink."),
        ], [go("Don't move.", node="ask", mins=3)]),
        node("ask", "Take me with you", [
            D(L, "Take me with you one night. To one of Zoe's. I want to see what you do."),
            ME("Wear something short."),
            P("She laughs, startled, and then she doesn't laugh, and she looks at you in the mirror like she's already picking the dress."),
        ], [go("\"Friday.\"", loc="home_hall", mins=3, consumes=True,
               eff=[nadd(L, "want", 10), setv("laura_step", 6)], flags=[done(6), fset("laura_asked_to_come")])]),
        no_node("no", [D(L, "Mark. Right."), P("She reaches round and does the zip herself, badly, halfway, and leaves it there. She doesn't ask you again tonight.")],
                "home_hall", 7, eff=[nadd(L, "warmth", -1)]),
    ]})

# ── step 7 · Laura C 7 · the dark stairs (the voice sample; every screen as signed) ──
PARTY_TO_2AM = [(("18:00", "19:00"), 465), (("19:00", "20:00"), 405), (("20:00", "21:00"), 345)]
out.append({
    "id": "laura_07_dark_stairs", "name": "The dark stairs",
    "description": "Laura step 7 (Laura C 7), the voice sample: Friday, Laura comes to Zoe's party; the kiss on the dark stairs, and Ryan sees. The party screen moves the clock past 02:00.",
    "trigger": step_trigger(L, 7, retry_days=7),
    "nodes": [
        node("kitchen", "Short enough", [
            P("Laura is leaning on the kitchen counter in a black dress that stops high on her thighs. Her wine glass is already half empty. Mark's radio plays out in the garage. \"You told me short,\" she says. \"Is this short enough, sweetheart?\" She turns for you, slow, and the neckline shows the tops of her tits. Then she just looks at you, too long. Her cheeks go pink, but she doesn't look away. \"Zoe's party. Take me with you tonight. Please.\" You feel it low in your stomach. She dressed for you, not for him. She sets the glass down and waits for your answer."),
        ], [
            go("\"Come on, then.\"", node="party", mins=15),
            go("\"Not tonight, Mom.\"", node="no", mins=2),
        ]),
        node("party", "Zoe's", [
            P("Zoe's apartment is loud, and nobody here knows the woman in the short dress is your mom. Laura drinks her wine too fast. She laughs too loud at a guy's joke, and two others stare at her chest. She likes it. She lets you see it. But her eyes keep finding you across the room. When you dance, her hand settles on your waist and stays too long. \"Sweetheart,\" she says against your ear, \"look at you tonight.\" Zoe grabs your arm, grinning. \"Babe. Your mom.\" *She wants you. She isn't hiding it.* When the party thins out, Laura takes your hand and won't let go. You walk home in the dark, her fingers laced in yours."),
        ], [go("Take her home.", node="stairs", mins=m, cond_=cond(tod(a, b)), flags=[fset("party_went")]) for (a, b), m in PARTY_TO_2AM]),
        node("stairs", "Halfway up", [
            P("Halfway up the stairs, Laura stops and turns. Before you can ask, she kisses you. Her mouth is warm and open, and you taste the wine on her tongue. Her hand lands flat on your chest. Then it slides, slow, until her palm covers your tit. Her thumb finds your nipple through the fabric and circles it until it goes hard. You gasp into her mouth, so she pushes your back into the wall. The plaster is cold, but she is hot all down your front. You kiss her back, hungry, your tongue chasing hers. \"Sweetheart,\" she breathes against your lips. Her hips press into yours and pin you there. Her thumb keeps rolling your nipple, and her breath goes ragged in your mouth."),
            VID("two women kissing on dark stairs, the older pinning the younger to the wall, her hand on her breast", "two women kissing on stairs at night hand on breast", "woman pins woman to wall kissing dark staircase", file="sex/laura_07_stairs_t4.webm"),
        ], [go("Kiss her back.", node="door", mins=3, eff=[add("corruption", 3), nadd(L, "want", 10)])]),
        node("door", "Ryan's door", [
            P("Laura's mouth is on yours, slow and wet, and her hand is full of your tit. She squeezes, and you moan into the kiss. Then Ryan's door opens at the top of the stairs. His light drops over you both. He stares. Laura doesn't let go. Her thumb keeps circling your nipple. \"Go to bed, Ryan.\" You look straight up at him. Then you pull your mother back into the kiss. \"Don't stop for him.\" He doesn't move. Laura's lips slide down to your neck and suck just under your jaw. Your nipples are hard against her, and she pinches one until you gasp. Up in the doorway, Ryan's hand is white on the frame and his cock is tenting his shorts."),
            VID("on dark stairs two women kissing, the younger looks up at a young man in a lit doorway above, his erection visible in his shorts", "women kissing on stairs man watching from doorway", "caught kissing on stairs brother watching hard", file="sex/laura_07_door_t4.webm"),
        ], [go("Let her stop.", node="after", mins=3, flags=[fset("laura_ryan_saw_kiss")])]),
        node("after", "Nothing", [
            P("Laura pulls back on the stairs. Her lipstick is smeared, and she is breathing hard. She looks at Ryan in his doorway, then at you. She says nothing. She goes up past him to her bedroom, and her door clicks shut beside Mark's snoring. \"@player.nickname,\" Ryan says, low. \"What was that?\" You don't answer him either. *You kissed your mother. You want her to do it again.* In the morning she'll be in the kitchen at breakfast. But a kitchen has nowhere to hide, and she'll have to look at you."),
        ], [go("Go to bed.", loc="home_ella_room", mins=5, consumes=True,
               eff=[setv("laura_step", 7)], flags=[done(7)])]),
        no_node("no", [P("Laura's face falls, and then she laughs at herself, too brightly, and takes her earrings out one at a time."), D(L, "Of course not. What was I thinking. Go, have fun."), P("When you leave she's still standing at the counter in the black dress, finishing the wine.")],
                "home_kitchen", 7, eff=[nadd(L, "warmth", -2)]),
    ]})

# ── step 8 · Laura C 8 · it wasn't the wine ──
HUNGRY = trait("corruption", "gte", 60)
out.append({
    "id": "laura_08_it_wasnt_the_wine", "name": "It wasn't the wine",
    "description": "Laura step 8 (Laura C 8), the next weekday breakfast: they name the kiss; \"I'm your mother.\" Her last step in 0.1.",
    "trigger": step_trigger(L, 8),
    "nodes": [
        node("coffee", "Breakfast", [
            P("Laura is at the counter with her back to you, making coffee she doesn't need, in her work blouse with the top button done up for once. She doesn't turn round when you come in. She can't."),
            D(L, "That was the wine. On the stairs. That was the wine."),
        ], [
            go("\"It wasn't the wine.\"", node="mother", mins=3),
            go("\"It was the wine.\"", loc="home_hall", mins=2, retry=1),
        ]),
        node("mother", "I'm your mother", [
            P("Her hand shakes on the cup and coffee slops over the rim onto her fingers. She doesn't wipe it off."),
            D(L, "I'm your mother."),
            P("She says it like it's a door she's holding shut with her whole body. She still won't look at you. But she isn't saying no, either."),
            T("She didn't say it was wrong. She said who she is."),
        ], [
            go("\"Okay. For now.\"", loc="home_hall", mins=5, consumes=True,
               eff=[nadd(L, "want", 10), setv("laura_step", 8)], flags=[done(8)]),
            go("\"You're my mom. That's all you get to be.\" (ends her path)", node="final", mins=3),
        ]),
        node("final", "That's all", [
            ME("You're my mom. That's all you get to be."),
            P("Laura turns round at last. Her face closes, neat and polite, like a door with a good lock."),
            D(L, "Good. Then go to class, @player."),
            P("From now on, when she catches you, she punishes you. Nothing else."),
        ], [go("Go. (ends her path)", loc="home_hall", mins=3, final=True,
               eff=[setv("laura_step", -1, clamp=False)], flags=[fset("laura_08_it_wasnt_the_wine_closed")])]),
    ]})

# ── her catches: the stairs when she comes home late (the repeat; laura_08 sheet) ──
CAUGHT_LOW = LOW_WARMTH
out.append({
    "id": "laura_catch", "name": "Mom, on the stairs",
    "description": "Laura's catch, the repeat: on the dark stairs when she comes home late. Reads her Warmth, her Want and laura_suspicion. Home late +5; a lie +5. The curfew at low Warmth or suspicion 50+.",
    "trigger": {"location": "home_hall", "npc": L, "requires_npc": L, "is_repeatable": True,
                "priority": 7, "is_active": True,
                "conditions": cond(flag("came_home_late"), flag("opening_done"), flag("laura_caught_today", False))},
    "nodes": [
        node("stairs", "On the stairs", [
            P("The landing lamp clicks on. Laura is on the stairs in her robe, waiting, the way she waits now."),
            G(cond(trait("laura_suspicion", "lt", 30)), D(L, "Where were you?")),
            G(cond(trait("laura_suspicion", "gte", 30)),
              P("She comes down and checks you over without asking: your face, your mouth, your hair. She smells it."),
              D(L, "Tell me where you were. Don't lie to me.")),
            G(cond(DRESS_ON), P("She looks at her dress on you for a long time.")),
            G(cond(trait("laura_step", "lt", 0)), D(L, "Grounded. Don't argue.")),
            G(cond(trait("laura_step", "gte", 2), ntrait(L, "want", "gte", 50)),
              D(L, "Sit down. Tell me everything. All of it, sweetheart."),
              P("She pats the step beside her. Her knee is bare where the robe has fallen open, and she doesn't fix it.")),
        ], [
            go("Tell her the truth.", node="truth", mins=10, cond_=HIGH_WARMTH, eff=[susp(5), nadd(L, "warmth", 2)]),
            go("Lie. (she'll know)", node="lied", mins=5, eff=[susp(10), nadd(L, "warmth", -5)]),
            go("Take what's coming.", node="grounded", mins=5, cond_=CAUGHT_LOW, eff=[susp(5)]),
            go("Kiss her goodnight.", node="wall", swl=True, cond_=cond(HUNGRY, trait("laura_step", "gte", 8))),
        ]),
        node("truth", "Everything", [
            POOL(
                P("You sit on the stair below hers and tell her: the party, the music, the guy who wouldn't stop looking. She listens with her chin on her knees. When you get to the part where he touched your waist, she stops breathing."),
                P("You tell her who was there and what they drank and who left with who. She laughs in the right places. Then she asks what you were wearing, and listens to the answer like it matters."),
            ),
            D(L, "Go to bed. Before I ask you anything else."),
        ], [go("\"Goodnight, Mom.\"", loc="home_ella_room", mins=3, flags=[LATE_CLEAR, fset("laura_caught_today")])]),
        node("lied", "She knows", [
            P("She lets you finish the lie. Then she just looks at you until you stop talking."),
            D(L, "You think I don't know that face? I invented that face."),
        ], [go("Go to bed.", loc="home_ella_room", mins=3, flags=[LATE_CLEAR, fset("laura_caught_today")])]),
        node("grounded", "Grounded", [
            D(L, "That's it. A week. No parties, no late shifts, no dates. You live in this house, you keep its hours."),
            T("A week. She means every second of it."),
        ], [go("\"Fine.\"", loc="home_ella_room", mins=3, flags=CURFEW_SET + [LATE_CLEAR, fset("laura_caught_today")], eff=CURFEW_EFF)]),
        node("wall", "Further", [
            P("You lean down and kiss her, there on the stairs, and her hand comes up into your hair."),
            P("What happens next with Laura is in the next release of First Term."),
        ], [go("Go to bed.", loc="home_ella_room", mins=5, flags=[LATE_CLEAR, fset("laura_caught_today")])]),
    ]})

# ── her kitchen: breakfast and evenings (her hub). Tuesday before step 1: "Come upstairs." ──
out.append({
    "id": "hub_laura_kitchen", "name": "Laura",
    "description": "Laura's hub in the kitchen. Warmth +2 a talk (once a day). Reads her clothes lines, her ladder's leaks, the start choice (at dinner), hygiene.",
    "trigger": {"location": "home_kitchen", "npc": L, "requires_npc": L, "is_repeatable": True,
                "priority": 6, "is_active": True, "conditions": cond(flag("opening_done"))},
    "nodes": [
        node("kitchen", "The kitchen", [
            G(cond(tod("06:30", "08:00")),
              P("Laura is in her work blouse, buttering toast with one hand and holding her coffee with the other."),
              POOL(D(L, "Eat something, sweetheart. You're not going to class on nothing."),
                   D(L, "Morning. Is that what you're wearing?"),
                   D(L, "Your hair looks nice like that."))),
            G(cond(tod("18:00", "22:00")),
              P("Laura's at the stove with the radio on and a glass of white by the chopping board."),
              POOL(D(L, "Dinner in ten. Set the table?"),
                   D(L, "Sit. Tell me about your day."),
                   D(L, "Pour me another, would you? Don't tell Mark."))),
            G(cond(tod("18:00", "22:00"), flag("college_for_grades")), D(L, "How are the grades? You said grades. I'm holding you to it.")),
            G(cond(tod("18:00", "22:00"), flag("college_for_fun")), D(L, "Having fun yet? You said fun. Don't have too much.")),
            G(cond(tod("18:00", "22:00"), flag("college_for_freedom")), D(L, "Freedom, you said. You still live in my house, you know.")),
            G(cond(wd(1), tod("18:00", "22:00"), trait("laura_step", "eq", 0)),
              P("She dries her hands on her apron and looks at you with a funny little smile."),
              D(L, "Come upstairs after. I have something for you.")),
            G(cond(trait("laura_step", "gte", 1), trait("laura_step", "lt", 3)), P("Her eyes go to you when you come in, and stay a second too long. She keeps a second glass on the counter now.")),
            G(cond(trait("laura_step", "eq", 3)), D(L, "How's Ryan? You two seem close lately.")),
            G(cond(trait("laura_step", "eq", 4), flag("jake_met")), D(L, "Is Jake bringing you home on Saturday?")),
            G(cond(trait("laura_step", "eq", 5)), P("Her bedroom door was open again when you came down. She's started leaving it open when she dresses.")),
            G(cond(trait("laura_step", "eq", 6)), D(L, "Wear something short, you said.")),
            G(cond(trait("laura_step", "eq", 7)), P("She can't meet your eyes. Her hand isn't steady on the cup.")),
            G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), D(L, "Is that for college or for a guy?")),
            G(cond(DRESS_ON), D(L, "It never fit me like that."), P("Her hand smooths the hip of it without thinking.")),
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "worn_exposure", "operator": "eq", "value": 0}),
              P("Her eyes stop on your chest. Then she pours the coffee.")),
            G(cond({"type": "worn_type", "operator": "eq", "value": "towel"}), D(L, "Hall's cold, sweetheart. Don't stand there.")),
            G(cond(trait("hygiene", "lt", 30), flag("hygiene_off", False)), D(L, "Sweetheart. Shower. Today.")),
            G(cond(ntrait(L, "warmth", "lt", 30)), P("She's short with you. Everything you do lands wrong with her lately.")),
            G(cond(ntrait(L, "warmth", "gte", 70)), P("She touches your hair when she passes. She's on your side, whatever you've done.")),
        ], [
            go("Talk to her.", node="talk", mins=20, cond_=cond(flag("laura_talk_today", False)),
               flags=[fset("laura_talk_today")],
               eff=[{"targetType": "npc", "npcId": L, "trait": "warmth", "op": "add", "value": 2, "cap": 100}]),
            go("Follow her upstairs.", loc="home_master_bedroom", mins=2,
               cond_=cond(wd(1), tod("18:00", "22:00"), trait("laura_step", "eq", 0))),
            go("Leave her to it.", loc="home_kitchen"),
        ]),
        node("talk", "Talk", [
            POOL(
                P("You sit on the counter and talk while she cooks. She asks about your classes, and you tell her the boring half."),
                P("She tells you about her office, the man who steals her yoghurt, the boss who calls her 'kiddo'. You make her laugh until she has to put the knife down."),
                P("You help her with the dishes, side by side, hips bumping. She hums. For ten minutes it's just the two of you and it's easy."),
            ),
            G(cond(trait("hygiene", "lt", 30), flag("hygiene_off", False)),
              P("Halfway through she wrinkles her nose and steps back, and the easy goes out of it.")),
        ], [go("Go.", loc="home_kitchen", mins=5)]),
    ]})

# ── waiting up on Saturday nights, in the dark living room ──
out.append({
    "id": "hub_laura_living_room", "name": "Laura, waiting up",
    "description": "Laura waiting up in the dark living room on Saturday nights; she can see the front door.",
    "trigger": {"location": "home_living_room", "npc": L, "requires_npc": L, "is_repeatable": True,
                "priority": 6, "is_active": True, "conditions": cond(flag("opening_done"))},
    "nodes": [
        node("dark", "The dark living room", [
            P("The lights are off. Laura is on the couch with her knees pulled up under her robe and a glass of wine she isn't drinking. From here she can see the front door and the path outside it."),
            POOL(D(L, "I'm not waiting up. I just couldn't sleep."),
                 D(L, "Come and sit with me. It's nice in the dark."),
                 D(L, "Who's bringing you home tonight?")),
            G(cond(trait("laura_step", "gte", 5)), D(L, "I saw you, you know. On the step. I didn't look away.")),
        ], [go("Sit with her a while.", loc="home_living_room", mins=30), go("Leave her be.", loc="home_living_room")]),
    ]})

# ── dressing on Saturday evenings, door open ──
out.append({
    "id": "hub_laura_bedroom", "name": "Laura, dressing",
    "description": "Laura dressing to go out on Saturday evening, her door open.",
    "trigger": {"location": "home_master_bedroom", "npc": L, "requires_npc": L, "is_repeatable": True,
                "priority": 6, "is_active": True,
                "conditions": cond(flag("opening_done"), tod("17:00", "18:30"))},
    "nodes": [
        node("mirror", "Her mirror", [
            P("Laura is at her long mirror in her slip, holding two dresses up one after the other."),
            POOL(D(L, "Black or green? Mark won't notice either way."),
                 D(L, "Do I look old in this? Be honest. No, don't be honest."),
                 D(L, "Hand me those earrings, sweetheart.")),
            G(cond(trait("laura_step", "gte", 6)), P("She leaves the zip undone and turns her back to you without asking. She knows you'll do it.")),
            G(cond(trait("laura_step", "lt", 6)), P("She catches you watching her in the mirror, and holds it."), D(L, "One of these nights I'm coming out with you. Don't think I won't.")),
        ], [go("Help her choose.", loc="home_master_bedroom", mins=20), go("Leave her to it.", loc="home_hall")]),
    ]})

# ── her curfew call (the person sheet: a call per curfew; missed costs suspicion +2) ──
out.append({
    "id": "laura_curfew_call", "name": "Mom, on the phone",
    "description": "Laura's call when she is under curfew, late at night. Played by answering the call (8_phone.toml); returns her to her room.",
    "trigger": {"location": "home_ella_room", "is_repeatable": True, "priority": 1, "is_active": True, "substitution_only": True},
    "nodes": [
        node("call", "Mom", [
            D(L, "Where are you? Don't lie to me, @player. You're grounded."),
            ME("I'm home, Mom. I'm in my room."),
            D(L, "Then open your door. I'm coming to look."),
            P("A minute later her shadow is under your door. She opens it, sees you, and stands there in the hall light looking at you for longer than she has to before she says goodnight."),
            D(L, "Next time you're not where you say you are, I'll come and find you. Wherever it is."),
        ], [go("\"Goodnight, Mom.\"", loc="home_ella_room", mins=5)]),
    ]})

cards = step_cards(L, {
    1: ("Laura has a dress for you upstairs. She said so on Tuesday.", "Tuesday evening: find Laura in the kitchen, then go up to her room"),
    2: ("She looked at you in that dress too long. She waits up now.", "Come home late, after ten at night (Daring)"),
    3: ("She keeps a second glass poured in the evenings.", "Find Laura in the kitchen late in the evening (Curious, Daring)"),
    4: ("She asks about Ryan, lightly, like it's nothing.", "An evening in Ryan's room with your feet in his lap (Curious, Daring)"),
    5: ("\"Is Jake bringing you home?\" She'll be waiting up.", "Saturday night: a date with Jake ends at the front door (Bold, Showing)"),
    6: ("She leaves her door open now, while she dresses.", "Saturday early evening: Laura's room, while she dresses (Bold, Showing)"),
    7: ("\"Wear something short,\" you told her. It's Friday.", "Friday evening in the kitchen: take Laura to Zoe's party (Bold, Showing)"),
    8: ("She'll be at breakfast. She'll have to look at you.", "A weekday breakfast in the kitchen (Bold, Showing)"),
}, terminal_text=("Her catches go on: home late, the stairs, \"tell me everything.\"", "Laura's next step comes in the next release."),
   closed_text="She's your mom. That's all she is now, and she punishes every catch.")
for c in cards:
    if "when" in c and not any(w.get("flag") == "opening_done" for w in c["when"]):
        c["when"].append({"flag": "opening_done", "op": "is_true"})

text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · LAURA (sheets/scenes/laura_0*.md, sheets/people/npc_laura.md)\n"
        "# Steps 1-8 (step 5 is also Jake's step 4), the catch, her hubs, the curfew call, her cards.\n"
        "# =============================================================================\n")
text += "".join(emit(c) for c in out) + "".join(emit_card(c) for c in cards)
open(__import__("sys").argv[1], "w").write(text)
print("laura:", len(out), "canvases,", len(cards), "cards")
