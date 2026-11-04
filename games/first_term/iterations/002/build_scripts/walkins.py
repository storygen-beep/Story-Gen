"""The walk-ins at home (heat proposal 2026-11-03, B1-B8; DECISIONS 147, chunk 1).

The engine's walk-in (the-surfaces.md R3, v2.py checkAndSubstituteCanvas): the solo activity she clicks
carries trigger.substitutions; on entry the engine rolls, and on a hit it shows a walk-in canvas instead.
Each walk-in canvas here is substitution_only with its own location (getCanvasById indexes only located
canvases), and none carries requires_npc: the walker is in another room when the roll happens, so the
canvas's own trigger reads WHERE HE IS NOW (an npc_at_location item) and each rule reads the time his next
row brings him into her room. One canvas per walker, so his presence is one AND item on the trigger
(conditions don't nest) and every line naming him is backed by it.

The pay rule (proposal B, H5, DECISIONS 143):
- screen 1 is the moment: her activity and the door opening. Its ONLY exit carries his Lust +2 (Ryan, Mark,
  Vance; nobody else here has a Lust meter) and sets the walk-in's daily flag, so the raise is on what
  happened and never on her answer;
- screen 2 is her answer: the first button is the cover and pays 0; one bolder button per band pays her
  +1, capped at that band's top;
- odds 0.25 (DECISIONS 59), 0.5 while the shower door is left unlocked (C4) or the TV sound is up (C2);
- once a day per walk-in: `<canvas>_today`, cleared in [engine.daily_tick].

Mark is looks only this release (DECISIONS 107), and every Mark walk-in waits for `mark_saw_her` so the
dryer stays his first accident (H2). Built, then not built, as written in the proposal: see DECISIONS 147.

DECISIONS 152 (LO, 2026-11-03) gave Mark two Saturday rows (bed to 08:30, coffee in the kitchen to 09:00) and with them
B2 Saturday, B4 Saturday and B6 Mark. Each host needs his room empty, so each rule reads the 15 minutes before the row
that brings him in (08:15, 08:45, 21:45), the way B4's weekday rule does; Ryan's Saturday kitchen window ends at 08:15.
"""
import copy
from canv import *
from tomlw import tod, wd
from home_items import here, npc_add, since, CURIOUS, BOLD, DARING, SHOWING

L, M, R, K, V = "npc_laura", "npc_mark", "npc_ryan", "npc_kayla", "npc_vance"


def slot(s, on=True):
    return {"type": "clothing_slot", "slot": s, "operator": "equipped" if on else "unequipped"}


def wt(v):
    return {"type": "worn_type", "operator": "eq", "value": v}


def pay(meter, cap):
    return {"targetType": "player", "trait": meter, "op": "add", "value": 1, "cap": cap}


def lust(npc):
    return npc_add(npc, "want", 2)


ANY = [{"type": "worn_exposure", "operator": "gte", "value": 0}]          # always true: a chain's else
SAW_ = flag("mark_saw_her")   # every Mark walk-in waits for his first accident (the dryer, H2)
COVERED = [{"type": "worn_exposure", "operator": "eq", "value": 0}]
NAKED = [slot("top", False), slot("bottom", False), slot("dress", False), slot("bra", False), slot("underwear", False)]
UNDIES = [slot("bra"), slot("underwear"), slot("top", False), slot("bottom", False), slot("dress", False)]
TOWEL = wt("towel")
SKIRT = wt("short_skirt")
BARE_LEGS = [{"type": "clothing_item", "item_id": "jeans", "operator": "unequipped"},
             {"type": "clothing_item", "item_id": "leggings", "operator": "unequipped"}]

# her meters' bands (DECISIONS 124: Good Girl / Curious / Bold; Covered / Daring / Showing)
E_COV = [trait("exhibitionism", "lt", 20)]
E_DAR = [trait("exhibitionism", "gte", 20), trait("exhibitionism", "lt", 40)]
E_SHO = [SHOWING]
C_GG = [trait("corruption", "lt", 20)]
C_CUR = [trait("corruption", "gte", 20), trait("corruption", "lt", 40)]

UNLOCKED = flag("shower_unlocked")
LOCKED = flag("shower_unlocked", False)
TV_LOUD = flag("tv_loud")
TV_QUIET = flag("tv_loud", False)

# the shower's own finish (home.py bathroom_shower): stripped, a towel on, hygiene +50
STRIP = [REMEMBER] + [{"action": "unequip", "item_id": g} for g in ALL_GARMENTS if g not in ("sneakers", "towel")]
SHOWER_DONE = dict(eff=[{"targetType": "player", "trait": "hygiene", "op": "add", "value": 50, "cap": 100}],
                   wardrobe=[{"action": "equip", "item_id": "towel"}])

CANVASES = []
RULES = {}          # host canvas id -> [substitution rules]
DAILY_FLAGS = []    # every `<canvas>_today`, for 0_systems_spec.toml [engine.daily_tick]


# (pass 3 D52) the meter each walk-in's answers pay (its description: "her answer on ..."); its odds band on it.
# Laundry routes into Mark's laundry ladder, whose rungs open on Curious (Corruption). Laura's and Kayla's carry no
# heat and no pay, so they stay flat.
BAND_ON = {"walkin_shower_ryan": "exhibitionism", "walkin_shower_kayla": "exhibitionism", "walkin_shower_mark": "exhibitionism",
           "walkin_mirror_ryan": "exhibitionism", "walkin_mirror_mark": "exhibitionism", "walkin_wardrobe_mark": "exhibitionism",
           "walkin_step_vance": "exhibitionism",
           "walkin_kitchen_ryan": "corruption", "walkin_kitchen_mark": "corruption", "walkin_tv_ryan": "corruption",
           "walkin_tv_mark_garage": "corruption", "walkin_tv_mark_kitchen": "corruption", "walkin_things_ryan": "corruption",
           "walkin_laundry_mark": "corruption", "walkin_laundry_mark_sat": "corruption",
           "walkin_nap_ryan": "exhibitionism", "walkin_garden_mark": "exhibitionism"}


def rule(host, target, chance, *items):
    for odds, band in odds_bands(BAND_ON.get(target), chance):
        RULES.setdefault(host, []).append({"target_canvas_id": target, "chance": odds, "conditions": cond(*items, *band)})


def walkin(cid, name, loc, desc, who, moment, moment_label, answer, answers, raise_=(), records=(), extra=(),
           also_set=(), when=(), moment_wardrobe=None, moment_mins=2):
    """One walker's walk-in: `who` = trigger items (his presence now, met flags, his gates).
    `moment_mins`: the clock on the moment's button (the nap spends its two hours there, B21)."""
    today = f"{cid}_today"
    DAILY_FLAGS.append(today)
    CANVASES.append({
        "id": cid, "name": name, "description": desc,
        "trigger": {"location": loc, "is_repeatable": True, "priority": 1, "is_active": True,
                    "substitution_only": True,
                    "conditions": cond(flag("opening_done"), flag(today, False), *who, *when)},
        "nodes": [node("moment", name, moment,
                       [go(moment_label, node="answer", mins=moment_mins, eff=list(raise_), wardrobe=moment_wardrobe,
                           flags=[fset(today)] + [fset(f) for f in records] + list(also_set))]),
                  node("answer", name, answer, answers), *extra]})
    return cid


def res(nid, name, blocks, label, dest, mins, **kw):
    """A result screen after her answer: what he does, then out."""
    return node(nid, name, blocks, [go(label, loc=dest, mins=mins, **kw)])


# ═════════════════════════════════════════════════════════════════════════════
# B1 · THE SHOWER (host bathroom_shower). Ryan from his room, Kayla on a Friday, Mark from the garage.
# The lock: it sticks halfway (the opening's fact); while `shower_unlocked` is set (C4) she left it off.
# ═════════════════════════════════════════════════════════════════════════════
def shower_in(locked, unlocked, water):
    """The shower's setup, worded per walker (gate `one pool, one place`): the lock by `shower_unlocked`, then the water."""
    return [GC(cond(LOCKED), P(locked)), GC(cond(UNLOCKED), P(unlocked)), P(water)]


def unlock_line(text):
    return G(cond(UNLOCKED), T(text))


def shower_answers(prefix, who_name, cover, gg, dar, sho):
    """The four answers on Exhibitionism: (label, blocks) per band; each finishes the shower."""
    ans = [go("Grab the towel.", node=f"{prefix}_cover", mins=2)]
    ans.append(go("Don't grab it straight away.", node=f"{prefix}_cov", mins=2, cond_=cond(*E_COV), eff=[pay("exhibitionism", 19)]))
    ans.append(go("Keep washing.", node=f"{prefix}_dar", mins=5, cond_=cond(*E_DAR), eff=[pay("exhibitionism", 39)]))
    ans.append(go("Turn round.", node=f"{prefix}_sho", mins=5, cond_=cond(*E_SHO), eff=[pay("exhibitionism", 59)]))
    nodes = [res(f"{prefix}_cover", "The towel", cover, "Dry off.", "home_bathroom", 15, **SHOWER_DONE),
             res(f"{prefix}_cov", "Not straight away", gg, "Dry off.", "home_bathroom", 15, **SHOWER_DONE),
             res(f"{prefix}_dar", "Keep washing", dar, "Dry off.", "home_bathroom", 15, **SHOWER_DONE),
             res(f"{prefix}_sho", "Turn round", sho, "Dry off.", "home_bathroom", 15, **SHOWER_DONE)]
    return ans, nodes


a, n = shower_answers("r",
    "Ryan",
    [P("You grab the towel off the rail and clutch it over your tits. Ryan backs out with one hand over the front of his shorts."),
     ME("Ryan! Knock, for fuck's sake!"), D(R, "Sorry. Sorry. The lock, it's, I thought it was locked."),
     ME("Get out!"), D(R, "Going. I'm going."), P("The door bangs shut. His door bangs across the hall a second later.")],
    [P("You don't grab it. Not straight away. You stand under the water and let him look, one second, two, your tits wet, your nipples hard. His mouth opens."),
     D(R, "I. Uh. Toothbrush."), ME("It's on the sink, Ryan. Where it always is."), D(R, "Right. Yeah. Right."),
     P("Then you reach for the towel, slow. He backs out with his toothbrush still in his fist and the front of his shorts tented.")],
    [P("You don't cover up. You turn your face back into the spray and soap yourself, slow, your hands over your tits and down your stomach, like he isn't there."),
     P("He stays. You can hear him breathing over the water. When you look round, his hand is pressed flat over the bulge in his shorts."),
     ME("You can wait outside, you know."), D(R, "Jesus Christ, @player.nickname. You're not even going to cover up?"),
     ME("It's my shower. You walked in."), P("The door swings shut behind him.")],
    [P("You turn round under the water, slow, and give him your back and your wet ass. You bend for the soap and take your time coming up."),
     P("The door frame creaks where he's gripping it."), ME("Seen enough?"), D(R, "You're killing me. You know that? You're actually killing me."),
     P("He goes. His door slams across the hall."), T("He'll be thinking about your ass for hours. Good.")])
