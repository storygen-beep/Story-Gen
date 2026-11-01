# [READY] Scene — ryan_02_phone_on_the_sink

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–113): Ryan's release-1 ladder (`sheets/people/npc_ryan.md`, signed). Changed: the gate drops Exhibitionism 20, the window starts 06:45, Want +5.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_ryan` · 2 (Ryan A 3) |
| where · when | the bathroom · weekdays 06:45–07:30, while he's in there (his bathroom row) |
| gate | his Want 10 · the drinks boost off (Exhibitionism 20 dropped: his meter is the lock) |
| want (test 1) | his eyes go to her and away too fast, every morning since step 1 |
| next step (test 2) | she learns his secret: Kayla, who sneaks in on Fridays |
| hook (test 3) | "Don't." She holds his secret; step 3 makes him pay for it |
| what she wears here (test 8) | a thin top: only in a group on "no bra"; otherwise no garment named |
| explicit? | no |
| her_line_low · her_line_high (rule 7) | low (under the stage): "This is Ryan. You should go." · high (over it): "You want him to hear Kayla on the phone while you do this." (the person sheet's pair; worded for this screen when the prose is written) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `sink` | she brushes her teeth; his phone buzzes: a text from Kayla | no | "Read it." → `read` · "Leave it." → the hall (parked) | none |
| `read` | he grabs the phone, too late | no | "Sneaking her in past Mom, huh?" → `secret` | `knows_about_kayla` set |
| `secret` | Ryan: "Don't." She smiles at him in the mirror | no | "Your secret's safe. For now." → the hall | Ryan's Want add +5 · `ryan_step` set 2 |

"Leave it." is the parked no: the step comes back the next weekday morning.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Ryan A 3 (heat 10-06) |
| the thin top in a group on her state | the truth rule · guess |
| `knows_about_kayla` causes his thread | the person sheet (LO, 2026-10-08) |
| the parked "Leave it." | guess |
