# [REVIEW] System — job

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. File and line cites removed.

> **Changed 2026-11-01, re-signed by LO 2026-11-01** ("Signed", DECISIONS 113; design DECISIONS 99–112): the café customers, from
> `proposals/R1_SYSTEM_CAFE.md` (signed 2026-11-01), with pay from `proposals/R1_SYSTEM_RENT.md`. Changed: the shift,
> pay, one drawn customer scene a shift in three levels, Gary as the regular, the café's footfall and name, Tom's top
> step, what reaches home and the street. Cut: Gary's paid ten minutes and Tom's half.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08 from SYSTEMS §2, SP4 and the ledger's `job` card.
> Every number marked "guess" is new here and waits for your yes.

| row | answer |
|---|---|
| id · name | `job` · The café job |
| place and hours | `cafe` · Monday to Saturday, 08:00–22:00 · Tom closes to 23:00 |
| cost | a shift: 3 hours (guess) · energy add −20 on the trigger (guess) |
| one ladder or two | one: the customers go further as she does (three levels) |
| people | Tom, the manager, strict: he never sells her and never tells her to wear less · Gary, the regular · the customers |
| pool | `cafe_shift` · one customer scene a shift from the pool for her level, 4–6 per level · `daily = true` |
| memory | the job, the uniforms she has, shifts today, level-2 shifts played, `cafe_footfall`, `cafe_name`, the window rule, Tom's step |
| growth | climbs |
| sink and deadline | rent, Sunday 00:00 · canteen food · the clothes shop |
| feeds | `money` · Corruption · Exhibitionism · `cafe_footfall` · `cafe_name` |
| reads | energy, Exhibitionism, Corruption, the uniform, the curfew |
| what drives it | her meters pick the level; her choice picks the tip |
| link into the hook | it pays her rent, and it is never enough at first (`money_pressure.md`, week one) |
| leads to | Tom, Gary |
| day 1 | yes: she can ask for the job on day 1; first shift Tuesday |
| BRAKE | one shift on weekdays, two on Saturday (`cafe_shift_<k>_today`) · energy |

## A shift

Clock in · **one customer scene, drawn from the pool for her level** · clock out with **$8 plus that shift's tips**.
The scene never repeats two shifts running: each level's pool is a shuffle bag (`block_pool` `memory = "seen"`,
`seen_weight = 0`: no repeats until every scene has shown, then a new round; engine, DECISIONS 112). A pool entry is
text only, so each level is its own canvas with its own choices, and the customer's scene comes from the pool.

| row | effect, with op | lands on a screen? |
|---|---|---|
| Work a shift | energy add −20 (guess) · money add +8 · the tip, by the scene's choice | yes: the customer scene |
| the next free shift flag | weekdays `cafe_shift_1_today`; Saturday `_1_`, then `_2_` | no: it is the cap |
| after the cap | "No more shifts today." | yes, one line |

**The locks.** Under 20 energy (guess): *"You'd drop a tray. Not today."* Under the curfew, the evening shift says why
it is shut. Classes and shifts overlap; she picks.

## Three levels: the customers go further as she does

| level | opens at | what the customers do | her choices | tips |
|---|---|---|---|---|
| **1 · They look** | the job | eyes on her when she bends to a table; a table whispering when she walks away | none needed: the scene is the room watching | $2–4 |
| **2 · They say it** | Daring (Exhibitionism 20), or the sexy uniform on | "Are you on the menu?" · a guy asks what time she gets off · a table rates her out loud | **play along** (showing yes: leans over the check, Exhibitionism +1) · **flirt back** (doing yes: Corruption +1) · **"Not tonight, hon."** | $4–8; playing along $6–10 |
| **3 · They touch** | Curious (Corruption 20) **and** Daring (Exhibitionism 20), after three level-2 shifts | a hand on her ass when she leans over · a hand up the back of her skirt at the counter · a guy pulls her onto his knee to "say thanks" | **let it** (both meters +1: seen, and touch) · **pull away**, polite ("Your food's here, sir.") · **slap it away** (he leaves, no tip) | $4–8; **let it: doubled, $10–16** |