walkin("walkin_shower_ryan", "The door opens", "home_bathroom",
    "B1, Ryan: from his room, for his toothbrush, he walks in on her in the shower. His Lust +2 on the moment; her answer on Exhibitionism: the towel 0, then +1 cap 19 / 39 / 59.",
    [here(R, "home_ryan_room")],
    shower_in("You lock the door, but the lock sticks halfway like always. You strip and step under the water.",
              "You don't touch the lock. You left it off, and you leave it off now. You strip and step under the water.",
              "It runs hot down your back and over your tits. You stand there with your eyes shut and your hands in your wet hair.")
    + [P("The door opens. Ryan walks in for his toothbrush, head down, and stops dead.")],
    "He's seen you.",
    [P("You're naked and wet three feet from him. His eyes go straight to your tits, then down, all the way down, and come back up slow."),
     GC(cond(ntrait(R, "want", "lt", 40)), P("He goes red to the ears. He turns side-on, too late. The front of his shorts is already tenting."), D(R, "Shit. Sorry. I didn't. The lock. I didn't know you were in here."), ME("Well, now you know.")),
     GC(cond(*ANY), P("He doesn't go red. He leans on the door frame and keeps looking at your tits. His cock is hard in his shorts, and he doesn't turn it away."), D(R, "Don't mind me. I'm just getting my toothbrush."), ME("Your toothbrush is on the sink, Ryan.")),
     unlock_line("You left the door unlocked for this. For somebody to walk through it."),
     VID("a young man frozen in a bathroom doorway, a naked girl in the shower looking back at him", "brother walks in on sister in shower", "guy walks in on naked girl showering", pool_dir="sex/walkin_shower_ryan_t4")],
    a, raise_=[lust(R)], records=["ryan_walked_in_shower"], extra=n, moment_wardrobe=STRIP)

a, n = shower_answers("k",
    "Kayla",
    [P("You grab the towel and hold it over your tits. Kayla grins and pads back across the hall in his shirt."), D(K, "Shy. Cute."), ME("Do you mind?"), D(K, "Not at all.")],
    [P("You don't grab it straight away. You let her look a second longer, your nipples hard, the water running off your tits."),
     D(K, "Nice tits. Ryan never said."), ME("Why would Ryan say anything about my tits?"), D(K, "Good question. I'll ask him."), P("She winks and goes. You grab the towel with your face on fire.")],
    [P("You keep washing. You soap your tits, slow, while she watches from the sink with her arms folded."),
     D(K, "Okay. Now I see what all the fuss is about."), ME("What fuss?"), D(K, "Ask your brother. Not tonight, though. Tonight he's mine."), P("She leaves the door open behind her.")],   # scene reader b03: the not-yet
    [P("You turn round under the water and give her your wet ass. Kayla laughs, low."),
     D(K, "Oh, you're trouble. Does he know you're trouble?"), ME("Who?"), D(K, "Don't play dumb with me, @player.nickname. Shake that ass at him and you'll have me to deal with."), P("She smacks the door frame on her way out. You stand there wet and grinning, nipples hard.")])
walkin("walkin_shower_kayla", "The door opens", "home_bathroom",
    "B1, Kayla: a Friday with Ryan, she comes in to pee and looks her over. No meter moves for her; kayla_saw_her (Ryan's hub reads it). Her answer on Exhibitionism: the towel 0, then +1 cap 19 / 39 / 59.",
    # (pass 3 group 2, round 2) she walks in from Ryan's room, where her Friday row holds her (people_data.py):
    # the trigger reads her there, as Ryan's own walk-in reads him, so the engine only runs it while she is across the hall
    [here(R, "home_ryan_room"), here(K, "home_ryan_room"), flag("kayla_met")],
    shower_in("You shove the lock across. It sticks halfway, the way it always does. You peel your clothes off and get under the spray.",
              "You leave the lock alone. It's been off since last time. You peel your clothes off and get under the spray.",
              "Across the hall Ryan's music thumps. You tip your head back and let the hot water run over your face and down between your tits.")
    + [P("The door opens. A girl with long dark hair walks in, in one of Ryan's T-shirts and nothing else. Kayla. She doesn't stop.")],
    "She sits down to pee.",
    [P("She pees with the shower running and looks you over the whole time, from your wet tits down to your pussy and back up."),
     D(K, "Oh, hi. Don't mind me. I couldn't hold it."),
     P("She flushes and doesn't leave. She leans on the sink and looks at your tits like she's comparing."),
     D(K, "Look at you, step-sister."), ME("And you're in my bathroom."),   # scene reader b03: true on every Friday, not only the first D(K, "Our bathroom, Fridays. Get used to it."),
     unlock_line("You left the lock off. Somebody was always going to use it."),
     VID("a girl in a man's T-shirt leaning on a bathroom sink, a naked girl in the shower", "girlfriend walks in on girl in shower", "girl watches naked girl shower bathroom", pool_dir="sex/walkin_shower_kayla_t4")],
    a, records=["kayla_saw_her"], extra=n, moment_wardrobe=STRIP, when=[wd(4), tod("18:00", "22:00")])

a, n = shower_answers("m",
    "Mark",
    [P("You grab the towel and hold it over your tits. Mark finishes at the sink, slow, and dries his hands on his jeans."),
     ME("Mark. I'm in the shower."), D(M, "I can see that. Mind the hot water. It's not free."), P("He goes, and leaves gray fingerprints on the door.")],
    [P("You don't grab it straight away. You stand there under the water and let him see it, your tits, your nipples hard, the water running down between your legs."),
     GC(cond(ntrait(M, "want", "lt", 20)), P("In the mirror his eyes find you, once, and drop to the drain. He scrubs at a knuckle that's already clean."),
        D(M, "Lock's broken. I'll fix it. Tonight."), P("Then you reach for the towel, and he turns the tap off without looking up.")),
     GC(cond(*ANY), P("In the mirror his eyes never leave you. Then you reach for the towel, and he turns the tap off."), D(M, "Lock's broken. I'll fix it. Maybe."))],
    [P("You keep washing. You soap your tits and your stomach, slow, while he scrubs his hands at the sink and watches you in the mirror."),
     GC(cond(ntrait(M, "want", "lt", 20)), P("He scrubs a long time with his eyes on the tiles. The front of his jeans is tight, and he turns his hip into the sink so you won't see it."),
        D(M, "Grease. Gets everywhere."), ME("I can see that, Mark."), D(M, "Don't be smart.")),
     GC(cond(*ANY), P("He scrubs a long time. The front of his jeans is tight. He doesn't hide it."), D(M, "You're your mother's girl, all right."), ME("Meaning what?"), D(M, "Meaning you know exactly what you're doing.")),
     P("He goes back down to the garage, and the radio comes on loud.")],
    [P("You turn round under the water and give him your back and your wet ass, and you don't hurry."),
     P("Behind you the tap stops running."), D(M, "Christ, @player. Anybody could walk in on this."), ME("You did."),
     P("When you look, he's gone, and the door's wide open.")])
walkin("walkin_shower_mark", "The door opens", "home_bathroom",
    "B1, Mark: up from the garage for the sink, he walks in on her in the shower; after mark_saw_her (the dryer stays first). His Lust +2 on the moment; her answer on Exhibitionism: the towel 0, then +1 cap 19 / 39 / 59.",
    [here(M, "home_garage"), flag("mark_saw_her")],
    shower_in("The lock catches halfway and sticks. You leave it. You strip off and step into the hot water.",
              "The lock's still off from last time, but you don't fix it. You strip off and step into the hot water.",
              "Down the hall Mark's radio is on in the garage. You soap your tits and your stomach with your eyes shut.")
    + [P("The door opens. Mark walks in with grease to his elbows, heading for the sink. He stops.")],
    "He's seen you.",
    [P("You're naked under the water. His eyes go to your tits and stay there. Then lower, to your pussy, and they stay there too."),
     # H7 (pass 3 A70): at his low Want he looks, catches himself and puts his eyes on the wall (npc_mark.md "one look, then the wall")
     GC(cond(ntrait(M, "want", "lt", 20)), P("Then he catches himself. He turns to the sink, hard, and puts his eyes on the tiles above the tap. He turns his hip to you, so the front of his jeans faces the wall."),
        D(M, "Sink's the only one with hot water. I'll be one minute. Don't."), ME("Don't what?"), D(M, "Don't stand there like that. Wash, girl.")),
     GC(cond(ntrait(M, "want", "lt", 50)), P("He doesn't look away. He turns the tap on at the sink and scrubs his hands, and in the mirror his eyes are on you the whole time."),
        D(M, "Sink's the only one with hot water. Don't mind me.")),
     GC(cond(*ANY), P("He doesn't look away. He turns the tap on at the sink and scrubs his hands, and in the mirror his eyes are on you the whole time."),
        D(M, "Don't stop on my account.")),
     unlock_line("You left the lock off, and he walked right in. You knew he might."),
     VID("a middle-aged man at a bathroom sink watching a naked girl in the shower in the mirror", "stepdad walks in on girl in shower", "man watches naked girl shower mirror", pool_dir="sex/walkin_shower_mark_t4")],
    # reader batch 4 (pass 3): not while Laura has the bathroom (her Saturday shower row, 16:30-17:00)
    a, raise_=[lust(M)], records=["mark_walked_in_shower"], extra=n, moment_wardrobe=STRIP, when=[wd(5), tod("14:00", "17:00"), here(L, "home_bathroom", False)])

