# [REVIEW] Scene — laura_05_jake_at_the_door

> A draft for LO to place. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_laura` · 5 (Laura C 5) = `npc_jake` · 4 (Jake B 4): one canvas |
| where · when | the front door, seen from the dark living room · Saturday 22:30–00:00 |
| gate | stage 3 on both meters, her Want 40, Jake B 3, a date |
| want (test 1) | Laura: "Is Jake bringing you home?" · Jake: "Is your mom up?" |
| next step (test 2) | she uses Jake's goodnight on the one watching from the dark |
| hook (test 3) | "Was he any good?" — "Better in your dress." |
| what she wears here (test 8) | Laura's dress: only in a group on `laura_blue_dress` worn |
| explicit? | yes: the doorstep screen (heat call A), no new act |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `porch` | Jake walks her to the door: "Everyone was looking at you tonight." | no | "Kiss me." → `kiss` · "Goodnight, Jake." → in (parked) | none |
| `kiss` | his hands on her ass under the dress; Laura in the dark window | yes (6 words) | "Higher. Don't stop." → `couch` | `jake_date_booked` set false |
| `couch` | inside: Laura's hand at her own throat: "Was he any good?" | no | "Better in your dress." → the hall | Laura's Want add +10 · `laura_step` set 5 · `jake_step` set 4 |

Both counters read this canvas, and it sets both (LO, 2026-10-08). Jake never learns Laura was watching.

## The explicit screen, written

**`kiss`** · 110 words · explicit words 6 (ass, cock, kiss, tits) · median sentence 11 · Jake's and Laura's middle columns

> Jake kisses you on the doorstep, hard, with his mouth open. His hands slide down your back and under the hem of your mother's dress. They close on your ass and pull your hips into his. His cock is hard behind his jeans, pressed right against you. Your tits flatten on his chest. "Everyone was looking at you tonight," he says into your mouth. You turn him slowly, until the dark living-room window can see you both. In the glass, Laura's shape stands still, her hand at her own throat. "Higher," you tell him. "Don't stop." His hands squeeze higher on your ass, and his cock grinds into your hips.

*The last sentence:* his hands on her ass, his cock against her hips. On the body; not a pivot.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the shared step | LO, 2026-10-06 (DIRECTION §6) · SP3 (LO, 2026-10-08) |
| the scene and its lines | the arc ideas, Laura C 5 and Jake B 4 |
| the dress in a group | the truth rule |
| the kiss lifted to 3+ list words, no new act | LO, 2026-10-08 (heat call A) · `v2-prose`, measured |
