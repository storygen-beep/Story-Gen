# [READY] Scene — park_hidden

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign.

> The signed plans behind this page: `proposals/COPY_FIXES_C.md`.

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08. An explicit pool scene of the park (`park_hidden`): Zoe, after
> their run, somewhere nobody sees.

| row | answer |
|---|---|
| system · pool | the park · `park_hidden` |
| where · when | the park, after a run with Zoe · Sat and Sun 08:00-09:30, within an hour of the run |
| gate | Corruption 60 · her step 3+ · `ran_with_zoe` · pays cap 79 |
| who sees | a man walking his dog looks and walks on; joggers pass close |
| want | Zoe grabs her wrist: "Come here. I know a place." |
| next step | her fingers in Ella in the hollow, joggers yards away |
| hook | "Same time next weekend. Don't be late." |
| what she wears here | not named |
| BRAKE | once a day, on the trigger |
| raises | corruption add +1 (the repeat raise) |
| no clit in the prose | Zoe's middle column has tits, nipples, wet; clit is her late column |
| the crude-word ceiling | Zoe's middle column: tits, nipples, wet · early: tits, ass (LO, 2026-10-08) |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`park_hidden`** — Park · Sat/Sun 08:00-09:30 · needs Corruption 60+ · Zoe's step 3+ · `ran_with_zoe` · under 1h since `ran_with_zoe` · repeatable · 1 a day

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `pull` | Zoe jogs to a stop beside you, pink and breathless, and grabs your wrist. | no | "Follow her." → `hidden` | Hygiene -10 · costs Energy 10 |
| | | | "Not here, Zo." → `no` | — |
| `hidden` | A man walking his dog slows on the path above the hollow, looks your way, and … | yes | "Back to the path." → `after` | Corruption +1 (cap 79) |
| `after` | She jogs off backwards, grinning, and doesn't fix her hair. | no | "Don't you be late." → Park | — |
| `no` | She laughs and runs off ahead, looking back over her shoulder every few strides. | no | "Let her run on." → Park | — |

## The explicit beats, as built (2026-11-03)

Every screen the build counts as explicit (3+ words from the frozen list), word for word, with its measurement. It replaces the drafted text.

**`park_hidden` · `hidden`** — 140 words · 5 counted: kiss, ass, nipple, orgasm, moan · ceiling: Zoe's middle column: tits, nipples, wet

> A man walking his dog slows on the path above the hollow, looks your way, and walks on.
>
> Zoe drags you off the path into the hollow behind the rhododendrons. Joggers pound past a few yards away. She shoves you against a tree and kisses you hard, both of you still panting from the run.
>
> Quiet, babe.
>
> She breathes. Her hand slides down inside, flat on your skin, and finds you wet. Her fingers start slow. You grab her ass and pull her in. Her thumb finds your nipple and rubs. Footsteps crunch past, close enough to touch, but Zoe doesn't stop. Her fingers go fast, deep, until your hips buck into her hand. Your orgasm hits and your knees give out. Zoe pins you to the bark with her whole body, her mouth on yours to swallow every moan.

## Why — the source of each key choice

| key choice | source |
|---|---|
| hidden, with someone she knows, at stage 3 | LO, 2026-10-08 (SYSTEMS §14, the park sheet) |
| Zoe's hand makes her come; no oral (Zoe A 6) | LO, 2026-10-08 (heat call A) |
| Zoe in the park on weekend mornings | LO, 2026-10-08 (question 7) |
| after Zoe A 3 | guess: their first kiss comes first |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| "still panting from the run" only after `ran_with_zoe` (set by running with Zoe, read for 2 hours); otherwise she walked in, and the line says so | sweep A6-09 |

## Changed 2026-11-02 (reader a3, `READER_FAILS_A3.md`, signed by LO 2026-11-02; DECISIONS 131)

- Row 53. "Not here, Zo." no longer sets `park_cool_zoe`; it moves Zoe's Lust −1. Note: Zoe has no declared core traits (none declared), so her Lust starts at 0 and the −1 clamps there; nothing reads it yet. `party_cool_zoe` (the dare's no) is also set and never read.
