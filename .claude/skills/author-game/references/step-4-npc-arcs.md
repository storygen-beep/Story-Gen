# Step 4 — NPC arcs: expand each cast row into a playable arc (ONE NPC at a time)

Takes one **cast row** (role · hook · fantasy lane · depth · arc-shape · rough sketch, from Step 3) and
expands it into a full playable arc: the personal trait (the lock), the escalation rungs **wired to the
cascade double-lock**, the lanes/scenes, voice, vocab ceiling, capstones, and — for core NPCs — the
repeatable loop. Answerable to the 8 qualities (Step 0).

**One NPC per increment.** Surface the brief (Mode A for *core* NPCs, Mode B for peripherals), get it
okayed, then move to the next. Never author the whole cast's arcs in one pass — this is the heart of
incremental authoring and the per-increment quality gate a one-shot can't have.

**This step is mostly ORCHESTRATION, not new doctrine** — the existing library already holds the per-NPC
apparatus; Step 4 *seeds it from the hook* and *binds it to the cascade.* Reuse, don't reinvent:

| Need | Reuse |
|---|---|
| which trait drives this arc (spine, by arc-shape) | `references/trait-design.md` (spine table + throttle/odometer + per-NPC odometer + dead-meter/split-spine + slow-burn pacing) |
| lanes, budgets, locked-visible rungs, hub-vs-solo, voice register | `references/lanes.md` |
| the repeatable explicit layer | `references/sex-loop.md` |
| per-NPC explicitness ceiling | `doctrine/08` (via `references/systems.md`) |

Source: `redesign_phase_3/07`. Output: one **Per-NPC R7 brief** per NPC in `design_book.md`.

---

## Inputs
The **cast row** from Step 3 (role · hook · fantasy lane · depth · arc-shape · sketch); the **cascade**
(Step 2 — the MC-corruption door tiers, the stat set); the **8 qualities** (Step 0 — the bar each arc is
checked against).

## The output per NPC = the R7 brief, seeded + bound
Author the **10-section R7 brief** below (the corpus's core per-NPC deliverable). A *partial* brief is the
failure mode — the continue loop re-derives what's missing and drifts. The load-bearing sections are
flagged. Sections, with the Step-4 seeding/binding noted:

1. **End-state fantasy** (one paragraph) — the complete arc's destination. **= EXPAND THE HOOK** (the
   casting hook + rough sketch are the seed; the end-state is where they land). **Gates everything
   downstream; author it FIRST** (without it the locked-visible rungs have nothing to telegraph).
