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
CLOCK_IN = [{"action": "equip", "item_id": "cafe_uniform_normal"}, {"action": "equip", "item_id": "cafe_uniform_sexy"}]

def back(next_node):
    """She changes in the back room: the uniform is equipped before any screen names it."""
    return node("back", "The back room", [
        P("Tom looks up from the till as you come in."),
        D(TM, "Uniform, @player. Back room."),
        P("You change in the back room in front of the staff mirror, between the mop bucket and the crates of milk."),
    ], [go("Clock in.", node=next_node, mins=5, wardrobe=CLOCK_IN)])

# ── the job ask: meets Tom, the job, the uniform ──
out.append({
    "id": "cafe_job_ask", "name": "Ask about the job",
    "description": "Meets Tom: the sign in the window. Sets cafe_job and tom_met; adds the café uniform.",
    "trigger": {"location": "cafe", "requires_npc": TM, "is_repeatable": False, "priority": 10, "is_active": True,
                "schedules": [{"weekdays": [0, 1, 2, 3, 4, 5], "start_time": "08:00", "end_time": "23:00"}],
                "conditions": cond(flag("opening_done"), flag("cafe_job", False))},
    "nodes": [
        node("sign", "STAFF WANTED", [
            IMG("scenes/cafe_job_ask.jpg", "a small cafe counter, a man in his thirties with rolled sleeves behind an espresso machine, a staff wanted sign in the window",
                "cafe manager behind counter espresso machine", "small cafe interior staff wanted sign"),
            P("There's a card taped inside the café window: STAFF WANTED, NO EXPERIENCE NEEDED. Behind the counter a man in his thirties with his sleeves rolled up is wiping the espresso machine. The manager. Tom, says the badge. He looks you over before you've opened your mouth, top to bottom, the way you'd look at something you were thinking of buying."),
            D(TM, "You're here about the sign."),
            ME("I can start today. I need the money."),
            D(TM, "Everybody needs the money. Eight a shift, plus tips. Regulars tip the pretty ones, so you'll do fine."),
            T("He said pretty like it's part of the job description. Maybe it is."),
        ], [go("\"When do I start?\"", node="uniform", mins=5)]),
        node("uniform", "The uniform", [
            P("He reaches under the counter and pushes a folded uniform across to you: a black dress with a white apron, the café's name stitched on the pocket."),
            D(TM, "Eight till seven, up to three shifts a day, Monday to Saturday. Wear that. Be on time. Smile at booth four."),
            G(cond(flag("college_for_fun")), D(TM, "You look like you like a good time. Customers like that.")),
        ], [go("Take the uniform.", loc="cafe", mins=5, flags=[fset("cafe_job"), fset("tom_met")],
               wardrobe=[{"action": "add", "item_id": "cafe_uniform_normal"}])]),
    ]})

# ── step 1 · Tom B 1 · the apron ──
out.append({
    "id": "tom_01_the_apron", "name": "The apron",
    "description": "Tom step 1 (Tom B 1), her first shift: he reties her apron. Both answers count.",
    "trigger": step_trigger(TM, 1),
    "nodes": [
        back("apron"),
        node("apron", "The apron", [
            P("Your first tray of the shift. You're halfway to table six when Tom catches your apron strings from behind and stops you. He unties them and ties them again, tighter, his knuckles pressing into your hips through the uniform."),
            D(TM, "Like that. You want it to show your waist."),
            P("His hands stay on you one second longer than tying takes."),
        ], [
            go("\"Then I'll be pretty.\"", node="tray", mins=2),
            go("\"I can tie my own apron.\"", node="tray", mins=2, eff=[nadd(TM, "power", -5)]),
        ]),
        node("tray", "Table six", [
            D(TM, "Regulars tip the pretty ones."),
            P("You carry the tray out. You can feel his eyes on your ass the whole way across the café, and when you look back at the counter, he's still looking. He doesn't pretend he isn't."),
            G(cond(trait("corruption", "lt", 20)), T("Pretty is worth money here. Is that all you are to him? A tip?")),
            G(cond(trait("corruption", "gte", 20)), T("Pretty is worth money here. You can do pretty.")),
        ], [go("\"Table six.\"", loc="cafe", mins=10, consumes=True,
               eff=[nadd(TM, "want", 10), setv("tom_step", 1)], flags=[done(1)])]),
    ]})

