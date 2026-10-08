# [READY] Place — Canteen

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the system sheets. Id `canteen`.

| row | answer |
|---|---|
| kind | destination |
| ENTERED FROM (S2) | campus |
| labels — what kind of place | `zone:campus`, `public`, `sells_food` |
| hours | Mon–Fri 08:00–18:00 |
| closed text | "The canteen is shut." |
| hidden until | no |
| fill — word budget (S3) | 2,500 words (ledger, unchanged) |
| door | no |
| dress code or wanted state | none |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| none | Zoe, Jake, Nadia: weekdays 11:45–13:00 | eat · listen to what they say | campus |

## Rows (`serves`)

| row | kind | system | cost and effect, with op (S4) | BRAKE (S9) | on a screen? |
|---|---|---|---|---|---|
| eat | need | energy · money | energy add +20 · money add −5 (guess) · price on the label | once a day, on the trigger | yes, short |
| sit with the table | person | college · `campus_talk` | `campus_talk` add +1 (guess) · the rival may start trouble | once a day, lunch | yes |
| listen | work | college · `campus_talk` | none · what they say reads `campus_talk` | none needed: it writes nothing | yes |

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
