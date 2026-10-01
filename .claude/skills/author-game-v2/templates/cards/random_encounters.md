# Card — Random encounters (infrastructure: a channel)

> **A worked card, not a template.** Take the shape, leave the furniture. Every line cites a traced game:
> round 9b, `round9b/cards/random_encounters.md` and `round9b/traces/random_encounters.md`. Model:
> **Course of Temptation (CoT)**, its walk pools.
>
> **Infrastructure, not a system** (`the-systems.md` SY1): declare it in `board.infrastructure[]` as
> `{ "name": "random_encounters", "kind": "channel" }`, never in `board.systems[]`. It carries or shows
> other systems; it has no ladder of its own. CoT's campus walk pool passes questions 1–5, but 40% of its
> ordinary events belong to other systems: count the pool once, and credit each event to its owner.

| field | the model (CoT) | cite |
|---|---|---|
| what it is | a roll on every move into a walk-tagged place: campus paths, town sidewalks, residence hall, her Greek house, the bus | `cot_49_nav_override.js:4`; round 9b `traces/random_encounters.md` |
| what it carries | of 172 ordinary campus events, 69 (40%) come from other systems: Greek house 18, campus sneaking 11, NNN 10, texts 8, birthdays 7, the classroom harasser 4, clothing 3 | round 9b `traces/random_encounters.md` |
| rules: odds | 1/6 per move (town ×1.5); ×2 with a worn toy, else ×1.33 / ×1.15 by horniness; 1.0 while sneaking or with visible cum | `cot_40_events.js:647-672` |
| rules: no skipping | fast travel multiplies the chance by path length; a 3-step trip is about 50% | [FastTravel]; `cot_65_storyfunc.js:1440` |
| rules: the pick | keep events whose tags match, then about 70 filters (hours, weather, clothes, kinks, skills, reputation, who is here, days since); weighted draw by frequency, ordinary weights 10–60 | round 9b `traces/random_encounters.md` |
| rules: hours | 94 of 186 campus events have a time window | round 9b `cards/random_encounters.md` |
| priority beats | 14 campus story beats ride the pool at weight 500 or more, so they fire on the first eligible walk, not by luck | round 9b `traces/random_encounters.md` |
| memory | per event only: the last day it fired, `unique`, prereq chains; no global "seen recently" rule for walks | round 9b `traces/random_encounters.md` |
| how it climbs | the pool opens as she changes: clothing state, reputation 175/250, horny, 11 kink opt-ins, a worn toy, the sneak pool (12), the cum-walk pool (6) | round 9b `cards/random_encounters.md` |
| the systems it serves | Greek life, sneaking, the phone, the harasser arc, clothing, reputation (being seen), relationships | round 9b `traces/random_encounters.md` |
| people | 122 of 172 ordinary campus events name a real NPC at the scene (71%); town 51 of 90 (57%) | round 9b `cards/random_encounters.md` |
| sizes | campus 210 (186 ordinary), town 111 (97), residence hall 70, Greek house 29, bus 14 | round 9b `traces/random_encounters.md` |

## Measured floors (directions, never gates)
- 1/6 per move, about 6 moves per encounter (`cot_40_events.js:647-672`).
- 60 or more ordinary events for a pool hit several times a day; CoT has campus 172, town 90, residence 62
  (round 9b `cards/random_encounters.md`).
- At least half name a recurring NPC (CoT 71% campus, 57% town).
- Every event 1 day or more apart: 85 of 186 carry `days since`, median 2 days; story beats `unique`.
- At least 3 of her states open new events (round 9b `cards/random_encounters.md`).

## What players say
- Random means waiting: *"A lot of the events in this game are purely random and require waiting an unspecified
  amount of time to trigger"* (CoT, mopoga#135155). CoT fixes it for story beats (high weight, `unique`), not
  for repeatable sex.
- Nothing happens to me: the loudest walk-related ask is for danger, e.g. mopoga#135696 (CoT). Encounters
  add; they rarely take.

## Our engine today (round 9b §6)
- SUPPORTED: `setup.checkRandomEncounters` (`v2.py:6331`) rolls per location canvas, with a cooldown of 3
  after a hit (`v2.py:6444`).
