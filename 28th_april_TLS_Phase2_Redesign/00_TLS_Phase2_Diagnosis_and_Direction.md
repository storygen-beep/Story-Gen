# The Long Summer — Phase 2 Redesign: Diagnosis & Direction

> **Created 2026-04-28.**
> Sibling to `../19th_april_UOR_Redesign_Session/` (the original UOR→TLS redesign).
> This folder is for the *content/structure* redesign that comes after the engine + design book are locked.

---

## Why this doc exists

The Long Summer's design book (`final_book.md`, 35,515 words), engine (F1–F4 shipped), TOML game data (79 canvases / 38 locations / 12 NPCs), and even a full content-rewrite project (`games/the_long_summer/content_rewrite/`) are all in good shape on paper. But playing the game — or even just reading the canvases — reveals that the **Phase 1 canvases are over-engineered, voice-collapsed, and partially hallucinated**, in ways that make the game feel like a kinetic novel pretending to be a sandbox.

This doc is the diagnosis: what we got wrong, what the four explored games (Road-to-Success, New Life Project, Shady Deals, Emilie) actually do, and where Phase 2 should go.

---

## TL;DR (one table)

| What explored games do | What TLS does |
|---|---|
| Tiny location menus (5 words + 4 buttons) | Novel-length scenes (1,300+ words across 3 sub-nodes) |
| Many short events (1–3 paragraphs) | Few long set-pieces |
| Real choices every 30 seconds | One "Continue" per scene |
| Repeatable activities = the game (80% of playtime) | Repeatables = side-dressing |
| Stats unlock *new content* | Stats decorate *prose variants* |
| Schedule + clock create rhythm | Flag chains create plot |
| Voice via short dialogue | Voice via long narration |
| State (numbers) gives feedback | Prose tries to land every change |

**The big miss:** TLS was designed *as a novel that pretends to be a game*. The explored games are designed *as games that occasionally hand you a paragraph*. Phase 2 needs to flip that ratio.

---

## Part 1 — What TLS currently has

### The shape on disk

```
games/the_long_summer/
├── book_phases/             ← 8 phase docs → final_book.md (3,900 lines, ~35,500 words)
├── toml_phases/             ← 6 files concat'd into 6_final_game.toml (7,868 lines)
├── content_rewrite/         ← Already-running rewrite project (Sessions 1-22+)
└── output/index.html        ← Compiled game
```

### The canvas inventory

- **Prologue:** 1 canvas × **9 sequential nodes** = ~8,500 words of novel-register prose.
  - Branching: only at `prep` (3 calculation_tier choices) and `diana` (told_sarah yes/no).
  - Every other node ends in single "Continue".
  - This is correct **for the Prologue** — it's a kinetic backstory cinematic before the player has agency.
- **Phase 1:** 28 canvases (B1–B28). Mix of Tier B (chapter milestones, 800–1,500 words), Tier C (arc-progression beats, 400–700 words), Tier D (diner shifts), Tier E (NPC repeatables), Tier F (solo/town dailies), and Tier A (Cracks, 1,500–2,500 words multi-node).
- **Activities:** 50 repeatables (`3_activities.toml`) + 4 diner tiers.
- **Story arc:** `4_story_arc.toml` for journal/milestone tracking.

### The content_rewrite project already exists

`games/the_long_summer/content_rewrite/PRD.md` *already names the problem*:

> "Everything after the Prologue collapses into sparse template prose. `@npc_xxx` tokens leak into the player-facing text. Activities are stat-vending-machines with no meaningful choices. Voice specs exist on paper but never on the page."

The rewrite has been running for 22+ sessions. It has style sheets, choice patterns, a corruption-band register, a worked example (Ryan beach), and a 27-rule standards doc. **And yet the rewritten canvases reproduce the original problem in a new form** — they're now Prologue-pastiche linear chains instead of skeletal templates. The fix overshot. This Phase 2 redesign is the correction.

---

## Part 2 — The diagnosis (four problems)

### Problem 1: The Phase 1 canvases imitate the Prologue's register, but the Prologue is a different *kind of object*

