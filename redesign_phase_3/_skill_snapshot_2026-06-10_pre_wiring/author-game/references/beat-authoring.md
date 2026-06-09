# Continue mode — author one beat per turn

The unit of work is **the next beat in the living plan**. A beat is any story development:
`npc_intro` · `location_reveal` · `arc_escalation` · `cross_npc` · `economic` · `story_turn` ·
`capstone`. Author exactly one per turn, validate it, then stop.

**Which phase file a beat's content goes in** (set the beat's `target_phase` accordingly; when
unsure, check where `games/late_shifts/toml_phases/` put the analogous content):

| Beat type | Canvases → phase file | Also touches |
|---|---|---|
| `npc_intro` | `5_scenes.toml` (meet + Lane-1 hub) | `1_metadata_and_locations.toml` (npc + schedule) |
| `location_reveal` | `5_scenes.toml` (its hubs) | `1_metadata_and_locations.toml` (location def + lock) |
| `arc_escalation` | `5_scenes.toml` | — |
| `cross_npc` | `5_scenes.toml` | — |
| `economic` | `5_scenes.toml` (beat canvases) | `0_systems_spec.toml` (rent/phone `[settings]`), `8_phone.toml` |
| `story_turn` | `2_one_shots.toml` (one-shot event) or `5_scenes.toml` | — |
| `capstone` | `4_story_arc.toml` or `5_scenes.toml` | — |

## Resume & reconcile (every continue turn, do this first)
1. Read `games/<slug>/authoring_state.json`.
2. `python scripts/merge_toml_phases.py games/<slug> --validate` — assembles `7_final_game.toml`.
3. **Drift check:** for each beat with status `authored`/`validated`, confirm its
   `produced_canvas_ids` appear in the merged TOML. If any are missing, STOP and report — the
   ledger and the build have diverged; fix before authoring anything new. (The merge +
   `package_from_toml` build is the real safety net; this check just catches out-of-band edits.)
4. Report: where we are, the `next_up` queue, what changed since last session.

## The beat loop
1. **Propose the next beat — with ideas + options.** Take the head of `next_up` (or let the user
   pick / inject a brand-new beat). **A beat fills a row from the `## Content roster` in
   `design_book.md`** (`references/content-design.md`) — read the roster and pull the row's
   archetype / track / tier / hook rather than improvising a scene cold. If the beat is player-track
   (a solo self-act, location flash, public dare, job-lewd feeder), it has no NPC arc — it raises the
   player's `corruption`/`exhibitionism` odometers and rides a solo activity host (no `npc`). Present
   via AskUserQuestion: 2–4 concrete ways to play the beat + a recommendation. A new or reshaped beat
   updates the roadmap AND the roster (add it to `plan` with the next `beat_NNNN` id; log the change in
   `decisions_log`).
2. **Mark active** — set the beat's `status` to `active` in the ledger.
3. **Amend structure if needed — WHOLE.** For each item in the beat's `introduces`, do the full
   amendment, never a bare reference:
   - location → definition + `entry_conditions`/`blocked_message` lock + `[[npcs.schedules]]`
     wiring + the unlock beat that reaches it (the unlock contract);
   - NPC → schedule + an OPEN on-ramp where the player first meets it (the presence floor);
   - flag → ensure a reachable setter exists before anything gates on it.
   Add each new location/npc/flag to `structure_registry`. If it's already there, that's a
   conflict — do not silently re-add.
4. **Author the canvases across the right lanes.** First read TWO things:
   - the NPC's **R7 brief** in `design_book.md` — its arc shape, lane budget, **voice spec**,
     **per-tier vocab ceiling**, and stat ladder. Honor that intent; don't re-derive or drift it.
     Size the arc to the brief's budget AND the game's `scope_mode` (from the ledger). The stat ladder
     commits the gating **spine** — which trait drives this arc, by shape (`references/trait-design.md`);
     gate the rungs on that, not on `relation` by default.
   - `references/lanes.md` — the four lanes (when + how to write each, verbs/narrative/fingerprints),
     beat-type→lane mapping, budgets, and the hub-vs-solo-work separation. For **repeatable explicit**
     content (after a first-night capstone) the loop menu is its own pattern — `references/sex-loop.md`.
   An NPC arc is built *across* lanes per its shape (never Lane-1-only); keep the NPC hub (Lane 1)
   separate from any Maya-solo work activity (Lane 3 host) — pronoun test: a menu verb with no NPC
   object is solo work, not a hub item. Voice: Lane 1/2/3 RTS-flat (~30 words) at the NPC's ceiling,
   Lane 4 Tier-3. **Before emitting, check `references/toml-gotchas.md`** (declare-before-use traits,
   single-line inline tables, choice/exit_block fields, stage-mutation shape — the silent
   build-breakers). Append ONLY to the beat's `target_phase` file. Record the new canvas ids in the
   beat's `produced_canvas_ids`.
