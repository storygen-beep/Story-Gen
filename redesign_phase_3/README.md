# Redesign Phase 3 — author-game pipeline restructure

Ground-up restructure of the author-game skill's authoring pipeline. **Spec-on-paper first — skill
files are NOT being edited yet** (brainstorm/optimize mode).

## Files
- **`00_CONTEXT.md`** — the full context: how we got here, the core principle (what-before-how), the
  target 5-step pipeline, the decisions log (D1–D11), carry-over concepts, source pointers, what's next.
- **`01_STEP1_SETUP_LOCKED.md`** — Step 1 (Setup) fully locked: the bare creative seed, what's in,
  what moved out and where, rationale, interaction model, output.
- **`02_GAME_SURVEY_top_level.md`** — research for Step 2: top-level live-play survey of 10 games
  (drive / progression spine / day loop / world logic / story shape / endings) + cross-game patterns.
  Key finding: the progression spine is a MENU (corruption+arousal / love+lust / addiction / trust+corr /
  relationship+perks …), not just "corruption." Grounds the Top-level step design.
- **`03_secondary_traits_gating.md`** — study of HOW secondary stats gate content (RTS, Generic Porn
  Game, Gakko). The 6 gating PATTERNS (hard-tier / banded / leveled-tier / inverse-maintenance /
  action-cost / soft-modifier), the domain-separation rule, the dead-stat trap, and how this becomes a
  rulebook so Claude authors to explicit rules. Key: RTS is corruption-DOMINANT (secondary stats soft);
  real multi-stat gating lives in the portfolio games.
- **`04_progression_engine.md`** — the cascade design (Step-2 core, LOCKED): "corrupt yourself before
  you can corrupt others." The 3-act cascade, the DOUBLE LOCK (MC corruption door + NPC's own personal
  traits), two build-loops, the stat set (each leg one job), why it works. 2 sub-choices pending (§7).
- **`05_what_makes_a_good_game.md`** — THE HEAD of the pipeline (Step 0). Evidence-grounded: "good" =
  sustained, legible, rewarded DESIRE toward a juicy fantasy. **Step 0a (above all): POV gate (female PC =
  RTS-native; pick POV before the fantasy) + the 3-part good-fantasy bar (POV-fit · sharp charge · built-in
  two-act shape) — the dry-run fix.** Then the 8 qualities (sharp fantasy · legible pull · no grind ·
  reward drip+payoff · desirable characters · paced escalation · the charge · reactive coherent world) +
  the enemies checklist. Canonical example: the female-PC **bar→empire/madam** fantasy.
- **`06_casting_roles_step.md`** — Step 3 (Casting): every NPC earns its place — a ROLE (derived from
  the fantasy + cascade) + a HOOK (charged dynamic + want). The role taxonomy (structural: pressure
  source / corrupting on-ramp · desire: core+peripheral targets / gatekeeper · optional drama), the hook
  definition, the casting self-check (coverage/coherence/variety/no-roleless), output table. The answer
  to "no random NPCs."
- **`07_npc_arc_step.md`** — Step 4 (NPC arcs): expand each cast row into a playable arc. An
  ORCHESTRATION step that REUSES the existing skill (trait-design / lanes / sex-loop / R7 brief /
  doctrine-08), seeded from the casting HOOK and bound to the cascade's DOUBLE LOCK (MC-corruption door +
  NPC's own lock; non-lewd ungated). Depth (core/peripheral) is an input from casting; held to the
  good-game qualities. Small net-new doctrine (mostly relocation + two bindings).

- **`08_dry_run_estate.md`** — paper dry-run of a fresh game ("The Estate") through Step 0→4 + brutal
  critique. Verdict: front-end HOLDS and beats LC (fantasy + hooks + double-lock create desire). But
  exposes gaps that map to the undesigned rest of Step 2: (1) cascade must be DESIRE-driven not
  meter-driven [deepest], (2) reactivity/acknowledgement layer has no owner, (3) legibility/objective
  thread has no owner, (4) pacing curve undesigned, (5) economy needs anti-grind multi-paths.
