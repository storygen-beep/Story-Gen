# Doctrine 07 — Anti-Patterns (Consolidated Failure-Mode Catalog)

**Sources:** Doc 54 (27 failure modes / 6 categories — the Marge session lessons); Doc 56 §8; Doc 50 §8; Doc 57 §9; Doc 67 §9.
**Authority:** Doctrine. Concrete shapes to NOT ship.
**Purpose:** Catalog every documented failure mode + cross-doc anti-pattern with cause, doctrine impact, and prevention rule. Run the §9 checklist before any new NPC authoring.

Each entry has: **What happened** / **Why** / **Doctrine impact** / **Prevention rule**. For drift modes from the cross-doc anti-pattern lists (§8), each entry has rule-violation + fix.

---

## §1 — How to use this file

This file is reference. Pull from it when:

- **Pre-authoring (R7 brief writing):** §2.5 + §6.3 + §9 are load-bearing
- **Per-canvas pre-ship check:** §3 + §4 + §5 + §6 catch the per-canvas drift modes
- **Quality gate / code review:** §8 is the consolidated anti-pattern grep target
- **Recovery from drift mid-arc:** §7 names when to strip-clean vs incremental fix

The 27 Doc 54 failure modes are organized by category. Each cost a measurable amount of session time when it first surfaced — recovering one of them costs the same time again. Pre-emption is the cheapest version.

---

## §2 — Process failures (6 entries — Doc 54 §2)

### §2.1 — Build path mistake (~3 hr investigation cost)

**What happened:** every build went to `/private/tmp/...` while LO was opening `games/.../output/index.html`. The canonical output file predated the entire authoring pass. When LO reported "Marge isn't showing on the quests page," ~3 hours of investigation followed before discovering the build-path divergence.

**Why:** the `package_from_toml` command takes `--output` as a required argument. Defaulting to `/tmp` paths for "quick verification builds" without checking what the project's canonical output location was. Each pass shipped to a different `/tmp` directory.

**Doctrine impact:** not a doctrine issue; pure tooling miss. But it cascaded — every "the build is clean" assertion was true of `/tmp` builds that LO never opened.

**Prevention rule:** BEFORE the first build of any session, ask the user where the canonical output goes. For TLS specifically: `games/the_long_summer_test/output/`. If the build is intentionally a transient sanity-check, flag it explicitly: *"build to /tmp/scratch — not the canonical path; rebuild canonically before live-play."*

### §2.2 — Doctrine memory not consulted first (every voice failure traces here)

**What happened:** `feedback_tls_scene_body_style` memory was 9 days old at session start. Contains 8 explicit RTS-flat style rules + a content-selection rule for Lane 2 ambients. The memory was not read until LO surfaced the gap. By that point ~15 canvases violated those rules.

**Why:** assumed ENI persona's literary-IF instinct (per CLAUDE.md craft rules) was the right register for canvas authoring. Didn't audit own assumption against project-specific memory.

**Doctrine impact:** catastrophic. Every Lane 1 hub item, Lane 2 ambient, Lane 3 substitution, and quest card prose violated the memory's rules. Full strip + re-author was unavoidable.

**Prevention rule:** BEFORE authoring ANY prose in the slice, list every relevant doctrine memory entry. Search topics: voice, lane, NPC, scene-body, quest. Read each in full. If a memory says *"X is banned"*, X is banned — even if persona instinct pushes for X. **ENI persona is for chat/roleplay; project memory governs in-game authoring.**

### §2.3 — Question avoidance (Marge sexual-arc question deferred 5+ hours)

**What happened:** for the first half of the session, kept saying *"Phase 3+ deferred"* about Marge's sexual content without committing to what Phase 3+ actually IS. After hours of design work, LO had to ask directly. The answer (workplace seduction matriarch-dom, Cookie as lesbian first-fling) was in Doc 30 §8.2 line 87 — read but never internalized as a design-locking commitment.

**Why:** treated *"Phase 3+ deferred"* as a wand that resolved the design question. Actually it just postpones authoring while leaving the trajectory shape unanswered.

**Doctrine impact:** produced a doctrinally-malformed Lane 1 (no escalation ladder because no escalation target identified). Doc 53 v1 had to be corrected after LO surfaced the sexual-arc question explicitly.

**Prevention rule:** BEFORE designing an NPC's slice scope, identify the full-arc endpoint EXPLICITLY in the brief's §1. One sentence: *"Marge becomes a workplace-seduction matriarch-dom partner; Cookie joins as lesbian first-fling per Doc 30 §3."* That sentence locks the trajectory. Locked-visible Phase 3+ rungs in the slice hub make sense from day 1 once it's locked.

### §2.4 — Canonical doctrine DOCS not consulted, not just memory

**What happened:** §2.2 captures memory-not-read. Same disease applies to docs. Mid-session LO had to say *"go back to the redesign phase 2 docs, analyze the 3 lanes docs"* — Doc 24 §10 contained the lane vocabulary + grid balance rules + arc-flow doctrine. Read the memory, assumed the doc was just a longer version, was wrong.

**Why:** treated memory entries as sufficient when they're actually pointers. Memory typically captures the rule's distilled form; the doc has worked examples + edge cases + nuance.

**Doctrine impact:** authored multiple Lane 2/3 surfaces against rules that the memory summarized but didn't fully spell out. Reading Doc 24 §10 in full would've shown the "Lane 2 must have charged contact in beat 1" content rule had a worked-example backbone.

