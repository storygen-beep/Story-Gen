"""The sex scenes in the cold places (heat proposal 2026-11-03, A1-A7; DECISIONS 147, chunk 2).

A1 the gym (Jake), A2 the canteen (Zoe), A3 the quad (Jake and his team), A5 Zoe's bedroom (Zoe) are NODES inside
that person's existing hub, not canvases beside it: the hub already owns the face and the window (the-first-hour.md
F5b, one repeatable canvas per person per window), so attach_jake() / attach_zoe() add one button to the hub's first
screen and the screens behind it. A6 Zoe's kitchen (the keg guy) and A7 Zoe's bathroom (Jake at the party) are solo
canvases, TOWN_CANVASES, emitted by town.py with Zoe's other rooms. A4 (the changing room) is hand-written TOML in
3_activities.toml, beside shop_try_on's own nodes.

The shape of every one (the-surfaces.md, the-heat-ladder.md H5):
- the hub button opens an offer screen: the person speaks, she thinks, and her answers are the stage-gated yes
  buttons and a written no;
- every act screen is a shuffle bag of explicit beats (POOL bag=True) and a clip behind it (VID, pool_dir only;
  no harvest is run here: the folders render their fallback until LO runs one);
- the pay is +1 capped at the top of the stage the act opens at (59 Bold, 79 Hungry or Watched), on the button
  into the act (pass 3 G74: before, it rode one of two exits, so the pay hung on the exit label), day-capped on
  that button: it reads `<x>_today` is_false and sets it, and [engine.daily_tick] clears it (gates.py
  _holder_day_capped). The same button costs 10 energy and lowers hygiene 10 (pass 3 E95, D18). Both exits after
  the act pay nothing (a spent day still has a door);
- the no pays 0 to everyone. Jake and Zoe have no Want meter, so no act moves a meter of theirs.

Timing (the truth rule): the offer and act screens move the clock 0 minutes; the time is on the exit. Each hub
button closes 15 minutes before its person's row ends, so every line naming them renders inside their row.
"""
from canv import *
from tomlw import tod, wd

J, Z, N = "npc_jake", "npc_zoe", "npc_nadia"
BOLD = trait("corruption", "gte", 40)
HUNGRY = trait("corruption", "gte", 60)
WATCHED = trait("exhibitionism", "gte", 60)
SKIRT = {"type": "worn_type", "operator": "eq", "value": "short_skirt"}
ANY = {"type": "worn_exposure", "operator": "gte", "value": 0}          # always true: a chain's else
AT_PARTY = {"type": "hours_since_flag", "subject": "player", "flag_key": "party_went", "operator": "lt", "value": 8}

DAILY_FLAGS = []    # every brake flag here, for 0_systems_spec.toml [engine.daily_tick]


def today(key):
    DAILY_FLAGS.append(key)
    return key


def pay(meter, cap):
    return {"targetType": "player", "trait": meter, "op": "add", "value": 1, "cap": cap}


# What a sex act takes from her body (board.needs, v2_state.json: energy is "spent ... sex scenes take it through
# costs", hygiene "falls faster after ... sex"; the-meters.md M8, M10; pass 3 E95). The energy cost is also the rung's
# floor with its refusal line: a priced exit-block choice stays on screen greyed, "Requires 10 Energy (you have 6)",
# so a tired day throttles the act (the-surfaces.md R3c; engine.md §27; pass 3 D18).
ACT_COSTS = [{"trait": "energy", "value": 10}]
ACT_HYGIENE = {"targetType": "player", "trait": "hygiene", "op": "add", "value": -10, "clamp": True}


def act_exits(label, loc, mins, brake, eff, plain, plain_loc=None, also=()):
    """The act's two exits. Both pay nothing: the act pays, on the button into it (pay_on_the_way_in), so the same
    act pays the same whichever door she takes out (the-heat-ladder.md H5, "the exit that leads into the screen
    where it happens"; pass 3 G74). The marker carries the pay and the day brake to that button."""
    exits = [go(label, loc=loc, mins=mins, flags=[fset(f) for f in also] or None),
             go(plain, loc=plain_loc or loc, mins=mins, flags=[fset(f) for f in also] or None)]
    exits[0]["_act"] = (eff, brake)
    return exits


