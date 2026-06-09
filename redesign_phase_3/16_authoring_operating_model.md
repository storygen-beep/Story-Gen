# The authoring operating model — how the pipeline RUNS (the interaction contract)

Every other doc in Phase 3 says *what* to build. This one says *how the building is run* — the process
contract between the skill and the user. It exists because the prior failure (LC/LS) wasn't only a design
failure; it was a **process** failure: the game fell out of one blind one-shot dump, so it couldn't be
*felt* into shape and the user couldn't steer before the mistakes were load-bearing. Dry-run #2 (`15`)
proved it in miniature — the back half rotted into management and nobody saw until we *walked* it.

**The fix is structural: after setup, the game is NEVER generated in one shot. It is built one verified
piece at a time, with the user in the loop, and nothing is invented silently.** This doc is that rule.

---

## The three laws

1. **Incremental after setup.** Setup is one conversation; everything after it is written in **increments**,
   one piece at a time, each surfaced and (where it matters) approved before the next. No "generate the
   whole game" call, ever.
2. **Visible, not silent.** The user always **knows what is being written** — in plain language, at the
   design level — *before* it becomes code. The user does not review every line; the user reviews *intent*.
3. **Grounded, not hallucinated.** No creative or technical decision is invented out of nothing. Crucial
   forks are **asked**; engine/reference facts are **verified against the files**; every increment is
   **built green** before the next leans on it; assumptions are **stated out loud**.

Everything below is the mechanics of these three.

---

## Increment ≠ slice (the disclaimer that prevents a regression)
Incremental is the **build ORDER, not the final SIZE.** Scope is still the **full game** (slice scope was
removed and stays removed). We build the whole game — just one verified piece at a time, converging on the
whole. "Incremental" must never be read as "ship a slice."

---

## Two interaction modes — keep them separate

The user named two distinct needs; conflating them is the failure (a black box on one side, death-by-a-
thousand-questions on the other).

### Mode A — DECISION GATE (`AskUserQuestion`)
Used **only at crucial forks** — where the answer **changes the game's identity** AND can't be derived from
what's already decided. Always: 2–4 concrete options + **a recommendation** (recommended option first,
labelled). The user can always pick "Other."

**Crucial (ask):** POV + the core fantasy · the charge/ceiling level (how explicit, non-con in or out) ·
who the core target(s) are + each one's hook · the economy shape (which income/pressure paths) · the
ending shape · any genuine creative fork with no derivable answer.

**Not crucial (never ask — just do it):** flag/trait names, lane numbers, file layout, which engine
primitive, scene ordering within an approved arc, prose wording, any mechanical translation of an
already-approved design.

**Batch per checkpoint.** One question-set carries a phase's crucial forks together — not one question per
micro-decision. A dozen decision gates across a whole game is the right order of magnitude, not a hundred.

### Mode B — INFORM-AND-PROCEED (a short plain-language note)
This is the *visibility* the user means by "I should know what's being written." Before/after each
increment, a **skimmable** plain-language statement of what the piece *is* — not a request for permission,
just the lights kept on. The user can interrupt any of them. Most of the loop is Mode B.

**The calibration rule (the whole skill of it):** *ask the crucial, inform the rest, invent nothing
silently.*

### The per-increment rhythm — ideate → decide → write (`20` decision 6)
Every increment after setup runs the **same three-beat loop**: **ideate → decide → write** (→ **verify
green** at Step 6) → next. It's **uniform across Steps 2–6** — only what "write" produces changes
(design-book prose in Steps 2–5; TOML-that-must-compile in Step 6). The split above is just the
*throttle* on it: at a **shape-setting** increment, ideate-and-decide happens **with the user** (Mode
A); at a **routine** increment, I ideate internally, decide, write, and report in one line (Mode B). So
the honest model is *not* "brainstorm-and-ask every piece" — it's **"every piece is ideated and never
invented blind; the crucial ones we decide together, the routine ones I write and report."**

---

## The review surface is the DESIGN BOOK, not the TOML
The crux of "I don't review each line of code, but I know what's written." The user reviews **intent in
plain language — the design book** (`design_book.md`). The TOML/engine layer is the *faithful translation*
of a design that was already surfaced and okayed, so the code can't surprise the user — the design it came
from didn't. This is the `what-before-how` split (`README`, `00_CONTEXT`) made into a process rule:
- **Creative layer → the design book → the user's review surface.**
- **Engine layer → the authoring step → derived from the approved design, built green, not separately
  reviewed line-by-line.**

If a technical reality forces a design change (an engine limit, a gotcha), that bounces **back up to the
design book** and is surfaced — it does not get silently patched in the code.

---

## The increment ladder — what "one by one" means at each phase
The unit of increment changes as the pipeline proceeds. Each phase has its mode and its checkpoint.

