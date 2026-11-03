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
def town_event(cid, name, sched, conds, blocks, plain, plain_eff=(), bolder=None, plain_after=None):
    # the plain answer is free of every cap (gate: a spent day still has a door); the canvas itself is once a day.
    # plain_after: pass 3 D44 (the-surfaces.md R9): the plain answer's screen, his reaction or her body, not a toast
    exits = [go(plain, mins=2, eff=list(plain_eff), flags=[fset("town_event")],
                **(dict(node="plain") if plain_after else dict(loc="street")))]
    if bolder:
        label, gate, eff, text = bolder
        exits.append(go(label, node="bolder", mins=2, cond_=cond(flag("town_event", False), *gate), eff=eff, flags=[fset("town_event")]))
    nodes = [node("event", name, blocks, exits)]
    if plain_after:
        nodes.append(node("plain", plain.rstrip("."), list(plain_after), [go("Walk on.", loc="street")]))
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
    plain_after=[P("You slap the hem down with both hands, too late, your face on fire. The man across the road is still standing there with his keys, and he grins at you like you did it for him.")],
    bolder=("Let it blow.", [trait("exhibitionism", "gte", 40)], [EXH1],   # her underwear, held up for one man: Showing (DECISIONS 124)
            "You don't grab it. You let the wind have it for a second longer, your ass on show to the road, and the man across the road walks into a bin. Then you push the hem down. That's all he gets today.")))
out.append(town_event("town_event_whistle", "A car slows down", S("07:00", "22:00"), NO_BRA_DRESSED,
    [P("A car slows down beside you. The window's down, and a guy leans across the passenger seat and whistles, long, at your tits, loose under your clothes. \"Get in, baby. I'll give you a ride.\""),
     # reader a3 #49 (DECISIONS 131): her answer reads her stage. Under Showing it's a flat no; from E40 she likes the look, not the car.
     GC(cond(trait("exhibitionism", "lt", 40)), P("Not a chance.")),
     GC(cond(trait("exhibitionism", "gte", 40)), P("Not for a ride."))],
    "Walk faster.",
    plain_after=[P("You walk faster, but that's worse. Your tits bounce loose under your clothes with every step. The car crawls beside you to the end of the street, and he whistles again before it pulls away.")],
    bolder=("Turn and let him look.", [CURIOUS, DARING], [dict(EXH1, cap=39)],   # a Daring act stops at Daring's top (pass 3 G8)
            "You stop and turn to face the car. You let him look at your tits, nipples hard through the cloth, for as long as the light's red. He forgets to drive when it changes.")))
out.append(town_event("town_event_vance", "Vance on his porch", S("18:00", "22:00"), [here(V, "vance_house"), flag("vance_met")],
    [P("Mr. Vance is on his porch with his paper. He lowers it to look at your legs when you pass."), D(V, "Evening, Miss."),   # reader a3 #65 (DECISIONS 131)
     P("He watches you all the way past his gate.")],
    "\"Evening.\"",
    bolder=("Slow down for him.", [CURIOUS], [{"targetType": "npc", "npcId": V, "trait": "want", "op": "add", "value": 2, "cap": 100}],
            "You slow down by his gate and take your time going past, and he doesn't even pretend to read. His eyes are on your ass the whole way. He opens his mouth to call you up the steps, and you're already past the hedge.")))
out.append(town_event("town_event_jogger", "A jogger looks back", S("07:00", "10:00"), [],
    [P("A jogger goes past in the other direction, and looks back over his shoulder at your ass, twice.")],   # reader a3 #64 (DECISIONS 131)
    "Pretend you didn't see.",
    plain_after=[P("You keep your eyes front and pretend, but your face goes hot anyway, and you can feel exactly where on your ass his eyes landed, both times.")],
    bolder=("Look back.", [CURIOUS], [], "You look back, and catch him doing it a third time, eyes on your ass. He nearly runs into a lamp post. He slows like he might turn round. You turn the corner first. He runs this street in the mornings, and now he knows your ass by sight.")))   # reader pass 3 b01: the hook (his window is 07:00-10:00)
