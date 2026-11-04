# [READY] Scene — tom_03_the_tip_jar
> Signed by LO: LO, 2026-11-04.

> Changed 2026-11-03 to match the build (third alignment pass); signed by LO 2026-11-04.

> The signed plans behind this page: `proposals/COPY_FIXES_C.md`.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–116): Tom's release-1 ladder (`sheets/people/npc_tom.md`, signed). Changed: now his step 2 of 3; the gate is his step 1 and five shifts worked (Exhibitionism 20 and his Want 20 dropped); it pays his Want +5 (was +10) and Power −5; her voice row. The screens stand as built.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Tom's steps play inside a shift; her uniform is backed by the café's dress rule.

| row | answer |
|---|---|
| person · step | `npc_tom` · 2 of 3 (was 3, Tom B 3; the canvas id stays) |
| where · when | the back room · Mon–Sat 14:30–22:00 |
| gate | `cafe_job` · `tom_step` eq 1 · player counter `cafe_shifts_worked` gte 5 · the boost off |
| the counter | `cafe_shifts_worked` (player trait, declared 0): +1 on every "Work a shift". No counter exists today (`grep` of `build_scripts/`); name mine, confirmed by LO 2026-11-01 ("Signed") |
| want | he counts the jar when she's near |
| next step | she catches him folding the tips into his apron |
| hook | "Not a word." She holds his secret |
| what she wears here | the café uniform |
| explicit? | no: info |
| who notices | Tom's secret is hers |
| what she risks | being caught seeing it |
| her_line_low · her_line_high | low (under the stage): "He's your boss. Do the job." · high (over it): "You felt that second. So did he." (the person sheet names none; worded by me, signed by LO 2026-11-01) | The built thought on `seen` ("He's a thief. And now he owes you.") is the high side. |
| what changes after | `knows_tip_jar`; his line at the counter changes (`tom_01_the_apron.md`, his counter) |

## The step row (as built, 2026-11-03)

The seven columns, filled from what the build does.

**Kind · stage:** she sees what she shouldn't, an accident · stage 1 (no meter gate; five shifts worked)

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| the back room: Tom folding the bills out of the tip jar | only her: he steals from the jar | being caught seeing it | "Busy shift?" · or "That depends what's in it for me." | "Not a word." His ears go red | yes | his step 2; `knows_tip_jar`; his Want +5, Power -5 on "Not a word." |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`tom_03_the_tip_jar`** — Café · Mon/Tue/Wed/Thu/Fri/Sat 14:30-22:00 · Tom there · needs Tom's step = 1 · `cafe_job` · drinks boost off · Shifts worked 5+ · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `back` | Tom looks up from the till as you come in. | no | "Clock in." — 2 versions, by clothes → `jar` | — · varies: equip cafe uniform normal |
| `jar` | He counts the jar when you're near now, lips moving. | no | "Busy shift?" → `seen` | — |
| | | | "Walk past." → Café | back in 3 days |
| `seen` | He turns round with his hand still in the jar. | no | "Not a word." → Café | Tom's Want +5 · Tom's Power -5 · Tom's step = 2 · `tom_03_done` set · `knows_tip_jar` set |
| | | | "That depends what's in it for me." → `seen_no` | — |
| `seen_no` | He puts the lid back on the jar too hard, and he doesn't look at you … | no | "Back out front." → Café | Tom's step = 2 · `tom_03_done` set · `knows_tip_jar` set |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Tom B 3 · DIRECTION §6 (the tip jar, kept) |
| step 2, five shifts, Want +5 | `proposals/TOM_R1_LADDER.md` (signed 2026-11-01) |
