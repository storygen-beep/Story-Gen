"""Mark — steps 1-9 (Mark A 1-9), the Sunday table (the repeat), Vance's knock, the twist's
offer, his hubs. Source: sheets/scenes/mark_0*.md, sheets/people/npc_mark.md,
sheets/systems/money_pressure.md. Explicit screens pasted as signed."""
import os
from canv import *
from tomlw import tod, wd

M = "npc_mark"
V = "npc_vance"
out = []
HERE = os.path.dirname(os.path.abspath(__file__))

def done(n):
    return fset(f"mark_0{n}_done")

HIS = ntrait(M, "power", "gte", 50)   # his version (M)
HERS = ntrait(M, "power", "lt", 50)   # her version (E)
SHORT = flag("rent_short")
FULL_ITEMS = [flag("rent_short", False), flag("ryan_covered", False), flag("mark_money_week", False)]
BROKEN = cond(flag("rent_short"), flag("ryan_covered"), flag("mark_money_week"), logic="OR")
SLEEP_SHIRT = {"type": "worn_type", "operator": "eq", "value": "sleep_shirt"}
# Bare legs (LO, 2026-10-08, Q72): shorts, a skirt, the sleep shirt, a dress, or nothing below,
# which is every outfit without jeans or leggings.
BARE_LEGS = [{"type": "clothing_item", "item_id": "jeans", "operator": "unequipped"},
             {"type": "clothing_item", "item_id": "leggings", "operator": "unequipped"}]
NOT_LATE = flag("came_home_late", False)
LAURA_IN_BED = {"type": "npc_at_location", "location_id": "home_master_bedroom", "npc_id": "npc_laura", "operator": "is_present"}   # "your mother sleeps" upstairs: she is in her bed, not on the stairs   # on a late night Laura is on the stairs, not asleep
COUNT_CLEAR = [funset("ryan_covered"), funset("mark_money_week"), fset("sunday_counted_today"), funset("grades_seen")]

def count_exits(text, dest, mins, eff=(), flags=(), consumes=False, node_=None):
    """The Sunday count's three exits: a clean Sunday adds to the streak (the fourth sets
    pays_her_own_way); a carried Sunday, Ryan's money or Mark's money breaks it."""
    kw = dict(mins=mins, consumes=consumes)
    if node_:
        kw["node"] = node_
    else:
        kw["loc"] = dest
    base_f = list(flags) + COUNT_CLEAR
    return [
        go(text, cond_=cond(*FULL_ITEMS, trait("paid_full_streak", "lt", 3)),
           eff=list(eff) + [add("paid_full_streak", 1, clamp=False), nadd(M, "power", -3)], flags=base_f + PAID_BACK, **kw),
        go(text, cond_=cond(*FULL_ITEMS, trait("paid_full_streak", "gte", 3)),
           eff=list(eff) + [add("paid_full_streak", 1, clamp=False), nadd(M, "power", -3)],
           flags=base_f + PAID_BACK + [fset("pays_her_own_way")], **kw),
        go(text, cond_=BROKEN, eff=list(eff) + [setv("paid_full_streak", 0), nadd(M, "power", 3)], flags=base_f, **kw),
    ]

# ── what a short Sunday costs, and paying it back (rent_short.md, money_pressure.md; DECISIONS 121) ──
HELD = ["short_skirt", "thin_top", "sports_bra"]           # the fixed order Mark takes them in
HELD_NAME = {"short_skirt": "short skirt", "thin_top": "sheer blouse", "sports_bra": "sports bra"}
CHANGE_INTO = {"short_skirt": "jeans", "thin_top": "tshirt", "sports_bra": "plain_bra"}   # what she changes into when he takes the one she has on
PAID_BACK = [funset("her_door_unlocked")] + [funset(f"garage_holds_{i}") for i in HELD]
# One set per canvas (one pool, one place): the Sunday table keeps the first words; each step has its own.
PAYBACK_WORDS = {
    "table": ("Key.", "He slides your door key across the table without looking at it.", "The {}'s on the nail. Take it."),
    "first": ("You're square. Here's your door key.", "He flicks it at you across the table with one finger, and his eyes stay on your legs.", "You're square. Go and get that {} off the nail."),
    "shorts": ("Paid up, so your key.", "He drops it by your hand on the table and looks at your thighs, not at it.", "That {} is off the tab. Take it down from the nail yourself."),
}
def payback_lines(which):
    said, done_, nail = PAYBACK_WORDS[which]
    return [
        G(cond(*FULL_ITEMS, flag("her_door_unlocked")), D(M, said), P(done_)),
        *[G(cond(*FULL_ITEMS, flag(f"garage_holds_{i}")), D(M, nail.format(HELD_NAME[i]))) for i in HELD],
    ]
# (reader fix, 2026-11-01) read before the count adds this Sunday, so a full Sunday says the streak it is about to
# make, and a carried or covered Sunday says nothing
STREAK_WORDS = {
    "table": ("One Sunday paid your way. He writes a small 1 on the back of the envelope and doesn't say anything about it.",
              "Two Sundays in a row, your own money. He notices, but he doesn't like noticing.",
              "Sunday after Sunday, all of it, from your own pocket. He looks at the envelope like he's hoping it's wrong."),
    "first": ("A whole Sunday paid with your own money. He pencils a small 1 in the corner of the envelope, and his mouth stays shut.",
              "That's twice running, from your own pocket. He looks at the pencil in his hand like it let him down.",
              "Week after week, every dollar yours. He presses the flap down with his thumb like he could make it come out short."),
    "shorts": ("It's all there this week, your own money. He writes a small 1 on the flap, and his eyes don't leave your thighs to do it.",
               "Twice running, and none of it his. He sees that, and he looks at your thighs instead so he doesn't have to.",
               "Another Sunday, all of it yours. He weighs the envelope in his palm and looks sorry it isn't lighter."),
}
def streak_lines(which):
    one, two, more = STREAK_WORDS[which]
    return [
        G(cond(*FULL_ITEMS, trait("paid_full_streak", "eq", 0)), P(one)),
        G(cond(*FULL_ITEMS, trait("paid_full_streak", "eq", 1)), P(two)),
        G(cond(*FULL_ITEMS, trait("paid_full_streak", "gte", 2)), P(more)),
    ]

# ── step 1 · Mark A 1 · count it slowly ──
out.append({
    "id": "mark_01_count_it_slowly", "name": "Count it slowly",
    "description": "Mark step 1 (Mark A 1), her first Sunday at the table. The rent page took the money; this is Mark at his table with it and her there, not a second count (LO, 2026-11-04, Q6). Reads rent_short. Counts the Sunday for the streak.",
    "trigger": step_trigger(M, 1),
    "nodes": [
        node("table", "The kitchen table", [
            IMG("scenes/mark_01_table.jpg", "a man in his forties at a kitchen table with an envelope of cash and a coffee, Sunday morning light",
                "man counting cash kitchen table morning", "stepfather kitchen table envelope of money"),
            P("Mark is at the kitchen table with the envelope of rent in front of him and a coffee going cold. Sunday. Laura's out shopping."),
            G(cond(*BARE_LEGS), P("He looks up, and his eyes go straight to your bare legs, and stay.")),
            G(cond({"type": "clothing_item", "item_id": "jeans", "operator": "equipped"}), P("He looks up, and his eyes go down your legs in your jeans, and stay.")),
            G(cond({"type": "clothing_item", "item_id": "leggings", "operator": "equipped"}), P("He looks up, and his eyes go down your legs in your leggings, and stay.")),
            G(cond(SLEEP_SHIRT), P("You came in your sleep shirt. It stops mid-thigh. He watches the hem the whole way to the table.")),
            D(M, "Sit. Every Sunday, you sit at my table while this goes in Vance's envelope. That way nobody says I took more than I did."),
        ], [
            go("\"Here.\"", node="count", mins=5),
            go("\"Give me a minute.\"", node="dressed", mins=5, wardrobe=[REMEMBER] + DRESS_BACK),   # reader 2026-11-04: true in jeans too, where she is dressed already
        ]),
        # LO, 2026-11-04 (Q6): the rent page has already taken the money, so nobody counts it twice; he makes her
        # sit with the envelope instead, and looks at her, not at it
        node("count", "The envelope", [
            G(cond(SHORT),
              P("He doesn't open the envelope. He doesn't need to. You're short and you both know it, and he makes you sit there and look at it with him, the way he'd make you sit through every bill."),
              D(M, "All of it, I said.")),
            G(cond(flag("rent_short", False)),
              P("You lean back in the chair. It's all in there, every bill, and he knows it."),
              ME("It's all there, Mark. Take your time."),
              P("He looks up. He doesn't like your tone, but he takes his time anyway, and his eyes keep leaving the envelope for your legs.")),
        ], [
            go("\"Can you just — say it?\"", node="short", mins=3, cond_=cond(SHORT)),
            go("Let him look.", node="short", mins=3, cond_=cond(flag("rent_short", False))),
        ]),
        node("short", "The week", [
            # reader 2026-11-04: "I'm saying it" answers her "say it" on the short branch only; on the paid one she chose "Let him look."
            G(cond(SHORT), D(M, "I'm saying it."), P("He writes the gap on the back of the envelope in pencil and taps it twice."), D(M, "The rest waits a week, but Vance doesn't.")),
            G(cond(flag("rent_short", False)), P("You let him. His eyes go down your legs, slow, and he doesn't hurry coming back."), D(M, "That's the week. Same again Sunday.")),
            G(cond(SLEEP_SHIRT), D(M, "And not the shirt, next time.")),
            *streak_lines("first"), *payback_lines("first"),
            T("He looked at you longer than he ever looked at the money."),
        ], count_exits("\"Fine.\"", "home_hall", 5, eff=[nadd(M, "want", 10), setv("mark_step", 1)], flags=[done(1)], consumes=True)),
        node("dressed", "Suit yourself", [
            D(M, "Suit yourself."),
            P("You go out and come back dressed. He's sealed the envelope without you. He pushes it at you to look at, and doesn't look at you at all."),
            G(cond(SHORT), D(M, "Short. The rest waits a week.")),
        ], count_exits("Go back to your room.", "home_ella_room", 15, eff=[setv("mark_step", 1)], flags=[done(1)], consumes=True)),
    ]})

