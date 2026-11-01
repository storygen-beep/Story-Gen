"""Town and the street, iteration 002 part 5: the random town events (the street sheet), Zoe's flat
when Zoe isn't in the room (zoe_kitchen.md, zoe_bathroom.md, zoe_apartment.md), the corner shop's
grocery run (corner_shop.md; home_life.md item 15), and the cocky guy's face at Zoe's party (his rows,
ledger 26: a face that isn't only the heat one)."""
from canv import *
from tomlw import tod, wd
from home_items import CURIOUS, DARING, here, nobody, placeholder

out = []
Z, V, COCKY = "npc_zoe", "npc_vance", "npc_cocky_guy"
SKIRT = {"type": "worn_type", "operator": "eq", "value": "short_skirt"}
NO_BRA_DRESSED = [{"type": "clothing_slot", "slot": "bra", "operator": "unequipped"},
                  {"type": "worn_exposure", "operator": "eq", "value": 0}]
EXH1 = {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 59}
DRINK_MOD = [{"key": "drinks_boost", "name": "Tipsy", "duration_hours": 3, "trait_offsets": {"corruption": 20, "exhibitionism": 20}}]


# ═════════════════════════════════════════════════════════════════════════════
# RANDOM EVENTS IN TOWN (street.md "Random events in town"): 1 in 4 when she comes out onto the
# street, one a day (`town_event`, cleared at midnight). When nothing rolls, nothing shows.
# ═════════════════════════════════════════════════════════════════════════════
def town_event(cid, name, sched, conds, blocks, plain, plain_eff=(), bolder=None):
    # the plain answer is free of every cap (gate: a spent day still has a door); the canvas itself is once a day
    exits = [go(plain, loc="street", mins=2, eff=list(plain_eff), flags=[fset("town_event")])]
    if bolder:
        label, gate, eff, text = bolder
        exits.append(go(label, node="bolder", mins=2, cond_=cond(flag("town_event", False), *gate), eff=eff, flags=[fset("town_event")]))
    nodes = [node("event", name, blocks, exits)]
    if bolder:
        nodes.append(node("bolder", label.rstrip("."), [P(bolder[3])], [go("Walk on.", loc="street", mins=2)]))
    t = {"location": "street", "is_repeatable": True, "priority": 4, "is_active": True, "trigger_mode": "random",
         "chance": 0.25, "conditions": cond(flag("opening_done"), flag("town_event", False), *conds)}
    if sched:
        t["schedules"] = sched
    return {"id": cid, "name": name, "description": f"Random event in town (street.md): {name}. 1 in 4, one a day.",
            "trigger": t, "nodes": nodes}


ALL = [0, 1, 2, 3, 4, 5, 6]
S = lambda a, b, days=ALL: [{"weekdays": days, "start_time": a, "end_time": b}]
out.append(town_event("town_event_wind", "The wind and your skirt", S("07:00", "22:00"), [SKIRT],
    [P("A gust comes down the street and gets right under your skirt and lifts it, all the way, for a second and a half. Your ass is out to the whole street. Across the road a man stops dead with his keys in his hand.")],
    "Grab the hem. Too late.",
    bolder=("Let it blow.", [trait("exhibitionism", "gte", 40)], [EXH1],   # her underwear, held up for one man: Showing (DECISIONS 124)
            "You don't grab it. You let the wind have it for a second longer, your ass on show to the road, and the man across the road walks into a bin. Then you push the hem down. That's all he gets today.")))
out.append(town_event("town_event_whistle", "A car slows down", S("07:00", "22:00"), NO_BRA_DRESSED,
    [P("A car slows down beside you. The window's down, and a guy leans across the passenger seat and whistles, long, at your tits, loose under your clothes. \"Get in, baby. I'll give you a ride.\" Not a chance.")],
    "Walk faster.",
    bolder=("Turn and let him look.", [CURIOUS, DARING], [EXH1],
            "You stop and turn to face the car. You let him look at your tits, nipples hard through the cloth, for as long as the light's red. He forgets to drive when it changes.")))
out.append(town_event("town_event_vance", "Vance on his porch", S("18:00", "22:00"), [here(V, "vance_house"), flag("vance_met")],
    [P("Mr. Vance is on his porch with his paper. He lowers it when you pass."), D(V, "Evening, Miss."),
     P("He watches you all the way past his gate.")],
    "\"Evening.\"",
    bolder=("Slow down for him.", [CURIOUS], [{"targetType": "npc", "npcId": V, "trait": "want", "op": "add", "value": 2, "cap": 100}],
            "You slow down by his gate and take your time going past, and he doesn't even pretend to read. His eyes are on your ass the whole way. He opens his mouth to call you up the steps, and you're already past the hedge.")))
