# [REVIEW] Scene — ryan_door_ajar

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. C3's "Stay until his light goes off." and its screen; want, next step and hook rows. the explicit beats as built, measured.

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder H7): the scene reads his Want. Under 30 he watches porn on his phone and her panties lie on the floor, untouched; from 30, the panties to his face (as built). Stays at Good Girl (DECISIONS 79).

> Signed by LO: LO, 2026-10-29 ("sign all", in chat).

> Written 2026-10-29 from LO's pick in chat (DECISIONS 79). Prose by `v2-prose`, measured with `gates.py --beat`, pasted here.

| row | answer |
|---|---|
| system · place | the way up (DECISIONS 78, 79) · `home_ryan_room`, from the door |
| where · when | the landing, Ryan's door · Sun–Thu 22:00–00:00, Ryan in · new door option "His door's open a crack." |
| gate | none: open at Good Girl · not Friday (Kayla's night) |
| who | Ryan, 22; he never sees her |
| what she wears here | not named |
| BRAKE | once a night |
| raises | the look: none · "Back to your room." after watching: corruption add +1, cap 19 · from Corruption 15, "Stay until his light goes off." → `light_off`, whose exit pays +1, cap 19 again · no Ryan number moves, no step changes |
| the crude-word ceiling | Ryan's middle column: ass, tits, cock, wet · no cunt, fuck, cum, pussy, clit |

| want | his: her panties on the floor (under 30), then in his hand (from 30) |
| next step | she stays until his light goes off (Corruption 15) |
| hook | `saw_ryan_alone` is set; nothing reads it this release |

The small rung "Stay until his light goes off." is C3 of the heat proposal (`proposals/FIRST_TERM_HEAT_PROPOSAL_20261103.md`, signed 2026-11-03).

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `crack_low` (his Want under 30) | his light, the door open a crack; Ryan stroking to porn on his phone, her panties on the floor by the hamper, untouched | yes | "Keep watching." → `watch_low` · "Pull the door shut." → the hall | `saw_ryan_alone` set (on both exits) |
| `watch_low` | he comes to the phone; his eyes go once to her panties on the floor; she backs away | yes | "Back to your room." → her room · "Stay until his light goes off." (Corruption 15) → `light_off` | corruption add +1, cap 19 on the first |
| `crack` (his Want 30 and up) | his light, the door open a crack; Ryan stroking, her panties from the laundry to his face | yes | "Keep watching." → `watch` · "Pull the door shut." → the hall | `saw_ryan_alone` set (on both exits) |
| `watch` | he comes saying her nickname; she backs away before he looks up | yes | "Back to your room." → her room · "Stay until his light goes off." (Corruption 15) → `light_off` | corruption add +1, cap 19 on the first |
| `light_off` | he wipes up with a sock; under 30 his phone face down, from 30 the panties in his fist; his lamp clicks off; "Jesus Christ. What is wrong with me." | no | "Back to your room." → her room | corruption add +1, cap 19 |

**The no** ("Pull the door shut."): back to the hall; nothing pays.
**His want, shown (A13, H7):** under 30, his eyes going once to her panties on the floor (he wants her and is not
there yet); from 30, her panties in his hand, and her nickname. The two nodes split on `npc_ryan` `want` lt 30 / gte 30. Nothing in 0.1 reads `saw_ryan_alone` yet;
a later Ryan step may.

## The explicit screens, written

**`crack`** · 126 words · explicit words 4 (cock, nipple) · median sentence 10 · ends on his hand and her nipples

> Ryan's door is open a crack, and his light is on. You mean to walk past, but you look in. Ryan is on his bed with his shorts shoved down. His cock is hard in his fist, and he is stroking it slowly. His other hand presses something to his face. It is a pair of panties from the laundry basket. They are yours. You know them. He breathes them in, and his hips lift off the bed. He has not seen you. Your face burns, but your body answers before you can stop it. Your nipples go tight and hard. Heat drops low in your belly, and you are wet. His fist slides up his cock and down again, slow, while your nipples ache.

**`watch`** · 128 words · explicit words 4 (cock, nipple) · median sentence 6 · ends on her body

> You stay. Your hand stays flat on the door frame. Ryan's fist moves faster on his cock. It is thick and red and wet at the tip. He lifts the panties to his face and breathes in. Then he groans under his breath. "@player.nickname." Your name, in that voice. His hips jerk off the bed. He comes hard, in long white ropes across his own stomach. You watch every one. Your nipples go tight and ache. You are wet, all at once, and you never decided that. You grip the frame until your fingers hurt. You do not touch yourself. You want to. His chest heaves. His cock twitches in his hand. You back away from the door before he looks up, thighs pressed together, nipples still hard.

No history words on either screen: both repeat. Changed 2026-10-29 in step 5: "your panties" became "the panties" on both screens, because the gate `her clothes are backed` read it as clothes she wears. The explicit count is unchanged.

**`crack_low`** · 120 words · explicit words 5 · median sentence 10 · written by the lead 2026-11-01, measured

> Ryan's door is open a crack, and his light is on. You mean to walk past, but you look in. Ryan is on his bed with his shorts shoved down and his phone propped on his knee. A girl moans on the screen, tinny and loud. His cock is hard in his fist, and he strokes it to her. He has not seen you. On the floor by his hamper lies a pair of panties from the laundry. They are yours, and he hasn't touched them. Your face burns. Your nipples go tight and hard anyway. Heat drops low in your belly, and you are wet. His fist slides up his cock and down again, slow, while your nipples ache.

**`watch_low`** · 132 words · explicit words 4 · median sentence 8 · written by the lead 2026-11-01, measured

> You stay. Your hand stays flat on the door frame. On the phone the girl is on her knees. Ryan's fist moves faster on his cock. It is thick and red and wet at the tip. His eyes leave the screen once, to the panties on the floor by the hamper, and stay there a beat too long. Then he groans under his breath. His hips jerk off the bed. He comes hard, in long white ropes across his own stomach. You watch every one. Your nipples go tight and ache. His cock twitches in his fist. You are wet, all at once, and you never decided that. You grip the frame until your fingers hurt. You back away from the door before he looks up, thighs pressed together, nipples still hard.

## Why — the source of each key choice

| key choice | source |
|---|---|
| walking in on Ryan jerking off | LO, chat, 2026-10-13, picked 2026-10-29 |
| her panties from the laundry | the plan of 2026-10-29: his want shown before (A13) |
| not Friday | Ryan's Friday is Kayla's night (`npc_ryan.md` schedule) |
| the split at his Want 30 | LO, 2026-11-01: "until ryan corruption hasnt risen up he doesnt want her then why he is masturbating on her panties??" · DECISIONS 124 |

## Explicit beats as built (measured 2026-11-03)

One row per explicit screen in the built game: 3 or more words on the build's own list, the count `gates.py` uses. A screen's variants fold into it, so a screen can hold more words than one visit shows. "Sits at" is the highest of the person's crude columns (SP2) that the screen uses. Where a screen's text differs from the prose above, the build is what plays.

| screen | words | counted words | sits at | the text |
|---|---|---|---|---|
| `crack` | 259 | 12: cock ×4, nipples ×4, fuck ×3, moans | Ryan's late column; also nipples | on this sheet above |
| `watch_low` | 138 | 6: cock ×2, nipples ×2, fuck ×2 | Ryan's late column; also nipples | on this sheet above |
| `watch` | 138 | 7: cock ×2, nipples ×2, fuck ×2, fucking | Ryan's late column; also nipples | on this sheet above |
