# vesper_two — the guidance page is empty in the build

**Written 2026-09-03. A findings-and-proposal document. Nothing has been changed.**

---

## 1 · The defect

`setup.quests_cards = []` in `games/vesper_two/output/index.html`.

**All twelve quest cards are absent from the built game.** The guidance page renders its heading
and nothing else. Not eleven mute cards — zero cards.

### Proof

| check | result |
|---|---|
| card text `"Ten coin a night"` in `0_systems_spec.toml` | present (line 181) |
| same text in the merged `7_final_game.toml` | present |
| same text in `output/index.html` | **0 occurrences** |
| `setup.quests_cards` in the build | **`[]`** |
| build timestamp vs source timestamp | 22:02 vs 21:48 — **the build is newer, so it is not stale** |
| control: `orientation`'s card text in `orientation`'s build | **4 occurrences**, `setup.quests_cards` populated |

The mechanism works. The problem is this game's TOML.

---

## 2 · The cause

Every card is written with the **canvas** condition form:

```toml
[[quest_cards]]
id   = "card_cover"
text = "The Spire reads what she is wearing before it reads anything else."
tip  = "The wardrobe is at the berth."
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait = "cover", op = "gte", value = 5 },
] }
```

A quest card does not read `conditions`. It reads a bare **`when`** array.
`_parse_quests_card` (`apps/projects/services/template_import.py:1187-1216`) reads `d.get("when")`
and `d.get("goals")` and nothing else.

So on every one of the twelve cards:

- **`conditions` is silently dropped** → the card imports with `when = []`
- **`id` is silently dropped** → not a field on the `QuestsCard` dataclass at all
  (`template_import.py:1109-1152`)

And a card with no `when` does not survive to the build.

> This is the trap `the-voice.md` R2 already warns about — *"a quest card is NOT a canvas condition
> and the two forms are different"* — applied to the entire guidance surface at once.

---

## 3 · Why nothing caught it

```
guidance exists                        PASS — "12 quest cards for 3 ascent tiers and 7 characters"
the guidance page says nothing (new)   11/12 cards render no requirement
--release · every canvas is a passage  PASS — 79/79 canvases reached the build
```

**All three read the SOURCE. None asks whether a card reached the ARTEFACT.** `--release` has a
check for canvases and no equivalent for cards.

Yesterday's new lint was correct that the page says nothing, but for a larger reason than it could
see: it was describing cards that do not exist in the game.

This is `defects/001` recurring — *"gates parse the source and reachability is decided at build
time."*

---

## 4 · Two side-findings, recorded so nobody "fixes" them

- **`type` on a condition item is inert.** `_parse_quests_condition`
  (`template_import.py:1155-1183`) reads `flag`, `trait`, `subject`, `npc_id`, `op`, `value`,
  `label`. It never reads `type`. `orientation` writes `type = "trait"`; `the-voice.md` R2 omits
  it. **Both are correct.** Do not go and make one match the other.
- **`id` on a quest card does nothing.** All twelve carry one. Harmless, but misleading — it looks
  like the card has a handle and it does not.

---

## 5 · Proposed repair — the game

Rewrite all twelve in `games/vesper_two/toml_phases/0_systems_spec.toml`, lines 181–278:
`conditions` → `when`, drop `id`, and add goals.

**What is available to point a goal at** (all verified present in this game):

- **tiers** — `cover` (sidebar bands 0/5/10/15/20; top authored gate 20) · `service`
  (0/10/20/30/40; gates up to 45) · `drain` (0/5/10/15/20; gates up to 100)
- **per-NPC** — `relation` on all seven; `arousal` additionally on Renner
- **arc flags** — `kess_open`, `renner_open`, `bastien_open`, `calloway_open`, `colm_open`,
  `marsh_open`, `mercer_open`, and the deeper ones (`renner_alone_known`, `calloway_believed`,
  `bastien_reading`, `marsh_slot`, `colm_talks`, `has_the_file`, `seated_1`/`seated_3`)
- **hubs to point `ready_canvas` at** — `hub_kess`, `hub_renner`, `hub_bastien`, `hub_calloway`,
  `hub_colm`, `hub_marsh`, `hub_mercer`

⚠️ **Do not write a `cover` goal above 20.** `0_systems_spec.toml:82-83` says cover was banded to
20 deliberately as *"what v0.1 REACHES"*. A goal above it promises a climb this release does not
contain.

