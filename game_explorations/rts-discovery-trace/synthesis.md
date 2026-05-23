# RTS Discovery & Unlock Patterns — Focused Session Synthesis

**Captured:** 2026-05-04
**URL:** https://mopoga.com/road-to-success
**Method:** Live play via twine-game-explorer skill, two passes:
- Pass 1 (Day 1 cold start): unlock surfaces survey, walkthrough+gallery+quests catalog
- Pass 2 (eval-bumped stats, 2-day progression): drove Brother arc through random encounter to full scene completion (PeepBrotherSex), watched walkthrough STATUS flip 🔒 → ✅ in real time

**Prior sessions referenced:** `road-to-success` (deep map), `rts-arc-trace` (cross-arc structural)

This session targets the discovery/unlock UX questions that surfaced from TLS Pattern 2 work — specifically the "where do I tease and do chores" / "Frank bookkeeping appeared from nowhere" complaints. The earlier two sessions captured *what* RTS does structurally; this one captures *how the player encounters new content moment-to-moment*.

## TL;DR

RTS solves discovery with **two parallel surfaces** (in-fiction + meta) and **three notify-fail tiers**. New activities never literally "appear from nowhere" — they were always pre-declared in the walkthrough; the player just hadn't met the prerequisite. The world updates silently around the player; no popups. NPC absences are explicitly explained, not silently empty.

## The two discovery surfaces

### Surface 1 — In-fiction (room buttons, NPC presence)

- **Room buttons are stable.** Same activity name across all stat tiers. "Play videogames" at corruption 0 fires a utility one-liner ("You are playing a game on the console..."); same button at corruption 10 + Stepbrother arousal 🔥🔥 fires a Stepbrother scene. Button label does NOT change between tiers.
- **NPC absence = narrated.** Visiting Stepbrother's Bedroom while he's at school shows: *"Your Stepbrother is at school"* + Hallway return. Empty rooms are NEVER silently empty. Player learns the NPC has a schedule.
- **Sidebar tracks NPC location continuously.** The right sidebar shows every NPC's current location in real-time, refreshed after every action. Player who wants to interact with NPC X just looks at sidebar → goes there.
- **Gated affordances stay visible with ❌ label.** Day 1 EM Bedroom shows: Study, ❌ Too early to sleep ❌, Nap, Wardrobe. The gated Sleep option is rendered AS A BUTTON with ❌ markers — player learns Sleep exists from Day 1 without clicking and failing.

### Surface 2 — Meta (Walkthrough + Quest Journal)

- **Walkthrough is the encyclopedia.** From Day 1, the Walkthrough page lists EVERY NPC + EVERY LOCATION with scene counts ("Stepbrother — 15 scenes", "Marcus — 5 scenes", "Park — 9 scenes"). Player can drill into each.
- **Each NPC's scene table is the planning UI.** Columns: `SCENE / NPC / REQUIREMENTS (NPC) / REQUIREMENTS (MC) / CHANCE / GUIDE / STATUS`.
  - Locked rows display with `🔒 Locked` STATUS but the row is still visible.
  - GUIDE column is concrete prose: *"Take the test and get at least an 8 grade"* / *"Have at least 15 relationship points with Marcus, wait for his invite and go to the date with him"* / *"Play videogame at your living room while being pregnant"*.
  - REQUIREMENTS columns are numeric (Corruption: 30) or emoji-tier (Arousal: 🔥🔥) or None.
- **Quest Journal is task-level.** Modal opened via sidebar `📜 Quests` button. Lists current objectives ("First Day Of School" / "I Need Money") with descriptions and "Pin to Sidebar" actions. Updates as quests advance. Doesn't list scenes — that's walkthrough's job.

The two surfaces do different work:
| Surface | Scope | When the player consults it |
|---|---|---|
| Walkthrough | Every scene with prereqs | "What can I unlock with NPC X?" / "Where do I raise corruption?" |
| Quest Journal | Top-of-mind goals | "What should I be doing right now?" |
| Room buttons | Current-location options | Moment-to-moment "what can I do here" |
| Sidebar NPC list | Current NPC locations | "Where is X right now?" |

## The three notify-fail tiers

| Tier | UX | Use case | Example |
|---|---|---|---|
| **Visible-disabled label** | Button rendered with ❌ markers around its label, in the room button list | Soft-known-blocked: option exists but trivially gated by time/state | `❌ Too early to sleep ❌` in Day 1 EM Bedroom |
| **Transient toast** | Short toast at top of screen on click; passage doesn't change | Click-and-learned: option is reachable but needs a state precondition | Click "🏫 Go to School" in casual outfit → toast "You need to wear school clothes to go there!" |
| **Modal page with explanation + path** | Click leads to a dedicated page that names the gate and offers the upgrade route | Hard fundamental gate (paywall, plot lock) | Click "👾 Cheats" → page reads "Cheats are only for Patreons / Become a Patreon / Return ↩️" |

The graduation matters: trivial state gates use the lightest UI (label-prefix); preference/prep gates use transient feedback (toast); fundamental hard gates use a full page with the upgrade path. Player never gets a silent no-op + confused.

