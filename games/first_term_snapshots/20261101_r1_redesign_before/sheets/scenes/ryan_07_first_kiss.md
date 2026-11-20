# [READY] Scene — ryan_07_first_kiss

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_ryan` · 7 (Ryan A 8) |
| where · when | his room · Mon, Tue, Thu, Sun 18:00–22:00, after two knocks |
| gate | Corruption 40 · his Want 60 · the boost off |
| want (test 1) | since the shower he leaves his door open a hand's width |
| next step (test 2) | the first kiss, and she starts it |
| hook (test 3) | his no, "I've got a girlfriend", and what she gets instead (step 8) |
| what she wears here (test 8) | not named |
| explicit? | yes: the kiss screen (heat call A), no new act |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `knocks` | two knocks; he opens; neither sits down | no | "Kiss him." → `kiss` · "Goodnight, Ryan." → the hall (parked) | none |
| `kiss` | she kisses him first; his hands on her ass; his cock hard against her | yes (8 words) | "Don't stop." → `text` | none |
| `text` | Kayla's text lights his phone; she turns it face-down | no | "Ignore it." → `his_no` | corruption add +3 · Ryan's Want add +10 |
| `his_no` | "@player.nickname — I've got a girlfriend." | no | "Then think about it." → the hall | `ryan_step` set 7 |

His no is parked: he still opens to two knocks, and the kiss waits a few nights.

## The explicit screen, written

**`kiss`** · 88 words · explicit words 8 (ass, cock, kiss, nipple, tits) · median sentence 7 · Ryan's middle column

> You kiss him first. Ryan goes still for one second, but then his mouth opens hot on yours. His hands drop to your ass. He pulls you in hard against him. His cock is rigid through his jeans, pressed right where you want it. Your tits flatten on his chest. Your nipples go tight. "@player.nickname," he says into the kiss, and his breath comes ragged in your mouth. You are wet already. You grind your hips into his cock, slow, until his fingers dig deeper into your ass.

*The last sentence:* her hips, his cock, his fingers on her ass. On the body; not a pivot.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene, his no | the arc ideas, Ryan A 8 · SP2 (his no) |
| a kiss at Bold | SP2 §1 (LO, 2026-10-06) |
| the kiss lifted to 3+ list words, no new act | LO, 2026-10-08 (heat call A) · `v2-prose`, measured |
