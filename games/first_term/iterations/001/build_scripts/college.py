"""College (sheets/systems/college.md, scenes college_*.md): the four classes, the guy beside her,
the dress-code warning, the midterms, the office hubs, the dean, Laura reading the grades.
Explicit screens pasted as signed."""
from canv import *
from tomlw import tod, wd

H, N = "npc_hale", "npc_nadia"
ART, BUS, TA, DEAN = "npc_art_lecturer", "npc_business_lecturer", "npc_bio_ta", "npc_dean"
DESK, RIVAL, STUDY, COCKY, MODEL = "npc_desk_guy", "npc_rival", "npc_study_guy", "npc_cocky_guy", "npc_figure_model"
Z, L = "npc_zoe", "npc_laura"
out = []
cards = []

def sched(*rows):
    return [{"weekdays": w, "start_time": a, "end_time": b} for w, a, b in rows]

PSYCH = sched(([0, 2, 4], "08:30", "10:00"), ([3], "13:00", "14:30"))
BUSI = sched(([0, 2], "10:15", "11:45"), ([1], "13:00", "14:30"))
BIO = sched(([1, 3], "10:15", "11:45"), ([0], "13:00", "14:30"))
FIG = sched(([1, 3], "08:30", "10:00"), ([2], "13:00", "14:30"))
HUNGRY = trait("corruption", "gte", 60)
WATCHED = trait("exhibitionism", "gte", 60)
DARING_STATE = cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"},
                    {"type": "worn_type", "operator": "eq", "value": "short_skirt"}, logic="OR")
CAP_BOLD = 59

