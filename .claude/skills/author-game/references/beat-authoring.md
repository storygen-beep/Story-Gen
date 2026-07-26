# Step 7 — authoring: write scenes + build (one beat per turn)

The final step: turn the design book into a working game. `pipeline_phase = "authoring"`. The unit of work
is **the next beat in the living plan**. A beat is any story development: `npc_intro` · `location_reveal` ·
`arc_escalation` · `cross_npc` · `economic` · `story_turn` · `capstone`. Author exactly one per turn,
validate it, then stop. This is `run-mode.md`'s "ideate → decide → write → **verify green**" rhythm in
engineering form — and the first step that produces TOML.

> **Two granularities under one word — don't conflate them.** This Step-7 **beat** is the PLAN unit: a *story
> chunk* you author + verify in one turn (a scene, an escalation, an intro). It is **not one screen.** A scripted
> beat **explodes into many single-click NODES** — the "one click reveals new content" beat of
> `references/rts-flat-prose.md` Rule 2 — each a ~2-sentence cascade node. **Design in beats (plan-units), build
> in nodes (screens):** Vesper's opening = **3 beats → ~23 nodes**. "One beat per turn" ≠ "one screen" — a rich
> beat is many.

---

## Step-7 ENTRY — the scaffold + first green build (do ONCE, before the beat loop)
Steps 1–6 produced the design book + the **blueprint** (the decided scene list with lanes/gates/placement, and
the seeded `plan`). The first time you enter authoring, the first actions emit the buildable skeleton +
register the scaffold's structure, and **prove green** — THEN the beat loop begins. (No STORY canvases here —
NPC arcs/hubs/ambients/capstones are beats. Only the skeleton + boot + sleep + spine card.)

1. **Scaffold TOML** (mirror *mechanism* table shapes from `games/late_shifts/toml_phases/` — but the
   **geography is DESIGNED, not copied**: build the location graph from the Step-2b `## Spatial graph &
   location model` artifact + `references/location-design.md`, never by cloning a peer whose topology
   family differs from this game's premise — that mismatch is what shipped The Inheritance's map wrong):
   - `games/<slug>/toml_phases/0_systems_spec.toml` — system blocks at their correct homes if used
     (clothing → `[settings]`, rent → `[settings.rent]`, phone → top-level `[phone]`; `references/engine-reference.md`) +
     engine config. *(If clothing is ON but its shop venue is a later beat, point `shop_location` at an
     existing reachable hub as a stub until the real venue is authored — don't leave it dangling.)*
   - `games/<slug>/toml_phases/1_metadata_and_locations.toml` — metadata, then the **locations exactly as the
     Step-2b graph designed them**: the topology/roots/layering + the naming contract + any `costs`
     travel-friction + locks (`entry_conditions` + `blocked_message`, each with `version = "1.0"`); then npcs
     + `[[npcs.schedules]]`. Tag each schedule row's location category (reachable / locked / **offscreen** —
     `location-design.md` §4). Run the `location-design.md` §6 room-content + reachability
     self-audit before the green build — the build won't catch a dead or incoherent map.
   - The **minimal boot / Start canvas** the engine needs to open (drops the player into the start location).
     Structural bootstrap, NOT story content.
   - The **day-advance (sleep/rest) activity** — IF the game is time-gated: a solo canvas at the player's
     home/hub, fixed forward `time_progression_minutes` (e.g. 420 ≈ 7h) + an energy restore, schedule-gated
     to the sleep window. The clock router (the day-cycle router) — without it daytime windows are unreachable.
     *(The day-advance is only the router. The daily-loop activities it unlocks — shower/bath/eat/work — are
     **content hosts**, not bare restores: in the main beat pass wire each as a Lane 3 hijack host + player
     feeder. Shape in `toml-gotchas.md` "Day System shapes"; lane wiring in `references/lanes.md`.)*
   - The **spine quest card** (one `[[quest_cards]]`, no `npc_id` → "Story Goals"). The game's central
     pressure from the economic engine / premise (e.g. "make the weekly rent or lose your place"). A
     mechanic-mode card (a `goals` trait gate like `money >= <amount>`, no `ready_canvas`), gated `when` the
     pressure is active. If `quests_engine = "v2"` you MUST populate the Quests page or it reads as broken.
     This is the ONLY story-bearing content the scaffold authors — everything else is beats.