out.append(town_event("town_event_jogger", "A jogger looks back", S("07:00", "10:00"), [],
    [P("A jogger goes past in the other direction, and looks back over his shoulder at you, twice.")],
    "Pretend you didn't see.",
    bolder=("Look back.", [CURIOUS], [], "You look back, and catch him doing it a third time, eyes on your ass. He nearly runs into a lamp post. He slows like he might turn round. You turn the corner first.")))
out.append(town_event("town_event_quiet", "The street, quiet", None, [],
    [P("Nothing happens. A dog barks two gardens down.")], "Walk on."))

# ═════════════════════════════════════════════════════════════════════════════
# ZOE'S FLAT, WHEN ZOE ISN'T IN THE ROOM
# ═════════════════════════════════════════════════════════════════════════════
PARTY_NIGHT = [{"weekdays": [4], "start_time": "19:00", "end_time": "00:00"}, {"weekdays": [5], "start_time": "00:00", "end_time": "02:00"}]
out.append({
    "id": "zoe_kitchen_drink", "name": "Get a drink",
    "description": "Zoe's kitchen on party night: a drink, as the party's (drinks_tonight +1, the boost), three a night (zoe_kitchen.md).",
    "trigger": {"location": "zoe_kitchen", "is_repeatable": True, "priority": 4, "is_active": True, "schedules": PARTY_NIGHT,
                "conditions": cond(trait("drinks_tonight", "lt", 3))},
    "nodes": [node("counter", "The counter", [
        P("The counter is a wall of bottles and red cups. Somebody's mixing something blue in a mixing bowl."),
        G(cond(trait("drinks_tonight", "eq", 2)), T("That'd be three. You'll feel it tomorrow.")),
    ], [
        go("Pour one.", loc="zoe_kitchen", mins=10, cond_=cond(trait("drinks_tonight", "lt", 2)), mods=DRINK_MOD, eff=[add("drinks_tonight", 1)]),
        go("Pour one. (your third)", loc="zoe_kitchen", mins=10, cond_=cond(trait("drinks_tonight", "eq", 2)), mods=DRINK_MOD,
           eff=[add("drinks_tonight", 1)], flags=[fset("heavy_night")]),
        go("Back to the party.", loc="zoe_apartment"),
    ])]})
out.append({
    "id": "zoe_kitchen_quiet", "name": "Get a glass of water",
    "description": "Zoe's kitchen on an ordinary evening: a glass of water, one line, writes nothing (zoe_kitchen.md).",
    "trigger": {"location": "zoe_kitchen", "is_repeatable": True, "priority": 3, "is_active": True,
                "schedules": [{"weekdays": [0, 1, 2, 3], "start_time": "18:00", "end_time": "00:00"},
                              {"weekdays": [4, 5], "start_time": "18:00", "end_time": "19:00"},
                              {"weekdays": [5], "start_time": "19:00", "end_time": "00:00"}]},
    "nodes": [node("sink", "The sink", [
        P("You run the tap until it's cold and drink a glass of water at the sink, looking at the photos on Zoe's fridge. Half of them are parties."),
        G(cond(flag("party_went")), P("You're in two of the new ones.")),
    ], [go("Done.", loc="zoe_apartment", mins=5)])]})
out.append({
    "id": "zoe_bathroom_face", "name": "Fix your face",
    "description": "Zoe's bathroom: fix your face in her mirror, hygiene +5, once a night; on party night, the queue (zoe_bathroom.md).",
    "trigger": {"location": "zoe_bathroom", "is_repeatable": True, "priority": 4, "is_active": True},
    "nodes": [node("mirror", "Her mirror", [
        P("Zoe's mirror is ringed with bulbs, and the shelf under it holds more make-up than a shop."),
        G(cond(wd(4), tod("19:00", "00:00")), P("Somebody's banging on the door before you've even shut it. \"Two minutes!\" you shout back.")),
        G(cond(wd(5), tod("00:00", "02:00")), P("Somebody's banging on the door before you've even shut it. \"Two minutes!\" you shout back.")),
    ], [
        go("Fix your face.", loc="zoe_apartment", mins=10, cond_=cond(flag("zoe_face_today", False)), flags=[fset("zoe_face_today")],
           eff=[{"targetType": "player", "trait": "hygiene", "op": "add", "value": 5, "cap": 100}]),
        go("Leave it.", loc="zoe_apartment"),
    ])]})
