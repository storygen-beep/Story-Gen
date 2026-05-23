# 14 — Engine PRD: RTS-Style Sandbox Additions

> **Created 2026-05-03.**
> Sibling addendum to `03_Engine_Changes_PRD.md` and `08_Engine_PRD_Phase2_Additions.md`. Does not supersede them.
> Specs the engine work needed to shift TLS authoring from VN-style stage chains toward RTS-style sandbox content.
> Empirically grounded in `13_Road_to_Success_Reference.md` (especially §16 Playthrough 2 findings).
> Will require doctrine updates to `feedback_tls_scene_body_style.md` (memory entry) and `11_Hint_Authoring_Guide.md` — flagged in §11.
>
> **Status: specified, not started.** Eight items: S1–S8. Six small (S1–S6, ~95 LOC total). Two structural (S7–S8, ~200 LOC). All additive — zero breaking schema changes.

---

## §0 Frame

### Why this PRD exists

Doc 13 captured what RTS actually does and §16 documented what playing Brother to near-exhaustion taught us. The user has confirmed the design direction (2026-05-03): **shift TLS toward RTS-style sandbox content**, where:

- Each NPC has 8–15 scenes scattered across triggers and tiers (not 3 scripted stage scenes)
- Family/proximity NPCs (Frank, Diana, Marge) get Day-1 random encounters
- Peer NPCs (Jake) keep deterministic quest-chain shape
- Career NPCs (future) get metric-gated digital content
- Same scene branches inside by stat tier, not new scenes per tier
- Stat thresholds are published, not hidden
- Content is dense, not gated behind grinding

This PRD does **not** propose abandoning the stage system. Stage transitions remain the *capstone* layer — big scripted moments like "Frank's first catch." What we add is the *daily texture* layer: random ambient encounters, time-gated check-ins, tier-branched dialogue, and counter-driven progression.

The existing engine ships ~85% of what this requires. This PRD closes the remaining ~15%.

### Status legend

- ✅ Shipped (working in current generator + slice)
- 🟡 Partial (works for some cases, needs extension)
- 🟦 Specified in this PRD, not started
- ⏸ Deferred (rationale in §10 or §12)

### What this PRD does NOT cover

- Authoring the new content (Phase 1 of rollout, but content not engine).
- Doctrine doc revisions (RTS-flat scene-body mandate, hint authoring guide) — flagged in §11 as follow-up work.
- Re-evaluating shipped E1–E11 items from PRDs 03 + 08 (still doctrine-compatible).
- Building S7 linkreplace-drip and S8 thought bubbles (specified but Phase 3, only build if Phase 2 playtest reveals need).
- Schema deprecations of any kind. Everything is additive.

---

## §1 What's already shipped — sandbox capability audit

A focused engine audit (2026-05-03) confirmed which of the RTS-style sandbox capabilities already exist. **5 of 12 are SUPPORTED**, 5 are PARTIAL, 2 are MISSING.

### Already shipped from PRDs 03 + 08 (doctrine-compatible, no rework needed)

| ID | Item | Phase 2 sandbox use |
|---|---|---|
| E1 | `flagEffects[].op = set/unset/toggle` ✅ | Per-scene unlock flags, daily-reset markers |
| E2 | Trait decay execution ✅ | NPC stats drift toward neutral if not interacted with |
| E4 | `[[engine.stage_helpers]]` + `type=stage` condition ✅ | Capstone scenes still gate on `frank_stage_2()` |
| E5 | `[engine.daily_tick]` ✅ | Daily counter resets, helper recomputation |
| E6 | `choices[].text_variants[]` ✅ | Choice text adjusts to stat tier — pattern S1 will mirror to blocks |
| E7 | `<<inc>>` / `<<dec>>` macros ✅ | Counter increments (frank_bookkeeping_count++) |
| E9 | Stage-flag stalled-progress detection ✅ | Hint engine knows when player is stuck |
| E10 | Stage-gated hints + per-NPC template consumer ✅ | Hint picker uses (priority desc, condition_items.length desc, file_order asc) |
| E11 | Stage label sidebar item ✅ | Player sees "Frank: Stage 1" in sidebar |

### New sandbox-readiness audit (this doc)

> **Update 2026-05-03 — Critical pre-existing bug discovered + fixed during Phase 1 Step B.** `template_import.py` lines 3835-3993 had a 4-place bug: group + block_pool block handlers read `conditions` and `blocks` from the TOP LEVEL of the block dict, but the actual TOML format puts them inside `props`. Result: ALL existing `[group]` block stage cascades silently rendered as `<p><em>No content</em></p>`. Fixed via 4 surgical edits (`b.get("blocks") or props.get("blocks") or []` pattern — preserves backward-compat). Verified: existing scene prose now renders (kitchen morning Stage 0, etc.) plus all new Phase 1 sample scenes. 132 tests still pass. **The slice was shipping with broken stage cascades — this is the first live verification that the prose actually appears in the browser.**

