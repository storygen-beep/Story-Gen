# SYSTEMS — Orientation  `[READY]`

> `the-surfaces.md` **R2c**. A room's rows are its **systems surfacing in that room**, so this
> document exists before any place sheet. `night_desk` was built to R2 alone and its rooms came out
> as a night porter's duties — *walk the property · fix the sign · hit the ice machine* — correctly
> derived and with nothing to want in them. The cause was six declared meters, no clothing, no
> items, no phone: **there were not enough systems to give six rooms a list.**

Nineteen keys. Every one names where it surfaces, and nothing goes in a room list that is not on
this page.

---

## 1 · The ascent — three tiers, player-owned

`board.who_climbs = "player"`. Rungs start at **5**, not 15.

| key | what going further means | rungs | sidebar |
|---|---|---|---|
| `nerve` | doing it where someone can see | 5 · 15 · 30 · 50 · 70 · 90 | banded, `hidden` |
| `appetite` | what she will take, and whether she is the one who asks | 5 · 15 · 30 · 50 · 70 · 90 | banded, `hidden` |
| `reputation` | how much of campus has heard | 10 · 25 · 45 · 65 · 85 | banded, `hidden` |

⚠️ **`hidden = true` in `[[traits.labels]]` on all three.** Gate *a banded meter is not also a
number* fails a banded sidebar stat that also prints its raw value.

**`reputation` is an audience meter** (`the-meters.md` W5b). It rises, it **rarely refuses**, and it
still decides things — its job is that people already know, delivered as one-line swaps. Do **not**
apply W5's shuts-a-door test to it. Field: ~10% of its branch arms carry a link; a median 41% of its
reads change something mechanical without ever printing a refusal.

**Surfaces in:** every hub. `nerve` at `the_pledge_house` upstairs and `the_quad`; `appetite` at
`the_kitchen` and `halloran_office`; `reputation` everywhere, mostly as a swapped line.

---

## 2 · The counterweight — `home_face`

What the household still believes about her. Starts at 100 and falls.

- **Falls** when the two hubs touch — campus carried home, a `reputation` rung that reaches the
  house, being seen on the avenue with someone from the row.
- **Shuts** (W5, and it must shut something or it is a falling number charged for nothing):
  **above 60, Ray will not move.** His arc steps 5–9 all carry `home_face lt 60`. Dee's questions at
  the kitchen table get sharper below 40.

**Surfaces in:** `the_kitchen`, `the_back_bedroom`, `the_hall` (the house reporting who is in), `the_avenue`.

⚠️ This is the wire between the two charges. Campus raises the three tiers; carrying it home spends
this one; spending it is what opens the taboo. If it ever stops doing that, the two halves of the
game are unconnected and this key should be cut rather than kept as decoration.

---

## 3 · Needs — the body's clock

`the-meters.md` M8–M10. Four fields each, and `shuts` is the load-bearing one.

| key | falls | fills | costs | shuts |
|---|---|---|---|---|
| `rest` | 12 a day | `her_room` · Sleep · to 07:00 | free | under 30 the eight o'clock is closed, and Halloran's ladder runs through attendance |
| `clean` | 15 a day | `the_bathroom` · Shower · 25 min | free at home, $2 at the house | under 40 she will not go where she is looked at — every `nerve` rung is shut |
| `fed` | 20 a day | `the_kitchen` · Eat · 20 min · free · `the_counter` · Eat on shift · 15 min · $4 | $4 on campus | under 30 no `appetite` rung will raise — she cannot hold a nerve she has not fed |

⚠️ **`fed` was on probation and it survives**, on the `appetite` clause above. Gate *a need shuts a
door* reads `key` and fails any need no condition reads, so all three carry a real condition. If the
`appetite` clause reads as invented at review, cut `fed` to two needs and log it in `decisions`
rather than leaving a chore in the game.

⚠️ `[player.trait_decay]` takes a **positive magnitude** — the validator rejects a negative.

---

## 4 · Money

| | |
|---|---|
| currency | `money`, symbol `$` — one notation on every button, in every paragraph, and in `[settings.rent] currency_symbol` |
| obligation | **the dues** — Friday, at `the_pledge_house`, Simone counts on the office desk |
| amount | **$120** opening |
| week income | **$260** honest maximum (46%) |
| moves by | **cost follows holdings** — every commitment she signs adds weekly upkeep |
| sinks | the dues · the meal plan · the bus · the lab kit · clothes that make a `nerve` rung reachable |

**Surfaces in:** `the_counter` (the only source), `the_pledge_house` (the dues), `the_avenue` (the
bus), `the_union_shop` (the lab kit and the two garments).

---

## 5 · Clothing — `[[clothing]]`

Two jobs, and they are different (`the-arc.md` **A6**):

- **A garment is a rung.** Simone's step 5 asks her to *wear* something, not to do anything — the
  arc will not pass until she does.
- **Clothing moves the odds the world acts.** `worn_exposure` shifts the floor of the ambient roll
  at `the_quad` and `the_pledge_house`. Same scenes, twice as much world.

