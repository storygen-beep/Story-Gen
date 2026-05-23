# Doc 40 — Player Arousal Engine PRD (RTS-faithful)

**Date:** 2026-05-21
**Builds on:** doc 38 (RTS Arousal System), doc 39 (RTS vs TLS Arousal). Same lineage as doc 37 (Worn-Clothing PRD).
**Status:** ✅ SHIPPED 2026-05-21. Engine E-CORE (`daily_tick.traitEffects`) implemented in v1+v2+importer with 4 tests; full TLS adoption done (Maya 0–10 meter, Frank/Jake/Ryan rescaled to 0–3, decay deleted). Build clean / pytest 257 green. Memory: `tls_player_arousal.md`. (Original PRD text retained below; engine facts verified by code exploration with line anchors.)

---

## 1. Goal & fidelity definition

Make our engine able to reproduce the RTS arousal model **100%**. "RTS-faithful" means these five behaviors:

1. **Player owns an arousal meter** (Maya), separate from corruption.
2. **It accumulates** — +1 per lewd event Maya is in, **and** +1 automatically every in-game day.
3. **It never decays** — only resets to 0 at climax.
4. **It is a `>0` switch** — at 0, Maya cannot start lewd self-actions ("not aroused enough"); above 0 those actions unlock.
5. **NPC arousal is a low-cap ladder** (0–3) that **rises daily** and pairs with corruption to gate escalation; climax zeroes the participating NPC too.

The headline finding: **almost all of this already works with existing engine primitives.** The only hard gap is behavior #2's *daily auto-rise*. Everything else is reuse + content authoring.

---

## 2. Gap table

| RTS behavior | Status in our engine | Evidence |
|---|---|---|
| Player arousal as a stat | ✅ Already works — add `arousal` to `player.core_traits` | init v2.py ~546 / ~4557; read like `corruption` |
| `>0` gate on player actions | ✅ Already works — `{type:"trait", subject:"player", trait_key:"arousal", operator:"gte", value:1}` | `triggerConditionsSatisfied` v2.py ~2986 |
| +1 per event / set 0 at climax | ✅ Already works — `{targetType:"player", trait:"arousal", op:"add"/"set", value}` | `applyTraitEffect` v2.py ~4544 |
| Cap at 10 (player) / 3 (NPC) | ✅ Already works — `cap` is a first-class effect field | dataclass template_import.py ~438; parsed ~1085/1141; emitted ~4602/4649/4760/4800; threaded into `applyAndNotifyTrait` |
| No decay unless configured | ✅ Already works — leave arousal out of `trait_decay` | player-decay loop v2.py ~4421 (only iterates configured keys) |
| Sidebar bar + level labels (Calm→Burning) | ✅ Already works — `trait_bar` + `trait_words` (the latter already supports `trait_owner:"player"`) | widgets v2.py ~13379 / ~13425 |
| **+1 every day (auto-rise)** | ❌ **NEEDS ENGINE CODE** — daily-tick hook is flag-only today | schema `TemplateDailyTick` template_import.py ~345; loop v2.py ~4433 (`applyFlagEffect`, no traits) |
| Gallery/freeze (pin-to-max) | ❌ Missing (optional) — dev mode only does +/- nudges, no freeze | dev helpers v2.py ~12658 |
| Player-side emotion text in StoryJournal | ❌ NPC-only (optional) | `interpretNpcState` v2.py ~5029; mappings ~9085 |

---

## 3. Engine spec

### E-CORE (REQUIRED) — daily-tick trait effects
The single required change. Today `[engine.daily_tick]` supports only `flagEffects` and calls `window.applyFlagEffect(...)` (flags, not traits).

**Change A — schema** (`template_import.py`, `TemplateDailyTick` ~345):
add a `traitEffects` list alongside `flagEffects`, each entry: `{ targetType, npcId?, trait, op, value, clamp?, cap? }` (same shape as the existing trait-effect dataclass at ~438, which already carries `clamp`/`cap`).

**Change B — runtime** (`v2.py` advanceDay daily-tick loop ~4433):
after the existing `flagEffects` loop, add a `traitEffects` loop that calls the existing `setup.applyAndNotifyTrait(targetType, npcId, trait, op, value, clamp, cap)` (defined ~4688). Mirror the flagEffects branch exactly; wrap in the same try/catch.

**Why this one hook covers everything:** it powers both the player +1/day (`{targetType:"player", trait:"arousal", op:"add", value:1, cap:10}`) and the family-NPC +1/day (`{targetType:"npc", npcId:"npc_frank", trait:"arousal", op:"add", value:1, cap:3}`). `cap` already works on the effect path, so no separate cap item is needed.

