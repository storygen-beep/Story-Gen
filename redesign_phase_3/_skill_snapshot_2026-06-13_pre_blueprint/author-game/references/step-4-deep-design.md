# Step 4 — deep-design: design each SUBJECT into a playable arc (ONE subject at a time)

Step 4 **GENERATES** the game's content by answering `references/content-framework.md`, **one subject at a
time**, in a fixed order:

**PLAYER (§2) → each NPC (§3, one each) → WORLD (§5) → REACTIVITY wiring (§4).**

The order is **supply → demand → stage**: the player's own feeder track (the *supply* of corruption) is sized
**before** the NPC arcs (the *demand* that gates on it), and the world (the *stage*) is dressed before the
reactivity pass wires everything together. This is the heart of incremental authoring — **never generate the
whole content in one pass.** Step 5 (`step-5-feedback.md`) then REVIEWS what this step generated, against the
same framework.

This replaces the old "Step 4 = NPC arcs only" — the per-NPC R7 brief survives intact as **Pass 2**; what's
new is that the **player** and the **world** are now first-class subjects (closing the player-track blind spot
at its source), and a final **reactivity** pass wires the machine.

## Inputs
The **cascade + economy + desire ladder + frontier** (Step 2 / framework §1), the **cast** (Step 3 — role ·
hook · lane · depth · arc-shape · sketch · place in the machine), the **8 qualities** (Step 0), and
**`references/content-framework.md`** — the question set this step answers (§2 for Pass 1, §3 for Pass 2, §5
for Pass 3, §4 for Pass 4).

## The ordering rule (enforced by the ledger)
The ledger's `deep_design` block tracks `{ player, npcs, world, reactivity }`. **Don't start `npcs` until
`player == "done"`; don't start `reactivity` until `npcs` and `world` are both done.** *Why:* you author the
player's feeder catalog first, so when an NPC's capstone needs `corruption ≥ 30` you can already see whether
the player can *get* to 30 through ordinary play — instead of discovering the starvation at review (the Last
Call failure). Reactivity is last because it can only wire content that already exists.

---

## Pass 1 — the PLAYER subject (§2 YOU) — FIRST, before any NPC
Answer **`content-framework.md` §2** against this game. Output: a **`### The player thread (Step 4 · §2)`**
block in `design_book.md`.
- **2A bootstrap** — the off-zero solo acts (ungated, `corruption 0`) + any behavior/story nudge.
- **2B exhibition backbone** — the being-seen ladder per venue/stage (the mid-tier workhorse).
- **2C the economy as CONTENT** — the income ladder (legit-low → lewd-high, better money always further down
  the lewd path), the wanted **sinks**, the **key items** the money buys (a teaching toy, an intoxicant, a
  held photo, a key), the broke-pressure. *(The economy ENGINE — one wallet, income-as-corruption-ladder — was
  set at Step 2 §4; here you author the actual scenes/items/sinks, NOT re-decide the shape.)*
- **2D the ceiling + other ladders** — the extreme-public top of HER own depravity; any non-corruption ladder
  (job rank / fame / faction / skill) walked start-to-top with what it ONLY unlocks.
- **2E the supply-vs-demand audit** — the OWNER of the feeder count. Seed it here; **close it at the end of
  Pass 2** once every NPC floor exists (count feeders band-by-band vs the floors the cast demands).

**Bridge:** solo-host canvases (Lane-3 *host* shape — `manual`, `is_repeatable`, `location`, no `npc`), player
`corruption`/`exhibitionism` odometers, the economy + clothing/rent systems (`lanes.md` Lane-3 player-lewd
amendment · `systems.md`). **Every feeder hangs on a WANT** (the desire ladder), never "raises corruption."
**Ledger:** set `deep_design.player = "done"` when the player block is complete.

---

## Pass 2 — each NPC (§3 THEM) — ONE NPC at a time
Takes one **cast row** and answers **`content-framework.md` §3** for that NPC: the full **10-section R7
brief** below. **One NPC per increment** — surface the brief (Mode A for *core*, Mode B for *peripheral*), get
it okayed, then the next. Never author the whole cast's arcs in one pass — this is the per-increment quality
gate a one-shot can't have. The **§3H "web between them"** is answered ONCE for the cast and **seeds Pass 4**.

This pass is mostly **ORCHESTRATION** — the library already holds the per-NPC apparatus; reuse, don't reinvent:

| Need | Reuse |
|---|---|
| which trait drives this arc (spine, by arc-shape) | `references/trait-design.md` |
| lanes, budgets, locked-visible rungs, hub-vs-solo, voice register | `references/lanes.md` |
| the repeatable explicit layer | `references/sex-loop.md` |
| per-NPC explicitness ceiling | `doctrine/08` (via `references/systems.md`) |

