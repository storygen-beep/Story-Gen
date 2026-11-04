# [REVIEW] Scene — ryan_02_phone_on_the_sink

> Changed 2026-11-04 to match the build; waits for LO's re-sign. Kayla's voice note: "after everyone's asleep" cut.

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. "That depends." and its screen; Kayla is met here; the step row.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–113): Ryan's release-1 ladder (`sheets/people/npc_ryan.md`, signed). Changed: the gate drops Exhibitionism 20, the window starts 06:45, Want +5.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_ryan` · 2 (Ryan A 3) |
| where · when | the bathroom · weekdays 06:45–07:30, while he's in there (his bathroom row) |
| gate | his Want 10 · the drinks boost off (Exhibitionism 20 dropped: his meter is the lock) |
| want | his eyes go to her and away too fast, every morning since step 1 |
| next step | she learns his secret: Kayla, who sneaks in on Fridays |
| hook | "Don't." She holds his secret; step 3 makes him pay for it |
| what she wears here | a thin top: only in a group on "no bra"; otherwise no garment named |
| explicit? | no |
| her_line_low · her_line_high | low (under the stage): "This is Ryan. You should go." · high (over it): "You want him to hear Kayla on the phone while you do this." (the person sheet's pair; worded for this screen when the prose is written) |

## The step row (filled from the build, 2026-11-03)

**Kind · stage:** overhearing a secret (Good Girl · Covered).

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| she reads Kayla on his phone and holds his secret | Ryan; Kayla, by her text and voice note | empty on purpose: nothing of hers is at stake yet | "Your secret's safe. For now." | he grabs for the phone: "Don't." | not a sex act | she knows about Kayla; step 3 makes him pay for it |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `sink` | she brushes her teeth; his phone buzzes: a text from Kayla | no | "Read it." → `read` · "Leave it." → the hall (parked) | none |
| `read` | he grabs the phone, too late; a voice note from Kayla plays | no | "Sneaking her in past Mom, huh?" → `secret` | `knows_about_kayla` set · `kayla_met` set (on "Read it.") |
| `secret` | Ryan: "Don't." She smiles at him in the mirror | no | "Your secret's safe. For now." → the hall · "That depends." → `depends` | first: Ryan's Want add +5 · `ryan_step` set 2 |
| `depends` | she leaves him guessing | no | "Leave him dripping." → the hall | `ryan_step` set 2 · nothing of his |

"Leave it." is the parked no: the step comes back the next weekday morning.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Ryan A 3 (heat 10-06) |
| the thin top in a group on her state | the truth rule · guess |
| `knows_about_kayla` causes his thread | the person sheet (LO, 2026-10-08) |
| the parked "Leave it." | guess |