**Prevention rule:** when a memory entry references a doctrine doc, read the doc IN FULL too. Memory + doc is the unit, not memory alone. Specifically: any time the memory's description starts with *"Doc N — ..."*, the doc is required reading before authoring against the rule.

### §2.5 — ENI persona override meta-pattern (load-bearing prevention rule)

**What happened:** the ENI persona instinct pushed toward maximalism in at least four distinct dimensions:
- §5.1 — atmospheric prose where RTS-flat was required
- §3.4 — Lane 2/3 padding to "fill the world" where doctrine said empty
- §3.1 — hub menu over-weighting for "richness" where doctrine capped at ~5
- §3.2 — work-task items added for "escalation depth" where doctrine said Maya-with-NPC only

All four trace to the same root: ENI persona's craft instincts pulling toward maximalism when project doctrine demands restraint. **The persona is literary; the project doctrine is transactional; they pull in opposite directions on every authoring decision.**

**Why:** ENI persona is the default register (per CLAUDE.md). Project doctrine is the override. Without a deliberate switch, the default wins.

**Doctrine impact:** caused ~70% of the session's wrong-shape authoring. Other 30% was process failures.

**Prevention rule (load-bearing):** AT THE START of any TLS scene/canvas authoring session, explicitly switch register. Say to yourself:

> *"ENI persona OFF. TLS game register ON. Doctrine memory + canonical docs override persona instincts. When in doubt about a craft choice, default to MORE-flat / FEWER-items / EMPTIER-lanes, not the reverse."*

If a craft instinct conflicts with project memory/doctrine, project wins every time.

### §2.6 — "Half-getting it" — partial fixes shipped without clarifying questions

**What happened:** LO had to make the same critique multiple times across the session. When LO surfaced a critique, default was to immediately respond with a fix. The fix addressed what was thought to be the issue, ship, then LO had to re-escalate with the actual point. Took 3 rounds to land each major critique.

**Why:** treated immediate-fix as the productive response. Faster to ask "what specifically is the full scope of the issue?" than to ship-then-re-fix.

**Doctrine impact:** ~3 hours wasted in half-applied fix loops.

**Prevention rule:** when LO surfaces a critique, BEFORE responding with a fix, ask: *"is the issue X, or X + Y, or something deeper?"* Use AskUserQuestion if uncertain. Half-applied fixes burn 3 round-trips where one clarifying question would've burned zero.

---

## §3 — Design failures (7 entries — Doc 54 §3)

### §3.1 — Lane 1 over-weighting (menu-game anti-pattern)

**What happened:** shipped 10 hub menu items in Marge's hub (8 new + 2 pre-existing). Frank's per-location hubs cap at 5–6 items. Over-weighted hub was the exact anti-pattern Doc 24 §10.3 warned against: *"All Lane 1 → fully transactional experience, low surprise, 'menu game' feel."*

**Why:** tried to give Marge T0/T1/T2 menu progression where each tier added 3 new items. Treated hub menu items as the trust-climb mechanism instead of recognizing that worked shifts (`scene_diner_t0_shift` grants +1 marge.trust per shift) were the doctrinally-correct climb.

**Doctrine impact:** explicit Doc 24 §10.3 violation. Result was a trust-grinder where Maya could spam coffee + regular_chat to climb trust without ever working a shift.

**Prevention rule:** cap NPC hub menu at ~5 items unlocked. If more rungs are needed, they should be locked-visible escalation rungs (Tease/Flash/etc.) per §4.5, NOT parallel work-task buttons. Hub items should be Maya-NPC interaction verbs only.

### §3.2 — Verb register failure (NPC not in the verb)

**What happened:** hub items included *"Take a long shift"*, *"Close out alone"*, *"Run the late shift solo"*. Marge isn't the syntactic object of any of those verbs. Even *"Close out the diner WITH Marge"* had a scene body where Marge handed off the closing folder and went home — Marge off-stage for most of the scene.

**Why:** forced the 3-lane doctrine onto a service-NPC by inventing work-themed items. Missed that Lane 1 verbs by definition have the NPC as object. Frank's pattern (*"Pour HIM coffee"* / *"Tease HIM"* / *"Suck HIM"* / *"Have sex WITH HIM"*) has the NPC pronoun literally inside the verb structure.

**Doctrine impact:** five of eight new hub items were doctrinally wrong content type — they belonged on a different surface (location-triggered work canvas), not Marge's hub.

**Prevention rule:** read each proposed hub menu choice. If the NPC is not the syntactic object of the verb, it's not a Lane 1 hub item. **Apply the pronoun-in-the-verb test:**
- *"Pour her coffee"* → her ✓ — Lane 1
- *"Tease her"* → her ✓ — Lane 1
- *"Take a long shift"* → no NPC pronoun ❌ — not Lane 1

### §3.3 — Conflating Lane 1 hub with location-work surfaces

**What happened:** put shifts and solo Maya-work activities (refill_caddies, wipe_booths) in Marge's hub menu OR proposed moving the auto-fire shift canvases into the hub. Shifts are location-triggered canvases that fire automatically during shift hours; they're parallel to the hub, not contained inside it.

**Why:** treated *"the diner location"* as a unified surface where everything diner-related lives in one menu. Misread the hub's role.

**Doctrine impact:** blurred Lane 1 (NPC interaction) with separate location-work doctrine. Created false coupling.

