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
    plain_after=[P("You keep your eyes front and pretend, but your face goes hot anyway, and you can feel exactly where on your ass his eyes landed, both times. He comes down this street most mornings. He'll look again.")],
    bolder=("Look back.", [CURIOUS], [], "You look back, and catch him doing it a third time, eyes on your ass. He nearly runs into a lamp post. He slows like he might turn round. You turn the corner first. He runs this street in the mornings, and now he knows your ass by sight.")))   # reader pass 3 b01: the hook (his window is 07:00-10:00)
_PANTIES_ON = {"type": "clothing_slot", "slot": "underwear", "operator": "equipped"}
_BRA_OFF = {"type": "clothing_slot", "slot": "bra", "operator": "unequipped"}
# everyday clothes by stage (DECISIONS 205): the micro shorts on the bus-stop bench (Showing), the plunge dress
# slipping (Watched). Letting it go on pays to the top of the stage it shows.
out.append(town_event("town_event_micro_bench", "The bus-stop bench", S("07:00", "22:00"),
    [{"type": "worn_type", "operator": "eq", "value": "micro_shorts"}, _PANTIES_ON],
    [P("You sit down on the bus-stop bench to wait, and the micro shorts ride straight up. Both cheeks of your bare ass are on the cold seat, and your panties show at the leg. The guy at the other end of the bench stops scrolling his phone."),
     WHO("Bus is late. Take your time.")],
    "Stand up and wait.",
    plain_after=[P("You stand up and wait on your feet, tugging the shorts down at the back, face hot. He keeps sitting there, but he's smiling at the empty seat. He waits for this bus every day. He'll keep a seat for you.")],
    bolder=("Stay sitting.", [trait("exhibitionism", "gte", 40)], [dict(EXH1, cap=59)],
            "You stay where you are. You cross your legs the other way, slow, and the shorts ride up further, your ass bare on the bench and your panties showing at the leg, and he gives up on his phone. The bus comes. He lets it go. He waits for this bus every day. He takes this bus most days. He'll remember the shorts."))) 
out.append(town_event("town_event_plunge_slip", "The neckline slips", S("07:00", "22:00"),
    [{"type": "worn_type", "operator": "eq", "value": "plunge_dress"}, _BRA_OFF],
    [P("You step off the curb too fast and the plunge dress swings open. Your left tit comes right out of the neckline, bare, the nipple hard in the air, in front of the whole bus queue."),
     WHO("Whoa. Lady. Your, um. Your.")],
    "Tuck it back in.",
    plain_after=[P("You shove it back inside the neckline and hold the dress shut with your hand flat over it, face on fire, and walk fast. The whole bus queue watches you go. They'll be at that stop again tomorrow.")],
    bolder=("Let it be for a few steps.", [trait("exhibitionism", "gte", 60)], [dict(EXH1, cap=79)],
            "You don't grab for it. You walk on three steps, four, with your bare tit out of the plunge and bouncing in front of the queue, before you tuck it back in, slow. The whole queue has turned round. Every one of them will remember the dress.")))

