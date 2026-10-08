"""Dr. Hale — steps 1-5 (Hale B 1-5), Thursdays at seven (the repeat), his office hub; Nadia's hubs.
Source: sheets/scenes/hale_0*.md, people/npc_hale.md, people/npc_nadia.md. Explicit screens pasted as signed."""
from canv import *
from tomlw import tod, wd

H = "npc_hale"
N = "npc_nadia"
CL = "npc_claire"
out = []

def done(n):
    return fset(f"hale_0{n}_done")

SKIRT = {"type": "worn_type", "operator": "eq", "value": "short_skirt"}
NOT_SKIRT = {"type": "worn_type", "operator": "neq", "value": "short_skirt"}
PANTIES_OFF = [{"action": "unequip", "item_id": "plain_panties"}]

HAND = ("You sit on the corner of his desk and undo the buttons yourself, one at a time, slowly. There is nothing under them. Your tits come free, bare to him, your nipples already tight. Dr. Hale stares. He wants to touch you, but he can't stop looking first. \"@player,\" he says. His voice cracks on it. Then his hand slides inside, and his palm closes over your tit. It covers you completely, warm and heavy. His thumb finds your nipple and rolls it, slow, then harder. You arch into his hand. His breath goes ragged against your neck. His cock is hard, pressing against the edge of the desk an inch from your hip. Your nipple is stiff under his thumb, so he rolls it again until you gasp.")

# ── step 1 · Hale B 1 · the first lecture (meets Hale and Nadia) ──
out.append({
    "id": "hale_01_first_lecture", "name": "Your first lecture",
    "description": "Hale step 1 (Hale B 1), Monday's first class: the dropped pen. Meets Hale, Nadia, the guy beside her and the rival girl.",
    "trigger": step_trigger(H, 1),
    "nodes": [
        node("front_row", "The front row", [
            IMG("scenes/hale_01_lecture.jpg", "a lecture hall, a male professor in his late thirties at a lectern, students in raked seats, a girl in the front row",
                "professor at lectern lecture hall students", "college lecture hall front row professor"),
            P("The lecture hall is half full and loud. The only free seats are in the front row. A girl with big glasses and a cardigan waves you over and moves her bag off the seat beside her."),
            WHO("Sit here. Nobody sits at the front for him. You'll see why."),
            P("At the lectern, a man in his late thirties is setting up his slides: tweed jacket, a wedding ring, a face that would be handsome if he smiled. Your Psychology professor. He looks up, and finds you, and his eyes stay on you while he says good morning to the room."),
            G(cond(SKIRT), P("You sit down and your skirt rides up your thighs. You tug it. He watches you tug it.")),
        ], [go("Sit.", node="pen", mins=10, flags=[fset("hale_met"), fset("nadia_met"), fset("desk_guy_met"), fset("rival_met")])]),
        node("pen", "The pen", [
            P("Twenty minutes in, your pen rolls off the desk. You bend down for it, all the way to the floor, and when you come back up with it, he's stopped talking."),
            P("Dr. Hale is standing very still behind the lectern. He's hard. You can see it from the front row, the line of it against his trousers, and he doesn't look away from you and he doesn't move to hide it. Then he clears his throat and finds his slide."),
            D(H, "Where was I. Attachment theory."),
        ], [
            go("\"Did he just—?\"", node="nadia", mins=60, eff=[setv("hale_step", 1)], consumes=True, flags=[done(1)]),
            go("Look away.", node="nadia", mins=60, eff=[setv("hale_step", 1)], consumes=True, flags=[done(1)]),
        ]),
        node("nadia", "Last spring", [
            P("The girl beside you leans over while the room packs up, and says it without looking up from her bag."),
            D(N, "He does that. Last spring it was me. I'm Nadia."),
            D(N, "His wife picks him up Thursdays. Half past seven, in the car park, every week. Ask anyone. He's very careful about Thursdays."),
            T("Your professor got hard looking at you, and the girl beside you thinks it's funny. Welcome to college."),
        ], [go("\"After class.\"", loc="campus", mins=5)]),
    ]})

