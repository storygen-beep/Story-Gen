# [REVIEW] Scene — laura_curfew_rule

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. once a day; the truths by where she was; want, next step and hook rows.

> **New 2026-11-01, signed by LO 2026-11-01 ("Go ahead")** (DECISIONS 99–114). From Laura's signed release-1 ladder
> (`sheets/people/npc_laura.md`; `proposals/LAURA_R1_LADDER.md`). The built canvas `laura_02_home_late`, moved: no longer her step 2; a repeatable owned by her suspicion.

| row | answer |
|---|---|
| system | her suspicion (`laura_suspicion`), `npc_laura.md` |
| where · when | the dark stairs, `home_hall` · her stairs row, every day 23:00–02:00, only when `came_home_late` was set in the last 4 hours (as built) |
| gate | `came_home_late` set · Laura present (her stairs row). No `laura_step` read |
| fires | once a day at most (`laura_caught_today`), within 4 hours of `came_home_late` |
| want | Laura's, on the high side: "Did anyone look at you?" |
| next step | none: a house rule, not a step |
| hook | the curfew: 7 days |
| what changes | no `laura_step` set, no `laura_02_done`, no Want. Every screen, line, and the low/high split by Love 40 or suspicion 50 stand as built |

## Branch map — one row per screen

| node | what happens | exits | effects |
|---|---|---|---|
| `stairs` | Laura on the stairs in the lamp; what she smells follows the late flag (as built) | "Wait for it." → `low` or `high` | `laura_suspicion` add +5 |
| `low` | "You're grounded. A week." | "Fine." · the truth ("Zoe's.", "Work." or "Out with Jake.", by where she was) → her room · a lie ("... (she'll know)") → `lie` | curfew 7 days · `came_home_late` cleared |
| `lie` | "Bed. Now." | "Goodnight, Mom." → her room | Laura's Love add −5 · `laura_suspicion` add +5 · the curfew |
| `high` | "I'm not angry. I was nineteen once." · "Did anyone look at you?" | "Everyone." → her room | `came_home_late` cleared (was: Want +10, `laura_step` 2) |

## Why

| key choice | source |
|---|---|
| it becomes the curfew rule | `proposals/LAURA_R1_LADDER.md`, "Moved to their owners" (signed 2026-11-01) |
| `high` pays nothing | nothing of hers reads Want; the proposal moves no pay here. confirmed by LO 2026-11-01 ("Go ahead") |
