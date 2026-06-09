# Step 6 — authoring: reconcile the existing engine to the new pipeline

The last design piece. **Step 6 is where scenes get written and turned into a working game** — the "how."
The headline finding from reading the actual skill (`SKILL.md` + `references/beat-authoring.md`): **Step 6
mostly already exists and already aligns.** It needs *reconciling*, not rebuilding. That confirms the whole
thesis of Phase 3 — the HOW layer was always solid; LC/LS were soulless from upstream failures (no fantasy,
no desire, thin content), not from bad authoring mechanics. **Spec-on-paper; skill edits happen at wiring
time (`16`).**

---

## What already exists AND already aligns (reuse as-is)
The skill's **continue mode** (`beat-authoring.md`) already does, almost verbatim, what `16` asks for:

| `16` / Phase-3 principle | Already in the skill |
|---|---|
| **Incremental, build-green per increment** (`16`) | "Author exactly one beat per turn, validate it, then stop." + per-beat validation (merge `--validate` → `package_from_toml` → doctrine self-audit). **This IS the increment + build-green.** |
| **Design book is the input/review surface** (`16`) | The beat loop reads `design_book.md` (roster, R7 briefs, roadmap) and *fills a roster row, never improvises one*. `7_final_game.toml` is generated, never hand-edited. |
| **Ask with options + recommendation** (`16` Mode A) | "Ask ONE question at a time via AskUserQuestion — 2–4 options + a recommendation. Never a blank prompt." |
| **No silent drift** (`16` grounded) | Resume-and-reconcile against the ledger every turn; the anti-drift invariant; "only offer real engine knobs." |
| **Whole, not dangling** (structure) | Structure amendments done WHOLE (location → def+lock+schedule+unlock; NPC → schedule+on-ramp; flag → reachable setter). |
| **The doctrine self-audit** | A deep per-beat checklist (reachability triad, presence floor, double-lock-as-"two-axis", feeder economy, vocab ceiling, trait spine, costs-gating, locked-render…). The build-green safety net. |

**So the reconcile is a set of targeted DELTAS, not a rewrite.** Everything above stays.

---

## The deltas to apply (at wiring — listed precisely so it's mechanical)

### D1 — Drop slice scope (`scope_mode`) everywhere
Scope is **always full game** (slice removed). Reconcile every `scope_mode`/`slice` reference:
- `SKILL.md` operating rule "`scope_mode` (full_game | slice) governs scale" → remove the slice branch; scope is full game; size arcs to the per-NPC budget + the **frontier** (`17`), not to a slice.
- `beat-authoring.md` §4 "size to the brief's budget AND `scope_mode`" → drop the slice sizing.
- The **contraception scope-conditional** rule (self-audit, `stages/02` §10.11): it branched on `slice` vs `full_game+pregnancy`. With slice gone it collapses to the **`pregnancy = defer | include`** axis only (defer → bareback, no contraception language; include → contraception language allowed pre-pregnancy, banned post-). *The `pregnancy` Phase-2 axis stays; only the `slice` arm is removed.*
- The roster method (`18`, was `content-design.md` step 4) "size to `scope_mode`" → full game; venue columns are *filled*.
- `ledger-schema.md` — remove the `scope_mode` field, but **KEEP the `npcs` budget block** (`arc_shape` / `lane_budget` / `vocab_ceiling`) — independent of slice, still load-bearing.
- `setup-interview.md` — delete **Step 1.5** (the whole "determine scope mode" step) + the slice arms in Step 2 item 5 / Step 3 / Step 5; `lanes.md` — drop the "~30–50% at slice" sizing paragraph.
- *(Full 7-file touch-list + the keep-`npcs` note: `20` decision 1.)*

### D2 — Point at the re-homed roster (`18`), not the old `content-design.md`
The beat loop's "a beat fills a `## Content roster` row" now reads **doc 18's** roster — which carries the new
columns: **`want`** (the desire-ladder rung, `09`), **`track` incl. `reactive`**, **`mode`** (sought/choice/
forced for reactive rows, `11`), and the **double-lock `gate`** (`07`). Pull those, don't improvise.

### D3 — Every beat serves a WANT (the desire-ladder binding, `09`)
The beat-proposal step (`beat-authoring.md` loop §1) currently takes "the head of `next_up`." Reconcile: it
takes **the current want on the desire ladder** (`09`) and frames the beat as *pursuing that want* (R1/R7) —
never "an activity that raises a meter." Add to the self-audit: **per beat, name the want it serves; none →
grind, cut or reframe (`09` R4).** This is the single most important behavioral delta — it's what stops the
beat loop from re-creating LC's meter-grind.

