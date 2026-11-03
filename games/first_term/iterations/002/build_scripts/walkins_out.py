"""The walk-ins outside the house (heat proposal 2026-11-03, B9-B20; DECISIONS 147, chunk 3).

The same mechanism and pay rule as walkins.py (B1-B8), which this file copies:
- each walker is one canvas, `substitution_only`, with its own `location` and no `requires_npc` (the walker is
  elsewhere, or nowhere, when the roll happens; _tryRule would refuse a requires_npc target);
- the host activity she does alone carries `trigger.substitutions`; each rule reads where the walker is now
  (an npc_at_location item) when a row holds him somewhere, and the window just before the row that brings him in;
  a walker with no row at that hour is read by his met flag and the window alone (walkins.py's Kayla);
- screen 1 is the moment; its only exit carries his Lust +2 where he has a Lust meter (of these, only Vance) and
  sets the daily flag. Screen 2 is her answer: the first button is the cover and pays 0; one bolder button per band
  pays her +1, capped at the band's top. People with no meter gain nothing; a flag records the walk-in;
- odds 0.25; once a day per walk-in through `<canvas>_today`, cleared in [engine.daily_tick];
- B20, the office doors: one screen each, a line, no pay. The person is inside in their own office hours (the office
  is open only then), so the rule reads them present in their own office.

Hosts: the solo activities built in Python get their rules from attach() in the script that builds them (extras.py,
college.py, pools.py, town.py). The hosts in 3_activities.toml carry the same rules written into that file by hand;
extras.py checks they match RULES, so the two cannot drift. extras.py emits CANVASES.
"""
from canv import *
from tomlw import tod, wd
from home_items import here, since, npc_add, CURIOUS, BOLD, HUNGRY, DARING

GY, J, Z, N, H, V = "npc_gary", "npc_jake", "npc_zoe", "npc_nadia", "npc_hale", "npc_vance"
ART, BUS, TA, DEAN = "npc_art_lecturer", "npc_business_lecturer", "npc_bio_ta", "npc_dean"


def slot(s, on=True):
    return {"type": "clothing_slot", "slot": s, "operator": "equipped" if on else "unequipped"}


def pay(meter, cap):
    return {"targetType": "player", "trait": meter, "op": "add", "value": 1, "cap": cap}


def lust(npc):
    return npc_add(npc, "want", 2)


ANY = [{"type": "worn_exposure", "operator": "gte", "value": 0}]          # always true: a chain's else
SKIRT = {"type": "worn_type", "operator": "eq", "value": "short_skirt"}
NOT_SKIRT = {"type": "worn_type", "operator": "neq", "value": "short_skirt"}
BARE_LEGS = [{"type": "clothing_item", "item_id": "jeans", "operator": "unequipped"},
             {"type": "clothing_item", "item_id": "leggings", "operator": "unequipped"}]
IN_JEANS = {"type": "clothing_item", "item_id": "jeans", "operator": "equipped"}
IN_LEGGINGS = {"type": "clothing_item", "item_id": "leggings", "operator": "equipped"}
SPORTS_ONLY = [{"type": "clothing_item", "item_id": "sports_bra", "operator": "equipped"},
               slot("top", False), slot("dress", False)]
BRALESS = slot("bra", False)
DARING_STATE = cond(BRALESS, SKIRT, logic="OR")   # the dean's own reading of "what you wear" (college.py)

C_GG = [trait("corruption", "lt", 20)]
C_CUR = [trait("corruption", "gte", 20), trait("corruption", "lt", 40)]
E_COV = [trait("exhibitionism", "lt", 20)]
E_DAR = [trait("exhibitionism", "gte", 20), trait("exhibitionism", "lt", 40)]

CANVASES = []
RULES = {}          # host canvas id -> [substitution rules]
DAILY_FLAGS = []    # every `<canvas>_today`, for 0_systems_spec.toml [engine.daily_tick]
TOML_HOSTS = ("canteen_eat", "canteen_listen", "library_study", "party_house_soak", "quad_grass",
              "door_grade_psych", "door_grade_art", "door_grade_business", "door_grade_bio", "door_dean_notice")


def rule(host, target, chance, *items):
    RULES.setdefault(host, []).append({"target_canvas_id": target, "chance": chance, "conditions": cond(*items)})


def walkin(cid, name, loc, desc, who, moment, moment_label, answer, answers, raise_=(), records=(), extra=(),
           shared=(), when=()):
    """One walker's walk-in (walkins.py's shape): `who` = trigger items (his presence now, met flags, his gates).
    `shared` = another walk-in of the same walker whose daily flag this one also reads and sets (one a day)."""
    today = f"{cid}_today"
    DAILY_FLAGS.append(today)
    CANVASES.append({
        "id": cid, "name": name, "description": desc,
        "trigger": {"location": loc, "is_repeatable": True, "priority": 1, "is_active": True,
                    "substitution_only": True,
                    "conditions": cond(flag("opening_done"), flag(today, False),
                                       *[flag(f"{s}_today", False) for s in shared], *who, *when)},
        "nodes": [node("moment", name, moment,
                       [go(moment_label, node="answer", mins=2, eff=list(raise_) or None,
                           flags=[fset(today)] + [fset(f"{s}_today") for s in shared] + [fset(f) for f in records])]),
                  node("answer", name, answer, answers), *extra]})
    return cid


def one_screen(cid, name, loc, desc, who, blocks, label, dest, records):
    """B20: the person opens the door. One screen, a line, no pay."""
    today = f"{cid}_today"
    DAILY_FLAGS.append(today)
    CANVASES.append({
        "id": cid, "name": name, "description": desc,
        "trigger": {"location": loc, "is_repeatable": True, "priority": 1, "is_active": True,
                    "substitution_only": True,
                    "conditions": cond(flag("opening_done"), flag(today, False), *who)},
        "nodes": [node("door", name, blocks, [go(label, loc=dest, mins=2, flags=[fset(today)] + [fset(f) for f in records])])]})
    return cid


def res(nid, name, blocks, label, dest, mins, **kw):
    """A result screen after her answer: what happens, then out."""
    return node(nid, name, blocks, [go(label, loc=dest, mins=mins, **kw)])


def legs_line(bare, jeans, leggings):
    """Her legs as she has them on: bare, in jeans, in leggings (exactly one shows)."""
    return [G(cond(*BARE_LEGS), P(bare)), G(cond(IN_JEANS), P(jeans)), G(cond(IN_LEGGINGS), P(leggings))]


