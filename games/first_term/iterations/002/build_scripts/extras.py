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
    "trigger": {"location": "cafe", "is_repeatable": True, "priority": 2, "is_active": True, "max_triggers_per_day": 1,
                "substitutions": []},   # the walk-in rules follow; the job ask has its own row (tom.py, LO 2026-11-05)
    "nodes": [node("coffee", "A coffee", [
        P("You take the stool at the end of the counter, watching the room, the regulars, the door."),
        G(cond(NORMAL_ON), P("In the uniform, off shift, the regulars still wave you over for refills. You ignore them, but it's nice to be asked."),
          WHO("Refill over here, when you get a minute!")),
        G(cond(SEXY_ON), P("In the tight uniform the man at the counter can't decide between your tits and your ass, so he looks at both, and his newspaper ends up in his lap. He asks you for a refill. You're off shift, so no."),
          WHO("Go on. One refill. I'll make it worth your while.")),   # LO 2026-11-03: the regular pushes
        # reader a3 #43 (DECISIONS 131): the pre-Tom render points at the job. The card is in the window until
        # cafe_job_ask's "Take the uniform." sets tom_met (tom.py; "Sign stays up till somebody takes it.").
        G(cond({"type": "worn_type", "operator": "neq", "value": "cafe_uniform"}, flag("tom_met", False)),
          P("Nobody here knows you. Taped inside the window, the STAFF WANTED card has a coffee ring on it."),
          WHO("What can I get you?")),   # LO 2026-11-03: the man at the till, not yet a name (tom_met unset)
        G(cond({"type": "worn_type", "operator": "neq", "value": "cafe_uniform"}, flag("tom_met")), P("Out of the apron you're just a customer here, and Tom still clocks you from the till.")),
        # LO 2026-11-03: Tom's line only while his row has him in (Mon-Sat 08:00-23:00), strict, @player on shift
        G(cond(flag("tom_met"), here_at("npc_tom", "cafe")), D("npc_tom", "Off the clock, @player? Then you pay like everyone else.")),
    ], [go("Drink it. ($3)", node="drunk", mins=20, costs=[{"trait": "money", "value": 3}],   # pass 3 D44 (R9): a screen, not a toast
           eff=[{"targetType": "player", "trait": "energy", "op": "add", "value": 5, "cap": 100}]),
        go("Leave it.", loc="cafe")]),
        node("drunk", "The bottom of the cup", [
            P("You drink it hot at the end of the counter with your legs crossed on the stool. It's strong and bitter, and by the bottom of the cup your heart's going quick and your skin feels too warm for your clothes."),
        ], [go("Leave the cup on the counter.", loc="cafe")])]})

out.append({
    "id": "vance_house_look", "name": "Look at the house next door",
    "description": "Vance's house from the sidewalk: who owns the street. Writes nothing.",
    "trigger": {"location": "vance_house", "is_repeatable": True, "priority": 1, "is_active": True},
    "nodes": [node("house", "Next door", [
        P("Vance's house is bigger than yours and better kept: the hedge cut square, the brass knocker polished, a rocking chair on the porch with a cushion that's moulded to one man. Through the front window you can see a wall of filing cabinets."),
        G(cond(flag("knows_mark_debt")), T("Somewhere in those cabinets is a folder with Mark's name on it. And your house.")),
    ], [go("Walk on.", loc="street", mins=2)])]})

out.append({
    "id": "zoe_bedroom_look", "name": "Look round her room",
    "description": "Zoe's bedroom: her things. After her dare on the balcony, the bra on the bedpost. Writes nothing.",
    "trigger": {"location": "zoe_bedroom", "is_repeatable": True, "priority": 1, "is_active": True},
    "nodes": [node("room", "Her room", [
        P("Zoe's room is a bed you can't see for clothes, fairy lights round the mirror, polaroids of parties stuck in the frame. In half of them she's kissing somebody."),
        G(cond(flag("party_went")), P("In two of the new ones she's looking at you.")),
        G(cond(flag("zoe_has_bra")), P("The bra she dared off you on the balcony hangs off her bedpost like a trophy. She hasn't given it back, but you haven't asked.")),
    ], [go("Leave her things where they are.", loc="zoe_apartment", mins=2)])]})   # pass 3 D39 (R7)

