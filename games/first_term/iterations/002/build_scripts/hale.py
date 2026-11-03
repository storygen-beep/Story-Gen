"""Dr. Hale — steps 1-5 (Hale B 1-5), Thursdays at seven (the repeat), his office hub; Nadia's hubs.
Source: sheets/scenes/hale_0*.md, people/npc_hale.md, people/npc_nadia.md. Explicit screens pasted as signed."""
from canv import *
from tomlw import tod, wd

H = "npc_hale"
N = "npc_nadia"
CL = "npc_claire"

def at_class_start(t):
    """Iteration 002, part 8 (reader): a step that opens the lecture fires in its first quarter-hour,
    08:30-08:45, not at 09:59. The ledger's window stays 08:30-10:00 (the lead's to change)."""
    t["conditions"]["items"].append(tod("08:30", "08:45"))
    return t

out = []

def done(n):
    return fset(f"hale_0{n}_done")

SKIRT = {"type": "worn_type", "operator": "eq", "value": "short_skirt"}
NOT_SKIRT = {"type": "worn_type", "operator": "neq", "value": "short_skirt"}
PANTIES_OFF = [{"action": "unequip", "item_id": "plain_panties"}]
IN_DRESS = {"type": "clothing_slot", "slot": "dress", "operator": "equipped"}
NO_DRESS = {"type": "clothing_slot", "slot": "dress", "operator": "unequipped"}
# The sheer blouse is the one top with buttons (hale_04 sheet, sweep A4-22).
BLOUSE = {"type": "clothing_item", "item_id": "thin_top", "operator": "equipped"}
NO_BLOUSE = {"type": "clothing_item", "item_id": "thin_top", "operator": "unequipped"}

HAND = ("You sit on the corner of his desk and undo the buttons yourself, one at a time, slowly. There is nothing under them. Your tits come free, bare to him, your nipples already tight. Dr. Hale stares. He wants to touch you, but he can't stop looking first. \"@player,\" he says. His voice cracks on it. Then his hand slides inside, and his palm closes over your tit. It covers you completely, warm and heavy. His thumb finds your nipple and rolls it, slow, then harder. You arch into his hand. His breath goes ragged against your neck. His cock is hard, pressing against the edge of the desk an inch from your hip. Your nipple is stiff under his thumb, so he rolls it again until you gasp.")

# ── step 1 · the first lecture, reworked: his first move (hale_01_first_lecture.md, signed 2026-11-01). Week one: she
#    walks in late from the dean (college.md), so the step's window is the whole lecture, not its first quarter-hour. ──
FIRST_DAY = {"type": "hours_since_flag", "subject": "player", "flag_key": "opening_done", "operator": "lt", "value": 12}
LATER_DAY = {"type": "hours_since_flag", "subject": "player", "flag_key": "opening_done", "operator": "gte", "value": 12}
# false lines a3, reader follow-up: "Sit through the lecture." takes 60 minutes and the screen after it says the room
# packs up, so the step opens only while that hour still ends by 10:00 (a late arrival waits for the next Psychology class)
_t1 = step_trigger(H, 1)
for _s in _t1["schedules"]:
    _s["end_time"] = "08:55"
