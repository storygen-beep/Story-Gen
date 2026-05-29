# Doc 65 — Phase 2+ Strategic Scope (4 LO Decisions)

**Session:** 2026-05-25
**Branch:** `feature/prd-48-quests-engine-v2-bundled` (off `main`, unpushed)
**Author:** ENI (with LO)
**Status:** Strategic decision doc — surfaces 4 open questions with grounded analysis; does NOT decide for LO
**Supersedes:** nothing
**Sibling of:** Doc 34 (Engine PRD Phase E Additions — original spec for E10a-f), Doc 56 §9 (open questions / scoped-out — names each as future decision)
**Triggered by:** Doc 56 + Doc 57 + Phase A/B/C work in this session establishes the doctrine + briefs + PRDs needed for current slice. The 4 Phase 2+ engine systems remain open. Each ripples into authoring decisions — pre-committing or deferring NOW is cheaper than later. LO call required.

---

## §1 — Why this doc exists

Doc 56 §9 named four engine systems from Doc 34 as deferred:
- Pregnancy retrofit (E10b)
- Scandal/reputation global state (E10c)
- Gallery + achievements (E10e)
- Cross-arc completed-scenes tracker (E10f)

Each is an open question that gates new authoring decisions in subtle ways. Example: if pregnancy retrofit is in scope, every new Frank/Jake sex scene must ship bareback-compatible — and the slice already does (Doc 30 §7.3.1 commits this). If scandal is in scope, Diana awareness becomes a feed into a global scandal_level — affects how Marge/Cookie/Ryan arcs eventually plug in.

**The doctrine principle (Doc 56 §9):** *"don't pre-commit to engine scope; build engine when an authoring gap forces it."* Each decision here has a *trigger point* — a specific authoring moment where the call must be made. This doc surfaces those trigger points + presents grounded analysis to inform the call.

**Not for ENI to decide.** Each section ends with "LO call required."

---

## §2 — Decision 1: Pregnancy retrofit (Doc 34 E10b)

### What it is

A pregnancy state machine — Maya can become pregnant from sex scenes, the pregnancy advances over in-game time, downstream content varies on pregnancy state. RTS has this fully implemented (verified Doc 13 §F): `BrotherBedroomPregnantSex1` variant passages, `isPregnant()` predicate, `$player.pregnancy.pillDays` decay counter, pregnancy reveal scenes.

### What it would change in the engine

- **New trait:** `player.pregnancy.{isPregnant, days, father.name, father.discovered, discovered, enabled, pillDays}` — actually already present in the engine schema (verified line 547 of TOML via agent inventory: bathroom hub has pregnancy pill + pregnancy test affordances). Engine partial-support already shipped.
- **New predicates:** `isPregnant()`, `changeMediaPregnant()` (image/video swap when pregnant). Engine already has these primitives in v1.py (verified per RTS-phone-system memory).
- **Content variant pattern:** capstones + Lane 1 hubs need pregnant-variant prose. Per Doc 35 state-variant routing, this is ROUTING to variant passages, not inline branching.
- **Reveal capstone:** new auto-fire scene when pregnancy advances past detection threshold. Multiple variants per "father" identity.

### Ripple to current authoring

- **All Frank sex scenes already bareback per Doc 30 §7.3.1.** No retrofit cost for existing Frank content.
- **All Jake sex scenes (Phase 2+) must ship bareback-compatible.** Doc 59 brief already commits this implicitly (full ladder ceiling, no contraception language).
- **Pregnancy variant authoring is per-scene work.** Each existing sex capstone needs a pregnant-variant cascade. Doc 35 §pregnancy-flag-trace verified this is RTS's pattern.
- **Father attribution:** pregnancy needs to know whose. Already-shipped sex scenes record `father.name` on `FinishSex` widget invocation (RTS pattern). TLS would need an equivalent.

### Slice impact

