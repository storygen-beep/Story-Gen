# [READY] Scene — zoe_03_hot_tub

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08. **Zoe's voice sample, in full:** every screen written by
> `v2-prose` from a spec, measured with `gates.py --beat`, pasted here. LO picked this step.

| row | answer |
|---|---|
| person · step | `npc_zoe` · 3 (Zoe A 3) |
| where · when | the party house hot tub · Saturday 20:00–00:00, seen from Zoe's apartment |
| gate | Corruption 40 · Exhibitionism 40 · `party_house_invite` (A 2) · the boost off |
| want (test 1) | "There's a hot tub Saturday. Just us." (A 2); her knee against @player's |
| next step (test 2) | topless for Zoe alone, and @player kisses her first |
| hook (test 3) | "You could've asked." Zoe answers on her couch (A 4); Ryan sees her come home |
| what she wears here (test 8) | she strips to her bra and panties at the tub's edge (top and bottom off on the first screen); "it" is her bra, and taking it off takes the bra off |
| only Zoe sees her | her friends go inside first (LO, 2026-10-08): SP2's group rule holds |
| the crude-word ceiling | Zoe's middle column: tits, nipples, wet · early: tits, ass (LO, 2026-10-08) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `tub` | the hot tub, Zoe's friends, Zoe pressed close | no | "Stay in the water." → `alone` | none |
| `alone` | the friends go in; Zoe: "Take it off. Just for me." | no | "Take your bra off." → `kiss` (bra off) · "Not tonight, Zo." → `home` (parked) | none |
| `kiss` | topless in the steam; she pulls Zoe in and kisses her | yes (9 words) | "Hold her." → `asked` | exhibitionism add +3 · corruption add +3 |
| `asked` | "Took you long enough." — "You could've asked." | no | "Go home." → `home` | `zoe_step` set 3 |
| `home` | home late, wet hair, Zoe's lipstick; Ryan at his door | no | "Go to bed." → her room | Ryan's Want add +5 (guess) |

"Not tonight, Zo." costs nothing: the dare comes back next Saturday.

## The screens, written

**`tub`** · 105 words · explicit words 1 (tits) · median sentence 8

> Zoe drags you into the hot tub on the back deck, laughing. Steam rolls off the water. Music thumps through the glass. Three of her friends are already in, drinks on the rim. "Make room, babe's here." She doesn't need room. She sits right against you, her knee pressed to yours under the water. When you talk, she watches your mouth. All term she has dared you instead of asking, but you know what she wants. "Your tits are floating, babe," she says, grinning. Your face goes hot, and it isn't the water. One of her friends stands up, restless. "Going in for more drinks."

**`alone`** · 99 words · explicit words 2 (nipple, tits) · median sentence 7

> The door slides shut behind her friends. Now it is just the two of you in the steam. Zoe goes quiet, and Zoe is never quiet. "Take it off, babe," she says, low. "Just for me. Nobody else is here." Her eyes drop to your chest and stay there. She bites her lip. Her breath comes short across the water. "Everything on you is wet anyway. I can see your nipples, babe. I want to see your tits." Your heart pounds, because you want her to keep looking. Your hands drift up and stop. She waits for your answer.

**`kiss`** · 119 words · explicit words 9 (ass, kiss, moan, nipple, tits) · median sentence 9 · act rung: touch · Zoe's middle column: tits, nipples, wet · early: tits, ass (LO, 2026-10-08)

> You unhook your bra and toss it on the deck. The steam rolls over your bare tits. The night air is cold on them, so your nipples go hard above the water. Zoe stares at them. "Babe," she breathes. "Look at you." You grab the back of her neck and pull her in. You kiss her hard, open-mouthed, until she moans into you. Her tits press flat against yours. Her nipples drag across your nipples, hard and wet. Her thigh slides between your thighs under the water. It presses up, slow and firm. Her breath catches. Your hands run down her slick back to her ass. You grab it with both hands and pull her tits tight against yours.

*The last sentence:* her hands on Zoe's ass, their tits pressed together. On the body; not a pivot.

**`asked`** · 88 words · explicit words 0 · median sentence 9 · the meaning beat

> Zoe pulls back, flushed and breathless, and laughs. "Took you long enough, babe." "You could've asked," you tell her. She goes quiet. She opens her mouth, but she doesn't answer that. Not yet. All term she dared you instead of asking for this. You liked every single dare. The sliding door bangs open. Your friends spill back out, shrieking. You sink to your shoulders in the hot water. Across the bubbles, Zoe is still looking at you. Next time you two are alone, somebody has to ask first.

**`home`** · 98 words · explicit words 0 · median sentence 11

> You let yourself in. The house is dark, and your hair drips on the mat. You smell of chlorine, and Zoe's lipstick is still on your neck. Upstairs, Ryan's door is open a crack. He is awake. He sees you on the landing. His eyes stop on your wet hair, then drop to your neck and stay there. "@player.nickname. Where've you been?" "Zoe's." You say nothing else, because you want him to wonder. Your face goes hot under his stare, but you hold it. Ryan's jaw tightens. He looks a beat too long, then his door closes slowly.

## Truth checks

| line | what backs it |
|---|---|
| "All term she has dared you" | Zoe A 1 and A 2 are in her counter; this step needs them |
| her friends gone; only Zoe sees | the `alone` screen sends them in before anything comes off |
| "Zoe's lipstick on your neck" | the kiss on the screen before |
| Ryan awake at his door | his night row, his room, every night |
| no garment of hers is named | she takes it off inside the act |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene: the hot tub, the kiss, Ryan at home | the arc ideas, Zoe A 3 (heat 10-06) |
| her friends go in first | LO, 2026-10-08 (question 6) |
| this step as the voice sample | LO, 2026-10-08 |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| Ryan's Want +5 on seeing her | guess |
| fix from the false-line sweep | sweep A4-24 (2026-10-08) |