# The odds: Ryan Sun-Thu evenings and weekend mornings while he's awake in his room; Kayla on a Friday with him;
# Mark on a Saturday afternoon, once Ryan's weekend row has him down at the TV (14:00), so no two can race.
for chance, lock in ((0.25, LOCKED), (0.5, UNLOCKED)):
    rule("bathroom_shower", "walkin_shower_ryan", chance, lock, here(R, "home_ryan_room"), wd(6, 0, 1, 2, 3), tod("19:00", "00:00"))
    rule("bathroom_shower", "walkin_shower_ryan", chance, lock, here(R, "home_ryan_room"), wd(5, 6), tod("07:30", "14:00"))
    rule("bathroom_shower", "walkin_shower_kayla", chance, lock, here(R, "home_ryan_room"), wd(4), tod("18:00", "22:00"))
    rule("bathroom_shower", "walkin_shower_mark", chance, lock, here(M, "home_garage"), here(L, "home_bathroom", False), wd(5), tod("14:00", "17:00"))

# ═════════════════════════════════════════════════════════════════════════════
# B2 · THE KITCHEN (hosts kitchen_breakfast, kitchen_coffee; the kitchen empty). Ryan, a weekend morning.
# A brush is stage 1 (H1): "Don't move." is her staying (Good Girl, then Curious); pushing back is a touch (Bold).
# ═════════════════════════════════════════════════════════════════════════════
walkin("walkin_kitchen_ryan", "Reaching past", "home_kitchen",
    "B2, Ryan: down from his room in his boxers on a weekend morning, he reaches over her for a mug and his morning wood presses into her ass. His Lust +2 on the moment; her answer on Corruption: step aside 0, stay +1 cap 19 / 39, push back (Bold) +1 cap 59.",
    [here(R, "home_ryan_room")],
    [P("You're at the counter with the kettle on, the kitchen to yourself. Ryan comes in from the hall in his boxers, half asleep, his hair everywhere."),   # pass 4 reader: one hall, no stairs (Q7)
     P("He reaches over you for a mug off the top shelf. His chest is against your back. His morning wood presses right into your ass.")],
    "He freezes.",
    [P("He feels it the same second you do. Neither of you moves. His cock is hard against your ass through his boxers, and his breath is hot on your neck."),
     GC(cond(ntrait(R, "want", "lt", 40)), P("Then he jerks his hips back and turns side-on, the mug held low in front of him, red to the ears."), D(R, "Morning. Sorry. Morning. That was the counter."), ME("Sure, Ryan. The counter.")),
     GC(cond(*ANY), P("He doesn't jerk back. He stays pressed to you one second longer than the mug needs, then reaches past you, slow."), D(R, "Morning, @player.nickname. Sleep well?"), ME("Better than you, by the feel of it.")),
     VID("a young man in boxers reaching over a girl at a kitchen counter for a mug, pressed against her from behind", "brother presses against sister kitchen counter morning", "guy morning wood presses girl kitchen", pool_dir="sex/walkin_kitchen_ryan_t4")],
    [go("Step aside.", node="r_aside", mins=2),
     go("Don't move.", node="r_stay", mins=2, cond_=cond(*C_GG), eff=[pay("corruption", 19)]),
     go("Don't move.", node="r_stay", mins=2, cond_=cond(*C_CUR), eff=[pay("corruption", 39)]),
     go("Push back into him.", node="r_push", mins=2, cond_=cond(BOLD), eff=[pay("corruption", 59)])],
    raise_=[lust(R)], records=["ryan_brushed_kitchen"], when=[wd(5, 6), tod("07:30", "10:00")], extra=[
        res("r_aside", "Step aside", [P("You duck out from under his arm and take your coffee to the window."), ME("Kettle's just boiled. Help yourself."), D(R, "Yeah. Thanks. I'll, yeah."),
                                      P("Behind you he fills his mug and goes back to his room fast, the mug in front of his boxers."),
                                      P("Next weekend he'll come in for a mug again. You'll know to listen for him.")],   # pass 4 reader: the hook
            "Drink your coffee.", "home_kitchen", 10),
        res("r_stay", "Don't move", [P("You don't move. You stand there with his cock pressed into your ass and let him feel you not moving. Your nipples go hard."),
                                     D(R, "@player.nickname. You're. You're not moving."), ME("Neither are you."),
                                     P("He breathes out, shaky, and steps back. He takes his mug back to his room and doesn't look at you once."),
                                     T("He felt you stay. He knows you felt him."),
                                     P("Next weekend he'll come in for a mug again, and you'll be at this counter.")],   # pass 4 reader: the hook
            "Drink your coffee.", "home_kitchen", 10),
        res("r_push", "Push back into him", [P("You push back into him. Your ass grinds right back against his cock, slow, once, and his hand grips the edge of the counter beside yours."),
                                             D(R, "Jesus, @player.nickname. Anybody could walk in."), ME("Then be quick about it."),
                                             P("He pulls away like it burns, the mug forgotten on the shelf, and goes back down the hall with his hand over his boxers."),
                                             D(R, "Next weekend I'm coming in for that mug again. You be at this counter.")],   # scene reader b02: the hook
            "Drink your coffee.", "home_kitchen", 10)])
# Ryan's Saturday window stops where Mark's starts (DECISIONS 152), so the two never overlap; Sunday stays 07:30-10:00.
for host in ("kitchen_breakfast", "kitchen_coffee"):
    rule(host, "walkin_kitchen_ryan", 0.25, here(R, "home_ryan_room"), wd(5), tod("07:30", "08:15"))
    rule(host, "walkin_kitchen_ryan", 0.25, here(R, "home_ryan_room"), wd(6), tod("07:30", "10:00"))

# B2 Saturday, Mark (DECISIONS 152): sleeping in until 08:30, then coffee at the counter before the garage. The kitchen
# hosts need the kitchen empty (home.py KITCHEN_EMPTY), and the engine rolls with the clock where it is when she
# clicks (v2.py checkAndSubstituteCanvas), so his arrival is the walk-in: the rule reads him upstairs in bed in the 15
# minutes before his kitchen row, as B4 reads him at dinner before his garage row. Looks and brushes only (DECISIONS 107).
walkin("walkin_kitchen_mark", "Reaching past", "home_kitchen",
    "B2, Mark: down from sleeping in on a Saturday for his coffee, he puts his hand on her hip to get past her at the counter; after mark_saw_her. His Lust +2 on the moment; her answer on Corruption: step aside 0, stay +1 cap 19 / 39, push back (Bold) +1 cap 59.",
    [here(M, "home_master_bedroom"), SAW_],
    [P("Saturday. You're at the counter with the kettle on and the kitchen to yourself. Down the hall a bed creaks, then a door."),
     P("Mark comes in barefoot in yesterday's jeans, his hair flat on one side from the pillow. He wants the coffee jar, and you're standing in front of it."),
     P("He doesn't ask you to move. His hand goes flat on your hip, big and warm, and he steps in behind you to reach past.")],
    "His hand stays.",
    [P("He takes his time with the jar. His hand stays on your hip the whole time, his thumb pressed into the curve of it. His chest is at your back, and the front of his jeans brushes your ass."),
     GC(cond(ntrait(M, "want", "lt", 50)), P("He clears his throat and gets the lid off, slow, like that's what he's doing."), D(M, "Morning, @player. You're in my way."), ME("You could have asked me to move."), D(M, "Could have.")),
     GC(cond(*ANY), P("He doesn't pretend. He looks down over your shoulder, straight down your front, and his fingers spread on your hip."), D(M, "Nice view from up here, @player."), ME("Get your coffee, Mark."), D(M, "I'm getting it.")),
     VID("a middle-aged man behind a girl at a kitchen counter, his hand on her hip, reaching past her", "stepdad hand on hip kitchen counter morning", "man brushes past girl kitchen counter hand on hip", pool_dir="sex/walkin_kitchen_mark_t4")],
    [go("Step aside.", node="m_aside", mins=2),
     go("Don't move.", node="m_stay", mins=2, cond_=cond(*C_GG), eff=[pay("corruption", 19)]),
     go("Don't move.", node="m_stay", mins=2, cond_=cond(*C_CUR), eff=[pay("corruption", 39)]),
     go("Push back into him.", node="m_push", mins=2, cond_=cond(BOLD), eff=[pay("corruption", 59)])],
    raise_=[lust(M)], records=["mark_brushed_kitchen"], when=[wd(5), tod("08:15", "08:30")], extra=[
        res("m_aside", "Step aside", [P("You slide out from under his hand and take your mug to the window."), D(M, "Touchy this morning."), ME("It's Saturday. I'm allowed."),
                                      P("Behind you he spoons his coffee in and leans on the counter to drink it, and you can feel him watching your ass the whole time.")],
            "Drink your coffee.", "home_kitchen", 10),
        res("m_stay", "Don't move", [P("You don't move. You stand there with his hand on your hip and let him take as long as he wants. His thumb presses in once. The front of his jeans grazes your ass again, and your nipples go hard."),
                                     P("Then he steps back with the jar, like nothing happened."),
                                     D(M, "Good girl."), ME("For what?"), D(M, "For staying out of my way."),
                                     T("He felt you stay. He'll remember it.")],
            "Drink your coffee.", "home_kitchen", 10),
        res("m_push", "Push back into him", [P("You push back into him. Your ass presses right into the front of his jeans, and he's hard. His fingers dig into your hip and hold you there."),
                                             D(M, "Careful, @player. You don't know what you're starting."), ME("Maybe I do."),
                                             P("One second. Two. Then he lets go, takes his coffee to the end of the counter and drinks it there, looking at you over the mug like he's working something out.")],
            "Drink your coffee.", "home_kitchen", 10)])
for host in ("kitchen_breakfast", "kitchen_coffee"):
    rule(host, "walkin_kitchen_mark", 0.25, here(M, "home_master_bedroom"), wd(5), tod("08:15", "08:30"))

# ═════════════════════════════════════════════════════════════════════════════
# B3 · THE LIVING ROOM (host living_tv): channel 5 on, someone walks in. C2: the sound up (`tv_loud`) doubles it.
# Mark from the garage (Mon, Tue, Thu, Fri) or the kitchen (Wed), whose late TV row starts at 22:00; Ryan before
# his weekend TV row (14:00); Laura on a Sunday from the kitchen, the cover branch: one line, no heat, no pay.
# ═════════════════════════════════════════════════════════════════════════════
def ch5_in(scene, loud):
    """Channel 5 on, worded per walker: what is on the screen, then the sound (C2's `tv_loud`)."""
    return [P("You drop onto the couch and flick to channel 5. " + scene),
            GC(cond(TV_LOUD), P(loud)), GC(cond(TV_QUIET), P("You keep the sound low, and you keep one eye on the hall door."))]


