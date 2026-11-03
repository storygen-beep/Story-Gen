# [REVIEW] Place — Café

> Changed 2026-11-04 (LO's answer Q2: the café's one-time scenes open from its activities, not on entry). Waits for LO's re-sign.

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. New section: what the heat proposal built here. Points at the copy fixes it took.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08). Re-signed 2026-10-29 ("sign all", in chat).

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the system sheets. Id `cafe`.

| row | answer |
|---|---|
| kind | destination |
| ENTERED FROM | town (the bus, 15 minutes, on the way in) |
| labels — what kind of place | `zone:town`, `public` |
| hours | Mon–Sat 08:00–23:00 (changed 2026-10-29, LO: open till 23:00 so Tom's after-close scenes can play; re-signed by LO 2026-10-29) |
| closed text | "The café's shut." (every day; the engine adds when it opens) · 22:00–23:00 the shifts are over and Tom is closing |
| hidden until | no |
| fill — word budget | 9,000 words (ledger, unchanged) |
| door | no: a shop |
| dress code or wanted state | the café uniform on shift (`clothing_rules`) · "Uniform, @player." · she changes in the back |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| none (LO, 2026-11-04, Q2): the job ask opens from "Order a coffee ($3)" until `cafe_job`; Tom's apron, the tip jar and Gary's first meeting open from "Work a shift"; "Not by the window" opens from Tom at the counter. Each keeps its own window and gates, and the room's own links always show | Tom: Mon–Sat 08:00–23:00 | work a shift | the street |
|  | Gary: weekdays 14:30–18:00 · Friday 20:00–22:00 |  |  |

## Rows (`serves`)

| row | kind | system | cost and effect, with op | BRAKE | on a screen? |
|---|---|---|---|---|---|
| ask for a job | work | job | `cafe_job` set true · meets Tom | once | yes |
| work a shift | work | job | energy add −20 · money add +12 or +16 | energy on the trigger; gone after 3 | yes, short |
| Tom | person | Tom's ladder | his Want and Power read (colour) | once per window | yes |
| Gary, booth four | person | job | his look · after Tom B 4: "$20 — Tom takes half" | once a shift | yes |
| stay after close, Friday | person | Tom's ladder | the kiss repeats (after Tom B 6) | Friday close, once | yes |

## Built from the heat proposal (signed 2026-11-03)

The plan: `proposals/FIRST_TERM_HEAT_PROPOSAL_20261103.md`. What the build has here:

**Walk-ins.** Her activity rolls on entry (1 in 4 at her lowest band, more higher up); on a hit someone walks in. A man's pay sits on the moment; her cover pays 0.

| who walks in | her activity | when | his pay, on the moment | her bolder answers |
|---|---|---|---|---|
| Gary | Order a coffee ($3) | Mon, Tue, Wed, Thu, Fri 14:30–18:00; Fri 20:00–22:00 | none: no meter | "Leave it." Corruption +1, cap 19; "Let his hand rest on your thigh." Corruption +1, cap 39 |

## Rows a gate needs

| row | gate |
|---|---|
| three shift flags, cleared at midnight | a day-cap closes |
| the price on Gary's button | sex for pay names the amount |
| Tom works beside her | the walk-in floor |

**Copy:** lines here were rewritten from `proposals/COPY_FIXES_C.md` (signed with the a2 sheets, DECISIONS 125).

## Why — the source of each key choice

| key choice | source |
|---|---|
| café hours, Tom to 23:00 | LO, 2026-10-08 (SP1) |
| the uniform | LO, chat (SYSTEMS §2) |
| the Friday kiss repeats | LO, 2026-10-08 |
| the job ask | SYSTEMS §2 (day 1) |
| inside Town | LO, 2026-10-08 (questions 43–45) |
| fix from the false-line sweep | sweep A1-20 (2026-10-08) |

## Changed 2026-11-02 (reader a3, `READER_FAILS_A3.md`, signed by LO 2026-11-02; DECISIONS 131)

- Row 43 (`cafe_coffee`, before she meets Tom): "Nobody here knows you. Taped inside the window, the STAFF WANTED card has a coffee ring on it."
