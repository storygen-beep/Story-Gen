# Sandbox Twine field survey + author-game skill review (2026-06-10)

Research pass over gamcore.ch + mopoga: identified the genuine Twine/SugarCube sandbox games,
deep-mined six of them offline (full passage catalogs), live-played one, then reviewed
`.claude/skills/author-game/` against the field. Agent evidence: engine fingerprints taken from
shipped HTML; design claims mined from passage source (not descriptions).

## 1. The corpus

### Confirmed Twine sandboxes — gamcore (engine fingerprinted from shipped HTML)
Degrees of Lewdity (89%, SugarCube, systems-driven benchmark) · Become Alpha (87%) ·
Course of Temptation (81%, the closest structural cousin to RTS-style design) · Apocalyptic World
(81%) · Become Someone (83%) · College Daze · Friends of Mine · Corrupted City (textbook
CityHub/OfficeHub/MallHub/GymHub) · Secret Taboo (room-schedule family home) · Project
Reeducation · Patriarch · Inheritance · Sissy Girlfriend Experiment · Become Taxi Driver ·
X-Change Life (Twine-**Harlowe**) · Hard Times in Hornstown (community-attested).
NOT Twine despite "HTML" tag: Urban Voyeur (Monogatari VN), Hentai University (custom JS),
Highschool of Succubus / SlutEd (custom), Fuckerman/Eroman (Unity/arcade), Double Homework
(episodic VN), TiTS (custom).

### Confirmed Twine sandboxes — mopoga
Road to Success (the exemplar; already deeply mapped) · Become Someone · Degrees of Lewdity ·
Sluttown USA (resource-economy corruption: rechargeable hypnosis-app charge paces per-resident
chains) · Gakko No Monogatari · The Company · Life at University · Lust for Life · Family
Business (camming-economy IS the corruption mechanic) · Just One More Chance · Generic Porn
Game · Back to Freedom · Life Choices · Zara's School Life. (Exchange Program = Ren'Py.)

### Deep-mined this session (full passage-catalog analysis)
| Game | Scale | Shape |
|---|---|---|
| Become Someone v1.87 | 3,228 passages, ~57 girl objects | life-sim, authored per-NPC ladders |
| The Company v5.12 | 2,075 passages, ~20 deep NPCs | qualitative-state TF/corruption tree |
| Gakko No Monogatari v0.35 | 4,269 passages, 34 NPCs | ladder-integer life-sim, video-first |
| Back to Freedom v0.42 | 2,919 passages, 15+40 girls | 45-day story VN + week-loop sandbox |
| Life at University v1.41 | 890 passages, ~20 NPCs | female-PC slutification, 303-day run |
| Generic Porn Game v0.20 | 327 passages (some 180KB) | schedule-stalking life-sim, NTR |
(+ prior: Road to Success deep maps, new-life-project, shady-deals, emilie-finds-a-way, zaras-school-life)

## 2. Cross-game design synthesis (what the field actually does)

### The universal rung grammar
Every authored-arc sandbox runs ONE pattern ~N× (Become Someone runs it ~40×):
**arc-stage integer + place + time-window + meter threshold (+ occasional item/cross-NPC gate)**.
Become Someone mom rung: `20:00–21:59 ∧ questmain is 7 ∧ momjewelry ∧ paidbills`; mom stage 10
requires *Tammy's* arc done; stage 4 requires *sis* stage 5. Depth is perceived through
**cross-wiring** (cross-NPC gates, NPC-trained-stat salaries, conquest→staffing), not per-arc
complexity. Gakko: time-window × ladder-position ≈ 80% of all real gating.

### Meters: what the field gates on (and doesn't)
- **Money almost never gates content**: 0.7% of gates in both Become Someone and The Company.
  Money gates infrastructure (housing, businesses, collars); pressure is narrative (bills, debt).
- **Player stats are mostly dashboards** in weaker games (Gakko confidence/academic ranks gate ~5
  things in 4,269 passages — the dead-meter bug shipped at scale). The Company gates on
  **qualitative state** (what you/NPCs have become: isSlut/isMaid/dose-tier), not raw numbers.
- LaU's **Liberal** (corruption) ladder: 10 gloryhole / 20 the big band (street offers, stripclub
  door, sex-for-taxi) / 30 cam acts / 50 club mid-tier / 80 park prostitution. ~RTS's
  grope-0/flash-5/sex-30/public-45. Confirms the "early intimacy cheap, deep/public floored" curve.
