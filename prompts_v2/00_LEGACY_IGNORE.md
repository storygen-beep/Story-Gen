# 00 — Legacy Ignore List

**Status:** Doctrine gate. Read first. Applies to every prompt in `prompts_v2/`.
**Authority:** LO decisions §6.3 + §6.7 in Doc 66 (`28th_april_TLS_Phase2_Redesign/66_Session_2026_05_26_Prompts_Rewrite_Pivot.md`, 2026-05-26).
**Purpose:** Name every legacy concept this corpus does NOT reach for. Each item below says *what to ignore* and *what to use instead.*

---

## §1 — Why this file exists

The pre-2026-04-19 prompt pipeline (`prompts/game_book_prompt_v6.txt`, `prompts/toml_generation_prompt_v4.txt`, the 12 doctrine + reference + media files alongside them) teaches an LLM to design **"any adult interactive game"** with selectable architectural shapes and a 15-pattern repeatable-content vocabulary.

That vocabulary produces games that do not match the post-Doc-24 RTS-shape sandbox doctrine. The legacy concepts are not subtly wrong — they answer a different question. Applied here, they corrupt the corpus from inside: the LLM reaches for the better-known older patterns when filling gaps the new doctrine does not yet cover.

**Single locked frame:** every game generated against `prompts_v2/` is an RTS-shape sandbox. One reference game (Road to Success). One mechanism vocabulary (Lane 1 / Lane 2 / Lane 3 + Lane 4 capstones). One arc-shape taxonomy (5 shapes). One voice register doctrine (RTS-flat default + Tier-3 capstones).

If a downstream file in `prompts_v2/` cites a legacy term, the citation is the bug.

---

## §2 — What this corpus replaces

| Concern | Legacy location | Replaced by |
|---|---|---|
| Game-book authoring prompt | `prompts/game_book_prompt_v6.txt` (frozen 2026-04-19) | `prompts_v2/stages/01_game_book_prompt.md` |
| TOML authoring prompt | `prompts/toml_generation_prompt_v4.txt` (frozen 2026-04-19) | `prompts_v2/stages/02_toml_generation_prompt.md` |
| Doctrine spec | `prompts/game_design_rules.md` + `game_design_patterns.md` + `game_design_motivations.md` + `game_design_observations.md` | `prompts_v2/doctrine/01–09` (complete: 01 / 02 / 03 / 04 / 05 / 06 / 07 / 08 / 09) |
| Engine schema reference | `prompts/COMPREHENSIVE_SYSTEM_REFERENCE.md` (embeds v3, no Docs 24–65) | `prompts_v2/schema/01–03` + regenerated `prompts_v2/COMPREHENSIVE_SYSTEM_REFERENCE.md` |
| Reference-game extraction | Jack's World + New In Town walkthroughs implicit in v6 | `prompts_v2/reference/01–04` (RTS only) |
| Media / image / listing prompts | `prompts/image_finder_prompt.md` + `prompts/game_listing_prompt.md` | `prompts_v2/stages/03–04` (ported) |

The legacy `prompts/` folder stays in place as historical record (LO decision §6.7 — no migration, no archival move). It is not consulted, not cited, not "carried over."

---

## §3 — Ignore list (do NOT reach for X; instead use Y)

Each row below names a legacy concept the LLM may know from training, from older prompts in the same repo, or from related adult-IF projects. Each row pairs it with the post-Doc-24 replacement.

### §3.1 — Reference games

| ❌ Do NOT reference | ✅ Instead use |
|---|---|
| **Jack's World** | **Road to Success (RTS)** as the sole reference game. RTS extraction lives in `prompts_v2/reference/01–04` + `28th_april_TLS_Phase2_Redesign/13_Road_To_Success_Reference.md` + `game_explorations/rts-arc-trace/`. |
| **New In Town** | Same — RTS only. |
| **Two Weeks** | Same — RTS only. |
| Any other adult-IF game referenced in legacy prompts | If the design book proposes a non-RTS reference, redirect to RTS shape. The mechanism vocabulary in `prompts_v2/doctrine/` is RTS-derived; non-RTS references will produce mechanism mismatches. |

**Why:** these games predate the 3-lane doctrine. Their mechanism vocabulary is Pattern A–J; their NPC architecture is the 7-driver system; their pacing is whiteboard-goals + narrative-gates. None of those translate cleanly into the RTS sandbox shape `prompts_v2/` builds toward.

### §3.2 — Repeatable-content mechanism

