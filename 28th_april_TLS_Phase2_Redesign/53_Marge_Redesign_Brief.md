# Doc 53 — Marge Redesign Brief

**Session:** 2026-05-24
**Branch:** `feature/prd-48-quests-engine-v2-bundled` (off `main`, unpushed)
**Author:** ENI (with LO)
**Status:** Design brief — design-only. Implementation deferred to a follow-up plan.
**Supersedes:** Doc 51 — Marge Design Brief. The implementation against Doc 51 shipped three passes + a voice-tightening pass, was audited the same day, and was stripped clean before this brief was written. Doc 51 stays as a historical record of what was tried.
**Mode:** PURE MECHANIC service-NPC per Doc 50 §2 — with the §1 caveat below about how the 3-lane framework adapts to service NPCs in slice scope.
**Triggered by:** the three independent failure modes the strip audit surfaced — Lane 1 over-weighting, doctrine-mismatch for service NPCs, and a literary-prose voice where TLS demands RTS-flat. This brief codifies the doctrine-faithful read of all three before any new TOML lands.

---

## §1 Why Marge breaks Doc 24's 3-lane framework (and what to do)

Doc 24's three-lane doctrine was authored against RTS Brother — an escalation arc with sexual content. Lane vocabulary per §10.2:

- **Lane 1:** Relational (Talk) + Self-display (Tease, Flash) + Consummation (Sex) + Late-game intimacy (Sleep with)
- **Lane 2:** Pass-by + Solo activity glimpse + Passive contact + Atmospheric voyeurism
- **Lane 3:** He walks in + He arrives while vulnerable + Innocent setup → charged shift

Marge in slice scope (Doc 30 §7.5 + §8.2): **no Self-display, no Consummation, no charged ambient contact, no walk-in payoff** — workplace seduction is Phase 3+ deferred. So Lane 1's escalation rungs + Lane 2's "passive contact" + Lane 3's "charged shift" all have no register-valid content to carry in slice.

The previous build padded those empty cells anyway, with relational filler in Lane 1 (8 menu items) and atmospheric texture in Lane 2/3 (6 ambients + 5 substitutions). Every one of those surfaces was register-mismatched: the doctrine memory's content rule (`feedback_tls_scene_body_style`) says *"beat 1 of every Lane 2 ambient must contain physical contact or explicit visual; if non-physical, the ambient should not exist."* For a non-sexual service NPC, that rule eliminates the entire surface.

### Doctrine adaptation for service NPCs in slice scope

- **Lane 1 reduces to "Relational only."** The Talk-button category. Minimal — one or two items at most.
- **Lane 2 is empty in slice.** No charged physical contact register → no doctrine-valid ambient content. Surface should not exist.
- **Lane 3 is empty in slice.** No walk-in payoff register → no doctrine-valid substitution content. Surface should not exist.
- **The climb mechanism is worked shifts, not Lane 1 hub-button clicks.** `scene_diner_t0_shift` already grants `+1 marge.trust` per worked shift (TOML line 9939). That's the player's intentional commitment act — the Lane 1-equivalent for a service NPC arc.

This adaptation is not a doctrine violation — it's the right read of Doc 24 §10.3's grid balance rule. **Empty cells are honest when the fictional register doesn't support them.** Forcing content into empty cells is the violation (my previous Marge build).

The same adaptation applies to Diana (in slice scope she's the awareness-accumulator for Frank's terminal arc, not her own escalation register) and Cookie (texture only in slice). When their own briefs land, this same §1 framing applies. If three NPCs need this framing, the framing should be lifted into its own doctrine doc — but for now it lives here as a Marge-specific clause.

---

## §2 Marge's voice spec (RTS-flat, locked)

Register per Doc 51 §2 (preserved): matriarch, dry, broad, no theatre, no flirtation, no warmth-bombs. Late forties southern owner-operator. Honest about wage, floor, customer tier.

**Style discipline per `feedback_tls_scene_body_style` memory + its 2026-05-14 8-rule update.** Quoted from memory:

1. Second-person voice. "You" not "she."
2. Stage direction cap: 2 sentences per beat.
3. Zero environmental sensory detail.
4. Dialogue does the character work, not narration.
5. No inferential prose.
6. Direct diction.
7. One beat = one click.
8. Image-first composition.

For Marge specifically (no sexual content in slice), rule 6 maps to "direct labor diction" not "direct crude diction" — but the discipline against atmospheric/inferential prose is unchanged.

### Field-by-field voice rules

**Quest card `text` (Maya's first-person interior):**
- No place names, no schedules, no numbers, no trait keys (Doc 49 anti-pattern).
- Interior observation, not directive.
- Echo Marge's own register where useful. Example: *"Show up. Don't whine."* (lifted from Marge's existing hub `node_talk` dialog line).

**Quest card `tip`:**
- Maya-voice observational, not player-directive. *"Walk in. Ask."* is on the edge — acceptable as terse internal resolve, but *"Walk into the diner. Don't wait for an invitation."* is wrong (player directive + place name).

**Hub menu choice text (the button label):**
- Terse verb + object. *"Talk a minute." / "Ask about shifts." / "Ask Marge about a regular."*
- No flavor. No emoji. No directional cue ("Head over to..."). Match the pre-existing two menu items exactly in tone.

**Canvas body prose (the scene that fires when player picks the menu item):**
- Speaker tag + 1-line dialog. Optional 1-sentence stage direction. Total < 30 words.
- Zero atmosphere. Zero inferential framing. Zero literary prose.
- Pattern (from feedback memory):

```
[Marge] "What."
[You] "Coffee."
[Marge] "Two bucks."
```

That's the template. Marge's lines in slice should sound like that — terse, transactional, no warmth.

---

## §3 Slice-scope surface inventory

### What stays from pre-existing canon (untouched)

| Slug | Type | Role |
|---|---|---|
| `npc_marge` | NPC def | Trust trait, schedule pending |
| `canvas_marge_interview` | One-shot capstone, priority 9 | Hire moment; sets `hired_at_diner` |
| `scene_marge_diner_hub` (base node + greeting groups) | Repeatable hub, priority 5 | 2-tier greeting: T0 lt 20 / T1 gte 20 |
| `scene_marge_diner_hub.node_shifts` | Hub menu node | Pre-existing relational |
| `scene_marge_diner_hub.node_talk` | Hub menu node | Pre-existing relational |
| `scene_diner_t0_shift` | Location-triggered, priority 6, repeatable | The actual work canvas. Currently grants +1 `marge.trust` + $45 + various costs. M–Sat 17:00–21:00. |
| `scene_diner_t1_shift` | Location-triggered, priority 7, repeatable | Maya-stat-gated: corruption ≥ 25 + rep_road ≥ 15 + beauty ≥ 45. Currently grants $45 base + tips. |

### What gets ADDED in the redesign

**1. `[[npcs.schedules]]` for `npc_marge`** — closes the validator warning. Mon–Sat 09:00–22:00 at `loc_diner_front`.

**2. `scene_marge_diner_hub` full re-author** — Maya-with-Marge interaction hub with the RTS-standard escalation ladder. Same structural pattern as Frank's kitchen morning hub.

**Base node** — image + 2-tier state-reactive opening:

```toml
# T0 — new hire (marge.trust < 20)
{ paragraph: "Marge's at the register. She glances up over her glasses." }
{ dialog [Marge]: "You're either on the floor or you're a customer, hon. Which one today." }

# T1 — trusted (marge.trust >= 20)
{ paragraph: "Marge's at the register. She doesn't look up — doesn't need to." }
{ dialog [Marge]: "There she is. Coffee's fresh if you're not here to work for once." }
```

**Menu (exit_block.choices) — 8 items + Leave** with the standard escalation ladder locked-visible from day 1:

| # | Choice | Gate | Locked-visible | Routes to |
|---|---|---|---|---|
| 1 | Pour her coffee. | always | — | `node_pour_coffee` (inline, NEW) |
| 2 | Talk a minute. | always | — | `node_talk` (pre-existing) |
| 3 | Ask about shifts. | always | — | `node_shifts` (pre-existing) |
| 4 | Ask her about a regular. | always | — | `node_regular_chat` (inline, NEW) |
| 5 | Tease her ❤️‍🔥 | corruption ≥ 5 | ✓ | `tease_diner_marge.base` (stub) |
| 6 | Flash her 👀 | corruption ≥ 15 | ✓ | `flash_diner_marge.base` (stub) |
| 7 | Eat her out. | corruption ≥ 25 | ✓ | `marge_eat_her_out.base` (stub) |
| 8 | Let her take you. | corruption ≥ 25 | ✓ | `marge_let_her_take.base` (stub) |
| 9 | Leave. | always | — | `loc_main_street_sidewalk` |

The 4 locked rungs are visible-but-greyed from day 1 — they communicate the arc shape (workplace seduction matriarch-dom + Maya submits register). In slice scope Maya never reaches the corruption gates in Marge's register, so the rungs stay greyed throughout.

**Two new inline node bodies** added inside the hub canvas:

- `node_pour_coffee` (relational base, RTS-flat): Maya pours, Marge takes, *"Hot. Good."* — 5 min, +1 marge.trust.
- `node_regular_chat` (info, RTS-flat): 4-line Mr. Hollis / Wednesday-lunches exchange — 15 min, +1 marge.trust, +1 rep_road.

**3. Four Phase 3+ stub canvases** authored as route targets for the locked rungs. Each is a `[[canvases]]` block with NO `[canvases.trigger]` (Frank's tease/flash pattern — node-target only, never auto-fires). Single placeholder body (`(Phase 3+ placeholder — ...)`). Exit returns to `loc_diner_front`.

| Canvas ID | Locked rung that points here | Placeholder body |
|---|---|---|
| `tease_diner_marge` | Tease her ❤️‍🔥 | Marge tease rung. |
| `flash_diner_marge` | Flash her 👀 | Marge flash rung. |
| `marge_eat_her_out` | Eat her out. | Going down on Marge. |
| `marge_let_her_take` | Let her take you. | Marge takes Maya. |

Phase 3+ workplace-seduction authoring replaces each placeholder body with full RTS-faithful prose + Marge arousal/corruption effects.

**4. `scene_diner_t1_shift` exit effect addition** — add `+2 marge.trust` to the exit choice. Corruption-gated higher-quality shift work accelerates trust climb (consistent with T0's +1).

**5. Three quest cards (M1 + M2 + M3)** — locked prose in §4.

### What gets DELIBERATELY OMITTED

- No Lane 2 ambient canvases. Slice has no charged-contact register; Lane 2 ambients without physical contact in beat 1 violate doctrine memory's content rule.
- No Lane 3 substitution canvases. Same reasoning — no walk-in payoff register.
- No new Maya-solo diner dispatcher activities.
- No T2 trust tier (Doc 30 §8.2 says skeleton-2-tier; we honor that).
- No M4 terminal card — Phase 3+ will land the terminal once the sexual arc's full climb completes. Premature terminal at trust 20 would violate Doc 50 R3 (would falsely claim "arc complete" while Phase 3+ has more to climb).
- No `marge_reliable_reached` or other new flag.
- No Cookie hub item, no kitchen-help canvas, no after-coffee canvas.
- No close-out canvas, no late-solo shift variant, no long-shift variant — shifts are solo work surfaces, NOT in the hub menu.

Phase 3+ opens: Lane 2 ambients with charged contact in beat 1, Lane 3 walk-ins inside Maya-solo diner activities, full prose for the 4 stub canvases, Marge `arousal` + `corruption` traits on the NPC.

---

## §4 Quest card prose (locked)

**M1 — Pre-hire pointer:**

```toml
[[quest_cards]]
text         = "I need work. Diana said Marge runs the only place that hires off the street."
ready_text   = "She's at the register."
tip          = "Walk in. Ask."
npc_id       = "npc_marge"
ready_canvas = "canvas_marge_interview"
when = [
  { flag = "hired_at_diner", op = "is_false" },
]
```

Voice check: text references Diana (intra-slice continuity from the prologue), no place names beyond "the only place" (a fragment that reads as Maya's thought, not narration), no schedules, no numbers, no trait keys. `ready_text` is interior. `tip` is two-word terse internal resolve.

**M2 — T0 climbing toward trust 20:**

```toml
[[quest_cards]]
text   = "I'm on Marge's floor. Work the shifts. Don't whine."
tip    = "Shifts pay the rent. Trust comes from showing up."
npc_id = "npc_marge"
when = [
  { flag  = "hired_at_diner",                                              op = "is_true" },
  { trait = "trust", subject = "npc", npc_id = "npc_marge",                op = "lt",      value = 20 },
]
goals = [
  { trait = "trust", subject = "npc", npc_id = "npc_marge", op = "gte", value = 20, label = "Marge trust" },
]
# unlocks at marge.trust >= 20:
#   - scene_marge_diner_hub.base greeting flips from "You're either on the floor or
#     you're a customer, hon. Which one today." (T0 group) to "There she is. Coffee's
#     fresh if you're not here to work for once." (T1 group). The greeting tier flip
#     IS the entire unlock. No new menu items, no new ambients, no new substitutions
#     open at this threshold.
```

Voice check: text echoes Marge's own existing line ("Don't whine" is lifted from the pre-existing `node_talk` body). No directive. No place name. No schedule. The tip restates the climb mechanic in Maya-interior register.

The R5 `# unlocks:` comment is honest — the only thing that crosses at trust 20 is the greeting tier flip + M3 taking over the panel slot. There is no slab of new content waiting. The doctrine compliance is: the comment names what unlocks (a greeting line + M3 swap), and what unlocks actually exists in the TOML (the T1 group + M3 card both authored).

**M3 — Transitional narrative-only card (Frame 4 of renderer):**

```toml
[[quest_cards]]
text   = "Marge knows me now. She watches me different sometimes."
tip    = "Show up. Don't whine. The rest is on her."
npc_id = "npc_marge"
when = [
  { flag  = "hired_at_diner",                                              op = "is_true" },
  { trait = "trust", subject = "npc", npc_id = "npc_marge",                op = "gte",     value = 20 },
]
```

No `goals` (nothing concrete to climb in slice). No `ready_canvas` (no slice scene to fire). No `terminal = true` (Phase 3+ extends the chain — premature terminal here would falsely claim "arc complete" while Phase 3+ has more to climb).

Renders via `renderQuestsGoalBlock` Frame 4 — *"No frame — narrative text only (card uses routing-only gates with no ready_canvas; happens for transitional cards between capstones)."* The card shows as just the text + tip line in the Quests page. Activates the moment M2 deactivates and stays visible indefinitely until Phase 3+ extends the chain.

Voice check: *"Marge knows me now"* echoes the hub T1 greeting shift ("doesn't look up — doesn't need to") in Maya-interior register. *"She watches me different sometimes"* points at Phase 3+ direction without promising specific scenes. Tip lifts Marge's own *"Don't whine"* (existing `node_talk` line) and adds *"The rest is on her"* — Maya recognizing Marge is the one who'll decide what happens next, register-correct for the matriarch-dom arc trajectory.

Purpose: **anti-blank-panel.** Marge's section never disappears from the Quests page in slice scope. The arc reads as "paused, continuing in Phase 3+" not "broken at trust 20."

---

## §5 Doctrine map — why this shape works

| Doctrine clause | How Doc 53 complies |
|---|---|
| Doc 24 §10.2 Lane vocabulary | Lane 1 = Relational only (1 new + 2 pre-existing). Lane 2/3 = empty per §1 adaptation. |
| Doc 24 §10.3 grid balance | Empty cells are honest for service-NPC slice register. No "menu game" feel — hub has 4 choices total, not 10. |
| Doc 24 §10.4 arc-flow | Lane 1 leads (hire + worked shifts via existing canvases). No Lane 2/3 consequences to light up because slice scope deferred that register. |
| Doc 30 §7.5 + §8.2 | Skeleton 2-tier preserved. No sexual content. Workplace seduction stays Phase 3+. |
| Doc 49 voice (Story Goals) | M1 + M2 prose is Maya-voice interior. No schedules, places, numbers, or trait keys. |
| Doc 50 R1 capstone coverage | M1's `ready_canvas` points at `canvas_marge_interview` (existing priority-9 one-shot). ✓ |
| Doc 50 R2 climbing-bullet | M2 has `goals` block for trust 0→20. ✓ |
| Doc 50 R3 terminal placement | No terminal card in slice; nothing to violate. R3 N/A. |
| Doc 50 R4 chain continuity | M2's "post-hire" requirement has M1 (whose `ready_canvas` sets `hired_at_diner`) as predecessor. ✓ |
| Doc 50 R5 mechanic-tier `# unlocks:` | M2's comment names the greeting tier flip (the one thing that actually unlocks). ✓ |
| Doc 50 R6 label voice | "Marge trust" not raw key. ✓ |
| `feedback_tls_scene_body_style` | One new canvas body (regular_chat) is < 30 words, speaker-tag + 1-line dialog, no atmosphere, no inferential prose. ✓ |

---

## §6 Acceptance criteria (E-checkpoint)

Implementation is complete when ALL of these land:

1. `npc_marge` has `[[npcs.schedules]]` declared (Mon–Sat 09:00–22:00 at `loc_diner_front`). Closes the existing validator warning.
2. `scene_marge_diner_hub` re-authored: base node has image + 2-tier state-reactive opening (paragraph + dialog per tier). Exit_block has 8 menu choices + Leave, with 4 locked-visible escalation rungs (Tease / Flash / Eat / Take) gated by player corruption. Two new inline nodes: `node_pour_coffee` + `node_regular_chat`. Pre-existing `node_shifts` + `node_talk` preserved unchanged. Leave routes to `loc_main_street_sidewalk`.
3. Four Phase 3+ stub canvases authored — `tease_diner_marge`, `flash_diner_marge`, `marge_eat_her_out`, `marge_let_her_take`. Each has NO `[canvases.trigger]` block (Frank's tease/flash pattern — reachable only via hub routing). Single placeholder paragraph. Phase 3+ authoring replaces placeholders with full prose.
4. `scene_diner_t1_shift` exit effect includes `+2 marge.trust`.
5. M1 + M2 quest cards authored in `7_final_game.toml`, ordered after Frank F6 and before Ryan R1.
6. **Validator:** ✓ Validation passed. Marge no-schedule warning resolved. Frank bedroom-overlap warning remains (pre-existing, unrelated).
7. **Live-play smoke test:**
   - Day 1 pre-hire: M1 shows 🔓 Ready on the Quests page. Walking into the diner fires `canvas_marge_interview` (existing).
   - Post-hire: hub menu shows 4 unlocked items + 4 greyed-out escalation rungs + Leave. M2 appears with "Marge trust — 0/20" bullet. T0 shift fires at 17:00 location-entry. Trust increments by 1 per shift.
   - After ~20 worked shifts: M2's goal bullet turns ✓ (allMet). Hub greeting + T1 paragraph flips ("Marge's at the register. She doesn't look up — doesn't need to."). Locked rungs stay greyed (corruption gates still unmet).
8. **Voice audit:** every line in new content passes RTS-flat rules. A reviewer reads each new line + asks *"Could this appear in an RTS scene body?"* Yes for every line, no exceptions.

---

## §7 Anti-patterns (what NOT to repeat from the Doc 51 build)

Lifted from today's strip-and-audit:

- **Adding more hub items to drive trust climb.** The shifts ARE the climb. Hub items are minor relational filler, capped at 1–2 new items.
- **Lane 2 ambients without physical/charged contact.** Marge has no register for it; the surface should not exist. The Doc 51 build had 6 such ambients; all were pure padding.
- **Lane 3 substitutions without a walk-in payoff.** Same reasoning. The Doc 51 build had 3 substitutions + 2 dispatcher activities; all were padding.
- **3-tier ladder where Doc 30 §8.2 says 2-tier.** Slice scope decisions are load-bearing; don't force a third tier to fit a doctrine that wasn't asking for it.
- **Literary canvas prose.** Phrases like *"napkin holder needs refilling," "she's seen you take it twice now," "she doesn't sit, she never sits"* are Tier-3 density on a flat surface. Per `feedback_tls_scene_body_style` they're explicitly banned outside Tier-3 carve-outs.
- **Maya-voice with player directives in tip lines.** *"Walk into the diner. Don't wait for an invitation."* — Maya observes; she doesn't instruct.
- **Cookie content inside Marge's lanes.** Defer Cookie entirely. The Doc 51 build authored 3 Cookie-touching surfaces inside Marge's hub; none of them belonged.
- **Forcing the 3-lane framework on a service NPC.** Lanes 2/3 are register-specific. Empty cells are honest. Filling them with relational/atmospheric texture violates Doc 24 §10.3.

---

## §8 Cross-references

### Doctrine docs
- **Doc 24** — RTS Three Lanes (especially §10 — the doctrine §1 of this brief adapts for service NPCs)
- **Doc 30** — TLS Test Redesign PRD (§7.5 Marge Phase 3+ deferral, §8.2 slice minimum contract = 2-tier skeleton)
- **Doc 49** — Story Goals vs Sidebar Doctrine (quest card text/tip/ready_text voice rules)
- **Doc 50** — Quest Card Shape Doctrine (M1 capstone + M2 mechanic compliance walked in §5)
- **Doc 51** — Marge Design Brief (⚠️ SUPERSEDED by this doc; historical record)

### Memory
- `feedback_tls_scene_body_style` — RTS-flat doctrine + 8 style rules + content-selection rule
- `feedback_rts_objective_quest_doctrine` — Story Goals doctrine background
- `quest_card_shape_doctrine` — Doc 50 memory entry
- `marge_implementation_shipped` — historical record of the Doc 51 build that was stripped today

### Live TLS (current TOML state)
- `npc_marge` def: `7_final_game.toml:525–533`
- Hire canvas: `7_final_game.toml:1595+` (`canvas_marge_interview`)
- Hub: `7_final_game.toml:7798+` (`scene_marge_diner_hub`)
- T0 shift: `7_final_game.toml:9892+` (`scene_diner_t0_shift`) — grants +1 marge.trust on completion
- T1 shift: `7_final_game.toml:9960+` (`scene_diner_t1_shift`) — Maya-stat-gated, no marge.trust currently

---

## Appendix A — Implementation pre-ship checklist

When the implementation lands (separate plan), the merge gate is:

- [ ] **NPC schedule** — `[[npcs.schedules]]` block added; validator warning resolved.
- [ ] **Hub menu** — exactly 4 choices total (Shifts / Talk / Regular / Leave). No additions beyond `node_regular_chat`.
- [ ] **Hub greeting groups** — unchanged. T0 lt 20 / T1 gte 20. No T2 added.
- [ ] **T1 shift trust effect** — `+2 marge.trust` added to exit choice effects.
- [ ] **Quest cards** — exactly two new cards (M1 + M2). No M3, no M4, no terminal.
- [ ] **Canvas body** — `node_regular_chat` body matches the RTS-flat template in §3. < 30 words. Speaker tags + dialog only.
- [ ] **Voice audit** — every line in M1/M2/regular_chat passes §2 rules. RTS-flat for canvas; Maya-interior for quest cards.
- [ ] **Build canonical path** — output at `games/the_long_summer_test/output/`, not `/tmp`.
- [ ] **Live-play smoke test** — chain reachable per §6.6.
