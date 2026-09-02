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
| ├ *Ask him about the house.* | cast — his eight exchanges, `hub_ray_kitchen.talk` |
| **Talk to your mother** | cast — `npc_dee`, 17:00–21:00 |
| ├ *Ask her about the shift.* | cast — her eight exchanges, `hub_dee_kitchen.talk` |
| **Sit up with him** | ascent — `appetite` / counterweight `home_face`. **The repeatable act surface**, opened by `ray_09` |

⚠️ **The talk pools are BRANCHES of the two hubs, not rows.** Folded 2026-09-03 — see
`wes_room.md` for why the solo lane is the wrong place for a person. **`act_kitchen_late` outranks
`hub_ray_kitchen` for the same man in the same room** (p7 over p6, and the portrait renders one
canvas per character), so his pool would have retired the moment `ray_open` set. The act surface
carries a qualified cross-canvas link, `nodeId = "hub_ray_kitchen.talk"`, which resolves globally
(`template_import.py:7414`). The same holds for Simone at the pledge house.

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