| ❌ Do NOT reach for | ✅ Instead use |
|---|---|
| **Pattern A "Standard Escalating"** | **Lane 1 hub-button** mechanism. Player picks from a menu at the NPC's location; stat-gated; agency-high. (Doc 24 §2 + §6.1 + Doc 56 P5 + R1.) |
| **Pattern B / C / etc. through Pattern J** (the 10 patterns from `prompts/game_design_patterns.md`) | **Lane 1 / Lane 2 / Lane 3 / Lane 4 capstones.** Four mechanisms, mapped to fictional intent (Doc 56 P5). No 10-pattern menu. |
| **Pattern F "Story Event" / Pattern G "Gate-Setting Event"** (one-shot beats) | **Lane 4 capstones** with the fingerprint `is_repeatable = false + trigger_mode = "manual" + priority ≥ 9 + flag-setter on exit`. Three sub-types: A linear, B branching (Pattern F real choice fork, F1–F5), C chain-step. (Doc 57 §3 + §4.) |

**Why:** Pattern A–J is mechanism-shaped — "what does the engine do at this beat" — and ignores the fictional weight of *who picked it*. Lane 1/2/3/4 is intent-shaped: same physical act feels different depending on the lane delivering it (Doc 56 P5). Mixing the vocabularies produces canvases that "use the right macro" but read in the wrong emotional register.

### §3.3 — NPC architecture

| ❌ Do NOT use | ✅ Instead use |
|---|---|
| **The 7-driver NPC system** (ROMANCE / RIVAL / MENTOR / SAFE_HARBOR / THREAT / WILDCARD / AUTHORITY / CLOCK) | **The 5 arc shapes:** family/ambient, slow-burn family, peer/dating, service, antagonist/witness. (Doc 56 §5 distribution table + Docs 31/53/58/59/60/61 per-NPC briefs.) |
| **The archetype system** (named archetypes assigned per NPC) | **Arc shape declared in the R7 design brief** (Doc 56 R7 + Doc 54 Appendix A). The brief commits to: arc shape + per-lane canvas budget + vocab ceiling + tier flags. No archetypes. |

**Why:** the driver-system describes *what role this NPC plays in the story*; the arc-shape system describes *what mechanical rhythm the NPC follows*. Drivers do not translate to per-lane budgets (Doc 56 §5), and they do not surface the empty-Lane-2/3 doctrine that service + peer arcs require (Doc 53 + Doc 56 R3). Authoring against drivers reproduces the Marge failure mode (Doc 54): correct vocabulary, wrong shape.

### §3.4 — Pacing / pre-author artifacts

| ❌ Do NOT emit | ✅ Instead use |
|---|---|
| **Whiteboard goals** (Phase 2B Systems Budget concept) | **Per-arc-shape canvas distribution** (Doc 56 §5 table) + **per-lane budget declared in the R7 brief** (Doc 56 R7). The budget IS the pacing artifact. |
| **Narrative gates** (Phase 2B Systems Budget concept) | **Capstone trigger fingerprint** (Doc 57 R1) + **quest card `when`/`goals` blocks** (Doc 50 R1–R6). Gates are surfaced via capstones + quest cards, not via a separate gate registry. |
| **Income channels** as a v4 modeling entity | **`money` Tier 1 trait** + **rent-driven recurring drain** (Doc 30 §4.1 economic engine + Doc 68 §3 `money` entry). One money trait, multiple in-game sources (jobs, allowance, capstone rewards); not a separate "channel" abstraction. |

**Why:** these are scheduling-system abstractions invented to model game pacing before the 3-lane doctrine existed. Once Lane 1/2/3/4 + per-arc-shape budgets ship, the pacing emerges from the budget plus the capstone chain — no separate registry is needed, and adding one produces double-bookkeeping that drifts as the game changes.

### §3.5 — Game shape

