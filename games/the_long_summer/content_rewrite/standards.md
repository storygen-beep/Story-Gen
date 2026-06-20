# Standards — TLS Canvas Content Rewrite

> **The 27 craft rules every canvas must satisfy.**
> Distilled from web research (Ashwell / Short / Ingold / Kennedy / Failbetter / Dias / COG / DoL / sub-Q) + four explored-game craft mining (Shady Deals, New Life Project, Road to Success, Emilie). Apply this checklist before claiming any canvas done.

## How to use

For every canvas you rewrite:
1. Read this file
2. Read the relevant style sheets (`style_sheets/<npc>.md` for any NPC in the scene + always `style_sheets/maya.md`)
3. Read `corruption_band_register.md` if the canvas has corruption-band variants
4. Read `choice_label_patterns.md` before writing any exit_block.choices
5. Write
6. Run through `qa_rubric.md` self-check

## The 27 rules

### Structure

**1. Use Failbetter density as the norm.** Passage intros ~30 words; result/outcome passages ~100 words; choice labels ≤20 words. Tier-A and Tier-B Cracks earn longer (Prologue node density: 400-2000 words per sub-node). Tier-D dailies and Tier-F solos stay tight. Source: Failbetter writer guidelines.

**2. Setup-first, payoff-late.** A choice's weight comes from what precedes it, not what branches from it. Build five sentences of setup before one sentence of decision. Source: Ingold (inkle).

**3. Get in late, leave early.** Open the scene at the moment something changes; close it just past the change. Don't write the walk-up, don't write the cooldown. Source: Kennedy (Failbetter).

**4. One scene = one decision.** A passage resolves *one* action and its consequence, not a chain. If it would carry a chain, split it into more nodes. Source: Failbetter.

**5. Respect the corruption band.** Every scene has a corruption tier (read the trigger conditions). Maya-of-this-band narrates, observes, and chooses differently than Maya-of-last-week. Pull the right voice from `corruption_band_register.md`.

### Voice & POV

**6. Third-person close + free indirect discourse.** Narration borrows Maya's vocabulary, rhythm, and emotional coloring without quoting it. Never write "she thought," never italicize a thought. Source: FID literature; Prologue exemplar.

**7. Per-NPC voice from the style sheet, every line.** Frank drops contractions in serious moments. Ryan fragments. Jake is bimodal (clipped or vocabulary-heavy). Diana finishes her sentences. Marge clips. Cookie monologues. Every NPC dialog line is a voice-sheet test.

**8. Body before emotion.** Show position, gesture, sensation. Let interior meaning emerge from the body and the room, not from a narrator-explainer. *"His knuckles whitened on the steering wheel"* not *"He felt frustrated."*

**9. Specificity of noun.** *"Yesterday's coffee, the one she hadn't dumped"* not *"old coffee."* *"The water mark in the shape of a comma by the vent"* not *"the stain on the ceiling."* If a noun is generic, find the specific thing the character would have noticed.

**10. Smell every ~500 words, load-bearing.** Southern register: cheap coffee, pine resin, cicadas, red clay, cut grass, frying oil, two-day sweat on a t-shirt, gasoline at the pump. Smell is *inhabited* — Maya breathes it in — not decorative.

### Choices

**11. Every option has real consequences.** Stat changes count, but no two choices in one set should have *identical* effects. The Tier-D T0 identical-payouts is the canonical violation; do not repeat. Source: COG rule 1.

**12. The set of options does character work.** Three choices in one block = three different Mayas making the *same* mechanical move feel different. *"Agree coldly / Say nothing / Nod"* is the canonical pattern (Dias, sub-Q).

**13. Choice labels = clear in-character action.** Button text alone tells the player what Maya will do. Not *"Continue"* — *"Walk the long way."* Not *"Yes"* — *"Stay."* Source: Failbetter.

**14. No false backpedaling.** Once a choice is offered, the chosen option is canon. Never offer an extreme option and have the narrative undercut the player who took it. Source: Dias.

**15. Choice labels reveal tone, not consequence.** *"Let him buy you another drink"* telegraphs accept, not what accepting unlocks. Hide the branch's content behind the character-move; reveal mechanical cost (time, money) only when diegetic. Source: Dias + adult-IF practice.

