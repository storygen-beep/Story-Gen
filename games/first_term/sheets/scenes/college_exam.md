# [READY] Scene — college_exam

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. The midterm (`college_exam`): one choice inside the exam.

| row | answer |
|---|---|
| system · pool | college · `college_exam` |
| where · when | the lecture hall · midterms, weeks 7–8, once per exam |
| gate | Focus: none · the study guy: Curious · the flash: Exhibitionism 20 |
| who sees the flash | the cocky guy (21) only: a flash for one person she knows |
| what she wears here (test 8) | not named; "pull everything up" |
| BRAKE (S9) | once per exam |
| effects | the result reads `intelligence` + that grade · copying adds +5 to the grade (guess) |
| the crude-word ceiling | tits, nipples, ass, cock, wet, clit · no cunt, fuck, cum, pussy (LO, 2026-10-08) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `paper` | the exam paper, the proctor at the front | no | "Focus." · "Flirt with the study guy." · "Look at the cocky guy." → `price` | none |
| `price` | "Show me and I'll tilt my paper." | no | "Show him." → `flash` · "No." → `result` | none |
| `flash` | three seconds under the desk line; his paper slides to the edge | yes | "Copy." → `result` | exhibitionism add +1 · that grade add +5 (guess) |
| `result` | the band: failing, fine, top | no | → the hall | `exam_<subject>_<term>_done` set |

## The explicit screens, written

**`flash`** · 115 words · explicit words 5 (breast, nipple, tits) · median sentence 9 · stage 2

> "Show me and I'll tilt my paper." He breathes it without looking up. The proctor sits at the front, reading. Every head in the row is bent over a page. You check the room once. Then you pull everything up under the desk line, where only he can see. Your tits are bare in the cold hall air. Your nipples go hard at once, tight and aching. His pen stops mid-word. His eyes drop to your tits and stay there. One second. Two. Three. You yank everything down and cover your breasts. He slides his paper to the edge of his desk. Your nipples are still hard, and his stare is still on your chest.

No history words on any screen: each one repeats.

## Why — the source of each key choice

| key choice | source |
|---|---|
| one choice inside the exam; the cocky guy's price | LO, chat 2026-10-06 (SYSTEMS §1) |
| a flash for one person she knows at Curious | SP2 §1 |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| +5 for copying | guess |
