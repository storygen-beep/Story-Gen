# PLACE · Wren's Room  `[READY]`  ★ HOME BASE (until it is not)

| | |
|---|---|
| **id** | `wren_room` |
| **ENTERED FROM** | `spire_plaza` — the lift, to a floor the directory does not list |
| **WAYS OUT** | back to `spire_plaza` |
| **DOOR** | **YES**, and it is the only door in the game that CLOSES rather than opens |
| **LABELS** | `private` · `zone:spire` · `home_base` · `she_can_undress` |
| **fill** | 1,500 `[INTENT]` |
| **heat** | none — nothing happens to her in here, which is the point |

## What this place is FOR

**It is the free thing, so that losing it is the ignition.**

The original `vesper` put her home three rooms deep in the tower — `wren_floor` (*"the asset level:
narrow corridors, numbered doors, no windows"*), `wren_room` (*"hers in the way a tool's drawer is
the tool's"*), and `cradle` as a fourth location. This build had none of them and started her at
`kess_berth` paying ten a night on frame one.

⚠️ **That made her housing an arc shipped in its converted state** — the exact failure
`the-arc.md` exists to stop, committed on the player's own bed. And it meant the obligation never
ignited: ten coin a night was a fact she woke up to rather than the price of not going back.

**One room and one row carry what four locations carried.** The cradle is a row inside this room,
not a location of its own.

## The list — needs only

| # | row | canvas | kind | system | gate | effect | screen |
|---|---|---|---|---|---|---|---|
| 1 | "Power down. (9h.)" | `act_the_cradle` | need | `charge` · `clean` | `max_triggers_per_day = 1` | `charge` `set` `100` · `clean` `set` `100` · **no cost** | yes |
| 2 | "Open the drawer." | `amb_wren_room` | — | — | — | 10 min | yes |
| 3 | "Sit on the bed for a while." | `amb_wren_room` | — | — | — | 20 min | yes |

No work and no people. **Nobody comes to this corridor** — the only voice in the room is the
building's, on a tannoy, talking *at* her about linen and personal effects.

## ⚠️ THE CRADLE'S BRAKE IS LOAD-BEARING, and it was measured, not assumed

`charge` **is** gated at 30 with `gte`, which makes it one of the eight meters
`the climb is paid for` prices. A free, uncapped cradle makes it freely farmable and turns that
gate red — the gate three passes were spent earning.

`trigger.max_triggers_per_day = 1` is the brake, and a sleep once a night is what this is anyway.
The feed line at the berth stays day-capped **and** priced, so the contrast is the whole design:
**free-but-once here, paid-and-once there**, and the difference between them is the ignition.

## The door that closes

`arc_badge_pulled` — a milestone in this room, fires on `service gte 10` **and** `kess_tenant`.
The company notices what she is doing down the hill and consolidates asset housing; there is a
crate outside the door with her name on a label.

⚠️ **`kess_tenant` is in that gate deliberately.** The feed line has to be ARMED before the cradle
is taken away, or a player who reaches `service 10` without having rented from Kess loses every
charge source in the game at once.

After it fires, `entry_conditions` on this location refuse her — *"The lift does not take her palm
for that floor any more. Somebody in an office decided it and nobody came down to say so."*

## What it converts into

The berth. And past the berth, `the_cot` — authored **locked** at `kess_berth`, keyed on
`npc_kess relation gte 60`, the way Cain's shutter is keyed on `drain gte 100`. *"It is not the
cradle and it is not a room, and it would be the first place in her life nobody signed for."*

⚠️ Keyed on a trait, NOT on the original's `berth_home` flag: the flag-chain validator hard-fails a
flag that is read and never set, and nothing sets it on purpose — it is next release's door.
