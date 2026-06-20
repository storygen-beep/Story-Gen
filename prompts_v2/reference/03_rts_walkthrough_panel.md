# Reference 03 — RTS Walkthrough Panel (Transparent Gating Doctrine)

**Sources:** Doc 56 P2 (transparent gating principle); Doc 24 §5 (walkthrough discovery doctrine); Doc 13 §6 (Walkthrough panel as transparent planning UI); live extraction of `WalkthroughV2` passage from RTS source (4738 chars).
**Authority:** Reference. P2 evidence base.
**Purpose:** Document the RTS Walkthrough panel as the canonical "published catalog" UI surface — what it renders, what columns it exposes, what doctrine it operationalizes.

This file is the source-of-truth for `doctrine/01_rts_principles.md` P2 and `doctrine/04_authoring_rules.md` D56-R5 (every canvas declares a `guide` string).

---

## §1 — The walkthrough IS the game's quest log

Doc 13 §6 — the `📕 Walkthrough` button in the right sidebar opens a passage that **literally renders the scene table as data to the player**. Same fields as the engine's internal scene struct, just formatted as a table.

**The player loop is literally:**

> open Walkthrough → pick a locked scene close to unlocking → read its requirements → close the gap → re-attempt.

**There is no hidden progression. The "story" is the player's self-authored checklist progression across the 130+ scene catalog.**

This is the P2 transparent-gating doctrine in pure form. Transparency is the design, not a fallback.

---

## §2 — What the Walkthrough panel renders

Three sections, in order:

### §2.1 — Top section: tutorial (verbatim)

```
How to gain corruption and exhibitionism

At the start of the game, you gain 1 arousal each day, or after being
groped in your bedroom. You can choose to masturbate to increase your
corruption.

Once you reach 5 corruption points, you unlock the option to flash
your Stepbrother through his bedroom, gaining 1 exhibitionism point.

Some events have requirements, such as a minimum corruption level,
exhibitionism level, or relationship level with an NPC. You can also
trigger events by visiting certain locations.
```

**The bootstrap loop is taught explicitly.** No discovery required.

**Implication for TLS-shape sandboxes:** when the walkthrough surface ships (Doc 62 PRD pending), include a tutorial block at the top. Teach the bootstrap loop in player-facing language. Don't make the player guess how corruption climbs.

### §2.2 — Middle section: NPC scenes index

Card grid of every NPC with a `scenes` object:

```
MC + Stepfather (12) + Stepbrother (15) + Stepgrandfather (6) +
Marcus (5) + Sam (2) + Emma (1) + Jamal (3) + Veronica (3) +
Priest (2) + Gangster (1) + Mr. Matthew (1) + Edward (4) +
Tow Truck Driver (1) + Yacht Captain (1) + Thief (2) + Josh (1) +
Landlord (1)
```

Each card shows the NPC name + scene count. Clicking a card opens the per-NPC drilldown table (§3).

### §2.3 — Bottom section: location scenes index

