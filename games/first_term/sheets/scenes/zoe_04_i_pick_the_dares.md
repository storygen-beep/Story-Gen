# [READY] Scene — zoe_04_i_pick_the_dares

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–118): Zoe's release-1 ladder (`sheets/people/npc_zoe.md`, signed). Changed: the gate is her step 3 (Corruption 40 dropped); her admission and Ella's answer as the proposal ("I dared you instead of asking. I always do." / "Then keep daring me."); Zoe keeps picking (the built "From now on, I pick the dares." and Ella daring Zoe are cut); the repeat is now `zoe_dares`.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_zoe` · 4 (Zoe A 4) · her last step in 0.1 |
| where · when | Zoe's couch · Mon–Thu 18:00–22:00 and Sat 18:00–20:00 (not Friday: the party; not Saturday from 20:00: Zoe is at the party house) |
| gate | `zoe_step` eq 3 · the boost off (was Corruption 40) |
| want | "Took you long enough." (A 3); she still won't ask |
| next step | Zoe admits she dared instead of asking; @player takes the dares |
| hook | "Then keep daring me." Party nights are Zoe's; the dares open (`zoe_dares.md`) |
| what she wears here | not named |
| explicit? | no: a talk |
| who notices | Zoe's secret is hers |
| her_line_low · her_line_high | low: "It's a dare. It doesn't count." · high: "You want her to dare you something worse." (the person sheet's pair) | |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `couch` | Zoe: "You didn't need me in the hot tub. You were the dare." | no | → `asked` | none |
| `asked` | Zoe: "I dared you instead of asking. I always do." | no | "Then keep daring me." → `keep` · "Okay." → the apartment (parked) | none |
| `keep` | Zoe grins, slow: "Friday, then. And Saturday. Every party." | no | "Every party." → the apartment | `zoe_step` set 4 · `picks_the_dares` set (the flag name stays; it now means the dares are open, Zoe picking) |

No "last night" in the lines: this step can come any evening after the hot tub (the truth rule).

## The repeat it turns into — party nights, her call (one sheet row)

| row | answer |
|---|---|
| where · when | Zoe's Friday party |
| what happens | `zoe_dares` opens: one dare a night, Zoe picks it (`zoe_dares.md`); the built `party_dare` is replaced |
| explicit? | the dare screens are; `party_dare`'s sheet carries the beat |
| BRAKE | one dare a night (was two) |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Zoe A 4 (heat 10-06) |
| "Not that one, babe." parked | SP2 (Zoe's no) |
| "Dare Zoe" in the pool | guess |
| fix from the false-line sweep | sweep A4-09 (2026-10-08) |
