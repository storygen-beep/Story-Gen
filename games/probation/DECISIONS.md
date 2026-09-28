# Probation — DECISIONS  `[REVIEW]`

> **Status lives in this title.** `[REVIEW]` → LO reads and edits → `[READY]` → built → `[GAME-READY]`.
> Verdict has four parts: **Character · Coherence · Correctness · Convenience.**
>
> ⚠️ **Every count on this page is a PROMISE, not a measurement.** There is no `--sheets` mode;
> nothing here was produced by an instrument. The measured column stays empty until v0.1 builds.

---

## A · Locked forever — expensive to reverse, decide now

| | decision | why it cannot move later |
|---|---|---|
| A1 | **`narration_person = "second"`** | rewrites every line in the game |
| A2 | **Title: `Probation`** | `the-returning-player.md` — immutable once saves exist. Alternative on the table was `The Box`. Working answer: keep `Probation`; it is the one word that says what the game is. **LO's call, and this is the last cheap moment.** |
| A3 | **`hold_kind = order`** — the box and the signature, not a bill | the whole economy, the map gate and three tiers derive from it |
| A4 | **`who_climbs = "player"`** (ladder) | gate 34 checks the build against this. Moving it re-homes every gate in the game |
| A5 | **Tier keys `radius` · `hours` · `vouch`; counterweight `clean`; throttle `arousal`** | trait keys are save join-keys. A rename strands every save and no gate can see it |
| A6 | **Canvas + location ids as declared in `sheets/places/`** | same reason. `gates.py --saves` only works from v0.2, so 0.1's ids are the baseline |
| A7 | **`battery` is a trait, spent via `costs`, not decayed** — and it is the BOX's battery, not hers | verified: `player_trait_decay` fires only inside `advanceDay()` (`v2.py:5733`, applied `:5826`). An 18-hour battery cannot be a daily decay |

⚠️ **A7's meter is called `battery` and the sidebar row is labelled `The box`.** It was `charge`
until 2026-09-05, when LO read the sidebar as a player and asked whether the lead was a humanoid —
a fair reading, because a fourth bar sitting beside `food` · `rest` · `wash` is read as her body.
The word came from `vesper`, whose lead genuinely *is* company property. She is a human woman with a
court order. The row renders **word bands** — *full · fine · getting low · it will start beeping
tonight · it is beeping* — not a percentage, so what the player meets is the object's state and
never a figure. (`hidden = true` in `[[traits.labels]]` or the number prints twice — gate 27.)

## B · Expensive but reversible — a release could change these

| | decision | cost of changing |
|---|---|---|
| B1 | 11 locations, 51,500-word v0.1 budget, anchor `martys` at 27.2% | re-budgeting is arithmetic; re-writing is not |
| B2 | Cast of four. Marty rich (6 rungs), the other three at 3 | adding a fifth is a release, not a rewrite — that is the point of the format |
| B3 | Rung spacing `5/12/20/30/45/60/80` etc. | every gate in the game reads these numbers |
| B4 | `the_far_side` is the door 0.1 ends on | it can be a different door; it cannot be no door |
| B5 | Creation screen: **2 fields**, `name` + `look` | 7 of 15 built games ship this screen; the engine writes its headings and we only own `player_description` (`v2.py:9509`) |

## C · Cheap — change freely

Room descriptions · quest-card wording · media queries · which ambient fires where · the diner's
counter-seat occupant (it is a **rotating slot**: room-scoped content names the occupant by role,
never by name, so a rotation costs one `[[npcs]]` block).

---

## The map

**Archetype `nested_zones`.** Chosen over `map_hotspots`, which the radius argues for — hotspots
wants 10+ drawn districts and this opens with six streets, so it would ship a map that is mostly
locked pictures. **The radius is the gate on the zone, not a drawing.**

**Exterior: `bowen_street` — a ROOT, no `entry_from`.** Everything hangs off it. `the_far_side` is a
**second root**, reached only across the bridge.

