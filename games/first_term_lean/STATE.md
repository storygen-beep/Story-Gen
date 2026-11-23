# STATE: First Term (first_term_lean)

## Built

- Game plan approved 2026-11-20 (`PLAN.md`, NOTES decisions).
- the frame (P01): Monday week 1, 07:00; sidebar shows Energy bar, Money, Corruption and Exhibitionism words; nothing moves them. The start is P13's opening (ft_start removed).
- Home (P02): an area, the hall its hub, six rooms off it with "Leave <room>"; second person; 7 room pictures wired, no files. 
- Neighbourhood (P03): her street the hub; The House Next Door, Corner Shop, Park, Gym (with hours and closed lines), Home. The hall's "Exit Home" goes to the street. Nothing to do yet at any of them (P33).
- Campus (P04): the quad the hub; Lecture Hall (Women's Bathroom off it), Library, Cafeteria, Faculty Offices, Theatre, with hours. Only way in or out: bus ($2, 20 min) or walk (10 energy, 45 min), from her street and the quad. Played live headless 2026-11-20: walk costs and times right, bus dimmed at $0, closed places greyed.
- Near campus (P05): Café (7am–9pm, 5 min from the quad) and Zoe's Apartment (10 min, hidden until `zoe_place_known`, which P20 must set). Played live 2026-11-20.
- Daily loop (P06): Sleep (8 hours, 9pm–3am, energy to 100) in Your Bedroom; Eat something (20 min, +15, three a day) in the Kitchen; Shower (15 min, +5) in the Bathroom. Played live 2026-11-20: times, energy and greyed lines right; sleeping at 23:00 wakes Tuesday 7:00.
- The opening (P13, re-carded 2026-11-21): name screen; her bedroom; Mark says the rent in the kitchen, Laura silent; Laura asks the start choice (start_grades/fun/freedom); the bathroom; Ryan in the hall, eyes drop one second, he catches himself (LO's B), three answers (ryan_hall_past/spoke/waited), no final no; goal 1's card on screen 6 and on the Quests page; hand-over to Laura alone in the Kitchen at 7:38. Laura and Mark on the People page, with weekday morning Kitchen rows. Energy effects clamp at 100 (P06 fixed too). All three paths played headless 2026-11-21.

## Release 1: the skeleton

Piece list updated 2026-11-21 (LO's yeses, NOTES): the opening is one piece (P12 and P14 folded
into P13); P33 grown into body care; P34–P41 added.

Out of scope: any step past a person's first meeting; meters moving (shown only), except the
Sundays-paid-in-a-row counter; Ella having sex. Her sex opens only with a partner, from the start of
that relationship; she has none in release 1. (Seeing sex is in.) Anything at a party past the one
dare and her no; Ella's own party; goals 2 and 3; Dean Sterling's meeting (release 5); Mark's
friends; Zoe staying over and Jake at the door (release 2); short arcs for named faces; any media search.

| piece | what | approved | built | checked | played |
|---|---|---|---|---|---|
| P13 | the opening, re-carded from craft/opening.md as one piece: Mom on screen, breakfast with Laura and Mark, Mark's rent line ($75 every Sunday), goal 1's card, Ryan's look per LO's B, hand-over on a hook; check.py --card, the reader, then LO plays | 2026-11-21 | 2026-11-21 | 2026-11-21 | |
| P02 | Home: re-checked 2026-11-23 (places, clock, voice, media): no "Nothing to do", menus named by piece, pictures of her, none on the hall | 2026-11-23 | 2026-11-23 | 2026-11-23 | |
| P03 | Neighbourhood: re-checked 2026-11-23: hours on signs, no "phone credit", the house next door hidden until met_vance (P24), pictures of her, none on the street; the clothes shop's link comes with P35 | 2026-11-23 | 2026-11-23 | 2026-11-23 | |
| P04 | Campus: re-check | 2026-11-20 | 2026-11-20 | 2026-11-20 | |
| P05 | Near campus: re-checked 2026-11-23: the café's sign, the Help Wanted line until cafe_hired, Zoe's line true when she's out, "Knock on Zoe's door" (P27) | 2026-11-23 | 2026-11-23 | 2026-11-23 | |
| P06 | the daily loop: re-check | 2026-11-20 | 2026-11-20 | 2026-11-20 | |
| P34 | home life: talk to each housemate, Wait, the dishes, meals with the family, lock your door, Watch TV (PLAN 8a) | | | | |
| P33 | body care: Go for a run, Work out ($5), hair and make-up, a snack ($2), a coffee ($3), lunch ($4), sit on the grass (PLAN 8b) | | | | |
| P07 | clothes: her wardrobe and the picker, Laura's wardrobe, Ryan's hoodie, the leave-the-house rule, the run/workout rule, noticing lines (PLAN 8d) | | | | |
| P35 | the clothes shop and Nina: place, stock in four levels, trait and money locks, clothes_layout = room (PLAN 8d) | | | | |
| P09 | college: the timetable, Go to class, Study, drama, practise on the stage, Grades shown, still (PLAN 8f) | | | | |
| P10 | the café job: shifts every day, $22 a shift, behind P21 (PLAN 8f) | | | | |
| P11 | Sunday rent: the rent page, Mark at the table, the short line, the Sundays-paid-in-a-row counter on goal 1's card (PLAN 8c, 8i) | | | | |
| P08 | the phone: chat only, a text after each meeting (PLAN 8e) | | | | |
| P36 | reputation: the meter (still), the Sunday board on the quad, overheard lines at the mirror and the next table (PLAN 8g) | | | | |
| P37 | Zoe's Saturday party: one fixed dare, her no (PLAN 8h) | | | | |
| P32 | schedules: everyone's rows from PLAN 9a–9d; run who_is_where.py |  | | | |
| P38 | walk-ins, home (PLAN 10a), from craft/walk-ins.md | | | | |
| P39 | walk-ins, neighbourhood: at least the park couple (bite to come) | | | | |
| P40 | walk-ins, campus: at least the library back stacks (bite to come) | | | | |
| P41 | walk-ins, near campus: Zoe and Sam, seen (bite to come) | | | | |
| P15 | day-one lectures: Hale and Nadia (psychology), Pratt (statistics); split in two if the card won't fit one screen | | | | |
| P16 | her first English class: Prof. Walsh, then asks to see her after, as her advisor | | | | |
| P17 | Mr. Cross, first drama class | | | | |
| P18 | Ms. Ivy Holt, the library | | | | |
| P19 | Rosa Diaz, the cafeteria | | | | |
| P20 | Zoe on the quad, week one; sets zoe_place_known | | | | |
| P21 | Tom hires her; Chris on her first shift; opens Work a shift | | | | |
| P22 | Frank and Danny, the corner shop | | | | |
| P23 | Marco, the gym | | | | |
| P24 | Mr. Vance, her first Sunday | | | | |
| P25 | Jake on the quad, week two | | | | |
| P26 | Brooke with Kayla and Tess, week two: one cold line | | | | |
| P27 | Sam: she knocks at Zoe's in the afternoon and he opens; must pass reach.py | | | | |
| P28 | everyday at home: who's in which room, a short line pool each | | | | |
| P29 | everyday in the neighbourhood: faces, crowds, the noticing line only (truth rule) | | | | |
| P30 | everyday on campus: the same | | | | |
| P31 | everyday near campus: the same | | | | |

## Open

- On the portal as "First Term (Lean)"; output/ is a dev + debug build of the re-carded opening, pushed to main 2026-11-22 (LO: "rebuild with dev and debug, commit, merge and push").

- Body moments, relayed from LO by the ENI session 2026-11-22 (craft/body-moments.md, read): the P02–P06 re-check also carries, each shown to LO as a card: the opening's shower (5_scenes.toml:93/116/139, "You give yourself five minutes."), a beat on her body and a gif before Ryan's fist; the slipping knot (:164, :241) paid off on her body with a picture, Ryan still looks away (B); "Back in your room, dressed" (:199/221/242) becomes the towel off and the dressing, clothes equipped (C719; needs P07's wardrobe or a piece of it first); P06's daily shower (:546-547), her under the water, pool 4 (LO 2026-11-22); the opening's pictures pool 1 each (LO); one line each for her body on the packed bus (:379) and her noticing Ryan shirtless (:159). No meter moves.
- P32 adds the rows for everyone outside the house; Laura, Mark and Ryan have their week from P13.
- P20 must set `zoe_place_known` (from P05), so P27 can reach Zoe's.
- P24 must set `met_vance` (from P03), on her street with him on his porch; then the house next door opens.
- P04's six campus places still say "Nothing to do here right now."; they go with P04's re-check.
- Piece list approved 2026-11-20, with LO's three changes (NOTES).

Next step: play — LO plays the opening and the re-checked Home, Neighbourhood and Near campus (output_dev/); then piece — P04, P06, P01, P13 re-checked once craft/heat.md and craft/systems.md are in