def pay_on_the_way_in(nodes):
    """Move each act's pay and day brake onto every button into its screen: the button reads the brake is_false
    (it already does) and now sets it and pays, so it is day-capped on itself (gates.py _holder_day_capped); it
    also costs energy and lowers hygiene (ACT_COSTS, ACT_HYGIENE)."""
    acts = {}
    for n in nodes:
        for c in n["choices"]:
            if "_act" in c:
                acts[n["id"]] = c.pop("_act")
    for n in nodes:
        for c in n["choices"]:
            if c.get("targetType") == "node" and c.get("nodeId") in acts:
                eff, brake = acts[c["nodeId"]]
                assert flag(brake, False) in c["conditions"]["items"], (n["id"], c["text"])
                c["effects"] = list(eff) + [ACT_HYGIENE]
                c["flagEffects"] = [fset(brake)]
                c["costs"] = list(ACT_COSTS)
    return nodes


def bag(pid, *beats):
    return POOL(*[P(b) for b in beats], pid=pid, bag=True)


def _canvas(out, cid):
    return next(c for c in out if c["id"] == cid)


def _add_button(canvas, button, nodes):
    """Put the hub button above the hub's last choice (its exit) and add the screens behind it."""
    first = canvas["nodes"][0]
    first["choices"].insert(len(first["choices"]) - 1, button)
    canvas["nodes"] += nodes


# ═════════════════════════════════════════════════════════════════════════════
# A1 · THE GYM · Jake (hub_jake_gym, his Tue/Thu 15:00-17:00 row). After training, after jake_first_time.
# Bold: her hand, then her mouth (cap 59). Hungry: he fucks her against the lockers, the team's showers through
# the wall (cap 79). His columns: Bold = his middle (ass, tits, cock), Hungry = his late (cock, fuck, cum).
# ═════════════════════════════════════════════════════════════════════════════
LOCKERS = today("jake_lockers_today")
LOCKERS_FREE = flag(LOCKERS, False)

A1_MOUTH = (
    "Jake kicks the locker-room door shut behind you. You push him back against the lockers and drop to your knees "
    "on the wet tiles. You tug his shorts down, and his cock springs out, hard and flushed. You wrap your fist round "
    "the base and lick the head, slow, so he has to watch. He thumps his head back on the metal. Then you suck him in "
    "deep, your hand pumping what your mouth can't take. The showers hiss on the other side of the wall. His hips jerk, "
    "and his cock throbs hot on your tongue.",
    "The door hasn't swung shut before your hand is inside his shorts. His cock is hot and heavy in your fist, slick "
    "with sweat. You stroke him slow, but he's already leaking, so you drop to your knees and take him in your mouth. "
    "He grabs the top of a locker with both hands. You suck harder, your cheeks hollow, your spit running down to your "
    "fist. His thighs shake. He comes in your mouth with a grunt he can't keep in. You swallow all of it, then lick "
    "his cock clean.",
)
A1_LOCKERS = (
    "Jake spins you round and pushes you face-first into the lockers. The metal is cold on your tits. He shoves "
    "everything you're wearing out of his way and kicks your feet apart. His cock slides along your ass, then into you "
    "in one hard thrust. He fucks you hard and fast, one hand over your mouth, the other gripping your hip. The locker "
    "doors bang with every stroke. Through the wall the team laughs at something. He slams in to the hilt, and his cum "
    "floods into you.",
    "Jake lifts you up against the lockers like you weigh nothing. Your clothes are in a heap on the bench. Your legs "
    "lock round his waist, and his cock pushes up into you, thick, stretching you open. He holds you pinned to the metal "
    "and fucks you in short, hard strokes that rattle every door down the row. Somebody shouts his name from the "
    "showers. He doesn't answer. He buries his face in your tits and fucks you harder, until you clench round his cock "
    "and come. He groans, and his cum spills hot inside you.",
)
NEXT_GYM = [G(cond(wd(1)), D(J, "Thursday. Same time. Don't you dare say no.")),
            G(cond(wd(3)), D(J, "Tuesday. Same time. Don't you dare say no."))]

A1_BUTTON = go("Wait for him after training.", node="a1_offer", mins=0,
               cond_=cond(flag("jake_first_time"), BOLD, LOCKERS_FREE, tod("16:30", "16:45")))