# ── step 2 · Mark A 2 · the late notice ──
out.append({
    "id": "mark_02_late_notice", "name": "Find Mark's late notice",   # pass 3 H33/H34 (the-voice.md R1, D11): the name says what happens if she clicks, and never hides the act
    "description": "Mark step 2 (Mark A 2), the kitchen drawer late at night, Mark on the phone next door. She learns his debt to Vance. Sets knows_mark_debt.",
    "trigger": step_trigger(M, 2, bind_npc=False),
    "nodes": [
        node("drawer", "The drawer", [
            P("You go to the kitchen for water in the dark. The drawer by the fridge is open an inch, the way it never is. Under the takeaway menus there's a letter on thick paper, Vance's name printed at the top. LATE NOTICE, it says. And under it, a number with a lot of zeros."),
            P("Through the wall you can hear Mark in the living room, the TV low, his voice lower."),
        ], [
            go("Read it.", node="phone", mins=3, flags=[fset("knows_mark_debt")]),
            go("Shut the drawer.", loc="home_kitchen", mins=1, retry=2),
        ]),
        node("phone", "Friday, Frank", [
            P("You're on the second page when he comes into the doorway with his phone at his ear. He sees you. He sees what's in your hand, but he doesn't hang up."),
            D(M, "Friday, Frank. I'll have it Friday. Yeah. Yeah. Friday."),
            P("He ends the call. He stands there with the phone at his side, looking at you, and for the first time in your life he looks like he's the one who owes."),
        ], [go("\"How late are we?\"", node="put", mins=2)]),
        node("put", "Put it back", [
            D(M, "Put it back."),
            P("He doesn't shout. He doesn't come for it. He just waits for you to fold it along its creases and put it under the menus and shut the drawer."),   # reader 2026-11-04: she has not done it yet; "No." below takes it from her hand
            T("He knows you know. You've got something on him now."),
        ], [go("\"Okay.\"", loc="home_kitchen", mins=3, consumes=True,
               eff=[nadd(M, "want", 10), setv("mark_step", 2)], flags=[done(2)]),
            # reader batch 5 (pass 3): his ask gets a written no. She has read it either way, so the step is done; her
            # no moves no Want (C1, LO 2026-11-03)
            go("\"No. I want to know how bad it is.\"", node="put_no", mins=2)]),
        node("put_no", "You know enough", [
            D(M, "You know enough."),
            P("He takes it out of your hand, folds it along its creases himself, puts it under the menus and shuts the drawer with his hip. Then he goes back to his TV without another word."),
        ], [go("Go back to bed.", loc="home_ella_room", mins=3, consumes=True, eff=[setv("mark_step", 2)], flags=[done(2)])]),
    ]})

# ── step 3 · Mark A 3 · shorts ──
SHORTS_ON = [{"action": "equip", "item_id": "tshirt"}, {"action": "equip", "item_id": "sleep_shorts"}]
out.append({
    "id": "mark_03_shorts", "name": "Shorts",
    "description": "Mark step 3 (Mark A 3), Sunday at the table: his dress rule. His version (Power 50+) asks; hers comes down in them first. The scene equips her sleep shorts. Sets mark_dress_rule.",
    "trigger": step_trigger(M, 3),
    "nodes": [
        node("start", "Sunday", [
            G(cond(HIS),
              P("Mark doesn't look up from the envelope when you come in."),
              D(M, "Shorts this time. Since you're reading my mail now."),
              P("When you sit, his eyes go down your legs under the table.")),   # reader a3 #16 (DECISIONS 131)
            G(cond(HERS, trait("exhibitionism", "gte", 20)),
              P("Sunday. Mark's at the table with the envelope. His eyes go down your legs and stay, and he's working up to asking for something. You've got a pair of sleep shorts that would save him the asking.")),
            # under Daring she waits, and he asks (reader: the screen promised an act she could not take)
            G(cond(HERS, trait("exhibitionism", "lt", 20)),
              P("Sunday. Mark's at the table with the envelope. He looks you up and down, slow."), D(M, "Shorts next time. You know the ones."),
              P("His eyes go down your legs under the table.")),   # reader a3 #16 (DECISIONS 131)
            # her voice at her level: being looked at, so Exhibitionism; the step has no floor on it
            G(cond(trait("exhibitionism", "lt", 20)), T("Shorts. At his table, with him looking. Your face burns just thinking about it.")),
            G(cond(trait("exhibitionism", "gte", 20), trait("exhibitionism", "lt", 40)), T("You wonder how long he'd look, if you wore them. You wonder what his face would do.")),
            G(cond(trait("exhibitionism", "gte", 40), trait("exhibitionism", "lt", 60)), T("He wants your legs at his table? Fine. Make him work to keep his eyes on that envelope.")),
            G(cond(trait("exhibitionism", "gte", 60)), T("You want his eyes on your ass all morning. You want him asking for it out loud.")),
        ], [
            go("\"Fine.\"", node="shorts", mins=5, cond_=cond(HIS, trait("exhibitionism", "gte", 20)), wardrobe=SHORTS_ON, eff=[nadd(M, "power", 3)]),   # her show: Daring (DECISIONS 124)
            go("\"I'm not changing for you.\"", node="no", mins=2, cond_=cond(HIS)),
            go("Go and change.", node="hers_down", mins=5, cond_=cond(HERS, trait("exhibitionism", "gte", 20)), wardrobe=SHORTS_ON),
            go("\"I'm not changing for you.\"", node="no", mins=2, cond_=cond(HERS)),   # her version has a no too (reader)   # her chosen show: Daring (DECISIONS 124)
        ]),
        # Iteration 002, part 8 (reader): the shorts are on her before the screen names them.
        node("hers_down", "Saved you asking", [
            P("You come back in the shortest thing you own to sleep in, the pair that shows the curve of your ass when you walk. Mark looks up and stops with his coffee halfway to his mouth."),
            ME("Saved you asking."),
        ], [go("Sit down across from him.", node="shorts", mins=2, eff=[nadd(M, "power", -3)])]),
        node("shorts", "His eyes go slow", [
            P("You sit. The chair is cold on the backs of your thighs. When you lean over to push the envelope at him, the shorts ride up and you feel his eyes go down the curve of your ass and stay there."),
            P("He doesn't touch the envelope. He picks his pen up and puts it down again, twice, and his eyes go back to your thighs every time."),
            D(M, "Every Sunday. Like that."),
            *streak_lines("shorts"), *payback_lines("shorts"),
        ], count_exits("\"Eyes up, Mark.\"", "home_hall", 10,
                       eff=[nadd(M, "want", 10), add("exhibitionism", 3, cap=79), setv("mark_step", 3)],
                       flags=[done(3), fset("mark_dress_rule")], consumes=True)),
        no_node("no", [D(M, "Suit yourself."), P("He keeps his eyes on the envelope and not on you, and writes something on the back of it that you don't get to see."), G(cond(SHORT), D(M, "Then the short stays on the tab, @player."))],
                "home_hall", 7, eff=[nadd(M, "power", -2)], label="Leave him to his envelope."),   # pass 3 D39 (R7)
    ]})

# ── step 6 · Mark A 6 · our arrangement ──
out.append({
    "id": "mark_06_our_arrangement", "name": "Our arrangement",
    "description": "Mark step 4 of 4, the top step (release 1): the garage; he saw her come out of Ryan's room; each holds the other's secret. Sets mark_arrangement.",
    "trigger": step_trigger(M, 4, retry_days=3),
    "nodes": [
        node("start", "The garage", [
            P("Mark's at his workbench with the radio on and his hands black with oil. He hears you come in and doesn't turn round."),
            D(M, "I saw you come out of Ryan's room. Late."),   # reader 2026-11-04: his step 4 can end by 22:20, so not "middle of the night"
            G(cond(HIS), D(M, "Our arrangement. Your mother has enough to worry about. We understand each other.")),
            G(cond(HERS), ME("Vance's letter is in the drawer. So we each keep one.")),
        ], [
            go("\"Vance's letter is in the drawer.\"", node="keep", mins=5, cond_=cond(HIS), eff=[nadd(M, "power", -3)]),
            go("\"There's no arrangement.\"", node="no", mins=2, cond_=cond(HIS)),
            go("Wait for him to answer.", node="keep", mins=5, cond_=cond(HERS)),
        ]),
        node("keep", "We each keep one", [
            P("He wipes his hands on a rag, slowly, one finger at a time, and then he nods. Just once."),
            D(M, "Our arrangement."),
            # her voice at her level: this step comes after Ryan's step 4 (Corruption 40), so Bold and Hungry only
            G(cond(trait("corruption", "lt", 60)), ME("Look at my legs all you want on Sundays, Mark. Just remember whose letter's in that drawer."),
              P("His eyes go down your thighs anyway, and the rag stops moving in his hand.")),
            G(cond(trait("corruption", "gte", 60)), ME("You saw me come out of his room and you've thought about it ever since. Tell me what you pictured."),
              P("He looks at your tits, then at your mouth. The rag twists in his fist, and the front of his jeans has gone tight.")),
            T("Your secret for his. He thinks it's even, but it isn't."),
            G(cond(flag("rent_starts")), D(M, "Sunday morning. The rent, at my table. Don't be late.")),   # reader pass 3 b01: the hook; the Sunday count reads mark_arrangement
        ], [go("\"Deal.\"", loc="home_hall", mins=3, consumes=True,
               eff=[nadd(M, "want", 10), setv("mark_step", 4)], flags=[done(6), fset("mark_arrangement")])]),
        no_node("no", [D(M, "There is now, @player. Since Ryan's door."), P("He turns back to the bench. The radio fills the garage. You leave him to it, and your face is hot all the way down the hall.")],
                "home_hall", 3, eff=[nadd(M, "power", 2)], label="Leave him to the radio."),   # pass 3 D39 (R7)
    ]})