# ═════════════════════════════════════════════════════════════════════════════
# B9 · THE CAFÉ (host cafe_coffee), off shift. Gary, already in booth four in his rows (Mon-Fri 14:30-18:00,
# Fri 20:00-22:00), comes and sits beside her. No money, no tip, no sex (DECISIONS 102, 117). He has no meter.
# Her answer on Corruption: the knee away 0, leave it +1 cap 19 (Good Girl), his hand on her thigh +1 cap 39 (Curious).
# ═════════════════════════════════════════════════════════════════════════════
walkin("walkin_cafe_gary", "Booth four comes to you", "cafe",
    "B9, Gary: off shift at the counter, Gary leaves booth four and sits beside her; his knee finds hers. No money moves. Her answer on Corruption: the knee away 0, leave it +1 cap 19, his hand on her thigh (Curious) +1 cap 39.",
    [here(GY, "cafe"), flag("gary_met")],
    [P("You take the stool at the end of the counter with your coffee, off the clock for once."),
     P("Gary gets up out of booth four with his paper under his arm and his pot of tea, and sits down on the stool next to yours. Not across. Right next to you."),
     D(GY, "Off the clock, sweetheart? Then you can keep an old man company.")],
    "His knee finds yours.",
    [P("Under the counter his knee presses against yours, warm and heavy, and stays there. He turns a page of his paper with his other hand like nothing's happening."),
     *legs_line("Your legs are bare. His trouser leg rubs against your skin every time he shifts on the stool.",
                "Through your jeans you can feel how warm he is.",
                "Through your leggings you can feel every time he presses."),
     P("His eyes come off the paper and go down to your thighs, and back up to your tits, and he doesn't hurry either way."),
     D(GY, "You've lovely legs, sweetheart. Shame to waste them behind a counter.")],
    [go("Move your knee.", node="g_move", mins=2),
     go("Leave it.", node="g_leave", mins=10, cond_=cond(*C_GG), eff=[pay("corruption", 19)]),
     go("Let his hand rest on your thigh.", node="g_hand", mins=10, cond_=cond(CURIOUS), eff=[pay("corruption", 39)])],
    records=["gary_sat_with_her"], extra=[
        res("g_move", "Your knee away", [P("You shift your knee away from his and pick up your cup with both hands."),
                                         D(GY, "Suit yourself, sweetheart."),
                                         P("He goes back to booth four with his tea, and his paper comes back up, an inch at a time.")],
            "Finish your coffee.", "cafe", 15),
        res("g_leave", "Leave it", [P("You leave it. His knee stays pressed against yours the whole time you drink your coffee, and you don't look at him once. Your face is hot, and your nipples have gone tight, and you hate that they have."),
                                    D(GY, "There. That's nice, isn't it?"),
                                    P("When you stand up he lets his knee drag along your thigh as you go.")],
            "Go.", "cafe", 10),
        res("g_hand", "His hand", [P("His hand comes off the paper and settles on your thigh, high up, big and warm. His thumb moves, slow, back and forth, an inch from your crotch."),
                                   G(cond(SKIRT, slot("underwear")), P("It's under your hem. His palm is on your bare skin, and his little finger is right at the edge of your panties.")),
                                   G(cond(SKIRT, slot("underwear", False)), P("It's under your hem. His palm is on your bare skin, and his little finger is an inch from your bare pussy.")),
                                   P("You keep drinking your coffee. You don't move his hand. Your pussy throbs, and you squeeze your thighs together round his fingers, and he feels it and smiles at his paper."),
                                   D(GY, "Good girl."),
                                   P("He takes his hand back when you finish the cup, and pats your thigh, twice, like he owns it.")],
            "Go.", "cafe", 10)])
for days, a, b in (((0, 1, 2, 3, 4), "14:30", "18:00"), ((4,), "20:00", "22:00")):
    rule("cafe_coffee", "walkin_cafe_gary", 0.25, here(GY, "cafe"), flag("gary_met"), wd(*days), tod(a, b))

# ═════════════════════════════════════════════════════════════════════════════
# B10 · THE GYM (host gym_workout): the team comes in for training, Tue and Thu 15:00-15:15, the start of Jake's
# training row (built differently from the proposal's 14:45-15:00: before 15:00 Jake has no row, so a line placing him
# in the gym would be untrue). Jake is in it only while his row has him there (once she has his number); before that
# the team is strangers and he is not named.
# A group look that happens to her in a sports bra. Her answer on Exhibitionism: go 0, finish your set (Daring) +1 cap 39.
# ═════════════════════════════════════════════════════════════════════════════
JN = here(J, "campus_gym")
walkin("walkin_gym_team", "The team comes in", "campus_gym",
    "B10, the team: in for training on Tuesday or Thursday at 15:00, they walk in on her at the bench. Jake leads them while his row has him there; nobody has a meter. Her answer on Exhibitionism: go 0, finish your set in her sports bra (Daring) +1 cap 39.",
    [],
    [P("You're flat on your back on the bench with the bar over your chest, alone in the free-weights corner."),
     GC(cond(*SPORTS_ONLY), P("Just your sports bra and your bottoms. Your tits strain the bra every time you press the bar up.")),
     GC(cond(*ANY), P("Your clothes are stuck to you with sweat.")),
     P("The double doors bang open and the team comes in for training, a dozen big guys in team vests, loud, bags over their shoulders.")],
    "They've seen you.",
    [GC(cond(*SPORTS_ONLY), P("The noise stops. A dozen of them look at you at once: your tits in the sports bra, your stomach, your legs spread either side of the bench. One of them whistles, long and low."),
       WHO("Bench is ours now, sweetheart. Take your time, though."),
       P("Nobody laughs. They just keep looking at your tits.")),
     GC(cond(*ANY), P("A dozen heads turn your way. Their eyes go down you on the bench, slow, your legs, your hips."),
       WHO("We need that bench. No rush.")),
     G(cond(JN), P("Jake's at the front of them. He drops his bag, and his eyes go down you and stay."),
       D(J, "Easy, boys. Eyes on your own reps.")),
     G(cond(JN), P("He doesn't take his own eyes off you while he says it."))],
    [go("Grab your things and go.", node="t_go", mins=2),
     go("Finish your set.", node="t_set", mins=15, cond_=cond(*SPORTS_ONLY, *E_DAR), eff=[pay("exhibitionism", 39)])],
    records=["team_saw_gym"], extra=[
        res("t_go", "Go", [GC(cond(*SPORTS_ONLY), P("You rack the bar, grab your hoodie off the floor and pull it on over your sports bra, and walk out through the middle of them with your face burning.")),
                           GC(cond(*ANY), P("You rack the bar and grab your bag and walk out through the middle of them, eyes down.")),
                           P("The noise starts up again behind you, and you hear the laugh.")],
            "Go.", "campus", 5),
        res("t_set", "Finish your set", [P("You don't get up. You lie back down under the bar and finish your set, ten slow reps, with a dozen of them standing round watching you do it."),
                                         P("Every time you push the bar up your tits squeeze together in the sports bra, and every time you bring it down they bounce. Your nipples are hard through the cloth. You can feel every pair of eyes on them."),
                                         G(cond(JN), D(J, "Ten. Look at her. Ten.")),
                                         G(cond(here(J, "campus_gym", False)), WHO("Ten. Jesus. Ten.")),
                                         P("You rack the bar and sit up slow, and take your time wiping down the bench."),
                                         VID("a girl in a sports bra on a weight bench, a sports team standing round watching her", "girl in sports bra lifting team watching gym", "guys staring at girl working out gym bench", pool_dir="sex/walkin_gym_team_t4")],
            "Go.", "campus", 5, eff=[add("energy", -10)], flags=[fset("worked_out")])],
    when=[wd(1, 3), tod("15:00", "15:15")])
