# UOR Redesign Analysis — 2026-04-19

*A content-layer redesign framework for Under One Roof, grounded in reference-game evidence. No engine, prompt, or framework changes — only how UOR's TOML is written.*

---

## 1. The Starting Question

UOR feels like a menu-clicker. You go to a location, click an activity, read a paragraph, return to the map, and repeat. It does not feel like a game.

The question this document answers: **why?** And just as importantly: **what would we change — without touching the engine or prompts — to make it feel like a real game?**

Constraints going in:
- No changes to the game generation engine
- No changes to the authoring prompts
- No changes to the framework
- No new NPCs (keeping Frank, Ryan, Jake, Diana as-is)
- Pure content-layer redesign within current engine capability

The analysis is grounded in fresh exploration data (2026-04-19) from three reference games: **Shady Deals**, **Road to Success**, and **New Life Project**. Each one feels different from UOR in a specific, identifiable way. Together they triangulate what the problem actually is.

---

## 2. The Three-Layer Framework

The diagnostic model developed across this analysis. Every game that feels alive has all three layers. UOR is weak on all three but especially weak on Layer 3.

### Layer 1 — Inside the click (game moments)

What happens *during* an activity. The click is not the activity — the click is the entry point. What follows should have:

- **Visible meters** that move with your choices (complaint gauge, noise, heat, suspicion)
- **Hidden rolls** with visible stakes (you see the range, you don't see the outcome)
- **A bail button** that's always available — you can cut losses mid-activity
- **Multi-beat resolution** — 3-5 decisions inside one activity, not one-click-one-outcome
- **Carryover state** — choices inside the activity create flags, relationships, and future scenes that didn't exist before

Without Layer 1, every click is a vending machine: insert 1 hour, receive $45.

### Layer 2 — The menu of options (who the MC is)

The list of things on the player's screen at any moment reflects **exactly who the MC is right now** — not her future self with options locked behind requirements. The menu itself is the arc, visualized.

- **Options are invisible until narratively earned** — a story canvas teaches the MC the behavior, then the option APPEARS on the activity menu
- **No grayed-out previews** — showing "flirt for tips — requires corruption 45" turns the arc into a grind target and kills surprise
- **The menu GROWS as she changes** — Week 1 Maya has 4 boring options, Week 8 Maya has 12, each new one earned through a beat
- **Two different playthroughs produce two different menus** — a Maya who triggered the trucker arc has different options than one who didn't

Without Layer 2, content feels like a tech tree to unlock, not a character to become.

### Layer 3 — The world around the click (running simulation)

The world is doing things whether the player clicks or not. This is the layer that makes the difference between *reading a pausable story* and *participating in a machine that's running*.

- **Autonomous state change** between clicks (stats decay, bills accumulate, NPC moods drift)
- **Scheduled bills and deadlines** that tick regardless of player choice (rent due, landlord visits)
- **Random events that INTRUDE** on the player's plans (muggers, drop-ins, surprise visits)
- **News / rumors / world events** that move independently of the player
- **RNG re-rolls** on location entry — the same place isn't the same place twice
- **Menu changes based on world state** — heat locks areas, time windows close, NPCs become unavailable

**Layer 3 is the highest-leverage layer.** The games that feel most alive all have Layer 3 strong. Games that are mechanically rich but Layer 3 weak (Road to Success) still feel dead. Games that are characterologically shallow but Layer 3 strong (New Life Project) still feel like games.

---

## 3. What UOR Currently Is

Facts from the TOML audit of `games/under_one_roof/toml_phases/6_final_game.toml` (8,647 lines):

**Scale**
- 24 locations (4 containers: Property, Backyard, Campus, Trail Head)
- 4 NPCs (3 mechanical — Frank, Ryan, Jake; 1 phone-only — Diana)
- 221 canvases (167 story/activity + 54 repeatable)
- 57 story arc nodes across 7 chapters
- ~59 flag keys
- 7 player core traits (corruption, confidence, money, energy, fitness, beauty, intelligence)

**Pressure & economy**
- Rent: $50/Monday, collected by Frank, 1 grace period
- Income: single channel — utility diner shift ($45 + tips, 17:00–22:00, confidence ≥ 30)
- Starting money: $400
- No debt, bill-shock, auto-loan, heat, suspicion, or reputation blocker

**Variety systems**
- 5 canvases with `trigger_mode = "random"` (rarely fire per audit)
- No minigames, no procgen NPC pools, no rival/clock/authority/threat archetype tags
- No `narrative_gates` section, no `whiteboard_goals`, no news/rumor layer

**Gates & hints**
- 6 story arc hints (good — engine's Quest Page can render these)
- No rumor/news/forum in-fiction explanation layer

**Time & schedule**
- `[time]` block exists (enabled, 17:00 Saturday Week 1 start)
- 62 canvas schedule blocks — heavy time-window gating
- No autonomous event scheduler (only player-triggered canvases advance state)

**Half-built**
- Orphan containers: `loc_backyard`, `loc_trail_head`, `loc_creek`, `loc_rest_stop` — declared but no canvases bound to them
- NPC `archetype` field not in schema (so no rival/threat categorization possible)
- 5 random-encounter canvases exist but don't fire reliably on arrival

**Engine capability vs. content usage**
- Engine supports: random encounters, time/schedules, per-trait decay, rent, emotion mappings, clothing/wardrobe with body_coverage, costs, passes, dimmed choices, Quest Page, getSidebarHint, getNextActivity
- Engine does NOT support: whiteboard_goals dataclass, narrative_gates routing, income_channels as structured data, NPC archetype field, npc_pools, minigame state machines, two-currency economy, heat/suspicion blocker
- **Approximately 70% of what we'd want is already in the engine.** UOR's TOML doesn't exercise most of it hard enough.

---

## 4. Reference Game Deep Reads

All three read fresh from updated exploration data on 2026-04-19.

### 4.1 Shady Deals — the running-simulation exemplar

**Verdict:** all three layers strong. This is the gold standard for ongoing-game structure.

**What makes it feel like a game:**

- **Sidebar is always alive.** Portrait, money/dirty money split, clock (Tue Jun 1 08:20 format), quick actions (WAIT/INVENTORY/STATS/LOG). Clock ticks on every passage transition. Player always sees they're in a *state*.
- **Heat is a real blocker.** `heat_lab_block`, `heat_warehouse_block`, `heat_thieves_block` — high heat closes activities. Paying Bleach to wash heat costs money and time, creating a squeeze.
- **Daily upkeep computes automatically.** NewDay passage deducts food+tax ($10), compares gained vs. spent, auto-loans $1000 if broke (carries bank debt).
- **Crew morale inflates wages.** `band_morale < 26` triggers `morale_mod = 1.5x` daily wage inflation. Ignore your crew → they get expensive.
- **Random encounters interrupt plans.** "Downtown Attack" demands $307 street tax on district entry — blocks Marketplace click until resolved.
- **Outskirts gated by in-fiction news.** Web Forum story "Road to Outskirts closed" IS the mechanical gate. Narrative event IS the barrier.
- **Whiteboard lists 7 visible goals** at the home passage: >$10k money / Own a warehouse / Own a house / Meet all 4 factions / "Big Shot" reputation / 3x Block 19 handguns / Gang strength >300. Completing all 7 unlocks Phase 2 content (Create Your Gang button).
- **Phase 2 is content expansion, not ending.** Junkyard workshop, semi-legal businesses, heist menu, prostitution management, different economy. The game doesn't end — it *widens*.
- **Failure has texture.** Losing a fight → "Downtown Lose" flavor + refund-if-broke + forced recovery at home. Losing turf war → -500 rep + -20 morale + enemy buffed for next attempt. Losing crew to jail → need police_connections to rescue.
- **Layered time horizons simultaneously.** Whiteboard (long) + daily upkeep (short) + turf war progress (medium) + yacht party cycles (14-day recurring) — all active at once.

### 4.2 Road to Success — scaffolding without bite

**Verdict:** game-shaped VN. Mechanics are present, consequences are absent.

**The paradox:** R2S has *more scaffolding* than UOR — 49 NPCs, job ladder, time buckets, dense sidebar, dual-gated content. And it still feels like a stat-grinding VN.

**Why it fails:**

- **NPCs are stat containers, not characters.** All 49 NPCs have arousal/corruption stats. **Zero mutations observed across 4 in-game days of play.** They exist as signposts.
- **Pressure is toothless.** `apartment.rentCycleDays = 7`, `daysUntilRent = 6-7` — rent exists but **never enforced in observed play**. Kidnapping event → +1 corruption, energy to 0 → forced sleep → full restore. No persistent damage.
- **Escalation is purchase-gated, not narrative-earned.** Want XCam scenes? Buy a Laptop ($800) + Webcam ($200). No story beat where the MC crosses the line. Economic gate IS the narrative gate.
- **Choices hide outcomes.** Restaurant interview: "Seduce boss" silently no-ops if corruption too low. No fail message, no alternate route shown. Player clicks blindly.
- **Sandbox with no goal.** No visible goal system — no Whiteboard, no endings matrix, no populated Guide Page, no signposted "Road to Success" objective. Graduation exists but is never surfaced to the player. The player grinds stats but doesn't know why.
- **World is frozen between clicks.** NPC locations shift at time-bucket transitions. That's it. No autonomous events, no ambient changes.

**Strengths worth stealing:**

- **Multi-track job ladder with switching costs** (Waiter → Secretary → Bartender → Stripper). Each has location/uniform requirements; switching jobs has costs. Creates real weekly decisions.
- **Time-bucket NPC presence** (EM/M/A/E/N/LN). Simpler than exact-hour schedules; player learns a mental map of where everyone is when.
- **Activity menus at hubs** (flat navigation — School = MathClass/Library/Cafeteria/Bathrooms on one screen). Keeps nav efficient.
- **Corruption-gated content ladder.** Concept works; UOR should use it more cleanly.

**The lesson:** mechanical features alone don't make a game feel alive. You can have 49 NPCs and a job ladder and still feel dead if nothing has teeth.

### 4.3 New Life Project — pressure without character

**Verdict:** pressure trap with hollow NPCs. Layer 3 very strong, Layer 2 very weak.

**The opposite failure from R2S.** R2S has dense mechanics and no bite. NLP has brutal bite and hollow characters.

**What makes it feel like a game (despite shallow NPCs):**

- **Period-per-click rationing.** 6 periods/day. Every action consumes one. Player can't visit cafe AND beauty shop AND alley AND still shower before sleep. Scarcity is structural.
- **Weekly rent actually collects.** £400/week, escalates to £1800. Observed: £372 → £72 week 1 to week 2. Hard deadline, bites.
- **Cascading failure as content.** Can't pay rent → `rentRape` event fires → +trauma + +corruption → unlocks alley-job content at higher corruption. *Failure is a door, not a wall.* Best pattern in the genre.
- **Autonomous hygiene decay.** `kitchenClean -25` every sleep. `zackClean -25` every sleep. You wake up grimy; you MUST shower; showering costs a period. The day starts with chores.
- **Regression that actually bites.** Allure -15 on alley assault. Shower +15 restores it. But while at low allure, cafe tips drop and social interactions suffer in the meantime. Stats actually degrade gameplay.
- **Three-axis stat system.** Allure (cosmetic — tips, bar access) / Inhibition (sexual comfort) / Corruption (moral darkness). Three separate gauges gating different content. High allure + high inhibition + low corruption is a different character from the opposite.
- **RNG re-rolls on hub transitions.** `rngesus` variable, 46 mutations observed. Mugged-arc triggers on `rngesus==7`. Alley dealer appears on `rngesus==1 && allure>=40`. Same location, different content per visit.
- **Time-of-day gates world access.** Downtown/Uptown inaccessible until evening. Beauty shop closes. Club only at night. World *feels* alive even if NPCs are frozen.

**Weaknesses worth avoiding:**

- **NPCs are stat sinks.** 7 NPCs defined (Chloe, Lily, Bro, Dad, Zack, Caine, Nun). Only Zack (landlord) mutates. Everyone else: 0 love-stat mutations across 481 clicks. Nun got 0→1 once.
- **Inhibition-as-progression is weirdly one-sided.** Losing inhibition unlocks content. So "become more corrupted" = "unlock better game." No mechanical reward for staying pure. Only submission has content.
- **97% of content is locked behind invisible flag sequences.** 2.9% passage coverage across 481 clicks. Mansion, cult, kidnap, dad, brother arcs exist in data but unreachable from intro without knowing flag sequences.
- **Hub is static.** Zack always home. Lily always at cafe. NPC schedules don't drift.

**The lesson:** you can make a game feel alive with shallow NPCs if Layer 3 is strong enough. But you can't make it feel *good* without Layer 2.

---

## 5. Comparative Matrix

| Game | Layer 1 (game moments) | Layer 2 (menu=character) | Layer 3 (running sim) | Verdict |
|---|---|---|---|---|
| **Shady Deals** | Yes — burglary, heat, factions | Partial — Whiteboard visible goals | **Strong** — heat, morale, upkeep, RNG, news | **Feels like a game** |
| **Road to Success** | Weak — silent fails, hidden outcomes | No — grind-gated, purchase-gated | Weak — time buckets only | **Stat spreadsheet** |
| **New Life Project** | Some — period cost visible, rent countdown | No — inhibition-only, frozen NPCs | **Strong** — rent, decay, RNG, cascading failure | **Pressure trap** |
| **UOR (current)** | No — deterministic outcomes | Weak — Guide Page exists but only 6 hints feed it | Very weak — no decay, no events | **VN with branches** |

**The pattern:** Layer 3 is the highest-leverage axis. Games strong at Layer 3 feel alive even when other layers are weak. Games weak at Layer 3 feel dead even when other layers are scaffolded.

UOR is weakest where it matters most.

---

## 6. The 13 Redesign Focus Items

Grouped by layer. Each item has **Current** (what UOR has now) and **Should be** (the target).

### Layer 3 — The world around the click (build first)

**1. Visible daily action budget**
- *Current:* Time advances in unpredictable 4-6 hour chunks per canvas. Player never feels the day ending; it just ends.
- *Should be:* 4-5 visible "periods" per day (Morning / Afternoon / Evening / Night). Each activity consumes one. Sidebar shows "Period 3 of 5." Player learns to triage.

**2. Rent that actually squeezes**
- *Current:* $50/week, easily covered by one diner shift. Scenery.
- *Should be:* Tight enough that one shift can't cover it. Forces real choice between earning, resting, and relationship-building. Missing rent has a concrete bad outcome — not game over, a darker story branch.

**3. Hygiene or maintenance decay**
- *Current:* Nothing decays overnight.
- *Should be:* 1-2 stats drop while Maya sleeps (hygiene, food, sleep debt). She wakes needing to address them before anything else. Each costs a period. The day STARTS with chores, not quests.

**4. Autonomous world events**
- *Current:* The only things that happen are canvases the player triggered.
- *Should be:* Scheduled events fire without player input. Day 7: Frank's sister visits unannounced. Day 14: a cop starts patrolling the neighborhood. Day 21: Ryan's friends visit for the weekend. The world DOES things to Maya.

**5. Failure as content, not "try again"**
- *Current:* No real failure states. Bad outcomes restore on sleep.
- *Should be:* Fail a shift → Frank docks trust permanently. Miss rent → forced into a humiliating "other arrangements" scene with Frank that unlocks a different arc. Losing opens DOORS, not walls. (Steal directly from NLP's `rentRape` cascade.)

**6. Live sidebar with moving meters**
- *Current:* Sidebar shows static stats.
- *Should be:* Sidebar shows *pressure*: "Rent due in 4 days," "Frank's trust: 5/10," "Hygiene: ●●○○○," "Period 2 of 5 today." The player SEES the world moving whether they're acting or not.

### Layer 2 — The menu of options (build second)

**7. Rich Guide Page hint pool** *(not a Whiteboard — the Guide Page pattern fits UOR's tone; Maya isn't a crime boss with a goals board)*
- *Current:* 6 hints in `story_arc.hints.templates`. Guide Page mostly falls back to generic next-activity output because the custom hint pool is thin. Player often doesn't know what Maya should do next, or the hint is too vague to act on.
- *Should be:* 30-50 context-aware hints covering every NPC / time window / Maya-state combination. Each hint is specific and actionable — *"Frank mentioned the office drawer earlier — he's at work until 6 on Tuesdays, the house is quiet"* — not generic — *"talk to Frank more."* The Guide Page always has something urgent and state-appropriate to show because the pool is big enough to match any moment. Engine's `setup.getSidebarHint()` / `setup.getNextActivity()` already handles selection; we just need a bigger, better-written pool.

**Why Guide Page instead of a visible Whiteboard:** UOR's tone is intimate family drama, not crime-empire sandbox. Maya lives the story one next-thing at a time — she doesn't maintain a literal goals list on her wall. The "next actionable thing, surfaced when relevant" pattern fits who she is. A whiteboard of 7 explicit goals would feel like HUD on a character who should feel human.

**8. Options that GROW through story beats, not grind**
- *Current:* Gated content shown as "requires corruption 45" — the player sees the locked future and grinds toward it.
- *Should be:* Options INVISIBLE until a story canvas teaches Maya the behavior. Week 1 menu has 4 boring options. Week 3 she catches another waitress flirting for tips — now "flirt with the trucker" APPEARS. The menu GROWING is the arc, not a requirements list.

**9. NPCs whose stats actually move**
- *Current:* Frank, Ryan, Jake have love/trust/corruption fields. Barely move in play. NPCs are stat containers. (Same disease as R2S and NLP.)
- *Should be:* Every interaction shifts NPC mood. Ignore Frank for 2 days → trust drops, he's cold next time. Lie to Ryan → he remembers, options narrow. NPCs have their own tick — mood decays, they initiate contact, they show up unexpectedly.

**10. Two progression axes, not one**
- *Current:* Corruption is the only axis. "Pure Maya" has nothing to play with — only the submission route has content.
- *Should be:* Corruption + one other axis (independence, defiance, self-respect — fits the UOR tone). Going along with Frank builds corruption; pushing back builds defiance. Both open different content. Two legitimate character shapes, two different playthroughs.

### Layer 1 — Inside each click (build last)

**11. Activities with a middle (not atomic)**
- *Current:* Click activity → single prose block → back at map.
- *Should be:* Click activity → 3-5 beats with decisions along the way. Diner shift becomes: greet host → pick a table/customer to handle → handle it → pick another → close out. Total outcome depends on the choices made inside.

**12. Hidden rolls with VISIBLE stakes**
- *Current:* Outcomes are deterministic and predictable.
- *Should be:* Show the meter (complaint gauge 1/3). Show the range (tip $5-25). HIDE the actual roll. Player decides based on risk tolerance and current meter state, not based on knowing the exact outcome. (The Shady Deals burglary model — NOT the R2S silent-fail model.)

**13. Bail buttons on risky activities**
- *Current:* Activities run to completion once started.
- *Should be:* "Call it a night early" / "Back out of the alley" / "Hang up" always available on multi-beat activities. Bailing costs some gain but stops risk from escalating. This is what turns a click into a judgment call.

---

## 7. Priority Order — The Five That Matter Most

If only five items can be done, these five deliver the most game-feel for the work:

1. **#1 Daily action budget** (periods) — every other mechanic plugs into this
2. **#2 Rent that squeezes** — creates the first real pressure
3. **#5 Failure as content** — teaches the player stakes are real
4. **#7 Rich Guide Page hint pool** — gives pressure a direction via the existing Guide Page infrastructure
5. **#9 NPCs that actually move** — makes Frank/Ryan/Jake into characters instead of dispensers

Without these five, the rest is polish on a VN. With these five, UOR fundamentally changes shape — even without Layers 1 and 2 complete.

---

## 8. What We Are NOT Doing

Scope discipline — none of these are in play:

- **Not changing the engine.** All 13 items work within current `template_import.py` + `v1.py` capability.
- **Not rewriting prompts.** Neither `game_book_prompt_v6.txt` nor `toml_generation_prompt_v4.txt` changes.
- **Not changing the framework.** The pipeline stays as-is.
- **Not adding NPCs.** Frank, Ryan, Jake, Diana remain. We make them *deeper*, not more numerous. (The R2S lesson: 49 shallow NPCs is worse than 3 deep ones.)
- **Not touching packaging.** The UOR TOML packaging was fixed in an earlier session; no infrastructure work.

This is a pure **content-layer redesign** within current engine capability. Every change happens in `games/under_one_roof/toml_phases/6_final_game.toml`.

---

## 9. One-Sentence Summary

**UOR currently writes scenes you can trigger. It should write a world that's running — with a tight daily budget, biting pressure, visible goals, reactive characters, and activities that have a middle.**

---

## Appendix: Sources

- UOR TOML audit: `games/under_one_roof/toml_phases/6_final_game.toml` (8,647 lines)
- Engine capability audit: `apps/projects/services/template_import.py` + `apps/game_generation/twee_comprehensive/generators/v1.py` (HEAD state, 2026-04-19)
- Shady Deals exploration (updated 2026-04-19): `game_explorations/shady-deals/` — report.md, notes.md, variable_profile.json, play_log.jsonl, state_timeline.jsonl, sidebar_snapshots.jsonl
- Road to Success exploration (added 2026-04-19): `game_explorations/road-to-success/` — report.md, notes.md, npcs.json, variable_profile.json, initial_state.json
- New Life Project exploration (updated 2026-04-19): `game_explorations/new-life-project/` — report.md, notes.md, npcs.json, variable_profile.json, state_timeline.jsonl
- Prior companion session: `17th_april_UOR_ZSL_Session/` (Framework_Review, Framework_Potential, UOR_v2_Redesign) — referenced for context; UOR_v2_Redesign's 6-endings model is a bounded-game artifact and does NOT apply to UOR's ongoing-game target