# ── the twist's offer, after goal 1 (DIRECTION §2 · money sheet: the answer stays parked) ──
out.append({
    "id": "debt_offer", "name": "How far behind",
    "description": "The twist's offer after goal 1 (pays_her_own_way): she learns how far the house is behind with Vance. Sets debt_offer_seen. Her answer stays parked until 0.2.",
    "trigger": {"location": "home_kitchen", "npc": M, "requires_npc": M, "is_repeatable": False,
                "priority": 11, "is_active": True, "consume_on": "exit", "retry_after_days": 7,
                "schedules": [{"weekdays": [6], "start_time": "08:00", "end_time": "22:00"},
                              {"weekdays": [2], "start_time": "18:00", "end_time": "22:00"}],
                "conditions": cond(flag("pays_her_own_way"), flag("debt_offer_seen", False))},
    "nodes": [
        node("letters", "The letters", [
            P("Mark has every letter out of the drawer, spread across the kitchen table in a fan. Vance's name on all of them. He doesn't hide them when you come in."),
            G(cond(flag("knows_mark_debt")), P("He hasn't hidden anything from you for a while.")),
            D(M, "You pay your way now. So you get to see what your way pays into."),
            P("He turns the last one round so you can read it. It isn't the rent. It's everything on top of the rent: years of short months and loans from the man who owns the house, and the number at the bottom is bigger than anything you've ever seen written down."),
            D(M, "Vance could put us out any month he likes. He knows it. I know it. Now you know it."),
            T("Your rent every week is a drop in that. And he's asking you something without asking."),
        ], [
            go("\"Let me think about it.\"", loc="home_kitchen", mins=10, retry=7, flags=[fset("debt_offer_seen")]),
            go("\"It's not my debt, Mark.\"", node="refuse", mins=5),
        ]),
        no_node("refuse", [D(M, "No. It's not."), P("He gathers the letters into a pile and squares the edges against the table, one by one, and doesn't look at you."), D(M, "Rent's Sunday. Same as ever.")],
                "home_kitchen", 14, eff=[nadd(M, "power", 3)], flags=[fset("debt_offer_seen"), fset("debt_refused")],
                label="\"Sunday, then.\""),   # pass 3 D39 (R7)
    ]})

# ── the Sunday table: the repeat (mark_09 sheet; money sheet: the count, his terms or hers) ──
HERS_LOOK = open(os.path.join(HERE, "beat_mark_table_look_hers.txt")).read().strip() if os.path.exists(os.path.join(HERE, "beat_mark_table_look_hers.txt")) else "PLACEHOLDER"
BOLD_HIS = open(os.path.join(HERE, "beat_mark_table_look_his_bold.txt")).read().strip()
BOLD_HERS = open(os.path.join(HERE, "beat_mark_table_look_hers_bold.txt")).read().strip()
out.append({
    "id": "mark_sunday_table", "name": "Sit down at the table",
    "description": "The Sunday table, the repeat after Mark's step 1, after the rent page has taken the money (no second count, LO 2026-11-04, Q6): his terms or hers by his Power; the streak counts here when no step has counted it. From Bold, after his step 7: \"Twenty, and you can look\", two voices, a stop exit. Once a Sunday.",
    "trigger": {"location": "home_kitchen", "requires_npc": M, "is_repeatable": True, "priority": 5,
                "is_active": True, "max_triggers_per_day": 1,
                # truth pass (2026-11-03): opens to 11:45, so the count's 15 minutes end before noon and "He doesn't
                # say good morning" (the counted screen's bag) is still morning
                "schedules": [{"weekdays": [6], "start_time": "08:00", "end_time": "11:45"}],
                "conditions": cond(trait("mark_step", "gte", 1), flag("sunday_counted_today", False), flag("rent_starts"))},
    "nodes": [
        node("table", "The Sunday table", [
            G(cond(HIS), P("Mark's at the table with the envelope, the way he is every Sunday, but he doesn't say good morning. He points at the chair across from him with his pen."),
              D(M, "Sit. My table, my Sunday.")),
            G(cond(HERS), P("Mark's at the table with the envelope. He's on his feet, and he doesn't sit back down until you've sat."),
              D(M, "Morning. Go on, then.")),
            G(cond(flag("mark_dress_rule"), {"type": "worn_type", "operator": "eq", "value": "shorts"}),
              P("You're in the shorts. His rule. His eyes go down your bare thighs to where the hem cuts into them, and he forgets his coffee.")),   # scene reader b02: the look lands on her body
            G(cond(flag("mark_dress_rule"), {"type": "worn_type", "operator": "neq", "value": "shorts"}),
              D(M, "That's not what I asked you to wear to my table.")),
            G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), D(M, "That's what you wear to my table?")),
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "worn_exposure", "operator": "eq", "value": 0}),
              P("With no bra your nipples push at the cloth, and his eyes go straight to them."), D(M, "Sit down, for God's sake.")),
            G(cond({"type": "worn_exposure", "operator": "eq", "value": 1}, {"type": "worn_type", "operator": "neq", "value": "towel"}, {"type": "worn_type", "operator": "neq", "value": "sleep_shirt"}),
              D(M, "Your mother's out."), P("His eyes go down to your tits and stay there while he talks. He doesn't tell you to cover up."),
              T("He'd have his hands on them if you let him. Not yet. Not at his table.")),
            G(cond(flag("mark_arrangement", False), SHORT), P("It's short. He writes the gap on the envelope in pencil, slow, and taps it twice without a word.")),
            G(cond(flag("mark_arrangement"), SHORT), P("It's short, and he writes the gap on the envelope in pencil without a word.")),
            G(cond(flag("mark_arrangement", False), flag("rent_short", False)), P("It's all there, and he knows it. He keeps the envelope in front of him anyway, because he wants to sit here longer.")),
            *streak_lines("table"), *payback_lines("table"),
            D(M, "Next Sunday. Same table."),
        ], count_exits("Sit down across from him.", None, 15, eff=[nadd(M, "want", 2)], node_="counted")),
        node("counted", "Sunday", [
            P("He squares up the envelope with Vance's name on it and leaves his hand flat on top of it."),   # reader 2026-11-04: a Sunday at $0 has no rent to fold
            # after his step 4, the arrangement (mark_sunday_table.md, signed 2026-11-01): normal speed, his eyes on
            # her, a new line a week from a shuffle bag of five
            G(cond(flag("mark_arrangement")), P("He doesn't open the envelope, and his eyes don't go to the money once."),
              POOL(P("He slides the envelope across to you to check, and keeps his fingers on it a second after you've taken it."),
                   P("He says your name, once, and then nothing at all."),
                   P("He puts the pencil behind his ear and looks at you instead of writing anything down."),
                   P("He licks his thumb to open the envelope, and stops, and leaves it shut."),
                   P("When you stand up he watches you all the way to the door. He doesn't pretend he isn't."),
                   pid="mark_table_after", bag=True)),
        ], [
            go("Leave him to his envelope.", loc="home_kitchen", mins=2),
        ]),
    ]})

# ── the three short Sundays (rent_short.md, signed 2026-11-01, DECISIONS 121): on the Sunday morning, before the
#    count (priority 7 over the table's 5). rent_carried is stamped at Sunday 00:00, so "under 12 hours" is this morning. ──
THIS_SHORT = [SHORT, {"type": "hours_since_flag", "subject": "player", "flag_key": "rent_short", "operator": "lt", "value": 12}]
def short_trigger(extra, repeat=False):
    t = {"location": "home_kitchen", "npc": M, "requires_npc": M, "is_repeatable": repeat, "priority": 7, "is_active": True,
         "schedules": [{"weekdays": [6], "start_time": "08:00", "end_time": "12:00"}],
         "conditions": cond(*THIS_SHORT, *extra)}
    if repeat:
        t["max_triggers_per_day"] = 1
    return t

out.append({
    "id": "rent_short_1", "name": "The key",
    "description": "The first short Sunday: Mark takes her bedroom-door key until she's paid up (her_door_unlocked).",
    "trigger": short_trigger([trait("rent_short_weeks", "eq", 1)]),
    "nodes": [node("key", "The key", [
        P("Mark doesn't open the envelope. He knows it's short, and he puts it down on the table between you."),   # Q6: no second count
        D(M, "Then it's owed. Vance doesn't wait, so I don't."),
        P("He holds out his hand, palm up."),
        D(M, "That old key in your bedroom door. Hand it over. You get it back when you're square."),
        T("It's the only key there is. Anyone can open your door now. Anyone in this house."),
    ], [go("\"Here.\"", loc="home_kitchen", mins=5, flags=[fset("her_door_unlocked")], eff=[nadd(M, "power", 5)])])]})

out.append({
    "id": "rent_short_2", "name": "The late fee",
    "description": "The second short Sunday: Vance charges late, $15 on next Sunday's rent (rent_late_fee, the engine adds it to the due).",
    "trigger": short_trigger([trait("rent_short_weeks", "eq", 2)]),
    "nodes": [node("fee", "Fifteen", [
        D(M, "Twice now. Vance comes round tomorrow night, and Vance charges late. Fifteen."),
        P("He writes it on the envelope under the rest, in pencil, and underlines it."),
        D(M, "That's yours, not mine."),
    ], [go("\"How much?\"", loc="home_kitchen", mins=5, eff=[add("rent_late_fee", 15, clamp=False), nadd(M, "power", 5)])])]})

def _take_cases():
    """Mark takes the first of HELD she owns and he doesn't already hold; flat cases, since a condition
    can't nest (v2.py triggerConditionsSatisfied): every earlier item is either not owned or already held."""
    import itertools
    cases = []
    for k, item in enumerate(HELD):
        here = [{"type": "clothing_item", "item_id": item, "operator": "owned"}, flag(f"garage_holds_{item}", False)]
        for gone in itertools.product(*[[("not_owned", e), ("held", e)] for e in HELD[:k]]):
            items = list(here)
            for why, e in gone:
                items.append({"type": "clothing_item", "item_id": e, "operator": "not_owned"} if why == "not_owned" else flag(f"garage_holds_{e}"))
            cases.append((item, items))
    return cases

