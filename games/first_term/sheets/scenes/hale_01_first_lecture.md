# [READY] Scene — hale_01_first_lecture

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_hale` · 1 (Hale B 1) · meets Hale and Nadia |
| where · when | the lecture hall · Monday 08:30–10:00, day 1 (his window) |
| gate | none: the first class |
| want (test 1) | none before: step 1. Hard behind the lectern, he doesn't look away |
| next step (test 2) | an accident: the dropped pen, and his eyes |
| hook (test 3) | Nadia: "Last spring it was me." His history, his wife's Thursdays |
| what she wears here (test 8) | a skirt line only in a group on her short-skirt state |
| her stage here | Good Girl: an accident, not a choice |
| explicit? | no |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `front_row` | the front row; the man at the lectern; a girl saves her the seat | no | "Sit." → `pen` | `hale_met` and `nadia_met` set |
| `pen` | she bends for a dropped pen; she looks up and he's hard behind the lectern | no | "Did he just—?" → `nadia` · "Look away." → `nadia` | Hale's step counter set 1 |
| `nadia` | Nadia: "He does that. Last spring it was me." His wife, Thursdays | no | "After class." → campus | none |

Role before name: "the man at the lectern", then "Dr. Hale"; "the girl beside you", then "Nadia".

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Hale B 1 (heat 10-06) |
| met at the first lecture, day 1 | LIVES §6 |
| the opening card points here | LO, 2026-10-08 (question 26) |
