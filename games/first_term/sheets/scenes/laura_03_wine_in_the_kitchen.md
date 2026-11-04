# [REVIEW] Scene — laura_03_wine_in_the_kitchen

> Changed 2026-11-04 to match the build; waits for LO's re-sign. `no`: "Say goodnight and go." as built (Q7).

> Changed 2026-11-04 to match the build; waits for LO's re-sign. `no`: she puts the empty glass back (only hers was poured).

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. the parked no's own screen; the step row.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Go ahead")** (DECISIONS 99–114): Laura's release-1 ladder (`sheets/people/npc_laura.md`, signed). Changed: now her step 2 of 4; the gate is her Love 10 only (Corruption 20, Exhibitionism 20 and Want 20 dropped); it pays Love +5 and sets `laura_step` 2; voice rows added. The screens and lines stand as built.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_laura` · 2 of 4 (was 3, Laura C 3; the canvas id stays) |
| where · when | the kitchen · Mon, Tue, Thu, Fri 20:00–22:00 (not Sunday: Mark is at the table) |
| gate | her Love (`warmth`) 10 · `laura_step` eq 1 · the boost off |
| want | she keeps a glass poured for two (the leak) |
| next step | her secret: at 19 she snuck out in her mother's dress |
| hook | "Like you get looked at." She wants to be looked at too |
| what she wears here | not named |
| explicit? | no: a talk |
| who notices | Laura's secret is Ella's |
| her_line_low · her_line_high | low: "That's your mom. Go to bed." · high: "She's lonely, and you can't stop watching her be lonely." The built thought on `mark` ("She wants somebody to look at her. She's telling you.") is the high side; the low line goes on the parked no ("I'm tired, Mom.") |
| what changes after | Ella knows she's lonely |

## The step row (filled from the build, 2026-11-03)

**Kind · stage:** a secret told (Good Girl · Covered): she hears her mother's want.

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| Laura, on wine, tells her secret and says Mark doesn't look at her | Laura and Ella, alone | empty on purpose: a talk, nothing of hers at stake | "Pour me one." | Laura: "Mark hasn't looked at my body like that since the wedding." | not a sex act | Love +5; her bedroom gap and shower gap open |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `glass` | Laura with wine, her robe open at the collar: "Sit with me." | no | "Pour me one." → `story` · "I'm tired, Mom." → `no` (parked) | none |
| `story` | at 19 she snuck out in her own mother's dress, home at dawn (no clock hour); "Like you get looked at." (the promise) | no | "Mom!" → `mark` | none |
| `mark` | "Mark hasn't looked at my body like that since the wedding." | no | "He should." → the hall | Laura's Love add +5 · `laura_step` set 2 · `laura_03_done` set |
| `no` | the parked no | no | "Say goodnight and go." → the hall | Laura's Love add −1 |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Laura C 3 (heat 10-06) |
| Laura snuck out at 19 | DIRECTION §6 (kept, LO 10-06) |
| fix from the false-line sweep | sweep A2-05, A2-40 (2026-10-08) |
| step 2, gate Love 10, Love +5 | `proposals/LAURA_R1_LADDER.md`, the ladder (signed 2026-11-01) |

**The parked no** ("I'm tired, Mom."): as built, Love −1, the step waits a day.