TAKE_LINES, TAKE_EXITS = [], []
for item, items in _take_cases():
    nm = HELD_NAME[item]
    TAKE_LINES.append(G(cond(*items, {"type": "clothing_item", "item_id": item, "operator": "unequipped"}),
        P(f"He doesn't shout. He gets up, goes down the hall, and comes back with the {nm} over his arm. The one you bought.")))
    TAKE_LINES.append(G(cond(*items, {"type": "clothing_item", "item_id": item, "operator": "equipped"}),
        P(f"He doesn't shout. He holds his hand out across the table for the {nm} you've got on, and waits until you go and change and put it in his hand. The one you bought.")))
    TAKE_LINES.append(G(cond(*items),
        D(M, "Garage. On the table, then you get it back."),
        P("Through the kitchen window you watch him hang it on the nail by his workbench, where you'll see it every time you walk past.")))
    # pass 4 reader (true on every visit): worn, she "goes and changes", so the exit puts her plain one on in its
    # place (CHANGE_INTO); not worn, nothing she has on moves
    for worn in ("equipped", "unequipped"):
        TAKE_EXITS.append(go("\"That's mine.\"", loc="home_kitchen", mins=5,
                             cond_=cond(*items, {"type": "clothing_item", "item_id": item, "operator": worn}),
                             flags=[fset(f"garage_holds_{item}")],
                             wardrobe=[{"action": "unequip", "item_id": item}] + ([{"action": "equip", "item_id": CHANGE_INTO[item]}] if worn == "equipped" else []),
                             eff=[nadd(M, "power", 5)]))
import itertools as _it
# nothing left to take: every item either not owned or already held (2^3 flat cases)
NOTHING_CASES = [[{"type": "clothing_item", "item_id": i, "operator": "not_owned"} if w == "n" else flag(f"garage_holds_{i}")
                  for i, w in zip(HELD, ws)] for ws in _it.product("nh", repeat=len(HELD))]
out.append({
    "id": "rent_short_3", "name": "The garage",
    "description": "The third short Sunday and every one after: Mark takes one thing she bought (skirt, sheer blouse, sports bra, in that order) and keeps it in the garage until she's paid up. The garment's own conditions lock it in her wardrobe.",
    "trigger": short_trigger([trait("rent_short_weeks", "gte", 3)], repeat=True),
    "nodes": [node("take", "Three times", [
        G(cond(trait("rent_short_weeks", "eq", 3)), D(M, "Three times.")),
        G(cond(trait("rent_short_weeks", "gte", 4)), D(M, "Again.")),
        *TAKE_LINES,
        *[G(cond(*nc), P("He looks you over like he's pricing you, and finds nothing of yours left to take."), D(M, "Next week, then. On top."))
          for nc in NOTHING_CASES],
    ], TAKE_EXITS + [go("\"Next week.\"", loc="home_kitchen", mins=5, cond_=cond(*nc), eff=[nadd(M, "power", 5)])
                     for nc in NOTHING_CASES])]})

# ── Vance's knock after a short Sunday (money sheet: the next evening; once per carried week) ──
out.append({
    "id": "vance_knock", "name": "Answer the door",
    "description": "Vance at the front door the evening after a short Sunday. Reads rent_short (set every short Sunday, cleared by a full payment: engine 8da4e050); Vance's Power +10 (each carried Sunday). At Power 60 he asks for her, not Mark.",
    # His row (ledger L23): the front door, Monday 18:00-19:00, the evening after a short Sunday. His face is
    # here; rent_short is read for 48 hours. The engine restamps it every short Sunday and clears it on a full
    # payment, so a missed knock no longer leaves her "short" for good (alignment pass 2, J44; 2026-11-03).
    "trigger": {"location": "home_front_door", "npc": V, "requires_npc": V, "is_repeatable": True, "priority": 6, "is_active": True,
                "schedules": [{"weekdays": [0], "start_time": "18:00", "end_time": "19:00"}],
                "conditions": cond(flag("rent_short"), {"type": "hours_since_flag", "subject": "player", "flag_key": "rent_short",
                                                          "operator": "lt", "value": 48}, flag("vance_met")), "max_triggers_per_day": 1},
    "nodes": [
        node("knock", "Vance", [
            P("Three knocks, slow and heavy, the way a man knocks on a door he owns. Mr. Vance is on the step in his cardigan, with an envelope in his hand."),
            G(cond(ntrait(V, "power", "lt", 60)),
              D(V, "Evening, Miss. Is your step-father in? Tell him I came by about Sunday. He'll know."),
              P("He hands you the envelope. His fingers stay on it a second after yours close.")),
            G(cond(ntrait(V, "power", "gte", 60)),
              D(V, "I didn't come for Mark. I came for you, Miss. You're the one who pays in that house now, aren't you?"),
              P("He looks past you into the hall, then back at you, slow: your legs, your chest, all the way down and up. He wets his lips."),   # copy fix A18 (DECISIONS 125)
              D(V, "Come and see me one evening. We'll talk about what's owed.")),
            G(cond(ntrait(V, "want", "gte", 30)), P("He doesn't look at your face once while he says it.")),
            G(cond(trait("rent_late_fee", "gt", 0)), D(V, "Fifteen on top, Miss. That's how it works.")),
            T("A short week, and it comes to the door."),
        ], [
            go("\"Mark will pay.\" Close the door.", node="shut", mins=5, eff=[nadd(V, "power", 10)]),
            go("\"Maybe one evening.\"", node="maybe", mins=5, cond_=cond(ntrait(V, "power", "gte", 60)),
               eff=[nadd(V, "power", 10), nadd(V, "want", 3)]),
        ]),
        node("shut", "The door", [D(V, "He'd better, Miss."), P("He touches the brim of a hat he isn't wearing and goes back down the path, slow. You lock the door. Through the glass you watch him stop on his own porch and look back.")],
             [go("Go back in.", loc="home_hall", mins=3)]),
        node("maybe", "One evening", [D(V, "Maybe's a start."), P("He smiles like you've signed something, and goes.")],
             [go("Go back in.", loc="home_hall", mins=3)]),
    ]})

# ── his hubs: the living room late, the garage, the kitchen, their bed ──
# Iteration 002, part 2: his home_life items are choices here (npc_mark.md:96-113; home_life.md).
# The plain line of each is the sheet's; the tease and the paid look are placeholders (LO, 2026-10-09).
# The paid look: money +20, his Want +1, Exhibitionism +1, one a day across all his items
# (`mark_paid_look`, 12 hours); no amount on the button (D11).
from home_items import *
MS = "sheets/people/npc_mark.md"
MARK_PAID_ROUTE = [flag("mark_paid_touch"), flag("mark_arrangement")]
L = "npc_laura"
R = "npc_ryan"
def m_tease(line, what, label="Let him look.", bold=False):
    # DECISIONS 124 (H2): his teases follow his accident (mark_00_the_dryer); a touch needs Bold
    return {"label": label, "ref": f"{MS}:{line}", "gate": [BOLD if bold else CURIOUS, trait("mark_step", "gte", 3), flag("mark_saw_her")],
            "eff": [want(M)], "what": f"Mark, {what}: tease (Curious, Mark A 3)"}
def m_paid(line, what, label="Let him pay to look."):
    return None   # release 1: Mark's paid look is cut (npc_mark.md, "Cut": no money for her body)
def _m_paid_cut(line, what, label="Let him pay to look."):
    # Writer fix pass (LO, 2026-10-10): behind his paid route, the flags his first paid touch (A 5)
    # and the arrangement (A 6) set, as well as the step that makes the price hers (A 7).
    return {"label": label, "ref": f"{MS}:{line}", "gate": [BOLD, trait("mark_step", "gte", 7), *MARK_PAID_ROUTE],
            "eff": [PAY20, want(M), EXH1], "brake": "mark_paid_look", "name": "The paid look",
            "what": f"Mark, {what}: the paid look (Bold, Mark A 7)"}
# One set per room (one pool, one place): the kitchen keeps the first words.
MARK_ROOM_WORDS = {
    "home_kitchen": dict(
        shirt="His thumb works at the edge of whatever he's holding. His eyes are on the hem of your sleep shirt.",
        skirt="That's what you wear in my house?",
        nobra="Sit down. You're making me lose my place.",
        under="You're in your underwear, but he doesn't tell you to cover up.",
        normal="Tips any good? Rent doesn't pay itself.",
        sexy="Where's a waitress get twenties, wearing that?",
        soft="He doesn't give you orders any more. He waits to hear what you want.",
        hard="He looks at you like you're one more thing in this house that's his.",
        wants="He wants you. He's stopped trying to hide it from you, only from her."),
    "home_living_room": dict(
        shirt="The can stops on his knee. His eyes go to the hem of your sleep shirt and stay there.",
        skirt="You sit down in that, I can't be blamed for where I look.",
        nobra="Either sit down or move. I've watched the same play twice.",
        under="You've got nothing on but your underwear, and all he does is turn the TV down.",
        normal="Still dressed for work. Hope it's paying. That envelope's hungry.",
        sexy="They tip you for that dress, or for what falls out of it?",
        soft="He used to give you orders from this couch. Now he shifts over and waits for you to say something.",
        hard="He looks you over from the couch the way he looks over his TV and his beer. Paid for.",
        wants="He wants you. The TV could catch fire and he wouldn't look around."),
    "home_garage": dict(
        shirt="The wrench slows in his hand. His eyes are on the hem of your sleep shirt, and he misses the bolt.",
        skirt="That skirt's got no business in a garage. Stand where I can see it.",
        nobra="Stand over there. I keep dropping the same damn bolt.",
        under="You walk in here in your underwear, and he wipes his hands and says nothing about it.",
        normal="That place paying you yet, or just feeding you?",
        sexy="That's for the customers, is it? Don't get oil on it.",
        soft="He used to bark at you from this bench. Now he puts the wrench down and asks what you need.",
        hard="He looks at you the way he looks at his tools. Every one has its nail, and every one is his.",
        wants="He wants you. His hands have stopped on that engine part, and he isn't even pretending."),
}
def mark_state_lines(loc):
    w = MARK_ROOM_WORDS[loc]
    return [
        G(cond(SLEEP_SHIRT), P(w["shirt"])),
        G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), D(M, w["skirt"])),
        G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "worn_exposure", "operator": "eq", "value": 0}), D(M, w["nobra"])),
        G(cond({"type": "clothing_slot", "slot": "bra", "operator": "equipped"}, {"type": "clothing_slot", "slot": "underwear", "operator": "equipped"},
               {"type": "clothing_slot", "slot": "top", "operator": "unequipped"}, {"type": "clothing_slot", "slot": "bottom", "operator": "unequipped"},
               {"type": "clothing_slot", "slot": "dress", "operator": "unequipped"}),
          P(w["under"])),
        # reader pass 4 b4: Mark is on the couch Sun 22:00-24:00, where "Sunday's coming" was false; no day word, so it is true any day
        G(cond(NORMAL_ON), D(M, w["normal"])),
        G(cond(SEXY_ON), D(M, w["sexy"])),
    ]
