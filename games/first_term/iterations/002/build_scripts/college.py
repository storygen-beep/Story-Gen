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

from classes import sched, PSYCH, BUSI, BIO, FIG   # one source with the timetable screen


def at_start(rows, mins=15):
    """The first quarter-hour of each class slot (iteration 002, part 8, reader): a canvas that opens a
    class, or spends the class, fires only while the class is starting, never in its last minute."""
    def plus(t):
        h, m = map(int, t.split(":")); m += mins
        return f"{h + m // 60:02d}:{m % 60:02d}"
    return [dict(r, end_time=plus(r["start_time"])) for r in rows]
HUNGRY = trait("corruption", "gte", 60)
WATCHED = trait("exhibitionism", "gte", 60)
DARING_STATE = cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"},
                    {"type": "worn_type", "operator": "eq", "value": "short_skirt"}, logic="OR")
CAP_BOLD = 59
# The two clothing sets DARING_STATE and the risky buttons cover (copy fixes B, DECISIONS 125): a line that
# names her body has to be true for the set on screen, so it splits into one group per set. They never overlap.
BRALESS = {"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}
SKIRT_WITH_BRA = [{"type": "clothing_slot", "slot": "bra", "operator": "equipped"},
                  {"type": "worn_type", "operator": "eq", "value": "short_skirt"}]

def by_clothes(braless_blocks, skirt_blocks, *after):
    """The risky screen's text: one group for braless, one for skirt-with-a-bra, then the lines true for both."""
    return [G(cond(BRALESS), *braless_blocks), G(cond(*SKIRT_WITH_BRA), *skirt_blocks), *after]

# Each class its own lines (iteration 002, part 4: sweep A5-09, A5-15; gate one pool, one place).
POOLS = {
    "psych": {
        "focus": ["You take notes on attachment theory until your hand cramps. Somewhere in the second half it clicks, and you feel smart, which is new.",
                  "Dr. Hale walks through a case study, a man who couldn't feel fear. You write down every word of it, and you understand all of it."],
        "chat": ["Nadia whispers through the whole lecture: who's seeing who, which TA cries in the car park. You learn nothing about psychology.",
                 "You and Nadia pass notes in the margin of her reader. By the end the margin's full and the slides are a blur."],
        "doze": ["You sink down in your seat and let Dr. Hale's voice turn into a warm hum. You wake when the room starts packing up.",
                 "Your eyes close somewhere around the third slide. Nadia nudges you awake for the last five minutes."],
        "eyes": "In the front row you can feel the whole room behind you. What you're wearing is doing its job.",
        "tired": "Too tired to take in a word of Psychology. Doze, or skip."},
    "business": {
        "focus": ["Supply, demand, a case about a shoe company that went bust. You fill two pages and could argue it either way.",
                  "The grey man talks in bullet points, and you write them all down. It's dull, but it's on the exam."],
        "chat": ["The guy in the row behind leans forward to whisper answers before the lecturer asks the questions. You learn more about him than about markets.",
                 "You whisper about Friday with the girl beside you until the lecturer says your name, flat, without looking up."],
        "doze": ["You prop your chin on your hand and drift. The lecturer's voice never changes pitch, which makes it easy.",
                 "Ninety minutes of margins and percentages. You nod off twice, and you catch yourself both times."],
        "eyes": "You can feel the study guy's eyes on the back of your neck. What you're wearing is doing its job.",
        "tired": "Too tired for margins and percentages. Doze, or skip."},
    "bio": {
        "focus": ["Cells, then more cells. You label the diagram until it makes sense, and by the end it does.",
                  "The TA goes through the heart valve by valve, pink to the ears. You take careful notes and understand all of it."],
        "chat": ["You whisper with the girl beside you through the slides, about everything but biology.",
                 "The back row passes a phone along with somebody's party photos on it. You look at every one."],
        "doze": ["The lab is warm and the TA's voice is soft. You put your head on the bench and lose twenty minutes.",
                 "You sit with your eyes half shut while the slides click past. Your body thanks you, but your notes don't."],
        "eyes": "Across the lab bench, the TA keeps looking and looking away. What you're wearing is doing its job.",
        "tired": "Too tired to label a single cell. Doze, or skip."},
    "figure": {
        "focus": ["You draw for ninety minutes without looking up. By the end your page holds her shoulder, her hip, the line of her back, and it looks like a person.",
                  "You fill three sheets with fast, loose sketches. The last one is good, and you know it is."],
        "chat": ["You draw with one hand and whisper with the girl at the next easel. Your drawing is mostly elbows.",
                 "Charcoal on your fingers, you talk through the pose about everything but the model. The lecturer clears her throat at you twice."],
        "doze": ["The lamp is warm and the room is quiet except for charcoal on paper. You stop drawing and let your eyes close.",
                 "You sit back from the easel and let the room go soft. Your page stays half a shoulder."],
        # reader a3 #25-26 (DECISIONS 131): one watcher at Exhibitionism 20, not a room of easels (H1: a group is stage 4)
        "eyes": "The guy at the next easel has stopped drawing the model. What you're wearing is doing its job.",
        "tired": "Too tired to hold the charcoal straight. Doze, or skip."},
}

def class_row(cid, name, subj, grade, schedules, lecturer, meet_flags, opening, beside, risky_label, risky_text, extra_blocks=(),
              pools=None, chat_beside=None):
    """One class visit (the college sheet's rows): Focus · Chat · Doze · Skip · the risky slot.
    No button for a stage this release does not write (LO 2026-11-03: "dont even show the option").
    Once per class window."""
    eyes_line = pools["eyes"]
    return {
        "id": cid, "name": name,
        "description": f"{subj} class: Focus (energy 10, {grade} +2, intelligence +1) · Chat · Doze (energy +5) · Skip ({grade} -2) · the risky slot (Daring).",
        "trigger": {"location": "lecture_hall", "is_repeatable": True, "priority": 5, "is_active": True,
                    "max_triggers_per_day": 1, "schedules": at_start(schedules), "conditions": cond(flag("opening_done"))},
        "nodes": [
            node("class", subj, [*opening, *extra_blocks,
                G(cond(trait("energy", "lt", 20)), T(pools["tired"])),
                G(DARING_STATE, P(eyes_line)),
            ], [
                # Shut under 20 energy, as the thought says (college.md "The lock", sweep A5-08)
                go("Focus. (90 minutes, 10 energy)", node="focus", mins=0, costs=[{"trait": "energy", "value": 10}], flags=meet_flags,
                   swl=True, cond_=cond(trait("energy", "gte", 20)),
                   eff=[add(grade, 2), add("intelligence", 1, clamp=False)]),
                go("Chat.", node="chat", mins=0, flags=meet_flags),
                go("Doze.", node="doze", mins=0, flags=meet_flags, eff=[{"targetType": "player", "trait": "energy", "op": "add", "value": 5, "cap": 100}]),
                go(risky_label, node="risky", mins=0, flags=meet_flags,
                   cond_=cond(trait("exhibitionism", "gte", 20), {"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}),
                   eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": CAP_BOLD}]),
                go(risky_label, node="risky", mins=0, flags=meet_flags,
                   cond_=cond(trait("exhibitionism", "gte", 20), {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}, {"type": "worn_type", "operator": "eq", "value": "short_skirt"}),
                   eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": CAP_BOLD}]),
                go("Skip it.", loc="campus", mins=0, eff=[add(grade, -2)]),
            ]),
            node("focus", "Focus", [POOL(*[P(t) for t in pools["focus"]]), *beside], [go("Pack up.", loc="lecture_hall", mins=90)]),
            node("chat", "Chat", [*(beside if chat_beside is None else chat_beside), POOL(*[P(t) for t in pools["chat"]])], [go("Pack up.", loc="lecture_hall", mins=90)]),
            node("doze", "Doze", [POOL(*[P(t) for t in pools["doze"]])], [go("Wake up.", loc="lecture_hall", mins=90)]),
            node("risky", "Let them look", [P(risky_text)] if isinstance(risky_text, str) else list(risky_text), [go("Pack up, slowly.", loc="lecture_hall", mins=90)]),
        ]}

# ── Psychology (Hale; Nadia beside her; the guy beside her, the rival) ──
out.append(class_row(
    "college_class_psych", "Attend the Psychology lecture", "Psychology", "grade_psych", PSYCH, H,
    [fset("hale_met"), fset("nadia_met"), fset("desk_guy_met"), fset("rival_met")],
    [G(cond(flag("hale_met"), flag("nadia_met")), P("Psychology. Dr. Hale at the lectern in his tweed, the slides already up. Nadia has saved you the seat beside her in the front row, like always.")),
     G(cond(flag("hale_met", False)), P("Psychology. A man in tweed at the lectern, slides already up: Dr. Hale, the timetable says. A girl in big glasses in the front row moves her bag off the seat beside her and pats it."),
       WHO("Sit here. I'm Nadia. Nobody sits at the front for him. You'll see why.")),
     G(cond(trait("hale_step", "gte", 2)), P("He finds you in the front row before he starts. He always does now.")),
     G(cond(trait("hale_step", "gte", 4)), P("He can't look at you for long. He keeps his eyes on the back wall when he talks.")),
     G(cond(trait("grade_psych", "lt", 40)), D(H, "Some of you are failing this course. You know who you are.")),
     G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), P("His eyes drop to your thighs. He loses the sentence, steps back behind the lectern, and starts it again.")),
     ],
    [D(N, "He watches you more than the slides. Just saying.")],
    "Sit in the front row and let him look.",
    by_clothes(
        [P("You sit in the front row and don't fold your arms over your chest, and don't cross your legs. Dr. Hale lectures to the back wall for ninety minutes, and every time he forgets and looks down at your chest, his voice goes. Nadia kicks your foot under the desk, grinning.")],
        [P("You sit in the front row and don't fold your arms over your chest, and don't cross your legs. Dr. Hale lectures to the back wall for ninety minutes, and every time he forgets and looks down at your thighs, his voice goes. Nadia kicks your foot under the desk, grinning.")],
        P("As the room packs up, he says it without looking at you."),
        D(H, "Sit like that again, @player, and we'll talk about your grade.")),
    pools=POOLS["psych"]))

# ── Business (strict; the rival; the study guy) ──
out.append(class_row(
    "college_class_business", "Attend the Business lecture", "Business", "grade_business", BUSI, BUS,
    [fset("desk_guy_met")],
    [P("Business. The lecturer is a grey man in a grey suit who calls the register and means it."),
     G(cond(flag("study_guy_met")), P("The study guy is already in the row behind you with three highlighters out.")),
     G(cond(flag("rival_met")), P("The rival girl sits where she can watch you.")),
     D(BUS, "Phones away. Eyes up. This is on the exam."),
     G(cond(trait("grade_business", "lt", 40)), D(BUS, "Retakes are by appointment. Honest work only. I won't say it twice.")),
     ],
    [D(STUDY, "You want my notes? You can have my notes. Seriously, any time."),
     G(cond(flag("dress_warned"), flag("rival_met"), {"type": "clothing_slot", "slot": "bra", "operator": "equipped"},
            {"type": "worn_type", "operator": "neq", "value": "short_skirt"}), D(RIVAL, "Nice of you to dress for once."))],
    "Lean back so the row behind can see.",
    by_clothes(
        [P("You lean back in your chair and stretch, slowly, arms over your head, so what you're wearing pulls tight across your tits. From the row behind, the guy can see straight down it. He stops highlighting.")],
        [P("You lean back in your chair and stretch, slowly, and your skirt rides up your thighs. The guy in the row behind leans sideways to see more. He stops highlighting.")],
        P("Every time the lecturer turns from the board you sit up straight. He'd write you up for less. Two seats down, a girl watches him watching you, and her mouth gets thinner and thinner.")),
    pools=POOLS["business"]))

# ── Biology (the shy TA; Zoe; the cocky guy) ──
out.append(class_row(
    "college_class_bio", "Attend the Biology lecture", "Biology", "grade_bio", BIO, TA,
    [],
    [P("Biology. The TA runs it, a shy woman in a lab coat who blushes when she has to say reproductive system out loud. The girl beside you whispers through the slides."),
     G(cond(flag("zoe_met", False)), WHO("Quad after? I'm always there. Tuesdays, Thursdays, Fridays.")),
     G(cond(flag("zoe_met")), D(Z, "Babe. Look at the TA. She's staring at your legs again.")),
     G(cond(trait("grade_bio", "lt", 40)), D(TA, "If anyone's struggling, my door's open Tuesday to Friday afternoons. Really.")),
     ],
    [G(cond(flag("zoe_met")), D(Z, "Party Friday. I'm not asking."))],
    "Let the TA see.",
    by_clothes(
        [P("You sit up straight in the second row with your shoulders back, and don't fold your arms. Your tits show through what you're wearing. The TA sees. She drops her pen, picks it up, drops it again.")],
        [P("You sit with your knees apart in the second row and don't fix your skirt. The TA can see right up it. She drops her pen, picks it up, drops it again.")],
        P("She spends the rest of the class looking very hard at her slides, her neck pink all the way down to her collar. Twice she opens her mouth to say something about it, and doesn't.")),
    pools=POOLS["bio"]))

# ── Figure drawing (the model, nude; the art lecturer; Zoe; the cocky guy) — the pose beat every class ──
POSE = ("The model drops her robe on the platform and steps up naked under the lamp. She sits on the stool and turns her shoulder to the room. Her tits are heavy. They sway when she settles. Her nipples are dark and tight in the cold air. Your charcoal follows the curve of her ass where it spreads on the stool. You draw her thighs, pressed together, and the soft crease between them. You can't stop looking. Your face burns. Your own nipples go hard. The lecturer walks the rows behind you. \"Look at the weight of her,\" she says. \"Draw that.\"")
POSE_END = "You keep drawing the heavy swing of the model's tits, but it's your nipples that ache."
fig = class_row(
    "college_class_figure", "Attend Figure drawing", "Figure drawing", "grade_art", FIG, ART,
    [],
    [P(POSE),
     G(cond(flag("zoe_met")), P("Zoe kicks your ankle under the easel.")),
     G(cond(flag("zoe_met", False)), P("The girl at the next easel kicks your ankle and grins.")),
     P(POSE_END),
     VID("a nude female life model posing on a stool under a lamp in an art class, students drawing at easels", "nude model posing art class students drawing", "life drawing class naked model on stool", pool_dir="sex/figure_class_pose_t4"),
     G(cond(flag("cocky_guy_met")), P("At the next easel, the cocky guy isn't drawing the model. He's drawing you.")),
     ],
    [D(ART, "Better. Look at what's actually there, not what you think is there.")],
    "Lean into your easel and let him look.",   # reader a3 #25-26 (DECISIONS 131): one watcher, as the screen says
    by_clothes(
        [P("You lean into your easel, slow, and your tits hang heavy against what you're wearing, your nipples showing through it. The guy at the next easel gives up on the model completely.")],
        [P("You lean into your easel, slow, and your skirt rides up the backs of your thighs. The guy behind you gives up on the model completely.")],
        P("The lecturer stops behind you, looks at your drawing, looks at you."),
        D(ART, "Clothes stay on in my class, @player. Unless you're on the platform.")),
    pools=POOLS["figure"], chat_beside=[])
# reader a3 #25-26 (DECISIONS 131): the risky screen's title names one watcher here too
next(n for n in fig["nodes"] if n["id"] == "risky")["name"] = "Let him look"
out.append(fig)

# ── first classes: meeting the staff (LIVES §6: the lecturers at their first class) ──
def first_class(cid, name, sch, met, people_flags, blocks):
    return {"id": cid, "name": name, "description": f"Meets the {name.lower()} people at the first class. Sets {met}.",
            "trigger": {"location": "lecture_hall", "is_repeatable": False, "priority": 8, "is_active": True,
                        "schedules": at_start(sch), "conditions": cond(flag("opening_done"), flag(met, False))},
            "nodes": [node("first", name, blocks, [go("Find a seat.", loc="lecture_hall", mins=2, flags=[fset(met)] + [fset(f) for f in people_flags])])]}

out.append(first_class("meet_business", "Your first Business class", BUSI, "business_lecturer_met", ["study_guy_met", "rival_met"], [
    P("Business is a grey room with a grey man at the front of it: the Business lecturer, fifty, a suit with no creases, a register in his hand he actually calls."),
    D(BUS, "I don't do extensions. I don't do excuses. I do honest work, and I grade it honestly. Sit down."),
    P("The guy in the row behind you, the one with three highlighters, leans forward."),
    D(STUDY, "You can borrow my notes. Any time. If you, um. If you want."),
    G(cond(flag("rival_met")), P("And the sharp girl from Psychology watches you sit and doesn't smile."), D(RIVAL, "Oh. You're in this one too.")),
    G(cond(flag("rival_met", False)), P("A sharp girl in the front row watches you sit and doesn't smile."), WHO("New? Don't take my seat.")),
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
    P("You take an easel halfway round the horseshoe."),
]))
_mf = out[-1]
_mf["nodes"][0]["choices"] = [go("Set up your easel.", node="easel", mins=2)]
_mf["nodes"].append(node("easel", "The next easel", [
    G(cond(flag("jake_met")), P("The guy at the next easel is in a team jacket: Jake's teammate, the cocky one. He looks you over, slow, and grins.")),
    G(cond(flag("jake_met", False)), P("The guy at the next easel is in a team jacket, the cocky kind. He looks you over, slow, and grins.")),
    D(COCKY, "This is going to be a good class."),
], [go("Find your charcoal.", loc="lecture_hall", mins=2,
       flags=[fset("art_lecturer_met"), fset("cocky_guy_met"), fset("figure_model_met")])]))
# The first class runs straight into the lecture (LO, 2026-11-01: "Biology just shows the lecture, nowhere to
# attend"). The meeting screen used to end back in the hall, so the first class read as over. Its last button now
# opens the class's own seat (Focus, Chat, Doze, Skip, the risky slot), copied from the class canvas. The opening
# lines are left out because the meeting has just said them (Figure drawing keeps its pose, which is the class);
# the tired and eyes lines stay.
import copy
CLASS_OF = {c["id"]: c for c in out if c["id"].startswith("college_class_")}
def into_class(meet, class_id, exit_text, keep_opening=False):
    cls = CLASS_OF[class_id]
    seat = copy.deepcopy(cls["nodes"])
    if not keep_opening:
        seat[0]["blocks"] = seat[0]["blocks"][-2:]      # the tired line and the eyes line (class_row's last two)
    seat[0]["name"] = cls["nodes"][0]["name"]
    last = [n for n in meet["nodes"] if any(c.get("locationId") == "lecture_hall" for c in n["choices"])][-1]
    flags = [f for c in last["choices"] for f in c.get("flagEffects", [])]
    last["choices"] = [go(exit_text, node="class", mins=2, flags=flags)]
    meet["nodes"] += seat
MEETS = {c["id"]: c for c in out if c["id"] in ("meet_business", "meet_bio", "meet_figure")}
into_class(MEETS["meet_business"], "college_class_business", "Find a seat.")
into_class(MEETS["meet_bio"], "college_class_bio", "Find a seat.")
into_class(MEETS["meet_figure"], "college_class_figure", "Find your charcoal.", keep_opening=True)   # the pose is the class
# ── the guy beside her (college_event_desk_guy; Psychology and Business; once a day) ──
DESK_HAND = ("You check the room first. The lecturer faces the board. The row in front has its heads down. The desk hides everything below your elbows, so you slide your hand under it and open his jeans. His cock springs into your fingers, hot and thick, slick at the tip. You stroke his cock slow, root to head. He grips the desk edge and breathes through his nose so he won't make a sound. Your face burns, but you go faster. His cock throbs in your fist and his balls pull tight. He comes over your knuckles, under the desk where nobody sees. You wipe your palm on his thigh while his cock twitches against his open jeans.")
out.append({
    "id": "college_event_desk_guy", "name": "The guy beside you",
    "description": "College event in Psychology and Business: the guy beside her is hard. Curious: she looks. Bold: her hand, unseen under the desk (explicit). Once a day.",
    "trigger": {"location": "lecture_hall", "is_repeatable": True, "priority": 4, "is_active": True, "max_triggers_per_day": 1,
                "schedules": at_start(PSYCH + BUSI), "conditions": cond(flag("desk_guy_met"), trait("corruption", "gte", 20))},
    "nodes": [
        node("ask", "Beside you", [
            P("The guy who sits beside you has his jacket across his lap and his jaw clenched. He catches you looking and leans in."),
            D(DESK, "I'm hard. Help me out."),
            T("He said it like he was asking for a pen."),
        ], [
            go("Look.", node="watch", mins=3),
            go("Help him.", node="hand", mins=3, cond_=cond(trait("corruption", "gte", 60))),   # a handjob in a full hall: Hungry (DECISIONS 124)
            go("\"Not here.\"", node="no", mins=1),
        ]),
        node("watch", "Look", [
            P("A girl two seats down has stopped writing and is watching the two of you."),
            P("You look. He moves the jacket an inch so you can see the shape of it straining his jeans, and watches you look, and grins at the board like nothing's happening."),
            P("Your thighs press together under the desk."),   # reader a3 #27 (DECISIONS 131): her body on the Look screen
            D(DESK, "Next time, then."),
        ], [go("Back to the class.", loc="lecture_hall", mins=90)]),
        node("hand", "Under the desk", [
            P(DESK_HAND),
            VID("under a lecture desk a girl's hand in a guy's open jeans, the class facing the front", "handjob under desk in class", "girl hand in guy jeans under lecture desk", pool_dir="sex/desk_guy_hand_t5"),
        ], [go("Wipe your hand.", loc="lecture_hall", mins=90,
               eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 79}])]),
        node("no", "Not here", [D(DESK, "Worth a try."), P("Two seats down a girl smirks into her notes."), P("He shrugs and puts his jacket straight and copies the slide like a model student. He keeps glancing at your hands for the rest of the class.")],
             [go("Back to the class.", loc="lecture_hall", mins=90, flags=[fset("desk_guy_refused")])]),
    ]})

# ── the dress-code warning (wardrobe pool, in class; once a day). Twice is a complaint ──
# It fires as the class starts (a class fills its window), and the lecturer is whoever teaches that slot.
def slot_cond(rows):
    return [cond(wd(*w), tod(a, b)) for w, a, b in rows]
WARN_BY = [(H, PSYCH, "Dr. Hale"), (BUS, BUSI, "The Business lecturer"), (TA, BIO, "The TA")]
warn_blocks = [P("Before the class starts, the lecturer calls you down to the front, quiet, while the room fills up.")]
HERE = lambda npc: {"type": "npc_at_location", "location_id": "lecture_hall", "npc_id": npc, "operator": "is_present"}
AWAY = lambda npc: {"type": "npc_at_location", "location_id": "lecture_hall", "npc_id": npc, "operator": "is_absent"}
for npc, rows, who in WARN_BY:
    warn_blocks.append(G(cond(HERE(npc)), D(npc, "This is a lecture hall, not a nightclub. Think about how you come to class.")))
warn_blocks.append(G(cond(AWAY(H), AWAY(BUS), AWAY(TA)),
                     WHO("This is a lecture hall, not a nightclub. Think about how you come to class.")))
warn_blocks += [
    G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}), P("Their eyes go to your chest, where everybody's eyes are going to be all class, and away.")),
    # reader a3 #28 (DECISIONS 131): her body, not the garment
    G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), P("Their eyes go to your bare thighs below the skirt, and away.")),
]
for r in PSYCH + BUSI:
    warn_blocks.append(G(cond(flag("dress_warned"), flag("rival_met"), wd(*r["weekdays"]), tod(r["start_time"], r["end_time"])),
                         P("On your way back to your seat, the rival girl leans out into the aisle with a little smile."),
                         D(RIVAL, "I told the dean's office. Somebody had to.")))
