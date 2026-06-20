# Field Survey + Skill Review — deep passage-catalog analysis of 6 Twine sandboxes (2026-06-10)

The **deep** companion to `02_GAME_SURVEY_top_level.md`. Where doc 02 was a top-level *live-play* read
of 10 games (drive / spine / day-loop, no mechanics), this pass **mined the full passage source** of six
games offline — every gate condition, every variable, every scene-shape — plus two fresh portal surveys
to fix the corpus, then **reviewed the now-shipped `author-game` skill against the field**.

This is the evidence base for the next round of skill refinement: it confirms which doctrine the field
*proves correct* (don't relitigate it) and isolates six structural gaps worth folding in.

**Method.** Agents fingerprinted engines from shipped HTML (`<tw-storydata format="SugarCube">`), then
mined `passage_catalog.json` / `static_graph.json` / `variable_index.json` with python3 — design claims
come from passage SOURCE and counted gate conditions, not store descriptions. Life at University was
additionally **live-played** this session (new capture `game_explorations/tl-life-at-university/`).
Full per-game reports are in the 2026-06-10 session transcript; the load-bearing numbers are folded in
below. Mirror copy: `game_explorations/sandbox_field_survey_2026-06-10.md`.

---

## 1. The corpus — which games are actually Twine sandboxes

The portals lie: a large share of gamcore's "HTML" listings are Unity arcade games (Fuckerman/Eroman),
Ren'Py/RPGM ports, TyranoScript/Monogatari VNs (Urban Voyeur), or hand-rolled JS (Hentai University,
TiTS). Engine fingerprinting from the shipped builds was the only reliable filter.

### Confirmed Twine/SugarCube sandboxes — gamcore (fingerprinted)
Degrees of Lewdity (89%, the systems-driven benchmark) · Become Alpha (87%) · **Course of Temptation**
(81%, the closest structural cousin to an RTS-style design — weekly class schedule + corruption/exhibition
meters + organic NPC ladders) · Apocalyptic World (81%, clean money+energy+travel+schedule profile) ·
Become Someone (83%) · College Daze · Friends of Mine · **Corrupted City** (textbook
CityHub/OfficeHub/MallHub/GymHub hub-spoke) · **Secret Taboo** (room-schedule family home) · Project
Reeducation · Patriarch · Inheritance (slave-trainer) · Sissy Girlfriend Experiment · Become Taxi Driver
(job-loop sandbox) · X-Change Life (Twine-**Harlowe**, real-porn compositing) · Hard Times in Hornstown
(community-attested, 4.1M words / ~500 NPCs).
**NOT Twine despite the HTML tag:** Urban Voyeur (Monogatari), Hentai University (custom JS), Highschool
of Succubus / SlutEd (custom), Fuckerman/Eroman (Unity), Double Homework (episodic VN), TiTS (custom).

### Confirmed Twine sandboxes — mopoga
Road to Success (the exemplar, already deeply mapped — SugarCube 2.37.3 verified) · Become Someone ·
Degrees of Lewdity · **Sluttown USA** (resource-economy corruption — a rechargeable hypnosis-app *charge*
paces per-resident chains) · Gakko No Monogatari · The Company · Life at University · Lust for Life ·
**Family Business** (the camming/business economy IS the corruption mechanic) · Just One More Chance ·
Generic Porn Game · Back to Freedom · Life Choices · Zara's School Life. (Exchange Program = Ren'Py.)

