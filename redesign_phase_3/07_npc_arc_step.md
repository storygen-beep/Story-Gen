# Step 4 — NPC arcs: expand each cast row into a playable arc

Takes one **cast row** (role · hook · fantasy lane · depth · arc-shape, from casting `06`) and expands
it into a full, playable arc: the personal trait (the lock), the escalation rungs **wired to the cascade
double-lock**, the lanes/scenes, voice, vocab ceiling, capstones, and — for core NPCs — the repeatable
loop. Answerable to the good-game qualities (`05`).

**This step is mostly ORCHESTRATION, not new doctrine.** The existing author-game skill already holds
the per-NPC apparatus; Step 4 *seeds it from the hook* and *binds it to the cascade*. What it reuses:

| Need | Reuse (existing skill) |
|---|---|
| which trait drives this arc (spine, by arc-shape) | `references/trait-design.md` — the spine table + throttle/odometer + per-NPC odometer + dead-meter/split-spine + slow-burn pacing |
| the per-NPC profile template | `setup-interview.md` Step 3 — the **R7 brief** (10 sections) |
| lanes, budgets, locked-visible rungs, hub-vs-solo, voice register | `references/lanes.md` |
| the repeatable explicit layer | `references/sex-loop.md` |
| per-NPC explicitness | `doctrine/08` (via `references/systems.md`) |

**Pipeline position:** step 4 — after casting (`06`), before the content roster (`05` feeders + scene
list). One NPC at a time.

---

## §1 — Inputs
- The **cast row** from `06`: role · hook (charged dynamic + want) · fantasy lane · **depth** (core vs
  peripheral) · arc-shape.
- The **cascade / engine** (`04`): the MC-corruption **door tiers** (flirt/grope/sex), the stat set.
- The **good-game qualities** (`05`): the bar every arc is checked against.

---

## §2 — Output per NPC = the R7 brief (reused), reframed
Author the existing 10-section R7 brief, but seeded and bound as follows:

- **§1 End-state fantasy = EXPAND THE HOOK.** The casting hook is the seed; the end-state is where it
  lands. (e.g. hook "loyal best friend who's wanted you for years and hates himself" → end-state "he
  stops hating himself and becomes yours, guilt traded for devotion.")
- **§2 Voice** = the hook's character. RTS-flat for lanes 1/2/3, Tier-3 earned in capstones (`lanes.md`).
- **§3 Stat ladder + spine** = pick the personal trait **by arc-shape** (`trait-design.md` table) at the
  **depth casting assigned**:
  - **core** → the rich two-meter model: the NPC's own `corruption` (odometer) + `arousal` (throttle).
  - **peripheral** → LIGHT: one odometer (`relation`/`money`) + flags + the player-corruption floor.
    No own arousal throttle, no own corruption odometer (P5 — gold-plating a peripheral is the failure).
- **§4 per-rung pretext + §5 lane map** = the lanes + the arc-shape's lane budget (`lanes.md`); empty
  cells stay empty (peer/dating → no Lane 3; service → no Lane 2/3).
- **§6 Capstones** = the one-shot milestones, gated on **odometer + flags** — NEVER the throttle.
- **Repeatable loop** (`sex-loop.md`) = **core NPCs only**, opens past the first-night flag.
- **Ceiling** = the hook's charge, delivered at the NPC's `doctrine/08` ceiling (default most-explicit).

---

## §3 — The genuinely-new bindings (what Step 4 adds)

**1. Hook → arc (the character drives the design).**
The hook seeds §1 + §2, and the NPC's **want** (from the hook) gives them **agency across the arc** —
they pursue, resist, scheme, set conditions; they are NOT a yes-man whose only state is your meters.
This is good-game quality #5 (desirable characters): the player chases a *person*, not a shape.

**2. The DOUBLE LOCK on every lewd rung (`04 §3`, made explicit + universal).**
Each lewd rung gates on BOTH:
- (a) the **MC-corruption tier** = the *door* — the same cascade tiers across the whole cast (built by
  the player's self-corruption feeders), and
- (b) the **NPC's own personal trait** = the *lock* — built by interacting with THIS NPC.

**Non-lewd interaction (talk, befriend, build trust) is NOT corruption-gated** — it's how you raise the
NPC's lock during Act 1, in parallel with corrupting yourself (`04 §4`). The two converge: when your
corruption opens the door, the NPCs you invested in are already unlocked.
*(This formalizes trait-design's existing rule — "the NPC's own axis gates rungs + player corruption is
the secondary floor on the most explicit beats" — as the universal cascade pattern.)*

**3. Depth is an INPUT from casting, not a re-decision.** Core → rich; peripheral → light. Don't
re-litigate it per NPC; casting (`06`) already set it for cast balance.

**3b. LATE-ACT arcs carry their OWN full pacing** (`15` Finding F). The double-lock has *two* gates only while
the MC-corruption door is still climbing (Act 1–2). By the late game that door is maxed/wide-open, so for a
late-introduced target (a recruit like Rosa) the door contributes **no** pacing — the lock collapses to the
NPC's own axis alone. So **late-act NPCs must be authored with a complete, self-contained rung ladder** (their
own slow-burn from cold to capstone); they cannot borrow tension from a rising MC door the way Act-1 targets do.
Build their pacing entirely into their own lock. (This is the per-NPC face of the endgame-stays-carnal rule — `14` P7 / `13` E9: a recruit is a full arc.)

**3c. The arc's WIRING CONTRACT — its place in the machine (`22`).**
Casting (`06`) gave each core NPC a **place in the machine** (its node in the core loop). Step 4 makes it
concrete: the R7 brief's **§8 is the arc's wiring contract** — the player-namespaced signals this arc
**SETS** (the milestone flags / `<this_npc>_stage` other arcs will read — e.g. Sal's first-night sets
`sal_opened_up`; taking the bar sets `bar_seized`) and the ones it **READS** (another arc's flag/stage that
gates one of *this* arc's mid/late rungs). Bound by the three disciplines (`22`):
- **D1 — never gate this arc's ENTRY on another arc.** A cross-read may gate a mid/late rung or a capstone,
  **never the on-ramp/first meeting.** The arc must stay enterable cold (the non-lewd on-ramp is ungated —
  §3.2). This is the cold-start firewall (`04 §4`) and what keeps the cast acyclic.
- **D2 — no cycle.** A cross-read points at a flag/stage *another* arc sets; never wire two arcs to mutually
  gate each other's depth (the roster `18` runs the DAG check).
- **D3 — legible.** Every cross-gated rung ships a **locked-visible telegraph naming the other arc's state**
  ("Sal won't cross that line while the bar's still in jeopardy" — naming `bar_seized`). An invisible
  cross-gate is a soft-lock (`14` L7 / `22` D3).
- **Mechanism:** milestone → a shared **player flag**; "how far along" → the **`<npc>_stage` player trait**;
  a wage/price **banded** by an NPC's trait → **band-gated sibling choices** (`22` realization). Never a raw
  cross-NPC trait read. Record SETS/READS in §8 so Step 5 can trace the wires and Step 6 can author them as
  `cross_npc` / `economic` beats with ordinary `deps`. (Scope: forms 1+2; a *finished* arc producing income/
  capability is **G6**, deferred.)

**4. Hold each NPC to the good-game qualities (`05`):**
- **Legible pull (#2):** ship the escalation rungs **locked-visible** so the player sees the ladder ahead.
- **Payoff (#4):** the capstones LAND (Tier-3 prose, the moment earned).
- **The charge (#7):** the ceiling honored at the peaks — no soft-pedaling.
- **Reactive (#8):** the NPC's lock-state visibly changes how they treat you (prose shifts with the odometer; heat-framed prose shifts with the throttle — `trait-design.md`).

---

## §4 — The per-NPC self-check (reuse + new)
- **Spine appropriate to arc-shape** (`trait-design.md`) — not `relation`-on-everything NOR
  player-`corruption`-on-everything; **no dead meter / split spine.**
- **Double lock present on lewd rungs** (MC corruption door + NPC's own lock); **non-lewd ungated.**
- **Late-act target?** then a **complete self-contained rung ladder** — it can't borrow pacing from the (now-maxed) MC door (`15` F / §3b).
- **Depth matches casting** — core rich / peripheral light; no gold-plating (P5).
- **The hook is visible** in the arc — voice + the NPC's want + real agency (resists/schemes).
- **Legible-pull rungs** (locked-visible) + **capstone payoff** + **ceiling honored** (good-game `05`).
- **Throttle off capstones**; **sex-loop core-only**; lanes sized to the arc-shape budget.
- **Wiring contract written** (`22`/§3c): §8 records the player flags / `<npc>_stage` this arc SETS and
  READS; every cross-**read** gates a mid/late rung (D1 — never entry), points at another arc (D2 — no
  cycle), and ships a locked-visible telegraph naming that arc's state (D3 — `14` L7). Never a raw cross-NPC
  trait read.
- **Traits declared before use** (`doctrine/09` / `toml-gotchas.md`).

---

## §5 — Worked example (the bar game)

**Sal — core target.** Hook: *"your late partner's loyal best friend, who's wanted you for years and
hates himself for it."*
- arc-shape = slow-burn → **rich two-meter**: `npc_sal.corruption` (odometer) + `npc_sal.arousal` (throttle).
- §1 end-state expands the hook (guilt → devotion).
- Act 1: you talk/serve Sal (ungated) → builds his lock; meanwhile you corrupt yourself (feeders) → the door.
- Act 2 lewd rungs **double-locked**: "flirt" needs MC corruption tier-1 AND `npc_sal.corruption ≥ N`
  (built by flirting/serving him); deeper rungs raise both tiers.
- Capstone (first night) = odometer + flags (MC `corruption ≥ 30` AND `npc_sal.corruption ≥ 5` + the chain), never the throttle.
- Repeatable loop opens after, gated by his `arousal` throttle.

**Marcus — peripheral target.** Hook: *"smooth regular, easy transactional heat."*
- arc-shape = dating/transactional → **light**: one odometer (`relation`) + flags + player-corruption floor.
- No own arousal throttle, no repeatable loop, one capstone. Lanes sized small (peer → no Lane 3).

Both pass the anti-LC test: a one-line hook, a clear next-thing-to-want (telegraphed rungs), a
shape-appropriate non-dead spine.

---

## §6 — Reconciliation note (for implementation, later — not now)
The existing `setup-interview.md` Step 3 authored R7 briefs *at setup*. The new pipeline **relocates**
that work to Step 4 (post-casting), **seeds** it from the hook, and **binds** it to the cascade.
`trait-design.md` / `lanes.md` / `sex-loop.md` / `doctrine/08` are reused essentially unchanged; the R7
template gains a "seed = casting hook" line and §3 gains the double-lock wiring. Net-new doctrine is
small — mostly relocation + the two bindings (hook→arc, double-lock).

## Cross-references
- `06_casting_roles_step.md` — supplies the cast row (role/hook/depth/arc-shape + place in the machine).
- `04_progression_engine.md` — the cascade + double lock (§3/§4) this step wires each NPC into.
- `22_the_machine_interconnection.md` — the cross-wiring layer; §8 of the brief is the arc's wiring contract (§3c).
- `05_what_makes_a_good_game.md` — the qualities each arc is checked against.
- Reused skill refs: `trait-design.md`, `lanes.md`, `sex-loop.md`, `setup-interview.md` (R7 brief), `doctrine/08`.
- Feeds Step 5 (content roster) — each NPC's rungs/scenes become roster rows.
