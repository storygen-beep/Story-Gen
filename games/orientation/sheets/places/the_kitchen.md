# PLACE · The Kitchen  `[READY]`

| | |
|---|---|
| **id** | `the_kitchen` · button `Kitchen` |
| **ENTERED FROM** | `the_hall` |
| **FILL** | 4,500 words |
| **cycling pool** | yes — `sex/kitchen_late_t5`, pool 5 |

## What kind of place this is
The one room in the house where two people are alone **by the clock rather than by accident.** Dee
works 22:00–06:00. From 22:00 the kitchen is Ray's, and everyone in the house knows it.

## The list
| row | system |
|---|---|
| **Eat** | needs — `fed`, 20 min, free |
| **Talk to @ray** | cast — `npc_ray` hub, 22:00–01:00 |
| **Talk to your mother** | cast — `npc_dee`, 17:00–21:00 |
| **Sit up with him** | ascent — `appetite` / counterweight `home_face`. **The repeatable act surface**, opened by `ray_09` |

## Sit up with him — the act surface
Opened by **`ray_09`**, the last step of his nine-step arc. Before that flag the row does not exist —
the surface is what finishing the arc **buys**.

**BRAKE:** `trigger.costs rest 12` · day-cap flag `kitchen_late_today` **set on the choice** ·
window Sun–Thu 22:00–01:00 only.

⚠️ **The window is the real throttle.** A 10-minute rung against an all-day hub is farmable ~144×
a day; a rung sized against a three-hour window that ends when he goes up is ~2. Advancing past his
window makes him absent, and that is what actually stops the rung.

**Gated on `home_face lt 60`** — the counterweight is the wire. He will not move while the household
still believes her.

**A10 aftermath** — ~32 words, written for *him*: how he leaves, what she is left holding, the offer
to stay or go. **A11 stop beat** — about how he takes being stopped.

## Walk-in
**Required.** `walkin_kitchen_dee` — Dee comes back for something she forgot. Fires on the act
surface at low probability, and it is the only thing in the game that can cost `home_face` in one
move.

## Ways out
`the_hall`