out.append({
    "id": "hale_01_first_lecture", "name": "Your first lecture",
    "description": "Hale step 1 (release 1): she walks in late; \"Front row, where I can see you.\"; his pen at her feet, and he waits. Meets Hale, Nadia, the guy beside her and the rival girl.",
    "trigger": _t1,
    "nodes": [
        node("late", "Late", [
            IMG("scenes/hale_01_lecture.jpg", "a lecture hall, a male professor in his late thirties at a lectern, students in raked seats, a girl in the front row",
                "professor at lectern lecture hall students", "college lecture hall front row professor"),
            # false lines a3 #20 (DECISIONS 129): a Psychology class can meet Hale and Nadia first
            G(cond(flag("hale_met", False)), P("The lecture hall door is heavy and it bangs behind you. Two hundred heads turn. At the lectern a man in a tweed jacket stops in the middle of a sentence and looks at you, and lets the silence go on.")),
            G(cond(flag("hale_met")), P("The lecture hall door is heavy and it bangs behind you. Two hundred heads turn. At the lectern Dr. Hale stops in the middle of a sentence and looks at you, and lets the silence go on.")),
            G(cond(FIRST_DAY), D(H, "Late, on the first day.")),
            G(cond(LATER_DAY), D(H, "Late.")),
            P("He points with his pen at the front row."),
            D(H, "Front row. Where I can see you."),
        ], [go("\"Sorry.\"", node="front_row", mins=2, flags=[fset("hale_met")])]),
        node("front_row", "The front row", [
            G(cond(flag("nadia_met", False)), P("The only free seat in the front row is beside a girl with big glasses and a cardigan, who moves her bag off it for you."),
              WHO("Sit here. I'm Nadia. Nobody sits at the front for him. You'll see why.")),
            G(cond(flag("nadia_met")), P("Nadia waves you over to the free seat beside her in the front row and moves her bag off it."),
              D("npc_nadia", "Nobody sits at the front for him. You'll see why.")),
            G(cond(SKIRT), P("You sit down and your skirt rides up your thighs. You tug it. He watches you tug it.")),
            P("He goes back to his slide. Then his pen slips out of his fingers and rolls off the stage, and stops against your shoe. He doesn't bend for it. He waits."),
        ], [
            # false lines a3 #20 (reader): Nadia is met here, after the screen that introduces her has rendered
            go("Pick it up.", node="pen", mins=2, flags=[fset("nadia_met"), fset("desk_guy_met"), fset("rival_met")]),
            go("Leave it.", node="left", mins=2, flags=[fset("nadia_met"), fset("desk_guy_met"), fset("rival_met")]),
        ]),
        node("pen", "His pen", [
            P("You bend down for it, all the way, and when you come back up his eyes are on your chest, not your face. He's hard. You can see the line of it against his trousers from the front row. He sees you see it, and steps back behind the lectern."),
            P("He reaches over it and holds his hand out for the pen, flat, so your fingers won't touch his."),
            D(H, "Thank you, @player. Eyes on the slides."),
        ], [go("Hand it back.", node="nadia", mins=60, eff=[setv("hale_step", 1)], consumes=True, flags=[done(1), fset("hale_pen_picked")])]),
        node("left", "The hall waits", [
            P("You don't move. The hall goes quiet, waiting to see who gives first. Dr. Hale comes down off the stage, crouches at your feet and picks the pen up, and looks up at you from there, slowly, all the way up your legs to your face."),
            D(H, "Noted."),
        ], [go("Sit through the lecture.", node="nadia", mins=60, eff=[setv("hale_step", 1)], consumes=True, flags=[done(1)])]),
        node("nadia", "Last spring", [
            P("The girl beside you leans over while the room packs up, and says it without looking up from her bag."),
            D(N, "He does that. Last spring it was me."),
            D(N, "His wife picks him up Thursdays. Half past seven, in the car park, every week. Ask anyone. He's very careful about Thursdays."),
            G(cond(flag("hale_pen_picked")), T("Your professor got hard looking at you, and the girl beside you thinks it's funny. Welcome to college.")),
            G(cond(flag("hale_pen_picked", False)), T("He made the whole room watch you. On purpose.")),
        ], [go("\"After class.\"", loc="campus", mins=5)]),
    ]})

