# 37 — Worn-Clothing-Stats Engine PRD (`beauty` / `corruption` + `worn_*` predicates)

> **Status:** PRD — locked, ready to implement. No code changed by this doc. Implementation is a separate follow-up.
> **Session:** 2026-05-21 (Thursday), ~12:00 IST. Follows doc 36 (`36_RTS_Closet_vs_Engine_Wardrobe_and_Maya_Sketch.md`), which identified the gap. Anchors below were source-verified this session via two parallel Explore passes + direct reads that resolved a contradiction between them.
> **Goal:** Let garments carry `beauty` + `corruption` stats, and let scenes/choices route on *how revealing the worn outfit is* — the one RTS closet capability the engine lacks today.
> **Method:** Read `apps/game_generation/twee_comprehensive/generators/v1.py` + `v2.py`, `apps/projects/services/template_import.py`, `prompts/COMPREHENSIVE_SYSTEM_REFERENCE.md`, `apps/projects/tests.py`.
>
> **Decisions locked (user):**
> - **Aggregate = MAX** — worn beauty/corruption = the highest single equipped garment's value (RTS-faithful: the sluttiest piece drives content; no layering inflation).
> - **Sidebar deferred** — this PRD is fields + aggregates + predicates + formatter + docs + tests. A sidebar readout of worn stats (doc 36 gap #5) is a separate follow-up (no computed-value sidebar item type exists yet).

---

## §1 Goal & non-goals

**Goal.** A clothing item may declare numeric `beauty` and `corruption`. Two new v1.0-condition predicates — `worn_beauty` and `worn_corruption` — let any canvas trigger, choice, or location rule gate on the **MAX** stat across what the player is currently wearing. This reproduces RTS's "wearing something daring opens content" on top of the engine's existing slot-based wardrobe.

**Non-goals (explicit).**
- **Sidebar readout** of worn stats — deferred to a follow-up.
- **`trait_checks` support** — the hint-template condition schema (`template_import.py:3099–3140`, E14) is a *separate*, allowlisted system (`trait`/`flag` only). Worn-stat hints are not needed; not touched here.
- **RTS `.type` routing** — slot/item presence checks (`clothing_slot`/`clothing_item`) already cover "is she in swimwear"; no `type` field is added.
- **Portrait-from-equipped** rendering — separate art track.
- **Any automatic coupling to the global `corruption` core_trait** — see §2.

---

## §2 Doctrine — worn corruption is a SEPARATE axis

Worn corruption **routes** content; it never mutates the player's global `corruption` core_trait. The global meter stays the progression spine (it gates the shop tiers and, in TLS, the Frank catch ≥25 / first-night / crack). Dressing daring opens *parallel, reversible* content without inflating the spine.

This preserves the shipped Frank economy (`[[frank_economy_rts_math]]`) untouched, and matches RTS live-verified fact #3 (doc 36 §3): wearing a corruption-30 garment left RTS's global `corruption.points` at 0. If a game ever *wants* sustained slutty-wear to nudge the global meter, that is a deliberate, separate `daily_tick` rule — never an automatic side effect of equipping.

---

## §3 Schema change — `apps/projects/services/template_import.py` (3 edits)

The v1.0 `conditions` path has **no import-time type allowlist** (see §5), and clothing-item parsing uses selective field extraction (unknown TOML keys are silently dropped). So adding two fields is purely additive and back-compatible (defaults `0`; existing clothing TOML unaffected).

**3.1 Dataclass** — `TemplateClothingItem` (`:152–160`), add two fields after `price`:
```python
    price: int = 0
    beauty: int = 0       # NEW — appearance contribution of this garment
    corruption: int = 0   # NEW — how revealing/lewd this garment is (content key)
```

**3.2 Parse loop** — the `[[clothing]]` reader (`:1484–1490`), add two extractions (`_require_int` already exists at `:761`):
```python
            price=int(c_raw.get("price", 0)),
            beauty=_require_int(c_raw, "beauty", 0),         # NEW
            corruption=_require_int(c_raw, "corruption", 0), # NEW
```

**3.3 Metadata emission** — the per-item dict that lands in `clothing_settings.items` (`:3990–4001`), add two keys:
```python
                "price": ci.price,
                "beauty": ci.beauty,         # NEW
                "corruption": ci.corruption, # NEW
```
This is the dict the generator reads via `clothing_settings.get("items", [])` (`v1.py:738`) and serializes to `setup.clothing_data` (`v1.py:763`/`:2129`) — so the new fields reach the runtime automatically.

---

## §4 Runtime aggregates — `v1.py` **and** `v2.py`

Add two helpers inside the existing `wardrobe_js_block` (the conditional JS string emitted only when `clothing_enabled`, `v1.py:977+`). Place them next to `setup.getWornBeauty`'s natural home — after `setup.getWardrobeItemsForSlot` (`:1031`).

**Correctness constraint (non-negotiable):** read stats from `setup.clothing_data` **by equipped item-id**, NOT from `sv.player.wardrobe[id]` or the equipped record. Reason: `initial_wardrobe`/`equipped` store only a 4-field subset (`id/name/slot/image`, `v1.py:754–759`) and `equipped[slot]` is just an item-id string — neither carries the new stats. `setup.clothing_data` is the single source of truth holding every field.

```javascript
// Worn-stat aggregates (MAX over equipped slots). Read from clothing_data
// by equipped id — equipped/wardrobe records do NOT carry beauty/corruption.
setup.getWornStatMax = function(field) {
    var sv = State.variables;
    if (!setup.clothing_enabled) return 0;
    var eq = (sv.player && sv.player.equipped) || {};
    var cdata = setup.clothing_data || [];
    var best = 0;
    for (var slot in eq) {
        if (!eq.hasOwnProperty(slot)) continue;
        var id = eq[slot];
        if (!id) continue;
        for (var i = 0; i < cdata.length; i++) {
            if (cdata[i].id === id) {
                var v = cdata[i][field] || 0;
                if (v > best) best = v;
                break;
            }
        }
    }
    return best;
};
setup.getWornBeauty = function() { return setup.getWornStatMax('beauty'); };
setup.getWornCorruption = function() { return setup.getWornStatMax('corruption'); };
```
Returns `0` when clothing is disabled or nothing relevant is equipped.

---

## §5 New predicates — `v1.py` **and** `v2.py` dispatch

`triggerConditionsSatisfied` (`:2823–3015`) is a plain if/else over `type`; unknown types fall through to `results.push(false)` (`:3014`). **No parser/allowlist change is needed** — the import pipeline does not validate v1.0 condition types. Insert two branches immediately after the `clothing_item` branch (`~:2972`), reusing the existing `compare(op, a, b)` helper (`:2780–2813`, supports `eq/ne/gt/gte/lt/lte`):

```javascript
            // worn_beauty / worn_corruption: gate on the MAX stat across the
            // equipped outfit. Routes content; does NOT touch global corruption.
            if (type === 'worn_beauty' || type === 'worn_corruption') {
                if (!setup.clothing_enabled) { results.push(false); continue; }
                var wornOp = it.operator || 'gte';
                var wornVal = it.value || 0;
                var wornCur = (type === 'worn_beauty')
                    ? setup.getWornBeauty()
                    : setup.getWornCorruption();
                satisfied = compare(wornOp, wornCur, wornVal);
                results.push(satisfied);
                continue;
            }
```

**Condition shape (authoring):**
```toml
{ type = "worn_corruption", operator = "gte", value = 30 }
{ type = "worn_beauty",     operator = "gte", value = 4  }
```
Works anywhere v1.0 conditions are honored: canvas `trigger.conditions`, choice `conditions`, and per-location `clothing_rules[].conditions`.

---

## §6 Condition formatter — `v1.py` **and** `v2.py`

Extend `setup.formatCanvasConditions` (`v1.py:6307–6402`, v2 `:6454–6548`) so gated/locked content reads naturally. Add after the `clothing_item` branch (`~:6377`):

```javascript
            else if (item.type === "worn_corruption") {
                var wcOp = item.operator || "gte";
                var wcVal = item.value || 0;
                parts.push("Outfit must be revealing (corruption " + _opSym(wcOp) + " " + wcVal + ")");
            }
            else if (item.type === "worn_beauty") {
                var wbOp = item.operator || "gte";
                var wbVal = item.value || 0;
                parts.push("Appearance " + _opSym(wbOp) + " " + wbVal);
            }
```
Where `_opSym` maps `gte→≥, gt→>, lte→≤, lt→<, eq→=` (inline a small switch if no helper exists). Player-facing, no mechanical jargon — consistent with `[[feedback_hint_narrative_no_time_or_location]]`.

---

## §7 Docs — `prompts/COMPREHENSIVE_SYSTEM_REFERENCE.md`

1. **Clothing section** (~`:1264–1287`): document the `beauty` + `corruption` item fields, that they're optional (default 0), and the **MAX** worn-aggregate semantics + the separate-axis doctrine (§2).
2. **Conditions schema** (~`:4244–4278`): add `worn_beauty` / `worn_corruption` entries with `operator` + `value`, alongside the existing condition types.
3. **Stale-comment fix** (~`:4568`): the note "ONLY flag, trait, days_since_flag" is already wrong (the runtime supports `clothing_slot/clothing_item/pass/item/stage`). Correct it to list the full live set + the two new types.

---

## §8 Tests — `apps/projects/tests.py`

Use the established `EnginePRDIntegrationTests` pattern (`_build()` `:331–354`): deep-copy a fixture dict, mutate it, run `create_project_from_template` → `TweeComprehensiveGeneratorV1().generate(project)`, and `assertIn` against the generated twee **string** (these are static-emission tests; they don't execute JS).

Add a test class/methods that:
1. Build with `clothing_enabled=true` + ≥2 items (one carrying `corruption`/`beauty`) + a canvas gated on `{ type = "worn_corruption", operator = "gte", value = 30 }`. Assert the output contains `setup.getWornCorruption`, `setup.getWornBeauty`, and the `type === 'worn_corruption'` dispatch branch + the formatter string.
2. **Back-compat:** build with clothing disabled → assert those tokens are **absent** (all new JS lives inside `wardrobe_js_block`, guarded by `clothing_enabled`).
3. **Schema:** assert the metadata round-trips `beauty`/`corruption` on a parsed item (and that omitting them defaults to 0).

**Runtime truth** (does the gate actually fire when a corruption-30 garment is equipped?) is verified by **live-play** (twine-game-explorer), per project doctrine — documented in §9, not asserted as a unit test.

---

## §9 Verification (acceptance criteria)

1. **Build:** `package_from_toml` on a clothing-enabled fixture exits 0, `✓ Validation passed`, baseline cosmetic warnings only.
   ```
   python manage.py package_from_toml --file <clothing_fixture.toml> \
     --owner-id 15b35759-e67f-4bab-be10-5a27dd7ddc7a --output /tmp/worn_clothing --dev --debug
   ```
2. **Pytest:** at/above baseline (266 passed + 5 pre-existing fails + 1 skipped) with new tests green. Run `pytest apps/projects/tests.py apps/game_generation/tests.py -q`.
3. **Twee inspection:** helpers (`getWornBeauty`/`getWornCorruption`/`getWornStatMax`) + both dispatch branches + both formatter strings present when enabled; **absent** when disabled.
4. **v1/v2 parity:** the emitted new block is byte-identical between generators (diff the relevant region).
5. **Live-play (twine-game-explorer):** in a clothing-enabled build, equip a corruption-30 garment → a `worn_corruption gte 30` scene becomes available; unequip → it hides; and the global `corruption` core_trait is **unchanged** across equip/unequip (proves §2).

---

## §10 Risks & mitigations

| Risk | Mitigation |
|---|---|
| v1/v2 drift (edit one, forget the other) | Apply identical edits to both; acceptance criterion #4 byte-equality check. |
| Aggregate reads stale stats off the equipped/wardrobe subset | §4 forbids it — read from `setup.clothing_data` by id only. |
| MAX surprises authors expecting additive layering | Documented in §7 (MAX semantics stated); MAX was the locked decision. |
| Breaking clothing-disabled games | All new JS is inside `wardrobe_js_block`, guarded by `clothing_enabled`; predicates short-circuit to `false` when disabled; acceptance criterion #3 proves absence. |
| Author tries `worn_*` in a `trait_checks` (hint) block | Out of scope; that path still allowlists `trait`/`flag` and will error clearly at import (`:3107`). Note this in the docs. |

---

## §11 File touch-list (for the implementer)

| File | Edits |
|---|---|
| `apps/projects/services/template_import.py` | dataclass `:152–160`; parse `:1484–1490`; metadata emit `:3990–4001` |
| `apps/game_generation/twee_comprehensive/generators/v1.py` | aggregates after `:1031`; dispatch after `:2972`; formatter after `:6377` |
| `apps/game_generation/twee_comprehensive/generators/v2.py` | same three edits at the corresponding v2 offsets (byte-identical surface) |
| `prompts/COMPREHENSIVE_SYSTEM_REFERENCE.md` | clothing fields ~`:1264–1287`; conditions schema ~`:4244–4278`; stale-comment fix ~`:4568` |
| `apps/projects/tests.py` | new tests in `EnginePRDIntegrationTests` (`_build()` pattern) |

---

End of PRD.