# The uniform's readers at home are lines in Laura's and Mark's kitchen hubs now (iteration 002,
# part 2: a garment reaction is a line in a hub, wardrobe.md:116-121; no "come home in the uniform"
# button).

# ── guidance: one card per light person (the cast page lists people by their cards) ──
light = [
    ("npc_nadia", "nadia_met", "Saves you a seat in Psychology. Knows Dr. Hale's history.", "Psychology, Monday, Wednesday and Friday mornings and Thursday after lunch; the library most afternoons.", "hub_nadia_library"),
    ("npc_vance", "vance_met", "Owns your house. He watches the street from his porch.", "His porch, every evening.", "hub_vance_porch"),
    ("npc_gary", "gary_met", "Booth four, his tea, his paper, his wallet.", "The café, weekday afternoons and Friday evenings.", "hub_gary_booth"),
    ("npc_art_lecturer", "art_lecturer_met", "Figure drawing. She wants to draw you.", "Figure drawing, Tuesday and Thursday mornings and Wednesday afternoon; her office in the afternoons.", "hub_art_office"),
    ("npc_business_lecturer", "business_lecturer_met", "Business. Strict. Can't be bought. An honest retake if you're failing.", "His office on the faculty floor, afternoons.", "hub_business_office"),
    ("npc_bio_ta", "bio_ta_met", "Biology. Shy. Looks, and hopes you won't notice.", "Her office on the faculty floor, afternoons.", "hub_ta_office"),
    ("npc_dean", "dean_met", "Grades, complaints, probation.", "The dean's office, weekdays.", "hub_dean_office"),
]
cards = []
# DECISIONS 231 (reader): release 1 cuts the three offices, so release 1's cards say where they teach instead
R1_TIPS = {"npc_art_lecturer": "Figure drawing, Tuesday and Thursday mornings and Wednesday afternoon.",
           "npc_business_lecturer": "Business, in the lecture hall.",
           "npc_bio_ta": "Biology, in the lecture hall."}
for npc, met, text, tip, hub in light:
    card = {"npc_id": npc, "priority": 5, "text": text, "tip": tip,
            "when": [{"flag": met, "op": "is_true"}], "ready_canvas": hub}
    if npc in R1_TIPS:
        r1 = dict(card, tip=R1_TIPS[npc], ready_canvas=hub.replace("_office", "_class"), release_until=1)
        if npc == "npc_business_lecturer":
            r1["text"] = "Business. Strict. Can't be bought."
        cards += [dict(card, release=2), r1]
    else:
        cards.append(card)