- **`09_desire_driven_progression.md`** — the FIX for Gap 1 (deepest). The cascade re-expressed as a
  DESIRE LADDER (a chain of escalating named WANTS), not a corruption bar with content at thresholds.
  Rules R1-R7 (every gain serves a named want; meter backstage; ban the meter-exercise; want-completion =
  tier-cross = payoff; per-NPC arcs are wants; feeders desire-framed). Bonus: this also SEEDS Gap 3
  (the visible want = the legible objective thread) and Gap 4 (chase→clear→new want = the pacing rhythm).
  Worked: the bar→empire desire ladder.
- **`10_reactive_world_research.md`** — research for Gap 2 (reactive world). How the games do it: M1
  state-gated ambient event pool (RTS — fewer/corrupt clothes → groping/flashing fires on ordinary
  actions); M2 clothing/nudity → reactions+consequences (Lustbound momHouse, disposition-mediated); M3
  per-NPC demeanor by relationship+stats; M4 standing/reputation reflected. Synthesis: reactivity =
  PASSIVE (world acts on you) + DEMEANOR (treats you differently), state-driven, **per-NPC-disposition**
  (keyed to casting hooks). Confirms LO's clothing→groping hypothesis.
- **`11_reactive_world_design.md`** — the FIX for Gap 2. World reacts to CLOTHING exposure (not traits);
  reactions are LEWD/transgressive (grope→molest→rape), never social. Exposure→transgression ladder;
  who/how-far = per-place CEILING (authored at generation) × NPC disposition (in character). Three modes:
  sought / choice (refuse-or-accept) / FORCED (high exposure × lawless = choice removed). Risk AND reward;
  feeds the desire ladder; charge at the ceiling (non-con incl.). Engine reuse: clothing/worn_corruption
  + lanes 2/3 gated on outfit not meters.
- **`12_economy_research.md`** — research for Gap 5 (economy). RTS source: two currencies (clean money +
  dirtyMoney with a laundering loop), multi-path income — legit gigs (DogWalking 45→Cleaning 75→Sitting/
  Care 110) + LEWD WORK (camgirl/xcam, prostitution/clients, stripping = pays more, IS the content).
  KEY INSIGHT: the economy IS a corruption ladder (legit-low → lewd-high as you fall, so earning = corrupting
  = playing the fantasy; money pressure pulls you down the lewd path). Cross-game same pattern (Lustbound
  OnlyFans+pros, Gakko corporate-ladder, Company slave economy, BtF gifts). Inherently anti-grind.
- **`13_economy_design.md`** — the FIX for Gap 5. ONE wallet (money is money — laundering dropped). The
  economy is a CORRUPTION LADDER (legit-low → lewd-high; better money is down the lewd path, so the broke
  pressure IS the temptation). Anti-grind by construction: multiple paths × paths-ARE-content ×
  escalating pay. Pressure kept alive by scaling SINKS (rent/debt + clothing + the empire), not a tax.
  Fuses income+pressure+content+desire into the same beats. Rates/paths authored per game.
- **`14_legibility_and_pacing.md`** — the FIX for Gaps 3 & 4 (both small; the desire ladder/economy carry
  most). **Gap 3 (legibility):** not a new tracker (we have quest cards) — a DISCIPLINE: the tracker IS
  the desire ladder's current want + shows the next concrete ACTION (what·where·when, the RTS miss) +
  telegraphs the next + never stale. **Gap 4 (pacing):** every want ends in a PAYOFF (P1); escalate (P2);
  alternate big/small (P3); cap the gap between payoffs (P4, anti-grind); don't dump it all (P5); rates
  authored per game (P6). The two reinforce: visible next-want = always-near next-payoff.
- **`15_dry_run_2_bar_empire.md`** — the VALIDATION re-run: the canonical bar→empire fantasy through the
  *now-complete* pipeline (Step 0a + cascade + casting + arcs + all 6 fixes), with a brutal re-critique.
  Verdict: front-end + all 6 fixes **hold** (harder than #1 — this fantasy clears the Step-0a bar the estate
  failed). But walking the WHOLE arc exposes that **our design was front-loaded** — the back half (Act 3 /
  the empire) is under-designed, failing as LC's *mirror*: drain-down-into-management, not grind-up. Six
  refinements (all one-rule additions to existing docs) — **ALL APPLIED 2026-06-09**: `14`+P7 (endgame
  escalates in CONTENT not management — the big one), `11` act-scoped forced mode (prey→predator inverts with
  power), `13`+E8/E9 (escalating pressure survival→empire-threat + recruits-are-arcs), `09` R6/`05` #5
  conquest-desire, `05` 0a-3/`06` declare desire-span, `07` §3b late-act own-pacing.
