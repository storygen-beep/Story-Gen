"""Laura — steps 1-8 (Laura C 1-8; step 5 = Jake B 4), her hubs, the catch, the curfew call.
Source: sheets/scenes/laura_0*.md, sheets/people/npc_laura.md. Explicit screens pasted as signed."""
import json
from canv import *
from tomlw import tod, wd
M = "npc_mark"
R = "npc_ryan"

L = "npc_laura"
J = "npc_jake"
out = []

def at_level(meter, lines, make=T):
    """Her line by her band of `meter` (register.md, "One event, several levels"). lines: {band floor: text}, only the
    bands the step can reach; the lowest listed band has no lower bound. Mutually exclusive, so one adjacent chain."""
    floors = sorted(lines)
    blocks = []
    for i, lo in enumerate(floors):
        items = ([trait(meter, "gte", lo)] if i else []) + ([trait(meter, "lt", floors[i + 1])] if i + 1 < len(floors) else [])
        blocks.append(GC(cond(*items), make(lines[lo])))
    return blocks

def done(n):
    return fset(f"laura_0{n}_done")

def susp(n):
    return add("laura_suspicion", n)

CURFEW_SET = [fset("curfew")]
LATE_CLEAR = funset("came_home_late")
DRESS_ON = {"type": "clothing_item", "item_id": "laura_blue_dress", "operator": "equipped"}

# ── step 1 · Laura C 1 · the blue dress (fires in her room; the kitchen line is on her hub) ──
_t1 = step_trigger(L, 1, bind_npc=False)
# truth pass (2026-11-03): she comes up from the kitchen "still in her kitchen apron", so the step reads her there
# when it fires (her Tue 18:00-22:00 kitchen row; the invite on her kitchen hub is under an hour old)
_t1["conditions"]["items"] += [here_at(L, "home_kitchen"), flag("laura_dress_invite"),
                               {"type": "hours_since_flag", "subject": "player", "flag_key": "laura_dress_invite", "operator": "lt", "value": 1}]
out.append({
    "id": "laura_01_blue_dress", "name": "Try on Laura's blue dress",   # pass 3 H33/H34 (the-voice.md R1, D11): the name says what happens if she clicks, and never hides the act
    "description": "Laura step 1 (Laura C 1), Tuesday evening, in the master bedroom (seen from the kitchen: her hub there says 'Come to my room'). Adds and equips laura_blue_dress. Sets laura_01_done (her thread).",
    "trigger": _t1,
    "nodes": [
        node("upstairs", "Her room", [
            P("Laura is right behind you down the hall, still in her kitchen apron, drying her hands on it. She shuts her bedroom door and goes straight to the wardrobe and reaches into the back, past the work blouses, to something in dry-cleaner plastic."),
            D(L, "I was saving this, but I don't know what for. Here. Try it."),
            P("It's a dress, blue, soft, short enough that she must have been very young when she wore it. She holds it against you and her eyes go somewhere far away."),
        ], [go("Try it on.", node="mirror", mins=10,
               wardrobe=[{"action": "add", "item_id": "laura_blue_dress"}, {"action": "equip", "item_id": "laura_blue_dress"}])]),
        node("mirror", "The mirror", [
            IMG("scenes/laura_01_mirror.jpg", "a mother behind her adult daughter in a long bedroom mirror, the daughter in a short tight blue dress, the mother's hands smoothing it at the hips",
                "mother behind daughter mirror blue dress", "woman fixing young woman's dress in bedroom mirror"),
            P("It's tight across your chest. It stops high on your thighs. In her long mirror you look like someone older, someone who goes out. Laura stands behind you and smooths the fabric down over your hips with both hands, slowly, and keeps her hands there a second longer than she needs to."),
            P("Her eyes in the mirror aren't on the dress. They're on you."),
            *at_level("exhibitionism", {
                0: "It's too tight, it's too short, and your mom is staring at you in it. You want to take it off.",
                20: "She's looking at you like a stranger would, but you don't hate it.",
                40: "Let her look. You stand up straighter, and your tits fill the front of the dress.",
                60: "You want somebody looking at you in this the way she is, and you want it tonight."}),
        ], [
            go("\"Is that bad?\"", node="no", mins=3),
            go("\"I can't take this.\"", node="give", mins=3),
        ]),
        node("no", "It never fit me like that", [
            ME("Is that bad?"),
            D(L, "It never fit me like that."),
            P("She says it quietly, to the mirror. Then she laughs, too bright, and takes her hands off you."),
            D(L, "No. No, sweetheart. It's not bad."),
            D(L, "Keep it. Wear it somewhere somebody can see you in it."),   # pass 4 reader (hook): this branch names what comes next too
        ], [go("\"Thank you, Mom.\"", loc="home_ella_room", mins=5, consumes=True,
               eff=[nadd(L, "warmth", 5), add("exhibitionism", 3, cap=79), setv("laura_step", 1)], flags=[done(1)])]),
        node("give", "Keep it", [
            ME("I can't take this. It's yours."),
            D(L, "Keep it. Wear it somewhere."),
            P("She won't take it back. She folds your hands round the hanger and holds them there, and her thumb strokes the back of your wrist."),
            D(L, "Somebody should look at you in it."),
        ], [go("\"Okay.\"", loc="home_ella_room", mins=5, consumes=True,
               eff=[nadd(L, "warmth", 5), add("exhibitionism", 3, cap=79), setv("laura_step", 1)], flags=[done(1)])]),
    ]})