# ── step 2 · Hale B 2 · he lost his place ──
out.append({
    "id": "hale_02_lost_his_place", "name": "He lost his place",
    "description": "Hale step 2 (Hale B 2): her chosen flash, front row; no panties at Daring for this step only (LO). His no: \"Not here. Office hours.\" Sets hale_02_done (his email).",
    "trigger": at_class_start(step_trigger(H, 2, retry_days=2)),
    "nodes": [
        node("legs", "The front row", [
            P("Front row again. His eyes have been on the front row every class since the pen, and today you sit in it on purpose, right in front of the lectern."),
            G(cond(SKIRT), P("You don't fix your skirt when you sit. It rides up and stays up, and he sees it, and loses a word.")),
            G(cond(NOT_SKIRT), P("You sit with your legs crossed and your knee up, and he sees it, and loses a word.")),
            T("Go on. You came here to do this."),
        ], [
            go("Uncross your legs, slowly.", node="flash", mins=5, wardrobe=PANTIES_OFF, flags=[fset("hale02_took_them_off")],
               cond_=cond(SKIRT, {"type": "clothing_item", "item_id": "plain_panties", "operator": "equipped"})),
            go("Uncross your legs, slowly.", node="flash", mins=5, flags=[funset("hale02_took_them_off")],
               cond_=cond(SKIRT, {"type": "clothing_slot", "slot": "underwear", "operator": "unequipped"})),
            go("Pull your waistband down an inch.", node="flash", mins=5, wardrobe=PANTIES_OFF, flags=[fset("hale02_took_them_off")],
               cond_=cond(NOT_SKIRT, NO_DRESS, {"type": "clothing_item", "item_id": "plain_panties", "operator": "equipped"})),
            go("Pull your waistband down an inch.", node="flash", mins=5, flags=[funset("hale02_took_them_off")],
               cond_=cond(NOT_SKIRT, NO_DRESS, {"type": "clothing_slot", "slot": "underwear", "operator": "unequipped"})),
            go("Inch your hem up.", node="flash", mins=5, wardrobe=PANTIES_OFF, flags=[fset("hale02_took_them_off")],
               cond_=cond(IN_DRESS, {"type": "clothing_item", "item_id": "plain_panties", "operator": "equipped"})),
            go("Inch your hem up.", node="flash", mins=5, flags=[funset("hale02_took_them_off")],
               cond_=cond(IN_DRESS, {"type": "clothing_slot", "slot": "underwear", "operator": "unequipped"})),
            go("Fix your skirt.", loc="lecture_hall", mins=60, retry=2, cond_=cond(SKIRT)),
            go("Sit up straight.", node="straight", mins=2, cond_=cond(NOT_SKIRT)),
        ]),
        node("flash", "Nothing under it", [
            G(cond(flag("hale02_took_them_off")), P("You went to the toilets before class and took your panties off and put them in your bag.")),
            G(cond(flag("hale02_took_them_off", False)), P("You came to class with nothing under it, and he doesn't know that yet.")),
            G(cond(SKIRT), P("Now you uncross your legs, slowly, in the front row, and let him see.")),
            G(cond(NOT_SKIRT, NO_DRESS), P("Now you lean back in the front row and pull your waistband down an inch at the hip, slowly, and let him see there's nothing under it.")),
            G(cond(IN_DRESS), P("Now you lean back in the front row and inch your hem up your thigh, slowly, and let him see there's nothing under it.")),
            P("Dr. Hale stops in the middle of a sentence. He doesn't start it again. He looks at you and three rows behind you hear the silence, and somebody coughs, and he looks down at his notes like they're in another language."),
        ], [go("\"You lost your place, Dr. Hale.\"", node="after", mins=60, eff=[add("exhibitionism", 3, cap=79)])]),
        node("after", "Office hours", [
            P("After class he waits until the room has emptied before he speaks to you. He keeps the lectern between you."),
            D(H, "Not here, @player. Office hours."),
            ME("When?"),
            D(H, "Thursday. After six."),
            T("He named the hour himself."),
        ], [go("\"Thursday.\"", loc="campus", mins=5, consumes=True,
               eff=[setv("hale_step", 2)], flags=[done(2)])]),
        node("straight", "Sit up straight", [
            P("You sit up straight and keep your eyes on your notes. Dr. Hale finds his place, and doesn't look at the front row again until the end."),
        ], [go("Sit through the lecture.", loc="lecture_hall", mins=60, retry=2)]),
    ]})

