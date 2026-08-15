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

**How many locations is not a number you pick. Derive it:** the places your declared cast's rotas
actually visit, plus the places the daily loop requires — where she sleeps, where she earns, where
she washes, where she crosses. Write that list and count it. That is the answer.

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
- **What is in it that she can act on** (`objects`) — the things the room's prose will name and
  she can do something with. *"the roll cages", "the cold store", "the recorder", "the eleven feet
  of corridor", "the padlocked door".* Not every noun: atmosphere goes in the prose, not this list.
  **This is what decides how many choices the room has** — every choice belongs to one of these,
  though a single object may afford several (a bed affords *get in* and *change first*). The
  relation is many-to-one, never one-to-one: do not invent an object to justify a choice, and do not
  cap an object at one choice. Gate 22 checks that each declared object is written and usable; how
  well the choices hang off the prose is reported as a lint. See `the-surfaces.md` R2b and R3.
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
v2.py:3446   if (!setup._weekdayMatches(ds.weekdays, todayIndex)) continue;
v2.py:3448   if (!setup.isCurrentTimeSlot(ds.start_time, ds.end_time)) continue;
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
the fiction rather than bolting it on. A lodger's room, a locker at a gym, a chair in a bar.

It only pays off if content is filed by **how long it lives**, and this is the part that gets
missed:

| scope | what it covers | file | survives a rotation? |
|---|---|---|---|
| **TENANT** | his ladder, his register, his props, his one paid-off secret | `5_scenes.toml` | no — dies with him, deliberately |
| **ROOM** | the slot itself, the furniture, the wall, what the arrangement IS | `3_activities.toml` | **yes** |

**Room-scoped content names the occupant by ROLE, never by name.** *The lodger*, not *Marek*.
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
different headboard heights, and the fact that the terms get set in the first fortnight by
whoever is standing there when the new one arrives.

---

## 3. The meters — three layers, measured

Not one meter. **Three layers**, and they do different jobs. Measured directly from the
reference game's seed source, because our first draft of this section said "exactly one
global axis" and the source refuted it:

**Layer 1 — ratcheting ascent tiers. Three or four, each naming a DIFFERENT transgression.**

| tier | raises | lowers | gate sites |
|---|---|---|---|
| promiscuity | 22 | 1 | 206 |
| deviancy | 20 | 0 | 129 |
| exhibitionism | 12 | 1 | 167 |

Nearly one-way — they ratchet. And they gate hard: **their rungs sit at 15 / 35 / 55 / 75**,
a four-rung ladder twenty points apart. Copy that shape.

Why several rather than one: each names a different *kind* of going-further — sleeping around,
being seen, doing the strange thing. A player who doesn't want one can still climb another.
A single undifferentiated "corruption" collapses three parallel ascents into one and gives
every player the same ladder. There is also a counterweight tier (`purity`, 58 gate sites)
moving the other way.

**Layer 2 — volatile state.** Arousal, stress, energy. These move constantly in both
directions (arousal: 277 sets, 55 increments, 8 decrements) and are managed minute to minute.
They are *not* ascent and must never be confused with it — a meter that goes up and down is
weather, not progress.

**Layer 3 — light per-character tracks.** Love, lust, and a disposition, per named character.
Light on purpose: the ascent tiers do the heavy gating, and these colour the individual arc.

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

```toml
[player]
core_traits = { corruption = 0, energy = 100, money = 20, … }   # flat {key: initial}

[[sidebar_items]]
type  = "trait_status_text"
trait = "corruption"
bands = [
  { min = 0,  max = 24, text = "…" },
  { min = 25, max = 49, text = "…" },
  { min = 50, max = 74, text = "…" },
  { min = 75, max = 100, text = "…" },
]
```

Two hard rules, both gated:

- **Rising must expand.** For each ascent tier, `gte`/`gt` gates must outnumber `lt`/`lte`.
  Gate 10 checks the three most-gated meters. A meter whose rise mostly *closes* content is a
  descent wearing an ascent's clothes — the measured failure case had exactly that as its
  dominant meter, with the world contracting to a sealed room as it rose.
- **The ceiling must be bought.** The top band's `max` is a promise to the player. If the
  highest authored gate on that trait is below it, the remaining points buy nothing. Gate 8.
  *(A top band with no `max` is unbounded on purpose and promises nothing.)*

**Where ceilings live:** `sidebar_items[].bands[]`. **Not** in `player.core_traits`, which is
a flat map of starting values only.

---

## 4. The daily loop and the money

Write down what an ordinary day is when no story is happening: sleep, eat, wash, earn, spend.
This exists in every game of this shape regardless of who is in the cast, and it is what the
TRIGGERED layer hangs off — *"during the weekends"*, *"when exposed"*, *"at high stress"* are
all readings of an ordinary day.

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