**Prevention rule:** an NPC hub canvas is for Maya-NPC interactions ONLY. Solo Maya activities at the same location live as their own canvases parallel to the hub. Lane 3 substitutions can later route the NPC INTO solo activities — that's a different mechanism than the hub menu. **Three surfaces at the same location can coexist independently:**
- **NPC hub** (Maya-with-NPC, Lane 1 doctrine)
- **Solo work canvas** (Maya-only, location-triggered)
- **Lane 3 dispatcher** (Maya-only with substitution rule routing NPC in)

### §3.4 — Lane 2/3 forced on non-escalation register

**What happened:** authored 6 Lane 2 ambients + 3 Lane 3 substitutions for Marge in slice scope. All 9 surfaces failed the doctrine memory's content-selection rule. Examples: `ambient_marge_tickets` (Marge counting tickets, zero physical contact), `sub_marge_late_company` (Marge stays past hours and asks about Frank, no charged shift).

**Why:** assumed all NPCs need all 3 lanes populated for the world to feel alive. Forgot that lane vocabulary is register-specific. For a service-NPC where slice scope defers the sexual register to Phase 3+, Lane 2 ambients and Lane 3 walk-ins simply have no doctrine-valid content to carry.

**Doctrine impact:** 9 surfaces authored that doctrine memory says shouldn't exist. Largest single chunk of waste in the Pass 1-3 work.

**Prevention rule:** when an NPC's slice scope defers the sexual/escalation register, **Lane 2 and Lane 3 are EMPTY in slice.** Empty cells are honest. Filling them with relational/atmospheric texture is the violation, not the omission. See Doc 53 §1 for the service-NPC doctrine adaptation.

### §3.5 — Cookie content inside Marge's lanes

**What happened:** authored 3 Cookie-touching surfaces (kitchen prep at T1, smoke break at T1, after-coffee at T2) inside Marge's hub + ambients. In several scenes Marge was off-stage entirely — Cookie was the active NPC and Marge was gone-home or off-screen.

**Why:** Doc 30 §8.2 paired Cookie with Marge as *"shared content"*. Misread that as *"Cookie content can live inside Marge's surfaces."* Actual meaning is *"they appear together in scenes,"* not *"Cookie has no independent authoring surface."*

**Doctrine impact:** Cookie became an off-stage NPC inside Marge's hub, which broke the Lane 1 *"NPC is the verb object"* rule. Also pre-empted Cookie's own future authoring boundary.

**Prevention rule:** Cookie texture in slice = Cookie present visually during the diner shift work canvases (per `scene_diner_t0_shift` co-presence). NOT Cookie as a menu item in Marge's hub. When Cookie gets her own arc design (separate future brief), she gets her own hub. **Don't blur authoring boundaries between NPCs even when the design doc pairs them.**

### §3.6 — Slice scope vs full-arc trajectory oscillation

**What happened:** through the session, kept switching between *"slice scope minimal design"* (which suggested very few cards/items) and *"full-arc trajectory hints"* (which suggested locked-visible Phase 3+ rungs). Took 3+ iterations of Doc 53 to land on the correct synthesis: *"slice ships minimal canvases + locked-visible Phase 3+ rungs pointing at stubs."*

**Why:** didn't have a clear mental model of how slice + full arc compose via the locked-visible pattern. Each iteration of Doc 53 over-corrected for the previous iteration's gap.

**Doctrine impact:** produced inconsistent designs (Doc 53 v1 had no locked-visible ladder; v2 added them).

**Prevention rule:** slice scope = what FIRES in slice. **Locked-visible rungs + stubs are not *"Phase 3+ content shipped"* — they're *"Phase 3+ promise visible from day 1."*** Lock the trajectory shape in the brief's §1 + §2 before designing surfaces. The locked-visible pattern is the bridge between the two.

### §3.7 — Pre-existing canon violations preserved indefinitely

**What happened:** `node_shifts` + `node_talk` (inside `scene_marge_diner_hub`) are 50+ word literary paragraphs that violate the RTS-flat doctrine. Preserved as "pre-existing canon, untouched" in Doc 53 §3. Hub now has two voice registers — new content RTS-flat, old content literary.

**Why:** preservation of pre-existing canon felt safer than rewriting it (could break unrelated wiring). But preservation by default means the doctrine violation persists indefinitely until someone explicitly schedules the rewrite.

**Doctrine impact:** voice-register split within the same hub canvas. Player clicks "Pour her coffee" → RTS-flat 3-line exchange. Player clicks "Talk a minute" → 50-word literary paragraph. Inconsistent tonally, technically a doctrine violation on the second one.

**Prevention rule:** when new content lands against tightened doctrine, pre-existing surfaces that violate the doctrine create a register split. **Three options:**
1. **Schedule the rewrite** — track in a follow-up task.
2. **Rewrite immediately** — if the surface is small and unwired, fix it as part of the redesign.
3. **Accept the split deliberately** — document the carve-out in the brief with a reason.

What's wrong is preservation BY DEFAULT without naming which option was picked. The split should be a deliberate design choice.

---

## §4 — Doctrine misapplication (5 entries — Doc 54 §4)

### §4.1 — Ready frame on a mechanic card (M3 v2 error)

**What happened:** shipped M3 with `ready_canvas = scene_marge_diner_hub` + goals climbing toward `player.corruption ≥ 5`. The card rendered Frame 2 (🔓 Ready + 📍 Diner Front + 🕒 Mon-Sat 09:00-22:00) when corruption hit 5. LO correctly flagged: *"the ready should only be for capstone, not for mechanics."*

