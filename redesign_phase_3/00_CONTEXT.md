# Redesign Phase 3 — Context & Overview

**What this is:** a ground-up restructure of the **author-game skill's authoring pipeline** — the
ordered set of steps the agent (Claude) follows to take a game from a blank idea to a built,
playable game. Started 2026-06-07/08 as a brainstorming + optimization pass. **We are SPEC'ing the
new process on paper first — no skill files are being edited yet** (explicit user constraint:
"Dont make any changes, we are brainstorming and optimizing the game gen process").

This folder is the durable record so the work survives context resets. Each step of the new pipeline
gets locked into its own file as we finish designing it.

---

## How we got here (the trail this session)

1. **RTS player-corruption investigation.** User asked what raises *player* corruption in RTS early
   and what it unlocks. Mined RTS live (twine-game-explorer, slug `rts-align-verify`): player
   corruption = `+1` per charged act, **hard cap 45**, bands `<5 / 5-14 / 15-29 / 30-44 / >=45`; the
   bands gate content tiers (flash 15 / sex 30 / public-sex 45). Bootstrap feeders (Watch Porn,
   grope) are ungated at corruption 0. Full evidence:
   `game_explorations/rts-align-verify/rts_scene_registry.json` (71 scenes / 27 venues) + that slug's
   `notes.md`.

2. **The "missing content writer" reframe.** User said the skill is "missing a lewd creative content
   writer." First mis-read as a *prose-craft* gap; user corrected: **NOT prose** (that's covered by
   `doctrine/08` vocab ceilings + the RTS-flat / Tier-3 register rules). The real gap = **nothing
   decides WHAT canvases/scenes the game should have.** The skill teaches *how* to write a canvas and
   gives each NPC a *budget of empty slots* — but never *what fills them*. And it's entirely
   NPC-arc-centric: the whole category of **player/world lewd activities** (solo self-acts, public
   flashing, dares, job-lewd — the things that feed the player's own corruption/exhibitionism
   odometers) has no home. That's why Last Call starves its player-corruption odometer.

3. **Shipped a first fix (content-design pass).** NEW `references/content-design.md` (the "what scenes
   exist" ideation step + RTS-derived 9-archetype catalog + the **feeder economy** concept + the
   **content roster** artifact), wired into SKILL.md / setup-interview.md (Step 3.5) / beat-authoring.md
   / lanes.md. Skill-only, uncommitted. Recorded in memory `content_design_pass.md`. **NOTE: this was
   built into the OLD pipeline shape; Phase-3 restructure supersedes where it sits (the roster moves
   to step 4 — see pipeline below).**

4. **The bigger realization → this restructure.** Designing the content-design pass exposed that the
   whole pipeline is mis-layered: setup mixes creative decisions with engine plumbing; there's no
   top-level game/world/story design before NPC arcs; "what before how" isn't enforced as the spine of
   the process. So we're restructuring the entire pipeline.

---

## The core principle

**Decide WHAT before HOW — nested.** The whole pipeline is layers of *what*, narrowing, until the very
last step which is *how*:

> what is the game (system/story) → what does each character do → what scenes exist → HOW to write them

Every step should be one layer down, and the **technical/engine layer (flags, traits, TOML, ledger,
build) is pushed to the very end** so nothing gets encoded before it's known (you don't know the flag a
scene needs until you write that scene; plumbing decided early goes stale).

Two layers the redesign keeps strictly separate:
- **Creative layer** — what the game IS, in plain English, into the **design book**.
- **Technical layer** — how the engine stores it (flags, traits, trait names, TOML homes, schedules,
  the quest-card TOML, the ledger JSON, the green build). Deferred to the authoring step.

---

## The new pipeline (target shape)

```
1. Setup          → bare creative seed (premise · cast names+roles · world map · which systems exist)
2. Top-level      → story order/roadmap, story spine, world logic, economy, time/day rhythm,
   design          progression spine, how player-state changes the world, endings/win-lose
3. NPC arcs       → per character (off the spine): arc shape, voice, vocab ceiling, the arc design.
                    Claude uses AskUserQuestion to offer options the user picks from.
4. Content roster → the scene list — WHAT scenes/activities exist (both tracks: NPC-arc + player/world
                    feeder catalog), informed by the spine + the arcs. (= the content-design pass,
                    moved here from old setup Step 3.5.)
5. Authoring      → write the actual canvases + ALL technical plumbing (flags, traits, TOML, ledger,
                    build). The only "how" step.
```

