# /effort - Read-Only Task Effort Estimate

## Purpose

Size a task before touching it. `/effort` is the standing-rule-#2 command: analyze
read-only first, surface the real options, hand LO a sized estimate — then stop.
**No files are changed. No build is run. Nothing is committed.** This command only reads.

## Usage

```
/effort <task description>
```

**Examples:**
```
/effort add a new NPC arc to step_sister_wedding
/effort fix the flag chain that breaks at T3 in the morning routine
/effort make the importer escape source bytes correctly
```

---

## When This Command Runs

Treat the argument as the task to size. Work the evidence, not your memory
(standing rule #1 — no hallucination). Concretely:

1. **Locate.** Grep / glob the files the task would touch. Name them at `file:line`.
2. **Read.** Skim the relevant code, TOML, or skill doctrine read-only. Do not edit.
3. **Place the layer.** If it's a built-game bug, decide which of the three layers
   owns it — one-off TOML, skill/doctrine, or engine (see CLAUDE.md). Say which.
4. **Estimate.** Return the report below. Then stop and wait for LO's call.

If the task is ambiguous enough that the estimate would be a guess, say so and ask
one sharp question instead of inventing a number.

---

## Output — the estimate

Return exactly this shape, RTS-flat, no filler:

```
TASK:   <one-line restatement>
SIZE:   S | M | L | XL          (with a one-line why)
LAYER:  one-off TOML | skill/doctrine | engine | n/a (non-game code)
FILES:  <file:line> — <what changes there>
        <file:line> — ...
RISKS:  <the real failure modes — flag collisions, UUID rebuilds, fail-open, etc.>
STEPS:  1) ...
        2) ...
        3) ...
UNKNOWNS: <what you couldn't verify read-only, if anything>
```

### Size rubric
- **S** — one file, no flag/graph changes, no rebuild surprises. Minutes.
- **M** — a few files or one flag chain / canvas; predictable. An hour-ish.
- **L** — cross-cutting: multiple canvases, a lane restructure, or skill + game both.
- **XL** — engine-level or a bug class that recurs across games; needs a real plan.

### Bug-class test (when sizing a fix)
Always answer: **"Would a correct author-game skill have prevented this?"**
- Yes → the estimate must include fixing the **skill/corpus**, not just the game.
- No → size the one-off or engine fix alone.

---

## Hard rules
- **Read-only.** No Edit/Write, no merge, no package, no commit. Estimating is the
  whole job; LO drives one task at a time and decides whether to proceed.
- **Evidence, not vibes.** Every claim about the code traces to a grep, a `file:line`,
  or a read — never an assumption.
- **No buzzwords.** Flat and specific. "Touches 3 canvases, two share a flag" beats
  "moderately complex refactor."