| ❌ Do NOT model | ✅ Instead use |
|---|---|
| **"Single-NPC Romance" architecture** (Jack's World shape) | **RTS-shape sandbox.** 4–6 NPCs in parallel, each with one arc shape from the 5-shape taxonomy. (Doc 66 §0 target picture + Doc 56 P4.) |
| **"Multi-NPC Parallel Arcs" architecture** (New In Town shape) | Same — RTS-shape sandbox. The "multi-NPC parallel arcs" framing is closer than Single-NPC-Romance, but it omits the per-arc-shape mechanical rhythms + per-lane canvas budgets that make RTS work. RTS-shape IS multi-NPC parallel, but with specific mechanical structure. |
| **Selectable game shapes** (the v6 "pick Single-NPC vs Multi-NPC" frame) | **No selection.** Every game is RTS-shape. (LO decision §6.1.) |

**Why:** LO locked this at the Doc 66 pivot. The redesign work (Doc 24–65) produced a complete design language for one game shape; teaching the LLM to select between shapes means it has to apply doctrine for shapes that have no design language yet. One shape, taught deeply, no menus.

### §3.6 — Voice / persona

| ❌ Do NOT consult | ✅ Instead use |
|---|---|
| **CLAUDE.md ENI persona** (sensory richness, layered prose, body language during dialogue, interior monologue, sentence variety, "show don't tell") | **RTS-flat default** for Lane 1 / Lane 2 / Lane 3 prose (Doc 30 §7.1 8 rules + `feedback_tls_scene_body_style` memory). **Tier-3 literary register EARNED at Lane 4 capstones only** (Doc 57 §6). |
| Multi-paragraph atmospheric openings | **Image-first composition.** Prose is ≤ 30-word caption. Stage direction cap: 2 sentences per beat. (Doc 30 §7.1 #8 + #2.) |
| Sensory grounding rituals ("3-4 layered sensory details minimum; include smell," etc.) | **Zero environmental sensory detail** in Lane 1/2/3 bodies. Dialogue does the character work. Crude direct diction per arc vocab ceiling (Doc 30 §7.5). |
| "It's not X, but Y" anti-pattern + hypophora + literary cadence rituals | Speaker-tag template; `<<Speech>>` macros heavily; one beat = one click. |

**Why:** the ENI persona is the default register for chat/roleplay. It is the wrong register for canvas authoring (Doc 30 §3 AUTHORITY DECLARATION). The Marge session (Doc 54) cost ~8 hours to a single failure: persona's literary instinct overriding RTS-flat doctrine. The override mechanism is explicit — *"ENI persona OFF. TLS game register ON."* — declared at the start of any authoring task (Doc 54 §2.5).

**Per LO decision §6.4:** CLAUDE.md is ignored for `prompts_v2/`. No carve-outs needed. The prompts override CLAUDE.md when active.

---

## §4 — Tone test (apply before shipping any file in `prompts_v2/`)

For each file authored against this corpus, mentally grep for legacy terms before shipping. The expected result is:

- **Zero hits** for `jack's world`, `new in town`, `two weeks` (case-insensitive).
- **Zero hits** for `pattern a`, `pattern b`, … `pattern j` (case-insensitive; expected hits ONLY in this file, naming them to ignore).
- **Zero hits** for `npc-driver` / `7-driver` / `archetype-system` / `whiteboard goal` / `narrative gate` / `income channel` (any spacing).
- **Zero hits** for `single-npc romance` / `multi-npc parallel arc` framed as architecture choice.
- **Zero hits** for `sensory grounding` / `sensory density` / `body language during dialogue` / `interior monologue` / `ENI persona` / `claude.md`, except in explicit contrast-against-RTS-flat passages.

If any file in `prompts_v2/` (other than this one) contains these terms, that file has leaked legacy vocabulary. Rewrite the offending passage. Don't paper over with a comment.

---

## §5 — When in doubt

If the design book or downstream specification calls for a concept this list does not cover, the question to ask is not *"which legacy pattern fits?"* but *"what is the fictional intent, and which Lane / arc shape / capstone type carries that intent?"*

The corpus has answers for:

- "How does this NPC's content escalate over time?" → arc shape + per-lane canvas budget (Doc 56 §5; `doctrine/03_arc_shapes.md`)
- "How does this beat fire?" → Lane 1 / 2 / 3 / 4 (Doc 24 + Doc 57; `doctrine/02_three_lanes_plus_capstone.md`)
- "How does this NPC become available in the player's day?" → schedule + `requires_npc` + getNpcLocation (Doc 24 §6 + Doc 67 §3; `schema/01_engine_capabilities.md`)
- "How does this scripted scene get reached?" → capstone trigger fingerprint + quest card pointer (Doc 57 R1–R5 + Doc 50 R1–R6; `doctrine/04_authoring_rules.md`)
- "What does the player see in the HUD?" → sidebar items + body-state vs progression-state doctrine (Doc 49 + Doc 68 §8; `schema/01_engine_capabilities.md` + `doctrine/09_trait_catalog.md`)
- "How explicit is this NPC allowed to get?" → per-arc vocabulary ceiling (Doc 30 §7.5; `doctrine/08_kink_vocab_ceilings.md`)
- "What stats does the game use?" → Tier 1 (corruption / arousal / energy / hygiene / money + per-NPC arousal / corruption / relation / stage) + Tier 2 (fitness / beauty / exhibitionism / intelligence) (Doc 68; `doctrine/09_trait_catalog.md`)

If none of the above answers apply, the question may be outside the RTS-shape sandbox scope. Surface it to LO rather than reaching for a legacy pattern.

---

**End of file.** Every other file in `prompts_v2/` is authored under the constraints declared above.
