"""first_term — the places and people, as data. Source of truth: the signed sheets
(games/first_term/sheets/places, sheets/people) and the ledger (v2_state.json board)."""
from tomlw import *
import json, os

# ── clothing rules: what she may wear OUT of the house (wardrobe sheet: the seven states) ──
TOWEL_RULE = {"conditions": cond({"type": "worn_type", "operator": "eq", "value": "towel"}),
              "slots_required": ["legwear"],
              "message": "Not in a towel. Get dressed first."}
SLEEP_RULE = {"conditions": cond({"type": "worn_type", "operator": "eq", "value": "sleep_shirt"}),
              "slots_required": ["legwear"],
              "message": "Not in your sleep shirt. Get dressed first."}
SKIRT_RULE = {"conditions": cond({"type": "worn_type", "operator": "eq", "value": "short_skirt"},
                                trait("exhibitionism", "lt", 20)),
              "slots_required": ["legwear"],
              "message": "Not in that skirt. Not yet. (Going out in it needs Daring.)"}
PUBLIC_RULES = [
    TOWEL_RULE, SLEEP_RULE, SKIRT_RULE,
    {"conditions": cond(trait("exhibitionism", "gte", 40)),
     "slots_required": ["top", "bottom"],
     "message": "Not like this. Not out there. Put something on."},
    {"conditions": cond(trait("exhibitionism", "gte", 20)),
     "slots_required": ["underwear", "top", "bottom"],
     "message": "Not like this. Not yet. (No panties out of the house needs Showing.)"},
    {"slots_required": ["bra", "underwear", "top", "bottom"],
     "message": "Not like this. Not yet. (Going out without a bra needs Daring.)"},
]
# The park: at Daring she may run in a bra with nothing over it (the park sheet).
PARK_RULES = [
    TOWEL_RULE, SLEEP_RULE, SKIRT_RULE,
    {"conditions": cond(trait("exhibitionism", "gte", 20),
                        {"type": "clothing_slot", "slot": "bra", "operator": "equipped"}),
     "slots_required": ["underwear", "bottom"],
     "message": "Not like this. Not yet."},
] + PUBLIC_RULES[3:]

H = lambda wds, a, b: {"weekdays": wds, "open": a, "close": b}
ALL = [0, 1, 2, 3, 4, 5, 6]
WEEK = [0, 1, 2, 3, 4]

OFFICE_CLOSED = "The office is locked. Office hours are on the door."

