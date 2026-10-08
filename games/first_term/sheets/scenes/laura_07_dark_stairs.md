# [READY] Scene — laura_07_dark_stairs

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. **Laura's voice sample, in full:** every screen written by
> `v2-prose` from a spec, measured with `gates.py --beat`, pasted here. LO picked this step.

| row | answer |
|---|---|
| person · step | `npc_laura` · 7 (Laura C 7) |
| where · when | the kitchen, Friday 18:00–21:00 · then Zoe's party · then the dark stairs |
| gate | Corruption 40 · Exhibitionism 40 · her Want 60 · Zoe A 1 |
| want (test 1) | "Take me with you one night." (step 6); tonight she dressed for her |
| next step (test 2) | the first kiss, and Ryan sees it |
| hook (test 3) | the next breakfast: she'll have to look at her (step 8) |
| what she wears here (test 8) | not named; Laura's short dress is Laura's |
| her voice | stage 3, confident with her mother |
| the crude-word ceiling | Laura's middle column: tits, nipples · no pussy · Ryan's middle column for his line |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `kitchen` | Laura in a short dress, wine: "Take me with you tonight." | no | "Come on, then." → `party` · "Not tonight, Mom." → parked | none |
| `party` | Zoe's: Laura dances, drinks, can't stop looking at her | no | "Take her home." → `stairs` | the clock to 02:15 (Mark asleep by then) |
| `stairs` | halfway up, Laura kisses her; her hand on her tit | yes (5 words) | "Kiss her back." → `door` | corruption add +3 · Laura's Want add +10 |
| `door` | Ryan's door opens; "Don't stop for him." | yes (8 words) | "Let her stop." → `after` | `laura_ryan_saw_kiss` set |
| `after` | Laura goes to bed without a word; Ryan: "What was that?" | no | "Go to bed." → her room | `laura_step` set 7 · `laura_suspicion` unchanged |

"Not tonight, Mom." is her parked no: Laura asks again next Friday (`retry_after_days = 7`, guess).

## The screens, written

**`kitchen`** · 105 words · explicit words 1 (tits) · median sentence 8 · not explicit

> Laura is leaning on the kitchen counter in a black dress that stops high on her thighs. Her wine glass is already half empty. Mark's radio plays out in the garage. "You told me short," she says. "Is this short enough, sweetheart?" She turns for you, slow, and the neckline shows the tops of her tits. Then she just looks at you, too long. Her cheeks go pink, but she doesn't look away. "Zoe's party. Take me with you tonight. Please." You feel it low in your stomach. She dressed for you, not for him. She sets the glass down and waits for your answer.

**`party`** · 117 words · explicit words 0 · median sentence 11 · not explicit

> Zoe's apartment is loud, and nobody here knows the woman in the short dress is your mom. Laura drinks her wine too fast. She laughs too loud at a guy's joke, and two others stare at her chest. She likes it. She lets you see it. But her eyes keep finding you across the room. When you dance, her hand settles on your waist and stays too long. "Sweetheart," she says against your ear, "look at you tonight." Zoe grabs your arm, grinning. "Babe. Your mom." *She wants you. She isn't hiding it.* When the party thins out, Laura takes your hand and won't let go. You walk home in the dark, her fingers laced in yours.

One line changed after `v2-prose`: "At one in the morning" became "When the party thins out". A beat never reads the clock (SP1).

**`stairs`** · 124 words · explicit words 5 (kiss, nipple, tit) · median sentence 10 · act rung: touch · Laura's middle column: tits, nipples · no pussy

> Halfway up the stairs, Laura stops and turns. Before you can ask, she kisses you. Her mouth is warm and open, and you taste the wine on her tongue. Her hand lands flat on your chest. Then it slides, slow, until her palm covers your tit. Her thumb finds your nipple through the fabric and circles it until it goes hard. You gasp into her mouth, so she pushes your back into the wall. The plaster is cold, but she is hot all down your front. You kiss her back, hungry, your tongue chasing hers. "Sweetheart," she breathes against your lips. Her hips press into yours and pin you there. Her thumb keeps rolling your nipple, and her breath goes ragged in your mouth.

*The last sentence:* her thumb on the nipple, her breath. On the body; not a pivot.

**`door`** · 122 words · explicit words 8 (cock, kiss, moan, nipple, suck, tit) · median sentence 9 · act rungs: touch, oral (her mouth on the neck) · Laura's middle column: tits, nipples · no pussy · Ryan's cock is his column

> Laura's mouth is on yours, slow and wet, and her hand is full of your tit. She squeezes, and you moan into the kiss. Then Ryan's door opens at the top of the stairs. His light drops over you both. He stares. Laura doesn't let go. Her thumb keeps circling your nipple. "Go to bed, Ryan." You look straight up at him. Then you pull your mother back into the kiss. "Don't stop for him." He doesn't move. Laura's lips slide down to your neck and suck just under your jaw. Your nipples are hard against her, and she pinches one until you gasp. Up in the doorway, Ryan's hand is white on the frame and his cock is tenting his shorts.

*The last sentence:* Ryan's grip and his cock. On the body; not a pivot.

**`after`** · 91 words · explicit words 1 (kiss) · median sentence 9 · the meaning beat

> Laura pulls back on the stairs. Her lipstick is smeared, and she is breathing hard. She looks at Ryan in his doorway, then at you. She says nothing. She goes up past him to her bedroom, and her door clicks shut beside Mark's snoring. "@player.nickname," Ryan says, low. "What was that?" You don't answer him either. *You kissed your mother. You want her to do it again.* In the morning she'll be in the kitchen at breakfast. But a kitchen has nowhere to hide, and she'll have to look at you.

## Truth checks

| line | what backs it |
|---|---|
| "You told me short" | `laura_asked_to_come`, set by step 6; the counter needs it |
| "Mark's radio … in the garage" | Mark's Friday garage row, 18:00–22:00 |
| "Mark's snoring" | the party screen moves the clock past 02:00; he is in bed from 02:00 |
| "nobody here knows … your mom", Zoe there | the Friday party; Zoe A 1 is in the gate |
| no garment of hers is named | nothing needs backing |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene: party, stairs, Ryan's door | the arc ideas, Laura C 7 (heat 10-06) |
| this step as the voice sample | LO, 2026-10-08 |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| the middle column at stage 3 | LO, 2026-10-08 (question 28) |
| the clock to 02:15 | guess, to keep "Mark's snoring" true |
| retry in 7 days | guess |