A1_NODES = [
    node("a1_offer", "After training", [
        P("Training ends. The team drifts off to the showers, loud, towels over their shoulders. Jake hangs back by the "
          "locker-room door, and the sweat is still running down his neck."),
        D(J, "Locker room's empty for ten minutes. Get in here, @player."),
        T("Ten minutes, and his whole team on the other side of one wall. You want it more because of that."),
    ], [
        go("Get on your knees.", node="a1_mouth", mins=0, cond_=cond(BOLD, LOCKERS_FREE)),
        go("\"Against the lockers.\"", node="a1_lockers", mins=0, cond_=cond(HUNGRY, LOCKERS_FREE)),
        go("\"Not here, Jake.\"", node="a1_no", mins=0),
    ]),
    node("a1_mouth", "On your knees", [
        bag("jake_lockers_mouth", *A1_MOUTH),
        VID("a girl on her knees on a wet locker-room floor sucking an athlete's cock, his back to the lockers",
            "blowjob locker room on knees", "girlfriend sucks athlete after practice locker room",
            pool_dir="sex/jake_lockers_mouth_t5"),
        D(J, "Jesus, @player. Coach is going to smell you on me."),
        T("His whole team was through that wall. That was the best part."),
        *NEXT_GYM,
    ], act_exits("Wipe your mouth. Go.", "campus", 15, LOCKERS, [pay("corruption", 59)], "Leave him to his shower.")),
    node("a1_lockers", "Against the lockers", [
        bag("jake_lockers_fuck", *A1_LOCKERS),
        VID("an athlete fucking his girlfriend against the lockers in an empty locker room, showers running next door",
            "fucked against lockers locker room", "athlete fucks girlfriend locker room after practice",
            pool_dir="sex/jake_lockers_fuck_t5"),
        D(J, "If Coach walks in, I'm telling him it was your idea."),
        T("You'd let him fuck you in front of the whole team. You know that now."),
        *NEXT_GYM,
    ], act_exits("Go, before Coach comes.", "campus", 15, LOCKERS, [pay("corruption", 79)], "Leave him to his shower.")),
    node("a1_no", "Not here", [
        D(J, "Later, then. When Coach isn't next door."),
        P("He grins, slaps the door frame and jogs off after the team. Through the wall they whistle at him."),
    ], [go("\"Later.\"", loc="campus", mins=2)]),   # pass 3 reader: "Saturday." booked nothing; dates book on his phone thread   # pass 3 D39 (the-surfaces.md R7): the way out answers him
]

# ═════════════════════════════════════════════════════════════════════════════
# A3 · THE QUAD · Jake and his team (hub_jake_quad, his Mon/Wed/Fri 08:30-11:45 row). After jake_first_time, in
# the skirt. A group sees: Watched. Showing yes, his hand up her skirt (Exhibitionism, cap 79); doing yes, his
# fingers in her, mixed (both meters at 60, both +1, cap 79). His late column (stage 4).
# ═════════════════════════════════════════════════════════════════════════════
QUAD = today("jake_quad_today")
QUAD_FREE = flag(QUAD, False)

A3_SHOW = ("His hand slides up under your skirt and lifts the hem with his wrist, so the whole team gets a look. His "
           "palm is on your ass, out in the open air, squeezing. Four guys stop talking. One of them forgets his drink "
           "halfway to his mouth. Jake runs his thumb slow along the crease of your ass while they stare. His other "
           "hand cups your tits. Under your thigh his cock is hard, pressing up through his jeans.")
A3_DO = ("Jake's hand stays under your skirt. His fingers slide between your legs from behind and push into you, two "
         "of them, deep, right there on the grass. The team can see his wrist working. You grind down on his hand and "
         "moan into his neck. He fucks you with his fingers, slow and then fast, his thumb pressed up against your ass. "
         "His cock throbs under you. You come on his fingers with your face in his shoulder, your thighs shaking where "
         "everyone can see them.")

# A public act feeds the audience meter like the other public acts (the-meters.md W5b; SYSTEMS.md campus_talk, "the
# public class moments"; pass 3 E94): campus_talk +1 on either yes, day-capped with the pay, and the team's witness
# flag (one NPC flag per thing a person saw, as the walk-ins record team_saw_gym / _canteen / _grass).
TALK = add("campus_talk", 1, clamp=False)

A3_BUTTON = go("Sit in his lap.", node="a3_offer", mins=0,
               cond_=cond(flag("jake_first_time"), SKIRT, WATCHED, QUAD_FREE, tod("08:30", "11:30")))
