# The Inheritance — Mopoga-Alignment Work Plan

> **What this is.** The change-list from the 2026-07-24 top-30 mopoga Twine-sandbox study,
> expanded into self-contained work items. Each item is written so a FRESH session can pick
> it up alone: why (evidence), current state (verified against the game registry at book
> rev 21), exact scope, explicit NON-goals, engine notes + known gotchas, and a definition
> of done. Work ONE item per session unless stated otherwise.
>
> **The research this comes from** (read the cited sections before building):
> - Report: `~/Documents/Mopoga_Twine_Sandbox_Research_20260724/report.md` (findings F1–F10)
> - Per-game evidence: `.../notes/<slug>.md` (30 games), live-play: `.../livenotes/*.md`
> - Comment corpus: `.../digests/`, aggregates: `.../theme_matrix.csv`
> - Memory summary: `mopoga-top30-twine-study` (auto-memory)
> - Headline numbers: median grind complaints **0.9%** of comments; guidance-lost **4.7%**;
>   update-hunger **8.4%**. Lostness, not grind, is the genre's #1 killer (report F1).
>
> **Game state assumed by this doc** (verified 2026-07-24, `authoring_state.json` rev 21):
> `_active_beat: FINISH` — fix-pass done; media harvest + production build + re-list remain.
> 105 canvases / 20 locations / 7 NPCs (5 real arcs) / 37 flags / 25 traits / 8 quests.
> If the registry has moved substantially since, re-verify each item's "current state" line.
>
> **Protocol per session:** read this doc's item + the cited research sections → build →
> verify per the item's DoD → update the item's Status line here → append the decision to
> `authoring_state.json` decisions_log (LO's ledger discipline). Never hand-edit
> `7_final_game.toml`; edit `toml_phases/*.toml`, merge, package.

---

## Priority map

| # | Item | Priority | Status | Depends on |
|---|------|----------|--------|------------|
| 1 | Walkthrough-grade quest cards | P1 pre-ship | ✅ DONE 2026-07-26 (rev 23; goals[] labels + terminal frames; live-tested 46/46) | — |
| 2 | Player cheat page | P1 pre-ship | TODO | — |
| 3 | Ambient-heat layer (elision fix + wallpaper) | P1 pre-ship | TODO | media harvest |
| 4 | Meter-ceiling audit | P1 pre-ship | TODO | — |
| 5 | Nightly ledger at sleep | P1 pre-ship | TODO | (grows with #6) |
| 6 | Hotel accumulation loop | P2 design-change | ✅ DONE 2026-07-26 (rev 22; derived `hotel_level`; live-tested 26/26) | #5 helps |
| 7 | Soft consequences (world with teeth) | P2 **PENDING LO CALL** | BLOCKED on decision | — |
| 8 | Breadth: guest/staff light ladders | P3 post-ship | TODO | ship |
| 9 | Dangling-hooks audit | P1 pre-ship gate | TODO | all content final |
| 10 | Media insurance | P1 during harvest | TODO | runs WITH harvest |

Items 1, 2, 4, 5 are independent — safe to run in any order, one per session.
Item 3 needs the media harvest running or done. Item 6 is the big one; do it before
final media harvest if LO wants it in the ship build (it adds canvases + media slots).

---

## Item 1 — Walkthrough-grade quest cards

> **✅ BUILT 2026-07-26 (rev 23).** A render-model audit refined the scope: the Quests *page*
> already carried `ready_text` + `tip` (mostly walkthrough-grade), but the always-visible sidebar
> per-NPC "next" panel renders ONLY the goal block, so with almost no `goals[]` it was **dark for
> the whole game** — and the one `goals[]` (Audrey b2) **leaked a raw meter** ("Surrender — N/8").
> Per skill `quests.md` §3 (walkthrough rides `goals[].label`): added a **numberless flag goal** to
> each of the 13 active bands (goal flag = the band's own advance milestone → goal-met and band-exit
> coincide, no blank rows) and **`terminal = true`** to the 6 final bands (→ "✓ Arc complete"); fixed
> the Audrey b2 leak; added 2 cosmetic hidden flags (`aud_surrendered`, `ric_wants_you`) so the 2
> stage-gated bands light the sidebar without a number; tightened 2 tips. Edited `2_one_shots.toml`
> + `5_scenes.toml` only. Live-tested **46/46**. The scope below (append a line to card `text`) was
> superseded — on this engine `text` mostly doesn't render for active cards; the goal block does.

**Why.** Guidance-lostness is the genre's #1 complaint (median 4.7% of ALL comments;
report F1). Winners ship literal walkthroughs in-game: New Lust has per-NPC pages with
progress bars and "Locked (needs X)" labels (`notes/new-lust.md`); Course of Temptation's
HINTS cards each end with one concrete instruction — "Go to Summit Market (next to your
residence hall) and apply for a job" — and locked choices name their gate stat
(`livenotes/course-of-temptation.md` §2). Destroyer's walkthrough is one-line staged hints
in the NPC's own voice: "Buy a goddamn phone! Then meet me in the kitchen."
(`livenotes/destroyer.md`). Corpo Life shows the failure mode: zero grind complaints,
guidance the loudest theme, because its walkthrough lived off-site and died
(`notes/corpo-life.md`).