# id, name, entry_from, kind, hours, closed_text, hidden_until, rules, costs, description
LOCATIONS = [
    dict(id="street", name="Your Street", entry_from=None, kind="thoroughfare",
         costs={"time": 10}, rules=PUBLIC_RULES,
         description=("Your street: the way out to everything. Your house is halfway down with Mr. Vance's porch "
                      "next door. The town starts at the corner: the park, the café, the clothes shop, "
                      "Zoe's building and the college gates. Every trip out walks this pavement, and every "
                      "neighbour with a window sees what you wore to do it.")),
    # ── the house ──
    dict(id="home_hall", name="Hall", entry_from="street", kind="thoroughfare",
         door=dict(
             description="Your front door, from the street. The house behind it.",
             no_answer="You stand at your own front door with your key out.",
             options=[
                 dict(text="Go in.",
                      conditions=cond(tod("06:00", "22:00")),
                      goes_to={"type": "enter"}),
                 dict(text="Let yourself in.",
                      conditions=cond(tod("22:00", "06:00")),
                      goes_to={"type": "canvas", "canvas_id": "hall_home_late"}),
             ]),
         description=("The hall: the middle of the house, and the stairs. Every door opens off it — the kitchen, "
                      "the living room, the garage, the one bathroom, the three bedrooms, the front door. "
                      "There's a mirror by the coats, and the stairs carry every sound up and down. Nothing "
                      "happens in this house that the hall doesn't hear first.")),
    dict(id="home_kitchen", name="Kitchen", entry_from="home_hall", kind="destination",
         description=("The kitchen: where this family eats, argues and pays. Laura makes breakfast here before "
                      "work and pours her wine here at night. Mark cooks on Wednesdays and owns the table on "
                      "Sundays, when he counts the rent into an envelope with Vance's name on it. The drawer "
                      "by the fridge is where the letters go that nobody wants to open."),
         variants=[
             (cond(wd(6), tod("08:00", "12:00")),
              "Sunday morning. Mark is already at the table with the envelope and a cold coffee, and the "
              "chair across from him is pulled out for you."),
             (cond(wd(0, 1, 2, 3, 4), tod("06:30", "08:00")),
              "Breakfast. Laura moves between the kettle and the toaster in her work blouse, and the "
              "radio is on low."),
         ]),
    dict(id="home_living_room", name="Living Room", entry_from="home_hall", kind="destination",
         description=("The living room: the couch, the big television and the dark after everyone goes up. Mark "
                      "stays down here late with the sound low, long after Laura is asleep. On Saturday nights "
                      "Laura waits up here, lights off, where she can see the front door. Lie on the couch and "
                      "whoever walks through sees exactly what you're wearing.")),
    dict(id="home_master_bedroom", name="Master Bedroom", entry_from="home_hall", kind="destination",
         description=("Laura and Mark's room: their bed, Laura's long mirror and a wardrobe full of dresses she "
                      "doesn't wear any more. It smells of her perfume. When they're both out, the wardrobe is "
                      "yours to go through. When she's up and dressing, you knock; at night, while they sleep, you don't."),
         # Iteration 002, part 2 (home_master_bedroom.md:34-54, Q58, LO's play note): no knock on a
         # sleeping room. Every row that puts them in here asleep lies inside 22:00-07:00; the one
         # awake row is Laura dressing, Saturday 17:00-18:30.
         door=dict(
             description="Laura and Mark's door, at the end of the landing.",
             no_answer="You knock. Nobody comes to the door.",
             options=[
                 dict(text="Knock.",
                      conditions=cond({"type": "npc_at_location", "location_id": "home_master_bedroom",
                                       "npc_id": "npc_laura", "operator": "is_present"},
                                      {"type": "weekday", "weekdays": [5]}, tod("17:00", "18:30")),
                      goes_to={"type": "enter"}),
                 dict(text="Ease the door open.",
                      conditions=cond({"type": "npc_at_location", "location_id": "home_master_bedroom",
                                       "operator": "is_present"}, tod("22:00", "07:00")),
                      goes_to={"type": "canvas", "canvas_id": "master_asleep"}),
                 dict(text="Go in.",
                      conditions=cond({"type": "npc_at_location", "location_id": "home_master_bedroom",
                                       "operator": "is_absent"}),
                      goes_to={"type": "enter"}),
             ])),
    dict(id="home_ella_room", name="Your Room", entry_from="home_hall", kind="destination",
         description=("Your room: your bed, your clothes, your mirror and your phone on charge. It's small, "
                      "but it's the only door in the house that's yours. The wall behind your headboard is the same wall as "
                      "Ryan's, and it is thin. Here you sleep, change, check your feed and see yourself the way "
                      "everyone else is going to.")),
    dict(id="home_ryan_room", name="Ryan's Room", entry_from="home_hall", kind="destination",
         description=("Ryan's room: his bed, his weights in the corner, his phone always face-down. He's home "
                      "most evenings and every night, and the door is usually shut. You knock to go in. Two "
                      "knocks means it's you."),
         door=dict(
             description="Ryan's door. A strip of light under it when he's home.",
             no_answer="You knock. Nothing. He's out.",
             options=[
                 dict(text="Knock.",
                      conditions=cond({"type": "npc_at_location", "location_id": "home_ryan_room",
                                       "npc_id": "npc_ryan", "operator": "is_present"},
                                      flag("ryan_knock_code", False)),
                      goes_to={"type": "enter"}),
                 dict(text="Two knocks.",
                      conditions=cond({"type": "npc_at_location", "location_id": "home_ryan_room",
                                       "npc_id": "npc_ryan", "operator": "is_present"},
                                      flag("ryan_knock_code")),
                      goes_to={"type": "enter"}),
                 dict(text="Go in.",
                      conditions=cond({"type": "npc_at_location", "location_id": "home_ryan_room",
                                       "npc_id": "npc_ryan", "operator": "is_absent"}),
                      show_when_locked=True, locked_text="He's in there. Knock first.",
                      goes_to={"type": "enter"}),
             ])),
    dict(id="home_bathroom", name="Bathroom", entry_from="home_hall", kind="destination",
         description=("The one bathroom, for four people. A shower with a door that doesn't quite shut, a sink, "
                      "a lock that sticks. Ryan has it first on weekday mornings. A shower keeps you clean, and "
                      "in this house somebody always needs the room while you're in it.")),
    dict(id="home_garage", name="Garage", entry_from="home_hall", kind="destination",
         description=("The garage: Mark's workbench, his radio, a fridge of beer and a filing box he keeps "
                      "locked. He spends his evenings out here, and his Saturdays. When he's out, his things "
                      "are just sitting there.")),
    dict(id="home_front_door", name="Front Door", entry_from="home_hall", kind="destination",
         description=("The front door and the step outside it: where the house meets the street. The porch "
                      "light is on a timer. You can sit on the step and watch the street go by, and on a "
                      "Saturday night, this is where a date ends — in full view of the living-room window.")),
    dict(id="vance_house", name="Vance's House", entry_from="street", kind="destination",
         hours=[H(ALL, "18:00", "22:00")], closed_text="Vance's porch is empty. The curtains are shut.",
         description=("Next door: Mr. Vance's house, and his porch. He owns your house too, but it's Mark who owes him. "
                      "Every evening he sits out there with a paper he doesn't read, and watches the street. "
                      "Walk past and he looks at what you wore.")),
    dict(id="park", name="Park", entry_from="street", kind="destination",
         hours=[H(ALL, "07:00", "22:00")], closed_text="The park gates are locked for the night.",
         rules=PARK_RULES,
         description=("The park at the end of the street: paths, a pond, benches and thick bushes along the far "
                      "side. People walk here, run here, sit here. You can walk, run or rest on a bench, and what "
                      "you wear decides who turns to look. Zoe runs here on weekend mornings.")),
    # ── campus ──
    dict(id="campus", name="Campus", entry_from="street", kind="thoroughfare",
         hours=[H(ALL, "07:00", "22:00")], closed_text="The college gates are shut.", rules=PUBLIC_RULES,
         description=("The college: brick buildings round a green, and students cutting across it with coffee. "
                      "From the gates you can reach the quad, the lecture hall, the library, the canteen, the "
                      "women's toilets and the faculty floor where the offices are.")),
    dict(id="quad", name="Quad", entry_from="campus", kind="destination",
         hours=[H(ALL, "07:00", "22:00")], closed_text="The quad is dark and empty.", rules=PUBLIC_RULES,
         description=("The quad: the big lawn in the middle of campus, where people sit between classes and "
                      "everybody watches everybody. Jake's team hangs out here in the mornings; Zoe lies on the "
                      "grass in the afternoons. Sit down and you'll hear what campus is saying — sometimes "
                      "about you.")),
    dict(id="lecture_hall", name="Lecture Hall", entry_from="campus", kind="destination",
         hours=[H([0, 1, 2, 3], "08:30", "14:30"), H([4], "08:30", "10:00")],
         closed_text="No class now. The timetable is on the door.", rules=PUBLIC_RULES,
         description=("The lecture hall: raked rows of seats down to a lectern, where all four of your classes "
                      "are held — Psychology, Business, Biology and Figure drawing. Classes run in the morning "
                      "and after lunch. Sit in the front row and the lecturer can see everything; sit at the back "
                      "and nobody can see your hands.")),
    dict(id="library", name="Library", entry_from="campus", kind="destination",
         hours=[H(WEEK, "08:00", "20:00")], closed_text="The library is closed.", rules=PUBLIC_RULES,
         description=("The library: long tables, green lamps and silence. Study here and you learn. It's dull, "
                      "but the exams read it. Nadia studies here most afternoons.")),
    dict(id="canteen", name="Canteen", entry_from="campus", kind="destination",
         hours=[H(WEEK, "08:00", "18:00")], closed_text="The canteen is shut.", rules=PUBLIC_RULES,
         description=("The canteen: trays, plastic chairs and the loudest room on campus. Food costs money, "
                      "but it puts energy back. At lunch everyone is here, and whatever campus is saying, it's said "
                      "here first.")),
    dict(id="college_womens_toilet", name="Women's Toilet", entry_from="campus", kind="destination",
         hours=[H(ALL, "07:00", "22:00")], closed_text="The college gates are shut.",
         description=("The women's toilets by the lecture hall: four stalls, a long mirror and a sink. A quick "
                      "wash between classes, a look at yourself, a change of clothes behind a locked stall door. "
                      "The door to the corridor doesn't lock.")),
    dict(id="faculty_floor", name="Faculty Floor", entry_from="campus", kind="thoroughfare",
         hours=[H(WEEK, "08:00", "19:30")], closed_text="The faculty floor is locked.", rules=PUBLIC_RULES,
         description=("The faculty floor: one long corridor of office doors with name cards. Dr. Hale, the art "
                      "lecturer, the Business lecturer, the Biology TA and the dean. Each door has its office "
                      "hours taped to it, and your grades are posted on them.")),
    dict(id="hale_office", name="Dr. Hale's Office", entry_from="faculty_floor", kind="destination",
         hours=[H([3], "17:00", "19:30")], closed_text=OFFICE_CLOSED, rules=PUBLIC_RULES,
         description=("Dr. Hale's office: books to the ceiling, one window, a desk with a photo of his wife on "
                      "it. He holds office hours on Thursday evenings, and his wife picks him up after. Your "
                      "Psychology grade is pinned to the door.")),
    dict(id="art_office", name="Art Lecturer's Office", entry_from="faculty_floor", kind="destination",
         hours=[H([0, 1, 3, 4], "14:30", "18:00")], closed_text=OFFICE_CLOSED, rules=PUBLIC_RULES,
         description=("The art lecturer's office: canvases stacked against the walls, charcoal dust on "
                      "everything, sketches of bodies pinned up to dry. Your Figure drawing grade is on the door.")),
    dict(id="business_office", name="Business Lecturer's Office", entry_from="faculty_floor", kind="destination",
         hours=[H([0, 2, 3, 4], "14:30", "18:00")], closed_text=OFFICE_CLOSED, rules=PUBLIC_RULES,
         description=("The Business lecturer's office: filing cabinets, a clock that ticks, nothing personal. "
                      "He offers an honest retake, but nothing else. Your Business grade is on the door.")),
    dict(id="ta_office", name="TA's Office", entry_from="faculty_floor", kind="destination",
         hours=[H([1, 2, 3, 4], "14:30", "18:00")], closed_text=OFFICE_CLOSED, rules=PUBLIC_RULES,
         description=("The Biology TA's office: a shared room with two desks, a skeleton on a stand and a "
                      "kettle. She keeps her door half open. Your Biology grade is on it.")),
    dict(id="dean_office", name="Dean's Office", entry_from="faculty_floor", kind="destination",
         hours=[H(WEEK, "09:00", "17:00")], closed_text=OFFICE_CLOSED, rules=PUBLIC_RULES,
         hidden_until="dean_summons",
         description=("The dean's office: a secretary's desk outside, a heavy door, a big desk and two hard "
                      "chairs. You come here when there's trouble: grades, complaints, probation. A notice on "
                      "the door lists who has been called in.")),
    # ── town ──
    dict(id="cafe", name="Café", entry_from="street", kind="destination",
         hours=[H([0, 1, 2, 3, 4, 5], "08:00", "23:00")], closed_text="Closed. Back Monday.", rules=PUBLIC_RULES,
         description=("The café by the corner: a counter, eight booths and a back room with a staff mirror. "
                      "Tom runs it. Shifts pay a small wage, but the tips go up with how you look in "
                      "the uniform. Regulars, mostly men. Gary takes booth four. Shifts end when the café shuts; "
                      "Tom stays on to close.")),
    dict(id="clothes_shop", name="Clothes Shop", entry_from="street", kind="destination",
         hours=[H([0, 1, 2, 3, 4, 5], "10:00", "18:00")], closed_text="Closed.", rules=PUBLIC_RULES,
         description=("A clothes shop on the strip: racks, a changing room with a curtain, a bored assistant. "
                      "What you buy here changes what you can wear, and what people do when they see it.")),
    dict(id="zoe_apartment", name="Zoe's Apartment", entry_from="street", kind="destination",
         hours=[H([0, 1, 2, 3, 5], "18:00", "24:00"), H([4], "18:00", "02:00")],
         closed_text="Zoe's out. Nobody answers.", hidden_until="zoe_met", rules=PUBLIC_RULES,
         description=("Zoe's apartment, three floors up: a couch, a balcony, fairy lights and a bedroom off the "
                      "living room. She's home most evenings, but on Fridays she isn't alone. On Fridays the whole flat is the party — music, "
                      "drinks, half of campus and dares.")),
    dict(id="zoe_bedroom", name="Zoe's Bedroom", entry_from="zoe_apartment", kind="destination",
         hours=[H([0, 1, 2, 3, 5], "18:00", "24:00"), H([4], "18:00", "02:00")],
         closed_text="Zoe's out. Nobody answers.", hidden_until="zoe_met",
         description=("Zoe's bedroom: an unmade bed, clothes on every surface and a full-length mirror. Her "
                      "wardrobe is yours to borrow from, and she watches you change. On party nights the door "
                      "stays open.")),
    dict(id="party_house", name="The Party House", entry_from="street", kind="destination",
         hours=[H([5], "20:00", "03:00")], closed_text="Dark. Nobody's home.", hidden_until="party_house_invite",
         description=("A big house at the edge of town where Zoe's friends throw Saturday nights. Music inside, "
                      "a garden out back and a hot tub steaming under the stars. Zoe's friends only.")),
]

