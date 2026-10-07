# [REVIEW] Scene — mark_05_a_bill_an_inch

> A draft for LO to place. Written 2026-10-08, fixed 2026-10-08 (cash, not rent; a stop at ten). **Mark's voice
> sample, in full:** every screen written by `v2-prose` from a spec, measured with `gates.py --beat`, pasted here.

| row | answer |
|---|---|
| person · step | `npc_mark` · 5 (Mark A 5) · his first paid touch |
| where · when | the living room · Sun–Fri 23:00–01:00, Laura asleep upstairs |
| gate | Corruption 40 · Exhibitionism 20 · his Want 40 · the boost off |
| want (test 1) | "Come down after your mother's asleep." (step 4); a bill folded, waiting |
| next step (test 2) | his hand, paid by the inch, in cash |
| hook (test 3) | Sunday she pays her rent with his money; what he asks next |
| what she wears here (test 8) | not named: her bare leg and thigh only |
| which version | his Power 50 or more: his (M) · under 50: hers (E) |
| the price | cash: $5 an inch, $20 at most · paid before Sunday's rent |
| the crude-word ceiling | Mark's middle column: tits, cock · early: legs, ass (LO, 2026-10-08) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `offer_m` | M: he names it: five an inch, cash | no | "Sit down. ($5 an inch, to $20)" → `climb` · "Hands off, Mark." → `no` | none |
| `offer_e` | E: her leg across his lap; she names it | no | "Let him. ($5 an inch, to $20)" → `climb` · "Not tonight." → `no` | none |
| `climb` | "Five." "Ten." His thumb, her legs part | yes (3 words) | "Keep going. (to $20)" → `climb2` · "That's far enough. ($10)" → `half` | none |
| `climb2` | "Fifteen." "Twenty." He stops an inch short | no (1 word) | "Keep going." → `stop` | none |
| `stop` | he doesn't; a floorboard upstairs; four fives on her knee | yes (3 words) | "Take the money." → `after` | money add +20 · corruption add +3 · Mark's Want add +10 |
| `half` | she stops his hand at ten; two fives in her palm | yes (4 words) | "Go to bed." → her room | money +10 · corruption +3 · his Want +10 (all add) · `mark_step` set 5 |
| `after` | "Go to bed, kid." The twenty in her fist | no | "Go to bed." → her room | `mark_step` set 5 · `mark_paid_touch` set |
| `no` | her no: he pulls back; "Rent's still Sunday." | no | "Go to bed." → her room | none: the step comes back in 3 days (guess) |

## The screens, written

**`offer_m`** · 102 words · explicit words 0 · median sentence 9

> It's late, the house asleep, the TV muttering low. Mark sits on the couch with a folded bill between two fingers. "You asked what the difference was worth, kid. Here it is." He pats the cushion beside him. "Five for every inch my hand climbs your bare thigh. Cash. Twenty tops." His voice drops on the last word. He stares at your legs like a starving man. Then his eyes flick to the ceiling, where your mother sleeps. *He actually said it out loud.* You aren't scared of him, but you've already done the math. He holds the bill out and waits.

**`offer_e`** · 108 words · explicit words 0 · median sentence 7

> The house is asleep, but Mark is still on the couch, pretending to watch a TV he turned down low. You sit on the arm beside him. Then you put one bare leg across his lap. "I asked what the difference was worth. Here's my answer," you say. "Five for every inch your hand climbs. Cash. Twenty tops." He swallows. His eyes drop to your thigh and stay there. Then they go to the ceiling, where your mother is sleeping. "Jesus, kid," he says, rough. He wants it, and it's all over his face. Your heart is pounding, but your leg stays put. You wait for his hand.

**`climb`** · 76 words · explicit words 3 (cock, nipple, tits) · median sentence 11 · Mark's middle column: tits, cock · early: legs, ass (LO, 2026-10-08)