2. **Voice spec** — how this NPC sounds (from the hook's character). RTS-flat register for Lane 1/2/3;
   Tier-3 earned only in capstones (`references/lanes.md`).
3. **Stat ladder + gating spine** — stage flags + per-rung thresholds, AND the **spine** trait by arc-shape
   at the **depth casting assigned**:
   - **core** → the rich two-meter model: the NPC's own `corruption` (odometer) + `arousal` (throttle).
   - **peripheral** → LIGHT: one odometer (`relation`/`money`) + flags + the player-corruption floor. No
     own arousal throttle, no own corruption odometer (gold-plating a peripheral is the failure — P5).
   Pick the spine by shape (peer → `relation`; family/slow-burn/escalation → NPC `corruption` odometer +
   `arousal` throttle, player `corruption` secondary floor; leverage → `money`; service → `relation`; never
   default to `relation`, never make player `corruption` the universal spine — `references/trait-design.md`).
   Note the **throttle/odometer split**: odometers (permanent: `corruption`/`relation`) gate rungs AND
   one-shot capstones; the throttle (`arousal`, resets at climax) gates the **repeatable** loop, never a
   capstone. Per-tier **vocab ceiling** here too (`doctrine/08`, default-to-maximum-explicit).
4. **Per-rung pretext shapes** — the in-fiction setup menu for each ladder rung (the content menu).
5. **Lane-by-lane map** — the budget compiled into specific canvas slots per location/window (empty cells
   stay empty: peer/dating → no Lane 3; service → no Lane 2/3).
6. **Capstones** — each scripted moment: type A/B/C + trigger + **the odometer threshold it gates on**
   (`corruption`/`relation` + flags — NEVER the `arousal` throttle) + the flag it writes (Pattern F F1–F5
   for forks). Committing the gate here (not just the flag) keeps the capstone on the same odometer the hub
   builds. **Commit these up front** so capstone beats are authorable later.
7. **Per-NPC anti-patterns** — what NOT to do for this NPC (e.g. empty Lane 3 for peer/dating).
8. **Cross-arc writes / reads** — flags this NPC's scenes set + flags they read from other arcs (this is
   where the **rough sketch's cross-NPC threads** become concrete).
9–10. **Cross-references + acceptance criteria** — the arc's "done" check.

The per-beat loop (Step 6) reads this instead of re-deriving voice / ceiling / ladder / capstone intent.

## The genuinely-new bindings (what Step 4 adds over the reused library)
1. **Hook → arc.** The hook seeds §1 + §2, and the NPC's **want** (from the hook) gives them **agency** —
   they pursue, resist, scheme, set conditions; NOT a yes-man whose only state is your meters (quality #5).
2. **The DOUBLE LOCK on every lewd rung** (`redesign_phase_3/04`, made explicit + universal). Each lewd rung
   gates on BOTH (a) the **MC-corruption tier** = the door (same cascade tiers across the cast, built by the
   player's feeders), AND (b) the **NPC's own personal trait** = the lock (built by interacting with THIS
   NPC). **Non-lewd interaction (talk, befriend, build trust) is NOT corruption-gated** — it raises the
   lock in Act 1. (This formalizes trait-design's "NPC's own axis gates rungs + player corruption is the
   secondary floor on the most explicit beats" as the universal cascade pattern.)
3. **Depth is an INPUT from casting**, not a re-decision. Core → rich; peripheral → light. Don't re-litigate.
4. **Late-act own pacing.** The double-lock has *two* gates only while the MC door is still climbing
   (Acts 1–2). By the late game that door is maxed, so a **late-introduced** target (a recruit) gets **no**
   pacing from the door — its lock collapses to the NPC's own axis. So **late-act NPCs carry a complete,
   self-contained rung ladder** (their own cold-to-capstone burn); they can't borrow tension from a rising
   MC door. (This is the per-NPC face of the endgame-stays-carnal rule — a recruit is a full arc.)
5. **Hold each NPC to the 8 qualities:** legible pull (locked-visible rungs telegraph the ladder), payoff
   (capstones land — Tier-3), the charge (ceiling honored, no soft-pedaling at peaks), reactive (lock-state
   visibly changes how they treat you — odometer shifts prose; throttle shifts heat-framed prose).

## The repeatable loop (core NPCs only)
Past the first-night capstone flag, a core NPC's arc opens its **repeatable sex-loop menu**
(`references/sex-loop.md`) — gated by its `arousal` throttle. Peripheral/service/antagonist NPCs do NOT get one.

## Per-NPC self-check (reuse + new)
- **Spine appropriate to arc-shape** (`trait-design.md`); **no dead meter / split spine.**
- **Double lock present on lewd rungs** (MC corruption door + NPC's own lock); **non-lewd ungated.**
- **Late-act target?** → a **complete self-contained rung ladder** (can't borrow the maxed MC door).
- **Depth matches casting** — core rich / peripheral light; no gold-plating.
- **The hook is visible** in the arc — voice + the NPC's want + real agency (resists/schemes).
- **Legible-pull rungs** (locked-visible) + **capstone payoff** + **ceiling honored**.
- **Throttle off capstones**; **sex-loop core-only**; lanes sized to the arc-shape budget.
- **Traits declared before use** (`doctrine/09` / `references/toml-gotchas.md`).

## Worked example (bar game)
**Sal — core.** Hook: *"your late partner's loyal best friend who's wanted you for years and hates himself."*
slow-burn → rich two-meter (`npc_sal.corruption` odometer + `npc_sal.arousal` throttle); §1 expands the hook
(guilt → devotion); Act 1 you talk/serve Sal (ungated) → builds his lock, while you corrupt yourself → the
door; Act 2 lewd rungs **double-locked** ("flirt" = MC corr tier-1 AND `npc_sal.corruption ≥ N`); first-night
capstone = odometer + flags (MC `corruption ≥ 30` AND `npc_sal.corruption ≥ 5` + chain), never the throttle;
repeatable loop opens after, gated by his `arousal`.
**Marcus — peripheral.** Hook: *"smooth regular, easy transactional heat."* dating → **light**: one odometer
(`relation`) + flags + player-corruption floor; no own throttle, no loop, one capstone; peer → no Lane 3.

## Cross-references
`redesign_phase_3/07` · `references/trait-design.md` / `lanes.md` / `sex-loop.md` / `doctrine/08` (reused) ·
Step 5 = `references/step-5-roster.md` (each NPC's rungs/scenes become roster rows). Set `pipeline_phase =
"roster"` when the whole cast's briefs are done.