# ── step 2 · Laura C 2 · home late: the first catch ──
# What she smells and asks follows the late flag (laura_02 sheet; the street sheet, "Why she's late").
LATE_REASON_LINES = [
    G(cond(late_for("late_party")), P("Smoke in your hair, somebody's cologne on your neck. She smells it on you."), D(L, "Zoe's?")),   # pass 4 reader: one hall, no stairs (Q7)
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
    "description": "The curfew rule (laura_curfew_rule.md, release 1): every time she comes home late, Laura waiting up in the dark hall. Low Love (or suspicion 50+): the curfew. High: \"Did anyone look at you in it?\" No longer a step of her ladder.",
    "trigger": {"location": "home_hall", "npc": L, "requires_npc": L, "is_repeatable": True, "priority": 7, "is_active": True,
                "conditions": cond(late_for("came_home_late"), flag("opening_done"), flag("laura_caught_today", False))},
    "nodes": [
        node("stairs", "The dark hall", [
            P("You're in the hall when the hall lamp clicks on. Laura is sitting on the bench by the coats in her robe, arms round her knees. She's been there a while."),
            G(cond(trait("laura_suspicion", "gte", 30)),
              P("She gets up and comes to you without a word and takes your chin in her hand and turns your face to the lamp. She looks you up and down, slowly, like she's reading it off you.")),
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
            go("\"Fine.\"", loc="home_ella_room", mins=3, flags=CURFEW_SET + [LATE_CLEAR, fset("laura_caught_today")], eff=CURFEW_EFF),
            *[go(f"\"{truth}\"", loc="home_ella_room", mins=3, cond_=cond(late),
                 flags=CURFEW_SET + [LATE_CLEAR, fset("laura_caught_today")], eff=CURFEW_EFF) for late, truth, _ in LATE_ANSWERS],
            *[go(f"\"{lie}\" (she'll know)", node="lie", mins=2, cond_=cond(late)) for late, _, lie in LATE_ANSWERS],
        ]),
        node("lie", "She knows", [
            P("Her mouth goes thin. She knows what time it is, she can smell where you've been, and she knows when you're lying. She's always known."),
            D(L, "Bed. Now."),
        ], [go("\"Goodnight, Mom.\"", loc="home_ella_room", mins=3,
               eff=[nadd(L, "warmth", -5), susp(5)] + CURFEW_EFF, flags=CURFEW_SET + [LATE_CLEAR, fset("laura_caught_today")])]),
        node("high", "Did anyone look", [
            P("She doesn't shout. She sits you down on the bench beside her, and she looks at you sideways in the lamplight."),   # reader 2026-11-04: at suspicion 30+ she has already got up
            D(L, "I'm not angry. I was nineteen once. Just— did you have fun?"),
            ME("Yeah."),
            G(cond(DRESS_ON), D(L, "Did anyone look at you in it?")),
            G(cond({"type": "clothing_item", "item_id": "laura_blue_dress", "operator": "unequipped"}), D(L, "Did anyone look at you?")),
        ], [go("\"I don't know. Maybe.\"", node="after", mins=1, cond_=cond(trait("exhibitionism", "lt", 20))),
            go("\"A couple of guys.\"", node="after", mins=1, cond_=cond(trait("exhibitionism", "gte", 20), trait("exhibitionism", "lt", 40))),
            go("\"Everyone.\"", node="after", mins=1, cond_=cond(trait("exhibitionism", "gte", 40), trait("exhibitionism", "lt", 60))),
            go("\"Everyone. I made sure of it.\"", node="after", mins=1, cond_=cond(trait("exhibitionism", "gte", 60)))]),
        # reader 2026-11-04: her answer by Exhibitionism (being looked at), Laura's reply, and the hook: she waits up every late night
        node("after", "The bench", [
            GC(cond(trait("exhibitionism", "lt", 20)), D(L, "You'd know, sweetheart. You'd feel it on your skin."),
               P("You feel it now, her eyes on you in the lamplight, and your face goes hot.")),
            GC(cond(trait("exhibitionism", "lt", 40)), D(L, "A couple. Good. And you looked back, didn't you?"),
               P("She's smiling, but her eyes go down your legs and take their time coming back.")),
            GC(cond(trait("exhibitionism", "lt", 60)), D(L, "Everyone. God, look at you."),
               P("Her eyes stop on your legs, and she laughs under her breath.")),
            GC(cond(trait("exhibitionism", "gte", 60)), D(L, "You made sure of it."),
               P("Her eyes go to your tits and stay a second too long. Then she pulls her robe shut at the neck.")),
            D(L, "I'll be on this bench the next time you're late. Go to bed."),
        ], [go("Go to bed.", loc="home_ella_room", mins=4, flags=[LATE_CLEAR, fset("laura_caught_today")])]),
    ]})

# ── step 3 · Laura C 3 · wine in the kitchen ──
out.append({
    "id": "laura_03_wine_in_the_kitchen", "name": "Wine in the kitchen",
    "description": "Laura step 2 of 4 (release 1; was Laura C 3): her secret, and Mark hasn't looked at her like that since the wedding.",
    "trigger": step_trigger(L, 2),
    "nodes": [
        node("glass", "Sit with me", [
            P("The kitchen's dark except the light over the stove. Laura's at the table with a bottle of white and two glasses, one of them already poured. Her robe is open at the collar. She's been waiting for somebody, but it wasn't Mark."),
            D(L, "Sit with me. Just for a bit."),
        ], [
            go("\"Pour me one.\"", node="story", mins=10),
            go("\"I'm tired, Mom.\"", node="no", mins=2),
        ]),
        node("story", "Her mother's dress", [
            P("She pours, and you clink, and she drinks half of hers like it's water. Then she tells you, out of nowhere, staring at the stove."),
            D(L, "When I was nineteen I used to climb out of my window in my mother's dress. Red one. Backless. She never knew. I'd come home at dawn with my shoes in my hand and walk on the edge of the hall carpet so the boards wouldn't creak."),
            P("She laughs into her glass."),
            D(L, "I used to get looked at, sweetheart. Like you get looked at."),
        ], [go("\"Mom!\"", node="mark", mins=10)]),
        node("mark", "Since the wedding", [
            D(L, "Don't \"Mom\" me. I had a body."),
            P("She tips the glass at you, smiling, and then the smile goes."),
            D(L, "Mark hasn't looked at my body like that since the wedding."),
            P("She says it to the wine. Then she looks at you, at your mouth, at your throat, and away, fast."),
            *at_level("corruption", {
                0: "She's your mom. You don't want to hear this. You want to finish your wine and go to bed.",
                20: "She wants somebody to look at her. She's telling you.",
                40: "She wants somebody to look at her, and you're the one sitting here. So you look.",
                60: "She just looked at your mouth. You want to know what she'd do if you looked back and didn't stop."}),
        ], [go("\"He should.\"", loc="home_hall", mins=5, consumes=True,
               eff=[nadd(L, "warmth", 5), setv("laura_step", 2)], flags=[done(3)])]),
        no_node("no", [P("She nods and puts the empty glass back on the shelf, carefully, so it doesn't clink."), D(L, "Go on, then. Bed."), P("She drinks the rest of hers alone, looking at the stove.")],
                "home_hall", 2, eff=[nadd(L, "warmth", -1)], label="Say goodnight and go."),   # pass 3 D39 (R7)
    ]})

# (release 1: laura_05_jake_at_the_door is merged into Jake's step 3, jake.py)

# ── step 3 · All dressed up (laura_03b_all_dressed_up.md, signed 2026-11-01): the laura_06 canvas reworked.
#    The zip, Mark off to the bar, "Do I still look like someone you'd look at?" Sets laura_lonely. ──
DONE3 = [nadd(L, "warmth", 5), setv("laura_step", 3)]
out.append({
    "id": "laura_06_take_me_with_you", "name": "All dressed up",
    "description": "Laura step 3 of 4 (release 1): Saturday early evening, Laura dressing up; Mark goes to the bar; she sits on the bed dressed up with nowhere to go. Sets laura_lonely.",
    "trigger": step_trigger(L, 3, retry_days=7),
    "nodes": [
        node("zip", "Zip me up", [
            P("Her bedroom door is open. Laura is in front of the long mirror in her good dress, holding it to her chest, the zip open all the way down to the small of her back."),
            D(L, "Zip me up, sweetheart? Mark's useless at it."),
        ], [
            go("\"Hold still.\"", node="zipped", mins=0),   # reader 2026-11-04: fired at 18:29, Mark calls before his row ends at 18:30; the 3 minutes go on "Wait."
            go("\"Ask Mark.\"", node="no", mins=2),
        ]),
        node("zipped", "Heading out", [
            P("You pull the zip up slowly, all the way to her shoulder blades. She smooths the dress over her hips and turns side-on to the mirror."),
            # her want for Ryan, on her body, before her step 4 says his name; true only while he is on the couch (DECISIONS 124)
            G(cond({"type": "npc_at_location", "location_id": "home_living_room", "npc_id": "npc_ryan", "operator": "is_present"}),
              P("In the living room Ryan laughs at something on the TV. Laura's hands stop on the dress. She looks at the door, not at you, and her chest rises fast under the silk.")),
            # reader pass 4 b5: his row has him in the kitchen till 18:30 ("heading out to the bar"), so he calls from
            # there and has not left yet; the front door does not go on this screen
            D(M, "Laur? I'm heading out to the bar with the guys. Don't wait up."),
            P("In the kitchen his keys jingle. He doesn't come to see her in the dress. Laura stands very still in front of the mirror."),
        ], [go("Wait.", node="bed", mins=5)]),
        node("bed", "Nowhere to go", [
            P("She sits down on the end of the bed in her good dress, her heels in her hand. Her lipstick is perfect. She has nowhere to go."),
            # copy fix A6 (DECISIONS 125): her want on her body, Laura's early column ("chest"); the Ryan line is in `zipped`
            P("She pulls her shoulders back for the mirror, and her chest lifts in the dress. She's looking at herself the way she wants somebody to look at her."),
            # reader pass 3 b00: low heat on Ella's body too, and Laura's reaction to it
            P("Then her eyes find you in the mirror and go down you, slow: your tits, your waist, the curve of your hips. Her mouth goes tight, and she looks away first."),
            D(L, "Do I still look like someone you'd look at?"),
            *at_level("corruption", {
                0: "She's your mom, and she's asking you this. You don't know where to put your eyes.",
                20: "She's asking you, because nobody else is here to ask. You wonder what she'd do if you said yes.",
                40: "She just looked at your tits and looked away. Ask her why, then.",
                60: "Yes, you'd look. You're looking now, and you want her to know it."}),
        ], [
            go("\"You look beautiful, Mom.\"", node="liar", mins=2),
            go("Say nothing.", node="quiet", mins=2),
        ]),
        node("liar", "Liar", [
            D(L, "Liar."),
            P("She says it smiling, and her eyes are wet."),
            P("On weeknights now, her bedroom door doesn't quite close."),
        ], [go("\"See you later, Mom.\"", loc="home_hall", mins=3, consumes=True, eff=DONE3, flags=[done(6), fset("laura_lonely")])]),
        node("quiet", "Quiet", [
            P("You sit down beside her. You don't say anything. After a while she puts her head on your shoulder, and her hair smells of the perfume she put on for nobody."),
            D(L, "Thank you, sweetheart."),
            P("On weeknights now, her bedroom door doesn't quite close."),
        ], [go("\"See you later, Mom.\"", loc="home_hall", mins=10, consumes=True, eff=DONE3, flags=[done(6), fset("laura_lonely")])]),
        no_node("no", [D(L, "Mark. Right."), P("She reaches round and does the zip herself, badly, halfway, and leaves it there. She doesn't ask you again tonight.")],
                "home_hall", 7, eff=[nadd(L, "warmth", -1)], label="Leave her with the zip."),   # pass 3 D39 (R7)
    ]})
