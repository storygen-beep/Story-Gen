"""Gossip that matters (DECISIONS 207; LO, 2026-11-08, "Go ahead" on the plan).

Course of Temptation's model (round10/cards/gossip.md): a person who saw her says it out loud in a busy place
while she is there, so the people round him know it too; her friends shut him down; at set levels strangers act
on what they heard. Ours keeps one audience (the campus) and one meter (`campus_talk`), and remembers WHAT was seen
in four flags that canv.talk_remembers sets on every answer that already paid the talk: talk_class, talk_gym,
talk_quad, talk_party. Every line here names the thing, behind the flag that makes it true.

Levels (the plan's table): 10 the spread scenes; 25 the ask on the quad (and Nadia, hale.py; the feed, phone.py);
40 the rival's report (college.py) and Nadia's lunch refusal (hale.py); 60 the ask at the party and the passer-by.
One campus event a day (`gossip_today`) and one at the party a night (`gossip_party_today`), both cleared at
midnight (0_systems_spec.toml daily tick).
"""
from canv import *
from tomlw import tod
from home_items import here

out = []
Z, N = "npc_zoe", "npc_nadia"
TODAY, PARTY_TODAY = "gossip_today", "gossip_party_today"
AT_PARTY = {"type": "hours_since_flag", "subject": "player", "flag_key": "party_went", "operator": "lt", "value": 8}
PARTY_SCHED = [{"weekdays": [4], "start_time": "19:00", "end_time": "00:00"}, {"weekdays": [5], "start_time": "00:00", "end_time": "02:00"}]
TALK = lambda n: trait("campus_talk", "gte", n)
TALK_LT = lambda n: trait("campus_talk", "lt", n)
TALK1 = add("campus_talk", 1, clamp=False)
BANDS = [(None, 20, 19), (20, 40, 39), (40, 60, 59), (60, None, 79)]   # (from, below, the stage's top): a pay stops at its stage


def exh_band(lo, hi):
    return ([trait("exhibitionism", "gte", lo)] if lo is not None else []) + ([trait("exhibitionism", "lt", hi)] if hi is not None else [])


# ── what campus remembers: one condition per thing, in order, first match wins (GC groups chain into one
# if/elseif). Each is true for every answer that sets its flag (canv.TALK_KIND). Each screen says it in its own
# words (gates: one pool, one place), and past acts never name a garment she may not have on now.
WHAT = [("lap",   cond(flag("talk_quad"), flag("team_saw_quad"))),
        ("kiss",  cond(flag("talk_quad"))),
        ("class", cond(flag("talk_class"))),
        ("gym",   cond(flag("talk_gym"))),
        ("dares", cond(flag("talk_party"), trait("zoe_dares_done", "gte", 1))),
        ("bra",   cond(flag("talk_party"), flag("zoe_has_bra"))),
        ("teammate", cond(flag("talk_party")))]
KIND_OF = {"lap": "talk_quad", "kiss": "talk_quad", "class": "talk_class", "gym": "talk_gym",
           "dares": "talk_party", "bra": "talk_party", "teammate": "talk_party"}
SPREAD = {   # the teller, to his table
    "class": "I sit two rows behind her in class. I've seen what's under her clothes.",
    "gym": "She trains at the campus gym. Ask the guys in there what they've seen of her.",
    "dares": "She takes Zoe's dares. In the middle of the party, in front of everyone.",
    "bra": "She pulled her bra off through her sleeve on Zoe's balcony. Gave Zoe the bra. Didn't put it back on.",
    "teammate": "She was all over Jake's teammate at Zoe's party."}
ASK_QUAD = {   # the guys on the steps, to her
    "lap": "You're Jake's girl. The one in his lap on the grass, with the whole team watching.",
    "kiss": "You're Jake's girl. We saw you two on the grass.",
    "class": "You sit in front of my buddy in class. He says he's seen everything.",
    "gym": "You're the girl from the gym. The guys at the rack won't shut up about you.",
    "dares": "You're the one who does Zoe's dares.",
    "bra": "You're the one from Zoe's balcony. The guy at the window told everybody.",
    "teammate": "You're the one who was all over Jake's teammate at Zoe's."}
