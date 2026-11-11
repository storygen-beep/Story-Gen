"""Media blocks for release 1 (sheets/media/release1.md, signed by LO 2026-11-12: "Sign it"; DECISIONS 238).

One row per block: (canvas id, node id, anchor, kind, name, what it shows, search words).
  anchor None   -> the block goes first on the screen (top)
  anchor "text" -> the block goes right after the paragraph containing that text, on the same screen
kind: "clip" (a video block) or "pic" (an image block). A name without an extension is a pool (`pool_dir`, the
engine cycles one file a visit); with an extension it is one file.

Placement (apply()):
  · the anchor found once -> right after that paragraph, in the same list, so a clothing version keeps its own
    picture. If the paragraph sits inside a block_pool (one entry picked per visit) the block goes after the pool,
    never into it (it would become an entry of its own).
  · the anchor found more than once (the same line repeated across clothing groups) -> after the last top-level
    block that holds it, and past the end of a raw group chain (adjacent groups render as one if/elseif chain,
    canv.py G/GC; a block between them would split it).
Every row must land: a row whose canvas, node or anchor isn't found stops the build, so the sheet and the game
can't drift apart. Rows for canvases a part doesn't emit are simply not applied by that part.
"""
from canv import IMG, VID

S = "screen"
ROWS = [
    # ── A · body moments ──
    ("bathroom_shower", "shower", None, "clip", "sex/shower_daily_t4",
     "a young woman alone in a small home shower, water running down her tits and back, eyes shut",
     "girl showering alone home bathroom", "woman under shower water eyes closed"),
    ("walkin_mirror_ryan", "answer", "his eyes go to the knot over your tits", "pic", "look/mirror_ryan_towel_t3",
     "a girl in a towel at a hall mirror; in the glass, a young man in a doorway behind her, staring",
     "girl towel hall mirror guy watching reflection"),
    ("walkin_mirror_ryan", "answer", "straight to your tits, then down to your pussy", "clip", "sex/mirror_ryan_naked_t4",
     "a naked girl at a hall mirror, a young man in a doorway behind her in the glass",
     "naked girl mirror man watching from doorway"),
    ("walkin_mirror_ryan", "answer", "your ass in your panties", "pic", "look/mirror_ryan_panties_t3",
     "a girl in bra and panties at a mirror, seen from behind, a guy in the doorway",
     "girl bra panties mirror seen from behind guy doorway"),
    ("walkin_mirror_ryan", "r_stay", "his hand goes to the front of his shorts", "clip", "sex/mirror_ryan_shorts_t4",
     "a young man in a doorway, hand pressing the bulge in his shorts, watching",
     "guy hand on bulge shorts watching girl"),
    ("walkin_mirror_mark", "answer", "his eyes go to the knot over your tits", "pic", "look/mirror_mark_towel_t3",
     "a girl in a towel at a hall mirror, an older man in his forties behind her in the glass",
     "girl towel mirror older man behind"),
    ("walkin_mirror_mark", "answer", "straight to your tits, then down to your pussy", "clip", "sex/mirror_mark_naked_t4",
     "a naked girl at a mirror, an older man close behind her, staring", "naked girl mirror older man behind her"),
    ("walkin_mirror_mark", "answer", "your ass in your panties", "pic", "look/mirror_mark_panties_t3",
     "a girl in bra and panties at a hall mirror, an older man passing behind", "girl underwear mirror older man walking past"),
    ("walkin_mirror_mark", "m_stay", "He stands right behind you", "pic", "look/mirror_mark_close_t3",
     "an older man standing close behind a girl at a mirror, not touching", "man standing close behind girl mirror tension"),
    ("hall_mirror", "mirror", "A towel, in the hall", "pic", "look/hall_mirror_towel_t3",
     "a girl in a towel in a narrow house hallway, doors all round", "girl in towel hallway nervous"),
    ("hall_mirror", "mirror", "Naked in the hall", "clip", "sex/hall_mirror_naked_t4",
     "a naked girl standing in a house hallway, looking at the doors", "naked girl standing in hallway house"),
    ("hall_mirror", "mirror", "Bra and panties in the hall", "pic", "look/hall_mirror_panties_t3",
     "a girl in bra and panties in a hallway at a mirror", "girl bra panties hallway mirror"),
    ("bathroom_mirror", "mirror", "Wet hair, pink skin", "pic", "look/bath_mirror_towel_t3",
     "a girl in a towel with wet hair at a steamy bathroom mirror", "girl wet hair towel bathroom mirror steam"),
    ("bathroom_mirror", "mirror", "You cup your tits and let them go", "clip", "sex/bath_mirror_naked_t4",
     "a naked girl at a small bathroom mirror, cupping her tits, on her toes", "naked girl bathroom mirror cupping breasts"),
    ("bathroom_mirror", "mirror", "Bra and panties, and the door doesn't lock properly", "pic", "look/bath_mirror_panties_t3",
     "a girl in bra and panties at a bathroom mirror, door open a crack behind", "girl underwear bathroom mirror door ajar"),
    ("home_event_ryan_towel", "event", "Ryan steps out in a towel, wet, steam behind him", "pic", "look/ryan_towel_hall_t3",
     "a young man stepping out of a bathroom in a towel, wet, steam behind him, in a narrow hall",
     "guy in towel coming out of bathroom steam"),
    # the washer: two clips, her then him (LO, 2026-11-12)
    ("walkin_laundry_mark", "moment", "bent right over at the drum, feeding it, your ass up in the air", "clip", "sex/washer_bent_her_t4",
     "a girl bent right over at a front-loading washer, her ass up in the air",
     "girl bent over washing machine", "girl bending over laundry from behind"),
    ("walkin_laundry_mark", "answer", "his beer hand drops in front of his jeans", "clip", "sex/washer_hard_him_t4",
     "a man in his forties in a garage doorway, beer in hand, the bulge in his jeans",
     "man bulge jeans watching", "guy getting hard in jeans"),
    ("walkin_laundry_mark_sat", "moment", "your ass up in the air", "clip", "sex/washer_sat_bent_her_t4",
     "a girl bent right over at a washing machine drum, her ass up, morning light", "girl bending over laundry morning"),
    ("walkin_laundry_mark_sat", "answer", "The front of his jeans is tight", "clip", "sex/washer_sat_hard_him_t4",   # the one version where he stays and it shows (reader 2026-11-12)
     "an older man in a garage doorway with a coffee mug, staring, the front of his jeans tight", "man coffee mug staring bulge jeans"),
    ("mark_00_the_dryer", "hose", "soaks you from the neck down", "clip", "sex/hose_soaked_t4.webm",
     "a girl soaked by a burst washer hose, her wet top see-through, gasping", "girl soaked wet shirt see through gasping"),
    ("mark_00_the_dryer", "stay", "you let him see you not take it", "pic", "look/hose_stay_t3.jpg",
     "a girl dripping wet in a garage, her shirt soaked through, an older man with his back to her",
     "soaked girl garage man back turned"),
    ("living_couch", "couch", "hold it over your bra", "pic", "look/couch_bra_t3",
     "a girl lying on a couch in her bra and panties, a cushion pulled over her chest, a man in the doorway",
     "girl underwear couch cushion man doorway"),
    ("garden_sun", "sun", None, "pic", "life/garden_lounger_t0",
     "a sun lounger in a small back garden in the sun, a low fence", "sun lounger back garden low fence"),
    ("garden_sun", "sun_wave", "Ryan jerks back from the glass", "pic", "look/garden_window_ryan_t3",
     "a young man at an upstairs window looking down into a garden", "guy at window looking down at garden"),
    ("park_run", "run", "Just the sports bra and your leggings", "pic", "look/run_sportsbra_t3",
     "a girl running in a sports bra and leggings round a park pond, heads turning", "girl jogging sports bra leggings park"),
    ("park_run", "run", "your tits bounce, your nipples hard against the cloth", "clip", "sex/run_nobra_t4",
     "a braless girl jogging, her tits bouncing under a thin top", "braless jogging bouncing"),
    ("park_run", "run_plain", "watches your ass the whole way round", "pic", "look/run_bench_man_t3",
     "a girl in leggings jogging past an older man on a park bench who watches", "girl leggings jogging past man on bench"),
    ("master_asleep", "dark", "Mark's on his back beside her, snoring", "pic", "look/master_asleep_t3",
     "a dark bedroom seen through a door gap, someone asleep in the bed",
     "dark bedroom door gap someone sleeping"),
    ("laura_alone_peek", "peek", "Her nightdress is still rucked up over her hip", "pic", "sex/laura_alone_peek_t4",
     "through a door gap, a woman in her forties asleep on her side, nightdress rucked up over her bare hip",
     "woman asleep nightdress rucked up door gap"),
    ("master_door_peek", "peek", "The lamp is still on.", "pic", "look/master_door_peek_t3",
     "a bedroom seen through a door gap, the lamp on", "bedroom door ajar lamp on"),
    ("ev_ryan_hall_squeeze", "scene", "squeeze past with your tits against his chest", "pic", "look/hall_squeeze_t3",
     "a girl squeezing past a shirtless young man in a narrow hallway, chests nearly touching",
     "squeezing past shirtless guy narrow hallway"),
    ("walkin_hall_hale", "answer", "his eyes go down, to your legs, and stay there a second too long", "pic", "look/hale_door_legs_t3",
     "a professor in his late thirties at a lecture-hall door, coffee in hand, eyes on a student's legs",
     "professor looking at student legs lecture hall"),
    ("walkin_door_dean", "door", "He looks you down and up, once, slowly", "pic", "look/dean_door_look_t3",
     "a man of 55 in a suit opening a heavy office door, a file under his arm",
     "older man suit opening office door file under arm"),
    ("town_event_wind", "event", "Your ass is out to the whole street", "clip", "sex/wind_skirt_t4",
     "wind lifting a girl's short skirt on a street, a man across the road", "wind blows skirt up street"),
    ("town_event_split_wind", "event", "your panties are out to the st", "clip", "sex/wind_slit_t4",
     "wind throwing open the slit of a long skirt to the waist on a street corner", "wind slit skirt flies open"),
    ("town_event_whistle", "event", "whistles, long, at your tits", "pic", "look/car_whistle_t3",
     "a car crawling beside a braless girl on a pavement, a guy leaning out of the window", "guy in car whistling at girl walking"),
    ("town_event_jogger", "event", "looks back over his shoulder at your ass, twice", "pic", "look/jogger_looks_back_t3",
     "a jogger looking back over his shoulder at a girl's ass as they pass", "jogger turns to look at girl's butt"),
    ("street_seen_lowtop", "seen", "straight at your tits in the low-cut top", "pic", "look/busstop_lowtop_t3",
     "a man at a bus stop staring at a girl's cleavage in a low-cut top", "man staring at cleavage bus stop"),
    ("street_seen_skirt", "seen", "His eyes go up your legs to the hem of your skirt", "pic", "look/porch_skirt_t3",
     "an older man on a porch with a newspaper watching a girl in a short skirt walk past",
     "old man porch watching girl short skirt walk by"),
    # the low-cut-top look in class: one block per class (one asset, one block)
    ("college_class_psych", "class", "keeps dropping his pen", "pic", "look/class_downblouse_psych_t3",
     "a guy in a lecture seat leaning down for his pen, looking down the low-cut top of the girl beside him",
     "guy looking down girl's top in class"),
    ("college_class_business", "class", "the low-cut top gapes", "pic", "look/class_downblouse_business_t3",
     "a guy in the row behind looking down a girl's gaping low-cut top as she leans forward to write",
     "guy behind looking down girl's top lecture"),
    ("college_class_bio", "class", "leans over your bench to check your diagram", "pic", "look/class_downblouse_bio_t3",
     "a shy young woman TA leaning over a student's bench, her eyes sliding down the student's low-cut top",
     "teacher glancing at student cleavage lab"),
    ("college_class_figure", "class", "He's not even pretending now", "pic", "look/class_downblouse_figure_t3",
     "a guy at the next easel looking down the front of a girl's low-cut top while she draws",
     "guy at easel looking down girl's top art class"),
    # ── B · everyday screens: top, rotating ──
    ("college_class_psych", "class", None, "pic", "life/class_psych_t0",
     "a male professor in his late thirties in a tweed jacket at a lectern, a raked lecture hall, a girl in the front row",
     "professor tweed lectern lecture hall front row"),
    ("college_class_business", "class", None, "pic", "life/class_business_t0",
     "a stern gray-suited lecturer in his fifties with a register, a lecture hall", "strict older lecturer gray suit lecture"),
    ("college_class_bio", "class", None, "pic", "life/class_bio_t0",
     "a shy young woman TA in a lab coat and big earrings at a whiteboard, a cell diagram", "female teaching assistant lab coat whiteboard"),
    ("cafe_shift", "counter", None, "pic", "life/cafe_shift_t0",
     "a busy café counter: cups, plates, the coffee machine", "busy coffee shop counter cups"),
    ("cafe_coffee", "coffee", None, "pic", "life/cafe_stool_t0",
     "a girl on a stool at the end of a café counter with a coffee, watching the room", "girl coffee café counter stool"),
    ("kitchen_breakfast", "eat", None, "pic", "life/kitchen_breakfast_t0",
     "breakfast at a kitchen counter in the morning", "breakfast kitchen counter morning"),
    ("kitchen_dinner", "eat", None, "pic", "life/kitchen_dinner_alone_t0",
     "a girl eating alone in a kitchen in the evening", "girl eating alone kitchen evening"),
    ("kitchen_coffee", "coffee", None, "pic", "life/kitchen_window_coffee_t0",
     "a girl drinking coffee at a kitchen window", "girl coffee kitchen window"),
    ("kitchen_dishes", "dishes", None, "pic", "life/kitchen_dishes_t0",
     "a girl at a full sink of dishes, sleeves up", "girl washing dishes sink"),
    ("room_sleep", "bed", None, "pic", "life/room_bed_t0",
     "a girl getting under the covers of a single bed, a dim small bedroom", "girl getting into bed night"),
    ("room_nap", "nap", None, "pic", "life/room_nap_t0",
     "a girl asleep on top of her covers in daylight", "girl napping on bed daytime"),
    ("room_study", "desk", None, "pic", "life/room_desk_t0",
     "a girl studying at a cluttered desk in a small bedroom", "girl studying desk bedroom"),
    ("room_makeup", "mirror", None, "pic", "life/room_makeup_t0",
     "a girl doing her make-up at a bedroom mirror", "girl doing makeup bedroom mirror"),
    ("park_walk", "path", None, "pic", "life/park_path_t0",
     "a path round a pond, ducks, a man on a bench with a newspaper", "park pond path bench"),
    ("park_rest", "bench", None, "pic", "life/park_bench_rest_t0",
     "a girl resting on a park bench by a pond", "girl resting park bench pond"),
    ("park_selfie", "photo", None, "pic", "look/park_selfie_t3",
     "a girl taking selfies by a willow, an older man on a bench watching", "girl taking selfie park man watching"),
    ("garage_laundry", "washer", None, "pic", "life/garage_washer_t0",
     "an old front-loading washer in a cluttered garage, a laundry basket on the floor", "old washing machine garage basket"),
    ("garden_washing", "line", None, "pic", "life/washing_line_t0",
     "a washing line in a back garden: jeans, towels, underwear pegged at the end", "washing line back garden underwear"),
    ("corner_shop_list", "till", None, "pic", "life/corner_shop_till_t0",
     "a corner-shop till: bread, milk, eggs, a bottle of wine, a bored clerk", "corner shop till groceries clerk"),
    ("living_film", "film", None, "pic", "life/living_film_t0",
     "a girl under a blanket on a couch in the dark, a film's glow on her face", "girl blanket couch watching movie dark"),
    # ── C · people: top of the person's screen, rotating ──
    ("hub_ryan_room", "room", None, "pic", "people/ryan_room_t0",
     "a fit young man of 22 on his bed, headphones round his neck, phone in hand", "young man on bed headphones phone"),
    ("hub_ryan_kitchen", "table", None, "pic", "people/ryan_table_t0",
     "a fit young man of 22 at a dinner table in a gym shirt, a full plate", "young man eating dinner gym shirt"),
    ("hub_ryan_living_room", "couch", None, "pic", "people/ryan_couch_t0",
     "a young man of 22 sprawled on a couch with a game controller, TV glow, chips on his chest", "guy on couch playing video games"),
    ("hub_laura_kitchen", "kitchen", None, "pic", "people/laura_kitchen_t0",
     "a woman of 41 in her kitchen, at the counter", "woman in her forties home kitchen counter"),
    ("hub_laura_living_room", "dark", None, "pic", "people/laura_waiting_t0",
     "a woman of 41 on a dark couch in a robe, knees up, a glass of wine", "woman robe dark couch glass of wine"),
    ("hub_laura_bedroom", "mirror", None, "pic", "people/laura_mirror_t0",
     "a woman of 41 in her bedroom", "woman in her forties bedroom"),
    ("hub_laura_bathroom", "door", None, "pic", "look/laura_shower_door_t3",
     "a bathroom door stuck a few inches open, steam rolling out, a shower running", "bathroom door ajar steam shower running"),
    ("hub_mark_kitchen", "hub", None, "pic", "people/mark_cooking_t0",
     "a heavy-set man of 46 in a home kitchen", "middle aged heavy man in kitchen"),
    ("hub_mark_garage", "hub", None, "pic", "people/mark_bench_t0",
     "a heavy-set man of 46 at a garage workbench with a radio and an engine part", "man garage workbench radio"),
    ("hub_tom_cafe", "counter", None, "pic", "people/tom_counter_t0",
     "a café manager of 31 behind the counter, a cloth over his shoulder", "young cafe manager behind counter cloth shoulder"),
    ("hub_gary_booth", "booth", None, "pic", "people/gary_booth_t0",
     "an older man in a café booth with a folded newspaper and a pot of tea", "old man cafe booth newspaper tea"),
    ("hub_nadia_canteen", "nadia", None, "pic", "people/nadia_lunch_t0",
     "a sharp young woman of 20 at a canteen table with a salad and a textbook", "college girl lunch salad textbook"),
    ("hub_nadia_library", "nadia", None, "pic", "people/nadia_library_t0",
     "a young woman of 20 at a library table, headphones round her neck", "college girl library headphones"),
    ("hub_nadia_lecture", "nadia", None, "pic", "people/nadia_lecture_t0",
     "a young woman of 20 in a lecture seat, pen moving", "college girl taking notes lecture"),
    ("hub_hale_class", "hub", None, "pic", "people/hale_lectern_t0",
     "a professor in his late thirties squaring his notes at a lectern", "professor at lectern notes"),
    ("hub_ta_class", "hub", None, "pic", "people/ta_handouts_t0",
     "a shy young woman TA dropping a stack of handouts at the front of a hall", "shy teaching assistant handouts lecture hall"),
    ("hub_business_class", "hub", None, "pic", "people/business_board_t0",
     "a gray-suited lecturer in his fifties writing headings on a board", "older lecturer writing on board"),
    ("hub_art_class", "hub", None, "pic", "people/art_easels_t0",
     "a woman in her forties with charcoal on her hands, walking between easels", "art teacher between easels charcoal"),
    ("hub_dean_office", "hub", None, "pic", "people/dean_desk_t0",
     "a man of 55 at a big desk in a dean's office, not looking up", "dean behind desk office"),
    # ── D · one-time steps ──
    ("meet_bio", "first", None, "pic", "scenes/meet_bio_t0.jpg",
     "a shy young woman TA in a lab coat and big earrings, blushing at the front of a lecture hall", "teaching assistant lab coat blushing"),
    ("meet_business", "first", None, "pic", "scenes/meet_business_t0.jpg",
     "a gray lecturer in his fifties with a register in a gray lecture room", "strict lecturer register gray room"),
    ("college_dean_office", "wait", None, "pic", "scenes/dean_office_first_t0.jpg",
     "a dean writing at his desk, a girl standing in front of it, not asked to sit", "dean desk student standing"),
    ("cafe_gary_meet", "booth", "his eyes drop to your ass and follow it", "pic", "look/gary_first_look_t3.jpg",
     "an older man in a café booth lowering his newspaper to watch a waitress walk past", "old man newspaper watching waitress"),
    ("debt_offer", "letters", None, "pic", "scenes/debt_letters_t0.jpg",
     "final-notice letters fanned across a kitchen table, a man's hands flat beside them", "final notice letters kitchen table"),
]


