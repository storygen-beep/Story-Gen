# Card — Greek life (a system)

> **A worked card, not a template.** Take the shape, leave the furniture. Every line cites a traced game:
> round 9b, `round9b/cards/unnamed_systems.md` and `round9b/traces/unnamed_systems.md`. The model is
> **Course of Temptation (CoT)**'s houses, pledging, dues, renown and upgrades. Counts use the lead's
> correction in `cards/unnamed_systems.md` (41 tasks / 79 points), not the reader's first script (34 / 64).
> Fill your own card on `templates/sheets/system.md`; record it in `board.systems[]`.
>
> Everyone on campus is 18+, and the game says so.

| field | the model (CoT) | cite |
|---|---|---|
| place and hours | 4 houses on campus; rush week is 7 days from month 4 day 20; pledging opens on day 27; parties run Thursday 18:00 to Friday 03:00 and the host rotates weekly | `cot_43_greekhouses.js:4`; round 9b `traces/unnamed_systems.md` §1 |
| cost | dues $50 a week, +$50 housing if she moves in, charged with the Monday bill; each task costs whatever its act costs | `cot_43_greekhouses.js:9–10`; [WeeklyDebtPayment] |
| one ladder or two | **one**: house renown (0–1000) is the ladder; lewd acts are one source of it, beside sports, class and party wins | round 9b `cards/unnamed_systems.md` |
| pay ladder | no wage: upgrades raise **other** systems' pay (job base pay, non-explicit stream pay, crafts pay) and give free coffee, food and laundry | round 9b `cards/unnamed_systems.md` |
| lewd ladder | the pledge list: **41 tasks worth 79 points, 30 to join**. Clean tasks and pranks reach 26, so joining needs at least 4 lewd points (0 if spanking and wrestling count as clean). Tasks run from a hat on the elk statue to streaking the football field (2) and "fuck the entire football team and/or cheer squad" (5). Parties have 7 activities, among them strip poker, an oral contest and pussy roulette; free-use scenes earn renown | round 9b `cards/unnamed_systems.md` (lead correction); round 9b `traces/unnamed_systems.md` §1 |
| people | house members, the president, the rush chair, rival houses (glitter bomb, kneeling, her number on a stall), the sports teams named in tasks | round 9b `cards/unnamed_systems.md` |
| pool, daily | parties 39 events, house walk 29, underwear raid 11, initiation 4 | round 9b `traces/unnamed_systems.md` §1 |
| memory | `$greekpledge`, `$pledgetasks`, `$pendingpledgetasks`, `$pchouse`, `$greekrenown`, `$greekhouseupgrades` | round 9b `cards/unnamed_systems.md` |
| growth | renown only grows: 17 calls (16 × +25, 1 × +50); renown 50 buys 1 upgrade point, 1000 buys 10; each house has 11 upgrades in 4 tiers (3/3/3/2), so she can't buy all. No decay | [GreekHouseUpgrades]; round 9b `traces/unnamed_systems.md` §1 |
| sink and deadline | **sink:** upgrades and a new home (moving out of the dorm). **deadline:** dues ride the weekly Monday bill | [WeeklyDebtPayment] |
| feeds · reads | feeds the weekly bill, other systems' pay, her housing · reads sports, tattoos, streams, the social feed and sex with teams: a task ticks itself off wherever she does the thing | round 9b `traces/unnamed_systems.md` §1 |
| link into the hook | the pledge list is a cross-system checklist: pledging sends her into every other system | round 9b `cards/unnamed_systems.md` |
| leads to | the Thursday parties, the teams, the rival houses | round 9b `traces/unnamed_systems.md` §1 |

## Measured floors (directions, never gates)
- Over-supply the points: 79 for 30, a 38% bar, so she can skip what she won't do. Round 9b `cards/unnamed_systems.md`.
- A weekly party with at least 7 activities. Round 9b `cards/unnamed_systems.md`.
- Fewer upgrade points (10) than upgrades (11) makes the choice matter. Round 9b `traces/unnamed_systems.md` §1.

## What players say
- *"Am i the only one who is kinda bored of the frat stuff getting updated? I'd prefer … more risk based
  developments, and pregnancy content"* (CoT, mopoga#184809). Of 11 judged units, 9 are CoT.
- *"So many glitches with the pledge tasks"* (CoT, mopoga#155098): self-ticking tasks need testing.

## Our engine today (round 9b §6)
- A weekly party fits schedule rows with `weekdays` (`template_import.py:782`); pledge tasks are flags, renown a trait.
- An upgrade can raise another system's pay: the upgrade raises a trait, and the pay is a stat-based value
  that reads it (`{type = "trait"}`, `setup.resolveEffectValue` (`v2.py:7038`); one trait per value).

## Other systems the round found
- **SD heat:** 0–125, raised by crime, drops 1–16% a day scaled by reputation; at 100 or more on a new day, one of 5 losses; 4 faction heats block a racket at 80. [Heat Widgets]
- **SD businesses:** 11 kinds, 77 passages, the most-patched topic (158 changelog lines across 38 of 55 versions). Round 9b `traces/unnamed_systems.md` §4.
- **IHOH porn taste:** 12 categories, each clip 30 minutes and + that taste; 88 gate reads; categories open at 5/10/30 views. [BRLaptopPorn]
- **Judged NOT systems (counts only):** gardening (7 plants, 12 passages), petitions (4), heists (6 types, 27 passages), gambling (13 passages), a one-shot drink modifier (1, capped at 20), a settings panel (15 kinks, read by 1 passage).
