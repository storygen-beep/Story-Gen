# [READY] Scene — zoe_04_i_pick_the_dares

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–118): Zoe's release-1 ladder (`sheets/people/npc_zoe.md`, signed). Changed: the gate is her step 3 (Corruption 40 dropped); her admission and Ella's answer as the proposal ("I dared you instead of asking. I always do." / "Then keep daring me."); Zoe keeps picking (the built "From now on, I pick the dares." and Ella daring Zoe are cut); the repeat is now `zoe_dares`.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_zoe` · 4 (Zoe A 4) · her last step in 0.1 |
| where · when | Zoe's couch · Mon–Thu 18:00–22:00 and Sat 18:00–20:00 (not Friday: the party; not Saturday from 20:00: Zoe is at the party house) |
| gate | her step 3 · the boost off |
| want | "Took you long enough." (A 3); she still won't ask |
| next step | Zoe admits she dared instead of asking; @player takes the dares |
| hook | "Then keep daring me." Party nights are Zoe's; the dares open (`zoe_dares.md`) |
| what she wears here | not named |
| explicit? | no: a talk |
| who notices | Zoe's secret is hers |
| her_line_low · her_line_high | low: "It's a dare. It doesn't count." · high: "You want her to dare you something worse." (the person sheet's pair) | |

## The step row (as built, 2026-11-03)

The seven columns, filled from what the build does.

**Kind · stage:** a talk, her admission · no stage gate (her step 3)

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| Zoe's couch: she dared instead of asking | nobody: the two of them | none in the build | "Then keep daring me." (or "Okay.", back in 3 days) | the admission | yes | her step 4; `picks_the_dares`: her dares open at parties |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`zoe_04_i_pick_the_dares`** — Zoe's Living Room · Mon/Tue/Wed/Thu 18:00-22:00 · Sat 18:00-20:00 · Zoe there · needs Zoe's step = 3 · drinks boost off · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `couch` | Zoe's on her couch in a big T-shirt with her bare legs tucked under her, eating … | no | "Sit down next to her." → `asked` | — |
| `asked` | She says it to the cereal box. | no | "Then keep daring me." → `keep` | — |
| | | | "Okay." → Zoe's Living Room | back in 3 days |
| `keep` | She looks at you properly for the first time tonight. | no | "Every party." → Zoe's Living Room | Zoe's step = 4 · `zoe_04_done` set · `picks_the_dares` set |

## The repeat it turns into — party nights, her call (one sheet row)

> Drafted before the build and kept as the signed record. Where it differs, the branch map and the beats above say what the build does.

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