5. **Author/update the quest card** — if the beat introduces or advances a *player-facing goal*
   (an NPC arc milestone, an economic milestone, a capstone). Add/replace the `[[quest_cards]]`
   that points the player at this step, with `when` flag-gates tracking arc state so the right
   card shows now and retires when the next stage opens (the milestone-chain pattern). NOT every
   beat gets a card — repeatable ambients / flavor hubs get none (Doc 49: quests are arcs, not
   activities). See "Quest cards" below for the shape.
6. **Validate** (below). Fix red BEFORE marking done.
7. **Mark validated + persist** — set `status` to `validated`, append a `decisions_log` entry,
   write `authoring_state.json` back.
8. **Build at milestones** — run the full HTML build at end of an arc / session / on demand
   (not every beat).

## Validation (per beat — the safety net)
Run with the repo venv active (`source venv/bin/activate`), in order; emit a PASS/FAIL line for each:
1. `python scripts/merge_toml_phases.py games/<slug> --validate` — **syntax only**: assembles
   `7_final_game.toml` and `tomllib`-parses it (catches malformed TOML, e.g. multi-line inline
   tables). It does NOT check flags or references.
2. `python manage.py package_from_toml --file games/<slug>/toml_phases/7_final_game.toml --owner-id 15b35759-e67f-4bab-be10-5a27dd7ddc7a --output games/<slug>/output --dev` — **the real validation**:
   schema, broken references, and flag chains, plus it builds `index.html`. This is the step that
   actually catches dangling structure, so never skip it. (`--owner-id` must be an existing user;
   on `Owner with ID ... not found`, see `setup-interview.md` Step 6.)