## How a new activity actually "appears" (revised after Pass 2)

RTS has **four appearance vectors**, all silent in the moment. The differential — the player walking into a familiar room and noticing the button set is denser than last time — IS the unlock notification.

1. **In-context button injection at the location passage.** The biggest one. After Pass 2 progressed Brother arc to corruption 31 + Brother arousal 🔥🔥 + Brother corruption 15 + relation 10, visiting `BrotherBedroom` at evening rendered FOUR new buttons in the same passage that previously showed only "is not in his bedroom" + Hallway return: **Talk with him 🗣️ / Tease him ❤️‍🔥 / Flash to him ❤️‍🔥 / Have sex with him 🔥**. Zero notification. Same `BrotherBedroom` passage. The location-passage walks the NPC's scene table at render time and emits a button per scene whose requirements are met (and whose chance is 100%). The player notices the room is "denser" and that's the discovery moment.

2. **Random-encounter passage override at navigation time.** PeepBrotherSex fired on room entry as a 25%-chance random encounter — INSTEAD OF the normal `BrotherBedroom` render. Not a button addition; a passage substitution. Player clicks BrotherBedroom tile → dice roll → either normal room or encounter scene takes over. The encounter scene drips out via linkreplace.

3. **Time/schedule world-flag flips.** Many `location.X.open` flags flipped after a single Nap (location.church.open, location.movieTheater.open) and after a Sleep night-rollover (location.gym.open, location.mall.open, etc.). Some use a `location.X.opensAt` field with day-relative countdown phrasing ("Tomorrow (Afternoon)" → "Afternoon" → eventually `open=true`). All silent — player sees the new tile next time they enter the city zone.

4. **Disabled→enabled label flip in the same passage.** `❌ Too early to sleep ❌` button became `Sleep 💤` silently when time hit Night. No animation, no toast, just the label changed. Player notices on next button-list scan.

**There's also a fifth (refined) — first-encounter scripted intro.** The game changelog v0.25 line confirms: *"Meeting Natasha for the first time in the school library is now a short intro scene before regular chats unlock."* So FIRST encounters with named NPCs CAN get a scripted intro vignette; subsequent visits drop into the normal scene-table flow. RTS uses scripted intros sparingly, primarily for new-NPC reveal moments — most other unlocks are silent.

Combined with the walkthrough's pre-declaration, the perception is: *"Oh right, I knew that scene existed — now I can finally do it."* Not: *"Where did this come from?"*

## What walkthrough STATUS actually means (revised after Pass 2)

**STATUS = scene completion tracker.** When a scene is played through to its final passage / climax / payoff choice, the engine writes `npc.<NPC>.scenes.<SceneId>.unlocked = true` and the walkthrough STATUS column flips from `🔒 Locked` to `✅ Unlocked`. Verified directly: `npc.Brother.scenes.PeepBrotherSex.unlocked: false → true` at the climax click of the linkreplace drip.

REQUIREMENTS columns + GUIDE column tell the player HOW to unlock; STATUS tells them WHICH they've completed.

Two corollaries:
- The walkthrough is a **scene catalog with achievement tracking**, not a real-time gate display. Even when player meets all requirements, scene shows 🔒 until played to completion.
- **Walkthrough requirements are SOFT for ATTEMPTS but HARD for COMPLETION-CREDIT.** I clicked "Sleep with him 💤" with one requirement unmet (Brother corruption 0 vs needed 10) — got a soft cuddle vignette ("snuggling close to his sleeping form" → "Go to your bedroom and sleep") that didn't count toward STATUS. The next time, with all requirements met, the FULL scene fires through to climax and flips STATUS. Players can attempt scenes with partial prereqs and see fall-through alt content; they get the canonical scene + completion credit only when all reqs are met.

## Linkreplace-drip pattern (confirmed on PeepBrotherSex)

Single passage (`PeepBrotherSex`), 4-step in-place reveal:
1. **Peep** — initial paragraph + video. Choice: Peep / Hallway return.
2. Click Peep → paragraph appended ("Heat flares in your belly..."), video URL swapped, choice replaced with **Stroke your pussy / Hallway**.
3. Click Stroke → paragraph appended, video swapped, choice replaced with **Masturbate / Hallway**.
4. Click Masturbate → paragraph appended, video swapped, choice replaced with **Cum! / Hallway**.
5. Click Cum! → final paragraph, **STATUS ✅ written, corruption +1, arousal -1, exit to Hallway**.

Engine sees one passage with progressive linkreplace content. Player sees a sustained 4-beat scene. Bridges "mechanical scene trigger" to "authored content" — makes scenes feel like reading a story even though the trigger was a dice roll. Bonus: each click in the drip is a "do you really want to continue" beat, giving the player consent moments without breaking flow.

## What this means for TLS

The TLS Quests-page issue (`◯ Teases ≥ 3` / `◯ Morning chores ≥ 3` with no breadcrumb to source) is a **counter→source surfacing gap**. RTS solves the equivalent problem two ways simultaneously:

1. The walkthrough's GUIDE column for each scene says where/when the prereq is raised (e.g., the Brother "Sleep with Stepbrother" scene has GUIDE: "Go to Stepbrother bedroom late at night and ask to sleep with him" — names location + time + action).
2. Sub-stat counters that gate scenes are USUALLY just numeric thresholds on global stats (corruption / exhibitionism / arousal), not opaque per-NPC counters. A player raising corruption knows *every* corruption gate moves toward unlocking.

TLS uses opaque per-NPC counters (`frank_tease_count`, `frank_chore_count`, `ryan_help_count`). These can't be incremented from one global activity — they require visiting specific scenes that may not even be visible yet. The walkthrough-equivalent (Quests page goal block) lists them as ◯ rows but doesn't say where to fulfill each.

**Four porting candidates for TLS, ordered by leverage** (revised after Pass 2):

### A. Add a Walkthrough-style scene table page WITH per-scene completion tracking (highest leverage)
Surface every authored canvas with its trigger conditions, location, schedule, NPC, and a short GUIDE prose line. PLUS add per-canvas completion tracking: a `canvas_completed_<id>` flag set on the canvas's terminal exit, and a STATUS column in the table that reads from it. From Day 1 player browses "Frank — N scenes" and sees the full scene roster; as they play, scenes flip 🔒 → ✅. Combined with REQUIREMENTS columns this becomes a self-driving player loop: scan locked scenes → pick one close to unlocking → execute the GUIDE → watch ✅ tick.

The data already exists in `setup.help_data.locationCanvases` — every canvas has trigger conditions, location, schedule, npcId. Authoring adds: per-canvas `guide` string (TOML field, defaults generated from trigger conditions); engine adds a single `set canvas_completed_<id> = true` effect to each canvas's terminal exit + a `_renderSceneTable` widget.

### B. Conditional-button injection in location passages (medium-high leverage)
TLS hub passages already render canvas buttons but only for canvases whose trigger conditions are AND-met. The RTS pattern is more permissive: a single hub passage walks every canvas in that location and renders a button per canvas whose primary stat-thresholds + chance=100 are met. The button label IS the canvas name; clicking dispatches the canvas. Brother bedroom going from 1 button → 4 buttons over a few days IS Q1's "appears from nowhere" problem solved.

This is a Pattern-3-ish refactor: replace the current single-button "enter scene" flow with multi-button conditional menus per hub. Doctrinally: hubs become menus; current scene-canvases become menu items unlocked by stat. Bigger lift than A but more transformative.

### C. Counter→source breadcrumb in Pattern 2 goal block (lower-medium leverage)
When a goal-block row references a counter (e.g., `frank_tease_count`), append a `↳ <canvas name> at <location>` line. Build a reverse index from `inc <counter>` effects → canvases that contain them. This is the "where do I tease" answer at the point of need.

If A ships, this becomes less critical because the walkthrough's per-scene GUIDE column will already tell the player where to do tease-incrementing scenes. So C is a fallback for slices that don't yet ship the walkthrough page.

### D. Notify-fail tier system at gated affordance click (lower leverage)
TLS today silently no-ops on gated room buttons. Adopting the three-tier RTS pattern (❌ label / transient toast / modal page) makes blocked clicks legible. Lower priority because the bigger problem is *discovering the affordance exists*, not *what blocks it once discovered*.

### Anti-pattern to avoid

Per-NPC opaque counters that gate cross-counter scenes (Frank Stage 3 needing tease ≥ 3 + chore ≥ 3) without visible "where to raise" breadcrumbs are RTS-incompatible. RTS uses global stats almost exclusively for cross-NPC gates; per-NPC chains use single-prereq narrative beats ("Have at least 15 relationship points") not cross-multiplication grinds. The TLS Stage-3 frank_tease_count + frank_chore_count + arousal + corruption + restrict-flag (5-AND) is doctrinally an outlier — Marcus's hardest gate is "Have at least 15 relationship points with Marcus, wait for his invite, go to the date" (one stat + one event).

## Bonus observations (not directly Q-aligned)

- **Same-button utility-vs-scene** is also a CONTENT TIERING strategy — RTS commits to writing the utility one-liner so every visit "does something." TLS's branch-inside-shell is the same idea but currently only at one or two scenes (catch, peek/draw). Should generalize.
- **The "Pin to Sidebar" button** on each Quest Journal entry suggests RTS knows players juggle multiple goals; pinning surfaces the chosen one in the always-visible sidebar quest line. TLS Quests page is the single goal block — no pinning concept yet.
- **Outfit "Set as Default" semantics** — the daily auto-rotate clothing system means tomorrow's clothes are a today decision. TLS doesn't have this; could be relevant if we add a wardrobe/clothing system.

## Session log artifacts

- `notes.md` — append-only Claude observations from this session
- `play_log.jsonl` — every command issued
- `screenshots/live/` — per-turn screenshots (cleaned on finalize)
- `passage_catalog.json` — full RTS passage source for offline grep
- `ui_map.json` — Phase 0 chrome-region catalog
