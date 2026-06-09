# Step 1 — Setup (LOCKED)

**Status: LOCKED** (2026-06-08). The first step of the Phase-3 pipeline. See `00_CONTEXT.md` for the
whole pipeline and the decision rationale (D1–D11).

---

## Purpose

Plant the **creative seed** of the game — nothing more. Setup answers *"what is this game, roughly?"*
in plain English and writes it into the **design book**. It does NOT design the story, the characters'
arcs, the scenes, or any engine plumbing. It is deliberately the **leanest** step: a short intake
conversation that gives the later steps something to grow from.

**One-line:** setup is the bare seed; every later step grows one layer on top of it.

---

## What Setup contains (exactly four things)

All four are plain-words creative choices, written into `design_book.md`. Nothing technical.

1. **Premise / setting / player**
   - Who the player is, where the game takes place, the central hook.
   - **The protagonist POV (male/female) is INHERITED from Step 0a** (`05`) — it's decided *with the
     fantasy*, not here; setup just carries it. (Female PC is the RTS-native / cascade-native default.)
   - Includes the creative-level player choice: is the player named / customizable? (a creative
     decision about the character — NOT the `@`-token wiring, which is authoring-step plumbing).

2. **Cast — names + roles only**
   - List the characters as *people*: e.g. "Sal the bartender, Dee the supplier, Marcus a regular."
   - **NO arc shape, NO voice, NO vocab ceiling, NO stats** at this point (those are the NPC-arc step).
   - The cast is part of the creative seed (decision D8, option a) — characters do NOT "emerge" from
     the story spine later; setup names them up front, lightly.

3. **World map — the locations**
   - The places the game happens (the bar, the back room, the apartment, the docks…).
   - Just the creative geography. No `is_container` / lock / schedule / `entry_conditions` decisions
     (those are authoring-step plumbing).

4. **Which systems exist — yes/no only**
   - Does the game use **phone** / **clothing** / **rent**? A pure creative scope choice
     ("this game has a phone"). (Decision D5.)
   - NOT the wiring, the TOML homes, or the settings blocks — those are the authoring step.

---

## What Setup explicitly does NOT contain (and where each moved)

| Pushed out of setup | Now lives in |
|---|---|
| Scope (slice vs full) | **Removed entirely** — always full game (D9) |
| Loose story order / roadmap | **Step 2 — Top-level design** (D7) |
| Economy + time / day rhythm | **Step 2 — Top-level design** (D6) |
| Story spine, progression, world logic, endings | **Step 2 — Top-level design** (D10) |
| Arc shape (slow-burn / dating / leverage / service / antagonist) | **Step 4 — NPC arcs** (D3) |
| Voice (how a character sounds) | **Step 4 — NPC arcs** (D2) |
| Vocab ceiling (how explicit a character goes) | **Step 4 — NPC arcs** (D4) |
| The scene list / content roster | **Step 5 — Content roster** (D11) |
| Flags, traits, core_traits, trait names | **Step 6 — Authoring** (D1) |
| Quest-card TOML, schedules, settings homes | **Step 6 — Authoring** (D1) |
| Ledger **structure/plan** seeding (`structure_registry` / `plan` / `produced_canvas_ids`) | **Step 6 — Authoring** (D1) — *but the ledger FILE itself is created at setup, see below* |
| The green build / scaffold TOML emission | **Step 6 — Authoring** (D1) |

> **Numbering note:** this table now uses the **6-step** scheme (0 good-game · 1 setup · 2 top-level ·
> 3 casting · 4 NPC arcs · 5 roster · 6 authoring) — the casting step (`06`) split NPC arcs and roster
> down one each. (Earlier drafts used a 5-step scheme with no separate casting step; `20` decision 8.)

---

## Why setup is creative-only (the rationale)

- **Plumbing decided early goes stale.** You don't know which flag/trait a scene needs until you write
  that scene. Choosing them at setup means guessing — and guessing wrong, then carrying the wrong
  schema forward.
- **Keeps the user in the creative seat.** The user (LO) is making creative calls at setup, not
  choosing trait names or TOML structure. The engine translation happens later, by the agent.
- **Keeps setup fast.** A short intake instead of a long technical interrogation; the heavy design
  work happens in the dedicated later steps where it has room to breathe.

---

## How Setup runs (interaction model)

- A short **interview**, one question at a time, via **AskUserQuestion** — each with 2–4 concrete
  options + a recommendation (the established skill convention). Skip anything the concept input
  already answers; state the default, don't ask.
- Setup is creative, so the questions are creative: "who's the player?", "what's the hook?", "who's in
  the cast?", "what locations?", "does the game have a phone/clothing/rent?".
- **No scope question** (always full game).

---

## Output artifact

Setup writes the **seed sections of `design_book.md`** only:
- World setup (premise / player / setting)
- Cast (names + roles)
- Locations (the map)
- Systems in use (phone / clothing / rent — yes/no)

It does **not** write per-NPC briefs (that's the NPC-arc step), the story spine (top-level step), the
roster (content step), or any TOML (authoring step).

**The ledger file IS created at setup** (`20` decision 4) — but only as the **pipeline-phase tracker**
(which step we're in, what's done). It's bookkeeping JSON, so it compiles nothing and can't fail a
build; creating it early costs nothing and lets the skill resume anywhere by reading its phase. Its
**creative/structure parts** (`structure_registry`, `plan`, `produced_canvas_ids`) stay **empty** until
Step 6 fills them. So: ledger *born* at setup; ledger *populated* at authoring.

---

## Open / to-confirm when we wire it
- Exact handoff to Step 2: setup ends by producing the seed; Top-level design reads it and begins the
  story/world/economy spine. (Define when Step 2 is designed.)
- Whether setup also records a one-line "tone/genre" note for the cast/world, or that's purely premise.
  (Minor; resolve during implementation.)
