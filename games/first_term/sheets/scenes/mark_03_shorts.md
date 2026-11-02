# [REVIEW]] Scene — mark_03_shorts

> **Changed 2026-11-02, signed by LO 2026-11-02** ("Signed, go with your recs, skip the play check"; DECISIONS 131, `sheets/READER_FAILS_A3.md`, Home): row 16: under Exhibitionism 20 both openings (his Power version and hers) add his look: "His eyes go down your legs under the table." ("When you sit, ..." on his version, where he doesn't look up as she comes in). Built in `mark.py`.

> **Changed 2026-11-01, re-signed by LO 2026-11-02** ("Signed, go ahead and build"; DECISIONS 124, the heat ladder a2): its gate or pay changes; the row is in `sheets/HEAT_LADDER_A2.md`.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–115): Mark's release-1 ladder (`sheets/people/npc_mark.md`, signed). Changed: the gate is his step 2 and one short week, ever (Corruption 20, Exhibitionism 20 and his Want 20 dropped); her voice row. The screens stand as built.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Every Mark step is written twice, by his Power: his terms (M) or hers (E).

| row | answer |
|---|---|
| person · step | `npc_mark` · 3 (Mark A 3) |
| where · when | the kitchen table · Sunday 08:00–12:00 |
| gate | `rent_starts` · `mark_step` eq 2 · player counter `rent_short_weeks` gte 1 (she has been short at least once) |
| why the counter | `rent_carried` is read for 48 hours and cleared by `vance_knock` (`mark.py:444-447`), so it can't say "short once, ever". `rent_short_weeks` is the engine's durable count (DECISIONS 112); the game declares it 0 in `[player.core_traits]` |
| want (test 1) | "Friday, Frank." He knows she heard |
| next step (test 2) | he sets what she wears to the table |
| hook (test 3) | his dress rule stands at every count after |
| what she wears here (test 8) | shorts: the step reads her short-skirt state or the scene equips shorts (guess) |
| which version | Power 50 or more (guess): his version · under 50: hers |
| explicit? | no: a dress dare (1 list word at most) |
| who notices | Mark |
| what she risks | his rule on her body, every Sunday |
| her_line_low · her_line_high (rule 7) | low (under the stage): "He's Mom's husband. Pay him and go." · high (over it): "You want him to lose count." (the person sheet names none; worded by me, signed by LO 2026-11-01) | |
| guidance card line | Sunday morning at the table, after a short week: Mark wants shorts this time. |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `m` | M: "Not the shirt this time. Shorts. Since you're listening." | no | "Fine." → `shorts` · "I'm not changing for you." → parked | none |
| `e` | E: she comes down already in her shortest pair: "Saved you asking." | no | → `shorts` | none |
| `shorts` | she sits; the curve of her ass; his count goes slow | no | "Count, Mark." → the hall | Mark's Want add +10 · exhibitionism add +3 · `mark_step` set 3 · `mark_dress_rule` set |

"I'm not changing for you." is parked: the short stays on the tab.

## Why — the source of each key choice

| key choice | source |
|---|---|
| both versions | the arc ideas, Mark A 3 (heat 10-06) |
| how the shorts are backed | guess |