# ── step 2 · Tom B 2 · the uniform rule (Gary introduced) ──
out.append({
    "id": "tom_02_uniform_rule", "name": "The uniform rule",
    "description": "Tom step 2 (Tom B 2): the sexy uniform, top button open. Gary lowers his paper (her paid climb is introduced). Adds cafe_uniform_sexy; sets uniform_sexy.",
    "trigger": step_trigger(TM, 2, retry_days=7),
    "nodes": [
        back("rule"),
        node("rule", "Top button", [
            P("Tom's been watching your apron strings since your first shift. Today he waits until you're behind the counter and hands you something folded: a black top, tighter than the dress, with a row of little buttons."),
            D(TM, "Wear this one. Top button stays open. House rule."),
        ], [
            go("\"Is this the uniform, or your idea?\"", node="both", mins=2),
            go("\"No.\"", node="no", mins=2),
        ]),
        node("both", "Both", [
            D(TM, "Both."),
            P("He doesn't smile when he says it. You go to the back and put it on. It's tight across your chest, and with the top button open you can see the shadow between your tits in the staff mirror."),
        ], [go("\"Fine.\"", node="gary", mins=5, flags=[fset("uniform_sexy")],
               wardrobe=[{"action": "add", "item_id": "cafe_uniform_sexy"}, {"action": "equip", "item_id": "cafe_uniform_sexy"}])]),
        node("gary", "Booth four", [
            # Iteration 002, part 8 (reader): booth four is Gary only at his hours; at other hours a regular at the window.
            G(cond(here(GY, "cafe")),
              P("Booth four is an older man in reading glasses with a newspaper and a pot of black tea, the same booth, the same tea. When you lean over to pour, he lowers the paper an inch, and then another inch, and doesn't raise it again until you've straightened up."),
              P("He leaves a tip under the saucer twice what anyone else leaves.")),
            G(cond(here(GY, "cafe", False)),
              P("A man at the window table, a regular, lowers his paper an inch when you lean over to pour, and then another inch, and doesn't raise it again until you've straightened up."),
              P("He leaves a tip under the saucer twice what anyone else leaves.")),
            G(cond(ntrait(TM, "power", "gte", 50)), D(TM, "Told you. That top tips big.")),
            G(cond(ntrait(TM, "power", "lt", 50)), D(TM, "See? It works. Don't let it go to your head.")),
            T("Double, for an inch of skin. Your face is hot. You're counting it anyway."),
        ], [go("\"Back to work.\"", loc="cafe", mins=10, consumes=True,
               eff=[nadd(TM, "want", 10), add("exhibitionism", 3), setv("tom_step", 2)], flags=[done(2)])]),
        no_node("no", [D(TM, "Your call. Tips stay low, then."), P("He takes the top back and drops it under the counter where you can see it, every shift.")],
                "cafe", 7, eff=[nadd(TM, "power", -2)]),
    ]})

