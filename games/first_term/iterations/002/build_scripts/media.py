"""Media blocks for release 1 (sheets/media/release1.md, signed by LO 2026-11-12: "Sign it"; DECISIONS 238) and for
the rest of the game (sheets/media/full.md, signed by LO 2026-11-12: "Sign them"; DECISIONS 240).

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
     "a young man in just his shorts blocking a narrow hallway, a girl about to squeeze past him",
     "guy in shorts blocking narrow hallway"),
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
    # ══ The rest of the game (sheets/media/full.md, signed by LO 2026-11-12: "Sign them"; DECISIONS 240) ══
    # ── 1 · sex ──
    ("gym_hit_man", "hand", "You reach back and take his cock in your wet hand", "clip", "sex/gym_man_hand_t5",
     "in a gym shower, a girl with her back to a big man in his forties, stroking his cock under the water",
     "shower handjob from behind", "girl stroking man in shower"),
    ("gym_hit_man", "body", "pushes his cock into your cunt from behind, under the water", "clip", "sex/gym_man_fuck_t5",
     "a man fucking a girl from behind against shower tiles, one of her legs lifted, water running",
     "shower sex from behind leg up", "fucked against shower wall"),
    ("gym_hit_man", "ask", "His cock is half hard", "clip", "sex/gym_man_ask_t4",
     "a big naked man in his forties walking over in an emptying gym shower, half hard", "naked man shower approaching half hard"),
    ("gym_hit_man", "wash", "He soaps your back slowly with both hands", "clip", "sex/gym_man_wash_t4",
     "a man behind a girl in a shower soaping her back, then her tits from behind", "man soaping girl's breasts from behind shower"),
    ("gym_hit_woman", "wash", "She washes your hair first", "clip", "sex/gym_woman_wash_t4",
     "a woman behind a girl in a shower washing her hair, then cupping her soapy tits", "woman washing girl's hair shower soapy breasts"),
    ("gym_hit_woman", "hand", "You rub her clit while she holds onto your shoulders", "clip", "sex/gym_woman_hand_t5",
     "two women in a gym shower, one fingering the other's clit, the other holding her shoulders",
     "lesbian shower fingering", "women shower touching"),
    ("gym_hit_woman", "body", "She eats your pussy with her tongue on your clit", "clip", "sex/gym_woman_lick_t5",
     "a woman on her knees in a shower eating out a girl pressed against the tiles", "lesbian shower pussy licking kneeling"),
    ("gym_hit_couple", "both", "She kneels and licks your pussy while he holds your tits from behind", "clip", "sex/gym_couple_t5",
     "a threesome in a shower: a woman kneeling licking a girl while a man holds her tits from behind, then fucks her",
     "shower threesome mmf", "couple and girl shower sex"),
    ("gym_hit_two_men", "both", "One of them fucks your cunt from behind while you suck the other's cock", "clip", "sex/gym_two_men_t5",
     "a girl in a gym shower fucked from behind while sucking a second man's cock, others watching",
     "shower spitroast", "two men one girl shower"),
    ("gym_hit_two_women", "both", "One of them kisses you and plays with your tits while the other kneels", "clip", "sex/gym_two_women_t5",
     "three women in a shower: one kissing her and playing with her tits, one kneeling licking her pussy", "three girls shower lesbian"),
    ("gym_hit_group", "wash", "Hands everywhere, too many to count", "clip", "sex/gym_group_wash_t5",
     "a girl in a crowded gym shower, many soapy hands on her tits, ass and between her legs", "group shower soaping girl many hands"),
    ("hub_dex_gym", "another", "locker room", "clip", "sex/dex_hub_locker_t5",   # both pool entries say it; the clip goes after the pool
     "a locker room: a girl jerking off a fit trainer of 34 with her hands, the man leaning on the lockers or sitting on the bench",
     "locker room handjob trainer"),
    ("dex_03_another_way", "hand", "his cock comes out thick and heavy, already hard", "clip", "sex/dex_first_hand_t5",
     "a fit man of 34 leaning on lockers with his shorts down, a girl taking his hard cock in her hand", "gym locker room handjob first time"),
    ("ryan_07_kayla_cant_know", "phone", "You keep stroking his cock, faster now", "clip", "sex/ryan_phone_handjob_t5",
     "a girl stroking a young man's cock on his bed while his phone buzzes beside his hip", "handjob on bed phone ringing"),
    ("ryan_two_knocks", "start", "He pulls your clothes off you, quick and rough", "clip", "sex/ryan_knocks_start_t5",
     "a young man of 22 pressing a girl against a bedroom door, kissing her, pulling her clothes off", "making out against door undressing"),
    ("ryan_two_knocks", "no_start", "his cock still hard and pointing at you", "clip", "sex/ryan_knocks_stop_t4",
     "a young man, still hard, watching a girl pull her clothes back on in his bedroom", "guy hard watching girl get dressed"),
    ("walkin_cafe_gary", "g_hand", "His hand comes off the paper and settles on your thigh", "clip", "sex/gary_hand_thigh_t4",
     "an older man on the stool next to a girl at a café counter, his hand settled on her thigh", "old man hand on girl thigh cafe counter"),
    ("walkin_canteen_zoe", "z_stay", "Her hand slides up the inside of your thigh", "clip", "sex/zoe_canteen_thigh_t4",
     "under a canteen table, a girl's hand sliding up another girl's inner thigh", "girl hand up friend's thigh under table"),
    ("walkin_quad_zoe", "qz_hand", "Her hand slides from the outside of your thigh to the inside", "clip", "sex/zoe_quad_thigh_t4",
     "two girls on the grass, one's head in the other's lap, her hand high between the other's thighs", "girl hand between friend's thighs on grass"),
    ("walkin_tub_zoe", "answer", "You're naked in the water up to your tits", "clip", "sex/zoe_tub_naked_t4",
     "two girls naked in a hot tub at night, steam, the water up to their tits", "girls naked hot tub night"),
    ("walkin_couch_zoe", "c_pull", "You pull her down on top of you.", "clip", "sex/zoe_couch_ontop_t4",
     "a girl in a sleep shirt lying on top of another girl on a couch, bare thighs, faces close", "girl lying on top of girl couch"),
    ("walkin_bedroom_zoe", "b_watch", "She turns round so you get all of it", "clip", "sex/zoe_bedroom_undress_t4",
     "a girl changing in her bedroom, topless in her panties, stretching, before pulling a sleep shirt on", "girl topless panties stretching bedroom"),
    ("walkin_kitchen_ryan", "r_push", "Your ass grinds right back against his cock", "clip", "sex/kitchen_ryan_grind_t4",
     "a girl at a kitchen counter pushing her ass back into a young man pressed behind her in boxers", "girl grinding ass against guy kitchen"),
    ("hub_dex_gym", "stretch", "the mat", "clip", "sex/dex_stretch_t4",   # all three pool entries say it; the clip goes after the pool
     "a fit trainer of 34 stretching a girl on a gym mat, his hands on her thighs and ass", "trainer stretching girl hands on thighs"),
    ("dex_02_the_mats", "mats", "His hand is flat on your inner thigh", "clip", "sex/dex_mats_first_t4",
     "on a gym mat, a trainer kneeling between a girl's legs, her leg on his shoulder, his thumb pressing between her legs through her gym clothes",
     "trainer leg on shoulder stretch thumb crotch"),
    ("hub_mark_kitchen", "hl_dinner_tease", "you lick it off while he watches your mouth", "pic", "look/dinner_lick_t3",
     "a girl at a dinner table licking sauce off her thumb, an older man across the table staring at her mouth", "girl licking thumb dinner man staring"),
    # ── 2 · nudity and flashes ──
    ("zoe_02_bra_through_the_sleeve", "sleeve", "nipples", "clip", "sex/zoe_bra_off_t4",   # after every version
     "a girl on a party balcony at night with her bra in her hand, nipples hard, the party behind the glass", "girl took bra off at party balcony"),
    ("zoe_03_hot_tub", "kiss_bare", "You kiss her hard", "clip", "sex/zoe_tub_kiss_t4",
     "two topless girls kissing in a hot tub at night, steam, tits pressed together", "topless girls kissing hot tub night"),
    ("gym_shared_shower", "in", None, "pic", "sex/gym_shower_in_t4",
     "a shared gym shower room, naked men and women under the heads", "coed shower room naked"),
    ("gym_shared_shower", "face", "You turn round and rinse facing the room.", "clip", "sex/gym_shower_face_t4",
     "a naked girl rinsing facing a shared shower room, a man two heads down watching, getting hard", "naked girl shower facing room man watching"),
    ("gym_shared_shower", "slow", "You soap yourself slowly for them", "clip", "sex/gym_shower_soap_t5",
     "a naked girl in a shared shower soaping her tits and between her legs while people watch", "girl soaping herself shower people watching"),
    ("gym_sauna_slip", "slip", "It drops open to your waist.", "clip", "sex/sauna_towel_slip_t4",
     "a girl in a sauna, her towel fallen open to her waist, topless and sweating, two men on the bench below", "sauna towel falls open girl"),
    ("gym_sauna_slip", "let", "both men staring at your nipples", "clip", "sex/sauna_stay_t4",
     "a topless girl sitting still in a sauna, two men staring, one covering his lap with a towel", "topless girl sauna men staring"),
    ("crowd_ask_quad", "bare", "your bare tits are right there", "clip", "sex/flash_quad_top_t4",
     "a girl kneeling on the grass pulling her top up over a guy's face, bare tits", "girl flashing tits on grass"),
    ("crowd_ask_quad", "bare_d", "your bare tits are right there", "clip", "sex/flash_quad_dress_t4",
     "a girl kneeling on the grass pulling the front of her dress down over a guy's face, bare tits", "girl pulls dress down flash grass"),
    ("crowd_ask_gym", "bare", "your bare tits are right there", "clip", "sex/flash_gym_top_t4",
     "a girl in a gym pulling her top up, flashing her bare tits at a guy on a bench", "girl flashing tits at gym"),
    ("crowd_ask_gym", "bare_d", "your bare tits are right there", "clip", "sex/flash_gym_dress_t4",
     "a girl in a gym pulling the front of her dress down, flashing her bare tits at a guy on a bench", "girl flashing gym dress down"),
    ("crowd_ask_canteen", "bare", "your bare tits are right there", "clip", "sex/flash_canteen_top_t4",
     "a girl leaning over a canteen table, pulling her top up to flash her tits at a guy with a tray", "girl flashing tits cafeteria"),
    ("crowd_ask_canteen", "bare_d", "your bare tits are right there", "clip", "sex/flash_canteen_dress_t4",
     "a girl leaning over a canteen table, pulling her dress down to flash her tits at a guy with a tray", "girl flashing cafeteria dress"),
    ("study_notes", "bare", "your bare tits are right there", "clip", "sex/flash_library_top_t4",
     "a girl lifting her top to flash her bare tits at a guy between library shelves", "girl flashing library shelves"),
    ("study_notes", "bare_d", "your bare tits are right there", "clip", "sex/flash_library_dress_t4",
     "a girl pulling her dress down to flash her bare tits at a guy between library shelves", "girl flashing library dress down"),
    ("gossip_ask_quad", "bare", "You pull your top up to your chin", "clip", "sex/flash_quad_steps_t4",
     "a girl on a campus quad, top pulled up to her chin, bare tits, guys on steps", "girl top pulled up campus flash"),
    ("gossip_ask_party", "bare", "in the hallway at Zoe's", "clip", "sex/flash_party_top_t4",
     "a girl in a party hallway holding her top up over her bare tits, two guys stopping dead", "girl flashing party hallway"),
    ("gossip_ask_party", "bare_d", "in the hallway at Zoe's", "clip", "sex/flash_party_dress_t4",
     "a girl in a party hallway holding her dress down under her bare tits, two guys stopping dead", "girl flashing party dress down"),
    ("cafe_acc_spill_bare", "event", "takes the water jug right out of your hand", "clip", "sex/cafe_spill_t4",
     "a waitress soaked by a water jug, her uniform gone see-through on her bare tits", "waitress soaked see through uniform"),
    ("cafe_acc_spill_bare", "let", "You don't run.", "clip", "sex/cafe_spill_stay_t4",
     "a waitress serving a table in a soaked see-through uniform, nipples showing", "waitress wet see through serving"),
    ("cafe_acc_button_bare", "let", "your bare tits swing in the gap", "clip", "sex/cafe_button_open_t4",
     "a waitress pouring coffee, her uniform open, bare tits swinging", "waitress uniform open pouring coffee"),
    ("class_acc_downblouse_bare", "event", "the low-cut top just falls open", "clip", "sex/class_downblouse_bare_t4",
     "a girl bending for a pen in a lecture aisle, her low-cut top falling open, no bra", "girl bending low cut top falls open"),
    ("class_acc_downblouse_bare", "let", "You stay bent over.", "clip", "sex/class_downblouse_stay_t4",
     "a girl staying bent over in a lecture aisle, her bare tits hanging in her open top", "girl bent over top open no bra"),
    ("class_acc_water_bare", "event", "goes straight down your front", "clip", "sex/class_water_bare_t4",
     "a girl in a lecture seat, water spilled down a sheer blouse, see-through on bare tits", "girl water spilled sheer blouse"),
    ("class_acc_water_bare", "let", "You don't cover up.", "clip", "sex/class_water_stay_t4",
     "a girl sitting in a lecture seat in a soaked sheer blouse, nipples showing through", "girl wet see through blouse class"),
    ("walkin_nap_ryan", "r_sho", "give him the whole front of you", "clip", "sex/nap_ryan_show_t4",
     "a girl lying on her bed, rolled onto her back, arms over her head, showing herself to a young man in her room", "girl lying on bed arms up guy watching"),
    ("home_event_ryan_towel", "ev_bold", "Ryan's eyes drop.", "pic", "look/ryan_towel_stop_t3",
     "a girl in a narrow hall not moving aside, a young man in a towel staring at her chest", "guy in towel staring at girl hallway"),
    ("home_event_ryan_towel", "ev_curious", "You walk past him slowly anyway", "pic", "look/ryan_towel_pass_t3",
     "a girl brushing past a young man in a towel in a narrow hallway", "girl squeezing past guy in towel"),
    ("ev_ryan_hall_squeeze", "a1", "Your tits drag across his bare chest", "clip", "sex/hall_squeeze_drag_t4",
     "a girl squeezing past a shirtless young man, her chest dragging across his, his shorts tenting", "girl squeezing past shirtless guy hallway"),
    ("wardrobe_event_stairs", "slower", None, "clip", "sex/stairs_bend_t4",   # top: the whole screen is her staying bent (reader 2026-11-12)
     "a girl bent forward in a narrow house hallway catching her bag strap, her skirt riding up from behind", "girl bent over hallway skirt riding up"),
    ("front_step", "street_sees", "You let your knees fall open on the step", "clip", "sex/front_step_knees_t4",
     "a girl sitting on a front step in a short skirt with her knees open, seen from the sidewalk", "girl sitting step knees apart short skirt"),
    ("garden_sun", "sun_ryan_touch", "You hold the sun lotion up at his window", "clip", "sex/garden_lotion_t4",
     "a girl lying on her front on a garden lounger, a young man kneeling, rubbing lotion on her back", "guy rubbing lotion on girl's back"),
    ("living_couch", "stay_ryan", "Ten minutes later Ryan comes out again", "pic", "look/couch_stay_ryan_t3",
     "a girl on a couch in bra and panties, one knee up, a young man staring at her", "girl underwear couch guy staring"),
    ("walkin_quad_team", "answer", "Six of them, standing at your feet", "clip", "sex/quad_team_upskirt_t4",
     "six college guys standing over a girl lying on the grass, her skirt round her hips", "guys standing over girl on grass skirt"),
    ("walkin_zoebath_cocky", "moment", "to fix your liner", "pic", "look/zoebath_mirror_t3",
     "a girl leaning over a bathroom sink at a party to fix her eyeliner, her ass out", "girl leaning over sink eyeliner party"),
    ("walkin_house_vance", "v_stay", "You lean back against his gatepost", "pic", "look/vance_gatepost_t3",
     "a girl with bare legs leaning back on a gatepost, an older man of 54 in a rocking chair watching", "girl leaning on gate older man porch"),
    ("hub_ryan_room", "towel_no", "His cock is hard under the cotton", "clip", "sex/ryan_room_towel_t4",
     "a young man in his room grinning, hard in his shorts, staring at a girl in a towel", "guy hard in shorts girl in towel"),
    ("hub_ryan_room", "hot1", "Your tits lift.", "pic", "look/ryan_door_stretch_t3",
     "a girl leaning in a young man's bedroom doorway, posing for him while he stares from his room", "girl leaning in bedroom doorway teasing guy"),
    ("hub_ryan_kitchen", "towel_no", "His cock is hard under there", "pic", "look/ryan_table_towel_t3",
     "a young man at a kitchen table pulling his chair in, a girl in a towel leaning back", "guy kitchen table girl in towel"),
    ("hub_ryan_living_room", "towel_no", "His cock is hard in his shorts", "clip", "sex/ryan_couch_towel_t4",
     "a young man on a couch, hard in his shorts, a girl in a towel stepping back over his legs", "guy couch hard girl in towel"),
    ("home_event_ryan_door", "ev_curious", "He's on his bed with his back against the wall", "pic", "look/ryan_door_ajar_watch_t3",
     "through a door gap, a young man on his bed with his back to the wall, looking back", "guy on bed through door gap"),
    # ── 3 · looks and hubs ──
    ("street_seen_crop", "seen", None, "pic", "look/street_crop_t3",
     "a girl walking down a residential street in a crop top, her belly bare, seen from where a man watches", "girl crop top walking street"),
    ("street_seen_bodycon", "seen", None, "pic", "look/street_bodycon_t3",
     "a girl walking down a residential street in a tight bodycon dress, seen from where a man watches", "girl bodycon dress walking street"),
    ("street_seen_micro", "seen", None, "pic", "look/street_micro_t3",
     "a girl walking down a residential street in micro shorts, the bottom of her ass bare", "girl micro shorts walking street"),
    ("street_seen_plunge", "seen", None, "pic", "look/street_plunge_t3",
     "a girl walking down a residential street in a plunge dress cut to her navel, no bra", "girl plunge dress walking street"),
    ("street_seen_split", "seen", None, "pic", "look/street_split_t3",
     "a girl walking down a residential street in a skirt slit to the hip, her bare leg out with every step", "girl high slit skirt walking"),
    ("street_seen_sequin", "seen", None, "pic", "look/street_sequin_t3",
     "a girl walking down a residential street in a short sequin dress", "girl sequin dress walking street"),
    ("street_seen_backless", "seen", None, "pic", "look/street_backless_t3",
     "a girl walking down a residential street in a backless dress, bare from her neck to the base of her spine", "girl backless dress walking street"),
    ("hub_business_office", "hub", "looks up from his marking", "pic", "look/business_office_look_t3",
     "a gray-suited lecturer of 50 at his desk, eyes flicking up from his marking", "lecturer at desk looking up"),
    ("hub_zoe_quad", "grass", None, "pic", "people/zoe_quad_t0",
     "a girl of 19 lying on the grass of a quad with her head in another girl's lap, shoes off", "college girl lying on grass head in lap"),
    ("hub_zoe_bedroom", "bed", None, "pic", "people/zoe_bed_t0",
     "a girl of 19 on her stomach on her bed in a big T-shirt, chin in her hands", "girl lying on bed big t-shirt"),
    ("hub_zoe_party_house", "deck", None, "pic", "look/zoe_tub_deck_t3",
     "a girl of 19 in a hot tub on a back deck at night with two friends, a drink on the rim, steam", "girls hot tub deck night"),
    ("hub_jake_gym", "rack", None, "pic", "people/jake_rack_t0",
     "a college athlete of 20 in a soaked tank top at a squat rack with his team", "college athlete squat rack"),
    ("gym_workout", "floor", None, "pic", "life/gym_floor_t0",
     "a gym floor with a mirror wall: treadmills, weights, mats", "gym floor mirror wall"),
    ("gym_workout", "worked", "You come off the last set dripping", "pic", "look/gym_after_set_t3",
     "a girl coming off her last set, sweaty, in a gym", "sweaty girl after workout gym"),
    ("gym_workout", "looked", "You do the mats last, in the sports bra", "pic", "look/gym_mats_sportsbra_t3",
     "a girl stretching on a gym mat in a sports bra, ass up, guys at the rack watching", "girl stretching sports bra gym"),
    ("gym_workout", "mats", "stretch out in the tiny shorts", "pic", "look/gym_mats_shorts_t3",
     "a girl stretching in tiny shorts in front of a bench, legs wide", "girl stretching tiny shorts gym"),
    # ══ The opening (LO, 2026-11-12: "Add media blocks to the starting scenes"; DECISIONS 241) ══
    # the opening's Ryan morning (ryan_01_hall_first_morning) is hand-written in 2_one_shots.toml; its 6 blocks are there
    ("mark_01_count_it_slowly", "table", "He looks up, and his eyes go", "pic", "look/mark_01_legs_t3.jpg",
     "an older man of 46 at a kitchen table, a rent envelope and a cold coffee in front of him, looking up at a girl's legs",
     "older man kitchen table staring at girl's legs"),
    ("mark_00_the_dryer", "basket", None, "pic", "scenes/mark_00_garage_t0.jpg",
     "a man in his forties at a garage workbench with his back turned, a radio on, a washing machine by the wall",
     "man at garage workbench back turned"),
    ("mark_00_the_dryer", "covered", "You take the towel and hold it over your chest", "pic", "look/hose_covered_t3.jpg",
     "a soaked girl holding a towel over her chest in a garage, an older man bent over his workbench, red ears",
     "soaked girl holding towel garage"),
    ("hale_01_first_lecture", "pen", "You bend down for it, all the way", "clip", "sex/hale_pen_hard_t4.webm",
     "a professor of 39 at a lecture stage, the line of his hard cock against his trousers, a girl coming back up from bending for his pen",
     "professor bulge trousers lecture", "teacher hard student bending"),
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


def check_landed(merged_toml):
    """Every row's block must be in the merged game. apply() only sees the canvases the build scripts emit, so a row
    for a hand-written canvas (2_one_shots.toml, 3_activities.toml) would otherwise be dropped without a word
    (the opening's Ryan morning, 2026-11-12)."""
    text = open(merged_toml).read()
    lost = [r[4] for r in ROWS if f'"{r[4]}"' not in text]
    assert not lost, f"media.py: {len(lost)} row(s) never landed (is the canvas hand-written?): {lost}"