**Status:** Step 1 LOCKED (see `01_STEP1_SETUP_LOCKED.md`). Steps 2–5 not yet designed.

---

## Decisions log (locked, with rationale)

- **D1 — Setup is creative-only.** No flags/traits/TOML/ledger/build in setup. *Why:* keep the user
  making creative calls, not wrangling engine schemas; early plumbing goes stale.
- **D2 — Voice moves out of setup → NPC-arc step.** Voice is writing craft, not structure. Moved, not
  deleted (deleting risks the "character drifts/contradicts" problem — the Marge precedent).
- **D3 — Arc shape moves out of setup → NPC-arc step.** (User answered "No" to keeping it in setup.)
  At setup the cast are just *people*; their shapes are designed later.
- **D4 — Vocab ceiling moves out of setup → NPC-arc step** (sits next to voice).
- **D5 — Systems (phone/clothing/rent) STAY in setup** — but only the yes/no creative choice ("does
  the game have a phone?"), never the wiring.
- **D6 — Economy + time/day feel move out of setup → Top-level design step.**
- **D7 — The loose story order / roadmap moves out of setup → Top-level design step.** It's story, not
  seed.
- **D8 — Setup still names the cast (option a)** — names + roles only; characters do NOT "emerge" from
  the spine. The cast is part of the creative seed.
- **D9 — Scope is ALWAYS full game. Slice scope REMOVED.** *Why:* removes a whole conditional axis
  (budgets, depth, Phase-2+ defer shortcut, minimum-contract rest). *Trade-off accepted:* we lose the
  "ship a small testable slice first" option — every game is designed/built to completion.
  *Application:* fold the slice removal into THIS restructure (don't do a standalone cleanup of the
  current skill first — we're rewriting setup/budgets anyway; doing it twice is wasted work).
- **D10 — A Top-level design step is ADDED before NPC arcs.** *Why:* designing NPCs first yields a bag
  of disconnected arcs with no through-line; the arcs need a spine to hang off. The top-level step is
  the game's "operating system" and the highest form of "what before how."
- **D11 — The content roster moves from old setup Step 3.5 → its own step 4** (after spine + arcs),
  because the spine tells you what content the game needs.

---

## Carry-over concepts (already designed, still valid — context for later steps)

- **Two content tracks** (for step 4): NPC-arc track (the four lanes) + player/world track (the
  feeder catalog the lanes omit).
- **The feeder economy** (load-bearing, for steps 2 & 4): NPC seduction content gates on a *player*
  corruption FLOOR (RTS `requirementsMC` — the two-axis gate). Player-track activities are the SUPPLY
  that raises the odometer; the floors are the DEMAND. Build the supply or the arcs stall. This is the
  exact mechanism behind LC's starvation.
- **The 9-archetype catalog** (RTS-derived, for step 4): solo self-act / location flash / location
  sex-escalation column / job-service ladder / public dare line / household grope-tease / voyeur /
  transit ambient / story-condition special. Source:
  `game_explorations/rts-align-verify/rts_scene_registry.json`.
- **The design book** is the single creative artifact every step writes into (per-game
  `design_book.md`); per-NPC briefs are the structured profiles inside it.

---

## What's next

Design **Step 2 — Top-level design** (the big new phase): what questions it asks the user, what it
produces in the design book (story spine, progression, world economy, time rhythm, endings). Then
Step 3 (NPC arcs), Step 4 (content roster, re-homing the content-design pass), Step 5 (authoring +
all technical). Lock each into its own numbered file here as it's finished.

---

## Source materials / pointers
- Current skill: `.claude/skills/author-game/` (SKILL.md + references/). The pipeline being replaced
  lives in `references/setup-interview.md` (old setup, Steps 1–7) + `beat-authoring.md` (continue loop).
- The content-design pass (step-4 seed): `references/content-design.md`.
- RTS evidence: `game_explorations/rts-align-verify/` (`rts_scene_registry.json`, `notes.md`).
- Memory: `content_design_pass.md`, `rts_arousal_system.md` (throttle/odometer + LC trait pass),
  `author_game_skill.md`.
- Constraint reminder: **brainstorm/spec mode — do NOT edit skill files until the user says implement.**