def class_row(cid, name, subj, grade, schedules, lecturer, meet_flags, opening, beside, risky_label, risky_text, hungry_label, extra_blocks=()):
    """One class visit (the college sheet's rows): Focus · Chat · Doze · Skip · the risky slot,
    and the next stage's button shown locked, naming Hungry (SP7 call 1). Once per class window."""
    return {
        "id": cid, "name": name,
        "description": f"{subj} class: Focus (energy 10, {grade} +2, intelligence +1) · Chat · Doze (energy +5) · Skip ({grade} -2) · the risky slot (Daring) · Hungry shown locked.",
        "trigger": {"location": "lecture_hall", "is_repeatable": True, "priority": 5, "is_active": True,
                    "max_triggers_per_day": 1, "schedules": schedules, "conditions": cond(flag("opening_done"))},
        "nodes": [
            node("class", subj, [*opening, *extra_blocks,
                G(cond(trait("energy", "lt", 20)), T("Too tired to focus. Doze, or skip.")),
                G(DARING_STATE, P("You can feel eyes on you from the row behind. What you're wearing is doing its job.")),
            ], [
                go("Focus. (90 minutes, 10 energy)", node="focus", mins=0, costs=[{"trait": "energy", "value": 10}], flags=meet_flags,
                   eff=[add(grade, 2), add("intelligence", 1, clamp=False)]),
                go("Chat.", node="chat", mins=0, flags=meet_flags),
                go("Doze.", node="doze", mins=0, flags=meet_flags, eff=[{"targetType": "player", "trait": "energy", "op": "add", "value": 5, "cap": 100}]),
                go(risky_label, node="risky", mins=0, flags=meet_flags,
                   cond_=cond(trait("exhibitionism", "gte", 20), {"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}),
                   eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": CAP_BOLD}]),
                go(risky_label, node="risky", mins=0, flags=meet_flags,
                   cond_=cond(trait("exhibitionism", "gte", 20), {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}, {"type": "worn_type", "operator": "eq", "value": "short_skirt"}),
                   eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": CAP_BOLD}]),
                go(hungry_label, node="hungry", swl=True, cond_=cond(HUNGRY)),
                go("Skip it.", loc="campus", mins=0, eff=[add(grade, -2)]),
            ]),
            node("focus", "Focus", [POOL(
                P("You make yourself listen. You take notes in your neat hand, and somewhere in the second half it starts to make sense, and you feel smart, which is new."),
                P("You sit up and pay attention for the full ninety minutes. Your wrist aches by the end. You understood all of it."),
                P("You focus so hard you don't notice the room till it's emptying. Two pages of notes, and every one of them is useful.")),
                *beside], [go("Pack up.", loc="lecture_hall", mins=90)]),
            node("chat", "Chat", [*beside, POOL(
                P("You spend the class passing notes and whispering. You learn nothing about the subject and everything about who slept with who."),
                P("You talk the whole way through, low, heads together. The lecturer looks at you twice. You learn which parties are this week.")),
            ], [go("Pack up.", loc="lecture_hall", mins=90)]),
            node("doze", "Doze", [POOL(
                P("You put your head on your arms and the lecture becomes a warm drone. You wake with the imprint of your sleeve on your cheek and twenty minutes gone."),
                P("You sit at the back with your eyes half shut and let the class wash over you. Your body thanks you. Your notes do not.")),
            ], [go("Wake up.", loc="lecture_hall", mins=90)]),
            node("risky", "Let them look", [P(risky_text)], [go("Pack up, slowly.", loc="lecture_hall", mins=90)]),
            node("hungry", "Further", [P("That's further than you go in this release of First Term. It comes later, when you're Hungry.")],
                 [go("Back to the class.", node="class", mins=0)]),
        ]}

# ── Psychology (Hale; Nadia beside her; the guy beside her, the rival) ──
out.append(class_row(
    "college_class_psych", "Psychology (Dr. Hale)", "Psychology", "grade_psych", PSYCH, H,
    [fset("hale_met"), fset("nadia_met"), fset("desk_guy_met"), fset("rival_met")],
    [P("Psychology. Dr. Hale at the lectern in his tweed, the slides already up. Nadia has saved you the seat beside her in the front row, like always."),
     G(cond(trait("hale_step", "gte", 2)), P("He finds you in the front row before he says good morning. He always does now.")),
     G(cond(trait("hale_step", "gte", 4)), P("He can't look at you for long. He keeps his eyes on the back wall when he talks.")),
     G(cond(trait("grade_psych", "lt", 40)), D(H, "Some of you are failing this course. You know who you are.")),
     G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), P("He loses the sentence, and starts it again.")),
     ],
    [D(N, "He watches you more than the slides. Just saying.")],
    "Sit in the front row and let him look.",
    "You sit in the front row and don't fold your arms and don't cross your legs. Dr. Hale lectures to the back wall for ninety minutes, and every time he forgets and looks down, his voice goes. Nadia kicks your foot under the desk, grinning.",
    "Under the desk, with the class there. (Needs Hungry)"))

# ── Business (strict; the rival; the study guy) ──
out.append(class_row(
    "college_class_business", "Business", "Business", "grade_business", BUSI, BUS,
    [fset("desk_guy_met")],
    [P("Business. The lecturer is a grey man in a grey suit who calls the register and means it. The study guy is already in the row behind you with three highlighters out. The rival girl sits where she can watch you."),
     D(BUS, "Phones away. Eyes up. This is on the exam."),
     G(cond(trait("grade_business", "lt", 40)), D(BUS, "Retakes are by appointment. Honest work only. I won't say it twice.")),
     ],
    [D(STUDY, "You want my notes? You can have my notes. Seriously, any time."),
     G(cond(flag("dress_warned")), D(RIVAL, "Nice of you to dress for once."))],
    "Lean back so the row behind can see.",
    "You lean back in your chair and stretch, slowly, and the study guy in the row behind stops highlighting. For ninety minutes he doesn't write a word. The rival girl watches him watching you, and her mouth gets thinner and thinner.",
    "Make the whole row look. (Needs Hungry)"))

# ── Biology (the shy TA; Zoe; the cocky guy) ──
out.append(class_row(
    "college_class_bio", "Biology", "Biology", "grade_bio", BIO, TA,
    [],
    [P("Biology. The TA runs it, a shy woman in a lab coat who blushes when she has to say reproductive system out loud. The girl beside you whispers through the slides."),
     G(cond(flag("zoe_met", False)), WHO("Quad after? I'm always there. Tuesdays, Thursdays, Fridays.")),
     G(cond(flag("zoe_met")), D(Z, "Babe. Look at the TA. She's staring at your legs again.")),
     G(cond(trait("grade_bio", "lt", 40)), D(TA, "If anyone's struggling, my door's open in the afternoons. Really. Any afternoon.")),
     ],
    [G(cond(flag("zoe_met")), D(Z, "Party Friday. I'm not asking."))],
    "Let the TA see.",
    "You sit with your knees apart in the second row and don't fix anything. The TA sees. She drops her pen, picks it up, drops it again. She spends the rest of the class looking very hard at her slides, her neck pink all the way down to her collar.",
    "Let the whole lab see. (Needs Hungry)"))

# ── Figure drawing (the model, nude; the art lecturer; Zoe; the cocky guy) — the pose beat every class ──
POSE = ("The model drops her robe on the platform and steps up naked under the lamp. She sits on the stool and turns her shoulder to the room. Her tits are heavy. They sway when she settles. Her nipples are dark and tight in the cold air. Your charcoal follows the curve of her ass where it spreads on the stool. You draw her thighs, pressed together, and the soft crease between them. You can't stop looking. Your face burns. Your own nipples go hard. The lecturer walks the rows behind you. \"Look at the weight of her,\" she says. \"Draw that.\" Zoe kicks your ankle under the easel. You keep drawing the heavy swing of the model's tits, but it's your nipples that ache.")
fig = class_row(
    "college_class_figure", "Figure drawing", "Figure drawing", "grade_art", FIG, ART,
    [],
    [P(POSE),
     VID("a nude female life model posing on a stool under a lamp in an art class, students drawing at easels", "nude model posing art class students drawing", "life drawing class naked model on stool", pool_dir="sex/figure_class_pose_t4"),
     G(cond(flag("cocky_guy_met")), P("At the next easel, Jake's teammate isn't drawing the model. He's drawing you.")),
     ],
    [D(ART, "Better. Look at what's actually there, not what you think is there.")],
    "Lean into your easel and let them look.",
    "You lean into your easel, slow, and let what you're wearing do the work. The cocky guy at the next easel gives up on the model completely. The art lecturer stops behind you, looks at your drawing, looks at you, and says nothing at all, which from her is a speech.",
    "Pose for the class. (Needs Watched)")
# posing nude for the class is Watched (SP2 §1: the stage turns on how many see her)
fig["nodes"][0]["choices"][5] = go("Pose for the class. (Needs Watched)", node="hungry", swl=True, cond_=cond(WATCHED))
out.append(fig)

# ── first classes: meeting the staff (LIVES §6: the lecturers at their first class) ──
def first_class(cid, name, sch, met, people_flags, blocks):
    return {"id": cid, "name": name, "description": f"Meets the {name.lower()} people at the first class. Sets {met}.",
            "trigger": {"location": "lecture_hall", "is_repeatable": False, "priority": 8, "is_active": True,
                        "schedules": sch, "conditions": cond(flag("opening_done"), flag(met, False))},
            "nodes": [node("first", name, blocks, [go("Find a seat.", loc="lecture_hall", mins=2, flags=[fset(met)] + [fset(f) for f in people_flags])])]}

out.append(first_class("meet_business", "Your first Business class", BUSI, "business_lecturer_met", ["study_guy_met", "rival_met"], [
    P("Business is a grey room with a grey man at the front of it: the Business lecturer, fifty, a suit with no creases, a register in his hand he actually calls."),
    D(BUS, "I don't do extensions. I don't do excuses. I do honest work, and I grade it honestly. Sit down."),
    P("The guy in the row behind you, the one with three highlighters, leans forward."),
    D(STUDY, "I'm doing study group Thursday. If you, um. If you want."),
    P("And a girl from your Psychology class, the sharp one, watches you sit and doesn't smile."),
    D(RIVAL, "Oh. You're in this one too."),
]))
out.append(first_class("meet_bio", "Your first Biology class", BIO, "bio_ta_met", [], [
    P("Biology is taught by the TA, a shy woman of twenty-eight in a lab coat and big earrings, who blushes when she says reproductive."),
    D(TA, "Hi. I'm— I'll be taking you this term. Please don't eat the specimens. That was a joke. Sort of."),
    P("Her eyes go round the room and land on you and skip off you, fast, like she touched something hot."),
    D(TA, "My door's open in the afternoons. If anyone. You know. Needs anything."),
]))
out.append(first_class("meet_figure", "Your first Figure drawing class", FIG, "art_lecturer_met", ["cocky_guy_met", "figure_model_met"], [
    P("Easels in a horseshoe round a platform with a stool on it, and a woman in a dressing gown sitting on the edge of the platform drinking from a flask: the model."),
    D(ART, "Figure drawing. Bodies. You'll draw what's there, not what you think is there, and you will not giggle. She's working. Respect it."),
    P("The art lecturer is forty-five, charcoal on her hands, and she looks at every new face like she's measuring it for a frame."),
    D(MODEL, "First years. Lovely. Nobody faint."),
    P("The guy at the next easel is in a team jacket: Jake's teammate, the cocky one. He looks you over, slow, and grins."),
    D(COCKY, "This is going to be a good class."),
]))
# ── the guy beside her (college_event_desk_guy; Psychology and Business; once a day) ──
DESK_HAND = ("He leans in close. \"I'm hard,\" he whispers. \"Help me out.\" You check the room first. The lecturer faces the board. The row in front has its heads down. The desk hides everything below your elbows, so you slide your hand under it and open his jeans. His cock springs into your fingers, hot and thick, slick at the tip. You stroke his cock slow, root to head. He grips the desk edge and breathes through his nose so he won't make a sound. Your face burns, but you go faster. His cock throbs in your fist and his balls pull tight. He comes over your knuckles, under the desk where nobody sees. You wipe your palm on his thigh while his cock twitches against his open jeans.")
out.append({
    "id": "college_event_desk_guy", "name": "The guy beside you",
    "description": "College event in Psychology and Business: the guy beside her is hard. Curious: she looks. Bold: her hand, unseen under the desk (explicit). Once a day.",
    "trigger": {"location": "lecture_hall", "is_repeatable": True, "priority": 4, "is_active": True, "max_triggers_per_day": 1,
                "schedules": PSYCH + BUSI, "conditions": cond(flag("desk_guy_met"), trait("corruption", "gte", 20))},
    "nodes": [
        node("ask", "Beside you", [
            P("The guy who sits beside you has his jacket across his lap and his jaw clenched. He catches you looking and leans in."),
            D(DESK, "I'm hard. Help me out."),
            T("He said it like he was asking for a pen."),
        ], [
            go("Look.", node="watch", mins=3),
            go("Help him.", node="hand", mins=3, cond_=cond(trait("corruption", "gte", 40))),
            go("\"Not here.\"", node="no", mins=1),
        ]),
        node("watch", "Look", [
            P("The rival girl, two seats down, has stopped writing and is watching the two of you."),
            P("You look. He moves the jacket an inch so you can see the shape of it straining his jeans, and watches you look, and grins at the board like nothing's happening."),
            D(DESK, "Next time, then."),
        ], [go("Back to the class.", loc="lecture_hall", mins=60)]),
        node("hand", "Under the desk", [
            P(DESK_HAND),
            VID("under a lecture desk a girl's hand in a guy's open jeans, the class facing the front", "handjob under desk in class", "girl hand in guy jeans under lecture desk", pool_dir="sex/desk_guy_hand_t5"),
        ], [go("Wipe your hand.", loc="lecture_hall", mins=60,
               eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": CAP_BOLD}])]),
        node("no", "Not here", [D(DESK, "Worth a try."), P("Two seats down the rival girl smirks into her notes."), P("He shrugs and puts his jacket straight and copies the slide like a good boy. He keeps glancing at your hands for the rest of the class.")],
             [go("Back to the class.", loc="lecture_hall", mins=60, flags=[fset("desk_guy_refused")])]),
    ]})

# ── the dress-code warning (wardrobe pool, in class; once a day). Twice is a complaint ──
out.append({
    "id": "college_event_dress_code", "name": "A word about what you're wearing",
    "description": "Wardrobe event in class: a lecturer's warning about what she wears (no bra, a short skirt). The first sets dress_warned; after that the rival complains (complaints +1). Exhibitionism +1, once a day.",
    "trigger": {"location": "lecture_hall", "is_repeatable": True, "priority": 4, "is_active": True, "max_triggers_per_day": 1,
                "schedules": PSYCH + BUSI + BIO, "conditions": DARING_STATE},
    "nodes": [node("warning", "After class", [
        P("As the room empties the lecturer calls your name and waits until it's just the two of you."),
        G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}), P("Their eyes go to your chest, where everybody's eyes have been all class, and away.")),
        G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), P("Their eyes go to your skirt, and away.")),
        WHO("This is a lecture hall, not a nightclub. Think about how you come to class."),
        G(cond(flag("dress_warned")), P("At the door, the rival girl is waiting with her bag on her shoulder and a little smile."), D(RIVAL, "I told the dean's office. Somebody had to.")),
    ], [
        go("\"Yes. Sorry.\"", loc="lecture_hall", mins=5, cond_=cond(flag("dress_warned", False)), flags=[fset("dress_warned")],
           eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": CAP_BOLD}]),
        go("\"Yes. Sorry.\"", loc="lecture_hall", mins=5, cond_=cond(flag("dress_warned")),
           eff=[add("complaints", 1, clamp=False), {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": CAP_BOLD}]),
    ])]})

# ── the midterms (college_exam): weeks 7-8, once per exam, in that subject's slot ──
FLASH = ("\"Show me and I'll tilt my paper.\" He breathes it without looking up. The proctor sits at the front, reading. Every head in the row is bent over a page. You check the room once. Then you pull everything up under the desk line, where only he can see. Your tits are bare in the cold hall air. Your nipples go hard at once, tight and aching. His pen stops mid-word. His eyes drop to your tits and stay there. One second. Two. Three. You yank everything down and cover your breasts. He slides his paper to the edge of his desk. Your nipples are still hard, and his stare is still on your chest.")
WEEKS_7_8 = [{"type": "days_since_flag", "subject": "player", "flag_key": "opening_done", "operator": "gte", "value": 42},
             {"type": "days_since_flag", "subject": "player", "flag_key": "opening_done", "operator": "lt", "value": 56}]
for subj, grade, sch, code in [("Psychology", "grade_psych", PSYCH, "psych"), ("Business", "grade_business", BUSI, "business"),
                               ("Biology", "grade_bio", BIO, "bio"), ("Figure drawing", "grade_art", FIG, "art")]:
    done_f = f"exam_{code}_done"
    out.append({
        "id": f"college_exam_{code}", "name": f"The {subj} midterm",
        "description": f"The {subj} midterm (college_exam), weeks 7-8 in its class slot: Focus (reads intelligence), flirt for the study guy's paper (Curious), or a flash for the cocky guy's (Daring, explicit). Copying +5. Sets {done_f} and midterm_done.",
        "trigger": {"location": "lecture_hall", "is_repeatable": False, "priority": 9, "is_active": True,
                    "schedules": sch, "conditions": cond(*WEEKS_7_8, flag(done_f, False))},
        "nodes": [
            node("paper", "The midterm", [
                P(f"The {subj} midterm. Desks pulled apart, bags at the front, a proctor reading a paperback by the door. The paper lands face-down in front of you, and the clock on the wall starts."),
                G(cond(trait("intelligence", "lt", 10)), T("You know some of this. Not enough of it.")),
                G(cond(trait("intelligence", "gte", 10)), T("You studied. You actually know this.")),
            ], [
                go("Focus. Do it yourself.", node="result", mins=90, cond_=cond(trait("intelligence", "gte", 10)), eff=[add(grade, 6)]),
                go("Focus. Do it yourself.", node="result", mins=90, cond_=cond(trait("intelligence", "lt", 10)), eff=[add(grade, 1)]),
                go("Flirt with the study guy for his paper.", node="study", mins=5, cond_=cond(trait("corruption", "gte", 20))),
                *([go("Look at the cocky guy.", node="price", mins=5, cond_=cond(trait("exhibitionism", "gte", 20), flag("cocky_guy_met")))] if code == "art" else []),
            ]),
            node("study", "The study guy", [
                P("You catch the study guy's eye across the gap and bite your lip and look at his paper and back at him. He goes red to the ears. A minute later his paper is on the corner of his desk, angled your way, and he's staring at the ceiling like a saint."),
            ], [go("Copy.", node="result", mins=85, eff=[add(grade, 5), add("campus_talk", 1, clamp=False)])]),
            *([
            node("price", "His price", [
                P("Jake's teammate is at the next desk with his paper finished and his pen behind his ear. He sees you looking at it and leans back in his chair."),
            ], [go("\"What?\"", node="flash_ask", mins=1), go("Look away.", node="result", mins=89, eff=[add(grade, 1)])]),
            node("flash_ask", "Show me", [
                D(COCKY, "Show me and I'll tilt my paper."),
            ], [go("Show him.", node="flash", mins=2), go("\"No.\"", node="result", mins=88, eff=[add(grade, 1)])]),
            node("flash", "Three seconds", [
                P(FLASH),
                VID("under a desk in an exam hall a girl lifts her top for the guy at the next desk, rows of students writing", "girl flashes tits during exam under desk", "exam hall flash for answers", file=f"sex/exam_{code}_flash_t4.webm"),
            ], [go("Copy.", node="result", mins=85, eff=[add(grade, 5), {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": CAP_BOLD}])])
            ] if code == "art" else []),
            node("result", "Pens down", [
                P("Pens down. The proctor collects the papers row by row. A week later the result is on the portal, and on the office door."),
                G(cond(trait(grade, "lt", 40)), P("Failing. Red, with a circle round it. Laura is going to see this.")),
                G(cond(trait(grade, "gte", 40), trait(grade, "lt", 70)), P("A pass. Fine. Nobody will say anything.")),
                G(cond(trait(grade, "gte", 70)), P("Near the top. For once the portal is going to make Laura smile.")),
            ], [go("Leave the hall.", loc="campus", mins=5, flags=[fset(done_f), fset("midterm_done")])]),
        ]})

# ── the lecturers in the lecture hall, before and after class (their class hubs) ──
def hub(cid, loc, npc, met, name, blocks, choices=None):
    return {"id": cid, "name": name, "description": f"{name}: one line on her grade, one on her clothes.",
            "trigger": {"location": loc, "npc": npc, "requires_npc": npc, "is_repeatable": True, "priority": 6, "is_active": True,
                        "conditions": cond(flag(met))},
            "nodes": [node("hub", name, blocks, choices or [go("Go.", loc=loc)])]}

def grade_lines(npc, grade, low, mid, top):
    return [G(cond(trait(grade, "lt", 40)), D(npc, low)),
            G(cond(trait(grade, "gte", 40), trait(grade, "lt", 70)), D(npc, mid)),
            G(cond(trait(grade, "gte", 70)), D(npc, top))]

def clothes_line(npc, line):
    return G(DARING_STATE, D(npc, line))

out.append(hub("hub_hale_class", "lecture_hall", H, "hale_met", "Dr. Hale, at the lectern", [
    P("Dr. Hale is packing his notes into his bag, slowly, the way he does when he's waiting to see who stays."),
    *grade_lines(H, "grade_psych", "You're behind, @player. Come and see me on Thursday.", "Good work. Could be better.", "Best paper in the room. Don't let it go to your head."),
    G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), P("He loses the sentence, and starts it again.")),
]))
out.append(hub("hub_art_class", "lecture_hall", ART, "art_lecturer_met", "The art lecturer", [
    P("The art lecturer is wiping charcoal off her hands with a rag, looking at you the way she looks at the model."),
    *grade_lines(ART, "grade_art", "You're drawing what you expect, not what's there. Look harder.", "Better. Your lines are getting braver.", "You see bodies properly. I'd like to draw you one day."),
    clothes_line(ART, "That's a good line you're wearing today. I mean the shape, not the clothes."),
]))
out.append(hub("hub_business_class", "lecture_hall", BUS, "business_lecturer_met", "The Business lecturer", [
    P("The Business lecturer is wiping the board clean in long straight lines."),
    *grade_lines(BUS, "grade_business", "Failing. Retakes by appointment.", "Adequate.", "Good. Keep it that way."),
    clothes_line(BUS, "This isn't a beach, @player."),
]))
out.append(hub("hub_ta_class", "lecture_hall", TA, "bio_ta_met", "The Biology TA", [
    P("The TA is stacking handouts with her back to the room. She turns, sees you, and drops half of them."),
    *grade_lines(TA, "grade_bio", "You're, um. You're struggling. My door's open. If you want.", "You're doing fine! Really fine.", "Top marks. Wow. Sorry. Top marks."),
    clothes_line(TA, "You look— sorry. Nothing. You look nice."),
]))

# ── the offices (college_office_talk): art, business (the honest retake), TA, the dean ──
out.append(hub("hub_art_office", "art_office", ART, "art_lecturer_met", "The art lecturer's office", [
    P("Canvases against every wall. The art lecturer looks up from a sketch of a woman's back."),
    *grade_lines(ART, "grade_art", "Sit. Show me your book. Ah. Yes. We have work to do.", "You're improving. Draw every day.", "You have an eye. Come and sit for me some time."),
    clothes_line(ART, "Stand by the window a moment. The light's good on you."),
]))
out.append(hub("hub_business_office", "business_office", BUS, "business_lecturer_met", "The Business lecturer's office", [
    P("The Business lecturer looks up from his marking and doesn't smile."),
    *grade_lines(BUS, "grade_business", "Failing. I can offer an honest retake. Nothing else.", "You're passing. Keep it honest.", "Good work. That's all."),
    clothes_line(BUS, "You can wear what you like. It won't change your grade. Nothing does."),
], [
    go("\"I'll take the retake.\"", node="retake", mins=5, cond_=cond(trait("grade_business", "lt", 40), flag("business_retake_used", False)),
       flags=[fset("business_retake_used")]),
    go("Go.", loc="business_office"),
]))
out[-1]["nodes"].append(node("retake", "The retake", [
    P("He hands you a paper and points at a chair, and sits watching you for an hour without blinking. You know more than you thought."),
    D(BUS, "Honest work. Thank you."),
], [go("Hand it in. (Business +5)", loc="business_office", mins=60, eff=[add("grade_business", 5)])]))
out.append(hub("hub_ta_office", "ta_office", TA, "bio_ta_met", "The TA's office", [
    P("The TA's office is half a room with a skeleton in the corner wearing a party hat. She jumps when you knock."),
    *grade_lines(TA, "grade_bio", "Oh! Hi. Your grade. Um. We should fix your grade. Sit?", "You're doing well. Do you want tea?", "You're my best student. Don't tell anyone I said that."),
    clothes_line(TA, "I like your— never mind. Sit down. Please."),
]))
out.append(hub("hub_dean_office", "dean_office", DEAN, "dean_met", "The dean", [
    P("The dean doesn't get up. He waits for you to sit in the hard chair before he looks at you."),
    G(cond(flag("on_probation")), D(DEAN, "You're on probation. Every grade, every complaint, crosses my desk now.")),
    G(cond(flag("on_probation", False)), D(DEAN, "You're not in trouble. Yet. Keep it that way.")),
    G(DARING_STATE, D(DEAN, "Is that what you wore to class?")),
]))

# ── the dean's warning: the calls bring her in (complaints, or failing a week after Laura saw it) ──
out.append({
    "id": "dean_warning", "name": "The dean's office",
    "description": "Her first trouble: the dean's warning. Meets the dean; sets dean_met, on_probation (if failing) and letter_home (laura_suspicion +10). Played by answering the dean's office's call.",
    "trigger": {"location": "dean_office", "is_repeatable": False, "priority": 1, "is_active": True, "substitution_only": True},
    "nodes": [node("warning", "The warning", [
        P("The dean's secretary sends you straight in. The dean is a grey-haired man in a pressed shirt with a file open in front of him. Your name is on the file."),
        D(DEAN, "Sit down, @player."),
        G(cond(trait("complaints", "gte", 2)), D(DEAN, "Complaints about your conduct in class. Your clothes. This is a college, not a stage.")),
        G(cond(flag("failing_noticed")), D(DEAN, "And your grades. You're failing. I'm putting you on probation.")),
        D(DEAN, "Your parents will be getting a letter. Consider this your warning."),
        T("A letter home. Laura is going to read every word of it."),
    ], [
        go("\"Yes, sir.\"", loc="dean_office", mins=20, cond_=cond(flag("failing_noticed")),
           flags=[fset("dean_met"), fset("dean_summons"), fset("on_probation"), fset("letter_home")], eff=[add("laura_suspicion", 10, clamp=True)]),
        go("\"Yes, sir.\"", loc="dean_office", mins=20, cond_=cond(flag("failing_noticed", False)),
           flags=[fset("dean_met"), fset("dean_summons"), fset("letter_home")], eff=[add("laura_suspicion", 10, clamp=True)]),
    ])]})

# ── Laura reads the grades (the failing chain): one per subject, in her evening kitchen ──
for grade, subj in [("grade_psych", "Psychology"), ("grade_business", "Business"), ("grade_bio", "Biology"), ("grade_art", "Figure drawing")]:
    out.append({
        "id": f"laura_reads_{grade}", "name": "Laura, with the portal open",
        "description": f"The failing chain: {subj} under 40 and Laura sees it at home. laura_suspicion +5; the curfew if her Warmth is low or suspicion 50+. Once a week (cleared at the Sunday count).",
        "trigger": {"location": "home_kitchen", "requires_npc": L, "is_repeatable": True, "priority": 7, "is_active": True, "max_triggers_per_day": 1,
                    "schedules": [{"weekdays": [0, 1, 3, 4, 6], "start_time": "18:00", "end_time": "22:00"}],
                    "conditions": cond(flag("opening_done"), trait(grade, "lt", 40), flag("grades_seen", False))},
        "nodes": [node("portal", "The portal", [
            P(f"Laura is at the kitchen table with her phone, and the college's portal open on it, and your {subj} grade in red. She turns the phone round so you can see it."),
            D(L, "Do you want to explain this to me, sweetheart?"),
            G(cond(flag("letter_home")), D(L, "After the letter. After the dean wrote to us.")),
        ], [
            go("\"I'll fix it.\"", loc="home_kitchen", mins=15, cond_=cond(ntrait(L, "warmth", "gte", 40), trait("laura_suspicion", "lt", 45)),
               flags=[fset("grades_seen"), fset("failing_noticed")], eff=[add("laura_suspicion", 5)]),
            go("\"I'll fix it.\"", node="curfew", mins=5, cond_=cond(ntrait(L, "warmth", "lt", 40), trait("laura_suspicion", "gte", 45), logic="OR"),
               flags=[fset("grades_seen"), fset("failing_noticed")], eff=[add("laura_suspicion", 5)]),
        ]), node("curfew", "Grounded", [
            D(L, "You'll fix it from this house, then. A week. No parties, no late shifts, no dates."),
        ], [go("\"Fine.\"", loc="home_kitchen", mins=10, flags=[fset("curfew")], eff=CURFEW_EFF)])]})

out.append({
    "id": "lecture_timetable", "name": "Read the timetable on the door",
    "description": "The timetable: when each class is. Writes nothing.",
    "trigger": {"location": "lecture_hall", "is_repeatable": True, "priority": 1, "is_active": True},
    "nodes": [node("timetable", "The timetable", [
        P("The timetable is taped to the door, three classes a day. Monday: Psychology, Business, Biology. Tuesday: Figure drawing, Biology, Business. Wednesday: Psychology, Business, Figure drawing. Thursday: Figure drawing, Biology, Psychology. Friday: just Psychology, first thing, and then the weekend."),
        P("Mornings start at half eight. The afternoon class starts after lunch. Somebody has drawn a penis on Thursday, but nobody has rubbed it off."),
    ], [go("Done.", loc="lecture_hall")])]})

text = "# ── college (sheets/systems/college.md · scenes college_*.md) ──\n" + "".join(emit(c) for c in out)
open(__import__("sys").argv[1], "w").write(text)
print("college:", len(out), "canvases")