out.append({
    "id": "college_event_dress_code", "name": "A word about what you're wearing",
    "description": "Wardrobe event in class: the slot's lecturer warns her about what she wears (no bra, a short skirt), as the class starts. The first sets dress_warned; after that, a complaint (complaints +1); the rival says so in her own classes. Exhibitionism +1, once a day.",
    "trigger": {"location": "lecture_hall", "is_repeatable": True, "priority": 4, "is_active": True, "max_triggers_per_day": 1,
                "schedules": at_start(PSYCH + BUSI + BIO), "conditions": DARING_STATE},
    "nodes": [node("warning", "Before class", warn_blocks, [
        # (DECISIONS 124, H5) the warning happens to her: it pays her nothing
        go("\"Yes. Sorry.\"", loc="lecture_hall", mins=5, cond_=cond(flag("dress_warned", False)), flags=[fset("dress_warned")]),
        go("\"Yes. Sorry.\"", loc="lecture_hall", mins=5, cond_=cond(flag("dress_warned")),
           eff=[add("complaints", 1, clamp=False)]),
    ])]})

# ── the midterms (college_exam): weeks 7-8, once per exam, in that subject's slot ──
# reader a3 #24 (DECISIONS 131, call A): a no costs him Want +1. The cocky guy has no core traits in
# people_data.py (core={}), and a pay to a trait he doesn't declare is a made-up stat (call B), so the pay
# switches on by itself once people_data.py gives him a "want" (that file is the lead's to change).
from people_data import PEOPLE as _PEOPLE
COCKY_NO_PAY = []   # C1 (LO 2026-11-03, reverses DECISIONS 131 call A): her no never raises his Want
FLASH = ("The proctor sits at the front, reading. Every head in the row is bent over a page. You check the room once. Then you pull everything up under the desk line, where only he can see. Your tits are bare in the cold hall air. Your nipples go hard at once, tight and aching. His pen stops mid-word. His eyes drop to your tits and stay there. One second. Two. Three. You yank everything down and cover your breasts. He slides his paper to the edge of his desk. Your nipples are still hard, and his stare is still on your chest.")
WEEKS_7_8 = [{"type": "days_since_flag", "subject": "player", "flag_key": "opening_done", "operator": "gte", "value": 42},
             {"type": "days_since_flag", "subject": "player", "flag_key": "opening_done", "operator": "lt", "value": 56}]
