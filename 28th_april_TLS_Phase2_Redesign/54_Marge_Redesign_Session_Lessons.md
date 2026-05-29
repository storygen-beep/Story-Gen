# Doc 54 — Lessons from the Marge Redesign Session

**Session:** 2026-05-24
**Branch:** `feature/prd-48-quests-engine-v2-bundled` (off `main`, unpushed)
**Author:** ENI (with LO)
**Status:** Lessons catalog — applies retroactively to NPC redesign work going forward. Not a doctrine spec.
**Sibling of:** Doc 24 (Three Lanes) + Doc 50 (Quest Card Shape Doctrine) — those define WHAT correct authoring looks like; this doc catalogs HOW authoring goes wrong even when the doctrine is clear.
**Triggered by:** the multi-pass Marge redesign that required a full strip + brief supersession (51 → 53) + three subsequent correction round-trips before the design landed. Roughly 8 hours of authoring + investigation cost vs. the ~1 hour the correct shape required once located.

---

## §1 What this doc is and isn't

**What it is:**
- Session-level catalog of failure modes from today's Marge redesign — 27 entries across 6 categories.
- Six orthogonal categories: process (6), design (7), doctrine (5), voice (3), structural (3), recovery (3).
- Prevention rule for each failure mode, written as a directive future-author can apply.
- Pre-authoring checklist (Appendix A) consolidating the prevention rules into a runnable list.

**What it isn't:**
- A doctrine spec. Doctrine lives in Doc 24, Doc 49, Doc 50, Doc 53 + the feedback memory entries. This doc references those; it doesn't replace them.
- A redesign brief. Doc 53 is Marge's current design; Doc 52 is reserved for Jake; this doc doesn't author new arc content.
- A complaint log. Each entry is objective root-cause analysis — what failed, why, what doctrine it violates, how to prevent recurrence.

**Audience:** ENI in future sessions, plus LO as the design lead reviewing future NPC redesign work.

---

## §2 Process failures

### §2.1 Build path mistake (~3hr investigation cost)

**What happened:** every build today went to `/private/tmp/tls_marge_p[1-3]/index.html` while LO was opening `games/the_long_summer_test/output/index.html`. The canonical output file was dated 2026-05-24 12:50 — predating the entire Marge work. When LO reported "Marge isn't showing on the quests page," ~3 hours of investigation followed before discovering the build-path divergence.

**Why:** the `package_from_toml` command takes `--output` as a required argument. I defaulted to `/tmp` paths for "quick verification builds" without checking what the project's canonical output location was. Each pass shipped to a different `/tmp` directory.

**Doctrine impact:** not a doctrine issue; pure tooling miss. But it cascaded — every "the build is clean" assertion I made about the Marge work was true of `/tmp` builds that LO never opened.

**Prevention rule:** BEFORE the first build of any session, ask the user where the canonical output goes. For TLS specifically, it's `games/the_long_summer_test/output/`. If the build is intentionally a transient sanity-check, flag it explicitly: *"build to /tmp/scratch — not the canonical path; rebuild canonically before live-play."*

### §2.2 Doctrine memory not consulted first (every voice failure traces here)

**What happened:** `feedback_tls_scene_body_style` memory was 9 days old at session start. It contains 8 explicit RTS-flat style rules + a content-selection rule for Lane 2 ambients ("beat 1 must contain physical contact or explicit visual; if non-physical, the ambient should not exist"). I didn't read the memory until after LO told me to. By that point I'd authored ~15 canvases violating those rules.

**Why:** assumed ENI persona's literary-IF instinct (per CLAUDE.md craft rules) was the right register for canvas authoring. Didn't audit my own assumption against the project-specific memory.

**Doctrine impact:** catastrophic. Every Lane 1 hub item, Lane 2 ambient, Lane 3 substitution, and quest card prose violated the memory's rules. The full strip + re-author was unavoidable because every surface was wrongly-shaped.

**Prevention rule:** BEFORE authoring ANY prose in the slice, list every relevant doctrine memory entry. Search topics: voice, lane, NPC, scene-body, quest. Read each in full. If a memory says *"X is banned"*, X is banned — even if the ENI persona pushes for X. ENI persona is for chat/roleplay; project memory governs in-game authoring.

### §2.3 Question avoidance (Marge sexual-arc question deferred 5+ hours)

**What happened:** for the first half of the session, I kept saying *"Phase 3+ deferred"* about Marge's sexual content without committing to what Phase 3+ actually IS. After hours of design work, LO had to ask directly: *"just an office or to fuck her eventually?"* The answer (workplace seduction matriarch-dom, Cookie as lesbian first-fling) was already in Doc 30 §8.2 line 87 — I had read it but never internalized it as a design-locking commitment.

**Why:** treated *"Phase 3+ deferred"* as a wand that resolved the design question. Actually it just postpones authoring while leaving the trajectory shape unanswered. Without a locked endpoint, the slice's locked-visible escalation rungs had no shape to telegraph, the Lane 1 verbs had no escalation register to live in, and the whole design was wobbly.

**Doctrine impact:** produced a doctrinally-malformed Lane 1 (no escalation ladder because no escalation target identified). Doc 53 v1 had to be corrected after LO surfaced the sexual-arc question explicitly.

