# [REVIEW] System — <system id>

> One page: the design card. Rules: `references/the-sheets.md` S8 · `the-systems.md` SY1–SY4.
> Saved at `games/<slug>/sheets/systems/<system_id>.md`. Written before the place sheets.
> Recorded in `v2_state.json` as one `board.systems[]` entry (`state.md`). Worked cards: `templates/cards/`.

| row | answer |
|---|---|
| id · name (`id`, `name`) | <system_id> · <what the player calls it> |
| place and hours (`place`, `hours`) | <location_id> · <weekdays, open–close> |
| cost (`cost`) | <time · energy or a need · money> |
| one ladder or two (`one_ladder`) | `true` · `false` |
| people (`people[]`) | <npc_id, npc_id> |
| pool (`pool[]`, `daily`) | <canvas_id, canvas_id> · `daily = true` · `false` |
| memory (`memory`) | <rank · audience · owned · history> |
| growth (`growth`) | `climbs` · `decays` |
| sink and deadline (`sink`, `deadline`) | <what money leaves for> · <weekday or day of month> |
| feeds (`feeds[]`) | <system or meter id> |
| reads (`reads[]`) | <system or meter id> |
| link into the hook (`hook_link`) | <favor · debt · invite> |
| leads to (`leads_to[]`) | <npc_id or canvas_id> |

## Pay ladder (`pay_ladder[]`)

| rung | gate | pay |
|---|---|---|
| <1> | <trait op value> | <amount> |

## Lewd ladder (`lewd_ladder[]`)

| rung | gate | acts (`acts[]`) |
|---|---|---|
| <1> | <trait op value> | <act, act> |

## The meters it writes and reads (`board.meters[]`)

| meter id | kind | key | fed at | read by |
|---|---|---|---|---|
| <meter_id> | `ambient` · `sourced` | <trait or flag> | <location_id> | <one line — what changes because of it> |