# Mark leaves for the bar from the house: his rows put him nowhere Saturday 17:00-22:00 (home, the garage until 17:00).

# ── her kitchen: breakfast and evenings (her hub). Tuesday before step 1: "Come upstairs." ──
# Iteration 002, part 2: her home_life items are choices here (npc_laura.md:78-99; home_life.md).
# The plain line of each is the sheet's; its tease and touch screens are placeholders (LO, 2026-10-09).
from home_items import *
LS = "sheets/people/npc_laura.md"
K = "home_kitchen"
WEEKDAY_AM = [wd(0, 1, 2, 3, 4), tod("06:30", "08:00")]
HER_EVE = [wd(0, 1, 3, 4, 6)]
# Release 1 (npc_laura.md, signed 2026-11-01): her plain items stay; the tease and touch columns are cut
# (never written; against "good mom"). The helpers return None, which item() skips.
def l_tease(line, what):
    return None
def l_touch(line, what, label=None):
    return None
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
# pass 3 D44 (the-surfaces.md R9): the coffee, breakfast, dishes, cooking, wine and film with her each land on a short
# screen of her reaction (item(after=...)), not a toast. Same effects, time and caps on the act button.
COFFEE_EXITS = [go("Just a coffee.", node="hl_coffee_after", mins=10, cond_=cond(flag("had_coffee", False)),
                   flags=[fset("had_coffee")], eff=[energy(5), warm(L)])]
hub_nodes.append(node("hl_coffee_after", "Just a coffee", [
    P("You drink it black and too fast, leaning on the counter, and she shakes her head at you over her own mug."),
    D(L, "That's not breakfast, sweetheart."),
], [go("Grab your bag.", loc=K)]))
for kind, spec in (("tease", l_tease(87, "coffee")), ("touch", l_touch(87, "coffee"))):
    if not spec:
        continue
    sub = f"hl_coffee_{kind}"
    COFFEE_EXITS.append(go("Over coffee: " + spec["label"][0].lower() + spec["label"][1:], node=sub,
                           cond_=cond(flag("had_coffee", False), *spec["gate"]), eff=spec["eff"], flags=[fset("had_coffee")]))
    hub_nodes.append(node(sub, kind.title(), [placeholder(spec["ref"], spec["what"])], [go("Done.", loc=K, mins=10)]))
add_item("breakfast", "Have breakfast with her.", WEEKDAY_AM, "ate_breakfast", K,
         [D(L, "Eat something before class, sweetheart."), P("She pushes the toast over and puts a second mug down beside it."),
          G(cond(flag("had_coffee", False)), D(L, "Tell me one thing about yesterday."))],
         None, 15, done_exits=[go("Eat with her.", node="hl_breakfast_after", mins=15, flags=[fset("ate_breakfast")], eff=[energy(10), warm(L)])] + COFFEE_EXITS,
         tease=l_tease(86, "breakfast"), touch=l_touch(86, "breakfast"),
         after=("Eat with her.", [P("You eat the toast at the counter while she watches you over her mug, and she wipes a crumb off your lip with her thumb."),
                                  D(L, "There. Now go and be clever.")], "Grab your bag."))
# One dinner, every evening she cooks (Mon, Tue, Thu, Fri, Sun 18:00-20:00). Sunday dinner reads
# room_tidy and clears it (npc_laura.md:96; home_ella_room.md:41): +2 tidy, -1 messy on top of dinner's +1.
NOT_SUN = wd(0, 1, 3, 4)
DINNER_DONE = [
    go("Done.", loc=K, mins=30, cond_=cond(NOT_SUN), flags=[fset("ate_dinner")], eff=[energy(15), warm(L)]),
    go("Done.", loc=K, mins=30, cond_=cond(wd(6), flag("room_tidy")), flags=[fset("ate_dinner"), funset("room_tidy")],
       eff=[energy(15), warm(L, 3)]),
    go("Done.", loc=K, mins=30, cond_=cond(wd(6), flag("room_tidy", False)), flags=[fset("ate_dinner")],
       eff=[energy(15)]),
    # reader a3 verify (DECISIONS 131): after an accident with her first (H2): her door or her shower; two copies, never both
    go("Ask what she saw in your room.", node="hl_tidy_tease", mins=30,
       cond_=cond(wd(6), flag("room_tidy"), CURIOUS, flag("ate_dinner", False), flag("saw_laura_alone")),
       flags=[fset("ate_dinner"), funset("room_tidy")], eff=[energy(15), warm(L, 3)]),
    go("Ask what she saw in your room.", node="hl_tidy_tease", mins=30,
       cond_=cond(wd(6), flag("room_tidy"), CURIOUS, flag("ate_dinner", False), flag("saw_laura_alone", False), flag("laura_shower_seen")),
       flags=[fset("ate_dinner"), funset("room_tidy")], eff=[energy(15), warm(L, 3)]),
]
# Her text (phone.py laura_dinner, DECISIONS 87): "yes, starving" sets dinner_promised, so coming pays
# warmth +1 more and clears it (else the no-show text arrives). "eating out tonight" sets said_eating_out,
# read for 8 hours (the text comes 16:00-17:30, dinner ends 20:00); eating with her anyway is the lie
# she sees, suspicion +1. Conditions don't nest, so "not said, or said long ago" is two copies.
SAID_OUT = {"type": "hours_since_flag", "subject": "player", "flag_key": "said_eating_out", "operator": "lt", "value": 8}
SAID_OUT_OLD = dict(SAID_OUT, operator="gte")


def _with_items(c, items, eff=(), flags=()):
    d = json.loads(json.dumps(c))
    d["conditions"] = cond(*(d.get("conditions") or {}).get("items", []), *items)
    d["effects"] = list(d.get("effects", [])) + list(eff)
    d["flagEffects"] = list(d.get("flagEffects", [])) + list(flags)
    return d