- **Reputation as two-sided currency** (LaU): ≥40 unlocks lewd commerce, ≥50 hard-locks legit
  jobs with in-character rejection. A visible point of no return.
- **Refusal costs** (LaU): declining a lewd offer = `redlib 0.5` — corruption is a steered
  equilibrium, "playing pure" is an active build.
- **Substitute gates** (LaU): `drunk > 70 OR liberal > 80` — intoxication previews high-tier
  content at a different cost.

### Economy
- LaU is the textbook one-way ratchet: legit jobs (gas/cafe/hotel, ~$30-45/shift, rep<50
  required) → in-job lewd add-ons appear at liberal>20 (every lewd dollar adds rep) → rep≥40
  unlocks eroshop/strip/brothel and rep≥50 closes legit work behind you. Earning = content.
- **Failure states ARE content funnels**: LaU rent debt >$100 → landlady lesbian "agreement";
  ≥$700 → game over. Loanshark default → forced photoshoots → forced porn → forced drug dealing
  → only then police. Three creditors, each default cascading into authored servitude before any
  ending. BTF: weekly $300 child-support call with a tracked Decline flag.
- GPG: **energy cap = fitness** — one stat is stamina pool, gym progression, AND seduction
  multiplier; early days are short and visibly lengthen.
- LaU: **stat-buys-back-time** — weekly class quota = `22 − intellect×0.25`, gym = `8 − fitness×0.15`.
  Progression reduces obligation, freeing the calendar for content.
- BTF: **session-scoped cash ladder** ($20 tips into `$kalimoney`, ≥150 = full service, resets on
  leaving) — an in-scene economy distinct from the wallet.

### Time & world-initiated content
- Sleep is universally the day-tick housekeeping pass (resets daily flags, decays, re-arms).
  Gakko **pre-rolls tomorrow's dice at the sleep tick** (no save-scumming, stable days).
- **Sleep-link hijacking** (Become Someone): the one mandatory daily click is a priority-ordered
  event dispatcher — guaranteed story delivery. BTF's PassageReady forces phone-call interrupts
  at fixed day×time. GPG: active quests **replace the normal "go outside" nav button**.
- **Neglect/desire counters** (BTF): per-girl +1 per ignored night; at threshold SHE initiates
  (wake-up scenes, boss summons) — missing content becomes alternate content.
- **Drip-feed unlock calendar** (LaU): day-5 cafe, day-20 loanshark, day-25 uncle, day-150
  eroshop... 44 timed notifications turn a flat sandbox into a paced season. The Company scripts
  beats to real calendar dates — miss the window and NPCs leave/die (permanent misses).
- **Repeatable-arms-one-shot** (Gakko): masturbate loop's exit silently swaps to the
  "aunt catches you" arc-opener at count 5 — grind loops as fuse timers for story.
- Travel friction is real: GPG per-hop minutes table; LaU walking costs time+energy+hygiene,
  taxi $5 (payable with sex if broke + liberal>20).