Same card grid for location-bound scenes — independent of NPCs (random encounters at the location regardless of who's there):

```
City Center (1) + House (1) + Bus (3) + Photo Studio (2) + School (12) +
Park (9) + Gym (3) + Mall (3) + Night Club (2) + Beach (7) + Bar (4) +
Public Pool (2) + Office (2) + Driving School (1) + Thomas's House (2) +
Strip Club (3) + Clandestine Clinic (2) + Restaurant (5) + Police Station (1) +
Hospital (2) + Abandoned Building (1) + Gas Station (1) + Movie Theater (2)
```

Clicking opens per-location scene table with the same columns as per-NPC table.

---

## §3 — The columns (per-NPC drilldown table)

Clicking "Stepbrother" → table with these columns:

| Column | What it shows | Source |
|---|---|---|
| **SCENE** | Display title of the scene (sugarcube-interpolated, e.g., "Stepbrother Bedroom Grope") | `scene.title` |
| **NPC** | NPC slug | `scene.npc` |
| **REQUIREMENTS (NPC)** | NPC stat thresholds: Arousal 🔥, Corruption: 5, Relation: 10 | `scene.requirements.{arousal, corruption, relation}` |
| **REQUIREMENTS (MC)** | Maya stat thresholds: Corruption: 30, Exhibitionism: 10 | `scene.requirementsMC.{corruption, exhibitionism}` |
| **CHANCE** | Dice probability when reqs met (20%, 25%, 33%, 100%) | `scene.chance` |
| **GUIDE** | Natural-language trigger recipe | `scene.guide` |
| **STATUS** | 🔒 Locked / ✅ Completed | `scene.unlocked` (lifetime flag) |

### Example row (verbatim from in-game panel)

| SCENE | NPC | REQUIREMENTS (NPC) | REQUIREMENTS (MC) | CHANCE | GUIDE | STATUS |
|---|---|---|---|---|---|---|
| Sleep with Stepbrother | Stepbrother | Arousal: 🔥, Corruption: 10 | Corruption: 30 | 100% | Go to Stepbrother bedroom late at night and ask to sleep with him | 🔒 Locked |

**Every column is data-driven.** No author-time per-scene customization beyond filling the `scene` object fields. The walkthrough is generated from the data, not authored as a separate UI surface.

### Implication for TLS-shape sandbox engine

The walkthrough rendering depends on the canvas having structured metadata:
- **Display title:** `canvas.name` (already in TLS schema)
- **NPC reqs:** `canvas.trigger.conditions.items[]` where `subject = "npc"`
- **MC reqs:** `canvas.trigger.conditions.items[]` where `subject = "player"`
- **Chance:** `canvas.trigger.chance` (Lane 2 random) OR derived from `substitutions[].chance` (Lane 3) OR 100% (Lane 1 / Lane 4)
- **GUIDE:** the `canvas.guide` field — currently pending Doc 62 PRD per `00_LEGACY_IGNORE.md`
- **STATUS:** derived from `setup.trigger_history[canvas.id].total > 0` (already in TLS engine)

When Doc 62 ships (`guide` field as a parsed canvas attribute), the walkthrough surface becomes authoring-trivial — render the existing canvas metadata in a table.

---

## §4 — The `guide` field convention per lane

From Doc 56 R5 (`doctrine/04_authoring_rules.md` D56-R5) + RTS walkthrough conventions verified across 130+ scenes.

The GUIDE string names the lane in the prose:

| Lane | Phrasing convention | RTS example | TLS example |
|---|---|---|---|
| **Lane 1 — Hub button** | "Visit X" / "Go to Y and Z" | "Go to your Stepbrother bedroom and have sex with him" | "Visit Frank in his kitchen during breakfast" |
| **Lane 2 — Location-entry random** | "Walk into X" / "Go to Y" (with conditions) | "Go to your bedroom" | "Walk into the kitchen late at night" |
| **Lane 3 — Dispatcher substitution** | The chore name, then "while X" | "Masturbate at shower at the house bathroom" / "Wash the dishes" | "Make tea in the kitchen while Frank is home" |
| **Lane 4 — Capstone** | The narrative milestone | "Go to Stepbrother bedroom late at night and ask to sleep with him" | "After the catch, return to Frank's bedroom in the evening" |

### Style rules for GUIDE strings

- **Player-facing.** Second person or Maya-third. Not author-side metadata.
- **Short.** One sentence. Not a marketing line; a recipe.
- **Concrete.** Names the location + chore + NPC condition. NOT "explore the kitchen" — "Wash dishes in the kitchen while Frank is home."
- **No mechanics jargon.** "while corruption ≥ 25" → "after the catch" (the player-facing flag name).

### Anti-patterns

- **Vague GUIDE:** "Spend time with him" — doesn't tell the player WHERE / WHEN / WHAT activity.
- **Author-side metadata:** "Lane 3 dispatcher inside activity_shower" — that's debug info, not a recipe.
- **Numbers / schedules:** "Go to the kitchen between 17:00-19:30 with corruption 25+" — schedules + numbers surface from canvas metadata; GUIDE stays in-fiction language.

---

## §5 — `<<NotifyCorruption N>>` — failure-as-information

P2 + P7 combined produce a specific UI pattern: the locked-click toast that publishes the threshold.

### §5.1 — Source pattern (5+ widget verifications)

Doc 13 §7.4. Reading widget definitions across many scenes (`JimDM`, `RichardDM`, `EdwardDM`, `EdwardSecondDateDM`, `EdwardThreesomeDM`, `RichardSecondPhotoShootDM`):

```twine
<<widget 'JimDM'>>
    ... pitch dialogue ...
    <<if getCorruptionLevel() >= 4>>
        <<linkreplace "Accept the proposal">> ... unlock film studio ... <</linkreplace>>
    <<else>>
        <<linkreplace "I can't do this">>
            <<Speech Player "I'm sorry but I can't do that">>
            <<Speech Jim "I understand, if you change your mind, you can contact me.">>
            <<NotifyCorruption 4>>      /* always in ELSE branch, N matches the if-threshold */
        <</linkreplace>>
    <</if>>
<</widget>>
```

**`<<NotifyCorruption N>>` is a UI hint widget that displays "you need corruption level N for this."**

Verified across 5+ widget definitions. Always called in the ELSE branch with N matching the required level. Used in DM widgets, in `BrotherBedroom` hub button handlers, etc.

### §5.2 — What it is NOT

**It is NOT a corruption-adder.** Doc 13 §11 Correction 3.

Live verified: clicked "Have sex with him 🔥" at MC corruption 0 → source has `<<NotifyCorruption 4>>` in that branch → no stat change after. The "rejection trains the player" loop does NOT exist.

**Failure is information, not progress.** The player still has to actually do the corruption-raising mechanic (masturbate / accept paid date / etc.). RTS doesn't shortcut progression via locked-click farming.

### §5.3 — TLS analog

TLS `locked_text_threshold` field on `TemplateChoice` (shipped 2026-05-06). Per-choice `show_when_locked = true` + `locked_text = "..."` + optional `locked_text_threshold = "..."` renders the choice greyed-out + click-to-toast pattern.

```toml
[[canvases.nodes.exit_block.choices]]
text = "Suck him"
show_when_locked = true
locked_text = "I need to know him better first"
locked_text_threshold = "Maya's corruption: 35+"
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 35 },
] }
nodeId = "loop_franks_bedroom_finisher"
```

When the player clicks at corruption < 35, the toast publishes "Maya's corruption: 35+". Zero stat effects. Zero flag effects. Pure threshold-publish.

See `schema/01_engine_capabilities.md` §10.4–§10.5 for the engine surface.

---

## §6 — Doc 62 PRD (current engine status)

**Status:** doctrine-locked + schema-pending. The TLS walkthrough surface is not yet shipped.

### §6.1 — What's shipped

The data primitives EXIST in the engine:
- Canvas `id` + `name` + `description` (via `TemplateCanvas`)
- Canvas trigger conditions (`TemplateTrigger.conditions`)
- Trigger schedules (`TemplateTrigger.schedules`)
- NPC schedules (`TemplateNPCSchedule`)
- Cooldown tracking (`setup.trigger_history`)
- `formatCanvasConditions` runtime (`v2.py:7043`) — renders condition blocks as human-readable strings

### §6.2 — What's NOT yet shipped (Doc 62)

- **`canvas.guide` field parser.** The doctrine-locked field is not yet a parsed dataclass attribute (Doc 56 R5 noted in §4 above). Author should still emit `guide = "..."` — the validator tolerates the field. When Doc 62 ships, every canvas's `guide` becomes the published-catalog recipe.
- **The walkthrough UI surface itself.** No `:: Walkthrough` passage in TLS. When the catalog UI ships, it renders the table from existing canvas metadata + the `guide` field.

### §6.3 — Held per Doc 66 §10

Doc 62 PRD is in the held list per Doc 66 (the prompts_v2/ rewrite pivot). LO will scope when:
- Next NPC authoring session demands `guide` backfill
- OR catalog UI prioritized over other Phase 2+ work

**For prompts_v2/ generated games:** every canvas authored ships with `guide = "..."` from day 1, so when Doc 62 ships the data is already populated and the catalog surface lands trivially.

---

## §7 — What TLS borrows vs differs from RTS Walkthrough

### §7.1 — TLS borrows (current TLS Quests engine)

- **Per-NPC scene table organization** — TLS V2 Quests engine groups quest cards per NPC (Frank section, Marge section, etc.). Mirrors RTS Walkthrough's "Stepbrother (15)" / "Marcus (5)" cards.
- **Status indicators** — TLS quest cards have visual frames (✓ Arc complete / 🔓 Ready / 🎯 To advance bullets). Maps to RTS's 🔒/✅.
- **Player-facing trigger recipes** — the GUIDE string convention (Doc 56 R5 / D56-R5 in `doctrine/04_authoring_rules.md`).
- **`locked_text_threshold` publishing** — direct port of `<<NotifyCorruption N>>` pattern.

### §7.2 — TLS differs (intentional)

- **TLS V2 Quests is ACTIVE quest cards only.** Doesn't render a per-NPC full catalog. RTS Walkthrough shows ALL scenes (locked + unlocked) for every NPC.
- **TLS has Maya-voice narrative copy.** Quest cards have `text` / `ready_text` / `tip` in Maya's interior voice. RTS Walkthrough is data-only — no narrative copy.
- **TLS hides stage trait.** Per Doc 68 §9 — stage NEVER surfaces. RTS's relation column shows raw values; TLS shows in-fiction equivalents only.

### §7.3 — What TLS SHOULD borrow when Doc 62 ships

Per Doc 13 §14 implications-for-TLS:

| Pattern | RTS source | TLS status | When Doc 62 ships |
|---|---|---|---|
| Published walkthrough with full scene table | §6 | Partially (V2 Quests is active cards only) | Extend QuestsPage with a per-NPC scene table view |
| Notification-as-threshold-hint | §7.2 / §7.4 | Variable — some TLS gates do this | Standardize: every gated button should publish its threshold via `locked_text_threshold` |
| Per-scene `guide` field | §3 / §6 | Doctrine-locked, schema-pending | Doc 62 PRD ships the field; backfill on Frank slice (28 canvases) |
| Cross-NPC scene branching (`SellingMyStepsister`) | Doc 13 §7.2 | Not used | Consider for arc convergence moments (e.g., Frank → Diana brought-in capstone) |

---

## §8 — TLS slice walkthrough deferrals

Per Doc 13 §14 cautions:

### Caution 1 — Walkthrough requirements aren't strict gates

Per Doc 13 §11 Correction 1: the walkthrough's "REQUIREMENTS (MC)" column is a **suggested threshold for the FULL content version**, not an entry gate. Player can stumble into scenes early and get a teaser; full content unlocks later.

**Implication for TLS:** the published catalog needs to communicate "this scene has a teaser at low stats + full content at high stats." TLS could be MORE transparent than RTS by surfacing content-tier thresholds explicitly (e.g., "Sleep with Stepbrother — basic version: relation 10+. Full version: relation 25+."). Or TLS could intentionally hide tier ladders to preserve the come-back-later loop. **LO call when Doc 62 ships.**

### Caution 2 — Deterministic scenes also have stat-tier branching

Per Doc 13 §16 Finding 2: walkthrough's `CHANCE: 100%` means the trigger always fires when reqs met, but the *content within* still gates by stats. A player can "unlock" a scene mechanically and still get a truncated/rejection version.

**Implication for TLS:** scene "completion" status is binary (✓ / 🔒) but content density isn't. The walkthrough surface should communicate this distinction — possibly via a "see full content?" indicator on completed scenes that still have tier-gated branches.

### Caution 3 — Scrollable / paginated UI

RTS Walkthrough has ~130 scenes total. Single-page rendering may not scale beyond ~50 scenes per NPC. TLS slice scope (8-12 NPCs × 5-30 canvases each) needs to think about UI organization upfront.

**Held for Doc 62 PRD scope.**

---

## §9 — Cross-references

### Sibling reference files

- `reference/01_rts_overview.md` §6.2 — Walkthrough panel surface (broad context)
- `reference/02_rts_scene_catalog.md` — the per-NPC scene tables that the Walkthrough renders
- `reference/04_rts_hud_world_model.md` — the sidebar (HUD) doctrine; sibling surface to the Walkthrough

### Sibling doctrine files

- `doctrine/01_rts_principles.md` P2 — transparent gating, not hidden progression
- `doctrine/01_rts_principles.md` P7 — don't punish trying (`<<NotifyCorruption N>>` doctrine)
- `doctrine/04_authoring_rules.md` D56-R5 — every canvas declares a `guide` string

### Source

- `28th_april_TLS_Phase2_Redesign/13_Road_To_Success_Reference.md` §6 — Walkthrough panel doctrine source
- `28th_april_TLS_Phase2_Redesign/24_RTS_Three_Lanes_Repeatable_Activities.md` §5 — discoverability doctrine
- `28th_april_TLS_Phase2_Redesign/56_RTS_Principles_and_TLS_Alignment_Doctrine.md` P2 — transparent gating principle source
- `28th_april_TLS_Phase2_Redesign/62_Canvas_Guide_Field_PRD.md` — engine work to ship the `guide` field (held)

### Engine source

- `WalkthroughV2` passage (`game_explorations/rts-arc-trace/passage_catalog.json`) — 4738 chars of canonical rendering logic
- `WalkthroughTable` widget — the per-NPC table renderer
- `formatCanvasConditions` (`v2.py:7043`) — TLS analog renderer (currently feeds `show_when_blocked` text, will feed walkthrough surface when Doc 62 ships)

---

**End of file.** Next: `reference/04_rts_hud_world_model.md` for the sidebar (HUD) doctrine.
