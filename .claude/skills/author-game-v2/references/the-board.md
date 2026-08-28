# The Board — the world, carrying its fill debt

The world comes before the first story, and it comes **wide but paid for**.

> Measured, and it killed the obvious rule: the earliest retrievable build of the reference
> game already had **25 locations** — the same width as a game of ours that reads as empty.
> Width was never the difference. **Fill** was — and fill is a *distribution*, not a floor:
> 116,540 words over 25 locations, **mean 4,661, median 3,154**, one anchor (`school`) holding
> **30%** of all location prose, tailing down to a 302-word bus station. By 2026 the mean had
> reached 24,564 while locations only went 25 → 61.

So: declare the world broad enough to be a world, and treat every location as a debt until
it reaches the floor.

Every field below maps to a real engine key. Nothing here is aspirational — if a field has no
key, it does not belong on the board.

---

## 1. Locations — `[[locations]]`

**How many locations is not a number you pick. Derive it from what a place is FOR** — the three
things a room's list can hold (`the-surfaces.md` R2):

```
needs served here  +  work done here  +  people scheduled here
```

Write the list of places that answer at least one of those, and count it. That is the answer.

> ⚠️ **Derive it from the SHAPE first, not from the cast.** Deriving the map from the roster alone is
> circular — the premise fixes the cast, the cast fixes the map, and a household returns a house
> every time. Pick the archetype (`the-map.md` R0) before this step; the count is derived *within*
> that shape.
>
> ⚠️ **A room that answers none of the three is not a location yet.** Measured: `games/vesper` shipped
> **12 of 30 locations thin or dead**, six of them completely empty — The Vault, The Atrium, The Site,
> The Door. The incumbent skill's version of this rule (*"this place exists so the player can ___"*)
> was a question in a review document rather than a check, and it never fired.

> ⚠️ **There used to be a "6–8" here, with a note saying it was a judgement rather than evidence.
> All three v2 games shipped exactly 8 anyway.** A prose caveat does not survive next to a number.
> Derived instead, `forty_miles` comes to 8 on its own — so the count was right and only its
> provenance was wrong, which is the whole problem: nobody had to think to arrive at it. Study 6.

Budget the set as a *shape*, not a flat quota:

- **one anchor** carrying **≥25%** of all your location prose — the place the game is actually
  about, where she spends her hours. At seed the reference game's anchor was the school, at
  35,218 words against a 116,540-word total.
- satellites may be genuinely small. A 300-word bus station is not a defect; it is a corridor —
  **provided you declared it as one** (see `fill`, below).

After that, widen at the measured
early rate of roughly 6–8 per year, and **never faster than fill**.

```toml
[[locations]]
id                   = "the_laundry"
name                 = "The Laundry"
description          = "…"
image                = "locations/the_laundry.jpg"
image_search_queries = ["…", "…"]      # find-media fills the file; v2 writes the vocabulary
entry_from           = "market_row"     # the graph
navigation_order     = ["back_room"]
# entry_conditions   = { version = "1.0", items = [...] }   # locked rooms only
```

For each location, decide and record in `v2_state.json` under `board.locations[]`:

- **Its dramatic job** (`job`). Why she goes there when nothing is happening.
- **Who is there, and when.** At least one scheduled character, or it is scenery.
- **What its list holds** (`serves`) — the three kinds and nothing else (`the-surfaces.md` R2):
  which declared **needs** she can fill here, what **work** is done here, which **people** are
  scheduled here. *That is the room's menu, and its length.* A room that answers none of the three
  is not a location yet.

  ```jsonc
  { "id": "the_kitchen", "serves": { "needs": ["hunger"], "work": [], "people": ["npc_martin", "npc_denise"] } }
  ```

  ⚠️ **This replaced an `objects` list on 2026-08-18 and the reason is worth carrying.** The old
  rule declared the things in the room and derived the choice count from them. It shipped
  `the_allowance`, whose kitchen got a six-choice browse screen **on top of** four activities
  already covering the same things — nine near-verbatim duplicate pairs across five rooms — because
  gate 22 computed affordances from `exit_block.choices` and **could not see a canvas at all**. A
  body needs about five things; a room contains fifty nouns. Needs are a closed list; objects are an
  open one. `the-surfaces.md`, *"Why this sizes itself"*.

  The `objects` key is left readable in the five existing ledgers. **Nothing reads it any more.**
- **Anchor or satellite?** (`anchor`) Exactly one location is the anchor.
- **Its word budget** (`fill`) — **in round numbers, written now, before the prose.**