**16. 3 choices is the default; 4 when a mechanical option is needed; 5 maximum.** Two feels binary; six+ overwhelms scanning.

**17. Player agency where it exists.** If Maya has agency in the moment, she gets choices. If she doesn't (auto-shower, Diana sets a place at dinner), she doesn't. Don't fake agency — but don't deny it where it exists.

### Variants & repeatables

**18. Variants must be tonally different, not lexically swapped.** DEFAULT / WITHDRAWN / WARM / CONSEQUENCE blocks need 3-5 sentences of distinct prose with different rhythm and stance — not the same sentence with three adjectives swapped. Source: sub-Q (generative prose), DoL practice.

**19. Rotating openings on dailies.** Anti-staleness: 3-5 alternate first lines per repeatable activity. Even small first-line variation makes the 15th read feel like the 3rd. Source: Short (procedural text essays).

**20. 5-10% rare-event injection on high-replay activities.** Tier-D shifts especially. A Cookie moment, a customer incident, a weather thing — breaks the loop without branching the graph. Source: Short, NLP/Shady Deals practice.

### Corruption arc & accumulation

**21. One corruption noticing per scene.** The arc happens here. Maya-at-this-tier sees one thing Maya-of-last-week wouldn't have. Distributed self-recognition: never have her announce her change; let the world-seen-through-her do it. Source: DoL practice + author reasoning.

**22. Art-as-honesty escape valve at high corruption.** Sketchbook prose stays clean. When she sketches, the corruption-band register briefly inverts. This is the diagnostic — if a scene at Operating-band can't find a moment where Maya could sketch something honest, the scene is over-compressed.

### Production hygiene

**23. Strip every `@npc_xxx` token from paragraph and dialog `content` fields.** Write the actual character name instead.

> **Note — this is a craft-hygiene rule, not a correctness fix.** The engine technically resolves these tokens at render time (`v1.py:9703` via `_resolve_at_references` — for non-customizable NPCs they render as the fixed name; for customizable NPCs they inject `<<print $npcs["uuid"].name>>`). So a scene with `@npc_ryan` in the body will *render correctly* in the HTML output. The reason we strip anyway: it keeps the writer in novel-prose mode ("I'm writing about Ryan," not "I'm authoring a template against a token registry"), and the source file reads cleaner on review. Tokens remain valid — and required — in `npcId` props inside `dialog` blocks.

**24. Author media blocks even when the file doesn't exist.** Every scene beat gets ≥1 image or video block with `file`, `description`, and ≥3 `search_queries`. Files retrieved separately. Don't skip.

**25. Validate after every canvas.** Run `package_from_toml --dry-run` on the rebuilt `6_final_game.toml`. Counts must match expected (79 + N for Option B node additions). Zero new flag-graph errors. 12 sibling-canvas overlap warnings stay at 12.

### Typography (added Session 2.5)

**26. Inline typography is the last tool, not the first.**

If the prose lands the weight, typography is unnecessary. If the prose fails to land, typography is a symptom treatment, not a cure. Use typography only when there is a *register distinction* that narration alone cannot carry — never for emphasis.