CH5_ANS = lambda pre: [
    go("Turn it off.", node=f"{pre}_off", mins=2),
    go("Don't reach for the remote yet.", node=f"{pre}_gg", mins=5, cond_=cond(*C_GG), eff=[pay("corruption", 19)]),
    go("Leave it on.", node=f"{pre}_cur", mins=10, cond_=cond(CURIOUS), eff=[pay("corruption", 39)])]


def mark_tv(cid, here_item, from_where, mother_line, when, scene, lines, loud):
    walkin(cid, "Channel 5", "home_living_room",
        f"B3, Mark: in from {from_where} before his late TV row, he finds channel 5 on. His Lust +2 on the moment; her answer on Corruption: off 0, wait +1 cap 19, leave it on (Curious) +1 cap 39.",
        [here_item, flag("mark_saw_her")],
        ch5_in(scene, loud)
        + [P(f"Mark walks in from {from_where} with a beer and stops behind the couch.")],
        "He's seen the screen.",
        [P(lines[0]),
         D(M, "Channel five, @player?"),
         P(lines[1]),
         VID("a man standing behind a couch with a beer, staring, porn on the TV, a girl curled on the couch", "stepdad catches girl watching porn tv", "man walks in on girl watching porn living room", pool_dir=f"sex/{cid}_t5")],
        CH5_ANS("m"), raise_=[lust(M)], records=["mark_caught_ch5"], when=when, extra=[
            res("m_off", "Turn it off", [P("You jab the remote and the screen goes black. Your face is burning."),
                                         ME("I was flicking through. It was just on."),
                                         D(M, "I pay for that channel, you know. I know what's on it."), P("He drinks, but he doesn't take his eyes off you while he does it.")],
                "Get up.", "home_hall", 2),
            res("m_gg", "Not yet", [P(lines[2]),
                                    D(M, "Your mother doesn't watch this one."), ME("I'm not my mother."), D(M, "No. You're not."), P("Then you turn it off. He breathes out through his nose.")],
                "Get up.", "home_hall", 2),
            res("m_cur", "Leave it on", [P(lines[3]), P(lines[4]),
                                         D(M, mother_line), ME("So go to bed, Mark."), P("He says it, but he doesn't go."), D(M, "In a minute."),
                                         VID("porn on a living room TV at night, a girl watching from the couch, a man standing behind her", "girl keeps watching porn while stepdad watches", "watching porn on tv man behind couch", pool_dir=f"sex/{cid}_leave_t5")],
                "Turn it off.", "home_hall", 5)])
    return cid


# Mon, Tue, Thu, Fri 21:30-22:00 Laura is in the kitchen (her evening row); on Wednesday she has no row, she is out
mark_tv("walkin_tv_mark_garage", here(M, "home_garage"), "the garage", "Not with your mother in the house, @player.", [wd(0, 1, 3, 4), tod("21:30", "22:00")],
        "A woman on her knees on a bed, a man behind her, his cock sliding in and out of her. Her tits swing with every thrust.",
        ["He looks at the screen. The man's cock drives into her, and she moans. Then Mark looks down at you.",
         "He doesn't sit. He stands there with the can halfway to his mouth, and the front of his jeans fills.",
         "You don't reach for the remote. Not yet. On screen he grips her hips and pounds her, and the two of you watch it together, Mark standing, you on the couch with your face hot and your nipples tight.",
         "You leave it on. You don't look at him. On screen she's on her back now, legs up, and he drives into her slow and deep, his cock shining every time it slides out.",
         "Behind you Mark doesn't move. The beer can creaks in his fist. You're wet, and you squeeze your thighs together and keep watching."],
        "You left the sound up from earlier. Her moans fill the room and carry out to the garage door.")
mark_tv("walkin_tv_mark_kitchen", here(M, "home_kitchen"), "the kitchen", "Your mother'll be back, @player.", [wd(2), tod("21:30", "22:00")],
        "Two women on a couch with one man between them. One rides his cock while the other one kisses her tits.",
        ["He smells of chilli and beer. He looks at the screen, at the girl bouncing on that cock, and then at you, curled up in front of it.",
         "He leans on the back of the couch with both hands. The bulge in his jeans is right there at the edge of your eye, and he doesn't move it.",
         "You don't reach for the remote. Not yet. On screen the girl on top comes, loud, and the other one licks her nipple. Mark breathes out hard over your head. Your face is burning, and your nipples are tight.",
         "You leave it on. On screen they swap, and the second girl sinks down on his cock, slow, her ass bouncing. You can feel Mark's eyes on the side of your face.",
         "He doesn't say turn it off. His knuckles go white on the couch. You're wet, and you press your thighs together and watch her ride."],
        "You left the sound up from earlier. The moaning carries over the kitchen fan.")

walkin("walkin_tv_ryan", "Channel 5", "home_living_room",
    "B3, Ryan: down from his room for his weekend TV row, he finds channel 5 on. His Lust +2 on the moment; her answer on Corruption: off 0, wait +1 cap 19, leave it on (Curious) +1 cap 39.",
    [here(R, "home_ryan_room")],
    ch5_in("A man flat on his back and a girl riding him, her tits bouncing, his hands full of her ass.",
           "You left the sound up. Her moans go all the way down the hall.")
    + [P("Ryan comes in from the hall for the TV and stops in the doorway.")],
    "He's seen the screen.",
    [P("He looks at the screen. She drops down on the man's cock, and she moans. Then he looks at you."),
     D(R, "Seriously, @player.nickname? It's the middle of the day."), ME("And?"),
     P("He goes red, but he doesn't go back to his room. His eyes go back to her tits on the screen, and he shoves his hands in his pockets."),
     VID("a young man on the bottom stair staring at porn on the living room TV, a girl on the couch", "brother catches sister watching porn", "guy walks in girl watching porn couch", pool_dir="sex/walkin_tv_ryan_t5")],
    CH5_ANS("r"), raise_=[lust(R)], records=["ryan_caught_ch5"], when=[wd(5, 6), tod("13:30", "14:00")], extra=[
        res("r_off", "Turn it off", [P("You jab the remote. The screen goes black. Ryan lets out a breath."), D(R, "My turn for the TV, then."), ME("Don't you dare tell anyone."), D(R, "Who would I tell? Mom?")],
            "Get up.", "home_hall", 2),
        res("r_gg", "Not yet", [P("You don't reach for the remote. Not yet. He comes and stands by the arm of the couch, and you both watch her ride him, her tits bouncing, your face hot."),
                                D(R, "Mom would actually die."), ME("So don't tell her."), D(R, "I'm not telling anybody anything."), P("You turn it off before he can sit down.")],
            "Get up.", "home_hall", 2),
        res("r_cur", "Leave it on", [P("You leave it on. Ryan sits down on the far end of the couch, very straight. On screen he takes her from behind, hard, and she moans every time his cock drives in."),
                                     P("Ryan's knee bounces. His hand sits on his thigh, an inch from the bulge in his shorts. You're wet, and you don't move either."),
                                     D(R, "We're not doing this. We're not. Turn it off."), ME("You turn it off. The remote's right there."), D(R, "Don't. Just. Fuck."),
                                     VID("a young man and a girl at opposite ends of a couch, both staring at porn on the TV", "brother and sister watching porn together couch", "watching porn together awkward couch", pool_dir="sex/walkin_tv_ryan_leave_t5")],
            "Turn it off.", "home_hall", 5)])

walkin("walkin_tv_laura", "Channel 5", "home_living_room",
    "B3, Laura (the cover branch): in from the kitchen on a Sunday night, she sees the screen. One line, no heat, no pay.",
    [here(L, "home_kitchen")],
    ch5_in("A man has a woman bent over the arm of a couch, his cock driving into her from behind.",
           "You left the sound up. Her moans carry all the way into the kitchen.")
    + [P("Laura comes through from the kitchen with a tea towel over her shoulder, and stops.")],
    "She's seen the screen.",
    [P("She looks at the screen for one second. Her face goes pink to the hairline."),
     # reader batch 4 (pass 3): the charge on her body, and the price (Laura saw)
     P("Then her eyes go to you on the couch, to your hot face and your nipples hard through what you're wearing, and stay there one second too long."),
     GC(cond(ntrait(L, "warmth", "lt", 40)), D(L, "Off. Now. And that is Mark's channel, not yours.")),
     GC(cond(*ANY), D(L, "Oh, sweetheart. Not in the living room. Turn it off.")),
     ME("Sorry, Mom. It was just on."), D(L, "Just on. Right."),
     P("She goes back into the kitchen without another word."),
     # reader batch 4 (pass 3): the hook, her Sunday kitchen row (18:00-22:00, hub_laura_kitchen)
     P("She'll be in the kitchen until ten.")],
    [go("Turn it off.", loc="home_hall", mins=2)], records=["laura_saw_ch5"], when=[wd(6), tod("21:30", "22:00")])

for chance, loud in ((0.25, TV_QUIET), (0.5, TV_LOUD)):
    rule("living_tv", "walkin_tv_mark_garage", chance, loud, here(M, "home_garage"), wd(0, 1, 3, 4), tod("21:30", "22:00"))
    rule("living_tv", "walkin_tv_mark_kitchen", chance, loud, here(M, "home_kitchen"), wd(2), tod("21:30", "22:00"))
    rule("living_tv", "walkin_tv_ryan", chance, loud, here(R, "home_ryan_room"), wd(5, 6), tod("13:30", "14:00"))
    rule("living_tv", "walkin_tv_laura", chance, loud, here(L, "home_kitchen"), wd(6), tod("21:30", "22:00"))

