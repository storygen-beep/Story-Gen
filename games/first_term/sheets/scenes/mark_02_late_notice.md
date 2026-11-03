# [READY] Scene — mark_02_late_notice

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–115): Mark's release-1 ladder (`sheets/people/npc_mark.md`, signed). Changed: the gate is his step 1 done (his Want 10 dropped: his steps are paced by Sundays, a declared exception to taste rule 5); her voice row. The screens stand as built.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Every Mark step is written twice, by his Power: his terms (M) or hers (E).

| row | answer |
|---|---|
| person · step | `npc_mark` · 2 (Mark A 2) |
| where · when | the kitchen drawer, late · Sun–Fri 22:00–00:00, Mark next door |
| gate | `mark_step` eq 1 (was his Want 10) |
| want | his eyes on her hem at the first count |
| next step | she learns his weak spot: the debt to Vance |
| hook | "Put it back." Each of them now holds something |
| what she wears here | not named |
| explicit? | no: info |
| who notices | his secret is hers |
| what she risks | being caught reading it |
| her_line_low · her_line_high | low (under the stage): "He's Mom's husband. Pay him and go." · high (over it): "You want him to lose count." (the person sheet names none; worded by me, signed by LO 2026-11-01) | The built thought on `put` ("You've got something on him now.") is the high side. |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `drawer` | under the takeout menus, Vance's late notice | no | "Read it." → `phone` · "Shut the drawer." → the kitchen (parked) | none |
| `phone` | Mark in the doorway, on the phone: "Friday, Frank. I'll have it Friday." | no | "How late are we?" → `put` | `knows_mark_debt` set |
| `put` | "Put it back." | no | "Okay." → the kitchen | Mark's Want add +10 · `mark_step` set 2 |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene; Frank is Vance | the arc ideas, Mark A 2 · DIRECTION §6 |
| `knows_mark_debt` as a key | guess |
