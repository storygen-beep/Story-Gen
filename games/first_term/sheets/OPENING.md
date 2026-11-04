# [REVIEW] Opening — First Term
> Changed 2026-11-04, LO's answers: she has an old key to her bedroom door and little else that's hers (C); waits for LO's re-sign.

> Changed 2026-11-04 (LO's answer Q10; PICKS 17): Mark has already left for work, so his words are last night's on screen 3 and his RENT envelope sits at breakfast; Ryan is in the shower during breakfast; no final no on Ryan's first meeting; Laura's call names no stairs; the start-choice reactions as built. Waits for LO's re-sign.

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. Every button quoted as built; the funnel ends in the dean's office; Ryan's +10 on "Open the door.".

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08 from SP1, SP7, IDEA §3–4 and the place and person sheets.
> A screen walk: one row per screen, in order, with the button quoted. The lines in quotes are labels and
> the people's key lines; the prose is written at the build.

| row | answer |
|---|---|
| shape | staged open: one person at a time, each on screen and speaking |
| starting clock | Monday, 07:00: her first morning of college |
| boot | her room: she wakes, then the shower |
| capstone | Ryan A 1 in the hall, running into breakfast in the kitchen |
| the handover lands at | the dean's office, Monday 08:05: his one-time welcome |
| the first open door | the dean's "Go to Psychology.": the first class, in the lecture hall |
| a returning player | "Skip the opening" on screen 2 sets every flag, shows one hall screen, then screen 9 |

## The screen walk

| # | screen | who speaks | what she learns | button (quoted) | clock after |
|---|---|---|---|---|---|
| 0 | the engine's title card and age gate | nobody | everyone here is 18 or older | "✓ I am 18 or older - Enter Game" · "✗ I am NOT 18 or older" | 07:00 |
| 1 | the engine's character screen: two text boxes | nobody | her name and what Ryan calls her (defaults on the name screen) | "Continue to Game" | 07:00 |
| 2 | boot · her room: who she is | her own voice | 18, first day of college, no job, no money; she wakes in her sleep shirt | "Get up." · "Skip the opening" | 07:03 |
| 3 | boot · her room: the problem | her own voice · Mark, last night at dinner | from Sunday she pays Mark $75, every week | "Grab a towel." | 07:05 |
| 4 | boot · the shower | her own voice · Ryan through the door | the one bathroom, the thin walls; Ryan's "Some of us have places to be" | "Open the door." (Ryan's Want +10) | 07:15 |
| 5 | capstone · the hall: Ryan waiting his turn | Ryan · her | he looks, and doesn't move | three, below | 07:18 |
| 6 | capstone · the reaction to her choice | Ryan · Laura, calling | what her answer did | "Get dressed." (`ryan_step` 1) | 07:30 |
| 7 | capstone · breakfast: Laura; Mark has already gone to work, his RENT envelope against the sugar bowl | Laura, saying the rent for him | the rent is real: Sunday, the table, $75, Vance behind it | three, below | 07:40 |
| 8 | capstone · Laura's rule | Laura · her | Ryan showers first from now on; he is in the shower down the hall, and his door shuts after | "Grab your bag." | 07:45 |
| 9 | capstone · the card and the plain lines | the game's voice · Laura | where to go, and how the game works | "Go to campus." · "Go to campus. (Turn hygiene off)" | 08:05 |
| — | **THE FUNNEL ENDS.** The dean's office, Monday 08:05: his welcome, the timetable, "Go to Psychology." | the dean | | | |
| skip | the hall, one screen: Ryan's look and line | Ryan | | "Get dressed." | 07:47, then screen 9 |

**Screen 5, her choices** (Good Girl only; she starts at stage 1):

| button | the reaction line | sets |
|---|---|---|
| "Run to your room." | her face hot; his eyes follow her down the hall | `ryan_hall_seen` (his +10 is on "Open the door.", DECISIONS 143) |
| "Knock next time." (parked) | *"Yeah. Sorry."* He looks at the carpet | `ryan_hall_knock` · `ryan_hall_seen` |
| "Stop and talk." | he's the only one who asks about her first day | Ryan's Warmth add +5 · `ryan_hall_talked` · `ryan_hall_seen` |

No final no on this screen (PICKS 17, pass 4): "Knock next time." is the parked no.

**Screen 7, the start choice**, asked by Laura over coffee: *"So. What do you want from college, sweetheart?"*

| button | the reaction line | sets |
|---|---|---|
| "Good grades." | Laura beams like you've handed her something. | `college_for_grades` |
| "Fun." | Laura laughs, then looks at the envelope: *"Fun's not free, sweetheart. Not in this house."* | `college_for_fun` |
| "Freedom." | Laura goes quiet and looks into her coffee, a beat too long. | `college_for_freedom` |

The breakfast scene sets `rent_starts`. The rent is armed here and charged only from Sunday 00:00.

## What happens on each screen