LEAKS_LATE = [
    G(cond(trait("mark_step", "eq", 1)), P("His eyes go down your legs and back to the TV, every time you move.")),
    G(cond(trait("mark_step", "eq", 3)), P("He stays up later than he used to.")),
    G(cond(trait("mark_step", "eq", 4)), P("He watches you from the couch the way he watches the game. He doesn't pretend not to.")),
]
LEAKS_GARAGE = [
    # the leak before his step 4 (npc_mark.md, release 1): he can't hold her look
    G(cond(trait("mark_step", "eq", 3)), P("He can't hold your look. He looks at the bench instead.")),
]
LEAKS_KITCHEN = [
    G(cond(trait("mark_step", "eq", 2)), P("His eyes go down your legs and stay, the way they did at the first Sunday table.")),
]
# ── the towel at home (LO, 2026-10-31, DECISIONS 98): his reaction by his Dominance, every visit, in his
#    hub's own bands (<40, 40-59, 60+); "Let it slip." (Daring) pays his Dominance +2 once a day; "Drop it."
#    needs Showing and his top band, no story step (LO, 2026-10-31). Living room and kitchen only (LO:
#    bedroom and garage out). ──
MARK_TOWEL_LEAD = [P("You loosen the tuck and let the towel slip. It drops to your waist before you catch it, and your tits are out in front of him, wet and bare, your nipples hard.")]
MARK_TOWEL_SLIP = [
    [P("Mark looks straight at your tits for one second, then at the wall."), D(M, "Cover yourself. Now."),
     P("You pull the towel back up. He doesn't look at you again until you've gone.")],
    [P("Mark doesn't look away. He looks at your tits like he's pricing them, slow, and his drink stops halfway to his mouth."),
     D(M, "Cover up before your mother sees."), P("He waits until you do. He watches you do it.")],
    [P("Mark looks at your bare tits and leans back."), D(M, "Did I say you could cover up?"),
     P("You hold the towel at your waist with your tits out. He looks for as long as he likes, and your nipples go hard and tight under his eyes.")],
]
MARK_TOWEL_DROP = [
    P("You undo the knot and let the towel drop to the floor. You're naked in his house. Your tits are bare and your nipples are hard. Your cunt is bare. Mark looks at your tits, then down at your cunt, and he takes his time about it. His cock is hard in his jeans, and he doesn't hide it. He puts his drink down."),
    D(M, "Turn round."),
    P("You turn round. You show him your bare ass, wet from the shower, and you hold still while he looks at it."),
    D(M, "Pick it up. Slowly."),
    P("You bend and pick the towel up off the floor with your ass to him, slow, the way he said, and you feel his eyes on your cunt the whole way down."),
]


# reader a3 #5-6 (DECISIONS 131): "Get dressed." after "Come here." / "Stand there." (his Power 60+, her in the towel)
MARK_TOWEL_NO = [
    P("You hitch the towel tighter over your tits and turn for the hall."),
    D(M, "Suit yourself."),
    P("He says it to your back. His eyes stay on the backs of your bare thighs all the way to the door, but he doesn't call you back."),
]


# The kitchen's own towel (one pool, one place): any of his kitchen hours (Sunday all day, Wednesday evening, a
# weekday dinner, Saturday's coffee and keys), so no chair and no drink: he may be on his feet with anything in his hand.
MARK_TOWEL_LEAD_K = [P("You work the tuck loose and the towel falls. You catch it at your waist, and your tits are bare in his kitchen, still dripping, your nipples hard.")]
MARK_TOWEL_SLIP_K = [
    [P("Mark gets one full look at your tits, then he finds something very interesting on the fridge."), D(M, "Towel. Up. Right now."),
     P("You drag it up over your nipples. He keeps his eyes on the fridge until you're out of the room.")],
    [P("Mark stays right where he is. His eyes go over your tits one at a time, like he's checking them for damage, and his hands stop moving."),
     D(M, "Get that up before somebody walks in."), P("He makes you tuck it back yourself, and he watches your fingers the whole way.")],
    [P("Mark folds his arms and takes a good look at your bare tits."), D(M, "Who told you to pull that up?"),
     P("You stay there with the towel bunched at your waist and your tits out, in the middle of the kitchen. He takes all the time he wants, and your nipples ache under it.")],
]
MARK_TOWEL_DROP_K = [
    P("You pull the knot and the towel hits the kitchen floor. You're naked in front of him with your tits bare and your nipples hard, and your cunt is bare too. Mark starts at your tits, goes down to your cunt, and stays there as long as he wants. His cock stands hard against his jeans, and he lets you see it. He sets down whatever he's holding."),
    D(M, "Now the back."),
    P("You turn and give him your bare ass, still wet from the shower, and you don't move while he looks."),
    D(M, "Get it off the floor. Take your time."),
    P("You bend for the towel with your ass aimed at him, slow, the way he told you, and you feel his eyes go right to your cunt as you reach the floor."),
]
MARK_TOWEL_NO_K = [
    P("You grab the towel tighter over your tits and head for the hall."),
    D(M, "Your loss."),
    P("You feel him watching your bare thighs go past the fridge and out the door, but he stays where he is and he doesn't say another word."),
]
MARK_TOWEL_LINES = {
    "home_living_room": [
        [D(M, "Get dressed. This isn't a hotel."),
         GC(cond(TOWEL_ON), P("Mark looks at the towel, then away, hard."), D(M, "Put something on, @player.")),
         D(M, "Your mother lets you walk round like that?")],
        [P("Mark's eyes go down the towel to your thighs and stay there, too long for a step-father."),
         GC(cond(TOWEL_ON), D(M, "That's all you've got on."), P("It isn't a question. He doesn't look away.")),
         P("He looks at you over his drink, slow, from your wet feet to the knot over your tits.")],
        [GC(cond(TOWEL_ON), D(M, "Stand there. Let me look at you."), P("He doesn't tell you to get dressed. He tells you where to stand.")),
         GC(cond(TOWEL_ON), D(M, "Don't you dare go and change."), P("His eyes stay on the knot over your tits.")),
         GC(cond(TOWEL_ON), P("He looks at the towel like it belongs to him, and what's under it too."), D(M, "Come here."))],
    ],
    "home_kitchen": [
        [D(M, "Not in my kitchen. People eat in here."),
         GC(cond(TOWEL_ON), P("Mark sees the towel, and his eyes go straight to the fridge door and stay on it."), D(M, "Clothes, @player. Go on.")),
         D(M, "You drip on that floor, you mop it.")],
        [P("Mark's eyes run down the towel to the wet tops of your thighs and forget to come back. He's your step-father, and he's still looking."),
         GC(cond(TOWEL_ON), D(M, "Nothing under that, is there?"), P("He isn't asking. He's already looking for the answer.")),
         P("He starts at the water running down your shins and takes his time climbing to the tuck between your tits.")],
        [GC(cond(TOWEL_ON), D(M, "Stop there, by the table. I'm not done looking."), P("He doesn't send you to get dressed. He picks the spot and waits for you to stand on it.")),
         GC(cond(TOWEL_ON), D(M, "Leave it on. That's all you need in here."), P("His eyes sit on the tuck between your tits.")),
         GC(cond(TOWEL_ON), P("He looks at the towel like he paid for it, and like he paid for your tits under it."), D(M, "Over here."))],
    ],
}
# Laura catches the slip (home_items.TOWEL_CAUGHT stays with Ryan's hubs): her words, this room's lines round them
MARK_TOWEL_CAUGHT = {
    "home_kitchen": [
        P("The knot over your tits comes loose in your fingers, the towel starts to go, and across the kitchen Laura's eyes land on your hand."),
        D(L, "What did I say about towels in this house?"),
        P("You yank it tight and walk out past the fridge. Nobody in that kitchen says a word, and you can feel the two of them not saying it."),
    ],
    "home_living_room": [
        P("You loosen the tuck and the towel slides down the top of your tits, and across the room you see Laura looking straight at them."),
        D(L, "What did I say about towels in this house?"),
        P("You grab it shut and head for the hall. The TV keeps talking, and she still hasn't said one word to him."),
    ],
}


def mark_towel(cid, loc):
    kitchen = loc == "home_kitchen"
    return towel_set(
        cid, M, "power", 40, 60, "mark_towel_today", [npc_add(M, "power", 2), EXH1], loc,   # her slip pays her, like Ryan's (DECISIONS 124)
        lines=MARK_TOWEL_LINES[loc],
        slip=MARK_TOWEL_SLIP_K if kitchen else MARK_TOWEL_SLIP, slip_lead=MARK_TOWEL_LEAD_K if kitchen else MARK_TOWEL_LEAD,
        slip_media=VID("a young woman letting her bath towel slip off her breasts in front of an older man on a couch", "girl drops towel in front of older man", "towel slip flash stepdad", pool_dir=f"sex/towel_mark_slip_{cid.replace('hub_mark_', '')}_t4"),
        slip_gate=(DARING, flag("mark_saw_her")), drop=MARK_TOWEL_DROP_K if kitchen else MARK_TOWEL_DROP, drop_gate=[SHOWING, flag("mark_saw_her")],   # his chosen acts follow his accident (H2, DECISIONS 124)
        drop_media=VID("a young woman standing naked with her bath towel on the floor, an older man looking at her", "girl drops towel naked older man", "towel drop naked stepdad", pool_dir=f"sex/towel_mark_drop_{cid.replace('hub_mark_', '')}_t4"),
        caught_by=L, caught=MARK_TOWEL_CAUGHT[loc],
        # reader batch 4 (pass 3): Laura at the dinner table, Mon/Tue/Thu/Fri 18:00-19:00 and Sunday evenings
        # fix_g3c: the room in the line, so each hub reads its own (one pool, one place); seen shows only while Laura is here
        seen=[P("Mark's eyes go down the towel to your bare thighs and snap away, fast. Laura is right there " + {"home_kitchen": "in the kitchen with you both.", "home_living_room": "in the living room with you both."}.get(loc, "with you both.")),
              D(M, "Go and put some clothes on, @player.")],
        # reader a3 #5-6 (DECISIONS 131, call A): his order's no, in his top band; his Want +1 once a day
        no=("Hitch the towel up.", MARK_TOWEL_NO_K if kitchen else MARK_TOWEL_NO, "home_ella_room", "Go to your room."))