rule("gym_workout", "walkin_gym_team", 0.25, wd(1, 3), tod("15:00", "15:15"))

# ═════════════════════════════════════════════════════════════════════════════
# B11 · THE CANTEEN (hosts canteen_eat, canteen_listen), as their lunch rows start at 11:45 (built differently from
# the proposal's 11:30-11:45: none of the three has a row before 11:45, so a line placing them there would be untrue).
# One walker a window, so each rolls the odds written: Zoe 11:45-12:00 Mon, Wed, Fri; Jake 11:45-12:00 Tue, Thu;
# Nadia 12:00-12:15 any weekday. Each is read in the canteen. Nobody has a meter.
# ═════════════════════════════════════════════════════════════════════════════
walkin("walkin_canteen_zoe", "Budge up", "canteen",
    "B11, Zoe: at the start of lunch she slides in beside her and puts a hand on her knee (F/F tease). Her answer on Corruption: move it 0, let it stay (Curious) +1 cap 39.",
    [here(Z, "canteen"), flag("zoe_met")],
    [P("You've got a table by the windows to yourself, the lunch queue building."),
     P("Zoe drops into the chair beside yours, hooks it closer with her foot until your hips touch, and steals your drink.")],
    "Her hand finds your knee.",
    [D(Z, "Budge up, babe. I'm hiding from my Biology group."),
     P("Under the table her hand lands on your knee like it lives there, and squeezes."),
     *legs_line("Your leg is bare. Her nails trace a slow circle on the inside of your knee, then an inch up your thigh, and stop.",
                "Her thumb rubs back and forth on the inside of your knee through your jeans, then an inch higher.",
                "Her thumb rubs back and forth on the inside of your knee through your leggings, then an inch higher."),
     P("She keeps talking with her mouth full, like her hand isn't there. She's watching your face the whole time.")],
    [go("Move her hand.", node="z_move", mins=2),
     go("Let it stay.", node="z_stay", mins=10, cond_=cond(CURIOUS), eff=[pay("corruption", 39)])],
    records=["zoe_canteen_knee"], extra=[
        res("z_move", "Move her hand", [P("You pick her hand up off your leg and put it back on her own."),
                                        D(Z, "Rude. Fine. Later, babe."),
                                        P("She steals another sip of your drink to punish you.")],
            "Go.", "canteen", 5),
        res("z_stay", "Let it stay", [P("You let it stay. Her hand slides up the inside of your thigh, slow, until her little finger is an inch from your crotch, and stops there. Your pussy clenches. Your nipples go hard, and she sees them do it."),
                                      D(Z, "Oh, babe. Look at you."),
                                      P("She squeezes your inner thigh once, hard, then takes her hand back and licks salt off her fingers like nothing happened. Your thighs are still tight together.")],
            "Go.", "canteen", 10)],
    when=[wd(0, 2, 4), tod("11:45", "12:00")])

walkin("walkin_canteen_jake", "The team's table", "canteen",
    "B11, Jake: at the start of lunch he and two of the team drop their trays at her table; in a short skirt he shows her legs off to them. A group look that happens to her: skirt down 0, leave it +1 cap 19 (Exhibitionism).",
    [here(J, "canteen"), flag("jake_met")],
    [P("You've got a table by the windows to yourself, the lunch queue building."),
     P("Jake drops his tray across from you, and two of the team drop theirs either side of him.")],
    "They sit down.",
    [GC(cond(SKIRT), P("Your skirt has ridden up your thighs on the plastic chair. Jake's eyes go straight down to it."),
        D(J, "Guys. Look at her."),
        P("They look. Three of them, staring at your bare thighs and the edge of your skirt under the table, nobody eating.")),
     GC(cond(*ANY), D(J, "Saved us a table? Good girl."),
        P("The two of them look you over across the table, your tits, your mouth, and grin at each other."))],
    [go("Pull your skirt down.", node="j_down", mins=2, cond_=cond(SKIRT)),
     go("Eat your lunch.", node="j_eat", mins=2, cond_=cond(NOT_SKIRT)),
     go("Leave it.", node="j_leave", mins=10, cond_=cond(SKIRT, *E_COV), eff=[pay("exhibitionism", 19)])],
    records=["team_saw_canteen"], extra=[
        res("j_down", "Skirt down", [P("You tug your skirt down to your knees, as far as it goes. The table groans."), D(J, "Spoilsport.")],
            "Go.", "canteen", 10),
        res("j_eat", "Eat", [P("You eat. They talk about Saturday over your head, and the one on the left keeps looking at your tits when he thinks you won't see.")],
            "Go.", "canteen", 15),
        res("j_leave", "Leave it", [P("You leave it. You eat your lunch with your skirt up round your thighs and three of them staring at your legs, and you don't look up. Your face is on fire. Your nipples are hard, and the one on the left sees that too."),
                                    D(J, "Told you, didn't I?")],
            "Go.", "canteen", 10)],
    when=[wd(1, 3), tod("11:45", "12:00")])