The Prologue is a **kinetic backstory cinematic**:
- 8,500 words, almost all single-"Continue" exits.
- No sandbox. No agency. Player is being delivered into the game.
- Long-form novel prose is *correct here* because there's nothing to do but read.

Phase 1 is supposed to be the opposite — a **sandbox**:
- Hubs (`loc_kitchen`, `loc_yard`, `loc_diner_front`, `loc_main_street`).
- Schedule-gated triggers (Sunday 06:30–08:30, Tuesday 17:00–17:30).
- NPC arcs running in parallel (Frank, Ryan, Jake — three Crack beats per chapter).
- Corruption accumulating from repeated choices.
- Economic pressure (rent + college savings) motivating escalation.

But here's what the Phase 1 canvases actually look like after rewriting:

- **B1 `arrival_at_franks`:** 3-sub-node 1,300-word "establishment sequence" with three "Continue" buttons in a row (driveway → porch → hallway).
- **B5 `town_walk_day_two`:** 3 sub-nodes (`kitchen → walk → diner`), each 400+ words, all linear.
- **B6 `marge_interview`:** single-node 700-word linear scene with no real branching.

These read like Prologue chapters, not sandbox triggers.

The standards file even *names* this contradiction. Rule 1 says: *"Failbetter density: passage intros ~30 words; result/outcome passages ~100 words."* The actual rewrites land at **400–700 words per node**. The mistake is using the Tier-A Crack worked example (Ryan beach, ~2,000 words multi-node) as a target for *every tier*.

### Problem 2: The "Rule 17 exception" stacking is the smoking gun

Every Phase-1 canvas description includes a defensive paragraph like:

- *"Rule 17 exception for N1→N2→N3 single-choice forward chain — this is an establishment scene"*
- *"Rule 17 single-exit exception (per book B4 'Choices: none')"*
- *"Rule 17 single-exit exception (per book B6 'Choices: none')"*

**If you're declaring an "exception" on most of your sandbox canvases, the rule isn't an exception — it's the de-facto pattern.**

The de-facto pattern is: split a paragraph-worth of prose into three nodes, put "Continue" between them, call it Option-B node-chaining. That's **faux-interactivity**. It's the same engine cost as a long single passage with three "Continue" clicks the player has no reason to make. RtS / NLP / Shady Deals don't do this; their multi-step events use real branching choices at every break or they don't break at all.

### Problem 3: The voice has collapsed into a single trick repeated forever

The Prologue's actual voice has *variety*:

- Short urban observations: *"Nothing was wrong. The morning was just the morning."*
- Interleaved with long subordinated sentences.

The Phase 1 rewrites kept only the long-subordinated trick:

> *"the count percolators ticked at when the heat had gone off them and the coffee had settled"*
>
> *"at the volume a man said a name at when the name was the full sentence he had to say"*
>
> *"the wiping-of-the-spot-that-did-not-need-wiping was the thing Diana did when the thing Diana was waiting on was a person and not a pan"*

That's a Cormac-McCarthy/Marilynne-Robinson *"the [thing] when the [thing] was the [thing] that..."* construction. **It's used 8+ times in `arrival_at_franks` alone, and every Phase-1 canvas leans on it.**

It hits hard once a chapter; deployed every paragraph it becomes pastiche, and worse, it's a tic the player will start to *parse around* — they'll skim because every sentence does the same trick.

This isn't hallucination of facts — it's **hallucination of register**. The model writing these decided the Prologue's voice was the target and applied it monotonically.

### Problem 4: Confabulation drift (the actual hallucinated facts)

Some specific factual details were invented during canvas rewrites that aren't anchored in the design book or in flags:

- *"three hundred and twenty miles"* — Maya's drive distance. Not in `final_book.md` or `Game_Redesign.md` as canon. It's now restated across canvases as if frozen.
- *"the chipped Hayes Hardware mug Frank's lumberyard had given out at an anniversary three counties over that Maya would not learn the story of for another month"* — a Chekhov's-mug deferral that the engine has no flag to redeem. It implies a payoff canvas that doesn't exist.
- *"the seventh shift, by which Maya was going to learn"* — same deferral pattern; the diner-tier system is real but no canvas references "the seventh shift."
- *"the Hansens' and the Deavers'"* — neighbor families introduced and not referenced again.