# more clothes, round 2 (DECISIONS 208): the split skirt in the wind (her panties: the fix at any stage, letting it be
# at Showing, 40, to 59, DECISIONS 202-203)
out.append(town_event("town_event_split_wind", "The wind in the slit", S("07:00", "22:00"),
    [{"type": "worn_type", "operator": "eq", "value": "split_skirt"}, _PANTIES_ON],
    [P("A gust comes off the corner and catches the slit in your skirt. It throws the whole front panel open to your waist, and your panties are out to the street, the front of them, to the whole street. A man waiting to cross stares straight at them."),
     WHO("Oh. Hello there.")],
    "Grab the skirt shut.",
    plain_after=[P("You grab the panel and pin it to your thigh with your fist, face burning, and walk the rest of the way holding it shut. He's still grinning at the crossing when you look back. He crosses here every day.")],
    bolder=("Let the wind have it.", [trait("exhibitionism", "gte", 40)], [dict(EXH1, cap=59)],
            "You don't grab it. The wind holds the slit open, the front of your panties on show to the crossing, and you let it, three steps, four, before you smooth the skirt flat. The man at the crossing misses the green light. He'll be at this crossing tomorrow, and he'll know the skirt.")))

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
        G(cond(trait("drinks_tonight", "eq", 2)), T("Number three, from a mixing bowl. Breakfast is going to hurt.")),
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
        # scene reader 2026-11-04: Saturday 00:00-02:00 is the end of his row, so "later" there is next Friday's party
        G(cond(flag("hookup_today"), wd(4)), D(COCKY, "Not here. Find me later.")),
        # scene reader 2026-11-04: only where neither "that bathroom door locks" line below shows
        G(cond(wd(5), flag("hookup_today")), D(COCKY, "Not here. Find me next Friday.")),
        G(cond(wd(5), flag("hookup_today", False), trait("corruption", "gte", 40), {"type": "npc_at_location", "location_id": "zoe_apartment", "npc_id": "npc_jake", "operator": "is_absent"}),
          D(COCKY, "Not here. Find me next Friday.")),
        # scene reader b02 (2026-11-03): his next step, named. party_hookup (pools.py) outranks this hub at Bold with
        # Jake out of the flat, so this hub only shows below Bold or with Jake here.
        G(cond(flag("hookup_today", False), trait("corruption", "lt", 40)),
          D(COCKY, "When you're done being a good girl, that bathroom door locks. I'm on this wall till two.")),
        G(cond(flag("hookup_today", False), trait("corruption", "gte", 40), here("npc_jake", "zoe_apartment")),
          D(COCKY, "Jake's right over there. When he goes home, that bathroom door locks.")),
    ], [
        # reader a3 #68 (DECISIONS 131): the talk is a screen with a pool he says, three lines, no counter (call B)
        go("Talk with him a while.", node="talk", mins=20, cond_=cond(tod("23:00", "01:40"))),   # his row and the party end at 02:00: the talk ends before them
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
# Once a day (out_shown_today, cleared in the daily tick). It pays Exhibitionism only (exhibition phase 1, LO
# 2026-11-08; it paid Corruption too on a level's first day while Corruption could open the leave rules). One witness by the hour: Mr. Vance on his porch (his 18:00-22:00 row),
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
CAFE_GIRL = {case: G(cond(trait("cafe_footfall", "gte", 10)), WHO(line)) for case, line in (
    ("crop", "Hey, café girl. Didn't know you had abs under that apron."),
    ("bodycon", "That's the waitress from the café. Wow. Okay."),
    ("micro", "Café girl! I'm coming in for a coffee this week, swear to God."),
    ("plunge", "Is that the café girl? Holy shit, it is."),
    ("split", "Café girl! Look at those legs."),
    ("sequin", "Café girl, all sparkly. Where are you off to?"),
    ("backless", "Café girl! Where's the rest of your dress?"),
    ("skirt", "You're the girl from the café."),
    ("nobra", "Aren't you from the café? You look different out here."),
    ("nopanties", "Café girl, right? I'd come in more often for this."))}
# (case, its worn items, level, Vance's line, the shop guy's line, the car's line)
STREET_CASES = [
    ("skirt", [SKIRT_ON, PANTIES_ON], 1,
     [D("npc_vance", "Mark's girl has good legs."), P("He doesn't pretend to read his paper. His eyes go up your legs to the hem of your skirt and stay there. He pats the step beside him. You keep walking.")],
     "The shop guy comes out from behind the counter to stack a box that doesn't need stacking, and watches your legs in that skirt all the way past. He says it to your back as you go past, and you don't turn round.",
     "A car slows beside you. The window comes down halfway, and the driver is looking at your legs, not your face. It stays with you to the end of the street, but you never look in, and it goes."),
    ("nobra", [BRA_OFF, SKIRT_OFF, PANTIES_ON], 1,
     [P("Mr. Vance sets the paper down. He looks at your tits, at your nipples pushing at the cloth, and doesn't look away. He nods at the step beside him. Not tonight. You keep walking.")],
     "The shop guy comes out from behind the counter to stack a box that doesn't need stacking. His eyes are on your tits, loose under your clothes, all the way past. He says it to your back as you go past, and you don't turn round.",
     "A car slows beside you. The window comes down halfway, and the driver is staring at your tits. It stays with you to the end of the street, but you never look in, and it goes."),
    # false lines a3 #14 (DECISIONS 129): the breeze needs a skirt or a dress, so no jeans, leggings or shorts.
    # pass 4 (LO, 2026-11-04): "pussy" was past the strangers' ceiling (DECISIONS 41); the breeze is on her ass now.
    ("nopanties", [PANTIES_OFF] + [{"type": "worn_type", "operator": "neq", "value": t} for t in ("jeans", "leggings", "shorts", "micro_shorts", "track_pants", "gym_shorts", "sheer_leggings")], 2,   # DECISIONS 233: no hem in any trousers
     [P("A breeze comes down the street as you pass the landlord's gate, and there's nothing under your clothes to stop it. It lifts your hem and runs cool over your bare ass. Mr. Vance stands up off his chair with his eyes on your hips, and takes one step toward the gate, but you don't stop. Not tonight.")],
     "The shop guy drops his change on the step and stares at your ass, like he knows there's nothing under your clothes. \"Come in a minute.\" You don't. He doesn't pick the change up until you've turned the corner.",
     "A car slows, then stops. Someone inside whistles at your ass. \"Get in.\" You don't walk faster, and you don't get in."),
    # everyday clothes by stage (DECISIONS 205): the crop top and the bodycon at Daring (20), the micro shorts at
    # Showing (40), the plunge dress at Watched (60). Each piece's own row outranks the bra and panties rows.
    ("crop", [trait("exhibitionism", "gte", 20), {"type": "worn_type", "operator": "eq", "value": "crop_top"}, BRA_ON], 1.5,
     [P("Mr. Vance lowers his paper. His eyes go to the bare strip of your belly under the crop top, then up to where it stops, under your tits. He doesn't go back to the paper, but he takes his time saying anything."), D("npc_vance", "Bit chilly for that, Miss."), P("He pats the step beside him. Not tonight. You keep walking.")],
     "The shop guy is out front with a broom, and he stops sweeping. His eyes are on your bare belly and the bottom edge of your crop top all the way past, waiting for it to ride up.",
     "A car slows beside you. The driver leans over to look at your bare belly and the crop top stretched over your tits. It stays with you to the end of the street, and then it goes."),
    ("bodycon", [trait("exhibitionism", "gte", 20), {"type": "worn_type", "operator": "eq", "value": "bodycon_dress"}, PANTIES_ON], 1.5,
     [P("Mr. Vance puts the paper down altogether. The bodycon dress shows him every curve you've got, the shape of your tits and the round of your ass, and it stops an inch under it. He watches the hem climb with every step.")],
     "The shop guy comes out of the door and just stands there. The tight dress hugs your ass so close he can see the line of your panties, and he watches it all the way past, but he doesn't come closer.",
     "A car slows beside you. The driver is staring at your ass in the skin-tight dress, the hem riding up your thighs as you walk. It stays with you to the corner, then it goes."),
    ("micro", [trait("exhibitionism", "gte", 40), {"type": "worn_type", "operator": "eq", "value": "micro_shorts"}, PANTIES_ON], 2.5,
     [P("Mr. Vance stands up off his chair. The micro shorts leave the bottom half of your ass bare, both cheeks, and he watches them bounce out of the shorts all the way past his gate."), D("npc_vance", "Mark lets you out in those?")],
     "The shop guy drops the box he's carrying. Your ass is hanging out of the bottom of your shorts, both cheeks, and he stares at it until you're past the corner.",
     "A car slows, then crawls behind you, not beside you. The driver wants the view from the back: your bare cheeks under the micro shorts, every step. He honks twice before he goes."),
    ("plunge", [trait("exhibitionism", "gte", 60), {"type": "worn_type", "operator": "eq", "value": "plunge_dress"}, BRA_OFF], 3,
     [P("Mr. Vance gets up and comes down to his gate. The plunge dress is cut open to your navel, and with no bra under it your tits sit bare inside the neckline, the inside curve of each one on show, moving loose with every step. He grips the gate, but he doesn't open it. He watches them go by.")],
     "The shop guy stops dead in his door. The neckline of your dress is open to your belly button, your bare tits loose inside it, and every step shows him more of the sides of them. He doesn't even pretend to sweep.",
     "A car slows beside you and stays there. The driver is staring down the open front of your dress at your bare tits, loose in the plunge, nearly out of it with every step. He follows you to the end of the street."),
    # more clothes, round 2 (DECISIONS 208): the split skirt and the sequin dress at Daring (20), the backless dress at
    # Watched (60): CoT's side-split and minidress at its 2, its backless minidress at its 4
    ("split", [trait("exhibitionism", "gte", 20), {"type": "worn_type", "operator": "eq", "value": "split_skirt"}], 1.5,
     [P("Mr. Vance looks up from his paper. The slit in your skirt falls open to your hip with every step, your whole bare leg out to the top of your thigh, and he watches it open and close all the way past his gate."), D("npc_vance", "That's some skirt, Miss.")],
     "The shop guy leans in his doorway and watches the slit in your skirt. Every step it falls open to your hip, your bare leg all the way up, and every step he waits for the next one.",
     "A car slows beside you on the side with the slit. The driver watches your bare leg come out of the skirt to the hip, step after step, all the way to the corner."),
    ("sequin", [trait("exhibitionism", "gte", 20), {"type": "worn_type", "operator": "eq", "value": "sequin_dress"}, PANTIES_ON], 1.5,
     [P("Mr. Vance takes his glasses off. The sequin dress throws the porch light back at him off every curve, your tits, your hips, the hem high on your thighs, and he watches you all the way past like you're on a stage."), D("npc_vance", "Going somewhere special, Miss?")],
     "The shop guy comes out to watch. The sequin dress flashes with every step, tight over your tits and your ass, the hem barely past the top of your thighs, and he doesn't go back in until you're round the corner.",
     "A car slows beside you. The sequins catch its lights, and the driver is looking at your ass, the hem riding up as you walk. It follows you to the corner."),
    ("backless", [trait("exhibitionism", "gte", 60), {"type": "worn_type", "operator": "eq", "value": "backless_dress"}, BRA_OFF], 3,
     [P("Mr. Vance stands up as you pass. The backless dress leaves you bare from your neck to the base of your spine, and with nothing under it the open side shows him the curve of your bare tit, moving with every step."), D("npc_vance", "Turn round for me, Miss. Just once.")],
     "The shop guy watches you go past from his doorway. Your back is bare to the base of your spine, no strap anywhere, and as you turn the corner the open side shows him the curve of your bare tit.",
     "A car slows behind you. The dress is open all the way down your back, bare to the top of your ass, and the driver follows close enough to see there's nothing under it."),
]
# heat proposal A11 (DECISIONS 147): a _t4 pool on the two witness screens that show her body (media only)
STREET_POOLS = {
    "nobra": [VID("a braless girl walking down a street, her nipples showing through her top, a man staring at her tits",
                  "braless walking street nipples showing", "no bra walk in public stared at", pool_dir="sex/street_seen_nobra_t4")],
    "nopanties": [VID("a girl in a short skirt on a windy street, the breeze lifting the hem over her bare ass",
                      "no panties skirt wind street", "skirt blows up no panties walking", pool_dir="sex/street_seen_nopanties_t4")],
}
SHOP_NEXT = "He'll be out front tomorrow."
SHOP_SAID = {"crop": "Lift your arms for me, sweetheart. Just once.", "bodycon": "Painted on, that dress. Turn round.",
             "micro": "You forgot the rest of your shorts.", "plunge": "Jesus. Does your mother know you're out in that?",
             "split": "That slit goes all the way up, doesn't it?", "sequin": "Where's the party, sweetheart? Can I come?",
             "backless": "Nothing under that, is there? Not a thing.",
             "skirt": "Nice day for a skirt like that.", "nobra": "Cold out today, is it? Come in and warm up.",
             "nopanties": "I mean it. Come in a minute. Just a minute."}
CAR_SAID = {"crop": "Nice stomach, baby. Show me the rest.", "bodycon": "Damn, that dress. Get in, I'll take you somewhere you can wear it.",
            "micro": "Those cheeks! Get in, I'll give you a ride.", "plunge": "Lean in the window, baby. Just lean.",
            "split": "Show me the other leg, baby.", "sequin": "Nice dress. Get in, I'll take you to the party.",
            "backless": "Turn round, baby. Show me the front.",
            "skirt": "Hey, legs! Where are you walking to? I'll drive you.", "nobra": "Jesus, look at those. Get in, I'll give you a lift.",
            "nopanties": "I said get in. I saw that breeze, legs."}
CAR_NEXT = "The same car's parked at the corner the next time you look."
for case, worn, lv, vance, shop, car in STREET_CASES:
    first = f"street_first_l{int(lv)}"
    # LO, 2026-11-04: a dress-code act pays to the top of the stage its dress code needs (world_data clothing rules: no bra
    # or a short skirt out needs a meter at 20, no panties out a meter at 40), on both meters.
    cap = {1: 39, 1.5: 39, 2: 59, 2.5: 59, 3: 79}[lv]   # crop and bodycon Daring, micro shorts Showing, plunge Watched (DECISIONS 205)
    # exhibition phase 1 (LO, 2026-11-08): going out is Exhibitionism's alone now, so the street pays it alone
    pay_first = [{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": cap}]
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
                                              "nopanties": "Walk the street with no panties", "crop": "Walk the street in your crop top",
                                              "bodycon": "Walk the street in your bodycon dress", "micro": "Walk the street in your micro shorts",
                                              "plunge": "Walk the street in your plunge dress", "split": "Walk the street in your split skirt",
                                              "sequin": "Walk the street in your sequin dress", "backless": "Walk the street in your backless dress"}[case],   # pass 3 H33/H34 (the-voice.md R1, D11): the name says what happens if she clicks, and never hides the act
        "description": f"The street sees what she's wearing ({case}): one witness a day by the hour; Exhibitionism +1 (exhibition phase 1, 2026-11-08).",
        "trigger": {"location": "street", "is_repeatable": True, "priority": int(3 + 2 * lv), "is_active": True, "max_triggers_per_day": 1,
                    "conditions": cond(flag("out_shown_today", False), *worn)},
        "nodes": [node("seen", "Somebody's looking", [
            G(cond(VANCE_PORCH), *vance, P("He'll be on his porch tomorrow evening. He always is.")),
            # reader a3 #46-48 (DECISIONS 131): the shop and car renders point at what comes next. The corner shop
            # opens every day 07:00-22:00 (corner_shop.md), so its guy is out front on any daytime walk.
            # pass 3 B4: the witness says it out loud (strangers: WHO)
            G(cond(VANCE_AWAY, DAYTIME), P(shop), WHO(SHOP_SAID[case]), P(SHOP_NEXT)),
            G(cond(VANCE_AWAY, NIGHT), P(car), WHO(CAR_SAID[case]), ME("Keep driving."), P(CAR_NEXT)),
            G(cond(VANCE_AWAY, tod("18:00", "22:00")), P(car), WHO(CAR_SAID[case]), ME("Keep driving."), P(CAR_NEXT)),
            CAFE_GIRL[case],
            *STREET_POOLS.get(case, []),
        ], exits)]})

