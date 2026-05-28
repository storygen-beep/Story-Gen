# Doctrine 09 — Trait Catalog (Canonical Trait Vocabulary)

**Source:** Doc 68 (`28th_april_TLS_Phase2_Redesign/68_Trait_Catalog.md`, 2026-05-26).
**Authority:** Doctrine. The canonical trait vocabulary every RTS-shape sandbox game uses.
**Purpose:** Name every Tier 1 + Tier 2 trait, declare its range + default + decay + sidebar render + bands, document when to use each + why not a close-neighbor trait. Replaces ad-hoc per-game trait invention.

**Locked decisions (Doc 68 LO calls 2026-05-26):**
- **Q1:** Stage trait is INTERNAL-ONLY, never player-facing.
- **Q2:** Player corruption = 0–100, 4 named bands (Pure / Lewd / Slutty / Whore).
- **Q3:** NPC affection trait = canonical name `relation` everywhere (RTS-aligned).
- **Q4:** Body-state canon = `energy` + `hygiene` only.

**Three tiers:**
- **Tier 1 — Required** for every RTS-shape sandbox. Always declared in initial state.
- **Tier 2 — Common extensions** used when the arc/setting calls for them.
- **Tier 3 — Per-game additions** authored against the design book, EXCEPT for §6.1 off-limits list (Phase 2+ engine work reserved).

Cross-reference: `schema/01_engine_capabilities.md` §6 (effect + predicate vocabulary); `doctrine/02_three_lanes_plus_capstone.md` (lane gating uses traits); `doctrine/04_authoring_rules.md` (rules reference trait names).

---

## §1 — Per-trait template

Every Tier 1 + Tier 2 trait is documented with the same 13 fields:

```
### `<name>` (<Player|NPC>)

**Tier:** <1 canonical / 2 common / 3 free-form>
**Range:** <numeric min–max or band-string>
**Default at game start:** <starting value>
**Decay:** <None / per-day amount / on-action>
**Sidebar render:** <trait_bar / trait_status_text / trait_words / hidden>
**Bands (if applicable):** <named bands with ranges>

**What it tracks:** <one-sentence semantic definition>

**When to use it:** <bulleted list of game-state changes that call for this trait>

**Why this trait, not another:** <disambiguates against close-neighbor traits>

**Modifiers (what changes it):** <bulleted list of in-game actions + their effects>

**What it gates (downstream content):** <bulleted list of content unlocks>

**Don't use it for:** <bulleted list of misuses>

**Anti-pattern:** <specific wrong usage with explanation>

**RTS analog:** <reference variable name in RTS source>
```

---

## §2 — Trait initialization requirement (READ BEFORE §3)

**Every player trait referenced in any effect, condition, or sidebar item MUST be pre-declared in the game's `[player.core_traits]` block at game start with an initial value.** Engine requirement, not stylistic.

```toml
[player.core_traits]
corruption = 0
arousal = 0
energy = 100
hygiene = 100
money = 80
# Per-NPC stage traits (one per NPC with an arc)
frank_stage = 0
ryan_stage = 0
jake_stage = 0
# Tier 2 traits (declare only if used)
fitness = 0
beauty = 0
exhibitionism = 0
intelligence = 0
```

**Why:**
- **Validator (sidebar only):** `template_import.py:2382-2547` rejects sidebar items referencing undeclared traits with hard error.
- **Runtime (effects + conditions):** `triggerConditionsSatisfied` reads `(player.core_traits || {})[key]` — undeclared = `undefined` = silent garbage. Conditions silently evaluate against `undefined`; effects produce garbage deltas. **No build error fires for effects or conditions on undeclared traits.**

**NPC traits:** initialized inside each `[[npcs]]` block via its own `core_traits` table. Same declare-before-use rule.

---

## §3 — Tier 1 Player Traits

### §3.1 — `corruption` (Player)

**Tier:** 1 (canonical / required)
**Range:** 0–100 integer
**Default at game start:** 0
**Decay:** None (one-way climb; corruption never goes down)
**Sidebar render:** `trait_words` (4 named bands rendered; raw number hidden)
**Bands:** Pure (0–24) / Lewd (25–49) / Slutty (50–74) / Whore (75–100)

**What it tracks:** Maya's accumulated transgression of her own pre-game norms. The universal cross-arc currency for content-tier unlocking. Climbs through explicit choices (flashing, masturbating, sexual scenes) AND through passive exposure (being groped, watching NPC sex scenes). Never decays.

**When to use it:**
- Clothing-tier unlocks (exhibitionist outfits require corruption ≥ 25)
- Lane 1 menu item unlocks (Tease at 5+; Flash at 15+; Sex at 30+)
- Location access gates (naked-in-hallway requires corruption ≥ 30)
- Per-arc Stage transitions (most arcs gate Stage 2 at corruption 15+, Stage 3 at 30+)
- Lane 2/3 substitution preconditions
- Capstone triggers (paired with a flag — Doc 57)

**Why corruption, not another trait:**
- `arousal` (player) is short-term per-attempt; corruption persists.
- `relation` (NPC) is per-NPC; corruption is global cross-arc currency.
- `exhibitionism` is a narrow subset (show-off axis); corruption is broader transgression.
- `stage` (NPC) is discrete milestone; corruption is continuous progression.

**Modifiers (what changes it):**
- Masturbation activities: +1 per completion
- Flashing / teasing scenes: +1 per beat
- Being groped (Lane 2 ambient): +1 per scene
- Watching NPC sex (peep / voyeur scenes): +1 per beat
- Capstone declaration / first-night: +5 to +10
- Days passing: NONE (no daily climb — corruption requires action)

**What it gates (downstream content):**
- Wardrobe tier-N items
- Lane 1 hub menu items (per-NPC corruption thresholds inside per-NPC corruption ALSO required; both must clear)
- Naked / underwear access to public locations
- Per-arc stage transitions
- Lane 2/3 substitution eligibility

**Don't use it for:**
- Per-day decay (it doesn't decay)
- Body-state gating (use `energy` for "can the player act")
- Per-NPC content gating (use NPC `corruption` or NPC `stage`)
- Capstone triggers as the SOLE gate (capstones need a flag + the corruption threshold — see Doc 57 R1)

**Anti-pattern:** "Reduce corruption when player declines a Lane 1 menu item." Wrong. Failing taboo actions doesn't add OR subtract corruption (RTS's `<<NotifyCorruption N>>` is a UI hint widget, NOT a state mutator. Verified live: clicked "Have sex with him 🔥" at corruption 0 → silent fail, no stat change). Decline = no change.

**RTS analog:** `$player.corruption` (0–200 in RTS; scaled to 0–100 here per Q2 lock).

---

### §3.2 — `arousal` (Player)

**Tier:** 1 (canonical / required)
**Range:** 0–10 integer
**Default at game start:** 0
**Decay:** None (per Doc 40 — arousal is always-climbing fuel meter; no daily decay)
**Sidebar render:** `trait_bar` with optional bands
**Bands (optional):** Cold (0–2) / Warm (3–5) / Hot (6–8) / Burning (9–10)

**What it tracks:** Maya's short-term sexual readiness — the per-attempt fuel meter for masturbation + lewd activities. Climbs from beats + days; resets to 0 on climax. Distinct from corruption (long-term progression).

