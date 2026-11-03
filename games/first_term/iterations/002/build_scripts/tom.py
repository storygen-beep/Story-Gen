"""Tom — the job ask, steps 1-6 (Tom B 1-6), his hub, the Friday kiss repeat, Gary's ten minutes.
Source: sheets/scenes/tom_0*.md, cafe_gary_ten_minutes.md, people/npc_tom.md, people/npc_gary.md,
systems/job.md. Explicit screens pasted as signed."""
from canv import *
from tomlw import tod, wd
from home_items import here

TM = "npc_tom"
GY = "npc_gary"
out = []

def done(n):
    return fset(f"tom_0{n}_done")

UNIFORM = {"type": "worn_type", "operator": "eq", "value": "cafe_uniform"}
SEXY_OWNED = {"type": "clothing_item", "item_id": "cafe_uniform_sexy", "operator": "owned"}
# (bug fix 2026-11-03) was normal then sexy: equip also gives the garment, so the tight uniform was forced on her
# first shift (DECISIONS 104: it is her choice). Normal only; in the tight one already, she keeps it on.
CLOCK_IN = [{"action": "equip", "item_id": "cafe_uniform_normal"}]
SEXY_WORN = {"type": "clothing_item", "item_id": "cafe_uniform_sexy", "operator": "equipped"}
SEXY_NOT_WORN = {"type": "clothing_item", "item_id": "cafe_uniform_sexy", "operator": "unequipped"}

def back(next_node):
    """She changes in the back room: the uniform is equipped before any screen names it."""
    return node("back", "The back room", [
        P("Tom looks up from the till as you come in."),
        D(TM, "Uniform, @player. Back room."),
        P("You change in the back room in front of the staff mirror, between the mop bucket and the crates of milk."),
    ], [go("Clock in.", node=next_node, mins=5, cond_=cond(SEXY_NOT_WORN), wardrobe=CLOCK_IN),
        go("Clock in.", node=next_node, mins=5, cond_=cond(SEXY_WORN))])

# ── the job ask: meets Tom, the job, the uniform ──
out.append({
    "id": "cafe_job_ask", "name": "Ask about the job",
    "description": "Meets Tom: the sign in the window. Sets cafe_job and tom_met; adds the café uniform.",
    # Q2 (LO, 2026-11-04): opens from the coffee at the counter (extras.py cafe_coffee), not on entry, so the café's
    # wardrobe link always shows
    "trigger": {"location": "cafe", "requires_npc": TM, "is_repeatable": False, "priority": 10, "is_active": True,
                "substitution_only": True,
                "consume_on": "exit", "retry_after_days": 1,   # "Not yet." parks it (tom_01_the_apron.md, signed 2026-11-01)
                "schedules": [{"weekdays": [0, 1, 2, 3, 4, 5], "start_time": "08:00", "end_time": "23:00"}],
                "conditions": cond(flag("opening_done"), flag("cafe_job", False))},
    "nodes": [
        node("sign", "STAFF WANTED", [
            IMG("scenes/cafe_job_ask.jpg", "a small cafe counter, a man in his thirties with rolled sleeves behind an espresso machine, a staff wanted sign in the window",
                "cafe manager behind counter espresso machine", "small cafe interior staff wanted sign"),
            P("There's a card taped inside the café window: STAFF WANTED, NO EXPERIENCE NEEDED. Behind the counter a man in his thirties with his sleeves rolled up is wiping the espresso machine. The manager. Tom, says the badge. He looks you over before you've opened your mouth, top to bottom, the way you'd look at something you were thinking of buying."),
            D(TM, "You're here about the sign."),
            ME("I can start today. I need the money."),
            D(TM, "Everybody needs the money. Eight a shift, plus tips. Be on time."),
            T("He looked at you one second too long. Then he was all business."),
        # Q2 (LO, 2026-11-04): from the counter now, which makes it an event to the gates; his look pays him (H5)
        ], [go("\"When do I start?\"", node="uniform", mins=5, eff=[nadd(TM, "want", 2)]),
            go("\"Not yet.\"", node="not_yet", mins=2)]),
        node("not_yet", "Not yet", [
            D(TM, "Sign stays up till somebody takes it."),
            P("He goes back to wiping the machine."),
        ], [go("Leave the sign where it is.", loc="cafe", mins=2, retry=1)]),   # pass 3 D39 (R7): the way out answers him
        node("uniform", "The uniform", [
            P("He reaches under the counter and pushes a folded uniform across to you: a black dress with a white apron, the café's name stitched on the pocket."),
            D(TM, "Eight till seven, up to three shifts a day, Monday to Saturday. Wear that. Be on time."),
        ], [go("Take the uniform.", loc="cafe", mins=5, consumes=True, flags=[fset("cafe_job"), fset("tom_met")],
               wardrobe=[{"action": "add", "item_id": "cafe_uniform_normal"}])]),
    ]})