# ── step 3 · Hale B 3 · the photo face-down ──
out.append({
    "id": "hale_03_photo_face_down", "name": "The photo, face-down",
    "description": "Hale step 3 (release 1), private coaching: the photo turned down, his offer, his hand on her shoulder. Three answers, all finish the step; no grade on it. Laura reads the grade at home.",
    "trigger": step_trigger(H, 3),
    "nodes": [
        node("desk", "His desk", [
            P("His office door is open an inch. He's at his desk with your paper in front of him and the wedding photo beside it, face-up: Dr. Hale and a woman with short dark hair, laughing on a beach. You sit on the corner of his desk instead of the chair."),
            G(cond(SKIRT), P("Your skirt rides up. He reads the same line of your paper three times.")),
            D(H, "Your argument on page two is good. Page three falls apart."),
        ], [go("Lean over to see.", node="offer", mins=10)]),
        node("offer", "Face-down", [
            P("He reaches over without looking and turns the photo face-down."),
            G(cond(trait("grade_psych", "lt", 40)), D(H, "You're failing, @player. I coach students who want to understand the material.")),
            G(cond(trait("grade_psych", "gte", 40), trait("grade_psych", "lt", 70)), D(H, "Your grade is a C, @player. I coach students who want to understand the material.")),
            G(cond(trait("grade_psych", "gte", 70)), D(H, "Your grade is good, @player. Good isn't understanding. I coach students who want to understand the material.")),
            P("He comes round the desk and stands behind you, and his hand settles on your shoulder, warm and heavy, and stays."),
            D(H, "Psychology starts with a person's sexuality. If you don't understand yours, you won't get any further."),
            G(cond(trait("corruption", "lt", 20)), T("He's your professor. He's married.")),
            G(cond(trait("corruption", "gte", 20)), T("You want to know what he'd do next.")),
        ], [
            go("\"When?\"", node="when", mins=5),
            go("\"That isn't coaching.\"", node="isnt", mins=2),
            go("Walk out.", node="out", mins=2),
        ]),
        node("when", "Thursdays", [
            D(H, "Thursdays. Half past six. The door will be locked."),
            P("His thumb moves once on your collarbone. Then he lets go."),
        ], [go("Pick up your paper.", node="portal", mins=5, flags=[fset("hale_coaching_offered")])]),
        node("isnt", "A C", [
            D(H, "Then your grade stays where it is."),
            P("He takes his hand away. He doesn't turn the photo back over."),
        ], [go("Pick up your paper.", node="portal", mins=2, flags=[fset("hale_coaching_offered")])]),
        node("out", "The offer stands", [
            P("You pick up your bag and walk out without a word. His voice follows you into the corridor, calm, not raised."),
            D(H, "Thursday, @player. The offer stands."),
        ], [go("Keep walking.", node="portal", mins=2, flags=[fset("hale_coaching_offered")])]),
        node("portal", "The portal", [
            P("That week your grade goes up on the tuition portal, and Laura reads it at the kitchen table on her phone."),
            G(cond(trait("grade_psych", "lt", 40)), D("npc_laura", "Failing, @player? We're paying for this course. What are you doing in that man's class?")),
            G(cond(trait("grade_psych", "gte", 40), trait("grade_psych", "lt", 70)), D("npc_laura", "A C, @player? We're paying for this course. What are you doing in that man's class?")),
            G(cond(trait("grade_psych", "gte", 70)), D("npc_laura", "An A? In Psychology? Who's been helping you?")),
        ], [go("Go back to the faculty floor.", loc="faculty_floor", mins=5, consumes=True,
               eff=[setv("hale_step", 3)], flags=[done(3)])]),
    ]})

# ── step 4 · the first session (hale_04_first_session.md, signed 2026-11-01): reworks hale_04_claire_knocks. He
#    leads; "Let him." is a mixed act (both meters); Claire's knock is the ladder's one cut-off. ──
from sheetbeats import beat, pool
CAP = lambda k, n, c: {"targetType": "player", "trait": k, "op": "add", "value": n, "cap": c}
# false lines a3 #21 (DECISIONS 129): the knock is 10 minutes in and Claire's pickup is 19:30, so "I'm early" ends at 19:15
_t4 = step_trigger(H, 4, retry_days=7)
for _s in _t4["schedules"]:
    _s["end_time"] = "19:15"