### Deep-mined this session
| Game | Scale | Engine | Shape |
|---|---|---|---|
| **Become Someone** v1.87 | 3,228 passages, ~57 girl objects, 3,149 vars | SC 2.37.3 | life-sim, ~40 authored per-NPC ladders |
| **The Company** v5.12 | 2,075 passages, ~20 deep NPCs, 779 vars | SC 2.36.1 | qualitative-state TF/corruption *tree* |
| **Gakko No Monogatari** v0.35 | 4,269 passages, 34 NPCs, 758 vars | SC 2.36.1 | ladder-integer life-sim, video-first |
| **Back to Freedom** v0.42 | 2,919 passages, 15+40 girls, 601 vars | SC 2.36.1 | 45-day story VN + week-loop sandbox |
| **Life at University** v1.41 | 890 passages, ~20 NPCs, 487 vars | SC 2 | female-PC slutification, 303-day run |
| **Generic Porn Game** v0.20 | 327 passages (some 180KB), 33 girls | SC 2.37.3 | schedule-stalking life-sim, NTR |
(Prior captures still on disk: Road to Success deep maps, new-life-project, shady-deals, emilie-finds-a-way,
zaras-school-life.)

---

## 2. Per-game findings (the explored games + what's in them)

### Become Someone (3,228 passages — the scale exemplar)
The single most important structural lesson in the whole survey. **It is ~40 copies of one rigid arc
pattern** — `arc-stage integer + place + time-window + trust/corr threshold (+ occasional item/cross-NPC
gate)` — and *all* of its perceived depth comes from **cross-wiring** those copies, not from any arc being
complex. Mom's rung 4 requires sister at stage 5; mom's rung 10 requires Tammy's arc done; your restaurant
**salary formula reads the boss-NPC's trained stats** (`(20 + (boss.int+boss.trust)*2 + venue.status*20) *
degreemult`) — corrupting your boss literally raises your wage. Conquered girls become **infrastructure**:
girlfriend OR slave terminal state (both reversible), then staffed into your strip club / startup / moved
into mansion bedrooms, so finished arcs keep generating money and presence.
- **Guidance:** a sidebar **girls-location radar** (every met girl + a live link to wherever she is *now* —
  proof the NPC-radar works at 60-NPC scale), quest-markers that mirror gate logic 1:1, **golden portraits**
  when a capstone is ready, and 238 in-fiction refusal hints that state the exact requirement ("after lunch
  from 13:00 till 16:00").
- **Gate profile (11,038 conditions, intra-scene plumbing stripped):** quest-stage ≈ 2× (trust/corr ≈ time
  ≈ presence) ≫ MC-stats > items > **money 0.7%**. Money gates infrastructure, never story.
- **Devices:** sleep-link is a priority-ordered event dispatcher (mandatory click = guaranteed delivery);
  permanent gift items (+1 to all future gains for that girl) vs consumable gifts mapped to her stat axes;
  charisma as a global `CharismaBoost` on every trust gain (one "build" knob); 43% of passages are a
  gallery replay-museum (completion is first-class).

### The Company (2,075 passages — corruption as a branching tree, not a meter)
Gates almost nothing on numbers; it gates on **qualitative state — what you/the NPC have become**. The
corruption system is the **serum-dose ladder**: each NPC has `dose`/`nextSerum`/`doseCD`, and each dose step
is a **branching choice menu** (make him agreeable → submissive / best-friend / devoted-lover, OR the lab
path → numb / oral-slave / full female TF). Tiers aren't a track — they're **irreversible forks** ending in
persistent flags (`isSlut`/`isMaid`/`isBride`/`isPornstar`/`isDog`) that rewrite schedules, outfits, and
scene variants game-wide. `serumStatus($npc)` returns four legible lock states, each with its own in-fiction
"why not" line.
- **Reactive deck:** `EventsCheck` runs every turn and **adds/removes events from the random pool based on
  current world-state** (`if $kagney.isBimbo and hasWorkingPenis() → AddWorkEvent 41 else RemoveWorkEvent 41`).
  Ambient content always matches the world — the direct cure for stale/dead presence.
- **Behavior→identity drift:** nightly `TFCheck` prints an itemized receipt of how today's clothing/acts moved
  your gender/dom meters ("• Crossdressing makes you feel feminine +2"), with point-of-no-return thresholds.
- **Calendar-scripted world:** beats keyed to real dates (`isOctober(17)`, `timeIsAfter(20171219)`) — miss a
  window and NPCs leave, conversations vanish, a side character *dies*. The world proceeds without you.
- Daily-capped affection (`MaxDailyLove=2`) + 20-point milestone gift drops; ►/►► time-cost icons on buttons;
  **money 0.7% of gates** again (decorative outside the lab/Pit subgames).
- **One scene name, N corruption-stage bodies:** the ISS entry passage switches its whole opener/choice set on
  dose/flag state — repeatable scenes *mature* with the arc instead of multiplying passage count.

### Gakko No Monogatari (4,269 passages — walkthrough-as-sidebar + the dead-stat trap at scale)
Video-first (one MP4 per passage); every arc is a single monotonic `_event` integer (Remu 41 steps).
- **Best-in-class guidance:** `StoryRightSidebar` (the 277KB largest passage) is a **per-NPC live
  walkthrough** keyed to the exact `_event` integer, always naming **place + time-window + weekday**: *"From
  3:00 to 6:00 p.m., have dinner with Aunt Ririko in the kitchen,"* *"On Friday night around 10 p.m. or later,
  go to the front of Aunt Ririko's house and choose to travel to Kyoto."* 30+ concurrent arcs stay totally
  legible with **no quest engine at all**.
- **Pre-rolled randomness at the day tick:** sleep rolls *tomorrow's* dice into flags (`saeko_class_trigger =
  either("A","B")`) — daily variety, zero mid-day nondeterminism, no save-scumming.
- **Repeatable-arms-one-shot:** the masturbate loop's exit button silently swaps to the arc-opening "aunt
  catches you" scene at `masturbate_count == 5`. Grind loops double as **fuse timers** for story beats.
- **Meter-gated climax inside a looping scene:** self-linking "keep fucking her" + `$lust>99` climax gate (453
  passages) turns a state bar into in-scene pacing; creampies feed the earned-fertility pregnancy endgame.
- **Time-window × ladder-position ≈ 80% of all real gating.** Money 14 income / 10 sink sites in 4,269
  passages (the ¥100,000 Hina predatory loan lands hard *because* money is otherwise scarce).
- **Anti-pattern at scale:** confidence/academic/fame rank up across hundreds of scenes but gate ~5 things —
  the **dead-meter bug** (our LC `npc.arousal` finding) shipped commercially.

### Back to Freedom (2,919 passages — neglect rewards + the global scheduler)
Two games in one: a 45-day linear story VN (66% of passages) + a week-looping sandbox unlocked at story-end.
Dual axis per girl (`love`+`lust`, 15 mains), meters climbing almost entirely from story scenes (the story
IS the ladder; the sandbox doesn't grind meters).
- **Desire/neglect counters that reward ABSENCE:** 8 girls carry a `desire` counter, +1 per ignored night; at
  threshold SHE initiates (wake-up scenes `$angeladesire gte 4`, the boss summons you `$amirahdesire gte 7`),
  with explicit tooltips: *"You could have seen something different if you had ignored Amirah for many days."*
  Missing content becomes *alternate* content.
- **`PassageReady` = one global scheduler** doing stat clamps, daily ticks, random rolls, AND **forced
  interrupts** (`if $sbday is 5 and $sbtime is 4 → goto "sarahevent2"` — phone calls hijack you at fixed
  weekly times) in ~40 lines.
- **Session-scoped cash escalation:** strip-club `$kalimoney` tip ladder ($20/interaction, ≥150 = full
  service, **reset to 0 on leaving the map**) — an in-scene economy distinct from the global wallet.
- **Story one-shots recycled as sandbox repeatables** via shadow variables (` 2`-suffix clones + `g`-suffixed
  meters) — replay/gallery with zero state contamination. `memorize()`/`recall()` for meta-progression.
- Honest locked UI (`<span class="fakelink">` + `?` tooltips that explain *missed* content too). Weekly $300
  child-support call with a tracked Decline flag — light narrative-true pressure, no rent math.

### Life at University (890 passages — the female-PC slutification ratchet)
The closest published cousin to our cascade premise: female PC, corruption (`Liberal`) as the master gate.
- **Liberal ladder (extracted thresholds):** 10 gloryhole / 20 *the big band* (street stranger offers,
  stripclub door, sex-for-taxi, cafe flash) / 30 cam-show lewd acts / 50 club mid-tier / 80 park prostitution.
  ≈ RTS's grope-0 / flash-5 / sex-30 / public-45. Confirms "early intimacy cheap, deep/public floored."
- **Reputation = two-sided currency:** ≥40 unlocks lewd commerce (eroshop/strip/brothel); ≥50 **hard-locks
  legit jobs** with in-character rejection ("I don't want that associated with my gas station"). A visible
  point of no return on the sidebar.
- **Refusal costs:** declining a lewd offer fires `redlib 0.5` — corruption is a steered *equilibrium*, and
  "playing pure" is an active build, not a default.
- **Substitute gates:** `$drunk gt 70 OR $liberal gt 80` — intoxication previews high-tier content at a
  different cost (pacing valve for under-corrupt players). (Engine note: our conditions are AND-only.)
- **The economy is a one-way ratchet by design:** legit jobs (gas/cafe/hotel ~$30–45/shift, *require rep<50*)
  → in-job lewd add-ons appear at `liberal>20` → every lewd dollar *adds rep* → rep≥40 unlocks lewd work and
  rep≥50 closes legit work behind you. Earning = content, end to end.
- **Failure states ARE content funnels — three creditors, each defaulting into authored servitude before any
  game-over:** rent debt >$100 → landlady's lesbian "agreement," ≥$700 → game over; loanshark default →
  forced 14-shoot photoshoot contract → forced porn → forced cocaine dealing → *only then* police; shop tab →
  police. All failure converges on ONE `Gohome` ending with a `$crimereason` string slot (15+ feeders, cheap
  + tonally consistent).
- **Stat-buys-back-time:** weekly class quota = `Math.round(22 − intellect*0.25)`, gym = `8 − fitness*0.15` —
  progression *reduces obligation*, freeing the calendar for content.
- **Drip-feed unlock calendar:** 44 timed day-N notifications (day-5 cafe, day-20 loanshark, day-25 uncle,
  day-150 eroshop) turn a flat sandbox into a paced season; obligations arrive as in-game email.
- **The Ava inversion (player-corrupts-NPC):** blackmail ladder keyed to cumulative extracted cash → you
  *order her into park prostitution* → you pimp her ($10–50/customer). The mirror — handing the player the
  predator verbs used on her — is the most memorable beat in the game. Luna is the wholesome
  contrast-friend who can independently fall (you find her at the brothel).
- **Anti-patterns visible in the data:** a 21KB `PassageHeader` god-passage (rent + pregnancy + 12 unlock
  checks every click, with `<<timed 50ms>><<goto>>` interrupt hacks that double-fire); magic-number drift
  (venue floors hygiene 30/40/50/60 with no system; an AND/OR bug makes the brothel never reject); one-way
  arc bricks (model career permanently dead after one no-show); **gate-proximity blindness** (`redlib` can
  park you at 79.5 vs a `>80` gate with no feedback — the sidebar shows a bar, not gate distance).

### Generic Porn Game (327 monolithic passages — schedule-stalking + the energy=fitness coupling)
Male-PC, NTR-flavored, real-performer video. Hub-and-spoke driven by one `NAVIGATE1` `$act` router.
- **Energy cap = fitness:** one stat is your stamina pool, your gym progression axis, AND your seduction
  multiplier (`add_love`/`add_lust` scale with fitness). Early days are 5-energy short and visibly lengthen
  as you train — every system pulls the same lever.
- **In-game per-NPC walkthrough** (`*_track_event_completion`): numbered checklist with live sub-progress and
  condition spoilers, revealed once an event is active ("Event 8: sneaky sex-kitchen while partner's home +
  sneaky sex-bedroom while she's on the phone with him + booty-call").
- **Quest-hijacked navigation:** an active story beat *replaces* the normal "Go outside" button — progression
  interrupts the grind instead of hiding behind it.
- **Schedule-readable NTR:** husband schedules are first-class data; the cheating window is something you
  *deduce* from observable routines (Eethan at church Sunday 13:00–16:00), not a flag.
- **Sexskill = a turn budget** inside scenes (≤20 skill → 2 position-actions, >80 → 6); skill grind buys
  *agency per scene*, not gate-passing. `base_lust` ratchets to `max(act counts)` — a girl's arousal floor
  can never fall below what she's already done. Anti-repetition RNG wraps every grind action (gym rolls
  14–17 clip variants + occasional NPC encounter). Failure-tolerant fertility (the in-world GACRP custody
  program absorbs the consequence explosion). Money 0.4% of gates.
- **Anti-pattern:** the `$act` mega-router means **72.7% of all gate conditions are UI-state plumbing**, not
  design — a maintainability sink.

---

## 3. Cross-game synthesis (the field's actual rules)

### A. The universal rung grammar
Every authored-arc sandbox runs ONE pattern N×:
**`arc-stage integer + place + time-window + meter threshold (+ occasional item / cross-NPC gate)`.**
Become Someone runs it ~40×; Gakko's whole game is time-window × ladder-position (~80% of gating). This **is**
the skill's two-axis double-lock rung. Depth is perceived through **cross-wiring** instances (cross-NPC gates,
NPC-trained-stat salaries, conquest→staffing), not per-arc complexity.

### B. What the field gates on — and what it doesn't
| Axis | Field behavior |
|---|---|
| **Money** | Almost never gates content (0.4–0.7% of gates in the three biggest games). Gates *infrastructure* (housing, businesses, collars). Pressure is *narrative* (bills, debt, child support). |
| **Player stats** | Mostly dashboards in weaker games (Gakko ranks gate ~5 of 4,269 passages — the **dead-meter bug at scale**). The Company gates on **qualitative state** (isSlut/dose-tier), not numbers. |
| **Corruption** | The master content-tier (LaU 10/20/30/50/80 ≈ RTS 0/5/30/45). Early intimacy cheap; the global tier only floors deep/public content. |
| **Reputation** | Two-sided currency (LaU): unlocks lewd / *locks* legit. A visible point of no return. |
| **Arc-stage flags** | The dominant *content* gate everywhere. |
| **Time + presence** | ~24% of Gakko gates; the schedule is the content router. |

### C. Economy = corruption ladder, earning = content
LaU is the textbook one-way ratchet (legit→grey→lewd, rep closing legit work behind you). GPG couples
energy=fitness=seduction. LaU's stat-buys-back-time makes progression *feel like freedom*. BTF's
session-scoped cash ladder is an in-scene economy. **Failure states are content funnels** — every pressure
defaults into an authored servitude arc *before* any ending (LaU's three creditors).

### D. World-initiated content (the field's biggest divergence from us)
Our model is ~100% player-initiated; the field constantly *pulls*:
- **Neglect counters** (BTF) — ignore her and she comes to you.
- **Sleep-link hijack** (Become Someone) — the mandatory daily click delivers ready beats.
- **Forced interrupts** (BTF `PassageReady`) — phone calls at fixed day×time.
- **Quest-hijacked nav** (GPG) — active beats replace the "go outside" button.
- **Reactive event deck** (The Company `EventsCheck`) — the pool is recomputed each turn to match world state.
- **Drip calendar** (LaU) + **calendar-scripted misses** (The Company — miss it, it's gone).

### E. Guidance is the field's strongest differentiator
Best-in-class always names **place + time-window + weekday** in the *active* hint (Gakko walkthrough-sidebar,
Become Someone refusal hints, GPG checklists). Plus: golden "ready" portraits, per-NPC Notes journals
(The Company), girls-location radar, ►/♥ cost icons, four legible lock-states each with a "why not" line.

### F. Scenes
In-scene escalation is a **session meter** (Gakko `lust>99` climax gate; BTF dual pleasure bars; GPG
sexskill turn-budget; LaU 2–5-rung in-scene offer ladders) — validates our sex-loop. **One scene name, N
corruption-stage bodies** (The Company, Become Someone) keeps repeatables maturing without passage bloat.
Anti-repetition RNG decks everywhere. Post-capstone, Become Someone routes conquered NPCs into infrastructure.

### G. Player-corrupts-NPC (our cascade) in the wild
LaU's Ava arc (blackmail → pimping) is the mirror-inversion done well: the player gets the predator verbs.
Become Someone's slave-staffing and Sluttown's resource-paced resident chains are the same family.

---

## 4. author-game skill review

### Strongly validated — keep, do not relitigate
1. **Two-axis double lock** — IS the field's universal rung grammar (Become Someone trust+corr, The Company
   dose+relationship, RTS corruption+arousal).
2. **Rich-core / light-periphery (P5)** — universal (Become Someone deep ladders for ~15, skeletons for 40;
   GPG 12 developed of 33).
3. **Throttle vs odometer** — Gakko's `lust>99` session meter vs permanent `_event` ladder is exactly the split.
4. **Daily caps** — The Company `MaxDailyLove=2`, Become Someone `$todayRanEvent`, LaU `$visituncletoday`.
5. **Economy as corruption ladder · earning = content · money never gates content** — LaU textbook; 0.4–0.7%
   money-gate share field-wide. Our doctrine is exactly right.
6. **Reachability triad / schedules as data** — GPG 7-day×hour grids, Become Someone 62 NPC `loc1-7` tables.
7. **Honest locked-visible UI** — fakelinks + requirement tooltips field-wide.
8. **Feeder economy / player track** — LaU's camshow/gloryhole/park columns tiered by Liberal mirror the
   step-5 archetype catalog ~1:1.
9. **Sleep as router + day-tick** — universal.
10. **npc_panel sidebar radar** — Become Someone proves it at 60-NPC scale (closes the Doc 56 P10 gap).

### HIGH-value gaps (recommend folding in)
| # | Gap | Field evidence | Authorable via (real knobs) | Skill touch |
|---|---|---|---|---|
| **G1** | **Guidance must name place + time-window verbatim** per rung, not just the goal. | Gakko walkthrough-sidebar; Become Someone 238 refusal hints. | quest-card `text`/`tip` + `npc_panel` `next` block. | `beat-authoring.md` quest-card rules; `systems.md` HUD row. |
| **G2** | **Failure-states-as-content** — each pressure defaults into an authored leverage/servitude cascade *before* any game-over. | LaU's three creditors; BTF child-support. Our `eviction_flag` is the seed but only a rent gate. | rent `eviction_mode=flag_set` → gated leverage arc; debt = forced lewd-work chain; one ending funnel. | `step-2-toplevel.md` §4; `step-5-roster.md` (a cascade row per sink). |
| **G3** | **World-initiated pull** — the biggest structural gap; we're ~100% player-initiated. | Neglect counters (BTF), sleep-hijack delivery (Become Someone), forced interrupts (BTF), reactive deck (The Company), quest-hijacked nav (GPG). | Tier-3 `neglect_<npc>` trait raised by `[engine.daily_tick]` traitEffects, reset by the hub-visit beat → auto-fire capstone-shape canvas at the home/wake window. Capstone delivery gated to the sleep/wake window. | NEW `step-5-roster.md` archetype #11; `lanes.md` note; capstone-delivery doctrine. |
| **G4** | **On-ramp stagger / season pacing** — we open everything day 1. | LaU day-N drip calendar; The Company real-date scripting. | flag-chain (meet A arms B's intro) or schedule-window staggering; design book states each arc's opening act. | `step-2-toplevel.md` §5 pacing. |
| **G5** | **Cross-wiring as the depth driver** — depth = connections between arcs, not arc complexity. | Become Someone: cross-NPC gates, NPC-stat salaries, conquest→staffing. Our cross_npc/threads are optional flavor. | cross-NPC condition gates; economic beats reading NPC traits; conquest→infrastructure rows. | `step-5-roster.md` self-check (min cross-NPC row count); `step-4-npc-arcs.md` §8 → budget. |
| **G6** | **Post-capstone repurposing** — completed NPCs keep generating value (cures post-capstone dead presence). | Become Someone staffs conquered girls into clubs/startups/bedrooms. | a repeatable earning/standing-obligation role gated on the arc's terminal flag. | `step-4-npc-arcs.md` repeatable-loop section; `17_frontier_endless_model.md` steady-state. |

### MEDIUM gaps (a line each — author-side patterns)
- **Refusal costs** — small `−corruption` on decline branches (LaU). CAUTION: pair with gate-proximity
  visibility or content silently re-locks (LaU's own bug).
- **Repeatable variety decks** — rotate 2–3 prose/media variants inside repeatable hubs/solo activities
  (GPG/LaU/Gakko all do). Engine path: substitution variants / random-chance sibling canvases.
- **Stat-buys-back-time** — if a game has an obligation system, let a stat reduce the quota (LaU formula).
- **Travel friction** — small time(+energy) cost on district moves makes schedules matter; we currently teleport.
- **Repeatable-arms-one-shot** — solo feeder loops trigger their arc's on-ramp at a usage count (Gakko
  masturbate→caught): the feeder raises a hidden trait; the auto-fire intro gates on it.
- **Substitute gates** (`drunk OR corruption`) — engine conditions are AND-only; emulate with parallel gated
  choices if wanted. Low effort, niche.

### Engine wishlist surfaced by the field (NOT skill changes — for a future engine PRD)
- **OR-combinator in conditions** (substitute gates).
- **Random variant selection among group blocks** (anti-repetition decks, currently author-faked).
- **A gallery / completed-scenes ledger** (Become Someone = 43% of passages; huge completionist pull; pure
  engine feature).
- **Absolute-day predicate** for canvas conditions (drip calendar + dated misses without flag-chain workarounds).
- **Map/nav "live event here now" badge** (Gakko pulsing hotspots; we have NEW only for capstones).

### Divergences checked and KEPT (the field does it, we shouldn't copy)
- **Endless frontier vs fixed run** — LaU's 303-day term suits ITS premise but produces brittle one-way
  endings; our endless-frontier (`17`) + season pacing (G4) gets the structure without the wall.
- **Constant hub opener (D56-R1)** — the field tier-swaps full SCENE bodies by stage; that's fine — our rule
  scopes only the *hub base node*, and stage-keyed group variants in scenes/ambients remain allowed.
- **Hard game-overs** — the field uses them heavily (LaU `Gohome` ×15 reasons) but always *behind a cascade*;
  our no-hard-ending stance + the G2 cascade is strictly better for an endless sandbox.

---

## 5. Status + artifacts
- **Review only — no skill files edited.** The six HIGH gaps are the proposed next wiring pass; they touch
  `beat-authoring.md`, `step-2-toplevel.md` §4/§5, `step-5-roster.md` (archetypes + self-check),
  `step-4-npc-arcs.md`, and `systems.md`.
- New capture: `game_explorations/tl-life-at-university/` (890-passage catalog + static graph + var index +
  live notes). Mirror of this doc: `game_explorations/sandbox_field_survey_2026-06-10.md`.
- Memory pointer: `memory/sandbox_field_survey.md`.
- Sources: gamcore.ch/html_spiele pages 1–6 (CDN-HTML engine fingerprints); mopoga.com `/sandbox` + `/html`
  tag pages; per-game passage catalogs in `game_explorations/`.
```
Doc 02 = top-level live-play of 10 games (drive/spine/day-loop).
Doc 21 = deep passage-source mining of 6 games + skill review.   ← this doc
```