| # | the job of the screen | the line it carries |
|---|---|---|
| 2 | setup: who she is, plainly, in her voice | first day, still at home, never had a job, an old key to her door and little else that's hers |
| 3 | the problem | Mark, last night: *"You're an adult now. Adults pay their way."* · *"Seventy-five a week. With what?"* |
| 4 | her body, her room, the house | the bathroom door, Ryan's voice through it |
| 5 | the first person, the conflict, the first choice | *"First day of college, huh. Look at you."* |
| 5 | the temptation | his eyes down her legs and back up; her face hot |
| 6 | who notices | Laura: *"@player, you'll be late on your first day!"* |
| 7 | the second person, the pressure | Laura, for Mark: *"Seventy-five, Sunday, at this table. Vance doesn't take excuses, so Mark doesn't either."* |
| 8 | the house's rule, and a hook | *"Ryan showers first from now on. Before you're up. I'll tell him."* |
| 9 | the objective, the plain lines, the hook | below |

**Screen 9, the card** (Story Goals, with goal steps):

| goal | when it's done |
|---|---|
| Go to your first class: Psychology, Monday morning, in the lecture hall | `hale_met` set |
| Ask for a job at the café | `cafe_job` set |
| Have $75 by Sunday | `money` 75 or more |

**Screen 9, the plain lines** (as built): *You need $75 by Sunday: the rent is taken then. The café near campus is hiring.
Classes are three a day Monday to Thursday and one on Friday; skipping one costs your grade. People are in
different places at different hours: the People and Schedules pages show where. What you wear changes how
people look at you. Hygiene is on unless you turn it off now: shower to keep it up.*

**Screen 9, the hook:** class at 08:30, the café is hiring, Mark's $75, and Ryan's door, shut, next to hers.

## Who is met, and where

| person | met on | the flag that meets them |
|---|---|---|
| Ryan | screen 5, the hall | forced opening: met by playing |
| Laura | screens 6–8, her call and the kitchen | forced opening: met by playing |
| Mark | screen 3, last night's words in his own voice; gone before breakfast | forced opening: met by playing |
| Hale and Nadia | the first class, 08:30, after the handover | Hale B 1 (his step 1) |
| everyone else | their own meeting, later | their met flag hides their rows and cards |

Mark's schedule has him at work on weekday mornings, and the opening agrees: he has gone before she comes to
breakfast. Ryan is in the shower while she eats (LO, 2026-11-04, Q10).

## Every live system gets a beat (F4)

| system | its beat in the opening | or the sidebar row |
|---|---|---|
| money and rent | Mark's words on screen 3, his envelope at breakfast; `rent_starts` set at breakfast | money $0 |
| college | the card: Psychology, 08:30 | — |
| the café job | the card and the plain line: the café is hiring | — |
| wardrobe | the towel in the hall; Ryan notices it; "Get dressed." | the engine's "Change Clothes" link in her room |
| energy, hygiene | the shower; the plain line; the hygiene choice | energy, hygiene |
| her two meters | — | her two stages, at the bottom |
| parties | not in the opening: Zoe tells her on campus in week 1 | — |
| the park | not in the opening: its own place, open all day, 10 minutes' walk | — |
| life at home | breakfast with Laura on screen 7 is its first beat (it does not set `ate_breakfast`) | — |
| the map and the clock | the plain lines point at the People and Schedules pages | the wait buttons under the clock |
| the phone | Mark's rent text, caused by `rent_starts`, arrives Saturday | — |

## The early first explicit beat

The park couple (LO, 2026-10-08): she walks into a couple in the bushes, sees them, and runs. Strangers,
an accident, stage 1. **Not in the funnel:** it is reachable from the handover on day 1, when the park
opens at 07:00. No step, no main man, no paid route.

## Rows a gate needs

| row | gate |
|---|---|
| the dean's office at 08:05, his one-time welcome | the opening opens a door |
| Ryan, Laura and Mark in the forced opening | every hub is met first |
| Hale met at the 08:30 class, in his window | a meeting fires where they are |
| the card's three goals | the opening arms a card with goals (lint) |
| the start choice read later | the start choice is read |
| her name and nickname printed in lines | what she picks is read |
| `rent_starts` before the first charge | the obligation is charged |

**The start choice's readers** (LO, 2026-10-08): Laura's dinner line, Zoe's line at the first party, and
Hale's office line each read which answer she gave.

## Why — the source of each key choice

| key choice | source |
|---|---|
| a staged open | `the-first-hour.md` F1, F1b |
| Monday 07:00 | SP1 |
| the name screen, two boxes | LO, option 3 (IDEA §3) |
| "what do you want from college?" on day one | WANT §1 |
| Ryan A 1 as the capstone; the bathroom door | IDEA §4 · the ledger's Ryan step 1 |
| Laura's rule at breakfast | IDEA §4 |
| the rent starts after Mark's scene | LO, 2026-10-07 (SYSTEMS, decided item 2) |
| hygiene off as a start choice | LO, chat 2026-10-06 (SYSTEMS §6) |
| the hygiene choice on screen 9, on the "Go to campus." button | LO, 2026-10-08 |
| a skip on screen 2 | `the-first-hour.md` F1c |
| Mark already gone, Ryan in the shower at breakfast | LO, 2026-11-04 (Q10; was Mark leaving at 07:40, LO 2026-10-08) |
| the clock after each screen | as built |
| the start-choice readers | LO, 2026-10-08 (flag names a guess) |
| the park couple, not in the funnel | LO, 2026-10-08 · `the-arc.md` A15 |
| the walk and the wait in the plain lines | LO, 2026-10-08 (picks 1, 2, 6); the build's lines name the People and Schedules pages instead |
