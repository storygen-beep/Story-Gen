"""Showing off to get something (DECISIONS 210; LO, 2026-11-09, "Go ahead" on A and C).

The studied pattern (exhibition_study/C_other_games.md:315, pattern 13, "exposure as a tool for a goal"):
curse-of-the-abyss gives the tavern job a goal, show more to bring men to the abyss, and prints "of 30
adventurers" after each one (co:3841-3845); corrupted-city's roommate outfit gets her the club job (cc:1174-1180).
A reason that is not about sex, a count she can see, and an end. The study's warning: the reason fades once the
goal is met, so each goal here ends in a payoff and Zoe's opens the next one for a later release.

A. Zoe's party needs a crowd: `zoe_crowd`, 10. Zoe asks by text (phone.py zoe_crowd); the asks on the quad, at the
   gym and in the canteen, once a day each; the payoff the first Friday after ten (party_crowd).
C. The study guy's notes: `study_notes`, 5. The library, weekdays, from week 4 until the Business midterm; the
   payoff is a new answer at that midterm (college.py college_exam_business).

Every ask has a plain way that always gets a no and counts nothing. Each yes is a show at her own stage:
Daring (20, pays to 39) close, nothing shown; Showing (40, pays to 59) her panties, a moment; Watched (60, pays to
79) her bare tits for a moment (DECISIONS 203-204). The count is said on the screen after the +1, one line per
count, fenced in its own one-item pool so it can't become the else of the screen's last group (v2.py:18686-18691).
"""
from canv import *
from tomlw import tod

