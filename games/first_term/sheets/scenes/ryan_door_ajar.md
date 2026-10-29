# [READY] Scene — ryan_door_ajar

> Signed by LO: LO, 2026-10-29 ("sign all", in chat).

> Written 2026-10-29 from LO's pick in chat (DECISIONS 79). Prose by `v2-prose`, measured with `gates.py --beat`, pasted here.

| row | answer |
|---|---|
| system · place | the way up (DECISIONS 78, 79) · `home_ryan_room`, from the door |
| where · when | the landing, Ryan's door · Sun–Thu 22:00–00:00, Ryan in · new door option "His door's open a crack." |
| gate | none: open at Good Girl · not Friday (Kayla's night) |
| who | Ryan, 22; he never sees her |
| what she wears here (test 8) | not named |
| BRAKE (S9) | once a night |
| raises | the look: none · "Keep watching.": corruption add +1, cap 19 · no Ryan number moves, no step changes |
| the crude-word ceiling | Ryan's middle column: ass, tits, cock, wet · no cunt, fuck, cum, pussy, clit |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `crack` | his light, the door open a crack; Ryan stroking, her panties from the laundry to his face | yes | "Keep watching." → `watch` · "Pull the door shut." → the hall | `saw_ryan_alone` set (on both exits) |
| `watch` | he comes saying her nickname; she backs away before he looks up | yes | "Back to your room." → her room | corruption add +1, cap 19 |

**The no** ("Pull the door shut."): back to the hall; nothing pays.
**His want, shown (A13):** her panties in his hand, and her nickname. Nothing in 0.1 reads `saw_ryan_alone` yet;
a later Ryan step may.

## The explicit screens, written

**`crack`** · 126 words · explicit words 4 (cock, nipple) · median sentence 10 · ends on his hand and her nipples

> Ryan's door is open a crack, and his light is on. You mean to walk past, but you look in. Ryan is on his bed with his shorts shoved down. His cock is hard in his fist, and he is stroking it slowly. His other hand presses something to his face. It is a pair of panties from the laundry basket. They are yours. You know them. He breathes them in, and his hips lift off the bed. He has not seen you. Your face burns, but your body answers before you can stop it. Your nipples go tight and hard. Heat drops low in your belly, and you are wet. His fist slides up his cock and down again, slow, while your nipples ache.

**`watch`** · 128 words · explicit words 4 (cock, nipple) · median sentence 6 · ends on her body

> You stay. Your hand stays flat on the door frame. Ryan's fist moves faster on his cock. It is thick and red and wet at the tip. He lifts the panties to his face and breathes in. Then he groans under his breath. "@player.nickname." Your name, in that voice. His hips jerk off the bed. He comes hard, in long white ropes across his own stomach. You watch every one. Your nipples go tight and ache. You are wet, all at once, and you never decided that. You grip the frame until your fingers hurt. You do not touch yourself. You want to. His chest heaves. His cock twitches in his hand. You back away from the door before he looks up, thighs pressed together, nipples still hard.

No history words on either screen: both repeat. Changed 2026-10-29 in step 5: "your panties" became "the panties" on both screens, because the gate `her clothes are backed` read it as clothes she wears. The explicit count is unchanged.

## Why — the source of each key choice

| key choice | source |
|---|---|
| walking in on Ryan jerking off | LO, chat, 2026-10-13, picked 2026-10-29 |
| her panties from the laundry | the plan of 2026-10-29: his want shown before (A13) |
| not Friday | Ryan's Friday is Kayla's night (`npc_ryan.md` schedule) |