| Marker | Authoring | Use for | Don't use for |
|---|---|---|---|
| `*italic*` | Markdown-style asterisks (engine regex at `v1.py:9706`) | (a) FID-thought beats where narration names what Maya is doing or registering; (b) memory intrusion mid-scene; (c) textual objects she is *reading* not speaking; (d) verbal tics / signature phrases quoted inside narration without being spoken | Generic emphasis. Cadence cap: ≤1 italic span per ~400 words. |
| **Blockquote** — `<blockquote>...</blockquote>` as raw HTML inside a *separate* `paragraph` block | Raw HTML passthrough (`v1.py:9712`) | Moments Maya is *reading* a physical text — brochure, rent notice, ledger line, text message, sketchbook annotation. Sits visually apart from her narration. | Dialog. Dialog has its own block. |
| **Bold** — `<strong>` | Raw HTML | **Mechanical UI only** — engine already uses `<strong>` for speaker-name labels, money readouts, etc. *Not in prose.* | Emphasizing "important" narrative moments. Bold activates reader's game-brain; prose needs reader-brain. |
| **Highlight / `<mark>` / colored text** | Raw HTML | **Never.** Breaks literary register. Contradicts Rule 21 (distributed self-recognition — she doesn't announce her change; highlight IS an announcement). | Anything. |
| **Underline / strikethrough** | Raw HTML | **Never.** Underline reads as clickable link in web UI. Strikethrough reads as joke or deletion. Both drop out of novel register. | Anything. |

See `style_sheets/maya.md` ("Inline texture" subsection) for specimen italic uses and `choice_label_patterns.md` ("Reading physical text" subsection) for blockquote authoring pattern.

### Trigger-prose binding (added Session 22)

**27. Temporal coherence — prose-time matches enforced-time.**

If a paragraph or dialog block names a specific weekday (*Sunday*, *Thursday*), clock time (*at eight-thirty*, *one in the morning*), week number (*Week 4*, *the fourth week*), month or season (*early July*, *late summer*), or time-of-day requiring those (*the dusk that holds at eight-thirty*), the canvas must enforce that specificity through `[[canvases.trigger.schedules]]` (each entry holds `weekdays = [N]` with N in 0..6 Python convention 0=Mon..6=Sun, plus `start_time = "HH:MM"` and `end_time = "HH:MM"`) and/or `trigger.conditions` checking a `week_N_reached` flag set by an upstream weekly-tick canvas. If the canvas cannot enforce the specificity (the moment is gated only by a milestone flag that can fire across many days), rewrite the prose to neutral framing: *"an evening,"* *"later that week,"* *"by the time."* The engine supports the schedule schema fully (`v1.py:2106-2111`; existing TLS activities use it across `3_activities.toml`); 0 of 30 Phase-1 story canvases currently use it. Worked failure: `frank_phase_a_test` narrates Sunday W4 8:30 with no schedule block — fires Tuesday W3 3pm.

**28. Action causality — narrated past actions must be flag-real.**

If prose retcons a Maya-action — *"she had left the porch light on,"* *"the morning after she had taken the brochure,"* *"the day she had told him yes"* — the cited action must be a flag set by an upstream activity, choice, or canvas the player actually triggered. If no flag tracks the action, choose one: (a) add an upstream player-set flag and gate the canvas on it; (b) rewrite the prose to describe the consequence (Frank's complaint, the brochure on the desk, his expectation) without claiming Maya performed the act. Frank-arc canvases are highest-risk; descriptions like *"the porch light Maya forgot to turn off"* are fine, but *"she had flipped the toggle on Saturday at 1am"* is not — the latter asserts a specific player history the engine never recorded.

Both rules are auditable in under 60 seconds per canvas: list every concrete time/date/season/prior-action claim in the body blocks, confirm each maps to (i) a trigger condition, (ii) a schedule-block field, or (iii) an upstream flag the player actually sets. If a claim has none of those, the canvas fails the rule.

## Banned phrases (zero tolerance)

The design book bans these explicitly. Search-and-replace before claiming done:

- "heart pounding" / "pounding heart"
- "drunk on" (drunk on power, drunk on him, etc.)
- "electric" (the kiss was electric, etc.)
- "every fiber" (of her being, etc.)
- "delve into"
- "navigate" (used metaphorically)
- "leverage" (used as a verb)
- "robust"
- "seamless"
- "innovate" / "innovative"
- "empower" / "empowering"
- "cutting-edge"
- "streamline"

If any of these appear, the canvas fails the rubric.

## Sources cited (for reference / further reading)

- Sam Kabo Ashwell — *Standard Patterns in Choice-Based Games*
- Emily Short — *Beyond Branching*; *Procedural Text Generation in IF*; *Small-Scale Structures in CYOA*
- Jon Ingold (inkle) — interviews on choice rhythm
- Alexis Kennedy / Failbetter — *Fallen London Writer Guidelines* I-III
- Bruno Dias — *Branching Choices*, *Interiority*, *Generative Prose* (sub-Q)
- Choice of Games — *5 Rules for Writing Interesting Choices*
- Vrelnir — *Degrees of Lewdity* (Trauma/Control register-shift practice)
