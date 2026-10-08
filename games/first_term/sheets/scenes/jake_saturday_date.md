# [READY] Scene — jake_saturday_date

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. The repeat Jake's steps turn into: the Saturday date, booked on his
> thread, ending at the front door.

| row | answer |
|---|---|
| person | `npc_jake` · the repeat after Jake B 4 (= Laura C 5) |
| where · when | the front door · Saturday 22:00–00:00 (his gated row) |
| gate | `jake_date_booked` · Jake B 4 done |
| booked by | his thread, Thursday 18:00–22:00: "Saturday?" · reminder: quest card, his quad hub line |
| what she wears here (test 8) | Laura's dress line only in a group on `laura_blue_dress` worn |
| explicit? | no in 0.1: kisses and his hands; his sex step (B 5) is later |
| BRAKE (S9) | once a week: the booking flag, cleared at the door |
| raises | corruption add +1, until she is past Bold (repeat raise) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `door` | the goodnight at the door, by her stage | no | "Kiss him." → `watch` · "Goodnight, Jake." → in | `jake_date_booked` set false |
| `watch` | who's watching: Laura from the dark couch (after C 5), or Ryan coming in | no | "Let them look." → in | corruption add +1 |

**By her stage:** Curious, a long kiss on the porch rail · Bold, his hands under her skirt line only if she wears one (a
group), her turning him so the dark room can see. Hungry is later and shows locked: *"Needs Hungry."*

**Who notices**, rotating by who is home: Laura on the dark couch (Saturday 22:00–00:00, her row), or Ryan home late.

## Why — the source of each key choice

| key choice | source |
|---|---|
| dating is Jake's loop, booked on his thread | LO, 2026-10-07 (SYSTEMS §12) |
| the door, Laura and Ryan watching | the arc ideas, Jake B After |
| no explicit beat in 0.1 | guess: his sex step, B 5, is later |
| `jake_saturday_date` as an id | guess |