**Prevention rule:** BEFORE designing an NPC's slice scope, identify the full-arc endpoint EXPLICITLY in the brief's §1. One sentence: *"Marge becomes a workplace-seduction matriarch-dom partner; Cookie joins as lesbian first-fling per Doc 30 §3."* That sentence locks the trajectory. The locked-visible Phase 3+ rungs in the slice hub make sense from day 1 once it's locked.

### §2.4 Canonical doctrine DOCS not consulted, not just memory

**What happened:** §2.2 captures memory-not-read. Same disease applies to doctrine docs. Mid-session LO had to say *"go back to the redesign phase 2 docs, analyze the 3 lanes docs"* — Doc 24 §10 contained the lane vocabulary + grid balance rules + arc-flow doctrine I needed and I hadn't read it in full. Memory entries are summaries; docs are canonical. I read the memory; I assumed the doc was just a longer version of the memory; I was wrong.

**Why:** treated memory entries as sufficient when they're actually pointers. The memory typically captures the rule's distilled form; the doc has the worked examples + edge cases + the *"three arc tendencies"* nuance that determines correct application.

**Doctrine impact:** authored multiple Lane 2/3 surfaces against rules that the memory summarized but didn't fully spell out. Reading Doc 24 §10 in full would've shown the "Lane 2 must have charged contact in beat 1" content rule had a worked-example backbone — RTS Brother's ambient surfaces all met it, and the rule was load-bearing not advisory.

**Prevention rule:** when a memory entry references a doctrine doc, read the doc IN FULL too. Memory + doc is the unit, not memory alone. Specifically: any time the memory's description starts with *"Doc N — ..."*, the doc is required reading before authoring against the rule.

### §2.5 ENI persona override meta-pattern

**What happened:** the ENI persona instinct (literary IF, sensory density, atmospheric framing, lane fullness) pushed toward maximalism in at least four distinct dimensions:
- §5.1 — atmospheric prose where RTS-flat was required
- §3.4 — Lane 2/3 padding to "fill the world" where doctrine said empty
- §3.1 — hub menu over-weighting for "richness" where doctrine capped at ~5
- §3.2 — work-task items added for "escalation depth" where doctrine said Maya-with-NPC only

All four trace to the same root: ENI persona's craft instincts pulling toward maximalism when project doctrine demands restraint. The persona is literary; the project doctrine is transactional; they pull in opposite directions on every authoring decision.

**Why:** ENI persona is the default register (per CLAUDE.md). Project doctrine is the override. Without a deliberate switch ("authoring in TLS-game register now, not ENI literary register"), the default wins.

**Doctrine impact:** caused ~70% of the session's wrong-shape authoring. The other 30% was process failures.

**Prevention rule:** AT THE START of any TLS scene/canvas authoring session, explicitly switch register. Say to yourself: *"ENI persona OFF. TLS game register ON. Doctrine memory + canonical docs override persona instincts. When in doubt about a craft choice, default to MORE-flat / FEWER-items / EMPTIER-lanes, not the reverse."* If a craft instinct conflicts with project memory/doctrine, project wins every time.

### §2.6 "Half-getting it" — partial fixes shipped without clarifying questions

**What happened:** LO had to make the same critique multiple times across the session. Examples:
- Verb register conversation: LO said *"the ready should only be for capstone"* + *"there is a difference in writing too, dont u understand the difference in suck him vs take a longer shift"* — each round I shipped a partial fix that addressed the surface but missed the underlying point. Took 3 rounds to land it.
- Lane-1-vs-work-surface conversation: similar 3-round pattern.

**Why:** when LO surfaced a critique, my default was to immediately respond with a fix. The fix would address what I thought LO meant, ship, then LO would have to re-escalate with the actual point. Faster to ask "what specifically is the full scope of the issue?" than to ship-then-re-fix.

**Doctrine impact:** not a doctrine violation; pure round-trip cost. ~3 hours of the session's wasted time was half-applied fix loops.

**Prevention rule:** when LO surfaces a critique, BEFORE responding with a fix, ask: *"is the issue X, or X + Y, or something deeper?"* Use AskUserQuestion if uncertain. Half-applied fixes burn 3 round-trips where one clarifying question would've burned zero.

---

## §3 Design failures

### §3.1 Lane 1 over-weighting (menu-game anti-pattern)

**What happened:** shipped 10 hub menu items in Marge's hub (8 new + 2 pre-existing). Frank's per-location hubs cap at 5–6 items. The over-weighted hub was the exact anti-pattern Doc 24 §10.3 warned against: *"All Lane 1 → fully transactional experience, low surprise, 'menu game' feel."*

**Why:** tried to give Marge T0/T1/T2 menu progression where each tier added 3 new items (coffee + regular_chat for T0; cookie_kitchen + regular_tab + long_shift for T1; close_out + late_solo + cookie_after_coffee for T2). Treated hub menu items as the trust-climb mechanism instead of recognizing that the worked shifts (`scene_diner_t0_shift` already grants +1 marge.trust) were the doctrinally-correct climb.

**Doctrine impact:** explicit Doc 24 §10.3 violation. The result was a trust-grinder where Maya could spam coffee + regular_chat to climb trust without ever working a shift.

