# [READY] Place — Café

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the system sheets. Id `cafe`.

| row | answer |
|---|---|
| kind | destination |
| ENTERED FROM (S2) | street |
| labels — what kind of place | `zone:town`, `public` |
| hours | Mon–Sat 08:00–22:00 |
| closed text | "Closed. Back Monday." on Sunday · after 22:00, only by staying for Tom |
| hidden until | no |
| fill — word budget (S3) | 9,000 words (ledger, unchanged) |
| door | no: a shop |
| dress code or wanted state | the café uniform on shift (`clothing_rules`) · "Uniform, @player." · she changes in the back |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| the job ask, first visit, until `cafe_job` is set | Tom: Mon–Sat 08:00–23:00 | work a shift | the street |
| Tom B 1–6 in their windows | Gary: weekdays 14:30–18:00 · Friday 20:00–22:00 |  |  |

## Rows (`serves`)

| row | kind | system | cost and effect, with op (S4) | BRAKE (S9) | on a screen? |
|---|---|---|---|---|---|
| ask for a job | work | job | `cafe_job` set true · meets Tom | once | yes |
| work a shift | work | job | energy add −20 · money add +12 or +16 | energy on the trigger; gone after 3 | yes, short |
| Tom | person | Tom's ladder | his Want and Power read (colour) | once per window | yes |
| Gary, booth four | person | job | his look · after Tom B 4: "$20 — Tom takes half" | once a shift | yes |
| stay after close, Friday | person | Tom's ladder | the kiss repeats (after Tom B 6) | Friday close, once | yes |

## Rows a gate needs

| row | gate |
|---|---|
| three shift flags, cleared at midnight | a day-cap closes |
| the price on Gary's button | sex for pay names the amount |
| Tom works beside her | the walk-in floor |

## Why — the source of each key choice

| key choice | source |
|---|---|
| café hours, Tom to 23:00 | LO, 2026-10-08 (SP1) |
| the uniform | LO, chat (SYSTEMS §2) |
| the Friday kiss repeats | LO, 2026-10-08 |
| the job ask | SYSTEMS §2 (day 1) |
