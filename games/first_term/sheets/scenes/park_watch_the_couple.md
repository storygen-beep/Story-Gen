# [READY] Scene — park_watch_the_couple
> Signed by LO: LO, 2026-11-04.

> Changed 2026-11-04 to match the build; signed by LO 2026-11-04. Touching pays +1, not +2.

> Changed 2026-11-03 to match the build (third alignment pass); signed by LO 2026-11-04.

> The signed plans behind this page: `proposals/COPY_FIXES_C.md`.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08). Re-signed 2026-10-29 ("sign all", in chat).

> **Changed 2026-10-29, re-signed by LO 2026-10-29** (DECISIONS 79): a `linger` screen at Good Girl; `run` now ends before he looks up. The old page is in the 20261029_good_girl_before snapshot. **Changed again 2026-10-29** (LO's yes to reader item 5): the walk starts only until 21:30.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. The first explicit scene (LO, 2026-10-08): strangers, an accident at stage 1. A walk event in the park.

| row | answer |
|---|---|
| system · pool | the park · `park_watch_the_couple` |
| where · when | the park, on a walk · starts 07:00–21:30, so every exit (at most 21 minutes) lands before the gates lock at 22:00 (LO, 2026-10-29, reader item 5) |
| gate | Corruption under 20: "Step off the path to look." · Corruption 20: "Stay and watch." |
| who | two strangers, adults, in the bushes; they never learn who she is |
| what she wears here | not named |
| BRAKE | once a day, on the walk's trigger |
| raises | "Look a second longer.": +1 (cap 19) · "Stay and watch.": +1 (cap 39) · touching: +1 (cap 39) |
| the crude-word ceiling | tits, nipples, ass, cock, wet, clit · no cunt, fuck, cum, pussy (LO, 2026-10-08) |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`park_watch_the_couple`** — Park · needs `opening_done` · 07:00-21:30 · repeatable · 1 a day

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `sound` | The far path behind the rhododendrons is empty and quiet. | no | "Step off the path to look." (Corruption under 20) → `run` | — |
| | | | "Stay and watch." (Corruption 20+) → `watch` | — |
| | | | "Walk the other way." → `away` | — |
| `run` | A sound comes from behind the bushes, low and wet and steady. | yes | "Look a second longer." → `linger` | `saw_the_couple` set |
| | | | "Run." → Park | `saw_the_couple` set |
| `linger` | You stay. | yes | "Keep walking." → Park | Corruption +1 (cap 19) · `saw_the_couple` set |
| `watch` | Behind you on the path a jogger thuds past. | yes | "Leave before they see." → Park | Corruption +1 (cap 39) · `saw_the_couple` set |
| | | | "Touch yourself while you watch." → `touch` | — |
| `touch` | A dog barks somewhere along the path, and you freeze with your hand on your belly, … | yes | "Slip away." → Park | Corruption +1 (cap 39) · `saw_the_couple` set |
| `away` | You turn round and walk the other way, fast, and don't look back, but your face … | no | "Back to the pond." → Park | — |

## The explicit beats, as built (2026-11-03)

Every screen the build counts as explicit (3+ words from the frozen list), word for word, with its measurement. It replaces the drafted text.

**`park_watch_the_couple` · `run`** — 125 words · 8 counted: naked, cock, tits, thrust, ass, moan, cock, fuck · ceiling: strangers' words (DECISIONS 41): tits, nipples, ass, cock, wet, clit · **past the ceiling: fuck**

> A sound comes from behind the bushes, low and wet and steady. You step off the path to look, straight into them. A man and a woman, both naked from the waist down, and they don't see you. She is bent over a fallen log, palms flat on the bark. He holds her hips from behind. His cock slides out of her, slick, then drives back in. Her tits swing under her with every thrust. His hand comes down on her ass and stays there, squeezing hard. You stare a second too long, and your face goes hot. She moans, loud, mouth open, his cock still driving into her.
>
> Oh God. Harder. Don't you dare stop.
>
> Fuck, you're so wet. Somebody's going to hear you.

**`park_watch_the_couple` · `linger`** — 138 words · 6 counted: naked, cock, tits, moan, ass, nipple · ceiling: strangers' words (DECISIONS 41): tits, nipples, ass, cock, wet, clit

> You stay. You make yourself look. The man is naked from the waist down, and his cock is thick and shining wet. He pulls almost all the way out of her, then drives back in. The woman is bent over the log with her tits swinging under her. She moans every time he hits bottom. His hands grip her ass hard enough to leave marks. Your nipples go tight and ache. Heat pours down your belly, and you are wet, so wet it shocks you. Then the man looks up. He stares straight at you, still buried deep inside her. You run. Your legs shake under you. Your heart slams against your ribs. Your thighs slide together, slick, with every step.
>
> Behind you, the man laughs.
>
> Come back! She likes being watched!
>
> Don't, Dan. Oh God, don't stop.

**`park_watch_the_couple` · `watch`** — 165 words · 14 counted: cock, thrust, thrust, tits, nipple, moan, cock, nipple, ass, cock, moan, cock, moan, fuck · ceiling: strangers' words (DECISIONS 41): tits, nipples, ass, cock, wet, clit · **past the ceiling: fuck**

> Behind you on the path a jogger thuds past. You hold your breath until he's gone.
>
> You crouch behind the rhododendron and part the leaves. A man has a woman bent against a tree, her palms flat on the bark. His cock slides out of her, slick and shining, then thrusts back in to the root. Every thrust makes a wet slap you can hear from here. He fills his hands with her tits and pinches her nipples hard. She moans loud, bites her lip, but can't hold the next one in. Her face is red, eyes shut, mouth hanging open. You stare at his cock. Your nipples go tight, and heat floods between your thighs. You press your hand flat on your stomach and keep it there. He drags her ass back onto his cock, faster, until her moans break into short, wet gasps.
>
> Look at you, taking all of my cock. Moan for me.
>
> Yes. Yes. Fuck me harder, right there, right there.

**`park_watch_the_couple` · `touch`** — 159 words · 9 counted: tits, cock, moan, clit, thrust, nipple, ass, cock, clit · ceiling: strangers' words (DECISIONS 41): tits, nipples, ass, cock, wet, clit

> A dog barks somewhere along the path, and you freeze with your hand on your belly, but nobody comes.
>
> Behind the rhododendron, you can see everything. The man has the woman pinned to the tree, a hand full of each of her tits. His cock drives into her, hard and steady, and she moans on every stroke. Your hand slides down your belly and inside. Your fingers find your clit, and you are already wet. You match him. Each time he thrusts, you rub, fast and tight. Her nipples stand stiff between his fingers while her ass slaps the bark. You bite your lip so no sound gets out. Neither of them looks toward the bush. He groans and buries his cock deep, and you come with him. Your knees buckle, and your free hand grips a branch while your fingers keep working your clit through it.
>
> Take it. Take all of it.
>
> I'm coming. Oh God, I'm coming.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the park couple, the first explicit scene | LO, 2026-10-08 (question 8) |
| an accident at Good Girl, watching at Curious | SP2 §1 |
| touching herself while she watches, at Curious | SP2 §1 |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| the discovery ("he looks up, straight at you") plays once and sets `saw_the_couple`; after it, a short repeat: a different couple, or the same one not seeing her | LO's play note (arrival text never on a button that can be clicked again) · sweep A6-10 |
