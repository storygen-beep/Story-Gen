# Doc 50 — Quest Card Shape Doctrine

**Session:** 2026-05-24
**Branch:** `feature/prd-48-quests-engine-v2-bundled` (off `main`, unpushed)
**Author:** ENI (with LO)
**Status:** Doctrine — applies to all current and future TLS-engine games using `quests_engine = "v2"`
**Sibling of:** Doc 49 (Story Goals vs Sidebar Doctrine). Doc 49 = *where does this belong?* Doc 50 = *given it's a card, how must the card be shaped?*
**Supersedes:** nothing. Codifies rules that Doc 47 + PRD 48 + the Frank slice authoring experience implied, but that no single doc has held until now.
**Triggered by:** the Frank-slice quest-card audit on 2026-05-24. F3 shipped without a `goals` bullet. Sleepover + Diana confrontation capstones shipped without quest cards pointing at them. Doc 47 §7's walked example contradicted the live canvases. All four were violations against rules we'd never written down — so we wrote them down.

---

## 1. The question this doc answers

You've decided a surface belongs in `[[quest_cards]]` (per Doc 49 §6). Now you're staring at the TOML wondering: *how must the card itself be shaped? What rules MUST it follow before it's safe to ship?*

The one-line rule:

> **Every card declares its mode (capstone / mechanic / hybrid), surfaces its climb visibly, and points at something that exists.**

The six hard rules in §4 are the mechanical floor. The voice rules in §5 are the doctrine floor. §6 names which of those a future validator can mechanize and which stay human-read forever.

---

## 2. The three card modes

The fundamental taxonomy. Every quest card is exactly one of these.

