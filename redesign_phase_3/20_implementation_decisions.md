# Implementation decisions — the locked wiring contract

The output of the conflict-audit review (2026-06-09 → 06-10): a full read of the existing skill
(`SKILL.md` + all 10 `references/`) against the redesign, the conflicts found, and **the decisions LO
locked for each**. This is the authoritative checklist for the wiring phase — when the spec-on-paper
becomes real edits to `author-game/SKILL.md` and its references.

**Standing rule (LO):** the **redesign is the source of truth; the skill is brought to match it
exactly.** Where the redesign was silent or under-specified, the resolution below *is* the redesign's
position now (write it into the redesign first, then the skill follows).

**Spec-on-paper still — no skill files edited yet.** These are decisions + their touch-lists.

---

## The locked decisions

### 1. Slice is removed (always full game)
`scope_mode` / `slice` is deleted, not rephrased. **Touch-list (7 skill files):**
- `SKILL.md` — drop the `scope_mode` operating rule entirely.
- `setup-interview.md` — delete **Step 1.5** (the whole "determine scope mode" step) + the slice arms
  in Step 2 item 5, Step 3, Step 5.
- `ledger-schema.md` — remove the `scope_mode` field. **KEEP the `npcs` budget block**
  (`arc_shape` / `lane_budget` / `vocab_ceiling`) — it's independent of slice and still load-bearing.
- `lanes.md` — drop the "~30–50% at slice" sizing paragraph; budgets are always full.
- `beat-authoring.md` — drop slice from arc-sizing **and** collapse the contraception rule to the
  `pregnancy` axis only (defer → bareback; include → contraception-language allowed pre-pregnancy,
  banned post-).
- `content-design.md` — drop "size to `scope_mode` (slice → thin spine)"; venue columns always filled.

### 2. The clothing rule is refined (reactive world carve-out)
The skill's absolute *"clothing gates PUBLIC content, NEVER an NPC arc"* becomes a **two-part** rule:
- clothing **MAY trigger ambient, in-character reactive events** (Lane 2/3 — the reactive world, `11`);
- clothing **must NOT gate an NPC's escalation spine / arc-progression** (the `worn_corruption`-gates-
  a-housemate's-arc case stays banned — it's still the backwards on-ramp).

**Touch-list:** `systems.md` (the clothing trap row) + `beat-authoring.md` self-audit line. This is the
carve-out `19` D4 needs but didn't spell out — without it the self-audit would reject every reactive
event.

### 3. Ask crucial / inform routine (not a question every beat)
`SKILL.md` + `beat-authoring.md` currently mandate AskUserQuestion **every** beat. Reconcile to `16`'s
split: **Mode A** (AskUserQuestion, options + recommendation) only at a **genuine fork**; **Mode B**
(one-line plain-language inform-and-proceed) for routine roster rows. *Ask the crucial, inform the rest.*
**Touch-list:** `SKILL.md` operating rules + `beat-authoring.md` loop §1.

### 4. The ledger is active from setup (phase-aware dispatch)
The ledger (`authoring_state.json`) is **created at setup**, not deferred to authoring — because it's
just bookkeeping JSON, it compiles nothing and can't fail a build. Early it carries only the **pipeline
phase / progress marker** (which step we're in, what's done); its creative parts (`structure_registry`,
`plan`, `produced_canvas_ids`) stay empty until Step 6 fills them.
- **Resolves B1** (how the skill knows its phase across the ledger-less Steps 2–5): it reads the
  ledger's explicit phase field — no inference from which design-book sections exist.
- **Downstream consequence:** the skill's mode dispatch flips from *"does `authoring_state.json` exist?"*
  (always true now) to **"what phase does the ledger say?"** — phase-aware across all 7 steps, not a
  binary setup/continue.

**Touch-list:** `01` (ledger born at setup), `ledger-schema.md` (add a `pipeline_phase` / progress
field), `SKILL.md` (phase-aware dispatch).

### 5. The build artifact stays at Step 6
Steps 1–5 produce **only the design book** (creative prose) — nothing to compile. The scaffold TOML +
**first green build** live at the **front of Step 6 (authoring)**; that's where the first buildable game
appears. Moving the *ledger* up (decision 4) does **not** drag the *build* up — they're independent.
- **Resolves B2.** **Touch-list:** `01`, `setup-interview.md` (the scaffold/green-build steps relocate
  to authoring).

### 6. The per-increment rhythm = ideate → decide → write
Every post-setup increment runs the same loop: **ideate → decide → write** (→ **verify green** at Step
6) → next. It's uniform across Steps 2–6 (only what "write" produces changes: design-book prose in 2–5,
TOML-that-compiles in 6). The **weight** of ideate-and-decide scales with how crucial the piece is
(decision 3) — shape-setting increments are decided with LO; routine rows are written and reported.
**Touch-list:** `16` (state the three-beat loop explicitly).

