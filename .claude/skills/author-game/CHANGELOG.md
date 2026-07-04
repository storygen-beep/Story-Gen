# author-game — CHANGELOG

The ledger for this skill. Record **every** change to any file in this skill
(`SKILL.md`, `references/*`, `scripts/*`, etc.) — including small fixes and wording.
Newest first. One bullet per change; group bullets under the date they were made.
Per entry: **what** changed (name the file) — **why** (the motivation / root cause) — and
how it was verified if relevant (grep / build / live-play).

Convention lives in `story_gen_django/CLAUDE.md` → "Skill ledger".

<!-- entries recorded going forward; example shape:
## YYYY-MM-DD
- reworded dispatch note (`SKILL.md`) — clarified phase resume — n/a
-->

## 2026-07-04
- **Vesper-history gap sweep — 6 doctrine follow-ups (batch 8).** An exhaustive workflow sweep (`wf_84dd0761`:
  231 raw candidate lessons mined across the 76-entry decisions_log / design_book / iteration-log / 10k-line
  transcript, deduped, adversarially verified) confirmed the just-closed backlog covered the vast majority; **6
  survived as genuinely-missed.** All doctrine-only, zero engine change (each composes primitives the skill
  already documents):
  - **Cascade beat-0 contract** (`engine-reference.md` + `beat-authoring.md` drift-check note) — beat[0] renders
    into the node lead and its `advance_text` is silently ignored; visible clicks = beats−1; a beat-count
    "dropped first beat" is the expected merge, not a bug (the Vesper turn-23 false-alarm). Kills a false-alarm
    class.
  - **Distinct-violation axis** (`trait-design.md` static-owner row) — differentiate stacked use-scenes by WHAT
    each violates (attention/downtime/sanctuary/status), not only pose/diction. Follows on #15.
  - **Rarity is the punch + thin-on-purpose** (`rts-flat-prose.md` + `lanes.md`; `content-framework.md §2F` +
    `step-6-feedback.md`) — a scarce beat escalates by WEIGHT not FREQUENCY (the rising-frequency curve is for
    repeatable ambients only); a *declared*-lean day is thin-on-purpose (say so, like the fail-state / systems
    declarations), not an auto-fatten gap. **Corrects the #10 day-breadth audit.**
  - **Floor-not-block refill path** (`location-design.md §5` + `§4 Case C` + `toml-gotchas.md`) — a costed move
    that's the ONLY route to its own refill must floor the cost (deduct + clamp), not gate it; a blocking toll
    strands the player. Kills a softlock class + removes a travel-friction contradiction.
  - **No real-time timer** (`engine-reference.md`) — time is click-driven minutes only; a "lasts N minutes"
    fiction is canvas-routed (`targetType="node"`), never a live countdown.
  - **Reverse ledger hygiene** (`beat-authoring.md` resume + `ledger-schema.md`) — on resume, also prune orphan
    flags, reconcile stale deferred notes, and advance a frozen `_active_beat`.
  Dropped a phantom `content-framework §G` cross-ref the verify agent mis-cited (that section doesn't exist).
- **#15 + #16 the "who climbs?" axis (static-owner NPC + still-point player)** — the skill taught exactly ONE
  progression model: the player climbs a corruption ladder + each NPC climbs their own odometer on top. The
  arc-shape table (`trait-design.md:35-41`) had 5 rows, ALL climbs — no row for a static/already-at-ceiling owner
  (Vesper's Mercer, hand-rolled as "the exemption" / "the sanctioned exception to the double-lock") — and
  `step-2-toplevel.md` + `rts-design-philosophy.md` baked in a player-corruption spine as the master "lewd door",
  with no room for a still-point player (Vesper's honeypot: player is the constant, global `corruption`
  legitimately DEAD, both axes on the NPC — `relation` = ACCESS + `corruption` = SEDUCTION, the "double-lock
  variant"). Both are GENERAL, field-recognized shapes (`nonlinear_rpg_skill_research`'s #1 gap "no
  player-identity axis"; `writing_craft` §5 fantasy-position; player-corruption is a CONVENTION not an engine
  requirement — `engine-reference.md:41-49`), so they're now named as first-class shapes on ONE **"who climbs?"**
  axis (both-climb / player-climbs-NPC-fixed / **player-fixed-NPC-climbs = still-point** / **neither-climbs =
  static owner**). Added: 2 arc-shape rows + a framing line (`trait-design.md`); the **"Who climbs?"**
  player-position question (`content-framework.md §1B`, linking §2F); the still-point **double-lock variant** +
  the "corruption may be legit-dead" exception (`step-2-toplevel.md`); a static-owner budget row (`lanes.md`);
  P1/P3 variant one-liners (`rts-design-philosophy.md`); a "not every NPC is a climb" note (`step-3-casting.md`).
  Anti-overfit: each shape lists ≥3 exemplars (spy / veteran / domme; spouse / regular / mentor) with Vesper cited
  SECOND, not as the definition. Grounded in 3 research agents (Mercer + the Renner honeypot + the field survey).
  Doctrine only, zero engine change (both compose existing machinery — an odometer initialized at ceiling / a
  flag; the per-NPC `relation`+`corruption` odometers already exist).
- **#12 location-design aliveness calibration** — `location-design.md` was created this build but its
  room-content-floor was a PURE-PLOT filter: "content" = a firing canvas, and it explicitly disqualified
  atmosphere ("a kitchen with nothing to do is not 'atmosphere,' it's a dead end"), so a zone whose only job is
  AMBIENT LIFE (street events, NPC routines you cross, a place to just *be*) had no way to earn its keep — and the
  only sizing axis was SCALE, never how ALIVE. That's how Vesper's first map shipped "utilitarian, not a living
  world" (`decisions_log[19,20]`, `iteration-log` Loop 7). Folds in the corrected principle LO logged in
  `games/vesper/location_design_note.md` (never integrated until now): (1) a **"how alive?" content-budget fork**
  at `step-2b-map-design.md` (sizing move + Mode-A + self-check) — tight mission-slice ↔ living city, set on
  purpose, leaning living for a sandbox; (2) `location-design.md` §2 reworked so **sizing is scale × aliveness**
  + **depth over breadth**; (3) §6 floor + audit reworked so **"earns its keep" counts ambient life** (a solo
  activity / street event / NPC routine) — only an **empty-dead** room (neither plot nor ambient) is cut, plus a
  new audit line that the map delivers the declared aliveness. Reconciled the surface tension with `lanes.md`
  (world ambient life ≠ padding an NPC's arc-shape cell — different axes). Grounded in 3 research agents (Vesper
  decisions_log + the best-games living-world model). Doctrine only, zero engine change; the mechanical half
  (presence-on-nav, travel-friction) already lived in §5.
- **#10 the day-breadth audit (`content-framework.md` §2F "walk a representative day")** — every content audit in
  the skill counted feeder DEPTH vertically (§2E, per corruption band) or checked each chore's fusion QUALITY;
  nothing counted HORIZONTALLY how many distinct non-grind threads a representative day offers, so a lean
  single-thread game (one NPC grind + one fused chore) passed every Step-6 row green. Worse: when a game has NO
  player-feeder economy (Vesper's inverted, already-degraded protagonist) §2E passes VACUOUSLY — exactly how
  Vesper shipped a thin day ("grind Renner + serve Mercer"): the feeder axis was zero by design
  (`decisions_log[27,28]`), Step 6 graded GO (`[33]`), and the emptiness surfaced only in play → the whole
  post-ship day-depth rescue (`[59]`–`[63]`, beats 0016–0020). Added **§2F** (the horizontal sibling to §2E):
  walk a representative mid-game day, enumerate every distinct non-grind thread against a 7-category checklist
  (solo self-care / exhibition / capability ladder / second economy / exploration / ambient walk-ins / the main
  grind), tagged feeder-vs-texture, floor ~2–3 live threads; **bites even when §2E is vacuous.** Wired:
  `step-5-blueprint.md` (seed the day-breadth count beside the feeder count), `step-6-feedback.md` (a new
  whole-game-check row — day-breadth is caught only here, not by the per-item rows), `system-patterns.md` §7 (the
  day-depth recipe now points back to §2F as its review-time trigger). Grounded in Vesper's decisions_log + the
  RTS content-design model (3 research agents). Doctrine only, zero engine change.
- **#9 grind-tuning / rung-pacing throttle menu** — a repeatable escalation rung with no throttle trivializes an
  arc (Vesper's Renner climb broke on first play; it collapsed the instant its single daily-cap flag was removed,
  `decisions_log[53]`→`[58]`). The skill taught the PRINCIPLE (`rts-design-philosophy.md` P8) and `§5E` even asked
  "what stops her maxing him out in an afternoon?" but that compiled to NO knob (no §5E bridge row), only ONE
  lever was taught (the daily-cap flag, brittleness un-noted), and threshold spacing wasn't taught at all. Added
  a **throttle menu** to `trait-design.md` "Slow-burn pacing": (1) ~×2.5 threshold spacing (don't over-space a
  thin repeated beat), (2) a diegetic time cost that closes the NPC's schedule window — the fiction-friendly cap,
  SIZED to the window (a window is not a one-shot; Vesper 180/540 ≈ 3/day vs a 3-min cost farmable ~50×), (3) a
  counted daily cap (`max_triggers_per_day` / a `_today` flag) — robust backstop but brittle alone, (4) a
  conditional per-rung energy `costs`; with the recipe "spacing **+** at least one hard throttle, never one flag
  alone." Wired: `step-5-blueprint.md` (both Gate bullets — spacing + pick-a-throttle), `rts-design-philosophy.md`
  P8 (pointer), `content-framework.md` §5E bridge-table row (cadence now compiles to a knob). Reconciled the
  contradiction at `trait-catalog.md:136` — energy is the wrong PRIMARY gate for NPC escalation, but a legitimate
  per-rung throttle-COST when the fiction supports it. Engine re-verified this session (3 agents): time-cost
  `advanceTime`/`getNpcLocation` window-close, per-choice `costs` gate-enforced by `checkCostsAffordable` (not
  clamped), `max_triggers_per_day` `canTriggerCanvas`. Doctrine only, zero engine change.
- **NEW `references/quests.md`** + wiring (backlog #11) — the Quests page was authored as per-beat plumbing, never
  designed as a surface (Step 2 designed the desire-ladder CONTENT; Step 7 authored cards one at a time; Step 5
  buried "the quest-card chain" in a 5-system bullet). No pass laid out the whole page — which cost Vesper 5
  reworks (`decisions_log[54,55,57,65,75]`). `quests.md` owns it: the two-tier layout (Story-Goals spine +
  per-NPC sections via the `npc_id` field), the two ladder shapes (flag-milestone chain vs NEW stepped trait-band
  ladder — exclusive `gte X`+`lt Y` bands, coaching in `goals[].label`), the three render frames + the
  **Frame-3-blank trap** (a met numeric top rung with no `ready_canvas`/`terminal` → blank sidebar; fix = a
  flag-goal/`ready_canvas` card), the end-of-content card (no fake objective, no dev-speak), the
  sidebar-`next` == Quests-page single-renderer fact, and the design-the-page process (the Step-5 deliverable).
  Wired: `SKILL.md` doctrine library; `step-2-toplevel.md` (desire ladder = the Story-Goals column);
  `step-5-blueprint.md` §5F.1 (elevated the buried clause into a design-the-page sub-pass); `step-6-feedback.md`
  (NEW page-as-a-surface rubric row); `beat-authoring.md` (pointer + the stepped-ladder alternative); `hud.md`
  (cross-ref). Every engine claim re-verified against the CURRENT `v2.py` this session (3 research agents):
  `renderQuestsGoalBlock:14217`, `pickQuestsCard:14065`, `checkQuestsCondition:14131` (ops gte/lte/gt/lt/eq, NO
  version key), Frame-3 blank `:14244/:14266`, sidebar parity `:15449`. Corrected 3 stale memory facts
  (`computeHintGoal` is a SEPARATE stage-hint engine `:6709`; the table is `[[quest_cards]]` not `[[quests]]`;
  there is no `title` field). Doctrine only, zero engine change; Vesper is the proof-of-concept (6-rung ladder,
  28/28 live-test).
- **#20 (beat vs node) + #26 (engine-citation sweep).**
  · **#20** `beat-authoring.md` — named the two granularities under "beat": the Step-7 beat = a PLAN unit (a story
  chunk authored/verified per turn), which explodes into many single-click NODES (the `rts-flat-prose.md` Rule-2
  sense) — "design in beats, build in nodes; 3 beats → ~23 nodes; one beat per turn ≠ one screen." Closes the
  jargon trap that helped collapse Vesper's 23-node opening to 3.
  · **#26** — swept ALL engine-code `file:line` cites after the no-DB/save-safety renumber left them stale (one
  change shifted `v2.py` +5→+294 across 67 hunks). A per-file verify-and-fix workflow (18 agents, one per file)
  grep-confirmed each cite's claimed symbol against the CURRENT engine and corrected the line: **262 corrected ·
  204 already-correct · 62 load-bearing cites given a stable function-name anchor · 0 unresolved.** Finding: only
  `v2.py` renumbered — every `template_import.py`/`package_from_toml.py` cite was grep-confirmed still exact.
  Deliberate "old corpus cited the WRONG line" examples were preserved as historical prose. Added a standing note
  to `engine-reference.md` (line-cites are approximate — grep the named symbol). Verified: 12/12 random
  spot-checks (incl. template_import "unchanged" cites) resolve to the claimed symbol in live code. Cite-accuracy
  + one doctrine note; zero engine change.
- **Batch: 7 small backlog fixes** (#22, #23, #21, #19, #18, #17, #6) — verified against the CURRENT engine
  FIRST (renumbered by the no-DB/save-safety commits), which corrected three stale premises before writing:
  · **#22** `SKILL.md` — built-in traits `(always-on)` → "(engine-privileged, NOT auto-created — declare each)";
  the false line seeded an arousal-always-on hallucination in Vesper.
  · **#23** `SKILL.md` — the one-line pipeline summary omitted map design; added `→ map` to match the dispatch table.
  · **#21** `step-2-toplevel.md` + `trait-design.md` — the dead-stat test was spatial only; added the TEMPORAL
  clause (a meter that only pays off in a later act is a dead stat *now*; lock the set at Step 2, don't add a core
  meter mid-game — LO's "if corruption isn't used now, no sense adding it later").
  · **#19** `location-design.md` — added the container **double-emit** symptom (no `default_entry` → child nav
  prints twice, `v2.py:9201-9233`) beside the existing swallow note.
  · **#18** `sex-loop.md` rule 1 + NEW `toml-gotchas.md` "Flag-chain hard-fail" section — CORRECTED the wrong
  error label (a flag set only by a triggerless canvas is NOT `NEVER SET`; it hard-fails with
  `MISSING HINT - set by '<canvas>' but no location/schedule`, `v2.py:11135`/`:11165`, `CommandError`
  `package_from_toml.py:396`) + taught the milestone-flag-in-loop case (hidden trait counter) + the exempt sources.
  · **#17** `beat-authoring.md` + `media.md` — the build examples hardcoded a now-optional `--owner-id` (no-DB is
  the default) and showed no deploy build; added a labelled PUBLISH build (drop `--dev`+`--debug`, keep
  `--video-folder`), documented that `--debug` bakes `[IMAGE MISSING]`/`[VIDEO MISSING]` TEXT into the HTML at
  build time (frozen — ships even after media is added), corrected the "--debug picks ./media" myth (real 404
  risk = missing `--video-folder`, in ANY build), and fixed `media.md`'s drifted `v2.py` cites (`:13348`/`:13313`
  → `:13606`/`:13571`).
  · **#6** `sex-loop.md` NEW "Variant: anonymous / paid service venue" — the same triggerless pose-ladder loop for
  an anonymous john: no NPC/relation gate (access+coin+hygiene), **pay ON FINISH not the entry faucet** (a bug
  Vesper's brothel fixed), upkeep drop on the exit-reset, cold register.
  Doctrine only, zero engine change. Facts verified against v2.py/package_from_toml.py this session (3 parallel
  grounding agents); grep-consistency across `references/`.
- **content-framework.md §1A + step-3-casting.md — pressure-test the premise's internal logic** (backlog #13) —
  two premise holes LO caught in Vesper, not the author: the central institution (Vance Dynamics) had a tower,
  boss, villain, and missions built on it with no defined FUNCTION ("what is this company even about?"), and the
  infiltration cover didn't hold — Renner was cast as a company insider who'd recognize what she is on sight
  (recast to a deniable outside supplier who never knew what his gear was for). §1A (the premise/hook) asked only
  the PLAYER's role, never what the institution DOES; casting had a "serves the fantasy" coherence check but no
  cover-coherence test. Added a §1A bullet ("pressure-test the premise's internal logic") carrying both questions
  + the "engine builds an incoherent premise green, catch it at the premise" why (§1 is owned by Step 2, re-run at
  Step 6 — both touches inherit it); a per-target "cover holds" line in the casting self-check (cross-ref §1A);
  and a one-line pointer from the `system-patterns.md` disguise recipe. Doctrine only, zero engine change.
- **kink-ceilings.md — "a character truth is a writing LENS, not a content GATE"** (backlog #14) — the skill's
  explicit-content doctrine covered vocabulary crudeness (§1 deliver-don't-soft-pedal, §8 anti-patterns) but not
  the reflex LO stopped twice in Vesper's Renner round: using a characterization note ("she feels only the sex,
  never comfort") to VETO/narrow a hot beat (cheer-him-up-with-sex → "cold help only"; a "but never I care about
  you" asterisk) — "this is not a society-helpful game, we are building an adult porn game." Added a §1 subsection
  (the lens/gate split + why + the reconciliation that the DECLARED caps — vocab ceiling §2, place ceiling §5,
  tier gate §4, `lanes.md` honest empty cells — stay legitimate; the rule bans only ad-hoc keyboard-time purity
  narrowing), citing the existing precedent `trait-design.md` (throttle-keyed prose is heat-not-status); + a §8
  anti-pattern bullet ("Character-purity restraint reflex"); + a Contents pointer. Reconciled against a skill-wide
  sweep's 4 tension points so it can't be read as overriding "consummation if vocab allows" (`lanes.md`). Doctrine
  only, zero engine change.
- **NEW `references/system-patterns.md`** + wiring — reframes backlog item #1 (the "systems invented after the
  game was called done" root cause). Root problem: the skill's only "systems" moment was `step-2-toplevel.md §8`,
  which declared **engine toggles only** and implied systems are decided up front — but ~half of Vesper's systems
  (disguise, capability/skill track, the underworld coin economy, weapon reload, loadout, day-depth) legitimately
  **emerged from play** and then got jammed in raw as Step-7 beats, skipping the design passes, after the ledger
  had effectively said "done." Fix is NOT "decide earlier" (that fights how sandbox design works); it's (a) a
  reach-for-it **recipe menu** of the common authored subsystems, framed explicitly as *not* a seed-time
  checklist, and (b) a first-class **mid-stream fold-in loop** so a discovered system still gets its quick
  design→place→build→fold passes instead of duct-tape, with **"playable ≠ done"** made doctrine. `system-patterns.md`
  carries 7 starter recipes (disguise/cover · capability · crawl · second economy · reload upkeep · loadout ·
  day-depth), each with when-you-reach-for-it / the shape / the trap, cross-linked to the owning references and
  the #8 clamp rule; engine facts kept to stable anchors (no brittle line cites, since the engine was just
  renumbered by `8446b3d`). Wiring: `run-mode.md` NEW section "Systems grow through iteration — playable ≠ done"
  (the 4-pass loop); `SKILL.md` operating rule "Structure is stable-and-extensible" extended from
  location/NPC/flag to whole systems + a doctrine-library bullet; `step-2-toplevel.md §8` reframed to declare
  engine toggles now but let authored subsystems emerge; `systems.md` gains a pointer distinguishing ENGINE
  toggles from these AUTHORED patterns. Doctrine only, zero engine change. Verified: grep-consistency (every new
  cross-ref resolves); the menu is deliberately distinct from `systems.md`. Also updates the root
  `AUTHOR_GAME_SKILL_BACKLOG.md` (#1 reframed; #2–#7 now have starter recipes, deepen on demand).

## 2026-07-03
- **NEW `references/save-safety.md`** + wiring in `SKILL.md` (Engine-ground-truth item 9, a Knowledge-base
  index bullet, and a reinforcement on the "Structure is stable-and-extensible" operating rule) — the skill
  had **no** release/save-safety doctrine, so after the engine shipped slug passage names + constant slug ids
  + a save-migration seam, nothing told an author which changes still break a *returning player's* save on an
  update. Documents the four join keys that must stay fixed on a shipped game (immutable slugs/ids · never
  rename/repurpose a live flag or trait key · don't rescale a stat range or move tier/stage thresholds · don't
  change the game title) + a pre-update grep-guard checklist + what IS safe (add content, insert/reorder/delete
  beats, rename display names). Verified: every `file:line` cite grepped against the shipped
  `games/vesper/output/index.html` + `v2.py` — slug passage naming (`_node_passage_name` :11246 /
  `_location_passage_name` :11259), `$npcs` slug keying + `npc_slug_map` identity, `Config.saves.id`/`version`
  (:2812), `setup.stateDefaults`/`backfillStateDefaults` (:14549), `npc.id = <slug>` (`game_graph.py:144`).
- **Corrected now-stale engine facts** the same fixes obsoleted (the skill must not teach false engine facts):
  `references/dev-console-jump.md` — node passages are `Node_<nodeSlug>` not the 1-based `Node_<n>`; `$npcs` is
  keyed by slug not `npcs[uuid]`; retired the "NPC uuids regenerate every build → stale-save" framing (the bug
  is fixed); fixed the grep guard (`[0-9]+`→`[a-z_0-9]+`) and the Renner worked example
  (`Node_4`→`Node_base_doggy_r`). `SKILL.md` — the dev-console bullet's `Canvas_<id>_Node_<n>`→`Node_<nodeSlug>`.
  `references/customization.md` — `$npcs[uuid]`→`$npcs[slug]`; `npc_slug_map` `slug→uuid`→identity. Doctrine +
  fact-correction only, zero engine change (the engine work shipped in commits 8446b3d + 1d9ce93).

## 2026-07-02
- **clamp-or-vanish lint** (backlog item #8 from the Vesper→skill analysis) — hardened the banded-stat clamp
  doctrine across 5 files after an unclamped banded body-stat shipped a **blank HUD twice** in Vesper
  (`decisions_log[64]` Charge went negative; `[66]` Condition/hygiene over-capped AND went negative — `[66]`
  records it as the SECOND time and asks for a lint that was never actioned). Root cause: effects run
  `eff.clamp || false` (unbounded by default), and a banded sidebar card only draws when the value lands inside a
  band (`trait_words` closed-match `v2.py:15252`; `trait_status_text` open-on-omit `v2.py:15183`) — out of range
  it renders **nothing**, reading as a *missing* HUD element, not a wrong number, so a quick playtest sails past
  it. Changes: (1) `references/trait-catalog.md` §4 — replaced the advisory "clamp recommended on a restore" with
  the hard two-part rule (bound the value on body-need/resource stats · cover the range for unbounded odometers),
  cross-citing the `engine-reference.md` Clamp trap; fixed the bare-`+N` energy-restore example to `cap = 100`;
  turned the §5 "renders nothing when no band matches" cell into an active pointer to the rule. (2)
  `references/beat-authoring.md` — added a hard clamp row to the Step-7 resource self-audit. (3)
  `references/step-6-feedback.md` — added the review-time "no unclamped banded stat" lint (the hard lint begged
  for twice). (4) `references/toml-gotchas.md` — capped the bare-`+N` Sleep/Shower restore example so it stops
  contradicting the rule. (5) `references/engine-reference.md` — one-clause pointer at the corruption Clamp-trap
  line so mechanism + application agree. Reconciles the "unbounded is correct for corruption" carve-out
  (completes it — the value may climb, but the top band must still cover it) rather than contradicting it; `money`
  stays exempt (unbanded number, never vanishes). Verified: engine facts read from `v2.py` this session;
  grep-consistency across `references/` (no surviving "recommended on a restore" or bare-`+N` counter-example);
  the two load-bearing engine cites re-checked against the current `v2.py` after HEAD moved to `8446b3d`
  (`trait_words` closed-match `:15252`, `trait_status_text` open-bound `:15183`). Doctrine only, zero engine change.

## 2026-07-01
- NEW `references/dev-console-jump.md` + one index line in `SKILL.md` — LO asked to save the browser-console
  "jump/arm" testing technique (fast-forward a built game to a gated state via `State.variables`) as a
  reference, **on-request only**. Documents: serve over `python3 -m http.server 8080` (not `file://`) +
  console context = `top` (not an extension); the `SugarCube` API handle (this build hides bare
  `State`/`Engine`/`setup` globals); the code-verified write paths (`player.core_traits.<k>`,
  `flags.<k>`, `setup.resolveNpcId(slug)`→`npcs[uuid].core_traits`, `Object.values(player.equipped)` for
  equip); `Canvas_<authoredId>_Node_<n>` passage naming (authored ids, stable — NPC uuids are not); ARM vs
  FIRE + the "leave/re-enter to re-eval" caveat; Renner-drain worked example. All paths verified by grepping
  the live `games/vesper/output/index.html` (evaluator branches, passage-name stems all authored-id, no
  uuid). Dev convenience, explicitly gated off the authoring flow.
## 2026-06-23
- NEW `references/onboarding.md` + `references/npc-intro.md` — closed two recurring doctrine gaps an
  adversarially-verified audit found behind LO's "set the player up properly / a new character can't start
  randomly". The skill *declared* the opening must "teach with no tutorial" (step-2 §8, content-framework §1E)
  but never taught the **method**, and treated `npc_intro` as hub-plumbing with no **dramatic** first-encounter
  craft. `onboarding.md` owns the linear-funnel machine-teaching method (surface each live system once in a
  fiction beat; sidebar at value-zero; named next-action on frame one; the three why-locked surfaces; the
  win/fail contract) + a HARD-gate Step-6 rubric. `npc-intro.md` owns the first-encounter craft (pretext +
  name-on-page + hook-as-want → fire once → open the hub; the 7-step Renner template
  `vesper/5_scenes.toml:315-346`; the Hank cold-spawn anti-pattern `late_shifts/5_scenes.toml:14-35`) on top of
  the intact mechanical on-ramp doctrine. LO's locked calls: linear-funnel is the ONLY opening shape; files
  kept split (different lifecycles — onboarding fires once/game, npc-intro every NPC); rubric is a hard gate on
  load-bearing rows. Every engine knob code-verified this session (starting_canvas hard-error
  `template_import.py:6104-6118`; auto-fire `v2.py:4025`; locked_text/cost/blocked_message
  `v2.py:11762/11756/4329`; `start_after_flag`; advanceDay-only-past-24h `v2.py:4958-4999`; quest
  goals/ready_canvas/tip; sidebar bands; `speaker=unknown` `v2.py:13590`; getNpcsWithSchedules leak
  `v2.py:3132`; conditions fail-open `v2.py:3398`; is_container swallow `template_import.py:3506`) — n/a
  (doctrine; dogfooded read-only by running the rubric against Vesper's opening → flags its known machine gaps)
- wired both files in (`SKILL.md` doctrine-library bullets; `step-2-toplevel.md` §8 method pointer;
  `step-5-blueprint.md` Pass-4 opening bullet; `content-framework.md` §1E machine clause + §3B on-ramp pointer;
  `step-6-feedback.md` two self-check rubric rows; `hud.md` §1 persistent-tutorial note; `lanes.md` `npc_intro`
  beat-type expanded from plumbing to designed-encounter; `beat-authoring.md` cold-start firewall + cold-spawn
  ban; `step-3-casting.md` hook→first-encounter forward wire) — why: a reference is dead unless the steps cite
  it where the author works — grep-verified the pointers resolve to the new files

## 2026-06-22
- NEW `references/media.md` — the skill had almost NO media doctrine (its whole footprint was a 1-line block-
  vocab mention + 1 location field in `engine-reference.md`), so authors hand-rolled media and missed the
  acquisition layer: Vesper (and Last Call, Late Shifts) shipped image refs with no `search_queries`, no video,
  silently-skipped media. media.md owns it: the 3 block types (`image`/`video`/`clip`) from engine truth, the
  extension-agnostic resolve law, the silent-skip-when-missing model, the `search_queries` craft (grafted from
  `prompts/toml_generation_prompt_v4.txt:905-1001`), the tier→format contract, the text-media-text rhythm
  (`prompts/media_writing_guide.md:657-705`), folder/naming, the `find-media` hand-off — with 4 corpus lies
  explicitly corrected (clip-uses-`file`; extension-is-authoritative; "t5+ must be webm or it won't render";
  inline `[image:]` syntax). Every engine claim re-verified against `v2.py`/`template_import.py` this session —
  n/a (doctrine; dogfooded by rebuilding Vesper with `search_queries` → Missing-Media page populated)
- wired media.md in (`SKILL.md` doctrine-library bullet; `engine-reference.md` §2.5 clip `{props.file}`→
  `{props.clipId}` fix + media.md pointer, and the `image_search_queries` row's key-name-trap note;
  `beat-authoring.md` Step-7 media instruction; `step-5-blueprint.md` Pass-2 **Media** placement bullet;
  `rts-flat-prose.md` Rule 8 — flagged the `[image:]` shorthand as non-engine, point to real TOML) — why: a
  reference is dead unless the steps cite it where the author works — grep-verified pointers resolve to media.md

## 2026-06-18
- added skill-ledger pointer note in the State section (`SKILL.md`) — distinguishes the game ledger
  (`authoring_state.json`) from this skill's own ledger (`CHANGELOG.md`); part of introducing the
  per-skill CHANGELOG convention (documented in `CLAUDE.md` → "Skill ledger") — n/a (docs only)