**Current state.** 8 quests in the registry: `spine_act1_get_house`,
`spine_act2_take_family`, `spine_frontier`, `audrey_x4`, `grayson_x3`, `richard_x3`,
`margaret_x3_warframed`, `lorna_x2`. Cards are RTS-doctrine one-sentence directives
(atmospheric, not instructional).

**Scope.**
1. For EVERY band of every quest ladder, append a concrete next-step line to the card
   body: **place + person + verb, plus time window if schedule-gated.** Keep the RTS
   directive sentence as line 1 (voice stays); the next-step line is line 2. Destroyer's
   NPC-voice trick is allowed where it fits the register (e.g. Lorna's cards can speak in
   Lorna's voice).
2. Gate visibility: where a band is trait-gated, the card TEXT states the tell in-world —
   not raw numbers, but unambiguous: "she isn't ready — keep the evening talks going" is
   too vague; "she won't go further until the lessons have gone further — bring her the
   next word" is right (names the repeatable that feeds the gate).
3. Verify NO band can show a met goal with no ready canvas — the known blank-next-row trap
   (memory: quest-card ladder). Every band's `when` window must have a reachable canvas.

**NON-goals.** Do NOT redesign the quest engine. Do NOT add new quests. Do NOT convert
cards to raw stat displays ("corruption 3/5") — the tell is in-world language that names
the concrete feeder, per the register.

**Engine notes / gotchas.** Quest cards = TOML `[[quests]]` with `when` predicates; bands
must be exclusive (stepped-ladder doctrine). Every conditions block needs
`version="1.0"` or it FAILS OPEN (memory: conditions-version-failopen). Quest `when`
supports trait predicates (v2.py:13873).

**Definition of done.** A cold reader can answer "what do I do next, where, when" for all
8 quests at every stage, from cards alone. Live-test (playwright harness, memory:
playwright-live-test): set each quest band's entry state, open Quests page, confirm no
blank rows, confirm each card names a place that exists. Build green.

**Size.** One session. Text-only TOML edits + one live-test pass.

---

## Item 2 — Player cheat page

**Why.** In ~25 of the 30 top games, the single most-liked comment is a cheat-code
request — pacing control is the genre's most universal demand (report F3). Games that
ship a free cheat valve get total grind amnesty: Apocalyptic World's default-on cheat
menu is one sidebar icon, and the game has ZERO grind complaints in 820 comments; its
menu doubles as documentation of what actually gates content
(`livenotes/apocalyptic-world.md` §7). We don't monetize, so free-valve is pure goodwill.

**Current state.** No player-facing valve. Dev-jumps exist (`6_dev_shortcuts.toml`) but
they're teleports and a dev tool (and note: dev-jump passages EMIT into prod builds —
memory: dev-jumps-engine — so tidy those separately at ship).