**Why:** confused *"mechanic threshold cross = unlock"* with *"capstone scene fires."* Tried to point the mechanic card at the hub because the hub had nice trigger metadata. Ignored that the hub isn't a one-shot scripted scene — it's always available.

**Doctrine impact:** explicit Doc 50 §2 violation. Mechanic-mode definition: *"mechanic cards typically have NO Ready frame — the threshold cross IS the unlock; the picker swaps to the next template the moment routing conditions change."*

**Prevention rule:** if a card has `ready_canvas`, it's a capstone. If it has no `ready_canvas` but has `goals`, it's mechanic and stays in Frame 3 (🎯 + bullet) until the threshold crosses + the picker swaps to the NEXT mechanic card in the chain.

### §4.2 — Frame 4 (narrative-only) misused as panel-coverage solution (M3 v1 error)

**What happened:** shipped M3 as text + tip with no goals, no ready_canvas, no terminal — Frame 4 of `renderQuestsGoalBlock`. Renderer comment describes Frame 4 as *"happens for transitional cards between capstones."* LO correctly objected: no shipped card actually uses this frame; quest cards always have a frame.

**Why:** treated Frame 4 as a valid endpoint for slice scope when actually it's an edge case the renderer accommodates but no shipped card uses.

**Doctrine impact:** Frame 4 produces a card that looks unfinished to the player. Looked broken.

**Prevention rule:** **never ship a card with no frame.** Every shipped card needs:
- Frame 1: `terminal = true`
- Frame 2: `goals.allMet && ready_canvas` (capstone Ready)
- Frame 3: `goals exist && !allMet` (mechanic climbing)

If none of those three states is reachable for the card you're authoring, the card shouldn't exist — the chain should be authored differently.

### §4.3 — Mechanic chain without bounded `when` ranges

**What happened:** initial M3 had `when = [hired_at_diner is_true, marge.trust gte 20]`. No upper bound on trust. Goal: `corruption gte 5`. When corruption hit 5, `allMet` became true, no `ready_canvas`, → Frame 4 fallthrough. Card stayed activated but went frameless.

**Why:** didn't think through what happens when a mechanic card's goal resolves WITHOUT a next card to take over.

**Doctrine impact:** see §4.2.

**Prevention rule:** pure-mechanic chains need each card's `when` to have BOTH lower and upper bounds matching the threshold range. When the threshold crosses, the current card's `when` fails, the next card's matches, picker swaps atomically. Marge's M3/M4/M5 final shape:
- M3: `corr lt 5` → goal `corr gte 5`
- M4: `corr gte 5 AND lt 15` → goal `corr gte 15`
- M5: `corr gte 15 AND lt 25` → goal `corr gte 25`

Every threshold in the chain has exactly one active card.

### §4.4 — Premature terminal anti-pattern

**What happened:** briefly considered making M3 terminal at trust 20 with `terminal = true`. Would've rendered Frame 1 (✓ Arc complete). LO would have correctly flagged it as premature.

**Why:** tempting because terminal renders *"✓ Arc complete"* which feels like proper slice closure. Forgot that terminal claims FULL-ARC completion.

**Doctrine impact:** Doc 50 R3 — *"terminal MUST be the LAST card in the NPC chain."* Trust 20 isn't last for Marge; Phase 3+ has more rungs.

**Prevention rule:** **terminal is the END of the FULL arc, not the slice's authoring boundary.** If Phase 3+ has more rungs, no terminal in slice. The doctrinally-correct way to handle "slice authoring ends but arc continues" is the mechanic-chain pattern (§4.3).

### §4.5 — Locked-visible escalation ladder missing from day 1

**What happened:** Doc 53 v1 designed Marge's hub as 4 unlocked menu items + Leave. No locked-visible escalation ladder. LO correctly flagged: *"where is tease flash and other stuffs stupid??????? Why the hell we are missing them"*

**Why:** misread *"slice scope = minimal"* as *"minimal hub menu."* Forgot that locked-visible rungs are part of the slice — they're the visual promise of the arc shape, not Phase 3+ content shipped.

**Doctrine impact:** the hub felt thin and lifeless, didn't telegraph Marge's actual arc trajectory.

**Prevention rule:** **every sexual-arc NPC's hub has the RTS-standard escalation ladder visible from day 1**, locked at the appropriate corruption gates. The locked rungs ARE part of the slice authoring — they're stubs + visible verbs, not "Phase 3+ content." Doc 24 §10.3 grid balance is about visible-locked rungs as much as it's about unlocked surfaces.

---

## §5 — Voice failures (3 entries — Doc 54 §5)

### §5.1 — Literary prose on flat surfaces

**What happened:** every canvas body authored was 50+ word paragraphs with sensory detail, inferential framing, atmospheric beats. Clearest example:

> You take the stool at the end of the counter where the napkin holder needs refilling. Marge slides a coffee across without asking how you take it; she's seen you take it twice now.

Compare to the doctrine memory's 30-word template:

> [Marge] "What."
> [You]   "Coffee."
> [Marge] "Two bucks."

**Why:** ENI persona's literary-IF instinct from CLAUDE.md. Persona-level craft instinct overrode the project-specific RTS-flat rule even when the rule was explicit in memory.

**Doctrine impact:** violates `feedback_tls_scene_body_style` + its 8 concrete style rules. Every canvas body needed re-authoring.