# ── step 1 · Tom B 1 · the apron ──
out.append({
    "id": "tom_01_the_apron", "name": "The apron",
    "description": "Tom step 1 (Tom B 1), her first shift: he reties her apron. Both answers count. Opens from \"Work a shift\" (Q2).",
    "trigger": dict(step_trigger(TM, 1), substitution_only=True),   # Q2: from the shift at the counter (cafe.py)
    "nodes": [
        back("apron"),
        node("apron", "The apron", [
            # scene reader b03 (2026-11-03): cafe_shift can play before this step, so the screen doesn't call it her first shift
            P("Tom hands you a fresh apron at the start of the shift, and when you tie it wrong he catches the strings from behind and stops you. He unties them and ties them again, properly. His knuckles press into your hips."),
            D(TM, "Tables first. Phone in the back. Smile."),
            P("His hands stay on your hips one second longer than tying takes, his thumbs on the curve of your ass. Then he lets go, like a man putting something back on the shelf for later."),   # scene reader b03: the not-yet (H4.3)
        ], [
            go("\"Yes, boss.\"", node="tray", mins=2, wardrobe=[{"action": "equip", "item_id": "cafe_uniform_normal"}]),
            go("\"I can tie my own apron.\"", node="tray", mins=2, eff=[nadd(TM, "power", -5)], wardrobe=[{"action": "equip", "item_id": "cafe_uniform_normal"}]),
        ]),
        node("tray", "Table six", [
            P("You carry the tray out. You can feel his eyes on your ass the whole way across the café, and when you look back at the counter, he's still looking. He doesn't pretend he isn't."),
            D(TM, "Don't run with it. Walk. Let them see you coming."),   # pass 3 B3: his line beside her thought
            ME("Table six, boss. I've got it."),
            D(TM, "Tips go in the jar. I count the jar. See you next shift."),   # scene reader b03: the hook (his step 2 is the tip jar)
            G(cond(trait("corruption", "lt", 20)), T("He's your boss. Do the job.")),
            G(cond(trait("corruption", "gte", 20)), T("You felt that second. So did he.")),
        ], [go("\"Table six.\"", loc="cafe", mins=10, consumes=True,
               eff=[nadd(TM, "want", 10), setv("tom_step", 1)], flags=[done(1)])]),
    ]})

# ── step 3 · Tom B 3 · the tip jar ──
out.append({
    "id": "tom_03_the_tip_jar", "name": "The tip jar",
    "description": "Tom step 2 of 3 (release 1; was Tom B 3): she sees him steal from the tip jar. Sets knows_tip_jar.",
    "trigger": dict(step_trigger(TM, 2, retry_days=3), substitution_only=True),   # Q2: from the shift at the counter (cafe.py)
    "nodes": [
        back("jar"),
        node("jar", "The back room", [
            P("He counts the jar when you're near now, lips moving. Today you go into the back room for milk and he's there with the tip jar on the shelf, folding twenties out of it into his apron pocket. Your twenties. Everybody's."),
        ], [
            go("\"Busy shift?\"", node="seen", mins=2),
            go("Walk past.", loc="cafe", mins=2, retry=3),
        ]),
        node("seen", "Not a word", [
            P("He turns round with his hand still in the jar. He sees you see it. For a second neither of you moves."),
            D(TM, "Not a word."),
            ME("Twenties, Tom? From the girls' jar?"),
            D(TM, "Float. I'm counting the float. Not a word, @player."),
            P("He takes his hand out of the jar slowly and puts the lid back on, and his ears go red."),
            T("He's a thief. And now he owes you."),
        ], [go("\"Not a word.\"", loc="cafe", mins=5, consumes=True,
               eff=[nadd(TM, "want", 5), nadd(TM, "power", -5), setv("tom_step", 2)], flags=[done(3), fset("knows_tip_jar")]),
            # reader batch 5 (pass 3): his ask gets a written no. She saw it either way, so the step is done and she
            # knows; her no moves none of his meters (C1, LO 2026-11-03)
            go("\"That depends what's in it for me.\"", node="seen_no", mins=2)]),
        node("seen_no", "What's in it for you", [
            D(TM, "You want to play it like that? Fine. Out front. Now."),
            P("He puts the lid back on the jar too hard, and he doesn't look at you again for the rest of the shift. His ears are still red."),
        ], [go("Back out front.", loc="cafe", mins=5, consumes=True, eff=[setv("tom_step", 2)], flags=[done(3), fset("knows_tip_jar")])]),
    ]})

