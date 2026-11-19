# [READY] Scene — hale_04_claire_knocks

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08. **Hale's voice sample, in full:** every screen written by
> `v2-prose` from a spec, measured with `gates.py --beat`, pasted here. LO picked this step. Claire is met here.

| row | answer |
|---|---|
| person · step | `npc_hale` · 4 (Hale B 4) · with Claire (38), his wife |
| where · when | his office, the faculty floor · Thursday 18:30–19:30, near her pickup |
| gate | Corruption 40 · Exhibitionism 40 · the boost off |
| want (test 1) | he turned the photo face-down himself (step 3); "like it costs him" |
| next step (test 2) | her body bare to him, his hand on her; and his wife at the door |
| hook (test 3) | next class he has to look at her from the lectern (step 5) |
| what she wears here (test 8) | the button lines only in the sheer blouse (the one top with buttons); in any other top the variant below: she pulls it up |
| Claire, role before name | "his wife", then "Claire" when he says it |
| the crude-word ceiling | Hale's middle column: tits, nipples, cock · early: legs, ass (LO, 2026-10-08) |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `desk` | the corner of his desk; the photo face-down; his eyes | no | "Undo it." → `hand` · "Button up." → `no` | none |
| `hand` | she undoes her buttons (blouse) or pulls her top up (any other top); his hand inside, his thumb on her nipple | yes (6 words) | → `knock` | exhibitionism add +3 · corruption add +3 |
| `knock` | "You ready, love?" She opens the door: "Your husband's a great teacher." | no | "Leave." → `corridor` | `claire_met` set |
| `corridor` | past his wife; "Grab your coat."; she's shaking because she liked it | no | "Go home." → campus | Hale's step counter set 4 |
| `no` | "Button up." "Next Thursday, then, @player." The photo, down again | no | "Leave." → the faculty floor | none: the step returns next Thursday |

## The screens, written

**`desk`** · 109 words · explicit words 1 (tits) · median sentence 9

> The corridor outside is empty. You sit on the corner of Dr. Hale's desk, like last time. His wedding photo still lies face-down where he turned it. He holds your paper and reads none of it. His eyes go to the clock, because his wife comes soon and you both know it. Then they come back to your mouth, and down your legs, and they stay there. "@player." He says your name like it costs him. His voice has gone rough. "You can't sit like that in here." "Like what?" He stares at your tits instead of answering. You want him staring. Your hand goes to your own top button.

**`hand`** · 129 words · explicit words 6 (cock, nipple, tit, tits) · median sentence 11 · act rung: touch · Hale's middle column: tits, nipples, cock · early: legs, ass (LO, 2026-10-08)

> You sit on the corner of his desk and undo the buttons yourself, one at a time, slowly. There is nothing under them. Your tits come free, bare to him, your nipples already tight. Dr. Hale stares. He wants to touch you, but he can't stop looking first. "@player," he says. His voice cracks on it. Then his hand slides inside, and his palm closes over your tit. It covers you completely, warm and heavy. His thumb finds your nipple and rolls it, slow, then harder. You arch into his hand. His breath goes ragged against your neck. His cock is hard, pressing against the edge of the desk an inch from your hip. Your nipple is stiff under his thumb, so he rolls it again until you gasp.

*The last sentence:* her nipple, his thumb, her gasp. On the body; not a pivot.

**`knock`** · 110 words · explicit words 1 (tit) · median sentence 10

> His hand is on your bare tit when the knock comes. A woman's voice through the door, bright: "You ready, love?" Hale goes grey. He snatches his hand back, and he can't move. Your heart is slamming, but your hands are steady. You do one button, slow. You slide off the desk and open the door yourself. His wife stands in a neat coat, car keys in her hand. Her smile stops halfway. "Your husband's a great teacher," you say. Hale, behind you: "Claire — this is one of my students." Her eyes drop to your flushed chest. Then they go past you, to the face-down photo on his desk.

**`corridor`** · 95 words · explicit words 0 · median sentence 7 · the meaning beat

> You walk down the empty faculty corridor, slowly, past Dr. Hale's wife. Claire doesn't stop you. You do the rest of your buttons as you go, one at a time, because your fingers won't hurry. Behind you, through the half-open door, Claire's voice comes very calm. "Grab your coat." *His wife saw you. His hand was on you a minute ago.* And you're not scared, not even a little. You're shaking because you liked it. Next class, Dr. Hale has to stand at the lectern and look at you. And he'll have something to say.

**`no`** · 64 words · explicit words 0 · median sentence 8 · the written no

> You let go of your top button. You slide off his desk and pick up your paper. Your face is hot. Dr. Hale breathes out, half relief and half not. "Next Thursday, then, @player." His eyes stay on you, and he still wants a yes. He turns the photo face-up. A second later his hand turns it face-down again and stays flat on it.

One change after `v2-prose`: "your open collar" (twice) became "your flushed chest" and "you". A collar is part of a
garment, and nothing on this screen backs one (her clothes are backed). Re-measured.

## Truth checks

| line | what backs it |
|---|---|
| "like last time", the photo face-down | step 3 is in his counter; this step needs it |
| "Claire comes soon" | her 7:30 pickup, a rule of the world; the step window ends 19:30 |
| "Next Thursday, then" | the no parks the step to next Thursday |
| no garment of hers is named | her buttons are undone inside the act |

## The top without buttons (sweep A4-22)

65 words · explicit words 4 (nipple, tits) · median sentence 11 · act rung: touch · the last sentence stays on her body (`gates.py --beat`, 2026-10-08). Hale's middle column caps it; tits and nipples sit under it.

Variant of the `hand` beat, for any top that isn't the sheer blouse:

> You sit on the corner of his desk and pull your top up over your tits, slowly, and hold it there. There is nothing under it. Your tits are bare to him, your nipples already tight. Dr. Hale stares. He wants to touch you, but he can't stop looking first. "@player," he says, and his voice cracks, and his eyes stay on your bare tits.

The later lines swap the same way: "You do one button, slow" becomes "You pull your top down"; "You do the rest of your buttons as you go" becomes "You tug your top straight as you go"; "You let go of your top button" becomes "You let go of your hem."

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene: her buttons, his hand, Claire at the door | the arc ideas, Hale B 4 (heat 10-06) |
| this step as the voice sample | LO, 2026-10-08 |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| `claire_met` as a key | guess |
| fix from the false-line sweep | sweep A4-19 ("his wife" until he names her at the door), A4-22 (2026-10-08) |