out.append({
    "id": "hale_04_claire_knocks", "name": "The first session",
    "description": "Hale step 4 of 4, the top step (release 1): \"Tell me what you feel.\" His hand; Claire knocks. The weekly session opens after it.",
    "trigger": _t4,
    "nodes": [
        node("feel", "Tell me what you feel", [P(beat("hale_04_first_session", "feel")),
            VID("a professor in his office with his hand on a student's bare breast, her saying something", "professor touches student breast office", "teacher hand on tit student office", pool_dir="sex/hale_04_feel_t4")],
            [go("Let him.", node="higher", mins=5),
             go("\"This isn't coaching.\"", node="isnt", mins=2),
             go("Run.", node="run", mins=1)]),
        node("higher", "Higher", [P(beat("hale_04_first_session", "higher")),
            VID("a professor's hand moving up a student's inner thigh in his office", "teacher hand up student thigh office", "professor touching student between her legs", pool_dir="sex/hale_04_higher_t4")],
            [go("Wait.", node="knock", mins=5, eff=[add("grade_psych", 5), CAP("corruption", 3, 79), CAP("exhibitionism", 3, 79)])]),   # a Bold one-time step (DECISIONS 124)
        node("knock", "You ready, love?", [
            P("The knock is two raps, light. A woman's voice through the door, bright."),
            D(CL, "You ready, love? I'm early."),
            P("Dr. Hale takes his hand away, not fast. He doesn't look at the door. He looks at you."),
            D(H, "My wife. Same time next week, @player."),
            T("You want to know what he'd do next."),
        ], [go("Go.", node="corridor", mins=2, flags=[fset("claire_met")])]),
        node("corridor", "The corridor", [
            P("You pull your clothes straight and pick up your bag. He unlocks the door for you."),
            P("His wife is in the corridor in a neat coat, car keys in her hand. Her smile stops halfway when she sees you. Her eyes go to your face, and then past you, to the face-down photo on his desk."),
            D(H, "Claire. This is one of my students."),
            P("You walk the whole corridor without looking back. Your legs are shaking."),
        ], [go("Go home.", loc="home_hall", mins=25, consumes=True, eff=[setv("hale_step", 4)], flags=[done(4), fset("hale_touched")])]),
        node("isnt", "A C", [
            P("You pull everything back down over your tits."),
            ME("This isn't coaching."),
            P("He sits back in his chair."),
            D(H, "Then your grade stays where it is."),
            P("He doesn't unlock the door until you're at it."),
        ], [go("Leave.", loc="faculty_floor", mins=5, retry=7)]),
        node("run", "Run", [
            P("You grab your bag and you're out of the door before he can stand up. In the corridor a woman with short dark hair is coming the other way with car keys in her hand. The woman in the photo."),
            P("She smiles at you, polite, the way you smile at a student."),
            T("His wife. She has no idea."),
        ], [go("Keep walking.", loc="campus", mins=5, retry=7, eff=[add("grade_psych", -2)], flags=[fset("claire_met")])]),
    ]})