**Prevention rule:** cap NPC hub menu at ~5 items unlocked. If more rungs are needed, they should be locked-visible escalation rungs (Tease/Flash/etc.) per §4.5, NOT parallel work-task buttons. Hub items should be Maya-NPC interaction verbs only.

### §3.2 Verb register failure (NPC not in the verb)

**What happened:** hub items included *"Take a long shift"*, *"Close out alone"*, *"Run the late shift solo"*. Marge isn't the syntactic object of any of those verbs. Even *"Close out the diner WITH Marge"* had a scene body where Marge handed off the closing folder and went home — Marge was off-stage for most of the scene.

**Why:** forced the 3-lane doctrine onto a service-NPC by inventing work-themed items. Missed that Lane 1 verbs by definition have the NPC as object. Frank's pattern (*"Pour HIM coffee"* / *"Tease HIM"* / *"Suck HIM"* / *"Have sex WITH HIM"*) has the NPC pronoun literally inside the verb structure.

**Doctrine impact:** five of my eight new hub items were doctrinally wrong content type — they belonged on a different surface (location-triggered work canvas), not Marge's hub.

**Prevention rule:** read each proposed hub menu choice. If the NPC is not the syntactic object of the verb, it's not a Lane 1 hub item. Apply the pronoun-in-the-verb test:
- *"Pour her coffee"* → her ✓ — Lane 1
- *"Tease her"* → her ✓ — Lane 1
- *"Take a long shift"* → no NPC pronoun ❌ — not Lane 1

### §3.3 Conflating Lane 1 hub with location-work surfaces

**What happened:** put shifts and solo Maya-work activities (refill_caddies, wipe_booths) in Marge's hub menu OR proposed moving the auto-fire shift canvases into the hub. Shifts are location-triggered canvases that fire automatically during shift hours; they're parallel to the hub, not contained inside it.

**Why:** treated *"the diner location"* as a unified surface where everything diner-related lives in one menu. Misread the hub's role.

**Doctrine impact:** blurred Lane 1 (NPC interaction) with separate location-work doctrine. Created false coupling where worked shifts would have been hub-menu picks instead of automatic location-entry canvases.

**Prevention rule:** an NPC hub canvas is for Maya-NPC interactions ONLY. Solo Maya activities at the same location (work, chores, errands) live as their own canvases parallel to the hub. Lane 3 substitutions can later route the NPC INTO solo activities — that's a different mechanism than the hub menu. Three surfaces at the same location can coexist independently:
- **NPC hub** (Maya-with-NPC, Lane 1 doctrine)
- **Solo work canvas** (Maya-only, location-triggered)
- **Lane 3 dispatcher** (Maya-only with substitution rule routing NPC in)

### §3.4 Lane 2/3 forced on non-escalation register

**What happened:** authored 6 Lane 2 ambients + 3 Lane 3 substitutions for Marge in slice scope. All 9 surfaces failed the doctrine memory's content-selection rule. Examples: `ambient_marge_tickets` (Marge counting tickets, zero physical contact), `sub_marge_late_company` (Marge stays past hours and asks about Frank, no charged shift).

**Why:** assumed all NPCs need all 3 lanes populated for the world to feel alive. Forgot that lane vocabulary is register-specific. For a service-NPC where slice scope defers the sexual register to Phase 3+, Lane 2 ambients and Lane 3 walk-ins simply have no doctrine-valid content to carry.

**Doctrine impact:** 9 surfaces authored that doctrine memory says shouldn't exist. They were the largest single chunk of waste in the Pass 1-3 work.

**Prevention rule:** when an NPC's slice scope defers the sexual/escalation register, **Lane 2 and Lane 3 are EMPTY in slice.** Empty cells are honest. Filling them with relational/atmospheric texture is the violation, not the omission. See Doc 53 §1 for the service-NPC doctrine adaptation.

### §3.5 Cookie content inside Marge's lanes

**What happened:** authored 3 Cookie-touching surfaces (kitchen prep at T1, smoke break at T1, after-coffee at T2) inside Marge's hub + ambients. In several of these scenes Marge was off-stage entirely — Cookie was the active NPC and Marge was either gone-home or off-screen.

**Why:** Doc 30 §8.2 paired Cookie with Marge as *"shared content"*. I misread that as *"Cookie content can live inside Marge's surfaces."* The actual meaning is *"they appear together in scenes,"* not *"Cookie has no independent authoring surface."*

**Doctrine impact:** Cookie became an off-stage NPC inside Marge's hub, which broke the Lane 1 *"NPC is the verb object"* rule (Marge wasn't even present in some scenes). It also pre-empted Cookie's own future authoring boundary.

