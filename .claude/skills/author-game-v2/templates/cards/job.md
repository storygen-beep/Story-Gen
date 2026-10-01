# Card — Job (a system)

> **A worked card, not a template.** Take the shape, leave the furniture. Every line cites a traced game:
> round 9b, `round9b/cards/job.md`, `round9b/traces/job_cot_river_rat.md` and `round9b/traces/job_cw_waitress.md`.
> Model: **Course of Temptation (CoT), the River Rat bar**; contrast: **Cupid's Way (CW), the waitress job**. Fill
> your own card on `templates/sheets/system.md`; record it in `board.systems[]`.

| field | the model (CoT River Rat) | cite |
|---|---|---|
| place and hours | a bar in town, open 12:00–02:00; she walks in and asks for the job (10 min) | [RiverRat]; [EventRiverRatAskJob] |
| cost | Rest −20 per clock-in; 5 min per table action, a round at most 60 min; refused if a need is at 0, the dress code is wrong, she is too uncovered, or cum is visible | [RiverRat]; [RiverRatNotDresscode]; [RiverRatTooUncovered]; [RiverRatCumCovered] |
| one ladder or two | **two meters that touch only through the shift's events**: rank picks the event pool and the wage; flirtiness picks which events in that pool can fire, and those events can add tips. The one-ladder default is CW: one counter, `$restaurant_event` 0→16, is both pay and lewd | round 9b `traces/job_cot_river_rat.md`; [serve1] |
| pay ladder | 5 ranks: trainee, junior, senior server, bartender, manager. Tipped $2/3/4/7/9 an hour, floor $7/9/11/15/18; tables 2/3/4, then the bar. Gate = performance 100/250/500/750 **and** 7/14/14/14 days worked (49 to manager). Tips per table = clamp(3 × people, 5, 10) × mood × attitude × clientele, then ×1–1.33 | [RiverRatPromotion]; round 9b `traces/job_cot_river_rat.md` |
| lewd ladder | flirtiness, +25 a day at most, **15 rungs** (2→40 shift days at the cap): remove bra (50) · sell underwear (100) · lap, grope (125) · hard grope, Sporty uniform (150) · flash for a tip (200) · remove top (250) · dance tables (300) · Sexy uniform (400) · under-table service, oral (500) · flash for cash at the bar (600) · Topless uniform, corner sex, bukkake (800) · table gang (1000) | round 9b `traces/job_cot_river_rat.md` |
| people | the named owner (the door; swaps the uniform at flirt 150/400/800), the bartender, coworkers, and **every town NPC as a customer**; a table's mood reads her relationship to its star (partner, friend, enemy, flirt) | [EventRiverRatOwnerFirstTimeTopless]; round 9b `traces/job_cot_river_rat.md` |
| pool, daily | server pool **46 events (40 distinct), 14 open on day 1, 23 flirt-gated**; bartender 20; between-round posts 20 and 36; clock-in 9. A seen event drops to 1/10 weight; the seen list resets each game day | round 9b `cards/job.md` |
| memory | rank list, performance 0–1000, flirt and professionalism, days worked since promotion, shift totals, owned upgrades | round 9b `traces/job_cot_river_rat.md` |
| growth | climbs only, no decay; flirtiness can fall with professional choices | round 9b `cards/job.md` |
| sink and deadline | the weekly bill; as manager a daily fund of $300–500 buys 42 upgrades in 7 categories ($0–2,600, 3 days each) | [WeeklyDebtPayment]; [RiverRatUpgrades] |
| feeds | money; what she wears (uniforms); people (a stranger at the bar can become a date) | round 9b `traces/job_cot_river_rat.md` |
| reads | her clothes (15 of 46 server events), her needs, her relationship with each table's star | round 9b `cards/job.md` |
| link into the hook | uniforms, flash, grope and under-table events; the owner's topless chain; strangers who become dates | [EventRiverRatOwnerFirstTimeTopless] |
| leads to | the owner; bartender rank; manager upgrades | [RiverRatPromotion]; [RiverRatUpgrades] |

## Measured floors (directions, never gates)
- 3 or more pay rungs (River Rat 5, QuickieBurger 4, CW internship 3). Round 9b `cards/job.md`.
- 6 or more lewd steps (CW waitress 6 over 17 counter values; River Rat 15). [serve1]; round 9b `cards/job.md`.
- About 1.5 new events per lewd rung, and 14 or more open at rung 0. Round 9b `cards/job.md`.
- Show both meters after every shift, with a line on how far the promotion is. [RiverRatPunchOut]
- A ladder needs a top rung that feeds back into money: CW's waitress ends at stage 15 in unpaid repeat sex. [waitress11]

## What players say
- *"The River Rat progression is too grindy."* (CoT, mopoga#118542); *"The promotions seem to come in increments of
  7 shifts worked… there's no cheat for"* (CoT, mopoga#117165). CoT later added pace sliders, 0.5–4×
  (`cot_70_update_vars.js:502`).
- Job complaints across the field: low pay 7, grind 6, repetitive 5. They are about pace, not about working.

## Our engine today (round 9b §6)
- No job primitive: a shift is a scheduled canvas with `costs` (`template_import.py:769`) and
  `max_triggers_per_day` (`template_import.py:762`). Rank and performance are hand-built traits and flags.
- Phone `fast_jobs` keep one global XP for all jobs, no per-job rank (`v2.py:3223`).
- Pay can be worked out from one player trait (`{type = "trait", trait, mult, add, min, max}`, `setup.resolveEffectValue` (`v2.py:6783`)), on a
  choice effect or a fast job's `income`.