ASK_PARTY = {   # the guy at the party, to her
    "lap": "I heard Jake had you in his lap on the quad with the whole team watching.",
    "kiss": "I heard about you and Jake, on the grass, in front of everybody.",
    "class": "I heard whoever sits behind you in class gets quite a view.",
    "gym": "I heard you're the reason the guys at the gym can't finish a set.",
    "dares": "I heard you do anything Zoe dares you.",
    "bra": "I heard what happened on Zoe's balcony. The guy at the window saw everything.",
    "teammate": "I heard about you and Jake's teammate."}
PASSBY = {   # a stranger passing, to her face
    "lap": "You're the one in Jake's lap on the grass, with the whole team watching.",
    "kiss": "You're the one all over Jake on the grass, in front of the whole team.",
    "class": "You're the one from the lecture hall. The guys in your row say they've seen what's under your clothes.",
    "gym": "You're the one from the gym. The guys in there can't stop talking about you.",
    "dares": "You're the one who takes Zoe's dares.",
    "bra": "You're the one from Zoe's balcony. With nothing on under your clothes, they say.",
    "teammate": "You're the one who was all over Jake's teammate at Zoe's."}
ANY_TALK_FLAG = ["talk_class", "talk_gym", "talk_quad", "talk_party"]


def said_chain(texts, speak, kinds=None):
    """First true line among `texts` (keys of WHAT), spoken by `speak`. One if/elseif chain."""
    return [GC(c, speak(texts[k])) for k, c in WHAT if k in texts and (kinds is None or KIND_OF[k] in kinds)]


def none_of(kinds):
    return [flag(k, False) for k in kinds]


# ═════════════════════════════════════════════════════════════════════════════
# 1. THE SPREAD SCENES (level 10): someone who saw says it out loud while she is there. 1 in 3 on arrival.
#    "Let him talk." spreads it (campus_talk +1) and pays her to the top of her stage: she lets the room look at
#    her while it hears (rule 1 of exhibition phase 1: below 20 she lets a look that is already happening go on).
#    "Shut him up." spreads nothing. A friend in the room (Nadia, Zoe) shuts him down first: no spread, no pay
#    (CoT: her friends refuse to pass it on and tell the teller off, traces/cot_reads.md, juiciest_rumor).
# ═════════════════════════════════════════════════════════════════════════════
def spread(cid, name, loc, kind, today, teller_intro, crowd_reacts, let_after, shut_after, friend=None, friend_lines=(),
           sched=None, extra=(), him="him", friend_until=None):
    # With no friend in the room (or one who no longer stands up for her: friend_until, a campus_talk level) the
    # teller has the floor; each set of answers below is exclusive of the friend's one.
    if friend:
        defends = [here(friend, loc)] + ([TALK_LT(friend_until)] if friend_until else [])
        floor_sets = [[here(friend, loc, False)]] + ([[here(friend, loc), TALK(friend_until)]] if friend_until else [])
    else:
        defends, floor_sets = None, [[]]
    exits = []
    for fs in floor_sets:
        exits += [go(f"Let {him} talk.", node="let", mins=5, eff=[TALK1, add("exhibitionism", 1, cap=cap)], flags=[fset(today)],
                     cond_=cond(*exh_band(lo, hi), *fs)) for lo, hi, cap in BANDS]
        exits.append(go(f"Walk over and shut {him} up.", node="shut", mins=5, flags=[fset(today)], cond_=cond(*fs) if fs else None))
    blocks = [P(teller_intro), *said_chain(SPREAD, WHO, kinds=[kind]), P(crowd_reacts)]
    nodes = [node("event", name, blocks, exits),
             node("let", f"Let {him} talk", let_after, [go("Leave them to it.", loc=loc, mins=0)]),
             node("shut", f"Shut {him} up", shut_after, [go("Leave them to it.", loc=loc, mins=0)])]
    if friend:
        blocks.append(G(cond(*defends), *friend_lines))
        exits.append(go("Let her.", loc=loc, mins=5, flags=[fset(today)], cond_=cond(*defends)))
    t = {"location": loc, "is_repeatable": True, "priority": 5, "is_active": True, "trigger_mode": "random", "chance": 0.35,
         "conditions": cond(flag("opening_done"), flag(today, False), TALK(10), flag(kind), *extra)}
    if sched:
        t["schedules"] = sched
    return {"id": cid, "name": name,
            "description": f"Gossip (DECISIONS 207): {name}. Someone who saw says it out loud while she is there ({kind}); "
                           "1 in 3 on arrival, one a day. Letting him talk spreads it (campus_talk +1) and pays her to her stage's top; "
                           "shutting him up spreads nothing" + ("; a friend in the room shuts him down first." if friend else "."),
            "trigger": t, "nodes": nodes}


