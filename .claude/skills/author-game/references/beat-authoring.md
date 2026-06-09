# Step 6 — authoring: write scenes + build (one beat per turn)

The final step: turn the design book into a working game. `pipeline_phase = "authoring"`. The unit of work
is **the next beat in the living plan**. A beat is any story development: `npc_intro` · `location_reveal` ·
`arc_escalation` · `cross_npc` · `economic` · `story_turn` · `capstone`. Author exactly one per turn,
validate it, then stop. This is `run-mode.md`'s "ideate → decide → write → **verify green**" rhythm in
engineering form — and the first step that produces TOML.

---

## Step-6 ENTRY — the scaffold + first green build (do ONCE, before the beat loop)
Steps 1–5 produced **only** the design book. The first time you enter authoring, the first actions emit the
buildable skeleton + seed the ledger's structure, and **prove green** — THEN the beat loop begins. (No STORY
canvases here — NPC arcs/hubs/ambients/capstones are beats. Only the skeleton + boot + sleep + spine card.)

1. **Scaffold TOML** (mirror table shapes from `games/late_shifts/toml_phases/`):
   - `games/<slug>/toml_phases/0_systems_spec.toml` — system blocks at their correct homes if used
     (clothing → `[settings]`, rent → `[settings.rent]`, phone → top-level `[phone]`; `schema/02` §1.3) +
     engine config. *(If clothing is ON but its shop venue is a later beat, point `shop_location` at an
     existing reachable hub as a stub until the real venue is authored — don't leave it dangling.)*
   - `games/<slug>/toml_phases/1_metadata_and_locations.toml` — metadata, locations (with `entry_conditions`
     + `blocked_message` for locks), npcs, `[[npcs.schedules]]`. Tag each schedule row's location category
     (reachable / locked / **offscreen** — `doctrine/10` §5.5).
   - The **minimal boot / Start canvas** the engine needs to open (drops the player into the start location).
     Structural bootstrap, NOT story content.
   - The **day-advance (sleep/rest) activity** — IF the game is time-gated: a solo canvas at the player's
     home/hub, fixed forward `time_progression_minutes` (e.g. 420 ≈ 7h) + an energy restore, schedule-gated
     to the sleep window. The clock router (`doctrine/04` §10) — without it daytime windows are unreachable.
   - The **spine quest card** (one `[[quest_cards]]`, no `npc_id` → "Story Goals"). The game's central
     pressure from the economic engine / premise (e.g. "make the weekly rent or lose your place"). A
     mechanic-mode card (a `goals` trait gate like `money >= <amount>`, no `ready_canvas`), gated `when` the
     pressure is active. If `quests_engine = "v2"` you MUST populate the Quests page or it reads as broken.
     This is the ONLY story-bearing content the scaffold authors — everything else is beats.
2. **Seed the ledger's structure** — fill `structure_registry` (every location/npc/flag the scaffold
   declares, each location tagged reachable/locked/offscreen) and `plan` (one beat per desire-ladder /
   roster item, `id = beat_0001…`, `status = planned`, `target_phase` set, `introduces` filled) + `next_up`.
   (The ledger file + `pipeline_phase` already exist from setup — here you fill the structure/plan parts.)
3. **Prove green** (repo venv active — `source venv/bin/activate`):
   ```bash
   python scripts/merge_toml_phases.py games/<slug> --validate
   python manage.py package_from_toml --file games/<slug>/toml_phases/7_final_game.toml \
     --owner-id 15b35759-e67f-4bab-be10-5a27dd7ddc7a --output games/<slug>/output --dev
   ```
   The second command does the REAL validation (schema + flag chains) and builds `index.html`; both must
   pass before the first beat. **Owner-id note:** `--owner-id` must be an existing DB user. The UUID above
   is this repo's known owner. On `Owner with ID ... not found`, find a real one
   (`python manage.py shell -c "from apps.authentication.models import User; print(User.objects.first().id)"`)
   or `createsuperuser`, and use that id.

**Which phase file a beat's content goes in** (set `target_phase`; when unsure, check where
`games/late_shifts/toml_phases/` put the analogous content):

| Beat type | Canvases → phase file | Also touches |
|---|---|---|
| `npc_intro` | `5_scenes.toml` (meet + Lane-1 hub) | `1_metadata_and_locations.toml` (npc + schedule) |
| `location_reveal` | `5_scenes.toml` (its hubs) | `1_metadata_and_locations.toml` (location def + lock) |
| `arc_escalation` | `5_scenes.toml` | — |
| `cross_npc` | `5_scenes.toml` | — |
| `economic` | `5_scenes.toml` (beat canvases) | `0_systems_spec.toml` (rent/phone `[settings]`), `8_phone.toml` |
| `story_turn` | `2_one_shots.toml` or `5_scenes.toml` | — |
| `capstone` | `4_story_arc.toml` or `5_scenes.toml` | — |

