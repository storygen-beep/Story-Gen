# SYSTEM · cover — how brazenly she wears the body as a tool  `[READY]`

| | |
|---|---|
| **kind** | `sourced` — the wardrobe is one place; the doors are everywhere |
| **key** | `cover` (0–100) — **also an ascent tier** (`board.ascent_tiers`) |
| **fed at** | `kess_berth` (the wardrobe) + the rungs that spend it |
| **labels** | `checks_cover` · `outdoors` |
| **mechanism** (S8) | a player trait. Rungs are garments and brazen uses; reads are `trait` conditions and stacked `[group]` bands. Not rotation. |

A meter is one kind of system. This one is both — which is legal and is why it is written here as
well as in `board.ascent_tiers`.

---

## THE LADDER

`the-meters.md` W4: the field's live player ascent meters run **8–17 rungs, densest at the bottom,
lowest rung at a median of 5.** All 16 tiers across the five earlier v2 games put their lowest rung
at exactly **15**, copied from one example — which makes their opening fifteen clicks in which
nothing the player does changes anything. This ladder does not repeat that.

```
5  ·  10  ·  15  ·  20  ·  30  ·  40  ·  50  ·  65  ·  80  ·  100
```

Ten rungs. Ceiling **100**, and there is an authored gate at 100 — gate 8 fails a bar whose top
band buys nothing.

⚠️ **A garment is a rung** (`the-arc.md` A6). The eight on disk are the ladder's spine:
`plain_bra` · `plain_briefs` · `flat_shoes` · `company_grays` · `cover_dockhand` ·
`cover_analyst` · `cover_stranger` · `dress_undertow`.

⚠️ **`grays` is an OPEN question.** `gates.py --words` flags it as a noun none of the 27 field
games use, and it is already on disk as `videos/clothing/company_grays.jpg`, so renaming costs a
media rename. Logged in `v2_state.json` `decisions[]`. Unresolved — LO's call.

## READERS — written first

| # | reader | where | what changes |
|---|---|---|---|
| 1 | does the door admit her | `spire_plaza` · `vance_securities` · `penthouse` | the `checks_cover` label; refusal is a sentence, never a greyed label (SY5) |
| 2 | what the floor pays | `underworld_bar` | the anchor's work rung scales on it |
| 3 | is she read as company | every `zone:reach` room | one clause swapped, not a branch — the field's differentiation is **~20 words, one sentence**, median 84–139 characters |
| 4 | who approaches her outdoors | `the_street` · `underworld_strip` | the `outdoors` label; ambient odds |
| 5 | what Bastien assumes at the door | `bastien_backroom` | what he expects to find before he looks |
| 6 | whether Marsh books her by name | `underworld_brothel` | the slot is bought differently in the dress |
| 7 | the quest card on the `cover` tier | guidance | S10 |

## WRITERS

| # | writer | where | effect |
|---|---|---|---|
| 1 | acquire a garment | `kess_berth` (wardrobe) · shop rungs | `cover` · `op = "add"` · `+5` |
| 2 | wear it somewhere it is the wrong thing | the `checks_cover` doors | `cover` · `op = "add"` · `+5` |
| 3 | work the floor in what he sent down | `underworld_bar` | `cover` · `op = "add"` · `+5` |

⚠️ **THE BRAKE IS ON THE WAY IN** (S9). Person sheets that said *"caps at 44"* read as a property of
the rung; `_is_free` disagreed, and three rounds of adding costs to inner choices moved nothing —
**moving the same costs to the triggers fixed five meters at once.** Every rung above carries its
brake on `trigger.costs` or `trigger.max_triggers_per_day`, not on a choice inside.

Vesper failed `the climb is paid for` on **17 of 18** gated meters — `corruption` 0 → 50 in nine
free clicks. `[INTENT]`: the fastest route to `cover 100` is measured in in-game **days**, and the
two numbers to compute when the build exists are *clicks to the top band* and *in-game minutes to
the top band* (M2).

## Coupled to a need

`clean` shuts this one: under 40 the three `checks_cover` doors refuse her regardless of `cover`.
That is deliberate — it is what makes the bathroom a room instead of scenery, and it is how an act
surface reaches back into the ascent without a new mechanic.
