# The Board — the world, carrying its fill debt

The world comes before the first story, and it comes **wide but paid for**.

> Measured, and it killed the obvious rule: the earliest retrievable build of the reference
> game already had **25 locations**. Width was never the difference. **Fill** was — and fill is a *distribution*, not a floor:
> 116,540 words over 25 locations, **mean 4,661, median 3,154**, one anchor location holding
> **30%** of all location prose, tailing down to a 302-word bus station. By 2026 the mean had
> reached 24,564 while locations only went 25 → 61.

So: declare the world broad enough to be a world, and treat every location as a debt until
it reaches the floor.

Every field below maps to a real engine key. Nothing here is aspirational — if a field has no
key, it does not belong on the board.

---

## 1. Locations — `[[locations]]`

⚠️ **Read `references/the-systems.md` before this section, and fill a card per system before the
rooms** (`board.systems[]`, `templates/sheets/system.md`; its meters go in `board.meters[]`). The
derivation below needs them: a room's rows come from the systems that live there, not from the
room. Course of Temptation reads `has_inclination` in 218 of its 5,294 passages, so what
she has become changes what a room offers (`the-systems.md` SY1).

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
> ⚠️ **Two kinds of place** *(LO decided, D9 · D10)*. A **thoroughfare** (`kind = "thoroughfare"`,
> `engine.md` §22) only routes: a corridor, a lobby, a street. A **destination** — the default —
> always offers one thing she can do alone, or it is closed then (`hours` + `closed_text`,
> `engine.md` §22). A room that is neither is not a location yet. One passing
> game keeps an open, empty shop — In Her Own Hands' formal-wear shop, empty 76 of its 77 open hours —
> and it says so: *"There's nothing to do here right now."* [WindsorBase]. That is the exception, named.

Budget the set as a *shape*, not a flat quota:

- **one anchor** carrying **≥25%** of all your location prose — the place the game is actually
  about, where she spends her hours. *The 25% is the reference game's seed figure, labelled;* the
  field reaches it at district scale (top district median 49.4%, 22 of 26 games) and rarely in a single
  room (top room median 13.1%, 6 of 26), so an anchor may be a set of rooms. At seed the reference game's anchor held 35,218 words
  against a 116,540-word total.
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
- **Who is there and when — and on a destination, one thing she does alone.** A thoroughfare needs
  neither.
- **What its list holds** (`serves`) — the three kinds and nothing else (`the-surfaces.md` R2):
  which declared **needs** she can fill here, what **work** is done here, which **people** are
  scheduled here. *That is the room's menu, and its length.*

  ```jsonc
  { "id": "the_kitchen", "serves": { "needs": ["hunger"], "work": [], "people": ["npc_martin", "npc_denise"] } }
  ```

  ⚠️ **This replaced an `objects` list on 2026-08-18 and the reason is worth carrying.** The old
  rule declared the things in the room and derived the choice count from them, and gate 22 computed
  affordances from `exit_block.choices` and **could not see a canvas at all**; the gate is deleted
  (`gates.py:2248`). A body needs about five things; a room contains fifty nouns. Needs are a closed
  list; objects are an open one. `the-surfaces.md`, *"Why this sizes itself"*.

  The `objects` key is left readable in old ledgers. **Nothing reads it any more.**
- **What KIND of place it is** (`labels`) — `the-systems.md` SY3. Not the same question as `serves`:
  `serves` is what happens here, `labels` is what would let anything happen here. *Private · has a
  mirror · open all night · she cannot undress here.* Cut the menu in SY3 down to the labels this
  game's systems actually read; a label nothing reads is dead weight.

  ```jsonc
  { "id": "the_kitchen", "labels": ["private", "sells_food", "has_washer"] }
  ```

  ⚠️ **Does a system here write a `sourced` meter?** (`the-systems.md` SY2) It is not gated — there is no measured answer to *how many is enough* — but it is the question to ask
  of every room on this list before the prose exists.
