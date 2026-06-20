# The MACHINE — cross-wiring as a designed top-level layer (the G5 fix)

The depth layer the pipeline was missing. The 2026-06-10 field survey (`21`) found that the deepest
sandboxes (esp. *Become Someone*) get their depth NOT from any single arc being clever, but from
**cross-wiring**: the game is **one machine** where the NPC arcs, the economy, and the player's rise all
read/write a shared state and feed each other in a loop (corrupt the boss → wage up → afford the
apartment → fund the next conquest). The earlier pipeline designed each arc as an island and bolted
connections on at casting as optional "rough-sketch threads" (`06`/`20` decision 7). This doc promotes
the connections to a **designed top-level layer** — *the machine* — settled up front in Step 2 alongside
the cascade (`04`), economy (`13`), and frontier (`17`); the arcs are then authored as **components that
plug into a machine that already exists on paper.**

**Position:** a Step-2 design layer, conceptually between `13` (the micro economy of one player's own
arcs) and `17` (the macro steady-state). It does **not** add a pipeline step — like the cascade and the
economy, it's a section of Step 2's output (a `## The machine` block in `design_book.md`).

**Decision-7 reconciliation.** Decision 7 (`20`) dropped "the cross-NPC web + weave checkpoint" as
over-engineering. What it correctly killed was a **bookkeeping diagram with no payoff**. What returns here
is different: **the machine as the depth SPINE** — designed as plain-language intent in the design book
(the review surface), same status as the cascade/economy already have, realized with ordinary engine
knobs. Casting's "light threads" (`06`) remain the *seed*; they now plug into a machine designed up front
rather than being the whole cross-NPC story. (`20` decision 7 is refined to say this.)

---

## Scope — two forms now, the third deferred to G6
This layer ships **Form 1 + Form 2 only**. **Form 3 (compounding conquest — a *finished* arc becomes a
resource: income / staff / a key / a venue) is gap G6, a later pass.** Form 3 is the same idea as
`14` P7 / `13` E9's "recruits are arcs," seen from the output end; it gets its own doctrine + the `09`/`13`
E10/`17` amendments then. Here we wire arcs to each other and to the economy; we do not yet make finished
arcs *produce* capability. (Forward-pointer left so a future session knows where it lands.)

---

## The two forms of wire (in scope)

**F1 — Progression dependency.** Arc A's *mid/late rung* is gated on arc B's *stage*: "Mom won't go
further until your sister trusts you," "Sal won't cross the line while the bar's still in jeopardy."
The wire constrains **depth ordering** between arcs — the order in which their deep content opens.

**F2 — Arc↔economy circulation** (the heart — the economy is the connective tissue):
- **F2a (load-bearing).** Money *earned* from activity/arc A is the *gate* to reach B. The economy is what
  *carries progress between arcs* — you corrupt the boss / work the floor to *afford* the dress that opens
  the next target. This is `13`'s ladder turned into connective tissue: `13` says "earning = corrupting
  yourself"; F2a adds "earning = the thing that lets you reach the NEXT person." Expressible today with
  ordinary money gates + the income beats `13` already designs.
- **F2b (flourish).** A payout/price *banded* by an NPC's trait — the wage is higher when the boss is more
  corrupted, so corrupting him you already wanted to do *also* pays better. The flourish tier, not the spine.

---

## The CORE LOOP is the spine — design it first
Before placing any single wire, design the **one economic circuit** that ties conquest → money/access →
the next conquest. It is the machine's spine; every arc hangs off it somewhere. Worked (bar→empire):
*seduce/break the owner → take the bar → the bar's income funds recruiting girls → the girls' arcs earn →
that funds becoming the madam.* Once the core loop exists, each arc has a **place in the machine** (what it
feeds, what feeds it — `06` assigns this), not just a story. A game whose arcs don't share a loop is a
menu of parallel quests, not a machine — the islands failure the survey named.

---

## The three safety disciplines (why it must be DESIGNED, not improvised)
A real web can deadlock or soft-lock; these are the firewalls.

- **D1 — never gate an arc's ENTRY on another arc.** Cross-wires gate only **mid/late rungs and capstones**,
  never the first meeting / on-ramp. Every arc must still **begin from a cold start** (befriending is
  ungated — `04 §4`). So a wire only ever constrains *how deep* you can go in A before B advances — never
  *whether A is available.* This is also what **breaks dependency cycles by construction**: if no entry is
  ever gated, no two arcs can mutually lock each other out at the start. (The cold-start / no-backwards-on-
  ramp rule is the existing law this preserves — `04 §4`, `lanes.md`.)
  - **Introducing an arc LATER ≠ gating its entry.** A late-act recruit who isn't *present* until the bar is
    taken is the separate **on-ramp-stagger** pattern (her arc is introduced by a roadmap beat / her schedule
    begins in Act 3) — and she carries her own full self-contained ladder (`07 §3b`). That is fine: D1
    forbids putting a `conditions` cross-gate on a **present** arc's on-ramp (hiding an available NPC's
    first meeting behind another arc), NOT sequencing *when* an NPC enters the world. Once introduced, the
    recruit's on-ramp is ungated co-presence like any other arc.
- **D2 — no dependency cycles.** Two *mid-rung* gates can still interlock (A-rung-3 needs B-stage-2 while
  B-rung-2 needs A-stage-3). The machine's F1 wires must form a **DAG**. The roster self-check (`18`) traces
  it: every node cold-start-reachable, no cycle. A cycle = a deadlock = a build that *passes* and a game
  that bricks — caught only by this check.