def mark_hub(cid, loc, name, setting, extra=(), awake=True, leaks=(), items=(), leave="Leave him to it.", leave_to="home_hall", towel=False):
    choices, nodes = [], []
    t_blocks, t_choices, t_nodes = mark_towel(cid, loc) if towel else ([], [], [])
    for args, kw in items:
        c, n = item(*args, **kw); choices += c; nodes += n
    return {"id": cid, "name": name,
            "description": f"Mark's hub: {setting}. His Want and Power colour it; his lines read what she wears.",
            "trigger": {"location": loc, "npc": M, "requires_npc": M, "is_repeatable": True, "priority": 6,
                        "is_active": True, "conditions": cond(flag("opening_done"))},
            "nodes": [node("hub", name, [*extra] + ([*mark_state_lines(loc), *leaks,
                G(cond(ntrait(M, "power", "lt", 40)), P(MARK_ROOM_WORDS[loc]["soft"])),
                G(cond(ntrait(M, "power", "gte", 60)), P(MARK_ROOM_WORDS[loc]["hard"])),
                G(cond(ntrait(M, "want", "gte", 50)), T(MARK_ROOM_WORDS[loc]["wants"])),
                *t_blocks,
            ] if awake else []), choices + t_choices + [go(leave, loc=leave_to)])] + nodes + t_nodes}

LR = "home_living_room"
out.append(mark_hub("hub_mark_living_room", LR, "Mark, up late", "the living room late", [
    P("Mark is on the couch with the TV low and a beer on his knee."),
    G(cond(LAURA_IN_BED), P("Laura's gone to bed."), D(M, "Shut the door. Your mother's in her room.")),
    POOL(D(M, "Can't sleep, @player?"), D(M, "Sit if you're sitting. Don't hover."), pid="mark_late_lines"),
    # B3 (DECISIONS 147): he walked in on her watching channel 5 before his late TV row
    G(cond(flag("mark_caught_ch5"), since("mark_caught_ch5", "lt", 24)), D(M, "Channel five, was it?"), P("He holds out the remote to you and doesn't let go of it straight away.")),
], leaks=LEAKS_LATE, towel=True, items=[
    (("beer", "Have a beer with him.", [], "had_drink_home", LR,
      [P("The game on low."), G(cond(LAURA_IN_BED), D(M, "Laura's in her room. Keep it down.")), P("He hands you a can without asking."),
       ME("Who's winning?"), D(M, "Not us. Never us. Drink your beer.")],
      None, 30),
     # pass 3 D44 (the-surfaces.md R9): the beer, the laundry, the dishes and Sunday breakfast with him each land on a
     # short screen of his reaction (item(after=...)), not a toast. Same effects, time and caps on the act button.
     dict(done_exits=[go("Drink it with him.", node="hl_beer_after", mins=30, flags=[fset("had_drink_home")], mods=DRINK)],   # plain: no Lust (DECISIONS 128)
          after=("Drink it with him.", [P("You drink it at the other end of the couch with your feet tucked under you. By the bottom of the can he isn't watching the game at all. He's watching your legs, and he doesn't bother hiding it."),
                                        D(M, "Not a word to your mother.")], "Leave him the empty can."),
          tease=m_tease(108, "late TV and a beer", "Curl up on the couch."), touch=m_paid(108, "late TV and a beer"),
          # reader batch 5 (pass 3): the can he holds out gets an answer when she says no
          no=([D(M, "Suit yourself. More for me."),
               P("He cracks it himself and drinks, and his eyes follow your legs all the way to the door.")], "Leave him to his game."))),
    (("film", "Put a film on with him.", [tod("22:00", "00:00")], "movie_night", LR,
      [D(M, "You pick. Nothing with singing."), ME("This one?"), D(M, "Fine. Wake me for the car chase.")],
      [energy(5)], 120),
     # reader 2026-11-04: the film plays behind the act button, so "Not now." never follows a film already watched (as hub_ryan_living_room)
     dict(after=("Watch it with him.", [P("He falls asleep in the second half, and you watch the end with his snoring for a soundtrack.")], "Get up.", "home_hall"),
          # the written no: his "You pick" gets an answer when she says no
          no=([D(M, "Your choice. I'd have slept through it anyway."),
               P("He flicks the TV back to whatever was on, but his eyes leave the screen once, for your legs on the way to the door, and go back.")], "Leave him the remote."))),
]))
# Watch TV with him (DECISIONS 85-86): the same remote as alone (home.py), his line on each channel,
# and on channel 5 his reaction by his step. "Leave it on." pays more than alone, once a day (LO, 2026-10-30,
# DECISIONS 92): her Corruption +2 (cap 19 / 39) and his Want +2; after that it plays and pays nothing.
MARK_TV_ADULT = ("Channel 5 fills the screen. A woman is on her knees in front of a man. She sucks his cock, slow and deep, her cheeks hollow. He pulls her up and bends her over the bed. He takes her from behind. Her tits swing with every thrust. She moans, loud and long. The room goes quiet under the sound. Mark stops with the beer halfway to his mouth, but he does not reach for the remote. His fingers squeeze tight around the can. On screen the man grips her hips and drives in harder. Your face goes hot. You are wet, and your nipples pull hard and tight.")
MARK_TV_LEAVE = ("You leave it on. You both watch. On screen the man drives into her from behind. He slaps her ass, hard, and she moans. Her tits swing under her with each thrust. Mark shifts on the couch. The can moves down to his lap. It does not hide the hard bulge of his cock in his jeans. His eyes go from the screen to you. Then back to the screen. Nobody says anything. The man grips her hips and pounds her harder. She moans louder with every thrust. You are wet. You squeeze your thighs together, tight. Your nipples go hard and tight.")
MARK_TV_LINES = {
    "news": ["The late bulletin. A man in a tie reads out road closures nobody's awake to use.",
             "The late news: a warehouse fire, the same mayor, the same apology."],
    "cooking": ["A grilling show on repeat. A man with a beard salts a steak from very high up.",
                "A baking rerun. A woman's cake falls in on itself, and the judges pull sad faces."],
    "sports": ["Football highlights from somewhere far away, three goals and a fight.",
               "A replay of an old game, and the commentator's still shouting about the same foul."],
    "film": ["A western with the color gone orange. A man in a long coat rides into town to shoot somebody.",
             "A war film, all mud and shouting. The young one shows a photo of his girl, so you know he's done."],
}
MARK_CH = {"news": D(M, "Same as yesterday. Same as every day."), "cooking": D(M, "Your mother never cooks like that."),
           "sports": D(M, "Watch this. Watch. Ah, for God's sake."), "film": D(M, "Seen it. He dies at the end.")}
_hub = out[-1]
assert _hub["id"] == "hub_mark_living_room"
_hub["nodes"][0]["choices"].insert(-1, go("Watch TV with him.", node="mremote"))
_hub["nodes"] += [node("mremote", "The remote", [
        P("You take the other end of the couch, and he hands you the remote without looking."),
    # reader a3 #1 (DECISIONS 131): channel 5 beside him after his accident, like "Leave it on."; reader batch 5 (pass 3):
    # and at Curious, as "Leave it on." is: putting porn on beside him is watching by choice (the-heat-ladder.md H1)
    ], remote_choices("mch_", "madult", adult_cond=cond(flag("mark_saw_her"), CURIOUS)) + [go("Leave him to it.", loc="home_hall")])]
for cid, btn, lines, desc, qs, pool in CHANNELS:
    _hub["nodes"].append(node(f"mch_{cid}", btn.split(": ", 1)[1].rstrip(".").capitalize(),
        [POOL(*[P(x) for x in MARK_TV_LINES[cid]]), MARK_CH[cid], VID(desc, *qs, pool_dir=pool.replace("tv/", "tv/mark_"))],
        [*watch_plain(LR), go("Change the channel.", node="mremote"), go("Leave him to it.", loc="home_hall")]))
_hub["nodes"] += [
    node("madult", "Channel 5", [P(MARK_TV_ADULT),
        G(cond(trait("mark_step", "lt", 4)), D(M, "Change it, @player."), P("He says it, but he doesn't reach for the remote.")),
        G(cond(trait("mark_step", "gte", 4)), P("He doesn't tell you to change it. He watches the screen, and then he watches you watching it.")),
        VID("porn playing on a living room TV at night, a man and a woman, seen from the couch", "porn on tv late night couch", "watching porn on tv with someone", pool_dir="sex/tv_adult_mark_t5")],
        [go("Leave it on.", node="mleave", mins=5, cond_=cond(CURIOUS, flag("mark_saw_her"))),   # porn beside him is a chosen act for one: Curious (DECISIONS 124)
         go("Change the channel.", node="madult_no", mins=1), go("Leave him to it.", loc="home_hall")]),
    # the written no: it costs nothing and moves nothing; his reply by his step
    node("madult_no", "Another channel", [
        P("You thumb the channel away. The moaning stops, and the room goes very quiet. Your face is still hot, and your nipples are still hard."),
        G(cond(trait("mark_step", "lt", 4)), D(M, "About time.")),
        G(cond(trait("mark_step", "gte", 4)), D(M, "Getting shy on me?")),
        P("He puts the can back on his knee and looks at the wall above the TV."),
    ], [go("Pick something else.", node="mremote"), go("Leave him to it.", loc="home_hall")]),
    node("mleave", "Leave it on", [P(MARK_TV_LEAVE),
        VID("a man on a couch at night watching porn on TV, a beer can in his lap", "man watching porn tv couch beer", "stepdad watching porn on tv", pool_dir="sex/tv_adult_mark_leave_t5")],
        [   # (DECISIONS 124) "Leave it on." needs Curious, so the Good Girl pay row is gone
         go("Keep watching.", loc=LR, mins=25, eff=tv_pay(2, 39) + [want(M, 2)], flags=[fset("mark_tv_paid")],
            cond_=cond(TV_CUR, flag("mark_tv_paid", False))),
         go("Keep watching.", loc=LR, mins=25, cond_=cond(flag("mark_tv_paid"))),
         go("Change the channel.", node="madult_no", mins=1)]),
]