_kept = []
for _c in DINNER_DONE:
    _yes, _no = booked_split(_c, "dinner_promised", eff=[warm(L)])
    _kept += [_yes,
              _with_items(_no, [flag("said_eating_out"), SAID_OUT], eff=[susp(1)], flags=[funset("said_eating_out")]),
              _with_items(_no, [flag("said_eating_out", False)]),
              _with_items(_no, [flag("said_eating_out"), SAID_OUT_OLD])]
DINNER_DONE = _kept
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
    # "You hand it back.": only with the twenty still on her, so the unclamped -20 never takes her below 0
    # (engine.md §21, "gate the choice on the trait"; pass 3 J5)
    go("\"I forgot the shopping.\"", node="hl_forgot", mins=2, cond_=cond(*OVERDUE, flag("grocery_done_today", False), trait("money", "gte", 20)),
       flags=[funset("grocery_list"), fset("grocery_done_today")], eff=[susp(2), add("money", -20, clamp=False)]),   # money is a quantity: never clamped (pass 4 J4/F73); the money gte 20 condition keeps it >= 0
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
# reader a3 #14 (DECISIONS 131): written from npc_laura.md (the tidy check row, was :96, now :158). The signed line's
# "The lace one." names a garment her catalog doesn't have (plain_panties only), so it says "panties".
# Sunday 18:00-20:00: Mark's Sunday row has him in the kitchen all day, Ryan only 18:00-19:00, so both are groups.
hub_nodes.append(node("hl_tidy_tease", "Your room", [
    ME("What did you see in my room, Mom?"),
    G(cond(here(M, K)), P("Laura looks down the table at Mark, and lowers her voice.")),
    D(L, "Your laundry was on the bed. The little things, right on top, where anybody could see them."),
    P("She says it into her wine, pink to the ears. Her eyes go down to your lap under the table, and come back up slowly."),
    D(L, "I folded them for you. I don't know why I'm telling you that."),
    T("She had your smallest things in her hands. She's still thinking about it."),
    D(L, "Eat your dinner, sweetheart."),
], [go("Done.", loc=K)]))
add_item("dinner", "Sit down to dinner.", HER_EVE + [tod("18:00", "20:00")], "ate_dinner", K,
         [G(cond(flag("dinner_promised")), D(L, "You came. Sit, sit. It's still hot.")),
          G(cond(flag("dinner_promised", False), flag("said_eating_out"), SAID_OUT),
            D(L, "I thought you were eating out."), P("She puts a plate down anyway, and watches you eat it.")),
          D(L, "How's college?"), P("She actually waits for the answer."), *AT_TABLE,
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
         after=("Chop for her.", [P("You chop until your eyes stream, and she leans past you to taste the sauce, her hip against yours and her hand flat on the small of your back."),
                                  D(L, "Better. You'll make somebody very happy one day.")], "Leave her to the stove."),
         tease=l_tease(89, "help her cook"), touch=l_touch(89, "help her cook", "Stay at the stove with her."))
add_item("dishes", "Do the dishes with her.", HER_EVE + [tod("19:00", "21:00")], "did_dishes", K,
         [D(L, "You wash, I dry."), P("Hip to hip at the sink.")],
         [energy(-5), warm(L)], 20, plain_costs=[{"trait": "energy", "value": 5}],
         after=("Wash up with her.", [P("You wash and she dries, her bare arm brushing yours every time she takes a plate. Suds run down to your elbows, and she flicks water at your neck when you hand one back dirty."),
                                      D(L, "Again, sweetheart. Properly.")], "Leave her the last pan."),
         tease=l_tease(90, "dishes"), touch=l_touch(90, "dishes"))
add_item("wine", "Have a glass with her.", HER_EVE + [tod("20:00", "22:00"), trait("laura_step", "gte", 2)], "had_drink_home", K,
         [G(cond({"type": "npc_at_location", "location_id": "home_kitchen", "npc_id": "npc_mark", "operator": "is_absent"}), D(L, "One glass. Don't tell Mark.")), G(cond({"type": "npc_at_location", "location_id": "home_kitchen", "npc_id": "npc_mark", "operator": "is_present"}), D(L, "One glass. Just the one.")),
          P("She pours two and clinks yours before you've picked it up.")],
         None, 30, done_exits=[go("Drink with her.", node="hl_wine_after", mins=30, eff=[warm(L)], flags=[fset("had_drink_home")], mods=DRINK)],
         tease=l_tease(91, "a glass of wine"), touch=l_touch(91, "a glass of wine"),
         after=("Drink with her.", [P("The wine goes warm in your stomach. She laughs with her head back at something you say, then reaches over and tucks your hair behind your ear, and leaves her hand on your cheek a second too long."),
                                    D(L, "Stay down here a while longer, okay?")], "Rinse your glass."))
# (pass 3 D1) the study is work, so it is its own canvas beside her hub, not a hub item (the-surfaces.md R1: "Never
# put work inside a character's hub"). Same screens, hours, pay and once-a-day flag; it still needs her in the
# kitchen, because she reads over your shoulder. Its Love pay shares her hub's once-a-day brake (below).
_study_door, _study_nodes = item("study", "Study at the kitchen table.", HER_EVE + [tod("19:00", "22:00")], "studied_home", K,
         [P("You spread your notes across the end of the table. Laura reads over your shoulder."), D(L, "That's wrong. No — that."),
          D(L, "Bring it down any night I'm in here after dinner, and I'll check it again.")],   # reader pass 3 b01: the hook names her, the place, the when
         None, 60, done_exits=[go(f"{name}.", loc=K, mins=60, flags=[fset("studied_home")],
                                  costs=[{"trait": "energy", "value": 10}],
                                  eff=[energy(-10), warm(L), {"targetType": "player", "trait": key, "op": "add", "value": 1, "cap": 100}])
                               for key, name in (("grade_psych", "Psychology"), ("grade_business", "Business"),
                                                 ("grade_bio", "Biology"), ("grade_art", "Figure drawing"))],
         )
STUDY_KITCHEN = {
    "id": "kitchen_study", "name": "Study at the kitchen table",
    "description": "Study at the kitchen table while Laura's there: 60 min, energy -10, one subject's grade +1, her Love (once a day with her hub). Work, so not in her hub (R1).",
    # DECISIONS 224: her own work with Laura only present (R1: work is never inside a hub), so a room link that
    # reads Laura's presence as a condition, not `requires_npc`, which the gate `a person's scene is inside their
    # portrait` reads as a scene done with her (engine_daygate_and_npc_canvas_limit, fix b)
    "trigger": {"location": K, "is_repeatable": True, "priority": 3, "is_active": True,
                "schedules": [{"weekdays": [0, 1, 3, 4, 6], "start_time": "19:00", "end_time": "22:00"}],
                "conditions": cond(flag("opening_done"), flag("studied_home", False),
                                   {"type": "npc_at_location", "location_id": K, "npc_id": L, "operator": "is_present"})},
    "nodes": _study_nodes}
# ── the towel at home (LO, 2026-10-31, DECISIONS 98): her reaction by her Love, every visit (<40, 40-69,
#    70+, her hub's own cut points); "Let her fix it." pays her Love +2 once a day. No Daring gate: it's a
#    mother fussing, not a tease. In her room only while she's up and dressing. ──
LAURA_TOWEL_WORDS = {
    "kitchen": dict(
        fix=[
            [P("You stand still. She tugs the towel straight and tucks the end in hard over your tits."), D(L, "There. Now go and put some clothes on.")],
            [P("She tucks the towel again over your tits, slower than she needs to, and smooths it flat with both hands."), D(L, "You've got my figure, you know.")],
            [P("She opens the towel to tuck it again. For a second your tits are bare between her hands, and she looks at them. Then she wraps it tight round you and smooths it down over your hips."), D(L, "There. Now you're decent.")],
        ],
        lines=[
            [D(L, "Go and get dressed, sweetheart. You'll catch your death."),
             D(L, "Clothes, please. This is a family house."),
             P("Laura looks at the towel and then at the door, like she's counting who could walk in.")],
            [GC(cond(TOWEL_ON), P("Laura tuts and tucks the towel tighter over your tits, like it's one more chore."), D(L, "You'll catch your death.")),
             D(L, "Dry your hair at least, sweetheart. You're dripping on my floor."),
             P("She looks you up and down, wet legs to wet hair, and smiles in a way you can't read.")],
            [GC(cond(TOWEL_ON), D(L, "Look at you. Where have you been hiding a body like that?"), P("She says it softly, and her eyes don't leave the towel.")),
             D(L, "One of my old dresses would look right on you, you know."),
             P("She pushes a wet strand of hair off your face and leaves her hand on your bare shoulder.")],
        ]),
    # Saturday night, the dark living room, her on the couch watching the front door
    "living": dict(
        fix=[
            [P("You stop in front of the couch. She leans forward, pulls the towel straight, and shoves the end in over your tits with two fingers."), D(L, "Now go and put something on before you get a chill.")],
            [P("She pulls you down by the towel and tucks it again over your tits, in no hurry, then flattens it with both hands in the dark."), D(L, "Who's looking at you these days, hm?")],
            [P("She opens the towel in the dark to tuck it. Your tits are bare a foot from her face, and she stares at them with her wine forgotten. Then she closes it tight and strokes it down over your hips."), D(L, "There, sweetheart. Go on, before I keep you up.")],
        ],
        lines=[
            [D(L, "You'll freeze, standing in the dark like that. Get something on, sweetheart."),
             D(L, "Anybody could come through that front door and see you."),
             P("Laura looks at the towel and then at the front door, the way she looks at everything tonight.")],
            [GC(cond(TOWEL_ON), P("Laura sets her glass down, reaches up from the couch, and hitches the towel higher over your tits."), D(L, "There. Stand there if you have to.")),
             D(L, "Sit down or go to bed, sweetheart. You're standing in my view."),
             P("She looks you over in the dark, bare feet to bare shoulders, and smiles at something she doesn't tell you.")],
            [GC(cond(TOWEL_ON), D(L, "Stand where I can see you. Who gets to look at you like that?"), P("She says it low, and her eyes stay on the towel.")),
             D(L, "I used to have legs like that, you know."),
             P("She reaches up from the couch and rests her warm hand on your bare shoulder, and she doesn't take it back.")],
        ]),
    # Saturday 17:00-18:30, her room, her at the long mirror in her slip
    "bedroom": dict(
        fix=[
            [P("You hold your arms out. She pulls the towel up and jams the end in hard over your tits, with the long mirror watching."), D(L, "Better. Now go and find some clothes.")],
            [P("She turns you to face the long mirror and tucks the towel over your tits, taking her time, and presses it flat with both palms."), D(L, "Now you look like somebody.")],
            [P("She undoes the towel in front of the long mirror to tuck it properly. Your tits are bare between her hands, and she looks at them in the glass. Then she pulls it snug and runs her palms down over your hips."), D(L, "There, sweetheart. Now you can go.")],
        ],
        lines=[
            [D(L, "I'm trying to get dressed, sweetheart. Go and put something on."),
             D(L, "Two of us half dressed in this room is plenty."),
             P("Laura looks at your towel in the mirror, then at her open door, and pushes it almost shut with her foot.")],
            [GC(cond(TOWEL_ON), P("Laura clicks her tongue at the mirror, turns round, and yanks the towel higher over your tits."), D(L, "You'll be sick by Monday.")),
             D(L, "Don't sit on my bed in that, sweetheart. I've got a dress laid out on it."),
             P("She looks you over in the mirror, bare feet to bare shoulders, and goes back to her two dresses with a small smile.")],
            [GC(cond(TOWEL_ON), D(L, "Stand next to me. Look at the two of us."), P("She says it quietly to the mirror, and her eyes go over your towel, not her own slip.")),
             D(L, "You could carry the green one better than I can."),
             P("She reaches across, hooks a strand of hair behind your ear, and her fingers stay on your bare neck.")],
        ]),
}


def laura_towel(hub, back, words, when=(), lines_when=()):
    w = LAURA_TOWEL_WORDS[words]
    return towel_set(
        hub, L, "warmth", 40, 70, "laura_towel_today", [warm(L, 2)], back, when=when,
        lines=w["lines"], lines_when=lines_when,
        slip=w["fix"], slip_label="Let her fix it.", slip_gate=())


LT_KITCHEN = laura_towel("hub_laura_kitchen", K, "kitchen")
UNIFORM_LINES = [
    G(cond(NORMAL_ON), D(L, "Look at you. My working girl. Sit, I'll make you something.")),
    G(cond(SEXY_ON), P("Laura looks at the open top button for a long second."), D(L, "Is that the uniform, or Tom's idea?")),
]
# ── (pass 3 C30) the failing chain: Laura reads the grades. One node per subject INSIDE her kitchen hub
# (the-first-hour.md, "a second surface for the same person in the same room is a NODE INSIDE THE FIRST").
# Until pass 3 these were four solo canvases laura_reads_<grade> in college.py beside this hub; no flag, gate or
# phone reads those ids. Only the first failing subject shows a door, so one button at a time; grades_seen
# (cleared at the Sunday count) keeps it to once a week, and laura_portal_today (cleared in [engine.daily_tick])
# is the day brake the canvases' max_triggers_per_day was, which a hub node has no trigger to carry (the-meters.md M3-M5).
PORTAL = [("grade_psych", "Psychology"), ("grade_business", "Business"), ("grade_bio", "Biology"), ("grade_art", "Figure drawing")]
portal_choices, portal_nodes = [], []
for _i, (grade, subj) in enumerate(PORTAL):
    _first_failing = [trait(g, "gte", 40) for g, _s in PORTAL[:_i]] + [trait(grade, "lt", 40)]
    # (pass 3 group 2, round 2; gate `the climb is paid for`) her sitting down is the moment: Laura's suspicion +5 and
    # the day brake ride this button, which reads the brake itself (a self-capped choice, the-meters.md M3-M5). Both
    # "I'll fix it." exits paid the same +5 before, so the pay is unchanged; their split now reads suspicion AFTER the
    # +5, so 45 became 50 (the same players are grounded). The exits keep no brake, so the screen always has a door.
    portal_choices.append(go("Sit with her. She has your grades up.", node=f"portal_{grade}", mins=0,
                             cond_=cond(wd(0, 1, 3, 4, 6), tod("18:00", "22:00"), flag("grades_seen", False),
                                        flag("laura_portal_today", False), *_first_failing),
                             eff=[add("laura_suspicion", 5)], flags=[fset("laura_portal_today")]))
    portal_nodes.append(node(f"portal_{grade}", "The portal", [
        P(f"Laura is at the kitchen table with her phone, and the college's portal open on it, and your {subj} grade in red. She turns the phone round so you can see it."),
        D(L, "Do you want to explain this to me, sweetheart?"),
        G(cond(flag("letter_home")), D(L, "After the letter. After the dean wrote to us.")),
    ], [
        go("\"I'll fix it.\"", loc="home_kitchen", mins=15, cond_=cond(ntrait(L, "warmth", "gte", 40), trait("laura_suspicion", "lt", 50)),
           flags=[fset("grades_seen"), fset("failing_noticed")]),
        go("\"I'll fix it.\"", node="portal_curfew", mins=5, cond_=cond(ntrait(L, "warmth", "lt", 40), trait("laura_suspicion", "gte", 50), logic="OR"),
           flags=[fset("grades_seen"), fset("failing_noticed")]),
    ]))
portal_nodes.append(node("portal_curfew", "Grounded", [
    D(L, "You'll fix it from this house, then. A week. No parties, no late shifts, no dates."),
], [go("\"Fine.\"", loc="home_kitchen", mins=10, flags=[fset("curfew")], eff=CURFEW_EFF)]))

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
            G(cond(tod("18:00", "19:00"), flag("ate_dinner", False)), D(L, "Dinner's on the table. Sit.")),   # reader 2026-11-04: Mark and Ryan are eating 18:00-19:00, and gone after
            G(cond(tod("06:30", "08:00"), flag("ate_breakfast", False)), D(L, "Eat something, sweetheart. You're not going to class on nothing.")),
            G(cond(tod("18:00", "22:00"), flag("college_for_grades")), D(L, "How are the grades? You said grades. I'm holding you to it.")),
            G(cond(tod("18:00", "22:00"), flag("college_for_fun")), D(L, "Having fun yet? You said fun. Don't have too much.")),
            G(cond(tod("18:00", "22:00"), flag("college_for_freedom")), D(L, "Freedom, you said, but you still live in my house, you know.")),
            dict(G(cond(wd(1), tod("18:00", "22:00"), trait("laura_step", "eq", 0)),
              P("She dries her hands on her apron and looks at you with a funny little smile."),
              D(L, "Come to my room after. I have something for you.")), release=2),   # DECISIONS 231: her invite buttons are release 2 (DECISIONS 230)
            # release 1: the leak before each of her four steps (npc_laura.md, "Leak and promise")
            G(cond(trait("laura_step", "eq", 1)), P("Her eyes go to you and stay a second too long. She keeps a second glass on the counter now.")),
            G(cond(trait("laura_step", "gte", 2), trait("ryan_step", "gte", 2)), D(L, "How's Ryan? You two seem close lately.")),
            G(cond(trait("laura_step", "gte", 1), flag("jake_date_booked")), D(L, "So Jake's taking you out? Where's he taking you?")),   # reader pass 3 b00: booked is set before any date, so no "again"
            G(cond(trait("laura_step", "eq", 2)), P("She's started leaving her bedroom door open when she dresses.")),
            G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), D(L, "Is that for college or for a guy?")),
            G(cond(DRESS_ON), D(L, "It never fit me like that."), P("Her hand smooths the hip of it without thinking.")),
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "worn_exposure", "operator": "eq", "value": 0}),
              P("Her eyes stop on your chest. Then she pours the coffee.")),
            *LT_KITCHEN[0],
            *UNIFORM_LINES,
            G(cond(*MADE_UP), D(L, "You did your face. Who's that for?")),
            G(cond(trait("hygiene", "lt", 30), flag("hygiene_off", False)), D(L, "Sweetheart. Shower. Today.")),
            G(cond(ntrait(L, "warmth", "lt", 30)), P("She's short with you. Everything you do lands wrong with her lately.")),
            G(cond(ntrait(L, "warmth", "gte", 70)), P("She touches your hair when she passes. She's on your side, whatever you've done.")),
        ], [
            *hub_choices,
            *portal_choices,
            *LT_KITCHEN[1],
            go("Talk to her.", node="talk", mins=20, cond_=cond(flag("laura_talk_today", False)),
               flags=[fset("laura_talk_today")],
               eff=[{"targetType": "npc", "npcId": L, "trait": "warmth", "op": "add", "value": 2, "cap": 100}]),
            # DECISIONS 230: her invite opens step 1 (the blue dress), which is release 2; both buttons ship with it
            dict(go("Follow her to her room.", loc="home_master_bedroom", mins=2, flags=[fset("laura_dress_invite")],
                    cond_=cond(wd(1), tod("18:00", "22:00"), trait("laura_step", "eq", 0))), release=2),
            # reader a3 #4 (DECISIONS 131): her invite gets a written no; it costs her Love -1
            dict(go("\"Not tonight, Mom.\"", node="not_tonight", mins=2, eff=[nadd(L, "warmth", -1)],
                    cond_=cond(wd(1), tod("18:00", "22:00"), trait("laura_step", "eq", 0))), release=2),
            go("Leave her to it.", loc="home_hall"),
        ]),
        node("talk", "Talk", [
            POOL(
                P("You sit on the counter and talk while she works. She asks about your classes, and you tell her the boring half."),
                P("She tells you about her office, the man who steals her yoghurt, the boss who calls everyone 'champ'. You make her laugh until she has to put down whatever's in her hand."),
                P("You lean on the counter beside her while she works. She hums. For a while it's just the two of you and it's easy."),
            ),
            G(cond(trait("hygiene", "lt", 30), flag("hygiene_off", False)),
              P("Halfway through she wrinkles her nose and steps back, and the easy goes out of it.")),
        ], [go("Leave her to her kitchen.", loc=K, mins=5)]),   # reader pass 3 b00: Talk opens at breakfast too, when nothing is being chopped   # pass 3 D39 (R7): the way out answers her
        # reader a3 #4 (DECISIONS 131): the no to "Come upstairs after." Every Tuesday at her step 0 she asks again.
        node("not_tonight", "Not tonight", [
            ME("Not tonight, Mom."),
            P("The funny little smile goes. She turns back to the stove and stirs something that doesn't need it."),
            D(L, "Oh. Okay, sweetheart. It'll keep."),
        ], [go("Leave her to the stove.", loc="home_hall", mins=2)]),
        *hub_nodes,
        *portal_nodes,
        *LT_KITCHEN[2],
    ]})