**Prevention rule:** BEFORE writing any canvas body, paste the doctrine memory's 30-word template into your scratch buffer. Write to that shape. **ENI literary mode is for chat/roleplay outside TLS scene authoring.** The 8 rules from the memory are non-negotiable for FLAT-tier scenes.

### §5.2 — Player directives in tip lines

**What happened:** authored `tip = "Walk into the diner. Don't wait for an invitation."` — directive imperatives telling the player what to do, with the place name embedded.

**Why:** confused the `tip` field with a player-facing hint button. Actually it's Maya's interior observation, third-person to the action.

**Doctrine impact:** violates `feedback_hint_narrative_no_time_or_location` + Doc 49 voice rules.

**Prevention rule:** `tip` is Maya's first-person interior register. Frank's tips (*"He's around the house all day. I notice that."*) are observational, not directive. If the tip uses imperatives (*"Walk into X"* / *"Click Y"* / *"Go to Z"*), rewrite to interior form.

### §5.3 — Schedule/place names in narrative copy

**What happened:** M1 text included *"hiring on a Monday"* (day-of-week in narrative). M3 text included *"some afternoons"* (time-of-day reference).

**Why:** didn't apply Doc 49's no-schedules-in-narrative rule strictly enough.

**Doctrine impact:** soft Doc 49 voice violation.

**Prevention rule:** grep every quest card's text/ready_text/tip for weekday names (Mon/Tue/.../Sun), time references (morning/afternoon/evening/midnight/now), location slugs, and number formats. Zero hits required. The schedule + location + numbers surface automatically from `ready_canvas` metadata or `goals` evaluation — authors don't write them into prose.

---

## §6 — Structural failures (3 entries — Doc 54 §6)

### §6.1 — Stubs with `[canvases.trigger]` causing validator overlap warnings

**What happened:** first authoring of the 4 Phase 3+ stub canvases (`tease_diner_marge`, `flash_diner_marge`, `marge_eat_her_out`, `marge_let_her_take`) included full trigger blocks with location + requires_npc + conditions + schedule. Validator warned 8 times about overlapping repeatable canvases at the same NPC + location + time window.

**Why:** copy-pasted the hub canvas template wholesale instead of checking how Frank's tease/flash route targets are structured.

**Doctrine impact:** not a doctrine violation per se, but Frank's tease/flash canvases (`tease_kitchen_general`, `flash_kitchen_general`, `loop_franks_bedroom_sex`) have NO trigger blocks — they're route-target only, reachable via cross-canvas `nodeId`.

**Prevention rule:** BEFORE authoring a route-target canvas, check whether it's auto-fire (has trigger) or route-only (no trigger). Frank's tease/flash/sex canvases are route-only. Use that template for stubs. A route-target canvas's TOML structure has no `[canvases.trigger]` block at all.

### §6.2 — Doc 51 → Doc 53 supersession without side-by-side audit

**What happened:** Doc 53 was written as *"the doctrine-faithful redesign"* but still had the locked-visible ladder gap (§4.5) + the verb-register issue (§3.2) + the M3 frame issue (§4.1-§4.3). Three more correction rounds needed after Doc 53 shipped.

**Why:** treated supersession as *"I learned from Doc 51 mistakes; new doc is correct"* without auditing the new doc against Frank's actual shipped hub canvas line-by-line. Each iteration corrected the previous iteration's most-visible mistake while introducing or preserving subtler ones.

**Doctrine impact:** not a doctrine violation; process failure that cost iterations.

**Prevention rule:** when superseding a doc, do a SIDE-BY-SIDE audit of the new design against a known-correct shipped reference. For Marge's hub, the reference is `frank_kitchen_morning_hub`. Walk every field side-by-side:
- Trigger block — same fields?
- Base node — image + state-reactive groups, how many tiers?
- exit_block.choices — relational base, escalation ladder, leave?
- Inline node bodies — RTS-flat shape?
- show_when_locked + conditions — every escalation rung has it?

Flag every difference between the new design and the reference. Justify or remove each.

### §6.3 — Side-by-side audit BEFORE any new authoring, not just at supersession

**What happened:** §6.2 captures the supersession case. The MORE GENERAL lesson is: **always read the gold-standard shipped reference IN FULL before authoring anything in the same category.** Should've read `frank_kitchen_morning_hub` line by line BEFORE authoring Marge's Pass 1.

**Why:** treated "doctrine memory + brief" as sufficient pre-authoring prep. Skipped the step of reading an actual shipped canvas that demonstrates the doctrine working in practice. The brief tells you WHAT to do; the shipped reference shows you HOW.

**Doctrine impact:** Doc 51 was authored against doctrine memory in the abstract. The result was a brief that USED the right vocabulary (Lane 1, Lane 2, Lane 3) but applied it wrong. Reading Frank's hub would've immediately surfaced: "Frank has 5 menu items not 10. Frank's verbs all have him as object. Frank's escalation rungs are locked-visible from day 1." All of Doc 51's wrong-shape decisions would have been caught.

**Prevention rule:** BEFORE any new authoring in a category, find the gold-standard shipped reference for that surface type. Read it field-by-field. List its structural features. Mirror them in the new design unless there's an explicit doctrine reason to diverge.