# ── step 3 · Not by the window (tom_03b_not_by_the_window.md, signed 2026-11-01), the top step: after a shift she let
#    a customer's hand stay (cafe_let_it, under an hour), at footfall 15 and name -5. ──
_t3 = step_trigger(TM, 3, retry_days=1)
_t3["substitution_only"] = True   # Q2 (LO, 2026-11-04): opens from Tom's hub at the counter (hub_tom_cafe below)
# "this shift": the flag is stamped when the clock-out choice runs, before its 180 minutes pass, so under 4 hours
_t3["conditions"]["items"].append({"type": "hours_since_flag", "subject": "player", "flag_key": "cafe_let_it", "operator": "lt", "value": 3.5})   # false lines a3 #15: "off the floor" = within 30 minutes of clocking out
# Q2 (LO, 2026-11-04): from his hub now, an event to the gates; he watched her let it happen, which pays him (H5)
WINDOW_DONE = dict(eff=[setv("tom_step", 3), nadd(TM, "want", 2)], flags=[fset("tom_window_rule"), fset("tom_03b_done")])
out.append({
    "id": "tom_03_not_by_the_window", "name": "Not by the window",
    "description": "Tom step 3 of 3, the top step (release 1): in the back room after a shift she let a customer touch her. \"Reputation's going. The tables are full.\" \"Not by the window.\" Sets tom_window_rule; his card ends on the locked line.",
    "trigger": _t3,
    "nodes": [
        node("back", "The back room", [
            P("When you come off the floor Tom is in the back room, leaning on the shelf by the tip jar, and he shuts the door behind you."),
            P("Your ass still burns where the man had you, and your face is hot with it."),
            D(TM, "Reputation's going. People talk. And the tables are full."),
            P("He doesn't sound angry. He sounds like he's done the sums. His eyes drop to your ass, once, and he drags them back up to your face."),
        ], [
            go("\"Say it, Tom.\"", node="line", mins=2),
            go("\"Not now, Tom.\"", loc="cafe", mins=2, retry=1),
        ]),
        node("line", "The window", [
            D(TM, "I'm not stopping you. I saw, but I didn't stop it."),
            P("He looks at the door, at the front of the café behind it, the big window on the street."),
            D(TM, "Not by the window."),
        ], [
            go("\"Then where?\"", node="where", mins=2),
            go("\"Yes, boss.\"", node="yes", mins=1),
            go("\"It's my tips.\"", node="tips", mins=1),
        ]),
        node("where", "Where", [
            D(TM, "Anywhere the street can't see. That's all I'm saying."),
            G(cond(trait("corruption", "lt", 20)), T("Say sorry. Keep the job.")),
            G(cond(trait("corruption", "gte", 20)), T("He watched, but he didn't stop it.")),
        ], [go("\"Okay.\"", loc="cafe", mins=2, consumes=True, **WINDOW_DONE)]),
        node("yes", "Yes, boss", [
            P("Tom nods once, and opens the door for you, and doesn't look at you while you go past him."),
        ], [go("Back to the floor.", loc="cafe", mins=2, consumes=True, **WINDOW_DONE)]),
        node("tips", "My tips", [
            D(TM, "Then keep them, but not by the window."),
            P("His ears go red, the way they did at the tip jar."),
        ], [go("Back to the floor.", loc="cafe", mins=2, consumes=True,
               eff=WINDOW_DONE["eff"] + [nadd(TM, "power", -3)], flags=WINDOW_DONE["flags"])]),
    ]})