# S6 (LO 2026-11-03): no "Nothing happens." random event on the street either.

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
        # pass 3 D44 (the-surfaces.md R9): the drink lands on her body, not a toast (drinks_tonight is already counted)
        go("Pour one.", node="poured", mins=10, cond_=cond(trait("drinks_tonight", "lt", 2)), mods=DRINK_MOD, eff=[add("drinks_tonight", 1)]),
        go("Pour one. (your third)", node="poured", mins=10, cond_=cond(trait("drinks_tonight", "eq", 2)), mods=DRINK_MOD,
           eff=[add("drinks_tonight", 1)], flags=[fset("heavy_night")]),
        go("Back to the party.", loc="zoe_apartment"),
    ]),
        node("poured", "A red cup", [
            G(cond(trait("drinks_tonight", "lt", 3)), P("You pour something strong into a red cup and knock half of it back at the counter. It burns all the way down and sits warm in your stomach, and a minute later the music is louder and your cheeks are hot.")),
            G(cond(trait("drinks_tonight", "gte", 3)), P("Three. The kitchen tips when you turn your head, your lips have gone numb, and you're laughing at nothing with your hip against the counter.")),
        ], [go("Hold on to the cup.", loc="zoe_kitchen")])]})
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
    "description": "Zoe's bathroom: fix your face in her mirror, hygiene +5, once a night; on party night, the line (zoe_bathroom.md).",
    "trigger": {"location": "zoe_bathroom", "is_repeatable": True, "priority": 4, "is_active": True},
    "nodes": [node("mirror", "Her mirror", [
        P("Zoe's mirror is ringed with bulbs, and the shelf under it holds more make-up than a shop."),
        G(cond(wd(4), tod("19:00", "00:00")), P("Somebody's banging on the door before you've even shut it. \"Two minutes!\" you shout back.")),
        G(cond(wd(5), tod("00:00", "02:00")), P("Somebody's banging on the door before you've even shut it. \"Two minutes!\" you shout back.")),
    ], [
        # pass 3 D44 (the-surfaces.md R9): her face in the mirror after, not a toast
        go("Fix your face.", node="fixed", mins=10, cond_=cond(flag("zoe_face_today", False)), flags=[fset("zoe_face_today")],
           eff=[{"targetType": "player", "trait": "hygiene", "op": "add", "value": 5, "cap": 100}]),
        go("Leave it.", loc="zoe_apartment"),
    ]),
        node("fixed", "Her mirror", [
            P("Lipstick, a flick of liner, your hair shaken out over your shoulders. The girl in Zoe's mirror looks ready to be stared at, and your nipples tighten at the thought."),
        ], [go("Open the door.", loc="zoe_apartment")])]})
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
        P("Bread, milk, eggs, the wine Laura likes, the laundry detergent she always forgets. The clerk scans it all without looking up from his phone and bags it in two thin bags that will definitely split."),
    ], [go("Pay with Laura's twenty ($20).", loc="street", mins=15, costs=[{"trait": "money", "value": 20}],
           eff=[add("money", -20, clamp=False)], flags=[fset("groceries_bought")]),
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
        # reader a3 #58 (DECISIONS 131): the renders the line above is gated off (Saturday 00:00-02:00, his row, and
        # after hookup_today) get his not-yet too. "Later" names no night, so it is true after a hookup as well.
        G(cond(flag("hookup_today"), wd(5), logic="OR"), D(COCKY, "Not here. Find me later.")),
        # scene reader b02 (2026-11-03): his next step, named. party_hookup (pools.py) outranks this hub at Bold with
        # Jake out of the flat, so this hub only shows below Bold or with Jake here.
        G(cond(flag("hookup_today", False), trait("corruption", "lt", 40)),
          D(COCKY, "When you're done being a good girl, that bathroom door locks. I'm on this wall till two.")),
        G(cond(flag("hookup_today", False), trait("corruption", "gte", 40), here("npc_jake", "zoe_apartment")),
          D(COCKY, "Jake's right over there. When he goes home, that bathroom door locks.")),
    ], [
        # reader a3 #68 (DECISIONS 131): the talk is a screen with a pool he says, three lines, no counter (call B)
        go("Talk with him a while.", node="talk", mins=20),
        # reader a3 #50 (DECISIONS 131): the hub no costs him (call A): his Lust +1 and one line
        go("Walk past him.", node="past", mins=1)]),   # reader a3 #50: he has no Want to pay (validator), so the no is his line
        node("talk", "Talking", [
            P("You lean on the wall beside him. He talks about the team and about nothing, but he doesn't try to keep his eyes off your tits while he does it."),
            POOL(D(COCKY, "You're easier to talk to than you look. You look like trouble."),
                 D(COCKY, "Everybody in figure drawing draws the model. I'm drawing you. Your ass, mostly."),
                 D(COCKY, "Zoe throws the best parties going. You know why? She invites girls like you."),
                 pid="cocky_talk_lines", bag=True),
        ], [go("Back to the party.", loc="zoe_apartment", mins=2)]),
        node("past", "Past him", [D(COCKY, "Your loss."), P("He tips his beer at you and watches your ass all the way to the kitchen.")],
             [go("Let him watch you go.", loc="zoe_kitchen", mins=1)]),   # pass 3 D39 (R7)
    ]})

