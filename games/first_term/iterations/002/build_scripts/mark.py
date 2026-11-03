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
SHORT = flag("rent_carried")
FULL_ITEMS = [flag("rent_carried", False), flag("ryan_covered", False), flag("mark_money_week", False)]
BROKEN = cond(flag("rent_carried"), flag("ryan_covered"), flag("mark_money_week"), logic="OR")
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
PAID_BACK = [funset("her_door_unlocked")] + [funset(f"garage_holds_{i}") for i in HELD]
PAYBACK_LINES = [
    G(cond(*FULL_ITEMS, flag("her_door_unlocked")), D(M, "Key."), P("He slides your door key across the table without looking at it.")),
    *[G(cond(*FULL_ITEMS, flag(f"garage_holds_{i}")), D(M, f"The {HELD_NAME[i]}'s on the nail. Take it.")) for i in HELD],
]
# (reader fix, 2026-11-01) read before the count adds this Sunday, so a full Sunday says the streak it is about to
# make, and a carried or covered Sunday says nothing
STREAK_LINES = [
    G(cond(*FULL_ITEMS, trait("paid_full_streak", "eq", 0)), P("One Sunday paid your way. He writes a small 1 on the back of the envelope and doesn't say anything about it.")),
    G(cond(*FULL_ITEMS, trait("paid_full_streak", "eq", 1)), P("Two Sundays in a row, your own money. He notices. He doesn't like noticing.")),
    G(cond(*FULL_ITEMS, trait("paid_full_streak", "gte", 2)), P("Sunday after Sunday, all of it, from your own pocket. He counts it like he's hoping it's wrong.")),
]

# ── step 1 · Mark A 1 · count it slowly ──
out.append({
    "id": "mark_01_count_it_slowly", "name": "Count it slowly",
    "description": "Mark step 1 (Mark A 1), her first Sunday at the table. The engine took the rent at midnight; this is Mark counting it with her there. Reads rent_carried. Counts the Sunday for the streak.",
    "trigger": step_trigger(M, 1),
    "nodes": [
        node("table", "The kitchen table", [
            IMG("scenes/mark_01_table.jpg", "a man in his forties at a kitchen table with an envelope of cash and a coffee, Sunday morning light",
                "man counting cash kitchen table morning", "stepfather kitchen table envelope of money"),
            P("Mark is at the kitchen table with the envelope of rent in front of him and a coffee going cold. Sunday. Laura's out shopping."),
            G(cond(*BARE_LEGS), P("He looks up, and his eyes go straight to your bare legs, and stay.")),
            G(cond({"type": "clothing_item", "item_id": "jeans", "operator": "equipped"}), P("He looks up, and his eyes go down your legs in your jeans, and stay.")),
            G(cond({"type": "clothing_item", "item_id": "leggings", "operator": "equipped"}), P("He looks up, and his eyes go down your legs in your leggings, and stay.")),
            G(cond(SLEEP_SHIRT), P("You came down in your sleep shirt. It stops mid-thigh. He watches the hem the whole way to the table.")),
            D(M, "Sit. I count it in front of you. That way nobody says I took more than I did."),
        ], [
            go("\"Here.\"", node="count", mins=5),
            go("\"Let me get dressed first.\"", node="dressed", mins=5, wardrobe=DRESS_DAY),
        ]),
        node("count", "The count", [
            G(cond(SHORT),
              P("He licks his thumb and counts the bills out onto the table, one at a time, slow. Slower than he needs to. You're short and you both know it, and he makes you sit through every bill of it."),
              D(M, "Seventy-five, I said.")),
            G(cond(flag("rent_carried", False)),
              P("You lean back in the chair and watch him lick his thumb and count. It's all there. Every bill."),
              ME("Count it slowly, Mark. Take your time."),
              P("He looks up. He doesn't like your tone. He counts slower anyway, and his eyes keep leaving the money.")),
        ], [
            go("\"Can you just — count it?\"", node="short", mins=3, cond_=cond(SHORT)),
            go("Watch him count.", node="short", mins=3, cond_=cond(flag("rent_carried", False))),
        ]),
        node("short", "I am counting", [
            D(M, "I am counting."),
            G(cond(SHORT), P("He writes the gap on the back of the envelope in pencil and taps it twice."), D(M, "The rest waits a week. Vance doesn't.")),
            G(cond(flag("rent_carried", False)), D(M, "That's the week. Same again Sunday.")),
            G(cond(SLEEP_SHIRT), D(M, "And not the shirt, next time.")),
            *STREAK_LINES, *PAYBACK_LINES,
            T("He counted you as much as the money."),
        ], count_exits("\"Fine.\"", "home_hall", 5, eff=[nadd(M, "want", 10), setv("mark_step", 1)], flags=[done(1)], consumes=True)),
        node("dressed", "Suit yourself", [
            D(M, "Suit yourself."),
            P("You go up and put clothes on and come back down. He's counted it without you. He pushes the envelope at you to look at, and doesn't look at you at all."),
            G(cond(SHORT), D(M, "Short. The rest waits a week.")),
        ], count_exits("Go back upstairs.", "home_hall", 15, eff=[setv("mark_step", 1)], flags=[done(1)], consumes=True)),
    ]})