# Sun 00:00-01:00 Mark and Laura are awake (DECISIONS 80): the "asleep" line skips that hour, written
# once per piece of the night because conditions do not nest.
ASLEEP_HOURS = [(wd(0, 1, 2, 3, 4, 5), tod("22:00", "07:00")), (wd(6), tod("22:00", "00:00")), (wd(6), tod("01:00", "07:00"))]
out.append(mark_hub("hub_mark_bedroom", "home_master_bedroom", "Mark, in bed", "their bed, at night", [
    *[G(cond(*hrs), P("Mark is asleep on his back on his side of the bed, snoring, one arm flung out. Even asleep he takes up most of it."))
      for hrs in ASLEEP_HOURS],
    # pass 3 D5: his Saturday lie-in row (DECISIONS 152, Sat 07:00-08:30 asleep) gets its own line
    G(cond(wd(5), tod("07:00", "08:30")), P("Saturday, and Mark is sleeping in, face down across most of the bed with the curtains still shut. He grunts into the pillow when the door creaks, and doesn't wake.")),
    # scene reader b02 (2026-11-03): his Sunday 00:00-01:00 row is awake, after Saturday night with Laura
    # (master_door_saturday_night); the hub had no line for that hour
    G(cond(wd(6), tod("00:00", "01:00")), P("Mark is awake, sat up against the headboard with the sheet shoved down to his hips, his chest still shining with sweat. He sees you in the doorway and doesn't pull the sheet up."),
      D(M, "Bed, @player. Shut that door on your way.")),
    G(cond(wd(6), tod("00:00", "01:00"), here(L, "home_master_bedroom")), P("Laura is face down beside him, already half asleep, and doesn't lift her head.")),
    # scene reader b02: his want on the page while he sleeps, and where he is when he's awake
    G(cond(ntrait(M, "want", "gte", 30), tod("01:00", "08:30")), P("He mutters in his sleep and rolls toward the door, toward you. Under the sheet his cock is a hard ridge against his thigh."),
      # reader pass 4 b5: low heat on her body, and the not-yet with its price
      P("Your nipples go tight, and heat drops low between your legs. You don't take one step closer. If he opens his eyes now, he finds you in his doorway staring at it.")),
    G(cond(wd(0, 1, 2, 3, 4, 5), tod("01:00", "00:00"), logic="OR"), P("Most nights he's in the living room late with a beer and the TV low, awake, and watching you. Not now.")),
], awake=False, leave="Back out."))
# ── the laundry tease ladder (LO, 2026-11-02, DECISIONS 128: "plain chores raises nothing, she can tease at a point").
#    Plain laundry pays Mark nothing; three teases by her stage, after his accident (`mark_saw_her`), no step needed;
#    once a day through the item's own `did_laundry`. Screens: sheets/scenes/mark_laundry_teases.md. ──
from sheetbeats import beat
MLT = "mark_laundry_teases"
PANTIES_ON = {"type": "clothing_slot", "slot": "underwear", "operator": "equipped"}
NO_TOWEL = {"type": "worn_type", "operator": "neq", "value": "towel"}
def _wt(v): return {"type": "worn_type", "operator": "eq", "value": v}
LAUNDRY_BASKET = {"label": "Leave your basket on top.", "ref": f"{MS}:109", "gate": [CURIOUS, flag("mark_saw_her")],
                  "eff": [want(M, 2)], "what": "Mark, laundry: tease (Curious)"}