# pass 3 H43/J34 (the-voice.md R3; engine.md 47.3): each of these had one card with flavour and nothing else, so
# their section of the guidance page never said what to do. Each gets one guiding line (a place, the person, a verb)
# and the existing canvas with a location where she finds them, so the card draws its frame (engine.md 47).
mute = [
    ("npc_kayla", "kayla_met", "Ryan's girlfriend. Fridays, and Saturday mornings in his shirt.",
     "Take a shower on a Friday evening while Ryan has her over, and Kayla may walk in on you.", "bathroom_shower"),
    ("npc_claire", "claire_met", "Dr. Hale's wife. She picks him up from his office on Thursday evenings.",
     "Go to Dr. Hale's office on a Thursday evening: Claire comes to pick him up.", "hub_hale_office"),
    ("npc_desk_guy", "desk_guy_met", "Sits beside you in Psychology and Business. Always needs help with something.",
     "Sit through Psychology or Business in the lecture hall: he takes the seat beside you.", "college_class_psych"),
    ("npc_rival", "rival_met", "Would love to see you in trouble with the dean.",
     "Wear a short skirt or no bra to Business in the lecture hall, and she tells the dean's office.", "college_class_business"),
    ("npc_study_guy", "study_guy_met", "Has the answers. Wants your attention.",
     "Go to Business in the lecture hall: he sits behind you and watches the back of your neck.", "college_class_business"),
    ("npc_cocky_guy", "cocky_guy_met", "Jake's teammate. Figure drawing; Zoe's parties, late.",
     "Talk to him at the next easel in Figure drawing, or find him by the bathroom door at Zoe's Friday party, late.", "hub_cocky_class"),
    ("npc_figure_model", "figure_model_met", "The model in Figure drawing. Paid to be drawn.",
     "Go to Figure drawing in the lecture hall: she poses naked at the front, and you draw her.", "college_class_figure"),
]
# Vance's meeting card under People until she has met him (LO 2026-11-02, "Yes all three"): the meeting fired
# only if she happened to cross the street of an evening, and his porch and his knock wait for vance_met.
cards.append({"npc_id": "npc_vance", "priority": 5, "heading": "Next door",   # C3 (LO 2026-11-03)
              "text": "Next door: the man who owns your house watches the street.",
              "tip": "The street, an evening, 6 to 10 PM",
              "when": [{"flag": "opening_done", "op": "is_true"}, {"flag": "vance_met", "op": "is_false"}],
              "ready_canvas": "vance_meeting"})
for npc, met, text, tip, where in mute:
    cards.append({"npc_id": npc, "priority": 5, "text": text, "tip": tip, "when": [{"flag": met, "op": "is_true"}],
                  "ready_canvas": where})

# The small rungs inside the first stage (heat proposal C1-C6, DECISIONS 147): one goal line per rung on its card.
# DECISIONS 228 (the-voice.md R3b): a line is the act at a place with no number; the engine prints "— 3 / 5" after it.
# Each line names the act ONE RUNG BELOW the value it climbs to, the one that pays her there, never the button the
# value itself opens (engine.md §23 "Check the label is not circular"; pass 3 J37): the stacks' shelf (Corruption 0)
# to 5, one aisle closer (5) to 10, channel 5's sound (10) to 15; the shower walk-in's towel (Exhibitionism 0) to 5,
# the unlocked shower door (5) to 15. Each of these pays +1 there, cap 19. The curtain opens at 20 now (LO, 2026-11-04).
SMALL_RUNGS = {
    ("corruption", 0): [(5, "Stay behind the shelf in the library's back stacks and watch"),
                        (10, "Move one aisle closer in the library's back stacks"),
                        (15, "Turn the sound up on channel 5 when you're alone")],
    # exhibition phase 1 (LO, 2026-11-08): the looks that pay at 0 name the way to 5; the shower door opens at 5,
    # so it names the way to 10 (it showed at 10 before, a card against the build)
    ("exhibitionism", 0): [(5, "Let people look at you: at home, in class, at the café. Don't cover up"),
                           (10, "Leave the shower door unlocked, and keep letting them look"),
                           (15, "Keep letting them look, at home, in class and out")],
}

