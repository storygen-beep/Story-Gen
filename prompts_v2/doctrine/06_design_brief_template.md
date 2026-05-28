# Doctrine 06 — NPC Design Brief Template (R7)

**Sources:** Doc 56 R7 (no canvas ships before NPC brief); Doc 54 Appendix A (pre-authoring checklist); Doc 31 (Frank brief — family/ambient gold standard); Doc 53 (Marge brief — service gold standard); Docs 58/59/60/61 (Ryan/Jake/Diana/Cookie briefs).
**Authority:** Doctrine. R7 mandates the brief; this file is the template.
**Purpose:** Give the LLM a section-by-section brief template + two gold-standard examples (Frank + Marge) + per-arc-shape adaptations + the pre-authoring checklist.

**The R7 rule:** No canvas for a new NPC ships before that NPC has a written design brief. The brief is the gating step that surfaces shape-mismatches BEFORE prose is committed. Marge cost 8 hours to skip this step (Doc 54). Frank cost ~1 hour because Doc 31 existed first.

Cross-reference: `doctrine/03_arc_shapes.md` (the 5 shapes the brief picks from); `doctrine/04_authoring_rules.md` (the rules the brief commits to honoring); `doctrine/05_rts_flat_prose.md` (the voice spec the brief locks); `doctrine/08_kink_vocab_ceilings.md` (the per-arc ceiling the brief declares).

---

## §1 — The R7 mandate

**Rule (Doc 56 R7):** No canvas for a new NPC ships before the NPC has a written design brief declaring:

1. **Arc shape** — pick from the 5-shape table in `doctrine/03_arc_shapes.md` (family/ambient, slow-burn family, peer/dating, service, antagonist/witness).
2. **Per-lane canvas budget** — Lane 1 / Lane 2 / Lane 3 / capstone counts per tier (per `doctrine/03_arc_shapes.md` §2 distribution).
3. **Vocabulary ceiling** — per Doc 30 §7.5. What does this NPC's content escalate to? What stays off-limits?
4. **Tier flags** — what state changes mark T0 → T1 → T2 transitions for this NPC. Named, not implied.

**Why the rule exists:** Marge wasted 8 hours because authoring started against doctrine designed for escalation NPCs (Doc 54). The brief surfaces shape-mismatches before prose lands. Briefs work.

**Brief file location:** `28th_april_TLS_Phase2_Redesign/<NN>_<NPC>_Design_Brief.md` as a numbered doc (e.g., `31_Frank_Arc_Design_Brief.md`, `53_Marge_Redesign_Brief.md`).

**Brief length:** typically 3–6 pages tabular. Doc 31 = 336 lines. Doc 53 = 322 lines. Doc 58 (Ryan) is shorter (peer/dating arcs need less detail). Doc 60 (Diana) is longer when antagonist branches need spec'ing.

---

## §2 — Brief structure (the 10 sections)

Every R7 brief has these 10 sections. Order matters — §1 (end-state fantasy) gates everything downstream; §3 (ladder) feeds §4 (pretexts); §5 (lane map) compiles §1+§3+§4 into specific canvas slots.