⚠️ **Daily-cap flags are not goals** — `bench_used_today`, `bar_shift_today`, `haul_done_today`
and the rest are cleared every night in `[engine.daily_tick]`.

### The proposed cards

Wording follows `the-voice.md` R3: **a place, a person where there is one, and a verb** — and the
hours, since every character here is schedule-gated.

**The three tier ladders** (`when` = a band, `goals` = the next rung; the engine prints
`label — current / target` itself for a trait goal):

| card | when | goal label |
|---|---|---|
| cover | `cover lt 5` | "Wear what the Spire reads — the wardrobe at the berth" |
| cover | `cover gte 5, lt 10` | "Walk the plaza in it" |
| cover | `cover gte 10, lt 20` | "Let the Spire read you at the door" |
| service | `service lt 10` | "Take a shift on the Undertow's floor, after dark" |
| service | `service gte 10, lt 20` | "Let the back room be the room" |
| service | `service gte 20, lt 40` | "Pick the man and the hour yourself" |
| drain | `drain lt 5` | "Get something seated — Kess's bench, ten to ten" |
| drain | `drain gte 5, lt 20` | "Take it off him while he is still talking" |

**The seven characters** — each gated on having met them, each goal a flag their content sets:

| npc | when | goal label | ready_canvas |
|---|---|---|---|
| Kess | `met_kess` | "Ask Kess to seat one — the berth, ten to ten" | `hub_kess` |
| Renner | `met_renner` | "Stay past five, when the crew has gone — the depot" | `hub_renner` |
| Bastien | `met_bastien` | "Let him search you and read him back — behind the Undertow, after eight" | `hub_bastien` |
| Calloway | `met_calloway` | "Give him something to believe — Vance Securities, before the auditors go at six" | `hub_calloway` |
| Colm | `met_colm` | "Keep him drinking until he answers — the end of the bar, after nine" | `hub_colm` |
| Marsh | `met_marsh` | "Take the Sunday slot that belongs to somebody else — the House, evening" | `hub_marsh` |
| Mercer | `met_mercer` | "Be somewhere he did not put you — the stall under the dock road, after dark" | `hub_mercer` |

**The wall card** stays `terminal = true` — it is the one card that is legitimately goal-less, and
it is why the lint is a lint.

⚠️ Every goal label above is a **proposal**, not a decision. They are written from what the game's
own conditions already gate on, but which rung is a character's *next* one is a design call and
should be read before it is built.

### The four traps that break this rewrite

1. **An inline table may not span lines.** The `when` array wraps because an array can; each
   `{ … }` must be whole on one line or the build stops at a parse error.
2. **`ne` is silently unsupported on cards** — `setup.checkQuestsCondition` has no `ne` case and
   falls through to `return false`. The card never matches and the row goes blank.
3. **`gte X` + `lt Y` on every rung**, so exactly one matches. `lt`-only makes the card vanish once
   passed; `gte`-only matches every rung at once and priority silently decides which shows.
4. **`group` and `npc_id` do not go together** — `group` is ignored on an NPC card.

---

## 6 · Proposed repair — the skill

**Add one check to `gates.py --release`: every quest card in the source reached the build.**

The existing `every canvas is a passage` proves the shape works and where it goes. Without it,
the next game writes `conditions` on a card and nobody finds out for a month.

The test from `CLAUDE.md` — *"would a correct author-game skill have prevented this?"* — is **yes**:
the wrong dialect is documented in `the-voice.md` R2 and nothing enforces it against the artefact.
So fixing only the game leaves the trap armed.

⚠️ **This is a skill change and the approved plan put skill changes out of scope.** Recorded here
as a recommendation, not done.

---

## 7 · Verification, once repaired

```
python3 scripts/merge_toml_phases.py games/vesper_two
python3 manage.py package_from_toml --file games/vesper_two/toml_phases/7_final_game.toml \
        --output games/vesper_two/output --gen-version v2
```

1. `setup.quests_cards` in the build is **non-empty and holds twelve entries** — this is the check
   that actually matters and the one nothing currently performs.
2. `gates.py vesper_two` — lint `the guidance page says nothing` silent; gate
   `a goal says what it wants` moves from **n/a to PASS** with a real denominator.
3. Tally does not drop from its baseline of **41/44 judged, 6 n/a**.
4. Open the built game's guidance page and read one character's card: the `🎯 To advance` block
   renders, and a trait goal shows `label — current / target`.