| Capability | Status | Where |
|---|---|---|
| Random encounters with `chance` field | ✅ Supported | `setup.checkRandomEncounters()` v1.py:3751-3820, `TemplateTrigger.chance` template_import.py:359 |
| Cross-NPC scene flag conditions | ✅ Supported | `setup.triggerConditionsSatisfied()` v1.py:9225, JSON `{version, logic, items}` |
| Passive trait drift (decay) | ✅ Supported | `setup.npc_trait_decay` v1.py:629-641, applied in `advanceDay()` v1.py:3929-3944, gated by `npc_interacted_today` |
| `chance` field on canvas triggers | ✅ Supported | TemplateTrigger.chance, rolled at v1.py:3807 |
| Choice text_variants | ✅ Supported | Schema template_import.py:459-460, picker v1.py:9689-9697 |
| **Per-block text_variants** | 🟡 Partial — choices only | **S1 below** |
| **Per-canvas executedToday** | 🟡 Partial — only per-activity-name | **S2 below** |
| **QuestsPage counter display** | 🟡 Partial — hint text only | **S3 below** |
| **Threshold notifications on gated choices** | 🟡 Partial — costs only | **S4 below** |
| **Sidebar travel shortcuts** | 🟡 Partial — data-driven, no shortcuts authored | **S5 below** |
| **Passive trait gains** (upward drift) | 🟡 Partial — only decay supported | **S6 below** |
| **Linkreplace-drip multi-step scenes** | ❌ Missing | **S7 below (Phase 3)** |
| **NPC thought bubble block type** | ❌ Missing | **S8 below (Phase 3)** |

**Net: ~85% of the doctrine is already in the engine.** The 8 items below close the remaining 15%.

---

## §2 Phase 1: Author with what we have (zero engine work)

Before any engine code is written, validate the philosophy shift on **one NPC** using only the existing engine primitives. Frank is the natural pilot — he's the densest in the slice (analogous to RTS's Brother) and his content currently spans Stage 0–4.

### Frank pilot scene library — rough shape

Reshape Frank from 3-stage spine into 10–15 scene library:

| Type | Count | Trigger pattern | Engine primitive used |
|---|---|---|---|
| **Random ambient** | 4-5 | Visit kitchen/porch/living room when Frank present + `chance = 0.30-0.50` | Existing `chance` field + location triggers |
| **Player-initiated deterministic** | 2-3 | Click "Talk to Frank" / "Help with chores" buttons | Existing canvas triggers, no chance roll |
| **Time-gated** | 1-2 | Specific time bucket only (evening porch cigarette, late-night kitchen raid) | Existing `weekdays` + `start_time` / `end_time` schedules |
| **Crisis (priority hint variant)** | 1-2 | Rent unpaid + Frank trust > 5 → hint priority swap | Existing hint priority mechanism (verified in `4_story_arc.toml` Frank rent variant) |
| **Stage-flag capstone** | 2-3 | The OLD stage scenes — keep them as flag-gated big moments | Existing `[story_arc.nodes]` + `linked_flag` |

Total = ~10–15 Frank scenes. Currently he has ~3 stage scenes.

### Authoring rules for Phase 1

Each scene in the new library:

1. **Independent gates.** No shared stage spine. Each scene declares its own conditions (location, time, NPC presence, traits, flags).
2. **Opening beat always shows.** Even at low stats, the player gets some text + image when the trigger fires. Use `[group]` blocks for stat-conditional *extended* content, not for *entry* gating.
3. **Optional `[group]` blocks for tier branching.** Wrap the "extra paragraphs at high trust" inside a group with `conditions = {trait: trust, op: gte, value: 15}`. This works today via the existing `group` block + `triggerConditionsSatisfied()` evaluator.
4. **Mix writing tiers deliberately.** Tier-1 utility for ambient ("Frank pours coffee."). Tier-2 vignette for random encounters. Tier-3 character writing reserved for stage capstones and arc transitions.

### Test loop

1. Build slice: `python manage.py package_from_toml --file games/the_long_summer_test/toml_phases/7_final_game.toml --owner-id … --output … --dev`
2. Play 30 minutes from Day 1 EM.
3. Validate three properties:
   - **Day 1 ambient content fires.** Walking around home should trigger Frank random encounters within first 5–10 turns at zero stats.
   - **Come-back-later loop works.** Replay a scene after raising trust by 10. Verify the `[group]`-gated extended content now renders.
   - **Frank feels alive.** Subjective check: does he show up unbidden in the player's life, or does he only appear when the player goes looking?