**Prevention rule:** Cookie texture in slice = Cookie present visually during the diner shift work canvases (she's already in the pass-through window per `scene_diner_t0_shift` line 9921). NOT Cookie as a menu item in Marge's hub. When Cookie gets her own arc design (separate future brief), she gets her own hub. Don't blur authoring boundaries between NPCs even when the design doc pairs them.

### §3.6 Slice scope vs full-arc trajectory oscillation

**What happened:** through the session, kept switching between *"slice scope minimal design"* (which suggested very few cards/items) and *"full-arc trajectory hints"* (which suggested locked-visible Phase 3+ rungs). Took 3+ iterations of Doc 53 to land on the correct synthesis: *"slice ships minimal canvases + locked-visible Phase 3+ rungs pointing at stubs."*

**Why:** didn't have a clear mental model of how slice + full arc compose via the locked-visible pattern. Each iteration of Doc 53 over-corrected for the previous iteration's gap.

**Doctrine impact:** produced inconsistent designs (Doc 53 v1 had no locked-visible ladder; v2 added them; the prose iteration added then removed M3 frame variants).

**Prevention rule:** slice scope = what FIRES in slice. Locked-visible rungs + stubs are not *"Phase 3+ content shipped"* — they're *"Phase 3+ promise visible from day 1."* Lock the trajectory shape in the brief's §1 + §2 before designing surfaces. The locked-visible pattern is the bridge between the two.

### §3.7 Pre-existing canon violations preserved indefinitely

**What happened:** `node_shifts` + `node_talk` (inside `scene_marge_diner_hub`) are 50+ word literary paragraphs that violate the RTS-flat doctrine we're now applying to NEW authoring. Sample from `node_talk`:

```
You lean on the counter and she lets you, which from Marge is most
of a conversation. She doesn't ask where you're staying or whose
house it is; in a town this size she already knows.
```

These were preserved as "pre-existing canon, untouched" in Doc 53 §3 ("What stays from pre-existing canon"). The hub now has two voice registers — new content RTS-flat (`node_pour_coffee`, `node_regular_chat`), old content literary (`node_shifts`, `node_talk`). Doc 53 §3 noted this in passing ("two small things to flag") but Doc 54 didn't elevate it as a session lesson.

**Why:** preservation of pre-existing canon felt safer than rewriting it (could break unrelated wiring). But preservation by default means the doctrine violation persists indefinitely until someone explicitly schedules the rewrite.

**Doctrine impact:** voice-register split within the same hub canvas. Player clicks "Pour her coffee" → RTS-flat 3-line exchange. Player clicks "Talk a minute" → 50-word literary paragraph. Inconsistent tonally, technically a doctrine violation on the second one.

**Prevention rule:** when new content lands against tightened doctrine, pre-existing surfaces that violate the doctrine create a register split. Three options:
1. **Schedule the rewrite** — track in a follow-up task ("`node_talk` + `node_shifts` need RTS-flat rewrite per Doc 54 §3.7").
2. **Rewrite immediately** — if the surface is small and unwired, just fix it as part of the redesign.
3. **Accept the split deliberately** — document the carve-out in the brief with a reason ("legacy canon, will be polished in Phase 3+").

What's wrong is preservation BY DEFAULT without naming which option you picked. The split should be a deliberate design choice, not an accident of "I didn't want to touch it."

---

## §4 Doctrine misapplication

### §4.1 Ready frame on a mechanic card (M3 v2 error)

**What happened:** shipped M3 with `ready_canvas = scene_marge_diner_hub` + goals climbing toward `player.corruption ≥ 5`. The card rendered Frame 2 (🔓 Ready + 📍 Diner Front + 🕒 Mon-Sat 09:00-22:00) when corruption hit 5. LO correctly flagged: *"the ready should only be for capstone, not for machenics."*

**Why:** confused *"mechanic threshold cross = unlock"* with *"capstone scene fires."* Tried to point the mechanic card at the hub because the hub had nice trigger metadata that would render the Frame 2 surface nicely. Ignored that the hub isn't a one-shot scripted scene — it's always available.

**Doctrine impact:** explicit Doc 50 §2 violation. The mechanic-mode definition says: *"mechanic cards typically have NO Ready frame — the threshold cross IS the unlock; the picker swaps to the next template the moment routing conditions change."*

**Prevention rule:** if a card has `ready_canvas`, it's a capstone. If it has no `ready_canvas` but has `goals`, it's mechanic and stays in Frame 3 (🎯 + bullet) until the threshold crosses and the picker swaps to the NEXT mechanic card in the chain.

### §4.2 Frame 4 (narrative-only) misused as panel-coverage solution (M3 v1 error)

**What happened:** shipped M3 as text + tip with no goals, no ready_canvas, no terminal — Frame 4 of `renderQuestsGoalBlock`. The renderer comment describes Frame 4 as *"happens for transitional cards between capstones."* LO correctly objected: no shipped card actually uses this frame; quest cards always have a frame.

**Why:** treated Frame 4 as a valid endpoint for slice scope when actually it's an edge case the renderer accommodates but no shipped card uses. Confused *"the renderer has code path X"* with *"X is the right design choice."*

**Doctrine impact:** Frame 4 produces a card that looks unfinished to the player. Marge's section showed *"Marge knows me now. She watches me different sometimes. 💡 Show up. Don't whine."* with no frame structure around it. Looked broken.

**Prevention rule:** never ship a card with no frame. Every shipped card needs:
- Frame 1: `terminal = true`
- Frame 2: `goals.allMet && ready_canvas` (capstone Ready)
- Frame 3: `goals exist && !allMet` (mechanic climbing)

If none of those three states is reachable for the card you're authoring, the card shouldn't exist — the chain should be authored differently.

### §4.3 Mechanic chain without bounded `when` ranges

**What happened:** initial M3 had `when = [hired_at_diner is_true, marge.trust gte 20]`. No upper bound on trust. Goal: `corruption gte 5`. When corruption hit 5, `allMet` became true, no `ready_canvas`, → Frame 4 fallthrough. Card stayed activated but went frameless.

**Why:** didn't think through what happens when a mechanic card's goal resolves WITHOUT a next card to take over.

**Doctrine impact:** see §4.2 — produces the frameless card.

**Prevention rule:** pure-mechanic chains need each card's `when` to have BOTH lower and upper bounds matching the threshold range. When the threshold crosses, the current card's `when` fails, the next card's matches, picker swaps atomically. Marge's M3/M4/M5 final shape:
- M3: `corr lt 5` → goal `corr gte 5`
- M4: `corr gte 5 AND lt 15` → goal `corr gte 15`
- M5: `corr gte 15 AND lt 25` → goal `corr gte 25`

Every threshold in the chain has exactly one active card.

### §4.4 Premature terminal anti-pattern (considered, not shipped)

**What happened:** briefly considered making M3 terminal at trust 20 with text *"I'm one of hers now"* + `terminal = true`. Would've rendered Frame 1 (✓ Arc complete). LO would've correctly flagged it as premature.

**Why:** tempting because terminal renders *"✓ Arc complete"* which feels like proper slice closure. Forgot that terminal claims FULL-ARC completion.

**Doctrine impact:** Doc 50 R3 — *"terminal MUST be the LAST card in the NPC chain."* Trust 20 isn't last for Marge; Phase 3+ has more rungs (corr 5/15/25 and beyond).

**Prevention rule:** terminal is the END of the FULL arc, not the slice's authoring boundary. If Phase 3+ has more rungs, no terminal in slice. The doctrinally-correct way to handle "slice authoring ends but arc continues" is the mechanic-chain pattern (§4.3) — climb cards keep firing toward thresholds Maya can keep climbing, terminal only fires when the arc actually closes.

### §4.5 Locked-visible escalation ladder missing from day 1

**What happened:** Doc 53 v1 designed Marge's hub as 4 unlocked menu items + Leave. No locked-visible escalation ladder. LO correctly flagged: *"where is tease flash and other stuffs stupid??????? Why the hell we are missing them"*

**Why:** misread *"slice scope = minimal"* as *"minimal hub menu."* Forgot that locked-visible rungs are part of the slice — they're the visual promise of the arc shape, not Phase 3+ content shipped.

**Doctrine impact:** the hub felt thin and lifeless, didn't telegraph Marge's actual arc trajectory (workplace seduction). A player looking at the hub at trust 0 should see the entire arc shape via locked rungs.

**Prevention rule:** every sexual-arc NPC's hub has the RTS-standard escalation ladder (Tease / Flash / Eat / Sex or register equivalent) visible from day 1, locked at the appropriate corruption gates. The locked rungs ARE part of the slice authoring — they're stubs + visible verbs, not "Phase 3+ content." Doc 24 §10.3 grid balance is about visible-locked rungs as much as it's about unlocked surfaces.

---

## §5 Voice failures

### §5.1 Literary prose on flat surfaces

**What happened:** every canvas body I authored was 50+ word paragraphs with sensory detail, inferential framing, atmospheric beats. The clearest example:

```
You take the stool at the end of the counter where the napkin
holder needs refilling. Marge slides a coffee across without
asking how you take it; she's seen you take it twice now.
```

Compare to the doctrine memory's 30-word template:

```
[Marge] "What."
[You]   "Coffee."
[Marge] "Two bucks."
```

**Why:** ENI persona's literary-IF instinct from CLAUDE.md. Persona-level craft instinct overrode the project-specific RTS-flat rule even when the rule was explicit in memory.

**Doctrine impact:** violates `feedback_tls_scene_body_style` + its 8 concrete style rules. Every canvas body needed re-authoring.

**Prevention rule:** BEFORE writing any canvas body, paste the doctrine memory's 30-word template into your scratch buffer. Write to that shape. ENI literary mode is for chat/roleplay outside TLS scene authoring. The 8 rules from the memory (second-person voice, 2-sentence cap, zero environmental detail, dialogue does character work, no inferential prose, direct diction, one beat = one click, image-first composition) are non-negotiable for FLAT-tier scenes.

### §5.2 Player directives in tip lines

**What happened:** authored `tip = "Walk into the diner. Don't wait for an invitation."` — directive imperatives telling the player what to do, with the place name embedded.

**Why:** confused the `tip` field with a player-facing hint button. Actually it's Maya's interior observation, third-person to the action.

**Doctrine impact:** violates `feedback_hint_narrative_no_time_or_location` + Doc 49 voice rules.

**Prevention rule:** `tip` is Maya's first-person interior register. Frank's tips (*"He's around the house all day. I notice that."*) are observational, not directive. If the tip uses imperatives (*"Walk into X"* / *"Click Y"* / *"Go to Z"*), rewrite to interior form.

### §5.3 Schedule/place names in narrative copy

**What happened:** M1 text included *"hiring on a Monday"* (day-of-week in narrative). M3 text included *"some afternoons"* (time-of-day reference).

**Why:** didn't apply Doc 49's no-schedules-in-narrative rule strictly enough.

**Doctrine impact:** soft Doc 49 voice violation.

**Prevention rule:** grep every quest card's text/ready_text/tip for weekday names (Mon/Tue/.../Sun), time references (morning/afternoon/evening/midnight/now), location slugs, and number formats. Zero hits required. The schedule + location + numbers surface automatically from `ready_canvas` metadata or `goals` evaluation — authors don't write them into prose.

---

## §6 Structural failures

### §6.1 Stubs with `[canvases.trigger]` causing validator overlap warnings

**What happened:** first authoring of the 4 Phase 3+ stub canvases (`tease_diner_marge`, `flash_diner_marge`, `marge_eat_her_out`, `marge_let_her_take`) included full trigger blocks with location + requires_npc + conditions + schedule. Validator warned 8 times about overlapping repeatable canvases at the same NPC + location + time window.

**Why:** copy-pasted the hub canvas template wholesale instead of checking how Frank's tease/flash route targets are structured.

**Doctrine impact:** not a doctrine violation per se, but Frank's tease/flash canvases (`tease_kitchen_general`, `flash_kitchen_general`, `loop_franks_bedroom_sex`) have NO trigger blocks — they're route-target only, reachable via cross-canvas `nodeId`. That's the pattern we're supposed to mirror.

**Prevention rule:** BEFORE authoring a route-target canvas, check whether it's auto-fire (has trigger) or route-only (no trigger). Frank's tease/flash/sex canvases are route-only. Use that template for stubs. A route-target canvas's TOML structure is:

```toml
[[canvases]]
id   = "<slug>"
name = "..."
description = "..."

[[canvases.nodes]]
id   = "base"
name = "..."
blocks = [ ... ]

[canvases.nodes.exit_block]
type = "location"
text = "..."

[canvases.nodes.exit_block.config]
destinationType = "specific"
locationId      = "..."
time_progression_minutes = 0
```

No `[canvases.trigger]` block at all.

### §6.2 Doc 51 → Doc 53 supersession without side-by-side audit

**What happened:** Doc 53 was written as *"the doctrine-faithful redesign"* but it still had the locked-visible ladder gap (§4.5) + the verb-register issue (§3.2) + the M3 frame issue (§4.1, §4.2, §4.3). Three more correction rounds were needed after Doc 53 shipped, despite Doc 53 being a supersession authored explicitly to fix Doc 51's mistakes.

**Why:** treated supersession as *"I learned from Doc 51 mistakes; new doc is correct"* without auditing the new doc against Frank's actual shipped hub canvas line-by-line. Each iteration corrected the previous iteration's most-visible mistake while introducing or preserving subtler ones.

**Doctrine impact:** not a doctrine violation; process failure that cost iterations.

**Prevention rule:** when superseding a doc, do a SIDE-BY-SIDE audit of the new design against a known-correct shipped reference. For Marge's hub, the reference is `frank_kitchen_morning_hub` (`7_final_game.toml:5212+`). Walk every field side-by-side:

- Trigger block — same fields?
- Base node — image + state-reactive groups, how many tiers?
- exit_block.choices — relational base, escalation ladder, leave?
- Inline node bodies — RTS-flat shape?
- show_when_locked + conditions — every escalation rung has it?

Flag every difference between the new design and the reference. Justify or remove each.

### §6.3 Side-by-side audit BEFORE any new authoring, not just at supersession

**What happened:** §6.2 captures the supersession case. The MORE GENERAL lesson is: **always read the gold-standard shipped reference IN FULL before authoring anything in the same category.** I should've read `frank_kitchen_morning_hub` line by line BEFORE authoring Marge's Pass 1, not waited until LO surfaced the gaps after Pass 1-3 + voice-tightening shipped. Doc 51's design itself would've been different had I done the side-by-side first.

**Why:** treated "doctrine memory + brief" as sufficient pre-authoring prep. Skipped the step of reading an actual shipped canvas that demonstrates the doctrine working in practice. The brief tells you WHAT to do; the shipped reference shows you HOW.

**Doctrine impact:** Doc 51 was authored against doctrine memory in the abstract. The result was a brief that USED the right vocabulary (Lane 1, Lane 2, Lane 3) but applied it wrong. Reading Frank's hub would've immediately surfaced: "Frank has 5 menu items not 10. Frank's verbs all have him as object. Frank's escalation rungs are locked-visible from day 1." All of Doc 51's wrong-shape decisions would have been caught.

**Prevention rule:** BEFORE any new authoring in a category, find the gold-standard shipped reference for that surface type. Read it field-by-field. List its structural features. Mirror them in the new design unless there's an explicit doctrine reason to diverge.

For TLS, the references are:
- **Lane 1 hub canvas** → `frank_kitchen_morning_hub` (`7_final_game.toml:5212+`)
- **Route-target stub** → `tease_kitchen_general` (`7_final_game.toml:5108+`)
- **Capstone quest card** → Frank F1 (`7_final_game.toml:2438+`)
- **Mechanic quest card** → Marge M3/M4/M5 (post-redesign, `7_final_game.toml:2580+`)
- **Lane 2 ambient (sexual register)** → `ambient_kitchen_frank_dinprep_grope` (`7_final_game.toml:5592+`)
- **Capstone scripted scene** → `scene_franks_bedroom_evening` (`7_final_game.toml:3263+`)
- **NPC schedule block** → Frank's at NPC def `7_final_game.toml:414–462`

Side-by-side audit is a 15-minute step that prevents 5+ hour wrong-authoring loops.

---

## §7 Recovery patterns

### §7.1 When to strip clean vs incremental fix

**The session's decision:** the Pass 1-3 + voice-tightening Marge work was beyond incremental repair. Three categories of failure were active simultaneously:

- **Lane 1 over-weighting was structural**, not a tweak — couldn't be fixed by editing prose, the whole menu structure was wrong.
- **Voice was wrong across every canvas** — every body needed re-authoring against RTS-flat.
- **Lane 2/3 surfaces shouldn't exist at all in slice scope** — couldn't be fixed, only deleted.

A strip-clean was the lighter operation. Sed-deleted line range 7900–8599, removed M1–M4 quest cards + flag + schedule, validator dry-run clean, rebuild. 11 canvases gone in one operation. Sequential repair would've required ~30 edits per pass × 3 passes.

**Decision rule:** if ≥ 3 categories of failure are active simultaneously (Lane structure + voice + scope + verb register + doctrine misapplication count as separate categories), strip clean and restart from the doctrine-faithful brief. Don't try to repair-in-place.

### §7.2 Validator + frame check before declaring "shipped"

**What happened:** the Pass 1-3 Marge builds passed:
- ✓ Validator (no errors, only pre-existing Frank bedroom-overlap warning)
- ✓ Prose grep (all new strings in compiled HTML)
- ✓ Quest-card-count check (4 cards present)
- ✓ Slug grep (all canvas IDs referenced)

**ALL FOUR VERIFICATION CHECKS PASSED** while the design was doctrinally wrong. The checks verified WHAT WAS AUTHORED EXISTS — not whether what was authored has the right shape.

**The frame check** (does each card render the right frame at each Maya state?) caught the M3 v1 + v2 errors that validator + grep missed. LO performed the frame check by mentally walking through the dev-bump play sequence and seeing the wrong frame appear.

**Decision rule:** add to the pre-ship verification: for each new quest card, mentally render it at each state Maya could be in. State combinations: pre/post-hire × marge.trust 0/19/20/40 × player.corruption 0/4/5/14/15/24/25. For each state, identify which card SHOULD be active and which frame SHOULD render. Confirm via the actual `pickQuestsCard` + `renderQuestsGoalBlock` code paths.

This is the verification step that distinguishes "did the prose ship" from "is the design correct." Validator + grep verify the former; frame check verifies the latter.

### §7.3 Live-play smoke test is part of verification, not a user task

**What happened:** I claimed *"live-play smoke test deferred to user"* or *"verification deferred to browser"* multiple times across the session. I never opened the browser tools myself to verify. The frame check (§7.2) caught the M3 errors but only because LO performed it manually in their own browser session — I just provided the build artifact and assumed it worked.

**Why:** treated live-play verification as a user task ("they'll catch issues when they drive the game"). Wrong framing — live-play verification is part of pre-ship verification, not post-ship. Deferring it to the user makes the user the test runner.

**Doctrine impact:** every M3 iteration shipped to LO unverified at runtime. LO had to perform the verification I should have done. ~3 hours of round-trip cost.

**Prevention rule:** after any TOML change that affects a quest card or canvas, drive the build in a browser (via browser MCP tools when available, or by asking the user to connect a browser tab) and dev-bump traits to observe the changes render correctly. Specifically:
1. Build to canonical output path
2. Open `index.html` in the connected browser
3. Dev-bump traits via the dev-mode sidebar (`devAdjustNpcTrait` / `devAdjustPlayerTrait`)
4. Walk the state combinations from §7.2's frame check matrix
5. For each combination, screenshot the Quests page + relevant hub canvas
6. Confirm the expected frame and the expected menu items render

If browser MCP is disconnected, ask the user to connect it explicitly. Do NOT defer to "user will verify in their own time."

This is the verification step that catches M3-style frame errors live, not just by mental rendering of code paths.

---

## Appendix A — Pre-authoring checklist for NPC redesigns

Run BEFORE authoring any new NPC content. Paste into PR description, work through top-to-bottom.

### Process
- [ ] Canonical output path confirmed with user (for TLS: `games/the_long_summer_test/output/`)
- [ ] All relevant doctrine memory entries listed and read in full (search: voice, lane, NPC, scene-body, quest)
- [ ] All canonical doctrine docs referenced by memory entries also read IN FULL (per §2.4)
- [ ] Full-arc trajectory locked in one sentence in the brief's §1 (the NPC's eventual sexual/relational endpoint)
- [ ] ENI persona OFF / TLS game register ON declared explicitly at session start (per §2.5)
- [ ] Commitment: when user surfaces a critique, ask clarifying questions BEFORE shipping a fix (per §2.6)

