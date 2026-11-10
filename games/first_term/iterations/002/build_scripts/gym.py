"""The street gym's rooms (LO, 2026-11-10, DECISIONS 225; sheets/places/gym.md): the desk on the floor, the locker room
and its showers, the sauna. Work out stays in college.py (gym_workout, moved to gym_floor); Jake's training in jake.py;
Dex in dex.py.

The desk checks her in for today (`gym_in_today`, cleared at midnight): her card, while the 30-day pass is active
(`[[passes]] gym_month`, the engine counts its days), or $5 for a day pass. The locker room and sauna need it
(world_data.py entry_conditions); so do Work out, Jake's training and Dex.
"""
import copy
from canv import *
from tomlw import tod, wd

out = []
CHECKED_IN = flag("gym_in_today")
PASS_ON = {"type": "pass", "pass_id": "gym_month", "operator": "is_active"}
PASS_OFF = {"type": "pass", "pass_id": "gym_month", "operator": "is_inactive"}
MONEY = lambda n: trait("money", "gte", n)
NO_MONEY = lambda n: trait("money", "lt", n)
GYM_ACC = "gym_accident_today"   # one gym accident a day (college.py), the towel slip among them
TOWEL = {"type": "worn_type", "operator": "eq", "value": "towel"}
ANY = [{"type": "worn_exposure", "operator": "gte", "value": 0}]   # always true: a chain's else