# ── her two stages: what the next rung opens (the-voice.md R2; DECISIONS: stages at 20/40/60) ──
for trait_k, bands in [
    ("corruption", [(0, 20, "Good Girl. Curious opens at 20: watching, touching yourself, a kiss, a dare.",
                     "Look when you should look away: the park couple, the library stacks. Stay longer"),
                    (20, 40, "Curious. Bold opens at 40: hands, mouths, a price for a look.",
                     # pass 3 H43 (the-voice.md R3): every line names a place and a verb, not a list of rooms
                     "Touch yourself: in bed, in the shower, in a college stall. Then watch again"),
                    # DECISIONS 124: release 1 reaches Hungry
                    (40, 60, "Bold. Hungry opens at 60: the taboo at home, strangers who can see, a room watching.",
                     "Go further with the ones who want you: Ryan's couch, the gym locker room"),   # playtest 2026-11-09: no unmet name on a card   # pass 4: a watched dare now needs Corruption 60, so it pays nothing at Bold   # the street pays Corruption only on a level's first day out (played 2026-11-04), so no card sends her there for it
                    (60, 80, "Hungry. Shameless is the next release: a crowd, free use.",
                     "Shameless (Corruption 80) opens in the next release")]),
    ("exhibitionism", [(0, 20, "Covered. It goes up when people look and you let them. Daring opens at 20: no bra, a short skirt out, bigger tips.",
                        # pass 3 G15: only places that pay her Exhibitionism while she is Covered (park_run, the
                        # street's looks, the shower walk-ins); the lecture hall pays nothing below Daring
                        "Let them look, everywhere you go. Every place pays once a day"),   # pass 4 G15: the park and street dress codes need Curious while she is Covered   # round 2: "at home" named the whole house, which pays nothing at 0
                       (20, 40, "Daring. Showing opens at 40: no panties out, naked for someone you know, your feed.",
                        # pass 3 G15: the garden pays only from Showing (garden_sun), so it is not a way through Daring
                        "Wear less out: the short skirt on the street, the curtain left open, the towel slipping"),   # LO, 2026-11-04: the street and park pay to 39 again; the curtain opens here
                       (40, 60, "Showing. Watched opens at 60: a room watching, a stranger.",
                        # what pays while she is Showing (garden_sun, the wind and the street with no panties, cap 59, the
                        # towel drops); the park stops at 39 (LO, 2026-11-04), and nothing repeatable pays it in the lecture hall;
                        # the gym's mats in the tiny shorts do, cap 59 (DECISIONS 198)
                        "Show off where you could be caught: the garden lounger, the street with nothing under your skirt"),
                       (60, 80, "Watched. Do your squats at the gym in the sheer leggings. A crowd comes in the next release.",
                        "On Display (Exhibitionism 80) opens in the next release: posing for the figure-drawing class")])]:
    for lo, hi, text, label in bands:
        card = {"group": f"tier_{trait_k}", "priority": 5, "text": text,
                "when": [{"flag": "opening_done", "op": "is_true"},
                         {"type": "trait", "subject": "player", "trait": trait_k, "op": "gte", "value": lo},
                         {"type": "trait", "subject": "player", "trait": trait_k, "op": "lt", "value": hi}],
                "goals": [*[{"type": "trait", "subject": "player", "trait": trait_k, "op": "gte", "value": v, "label": l}
                            for v, l in SMALL_RUNGS.get((trait_k, lo), [])],
                          {"type": "trait", "subject": "player", "trait": trait_k, "op": "gte", "value": hi, "label": label}]}
        if hi == 80:
            # The climb stops at 79 in this release (DECISIONS 142), so a goal at 80 can never flip: the top card is
            # terminal and says where the stage ends, with no live goal (the-voice.md "Never dangle a live goal bullet
            # that cannot flip in this build"; engine.md §23; pass 3 H48)
            del card["goals"]
            card.update(terminal=True, terminal_text=label)
        cards.append(card)

# THE WALK-INS OUTSIDE THE HOUSE (heat proposal B9-B20, DECISIONS 147 chunk 3): walkins_out.py holds the canvases and
# the router rules. Here: the rules on this file's three hosts, the check that 3_activities.toml's hosts carry the same
# rules, and every walk-in canvas (emitted once, here).
import os
import walkins_out
import everyday   # DECISIONS 222: Tom's everyday walk-ins on her coffee
everyday.attach_subs(out)
_done = walkins_out.attach(out)
assert _done == {"cafe_coffee", "vance_house_look", "zoe_bedroom_look"}, _done
walkins_out.check_toml_hosts(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "toml_phases", "3_activities.toml"))
out += walkins_out.CANVASES

text = "# ── rows so no place stands empty, the uniform's readers, cards for the light cast and her stages ──\n"
text += "".join(emit(c) for c in out) + "".join(emit_card(c) for c in cards)
open(__import__("sys").argv[1], "w").write(text)
print("extras:", len(out), "canvases,", len(cards), "cards")