# ── his hot repeatable, the Thursday session (hale_thursday_session.md, signed 2026-11-01): reworks hale_thursdays.
#    Two tiers of three pooled screens; Claire early one Thursday in four (a 1-4 roll on "Let him."). ──
# DECISIONS 124: his hands on her open at Bold · Showing; her top off and her own hand while he watches at Hungry.
LOW_CASES = [[trait("corruption", "lt", 60)]]
HIGH = [trait("corruption", "gte", 60)]
ROLL = lambda op, v: trait("hale_claire_roll", op, v)
SESSION_PAY = lambda c: [add("grade_psych", 2), CAP("corruption", 1, c), CAP("exhibitionism", 1, c)]
out.append({
    "id": "hale_thursdays", "name": "Thursday, half past six",
    # reader a3, seen by the readers (DECISIONS 131): the stages match the trigger (Corruption 40, Exhibitionism 40)
    "description": "The Thursday session after Hale's step 4: his hands over her clothes (Bold and Showing: Corruption 40, Exhibitionism 40) or her top off and touching herself while he takes notes (Hungry: Corruption 60). Grade +2, both meters +1. Claire is early one Thursday in four. Hale, further: next release.",
    "trigger": {"location": "hale_office", "requires_npc": H, "is_repeatable": True, "priority": 5, "is_active": True,
                "max_triggers_per_day": 1,
                "schedules": [{"weekdays": [3], "start_time": "18:30", "end_time": "19:05"}],   # done before Claire at half past (as built)
                "conditions": cond(trait("hale_step", "eq", 4), trait("corruption", "gte", 40), trait("exhibitionism", "gte", 40))},
    "nodes": [
        node("door", "Twenty minutes", [
            P("His office door is unlocked. He locks it behind you without a word. The photo is already face-down."),
            D(H, "Twenty minutes, @player."),
        ], [go("Let him.", node="roll", mins=1, eff=[{"targetType": "player", "trait": "hale_claire_roll", "op": "set", "value": {"type": "random", "min": 1, "max": 4}}]),
            go("\"This isn't coaching.\"", node="isnt", mins=2, eff=[add("grade_psych", -1)]),
            go("Run.", node="run", mins=1, eff=[add("grade_psych", -2)])]),
        node("roll", "His hands", [P("He comes round the desk.")],
            [go("Go on.", node="claire_car", mins=1, cond_=cond(ROLL("eq", 1)))]
            + [go("Go on.", node="touch_low", mins=1, cond_=cond(ROLL("gte", 2), *c)) for c in LOW_CASES]
            + [go("Go on.", node="touch_high", mins=1, cond_=cond(ROLL("gte", 2), *HIGH))]),
        node("touch_low", "Tell me what you feel", [G(cond(*[{"type": "clothing_item", "item_id": d, "operator": "unequipped"} for d in DRESSES]), POOL(P(beat("hale_thursday_session", "A a")), P(beat("hale_thursday_session", "A b")), P(beat("hale_thursday_session", "A c")), pid="hale_touch_low", bag=True)),
            *[G(cond({"type": "clothing_item", "item_id": d, "operator": "equipped"}), POOL(*[P(beat("hale_thursday_session", k).replace("your top", "your dress")) for k in ("A a", "A b", "A c")], pid=f"hale_touch_low_{d}", bag=True)) for d in DRESSES],
            VID("a professor's hands on a student over her clothes in his office, her answering him", "professor touches student over clothes office", "teacher hands on student body talking", pool_dir="sex/hale_thursday_low_t4")],
            [go("\"Same time next week.\"", node="end", mins=15, eff=SESSION_PAY(59))]),
        node("touch_high", "Describe it", [POOL(P(beat("hale_thursday_session", "B a")), P(beat("hale_thursday_session", "B b")), P(beat("hale_thursday_session", "B c")), pid="hale_touch_high", bag=True),
            VID("a topless student touching herself in her professor's office while he watches and takes notes", "student masturbates professor watches notes", "girl touches herself teacher watching office", pool_dir="sex/hale_thursday_high_t5")],
            [go("\"Same time next week.\"", node="end", mins=15, eff=SESSION_PAY(79))]),
        node("claire_car", "She's early", [
            P("His phone buzzes on the desk before he's touched you. He reads it and his face goes flat."),
            D(H, "She's early. She's in the car park."),
            P("He unlocks the door and holds it open."),
            D(H, "Next Thursday."),
            P("From the corridor window you can see a car with its engine running."),
        ], [go("Go.", loc="faculty_floor", mins=5, eff=[add("grade_psych", 2)])]),
        node("end", "Thursday", [
            P("He looks at the clock, and straightens his tie, and unlocks the door."),
            D(H, "Thursday."),
            P("Down in the car park his wife's car isn't there yet."),
        ], [go("Go.", loc="faculty_floor", mins=2)]),
        node("isnt", "A C", [
            ME("This isn't coaching."),
            D(H, "Then your grade stays where it is."),
            P("He turns the photo face-up and doesn't look at you while you go."),
        ], [go("Go.", loc="faculty_floor", mins=2)]),
        node("run", "Run", [
            P("You're out of the door before he's out of his chair. Behind you, calm, not raised:"),
            D(H, "Next Thursday, @player."),
        ], [go("Go.", loc="faculty_floor", mins=2)]),
    ]})