> ⚠️ **`fill` must be a plan, and gate 1 can tell when it is not.** Measured across all three v2
> games: every declared figure was an exact post-hoc word count — 9,607 / 4,936 / 10,295, not one
> of twenty-four round to the nearest hundred — so delivered-vs-declared matched 8/8 in all three
> and proved nothing. **A budget that cannot be wrong is not a budget.** Gate 1 now refuses to
> credit a declaration that is mostly non-round and falls back to the global backstop instead.

**A declared location with nothing placed in it is debt, not a location.** Gate 1 checks each
location against **its own declared `fill`**; the global mean/median floors are only a backstop for
a game with no ledger.

⚠️ Measured failure worth naming: one of our games *does* have an anchor at 29% — and it is a
sealed room with no exits that the player can never return to. An anchor the world cannot
reach is not a centre.

### ⚠️ Fill the anchor IN STEP with the rest

The anchor rule is a **ratio**, so it tightens every time any other room grows. An anchor left
alone while the world fills around it will fail *even though nothing about it got worse*.

Measured on a real build: the front room sat at 4,020 words while six other rooms were written,
and its share fell **53% → 46% → 40% → 39% → 35%** without a word being removed. Held there, it
would have crossed below 25% within a single further increment — the game going 9/10 → 8/10
while getting objectively better.

**Budget the anchor against the FINISHED total, not the current one** — work out its share of the
total you are planning for and put that share into every increment, rather than topping it up at
the end. A ratio gate cannot be satisfied by working elsewhere; the target moves with you.

> ⚠️ **This paragraph used to carry a worked example with a number in it, and the number has been
> removed because three games shipped to it.** back_home 36,035 · steam 36,019 · forty_miles
> 37,450 — against a figure that appeared once, as arithmetic, and was a spec nowhere. Illustrative
> numbers in a file that also contains thresholds get read as thresholds. Study 6.

**Cold rooms are allowed.** Not every place is erotic — the reference game had no sexual
content in 8 of its 25 locations (a police station, a museum). The floor is **60% of
locations carrying heat**, not 100%.

---

## 2. Characters — `[[npcs]]` and `[[npcs.schedules]]`

```toml
[[npcs]]
id          = "npc_wren"
name        = "Wren"
description = "…"
portrait    = "wren.jpg"
core_traits = { relation = 0 }
flag_keys   = []
arc_stages  = ["Stranger", "Familiar", "…"]

[[npcs.schedules]]
location   = "the_laundry"
weekdays   = [0, 1, 2, 3, 4, 5, 6]
start_time = "09:00"
end_time   = "18:00"
activity   = "working the presses"
```

**Every character needs at least one standing surface and at least one schedule row.** Gate 6
fails otherwise.

> Measured anti-pattern: a character referenced 88 times in a game's source — more than any
> other except the lead — carrying zero bound canvases and zero schedule rows. Heavily
> written, reachable nowhere.

**Overnight windows are supported — but ONLY on a row that covers every weekday.** The wrap and
the weekday are two separate checks, and the weekday one runs first against **today**:

```
v2.py:3596   if (!setup._weekdayMatches(ds.weekdays, todayIndex)) continue;
v2.py:3597   if (!setup.isCurrentTimeSlot(ds.start_time, ds.end_time)) continue;
```

`isCurrentTimeSlot` does handle the wrap (`if (endTotal < startTotal) return currentTotal >=
startTotal || currentTotal < endTotal;`, the `isCurrentTimeSlot` definition at `v2.py:3784`). So
`weekdays = [0,1,2,3,4,5,6]`, `22:00`–`04:00` is correctly **one** row.

⚠️ **But `weekdays = [1]`, `23:00`–`06:00` puts the character on site on Tuesday night and DELETES
them at midnight**, because `todayIndex` is now Wednesday and Wednesday is not in the list. A
day-specific overnight window needs **two rows** — `[1] 23:00–23:59` and `[2] 00:00–06:00`.

This section previously said "`22:00`–`04:00` is one row, not two" with no weekday qualifier, and
its own example happens to use all seven days — which is exactly why the caveat stayed invisible.
An older note in project memory claimed overnight windows always need two rows. **Both were half
right**, and a game following either one blindly loses half its night cast or doubles rows it did
not need to. Verified live in a built game: nine presence probes across the midnight and week
boundaries, all correct only once the day-specific rows were split.

**Ordering trap:** `[[npcs.schedules]]` binds to the `[[npcs]]` block above it. Inserting a
new character between an existing one and its schedules silently re-parents them.

### The rotating slot, and the split that makes it actually cheap

A **rotating slot** — one location whose occupant is replaced every few releases — is the
cleanest way to build the measured release shape (*a new character at an existing place*) into
the fiction rather than bolting it on. A tenant's room, a locker at a gym, a chair in a bar.

