"""first_term — the places and people, as data. Source of truth: the signed sheets
(games/first_term/sheets/places, sheets/people) and the ledger (v2_state.json board)."""
from tomlw import *

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
                      "yours to go through, but when they're home, you knock."),
         door=dict(
             description="Laura and Mark's door, at the end of the landing.",
             no_answer="You knock. Nobody comes to the door.",
             options=[
                 dict(text="Knock.",
                      conditions=cond({"type": "npc_at_location", "location_id": "home_master_bedroom",
                                       "operator": "is_present"}),
                      goes_to={"type": "enter"}),
                 dict(text="Go in.",
                      conditions=cond({"type": "npc_at_location", "location_id": "home_master_bedroom",
                                       "operator": "is_absent"}),
                      show_when_locked=True, locked_text="Somebody's in there. Knock.",
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

ROOT = "street"


def children(loc_id):
    return [l["id"] for l in LOCATIONS if l.get("entry_from") == loc_id]