# =============================================================================
# Iteration 002 — the map from the everyday pass (ledger L1–L9, L18, L19; DECISIONS 43–51, 64, 65).
#
# Areas: Home, Campus and Town are containers with `crossing_costs` (Home 10, Campus 15, Town 15),
# charged once on the way in; the engine finds an area through each room's `parent` chain
# (v2.py:11398-11433), so every room inside an area names its `parent`. A building with a
# `default_entry` (Home, Zoe's Flat) redirects to that room, which must have the container as its
# parent and no `entry_from` (template_import.py:5183-5195). The park's 10 minutes is its own
# `costs`. Hours, closed text, hidden flags and costs come from the ledger below, never hand-copied.
# The men's toilet stays out: its sheet says "not in 0.1" (LO, 2026-10-07; ledger in_release false).
# =============================================================================
_BY_ID = {l["id"]: l for l in LOCATIONS}


def _set(loc_id, **kw):
    _BY_ID[loc_id].update(kw)


def _add(after_id, loc):
    i = next(n for n, l in enumerate(LOCATIONS) if l["id"] == after_id)
    LOCATIONS.insert(i + 1, loc)
    _BY_ID[loc["id"]] = loc


# ── the street: the ground, no toll of its own; the minutes said once (Q65, exact words) ──
_BY_ID["street"].pop("costs", None)
_set("street", description=(
    "Your street: the way out to everything. Home is halfway down, with Mr. Vance's porch next door, "
    "the corner shop on the corner and the park at the far end. Campus is fifteen minutes on foot. "
    "Town is the bus, fifteen. Home is ten. Every trip out walks this pavement, and every neighbour "
    "with a window sees what you wore to do it."))

