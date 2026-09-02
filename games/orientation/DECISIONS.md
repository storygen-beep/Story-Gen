# DECISIONS — Orientation  `[READY]`

> Blocked by **reversibility**, per `the-sheets.md`. **A** cannot be changed once a release ships.
> **B** is expensive — it moves prose, ids or saves. **C** is cheap and can move at any time.
>
> **S7: this sheet and `v2_state.json` are one document written twice.** Every key below is at the
> exact path a gate reads. The first ledger written to a schema nothing consumes silently degraded
> six gates to backstops, one of them printing *"[top-3 guess — no v2_state.json]"* while the file
> sat there being read by a different gate.

The verdict has four parts: **Character · Coherence · Correctness · Convenience.**

---

# A · Locked once a release ships

## A1 · `narration_person = "second"`
Immutable after v0.1. Changing it rewrites every line in the game.

## A2 · Location ids, canvas ids, flag keys, trait keys, the title
`the-returning-player.md`. Renaming an id is invisible to every gate in this skill and **strands
every save in the wild**; the engine's migration seam repairs additions and nothing else. The ids
below are the contract:

```
the_avenue  the_hall  the_quad  the_row  her_room  the_kitchen  the_bathroom
the_back_bedroom  wes_room  the_pledge_house  halloran_office  the_counter

npc_ray  npc_wes  npc_dee  npc_simone  npc_halloran

nerve  appetite  reputation  home_face  rest  clean  fed  money  followers
```

## A3 · `board.who_climbs = "player"`
The brief is that **college** corrupts her, so the ladder is hers and the cast meters stay light.
Gate 34 checks the built game against this: `player` wants ≥60% of meter-gating on her own tiers.

⚠️ Deliberately outside the 19–29% band all five prior v2 games landed in **by accident**. The field
splits 8 roster / 9 ladder with nothing between 15% and 65%.

## A4 · `want.player.definition = "blank"`
First `blank` in v2. Field runs 19 blank / 10 written with blank holding 80.4% of top-30 engagement;
eight prior v2 games are `written` and **no ledger records anyone choosing it.**

**Cost, accepted:** no written past to gate on, so every early gate hangs on the start choice or on a
meter. Her face is fixed by real-performer media either way — blank means we do not write her past.

## A5 · The map is `nested_zones`, rooted on `the_avenue`
`the_avenue` is the declared exterior and it is a **root** — no `entry_from`. Gate 28 fails a
declared exterior that hangs off an interior room, and the measured failure stepped out of a kitchen
straight into a row of shops. Nothing here does.

```
the_avenue ──┬── the_hall ──┬── her_room  (home base)
 (ROOT,      │              ├── the_kitchen
  exterior)  │              ├── the_bathroom
             │              ├── the_back_bedroom
             │              └── wes_room
             └── the_quad ──┬── the_row ── the_pledge_house   ANCHOR
               40 min, $2   ├── halloran_office
                            └── the_counter
```