### D4 — Add the new doctrine to the per-beat self-audit
The self-audit is the right home for each new rule (it's already the build-green gate). Add:
- **Reactive-world beats (archetype 10, `11`):** a clothing-triggered beat gates on **outfit exposure × place
  ceiling × NPC disposition**, NOT cascade meters; ships the right **mode** (sought/choice/forced); **forced is
  act-scoped** (`11`/`15` D) — present in the fall, retired above a power tier.
  - **REFINE the existing clothing rule, don't just add (`20` decision 2).** The skill's absolute
    *"clothing gates PUBLIC content, NEVER an NPC arc"* (in `systems.md` + this self-audit) would otherwise
    **reject every reactive event**. Rewrite it to two parts: clothing **MAY trigger ambient, in-character
    reactive events** (Lane 2/3); clothing **must NOT gate an NPC's escalation spine / arc-progression** (the
    `worn_corruption`-gates-a-housemate's-arc case stays banned — still the backwards on-ramp). This is the
    carve-out without which D4's reactive-world line fights the existing clothing line.
- **Double-lock made explicit (`07`/`04`):** the skill's "two-axis core gate" *is* the double lock — align the
  vocabulary and make it universal: every NPC **lewd** rung gates on the **player-corruption door + that NPC's
  own lock**; **non-lewd interaction is ungated** (builds the lock in Act 1).
- **Frontier (`17`):** beats beyond the **current frontier** are authored as **telegraphed locked-visible
  seeds**, never silent gaps (open-topped roster); the **frontier beat does its three jobs** (payoff · drop into
  steady-state · greyed next-hook); the **quest card narrates the frontier honestly** (`14` L6) — never blank.
- **Endgame stays carnal (`14` P7 / `13` E9):** a late/empire beat **cashes out as content** — a recruit is a
  **full arc** (its own `07` brief + double-lock + capstone), an "upgrade" unlocks **new scene types**, the apex
  is the hottest beats. **Never** model a recruit as a `+income` widget or an upgrade as a stat bump.
- **Escalating pressure (`13` E8):** support a **late-act pressure beat** (rival/cop/boss) so the squeeze
  doesn't die when the empire earns; gate late leverage content on it.
- **Late-act own pacing (`07` §3b):** a **late-introduced** NPC carries a **complete self-contained rung
  ladder** — it can't borrow pacing from the (now-maxed) player-corruption door.
- **Conquest-desire (`09` R6 / `05` #5):** a conquest-target beat reads as **wanted-as-conquest** (hot pursuit +
  the target has agency: resists/schemes/cracks) — not a cold instrument you merely *use*.

### D5 — Calibrate ask-vs-inform (`16` Modes A/B) to avoid death-by-questions
The skill asks AskUserQuestion **every** beat. Across a *full game's* worth of beats that's too many gates.
Reconcile to `16`'s split: **Mode A (AskUserQuestion)** for a **genuine fork** (how to play a charged beat, a
real branch, a frontier/identity call); **Mode B (skimmable inform-and-proceed)** for a routine roster row
that's already specified (just build it, tell the user in one line, let them interrupt). *Ask the crucial,
inform the rest* — the existing "options + recommendation" shape is kept for the Mode-A gates.

### D6 — Bounce engine-forced changes UP to the design book (`16`)
Already mostly true (TOML is generated). Make explicit: if an engine limit/gotcha forces a design change, it
**updates `design_book.md`** (the review surface) and is surfaced to the user — it is **not** silently patched
into the TOML. The design book stays the source of truth the user reviews.

### D7 — Phase-aware dispatch (the ledger is born at setup) (`20` decision 4)
The skill's mode dispatch currently branches on *"does `authoring_state.json` exist?"* → setup vs continue.
With the **ledger created at setup** (`01` / `20` decision 4) the file always exists, so that check breaks.
Reconcile the dispatch (`SKILL.md`) to **read the ledger's `pipeline_phase` field** — phase-aware across all
7 steps, not a binary. Resume = read the phase, continue the next unfilled piece. (Step 6 itself is reached
when the phase says authoring; the structure/plan parts of the ledger are empty until then.) Add the
`pipeline_phase` field to `ledger-schema.md`.

---

## What stays exactly as-is (do NOT touch)
- The per-beat **validation + doctrine self-audit** pipeline (merge `--validate` → `package_from_toml` →
  audit) — the build-green engine.
- The **ledger** + resume-and-reconcile **anti-drift** discipline (the *anti-drift* logic is unchanged; only
  the dispatch trigger + the new `pipeline_phase` field are added — D7).
- The **TOML phase-file mapping**, `toml-gotchas.md`, the merge + `package_from_toml` build, quest-card schema.
- `lanes.md` / `trait-design.md` / `sex-loop.md` / `systems.md` / `doctrine/08` — reused unchanged.

---

## Self-check (the reconciled Step 6)
- One beat per turn → **validate → stop** (build-green) — *unchanged, already aligned.*
- The beat **fills a roster row from `18`** (with `want`/`mode`/double-lock gate) — never improvises.
- **Every beat names the want it serves** (`09` R4) — no meter-grind beats.
- **No `scope_mode`/slice** anywhere — full game, sized to budgets + the frontier.
- The self-audit now covers **reactive world, double-lock, frontier, endgame-carnal, escalating pressure,
  late-act pacing, conquest-desire** (D4).
- **Ask crucial / inform routine** (`16` D5) — not a question every beat.
- Engine-forced changes **bounce up to the design book** (D6), never silent TOML patches.
- All prior build-green doctrine (reachability, presence floor, ceiling, spine, costs, locked-render) intact.

## Cross-references
- `16` run-mode (the discipline this aligns the authoring engine to) · `18` the roster it builds from ·
  `09` desire ladder (every beat a want) · `07`/`04` double-lock + late-pacing · `11`/`15` reactive world +
  act-scoped forced · `13` economy (E8/E9) · `14` P7 + L6 · `17` frontier · `05` conquest-desire.
- Existing skill (reconciled at wiring, not now): `SKILL.md`, `references/beat-authoring.md`,
  `references/content-design.md` (→ superseded by `18`), `lanes.md`, `trait-design.md`, `systems.md`,
  `toml-gotchas.md`, the ledger + build scripts.