# ── his hub: the café, all his hours ──
out.append({
    "id": "hub_tom_cafe", "name": "Tom",
    "description": "Tom's hub at the café. His Want and Power colour the lines; his lines read her uniform.",
    # The counter is the open café, 08:00-22:00. The café stays open till 23:00 for his closing hour
    # (LO, 2026-10-29), and that hour's face is after close; this hub would take it (priority 6 over 5).
    "trigger": {"location": "cafe", "npc": TM, "requires_npc": TM, "is_repeatable": True, "priority": 6,
                "is_active": True, "conditions": cond(flag("tom_met"), tod("08:00", "22:00")),
                # Q2 (LO, 2026-11-04): his top step opens from him, after the shift, not on entry
                "substitutions": [on_activity("tom_03_not_by_the_window", flag("cafe_job"))]},
    "nodes": [
        node("counter", "The counter", [
            P("Tom's behind the counter with a cloth over his shoulder, keeping an eye on the room and an eye on you."),
            # Iteration 002, part 8 (reader): the work lines only while she's in the uniform.
            G(cond(UNIFORM, tod("08:00", "22:00")), POOL(D(TM, "Table three wants you, @player."), D(TM, "Smile. Table three's waiting."), D(TM, "Two lattes for six. Go."),
                 D(TM, "I'm the manager, @player, not the help. Table three."), pid="tom_counter_lines")),
            G(cond({"type": "worn_type", "operator": "neq", "value": "cafe_uniform"}), D(TM, "Day off? Then you're a customer. Sit where I can see you.")),
            # release 1, strict (tom_01_the_apron.md, his counter): he never tells her to show
            G(cond(UNIFORM, {"type": "clothing_item", "item_id": "cafe_uniform_sexy", "operator": "equipped"}), P("He looks once, at your tits in it, and makes himself look at the till."), D(TM, "Your choice. Tables don't wait.")),   # reader a3 #59 (DECISIONS 131)
            G(cond(UNIFORM, {"type": "clothing_item", "item_id": "cafe_uniform_normal", "operator": "equipped"}),
              P("He reties your apron from behind on his way past. His knuckles brush your ass. He takes his hand back fast, like the knot burned him."), D(TM, "Tables first.")),
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, UNIFORM), D(TM, "Apron on. Keep it on.")),
            G(cond(trait("tom_step", "eq", 1), {"type": "worn_type", "operator": "eq", "value": "cafe_uniform"}), P("His eyes are on your apron strings again.")),
            G(cond(trait("tom_step", "eq", 1)), P("He counts the tip jar when you're near.")),
            G(cond(trait("tom_step", "eq", 2)), P("He won't look at the tip jar when you're near. Or at you.")),
            G(cond(trait("tom_step", "eq", 3)), P("He watches the room now, and you in it, but he doesn't say a word about the window.")),
            G(cond(ntrait(TM, "want", "gte", 50), UNIFORM, tod("08:00", "22:00")), P("He watches you the whole shift. He doesn't even pretend to watch the room.")),
            G(cond(ntrait(TM, "power", "lt", 40)), P("He asks you now. He used to tell you.")),
            G(cond(ntrait(TM, "power", "gte", 60)), P("He tells you where to stand, and expects you to do it.")),
            # after 22:00 the café is shut and Tom is closing up (his 22:00-23:00 row): no work lines (part 10, reader)
            G(cond(tod("22:00", "23:00")), P("The sign's turned to CLOSED. Tom's putting the chairs up on the tables.")),
        ], [go("Back to work.", loc="cafe", mins=30, cond_=cond(UNIFORM, tod("08:00", "21:30"))),
            # a build addition (release 1): with the uniform rule cut, asking is the only way to the tight top; her choice
            go("Ask for the tight dress.", node="tight", mins=2,
               cond_=cond(trait("exhibitionism", "gte", 20), {"type": "clothing_item", "item_id": "cafe_uniform_sexy", "operator": "not_owned"}, tod("08:00", "22:00"))),
            go("Sit at the counter a while.", loc="cafe", mins=20, cond_=cond({"type": "worn_type", "operator": "neq", "value": "cafe_uniform"}, tod("08:00", "21:30"))),
            go("Leave him to the till.", loc="town")]),
        node("tight", "The tight dress", [
            P("Tom reaches under the counter without a word and puts it on the counter between you: the black dress, tighter than the other one and cut for your tits. His eyes go to your chest once. He makes them go back to the till."),
            D(TM, "Your choice. They tip more for it. They grab more too."),
        ], [go("Take it.", loc="cafe", mins=3, flags=[fset("uniform_sexy")], wardrobe=[{"action": "add", "item_id": "cafe_uniform_sexy"}]),
            # reader a3 #51 (DECISIONS 131): the written no. No pay: it's the uniform she turns down, not him.
            go("Leave it on the counter.", node="leave_it", mins=1)]),
        node("leave_it", "Not the dress", [D(TM, "Your call."), P("He folds it back under the counter without looking at it, or at you.")],
             [go("Leave him to his folding.", loc="cafe", mins=1)]),
    ]})

