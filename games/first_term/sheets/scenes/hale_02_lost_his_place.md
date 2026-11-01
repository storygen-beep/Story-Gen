# [READY] Scene — hale_02_lost_his_place

> **Changed 2026-11-01 after the build, signed by LO 2026-11-01 ("Signed, build them")** (the reader's FAILs; LO's picks in chat): a no in any clothes, not only a skirt.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–117): Hale's release-1 ladder (`sheets/people/npc_hale.md`, signed). Changed: the gate is Daring only (Exhibitionism 20; Corruption 20 dropped) and his step 1; her voice row. The screens stand as built.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_hale` · 2 (Hale B 2) |
| where · when | the lecture hall · Mon, Wed, Fri 08:30–10:00 |
| gate | Exhibitionism 20 (Daring) · Hale's step counter eq 1 · the boost off |
| want (test 1) | his eyes on the front row, every class since the pen |
| next step (test 2) | her chosen flash, for one person she knows |
| hook (test 3) | "Thursday, after six." His office (step 3) |
| what she wears here (test 8) | no panties: the step's own choice, Daring, this step only (LO, 2026-10-08) |
| explicit? | no: a flash under her stage's words |
| crude words | Hale's early column: legs, ass (stage 2) |
| who notices | Hale; the guy beside her |
| what she risks | being seen by the row |
| her_line_low · her_line_high (rule 7) | low: "He's your professor. He's married." · high: "You want to know what he'd do next." (the person sheet's pair) | |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `legs` | front row (her seat since step 1); she doesn't fix her skirt; he looks | no | "Uncross your legs, slowly." → `flash` · "Fix your skirt." → the class (parked) | none |
| `flash` | he sees she's wearing nothing under it; he loses the sentence; three rows hear | no | "You lost your place, Dr. Hale." → `after` | exhibitionism add +3 |
| `after` | after class, his no: "Not here. Office hours." — "When?" — "Thursday, after six." | no | "Thursday." → campus | Hale's step counter set 2 · `hale_02_done` set |

`hale_02_done` causes his college email (his thread). His no is parked: the hour still comes.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Hale B 2 (heat 10-06) |
| no panties at Daring, this step only | LO, 2026-10-08 (question 18) |

## Changed after the build (2026-11-01), signed by LO 2026-11-01

| node | the no (new, when she isn't in a skirt) | the reply (mine, signed by LO 2026-11-01) |
|---|---|---|
| `legs` | "Sit up straight." | "You sit up straight and keep your eyes on your notes. Dr. Hale finds his place, and doesn't look at the front row again until the end." The step waits two days, as "Fix your skirt." does. |
