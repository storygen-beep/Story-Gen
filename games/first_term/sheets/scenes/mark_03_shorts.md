# [READY] Scene — mark_03_shorts

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. the gate reads `mark_saw_her`; the counter row reads `rent_short`; the screens and buttons as built; the step row. file and line cites cut.

> **Changed 2026-11-02, signed by LO 2026-11-02** ("Signed, go with your recs, skip the play check"; DECISIONS 131, `sheets/READER_FAILS_A3.md`, Home): row 16: under Exhibitionism 20 both openings (his Power version and hers) add his look: "His eyes go down your legs under the table." ("When you sit, ..." on his version, where he doesn't look up as she comes in).

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–115): Mark's release-1 ladder (`sheets/people/npc_mark.md`, signed). Changed: the gate is his step 2 and one short week, ever (Corruption 20, Exhibitionism 20 and his Want 20 dropped); her voice row. The screens stand as built.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Every Mark step is written twice, by his Power: his terms (M) or hers (E).

| row | answer |
|---|---|
| person · step | `npc_mark` · 3 (Mark A 3) |
| where · when | the kitchen table · Sunday 08:00–12:00 |
| gate | `rent_starts` · `mark_step` eq 2 · `rent_short_weeks` gte 1 (she has been short at least once) · `mark_saw_her` · the boost off |
| why the counter | `rent_short` lasts only until a full payment, so it can't say "short once, ever". `rent_short_weeks` is the engine's durable count (DECISIONS 112, 144); the game declares it 0 in `[player.core_traits]` |
| want | "Friday, Frank." He knows she heard |
| next step | he sets what she wears to the table |
| hook | his dress rule stands at every count after |
| what she wears here | shorts: the step reads her short-skirt state or the scene equips shorts (guess) |
| which version | Power 50 or more (guess): his version · under 50: hers |
| explicit? | no: a dress dare (1 list word at most) |
| who notices | Mark |
| what she risks | his rule on her body, every Sunday |
| her_line_low · her_line_high | low (under the stage): "He's Mom's husband. Pay him and go." · high (over it): "You want him to lose count." (the person sheet names none; worded by me, signed by LO 2026-11-01) | |
| guidance card line | Sunday morning at the table, after a short week: Mark wants shorts this time. |

## The step row (filled from the build, 2026-11-03)

**Kind · stage:** a dress dare for one person she knows (Curious · Daring 20), after his accident.

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| Mark sets what she wears to the table: shorts | Mark | his rule on her body, every Sunday | "Fine." · "Go up and change." | he names the shorts, or she beats him to it | not a sex act | `mark_dress_rule` stands at every count |

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `start`, his version (Power 50+) | M: "Not the shirt this time. Shorts. Since you're listening." | no | "Fine." (Exhibitionism 20) → `shorts` · "I'm not changing for you." → `no` (parked) | "Fine.": his Power add +3 |
| `start`, hers (under 50) | E: she decides before he asks | no | "Go up and change." (Exhibitionism 20) → `hers_down` · "I'm not changing for you." → `no` (parked) | none |
| `hers_down` | she comes down already in her shortest pair: "Saved you asking." | no | "Sit down across from him." → `shorts` | his Power add −3 |
| `no` | the parked no | no | "Leave him to his envelope." → the hall | his Power add −2 |
| `shorts` | she sits; the curve of her ass; his count goes slow | no | "Count, Mark." → the hall | Mark's Want add +10 · exhibitionism add +3, cap 79 · `mark_step` set 3 · `mark_dress_rule` set · the Sunday count |

"I'm not changing for you." is parked: the short stays on the tab.

## Why — the source of each key choice

| key choice | source |
|---|---|
| both versions | the arc ideas, Mark A 3 (heat 10-06) |
| how the shorts are backed | guess |