⚠️ **RESTRUCTURED 2026-09-02, from `two_hub`.** The first build declared `two_hub` and hung all five
house rooms off **the street**, because the board wanted two roots and the engine refuses them
(`template_import.py:4306` hard-fails a `navigation_order` entry whose `entry_from` is not that
location). The workaround made `the_avenue` the root of the house as well as the road to campus, and
that is `the-map.md` R3's own inverted map — *"the home contains a bit of world"*. **There was no
house.** She walked out to the street to get from her bed to the bathroom, and the prose named a
landing 7×, stairs 6× and a corridor 3× that the map did not contain (R5: *"three uses of the same
word is a place"*).

Measured against the 25-game mopoga corpus: the avenue carried **2 things to do against 6 ways out**,
the quad 5 against 4, and every other room 1 way out. Field median for a place is **3 things to do
and 1 way out** (`the-surfaces.md:151-156`, measured by playing five games).

`nested_zones` is `the-map.md:38`'s *"default to beat"* and a literal description of this premise —
*"a town or campus **plus** a home."* Depth is free: validation is existence, cycle-DFS and
child-membership only, and `steam`, `vesper` and `the_inheritance` all ship depth 5. Two roots are
still impossible, and are no longer wanted.

The bridge is unchanged: `costs = { time = 40, money = 2 }` **on `the_quad` location**, which is
`the-map.md`'s own mechanism for friction between zones. **The crossing is still a favour she can
ask a man for instead of paying — and that canvas is still unbuilt.** See the open-debt note in
`v2_state.json`.

## A5b · `the_row` is open ground, and 0.1 ends on Ray's door
`act_quad_row` — *"Cross to the row"* — was 0.1's declared locked door. It was a canvas whose only
content was its own `locked_text`, gated at `reputation >= 85`, and whose reward branch sent the
player back to `the_quad` after thirty minutes with **no effect, no flag and no destination**.
`gates.py` printed it as a lint on every build — *"costs 30m and leaves nothing behind"* — and it
shipped anyway. **Deleted.**

The row is a street in this game's own prose (17 sites, the sidebar band *"The row knows who you
are"*, an item called `row_dress`). It is ground now: walkable at any reputation, carrying the
pledge house. The other seven houses are **reputation-banded prose on the location**, not seven stub
locations and not a locked door onto an empty street — a player who grinds to 85 must not arrive at
nothing, which was the original defect wearing a new costume.

What 85 buys is `act_row_walk`'s gated exit: **being spoken to on that street first**, which sets
`row_knows_her` for 0.2. That canvas also carries the reputation tier's **only** `gte` site —
deleting `act_quad_row` took gate `ascent tiers expand the world` red with reputation at 0 expand /
0 contract, because a declared tier that gates nothing is not a tier.

**0.1 now ends on Ray's door** (`appetite >= 70`, `[locations.door]` on `the_back_bedroom`) and
Simone's landing (`nerve >= 50`) — 19 shown-locked choices, all 19 carrying a reason, and both
headline doors have authored content behind them.

⚠️ **R4 naming risk, accepted in the open.** `the-map.md:180-183` killed **`The Parade`** for being a
word a player cannot resolve off a button. *"The Row"* is the same class. It survives because the
game teaches it before the card exists — the meeting with Simone, the dress on the rail, the sidebar
band — and because R4 puts the load on the **location's own description** where the button cannot
carry it. Its first clause says *eight houses* for that reason.

---

# B · Expensive — moves prose, ids or saves

## B1 · The fill budget · `board.locations[].fill`

Declared **before the prose**, in round numbers. Gate 1 refuses to credit a budget that is mostly
non-round, because a budget written afterwards is a description and **cannot fail**.

| location | fill | anchor |
|---|---|---|
| `the_pledge_house` | **12,000** | ✅ **25.8%** |
| `the_quad` | 5,000 | |
| `the_kitchen` | 4,500 | |
| `her_room` | 4,000 | |
| `halloran_office` | 4,000 | |
| `the_bathroom` | 3,500 | |
| `the_counter` | 3,500 | |
| `the_avenue` | 3,000 | |
| `the_back_bedroom` | 3,000 | |
| `wes_room` | 3,000 | |
| `the_hall` | 600 | |
| `the_row` | 400 | |

**46,500 · 12/12 round.** Clears gate 1's backstop
(`MEDIAN_LOCATION_WORDS = 3000`, `MEAN_LOCATION_WORDS = 4500`).

⚠️ **The anchor was raised 11,500 → 12,000 by the same edit that added the two locations, and it
had to be.** Gate 1's plan-anchor test is `max(fill) / sum(fill) >= 25.0` (`gates.py:4784-4790`).
At 11,500 / 45,000 the anchor sat at 25.56% — **0.56 points of headroom**, so any new budget above
1,000 words in total would have introduced a failure line that did not exist before: *"the PLAN has
no centre."* This is `the-board.md:137-139` in practice — **budget the anchor against the FINISHED
total, not the current one.** The two new rooms are small on purpose: a hall and a street are
corridors with one row each, and `the-board.md:55-59` says a 300-word satellite is not a defect
**provided you declared it as one**.

⚠️ **Why this large.** `night_desk` is the only other game built from sheets. It scores **39/40** and
the one gate it fails is this one — 4,590 words, mean 656, **seven times too small.** Nothing about
it was badly made; there was not enough of it for the structure to hold anything up.

⚠️ **The anchor is a RATIO and it tightens as everything else grows.** Budget it against the finished
45,000, not against the current total. One build watched a front room fall 53% → 46% → 40% → 39% →
35% without losing a word.

## B2 · The cast is five, and each owns a different corner
`the-surfaces.md` R8 — a character is separated by **the subject he talks about and the people who
are his**, and by **a place and an hour where he is the only one there.**

| | owns | alone with her |
|---|---|---|
| `npc_ray` | the house, the money, the car | `the_kitchen` 22:00–01:00, after Dee leaves |
| `npc_wes` | the ride, the bathroom, the campus he already knows | `the_bathroom` 07:00–08:00 |
| `npc_dee` | the shift schedule, the rules, the reason it costs | `the_kitchen` 17:00–21:00, before she leaves |
| `npc_simone` | the pledge ladder, the other girls, the party, the dues | the house office, Friday 17:00–19:00 |
| `npc_halloran` | grades, the department, office hours | `halloran_office` 16:00–18:00 |

Five good voices scheduled into one room every evening still read as one person. These do not
overlap.

## B3 · `homes` — declared, never guessed
`ray` and `dee` → `the_back_bedroom` · `wes` → `wes_room` · `simone` → `the_pledge_house` ·
**`halloran` → `offscreen`**, deliberately: faculty, lives across town, has no bed in this world.

⚠️ Only a declaration separates *lives elsewhere* from *was never given a room*. The measured failure
counted four doors in its landing description while three of its four men slept nowhere at all.

## B4 · Two arcs in v0.1, and the rest is logged as debt
`the-arc.md`. Across twelve built games and **1,396 canvases this repo has zero arcs** — every hub
and act loop is authored in its converted state on day one.

| | steps | direction | converts into |
|---|---|---|---|
| `npc_ray` | 9 | **hers** — how far will she go | the kitchen act surface |
| `npc_simone` | 7 | **theirs** — getting the house to take her | the upstairs on party nights |
| `npc_wes` | — | converted day one, 3 rungs | **arc debt, owed 0.2** |
| `npc_halloran` | — | converted day one, 3 rungs | **arc debt, owed 0.3** |
| `npc_dee` | — | no ladder, deliberate | she is the price tag |

## B5 · The phone ships in v0.1 — messaging, then the feed
`the-phone.md` P1 answers yes three times. Build order is the field's (messaging 24/27, the thing
that makes her looked at 20/27) and **not** the engine's app-type list — an author reading down that
list builds the 4-of-27 thing before the 24-of-27 thing. No map (0/27), no bank, no job board.