# heat proposal A6 (the keg guy, Zoe's kitchen) and A7 (Jake, Zoe's bathroom), DECISIONS 147 chunk 2 (heat_a.py)
import heat_a
out += heat_a.TOWN_CANVASES

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
     "The shop guy comes out from behind the counter to stack a box that doesn't need stacking, and watches your legs in that skirt all the way past. He says it to your back as you go past, and you don't turn round.",
     "A car slows beside you. The window comes down halfway, and the driver is looking at your legs, not your face. It stays with you to the end of the street, but you never look in, and it goes."),
    ("nobra", [BRA_OFF, SKIRT_OFF, PANTIES_ON], 1,
     [P("Mr. Vance sets the paper down. He looks at your tits, at your nipples pushing at the cloth, and doesn't look away. He nods at the step beside him. Not tonight. You keep walking.")],
     "The shop guy comes out from behind the counter to stack a box that doesn't need stacking. His eyes are on your tits, loose under your clothes, all the way past. He says it to your back as you go past, and you don't turn round.",
     "A car slows beside you. The window comes down halfway, and the driver is staring at your tits. It stays with you to the end of the street, but you never look in, and it goes."),
    # false lines a3 #14 (DECISIONS 129): the breeze needs a skirt or a dress, so no jeans, leggings or shorts
    ("nopanties", [PANTIES_OFF] + [{"type": "worn_type", "operator": "neq", "value": t} for t in ("jeans", "leggings", "shorts")], 2,
     [P("A breeze comes down the street as you pass the landlord's gate, and there's nothing under your clothes to stop it. Your pussy is bare under there. Mr. Vance stands up off his chair with his eyes on your hips, and takes one step toward the gate, but you don't stop. Not tonight.")],
     "The shop guy drops his change on the step and stares at your ass, like he knows there's nothing under your clothes. \"Come in a minute.\" You don't. He doesn't pick the change up until you've turned the corner.",
     "A car slows, then stops. Someone inside whistles at your ass. \"Get in.\" You don't walk faster, and you don't get in."),
]
# heat proposal A11 (DECISIONS 147): a _t4 pool on the two witness screens that show her body (media only)
STREET_POOLS = {
    "nobra": [VID("a braless girl walking down a street, her nipples showing through her top, a man staring at her tits",
                  "braless walking street nipples showing", "no bra walk in public stared at", pool_dir="sex/street_seen_nobra_t4")],
    "nopanties": [VID("a girl in a short skirt on a windy street, the breeze lifting the hem over her bare ass",
                      "no panties skirt wind street", "skirt blows up no panties walking", pool_dir="sex/street_seen_nopanties_t4")],
}
SHOP_NEXT = "He'll be out front tomorrow."
SHOP_SAID = {"skirt": "Nice day for a skirt like that.", "nobra": "Cold out today, is it? Come in and warm up.",
             "nopanties": "I mean it. Come in a minute. Just a minute."}
CAR_SAID = {"skirt": "Hey, legs! Where are you walking to? I'll drive you.", "nobra": "Jesus, look at those. Get in, I'll give you a lift.",
            "nopanties": "I said get in. I saw that breeze, legs."}
CAR_NEXT = "The same car's parked at the corner the next time you look."
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
        "id": f"street_seen_{case}", "name": {"skirt": "Walk the street in your short skirt", "nobra": "Walk the street with no bra",
                                              "nopanties": "Walk the street with no panties"}[case],   # pass 3 H33/H34 (the-voice.md R1, D11): the name says what happens if she clicks, and never hides the act
        "description": f"The street sees what she's wearing ({case}): one witness a day by the hour; the first day out in level {lv} pays both meters, after that Exhibitionism (meters.md rule 2).",
        "trigger": {"location": "street", "is_repeatable": True, "priority": 3 + lv, "is_active": True, "max_triggers_per_day": 1,
                    "conditions": cond(flag("out_shown_today", False), *worn)},
        "nodes": [node("seen", "Somebody's looking", [
            G(cond(VANCE_PORCH), *vance, P("He'll be on his porch tomorrow evening. He always is.")),
            # reader a3 #46-48 (DECISIONS 131): the shop and car renders point at what comes next. The corner shop
            # opens every day 07:00-22:00 (corner_shop.md), so its guy is out front on any daytime walk.
            # pass 3 B4: the witness says it out loud (strangers: WHO)
            G(cond(VANCE_AWAY, DAYTIME), P(shop), WHO(SHOP_SAID[case]), P(SHOP_NEXT)),
            G(cond(VANCE_AWAY, NIGHT), P(car), WHO(CAR_SAID[case]), ME("Keep driving."), P(CAR_NEXT)),
            G(cond(VANCE_AWAY, tod("18:00", "22:00")), P(car), WHO(CAR_SAID[case]), ME("Keep driving."), P(CAR_NEXT)),
            CAFE_GIRL,
            *STREET_POOLS.get(case, []),
        ], exits)]})

# heat proposal B17 (Zoe out of her bedroom), DECISIONS 147 chunk 3
import walkins_out
_done = walkins_out.attach(out)
assert _done == {"zoe_couch_alone"}, _done

text += "".join(emit(c) for c in out)
open(__import__("sys").argv[1], "w").write(text)
print("town:", len(out), "canvases")