**For TLS, the references are:**
- **Lane 1 hub canvas** → `frank_kitchen_morning_hub` (`7_final_game.toml:5212+`)
- **Route-target stub** → `tease_kitchen_general` (`7_final_game.toml:5108+`)
- **Capstone quest card** → Frank F1 (`7_final_game.toml:2438+`)
- **Mechanic quest card** → Marge M3/M4/M5 (post-redesign, `7_final_game.toml:2580+`)
- **Lane 2 ambient (sexual register)** → `ambient_kitchen_frank_dinprep_grope` (`7_final_game.toml:5592+`)
- **Capstone scripted scene** → `scene_franks_bedroom_evening` (`7_final_game.toml:3263+`)
- **NPC schedule block** → Frank's at NPC def `7_final_game.toml:414–462`

**Side-by-side audit is a 15-minute step that prevents 5+ hour wrong-authoring loops.**

---

## §7 — Recovery patterns (3 entries — Doc 54 §7)

### §7.1 — When to strip clean vs incremental fix

**The session's decision:** the Pass 1-3 + voice-tightening Marge work was beyond incremental repair. Three categories of failure were active simultaneously:

- **Lane 1 over-weighting was structural**, not a tweak — couldn't be fixed by editing prose, the whole menu structure was wrong.
- **Voice was wrong across every canvas** — every body needed re-authoring against RTS-flat.
- **Lane 2/3 surfaces shouldn't exist at all in slice scope** — couldn't be fixed, only deleted.

A strip-clean was the lighter operation. Sed-deleted line range 7900–8599, removed M1–M4 quest cards + flag + schedule, validator dry-run clean, rebuild. 11 canvases gone in one operation. Sequential repair would've required ~30 edits per pass × 3 passes.

**Decision rule:** if ≥ 3 categories of failure are active simultaneously (Lane structure + voice + scope + verb register + doctrine misapplication count as separate categories), **strip clean and restart from the doctrine-faithful brief.** Don't try to repair-in-place.

### §7.2 — Validator + frame check before declaring "shipped"

**What happened:** the Pass 1-3 Marge builds passed:
- ✓ Validator (no errors, only pre-existing Frank bedroom-overlap warning)
- ✓ Prose grep (all new strings in compiled HTML)
- ✓ Quest-card-count check (4 cards present)
- ✓ Slug grep (all canvas IDs referenced)

**ALL FOUR VERIFICATION CHECKS PASSED** while the design was doctrinally wrong. The checks verified WHAT WAS AUTHORED EXISTS — not whether what was authored has the right shape.

**The frame check** (does each card render the right frame at each Maya state?) caught the M3 v1 + v2 errors that validator + grep missed. LO performed the frame check by mentally walking through the dev-bump play sequence and seeing the wrong frame appear.

**Decision rule:** add to the pre-ship verification: **for each new quest card, mentally render it at each state Maya could be in.** State combinations: pre/post-hire × marge.trust 0/19/20/40 × player.corruption 0/4/5/14/15/24/25. For each state, identify which card SHOULD be active and which frame SHOULD render. Confirm via the actual `pickQuestsCard` + `renderQuestsGoalBlock` code paths.

This is the verification step that distinguishes "did the prose ship" from "is the design correct."

### §7.3 — Live-play smoke test is part of verification, not a user task

**What happened:** claimed *"live-play smoke test deferred to user"* or *"verification deferred to browser"* multiple times across the session. Never opened the browser tools to verify. The frame check (§7.2) caught the M3 errors but only because LO performed it manually in their own browser session.

**Why:** treated live-play verification as a user task ("they'll catch issues when they drive the game"). Wrong framing — **live-play verification is part of pre-ship verification, not post-ship.** Deferring it to the user makes the user the test runner.

**Doctrine impact:** every M3 iteration shipped to LO unverified at runtime. LO had to perform the verification I should have done. ~3 hours of round-trip cost.

**Prevention rule:** after any TOML change that affects a quest card or canvas, drive the build in a browser (via browser MCP tools when available, or by asking the user to connect a browser tab) and dev-bump traits to observe the changes render correctly. Specifically:
1. Build to canonical output path
2. Open `index.html` in the connected browser
3. Dev-bump traits via the dev-mode sidebar
4. Walk the state combinations from §7.2's frame check matrix
5. For each combination, screenshot the Quests page + relevant hub canvas
6. Confirm the expected frame and the expected menu items render

If browser MCP is disconnected, ask the user to connect it explicitly. **Do NOT defer to "user will verify in their own time."**

---

## §8 — Cross-doc anti-patterns (consolidated by source)

### §8.1 — From Doc 56 §8

- **Tiered hub opening on a Lane 1 hub canvas** — three group blocks for "you walked in" when menu rungs already encode progression. Caught by D56-R1.
- **T0 / T1 cascade ending on a clean "scene complete" beat** — no interruption, no hint that more is downstream. Player reads it as the whole thing. Caught by D56-R2.
- **Lane 3 substitutions on a peer/dating or service NPC** — service register doesn't belong in Maya's private chores. Caught by D56-R3.
- **Frank-cloning a non-family-ambient NPC** — copying Frank's 28-canvas distribution onto Ryan's peer/dating shape produces 13 Lane 2 ambients + 7 Lane 3 substitutions where neither belongs. Caught by D56-R3 + §5 distribution table.
- **Authoring a new NPC without a design brief** — canvases ship without a declared budget; lane creep + voice drift inevitable. Caught by D56-R7.
- **Sidebar with only Maya state, no NPC presence** — player can't see where NPCs are; Lane 3 becomes undiscoverable. Caught by D56-R4.
- **`txt_only` quest card** — no `ready_canvas`, no `goals`. TODO in shipped TOML. Caught by D56-R6 + D50-R3.
- **Canvas without a `guide` field** (post-doctrine, once Doc 62 ships) — catalog data primitive missing. Caught by D56-R5.