out.append({
    "id": "zoe_couch_alone", "name": "Sit on her couch",
    "description": "Zoe's living room while Zoe is in her bedroom (Mon-Thu 22:00-00:00): her couch, alone (zoe_apartment.md).",
    "trigger": {"location": "zoe_apartment", "is_repeatable": True, "priority": 3, "is_active": True,
                "conditions": cond(here(Z, "zoe_apartment", False))},
    "nodes": [node("couch", "Her couch", [
        P("You sit on Zoe's couch under the fairy lights."),
        G(cond(here(Z, "zoe_bedroom")), P("Her door's half shut down the hall, her music low behind it.")),
        G(cond(here(Z, "zoe_bedroom", False)), P("The flat's quiet without her. Her music's off, for once.")),
    ], [go("Sit a while.", loc="zoe_apartment", mins=20), go("Go.", loc="town")])]})

# ═════════════════════════════════════════════════════════════════════════════
# THE CORNER SHOP: Laura's list (corner_shop.md; home_life.md:100). The shop opens on her map only on
# an errand (world_data.py entry_conditions); the money is Laura's twenty.
# ═════════════════════════════════════════════════════════════════════════════
out.append({
    "id": "corner_shop_list", "name": "Buy Laura's list",
    "description": "The grocery run: 15 minutes, money -20 (Laura's twenty), groceries_bought set. Only while the list is in her pocket.",
    "trigger": {"location": "corner_shop", "is_repeatable": True, "priority": 4, "is_active": True,
                "conditions": cond(flag("grocery_list"), flag("groceries_bought", False))},
    "nodes": [node("till", "The till", [
        P("Bread, milk, eggs, the wine Laura likes, the washing powder she always forgets. The clerk scans it all without looking up from his phone and bags it in two thin bags that will definitely split."),
    ], [go("Pay with Laura's twenty ($20).", loc="street", mins=15, costs=[{"trait": "money", "value": 20}],
           eff=[add("money", -20)], flags=[fset("groceries_bought")]),
        go("Not now.", loc="street")])]})

# ═════════════════════════════════════════════════════════════════════════════
# THE COCKY GUY AT ZOE'S PARTY (his rows: Fri 23:00-00:00, Sat 00:00-02:00, once met; ledger 26).
# A face that isn't only the heat one; party_hookup stays his heat.
# ═════════════════════════════════════════════════════════════════════════════
out.append({
    "id": "hub_cocky_party", "name": "The cocky guy",
    "description": "Jake's teammate at Zoe's party late, leaning on the wall by the bathroom: talk.",
    "trigger": {"location": "zoe_apartment", "npc": COCKY, "requires_npc": COCKY, "is_repeatable": True, "priority": 5,
                "is_active": True, "conditions": cond(flag("cocky_guy_met"))},
    "nodes": [node("wall", "By the bathroom", [
        P("The cocky guy from figure drawing is leaning on the wall by Zoe's bathroom with a beer he's barely touched. His eyes drop to your tits while you walk up, and he doesn't bother pretending they didn't."),
        POOL(D(COCKY, "There she is. Sit with me. Out here I don't bite. In there, ask me."), D(COCKY, "You draw like a girl who's never been drawn. Give it time."),
             pid="cocky_lines"),
        # "Not yet" only on a night she hasn't gone in with him (hookup_today, set by party_hookup's "Lead the way.").
        # Friday before midnight only: hookup_today is a daily flag (0_systems_spec.toml daily unset), so past the
        # day's turn it can't say whether she went with him at 23:30.
        G(cond(flag("hookup_today", False), wd(4), tod("19:00", "00:00")),
          P("He pats the wall next to him, not the bathroom door behind it. Not yet.")),
    ], [go("Talk with him a while.", loc="zoe_apartment", mins=20), go("Walk past him.", loc="zoe_kitchen", mins=2)])]})

text = ("# =============================================================================\n"
        "# First Term — 5 · scenes · TOWN (iteration 002, part 5): random town events, Zoe's flat alone,\n"
        "# the corner shop's grocery run, the cocky guy at the party. Source: iterations/002/build_scripts/town.py.\n"
        "# =============================================================================\n")

