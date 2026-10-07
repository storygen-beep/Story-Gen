# [REVIEW] System — money_pressure

> A draft for LO to place. Written 2026-10-08 from SYSTEMS §3, SP4 and the ledger's `money_pressure` card.
> Every number marked "guess" is new here and waits for your yes.

| row | answer |
|---|---|
| id · name | `money_pressure` · Money and rent |
| place and hours | `home_kitchen` · the engine takes the rent Sunday 00:00 · Mark's table Sunday morning |
| cost | $75 a week · $90 after $300 paid · $100 after $900 · then flat |
| one ladder or two | one: the rent climbs, and Mark's acts ride on the same table |
| people | Mark collects · Vance, behind him · Ryan, who may cover her |
| pool | `mark_sunday_table`, `vance_knock`, `ryan_cover` · `daily = false` (weekly) |
| memory | rent carried, the paid-in-full streak, Ryan's cover, the total paid |
| growth | climbs |
| sink and deadline | the rent, to Mark, Vance behind him · Sunday 00:00 |
| feeds | `paid_full_streak` (no `laura_suspicion` raise in 0.1; ledger change 25) |
| reads | `money` |
| what drives it (S8) | money against what she owes · `rent_carried` · Mark's Want and Power colour the table |
| link into the hook | her $75 is part of what Mark owes Vance |
| leads to | Mark, Vance |
| day 1 | from the scene where Mark says she pays rent now (`rent_starts`) |
| BRAKE (S9) | the table fires once, Sunday morning only, on its trigger |

## The week

| when | what happens | key, with op |
|---|---|---|
| Sunday 00:00 | the engine takes the rent | money add −75 (then −90, −100) |
| she was short | owed again next week | `rent_carried` set true, by the engine |
| Sunday morning | Mark counts it at the kitchen table | paid in full: `paid_full_streak` add +1 |
| a carried Sunday, or Ryan's money | the streak breaks | `paid_full_streak` set 0 |
| a short Saturday or Sunday morning | Ryan offers at his door | `ryan_covered` set true · Ryan's Warmth add +5 (guess) |
| the next evening, Monday (guess) | Vance knocks | `rent_carried` set false |
| Bold, before Sunday 00:00 | Mark pays her for a look | money add +20, at most (SP4) |

**Goal 1, the money route.** Four Sundays in a row paid in full from her own money. Ryan's cover never
counts, and neither does Mark's money.

**The twist.** When goal 1 ends, the offer scene ships (`debt_offer_seen`). Her answer stays parked
until 0.2.

## Pool (`pool[]`)

| canvas | what it is | explicit? | what drives it | brake |
|---|---|---|---|---|
| `mark_sunday_table` | the count, his terms or hers; "twenty, and you can look" | yes, from Bold (LO, 2026-10-08) | Mark's Power · her stage | Sunday morning, once |
| `vance_knock` | Vance at the front door after a short week | no | `rent_carried` | once per carried week |
| `ryan_cover` | Ryan offers what she's short | no | money under the rent | Saturday or Sunday morning, once |

## Pay ladder (`pay_ladder[]`)

| rung | gate | pay |
|---|---|---|
| 1 | `rent_starts` set · total paid under $300 | she owes $75 |
| 2 | total paid reaches $300 | she owes $90; Mark names it as Vance's |
| 3 | total paid reaches $900 | she owes $100, then flat |
| 4 | Bold: Corruption gte 40 | Mark's prices, paid before the rent: up to $20 |

## Lewd ladder (`lewd_ladder[]`)

| rung | gate | acts |
|---|---|---|
| 1 · Good Girl · Covered | none | counted in her sleep shirt (Mark A 1) · his eyes on the hem |
| 2 · Curious · Daring | Corruption and Exhibitionism gte 20 | shorts to the table (Mark A 3) · his dress rule at the table |
| 3 · Bold · Showing | Corruption gte 40 | a bill off (Mark A 5) · twenty, he can look (Mark A 7) |
| 3, top | Corruption and Exhibitionism gte 40 | his chair (Mark A 9), goal 1's body route |

Every version where Mark names the act has a labelled, parked no: *"Not with your mother home."*

## The meters it writes and reads (`board.meters[]`)

| meter id | kind | key | fed at | read by |
|---|---|---|---|---|
| paid_full_streak | sourced | `paid_full_streak` | `home_kitchen` | goal 1: four Sundays in a row |
| money | ambient | `money` | `cafe` | the rent, canteen food, the clothes shop |

**Over 8 weeks** she owes $660 and can earn $1,856.

## Rows a gate needs

| row | gate |
|---|---|
| $75 taken Sunday 00:00, carried when short | the obligation is charged |
| the table reads `money` and `rent_carried` | money gates something |
| sink and deadline named | every system has a card |
| leads to Mark and Vance | leads to a person |
| `paid_full_streak` read by goal 1 | a meter is read · a goal's end is built |
| Mark's price on the button | a price is on its label |

## Why — the source of each key choice

| key choice | source |
|---|---|
| $75, rising to $90 and $100 | LO, 2026-10-07 (SP4) |
| carried, not a game over | LO, 2026-10-07 (SP4) |
| four Sundays in a row; Ryan's cover never counts | LO, 2026-10-07 (SP4) |
| rent starts after Mark's scene | LO, 2026-10-07 (SYSTEMS, decided item 2) |
| Mark's prices paid as money | LO, 2026-10-07 (SYSTEMS, decided item 8) |
| Vance knocks the next evening | LO approved the week plan, 2026-10-05 |
| Ryan's Warmth +5 for covering | guess |
| the table's priced look, from Bold | LO, 2026-10-08 (question 33) |