### The output per NPC = the R7 brief, seeded + bound
Author the **10-section R7 brief** (the corpus's core per-NPC deliverable). A *partial* brief is the failure
mode — the continue loop re-derives what's missing and drifts.

1. **End-state fantasy** (one paragraph) — the complete arc's destination. **= EXPAND THE HOOK.** Gates
   everything downstream; **author it FIRST** (without it the locked-visible rungs have nothing to telegraph).
2. **Voice spec** — how this NPC sounds (from the hook). RTS-flat for Lane 1/2/3; Tier-3 earned only in
   capstones (`references/lanes.md`).
3. **Stat ladder + gating spine** — stage flags + per-rung thresholds, AND the **spine** trait by arc-shape at
   the **depth casting assigned**: **core** → the rich two-meter model (NPC's own `corruption` odometer +
   `arousal` throttle); **peripheral** → LIGHT (one odometer `relation`/`money` + flags + the player-corruption
   floor; no own throttle/odometer — gold-plating a peripheral is the failure). Pick by shape (peer →
   `relation`; family/slow-burn/escalation → NPC `corruption` + `arousal`, player `corruption` secondary floor;
   leverage → `money`; service → `relation`; never default to `relation`, never make player `corruption` the
   universal spine). Throttle/odometer split: odometers gate rungs AND capstones; the `arousal` throttle gates
   the **repeatable loop**, never a capstone. Per-tier vocab ceiling here (`doctrine/08`, default-to-maximum).
4. **Per-rung pretext shapes** — the in-fiction setup menu for each ladder rung.
5. **Lane-by-lane map** — the budget compiled into specific canvas slots per location/window (empty cells stay
   empty: peer/dating → no Lane 3; service → no Lane 2/3).
6. **Capstones** — each scripted moment: type A/B/C + trigger + **the odometer threshold it gates on**
   (`corruption`/`relation` + flags — NEVER the `arousal` throttle) + the flag it writes (Pattern F F1–F5 for
   forks). **Commit these up front** so capstone beats are authorable later.
7. **Per-NPC anti-patterns** — what NOT to do for this NPC (e.g. empty Lane 3 for peer/dating).
8. **The wiring contract — this arc's place in the machine** (`redesign_phase_3/22`). Record the
   player-namespaced signals this arc **SETS** (the milestone flags / `<this_npc>_stage` other arcs read) and
   the ones it **READS** (another arc's flag/stage gating one of *this* arc's **mid/late** rungs). Bound by:
   **D1** never gate this arc's ENTRY on another arc (cross-read gates a mid/late rung, never the ungated
   on-ramp); **D2** the read points at *another* arc, never a mutual lock (the reactivity pass runs the DAG
   check); **D3** every cross-gated rung ships a **locked-visible telegraph naming the other arc's state**
   (`14` L7). Mechanism: milestone → a shared **player flag**; "how far" → the **`<npc>_stage` player trait**;
   a wage/price banded by a trait → **band-gated sibling choices** — never a raw cross-NPC trait read.
9–10. **Cross-references + acceptance criteria** — the arc's "done" check.

The per-beat loop (Step 6) reads this instead of re-deriving voice / ceiling / ladder / capstone intent.

