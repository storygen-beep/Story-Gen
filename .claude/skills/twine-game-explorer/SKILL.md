---
name: twine-game-explorer
description: Turn-based live-play toolkit for exploring browser-based Twine/SugarCube/Harlowe/Chapbook interactive fiction games. Claude drives the browser click-by-click via `scripts/live.js` — `start` → `peek` → `click` → `peek` → ... → `finalize`. Every command returns the new passage, variable diff, clickables, and a screenshot path Claude reads before deciding the next action. Unlike a DFS clicker, this respects that games have locations, stat gates, schedules, NPCs, and branching logic that require judgment, not enumeration. Sessions are fully resumable — saves/, notes.md, and the persistent Chromium profile survive across runs; re-running `start --slug <same>` (without `--fresh`) picks up where the last session left off. Use this skill whenever the user wants to play, analyze, map, explore, or understand an online browser-based interactive fiction game — even if they just paste a URL and say "figure out what this game does," "map the choices," or "analyze the mechanics." Keywords: *twine*, *sugarcube*, *harlowe*, *chapbook*, *interactive fiction*, *adventure game*, *explore this game*, *map the choices*, *analyze the mechanics*, *play through*, *generate a game report*, any pasted URL to a game.
---

# Twine Game Explorer

A **live-play toolkit** for analyzing browser-based interactive fiction games.

## The core idea

Games with real systems — locations, stat gates, NPC schedules, inventory, economy — can't be mapped by a brainless DFS clicker. A clicker can't tell Study is a self-loop that advances time without plot, or that the apartment upgrade arc is gated on $50 + completed work, or that Alice only appears on Saturdays. Claude drives the browser turn-by-turn: every command returns the new state + a screenshot path; Claude reads the PNG, decides the next action, invokes the next command.

## When to use

Trigger whenever a user wants to:
- Play and analyze an online Twine/SugarCube game
- Map branches, mechanics, NPCs, or the stat system
- Build a design-reference report from an existing game
- Resume exploration on a game we've partially mapped

## The loop

```
start [Phase 0 auto-runs]  →  peek  →  click  →  peek  →  click  →  ...  →  finalize
                                ↑                    ↓
                                └── screenshot + state + clickables ──┘
```

Every `peek` / `click` / `fill` / `eval` / `dom` command returns:
- `passage` + `state_hash`
- `variables_diff` — what moved since the previous state (`diff_full` on disk carries before/after values)
- `clickables` — visible, text-bearing interactive elements with bboxes
- `passage_body_text` / `passage_body_html` — the full rendered narrative of the current passage (no truncation). Claude can work off text and only fall back to the screenshot for coordinate-level detail.
- `modal_text` — the contents of `#ui-dialog` when a modal is layered over the passage (null otherwise)
- `screenshot` — absolute path Claude can `Read` when layout/coordinates matter. The `screenshots/live/` directory is automatically wiped on `finalize` (preserved on `stop`).
- `frontier_size`, `unique_states_seen`
- `ui_frame_hash`, `ui_map_path` — fingerprint + path to the Phase 0 UI map (see below)

## Phase 0 — UI recon (automatic)

On `start`, before returning control to Claude, the daemon runs a two-stage preamble:

**Phase 0a — Pre-game auto-advance.** Closes any SugarCube `#ui-dialog` modal (age disclaimers, etc.), clicks forward buttons (Play / Start / Continue / I understand / Accept / Next / Skip Intro), prefills name inputs with `"Player"` (override via `--name <str>`), and leaves preference radio/checkbox controls at defaults. Terminates when no clickable text matches any forward pattern — at which point Claude has the first real narrative passage loaded.