# ── step 2 · Hale B 2 · he lost his place ──
out.append({
    "id": "hale_02_lost_his_place", "name": "He lost his place",
    "description": "Hale step 2 (Hale B 2): her chosen flash, front row; no panties at Daring for this step only (LO). His no: \"Not here. Office hours.\" Sets hale_02_done (his email).",
    "trigger": step_trigger(H, 2, retry_days=2),
    "nodes": [
        node("legs", "The front row", [
            P("Front row again. His eyes have been on the front row every class since the pen, and today you sit in it on purpose, right in front of the lectern."),
            G(cond(SKIRT), P("You don't fix your skirt when you sit. It rides up and stays up, and he sees it, and loses a word.")),
            G(cond(NOT_SKIRT), P("You sit with your legs crossed and your knee up, and he sees it, and loses a word.")),
            T("Go on. You came here to do this."),
        ], [
            go("Uncross your legs, slowly.", node="flash", mins=5, wardrobe=PANTIES_OFF, cond_=cond(SKIRT, {"type": "clothing_item", "item_id": "plain_panties", "operator": "equipped"})),
            go("Uncross your legs, slowly.", node="flash", mins=5, cond_=cond(SKIRT, {"type": "clothing_slot", "slot": "underwear", "operator": "unequipped"})),
            go("Pull your waistband down an inch.", node="flash", mins=5, wardrobe=PANTIES_OFF, cond_=cond(NOT_SKIRT, {"type": "clothing_item", "item_id": "plain_panties", "operator": "equipped"})),
            go("Pull your waistband down an inch.", node="flash", mins=5, cond_=cond(NOT_SKIRT, {"type": "clothing_slot", "slot": "underwear", "operator": "unequipped"})),
            go("Fix your skirt.", loc="lecture_hall", mins=60, retry=2, cond_=cond(SKIRT)),
        ]),
        node("flash", "Nothing under it", [
            G(cond(SKIRT), P("You went to the toilets before class and took your panties off and put them in your bag, and now you uncross your legs, slowly, in the front row, and let him see what you did.")),
            G(cond(NOT_SKIRT), P("You went to the toilets before class and took your panties off and put them in your bag. Now you lean back in the front row and pull your waistband down an inch at the hip, slowly, and let him see there's nothing under it.")),
            P("Dr. Hale stops in the middle of a sentence. He doesn't start it again. He looks at you and three rows behind you hear the silence, and somebody coughs, and he looks down at his notes like they're in another language."),
        ], [go("\"You lost your place, Dr. Hale.\"", node="after", mins=60, eff=[add("exhibitionism", 3)])]),
        node("after", "Office hours", [
            P("After class he waits until the room has emptied before he speaks to you. He keeps the lectern between you."),
            D(H, "Not here, @player. Office hours."),
            ME("When?"),
            D(H, "Thursday. After six."),
            T("He named the hour himself."),
        ], [go("\"Thursday.\"", loc="campus", mins=5, consumes=True,
               eff=[setv("hale_step", 2)], flags=[done(2)])]),
    ]})