- **D3 — every cross-gate is LEGIBLE.** A rung gated on another arc's state ships a **locked-visible
  telegraph that names that state** — "Sal won't go further while the bar's still in jeopardy" (naming
  `bar_seized`). An invisible cross-gate is a **soft-lock** — the field's own worst guidance bug (`21` §3E).
  This is the seam with G1: D3 *is* the cross-gate case of `14` L7 (the legibility rule). The machine's
  wires cannot ship without it.

---

## Realization — real engine knobs only (verified)
All cross-arc coordination runs on **player-namespaced** signals. There is **no** cross-NPC trait read
across canvases in the shipped engine, and **no** `value = f(trait)` effect — so:

- **F1 gate — milestone vs depth:**
  - *Milestone* ("the bar is seized," "Sal cracked") → a **shared player flag** the source arc SETS, read
    as `{ type = "flag", subject = "player", flag_key = "bar_seized", operator = "is_true" }`. (Shipped
    games already coordinate this way — `sal_opened_up`, `bar_seized` are all `subject="player"`.)
  - *"How far along"* (graded depth, "arc B is at least this deep") → the **`<npc>_stage` player trait**
    (stage integers live at `player.core_traits.<slug>_stage`), read as `{ type = "trait", subject =
    "player", trait_key = "<otherNpc>_stage", operator = "gte", value = N }`.
  - **Rule of thumb: milestone → flag; "how far" → stage trait.** Both are player-namespaced → both are the
    SAFE mechanism. **Never gate on a raw cross-NPC trait** (`subject="npc", npc_id="npc_OTHER"` from a
    foreign canvas is unverified — see below); mirror it to the player namespace at the source arc instead.
- **F2a gate:** ordinary `money` gates + the income beats `13` designs. No new mechanism.
- **F2b banded payout:** **one band-gated sibling CHOICE per band**, each with its own `conditions` (the
  band) + its own literal-int money `effects` — the existing tiered-choice schema (`schema/02` §7.4 /
  `COMPREHENSIVE_SYSTEM_REFERENCE.md` §7.4). Band on the **host** NPC's own trait (verified — the Sal
  arousal group-blocks at `games/last_call/toml_phases/5_scenes.toml:173-176` read the canvas's own NPC),
  OR — for a solo/foreign-host work canvas — **mirror** the source NPC's corruption onto a player trait/flag
  at the source arc and band on `{ subject = "player" }`. **Forbidden until a shipped example exists:**
  relying on `{ subject = "npc", npc_id = "npc_OTHER" }` from a *different* NPC's canvas. F2b is the
  flourish; the spine (F2a) never touches the unverified path.

**No new ledger field.** The machine is *designed* in `design_book.md ## The machine` (prose) and
*enforced* by ordinary beat `deps` (`ledger-schema.md`) on the gated rung's beat + the existing `cross_npc`
/ `economic` beat types. **Do NOT add a `cross_wires` schema field** — that re-introduces the bookkeeping
diagram decision 7 correctly killed. The ledger stays a flat plan.

**Incremental authoring (one NPC at a time, Step 4) is preserved.** Because all coordination is on
player-namespaced flags/stage-traits, arc A can be authored fully before B exists — A just READS a flag B
will later SET; an unset flag is simply a locked rung (correct cold-start). Only the machine's *shape* is
fixed up front (the core loop + who's a node); the arcs still build one at a time into it.

---

## How the layer lands across the pipeline
- **Step 2** (`step-2-toplevel.md` §7): design the **core loop** + the two forms + the three disciplines.
- **Step 3 casting** (`06`): each *core* NPC gets a **place in the machine** (income node / gate / consumer)
  alongside role+hook+sketch.
- **Step 4 NPC arcs** (`07`): the R7 brief's **§8 becomes the arc's wiring contract** — the player flags /
  stage-traits this arc SETS and READS, under D1–D3.
- **Step 5 roster** (`18`): the self-check **verifies the machine** — core loop designed, every core NPC
  placed, **DAG (D2)**, every cross-gate telegraphed (D3). A real check, not a token "≥1 link."
- **Step 6 authoring** (`beat-authoring.md`): the `cross_npc` / `economic` beats carry the F1 gate recipe +
  the F2b banded-choice recipe + the D3 telegraph.

---

## Self-check
- The **core loop** is designed (conquest → money/access → next conquest); every core NPC has a **place** in it.
- Cross-wires are **F1 (arc→arc depth gate)** and/or **F2 (arc↔economy circulation)** — not Form 3 (that's G6).
- **D1:** no wire gates an arc's ENTRY — only mid/late rungs (every arc cold-start-enterable).
- **D2:** the F1 wires form a **DAG** — no cycle; every node cold-start-reachable.
- **D3:** every cross-gate ships a **locked-visible telegraph naming the other arc's state** (= `14` L7).
- F1 gates read a **player flag** (milestone) or **`<npc>_stage` player trait** ("how far"); never a raw
  cross-NPC trait. F2b uses **band-gated sibling choices** on the host-NPC trait or a player mirror.
- **No `cross_wires` ledger field** — ordinary beat `deps` + `cross_npc`/`economic` beat types carry it.
- Form 2b reads as "the corruption you wanted anyway *also* pays better," never grind-for-money (`09` R4).

## Cross-references
- `21` §3 (the field evidence — cross-wiring as the depth driver) · `04` cascade (the cold-start law D1
  preserves) · `09` desire ladder (every wire serves a want) · `13` economy (F2a is its connective-tissue
  extension) · `14` L7 (the D3 legibility seam, = G1) · `17` frontier (the steady-state the machine idles
  into) · `06`/`07`/`18` (the pipeline touch-points) · `20` decision 7 (refined — the web returns as the
  spine). **Deferred: G6** (Form 3 / compounding conquest — finished arcs become capability).