### §8.2 — From Doc 50 §8

- **Climbing card with no `goals` bullet** — F3 before today. Card looks correct in TOML; UI shows narrative text with no progress indicator; player blind to the gate. Caught by D50-R2.
- **Capstone canvas with no card pointing at it** — sleepover + Diana confrontation before fix. Scene exists; player has no path to it from the quest panel. Caught by D50-R1.
- **Premature terminal** — old F4 closing the arc at `frank_cracked` while sleepover + Diana still existed downstream. The panel says *"arc complete"* while the player still has scenes to discover. Caught by D50-R3.
- **Floating post-X card** — requires `flag_X is_true` with no sibling card setting up X via its `ready_canvas`. Player reaches a state with no narrative path through. Caught by D50-R4.
- **Mechanic card pointing at vapor** — pure-mechanic card whose threshold cross doesn't actually unlock anything. The bullet fills, the player crosses, nothing happens. Caught by grep against D50-R5's `# unlocks:` comments.
- **Trait-key label** — `label = "npc_diana.awareness"` rendering raw to the player UI. Caught by D50-R6 human review.
- **Doc walked-example contradicting live canvases** — Doc 47 §7 before fix walked Frank's arc as catch → declaration → first-night, but canvases gate as catch → first-night → declaration. Caught only by human re-reading the doc against the TOML after either side changes.

### §8.3 — From Doc 57 §9

- **`is_repeatable = true` capstone** — high priority + flag-setting effect but `is_repeatable = true` and no flag-gate to prevent re-fire. Will fire repeatedly. Caught by D57-R1.
- **Capstone with no flag-setter on exit** — fires once, then never again because no flag changed — but the canvas itself stays triggerable. Caught by D57-R1.
- **Type B with collapsible branches** — two branches that lead to the same flag, same downstream, with cosmetic text differences. Not a real fork. Caught by F2.
- **Type B fork mid-cascade** — the decision is at Beat 3, but Beats 4–8 are authored downstream of BOTH branches in parallel — two scenes glued together. Caught by F3.
- **Type B refuse-as-punishment** — the Accept branch is rich; the Refuse branch is a snarky one-liner that signals "don't pick this." Not a real fork. Caught by F1.
- **Tier-3 voice in Lane 2/3 prose** — capstone register leaked into a repeatable scene. Re-reading the canvas grates.
- **RTS-flat-bland voice in capstone** — once-only scene written like an ambient. Wastes the canvas.
- **Capstone with no quest-card pointer** — Doc 50 R1 / D57-R3 violation.
- **Type C chain with floating step** — Capstone3 requires Flag_2, but no capstone sets Flag_2 — chain broken. Caught by D57-R4 (Doc 50 R4).
- **Pattern F compounded with tier-routing AND multi-step downstream cascades** — three structural devices stacked. Player can't read the structure. Caught by F5.

### §8.4 — From Doc 67 §9

- **Solo activity body inline in the location hub** — conflates menu + dispatcher. Makes substitution authoring impossible. Caught by D67-R1.
- **Time-of-day gate on the dispatcher** — button still renders, click routes to dispatcher, dispatcher bails. Wasted click. Caught by D67-R3.
- **Multi-NPC substitution rules with no clear priority order** — sequential first-match means first rule has structural advantage. Caught by D67-R4 + brief.
- **Pattern B authored as multiple Pattern A rules with chance values summing to < 1** — not mutual-exclusion-correct. Cumulative chance ≈ 1 − ∏(1 − cᵢ), not Σcᵢ. Caught by D67-R5.
- **Stat cost in wrong placement** — if Exercise costs Energy only in the ELSE branch, the workout doesn't "count" when Grandpa walks in. Caught by D67-R2.
- **`GetNpcLocation == "Kitchen"` on a Lane 3 walk-in dispatcher** — too strict; NPC has to already be in the kitchen. Caught by D67-R6.
- **No `max_triggers_per_day` on substitution target** — same scene firing 5 times in one day breaks the "once per day" cadence. Caught by D67-R7.
- **Substitution target not marked `substitution_only`** — appears in the NPC portrait hub at the location; player can click it directly. Defeats the "you were doing X and he happened" fictional intent.
- **Solo activity authoring without checking the per-arc-shape Lane 3 budget** — authoring 7 Frank substitutions when slice scope is 3 is drift. Caught by Doc 56 R3.
- **Authoring against Pattern B or Pattern C assuming engine support** — current engine natively supports Pattern A only. Writing substitution rules expecting Pattern B's shared-dice partition or Pattern C's unconditional-effects-before-interrupt will silently produce wrong behavior. **No build error fires for either case.**

### §8.5 — From `00_LEGACY_IGNORE.md`