- **Anchor or satellite?** (`anchor`) Exactly one location is the anchor.
- **Its word budget** (`fill`) — **in round numbers, written now, before the prose.**

> ⚠️ **`fill` must be a plan, and gate 1 can tell when it is not.** A figure copied from the
> delivered word count matches delivered-vs-declared by construction and proves nothing. **A budget
> that cannot be wrong is not a budget.** Gate 1 refuses to credit a declaration that is mostly
> non-round and falls back to the global backstop instead.

**A declared location with nothing placed in it is debt, not a location.** Gate 1 checks each
location against **its own declared `fill`**; the global mean/median floors are only a backstop for
a game with no ledger.

### ⚠️ Fill the anchor IN STEP with the rest

The anchor rule is a **ratio**, so it tightens every time any other room grows. An anchor left
alone while the world fills around it will fail *even though nothing about it got worse*.

**Budget the anchor against the FINISHED total, not the current one** — work out its share of the
total you are planning for and put that share into every increment, rather than topping it up at
the end. A ratio gate cannot be satisfied by working elsewhere; the target moves with you.

**Cold rooms are allowed.** Not every place is erotic — the reference game had no sexual
content in 8 of its 25 locations (a police station, a museum). **A place is hot when it holds at least
one sex scene** *(LO decided, D9c)*, counting the men's own rooms and a phone-started scene under the
man's home (where his schedule puts him most). About **60% of places** are hot, not 100%.

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

**Overnight windows are supported — but ONLY on a row that covers every weekday.** The wrap and
the weekday are two separate checks, and the weekday one runs first against **today**:

```
v2.py:3800   if (!setup._weekdayMatches(ds.weekdays, todayIndex)) continue;
v2.py:3801   if (!setup.isCurrentTimeSlot(ds.start_time, ds.end_time)) continue;
```

`isCurrentTimeSlot` does handle the wrap (`if (endTotal < startTotal) return currentTotal >=
startTotal || currentTotal < endTotal;`, the `isCurrentTimeSlot` definition at `v2.py:4152`). So
`weekdays = [0,1,2,3,4,5,6]`, `22:00`–`04:00` is correctly **one** row.

⚠️ **But `weekdays = [1]`, `23:00`–`06:00` puts the character on site on Tuesday night and DELETES
them at midnight**, because `todayIndex` is now Wednesday and Wednesday is not in the list. A
day-specific overnight window needs **two rows** — `[1] 23:00–00:00` and `[2] 00:00–06:00`. The end is
exclusive, so `23:59` would lose the last minute; `00:00` wraps and keeps it.

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

### What the reference game requires of its own writers

`[added 2026-08-31]` **We have measured that game ten ways and never read its instructions to its
writers.** Four rules from its own Writer's Guide that this skill did not hold:

**1 · The three-way personality check is MANDATORY on every player line.**

> *"It is essential you include all three checks when the player speaks up."*

Meek / bratty / neutral, every time she speaks. This is the mechanism behind the field's largest
love-reason — **freedom, 25.9%, against premise at 0.0%**. Mechanically it is `block_pool`.

**2 · Per-character mood axes are enumerated and REQUIRED.** Each character has named axes —
cheerful↔traumatised, shy↔obsessive, pure↔corrupt — and:

> *"Scenes that can trigger at any level of trauma need variants to cover both."*

We have per-NPC meters and no rule that a scene must cover their range.

**3 · A required exit matrix on every encounter** — she resists, she ends it herself, she asks to
stop — **the first two required for all encounters**. Our `she can say no` fails only on zero across a
whole game, which is a floor, not a matrix.

**4 · Character bibles are ONE LINE.**

> *"Mrs. Hale: The landlady. Collects on Friday and remembers every late week. Tired, fair, never
> charming."* — ours, in the one-line shape the reference game's writer guide asks for

A page is where an author hides the fact that they have not decided anything.

---

## 3. The meters — declared here, designed in `the-meters.md`

