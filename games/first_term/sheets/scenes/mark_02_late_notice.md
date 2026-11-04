# [READY] Scene — mark_02_late_notice
> Signed by LO: LO, 2026-11-04.

> Changed 2026-11-04 to match the build; signed by LO 2026-11-04. her_line row: what the build says; the paying and losing-count lines are gone (Q6). The want row says the table, not a count.

> Changed 2026-11-04 to match the build; signed by LO 2026-11-04. `put`: he waits for her to put it back (she hasn't yet); "Go back to bed." lands in her room.

> Changed 2026-11-03 to match the build (third alignment pass); signed by LO 2026-11-04. the second answer and its screen; the step row.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–115): Mark's release-1 ladder (`sheets/people/npc_mark.md`, signed). Changed: the gate is his step 1 done (his Want 10 dropped: his steps are paced by Sundays, a declared exception to taste rule 5); her voice row. The screens stand as built.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Every Mark step is written twice, by his Power: his terms (M) or hers (E).

| row | answer |
|---|---|
| person · step | `npc_mark` · 2 (Mark A 2) |
| where · when | the kitchen drawer, late · Sun–Fri 22:00–00:00, Mark next door |
| gate | `mark_step` eq 1 (was his Want 10) |
| want | his eyes on her hem at her first Sunday table |
| next step | she learns his weak spot: the debt to Vance |
| hook | "Put it back." Each of them now holds something |
| what she wears here | not named |
| explicit? | no: info |
| who notices | his secret is hers |
| what she risks | being caught reading it |
| her_line_low · her_line_high | low: none built · high, as built: her button "How late are we?" | The built thought on `put` ("He knows you know. You've got something on him now.") is the high side. |

## The step row (filled from the build, 2026-11-03)

**Kind · stage:** overhearing (Good Girl · Covered): his debt.

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| she finds Vance's late notice and hears Mark promise to pay | Mark, in the doorway, on the phone | being caught reading it | "Read it." | "Put it back." | not a sex act | she knows his debt; step 3 after a short week |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `drawer` | under the takeout menus, Vance's late notice | no | "Read it." → `phone` · "Shut the drawer." → the kitchen (parked) | none |
| `phone` | Mark in the doorway, on the phone: "Friday, Frank. I'll have it Friday." | no | "How late are we?" → `put` | `knows_mark_debt` set (on "Read it.") |
| `put` | "Put it back." | no | "Okay." → the kitchen · "No. I want to know how bad it is." → `put_no` | first: Mark's Want add +10 · `mark_step` set 2 |
| `put_no` | she won't put it back | no | "Go back to bed." → her room | `mark_step` set 2 · nothing of his |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene; Frank is Vance | the arc ideas, Mark A 2 · DIRECTION §6 |
| `knows_mark_debt` as a key | guess |