walkin("walkin_canteen_nadia", "Nadia sits down", "canteen",
    "B11, Nadia: at lunch she sits down opposite with a line about Dr. Hale. No heat, no pay.",
    [here(N, "canteen"), flag("nadia_met"), flag("hale_met")],
    [P("You've got a table by the windows to yourself. Nadia comes over from the queue with her salad, puts it down across from you and sits.")],
    "She leans in.",
    [D(N, "Word of advice. Don't sit in the front row for Hale. He learns the front row's names first, and then he learns their legs."),
     G(cond(trait("hale_step", "gte", 2)), D(N, "He knows yours already, doesn't he? I've seen him look.")),
     P("She stabs a tomato and doesn't look up.")],
    [go("Eat with her.", loc="canteen", mins=15)],
    records=["nadia_canteen_hale"], when=[wd(0, 1, 2, 3, 4), tod("12:00", "12:15")])

for host in ("canteen_eat", "canteen_listen"):
    rule(host, "walkin_canteen_zoe", 0.25, here(Z, "canteen"), wd(0, 2, 4), tod("11:45", "12:00"))
    rule(host, "walkin_canteen_jake", 0.25, here(J, "canteen"), wd(1, 3), tod("11:45", "12:00"))
    rule(host, "walkin_canteen_nadia", 0.25, here(N, "canteen"), flag("hale_met"), wd(0, 1, 2, 3, 4), tod("12:00", "12:15"))

# ═════════════════════════════════════════════════════════════════════════════
# B12 · THE LIBRARY (host library_study, not the stacks): Nadia, 14:30-14:45 on her library days, as her row there
# starts (built differently from the proposal's 14:15-14:30: she has no row before 14:30). If she has seen the couple in the back stacks (saw_the_library_couple, set on every way out of the stacks),
# Nadia knows; otherwise she points at them. Overhearing as a hook; no pay.
# ═════════════════════════════════════════════════════════════════════════════
SAW = flag("saw_the_library_couple")
walkin("walkin_library_nadia", "Nadia sits down", "library",
    "B12, Nadia: in for her library afternoon, she sits beside her and talks about the back stacks. No pay; nadia_knows_stacks once she has seen them.",
    [here(N, "library"), flag("nadia_met")],
    [P("You've got a desk under a green lamp and the Psychology reader open. Nadia comes in with her bag, drops into the chair beside yours and plugs her laptop into your socket without asking.")],
    "She leans over.",
    [D(N, "This is the only desk with a plug. Don't take it personally."),
     GC(cond(SAW), P("She sees you glance at the back stacks, and her eyebrows go up."),
        D(N, "You've been back there, haven't you? You saw them too?"),
        D(N, "Everyone goes back there. Everyone pretends they only went for a book.")),
     GC(cond(*ANY), D(N, "Don't go in the back stacks after lunch. Unless you want an education."),
        P("She doesn't say what kind. She doesn't have to."))],
    [go("Get back to work.", loc="library", mins=15, cond_=cond(SAW), flags=[fset("nadia_knows_stacks")]),
     go("Get back to work.", loc="library", mins=15, cond_=cond(flag("saw_the_library_couple", False)))],
    when=[wd(0, 1, 2, 4), tod("14:30", "14:45")])
rule("library_study", "walkin_library_nadia", 0.25, here(N, "library"), wd(0, 1, 2, 4), tod("14:30", "14:45"))

# ═════════════════════════════════════════════════════════════════════════════
# B13 · THE PARK (hosts park_run, park_rest): Zoe, Saturday and Sunday 08:00-08:15, as her run row starts (built
# differently from the proposal's 07:45-08:00: she has no row before 08:00).
# The answers route into her built park hub and her dare. One a day between the two.
# ═════════════════════════════════════════════════════════════════════════════
def park_answers():
    return [go("Let her run on.", loc="park", mins=2),
            go("Run with her.", node="hub_zoe_park.path", mins=0),
            go("\"Dare me, Zo.\"", node="zoe_park_dare.ask", mins=0, cond_=cond(slot("top")))]


walkin("walkin_run_zoe", "Race you", "park",
    "B13, Zoe: out for her weekend run, she catches her stretching at the gates and slaps her ass. No meter; the answers route into hub_zoe_park and zoe_park_dare.",
    [here(Z, "park"), flag("zoe_met")],
    [P("You're stretching against the park gates, bent over your knees, when somebody comes up behind you fast."),
     P("A hand cracks across your ass, hard enough to sting through your clothes.")],
    "You spin round.",
    [P("Zoe, in tiny shorts and a sports top, bouncing on her toes, grinning. Her tits bounce with her."),
     D(Z, "Race you. Loser buys coffee."),
     P("Your ass is still stinging where her hand was, and she knows it.")],
    park_answers(), records=["zoe_caught_up"], shared=("walkin_rest_zoe",), when=[wd(5, 6), tod("08:00", "08:15")])

walkin("walkin_rest_zoe", "Pillow", "park",
    "B13, Zoe: out for her weekend run, she flops down on the bench with her head in her lap. No meter; the answers route into hub_zoe_park and zoe_park_dare.",
    [here(Z, "park"), flag("zoe_met")],
    [P("You're stretched out on a bench by the pond with your eyes shut when somebody drops onto the end of it.")],
    "A head lands in your lap.",
    [P("Zoe, in tiny shorts and a sports top, her ponytail spread across your thighs, her face turned in against your stomach. She's warm and smells of sun cream."),
     D(Z, "Five minutes. Then we run. Don't move, you're comfy."),
     P("Her cheek rubs against your thigh when she talks, and her hand settles on your hip.")],
    park_answers(), records=["zoe_caught_up"], shared=("walkin_run_zoe",), when=[wd(5, 6), tod("08:00", "08:15")])
for host, cid in (("park_run", "walkin_run_zoe"), ("park_rest", "walkin_rest_zoe")):
    rule(host, cid, 0.25, here(Z, "park"), wd(5, 6), tod("08:00", "08:15"))