- **The sexy uniform is her choice** (Tom doesn't push it). It opens level 2 early and adds +50% to tips.
- **The no is written at every level** and costs only tips, never her job.
- **After Tom's step 3** (the window rule), level-3 scenes stop using the window seats.
- **Levels 4 and up** (under the table, the back room, the regulars as a group) are a later release, shown locked with
  the number.

## Gary, the regular

Gary (52, booth four) is the face that comes back. Level 1 he lowers his paper; level 2 he says it; level 3 his is the
hand she lets stay, or not. He tips +$4 over strangers and remembers what she let him do last time. His own route is a
later release. `npc_gary.md` is rewritten to match: met at level 1, not at booth four.

## The café keeps score

| counter | moves | read by |
|---|---|---|
| `cafe_footfall` (player trait, −20…+30) | +1 every shift she plays along or lets them | footfall 10: fuller tables, more men waiting, tips +$2 · the street and home lines · Tom's step 3 |
| `cafe_name` (player trait, −20…+30) | −1 every shift she lets them touch | Tom's step 3 (name −5 or lower) |

At **footfall 15 and name −5**, Tom's top step, "Not by the window" (`npc_tom.md`).

## The café reaches the rest of her life

- **The street** (the street scene, `meters.md` rule 2): from footfall 10, "You're the girl from the café."
- **Home:** Mark's Sunday table, from footfall 10: "Good tips this week. What are they tipping for?" · Ryan, at his Lust
  40+: "Some guys from the yard said they went to your café."

## Against the taste columns

| column | here |
|---|---|
| who sees | the room, every shift; Gary, who comes back; Tom, at the top |
| what she risks | being seen letting it; the café's name; Tom's line |
| how she says yes | two kinds at levels 2 and 3, plus the no |
| his move | the customer's: the comment, the hand. Hers to allow |
| does it finish | yes: each scene ends with the tip, and the line about what she did for it |
| what changes after | footfall and name; the fuller room; Tom's window rule; the street and the house know |

## Pay ladder (`pay_ladder[]`)

| rung | gate | pay |
|---|---|---|
| 1 | `cafe_job` set | $8 + level-1 tips $2–4 |
| 2 | level 2 (Daring, or the sexy uniform) | $8 + $4–8; playing along $6–10; sexy uniform +50% tips |
| 3 | level 3 | $8 + $4–8; let it, $10–16 |
| busy | `cafe_footfall` 10 | tips +$2 |
| Friday close | stays as built: a Friday evening shift pays $16, $24 in the sexy uniform (LO, 2026-11-01, "Continue") | — |
| ~~paid~~ | cut 2026-11-01 | Gary's ten minutes, "$20 — Tom takes half": Tom never sells her |

## Lewd ladder (`lewd_ladder[]`)

| rung | gate | acts |
|---|---|---|
| 1 · Good Girl · Covered | none | Tom reties her apron, strict · the room looks |
| 2 · Daring, or the sexy uniform | Exhibitionism gte 20 | they say it; she plays along or flirts back |
| 3 · Curious and Daring | Corruption 20 and Exhibitionism 20, three level-2 shifts | they touch; she lets it, or not |
| 4 · later | shown locked with the number | under the table, the back room, the regulars as a group |

## The meters it writes and reads (`board.meters[]`)

| meter id | kind | key | fed at | read by |
|---|---|---|---|---|
| money | ambient | `money` | `cafe` | the rent, canteen food, the clothes shop |
| exhibitionism | sourced | `exhibitionism` | here, playing along and letting it | the levels |
| corruption | sourced | `corruption` | here, flirting back and letting it | the levels |
| cafe_footfall | sourced | `cafe_footfall` | here | Tom's step 3, the street, home |
| cafe_name | sourced | `cafe_name` | here | Tom's step 3 |

**The week** (`money_pressure.md`): week one ≈ $55 against $75; week three $120–160.

## Rows a gate needs

| row | gate |
|---|---|
| shift flags set and cleared at midnight | a day-cap closes |
| no shift under 20 energy | a need shuts a door |
| a no written at every level | a no has content |
| footfall and name read by Tom, the street and home | a meter is read |
| the sink and deadline | every system has a card |
| a pool of 4–6 per level | a system meets its floors |

## Why — the source of each key choice

| key choice | source |
|---|---|
| $8 a shift, one a weekday and two on Saturday | `proposals/R1_SYSTEM_RENT.md`, signed by LO 2026-11-01 (DECISIONS 101) |
| the three levels, the choices, the tips, Gary, footfall and name, Tom's line | `proposals/R1_SYSTEM_CAFE.md`, signed by LO 2026-11-01 (DECISIONS 103) · scout `scout/cafe_customers.md` (IHOH, corrupted-city, CoT) |
| Tom strict, never sells her | LO, 2026-10-31 |
| no repeats until all shown | engine, `seen_weight = 0` (DECISIONS 112) |
| café hours, Tom to 23:00 | LO, 2026-10-08 (SP1) |
| a shift is 3 hours, costs 20 energy | guess |
| leaving after Tom's close sets `late_shift` | LO's play note, 2026-10-08 |
| Gary's $20, half to Tom | LO, 2026-10-07 (SP4) · **cut** 2026-11-01 |