# ── step 3 · Hale B 3 · the photo face-down ──
out.append({
    "id": "hale_03_photo_face_down", "name": "The photo, face-down",
    "description": "Hale step 3 (Hale B 3), Thursday evening in his office: his hand on her shoulder, the wedding photo turned down. A study session lifts her Psychology grade; Laura reads the grade at home.",
    "trigger": step_trigger(H, 3),
    "nodes": [
        node("desk", "His desk", [
            P("His office door is open an inch. He's at his desk with your paper in front of him and the wedding photo beside it, face-up: Dr. Hale and a woman with short dark hair, laughing on a beach. You sit on the corner of his desk instead of the chair."),
            G(cond(SKIRT), P("Your skirt rides up. He reads the same line of your paper three times.")),
            D(H, "Your argument on page two is good. Page three falls apart."),
        ], [go("Lean over to see.", node="photo", mins=10)]),
        node("photo", "Face-down", [
            P("He stands behind you to point at page three, and his hand comes to rest on your shoulder while he reads, and stays there. Warm. Heavy. He's not reading any more. Then, without looking at it, he reaches over and turns the photo face-down on the desk."),
            T("He turned his wife over so she wouldn't see."),
        ], [
            go("\"Is that a no on my paper, or a yes?\"", node="portal", mins=20, eff=[add("grade_psych", 2)]),
            go("\"Just the paper.\"", node="paper", mins=20, eff=[add("grade_psych", 2)]),
        ]),
        node("portal", "The portal", [
            D(H, "It's a yes, @player. On the paper."),
            G(cond(flag("college_for_grades")), D(H, "You told me you came here for grades. So did I, once.")),
            P("That week your grade goes up on the tuition portal, and Laura reads it at the kitchen table on her phone."),
            G(cond(trait("grade_psych", "lt", 40)), D("npc_laura", "Failing, @player? We're paying for this course. What are you doing in that man's class?")),
            G(cond(trait("grade_psych", "gte", 40), trait("grade_psych", "lt", 70)), D("npc_laura", "A C, @player? We're paying for this course. What are you doing in that man's class?")),
            G(cond(trait("grade_psych", "gte", 70)), D("npc_laura", "An A? In Psychology? Who's been helping you?")),
        ], [go("Go back to the faculty floor.", loc="faculty_floor", mins=5, consumes=True,
               eff=[setv("hale_step", 3)], flags=[done(3)])]),
        no_node("paper", [D(H, "The paper, then."), P("He takes his hand off your shoulder and turns the photo face-up again, carefully, like he's putting something back where it belongs."), D(H, "Page three. Fix it.")],
                "hale_office", 7),
    ]})

# ── step 4 · Hale B 4 · Claire knocks (his voice sample; every screen as signed) ──
out.append({
    "id": "hale_04_claire_knocks", "name": "Claire knocks",
    "description": "Hale step 4 (Hale B 4), the voice sample: Thursday near his wife's pickup; her body bare to him, his hand on her; Claire at the door. Meets Claire.",
    "trigger": step_trigger(H, 4, retry_days=7),
    "nodes": [
        node("desk", "Thursday", [
            P("The corridor outside is empty. You sit on the corner of Dr. Hale's desk, like last time. His wedding photo still lies face-down where he turned it. He holds your paper and reads none of it. His eyes go to the clock, because Claire comes soon and you both know it. Then they come back to your mouth, and down your legs, and they stay there. \"@player.\" He says your name like it costs him. His voice has gone rough. \"You can't sit like that in here.\" \"Like what?\" He stares at your tits instead of answering. You want him staring. Your hand goes to your own top button."),
        ], [
            go("Undo it.", node="hand", mins=5, wardrobe=[{"action": "unequip", "item_id": "plain_bra"}, {"action": "unequip", "item_id": "sports_bra"}]),
            go("Button up.", node="no", mins=2),
        ]),
        node("hand", "His hand", [
            P(HAND),
            VID("a professor's hand inside a student's open blouse on his desk, his thumb on her nipple, a face-down photo on the desk", "professor hand inside open blouse desk office", "student on desk shirt open teacher touching breast", file="sex/hale_04_hand_t4.webm"),
        ], [go("Let him.", node="knock", mins=5, eff=[add("exhibitionism", 3), add("corruption", 3)])]),
        node("knock", "You ready, love?", [
            P("His hand is on your bare tit when the knock comes. A woman's voice through the door, bright: \"You ready, love?\" Hale goes grey. He snatches his hand back, and he can't move. Your heart is slamming, but your hands are steady. You do one button, slow. You slide off the desk and open the door yourself. His wife stands in a neat coat, car keys in her hand. Her smile stops halfway. \"Your husband's a great teacher,\" you say. Hale, behind you: \"Claire — this is one of my students.\" Her eyes drop to your flushed chest. Then they go past you, to the face-down photo on his desk."),
        ], [go("Leave.", node="corridor", mins=2, flags=[fset("claire_met")])]),
        node("corridor", "The corridor", [
            P("You walk down the empty faculty corridor, slowly, past Dr. Hale's wife. Claire doesn't stop you. You do the rest of your buttons as you go, one at a time, because your fingers won't hurry. Behind you, through the half-open door, Claire's voice comes very calm. \"Grab your coat.\" *His wife saw you. His hand was on you a minute ago.* And you're not scared, not even a little. You're shaking because you liked it. Next class, Dr. Hale has to stand at the lectern and look at you. And he'll have something to say."),
        ], [go("Go home.", loc="campus", mins=10, consumes=True, eff=[setv("hale_step", 4)], flags=[done(4)])]),
        node("no", "Next Thursday", [
            P("You let go of your top button. You slide off his desk and pick up your paper. Your face is hot. Dr. Hale breathes out, half relief and half not. \"Next Thursday, then, @player.\" His eyes stay on you, and he still wants a yes. He turns the photo face-up. A second later his hand turns it face-down again and stays flat on it."),
        ], [go("Leave.", loc="faculty_floor", mins=5, retry=7)]),
    ]})