# ═════════════════════════════════════════════════════════════════════════════
# B14 · THE HOT TUB (host party_house_soak, Watched 60): Zoe, at the party house on her Saturday row, gets in beside
# her at 23:30-00:00. After zoe_together her hand goes under the water while the deck can see: a mixed act, Hungry
# (Corruption 60) on top of the tub's own Exhibitionism 60. "Let her." +1 cap 79. Every exit is after 22:00, so each
# marks the late night like the tub's own (late_party, came_home_late).
# ═════════════════════════════════════════════════════════════════════════════
TOG = flag("zoe_together")
LATE = [fset("late_party"), fset("came_home_late")]
TUB_EXIT = dict(eff=[{"targetType": "player", "trait": "energy", "op": "add", "value": 5, "cap": 100}], flags=LATE)
walkin("walkin_tub_zoe", "Zoe gets in", "party_house",
    "B14, Zoe: late on Saturday she gets into the hot tub beside her; after zoe_together her hand goes under the water while the deck can see. Hers: not here 0; Hungry, let her, Corruption +1 cap 79.",
    [here(Z, "party_house"), flag("zoe_met")],
    [P("You're naked in the tub up to your tits, the steam going up into the dark. The deck is full: people with drinks along the rail, a couple on the steps, all of them in reach of a look."),
     P("Zoe comes out of the house with a drink in each hand, steps out of her dress on the deck, and gets in beside you, naked, so close her thigh is against yours.")],
    "Her thigh is against yours.",
    [D(Z, "There you are. I've been looking everywhere."),
     GC(cond(TOG), P("Under the water her hand lands on your thigh. Then it slides up, slow, to the top of your thigh, and her fingers brush your pussy."),
        P("She doesn't look at you. She sips her drink and smiles at the people on the rail, and her fingers stroke you once, light, under the water where they could all see if they looked down."),
        D(Z, "Shh. Nobody's looking. Yet.")),
     GC(cond(*ANY), P("She hands you a drink and leans her head on your shoulder. Her wet tits press against your arm. Under the water her foot hooks round your ankle."),
        D(Z, "This is the life, babe."))],
    [go("\"Not here, Zo.\"", node="tub_no", mins=2, cond_=cond(TOG)),
     go("Get out, dripping.", loc="party_house", mins=30, cond_=cond(flag("zoe_together", False)), **TUB_EXIT),
     go("Let her.", node="tub_let", mins=10, cond_=cond(TOG, HUNGRY), eff=[pay("corruption", 79)])],
    records=["zoe_in_the_tub"], extra=[
        res("tub_no", "Not here", [P("You catch her wrist under the water and put her hand back on her own thigh."),
                                   D(Z, "Fine. Later, babe. You owe me."),
                                   P("She kisses your cheek and climbs out, and the whole rail watches her go.")],
            "Get out, dripping.", "party_house", 30, **TUB_EXIT),
        res("tub_let", "Let her", [P("You let her. You open your thighs under the water, and her fingers find your clit straight away and rub it in slow, tight circles."),
                                   P("Then two of her fingers push into your pussy, deep, and curl. You grip the edge of the tub. The guy on the steps has stopped talking. He's looking at the water, at the way your hips are moving, at your tits rising out of it every time you gasp."),
                                   P("Zoe fucks you with her fingers in time with the music from the house, and keeps sipping her drink with her other hand. Your nipples are hard in the cold air. You come with your mouth clamped shut, your pussy clenching round her fingers, half the deck watching your face do it."),
                                   D(Z, "Good girl. They all saw that."),
                                   VID("two naked girls in a steaming hot tub at night, one fingering the other under the water, people on the deck watching", "lesbian fingering in hot tub party watching", "girl fingers girlfriend hot tub people watching", pool_dir="sex/walkin_tub_zoe_t5")],
            "Get out, dripping.", "party_house", 30, **TUB_EXIT)],
    when=[wd(5), tod("23:30", "00:00")])
rule("party_house_soak", "walkin_tub_zoe", 0.25, here(Z, "party_house"), wd(5), tod("23:30", "00:00"))

# ═════════════════════════════════════════════════════════════════════════════
# B15 · THE QUAD (host quad_grass). Jake and the team, Mon, Wed, Fri 08:30-08:45 as their row starts, when her
# skirt has ridden up: a group look that happens to her, Exhibitionism, skirt fixed 0, left +1 cap 19. Zoe, Tue, Thu,
# Fri 14:30-14:45 as her grass row starts, her head in her lap (built differently from the proposal's 08:15-08:30 and
# 14:15-14:30: neither has a row before, so a line placing them on the quad would be untrue): Corruption, sit up 0, leave her +1 cap 19 (Good
# Girl), her hand on her thigh +1 cap 39 (Curious).
# ═════════════════════════════════════════════════════════════════════════════
walkin("walkin_quad_team", "The team's spot", "quad",
    "B15, Jake and the team: arriving at their spot on the grass, they find her with her skirt ridden up. A group look that happens to her: fix it 0, leave it +1 cap 19 (Exhibitionism). Nobody has a meter.",
    [here(J, "quad"), flag("jake_met"), SKIRT],
    [P("You're lying back on the grass with your bag under your head and your eyes shut. Your skirt has ridden right up your thighs on the slope, and you haven't noticed."),
     P("Then a shadow. Jake and the team, coming across the grass for their spot under the tree.")],
    "They've stopped.",
    [P("You open your eyes. Six of them, standing at your feet, looking straight up your thighs. Your skirt is round your hips."),
     G(cond(slot("underwear")), P("They can see your panties, and the shape of you through them.")),
     G(cond(slot("underwear", False)), P("There's nothing under it. They can see your pussy.")),
     D(J, "Morning. Nice view."),
     WHO("Best thing I've seen all week."),
     P("Nobody moves to sit down.")],
    [go("Fix your skirt.", node="q_fix", mins=2),
     go("Leave it.", node="q_leave", mins=10, eff=[pay("exhibitionism", 19)])],
    records=["team_saw_grass"], extra=[
        res("q_fix", "Fix your skirt", [P("You sit up fast and yank your skirt down over your thighs. Your face is burning. They laugh and sit down round you, and the one nearest keeps looking at your legs anyway.")],
            "Get up.", "quad", 15),
        res("q_leave", "Leave it", [P("You don't fix it. You shut your eyes again and leave your skirt where it is, round your hips, your thighs bare all the way up, six of them looking."),
                                    P("Your nipples go hard. You can hear them not talking. One of them sits down right by your feet, where the view's best."),
                                    D(J, "Fuck me. Okay."),
                                    P("You count to twenty before you sit up and smooth it down.")],
            "Get up.", "quad", 15)],
    when=[wd(0, 2, 4), tod("08:30", "08:45")])