| Phase | Increment unit | Mode at the gate | Checkpoint output |
|---|---|---|---|
| 0 — fantasy/POV (`05`) | the whole fantasy | **A** (POV · fantasy · charge · desire-span) | the locked fantasy line + bar |
| 1 — setup (`01`) | one conversation | **A/B** (the bare seed) | the seed (premise·cast·map·systems) |
| 2 — top-level (`04`/`09`/`11`/`13`/`14`) | the spine | **A** (cascade shape · economy shape · ending shape) | the desire ladder + engine + economy in the book |
| 3 — casting (`06`) | the cast as a set | **A** (core targets + hooks; confirm cuts) | the casting table |
| 4 — NPC arcs (`07`) | **ONE NPC at a time** | **A** per *core* NPC's brief; **B** for peripherals | each approved R7 brief in the book |
| 5 — content roster (`content-design`) | the scene list | **B** (surface the list; **A** only on a real fork) | the roster |
| 6 — authoring | **scene by scene / NPC by NPC** | **B**, **build green each increment** | working, compiled scenes |

The two heaviest interaction points are **Step 2** (identity-setting, cheap on paper — ask freely) and
**Step 4** (one NPC at a time — the heart of incremental authoring). Step 6 is mostly Mode B + the
build-green discipline.

---

## Step 4 + Step 6 are where one-shot is actually banned
The temptation to "just generate it all" lives here. The rule:
- **Step 4 — one NPC per increment.** Surface the brief (expanded hook · spine · double-locked rungs ·
  capstones · ceiling), get the core ones okayed, *then* move to the next NPC. Never author the whole cast's
  arcs in one pass. This is *also* how each NPC is held to the 8 qualities (`05`) **before** the next leans
  on it — the per-increment quality gate that a one-shot can't have.
- **Step 6 — one scene/NPC per increment, built green before the next.** Author a unit → compile/validate →
  confirm it runs → next. Errors are caught locally, at the seam, not discovered as a pile at the end. (This
  is the anti-hallucination law in engineering form: correctness *verified*, never assumed.)

---

## The anti-hallucination contract (Law 3, made concrete)
- **Unsure on a creative/identity call → ASK (Mode A), don't guess.**
- **Engine/reference facts → VERIFY against the files** before relying on them. (We've been burned: agents
  hallucinate doc structure, fictional trigger keys, non-existent primitives — `MEMORY` records several.
  Read the file; don't trust recall.)
- **Every increment BUILDS GREEN** before the next. A red build is a stop, not a footnote.
- **Assumptions are STATED** ("I'm assuming X — stop me if wrong"), never buried in the output.
- **A change of plan is surfaced**, not silently absorbed — if reality forces a deviation from an approved
  design, say so and re-confirm.

---

## What this buys (why it's load-bearing, not bureaucracy)
- **Steerability** — the user shapes the game while it's cheap to shape, not after it's set in code.
- **The quality bar actually bites** — the 8 qualities / double-lock / desire ladder / the six `15`
  refinements are *enforced per increment*, instead of hoped-for across a blind dump. Incremental is what
  makes the rest of Phase 3 real rather than aspirational.
- **No black box** — the user always knows the game's state in plain language.
- **Local failure** — design and build errors surface at the seam, not as an end-of-run avalanche (the LC
  experience).

---

## Anti-patterns (the process failures this bans)
- **The one-shot dump** — generating the whole game (or a whole phase's worth) in a single pass. *(The LC/LS
  origin sin.)*
- **The black box** — writing design/code the user never saw described in plain language.
- **Death by questions** — asking Mode-A questions for non-crucial, derivable decisions.
- **Silent invention** — filling a gap with a guess instead of an ask or a verification.
- **Assumed-green** — moving to the next increment without building/validating the last.
- **Code-first surprise** — changing the design *in* the TOML instead of bouncing it back to the design book.

---

## Self-check (run the process against itself)
- Is anything being generated in **one shot** after setup? → stop, break into increments.
- For the current piece: is this a **crucial fork** (ask, Mode A) or a **derivable detail** (inform, Mode B)?
- Does the user **know, in plain language**, what this increment is — *before* it's code?
- Is every engine/reference claim **verified against a file**, not recalled?
- Did the last increment **build green** before this one started?
- Are decisions **batched per checkpoint** rather than dribbled out?
- Is the **design book** (not the TOML) the thing the user is reviewing?

---

## Implementation note (for later — not now)
This relocates and hardens what the skill already half-does: `setup-interview.md` is interactive at setup;
this doc extends that interactive, incremental, user-in-the-loop discipline across **the entire pipeline**
(Steps 2–6), and makes the ask-vs-inform split + build-green-per-increment + design-book-as-review-surface
explicit. When the pipeline is wired into `author-game/SKILL.md`, the SKILL flow must encode: per-phase
checkpoints, Mode-A gates only at the crucial forks listed above, Step-4 one-NPC-at-a-time, Step-6
one-scene-at-a-time-build-green. No skill/code changes here — spec only.

## Cross-references
- `00_CONTEXT.md` / `README.md` — the what-before-how split this turns into a process rule.
- `01_STEP1_SETUP_LOCKED.md` — setup = the one conversation before increments begin.
- `05`–`14` + `15` — the *what* this process is built to deliver per-increment (the quality bar that
  incremental enforcement makes real).
- `07_npc_arc_step.md` — Step 4, the one-NPC-per-increment heart.
- Existing skill: `setup-interview.md` (interactive setup, the seed this extends), `toml-gotchas.md` /
  build pipeline (the green this checks each increment against).