out = []
Z, STUDY = "npc_zoe", "npc_study_guy"
TALK1 = add("campus_talk", 1, clamp=False)
NUM = ["", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten"]
EXH = lambda n: trait("exhibitionism", "gte", n)

# what she has on (the gate "her clothes are backed": a line that names a garment sits behind its check)
TOP_ON = [{"type": "clothing_slot", "slot": "top", "operator": "equipped"}, {"type": "clothing_slot", "slot": "dress", "operator": "unequipped"}]
DRESS_ON = {"type": "clothing_slot", "slot": "dress", "operator": "equipped"}
BRA_OFF = {"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}
PANTIES_ON = {"type": "clothing_slot", "slot": "underwear", "operator": "equipped"}
# a hem she can lift: the two short skirts, or a dress she goes out in (not the towel, the sleep shirt or a uniform)
HEMS = [[{"type": "worn_type", "operator": "eq", "value": "short_skirt"}],
        [{"type": "worn_type", "operator": "eq", "value": "split_skirt"}],
        [DRESS_ON, {"type": "worn_beauty", "operator": "gte", "value": 2},
         {"type": "worn_type", "operator": "neq", "value": "cafe_uniform"}]]

NO_HEM = cond({"type": "worn_type", "operator": "neq", "value": "short_skirt"}, {"type": "worn_type", "operator": "neq", "value": "split_skirt"},
              {"type": "clothing_slot", "slot": "dress", "operator": "unequipped"})
BRA_ON = {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}
PANTIES_OFF = {"type": "clothing_slot", "slot": "underwear", "operator": "unequipped"}


def counted(key, lines):
    """The count, said after the +1: lines[n-1] at count n. One fenced first-match chain."""
    chain = [GC(cond(trait(key, "lt", n + 1)), P(line)) for n, line in enumerate(lines, 1)]
    chain[-1] = GC(cond(trait(key, "gte", len(lines))), P(lines[-1]))
    return G(cond({"type": "worn_exposure", "operator": "gte", "value": 0}), *chain)


def crowd_lines(place):
    """Zoe's count, in this place's words (gate: one pool, one place)."""
    lines = [f"That's the first one for Zoe, and he's {place}. Nine more to find."]
    for n in range(2, 10):
        lines.append(f"{NUM[n].capitalize()} for Zoe now, counting this one {place}. {NUM[10 - n].capitalize()} to go.")
    lines.append(f"Ten. This one {place} makes ten. Zoe's going to lose her mind.")
    return lines


def pay(key, cap, talk=False, extra=()):
    return [add("exhibitionism", 1, cap=cap), add(key, 1, clamp=False)] + ([TALK1] if talk else []) + list(extra)


# ═════════════════════════════════════════════════════════════════════════════
# A. ZOE'S CROWD: the asks. They read the hidden trait zoe_crowd_asked, not the flag: the flag is set by a phone
# reply, which has no place, and the flag-chain check fails a trigger that needs a flag with no located setter
# (v2.py validate_flag_chains). The flag stays for the card and the text's own guard.
# ═════════════════════════════════════════════════════════════════════════════
def crowd_ask(cid, name, loc, sched, place, close_label, intro, more_blocks, flash_blocks, off, plain_no, close, show, bare, bare_d, show_choice=None):
    """show_choice: (label, extra conditions) for the Showing answer where a hem isn't the way (the gym's mats)."""
    flag_here = f"crowd_{loc}"
    yes = lambda cap, talk, extra=(): dict(eff=pay("zoe_crowd", cap, talk), flags=[fset(flag_here)] + list(extra))
    # The stage gates sit on two doors ("A little more." at 40, "Flash him." at 60); what she has on picks the act
    # behind each door, so a stage is checked once, not once per garment (gate: the climb is where you said it is).
    exits = [go("Ask him to come.", node="no", mins=2),
             go(close_label, node="close", mins=3, **yes(39, False)),
             go("Give him a little more.", node="more", mins=0, cond_=cond(EXH(40))),
             go("Flash him.", node="flash", mins=0, cond_=cond(EXH(60))),
             go("Not today.", loc=loc, mins=0)]
    if show_choice:
        more = [go(show_choice[0], node="show", mins=3, cond_=cond(*show_choice[1]), **yes(59, True))]
    else:
        more = [go("Lift your hem and let him see your panties.", node="show", mins=2, cond_=cond(PANTIES_ON, *h), **yes(59, True))
                for h in HEMS]
    flash = [go("Lift your top. Flash him your tits.", node="bare", mins=2, cond_=cond(*TOP_ON, BRA_OFF), **yes(79, True, [fset("crowd_flashed")])),
             go("Pull your dress down. Flash him your tits.", node="bare_d", mins=2, cond_=cond(DRESS_ON, BRA_OFF), **yes(79, True, [fset("crowd_flashed")]))]
    count = counted("zoe_crowd", crowd_lines(place))
    back = [go("Leave him to it.", loc=loc, mins=0)]
    nodes = [node("ask", name, intro, exits),
             node("more", "A little more", more_blocks, more + [go("Change your mind.", node="off", mins=1)]),
             node("flash", "A flash", flash_blocks, flash + [go("Change your mind.", node="off", mins=1)]),
             node("off", "Not today", off, back),
             node("no", "Ask him", plain_no, back),
             node("close", "Close", close + [count], back),
             node("show", "A look", show + [count], back),
             node("bare", "A flash", bare + [count], back),
             node("bare_d", "A flash", bare_d + [count], back)]
    return {"id": cid, "name": name,
            "description": f"Zoe's crowd (DECISIONS 210): find someone {place} for Zoe's party. Once a day while zoe_crowd_on and "
                           "zoe_crowd under 10. Asking plainly gets a no and counts nothing; a show at her stage gets a yes: "
                           "close (20, to 39), her panties (40, to 59, campus_talk +1), her bare tits for a moment (60, to 79, campus_talk +1). "
                           "Each yes: zoe_crowd +1, said on the screen.",
            "trigger": {"location": loc, "is_repeatable": True, "priority": 4, "is_active": True, "max_triggers_per_day": 1,
                        "schedules": sched,
                        "conditions": cond(trait("zoe_crowd_asked", "gte", 1), trait("zoe_crowd", "lt", 10), EXH(20))},
            "nodes": nodes}


out.append(crowd_ask("crowd_ask_quad", "Find someone for Zoe's party", "quad",
    [{"weekdays": [0, 1, 2, 3, 4, 5, 6], "start_time": "08:00", "end_time": "20:00"}], "off the quad", "Sit down on the grass next to him, close, and ask.",
    [P("A guy is stretched out on the grass by the path with his bag under his head and his eyes shut. He opens them when your shadow lands on his face."),
     WHO("Hey. Can I help you?"),
     T("Zoe wants ten. You need a yes out of him, and you know what gets guys to say yes.")],
    [P("You lean in over him, close. He's already looking at you; now you can give him something to look at."),
     WHO("Go on, then. Convince me."),
     G(NO_HEM, T("You'd lift your hem for him, but there's nothing short enough on to lift.")),
     G(cond(PANTIES_OFF), T("There are no panties under your clothes, so a little more would be everything, on the quad."))],
    [P("You look up and down the path. Nobody close. He props himself up on his elbows, watching your hands."),
     WHO("What are you doing? What are you, oh."),
     G(cond(BRA_ON), T("Not with a bra on. It'd have to come off first, and not here."))],
    [P("You straighten up and step back off the grass. He lies back down with his bag under his head, grinning at the sky."),
     WHO("Tease. Tell your friend I said maybe."),
     ME("Maybe means you'll come. I'll hold you to it."),
     WHO("Sure you will. Bye, tease."),
     T("Maybe isn't a yes. That's one more to find somewhere else.")],
    [ME("My friend's having a party. You should come."),
     P("He looks at you for a second, then shuts his eyes again."),
     WHO("Yeah, maybe. Everybody's having a party. But thanks."),
     T("Maybe means no. Asking nicely won't get Zoe her ten.")],
    [P("You sit down on the grass right next to him, close, your knee against his hip. You lean over him while you tell him about Zoe's party, slowly, so he has time to look. He looks at your mouth, then your chest, then your legs, and he doesn't hear a word you say."),
     WHO("Yeah. Yeah, I'll come. Where is it? What time? Can I bring my roommate?"),
     ME("Bring whoever you want. Just come."),
     P("You put Zoe's address into his phone yourself, leaning in, and he breathes in when your hair brushes his face."),
     T("He didn't come for the party. He came for you.")],
    [P("You sit down on the grass facing him with your knees up, lift your hem out of the way, and let your knees drift apart while you talk. His eyes drop between your thighs and stay there, on your panties, right there on the quad with people walking past."),
     WHO("Okay. Yes. Whatever it is, yes. I'll be there early."),
     P("You close your knees and get up. A girl on the path saw it, and she's already telling her friend."),
     T("Your face is hot, and you're grinning. That's how you get a yes.")],
    [P("You check the path once. Then you kneel over him on the grass and pull your top up, and your bare tits are right there over his face for three seconds, nipples tight in the open air."),
     WHO("Oh my god. Yes. I'm coming. I'm definitely coming."),
     P("You drop the top and stand up. Two guys on the library steps are on their feet, staring."),
     T("Three seconds. You could have got ten off the quad with that.")],
    [P("You check the path once. Then you kneel over him on the grass and pull the front of your dress down, and your bare tits are right there over his face for three seconds, nipples tight in the open air."),
     WHO("Oh my god. Yes. I'm coming. I'm definitely coming."),
     P("You pull the dress up and stand. Two guys on the library steps are on their feet, staring."),
     T("Three seconds. You could have got ten off the quad with that.")]))

out.append(crowd_ask("crowd_ask_gym", "Find someone for Zoe's party", "campus_gym",
    [{"weekdays": [0, 1, 2, 3, 4, 5, 6], "start_time": "08:00", "end_time": "21:00"}], "from the gym", "Sit on the end of his bench, close, and ask.",
    [P("A guy on the bench by the rack is between sets, red-faced, drinking from a bottle. He's been watching you in the mirror wall since you walked in."),
     WHO("You need the bench?"),
     T("Zoe wants ten. He's already looking. You just have to give him a reason to say yes.")],
    [P("You don't move off his bench. You let him see you thinking about it, and in the mirror wall he watches you do it."),
     WHO("You're still here. Okay. Sell it to me.")],
    [P("You look at the door, then at the mirror wall. Every guy in here is in it, and so are you."),
     WHO("Wait. You're not going to, are you?"),
     G(cond(BRA_ON), T("Not with a bra on. It'd have to come off first, and not in front of the whole gym."))],
    [P("You step back from his bench. He watches you go in the mirror wall, and picks his bar back up."),
     WHO("That's it? Come on. You can't just sit there and leave."),
     ME("Watch me. Think about the party."),
     T("Not today. He'll still be on that bench tomorrow.")],
    [ME("My friend's having a party. You should come."),
     P("He wipes his face on his towel and goes back to his set."),
     WHO("I'm cutting. No parties till the meet. Sorry, but no."),
     T("He'd go if you gave him a reason. Asking isn't a reason.")],
    [P("You sit on the end of his bench, close, so your thigh is against his, and tell him about Zoe's party. He forgets his set. In the mirror wall you can see him looking at your chest the whole time you talk, and the guy at the rack watching both of you."),
     WHO("Yeah. I'll be there. Save me a drink. Save me a dance, too."),
     ME("Come and find out."),
     P("He's still looking when you get up. So is the guy at the rack."),
     T("He'll come, and he'll bring his eyes.")],
    [P("You get down on the mat right in front of his bench and stretch while you tell him about Zoe's party. Legs wide, then wider, chest down to the mat, and your ass up for him. He puts the bar back on the rack without looking at it."),
     WHO("Okay. I'll come. Just keep doing that. Don't stop doing that."),
     P("You sit up slow. The guy at the rack has stopped his set to watch, and so has the guy behind him."),
     T("Every guy in the gym just saw how you get a yes.")],
    [P("You check the door once. Then you stand in front of his bench and pull your top up, and your bare tits are right there in front of his face for three seconds, nipples hard, and in the mirror wall the whole gym sees them too."),
     WHO("Holy shit. Yes. Wherever it is, yes."),
     P("You drop the top. Somebody by the treadmills drops a weight."),
     T("Three seconds, in a room made of mirrors.")],
    [P("You check the door once. Then you stand in front of his bench and pull the front of your dress down, and your bare tits are right there in front of his face for three seconds, nipples hard, and in the mirror wall the whole gym sees them too."),
     WHO("Holy shit. Yes. Wherever it is, yes."),
     P("You pull the dress up. Somebody by the treadmills drops a weight."),
     T("Three seconds, in a room made of mirrors.")],
    show_choice=("Stretch out on the mat in front of him while you ask.", [{"type": "clothing_slot", "slot": "bottom", "operator": "equipped"}])))

out.append(crowd_ask("crowd_ask_canteen", "Find someone for Zoe's party", "canteen",
    [{"weekdays": [0, 1, 2, 3, 4], "start_time": "11:30", "end_time": "14:00"}], "from the canteen", "Sit on his table, close, and ask.",
    [P("At the end of the long table a guy is eating alone with a textbook propped against the ketchup. He looks up when you stop beside him with your tray."),
     WHO("Seat's free, if you want it."),
     T("Zoe wants ten. He's on his own, and he's already looking at you.")],
    [P("You put your tray down on his table and stay standing over him."),
     WHO("You're really selling this party, huh?"),
     G(NO_HEM, T("You'd need a short hem to lift over lunch, but not in these clothes.")),
     G(cond(PANTIES_OFF), T("There are no panties under your clothes, so lifting your hem in here would show the whole canteen everything."))],
    [P("You glance round the canteen. Trays, phones, a hundred people looking down at their lunch."),
     WHO("Why are you looking round like that?"),
     G(cond(BRA_ON), T("Not with a bra on. It'd have to come off first, and not over lunch."))],
    [P("You pick your tray back up. He watches you go, and the ketchup bottle falls over when he reaches for it."),
     WHO("Hey, wait. What about the party? Are you coming back?"),
     ME("Ask me nicely tomorrow."),
     T("Let him think about it over lunch. You can ask him again another day.")],
    [ME("My friend's having a party. You should come."),
     P("He smiles, polite, and turns a page."),
     WHO("Thanks, but I'm not really a party guy. I've got a lab Saturday."),
     T("He'd be a party guy for the right reason.")],
    [P("You don't take the seat. You sit on the table, right next to his tray, and lean on one hand while you tell him about Zoe's party, close enough that he has to look up at you. He looks everywhere except your face."),
     WHO("Yeah, okay. I'll come. Text me where. I mean it, text me."),
     ME("I'll text you. Don't flake on me."),
     P("Half the next table watched you do it."),
     T("A whole canteen, and he only saw you.")],
    [P("You sit on the edge of the table facing him and cross your legs, slowly, then uncross them, and let him see your panties right there over his lunch. His fork stops halfway to his mouth."),
     WHO("Okay. Yes. I'm there. I'm so there."),
     P("Somebody at the next table laughs, and somebody else says your name."),
     T("Your face is on fire, but he said yes.")],
    [P("You check the room once. Then you lean down over his tray and lift your top, and your bare tits are right there for three seconds, between him and his textbook, nipples hard, with the whole canteen behind you."),
     WHO("Jesus. Yes. Yes, I'll come."),
     P("You drop the top and pick up your tray. The table behind him has gone dead quiet."),
     T("Three seconds over lunch. They'll be talking about it all afternoon.")],
    [P("You check the room once. Then you lean down over his tray and pull the front of your dress down, and your bare tits are right there for three seconds, between him and his textbook, nipples hard, with the whole canteen behind you."),
     WHO("Jesus. Yes. Yes, I'll come."),
     P("You pull the dress up and pick up your tray. The table behind him has gone dead quiet."),
     T("Three seconds over lunch. They'll be talking about it all afternoon.")]))


# ── A. the payoff: the first Friday party after ten (one time). It fires inside the party (party_went in the last 8 hours). ──
AT_PARTY = {"type": "hours_since_flag", "subject": "player", "flag_key": "party_went", "operator": "lt", "value": 8}
DONE = [fset("zoe_crowd_done")]
out.append({
    "id": "party_crowd", "name": "The crowd you brought",
    "description": "Zoe's crowd (DECISIONS 210), the payoff, once: the first Friday party after zoe_crowd reaches 10. The guys she "
                   "brought cheer her in; Zoe's dare in front of all of them, by stage. Every way out pays campus_talk +5 and sets "
                   "zoe_crowd_done. Zoe opens the next count for a later release.",
    "trigger": {"location": "zoe_apartment", "is_repeatable": False, "priority": 9, "is_active": True,
                # Zoe's row at the flat ends at 02:00 on Saturday and the scene runs about half an hour
                "schedules": [{"weekdays": [4], "start_time": "19:00", "end_time": "00:00"}, {"weekdays": [5], "start_time": "00:00", "end_time": "01:15"}],
                "conditions": cond(trait("zoe_crowd", "gte", 10), flag("zoe_crowd_done", False), AT_PARTY)},
    "nodes": [
        node("packed", "Packed", [
            P("Zoe's flat is packed to the walls. People on the stairs, people on the balcony, a line for the bathroom down the hall. Half the faces are ones you brought."),
            G(cond(flag("crowd_quad")), WHO("There she is! The girl off the quad!")),
            G(cond(flag("crowd_campus_gym")), WHO("Gym girl! You said there'd be a party. You didn't say it'd be this good.")),
            G(cond(flag("crowd_canteen")), WHO("She's the reason I'm here. Ask me how she asked.")),
            G(cond(flag("crowd_flashed")), P("Somebody by the speakers is telling the story of how you asked him, with his hands, and the guys round him look over at your chest when he gets to the end.")),
            WHO("Is that her? That's her. She's the one who told me about this place."),
            G(cond(flag("crowd_campus_gym")), WHO("She told everybody. I heard she asked half the gym.")),
            P("Zoe pushes through all of them and grabs your face in both hands."),
            D(Z, "Ten. I said ten and you got me ten. Look at this place. I didn't think you'd do it, but look."),
            D(Z, "They all came for you, babe. So give them something. Up on the table."),
        ], [
            go("Laugh her off.", node="end", mins=10, eff=[add("campus_talk", 5, clamp=False)], flags=DONE),
            go("Dance with them on the floor.", node="floor", mins=20,
               eff=[add("exhibitionism", 1, cap=39), add("campus_talk", 5, clamp=False)], flags=DONE),
            go("Get up on the coffee table.", node="table", mins=20, cond_=cond(EXH(40)),
               eff=[add("exhibitionism", 2, cap=79), add("campus_talk", 5, clamp=False)], flags=DONE),
        ]),
        node("floor", "On the floor", [
            P("You don't get on the table, but you let Zoe drag you into the middle of the room, and the guys you brought close in round you. You dance with all of them, one after another, hands on your hips, on your waist, someone's chest against your back."),
            WHO("This is the best party she's ever had."),
            WHO("Hey, you invited me, remember? You owe me a dance."),
            ME("I owe everybody a dance tonight, apparently."),
            T("Your face is burning, and you don't want it to stop.")], [go("Find Zoe.", node="end", mins=5)]),
        node("table", "On the table", [
            P("Zoe sweeps the cups off the coffee table with her arm, and you climb up. The room turns to you and roars. You dance up there with your arms over your head, hips rolling, your tits bouncing with the bass, and every guy you brought is right at the edge of the table looking up at you."),
            G(cond(EXH(60), *TOP_ON, BRA_OFF), P("When someone shouts for more, you give it to them: you pull your top down off one shoulder, then the other, and hold it there at the very edge of your nipples while the room screams, and then you pull it back up and laugh.")),
            G(cond(EXH(60), DRESS_ON, BRA_OFF), P("When someone shouts for more, you give it to them: you slide your dress down off one shoulder, then the other, and hold it there at the very edge of your nipples while the room screams, and then you pull it back up and laugh.")),
            WHO("Again! Again!"),
            WHO("That's the girl who got us all here! Give it up for her!"),
            D(Z, "Told you they came for you. Look at them, babe."),
            VID("a woman dancing on a coffee table at a packed house party, the crowd cheering up at her", "girl dancing on table at party crowd cheering", "college party table dance", file="sex/party_crowd_table_t3.webm"),
            T("They came for you. You're giving them what they came for.")], [go("Climb down to Zoe.", node="end", mins=5)]),
        node("end", "Twice the size", [
            P("Later, out on the balcony, Zoe hands you a cup and clinks hers against it."),
            D(Z, "Everyone's going to be talking about this one. Half of them are already asking when the next one is."),
            ME("You're going to make me do it again, aren't you?"),
            D(Z, "Next one's twice the size. Don't look at me like that. You know you can."),
            T("Twenty. She wants twenty next time."),
        ], [go("Back inside.", loc="zoe_apartment", mins=5)]),
    ]})


# ═════════════════════════════════════════════════════════════════════════════
# C. THE STUDY GUY'S NOTES: five chapters before the Business midterm
# ═════════════════════════════════════════════════════════════════════════════
NOTES = ["One chapter of his notes in your bag. Four more before the midterm.",
         "Two chapters in your bag now, highlighted three colours. Three to go before the midterm.",
         "Three of his five chapters. Two more and you'll know that paper better than he does.",
         "Four chapters. One more before the midterm.",
         "All five chapters. You could sit the Business midterm in your sleep."]
NOTES_EFF = lambda cap, talk=False: pay("study_notes", cap, talk, [add("intelligence", 1), nadd(STUDY, "want", 1)])
NOTES_COUNT = counted("study_notes", NOTES)
WEEK4 = {"type": "days_since_flag", "subject": "player", "flag_key": "opening_done", "operator": "gte", "value": 21}
back = [go("Leave him to his binders.", loc="library", mins=0)]
out.append({
    "id": "study_notes", "name": "Sit with the study guy",
    "description": "The study guy's notes (DECISIONS 210): five chapters before the Business midterm, from week 4, weekdays in the "
                   "library, once a day. Asking nicely gets a no; a show at her stage gets a chapter: close (20, to 39), her panties "
                   "under the table (40, to 59), a flash in the stacks (60, to 79). Each chapter: study_notes +1, intelligence +1. "
                   "Five open a new answer at the Business midterm (college.py).",
    "trigger": {"location": "library", "is_repeatable": True, "priority": 4, "is_active": True, "max_triggers_per_day": 1,
                # not in his Business class (classes.py BUSI: Mon/Wed 10:15-11:45, Tue 13:00-14:30), where he sits behind her
                "schedules": [{"weekdays": [0, 2], "start_time": "08:00", "end_time": "10:15"}, {"weekdays": [0, 2], "start_time": "11:45", "end_time": "19:30"},
                              {"weekdays": [1], "start_time": "08:00", "end_time": "13:00"}, {"weekdays": [1], "start_time": "14:30", "end_time": "19:30"},
                              {"weekdays": [3, 4], "start_time": "08:00", "end_time": "19:30"}],
                "conditions": cond(flag("study_guy_met"), WEEK4, flag("exam_business_done", False), trait("study_notes", "lt", 5), EXH(20))},
    "nodes": [
        node("table", "His notes", [
            P("The study guy has a whole end of the long table to himself: four binders, three highlighters, Business notes in tabs by chapter. He sees you and puts his hand flat on the top binder."),
            # his want: how many times she has paid him (people_data.py npc_study_guy), so he remembers
            GC(cond(ntrait(STUDY, "want", "lt", 2)), D(STUDY, "I know what you want. Everybody wants these before the midterm."),
               D(STUDY, "One chapter at a time. And they're not free.")),
            GC(cond(ntrait(STUDY, "want", "lt", 4)), D(STUDY, "I wondered which chapter you'd want next. I hoped you'd want one."),
               D(STUDY, "Next chapter's right here. Same price.")),
            GC(cond(ntrait(STUDY, "want", "gte", 4)), D(STUDY, "I can't get any work done in here any more. I keep looking at the door for you."),
               D(STUDY, "Sit down. Please. I already pulled the chapter out for you.")),
        ], [
            go("Ask nicely.", node="no", mins=2),
            go("Sit on the table, right on his notes, and ask.", node="close", mins=20, eff=NOTES_EFF(39)),
            go("Give him a little more.", node="more", mins=0, cond_=cond(EXH(40))),
            go("Take him into the stacks.", node="stacks", mins=2, cond_=cond(EXH(60))),
            go("Leave him to his binders.", loc="library", mins=0),
        ]),
        node("more", "A little more", [
            P("You sit down across from him instead and slide your chair in, close, so your knees are under his side of the table."),
            D(STUDY, "What are you doing down there?"),
            G(NO_HEM, T("Nothing short enough on to hitch up. Not in these clothes.")),
            G(cond(PANTIES_OFF), T("No panties on. Under the table that wouldn't be a little more, here.")),
        ], [*[go("Hitch your hem up under the table and open your knees.", node="show", mins=20, cond_=cond(PANTIES_ON, *h), eff=NOTES_EFF(59))
              for h in HEMS],
            go("Change your mind.", node="off_more", mins=1)]),
        node("stacks", "The back aisle", [
            P("You take his wrist and walk him back into the stacks, past the end of the aisle where nobody goes. He comes along like he's been hoping for this since week one."),
            D(STUDY, "Here? Someone could come round the end."),
            ME("Then be quick looking."),
            G(cond(BRA_ON), T("Not with a bra on. It'd have to come off first, and you'd never get it back on before somebody came.")),
        ], [go("Lift your top.", node="bare", mins=18, cond_=cond(*TOP_ON, BRA_OFF), eff=NOTES_EFF(79)),
            go("Pull your dress down.", node="bare_d", mins=18, cond_=cond(DRESS_ON, BRA_OFF), eff=NOTES_EFF(79)),
            go("Change your mind.", node="off", mins=2)]),
        node("off_more", "Not today", [
            P("You pull your chair back out from under his side of the table. He looks at you, then at his binders, and pulls the chapter back to his side."),
            D(STUDY, "Your call. Same chapter tomorrow. It's not going anywhere."),
            T("He's not going anywhere either.")], back),
        node("off", "Not today", [
            P("You let go of his wrist and step back out of the aisle. He follows you back to the long table and pulls the chapter back across it, to his side."),
            D(STUDY, "Your call. It'll still be here. So will I. Same chapter, same price, any day you want it."),
            T("He's not going anywhere. Neither are his notes.")], back),
        node("no", "Nicely", [
            ME("Please? Just one chapter."),
            G(cond(ntrait(STUDY, "want", "lt", 3)), D(STUDY, "Nicely doesn't cost you anything. That's the problem with nicely.")),
            G(cond(ntrait(STUDY, "want", "gte", 3)), D(STUDY, "You've paid me before. Don't go shy on me now.")),
            P("He goes back to his highlighting, but he's smiling."),
            D(STUDY, "You know where to find me. Same table, every weekday till the midterm."),
            T("He'll give them up. Just not for a please.")], back),
        node("close", "On his notes", [
            P("You sit on the table right on top of his open binder, so he has to look up at you to see anything, and you cross your legs slowly and ask him to explain break-even. He explains it to your chest. He doesn't notice he's doing it, and you let him go on."),
            D(STUDY, "Okay. Okay, take this one. Bring it back. And come back for the next one, okay?"),
            ME("Maybe. Depends what it costs."),
            P("He slides the chapter out from under your thigh, warm, and holds it out without looking at it."),
            NOTES_COUNT], back),
        node("show", "Under the table", [
            P("You sit across from him and hitch your hem up under the table, all the way, and open your knees. He drops his highlighter. When he ducks under the table to get it, he stays down there, looking straight up between your thighs at your panties, for a long time."),
            D(STUDY, "That's. Yeah. Take the chapter. Take two, if you want. No, one. One a day. I can't take more than that."),
            P("A girl two seats down looks up from her laptop at the sound of his head hitting the table on the way up."),
            NOTES_COUNT], back),
        node("bare", "In the stacks", [
            P("You lift your top, and your bare tits are right there in front of him for three seconds between the shelves, nipples hard in the cold library air."),
            D(STUDY, "Oh. Oh, wow. Okay. I didn't think you'd actually do it."),
            P("You drop the top and hold out your hand. He puts the chapter in it without a word, and somebody on the other side of the shelf stops turning pages."),
            NOTES_COUNT], back),
        node("bare_d", "In the stacks", [
            P("You pull the front of your dress down, and your bare tits are right there in front of him for three seconds between the shelves, nipples hard in the cold library air."),
            D(STUDY, "Oh. Oh, wow. Okay. I didn't think you'd actually do it."),
            P("You pull the dress up and hold out your hand. He puts the chapter in it without a word, and somebody on the other side of the shelf stops turning pages."),
            NOTES_COUNT], back),
    ]})


# ── the guidance cards: where and when, and the goal that flips ──
cards = [
    {"npc_id": Z, "priority": 6, "heading": "Zoe's big party",
     "text": "Zoe wants ten people at her next party, and she wants you to find them.",
     "tip": "The quad and the gym any day, the canteen at lunch on weekdays. Asking nicely won't do it. Zoe asks once you're Daring (Exhibitionism 20).",
     "when": [{"flag": "zoe_met", "op": "is_true"}, {"flag": "zoe_crowd_on", "op": "is_true"}, {"type": "trait", "subject": "player", "trait": "zoe_crowd", "op": "lt", "value": 10}],
     "goals": [{"type": "trait", "subject": "player", "trait": "exhibitionism", "op": "gte", "value": 20, "label": "Daring (Exhibitionism 20)"},
               {"type": "trait", "subject": "player", "trait": "zoe_crowd", "op": "gte", "value": 10, "label": "Ten people for Zoe's party"}],
     "ready_canvas": "crowd_ask_quad"},
    {"npc_id": Z, "priority": 6, "heading": "Zoe's big party",
     "text": "Ten are coming. Zoe's party, Friday night.",
     "tip": "Zoe's flat, Friday, 7 PM to midnight",
     "when": [{"flag": "zoe_met", "op": "is_true"}, {"flag": "zoe_crowd_done", "op": "is_false"}, {"type": "trait", "subject": "player", "trait": "zoe_crowd", "op": "gte", "value": 10}],
     "ready_canvas": "party_crowd"},
    {"npc_id": STUDY, "priority": 6, "heading": "His notes",
     "text": "He'll trade his Business notes before the midterm, a chapter at a time, once you're Daring (Exhibitionism 20). Not for a please.",
     "tip": "The library, weekdays, 8 AM to 7:30 PM except in Business class, from your fourth week, once you're Daring (Exhibitionism 20)",
     "when": [{"flag": "study_guy_met", "op": "is_true"}, {"flag": "exam_business_done", "op": "is_false"},
              {"type": "trait", "subject": "player", "trait": "study_notes", "op": "lt", "value": 5},
              {"type": "trait", "subject": "player", "trait": "exhibitionism", "op": "gte", "value": 20}],
     "goals": [{"type": "trait", "subject": "player", "trait": "exhibitionism", "op": "gte", "value": 20, "label": "Daring (Exhibitionism 20)"},
               {"type": "trait", "subject": "player", "trait": "study_notes", "op": "gte", "value": 5, "label": "All five chapters of his notes"}],
     "ready_canvas": "study_notes"},
]

text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · GOALS (DECISIONS 210): Zoe's crowd and the study guy's notes\n"
        "# =============================================================================\n")
text += "".join(emit(c) for c in out) + "".join(emit_card(c) for c in cards)
open(__import__("sys").argv[1], "w").write(text)
print("goals:", len(out), "canvases,", len(cards), "cards")
