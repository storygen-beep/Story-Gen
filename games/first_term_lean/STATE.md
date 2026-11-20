# STATE: First Term (first_term_lean)

## Built

- Game plan approved 2026-11-20 (`PLAN.md`, NOTES decisions).
- the frame (P01): Monday week 1, 07:00; sidebar shows Energy bar, Money, Corruption and Exhibitionism words; nothing moves them. The start is P13's opening (ft_start removed).
- Home (P02): an area, the hall its hub, six rooms off it with "Leave <room>"; second person; 7 room pictures wired, no files. 
- Neighbourhood (P03): her street the hub; The House Next Door, Corner Shop, Park, Gym (with hours and closed lines), Home. The hall's "Exit Home" goes to the street. Nothing to do yet at any of them (P33).
- Campus (P04): the quad the hub; Lecture Hall (Women's Bathroom off it), Library, Cafeteria, Faculty Offices, Theatre, with hours. Only way in or out: bus ($2, 20 min) or walk (10 energy, 45 min), from her street and the quad. Played live headless 2026-11-20: walk costs and times right, bus dimmed at $0, closed places greyed.
- Near campus (P05): Café (7am–9pm, 5 min from the quad) and Zoe's Apartment (10 min, hidden until `zoe_place_known`, which P20 must set). Played live 2026-11-20.
- Daily loop (P06): Sleep (8 hours, 9pm–3am, energy to 100) in Your Bedroom; Eat something (20 min, +15, three a day) in the Kitchen; Shower (15 min, +5) in the Bathroom. Played live 2026-11-20: times, energy and greyed lines right; sleeping at 23:00 wakes Tuesday 7:00.
- The opening (P13): name screen (name, what Ryan calls you), her first screen and start choice (start_grades/fun/freedom), Ryan in the hall with four answers (met_ryan, ryan_hall_*), Mom's voice, hand-over to the Kitchen at 7:26. Ryan on the People page with Want/Warmth words. All four answers played live 2026-11-20.

## Release 1: the skeleton

Out of scope: any step past a person's first meeting; meters moving (shown only); sex scenes; parties;
goals 2 and 3 (named as next on goal 1's card, no flags); Dean Sterling's meeting (behind Brooke's
report, release 5; his office exists, door closed); Mark's friends; Zoe staying over and Jake at the door (release 2, LO's pick A); short arcs for named faces;
any media search.

| piece | what | approved | built | checked | played |
|---|---|---|---|---|---|
| P01 | the frame: her, the clock, energy, money, sidebar meters (hers and each person's, shown) | 2026-11-20 | 2026-11-20 | 2026-11-20 | |
| P02 | Home: the seven rooms, what each is for, who's home | 2026-11-20 | 2026-11-20 | 2026-11-20 | |
| P03 | Neighbourhood: street, the house next door, shop, park, gym (bus and walk moved to P04) | 2026-11-20 | 2026-11-20 | 2026-11-20 | |
| P04 | Campus: quad, lecture hall, library, cafeteria, offices, theatre, bathroom, dean's door; the bus ($2, 20 min) and the walk (45 min, energy) from her street | 2026-11-20 | 2026-11-20 | 2026-11-20 | |
| P05 | Near campus: the café, Zoe's apartment | 2026-11-20 | 2026-11-20 | 2026-11-20 | |
| P06 | the daily loop: sleep, wake, eat, wash; the day moves | 2026-11-20 | 2026-11-20 | 2026-11-20 | |
| P13 | the opening: name screen, first morning, start choice, Ryan in the hall | 2026-11-20 | 2026-11-20 | 2026-11-20 | |
| P33 | things to do in the neighbourhood: a snack at the shop, a run in the park, a workout at the gym; each costs time and energy, the shop money | | | | |
| P07 | clothes: her wardrobe, Laura's wardrobe to borrow from | | | | |
| P08 | the phone: contacts as she meets people, texts | | | | |
| P09 | college: four courses on a timetable, attending, grades shown | | | | |
| P10 | the café job: shifts, pay, tips | | | | |
| P11 | Sunday rent: the rent page, $75, Mark at the table. Short in release 1: Mark takes what she has, the rest is owed and shows on the rent page, and he says it waits a week; play goes on (his real decision is release 2) | | | | |
| P12 | goal 1's quest card: pay her own way | | | | |
| P14 | breakfast, day one: Laura and Mark | | | | |
| P15 | day one lectures: Hale and Nadia (psychology), Pratt (statistics); split in two if the card won't fit one screen | | | | |
| P16 | her first English class: Prof. Walsh teaches it, then asks to see her after, as her advisor | | | | |
| P17 | Mr. Cross, first drama class | | | | |
| P18 | Ms. Ivy Holt, the library | | | | |
| P19 | Rosa Diaz, the cafeteria | | | | |
| P20 | Zoe on the quad, week one | | | | |
| P21 | Tom hires her; Chris on her first shift | | | | |
| P22 | Frank and Danny, the corner shop | | | | |
| P23 | Marco, the gym | | | | |
| P24 | Mr. Vance, her first Sunday | | | | |
| P25 | Jake on the quad, week two | | | | |
| P26 | Brooke, week two | | | | |
| P27 | Sam, at Zoe's apartment; the card says what opens Zoe's door in release 1, or meets Sam another way; must pass reach.py | | | | |
| P32 | schedules: one week table per person, shown one area at a time (home; campus; neighbourhood and café; then Zoe, Jake, Brooke, Sam), on the approved hours, with rough hours a week she can reach each |  | | | |
| P28 | everyday at home: who's in which room, a short line pool each | | | | |
| P29 | everyday in the neighbourhood: the faces at their places, the crowds and the noticing line only; no follow-up (tells Laura, tells Mark) while meters are still, and the card says so (truth rule) | | | | |
| P30 | everyday on campus: the same, noticing line only (no "calls Laura") | | | | |
| P31 | everyday near campus: the same, noticing line only | | | | |

## Open

- On the portal since 2026-11-20 as "First Term (Lean)", release form; rebuild output/ with `build.py --release` when LO wants the phone copy refreshed.

- P14 must take over the opening's hand-over (now to the Kitchen) and meet Laura and Mark on screen; it carries "Ryan, you shower first from now on" (P13 out of scope).
- P32 gives Ryan a schedule; until then the People page says "Away" (P13 ruling).
- P20 must set `zoe_place_known` (from P05), so P27 can reach Zoe's.
- Piece list approved 2026-11-20, with LO's three changes (NOTES).

Next step: play — LO plays the start (P01–P06, P13), then piece — P33 (things to do in the neighbourhood)