| Mode | What the player is doing | 🎯 frame shows | 🔓 frame shows | Live example |
|---|---|---|---|---|
| **Capstone** | Climbing toward a scripted scene that will fire | `goals` bullets toward the scene's gate | 🔓 Ready + 📍 + 🕒 pulled from the scene's metadata | Frank F1–F5 (today's slice) |
| **Mechanic** | Climbing toward a content unlock with no scripted scene — a stat threshold opens a menu item, a hub group, a substitution rule, a `[group]` block | `goals` bullets toward the threshold | (mechanic cards typically have NO Ready frame — the threshold cross IS the unlock; the picker swaps to the next template automatically) | Ryan R1 (trust → 10) |
| **Hybrid** | The arc transitions modes mid-stream — early tiers are mechanic, later tiers are capstone (or vice versa) | Whichever bullets are climbing at the current tier | Whichever the current-tier card points at | Ryan full arc (R1 mechanic → R2 wait → R3 capstone-ish) |

Cross-reference: Doc 47 §6 six-situation matrix is the **row-level** version of this table — it walks individual state-windows. Doc 50 §2 is the **card-level** version — it classifies the card you're authoring as a whole. A hybrid arc contains multiple cards; each individual card is one mode at a time.

---

## 3. Picking the mode (3-question decision rule)

Before you author the card, run this check. Stop at the first match.

1. Is the next thing the player must do **gated by a scripted scene firing** (a canvas with `priority ≥ 9`, `is_repeatable = false`, and an effect that sets a flag)?
   → **Capstone**. Card has `ready_canvas` pointing at the scene. If the scene's trigger conditions include trait gates above what the card's `when` enforces, card also has a `goals` block surfacing the climb.

2. Is the next thing the player must do **gated by a stat crossing a threshold**, after which new content opens *without* a scripted scene — a new menu item appears, a `[group]` block becomes eligible, a substitution rule activates?
   → **Mechanic**. Card has `goals` but NO `ready_canvas`. The threshold cross IS the unlock; the V2 picker swaps to the next template the moment routing conditions change.

3. Is the arc itself mid-transition (this card is mechanic, the next will be capstone — or the inverse)?
   → **Hybrid arc**. Author each card according to rule 1 or 2 for its own tier. The arc-level shape doesn't change how an individual card is built.

If you can't decide between the three: the surface is probably wrong. Re-read Doc 49 §6 — what you're trying to express might not belong in `[[quest_cards]]` at all. Body-state needs go to `[[sidebar_items]]`.

---

## 4. Hard rules — what MUST be true before shipping a card

These are the mechanical rules. Most are validatable; §6 calls out the human-review subset.

### R1. Capstone coverage

Every canvas with `priority ≥ 9` + `is_repeatable = false` + a flag-setting effect MUST be referenced by some quest_card's `ready_canvas` field — OR be explicitly marked off-panel with a single-line comment on the canvas:

```toml
# off-panel: reached via setter-menu only; not a quest-pointed milestone
```

No silent off-panel capstones. The off-panel marker is a design choice that needs to be visible to the next author reading the canvas. *Why this rule exists:* sleepover (before 2026-05-24) was off-panel by accident, not by decision — `scene_frank_sleepover` shipped to production and was reachable only via the bedroom setter menu, with no quest-panel pointer. Same for Diana confrontation.

### R2. Climbing-bullet rule

If a card has a `ready_canvas`, AND the `ready_canvas`'s trigger conditions include a trait gate strictly above what the card's `when` clause enforces, the card MUST have a `goals` block surfacing that trait climb.

Concrete check: read your card's `ready_canvas`. Read that canvas's `conditions.items`. For every trait condition, ask *"is this value strictly above what my card's `when` already guarantees?"* If yes, the player needs a `goals` bullet to know about it. *Why:* F3 (before 2026-05-24) shipped without one — player completed first-night, saw F3 say *"He took me upstairs. He hasn't said the word yet,"* and had no visibility into the corruption 25 → 35 climb gating declaration.

### R3. Terminal placement

A card with `terminal = true` MUST be the LAST card in its NPC chain. No flag in its `when` may permit unmet subsequent cards.

Concrete check: list every card for this NPC. Find the one with `terminal = true`. Confirm no other card has a `when` requiring a flag set AFTER the terminal's flag fires. *Why:* old F4 (before 2026-05-24) was terminal at `frank_cracked` (the declaration capstone) while sleepover + Diana capstones still existed downstream with their own setter flags. The arc closed on the panel two scenes too early.

### R4. Chain continuity

Every "post-X" card (one whose `when` requires `flag_X = is_true`) MUST have a sibling "pre-X" card whose `ready_canvas` points at the canvas that sets X.

Concrete check: for each card, identify the flag it requires to be true. Confirm another card in the chain points at the canvas that sets that flag. *Why:* prevents floating cards that activate from states the player has no narrative path into.

### R5. Mechanic-tier explicit unlock

A pure-mechanic card (no `ready_canvas`) MUST carry a one-line author comment naming what content opens when the threshold lands. Format:

```toml
# unlocks: <slug>_hub menu item "X" at npc_<slug>.trust >= 10
```

Or for substitution-rule unlocks:

```toml
# unlocks: substitution beat <slug> when worn_corruption >= 25
```

*Why this rule exists:* validators can't see "what's behind the threshold." A mechanic card without this comment can ship pointing at vapor — the threshold crosses and nothing actually changes for the player. The comment makes the unlock greppable and reviewable.

### R6. Goals labels in voice

`goals[i].label` MUST be in Maya-voice or in-character framing — *"Maya's corruption,"* *"Diana noticing,"* *"Yard help,"* *"Ryan trust."* Never raw trait keys like `npc_diana.awareness` or `core_traits.corruption`.

The label renders directly under the 🎯 frame in the player UI. It's a narrative surface, not a debug surface.

---

## 5. Voice rules — narrative fields

Tightening `feedback_hint_narrative_no_time_or_location` for the card context.

| Field | Voice | May NOT contain |
|---|---|---|
| `text` | Maya, first-person, in-character | location names, schedules, numbers, NPC mechanics jargon, trait keys, flag names |
| `ready_text` | Maya, the "moment is on her" line | same as `text` |
| `tip` | Maya or in-scene observer | same as `text` |
| `goals[i].label` | In-character, allowed to name the thing being climbed | trait key strings, flag names, raw stat references, debug labels |

Schedule + location + threshold numbers surface automatically — from `ready_canvas` metadata for capstone cards, from `goals` evaluation for mechanic cards. Authors never write them into prose.

What this looks like in practice — F4 (post-declaration / pre-sleepover):

```toml
text         = "He moved the line. The bedroom is the venue now."
ready_text   = "Tonight I don't leave."
tip          = "Diana down the hall. Quiet."
ready_canvas = "scene_frank_sleepover"
goals = [
  { trait = "corruption", subject = "player", op = "gte", value = 50, label = "Maya's corruption" },
]
```

The player sees Maya's voice. The mechanical surface — *📍 Frank's bedroom, 🕒 Mon–Fri 21:00–23:00, Maya's corruption 42 / 50* — is rendered by the engine from the canvas's own metadata and the live trait value. Author never writes those numbers or place names.

---

## 6. Validators vs human-review split

The honest table of what mechanizes and what doesn't.

| Rule | Validatable? | Who catches if violated | Severity |
|---|---|---|---|
| R1 capstone coverage | ✅ full | engine validator (proposed) | error |
| R2 climbing-bullet | ✅ full | engine validator (proposed) | warning |
| R3 terminal placement | ✅ full | engine validator (proposed) | error |
| R4 chain continuity | ✅ full | engine validator (proposed) | warning |
| R5 mechanic-tier comment | ⚠️ partial | grep for `# unlocks:` pattern, otherwise human read | warning |
| R6 label voice | ❌ | human read at code review | warning |
| §5 narrative voice | ❌ | human read | warning |
| "Is this story-shaped or chore-shaped?" (Doc 49 §3 anti-pattern) | ❌ | human read against Doc 49 §6 | error |

Roughly half the shape failures we'd want to catch are validatable. The other half need a human read. Validators are necessary but not sufficient — don't ship them and assume the panel is healthy. The settle-in failure (2026-05-17) and the Frank chain failures (2026-05-24) had different shapes; only R1–R4 would have caught the second set, and nothing automated would have caught the first.

The validator PRD (when prioritized) wires up R1–R4 plus the grep half of R5. Doc 50 names the rules; the PRD implements them.

---

## 7. Worked case study — Frank's six-card chain (shipped 2026-05-24)

Walk every card in `games/the_long_summer_test/toml_phases/7_final_game.toml` F1–F6 (lines 2439–2535). Each row annotates which rules apply and where today's fix landed.

| Card | Mode | `ready_canvas` | `goals` | Rule applications |
|---|---|---|---|---|
| **F1** Pre-catch | Capstone | `scene_livingroom_catch` (corr ≥ 25) | corruption ≥ 25 | R1 ✓ (catch covered), R2 ✓ (bullet for the 0 → 25 climb), R4 ✓ (chain root — no predecessor needed) |
| **F2** Pre-first-night | Capstone | `scene_franks_bedroom_evening` (corr ≥ 25 — already met from catch threshold) | — (correctly omitted) | R1 ✓, R2 N/A (no climb above `when` flag), R4 ✓ (F1 sets `frank_caught`) |
| **F3** Pre-declaration | Capstone | `scene_frank_declaration` (corr ≥ 35) | corruption ≥ 35, label "Maya's corruption" | **R2 ✓ — THIS IS THE FIX** from 2026-05-24. Before today, F3 violated R2 — corr 25 → 35 climb was invisible. R4 ✓ (F2 sets `frank_bedroom_first_done`). |
| **F4** Pre-sleepover | Capstone | `scene_frank_sleepover` (corr ≥ 50) | corruption ≥ 50, label "Maya's corruption" | **R1 ✓ — THIS IS THE FIX.** Before today, sleepover was off-panel and F4 incorrectly held the terminal slot. **R2 ✓** for the 35 → 50 climb. R4 ✓ (F3 sets `frank_cracked`). |
| **F5** Pre-Diana | Capstone | `scene_diana_confrontation` (`npc_diana.awareness` ≥ 8) | awareness ≥ 8, label "Diana noticing" | **R1 ✓ — THIS IS THE FIX.** Diana confrontation was off-panel before today. **R2 ✓** for the awareness 0 → 8 climb. **R6 ✓** — label is *"Diana noticing,"* not `npc_diana.awareness`. R4 ✓ (F4 sets `frank_sleepover_done`). |
| **F6** Terminal | Terminal (sub-mode of Capstone) | — | — | **R3 ✓** — terminal is now the last card, fires only on `diana_confronted` (last flag in chain). Before today, F4 held terminal at `frank_cracked` — two scenes too early. |

The Frank slice is a clean teaching example: every rule fires at least once across the six cards. Future authors can copy this shape directly — *"be Frank-shaped"* is a fair shorthand for *"comply with Doc 50."*

What today's fix touched in rule terms:
- R1 violated by sleepover + Diana off-panel → fixed by adding F4's `ready_canvas` repurpose + F5 entirely new
- R2 violated by F3 missing goals → fixed by adding the corruption bullet
- R3 violated by F4 being terminal too early → fixed by moving terminal to F6
- R4 not violated (chain was internally consistent on the flags it had)
- R5 not applicable (Frank's arc has no pure-mechanic tiers)
- R6 trivially satisfied (existing labels were already in voice)

---

## 8. Anti-patterns — concrete shapes to NOT ship

- **Climbing card with no `goals` bullet.** F3 before today. Card looks correct in TOML; UI shows narrative text with no progress indicator; player is blind to the gate. Caught by R2.
- **Capstone canvas with no card pointing at it.** Sleepover + Diana confrontation before today. Scene exists in the game; player has no path to it from the quest panel. Caught by R1.
- **Premature terminal.** Old F4 closing the arc at `frank_cracked` while sleepover + Diana still existed downstream. The panel says *"arc complete"* while the player still has scenes to discover. Caught by R3.
- **Floating post-X card.** A card requiring `flag_X is_true` with no sibling card setting up X via its `ready_canvas`. Player reaches a state with no narrative path through. Caught by R4.
- **Mechanic card pointing at vapor.** Pure-mechanic card whose threshold cross doesn't actually unlock anything — no menu item, no `[group]` block, no substitution rule. The bullet fills, the player crosses, nothing happens. Caught by grep against R5's `# unlocks:` comments — if no line, flag it.
- **Trait-key label.** `label = "npc_diana.awareness"` rendering raw to the player UI. Lazy authoring. Caught by R6 human review.
- **Doc walked-example contradicting live canvases.** Doc 47 §7 before today's fix walked Frank's arc as catch → declaration → first-night, but canvases gate as catch → first-night → declaration. Caught only by a human re-reading the doc against the TOML after either side changes.

---

## 9. Open questions / scoped-out

Things this doc deliberately does NOT cover. Each is its own future doc if it becomes load-bearing:

- **Pure-mechanic arc topology.** Ryan R1–R3 are not deeply audited here. The R5 question (*"is this threshold pointing at real content?"*) is doctrine-shaped, but the Ryan/Jake audit itself is separate work. If a future audit surfaces patterns specific to mechanic arcs, Doc 51 (mechanic-arc doctrine) is the natural home.
- **Per-NPC card audit ritual.** §6 mentions human review; Doc 49 §10 referenced this; the ritual itself (what's the checklist, when do you run it, what's the output) is its own doc if it becomes routine practice.
- **Capstone-coverage validator implementation.** Engine work, not doctrine. Belongs in a PRD when prioritized. Doc 50 names the rules; the validator PRD wires them up against `apps/projects/services/template_import.py`.
- **Diana / Marge zero-card audit.** Both NPCs currently have no `[[quest_cards]]`. Whether they SHOULD is a content decision, not a doctrine decision. If it's decided they should, Doc 50's rules apply to whatever lands.
- **Voice/tone audit of existing card prose.** Doc 50 names the rules; it does not re-audit every card already shipped. The Frank slice is canon; other NPCs can be checked against §5 when next touched.

---

## 10. References

### Sibling and ancestor docs
- **Doc 47** — Quests Page Unified Card Design (mechanics + §6 six-situation matrix that Doc 50 §2 is the card-level distillation of)
- **Doc 48** — Quests Engine V2 PRD (the schema + render engine Doc 50 assumes you're authoring against)
- **Doc 49** — Story Goals vs Sidebar Doctrine (the *where-does-it-belong* sibling)

### Memory entries
- `feedback_rts_objective_quest_doctrine` — the 2026-05-17 doctrine; the original "Story Goals aren't chore proxies" rule that Doc 49 generalized
- `feedback_hint_narrative_no_time_or_location` — Maya voice in card narrative copy
- `prd_48_quests_engine_v2` — the V2 engine implementation log

### Live TLS reference
- `games/the_long_summer_test/toml_phases/7_final_game.toml:2439–2535` — Frank F1–F6 (the §7 case study)
- `games/the_long_summer_test/toml_phases/7_final_game.toml:2498–2528` — Ryan R1–R3 (the hybrid-arc reference for §2 / §3)

### Engine
- `apps/projects/services/template_import.py` — where future R1–R4 validators would live (next to the existing `_validate_quests_cards` function)
- `apps/game_generation/twee_comprehensive/generators/v2.py` — the V2 render path (`renderQuestsGoalBlock`, `_isHintReady`, `getStageHintForNPC`)

---

## Appendix A — Pre-ship checklist

Copy this into the PR description (or run it in your head) before merging any card change:

- [ ] **Mode declared.** I know whether this card is capstone, mechanic, or hybrid-tier. (§2 / §3)
- [ ] **R1 capstone coverage.** Every priority-9+ one-shot flag-setting canvas in scope is either referenced by a card's `ready_canvas` or has an off-panel comment.
- [ ] **R2 climbing-bullet.** If the card has `ready_canvas` with trait gates above the card's `when`, a `goals` block surfaces the climb.
- [ ] **R3 terminal placement.** Any `terminal = true` card is the last in its NPC chain.
- [ ] **R4 chain continuity.** Every "post-X" card has a sibling "pre-X" card pointing at X's setter.
- [ ] **R5 mechanic comment.** Every pure-mechanic card has a `# unlocks:` comment.
- [ ] **R6 label voice.** Every `goals[i].label` reads in-character.
- [ ] **§5 narrative voice.** `text` / `ready_text` / `tip` contain no place names, schedules, numbers, or jargon.
- [ ] **Doc-canvas alignment.** If this change touches scene gates referenced by any design doc, the doc's walked example still matches the canvases.