# ── Home: a building over the house rooms; the street shows "Home" and it opens in the hall ──
_add("street", dict(
    id="home", name="Home", entry_from="street", kind="thoroughfare",
    is_container=True, default_entry="home_hall", crossing_costs={"time": 10},
    description="Home: the house you share with Laura, Mark and Ryan. The front door opens into the hall."))
_HOUSE = ["home_hall", "home_kitchen", "home_living_room", "home_master_bedroom", "home_ella_room",
          "home_ryan_room", "home_bathroom", "home_garage", "home_front_door"]
for _r in _HOUSE:
    _set(_r, parent="home")
_BY_ID["home_hall"].pop("entry_from", None)          # the building's default_entry has none
# The hall's late door is gone: with Home a building, the street's "Home" opens the hall directly
# (v2.py:11112-11121) and never shows a door on it. LO, 2026-10-09 (iteration 002): no
# came_home_late from the street; Laura's catch reads only the outing flags.
_BY_ID["home_hall"].pop("door", None)
_set("home_hall", description=(
    "The hall: the middle of the house, and the stairs. Every door opens off it: the kitchen, the "
    "living room, the garage, the one bathroom, the three bedrooms, the front door, and the back door "
    "to the garden. There's a mirror by the coats, and the stairs carry every sound up and down."))