A3_NODES = [
    node("a3_offer", "His lap", [
        P("Jake pulls you down into his lap on the grass, sideways, right in front of the team. His hand settles on "
          "your bare thigh, just under the hem of your skirt."),
        D(J, "Forget later. Guys. Look at her."),
        P("Four of them look. None of them looks away."),
        T("He wants them to see what's his. You want them to see more than that."),
    ], [
        go("Let him show them.", node="a3_show", mins=0, cond_=cond(WATCHED, SKIRT, QUAD_FREE)),   # SKIRT backs "your skirt" behind it
        go("Let him in.", node="a3_do", mins=0, cond_=cond(WATCHED, HUNGRY, SKIRT, QUAD_FREE)),
        go("\"Not in front of them.\"", node="a3_no", mins=0),
    ]),
    node("a3_show", "For the team", [
        P(A3_SHOW),
        VID("a guy on the grass lifting his girlfriend's skirt over her bare ass for his friends to see",
            "boyfriend shows off girlfriend's ass in public", "lifts her skirt on campus lawn friends watching",
            pool_dir="sex/jake_quad_show_t4"),
        WHO("Jesus, Jake."),
        D(J, "Told you. Mine."),
        T("The whole quad could see your ass, but you didn't pull the hem down."),
    ], act_exits("Get up off his lap.", "quad", 20, QUAD, [pay("exhibitionism", 79), TALK], "Leave him to the guys.", plain_loc="campus",
                 also=["team_saw_quad"])),
    node("a3_do", "In front of them", [
        P(A3_DO),
        VID("a guy fingering his girlfriend in his lap on a college lawn, his friends watching",
            "fingered in public on the grass", "boyfriend fingers girlfriend in front of friends outdoors",
            pool_dir="sex/jake_quad_do_t5"),
        WHO("Jesus Christ, man."),
        D(J, "All mine, guys. Look all you want."),
        T("Half the team just watched you come. Your face is burning, and you'd let him do it again."),
    ], act_exits("Get up off his lap.", "quad", 20, QUAD, [pay("corruption", 79), pay("exhibitionism", 79), TALK], "Leave him to the guys.",
                 plain_loc="campus", also=["team_saw_quad"])),
    # reader batch 5 (pass 3): "Saturday." booked nothing (dates book on his phone thread, phone.py jake_date /
    # jake_date_wed, and a booking made here could bring him to the door on a Wednesday), so neither line names a day
    node("a3_no", "Not in front of them", [
        D(J, "Later, then. When it's just us."),
        P("He lets you up, grinning, and the team jeers at him while you walk off across the grass."),
    ], [go("\"Later.\"", loc="campus", mins=2)]),
]


pay_on_the_way_in(A1_NODES)
pay_on_the_way_in(A3_NODES)


def attach_jake(out):
    _add_button(_canvas(out, "hub_jake_gym"), A1_BUTTON, A1_NODES)
    _add_button(_canvas(out, "hub_jake_quad"), A3_BUTTON, A3_NODES)


# ═════════════════════════════════════════════════════════════════════════════
# A2 · THE CANTEEN · Zoe (hub_zoe_canteen, her Mon-Fri 11:45-13:00 row). After zoe_together, in the skirt. The
# table could see: Hungry (cap 79). Nadia talks across the table when her row has her there and they have met.
# Zoe's late column (pussy, clit, fuck).
# ═════════════════════════════════════════════════════════════════════════════
TABLE = today("zoe_table_today")
TABLE_FREE = flag(TABLE, False)
NADIA_HERE = [here_at(N, "canteen"), flag("nadia_met")]

A2_FINGERS = (
    "Zoe keeps eating fries with her left hand. Her right slides up your thigh and under your skirt. She finds your "
    "clit first and rubs it in slow, lazy circles until you're soaking. Then two fingers push into your pussy, deep, "
    "and curl. You grip the edge of the table. Zoe fucks you with her fingers in time with the talk across the table, "
    "slow, then fast, her thumb back on your clit. Your pussy clenches round her fingers. You come with your mouth shut "
    "tight and your thighs locked round her wrist.",
    "Zoe leans her chin on her hand like she's listening across the table. Under it her fingers are already inside "
    "you. She pumps them slow and deep, so the bench doesn't creak. Her thumb rubs your clit until your pussy is "
    "dripping on her palm. You bite the inside of your cheek. She curls her fingers and fucks you harder, right where "
    "it makes your thighs jump. Your tray rattles. She doesn't stop until you come on her hand, your pussy pulsing "
    "round her fingers.",
)
A2_BUTTON = go("Slide in next to Zoe.", node="a2_offer", mins=0,
               cond_=cond(flag("zoe_together"), HUNGRY, SKIRT, TABLE_FREE, tod("11:45", "12:45")))