It only pays off if content is filed by **how long it lives**, and this is the part that gets
missed:

| scope | what it covers | file | survives a rotation? |
|---|---|---|---|
| **TENANT** | his ladder, his register, his props, his one paid-off secret | `5_scenes.toml` | no — dies with him, deliberately |
| **ROOM** | the slot itself, the furniture, the wall, what the arrangement IS | `3_activities.toml` | **yes** |

**Room-scoped content names the occupant by ROLE, never by name.** *The tenant*, not *Marek*.
That one rule is the difference between a rotation that costs one `[[npcs]]` block plus one
scene file, and a rotation that quietly costs a rewrite of every solo surface in the room.

⚠️ Caught in a real build: a game's box-room solo surface was room-scoped *by file* and
tenant-scoped *by content* — a specific paperback, a specific bus ticket, a specific tin with a
specific amount in it. Every one of those was the current tenant. The ledger's plan said a
replacement would touch only his `[[npcs]]` entry and his scene block; in fact the first
rotation would have cost a rewrite in a file the plan claimed it would not open. The fix is
free if you do it while writing and annoying afterwards, so decide the scope of each surface
*before* you write it.

The room-scoped layer is also the more interesting half to write, because it is the only place
the slot is legible **as a slot** — the same mattress, four tenants, marks on the wall at three
different headboard heights, and the fact that the terms get set in the first two weeks by
whoever is standing there when the new one arrives.

---

## 3. The meters — declared here, designed in `the-meters.md`

**The design decision is not on this page.** Which meters exist, who owns them, how deep the ladder
goes and what a throttle is for all live in `references/the-meters.md` W1–W6. This section is the
declaration and the two rules the gates read off it.

### 3a. Declare who climbs — FIRST

```jsonc
"who_climbs": "player" | "cast" | "both"
```

The field splits, cleanly, into two schools with nothing between them: **8 roster games** put 65%+
of their character-gating on per-character meters, **9 ladder games** put 13% or less. All five v2
games sit at 19–29% — inside a band no shipped game occupies, because the question was never asked.
`the-meters.md` W1 carries the measurement and the table of what each answer looks like on a board.
**Gate 34** checks the game against this declaration.

### 3b. Three layers

Measured directly from the reference game's seed source, because our first draft said "exactly one
global axis" and the source refuted it.

⚠️ **The layer-1 shape below is ONE game's, and the corpus does not repeat it.** Of 27 parseable
sandboxes, **15 have no player ascent tier at all** and only two carry three or more — one of which
is this same reference game. Three-or-four-tiers is a legitimate answer for a `who_climbs = "player"`
game. It is not the default, and treating it as one is how five games got the same board
(`the-meters.md` W1).

**Layer 1 — ratcheting ascent tiers**, if the game has any. Each names a DIFFERENT kind of going
further — sleeping around, being seen, doing the strange thing — so a player who does not want one
can still climb another. A single undifferentiated "corruption" collapses parallel ascents into one
and gives every player the same ladder.

| tier | raises | lowers | gate sites |
|---|---|---|---|
| promiscuity | 22 | 1 | 206 |
| deviancy | 20 | 0 | 129 |
| exhibitionism | 12 | 1 | 167 |
| *purity* (counterweight) | | | 58 |

*(Provenance: the reference game's 2018 **seed**, read from its twee source. A passage-level read of
its 2026 build returns different figures because most of that game's logic now lives in JavaScript —
the two are not comparable and neither supersedes the other.)*

⚠️ **Rung spacing is NOT declared here and there is no shape to copy.** This section used to end
*"their rungs sit at 15/35/55/75 — copy that shape"*, and every tier of every game built afterwards
did exactly that: **all 16 declared tiers across five games put their lowest rung at 15.** The
field's live meters run **8–17 rungs with the lowest at ~5** (`the-meters.md` W4).

**Layer 2 — volatile state.** Arousal, stress, energy. These move both ways and are managed minute
to minute; they are *not* ascent. **But volatile is not the same as unread** — a throttle gates the
repeatable act surface, and a game that raises arousal 50 times and reads it never has a decoration,
not a meter (`the-meters.md` W2, gate 33).

**Layer 3 — per-character tracks.** Light in a ladder game, load-bearing in a roster one — W1
decides which, and `the-meters.md` W6 says how to pick each character's.