**Phase 0b — UI recon (six stages).**
1. **Scan regions** — structural + corner-sampling detection of every chrome region (sidebars, overlays, bars, floating widgets).
2. **Toggle candidates** — score elements that look like open/close triggers (aria-expanded, narrow edge strips, ≡/☰/◀/▶ glyphs, title="Toggle…").
3. **Probe toggles** — snap → click → diff → restore if stateful; reveal collapsed sidebars (`stowed` class) before cataloging.
4. **Catalog contents** — per region: interactive elements (buttons/links), heading-based cards OR flat `<a>` menu list, passive text samples.
5. **Probe chrome buttons** — for each safe chrome button: snap → click → screenshot → restore. Claude reads the screenshots in `ui_probes/<label>.png` to understand what each button reveals. Skip categories (never auto-probed):

   | Skip category | Examples |
   |---|---|
   | **Destructive** | Restart, New Game, Delete Save, Reset, Confirm Ending |
   | **Save mutations** | Save, Save Game, Quick Save, Save Slot |
   | **Exit** | Exit, Quit, Leave Game |
   | **External** | Discord, Patreon, SubscribeStar, Reddit, Twitter, Support, Feedback, Report a Bug — plus any `<a target="_blank">` or cross-origin href |

6. **Write artifact** — `ui_map.json` + `ui_probes/<label>.png` per probed button + seeds a `## UI frame` section in `notes.md`.

**Doctrine:** Before making any narrative click, read `ui_map.json` (path returned in every response as `ui_map_path`). Every chrome region, every safe chrome button, and what each reveals is already cataloged — don't re-probe manually. Use the catalog to inform strategy: location shortcuts, NPC rosters, visible stats, built-in walkthroughs/cheats, etc. are all inventoried before your first narrative turn.

**Flags on `start`:**
- `--skip-phase0` — disable Phase 0 entirely (fall back to the previous behavior)
- `--rerun-phase0` — force regeneration even if `ui_map.json` already exists on disk
- `--skip-buttons` — run Phase 0a + stages 1–4 only, skip Stage 5 button probing (faster)
- `--name "<str>"` — default for auto-filled name inputs (default `"Player"`)

**Manual re-run:** mid-session, `node $SKILL_DIR/scripts/live.js regions [--skip-buttons]` reruns Phase 0b on the current passage and refreshes `ui_map.json`. Useful after a major passage shift that may have changed the chrome frame.

**Resume behavior:** `start` without `--fresh` reuses an existing `ui_map.json` on disk (no re-probe) unless `--rerun-phase0` is passed.

**Crash safety:** Phase 0 failures are caught and logged to `live.log`; the session still starts with `ui_map: null`. The skill never blocks on Phase 0 going sideways.

## Phase 1 — Location mapping (Claude-driven, after Phase 0)

Not all games have explorable locations. If Phase 0 lands on a passage with only
narrative choices (no room/area destinations), skip Phase 1 and proceed to the
main exploration loop. Signs of a location-based game: a hub passage with 2+
destination clickables (room names, area names, image grid), or sidebar shortcuts
referencing locations ("Go to School").

### When to do this

After Phase 0 completes and you're on the first gameplay passage — before making
story decisions. Takes ~2-5 minutes.

### Step 1: Read Phase 0 data first

`ui_map.json` may already contain location data from the sidebar catalog:
- NPC names + current locations (sidebar "House" / "Characters" section)
- Location shortcut buttons ("Go to School", "Go to Park")
- Time/day display (relevant for NPC schedule tracking)

Don't re-discover what Phase 0 already captured.

### Step 2: Discover the hub

Look at the current passage's clickables. If there's a hub (multiple room/area
destinations from one passage), visit each room:

1. **Try text-click first** — `click "Kitchen"`. If it works, record `method: text`.
2. **If text fails** (common on image-grid hubs like RTS Hallway):
   ```bash
   node $SKILL_DIR/scripts/live.js eval "
     const out = [];
     for (const el of document.querySelectorAll('*')) {
       const cs = getComputedStyle(el);
       if (cs.cursor !== 'pointer' || cs.display === 'none') continue;
       const r = el.getBoundingClientRect();
       if (r.width < 80 || r.height < 80 || r.x < 316 || r.x > 1100) continue;
       const txt = (el.textContent || '').trim().slice(0, 40);
       if (txt) out.push({t: txt, x: Math.round(r.x + r.width/2), y: Math.round(r.y + r.height/2)});
     }
     return JSON.stringify(out);
   "
   ```
   Then `click --xy <x>,<y>` with the center coordinates. Record `method: xy <x>,<y>`.