for subj, grade, sch, code in [("Psychology", "grade_psych", PSYCH, "psych"), ("Business", "grade_business", BUSI, "business"),
                               ("Biology", "grade_bio", BIO, "bio"), ("Figure drawing", "grade_art", FIG, "art")]:
    done_f = f"exam_{code}_done"
    out.append({
        "id": f"college_exam_{code}", "name": f"The {subj} midterm",
        "description": f"The {subj} midterm (college_exam), weeks 7-8 in its class slot: Focus (reads intelligence), flirt for the study guy's paper (Curious), or a flash for the cocky guy's (Daring, explicit). Copying +5. Sets {done_f} and midterm_done.",
        "trigger": {"location": "lecture_hall", "is_repeatable": False, "priority": 9, "is_active": True,
                    "schedules": at_start(sch), "conditions": cond(*WEEKS_7_8, flag(done_f, False))},
        "nodes": [
            node("paper", "The midterm", [
                P(f"The {subj} midterm. Desks pulled apart, bags at the front, a proctor reading a paperback by the door. The paper lands face-down in front of you, and the clock on the wall starts."),
                WHO("Phones in your bags. Ninety minutes. Turn your papers over."),   # LO 2026-11-03: the proctor
                G(cond(trait("intelligence", "lt", 10)), T("You know some of this. Not enough of it.")),
                G(cond(trait("intelligence", "gte", 10)), T("You studied. You actually know this.")),
            ], [
                go("Focus. Do it yourself.", node="result", mins=90, cond_=cond(trait("intelligence", "gte", 10)), eff=[add(grade, 6)]),
                go("Focus. Do it yourself.", node="result", mins=90, cond_=cond(trait("intelligence", "lt", 10)), eff=[add(grade, 1)]),
                *([go("Flirt with the study guy for his paper.", node="study", mins=5, cond_=cond(trait("corruption", "gte", 20), flag("study_guy_met")))]
                  if code == "business" else []),
                *([go("Look at the cocky guy.", node="price", mins=5, cond_=cond(trait("exhibitionism", "gte", 20), flag("cocky_guy_met")))] if code == "art" else []),
            ]),
            *([node("study", "The study guy", [
                P("You catch the study guy's eye across the gap and bite your lip and look at his paper and back at him. He goes red to the ears. A minute later his paper is on the corner of his desk, angled your way, and he's staring at the ceiling like a saint."),
            ], [go("Copy.", node="result", mins=85, eff=[add(grade, 5), add("campus_talk", 1, clamp=False)])])] if code == "business" else []),
            *([
            node("price", "His price", [
                G(cond(flag("jake_met")), P("Jake's teammate is at the next desk with his paper finished and his pen behind his ear. He sees you looking at it and leans back in his chair.")),
                G(cond(flag("jake_met", False)), P("The cocky guy from Figure drawing is at the next desk with his paper finished and his pen behind his ear. He sees you looking at it and leans back in his chair.")),
            ], [go("\"What?\"", node="flash_ask", mins=1), go("Look away.", node="result", mins=89, eff=[add(grade, 1)])]),
            node("flash_ask", "Show me", [
                D(COCKY, "Show me and I'll tilt my paper."),
            ], [go("Show him.", node="flash", mins=2, cond_=cond(trait("exhibitionism", "gte", 40))), go("\"No.\"", node="no", mins=1)]),   # a flash with the hall behind it: Showing (DECISIONS 124)
            # reader a3 #24 (DECISIONS 131, call A): her no gets his answer and costs him (his Want +1, when he has one)
            node("no", "Your loss", [
                P("He shrugs and turns his paper face-down, slow, so you watch it go."),
                D(COCKY, "Your loss."),
            ], [go("Back to your own paper.", node="result", mins=87, eff=[add(grade, 1)] + COCKY_NO_PAY)]),
            node("flash", "Three seconds", [
                P(FLASH),
                VID("under a desk in an exam hall a girl lifts her top for the guy at the next desk, rows of students writing", "girl flashes tits during exam under desk", "exam hall flash for answers", file=f"sex/exam_{code}_flash_t4.webm"),
            ], [go("Copy.", node="result", mins=85, eff=[add(grade, 5), {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": CAP_BOLD}],
                   flags=[fset("cocky_exam_deal")])])
            ] if code == "art" else []),
            node("result", "Pens down", [
                P("Pens down. The proctor collects the papers row by row. The results go up on the portal next week, and on the office door."),
                WHO("Stay in your seats till I have every paper."),
                G(cond(trait(grade, "lt", 40)), T("It went badly. Laura is going to see this on the portal.")),
                G(cond(trait(grade, "gte", 40), trait(grade, "lt", 70)), T("It went fine. A pass, probably. Nobody will say anything.")),
                G(cond(trait(grade, "gte", 70)), T("It went well. For once the portal is going to make Laura smile.")),
            ], [go("Leave the hall.", loc="campus", mins=5, flags=[fset(done_f), fset("midterm_done")])]),
        ]})

# ── the lecturers in the lecture hall, before and after class (their class hubs) ──
LEAVE_TO = {"lecture_hall": "campus", "art_office": "faculty_floor", "business_office": "faculty_floor",
            "ta_office": "faculty_floor", "dean_office": "faculty_floor"}


def hub(cid, loc, npc, met, name, blocks, choices=None):
    return {"id": cid, "name": name, "description": f"{name}: one line on her grade, one on her clothes.",
            "trigger": {"location": loc, "npc": npc, "requires_npc": npc, "is_repeatable": True, "priority": 6, "is_active": True,
                        "conditions": cond(flag(met))},
            "nodes": [node("hub", name, blocks, choices or [go("Go.", loc=LEAVE_TO[loc])])]}

def grade_lines(npc, grade, low, mid, top):
    return [G(cond(trait(grade, "lt", 40)), D(npc, low)),
            G(cond(trait(grade, "gte", 40), trait(grade, "lt", 70)), D(npc, mid)),
            G(cond(trait(grade, "gte", 70)), D(npc, top))]

def clothes_line(npc, line):
    return G(DARING_STATE, D(npc, line))

out.append(hub("hub_hale_class", "lecture_hall", H, "hale_met", "Dr. Hale, at the lectern", [
    P("Dr. Hale is at the lectern with his notes, squaring the edges."),
    # S4 (LO 2026-11-03): he's teaching, so this screen is look-only, and it says why
    P("He's mid-lecture. He catches your eye once, then goes back to his slides."),
    *grade_lines(H, "grade_psych", "You're behind, @player. Come and see me on Thursday.", "Good work. Could be better.", "Best paper in the room. Don't let it go to your head."),
    # reader a3 #17 (DECISIONS 131): at grade 40+ a line points at his office. Office hours are Thu 17:00-19:30
    # (his rows); he names it only from his step 2 on, the step where he invites her. This hub fires Mon/Wed/Fri
    # mornings and Thursday 13:00-14:30, so on a Thursday the office is "tonight".
    G(cond(trait("grade_psych", "gte", 40), trait("hale_step", "gte", 2), wd(0, 2, 4)), D(H, "Thursday, @player. My office.")),
    G(cond(trait("grade_psych", "gte", 40), trait("hale_step", "gte", 2), wd(3)), D(H, "Tonight, @player. My office.")),
    G(cond(trait("grade_psych", "gte", 40), trait("hale_step", "lt", 2)), D(H, "See me if you're stuck.")),
    G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), P("His eyes drop to your thighs below your skirt, and he swallows. He steps in tight behind the lectern, so it hides him from the waist down, and squares the notes again.")),
]))
out.append(hub("hub_art_class", "lecture_hall", ART, "art_lecturer_met", "The art lecturer", [
    P("The art lecturer is moving between the easels with a box of charcoal, looking at you the way she looks at the model."),
    # S4 (LO 2026-11-03): she's teaching, so this screen is look-only, and it says why
    P("She's teaching. She holds your eye over an easel for a second, then turns back to the model."),
    *grade_lines(ART, "grade_art", "You're drawing what you expect, not what's there. Look harder.", "Better. Your lines are getting braver.", "You see bodies properly. I'd like to draw you one day."),
    G(cond(BRALESS), P("She looks at your tits the way she looks at the model, slow, measuring the weight, and doesn't pretend she isn't."),
      D(ART, "That's a good line today. I mean the shape under it, not the clothes. Not yet, anyway.")),
    G(cond(*SKIRT_WITH_BRA), P("She looks at your legs, hip to knee, like she's measuring them for paper."),
      D(ART, "That's a good line today. I mean the legs, not the skirt. Not yet, anyway.")),
]))
out.append(hub("hub_business_class", "lecture_hall", BUS, "business_lecturer_met", "The Business lecturer", [
    P("The Business lecturer is writing headings on the board in long straight lines."),
    # S4 (LO 2026-11-03): he's teaching, so the screen is look-only and says why
    P("He's mid-lecture, and he doesn't stop for anyone."),
    *grade_lines(BUS, "grade_business", "Failing. Retakes by appointment.", "Adequate.", "Good. Keep it that way."),
    clothes_line(BUS, "This isn't a beach, @player."),
]))
out.append(hub("hub_ta_class", "lecture_hall", TA, "bio_ta_met", "The Biology TA", [
    P("The TA is sorting a stack of handouts at the front. She turns, sees you, and drops half of them."),
    # S4 (LO 2026-11-03): she's running the class, so the screen is look-only and says why
    P("She's handing out the worksheets, too busy to talk."),
    # reader a3 #19 (DECISIONS 131): the 40+ bands point at her office too (her rows: ta_office Tue-Fri 14:30-18:00)
    *grade_lines(TA, "grade_bio", "You're, um. You're struggling. My door's open. If you want.", "You're doing fine! Really fine. My door's open afternoons.", "Top marks. Wow. Sorry. Top marks. My door's open afternoons."),
    # reader a3 #35 (DECISIONS 131): the act she holds back, not only a compliment
    G(cond(BRALESS), P("Her eyes go to your chest, to the shape of you under the fabric, and jump back up to your face. Her neck goes pink."),
      D(TA, "You look— sorry. Nothing. You look nice."),
      P("Her eyes drop to your chest. She looks back at her clipboard, fast, and doesn't finish what she was saying.")),
    G(cond(*SKIRT_WITH_BRA), P("Her eyes go down your legs to the hem of your skirt and jump back up to your face. Her neck goes pink."),
      D(TA, "You look— sorry. Nothing. You look nice."),
      P("Her eyes drop to your chest. She looks back at her clipboard, fast, and doesn't finish what she was saying.")),
]))

