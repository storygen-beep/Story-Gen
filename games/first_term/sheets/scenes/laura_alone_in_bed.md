# [READY] Scene — laura_alone_in_bed

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. the gate row reads `laura_step` 2 as built; want, next step and hook rows. the explicit beats as built, measured. file and line cites cut.

> **Changed 2026-11-02, signed by LO 2026-11-02** ("Signed, go with your recs, skip the play check"; DECISIONS 131, `sheets/READER_FAILS_A3.md`, Home): row 2: `crack` gains one ungated line after the signed beat: "Her face is turned on the pillow toward the hall, toward Ryan's door. Her lips move around a word you can't hear, and her fingers go faster." Her want for Ryan on her body before `laura_04_she_saw_you` says his name. True every night of the window: Ryan's row has him in his room 22:00-06:45. The signed `crack` beat itself is unchanged.

> **Changed 2026-11-01 after the build, signed by LO 2026-11-01 ("Signed, build them")** (the reader's FAILs; LO's picks in chat): the gap opens after Laura's step 2 (LO's pick 2b: her want is shown first).

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Go ahead")** (DECISIONS 99–114): Laura's release-1 ladder (`sheets/people/npc_laura.md`, signed). Changed: "Keep watching." also adds 1 to `laura_gaps_watched` (her step 4 needs 3, this gap and the shower's); after step 3 one line names the dressed-up night; after step 4 two new screens, `crack_after` and `watch_after` (Laura knows, face to the wall, quieter), by `v2-prose`, measured; on a night her step 4 is ready, `laura_04_she_saw_you` takes this slot. The signed screens stand.

> Signed by LO: LO, 2026-10-29 ("sign all", in chat).

> Written 2026-10-29 from LO's pick in chat ("yes, 1, laura alone, fingering herself", DECISIONS 82). Prose by `v2-prose`, measured with `gates.py --beat`, pasted here.