3. **At each room, peek** — note available activities.
4. **Return to hub** — record the return text (e.g., "Hallway 🚪", "Go back").
5. **Record any gate messages** — if a click produces a toast ("You need school
   clothes!"), note the target + requirement in the Gates table.

### Step 3: Track NPC schedules (if sidebar shows NPC positions)

After visiting rooms, advance time (Study / Nap / Sleep) and re-check sidebar
NPC locations. Two observations at different times reveals the schedule pattern.

### notes.md template

Add after the `## UI frame` section:

```
## Locations
| Location | Passage | Nav from | Click method | Return via | Activities |
|---|---|---|---|---|---|

## Gates
| Target | Message | Requirement | Resolved? |
|---|---|---|---|

## NPC schedules (if sidebar tracks NPCs)
| NPC | Early Morning | Morning | Afternoon | Evening | Night |
|---|---|---|---|---|---|
```

### What NOT to map as locations

- **Action passages** (Study, Nap, Sleep) — timed activities that return to hub.
  Record them as activities OF a location, not as separate locations.
- **Event passages** (NPC encounters triggered by location + time) — one-time or
  conditional. Note in NPC schedule, not location table.
- **Transition passages** (intro1 → intro2) — pre-game. Already handled by Phase 0a.

## Phase 2 — Read the game's quest/hint system (Claude-driven, after Phase 1)

Some games provide built-in progression guidance — quest journals, walkthroughs,
hint systems, or objective trackers. Phase 0 already screenshotted these buttons
in `ui_probes/`. If the game has them, read them BEFORE exploring blindly.

### How to use

1. **Check `ui_probes/` for Quests, Walkthrough, Guide, or Hints screenshots.**
   Read the screenshot to understand starting objectives. Not all games have
   these — if none exist, skip Phase 2.

2. **Extract actionable hints from quest text.** Quest descriptions contain
   location names, resource requirements, and NPC references:
   - "I should get a job, maybe at the restaurant?" → restaurant is a location,
     money is the resource, find the restaurant during Phase 1
   - "First Day of School" → school is a key location, attend it
   - "Talk to Alice at the park on Saturday" → park location, Saturday schedule

3. **Check the sidebar.** Many games show the current active quest inline in the
   sidebar on every passage (visible in every screenshot). RTS shows
   `🎯 Quest / I Need Money / ...` — this updates as quests advance.

4. **Record starting objectives in notes.md:**

```
## Active quests
| Quest | Objective | Hints from text | Status |
|---|---|---|---|
```

### During play: re-check after progress

Quests update as you advance. After major events (new NPC met, new location
found, item acquired, time advanced significantly), glance at the sidebar quest
text in the screenshot. If objectives changed or new quests appeared, update the
Active quests table in notes.md and adjust your exploration strategy.

## Phase 3 — Navigation intelligence (on-demand, when stuck on gates)

Phases 0–2 give you the chrome map, the location map, and the quest hints.
Phase 3 adds a fourth source of truth: a **static analysis of the entire
game's passage graph**, computed once at daemon startup from
`passage_catalog.json` → `static_graph.json` + `variable_index.json`. Four
read-only endpoints consult this data in memory so you can plan before
clicking — no exploration cost, no mutation of game state.

**When to reach for it.** Don't use these on every turn. Use them when:
- You've hit a gate (click refused, passage unchanged) and you want to know
  *why* and *what to change* — `requirements <target>`.
- You want to get somewhere specific without exploring the whole tree —
  `path <target>`.
- You've just entered a location hub and want to see what's open vs.
  gate-blocked before clicking blindly — `reachable`.
- You want to understand a mechanic — `setters <var>` enumerates every
  source of change for a single variable.

### `path <target_passage>`

Shortest click chain from the current passage to `<target>`, with every
enclosing `<<if>>` gate evaluated against the current variable state.

```bash
node $SKILL_DIR/scripts/live.js path "Wardrobe"
# → 3 steps: RING RING RING RING → Get out of bed → Wardrobe.
#   All gates satisfied.
```

If a gate is failing, you get back an actionable hint instead of a
raw miss:

```bash
node $SKILL_DIR/scripts/live.js path "School"
# → No path from dream1 to School — blocked by gates.
#   Use `requirements School` to see what's needed, or
#   `path School --ignore-gates` to see the gated path.
```

Flags:
- `--ignore-gates` — return shortest path regardless of satisfiability
- `--max-hops N` — bound the BFS (default 20, capped at 50)

Default gate policy is `allow_unknown`: edges with fully-satisfied gates
are traversed; edges where the gate evaluates false are skipped; edges
where the evaluator returns `'unknown'` (expression too complex) are
traversed — treated as possibly-satisfiable rather than assumed
false-negative.

### `requirements <target_passage>`

For every blocking gate on the path to `<target>`, extract the variables
it references, look them up in `variable_index.json`, and surface setter
passages with reachability from the current state. Setters whose
`value_expr` matches the gate's desired value (from `==` / `eq` clauses)
are tagged `✓ matches gate` and sorted first.

```bash
node $SKILL_DIR/scripts/live.js requirements "School"
# → School is NOT currently reachable. Path length 7, 2 blocking gates:
#     step 6 (Living room → Jecinda District): !($dayCount==2 and ...)
#       $PlayerClothes (currently "Casual", wants "SchoolUni" or "SchoolUniSlutty")
#         setter: Wardrobe (= "SchoolUni") [✓ matches gate, 3 clicks].
#     step 7 (Jecinda District → School): !(($weekDay eq false) || ...)
#       $weekDay (currently true, wants false) — 2 setter(s), none reachable now.
```

Use the `✓ matches gate` setter first — its path_to_setter is the
concrete action sequence. Other setters are fallbacks (e.g. a different
passage that also writes the same value).

### `reachable [hops]`

From the current passage, partition every passage reachable within N hops
(default 5, capped at 15) into three buckets:

- **`open`** — gate-free or currently-satisfied, you can click there now
- **`gated_satisfiable`** — gate evaluator couldn't decide; may or may
  not be satisfiable
- **`gated_blocked`** — gate evaluates false under current variables

```bash
node $SKILL_DIR/scripts/live.js reachable 5
# → { open_count: 7, gated_satisfiable_count: 0, gated_blocked_count: 2,
#     open: [...], gated_blocked: [
#       { passage: "Weekly Allowance",
#         blocking_gate: "$day==7 and $weeklyAllowanceCheck==false and ...",
#         variables_involved: {...} },
#       { passage: "Sleep", blocking_gate: "!($dayCount ==2 and $hour lt 13)", ... }
#     ]}
```

### `setters <variable>`

Direct lookup into `variable_index.json`. Lists every passage that
`<<set>>`s or `<<unset>>`s the variable plus every wiki-link edge that
does so. Accepts the var name with or without `$` prefix — `setters
PlayerClothes` is equivalent to `setters '$PlayerClothes'`.

```bash
node $SKILL_DIR/scripts/live.js setters '$PlayerClothes'
# → 13 setters including:
#     Wardrobe (= "SchoolUni"), Wardrobe (= "Casual"),
#     Living room (= "Casual"), Gym Locker Room (= "Gym"), ...
```

### Phase 3 limitations — know before you trust

- **Parser coverage is partial.** `variable_index.json`'s
  `indexing_coverage` field reports `"partial"` when `<<script>>` blocks,
  widget bodies, or method-call setters (`.push()` / `.delete()`) were
  skipped. Those setters exist but aren't in the index. For mechanics
  that mutate state via JS, Claude still has to observe the runtime diff.
- **Gate evaluator handles common forms only.** Comparison operators
  (including SugarCube's `eq`/`lt`/`gte` word aliases), boolean
  combinators, parenthesization, and negation — covers the vast majority
  of gates in the wild. Complex expressions (method calls, ternary,
  arithmetic on the LHS) evaluate to `'unknown'`; pathfinder still
  traverses them, and the raw condition string comes back in the
  response so you can read it yourself.
- **Chrome / sidebar buttons are NOT in the graph.** Phase 0's
  `ui_map.json` catalogs sidebar affordances separately. If a game lets
  you open the wardrobe via a sidebar button, pathfinder only sees the
  in-world path (Bedroom → Wardrobe). Check `ui_map.json` too.
- **Dynamic targets** (`<<goto $dest>>`) can't be resolved statically
  and are omitted — pathfinder won't route through them.
- **Temp variables** (`_var`) reset every render, so their
  "initial_value" in the index is usually missing. Treat them as
  observe-only.

## Workflow

### 1. Start a session

```bash
node $SKILL_DIR/scripts/live.js start \
  --url https://mopoga.com/<game-slug> \
  --slug <game_folder_name> \
  --fresh
```

`start` forks a detached daemon (Playwright + Detector + Frontier in memory),
runs portal entry via `setup.js::doSetup`, and returns the initial engine
state + screenshot + clickables. The lockfile at
`game_explorations/<slug>/.live/daemon.json` tracks the port; every
subsequent command discovers it automatically.

- `--fresh` archives the whole slug directory (notes, play_log, saves/, **and** the Chromium profile) to `archive/<timestamp>/`. Use this to start a clean playthrough from scratch.
- Omit `--fresh` to **reopen the same Chromium profile** — `notes.md` and `play_log.jsonl` from past sessions are preserved on disk, and the response's `resumed_from_prior` block reports how much prior activity exists. **Note:** reopening the profile does not by itself restore the in-game state — SugarCube saves live in the profile's localStorage, but the game still boots to its title screen. See "Resuming a prior playthrough" below.
- `--idle-ms` overrides the 30-minute idle timeout (ms).
- `--headless` runs Chromium headless.

### 1a. Resuming a prior playthrough

Reopening the Chromium profile (omitting `--fresh`) is necessary but not sufficient — you also need an in-game save slot to restore from. The round-trip is:

1. **Before ending a session**, click the game's own in-sidebar Save Game button (typical SugarCube sidebar; text varies per game). This writes a slot into localStorage.
2. Then `stop` (or `finalize` if you also want the report) — either preserves the profile.
3. On the next `start --slug <same>` (no `--fresh`), the daemon lands on the game's title screen. **Check the first screenshot.** If `resumed_from_prior.prior_sessions > 0` and you see a save-load affordance (e.g. `Load`, `Continue`, `Continue Latest Save`, `Resume`, or a slot list), click it to restore — do not click `Play` / `New Game` / `Skip Intro`, which overwrite the save with a fresh playthrough.
4. If there's no such button, there's no save to resume from; start normally.

If the user didn't click Save Game before the prior session ended, there is nothing to restore — only `notes.md` / `play_log.jsonl` survive, which give you context but not game state.

### 2. Observe

Look at the `screenshot` field in the response, `Read` the PNG. Note:
- What passage is this?
- Which clickables are real story choices vs. sidebar/menu?
- Is there a modal overlay (age gate, name input, dialog)?
- Does the sidebar show quest/objective text? Has it changed since last check?
  If a new quest appeared or an objective updated, note it and adjust strategy.

### 3. Decide, click, repeat

```bash
# Text click — the normal case:
node $SKILL_DIR/scripts/live.js click "Start the story"

# When text selector fails (div-with-onclick, custom components):
node $SKILL_DIR/scripts/live.js dom --filter Continue
# → inspect the tag/class/bbox of the actual Continue element
node $SKILL_DIR/scripts/live.js click --selector "div.continue-btn"

# Or fall back to coord click:
node $SKILL_DIR/scripts/live.js click --xy 560,190

# Keyboard for modals that accept Enter:
node $SKILL_DIR/scripts/live.js keys Enter
```

After every click, the response already includes the new state — no separate
`peek` needed.

### 3a. Plan before clicking when you know where you want to go

If you have a concrete target (a specific passage, location, or quest
objective) and don't want to explore blindly, reach for the Phase 3
navigation-intelligence endpoints:

```bash
# "Can I get to Wardrobe from here?"
node $SKILL_DIR/scripts/live.js path "Wardrobe"

# "Why can't I enter School yet?"
node $SKILL_DIR/scripts/live.js requirements "School"

# "What's open right now within 3 hops?"
node $SKILL_DIR/scripts/live.js reachable 3
```

See the **Phase 3 — Navigation intelligence** section above for the full
reference. These endpoints are read-only (no clicks, no state mutation)
and return data synthesized from the static passage graph + variable
setter index — they don't replace `peek`/`click`, they tell you which
clicks are worth making.

### 4. Capture snapshots before branching

When you hit a decision point with N ≥ 2 real options:

```bash
node $SKILL_DIR/scripts/live.js snap --note "at apartment kitchen choice"
# → returns snap_id, e.g. "s1a2b3c4d5"

node $SKILL_DIR/scripts/live.js click "Go to work"
# ... explore a branch ...

# Come back:
node $SKILL_DIR/scripts/live.js restore s1a2b3c4d5

# Take the other option:
node $SKILL_DIR/scripts/live.js click "Stay home"
```

For systematic DFS, use the frontier queue:

```bash
node $SKILL_DIR/scripts/live.js frontier push "Stay home" "Call Alice"
node $SKILL_DIR/scripts/live.js click "Go to work"
# ... later ...
node $SKILL_DIR/scripts/live.js frontier pop   # restores + advances
```

### 5. Record observations

```bash
node $SKILL_DIR/scripts/live.js note "LOVE is per-NPC — love.alice, love.bob"
node $SKILL_DIR/scripts/live.js note "Money gate at \$50 blocks the apartment upgrade"
node $SKILL_DIR/scripts/live.js note "Study is a self-loop: advances time, no plot"
```

Notes go to `game_explorations/<slug>/notes.md` with timestamps. These are the
primary research artifact — more valuable than any auto-generated report for
understanding how the game actually plays.

### 6. Finalize

```bash
node $SKILL_DIR/scripts/live.js finalize
```

Writes the report artifacts: `report.md`, `mechanics.md`, `coverage.md`,
`variable_profile.json`, `variable_schema.json`, `npcs.json`, `items.json`,
`body_changes.json`, `scene_catalog.json`. Closes the browser, cleans the
lockfile, exits the daemon. `notes.md`, `play_log.jsonl`, `saves/`, and the
Chromium profile stay on disk for resume.

If you want to resume this playthrough in a future session, click the in-game Save Game button **before** `finalize` — otherwise only notes/log survive, not game state.

### 7. If you need to step away

```bash
node $SKILL_DIR/scripts/live.js stop
```

Clean shutdown without running the report. Everything is still on disk.
Re-running `start --slug <same>` (no `--fresh`) reopens the same Chromium
profile and surfaces past session activity in the response.

Same caveat as `finalize`: save in-game first if you want to resume the actual playthrough; otherwise only research artifacts persist.

## Breaking loose when stuck

The live CLI exposes escape hatches a scripted clicker can't use. Reach for these in order when a click misses or a passage stalls.

### Text click failed — selector is wrong

```bash
node $SKILL_DIR/scripts/live.js dom --filter Continue
# Shows every element whose text matches /Continue/i with tag, class, bbox.
# If it's a <div onclick>, fall back:

node $SKILL_DIR/scripts/live.js click --selector "div.dialog-btn"
node $SKILL_DIR/scripts/live.js click --xy 610,206
```

### Passage is stuck, nothing advances it

```bash
node $SKILL_DIR/scripts/live.js keys Enter         # try Enter first
node $SKILL_DIR/scripts/live.js eval "SugarCube.Engine.play('ApartmentKitchen')"
node $SKILL_DIR/scripts/live.js eval "SugarCube.State.variables.disclaimer_accepted = true; SugarCube.Engine.show();"
node $SKILL_DIR/scripts/live.js reload             # nuclear: re-run setup
```

### Same passage repeats (self-loop)

Don't click it again. Restore an earlier snapshot, or pop the frontier to try a different branch.

```bash
node $SKILL_DIR/scripts/live.js restore <snap_id_from_before_loop>
node $SKILL_DIR/scripts/live.js frontier pop
```

Then `note` the self-loop so we don't fall into it again.

### Name / avatar prompt mid-story

```bash
node $SKILL_DIR/scripts/live.js fill --index 0 --value "Player"
node $SKILL_DIR/scripts/live.js fill --index 1 --value "Smith"
node $SKILL_DIR/scripts/live.js click "Confirm"
```

### Icon-font glyphs

If `clickables` contains items with `icon_only: true`, those are Private-Use-Area unicode (U+E000–U+F8FF) — icon-font nav arrows. Ignore them; they create infinite loops.

## Toolkit reference

All modules live under `scripts/lib/`. `scripts/live.js` imports them via explicit paths.

- **`engine.js`** — `introspect(frame)` returns `{engine, passage, variables, saveCaps}`. `snapshot(frame)` captures state; `restore(page, frame, snap)` restores. Primary mode is SugarCube's `State.marshalForSave`/`State.unmarshalForSave` (bypasses Save API rejection). Falls back to `Save.serialize`/`Save.deserialize` with progressive guard bypass.
- **`state.js`** — `hashState({passage, variables})` for dedup. `diffVariables(before, after)` returns `{added, removed, changed}`.
- **`setup.js`** — `doSetup(page, context, {url})` returns the game's iframe. Handles portal-entry (mopoga, generic), age disclaimers, minimal name-input prefill.
- **`detector.js`** — `new Detector()` + `observeState()` + `observeChoice()`. Profiles variables statistically (ranges, mutation counts, co-change edges, name-prefix clusters) without applying semantic labels.
- **`labeler.js`** — `labelProfile(profile)` applies semantic labels (npc_stat, body, player_stat, time, flag, item) with confidence ratings. Runs inside `report.write()`.
- **`frontier.js`** — `new Frontier(file)` is a persistent DFS queue. Append-only JSONL with compact-on-load.
- **`session.js`** — `new SessionTracker(dir)` + `aggregateSessions(dir)`. Per-run metrics + cross-run rollup.
- **`report.js`** — `write(outDir, detector, frontier, exploredCount, sessionsSummary, meta)` generates all human-readable artifacts.
- **`choices.js`** — `listInteractive(frame)` returns every visible clickable with text+bbox+tag.
- **`passage_catalog.js`** — `dumpCatalog(frame)` enumerates `Story.passages` (and `<tw-passagedata>` fallback) with tags + raw Twine source; written once at daemon start.
- **`static_graph.js`** — `buildStaticGraph(catalog)` walks the catalog and parses every `[[link]]`, `<<link>>`, `<<goto>>`, `<<return>>`, `<<include>>` into a graph of navigation edges, each tagged with the enclosing `<<if>>` gate stack.
- **`variable_index.js`** — `buildVariableIndex(catalog, staticGraph, initialState)` parses `<<set>>` / `<<unset>>` from passage bodies (and wiki-link setter suffixes on edges) into a per-variable lookup: initial_value + setter list (passage, op, value_expr, gate) + unsetter list. `indexing_coverage` flags when `<<script>>` blocks / widget bodies / method-call setters were skipped. (M6.1)
- **`gate_eval.js`** — `evaluateGate(condition, variables)` parses an `<<if>>` condition and returns `true` / `false` / `'unknown'` plus every `$var`/`_var` it references with current values. Handles JS operators (`===`, `==`, `&&`, `||`, `!`), SugarCube word operators (`eq`, `neq`, `lt`, `gt`, `lte`, `gte`, `and`, `or`, `not`), parens, nested negation. (M6.2)
- **`pathfinder.js`** — `buildContext(staticGraph, variableIndex)` → reusable BFS context. `findPath` / `computeRequirements` / `reachableFrom` / `lookupSetters` power the four navigation-intelligence endpoints. Three gate policies: `strict` (only TRUE gates), `allow_unknown` (default), `ignore`. Requirements automatically ranks setters by "matches gate target" + reachability. (M6.2)
- **`portal_adapters/`** — per-host entry recipes. `mopoga.js` handles mopoga.com's "PLAY" button. `generic.js` is the fallback. Add `<host>.js` for new portals.

## Output directory structure

Every session writes to `game_explorations/<slug>/`:

```
<slug>/
├── .live/
│   └── daemon.json           running-daemon lockfile (deleted on stop/finalize)
├── notes.md                  append-only research notes (Claude's observations; Phase 0 seeds a UI-frame section)
├── play_log.jsonl            one line per command: {ts, cmd, args, passage, state_hash}
├── pregame_auto_advance.jsonl  Phase 0a trail: each modal dismissed / forward button clicked
├── ui_map.json               Phase 0b artifact: regions, contents, chrome-button probes
├── ui_probes/                Phase 0b screenshots — one per probed chrome button (durable — kept across finalize)
│   └── <label>.png
├── live.log                  daemon log
├── session.log               cross-session log
├── report.md                 human-readable synthesis (regenerated by finalize)
├── mechanics.md              design patterns observed
├── coverage.md               exploration progress
├── variable_profile.json     raw statistical evidence, no labels
├── variable_schema.json      labeled variables + confidence
├── npcs.json                 per-NPC stats + scenes
├── items.json                detected items
├── body_changes.json         body/appearance transitions
├── scene_catalog.json        every unique passage + visit counts
├── state_timeline.jsonl      per-observation records: hash, passage, kind, diff_full {before/after}
├── sessions/                 per-session metadata (timing, clicks, completion)
│
│ ── Text-capture pipeline (M1 + M2 + M3 + M4) ──
├── initial_state.json        pristine variables + body_text captured BEFORE Phase 0a mutates state
├── passage_catalog.json      every `Story.passages` entry with tags + raw Twine source (one-shot, at start)
├── scene_bodies.jsonl        one line per unique (passage, variables) hash — full body_text + body_html + variables snapshot (no truncation)
├── engine_config.json        SugarCube Config/Setting/version/save-caps + State.history shape + Story IFID
├── static_graph.json         every navigation edge parsed from passage source — wiki, <<link>>, <<goto>>, <<return>>, <<include>> — with gate stacks (written at startup as of M6.1, consulted live by path/requirements/reachable)
├── variable_index.json       every $var / _var → passages that <<set>>/<<unset>> it (passage-body + wiki-link edge setters), with enclosing <<if>> gates and initial values (M6.1)
├── choice_graph.json         observed edges aggregated from play_log + state_timeline, with effect_aggregate per variable and coverage vs static_graph
├── sidebar_snapshots.jsonl   sidebar/chrome panel content captures: phase0_probe, baseline, passive_change, manual_regions; each line carries panel innerText + structured interactive elements
│
├── saves/
│   ├── frontier.jsonl        DFS queue (persistent across runs)
│   ├── explored_hashes.txt   state dedup set
│   ├── detector_snapshot.json  periodic detector serialization
│   └── snapshots/<id>.json   engine snapshots saved via `snap`
├── screenshots/
│   └── live/                 one per live-play command — auto-deleted on `finalize` (preserved on `stop`)
├── profile/                  persistent browser profile (cookies, localStorage)
└── archive/                  prior runs, stashed by `start --fresh`
```

## Legacy generic explorer (kept for DOM probes)

`scripts/explore.js` and `scripts/lib/classifiers/v2_behavioral.js` were the
original driver before live-play existed. They remain usable for a one-shot
60-second DOM recon:

```bash
node $SKILL_DIR/scripts/explore.js --url <URL> --name <slug> --budget-ms 60000 --fresh
```

Live-play is strictly better for actual exploration.

## Setup (first time)

```bash
cd $SKILL_DIR
npm install
```

Installs `playwright`. The Chromium binary downloads on first `launch()`
(~300 MB). If the daemon fails with "executable not found," run
`npx playwright install chromium`.

## Content note

The skill is engine-agnostic and runs against any Twine-family game, including
adult ones. The capture pipeline records **everything textual** the engine
exposes — rendered passage bodies, raw passage source, widget definitions,
Story JS/CSS, engine config, settings, sidebar panel contents, static + dynamic
choice graphs — so downstream analysis or comparison against other games can
work off structured data rather than screenshots.

Two things the pipeline deliberately does NOT capture:
- `<img>` / `<video>` / `<audio>` asset URLs referenced by passages (media
  inventory is out of scope).
- Any network traffic — these are HTML-only games and the browser already
  has everything loaded locally.

Per-turn screenshots under `screenshots/live/` are only Claude's in-session
feedback loop; they're automatically deleted on `finalize`. Phase-0 chrome-
button screenshots under `ui_probes/` and scene-tagged screenshots remain
alongside their structured-text siblings in `sidebar_snapshots.jsonl` and
`scene_bodies.jsonl` respectively.
