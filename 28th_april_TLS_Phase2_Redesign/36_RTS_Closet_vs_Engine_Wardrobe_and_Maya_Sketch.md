# 36 — RTS Closet vs. Engine Wardrobe + Maya Wardrobe Sketch

> **Status:** Analysis record + design sketch. No code changed by this doc. (The one code change this session — fixing the misleading "Corruption & Beauty" Tips-panel blurb in `7_final_game.toml` / `1_metadata_and_locations.toml` — is already shipped, rebuilt, and verified; it is *referenced* in §8, not redone here.) The §9 Maya sketch is **design-sketch depth, not a build PRD**.
> **Session:** 2026-05-21, ~10:00–12:00 IST (Thursday). Single conversation. Question chain: "does RTS have a wardrobe like our wardrobe?" → focused live twine-game-explorer closet session → engine wardrobe code audit → "is it enabled in TLS?" → tips-line fix → this consolidation doc.
> **Method:** RTS static artifacts in `game_explorations/rts-arc-trace/` (`passage_catalog.json` 361 passages source_raw, `variable_index.json` 131 vars) + a live twine-game-explorer session against `mopoga.com/road-to-success` (eval against `window.SugarCube.State.variables`, ran buy/equip and read function bodies). Engine read of `apps/game_generation/twee_comprehensive/generators/v1.py` + `v2.py` and `apps/projects/services/template_import.py`. Grep of `games/the_long_summer_test/toml_phases/`.

---

## §1 How the session got here

The conversation walked a deliberate ladder, each rung checked against source before the next:

1. Does RTS have a clothes-changing system like the engine's "wardrobe"? → yes, found `$clothes` + Wardrobe/ClothingStore in the captured artifacts.
2. Show its full functionality, how it works, how it affects gameplay. → static read + a focused live session to close the StoryJS gap.
3. In the game-gen engine we also have a "wardrobe" — do we support everything we learned from RTS? → full engine code audit.
4. Is it even enabled in TLS? → no (clothing disabled); but TLS has the scalar axes RTS uses, just not bolted to clothes.
5. Fix the Tips-panel line that claims a wardrobe that doesn't exist. → shipped + verified.
6. Consolidate all of it into one doc. → this file.

The point of the ladder: the comparison below is trustworthy because each claim was source-grounded (or live-verified) before being asserted.

---

## §2 RTS closet — what it is

RTS keeps **one catalog object** `$clothes` — 31 garments, each a flat record:

```
{ name, title, type, price, beauty, corruption, image, purchased, isDefault }
```

The **worn** outfit is a separate pointer, `$player.clothing` (its `.name` / `.type` / `.beauty` / `.corruption` / `.image`). The catalog is the closet; the pointer is what's on her body.

- **7 wearable categories** (the Wardrobe tabs): `underwear, casual, school, fitness, swim, uniform, costume` — plus a hidden `schoolCheerleader` type.
- Every garment carries **two stats**: `beauty` (0–6) and `corruption` (0–45), both scaling with price (100→600). E.g. `casual1` = beauty 1 / corr 0 / $100; `school5` = beauty 4 / corr 45 / $400; `swim6` = beauty 6 / corr 45.
- **Two screens, deliberately split:** `ClothingStore` (in the Mall — *buy*) and `Wardrobe` (reachable from Bedroom / ApartmentBedroom / SchoolGym / Beach — *equip what you own*). The grids loop `$clothes` filtered by `purchased` + category and render each through `<<ClothShop _clothing>>` / `<<Wardrobe _clothing>>` widgets.

---

## §3 RTS closet — the four live-verified behaviors

Read sites are catalogued statically, but the equip/buy logic lives in module-private JS (`ClothService.changeClothes` / `ClothService.buyCloth`, with `StatsService` / `CorruptionService` behind `getBeauty()` / `getCorruptionLevel()`). The closures aren't reachable as source, so I drove the live game and observed behavior (state via `window.SugarCube.State.variables` — bare `State` / `game()` are closure-scoped in the eval frame).