---

## Resume & reconcile (every continue turn, do this first)
1. Read `games/<slug>/authoring_state.json`. **Confirm `pipeline_phase = "authoring"`** — if it's an earlier
   phase, the game isn't ready for beats; go to that phase's reference (the dispatch in SKILL.md).
2. `python scripts/merge_toml_phases.py games/<slug> --validate` — assembles `7_final_game.toml`.
3. **Drift check:** for each beat with status `authored`/`validated`, confirm its `produced_canvas_ids`
   appear in the merged TOML. If any are missing, STOP and report — the ledger and build diverged; fix
   before authoring anything new.
4. Report: where we are, the `next_up` queue, what changed since last session.

## The beat loop
1. **Propose the next beat — ideate, then ask-or-inform (`references/run-mode.md`).** Take the head of
   `next_up` (or let the user pick / inject a new beat). **A beat fills a row from the `## Content roster`
   in `design_book.md`** (`references/step-5-roster.md`) — read the roster and pull the row's archetype /
   track / tier / **want** / hook rather than improvising a scene cold. **Name the WANT the beat serves**
   (the desire ladder, `redesign_phase_3/09` R1/R7) — frame the beat as *pursuing that want*, never "an
   activity that raises a meter"; a beat with no want is grind, cut or reframe (R4). If the beat is
   player-track (a solo self-act, location flash, public dare, job-lewd, or a **reactive-world event**), it
   has no NPC arc — it raises the player's `corruption`/`exhibitionism` odometers (or, for reactive events,
   fires on `worn_corruption`) and rides a solo host (no `npc`).
   **Ask vs inform:** a **crucial fork** (how to play a charged beat, a real branch, a frontier/identity
   call) → **Mode A** AskUserQuestion (2–4 options + a recommendation). A **routine** roster row already
   specified → **Mode B**: build it, tell the user in one line, let them interrupt. *Ask the crucial, inform
   the rest* — not a question every beat. A new/reshaped beat updates the roadmap AND the roster (add to
   `plan` with the next `beat_NNNN` id; log in `decisions_log`).
2. **Mark active** — set the beat's `status` to `active`.
3. **Amend structure if needed — WHOLE.** For each item in `introduces`, do the full amendment, never a
   bare reference: location → definition + `entry_conditions`/`blocked_message` lock + `[[npcs.schedules]]`
   + the unlock beat that reaches it; NPC → schedule + an OPEN on-ramp where the player first meets it;
   flag → ensure a reachable setter exists before anything gates on it. Add each to `structure_registry`;
   if already there, that's a conflict — don't silently re-add.
4. **Author the canvases across the right lanes.** First read TWO things:
   - the NPC's **R7 brief** in `design_book.md` — arc shape, lane budget, **voice spec**, **per-tier vocab
     ceiling**, stat ladder. Honor that intent; don't re-derive or drift it. Size to the brief's budget
     (always full-game — slice was removed). The stat ladder commits the gating **spine** (`references/
     trait-design.md`); gate rungs on that, not `relation` by default.
   - `references/lanes.md` — the four lanes, beat-type→lane mapping, budgets, hub-vs-solo separation. For
     **repeatable explicit** content (after a first-night capstone) the loop menu is `references/sex-loop.md`.
   An NPC arc is built *across* lanes per its shape (never Lane-1-only); keep the NPC hub (Lane 1) separate
   from any solo-work activity (Lane 3 host) — pronoun test: a menu verb with no NPC object is solo work.
   Voice: Lane 1/2/3 RTS-flat (~30 words) at the NPC's ceiling, Lane 4 Tier-3. **Before emitting, check
   `references/toml-gotchas.md`.** Append ONLY to the beat's `target_phase` file. Record new canvas ids in
   `produced_canvas_ids`.
5. **Author/update the quest card** — if the beat introduces/advances a *player-facing goal* (an NPC arc
   milestone, an economic milestone, a capstone). Add/replace the `[[quest_cards]]` with `when` flag-gates
   tracking arc state. NOT every beat gets a card — repeatable ambients / flavor hubs get none. See "Quest
   cards" below.