# ── step 3 · Tom B 3 · the tip jar ──
out.append({
    "id": "tom_03_the_tip_jar", "name": "The tip jar",
    "description": "Tom step 3 (Tom B 3): she sees him steal from the tip jar. Sets knows_tip_jar.",
    "trigger": step_trigger(TM, 3),
    "nodes": [
        back("jar"),
        node("jar", "The back room", [
            P("He counts the jar when you're near now, lips moving. Today you go into the back room for milk and he's there with the tip jar on the shelf, folding twenties out of it into his apron pocket. Your twenties. Everybody's."),
        ], [
            go("\"Busy night?\"", node="seen", mins=2),
            go("Walk past.", loc="cafe", mins=2, retry=3),
        ]),
        node("seen", "Not a word", [
            P("He turns round with his hand still in the jar. He sees you see it. For a second neither of you moves."),
            D(TM, "Not a word."),
            P("He takes his hand out of the jar slowly and puts the lid back on, and his ears go red."),
            T("He's a thief. And now he owes you."),
        ], [go("\"Not a word.\"", loc="cafe", mins=5, consumes=True,
               eff=[nadd(TM, "want", 10), nadd(TM, "power", -5), setv("tom_step", 3)], flags=[done(3), fset("knows_tip_jar")])]),
    ]})

# ── step 4 · Tom B 4 · booth four (the voice sample; the first time on the paid route) ──
out.append({
    "id": "tom_04_booth_four", "name": "Booth four",
    "description": "Tom step 4 (Tom B 4), the voice sample: Gary's ten minutes, $20, Tom takes half. The first time on her paid route. Meets Gary; opens gary_ten_minutes_open.",
    "trigger": step_trigger(TM, 4),
    "nodes": [
        back("counter"),
        node("counter", "Twenty, half is mine", [
            P("Tom leans on the counter beside you and keeps his voice low. \"Gary wants company. Ten minutes. Sit.\" He tips his head at booth four. Gary is already watching you, a folded twenty on his saucer. \"Twenty for ten minutes. Half is mine.\" Tom says the price slowly, because he likes saying it. His eyes drop down your uniform. \"He just wants a look at your tits up close, @player. Easy money.\" Your face goes hot. You want the ten, but you don't want Gary's eyes on you for ten minutes. *You could just say no. So why haven't you?* Gary taps the bill, and both men wait for you."),
        ], [
            go("Sit with him.", node="booth", mins=2, flags=[fset("gary_met")]),
            go("\"Not today.\"", node="no", mins=2),
        ]),
        node("booth", "Booth four", [
            P("You slide into booth four. Not across from Gary, but beside him. The twenty sits folded on his saucer. Gary doesn't pretend to look anywhere else. His eyes drop to your tits, then climb back to your mouth. \"Ten minutes, sweetheart.\" His voice has gone thick. Your face burns, because you know exactly what that twenty buys. You hesitate, then you say it out loud. \"Ten minutes. Hands where I can see them.\" At the counter, Tom is drying a glass that is already dry. He hasn't looked away once. Under the table, Gary's warm palm settles on your bare knee. The clock starts."),
        ], [go("\"Ten minutes.\"", node="ten", mins=2)]),
        node("ten", "Ten minutes", [
            P("Gary's hand finds your bare knee under the table, warm and heavy. Then it slides up your thigh, slow, and his thumb starts to stroke. His eyes are on your tits. He tries to look at your face, but they drop back every time. \"You've no idea what you do to me, sweetheart,\" he says, low. He shifts in the booth so you see it. His cock is hard in his slacks, a thick ridge pressing the cloth. Your nipples tighten under your uniform, and he sees it. His other hand stays flat on the table, where you told him to keep it. Behind him, Tom watches from the counter. You let the hand stay. You're shaky, and more turned on than you expected. Gary checks his watch with his breath short and his hand still squeezing your thigh."),
            VID("in a cafe booth an older man's hand on a waitress's bare thigh under the table, he stares at her chest", "older man hand on waitress thigh cafe booth", "cafe booth hand up thigh under table waitress uniform", file="sex/tom_04_ten_t4.webm"),
        ], [
            go("\"Time.\"", node="after", mins=10, eff=[add("corruption", 3), nadd(TM, "want", 10)]),
            go("\"That's enough, Gary.\"", loc="cafe", mins=5, consumes=True,
               eff=[{"targetType": "player", "trait": "money", "op": "add", "value": 5, "clamp": False}, add("corruption", 3), nadd(TM, "want", 10), setv("tom_step", 4)],
               flags=[done(4), fset("gary_ten_minutes_open")]),
        ]),
        node("after", "Half", [
            P("Gary leaves the twenty on the saucer, and a wink. You fold the note small before anyone sees it. At the counter, Tom holds out his hand. He doesn't say a word. You give him ten. He pockets it and grins like he did the work. \"Nice, @player. Easy money.\" *Ten for letting a man touch your thigh. And you'd do it again.* *But Tom taking half already feels wrong. He never sat in that booth.* His palm stays open on the counter, like it will be there every time."),
            D(GY, "Thursday, sweetheart. Same booth."),
        ], [go("\"Back to work.\"", loc="cafe", mins=5, consumes=True,
               eff=[{"targetType": "player", "trait": "money", "op": "add", "value": 10, "clamp": False}, setv("tom_step", 4)],
               flags=[done(4), fset("gary_ten_minutes_open")])]),
        node("no", "Not today", [
            P("\"Not today, Tom.\" He shrugs. \"Your call, @player. Offer stands.\" Then he gives booth four to the other server, and that is the price. You're angry, but you knew it would cost something. You watch her laugh at Gary's jokes. You watch the big tip go into her hand instead of yours. Gary never looks at her. His eyes follow you across the room."),
        ], [go("\"Back to work.\"", loc="cafe", mins=5, retry=1)]),
    ]})