```
   bowen_street  (ROOT · the ground)
        ├── the_stairwell ─┬── her_room        (up the stairs)
        │                  └── the_laundry     (through the other door)
        ├── martys ─── martys_back
        ├── the_county_office
        ├── the_stop ─── the_bridge ─ ─ ─ ▶  the_far_side  (ROOT · locked, radius ≥ 45)
        └── the_diner
```

**`r1_signoff`: PARTIAL — walked by LO 2026-09-04, one defect found and fixed.** He rejected the
topology: `her_room` and `the_laundry` were two leaves off the street and are physically one
building. `the_stairwell` is the fix. **Not yet signed as a whole.**

⚠️ **It is a real location, not `is_container`.** A container *swallows any canvas attached to it*
(`template_import.py:153`) and auto-enters its `default_entry` — it would have given the grouping
and removed the choice the room exists to provide. Being a real room also means it answers R2
(`needs + work + people`) with a **Rae** row at 04:00–05:00, in the gap between her laundry night
and her diner hour — and it puts everyone who uses the machines at three in the morning on her
stairs.

> A street on the east side of a river. One door on it opens on a stairwell with the laundry
> through it and her room at the top of the stairs; the shop and the county office are further
> along; the street runs down to the bus stop and then to the bridge, and the far side of the
> bridge is a second ground she cannot reach yet.

---

## The three tiers, and what each one's rungs OPEN

| tier | rungs | what going further means | what release 41 hangs on |
|---|---|---|---|
| `radius` | 5·12·20·30·45·60·80 | how far from the home point she is when it happens | opens **map** |
| `hours` | 5·15·25·40·55·70·85 | how late, and how long she will stay | opens **the clock on rooms that already exist** ← this is the schedule |
| `vouch` | 5·15·30·45·60·80 | how many people are lying for her, and what they take | opens **the cast** |

**Counterweight `clean`** starts 100 and shuts three doors, written before the prose because four of
our five games shipped a counterweight that gates nothing:

- **< 40** — Delgado's Thursday row becomes a summons. Costs a whole evening slot.
- **< 20** — the county office is daily; every `hours` surface above 40 is unavailable those nights.
- **0** — the hearing. A terminal state, shipped on purpose, and not an ending for the product.

⚠️ **The Thursday summons is a CANVAS gated on `clean`, not a conditional schedule row.** Delgado is
declared at the office Tue **and** Thu regardless; what `clean` changes is whether one of those
hours is hers. Nothing in this design assumes the engine can gate a schedule.

---

## Guidance — S10

One quest card per tier, one per character. `quests_engine = "v2"`; with no cards the page renders a
heading and nothing.

| card | when it appears | goal bullet |
|---|---|---|
| `card_the_box` | from screen 1 | *Dock the box before it drops under 20.* `battery` — `label` written |
| `card_the_sheet` | after `met_marty` | *Get a week of hours signed.* `sheet` — `label` written |
| `card_tuesday` | from screen 1 | *Be at the county office, Tuesday, two o'clock.* flag goal → **`label` REQUIRED** |
| `card_marty` · `card_rae` · `card_tobin` · `card_delgado` | each behind that person's meeting flag | one per person |

⚠️ **Every flag goal carries a `label`.** The importer requires `label` on trait and counter goals
**only**, so a flag goal falls straight through and the renderer prints the raw key —
`met_marty` — to the player under 🎯 To advance.

---

## What is DEFERRED, named out loud — S6

Nothing a gate requires. **A deferral is not a pass**, and the incident behind that rule was a
walk-in honestly deferred against a gate that then failed 0/5.

Deferred and **not** gate-bearing: `the_far_side`'s interior · Rae's back flat as an enterable room ·
a fifth character · the phone (`the-phone.md` P1 is a refusal question and the answer here is **no**).

---

## Sign-off

| part | verdict | note |
|---|---|---|
| Character | | |
| Coherence | | |
| Correctness | | |
| Convenience | | |

**Signed:** _________________  **Date:** _________
