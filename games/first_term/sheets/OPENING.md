# [READY] Opening — First Term

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08 from SP1, SP7, IDEA §3–4 and the place and person sheets.
> A screen walk: one row per screen, in order, with the button quoted. The lines in quotes are labels and
> the people's key lines; the prose is written at the build.

| row | answer |
|---|---|
| shape | staged open: one person at a time, each on screen and speaking |
| starting clock | Monday, 07:00: her first morning of college |
| boot | her room: she wakes, then the shower |
| capstone | Ryan A 1 in the hall, running into breakfast in the kitchen |
| the handover lands at | `home_kitchen`, Monday 07:50: Laura is there until 08:00 |
| the first open door | the first class, Psychology, 08:30, in the lecture hall |
| a returning player | "Skip the opening" on screen 2 sets every flag and goes to screen 9 |

## The screen walk

| # | screen | who speaks | what she learns | button (quoted) | clock after |
|---|---|---|---|---|---|
| 0 | the engine's title card and age gate | nobody | everyone here is 18 or older | "✓ I am 18 or older - Enter Game" | 07:00 |
| 1 | the engine's character screen: two text boxes | nobody | her name and what Ryan calls her (defaults on the name screen) | "Continue to Game" | 07:00 |
| 2 | boot · her room: who she is, the problem | her own voice | 18, first day of college, no job, no money | "Get up." · "Skip the opening" | 07:03 |
| 3 | boot · her room: the problem, said | her own voice | from Sunday she pays Mark $75, every week | "Grab a towel." | 07:05 |
| 4 | boot · the shower | her own voice | the one bathroom, the thin walls, the clock | "Open the door." | 07:15 |
| 5 | capstone · the hall: Ryan waiting his turn | Ryan · her | he looks, and doesn't move | four, below | 07:18 |
| 6 | capstone · the reaction to her choice | Ryan · Laura up the stairs | what her answer did | "Get dressed." | 07:30 |
| 7 | capstone · breakfast: Laura, Mark leaving for work | Laura · Mark · her | the rent is real: Sunday, the table, $75 | three, below | 07:40 |
| 8 | capstone · Laura's rule | Laura · Ryan | Ryan showers first from now on | "Grab your bag." | 07:45 |
| 9 | capstone · the card and the plain lines | the game's voice | where to go, and how the game works | "Keep hygiene on" · "Turn hygiene off" | 07:50 |
| — | **THE FUNNEL ENDS.** The kitchen, Monday 07:50 | Laura, her hub | | | |

**Screen 5, her choices** (Good Girl only; she starts at stage 1):

| button | the reaction line | sets |
|---|---|---|
| "Run to your room." | her face hot; his eyes follow her down the hall | Ryan's Want add +10 · `ryan_hall_seen` |
| "Knock next time." (parked) | *"Yeah. Sorry."* His next step waits three days | `ryan_hall_knock` |
| "Stop and talk." | he's the only one who asks about her first day | Ryan's Warmth add +5 (guess) · `ryan_hall_talked` |
| "Don't ever look at me like that. (ends his path)" | he goes white, and steps back | `ryan_01_hall_first_morning_closed` |

**Screen 7, the start choice**, asked by Laura over coffee: *"So. What do you want from college, sweetheart?"*

| button | the reaction line | sets |
|---|---|---|
| "Good grades." | Laura beams. Mark snorts into his coffee. | `college_for_grades` |
| "Fun." | Laura laughs. Mark: *"Fun's not free. Seventy-five."* | `college_for_fun` |
| "Freedom." | Laura goes quiet. Mark looks at her a beat too long. | `college_for_freedom` |

The breakfast scene sets `rent_starts`. The rent is armed here and charged only from Sunday 00:00.

## What happens on each screen

| # | the job of the screen | the line it carries |
|---|---|---|
| 2 | setup: who she is, plainly, in her voice | first day, still at home, never had a job or a lock |
| 3 | the problem | *"Seventy-five a week. With what?"* |
| 4 | her body, her room, the house | the bathroom door, Ryan's voice through it |
| 5 | the first person, the conflict, the first choice | *"First day of college, huh. Look at you."* |
| 5 | the temptation | his eyes down her legs and back up; her face hot |
| 6 | who notices | Laura: *"@player, you'll be late on your first day!"* |
| 7 | the second person, the pressure | Mark: *"Sunday. Kitchen table. All of it."* |
| 8 | the house's rule, and a hook | *"Ryan, you shower first from now on."* |
| 9 | the objective, the plain lines, the hook | below |

**Screen 9, the card** (Story Goals, with goal steps):

| goal | when it's done |
|---|---|
| Go to your first class: Psychology, 08:30 | `hale_01_first_lecture` played |
| Ask for a job at the café | `cafe_job` set |
| Have $75 by Sunday | `money` 75 or more |

**Screen 9, the plain lines** (the game's own voice, not a scene): *You need $75 by Sunday. The café near
campus is hiring. Classes are three a day; skipping one costs your grade. People are in different places at
different hours. What you wear changes how they look at you. Hygiene is on: shower to keep it up.*

**Screen 9, the hook:** class at 08:30, the café is hiring, Mark's $75, and Ryan's door shut behind her.

## Who is met, and where

| person | met on | the flag that meets them |
|---|---|---|
| Ryan | screen 5, the hall | forced opening: met by playing |
| Laura | screens 6–8, the stairs and the kitchen | forced opening: met by playing |
| Mark | screen 7, the kitchen, leaving for work | forced opening: met by playing |
| Hale and Nadia | the first class, 08:30, after the handover | Hale B 1 (his step 1) |
| everyone else | their own meeting, later | their met flag hides their rows and cards |

Mark's schedule has him at work on weekday mornings. In the opening he is on his way out at 07:40: a forced
scene, not a row (LO, 2026-10-08).

## Every live system gets a beat (F4)

| system | its beat in the opening | or the sidebar row |
|---|---|---|
| money and rent | Mark at breakfast; `rent_starts` set | money $0 |
| college | the card: Psychology, 08:30 | — |
| the café job | the card and the plain line: the café is hiring | — |
| wardrobe | the towel in the hall; Ryan notices it; "Get dressed." | the engine's "Change Clothes" link in her room |
| energy, hygiene | the shower; the plain line; the hygiene choice | energy, hygiene |
| her two meters | — | her two stages, at the bottom |
| parties | not in the opening: Zoe tells her on campus in week 1 | — |
| the park | not in the opening: its own place, open all day | — |
| the phone | Mark's rent text, caused by `rent_starts`, arrives Saturday | — |

## The early first explicit beat

The park couple (LO, 2026-10-08): she walks into a couple in the bushes, sees them, and runs. Strangers,
an accident, stage 1. **Not in the funnel:** it is reachable from the handover on day 1, when the park
opens at 07:00. No step, no main man, no paid route.

## Rows a gate needs

| row | gate |
|---|---|
| the kitchen at 07:50, Laura there until 08:00 | the opening opens a door |
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
| the hygiene choice on screen 9 | LO, 2026-10-08 |
| a skip on screen 2 | `the-first-hour.md` F1c |
| Mark leaving at 07:40, the opening only | LO, 2026-10-08 |
| the clock after each screen | guess |
| the start-choice readers | LO, 2026-10-08 (flag names a guess) |
| the park couple, not in the funnel | LO, 2026-10-08 · `the-arc.md` A15 |