_add("home_front_door", dict(
    id="home_garden", name="Garden", entry_from="home_hall", parent="home", kind="destination",
    description=("The garden out the back door: a square of grass, a washing line, one lounger and a "
                 "fence low enough to see over. The garage door opens onto it, and so does Ryan's window. "
                 "Lie in the sun here and whoever's home can see exactly what you're wearing.")))

# ── on the street: Vance (0 min), the park (its own 10), the corner shop (0) ──
_set("vance_house", description=(
    "Next door: Mr. Vance's house, and his porch. He owns your house too, and Mark pays him every "
    "Sunday. Most evenings he sits out there with a paper he doesn't read and watches the street. "
    "Walk past and he looks at what you wore."))
# In 0.1 the corner shop is for the grocery run only (LO Q50; corner_shop.md): it opens on an errand.
_add("park", dict(
    id="corner_shop", name="Corner Shop", entry_from="street", kind="destination", rules=PUBLIC_RULES,
    entry_conditions=cond(flag("grocery_list"), flag("groceries_bought", False)),
    blocked_message="You've got nothing to buy.",
    description=("The corner shop: three narrow aisles, a fridge that hums, a clerk behind the till who "
                 "never looks up from his phone. Bread, milk, wine. This is where Laura's shopping list "
                 "gets bought.")))