### The genuinely-new bindings (what Pass 2 adds over the reused library)
1. **Hook → arc.** The hook seeds §1 + §2, and the NPC's **want** gives them **agency** — they pursue, resist,
   scheme, set conditions; NOT a yes-man whose only state is your meters (quality #5).
2. **The DOUBLE LOCK on every lewd rung** (`redesign_phase_3/04`). Each lewd rung gates on BOTH (a) the
   **MC-corruption tier** = the door (the same cascade tiers across the cast, built by the player's feeders —
   Pass 1), AND (b) the **NPC's own personal trait** = the lock (built by interacting with THIS NPC).
   **Non-lewd interaction (talk, befriend, build trust) is NOT corruption-gated** — it raises the lock in Act 1.
3. **Depth is an INPUT from casting**, not a re-decision. Core → rich; peripheral → light. Don't re-litigate.
4. **Late-act own pacing.** The double-lock has *two* gates only while the MC door is still climbing (Acts
   1–2). A **late-introduced** target gets **no** pacing from the maxed door, so it carries a **complete,
   self-contained rung ladder** (its own cold-to-capstone burn).
5. **Hold each NPC to the 8 qualities:** legible pull (locked-visible rungs telegraph the ladder), payoff
   (capstones land — Tier-3), the charge (ceiling honored), reactive (lock-state visibly shifts prose).
6. **The wiring contract (§8) is part of the brief** — seed it from the casting **place in the machine**.

### The repeatable loop (core NPCs only)
Past the first-night capstone flag, a core NPC's arc opens its **repeatable sex-loop menu**
(`references/sex-loop.md`) — gated by its `arousal` throttle. Peripheral/service/antagonist NPCs do NOT get one.

### Per-NPC self-check
- **Spine appropriate to arc-shape**; **no dead meter / split spine.** · **Double lock on lewd rungs**;
  **non-lewd ungated.** · **Late-act target?** → complete self-contained ladder. · **Depth matches casting**
  (no gold-plating). · **The hook is visible** (voice + want + real agency). · **Legible-pull rungs** +
  **capstone payoff** + **ceiling honored**. · **Throttle off capstones**; **sex-loop core-only**. ·
  **Wiring contract written** (§8: SETS/READS recorded; every cross-read gates a mid/late rung — D1; points at
  another arc — D2; telegraphed naming that arc's state — D3). · **Traits declared before use.**

### Worked example (bar game)
**Sal — core.** Hook: *"your late partner's loyal best friend who's wanted you for years and hates himself."*
slow-burn → rich two-meter (`npc_sal.corruption` odometer + `npc_sal.arousal` throttle); §1 expands the hook;
Act 1 you talk/serve Sal (ungated) → builds his lock, while you corrupt yourself on the floor (Pass 1) → the
door; Act 2 lewd rungs **double-locked**; first-night capstone = odometer + flags, never the throttle;
repeatable loop opens after. **Marcus — peripheral.** dating → **light**: one `relation` odometer + flags +
player-corruption floor; no own throttle, no loop, one capstone; peer → no Lane 3.

**Ledger:** `npcs.<id>` per NPC as before (arc_shape, lane_budget, vocab_ceiling). Set `deep_design.npcs =
"done"` when the whole cast's briefs are done, and **close the §2E supply-vs-demand audit** now that every floor
exists.

---

## Pass 3 — the WORLD subject (§5) — the stage
Answer **`content-framework.md` §5**. Output: a **`### The world (Step 4 · §5)`** block.
- **5A** each place's dramatic JOB ("this place exists so the player can ___") + which track lives there.
- **5B** the **per-place ceiling** — the OWNER of *where forced content is allowed* and how it act-scopes out.
- **5C** the reactive public + dispositions + the **downside outcomes** of risky exposure.
- **5D** who's-here-when (schedules); **5E** cadence + the pressure clock; **5F** the phone & sidebar
  (`systems.md`); **5G** access & travel + the locked-visible map.

This **registers locations/schedules into `structure_registry`**. The map's *creative geography* came at
setup; here you give each place its dramatic JOB + ceiling + clock. **Bridge:** place ceiling **author-encoded
in canvas `conditions`** (not a location attribute); clothing `worn_corruption` gates PUBLIC content only;
`[phone]` (flags + elapsed-days) + `[[sidebar_items]]` via `systems.md`. **Ledger:** `deep_design.world = "done"`.

---

## Pass 4 — the REACTIVITY wiring (§4) — LAST
Answer **`content-framework.md` §4**. This **invents no new content** — it WIRES the content Passes 1–3
created: walk every state-change (hers §4A, theirs §4B, outfit §4C, wallet/day/place/body §4D, the machine
§4E, **loses-ground §4F**) and confirm each set-point declared upstream is **READ** by something — upward AND
downward. **Completes the `## The machine` block** Step 2 seeded.
- Each wire = an ordinary `cross_npc`/`economic` beat with `deps` (no new schema), bound by **D1** (entry never
  gated), **D2** (no cycle — trace the F1 cross-reads as a DAG), **D3** (every cross-gate telegraphed).
- §4F (the negative axis) is where the Step-2 §1C fail-state declaration gets its *ripples* — if "no failure by
  design" was declared, record that here in one line.

**Ledger:** set `deep_design.reactivity = "done"`, then **set `pipeline_phase = "feedback"`.**

---

## Navigation (which subject / NPC next)
At each pass boundary, **propose the next move with options** (`run-mode.md` → "Navigation at junctions"). The
four-pass ORDER is fixed (supply→demand→stage), but *within* Pass 2 "which NPC next" and *at* boundaries "ready
to move from the player to the NPCs?" are real junctions — propose from the `deep_design` ledger block, don't
assume.

## Cross-references
`references/content-framework.md` (the question set this step answers) · `references/trait-design.md` /
`lanes.md` / `sex-loop.md` / `systems.md` (the reused library) · Step 2 = `references/step-2-toplevel.md`
(framework §1 + the inputs) · Step 5 = `references/step-5-feedback.md` (reviews this against the framework).
Set `pipeline_phase = "feedback"` when all four passes are `done`.
