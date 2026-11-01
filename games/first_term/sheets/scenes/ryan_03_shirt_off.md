# [READY] Scene — ryan_03_shirt_off

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–113): Ryan's release-1 ladder (`sheets/people/npc_ryan.md`, signed). Changed: gate Corruption 20 · his Want 20 (Exhibitionism 20 dropped); Laura calls up the stairs while he strips (the risk); Want +5.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_ryan` · 3 (Ryan A 4) |
| where · when | his room · Mon, Tue, Thu, Sun 18:00–22:00 |
| gate | Corruption 20 · his Want 20 · the boost off |
| want (test 1) | "Don't." He holds her look a beat longer since she read the text |
| next step (test 2) | she names a price for his secret, and he pays it |
| hook (test 3) | the code: two knocks, and he opens |
| who notices | Laura, nearly: her call up the stairs (the step's new risk) |
| what she wears here (test 8) | not named |
| explicit? | no: he shows, she looks; no body words on the list |
| her_line_low · her_line_high (rule 7) | low (under the stage): "This is Ryan. You should go." · high (over it): "You want him to hear Kayla on the phone while you do this." (the person sheet's pair; worded for this screen when the prose is written) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `door` | she knocks; he opens, wary: "If this is about Kayla—" | no | "It's about Kayla." → `price` · "Never mind." → the hall (parked) | none |
| `price` | her price: "You saw me. Shirt off." | no | "Turn around. Slowly." → `look` | none |
| `look` | the shirt over his head; he turns on her order; Laura calls up the stairs, "Ryan, is your sister in there?"; he answers "No" without taking his eyes off her; "Happy?" | no | "Two knocks. That's me." → the hall | Ryan's Want add +5 · corruption add +1 · `ryan_knock_code` set · `ryan_step` set 3 |

His parked no, if she comes on a Friday or he has a call: *"Kayla's coming over."*

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Ryan A 4 (heat 10-06) |
| Corruption +1, not +3 | LO, 2026-10-08 (ledger change 8) |
| `ryan_knock_code` opens "Two knocks" on his door | LO, 2026-10-08 (the door, question 12) |
| the "Never mind." no | guess |