# ── the offices (college_office_talk): art, business (the honest retake), TA, the dean ──
out.append(hub("hub_art_office", "art_office", ART, "art_lecturer_met", "The art lecturer's office", [
    P("Canvases against every wall. The art lecturer looks up from a sketch of a woman's back."),
    *grade_lines(ART, "grade_art", "Sit. Show me your book. Ah. Yes. We have work to do.", "You're improving. Draw every day.", "You have an eye. Come and sit for me some time."),
    G(cond(BRALESS), D(ART, "Stand by the window a moment. The light's good on you."),
      P("She's already looking at your tits under what you're wearing, the way she looks at the model, pencil moving."),
      D(ART, "Clothes on today. Some day you'll sit for me properly.")),
    G(cond(*SKIRT_WITH_BRA), D(ART, "Stand by the window a moment. The light's good on you."),
      P("She's already looking at your bare legs below the skirt, pencil moving."),
      D(ART, "Clothes on today. Some day you'll sit for me properly.")),
]))
# S4 (LO 2026-11-03): she isn't busy in her office, so one choice aimed at her. An hour, Figure drawing +1, cap 69.
_ao = out[-1]
_ao["nodes"][0]["choices"] = [go("Show her your sketchbook.", node="book", mins=0), go("Go.", loc=LEAVE_TO["art_office"])]
_ao["nodes"].append(node("book", "Your sketchbook", [
    P("She turns the pages slowly, and stops on the figures. She takes a pencil and corrects a hip with three lines, without asking."),
    D(ART, "There. You keep drawing what you think a body does. Draw what it's doing."),
], [go("Thank her.", loc=LEAVE_TO["art_office"], mins=60, eff=[{"targetType": "player", "trait": "grade_art", "op": "add", "value": 1, "cap": 69}])]))
out.append(hub("hub_business_office", "business_office", BUS, "business_lecturer_met", "The Business lecturer's office", [
    P("The Business lecturer looks up from his marking and doesn't smile."),
    *grade_lines(BUS, "grade_business", "Failing. I can offer an honest retake. Nothing else.", "You're passing. Keep it honest.", "Good work. That's all."),
    clothes_line(BUS, "You can wear what you like. It won't change your grade. Nothing does."),
], [
    go("\"I'll take the retake.\"", node="retake", mins=5, cond_=cond(trait("grade_business", "lt", 40), flag("business_retake_used", False)),
       flags=[fset("business_retake_used")]),
    go("Go.", loc="faculty_floor"),
]))
out[-1]["nodes"].append(node("retake", "The retake", [
    P("He hands you a paper and points at a chair, and sits watching you for an hour without blinking. You know more than you thought."),
    D(BUS, "Honest work. Thank you."),
], [go("Hand it in.", loc="faculty_floor", mins=60, eff=[add("grade_business", 5)])]))
out.append(hub("hub_ta_office", "ta_office", TA, "bio_ta_met", "The TA's office", [
    P("The TA's office is half a room with a skeleton in the corner wearing a party hat. She jumps when you knock."),
    *grade_lines(TA, "grade_bio", "Oh! Hi. Your grade. Um. We should fix your grade. Sit?", "You're doing well. Do you want tea?", "You're my best student. Don't tell anyone I said that."),
    G(cond(BRALESS), P("She can't keep her eyes off your chest."),
      D(TA, "I like your— never mind. Sit down. Please."),
      P("She gets up to shut the door, stops with her hand on it, and leaves it open.")),
    G(cond(*SKIRT_WITH_BRA), P("Her eyes go down your legs when you sit, and stay."),
      D(TA, "I like your— never mind. Sit down. Please."),
      P("She gets up to shut the door, stops with her hand on it, and leaves it open.")),
]))
# S4 (LO 2026-11-03): a person who isn't busy gets one choice aimed at them. An hour of her help, Biology +1,
# capped at 69 so the top band is still earned in class.
_ta = out[-1]
_ta["nodes"][0]["choices"] = [go("Ask her to help you with Biology.", node="help", mins=0), go("Go.", loc=LEAVE_TO["ta_office"])]
_ta["nodes"].append(node("help", "Her help", [
    P("She pulls her chair round to your side of the desk and goes through your last lab with a pencil, too close, apologising every time her knee touches yours."),
    D(TA, "See? You had it. You just didn't believe it."),
], [go("Thank her.", loc=LEAVE_TO["ta_office"], mins=60, eff=[{"targetType": "player", "trait": "grade_bio", "op": "add", "value": 1, "cap": 69}])]))
# (2026-11-01) met on day 1 now
# (college_dean_office), so the warning line shows only after the warning call (dean_summons).
out.append(hub("hub_dean_office", "dean_office", DEAN, "dean_met", "The dean", [
    P("The dean doesn't get up. He waits for you to sit in the hard chair before he looks at you."),
    G(cond(flag("on_probation")), D(DEAN, "You're on probation. Every grade, every complaint, crosses my desk now.")),
    G(cond(flag("on_probation", False), flag("dean_summons")), D(DEAN, "You've had your warning. Don't make me write another letter.")),
    G(cond(flag("dean_summons", False)), D(DEAN, "Your timetable isn't decoration, @player. Use it.")),
    G(DARING_STATE, D(DEAN, "Is that what you wear to college?")),
]))
# S4 (LO 2026-11-03): one choice aimed at the dean. A talk, no counter: his answer reads her grades.
ANY_FAILING = cond(*[trait(g, "lt", 40) for g in ("grade_psych", "grade_business", "grade_bio", "grade_art")], logic="OR")
_dean = out[-1]
_dean["nodes"][0]["choices"] = [go("Ask about your grades.", node="grades", mins=0), go("Go.", loc=LEAVE_TO["dean_office"])]
_dean["nodes"].append(node("grades", "Your grades", [
    P("He turns his screen so you can see it, and reads your grades off it without looking at you."),
    # adjacent groups render as one if/elseif chain (canv.G's docstring), so exactly one answer shows
    GC(cond(flag("on_probation")), D(DEAN, "Every one of these goes up, or you go home. That's what probation means.")),
    GC(ANY_FAILING, D(DEAN, "Some of these worry me. Fix them before I have to.")),
    GC(cond(flag("on_probation", False)), D(DEAN, "Fine. Keep them there.")),
], [go("Go.", loc=LEAVE_TO["dean_office"], mins=10)]))

