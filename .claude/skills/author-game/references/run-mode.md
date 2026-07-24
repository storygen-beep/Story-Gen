# Run mode — how the pipeline RUNS (the interaction contract)

Every other reference says *what* to build; this one says *how the building is run* — the process contract
between the skill and the user. It exists because the prior failure (LC/LS) wasn't only a design failure;
it was a **process** failure: the game fell out of one blind one-shot dump, so it couldn't be *felt* into
shape and the user couldn't steer before the mistakes were load-bearing.

**The fix: after setup, the game is NEVER generated in one shot. It is built one verified piece at a time,
with the user in the loop, and nothing is invented silently.** This applies across **Steps 2–7** (Steps 0–1
are the one upfront conversation).

---

## The three laws
1. **Incremental after setup.** Everything after the seed is written in **increments**, one piece at a time,
   each surfaced and (where it matters) approved before the next. No "generate the whole game" call, ever.
2. **Visible, not silent — in PLAIN language.** The user always **knows what is being written** — *before* it
   becomes code, and said in **plain, simple language**: short everyday words, no unexplained jargon, a
   concrete example over an abstraction. The user reviews **intent**, not every line — and intent is only
   reviewable if it's actually readable. When a mechanism term is unavoidable (lane, odometer, capstone),
   gloss it in plain words the first time. This holds for every note, proposal, and question, in every step.
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
  the core target(s) are + each one's hook · the economy shape · the frontier/ending shape · **each shared
  private space's perception (per place: walk-in / peep / occupied / caught — `content-framework.md` §5H;
  grounded in the place, never a game-wide toggle)** · any genuine creative fork with no derivable answer.
- **Batch per checkpoint.** One question-set carries a phase's crucial forks together — not one question per
  micro-decision. A dozen decision gates across a whole game is the right order of magnitude, not a hundred.

### Mode B — INFORM-AND-PROCEED (a short plain-language note)
The *visibility* the user means by "I should know what's being written." Before/after each increment, a
**skimmable** plain-language statement of what the piece *is* — not a request for permission, just the
lights kept on. The user can interrupt any of them. **Most of the loop is Mode B.**
- **Not crucial (never ask — just do it):** flag/trait names, lane numbers, file layout, which engine
  primitive, scene ordering within an approved arc, prose wording, any mechanical translation of an
  already-approved design.
- **Blueprint (Step 5) is the opposite — it PROPOSES before it writes.** lane choice, scene ordering, and gate
  philosophy are NOT decided silently there: Blueprint proposes a subject's plan in plain words and brainstorms
  the real forks *before* writing (propose → explain → brainstorm → write). The "never ask about lanes/ordering"
  rule above is reversed **only in Blueprint**, because structuring is its whole job. Held per subject, never
  per scene — a silent write and a question-per-scene are both failures.

**The calibration rule:** *ask the crucial, inform the rest, invent nothing silently.*

## The per-increment rhythm — ideate → decide → write
Every increment after setup runs the same three-beat loop: **ideate → decide → write** (→ **verify green**
at Step 7) → next. Uniform across Steps 2–7 — only what "write" produces changes (design-book prose in
Steps 2–6; TOML-that-must-compile in Step 7). The *throttle* on it is the ask/inform split: at a
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
| 4 — design (story) | **ONE subject at a time:** player → NPCs (one each) → world → reactivity | **A** at each subject boundary + per *core* NPC; **B** for peripherals/routine |
| 5 — blueprint | **ONE subject's scene list at a time** (lane / gate / placement / order) | **Propose-first:** propose the subject's plan in plain words + brainstorm the real forks, THEN write — never a silent write, never a question per scene |
| 6 — feedback | **ONE subject's question-cluster at a time** (the review) | **B**; **A** on any gap whose fix changes identity |
| 7 — authoring | **scene by scene** | **B**, **build green each increment** |

The two heaviest interaction points: **Step 2** (identity-setting, cheap on paper — ask freely) and **Step
4** (one subject at a time — the heart, now player + each NPC + world + reactivity). **Step 4 + Step 5 + Step 7
are where one-shot is actually banned** (imagine the story, decide the structure, build the TOML — each one
verified piece at a time).

