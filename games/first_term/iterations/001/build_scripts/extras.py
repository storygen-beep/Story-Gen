"""Rows so no place is open and empty, the uniform's readers, and the guidance cards for the light
cast and her two stages."""
from canv import *
from tomlw import tod, wd

out = []
UNIFORM = {"type": "worn_type", "operator": "eq", "value": "cafe_uniform"}
NORMAL_ON = {"type": "clothing_item", "item_id": "cafe_uniform_normal", "operator": "equipped"}
SEXY_ON = {"type": "clothing_item", "item_id": "cafe_uniform_sexy", "operator": "equipped"}

out.append({
    "id": "cafe_coffee", "name": "Order a coffee ($3)",
    "description": "A coffee at the counter: energy +5 for $3, once a day. The uniform's readers: the regulars look.",
    "trigger": {"location": "cafe", "is_repeatable": True, "priority": 2, "is_active": True, "max_triggers_per_day": 1},
    "nodes": [node("coffee", "A coffee", [
        P("You sit at the end of the counter with a coffee you paid for, watching the room, the regulars, the door."),
        G(cond(NORMAL_ON), P("In the uniform, off shift, the regulars still wave you over for refills. You ignore them, but it's nice to be asked.")),
        G(cond(SEXY_ON), P("In the tight uniform the man at the counter can't decide where to look, so he looks everywhere but his newspaper.")),
        G(cond({"type": "worn_type", "operator": "neq", "value": "cafe_uniform"}), P("Nobody here knows you when you're not in the apron. It's strange how much that changes.")),
    ], [go("Drink it. ($3)", loc="cafe", mins=20, costs=[{"trait": "money", "value": 3}],
           eff=[{"targetType": "player", "trait": "energy", "op": "add", "value": 5, "cap": 100}]),
        go("Leave it.", loc="cafe")])]})

out.append({
    "id": "vance_house_look", "name": "Look at the house next door",
    "description": "Vance's house from the pavement: who owns the street. Writes nothing.",
    "trigger": {"location": "vance_house", "is_repeatable": True, "priority": 1, "is_active": True},
    "nodes": [node("house", "Next door", [
        P("Vance's house is bigger than yours and better kept: the hedge cut square, the brass knocker polished, a rocking chair on the porch with a cushion that's moulded to one man. Through the front window you can see a wall of filing cabinets."),
        G(cond(flag("knows_mark_debt")), T("Somewhere in those cabinets is a folder with Mark's name on it. And your house.")),
    ], [go("Go.", loc="vance_house")])]})

out.append({
    "id": "zoe_bedroom_look", "name": "Look round her room",
    "description": "Zoe's bedroom: her things. After her dare on the balcony, the bra on the bedpost. Writes nothing.",
    "trigger": {"location": "zoe_bedroom", "is_repeatable": True, "priority": 1, "is_active": True},
    "nodes": [node("room", "Her room", [
        P("Zoe's room is a bed you can't see for clothes, fairy lights round the mirror, polaroids of parties stuck in the frame. In half of them she's kissing somebody. In two of the new ones she's looking at you."),
        G(cond(flag("zoe_02_done")), P("The bra she dared off you on the balcony hangs off her bedpost like a trophy. She hasn't given it back, but you haven't asked.")),
    ], [go("Go.", loc="zoe_bedroom")])]})

# the uniform's readers at home: Mark and Ryan see it
out.append({
    "id": "kitchen_uniform_home", "name": "Come home in the uniform",
    "description": "The café uniform read at home (the wardrobe sheet: Mark's \"where's a waitress get twenties?\").",
    "trigger": {"location": "home_kitchen", "is_repeatable": True, "priority": 2, "is_active": True, "conditions": cond(UNIFORM)},
    "nodes": [node("uniform", "Still in the uniform", [
        P("You come in through the kitchen still in your café uniform, apron stuffed in your bag, smelling of coffee."),
        G(cond({"type": "npc_at_location", "location_id": "home_kitchen", "npc_id": "npc_mark", "operator": "is_present"}, SEXY_ON),
          D("npc_mark", "Where's a waitress get twenties, wearing that?")),
        G(cond({"type": "npc_at_location", "location_id": "home_kitchen", "npc_id": "npc_laura", "operator": "is_present"}, NORMAL_ON),
          D("npc_laura", "Look at you. My working girl. Sit, I'll make you something.")),
        G(cond({"type": "npc_at_location", "location_id": "home_kitchen", "npc_id": "npc_mark", "operator": "is_present"}, NORMAL_ON),
          D("npc_mark", "Tips any good? Sunday's coming.")),
        G(cond({"type": "npc_at_location", "location_id": "home_kitchen", "npc_id": "npc_laura", "operator": "is_present"}, SEXY_ON),
          P("Laura looks at the open top button for a long second."), D("npc_laura", "Is that the uniform, or Tom's idea?")),
        G(cond({"type": "npc_at_location", "location_id": "home_ryan_room", "npc_id": "npc_ryan", "operator": "is_present"}),
          P("Ryan comes down for a drink, sees the uniform, and stops on the bottom stair. \"Huh,\" he says, and takes his time with the fridge.")),
        G(cond({"type": "npc_at_location", "location_id": "home_kitchen", "operator": "is_absent"}),
          P("Nobody's in. You eat cereal standing up at the counter in the uniform, too tired to change.")),
    ], [go("Go and change.", loc="home_kitchen")])]})