# ── waiting up on Saturday nights, in the dark living room: a film or the TV with her ──
lr_choices, lr_nodes = [], []
for args, kw in [
    (("film", "Watch the film with her.", [tod("22:00", "00:00")], "movie_night", "home_living_room",
      [P("A film on low, the only light in the room."), D(L, "Sit with me a while.")],
      [energy(5), warm(L, 2)], 120),
     dict(tease=l_tease(92, "movie night"), touch=l_touch(92, "movie night", "Stay under the blanket with her."),
          after=("Watch it with her.", [P("Halfway through she pulls the blanket over both of you. By the end her head is on your shoulder and her hand is resting on your knee, warm, forgotten there."),
                                        D(L, "Don't tell Mark I cried.")], "Say goodnight and go.", "home_hall"))),
    (("tv", "Watch TV with her.", [tod("22:00", "00:00")], "watched_tv", "home_living_room",
      [P("She hands you the remote without looking away from the door."), D(L, "Find something. Anything.")],
      [energy(5), warm(L)], 60),
     # the written no: her offer gets her daughter's words and her reply; free of every cap and cost
     dict(no=([ME("Not tonight, Mom. You pick."), D(L, "Go on, then, sweetheart. I'll be here."),
               P("She takes the remote back and doesn't turn it on. Her eyes are already on the front door again.")], "Leave her the remote."))),
]:
    c, n = item(*args, **kw); lr_choices += c; lr_nodes += n
