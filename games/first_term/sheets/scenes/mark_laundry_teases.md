# [REVIEW] Scene — mark_laundry_teases

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. want, next step and hook rows. the explicit beats as built, measured.

> **New 2026-11-02, signed by LO 2026-11-02** ("Signed, skip the play check, build it"; DECISIONS 128). LO: "not
> dominance, not chores too, plain chores raises nothing, she can tease at a point, like when doing laundry tease
> him by doing something that can increase lust."

| row | answer |
|---|---|
| person · where | `npc_mark` · the garage, his laundry item (`hub_mark_garage`, "Do your laundry while he works.") |
| when | his garage rows (as built), 07:00–21:00 |
| plain laundry | pays Mark nothing (was his Lust +1). Every plain item with Mark pays him nothing now: the beer, the film, the TV, breakfast, dinner, cooking, the dishes. Her energy pays stay. |
| the accident first (H2) | every tease needs `mark_saw_her` (his accident at the dryer, `mark_00_the_dryer`). Mark's step 3 is no longer needed. |
| once a day | through the item's own `did_laundry`: one laundry, plain or tease, a day |
| the no | the item's "Not now." (as built) |
| want | his: he stops sanding when she bends at the drum |
| next step | the next button opens at Curious + Daring, then Bold + Showing |
| hook | his walk-ins at the laundry (`walkins_home.md`) come in on this ladder |

## The ladder

| button | gate | pays | what she wears |
|---|---|---|---|
| "Leave your basket on top." | Curious · `mark_saw_her` | Mark's Lust +2 | not named (the built screen: her panties on the basket) |
| "Bend for the bottom drum." | Curious · Daring (mixed: `meters.md` rule 4) · `mark_saw_her` · panties on · not a towel | Mark's Lust +3 · Exhibitionism +1, cap 39 | three screens by what she wears: a skirt or dress · the sleep shirt · jeans, leggings or shorts |
| "Wash what you're wearing." | Bold · Showing · `mark_saw_her` · a top and a bra on | Mark's Lust +4 · Exhibitionism +1 · Corruption +1, cap 59 | her top comes off into the washer (unequipped); she leaves in her bra |

Media (LO harvests): `sex/mark_laundry_bend_t4`, `sex/mark_laundry_wash_t4`.

## The screens, written

Written by `v2-prose` and measured by `gates.py --beat`, 2026-11-02 (low heat, H4: his want on his body, her reaction, a not-yet). `daring_jeans` names no garment of hers, so it is true in jeans, leggings or shorts; `daring_skirt` is true in a dress.

**daring_skirt** · 118 words · explicit words 4 · median sentence 9

> Mark's radio plays low over the sound of his sanding. You pull the wet load out and bend from the waist to fill the bottom drum. Your skirt rides up the backs of your thighs. Your panties show, and the curve of your ass under them. The sanding stops. "Take your time, @player," Mark says. His voice comes out rough. You feed the drum one shirt at a time and stay bent over. *He's looking. Good.* When you glance back, he's leaning on the bench, staring at your ass. His cock is hard in his jeans. You straighten and smooth the skirt down. He turns back to the bench, but his cock is still pushing at his zipper.

**daring_shirt** · 115 words · explicit words 4 · median sentence 12

> You're in only your long sleep shirt, barefoot on the cold concrete. Mark is at his bench with the radio on. You bend from the waist to load the bottom drum. The hem rides up over your ass. Your panties are right there, the cotton pulled tight across your cheeks. His screwdriver stops turning. "Jesus, @player. Laura's in the house." He doesn't look away when he says it. *Then don't look.* You stay bent and push the towels in slowly. His eyes stay on your ass, and his cock is hard in his jeans. You stand and tug the hem down. He turns back to the bench with his cock still straining against his fly.

**daring_jeans** · 118 words · explicit words 4 · median sentence 12

> The radio is on and Mark is bent over something at his bench. You bend from the waist to load the bottom drum. The seat pulls tight across your ass. Your waistband slides low at the back, and the top of your panties shows above it. Mark's hands stop. "You know what you look like right now, @player?" He doesn't finish. You feel his eyes on your ass while you shove the sheets in. *Say it, then.* He doesn't. When you look over, he's shifting on his stool, his cock hard in his jeans. You straighten and hitch your waistband up. He turns back to the bench, but his cock is still a hard ridge behind his zipper.

**bold** · 111 words · explicit words 5 · median sentence 11

> You pull your top off over your head and drop it in the drum. Then you stand there in your bra while the machine fills. You don't cover up. The radio keeps playing, but Mark's hands go still on the bench. He looks straight at your tits and doesn't pretend not to. "That's not laundry, @player. That's a show." *So watch it.* Your nipples go hard in the cold air, and he sees that too. He takes a long look at your tits, then another. Somewhere in the house Laura shuts a cupboard. He turns back to the bench, his cock hard in his jeans, his eyes still on your tits.

## Explicit beats as built (measured 2026-11-03)

One row per explicit screen in the built game: 3 or more words on the build's own list, the count `gates.py` uses. A screen's variants fold into it, so a screen can hold more words than one visit shows. "Sits at" is the highest of the person's crude columns (SP2) that the screen uses. Where a screen's text differs from the prose above, the build is what plays.

| screen | words | counted words | sits at | the text |
|---|---|---|---|---|
| `hl_laundry_tease2` | 1066 | 36: ass ×18, cock ×18 | Mark's middle column | on this sheet above |
| `hl_laundry_tease3` | 244 | 10: tits ×6, nipples ×2, cock ×2 | Mark's middle column; also nipples | on this sheet above |
