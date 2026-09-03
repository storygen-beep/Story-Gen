# PLACE · Vance Securities  `[READY]`

| | |
|---|---|
| **id** | `vance_securities` |
| **ENTERED FROM** | `spire_plaza` |
| **WAYS OUT** | back to `spire_plaza` |
| **DOOR** | no — a workplace with a lobby, and the lobby is `spire_plaza` |
| **LABELS** | `private` · `zone:spire` · `checks_cover` |
| **fill** | 1,500 `[INTENT]` |
| **heat** | cycling pool |

## What this place is FOR

Calloway's un-indexed file room, being audited shut. **The one place her own file might be** — which
is what she wants from him, and it is never what he wants from her.

**His secret is not a kink: he is starving to be believed.** Nobody has taken his hunt seriously in
two years. She does, and that is the whole seduction — and the first time in the game she is holding
something a man needs.

## The list — work + people

| # | row | canvas | kind | system | gate | effect | screen |
|---|---|---|---|---|---|---|---|
| 1 | "Work his case. (2h.)" | `TBD` | work | `seated` | `cover gte 10` **and** `clean gte 40` | `relation` `add` `+3` · `time` `add` `+120` | yes |
| 2 | Calloway | `TBD` | hub | `service` | `trigger.npc` = `npc_calloway`, 08:00–20:00 | — | yes |

⚠️ **Row 1 is work that pays in relation, not coin, and that is deliberate.** `the-economy.md` R1c
asks whether a repeatable leaves anything behind. This one deposits belief.

⚠️ **`cover` AND `clean` both gate the way in here** — the `checks_cover` label is read at
`spire_plaza` before she reaches this room at all, so an evening of `service` in the Reach locks the
Spire until she washes. That is the coupling the whole board is built on, and it is why `clean` is a
need rather than a chore.

## Walk-in — REQUIRED

He is scheduled and she works alone in the stacks. Banded on `relation`: the audit, and who else has
a key. His lever is belief, so the walk-in threatens the belief, not her body.

## Media

`scenes/rung_calloway_contact_t4` · `rung_calloway_oral_t5` — the two rungs on disk.
`sex/calloway_loop_*_t5` (4) · `sex/calloway_finish_*_t5` (3). **7 pools + 2 rungs.**

⚠️ His ceiling is **warm at the top**, because being believed is what he is paying for. That is a
register note, not a content limit — the words permitted are in `v2_state.json` `crude_ceiling`.