- **`16_authoring_operating_model.md`** — HOW the pipeline RUNS (the interaction contract). Three laws:
  **(1) incremental after setup** — the game is never generated one-shot; it's built one verified piece at a
  time; **(2) visible, not silent** — the user always knows, in plain language, what's being written *before*
  it's code (the review surface is the DESIGN BOOK, not the TOML); **(3) grounded, not hallucinated** — crucial
  forks asked, engine facts verified against files, every increment built green, assumptions stated. Two
  interaction modes kept separate: **A — decision gate** (`AskUserQuestion`, only at identity-setting forks,
  options+recommendation, batched per checkpoint) vs **B — inform-and-proceed** (skimmable plain-language note,
  most of the loop). The increment ladder per phase (Step 4 = one NPC at a time; Step 6 = one scene at a time,
  build-green). Increment ≠ slice (build order, not final size — full game still). This is the missing process
  doctrine that makes the quality bar (`05`–`15`) actually *bite* per-increment instead of hoped-for in a dump.
- **`17_frontier_endless_model.md`** — what replaces "design the endings." We build **endless sandboxes**
  (like RTS), not limited games with a finish line. Three kinds of "ending": **local arc endings KEEP**
  (a thread's terminal capstone), **the hard game-ending DROP** (no closing win-screen), **the FRONTIER
  DESIGN** — the desire ladder (`09`) is **open-topped**, its top rung is the current edge of authored
  content, not a wall. The frontier rung does three jobs: **land a payoff · drop into a livable steady-state
  · leave a greyed seed for the next rung** (the clip-point a later extension bolts onto). Endless ≠ aimless:
  the frontier is **narrated honestly** (`14` L6), never a blank screen (the RTS sin). Pacing becomes
  **climb → plateau → climb** (`14` P2). Folds into `09` (open-topped) + `14` (L6 + P2); partner of `16`
  (build to a frontier, extend it later).
- **`18_step5_content_roster.md`** — **Step 5 re-homed.** The checklist of every scene the game needs — the
  bridge from arcs (`07`) to authoring (Step 6). Re-homes the skill's `references/content-design.md` into the
  pipeline and rewires it: **two tracks** (NPC-arc, double-locked `07`; AND the player/world feeders the old
  skill was blind to — self-corruption feeders + the new **reactive-world** track `11`/archetype 10); **every
  row hangs on a WANT** (`09` — no meter-exercise rows); the **feeder economy** (supply must open the doors the
  NPC track demands); the 9+1 **archetype catalog** + the corr-0→45 **tier ladder** (RTS-grounded, preserved);
  **archetype 4 = the economy `13`**; the roster artifact table (now with `want` + reactive `mode`/`gate`
  columns); **open-topped** (rows past the frontier = telegraphed seeds, `17`); surfaced + authored
  incrementally (`16`). Slice scope dropped (full game; venue columns filled).
- **`19_step6_authoring_reconcile.md`** — **Step 6 reconciled** (the "how" — write scenes + build). Headline:
  reading the actual skill (`SKILL.md` + `beat-authoring.md`), **Step 6 mostly already exists and aligns** —
  one beat/turn → validate → stop **is** `16`'s incremental build-green; it already reads the design book /
  roster and uses AskUserQuestion. So it's a set of targeted DELTAS, not a rewrite: **D1** drop `scope_mode`/
  slice everywhere (contraception rule collapses to the `pregnancy` axis); **D2** point at the re-homed roster
  (`18`); **D3** every beat serves a WANT (`09` R4 — the key anti-grind delta); **D4** add the new doctrine to
  the per-beat self-audit (reactive world `11`, explicit double-lock `07`, frontier `17`, endgame-carnal `14`
  P7/`13` E9, escalating pressure `13` E8, late-act pacing `07` §3b, conquest-desire `05`/`09`); **D5**
  calibrate ask-vs-inform (`16` — not a question every beat); **D6** engine-forced changes bounce UP to the
  design book. The whole validation/doctrine self-audit + ledger + build pipeline stays as-is.
- **`20_implementation_decisions.md`** — **the locked wiring contract.** The output of the conflict-audit
  review (read the whole existing skill against the redesign): the conflicts found + **LO's locked decision on
  each**, with per-decision skill touch-lists. Standing rule: **redesign wins; the skill is brought to match it
  exactly.** Eight decisions: (1) slice removed (7-file touch-list; keep the ledger `npcs` block); (2) clothing
  rule refined — may *trigger* reactive events, must not gate an NPC arc spine; (3) ask-crucial/inform-routine,
  not every beat; (4) **ledger born at setup** as a phase tracker → **phase-aware dispatch** (D7); (5) build
  artifact stays at Step 6; (6) the per-increment rhythm = ideate → decide → write; (7) **casting = role + hook
  + rough sketch** (cross-NPC = light threads in the sketch, no formal web); (8) fix the stale step numbering in
  `01`. Plus open-verify **E1** (the `04` stat legs charisma/fitness must be confirmed real engine traits).

## The pipeline (target)
```
0. Good-game      → core FANTASY + desire curve; the 8 quality checks everything answers to   [doc 05]
1. Setup          → bare seed (premise · cast · map · systems)                          [LOCKED, doc 01]
2. Top-level      → story/roadmap, world logic, economy, time, progression ENGINE/cascade   [doc 04; rest TBD]
3. Casting        → every NPC a ROLE + HOOK serving the fantasy (no random NPCs)        [doc 06]
4. NPC arcs       → per-character locks/scenes/voice/ceiling (off the cascade)          [doc 07]
5. Content roster → the scene list (NPC-arc + player/world feeders + reactive)          [doc 18 — re-homed]
6. Authoring      → write scenes + all technical plumbing (the "how")                   [doc 19 — reconciled]

   RUN MODE (all phases) → incremental after setup · ask crucial / inform rest · build green   [doc 16]
```

## Status
- **Step 0** (good-game qualities): drafted (`05`).
- **Step 1** (setup): LOCKED (`01`).
- **Step 2** (top-level): progression engine LOCKED (`04`); desire ladder (`09`), reactive world (`11`),
  economy (`13`), legibility+pacing (`14`), **frontier/endless model (`17`)** designed; only the explicit
  story-spine/roadmap framing left (mostly subsumed by the desire ladder `09`).
- **Step 3** (casting): drafted (`06`).
- **Step 4** (NPC arcs): drafted (`07`).
- **Step 5** (roster): **re-homed (`18`)** — relocated into the pipeline + rewired to `07`/`09`/`11`/`13`/`17`/`16`.
- **Step 6** (authoring): **reconciled (`19`)** — already largely aligned (one beat/turn → validate → stop); 6 targeted deltas D1–D6.
- **Validated**: dry-run #2 (`15`) — front-end + 6 fixes hold; 6 back-half refinements applied across `05`–`14`.
- **Run mode**: the operating model / interaction contract is drafted (`16`).
- **All steps designed + conflict-audited against the existing skill; decisions LOCKED (`20`).** Remaining =
  **IMPLEMENTATION**: wire the whole pipeline (steps 0–6 + `16` run-mode + `17` frontier + `18` roster +
  `19`'s D1–D7 deltas + `20`'s 8 locked decisions) into `author-game/SKILL.md` and its references. Open-verify
  at wiring: **E1** (the `04` stat legs charisma/fitness must be confirmed real engine traits — don't assume).
  (Only a light story-spine framing is still optional, largely covered by the desire ladder `09`.)

## Hard rules carried in
- Scope is always **full game** (slice removed). Incremental = build ORDER, not size (`16`).
- **Incremental after setup** — never generate the game (or a phase) in one shot; one verified piece at a time (`16`).
- **Visible, not silent** — the user knows in plain language what's written *before* it's code; ask crucial forks,
  inform the rest, invent nothing silently (`16`).
- **What before how** — technical layer (flags/traits/TOML/ledger/build) deferred to step 6.
- Creative layer → the **design book** (the user's review surface); engine layer → the authoring step.
