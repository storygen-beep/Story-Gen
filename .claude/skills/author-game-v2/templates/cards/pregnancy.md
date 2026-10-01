# Card — Pregnancy (a system)

> **A worked card, not a template.** Take the shape, leave the furniture. Every line cites a traced game:
> round 9b, `round9b/cards/pregnancy.md` and `round9b/traces/pregnancy.md`. Model: **Course of Temptation (CoT)
> only** (IHOH, SD and CW have none). Fill your own card on `templates/sheets/system.md`; record it in `board.systems[]`.

| field | the model (CoT) | cite |
|---|---|---|
| place and hours | anywhere sex happens (the risk); a test in any of 7 bathrooms; the campus clinic (birth control, check-ups); her phone (a cycle app); the weekly call home (the cost) | [PregnancyTest]; [CampusClinicBirthControl]; [PhoneMain]; [WeeklyDebtPayment] |
| cost | protection: a daily pill, or an IUD, implant or condoms bought (clinic prices $50–$800). Pregnant: Food ×1.1–1.3, Rest ×1.05–1.3, Bladder ×1.1–1.4 faster. After birth $200 a week per child sent home | [CampusClinicBirthControl]; `cot_50_needs.js:133`; `cot_65_storyfunc.js:5114` |
| one ladder or two | **no pay ladder**: it costs money and pays in story. One ladder, the stages of her body | round 9b `cards/pregnancy.md` |
| pay ladder | none | round 9b `cards/pregnancy.md` |
| lewd ladder | the risk sits inside every unprotected scene (a partner carries a condom, asks for one, or insists; "risky sex" text behind the breeding switch, 28 readers); 3 breeding-kink events; strangers touching the bump; the father's reaction | [EventWalkingPregnancyStrangerFeel]; round 9b `cards/pregnancy.md` |
| people | the father (6 outcomes: support, not ready, wants it, breakup, congratulate, commiserate); strangers on walks; the clinic doctor; parents (the bill); friends who advise; NPCs who get pregnant too | [EventInPersonInformOfPregnancy]; [EventCampusWalkPregnant] |
| pool, daily | 38 event entries (35 passages) with a pregnancy condition; 55 named pregnancy and birth passages | round 9b `cards/pregnancy.md` |
| memory | per pregnancy: father, start, days, trimester, due date, showing noticed; last creampie per partner (who is the father); children and their status; pills taken by day | `cot_57_pregnancy.js:803` |
| growth | odds by cycle day: 0 on days 1–7, 5–30% on days 8–15, 0.2% after. One day per day: trimester 2 at day 56, 3 at day 112; showing at day 65; due at 168 (option 28–252); labour 11.3% per awake hour once due | round 9b `traces/pregnancy.md`; `cot_57_pregnancy.js:8` |
| sink and deadline | $200 a week per child sent home, every week after | [WeeklyDebtPayment]; `cot_65_storyfunc.js:5114` |
| feeds | her needs (faster decay), money, NPC reactions, the father's relationship | `cot_50_needs.js:133`; [EventInPersonInformOfPregnancy] |
| reads | the breeding switch (default on), cycle day, protection, partner age (×0.5 at 30+) | `cot_23_database_inclinations.js:1502` |
| link into the hook | risk on every unprotected scene, then a body that shows, people who notice, a father and a choice, a lasting bill | round 9b `cards/pregnancy.md` |
| leads to | the father talk; clinic check-ups; birth, then adoption or sending the child home | [CampusClinicPregnancyCheckup]; [PendingBirths]; [PendingBirthsAdopt]; [PendingBirthsSendHome] |

## Measured floors (directions, never gates)
- A switch, on by default, with options for odds (0.05–5×) and length (28–252 days). `cot_23_database_inclinations.js:1502`
- A way for her to know: tests (positive from day 6, sure by day 14) and a cycle app. [PregnancyTest]; [PhoneMain]
- Showing at a fixed day (65), so people react on schedule; 38 reaction events plus 6 father outcomes. Round 9b `cards/pregnancy.md`.
- Birth is a choice with a lasting cost, not a game over. [PendingBirths]
- The odds: 4.2% per creampie on a random day, 73% per cycle with daily unprotected sex, 2.3% on the pill.
  Players read this as broken; say the odds on the scene. Round 9b `traces/pregnancy.md`.

## What players say
- *"Waiting for pregnancy update"* (CoT, mopoga#177749), the game's top comment; *"We literally just want pregnancy
  bro you keep hinting towards it"* (CoT, mopoga#182919). Birth control shipped first and read as a promise.
- After release, two threads said the odds felt broken (57 and 98 creampies without a pregnancy). Pregnancy is the
  #1 ask: 226 ask verdicts across 30 games.

## Our engine today (round 9b §6)
- Partial: a pregnancy trait only swaps the player portrait to a pregnant variant (`template_import.py:961`,
  used at `v2.py:1892`). No cycle, conception roll or stage primitive; build them from traits, flags and conditions.