**The design decision is not on this page.** Which meters exist, who owns them, how deep the ladder
goes and what a throttle is for all live in `references/the-meters.md` W1–W6. This section is the
declaration and the two rules the gates read off it.

### 3a. Declare who climbs — first of the meters, after the systems

```jsonc
"who_climbs": "player" | "cast" | "both"
```

The field splits, cleanly, into two schools with nothing between them: **8 roster games** put 65%+
of their character-gating on per-character meters, **9 ladder games** put 13% or less.
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

**The board sets the rung numbers.** The default is the field's: **8–17 rungs, the lowest near 5**
(`the-meters.md` W4). The spine's first gates start there, and the board may move them.

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
  descent wearing an ascent's clothes.
- **The ceiling must be bought.** Every band boundary is a promise to the player, so the highest
  band `min` needs an authored gate on that trait at or above it, or the points past the last gate
  buy nothing. Gate 8. Two exceptions: the band holding the meter's **starting value** (a meter that
  starts full and drains starts there), and a meter declared `falling = true` in `[[traits.labels]]`
  (read by `gates.py` only).
- **Every meter you raise is read by something.** Gate 33, `the-meters.md` W3.

**Where ceilings live:** `sidebar_items[].bands[]`. **Not** in `player.core_traits`, which is
a flat map of starting values only.

**The operators a trait gate may use.** Six, and every evaluator in the engine agrees on all six:

```
eq   ne   gt   gte   lt   lte
```

⚠️ **`ne` is legal and this skill never said so.** It has worked on a canvas, node or choice
condition since v2 shipped, and until 2026-08-29 the only two places it appeared in this skill were an engine architecture section
and a warning telling you not to use it on a quest card. *"She is not at stage 3"* is the negated
form of the field's commonest gate shape (`the-surfaces.md` R5d) and it is one word.

⚠️ **Quest cards take five, not six** — `[[quest_cards]]` `when` and `goals` reject `ne` at build
time, deliberately, because their evaluator has no case for it. `the-voice.md` R2 and `engine.md`
§37. Do not widen that whitelist without the evaluator case in the same change.

⚠️ **`compare()` accepts six more** — `in`, `not_in`, `contains`, `not_contains`, `exists`,
`not_exists` — **and nothing else in the engine does.** A gate using one of those opens the door and
then reads as false in the locked-reason line and in every hint. Treat the six above as the set.
`engine.md` §37 carries the count.

---

## 4. The daily loop — `board.needs[]`

An ordinary day when no story is happening: sleep, eat, wash, earn, spend. This exists in every game
of this shape regardless of who is in the cast, and it is what the TRIGGERED layer hangs off —
*"during the weekends"*, *"when exposed"*, *"at high stress"* are all readings of an ordinary day.

**It is a declaration, not a note to self.** Authors build toward what is measured: a need with no
field shipped a game whose anchor room is a kitchen with no food and no bed.

Declare each need with the four fields from `the-meters.md` M8:

```jsonc
"needs": [
  { "key":   "energy",
    "falls": "8 a day",                                   // [player.trait_decay]
    "fills": "her_room · Sleep · 8 hours",
    "costs": "nothing",
    "shuts": "under 20 she will not go out" }             // ← gate 29 checks THIS
]
```

- **Needs are per game, not a fixed list.** A truck stop's body is not a household's.
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

Record in `v2_state.json`: every system card, every meter and the infrastructure, every location
with its budget and current fill, every character with its surface count and schedule rows, the
ascent meter and its ceiling.

Then run the check that reads the ledger alone — before any TOML exists, `gates.py` has nothing to
read and says so:

```
python3 .claude/skills/author-game-v2/scripts/shape.py <slug>
```

The scoreboard (`gates.py`) takes over once the build writes `7_final_game.toml`.

Then set `phase = "board"` and move to `references/the-sheets.md`: write the sheets LO reads and
signs, before any TOML.