# ── Campus: an area, no hours, no content; its 500 words moved to the quad (L2) ──
for _k in ("hours", "closed_text", "rules"):
    _BY_ID["campus"].pop(_k, None)
_set("campus", is_container=True, crossing_costs={"time": 15}, description=(
    "The college: brick buildings round a green, and students cutting across it with coffee."))
_CAMPUS = ["quad", "lecture_hall", "library", "canteen", "college_womens_toilet", "faculty_floor",
           "hale_office", "art_office", "business_office", "ta_office", "dean_office"]
for _r in _CAMPUS:
    _set(_r, parent="campus")
_add("college_womens_toilet", dict(
    id="college_mens_toilet", name="Men's Toilet", entry_from="campus", parent="campus",
    kind="destination", hours=[H(ALL, "07:00", "22:00")], closed_text="The college gates are shut.",
    description=("The men's toilets across the corridor from the women's: a row of urinals, two stalls "
                 "and a mirror nobody looks in.")))
_add("college_mens_toilet", dict(
    id="campus_gym", name="Gym", entry_from="campus", parent="campus", kind="destination",
    rules=PARK_RULES,
    description=("The college gym: racks of weights, a row of treadmills facing the mirror wall, mats in "
                 "the corner and a locker room at the back. Work out here and you get fitter. What you "
                 "train in is what everybody in that mirror sees.")))

# ── Town: an area off the street, the bus, 15 minutes, no fare (L3, Q45) ──
_add("dean_office", dict(
    id="town", name="Town", entry_from="street", kind="thoroughfare",
    is_container=True, crossing_costs={"time": 15},
    description="Town: the bus stop, the shops, the café and the flats above them."))
for _r in ("cafe", "clothes_shop", "party_house"):
    _set(_r, entry_from="town", parent="town")
_set("cafe", description=(
    "The café on the town strip: a counter, eight booths and a back room with a staff mirror. Tom runs "
    "it. Shifts pay a small wage, but the tips go up with how you look in the uniform. Regulars, "
    "mostly men. Shifts end when the café shuts; Tom stays on to close."))
_set("party_house", description=(
    "A big house at the edge of town where Zoe's friends throw Saturday nights. Music inside, a garden "
    "out back and a hot tub steaming under the stars. Zoe's friends only."))