# ── step 2 · Mark A 2 · the late notice ──
out.append({
    "id": "mark_02_late_notice", "name": "The late notice",
    "description": "Mark step 2 (Mark A 2), the kitchen drawer late at night, Mark on the phone next door. She learns his debt to Vance. Sets knows_mark_debt.",
    "trigger": step_trigger(M, 2, bind_npc=False),
    "nodes": [
        node("drawer", "The drawer", [
            P("You come down for water in the dark. The drawer by the fridge is open an inch, the way it never is. Under the takeaway menus there's a letter on thick paper, Vance's name printed at the top. LATE NOTICE, it says. And under it, a number with a lot of zeros."),
            P("Through the wall you can hear Mark in the living room, the TV low, his voice lower."),
        ], [
            go("Read it.", node="phone", mins=3, flags=[fset("knows_mark_debt")]),
            go("Shut the drawer.", loc="home_kitchen", mins=1, retry=2),
        ]),
        node("phone", "Friday, Frank", [
            P("You're on the second page when he comes into the doorway with his phone at his ear. He sees you. He sees what's in your hand. He doesn't hang up."),
            D(M, "Friday, Frank. I'll have it Friday. Yeah. Yeah. Friday."),
            P("He ends the call. He stands there with the phone at his side, looking at you, and for the first time in your life he looks like he's the one who owes."),
        ], [go("\"How late are we?\"", node="put", mins=2)]),
        node("put", "Put it back", [
            D(M, "Put it back."),
            P("He doesn't shout. He doesn't come for it. He just waits until you fold it along its creases and put it under the menus and shut the drawer, and then he goes back to his TV."),
            T("He knows you know. You've got something on him now."),
        ], [go("\"Okay.\"", loc="home_kitchen", mins=3, consumes=True,
               eff=[nadd(M, "want", 10), setv("mark_step", 2)], flags=[done(2)])]),
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
              P("Sunday. Mark's at the table with the envelope, and you know what he's going to ask for. You don't wait to be asked.")),
            # under Daring she waits, and he asks (reader: the screen promised an act she could not take)
            G(cond(HERS, trait("exhibitionism", "lt", 20)),
              P("Sunday. Mark's at the table with the envelope. He looks you up and down, slow."), D(M, "Shorts next time. You know the ones."),
              P("His eyes go down your legs under the table.")),   # reader a3 #16 (DECISIONS 131)
        ], [
            go("\"Fine.\"", node="shorts", mins=5, cond_=cond(HIS, trait("exhibitionism", "gte", 20)), wardrobe=SHORTS_ON, eff=[nadd(M, "power", 3)]),   # her show: Daring (DECISIONS 124)
            go("\"I'm not changing for you.\"", node="no", mins=2, cond_=cond(HIS)),
            go("Go up and change.", node="hers_down", mins=5, cond_=cond(HERS, trait("exhibitionism", "gte", 20)), wardrobe=SHORTS_ON),
            go("\"I'm not changing for you.\"", node="no", mins=2, cond_=cond(HERS)),   # her version has a no too (reader)   # her chosen show: Daring (DECISIONS 124)
        ]),
        # Iteration 002, part 8 (reader): the shorts are on her before the screen names them.
        node("hers_down", "Saved you asking", [
            P("You come down in the shortest thing you own to sleep in, the pair that shows the curve of your ass when you walk. Mark looks up and stops with his thumb on a bill."),
            ME("Saved you asking."),
        ], [go("Sit down across from him.", node="shorts", mins=2, eff=[nadd(M, "power", -3)])]),
        node("shorts", "His count goes slow", [
            P("You sit. The chair is cold on the backs of your thighs. When you lean over to push the envelope at him, the shorts ride up and you feel his eyes go down the curve of your ass and stay there."),
            P("His count goes slow. He loses his place twice. He starts again."),
            D(M, "Every Sunday. Like that."),
            *STREAK_LINES, *PAYBACK_LINES,
        ], count_exits("\"Count, Mark.\"", "home_hall", 10,
                       eff=[nadd(M, "want", 10), add("exhibitionism", 3, cap=79), setv("mark_step", 3)],
                       flags=[done(3), fset("mark_dress_rule")], consumes=True)),
        no_node("no", [D(M, "Suit yourself."), P("He counts it with his eyes on the money and not on you, and writes something on the back of the envelope that you don't get to see."), G(cond(SHORT), D(M, "Then the short stays on the tab, @player."))],
                "home_hall", 7, eff=[nadd(M, "power", -2)]),
    ]})