out.append(spread("gossip_spread_canteen", "Your name at the next table", "canteen", "talk_gym", TODAY,
    "A guy from the gym has the next table laughing. He doesn't lower his voice when you sit down. He raises it.",
    "The whole table turns round to look at you. A girl at the end looks you up and down, slowly, like she's checking.",
    [P("You could say something, but you don't. You eat, and let them look. He goes on, and the table leans in, and every face at it keeps coming back to you: your chest, your legs, your face, your chest again."),
     WHO("Is that true?"),
     P("He just grins at you over his tray. The next table along has stopped talking to listen."),
     T("Now they all know. And all of them are looking.")],
    [P("You put your tray down on his table, hard, right by his hand. He stops mid-word."),
     ME("Finish that sentence. I dare you."),
     P("He holds his hands up, grinning. The table laughs, at him this time. He doesn't say it again, not while you're here."),
     T("He's quiet now, but they heard the start of it. They're still looking.")],
    friend=N, friend_lines=[
        P("Nadia puts her fork down."),
        D(N, "Hey. Gym boy. Nobody asked."),
        P("He laughs, but he shuts up. Nadia goes back to her salad like nothing happened."),
        D(N, "Eat your lunch. Ignore him.")],
    friend_until=40,
    sched=[{"weekdays": [0, 1, 2, 3, 4], "start_time": "11:30", "end_time": "14:00"}]))

out.append(spread("gossip_spread_quad", "The guy from your row", "quad", "talk_class", TODAY,
    "On the grass by the path, a guy who sits behind you in class is sitting with two girls. He sees you coming and leans in to them, and doesn't bother to whisper.",
    "Both girls look up at you at once. One of them covers her mouth. The other one doesn't look away.",
    [P("You walk past slow, right past them, close enough to hear the rest. You don't fold your arms and you don't look away. The girl who didn't look away watches your chest the whole way past."),
     WHO("Oh my god. She heard you."),
     P("He should sound sorry, but he sounds pleased."),
     T("Half your class knows. By next week it'll be all of it.")],
    [P("You stop right in front of him, so close your shadow's on his face."),
     ME("Tell them what you were doing, staring up my clothes in class instead of taking notes."),
     P("The girls laugh, at him. He goes red to the neck and finds something to read on his phone."),
     T("He'll still tell it, but not where you can hear.")],
    sched=[{"weekdays": [0, 1, 2, 3, 4], "start_time": "08:00", "end_time": "18:00"}]))