> The TV mutters low. His rough palm settles on your bare knee, warm and heavy. "Five," Mark breathes, and the hand slides up. Your breath goes quick and shallow. "Ten." His thumb drags along the inside of your thigh, and your legs part a little for him. His cock is hard in his sweatpants, a thick ridge you can see from where you sit. Your nipples pull tight, and your tits ache with every short breath.

**`climb2`** · 41 words · explicit words 1 (cock) · median sentence 14

> "Fifteen." His fingers are shaking now, but they climb anyway, rough skin on soft. "Twenty." He stops one inch short of the top of your thigh. His hand stays there, hot and trembling, while his cock twitches against the grey cotton.

**`stop`** · 109 words · explicit words 3 (cock, nipple, tits) · median sentence 11 · Mark's middle column: tits, cock · early: legs, ass (LO, 2026-10-08)

> "Keep going," you say. His hand stays where it is, one inch short of the top of your thigh. His jaw is tight. His cock strains against his sweatpants, hard and close enough to touch. His palm trembles on your skin, but it does not move up. "Not yet, kid." Upstairs, a floorboard creaks. Your mother. You both freeze, his fingers still spread on your leg. He takes his hand back slowly. Then he lays four fives on your knee, right where his palm was. Your nipples are still hard, and your tits ache with it. Your legs stay open, and your thigh still burns where his hand was.

*The last sentence:* flagged by `--beat`; on her body, not a pivot: kept (LO, 2026-10-08).

**`half`** · 89 words · explicit words 4 (cock ×2, nipple, tits) · median sentence 8 · Mark's middle column: tits, cock · early: legs, ass (LO, 2026-10-08)

> You put your hand over his and press it still on your thigh. Mark freezes. His breath comes hard through his nose. Under his sweatpants his cock is a thick ridge, straining the cotton. He takes his hand back. He peels off two fives and lays them in your palm. Ten, not twenty. His eyes drop to your bare legs and stay there. Your tits ache, the nipples tight and hard. You keep your legs where they are a moment longer, on purpose. His cock jerks against the cotton.

**`after`** · 100 words · explicit words 0 · median sentence 10 · the meaning beat

> Four fives in your fist, still warm from Mark's wallet. He won't look at you. He turns the TV up until the room is only noise. "Go to bed, kid," he says, rough. You climb the stairs and pass your mother's door. It's shut, but you walk past it slowly. *You just got paid to let your step-father touch you. It was the easiest twenty you ever made.* Sunday you pay your rent at the kitchen table with his own money. He'll sit across from you and count it, and you already want to know what he'll ask for next.

**`no`** · 58 words · explicit words 0 · median sentence 9 · the written no

> "Hands off, Mark." His hand jerks off your thigh like it burned him. He folds the twenty and shoves it in his pocket. "Suit yourself, kid. Rent's still Sunday." The no cost you twenty, nothing more. But he'll offer again, and you both know it. You walk to the stairs. His eyes follow you all the way up.

**Fixed 2026-10-08:** the price lines said "off your rent"; it is cash, so they now say "Five for every inch …
Cash." The old climb screen is split at ten so "That's far enough" can stop it there for $10.

## Truth checks

| line | what backs it |
|---|---|
| "You asked what the difference was worth" | step 4 is in the counter; this step needs it |
| "your mother sleeps" upstairs | Laura's night row, master bedroom, from 22:00 |
| the twenty or the ten in her hand | money add +20 on `stop`, +10 on `half`; the price on the button |
| "Sunday you pay your rent … with his own money" | the cash is in `money`; the rent is taken from it Sunday |
| no garment of hers is named | nothing needs backing |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene: a bill an inch, he stops at the hem | the arc ideas, Mark A 5 (heat 10-06) |
| paid as cash, before the rent | LO, 2026-10-07 (SYSTEMS, decided item 8) · LO, 2026-10-08 (fix 3) |
| up to $20; a stop at ten for less | LO, 2026-10-07 (SP4) · LO, 2026-10-08 |
| two versions by his Power | SP2 (Mark: written twice) |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| $5 an inch, the Power edge at 50, retry in 3 days | guess |