# ── step 6 · Mark A 6 · our arrangement ──
out.append({
    "id": "mark_06_our_arrangement", "name": "Our arrangement",
    "description": "Mark step 4 of 4, the top step (release 1): the garage; he saw her come out of Ryan's room; each holds the other's secret. Sets mark_arrangement.",
    "trigger": step_trigger(M, 4, retry_days=3),
    "nodes": [
        node("start", "The garage", [
            P("Mark's at his workbench with the radio on and his hands black with oil. He hears you come in and doesn't turn round."),
            D(M, "I saw you come out of Ryan's room. Middle of the night."),
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
            T("Your secret for his. He thinks it's even. It isn't."),
        ], [go("\"Deal.\"", loc="home_hall", mins=3, consumes=True,
               eff=[nadd(M, "want", 10), setv("mark_step", 4)], flags=[done(6), fset("mark_arrangement")])]),
        no_node("no", [D(M, "There is now, @player. Since Ryan's door."), P("He turns back to the bench. The radio fills the garage. You leave him to it, and your face is hot all the way up the stairs.")],
                "home_hall", 3, eff=[nadd(M, "power", 2)]),
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
                "home_kitchen", 14, eff=[nadd(M, "power", 3)], flags=[fset("debt_offer_seen"), fset("debt_refused")]),
    ]})

# ── the Sunday table: the repeat (mark_09 sheet; money sheet: the count, his terms or hers) ──
HERS_LOOK = open(os.path.join(HERE, "beat_mark_table_look_hers.txt")).read().strip() if os.path.exists(os.path.join(HERE, "beat_mark_table_look_hers.txt")) else "PLACEHOLDER"
BOLD_HIS = open(os.path.join(HERE, "beat_mark_table_look_his_bold.txt")).read().strip()
BOLD_HERS = open(os.path.join(HERE, "beat_mark_table_look_hers_bold.txt")).read().strip()
out.append({
    "id": "mark_sunday_table", "name": "Sit down at the table",
    "description": "The Sunday count, the repeat after Mark's step 1: his terms or hers by his Power; the streak counts here when no step has counted it. From Bold, after his step 7: \"Twenty, and you can look\", two voices, a stop exit. Once a Sunday.",
    "trigger": {"location": "home_kitchen", "requires_npc": M, "is_repeatable": True, "priority": 5,
                "is_active": True, "max_triggers_per_day": 1,
                "schedules": [{"weekdays": [6], "start_time": "08:00", "end_time": "12:00"}],
                "conditions": cond(trait("mark_step", "gte", 1), flag("sunday_counted_today", False), flag("rent_starts"))},
    "nodes": [
        node("table", "The Sunday table", [
            G(cond(HIS), P("Mark's at the table with the envelope, the way he is every Sunday. He doesn't say good morning. He points at the chair across from him with his pen."),
              D(M, "Sit. Watch me count.")),
            G(cond(HERS), P("Mark's at the table with the envelope. He's on his feet, and he doesn't sit back down until you've sat."),
              D(M, "Morning. Go on, then.")),
            G(cond(flag("mark_dress_rule"), {"type": "worn_type", "operator": "eq", "value": "shorts"}),
              P("You're in the shorts. His rule. He sees them and his count slows before he's started.")),
            G(cond(flag("mark_dress_rule"), {"type": "worn_type", "operator": "neq", "value": "shorts"}),
              D(M, "That's not what I asked you to wear to my table.")),
            G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), D(M, "That's what you wear to my table?")),
            G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "worn_exposure", "operator": "eq", "value": 0}),
              D(M, "Sit down. You're making me lose count.")),
            G(cond({"type": "worn_exposure", "operator": "eq", "value": 1}, {"type": "worn_type", "operator": "neq", "value": "towel"}, {"type": "worn_type", "operator": "neq", "value": "sleep_shirt"}),
              D(M, "Your mother's out."), P("He doesn't tell you to cover up.")),
            G(cond(flag("mark_arrangement", False), SHORT), P("He counts it slow, and it's short, and he writes the gap on the envelope in pencil without a word.")),
            G(cond(flag("mark_arrangement"), SHORT), P("It's short, and he writes the gap on the envelope in pencil without a word.")),
            G(cond(flag("mark_arrangement", False), flag("rent_carried", False)), P("It's all there. He counts it twice anyway, because he wants to sit here longer.")),
            *STREAK_LINES, *PAYBACK_LINES,
            D(M, "Next Sunday. Same table."),
        ], count_exits("\"Count it, Mark.\"", None, 15, eff=[nadd(M, "want", 2)], node_="counted")),
        node("counted", "Counted", [
            P("He folds the rent into the envelope with Vance's name on it and leaves his hand flat on top of it."),
            # after his step 4, the arrangement (mark_sunday_table.md, signed 2026-11-01): normal speed, his eyes on
            # her, a new line a week from a shuffle bag of five
            G(cond(flag("mark_arrangement")), P("He counts it once, at normal speed, and his eyes don't go to the money once."),
              POOL(P("He slides the envelope across to you to check, and keeps his fingers on it a second after you've taken it."),
                   P("He doesn't say good morning. He says your name, once, and then he counts."),
                   P("He puts the pencil behind his ear and looks at you instead of writing anything down."),
                   P("He licks his thumb, and stops, and counts the rest without it."),
                   P("When you stand up he watches you all the way to the door. He doesn't pretend he isn't."),
                   pid="mark_table_after", bag=True)),
        ], [
            go("Leave him to his envelope.", loc="home_kitchen", mins=2),
        ]),
    ]})

