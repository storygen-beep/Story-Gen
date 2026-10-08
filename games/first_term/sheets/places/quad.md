# [READY] Place — Quad

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08 against the system sheets. Id `quad`.

| row | answer |
|---|---|
| kind | destination |
| ENTERED FROM (S2) | campus |
| labels — what kind of place | `zone:campus`, `outdoors`, `public` |
| hours | every day 07:00–22:00 |
| closed text | "The quad is dark and empty." |
| hidden until | no |
| fill — word budget (S3) | 2,500 words (ledger, unchanged) |
| door | no |
| dress code or wanted state | none |

## On entering

| auto-fires | who is here, and when | things to do alone | ways out |
|---|---|---|---|
| Zoe's meeting, first visit in her hours (`zoe_00_quad_meeting`) | Jake: Mon, Wed, Fri 08:30–11:45 | sit on the grass and hear what campus says | campus |
|  | Zoe: Tue, Thu, Fri 14:30–18:00 |  |  |

## Rows (`serves`)

| row | kind | system | cost and effect, with op (S4) | BRAKE (S9) | on a screen? |
|---|---|---|---|---|---|
| Jake | person | Jake's ladder | Jake B 2 here · his look (colour) | once per window, on the trigger | yes |
| Zoe | person | Zoe's ladder | her want shown first: her head in @player's lap | once per window, on the trigger | yes |
| sit on the grass | work | college · `campus_talk` | none · what she overhears reads `campus_talk` | none needed: it writes nothing | yes |

## Rows a gate needs

| row | gate |
|---|---|
| `campus_talk` read here | a meter is read |
| the grass at every hour | a destination is never open and exit-only |

## Why — the source of each key choice

| key choice | source |
|---|---|
| Zoe met here, week 1 | LO, 2026-10-08 (fix 1) |
| Jake's mornings, Zoe's afternoons | LIVES §3 |
| Zoe's leak on the quad | ARC_IDEAS, Zoe A step 0 |
| the grass row reads campus talk | LO, 2026-10-08 |
