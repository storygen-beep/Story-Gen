# Probation — DECISIONS  `[REVIEW]` · PROPOSAL, for LO to place

> Proposed 2026-09-29 to replace `DECISIONS.md` (2026-09-04, older skill). LO places it or edits it.
> Verdict has four parts: **Character · Coherence · Correctness · Convenience.**
> Every count on this page is a **promise**, not a measurement. Nothing is built yet.

---

## Needs you first

| # | question | my recommendation | why it matters |
|---|---|---|---|
| 1 | ~~Old sheets or the new spine?~~ | **Ruled: the new design** | — |
| 2 | ~~Ages~~ | **Ruled: Rae 58, Delgado 44** | — |
| 3 | Re-sign SP7: the bridge in, the bus stop out | Sign | Review 1 opens the bridge, so it must exist |
| 4 | Where is 0.1 published, and is it phone-first? | The game portal; phone-first | Sets screen length and clip size |
| 5 | Marty's shop is the main place and has almost no heat in 0.1. OK? | Yes, for one release | Marty's first sex scene arrives in 0.2 |
| 6 | Title: `Probation` or `The Box`? | `Probation` | Every saved game breaks if it changes later |
| 7 | Can scenes be replayed from a gallery later? | Yes | Cheap to decide now, costly to add later |
| 8 | Walk the 7-place map below and sign it | — | Your last walk was the 11-place map |

---

## A · Locked forever

| | decision |
|---|---|
| A1 | Second person ("you") |
| A2 | Title (question 6) |
| A3 | What holds her: a court order. Delgado, and the box on her ankle |
| A4 | She climbs. The cast runs on step counters, not meters |
| A5 | Meter names: `radius` · `hours` · `vouch` · `clean` · `battery` · `review_days` |
| A6 | Step names: `tobin_01_fault` … `rae_02_folding`, as on the person sheets |

Renaming any of these after 0.1 ships breaks every saved game.

## B · Expensive, but a release can change it

| | decision |
|---|---|
| B1 | 7 places, 30,000 words; Marty's shop is the main place (8,000) |
| B2 | 4 people: Tobin 4 steps, Delgado 3, Marty 3, Rae 2 |
| B3 | A review every 30 days; each pass removes one rule |
| B4 | 0.1 ends on Tobin's locked offer: *"Make it say I'm home"* |
| B5 | Creation screen: her name (her look added once the select field is verified) |
| B6 | The first thing money buys: a dock behind Marty's counter, $120 |

## C · Cheap, change freely

Room descriptions · card wording · clip searches · random events · who walks in.

---

## The map

```
   bowen_street  (the street, the ground)
        ├── the_stairwell ─┬── her_room
        │                  └── the_laundry
        ├── martys
        ├── the_county_office
        └── the_bridge   (locked until review 1)
```

Left for later releases: Marty's back room, the diner, the bus stop, the far side.

## The three meters she climbs, and what each opens in 0.1

| meter | what it means | opens in 0.1 |
|---|---|---|
| `radius` | how far from home | the bridge, after review 1 |
| `hours` | how late she stays out | the paid night sit at the laundry |
| `vouch` | how many people lie for her | Tobin's bench, then his locked offer |

**Her record (`clean`)** starts at 100. Each dot left on file costs 20. Review 1 needs 60.
Under 40, a Thursday check-in is added. At 0, the hearing.

## Guidance cards

| card | shows | goal line |
|---|---|---|
| The box | from the start | *Dock the box before it runs low.* |
| The review | from the start | *First review: the first Tuesday after day 30.* |
| The dot | after Delgado reads it | *Find out who put you at the yards.* |
| Tobin · Delgado · Marty · Rae | after each meeting | that person's next step, place and time |
| Further · Later · Covered | one per meter | the next thing that meter opens |

## Deferred, and why that is safe

The far side, Marty's back room, the diner, the bus stop, a fifth person, a phone. **None is
needed by a check.** The phone is a no.

---

## Sign-off

| part | verdict | note |
|---|---|---|
| Character | | |
| Coherence | | |
| Correctness | | |
| Convenience | | |

**Signed:** _________  **Date:** _________

*Evidence and reasons: `v2_state.json` → `decisions`, and `spine/`.*
