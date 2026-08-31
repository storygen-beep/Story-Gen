# Build vs sheet — what the format caught, and what it could not

**The experiment's actual output.** `night_desk` 0.0.1 was designed entirely in Markdown sheets,
signed off, and only then translated to TOML and built. This file records every place the design and
the build disagreed, and answers one question about each:

> **Did the sheet format have a row that would have caught this?**

Design defects found along the way were fixed in the game and are **not** the output — the skill
already knows how to design a game. What is promotable is the list in Part 2.

**Final state: 39 of 40 gates green · 35/35 canvases reached the build · build validates clean.**

---

# Part 1 — the numbers

| | the sheets claimed | the build measured | |
|---|---|---|---|
| rooms | 7 | **7** | ✅ |
| things to do per room | 5 · 4 · 3 · 3 · 3 · 2 · 0 | **5 · 4 · 4 · 3 · 3 · 2 · 0** | ⚠️ the lot gained the bus |
| people | 2, nine rungs each | **2**, 10 schedule rows | ✅ |
| canvases | not counted | **35** | — |
| **beats** | **75** | **52** | ❌ **different definitions** |
| repeatable beats | 50 | **41** | ❌ same cause |
| explicit beats | 6 | **6** | ⚠️ agrees by coincidence |
| explicit share | 12.0% of repeatable | **14.6% of repeatable** · 11.5% of all | ⚠️ |
| words | ~3,670 | **4,590** | ⚠️ +25% |
| opening screens | 12 | **13** | ⚠️ Marek's meeting was not counted |
| quest cards | **not in the format at all** | 9 | ❌ |
| walk-ins | 0, "owed" | **5** | ❌ a gate required them |

---

# Part 2 — the format gaps

## ⚠️ 1 · "BEAT" MEANS TWO DIFFERENT THINGS, and the whole measurement rests on it

**The sheets counted paragraphs. `gates.py` counts NODES.**

Every scene sheet says *"5 beats · 1 explicit"*, and those beats are paragraphs. The instrument's
`Beat` is one node — 52 nodes, 52 beats, exactly. A node holding three explicit paragraphs is **one**
explicit beat, not three.

So the release's headline figure was computed in a unit the build does not use, and the two only
agreed at the end by coincidence: 6 explicit paragraphs, and after the walk-ins were added, 6
explicit nodes. Earlier in the same session the same game read **3** explicit by the instrument and
**6** by the sheet.

**Did the format have a row for it?** It had the wrong row. It has a beat count on every scene sheet
and the count is in the author's unit.

**Change owed:** the format must either count nodes, or say in every sheet header which unit it is
using and print both. A number that does not survive translation is not a measurement.

---

## 2 · No row for how a room attaches to the map

`the-map.md` R3 requires the exterior to be the map's **root**, and gate 28 enforces it. The sheets
put `the_lot` as one of five exits off `the_desk` — an exterior leaf, the exact inversion the rule
was written against.

The place sheet has a `WAYS OUT` block listing doors. It has **no row for which door is the way
in**, so a map can be drawn correctly room-by-room and be wrong as a whole.

**Change owed:** an `ENTERED FROM` row on the place sheet, and one map-shape line on the decision
sheet naming the archetype and the exterior.