# ── step 5 · Hale B 5 · seven-twenty ──
out.append({
    "id": "hale_05_seven_twenty", "name": "Seven-twenty",
    "description": "Hale step 5 (Hale B 5), after a Psychology class: she sets his hour. Sets hale_hour_set and hale_05_done (his weekly email).",
    "trigger": step_trigger(H, 5, retry_days=2),
    "nodes": [
        node("stay", "Stay behind", [
            P("He couldn't start the lecture on time. He hasn't been able to since the knock. When the room empties you stay in the front row, and he stands at the lectern gripping it with both hands."),
            D(H, "This has to stop, @player."),
        ], [
            go("\"What do you want?\"", node="hour", mins=5),
            go("\"See you in class.\"", loc="campus", mins=2, retry=2),
        ]),
        node("hour", "Seven", [
            P("He doesn't answer, because the answer is you. So you answer for him."),
            ME("Thursdays at seven. Your office. You'll be done by seven-twenty."),
            P("He closes his eyes. When he opens them he nods, once, like a man signing something."),
            G(cond(flag("midterm_done"), trait("grade_psych", "gte", 70)),
              P("At dinner that week Laura reads your Psychology midterm off her phone. A B-plus."),
              D("npc_laura", "See what she does when she tries.")),
            T("He'll watch the clock the whole time. So will you."),
        ], [go("\"Seven.\"", loc="campus", mins=5, consumes=True,
               eff=[setv("hale_step", 5)], flags=[done(5), fset("hale_hour_set")])]),
    ]})

# ── the repeat: Thursdays at seven (hale_05 sheet) ──
out.append({
    "id": "hale_thursdays", "name": "Thursday, seven",
    "description": "The repeat after Hale step 5: her hour in his office, his hands on her (at Bold, above her waist, as in step 4), the photo down, Claire due at half past. Once a Thursday.",
    "trigger": {"location": "hale_office", "requires_npc": H, "is_repeatable": True, "priority": 5, "is_active": True,
                "max_triggers_per_day": 1,
                "schedules": [{"weekdays": [3], "start_time": "18:30", "end_time": "19:20"}],
                "conditions": cond(trait("hale_step", "eq", 5), trait("corruption", "gte", 40))},
    "nodes": [
        node("door", "Seven", [
            P("He's waiting with the door unlocked and the photo already face-down. He locks the door behind you without a word and looks at the clock, and then at you, and the clock doesn't matter any more."),
            D(H, "Twenty minutes, @player."),
        ], [
            go("Sit on the desk.", node="hand", mins=5, wardrobe=[{"action": "unequip", "item_id": "plain_bra"}, {"action": "unequip", "item_id": "sports_bra"}]),
            go("\"Not tonight.\"", node="no", mins=2),
        ]),
        node("hand", "Twenty minutes", [
            P(HAND),
            VID("a professor touching a student's bare breast on his desk, evening light, office", "professor touching student breast office desk evening", "teacher hand on breast student sitting on desk", pool_dir="sex/hale_thursday_t4"),
        ], [
            go("Make him watch the clock.", node="leave", mins=15,
               eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 59}]),
            go("Button up.", node="leave", mins=5),
        ]),
        node("leave", "Seven-twenty", [
            P("When the twenty minutes are gone he stands up and straightens his tie with shaking hands and unlocks the door. Footsteps in the corridor stop outside, then go on. You walk out past the car park, where his wife's car will be soon."),
            D(H, "Thursday."),
        ], [go("Go.", loc="faculty_floor", mins=5)]),
        no_node("no", [D(H, "Then why did you come?"), P("He sits back down behind the desk and turns the photo face-up, and stares at it, and doesn't look at you while you go.")], "faculty_floor", None),
    ]})

