# [REVIEW] Scene — laura_01_blue_dress

> Changed 2026-11-04 to match the build; waits for LO's re-sign. The invite's button: "Follow her to her room." (Q7). The first screen's id is still `upstairs` in the build.

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. the first screen is `upstairs`, "Try it on."; the cap; the step row.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Go ahead")** (DECISIONS 99–114): Laura's release-1 ladder (`sheets/people/npc_laura.md`, signed). Changed: the step pays Love +5 and Exhibitionism +3 (Want +10 dropped: nothing of hers reads Want); her voice rows added. The screens and lines stand as built.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_laura` · 1 (Laura C 1) |
| where · when | the kitchen, then the master bedroom · Tuesday 18:00–22:00, day 2 or later · it starts only from "Follow her to her room." in Laura's kitchen hub (that choice sets `laura_dress_invite`), never by walking into the bedroom |
| gate | none: step 1, day 2 |
| want | none before it: step 1, and it says so |
| next step | she dresses her daughter, and lingers |
| hook | the dress is hers now; it comes home late (step 2) |
| what she wears here | Laura's blue dress: the scene adds and equips it |
| her stage here | Good Girl: shy choices only (SP2) |
| explicit? | no |
| her_line_low · her_line_high | low (under the stage): "That's your mom. Go to bed." · high (over it): "She's lonely, and you can't stop watching her be lonely." (the person sheet's pair; at step 1 the high line is worded for the mirror: "She's looking at you like a stranger would. You don't hate it.", the built thought) |
| what changes after | the dress is Ella's; Laura's line on it (`npc_laura.md`, her line: her blue dress) |

## The step row (filled from the build, 2026-11-03)

**Kind · stage:** borrowed clothes: her mother's dress (Good Girl · Covered).

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| Laura dresses her in her own old dress and looks at her in the mirror | Laura, behind her in the mirror | empty: step 1 | "Try it on." | Laura smooths it over her hips: "It never fit me like that." | not a sex act | the blue dress is hers; step 2 |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `upstairs` | her room; Laura takes a blue dress from the back of her wardrobe: "Here. Try it." (the invite, "Follow her to her room.", is in her kitchen hub) | no | "Try it on." → `mirror` | none |
| `mirror` | the blue dress, tight across her chest; Laura smooths it over her hips | no | "Is that bad?" → `no` · "I can't take this." → `give` (parked) | `laura_blue_dress` added and worn |
| `no` | "It never fit me like that." — "No." — "Keep it. Wear it somewhere somebody can see you in it." | no | "Thank you, Mom." → her room | Laura's Love (`warmth`) add +5 · exhibitionism add +3, cap 79 · `laura_step` set 1 · `laura_01_done` set |
| `give` | "Keep it. Wear it somewhere." Laura doesn't take it back | no | "Okay." → her room | `laura_blue_dress` kept · Laura's Love add +5 (the built extra +3 on this exit is dropped: one pay per step) · exhibitionism add +3 · `laura_step` set 1 · `laura_01_done` set |

Who notices: Laura, behind her in the mirror.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Laura C 1 (heat 10-06) |
| day 2, shy choices only | SP2 §6 (kept) |
| the dress is equipped by the scene | the truth rule · guess for the mechanism |
| fix from the false-line sweep | sweep A2-09 (2026-10-08) |
| Love +5, not Want +10 | `proposals/LAURA_R1_LADDER.md`, the numbers (signed 2026-11-01) |