# reader pass 3 b01 (the written no): her "Sit with me a while." gets a spoken no and her reaction, not a bare exit
for _n in lr_nodes:
    if _n["id"] == "hl_film":
        for _c in _n["choices"]:
            if _c.get("text") == "Not now.":
                _c.pop("locationId", None)
                _c.update(go("Not now.", node="hl_film_no"))
lr_nodes.append(node("hl_film_no", "Not now", [
    ME("Not now, Mom. I'm going to my room."),
    D(L, "Oh. No, of course. Go on, sweetheart. I'll just watch the door."),
    P("She pulls her robe tighter over her knees and turns back to the film, and she doesn't turn the sound up."),
], [go("Go to your room.", loc="home_ella_room")]))
LT_LIVING = laura_towel("hub_laura_living_room", "home_living_room", "living")
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
            G(cond(trait("jake_step", "gte", 3)), D(L, "I saw you, you know. On the step. I didn't look away.")),
            *LT_LIVING[0],
        ], [*lr_choices, *LT_LIVING[1], go("Leave her be.", node="leave")]),
        # the written no: "Sit with me" gets her words and Laura's reply, not a bare exit
        node("leave", "Goodnight", [
            ME("I'm done for tonight, Mom."),
            D(L, "Goodnight, sweetheart. I'll hear you if you go back out."),
            P("She lifts the wine she isn't drinking, a small toast, and her eyes go straight back to the front door."),
        ], [go("Leave her be.", loc="home_hall")]),
        *lr_nodes, *LT_LIVING[2],
    ]})