def exh(cap):
    return {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": cap}


# ── the desk (gym_floor): shows until she is checked in today ──
CHECK_IN = [fset("gym_in_today")]
buy_month = go("Buy 30 days ($40).", loc="gym_floor", mins=2, flags=list(CHECK_IN),
               cond_=cond(PASS_OFF, MONEY(40)))
buy_month["passEffects"] = [{"pass_id": "gym_month"}]   # setup.purchasePass: takes the $40, counts 30 days
out.append({
    "id": "gym_desk", "name": "The front desk",
    "description": "The street gym's desk (gym.md, DECISIONS 225): check in for today with her card (the 30-day pass, $40) or a $5 day pass. Everything past the desk needs it.",
    "trigger": {"location": "gym_floor", "is_repeatable": True, "priority": 8, "is_active": True,
                "conditions": cond(flag("gym_in_today", False))},
    "nodes": [node("desk", "The front desk", [
        P("The guy on the desk has a protein shake and his phone, and he looks up at you over both."),
        GC(cond(PASS_ON), WHO("Card? Cheers. You're in.")),
        GC(cond(flag("gym_card_bought")), WHO("Your card's run out. Forty gets you another month. Or five for today.")),
        GC(cond(*ANY), WHO("Members only past the desk. Five for today, forty for the month.")),
        G(cond(PASS_OFF, NO_MONEY(5)), T("You haven't got five dollars on you.")),
        P("Past him, the floor: the racks, the mirror wall, and the locker room at the back."),
    ], [
        go("Show your card.", loc="gym_floor", mins=1, flags=list(CHECK_IN), cond_=cond(PASS_ON)),
        go("Buy a day pass ($5).", loc="gym_floor", mins=2, flags=list(CHECK_IN), cond_=cond(PASS_OFF, MONEY(5)),
           eff=[add("money", -5)]),
        dict(buy_month, flagEffects=CHECK_IN + [fset("gym_card_bought")]),
        go("Not today.", loc="street"),
    ])]})


# ── the locker room (gym_locker): change (wardrobe_location), a towel for the sauna, the shower ──
STRIP_TO_TOWEL = STRIP + [{"action": "equip", "item_id": "towel"}]
out.append({
    "id": "gym_towel", "name": "Strip down to a towel",
    "description": "The locker room: undress and wrap a towel round her, for the sauna (towel only) or the showers. 2 minutes.",
    "trigger": {"location": "gym_locker", "is_repeatable": True, "priority": 3, "is_active": True,
                },   # no condition: in a towel already, it just puts the towel back on
    "nodes": [node("bench", "The bench", [
        P("You strip on the bench in front of your locker, everything off, and wrap one of the gym's thin white towels round you. It barely covers your ass."),
        P("Through the wall you can hear the sauna door, and the showers running at the back."),
    ], [go("Lock your things away.", loc="gym_locker", mins=2, wardrobe=list(STRIP_TO_TOWEL))])]})

# ── the shared showers (gym_showers, DECISIONS 227; gym.md "The shared shower room"). The only showers in the gym, men
#    and women together, entered from the locker room in a towel. Hygiene +50, 15 minutes, once a day. A bathroom, not
#    the street: not public topless (LO, 2026-11-10). Her ladder is what she does while they look (a look that happens
#    to her is stage 1; her bare body to strangers by choice, stage 4: the-heat-ladder.md H1). ──
HYGIENE = {"targetType": "player", "trait": "hygiene", "op": "add", "value": 50, "cap": 100}
SHOWER_DONE = [fset("gym_shower_today")]
HIT_DONE = [fset("gym_hit_today")]
TEAM = [wd(1, 3), tod("16:45", "18:00")]   # the team showers from the end of training (Jake's A1 offer, 16:45)
EXH = lambda n: trait("exhibitionism", "gte", n)
COR = lambda n: trait("corruption", "gte", n)


def corr(cap):
    return {"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": cap}


def towel_back(eff=(), flags=(), mins=15, label="Wrap the towel back round you."):
    return go(label, loc="gym_locker", mins=mins, eff=[HYGIENE, *eff], flags=SHOWER_DONE + list(flags))


STRANGERS = "Four or five men and a couple of women, strangers, under the heads along both walls."
WHO_IN = [
    G(cond(*TEAM), P("Jake's team is in from training, a dozen of them naked under the heads along the far wall, loud, slapping each other with towels.")),
    G(cond(wd(0, 2, 4, 5, 6)), P(STRANGERS)),
    G(cond(wd(1, 3), tod("06:00", "16:45")), P(STRANGERS)),
    G(cond(wd(1, 3), tod("18:00", "21:00")), P(STRANGERS)),
]
out.append({
    "id": "gym_shared_shower", "name": "Take a shower",
    "description": "The gym's shared showers (gym.md, DECISIONS 227): hygiene +50, 15 min, once a day. Her ladder by Exhibitionism: face the wall 0; stop covering 20 (+1 cap 39); face them 40 (+1 cap 59); soap slowly for them 60 (+1 cap 79). 1 in 3 someone hits on her (gym_hit_*), once a day.",
    "trigger": {"location": "gym_showers", "is_repeatable": True, "priority": 4, "is_active": True,
                "conditions": cond(flag("gym_shower_today", False)),
                "substitutions": [{"target_canvas_id": f"gym_hit_{w}", "chance": 0.055,   # six swaps, about 1 in 3 together (gym.md)
                                   "conditions": cond(flag("gym_hit_today", False), flag("gym_shower_today", False))}
                                  for w in ("man", "woman", "couple", "two_men", "two_women", "group")]},
    "nodes": [
        node("in", "The showers", [
            P("You hang your towel on the hook by the door. Then you're naked, in a room full of people who are naked too."),
            *WHO_IN,
            P("Heads turn. Men look at your tits, then lower, and some of them don't look away."),
            GC(cond(trait("exhibitionism", "lt", 20)), T("Everyone showers together. It's that kind of gym. Get in, get clean, get out.")),
            GC(cond(trait("exhibitionism", "lt", 40)), T("They're looking. Let them.")),
            GC(cond(trait("exhibitionism", "lt", 60)), T("You want them to look. You want all of them to.")),
            GC(cond({"type": "worn_exposure", "operator": "gte", "value": 0}), T("Give them something to look at.")),
        ], [
            go("Shower fast, facing the wall.", node="fast", mins=0),
            go("Stop covering.", node="back", mins=0, cond_=cond(EXH(20))),
            go("Turn round and face them.", node="face", mins=0, cond_=cond(EXH(40))),
            go("Soap yourself slowly for them.", node="slow", mins=0, cond_=cond(EXH(60))),
        ]),
        node("fast", "Facing the wall", [
            P("You take the head in the corner and shower facing the tiles, one arm over your tits the whole time, as fast as you can. The room goes quiet behind you."),
            P("You can feel them looking at your ass the entire time. Tomorrow they'll look for you again."),
        ], [towel_back()]),
        node("back", "Your back to the room", [
            P("You drop your arm. You keep your back to the room and wash your hair slowly, and let them look at your bare ass and the water running down the backs of your thighs."),
            WHO("Nice."),
            P("You don't turn round, but you take twice as long as you need. Next time you might."),
        ], [towel_back([exh(39)])]),
        node("face", "Facing them", [
            P("You turn round and rinse facing the room. Your tits are bare, your nipples hard under the water, and the water runs down your stomach and between your legs where everyone can see."),
            WHO("Jesus. Okay."),
            P("A man two heads down has stopped washing. He's just looking at your pussy, and he isn't hiding that he's getting hard."),
            T("Next time, give them more than a look."),
        ], [towel_back([exh(59)])]),
        node("slow", "Slowly", [
            P("You soap yourself slowly for them: your tits in both hands, your nipples between your fingers, down your stomach, between your legs, your hand slow on your pussy like you're alone. You're not alone. Half the room has stopped to watch, and one man has his hand on his cock."),
            WHO("Need a hand with that?"),
            P("You rinse off without answering, and walk out past all of them to the hook."),
        ], [towel_back([exh(79)])]),
    ]})


# ── someone hits on her (1 in 3 of her showers, once a day; gym.md). No money (LO: "Not money they offer"): they offer
#    themselves. Washed Bold 40; her hand Bold 40, alone with one; her body Hungry 60, one; a couple or two of them with
#    the room watching, Corruption 60 and Exhibitionism 60 (a mixed act, H1); a group, stage 5: locked. ──
ALONE = [tod("06:00", "16:45")]   # one person, the room emptied: never in the team's half-hour
NO = lambda line: node("no", "No", [P(line)], [towel_back(flags=HIT_DONE)])


NO_LINES = {
    "man": "You shake your head. He shrugs and goes back to his own head, and watches you the rest of the time.",
    "woman": "You shake your head. She smiles like she'll ask again another day, and goes back to her shower.",
    "couple": "You shake your head. They laugh about it together, and go back to each other.",
    "two_men": "You tell them no. They back off to their own heads, grinning, and keep looking.",
    "two_women": "You say no. They pout at each other, and go back to their own heads.",
    "group": "You say no and push through them to your towel. Nobody stops you, but nobody stops looking either.",
}


HOOKS = {
    "man": "He's in here most mornings. He'll find you under the water again.",
    "woman": "She trains most mornings. She'll find you again.",
    "couple": "They'll be back, and they'll ask again.",
    "two_men": "They'll be back in here, and they'll come and find you.",
    "two_women": "They'll be looking for you next time.",
    "group": "Next time there'll be more of them.",
}


# LO, 2026-11-10 ("Go ahead with your picks"): with more than one of them, the room watches them wash her, so it needs
# both meters at Bold/Showing (Corruption 40 and Exhibitionism 40); alone with one person, Corruption 40.
WASH_GATE = {"man": [], "woman": [], "couple": [EXH(40)], "two_men": [EXH(40)], "two_women": [EXH(40)], "group": [EXH(40)]}


def hit(who, name, intro, wash, extra_nodes, extra_buttons, conds=()):
    nodes = [node("ask", name, intro, [
        go("\"No.\"", node="no", mins=0),
        go(wash[0], node="wash", mins=0, cond_=cond(COR(40), *WASH_GATE[who])),
        *extra_buttons]),
        NO(NO_LINES[who]),
        node("wash", "Washed", [P(wash[1])], [towel_back([corr(59)] + ([exh(59)] if WASH_GATE[who] else []), HIT_DONE)]),
        *extra_nodes]
    for n in nodes[1:]:   # the reader: every way out points ahead
        n["blocks"].append(P(HOOKS[who]))
    return {"id": f"gym_hit_{who}", "name": name,
            "description": f"Someone hits on her in the shared showers (gym.md, DECISIONS 227): {name}. 1 in 3 of her showers, once a day; no money. Washed Bold 40 (+1 cap 59); the rest by the table.",
            "trigger": {"location": "gym_showers", "is_repeatable": True, "priority": 5, "is_active": True, "substitution_only": True,
                        "conditions": cond(flag("gym_hit_today", False), flag("gym_shower_today", False), *conds)},
            "nodes": nodes}


ACT_COST = [{"trait": "energy", "value": 10}]
SEX = {"targetType": "player", "trait": "energy", "op": "add", "value": -10, "clamp": True}


def single(who, he, name, intro, wash, hand, body):
    """One person, the room emptied: her hand (Bold 40), her body (Hungry 60)."""
    return hit(who, name, intro, wash, [
        node("hand", "Your hand", [P(hand)], [towel_back([corr(59)], HIT_DONE)]),
        node("body", "All of you", [P(body)], [towel_back([corr(79), SEX], HIT_DONE)]),
    ], [go(f"Put your hand on {he}.", node="hand", mins=0, cond_=cond(COR(40))),
        go(f"Let {he} have you.", node="body", mins=0, cond_=cond(COR(60)), costs=ACT_COST)], conds=ALONE)


def pair(who, them, name, intro, wash, both):
    """Two of them, the room watching: a mixed act, Corruption 60 and Exhibitionism 60."""
    return hit(who, name, intro, wash, [
        node("both", "Both of them", [P(both)], [towel_back([corr(79), exh(79), SEX], HIT_DONE)]),
    ], [go(f"Let both of {them} have you.", node="both", mins=0, cond_=cond(COR(60), EXH(60)), costs=ACT_COST)])


out.append(single("man", "him", "A man hits on you",
    [P("The room empties out until it's just you and one man two heads down, forties, big, a grey chest. He's had his eyes on you the whole time, and now he comes over."),
     WHO("You missed a bit. Want me to get your back?"),
     P("His cock is half hard and he doesn't care that you see it.")],
    ("Let him wash your back.", "You turn round and let him. He soaps your back slowly with both hands, down to your ass, and then his hands come round the front and he's soaping your tits from behind, his cock pressed against your ass, his thumbs on your nipples. You lean back into him and let him."),
    "You reach back and take his cock in your wet hand. He's thick, and he gets hard fast in your fist. You stroke him under the water with your back against his chest, slow, then fast, until he comes over your fingers and the tiles with a groan he can't keep in.",
    "He turns you to the wall and lifts one of your legs, and pushes his cock into your cunt from behind, under the water. He fucks you hard against the tiles, his hand on your tit, the slap of it echoing round the empty room, until you come with your cheek on the wet wall. He pulls out and comes on your ass, and the water washes it off."))
out.append(single("woman", "her", "A woman hits on you",
    [P("The room empties out until it's just you and a woman about thirty, short hair, a swimmer's shoulders. She's been watching you in a way the men don't, and now she comes over."),
     WHO("You've got soap in your hair. Here."),
     P("Her tits brush your arm. She doesn't move them away.")],
    ("Let her wash you.", "She washes your hair first, her fingers slow on your scalp, her tits pressed to your back. Then her soapy hands go down over your shoulders and onto your tits, and she cups them and rubs your nipples with her thumbs until you're breathing hard."),
    "You turn round and slide your hand between her legs. She's wet, and not from the shower. You rub her clit while she holds onto your shoulders, and she comes fast, biting your neck to stay quiet.",
    "She pushes you back against the tiles, kisses you, and goes down on her knees under the water. She eats your pussy with her tongue on your clit and two fingers inside you, slow and then hard, until you come with your hand in her hair. Then she stands up and makes you do her the same way."))
out.append(pair("couple", "them", "A couple hits on you",
    [P("A couple under the next two heads, both thirties, his arm round her waist. They've been watching you together, and now the woman says something in his ear and they come over."),
     WHO("We were wondering. Would you like company?"),
     P("Half the room has noticed. Nobody's pretending to wash any more.")],
    ("Let them wash you.", "They wash you between them, his hands on your tits from behind, hers soaping your stomach and the insides of your thighs, while the whole room watches. You stand there with the water on your face and let four hands go everywhere."),
    "She kneels and licks your pussy while he holds your tits from behind, and then he bends you over and fucks your cunt while she kisses you. Everyone in the room is watching. You come on his cock with her tongue in your mouth, and he pulls out and comes on her tits and yours."))
out.append(pair("two_men", "them", "Two men hit on you",
    [P("Two men, mates, maybe twenty-five, come and take the heads either side of you. Both of them hard. The rest of the room has gone quiet to see what you do."),
     WHO("Room for us?"),
     P("One of them's already got his hand on the small of your back.")],
    ("Let them wash you.", "They soap you between them, one at your tits, one at your ass, their cocks pressing into you from both sides, while the room watches. You let their hands go everywhere."),
    "One of them fucks your cunt from behind while you suck the other's cock under the water, the whole room watching. They swap. You come on the second one's cock, and they both come on your tits and stomach, and you stand under the water and let it run off you."))
out.append(pair("two_women", "them", "Two women hit on you",
    [P("Two women, friends, take the heads either side of you, laughing at something. Then they stop laughing and look at you, and at each other."),
     WHO("She's cute. Isn't she cute?"),
     P("The men along the far wall have all turned to watch.")],
    ("Let them wash you.", "They wash you together, one soaping your tits and the other your ass and thighs, slow, giggling, while every man in the room watches. One of them kisses your neck."),
    "One of them kisses you and plays with your tits while the other kneels and eats your pussy, her fingers inside you, and the men along the wall stop pretending. You come with your back on the tiles, and then they make you go down on each of them in turn while the room watches."))
out.append(hit("group", "Everyone wants a turn",
    [P("It's crowded, and you're the only one in here anyone is watching. One man says something, then another, and then five or six of them have moved in round you, men and women, too close."),
     WHO("Go on. Let us all have a go."),
     P("Every one of them is looking at your tits, and at you.")],
    ("Let them wash you.", "You let them. Hands everywhere, too many to count, soap on your tits and your ass and between your legs, someone kissing your shoulder, someone else's fingers sliding over your pussy, while you stand in the middle of them and let it happen."),
    [], [go("All of them. (Next release)", node="no", mins=0, cond_=cond(NEXT_RELEASE), swl=True)]))
# ── the sauna (gym_sauna): towel only (world_data entry_conditions). Sit: 20 min, energy +10, once a day.
#    The towel slip (1 in 4, the day's one gym accident): fix it 0; from Watched, three seconds, +1 cap 79. A flash,
#    never sitting topless (first_term: no public topless, 2026-11-08). ──
SAUNA_DONE = [fset("sauna_today")]
ENERGY = {"targetType": "player", "trait": "energy", "op": "add", "value": 10, "cap": 100}
out.append({
    "id": "gym_sauna_sit", "name": "Sit in the sauna",
    "description": "The sauna: 20 minutes, energy +10, once a day (gym.md, DECISIONS 225). 1 in 4 the towel slips (gym_sauna_slip), the day's one gym accident.",
    "trigger": {"location": "gym_sauna", "is_repeatable": True, "priority": 4, "is_active": True,
                "conditions": cond(flag("sauna_today", False)),
                "substitutions": [{"target_canvas_id": "gym_sauna_slip", "chance": 0.25,
                                   "conditions": cond(flag(GYM_ACC, False), flag("sauna_today", False))}]},
    "nodes": [node("heat", "The heat", [
        P("You sit on the top bench with the towel tucked tight over your tits. The heat hits you like a hand. Sweat runs down your neck and into the towel within a minute."),
        P("Two older men sit on the bench below with their eyes half shut, but not all the way shut. Every time you shift, one of them looks at your thighs, where the towel stops."),
        POOL(T("They're looking. Let them. It's only legs."),
             T("You could fix the towel. You don't."),
             T("Ten more minutes, and the towel's soaked through and stuck to you."),
             pid="gym_sauna_lines"),
    ], [go("Sit until you can't take the heat.", loc="gym_sauna", mins=20, eff=[ENERGY], flags=list(SAUNA_DONE))])]})

out.append({
    "id": "gym_sauna_slip", "name": "The towel slips",
    "description": "Random gym accident in the sauna (gym.md, DECISIONS 225): the towel comes undone. Fix it 0; from Exhibitionism 60, let it slip for three seconds, +1 to cap 79. Both finish the sit (20 min, energy +10).",
    "trigger": {"location": "gym_sauna", "is_repeatable": True, "priority": 5, "is_active": True, "substitution_only": True,
                "conditions": cond(flag(GYM_ACC, False), flag("sauna_today", False))},
    "nodes": [
        node("slip", "The towel slips", [
            P("You lean back on the top bench and the wet towel comes untucked. It drops open to your waist. Your tits are bare, slick with sweat, your nipples hard in the heat."),
            P("Both men on the bench below have their eyes open now."),
            WHO("Your towel, love."),
            P("He says it. He doesn't look away while he does."),
            GC(cond(trait("exhibitionism", "lt", 40)), T("Fix it. Now.")),
            GC(cond(trait("exhibitionism", "lt", 60)), T("Fix it. But not too fast.")),
            GC(cond(*ANY), T("Three seconds. Count them.")),
        ], [go("Pull it up fast.", node="fix", mins=0),
            go("Let it stay down, three seconds.", node="let", mins=0, cond_=cond(trait("exhibitionism", "gte", 60)))]),
        node("fix", "Pull it up", [
            P("You grab the towel and yank it up over your tits and hold it there with both arms. The man who spoke shuts his eyes again and smiles."),
        ], [go("Sit out the heat.", loc="gym_sauna", mins=20, eff=[ENERGY], flags=SAUNA_DONE + [fset(GYM_ACC)])]),
        node("let", "Three seconds", [
            P("You don't grab it. You sit there with your bare tits out in the heat for one, two, three seconds, sweat running between them, both men staring at your nipples."),
            P("Then you tuck the towel back up, slow, like nothing happened. The quiet one on the end has to put his own towel over his lap."),
            T("Three seconds. They'll be here tomorrow, waiting for four."),
        ], [go("Sit out the heat.", loc="gym_sauna", mins=20, eff=[ENERGY, exh(79)], flags=SAUNA_DONE + [fset(GYM_ACC)])]),
    ]})


text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · THE GYM (sheets/places/gym.md, DECISIONS 225)\n"
        "# The desk, the locker room and its showers, the sauna.\n"
        "# =============================================================================\n")
text += "".join(emit(c) for c in out)
open(__import__("sys").argv[1], "w").write(text)
print("gym:", len(out), "canvases")
