# Run mode — how the pipeline RUNS (the interaction contract)

Every other reference says *what* to build; this one says *how the building is run* — the process contract
between the skill and the user. It exists because the prior failure (LC/LS) wasn't only a design failure;
it was a **process** failure: the game fell out of one blind one-shot dump, so it couldn't be *felt* into
shape and the user couldn't steer before the mistakes were load-bearing.

**The fix: after setup, the game is NEVER generated in one shot. It is built one verified piece at a time,
with the user in the loop, and nothing is invented silently.** This applies across **Steps 2–6** (Steps 0–1
are the one upfront conversation). Source: `redesign_phase_3/16`.

---

## The three laws
1. **Incremental after setup.** Everything after the seed is written in **increments**, one piece at a time,
   each surfaced and (where it matters) approved before the next. No "generate the whole game" call, ever.
2. **Visible, not silent.** The user always **knows what is being written** — in plain language, at the
   design level — *before* it becomes code. The user reviews **intent**, not every line.
3. **Grounded, not hallucinated.** No creative or technical decision is invented from nothing. Crucial forks
   are **asked**; engine/reference facts are **verified against the files**; every increment is **built
   green** before the next leans on it; assumptions are **stated out loud**.

**Increment ≠ slice.** Incremental is the build *order*, not the final *size*. Scope is always the **full
game** (slice removed). We build the whole game — just one verified piece at a time.

## Two interaction modes — keep them separate
Conflating them is the failure (a black box on one side, death-by-questions on the other).

### Mode A — DECISION GATE (`AskUserQuestion`)
Used **only at crucial forks** — where the answer **changes the game's identity** AND can't be derived from
what's already decided. Always: 2–4 concrete options + **a recommendation** (recommended option first,
labelled). The user can pick "Other."
- **Crucial (ask):** POV + the core fantasy · the charge/ceiling level (how explicit, non-con in/out) · who
  the core target(s) are + each one's hook · the economy shape · the frontier/ending shape · any genuine
  creative fork with no derivable answer.
- **Batch per checkpoint.** One question-set carries a phase's crucial forks together — not one question per
  micro-decision. A dozen decision gates across a whole game is the right order of magnitude, not a hundred.

### Mode B — INFORM-AND-PROCEED (a short plain-language note)
The *visibility* the user means by "I should know what's being written." Before/after each increment, a
**skimmable** plain-language statement of what the piece *is* — not a request for permission, just the
lights kept on. The user can interrupt any of them. **Most of the loop is Mode B.**
- **Not crucial (never ask — just do it):** flag/trait names, lane numbers, file layout, which engine
  primitive, scene ordering within an approved arc, prose wording, any mechanical translation of an
  already-approved design.

**The calibration rule:** *ask the crucial, inform the rest, invent nothing silently.*

## The per-increment rhythm — ideate → decide → write
Every increment after setup runs the same three-beat loop: **ideate → decide → write** (→ **verify green**
at Step 6) → next. Uniform across Steps 2–6 — only what "write" produces changes (design-book prose in
Steps 2–5; TOML-that-must-compile in Step 6). The *throttle* on it is the ask/inform split: at a
**shape-setting** increment, ideate-and-decide happens **with the user** (Mode A); at a **routine**
increment, ideate internally, decide, write, report in one line (Mode B). The honest model is *not*
"brainstorm-and-ask every piece" — it's **"every piece is ideated and never invented blind; the crucial
ones we decide together, the routine ones I write and report."**

## The review surface is the DESIGN BOOK, not the TOML
The crux of "I don't review each line of code, but I know what's written." The user reviews **intent in
plain language — `design_book.md`**. The TOML/engine layer is the *faithful translation* of a design that
was already surfaced and okayed, so the code can't surprise the user — the design it came from didn't.
- **Creative layer → the design book → the user's review surface.**
- **Engine layer → the authoring step → derived from the approved design, built green, not reviewed line-by-line.**
- If a technical reality forces a design change (an engine limit/gotcha), it **bounces back up to the design
  book** and is surfaced — never silently patched into the TOML.

## The increment ladder (what "one by one" means per phase)
| Phase | Increment unit | Mode at the gate |
|---|---|---|
| 0+1 — fantasy/seed | the whole fantasy + the seed | **A** (POV · fantasy · charge · desire-span) |
| 2 — top-level | the spine | **A** (cascade shape · economy shape · frontier shape) |
| 3 — casting | the cast as a set | **A** (core targets + hooks; confirm cuts) |
| 4 — deep-design | **ONE subject at a time:** player → NPCs (one each) → world → reactivity | **A** at each subject boundary + per *core* NPC; **B** for peripherals/routine |
| 5 — feedback | **ONE subject's question-cluster at a time** (the review) | **B**; **A** on any gap whose fix changes identity |
| 6 — authoring | **scene by scene** | **B**, **build green each increment** |

The two heaviest interaction points: **Step 2** (identity-setting, cheap on paper — ask freely) and **Step
4** (one subject at a time — the heart, now player + each NPC + world + reactivity). **Step 4 + Step 6 are
where one-shot is actually banned.**

## Navigation at junctions (propose the next move with choices)
The pipeline is not a silent march down a locked plan: at each junction the step **proposes what's next and
offers the choices**, so the user always sees where things are headed and keeps the wheel.
- **Step 4** (`references/step-4-deep-design.md`): the four-pass ORDER is fixed (supply→demand→stage), but
  *within* the NPC pass "which NPC next" and *at* each pass boundary "ready to move from the player to the
  NPCs?" are real junctions. Propose from the ledger's `deep_design` block — the next subject + a one-line why
  + the alternatives; the user picks or says continue. A lightweight offered choice, not a heavy gate (Mode A
  only when it's a genuine fork; otherwise inform and proceed).
- **Step 5** (`references/step-5-feedback.md`): the `feedback.open_gaps` list IS the junction menu — propose
  which gap to fix first; **Mode A** on a gap whose fix changes the game's identity, **Mode B** for routine.
The point: never barrel down a locked plan — show the board (what's done / what's left), propose the next
piece, keep the choice with the user. The proposal is always offered; accepting it is one word, so it never
becomes death-by-questions.

## The anti-hallucination contract (Law 3, made concrete)
- **Unsure on a creative/identity call → ASK (Mode A), don't guess.**
- **Engine/reference facts → VERIFY against the files** before relying on them. (Agents hallucinate doc
  structure, fictional trigger keys, non-existent primitives — read the file; don't trust recall.) Only
  cite **real engine knobs** (see the SKILL.md engine ground-truth callout).
- **Every increment BUILDS GREEN** before the next (Step 6). A red build is a stop, not a footnote.
- **Assumptions are STATED** ("I'm assuming X — stop me if wrong"), never buried.
- **A change of plan is surfaced**, not silently absorbed.

## Anti-patterns (the process failures this bans)
- **The one-shot dump** — generating the whole game (or a whole phase) in a single pass. *(The LC/LS origin sin.)*
- **The black box** — writing design/code the user never saw described in plain language.
- **Death by questions** — Mode-A questions for non-crucial, derivable decisions.
- **Silent invention** — filling a gap with a guess instead of an ask or a verification.
- **Assumed-green** — moving on without building/validating the last increment.
- **Code-first surprise** — changing the design *in* the TOML instead of bouncing it to the design book.

## Cross-references
`redesign_phase_3/16` (full detail) · `references/ledger-schema.md` (the `pipeline_phase` this advances) ·
every step reference (each runs this rhythm) · `references/beat-authoring.md` (Step 6 — where build-green
makes the contract bite).