**The `corruption_min` finding, and the call taken.** `post_actions`' only gate reads
`player.core_traits.corruption` **literally** — `v2.py:2652`, `:2764`, `:2824`, `:2440`. No trait of
that name exists here, so every rung above the first would read 0 and sit permanently `🔒`.

**Taken: the hybrid, no engine change.** Bottom two rungs use `post_actions` with `daily_cap` and no
`corruption_min`. Every rung above is a **canvas the feed links to**, gated on `nerve` through
`setup.triggerConditionsSatisfied` (`v2.py:2204`) — the same evaluator canvases use (`v2.py:3888`).
**Cost:** the native `🔒` / `✓` rendering is lost above rung 2.

⚠️ `followers` **buys a door** — at 200 the row answers her. A counter with no sink is the
`college-daze` complaint waiting to happen.

---

# C · Cheap — can move at any time

## C1 · `fed` survives probation, on one clause
Under 30 no `appetite` rung will raise. If that reads as invented at review, **cut it to two needs
and log the cut** rather than leaving a chore in the game. A need that shuts nothing is a chore, and
gate *a need shuts a door* fails any declared need no condition reads.

## C2 · Rungs start at **5**, not 15
All sixteen declared tiers across five v2 games put their lowest rung at exactly 15, because
`templates/board.toml` carries that band table. The field's live meters run **8–17 rungs with the
lowest at ~5**. Read that against the measured failure where twelve clicks of one free choice moved
a meter 4 → 16: **the opening of a v2 game is fifteen clicks in which nothing the player does
changes anything.**

## C3 · Location names — the contract
Public venues **bare** (`Quad`, `Counter`, `Pledge House`); owned interiors **possessive**
(`Your Room`, `Ray's Room`, `Wes's Room`). Consistency beats flattening; the defect is being
inconsistent. Flavour lives in the description, never on the button.

## C4 · The eight o'clock has no room of its own
It is a row on `the_quad`. A lecture hall with two hundred people in it is not a surface, and
`the-map.md`'s count is derived from **needs + work + people** — a hall answers only *work*, thinly.

---

# The gate reconciliation — S6

**Nothing a gate requires may be deferred by a sheet.** A bathroom sheet once said of its walk-in
*"Not authored this release. Named here so it is not forgotten"* — honest, deliberate, signed off,
and `the walk-in floor` is a **gate**, which failed 0/5. **A deferral is not a pass.**

| gate | where this design answers it |
|---|---|
| location fill | B1 — 45,000 over 10, declared round, before the prose |
| the map is a place · residents have homes · world reachable | A5, B3 — `nested_zones`, 12/12 reachable on foot from `the_avenue` |
| standing surface | B2 — every character has ≥1 surface and ≥1 schedule row |
| **the walk-in floor** | `the_bathroom`, `the_counter` back room, `the_kitchen`, `halloran_office`, `the_pledge_house` office — **all five authored, none deferred** |
| the climb is paid for | every rung carries a price or a day-cap flag **set on the choice** |
| a need shuts a door | all three needs carry a real condition (SYSTEMS §3) |
| a meter is read · the wardrobe is read | `worn_exposure` on the ambient roll; `followers` at 200 |
| she can say no | the two parked refusals, plus in-scene stops |
| a locked door says why | every `show_when_locked` row carries the bar and the number |
| ends on an opening | A5b — v0.1 closes on **Ray's door** (`appetite` 70) and Simone's landing (`nerve` 50). It used to close on `act_quad_row`, which had nothing behind it. 19 shown-locked choices, 19 with a reason |
| the start choice is read | `past_*`, 5 read sites each |
| what she picks is read | `@player`, `@ray.rel`, `@wes.rel` |
| every hub is met first · a meeting fires where they are | F5/F8 — one flag per character, `trigger.schedules` matching their own hours |
| the obligation is charged | $120 Friday. **If `[settings.rent]` does the charging, do not also author a canvas that narrates the payment** — write the scene beside it |
| money gates something · what money buys opens a door | B5 and the three purchases in `board.economy.buys_a_door` |

---

## Sign-off

`board.map.r1_signoff` is **UNSIGNED**. It records **who** and **when**, and a sign-off written by
the author of the map is not a sign-off — the game that shipped seven rooms of a house at 26/26
recorded *"Signed off in the board phase"* with no name and no date.
