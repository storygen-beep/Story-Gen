# SYSTEM · service — who she will let use her, and where  `[READY]`

| | |
|---|---|
| **kind** | `ambient` — fed at every act surface, which is most rooms |
| **key** | `service` (0–100) — **an ascent tier** |
| **fed at** | every act surface: `underworld_bar` · `bastien_backroom` · `underworld_brothel` · `mercer_room` · `penthouse` · `renner_depot` · `vance_securities` |
| **labels** | `private` · `she_can_undress` |
| **mechanism** (S8) | a player trait. Rungs are acts; reads are `trait` conditions and `[group]` bands. Not rotation. |

⚠️ **Ambient-fed does not mean thinly read.** DoL's `promiscuity` is raised in **22** places and
gates **206** — fed everywhere, read four times as often. That is the shape this tier is aimed at,
and it is the opposite of ours: five v2 games raised `arousal` **232 times against 4 reads**.

## THE LADDER

```
5  ·  10  ·  15  ·  25  ·  35  ·  45  ·  60  ·  75  ·  100
```

Nine rungs, densest at the bottom, ceiling **100** with an authored gate at 100.

## READERS — written first

| # | reader | where | what changes |
|---|---|---|---|
| 1 | which act rungs render at all | all 7 people | the ladder itself |
| 2 | which room she is allowed into | `bastien_backroom` · `mercer_room` | the back rooms open before the rooms behind those |
| 3 | how a man opens the scene | every act surface | one clause, not a branch |
| 4 | what the floor lets her do | `underworld_bar` (anchor) | counter → floor → the room upstairs |
| 5 | whether Marsh books her by name | `underworld_brothel` | the Sunday slot |
| 6 | what Mercer assumes she is for now | `penthouse` · `mercer_room` | he never learns, so it colours and never gates |
| 7 | the quest card on the `service` tier | guidance | S10 |

## WRITERS

Every finish rung: `service` · `op = "add"` · `+2` to `+5` by depth.

⚠️ **THE BRAKE IS ON THE WAY IN** (S9) — `trigger.costs` or `trigger.max_triggers_per_day` on each
surface, never a cost on an inner choice. One unbraked door makes the whole rung farmable no matter
how well priced the others are.

⚠️ Each finish also writes `clean` down 30, which is what stops this tier being farmed in an
afternoon: the cover doors shut under 40 and the bathroom costs 20 minutes.