| row | answer |
|---|---|
| system · place | the way up (DECISIONS 78, 79, 82) · `home_master_bedroom`, from the door |
| where · when | the hall, their door · Sun–Fri 22:00–23:00, Laura in and awake, Mark in the living room (new row in Laura's schedule) · door option "The door's ajar." in place of "Ease the door open" in that hour |
| gate | `laura_step` gte 2 · Laura present, Mark absent · Sun–Fri |
| who | Laura, 41, her mother; she never sees her |
| want | Laura's: alone while Mark stays in the living room, her hand between her thighs |
| next step | three watched gaps open her step 4 (`laura_04_she_saw_you`) |
| hook | each watch adds 1 to `laura_gaps_watched` |
| what she wears here | not named |
| BRAKE | once a night (20 hours, as Ryan's door) · after she watched, "Peek through the gap." → `laura_alone_peek`, pays nothing |
| raises | the look: none · "Keep watching.": corruption add +1, cap 19 · `laura_gaps_watched` add +1 (counts toward her step 4) |
| the crude-word ceiling | the park's: tits, nipples, ass, wet, clit · no cunt, fuck, cum, pussy (guess: LO to confirm for Laura) |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `crack` | the lamp low, Laura alone, nightdress up, fingers on her clit; she hasn't seen her | yes | "Keep watching." → `watch` · "Pull the door to." → the hall | `saw_laura_alone`, `laura_alone_seen` set (on every exit) |
| `watch` | two fingers inside, she bites her hand so Mark won't hear, she comes; she backs away | yes | "Back to your room." → her room | corruption add +1, cap 19 |
| `laura_alone_peek` (own canvas) | the lamp off, Laura on her side under the sheet, breathing slow | no | "Close the door." → the hall | none |

**The no** ("Pull the door to."): nothing pays.
**Laura's want, shown:** alone while Mark stays in the living room; it feeds her arc and the Saturday scene's ending (her hand under the sheet). Nothing in 0.1 reads `saw_laura_alone` yet.

## After her step 3 and step 4 (changed 2026-11-01)

| when | what changes |
|---|---|
| `laura_lonely` set (step 3) | `crack` gains one line, after "Down the hall the TV mutters.": "The good dress you zipped her into hangs on the wardrobe door." True on every night after the Saturday it happened |
| her step 4 ready (its gate met) | `laura_04_she_saw_you` fires in this slot instead (priority over this canvas) |
| `laura_04_done` set | the door option opens `crack_after` in place of `crack`; "Keep watching." → `watch_after`; the same pay, brake and no |

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `crack_after` | Laura on her side, back to the door, face to the wall, her hand between her thighs; she knows the door is open | yes | "Keep watching." → `watch_after` · "Pull the door to." → the hall | `saw_laura_alone`, `laura_alone_seen` set (on every exit) |
| `watch_after` | she comes into the pillow, almost silent; she doesn't turn round; you go to your room | yes | "Back to your room." → her room | corruption add +1, cap 19 · `laura_gaps_watched` add +1 |

**`crack_after`** · 132 words · explicit words 5 · median sentence 8 · act rungs: hands · written by `v2-prose`, measured by `gates.py --beat`, 2026-11-01. "She is quieter than she used to be" is true only behind `laura_04_done`, where it shows.

> Her door is open a hand's width, and the lamp is low. Laura lies on her side with her back to you, her face to the wall. Her hip is bare, and so is her ass, round and pale. Her hand is between her thighs from the front, moving slow. You hear it, a small wet sound, steady. She is quieter than she used to be. She doesn't look round, but she knows the door is open. Down the hall the TV mutters. You know you should go. You stay. Her shoulders tighten. Her ass clenches as her fingers work her clit. Heat climbs your face. Your nipples go hard, and you are wet. You keep your hands at your sides. A soft moan leaves her, and her thighs press tight around her hand.

*The last sentence:* the moan, her thighs tight round her hand. On the body.

**`watch_after`** · 125 words · explicit words 4 · median sentence 8 · act rungs: hands, vaginal (her own fingers)

> You stay in the gap of the door. Laura's fingers slide off her clit and push inside her, faster now. Her hips rock back toward the door, toward you. She shoves her face into the pillow. Her thighs start to shake. Her ass clenches hard, twice, and she comes with one long breath into the pillow, almost silent. Down the hall, Mark's TV laughs at something. Laura says nothing. She doesn't turn round. She stays on her side, breathing hard, her hand still between her thighs. You back away to your room. You lie down on top of the covers. Your nipples are tight and aching. You're wet, and you press your thighs together hard. Your clit throbs, and you keep both hands flat on the sheet.

*The last sentence:* your clit throbbing, your hands flat on the sheet. On the body.

## Prose

**`crack`** (127 words, 7 explicit):

Laura's door is open a hand's width. The bedside lamp is on low. Down the hall the TV mutters. Laura is alone in bed, the covers kicked down. Her nightdress is pushed up to her waist. Her knees are up and apart, her ass bare on the sheet. Two fingers rub slow circles on her clit. She is wet, and it shines in the lamplight. Her other hand squeezes her tit through the nightdress. Her nipple stands hard against the cotton. Her tits rise and fall faster. Her eyes are shut, her lip caught in her teeth. A small moan escapes her. Her hips lift into her fingers. She hasn't seen you. Your face burns. Heat pools low in your belly. You are wet, and your nipples go tight.

**`watch`** (140 words, 7 explicit):

You stay. Your hand stays flat on the door frame. Laura pushes two fingers inside herself. Her thumb rubs her clit, faster now. Her other hand squeezes her tit and pinches the nipple. Her hips lift off the mattress. She bites the back of her hand so Mark won't hear. Her fingers pump in and out, wet and loud in the quiet. Then she comes. Her whole body shakes. Her thighs clamp hard on her hand. A moan leaks out around her teeth. Your nipples go tight and ache. You are wet, all at once. You press your thighs together. You do not touch yourself. You want to. Laura goes still, breathing hard, two fingers still inside her. Her tits rise and fall. You back away from the door before she opens her eyes, thighs pressed tight, nipples still hard.

**`laura_alone_peek`:** "You ease the door a finger's width wider. The lamp is off now." · "Laura lies on her side with the sheet pulled up to her shoulder, breathing slow. Her nightdress is still rucked up at her hip." · "Down the hall the TV mutters. You pull the door to without a sound."

## What else changed for it

- Laura's bedroom row Sun–Fri 22:00–06:30 splits at 23:00 (22:00–23:00 "awake, alone").
- Every line saying Laura is asleep skips Sun–Fri 22:00–23:00 (her face in their room, "Ease the door open").
- Mark's and Ryan's lines say she has "gone up" or "gone to bed", not that she is asleep (DECISIONS 83).

## Why — the source of each key choice

| key choice | source |
|---|---|
| Laura alone, not the couple more often | LO, 2026-10-29 (DECISIONS 82) |
| 22:00–23:00, Mark reworded | LO, 2026-10-29 (DECISIONS 83) |
| the walk-in shape and pay | DECISIONS 79 |
| the prose | `v2-prose`, from the spec in chat · guess until LO signs |
| the counter, the step-3 line, the after-step-4 screens | `proposals/LAURA_R1_LADDER.md`, step 4 and "the gap after step 4" (signed 2026-11-01) |

## Changed after the build (2026-11-01), signed by LO 2026-11-01

| row | was | now |
|---|---|---|
| gate | none: open at Good Girl | `laura_step` gte 2: after the wine, "Mark hasn't looked at me like that since the wedding." Her want is shown before the gap |

## Explicit beats as built (measured 2026-11-03)

One row per explicit screen in the built game: 3 or more words on the build's own list, the count `gates.py` uses. A screen's variants fold into it, so a screen can hold more words than one visit shows. "Sits at" is the highest of the person's crude columns (SP2) that the screen uses. Where a screen's text differs from the prose above, the build is what plays.

| screen | words | counted words | sits at | the text |
|---|---|---|---|---|
| `laura_alone_in_bed` · `crack` | 175 | 7: ass, clit, tit, nipple, tits, moan, nipples | Laura's late column; also ass, clit | on this sheet above |
| `laura_alone_in_bed` · `watch` | 304 | 15: nipples ×4, clit ×3, tit ×2, nipple ×2, moan ×2, tits ×2 | Laura's late column; also clit | on this sheet above |
| `laura_alone_after` · `crack_after` | 136 | 5: ass ×2, clit, nipples, moan | Laura's late column; also ass, clit | on this sheet above |
| `laura_alone_after` · `watch_after` | 141 | 4: clit ×2, ass, nipples | Laura's late column; also ass, clit | on this sheet above |
