# [READY] Scene — zoe_00_quad_meeting

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08 (fix 1). Zoe's meeting: nothing set `zoe_met` before, so her
> apartment, the parties, Zoe A 1 and Jake B 1 could never open.

| row | answer |
|---|---|
| person · step | `npc_zoe` · her meeting (a one-time scene, not a ladder step) |
| where · when | the quad · Tue, Thu, Fri 14:30–18:00 (her row), the first time she's there |
| gate | `zoe_met` is false · Zoe's schedule window (the meeting fires where she is) |
| priority | high: it fires before her hub can show |
| want (test 1) | she picks @player out: someone to drag to her party |
| next step (test 2) | her name, her number, and Friday |
| hook (test 3) | "Friday. My place. Wear something short." (her thread, then Zoe A 1) |
| what she wears here (test 8) | not named |
| explicit? | no |
| role before name | "the girl from Biology", then "Zoe" once she says it |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `wave` | the girl from Biology waves from the grass: "Hey. You. Sit." | no | "Sit with her." → `zoe` · "Can't, I've got a shift." → `later` | none |
| `zoe` | "Zoe." She talks fast, looks at @player too long, laughs | no | "Party?" → `friday` | `zoe_met` set |
| `friday` | "Friday. My place. Wear something short." She takes her phone, types her number | no | "Friday." → the quad | `zoe_number` set |
| `later` | "Fine, run. Friday, my place!" She shouts the address after her | no | → campus | `zoe_met` set · `zoe_number` set |

Both answers meet her: the meeting refuses nothing (the first hour's rule), and "Can't" still gets the invite.

## The nudges, so she isn't missed

| where | what | sets |
|---|---|---|
| Biology, Mon 13:00 and Tue 10:15 | the girl beside her whispers through the slides: "Quad after?" | nothing |
| Story Goals card, from day 2, while `zoe_met` is false | "Someone from your Biology class hangs out on the quad in the afternoons." | nothing |

## Why — the source of each key choice

| key choice | source |
|---|---|
| met on the quad in week 1 | LIVES §6 · LO, 2026-10-08 (fix 1) |
| her quad hours | LIVES §3 (Tue, Thu, Fri afternoons) |
| the meeting fires in her window | `the-first-hour.md` F5 (a meeting fires where they are) |
| her seat in Biology | LO, chat 2026-10-07 (SYSTEMS, seating) |
| the nudges, the lines, `zoe_number` | guess |