# ═════════════════════════════════════════════════════════════════════════════
# B4 · THE GARAGE (host garage_laundry): Mark back from dinner, bent at the drum. Her answers route into his
# built laundry tease ladder (mark.py, DECISIONS 128) with their built gates and pays; after mark_saw_her.
# ═════════════════════════════════════════════════════════════════════════════
PANTIES_ON = slot("underwear")
NO_TOWEL = {"type": "worn_type", "operator": "neq", "value": "towel"}
SAW = flag("mark_saw_her")
# Her answers, shared by the weekday and the Saturday walk-in: they route into the built tease ladder.
LAUNDRY_ANSWERS = [go("Load it and go.", loc="home_garage", mins=30, flags=[fset("did_laundry")], eff=[add("energy", -5)],
        costs=[{"trait": "energy", "value": 5}]),
     go("Leave your basket on top.", node="hub_mark_garage.hl_laundry_tease", cond_=cond(CURIOUS, SAW),
        eff=[npc_add(M, "want", 2)], flags=[fset("did_laundry")]),
     go("Bend for the bottom drum.", node="hub_mark_garage.hl_laundry_tease2", cond_=cond(CURIOUS, DARING, SAW, PANTIES_ON, NO_TOWEL),
        eff=[npc_add(M, "want", 3), pay("exhibitionism", 39)], flags=[fset("did_laundry")]),
     go("Wash what you're wearing.", node="hub_mark_garage.hl_laundry_tease3",
        cond_=cond(BOLD, SHOWING, SAW, slot("top"), slot("bra")),
        eff=[npc_add(M, "want", 4), pay("exhibitionism", 59), pay("corruption", 59)], flags=[fset("did_laundry")],
        wardrobe=[{"action": "unequip", "item_id": g} for g in ("tshirt", "thin_top")]),
     go("Leave it for later.", loc="home_hall")]
walkin("walkin_laundry_mark", "Bent at the drum", "home_garage",
    "B4, Mark: back from dinner to his garage row, he finds her bent at the washer. His Lust +2 on the moment; her answers route into his laundry tease ladder (hub_mark_garage) with its own gates and pays.",
    [here(M, "home_kitchen"), SAW],
    [P("You've got your basket on the garage floor and you're bent right over at the drum, feeding it, your ass up in the air."),
     G(cond(SKIRT), P("Your short skirt has ridden up the backs of your thighs.")),
     P("The door from the house opens behind you. Mark, back from dinner.")],
    "He stops in the doorway.",
    [P("He doesn't go to his bench. He leans on the door frame and looks at your ass, slow, and takes a drink of his beer."),
     # H7 (pass 3 A70): under Want 20 he catches himself and looks away; the open look waits for his higher Want
     GC(cond(ntrait(M, "want", "lt", 20)), P("Then he catches himself. He looks at the ceiling, at his bench, anywhere, and his beer hand drops in front of his jeans."),
        D(M, "Whites with whites, @player. Don't let me stop you."), ME("I know how to do laundry, Mark."), D(M, "Could've fooled me.")),
     GC(cond(*ANY), D(M, "Don't let me stop you."),
        P("The front of his jeans is tight. He doesn't hide it, but he doesn't come any closer."))],
    LAUNDRY_ANSWERS,
    raise_=[lust(M)], records=["mark_walked_in_laundry"], when=[wd(0, 1, 3, 4), tod("18:45", "19:00")])
rule("garage_laundry", "walkin_laundry_mark", 0.25, here(M, "home_kitchen"), wd(0, 1, 3, 4), tod("18:45", "19:00"))

# B4 Saturday (DECISIONS 152): Mark out to the garage after his coffee at the counter. The host needs him out of the
# garage (home.py garage_laundry), so, like the weekday one, the rule reads him in the kitchen in the 15 minutes
# before his garage row (09:00). His own canvas: the weekday's lines say dinner and beer.
walkin("walkin_laundry_mark_sat", "Bent at the drum", "home_garage",
    "B4 Saturday, Mark: in from his coffee for his Saturday in the garage, he finds her bent at the washer. His Lust +2 on the moment; her answers route into his laundry tease ladder (hub_mark_garage) with its own gates and pays.",
    [here(M, "home_kitchen"), SAW],
    [P("Saturday morning. You've got your basket on the garage floor and you're bent right over at the drum, feeding it, your ass up in the air."),
     G(cond(SKIRT), P("Bent like this, your short skirt is up over the backs of your thighs.")),
     P("The door from the house opens behind you. Mark, with his coffee, out for his day at the bench.")],
    "He stops in the doorway.",
    [P("He doesn't go to his bench. He stands in the doorway with the mug halfway to his mouth and looks at your ass, but he doesn't drink."),
     GC(cond(ntrait(M, "want", "lt", 20)), P("Then he catches himself and looks at his bench instead, hard, like it owes him money. He holds the mug low, in front of his jeans."),
        D(M, "Saturday's my garage, @player. Be quick about it."), ME("I'll be ten minutes."), D(M, "Five.")),
     GC(cond(*ANY), D(M, "Saturday's my garage, @player. Carry on."),
        P("He takes his time over the first sip. The front of his jeans is tight, and he stays where he is."))],
    copy.deepcopy(LAUNDRY_ANSWERS),
    raise_=[lust(M)], records=["mark_walked_in_laundry"], when=[wd(5), tod("08:45", "09:00")])
rule("garage_laundry", "walkin_laundry_mark_sat", 0.25, here(M, "home_kitchen"), wd(5), tod("08:45", "09:00"))

# ═════════════════════════════════════════════════════════════════════════════
# B5 · THE HALL MIRROR (host hall_mirror). One hall accident a day: it shares `home_event`, the brake of the
# hall's random events. Ryan's door behind her while he's awake in his room; Mark up the stairs to bed.
# ═════════════════════════════════════════════════════════════════════════════
def mirror_seen(who, frm):
    """The mirror by what she wears, from where he stands (`frm`), worded per walker."""
    return [
        GC(cond(TOWEL), P(f"You're in a towel. {frm}, in the glass, {who} eyes go to the knot over your tits, then down your bare thighs.")),
        GC(cond(*NAKED), P(f"You're naked. {frm}, in the glass, {who} eyes go straight to your tits, then down to your pussy, and stay.")),
        GC(cond(*UNDIES), P(f"Bra and panties. {frm}, {who} eyes go down your back to your ass in your panties.")),
        GC(cond(SKIRT, slot("underwear", False)), P(f"Nothing under your skirt, and it's short. {frm}, {who} eyes go to the backs of your thighs and up, to where the hem stops.")),
        GC(cond(SKIRT), P(f"Your skirt is short. {frm}, {who} eyes go up the backs of your bare thighs to your hem.")),
        GC(cond(slot("bra", False), slot("top"), *COVERED), P(f"No bra. {frm}, in the glass, {who} eyes find your nipples through your top.")),
        GC(cond(*COVERED), P(f"You're dressed. {frm}, {who} eyes go down your back to your ass anyway.")),
        GC(cond(*ANY), P(f"Half dressed. {frm}, {who} eyes go to what's missing first.")),
    ]


def mirror_answers(pre):
    return [go("Go to your room.", loc="home_ella_room", mins=2),
            go("Stay at the mirror.", node=f"{pre}_stay", mins=3, cond_=cond(*E_COV), eff=[pay("exhibitionism", 19)]),
            go("Stay at the mirror.", node=f"{pre}_stay", mins=3, cond_=cond(*E_DAR), eff=[pay("exhibitionism", 39)]),
            go("Stay at the mirror.", node=f"{pre}_stay", mins=3, cond_=cond(*E_SHO), eff=[pay("exhibitionism", 59)])]


walkin("walkin_mirror_ryan", "In the mirror", "home_hall",
    "B5, Ryan: his door opens behind her at the hall mirror. His Lust +2 on the moment; her answer on Exhibitionism: her room 0, stay +1 capped at her stage's top (19 / 39 / 59). Shares home_event.",
    [here(R, "home_ryan_room"), flag("home_event", False)],
    [P("You're at the hall mirror checking yourself over when Ryan's door opens behind you. In the glass you see him stop on his threshold.")],
    "He's looking.",
    mirror_seen("his", "From his doorway") + [
        G(cond(ntrait(R, "want", "lt", 40)), P("He catches you catching him in the glass. He goes red and looks at the carpet."), D(R, "Is the bathroom free?"), ME("Since when do you ask?"), D(R, "Since now. Is it?")),
        G(cond(ntrait(R, "want", "gte", 40)), P("He catches your eyes in the glass and doesn't look away."), D(R, "Looking good, @player.nickname."), ME("Going somewhere?"), D(R, "Not anymore."))],
    mirror_answers("r"), raise_=[lust(R)], records=["ryan_saw_mirror"], also_set=[fset("home_event")], extra=[
        res("r_stay", "Stay at the mirror", [P("You stay at the mirror. You fix your hair, slow, and turn a little side-on so he gets all of it. In the glass his hand goes to the front of his shorts and stays there."),
                                             ME("Like what you see?"), D(R, "Jesus. You can't ask me that."), P("His door clicks shut. Through it, his bed creaks.")],
            "Go on.", "home_hall", 2)])

walkin("walkin_mirror_mark", "In the mirror", "home_hall",
    "B5, Mark: down the hall to bed after his late TV, he stops behind her at the hall mirror; after mark_saw_her. His Lust +2 on the moment; her answer on Exhibitionism: her room 0, stay +1 cap 19 / 39 / 59. Shares home_event.",
    [here(M, "home_living_room"), SAW, flag("home_event", False)],
    [P("You're at the hall mirror checking yourself over when the living-room door creaks. Mark, on his way to bed. In the glass you see him stop behind you.")],
    "He's looking.",
    mirror_seen("his", "From behind you") + [
        P("His hands close into fists at his sides."),   # DO NOT DELETE: a non-group block, so his bands below are not elseifs of mirror_seen's
        GC(cond(ntrait(M, "want", "lt", 20)), P("Then he catches himself. He looks down at the hall carpet, at his own feet, anywhere but the glass."),
           D(M, "Bit late to be dressing up, @player. Bed."), ME("Night, Mark."), D(M, "Night.")),
        GC(cond(*ANY), P("He stands there and doesn't pretend he's doing anything else."),
           D(M, "Bit late to be dressing up, @player."))],
    mirror_answers("m"), raise_=[lust(M)], records=["mark_saw_mirror"], also_set=[fset("home_event")],
    # reader batch 4/5 (pass 3): not while Laura waits on the dark stairs after a late night (her hall row)
    when=[wd(0, 1, 2, 3, 4, 5), tod("01:30", "02:00"), here(L, "home_hall", False)], extra=[
        res("m_stay", "Stay at the mirror", [P("You stay at the mirror and take your time, and let him look at all of it. He comes up the last step. He stands right behind you, close enough that you feel the heat off him, but he doesn't touch."),
                                             D(M, "Bed, @player."), ME("I'm not tired."), D(M, "I didn't ask if you were tired."), P("He goes past you into his room and shuts the door hard.")],
            "Go on.", "home_hall", 2)])