walkin("walkin_quad_zoe", "Pillow", "quad",
    "B15, Zoe: arriving for her afternoon on the grass, she lies down with her head in her lap. Her answer on Corruption: sit up 0, leave her +1 cap 19, her hand on her thigh (Curious) +1 cap 39.",
    [here(Z, "quad"), flag("zoe_met")],
    [P("You're sitting on the grass with your knees out and your notes on your lap."),
     P("Zoe flops down beside you without a word, shoves your notes off, and puts her head in your lap.")],
    "Her head's in your lap.",
    [P("She turns her face in against your thigh and looks up at you, upside down, her breath warm through your clothes, an inch from your crotch."),
     D(Z, "Hi. I live here now."),
     P("Her hand comes up and rests on the outside of your thigh. People on the next blanket look over. She doesn't care, and she doesn't move.")],
    [go("Sit up. \"Get your own lap.\"", node="qz_up", mins=2),
     go("Leave her there.", node="qz_leave", mins=20, cond_=cond(*C_GG), eff=[pay("corruption", 19)]),
     go("Let her hand slide up your thigh.", node="qz_hand", mins=20, cond_=cond(CURIOUS), eff=[pay("corruption", 39)])],
    records=["zoe_lap_quad"], extra=[
        res("qz_up", "Get your own lap", [ME("Get your own lap."), P("Zoe rolls off you onto the grass, laughing."), D(Z, "Mean. I'll remember this.")],
            "Get up.", "quad", 10),
        res("qz_leave", "Leave her there", [P("You leave her there. She shuts her eyes with her cheek against your thigh, and you sit very still with her breath on you and your heart going too fast."),
                                            D(Z, "See? You like it.")],
            "Get up.", "quad", 10),
        res("qz_hand", "Her hand", [P("Her hand slides from the outside of your thigh to the inside, slow, and keeps going, and stops high, her fingers pressing in right next to your pussy."),
                                    P("She's looking up at your face while she does it. Your nipples go hard, and she sees them, upside down, and grins. On the next blanket two guys have stopped talking."),
                                    D(Z, "Your face, babe. Your face right now.")],
            "Get up.", "quad", 10)],
    when=[wd(1, 3, 4), tod("14:30", "14:45")])
rule("quad_grass", "walkin_quad_team", 0.25, here(J, "quad"), SKIRT, wd(0, 2, 4), tod("08:30", "08:45"))
rule("quad_grass", "walkin_quad_zoe", 0.25, here(Z, "quad"), wd(1, 3, 4), tod("14:30", "14:45"))

# ═════════════════════════════════════════════════════════════════════════════
# B16 · THE LECTURE HALL (host lecture_timetable): Dr. Hale comes in for his Psychology lecture as his row starts,
# Mon, Wed, Fri 08:30-08:45 and Thu 13:00-13:15, after hale_01_done. Built differently from the proposal (Mon, Wed,
# Fri 08:15-08:30, "alone in the hall"): the hall opens at 08:30 and Hale has no row before his lecture, so the only
# true moment is the class's own start, with the room filling. His leak: his eyes on her legs, the pen in his hand.
# Hers on Exhibitionism: a seat 0, the front desk while he sets up (Daring) +1 cap 39.
# ═════════════════════════════════════════════════════════════════════════════
walkin("walkin_hall_hale", "Before the lecture", "lecture_hall",
    "B16, Dr. Hale: in for his lecture, he finds her at the door and looks at her legs, his pen in his hand. Hers on Exhibitionism: a seat 0, sit on the front desk while he sets up (Daring) +1 cap 39.",
    [here(H, "lecture_hall"), flag("hale_met"), flag("hale_01_done")],
    [P("You're at the door reading the timetable when Dr. Hale comes in for his lecture with his laptop bag and a coffee, the first of the class filing in behind him.")],
    "He stops beside you.",
    [P("He looks at you, and then his eyes go down, to your legs, and stay there a second too long."),
     *legs_line("Your legs are bare. His eyes go up them to your hem.",
                "His eyes go down the length of your legs in your jeans and up again to your ass.",
                "His eyes go down your legs in your leggings, and up again to your ass."),
     P("The pen in his hand clicks, once, twice."),
     D(H, "Keen, @player. Good.")],
    [go("Take a seat.", node="h_seat", mins=2),
     go("Sit on the front desk while he sets up.", node="h_desk", mins=10, cond_=cond(*E_DAR), eff=[pay("exhibitionism", 39)])],
    records=["hale_early_look"], extra=[
        res("h_seat", "A seat", [P("You go and sit in the third row while the seats fill up round you. He sets up his laptop at the lectern and doesn't look your way again, and you can tell it costs him.")],
            "Take notes.", "lecture_hall", 5),
        res("h_desk", "The front desk", [P("You hop up onto the front desk, right beside his lectern, and cross your legs."),
                                         G(cond(SKIRT), P("Your skirt rides up your thighs. You don't pull it down.")),
                                         P("He plugs his laptop in with his back to you. Then he turns round, and his eyes go straight to your legs and stay there, and the pen stops clicking. Behind you the rows are filling, and they can all see where he's looking."),
                                         D(H, "That's my desk."),
                                         P("He doesn't tell you to get off it. He goes red to the collar and waits until you slide down and take the front row, right in front of him.")],
            "Take notes.", "lecture_hall", 5)],
    )
for days, a, b in (((0, 2, 4), "08:30", "08:45"), ((3,), "13:00", "13:15")):
    rule("lecture_timetable", "walkin_hall_hale", 0.25, here(H, "lecture_hall"), flag("hale_01_done"), wd(*days), tod(a, b))

# ═════════════════════════════════════════════════════════════════════════════
# B17 · ZOE'S COUCH (host zoe_couch_alone, Zoe in her bedroom Mon-Thu 22:00-00:00): she comes out in her sleep shirt
# and no bra (her leak). Hers on Corruption: goodnight 0, pull her down (Curious) +1 cap 39; after zoe_together, at
# Bold, a link into A5's offer in her bedroom. Until 23:30, so every exit lands before the flat shuts.
# ═════════════════════════════════════════════════════════════════════════════
walkin("walkin_couch_zoe", "Can't sleep", "zoe_apartment",
    "B17, Zoe: out of her bedroom in her sleep shirt and no bra, she sits down with her. Hers on Corruption: goodnight 0, pull her down onto the couch (Curious) +1 cap 39; after zoe_together, A5.",
    [here(Z, "zoe_bedroom"), flag("zoe_met")],
    [P("You're on Zoe's couch under the fairy lights. Down the hall her door opens."),
     P("Zoe pads out barefoot in a sleep shirt that barely covers her ass, no bra under it. Her nipples show through the cotton.")],
    "She drops down next to you.",
    [P("She curls up against your side with her bare legs over your lap. The shirt rides up her thighs. Her tits press soft against your arm."),
     D(Z, "Can't sleep. Talk to me."),
     P("She doesn't want to talk. She's looking at your mouth.")],
    [go("Say goodnight.", node="c_night", mins=5),
     go("Pull her down onto the couch.", node="c_pull", mins=15, cond_=cond(CURIOUS), eff=[pay("corruption", 39)]),
     go("Go to bed with her.", node="hub_zoe_bedroom.a5_offer", mins=2,
        cond_=cond(TOG, BOLD, flag("zoe_bed_today", False), tod("22:00", "23:45")))],
    records=["zoe_couch_night"], extra=[
        res("c_night", "Goodnight", [D(Z, "Boring. Night, babe."),
                                     P("She kisses your cheek, slow, near your mouth, and pads back down the hall. Her door shuts.")],
            "Sit a while.", "zoe_apartment", 15),
        res("c_pull", "On the couch", [P("You pull her down on top of you. She lands with a laugh and her whole weight on you, her bare thighs either side of yours, her tits squashed soft against yours through her shirt."),
                                       P("She stops laughing. Her nipples are hard against you. Her hips settle, and press down, once, and you feel the heat of her through your clothes."),
                                       D(Z, "Oh. Okay. Hi."),
                                       P("She stays there a long minute, her face in your neck, breathing. Then she gets up, tugs her shirt down and goes back to bed without looking back.")],
            "Sit a while.", "zoe_apartment", 15)],
    when=[wd(0, 1, 2, 3), tod("22:00", "23:30")])