3. **Doctrine self-audit** — check each against what THIS beat authored (cite the doctrine in
   `COMPREHENSIVE_SYSTEM_REFERENCE.md`):
   - **reachability triad** — the canvas fires only where NPC-schedule ∩ canvas-window ∩
     player-present-and-awake overlap.
   - **dead-presence / presence floor** — every scheduled NPC has a reachable hub at each
     **reachable** schedule row; no dead presence. **Offscreen** rows (`offscreen = true` away/home/
     sleep blocks) are exempt — no hub, no floor (`doctrine/10` §5.5).
   - **cold-start / no backwards on-ramp** — every arc is enterable at corruption 0 / no flags, through
     ordinary presence; an arc's entry must NOT gate on a stat/flag only raisable by that arc's own
     downstream content (a circular gate — e.g. a housemate arc gated on `worn_corruption`). The first
     beat needs only co-presence; escalation layers after (`doctrine/07` backwards-on-ramp, `doctrine/02`
     §6/§8.12).
   - **navigable scarcity (the Dee-bug law)** — every scheduled window the player must reach sits in
     a day-phase the day-cycle can deliver them to. A daytime depot window is dead if nothing carries
     the player from the night hub to daytime; the day-advance sleep activity is that router
     (`doctrine/04` §10). If this beat schedules content in a new phase, confirm the cycle reaches it.
   - **stat-restore infrastructure** — if `[engine.daily_tick]` drains a player stat (hygiene/energy)
     with no way to recover it, the game spirals to the bottom band. The sleep router already restores
     energy (`doctrine/04` §10); mirror it for any other drained stat — a restore activity (e.g. a
     shower for hygiene) authored as a solo canvas (no NPC sub), not optional polish.
   - **locked-location unlock contract** — any NPC at a locked location is meetable at an open
     on-ramp and the unlock flag has a reachable setter (Cases A/B/C).
   - **system scoping** — three systems, three different homes (`schema/02` §1.3): clothing →
     `[settings]`, rent → `[settings.rent]`, phone → **top-level `[phone]`** (NOT under `[settings]`).
     Never bare keys under `[time]`.
   - **optional-system doctrine** — if this beat wires clothing / rent / phone / customization, honor
     its signature trap (`references/systems.md` + the linked doctrine): clothing gates PUBLIC content
     never an NPC arc; rent arms after an income flag; phone triggers can't use `day`/`time`/`location`/
     `random`; customizable names must be emitted as `@`-tokens, never hardcoded into labels.
   - **`is_container` swallow** — no activity / ambient / capstone attached to a container
     location (containers are pure-nav and swallow attached canvases).
   - **engine-set flag gating** — the flag-chain validator accepts a flag as gate-satisfiable only
     if *something* sets it — and that includes ENGINE-configured setters: the rent `eviction_flag`
     **and** `[engine.daily_tick]` `flagEffects` with `op = "set"` are registered in the unlock map, so
     you MAY gate a trigger `is_true` on them. The rent `eviction_flag` is in fact the CORRECT "fell
     behind" signal — gate leverage/escalation content on it, not on a day-1 onboarding flag (so a
     player who always pays never triggers the fell-behind branch). What STILL fails `✗ <flag>  NEVER SET`: a flag
     NOTHING sets — no canvas `flagEffects`, no phone reply, not an engine setter — or a `daily_tick`
     flag that's only `unset` (a clear, not a setter; its canvas setter still must exist). For those,
     gate on a canvas-set flag (+ `requires_npc`/schedule for timing), or deliver via a phone-thread
     condition (not flag-chain-validated). Only `is_true` gates are checked; `is_false` guards are exempt.
   - **Quests page reflects current goals** — if this beat is a trackable goal, a `[[quest_cards]]`
     now shows it at the right time (and the prior milestone's card retires via its `when` gate).
     The Quests page is never empty and never stale (Doc 49). Repeatable ambients/flavor: no card.
     Each `goals` label **NAMES THE TRAIT** ("Corruption" / "<NPC> Relation"), matching the sidebar —
     never a raw key path (D50-R6, reversed; `doctrine/04` §2).
   - **lane coverage vs arc shape** — the NPC's content spans the lanes its shape calls for (not
     Lane-1-only), within the brief's budget + the game's `scope_mode`, and EMPTY cells stay empty
     (peer/dating: no Lane 3; service: no Lane 2/3). The NPC hub holds only NPC-object verbs; solo
     work/chores are their own canvases (§8.2/§8.3). Each Lane 3 substitution canvas ships
     `substitution_only=true` + `max_triggers_per_day=1` + `is_repeatable=true` + a `location`
     (missing any = silent miss). Hub base opener is one constant paragraph (not tiered, D56-R1).
   - **vocab ceiling honored** — explicit content sits at the NPC's declared per-tier ceiling (R7
     brief); default to the MOST explicit reading, no euphemism drift at high tiers, lower tiers
     naturally lighter. **Contraception language is scope-conditional** (`stages/02` §10.11): ship
     bareback (no contraception language, so a pregnancy retrofit can attach) when `scope_mode: slice`
     OR `full_game` + `pregnancy = defer`; it INVERTS at `full_game` + `pregnancy = include` —
     contraception language is then ALLOWED in pre-pregnancy scenes (it sets up the beat), still banned
     post-pregnancy. Read the game's `scope_mode` + Phase-2+ calls from the ledger / design book.
   - **traits declared before use** — any trait this beat references (effect, condition, sidebar, or
     stage) is already in `[player.core_traits]` / `[npcs.core_traits]`; an undeclared trait is a
     sidebar hard-fail or a silent effect/condition no-op (`toml-gotchas.md`).
   - **trait spine + throttle/odometer + no dead/split meter** — gates use a shape-appropriate
     **odometer** (`references/trait-design.md`), not `relation`-on-everything AND not
     player-`corruption`-on-everything. **Odometer** (permanent: player `corruption`, `npc.relation`,
     `npc.corruption`) gates rungs AND one-shot capstones. **Throttle** (`arousal`, resets at climax)
     gates **repeatable in-scene content** (the sex loop) — NEVER a one-shot capstone; and its prose
     stays heat-framed, never relationship-status. Failure modes:
     - **Dead meter** — a trait climbs but NO gate reads it (worst as a visible sidebar bar). Gate it
       or cut the raise.
     - **Split spine** — an **odometer** the hub builds that the milestone it's meant to earn never
       reads (e.g. a `relation` that climbs all arc but only gates capstone #1, then the deeper
       capstones switch to global corruption — LC's Marcus). A throttle read only by the repeatable
       loop is NOT a split spine — that's its correct job.
     - **Gold-plated peripheral NPC** — the rich two-meter model (own `corruption` odometer + `arousal`
       throttle) belongs ONLY to the 1–2 core slow-burn arcs (RTS gives it to just its 3 housemates).
       If this beat hands a *peripheral* NPC (dating/service/transactional/one-off) its own arousal
       throttle or corruption odometer, that's gold-plating — run it LIGHT (player corruption tier + a
       flag, or one `relation`/`money` milestone). (`rts-design-philosophy.md` P5.)
   - **feeder economy / player-odometer reachable** — a player-track beat (solo self-act, location
     flash, public dare, job-lewd) actually RAISES the player `corruption`/`exhibitionism` odometer it's
     meant to feed, rides a solo host (no `npc`/`requires_npc`), and gates on the **player** tier — it is
     NOT an NPC walk-in (`references/content-design.md`). And the converse for NPC-track beats: a
     seduction capstone's player-corruption FLOOR is reachable from the feeder supply the roster
     declares — if this arc demands corr 30 but the game seeds no corr-0/15 feeders, the floor never
     clears (the starvation pattern). Tier-complete feeders before deep floors.
   - **spent resources gate via `costs`** (the converse of the dead-meter rule) — if this beat costs
     the player a resource (energy/hygiene on an activity, work shift, or chore), the spend goes in
     **`costs`**: trigger-level for a single-exit activity, or per-choice for a multi-intensity exit
     (tiered UNDER any `conditions` main-lock, greyed per-tier message). `costs` GATES *and* deducts.
     NEVER spend a resource via `effects {op=add, value=-N}` (it decrements without gating → cosmetic
     meter the player burns through to 0), and NEVER gate a resource with `conditions` +
     `locked_text_threshold` (renders a clickable blue toast-button, not a plain greyed rung). `effects`
     carries only the *gains* (money/relation) + `time_progression_minutes`; restores (sleep/shower)
     stay `effects`-positive. (`toml-gotchas.md` "Resource gating"; `schema/02` §6.1 + §7.4.)
   - **sidebar visibility per arc shape** — a beat that adds an NPC surfaces its traits by shape
     (family: arousal+corruption+relation; slow-burn: arousal+relation; peer/service: relation;
     antagonist: location-only); `stage` + antagonist `awareness` NEVER surface. The HUD is the world
     model — without the NPC-location radar, Lane 3 is unplannable (`doctrine/09` §8, `reference/04`).
   - **choice labels RTS-flat** — labels are terse action verbs, not literary sentences; no
     self-justifying subtext; crude-in-label at the NPC's ceiling; emoji on menu/hub buttons, bare on
     in-loop cascade beats (`lanes.md` choice-vocab).
   - **locked rungs render as intended** — escalation rungs use `show_when_locked` (greyed-visible).
     A bare greyed span (the TLS look) needs NO `locked_text_threshold` — that field renders a
     click-to-toast **button** instead. Non-ladder gated choices (daily caps, intra-loop beats,
     narrative branches) HIDE — no `show_when_locked` (`lanes.md`).