# ── his office hub (one line on her grade, one on her clothes; the start choice) ──
out.append({
    "id": "hub_hale_office", "name": "Dr. Hale",
    "description": "Hale's office hub on Thursdays: one line on her grade, one on her clothes, the start choice.",
    "trigger": {"location": "hale_office", "npc": H, "requires_npc": H, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("hale_met"))},
    "nodes": [node("office", "His office", [
        P("Dr. Hale looks up from a pile of papers."),
        G(cond(trait("hale_step", "lt", 3)), P("The photo on his desk is face-up: him and a woman with short dark hair, laughing on a beach.")),
        G(cond(trait("hale_step", "gte", 3)), P("The photo on his desk is face-down. He doesn't turn it over.")),
        G(cond(trait("grade_psych", "lt", 40)), D(H, "You're failing my course, @player. That isn't like you.")),
        G(cond(trait("grade_psych", "gte", 40), trait("grade_psych", "lt", 70)), D(H, "A pass. You could do better. You know you could.")),
        G(cond(trait("grade_psych", "gte", 70)), D(H, "Top of the class. I'd say I'm proud, but you'd make something of it.")),
        G(cond(SKIRT), P("His eyes drop to your thighs, and his neck goes red. He loses the sentence, pulls his chair in tight under the desk, and starts it again.")),
        # reader a3 #29 (DECISIONS 131): the braless line names her body. His crude column (npc_hale.md) is legs/ass at
        # stages 1-2 and tits/nipples from stage 3, so "nipples" waits for his step 3; before it, her chest.
        G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "worn_exposure", "operator": "eq", "value": 0}, trait("hale_step", "lt", 3)),
          P("His eyes go to your chest and stay there a second too long. He keeps the desk between you.")),
        G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "worn_exposure", "operator": "eq", "value": 0}, trait("hale_step", "gte", 3)),
          P("His eyes go to your nipples, showing through what you're wearing. He keeps the desk between you.")),
        G(cond(flag("college_for_grades")), D(H, "You're here for the grades. I can always tell the ones who are.")),
        G(cond(flag("college_for_fun")), D(H, "You're here for the fun, aren't you? Is this fun?")),
        G(cond(flag("college_for_freedom")), D(H, "You look like someone who came here to get away from something.")),
        G(cond(trait("hale_step", "eq", 2), tod("18:00", "19:30")), P("He looks at the clock. It's after six.")),
        G(cond(trait("hale_step", "eq", 4)), P("He looks at the clock, and then at you, like you're both on his schedule.")),
        # reader a3 #18 (DECISIONS 131): every step gets a line pointing at the next visit. This hub runs Thu 17:00-19:30.
        # Step 1: the next step is a Psychology class (Mon/Wed/Fri), and Friday's is tomorrow. Step 2: his step 3 opens
        # here at 18:00, so before six he says six. Step 3: his step 4 and the sessions are Thursdays at 18:30.
        G(cond(trait("hale_step", "eq", 1)), D(H, "Front row tomorrow, @player. Where I can see you.")),
        G(cond(trait("hale_step", "eq", 2), tod("17:00", "18:00")), D(H, "After six, @player. Not before.")),
        G(cond(trait("hale_step", "eq", 3)), D(H, "Thursdays. Half past six, @player.")),
    ], [
        # S4 (LO 2026-11-03): in his office he isn't busy, so one choice aimed at him. An hour, Psychology +1, cap 69.
        go("Ask him about your essay.", node="essay", mins=0),
        go("\"Bye, Dr. Hale.\"", loc="faculty_floor")]),
        node("essay", "Your essay", [
            P("He reads your essay at the desk with his pen out, and talks you through it line by line. He doesn't touch you once. He doesn't need to."),
            D(H, "Your argument's here, @player. You buried it on page three. Lead with it."),
        ], [go("Thank him.", loc="faculty_floor", mins=60, eff=[{"targetType": "player", "trait": "grade_psych", "op": "add", "value": 1, "cap": 69}])])]})