rule("zoe_couch_alone", "walkin_couch_zoe", 0.25, here(Z, "zoe_bedroom"), wd(0, 1, 2, 3), tod("22:00", "23:30"))

# ═════════════════════════════════════════════════════════════════════════════
# B18 · ZOE'S BEDROOM (host zoe_bedroom_look): Zoe in from the living room to change for bed, Mon-Thu 21:45-22:00
# (her bedroom row starts at 22:00). She strips in front of her. A look that happens to her, she stays: Corruption,
# look away 0, watch +1 cap 19.
# ═════════════════════════════════════════════════════════════════════════════
walkin("walkin_bedroom_zoe", "Bedtime", "zoe_bedroom",
    "B18, Zoe: in to change for bed, she strips in front of her. Hers on Corruption: look away 0, watch her change +1 cap 19.",
    [here(Z, "zoe_apartment"), flag("zoe_met")],
    [P("You're looking at the polaroids round Zoe's mirror when she comes in behind you and kicks the door shut."),
     D(Z, "Bedtime. Don't mind me.")],
    "She starts undressing.",
    [P("She pulls her top over her head and drops it on the floor. Then her bra. Her tits come free, round and heavy, her nipples tight in the cool of the room."),
     P("She hooks her thumbs in her shorts and pushes them down, and steps out of them in just her knickers, and takes her time finding a sleep shirt."),
     P("She catches you in the mirror."),
     D(Z, "Nope. Eyes stay.")],
    [go("Look away.", node="b_away", mins=2),
     go("Watch her change.", node="b_watch", mins=5, eff=[pay("corruption", 19)])],
    records=["zoe_changed_in_front"], extra=[
        res("b_away", "Look away", [P("You look at the polaroids. Your face is hot. Behind you she laughs, softly."), D(Z, "Chicken.")],
            "Leave her to sleep.", "zoe_apartment", 2),
        res("b_watch", "Watch", [P("You watch. She turns round so you get all of it: her tits, her stomach, the line of her knickers low on her hips. She stretches with her arms over her head, slow, and her tits lift."),
                                 P("Then she pulls the sleep shirt on, and her nipples poke through it."),
                                 D(Z, "Enjoy that?"),
                                 T("You did. She knows you did.")],
            "Leave her to sleep.", "zoe_apartment", 2)],
    when=[wd(0, 1, 2, 3), tod("21:45", "22:00")])
rule("zoe_bedroom_look", "walkin_bedroom_zoe", 0.25, here(Z, "zoe_apartment"), wd(0, 1, 2, 3), tod("21:45", "22:00"))

# ═════════════════════════════════════════════════════════════════════════════
# B19 · VANCE'S HOUSE (host vance_house_look): Vance comes out onto his porch, 18:00-18:15 (he's in his house on his
# row), and looks at her legs; his lines by Lust like his porch hub. His Lust +2 on the moment. Hers on Exhibitionism:
# walk on 0, stay where he can see (Daring) +1 cap 39. Bare legs only, like the front step (B8).
# ═════════════════════════════════════════════════════════════════════════════
walkin("walkin_house_vance", "Out on his porch", "vance_house",
    "B19, Vance: he comes out onto his porch and looks at her legs on the pavement. His Lust +2 on the moment; hers on Exhibitionism: walk on 0, stay where he can see (Daring) +1 cap 39.",
    [here(V, "vance_house"), flag("vance_met"), *BARE_LEGS],
    [P("You're on the pavement looking up at the house next door when the front door opens. Vance comes out onto his porch with his paper and lowers himself into the rocking chair.")],
    "He looks at your legs.",
    [P("He doesn't open the paper. He looks at your bare legs, from your ankles all the way up, and takes his time."),
     G(cond(SKIRT), P("From up on the porch, in this skirt, he can see right up your thighs.")),
     GC(cond(ntrait(V, "want", "lt", 30)), P("He nods, once. That's all you get.")),
     GC(cond(ntrait(V, "want", "lt", 60)), P("He folds the paper on his knee, the way he does now when it's you, and looks at your legs like he's doing sums."),
        D(V, "Evening, Miss.")),
     GC(cond(*ANY), P("He leans forward in the chair and lets you see him look. Your legs, your hips, your tits."),
        D(V, "Turn round for me, Miss. Let an old man see what Mark's got living under his roof."))],
    [go("Walk on.", loc="street", mins=2),
     go("Stay where he can see your legs.", node="v_stay", mins=10, cond_=cond(DARING), eff=[pay("exhibitionism", 39)])],
    raise_=[lust(V)], records=["vance_porch_look"], extra=[
        res("v_stay", "Where he can see", [P("You stay. You lean back against his gatepost with one knee bent, your bare legs right where he can see them, and you don't look at him."),
                                           P("The rocking chair stops rocking. Your face goes hot, and your nipples go tight."),
                                           D(V, "Nice. Very nice."),
                                           P("When you finally walk on, you can feel his eyes on your ass all the way down the street.")],
            "Walk on.", "street", 5)],
    when=[tod("18:00", "18:15")])
rule("vance_house_look", "walkin_house_vance", 0.25, here(V, "vance_house"), tod("18:00", "18:15"))

