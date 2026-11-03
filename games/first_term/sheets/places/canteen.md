# [READY] Place — Canteen

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. New section: what the heat proposal built here.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the system sheets. Id `canteen`.

| row | answer |
|---|---|
| kind | destination |
| ENTERED FROM | campus |
| labels — what kind of place | `zone:campus`, `public`, `sells_food` |
| hours | Mon–Fri 08:00–18:00 |
| closed text | "The canteen is shut." |
| hidden until | no |
| fill — word budget | 2,500 words (ledger, unchanged) |
| door | no |
| dress code or wanted state | none |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| none | Zoe, Jake, Nadia: weekdays 11:45–13:00 | eat · listen to what they say | campus |

## Rows (`serves`)

| row | kind | system | cost and effect, with op | BRAKE | on a screen? |
|---|---|---|---|---|---|
| eat | need | energy · money | energy add +20 · money add −5 (guess) · price on the label | once a day, on the trigger | yes, short |
| sit with the table | person | college · `campus_talk` | `campus_talk` add +1 (guess) · the rival may start trouble | once a day, lunch | yes |
| listen | work | college · `campus_talk` | none · what they say reads `campus_talk` | none needed: it writes nothing | yes |

## Built from the heat proposal (signed 2026-11-03)

The plan: `proposals/FIRST_TERM_HEAT_PROPOSAL_20261103.md`. What the build has here:

**Walk-ins.** Her activity rolls on entry (1 in 4 at her lowest band, more higher up); on a hit someone walks in. A man's pay sits on the moment; her cover pays 0.

| who walks in | her activity | when | his pay, on the moment | her bolder answers |
|---|---|---|---|---|
| Zoe | Eat ($5), Listen to what they say | Mon, Wed, Fri 11:45–12:00 | none: no meter | "Let it stay." Corruption +1, cap 39 |
| Jake | Eat ($5), Listen to what they say | Tue, Thu 11:45–12:00 | none: no meter | "Leave it." Exhibitionism +1, cap 19 |
| Nadia | Eat ($5), Listen to what they say | Mon, Tue, Wed, Thu, Fri 12:00–12:15 | none: no meter | a line only, no pay |

**Acts, rungs and pools.**

| what | where | buttons and pays |
|---|---|---|
| Zoe under the table (A2) | her canteen hub, at lunch | "Let her." Hungry 60, Corruption +1, cap 79 · "Not here, Zo." pays 0 |

## Rows a gate needs

| row | gate |
|---|---|
| food costs money | money gates something · a price is on its label |
| `campus_talk` fed and read here | a meter is read |
| eat every weekday | a need can be met every day (with the bed) |

## Why — the source of each key choice

| key choice | source |
|---|---|
| canteen food costs money; talk spreads | LO, chat 2026-10-07 (SYSTEMS §3, §9) |
| lunch for Zoe, Jake, Nadia | LIVES §3 |
| hours | LO took the guess, 2026-10-08 |
| the price and energy | guess |
