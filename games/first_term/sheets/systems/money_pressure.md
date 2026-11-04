# [READY] System — money_pressure
> Signed by LO: LO, 2026-11-04.

> Changed 2026-11-04 to match the build; signed by LO 2026-11-04. `money` is declared spent in the ledger; "her cut", as the rent rises.

> Changed 2026-11-04 (LO's answer Q6: the rent page takes the money and is the one count; Mark's Sunday table comes after and counts nothing). Waits for LO's re-sign.

> Changed 2026-11-03 to match the build (third alignment pass); signed by LO 2026-11-04. Rent reads `rent_short`; Vance's knock no longer clears it.

> **Changed 2026-11-03 (LO: "B: keep it easy", DECISIONS 141).** Week one is no longer built to come up short. Up to three café shifts a day make about $205-245 against $75; the section "Week one is built to come up short" below is superseded. What a short Sunday costs is unchanged.

> **Changed 2026-11-01, re-signed by LO 2026-11-01** ("Signed", DECISIONS 113; design DECISIONS 99–112): rent that bites, from `proposals/R1_SYSTEM_RENT.md` (signed 2026-11-01). Changed: the pay, week one built to come up short, what a short Sunday costs, the cards, Mark's prices cut. Engine: `rent_short_weeks` counts short Sundays (DECISIONS 112).

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08 from SYSTEMS §3, SP4 and the ledger's `money_pressure` card.
> Every number marked "guess" is new here and waits for your yes.

| row | answer |
|---|---|
| id · name | `money_pressure` · Money and rent |
| place and hours | `home_kitchen` · the engine takes the rent Sunday 00:00 · Mark's table Sunday morning |
| cost | $75 a week · $90 after $300 paid · $100 after $900 · then flat (the rises stay as built: LO, 2026-11-01, "Continue") |
| one ladder or two | one: the rent climbs. Mark's acts no longer ride on it (no money for her body, 2026-11-01) |
| people | Mark collects · Vance, behind him · Ryan, who may cover her |
| pool | `mark_sunday_table`, `vance_knock`, `ryan_cover` · `daily = false` (weekly) |
| memory | rent carried, `rent_short_weeks` (engine), the paid-in-full streak, Ryan's cover, the total paid, `her_door_unlocked`, the held item |
| growth | climbs |
| sink and deadline | the rent, to Mark, Vance behind him · Sunday 00:00 |
| feeds | `paid_full_streak` (no `laura_suspicion` raise in 0.1; ledger change 25) |
| reads | `money` (the ledger marks it `"spent": true`: she spends it on purpose, so a read below a price is a price, not a descent) · `rent_short_weeks` |
| what drives it | money against what she owes · `rent_short` · `rent_short_weeks` picks the cost · Mark's Power colours the table |
| link into the hook | her cut is part of what Mark owes Vance |
| leads to | Mark, Vance |
| day 1 | from the scene where Mark says she pays rent now (`rent_starts`) |
| BRAKE | the table fires once, Sunday morning only, on its trigger |

## The pay (changed 2026-11-01)

- **A shift pays $8** in any uniform ("Eight a shift, plus tips. Be on time.", Tom). Tips on top, set by the café
  levels (`sheets/systems/job.md`): a quiet shift tips $2–4, more as the customers go further and she lets them.
- **One shift a day on weekdays, two on Saturday.** College takes her mornings; the energy cost stays.
- **The sexy uniform pays in tips, not wages.**
- **Money has somewhere to go:** the skirt ($30), the sheer blouse ($20) and the sports bra ($25) raise her tips.
  Rent now, or the skirt that tips better, later. No other sinks this release.

## Week one is built to come up short

LO (2026-10-31): "I say we miss first few rents inspire her to earn more."

| week | what she can make | due | so |
|---|---|---|---|
| 1 | starts at $0; hired Monday after class, first shift Tuesday; five shifts × ($8 + about $3) ≈ $55 | $75 | short by about $20, even working every day she can |
| 2 | the first customer level open: a hard week ≈ $80–100 | $75 + $20 carried = $95 | close: short, or just made it |
| 3 | the uniform and the next level: $120–160 | $75 (+ carried) | she can pay it all; the four-Sunday streak can start |

A normal player misses two rents; a player who grinds every shift misses one.

## The week

| when | what happens | key, with op |
|---|---|---|
| Sunday 00:00 | the engine takes the rent | money add −75 (then −90, −100) |
| she was short | owed again next week, and counted | `rent_short` set true (cleared only by a full payment) · `rent_short_weeks` add +1 (both by the engine) |
| Sunday morning | Mark sits her at the kitchen table with the sealed envelope; nobody counts it twice (Q6) | paid in full: `paid_full_streak` add +1 |
| a carried Sunday, or Ryan's money | the streak breaks | `paid_full_streak` set 0 |
| a short Saturday or Sunday morning | Ryan offers at his door, $25 once, at his Love 40 | `ryan_covered` set true · Ryan's Warmth add +5 (guess) · never counts for the streak |
| the next evening, Monday 18:00–19:00, within 48 hours of the short Sunday | Vance knocks | nothing: his knock no longer clears `rent_short` |

## What a short Sunday costs (new 2026-11-01)

Three one-time canvases on Sunday morning, read from `rent_short_weeks`:

| short Sunday | gate | what it costs her | what changes after |
|---|---|---|---|
| **1st** | `rent_short_weeks` eq 1 | Mark: "Then it's owed. Vance doesn't wait, so I don't." He **takes the key to her bedroom door** until she's paid up | `her_door_unlocked` set: the house's walk-ins can open her door (Ryan, Mark) until she clears the debt · Mark's Power add +5 |
| **2nd** | `rent_short_weeks` eq 2 | Vance knocks (built, `vance_knock`), and now adds **a $15 late fee** to her face | owed add +15 · Vance's Power add +10 (built) · Mark's Power add +5 |
| **3rd and on** | `rent_short_weeks` gte 3 | Mark takes **one thing she bought** and keeps it in the garage until she's paid up: the first she owns of the skirt, the sheer blouse, the sports bra (a fixed order) | `garage_holds_<item>` set · that garment unequipped and locked in her wardrobe (🔒) · "On the table, then you get it back." · Mark's Power add +5 each time |

- **Paying the whole debt gives back what she lost:** the key (`her_door_unlocked` false), then the item
  (`garage_holds_<item>` false). The streak starts from that Sunday.
- **Engine (checked 2026-11-01):** the count is `setup.carryRent` (DECISIONS 112). The hold needs no engine change:
  each buyable garment gets the condition "`garage_holds_<item>` is false", and `equipItem` refuses a garment whose
  conditions fail; `clothing_item owned` picks which one she has.
- **No sex for money.** What a short week buys is pressure, not an offer.
- **Vance's "Come and see me"** (built) stays a hook. At his Power 60 he asks for her; that answer is not in release 1.

## The cards

- **Week one:** "Pay your first rent to Mark this Sunday: $75." Goals: go to your first class; get a job at the café;
  "Have $75 for Mark by Sunday".
- **After a short Sunday:** "You owe Mark $<owed>. He has your door key." The goal is the full sum by Sunday.
- **Goal 1** as built: four Sundays in a row paid in full from her own money. The tip loses "so does taking his chair".

**Goal 1, the money route — the only route now.** Four Sundays in a row paid in full from her own money. Ryan's cover
never counts. Mark's chair (the body route) is cut.

**The twist.** When goal 1 ends, the offer scene ships (`debt_offer_seen`). Her answer stays parked until 0.2.

## Pool (`pool[]`)

| canvas | what it is | explicit? | what drives it | brake |
|---|---|---|---|---|
| `mark_sunday_table` | the Sunday table, his terms or hers (no price on her body); no second count (Q6) | no | Mark's Power · her stage · `mark_dress_rule` | Sunday morning, once |
| `rent_short_1`, `rent_short_2`, `rent_short_3` (new) | the costs above | no | `rent_short_weeks` | once each (the third repeats per short week) |
| `vance_knock` | Vance at the front door after a short week | no | `rent_short`, in its 48 hours | once per short week |
| `ryan_cover` | Ryan offers what she's short | no | money under the rent | Saturday or Sunday morning, once |

## Pay ladder (`pay_ladder[]`)

| rung | gate | pay |
|---|---|---|
| 1 | `rent_starts` set · total paid under $300 | she owes $75 |
| 2 | total paid reaches $300 | she owes $90; Mark names it as Vance's |
| 3 | total paid reaches $900 | she owes $100, then flat |
| ~~4~~ | cut 2026-11-01 | Mark's prices: no money for her body |

## Lewd ladder (`lewd_ladder[]`)

| rung | gate | acts |
|---|---|---|
| 1 · Good Girl · Covered | none | at his table in her sleep shirt (Mark step 1) · his eyes on the hem |
| 2 | after one short Sunday | shorts to the table (Mark step 3) · his dress rule at the table |
| ~~3~~ | cut 2026-11-01 | a bill off, twenty and he can look, his chair (Mark A 5, 7, 9) |

## The meters it writes and reads (`board.meters[]`)

| meter id | kind | key | fed at | read by |
|---|---|---|---|---|
| paid_full_streak | sourced | `paid_full_streak` | `home_kitchen` | goal 1: four Sundays in a row |
| money | ambient | `money` | `cafe` | the rent, canteen food, the clothes shop |

**Over 8 weeks** she owes $660. The old $1,856 (up to three shifts a day at $12–24) no longer holds; at $8 a shift plus tips it is set by the café levels (re-count at build).

## Rows a gate needs

| row | gate |
|---|---|
| $75 taken Sunday 00:00, carried when short | the obligation is charged |
| the table reads `money` and `rent_short` · the short canvases read `rent_short_weeks` | money gates something |
| sink and deadline named | every system has a card |
| leads to Mark and Vance | leads to a person |
| `paid_full_streak` read by goal 1 | a meter is read · a goal's end is built |
| the late fee said to her face, and on the card | a price is on its label |

## Why — the source of each key choice

| key choice | source |
|---|---|
| $75, rising to $90 and $100 | LO, 2026-10-07 (SP4) |
| carried, not a game over | LO, 2026-10-07 (SP4) |
| four Sundays in a row; Ryan's cover never counts | LO, 2026-10-07 (SP4) |
| rent starts after Mark's scene | LO, 2026-10-07 (SYSTEMS, decided item 2) |
| Mark's prices paid as money | LO, 2026-10-07 (SYSTEMS, decided item 8) · **cut** 2026-11-01 (LO: "sex in return of money is not good") |
| Vance knocks the next evening | LO approved the week plan, 2026-10-05 |
| Ryan's Warmth +5 for covering | guess |
| the table's priced look, from Bold | LO, 2026-10-08 (question 33) · **cut** 2026-11-01 |
| $8 a shift, week one short, the three costs, the cards | `proposals/R1_SYSTEM_RENT.md`, signed by LO 2026-11-01 (DECISIONS 101) |