### 7. Casting = role + hook + rough sketch
Each NPC at casting gets **role + hook + a rough sketch** — a loose few lines of where the character
roughly goes. **Cross-NPC connections live as light threads inside the sketch** ("her friend could
become her own arc," "if she's pregnant it changes how Sal treats you") — *ideas, not a format*;
optional, not every NPC; islands are fine. This replaces the heavier "cross-NPC web + weave checkpoint"
idea (dropped as over-engineering).
- Gives the **whole cast a once-over at casting** (see the connections while they're all in front of
  you) and feeds Step 4 so no NPC is authored in a vacuum.
- Creates a clean **three-level zoom**: hook (one line) → rough sketch (casting) → full arc brief
  (Step 4); the sketch seeds the brief's §1 end-state.
- When a thread grows up: a friend-who-becomes-playable is a **new NPC** back through casting; a ripple
  is a **`cross_npc` beat** at authoring. No system, no diagram.

**Touch-list:** `06` (add the rough sketch to what casting assigns + the output artifact).

### 8. Fix the stale step numbering in `01`
`01`'s "what moved out of setup" table still uses the **old 5-step** scheme (NPC arcs = Step 3, roster =
Step 4, authoring = Step 5 — no separate Casting step). Renumber to the **current 6-step** scheme
(Casting = 3, NPC arcs = 4, Roster = 5, Authoring = 6). **Touch-list:** `01`.

---

## Open — verify, don't assume (not a decision, a check)

### E1. The new stat legs in `04` must be real engine traits
`04 §5` proposes **charisma / social** and **fitness / beauty** as derivable stat legs. The skill's iron
rule is *"only offer real engine knobs — never invent a field the engine lacks."* These must be
**verified against `doctrine/09` (the trait catalog) / the engine** before they're wired as concrete
stats. `04 §7`'s "derive, don't hardcode" keeps them optional; if a game wants them, confirm they exist
first. **Check at wiring; do not assume.**

---

## Phase A — engine-misstatement corrections APPLIED (2026-06-10)
Read-only verification (`doctrine/09_trait_catalog.md`, `schema/*`, the `twee_comprehensive` engine
`v2.py`, shipped games) resolved E1 and surfaced two reactive-world misstatements. All three corrected in
the redesign before any skill wiring (so the skill never inherits a fake knob):

1. **Stat legs (`04` §5 + §7) — DONE.** `beauty` is **derived from worn clothing** (`getWornBeauty`,
   `op=add/set` forbidden), NOT a raisable leg — moved to the clothing system. `charisma`/`social` (and a
   career/skill stat) are **NOT built-in** — only authorable as **Tier-3 custom traits**; relabelled as
   such. Added an engine-ground-truth box: real built-ins = corruption/arousal/energy/hygiene/money (T1) +
   exhibitionism/fitness/intelligence (T2) + beauty (derived). `fitness` IS a real raisable Tier-2 trait.
2. **Forced mode (`11` + `18`) — DONE.** No zero-choice engine primitive exists (every canvas renders a
   fallback Continue). *Forced* = an **auto-fire capstone-shape canvas** (`priority ≥ 9`,
   `is_repeatable = false`, single Continue, no refuse/accept branch). Achievable today, no engine work.
3. **Per-place ceiling (`11` + `18`) — DONE.** **Not an engine location attribute** — author-encoded in
   each reactive canvas's `conditions`. A design discipline, not an engine field.

Confirmed REAL (reactive world is buildable as designed): `worn_corruption`/`worn_beauty` predicates,
gating Lane 2/3 triggers on them, the `corruption_level` banded predicate, and the clothing doctrine rule
(`doctrine/11_clothing_design.md` §2 — clothing gates PUBLIC content via Lane 2/3, never an NPC arc spine)
which *confirms* decision 2's carve-out almost verbatim.

---

## What was already aligned (no action — for the record)
- The game **story / spine** = Step 2's desire ladder (`09`); the **whole-game quality bar** = Step 0's
  8 qualities, carried as a check through every step. Both already homed — not a gap.
- `19`'s D1–D6 and `07 §6`'s relocation note already anticipate most of the structural reconciliation
  (slice, roster re-home, briefs relocate, ask-vs-inform). Decisions 1–3 above sharpen them; they don't
  contradict them.

## Cross-references
- `README.md` (pipeline + status) · `01` (setup, ledger-at-setup, numbering) · `06` (casting + sketch) ·
  `11` (reactive world — the clothing carve-out's reason) · `16` (run mode + the rhythm) ·
  `19` (Step 6 deltas D1–D6) · `ledger-schema.md` (the phase field).
