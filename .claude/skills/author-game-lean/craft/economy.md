# craft/economy.md — money, the bill and what things cost

Read this before you write a card that pays her, charges her, or collects a bill. Checked against Course of Temptation (CoT) and the field (LO, relayed 2026-11-22: "yes, send it"). The time on a button is `craft/clock.md`; the label's shape is `craft/places.md`.

## Must read

The card's `Craft:` line cites each one, or says in one line why it skips it. `when` and `judge` are the labels in `SKILL.md`, "Rule labels".

| id | what it asks | the failure it stops | when | judge |
|---|---|---|---|---|
| C1003 | the bill is real, recurring and has a face | — | the plan | note |
| C1004 | it has a date, a face who collects, and is armed only after income exists | — | the plan | note |
| C1033 | the first collection is free and explains the rules | — | a price or pay is shown | note |
| C1008 | a rise works when the collector says the new number at the moment of payment | — | a price or pay is shown | note |
| C1014 | climb through the opening, then plateau; top games cap it by hand | — | the plan | note |
| C1013 | a short week is carried, not game over, and costs her something | — | a price or pay is shown | note |
| C1016 | the first rent can be paid by working clean | — · kept blocking: LO's choice (2026-11-24) | the plan | reader |
| C1020 | one currency, declared once | — | the plan | note |
| C1021 | a price on a button is a figure: "($3)" | — | a price or pay is shown | note |
| C1022 | the default is `$`, and prose names no real-world currency | P13 reader pass 8: "you've never had a dollar that wasn't your mom's" | a price or pay is shown | reader |
| C954 | a spend price stays on the button; pay she earns is said in the scene, never on the button | — | a price or pay is shown | note |
| C1001 | spends outnumber earns | — | the plan | note |
| C1002 | a spend lives where the thing bought lives | — | a place is entered | note |
| C989 | money is the system that makes her choose | — · kept blocking: LO's choice (2026-11-24) | the plan | reader |
| C990 | money gates content: conditions read the money, not only prices | — · kept blocking: LO's choice (2026-11-24) | the plan | reader |
| C951 | keep the amount in prose; the player budgets against it | — · kept blocking: LO's choice (2026-11-24) | a price or pay is shown | reader |
| C952 | every number a scene or a card states agrees with the plan and the ledger | — · kept blocking: LO's choice (2026-11-24) | a price or pay is shown, a goal card is shown | reader |
| C992 | example numbers are filler; derive real prices from her week's income | — | the plan | note |
| C1017 | a route to money she'd be ashamed of is visible but locked, never the only way to pay | — · kept blocking: LO's choice (2026-11-24) | the plan | reader |
| C967 | a game with no paid sex says so | — | the plan | note |

## The measures

CoT, read in full 2026-11-22 (`/Users/a0000/Documents/Player_Legibility_Study_20260825/corpus/course-of-temptation/passages`):
- **`WeeklyDebtPayment.txt`.** `$weeklydebt` starts at 100 (line 1) and is capped at 200, with the author's note "/* !!!! must be removed someday once money is easier */" (line 3). Her mom phones. Without a phone, someone with her hands one over: "It's... your mom?" (line 18) or "Please. It's your mom. She won't stop calling." (line 29). The first call explains the rules: "Have you found a job yet?... some of these payments depend on your grades..." with a GPA line at 2.5 (lines 37, 68-70). Every amount is shown, multiplied by a difficulty option (`$optdebtpaymentmultiplier`).
- **`WeeklyDebtPaid.txt`.** The bill goes 100 to 150 once $500 has been paid in total, and 150 to 200 at $1,000, each said out loud: "Next week we're going to need $… to keep up." (lines 8-15). The rises at 250 and 300 are switched off with `false and` (lines 16, 20), so it's capped by hand. Otherwise: "I know it sucks, but please don't forget we'll need the same amount from you next week." (line 25)
- **`WeeklyDebtUnpaid.txt`.** The lecture ("you need to start taking some responsibility... Find a job and get the money"), then `<<dalterneed Relaxation -50 true>>`, and play goes on (lines 1, 5).
- **The job button.** QuickieBurger's shift button is "Work" with its time and rest cost (`<<dtime 60>>`, `<<dalterneed Rest …>>`) and no pay (`QuickieBurger.txt`, lines 8-11). The wage sits on the Work page ("Wages: $… / hour", `Work.txt`, line 14). That's one job read, not a count.

Field-measured, from `lists/COVERAGE.md`'s evidence column and not re-run today: C1001 (median 2.2 spends to 1 earn), C1002, C989 and C990 (18 games), C1020–C1022 (one currency; 94% of prices as a symbol; 10 of 16 games use $), and C954.

## The shape

Each rule is marked **measured** or **LO's choice**.

1. **The bill is weekly, real, and has a face** who collects it and says the number out loud (C1003, C1004). *Measured:* CoT's mom, every week.
2. **The first collection explains the rules** (C1033). *Measured:* CoT's first call.
3. **The bill climbs through the opening, each rise said at payment, then plateaus at a cap** (C1008, C1014). *Measured:* CoT goes 100 to 150 to 200, and switches off its higher rises by hand.
4. **A short week is carried, not game over, and costs her something she feels** (C1013). *Measured:* CoT's lecture and −50 Relaxation, then play goes on.
5. **One currency, `$`, figures on buttons** (C1020–C1022). *Measured in the field.*
6. **A spend price is on the button; pay she earns is said in the scene that offers the work,** never on the button (C954). *Measured in the field;* CoT's "Work" button shows time and rest, and its wage is on the Work page.
7. **Spends outnumber earns, and each spend lives where the thing bought lives** (C1001, C1002). *Measured in the field.*
8. **Money gates something** (C989, C990), and **every amount in prose agrees with the ledger** (C951, C952; the truth rule). *Measured in the field;* the truth rule is *LO's choice.*
9. **The first rent is payable by working clean** (C1016). *LO's choice.* A route she'd be ashamed of is visible but locked (C1017); release 1 has none.

## When paid sex opens (not in release 1)

Release 1 has no paid sex, and the game says so (C967, LO's). When a release opens it, read C966–C973 in `lists/COVERAGE.md` first:
- only money paid for the act on screen counts;
- someone introduces it in a one-time scene before the activity appears;
- a first time comes before any repeat;
- the price is on screen before she agrees;
- there's always a no.

## Worked example

Roles: her step-father, who keeps the rent book, and her mom. LO approved these words, with the names swapped for roles. The figures show the shape only: example numbers are filler, and a game's real numbers come from her week's income (C992).

**Kitchen, Sunday**
> Your step-father's at the table with a mug and a pen. The rent book is open in front of him.
> Step-father: "Sunday. Seventy-five."

Buttons: Pay him ($75) (only when she has it) · "I don't have it all."

**After paying, at $300 paid in total**
> He counts it twice and writes it down.
> Step-father: "Good. It's ninety from next week. Things cost more."
> Your stomach drops. You just worked all week for that.

**After "I don't have it all."**
> He takes what you have and writes the rest under your name.
> Step-father: "It waits a week. Not two."
> Your face goes hot. Mom keeps her eyes on the sink.

The rest is carried and shows on the rent page. Play goes on.

## Not this

- Earned pay on a button: "Work a shift (+$22)". Say the pay in the scene that offers the work (C954).
- A bill that never moves. It climbs through the opening, then plateaus (C1014).
- A short week that ends the game. It's carried, and it costs her (C1013).
- An amount in prose that disagrees with the ledger (C952).