# ── his office hub (one line on her grade, one on her clothes; the start choice) ──
out.append({
    "id": "hub_hale_office", "name": "Dr. Hale",
    "description": "Hale's office hub on Thursdays: one line on her grade, one on her clothes, the start choice.",
    "trigger": {"location": "hale_office", "npc": H, "requires_npc": H, "is_repeatable": True, "priority": 6, "is_active": True,
                "conditions": cond(flag("hale_met"))},
    "nodes": [node("office", "His office", [
        P("Dr. Hale looks up from a pile of papers. The photo on his desk is face-up, for now."),
        G(cond(trait("grade_psych", "lt", 40)), D(H, "You're failing my course, @player. That isn't like you.")),
        G(cond(trait("grade_psych", "gte", 40), trait("grade_psych", "lt", 70)), D(H, "A pass. You could do better. You know you could.")),
        G(cond(trait("grade_psych", "gte", 70)), D(H, "Top of the class. I'd say I'm proud, but you'd make something of it.")),
        G(cond(SKIRT), P("He loses the sentence, and starts it again.")),
        G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "worn_exposure", "operator": "eq", "value": 0}), P("He keeps the desk between you.")),
        G(cond(flag("college_for_grades")), D(H, "You came here for grades. I remember. Everyone remembers what they came for.")),
        G(cond(flag("college_for_fun")), D(H, "You came here for fun, you said. Is this fun?")),
        G(cond(flag("college_for_freedom")), D(H, "Freedom. That's a big word for a first-year.")),
        G(cond(trait("hale_step", "eq", 2), tod("18:00", "19:30")), P("He looks at the clock. It's after six.")),
        G(cond(trait("hale_step", "eq", 4)), P("He can't look at you for long. He checks the corridor before he speaks.")),
    ], [go("\"Goodnight, Dr. Hale.\"", loc="hale_office")])]})

# ── Nadia: the library, the canteen, beside her in Psychology ──
NADIA_LINES = POOL(D(N, "He asked about you. Hale. After class."), D(N, "Thursday office hours are a trap, you know that?"),
                   D(N, "You want my notes? You can have my notes."), pid="nadia_lines")
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
            G(cond(SKIRT), D(N, "He'll lose his place again.")),
            G(cond(trait("hale_step", "gte", 4)), D(N, "His wife came to the office. Everyone's saying. Was it you?")),
        ], [go("Talk a while.", loc=loc, mins=20), go("Go.", loc=loc)])]})

cards = step_cards(H, {
    1: ("Monday, first class: Psychology with Dr. Hale.", "Go to Psychology on Monday morning, the lecture hall"),
    2: ("His eyes are on the front row every class.", "The next Psychology class, front row, Monday, Wednesday or Friday morning (Curious, Daring)"),
    3: ("\"Thursday. After six.\"", "Thursday evening: Dr. Hale's office on the faculty floor, after six (Curious, Daring)"),
    4: ("The photo on his desk is face-down. Claire picks him up at half past seven.", "Thursday evening in his office, close to half past seven (Bold, Showing)"),
    5: ("He can't start the lecture on time any more.", "After a Psychology class, Monday, Wednesday or Friday morning: stay behind (Bold)"),
}, terminal_text=("Thursdays at seven, your hour. Done by seven-twenty.", "Dr. Hale's next step comes in the next release."),
   closed_text="You transferred out of his section. Your grade is what you earn.")
for c in cards:
    c["when"].append({"flag": "opening_done", "op": "is_true"})

text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · DR. HALE (sheets/scenes/hale_0*.md, people/npc_hale.md, people/npc_nadia.md)\n"
        "# Steps 1-5, Thursdays at seven, his office hub, Nadia's hubs, his cards.\n"
        "# =============================================================================\n")
text += "".join(emit(c) for c in out) + "".join(emit_card(c) for c in cards)
open(__import__("sys").argv[1], "w").write(text)
print("hale:", len(out), "canvases,", len(cards), "cards")