# ── Zoe's Flat: a building in Town, laid out like a flat (L4, Q47) ──
_add("clothes_shop", dict(
    id="zoe_flat", name="Zoe's Flat", entry_from="town", parent="town", kind="thoroughfare",
    is_container=True, default_entry="zoe_apartment",
    description="Zoe's flat, three floors up. Her front door opens into the living room."))
_BY_ID["zoe_apartment"].pop("entry_from", None)      # the building's default_entry has none
_set("zoe_apartment", parent="zoe_flat", name="Zoe's Living Room", description=(
    "Zoe's living room: a couch, a balcony door, fairy lights and music always on. The kitchen, the "
    "bathroom and her bedroom open off it. On Fridays the whole flat is the party: music, drinks, half "
    "of campus and dares."))
_add("zoe_apartment", dict(
    id="zoe_kitchen", name="Zoe's Kitchen", entry_from="zoe_apartment", parent="zoe_flat",
    kind="destination",
    description=("Zoe's kitchen: a counter crowded with bottles, a fridge covered in photos, and cups "
                 "that are never clean. On party nights the drinks come from here.")))
_add("zoe_kitchen", dict(
    id="zoe_bathroom", name="Zoe's Bathroom", entry_from="zoe_apartment", parent="zoe_flat",
    kind="destination",
    description=("Zoe's bathroom: a mirror ringed with bulbs and a shelf of make-up you could live on. "
                 "Fix your face here. On party nights there's always somebody banging on the door.")))
_set("zoe_bedroom", parent="zoe_flat", description=(
    "Zoe's bedroom: an unmade bed, clothes on every surface and a full-length mirror. Her wardrobe is "
    "where the good dresses are, and she lends them when she's here. On party nights the door stays "
    "shut unless Zoe opens it."))

# ── the ledger's fields, verbatim: name, kind, hours, closed text, hidden flag, costs ──
_LEDGER = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                      "..", "..", "..", "v2_state.json")))
_DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]


def _days(spec):
    out = []
    for part in spec.split(","):
        if "-" in part:
            a, b = part.split("-")
            out += list(range(_DAYS.index(a), _DAYS.index(b) + 1))
        else:
            out.append(_DAYS.index(part))
    return out


def _hours(text):
    """'Mon-Thu 08:30-14:30; Fri 08:30-10:00' → engine windows. No day part = every day.
    A close of 00:00 is written 24:00, midnight (engine.md "Opening hours")."""
    wins = []
    for chunk in text.split(";"):
        bits = chunk.strip().split()
        days, span = (ALL, bits[0]) if len(bits) == 1 else (_days(bits[0]), bits[1])
        a, b = span.split("-")
        wins.append(H(days, a, "24:00" if b == "00:00" else b))
    return wins


for _l in _LEDGER["board"]["locations"]:
    if not _l.get("in_release"):
        continue
    loc = _BY_ID[_l["id"]]
    loc["name"], loc["kind"] = _l["name"], _l["kind"]
    for _k in ("hours", "closed_text", "hidden_until", "costs"):
        loc.pop(_k, None)
    if _l.get("hours"):
        loc["hours"] = _hours(_l["hours"])
    if _l.get("closed_text"):
        loc["closed_text"] = _l["closed_text"]
    if _l.get("hidden_until"):
        loc["hidden_until"] = _l["hidden_until"]
    if _l.get("costs"):
        loc["costs"] = _l["costs"]
    if _l.get("crossing_costs"):
        loc["crossing_costs"] = _l["crossing_costs"]
# The men's toilet is built empty by LO's call (2026-10-09, iteration 002) though the ledger still
# says in_release false; its hours and closed line copy the women's toilet in the same building.
_LEDGER_IDS = {l["id"] for l in _LEDGER["board"]["locations"] if l.get("in_release")} | {"college_mens_toilet"}
assert set(_BY_ID) == _LEDGER_IDS, (set(_BY_ID) ^ _LEDGER_IDS)

ROOT = "street"


def children(loc_id):
    return [l["id"] for l in LOCATIONS if l.get("entry_from") == loc_id]