# ── step 5 · Tom B 5 · half is mine ──
out.append({
    "id": "tom_05_half_is_mine", "name": "Half is mine",
    "description": "Tom step 5 (Tom B 5): she names her terms; the tip jar is hers to tell about. Tom's Power -10.",
    "trigger": step_trigger(TM, 5),
    "nodes": [
        back("half"),
        node("half", "His hand out", [
            P("In the back room, between orders, Tom holds his hand out. He does that now. Palm up, waiting, every time Gary's been in, like it's rent."),
            D(TM, "Half's mine."),
        ], [
            go("\"Half's yours till I name the price.\"", node="jar", mins=3),
            go("\"Fine.\"", loc="cafe", mins=2, retry=3),
        ]),
        node("jar", "The jar", [
            ME("And the jar's mine to tell about."),
            P("He stops smiling. He looks at the shelf where the tip jar sits, and back at you, and he closes his hand."),
            D(TM, "You've got a mouth on you, @player."),
            ME("You hired it."),
            T("He's not the one setting the price any more. Not for long."),
        ], [go("\"Goodnight, Tom.\"", loc="cafe", mins=5, consumes=True,
               eff=[nadd(TM, "want", 10), nadd(TM, "power", -10), setv("tom_step", 5)], flags=[done(5)])]),
    ]})

# ── step 6 · Tom B 6 · after close ──
out.append({
    "id": "tom_06_after_close_kiss", "name": "After close",
    "description": "Tom step 6 (Tom B 6): the blinds down, the first kiss by the machine, a late regular at the glass.",
    "trigger": step_trigger(TM, 6),
    "nodes": [
        back("blinds"),
        node("blinds", "The blinds", [
            P("Friday, closing time. The last customer goes and Tom flips the sign and pulls the blinds down one by one, slowly, and the café goes dim and private. Then he comes up behind you at the counter and reties your apron, and when it's tied his hands stay on your hips."),
            D(TM, "Stay a minute."),
        ], [
            go("\"Don't stop.\"", node="kiss", mins=5),
            go("\"Night, Tom.\"", node="no", mins=2),
        ]),
        node("kiss", "The machine", [
            P("He turns you round and backs you into the espresso machine and kisses you. His mouth is hot and tastes of coffee. The steam wand is warm behind your back and his hands slide down from your hips to your ass and pull you against him, and he's hard through his jeans, and you kiss him back like you meant to stay."),
        ], [go("Keep kissing him.", node="glass", mins=10, eff=[add("corruption", 3), nadd(TM, "want", 10)])]),
        node("glass", "We're closed", [
            P("Somebody taps on the glass. A late regular, peering in through the gap in the blinds. Neither of you breaks off."),
            ME("We're closed."),
            P("Tom laughs into your mouth. The regular goes."),
            T("Somebody saw. You didn't care. That's new."),
            D(TM, "Friday. After close. Same again."),
        ], [go("\"Goodnight.\"", loc="street", mins=10, consumes=True,
               eff=[setv("tom_step", 6)], flags=[done(6)])]),
        no_node("no", [D(TM, "Friday, then."), P("He lets go of your hips one finger at a time and unlocks the door for you.")], "street", 2, eff=[nadd(TM, "want", 2)]),
    ]})

