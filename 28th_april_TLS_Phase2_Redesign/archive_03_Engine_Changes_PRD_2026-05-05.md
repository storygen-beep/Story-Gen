# Game Generation Engine — Changes PRD

> **Created 2026-04-28.** Sibling to `00_TLS_Phase2_Diagnosis_and_Direction.md` and `02_TLS_Rewrite_Spec.md`.
>
> **Mandate:** define the engine changes required to support the TLS Phase 2 rewrite. The rewrite spec maps onto the verified Road-to-Success design pattern, but during engine audit we identified gaps where the current generator falls short of what the rewrite needs. This PRD enumerates those gaps with issue/rationale/implementation pointers so engineering can scope and prioritize.

---

## §0 Frame

### How we got here

The TLS Phase 2 rewrite (`02_TLS_Rewrite_Spec.md`) commits to rebuilding the game using a hub-and-event sandbox architecture verified against four reference games (Road-to-Success, New Life Project, Shady Deals, Emilie). The architecture is convention-only — no engine entity changes are required for the basic shape.

A direct audit of the engine source (`apps/game_generation/twee_comprehensive/generators/v1.py`, ~13.3K lines, plus `apps/projects/services/template_import.py`, the schema validator) confirmed that **~80% of what the rewrite spec needs is already supported** (revised upward from initial ~78% after the 2026-04-29 audit pass found E2 trait decay was already implemented). The remaining ~20% splits into:

- **Confirmed engine gaps** that block specific rewrite patterns (3 items: E1, E4, E5).
- **Authoring quality-of-life features** that aren't gaps but would meaningfully reduce hand-authoring volume across the rewrite's ~200 canvases (4 items: E3, E6, E7, E8).
- **Verify-only items** that turned out to be already implemented during audit (1 item: E2).

This PRD captures both, prioritized.

### Engine features I previously thought were gaps but ARE supported

These are NOT in this PRD because the engine already handles them. Listed here for context:

| Feature | Reality |
|---|---|
| NPC schedule auto-update | ✅ `setup.getNpcLocation(npcId)` at `v1.py:2242` computes location dynamically from canvas-linked schedules. Schedule Page UI at `v1.py:12666`. |
| Per-choice conditions | ✅ Choices DO support a `conditions` field. `template_import.py:389`, `v1.py:8872`, runtime check at `v1.py:8476-8495`. |
| Trait operator richness | ✅ 12 operators supported (`eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `in`, `not_in`, `contains`, `not_contains`, `exists`, `not_exists`). |
| Random rare events on canvas triggers | ✅ `chance` field on triggers. `v1.py:3216, 3585`. |
| Notifications / toasts | ✅ `setup.showNotification(text)` and `setup.showEffectNotification()`. `v1.py:3960, 3665`. |
| Modifiers (temporary trait offsets) | ✅ Full system. `v1.py:2551, 2855`. |
| Quest system | ✅ Quests Page exists. `v1.py:9889`. |
| Days-since-flag conditions | ✅ Already a condition item type (`type = "days_since_flag"`). |
| Multi-node canvas + cross-canvas node jumps | ✅ Closure algorithm at `v1.py:359-377`. |

### Status legend used in this PRD

- **P0** — Must have for the rewrite to ship in the new architecture.
- **P1** — Should have to keep authoring volume tractable.
- **P2** — Nice to have. Defer unless cheap.

### What this PRD does NOT cover

- Per-canvas content authoring.
- Voice / register / style work (handled by `02_TLS_Rewrite_Spec.md` §10 + style sheets).
- Frontend UI changes outside the sidebar item type and Schedule Page (those exist).
- TOML schema migration scripts for existing TLS canvases (the rewrite is parallel-rebuild; old canvases stay as-is).

---

## §1 The eight engine changes

### E1 — Flag unset / toggle ops on `flagEffects` [P0]

**Issue.** `flagEffects` entries on choices and exit_blocks always implicitly set the target flag to `true`. There's no way to clear or toggle a flag from TOML. Once set, a flag is set forever (or until manually overwritten — which the engine doesn't expose).

**Why we need it.** The rewrite uses several patterns that require flag clearing:

- Daily cooldowns: `talked_to_frank_today` should clear at day rollover. Without unset, the cooldown becomes permanent on first use.
- Weekly resets: `attended_church_this_week`, `paid_rent_this_week`.
- Mid-arc state resets: `frank_almost_cracked` clearing if Maya backs off the arc.

**Current state.**
- Schema: `template_import.py:326-330` defines `TemplateFlagEffect` with fields `target_type`, `flag` only. No `op` field.
- Runtime: `v1.py:3858-3895` defines `setup.applyFlagEffect()` which assigns `true` unconditionally.
- Validator note: `--dry-run` accepts unknown fields silently. We confirmed earlier that authoring `op = "unset"` passes validation but does NOT unset at runtime.

**Proposed change.**

Schema addition (`template_import.py`):
```python
@dataclass
class TemplateFlagEffect:
    target_type: str  # "player" | "npc"
    flag: str
    npc_id: Optional[str] = None
    op: str = "set"  # "set" (default) | "unset" | "toggle"
```

Runtime (`v1.py:3858-3895`).

Note: actual signature is `window.applyFlagEffect = function(targetType, npcId, flag)` (three positional args, `window`-scoped not `setup`-scoped). The wrapper `setup.applyAndNotifyFlag(targetType, npcId, flag)` at `v1.py:3941` also calls it. Both need a 4th `op` param. All emit-sites in the generator that produce `<<run setup.applyAndNotifyFlag(...)>>` (e.g. `v1.py:3094-3101, 3253-3262`) must be updated to pass `op` when present.

```javascript
window.applyFlagEffect = function(targetType, npcId, flag, op) {
    op = op || 'set';
    // ... existing player/npc resolution unchanged ...
    var flagsObj = (targetType === 'player') ? sv.flags : npc.flags;
    if (op === 'set')         flagsObj[key] = true;
    else if (op === 'unset')  flagsObj[key] = false;   // set-to-false (decided 2026-04-29)
    else if (op === 'toggle') flagsObj[key] = !flagsObj[key];
    // flags_meta tracking only on 'set' — preserve current semantics
};
```

**Acceptance criteria.**

1. TOML with `flagEffects = [{ flag = "X", op = "unset" }]` validates without warnings.
2. At runtime, the unset op sets `State.variables.player.flags[X] = false` (set-to-false convention).
3. `is_true`/`is_false` conditions evaluate correctly against unset flags after the effect.
4. `op = "toggle"` flips the flag value on each fire.
5. `op = "set"` (default behavior) is unchanged from current.
6. Existing TOML without `op` field continues to work (default = set).

**Effort estimate.** Small. ~30-50 lines across schema + runtime. ~2 hours including tests.

**Open question — RESOLVED (2026-04-29):** `unset` means **set-to-false**, not delete-from-dict. Cleaner for serialization round-trips and SugarCube `State` snapshotting. `is_false` checks evaluate identically; `exists` checks would need to be authored with the understanding that all known flags are always present in the dict (which already matches the seeding pattern from `flag_keys` at template-import time).

---

### E2 — Trait decay execution [P0 — ALREADY IMPLEMENTED, verify only]

> **Audit correction (2026-04-29).** During engine source verification, this gap was found to be **already implemented**. The original PRD claim ("Trait decay is configured and validated but not executed") was based on incomplete code reading. Decay IS executed at `v1.py:3673-3700` inside `window.advanceDay()`, fired once per day rollover. The variable names in JS-runtime are `setup.npc_trait_decay` and `setup.player_trait_decay` (the `_config` suffix only appears on the Python-side ingestion vars at `v1.py:505, 627`).
>
> **What's actually there:**
> - NPC decay loop with per-NPC `npc_interacted_today` skip (line 3675-3688). If the player interacted with an NPC today, that NPC's traits don't decay — sophisticated maintenance-pressure semantics already wired.
> - Player decay loop with no skip — applies every day rollover unconditionally (line 3690-3700).
> - `Math.max(0, ...)` clamping at 0 already in place.
> - `npc_interacted_today` is set on every trait/flag effect targeting an NPC at `v1.py:2845`, reset at end of `advanceDay()` at `v1.py:3702`.
>
> **Action for E2:** verify the existing decay produces the maintenance pressure the rewrite arcs assume (Frank/Ryan/Jake stage decay), tune `trait_decay = {...}` per NPC in `0_systems_spec.toml`, and surface decay events in the dev-mode state log if not already visible. **No engine code change required.**
>
> The original analysis below is preserved for context.

---

**Issue (original framing — incorrect).** `trait_decay` config in `0_systems_spec.toml` is parsed and stored but never applied at runtime. NPC trust/love/arousal accumulate forever and never fall.

**Why we need it.** The Frank/Ryan/Jake arc designs in `2b_systems_budget.md` and `02_TLS_Rewrite_Spec.md` §6 assume decay creates maintenance pressure: Maya must *keep* engaging with each NPC or risk losing tier access. Without decay, a single week of Talk-pumping locks in Stage 2 access permanently. The economic loop's "neglect Frank to chase Ryan's big deal → Frank's chore-supervision tier collapses" is impossible without decay.

**Current state.**
- Schema parses correctly: `template_import.py:86, 116`. Format: `trait_decay = { trust = 2, love = 1, arousal = 3 }` (decay-per-day).
- Python ingestion: `v1.py:485-505` (player) and `v1.py:615-627` (NPC) read the config into Python-side vars `self.player_trait_decay_config` / `self.npc_trait_decay_config`.
- JS-side handoff: `v1.py:2019-2020` emits `setup.npc_trait_decay = {...}` and `setup.player_trait_decay = {...}` into the runtime.
- **Runtime execution (CONFIRMED, see audit correction note above): `v1.py:3673-3700` inside `window.advanceDay()` consumes both configs and decays traits at every day rollover.** The original audit's "configured but not executed" claim was wrong.

**Proposed change.**

Add a daily-decay step to the time-advance pipeline. The macro/function that fires at day rollover (current location: TBD by implementer, likely tied to the day-counter increment in `setup.advanceTime`) iterates the decay configs and applies negative effects:

```javascript
setup.applyDailyDecay = function() {
    var sv = State.variables;
    // Player trait decay
    var pConfig = setup.player_trait_decay_config || {};
    for (var trait in pConfig) {
        var amount = pConfig[trait];
        sv.player.traits[trait] = Math.max(0, (sv.player.traits[trait] || 0) - amount);
    }
    // NPC trait decay (per-NPC)
    var nConfigs = setup.npc_trait_decay_config || {};
    for (var npcId in sv.npcs) {
        var nc = nConfigs[npcId];
        if (!nc) continue;
        for (var trait in nc) {
            var amt = nc[trait];
            sv.npcs[npcId].traits[trait] = Math.max(0, (sv.npcs[npcId].traits[trait] || 0) - amt);
        }
    }
};
// Hook into time advance — when day flips, fire decay.
```

**Acceptance criteria.**

1. With `trait_decay = { trust = 2 }` set on Frank, after 5 in-game days with no Frank-trust effects fired, `npc.frank.trust` drops by 10.
2. Decay does NOT take traits below 0 (clamped).
3. Decay applies once per day rollover, not per time-band advance.
4. Daily decay is observable in dev-mode state log.
5. Setting decay to 0 (or omitting) results in no decay (current behavior).
6. Existing games without decay configs continue to work unchanged.

**Effort estimate.** Small to medium. ~40-80 lines including the day-rollover hook (which may need to be added if not already isolated). ~3-4 hours including tests.

**Open question.** Should decay run BEFORE or AFTER day-rollover flag effects (E5)? Recommend: flag effects first, then decay. Flag-effects represent ritualistic state changes (today-flags clear); decay is a passive process.

**Bonus.** Once decay runs, consider exposing `setup.last_decay_day` for sidebar visibility ("trait decayed yesterday: trust -2").

---

### E3 — NPC location sidebar widget (live roster) [P2 — DEFERRED to future]

**Decision (2026-04-28):** demoted from P0 to P2 / future. The Schedule Page already exists at `v1.py:12666` as the player's NPC schedule reference; it's accessible via the chrome "📅 Schedules" link on every passage. That's sufficient for v1. The always-visible right-sidebar live roster is a polish improvement, not a must-have for the rewrite.

The original analysis below is preserved for when this gets revisited.

---


**Issue.** The data exists (`setup.getNpcLocation(npcId)`). The Schedule Page shows a full-detail view. But there's no always-visible right-sidebar widget that renders the live NPC roster — *"Frank: Office, Diana: Kitchen, Jake: Bedroom"* — on every passage.

**Why we need it.** This is the core RtS planning surface. Players need to see at-a-glance where everyone is to make routing decisions ("Frank's in his office, I can go talk to him now" vs. "Frank's in the kitchen, the office is empty, I'll wait"). Without it, Maya navigates blind — opens the office, sees "Frank's not here," wastes time, repeats. Verified at RtS during live exploration: the sidebar's `🏠 House` panel is the highest-information piece of chrome.

**Current state.**
- Sidebar item types: only `trait_words` is verified. `v1.py:10410-10551` renders sidebar items.
- Data source: `setup.getNpcLocation(npcId)` returns `{ location: "Kitchen", activity: "..." }` or null. `v1.py:2242`.
- No sidebar item type that calls this on render.

**Proposed change.**

Add a new sidebar item type `npc_location` (or `npc_location_roster`) to `v1.py:10410-10551` render loop. Schema extension:

```toml
[[sidebar_items]]
type = "npc_location"
title = "House"  # Optional header
icon = "🏠"  # Optional emoji
include_npcs = ["npc_frank", "npc_diana", "npc_ryan", "npc_jake"]
# OR omit include_npcs to render all NPCs that have schedules
show_when = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "arrived_at_franks", operator = "is_true" }
] }
```

Render output (one per NPC in `include_npcs`):
```
🏠 House
Frank          📍 Office
Diana          📍 Kitchen
Ryan           📍 Yard
Jake           📍 Bedroom
```

Each NPC line is interactive-styled (could even be a click-to-navigate link if the location is currently accessible — not required for v1).

**Acceptance criteria.**

1. TOML with `[[sidebar_items]] type = "npc_location"` renders the panel on every passage.
2. NPC location updates when game time advances (calls `getNpcLocation` on each render).
3. `show_when` gates visibility (panel hidden until Maya has arrived).
4. NPC with no current scheduled location shows "—" or is omitted (configurable).
5. The activity field can be optionally rendered ("Frank: Kitchen — breakfast").
6. Style matches existing sidebar cards (`caption-card` class structure).

**Effort estimate.** Small. ~60-100 lines across schema + render. ~3 hours including style tweaks.

**Open questions.**
- Should NPCs not currently scheduled anywhere be shown ("Frank: —") or hidden? Recommend: hide by default, configurable via `show_unscheduled = true`.
- Should the activity-name be optional? Recommend yes, `show_activity = true|false`.
- Should this support a "click to navigate to that location" affordance? Defer to v2.

---

### E4 — Stage-function helpers (named gate recipes) [P1]

**Issue.** No way to define a named composite gate. Same set of conditions gets repeated across every canvas that needs it. Across ~200 canvases with ~12 NPC-arc stages × ~5 gates per stage, the rewrite will repeat the same condition tuples ~60 times. Tuning a stage threshold (e.g., "Stage 2 also needs `beauty >= 50`") requires editing every place that uses it.

**Why we need it.** Authoring scale. The rewrite has 12 NPC arc stages (Frank 4 + Ryan 4 + Jake 4). Each stage is a recipe of 3-5 conditions. Without helpers, those conditions appear inline at every gate-use site. With helpers, the recipe is defined once and referenced by name.

This is a maintainability concern, not a runtime correctness concern. The architecture works without it. Authoring quality and tuning agility require it.

**Current state.**
- No engine support for named condition recipes.
- Conditions are inline arrays only.
- The `2b_systems_budget.md` already informally names stages (Frank Phase A, Frank Restrict, Frank Cracked, etc.) — the helpers would formalize these names in TOML.

**Proposed change.**

Add a top-level `[[engine.stage_helpers]]` section to TOML:

```toml
[[engine.stage_helpers]]
name = "frank_stage_2"
description = "Frank tease tier — gated on Maya corruption + Frank arousal + Restrict declared"
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 25 },
  { type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "arousal", operator = "gte", value = 30 },
  { type = "flag", subject = "player", flag_key = "frank_restrict_declared", operator = "is_true" }
] }