LAURA_IN_HOUSE_Q = "\"Jesus, @player. Laura's in the house.\""
assert beat(MLT, "daring_shirt").count(LAURA_IN_HOUSE_Q) == 1
LAUNDRY_TEASES = [
    {"label": "Bend for the bottom drum.", "name": "The bottom drum",
     "gate": [CURIOUS, DARING, flag("mark_saw_her"), PANTIES_ON, NO_TOWEL],   # seen and sexual: both meters (meters.md rule 4)
     "eff": [want(M, 3), {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 39}],
     "blocks": [*[GC(cond(_wt(t)), P(beat(MLT, "daring_skirt"))) for t in ("short_skirt", "laura_dress", "party_dress", "cafe_uniform")],
                # truth pass (2026-11-03): "Laura's in the house." only while she is (her kitchen row, weekday evenings);
                # on a Saturday in the garage she is out, and his line stops at "Jesus, @player."
                GC(cond(SLEEP_SHIRT, here(L, "home_kitchen")), P(beat(MLT, "daring_shirt"))),
                GC(cond(SLEEP_SHIRT), P(beat(MLT, "daring_shirt").replace(LAURA_IN_HOUSE_Q, '"Jesus, @player."'))),
                *[GC(cond(_wt(t)), P(beat(MLT, "daring_jeans"))) for t in ("jeans", "leggings", "shorts")],
                VID("a girl bending over to load a front-loading washer, her skirt riding up, a man at a workbench watching", "girl bends over washing machine skirt rides up", "bending over laundry panties showing", pool_dir="sex/mark_laundry_bend_t4"),
                # pass 3 B4: the garage talks
                D(M, "Take your time down there. Find every sock."), ME("I'm looking, Mark."), D(M, "So am I.")]},
    {"label": "Wash what you're wearing.", "name": "In the wash",
     "gate": [BOLD, SHOWING, flag("mark_saw_her"), {"type": "clothing_slot", "slot": "top", "operator": "equipped"},
              {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}],
     "eff": [want(M, 4), {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 59},
             {"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 59}],
     "wardrobe": [{"action": "unequip", "item_id": g} for g in ("tshirt", "thin_top")],   # the top is in the washer
     # scene reader b03 (2026-11-03): "Laura shuts a cupboard" only while she is in the house (Saturday 09:00-16:00
     # she is out, and this tease plays in his garage row then); out of the house a car door does the same job
     "blocks": [GC(cond(*[here(L, r) for r in ("home_kitchen", "home_master_bedroom", "home_bathroom", "home_living_room", "home_hall")], logic="OR"), P(beat(MLT, "bold"))),
                # fix_g3c: the else is her bra (the tease's own gate), an exact check, not worn_exposure
                GC(cond({"type": "clothing_slot", "slot": "bra", "operator": "equipped"}), P(beat(MLT, "bold").replace("Somewhere in the house Laura shuts a cupboard.", "Out on the street a car door slams."))),
                VID("a girl in her bra by a running washing machine in a garage, a man at a bench staring", "girl in bra doing laundry garage", "topless laundry bra man watching", pool_dir="sex/mark_laundry_wash_t4"),
                D(M, "Put a shirt on before somebody walks in."), ME("It's in the wash."), D(M, "Then stand there and let me look till it's dry.")]},
]
G_ = "home_garage"
out.append(mark_hub("hub_mark_garage", G_, "Mark, in the garage", "the garage", [
    P("Mark's at his bench with the radio on, doing something to an engine part that doesn't need doing."),
    POOL(D(M, "Hand me that wrench. No, the other one."), D(M, "Don't touch anything."), D(M, "What do you want? I'm busy."), pid="mark_garage_lines"),
    ME("Hi to you too, Mark."), D(M, "Hi. Now what?"),   # pass 3 B4
], leaks=LEAKS_GARAGE, items=[
    (("laundry", "Do your laundry while he works.", [tod("07:00", "21:00")], "did_laundry", G_,
      [D(M, "Whites with whites, @player."), ME("I know how a washing machine works."), D(M, "Prove it.")],
      [energy(-5)], 30),
     dict(plain_costs=[{"trait": "energy", "value": 5}],
          after=("Load the machine.", [P("He looks at you like you're going to break the machine, and he goes back to his bench."),
                                       P("You bend over the basket and feed the drum, and behind you the wrench stops. When you straighten up, Mark is looking at your ass, and he goes back to the engine part like he never stopped."),
                                       D(M, "Whites with whites. Good girl.")], "Leave him to his bench.", "home_hall"),
          tease=LAUNDRY_BASKET, teases=LAUNDRY_TEASES,
          # the written no: his "Whites with whites" gets an answer when she takes the basket away
          no=([D(M, "Then get that basket out of my way."),
               P("You pick it up and go. He doesn't look up from the bench until your ass is in the doorway, but then he does.")], "Take the basket back."))),
]))
K = "home_kitchen"
out.append(mark_hub("hub_mark_kitchen", K, "Mark, in the kitchen", "the kitchen", [
    G(cond(wd(2), tod("17:00", "20:00")), P("Wednesday. Mark's cooking, badly, with a beer on the counter and the extractor fan roaring."), D(M, "It's chilli. It's always chilli.")),
    G(cond(wd(2), tod("20:00", "22:00")), P("Wednesday. The chilli pan is soaking in the sink and Mark's at the table with a beer.")),
    G(cond(wd(6), tod("08:00", "18:00")), P("Sunday. Mark's at the table with the paper and his coffee, in the chair at the head of it.")),
    G(cond(wd(6), tod("08:00", "12:00")), D(M, "Morning.")),
    # pass 4 D5 (the-surfaces.md R2): between breakfast and dinner nothing on Sunday is aimed at him, so the screen says why
    G(cond(wd(6), tod("12:00", "18:00")), P("He has the sports pages spread over the whole table and doesn't look up. Sunday afternoon is his, and he wants it to himself.")),   # reader 2026-11-04: from noon; "to himself", since Ryan's row 6 hears his radio
    G(cond(wd(6), tod("18:00", "20:00")), P("Sunday dinner. Mark's at the head of the table with his sleeves rolled, filling his plate.")),
    G(cond(wd(6), tod("20:00", "22:00")), P("Sunday night. Mark's at the table with a beer and the game on the radio, the dinner plates stacked by the sink.")),
    # DECISIONS 152: his Saturday coffee row, 08:30-09:00, before the garage
    G(cond(wd(5), tod("08:30", "09:00")), P("Saturday. Mark's on his feet at the counter with his coffee, in his work jeans. He drinks it standing, on his way to the garage, and he isn't stopping to talk."), D(M, "Morning.")),
    # pass 4 D5: his Saturday bar row (17:00-18:30) had no line at all; he is busy leaving, and says so
    G(cond(wd(5), tod("17:00", "18:30")), P("Saturday. Mark's at the counter in a clean shirt with his keys in his hand, on his way out to the bar with the guys."), D(M, "Don't wait up.")),
    G(cond(wd(0, 1, 3, 4), tod("18:00", "19:00")), P("Mark's at the table for dinner, sleeves rolled, already eating.")),
], leaks=LEAKS_KITCHEN, towel=True, items=[
    (("breakfast", "Sunday breakfast with him.", [wd(6), tod("08:00", "11:00")], "ate_breakfast", K,
      [P("He slides the paper over."), G(cond(flag("rent_starts"), flag("sunday_counted_today", False)), D(M, "Eat, @player. Then the rent.")),
       G(cond(flag("sunday_counted_today")), D(M, "Eat, @player.")), G(cond(flag("rent_starts", False)), D(M, "Eat, @player."))],
      [energy(10)], 15),
     dict(tease=m_tease(104, "Sunday breakfast"), touch=m_paid(104, "Sunday breakfast"),
          after=("Eat with him.", [P("You eat with the paper between you. He reads the football and doesn't look up until you push your plate away, and then he looks you over once, slow, over the top of the page."),
                                   D(M, "That's more like it."), ME("More like what?"), D(M, "Like you live here.")], "Clear your plate."),
          no=([D(M, "Nobody's making you. Toast's getting cold either way."),
               P("He goes back behind the paper, and he lowers it an inch to watch your legs leave the kitchen.")], "Leave him to his paper."))),
    (("dinner", "Sit down to dinner.", [wd(0, 1, 2, 3, 4, 6), tod("18:00", "20:00")], "ate_dinner", K,
      [G(cond(wd(0, 1, 3, 4, 6)), P("Burnt chops."), D(M, "Your mother cooks. I fill plates."), ME("They're black, Mark."), D(M, "They're cooked. Eat.")),
       G(cond(wd(2)), P("Chilli, again."), D(M, "It's always chilli. Eat it."), ME("I had chilli last week."), D(M, "And you'll have it next week.")),
       G(cond(here(L, K)), P("Laura sits across from him and asks you about college before he can say anything else.")),
       G(cond(here(R, K)), P("Ryan eats beside you like he's late for something."))],
      [energy(15)], 30),
     dict(tease=m_tease(105, "dinner", "Eat slowly for him."),
          no=([D(M, "Your plate's going in the trash, then."),
               P("He doesn't look up from his food, but you feel it when you stand: one look at your legs, quick, and back to his fork.")], "Leave the table."))),
    (("cook", "Help him cook.", [wd(2), tod("18:00", "19:00")], "helped_cook", K,
      [D(M, "Hand me the salt. No, the other salt."), ME("There's only one salt, Mark."), D(M, "Then that one. Don't be clever.")],
      [energy(-5)], 30),
     dict(plain_costs=[{"trait": "energy", "value": 5}], tease=m_tease(106, "help him cook", "Reach past him for the pan.", bold=True),
          no=([D(M, "Fine. Go on. I can ruin it by myself."),
               P("He bangs the spoon on the pan and turns back to the chilli. He doesn't ask twice, but he looks over his shoulder at your ass on the way out.")], "Leave him to the chilli."))),
    (("dishes", "Do the dishes with him.", [wd(2, 6), tod("19:00", "21:00")], "did_dishes", K,
      [P("He dries, slow."), D(M, "You missed one.")],
      [energy(-5)], 20),
     dict(plain_costs=[{"trait": "energy", "value": 5}],
          after=("Wash up with him.", [P("He dries slow at your shoulder and holds every plate you hand him up to the light before he puts it away. Twice he hands one back without a word, and his fingers stay on yours on the plate."),
                                       D(M, "Slow down. You're not in a race.")], "Leave him the tea towel."),
          tease=m_tease(107, "dishes", "Bend to the dishwasher."), touch=m_paid(107, "dishes", "Stay bent."),
          no=([D(M, "Leave them, then. They'll be here tomorrow, same as me."),
               P("He picks the tea towel up anyway. He doesn't watch you go, but you can tell how hard he's working at it.")], "Leave him the plates."))),
]))

cards = step_cards(M, {
    1: ("Sunday. Mark sits you down at the kitchen table with the rent.", "Sunday morning: the kitchen, Mark and the rent envelope"),   # Q6: no second count
    2: ("His eyes were on your hem at the table. He's on the phone a lot, late.", "Late at night: the kitchen drawer, Mark next door"),
    3: ("\"Friday, Frank.\" He knows you heard. Sunday's coming.", "Sunday morning at the table, after a short week"),
    4: ("He can't hold your look at the table. He wants to talk terms.", "An evening in the garage, after a late night in Ryan's room"),
}, terminal_text=("The Sunday table, every week: his eyes on you.", "Mark, later. (After the house is yours.) His Want still counts: every look you give him is kept for the next release."),
   closed_text="You told him you'd tell Mom. The rent is strict now, every Sunday, and nothing else.")
for c in cards:
    c["when"].append({"flag": "opening_done", "op": "is_true"})

from sheetbeats import beat
# ── step 0 · the dryer (mark_00_the_dryer.md, signed 2026-11-02; DECISIONS 124-125, the-heat-ladder.md H2):
#    his first accident. It happens to her; it pays his Want and sets mark_saw_her, which his chosen acts read.
BRA_ON = {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}
BRA_OFF = {"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}
SAW = [nadd(M, "want", 5)]
SAW_FLAGS = [fset("mark_saw_her")]


def _cut(key):
    """The signed dryer beat in two at "You go to your room to change": (before, from there on)."""
    b = beat("mark_00_the_dryer", key)
    i = b.index("You go to your room to change")
    return b[:i].strip(), b[i:]


out.append({
    "id": "mark_00_the_dryer", "name": "The washer hose",
    "description": "Mark's first accident (DECISIONS 124): Saturday in the garage, the washer hose soaks her; he looks, then turns his back and holds out a towel. His Want +5 on the way in (\"Load the washer.\", DECISIONS 147), mark_saw_her either way; her \"Don't take it yet.\" pays Exhibitionism +1, cap 19.",
    "trigger": {"location": "home_garage", "npc": M, "requires_npc": M, "is_repeatable": False, "priority": 9, "is_active": True,
                "consume_on": "exit",
                "schedules": [{"weekdays": [5], "start_time": "09:00", "end_time": "17:00"}],
                "conditions": cond(flag("opening_done"), flag("mark_saw_her", False))},
    "nodes": [
        # DECISIONS 147 (H5): his Want +5 moved off both endings onto the moment, the exit into the screen where he sees her
        node("basket", "Laundry", [
            P("You carry your basket down the hall to the garage. Mark's at his bench with the radio on, his back to you. He grunts at you without turning round."),
            D(M, "Machine's playing up. Mind the hose."),
        ], [go("Load the washer.", node="hose", mins=5, eff=SAW)]),
        node("hose", "The washer hose", [
            GC(cond(BRA_ON), P(beat("mark_00_the_dryer", "hose_bra"))),
            GC(cond(BRA_OFF), P(beat("mark_00_the_dryer", "hose_nobra"))),
        ], [
            go("Take the towel.", node="covered", mins=2),
            go("Don't take it yet.", node="stay", mins=2),
        ]),
        # pass 3 (B3, A63): spoken lines beside her thoughts, and the wish her accident turns into
        # the signed beat is cut where she leaves (_cut), so the talk sits before the stairs; every signed word stays
        node("covered", "Back to his bench", [P(_cut("covered")[0]),
                                             ME("Thanks. For the towel."),
                                             D(M, "Don't thank me. Go and change before you catch your death."),
                                             ME("You can turn round now, Mark."),
                                             D(M, "I'm fine where I am. Go on."),
                                             P(_cut("covered")[1]),
                                             # reader 2026-11-04: her thought by Exhibitionism; the accident has no floor
                                             GC(cond(trait("exhibitionism", "lt", 20)), T("He wouldn't turn round. Thank God. Your face burns the whole way to your room.")),
                                             GC(cond(trait("exhibitionism", "lt", 40)), T("He wouldn't turn round. You wonder what his face was doing.")),
                                             GC(cond(trait("exhibitionism", "lt", 60)), T("He wouldn't turn round. You want to see what he does the day he doesn't stop himself.")),
                                             GC(cond(trait("exhibitionism", "gte", 60)), T("He wouldn't turn round. Next time you won't take the towel, and you'll make him look."))],
             [go("Go and change.", loc="home_hall", mins=10, consumes=True, flags=SAW_FLAGS)]),
        node("stay", "Not yet", [P(_cut("stay")[0]),
                                 ME("You didn't have to turn round, Mark."),
                                 D(M, "Yes, I did. Go and get dressed, @player. Now. Before anybody sees you like that."),
                                 P(_cut("stay")[1])],
             [go("Go and change.", loc="home_hall", mins=10, consumes=True, flags=SAW_FLAGS,
                 eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 19}])]),
    ]})

text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · MARK (sheets/scenes/mark_0*.md, people/npc_mark.md, systems/money_pressure.md)\n"
        "# Steps 1-9, the Sunday table, Vance's knock, the twist's offer, his hubs, his cards.\n"
        "# =============================================================================\n")
# Iteration 002, part 7: the speech written inside Mark A 5's paragraphs becomes dialog blocks, word for word
for _c in out:
    if _c["id"] == "mark_05_a_bill_an_inch":
        for _n in _c["nodes"]:
            if _n["id"] == "start":
                _n["blocks"] = lift_line(_n["blocks"], "You asked what the difference was worth, @player. Here it is.", M)
                _n["blocks"] = lift_line(_n["blocks"], "Five for every inch my hand climbs your bare thigh. Cash. Twenty tops.", M)
                _n["blocks"] = lift_line(_n["blocks"], "I asked what the difference was worth. Here's my answer,", "player")
text += "".join(emit(c) for c in out) + "".join(emit_card(c) for c in cards)
open(__import__("sys").argv[1], "w").write(text)
print("mark:", len(out), "canvases,", len(cards), "cards", "(her table voice:", "placeholder" if HERS_LOOK == "PLACEHOLDER" else "written", ")")