A2_NODES = [
    node("a2_offer", "Under the table", [
        P("You slide in beside Zoe on the bench, close enough that her thigh is hot against yours. Her hand lands on "
          "your knee under the table, then on the inside of it."),
        D(Z, "I said not here. I lied. Hold still, babe."),
        GC(cond(*NADIA_HERE), P("Across the table Nadia has her textbook open and hasn't noticed a thing."),
           D(N, "Forty pages of reading. Who sets forty pages?")),
        GC(cond(ANY), P("Across the table two girls from Biology are arguing about a test, and neither of them looks down.")),
        T("Anyone who looks under this table will see everything. You hope somebody does."),
    ], [
        go("Let her.", node="a2_fingers", mins=0, cond_=cond(HUNGRY, SKIRT, TABLE_FREE)),   # SKIRT backs "your skirt" behind it
        go("\"Not here, Zo.\"", node="a2_no", mins=0),
    ]),
    node("a2_fingers", "Her fingers", [
        bag("zoe_table_fingers", *A2_FINGERS),
        VID("a girl fingering her girlfriend under a canteen table at lunch, the table talking across from them",
            "fingered under the table in public", "lesbian fingering under cafeteria table",
            pool_dir="sex/zoe_table_fingers_t5"),
        P("She pulls her hand out and licks two fingers clean, looking right at you."),
        D(Z, "Eat your lunch, babe. You look flushed."),
        T("Half the canteen could have looked down. You wanted one of them to."),
    ], act_exits("Finish your lunch.", "canteen", 30, TABLE, [pay("corruption", 79)], "Leave her to her lunch.", plain_loc="campus")),
    node("a2_no", "Not here", [
        D(Z, "Later, babe."),
        P("She takes her hand back and steals a fry off your tray instead, grinning."),
    ], [go("Finish your lunch.", loc="canteen", mins=30)]),
]

# ═════════════════════════════════════════════════════════════════════════════
# A5 · ZOE'S BEDROOM · Zoe (hub_zoe_bedroom, her Mon-Thu 22:00-00:00 row). "Stay over." After zoe_together.
# Bold: her mouth on her tits, her fingers in her (Zoe's middle column: tits, nipples, wet; cap 59). Hungry adds her
# pick of the act (Zoe's late column: pussy, clit, fuck; cap 79). Out to the street: the flat shuts at midnight.
# ═════════════════════════════════════════════════════════════════════════════
BED = today("zoe_bed_today")
BED_FREE = flag(BED, False)

A5_BOLD = (
    "You get under the duvet with her. Zoe rolls on top of you, pushes your clothes out of her way and kisses you, slow "
    "and wet. "
    "Then her mouth goes to your tits. She sucks one nipple hard, then the other, until both are wet and aching. Her "
    "hand slides down your stomach and between your legs. You're already wet. Two of her fingers slip into you and "
    "curl, and she sucks your nipple in time with them. Your hips lift off her sheets. You come on her fingers with her "
    "teeth on your nipple.",
    "Under the duvet Zoe shoves your clothes out of the way. She peels her T-shirt over her head and pulls you down onto "
    "her. Her tits press soft against yours. She kisses your neck, then takes your nipple in her mouth and sucks. Her "
    "fingers find you, slick and wet. She rubs you slow while her tongue flicks your nipple, then pushes two fingers "
    "inside. You grab her hair. She sucks harder and curls her fingers deep, until you come shaking against her, your "
    "nipple still in her mouth.",
)
A5_LICK = ("You're naked under her duvet before she's put her phone down. Zoe kisses down your stomach and pushes your "
           "thighs apart with both hands. She licks your pussy in one long stroke, bottom to top, and laughs at the "
           "noise you make. Then she sucks your clit into her mouth. Two fingers fuck into you while her tongue works. "
           "You grab her hair and grind on her face. Your pussy clenches round her fingers, and you come with your "
           "thighs clamped round her head.")
A5_HERS = ("You push Zoe onto her back and drag her T-shirt up over her tits. She's bare under it. You suck her nipple "
           "and slide your hand down between her legs. Her pussy is soaked. You rub her clit in fast circles while she "
           "swears at the ceiling. Then you push two fingers into her and fuck her with them, hard, the way she begs you "
           "to. She comes bucking against your hand, her pussy tight round your fingers.")
A5_AFTER = [P("She falls asleep with her face in your neck and one leg thrown over yours."),
            T("Her bed smells like her. You don't want to get out of it.")]
A5_BUTTON = go("Get into her bed.", node="a5_offer", mins=0,
               cond_=cond(flag("zoe_together"), BOLD, BED_FREE, tod("22:00", "23:45")))
