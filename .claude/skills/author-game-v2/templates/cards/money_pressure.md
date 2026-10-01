# Card — Money pressure (a system)

> **A worked card, not a template.** Take the shape, leave the furniture. Every line cites a traced game:
> round 9b, `round9b/cards/money_pressure.md` and `round9b/traces/money_pressure.md`. The model is
> **Course of Temptation (CoT)**'s Monday bill; **In Her Own Hands (IHOH)** supplies the miss that turns into
> sex, and **Cupid's Way (CW)** (the Mark waitress chain only) the debt paid in sex. Fill your own card on
> `templates/sheets/system.md`; record it in `board.systems[]`.
>
> **Money pressure is a sink with a clock, not a job.** It has no place and no scene pool of its own. Its job
> is to make every paying system matter. The pressure is the date, not the amount.

| field | the model (CoT; IHOH and CW for the lewd side) | cite |
|---|---|---|
| place and hours | no place: a phone call from Mom that finds her wherever she is, Monday 18:00 or later, every 7 days from day 8; the first call is free and explains the rules. IHOH: a roommate knocks on her door on the 1st | [WeeklyDebtPayment]; `userjs:108402–108408`; [PayRent] |
| cost | base bill $100 → $150 → $200, times a difficulty slider 0.5–2; plus GPA ±20%, Greek dues $50 + housing $50, $200 per child, 10% of clinic debt, and any back debt. IHOH: $450 rent in cash + $500 loan from the bank, monthly | [WeeklyDebtPayment]; `cot_43_greekhouses.js:9–10`; [StoryCaption] |
| one ladder or two | CoT: **two that never touch** (bill size climbs; the lewd climb lives in the jobs). IHOH and CW: **one** — the miss ladder (IHOH) or the debt counter (CW) is the lewd ladder. Copy the one-ladder shape | round 9b `cards/money_pressure.md` |
| pay ladder | the bill climbs with what she has paid: $150 after 5 payments, $200 (cap) after 9; two more steps ($250, $300) are coded but switched off | [WeeklyDebtPaid] |
| lewd ladder | IHOH late rent, counted for the whole game: 1st late = a week's grace; 2nd = evicted unless she "convinces" him (inhibition ≤ 400 or not a virgin); 3rd = inhibition ≤ 350 and not a virgin; else a bad end. CW: a $1,000 debt, −$250 each time she makes Mark cum = 4 acts | [RentDelay_Start]; [RentConvince1]; [RentConvince2]; [BadEnd_Eviction]; round 9b `traces/money_pressure.md` §4 |
| people | Mom (voice only); whoever hands her the phone (best friend, bar owner). IHOH: the roommate collecting, Dad on the loan. CW: Mark | [WeeklyDebtPayment]; [DadCall3] |
| pool, daily | not a pool: 4 delivery openers (own phone, mid-stream, bar landline, best friend's phone). IHOH: 2 roommates × 3 late answers | round 9b `cards/money_pressure.md` |
| memory | `$debtpaid`, `$weeklydebt`, `$backdebt`, `$medicaldebt`, `$lastpaymentday`. IHOH `rent.delay` is lifetime and never resets | [WeeklyDebtPaid]; [RentDelay_Start] |
| growth | grows with the total paid; GPA, sports, Greek life and children move it each week. IHOH flat; an unpaid loan grows +$500 per miss | [WeeklyDebtPayment]; [PassageFooter] |
| sink and deadline | **sink:** all income (jobs, the bar, streaming, gigs) feeds one Monday total. **deadline:** Monday 18:00, shown a week ahead as a red "Owe $N" line on the phone calendar, with "Plus $X from before. FUCK." when she is behind | [WeeklyDebtPayment]; `userjs:121102–121110`; `userjs:121263–121268` |
| feeds · reads | a miss becomes back debt: the shop refuses all but food, outfits and underwear; no piercings; on a date she can't pay (Humiliation +25, romance −2); Relaxation −50. **No game over** (grep 0) · reads money, GPA, sports, Greek membership, children, clinic debt | [ShopItem]; [TattooShopPiercing]; [EventHangoutDinnerOrder]; [WeeklyDebtUnpaid] |
| link into the hook | IHOH: a miss is sex with a roommate to keep the room. CoT: the bill doubles while the starter wage stays flat, which pushes her up the exposure-paid job rungs | [RentConvince1]; round 9b `traces/money_pressure.md` §1 |
| leads to | the roommate (IHOH), Mark (CW), the better-paid lewd job rungs (CoT) | [RentConvince2]; round 9b `cards/money_pressure.md` |

## Measured floors (directions, never gates)
- A due date every 7 days (CoT) or every month (IHOH, two bills on the same day). Round 9b `cards/money_pressure.md`.
- 3 live bill steps, reached after 5 and 9 payments. At the $7/h starter wage the bill is 14.3 / 21.4 / 28.6
  hours a week; at the top $15/h, 6.7–13.3 hours. Round 9b `traces/money_pressure.md` §1.
- 3 misses before the worst outcome (IHOH rent, lifetime; IHOH loan, in a row). CoT has no worst outcome.
  [RentDelay_Start]; [DadCall3].
- 5 modifiers tie the CoT bill to other systems; 2 warning surfaces (calendar line, phone entry). Round 9b `cards/money_pressure.md`.
- The CoT bill is clamped at 200 with `/* !!!! must be removed someday once money is easier */` and a slider
  exists: the curve was eased after launch. [WeeklyDebtPayment].

## What players say
- Money is round 8's second-biggest complaint: 116 complaints in 29 games, 61 of them grind. Round 9b `cards/money_pressure.md`.
- *"it takes so long to build up a decent amount of money"* (CoT, mopoga#51031); *"a microwave is not $800 bro
  lmao"* (CoT, mopoga#68535). The bill must stay inside ~15–30 starter hours a week.

## Our engine today (round 9b §6)
- A recurring bill that escalates by total paid exists: `rent_stages` (`template_import.py:485`) and
  `setup.rentStageIndex = function (totalPaid)` (`v2.py:13530`); `rent_on_short` (`template_import.py:490`)
  carries a short payment forward, like back debt.
- A computed bill (±20% for grades, +$200 per child) is not built (`v2.py:15610`, "only 'random' is
  supported"); author fixed amounts per band instead.