| # | Behavior | Verdict | Evidence |
|---|---|---|---|
| 1 | **Equipping is free + instant** | ✅ | default→naked left money / energy / time all unchanged. |
| 2 | **Buying = exact price, affordability-gated, no auto-equip** | ✅ | $100 buy: money 1000→900; affordability: money 50 vs $200 → no deduction, `purchased` stayed false; after buy, worn stayed `naked` (no auto-equip). |
| 3 | **Worn corruption is a SEPARATE axis** | ✅ | wearing `casual4` (corruption 30) → `worn_corruption = 30` but `corruption.points = 0`, `getCorruptionLevel() = 0`. Wearing slutty clothes does **not** raise the global corruption meter. |
| 4 | **`getBeauty()` = worn garment's beauty, non-cumulative** | ✅ | tracked `0 → 4 → 2` as I swapped Casual 4 then Casual 2 — replaces, never sums. |

(One harness artifact: `changeClothes` commits `$player.clothing` on the *next* render, so `getBeauty()` updated immediately while the `.name` field lagged one read. Not a game bug — confirmed with a settled read after forcing a passage render.)

---

## §4 RTS — how clothing drives gameplay (four mechanisms)

This is richer than dress-up. Worn clothing feeds gameplay four ways, none of which feed each other:

- **(a) Worn corruption gates lewd content** (`$player.clothing.corruption >= 15 / 30`): `ParkJog` flash event (≥15; predator button at ≥30), `BeachSunbathe` / `PoolSwim` attention branches (≥30), `Workout` sexy-media swap (≥30), `Library` → `_hasCorruptOutfit = corruption >= 30` unlocks Natasha's `PublicExhibitionism` quest, `ComputerClassEvent` → `TeacherSecretFetish` (≥30 + quest active).
- **(b) Worn `.type` routes content** (doc-35 variant-routing, keyed on an equippable state): `swim` → Beach challenges / `Marina`; `costume` → `VeronicaCostumeParty` (Saturday); `schoolCheerleader` → "Join Cheerleaders" / `Cheerleader`.
- **(c) `beauty` gates SOCIAL content** (`getBeauty() >= N`): `Club` ("out of place" + bouncer rejection if beauty <3), `ThomasPartyInvite` (needs ≥3), `StripClubInterview` (rejected at beauty ==0).
- **(d) Global corruption gates the *right* to leave home under-dressed**: Bedroom / ApartmentBedroom hallway buttons + the Wardrobe Return button block leaving while `naked` (needs `getCorruptionLevel() ≥ 3`) or `underwear` (≥2), with a "30+ Corruption Needed" toast.

Plus the **player portrait**: `StoryCaption` builds the image path from `$player.clothing.type + .image`, so every screen reflects what she's wearing.

**Doctrinal frame** (ties to doc 35, `[[rts_state_variant_authored_vs_mechanism]]`): clothing is a *player-controlled* persistent state that variant-routes content. It's a soft **corruption on-ramp** — buy a corrupt garment → wear it → cross a worn-corruption threshold → new content opens — without the global meter moving.

---

## §5 The game-gen engine wardrobe — what it generates today

The engine ships its own wardrobe (opt-in via `metadata.clothing_settings.enabled`). It is **a slot-based paper-doll, not RTS's single-outfit swap.**

**Slots & layering.** Seven slots — `bra, underwear, top, bottom, dress, legwear, shoes` (`VALID_CLOTHING_SLOTS`, `template_import.py:149`). Dress↔top/bottom mutex: equipping a dress clears top+bottom and vice-versa (`v1.py:1003-1009`).

**Item schema** (`TemplateClothingItem`, `template_import.py:152-160` — the *only* accepted fields):
```
id · name · slot · image · initial · conditions · price
```
**No `beauty` field. No per-item `corruption` field.** Grep of both generators: `beauty` appears **0 times**.

**Two screens.** `WardrobePage` (equip what you own, `setup.renderWardrobePage` `v1.py:1041`) and `ShopPage` (buy, behind `shop_location` + usually a story flag, `setup.renderShopPage` `v1.py:1269`).

