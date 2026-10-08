# [READY] Scene — ryan_03_shirt_off

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_ryan` · 3 (Ryan A 4) |
| where · when | his room · Mon, Tue, Thu, Sun 18:00–22:00 |
| gate | Corruption 20 · Exhibitionism 20 · his Want 20 · the boost off |
| want (test 1) | "Don't." He holds her look a beat longer since she read the text |
| next step (test 2) | she names a price for his secret, and he pays it |
| hook (test 3) | the code: two knocks, and he opens |
| what she wears here (test 8) | not named |
| explicit? | no: he shows, she looks; no body words on the list |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `door` | she knocks; he opens, wary: "If this is about Kayla—" | no | "It's about Kayla." → `price` · "Never mind." → the hall (parked) | none |
| `price` | her price: "You saw me. Shirt off." | no | "Turn around. Slowly." → `look` | none |
| `look` | the shirt over his head; the trail of hair under his navel; "Happy?" | no | "Two knocks. That's me." → the hall | Ryan's Want add +10 · corruption add +1 · `ryan_knock_code` set · `ryan_step` set 3 |

His parked no, if she comes on a Friday or he has a call: *"Kayla's coming over."*

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Ryan A 4 (heat 10-06) |
| Corruption +1, not +3 | LO, 2026-10-08 (ledger change 8) |
| `ryan_knock_code` opens "Two knocks" on his door | LO, 2026-10-08 (the door, question 12) |
| the "Never mind." no | guess |
