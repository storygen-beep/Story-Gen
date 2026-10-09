"""Laura — steps 1-8 (Laura C 1-8; step 5 = Jake B 4), her hubs, the catch, the curfew call.
Source: sheets/scenes/laura_0*.md, sheets/people/npc_laura.md. Explicit screens pasted as signed."""
from canv import *
from tomlw import tod, wd
M = "npc_mark"
R = "npc_ryan"

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
_t1 = step_trigger(L, 1, bind_npc=False)
_t1["conditions"]["items"] += [flag("laura_dress_invite"),
                               {"type": "hours_since_flag", "subject": "player", "flag_key": "laura_dress_invite", "operator": "lt", "value": 1}]
out.append({
    "id": "laura_01_blue_dress", "name": "The blue dress",
    "description": "Laura step 1 (Laura C 1), Tuesday evening, in the master bedroom (seen from the kitchen: her hub there says 'Come upstairs'). Adds and equips laura_blue_dress. Sets laura_01_done (her thread).",
    "trigger": _t1,
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
# What she smells and asks follows the late flag (laura_02 sheet; the street sheet, "Why she's late").
LATE_REASON_LINES = [
    G(cond(late_for("late_party")), P("Smoke in your hair, somebody's cologne on your neck. She smells it from the step."), D(L, "Zoe's?")),
    G(cond(late_for("late_shift")), P("You smell of coffee and the café's fryer. She knows that smell."), D(L, "Tom kept you late?")),
    G(cond(late_for("late_date")), P("She doesn't ask. She just looks at you, at your mouth, at your hair.")),
]
# (the flag, the truth, a lie that names somewhere else)
LATE_ANSWERS = [
    (late_for("late_party"), "Zoe's.", "I was at work."),
    (late_for("late_shift"), "Work.", "I was at Zoe's."),
    (late_for("late_date"), "Out with Jake.", "I was at Zoe's."),
]
LOW_WARMTH = cond(ntrait(L, "warmth", "lt", 40), trait("laura_suspicion", "gte", 50), logic="OR")
HIGH_WARMTH = cond(ntrait(L, "warmth", "gte", 40), trait("laura_suspicion", "lt", 50))
out.append({
    "id": "laura_02_home_late", "name": "Home late",
    "description": "Laura step 2 (Laura C 2): the first catch on the dark stairs. Low Warmth (or suspicion 50+): the curfew. High: \"Did anyone look at you in it?\"",
    "trigger": step_trigger(L, 2),
    "nodes": [
        node("stairs", "The dark stairs", [
            P("You've got your shoes in your hand and you're halfway to the stairs when the lamp on the landing clicks on. Laura is sitting on the third step from the top in her robe, arms round her knees. She's been there a while."),
            G(cond(trait("laura_suspicion", "gte", 30)),
              P("She comes down to you without a word and takes your chin in her hand and turns your face to the lamp. She looks you up and down, slowly, like she's reading it off you.")),
            *LATE_REASON_LINES,
            G(cond(DRESS_ON), P("Her eyes stop on the blue dress. Her dress. She doesn't say anything about it, but she looks at it for a long time.")),
        ], [
            go("Wait for it.", node="low", mins=2, cond_=LOW_WARMTH, eff=[susp(5)]),
            go("Wait for it.", node="high", mins=2, cond_=HIGH_WARMTH, eff=[susp(5)]),
        ]),
        node("low", "Grounded", [
            D(L, "You're grounded. A week. No parties, no late shifts, no guys at the door. I mean it, @player."),
            P("Her voice shakes. She's angry and she's scared, and you can't tell which is winning."),
            T("A week. She means every second of it."),
        ], [
            go("\"Fine.\"", loc="home_ella_room", mins=3, retry=1, flags=CURFEW_SET + [LATE_CLEAR], eff=CURFEW_EFF),
            *[go(f"\"{truth}\"", loc="home_ella_room", mins=3, retry=1, cond_=cond(late),
                 flags=CURFEW_SET + [LATE_CLEAR], eff=CURFEW_EFF) for late, truth, _ in LATE_ANSWERS],
            *[go(f"\"{lie}\" (she'll know)", node="lie", mins=2, cond_=cond(late)) for late, _, lie in LATE_ANSWERS],
        ]),
        node("lie", "She knows", [
            P("Her mouth goes thin. She knows what time it is, she can smell where you've been, and she knows when you're lying. She's always known."),
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
            D(L, "When I was nineteen I used to climb out of my window in my mother's dress. Red one. Backless. She never knew. I'd come home at dawn with my shoes in my hand and sit on the stairs so the stairs wouldn't creak."),
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
            go("\"Don't tell Mark.\"", node="secret", mins=5),
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
               flags=[done(5), fset("jake_04_done"), fset("laura_caught_today")])]),
        no_node("no", [P("You kiss his cheek and step back. Jake shrugs, grinning, and walks backwards down the path."), D(J, "Next Saturday, then."), P("In the dark window the shape on the couch hasn't moved. When you let yourself in, the living room is dark, and Laura doesn't say a word.")],
                "home_hall", 7, eff=[nadd(L, "want", 2)], flags=[funset("jake_date_booked")]),
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
PARTY_TO_2AM = [(("18:00", "19:00"), 465), (("19:00", "20:00"), 405), (("20:00", "21:00"), 345), (("21:00", "18:00"), 285)]
out.append({
    "id": "laura_07_dark_stairs", "name": "The dark stairs",
    "description": "Laura step 7 (Laura C 7), the voice sample: Friday, Laura comes to Zoe's party; the kiss on the dark stairs, and Ryan sees. The party screen moves the clock to about 02:00.",
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
            P("Laura pulls back on the stairs. Her lipstick is smeared, and she is breathing hard. She looks at Ryan in his doorway, then at you. She says nothing. She goes up past him to her bedroom, and her door clicks shut. \"@player.nickname,\" Ryan says, low. \"What was that?\" You don't answer him either. *You kissed your mother. You want her to do it again.* In the morning she'll be in the kitchen at breakfast. But a kitchen has nowhere to hide, and she'll have to look at you."),
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
                "conditions": cond(late_for("came_home_late"), flag("opening_done"), flag("laura_caught_today", False))},
    "nodes": [
        node("stairs", "On the stairs", [
            P("The landing lamp clicks on. Laura is on the stairs in her robe, waiting."),
            G(cond(flag("laura_02_done")), P("She waits like this now.")),
            G(cond(trait("laura_suspicion", "gte", 30)),
              P("She comes down and checks you over without asking: your face, your mouth, your hair."),
              D(L, "Tell me where you were. Don't lie to me.")),
            *LATE_REASON_LINES[:2],
            G(cond(late_for("late_date"), trait("laura_suspicion", "lt", 30), ntrait(L, "want", "lt", 50)),
              P("She doesn't ask. She just looks at you, at your mouth, at your hair.")),
            G(cond(late_for("late_date"), trait("laura_suspicion", "lt", 30), ntrait(L, "want", "gte", 50), trait("laura_step", "lt", 2)),
              P("She doesn't ask. She just looks at you, at your mouth, at your hair.")),
            G(cond(DRESS_ON), P("She looks at her dress on you for a long time.")),
            G(cond(trait("laura_step", "lt", 0)), D(L, "Grounded. Don't argue.")),
            G(cond(trait("laura_step", "gte", 8), trait("corruption", "lt", 60)), T("You want to kiss her goodnight, right here on the stairs. Not yet.")),
            G(cond(trait("laura_step", "gte", 2), ntrait(L, "want", "gte", 50)),
              D(L, "Sit down. Tell me everything. All of it, sweetheart."),
              P("She pats the step beside her. Her knee is bare where the robe has fallen open, and she doesn't fix it.")),
        ], [
            go("Tell her the truth.", node="truth", mins=10, cond_=cond(*HIGH_WARMTH["items"], trait("laura_step", "gte", 0)), eff=[susp(5), nadd(L, "warmth", 2)]),
            go("Lie. (she'll know)", node="lied", mins=5, cond_=cond(trait("laura_step", "gte", 0)), eff=[susp(10), nadd(L, "warmth", -5)]),
            go("Take what's coming.", node="grounded", mins=5, cond_=CAUGHT_LOW, eff=[susp(5)]),
            # Iteration 002, part 8 (laura_08's final, npc_laura.md:72): after her path ends, every catch
            # is the punishment; this one covers the high-Warmth case CAUGHT_LOW leaves out.
            go("Take what's coming.", node="grounded", mins=5, cond_=cond(trait("laura_step", "lt", 0), *HIGH_WARMTH["items"]), eff=[susp(5)]),
            go("Kiss her goodnight.", node="wall", cond_=cond(HUNGRY, trait("laura_step", "gte", 8))),
        ]),
        node("truth", "Everything", [
            G(cond(late_for("late_party")), POOL(
                P("You sit on the stair below hers and tell her: the party, the music, the guy who wouldn't stop looking. She listens with her chin on her knees. When you get to the part about him, she stops breathing."),
                P("You tell her who was there and what they drank and who left with who. She laughs in the right places. Then she asks what you were wearing, and listens to the answer like it matters."))),
            G(cond(late_for("late_shift")), P("You tell her about the close: the mop, the till, Tom counting the tips, the walk to the bus. She listens like it's a story, and asks what Tom's like when it's just the two of you.")),
            G(cond(late_for("late_date")), P("You tell her about Jake: where he took you, what he said, the walk back. She wants to know if he held your hand. She wants to know everything after that, too.")),
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
# Iteration 002, part 2: her home_life items are choices here (npc_laura.md:78-99; home_life.md).
# The plain line of each is the sheet's; its tease and touch screens are placeholders (LO, 2026-10-09).
from home_items import *
LS = "sheets/people/npc_laura.md"
K = "home_kitchen"
WEEKDAY_AM = [wd(0, 1, 2, 3, 4), tod("06:30", "08:00")]
HER_EVE = [wd(0, 1, 3, 4, 6)]
def l_tease(line, what):
    return {"label": "Let her look.", "ref": f"{LS}:{line}", "gate": [CURIOUS, trait("laura_step", "gte", 1)],
            "eff": [warm(L)], "what": f"Laura, {what}: tease (Curious, Laura C 1)"}
def l_touch(line, what, label="Let her hands stay."):
    return {"label": label, "ref": f"{LS}:{line}", "gate": [BOLD, trait("laura_step", "gte", 7)],
            "eff": [warm(L), CORR1], "what": f"Laura, {what}: touch (Bold, Laura C 7)"}
AT_TABLE = [
    G(cond(here(M, K)), P("Mark's at the head of the table already, reaching for the potatoes before anyone's sat down.")),
    G(cond(here(R, K), wd(0, 1, 2, 3, 4, 5)), P("Ryan slides in next to you with his hair still wet from the gym.")),
    G(cond(here(R, K), wd(6)), P("Ryan slides in next to you, still yawning from the couch.")),
]
hub_choices, hub_nodes = [], []
def add_item(*a, **k):
    c, n = item(*a, **k)
    hub_choices.extend(c); hub_nodes.extend(n)
# Breakfast and coffee share one screen (home_life items 6 and 11): "Eat." or "Just a coffee.", each with
# its own once-a-day flag; the coffee's tease and touch sit beside the breakfast's.
COFFEE_EXITS = [go("Just a coffee.", loc=K, mins=10, cond_=cond(flag("had_coffee", False)),
                   flags=[fset("had_coffee")], eff=[energy(5), warm(L)])]
for kind, spec in (("tease", l_tease(87, "coffee")), ("touch", l_touch(87, "coffee"))):
    sub = f"hl_coffee_{kind}"
    COFFEE_EXITS.append(go("Over coffee: " + spec["label"][0].lower() + spec["label"][1:], node=sub,
                           cond_=cond(flag("had_coffee", False), *spec["gate"]), eff=spec["eff"], flags=[fset("had_coffee")]))
    hub_nodes.append(node(sub, kind.title(), [placeholder(spec["ref"], spec["what"])], [go("Done.", loc=K, mins=10)]))
add_item("breakfast", "Have breakfast with her.", WEEKDAY_AM, "ate_breakfast", K,
         [D(L, "Eat something before class, sweetheart."), P("She pushes the toast over and puts a second mug down beside it."),
          G(cond(flag("had_coffee", False)), D(L, "Tell me one thing about yesterday."))],
         None, 15, done_exits=[go("Eat.", loc=K, mins=15, flags=[fset("ate_breakfast")], eff=[energy(10), warm(L)])] + COFFEE_EXITS,
         tease=l_tease(86, "breakfast"), touch=l_touch(86, "breakfast"),
         hungry="Further. (Needs Hungry)")
# One dinner, every evening she cooks (Mon, Tue, Thu, Fri, Sun 18:00-20:00). Sunday dinner reads
# room_tidy and clears it (npc_laura.md:96; home_ella_room.md:41): +2 tidy, -1 messy on top of dinner's +1.
NOT_SUN = wd(0, 1, 3, 4)
DINNER_DONE = [
    go("Done.", loc=K, mins=30, cond_=cond(NOT_SUN), flags=[fset("ate_dinner")], eff=[energy(15), warm(L)]),
    go("Done.", loc=K, mins=30, cond_=cond(wd(6), flag("room_tidy")), flags=[fset("ate_dinner"), funset("room_tidy")],
       eff=[energy(15), warm(L, 3)]),
    go("Done.", loc=K, mins=30, cond_=cond(wd(6), flag("room_tidy", False)), flags=[fset("ate_dinner")],
       eff=[energy(15)]),
    go("Ask what she saw in your room.", node="hl_tidy_tease", mins=30,
       cond_=cond(wd(6), flag("room_tidy"), CURIOUS, flag("ate_dinner", False)),
       flags=[fset("ate_dinner"), funset("room_tidy")], eff=[energy(15), warm(L, 3)]),
]
# The grocery run (home_life.md:100; LO Q67: $20 in, $20 out, Warmth +2 delivered, suspicion +2 after a day):
# Laura asks at dinner; you give it to her at a later dinner; a day late, she asks where it is. Each goes
# back to the dinner screen. One list at a time; asked once a day (`grocery_asked_today`, cleared at midnight).
OVERDUE = [flag("grocery_list"), flag("groceries_bought", False),
           {"type": "hours_since_flag", "subject": "player", "flag_key": "grocery_list", "operator": "gte", "value": 24}]
# One button on the dinner screen opens the list's own screen (Laura's dinner stays under 8 buttons).
# Giving it or owning up is once a day (`grocery_done_today`, cleared at midnight).
DINNER_DONE += [go("The shopping list.", node="hl_shop", mins=0)]
SHOP_EXITS = [
    go("\"Need anything from the shop?\"", node="hl_list", mins=2,
       cond_=cond(flag("grocery_list", False), flag("grocery_asked_today", False)),
       flags=[fset("grocery_list"), fset("grocery_asked_today")], eff=[{"targetType": "player", "trait": "money", "op": "add", "value": 20, "clamp": False}]),
    go("Give her the shopping.", node="hl_given", mins=2, cond_=cond(flag("groceries_bought"), flag("grocery_done_today", False)),
       flags=[funset("grocery_list"), funset("groceries_bought"), fset("grocery_done_today")], eff=[warm(L, 2)]),
    go("\"I forgot the shopping.\"", node="hl_forgot", mins=2, cond_=cond(*OVERDUE, flag("grocery_done_today", False)),
       flags=[funset("grocery_list"), fset("grocery_done_today")], eff=[susp(2), add("money", -20)]),
    go("Never mind.", node="hl_dinner"),
]
hub_nodes.append(node("hl_shop", "The shopping", [
    G(cond(flag("grocery_list", False)), P("The shopping pad is on the fridge, half a list already on it in her writing.")),
    G(cond(flag("grocery_list"), flag("groceries_bought", False)), P("Her list is still in your pocket.")),
    G(cond(flag("groceries_bought")), P("The bags are by the door where you left them.")),
], SHOP_EXITS))
hub_nodes += [
    node("hl_list", "Here's twenty", [D(L, "Could you get these? Here's twenty."),
                                       P("She tears a list off the pad on the fridge and folds a twenty into it. The corner shop has everything on it.")],
         [go("Pocket it.", node="hl_dinner")]),
    node("hl_given", "The shopping", [D(L, "You're an angel. Look, you even got the right wine."),
                                       P("She kisses the top of your head on her way to the fridge.")],
         [go("Sit back down.", node="hl_dinner")]),
    node("hl_forgot", "Where's my shopping", [D(L, "Where's my shopping? And where's my twenty?"),
                                               P("You hand it back."),
                                               G(cond(flag("laura_counted_twenty", False)), P("She counts it, which she has never done before.")),
                                               G(cond(flag("laura_counted_twenty")), P("She counts it again."))],
         [go("Sit back down.", node="hl_dinner", flags=[fset("laura_counted_twenty")])]),
]
hub_nodes.append(node("hl_tidy_tease", "Your room", [placeholder(f"{LS}:96", "Laura, Sunday dinner tidy check: tease (Curious)")],
                      [go("Done.", loc=K)]))
add_item("dinner", "Sit down to dinner.", HER_EVE + [tod("18:00", "20:00")], "ate_dinner", K,
         [D(L, "How's college?"), P("She actually waits for the answer."), *AT_TABLE,
          G(cond(wd(6), flag("room_tidy")), D(L, "Your room looked nice."), P("She means it. She squeezes your hand on the table.")),
          G(cond(wd(6), flag("room_tidy", False)), D(L, "I looked in your room. Pigsty."), P("She doesn't squeeze anything.")),
          G(cond(flag("grocery_list"), flag("groceries_bought", False),
                 {"type": "hours_since_flag", "subject": "player", "flag_key": "grocery_list", "operator": "gte", "value": 24}),
            D(L, "Where's my shopping?"))],
         None, 30, done_exits=DINNER_DONE,
         tease=l_tease(88, "dinner"), touch=l_touch(88, "dinner"))
add_item("cook", "Help her cook.", HER_EVE + [tod("18:00", "19:00")], "helped_cook", K,
         [P("She hands over the knife."), D(L, "Onions. Don't cry on my sauce.")],
         [energy(-5), warm(L)], 30, plain_costs=[{"trait": "energy", "value": 5}],
         tease=l_tease(89, "help her cook"), touch=l_touch(89, "help her cook", "Stay at the stove with her."))
add_item("dishes", "Do the dishes with her.", HER_EVE + [tod("19:00", "21:00")], "did_dishes", K,
         [D(L, "You wash, I dry."), P("Hip to hip at the sink.")],
         [energy(-5), warm(L)], 20, plain_costs=[{"trait": "energy", "value": 5}],
         tease=l_tease(90, "dishes"), touch=l_touch(90, "dishes"))
add_item("wine", "Have a glass with her.", HER_EVE + [tod("20:00", "22:00"), trait("laura_step", "gte", 3)], "had_drink_home", K,
         [G(cond({"type": "npc_at_location", "location_id": "home_kitchen", "npc_id": "npc_mark", "operator": "is_absent"}), D(L, "One glass. Don't tell Mark.")), G(cond({"type": "npc_at_location", "location_id": "home_kitchen", "npc_id": "npc_mark", "operator": "is_present"}), D(L, "One glass. Just the one.")),
          P("She pours two and clinks yours before you've picked it up.")],
         None, 30, done_exits=[go("Done.", loc=K, mins=30, eff=[warm(L)], flags=[fset("had_drink_home")], mods=DRINK)],
         tease=l_tease(91, "a glass of wine"), touch=l_touch(91, "a glass of wine"))
add_item("study", "Study at the kitchen table.", HER_EVE + [tod("19:00", "22:00")], "studied_home", K,
         [P("You spread your notes across the end of the table. She reads over your shoulder."), D(L, "That's wrong. No — that.")],
         None, 60, done_exits=[go(f"{name}.", loc=K, mins=60, flags=[fset("studied_home")],
                                  costs=[{"trait": "energy", "value": 10}],
                                  eff=[energy(-10), warm(L), {"targetType": "player", "trait": key, "op": "add", "value": 1, "cap": 100}])
                               for key, name in (("grade_psych", "Psychology"), ("grade_business", "Business"),
                                                 ("grade_bio", "Biology"), ("grade_art", "Figure drawing"))],
         tease={"label": "Let her keep her hand there.", "ref": f"{LS}:94", "gate": [CURIOUS, trait("laura_step", "gte", 1)],
                "eff": [warm(L)], "what": "Laura, study at the table: tease (Curious, Laura C 1)"})
hub_nodes.append(hungry_node(K))
UNIFORM_LINES = [
    G(cond(NORMAL_ON), D(L, "Look at you. My working girl. Sit, I'll make you something.")),
    G(cond(SEXY_ON), P("Laura looks at the open top button for a long second."), D(L, "Is that the uniform, or Tom's idea?")),
]
out.append({
    "id": "hub_laura_kitchen", "name": "Laura",
    "description": "Laura's hub in the kitchen: breakfast, coffee, dinner, help her cook, dishes, a glass, study at the table (home_life). Warmth +2 a talk (once a day). Reads her clothes lines, her ladder's leaks, the start choice (at dinner), hygiene, made_up.",
    "trigger": {"location": K, "npc": L, "requires_npc": L, "is_repeatable": True,
                "priority": 6, "is_active": True, "conditions": cond(flag("opening_done"))},
    "nodes": [
        node("kitchen", "The kitchen", [
            G(cond(tod("06:30", "08:00")),
              P("Laura is in her work blouse, buttering toast with one hand and holding her coffee with the other."),
              POOL(
                   D(L, "Morning. Is that what you're wearing?"),
                   D(L, "Your hair looks nice like that."))),
            G(cond(tod("18:00", "22:00")),
              P("Laura's at the stove with the radio on and a glass of white by the chopping board."),
              POOL(D(L, "Sit. Tell me about your day."),
                   D(L, "Pour me another, would you?"))),
            G(cond(tod("18:00", "22:00"), {"type": "npc_at_location", "location_id": "home_kitchen", "npc_id": "npc_mark", "operator": "is_absent"}), D(L, "Don't tell Mark how many that is.")),
            G(cond(tod("18:00", "19:50"), flag("ate_dinner", False)), D(L, "Dinner in ten. Set the table?")),
            G(cond(tod("06:30", "08:00"), flag("ate_breakfast", False)), D(L, "Eat something, sweetheart. You're not going to class on nothing.")),
            G(cond(tod("18:00", "22:00"), flag("college_for_grades")), D(L, "How are the grades? You said grades. I'm holding you to it.")),
            G(cond(tod("18:00", "22:00"), flag("college_for_fun")), D(L, "Having fun yet? You said fun. Don't have too much.")),
            G(cond(tod("18:00", "22:00"), flag("college_for_freedom")), D(L, "Freedom, you said. You still live in my house, you know.")),
            G(cond(wd(1), tod("18:00", "22:00"), trait("laura_step", "eq", 0)),
              P("She dries her hands on her apron and looks at you with a funny little smile."),
              D(L, "Come upstairs after. I have something for you.")),
            G(cond(trait("laura_step", "gte", 1), trait("laura_step", "lt", 3)), P("Her eyes go to you and stay a second too long. She keeps a second glass on the counter now.")),
            G(cond(trait("laura_step", "eq", 3), trait("ryan_step", "gte", 2)), D(L, "How's Ryan? You two seem close lately.")),
            G(cond(trait("laura_step", "eq", 4), flag("jake_date_booked")), D(L, "Is Jake bringing you home on Saturday?")),
            G(cond(trait("laura_step", "eq", 5)), P("She's started leaving her bedroom door open when she dresses.")),
            G(cond(trait("laura_step", "eq", 6)), D(L, "Wear something short, you said.")),
            G(cond(trait("laura_step", "eq", 7)), P("She can't meet your eyes. Her hand isn't steady on the cup.")),
            G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), D(L, "Is that for college or for a guy?")),
            G(cond(DRESS_ON), D(L, "It never fit me like that."), P("Her hand smooths the hip of it without thinking.")),
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "worn_exposure", "operator": "eq", "value": 0}),
              P("Her eyes stop on your chest. Then she pours the coffee.")),
            G(cond({"type": "worn_type", "operator": "eq", "value": "towel"}), D(L, "Go and get dressed, sweetheart. You'll catch your death.")),
            *UNIFORM_LINES,
            G(cond(*MADE_UP), D(L, "You did your face. Who's that for?")),
            G(cond(trait("hygiene", "lt", 30), flag("hygiene_off", False)), D(L, "Sweetheart. Shower. Today.")),
            G(cond(ntrait(L, "warmth", "lt", 30)), P("She's short with you. Everything you do lands wrong with her lately.")),
            G(cond(ntrait(L, "warmth", "gte", 70)), P("She touches your hair when she passes. She's on your side, whatever you've done.")),
        ], [
            *hub_choices,
            go("Talk to her.", node="talk", mins=20, cond_=cond(flag("laura_talk_today", False)),
               flags=[fset("laura_talk_today")],
               eff=[{"targetType": "npc", "npcId": L, "trait": "warmth", "op": "add", "value": 2, "cap": 100}]),
            go("Follow her upstairs.", loc="home_master_bedroom", mins=2, flags=[fset("laura_dress_invite")],
               cond_=cond(wd(1), tod("18:00", "22:00"), trait("laura_step", "eq", 0))),
            go("Leave her to it.", loc="home_hall"),
        ]),
        node("talk", "Talk", [
            POOL(
                P("You sit on the counter and talk while she works. She asks about your classes, and you tell her the boring half."),
                P("She tells you about her office, the man who steals her yoghurt, the boss who calls everyone 'champ'. You make her laugh until she has to put the knife down."),
                P("You lean on the counter beside her while she chops. She hums. For a while it's just the two of you and it's easy."),
            ),
            G(cond(trait("hygiene", "lt", 30), flag("hygiene_off", False)),
              P("Halfway through she wrinkles her nose and steps back, and the easy goes out of it.")),
        ], [go("Go.", loc=K, mins=5)]),
        *hub_nodes,
    ]})

# ── waiting up on Saturday nights, in the dark living room: a film or the TV with her ──
lr_choices, lr_nodes = [], []
for args, kw in [
    (("film", "Watch the film with her.", [tod("22:00", "00:00")], "movie_night", "home_living_room",
      [P("A film on low, the only light in the room."), D(L, "Sit with me a while.")],
      [energy(5), warm(L, 2)], 120),
     dict(tease=l_tease(92, "movie night"), touch=l_touch(92, "movie night", "Stay under the blanket with her."))),
    (("tv", "Watch TV with her.", [tod("22:00", "00:00")], "watched_tv", "home_living_room",
      [P("She hands you the remote without looking away from the door."), D(L, "Find something. Anything.")],
      [energy(5), warm(L)], 60), {}),
]:
    c, n = item(*args, **kw); lr_choices += c; lr_nodes += n
out.append({
    "id": "hub_laura_living_room", "name": "Laura, waiting up",
    "description": "Laura waiting up in the dark living room on Saturday nights; she can see the front door. A film (+2 Warmth) or the TV with her (home_life).",
    "trigger": {"location": "home_living_room", "npc": L, "requires_npc": L, "is_repeatable": True,
                "priority": 6, "is_active": True, "conditions": cond(flag("opening_done"))},
    "nodes": [
        node("dark", "The dark living room", [
            P("The lights are off. Laura is on the couch with her knees pulled up under her robe and a glass of wine she isn't drinking. From here she can see the front door and the path outside it."),
            POOL(D(L, "I'm not waiting up. I just couldn't sleep."),
                 D(L, "Come and sit with me. It's nice in the dark."),
                 D(L, "Who's bringing you home tonight?")),
            G(cond(trait("laura_step", "gte", 5)), D(L, "I saw you, you know. On the step. I didn't look away.")),
        ], [*lr_choices, go("Leave her be.", loc="home_hall")]),
        *lr_nodes,
    ]})

# ── their room: Laura dressing on Saturday evenings (her hair), or asleep at night ──
DRESSING = [wd(5), tod("17:00", "18:30")]
bd_choices, bd_nodes = item("hair", "Let her do your hair.", DRESSING, "made_up_today", "home_master_bedroom",
    [P("She sits you down at her mirror and brushes your hair out, long strokes."), D(L, "You had my hair at your age.")],
    [warm(L)], 20,
    done_exits=[go("Done.", loc="home_master_bedroom", mins=20, eff=[warm(L)], flags=[fset("made_up_today"), fset("made_up")])],
    tease={"label": "Watch her in the mirror.", "ref": f"{LS}:95", "gate": [CURIOUS, trait("laura_step", "gte", 1)],
           "eff": [warm(L)], "what": "Laura, her hair: tease (Curious, Laura C 1)"})
out.append({
    "id": "hub_laura_bedroom", "name": "Laura",
    "description": "Laura in her room: dressing on Saturday evenings with the door open (her hair, home_life item 12), or asleep at night (her face; home_master_bedroom.md:36-45).",
    "trigger": {"location": "home_master_bedroom", "npc": L, "requires_npc": L, "is_repeatable": True,
                "priority": 6, "is_active": True, "conditions": cond(flag("opening_done"))},
    "nodes": [
        node("mirror", "Laura", [
            G(cond(*DRESSING),
              P("Laura is at her long mirror in her slip, holding two dresses up one after the other."),
              POOL(D(L, "Black or green? Mark won't notice either way."),
                   D(L, "Do I look old in this? Be honest. No, don't be honest."),
                   D(L, "Hand me those earrings, sweetheart."))),
            G(cond(*DRESSING, trait("laura_step", "gte", 6)), P("She leaves the zip undone and turns her back to you without asking. She knows you'll do it.")),
            G(cond(*DRESSING, trait("laura_step", "lt", 6)), P("She catches you watching her in the mirror, and holds it."), D(L, "One of these nights I'm coming out with you. Don't think I won't.")),
            G(cond(tod("22:00", "07:00")),
              P("Laura's asleep on her side, curled toward the wall, one bare shoulder out of the covers. She doesn't stir.")),
        ], [*bd_choices,
            go("Help her choose.", node="choose", mins=20, cond_=cond(*DRESSING)),
            go("Back out.", loc="home_hall")]),
        node("choose", "Black or green", [
            P("You make her try both. Then the black again. She turns side to side in the mirror while you tell her the truth: the green."),
            D(L, "The green it is. Don't tell Mark it was your idea."),
        ], [go("Leave her to finish.", loc="home_hall")]),
        *bd_nodes,
    ]})

# ── her curfew call (npc_laura.md:130-137): while the curfew is on, Friday 21:00-22:00, Laura
# awake in the kitchen. She never says where @player is (the engine can't see it), and answering
# never moves her: every way out is `return` (engine.md §13). Missed: suspicion +2 (8_phone.toml).
out.append({
    "id": "laura_curfew_call", "name": "Mom, on the phone",
    "description": "Laura's curfew call (8_phone.toml), Friday 21:00-22:00 while the curfew is on. It never says where she is; both answers return her to where she was.",
    "trigger": {"location": "home_ella_room", "is_repeatable": True, "priority": 1, "is_active": True, "substitution_only": True},
    "nodes": [
        node("call", "Mom", [
            D(L, "It's nine. You know the rule. Home by eleven."),
        ], [go("\"I know. Eleven.\"", node="good", mins=2, flags=[fset("laura_call_today")]),
            go("\"I'm staying at Zoe's.\"", node="talk", mins=2, eff=[susp(2)], flags=[fset("laura_call_today")],
               cond_=cond(flag("laura_call_today", False)))]),
        node("good", "Good girl", [D(L, "Good girl.")], [go("Hang up.", ret=True)]),
        node("talk", "We'll talk", [D(L, "We'll talk about this."), P("She hangs up before you can answer.")], [go("Put the phone away.", ret=True)]),
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
# Iteration 002, part 3: leaving this outing after 22:00 sets late_date and came_home_late (Q69,
# the street sheet "Why she's late"; canv.mark_late). Each is read for 4 hours; her bed clears them.
for _c in out:
    if _c["id"] in ['laura_05_jake_at_the_door']:
        mark_late(_c, 'late_date', split=False)

# Iteration 002, part 7: she watches from the dark living room in step 5 (gate: a named person is where the line says)
require_present(out, "laura_05_jake_at_the_door", here_at(L, "home_living_room"))
text += "".join(emit(c) for c in out) + "".join(emit_card(c) for c in cards)
open(__import__("sys").argv[1], "w").write(text)
print("laura:", len(out), "canvases,", len(cards), "cards")