[[engine.stage_helpers]]
name = "frank_stage_3"
description = "Frank crack-adjacent tier"
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 50 },
  { type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "arousal", operator = "gte", value = 60 },
  { type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "love", operator = "gte", value = 40 }
] }

# ... ryan_stage_2, ryan_stage_3, jake_stage_2, jake_stage_3
```

New condition item type to reference helpers:

```toml
conditions = { version = "1.0", items = [
  { type = "stage", helper = "frank_stage_2", operator = "is_true" }
] }
```

Runtime evaluation: `setup.evaluateStageHelper(name)` looks up the helper, recursively evaluates its conditions array using the existing `triggerConditionsSatisfied` machinery, returns true/false.

**Acceptance criteria.**

1. TOML with `[[engine.stage_helpers]]` validates.
2. Helpers can reference traits, flags, days_since_flag, and other primitive condition types — but NOT other helpers (no recursion in v1, to keep evaluation simple).
3. New `type = "stage"` condition item evaluates via lookup + recursive call.
4. Operator support: `is_true` and `is_false`.
5. Helper not found: render-time error visible in dev mode, falls back to `false` in production.
6. Editing a helper definition propagates to all canvases that reference it (no per-canvas edits).

**Effort estimate.** Medium. ~150-250 lines across schema, registry, evaluator. ~6-10 hours including tests for recursive evaluation guards.

**Open questions.**
- Allow helpers to reference other helpers (1-deep)? Adds tuning power, adds cycle-detection complexity. Recommend: defer to v2.
- Allow helpers to take arguments (e.g., `npc_at_stage_2(npcId)`)? Would unify Frank/Ryan/Jake stage-2 into one helper. Strong DRY win. Defer to v2.
- Should helpers also be referenceable in choice/group conditions? Yes — should work uniformly anywhere the condition schema is valid.

---

### E5 — Day-rollover hook [P1]

**Issue.** Daily resets currently have to be manually authored on every Sleep activity (or whichever activity ends the day). Easy to forget. Inconsistent if multiple "ways to advance to next day" exist (Sleep, Skip Day, etc.).

**Why we need it.** Cleaner authoring. One central place to declare "things that happen at every day rollover." Especially important after E1 ships — daily flags need automatic clearing. Without this, every Sleep variant has to enumerate every `*_today` flag manually.

**Current state.**
- No engine-level day-rollover hook.
- Day rollover is implicit (`game_state.time_state.day` increments somewhere in time advance).
- Flag resets must be authored on individual canvases.

**Proposed change.**

Add `[[engine.daily_tick]]` (singular section, not array — one hook config per game):

```toml
[engine.daily_tick]
flagEffects = [
  { targetType = "player", flag = "talked_to_frank_today", op = "unset" },
  { targetType = "player", flag = "talked_to_diana_today", op = "unset" },
  { targetType = "player", flag = "talked_to_ryan_today", op = "unset" },
  { targetType = "player", flag = "talked_to_jake_today", op = "unset" },
  { targetType = "player", flag = "talked_to_marge_today", op = "unset" },
  { targetType = "player", flag = "talked_to_cookie_today", op = "unset" },
  { targetType = "player", flag = "watched_ryan_today", op = "unset" },
  { targetType = "player", flag = "helped_diana_today", op = "unset" },
  { targetType = "player", flag = "sat_with_diana_today", op = "unset" }
  # ... etc
]
effects = [
  # Optional — could host trait decay here if E2 is implemented as part of this hook
]
```

Engine fires this once at every day rollover, BEFORE any other day-1 logic. Hook execution is server-side; no canvas/passage authoring required.

**Optional weekly hook** (for `*_this_week` flags):
```toml
[engine.weekly_tick]
trigger_on_weekday = 0  # Monday
flagEffects = [...]
```

**Acceptance criteria.**

1. TOML with `[engine.daily_tick]` validates.
2. At day rollover, all configured flagEffects fire automatically.
3. Sleep activity authoring no longer needs to manually unset day-flags.
4. Hook fires exactly once per day flip (not per time-band advance).
5. Order vs. trait decay (E2): flagEffects first, then decay. Documented.
6. Existing games without `[engine.daily_tick]` continue to work (no decay, no flag clears unless authored manually).

**Effort estimate.** Small. ~50-80 lines including the hook integration. Depends on E1 (uses unset op). ~3-4 hours.

**Open question.** Should daily-tick run BEFORE or AFTER the player's first action of the new day? Recommend: BEFORE — the new day starts clean. (RtS convention.)

---

### E6 — Per-choice text variants by stat band [P2]

**Issue.** Choice button text is a single static string per choice entry. To vary the label by Maya's corruption band, authors must wrap the entire exit_block in a group-block variant chain — verbose, error-prone, hard to read.

**Why we need it.** §10 of the rewrite spec calls for "register-marker beats" where Maya's interior shift surfaces in single sentences. The same surface mechanic at different corruption bands should LOOK different. *"Sit at the table"* (Closed band) reads differently than *"Sit at the table — claim it"* (Saturated band). Currently the only way to do this is duplicate the entire exit_block which doubles the choice authoring per hub.

**Current state.**
- Choices: single `text` field.
- Variant labels: must be authored via group-block-around-the-whole-exit-block, with a different exit_block per variant.
- Cost per stat-band-aware hub: ~3-4× authoring effort.

**Proposed change.**

Add optional `text_variants` array on choice entries:

```toml
exit_block = { type = "choices", choices = [
  {
    text = "Sit at the table.",  # default fallback
    text_variants = [
      { text = "Sit at the table — claim it.", conditions = { version = "1.0", items = [
        { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 75 }
      ] } },
      { text = "Sit at the table.", conditions = { version = "1.0", items = [
        { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 50 }
      ] } }
      # default falls through if no variant matches
    ],
    targetType = "trigger",
    time_progression_minutes = 30
  }
] }
```

Engine evaluates `text_variants` top-to-bottom, first match wins, falls back to `text`.

**Acceptance criteria.**

1. TOML with `text_variants` validates.
2. At render time, the appropriate variant is selected based on current state.
3. If no variant matches, the default `text` renders.
4. Choice's other fields (`targetType`, `effects`, etc.) are NOT affected by which variant rendered — only the label changes.
5. Existing choices without `text_variants` continue to work.

**Effort estimate.** Small. ~30-50 lines schema + render. ~2 hours.

**Open question.** Should `text_variants` also support icon/emoji variation? (e.g., 🪑 → 🪑✨). Probably yes, free to add — same render path.

---

### E7 — Counter increment helper macro [P2]

**Issue.** Counter increments require verbose effects syntax: `effects = [{ targetType = "player", trait = "lean_by_desk_count", op = "add", value = 1 }]`. Authors will write this hundreds of times across the rewrite (~12 counters × ~50 increment sites each = ~600 increments).

**Why we need it.** Quality-of-life. Saves ~80 chars per increment. Reduces typos. Makes counter-increment authoring feel like a first-class operation, not a verbose effects-array entry.

**Current state.**
- Counters work via existing trait effects.
- No shorthand syntax in TOML or any SugarCube macro for incrementing.

**Proposed change.**

Two changes:

**(a) TOML shorthand on choices/exit_blocks:**
```toml
{ text = "...", targetType = "trigger", inc = ["lean_by_desk_count"], time_progression_minutes = 5 }
# Or with explicit value:
{ inc = [{ counter = "lean_by_desk_count", by = 1 }] }
```

Resolves to existing trait increment under the hood.

**(b) SugarCube macro for use in passage scripts:**
```
<<inc lean_by_desk_count>>
<<inc lean_by_desk_count 2>>
```

Both call the same underlying machinery as `effects = [{ ... op = "add", value = N }]`.

**Acceptance criteria.**

1. TOML `inc` field resolves to numeric trait increment.
2. SugarCube macro `<<inc X>>` increments by 1 by default; `<<inc X N>>` by N.
3. Existing trait-effect syntax continues to work unchanged.
4. The new shorthand and the verbose form produce identical state changes.

**Effort estimate.** Small. ~50-80 lines (schema sugar + macro generator + tests). ~3 hours.

**Open question.** Should there be a corresponding `<<dec X>>` decrement macro? Recommend yes — symmetry, free to add.

---

### E8 — NPC arousal passive accumulation [P2 — defer]

**Issue.** RtS's NPC arousal builds passively when Maya is co-located with the NPC for extended periods. TLS would currently require authors to scatter `arousal +1` effects across every co-presence canvas, plus track the time bands manually.

**Why we need it.** Realism + clean authoring. The Frank-arc pressure depends on Frank's arousal building over time as Maya is near him. With passive accumulation, this happens automatically when she's in his location during his scheduled bands. Without it, every co-presence canvas needs manual arousal pumping.

**Current state.**
- No passive accumulation system.
- `setup.getNpcLocation(npcId)` knows where Frank is now.
- No infrastructure to detect "Maya is at the same location as Frank" and accumulate.

**Proposed change.**

Per-NPC `passive_arousal` config in `0_systems_spec.toml`:

```toml
[npcs.npc_frank]
core_traits = { trust = 0, love = 0, arousal = 0 }
trait_decay = { arousal = 1 }
passive_arousal = { per_band_when_co_located = 1, max_passive = 30 }
```

At time-band advance, engine checks: was Maya at the same location as Frank during the just-ended band? If yes, increment `frank.arousal` by `per_band_when_co_located`, capped at `max_passive`.

**Acceptance criteria.**

1. With `passive_arousal.per_band_when_co_located = 1`, after Maya spends 1 full band in the same location as Frank, `frank.arousal +1`.
2. Capped at `max_passive` — passive accumulation never exceeds this. (Active effects can still push higher.)
3. Existing games without `passive_arousal` config continue to work.
4. Passive accumulation is visible in dev-mode state log.

**Effort estimate.** Medium. ~80-150 lines. Tied to time-advance pipeline — needs careful integration. ~5-8 hours.

**Recommendation: DEFER.** Until the rewrite reaches Phase D (Frank trigger / Ryan partner / Jake hand) and we have actual playtest data, we don't know the right rate. Build the rewrite without passive accumulation first; commission this change if play reveals the need. Listed here for completeness so it's not forgotten.

---

## §2 Recommended implementation order

Sequenced for risk minimization and unblocking the rewrite:

| Order | Change | Priority | Why this order |
|---|---|---|---|
| 1 | E1 — Flag unset / toggle | P0 | Foundation for E5; enables daily-cooldown patterns |
| 2 | E5 — Day-rollover hook | P1 | Depends on E1; enables the daily-reset pattern centrally; small once E1 ships |
| 3 | E2 — Trait decay execution | P0 (verify only — already implemented) | No engine work. Tune decay-per-day in `0_systems_spec.toml` against rewrite arc designs; surface in dev log if not already visible |
| 4 | E3 — NPC location sidebar widget | P2 — DEFERRED | Schedule Page (already shipping) is sufficient for v1; live sidebar is polish |
| 5 | E4 — Stage-function helpers | P1 | Larger; defer until E1/E2/E3 ship and the rewrite begins authoring at scale (need exposes the pain) |
| 6 | E7 — Counter increment macro | P2 | Pure quality-of-life. Ship anytime |
| 7 | E6 — Per-choice text variants | P2 | Pure authoring sugar. Ship when capacity allows |
| 8 | E8 — NPC arousal passive accumulation | P2 — DEFER | Defer until playtest reveals need |

**Suggested batches:**
- **Batch 1 (Foundation, ~6-8 hours):** E1 + E5. Unblocks daily-cooldown patterns and the central reset hook. (E2 was scoped here originally but is already implemented — verification rolls into Phase A authoring.)
- **Batch 2 (Authoring scale, ~10-15 hours):** E4 + E7. Reduces authoring volume across hundreds of canvases.
- **Batch 3 (Polish, ~2-3 hours):** E6. After core rewrite ships.
- **Batch 4 (Deferred / future, ~8-15 hours):** E3 (sidebar widget) + E8 (passive arousal). Conditional on rewrite playtest revealing need.

**Critical path:** Batch 1 (~6-8 hours) is the must-ship. After E1+E5 land — and E2 decay is verified against arc designs — the rewrite can begin Phase A vertical-slice authoring. Batches 2-3 unblock authoring scale; Batch 4 is polish + future.

---

## §3 Backwards compatibility and migration

All eight changes are additive. No existing TOML schema fields change shape; no existing engine semantics are removed.

| Concern | Status |
|---|---|
| Existing games without `op` field on flagEffects | Continue to work (default = set) |
| Existing games without trait_decay config | Continue to work (no decay applied — same as today) |
| Existing games without `npc_location` sidebar item | Continue to work — new sidebar item type is opt-in |
| Existing games without `engine.stage_helpers` section | Continue to work; helpers are opt-in |
| Existing games without `engine.daily_tick` | Continue to work; no automatic resets |
| Existing games using inline trait increments | Continue to work; new shorthand is opt-in |
| Existing games using single-text choices | Continue to work; `text_variants` is opt-in |

**No migration scripts required.** The current TLS v1 game (in `toml_phases/`) continues to compile and play exactly as before.

The rewrite (in `toml_phases_v2/`) opts into the new features as it's authored.

---

## §4 Risk assessment

| Risk | Severity | Mitigation |
|---|---|---|
| E1 unset semantics ambiguous (delete vs. set-false) | Low | Pick delete-from-dict, document, both behave identically for is_false checks |
| E2 decay timing creates visible discontinuities | Low | Apply at day-rollover only, not per-band; visible in dev log; clamp at 0 |
| E3 sidebar widget performance on every render | Low | `getNpcLocation` is already O(canvases × schedules); cache in render state if needed |
| E4 stage-helper recursion / cycles | Medium | Disallow helper-references-helper in v1 (only primitive conditions). Cycle-detection deferred. |
| E5 daily-tick fires too early/late | Low | Pick "before first action of new day" convention, document |
| E6 text variant evaluation order ambiguity | Low | Top-to-bottom, first match wins (matches existing trait_words pattern) |
| E7 counter macro conflicts with existing macros | Low | Verify no `<<inc>>` macro exists today before adding |
| E8 passive accumulation rate too aggressive/slow | High | Defer until playtest |

---

## §5 Open questions for prioritization

Before scoping engineer time, decisions needed:

1. **Trait decay (E2)** — confirm we want decay-based pressure in the design. The `2b_systems_budget.md` and rewrite spec assume decay. If decay is dropped, E2 isn't needed and Frank/Ryan/Jake arc designs need re-examination.
2. **NPC sidebar widget (E3)** — confirm this is the player's primary NPC-schedule visibility surface. If the existing Schedule Page is sufficient, E3 is nice-to-have, not must-have.
3. **Stage-function helpers (E4)** — confirm the rewrite will use enough composite gates to justify the engine work. If we plan to use ≤5 helpers, inline conditions are probably fine.
4. **Daily-tick hook (E5)** — confirm we prefer central declaration over per-canvas authoring of resets. If we're OK with each Sleep activity manually unsetting flags, E5 is convenience-only.
5. **NPC arousal passive accumulation (E8)** — agree to defer? Or is there evidence already from the rewrite that this is needed before playtest?

---

## §6 What this PRD does not commission

- TOML migration tools for existing TLS canvases (parallel rebuild — old canvases stay).
- Style sheet updates / voice register decisions (out of scope; covered by `02_TLS_Rewrite_Spec.md` §10).
- Frontend UI changes outside the sidebar item type and NPC location panel.
- Playtest infrastructure or test harness for the new features.
- Engine performance work beyond making the changes themselves correct.

---

## §7 Status

### Per-item ledger (2026-04-29)

| ID | Item | Priority | Status | Notes |
|---|---|---|---|---|
| **E1** | Flag unset / toggle op | P0 | ✅ **SHIPPED** (Batch 1) | Schema + 10-touchpoint runtime threading. 14 tests. Set-to-false semantics. |
| **E2** | Trait decay execution | P0 | ✅ **already implemented** | Verified at `v1.py:3673-3700` during 2026-04-29 audit; PRD's original "not executed" claim was wrong. Verify-only during Phase A arc tuning. |
| **E3** | NPC location sidebar widget | P2 | ⏸ **deferred** | Schedule Page (`v1.py:12666`) sufficient for v1; revisit if playtest reveals gap. |
| **E4** | Stage-function helpers | P1 | ✅ **SHIPPED** (Batch 2) | `[[engine.stage_helpers]]` + `setup.stage_helpers_map` lookup + new `type=stage` condition branch. Recursion rejected at validate-time. 9 tests. |
| **E5** | Day-rollover hook | P1 | ✅ **SHIPPED** (Batch 1) | `[engine.daily_tick]` config consumed inside `advanceDay()`. Silent (no notification queue). 5 tests. |
| **E6** | Per-choice text variants | P2 | ✅ **SHIPPED** (Batch 2) | `text_variants` array on choices → SugarCube `<<set _cv to ...>>` chain + `<<link _cv "target">>`. First-match-wins. 6 tests. |
| **E7** | Counter increment macro | P2 | ✅ **SHIPPED** (Batch 2) | TOML `inc = ["x"]` shorthand parse-expanded into existing trait effects + `<<inc>>` / `<<dec>>` SugarCube widgets. 7 tests. |
| **E8** | NPC arousal passive accumulation | future | ⏸ **deferred** | Rate is a guess until playtest data; defer until Phase D. |

### Summary

| Field | Value |
|---|---|
| **PRD state** | Draft 4 — Batch 1 (E1+E5) and Batch 2 (E4+E6+E7) shipped 2026-04-29 |
| **Total changes proposed** | 8 |
| **Shipped this session** | 5 (E1, E5, E4, E6, E7) — 41 tests passing |
| **Already implemented (verify-only)** | 1 (E2) |
| **Deferred per PRD** | 2 (E3, E8) |
| **Tests added** | 36 new tests in `apps/projects/tests.py` (49 → 71 with Batch 2 included; pre-existing 35 retained) |
| **Engine files changed** | 2 (`apps/projects/services/template_import.py`, `apps/game_generation/twee_comprehensive/generators/v1.py`) |
| **Migrations** | None (all changes additive) |
| **Engine version targeted** | v1 generator (no v2 engine fork) |
| **Backwards-compatible** | Yes — verified: existing fixtures validate clean and emit unchanged |
| **Blocking the rewrite** | Nothing engine-side. Phase A authoring can begin. |

### Outstanding work (not engine)

1. **Manual integration check**: compile a real game (Road to Success / New Life Project) through Tweego, click through one in-game day in browser. Unit tests prove emission shape; only browser exercise proves runtime correctness end-to-end.
2. **E2 verification during Phase A**: confirm trait decay rates produce the maintenance pressure that `2b_systems_budget.md` assumes. Tune `trait_decay = {...}` per NPC in `0_systems_spec.toml` if needed.
3. **Conditional reactivation**: E3 if Schedule Page proves insufficient during playtest; E8 once Phase D playtest reveals the right per-band arousal accumulation rate.

**Next action:** begin Phase A vertical-slice authoring per `02_TLS_Rewrite_Spec.md`. Engine is unblocked.