**Acceptance:** advancing one day applies each `traitEffects` entry once; capped values stop climbing; a build with no `traitEffects` is byte-identical to today (back-compat).

### E-GALLERY (OPTIONAL — only for literal 100% parity)
No `galleryMode` equivalent exists. Spec a dev/gallery flag that (a) makes arousal *reads* return max and (b) skips arousal *mutators*. Lowest value of the set — RTS uses it only for the unlock-all gallery. Recommend deferring unless a gallery feature is actually wanted.

### E-EMOTION (OPTIONAL)
`emotion_mappings` / `interpretNpcState` are NPC-only (~5029, ~9085). To get "she feels burning with desire" *narrative* text on the player (StoryJournal), generalize `trait_owner` to accept `"player"` and add an `interpretPlayerState`. **Not needed for the sidebar label** — `trait_words` already renders the player-facing Calm→Burning band. Optional polish.

---

## 4. TLS adoption checklist (content — no engine code beyond E-CORE)

1. Add `arousal = 0` to Maya's `player.core_traits` (in `7_final_game.toml` + mirror to `1_metadata_and_locations.toml`).
2. Add a sidebar `trait_bar` (arousal, max 10) + a `trait_words` block with bands **Calm / Warm / Aroused / Hot / Burning**.
3. Append `{targetType:"player", trait:"arousal", op:"add", value:1, cap:10}` to every Maya lewd beat (teases, flashes, ambient grope beats).
4. Add `[engine.daily_tick].traitEffects`: player arousal +1 (cap 10) and the always-around NPC arousal +1 (cap 3).
5. Gate Maya-initiated lewd actions on `player arousal gte 1` (the fuel switch).
6. In every climax/finisher canvas, `set` player arousal 0 **and** participating NPC arousal 0 in the same effect block.
7. Re-scale NPC arousal authoring to the **0–3** band (values + `cap:3`); gate escalation beats on `npc corruption gte X AND npc arousal gte Y` (RTS uses 5/10/15 + 1/2/3).
8. **Delete `arousal` from `[npcs.trait_decay]`** — today TLS decays Frank's arousal 1/day, the exact opposite of RTS. This must be removed.

---

## 5. Effort tiers

- **Behavioral core (recommended for "feels like RTS"):** E-CORE only + the full TLS content checklist. One engine change (schema + one JS loop), the rest is authoring. Reproduces all five fidelity behaviors.
- **Full 100% parity:** the above **+ E-GALLERY + E-EMOTION**. Adds the gallery freeze and player narrative-emotion text — cosmetic/edge, not part of the core loop.

---

## 6. Test plan

1. **Build:** `package_from_toml` on TLS → exit 0, validation passes, no NEW warnings.
2. **pytest:** add a test that a `daily_tick.traitEffects` entry applies once per `advanceDay` and respects `cap`; baseline otherwise unchanged.
3. **Twee inspection:** `setup.daily_tick.traitEffects` present; advanceDay emits the traitEffects loop; arousal not in `player_trait_decay`/`npc_trait_decay`.
4. **Live-play (twine-game-explorer):**
   - arousal **accumulates** — +1 per lewd beat and +1 across a slept day; **never falls** without a climax.
   - at arousal 0 the Maya lewd action is **blocked**; at ≥1 it's available (the `>0` switch).
   - climax canvas drops **both** player and NPC arousal to 0.
   - NPC daily rise **caps at 3**; player caps at 10.
   - global `corruption` core_trait is **unchanged** by any arousal effect (axes stay separate).

---

## 7. Risks

- **Scale choice (10/3 vs 100):** RTS numbers (cap 10 / cap 3) are the faithful option and are fully supported via `cap`. Sidebar bands must match whatever scale is chosen.
- **Keep arousal and corruption separate** — arousal effects must never write `corruption` (preserve the Frank economy spine: catch 25 / crack 35 / Stage-4 50). Same doctrine as worn-corruption in [[tls_clothing_system]].
- **Don't reintroduce decay** — the whole point is accumulation; the wrong-direction TLS decay (step 8) is the one thing that must be deleted, not retuned.
- **Back-compat** — E-CORE must no-op when `traitEffects` is absent (existing games unaffected).

---

*Companion: docs 38 (RTS arousal) + 39 (RTS vs TLS). Implementation, when approved, should mirror the worn-clothing W1–W6 cadence (schema → generator → tests → docs → TLS adoption → verify). Memory: `rts_arousal_system.md`.*