**Scope.**
1. One new always-open location or phone entry, diegetically skinned (suggestion: the
   hotel's old **master-key cabinet** — "some doors were always going to open for you").
2. Choices granting: +money (a few denominations), full energy, +1 arousal/corruption/
   exhibitionism, per-NPC relation/stage +1 (one choice per core NPC). Each choice is a
   plain effects block; repeatable; no conditions beyond `version="1.0"`.
3. A one-line label per choice saying what it touches — the AW lesson: the cheat menu IS
   the legend of the game's gating currencies.

**NON-goals — read this twice.** The cheat page grants **traits and money ONLY. It must
NEVER set story FLAGS.** Flags encode causality (`richard_signed`, `private_floor_open`,
`opening_done`...) — granting them skips scenes and can strand content behind never-fired
setters (the flag-chain validator only proves authored paths; a cheat bypassing them
voids that proof). Accelerate the climb, never skip the story. Also: no teleports (that's
dev-jumps), no day-skips (interacts with schedule windows and daily flags).

**Engine notes / gotchas.** Trait grants via standard effects. If any ITEM is granted, the
key is `itemEffects` (camelCase — snake_case is silently dropped; memory:
item-economy-itemeffects). Stage traits (`audrey_stage` etc.) — check whether stages are
derived or directly-set before touching them; if derived from relation, bump relation only.
Non-navigating mutators need the moment-commit guard the engine already applies to choices
(memory: moment-commit) — use normal choice blocks, nothing exotic.

**Definition of done.** From a fresh save: earn nothing, cheat to mid-game trait levels,
confirm every story gate still requires its authored scene chain (spot-check the 3 spine
flags stay false). Build green; page reachable; every choice fires and notifies.

**Size.** One short session. ~1 canvas.

---

## Item 3 — Ambient-heat layer (elision fix + wallpaper)

**Why.** Two evidence lines. (a) Register: the pending arousal-axis fix — skill Rule 9
(player-as-erotic-subject, show-the-act anti-elision; memory: author-game-arousal-axis)
was added to the skill but The Inheritance's scenes predate it; the game reads cold-noir
between and DURING acts. (b) Wallpaper: Destroyer re-rolls looping porn clips from
per-location pools on EVERY hub render (shop pool 26 clips, gym pool 56) so the game is
never dry even when the next scripted scene is 15 stages away
(`livenotes/destroyer.md` §4); porn-as-wallpaper vs porn-as-payoff is the tier structure
that keeps players warm (report, live-play addenda).

**Current state.** Sex scenes authored pre-Rule-9 (elision audit never run on this game).
No ambient media layer; hubs are dry prose between beats. Feeder canvases exist
(`feeder_channel`, `feeder_get_off`, `feeder_mirror`) but they're player-solo verbs, not
environmental heat.

**Scope.**
1. **Elision pass:** audit every L2/L3/L4 sex scene against Rule 9's checks (the act is
   shown, not cut away from; the player is the erotic subject, not the camera). Rewrite
   offenders. Keep beats ~35-40 words; heat comes from specificity, not length
   (the caption-over-clip economy is validated at market scale — report F5, Become Taxi
   Driver median ~36 words/passage).
2. **Wallpaper:** 2–4 short glimpse-ambients per PUBLIC hub (lobby, bar, the floor —
   places where a hotel sliding into vice would leak heat): ~30-word beat + clip,
   `trigger_mode=random` + chance, repeatable. The engine re-rolls random ambients on
   every location render (memory: sealed-room notes) — that's exactly Destroyer's
   mechanic. Escalate pools by hotel state if/when Item 6 lands (hotter glimpses as the
   house turns).
3. Add the needed clips to the media harvest list (this item feeds `find-media`).

**NON-goals.** No new NPC story content in ambients — glimpses are anonymous/staff/guest
texture, never plot. No purple prose. Do NOT touch L1 hub base descriptions' length
budget. Private/family spaces stay cold until the story heats them — the contrast is the
game's register; wallpaper belongs to the public-vice spaces.