2. **Register the scaffold's structure** — fill `structure_registry` (every location/npc/flag the scaffold
   declares, each location tagged reachable/locked/offscreen). **The `plan` is already seeded by Blueprint
   (Step 5 Pass 4)** — one beat per scene, `id = beat_0001…`, `status = planned`, `target_phase`, `introduces`,
   `next_up` order. Do NOT re-decide it here — confirm it against the scaffold and proceed. (The ledger file +
   `pipeline_phase` + the `plan` already exist; here you fill the `structure_registry` part.)
3. **Prove green** (repo venv active — `source venv/bin/activate`):
   ```bash
   python scripts/merge_toml_phases.py games/<slug> --validate
   python manage.py package_from_toml --file games/<slug>/toml_phases/7_final_game.toml \
     --output games/<slug>/output --video-folder games/<slug>/videos --dev
   ```
   The second command does the REAL validation (schema + flag chains) and builds `index.html`; both must
   pass before the first beat. **Build flags:** the no-DB in-memory build is now the DEFAULT — **no `--owner-id`
   needed** (that flag is only for the legacy `--use-db` path). `--dev` adds the stat/canvas dev controls (QA
   only). Pass **`--video-folder <media-dir>`** or every clip 404s (the src resolves to an unpopulated copy
   path — folder-independent, `--debug` does NOT switch folders). **To PUBLISH for players, drop `--dev` AND
   `--debug`** (keep `--video-folder`): `--debug` bakes `[IMAGE MISSING]`/`[VIDEO MISSING]` TEXT into the HTML at
   build time, so a debug build ships those placeholders even after the media is added; `--dev` leaks dev
   controls (`references/media.md` "QA vs publish build"). A build that actually goes to players runs
   `references/ship-gate.md` first — dropping the flags is one row of that checklist, not the whole of it.
   **`--build free|paid`** selects the cheat-page variant and **defaults to `free`**, so an ordinary build
   is always the safe one. It only matters for a game that authors `[ui.cheat_page]`; a `free` build emits
   the rows as padlocked labels with **no working effects in the file**, a `paid` build emits live rows.
   The paid artifact must go to a **gitignored** `games/<slug>/output-paid/` — the command refuses to write
   a paid build into any directory named `output`, because that path is tracked in a PUBLIC repo:
   ```bash
   python manage.py package_from_toml --file games/<slug>/toml_phases/7_final_game.toml \
     --build paid --output games/<slug>/output-paid --video-folder games/<slug>/videos
   ```

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
   before authoring anything new. *(Counting rendered clicks to sanity-check a `cascade`? Its beat[0] merges
   into the node lead and shows no advance link, so visible clicks = beats − 1 — a "dropped first beat" is the
   expected merge, not drift. See `engine-reference.md` cascade contract — which also carries the buildable shape +
   the **cascade-last** rule, mechanically checked by the cascade-order guard below.)*
4. **Ledger hygiene (reverse sweep):** beyond the ledger→TOML drift check, sweep the other direction —
   (a) a `structure_registry` flag **set but read by NO** trigger/choice/group condition or quest `when` is an
   **orphan**, safe to prune; (b) a `deferred`/`next_up`/`decisions_log` note **contradicted by since-shipped
   content** must be reconciled — an orphan flag is harmless, but a stale note actively misleads the next
   session; (c) an `_active_beat` still marked active (or pointing at an old beat) while work has moved on must
   be advanced. Cheap hygiene, not a content gate.
5. Report: where we are, the `next_up` queue, what changed since last session.

## The beat loop
1. **Propose the next beat — ideate, then ask-or-inform (`references/run-mode.md`).** Take the head of
   `next_up` (or let the user pick / inject a new beat). **A beat builds a scene from the blueprint in
   `design_book.md`** (the player blueprint / an NPC's scene list / the world blueprint — Step 5,
   `references/step-5-blueprint.md`) — pull the scene's **lane / gate / placement / want / hook** from the
   blueprint (which already decided them from the Step-4 story) rather than improvising cold. **Name the WANT the beat serves**
   (the desire ladder) — frame the beat as *pursuing that want*, never "an
   activity that raises a meter"; a beat with no want is grind, cut or reframe. If the beat is
   player-track (a solo self-act, location flash, public dare, job-lewd, or a **reactive-world event**), it
   has no NPC arc — it raises the player's `corruption`/`exhibitionism` odometers (or, for reactive events,
   fires on `worn_corruption`) and rides a solo host (no `npc`).
   **Ask vs inform:** a **crucial fork** (how to play a charged beat, a real branch, a frontier/identity
   call) → **Mode A** AskUserQuestion (2–4 options + a recommendation). A **routine** scene already
   specified in a subject brief → **Mode B**: build it, tell the user in one line, let them interrupt. *Ask the
   crucial, inform the rest* — not a question every beat. A new/reshaped beat updates the roadmap AND the
   relevant subject brief (add to `plan` with the next `beat_NNNN` id; log in `decisions_log`).
