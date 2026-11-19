# [READY] Scene — tom_06_after_close_kiss

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Tom's steps play inside a shift; her uniform is backed by the café's dress rule.

| row | answer |
|---|---|
| person · step | `npc_tom` · 6 (Tom B 6) · his last step in 0.1 |
| where · when | the café, blinds down, after close · Friday 22:00–23:00 (his ask is "Stay late Friday?") |
| gate | `cafe_job` · Corruption 40 · Exhibitionism 20 · his Want 50 |
| want (test 1) | "Stay late Friday?" since she named her terms |
| next step (test 2) | the first kiss, after close, and a regular sees |
| hook (test 3) | "We're closed." Friday close, again |
| what she wears here (test 8) | the café uniform |
| explicit? | no: a kiss (under 3 list words) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `blinds` | he reties her apron; his hands stay on her hips | no | "Don't stop." → `kiss` · "Night, Tom." → the street (parked) | none |
| `kiss` | he backs her into the espresso machine and kisses her, the steam wand hot | no | → `glass` | corruption add +3 · Tom's Want add +10 |
| `glass` | a late regular taps the glass; they don't break: "We're closed." | no | "Goodnight." → the street | `tom_step` set 6 |

## The repeat it turns into — the kiss after close (`tom_after_close`, one sheet row)

| row | answer |
|---|---|
| where · when | the café after close, Friday only, 22:00–23:00 |
| what happens | the blinds down, his hands on her hips, the kiss by the machine |
| explicit? | no in 0.1; steps 7–9 wait for his rewrite |
| BRAKE (S9) | once a week, Friday, on the trigger |
| his thread | after step 6: "Stay after close." every Friday, 12:00–18:00 |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Tom B 6 (fixed 10-06: Bold) |
| the Friday repeat | LO, 2026-10-08 (question 2) |
| `tom_after_close` as an id | guess |
| fix from the false-line sweep | sweep A3-30 (2026-10-08) |
