# QA Rubric — Per-Canvas Pass/Fail

> **Run this before claiming any canvas done.**
> Binary checklist. "Mostly good" fails. Every box must be ticked.

## Hygiene (mechanical — fix these first)

- [ ] **No `@npc_xxx` tokens in any paragraph or dialog `content` field.** Tokens valid in `npcId` props only. Grep: `grep '@npc_' <canvas_block>` returns zero matches in body content.
- [ ] **No banned phrases.** Run mental search for: heart pounding, drunk on, electric, every fiber, delve into, leverage, navigate, robust, seamless, innovate, empower, cutting-edge, streamline. Any hit = fail.
- [ ] **Media blocks present.** ≥1 `type = "image"` or `type = "video"` block per scene beat. Each has `file`, `description`, ≥3 `search_queries`.
- [ ] **`package_from_toml --dry-run` passes** after rebuild of `6_final_game.toml`. Counts match expected (79 + N for Option B node additions). Zero new flag-graph errors. Sibling-canvas overlap warnings stay at 12.

## Voice & POV

- [ ] **Maya narrates in third-person close + free indirect discourse.** No "she thought." No italicized internal thoughts. The narration borrows her voice.
- [ ] **Per-NPC voice from style sheet, every dialog line.** Frank-line passes the contraction-drop test under serious pressure. Ryan-line passes the fragment test. Jake-line passes the bimodal test. Diana finishes her sentences. Marge clips. Cookie monologues with intel.
- [ ] **Body before emotion.** No line of the form "she felt X" without a physical or sensory antecedent. Show position, gesture, sensation; let interior meaning emerge.

## Specificity

- [ ] **Specific nouns over generic.** *Yesterday's coffee, the one she hadn't dumped*, not *old coffee*. If a noun is generic, ask whether the character would have noticed it more specifically.
- [ ] **Smell embedded at least once per ~500 words.** Load-bearing not decorative. Maya breathes it in, names it, remembers it. Southern register: cheap coffee, pine resin, cicadas, red clay, cut grass, frying oil.
- [ ] **One corruption noticing.** The arc happens here. Maya-at-this-corruption-band sees one thing Maya-of-last-week wouldn't have. Distributed self-recognition: she does not announce her change; the world-seen-through-her shows it.

## Choice text

- [ ] **Each label is a clear in-character action.** Button text alone tells the player what Maya does.
- [ ] **The set of labels makes the player feel three different Mayas** (or two, or four — but distinct, not volume dials).
- [ ] **No "Continue," "Yes," "No," "Back," "Cancel" as label text** — unless it's the Prologue's deliberate sequential-narrative pacing.
- [ ] **No `@npc_xxx` tokens in choice text.**
- [ ] **No parenthetical stage directions in labels** — *(stand up)*, *(eye contact held)*. Move to result body.
- [ ] **≤20 words per label.**
- [ ] **No two choices in the same set have identical effects.** (Unless the choice is genuinely cosmetic and the design needs it — flag in commentary if so.)

## Structure

- [ ] **Failbetter density at the right tier.** Tier A: 1500-2500 words across multi-node mini-arc. Tier B: 800-1500. Tier C: 400-700. Tier D: 400-600 per shift body, with rotations. Tier E: 300-500 incl. variants. Tier F: 150-300 (mirror_look special at ~600).
- [ ] **Setup-first, payoff-late.** The choice has setup before it. Not a one-line scene followed by a three-button menu.
- [ ] **One scene = one decision.** If the passage carries a chain of actions+consequences, split into more nodes.

## Variants & repeatables (where applicable)

- [ ] **Variants are tonally different, not lexically swapped.** DEFAULT/WITHDRAWN/WARM/CONSEQUENCE blocks have 3-5 sentences of distinct prose with different rhythm and stance. Not the same sentence with three adjectives.
- [ ] **Rotating openings on dailies.** Tier D and Tier F repeatables: 3-5 alternate first lines so the 15th read isn't the same as the 3rd.
- [ ] **Rare-event injection on Tier D shifts.** 5-10% block-pool entries that are one-offs.

## Corruption-band fidelity (where applicable)

- [ ] **The narrator changes between bands, not just the verb.** Closed Maya and Saturated Maya read like different writers narrating the same person. Reference `corruption_band_register.md`.
- [ ] **Art-as-honesty escape valve at high corruption.** If the scene is Operating-band or Saturated-band, can Maya sketch something honest somewhere in it? If no, the scene may be over-compressed.

## Trigger-prose binding (where applicable)

- [ ] **No hardcoded weekday / hour / week / season in prose unless the canvas trigger enforces it.** Scan every paragraph and dialog block for: weekday names (Mon–Sun), specific clock times (*"at eight-thirty,"* *"one in the morning"*), week-number references (*"Week 4,"* *"the fourth week"*), month/season tells (*"early July,"* *"late summer"*). For each hit: verify the canvas has a `[[canvases.trigger.schedules]]` entry with `weekdays = [N]` (0=Mon..6=Sun) / `start_time` / `end_time` matching the prose, or a `trigger.conditions.items` entry gating on a `week_N_reached` flag set by the daily-tick canvas. If the prose claims a specificity the trigger doesn't enforce, either (a) add the schedule/condition, or (b) rewrite to neutral framing (*"an evening," "later that week," "by the time"*). Reference: standards.md Rule 27.
- [ ] **No retconned Maya-actions without an upstream flag.** Scan for past-action narration patterns: *"she had Xed,"* *"the day she Xed,"* *"the morning after she Xed."* For each: confirm a flag tracks the X event and is set by an upstream activity/canvas the player actually triggered. If no flag exists, either (a) add the upstream flag plumbing, or (b) rewrite the prose to describe consequence-without-retcon (the room shows the result; Frank reacts to it; the act itself is not claimed to have happened). Reference: standards.md Rule 28.

## Per-NPC voice spot-check

- [ ] **Frank dialog under pressure has zero contractions.**
- [ ] **Ryan dialog is fragments throughout** (single complete sentence allowed only at Beach Crack).
- [ ] **Jake dialog is bimodal** — clipped under pressure, vocabulary-deploying when comfortable. No mid-length casual.
- [ ] **Diana finishes her sentences and does not ask the question she does not want the answer to.**
- [ ] **Marge speaks only what is necessary, no endearments, no moralizing.**
- [ ] **Cookie talks while she works, transfers intel, no judgment.**

## Sign-off

When every box is ticked:
- [ ] Update `priority_queue.yaml` — set status to `done`, fill `actual_words`, append note
- [ ] Append entry to `session_log.md` (1-3 lines: canvas id, what changed, dry-run status)

If even one box fails: status stays `in_progress` and the canvas is not done.
