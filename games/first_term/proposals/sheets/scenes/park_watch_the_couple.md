# [REVIEW] Scene — park_watch_the_couple

> A draft for LO to place. Written 2026-10-08. The first explicit scene (LO, 2026-10-08): strangers, an accident at stage 1. A walk event in the park.

| row | answer |
|---|---|
| system · pool | the park · `park_watch_the_couple` |
| where · when | the park, on a walk · 07:00–22:00 |
| gate | stage 1: none · stage 2 adds "Stay and watch." |
| who | two strangers, adults, in the bushes; they never learn who she is |
| what she wears here (test 8) | not named |
| BRAKE (S9) | once a day, on the walk's trigger |
| raises | stage 1: none · stage 2: corruption add +1 until she is past Curious |
| the crude-word ceiling | tits, nipples, ass, cock, wet, clit · no cunt, fuck, cum, pussy (LO, 2026-10-08) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `sound` | a sound off the path; she steps off to look | no | → `run` (Good Girl) · or "Stay and watch." → `watch` (Curious) | none |
| `run` | she walks into them, sees all of it; he looks up; she runs | yes | "Keep walking." → the park | `saw_the_couple` set |
| `watch` | hidden behind a rhododendron, she watches them, her hand flat on her stomach | yes | "Leave before they see." · "Touch yourself while you watch." → `touch` | corruption add +1 |
| `touch` | she touches herself as she watches, and comes with him | yes | "Slip away." → the park | corruption add +1 |

Touching herself while she watches is at Curious (SP2 §1: "watching, then touching herself while she watches").

## The explicit screens, written

**`run`** · 126 words · explicit words 7 (ass, cock, moan, naked, thrust, tits) · median sentence 11 · stage 1, the first explicit beat

> A sound comes from behind the bushes, low and wet and steady. You step off the path to look, straight into them. A man and a woman, both naked from the waist down, and they don't see you. She is bent over a fallen log, palms flat on the bark. He holds her hips from behind. His cock slides out of her, slick, then drives back in. Her tits swing under her with every thrust. His hand comes down on her ass and stays there, squeezing hard. She moans, loud, mouth open. You stare a second too long, and your face goes hot. Then he looks up, straight at you, still buried in her. You run, heart slamming, legs shaking, her moan still going behind you.

**`watch`** · 129 words · explicit words 11 (ass, cock, moan, nipple, thrust, tits) · median sentence 12 · stage 2

> You crouch behind the rhododendron and part the leaves. A man has a woman bent against a tree, her palms flat on the bark. His cock slides out of her, slick and shining, then thrusts back in to the root. Every thrust makes a wet slap you can hear from here. He fills his hands with her tits and pinches her nipples hard. She moans loud, bites her lip, but can't hold the next one in. Her face is red, eyes shut, mouth hanging open. You stare at his cock. Your nipples go tight, and heat floods between your thighs. You press your hand flat on your stomach and keep it there. He drags her ass back onto his cock, faster, until her moans break into short, wet gasps.

**`touch`** · 128 words · explicit words 9 (ass, clit, cock, moan, nipple, thrust, tits) · median sentence 10 · stage 2

> Behind the rhododendron, you can see everything. The man has the woman pinned to the tree, a hand full of each of her tits. His cock drives into her, hard and steady, and she moans on every stroke. Your hand slides down your belly and inside. Your fingers find your clit, and you are already wet. You match him. Each time he thrusts, you rub, fast and tight. Her nipples stand stiff between his fingers while her ass slaps the bark. You bite your lip so no sound gets out. Neither of them looks toward the bush. He groans and buries his cock deep, and you come with him. Your knees buckle, and your free hand grips a branch while your fingers keep working your clit through it.

No history words on any screen: each one repeats.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the park couple, the first explicit scene | LO, 2026-10-08 (question 8) |
| an accident at Good Girl, watching at Curious | SP2 §1 |
| touching herself while she watches, at Curious | SP2 §1 |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