### Decision gate

- ✅ If Frank works → expand pattern to Diana, Marge, Ryan, Jake. Then begin Phase 2 (engine additions).
- ❌ If Frank still feels mechanical → revisit doctrine before any engine work. The problem may be content density, not engine capability.

---

## §3 Engine additions in this PRD

| ID | Item | Status | Phase | Est. LOC | Schema impact |
|---|---|---|---|---|---|
| S1 | Per-block text_variants | 🟦 | 2 | 20 | Additive |
| S2 | Per-canvas executedToday flag | 🟦 | 2 | 5–15 | None (key change only) |
| S3 | QuestsPage counter display | 🟦 | 2 | 25 | Additive (help_data.npcs[id].counters) |
| S4 | Gated-action threshold notifications | 🟦 | 2 | 35 | Additive (`locked_text_threshold` on choice) |
| S5 | Sidebar travel shortcuts | 🟦 | 2 | 15 | Additive (`sidebar_shortcuts` in metadata) |
| S6 | NPC trait passive gains | 🟦 | 2 | 15 | Additive (`npc_trait_passive_gains`) |
| S7 | Linkreplace-drip multi-step scenes | 🟦 | 3 | ~150 | Additive (new `progressive_reveal` block) |
| S8 | NPC thought bubble block type | 🟦 | 3 | ~50 | Additive (new `thought` block) |

**Total Phase 2 LOC: ~95 lines.** Total Phase 3 LOC: ~200. All additive — zero breaking schema changes. Existing TOMLs remain valid.

---

## §4 S1 — Per-block text_variants 🟦

### Issue

The same scene shows the same paragraphs to every player regardless of stats. A player at trust 0 and a player at trust 30 read identical Frank kitchen scenes. There's no incentive to revisit the scene at higher stats.

### Why we need it

Doc 13 §11 #2 verified live: `BrotherCaughtMasturbating` shows 5 lines of Victoria-disgusted-rejection at MC corruption 6, but ~590 words of Victoria-seducing-Brother sequence at MC corruption 31. Same scene, two depths.

This is the come-back-later loop that makes RTS feel like a sandbox with hidden depth instead of a checklist. Player's reward for grinding stats isn't a *new* scene — it's the *same* scene revealing more of itself.

Without S1, TLS players will hit each scene once at low stats, see all of it, and never replay. The stat economy loses its narrative payoff.

### Current state

- **Schema:** `text_variants: List[Dict[str, Any]]` exists on `TemplateChoice` (template_import.py:459-460). Each variant is `{"text": str, "conditions": {version, items}}`.
- **Picker:** v1.py:9689-9697 iterates variants in order, returns first whose conditions evaluate true via `setup.triggerConditionsSatisfied()`. Falls back to choice's default `text` if none match.
- **Block schema:** paragraph and dialog blocks (v1.py:10487-10489) have `content` field but no `text_variants`. Render is unconditional.

### Proposed change

**Schema** (additive, no break):

```python
# template_import.py — extend block validation if any
# Block dicts gain optional text_variants field, mirroring TemplateChoice
{
  "type": "paragraph",
  "content": "Frank reads the paper.",
  "text_variants": [
    {
      "text": "Frank reads the paper. He glances up when you walk in, smiles briefly, looks back down.",
      "conditions": {"version": "1.0", "logic": "AND", "items": [
        {"type": "trait", "subject": "npc", "npc_slug": "frank", "trait_key": "trust", "operator": "gte", "value": 10}
      ]}
    },
    {
      "text": "Frank reads the paper, but his eyes track you across the kitchen. He clears his throat. 'Coffee's still warm.'",
      "conditions": {"version": "1.0", "logic": "AND", "items": [
        {"type": "trait", "subject": "npc", "npc_slug": "frank", "trait_key": "trust", "operator": "gte", "value": 20}
      ]}
    }
  ]
}
```

**Generator** — `_convert_blocks_to_game_html()` in v1.py:10138-10530, paragraph/dialog branches:

```python
# Pseudocode, ~20 LOC addition:
def render_paragraph(block):
    variants = block.get("text_variants", []) or []
    if not variants:
        return f'<p>{block["content"]}</p>'
    # Emit Twine <<if>>/<<elseif>>/<</if>> chain
    out = []
    for i, variant in enumerate(variants):
        cond_expr = build_twine_condition(variant["conditions"])
        macro = "if" if i == 0 else "elseif"
        out.append(f'<<{macro} {cond_expr}>><p>{variant["text"]}</p>')
    out.append(f'<<else>><p>{block["content"]}</p>')
    out.append('<</if>>')
    return "\n".join(out)
```