# ── day 1, the dean's office (college_dean_office.md, signed 2026-11-01, DECISIONS 121): straight from the
#    opening's "Go to campus."; four screens; the timetable; "Go to Psychology." Time: the opening ends about
#    07:50, the walk is 15, so "You're already late" is said at about 08:35 (Psychology starts 08:30). ──
TIMETABLE_LINK = '<<link "Your timetable">><<run setup.openTimetable()>><</link>>'
out.append({
    "id": "college_dean_office", "name": "The dean's office",
    "description": "Day 1, Monday of week one, from the opening: the dean's look, his rules, the timetable, and \"Go to Psychology.\" Sets dean_met.",
    # Not bound to his face: his rows start at dean_met, which this scene sets (the meeting itself).
    "trigger": {"location": "dean_office", "is_repeatable": False, "priority": 10, "is_active": True,
                "schedules": [{"weekdays": [0], "start_time": "08:00", "end_time": "09:00"}],
                "conditions": cond(flag("opening_done"), flag("dean_met", False))},
    "nodes": [
        node("wait", "The dean's office", [
            P("The dean's office smells of carpet and old coffee. He's writing. He doesn't look up, and he doesn't ask you to sit, so you stand."),
            P("When he does look up, he takes his time. Your face, then down, then back up, slowly, like he's reading a form."),
            G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), D(DEAN, "Is that what you wore to class?")),
            G(cond({"type": "worn_type", "operator": "neq", "value": "short_skirt"}), D(DEAN, "You're the new one. @player.")),
        ], [go("\"Good morning.\"", node="rules", mins=20, flags=[fset("dean_met")])]),
        node("rules", "The rules", [
            D(DEAN, "Classes are not optional. Your grades come to me. Complaints come to me."),
            P("He taps a folder with one finger."),
            D(DEAN, "Two complaints and you're back in this office. I don't like seeing a student twice."),
        ], [go("\"I understand.\"", node="timetable", mins=5)]),
        node("timetable", "Your timetable", [
            P("He slides a printed sheet across the desk and keeps two fingers on it a second before he lets go."),
            D(DEAN, "Your timetable. Learn it."),
            P(TIMETABLE_LINK),
        ], [go("Fold it into your bag.", node="late", mins=5)]),
        node("late", "Already late", [
            P("He's already looking back at his writing."),
            D(DEAN, "Psychology. Lecture hall. You're already late."),
        ], [go("Go to Psychology.", loc="lecture_hall", mins=15)]),
    ]})