### Guidance (the field's strongest differentiator)
- Gakko: **walkthrough-as-sidebar** — per-NPC hint keyed to the exact ladder integer, always
  naming **place + time window + weekday** ("From 3 to 6 p.m., have dinner with Ririko in the
  kitchen"). 30+ concurrent arcs stay legible with zero quest engine.
- GPG: **in-game per-NPC walkthrough checklists** with live sub-progress and condition spoilers
  revealed once the event is active.
- Become Someone: **girls-location radar** in the sidebar (every met girl + live link to where
  she is now — proof the NPC-radar works at 60-NPC scale), quest markers mirroring gate logic,
  **golden portraits** when a capstone is ready, and 238 in-fiction refusal hints that state the
  exact requirement ("after lunch from 13:00 till 16:00").
- The Company: per-NPC auto-timestamped **Notes journal**; serumStatus four lock-states each with
  an in-fiction "why not" line; ►/►► time-cost icons on every button.

### Scenes
- **In-scene escalation is a session meter**: Gakko self-linking "keep going" + `$lust>99` climax
  gate (453 passages); BTF dual pleasure bars; GPG sexskill = turn budget (more position switches
  per session); LaU 2–5-rung offer ladders inside every repeatable. Validates the sex-loop shape.
- **One scene name, N corruption-stage bodies** (The Company, Become Someone): entry passage
  switches its whole opener/choice set on dose/stage — repeatable scenes mature with the arc
  instead of multiplying passages.
- **Anti-repetition RNG** everywhere: GPG gym rolls 14–17 clip variants + occasional NPC
  encounter; LaU has 444 random() sites; Gakko either() per visit. Repeatables never render
  identical twice.
- Post-capstone: Become Someone routes conquered NPCs into **infrastructure** (strip-club
  staffing, startup employees, bedrooms in your mansion) — finished arcs keep generating value.

### Player-corrupts-NPC (our cascade premise) in the wild
- LaU's **Ava arc**: blackmail ladder keyed to cumulative extracted cash → you order her into
  park prostitution → you pimp her ($10-50/customer). The mirror-inversion (player gets the
  predator verbs used on her) is the game's most memorable beat. Luna = the wholesome
  contrast-friend who can independently fall (you find her at the brothel).
- Become Someone: girlfriend OR slave terminal state per girl (reversible), slaves staffed into
  businesses. Sluttown USA: per-resident chains paced by a rechargeable resource.

### Shipped anti-patterns (failure modes the field confirms)
- Dead dashboards (Gakko fame/charm; LaU gate-proximity blindness — `redlib` can park you at 79.5
  vs a `>80` gate with no feedback).
- Magic-number drift (LaU venue floors hygiene 30/40/50/60 with no system; one AND/OR bug makes
  the brothel never reject).
- God-passages (LaU 21KB PassageHeader with timed-goto interrupt hacks; GPG $act mega-router =
  72.7% of all gates are UI plumbing).
- One-way arc bricks (LaU model career permanently dead after a single no-show, vs 3-strike
  forgiveness elsewhere).
- RNG pacing with no pity timer (LaU uncle home = coin flip per visit, one rung per visit).

## 3. author-game skill review (vs the field)

### Strongly validated — keep, no change
1. **Two-axis double lock** (MC door + NPC's own lock) — RTS, Become Someone (trust+corr per
   rung), The Company (dose + relationship). The field's universal grammar IS our rung model.
2. **Rich-core/light-periphery (P5)** — every field game does this (Become Someone deep ladders
   for ~15, skeletons for 40; GPG 12 developed of 33).
3. **Throttle vs odometer** — Gakko's lust>99 climax gate + per-NPC `_lust` session meters vs
   permanent `_event` ladders is exactly the split.
4. **Daily caps** — The Company MaxDailyLove=2 + 20-pt milestone gifts; Become Someone
   `$todayRanEvent` / SexApp caps; LaU `$visituncletoday`. Universal.
5. **Economy as corruption ladder, earning = content, money ≠ content gate** — LaU textbook;
   0.7% money-gate share in the two biggest games. Our doctrine is exactly right.
6. **Reachability triad / schedules as data** — GPG per-girl 7-day×hour grids (and husbands'
   schedules = readable cheating windows); Become Someone 62 NPC loc1-7 tables.
7. **Honest locked-visible UI** — fakelinks + requirement tooltips field-wide.
8. **Feeder economy / player track** — LaU camshow/gloryhole/park columns tiered by Liberal
   mirror the step-5 archetype catalog almost 1:1.
9. **Sleep as router + day-tick** — universal; our day-cycle doctrine matches.
10. **npc_panel sidebar radar** — Become Someone proves it at 60-NPC scale.

### Gaps — HIGH value (recommend folding into the skill)
1. **Guidance concreteness rule.** Field best-in-class always names PLACE + TIME-WINDOW +
   WEEKDAY in the active hint (Gakko sidebar, Become Someone refusal hints). Our quest-card
   doctrine says "what·where·when" once (step-2 §5) but beat-authoring's card spec doesn't
   require it per rung. → Add to beat-authoring quest-card rules + npc_panel `next`: the active
   card/tip MUST name the location and schedule window verbatim, not just the goal.
2. **Failure-states-as-content (the debt cascade).** Every pressure system should default into
   an authored leverage/servitude arc BEFORE any ending (LaU's 3 creditors; our eviction_flag
   doctrine is the seed but only covers rent, and only as a gate). → step-2 §4 economy + step-5
   roster: each sink/pressure gets a "default cascade" roster row (rent → landlord leverage
   ladder; debt → forced lewd work chain), game-over only past the cascade.
3. **World-initiated pull (the biggest structural gap).** Our model is ~100% player-initiated;
   the field pulls the player constantly: neglect counters (BTF), sleep-hijack delivery
   (Become Someone), forced interrupts (BTF), quest-hijacked nav (GPG). Authorable with real
   knobs today: Tier-3 `neglect_<npc>` trait raised by `[engine.daily_tick]` traitEffects, reset
   by the hub-visit beat, auto-fire capstone-shape canvas gated `gte N` at the player's home /
   morning window ("she comes to you"). → New step-5 archetype (#11 "world-initiated pull") +
   lanes.md note; capstone-delivery doctrine: gate ready capstones to fire on the wake/sleep
   window so the mandatory daily click is the delivery channel.
4. **On-ramp stagger / season pacing.** Field paces arc openings across days (LaU day-N calendar,
   The Company real dates); we open everything at day 1. Authorable via flag-chains (meet A
   before B's intro arms) or schedule windows. → step-2 §5 pacing: stagger on-ramps in waves;
   the design book states which act each arc opens in.
5. **Cross-wiring as the depth driver.** We have cross_npc beats + casting threads, but the field
   lesson is stronger: depth = cross-NPC gates (mom needs sis stage 5), arcs feeding the economy
   (salary scales with boss-NPC's trained stats), conquest→infrastructure. → step-5 self-check:
   a minimum count of cross-NPC roster rows; step-4 §8 strengthened from "optional threads" to
   a budget.
6. **Post-capstone repurposing (conquest → infrastructure).** Our frontier doctrine gives a
   "livable steady-state"; Become Someone shows the concrete device — a completed arc's NPC gets
   an earning/staffing/standing-obligation repeatable so she keeps generating value (also the
   real cure for post-capstone dead presence). → step-4 repeatable-loop section + frontier rules.

### Gaps — MEDIUM (worth a line each, author-side patterns)
7. **Refusal costs**: optional small negative corruption on decline branches (LaU) — makes purity
   a build; CAUTION: pair with gate-proximity visibility or it re-locks content invisibly.
8. **Repeatable variety decks**: rotate 2-3 prose/media variants inside repeatable hubs/solo
   activities (GPG/LaU/Gakko all do); engine path: substitution variants / random-chance sibling
   canvases. Add to sex-loop + Lane-3 host guidance.
9. **Stat-buys-back-time**: if a game has an obligation system (shifts/classes), let a stat reduce
   the quota (LaU intellect/fitness formula) — progression felt as freedom.
10. **Travel friction**: small time (+ energy) costs on district moves make schedules matter;
    currently our games teleport.
11. **Repeatable-arms-one-shot**: solo feeder loops should occasionally trigger their arc's
    on-ramp at a usage count (Gakko masturbate→caught) — the on-ramp lives inside the grind loop.
    Authorable: feeder raises a hidden trait; auto-fire intro gates on it.
12. **Substitute gates** (drunk OR corruption): engine conditions are AND-only; emulate with
    parallel gated choices if wanted. Low effort, niche.

### Engine wishlist surfaced by the field (NOT skill changes)
- OR-combinator in conditions (substitute gates).
- Random variant selection among group blocks (anti-repetition decks).
- A gallery / completed-scenes ledger (Become Someone's 43%-of-passages replay museum; huge
  completionist pull, pure engine feature).
- Absolute-day predicate for canvas conditions (drip calendar without flag-chain workarounds).
- Map/nav badge for "live event here now" (Gakko's pulsing hotspots; we have NEW only for capstones).

### Divergences checked and kept
- **Endless frontier vs fixed run**: LaU's 303-day term works for ITS premise but produces brittle
  endings; our endless-frontier + season-pacing (gap 4) gets the structure without the wall.
- **Constant hub opener (D56-R1)**: field tier-swaps full SCENE bodies by stage (fine — our rule
  scopes only the hub base node; stage-keyed group variants in scenes/ambients remain allowed).
- **No hard game-over**: field uses game-overs heavily (LaU Gohome ×15 reasons) but always behind
  a cascade; our no-hard-ending stance + cascade arcs (gap 2) is strictly better for a sandbox.

## 4. Artifacts
- Full per-game agent reports: this session's transcript (2026-06-10); key numbers folded in above.
- New capture: `game_explorations/tl-life-at-university/` (890-passage catalog, static graph,
  variable index, live notes).
- Surveys sourced: gamcore.ch/html_spiele pages 1-6 (engine-fingerprinted via CDN HTML),
  mopoga.com /sandbox + /html tag pages.
