# The trait catalog — every built-in trait's range, default, decay, sidebar render

Read this when you declare `[player.core_traits]` / `[[npcs.core_traits]]`, raise/gate a trait, or put a
stat on the sidebar — it's the DATA layer (names, ranges, defaults, bands, decay, which sidebar primitive
renders what). For the DESIGN decision — *which* trait drives a given NPC arc by shape — see
`references/trait-design.md`. This file does NOT decide the spine; it tells you what each trait IS.

**Every fact here is verified against live engine code** (`v2.py` = the comprehensive generator;
`template_import.py` = the importer/validator), cited `file:line`. Where the engine and the old corpus
disagreed, the **code wins** and the divergence is flagged inline.

## Contents
- §1 — The headline: the engine ships NUMBERS, you author the WORDS
- §2 — Player traits (table) + per-trait notes
- §3 — Per-NPC traits (table) + arousal-as-throttle
- §4 — Body-state spec (`energy` / `hygiene`)
- §5 — Encode-by-type sidebar mapping + the doubling trap
- §6 — Pointers (don't duplicate)

---

## §1 — The headline: the engine ships NUMBERS, you author the WORDS

The engine has **no hardcoded trait list, no hardcoded defaults, and no hardcoded band names.** Two
consequences that the old corpus draft got wrong — the code is the source of truth:

- **No trait exists until you declare it.** All defaults (`corruption = 0`, `energy = 100`, …) come
  from the game's `[player.core_traits]` / `[[npcs]].core_traits` TOML, read verbatim at import
  (`template_import.py:1537`, `:1601`) and state-init (`v2.py` reads `pc.core_traits or {}`). The
  "always-on" set below is a *convention*, not an engine constant — you still type every line.
- **No daily passive is hardcoded.** The arousal "+1/day climb" and the `energy`/`hygiene` daily decay
  are NOT in the engine. `advanceDay` just iterates whatever you put in `[engine.daily_tick].traitEffects`
  and applies it through the normal effect path (`v2.py:5255-5275`, `daily_tick.traitEffects` loop → `applyAndNotifyTrait`). *(Code-vs-lore note: older drafts
  claimed a "hardcoded daily climb" for family NPCs. The engine hardcodes nothing — if you want the
  climb, you author the tick. If you want a slow burn, you simply don't.)*
- **No band names are hardcoded.** "Pure / Lewd / Slutty / Whore" is NOT in the engine. What the engine
  ships for corruption is (a) a raw 0–100 number and (b) a derived discrete **level 0–4** from tier
  thresholds `[0, 5, 15, 30, 45]` (`getCorruptionLevel`, `v2.py:5622-5628`; override via
  `[engine].corruption_tiers`, parsed at `template_import.py:2543-2545`, read by the generator at
  `v2.py:1060-1061` (`self.corruption_tiers` metadata read)). The *word* bands you see on the
  sidebar are author-supplied `bands` on a `trait_words` item (each `{min, max, text}`), matched at
  `v2.py:15362-15379` (`trait_words` band-match loop). *(Code-vs-lore note: older drafts presented Pure 0–24 / Lewd 25–49 / Slutty 50–74 /
  Whore 75–100 as canonical. The 0–100 range is real and a fine 4-band scheme, but those exact boundaries
  are your authored choice, not an engine fact — and they don't line up with the engine's `corruption_level`
  tiers `[0,5,15,30,45]`. If a gate uses `corruption_level`, band your `trait_words` on the SAME tier
  boundaries so the word the player reads matches the level the gate checks.)*

So: the engine is a generic numeric-trait + author-supplied-band machine. The tables below are the
**recommended canon** (RTS-shape default), not engine validation — except the one hard rule:

> **Declare every trait before use** or it's a silent no-op gate / hard sidebar fail. Engine ground-truth
> and grep guards: `references/toml-gotchas.md` "Declare every trait BEFORE use". (Sidebar undeclared-trait
> error: `template_import.py:3149-3152`.)

---

## §2 — Player traits

| Trait | Range | Default | Decay / daily passive | Sidebar primitive | Tier |
|---|---|---|---|---|---|
| `corruption` | 0–100 int | 0 | **None** — one-way climb, never decays | `trait_words` (author bands) | 1 — always on |
| `arousal` | 0–10 int | 0 | **None** (no decay). Optional `+1/day` IF you author the tick. Reset to 0 at climax (author-emitted) | `trait_bar` + `bands` + `hide_value=true` | 1 — always on |
| `energy` | 0–100 int | 100 | Spent per action (via `costs`); restored by sleep. Daily passive only if you author it | `trait_status_text` (author bands) | 1 — always on |
| `hygiene` | 0–100 int | 100 | `-N/day` IF you author the tick; restored by shower | `trait_status_text` (author bands) | 1 — always on |
| `money` | int ≥ 0 (no cap) | varies by setting | Rent / purchases (authored); no passive | `trait_bar` as a NUMBER — `hide_value=false`, NO bands (§5) | 1 — always on |
| `exhibitionism` | 0–100 int | 0 | None | `trait_bar` or `trait_words` (if banded) | 2 — optional |
| `fitness` | 0–100 int | 0 | None (progression, never decays) | `trait_bar` if a gym mechanic exists, else hide | 2 — optional |
| `intelligence` (alias `intel`) | 0–100 int | 0 | None | `trait_bar` if a school mechanic exists, else hide | 2 — optional |

**`corruption` (player)** — the global depravity odometer; the cross-arc content-tier currency. One-way:
no engine decay, and *declining* a taboo action neither adds nor subtracts it (the gated-action toast is a
UI hint, not a mutator — `showEffectNotification`, `v2.py:5654+`). It is the **global** tier, NOT a per-NPC
relationship clock — gating a specific NPC's milestone *only* on player corruption while that NPC's own
built axis goes unread is the corruption-as-universal-spine bug (`references/trait-design.md`). Locked to
0–100, 4 bands by convention; author the bands on the same boundaries your `corruption_level` gates use.

**`arousal` (player)** — a **THROTTLE**, not an odometer: the per-attempt fuel that gates *when* she can act
(must be `> 0` to masturbate; cascade/lewd-menu thresholds), never long-term progression. Climbs from lewd
beats (+1/beat) and optionally +1/day if you author the tick; **resets to 0 only at climax, and only because
you emit it** — `{ targetType = "player", trait = "arousal", op = "set", value = 0 }` on the climax canvas's
exit. There is **no engine macro that auto-zeroes it** (no `FinishSex`/`FinishMasturbation` — searched, none
exist in `v2.py`). Forget the reset and arousal sticks at max forever. Because it resets, it must NEVER gate
a one-shot capstone (`references/trait-design.md` "Throttle vs odometer").

**`money` (player)** — a countable resource: economic pressure (rent, shop, job income), integer ≥ 0, no cap.
Don't band it — it stays a number (see §5).

**`exhibitionism` / `fitness` / `intelligence`** — Tier-2 optional player axes. Declare only when the premise
uses the mechanic (`exhibitionism` for public/display/bar/club premises — gate the public floor on it;
`fitness` for a gym arc; `intelligence` for a school arc). All one-way (no decay). An optional axis that
climbs but gates nothing is a dead meter — cut it or wire the gate (`references/trait-design.md`).

---

## §3 — Per-NPC traits

NPC traits live in each `[[npcs]]` block's own `core_traits` table (same declare-before-use rule).

| Trait | Range | Default | Decay / daily passive | Notes |
|---|---|---|---|---|
| `relation` | 0–100 int | 0 | **None** (one-way; specific negative beats may `-N`, daily tick must NOT) | The bond — courtship/trust ODOMETER. Single canonical name across all arc shapes. |
| `corruption` | 0–50+ int (varies by arc depth) | 0 | **None** — one-way climb | His willingness ceiling — the per-NPC ODOMETER. The family-arc spine. |
| `arousal` | 0–3 int | 0 | **None** (no decay). Optional `+1/day` IF you author the tick | His wanting-*now* — a THROTTLE (resets at climax, author-emitted, two effects: player AND npc). |

**`relation`** — the courtship/commitment odometer; the workhorse for peer/dating + service. High-relation +
low-corruption = chaste mentor; high-corruption + low-relation = FWB. The three NPC axes are **independent**;
don't conflate them.

**`arousal` (NPC) — a throttle, default `+1/day` for in-scope/family NPCs (if you wire it).** The willingness
*warm-up* axis for **family/ambient, slow-burn, and escalation** arcs only. Range 0–3 (RTS-faithful — a
`+5` overflows it and breaks stage gating). **Peer/dating, service, and antagonist NPCs do NOT track arousal**
(peer/service are relation-spined; antagonists use a hidden `awareness` accumulator) — an arousal meter on a
relation-spined NPC is a dead meter. **The "+1/day for in-scope family NPCs" is a *deliberate authoring choice*,
not an engine behavior** — you put it in `[engine.daily_tick].traitEffects` (`cap = 3`). For a **slow burn**
you deliberately DEVIATE: omit the passive climb and make the willingness *earned* from arc beats
(daily-capped raises on charged moments), so the burn stays player-paced. Flag that deviation in the NPC's design
brief. (Reset at climax is author-emitted for BOTH player and npc — no engine macro zeroes either.)

**`<slug>_stage`** — the per-NPC arc milestone is NOT an NPC trait. It's stored as a **player** trait keyed by
slug (`player.core_traits.<slug>_stage`, integer), advanced by `op = "set"` only (never `add`), and the engine
special-cases it: `applyAndNotifyTrait` matches `/^([a-z_]+)_stage$/` and writes
`game_state.stage_advancement_log[slug]` on an upward delta (`v2.py:5549-5554`). **INTERNAL-ONLY — never
surfaces to any sidebar or player-facing text.** Full storage/mutation contract: `references/toml-gotchas.md`
(stage-trait mutation uses the PLAYER namespace).

---

## §4 — Body-state spec (`energy` / `hygiene`)

Both are 0–100, default 100, and are the body-need axes — they DECAY and RESTORE (unlike the one-way odometers).

- **`energy`** — capacity to act. **Spend it through `costs`, not `effects`** — an `effects` deduction moves
  the number but gates nothing (cosmetic bar); `costs` both gates *and* deducts (`references/toml-gotchas.md`
  "Resource gating"). Restore via a sleep/nap activity (`effects { op = "add", value = +N, cap = 100 }` — cap it;
  `energy` is banded, so an unclamped restore past 100 vanishes the card, see §4 clamp rule above). No engine daily
  decay — sleep is the loop. Energy is the wrong **primary gate** for an NPC's escalation ("too tired to flirt"
  is bad fiction — the lock is the corruption/relation trait); gate chores/activities with it. **But** a per-rung
  `costs` energy spend is a legitimate *throttle* on a repeatable charged rung when the fiction supports it (a
  machine powered by charge, a stamina economy) — see the throttle menu, `references/trait-design.md` "Slow-burn
  pacing".
- **`hygiene`** — cleanliness. Daily decay only if you author it in `[engine.daily_tick].traitEffects`
  (`value = -N`); restore via shower. A **soft modifier** on NPC-interaction quality — it COLORS scenes
  (low-hygiene prose variants, an occasional "go shower" reaction), it does **not** hard-gate an arc. Block at
  most one specific high-stakes scene; never the whole arc. Its real job is to *pull the player to the shower*
  — and that shower is a Lane 3 hijack host (`references/lanes.md`), so the decay loop is what delivers the
  player into catchable self-care. Energy + hygiene MUST surface (the player needs to know when to sleep/shower).

`op` is `add` (negative value = decay; there is **no `sub` op**) or `set`. **Effects are UNBOUNDED by default —
you opt IN to bounding.** The effect path passes `eff.clamp || false`, so an `op=add` that omits `clamp` applies
the raw delta with no 0–100 bound (the "Clamp trap" — full mechanism in `references/engine-reference.md`). That is
correct for the *value* of a one-way climber: `money` (no cap) or a `corruption` odometer meant to pass its
nominal top.

**But a *banded* stat must never leave its bands, or its sidebar card silently VANISHES.** The band only draws
when the value lands inside one — `trait_words` matches a **closed** `[min, max]` (`v2.py:15371`, `_twBand.min`/`.max` closed match);
`trait_status_text` treats an omitted `min`/`max` as **open** (∓1e9, `v2.py:15302`, `_bMin`/`_bMax` default). A value outside every band
renders **nothing** — for a text card (`trait_words` / `trait_status_text`) the whole card disappears (§5), which
reads as a *missing HUD element*, not a wrong number, so a quick playtest sails past it. Guarantee a match two ways:
- **Bound the value** — every `op=add` on a bounded body-need/resource stat (`energy` · `hygiene` · a custom
  `charge`/`coin`) carries **`clamp = true`** (a drop that could pass 0) or **`cap = N`** (a restore that could
  pass its ceiling). Clamp/cap math lives in `_traitClamp` / `applyAndNotifyTrait` (mechanism in
  `references/engine-reference.md`); `costs` deductions already floor at 0. *(This shipped broken twice in Vesper — Charge went negative, Condition over-capped; both
  cards vanished.)*
- **Cover the whole range** — a one-way odometer (`corruption`) whose *value* climbs unbounded still needs its top
  band to cover wherever it lands: `trait_status_text` can omit the top `max` (open top); `trait_words` needs an
  explicit high `max` (or `cap` the terminal add), or the word vanishes past the top band.

*(All of the above governs whether the HUD **draws**. Whether the climb still **buys** anything is a
different question, asked at ship time — `references/ship-gate.md` §1: widening a top band so the card keeps
rendering can *hide* a bar that fills past its last authored gate. Both apply; `cap` the terminal add and
you satisfy each.)*

---

## §5 — Encode-by-type sidebar mapping (and the doubling trap)

A surfaced stat is *upgraded* by choosing the sidebar primitive that matches what the number MEANS. The
auto-numbered Traits dump already prints every declared `core_trait` as a number, so a band is the upgrade —
but only if you suppress the auto number, or it prints twice.

| Stat KIND | Example | Sidebar type | Why | Verified |
|---|---|---|---|---|
| **Identity / qualitative state** | `corruption` | `trait_words` + author `bands` | The player thinks in a word ("Slutty"), not a number — a one-way identity ladder | `v2.py:15350-15385` |
| **Transient mood** | `arousal` | `trait_bar` + `bands` + `hide_value=true` | A dial that climbs and resets — show the heat band/glyph, hide the volatile raw number | `v2.py:15240-15286` (`hide_value`, `bands`) |
| **Body-need** | `energy`, `hygiene` | `trait_status_text` + author `bands` | Passive banded body-state; renders **nothing** when the value leaves its bands — clamp/cap every `op=add` (§4 clamp rule) or the card silently vanishes | `v2.py:15287-15315` (`trait_status_text` render) |
| **Countable resource** | `money` | `trait_bar`, `hide_value=false`, **NO `bands`** | You want the exact figure ($80), not a word — don't band a thing the player counts | `v2.py:15240-15277` (`trait_bar` number render) |

There is **no dedicated number/money sidebar type** — a plain resource renders through `trait_bar` with
`hide_value` false and no bands (it shows `Label: N / max`). *(Code-vs-lore note: older drafts implied a
"Numeric display" primitive; none exists — money is a `trait_bar`.)* Per-NPC variants set `trait_owner = "npc"`
+ `npc_id`; for the RTS House card use `npc_panel` (`references/hud.md`).

**The doubling trap.** `trait_words` / `trait_bar` / `trait_status_text` read the trait DIRECTLY and do NOT
consult `setup.hiddenTraits` — so the band always renders. But the **auto Traits dump** (and the Stats page)
print EVERY non-hidden `core_trait` as a number. So a stat you band ALSO appears as a raw number in the dump —
it shows **twice**. Suppress the auto number with a hide-only label so the banded stat shows once (as the band):

```toml
[[traits.labels]]
key    = "corruption"
hidden = true   # drops the auto-dump number; the trait_words band still renders
```

This is safe precisely because the band renderers ignore `hiddenTraits` (`v2.py:15240` `trait_bar`, `:15350` `trait_words`) while the
dump loops honor it. Band a stat ⇒ hide the same key. *(Side effect: a hidden key is also dropped from the dev
+/- panel — fine for ship builds.)* `<slug>_stage` and antagonist `awareness` are hidden by the same mechanism
(they must never surface at all).

**One cross-panel catch.** `hiddenTraits` matches by **bare global name**, and the `npc_panel` arousal/corruption
rows check the SAME global key (`v2.py:15424` / `:15437`, `hiddenTraits.includes`) — so hiding the *player's* banded `corruption`/`arousal`
to kill the doubling trap ALSO blanks that row on **every NPC House card**. If you surface `npc_panel`
corruption/arousal rows, read `references/hud.md` §5 for the workaround before you band-and-hide the colliding key.

---

## §6 — Pointers (don't duplicate)

- **Declare-before-use, grep guards, the field-name reference card (effect `targetType/trait/op` vs predicate
  `subject/trait_key/operator`), `version = "1.0"` on every conditions block, stage mutation on the player
  namespace, `costs`-not-`effects` resource gating** → `references/toml-gotchas.md`.
- **Which trait drives which arc (the spine by shape), throttle-vs-odometer, the dead-meter anti-pattern,
  slow-burn earned-willingness** → `references/trait-design.md`.
- **The per-arc-shape sidebar VISIBILITY table (which NPC surfaces which axis) + the `npc_panel` rendering
  model (`rows = ["arousal","corruption","location","next"]`, validated at `template_import.py:3373`)** →
  `references/hud.md`.