These are **prose-weather hallucinations**: invented background detail that *feels* canonical because it's reiterated, but isn't in the design book and won't pay off in the engine. They aren't bugs — they're **fiction debt**. The next rewrite session that doesn't re-read the same canvas will either contradict them or compound them.

### Problem 5 (bonus): Metadata bloat in canvas `description =` fields

Every canvas description is now a 150–250-word lawyer's brief justifying flag preservation, Rule 17 exceptions, and session attribution. Example from B6:

> *"Rewritten 2026-04-24 (Session 13) as single-node Option A prose expansion per content_rewrite/PRD.md Tier C spec. Closed-band Maya. First Cookie voice of the rewrite pipeline (pre-vouch register per Cookie style sheet — friendly-but-watching, tests her on the line). Marge style-sheet signature lines landed exact: 'Tie it. Learn as you go.' + 'Cookie's back here. Do what she says.' ..."*

This is **process metadata in a runtime file**. `package_from_toml` doesn't use it; players don't see it. It belongs in `session_log.md`. Currently every TOML rebuild compounds this.

---

## Part 3 — What the explored games actually do (the comparison)

### The four reference games

| Game | Passages | Flags | Tracked stats | Source |
|---|---|---|---|---|
| **Road-to-Success** | 358 | 1,521 | money, fitness, beauty, corruption, intelligence, energy + scene-specific gates | `game_explorations/road-to-success/` |
| **New Life Project** | 1,636 | 142 | corrupt 0..178, allure 20..30, inhib 0..100, trauma 0..70, mood (6 dims) | `game_explorations/new-life-project/` |
| **Shady Deals** | (50KB+ state file) | many | charm, combat, energy, heat, traits-by-progress (burglar/camwhore/hustler), faction reps | `game_explorations/shady-deals/` |
| **Emilie** | — | — | — | `game_explorations/emilie-finds-a-way/` |

### The seven things they all do that TLS doesn't

#### 1. The hub-and-event split

A **location** is a tiny menu. Sample bodies from RtS:

```
YOUR BEDROOM
Study 📖
Nap 💤
Wardrobe 👚
Hallway 🚪
```

```
MARCUS'S BEDROOM
Talk with Marcus 💬
Study with Marcus 📖
Hallway 🚪
```

An **event** is what happens *inside* an activity. Short. 1–3 paragraphs. Then back to the menu.

```
PRACTICAL LESSON 🚗
You take a practical driving lesson with your instructor.
Lessons completed: 1 / 5
You need 4 more lessons to take the practical exam.
Return ↩️
```

```
PLAYING WITH NATASHA
While you are reading a book, your friend Natasha appears to talk to you.
Natasha: Hi Victoria, what are you doing?

[Looking for some books]
[Library 📚]
```

The player *lives in a menu* and steps into short scenes. TLS makes them step into a novel.

#### 2. Choices everywhere, not just at the end

Every passage ends with 2–4 real choices. Each one does something different to your stats.

- "Study" → energy −10, intelligence +1
- "Jog" → energy −15, fitness +1
- "Go to mall" → time advance, money spend opportunities
- "Sleep" → reset to next morning

TLS Phase 1: most canvases have **one** "Continue" button, or two-three buttons that all set the same flags.

#### 3. Repeatable activities are the engine

The most-visited passages in RtS:

| Passage | Visits |
|---|---|
| `Center` | 21 |
| `Library` | 14 |
| `RestaurantWork` | 11 |
| `Residential` | 8 |
| `ParkJog` | 8 |
| `RestaurantVIPScene` | 7 |
| `LibraryExhibitionism` | 7 |

You do "Park Jog" or "Library Study" **dozens of times**. Each repeat slowly moves a stat. Rare-event injection: 1 in 10 times something different happens.

In RtS, **the loop is the game**. Repeatable activities are 80% of playtime. In TLS, the story canvases are 80% and the activities are stat-vending-machines no one will revisit.

