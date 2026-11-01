# [READY] Scene — mark_sunday_table

> **New sheet 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–115). The built canvas `mark_sunday_table`
> (`iterations/002/build_scripts/mark.py:379`), the Sunday count after Mark's step 1. Its old sheet was `mark_09`
> (cut). From Mark's signed release-1 ladder (`sheets/people/npc_mark.md`, step 4, "After") and the rent sheet
> (`sheets/systems/money_pressure.md`: no price on her body). No explicit screen; the new lines are mine.

| row | answer |
|---|---|
| system | the rent (`money_pressure.md`) · Mark |
| where · when | the kitchen table · Sunday 08:00–12:00, once a Sunday (as built) |
| gate | `mark_step` gte 1 · `rent_starts` · not counted today (as built) |
| which version | his terms (Power 50+) or hers, as built |
| raises | his Want add +2 (as built, stored) |
| explicit? | no: he looks |

## What changes

**Cut (the paid route):** from `counted`, the wallet line ("He counts the twenties in his wallet…") and both
"Twenty, and you can look." exits; the screens `look_his`, `look_hers` and `cover`; the beats they load
(`beat_mark_table_look_*.txt`) and their two clip pools. `counted` keeps one exit, "Leave him to his envelope."

**Kept:** the whole `table` screen: his terms or hers, the dress-rule lines, what she wears, short or full, the
streak lines, "Next Sunday. Same table."

**New, after his step 4** (`mark_arrangement` set):
- His count line. In place of the built "He counts it slow" (short) and "He counts it twice anyway" (full), he
  counts at normal speed: "He counts it once, at normal speed, and his eyes don't go to the money once." Short
  weeks keep the pencil line after it.
- One line a week from a pool of five (`block_pool`, `memory = "seen"`, `seen_weight = 0`: no line repeats until
  all five have shown, DECISIONS 112). The Sunday table is once a week, so it is a new line each week for five weeks.

## The pool, written (mine, signed by LO 2026-11-01)

1. "He slides the envelope across to you to check, and keeps his fingers on it a second after you've taken it."
2. "He doesn't say good morning. He says your name, once, and then he counts."
3. "He puts the pencil behind his ear and looks at you instead of writing anything down."
4. "He licks his thumb, and stops, and counts the rest without it."
5. "When you stand up he watches you all the way to the door. He doesn't pretend he isn't."

Truth: no line names a past Sunday or where anyone else is (Laura is out on Sunday mornings, `mark.py:63`).

## Why — the source of each key choice

| key choice | source |
|---|---|
| the paid exits cut | `proposals/MARK_R1_LADDER.md`, "Cut": "the Sunday table's twenties at Mark step 7" |
| normal speed, his eyes on her, a new line per week | the same, step 4 reworked, "What changes after" |
| the shuffle-bag pool | DECISIONS 112 (`seen_weight = 0`) |
| the five lines | mine, signed by LO 2026-11-01 |