# ── the repeat: the kiss after close, Friday only (tom_06 sheet; DECISIONS 2) ──
out.append({
    "id": "tom_after_close", "name": "Stay after close",
    "description": "The repeat after Tom step 6: Friday close, the blinds down, the kiss by the machine. Not explicit in 0.1. Once a Friday.",
    "trigger": {"location": "cafe", "npc": TM, "requires_npc": TM, "is_repeatable": True, "priority": 5, "is_active": True,
                "max_triggers_per_day": 1,
                "schedules": [{"weekdays": [4], "start_time": "22:00", "end_time": "23:00"}],
                "conditions": cond(trait("tom_step", "eq", 6))},
    "nodes": [
        node("close", "After close", [
            POOL(
                P("Tom pulls the blinds down one by one while you wipe the last table. When he's done he doesn't say anything. He just holds his hand out, and this time it isn't for money."),
                P("The sign goes to CLOSED. Tom puts the radio on low and leans on the counter, watching you, until you put the cloth down and come to him."),
                pid="tom_close_open"),
            P("He kisses you against the espresso machine, his hands on your hips and then lower, pulling you in. He's hard against you. He groans when you push back into it, and his hands tighten on your ass, and that's as far as he takes it, every time, like the counter's a line he drew."),
            G(cond(ntrait(TM, "power", "lt", 40)), D(TM, "You set the price, @player. What does this cost me?")),
            G(cond(ntrait(TM, "power", "gte", 40)), D(TM, "Same time next Friday.")),
            G(cond(flag("knows_tip_jar")), P("A late regular walks past the window, slows, and keeps walking. Tom doesn't pull the blind any lower.")),
        ], [
            go("Kiss him till the radio's done.", loc="street", mins=40,
               eff=[{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 59}, nadd(TM, "want", 2)]),
            go("\"Night, Tom.\"", node="night", mins=5),
        ]),
        node("night", "Night", [
            D(TM, "Go on, then. Friday."),
            P("He's sulking a little. He'll ask twice next week."),
            P("He unlocks the door for you and stands in it watching you go up the street."),
        ], [go("Walk home.", loc="street", mins=5, eff=[nadd(TM, "want", 1)])]),
    ]})