`build_twine_condition()` already exists for choice text_variants — reuse.

### LOC

~20 lines in generator (paragraph + dialog branches) + 2 lines schema doc.

### Test plan

1. Author one Frank scene with 3 paragraph variants (low/mid/high trust thresholds).
2. Build slice.
3. Open scene at trust 0 → verify default paragraph renders.
4. Set trust = 12 via dev shortcut → reopen → verify mid variant renders.
5. Set trust = 25 → reopen → verify high variant renders.
6. Confirm no breakage on scenes without `text_variants`.

---

## §5 S2 — Per-canvas executedToday flag 🟦

### Issue

Today, daily firing limits are tracked per **activity name** (`setup.canTriggerActivity(actName, maxPerDay)`, v1.py:3789). If two canvases both belong to the activity "kitchen_chores", they share the cooldown. Bad for sandbox where multiple canvases of the same activity (morning kitchen with Frank, afternoon kitchen with Diana, evening kitchen alone) should each have independent daily fire flags.

### Why we need it

Doc 13 §7 — RTS pattern: `<<if previous() == "Hallway" && random(1,4) == 1 && !$npc.Brother.scenes.PeepBrotherSex.executedToday>>`. Each scene independently gated. Two random encounters can compete for the same dice slot in one passage entry; both have their own daily fire flag.

In TLS today, two kitchen canvases sharing the cooldown means: visit kitchen morning → morning canvas fires → return at evening → evening canvas blocked because activity "kitchen_chores" already fired today. Player gets one scene per day per activity, not per canvas.

### Current state

- **State storage** (v1.py:2957-2990): `sv.game_state.activity_trigger_history[activity_name] = {dayKey, dayCount}`. `dayKey` is "Monday_1" style (from `setup.getCurrentDayKey()`).
- **Reset:** dayKey check (v1.py:2976, 3004) compares stored dayKey against current — if mismatch, treats as fresh day. No explicit reset function needed.
- **Gate read:** v1.py:3789 in `canTriggerActivity()`.

### Proposed change

Change the storage key from `activity_name` to `canvas_id` in 3 call sites:
- v1.py:3573 (write side, when canvas fires)
- v1.py:3789 (read side, when checking cooldown)
- v1.py:2976 / 3004 (dayKey comparison — already canvas-agnostic, no change needed there)

**Backward compatibility:** existing TOMLs that share activities across canvases will get *more* permissive cooldowns under new behavior (each canvas gets its own slot). This is the desired direction. No author intervention needed.

If we want to preserve the activity-level cap as a separate concept (e.g., "can fire kitchen scenes 3 times total across all canvases"), keep `activity_trigger_history` as-is and add a parallel `canvas_trigger_history` keyed by canvas_id. Gate checks consult both.

### LOC

5–15 lines depending on whether we replace or add the per-canvas tracking.

### Test plan

1. Author two canvases under the same activity name (e.g., `kitchen_morning_frank` + `kitchen_evening_diana`, both `activity = "kitchen_visit"`).
2. Visit kitchen morning → first canvas fires. Verify second canvas can also fire same day at evening.
3. Without S2 (control), verify second is blocked. With S2, verify it fires.

---

## §6 S3 — QuestsPage counter display 🟦

### Issue

The hint says "Frank wants help with the books." It does not say "Frank bookkeeping: 1/3 sessions done." Player has no idea how close they are to advancing Frank.

### Why we need it

Doc 13 §13 #6: RTS player loop is *literally* "open Walkthrough → pick a near-unlock → close the gap." This requires the player to *see* what threshold they're trying to cross. Without counter visibility, TLS player can't plan; they grind blindly until something happens.

The counter values exist in `$player.core_traits` and `$npcs[uuid].core_traits` — they're just not surfaced to the QuestsPage.

### Current state

- **QuestsPage** (v1.py:13241-13276): renders hints from `setup.getStageHintForNPC(slug)` per NPC. Has access to:
  - `setup.help_data.npcs[npcId]` — dict of NPC IDs → `{name, ...}`
  - `$npcs[uuid]` — full NPC data including `core_traits`
  - `$player.core_traits` — player traits
- **Helper** `getStageHintForNPC(slug)` (v1.py:4704-4745): picks highest-priority matching hint per NPC. Returns hint object with `text`, optional `tip`, but no counter metadata.
- **Render widget** `renderStageHint` (v1.py:11153): emits hint text + tip into a styled card. No counter rendering.

### Proposed change

**Generator pass — extend `help_data.npcs[npcId]`:**

For each NPC, walk the stage helper definitions (where conditions like `frank_bookkeeping_count >= 3` live) and emit per-trait counter metadata:

```js
// help_data.npcs["uuid-frank"]
{
  name: "Frank",
  counters: {
    frank_bookkeeping_count: { current_field: "$frank.bookkeeping_count", max: 3, label: "bookkeeping sessions" },
    frank_trust: { current_field: "$frank.core_traits.trust", max: 15, label: "trust" }
  }
}
```

The thresholds are auto-detected from existing stage helper gate lists — no new authoring required for existing TOMLs to get counter display.

**Twee passage — extend `renderStageHint` widget** (v1.py:11153):

```twine
<<if _hint.counters && Object.keys(_hint.counters).length>>
  <div class="counter-row">
    <<for _key, _ctr range _hint.counters>>
      <<set _current = setup.evalTraitField(_ctr.current_field)>>
      <span class="counter-badge"><<print _ctr.label>>: <<print _current>>/<<print _ctr.max>></span>
    <</for>>
  </div>
<</if>>
```

**CSS:**

```css
.counter-row {
  display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px;
}
.counter-badge {
  display: inline-block; padding: 2px 8px;
  background: var(--theme-surface-alt); color: var(--theme-text);
  border: 1px solid var(--theme-border); border-radius: 10px;
  font-size: 0.78em; font-weight: 600;
}
```

### LOC

25 lines (15 generator helper-data extension + 5 widget edit + 10 CSS).

### Test plan

1. Author Frank stage helper requiring `frank_bookkeeping_count >= 3`.
2. Build slice.
3. Open QuestsPage at count = 0 → verify "bookkeeping sessions: 0/3" badge renders alongside Frank hint.
4. Do bookkeeping once → reopen QuestsPage → verify "1/3".
5. Do bookkeeping 3 times → verify counter disappears (stage advanced, helper no longer in gate path) OR shows "3/3 ✓".

---

## §7 S4 — Gated-action threshold notifications 🟦

### Issue

When a TLS choice is gated by a condition the player doesn't meet, the choice silently doesn't render. Player has no feedback. They don't learn what's possible.

### Why we need it