# ── guidance: one card per light person (the cast page lists people by their cards) ──
light = [
    ("npc_nadia", "nadia_met", "Saves you a seat in Psychology. Knows Dr. Hale's history.", "Psychology, Monday, Wednesday and Friday mornings; the library most afternoons.", "hub_nadia_library"),
    ("npc_vance", "vance_met", "Owns your house. Mark owes him. He watches from his porch.", "His porch, every evening.", "hub_vance_porch"),
    ("npc_gary", "gary_met", "Booth four, his tea, his paper, his wallet.", "The café, weekday afternoons and Friday evenings.", "hub_gary_booth"),
    ("npc_art_lecturer", "art_lecturer_met", "Figure drawing. She wants to draw you.", "Figure drawing, Tuesday and Thursday mornings and Wednesday afternoon; her office in the afternoons.", "hub_art_office"),
    ("npc_business_lecturer", "business_lecturer_met", "Business. Strict. Can't be bought. An honest retake if you're failing.", "His office on the faculty floor, afternoons.", "hub_business_office"),
    ("npc_bio_ta", "bio_ta_met", "Biology. Shy. Looks, and hopes you won't notice.", "Her office on the faculty floor, afternoons.", "hub_ta_office"),
    ("npc_dean", "dean_met", "Grades, complaints, probation.", "The dean's office, weekdays.", "hub_dean_office"),
]
cards = []
for npc, met, text, tip, hub in light:
    cards.append({"npc_id": npc, "priority": 5, "text": text, "tip": tip,
                  "when": [{"flag": met, "op": "is_true"}], "ready_canvas": hub})
mute = [
    ("npc_kayla", "kayla_met", "Ryan's girlfriend. Fridays, and Saturday mornings in his shirt."),
    ("npc_claire", "claire_met", "Dr. Hale's wife. She picks him up on Thursdays at half past seven."),
    ("npc_desk_guy", "desk_guy_met", "Sits beside you in Psychology and Business. Always needs help with something."),
    ("npc_rival", "rival_met", "Would love to see you in trouble with the dean."),
    ("npc_study_guy", "study_guy_met", "Has the answers. Wants your attention."),
    ("npc_cocky_guy", "cocky_guy_met", "Jake's teammate. Figure drawing; Zoe's parties, late."),
    ("npc_figure_model", "figure_model_met", "The model in Figure drawing. Paid to be drawn."),
]
for npc, met, text in mute:
    cards.append({"npc_id": npc, "priority": 5, "text": text, "when": [{"flag": met, "op": "is_true"}]})

# ── her two stages: what the next rung opens (the-voice.md R2; DECISIONS: stages at 20/40/60) ──
for trait_k, bands in [
    ("corruption", [(0, 20, "Good Girl. Curious opens at 20: watching, touching yourself, a kiss, a dare.",
                     "Reach Curious (Corruption 20): parties, the café, the park, touching yourself"),
                    (20, 40, "Curious. Bold opens at 40: hands, mouths, a price for a look.",
                     "Reach Bold (Corruption 40): the guy beside you, Gary's booth, Zoe's hot tub"),
                    (40, 60, "Bold. Hungry is the next release: strangers, a crowd, the taboo at home.",
                     "Hungry (Corruption 60) opens in the next release")]),
    ("exhibitionism", [(0, 20, "Covered. Daring opens at 20: no bra, a short skirt out of the house.",
                        "Reach Daring (Exhibitionism 20): selfies, the couch, the café uniform"),
                       (20, 40, "Daring. Showing opens at 40: no panties out, naked for someone you know.",
                        "Reach Showing (Exhibitionism 40): dares, the park run, the tables at home"),
                       (40, 60, "Showing. Watched is the next release: posing for the class, a crowd.",
                        "Watched (Exhibitionism 60) opens in the next release")])]:
    for lo, hi, text, label in bands:
        cards.append({"group": f"tier_{trait_k}", "priority": 5, "text": text,
                      "when": [{"flag": "opening_done", "op": "is_true"},
                               {"type": "trait", "subject": "player", "trait": trait_k, "op": "gte", "value": lo},
                               {"type": "trait", "subject": "player", "trait": trait_k, "op": "lt", "value": hi}],
                      "goals": [{"type": "trait", "subject": "player", "trait": trait_k, "op": "gte", "value": hi, "label": label}]})

text = "# ── rows so no place stands empty, the uniform's readers, cards for the light cast and her stages ──\n"
text += "".join(emit(c) for c in out) + "".join(emit_card(c) for c in cards)
open(__import__("sys").argv[1], "w").write(text)
print("extras:", len(out), "canvases,", len(cards), "cards")