def _block(kind, name, desc, queries):
    pool = "." not in name.rsplit("/", 1)[-1]
    if kind == "clip":
        return VID(desc, *queries, pool_dir=name) if pool else VID(desc, *queries, file=name)
    return IMG(None if pool else name, desc, *queries, pool_dir=name if pool else None)


def _finds(blocks, text, path=()):
    """Every (path) to a paragraph containing `text`; path = ((list, index), ...) from the node down."""
    out = []
    for i, b in enumerate(blocks):
        if b.get("type") == "paragraph" and text in (b.get("content") or ""):
            out.append(path + ((blocks, i),))
        if b.get("blocks"):
            out += _finds(b["blocks"], text, path + ((blocks, i),))
    return out


def _past_chain(blocks, i):
    while i + 1 < len(blocks) and blocks[i + 1].get("type") == "group" and blocks[i].get("type") == "group":
        i += 1
    return i


def apply(canvas):
    rows = [r for r in ROWS if r[0] == canvas["id"]]
    for cid, nid, anchor, kind, name, desc, *queries in rows:
        node = next((n for n in canvas["nodes"] if n["id"] == nid), None)
        assert node is not None, f"media.py: {cid} has no node {nid!r}"
        blk = _block(kind, name, desc, queries)
        if anchor is None:
            node["blocks"].insert(0, blk)
            continue
        hits = _finds(node["blocks"], anchor)
        assert hits, f"media.py: {cid}.{nid}: no paragraph with {anchor!r}"
        if len(hits) == 1:
            path = hits[0]
            # climb out of any block_pool: a block put in a pool would become one of its entries
            k = len(path) - 1
            while k > 0 and path[k - 1][0][path[k - 1][1]].get("type") == "block_pool":
                k -= 1
            lst, i = path[k]
            lst.insert(_past_chain(lst, i) + 1, blk)
        else:
            top = max(h[0][1] for h in hits)
            node["blocks"].insert(_past_chain(node["blocks"], top) + 1, blk)
    return canvas
