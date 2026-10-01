# Card — Gym and body (a system)

> **A worked card, not a template.** Take the shape, leave the furniture. Every line cites a traced game:
> round 9b, `round9b/cards/gym_body.md` and `round9b/traces/gym_body.md`. Two models, because the name covers two
> things: **In Her Own Hands (IHOH)** for a body number that pays, and **Course of Temptation (CoT)** for a gym and a
> sports team as a place with people. Fill your own card on `templates/sheets/system.md`; record it in `board.systems[]`.

| field | the model (IHOH body · CoT gym and team) | cite |
|---|---|---|
| place and hours | IHOH: the building gym and the park, any hour. CoT: the campus gym 6–22; team practice Wed 9–11 and Fri 12–15 (5 h a week) | [AptGymBase]; [BlodgettGymInterior]; `cot_31_database_school.js:184` |
| cost | IHOH: 1 h, −40 of 150 energy, needs leggings or yoga pants and 40+ energy. CoT: 20 min, Rest −30/−40, Hygiene −40/−50, a Physical skill check 3/4/6 | [GymWorkOut]; [BlodgettGymInterior] |
| one ladder or two | **two that touch through the place**: the body number is the pay ladder (IHOH); the lewd ladder lives in the gym's events and the team (CoT). In none of the four games is it the same ladder | round 9b `cards/gym_body.md` |
| pay ladder | IHOH: tips = random(10, hours × 10 + 2 × (beauty + fitness)), up to +100 at 25/25; cam viewers + random(fit/2, fit) + random(beauty/2, beauty). CoT: a team win takes 20% off the weekly bill (33.3% with a high GPA) | [DinerWorkEnd]; [Cam Widgets]; [WeeklyDebtPayment] |
| lewd ladder | CoT event pools: gym 36 (yoga 6, cardio 8, weights 9; swim 13), practice 69, leaving practice 13, games 55; an all-naked swim practice; a team hookup counter on 2 hint cards and a pledge task. IHOH: roommate workouts (5 of 7 yoga passages). Acts per rung: not in the model | [SportsPractice]; `cot_37_database_storyhints.js:140` |
| people | IHOH: roommate Shaun's gym hours. CoT: 5 teams (football 22, swimming 10, cheer 12, esports 8, mascot) with a coach and a posted roster | [AptGymBase]; `cot_31_database_school.js:2203` |
| pool, daily | IHOH: the same click, no event pool. CoT: 6–13 events per click, about half "uneventful"; 10–15 practice and 8–16 game events per team | round 9b `cards/gym_body.md` |
| memory | IHOH: the bonus value and the last day trained. CoT: muscle and plumpness 0–1000, practice counts, game results, the roster | [PassageFooter]; `cot_68_time.js:1029` |
| growth | IHOH: +5 a gym hour, +4 a jog, +3 yoga; cap 25; **−1 a day** unless she trained. CoT: at most +10 a day, about −3.07 a day idle; one body band takes 25 days up, about 81 down | [GymWorkOut]; [ParkJog]; [PassageFooter] |
| sink and deadline | the decay is the deadline (IHOH upkeep); CoT's team pays into the weekly bill | [PassageFooter]; [WeeklyDebtPayment] |
| feeds | IHOH: money (tips, cam viewers), the sidebar. CoT: the bill, Physical skill | [DinerWorkEnd]; [StoryCaption] |
| reads | her clothes (workout wear), energy or Rest and Hygiene | [AptGymBase]; [BlodgettGymInterior] |
| link into the hook | CoT's team: people she practises with, a hookup counter, naked swim practice, a win that pays. Weakest: CoT's body shape, which for a female lead is mostly a word | [SportsPractice]; `cot_39_entity.js:3528` |
| leads to | team sign-up; teammates; IHOH's roommate at the gym | [SportsSignup]; [AptGymBase] |

## Measured floors (directions, never gates)
- A cap of 25–40 (IHOH 25, CW 40) and a gain of 1–5 a session. Round 9b `cards/gym_body.md`.
- A decay so it must be kept (IHOH −1 a day), or permanent ranks (SD, CW). Round 9b `cards/gym_body.md`.
- **At least one money reader** (tips, viewers, a bill cut). [DinerWorkEnd]; [WeeklyDebtPayment]
- First payoff within a few sessions: SD rank 1 in about 3, IHOH cap in 5 gym hours. [TraitsProgress]; [GymWorkOut]
- Show the change on her: a number nobody reads is a system with no output. Round 9b `cards/gym_body.md`.

## What players say
- *"Shaun is never at the gym anymore, even at the times he was supposed to be in the last updates"* (IHOH,
  mopoga#88782). When the gym's value is a person's schedule, one schedule bug empties it.
- *"A cheeseburger + no exercise = a huge ASS. WHERE IS IT???"* (CoT, mopoga#221114): players want the change seen.
- Grind is rare here: 2 of 242 units name the gym or body.

## Our engine today (round 9b §6)
- Partial: a gym membership is a pass (`template_import.py:998`, `pass` condition `v2.py:5176`); the body number
  is a trait with `trait_decay` (applied at `v2.py:6858`). No body-shape primitive.
- Tips from the body are a stat-based value on the tip effect (`{type = "trait"}`, `setup.resolveEffectValue` (`v2.py:7159`)).