A5_NODES = [
    node("a5_offer", "Stay over", [
        P("Zoe lifts the edge of her duvet without looking up from her phone."),
        D(Z, "Stay over. I'm not asking twice."),
        T("Her bed, her rules. You want both."),
    ], [
        go("Get in with her.", node="a5_bold", mins=0, cond_=cond(BOLD, BED_FREE)),
        go("Her mouth. Down there.", node="a5_lick", mins=0, cond_=cond(HUNGRY, BED_FREE)),
        go("Your fingers in her.", node="a5_hers", mins=0, cond_=cond(HUNGRY, BED_FREE)),
        go("\"Not tonight, Zo.\"", node="a5_no", mins=0),
    ]),
    node("a5_bold", "Her bed", [
        bag("zoe_bed_bold", *A5_BOLD),
        VID("a girl sucking her girlfriend's nipple in bed under a duvet, fingers between her legs",
            "lesbian nipple sucking fingering in bed", "girlfriends in bed fingering sleepover",
            pool_dir="sex/zoe_bed_bold_t5"),
        D(Z, "Mine tonight. Shh. Sleep."),
        *A5_AFTER,
    ], act_exits("Slip out while she sleeps.", "town", 60, BED, [pay("corruption", 59)], "Kiss her goodnight.")),
    node("a5_lick", "Her mouth", [
        P(A5_LICK),
        VID("a girl eating her girlfriend out in bed, thighs clamped round her head", "lesbian eating pussy in bed",
            "girlfriend licks her clit sleepover", pool_dir="sex/zoe_bed_lick_t5"),
        D(Z, "Stay. Don't you dare go home yet."),
        *A5_AFTER,
    ], act_exits("Slip out while she sleeps.", "town", 60, BED, [pay("corruption", 79)], "Kiss her goodnight.")),
    node("a5_hers", "Your fingers", [
        P(A5_HERS),
        VID("a girl fingering her girlfriend hard on her back in bed, the other one swearing", "fingering her girlfriend in bed",
            "lesbian fingering orgasm bed", pool_dir="sex/zoe_bed_hers_t5"),
        D(Z, "Fuck, babe. Where did you learn that?"),
        *A5_AFTER,
    ], act_exits("Slip out while she sleeps.", "town", 60, BED, [pay("corruption", 79)], "Kiss her goodnight.")),
    node("a5_no", "Not tonight", [
        D(Z, "Fine. Ask me again when you're brave."),
        P("She drops the duvet and goes back to her phone, but she's smiling at it."),
    ], [go("Leave her to sleep.", loc="zoe_apartment", mins=2)]),
]


pay_on_the_way_in(A2_NODES)
pay_on_the_way_in(A5_NODES)


def attach_zoe(out):
    _add_button(_canvas(out, "hub_zoe_canteen"), A2_BUTTON, A2_NODES)
    _add_button(_canvas(out, "hub_zoe_bedroom"), A5_BUTTON, A5_NODES)


# ═════════════════════════════════════════════════════════════════════════════
# A6 · ZOE'S KITCHEN · the keg guy (a party regular with no NPC and no row). Party night, 22:00-02:00, after
# keg_guy_dared (her flash for him in Zoe's dares). The party can walk in: Hungry (cap 79). Strangers' words only
# (DECISIONS 41: tits, nipples, ass, cock, wet, clit; no fuck, cum, pussy, cunt).
# No `schedules`: the hours are condition items (party_went inside 8 hours + 22:00-02:00), so the button is hidden
# when he isn't at the keg, the way a person's hub is. A schedule would dim the button with its hours on every
# visit, including a Monday before she has ever flashed him. One a party night: `keg_guy_went` read for 6 hours
# (the night crosses midnight, which clears a daily flag), and the exit's own daily cap for the climb gate.
# ═════════════════════════════════════════════════════════════════════════════
KEG = today("keg_counter_today")
KEG_FREE = flag(KEG, False)
KEG_ONCE = {"type": "hours_since_flag", "subject": "player", "flag_key": "keg_guy_went", "operator": "gte", "value": 6}