#### 4. State (numbers) gives feedback, not prose

You see your `corruption: 45` go up by 1. You see `fitness: 9`. You see the sidebar change. **The number IS the feedback.**

The prose stays terse. The system tracks the change.

TLS tries to land the corruption arc *in the prose of every scene*. Every paragraph wants to show Maya noticing she's different. Heavy literary lifting on every page.

Players don't read carefully on read 50. They watch numbers and unlocked options. The explored games trust the system; TLS distrusts it and over-writes.

#### 5. Time-of-day + schedule does the work

From RtS variable schema:

```
location.school.MathClass.time = "EM"  (early morning)
location.school.HistoryClass.time = "M"  (morning)
location.school.PEClass.time = "A"  (afternoon)
location.school.EmptyClass.time = "E"  (evening)
```

Locations close ("Opens at: Evening"). Choices appear/disappear based on the clock. This makes the **same hub feel different** at 8am vs 10pm without writing 4 versions of the prose.

TLS has the schedule schema (`[[canvases.trigger.schedules]]`) but uses it sparingly. Most B-canvases gate on a flag chain — which means they're really just a linear story spine, not a sandbox.

Schedules give the player a **daily rhythm**. Flag chains give them a **plot**. Sandbox games need rhythm; TLS is currently a plot.

#### 6. Short events let writers nail voice; long scenes let them lose it

A 100-word scene only needs Marge to be Marge for 100 words. Easy to keep voice tight. The character's personality lands in **dialogue rhythm**, not narration.

TLS's 700-word linear scenes need the narrator to carry voice for 700 words — and that's where the "the count percolators ticked at when…" tic took over. The same Cormac McCarthy trick gets repeated 8 times in one canvas because the writer ran out of new ways to hold the register.

**Length isn't quality. Short = controllable voice. Long = drift.**

#### 7. Stats unlock new content, not just register variants

From RtS variable schema:

```
player.scenes.HouseCleaning1.requirementsMC.corruption = 30
player.scenes.XCam.requirementsMC.corruption = 45
player.scenes.xCamPizzaDelivery.requirementsMC.corruption = 45
player.scenes.SchoolBathroomMasturbate.requirementsMC.corruption = 0
```

Hit the number → a brand-new scene unlocks at the existing hub. Hit it later → another one.

TLS has the variant-block pattern (DEFAULT / WITHDRAWN / WARM / CONSEQUENCE), but it's mostly used to **change adjectives in already-written prose**, not to expose new scenes/choices. Corruption ≥ 25 should unlock new options at the diner, the yard, the bathroom mirror — not just shift Maya's voice in a scene she was already going to play.

The explored games show **new content**; TLS shows **new adjectives**.

---

## Part 4 — Where Phase 2 should go (direction, not yet a plan)

### What's NOT broken

- **Engine.** F1–F4 are shipped. Trait words sidebar, entry-conditions, trait_decay, eviction_mode all work.
- **Design book.** All 12 sections of `Game_Redesign.md` are FINALIZED. Cast, NPC arcs, Crack beats, calendar, corruption-band, sub-reputation, 4-tier diner — keep all of it.
- **The Prologue.** It's correctly long-form, correctly placed, voice is genuinely tight. **Freeze it. Don't touch it.**
- **The Tier-A Cracks.** Beach proposal, Frank trigger, Jake hand — these *should* be 1,500–2,500 words multi-node. The worked example (`worked_example_ryan_beach.md`) is correct for Tier A.
- **The activity inventory.** 50 activities is right. They just need to actually carry the loop.

### What needs to flip

#### Flip 1: Tier B/C/D/E/F all collapse toward hub-and-event density

| Tier | Current avg per canvas | Target |
|---|---|---|
| A (Cracks) | 1,500–2,500 (correct) | **Keep** |
| B (chapter milestones) | 800–1,500 across multiple sub-nodes | **150–250 single node, 2–3 real choices** |
| C (arc beats) | 400–700 | **80–150 single node, 2–3 real choices** |
| D (diner shifts) | varies | **60–120 + variant blocks for tier escalation** |
| E (NPC repeatables) | 300–500 | **40–100 + variant blocks for relationship escalation** |
| F (solo dailies) | 150–300 | **20–60 + 3–5 rotating openings** |