# ── the dean's warning: the call itself (8_phone.toml). It never says where she is and never moves her:
# both answers return her to where she was; the office opens on her map (dean_summons). ──
out.append({
    "id": "dean_warning", "name": "The dean's office",
    "description": "Her first trouble: the dean's warning, by phone. Meets the dean; sets dean_met, dean_summons, on_probation (if failing) and letter_home (laura_suspicion +10). Played by answering the dean's office's call; returns her to where she was.",
    "trigger": {"location": "dean_office", "is_repeatable": False, "priority": 1, "is_active": True, "substitution_only": True},
    "nodes": [node("warning", "The warning", [
        P("The dean's secretary puts you straight through. A dry voice, a man used to being listened to."),
        D(DEAN, "This is the dean. @player, I have your file open in front of me."),
        G(cond(trait("complaints", "gte", 2)), D(DEAN, "Complaints about your conduct in class. Your clothes. This is a college, not a stage.")),
        G(cond(flag("failing_noticed")), D(DEAN, "And your grades. You're failing. I'm putting you on probation.")),
        D(DEAN, "Your parents will be getting a letter. Consider this your warning. My door is on the faculty floor, if you want to argue."),
        T("A letter home. Laura is going to read every word of it."),
    ], [
        go("\"Yes, sir.\"", ret=True, mins=10, cond_=cond(flag("failing_noticed")),
           flags=[fset("dean_met"), fset("dean_summons"), fset("on_probation"), fset("letter_home")], eff=[add("laura_suspicion", 10, clamp=True)]),
        go("\"Yes, sir.\"", ret=True, mins=10, cond_=cond(flag("failing_noticed", False)),
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

# ── the gym (campus_gym.md): work out, alone. Jake's training is his hub (jake.py). Once a day:
# `worked_out` cleared at midnight (the home brakes' rule, DECISIONS 77). A sports bra with nothing over
# it is Daring (the gym sheet), and that is when the mirror wall pays.
SPORTS_ONLY = [{"type": "clothing_item", "item_id": "sports_bra", "operator": "equipped"},
               {"type": "clothing_slot", "slot": "top", "operator": "unequipped"},
               {"type": "clothing_slot", "slot": "dress", "operator": "unequipped"}]
out.append({
    "id": "gym_workout", "name": "Work out",
    "description": "The gym: 60 min, energy -15; in just a sports bra at Daring, exhibitionism +1 (campus_gym.md). Once a day.",
    "trigger": {"location": "campus_gym", "is_repeatable": True, "priority": 4, "is_active": True,
                "conditions": cond(flag("worked_out", False))},
    "nodes": [node("floor", "The gym floor", [
        P("Treadmill, then the weights, then the mats. The mirror wall shows you everything you're doing, and everyone else doing it too."),
        WHO("You using that bench, or can I jump in?"),   # LO 2026-11-03: someone on the gym floor
        G(cond(*SPORTS_ONLY), P("Just the sports bra and your bottoms. Your tits bounce in it with every stride on the treadmill, and in the mirror wall you can see two guys at the rack stop counting their reps. One looks away when you catch his eye. The other doesn't, and he doesn't come over either. Not yet.")),
        G(cond({"type": "clothing_item", "item_id": "jeans", "operator": "equipped"}), P("You're working out in jeans. It's stupid, and you feel it in every squat.")),
    ], [
        go("Work out an hour.", loc="campus_gym", mins=60, costs=[{"trait": "energy", "value": 15}],
           eff=[add("energy", -15)], flags=[fset("worked_out")], cond_=cond(flag("worked_out", False))),
        go("Work out an hour, and let them look.", loc="campus_gym", mins=60, costs=[{"trait": "energy", "value": 15}],
           eff=[add("energy", -15), {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": CAP_BOLD}],
           flags=[fset("worked_out")], cond_=cond(flag("worked_out", False), trait("exhibitionism", "gte", 20), *SPORTS_ONLY)),
        go("Not today.", loc="campus"),
    ])]})

out.append({
    "id": "lecture_timetable", "name": "Read the timetable on the door",
    "description": "The timetable: when each class is. Writes nothing.",
    "trigger": {"location": "lecture_hall", "is_repeatable": True, "priority": 1, "is_active": True},
    "nodes": [node("timetable", "The timetable", [
        P("The timetable is taped to the door. Somebody has drawn a penis on Thursday, but nobody has rubbed it off."),
        P(TIMETABLE_LINK),
    ], [go("Done.", loc="lecture_hall")])]})

# ═════════════ THE BACK STACKS (library_back_stacks.md, DECISIONS 79) ═════════════
# A Good Girl way up: the couple is an event and pays nothing; "Stay behind the shelf." is her
# choice and pays corruption +1, cap 19. Nobody sees her. Once a day; it opens until 19:45 so
# its 15 minutes of exits land before the library closes at 20:00.
STACKS_SEEN = ("The back aisles are dead quiet. You run a finger along the spines, hunting a call number. Then you hear it. A soft knock of books on wood, steady, over and over. A muffled sound under it. You turn the corner. Two seniors fill the dead end of the stacks. She is up on the edge of a low shelf, skirt shoved to her waist, legs locked round him. Her top is pushed up and her tits bounce with every thrust. His jeans hang open. You see his cock slide out of her, wet, and drive back in. His hand is clamped over her mouth. She moans into his palm anyway. Your face goes hot. You stop dead at the end of the aisle. Her nipples are hard. He thrusts again, and the books knock.")
STACKS_STAY = ("You step back behind the next shelf. Three books are missing at eye height. His cock slides out of her, wet and shining, then thrusts back in. Her tits bounce with every push. Her nipples are dark and hard. His hand stays clamped over her mouth. She moans into his palm anyway. Her heels dig into his ass and pull him deeper. That is a real cock, inside a real woman, four feet from you. You should look away. You don't. Your own nipples go tight. You are wet, and you press your thighs together hard. Your hands stay flat on the shelf. She shudders and comes against his palm, hips jerking. Two aisles over, a book trolley squeaks. You slip away with your book, nipples still tight, thighs clenched.")
out.append({
    "id": "library_back_stacks", "name": "Find a book in the back stacks",
    "description": "Two seniors (22) in the back stacks: the look pays nothing; staying behind the shelf pays corruption +1, cap 19 (DECISIONS 78-79). Once a day.",
    "trigger": {"location": "library", "is_repeatable": True, "priority": 4, "is_active": True, "max_triggers_per_day": 1,
                "schedules": sched(([0, 1, 2, 3, 4], "08:00", "19:45")), "conditions": cond(flag("opening_done"))},
    "nodes": [
        node("stacks", "The back stacks", [P(STACKS_SEEN),
            WHO("Shh. Quiet. Take my cock and keep quiet."),   # LO 2026-11-03: the senior, in her ear (the park's ceiling: no fuck)
            VID("a couple having sex against a bookshelf at the end of a library aisle, his hand over her mouth", "couple fucking in library stacks", "quiet library sex against bookshelf", pool_dir="sex/library_stacks_seen_t5")],
            [go("Stay behind the shelf.", node="stay", mins=5, flags=[fset("saw_the_library_couple")]),
             go("Take the book and go.", loc="library", mins=5, flags=[fset("saw_the_library_couple")])]),
        node("stay", "Behind the shelf", [WHO("You're so wet. Not a sound, or they'll hear."), P(STACKS_STAY),
            VID("seen through a gap in library books, a couple having sex against the shelves", "voyeur watching couple in library", "peeking through bookshelf at couple sex", pool_dir="sex/library_stacks_stay_t5")],
            [go("Back to your desk.", loc="library", mins=10, eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 19}], flags=[fset("saw_the_library_couple")]),
             # C1 (DECISIONS 147): Corruption 5; still hidden, still stage 1. The button pays +1, its screen's exit +1, cap 19
             go("Move one aisle closer.", node="closer", mins=5, swl=True, cond_=cond(trait("corruption", "gte", 5)),
                eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 19}], flags=[fset("saw_the_library_couple")])]),
        node("closer", "One aisle closer", [
            P("You slide along to the next aisle, the one that backs right onto theirs. The gap between the books is a hand's width. They are close enough to touch."),
            P("You can see the wet shine on his cock every time he pulls out of her. You can hear it. Her tits bounce in his face, and he bites one, and she jerks against his hand and moans into it."),
            P("You hold your breath. If either of them turns their head, they're looking straight at you. Your nipples ache, and you are soaked."),
            WHO("God, you're tight. Don't make a sound."),
            VID("through a gap in library books, very close, a couple having sex against the shelves", "close up voyeur library sex through books", "peeking through bookshelf gap couple close", pool_dir="sex/library_stacks_closer_t5")],
            [go("Back to your desk.", loc="library", mins=10, eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 19}], flags=[fset("saw_the_library_couple")])]),
    ]})

# ── the cocky guy at the next easel (false lines a3 #17-19, DECISIONS 129): his Figure drawing rows need a face ──
out.append({
    "id": "hub_cocky_class", "name": "The next easel",
    "description": "The cocky guy in Figure drawing (his class rows, v2_state.json): a look and a line.",
    "trigger": {"location": "lecture_hall", "npc": COCKY, "requires_npc": COCKY, "is_repeatable": True, "priority": 6,
                "is_active": True, "conditions": cond(flag("cocky_guy_met"))},
    "nodes": [node("easel", "The next easel", [
        P("The cocky guy is at his easel in the horseshoe. He's looking at you, not the model."),
        POOL(D(COCKY, "You're better than the model, you know."),
             D(COCKY, "Sit closer next class. I draw better up close."), pid="cocky_class_lines"),
        # reader a3 #42 (DECISIONS 131): his price on a fixed line, until the Figure drawing midterm is behind her
        P("His eyes go down your tits and back up to your mouth, slow, and his pencil keeps moving."),   # reader a3 verify: her body in any outfit
        G(cond(flag("exam_art_done", False)), D(COCKY, "Midterm answers cost a look.")),
        G(cond(flag("exam_art_done")), D(COCKY, "Anything you want from me costs a look. You know that now.")),
        # reader a3 #42 (DECISIONS 131): her body, not only the hem
        G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), P("His eyes go down your thighs to your hem and stay there while his pencil keeps moving.")),
    ], [go("Talk with him a while.", node="talk", mins=0), go("Go.", loc="campus")]),
    # reader a3, seen by the readers (DECISIONS 131): "Talk a while." showed no talk. A talk screen, his lines in a
    # shuffle bag (call B: a second and third pool line, no counter). Every entry a group on the trigger's own
    # condition, so the pool is one type (home_items.py's rule).
    node("talk", "At the next easel", [
        POOL(
            GC(cond(flag("cocky_guy_met")), D(COCKY, "You draw like you're scared of the paper. Push harder."),
               P("He reaches over and drags your charcoal down the page in one thick black line. His arm stays pressed against yours after."),
               D(COCKY, "Like that.")),
            GC(cond(flag("cocky_guy_met")), D(COCKY, "Hold still. I'm drawing your mouth."),
               P("He turns his pad round so you can see. It's your mouth, three times over, and in every one it's open."),
               D(COCKY, "That's how I'd keep it.")),
            GC(cond(flag("cocky_guy_met")), D(COCKY, "The lecturer hates me. She still gives me top marks. Want to know why?"),
               ME("Why?"),
               D(COCKY, "I look properly. Same as I'm looking at you.")),
            pid="cocky_class_talk", bag=True),
    ], [go("Back to your easel.", loc="lecture_hall", mins=20)])]})

# heat proposal B10 (the gym), B16 (the lecture hall) and B20 (the office doors' hub lines), DECISIONS 147 chunk 3
import walkins_out
_done = walkins_out.attach(out)
assert _done == {"gym_workout", "lecture_timetable"}, _done
walkins_out.hub_read(out)

text = "# ── college (sheets/systems/college.md · scenes college_*.md) ──\n" + "".join(emit(c) for c in out)
open(__import__("sys").argv[1], "w").write(text)
print("college:", len(out), "canvases")