# ── their room: Laura dressing on Saturday evenings (her hair), or asleep at night ──
DRESSING = [wd(5), tod("17:00", "18:30")]
bd_choices, bd_nodes = item("hair", "Let her do your hair.", DRESSING, "made_up_today", "home_master_bedroom",
    [P("She sits you down at her mirror and brushes your hair out, long strokes."), D(L, "You had my hair at your age.")],
    [warm(L)], 20,
    done_exits=[go("Done.", loc="home_master_bedroom", mins=20, eff=[warm(L)], flags=[fset("made_up_today"), fset("made_up")])],
    # reader 2026-11-04: the written no to the brush; it costs nothing
    no=([ME("Not now, Mom. Leave it."), D(L, "Suit yourself, sweetheart. It's your head."),
         P("She shrugs at you in the glass and goes back to her own hair with the brush.")], "Leave her to it."),
    )
# Sun 00:00-01:00 Mark and Laura are awake (DECISIONS 80): the "asleep" line skips that hour, written
# once per piece of the night because conditions do not nest.
ASLEEP_HOURS = [(wd(0, 1, 2, 3, 4, 5), tod("22:00", "07:00")), (wd(6), tod("22:00", "00:00")), (wd(6), tod("01:00", "07:00"))]
# Laura is awake and alone Sun-Fri 22:00-23:00 (DECISIONS 82), so a line saying she is asleep skips that hour too.
LAURA_ASLEEP_HOURS = [(wd(0, 1, 2, 3, 4), tod("23:30", "07:00")), (wd(5), tod("22:00", "07:00")), (wd(6), tod("23:30", "00:00")), (wd(6), tod("01:00", "07:00"))]   # bedtime 23:30 (LO, 2026-11-09)
LT_BED = laura_towel("hub_laura_bedroom", "home_master_bedroom", "bedroom", when=DRESSING,
                     lines_when=[flag("laura_dress_chosen", False)])   # the lines have her in her slip, choosing; chosen, she's in the green
out.append({
    "id": "hub_laura_bedroom", "name": "Laura",
    "description": "Laura in her room: dressing on Saturday evenings with the door open (her hair, home_life item 12), or asleep at night (her face; home_master_bedroom.md:36-45).",
    "trigger": {"location": "home_master_bedroom", "npc": L, "requires_npc": L, "is_repeatable": True,
                "priority": 6, "is_active": True, "conditions": cond(flag("opening_done"))},
    "nodes": [
        node("mirror", "Laura", [
            # scene reader 2026-11-04: once the green is chosen the choice is over for the day (laura_dress_chosen)
            G(cond(*DRESSING, flag("laura_dress_chosen")),
              P("Laura's in the green now, at the long mirror, doing her earrings."),
              D(L, "It's the green, sweetheart. Go on, I've got it from here.")),
            G(cond(*DRESSING, flag("laura_dress_chosen", False)),
              P("Laura is at her long mirror in her slip, holding two dresses up one after the other."),
              POOL(D(L, "Black or green? Mark won't notice either way."),
                   D(L, "Do I look old in this? Be honest. No, don't be honest."),
                   D(L, "Hand me those earrings, sweetheart."))),
            G(cond(*DRESSING, flag("laura_dress_chosen", False), trait("laura_step", "gte", 3)), P("She lifts her hair off her neck and turns her back to you without asking. Whichever dress wins, she knows you'll do the zip.")),
            G(cond(*DRESSING, flag("laura_dress_chosen", False), trait("laura_step", "lt", 3)), P("She catches you watching her in the mirror, and holds it.")),
            *[G(cond(*hrs),
                P("Laura's asleep on her side, curled toward the wall, one bare shoulder out of the covers. She doesn't stir."))
              for hrs in LAURA_ASLEEP_HOURS],
            # reader 2026-11-04: her awake rows outside DRESSING and outside the asleep hours, so the screen is never empty
            G(cond(wd(0, 1, 2, 3, 4, 6), tod("22:00", "23:30")),
              P("Laura's on the edge of the bed in her nightdress, wide awake, the lamp on low and a book open on her knees that she isn't reading."),
              D(L, "It's late, sweetheart. Go on to bed.")),
            G(cond(wd(5), tod("18:30", "19:00")),
              P("Laura has her earrings in and her bag on the bed. She looks you over once in the long mirror and picks up her keys."),
              D(L, "I'm late. Whatever it is, it can wait till tomorrow, sweetheart.")),
            G(cond(wd(6), tod("00:00", "01:00")),
              P("The lamp's on. Laura's on the edge of the bed in her nightdress, taking her earrings out."),
              D(L, "Not now, sweetheart. Go to bed.")),
            *LT_BED[0],
        ], [*bd_choices, *LT_BED[1],
            go("Help her choose.", node="choose", mins=20, cond_=cond(*DRESSING, flag("laura_dress_chosen", False)), flags=[fset("laura_dress_chosen")]),
            go("Back out.", loc="home_hall")]),
        node("choose", "Black or green", [
            P("You make her try both. Then the black again. She turns side to side in the mirror while you tell her the truth: the green."),
            D(L, "The green it is. Don't tell Mark it was your idea."),
        ], [go("Leave her to finish.", loc="home_hall")]),
        *bd_nodes, *LT_BED[2],
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
            # scene reader b03 (2026-11-03): the call rings wherever she is, her own room too, and no condition reads where
            # the player is (the kitchen with Laura too), so it never says she is away or tells her to come home
            D(L, "You know the rule, sweetheart. No parties, no late shifts, no dates."),
        ], [go("\"I know. Not this week.\"", node="good", mins=2, flags=[fset("laura_call_today")]),
            go("\"You can't ground me forever.\"", node="talk", mins=2, eff=[susp(2)], flags=[fset("laura_call_today")],
               cond_=cond(flag("laura_call_today", False)))]),
        node("good", "The rule", [D(L, "That's all I wanted to hear, sweetheart.")], [go("Hang up.", ret=True)]),
        node("talk", "We'll talk", [D(L, "We'll talk about this."), P("She hangs up before you can answer.")], [go("Put the phone away.", ret=True)]),
    ]})

