# [READY] Scene — laura_02_home_late

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08.

| row | answer |
|---|---|
| person · step | `npc_laura` · 2 (Laura C 2) |
| where · when | the hall, the dark stairs · any night 23:00–01:00, home late |
| gate | `came_home_late` · Exhibitionism 20 · her Want 10 · the boost off |
| want (test 1) | she looked too long at the dress (step 1) |
| next step (test 2) | the first catch: punishment or questions, by her Warmth |
| hook (test 3) | "Did anyone look at you in it?"; the catches go on |
| what she wears here (test 8) | the dress line only in a group on `laura_blue_dress` worn |
| explicit? | no |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `stairs` | shoes in her hand; Laura on the dark stairs in her robe; what she smells and asks follows the late flag: `late_party` smoke and cologne · `late_shift` coffee and the café · `late_date` nothing, she just looks · none: "Where were you?" | no | → `low` or `high`, by Laura's Warmth | `laura_suspicion` add +5 (home late) |
| `low` | Warmth under 40 (guess): "You're grounded. A week." | no | "Fine." → her room · the truth, by the flag ("Zoe's." · "Work." · "Out with Jake." · "Just walking.") → her room · a different place than the flag says, "(she'll know)" → `lie` | `curfew` set true |
| `high` | Warmth 40 or more: "Did anyone look at you in it?" | no | "Everyone." → her room | Laura's Want add +10 · `laura_step` set 2 |
| `lie` | she knows; her mouth goes thin | no | "Goodnight, Mom." → her room | Laura's Warmth add −5 · `laura_suspicion` add +5 |

**Her suspicion reads this screen** (LO, 2026-10-08): low, "Where were you?"; high, she checks the dress and the smell of her hair. At 50, the curfew comes even at middling Warmth.

## Why — the source of each key choice

| key choice | source |
|---|---|
| the catch, both versions | the arc ideas, Laura C 2 · SP2 (low Warmth, a curfew) |
| lying is labelled "(she'll know)" | the arc ideas, Laura C |
| suspicion's two readers and the 50 | LO, 2026-10-08 (questions 5, 20) |
| the Warmth edge at 40 | guess |
| the catch says the true reason; only a wrong reason is the lie | LO's play note, 2026-10-08 · sweep A2-02 |