# ═════════════════════════════════════════════════════════════════════════════
# B20 · THE FIVE OFFICE DOORS (hosts door_grade_*, door_dean_notice): the person in each office opens the door while
# she reads her grade. Each office is open only in its person's office hours, and the rule reads them in it. One
# screen, a line, no pay; `<person>_door_seen`, read once by their office hub.
# ═════════════════════════════════════════════════════════════════════════════
one_screen("walkin_door_art", "The door opens", "art_office",
    "B20, the art lecturer: she opens her door and looks at her the way she looks at the model. No pay.",
    [here(ART, "art_office"), flag("art_lecturer_met")],
    [P("You're reading your grade when the door opens under your finger. The art lecturer, with a mug in her hand."),
     P("She stops and looks at you with her head on one side, the way she looks at the model before she draws: your shoulders, your hips, the length of your legs, the shape of your tits under what you're wearing. Measuring."),
     D(ART, "Hold that. Don't move. Hm. Another time.")],
    "Step back.", "art_office", ["art_door_seen"])
one_screen("walkin_door_ta", "The door opens", "ta_office",
    "B20, the TA: she opens her door, looks her over and catches herself. No pay.",
    [here(TA, "ta_office"), flag("bio_ta_met")],
    [P("The half-open door swings wide. The TA, with her kettle."),
     P("Her eyes go down you, all the way down, your tits, your legs, and snap back up to your face. Her neck goes pink."),
     D(TA, "Oh! Hi. It's, um. It's up to date. The grades. Sorry.")],
    "Step back.", "ta_office", ["ta_door_seen"])
one_screen("walkin_door_dean", "The door opens", "dean_office",
    "B20, the dean: he opens his door and reads her clothes. No pay.",
    [here(DEAN, "dean_office"), flag("dean_met")],
    [P("The heavy door opens while you're reading the notice. The dean, a file under his arm."),
     G(DARING_STATE, P("He looks you down and up, once, slowly."), D(DEAN, "Is that what you wore to class?")),
     G(cond(slot("bra"), NOT_SKIRT), D(DEAN, "The list is on the door so that you read it, @player. Read it and move along."))],
    "Step back into the corridor.", "faculty_floor", ["dean_door_seen"])
one_screen("walkin_door_hale", "The door opens", "hale_office",
    "B20, Dr. Hale: he opens his door in his Thursday hours; his line by his step. No pay.",
    [here(H, "hale_office"), flag("hale_met")],
    [P("You've got your finger on your grade when Dr. Hale opens his door."),
     G(cond(trait("hale_step", "lt", 3)), P("He sees you there, and his eyes go down your legs before they come back up to your face."),
       D(H, "Checking up on me, @player?")),
     G(cond(trait("hale_step", "gte", 3)), P("He doesn't step out. He holds the door open and waits, and his eyes go to your mouth."),
       D(H, "Come in or don't, @player. Don't stand in my doorway."))],
    "Step back.", "hale_office", ["hale_door_seen"])
one_screen("walkin_door_business", "The door opens", "business_office",
    "B20, the Business lecturer: he opens his door and looks at the grade, not at her. No pay.",
    [here(BUS, "business_office"), flag("business_lecturer_met")],
    [P("The door opens. The Business lecturer looks at the grade sheet, then at your number on it, and not at you once."),
     G(cond(trait("grade_business", "lt", 40)), D(BUS, "Retakes by appointment.")),
     G(cond(trait("grade_business", "gte", 40)), D(BUS, "It's accurate. They all are."))],
    "Step back.", "business_office", ["business_door_seen"])
for host, cid, npc, office in (("door_grade_art", "walkin_door_art", ART, "art_office"),
                               ("door_grade_bio", "walkin_door_ta", TA, "ta_office"),
                               ("door_dean_notice", "walkin_door_dean", DEAN, "dean_office"),
                               ("door_grade_psych", "walkin_door_hale", H, "hale_office"),
                               ("door_grade_business", "walkin_door_business", BUS, "business_office")):
    rule(host, cid, 0.25, here(npc, office))

# The hub lines that read the flags (proposal B9 and B20: "read by his/their hub"): Gary for two days, an office hub
# in the hour after its door (she goes in straight from it).
HUB_READS = {
    "hub_gary_booth": G(cond(flag("gary_sat_with_her"), since("gary_sat_with_her", "lt", 48)),
                        D(GY, "Sit with me again sometime, sweetheart. My knee's been cold.")),
    "hub_art_office": G(cond(flag("art_door_seen"), since("art_door_seen", "lt", 1)),
                        D(ART, "You stood very well at my door. Remember how.")),
    "hub_ta_office": G(cond(flag("ta_door_seen"), since("ta_door_seen", "lt", 1)),
                       D(TA, "Sorry about the door. I wasn't staring. I was. Sorry.")),
    "hub_dean_office": G(cond(flag("dean_door_seen"), since("dean_door_seen", "lt", 1)),
                         D(DEAN, "You read the notice very closely, @player. Good. That is what it is for.")),
    "hub_hale_office": G(cond(flag("hale_door_seen"), since("hale_door_seen", "lt", 1)),
                         D(H, "You were reading your grade very carefully.")),
    "hub_business_office": G(cond(flag("business_door_seen"), since("business_door_seen", "lt", 1)),
                             D(BUS, "You read it. Good. Now earn the next one.")),
}


def hub_read(out):
    """Put each hub's flag line at the end of its first screen's text (hubs not in `out` are skipped)."""
    for c in out:
        if c.get("id") in HUB_READS:
            c["nodes"][0]["blocks"].append(HUB_READS[c["id"]])


def attach(out):
    """Put each host's rules on its canvas in `out`; returns the ids attached."""
    done = set()
    for c in out:
        if c.get("id") in RULES and c["id"] not in TOML_HOSTS:
            c["trigger"]["substitutions"] = list(c["trigger"].get("substitutions") or []) + RULES[c["id"]]
            done.add(c["id"])
    return done


def check_toml_hosts(path):
    """The 3_activities.toml hosts must carry exactly RULES (written by hand there; this stops drift)."""
    import tomllib
    doc = tomllib.load(open(path, "rb"))
    by_id = {c["id"]: c for c in doc.get("canvases") or []}
    for host in TOML_HOSTS:
        have = (by_id[host].get("trigger") or {}).get("substitutions") or []
        assert have == RULES[host], f"3_activities.toml {host}: substitutions differ from walkins_out.RULES"


def toml_line(host):
    """The `substitutions = [...]` line for a 3_activities.toml host (what was pasted there)."""
    from tomlw import v
    return f"substitutions = {v(RULES[host])}"