*(The re-root cost nothing: the desk still shows five doors, four children plus the implicit way
back, so decision 8's "five exits, LO's call" survived untouched.)*

---

## 3 · No row for a word budget — so the ledger was written after the prose

Gate 1 checks each location against **its own declared budget**, and the point of that is the budget
is declared **first**. The place-sheet format declares a count of *things to do* and never a word
count, so `v2_state.json`'s `board.locations[].fill` had to be invented after the prose existed.

`gates.py` noticed by itself and printed **`[declared budget is post-hoc — judged on the backstop]`**.

**Change owed:** a `fill` row on every place sheet, filled in at design time.

---

## 4 · No row for the mechanism of a cost or an effect

The place sheets carry `20m`, `+energy`, `hunger half`. Nothing says how any of that is *written*,
so the author fills the gap from memory — and got it wrong the same way nine times:

> trait effect uses `op='sub'`, which the engine discards (`applyTraitEffect` runs only
> `['add','set']`, `v2.py:5742-5751`)

Every energy cost in the game would have been free. Caught by the importer's validator, not by the
sheets.

**Change owed:** the format needs one line per effect that names the trait, the op and the value, or
it needs to stop implying a mechanism it does not specify.

---

## 5 · The person sheet says WHERE somebody is and never WHEN — two contradictions shipped

- Del was declared 22:00–02:00 at the **desk** (desk sheet) and 22:00–02:00 in the **office**
  (office sheet). He cannot be in both.
- Marek was declared 00:20–01:30 in the **corridor** and 00:00–01:00 in the **bathroom**. Forty
  minutes of overlap.

Neither is a design defect. Both are two sheets each describing one room correctly, with **nothing in
the format that reads across them.** The person sheet's header line is `at: the_desk · the_office ·
the_bathroom · the_kitchen` — four places and no hours.

⚠️ **And a third thing fell out of resolving them.** `del_30` needs him at the monitor at four in the
morning. No sheet had him at the desk at that hour, so the rung was written and would have been
**unreachable**. A 03:30–04:30 desk row was added.

**Change owed:** the person sheet needs a schedule grid — place × hours × days — not a list of
places. It is the one artifact that can see across rooms and it was the one not doing it.

---

## 6 · The format lets you write "owed" next to something the scoreboard requires

The bathroom sheet says of the walk-in: *"Not authored this release. Named here so it is not
forgotten."* Honest, deliberate, signed off — and `the walk-in floor` is a **gate**, which failed
0/5. A deferral is not a pass.

Five walk-ins are now authored. The one the sheet deferred is among them.

**Change owed:** anything a gate requires cannot be deferred by a sheet. The format needs to know
which of its rows are load-bearing, which means the sheet has to be reconciled against the gate list
before sign-off rather than after the build.

---

## 7 · Nothing connects the design to the ledger the scoreboard reads

The sheets are the design; `v2_state.json` is what six gates read. The first version of that file was
written to a schema nothing consumes — `board.fill` as a dict, `ascent_tiers` at the top level, no
`board.map`, no `board.characters`, no `board.economy`. Six gates silently degraded to backstops and
one printed *"[top-3 guess — no v2_state.json]"* while the file sat there being read by a different
gate.

**Change owed:** the decision sheet and `v2_state.json` are the same document written twice. Either
the sheet generates it, or the format carries the exact keys.

---

## 8 · A rule was specified that the game has no mechanism for

Every scene sheet says *"she speaks 3 ways"* — meek / bratty / neutral, the reference game's own
mandatory personality check. **This game has no personality axis**, so all thirty-three of those
lines shipped as `block_pool`: they rotate at random instead of reading identity.

The format let a mandatory-sounding rule be written with nothing underneath it, three times per
scene, eleven scenes deep.

**Change owed:** a sheet that names a system must point at the meter or flag that drives it, or say
in the open that it is rotation.

---

## 9 · No row for the brake, and the brake is not where the sheet implies

Person sheets say things like *"caps at 44"* and *"+2 relation a visit, caps at 10"*, which reads as
a property of the rung. The instrument disagrees: `_is_free` (`gates.py:2913`) reads
`trigger.costs`, `trigger.max_triggers_per_day`, or a day-cap flag **condition on the trigger**.
Costs written on the inner choices are invisible to it — *"one unbraked door makes the whole rung
farmable, no matter how well priced the other doors are."*

Three rounds of adding costs to choices moved nothing. Moving them to the triggers fixed it at once.

**Change owed:** the sheet needs a `BRAKE` row per repeatable surface saying what stops it, on the
way **in**.

---

## 10 · Guidance is not in the format at all

`quests_engine = "v2"` lights a sidebar entry and a page, and with no cards renders a heading and
nothing. Lostness is the genre's dominant complaint — a 4.7% median share of player comments against
grind's 0.9%. **No sheet in the format mentions a quest card.** Nine were written from scratch after
the first gate run.

**Change owed:** a guidance row on the person sheet and one per ascent tier on the decision sheet.

---

# Part 3 — engine findings, which are not the format's job

Recorded for `engine.md`, not for the sheets:

| | |
|---|---|
| `op = "sub"` parses, imports, and silently does nothing | `v2.py:5742-5751` |
| **quest-card conditions use `trait`; canvas conditions use `trait_key`** — same word, two parsers | `template_import.py:1361` |
| quest goals need a `label` or validation fails; every card needs a `when` | |
| a banded meter is suppressed by `[[traits.labels]] hidden = true`, **not** by `hide_value` on the sidebar item | `engine.md` §30 |
| `_is_free` reads the trigger, never the inner choices | `gates.py:2913` |

---

# Part 4 — the one gate that did not go green, and will not

```
[FAIL]  location fill   7 locations · 4,590 words · mean 656 · median 599
```

The backstop expects a mean of **4,500 words per location**. This game has **656**.

**That is not fixable by editing.** It is the minimum-viable-mass finding arriving with a number
attached: 4,590 words against DoL's seed of 116,540 across 25 locations. To pass, this game needs to
be roughly **seven times larger**.

It is the honest state of a slice built to test a review loop, and it is already written up as
`SKILL_CHANGES_OWED.md` §5. The two release-check failures are the same kind of thing: no media
(a testing-stage build by design) and not filed as published (0.0.1 is not being released).

---

# What this experiment actually proved

**The format works as a review surface and fails as a specification.**

LO read a game he could not play, changed it, and signed it off — and the sheets caught ten design
defects before a line of TOML existed. That half is proved.

But **ten of the format's gaps were only visible once something ran.** The unit its headline number
is measured in does not survive translation; the map can be right room-by-room and wrong as a whole;
a deferral can sit where a gate is; and a mandatory-sounding rule can be written with no mechanism
under it.

**Every one of those is fixable in the format, and none of them was visible from inside it.**
