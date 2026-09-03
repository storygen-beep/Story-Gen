# PLACE · Kess's Berth  `[READY]`  ★ HOME BASE

| | |
|---|---|
| **id** | `kess_berth` |
| **ENTERED FROM** | `underworld_strip` |
| **WAYS OUT** | back to `underworld_strip` |
| **DOOR** | no — she lives here. A door is where she is the visitor. |
| **LABELS** | `private` · `zone:reach` · `home_base` · `has_bench` · `she_can_undress` |
| **fill** | 3,000 `[INTENT]` |
| **heat** | cycling pool |

## What this place is FOR

**Three jobs in one room, and that is why it is the second-biggest budget in the game.**

1. **Her bed.** `board.map.home_base`.
2. **The feed line** — the only fill point for `charge`, and the obligation: 10 coin a night.
3. **The bench** — the ONLY place `seated` is written. Carries `has_bench`, and it is the one label
   in the game that exactly one room holds.

That third one is the whole design. `the-systems.md` SY2: *"the payoff of a thin room is not
thinness — it is being the only source of something."* `family-ties` feeds piercings in **2 rooms**
and reads them in **117 passages**.

## The list — needs + work + people

| # | row | canvas | kind | system | gate | effect | screen |
|---|---|---|---|---|---|---|---|
| 1 | "A night on the line. (10 coin.)" | `TBD` | need | `charge` | `coin gte 10` | `charge` `set` `100` · `clean` `set` `100` · `coin` `add` `-10` · `time` to 07:00 | yes |
| 2 | "Hold still." | `TBD` | act | `seated` | `relation gte N` per rung | `seated` `add` `+1` | yes |
| 3 | Kess | `TBD` | hub | `seated` | `trigger.npc` = `npc_kess`, 10:00–22:00 | — | yes |

**Three rows** — the field median for things-to-do-at-a-place is exactly 3.

⚠️ **THE WARDROBE IS NOT A ROW, AND WRITING ONE IS A KNOWN DEFECT.** This sheet declared
*"The wardrobe."* as a fourth row until F4 was read properly. Declaring
`wardrobe_location = "kess_berth"` renders `[[Change Clothes->WardrobePage]]` on this location's
screen **unconditionally** (`v2.py:9814`), above the portrait row and above the activity list, on
every visit, needing nothing from us. An authored canvas beside it is a **second door**, and
`orientation` shipped exactly that — the authored one is the one that does not work.

So the `cover` system's door here is the engine's, and it is free.

⚠️ **Row 1 is the game's ONLY money outflow of size, and gate 24 reads it.** It must charge `10`
`coin` via a `costs` entry, because gate 24 compares `obligation_amount` against the **largest
single authored outflow** (`gates.py:5901`). `[settings.rent]` is deliberately not used: `due_day`
takes weekday names only and arms at 00:00 (`engine.md` §26), so the engine's system is weekly.
**One channel. No authored canvas narrates a payment the engine is making.**

⚠️ **Row 2's brake is on the TRIGGER** (S9). `trigger.max_triggers_per_day = 1`, not a cost on an
inner choice. Three rounds of adding costs to inner choices moved nothing; moving the same costs to
the triggers fixed five meters at once.

## Walk-in (R3) — REQUIRED

Kess is scheduled and she does solo things here. Banded on `seated`: what he does while she is on
the bench and thinks she is only being repaired.

## Media

`videos/portraits/wren_*.jpg` — **8 states already on disk**, and this is the room where she
undresses, so it is where the state-reactive sidebar portrait earns itself.
Kess has **no act pools** and needs none: his ceiling is the seam, not sex.
