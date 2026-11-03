# [READY] Scene — laura_04_she_saw_you

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. "Stay where you are." pays cap 59 as built; the gate reads `laura_alone_seen`; the breakfast's second screen; the step row. the explicit beats as built, measured. file and line cites cut.

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> **Changed 2026-11-01 after the build, signed by LO 2026-11-01 ("Signed, build them")** (the reader's FAILs; LO's picks in chat): the breakfast points ahead.

> **New 2026-11-01, signed by LO 2026-11-01 ("Go ahead")** (DECISIONS 99–114). From Laura's signed release-1 ladder
> (`sheets/people/npc_laura.md`; `proposals/LAURA_R1_LADDER.md`). Her top step. Replaces the built step 4 slot (`laura_04_ryans_door`, moved to Ryan).
> The explicit screens are written by `v2-prose` and measured: below.

| row | answer |
|---|---|
| person · step | `npc_laura` · 4 of 4 (new, top step) |
| where · when | her door, `home_master_bedroom` from the landing · Sun–Fri 22:00–23:00, Laura in and awake, Mark downstairs: it takes the `laura_alone_in_bed` slot that night (higher priority) |
| gate | Corruption 20 · her Love 30 · `laura_step` eq 3 · `laura_gaps_watched` gte 3 · `laura_alone_seen` · the boost off |
| the counter | `laura_gaps_watched` (player trait, declared 0): +1 on "Keep watching." in `laura_alone_in_bed` and in `laura_shower_gap`. Name mine; confirmed by LO 2026-11-01 ("Go ahead") |
| want | the alone-in-bed line names the dressed-up night (`laura_lonely`, step 3) |
| next step | Laura comes, and sees her |
| hook | "Ryan." `laura_said_ryan` set, for a later release |
| who notices | **Laura sees Ella** |
| what she risks | being caught watching her mother |
| what she wears here | Laura: her nightdress (named in prose) · Ella: not named |
| her voice | stage 2 (Curious) |
| the crude-word ceiling | Laura's late column: pussy, wet (SP2), with the park's tits, nipples, ass, clit · no cunt, fuck, cum, cock. confirmed by LO 2026-11-01 ("Go ahead") |
| her_line_low · her_line_high | low: "That's your mom. Go to bed." · high: "She's lonely, and you can't stop watching her be lonely." | The low line is the thought "You should walk away" in `gap`; the high side is "you stay, because you want to watch her". |
| mixed act? | no: watching, unseen until the end. Corruption only (`meters.md` rule 3) |
| does it finish | yes: Laura comes before she sees her |

## The step row (filled from the build, 2026-11-03)

**Kind · stage:** she watches (Curious · Daring 20), and is seen: an accident-watching scene turned into her mother seeing her.

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| Laura comes whispering "Ryan.", opens her eyes, and sees her daughter at the door | Laura sees her | being caught watching her mother | "Keep watching." · "Stay where she can see you." | Laura doesn't pull the sheet up: "Go to bed, sweetheart." | yes: Laura comes | `laura_said_ryan`; the breakfast; the after-step-4 gap |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `gap` | the door a hand's width again; Laura fingering herself, biting her hand, close | yes | "Keep watching." → `comes` · "Pull the door to." → the hall | `saw_laura_alone`, `laura_alone_seen` set (on every exit) |
| `comes` | she comes; through her teeth she whispers "Ryan."; her eyes stay shut | yes | "Stay where you are." → `eyes` | corruption add +1, cap 59 · `laura_gaps_watched` add +1 |
| `eyes` | her eyes open on the door, on you; she doesn't pull the sheet up | no | "Step back from the gap." → `back` · "Stay where she can see you." (Curious) → `stay` | none |
| `back` | from the dark: "Go to bed, sweetheart." | no | "Back to your room." → her room | Laura's Love add +5 · `laura_step` set 4 · `laura_04_done` set · `laura_said_ryan` set |
| `stay` | she holds your eyes; "Go to bed, sweetheart."; the lamp goes off | no | "Back to your room." → her room | the same as `back` |