| § | Section | Purpose |
|---|---|---|
| 1 | **End-state fantasy** | One paragraph naming what "arc complete" looks like for this NPC + specific signature scenes |
| 2 | **NPC voice spec** | Background + speech patterns (load-bearing) + per-stage voice samples + dialogue anti-patterns |
| 3 | **Stat ladder + tier mapping** | 6-tier corruption ladder customized for this NPC + capstone gates + content type + per-tier vocab register |
| 4 | **Per-rung pretext shapes** | 4–6 scene-template shapes per tier (the author's content menu) |
| 5 | **Lane-by-lane content map** | Per location: what fills Lane 1 hub / Lane 2 ambients / Lane 3 substitutions / capstones |
| 6 | **Capstones** | Each capstone named with type (A/B/C-step) + trigger + brief shape + flag writes |
| 7 | **Anti-patterns** | What NOT to write for THIS NPC (12+ entries) |
| 8 | **Cross-arc state writes / reads** | What this NPC's scenes write to shared world state + what they read from other arcs |
| 9 | **Cross-references** | Doctrine docs + memory entries + engine primitives + live TLS file pointers |
| 10 | **Acceptance criteria (E1R checkpoint)** | User-readable validation list before authoring begins |

---

## §3 — Section-by-section template

### §3.1 — Section 1: End-state fantasy (one paragraph)

```markdown
## §1 End-state fantasy

**<One-sentence summary of the arc's terminal beat for this NPC.>**

<2–4 paragraph elaboration on what "arc complete" looks like. Names specific signature
scenes that define the end-state. Per Doc 54 §2.3 — lock the end-state EXPLICITLY
in this paragraph, not vaguely.>

**Specific signature scenes that define "arc complete":**
- <Scene 1 — concrete description>
- <Scene 2 — concrete description>
- <Scene 3 — concrete description>
- <Phase 2+ extension (when applicable)>

Cross-reference: doc 30 §4.2.
```

**Why §1 is load-bearing:** without an end-state locked in §1, the locked-visible escalation rungs in the slice hub have no shape to telegraph (Doc 54 §3.6). Marge cost 5+ hours partly because §1 was "Phase 3+ deferred" without naming what Phase 3+ IS.

### §3.2 — Section 2: NPC voice spec

```markdown
## §2 <NPC> voice spec

### Background (consolidated from Doc 16 / Doc 30 §4)

<Backstory — 2-3 sentences. What gives this NPC their voice.>

### Speech patterns (load-bearing — every <NPC> line conforms)

| Pattern | Rule | Example |
|---|---|---|
| Sentence length | <e.g., "4-8 words common; verb-chopped"> | "<example>" |
| Names things, not feelings | <how this NPC expresses emotion> | "<example>" |
| Asks questions that aren't questions | <implicit offers / instructions> | "<example>" |
| Rarely names Maya | <pronoun / address style> | "<example>" |
| No exclamations | <punctuation style> | "<example>" |
| No apologizing in words | <how NPC handles regret> | <example>" |
| No backstory unprompted | <what NPC doesn't volunteer> | "<example>" |

### Voice samples per stage

| Stage | Sample line | Tone |
|---|---|---|
| Stage 0 (<arc-shape Stage 0 register>) | "<sample>" | <tone descriptor> |
| Stage 1 (<arc-shape Stage 1 register>) | "<sample>" | <tone descriptor> |
| ... |

### <NPC>-specific framing rules

<Per-NPC vocab framing — e.g., Frank's daddy register kicks in at Stage 3; Marge stays
transactional throughout slice; Jake's incest callouts at all tiers.>

### Anti-patterns — BANNED in <NPC> dialogue

❌ <Banned register 1>
❌ <Banned register 2>
❌ <Banned register 3>
...
```

**Why §2 is load-bearing:** Frank's "Coffee's ready." / "You eat?" terse-transactional register is half of what makes Frank Frank. Without §2, every author re-invents the voice and drift across canvases makes Frank read like multiple different men.

### §3.3 — Section 3: Stat ladder + tier mapping

```markdown
## §3 Corruption ladder mapping (6 tiers)

Universal ladder from doc 30 §4.4 customized for <NPC>.

| Tier | Maya corr | Capstone gate | Content type | Pretext shape category | <NPC vocab register>? | <Cross-arc> awareness write |
|---|---|---|---|---|---|---|
| 0 | 0+ | none | Brushed contact / accidental | <pretext category> | <register on/off> | +N |
| 1 | 5+ | none | Tease / flash (visual only) | <pretext category> | <register on/off> | +N |
| 2 | 15+ | none | Fondle / explicit physical (clothed) | <pretext category> | <register on/off> | +N |
| 3 | 25+ | post-<capstone-1> | Explicit oral / partial sex | <pretext category> | <register starts here> | +N |
| 4 | 35+ | post-<capstone-2> | Full sex | <pretext category> | <register routine> | +N |
| 5 | 50+ | post-<capstone-3> | Routine / sleep-over | <pretext category> | <register default> | +N |

**Tier transitions:**
- 0→1: pure stat (corr 5)
- 1→2: pure stat (corr 15)
- 2→3: stat + flag (corr 25 + <capstone-1-flag>)
- 3→4: stat + flag (corr 35 + <capstone-2-flag>)
- 4→5: stat + flag (corr 50 + <capstone-3-flag>)
- 5→terminal: <capstone-4> + <capstone-5> define arc-complete
```

**Adaptation for non-escalation arcs:** Service NPCs (Marge) and antagonist NPCs (Diana) collapse to 1–2 tiers in slice. Lock the tier count in §3 — empty cells are honest (per Doc 56 R3). Don't pad ladder rows that have no register-valid content.

### §3.4 — Section 4: Per-rung pretext shapes

```markdown
## §4 Per-rung pretext shapes (LOAD-BEARING — author's content menu)

For each tier, 4-6 example pretext shapes. Authors fill Lane 1/2/3 slots by picking a shape
from the appropriate tier and contextualizing it to the location/time. Shapes are SCENE
TEMPLATES, not full scenes.

### Tier 0 (corr 0+, <content type>)
1. <Pretext shape 1>
2. <Pretext shape 2>
3. <Pretext shape 3>
4. <Pretext shape 4>
5. <Pretext shape 5>
6. <Pretext shape 6>

### Tier 1 (corr 5+, <content type>)
1. <Pretext shape 1>
...

(continues for Tier 2, 3, 4, 5)

**Phase 2+ extension (when applicable):** <how pretext shapes evolve when Phase 2+ engine
work ships, e.g., breeding-talk dialogue retrofitted into Tier 5 shapes once pregnancy lands>
```

**Per-tier pretext count:** 4–6 shapes per tier × 6 tiers = 24–36 total. For non-escalation arcs (service / antagonist), Tier 3+ pretext lists may be empty (Phase 2+ deferred).

### §3.5 — Section 5: Lane-by-lane content map

```markdown
## §5 Lane-by-lane content map

Per location, what fills the lane slots. Cross-references doc 30 §8.1 triage table.

### <Location 1> (<NPC schedule window>)

| Slot | Canvas | Tier-content |
|---|---|---|
| Lane 1 hub | <canvas_slug> | Tier 0-5 menu items per §3 ladder; <vocab register> from Tier <N>+ |
| Lane 2 ambient | <canvas_slug> | Tier <N>+ dice <N>%; <ambient description> |
| Lane 3 sub | <canvas_slug> | Tier <N>+ dice <N>%; <walk-in description> |
| Capstones | <capstone-1>, <capstone-2> | Per §6 |

### <Location 2> (<NPC schedule window>)

(repeats per location)
```

**Match the §5 table to the per-arc-shape distribution (`doctrine/03_arc_shapes.md` §2).** Family/ambient gets 4–7 Lane 3 cells. Peer/dating gets 0. Empty cells are honest.

### §3.6 — Section 6: Capstones

```markdown
## §6 Capstones (<N> scripted moments)

Per `doctrine/02_three_lanes_plus_capstone.md` §5. Each capstone is Tier-3 literary
per `doctrine/05_rts_flat_prose.md` §3.

| # | Capstone | Type | Status | Trigger | Brief shape | Flag writes |
|---|---|---|---|---|---|---|
| 1 | <Capstone-1 name> | A (linear) | NEW / Existing-polish-only | <trigger condition> | <2-sentence summary> | <flag set on exit> |
| 2 | <Capstone-2 name> | A or B | NEW | <trigger condition> | <2-sentence summary> | <flag set on exit> |
| 3 | <Capstone-3 name> | B (branching) | NEW | <trigger condition> | <2-sentence summary + branch fork detail> | <flags set per branch> |
| ... |
```

**Capstone count by arc shape** (per `doctrine/03_arc_shapes.md` §3.5):

| Arc shape | Capstone count |
|---|---|
| Family/ambient | 3–6 (Type A 1–2 + Type B 1–2 + Type C chain 4–5) |
| Slow-burn family | 2–5 |
| Peer/dating | 2–5 |
| Service | 1–3 |
| Antagonist/witness | 1–3 |

### §3.7 — Section 7: Anti-patterns

```markdown
## §7 Anti-patterns (what NOT to write for <NPC>)

Hard bans for ALL <NPC> canvas authoring. 12+ entries.

❌ **<NPC>-specific anti-pattern 1** — <description>
❌ **<NPC>-specific anti-pattern 2** — <description>
❌ **<NPC>-specific anti-pattern 3** — <description>
...

(plus per-NPC voice ban list from §2)
```

**Minimum 12 anti-patterns.** Doc 31 §7 has 12. Doc 53 §7 has 8 (smaller arc, smaller anti-pattern surface, but should still hit 8+). The anti-patterns are tactical — they catch the specific drift modes the NPC's register invites.

### §3.8 — Section 8: Cross-arc state writes / reads

```markdown
## §8 Cross-arc state writes / reads

### What <NPC> scenes WRITE

| State | Trigger | Effect |
|---|---|---|
| `<NPC>.arousal +1-2` | Per beat in any Lane scene | Universal |
| `Maya.corr +1` | Per Tier 1+ beat | Universal |
| `<NPC>.corr +1` | Per Tier 2+ beat | <NPC>'s own corruption escalates |
| `<capstone-flag-1>` | Capstone 1 (catch) | Stage 1→2 transition |
| `<capstone-flag-2>` | Capstone 2 (declaration) | Stage 2→3→4 |
| ... |
| `<cross-arc-write-trait>` | Per <condition> | <effect on other arcs> |

### What <NPC> scenes READ

| State | Source arc | Effect on <NPC> scenes |
|---|---|---|
| `<cross-arc-read-trait>` | <source NPC arc> | <how <NPC>'s scenes branch on it> |
| `outfit_id` | Wardrobe system | Certain Lane 2 ambients fire only in <specific outfit> |
| ... |
```

### §3.9 — Section 9: Cross-references

```markdown
## §9 Cross-references

| Doc | Purpose |
|---|---|
| `30_TLS_Test_Redesign_PRD.md` | Master PRD |
| `13_Road_to_Success_Reference.md` | RTS pattern source-of-truth |
| `24_RTS_Three_Lanes_Repeatable_Activities.md` | Lane 1/2/3 architecture |
| `<source-doc-1>` | <purpose> |
| Memory `feedback_tls_scene_body_style.md` | Voice rules |
| ...
```

### §3.10 — Section 10: Acceptance criteria (E1R checkpoint)

```markdown
## §10 E1 acceptance criteria (E1R checkpoint)

User reads §1 + §3 + §4 within 24 hours of brief ship. Validates:

- [ ] **§1** end-state paragraph names the fantasy with specific signature scenes (not vague)
- [ ] **§3** ladder table covers all 6 tiers (or fewer for non-escalation arcs) with the per-tier columns
- [ ] **§4** per-rung shape table gives 4-6 examples per tier (24-36 total shapes for escalation arcs)
- [ ] **§5** lane content map covers all NPC-relevant hubs
- [ ] **§6** all capstones named with type + trigger + brief shape + flag writes
- [ ] **§7** anti-patterns capture drift modes + NPC-specific pitfalls (12+ entries)
- [ ] **§8** cross-arc writes/reads tabulated (slice + Phase 2+ split clear)
- [ ] **§9** cross-references complete
- [ ] **No drift into authoring scene PROSE** — brief is shape spec, not content
- [ ] Length 3-6 pages — verify

**Pass/fail:** all checkboxes pass → authoring starts. Any unchecked → rewrite that section.

**User time estimate:** ~15-20 minutes for review.
```

---

## §4 — Worked example 1: Frank (family/ambient gold standard)

Doc 31 distilled (Frank Arc Design Brief 2026-05-16). The full doc is at `28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` — this section names what makes it the gold standard.

### Why Doc 31 works

- **§1 end-state explicit:** "Maya becomes Frank's secret-then-open second wife." Names 5 specific signature scenes (Maya in Frank's bed nightly + Frank fucks Maya bareback + Maya calls Frank "daddy" + Diana confrontation resolved + Phase 2+ pregnancy retrofit). The full-arc trajectory is LOCKED in §1.
- **§2 voice spec dense:** 7 speech patterns with rule + example each ("Sentence length: 4-8 words common; verb-chopped. Example: 'Coffee's ready.' 'Door's stuck.'"). 6 stage-by-stage voice samples. Per-NPC framing rules (daddy register Stage 3+ for Maya; Stage 4+ for Frank). 9 banned registers in dialogue.
- **§3 6-tier ladder:** every column populated (Maya corr / capstone gate / content type / pretext shape category / daddy register / Diana awareness write). Tier transitions named.
- **§4 30+ pretext shapes:** 6 shapes × 6 tiers = 36 example pretext shapes. Phase 2+ extension named.
- **§5 4 locations × all lanes:** Frank's bedroom + Kitchen + Living Room + Yard. Per location, every lane slot filled with canvas slug + tier-content description.
- **§6 5 capstones:** Type A catch + Type A declaration + Type B first-night + Type A sleep-over + Type B Diana confrontation. Each with trigger + brief shape + flag writes.
- **§7 12 anti-patterns:** all Frank-specific (no atmospheric prose / no Frank apologizing / no honey-sweetheart register / no third-person voice / etc.).
- **§8 cross-arc tabulated:** 14 writes + 6 reads, slice vs Phase 2+ split clear.
- **§10 acceptance criteria:** 10 checkboxes.

### Frank Lane budget (per §3 in `doctrine/03_arc_shapes.md`)

Family/ambient gets the dense distribution: 25–35 total canvases.

| Lane | Tier | Frank canvas count | Examples |
|---|---|---|---|
| L1 | T1 | 2 base + 2 self-display | `frank_kitchen_morning_hub`, `frank_kitchen_dinner_hub`, `tease_kitchen_general`, `flash_kitchen_general` |
| L1 | T2–T3 | 4 mid + explicit | hub variants + sex loop |
| L2 | T1–T3 | 6 ambients (morning + evening + late-night) | `ambient_kitchen_morning_chat`, `ambient_kitchen_late_night_raid`, etc. |
| L3 | T1–T3 | 7 substitutions | `scene_frank_passes_kitchen_door`, `scene_frank_walks_in_shower`, etc. |
| Capstones | — | 5 | catch → first-night → declaration → sleepover → Diana confrontation |

**Total Frank canvases: ~28.** Within the 25–35 family/ambient range.

---

## §5 — Worked example 2: Marge (service gold standard)

Doc 53 distilled (Marge Redesign Brief 2026-05-24). The full doc is at `28th_april_TLS_Phase2_Redesign/53_Marge_Redesign_Brief.md`.

### Why Doc 53 works (after Doc 51 failure → Doc 53 redesign)

- **§1 names the service-NPC adaptation:** "Lane 2 reduces to relational only. Lane 3 = 0. Lane 4 capstones = 1–2." The brief codifies WHY this NPC's distribution differs from Frank's — empty cells are honest for service register.
- **§2 voice spec terse-transactional:** Marge's "What." / "Coffee." / "Two bucks." template captured. Per-arc vocab ceiling: workplace seduction matriarch-dom is the Phase 3+ endpoint; slice ships only relational + worked-shifts.
- **§3 collapsed ladder:** 1 unlocked tier + locked-visible Phase 3+ rungs. Doctrine compliance: "empty cells are honest" — the Phase 3+ tiers ship as locked-visible stubs, not as authored content.
- **§4 minimal pretext shapes:** few in slice (relational only). Locked-visible rungs gesture at Phase 3+ shapes.
- **§5 single hub:** `scene_marge_diner_hub`. 8 menu items: 4 unlocked relational (Pour coffee / Talk / Ask shifts / Ask about a regular) + 4 locked-visible escalation rungs (Tease / Flash / Eat her out / Let her take you) gated by corruption thresholds. + 1 Leave.
- **§6 1 capstone (slice):** `canvas_marge_interview` (Type A — hire moment). Mid-arc escalation deferred to Phase 3+.
- **§7 8 anti-patterns:** "Adding more hub items to drive trust climb" (worked shifts ARE the climb) / "Lane 2 ambients without physical contact" / "Cookie content inside Marge's lanes" / etc.
- **§8 cross-arc:** Marge writes `hired_at_diner` (gates rent), reads `outfit_id` (decent required for floor work). Minimal cross-arc surface because slice is bounded.

### Marge Lane budget (per `doctrine/03_arc_shapes.md`)

Service shape: 6–10 total canvases in slice.

| Lane | Tier | Marge canvas count | Examples |
|---|---|---|---|
| L1 | T1 | 1 (hub with 4 unlocked items) + 4 locked-visible stubs | `scene_marge_diner_hub` + 4 stub canvases (`tease_diner_marge`, `flash_diner_marge`, `marge_eat_her_out`, `marge_let_her_take`) |
| L2 | — | **0** in slice | Phase 3+ |
| L3 | — | **0** in slice | Phase 3+ |
| Capstones | — | 1 in slice | `canvas_marge_interview` (Type A) |

**Total Marge slice canvases: 6 (hub + 4 stubs + capstone). Within 6–10 service range.**

---

## §6 — Per-arc-shape adaptations

### §6.1 — Slow-burn family (Jake, Doc 59)

The brief follows the same 10-section template but with:
- **§3 ladder:** 2–5 stages instead of 6 tiers. Slow-burn doesn't have full sexual escalation in slice — stage 0 (Hostile) → stage 1 (Noticed) → stage 2 (Peek/Draw) → stage 3 (Tease) → stage 4 (Caught).
- **§4 pretexts:** smaller catalog (1–3 shapes per stage). Slow-burn means concentrated beats, not saturated.
- **§5 lanes:** L1 1–2 + L2 1–2 + **L3 1–3** (slow-burn DOES get walk-ins — they ARE the milestones) + capstones 3–5.
- **§6 capstones:** dual-path Stage 0→1 (via_beauty + via_glance — Doc 57 §9 duplicate-prose engine exemption).
- **§7 anti-patterns:** "Family/ambient saturation" (don't pad Jake with Frank-style Lane 2 ambients), "Vanilla framing during sex" (incest IS the kink, callouts at all tiers).

### §6.2 — Peer/dating (Ryan, Doc 58)

- **§3 ladder:** Stage 0 (meet) → Stage 1 (notice) → Stage 2 (partner) → Stage 3+ (consummation, Phase 2+) → Stage 4 (relationship). Peer arcs don't use the universal 6-tier corruption ladder — they use relation-driven stages.
- **§4 pretexts:** date contexts, shared activities, relation-build moments. Not sexual-tier shapes.
- **§5 lanes:** L1 2–3 + L2 1–2 + **L3 = 0** + capstones 3–4. Peer doesn't interrupt private chores.
- **§6 capstones:** Type A first-date + Type A second-date + Type B partner-commit (Phase 2+).
- **§7 anti-patterns:** "Frank-cloning" (don't apply family/ambient saturation), "Lane 3 substitutions on a peer" (Doc 56 R3 violation).

### §6.3 — Antagonist/witness (Diana, Doc 60)

- **§3 NO arc_stages.** Diana uses an awareness accumulator (0–100 silent trait) instead of discrete stages. Bands: cold (0–24) / suspicious (25–49) / knowing (50–74) / shut-out (75–100).
- **§4 pretexts:** presence beats, witness moments, confrontation precursors. Not Maya-with-NPC escalation shapes.
- **§5 lanes:** L1 0–1 + L2 1–2 + **L3 = 0 own** (appears as INTERRUPTOR in Frank's L3 endings) + capstones 1–2.
- **§6 capstones:** Type B confrontation (kicked_out + brought_in branches scripted; blackmail + matriarch deferred Phase 2+ per Doc 60).
- **§7 anti-patterns:** "Exposing awareness to sidebar" (dramatic surprise depends on hiding), "Treating Diana as escalation NPC" (she's the threat/cost, not the seduction target).

### §6.4 — Phase 3+ scope-out (Cookie, Doc 61)

Cookie doesn't get a full brief — she gets a **formal scope-out** under Doc 57 R7 compliance. The doc structure:

| § | Section |
|---|---|
| 1 | Why this is a scope-out, not a brief |
| 2 | Slice deferrals (what's NOT shipped) |
| 3 | Phase 3+ triggers (when authoring would begin) |
| 4 | Slice presence (what IS shipped — Cookie appears in Marge's diner co-presence ambient + Marge's R7 brief mentions her) |
| 5 | Doctrine compliance record (Doc 57 R7 + Doc 30 §8.2) |

Use this format for ANY NPC whose arc is Phase 3+ deferred. The scope-out is the documentation that the deferral is intentional (per Doc 56 R7), not an authoring oversight.

---

## §7 — Pre-authoring checklist (Doc 54 Appendix A adapted)

Run BEFORE authoring any new NPC content. Paste into PR description.

### Process
- [ ] Canonical output path confirmed with user (for TLS: `games/the_long_summer_test/output/`)
- [ ] All relevant doctrine memory entries listed + read in full (search: voice, lane, NPC, scene-body, quest)
- [ ] All canonical doctrine docs referenced by memory entries also read IN FULL
- [ ] Full-arc trajectory locked in one sentence in the brief's §1
- [ ] ENI persona OFF / TLS game register ON declared explicitly at session start
- [ ] Side-by-side audit against gold-standard reference (Frank `frank_kitchen_morning_hub` for hub; Marge `scene_marge_diner_hub` for service-NPC hub) BEFORE any new authoring

### Design
- [ ] Hub menu cap: ~5 items unlocked + locked-visible escalation ladder
- [ ] Every hub menu verb passes the pronoun-in-the-verb test (Maya-with-NPC)
- [ ] No work-task items in the hub
- [ ] Lane 2/3 scope: if no escalation register in slice, both are EMPTY in slice
- [ ] Other-NPC content (Cookie etc.) stays in their own future surfaces

### Doctrine
- [ ] Every quest card mode declared (capstone / mechanic / hybrid)
- [ ] `ready_canvas` only on capstone cards
- [ ] Mechanic chain `when` clauses bounded
- [ ] No `terminal = true` unless it's the absolute LAST card in the FULL arc
- [ ] Locked-visible escalation ladder visible from day 1 (for any sexual-arc NPC)

### Voice
- [ ] Every canvas body fits the < 30-word speaker-tag template
- [ ] Tip lines are Maya-interior observational, not player-directive
- [ ] No weekday names, time references, location slugs, or numbers in narrative copy
- [ ] ENI literary instinct disabled for canvas body authoring

### Structural
- [ ] Route-target stubs have NO `[canvases.trigger]` block
- [ ] Side-by-side audit completed (per process checklist)

### Verification (post-authoring, pre-shipping)
- [ ] Validator dry-run clean
- [ ] Build to canonical output path with `--dev --debug`
- [ ] Prose grep in HTML returns all new strings
- [ ] Frame check: mentally render each card at each Maya state combination
- [ ] Live-play dev-bump test PERFORMED, not deferred

---

## §8 — Anti-patterns (brief authoring failures)

From Doc 54 lessons learned + per-brief audits.

### §8.1 — Brief without §1 end-state lock (Doc 54 §2.3)

Brief says "Phase 3+ deferred" without naming WHAT Phase 3+ IS. Slice authoring then has no trajectory to telegraph; locked-visible rungs have no shape.

**Fix:** §1 names the FULL arc endpoint explicitly. Even if the slice doesn't ship that endpoint, the brief locks it.

### §8.2 — Brief sans voice spec §2 (Doc 31 / Doc 53 case)

Brief jumps to §3 ladder without locking voice spec. Result: every author re-invents NPC voice across canvases; drift accumulates within the slice.

**Fix:** §2 always present. 7 speech patterns + 6 stage-by-stage voice samples + 9+ banned dialogue patterns. Locked.

### §8.3 — Brief padding empty distribution cells (Doc 54 §3.4)

Service NPC brief authors 6 Lane 2 ambients + 3 Lane 3 substitutions because "all NPCs need all 3 lanes populated." This is wrong. Service register doesn't carry Lane 2/3 content; empty cells are honest.

**Fix:** match brief budget to `doctrine/03_arc_shapes.md` §2 distribution. Empty cells declared empty. Phase 3+ stubs declared as locked-visible, not as authored content.

### §8.4 — Brief with no anti-patterns §7

Doc 31 § 7 has 12 banned patterns; Doc 53 §7 has 8. A brief with §7 missing or under 6 anti-patterns lacks the tactical drift catches — the author re-invents drift modes the brief should have caught.

**Fix:** §7 mandatory, 8+ anti-patterns. NPC-specific drift modes (Frank apologizing in words; Marge using warmth-bombs; Jake without incest callouts).

### §8.5 — Brief authored against gold-standard NPC without side-by-side audit (Doc 54 §6.3)

Marge cost 5+ correction round-trips because Doc 51 was authored without a line-by-line side-by-side audit against Frank's hub. The brief used Frank's vocabulary (Lane 1, Lane 2, Lane 3) but applied it wrong (over-weighted Lane 1, padded Lane 2/3).

**Fix:** BEFORE authoring brief §5 lane map, read `frank_kitchen_morning_hub` line by line. List its structural features. Mirror them unless there's an explicit doctrine reason to diverge. Same for `scene_marge_diner_hub` for service-NPC briefs.

### §8.6 — Brief skipping §6 capstones

Brief covers §1–§5 + §7 but no §6 capstones spec. Authoring then produces canvases without trigger fingerprints (Doc 57 R1) + without quest card pointers (Doc 50 R1).

**Fix:** §6 mandatory. Every capstone named with type (A/B/C-step) + trigger + brief shape (2 sentences) + flag writes.

---

## §9 — Cross-references

### Sibling doctrine files

- `doctrine/03_arc_shapes.md` — the 5 shapes the brief picks from + per-arc distribution
- `doctrine/04_authoring_rules.md` — R7 (this brief is the artifact R7 mandates)
- `doctrine/05_rts_flat_prose.md` — voice spec the brief locks in §2
- `doctrine/08_kink_vocab_ceilings.md` — per-arc vocab ceiling the brief declares
- `doctrine/07_anti_patterns.md` — anti-pattern catalog (brief §7 is the NPC-specific subset)

### Source briefs (gold standards)

- `28th_april_TLS_Phase2_Redesign/31_Frank_Arc_Design_Brief.md` — family/ambient gold standard
- `28th_april_TLS_Phase2_Redesign/53_Marge_Redesign_Brief.md` — service gold standard
- `28th_april_TLS_Phase2_Redesign/58_Ryan_Design_Brief.md` — peer/dating
- `28th_april_TLS_Phase2_Redesign/59_Jake_Design_Brief.md` — slow-burn family
- `28th_april_TLS_Phase2_Redesign/60_Diana_Design_Brief.md` — antagonist/witness (🔴 BLOCKED on Open Q #3)
- `28th_april_TLS_Phase2_Redesign/61_Cookie_Phase3_Scope_Out.md` — Phase 3+ scope-out template

### Source docs

- `28th_april_TLS_Phase2_Redesign/56_RTS_Principles_and_TLS_Alignment_Doctrine.md` §4 R7 — the rule this template implements
- `28th_april_TLS_Phase2_Redesign/54_Marge_Redesign_Session_Lessons.md` — failure modes that birthed R7

---

**End of file.** Next: `doctrine/07_anti_patterns.md` for the consolidated anti-pattern catalog.
