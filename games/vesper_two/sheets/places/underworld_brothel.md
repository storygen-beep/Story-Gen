# PLACE · The House  `[READY]`

| | |
|---|---|
| **id** | `underworld_brothel` |
| **ENTERED FROM** | `underworld_strip` |
| **WAYS OUT** | back to `underworld_strip` |
| **DOOR** | no — a place of business |
| **LABELS** | `private` · `zone:reach` · `she_can_undress` |
| **fill** | 2,500 `[INTENT]` |
| **heat** | cycling pool |

## What this place is FOR

**Work, priced by the act.** The honest version of what the company does to her: he pays, and he
does not care whose body is in the slot. It is where the `service` tier is earned fastest and where
the money is worst per hour of clock.

Marsh books the same slot every Sunday. **The slot has to be bought off whoever holds it** — that is
Rue's obstacle from the shipped game, folded onto the economy after she was cut from the cast. The
coin is the obstacle now, which is `the-economy.md` R4: money is not a scene, and a sink belongs
where the thing being bought lives.

## The list — work + people

| # | row | canvas | kind | system | gate | effect | screen |
|---|---|---|---|---|---|---|---|
| 1 | "Take an hour. (by the act.)" | `TBD` | work | `coin` · `service` | `clean gte 40` | `coin` `add` `+N` · `service` `add` `+3` · `clean` `add` `-30` | yes |
| 2 | "Buy Sunday's slot. (20 coin.)" | `TBD` | work | `coin` | Saturday only | `coin` `add` `-20` · flag | yes |
| 3 | Marsh | `TBD` | hub | `service` | `trigger.npc` = `npc_marsh`, 20:00–23:59, Sunday | — | yes |

⚠️ **Row 1 is day-capped on the TRIGGER** — `trigger.max_triggers_per_day = 1`, plus a `_today` flag
cleared in `[engine.daily_tick]`. Vesper shipped this exact surface granting **+30 coin every 120
minutes with no cost, no cap and no daily limit**, plus two more like it. Being behind a tier gate
is not a cap: the tier is bought once, the rung repeats.

⚠️ **A day-cap has three parts and vesper shipped two.** The flag must be READ `is_false` on the
trigger, SET by a choice inside, and CLEARED in `[engine.daily_tick]`. Two of three validates and
throttles nothing.

## Walk-in — REQUIRED

Marsh is scheduled, she works alone. Banded on `service`: who is in the next room, and whether the
door was shut.

## Media

`sex/marsh_*_t5` (7) · `sex/brothel_*_t5` (6) — **13 pools on disk.** The `brothel_*` set is the
generic surface for row 1; `marsh_*` is his.