A6_COUNTER = (
    "He turns you round and bends you over the counter between the bottles. He shoves everything you're wearing out of "
    "his way. His cock is hard against your ass. He pushes into you from behind in one slow thrust, and the edge of the "
    "counter digs into your hips. Then he slams into you, hard and fast, one hand on the back of your neck. Red cups "
    "roll off onto the floor. Your tits drag on the sticky worktop with every stroke. He grabs your ass with both hands "
    "and empties into you with a groan, buried as deep as he goes.",
    "He lifts you onto the counter and pushes everything you're wearing out of the way. Bottles clink behind you. He "
    "opens his jeans, and his cock is thick and already wet at the tip. He rubs the head over your clit until you're "
    "dripping, then drives into you. You lock your legs round him. He pounds you back against the cupboards, his mouth "
    "on your tits, sucking a nipple hard. Somebody comes in for a cup and goes straight back out, but he doesn't stop. You "
    "come clenching round his cock, your nails dug into his back.",
)
TOWN_CANVASES = [{
    "id": "keg_guy_counter", "name": "Fuck the keg guy on the counter",   # pass 3 H33/H34 (the-voice.md R1, D11): the name says what happens if she clicks, and never hides the act
    "description": "Heat proposal A6 (DECISIONS 147): party night 22:00-02:00, after keg_guy_dared, Hungry. The guy she "
                   "flashed bends her over Zoe's kitchen counter while the party is through the door. Corruption +1, cap "
                   "79, one a party night.",
    "trigger": {"location": "zoe_kitchen", "is_repeatable": True, "priority": 4, "is_active": True,
                "conditions": cond(AT_PARTY, tod("22:00", "02:00"), flag("keg_guy_dared"), HUNGRY, KEG_ONCE),
                # pass 3 H64: an act she chooses, windowed by a condition, so it says its hours when shut (C5)
                "show_when_blocked": True, "cooldown_message": "Party nights, 10 PM-2 AM"},
    "nodes": [
        node("keg", "The keg", [
            P("The guy from the keg is leaning on the counter with a red cup, right where the bottles are. His grin at you "
              "goes slow, but his eyes go straight to your tits."),
            WHO("Look who's back. I still can't stop thinking about your tits."),
            ME("Just thinking?"), WHO("Come round this side of the counter and find out."),
            P("Through the door the party is loud and close. Anyone could walk in for a drink."),
            T("Anyone could walk in. That's the point."),
        ], [
            go("Let him bend you over the counter.", node="counter", mins=0, cond_=cond(HUNGRY, KEG_FREE)),
            go("\"Not tonight.\"", node="no", mins=0),
        ]),
        node("counter", "Over the counter", [
            bag("keg_guy_counter", *A6_COUNTER),
            VID("a guy fucking a girl bent over a kitchen counter at a house party, red cups everywhere",
                "fucked over the kitchen counter at a party", "stranger bends her over counter house party",
                pool_dir="sex/keg_guy_counter_t5"),
            WHO("Same keg next Friday."), ME("Maybe. If you're lucky."),
            T("You don't even know his name. You'll be back at that keg."),
        ], act_exits("Back to the party.", "zoe_apartment", 15, KEG, [pay("corruption", 79)], "Fix yourself up first.",
                     also=("keg_guy_went",))),
        node("no", "Not tonight", [
            WHO("You know where the keg is."),
            P("He lifts his cup at you and goes back to pouring."),
        ], [go("Back to the party.", loc="zoe_apartment", mins=2)]),
    ]}]

# ═════════════════════════════════════════════════════════════════════════════
# A7 · ZOE'S BATHROOM · Jake at the party (his Friday 19:00-00:00 row is zoe_apartment, next door, so the trigger
# reads him there; requires_npc would read the bathroom and fail). After jake_first_time. Bold: the locked door, his
# middle column (cap 59). Hungry: the door left unlocked, his late column (cap 79). No `schedules`, for A6's reason:
# the button is hidden while he isn't at the party.
# ═════════════════════════════════════════════════════════════════════════════
BATH = today("jake_bathroom_today")
BATH_FREE = flag(BATH, False)

