# [READY] System — job

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08 from SYSTEMS §2, SP4 and the ledger's `job` card.
> Every number marked "guess" is new here and waits for your yes.

| row | answer |
|---|---|
| id · name | `job` · The café job |
| place and hours | `cafe` · Monday to Saturday, 08:00–22:00 · Tom closes to 23:00 |
| cost | a shift: 3 hours (guess) · energy add −20 on the trigger (guess) |
| one ladder or two | one: a bolder uniform pays better tips |
| people | Tom, the manager · Gary, a regular |
| pool | `cafe_shift`, `cafe_shift_events` · `daily = true` |
| memory | the job, the uniforms she has, shifts today, Tom's step, Want and Power |
| growth | climbs |
| sink and deadline | rent, Sunday 00:00 · canteen food · the clothes shop |
| feeds | `money` |
| reads | energy, Exhibitionism, Corruption, the curfew |
| what drives it (S8) | her uniform and Exhibitionism pick the tip rung; shift events rotate |
| link into the hook | it pays her cut of the rent |
| leads to | Tom, Gary |
| day 1 | yes: she can ask for the job on day 1 |
| BRAKE (S9) | the shift row costs energy, and it is gone once `cafe_shift_3_today` is set |

## The shift row

| row | effect, with op | lands on a screen? |
|---|---|---|
| Work a shift | energy add −20 (guess) · money add +12 (normal) or +16 (sexy) | yes, short: who came in |
| the next free shift flag | `cafe_shift_1_today`, then `_2_`, then `_3_` set true | no: it is the cap |
| after three shifts | the row says "No more shifts today." | yes, one line |

**The locks.** Under 20 energy (guess): *"You'd drop a tray. Not today."* Under the curfew, the
evening shift says why it is shut. Classes and shifts overlap; she picks.

## Pool (`pool[]`)

| canvas | what it is | explicit? | what drives it | brake |
|---|---|---|---|---|
| `cafe_shift` | the shift itself: the row above | no | her uniform | three a day, on the trigger |
| `cafe_shift_events` | one small event a shift: Gary, a regular, Tom | guess: yes from Bold, Gary's ten minutes | her stage, her uniform | once a shift, seen ones weighted down |

## Pay ladder (`pay_ladder[]`)

| rung | gate | pay |
|---|---|---|
| 1 | `cafe_job` set | $8 + $4 tips: money add +12 |
| 2 | `uniform_sexy` set · Exhibitionism gte 20 | $8 + $8 tips: money add +16 |
| 3 | the Friday close shift | tips doubled: money add +16 or +24 |
| 4 | `uniform_slutty` · after 0.1 | named with that release |
| paid | Bold · after Tom B 4 | Gary's ten minutes: "$20 — Tom takes half". money add +10 |

**Her climb into paid.** Tom B 2 introduces Gary: he lowers his paper when she pours. Tom B 4 is the
first time. After that, Gary's ten minutes is a shift event, two voices, with "Stop" on every screen.

## Lewd ladder (`lewd_ladder[]`)

| rung | gate | acts |
|---|---|---|
| 1 · Good Girl · Covered | none | Tom reties her apron · the regulars look |
| 2 · Curious · Daring | Exhibitionism gte 20 | the sexy uniform, top button open (Tom B 2) · leaning to pour for Gary |
| 3 · Bold · Showing | Corruption gte 40 | Gary's ten minutes (Tom B 4) · a kiss after close (Tom B 6) |
| 3, repeat | after Tom B 6 | the kiss after close, again, Friday close only |
| 4 · later | Tom B 7 waits; Tom B 8–9 wait for his rewrite | her price named to the room · after hours |

## The meters it writes and reads (`board.meters[]`)

| meter id | kind | key | fed at | read by |
|---|---|---|---|---|
| money | ambient | `money` | `cafe` | the rent, canteen food, the clothes shop |
| exhibitionism | sourced | `exhibitionism` | not here: read only | which uniform she can wear |
| corruption | sourced | `corruption` | here, by Tom's steps | Gary's offer, Tom's steps |

**SP4's week.** A clean week of one evening shift on weekdays and two on Saturday pays $72, $3 short.
A top week in the sexy uniform pays $232.

## Rows a gate needs

| row | gate |
|---|---|
| shift flags set and cleared at midnight | a day-cap closes |
| no shift under 20 energy | a need shuts a door |
| "$20 — Tom takes half" on the button | sex for pay names the amount · a price is on its label |
| Tom B 2, then Tom B 4, then the repeat | her climb |
| the sink and deadline | every system has a card |
| pool has 2, not 20 | a system meets its floors (a warning) |

## Why — the source of each key choice

| key choice | source |
|---|---|
| three uniforms, better tips each | LO, chat (SYSTEMS §2) |
| $8 + $4 and $8 tips, Friday doubles | LO, 2026-10-07 (SP4) |
| three shifts a day, flags not a counter | LO, 2026-10-03 (SP1) |
| café hours, Tom to 23:00 | LO, 2026-10-08 (SP1) |
| Gary's $20, half to Tom | LO, 2026-10-07 (SP4) |
| Tom to step 6 | LO, 2026-10-08 (SP7) |
| Tom's step 6 repeats on Friday close | LO, 2026-10-08 |
| Tom B 7–9 after 0.1 | LO, 2026-10-08 |
| a shift is 3 hours, costs 20 energy | guess |
| Tom B 2 counts as Gary's introduction | guess · `the-arc.md` A15 |
| Gary's ten minutes is explicit as a repeat | guess |