**Shop tiers.** Basic / Cute / Bold / Daring at corruption `0 / 45 / 85 / 135` (`v1.py:1283-1302`). A tier locks if **global** `core_traits.corruption` is below threshold (`v1.py:1316`). The tier an item lands in is **derived** from its equip-condition (`setup.getCorruptionThreshold` reads the item's `corruption gte N` condition, `v1.py:1233-1242`), not stored on the item.

**Buy semantics** (`setup.buyItem` `v1.py:1244-1267`): `money < price → false`; exact deduction from `core_traits.money`; honors `item.conditions`; calls `addToWardrobe` only — **does not auto-equip**. (Matches RTS fact #2 to the letter.)

**Equip semantics** (`setup.equipItem` `v1.py:994-1012`): checks `item.conditions` (`triggerConditionsSatisfied`), sets the slot, handles the dress mutex. **Free** — no money / time / energy cost. (Matches RTS fact #1.)

**Content routing** — scenes branch on worn clothing via two condition predicates (`v1.py:2932-2972`):
- `clothing_slot` — slot `equipped` / `unequipped`.
- `clothing_item` — item `equipped` / `unequipped` / `owned` / `not_owned`.

This is **presence / identity-based, not scalar** — nothing reads a beauty or worn-corruption *number*.

**Location gating** (`setup.checkLocationClothing` `v1.py:1164-1204`): per-location `clothing_rules` (`slots_required` + `conditions` + `message`) block navigation if required slots are empty; first satisfied rule wins. Global safety nets in `setup.validateClothing` (`v1.py:1128`): `body_coverage` (top+bottom OR dress), `always_required`, and `conditional` (required-until-a-flag).

**Story gifts** — `wardrobeEffects` on a scene/choice can `add` (or add+equip) a garment, with a "👗 New item: X" toast (`v1.py:4588`, emission `v1.py:10680-10682` / `11265-11267`). This is RTS's NPC-gift pattern (SecretAdmirer→cute, OfficeHR→secretary).

**No sidebar outfit display** (grep for "Your Outfit" / outfit sidebar → empty). RTS shows "👗 Your Outfit"; the engine does not.

**v1/v2 parity.** Byte-identical on this surface — 132 wardrobe-token hits in each generator, 0 `beauty` in each. (v2 is the default fork; see `[[v2_engine_fork]]`.)

---

## §6 Side-by-side support matrix

| RTS fact / mechanism | Engine support | Notes |
|---|---|---|
| Equip is free + instant | ✅ Yes | `equipItem` sets the slot only, after condition check. |
| Buy = exact price + affordability-gated + no auto-equip | ✅ Yes, exact | `buyItem` matches RTS precisely. |
| Worn corruption is a separate content-driving axis | ⚠️ Different / inverted | Engine has **no worn-corruption stat**; instead global corruption gates the *shop tiers*. The relationship runs the opposite direction. |
| `beauty` = social key | ❌ Absent | No beauty stat, no `getBeauty()`, no beauty-gated social content anywhere. |
| Clothing routes content | ✅-ish | Yes via `clothing_slot` / `clothing_item`, but **identity-based, not scalar** (no "any outfit ≥30 corruption"). |
| Can't leave home under-dressed | ✅ Yes | Via per-location `clothing_rules`, but gates on **slot coverage**, not a corruption *level* (a rule's `conditions` *could* add a corruption check). |
| Worn `.type` routes content | ➖ Partial | No `type` field on items; approximate via specific-item or slot checks. |
| Player portrait reflects outfit | ❌ Not wired | No portrait-from-equipped rendering. |
| — | ➕ Engine extras | Layered slots + dress mutex; `owned` / `not_owned` predicate; `wardrobeEffects` story-gifts; corruption-tiered shop UI. |

---

## §7 What's missing (the gaps vs. RTS)

1. **No `beauty` stat / axis** anywhere → no "you look out of place / can't get the job / no party invite" social gating.
2. **No worn-`corruption` scalar on garments** → you can't express "any outfit with corruption ≥ 30 unlocks the flash event." Only per-item (`clothing_item equipped`) or per-slot (`clothing_slot top unequipped`) checks — manual, not a clean tier.
3. **Routing is inverted vs RTS.** In RTS the *clothes* carry corruption that opens content; in the engine, *global corruption* opens the *clothes* (shop tiers). The engine never made worn-corruption a content-driving axis of its own.
4. **No aggregate "what am I wearing" scalar** for scenes or social gates (no `getWornBeauty()` / `getWornCorruption()`).
5. **No sidebar outfit readout** (RTS surfaces it on every screen).

---

## §8 TLS today — the enabled check

**The clothing system is DISABLED in The Long Summer.** Zero matches for `clothing_enabled`, `clothing_settings`, `[[clothing]]`, `wardrobe_location`, `shop_location`, or `clothing_rules` in `games/the_long_summer_test/toml_phases/`. The engine default is `enabled = false`, and the Frank slice never turns it on — so `WardrobePage` / `ShopPage` / equip / buy are not generated for TLS.

**But TLS already has the scalar axes RTS uses** — just not bolted to clothes:

- `beauty` and `corruption` are real player `core_traits` (`beauty = 40, corruption = 22` at start, `1_metadata_and_locations.toml:94`).
- They gate content exactly like RTS's scalars, via trait conditions: Jake's arc keys off beauty (`beauty >= 50 OR jake_first_glance_noticed` for stage 1; a first-glance sub-branch fires when `beauty` crosses 40, `3_activities.toml:383-396`). Beauty rises from showers + sketching (capped 70–80, `3_activities.toml:125/171`); corruption from Frank escalation.

**The irony:** TLS has the scalars the engine wardrobe *lacks*; the engine wardrobe has the slot/shop machinery TLS *doesn't use*.

**Shipped this session — Tips-panel fix.** The "Corruption & Beauty" blurb (`7_final_game.toml:1007` + `1_metadata:629`) read *"Wardrobe upgrades push corruption up over time. Beauty rises with showers + better outfits"* — describing a clothing system that doesn't exist. Rewritten to: *"Beauty rises when Maya showers and sketches — it shapes how NPCs first notice her. Corruption climbs as she pushes things further with Frank. Both gate certain scene branches, so keep an eye on the sidebar."* Rebuilt + verified (old string 0 hits in compiled `index.html`, new string present).

---

## §9 Design sketch — Maya's wardrobe after closing the engine gaps

> **Depth:** design sketch, not a build PRD. A real implementation graduates to a numbered Engine PRD (like doc 25 / doc 34) with file paths, function signatures, and a test plan.

The engine already covers the *mechanical spine* RTS-faithfully — two-screen buy/equip, free instant equipping, exact-price affordability-gated purchases that don't auto-equip, corruption-tiered shop, story-gifted garments, clothing-aware scene routing + location gates. **Reuse all of it.** The sketch only adds the two scalar axes the engine lacks.

### Engine deltas assumed (the missing things, added)

1. **Item stats.** Add optional `beauty` (int) + `corruption` (int) numeric fields to `TemplateClothingItem` (`template_import.py:152`). Default 0; back-compatible (existing clothing TOML still parses).
2. **Worn aggregates.** Add `setup.getWornBeauty()` / `setup.getWornCorruption()` — sum the `beauty` / `corruption` of items currently in `equipped` across all slots. (RTS reads a single worn garment; a slot model naturally *sums*, which is the right generalization for layering.)
3. **Scalar predicates.** Add `worn_beauty` and `worn_corruption` condition types (`gte` / `lt` / `gt` / `lte`) to `triggerConditionsSatisfied` (`v1.py:2932` block) so scenes route on the scalar — the thing `clothing_item equipped` can only fake today.
4. **Optional sidebar outfit readout** — a `sidebar_item` showing current worn beauty / corruption (closes the RTS "👗 Your Outfit" gap; reuses the existing `sidebar_items` machinery).

### The key doctrinal choice (carry RTS fact #3)

**Keep worn-corruption a SEPARATE axis from Maya's global `corruption` core_trait.** Dressing slutty should *route* content (open Frank/Jake/Ryan branches) **without inflating the master meter.** Global `corruption` stays the spine that gates the catch (≥25) / first-night / crack. This preserves the Frank economy work (`[[frank_economy_rts_math]]`) untouched while letting outfits add a parallel, reversible content key. (If we ever *want* a small global bump from sustained slutty wear, that's a deliberate, separate `daily_tick` rule — not an automatic side-effect of equipping.)

### How it interlocks for Maya

- **Money sink** — buy at a town shop (e.g. a `loc_thrift_store` / mall), gated behind an unlock flag (Maya discovers it after settling in), reusing `shop_location` + the flag gate.
- **Global corruption gates the shelves** — the existing Basic/Cute/Bold/Daring tier-lock (already built) decides which garments she's even allowed to buy. Her corruption *spine* opens the *closet*.
- **Worn corruption = the content key** — Frank/Jake/Ryan ambient + tease branches gate on `worn_corruption gte N`. Wearing the daring top in the kitchen opens a Frank ambient that the modest top doesn't.
- **Worn beauty feeds the existing beauty arcs** — so showers/sketching **and** outfits both raise the number Jake's first-glance reads. Beauty becomes "grooming + presentation," not just grooming.

### Example TOML shapes (illustrative, not final)

A garment carrying both stats:
```toml
[[clothing]]
id = "sundress_short"
name = "Short Sundress"
slot = "dress"
price = 40
beauty = 3
corruption = 12
# shop tier still derived from this equip-condition:
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 45 },
]}
```

A scene that only fires when she's dressed daringly (the thing we can't express today):
```toml
conditions = { version = "1.0", logic = "AND", items = [
  { type = "worn_corruption", operator = "gte", value = 30 },
]}
```