**The no** ("Pull the door to." on `gap`): nothing pays; the step waits for the next night (the gap's own once-a-night brake).
**"Stay where she can see you."** pays nothing more than the step. The proposal names no pay for it; confirmed by LO 2026-11-01 ("Go ahead").

## The explicit screens, written

Written by `v2-prose` and measured by `gates.py --beat`, 2026-11-01. The tool's rung check lists `vaginal` on `comes` for her fingers inside her; that is her own hand, alone.

**`gap`** · 138 words · explicit words 6 · median sentence 12 · act rungs: hands

> Laura's door is open a hand's width again, and the lamp is low. She lies on top of the sheet with her nightdress pushed up to her waist. Her knees are apart. Her fingers slide slow through her pussy, and you can hear how wet she is. You should walk away. You know it, but you stay, because you want to watch her. She rubs her clit in small circles, then harder. Her tits shake under the thin cotton, nipples stiff against it. She bites the back of her other hand to keep the moan in. Downstairs, Mark's TV mutters on. Heat climbs your chest. Your own nipples tighten and you're wet too, but your hands stay flat on the wall. Laura's thighs start to tremble. Her hips lift off the bed as she pushes two fingers inside.

*The last sentence:* her hips lifting, two fingers going in. On the body; the tool flags it only because "hips" and "fingers" aren't on its list.

**`comes`** · 129 words · explicit words 7 · median sentence 7 · act rungs: hands, vaginal (her own fingers)

> Two of her fingers are deep inside her pussy, and her thumb rubs her clit in hard, fast circles. Her hips lift off the bed. Her thighs clamp shut around her hand. She bites down on her knuckles to hold the moan in, but her whole body is shaking. Then she comes. Her back arches and her ass leaves the sheet. Through her teeth, against her own hand, she whispers one name. "Ryan." Not Mark. You hear it clearly. She sags onto the mattress, still breathing hard, her fingers still buried in her wet pussy. Her eyes stay shut. Her chest heaves under the lamp. Your nipples are hard and aching. You press your thighs together at the gap in her door, but your own pussy only gets wetter.

*The last sentence:* your thighs pressed together, wetter. On the body; what the name means is the next screen.

## The other screens (not explicit; mine, for LO to read)

**`eyes`:** "Laura's eyes open. They go straight to the door. To the gap. To you." · "She doesn't pull the sheet up fast. She doesn't pull it up at all. She lies there with her hand still between her legs, and she looks at you." · *(thought)* "Ryan. She said Ryan. Not Mark."

**`back`:** "You step back into the dark of the landing. Your heart is going so hard you can hear it." · Laura, quietly, through the gap: "Go to bed, sweetheart."

**`stay`:** "You don't move. You let her see you." · "Laura holds your eyes for a long second. Her face doesn't change." · Laura, quietly: "Go to bed, sweetheart." · "She reaches out and turns off the lamp."

## Breakfast, next morning (own canvas `laura_04_breakfast`)

| row | answer |
|---|---|
| where · when | the kitchen, her breakfast row (Mon–Fri 06:30–08:00), the first one after step 4 · once (`laura_04_breakfast_done`) |
| gate | `laura_04_done` · Laura present |
| the truth | "last night" shows only when step 4 was under 12 hours ago (`hours_since_flag` `laura_04_done` lt 12); after a Friday night her next breakfast is Monday, and the line reads "the other night" |

| node | what happens | exits | effects |
|---|---|---|---|
| `table` | Laura pours your coffee without looking up: "We don't talk about last night." (or "the other night") | "Okay, Mom." → the kitchen · "You should talk to Mark." → `mark` ("Eat your toast." → the kitchen) | first: Laura's Love add +5 · second: `laura_suspicion` add −5 · Laura's Love add +2 · both: `laura_04_breakfast_done` set |

Lines: "Laura is at the counter in her robe, pouring two coffees. She puts yours down in front of you and doesn't look up." · Laura: "We don't talk about last night." · on "You should talk to Mark.": "She laughs, once, without anything in it. 'Eat your toast, sweetheart.'"

## Why — the source of each key choice

| key choice | source |
|---|---|
| the step, the gap, "Go to bed, sweetheart.", the breakfast | `proposals/LAURA_R1_LADDER.md`, step 4 (signed 2026-11-01) |
| "Ryan." | LO, 2026-11-01 |
| the counter counts both gaps | the same, "The counter" |
| "the other night" after a Friday | the truth rule: her breakfast row is weekdays only (`npc_laura.md`, schedule grid) |
| the counter name, the 12-hour line | guess, confirmed by LO 2026-11-01 ("Go ahead") |

## Changed after the build (2026-11-01), signed by LO 2026-11-01

A hook line, proposed (LO asked whether a line solves it). Each line names a thing that is in the game and comes next, so it is true; a line that points at nothing would break the truth rule instead.

| node | the closing line (mine, signed) | what it points at |
|---|---|---|
| breakfast `table`, `mark` | *(thought)* "Tonight her door will be open a gap again. You both know it." | the after-step-4 gap (`laura_alone_after`), weeknights 22:00 |

## Explicit beats as built (measured 2026-11-03)

One row per explicit screen in the built game: 3 or more words on the build's own list, the count `gates.py` uses. A screen's variants fold into it, so a screen can hold more words than one visit shows. "Sits at" is the highest of the person's crude columns (SP2) that the screen uses. Where a screen's text differs from the prose above, the build is what plays.

| screen | words | counted words | sits at | the text |
|---|---|---|---|---|
| `gap` | 143 | 6: nipples ×2, pussy, clit, tits, moan | Laura's late column; also clit | on this sheet above |
| `comes` | 129 | 7: pussy ×3, clit, moan, ass, nipples | Laura's late column; also ass, clit | on this sheet above |