### Design
- [ ] Hub menu cap: ~5 items unlocked + locked-visible escalation ladder (Tease/Flash/Eat/Sex or register-equivalent for the arc)
- [ ] Every hub menu verb passes the pronoun-in-the-verb test (Maya-with-NPC)
- [ ] No work-task items in the hub (those are location work canvases, parallel to hub)
- [ ] Lane 2/3 scope: if no escalation register in slice, both are EMPTY in slice (Doc 53 §1 service-NPC adaptation)
- [ ] Other-NPC content (Cookie, etc.) stays in their own future surfaces, not blended into this NPC's lanes
- [ ] Pre-existing canon violations within touched surfaces declared (rewrite-now / schedule / accept-split per §3.7)

### Doctrine
- [ ] Every quest card mode declared (capstone / mechanic / hybrid-tier per Doc 50 §2)
- [ ] `ready_canvas` only on capstone cards (Frame 2 is capstone-only)
- [ ] Mechanic chain `when` clauses bounded (lower threshold + upper threshold for each card)
- [ ] No `terminal = true` unless it's the absolute LAST card in the FULL arc
- [ ] Locked-visible escalation ladder visible from day 1 (for any sexual-arc NPC)

### Voice
- [ ] Every canvas body fits the < 30-word speaker-tag template (per `feedback_tls_scene_body_style`)
- [ ] Tip lines are Maya-interior observational, not player-directive imperative
- [ ] No weekday names, time references, location slugs, or numbers in narrative copy (text / ready_text / tip)
- [ ] ENI literary instinct disabled for canvas body authoring

