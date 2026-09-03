# PLACE · The Undertow  `[READY]`  ★ ANCHOR

| | |
|---|---|
| **id** | `underworld_bar` |
| **ENTERED FROM** | `underworld_strip` |
| **WAYS OUT** | `underworld_bar_bathroom` · `bastien_backroom` · back to `underworld_strip` |
| **DOOR** | no — a public floor. Occupancy is a row INSIDE the room (`the-map.md` R6c) |
| **LABELS** | `public` · `zone:reach` · `checks_cover` |
| **fill** | **9,000** `[INTENT]` — **30.4% of the game's 29,600** (floor 25%) |
| **heat** | cycling pool |

## What this place is FOR

**The anchor.** DoL's seed put 30% of all its location prose in one place — the school — and the
game is *about* that place. This is ours: where she works, where men come to her instead of the
other way round, and where the `service` and `cover` tiers are both climbed.

⚠️ **Vesper had NO anchor.** Its deepest location was `captive_room` at **15.5%**, and that room was
sealed with no exits and unreachable on foot. An anchor the world cannot reach is not a centre.

⚠️ **Budget this against the FINISHED total, not the current one.** The anchor rule is a **ratio**,
so it tightens every time any other room grows. Measured on a real build: a front room sat at 4,020
words while six other rooms were written and its share fell **53% → 46% → 40% → 39% → 35%** without
a word being removed. Put 30% of every increment here, do not top it up at the end.

## The list — work + people

No need is served here; `clean` lives next door, which is what makes the bathroom a room.

| # | row | canvas | kind | system | gate | effect | screen |
|---|---|---|---|---|---|---|---|
| 1 | "Work the counter." | `TBD` | work | `coin` | `bar_rung gte 0` | `coin` `add` `+15` · `clean` `add` `-10` | yes |
| 2 | "Work the floor." | `TBD` | work | `coin` · `cover` | `bar_rung gte 1` **and** `clean gte 40` | `coin` `add` `+15` · `cover` `add` `+5` | yes |
| 3 | "Work the floor in what he sent down." | `TBD` | work | `cover` | `bar_rung gte 2` **and** wearing `dress_undertow` | `coin` `add` `+25` · `cover` `add` `+5` | yes |
| 4 | Colm | `TBD` | hub | `service` | `trigger.npc` = `npc_colm`, 19:00–23:59 | — | yes |

**Four rows.** Field median for things-to-do-at-a-place is **3**; gate 20's cap of 8 is a backstop
against the pathological case, not a target. The game built *after* that cap existed put **19 of its
30 screens at exactly 8** and shipped the same 213 choices as the game it was written to fail.

⚠️ **Row 4 passes the object test; rows 1–3 do not, and that is correct.** *"Work the counter"* has
no person as the object of its verb, so it is **work with its own surface**, never a rung inside
Colm's hub. The 23-choice failure was a hub binding no NPC where every choice was a work surface
wearing a menu item's clothes.

⚠️ **`clean gte 40` on row 2 is the coupling.** Every finish takes `clean` down 30, so an evening of
`service` shuts the floor until she uses the bathroom. That is how an act surface reaches back into
the ascent without a new mechanic.

## The ladder across visits (R3c)

`bar_rung` is Colm's own ladder, not a player tier: **3 rungs**, which is the field's per-character
median (p25 2, p75 6). Counter → floor → the room upstairs. Three rungs, and the first is a
conversation.

## Walk-in (R3) — REQUIRED

She works alone here and Colm is scheduled, so gate `the walk-in floor` reads this room. **Vesper
scored 2 of 10.**

```
the router    trigger.substitutions on rows 1-3 (the ACTIVITY), chance x conditions, rolled on entry
the branch    ONE canvas, substitution_only = true, [group] bands on `service`
the payoff    routes into a rung that already exists
```

| band | chance | what changes |
|---|---|---|
| `service lt 20` | 0.10 | somebody watches the counter too long |
| `service gte 20, lt 45` | 0.35 | a hand finds a reason |
| `service gte 45` | 0.70 | she is walked into the back and it is not a surprise to anyone |

⚠️ **ONE canvas, three bands — not three canvases.** Vesper's own `walkin_renner_depot` is the
doctrine's validated example: 2.3 KB, three `[group]` bands on the trait the odds ride. DoL's
equivalent branches are **458 and 473 bytes**. The richness is combinatorial, not authored.

⚠️ **The target MUST declare a `location`** — `getCanvasById` indexes only location-bound canvases
(`v2.py:3177`), so a triggerless rung silently never fires.

## Media

`pool_dir = "sex/colm_loop_*_t5"` and `sex/colm_backroom_t4` — **on disk already, 7 pools**.
`sex/bar_floor_handled_t4` for the walk-in. `sex/colm_ruin_t4` is **EMPTY on disk** and is the one
slot in this room that needs a find-media run.

⚠️ Repeatable explicit content declares `pool_dir` + `pool`, **never a single `file`**.