out.append(spread("gossip_spread_party", "Somebody tells the kitchen", "zoe_apartment", "talk_party", PARTY_TODAY,
    "In Zoe's kitchen a girl with a red cup is holding court by the fridge. She sees you in the doorway and smiles, wide, and tells the room.",
    "The kitchen goes quiet, then loud. Somebody whoops. Every face in there turns to you: guys you've never met, girls from your classes, a guy with a keg cup who looks at you like you're the next thing on the menu.",
    [P("You stand in the doorway and let them look. You don't deny it. The guy with the keg cup raises it to you, and his eyes go to your tits and stay there."),
     WHO("Is she gonna do it again?"),
     P("The girl by the fridge shrugs, smiling, like it's up to you."),
     *[G(cond(*exh_band(lo, hi)), T(line)) for (lo, hi, _), line in zip(BANDS, [
         "Your face is on fire. You want to be anywhere but this doorway, but your feet don't move.",
         "They're all going to tell it tomorrow. Your face burns, but you don't look away.",
         "They're all going to tell it tomorrow. You want them to tell it right.",
         "They're all going to tell it tomorrow. Good. Let them."])]],
    [P("You walk straight up to her and take the red cup out of her hand and drink half of it."),
     ME("You weren't even there."),
     P("The kitchen laughs, at her. She snatches the cup back and goes looking for someone else to tell."),
     T("It's a good line, but nobody in the kitchen believes it.")],
    friend=Z, friend_lines=[
        P("Zoe comes in from the living room, hears the end of it, and puts herself between you and the fridge."),
        D(Z, "Britt. My house, my friend. Say it again and you're out on the step."),
        P("Britt says nothing. Zoe hooks her arm through yours and steers you back out to the music."),
        D(Z, "She's jealous, babe. Look at you. Of course she is.")],
    sched=PARTY_SCHED, extra=(AT_PARTY,), him="her"))