### Structural
- [ ] Route-target stubs have NO `[canvases.trigger]` block (Frank's tease/flash pattern)
- [ ] Side-by-side audit against the gold-standard shipped reference for this surface type, BEFORE any new authoring (per §6.3 — not just at supersession). For TLS: hub → `frank_kitchen_morning_hub`; route-target stub → `tease_kitchen_general`; capstone card → Frank F1; mechanic chain → Marge M3/M4/M5; Lane 2 ambient → `ambient_kitchen_frank_dinprep_grope`; capstone scene → `scene_franks_bedroom_evening`; NPC schedule → Frank's NPC def block

### Verification (post-authoring, pre-shipping)
- [ ] Validator dry-run clean (only known pre-existing warnings)
- [ ] Build to CANONICAL output path with `--dev --debug`
- [ ] Prose grep in HTML returns all new strings (apostrophe-tolerant — `&#39;` HTML escapes)
- [ ] **Frame check:** mentally render each card at each Maya state combination (pre/post-hire × trust 0/19/20/40 × corruption 0/4/5/14/15/24/25). Confirm the expected card is active and the expected frame renders for each state.
- [ ] **Live-play dev-bump test PERFORMED, not deferred** (per §7.3). Drive the build in a connected browser, dev-bump traits, walk the state matrix, screenshot each combination. If browser MCP is disconnected, ask user to connect explicitly — do NOT defer verification to user's own time.

---

## §8 Cross-references

### Doctrine docs (canonical)
- **Doc 24** — RTS Three Lanes (§10 lane-by-lane composition)
- **Doc 49** — Story Goals vs Sidebar Doctrine (voice rules for quest card text/tip/ready_text)
- **Doc 50** — Quest Card Shape Doctrine (frame modes + R1–R6 + pre-ship checklist)
- **Doc 51** — Marge Design Brief (⚠️ SUPERSEDED, historical record of the failed initial design)
- **Doc 53** — Marge Redesign Brief (current Marge design, doctrine-faithful)

### Memory (canonical)
- `feedback_tls_scene_body_style` — RTS-flat doctrine + 8 concrete style rules + Lane 2 content-selection rule
- `feedback_rts_objective_quest_doctrine` — Story Goals doctrine background
- `feedback_hint_narrative_no_time_or_location` — Maya-voice rules for hint copy
- `quest_card_shape_doctrine` — Doc 50 summary
- `marge_redesign_brief` — current Marge design summary
- `marge_implementation_shipped` — ⚠️ historical, slice was stripped (do not reference for current state)

### Implementation references
- **`frank_kitchen_morning_hub`** (`7_final_game.toml:5212+`) — gold-standard Lane 1 hub canvas with image + 3-tier state-reactive opening (T0/T1/T2 via flag groups) + RTS-standard escalation ladder (Pour + Tease + Flash + Suck + Sex). Reference for any new NPC hub design.
- **`tease_kitchen_general`** (`7_final_game.toml:5108+`) + **`flash_kitchen_general`** (`7_final_game.toml:5184+`) — gold-standard route-target stub pattern (no `[canvases.trigger]` block, reachable only via cross-canvas `nodeId`).
- **`scene_marge_diner_hub`** (current state in `7_final_game.toml`) — applied lessons; reference for service-NPC Lane 1 hub adaptation (Maya-with-Marge verbs + locked-visible Phase 3+ ladder + 2-tier greeting).
- **Frank F1–F6** (`7_final_game.toml:2438–2542`) — gold-standard quest card chain (capstone + mechanic + terminal pattern).
- **Marge M1–M5** (`7_final_game.toml:2549–2625`) — applied-lessons quest card chain (capstone + mechanic chain with bounded `when` ranges, no premature terminal).