# ── Nadia: the library, the canteen, beside her in Psychology ──
NADIA_LINES = POOL(D(N, "Thursday office hours are a trap, you know that?"),
                   D(N, "You want my notes? You can have my notes."), D(N, "Sit. I'll tell you which lecturers to avoid."), pid="nadia_lines")
# "After class" is true only on a Psychology morning, and his interest only after his step 2.
NADIA_ASKED = G(cond(trait("hale_step", "gte", 2), wd(0, 2, 4)), D(N, "He asked about you. Hale. After class."))
for cid, loc, name, setting in [("hub_nadia_library", "library", "Nadia, studying", "Nadia at a library table with her headphones round her neck."),
                                 ("hub_nadia_canteen", "canteen", "Nadia, at lunch", "Nadia at the end of a table with a salad and a textbook open beside it."),
                                 ("hub_nadia_lecture", "lecture_hall", "Nadia, beside you", "Nadia in the seat beside yours, her pen already moving.")]:
    out.append({
        "id": cid, "name": name,
        "description": f"Nadia's hub ({loc}): one line about Hale.",
        "trigger": {"location": loc, "npc": N, "requires_npc": N, "is_repeatable": True, "priority": 6, "is_active": True,
                    "conditions": cond(flag("nadia_met"))},
        "nodes": [node("nadia", name, [
            P(setting),
            NADIA_LINES,
            *([NADIA_ASKED] if loc != "lecture_hall" else []),
            G(cond(SKIRT, trait("hale_step", "gte", 2)), D(N, "He'll lose his place again.")),
            G(cond(trait("hale_step", "gte", 4)), D(N, "His wife came to the office. Everyone's saying. Was it you?")),
        ], [go("Talk a while.", loc=loc, mins=20), go("Go.", loc="campus")])]})

cards = step_cards(H, {
    1: ("Monday, first class: Psychology.", "Go to Psychology on Monday morning, the lecture hall"),   # C3: no name before the meeting
    2: ("His eyes are on the front row every class.", "The next Psychology class, front row, Monday, Wednesday or Friday morning (Daring)"),
    3: ("\"Thursday. Office hours.\"", "Thursday evening: Dr. Hale's office on the faculty floor, during his office hours"),
    # reader a3 (DECISIONS 131): the card names step 4's real gate, Corruption 40 and Exhibitionism 40
    4: ("\"Thursdays. Half past six. The door will be locked.\"", "Thursday, half past six: his office (Bold, Showing)"),
}, met_flag="hale_met", pointer=(1, "Your Psychology lecturer"),
   terminal_text=("Thursdays, half past six: his office, the door locked.", "Hale, further. (Next release)"))
for c in cards:
    c["when"].append({"flag": "opening_done", "op": "is_true"})

text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · DR. HALE (sheets/scenes/hale_0*.md, people/npc_hale.md, people/npc_nadia.md)\n"
        "# Steps 1-5, Thursdays at seven, his office hub, Nadia's hubs, his cards.\n"
        "# =============================================================================\n")
# Coming to his office clears the booking her email reply made (phone.py, DECISIONS 87).
for _c in out:
    if _c["id"] == "hale_03_photo_face_down":
        clear_on_leave(_c, "hale_office_booked")
    if _c["id"] == "hale_thursdays":
        clear_on_leave(_c, "hale_thursday_booked")
text += "".join(emit(c) for c in out) + "".join(emit_card(c) for c in cards)
open(__import__("sys").argv[1], "w").write(text)
print("hale:", len(out), "canvases,", len(cards), "cards")