for host_rule in ((here(R, "home_ryan_room"), wd(5, 6), tod("07:30", "14:00")),
                  (here(R, "home_ryan_room"), wd(6, 0, 1, 2, 3), tod("19:00", "00:00"))):
    rule("hall_mirror", "walkin_mirror_ryan", 0.25, flag("home_event", False), *host_rule)
rule("hall_mirror", "walkin_mirror_mark", 0.25, flag("home_event", False), here(M, "home_living_room"), here(L, "home_hall", False), wd(0, 1, 2, 3, 4, 5), tod("01:30", "02:00"))

# ═════════════════════════════════════════════════════════════════════════════
# B6 · LAURA'S WARDROBE (host master_wardrobe): Laura out of her Saturday shower, before she dresses at 17:00.
# Good mom: one line by her Love, no heat, no pay.
# ═════════════════════════════════════════════════════════════════════════════
walkin("walkin_wardrobe_laura", "Laura's mirror", "home_master_bedroom",
    "B6, Laura: out of her Saturday shower, she finds her daughter at her wardrobe with the red dress. A line by her Love; no heat, no pay.",
    [here(L, "home_bathroom")],
    [P("You've got the red one from the back of Laura's wardrobe out of its plastic and held up against you in her long mirror. It would barely cover your ass."),
     P("The door opens. Laura, in her robe, her hair wet from the shower. She stops.")],
    "She's seen the dress.",
    [GC(cond(ntrait(L, "warmth", "lt", 40)), D(L, "Put that back, please. That's mine."), ME("I was only looking, Mom."), D(L, "Look with your eyes, then."),
        P("She takes it out of your hands and hangs it up herself, careful, back in its plastic, and doesn't look at you while she does it.")),
     GC(cond(*ANY), P("She doesn't take it off you. She looks at you in her mirror, with her dress held up against you, and her face goes soft."),
        D(L, "I wore that once. I was about your age."), ME("Where did you wear it?"), D(L, "Somewhere I shouldn't have. Don't ask me where."),
        P("She smooths it down over your hip, then hangs it back up herself.")),
     # scene reader b02 (2026-11-03): the hook: her Saturday row has her dressing to go out from 17:00
     D(L, "Now out, please. I have to get dressed for tonight.")],
    [go("Hang it back up.", loc="home_hall", mins=5)], records=["laura_saw_wardrobe"], when=[wd(5), tod("16:45", "17:00")])
rule("master_wardrobe", "walkin_wardrobe_laura", 0.25, here(L, "home_bathroom"), wd(5), tod("16:45", "17:00"))

# B6 Mark (DECISIONS 152): home from the bar, up to bed (his Saturday bedroom row starts at 22:00). The host needs the
# room empty (home.py master_wardrobe, nobody in it) and the engine rolls at the clock she clicks on, so his arrival is
# the walk-in: the rule reads the 15 minutes before his row, while he is out (no row 18:30-22:00, read by the window
# alone, as walkins_out.py reads a walker with no row). A taboo accident, a look, no touch (DECISIONS 107).
# He says nothing: his rows have him nowhere until 22:00, and a speaker is judged where the scene starts (gate
# `a named person is where the line says`), so the stare carries it.
# Q12 (LO, 2026-11-04): Laura's black lace bra and panties are wardrobe items (0_systems_spec.toml, no price, so
# no shop sells them). The moment's button takes off what she wore and puts the pair on, so from the answer screen
# on the sidebar and the words agree. Every way out removes the pair (it goes back in Laura's drawer, not into
# hers) and gives back what she took off (canv.DRESS_BACK, LO 2026-11-04), the towel too: she "grabs her things".
# What she took off is worded on screen 1 by what she wears, before the button reads it away.
LACE = ("laura_lace_bra", "laura_lace_panties")
LACE_ON = ([{"action": "remember_outfit"}] + [{"action": "unequip", "item_id": g} for g in ALL_GARMENTS if g != "sneakers"]
           + [{"action": "equip", "item_id": g} for g in LACE])
LACE_OFF = [{"action": "remove", "item_id": g} for g in LACE] + DRESS_BACK
IN_LACE = {"type": "clothing_item", "item_id": "laura_lace_panties", "operator": "equipped"}
LINGERIE_OFF = [
    GC(cond(TOWEL), P("You drop your towel in a heap on her bed.")),
    GC(cond(*ANY), P("You strip off and leave your own things in a heap on her bed.")),
]
walkin("walkin_wardrobe_mark", "Laura's lingerie", "home_master_bedroom",
    "B6, Mark: home from the bar on a Saturday night, up to bed, he finds her at Laura's mirror in Laura's black lace bra and stares; after mark_saw_her. A look, no touch. His Lust +2 on the moment; her answer on Exhibitionism: cover up 0, let him look +1 cap 19 / 39 / 59.",
    [SAW_],
    [P("Laura's drawer under the dresses is open. The stockings are still in their packet. Under them is a black lace bra and the panties that match it, and neither one is a mom's."),
     *LINGERIE_OFF,
     P("You hook her bra on and pull her panties up. In her long mirror your tits sit high in the lace, and your nipples show dark right through it. You turn side-on to see how the lace looks on your ass."),
     P("The front door goes. Then heavy feet in the hall, slow, a man's. The bedroom door opens before you can move. Mark, home from the bar."),
     # pass 3 B4: the speech on this screen is hers; Mark's one line is on the next (pass 4 B51)
     ME("Mark. I was just. I was only trying it on.")],
    "He stops in the doorway.",
    [P("He smells of beer. He stands in his own bedroom doorway with his keys still in his fist and looks at you in his wife's bra."),
     # H7 (pass 3 A70): under Want 20 he looks once and puts his eyes on the wall; one chain of three bands
     GC(cond(ntrait(M, "want", "lt", 20)), P("His eyes go to your tits in the black lace, to your nipples through it. Then he catches himself and looks at the wall above your head, hard, and keeps them there. He doesn't take one step into the room."),
        P("His jaw works like he's going to tell you to take it off.")),
     GC(cond(ntrait(M, "want", "lt", 50)), P("His eyes go to your tits in the black lace, to your nipples through it, and stay there. Then down your stomach, slow, and back up. The front of his jeans fills, but he doesn't take one step into the room."),
        P("His eyes go to Laura's open drawer and back to your tits, and his jaw works like he's going to tell you to take it off.")),
     GC(cond(*ANY), P("His eyes go to your tits in the black lace, to your nipples through it, and stay there. Then down your stomach, slow, and back up. The front of his jeans fills, but he doesn't take one step into the room."),
        P("He leans on the door frame to look longer, and he wets his lips.")),
     # pass 4 B51 (LO, 2026-11-04: Mark may speak here): his one line, true in every band; the chain ends on it
     D(M, "That's your mother's."),
     VID("a middle-aged man in a bedroom doorway staring at a girl in a black lace bra at a long mirror", "stepdad catches girl in mom's lingerie", "man walks in on girl trying on lingerie bedroom", pool_dir="sex/walkin_wardrobe_mark_t4")],
    [go("Cover up.", node="m_cover", mins=2),
     go("Let him look.", node="m_look", mins=3, cond_=cond(*E_COV), eff=[pay("exhibitionism", 19)]),
     go("Let him look.", node="m_look", mins=3, cond_=cond(*E_DAR), eff=[pay("exhibitionism", 39)]),
     go("Let him look.", node="m_look", mins=3, cond_=cond(*E_SHO), eff=[pay("exhibitionism", 59)])],
    raise_=[lust(M)], records=["mark_saw_lingerie"], when=[wd(5), tod("21:45", "22:00")], moment_wardrobe=LACE_ON, extra=[
        res("m_cover", "Cover up", [P("You cross your arms over your tits, over her lace. Your face is on fire."), ME("Don't tell her. Please don't tell Mom."),
                                    P("He jerks his chin at Laura's drawer: put it back. Then he stands aside in the doorway while you grab your things, and he watches you the whole time you do.")],
            "Get changed. Go.", "home_hall", 5, wardrobe=LACE_OFF),
        # scene reader b03 (2026-11-03): her voice at her level: under Daring she can't make her arms move; from Daring she asks
        res("m_look", "Let him look", [GC(cond(trait("exhibitionism", "lt", 20)), P("You don't cover up. You can't make your arms move. You stand there facing him in his wife's bra with your face on fire and your nipples hard through her lace."),
                                          ME("Mark. Say something. Please."), T("*Cover up. Cover up. You don't.*")),
                                       GC(cond(trait("exhibitionism", "gte", 20)), P("You don't cover up. You turn round to face him, drop your hands to your sides, and let him look at you in his wife's bra."), ME("Does it look better on her, Mark? Or on me?")),
                                       P("He looks. A long time. At your tits in the lace, your nipples hard through it. His keys bite into his fist, but he still doesn't come in."),
                                       P("He breathes out hard through his nose. Then he steps back into the hall and pulls the door to without a word, and leaves you to get changed."),
                                       G(cond(IN_LACE), P("Alone, you look at yourself in her mirror a second longer: her bra, her panties, your body in them. Then you take them off and fold them back into her drawer the way you found them.")),
                                       T("He'll think about this bra every time she wears it.")],
            "Get changed. Go.", "home_hall", 5, wardrobe=LACE_OFF)])
rule("master_wardrobe", "walkin_wardrobe_mark", 0.25, wd(5), tod("21:45", "22:00"))