Any FAIL → fix, re-run, then mark validated.

## Live-testing note (twine-game-explorer + `--dev` builds)
When live-playing a `--dev` build to verify rendering, the explorer's Phase 0 auto-advance clicks
buttons matching "Next" — and the dev **"Next Day"** button matches, so Phase 0 can advance days and
reset the clock to morning (6 AM). That puts the game OUTSIDE evening schedules, so schedule/presence-
gated content (NPC hubs, scheduled canvases, Lane 2 ambients) correctly won't render — looking like a
bug that isn't one. Before concluding a hub/canvas is broken, **verify the NPC is present at the
current game time** (check the clock + the NPC's `[[npcs.schedules]]` window). To avoid the artifact,
live-test with `--skip-phase0` (drive pre-game manually) or a non-`--dev` build.

**Stale-session trap (the bigger one).** SugarCube keeps the in-progress playthrough in
sessionStorage and restores it on a plain page **reload** — so after you rebuild `index.html`, a
refresh resumes the OLD session's state on the NEW code, showing inconsistent gates (a flag set under
old rules + a meter at a now-impossible value). That reads as a bug but isn't. For a TRUE fresh test:
use the in-game **Restart**, clear the site's local/sessionStorage, or a private window (the
explorer's `--fresh` does this). After ANY gate/trait change, reset before judging behavior — a
"restart" that's really an F5 will mislead you.

## Quest cards (`[[quest_cards]]` — the Quests page)
Active only when `[project].quests_engine = "v2"`. Authoritative schema: `prompts_v2` `schema/02`
§8; condition shape: §16.5; doctrine: `doctrine/04` (Doc 49 goals-vs-sidebar, Doc 50 R1–R6 card shape).

- **Where they render:** no `npc_id` → top **"Story Goals"** (the spine / main objective);
  `npc_id` set → that NPC's section.
- **Fields:** `text` (climbing copy) · `ready_text` (when goals met) · `tip` (interior line) ·
  `npc_id` · `priority` · `when` (routing — ALL must be true to show this card) · `goals`
  (🎯 to-advance bullets) · `ready_canvas` (set → 🔓 Ready frame) · `terminal = true` (✓ arc complete).
- **Condition shape is FLAT** (different from trigger conditions — no `type` discriminator):
  flag gate `{ flag = "x", op = "is_true" }`; trait gate
  `{ trait = "relation", subject = "npc", npc_id = "npc_x", op = "gte", value = 10, label = "X trust" }`.
- **Three modes:** *mechanic* (no `ready_canvas` — crossing a `goals` threshold IS the unlock);
  *capstone* (`ready_canvas` → Ready frame launches the one-shot); *terminal* (`terminal = true`).
- **Milestone chain:** one card per arc stage, each gated `when` the prior stage's flag is set and
  this stage's completion flag is not — so exactly one card shows per NPC at a time.
- Author quest cards into the beat's `target_phase` (or `5_scenes.toml`), alongside its canvases.