```toml
[player]
core_traits = { promiscuity = 0, exhibitionism = 0, deviancy = 0,   # layer 1: ratchets
                arousal = 0, stress = 0, energy = 100, money = 20 } # layer 2: volatile

[[sidebar_items]]
type  = "trait_status_text"
trait = "promiscuity"
bands = [ { min = 0, max = 14, text = "…" }, { min = 15, max = 34, text = "…" },
          { min = 35, max = 54, text = "…" }, { min = 55, max = 74, text = "…" },
          { min = 75, max = 100, text = "…" } ]
```

*(Band boundaries are the sidebar's business — how the player READS the meter — and are independent
of where the gates sit. Do not derive one from the other.)*

Three hard rules, all gated:

- **Rising must expand.** For each ascent tier, `gte`/`gt` gates must outnumber `lt`/`lte`.
  Gate 10 checks the three most-gated meters. A meter whose rise mostly *closes* content is a
  descent wearing an ascent's clothes — the measured failure case had exactly that as its
  dominant meter, with the world contracting to a sealed room as it rose.
- **The ceiling must be bought.** The top band's `max` is a promise to the player. If the
  highest authored gate on that trait is below it, the remaining points buy nothing. Gate 8.
  *(A top band with no `max` is unbounded on purpose and promises nothing.)*
- **Every meter you raise is read by something.** Gate 33, `the-meters.md` W3.

**Where ceilings live:** `sidebar_items[].bands[]`. **Not** in `player.core_traits`, which is
a flat map of starting values only.

---

## 4. The daily loop — `board.needs[]`

An ordinary day when no story is happening: sleep, eat, wash, earn, spend. This exists in every game
of this shape regardless of who is in the cast, and it is what the TRIGGERED layer hangs off —
*"during the weekends"*, *"when exposed"*, *"at high stress"* are all readings of an ordinary day.

**It is a declaration, not a note to self.** Until 2026-08-18 this section was the four lines above
and nothing else: no field, no gate, no checklist — against `objects`, which had a field, a hard gate
and a lint. Authors build toward what is measured, and the result was a game whose anchor room is a
kitchen and which contains no food and no bed.

Declare each need with the four fields from `the-meters.md` M8:

```jsonc
"needs": [
  { "key":   "hygiene",
    "falls": "10 a day",                                  // [player.trait_decay]
    "fills": "the_bathroom · Wash · 30 min",
    "costs": "$5 for the water heater",
    "shuts": "under 40 she will not go out in public" }   // ← gate 29 checks THIS
]
```

- **Needs are per game, not a fixed list.** A truck stop's body is not a household's; `vesper`'s is
  `Power down` / `Charge up`.
- **`shuts` is the load-bearing field.** A need that shuts nothing is a chore (M9, gate 29).
- Each need must appear on some room's list (`the-surfaces.md` R2) — a need with nowhere to fill it
  is a countdown to a wall.

`[time]` sets `starting_hour`, `starting_day`, `starting_week`.

---

## 5. Media declaration — v2 writes the slot, `find-media` fills it

This skill never searches for media. It **declares** it, and the declaration is load-bearing.

```toml
# repeatable explicit content — ALWAYS a cycling pool
{ type = "video", props = { pool_dir = "sex/laundry_backroom_t5", pool = 4,
                            description = "…",
                            search_queries = ["…", "…"] } }

# a single fixed file is only for one-time or non-explicit beats
{ type = "image", props = { file = "scenes/first_shift.jpg", … } }
```

Three rules, all gated:

- **Repeatable explicit content declares `pool_dir` + `pool`, never a single `file`.** A beat
  replayed fifty times with one clip is dead on arrival; the reference game re-rolls pools of
  26 and 56 items on every room render. Gate 4.
- **High-traffic locations carry a cycling pool.** This is the traversal layer, and its
  absence is the clearest single cause of a game reading cold: movement between scenes is most
  of the play minutes, and a non-erotic traversal layer wins by sheer occupancy. Gate 5.
- **Tier the filename.** The `_t4` / `_t5` suffix is how downstream tooling knows the slot is
  explicit. An untagged explicit slot is read as safe and mis-sourced.

---

## 6. Settings

```toml
[settings]
narration_person  = "second"     # per-game, IMMUTABLE after the first release ships
clothing_enabled  = true
wardrobe_location = "her_room"
```

---

## Before leaving this phase

Record in `v2_state.json`: every location with its budget and current fill, every character
with its surface count and schedule rows, the ascent meter and its ceiling.

Then run the scoreboard — it works on an empty world and will simply report the debt:

```
python3 .claude/skills/author-game-v2/scripts/gates.py <slug>
```

Gates 1, 5, 6, 8 and 10 are all decidable from the Board alone. Fix them here, where it is
cheap, rather than after content is hung on a broken frame.

Then move to `references/the-release.md` and build v0.1.