# ═════════════════════════════════════════════════════════════════════════════
# 2. THE ASKS: strangers act on what they heard (CoT's "show us your tits" on the campus walk at exh ≥250,
#    cot_20:1219-1227; its party asks, cot_20:8990-9004). Her answers read her stage: below 20 she only lets the
#    look happen (rule 1); her bra at Daring (20, pays to 39); her bare tits for a moment at Watched (60, pays to
#    79; DECISIONS 203: a chosen show of bare breasts is 60; DECISIONS 204: a flash, not topless). Each yes spreads.
# ═════════════════════════════════════════════════════════════════════════════
TOP_ON = [{"type": "clothing_slot", "slot": "top", "operator": "equipped"}, {"type": "clothing_slot", "slot": "dress", "operator": "unequipped"}]
BRA_ON = {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}
BRA_OFF = {"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}


DRESS_ON = {"type": "clothing_slot", "slot": "dress", "operator": "equipped"}


def ask(cid, name, loc, level, today, intro, said, after_look, after_bra, after_bare, after_no, sched, extra=(), back="Walk on.",
        dress=None):
    exits = [
        go("Stop, and let them look.", node="look", mins=2, eff=[add("exhibitionism", 1, cap=19)], flags=[fset(today)],
           cond_=cond(trait("exhibitionism", "lt", 20))),
        go("Lift your top and flash your bra.", node="bra", mins=2, eff=[TALK1, add("exhibitionism", 1, cap=39)], flags=[fset(today)],
           cond_=cond(trait("exhibitionism", "gte", 20), *TOP_ON, BRA_ON)),
        go("Lift your top. Flash your tits.", node="bare", mins=2, eff=[TALK1, add("exhibitionism", 1, cap=79)], flags=[fset(today)],
           cond_=cond(trait("exhibitionism", "gte", 60), *TOP_ON, BRA_OFF)),
        *([go("Pull your dress down and flash your bra.", node="bra_d", mins=2, eff=[TALK1, add("exhibitionism", 1, cap=39)], flags=[fset(today)],
              cond_=cond(trait("exhibitionism", "gte", 20), DRESS_ON, BRA_ON)),
           go("Pull your dress down. Flash your tits.", node="bare_d", mins=2, eff=[TALK1, add("exhibitionism", 1, cap=79)], flags=[fset(today)],
              cond_=cond(trait("exhibitionism", "gte", 60), DRESS_ON, BRA_OFF))] if dress else []),
        go("Keep walking.", node="no", mins=1, flags=[fset(today)]),
    ]
    blocks = [P(intro),
              *said_chain(said, WHO),
              GC(cond(*none_of(ANY_TALK_FLAG)), WHO(said["none"])),
              WHO("Go on. Show us.")]
    nodes = [node("event", name, blocks, exits),
             node("look", "Let them look", after_look, [go(back, loc=loc, mins=0)]),
             node("bra", "Your bra", after_bra, [go(back, loc=loc, mins=0)]),
             node("bare", "Your tits", after_bare, [go(back, loc=loc, mins=0)]),
             node("no", "Keep walking", after_no, [go(back, loc=loc, mins=0)])]
    if dress:
        nodes += [node("bra_d", "Your bra", dress[0], [go(back, loc=loc, mins=0)]),
                  node("bare_d", "Your tits", dress[1], [go(back, loc=loc, mins=0)])]
    t = {"location": loc, "is_repeatable": True, "priority": 5, "is_active": True, "trigger_mode": "random", "chance": 0.3,
         "schedules": sched, "conditions": cond(flag("opening_done"), flag(today, False), TALK(level), *extra)}
    return {"id": cid, "name": name,
            "description": f"Gossip (DECISIONS 207): {name}. Strangers who heard about her ask her to show them (campus_talk {level}+). "
                           "1 in 3, one a day. Her answers by stage: let them look (under 20, to 19), her bra (20, to 39), "
                           "her bare tits for a moment (60, to 79); a yes spreads it (campus_talk +1).",
            "trigger": t, "nodes": nodes}


out.append(ask("gossip_ask_quad", "Three guys on the steps", "quad", 25, TODAY,
    "Three guys on the library steps stop talking when you come up the path. One of them nudges the others and stands up.",
    dict(ASK_QUAD, none="You're the new girl. The one everybody's talking about."),
    [P("You stop on the path in front of them and stand there, and let them look. Your face is hot. They look at your chest and your legs and your mouth, all three of them, and nobody says anything for a second."),
     WHO("Okay. Okay, that's something."),
     P("You want to stay, but you walk on before your nerve goes. Behind you one of them laughs, not mean, and says your name to the others like he's learning it."),
     T("You didn't show them anything, but your heart's going like you did.")],
    [P("You look round once. Then you grab the hem of your top and pull it up to your collarbone, right there on the path, and hold it. Your tits in your bra, pushed up, for three guys and anyone else on the steps."),
     WHO("Holy shit. She did it."),
     P("You count three and pull it down. The one standing sits down hard, like his legs went."),
     T("By tonight that's all three of them telling it. You can feel the grin on your own face.")],
    [P("You don't look round. You pull your top up to your chin, nothing under it, and stand there with your bare tits out to the library steps, nipples hard in the air, while three guys forget how to breathe."),
     WHO("Oh my god. Oh my god."),
     P("Two seconds. Three. You drop the top and walk on, not fast. Someone on the steps above them has a phone out, and you don't stop to see if it's pointed at you."),
     T("Everyone was right about you. You just proved it to their faces.")],
    [P("You walk past without slowing down, but you hear them laugh, and one of them calls after you."),
     WHO("Next time, then!"),
     T("Next time. Like it's already decided.")],
    sched=[{"weekdays": [0, 1, 2, 3, 4], "start_time": "08:00", "end_time": "18:00"}]))

out.append(ask("gossip_ask_party", "A guy who heard", "zoe_apartment", 60, PARTY_TODAY,
    "A guy you've never met finds you by the bathroom door in Zoe's hall. He's been looking for you; you can tell from how he smiles when he does.",
    dict(ASK_PARTY, none="I heard about you. Everybody's heard about you."),
    [P("You lean back on the wall and let him look. He takes his time about it: your legs, your chest, your mouth."),
     WHO("Yeah. They weren't lying."),
     P("He goes back to the kitchen and tells them all you said hi."),
     T("You didn't say anything. He'll tell it like you did.")],
    [P("You check the hall, then pull your top up over your bra and let him look, against the wall, with the party right there through the doorway."),
     WHO("They weren't lying."),
     P("When you pull it down he's already got his phone out, typing to someone."),
     T("Tomorrow the whole team knows. You want them to.")],
    [P("You don't check anything. You pull your top up over your bare tits in the hallway at Zoe's and hold it there. He stares. Two guys coming out of the kitchen stop dead in the doorway."),
     WHO("They weren't lying. Holy shit, they weren't lying."),
     P("You let it drop and walk past all three of them back to the music, nipples hard against your top."),
     T("They'll all tell it now. Every one of them saw it for himself.")],
    [P("He's cute, but you walk past him back to the music."),
     WHO("Worth a try. Everybody says you're up for it."),
     T("Everybody says. You can still feel his eyes on your ass, all the way to the kitchen.")],
    sched=PARTY_SCHED, extra=(AT_PARTY,), back="Back to the party.",
    dress=([P("You check the hall, then hook a finger in the neckline of your dress and pull it down over your bra, and let him look, against the wall, with the party right there through the doorway."),
            WHO("They weren't lying."),
            P("When you tug it back up he's already got his phone out, typing to someone."),
            T("Tomorrow the whole team knows. You want them to.")],
           [P("You don't check anything. You pull the front of your dress down under your bare tits in the hallway at Zoe's and hold it there. He stares. Two guys coming out of the kitchen stop dead in the doorway."),
            WHO("They weren't lying. Holy shit, they weren't lying."),
            P("You pull it back up and walk past all three of them to the music, nipples hard against the dress."),
            T("They'll all tell it now. Every one of them saw it for himself.")])))


# ═════════════════════════════════════════════════════════════════════════════
# 3. THE PASSER-BY (level 60): everyone has heard. A stranger says her name and the thing as he passes. Her line
#    moves from shame to pride by Exhibitionism band (her reaction drifts: CoT inclination, SYNTHESIS §1 item 7).
# ═════════════════════════════════════════════════════════════════════════════
out.append({
    "id": "gossip_passby", "name": "A stranger says your name",
    "description": "Gossip (DECISIONS 207): at campus_talk 60, a stranger on the quad says her name and what he heard. 1 in 4, "
                   "one a day. Her line by Exhibitionism band. Smiling back (Showing, 40) spreads it and pays to her stage's top.",
    "trigger": {"location": "quad", "is_repeatable": True, "priority": 5, "is_active": True, "trigger_mode": "random", "chance": 0.25,
                "schedules": [{"weekdays": [0, 1, 2, 3, 4, 5, 6], "start_time": "08:00", "end_time": "20:00"}],
                "conditions": cond(flag("opening_done"), flag(TODAY, False), TALK(60))},
    "nodes": [
        node("event", "Your name", [
            P("A guy you've never seen in your life passes you on the path, slows down, and says your name, like he's been waiting to try it out."),
            *said_chain(PASSBY, lambda line: WHO("@player, right? " + line)),
            GC(cond(*none_of(ANY_TALK_FLAG)), WHO("@player, right? Everybody's heard about you.")),
            *[G(cond(*exh_band(lo, hi)), T(line)) for (lo, hi, _), line in zip(BANDS, [
                "A total stranger. Your stomach drops. How many people have heard?",
                "A total stranger knows. Your face burns, but under it there's something else.",
                "A total stranger knows. You thought you'd hate that, but you don't.",
                "A total stranger knows. Good."])],
        ], [
            go("Keep walking.", node="walk", mins=1, flags=[fset(TODAY)]),
            *[go("Smile at him.", node="smile", mins=1, eff=[TALK1, add("exhibitionism", 1, cap=cap)], flags=[fset(TODAY)],
                 cond_=cond(*exh_band(lo, hi))) for lo, hi, cap in BANDS[2:]],
        ]),
        node("walk", "Keep walking", [
            P("You walk on with your face hot. Behind you he says it again to his friend, laughing."),
            T("Everybody. Everybody's heard.")], [go("Walk on.", loc="quad", mins=0)]),
        node("smile", "Smile at him", [
            P("You smile at him, slow, and let him look at you while you do it: your mouth, your chest, all the way down. He walks into the guy in front of him."),
            WHO("She smiled at me. Dude. She smiled."),
            T("Let him tell that one too.")], [go("Walk on.", loc="quad", mins=0)]),
    ]})

text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · GOSSIP (DECISIONS 207; SYSTEMS.md §9, sheets/systems/college.md)\n"
        "# The spread scenes, the asks on the quad and at the party, the passer-by.\n"
        "# =============================================================================\n")
text += "".join(emit(c) for c in out)
open(__import__("sys").argv[1], "w").write(text)
print("gossip:", len(out), "canvases")