**Surfaces in:** `the_union_shop` (**where she gets them** — the engine's shop screen, off
`[settings] shop_location`), `her_room` (the engine's wardrobe link, off `wardrobe_location`), and as
a predicate everywhere.

⚠️ **Both halves are needed and only one used to exist.** Until 2026-09-03 this game declared
`clothing_enabled`, a `wardrobe_location`, two `initial = false` garments and four conditions reading
them — and **no `shop_location`**, so nothing could put either garment in the wardrobe. `row_dress`
and `black_set` are the only garments carrying `exposure = 1` / `type = "going_out"`, which is what
all four conditions read, so all four were dead and Simone's step 5 could not be entered. **A read is
only armed if something she can obtain satisfies it.** Gate: `a declared garment can be got`.

`worn_exposure` is the only one of the four worn predicates that reads an empty slot.

---

## 6 · The cast's meters

`the-meters.md` **W6**: one willingness word for the whole game, everyone on the same scale,
differentiated by what modifies it — never by giving people different vocabularies.

| character | meters | rungs |
|---|---|---|
| `npc_ray` | `relation` + `lust` | 3 |
| `npc_simone` | `relation` + `lust` | 3 |
| `npc_wes` | `relation` | 3 |
| `npc_halloran` | `relation` | 3 |
| `npc_dee` | `relation` | 2 |

The rich pair goes to **Ray and Simone only** — the two arcs that carry the game. Field median is
**3 rungs per person**; the 8–17 figure is the player's ascent meter and does not transfer to the
cast. A character who gates nothing is not in the game yet, so Dee's two rungs gate the kitchen
window.

---

## 7 · The phone

`the-phone.md`. P1's three questions are all yes here: she cannot reach Wes while she is at home,
Dee's shift and the pledge house run offscreen, and `reputation` **is** being looked at by people
she is not in the room with.

Build order is the field's, not the engine's app-type list: **messaging (24/27), then the thing that
makes her looked at (20/27), and nothing else.** No map (0/27), no bank (7/27), no job board (4/27).

| app | type | what it is |
|---|---|---|
| messages | `messaging` | Ray, Wes, Simone, Dee. Threads arrive; the trigger is a **latch** |
| `flaunt` | `social_feed` | she posts. `followers` counter, and it **buys** something |

⚠️ **`followers` must buy something or it is not counted** (`the-economy.md` R1b): at 200 the row
answers her, which is the `reputation` 45 rung's cheapest route in.

⚠️ **The `corruption_min` finding, and the decision taken.** `post_actions`' only gate reads
`player.core_traits.corruption` **literally** — `v2.py:2652`, `:2764`, `:2824`, and `:2440` for
daily topics. No trait of that name exists in this game, so every rung above the first would read 0
and sit permanently `🔒`. **Taken: the hybrid.** The bottom two post rungs use `post_actions` with
`daily_cap` and **no** `corruption_min`; every rung above that is a **canvas the feed links to**,
gated on `nerve` through the full evaluator — phone content is evaluated by
`setup.triggerConditionsSatisfied` (`v2.py:2204`), the same evaluator canvases use (`v2.py:3888`),
so it can read any condition type a canvas can. Cost: the native `🔒` / `✓` rendering is lost above
rung 2. No engine change requested.

⚠️ **Nothing on our phone costs anything** — `sendDailyChat` (`v2.py:2375`) applies effects and
returns; there is no `advanceTime` anywhere in the phone block. Charge with `daily_cap` and
`cooldown`, and in the fiction. A free infinite button is the *use the app, wait, use the app*
complaint.

**A message is 11–16 words**, lowercase, no full stops. The phone is its own register and it is the
one place 35–40 does not apply.

---

## 8 · Arc flags

| | |
|---|---|
| `ray_01` … `ray_09` | one-shots, each gated on the flag before it. Step 9 sets `ray_open`, which opens the kitchen act surface |
| `simone_01` … `simone_07` | same shape. Step 7 sets `simone_open`, which opens the upstairs on party nights |
| `ray_refused` · `simone_refused` | the **parked** refusal (A3b) — free, reversible, and the game prints the place and the hour to come back to |

**Surfaces in:** one-shots at their characters' own hours. Every arc step's canvas carries a
`trigger.schedules` window matching that character's schedule rows — `requires_npc` does **not**
gate the auto-fire path, so a step without one plays to an empty room.

---

## 9 · The start choice

`past_top` · `past_crowd` · `past_nobody`. Asked once on the arrival night, by Wes. **Five read sites
each**, additive only: every original rung keeps its numbers and gains `<flag> is_false`.

⚠️ Separate the past-ladder from any surface's existing ladder with a **non-`group` block**.
Adjacent `[group]` blocks merge into one if/elseif chain and first match wins (`v2.py:14637`) — the
original ladder goes dark with no error.

---

## The count, and what it is for

**19 keys** — 3 tiers, 1 counterweight, 3 needs, money, clothing, 7 cast meters, followers, and two
flag families. Against `night_desk`'s six.

⚠️ **This is not a target and there is no defensible number.** The field's own spread on a crude
instrument is 52 → 693 variables used 25+ times, a 13× range, and it counts `$vars` in built HTML
while ours live in `player.core_traits`. What the count is for is the R2c test: **can every room's
list be written from systems that already exist, without inventing a chore?** Step 2's place sheets
answer that, room by room. If any room needs a row this page does not have, the row does not get
invented — either the system goes on this page first, or the room is smaller than it looked.
