# Card — Map and travel (infrastructure: a channel)

> **A worked card, not a template.** Take the shape, leave the furniture. Every line cites a traced game:
> round 9b, `round9b/cards/map_travel.md` and `round9b/traces/map_travel.md`. Model: **Course of Temptation
> (CoT)**, with Shady Deals (SD) and In Her Own Hands (IHOH) for the speed rungs.
>
> **Infrastructure, not a system** (`the-systems.md` SY1): declare it in `board.infrastructure[]` as
> `{ "name": "map_travel", "kind": "channel" }`, never in `board.systems[]`. It carries or shows other
> systems; it has no ladder of its own. Round 9b: "it is the carrier for encounter pools".

| field | the model (CoT) | cite |
|---|---|---|
| what it is | 26 map screens, 112 nodes; campus 17 nodes (14 clickable, 2.6 exits each), town 14; 23 location passages carry the map | round 9b `cards/map_travel.md` |
| what it carries | every move rolls the walk pool: campus walk 206 live events, town walk 109, bus 14, cum walk 6, exhibitionism sneak 12 | `cot_49_nav_override.js:313-347`; [BusInterior] |
| rules: cost | 3 min a move, 2 on campus with a bicycle; the bus to town 20 min and $0, at all hours | `cot_65_storyfunc.js:3050`; [StudentParking] |
| rules: odds | 1 in 6 per move; ×2 with a worn toy, ×1.33 / ×1.15 when horny, ×1.5 in town; 100% while sneaking naked or with visible cum | `cot_40_events.js:647-668` |
| rules: fast travel | one click to any node saves clicks, not minutes or events: time = 3 min × path length, and the event chance is multiplied by path length | `cot_65_storyfunc.js:1440`; [FastTravel] |
| rules: blocks | fast travel is off when Food, Rest or Bladder is 0, while sneaking, or with visible cum, so those states force the slow, event-rolling walk | `cot_65_storyfunc.js:3480-3493` |
| memory | barely any: the route taken (so path events know it) and whether she owns the bike | round 9b `cards/map_travel.md` |
| speed rungs | CoT 2 (walk, bike); IHOH 3 (walk 40–45 min −10 energy, scooter $5, RideMe $10); SD 4 (30 / 20 / 15 / 10 min by car tier) | [Walking]; [Scooter]; [RideMeDone]; [Suburbs Road] |
| the systems it serves | random encounters (the walk pools), needs (blocked fast travel), exposure (the sneak and cum-walk pools), people (walk events pick from those at the destination) | `cot_49_nav_override.js:27`; round 9b `cards/map_travel.md` |
| shows another system | SD's city map is also the turf board: 34 status icons for captured and blocked spots | [City Map] |
| sizes | campus 17 nodes, town 14; 5 SD districts plus home; 3 IHOH districts | round 9b `cards/map_travel.md` |

## Measured floors (directions, never gates)
- Base event chance 1 in 6 per move (CoT). Round 9b `cards/map_travel.md`.
- 2–4 speed rungs (CoT 2, IHOH 3, SD 4). Round 9b `cards/map_travel.md`.
- Fast travel keeps the minutes and the odds; it saves clicks only (`cot_65_storyfunc.js:1440`).
- 3 needs and 2 lewd states force the slow road in CoT (`cot_65_storyfunc.js:3480-3493`).

## What players say
- Too many clicks: 8 of CoT's 10 map complaints came in its launch month, e.g. *"Make a less annoying map.
  Why is this game so hard to navigate?"* (CoT, mopoga#51286). One-click travel to any node fixed it.
- Travel with no risk: *"you go to the bar, you get drunk and leave… nothing really comes of it"*
  (CoT, mopoga#135696). The road should be able to take, not only give.

## Our engine today (round 9b §6)
- Map and travel is PARTIAL: per-entry `costs` and `crossing_costs` (`template_import.py:225`), hours and
  `hidden_until`; no drawn map and no fast travel.