A Frank kitchen ambient gated on the outfit, not the meter:
```toml
# fires only when Maya is in something revealing — routes content,
# does NOT touch player.corruption
conditions = { version = "1.0", logic = "AND", items = [
  { type = "worn_corruption", operator = "gte", value = 20 },
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
]}
```

### Scope / anti-scope

- **In:** two scalar fields, two aggregate helpers, two predicates, optional sidebar readout. Everything else reused.
- **Out (this sketch):** RTS's single-outfit model (keep the richer slot system), `.type` routing (slot/item checks + worn scalars cover it), player portrait-from-equipped (separate art track), any forced global-corruption coupling.
- **Not decided:** whether a Maya clothing arc is even worth authoring yet — that's a content-priority call, not an engine one. This sketch only ensures that *if* we want it, the engine gap is small and well-understood.

---

## §10 Confidence ladder + source artifacts

✅ **HIGH (live-verified or code-read this session):**
- The four RTS closet behaviors (§3) — observed live via eval.
- The engine wardrobe surface (§5) — read directly from `v1.py` / `v2.py` / `template_import.py` with file:line anchors.
- TLS clothing disabled + the scalar-trait reality (§8) — grep + TOML read.

🟡 **MED (consistent with source, not exhaustively sampled):**
- RTS content-gate read sites (§4) — ~30% catalog sample (Brother/Dad/Marcus-era, beach/club/park/library), consistent with docs 21/22.

❌ **NOT established:**
- RTS `getBeauty()` exact formula — `StatsService` is a module-private closure; behavior pinned empirically (worn garment's beauty, non-cumulative), source unread.
- Whether a future Maya clothing arc is actually desired — a content-priority decision, deliberately left open in §9.

**Source artifacts:**
- `game_explorations/rts-arc-trace/passage_catalog.json` (361 passages, source_raw) + `variable_index.json` (131 vars).
- Live session: `mopoga.com/road-to-success` via twine-game-explorer (`window.SugarCube.State.variables`, ran buy/equip + read `<<Wardrobe>>`/`<<ClothShop>>` macro handlers).
- `apps/game_generation/twee_comprehensive/generators/v1.py` + `v2.py`.
- `apps/projects/services/template_import.py`.
- `prompts/COMPREHENSIVE_SYSTEM_REFERENCE.md` §"CLOTHING/WARDROBE SYSTEM" (lines ~1247–1326).
- Memories: `[[rts_clothing_system]]`, `[[rts_state_variant_authored_vs_mechanism]]` (doc 35), `[[frank_economy_rts_math]]`, `[[v2_engine_fork]]`.

---

End of analysis record.