# ═════════════════════════════════════════════════════════════════════════════
# B7 · RYAN'S THINGS (host ryan_things, Ryan out): Ryan up from dinner; Kayla early on a Friday.
# ═════════════════════════════════════════════════════════════════════════════
walkin("walkin_things_ryan", "Caught", "home_ryan_room",
    "B7, Ryan: up from dinner, he catches her with the box from his drawer. His Lust +2 on the moment; her answer on Corruption: put it back 0, \"Explain this.\" (Curious, Corruption 20 up; LO 2026-11-04, Q15) +1 cap 39.",
    [here(R, "home_kitchen")],
    [P("You've got Ryan's bedside drawer open and the box of condoms in your hand, opened, half gone, when the door opens behind you."),
     P("Ryan, up from dinner.")],
    "He's caught you.",
    [GC(cond(ntrait(R, "want", "lt", 40)), D(R, "What the hell, @player.nickname? Get out of my stuff."),
        P("His eyes go to the box in your hand, then to your tits, then back to your face, fast, and he goes red."), ME("I was looking for a charger."), D(R, "In my condoms?")),
     GC(cond(*ANY), P("He shuts the door behind him and leans on it. His eyes go down you, slow, your tits, your legs, the box in your hand."),
        D(R, "Find what you were looking for?"), ME("Maybe. Half the box is gone, Ryan."), D(R, "Counting, are you?"))],
    [go("Put it back.", loc="home_hall", mins=5),
     go("Hold it up. \"Explain this.\"", node="explain", mins=3, eff=[pay("corruption", 39)], cond_=cond(CURIOUS))],
    raise_=[lust(R)], records=["ryan_caught_snooping", "ryan_things_found"], when=[wd(6, 0, 1, 3), tod("18:45", "19:00")], extra=[
        res("explain", "Explain this", [ME("Explain this."),
                                        P("You hold the box up between you. Half gone. Ryan looks at it, then at you, and his ears go red."),
                                        G(cond(flag("knows_about_kayla")), D(R, "That's mine and Kayla's business.")),
                                        G(cond(flag("knows_about_kayla", False)), D(R, "That's none of your business.")),
                                        # LO, 2026-11-04 (Q15): the flirt opens at Curious, so the button waits for Corruption 20
                                        # and the Good Girl tease that stood in for it below 20 is gone
                                        GC(cond(*ANY), P("He takes it out of your hand. His fingers close over yours on the box, but he doesn't let go as fast as he should. His eyes drop to your mouth."),
                                           D(R, "Out. Before I start asking what you're doing in my drawer."), ME("Ask, then."))],
            "Leave him to it.", "home_hall", 2)])
walkin("walkin_things_kayla", "Caught", "home_ryan_room",
    "B7, Kayla: early on a Friday, she lets herself in and catches her in Ryan's drawer. A hook line; nothing about Ryan's secret; no pay.",
    [flag("kayla_met"), here(R, "home_ryan_room", False)],
    [P("You've got Ryan's bedside drawer open and the box of condoms in your hand when the bedroom door opens."),
     P("Kayla, an overnight bag on her shoulder.")],
    "She's seen you.",
    [D(K, "Snooping?"),
     P("Kayla drops the bag on Ryan's bed and looks at the box in your hand, then at you, up and down, slow, your tits, your legs."),
     D(K, "Relax. I won't tell him. He's the one who should be worried, with you across the hall."), ME("What's that supposed to mean?"), D(K, "You know exactly what it means. Put them back, @player.nickname.")],
    [go("Put it back.", loc="home_hall", mins=5)], records=["kayla_caught_her", "ryan_things_found"], when=[wd(4), tod("17:45", "18:00")])
rule("ryan_things", "walkin_things_ryan", 0.25, here(R, "home_kitchen"), wd(6, 0, 1, 3), tod("18:45", "19:00"))
rule("ryan_things", "walkin_things_kayla", 0.25, flag("kayla_met"), wd(4), tod("17:45", "18:00"))

# ═════════════════════════════════════════════════════════════════════════════
# B8 · THE FRONT STEP (host front_step): Vance down off his porch to his gate, while it's light, her legs bare.
# ═════════════════════════════════════════════════════════════════════════════
walkin("walkin_step_vance", "At the gate", "home_front_door",
    "B8, Vance: down off his porch to his gate, he looks at her legs on the step. His Lust +2 on the moment; her answer on Exhibitionism: knees together 0, leave them +1 cap 19, stretch out (Daring) +1 cap 39.",
    [here(V, "vance_house"), flag("vance_met"), *BARE_LEGS],
    [P("You're on the front step with your knees up, your bare legs out down the steps, when Vance comes down off his porch to his gate.")],
    "He stops at the gate.",
    [P("He stands there with his paper folded under his arm and looks at your legs, from your ankles all the way up, and he takes his time."),
     G(cond(SKIRT), P("In this skirt, from where he stands, he can see right up your thighs.")),
     GC(cond(ntrait(V, "want", "lt", 30)), P("He doesn't say good evening at first. He just looks."), D(V, "Evening."), ME("Evening, Mr. Vance.")),
     GC(cond(*ANY), D(V, "Nice evening for it, Miss."), ME("It is."), D(V, "You should sit out here more often."))],
    [go("Knees together. Go in.", loc="home_hall", mins=5),
     go("Leave them.", node="v_leave", mins=5, cond_=cond(*E_COV), eff=[pay("exhibitionism", 19)]),
     go("Stretch your legs out.", node="v_stretch", mins=5, cond_=cond(DARING), eff=[pay("exhibitionism", 39)])],
    raise_=[lust(V)], records=["vance_saw_step"], when=[tod("18:00", "21:00")], extra=[
        res("v_leave", "Leave them", [P("You leave them. You don't pull your knees together, and you don't look at him. Your face goes hot."), D(V, "Tell Mark I said hello."), ME("Tell him yourself."),
                                      P("He looks until a car goes by, and then he goes back up to his porch, slow.")],
            "Go back in.", "home_hall", 10),
        res("v_stretch", "Stretch your legs out", [P("You stretch your legs out long down the step, one ankle over the other, bare all the way up, and lean back on your hands."),
                                                   P("Vance's paper drops to his side. He doesn't pretend any more."),
                                                   D(V, "Mark's a lucky man, having you in that house."), ME("Does he know that?"), D(V, "He will."), P("He goes back up to his porch and sits where he can see you.")],
            "Go back in.", "home_hall", 10)])
rule("front_step", "walkin_step_vance", 0.25, here(V, "vance_house"), tod("18:00", "21:00"))

# ═════════════════════════════════════════════════════════════════════════════
# Q4 (LO, 2026-11-04: "Add walkins in this release itself"): the refill places that rolled no event (gate `a refill
# place rolls an event`). The same shape as B1-B8: one moment screen, one graded answer screen (the-surfaces.md R3).
# B21 · HER NAP (host room_nap): Ryan across the hall on a weekend, after Kayla's Friday night is over (her row in
# his room ends 10:00 on Saturday) and before his TV row (14:00). He comes in for her charger. A housemate covers
# at his low Want (the-heat-ladder.md H7). His Lust +2 on the moment; her answer on Exhibitionism.
# ═════════════════════════════════════════════════════════════════════════════
SLEEP_SHIRT = wt("sleep_shirt")
NAP_SEEN = [
    GC(cond(TOWEL), P("You fell asleep in your towel. In your sleep it has come undone down one side, and it's open from your hip to the side of your tits.")),
    GC(cond(*NAKED), P("You fell asleep naked on top of the covers, on your front, your bare ass to the door.")),
    GC(cond(*UNDIES), P("Bra and panties, on top of the covers. You've rolled onto your front in your sleep, and your panties have ridden up into the crack of your ass.")),
    GC(cond(SLEEP_SHIRT), P("Your sleep shirt has rucked up round your hips in your sleep, and the backs of your thighs are bare to the door.")),
    GC(cond(SKIRT), P("Your short skirt has ridden up in your sleep, all the way up the backs of your thighs.")),
    GC(cond(*COVERED), P("You fell asleep dressed, on your front, one knee pulled up under you.")),
    GC(cond(*ANY), P("You fell asleep half dressed on top of the covers, and the half that's bare is the half facing the door.")),
]
walkin("walkin_nap_ryan", "The door clicks", "home_ella_room",
    "B21 (Q4), Ryan: from his room on a weekend late morning, he comes in for her charger and finds her asleep on the covers. His Lust +2 on the moment; her answer on Exhibitionism: the blanket 0, then +1 cap 19 / 39 / 59.",
    [here(R, "home_ryan_room")],
    # reader pass 4 b4: it replaces room_nap's "Sleep (2h)." (120 minutes, energy +30), so the nap is spent on the
    # moment's button, and the door clicks after it; it starts by 12:00 so it ends inside his room row (to 14:00)
    [P("You lie down on top of the covers for a nap, and you're asleep before your head is properly on the pillow.")],
    "Sleep.",
    [P("Your door clicks. You open your eyes."),
     *NAP_SEEN,
     P("Ryan is in your room with your phone charger in his hand, but he isn't looking at the charger. He's looking at you."),
     P("His eyes go all the way down you and all the way back up, slow. Then they get to your face, and he sees your eyes are open."),
     GC(cond(ntrait(R, "want", "lt", 40)), P("He goes red to the ears and turns to the wall, fast. He holds the charger in front of his shorts like it hides anything. It doesn't. He's hard."),
        D(R, "Charger. Mine's dead. You were asleep, I wasn't going to wake you. I'm going."), ME("You could knock.")),
     GC(cond(*ANY), P("He doesn't go red, but he doesn't leave either. He leans back on your desk and keeps looking, and he doesn't turn the front of his shorts away from you."),
        D(R, "Didn't want to wake you. Good nap?"), ME("So you stood there and watched me instead.")),
     VID("a young man in a bedroom holding a phone charger, staring at a girl waking up on top of the covers", "brother walks in on sister napping", "guy walks in on girl sleeping in bed", pool_dir="sex/walkin_nap_ryan_t4")],
    [go("Pull the blanket over you.", node="r_cover", mins=2),
     go("Don't move.", node="r_cov", mins=3, cond_=cond(*E_COV), eff=[pay("exhibitionism", 19)]),
     go("Stretch.", node="r_dar", mins=3, cond_=cond(*E_DAR), eff=[pay("exhibitionism", 39)]),
     go("Roll onto your back.", node="r_sho", mins=5, cond_=cond(*E_SHO), eff=[pay("exhibitionism", 59)])],
    raise_=[lust(R), {"targetType": "player", "trait": "energy", "op": "add", "value": 30, "cap": 100}], moment_mins=120,
    records=["ryan_saw_nap"], when=[wd(5, 6), tod("10:00", "12:00")], extra=[
        res("r_cover", "The blanket", [P("You drag the blanket up to your chin and glare at him over the top of it."), ME("Out. Now. And knock next time."),
                                       D(R, "Going. Sorry. I'm going."), P("He backs out with your charger. His door shuts across the hall, and a second later his music comes on loud.")],
            "Get up.", "home_ella_room", 5),
        res("r_cov", "Don't move", [P("You don't move. You lie there with your cheek on the pillow and let him look, one second, two, three. Your face is hot, but you stay put, your nipples hard against the covers."),
                                    D(R, "You're. You're awake."), ME("I am. And you're still looking."), D(R, "Yeah. I. Yeah. Sorry."),
                                    P("He goes, and he leaves your door open behind him.")],
            "Get up.", "home_ella_room", 5),
        res("r_dar", "Stretch", [P("You stretch, slow, your arms over your head and your back arching off the covers, and you take your time about it. Your ass lifts off the bed. His breath goes out of him."),
                                 D(R, "Jesus, @player.nickname. Anybody could come down that hall."), ME("So? I'm only stretching."),
                                 D(R, "Lock your door next time. Or don't. I don't know any more."), P("He goes with the charger held low in front of his shorts.")],
            "Get up.", "home_ella_room", 5),
        res("r_sho", "Roll onto your back", [P("You roll onto your back, slow, and stretch your arms up over your head, and give him the whole front of you."),
                                             GC(cond(*NAKED), P("Your tits are bare, and you leave them bare. His eyes go to them and stay.")),
                                             GC(cond(TOWEL), P("The towel stays where it fell, open down your side, and his eyes go to the bare curve of your tit and stay.")),
                                             GC(cond(*ANY), P("His eyes go down the front of you, slow, to every place your clothes don't cover.")),
                                             D(R, "You want me to look."), ME("You walked in, Ryan. Not me."),
                                             D(R, "Not now. Not with the house this full. But Jesus, @player.nickname."),
                                             P("He goes, and his door shuts hard across the hall.")],
            "Get up.", "home_ella_room", 5)])