# ── step 4 · She saw you (laura_04_she_saw_you.md, signed 2026-11-01): reached only through her door, "The door's
#    ajar." (world_data.py), in her alone-in-bed hour, once she has watched three times. ──
from sheetbeats import beat
_t4 = step_trigger(L, 4, bind_npc=False)
_t4["substitution_only"] = True
# reader a3 verify (DECISIONS 131): "Laura's door ... again" and her "Ryan." need her bedroom door seen first, not only the shower
_t4["conditions"]["items"].append(flag("laura_alone_seen"))
DONE4_EFF = [nadd(L, "warmth", 5), setv("laura_step", 4)]
DONE4_FLAGS = [fset("laura_04_done"), fset("laura_said_ryan"), fset("saw_laura_alone"), fset("laura_alone_seen")]
out.append({
    "id": "laura_04_she_saw_you", "name": "Watch Laura touch herself",   # pass 3 H33/H34 (the-voice.md R1, D11): the name says what happens if she clicks, and never hides the act
    "description": "Laura step 4 of 4, the top step (release 1): through the gap Laura comes, whispering \"Ryan.\", and her eyes open on Ella. \"Go to bed, sweetheart.\" Sets laura_said_ryan; breakfast follows.",
    "trigger": _t4,
    "nodes": [
        node("gap", "Laura's door, again", [P(beat("laura_04_she_saw_you", "gap")),
            VID("through a bedroom door left ajar, a woman alone in bed fingering herself, biting her hand", "mom masturbating seen through door gap", "woman fingering herself bed door ajar biting hand", pool_dir="sex/laura_04_gap_t5"),
            D(L, "Oh. Oh God. Please. Please."),   # pass 3 B4: to herself, under her breath
            ],
            [go("Keep watching.", node="comes", mins=5, flags=[fset("saw_laura_alone"), fset("laura_alone_seen")]),
             go("Pull the door to.", loc="home_hall", mins=2, retry=1, flags=[fset("saw_laura_alone"), fset("laura_alone_seen")])]),
        node("comes", "Ryan", [P(beat("laura_04_she_saw_you", "comes")),
            VID("a woman alone in bed coming hard, biting her knuckles, whispering a name", "woman orgasm in bed whispering a name", "mom cums biting hand bed", pool_dir="sex/laura_04_comes_t5")],
            [go("Stay where you are.", node="eyes", mins=2,
                eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 59}, add("laura_gaps_watched", 1, clamp=False)])]),
        node("eyes", "Her eyes", [
            P("Laura's eyes open. They go straight to the door. To the gap. To you."),
            P("She doesn't pull the sheet up fast. She doesn't pull it up at all. She lies there with her hand still between her legs, and she looks at you."),
            D(L, "How long have you been standing there?"),
            *at_level("corruption", {
                20: "Mom. I'm sorry. I didn't.",
                40: "Long enough, Mom. I'm not going to say sorry.",
                60: "Since before you came, Mom. I saw all of it, and I didn't want it to stop."}, make=ME),
            T("Ryan. She said Ryan. Not Mark."),
        ], [
            go("Step back from the gap.", node="back", mins=1),
            go("Stay where she can see you.", node="stay", mins=1, cond_=cond(trait("corruption", "gte", 20))),
        ]),
        node("back", "Go to bed", [
            P("You step back into the dark of the hall. Your heart is going so hard you can hear it."),
            D(L, "Go to bed, sweetheart."),
            P("She says it quietly, through the gap."), ME("Night, Mom."), D(L, "And shut the door all the way this time."),
        ], [go("Back to your room.", loc="home_ella_room", mins=3, consumes=True, eff=DONE4_EFF, flags=DONE4_FLAGS)]),
        node("stay", "Let her see you", [
            P("You don't move. You let her see you."),
            P("Laura holds your eyes for a long second. Her face doesn't change."),
            ME("You said his name."),
            D(L, "I know what I said. Go to bed, sweetheart."),
            P("She reaches out and turns off the lamp."),
        ], [go("Back to your room.", loc="home_ella_room", mins=3, consumes=True, eff=DONE4_EFF, flags=DONE4_FLAGS)]),
    ]})

# ── the breakfast after (laura_04_she_saw_you.md, "Breakfast, next morning"): her next weekday breakfast, once.
#    "last night" only when step 4 was under 12 hours ago; after a Friday night her breakfast is Monday. ──
SINCE4 = lambda op, h: {"type": "hours_since_flag", "subject": "player", "flag_key": "laura_04_done", "operator": op, "value": h}
out.append({
    "id": "laura_04_breakfast", "name": "We don't talk about it",
    "description": "The morning after Laura's step 4 (her next weekday breakfast): \"We don't talk about last night.\" Once.",
    "trigger": {"location": K, "npc": L, "requires_npc": L, "is_repeatable": False, "priority": 9, "is_active": True,
                "schedules": [{"weekdays": [0, 1, 2, 3, 4], "start_time": "06:30", "end_time": "08:00"}],
                "conditions": cond(flag("laura_04_done"))},
    "nodes": [node("table", "Breakfast", [
        P("Laura is at the counter in her robe, pouring two coffees. She puts yours down in front of you and doesn't look up."),
        G(cond(SINCE4("lt", 12)), D(L, "We don't talk about last night.")),
        G(cond(SINCE4("gte", 12)), D(L, "We don't talk about the other night.")),
        T("Tonight her door will be open a gap again. You both know it."),
    ], [
        go("\"Okay, Mom.\"", loc=K, mins=10, eff=[nadd(L, "warmth", 5)], flags=[fset("laura_04_breakfast_done")]),
        go("\"You should talk to Mark.\"", node="mark", mins=2),
    ]),
    node("mark", "Eat your toast", [
        P("She laughs, once, without anything in it."),
        D(L, "Eat your toast, sweetheart."),
    ], [go("Eat your toast.", loc=K, mins=10, eff=[add("laura_suspicion", -5) | {"clamp": True}, nadd(L, "warmth", 2)], flags=[fset("laura_04_breakfast_done")])])]})

cards = step_cards(L, {
    1: ("Laura has a dress for you in her room. She said so on Tuesday.", "Tuesday evening: find Laura in the kitchen, then go to her room"),
    2: ("She keeps a second glass poured in the evenings.", "Find Laura in the kitchen late in the evening"),
    3: ("She leaves her door open now, while she dresses.", "Saturday early evening: Laura's room, while she dresses"),
    4: ("Her door is open a gap on weeknights. You keep going back to it.", "A weeknight, late: Laura's door (Curious)"),
}, terminal_text=("She knows you watch. Her door is still open a gap.", "Whether the gap gets wider is the next release."),
   closed_text="She's your mom. That's all she is now, and she punishes every catch.")
for c in cards:
    if "when" in c and not any(w.get("flag") == "opening_done" for w in c["when"]):
        c["when"].append({"flag": "opening_done", "op": "is_true"})

# ── her plain items pay Love +2, once a day in total (one brake across all of them, `laura_love_today`) ──
def _love_once_a_day(canvas):
    for nd in canvas["nodes"]:
        new = []
        for ch in nd.get("choices", []):
            effs = ch.get("effects") or []
            hit = [e for e in effs if e.get("targetType") == "npc" and e.get("npcId") == L and e.get("trait") == "warmth"
                   and isinstance(e.get("value"), (int, float)) and e["value"] > 0]
            if not hit:
                new.append(ch); continue
            items = list((ch.get("conditions") or {}).get("items") or [])
            assert (ch.get("conditions") or {}).get("logic", "AND") == "AND", ch["text"]
            paid = dict(ch, effects=[dict(e, value=2) if e in hit else e for e in effs],
                        conditions=cond(*items, flag("laura_love_today", False)),
                        flagEffects=list(ch.get("flagEffects") or []) + [fset("laura_love_today")])
            free = dict(ch, effects=[e for e in effs if e not in hit] or None,
                        conditions=cond(*items, flag("laura_love_today")))
            if not free["effects"]:
                free.pop("effects")
            new += [paid, free]
        nd["choices"] = new
out.append(STUDY_KITCHEN)
for _c in out:
    if _c["id"] in ("hub_laura_kitchen", "hub_laura_living_room", "hub_laura_bedroom", "kitchen_study"):
        _love_once_a_day(_c)

text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · LAURA (sheets/scenes/laura_0*.md, sheets/people/npc_laura.md)\n"
        "# Steps 1-8 (step 5 is also Jake's step 4), the catch, her hubs, the curfew call, her cards.\n"
        "# =============================================================================\n")
# Iteration 002, part 3: leaving this outing after 22:00 sets late_date and came_home_late (Q69,
# the street sheet "Why she's late"; canv.mark_late). Each is read for 4 hours; her bed clears them.
import everyday   # DECISIONS 221: the day after an everyday scene, the hub remembers it
everyday.hub_read(out)
text += "".join(emit(c) for c in out) + "".join(emit_card(c) for c in cards)
open(__import__("sys").argv[1], "w").write(text)
print("laura:", len(out), "canvases,", len(cards), "cards")
