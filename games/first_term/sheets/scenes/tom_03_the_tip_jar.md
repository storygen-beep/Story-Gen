# [READY] Scene — tom_03_the_tip_jar

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–116): Tom's release-1 ladder (`sheets/people/npc_tom.md`, signed). Changed: now his step 2 of 3; the gate is his step 1 and five shifts worked (Exhibitionism 20 and his Want 20 dropped); it pays his Want +5 (was +10) and Power −5; her voice row. The screens stand as built.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Tom's steps play inside a shift; her uniform is backed by the café's dress rule.

| row | answer |
|---|---|
| person · step | `npc_tom` · 2 of 3 (was 3, Tom B 3; the canvas id stays) |
| where · when | the back room · Mon–Sat 14:30–22:00 |
| gate | `cafe_job` · `tom_step` eq 1 · player counter `cafe_shifts_worked` gte 5 · the boost off |
| the counter | `cafe_shifts_worked` (player trait, declared 0): +1 on every "Work a shift". No counter exists today (`grep` of `build_scripts/`); name mine, confirmed by LO 2026-11-01 ("Signed") |
| want (test 1) | he counts the jar when she's near |
| next step (test 2) | she catches him stealing: leverage |
| hook (test 3) | "Not a word." She holds his secret; it's her lever in a later release ("half is mine", later) |
| what she wears here (test 8) | the café uniform |
| explicit? | no: info |
| who notices | Tom's secret is hers |
| what she risks | being caught seeing it |
| her_line_low · her_line_high (rule 7) | low (under the stage): "He's your boss. Do the job." · high (over it): "You felt that second. So did he." (the person sheet names none; worded by me, signed by LO 2026-11-01) | The built thought on `seen` ("He's a thief. And now he owes you.") is the high side. |
| what changes after | `knows_tip_jar`; his line at the counter changes (`tom_01_the_apron.md`, his counter) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `jar` | she sees Tom fold twenties from the tip jar into his apron | no | "Busy night?" → `seen` · walk past → the shift (parked) | none |
| `seen` | he sees her see it: "Not a word." | no | "Not a word." → the shift | Tom's Want add +5 · Tom's Power add −5 · `tom_step` set 2 · `tom_03_done` set · `knows_tip_jar` set |

**The built first line** ("He counts the jar when you're near now, lips moving.") stays: his counter shows that line
at `tom_step` eq 1, so it is true when this step can fire.

**The parked no** (walk past): as built, the step waits 3 days.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Tom B 3 · DIRECTION §6 (the tip jar, kept) |
| step 2, five shifts, Want +5 | `proposals/TOM_R1_LADDER.md` (signed 2026-11-01) |