# heat proposal B17 (Zoe out of her bedroom), DECISIONS 147 chunk 3; B24 (Q4, LO 2026-11-04) on Zoe's bathroom
import walkins_out
_done = walkins_out.attach(out)
assert _done == {"zoe_couch_alone", "zoe_bathroom_face"}, _done   # B24 (Q4): the loose bolt

# ── exhibition phase 1 (LO, 2026-11-08): the low-cut top on the street, under Daring. A look happens to her (stage
# 1); her choice is not to cover up. Shares out_shown_today with the other street rows, so one street look a day.
out.append({
    "id": "street_seen_lowtop", "name": "Walk the street in your low-cut top",
    "description": "The street sees the low-cut top: a man at the bus stop looks; not covering up pays Exhibitionism +1 (cap 19). Once a day, shared with the other street looks.",
    "trigger": {"location": "street", "is_repeatable": True, "priority": 3, "is_active": True, "max_triggers_per_day": 1,
                "conditions": cond(flag("out_shown_today", False), {"type": "clothing_item", "item_id": "low_top", "operator": "equipped"},
                                   BRA_ON, PANTIES_ON, SKIRT_OFF, trait("exhibitionism", "lt", 20))},
    "nodes": [node("seen", "The bus stop", [
        P("A man at the bus stop looks once, then again, longer, straight at your tits in the low-cut top. He doesn't pretend to read the timetable."),
    ], [
        go("Keep walking, and don't cover up.", node="walked", mins=2, flags=[fset("out_shown_today")],
           eff=[{"targetType": "player", "trait": "exhibitionism", "op": "add", "value": 1, "cap": 19}]),
        go("Cross your arms and walk on.", node="covered", mins=2, flags=[fset("out_shown_today")]),
    ]), node("covered", "Arms crossed", [
        P("You fold your arms over your chest and walk faster. He laughs, low, and goes back to the timetable. The bus stop's on your way most days."),
    ], [go("Walk on.", loc="street", mins=1)]), node("walked", "The corner", [
        P("You don't fold your arms. You can feel his eyes on your tits all the way to the corner, and you don't walk any faster. He doesn't follow. Not today."),
        GC(cond(trait("exhibitionism", "lt", 5)), T("People look. That's all it was.")),
        GC(cond(trait("exhibitionism", "lt", 10)), T("He looked, and you let him.")),
        GC(cond(trait("exhibitionism", "lt", 15)), T("You liked knowing he was still watching.")),
        GC(cond(trait("exhibitionism", "lt", 20)), T("The top isn't enough any more. Something shorter, next time.")),
        P("The bus stop's on your way most days."),
    ], [go("Walk on.", loc="street", mins=2)])]})

text += "".join(emit(c) for c in out)
open(__import__("sys").argv[1], "w").write(text)
print("town:", len(out), "canvases")