# ── Gary's hub (booth four, his hours) ──
out.append({
    "id": "hub_gary_booth", "name": "Gary, booth four",
    "description": "Gary in booth four: his look, his tea.",
    "trigger": {"location": "cafe", "npc": GY, "requires_npc": GY, "is_repeatable": True, "priority": 6,
                "is_active": True, "conditions": cond(flag("gary_met"))},
    "nodes": [
        node("booth", "Booth four", [
            P("Gary in booth four with his paper and his pot of black tea. He lowers the paper when you come near, an inch at a time."),
            POOL(D(GY, "There she is. Top me up, doll."), D(GY, "Slow day. I could use the company."), D(GY, "You look lovely today. You always look lovely."), pid="gary_lines"),
            # (release 1: Gary's paid ten minutes are cut, DECISIONS 117)
        ], [go("Top up his tea.", node="poured", mins=10, flags=[fset("served_gary")]),   # read by Tom's palm line (part 9)
            # reader batch 4 (pass 3): his ask gets a written no
            go("\"Pour your own, Gary.\"", node="no", mins=2)]),
        # pass 3 D44 (the-surfaces.md R9): his look when she pours, not a toast
        node("poured", "His tea", [
            P("You bend over the booth to pour, slow, and Gary looks straight down the front of you at your tits the whole time the pot is tipped. He wets his lip. He doesn't pretend to read."),
            P("His hands stay flat on the paper. For now."),
            # reader batch 4 (pass 3): what comes next is his hand on her on shift (cafe_shift L3, Gary in booth four)
            D(GY, "Lovely. Lovely, doll. Pour like that when you're on shift, and see what an old man does about it."),
        ], [go("Take the pot back to the counter.", loc="cafe")]),
        node("no", "Pour your own", [
            D(GY, "Hard-hearted, doll. Hard-hearted."),
            P("He laughs into his paper, but his eyes follow your ass all the way back to the counter."),
        ], [go("Leave him to his paper.", loc="cafe")]),
    ]})

cards = step_cards(TM, {
    1: ("Tom gave you the job. Your first shift is waiting.", "Take a shift at the café, afternoon or evening, Monday to Saturday"),
    2: ("He counts the tip jar when you're near.", "Five shifts in: a café shift, watch the back room"),
    3: ("He watches the customers' hands. He wants a word.", "A café shift after you let a customer's hand stay"),
}, met_flag="tom_met", terminal_text=("The window rule: the street can't see.", "Tom, later. (Next release) His Want and Power still count: what you do at the café now is kept for the next release."))
# His hiring card under People until she has the job (LO 2026-11-02, "Yes all three"): only the "Week one" story
# card named the job, and it goes after 7 days, so a player who skipped it lost Tom, Gary and the shift money.
cards.insert(0, {"npc_id": TM, "priority": 10, "heading": "The café", "text": "The café in town is hiring.",   # C3 (LO 2026-11-03)
                 "tip": "The café in town, Monday to Saturday, 8 AM to 11 PM",
                 "when": [{"flag": "opening_done", "op": "is_true"}, {"flag": "tom_met", "op": "is_false"}],   # C3: the met flag
                 "ready_canvas": "cafe_job_ask"})

text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · TOM (sheets/scenes/tom_0*.md, cafe_gary_ten_minutes.md, people/npc_tom.md)\n"
        "# The job ask, steps 1-6, the Friday repeat, Gary's ten minutes, his and Gary's hubs, his cards.\n"
        "# =============================================================================\n")
# Iteration 002, part 3: leaving this outing after 22:00 sets late_shift and came_home_late (Q69,
# the street sheet "Why she's late"; canv.mark_late). Each is read for 4 hours; her bed clears them.
for _c in out:
    if _c["id"] in ['tom_06_after_close_kiss', 'tom_after_close']:
        mark_late(_c, 'late_shift', split=False)

# (Iteration 002, part 7: no presence check on Gary here. Tom B 4 is where she meets him, and his row
# waits for gary_met, so a check made the step unreachable: found by reach_all.py.)
# Showing up after close clears her "i'll stay" (phone.py tom_close, DECISIONS 87).
for _c in out:
    if _c["id"] == "tom_after_close":
        clear_on_leave(_c, "tom_close_booked")
# heat proposal B9 (DECISIONS 147 chunk 3): Gary's booth reads his walk-in
import walkins_out
walkins_out.hub_read(out)
text += "".join(emit(c) for c in out) + "".join(emit_card(c) for c in cards)
open(__import__("sys").argv[1], "w").write(text)
print("tom:", len(out), "canvases,", len(cards), "cards")