2. **Mark active** — set the beat's `status` to `active`.
3. **Amend structure if needed — WHOLE.** For each item in `introduces`, do the full amendment, never a
   bare reference: location → definition + `entry_conditions`/`blocked_message` lock + `[[npcs.schedules]]`
   + the unlock beat that reaches it; NPC → schedule + an OPEN on-ramp where the player first meets it;
   flag → ensure a reachable setter exists before anything gates on it. Add each to `structure_registry`;
   if already there, that's a conflict — don't silently re-add.
   **Changing something that already exists is an amendment too** — and its *whole*-ness includes the prose
   that quotes it. Four edits carry this bill: **MOVE** (re-parent `entry_from`/`parent`) · **RE-PRICE**
   (`costs`, rent `amount`) · **RE-SCHEDULE** (`start_time`/`end_time`/`weekdays`, `due_day`) · **RENAME a
   display label** (a trait/NPC `name`). Each silently invalidates every `tip`/`text`/`goals[].label`/
   `blocked_message`/dialogue naming the old value — the build stays green and the game lies to the player.
   Re-read that prose in the same turn; `references/prose-truth.md` has the git-diff detector that tells you
   which coupled fields you just moved (and their OLD values — the search key).
4. **Author the canvases across the right lanes.** First read TWO things:
   - the scene's row in the **blueprint** + the NPC's **story brief** in `design_book.md` — the blueprint
     already decided the lane, the gate (the spine + thresholds), the placement, and the capstone triggers;
     the story brief carries the **voice spec** + **per-tier vocab ceiling**. **Translate the blueprint; don't
     re-decide it** (a missing decision is a stop — bounce to Blueprint, don't improvise). Size to the
     blueprint's budget (always full-game — slice was removed).
   - `references/lanes.md` — the four lanes, beat-type→lane mapping, budgets, hub-vs-solo separation. For
     **repeatable explicit** content (after a first-night capstone) the loop menu is `references/sex-loop.md`.
   An NPC arc is built *across* lanes per its shape (never Lane-1-only); keep the NPC hub (Lane 1) separate
   from any solo-work activity (Lane 3 host) — pronoun test: a menu verb with no NPC object is solo work.
   Voice — **three axes** (defined in `references/rts-flat-prose.md` §2). *Person:* every `paragraph` /
   `thought_bubble` is in the game's declared `register.person` (read it from `authoring_state.json` —
   `second` by default; `dialog` blocks exempt). *Density:* Lane 1/2/3 RTS-flat — **~35–40 words per BEAT**,
   flat across every tier — at the NPC's ceiling; Lane 4 Tier-3 = **more beats (10–20), not thicker ones**.
   A beat over ~50 words wanted to be two beats: **split it, don't compress it.**
   *Mode:* when the player and an NPC are in a scene together and something gets said, play it in `dialog`
   blocks (their words do the character work) instead of narrating the exchange ("she asks how long he's
   worked here, he says four years") — `references/rts-flat-prose.md` Rule 4. **RTS runs 0.73 narration
   words : 1 dialogue word; target ≤ 1.5:1 on any scene with a present NPC, > 3:1 is a FAIL.** Lean hardest at the **hot beats**: a capstone, sex scene, or confrontation that
   narrates the encounter as summary is the worst drift there is — play those, don't report them. Multi-party
   beats give each present NPC a voiced moment (short volleys, no monologues). Narration is right
   **only when no one's actually there to speak**: solo activities, voyeur/peek where you're unseen, and the
   interior-monologue stretches of a capstone. An NPC who's *present* is not exempt — give them at least a
   line, even a terse one (a mood glimpse can be a single spoken beat). **Media:** if the beat carries a
   visual (most scene beats should — these games are image-first), author the `image`/`video` block per
   `references/media.md` — in the text-media-text rhythm, with a `description` + 2 `search_queries` (a missing
   media block with no queries renders nothing AND leaves no acquisition trail). **Before emitting, check
   `references/toml-gotchas.md`.** Append ONLY to the beat's `target_phase` file. Record new canvas ids in
   `produced_canvas_ids`.
5. **Author/update the quest card** — if the beat introduces/advances a *player-facing goal* (an NPC arc
   milestone, an economic milestone, a capstone). Add/replace the `[[quest_cards]]` with `when` flag-gates
   tracking arc state. NOT every beat gets a card — repeatable ambients / flavor hubs get none. See "Quest
   cards" below.
6. **Validate** (below). Fix red BEFORE marking done.
7. **Mark validated + persist** — set `status` to `validated`, append a `decisions_log` entry, write
   `authoring_state.json` back.
8. **Build at milestones** — run the full HTML build at end of an arc / session / on demand. **When the
   milestone is a RELEASE** (a build that goes to players), run `references/ship-gate.md` first — the
   whole-game checklist (meter ceilings · dangling promises · the cheat page · the publish flags · the
   scanners re-run at whole-game scope). It is recurring, not a phase: shipping doesn't end authoring.

**If an engine limit/gotcha forces a design change:** it **bounces UP to `design_book.md`** (the review
surface) — to the **blueprint** if it's a structural change (a gate, a lane, a placement), to the **story** if
it runs deeper — and is surfaced to the user, **not** silently patched into the TOML. The design book stays
the source of truth.

## Validation (per beat — the safety net)
Run with the repo venv active, in order; emit a PASS/FAIL line for each:
1. `python scripts/merge_toml_phases.py games/<slug> --validate` — **syntax only**: assembles
   `7_final_game.toml` and `tomllib`-parses it. Does NOT check flags/references.
2. `python manage.py package_from_toml --file games/<slug>/toml_phases/7_final_game.toml --output games/<slug>/output --video-folder games/<slug>/videos --dev` — **the real validation**: schema,
   broken references, flag chains, plus it builds `index.html`. Never skip it. (No-DB is the default — no
   `--owner-id` needed; `--video-folder` keeps clips from 404ing. To publish, drop `--dev`/`--debug` — see the
   Step-7 ENTRY build-flags note above.)
3. **Mechanical guards** — two lint scripts (both exit 1 to gate the build; run under the venv):
   - **Render-bucket guard** — `python .claude/skills/author-game/scripts/check_render_buckets.py games/<slug>/toml_phases/7_final_game.toml`.
     Flags every repeatable, manual, non-substitution canvas that has `requires_npc` but no `npc` — the silent
     trap where an NPC hub drops to a **flat solo LINK** instead of a portrait (it shipped across every hub in
     The Inheritance; the build was green). Review each hit: a Lane-1 hub needs `npc = "npc_x"`; a Lane-2 ambient
     needs `trigger_mode = "random"` + `chance`; a deliberately presence-gated flat link is a rare, legitimate
     exception (confirm and move on). It **cannot** see a hub authored with NEITHER field — verify by content that
     every present-NPC surface has `npc` set. Full trap + engine trace: `references/toml-gotchas.md`.
   - **Cascade-order guard** — `python .claude/skills/author-game/scripts/check_cascade_order.py games/<slug>/toml_phases/7_final_game.toml`.
     Flags any node with a content block AFTER a `cascade` (or more than one `cascade`) — the silent trap where
     trailing prose renders **below** the reveal link (`[content][link][content][link]`) and two cascades
     duplicate the spliced exit link (both shipped green in Vesper's capstones). Fix: a `cascade` is the node's
     **last** content block; fold a bridge or a closing beat INTO it (an `advance_text` or terminal beat). Full
     contract + shape: `references/engine-reference.md` (the cascade section).
4. **Doctrine self-audit** — check each against what THIS beat authored (the in-skill `references/*.md`
   own each rule cited below):
   - **the beat serves a WANT** — name the desire-ladder rung it pursues; a beat
     whose only justification is "raises a meter" is grind — cut or reframe. If it's a **charged
     repeatable**, it also **deposits something the player SEES** this turn and carries a brake
     (`references/lanes.md` Lane 3).
   - **reachability triad** — the canvas fires only where NPC-schedule ∩ canvas-window ∩
     player-present-and-awake overlap.
   - **dead-presence / presence floor** — every scheduled NPC has a reachable hub at each **reachable**
     schedule row; no dead presence. **Offscreen** rows (`offscreen = true`) are exempt.
   - **cold-start / no backwards on-ramp** — every arc is enterable at corruption 0 / no flags, through
     ordinary presence; an arc's entry must NOT gate on a stat only raisable by that arc's own downstream
     content (a circular gate — e.g. a housemate arc gated on `worn_corruption`). First beat needs only
     co-presence; escalation layers after. The opening beat also has to NAME the setup in the prose —
     who the player is, who this person is to her, the tie between them, the hook — not lean on
     metadata, the Start/Customize copy, or a button label to carry it; a player reading only the story
     should grasp the premise from the page. Keep it RTS-flat: state the facts, don't ritualize them
     (`last_call` says "Sully's niece" in the cold open and stops there). And a repeatable NPC hub MUST sit
     behind a **dramatized auto-fire first-contact** that names the NPC and lands one hook (the
     `references/npc-intro.md` template, sets `<npc>_opened_up`) — a hub whose base node is the de-facto
     introduction is the forbidden cold-spawn (Late Shifts' Hank).
   - **double lock on lewd rungs** — every **lewd** rung gates on BOTH the
     **player-corruption door** (the cascade tier) AND **the NPC's own lock** (its built personal trait);
     **non-lewd interaction is ungated** (it builds the lock in Act 1). This is the "two-axis core gate"
     vocabulary, made universal. Don't gate a lewd rung on the door alone, or on the NPC lock alone.
   - **machine wiring — `cross_npc` / `economic` beats** — if this beat carries a
     cross-arc wire (it READS another arc's state, or routes income that gates reaching another arc), honor
     the arc's §8 wiring contract + the three disciplines: **D1** the cross-read gates a **mid/late rung or
     capstone, NEVER an arc's entry** (the on-ramp stays cold-start-enterable — same firewall as the
     cold-start bullet above); **D2** it reads *another* arc's signal (no mutual lock — the
     blueprint (Step 5 Pass 4) built + the Step-6 feedback confirmed the DAG); **D3** the gated rung is **locked-visible with
     `locked_text` naming the other arc's state** ("Sal
     won't go further while the bar's still in jeopardy"), never a silent lock. **Mechanism (real
     knobs only):** Form 1 milestone → read a shared **player flag** the source arc sets (`{type="flag",
     subject="player", flag_key="bar_seized", operator="is_true"}`); Form 1 "how far" → the **`<npc>_stage`
     player trait** (`{type="trait", subject="player", trait_key="<otherNpc>_stage", operator="gte",
     value=N}`); Form 2b banded payout → **one band-gated sibling `exit_block.choices` entry per band**, each
     with its own `conditions` (the band, `version="1.0"`) + its own literal-int money `effects`, banding on
     the **host** NPC's trait or a player-mirror trait (NEVER a foreign `{subject="npc", npc_id="npc_OTHER"}`
     read). No `value = f(trait)` exists; no `cross_wires` ledger field — use ordinary `deps`. (Form 3 — a
     finished arc *producing* income/capability — is **G6**, not yet authored.)
   - **reactive-world beats (archetype 10)** — a clothing-triggered ambient gates on
     **`worn_corruption` × place ceiling (per-canvas conditions) × NPC disposition**, NOT cascade meters,
     and is authored as Lane 2/3. **Clothing carve-out** (`references/systems.md`): clothing MAY trigger
     these ambient PUBLIC events but must **NEVER gate an NPC's escalation spine/arc**. The *forced* mode =
     an **auto-fire capstone-shape canvas** (`priority ≥ 9`, `is_repeatable = false`, single Continue, no
     refuse/accept branch — there is no zero-choice primitive), **act-scoped** (present early, gated off
     above a power tier); the *choice* mode = a normal refuse/accept exit block.
   - **sequenced auto-fire — band the stage** — if this beat is one of a chain of auto-fire capstones that
     must play IN ORDER, gate it on a strict **stage band** (`stage gte <prev>` AND `stage lt <this>`), not
     a lone threshold + "fires once". Auto-fire picks the **highest-priority** eligible canvas (one per
     location entry) and never consults your intended order, so an **ungated feeder** — which is the
     recommended on-ramp shape — can pump the spine odometer past a later capstone's threshold and fire it
     first. The Inheritance handed over the keys at stage 0, before the two beats that earn them; the build
     was green and the flag-chain validator passed, because it checks that setters exist, never that they
     fire in order.
   - **frontier** — beats beyond the current frontier are **telegraphed
     locked-visible seeds**, never silent gaps; the frontier beat does its three jobs (payoff · drop into
     steady-state · greyed next-hook) and its quest card narrates the frontier **honestly**, never blank.
   - **quest-card walkthrough line** — if this beat authored/advanced a card: the live rung's `goals[].label`
     names **place + person + verb (+ window)**; a meter-gated rung names its **feeder**; and the band the
     beat leaves behind cannot render blank (the Frame-3 trap — met numeric goal, no `ready_canvas`, not
     `terminal`). Owner: `references/quests.md` §3/§6.
   - **retire the standing surface on a terminal beat** — if this beat is a **terminal one-way turning
     point** (she's blown/flees, the mark is owned, the house falls), its setter flag is the audit key:
     sweep this NPC's *standing* surfaces — hub choices · Lane-2 ambients · Lane-3 walk-in/drain/work · schedule
     presence · the floor cluster — and gate each on that flag (close, `[group]`-swap, or **zone-seal the
     chokepoint** if the cluster is one location tree). A surface left running offers courtship to a man she
     owns / a hub for a man who fled. **Verify by simulation, not by memory:** set the terminal flag and
     confirm no pre-flip canvas is still eligible — there is no engine auto-retirement (eligibility is
     schedule + your conditions + repeatability, full stop) and the flag-chain validator can't see it,
     since `is_false` guards are exempt from its scan. The Inheritance applied this correctly to one NPC
     and forgot it on the apex, leaving a broken slave still "catching" the player at work.
     → `references/lanes.md` "Retire the standing surface on the terminal flag."
   - **endgame stays carnal** — a late/empire beat cashes out as
     **content**: a recruit is a **full new arc** (back through Step 4 story → Step 5 blueprint — own double-lock + capstone + loop), an
     "upgrade" / accumulation stage unlocks **new scene types** — ship the stage and the scene it opens in
     the **same** increment — the apex is the **hottest beats** — never a `+income` widget or
     a stat-bump. Support a **late-act pressure beat** (rival/cop/boss) so the squeeze never dies.
   - **late-act own pacing** — a **late-introduced** NPC carries a complete self-contained rung
     ladder; it can't borrow pacing from the (now-maxed) MC-corruption door.
   - **conquest-desire** — a conquest-target beat reads as **wanted-as-conquest** (hot pursuit +
     the target has agency: resists/schemes/cracks), not a cold instrument you merely *use*.
   - **navigable scarcity (the Dee-bug law)** — every scheduled window the player must reach sits in a
     day-phase the day-cycle can deliver them to; the sleep activity is the router.
   - **stat-restore infrastructure** — if `[engine.daily_tick]` drains a player stat, there's a recovery
     activity (sleep restores energy; mirror it for hygiene etc.) — not optional polish.
   - **locked-location unlock contract** — any NPC at a locked location is meetable at an open on-ramp and
     the unlock flag has a reachable setter (Cases A/B/C).
   - **system scoping** — the homes (`references/engine-reference.md`): clothing → `[settings]`, rent → `[settings.rent]`,
     phone + player-portrait → **top-level `[phone]` / `[player_portrait]`**. Never bare keys under `[time]`.
   - **optional-system doctrine** — if this beat wires clothing / rent / phone / customization / player-portrait,
     honor its signature trap (`references/systems.md`): clothing's **two-part rule** (triggers public reactive
     events; never gates an NPC arc spine; and it is **never enabled before an `initial = true` garment
     exists** — an empty catalog pins the portrait to naked from turn 0 and ships dead menus, so a
     clothing beat can't be marked validated with zero items, `references/clothing.md` §9); rent arms
     after an income flag; phone triggers can't use `day`/`time`/
     `location`/`random`; customizable names emit as `@`-tokens, never hardcoded; player-portrait `corruption` is a
     **LEVEL 0–4, not points** + outfit rules are first-match on the dominant garment (`dress||top||bottom`).
   - **`is_container` swallow** — no activity/ambient/capstone attached to a container location.
   - **engine-set flag gating** — the flag-chain validator accepts a flag as gate-satisfiable only if
     *something* sets it (incl. engine setters: the rent `eviction_flag` and `[engine.daily_tick]`
     `flagEffects op="set"`). The rent `eviction_flag` is the CORRECT "fell behind" signal — gate
     leverage/escalation on it, not a day-1 onboarding flag. `✗ NEVER SET` = a flag nothing sets, or a
     `daily_tick` flag only `unset`. Only `is_true` gates are checked; `is_false` guards exempt.
   - **Quests page reflects current goals** — if this beat is a trackable goal, a `[[quest_cards]]` shows it
     at the right time (and the prior milestone's card retires via its `when` gate). Never empty, never
     stale. If a label names the meter, it uses the sidebar's display name ("Corruption" / "<NPC> Relation"),
     never a raw key path — but naming the meter is optional garnish; the label's job is the walkthrough line
     (`quests.md` §3). Repeatable ambients/flavor: no card.
   - **legibility — the walkthrough line stays TRUE** — the **active** card's `goals[].label` (the surface
     both the page AND the `npc_panel` `next` row render) carries the next concrete action per the
     walkthrough standard (`quests.md` §3). A goal-only card with no place+verb fails this — **and so does
     one whose place+window no longer MATCHES the canvas's `location`/`schedules`.** A card naming last
     week's place is worse than a vague one: it sends the player somewhere real that's now wrong. Existence
     isn't enough; the copy has to still be true (`references/prose-truth.md`).
     **Cross-gated rung →** its locked-visible `locked_text` **names the gating arc's state**
     ("Sal won't go further while the bar's still in jeopardy" — the machine D3); a silent
     cross-lock is a soft-lock.
   - **lane coverage vs arc shape** — the NPC's content spans the lanes its shape calls for (not
     Lane-1-only), within the brief's budget, and EMPTY cells stay empty (peer/dating: no Lane 3; service:
     no Lane 2/3). The hub holds only NPC-object verbs; solo work/chores are their own canvases. Each Lane 3
     substitution canvas ships `substitution_only=true` + `max_triggers_per_day=1` + `is_repeatable=true` +
     a `location`. Hub base opener is one constant paragraph (not tiered).
   - **declared person (Rule 1)** — every `paragraph` / `thought_bubble` this beat wrote is in the game's
     `register.person` (read it from `authoring_state.json`; `dialog` blocks are exempt). **Run
     `references/rts-flat-prose.md` §7 check 1** — one grep. A mixed-person game is a reader-facing bug and
     nothing else in the pipeline catches it (`late_shifts` ships "He looks up when **you** come in" and
     "**She** says something about the shift" in the same file).
   - **dialogue carries character (Rule 4) — THE ONE WE ALWAYS FAIL** — for any beat where the player and an
     NPC actually interact, is the character built from what they *say* (`dialog` blocks — their voice, their
     refusals, their scheming) or narrated *about* (a summary of the exchange)? Play it. The flat register
     caps *density*, not speech — **RTS runs 0.73 narration words : 1 dialogue word across its whole corpus,
     and its deepest sex scenes are its MOST spoken.** Every game this skill has shipped inverts that
     (vesper 7.25:1 · the_inheritance 5.79:1 · late_shifts 15.04:1). **Target ≤ 1.5:1 on any scene with a
     present NPC; > 3:1 is a FAIL — run `references/rts-flat-prose.md` §7 check 3 and report the number at
     every milestone build.** **Push hardest at the hot beats:** a capstone,
     sex scene, or confrontation that narrates the encounter ("she asks, he answers") instead of voicing it
     is the single worst drift — those are the beats the player waited for, so play them, don't report them.
     Multi-party → each present NPC gets a line — short volleys, no monologues (`references/rts-flat-prose.md`
     Rule 4; `references/lanes.md` Voice register). EXEMPT only when **no one's
     actually there to speak**: solo activities, voyeur/peek where you're unseen, and the interior-monologue
     stretches of a capstone. An NPC who's *present* is not exempt — give them at least a line (a mood
     glimpse can be one terse spoken beat).
   - **per-beat density (Rule 2)** — each **beat** (not each block — a beat is often a `dialog` + a
     `paragraph`, and beat 0 includes the node's lead blocks) carries **~35–40 words**. **Over ~50 → SPLIT it
     into two beats, don't compress it.** The click is the fix. `references/rts-flat-prose.md` §7 check 2.
   - **tier = beat COUNT, not prose thickness (§5)** — a Lane-4 capstone runs **10–20 beats**; under 10 it's a
     Tier-2 ambient wearing a capstone's badge. A Lane-2 ambient over 9 beats will grate on the third
     re-read. RTS's biggest scene is 24 beats of ~25 words. Escalate by **adding beats**, never by fattening
     them.
   - **body yes, room no (Rule 3)** — did a scene body describe the *location*? Cut it; the location card
     already did that once. Did a hot beat carry **no body sensation**? That's under-written, not disciplined
     — RTS writes the body constantly ("Heat flares in your belly"), and body sensation encodes reluctance as
     readily as arousal.
   - **vocab ceiling honored** — explicit content sits at the NPC's declared per-tier ceiling (design brief);
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
     on the **player** tier — NOT an NPC walk-in (the player blueprint, `references/step-5-blueprint.md` Pass 1).
     Converse for NPC-track: a seduction capstone's player-corruption FLOOR is reachable from the feeder supply
     the player thread declares — tier-complete feeders before deep floors.
   - **spent resources gate via `costs`** — if this beat costs a resource (energy/hygiene/shift/chore), the
     spend goes in **`costs`** (trigger-level for a single-exit activity, per-choice for a multi-intensity
     exit, tiered under any `conditions` main-lock). `costs` GATES *and* deducts. NEVER spend via `effects
     {op=add, value=-N}` (decrements without gating → cosmetic meter), NEVER gate with `conditions` +
     `locked_text_threshold` (renders a clickable toast-button). `effects` carries only gains (money/relation)
     + `time_progression_minutes`; restores (sleep/shower) stay `effects`-positive.
   - **banded stats never leave their bands** — every `effects {op=add}` on a bounded banded stat
     (`energy`/`hygiene`/a custom `charge`/`coin`) carries `clamp=true` (a drop that could pass 0) or `cap=N`
     (a restore that could pass its ceiling). Unclamped, the value leaves its bands and the sidebar **card
     renders BLANK** — a *missing* HUD card, not a wrong number, so a quick playtest misses it
     (`references/trait-catalog.md` §4). Shipped twice in Vesper.
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
Active only when `[project].quests_engine = "v2"`. Authoritative schema + condition shape:
`references/engine-reference.md`. Design split: quests are narrative goals, the sidebar carries body-state
status (the quests-vs-sidebar split); the card shape follows the capstone/mechanic/hybrid modes.
- **Where they render:** no `npc_id` → top **"Story Goals"** (the spine); `npc_id` set → that NPC's section.
- **Fields:** `text` · `ready_text` · `tip` · `npc_id` · `priority` · `when` (routing — ALL must be true) ·
  `goals` (🎯 to-advance bullets) · `ready_canvas` (set → 🔓 Ready frame) · `terminal = true` (✓ complete).
- **Condition shape is FLAT** (no `type` discriminator): flag gate `{ flag = "x", op = "is_true" }`; trait
  gate `{ trait = "relation", subject = "npc", npc_id = "npc_x", op = "gte", value = 10, label = "X trust" }`.
- **Three modes:** *mechanic* (no `ready_canvas` — crossing a `goals` threshold IS the unlock); *capstone*
  (`ready_canvas` → Ready frame launches the one-shot); *terminal* (`terminal = true`).
- **Milestone chain:** one card per arc stage, each gated `when` the prior stage's flag is set and this
  stage's completion flag is not — so exactly one card shows per NPC at a time. The frontier card narrates
  the current peak honestly, never blank. *(One of two chain shapes — for an arc riding ONE climbing trait use a
  **stepped trait-band ladder** instead. The whole-page design (Story-Goals spine + per-NPC sections + end card),
  both ladder shapes, and the Frame-3-blank trap live in `references/quests.md`, designed at Step 5.)*
- **The walkthrough line rides `goals[].label`, not only `text`/`tip`.** The sidebar `next` row renders ONLY
  the goal block, so a step written only into `text`/`tip` vanishes from the sidebar; a **meter-gated** rung
  names its **feeder**. Mandatory — the standard (place + person + verb (+ window)), the gate-tell rule, and
  the blank-row trap are owned by `references/quests.md` §3/§6. A **cross-gated** rung (gated on another
  arc — the machine) is **locked-visible with `locked_text` naming the gating arc's state**; never a
  silent cross-lock.
- Author quest cards into the beat's `target_phase` (or `5_scenes.toml`), alongside its canvases.

## Cross-references
`references/run-mode.md` (the ask/inform + build-green discipline) · `references/step-5-blueprint.md` (the
blueprint this beat builds) · `references/step-4-deep-design.md` (the story behind it) ·
`references/content-framework.md` (the question set the blueprint was built against) ·
`references/trait-design.md` / `lanes.md` / `sex-loop.md` / `systems.md` / `toml-gotchas.md` ·
(the design rationale behind these self-audit lines — including the machine: cross_npc/economic wiring + the
D3 cross-gate telegraph).