A7_LOCKED = (
    "Jake locks the door and lifts you onto the sink. Zoe's make-up clatters into the basin. He shoves everything "
    "you're wearing out of his way and pushes his cock into you, slow and thick, all the way in. Then he starts "
    "slamming. The mirror bulbs shake with every thrust. Somebody bangs on the door. He grabs your ass with both hands "
    "and pulls you onto him harder. You come clenching round his cock, and he groans into your tits as he empties "
    "inside you.",
    "He turns you to face the mirror and bends you over the sink. In the glass you watch him push your clothes out of "
    "the way. His cock slides into you from behind. He holds your hips and thrusts, hard and steady, his eyes on yours "
    "in the mirror. The line knocks on the door. Your tits bounce over the basin with every stroke. He reaches round "
    "and squeezes one, rough, and you come on his cock with your palm flat on the cold glass.",
)
A7_OPEN = (
    "You don't lock it. Jake sees, and his grin goes wolfish. He shoves your clothes aside, bends you over the sink "
    "with the line right outside, and fucks you hard, his cock slamming in deep. The handle turns. The door swings "
    "open a foot, and a girl with a red cup stares straight at your ass and his cock sliding in and out of you. Jake "
    "doesn't stop. He fucks you faster while she watches, until he pulls you back onto him and his cum runs down your "
    "thighs.",
    "The door stays unlocked, and you both know it. Jake drags your clothes out of the way. He sits on the edge of the "
    "bath and pulls you down onto his cock, facing the door. You ride him hard, your tits bouncing, while the line "
    "bangs on the wood. Somebody pushes the door open, sees you, and doesn't shut it. Jake grips your hips and fucks up "
    "into you, faster and harder. You come on his cock in front of the open door, and he groans and fills you with his "
    "cum.",
)
JAKE_AT_PARTY = here_at(J, "zoe_apartment")
TOWN_CANVASES.append({
    "id": "jake_party_bathroom", "name": "Pull Jake into the bathroom",
    "description": "Heat proposal A7 (DECISIONS 147): Zoe's Friday party, Jake in the living room (his row), after "
                   "jake_first_time. Bold: the locked door (Corruption +1, cap 59). Hungry: the door left unlocked "
                   "(cap 79). Once a day.",
    "trigger": {"location": "zoe_bathroom", "is_repeatable": True, "priority": 5, "is_active": True,
                "conditions": cond(AT_PARTY, JAKE_AT_PARTY, flag("jake_first_time"), BOLD, wd(4), tod("19:00", "23:45"),
                                   BATH_FREE),
                # pass 3 H64: an act she chooses, windowed by a condition, so it says its hours when shut (C5)
                "show_when_blocked": True, "cooldown_message": "Fri, 7 PM-11:45 PM"},
    "nodes": [
        node("door", "Zoe's bathroom", [
            P("Jake catches your wrist at the bathroom door and backs you inside. The party thumps through the wall. "
              "Somebody is already lined up in the hall."),
            D(J, "Five minutes. Nobody will notice."),
            ME("Five minutes? You've never lasted five minutes."),   # pass 3 B3: the talk beside her thought
            D(J, "Then lock the door and find out."),
            T("Everybody will notice, but you want him anyway."),
        ], [
            go("Lock the door.", node="locked", mins=0, cond_=cond(BOLD, BATH_FREE)),
            go("Leave it unlocked.", node="open", mins=0, cond_=cond(HUNGRY, BATH_FREE)),
            go("\"Not at Zoe's.\"", node="no", mins=0),
        ]),
        node("locked", "On the sink", [
            bag("jake_bathroom_locked", *A7_LOCKED),
            VID("a guy fucking his girlfriend on a bathroom sink at a house party, make-up everywhere, someone knocking",
                "sex on bathroom sink at party", "boyfriend fucks her on the sink at a house party",
                pool_dir="sex/jake_bathroom_locked_t5"),
            WHO("Some of us need to pee in here!"),
            D(J, "Next date. Your room. I mean it."),
            T("Somebody in that line heard every second. Good."),
        ], act_exits("Back to the party.", "zoe_apartment", 15, BATH, [pay("corruption", 59)], "Fix your face first.")),
        node("open", "The door open", [
            bag("jake_bathroom_open", *A7_OPEN),
            VID("a couple fucking in a party bathroom with the door open, a girl in the doorway staring",
                "caught fucking in party bathroom door open", "sex with the bathroom door unlocked party",
                pool_dir="sex/jake_bathroom_open_t5"),
            WHO("Oh my God. Sorry!"),
            ME("Leave it open."),
            D(J, "Next date. Your room. I mean it."),
            T("By the end of the night half the party will know, but you don't care."),
        ], act_exits("Back to the party.", "zoe_apartment", 15, BATH, [pay("corruption", 79)], "Fix your face first.")),
        node("no", "Not at Zoe's", [
            D(J, "Later, then. Somewhere with a lock."),
            P("He kisses your neck once and lets you go back out into the noise."),
        ], [go("Back to the party.", loc="zoe_apartment", mins=2)]),
    ]})

for _c in TOWN_CANVASES:   # A6, A7: the pay rides the button into the act (pass 3 G74)
    pay_on_the_way_in(_c["nodes"])