Doc 13 §7.2 — RTS Bedroom passage uses notifications to publish thresholds: *"I should wear some clothes.. 30+ Corruption Needed"*. The mechanic and the rationale are surfaced together. Failure becomes information, not punishment. The notification is in-character (Victoria's internal voice) but exposes the exact threshold.

In TLS today, a player who can't yet flash Frank just sees no Flash button. No hint. No threshold. They have to read the Walkthrough panel hoping there's a hint about it.

### Current state

- **Cost-blocked messages exist:** `setup.getCostBlockedMessage()` v1.py:3344-3358 surfaces "Requires X Trait (you have Y)" when a *cost* fails (e.g., not enough money for a purchase).
- **No equivalent for choice condition failures.** Conditions are evaluated and the choice is hidden if false. No notification path.
- **Notification system:** `setup.showEffectNotification()` v1.py:4269-4300, queues effects into `setup.pendingEffects`, emits styled `.effect-toast` div (CSS at v1.py:12124). No type distinction (warning vs info).

### Proposed change

**Schema — add `locked_text_threshold` field on choice:**

```python
@dataclass
class TemplateChoice:
    text: str
    text_variants: List[Dict[str, Any]] = field(default_factory=list)
    conditions: Dict[str, Any] = field(default_factory=dict)
    locked_text: Optional[str] = None              # existing: replacement text shown when gated
    locked_text_threshold: Optional[str] = None    # NEW: notification text shown on click attempt
    effects: List[Dict[str, Any]] = field(default_factory=list)
    # ... existing fields
```

**Generator — wire to choice click handler:**

When emitting a gated-but-still-rendered choice (the `locked_text` pattern), wrap the click in a notification trigger:

```twine
<<button "$_choice.locked_text">>
  <<run setup.queueGatedNotification("$_choice.locked_text_threshold")>>
  <<run setup.showEffectNotification()>>
<</button>>
```

**Generator — extend `showEffectNotification()`:**

Recognize new `gated_action` type in the queue:

```js
setup.queueGatedNotification = function(message) {
  setup.pendingEffects.push({ type: "gated_action", message: message });
};

// In showEffectNotification(), add case:
if (effect.type === "gated_action") {
  toast.classList.add("notify-warning");
  toast.textContent = effect.message;
}
```

**CSS** — new `.notify-warning` class (amber background, slightly different from default `.effect-toast`):

```css
.effect-toast.notify-warning {
  background: var(--theme-warning-bg, #4a3520);
  color: var(--theme-warning-text, #ffd9a3);
  border-left: 3px solid var(--theme-warning-accent, #ff9933);
}
```

### LOC

35 lines total (10 schema + 15 generator + 10 CSS).

### Test plan

1. Author Frank choice with `locked_text_threshold = "I'd need to know him better — at least 15 trust — before doing this."`
2. Build slice.
3. Open Frank scene at trust 5 → verify "locked" version of choice renders (greyed/italic).
4. Click the locked choice → verify notification appears with the threshold text.
5. Raise trust to 15 → verify choice becomes active (no notification on click).

---

## §8 S5 — Sidebar travel shortcuts 🟦

### Issue

Travel friction is real. Bedroom → Hallway → Town = 3 clicks. Inside the house, multi-room nav is even worse. RTS mitigates with `🏫 Go to School` hard-coded sidebar button.

### Why we need it

Doc 13 §13 #11 — sidebar shortcuts are a cheap UX win. Most clicks per session in RTS playthrough went to navigation. Cutting nav cost in half cuts overall click count meaningfully.

### Current state

- `sidebar_items` exists at v1.py:730, 742, 2045, 4006 — data-driven. Renders text/badges/links per game state.
- Auto-emit logic for counter traits (v1.py:5914-5954) shows trait values in the sidebar.
- No first-class "shortcut button" concept that navigates to a passage.

### Proposed change

**Schema — add to `1_metadata_and_locations.toml`:**

```toml
[[sidebar_shortcuts]]
label = "🏠 Go Home"
target_passage = "Hallway"
icon = "🏠"
conditions = { ... optional, e.g., "not at home already" }

[[sidebar_shortcuts]]
label = "🏫 Go to Town"
target_passage = "MainStreet"
icon = "🏫"
conditions = { unlocked_flag = "town_unlocked" }
```

**Generator — emit shortcut buttons in right sidebar widget:**

```twine
<<if setup.help_data.sidebar_shortcuts>>
  <div class="sidebar-shortcuts">
    <<for _sc range setup.help_data.sidebar_shortcuts>>
      <<if setup.triggerConditionsSatisfied(_sc.conditions)>>
        <<button "_sc.label">>
          <<run Engine.play(_sc.target_passage)>>
        <</button>>
      <</if>>
    <</for>>
  </div>
<</if>>
```

### LOC

15 lines (5 schema validation + 5 generator emit + 5 widget render + small CSS already in sidebar styles).

### Test plan

1. Define `🏠 Go Home` and `🏫 Go to Town` shortcuts in metadata.
2. Build slice.
3. From any passage, verify shortcuts appear in right sidebar.
4. Click shortcut → verify navigation to target passage.
5. Add a condition (`unlocked_flag = "town_unlocked"`) → verify shortcut hidden until flag set.

---

## §9 S6 — NPC trait passive gains 🟦

### Issue

TLS NPC traits only change when the player triggers actions. Frank's trust doesn't move unless the player clicks something. World feels static.

### Why we need it

Doc 13 §16 finding 4 — Brother arousal climbed 0 → 3 over 3 in-game days passively in RTS. Day 1 voyeur content works because by Day 1 Evening, family arousals are already non-zero, so the random-encounter preconditions are met.

For TLS sandbox: Frank trust slowly accruing from co-presence (player just being in the kitchen at evening) means random encounters can fire earlier. Jake notice slowly increasing on player visibility means his arc starts to move without explicit player action. World drift makes the sandbox feel alive.

### Current state

- `setup.npc_trait_decay = {uuid: {trait: decay_amount}}` v1.py:629-641 — config defined at game build time.
- Applied in `advanceDay()` v1.py:3929-3944 — gated by `!interacted[npcId]` (NPC must not have been interacted with today).

### Proposed change

**Mirror decay config with passive-gains:**

```js
setup.npc_trait_passive_gains = {
  "uuid-frank": { trust: 0.5 },     // +0.5/day if not interacted
  "uuid-jake": { notice: 1.0 }      // +1/day always (could differ in gate)
};
```

**Generator — emit from stage helpers (or new TOML block):**

Recommended: new optional TOML block `[engine.passive_trait_gains]` with same shape as decay config. Authors specify per-NPC passive accruals.

**Runtime — in `advanceDay()` after decay block (v1.py:3944):**

```js
for (var npcId in setup.npc_trait_passive_gains) {
  if (!interacted[npcId]) {
    var gains = setup.npc_trait_passive_gains[npcId];
    for (var trait in gains) {
      var npcData = sv.npcs[npcId];
      if (npcData && npcData.core_traits) {
        npcData.core_traits[trait] = (npcData.core_traits[trait] || 0) + gains[trait];
      }
    }
  }
}
```

**Question for design (not engine):** should passive gains be gated by `!interacted` (same as decay), or always-on, or by other conditions (player at home, player slept, etc.)? Recommend `!interacted` for consistency with decay; authors who want always-on can set decay = 0 + gain = N.

### LOC

15 lines (5 schema + 8 runtime + 2 generator emit).

### Test plan

1. Configure Frank trust passive +0.5/day.
2. Build slice.
3. Sleep 5 days without talking to Frank.
4. Verify Frank trust = 2.5 (or 5 × 0.5).
5. Talk to Frank on day 6, sleep → verify NO passive gain that day (interacted gate working).

---

## §10 Structural items (Phase 3 / optional)

### S7 — Linkreplace-drip multi-step scenes 🟦

#### Issue

TLS scenes render all at once. The player clicks into a scene and sees the entire body in one shot. Then exit. Feels like a popup.

RTS scenes use `<<linkreplace>>` to drip content progressively: click → +paragraph + image → click → +video + new line → click → next reveal. The whole scene unfolds inside one passage, page-by-page.

#### Why we need it (and why it's structural)

Doc 13 §8 — linkreplace-drip is the IF-craft layer that converts "a dice roll triggered this" into "I'm reading a story." Without it, even with all of S1–S6, scenes feel mechanical.

**Why structural:** zero matches for `<<linkreplace>>`, `<<replace>>`, `<<insert>>` in v1.py. No existing scaffold. Would require:

1. New block type `progressive_reveal` in schema with `beats: [{content, condition, media}]`.
2. Generator render emits SugarCube `<<linkreplace>>` macro chains.
3. Click-to-reveal logic on the client side (SugarCube handles natively, but our HTML structure needs the right DOM).
4. Stat changes during scene need to apply on each click (currently scene effects apply on entry only).

#### Trigger gate for building

Build only if Phase 1 + Phase 2 don't satisfy. Most TLS scenes might be fine without it once tier-branched paragraphs (S1) are in place. Re-evaluate after Frank pilot completes Phase 2.

#### Estimated effort

~150 LOC + careful HTML/CSS + manual testing (linkreplace can have edge cases with nested macros).

### S8 — NPC thought bubble block type 🟦

#### Issue

TLS dialog blocks render as styled bubbles for what an NPC *says*. There's no equivalent for what an NPC *thinks*.

RTS uses `💭 NPC is thinking... <em>thought text</em>` rendered as a different colored bubble with the `💭` emoji and italic content. Distinct from regular speech.

#### Why we need it (and why it's structural)

Doc 13 §16 finding 1 — verified live in `BedroomSleepDadScene` (3 thought bubbles across 3 beats). Drastically increases narrative depth without adding text density. Current TLS scene-body style mandate (RTS-flat) prohibits "interior monologue" — but interior monologue *of an NPC* is a different beast and reveals character without forcing players to read more prose.

**Why structural:** new block type, new CSS class. Not an extension of existing block.

#### Proposed change

```python
# Block dict:
{
  "type": "thought",
  "props": {"npcId": "npc_frank"},
  "content": "She's been showing up every evening. Maybe I read her wrong about the rent."
}
```

**Render:**

```html
<div class="npc-thought-bubble" data-npc="frank">
  <span class="thought-icon">💭</span>
  <span class="thought-attribution">Frank is thinking...</span>
  <em class="thought-content">She's been showing up every evening. Maybe I read her wrong about the rent.</em>
</div>
```

**CSS** — new `.npc-thought-bubble` class with italic styling, muted color, thought-cloud border.

#### Estimated effort

~50 LOC (new block type render branch + CSS).

#### Priority

Lower than S7. S7 is the bigger experiential win. S8 is a craft refinement that pairs well with S7 but isn't required.

---

## §11 Doctrine docs to update (follow-up work, not in this PRD)

The philosophy shift conflicts with three existing doctrine docs. **All three need revision before content authoring begins**, or authors will keep producing VN-style content under sandbox rules.

| Doc | Current stance | Required revision |
|---|---|---|
| `feedback_tls_scene_body_style.md` (memory entry) | Mandates **RTS-flat** prose for ALL scene bodies (no sensory density, no interior thought, no body language) | Revise to three-tier system: Tier-1 utility for activities, Tier-2 vignette for random encounters, Tier-3 character writing reserved for arc transitions and named-NPC intros. The flat mandate stays for tier-1; tier-3 explicitly allows sensory + interiority. |
| `11_Hint_Authoring_Guide.md` | Teaches stage-keyed hints (`stage_npc/stage_op/stage_value`) | Add new section on **scene-variant hints by stat tier** using existing hint picker (`priority desc, condition_items.length desc`). Same picker — new use pattern. |
| `01_Repeatable_First_Doctrine.md` | Says repeatable scenes are the spine; one shape per NPC | Add §X: "Repeatable scenes can ALSO have stat-tier branching internally (S1). Same canvas, different content depth at different stats." Doctrine remains compatible — sandbox layer is additive. |
| `02_NPC_Stage_Chains.md` | Stages are the per-NPC narrative spine | Add note: stage chains are now the **capstone layer**; scene library is the **daily texture layer**. Both coexist. Capstones are flag-gated big moments; daily texture is random + deterministic + time-gated mix. |

These revisions are flagged here but **not part of this PRD's deliverables**. They're follow-up work coordinated with the content rewrite for Phase 1.

---

## §12 Phased rollout + risk register

### Rollout

**Phase 1 (1–2 weeks): Frank pilot, content-only, zero engine work.**

- Reshape Frank from 3-stage spine to 10–15 scene library (per §2 above).
- Use only existing engine primitives: `chance` triggers, `group` blocks with conditions, schedules, hint priority.
- Build slice, play 30 minutes, validate sandbox feel.
- Decision gate: does Frank feel alive?

**Phase 2 (1–2 weeks): Small engine additions S1–S6.**

- ~95 LOC total, all additive, zero schema breaks.
- Roll out tier-branching (S1), per-canvas executedToday (S2), counter display (S3), threshold notifications (S4), sidebar shortcuts (S5), passive gains (S6).
- Apply to Frank first, then expand pattern to Diana → Marge → Ryan → Jake.
- Update doctrine docs (§11) in parallel.

**Phase 3 (2–3 weeks, OPTIONAL): Structural additions S7 + S8.**

- Build only if Phase 2 playtest shows scenes still feel like popups instead of flows.
- S7 (linkreplace-drip) is the bigger win. S8 (thought bubbles) pairs with it.
- May not be needed at all — re-evaluate at end of Phase 2.

### Risk register

| Risk | Severity | Mitigation |
|---|---|---|
| **Content authoring volume.** 3 scenes/NPC → 10–15 scenes/NPC × 12 NPCs = ~150 new scenes for full game. RTS has ~130. Are we set up to write that? | High | Validate on Frank first. If pace is acceptable, scale. If not, reduce per-NPC scene count or accept lighter sandbox feel. |
| **RTS-flat doctrine collision.** Memory entry `feedback_tls_scene_body_style.md` will block tier-3 character writing. Authors will stay in tier-2. | High | Update memory entry BEFORE Phase 1 authoring. Explicitly carve out tier-3 for capstones and intros. |
| **Linkreplace gap is real.** Without S7, even with S1–S6, scenes will feel less alive than RTS. | Medium | Phase 2 playtest answers whether S7 is required. Budget 2–3 weeks for Phase 3 in case it is. |
| **Stage system tension.** TLS authored coherent per-NPC arcs. Sandbox shift trades that for emergent narrative. Players may miss the scripted progression. | Medium | Keep stage-flag capstones (the OLD scenes) intact. Emergent narrative is the *daily texture*; scripted arcs are the *milestones*. Both coexist. |
| **Counter discovery for S3.** If stage helpers don't expose thresholds in a parseable way, S3 generator pass might miss some counters. | Low | Walk all `[[engine.stage_helpers]]` definitions, parse `conditions.items` for trait + value pairs. Most should be auto-detectable. Manual override field for edge cases. |
| **Per-canvas executedToday backward compatibility.** Existing TOMLs that share activities will get more permissive cooldowns under S2. May change game balance. | Low | Author TOMLs that depend on the activity-level cap should explicitly set `max_per_day` if they want shared cooldown semantics. Default change is more permissive, which authors can tighten if needed. |

---

## §13 TL;DR

**The engine is more ready than expected.** ~85% of RTS-style sandbox capabilities already ship. Closing the remaining 15% takes:

- **6 small engine additions (S1–S6) totaling ~95 LOC** — all additive, no breaking changes.
- **2 structural additions (S7–S8)** that may not even be needed depending on Phase 2 playtest.

**The biggest work is content authoring**, not engine engineering. We need to write ~150 new scenes across 12 NPCs to populate the sandbox to RTS density. That's a separate effort track — flagged in §12 risk register.

**Three doctrine docs (`feedback_tls_scene_body_style.md`, `11_Hint_Authoring_Guide.md`, `01_Repeatable_First_Doctrine.md`) need revision** before Phase 1 content authoring begins, or authors will reproduce the current VN-style output under sandbox rules.

**Recommended next action:** Phase 1 Frank pilot. Zero engine work. Validate the philosophy on one NPC before committing engine code or content for the others.

---

**End of doc 14.** 🟦 Specified, not started. Status updates land in §1 + §3 tables as items ship.