# ── the street sees what she wears (street_seen.md, signed 2026-11-01; meters.md rule 2; DECISIONS 121) ──
# Once a day (out_shown_today, cleared in the daily tick). The first day out in each level pays both meters;
# every day after, Exhibitionism only. One witness by the hour: Mr. Vance on his porch (his 18:00-22:00 row),
# the corner-shop guy by day, a car slowing down at night.
VANCE_PORCH = {"type": "npc_at_location", "location_id": "vance_house", "npc_id": "npc_vance", "operator": "is_present"}
VANCE_AWAY = {"type": "npc_at_location", "location_id": "vance_house", "npc_id": "npc_vance", "operator": "is_absent"}
SKIRT_ON = {"type": "worn_type", "operator": "eq", "value": "short_skirt"}
SKIRT_OFF = {"type": "worn_type", "operator": "neq", "value": "short_skirt"}
BRA_OFF = {"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}
BRA_ON = {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}
PANTIES_OFF = {"type": "clothing_slot", "slot": "underwear", "operator": "unequipped"}
PANTIES_ON = {"type": "clothing_slot", "slot": "underwear", "operator": "equipped"}
DAYTIME, NIGHT = tod("08:00", "18:00"), tod("22:00", "08:00")
CAFE_GIRL = G(cond(trait("cafe_footfall", "gte", 10)), WHO("You're the girl from the café."))
# (case, its worn items, level, Vance's line, the shop guy's line, the car's line)
STREET_CASES = [
    ("skirt", [SKIRT_ON, PANTIES_ON], 1,
     [D("npc_vance", "Mark's girl is growing up."), P("He doesn't pretend to read his paper. His eyes go up your legs to the hem of your skirt and stay there. He pats the step beside him. You keep walking.")],
     "The shop guy comes out from behind the counter to stack a box that doesn't need stacking, and watches your legs in that skirt all the way past. He starts to say something. You're gone before he finds it.",
     "A car slows beside you. The window comes down halfway, and the driver is looking at your legs, not your face. It stays with you to the end of the street. You never look in, and it goes."),
    ("nobra", [BRA_OFF, SKIRT_OFF, PANTIES_ON], 1,
     [P("Mr. Vance sets the paper down. He looks at your tits, at your nipples pushing at the cloth, and doesn't look away. He nods at the step beside him. Not tonight. You keep walking.")],
     "The shop guy comes out from behind the counter to stack a box that doesn't need stacking. His eyes are on your tits, loose under your clothes, all the way past. He starts to say something. You're gone before he finds it.",
     "A car slows beside you. The window comes down halfway, and the driver is staring at your tits. It stays with you to the end of the street. You never look in, and it goes."),
    ("nopanties", [PANTIES_OFF], 2,
     [P("A breeze comes down the street as you pass his gate, and there's nothing under your clothes to stop it. Your pussy is bare under there. Mr. Vance stands up off his chair with his eyes on your hips, and takes one step toward the gate. You don't stop. Not tonight.")],
     "The shop guy drops his change on the step and stares at your ass, like he knows there's nothing under your clothes. \"Come in a minute.\" You don't. He doesn't pick the change up until you've turned the corner.",
     "A car slows, then stops. Someone inside whistles at your ass. \"Get in.\" You don't walk faster, and you don't get in."),
]
for case, worn, lv, vance, shop, car in STREET_CASES:
    first = f"street_first_l{lv}"
    cap = 39 if lv == 1 else 59
    pay_first = [{"targetType": "player", "trait": "corruption", "op": "add", "value": 1, "cap": cap},
                 {"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": cap}]
    pay_after = [{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": cap}]
    exits = []
    for w_items, extra_eff in [([VANCE_PORCH], [nadd("npc_vance", "want", 2)]), ([VANCE_AWAY, DAYTIME], []),
                               ([VANCE_AWAY, NIGHT], []), ([VANCE_AWAY, tod("18:00", "22:00")], [])]:
        for is_first in (True, False):
            exits.append(go("Keep walking.", loc="street", mins=2, cond_=cond(*w_items, flag(first, not is_first)),
                            eff=(pay_first if is_first else pay_after) + extra_eff,
                            flags=[fset("out_shown_today")] + ([fset(first)] if is_first else [])))
    out.append({
        "id": f"street_seen_{case}", "name": "Somebody's looking",
        "description": f"The street sees what she's wearing ({case}): one witness a day by the hour; the first day out in level {lv} pays both meters, after that Exhibitionism (meters.md rule 2).",
        "trigger": {"location": "street", "is_repeatable": True, "priority": 3 + lv, "is_active": True, "max_triggers_per_day": 1,
                    "conditions": cond(flag("out_shown_today", False), *worn)},
        "nodes": [node("seen", "Somebody's looking", [
            G(cond(VANCE_PORCH), *vance, P("He'll be on his porch tomorrow evening. He always is.")),
            G(cond(VANCE_AWAY, DAYTIME), P(shop)),
            G(cond(VANCE_AWAY, NIGHT), P(car)),
            G(cond(VANCE_AWAY, tod("18:00", "22:00")), P(car)),
            CAFE_GIRL,
        ], exits)]})

text += "".join(emit(c) for c in out)
open(__import__("sys").argv[1], "w").write(text)
print("town:", len(out), "canvases")