# ── the three short Sundays (rent_short.md, signed 2026-11-01, DECISIONS 121): on the Sunday morning, before the
#    count (priority 7 over the table's 5). rent_carried is stamped at Sunday 00:00, so "under 12 hours" is this morning. ──
THIS_SHORT = [SHORT, {"type": "hours_since_flag", "subject": "player", "flag_key": "rent_carried", "operator": "lt", "value": 12}]
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
        P("Mark doesn't count it twice. He counts it once, and it's short, and he puts the envelope down."),
        D(M, "Then it's owed. Vance doesn't wait, so I don't."),
        P("He holds out his hand, palm up."),
        D(M, "Your door key. You get it back when you're square."),
        T("Anyone can open your door now. Anyone in this house."),
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
        P(f"He doesn't shout. He gets up, goes upstairs, and comes back down with the {nm} over his arm. The one you bought.")))
    TAKE_LINES.append(G(cond(*items, {"type": "clothing_item", "item_id": item, "operator": "equipped"}),
        P(f"He doesn't shout. He holds his hand out across the table for the {nm} you've got on, and waits until you go and change and put it in his hand. The one you bought.")))
    TAKE_LINES.append(G(cond(*items),
        D(M, "Garage. On the table, then you get it back."),
        P("Through the kitchen window you watch him hang it on the nail by his workbench, where you'll see it every time you walk past.")))
    TAKE_EXITS.append(go("\"That's mine.\"", loc="home_kitchen", mins=5, cond_=cond(*items),
                         flags=[fset(f"garage_holds_{item}")], wardrobe=[{"action": "unequip", "item_id": item}], eff=[nadd(M, "power", 5)]))
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
    "description": "Vance at the front door the evening after a short Sunday. Clears rent_carried; Vance's Power +10 (each carried Sunday). At Power 60 he asks for her, not Mark.",
    # His row (ledger L23): the front door, Monday 18:00-19:00, the evening after a short Sunday. His face is
    # here; rent_carried is read for 48 hours (the engine stamps it at Sunday's count, v2.py:14462).
    "trigger": {"location": "home_front_door", "npc": V, "requires_npc": V, "is_repeatable": True, "priority": 6, "is_active": True,
                "schedules": [{"weekdays": [0], "start_time": "18:00", "end_time": "19:00"}],
                "conditions": cond(flag("rent_carried"), {"type": "hours_since_flag", "subject": "player", "flag_key": "rent_carried",
                                                          "operator": "lt", "value": 48}, flag("vance_met")), "max_triggers_per_day": 1},
    "nodes": [
        node("knock", "Vance", [
            P("Three knocks, slow and heavy, the way a man knocks on a door he owns. Mr. Vance is on the step in his cardigan, with an envelope in his hand."),
            G(cond(ntrait(V, "power", "lt", 60)),
              D(V, "Evening, Miss. Is your stepfather in? Tell him I came by about Sunday. He'll know."),
              P("He hands you the envelope. His fingers stay on it a second after yours close.")),
            G(cond(ntrait(V, "power", "gte", 60)),
              D(V, "I didn't come for Mark. I came for you, Miss. You're the one who pays in that house now, aren't you?"),
              P("He looks past you into the hall, then back at you, slow: your legs, your chest, all the way down and up. He wets his lips."),   # copy fix A18 (DECISIONS 125)
              D(V, "Come and see me one evening. We'll talk about what's owed.")),
            G(cond(ntrait(V, "want", "gte", 30)), P("He doesn't look at your face once while he says it.")),
            G(cond(trait("rent_late_fee", "gt", 0)), D(V, "Fifteen on top, Miss. That's how it works.")),
            T("A short week, and it comes to the door."),
        ], [
            go("\"Mark will pay.\" Close the door.", node="shut", mins=5, eff=[nadd(V, "power", 10)], flags=[funset("rent_carried")]),
            go("\"Maybe one evening.\"", node="maybe", mins=5, cond_=cond(ntrait(V, "power", "gte", 60)),
               eff=[nadd(V, "power", 10), nadd(V, "want", 3)], flags=[funset("rent_carried")]),
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
MARK_STATE_LINES = [
    G(cond(SLEEP_SHIRT), P("His thumb works at the edge of whatever he's holding. His eyes are on the hem of your sleep shirt.")),
    G(cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"}), D(M, "That's what you wear in my house?")),
    G(cond({"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}, {"type": "worn_exposure", "operator": "eq", "value": 0}), D(M, "Sit down. You're making me lose my place.")),
    G(cond({"type": "clothing_slot", "slot": "bra", "operator": "equipped"}, {"type": "clothing_slot", "slot": "underwear", "operator": "equipped"},
           {"type": "clothing_slot", "slot": "top", "operator": "unequipped"}, {"type": "clothing_slot", "slot": "bottom", "operator": "unequipped"},
           {"type": "clothing_slot", "slot": "dress", "operator": "unequipped"}),
      P("You're in your underwear. He doesn't tell you to cover up.")),
    G(cond(NORMAL_ON), D(M, "Tips any good? Sunday's coming.")),
    G(cond(SEXY_ON), D(M, "Where's a waitress get twenties, wearing that?")),
]
LEAKS_LATE = [
    G(cond(trait("mark_step", "eq", 1)), P("His eyes go to your hem and back to the TV, every time you move.")),
    G(cond(trait("mark_step", "eq", 3)), P("He stays up later than he used to.")),
    G(cond(trait("mark_step", "eq", 4)), P("He watches you from the couch the way he watches the game. He doesn't pretend not to.")),
]
LEAKS_GARAGE = [
    # the leak before his step 4 (npc_mark.md, release 1): he can't hold her look
    G(cond(trait("mark_step", "eq", 3)), P("He can't hold your look. He looks at the bench instead.")),
]
LEAKS_KITCHEN = [
    G(cond(trait("mark_step", "eq", 2)), P("His eyes go to your hem and stay, the way they did at the first count.")),
]
# ── the towel at home (LO, 2026-10-31, DECISIONS 98): his reaction by his Dominance, every visit, in his
#    hub's own bands (<40, 40-59, 60+); "Let it slip." (Daring) pays his Dominance +2 once a day; "Drop it."
#    needs Showing and his top band, no story step (LO, 2026-10-31). Living room and kitchen only (LO:
#    bedroom and garage out). ──
MARK_TOWEL_LEAD = [P("You loosen the tuck and let the towel slip. It drops to your waist before you catch it, and your tits are out in front of him, wet and bare, your nipples hard.")]
MARK_TOWEL_SLIP = [
    [P("Mark looks straight at your tits for one second, then at the wall."), D(M, "Cover yourself. Now."),
     P("You pull the towel back up. He doesn't look at you again until you've gone.")],
    [P("Mark doesn't look away. He looks at your tits like he's pricing them, slow, and the can stops halfway to his mouth."),
     D(M, "Cover up before your mother sees."), P("He waits until you do. He watches you do it.")],
    [P("Mark looks at your bare tits and leans back."), D(M, "Did I say you could cover up?"),
     P("You hold the towel at your waist with your tits out. He looks for as long as he likes, and then he nods, and you're allowed.")],
]
MARK_TOWEL_DROP = [
    P("You undo the knot and let the towel drop to the floor. You're naked in his house, still wet from the shower. Your tits are bare and your nipples are hard. Your cunt is bare. Mark looks at your tits, then down at your cunt, and he takes his time about it. His cock is hard in his jeans, and he doesn't hide it. He puts the beer down."),
    D(M, "Turn round."),
    P("You turn round. You show him your bare ass, wet from the shower, and you hold still while he looks at it."),
    D(M, "Pick it up. Slowly."),
    P("You bend and pick the towel up off the floor with your ass to him, slow, the way he said, and you feel his eyes on your cunt the whole way down."),
]


# reader a3 #5-6 (DECISIONS 131): "Get dressed." after "Come here." / "Stand there." (his Power 60+, her in the towel)
MARK_TOWEL_NO = [
    P("You hitch the towel tighter over your tits and turn for the stairs."),
    D(M, "Suit yourself."),
    P("He says it to your back. His eyes stay on the backs of your bare thighs all the way to the door, and he doesn't call you back."),
]


def mark_towel(cid, loc):
    return towel_set(
        cid, M, "power", 40, 60, "mark_towel_today", [npc_add(M, "power", 2), EXH1], loc,   # her slip pays her, like Ryan's (DECISIONS 124)
        lines=[
            [D(M, "Get dressed. This isn't a hotel."),
             GC(cond(TOWEL_ON), P("Mark looks at the towel, then at his beer."), D(M, "Put something on, @player.")),
             D(M, "Your mother lets you walk round like that?")],
            [P("Mark's eyes go down the towel to your thighs and stay there, too long for a step-father."),
             GC(cond(TOWEL_ON), D(M, "That's all you've got on."), P("It isn't a question. He doesn't look away.")),
             P("He looks at you over the rim of the can, slow, from your wet feet to the knot over your tits.")],
            [GC(cond(TOWEL_ON), D(M, "Stand there. Let me look at you."), P("He doesn't tell you to get dressed. He tells you where to stand.")),
             GC(cond(TOWEL_ON), D(M, "Don't you dare go and change."), P("His eyes stay on the knot over your tits.")),
             GC(cond(TOWEL_ON), P("He looks at the towel like it belongs to him, and what's under it too."), D(M, "Come here."))],
        ],
        slip=MARK_TOWEL_SLIP, slip_lead=MARK_TOWEL_LEAD,
        slip_media=VID("a young woman letting her bath towel slip off her breasts in front of an older man on a couch", "girl drops towel in front of older man", "towel slip flash stepdad", pool_dir="sex/towel_mark_slip_t4"),
        slip_gate=(DARING, flag("mark_saw_her")), drop=MARK_TOWEL_DROP, drop_gate=[SHOWING, flag("mark_saw_her")],   # his chosen acts follow his accident (H2, DECISIONS 124)
        drop_media=VID("a young woman standing naked with her bath towel on the floor, an older man looking at her", "girl drops towel naked older man", "towel drop naked stepdad", pool_dir="sex/towel_mark_drop_t4"),
        caught_by=L, caught=TOWEL_CAUGHT,
        # reader a3 #5-6 (DECISIONS 131, call A): his order's no, in his top band; his Want +1 once a day
        no=("Hitch the towel up.", MARK_TOWEL_NO, "home_ella_room", "Go up to your room."))


def mark_hub(cid, loc, name, setting, extra=(), awake=True, leaks=(), items=(), leave="Leave him to it.", leave_to="home_hall", towel=False):
    choices, nodes = [], []
    t_blocks, t_choices, t_nodes = mark_towel(cid, loc) if towel else ([], [], [])
    for args, kw in items:
        c, n = item(*args, **kw); choices += c; nodes += n
    return {"id": cid, "name": name,
            "description": f"Mark's hub: {setting}. His Want and Power colour it; his lines read what she wears.",
            "trigger": {"location": loc, "npc": M, "requires_npc": M, "is_repeatable": True, "priority": 6,
                        "is_active": True, "conditions": cond(flag("opening_done"))},
            "nodes": [node("hub", name, [*extra] + ([*MARK_STATE_LINES, *leaks,
                G(cond(ntrait(M, "power", "lt", 40)), P("He doesn't give you orders any more. He waits to hear what you want.")),
                G(cond(ntrait(M, "power", "gte", 60)), P("He looks at you like you're one more thing in this house that's his.")),
                G(cond(ntrait(M, "want", "gte", 50)), T("He wants you. He's stopped trying to hide it from you, only from her.")),
                *t_blocks,
            ] if awake else []), choices + t_choices + [go(leave, loc=leave_to)])] + nodes + t_nodes}

LR = "home_living_room"
out.append(mark_hub("hub_mark_living_room", LR, "Mark, up late", "the living room late", [
    P("Mark is on the couch with the TV low and a beer on his knee."),
    G(cond(LAURA_IN_BED), P("Laura's gone up."), D(M, "Shut the door. Your mother's upstairs.")),
    POOL(D(M, "Can't sleep, @player?"), D(M, "Sit if you're sitting. Don't hover."), pid="mark_late_lines"),
], leaks=LEAKS_LATE, towel=True, items=[
    (("beer", "Have a beer with him.", [], "had_drink_home", LR,
      [P("The game on low."), G(cond(LAURA_IN_BED), D(M, "Laura's upstairs. Keep it down.")), P("He hands you a can without asking.")],
      None, 30),
     dict(done_exits=[go("Done.", loc=LR, mins=30, flags=[fset("had_drink_home")], mods=DRINK)],   # plain: no Lust (DECISIONS 128)
          tease=m_tease(108, "late TV and a beer", "Curl up on the couch."), touch=m_paid(108, "late TV and a beer"))),
    (("film", "Put a film on with him.", [tod("22:00", "00:00")], "movie_night", LR,
      [P("He lets you pick. He falls asleep in the second half, and you watch the end with his snoring for a soundtrack.")],
      [energy(5)], 120), {}),
]))
# Watch TV with him (DECISIONS 85-86): the same remote as alone (home.py), his line on each channel,
# and on channel 5 his reaction by his step. "Leave it on." pays more than alone, once a day (LO, 2026-10-30,
# DECISIONS 92): her Corruption +2 (cap 19 / 39) and his Want +2; after that it plays and pays nothing.
MARK_TV_ADULT = ("Channel 5 fills the screen. A woman is on her knees in front of a man. She sucks his cock, slow and deep, her cheeks hollow. He pulls her up and bends her over the bed. He takes her from behind. Her tits swing with every thrust. She moans, loud and long. The room goes quiet under the sound. Mark stops with the beer halfway to his mouth. He does not reach for the remote. His fingers squeeze tight around the can. On screen the man grips her hips and drives in harder. Your face goes hot. You are wet, and your nipples pull hard and tight.")
MARK_TV_LEAVE = ("You leave it on. You both watch. On screen the man drives into her from behind. He slaps her ass, hard, and she moans. Her tits swing under her with each thrust. Mark shifts on the couch. The can moves down to his lap. It does not hide the hard bulge of his cock in his jeans. His eyes go from the screen to you. Then back to the screen. Nobody says anything. The man grips her hips and pounds her harder. She moans louder with every thrust. You are wet. You squeeze your thighs together, tight. Your nipples go hard and tight.")
MARK_CH = {"news": D(M, "Same as yesterday. Same as every day."), "cooking": D(M, "Your mother never cooks like that."),
           "sports": D(M, "Watch this. Watch. Ah, for God's sake."), "film": D(M, "Seen it. He dies at the end.")}
_hub = out[-1]
assert _hub["id"] == "hub_mark_living_room"
_hub["nodes"][0]["choices"].insert(-1, go("Watch TV with him.", node="mremote"))
_hub["nodes"] += [node("mremote", "The remote", [
        P("You take the other end of the couch, and he hands you the remote without looking."),
    ], remote_choices("mch_", "madult", adult_cond=cond(flag("mark_saw_her"))) + [go("Leave him to it.", loc="home_hall")])]   # reader a3 #1 (DECISIONS 131): channel 5 beside him after his accident, like "Leave it on."
for cid, btn, lines, desc, qs, pool in CHANNELS:
    _hub["nodes"].append(node(f"mch_{cid}", btn.split(": ", 1)[1].rstrip(".").capitalize(),
        [POOL(*[P(x) for x in lines]), MARK_CH[cid], VID(desc, *qs, pool_dir=pool.replace("tv/", "tv/mark_"))],
        [*watch_plain(LR), go("Change the channel.", node="mremote"), go("Leave him to it.", loc="home_hall")]))
_hub["nodes"] += [
    node("madult", "Channel 5", [P(MARK_TV_ADULT),
        G(cond(trait("mark_step", "lt", 4)), D(M, "Change it, @player."), P("He says it. He doesn't reach for the remote.")),
        G(cond(trait("mark_step", "gte", 4)), P("He doesn't tell you to change it. He watches the screen, and then he watches you watching it.")),
        VID("porn playing on a living room TV at night, a man and a woman, seen from the couch", "porn on tv late night couch", "watching porn on tv with someone", pool_dir="sex/tv_adult_mark_t5")],
        [go("Leave it on.", node="mleave", mins=5, cond_=cond(CURIOUS, flag("mark_saw_her"))),   # porn beside him is a chosen act for one: Curious (DECISIONS 124)
         go("Change the channel.", node="mremote"), go("Leave him to it.", loc="home_hall")]),
    node("mleave", "Leave it on", [P(MARK_TV_LEAVE),
        VID("a man on a couch at night watching porn on TV, a beer can in his lap", "man watching porn tv couch beer", "stepdad watching porn on tv", pool_dir="sex/tv_adult_mark_leave_t5")],
        [   # (DECISIONS 124) "Leave it on." needs Curious, so the Good Girl pay row is gone
         go("Keep watching.", loc=LR, mins=25, eff=tv_pay(2, 39) + [want(M, 2)], flags=[fset("mark_tv_paid")],
            cond_=cond(TV_CUR, flag("mark_tv_paid", False))),
         go("Keep watching.", loc=LR, mins=25, cond_=cond(flag("mark_tv_paid"))),
         go("Change the channel.", node="mremote")]),
]

# Sun 00:00-01:00 Mark and Laura are awake (DECISIONS 80): the "asleep" line skips that hour, written
# once per piece of the night because conditions do not nest.
ASLEEP_HOURS = [(wd(0, 1, 2, 3, 4, 5), tod("22:00", "07:00")), (wd(6), tod("22:00", "00:00")), (wd(6), tod("01:00", "07:00"))]
out.append(mark_hub("hub_mark_bedroom", "home_master_bedroom", "Mark, asleep", "their bed, at night", [
    *[G(cond(*hrs), P("Mark is asleep on his back on his side of the bed, snoring, one arm flung out. Even asleep he takes up most of it."))
      for hrs in ASLEEP_HOURS],
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
LAUNDRY_TEASES = [
    {"label": "Bend for the bottom drum.", "name": "The bottom drum",
     "gate": [CURIOUS, DARING, flag("mark_saw_her"), PANTIES_ON, NO_TOWEL],   # seen and sexual: both meters (meters.md rule 4)
     "eff": [want(M, 3), {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 39}],
     "blocks": [*[GC(cond(_wt(t)), P(beat(MLT, "daring_skirt"))) for t in ("short_skirt", "laura_dress", "party_dress", "cafe_uniform")],
                GC(cond(SLEEP_SHIRT), P(beat(MLT, "daring_shirt"))),
                *[GC(cond(_wt(t)), P(beat(MLT, "daring_jeans"))) for t in ("jeans", "leggings", "shorts")],
                VID("a girl bending over to load a front-loading washer, her skirt riding up, a man at a workbench watching", "girl bends over washing machine skirt rides up", "bending over laundry panties showing", pool_dir="sex/mark_laundry_bend_t4")]},
    {"label": "Wash what you're wearing.", "name": "In the wash",
     "gate": [BOLD, SHOWING, flag("mark_saw_her"), {"type": "clothing_slot", "slot": "top", "operator": "equipped"},
              {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}],
     "eff": [want(M, 4), {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 59},
             {"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": 59}],
     "wardrobe": [{"action": "unequip", "item_id": g} for g in ("tshirt", "thin_top")],   # the top is in the washer
     "blocks": [P(beat(MLT, "bold")),
                VID("a girl in her bra by a running washing machine in a garage, a man at a bench staring", "girl in bra doing laundry garage", "topless laundry bra man watching", pool_dir="sex/mark_laundry_wash_t4")]},
]
G_ = "home_garage"
out.append(mark_hub("hub_mark_garage", G_, "Mark, in the garage", "the garage", [
    P("Mark's at his bench with the radio on, doing something to an engine part that doesn't need doing."),
    POOL(D(M, "Hand me that wrench. No, the other one."), D(M, "Don't touch anything."), D(M, "What do you want? I'm busy."), pid="mark_garage_lines"),
], leaks=LEAKS_GARAGE, items=[
    (("laundry", "Do your laundry while he works.", [tod("07:00", "21:00")], "did_laundry", G_,
      [D(M, "Whites with whites, @player."), P("He watches you load the machine like you're going to break it.")],
      [energy(-5)], 30),
     dict(plain_costs=[{"trait": "energy", "value": 5}],
          tease=LAUNDRY_BASKET, teases=LAUNDRY_TEASES)),
]))
K = "home_kitchen"
out.append(mark_hub("hub_mark_kitchen", K, "Mark, in the kitchen", "the kitchen", [
    G(cond(wd(2), tod("17:00", "20:00")), P("Wednesday. Mark's cooking, badly, with a beer on the counter and the extractor fan roaring."), D(M, "It's chilli. It's always chilli.")),
    G(cond(wd(2), tod("20:00", "22:00")), P("Wednesday. The chilli pan is soaking in the sink and Mark's at the table with a beer.")),
    G(cond(wd(6), tod("08:00", "18:00")), P("Sunday. Mark's at the table with the paper and his coffee, in the chair at the head of it.")),
    G(cond(wd(6), tod("08:00", "12:00")), D(M, "Morning.")),
    G(cond(wd(0, 1, 3, 4), tod("18:00", "19:00")), P("Mark's at the table for dinner, sleeves rolled, already eating.")),
], leaks=LEAKS_KITCHEN, towel=True, items=[
    (("breakfast", "Sunday breakfast with him.", [wd(6), tod("08:00", "11:00")], "ate_breakfast", K,
      [P("He slides the paper over."), G(cond(flag("rent_starts"), flag("sunday_counted_today", False)), D(M, "Eat, @player. Then the rent.")),
       G(cond(flag("sunday_counted_today")), D(M, "Eat, @player.")), G(cond(flag("rent_starts", False)), D(M, "Eat, @player."))],
      [energy(10)], 15),
     dict(tease=m_tease(104, "Sunday breakfast"), touch=m_paid(104, "Sunday breakfast"))),
    (("dinner", "Sit down to dinner.", [wd(0, 1, 2, 3, 4, 6), tod("18:00", "20:00")], "ate_dinner", K,
      [G(cond(wd(0, 1, 3, 4, 6)), P("Burnt chops."), D(M, "Your mother cooks. I fill plates.")),
       G(cond(wd(2)), P("Chilli, again."), D(M, "It's always chilli. Eat it.")),
       G(cond(here(L, K)), P("Laura sits across from him and asks you about college before he can say anything else.")),
       G(cond(here(R, K)), P("Ryan eats beside you like he's late for something."))],
      [energy(15)], 30),
     dict(tease=m_tease(105, "dinner", "Eat slowly for him."))),
    (("cook", "Help him cook.", [wd(2), tod("18:00", "19:00")], "helped_cook", K,
      [D(M, "Hand me the salt. No, the other salt.")],
      [energy(-5)], 30),
     dict(plain_costs=[{"trait": "energy", "value": 5}], tease=m_tease(106, "help him cook", "Reach past him for the pan.", bold=True))),
    (("dishes", "Do the dishes with him.", [wd(2, 6), tod("19:00", "21:00")], "did_dishes", K,
      [P("He dries, slow."), D(M, "You missed one.")],
      [energy(-5)], 20),
     dict(plain_costs=[{"trait": "energy", "value": 5}],
          tease=m_tease(107, "dishes", "Bend to the dishwasher."), touch=m_paid(107, "dishes", "Stay bent."))),
]))

cards = step_cards(M, {
    1: ("Sunday. Mark counts the rent at the kitchen table.", "Sunday morning: the kitchen, while Mark counts the rent"),
    2: ("His eyes were on your hem at the count. He's on the phone a lot, late.", "Late at night: the kitchen drawer, Mark next door"),
    3: ("\"Friday, Frank.\" He knows you heard. Sunday's coming.", "Sunday morning at the table, after a short week"),
    4: ("He can't hold your look at the table. He wants to talk terms.", "An evening in the garage, after a late night in Ryan's room"),
}, terminal_text=("The Sunday table, every week: his eyes on you.", "Mark, later. (After the house is yours.)"),
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
out.append({
    "id": "mark_00_the_dryer", "name": "The washer hose",
    "description": "Mark's first accident (DECISIONS 124): Saturday in the garage, the washer hose soaks her; he looks, then turns his back and holds out a towel. His Want +5 and mark_saw_her either way; her \"Don't take it yet.\" pays Exhibitionism +1, cap 19.",
    "trigger": {"location": "home_garage", "npc": M, "requires_npc": M, "is_repeatable": False, "priority": 9, "is_active": True,
                "consume_on": "exit",
                "schedules": [{"weekdays": [5], "start_time": "09:00", "end_time": "17:00"}],
                "conditions": cond(flag("opening_done"), flag("mark_saw_her", False))},
    "nodes": [
        node("hose", "The washer hose", [
            GC(cond(BRA_ON), P(beat("mark_00_the_dryer", "hose_bra"))),
            GC(cond(BRA_OFF), P(beat("mark_00_the_dryer", "hose_nobra"))),
        ], [
            go("Take the towel.", node="covered", mins=2),
            go("Don't take it yet.", node="stay", mins=2),
        ]),
        node("covered", "Back to his bench", [P(beat("mark_00_the_dryer", "covered"))],
             [go("Go and change.", loc="home_hall", mins=10, consumes=True, eff=SAW, flags=SAW_FLAGS)]),
        node("stay", "Not yet", [P(beat("mark_00_the_dryer", "stay"))],
             [go("Go and change.", loc="home_hall", mins=10, consumes=True, flags=SAW_FLAGS,
                 eff=SAW + [{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 19}])]),
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