## Navigation at junctions (propose the next move with choices)
The pipeline is not a silent march down a locked plan: at each junction the step **proposes what's next and
offers the choices**, so the user always sees where things are headed and keeps the wheel.
- **Step 4** (`references/step-4-deep-design.md`): the four-pass ORDER is fixed (supply→demand→stage), but
  *within* the NPC pass "which NPC next" and *at* each pass boundary "ready to move from the player to the
  NPCs?" are real junctions. Propose from the ledger's `deep_design` block — the next subject + a one-line why
  + the alternatives; the user picks or says continue. A lightweight offered choice, not a heavy gate (Mode A
  only when it's a genuine fork; otherwise inform and proceed).
- **Step 5 Blueprint** (`references/step-5-blueprint.md`): subject by subject like Step 4 — but Blueprint
  **proposes the whole plan for a subject and brainstorms it before writing** (propose → explain → brainstorm →
  write; never a silent write). The structuring forks (a gate philosophy, an ordering) ARE the brainstorm, held
  per subject, not per scene. Propose the next subject from the `blueprint` block at each boundary.
- **Step 6** (`references/step-6-feedback.md`): the `feedback.open_gaps` list IS the junction menu — propose
  which gap to fix first; **Mode A** on a gap whose fix changes the game's identity, **Mode B** for routine.
The point: never barrel down a locked plan — show the board (what's done / what's left), propose the next
piece, keep the choice with the user. The proposal is always offered; accepting it is one word, so it never
becomes death-by-questions.

**What the proposal has to CONTAIN is a separate question from when you offer it — and it's the one that
decides whether the game is hot or merely well-built.** Any pitch of *content* (a beat, an arc, an NPC, a
chunk) carries the five parts and passes the heat test in `references/pitching.md`. This section owns the
junction mechanics; that file owns the pitch quality. They compose: when a Mode A fork above is *also* a
content pitch (core targets + their hooks, the frontier shape), still ASK — but the options you offer are
**fully-written pitches**, never abstract labels.

## Systems grow through iteration — playable ≠ done
The pipeline gets you to a **playable** game; it does not get you to a **finished** one. A playable build is
*"playable, keep iterating,"* not *"done."* You will NOT have decided every system at the seed — most **emerge**
only once the game is concrete and you've played it and *felt* a gap ("this day is thin," "she needs a way to
pass as staff," "the fight needs stakes"). That is normal, good design — not a planning failure.

What matters is HOW a discovered system gets folded in. The failure mode (the first games) is jamming it
straight into TOML as a raw Step-7 beat — skipping the design passes — after the project has quietly decided
it's "done." Instead, give a mid-stream system the **same quick passes a day-one system gets**, just entered
where you are:
1. **What / why / how it feels** — a short design-book note: what the system is, why the game needs it now, how
   it should FEEL. *(the Step-4 story pass, in miniature)*
2. **Place it** — which locations / traits / gates, how it wires into the machine and the day; register the new
   pieces in `structure_registry`. *(the Step-5 blueprint pass, in miniature)*
3. **Build + verify green** — author it, build, live-check it. *(Step 7)*
4. **Fold the ripple back** — update the design book + ledger so the record still matches the game.

Before inventing a system live, open `references/system-patterns.md` — the menu of common ones (disguise,
capability, crawl, second economy, reload, loadout, day-depth, accumulation) with a ready recipe each. Grab the recipe, run
it through the four passes above.

On a **shipped** game (players may hold saves), a mid-stream system may only ADD — never rename a live
id/flag/trait key, rescale a stat, or change the title (`references/save-safety.md`).

> Discovering a system late is fine; *duct-taping* it is not. Same rigor, entered mid-stream.

## The anti-hallucination contract (Law 3, made concrete)
- **Unsure on a creative/identity call → ASK (Mode A), don't guess.**
- **Engine/reference facts → VERIFY against the files** before relying on them. (Agents hallucinate doc
  structure, fictional trigger keys, non-existent primitives — read the file; don't trust recall.) Only
  cite **real engine knobs** (see the SKILL.md engine ground-truth callout).
- **Every increment BUILDS GREEN** before the next (Step 7). A red build is a stop, not a footnote.
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
`references/ledger-schema.md` (the `pipeline_phase` this advances) ·
every step reference (each runs this rhythm) · `references/beat-authoring.md` (Step 7 — where build-green
makes the contract bite).