6. **Validate** (below). Fix red BEFORE marking done.
7. **Mark validated + persist** — set `status` to `validated`, append a `decisions_log` entry, write
   `authoring_state.json` back.
8. **Build at milestones** — run the full HTML build at end of an arc / session / on demand.

**If an engine limit/gotcha forces a design change (D6):** it **updates `design_book.md`** (the review
surface) and is surfaced to the user — it is **not** silently patched into the TOML. The design book stays
the source of truth.

## Validation (per beat — the safety net)
Run with the repo venv active, in order; emit a PASS/FAIL line for each:
1. `python scripts/merge_toml_phases.py games/<slug> --validate` — **syntax only**: assembles
   `7_final_game.toml` and `tomllib`-parses it. Does NOT check flags/references.
2. `python manage.py package_from_toml --file games/<slug>/toml_phases/7_final_game.toml --owner-id 15b35759-e67f-4bab-be10-5a27dd7ddc7a --output games/<slug>/output --dev` — **the real validation**: schema,
   broken references, flag chains, plus it builds `index.html`. Never skip it. (`--owner-id` must be an
   existing user; on `Owner with ID ... not found`, see the Step-6 entry owner-id note above.)
3. **Doctrine self-audit** — check each against what THIS beat authored (cite the doctrine in
   `COMPREHENSIVE_SYSTEM_REFERENCE.md`):
   - **the beat serves a WANT** — name the desire-ladder rung it pursues (`redesign_phase_3/09` R4); a beat
     whose only justification is "raises a meter" is grind — cut or reframe.
   - **reachability triad** — the canvas fires only where NPC-schedule ∩ canvas-window ∩
     player-present-and-awake overlap.
   - **dead-presence / presence floor** — every scheduled NPC has a reachable hub at each **reachable**
     schedule row; no dead presence. **Offscreen** rows (`offscreen = true`) are exempt.
   - **cold-start / no backwards on-ramp** — every arc is enterable at corruption 0 / no flags, through
     ordinary presence; an arc's entry must NOT gate on a stat only raisable by that arc's own downstream
     content (a circular gate — e.g. a housemate arc gated on `worn_corruption`). First beat needs only
     co-presence; escalation layers after.
   - **double lock on lewd rungs** (`redesign_phase_3/04`/`07`) — every **lewd** rung gates on BOTH the
     **player-corruption door** (the cascade tier) AND **the NPC's own lock** (its built personal trait);
     **non-lewd interaction is ungated** (it builds the lock in Act 1). This is the "two-axis core gate"
     vocabulary, made universal. Don't gate a lewd rung on the door alone, or on the NPC lock alone.
   - **reactive-world beats (archetype 10, `redesign_phase_3/11`)** — a clothing-triggered ambient gates on
     **`worn_corruption` × place ceiling (per-canvas conditions) × NPC disposition**, NOT cascade meters,
     and is authored as Lane 2/3. **Clothing carve-out** (`references/systems.md`): clothing MAY trigger
     these ambient PUBLIC events but must **NEVER gate an NPC's escalation spine/arc**. The *forced* mode =
     an **auto-fire capstone-shape canvas** (`priority ≥ 9`, `is_repeatable = false`, single Continue, no
     refuse/accept branch — there is no zero-choice primitive), **act-scoped** (present early, gated off
     above a power tier); the *choice* mode = a normal refuse/accept exit block.
   - **frontier (`redesign_phase_3/17`)** — beats beyond the current frontier are **telegraphed
     locked-visible seeds**, never silent gaps; the frontier beat does its three jobs (payoff · drop into
     steady-state · greyed next-hook) and its quest card narrates the frontier **honestly**, never blank.
   - **endgame stays carnal (`redesign_phase_3/14` P7 / `13`)** — a late/empire beat cashes out as
     **content**: a recruit is a **full `step-4-npc-arcs.md` arc** (own double-lock + capstone + loop), an
     "upgrade" unlocks **new scene types**, the apex is the **hottest beats** — never a `+income` widget or
     a stat-bump. Support a **late-act pressure beat** (rival/cop/boss) so the squeeze never dies.
   - **late-act own pacing (`07`)** — a **late-introduced** NPC carries a complete self-contained rung
     ladder; it can't borrow pacing from the (now-maxed) MC-corruption door.
   - **conquest-desire (`05`/`09`)** — a conquest-target beat reads as **wanted-as-conquest** (hot pursuit +
     the target has agency: resists/schemes/cracks), not a cold instrument you merely *use*.
   - **navigable scarcity (the Dee-bug law)** — every scheduled window the player must reach sits in a
     day-phase the day-cycle can deliver them to; the sleep activity is the router.
   - **stat-restore infrastructure** — if `[engine.daily_tick]` drains a player stat, there's a recovery
     activity (sleep restores energy; mirror it for hygiene etc.) — not optional polish.
   - **locked-location unlock contract** — any NPC at a locked location is meetable at an open on-ramp and
     the unlock flag has a reachable setter (Cases A/B/C).
   - **system scoping** — three homes (`schema/02` §1.3): clothing → `[settings]`, rent → `[settings.rent]`,
     phone → **top-level `[phone]`**. Never bare keys under `[time]`.
   - **optional-system doctrine** — if this beat wires clothing / rent / phone / customization, honor its
     signature trap (`references/systems.md`): clothing's **two-part rule** (triggers public reactive events;
     never gates an NPC arc spine); rent arms after an income flag; phone triggers can't use `day`/`time`/
     `location`/`random`; customizable names emit as `@`-tokens, never hardcoded.
   - **`is_container` swallow** — no activity/ambient/capstone attached to a container location.
   - **engine-set flag gating** — the flag-chain validator accepts a flag as gate-satisfiable only if
     *something* sets it (incl. engine setters: the rent `eviction_flag` and `[engine.daily_tick]`
     `flagEffects op="set"`). The rent `eviction_flag` is the CORRECT "fell behind" signal — gate
     leverage/escalation on it, not a day-1 onboarding flag. `✗ NEVER SET` = a flag nothing sets, or a
     `daily_tick` flag only `unset`. Only `is_true` gates are checked; `is_false` guards exempt.
   - **Quests page reflects current goals** — if this beat is a trackable goal, a `[[quest_cards]]` shows it
     at the right time (and the prior milestone's card retires via its `when` gate). Never empty, never
     stale. Each `goals` label **NAMES THE TRAIT** ("Corruption" / "<NPC> Relation"), matching the sidebar —
     never a raw key path. Repeatable ambients/flavor: no card.
   - **lane coverage vs arc shape** — the NPC's content spans the lanes its shape calls for (not
     Lane-1-only), within the brief's budget, and EMPTY cells stay empty (peer/dating: no Lane 3; service:
     no Lane 2/3). The hub holds only NPC-object verbs; solo work/chores are their own canvases. Each Lane 3
     substitution canvas ships `substitution_only=true` + `max_triggers_per_day=1` + `is_repeatable=true` +
     a `location`. Hub base opener is one constant paragraph (not tiered).
   - **vocab ceiling honored** — explicit content sits at the NPC's declared per-tier ceiling (R7 brief);
     default to the MOST explicit reading. **Contraception language is `pregnancy`-conditional** (slice was
     removed, so it's now a single axis): ship **bareback** (no contraception language, so a pregnancy
     retrofit can attach) when `pregnancy = defer`; it INVERTS at `pregnancy = include` — contraception
     language is then ALLOWED in pre-pregnancy scenes, still banned post-pregnancy. Read the game's
     Phase-2+ calls from the design book.
   - **traits declared before use** — any trait this beat references is already in `[player.core_traits]` /
     `[npcs.core_traits]`; an undeclared trait is a sidebar hard-fail or a silent no-op. **Only real engine
     traits** — corruption/arousal/energy/hygiene/money + exhibitionism/fitness/intelligence; `beauty` is
     derived from clothing (not raisable); a "social"/charisma/career stat is a **Tier-3 custom** trait
     (declare it, then it's fine). See the SKILL.md engine ground-truth.
   - **trait spine + throttle/odometer + no dead/split meter** — gates use a shape-appropriate **odometer**
     (`references/trait-design.md`), not `relation`-on-everything NOR player-`corruption`-on-everything.
     Odometer (permanent: player `corruption`, `npc.relation`, `npc.corruption`) gates rungs AND one-shot
     capstones. Throttle (`arousal`, resets at climax) gates **repeatable** in-scene content — NEVER a
     one-shot capstone; its prose stays heat-framed. Failure modes: **dead meter** (climbs but no gate reads
     it — gate it or cut the raise); **split spine** (an odometer the hub builds that the milestone never
     reads — LC's Marcus); **gold-plated peripheral** (the rich two-meter model belongs ONLY to the 1–2 core
     slow-burn arcs — a peripheral gets player corruption + a flag, or one `relation`/`money` milestone).
   - **feeder economy / player-odometer reachable** — a player-track beat actually RAISES the player
     `corruption`/`exhibitionism` odometer it feeds, rides a solo host (no `npc`/`requires_npc`), and gates
     on the **player** tier — NOT an NPC walk-in (`references/step-5-roster.md`). Converse for NPC-track: a
     seduction capstone's player-corruption FLOOR is reachable from the feeder supply the roster declares —
     tier-complete feeders before deep floors.
   - **spent resources gate via `costs`** — if this beat costs a resource (energy/hygiene/shift/chore), the
     spend goes in **`costs`** (trigger-level for a single-exit activity, per-choice for a multi-intensity
     exit, tiered under any `conditions` main-lock). `costs` GATES *and* deducts. NEVER spend via `effects
     {op=add, value=-N}` (decrements without gating → cosmetic meter), NEVER gate with `conditions` +
     `locked_text_threshold` (renders a clickable toast-button). `effects` carries only gains (money/relation)
     + `time_progression_minutes`; restores (sleep/shower) stay `effects`-positive.
   - **sidebar visibility per arc shape** — a beat that adds an NPC surfaces its traits by shape (family:
     arousal+corruption+relation; slow-burn: arousal+relation; peer/service: relation; antagonist:
     location-only); `stage` + antagonist `awareness` NEVER surface.
   - **choice labels RTS-flat** — terse action verbs, not literary sentences; no self-justifying subtext;
     crude-in-label at the NPC's ceiling; emoji on menu/hub buttons, bare on in-loop cascade beats.
   - **locked rungs render as intended** — escalation rungs use `show_when_locked` (greyed-visible); a bare
     greyed span needs NO `locked_text_threshold` (that field renders a click-to-toast button). Non-ladder
     gated choices (daily caps, intra-loop beats, narrative branches) HIDE — no `show_when_locked`.

Any FAIL → fix, re-run, then mark validated.

## Live-testing note (twine-game-explorer + `--dev` builds)
When live-playing a `--dev` build, the explorer's Phase 0 auto-advance clicks "Next" — and the dev **"Next
Day"** button matches, so Phase 0 can advance days and reset the clock to morning (6 AM), putting the game
OUTSIDE evening schedules so schedule/presence-gated content correctly won't render (looks like a bug that
isn't). Before concluding a hub/canvas is broken, **verify the NPC is present at the current game time**.
Avoid it with `--skip-phase0` or a non-`--dev` build.

**Stale-session trap.** SugarCube keeps the in-progress playthrough in sessionStorage and restores it on a
plain **reload** — so after rebuilding `index.html`, a refresh resumes the OLD session's state on the NEW
code (inconsistent gates). For a TRUE fresh test: in-game **Restart**, clear local/sessionStorage, or a
private window (`--fresh`). After ANY gate/trait change, reset before judging.

## Quest cards (`[[quest_cards]]` — the Quests page)
Active only when `[project].quests_engine = "v2"`. Authoritative schema: `schema/02` §8; condition shape:
§16.5; doctrine: `doctrine/04` (Doc 49 goals-vs-sidebar, Doc 50 R1–R6 card shape).
- **Where they render:** no `npc_id` → top **"Story Goals"** (the spine); `npc_id` set → that NPC's section.
- **Fields:** `text` · `ready_text` · `tip` · `npc_id` · `priority` · `when` (routing — ALL must be true) ·
  `goals` (🎯 to-advance bullets) · `ready_canvas` (set → 🔓 Ready frame) · `terminal = true` (✓ complete).
- **Condition shape is FLAT** (no `type` discriminator): flag gate `{ flag = "x", op = "is_true" }`; trait
  gate `{ trait = "relation", subject = "npc", npc_id = "npc_x", op = "gte", value = 10, label = "X trust" }`.
- **Three modes:** *mechanic* (no `ready_canvas` — crossing a `goals` threshold IS the unlock); *capstone*
  (`ready_canvas` → Ready frame launches the one-shot); *terminal* (`terminal = true`).
- **Milestone chain:** one card per arc stage, each gated `when` the prior stage's flag is set and this
  stage's completion flag is not — so exactly one card shows per NPC at a time. The frontier card narrates
  the current peak honestly (`redesign_phase_3/17`), never blank.
- Author quest cards into the beat's `target_phase` (or `5_scenes.toml`), alongside its canvases.

## Cross-references
`references/run-mode.md` (the ask/inform + build-green discipline) · `references/step-5-roster.md` (the rows
this fills) · `references/trait-design.md` / `lanes.md` / `sex-loop.md` / `systems.md` / `toml-gotchas.md` ·
`redesign_phase_3/{04,07,09,11,14,17}` (the doctrine the new self-audit lines enforce).