# ── Gary's ten minutes: the paid repeat (cafe_gary_ten_minutes sheet; two voices by her Corruption) ──
out.append({
    "id": "cafe_gary_ten_minutes", "name": "Booth four: Gary's ten minutes",
    "description": "The café's paid repeat after Tom step 4: $20, Tom takes half. Two voices: reluctant (Corruption 40-49), eager (50+). A stop exit for half. Once a shift-day.",
    "trigger": {"location": "cafe", "requires_npc": GY, "is_repeatable": True, "priority": 5, "is_active": True,
                "max_triggers_per_day": 1,
                "schedules": [{"weekdays": [0, 1, 2, 3, 4], "start_time": "14:30", "end_time": "18:00"}],
                "conditions": cond(flag("gary_ten_minutes_open"), trait("corruption", "gte", 40), UNIFORM)},
    "nodes": [
        node("ask", "Gary's in", [
            D(TM, "Gary's in. Twenty for ten minutes. Half's mine."),
            P("Gary's already looking over his paper at you."),
        ], [
            go("Sit with him.", node="ten", mins=2),
            go("\"No.\"", node="no", mins=2),
        ]),
        node("no", "No", [D("npc_gary", "Another time, sweetheart."), P("He goes back behind his paper. Tom shrugs at the till and gives booth four to the other girl.")],
             [go("Back to work.", loc="cafe", mins=2, eff=[nadd(TM, "power", -1)])]),
        node("ten", "Ten minutes", [
            G(cond(trait("corruption", "lt", 50)),
              P("Gary pats the seat in booth four. \"Ten minutes, sweetheart.\" You sit down stiffly and start counting. His hand lands on your bare thigh under the table, warm and heavy. His other hand stays flat on the tabletop, where your rule keeps it. His eyes drop to your tits and stay there. His cock is hard in his slacks, pressed against your hip. You don't want it, but your nipples tighten against your uniform. His thumb strokes your thigh, and your nipples stiffen harder under his stare.")),
            G(cond(trait("corruption", "gte", 50)),
              P("You take Gary's hand and put it on your bare thigh yourself. You slide closer in booth four and lean in slow, so your tits push at your uniform under his nose. His cock strains his slacks. You smile at it. Your nipples are hard, and he stares at them. \"Sweetheart,\" he breathes. His other hand lifts off the table, but you tap it back down. His palm creeps up your thigh. You stop it at the very top with your own hand, and his cock jerks against his slacks.")),
            VID("an older man's hand on a waitress's thigh in a cafe booth, her uniform tight, his erection visible", "waitress older man booth hand on thigh", "cafe regular touching waitress thigh under table", pool_dir="sex/cafe_gary_ten_t4"),
        ], [
            go("\"Time.\"", node="after", mins=10,
               eff=[{"targetType": "player", "trait": "money", "op": "add", "value": 10, "clamp": False},
                    {"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 59}]),
            go("\"That's enough, Gary.\"", loc="cafe", mins=5,
               eff=[{"targetType": "player", "trait": "money", "op": "add", "value": 5, "clamp": False}]),
        ]),
        node("after", "Time", [P("Gary checks his watch and sighs and folds the twenty under the saucer for you. At the counter Tom's palm is open, and the girl on the other till is staring at you like she's doing sums."),
                               D(GY, "Same booth Thursday, sweetheart.")],
             [go("Back to work.", loc="cafe", mins=2)]),
    ]})

# ── his hub: the café, all his hours ──
out.append({
    "id": "hub_tom_cafe", "name": "Tom",
    "description": "Tom's hub at the café. His Want and Power colour the lines; his lines read her uniform.",
    "trigger": {"location": "cafe", "npc": TM, "requires_npc": TM, "is_repeatable": True, "priority": 6,
                "is_active": True, "conditions": cond(flag("tom_met"))},
    "nodes": [
        node("counter", "The counter", [
            P("Tom's behind the counter with a cloth over his shoulder, keeping an eye on the room and an eye on you."),
            # Iteration 002, part 8 (reader): the work lines only while she's in the uniform.
            G(cond(UNIFORM, tod("08:00", "22:00")), POOL(D(TM, "Table three wants you, @player."), D(TM, "Smile. It's worth money."), D(TM, "Two lattes for six. Go."), pid="tom_counter_lines")),
            G(cond({"type": "worn_type", "operator": "neq", "value": "cafe_uniform"}), D(TM, "Day off? Then you're a customer. Sit where I can see you.")),
            G(cond(UNIFORM, {"type": "clothing_item", "item_id": "cafe_uniform_sexy", "operator": "equipped"}), D(TM, "Top button stays open. House rule.")),
            G(cond(UNIFORM, {"type": "clothing_item", "item_id": "cafe_uniform_normal", "operator": "equipped"}),
              P("He reties your apron from behind on his way past."), D(TM, "Regulars tip the pretty ones.")),
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, UNIFORM,
                   {"type": "npc_at_location", "location_id": "cafe", "npc_id": GY, "operator": "is_present"}), D(TM, "Booth four's going to tip big today.")),
            G(cond(trait("tom_step", "eq", 1), {"type": "worn_type", "operator": "eq", "value": "cafe_uniform"}), P("His eyes are on your apron strings again.")),
            G(cond(trait("tom_step", "eq", 2)), P("He counts the tip jar when you're near.")),
            G(cond(trait("tom_step", "eq", 3)), D(TM, "Gary asks about you, you know. Every day.")),
            G(cond(trait("tom_step", "eq", 4), UNIFORM, flag("served_gary"), {"type": "hours_since_flag", "subject": "player", "flag_key": "served_gary", "operator": "lt", "value": 1}), P("His palm is already open on the counter when you come out of booth four.")),
            G(cond(trait("tom_step", "eq", 5)), D(TM, "Stay late Friday?")),
            G(cond(ntrait(TM, "want", "gte", 50), UNIFORM, tod("08:00", "22:00")), P("He watches you the whole shift. He doesn't even pretend to watch the room.")),
            G(cond(ntrait(TM, "power", "lt", 40)), P("He asks you now. He used to tell you.")),
            G(cond(ntrait(TM, "power", "gte", 60)), P("He tells you where to stand and how to lean, and expects you to do it.")),
            # after 22:00 the café is shut and Tom is closing up (his 22:00-23:00 row): no work lines (part 10, reader)
            G(cond(tod("22:00", "23:00")), P("The sign's turned to CLOSED. Tom's putting the chairs up on the tables.")),
        ], [go("Back to work.", loc="cafe", mins=30, cond_=cond(UNIFORM, tod("08:00", "21:30"))),
            go("Sit at the counter a while.", loc="cafe", mins=20, cond_=cond({"type": "worn_type", "operator": "neq", "value": "cafe_uniform"}, tod("08:00", "21:30"))),
            go("Go.", loc="town")]),
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
            POOL(D(GY, "There she is. Top me up, sweetheart."), D(GY, "Slow day. I could use the company."), D(GY, "You look lovely today. You always look lovely."), pid="gary_lines"),
            G(cond(flag("gary_ten_minutes_open"), trait("corruption", "gte", 40), UNIFORM, wd(0, 1, 2, 3, 4), tod("14:30", "18:00")), P("He pats the seat beside him in the booth and leaves his hand there, palm up."), D(GY, "Ten minutes, when you've got them.")),
        ], [go("Top up his tea.", loc="cafe", mins=10, flags=[fset("served_gary")])]),   # read by Tom's palm line (part 9)
    ]})

cards = step_cards(TM, {
    1: ("Tom gave you the job. Your first shift is waiting.", "Take a shift at the café, afternoon or evening, Monday to Saturday"),
    2: ("He watches your apron strings. He has a new rule.", "A café shift, afternoon or evening (Daring)"),
    3: ("He counts the tip jar when you're near.", "A café shift: watch the back room (Daring)"),
    4: ("\"Gary asks about you.\" Booth four, weekday afternoons.", "A weekday afternoon shift, Gary in booth four (Bold)"),
    5: ("His hand's out for half, every time.", "A café shift, afterwards in the back room (Bold)"),
    6: ("\"Stay late Friday?\"", "Stay at the café after close on a Friday night"),
}, met_flag="tom_met", terminal_text=("Fridays after close: the blinds, the machine, his hands.", "Tom's next step comes in a later release."))

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
text += "".join(emit(c) for c in out) + "".join(emit_card(c) for c in cards)
open(__import__("sys").argv[1], "w").write(text)
print("tom:", len(out), "canvases,", len(cards), "cards")