**When to use it:**
- Masturbation activity gate (must be > 0 to masturbate)
- Lane 3 substitution preconditions ("if Maya aroused")
- Some Lane 1 menu items at high arousal (flash unlocks at arousal 2+; specific lewd activities at 5+)
- Self-touch beats inside scenes (cascade gating on arousal threshold)
- Body-language descriptions inside scene prose (arousal level can route through different prose beats)

**Why arousal, not another trait:**
- `corruption` is long-term cross-arc; arousal is per-attempt + resets at climax.
- NPC `arousal` (different trait) tracks NPC interest; player `arousal` is Maya's interest.
- Don't conflate with `energy` — arousal climbs even when tired (and vice versa).

**Modifiers (what changes it):**
- Lewd scene beats: +1 per beat (peeping, being groped, intimate touch)
- Daily passive: +1 per day (per Doc 40 — "fuel that always climbs")
- Climax (masturbation completion + NPC sex completion): **author-emitted** reset to 0 via `{ targetType = "player", trait = "arousal", op = "set", value = 0 }` on the climax canvas's exit_block. **No engine macro auto-zeroes arousal** — RTS has `FinishMasturbation` / `FinishSex` macros; TLS does not. The reset is the author's responsibility on every climax canvas.
- Cold shower / break beat: -1 (rare; specific scenes only)

**What it gates (downstream content):**
- Masturbate button at any location (must be > 0)
- Lane 3 substitution conditions on solo activities
- Self-touch / flash menu items at NPC hubs
- Cascade beats inside scenes (more content at higher arousal)

**Don't use it for:**
- Long-term content gating (use `corruption`)
- Cross-arc state (arousal is per-attempt, resets)
- Capstone triggers (too volatile)
- Permanent stat ladders

**Anti-pattern:** Decaying arousal per day. Doc 40 explicitly locks no-decay rule based on RTS live verification — sleep RAISES arousal, never resets it. Resets happen only at climax. If a game emits `[engine.daily_tick].traitEffects` with `arousal -1`, that's wrong.

**RTS analog:** `$player.arousal` (integer 0–10).

---

### §3.3 — `energy` (Player)

**Tier:** 1 (canonical / required — body-state per Doc 49)
**Range:** 0–100 integer
**Default at game start:** 100
**Decay:** Per-action (-10 to -25 per activity); restored by sleep (+50 to +100 to full); nap +15
**Sidebar render:** `trait_status_text` (body-state Tier 2 sidebar primitive)
**Bands:** Exhausted (0–24) / Tired (25–49) / Fine (50–74) / Rested (75–100)

**What it tracks:** Maya's capacity to act. Body-state primitive — decays through action, restores through rest. Distinct from corruption (one-way climb) and arousal (per-attempt fuel).

**When to use it:**
- Activity-attempt gating (study button disabled at energy 0; work jobs require energy)
- Time-pressure mechanic (running out of energy forces sleep, advances time)
- Some Lane 1 / Lane 3 conditions ("if Maya not exhausted")

**Why energy, not another trait:**
- Body-state primitive — decays + restores. Corruption + arousal don't.
- Distinct from `hygiene` — both are body-state but track different axes (capacity vs cleanliness).
- Distinct from `intelligence` — intelligence is an outcome of studying; energy is the cost.

**Modifiers (what changes it):**
- Activity completion: -10 to -25 per (study -10, work -15, exercise -15, shower -10)
- Sleep activity: restore to 100 (or +50 if nap-style sleep)
- Nap: +15
- Daily passive: NONE (sleep is the daily restore)
- Some food activities: +5 to +15

**What it gates (downstream content):**
- Activity menu buttons at location hubs (study disabled if energy 0)
- Forced-sleep mechanic (energy 0 → next-action requires sleep)
- Some Lane 3 substitutions (NPC walk-in scenes requiring Maya have energy to engage)

**Don't use it for:**
- Content-tier gating (use `corruption`)
- NPC interaction quality (use NPC `corruption` + Maya `corruption` + `relation`)
- Long-term progression
- Lane 1 menu items at NPC hubs (use stat thresholds, not energy)

**Anti-pattern:** Gating Lane 1 NPC menu items on energy. Wrong axis — Lane 1 is escalation choices, not chores. If Maya is too tired to seduce Frank, that's a fictional issue, not a mechanical gate. Tease/Flash/Sex buttons gate on corruption + Frank's corruption + flag-based stage transitions; NOT energy.

**RTS analog:** `$player.energy` (per RTS source — `<<Energy -10>>` macro inside ReturnButton).

---

### §3.4 — `hygiene` (Player)

**Tier:** 1 (canonical / required — body-state per Doc 49)
**Range:** 0–100 integer
**Default at game start:** 100
**Decay:** -10 per day (daily_tick); restored by shower (+60 to full)
**Sidebar render:** `trait_status_text` (body-state Tier 2 sidebar primitive)
**Bands:** Filthy (0–24) / Dirty (25–49) / Fresh (50–74) / Clean (75–100)

**What it tracks:** Maya's cleanliness state. Body-state primitive — decays daily, restores via shower. Soft modifier for NPC interaction quality (not hard gate).

**When to use it:**
- Soft modifier on NPC interaction quality (some scenes route different prose beats at low hygiene)
- Shower self-care loop (player has reason to shower regularly)
- Sidebar feedback (player can see when Maya needs to shower)

**Why hygiene, not another trait:**
- Body-state primitive — decays + restores.
- Distinct from `energy` — different axis (cleanliness vs capacity).
- Distinct from `beauty` (Tier 2) — beauty is outfit-driven, hygiene is body-driven.

**Modifiers (what changes it):**
- Daily passive: -10 per day (via `[engine.daily_tick].traitEffects`)
- Shower activity: +60 (or set to 100)
- Sex / sweaty activities: -5 to -10
- Some Lane 2/3 substitution scenes (sweat/sex) lower hygiene

**What it gates (downstream content):**
- Soft modifier (prose variants at low hygiene); rarely a hard gate
- Shower activity is the restore loop
- Some NPC reactions at Filthy band (e.g., "you smell — go shower")