rule("room_nap", "walkin_nap_ryan", 0.25, here(R, "home_ryan_room"), wd(5, 6), tod("10:00", "12:00"))

# ═════════════════════════════════════════════════════════════════════════════
# B22 · THE LOUNGER (host garden_sun): Mark out of the kitchen on a Sunday (his Sunday table row, 08:00-22:00) for
# the tomatoes by the fence, while Laura is out (her Sunday kitchen row starts 18:00). After mark_saw_her (the
# dryer stays first, H2). A housemate: he covers at his low Want (H7). Mark's early words are legs and ass
# (spine/SP2_ladders.md). His Lust +2 on the moment; her answer on Exhibitionism.
# ═════════════════════════════════════════════════════════════════════════════
LOUNGER_TOPLESS = [slot("top", False), slot("dress", False), slot("bra", False)]
LOUNGER_BRA = [slot("top", False), slot("dress", False), slot("bra")]
walkin("walkin_garden_mark", "The back step", "home_garden",
    "B22 (Q4), Mark: out of the kitchen on a Sunday with a beer and the hose, he stops on the back step and looks at her on the lounger; after mark_saw_her. His Lust +2 on the moment; her answer on Exhibitionism: cover up 0, then +1 cap 19 / 39 / 59.",
    [here(M, "home_kitchen"), SAW_],
    [P("Sunday. You drag the lounger into the sun on the grass and lie back with your eyes shut. Behind you the house is quiet except for the kitchen radio."),
     GC(cond(*LOUNGER_TOPLESS), P("Topless, on your front, bare to the waist, the sun hot all down your back.")),
     GC(cond(*LOUNGER_BRA), P("Just your bra on top, on your back, the sun on your bare stomach.")),
     GC(cond(*ANY), P("On your back in what you have on, your face turned up to the sun.")),
     P("The back door bangs. Mark comes out of the kitchen with a beer in one hand and the hose in the other, for the tomatoes by the fence, and stops on the step.")],
    "He's stopped on the step.",
    [P("He doesn't turn the hose on. He stands on the step with his beer and looks at you, from your feet all the way up, slow."),
     GC(cond(ntrait(M, "want", "lt", 20)), P("Then he catches himself. He turns his back on you and gives the tomatoes a soaking they don't need, and he keeps the beer low in front of his jeans the whole time."),
        D(M, "You'll burn, lying out like that. Your mother'll blame me."), ME("Then don't look, Mark."), D(M, "I'm watering.")),
     GC(cond(ntrait(M, "want", "lt", 50)), P("He doesn't turn away. He waters the same pot until it runs over the rim and onto his boots, and his eyes stay on your legs the whole time, slow up your thighs and back down."),
        D(M, "Nice day for it, @player."), ME("The tomatoes are drowning, Mark.")),
     GC(cond(*ANY), P("He doesn't pretend. He drops the hose on the grass, still running, and drinks his beer and looks, and the front of his jeans fills."),
        D(M, "Sunday's my day off, @player. This is a good way to spend it.")),
     VID("a middle-aged man on a back step with a beer and a garden hose, staring at a girl sunbathing on a lounger", "stepdad watches girl sunbathing garden", "man stares at girl sunbathing backyard", pool_dir="sex/walkin_garden_mark_t4")],
    [go("Sit up and cover up.", node="m_cover", mins=2),
     go("Stay as you are.", node="m_stay", mins=5, cond_=cond(*E_COV), eff=[pay("exhibitionism", 19)]),
     go("Stretch your legs out.", node="m_stretch", mins=5, cond_=cond(*E_DAR), eff=[pay("exhibitionism", 39)]),
     go("Turn over for him.", node="m_turn", mins=5, cond_=cond(*E_SHO), eff=[pay("exhibitionism", 59)])],
    raise_=[lust(M)], records=["mark_saw_garden"], when=[wd(6), tod("10:00", "18:00")], extra=[
        res("m_cover", "Cover up", [P("You sit up fast and hug your knees to your chest, and your face goes hot."),
                                    ME("Mark! You could say something before you come out."), D(M, "It's my garden. I don't have to say anything."),
                                    P("He waters the tomatoes with his back to you while you grab your things and go in.")],
            "Go in.", "home_hall", 5),
        res("m_stay", "Stay as you are", [P("You stay exactly as you are, eyes shut, and let him look. You can feel where his eyes are by the heat of them: your legs, the tops of your thighs. Your face goes red, but you still don't move."),
                                          D(M, "Tomatoes need doing every Sunday, @player."), ME("Then I'll be out here every Sunday."),
                                          P("He waters them slow, but he doesn't look at the tomatoes once.")],
            "Get up off the lounger.", "home_garden", 20),
        res("m_stretch", "Stretch your legs out", [P("You stretch out long on the lounger, one knee up, your arms over your head, and you hold it there for him."),
                                                   GC(cond(ntrait(M, "want", "lt", 20)), P("He looks once, long. Then he looks at the fence instead, hard, like he's counting the slats.")),
                                                   GC(cond(*ANY), P("He looks all he wants. He takes a long drink, and his eyes go from your knee all the way down your thigh.")),
                                                   D(M, "Not out here, @player. The neighbours can see over that fence."), ME("Then come and stand in front of me."), D(M, "Not yet.")],
            "Get up off the lounger.", "home_garden", 20),
        # reader pass 4 b5: only the topless visit is on her front, so only it rolls over; the others are on their backs
        res("m_turn", "Turn over for him", [GC(cond(*LOUNGER_TOPLESS), P("You roll over slow on the lounger and let him have the front of you."),
                                               P("You're topless, and you don't cover up. You lie back with your arms behind your head, bare to the sky and to him.")),
                                            GC(cond(*ANY), P("You're already on your back. You stretch your arms up behind your head, arch off the lounger, and let him look at all of it.")),
                                            P("On the step, Mark goes still."),   # DO NOT DELETE: a non-group block, so his bands below are not elseifs of the clothes chain
                                            GC(cond(ntrait(M, "want", "lt", 20)), P("His jaw goes tight. He turns his back on you and turns the hose up hard on the tomatoes, and his free hand goes to the front of his jeans to hide it."),
                                               D(M, "Get some clothes on, @player. Anybody could look out a window."), ME("Somebody is looking, Mark. You.")),
                                            GC(cond(*ANY), P("He doesn't turn away. He drinks and looks, a long time, and the front of his jeans is tight."),
                                               D(M, "Cover up, @player. Not out here."), ME("Then where?"), D(M, "Not today. That's all you get."))],
            "Get up off the lounger.", "home_garden", 20)])
rule("garden_sun", "walkin_garden_mark", 0.25, here(M, "home_kitchen"), wd(6), tod("10:00", "18:00"))

# pass 4 A57: her own line by her stage on the walk-ins where a short band line does it (canv.her_band_line)
her_band_line(CANVASES, {
    "walkin_shower_ryan": ("exhibitionism", [
        "Ryan. In here. Grab the towel.",
        "Ryan's looking. You don't want the towel yet.",
        "Let your step-brother look. See how long he stays.",
        "Ryan can look all he wants. You want him to."]),
    "walkin_shower_kayla": ("exhibitionism", [
        "Kayla, a foot away. You want the towel.",
        "Kayla's watching. You mind less than you should.",
        "Let Ryan's girlfriend see what's across the hall.",
        "Let her look, and tell Ryan all of it."]),
    "walkin_shower_mark": ("exhibitionism", [
        "Mom's husband, and you're naked. Cover up.",
        "Mark's looking. You don't want to cover up yet.",
        "Let Mark look. Watch what it does to him.",
        "You want Mark thinking about this at dinner."]),
    "walkin_tv_ryan": ("corruption", [
        "Ryan saw it. You want the floor to swallow you.",
        "Ryan saw it. You want to know what he thinks.",
        "You don't want to turn it off. Not with him here.",
        "You want to watch the rest with Ryan."]),
})

def attach(out):
    """Put each host's rules on its canvas in `out` (host ids not in `out` are skipped and returned)."""
    left = set(RULES)
    for c in out:
        if c.get("id") in RULES:
            c["trigger"]["substitutions"] = list(c["trigger"].get("substitutions") or []) + RULES[c["id"]]
            left.discard(c["id"])
    return left