**Engine notes / gotchas.** Ambient bucket = `trigger_mode=random` + chance, no `npc=`
(memory: canvas-lane-render-buckets). If any ambient gets `max_triggers_per_day=1`,
beware the midnight-straddle double-fire (memory: engine-daygate). Only ONE repeatable
npc-bound canvas per loc+NPC+window — keep ambients NPC-unbound to dodge it entirely.
Every conditions block: `version="1.0"`.

**Definition of done.** Elision: a re-read of every sex scene passes Rule 9's checklist
(record pass/fail per scene in the session log). Wallpaper: live-test — 10 renders of
each public hub produce visibly rotating glimpses; `--debug` build shows zero
[VIDEO MISSING] for new slots (ship-gate discipline: memory video-media-blocks — final
build has NO --debug/--dev and greps MISSING==0).

**Size.** Two sessions (one elision, one wallpaper+media-list). Needs harvest for clips.

---

## Item 4 — Meter-ceiling audit

**Why.** Family Business: players accept brutal repetition while every bar-fill buys a
new act — the moment a maxed meter returns "she is not ready," the loop reads as a
paywalled insult (`notes/family-business.md`, one_lesson: "cap the meter at the content,
never past it"). Confined & Horny shows the adjacent failure: escalation debt — meters
imply a payoff that never ships and fans call the update "insulting"
(`notes/confined-and-horny.md`).

**Current state.** 25 traits incl. `corruption`, `exhibitionism`, `arousal`, `energy`,
`money`, per-NPC `relation/corruption/arousal`, and stage traits (`audrey_stage`,
`grayson_stage`, `richard_stage`). Never audited for ceiling-vs-content since the v2
re-author.

**Scope.**
1. Script a pass over the MERGED game TOML: for each gating trait, extract (a) the
   highest threshold any condition references, (b) the maximum value reachable via
   authored effects. Flag every trait where reachable-max > highest-content-threshold.
2. For each flagged trait: either cap the effects (stop granting past the last gate) or
   confirm a terminal state consumes the top band (e.g. a terminal status_text band that
   NAMES itself terminal — "she has no lines left" — so the number can't promise more).
3. Check `trait_status_text` bands cover the full reachable range — no band-gap prose
   holes (memory: quest-card + trait_status_text doctrine).

**NON-goals.** No new content to "fill" ceilings — this item CAPS, it doesn't author.
(If a cap reveals a content hole worth filling, log it as a candidate for Item 8.)

**Engine notes / gotchas.** Do NOT audit from the compiled `trait_effects` JSON — it's a
value>0-filtered PREVIEW; the real apply is the HTML-escaped `applyAndNotifyTrait`
script from raw config.effects. Audit the SOURCE TOML, and if grepping built HTML,
decode entities first (memory: trait-effects-json-is-preview).

**Definition of done.** A table in the session log: trait | max reachable | last content
gate | verdict (ok / capped / terminal-band-added). Zero traits where the number can
climb past the last authored payoff. Build green.

**Size.** One session. Mostly a script + small TOML edits.

---

## Item 5 — Nightly ledger at sleep

**Why.** Apocalyptic World prints a categorized morning report every sleep ("Net change,
produced(+) and consumed(-)... -1 Food") — it's half of why its systems feel alive; the
world visibly ticks (`livenotes/apocalyptic-world.md` §2c, §3). Free Cities is built
ENTIRELY on the weekly end-turn report and its players call the management loop itself
the fantasy (`notes/free-cities.md`). We track state; we just never show the day's delta.

**Current state.** `activity_sleep` canvas exists; daily flags exist and reset:
`worked_floor_today`, `photos_sold_today`, `bathed_today`, `ate_today`, `preened_today`.
No summary is rendered anywhere.

**Scope.**
1. Extend the sleep→wake scene with a short conditional ledger block: one line per
   daily flag that fired ("The floor was worked. The take is banked." / "Photos went out.
   Someone, somewhere, is looking at you."), rendered flat, RTS register, ≤1 line each.
2. If Item 6 lands: add the hotel income/state line here ("The house earned while you
   slept.") — the ledger is where accumulation becomes visible daily.
3. Keep it skimmable: max ~5 lines, only lines whose flag/state is true.

**NON-goals.** No engine templating work — this is conditional TOML blocks on existing
flags, not computed sums. No stats-dump (the sidebar already shows money); the ledger is
NARRATIVE confirmation the day happened, not a spreadsheet.

**Engine notes / gotchas.** Conditional blocks on flags — every conditions block needs
`version="1.0"`. Two independent conditional ladders in one node: adjacent [group] blocks
MERGE into ONE if/elseif chain — separate independent ladders with a non-group block
between them or the second ladder is dead code, build stays green (memory:
adjacent-groups-merge).

**Definition of done.** Live-test: a day where floor was worked + photos sold renders
both lines; a lazy day renders none; no group-merge dead code (verify each line CAN fire
in one run). Build green.

**Size.** Half a session. Pure TOML.

---

## Item 6 — Hotel accumulation loop (the big one)

> **✅ BUILT 2026-07-26 (rev 22).** Full spec + as-built: `design_item6_hotel_level.md`.
> A read-only audit found the compounding loop **already existed, invisibly** (money → the
> `escort_upgrade`/`private_floor_open` back-office sinks → higher-income venue tiers), so the
> build **gave it a face** rather than building a new loop. Key refinements vs the scope below:
> `hotel_level` is a **hidden DERIVED** trait SET at the three existing story beats (NOT a new
> bought trait — avoids duplicating the sinks + competing with `corruption`); the hub reskin is
> **prose-only** raw `<<if>>` macros in each `description` (**media-neutral**, no per-level images —
> that's Item 3); the spine card was **refined in place**, split on `richard_signed` (the real
> phase boundary) instead of adding a colliding `spine_house` ladder. Passive income + ledger +
> regression guard all as scoped. Live-tested 26/26. Original scope preserved below for reference.

**Why.** Report F2/F4 + the "what IS a top game" model: winners are engines of
accumulation with NPC arcs hanging off them — settlement (Apocalyptic World: content
gates on BUILDINGS, not stat bars; `livenotes/apocalyptic-world.md` §4), empire
(Patriarch: money → soldiers → city laws → new girls makes farming feel like conquest;
`notes/patriarch.md`), business/genealogy (Inseminator), brothel income (Amore). The
save file must become YOURS — that's why people run Degrees of Lewdity for 900 in-game
days. The Inheritance's fantasy is literally "this house becomes yours" — the theme and
the missing mechanic are the same sentence. This also closes the old pre-ship-audit
"income apex" gap.

**Current state.** Money sources exist (`activity_work_floor`, `activity_sell_photos`)
and money gates exist early, but money has no late-game purpose (no sinks, no growth
object). `private_floor_open` flag exists (story-driven). Renown was discussed in the
Step-6 review (a "renown split" gap was refuted — check the book §world before naming a
new currency). Nothing visibly compounds.

**Scope (agreed direction; needs ONE design pass with LO for names/prices before build).**
1. A hidden `hotel_level` trait, 0→3, four states with in-world names (working titles:
   **0 dust sheets → 1 the bar pours again → 2 the private floor earns → 3 the house
   full**). Level-ups are BOUGHT with money at a fixed sink each, AND gated on the story
   flags that justify them (level 2 requires `private_floor_open`; level 3 sits behind
   the Act-2 keystones — exact flags from the book, e.g. `richard_signed` and the
   Grayson buyout flag). Money buys speed; story buys permission. Both, always.
2. Each level visibly changes the PUBLIC hubs: conditional hub-prose variants + (with
   Item 3) hotter wallpaper pools per level. The house LOOKS different as it turns.
3. Income: from level 2, sleeping grants money scaled by level (implementation: prefer
   conditional effects in the sleep canvas keyed on hotel_level — zero engine work;
   VERIFY in-session whether `[engine.daily_tick]` can grant money conditionally, the
   arousal system uses daily_tick, but sleep-canvas conditionals are the safe fallback).
   Income prints in the Item-5 ledger.
4. One new quest ladder, `spine_house` (stepped bands on hotel_level per quest-card
   doctrine, every band with a ready canvas), whose cards follow Item 1's format — this
   is the player's visible "what my money is FOR."
5. Price the sinks against the current economy: audit total earnable/day from floor+
   photos mid-game, set level costs so level 1 is reachable in Act 1, level 3 lands
   with the Act-2 apex. Log the arithmetic in the session log.

**NON-goals.** NOT a management minigame: no staff hiring UI, no per-room assignments,
no upkeep failure. Levels never DECREASE (no decay — that's Item 7's territory and it's
pending). No new NPCs. The loop is: earn (existing verbs) → spend (new sinks) → see it
(hub states + ledger + wallpaper) → repeat.

**Engine notes / gotchas.** Hidden trait: `[[traits.labels]] hidden=true` suppresses
sidebar display (memory: hidden-traits-engine). Flag-chain validator wants a LOCATED
setter for flags required by triggers — hotel_level is a TRAIT, which dodges the
validator by design (memory: flag-chain-validator-located-setter). Hub-prose variants:
watch the adjacent-group merge (Item 5 note). New canvases with money effects: effects
deduct but never gate — gates go in costs/conditions (memory: energy-costs-vs-effects).

**Definition of done.** Live-test a full arc: start broke → work the loop → buy level 1
→ hub text changes → level 2 behind `private_floor_open` + cash → sleep income appears
in ledger → level 3 behind Act-2 keystones. Quest ladder shows correct card at every
level with no blank rows. Economy arithmetic logged. Build green.

**Size.** 2–3 sessions: one short design pass (state names, prices, exact keystone flags
— LO in the loop), one build, one live-test/tune. Do BEFORE final media harvest if it
ships in v2.0 (its hub variants + wallpaper add media slots).

---

## Item 7 — Soft consequences (world with teeth) — **PENDING LO's CALL, DO NOT BUILD**

**Why (the case FOR).** Course of Temptation's sharpest complaint, 32 likes: "I can go
out anywhere... and NOTHING happens to me" — its players beg for risk/pregnancy/scandal,
not more scenes (`notes/course-of-temptation.md`, report F9). DoL's identity is danger
embedded in routine. AW ships instant-death forks. A world that can't push back reads
as dead.

**The tension (the case AGAINST).** The v2 book deliberately re-confirmed **no
fail-state** (blueprint.wiring, feedback verdict). This item bends a locked decision —
that's why it's parked until LO rules on it.

**Pre-agreed shape IF approved** (so the future session doesn't reinvent): Margaret is
already cast "pressure source + late-act pressure." Consequences stay SOFT: she can cost
money (a fine, a "correction" to the books), close a door for N days (flag + day-gate,
auto-reopens), or take a scene of humiliation-pressure if the player is sloppy in public
(fed by a hidden `suspicion` trait raised by risky public acts, spent/reset by her
beats). NO game-over, NO permanent content locks, NO decay of hotel_level. Danger is
texture and stakes, never a wall.

**Definition of done (if approved).** Every consequence is recoverable within ~3 in-game
days; live-test that no consequence can strand a quest band (blank-row check re-run).

**Size.** 1–2 sessions after approval.

---

## Item 8 — Breadth: guest/staff light ladders (post-ship)

**Why.** Top games run 20–75 parallel ladders; we run 5 real arcs. Breadth is what
guarantees "always something to nudge" (report, "what IS a top game" §3). Our Step-6
check confirmed ≥3 non-grind threads/day — the honest minimum, not comfort.

**Scope (frontier work, post-ship).** 2–4 LIGHT NPCs (hotel guests / staff hired as the
house grows — natural fit ON TOP of Item 6's levels: new faces appear at level 2/3).
Each: 2–3 canvas micro-ladders (feeder-economy shapes per content-design.md), portrait
bucket, schedule row. NOT core arcs, no quests beyond maybe one shared "the house's
people" card.

**Gotchas.** Inserting `[[npcs]]` — a new NPC inserted BETWEEN an existing NPC and its
`[[npcs.schedules]]` silently re-attaches the schedule to the wrong NPC and the build
stays green: APPEND new NPCs AFTER the prior NPC's schedule block and grep-verify
(memory: npc-schedule-orphan-on-insert). One repeatable npc-bound canvas per
loc+NPC+window (memory: engine-daygate).

**DoD.** Each new NPC reachable, scheduled, portrait renders, ladders fire; day-breadth
re-check shows ≥4 threads.

---

## Item 9 — Dangling-hooks audit (ship gate)

**Why.** Sluttown's players quote its unpaid hooks BY NAME years later ("Are we EVER
going to talk to the university president?" — 24 likes; `notes/sluttown-usa.md`):
planted names are debts. Vesper's 1b deferral taught us the same.

**Scope.** Before the production build: grep the full merged TOML scene text +
`spine_frontier` cards for named promises (characters teased but sceneless, "one day,"
"soon," doors described as openable-later). For each: pay a minimal beat, cut the name,
or make the deferral explicit and terminal in-fiction (the Vesper 1a-close pattern —
"build(vesper): defer 1b — 1a close is now terminal"). Log every hook found + verdict.

**DoD.** Zero named, sceneless promises in the ship build. Runs LAST, after all other
content items land.

---

## Item 10 — Media insurance (runs WITH the harvest)

**Why.** Lust for Life was legally forced to swap all real-porn media for AI art — every
top-liked comment is the revolt (138/135/126 likes) and the game died of it overnight
(`notes/lust-for-life.md`). High School Days' actress retirements forced quest REWRITES
(`notes/high-school-days.md`). GrowUp recast its performer-NPCs and got "I want my mom
back" + abandonment (`notes/growup.md`). Zara's crops faces specifically so the NPC
isn't married to one performer (`notes/zaras-school-life.md`). The performer corpus IS
the content plan; treat it as a first-class risk.

**Scope (fold into the imminent find-media run):**
1. **Archive:** keep a full local copy of every harvested asset OUTSIDE the build tree
   (media is git-ignored — memory: games-tracked-media-ignored — so the repo is NOT a
   backup; a plain rsync target + the manifest is).
2. **Manifest:** per asset — source URL, query used, date, per-NPC role. (The find-media
   skill's evidence files already carry most of this; make sure they're retained, not
   scratch.)
3. **Casting rule for identity media:** for NPC-identity slots (portraits, signature
   scenes of Audrey/Margaret), prefer face-light/croppable framing so a performer can be
   replaced without the NPC dying. Scene-media (acts) can be freer. Do not name
   performers anywhere in prose.

**DoD.** Manifest exists + archive verified (spot-restore 3 files); identity slots
reviewed against the casting rule.

---

## Appendix — cross-item engine gotchas (check before ANY session)

Full detail lives in auto-memory; the ones that bite these items:
- **conditions need `version="1.0"` or FAIL OPEN** — every block, no build error.
- **Adjacent `[group]` blocks merge into one if/elseif chain** — dead second ladder,
  green build (v2.py:13649-13662). Separate with a non-group block.
- **`itemEffects` is camelCase** — snake_case grants are silently dropped.
- **trait_effects JSON in built HTML is a filtered PREVIEW** — audit source TOML, or
  decode the `applyAndNotifyTrait` script entities.
- **NPC insert orphans schedules** — append after the prior NPC's schedule; grep-verify.
- **`max_triggers_per_day=1` midnight-straddle double-fire** — keep daily windows inside
  one calendar day.
- **Effects deduct but never gate** — gating goes in costs/conditions.
- **Ship build:** `--video-folder`, NO `--debug`/`--dev`, grep built index.html for
  `IMAGE MISSING`/`VIDEO MISSING` == 0 (a --debug ship once baked 147 placeholders into
  live Vesper). Dev-jump passages emit into prod — strip/verify at ship.
- **Never hand-edit `7_final_game.toml`** — phases → merge_toml_phases.py → package.

*Doc created 2026-07-24 from the mopoga top-30 study. Owner: LO + ENI. Update Status
lines here as items land; keep `authoring_state.json` decisions_log in sync.*