**Don't use it for:**
- Hard-gating ALL NPC interactions (soft modifier; don't block entire arcs on hygiene)
- Long-term progression (use `corruption`)
- Per-NPC content gating

**Anti-pattern:** Making low hygiene block ALL NPC interactions or activities. Wrong design — hygiene is a soft modifier that COLORS scenes, not a hard gate. Block at most one specific high-stakes scene; don't block the whole arc. (Per Doc 49 — body-state should encourage self-care, not punish.)

**RTS analog:** No direct RTS equivalent. TLS-specific per Doc 49.

---

### §3.5 — `money` (Player)

**Tier:** 1 (canonical / required)
**Range:** Integer ≥ 0 (no upper cap)
**Default at game start:** Varies by setting (TLS starts at $80 per Doc 30 §4.1)
**Decay:** Rent-driven (recurring cost — typically monthly); shop purchases
**Sidebar render:** Numeric display (with currency symbol; or `trait_words` if banded)

**What it tracks:** Economic pressure / income. Forces the player to engage with arcs (jobs, allowance). Distinct from corruption (sexual progression) and stat-traits (skill progression).

**When to use it:**
- Rent payment (recurring monthly drain; insufficient = game-over-ish)
- Shop purchases (clothing items at thrift store, contraceptive pills at pharmacy)
- Quest rewards (capstones may grant +$ via job offers, sex-work scenes)
- Allowance from NPCs at certain relation thresholds

**Why money, not another trait:**
- Economic axis is its own thing — separate from sexual / emotional / skill progression.
- Forces engagement with peer/service arcs (jobs).
- Discrete state (you have it or you don't), unlike continuous progression traits.

**Modifiers (what changes it):**
- Job rewards (+$20 to +$100 per shift)
- Capstone rewards (+$200 to +$500 for major scenes like SellingMyStepsister — RTS reference)
- Allowance (NPC at high relation gives weekly allowance)
- Rent (-$400/month or per setting)
- Shop purchases (-$ per item)

**What it gates (downstream content):**
- Rent payment (game state — can't pay rent = game-over-ish OR `rent_evicted` flag fail-forward)
- Shop items (thrift clothes, contraceptive pills, pregnancy tests)
- Some quest beats (need $X to do Y)
- Phone purchase, laptop purchase (RTS pattern)

**Don't use it for:**
- Emotional / sexual content gating (use `corruption`, `arousal`, `relation`)
- Lane 2/3 NPC substitution conditions
- Per-NPC arc progression (money is global, not per-NPC)

**Anti-pattern:** Gating Lane 2/3 substitutions on money ("Frank walks in IF Maya has $50+"). Wrong axis — money is economic pressure, not narrative trigger.

**RTS analog:** `$player.money` (integer).

---

## §4 — Tier 1 NPC Traits

### §4.1 — `arousal` (NPC)

**Tier:** 1 (canonical / required, per-NPC)
**Range:**
- **Family/ambient + slow-burn family NPCs:** 0–3 integer (per Doc 40 — RTS-faithful for family register)
- **Peer/dating + career NPCs:** 0–10 integer (matches player range)
- **Service NPCs:** 0–3 (workplace register stays bounded)
- **Antagonist/witness:** N/A (antagonists don't track arousal — use awareness or hidden state instead)

**Default at game start:** 0
**Decay:** None (no-decay per Doc 40 — both player + NPC arousal are always-climbing meters)
**Sidebar render:** Per-arc (see §8 — family/ambient + slow-burn family surface to sidebar; peer/service hide)

**What it tracks:** NPC's sexual interest in Maya. Climbs from Maya's actions (teases, flashes); resets to 0 on climax. The dispatcher precondition for Lane 2/3 walk-in scenes.

**When to use it:**
- Lane 2 random encounter conditions ("if Brother arousal > 0 → bedroom grope eligible")
- Lane 3 substitution conditions ("if Dad arousal > 0 → dishwashing dispatcher fires Dad scene")
- Lane 1 menu items that require NPC interest ("Tease at NPC arousal ≥ 1")
- Stage transitions (NPC arousal threshold combined with Maya corruption threshold marks Stage N → N+1)

**Why NPC arousal, not another trait:**
- `corruption` (NPC) is willingness; `arousal` is short-term wanting.
- Player `arousal` is Maya's interest; NPC `arousal` is the NPC's interest.
- `relation` is bond/love; `arousal` is sexual interest. Both can be high or low independently.

**Modifiers (what changes it):**
- Maya teases / flashes the NPC: +1 per tease/flash
- Daily passive: +1 per day for in-scope family NPCs (per Doc 40 — Dad/Brother/Grandpa hardcoded daily climb)
- Climax in a sex scene with the NPC: **author-emitted** reset to 0 via TWO effects on the climax canvas's exit_block — one for Maya, one for the NPC. **No engine macro auto-zeroes either** — RTS has `FinishSex`; TLS does not. Author must explicitly emit `{ targetType = "player", trait = "arousal", op = "set", value = 0 }` AND `{ targetType = "npc", npcId = "npc_X", trait = "arousal", op = "set", value = 0 }`.
- Some Lane 2/3 ambient scenes: +1 per beat

**What it gates (downstream content):**
- Lane 2 random encounter substitution
- Lane 3 dispatcher substitution
- Lane 1 hub menu items (tease, certain seduction buttons)
- NPC stage transitions (per-arc thresholds)

**Don't use it for:**
- Long-term content gating (use NPC `corruption` + `stage`)
- Cross-NPC state (each NPC's arousal is independent)
- Player-facing display for antagonist NPCs (would spoil the dramatic surprise)

**Anti-pattern:** Decaying NPC arousal per day. Doc 40 locks no-decay for family NPCs (RTS-verified — passive +1/day, never -1/day). If you author `[engine.daily_tick].traitEffects` with NPC arousal -1, that's wrong.

**RTS analog:** `$npc.X.arousal` (integer; emoji-tier-string only used in walkthrough display per Doc 13 §10).

---

### §4.2 — `corruption` (NPC)

**Tier:** 1 (canonical / required, per-NPC)
**Range:** 0–50+ integer (varies by arc depth — Frank caps higher than Marge; Brother in RTS hits 50+ at full arc)
**Default at game start:** 0
**Decay:** None (one-way climb)
**Sidebar render:** Per-arc (see §8 — family/ambient surface; peer/service hide)

**What it tracks:** NPC's willingness to act sexually with Maya. The NPC-side analog of player corruption. Climbs through scene completions; never decays.

**When to use it:**
- Lane 1 hub menu items at NPC's location (per-NPC corruption thresholds gate specific options)
- Lane 2/3 substitution conditions (often combined with NPC arousal + player corruption)
- NPC stage transitions
- Cross-NPC bridge scenes (e.g., RTS `SellingMyStepsister` gates on Brother corruption ≥ 10)

**Why NPC corruption, not another trait:**
- `arousal` is short-term wanting (fluctuates).
- `relation` is broader bond (love/trust).
- `corruption` is the willingness threshold — needed for actual sexual acts to fire.
- `stage` is discrete; `corruption` is continuous.

**Modifiers (what changes it):**
- Flash / tease scenes with this NPC: +1 per scene (RTS pattern: flash raises NPC corruption, not arousal)
- Capstone scenes: +5 to +10
- Sex completion: +1 to +3
- Daily passive: NONE

**What it gates (downstream content):**
- Lane 1 hub menu items (Sex with NPC at NPC corruption ≥ 5; harder acts at higher thresholds)
- Lane 3 substitution scenes (`StageTwoCorruption($npc.Brother)` predicate)
- Per-arc stage transitions
- Cross-NPC bridge scenes

**Don't use it for:**
- Player content gating (use `player.corruption`)
- Cross-NPC gating (each NPC's corruption is independent)
- Per-day decay
- Capstone triggers as the SOLE gate (capstones need flag + corruption threshold)

**Anti-pattern:** Capping all NPC corruption at the same max. NPCs vary per arc — Frank (family/ambient escalation) goes to 50+; Marge (service) stays under 20; Diana (antagonist) doesn't use corruption at all (use awareness instead).

**RTS analog:** `$npc.X.corruption` (integer 0–50+).

---

### §4.3 — `relation` (NPC)

**Tier:** 1 (canonical / required, per-NPC, per LO Q3 — single canonical name)
**Range:** 0–100 integer
**Default at game start:** 0
**Decay:** None (one-way climb; relations don't naturally decay)
**Sidebar render:** Per-arc (see §8 — peer/dating + service surface always; family surfaces post-establishment; antagonist hides)

**What it tracks:** NPC's interpersonal connection to Maya — the love/like/trust spectrum. Single canonical name across all arc shapes (per LO Q3 — `relation` is RTS-aligned and register-neutral enough to work for both intimate and professional bonds).

**When to use it:**
- Peer/dating arc progression (Ryan Stage transitions, first-date capstone triggers)
- Service arc trust gates (Marge promotes Maya at relation threshold)
- Family/ambient late-game intimate beats (Frank "sleep with him" at relation ≥ 30)
- Capstone triggers paired with stage flags
- Cross-NPC scenes that depend on Maya's standing with multiple NPCs

**Why relation, not another trait:**
- Single canonical name per LO Q3 — avoids the love/relation register split.
- Distinct from `corruption` — relation is bond; corruption is sexual willingness. NPC can be high-corruption + low-relation (FWB) or high-relation + low-corruption (chaste mentor).
- Distinct from `arousal` — relation is long-term; arousal is short-term.

**Modifiers (what changes it):**
- Talk / conversation scenes: +1 per scene
- Capstone scenes: +5 to +10 (first-date, partner-establish, declaration)
- Bonding activities (help with chores, listen to NPC's problem): +1 to +2 per
- Some Lane 2/3 intimate beats: +1
- Daily passive: NONE
- Some negative beats: -1 to -5 (rare; specific scenes only — e.g., RTS SleepingBrother negative ending at relation 12)

**What it gates (downstream content):**
- Peer/dating capstones (first-date at relation ≥ 5; partner at relation ≥ 15)
- Service arc trust gates (Marge tells Maya secrets at relation ≥ 20)
- Late-family intimate beats (Frank sleepover at relation ≥ 30)
- Some Lane 1 hub menu items (talk/comfort options at relation thresholds)
- Cross-NPC scenes (Diana confrontation outcome routes on Frank.relation)

**Don't use it for:**
- Short-term per-scene gating (use NPC `arousal`)
- Body-state (use `energy` / `hygiene`)
- Player corruption gating (use `player.corruption`)
- Stage transitions as sole gate (stage uses flag + corruption + relation)

**Anti-pattern:** Decaying relation per day. Relations don't naturally decay just from time passing. Specific negative scenes can decrement; daily_tick should NOT touch relation.

**RTS analog:** `$npc.X.relation` (integer 0–100, RTS-aligned).

---

### §4.4 — `stage` (per-NPC, stored on PLAYER namespace) — 🔒 INTERNAL-ONLY (NEVER PLAYER-FACING)

**Tier:** 1 (canonical / required, one per NPC with an arc)
**Range:** Integer 0 to N (N varies per arc depth — typically 0–4 or 0–5)
**Default at game start:** 0
**Decay:** None (stages don't regress)
**Sidebar render:** ❌ **HIDDEN** — never rendered to any sidebar item, never displayed in any player-facing UI surface.

> **⚠️ STORAGE DOCTRINE:** Stage is stored as a **PLAYER trait keyed by NPC slug**, NOT as a trait on the NPC object. Trait name pattern: `<npc_slug>_stage` (e.g., `frank_stage`, `ryan_stage`, `jake_stage`) at `player.core_traits.<slug>_stage`. Engine special-cases this at `v2.py:5077-5087` (`applyAndNotifyTrait` recognizes the regex `/^([a-z_]+)_stage$/` and updates `setup.npc_arc_stages` registry on upward delta). The NPC's `arc_stages = [...]` declaration on `[[npcs]]` is just the LIST of stage NAMES (display strings); the CURRENT stage value lives on player.

> **⚠️ PLAYER-FACING DOCTRINE:** Per LO Q1 — *"Stage shouldn't be a player-facing thing."* See §9 for the full stage-handling doctrine including how the player feels progression without seeing a stage number.

**What it tracks:** Discrete arc-progression milestone for one NPC's arc. Stored as an integer on the player namespace; used by authors + LLM for content gating; never surfaced to player. Player feels stage progression through what the world DOES (new menu items, NPC behavior shifts, location access opens), NOT through a stage number.

**When to use it:**
- Lane 1 hub canvas selection (multiple canvases per location; engine picks by stage via `selectAutoFireCanvasForLocation`)
- Lane 2/3 substitution conditions ("if Frank stage ≥ 2 → kitchen substitutions eligible")
- Per-stage menu items inside hub canvases (group blocks gated on stage)
- Capstone trigger fingerprints (per Doc 57 R1 — capstones flag-set + stage-advance on exit)
- Quest card `when` conditions (NEVER the quest card text or goals — see §9)

**Why stage, not another trait:**
- `corruption` is continuous; stage is discrete milestone.
- `relation` is bond; stage is arc-progress.
- `arousal` is short-term; stage is permanent.
- Stage is the authoring shortcut for "where in the arc" — cleaner than chaining 3-trait conditions.

**Modifiers (how to advance it):**

```toml
# Capstone scene exit — advance Frank to stage 2
{ targetType = "player", trait = "frank_stage", op = "set", value = 2 }
```

- Effect uses `targetType = "player"` (NOT `targetType = "npc"`) because stage lives on player namespace
- Trait name is `<npc_slug>_stage` (e.g., `frank_stage`, NOT `stage`)
- `op = "set"` only — never `add` (stage advances are deliberate, capstone-driven; no auto-promotion)
- Stage advances are ALWAYS deliberate (via capstone or transition canvas), NEVER from accumulated stats alone
- Daily passive: NONE
- No regression
- Engine logs the advancement timestamp in `game_state.stage_advancement_log[slug]` on upward delta (used by E9 stalled-detection)

**What it gates (downstream content):**
- Lane 1 hub canvas variants (per-stage hub for the location)
- Per-stage menu items (`group` blocks inside hub canvases)
- Lane 2/3 substitution eligibility
- New activities unlocking at NPC's location (e.g., suck-in-pantry button at Frank stage ≥ 3)
- Capstone availability (next capstone in chain gates on current stage)

**How to CHECK stage in a condition (two forms; pick one):**

```toml
# Form A — raw player-trait check (RECOMMENDED for most uses)
{ type = "trait", subject = "player", trait_key = "frank_stage", operator = "gte", value = 2 }

# Form B — dedicated stage predicate via helper (engine plumbing; rarely needed)
{ type = "stage", helper = "frank_stage_2_plus", operator = "is_true" }
```

Form A is cleaner. Form B is engine plumbing (used internally by `stage_label` sidebar widget).

**Don't use it for:**
- **ANY player-facing surface.** No sidebar render. No quest card display. No menu text saying "Frank Stage 2." No achievement showing "Reached Stage 3."
- Continuous gating (use `corruption` for that — stage is for milestones)
- Cross-NPC gating (each NPC has its own `<slug>_stage` trait)

**Anti-pattern:** Writing `{ targetType = "npc", npcId = "npc_frank", trait = "stage" }`. Wrong namespace. The engine looks for stage on the NPC object (where it doesn't exist) instead of on the player namespace at `frank_stage`. Stage gating silently breaks; no build error fires.

**Anti-pattern:** Writing "Frank reaches Stage 2 now" in quest card prose or scene body. Wrong. The PLAYER doesn't think in stages; they think in events. Instead, the in-fiction equivalent — *"Frank invited me to his bedroom"* or *"Frank caught me snooping"* — is what the player sees. Stage is the engine's bookkeeping; events are the player's experience.

**RTS analog:** No stored equivalent — RTS uses derived helpers (`StageOneCorruption($npc.X)`, `StageTwoCorruption($npc.X)`) computed at read-time from underlying corruption + arousal thresholds. TLS stores stage explicitly per LO Q1 — but on the player namespace, not the NPC.

---

## §5 — Tier 2 Player Traits

These are common but optional — use them when the arc/setting calls for them. The LLM should not emit them unless the design book proposes the corresponding mechanic.

### §5.1 — `fitness` (Player)

**Tier:** 2 (common; use if exercise / gym mechanic in game)
**Range:** 0–100 integer
**Default at game start:** 0 (or 10 if game premise includes prior fitness)
**Decay:** None (progression trait per Doc 49)
**Sidebar render:** `trait_bar` if exercise mechanic exists; otherwise hidden

**What it tracks:** Maya's physical fitness — a progression stat for gym-related content + body-aesthetic gates.

**When to use it:**
- Exercise activity rewards (each exercise session +1 or +2)
- Gym-arc content gating (gym-NPC arcs unlock at fitness thresholds)
- Certain sex-scene variant gates (high-fitness Maya gets athletic sex variants)
- Some peer/dating beats (fit Maya can join sports club)

**Why fitness, not another trait:**
- `corruption` is sexual; `fitness` is physical/aesthetic.
- `beauty` is outfit-driven; `fitness` is body-driven.
- `intelligence` is mental; `fitness` is physical.

**Modifiers (what changes it):**
- Exercise activity: +1 to +2 per session
- Gym shifts (if working at gym): +1 per shift
- Capstone-specific gains: +5 to +10
- Daily passive: NONE

**What it gates:**
- Gym arc content
- Fitness-themed dating
- Athletic sex variants
- Some body-aesthetic-required scenes

**Don't use it for:**
- NPC interaction gating outside fitness-specific content
- Long-term progression in non-fitness arcs

**Anti-pattern:** Decay on missed days. Doc 40 + 49 — progression traits don't decay.

**RTS analog:** `$player.fitness` (integer).

---

### §5.2 — `beauty` (Player)

**Tier:** 2 (common; use with wardrobe system per Doc 36/37 — `worn_beauty` predicate)
**Range:** 0–N (derived from worn outfit's beauty value via `worn_beauty` predicate)
**Default at game start:** Derived (starts at starting outfit's beauty)
**Decay:** None (changes when outfit changes)
**Sidebar render:** Hidden (typically) or `trait_bar` (if game surfaces it)

**What it tracks:** Outfit beauty rating. Derived from worn clothing via `worn_beauty` (MAX aggregate from clothing_data per Doc 37). NOT a stored stat — it's a predicate that reads the worn outfit.

**When to use it:**
- Social content gates ("must look beautiful to attend the party")
- Certain peer/dating beats (beauty-threshold first-date scenes)
- NPC reaction variants (high-beauty Maya gets different prose at NPC encounters)

**Why beauty, not another trait:**
- It's derived from outfit (worn_beauty) — distinct from stored stats.
- Distinct from `fitness` (body-driven) — beauty is outfit-driven.
- Allows the player to "dress up" for specific content.

**Modifiers:**
- Outfit changes (worn_beauty re-derives from new outfit)
- No stat-mutator effects (don't write `{ trait_key = "beauty", op = "add" }` — beauty is derived, not stored)

**What it gates:**
- Some social scenes (party, club, formal event)
- Peer/dating beats requiring "looking your best"
- Some NPC reactions

**Don't use it for:**
- NPC sexual content gating (use `corruption`)
- Stored stat-like progression
- Anything that requires `op = "add"` or `op = "set"` (beauty is read-only via predicate)

**Anti-pattern:** Setting beauty as a stored trait. Doc 37 made it derived (worn_beauty predicate). Stored beauty creates a sync bug — if Maya changes outfits, stored value lags behind worn outfit.

**RTS analog:** `$player.beauty` (integer in RTS; TLS uses worn-derived predicate).

---

### §5.3 — `exhibitionism` (Player)

**Tier:** 2 (common; use if flash/tease/exhibitionism arc in game)
**Range:** 0–100 integer
**Default at game start:** 0
**Decay:** None
**Sidebar render:** `trait_bar` or `trait_words` (if banded into Modest / Open / Bold / Brazen)

**What it tracks:** Maya's comfort with showing her body. A narrower subset of corruption — the "show-off" axis. Distinct from corruption (broader transgression) and arousal (short-term).

**When to use it:**
- Flash menu items at NPC hubs (separate from sexual escalation)
- Naked-in-public access (Hallway access while naked)
- Exhibitionist content gates (cam shows, public sex, outdoor exposure)
- Certain Lane 1 menu items (flash, change-in-front-of-NPC)

**Why exhibitionism, not another trait:**
- `corruption` is broader transgression; exhibitionism is the show-off subset.
- Allows separate tracking of "comfortable being seen" vs "comfortable having sex."
- Useful for cam-girl / public arcs without conflating with sexual corruption.

**Modifiers:**
- Flash scenes: +1 per
- Naked-in-public beats: +1 per
- Cam show / public exposure scenes: +1 to +2

**What it gates:**
- Flash menu items
- Naked / underwear public access
- Cam-show / streaming-arc content (if game has career arc with that flavor)
- Outdoor sex scenes

**Don't use it for:**
- General sexual content gating (use `corruption`)
- NPC interaction gating

**Anti-pattern:** Collapsing exhibitionism into corruption. They're related but distinct — Maya can be high-corruption + low-exhibitionism (sexually active but private) or low-corruption + high-exhibitionism (loves being seen but not having sex yet). Keep them separate if the game's arc uses exhibitionism as a distinct progression.

**RTS analog:** `$player.exhi` (RTS integer trait).

---

### §5.4 — `intelligence` (Player) — also accepted: `intel`

**Tier:** 2 (common; use if school / study / academic arc in game)
**Range:** 0–100 integer
**Default at game start:** 0 (or 10 for "average student" premise)
**Decay:** None
**Sidebar render:** `trait_bar` if school mechanic exists; otherwise hidden

**What it tracks:** Academic / cognitive stat. Used for school arc, study mechanic, test grades, certain quest beats.

**When to use it:**
- Study activity rewards (+1 to +2 per session)
- School test / grade gates (Marcus-style "get test grade ≥ 8" quest)
- Tutor / library scenes
- Bookish capstones (academic milestones)

**Why intelligence, not another trait:**
- Separate axis from physical (fitness) / social (relation) / sexual (corruption).
- Specific to academic arcs.

**Modifiers:**
- Study activity: +1 to +2 per
- Tutor scenes: +2 to +3
- Some peer scenes (Brother helps study): +1
- Daily passive: NONE

**What it gates:**
- School content
- Test-grade-pegged quests
- Library/study-arc beats
- Some peer NPC scenes (intelligent Maya can hold smarter conversations)

**Don't use it for:**
- NPC interaction gating outside academic context
- Sexual content gating

**Anti-pattern:** Decay on missed days.

**RTS analog:** `$player.intel` (integer).

---

## §6 — Tier 3 Per-Game Additions

Tier 3 traits are **free-form per game** — authored against the design book, not part of the canonical vocabulary. The LLM emits them only when the design book proposes the mechanic.

**Examples of legitimate Tier 3 traits:**
- `follower_count` (Instafame / metric-grind career arcs — RTS Edward arc analog)
- `gym_membership` (boolean for gym-arc access)
- `notoriety` (small-town gossip mechanic; per-arc, not canonical)
- `confidence` (some character-development arcs use it)
- `language_skill` (foreign-NPC arc)
- `awareness` (per-NPC antagonist tracking — Diana model)

**Constraints on Tier 3:**
- Tier 3 traits CANNOT redefine Tier 1 or Tier 2 names. If a design book proposes "love" or "lust" or "horniness" as a new trait, the LLM redirects to the canonical equivalent (`relation` / `arousal`).
- Tier 3 traits must follow the same engine effect schema (§7) — declared in `[player.core_traits]` or per-NPC `core_traits` initial state, mutated via `{ targetType = "player", trait = "X", op = "add", value = N }`, tested via `{ type = "trait", subject = "player", trait_key = "X", operator = "gte", value = N }`. Effect + predicate use different field names — see §7.6.
- Tier 3 traits should be documented in the game's own design book + per-game README.

### §6.1 — Off-limits list (Phase 2+ traits — DO NOT AUTHOR AGAINST)

These traits surface from Phase 2+ engine work scoped in Doc 65. The LLM MUST NOT emit these in any generated game until LO calls the corresponding strategic decision per Doc 65.

#### `pregnancy.*` traits (Doc 65 E10b — Pregnancy retrofit)

```
player.pregnancy.isPregnant       (bool)
player.pregnancy.days             (integer; days since conception)
player.pregnancy.discovered       (bool)
player.pregnancy.pillDays         (integer; contraceptive cooldown)
player.pregnancy.father           (object — { name: str, discovered: bool })
player.babies[]                   (array of completed pregnancy records)
```

**Why off-limits:** Pregnancy is a complex engine feature requiring father-attribution, parallel scene variants, scandal interaction, birth events. None of this is in the v2 engine yet. Authoring against `pregnancy.isPregnant` without the engine produces broken references.

**Trigger to unlock authoring:** LO calls "ship pregnancy" per Doc 65. Until then, all sex scenes ship bareback (per Doc 30 §7.3.1) with no pregnancy language — future pregnancy retrofit will be additive, not breaking.

#### `scandal_level` / `reputation` (Doc 65 E10c)

**Why off-limits:** Global scandal/reputation is a new engine system requiring multiple writer arcs (outdoor scenes), multiple reader arcs (Diana confrontation gate, town-NPC reactions), and UI surface.

**Trigger to unlock authoring:** LO calls "ship scandal" per Doc 65. Until then, antagonist arcs use per-NPC `awareness` (silent accumulator) instead of global scandal.

#### `gallery.*` flags (Doc 65 E10e)

```
gallery.unlocked_scenes[]
gallery.achievements[]
```

**Why off-limits:** Gallery UI requires Doc 62 (canvas `guide` field) + Doc 64 (sidebar radar) + the gallery panel itself. None shipped.

**Trigger to unlock authoring:** Doc 62 ships + LO calls "ship gallery."

#### Cross-arc completed-scenes tracker (Doc 65 E10f)

```
player.completed_scenes[]
npc.X.completed_scenes[]
```

**Why off-limits:** Cross-arc state writers + readers require the tracker mechanism shipped + the canvas `guide` field. Neither in engine yet.

**Trigger to unlock authoring:** Doc 62 ships + LO calls "ship cross-arc tracker."

---

## §7 — Engine effect schema (how traits emit in TOML)

> **⚠️ CRITICAL — effect syntax vs predicate syntax use DIFFERENT field names.** Both shapes appear below; do not mix them.

### §7.1 — Trait effect (mutate a trait value)

```toml
# Player trait effects
{ targetType = "player", trait = "corruption", op = "add", value = 1 }
{ targetType = "player", trait = "arousal", op = "set", value = 0 }
{ targetType = "player", trait = "energy", op = "add", value = -10 }   # decay via negative-add
{ targetType = "player", trait = "money", op = "add", value = 50 }

# NPC trait effects
{ targetType = "npc", npcId = "npc_frank", trait = "relation", op = "add", value = 2 }
{ targetType = "npc", npcId = "npc_frank", trait = "arousal", op = "add", value = 1, cap = 3 }

# With clamp + cap
{ targetType = "player", trait = "arousal", op = "add", value = 1, clamp = true, cap = 10 }
```

**Required fields:**
- `targetType` — `"player"` or `"npc"` (NOT `subject` — that's predicate)
- `trait` — trait name (NOT `trait_key` — that's predicate)
- `op` — operation (see §7.2)
- `value` — numeric

**Optional:**
- `npcId` — required when `targetType = "npc"` (NOT `npc_id` — that's predicate)
- `clamp` — boolean; floor at 0
- `cap` — upper bound

Schema: `TemplateChoiceEffect` at `template_import.py:503`.

### §7.2 — Allowed `op` values

Engine supports exactly **two `op` values** for trait effects:

| op | Behavior |
|---|---|
| `"add"` | Adds `value` to current trait (use negative `value` for decay/subtraction) |
| `"set"` | Sets trait to `value` directly |

**There is no `"sub"` op.** Decay = `op = "add"` with negative `value` (e.g., `value = -10` to subtract 10).

### §7.3 — Per-trait operation conventions

| Trait | Common ops | Notes |
|---|---|---|
| `player.corruption` | `add` (positive) | One-way climb |
| `player.arousal` | `add` (positive); `set` to 0 only at climax | **No engine macro auto-zeroes** — author must explicitly emit `op = "set", value = 0` |
| `player.energy` | `add` with negative value (decay); `set` to 100 (sleep restore) | `cap = 100` recommended |
| `player.hygiene` | `add` with negative value; `set` to 100 (shower) | `cap = 100` recommended |
| `player.money` | `add` (positive/negative) | Income / costs |
| `npc.X.arousal` | `add` (positive); `set` to 0 at climax | Same author-emitted reset as player arousal |
| `npc.X.corruption` | `add` (positive) | One-way climb |
| `npc.X.relation` | `add` (positive/negative; negative rare) | Doesn't decay daily |
| `<npc_slug>_stage` (player namespace — see §9) | `set` only | Deliberate capstone advances |
| Tier 2 player traits | `add` (positive) | One-way climb |
| Body-state (`energy`, `hygiene`) | `add` (negative for decay), `set` for restores | Daily decay via `[engine.daily_tick].traitEffects` |

### §7.4 — Flag effect (set/unset/toggle a flag)

Different schema from trait effects (separate dataclass `TemplateFlagEffect` at `template_import.py:521`):

```toml
{ targetType = "player", flag = "frank_caught", op = "set" }
{ targetType = "player", flag = "talked_to_ryan_today", op = "unset" }
{ targetType = "npc", npcId = "npc_frank", flag = "secret_known", op = "set" }
{ targetType = "player", flag = "scandal_visible", op = "toggle" }
```

**Required fields:**
- `targetType` — `"player"` or `"npc"`
- `flag` — flag name (NOT `flag_key` — that's predicate)
- `op` — `"set"`, `"unset"`, or `"toggle"`

**Optional:**
- `npcId` — required when `targetType = "npc"`

### §7.5 — Predicate (trigger condition) schema

> **The predicate schema uses DIFFERENT field names from effects.** This is the engine's actual API — there's no translation layer.

```toml
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 15 },
  { type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "relation", operator = "gte", value = 30 },
  { type = "trait", subject = "player", trait_key = "frank_stage", operator = "gte", value = 2 },   # stage check
  { type = "flag", subject = "player", flag_key = "frank_caught", operator = "is_true" },
]
```

**Predicate field names:**
- `type` — `"trait"`, `"flag"`, `"modifier"`, `"days_since_flag"`, `"clothing_slot"`, `"clothing_item"`, `"pass"`, `"item"`, `"stage"`, `"quest"`, `"worn_beauty"`, `"worn_corruption"`, `"worn_type"`, `"corruption_level"`
- `subject` — `"player"` or `"npc"` (predicate uses `subject`; effects use `targetType`)
- `trait_key` (for `type = "trait"`) — trait name (predicate uses `trait_key`; effects use `trait`)
- `flag_key` (for `type = "flag"`) — flag name (predicate uses `flag_key`; effects use `flag`)
- `npc_id` (when `subject = "npc"`) — NPC slug (predicate uses `npc_id`; effects use `npcId`)
- `operator` — comparison op (`"gte"`, `"lt"`, `"eq"`, etc.)
- `value` — comparison value

**Allowed predicate `operator` values:**
- Numeric: `"eq"`, `"ne"`, `"gt"`, `"gte"`, `"lt"`, `"lte"`
- Set: `"in"`, `"not_in"`
- Boolean (for flags + booleans): `"is_true"`, `"is_false"`
- Existence: `"exists"`, `"not_exists"`

### §7.6 — Field-name reference card (KEEP HANDY)

The single most common authoring mistake is mixing effect + predicate field names.

| Concept | EFFECT field | PREDICATE field |
|---|---|---|
| Player vs NPC | `targetType` | `subject` |
| NPC identifier | `npcId` | `npc_id` |
| Trait name | `trait` | `trait_key` |
| Flag name | `flag` | `flag_key` |
| Operation | `op` (`"add"`, `"set"` for traits; `"set"`, `"unset"`, `"toggle"` for flags) | `operator` (`"gte"`, `"lt"`, etc.) |
| Type discriminator | (dispatched by `trait` vs `flag` field presence) | `type` (required: `"trait"`, `"flag"`, etc.) |

**Using effect field names in a predicate (or vice versa) causes silent no-ops — no build error fires.** Validators at `template_import.py:1077` + `:1098` catch some cases as warnings, not all.

---

## §8 — NPC trait sidebar visibility doctrine

Per LO Q6: each NPC's design brief (R7 per Doc 56) declares which traits surface to the player. The catalog provides per-arc-shape defaults; the brief can deviate with reason.

| Arc shape | Sidebar surfaces (default) | Rationale |
|---|---|---|
| **Family/ambient** (Frank) | location + arousal + corruption + relation | Player needs to plan Lane 3 attempts (arousal), Lane 1 escalation (corruption), late-game intimacy (relation). All three mechanically relevant. RTS surfaces all three for family NPCs — verified live. |
| **Slow-burn family** (Jake) | location + arousal + relation | Corruption stays low in slow-burn arcs by design; surfacing it would mislead the player. Arousal + relation are the player-relevant dimensions. |
| **Peer/dating** (Ryan) | location + relation | Dating chain is relation-driven. Arousal is bounded + less player-controllable. Corruption isn't meaningful for peer arcs. |
| **Service** (Marge) | location + relation only | Workplace bond is the operative axis. Arousal/corruption don't apply to service register. |
| **Antagonist/witness** (Diana) | location only | Awareness/scandal accumulator stays HIDDEN — dramatic surprise depends on player NOT seeing how close confrontation is. Doc 30 §6 + Doc 60 lock this. |
| **ALL arc shapes** | `stage` NEVER surfaces | Per LO Q1 + §9 — stage is internal-only across all NPCs. |

### Authoring rule (R7 brief addition)

When writing an NPC's design brief, declare a "Sidebar surfaces" line:

```markdown
**Sidebar surfaces:** location + arousal + corruption + relation (family/ambient default per Doc 68 §8)
```

The brief can override the default with reason. Override must be documented.

---

## §9 — Stage trait special-handling doctrine

Per LO Q1 — *"Stage shouldn't be a player-facing thing."* Stage is the canonical example of a stored trait that lives entirely in the authoring layer and never surfaces to the player.

### §9.0 — Storage location

Stage is stored as a **player-namespace trait keyed by NPC slug**: `player.core_traits.<slug>_stage`. The NPC's `arc_stages = [...]` declaration on `[[npcs]]` is just the LIST of stage NAMES (display strings used by the optional `stage_label` sidebar item — which doctrine FORBIDS using for player-facing rendering); the CURRENT stage integer lives on the player object.

Engine recognition: `applyAndNotifyTrait` at `v2.py:5077-5087` matches the trait name against `/^([a-z_]+)_stage$/` and, when `targetType === 'player'` + delta > 0, updates `setup.npc_arc_stages` registry + writes `game_state.stage_advancement_log[slug] = currentDay`.

**Mutation syntax (advance Frank to stage 2):**

```toml
{ targetType = "player", trait = "frank_stage", op = "set", value = 2 }
```

**Common authoring mistake — wrong namespace:**

```toml
# ❌ WRONG — stage doesn't live on the NPC object
{ targetType = "npc", npcId = "npc_frank", trait = "stage", op = "set", value = 2 }
```

### §9.0.1 — Checking stage in a condition

**Form A — raw player-trait check (RECOMMENDED):**

```toml
{ type = "trait", subject = "player", trait_key = "frank_stage", operator = "gte", value = 2 }
```

Simple, readable, no indirection. Use for almost all stage checks.

**Form B — dedicated `stage` predicate via helper:**

```toml
{ type = "stage", helper = "frank_stage_2_plus", operator = "is_true" }
```

Used internally by `stage_label` sidebar widget. Don't author in trigger conditions.

### What stage IS used for

- **Lane 1 hub canvas selection.** `selectAutoFireCanvasForLocation` picks per-stage canvas at a location.
- **Lane 2/3 substitution conditions.** Substitution rule conditions reference NPC stage.
- **Per-stage menu items inside hub canvases.** `group` blocks gated on stage.
- **Capstone trigger fingerprints.** Per Doc 57 R1.
- **Quest card `when` conditions.** Cards route on NPC stage (without exposing stage number in text).

### What stage is NEVER used for

- **Sidebar items.** No `trait_bar`, no `trait_status_text`, no `trait_words` rendering of stage.
- **Quest card text.** Card prose says *"Frank invited me to his bedroom"*, NOT *"Frank stage 2 reached"*.
- **Quest card `goals` block.** Goals describe in-fiction milestones, not stage numbers.
- **NPC menu text.** Hub canvas prose says *"Frank watches you with a new tension"*, NOT *"Frank Stage 2 unlocked"*.
- **Achievement / notification toasts.** No "Stage 2 reached!" popup.
- **Dev shortcuts in player-visible builds.** Fine for authoring/testing; should not ship in player-facing builds.

### How the player feels stage progression (without seeing it)

| Stage transition | What the player sees |
|---|---|
| Frank Stage 0 → 1 (Maya helps Frank with bookkeeping) | New "Stand close while he reads" menu item in Frank's office hub. Coffee Alone Lane 2 ambient ends differently. |
| Frank Stage 1 → 2 (catch capstone fires) | Frank's kitchen morning hub renders different opening prose. "Sleepover" option appears at evening hub. Hallway pass-by Lane 2 ambient has new variant. |
| Frank Stage 2 → 3 (first night capstone) | Frank's bedroom unlocks as a location. Per-stage Lane 3 substitution kitchen-dishes-while-Frank-cooks becomes eligible. |

The player understands the arc moved without needing a stat number. RTS calls this **"emergent escalation"** — the world fills out around the player as they escalate; the world model itself is the progress feedback.

### Doctrine summary

> **`stage` is stored, never rendered, never spoken of in player-facing text. It exists for the LLM and the validator. Player progression is communicated through content changes, never through stage numbers.**

---

## §10 — Anti-patterns (cross-trait misuses)

### Trait-name anti-patterns

- **Inventing new Tier 1 names.** If the design book proposes `lust`, `horniness`, `desire`, or `attraction`, redirect to `arousal`. If it proposes `love`, `affection`, `attraction-bond`, redirect to `relation`. If it proposes `depravity`, `degeneracy`, `lewdness`, redirect to `corruption`. Tier 1 names are canonical for a reason — multi-game consistency.

- **Per-NPC trait references without proper namespacing.** Two forms — predicate vs effect — use different field names (§7.6).
  - **Predicate (condition):** wrong: `{ type = "trait", subject = "player", trait_key = "npc_frank_corruption" }`. Right: `{ type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "corruption", operator = "gte", value = 5 }`.
  - **Effect (mutation):** wrong: `{ targetType = "player", trait = "npc_frank_corruption", op = "add" }`. Right: `{ targetType = "npc", npcId = "npc_frank", trait = "corruption", op = "add", value = 1 }`.
  - EXCEPTION: stage traits live on the player namespace as `<slug>_stage` — see §9.

### Range / type anti-patterns

- **Player corruption outside 0–100.** Per LO Q2 lock. Don't author against the RTS 0–200 scale.
- **Family NPC arousal outside 0–3.** Per Doc 40. If the LLM emits `{ trait_key = "arousal", op = "add", value = 5 }` for Frank, that's wrong (overflows 0–3, breaks Stage-gating).
- **Float values in integer traits.** All canonical traits are integer; don't emit `value = 0.5`.

### Decay anti-patterns

- **Decaying corruption.** Corruption never decays.
- **Decaying arousal.** Per Doc 40 — no-decay rule. Reset to 0 only at climax.
- **Decaying relation.** Specific negative beats can decrement; daily_tick should NOT touch relation.
- **Decaying stage.** Stages don't regress, ever.
- **NOT decaying energy or hygiene.** These ARE supposed to decay (body-state per Doc 49). If the LLM authors `energy` as no-decay, that's wrong.

### Gating anti-patterns

- **Using arousal for content-tier gating.** Wrong axis — arousal is short-term per-attempt. Use `corruption`.
- **Using corruption for activity-attempt gating.** Wrong axis — corruption is content-progression. Use `energy`.
- **Using `relation` for sexual content gating.** Relation is bond; corruption is sexual willingness. High relation + low corruption = mentor; high corruption + low relation = FWB.
- **Gating Lane 2/3 substitutions on money.** Wrong axis — money is economic; substitutions are sexual/narrative.

### Visibility anti-patterns

- **Exposing stage to the player.** Per LO Q1 + §9.
- **Surfacing antagonist awareness to sidebar.** Per Doc 30 §6 + §8 — the dramatic surprise depends on the player NOT seeing how close confrontation is.
- **Hiding body-state from player.** Energy + hygiene MUST surface. Player needs to know when to sleep/shower.

### Phase 2+ anti-patterns

- **Authoring against `pregnancy.*` traits.** Off-limits per §6.1.
- **Authoring against `scandal_level` / `reputation` globally.** Use per-NPC `awareness` instead.
- **Authoring against `gallery.*` flags.** Off-limits until Doc 62 + gallery panel ship.
- **Authoring against `completed_scenes[]` tracker.** Off-limits until Doc 62 + cross-arc tracker ship.

### Effect-schema anti-patterns

- **Effect using predicate field names (`subject` / `trait_key` / `npc_id`).** Wrong: `{ type = "trait", subject = "player", trait_key = "corruption", op = "add", value = 1 }`. Right: `{ targetType = "player", trait = "corruption", op = "add", value = 1 }`. Using predicate field names in an effect causes silent no-op with NO build error.
- **Predicate using effect field names (`targetType` / `trait` / `npcId`).** Same silent-failure risk in reverse direction.
- **NPC effect without `npcId`.** Wrong: `{ targetType = "npc", trait = "corruption", op = "add", value = 1 }`. Right: includes `npcId = "npc_frank"`.
- **Stage effect targeting NPC namespace.** Wrong: `{ targetType = "npc", npcId = "npc_frank", trait = "stage", op = "set", value = 2 }`. Right: `{ targetType = "player", trait = "frank_stage", op = "set", value = 2 }`.
- **`op = "sub"` for decay.** Engine has no `sub` op (only `add` + `set`). Use `op = "add"` with negative `value`: `{ targetType = "player", trait = "energy", op = "add", value = -10 }`.
- **Stage advance via `op = "add"`.** Wrong: `{ targetType = "player", trait = "frank_stage", op = "add", value = 1 }`. Right: `{ targetType = "player", trait = "frank_stage", op = "set", value = 2 }`. Engine doesn't auto-promote on accumulated `add`s.

---

## §11 — Cross-references

### Sibling doctrine files

- `doctrine/01_rts_principles.md` — P6 (stats change during scenes); P10 (HUD = world model)
- `doctrine/02_three_lanes_plus_capstone.md` — lane gating uses traits
- `doctrine/03_arc_shapes.md` — per-arc-shape sidebar visibility defaults
- `doctrine/04_authoring_rules.md` — rules reference trait names + ranges

### Schema files

- `schema/01_engine_capabilities.md` §6 — effect + predicate vocabulary
- `schema/02_toml_schema.md` §16 — field-name reference card

### Source docs

- `28th_april_TLS_Phase2_Redesign/68_Trait_Catalog.md` — source for this file
- `28th_april_TLS_Phase2_Redesign/40_Player_Arousal_System.md` — no-decay rule + 0–10 player / 0–3 family NPC ranges
- `28th_april_TLS_Phase2_Redesign/49_Story_Goals_vs_Sidebar_Doctrine.md` — body-state vs progression distinction
- `28th_april_TLS_Phase2_Redesign/65_Phase2_Plus_Strategic_Scope.md` — Phase 2+ off-limits decisions

### Engine primitives

- `applyAndNotifyTrait` (`v2.py:5174`) — core trait mutation
- `triggerConditionsSatisfied` (`v2.py:3275`) — predicate evaluation
- Stage advancement detection (`v2.py:5077-5087`) — `<slug>_stage` regex recognition
- `_player_trait_keys` validator (`template_import.py:2382-2547`) — hard-rejects undeclared traits in sidebar items

---

**End of file.** Batch 1 complete. Next: §9.1 quality gate.