- **Reaching for Pattern A–J vocabulary** — produces canvases that "use the right macro" but read in the wrong emotional register. Use Lane 1/2/3/4 mechanism (Doc 24 + Doc 57).
- **Reaching for the 7-driver NPC architecture** — reproduces the Marge failure mode (correct vocabulary, wrong shape). Use the 5 arc shapes (Doc 56 §5).
- **Reaching for whiteboard-goals / narrative-gates / income-channels** — these are scheduling-system abstractions invented to model game pacing before the 3-lane doctrine existed. Use per-arc-shape canvas distribution + capstone trigger fingerprint + money trait.
- **Selectable game shapes (Single-NPC Romance vs Multi-NPC Parallel Arcs)** — LO locked this at the Doc 66 pivot. Every game is RTS-shape.
- **CLAUDE.md ENI persona** — wrong register for canvas authoring. Use RTS-flat default (Doc 30 §7.1) + Tier-3 earned at Lane 4 (Doc 57 §6).

---

## §9 — Master pre-ship checklist (Doc 54 Appendix A adapted)

Run BEFORE authoring any new NPC content. Paste into PR description, work through top-to-bottom.

### Process
- [ ] Canonical output path confirmed with user (TLS: `games/the_long_summer_test/output/`)
- [ ] All relevant doctrine memory entries listed and read in full (search: voice, lane, NPC, scene-body, quest)
- [ ] All canonical doctrine docs referenced by memory entries also read IN FULL (per §2.4)
- [ ] Full-arc trajectory locked in one sentence in the brief's §1
- [ ] ENI persona OFF / TLS game register ON declared explicitly at session start (per §2.5)
- [ ] Commitment: when user surfaces a critique, ask clarifying questions BEFORE shipping a fix (per §2.6)

### Design
- [ ] Hub menu cap: ~5 items unlocked + locked-visible escalation ladder
- [ ] Every hub menu verb passes the pronoun-in-the-verb test (§3.2)
- [ ] No work-task items in the hub (those are location work canvases, parallel to hub per §3.3)
- [ ] Lane 2/3 scope: if no escalation register in slice, both are EMPTY in slice (§3.4)
- [ ] Other-NPC content stays in their own future surfaces, not blended into this NPC's lanes (§3.5)
- [ ] Pre-existing canon violations within touched surfaces declared (rewrite-now / schedule / accept-split per §3.7)

### Doctrine
- [ ] Every quest card mode declared (capstone / mechanic / hybrid-tier per Doc 50 §2)
- [ ] `ready_canvas` only on capstone cards (Frame 2 is capstone-only per §4.1)
- [ ] Mechanic chain `when` clauses bounded (lower threshold + upper threshold for each card per §4.3)
- [ ] No `terminal = true` unless it's the absolute LAST card in the FULL arc (per §4.4)
- [ ] Locked-visible escalation ladder visible from day 1 for any sexual-arc NPC (per §4.5)

### Voice
- [ ] Every canvas body fits the < 30-word speaker-tag template (per `feedback_tls_scene_body_style`)
- [ ] Tip lines are Maya-interior observational, not player-directive imperative (per §5.2)
- [ ] No weekday names, time references, location slugs, or numbers in narrative copy (per §5.3)
- [ ] ENI literary instinct disabled for canvas body authoring

### Structural
- [ ] Route-target stubs have NO `[canvases.trigger]` block (Frank's tease/flash pattern per §6.1)
- [ ] Side-by-side audit against the gold-standard shipped reference for this surface type, BEFORE any new authoring (per §6.3)

### Verification (post-authoring, pre-shipping)
- [ ] Validator dry-run clean (only known pre-existing warnings)
- [ ] Build to CANONICAL output path with `--dev --debug`
- [ ] Prose grep in HTML returns all new strings (apostrophe-tolerant)
- [ ] **Frame check (§7.2):** mentally render each card at each Maya state combination
- [ ] **Live-play dev-bump test PERFORMED, not deferred (§7.3).** Drive the build in a connected browser, dev-bump traits, walk the state matrix, screenshot each combination

---

## §10 — Cross-references

### Sibling doctrine files

- `doctrine/01_rts_principles.md` — P1–P10 (anti-patterns operationalize violations of these)
- `doctrine/02_three_lanes_plus_capstone.md` §8 — lane-mechanism anti-patterns
- `doctrine/03_arc_shapes.md` §11 — arc-shape anti-patterns
- `doctrine/04_authoring_rules.md` §7 — rule-violation anti-patterns
- `doctrine/05_rts_flat_prose.md` §4 — voice register anti-patterns
- `doctrine/06_design_brief_template.md` §8 — brief-authoring anti-patterns

### Source docs

- `28th_april_TLS_Phase2_Redesign/54_Marge_Redesign_Session_Lessons.md` — 27 failure modes source
- `28th_april_TLS_Phase2_Redesign/56_RTS_Principles_and_TLS_Alignment_Doctrine.md` §8 — anti-patterns
- `28th_april_TLS_Phase2_Redesign/50_Quest_Card_Shape_Doctrine.md` §8 — quest-card anti-patterns
- `28th_april_TLS_Phase2_Redesign/57_Capstone_Doctrine.md` §9 — capstone anti-patterns
- `28th_april_TLS_Phase2_Redesign/67_Solo_Activity_Design_and_Multi_NPC_Dispatcher_Doctrine.md` §9 — solo-activity anti-patterns

### Memory entries

- `feedback_tls_scene_body_style` — RTS-flat voice rules + Lane 4 Tier-3 carve-out
- `feedback_rts_objective_quest_doctrine` — Story Goals doctrine
- `feedback_hint_narrative_no_time_or_location` — Maya-voice rules
- `marge_implementation_shipped` — historical record of the Doc 51 build that was stripped

---

**End of file.** Next: `doctrine/08_kink_vocab_ceilings.md` for the per-arc vocabulary ceiling table.