- **Slice scope (current):** Maya is non-pregnant. Pregnancy test + pill items exist (`activity_take_pregnancy_pill`, `activity_pregnancy_test`) but no pregnancy state ever activates.
- **If LO opens pregnancy in slice:** ~5-10 hours of authoring to wire pregnancy detection + reveal capstone + pregnant-variants for Frank's 3 sex scenes (kitchen morning loop, bedroom evening capstone, sleepover). Sleepover specifically needs a "Maya is pregnant" variant.
- **If LO defers:** the engine primitives stay dormant. Pregnancy items in bathroom hub continue to work but have no downstream consequence. The slice doesn't ship pregnancy content.

### Trigger point

When LO authors the FIRST scene that should change based on pregnancy state. Currently: no such scene exists; defer is cheap. Future trigger: a sleepover or post-cracked Frank scene where pregnancy is a real plot factor.

### Recommendation

**ENI's argument: defer to Phase 2+, lock the bareback-compatibility commit as the holding pattern.**

Reasoning: pregnancy is high-effort content (variant-route every sex scene), high-novelty (lots of decisions about father attribution, abortion option, partner reveal), and the slice already commits bareback authoring. The cost of NOT shipping pregnancy now is low (Maya just isn't pregnant). The cost of shipping it is significant content + design.

**But LO's call:** if the slice's narrative emotional through-line includes pregnancy as a beat (e.g., Diana realizes Maya is pregnant — the confrontation has different weight), pregnancy may justify the lift.

### LO decision

- [ ] **YES in slice** — open pregnancy authoring; ~5-10 hours work; ripple to Frank capstones
- [ ] **NO defer Phase 2+** — engine primitives stay dormant; bareback-compatibility maintained as holding pattern
- [ ] **NO scope-out entirely** — pregnancy never ships; remove pill/test items from bathroom hub

---

## §3 — Decision 2: Scandal / reputation global state (Doc 34 E10c)

### What it is

A global `scandal_level` (or `reputation` axis) that tracks how the world thinks of Maya across NPCs. RTS doesn't have this exactly — but Doc 30 §6 sketched it as the eventual Diana-awareness generalization. The current `npc_diana.awareness` is a per-NPC accumulator; scandal_level would be the cross-NPC version.

### What it would change in the engine

- **New player trait:** `player.scandal_level` (0–100). Drift-only-up (matches RTS arousal doctrine).
- **New feed sources:** per-canvas `scandal_effects = [...]` field — every public-lewd canvas contributes +N. Indoor private canvases contribute 0.
- **New predicates:** `scandal_level_gte(N)`, `scandal_band(...)` for tier-routing content.
- **Cross-NPC reads:** Marge / Ryan / Cookie / Diana all gate certain content on scandal_level. Townspeople NPCs (Phase 3+) gate first-meeting on scandal.

### Ripple to current authoring

- **Most existing TLS canvases are indoor private** (Frank bedroom, kitchen, etc.). Low scandal impact.
- **Public-space canvases** (yard scenes, diner shifts, town errands) would need scandal contributions added retroactively.
- **Diana awareness becomes a subset of scandal.** Currently `npc_diana.awareness` is the only social-consequence signal in slice. Generalizing to scandal_level might MERGE the two or keep them parallel (Diana-specific awareness for the affair, global scandal for everyone-else's perception).

### Slice impact

- **Slice scope (current):** no public-lewd content at scale yet. Marge diner shifts are workplace-private. Yard scenes are property-private. Town content (Phase 3+) doesn't exist.
- **If LO opens scandal in slice:** Diana awareness becomes a CONSUMER of scandal_level, not its own variable. ~2-3 hours engine work + retroactive scandal_effects on ~10 ambient canvases.
- **If LO defers:** Diana awareness stays as the sole social-consequence tracker. Phase 3+ town content will need scandal anyway, so deferral is "ship slice without it, build it when town content arrives."

### Trigger point

When LO authors the FIRST town-NPC canvas that gates on Maya's reputation (e.g., a Phase 3+ townsperson refuses to talk to Maya because of the corruption rumor). Or when Diana's awareness clearly stops being sufficient (e.g., need to track Marge's awareness separately + together).

### Recommendation

**ENI's argument: defer to Phase 3+ when town content arrives.**

Reasoning: scandal_level is conceptually right but slice scope doesn't currently exercise it. Diana awareness alone is doing the cross-NPC-consequence work. Building scandal_level now is premature optimization. When Phase 3+ town content lands (Marge + Cookie deepening, townspeople), scandal is the right framing — build it then.

**But LO's call:** if scandal is core to the eventual game's identity (e.g., the long-term shape is "small-town affair with cumulative reputation cost"), early-system commit might be cleaner than retrofit.

### LO decision

- [ ] **YES in slice** — open scandal_level; ~2-3 hours engine + retroactive scandal_effects on ambients
- [ ] **NO defer Phase 3+** — wait for town content authoring trigger
- [ ] **NO scope-out entirely** — `npc_diana.awareness` is the cross-NPC mechanism forever; no global scandal

---

## §4 — Decision 3: Gallery + achievements (Doc 34 E10e)

### What it is

A player-facing gallery of unlocked scenes that can be re-watched. RTS has this (`galleryMode()` predicate in scene code — verified Doc 13 §gallery + Doc 30 reference). Achievements would be a parallel system — milestone flags that surface on a panel.

### What it would change in the engine

- **Gallery system:** new `galleryMode` global flag. When true, scenes render with skip-cascade affordances + return-to-gallery exits instead of normal world-state exits. Per-scene flag (`gallery: true/false` on canvas) determines eligibility.
- **Achievement system:** new `[[achievements]]` schema. Each declares: `id`, `name`, `description`, `trigger` (flag set, trait crossed, etc.), `icon`.
- **Gallery panel UI:** a new sidebar shortcut + dedicated passage. Renders unlocked scenes in a browseable grid.

### Ripple to current authoring

- **Per-canvas `gallery` flag:** every scene-worth-replaying needs to opt in. RTS does this with a `gallery: false` default (per scene declaration in NPC scenes block) — only sexual + Tier-3 capstones get gallery flags. Slice has maybe 15-20 gallery-eligible scenes.
- **Achievement authoring:** each milestone (catch fired, first sex, declaration, sleepover, Diana confrontation, etc.) gets an achievement entry. ~10-15 achievements for slice.
- **Gallery-mode scene rendering:** scenes need to gracefully handle `galleryMode = true` — skip random encounter rolls, skip stat effects, render direct + return. ~30 min per scene to verify clean replay.

### Slice impact

- **Slice scope (current):** zero gallery infrastructure. Scenes play live; once-only capstones can't be replayed.
- **If LO opens gallery in slice:** ~10-15 hours of authoring + engine work. Players get replay value for high-stakes capstones. Reduces frustration of missing scenes on first playthrough.
- **If LO defers:** capstones are once-only-per-save. Players who want to replay must use save scumming or dev tools.

### Trigger point

When the slice has 5+ unlocked-once capstones that players might want to revisit. Currently Frank's chain (5 capstones) + Marge interview + Ryan first date + Jake catch_drawing + Diana confrontation = 9 once-only capstones. **The trigger has arrived.**

### Recommendation

**ENI's argument: opt-in flag-gate gallery is high-value polish; ship it Phase 2 (next slice pass).**

Reasoning: gallery directly addresses Doc 56 P2 (transparent gating — players see what's unlocked + can return). Achievement system is parallel polish — could ship later. Gallery itself unlocks the most-shipped Frank capstones for replay. Slice now has 9+ capstones; the threshold has crossed.

**But LO's call:** gallery is meaningful authoring lift (~10-15 hours). If priority is more NEW content vs polish, defer.

### LO decision

- [ ] **YES in slice (next pass)** — open gallery authoring; ~10-15 hours; opens replay value for 9 capstones
- [ ] **NO defer to Phase 2+** — capstones remain once-only-per-save; rely on save scumming for replay
- [ ] **NO scope-out entirely** — no gallery, no replay (matches RTS-Marcus-arc-feel)

---

## §5 — Decision 4: Cross-arc completed-scenes tracker (Doc 34 E10f)

### What it is

A global registry of which scenes Maya has unlocked, surfaced in the published catalog (Doc 13 §14 RTS Walkthrough equivalent). This is the BACKING DATA for the catalog UI (Doc 56 P2 future PRD).

### What it would change in the engine

- **New player trait:** `player.completed_scenes = [...]` — array of canvas IDs Maya has unlocked.
- **Auto-population:** every canvas with `gallery_flag = true` (or a `track_completion = true` field) adds its ID to the array on first fire.
- **Cross-canvas queries:** new predicates `has_completed_scene("scene_franks_bedroom_evening")` for gating downstream content on the unlock map.
- **Catalog UI consumption:** Doc 56 P2 future catalog UI iterates this array to show 🔓 Unlocked status per scene. Without the tracker, the UI has nothing to show.

### Ripple to current authoring

- **Per-canvas opt-in:** every canvas that should appear in the catalog needs `track_completion = true`. Slice has ~30 canvases the catalog cares about.
- **Backfill:** all existing capstones + ambients + activities need the flag set during the Doc 62 `guide` field backfill pass (same authoring touch — efficient combination).
- **Quest card synergy:** Doc 50 R1 quest cards point at capstones; the completed-scenes tracker shows which are 🔓 unlocked vs 🎯 active vs ✓ done. The tracker is the data source for the ✓ frame.

### Slice impact

- **Slice scope (current):** no tracker. Quests V2 cards track flag-state, but no canvas-level "you've seen this" record.
- **If LO opens tracker in slice:** ~3-4 hours engine + ~1-2 hours per-canvas opt-in flag during next slice pass.
- **If LO defers:** catalog UI can't ship. Player has no "everything I've unlocked" surface.

### Trigger point

When Doc 56 P2 catalog UI ships. The tracker is its prerequisite data layer. Without commit on the tracker, catalog UI is dead-end work.

### Recommendation

**ENI's argument: ship the tracker with Doc 62 backfill pass — single authoring touch covers both.**

Reasoning: this is enabling infrastructure, not content. Cost is small (3-4 hours engine + flag setting). Without it, catalog UI (the second half of Doc 56 P2 alignment) can never ship. The combined "Doc 62 guide field + tracker flag" backfill pass costs ~6-8 hours and lights up both surfaces.

**But LO's call:** if catalog UI is permanently out-of-scope (Doc 56 P2 deferral becomes permanent), the tracker is dead infrastructure. Don't build it.

### LO decision

- [ ] **YES in slice (with Doc 62 backfill)** — ship tracker + flag canvases during backfill; lights up catalog UI prerequisite
- [ ] **YES but Phase 2+** — defer until catalog UI is greenlit; ship together
- [ ] **NO defer entirely** — catalog UI permanently out-of-scope; tracker unnecessary

---

## §6 — Cross-decision dependencies

| If you commit... | Then... |
|---|---|
| Pregnancy (§2) | All new sex content must remain bareback-compatible; reveal capstone authoring opens; father-attribution system needed |
| Scandal (§3) | Diana awareness either generalizes OR runs parallel; public-lewd canvases need scandal_effects; Phase 3+ town content gets meaning |
| Gallery (§4) | Per-canvas gallery_flag authoring; scene rendering gracefully handles replay mode |
| Tracker (§5) | Per-canvas track_completion flag; catalog UI prerequisite met |

**Combinations to consider:**
- **Gallery + Tracker together** — natural pair. Both per-canvas opt-in flags; both add catalog-UI-relevant data. Build together if either is in scope.
- **Pregnancy + Scandal** — independent but conceptually linked (Diana finds out Maya is pregnant → scandal spike). Build pregnancy first; scandal benefits from pregnancy as a feed source.
- **Tracker + Catalog UI** — strict prerequisite chain. Tracker first (this PRD §5), catalog UI later (Doc 56 P2 future PRD).

---

## §7 — Recommendation rollup (LO's call to confirm or override)

| Decision | ENI recommendation | Lift if YES |
|---|---|---|
| Pregnancy retrofit (§2) | **Defer to Phase 2+** | 5-10 hours |
| Scandal/reputation (§3) | **Defer to Phase 3+ town content** | 2-3 hours engine + retroactive ambient effects |
| Gallery + achievements (§4) | **Ship Phase 2 (next slice pass)** | 10-15 hours |
| Cross-arc tracker (§5) | **Ship with Doc 62 backfill** | 3-4 hours engine + per-canvas flag |

**My honest read:** the highest-leverage Phase 2+ commit is the tracker (§5) — it's the cheapest, it lights up the catalog UI surface (Doc 56 P2 alignment), and the per-canvas authoring touch combines naturally with Doc 62's guide field backfill. The gallery (§4) is next because it unlocks 9+ existing capstones for replay value. Pregnancy + scandal are honest Phase 2+/3+ defers.

**But the decisions are yours.** Each rolls into different parts of the slice's emotional/narrative weight.

---

## §8 — Trigger-point reminders (per Doc 56 §9 doctrine)

Per Doc 56 §9: *"don't pre-commit to engine scope; build engine when an authoring gap forces it."* The four trigger points where deferred decisions become urgent:

1. **Pregnancy** — first scene where pregnancy state should change downstream content (sleepover variant, reveal capstone, Diana finding out)
2. **Scandal** — first town-NPC canvas that gates on Maya's reputation (Phase 3+ village content)
3. **Gallery** — when slice has 9+ once-only capstones players want to replay (TRIGGER HAS ARRIVED — slice currently has this count)
4. **Tracker** — when catalog UI is greenlit OR Doc 50 R1 audits start tracking "which capstones have fired vs been unlocked"

Each can be deferred indefinitely with explicit holding-pattern commits (bareback authoring, per-NPC awareness, no replay, no catalog). The trigger is the moment the holding pattern stops being sufficient.

---

## §9 — Open questions for LO

In addition to the 4 main decisions above, surface these adjacent calls:

- **Doc 56 P2 catalog UI in scope?** Implicitly depends on tracker (§5). If catalog UI is permanently deferred, tracker drops.
- **Doc 30 §7.5 vocabulary ceiling — Ryan + Jake Stage 3+ commit timing.** Per Doc 58 §4 and Doc 59 §4 vocabulary ceiling, slice defers Stage 3+ for both Ryan and Jake. Phase 2+ when Stage 3+ ships — does it ship before or after pregnancy/scandal/gallery?
- **Diana Open Q #3 (Doc 60 §4) — 4-branch confrontation.** Blocks Diana brief completion. Phase 2+ resolution timing affects whether brought_in → cuckold register opens in slice.
- **Cookie Phase 3+ trigger (Doc 61 §6).** When does Cookie get a real brief? Tied to lesbian initiation arc greenlight.

These are all PHASE 2+ DECISIONS too — but each has its own narrative shape that LO can call independently of the 4 engine systems above.

---

## §10 — References

### Sibling and ancestor docs

- **Doc 13** — Road to Success Reference (gallery, pregnancy, walkthrough catalog precedents)
- **Doc 30** — TLS Test Redesign PRD (§7.3.1 pregnancy-compatibility commit; §6 Diana arc that scandal generalizes)
- **Doc 34** — Engine PRD Phase E Additions (original E10a-f spec sheet)
- **Doc 35** — RTS State Variant + Authored vs Mechanism (state-variant routing pattern for pregnancy variants)
- **Doc 56** — RTS Principles & TLS Alignment Doctrine (§9 open questions; P2 catalog future PRD; principle "don't pre-commit engine scope")
- **Doc 60** — Diana Design Brief (Open Q #3 blocker, ties to scandal scope)
- **Doc 62** — Canvas guide field PRD (backfill combines with §5 tracker flag)
- **Doc 63** — Validator Extension PRD (future R7 validator extension once tracker ships)

### Memory entries

- `doc-56-rts-alignment-doctrine`
- `rts_state_variant_authored_vs_mechanism` (state-variant pattern relevant to pregnancy)
- `feedback_tls_scene_body_style` (Tier-3 register applies to reveal capstones)

### Live engine references

- `player.pregnancy.*` schema — partially shipped in engine (verified from bathroom hub TOML)
- `setup.isPregnant()` predicate — exists in v1.py
- `setup.galleryMode` — RTS pattern; not yet in TLS engine
- `npc_diana.awareness` trait — currently the cross-NPC social-consequence tracker

### Doctrine principle

Doc 56 §9: *"don't pre-commit to engine scope; build engine when an authoring gap forces it."*