The standards file *already has these caps in Rule 1*. The actual rewrites violated their own standard. Phase 2 enforces the standard.

#### Flip 2: Drop Option-B sub-nodes for Tier B/C entirely

If a canvas is one location, one decision, one consequence, **it's one node**. The Prologue earned its 9-node chain because it spans 3 days and 4 settings. B1 (arrive at house) doesn't span anything — it's one moment.

Sub-nodes are reserved for:
- Tier-A Cracks (where genuine multi-beat escalation justifies them).
- Player-branching points (where node 2 is actually different from node 3 because of a choice in node 1).

Sub-nodes are **forbidden** for:
- "Establishment sequences" (split for atmosphere only).
- Single-decision canvases.
- "Continue / Continue / Continue" linear flows.

#### Flip 3: Story canvases shrink, activities grow

Currently: 28 story canvases carry 80% of the wordcount. 50 activities are skeletal.

Phase 2 target: 28 story canvases become quick milestone gates that fire-and-forget. 50 activities each have:
- 3–5 rotating openings (Rule 19).
- 5–10% rare-event injection (Rule 20).
- Real choice consequences (Rule 11) — no two choices set the same flags.
- Stat-gated escalation tiers exposed as new menu options at the same hub.

The diner becomes a real location, not a 4-tier story spine. The yard is a hub where Ryan's arc can be lived in 30-second beats over 20 visits.

#### Flip 4: Stats unlock content, not adjectives

Audit every Phase-1 milestone flag and ask: does hitting this flag (or this trait threshold) **expose a new menu option somewhere the player will see**? If not, it's a decoration. The 10 player traits and sub-reputations should each gate at least 3–5 new activity branches that didn't exist before they crossed the threshold.

#### Flip 5: Schedule everything that has a clock

If a canvas or activity says "Sunday morning" / "Thursday night" / "after church" anywhere in the prose, it MUST have a `[[canvases.trigger.schedules]]` block enforcing that. Rule 27 (Trigger-prose binding) is in the standards file but only audited late. Phase 2 makes this part of the canvas-creation step, not a post-hoc check.

#### Flip 6: Move metadata out of `description =`

Canvas `description =` should describe **what the canvas is, in one sentence**. Audit trail (rewrite session, rule justifications, flag preservation notes) goes in `session_log.md` only.

#### Flip 7: Confabulation registry

Build a small file that lists every **invented background fact** in the prose (mile distances, mug origin stories, neighbor names, "by the seventh shift" deferrals) and binds each one to either:
- A canon entry in the design book, or
- A flag the engine actually tracks, or
- A "decorative — never reference again" tag.

Anything with a deferred-payoff implication that has no flag must either get a flag-and-payoff canvas OR be rewritten to remove the implication.

---

## Part 5 — What this folder will contain (proposed)

This is the kickoff doc. The proposed siblings (not yet written):

- `01_Phase2_PRD.md` — concrete plan: tier caps, batch order, validation steps. Successor to `content_rewrite/PRD.md`.
- `02_Hub_Event_Architecture.md` — the new shape for hubs (tiny menus) and events (short scenes). Worked examples for `loc_kitchen`, `loc_yard`, `loc_diner_front`.
- `03_Activity_Loop_Spec.md` — what makes the 50 activities carry the game. Rotating openings, rare events, stat-gated escalation.
- `04_Confabulation_Registry.md` — every invented detail in current prose, with a disposition (canonize / flag / remove).
- `05_Tier_Compression_Examples.md` — before/after for B1, B5, B6 showing the collapse from linear-prose to hub-and-event.
- `06_Schedule_Rhythm_Spec.md` — how time-of-day and weekday turn the same hubs into different rooms across the week.

---

## Part 6 — One-line summary

The Long Summer's Prologue is a beautiful novel. Phase 1 should not be a beautiful novel — it should be the sandbox that the design book, the engine, and the explored games all already know how to be. Phase 2 is the work of remembering that.
