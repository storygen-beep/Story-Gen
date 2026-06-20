# PRD — Trigger-Prose Fix Pass (Per-Canvas)

> **Methodology: case-by-case.** Each canvas is diagnosed and fixed on its own merits. No master patterns assumed; no shared infrastructure built ahead of need. This doc records the chosen solution per canvas. Execution is downstream — nothing here is implemented until explicitly approved per-canvas.

**Created:** 2026-04-27
**Execution complete:** 2026-04-27 — all 26 pending canvases implemented in `2_story_canvases.toml`; 6_final_game.toml regenerated; `package_from_toml --dry-run` passed cleanly (73 canvases / 125 nodes / 38 locations / 12 NPCs / zero warnings).
**Owner:** Aman + Claude
**Bug class:** Prose hardcodes day/hour/week/season/prior-actions that the canvas trigger doesn't enforce. See `standards.md` Rules 27 + 28 and `qa_rubric.md` "Trigger-prose binding" section for the rule definitions this pass enforces.

---

## Status legend
- `pending implementation` — solution decided in this doc, not yet edited into the TOML
- `implemented` — TOML edited; `package_from_toml --dry-run` passes
- `verified` — playtested in browser; canvas fires correctly post-fix

---

## Canvas #1 — frank_phase_a_test ("The Porch Light")

**TOML location:** `2_story_canvases.toml:1041`
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Prose surgery only — no trigger changes, no engine changes

### Diagnosis
The canvas has the worst severity in the file: it claims a specific time *and* retcons an action Maya never took. Trigger condition is `first_rent_paid is_true` only — fires on any porch visit after rent (could be Tuesday W3 3pm). Prose lies about the day, the hour, AND the porch-light-leaving event.

### Chosen solution
Three surgical edits to the prose blocks. Frank's correction beat (the no-verb *"Maya. / The porch light."*), the kitchen-toggle detail (*"the low oak toggle he had put in the week she moved in"*), and Maya's three-Mayas-in-her-mouth beat all stay verbatim. The description metadata at line 1043 is left alone — it's authorial scaffolding, not player-facing.

#### Edit 1 — line 1058 (decorative time/season anchor)

**ORIGINAL:**
> *"She had come out onto the porch at eight-thirty with the dish towel still on her shoulder because she had thought she was going to say she was going upstairs. The porch at eight-thirty on a Sunday in early July was the hour the light had gone out of the sky without turning the yard black yet — dusk held on the rosemary at the railing and on the white of the far fence and on the grass at the edge of the gravel..."*

**REWRITE:**
> *"She had come out onto the porch with the dish towel still on her shoulder because she had thought she was going to say she was going upstairs. The hour the light had gone out of the sky without turning the yard black yet — dusk held on the rosemary at the railing and on the white of the far fence and on the grass at the edge of the gravel..."*

Strips: "at eight-thirty" (twice), "on a Sunday in early July." Preserves the dusk-light register entirely.

#### Edit 2 — line 1065 (decorative week-anchor)

**ORIGINAL:**
> *"...and she had been in the house long enough now, at the end of the fourth week, to hear the absence of the verb as the loudest part of the sentence."*

**REWRITE:**
> *"...and she had been in the house long enough now to hear the absence of the verb as the loudest part of the sentence."*

Strips: ", at the end of the fourth week,". Preserves the temporal-arrival register ("long enough now") which doesn't claim a specific week.

#### Edit 3 — line 1066 (the retcon — most important)

**ORIGINAL:**
> *"She had flipped the toggle on when she came home on Saturday at one in the morning from a shift that had gone long. She had meant to flip it off before bed. She had not. He had come out for the paper at seven and seen it on. He had not said anything at breakfast. He had waited until Sunday evening. *That was the agreement,* he was not saying, and she heard the not-saying."*

**REWRITE:**
> *"The porch light he'd asked her not to leave on past midnight had been on, last shift-night home. He had seen it the next morning. He had not said anything at breakfast. He had waited until tonight. *That was the agreement,* he was not saying, and she heard the not-saying."*

What changed:
- Active retcon ("She had flipped the toggle on") → passive consequence ("had been on")
- "Saturday at one in the morning" → "last shift-night home" (matches whatever the player's last actually-late shift was, or just reads as ambient)
- "Sunday evening" → "tonight"
- Frank's not-said line preserved exactly

### Why this works
- The Maya-action retcon is the actual rule violation (Rule 28). Passive voice removes the false claim.
- Day/hour anchors are atmospheric, not load-bearing — Frank's correction-discipline works on any evening she's slipped (Rule 27).
- The canvas fires once per playthrough (`is_repeatable = false`), so we don't need temporal gating to prevent re-fires in mismatched states.
- Frank's correction beat — the no-verb "Maya. / The porch light." — never had any time-anchor in it. It carries the scene.

### Verification (when implemented)
1. Read the rewritten canvas top-to-bottom — Frank-Phase-A register intact, three-Mayas-in-her-mouth beat intact.
2. `package_from_toml --dry-run` — counts unchanged from current dry-run.
3. Browser playtest: walk Maya from arrival → first rent paid → visit porch on a non-Sunday afternoon. Confirm canvas fires (it should — trigger is unchanged) and confirm prose no longer claims Sunday/8:30/Saturday-1am/Week-4.

---

## Canvas #2 — first_ryan_encounter ("Wrench'd Help")

**TOML location:** `2_story_canvases.toml:585`
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Prose surgery only — no trigger changes, no engine changes

### Diagnosis
First Maya-Ryan exchange. Trigger gates on `first_morning_kitchen_done` which already places Maya in Sunday W1 vicinity. The prose hardcodes "two in the afternoon on a Sunday in early June" — afternoon hour and June season are decorative, the Sunday is approximately enforced by the upstream flag chain. Ryan's character voice (fragments, *kid* endearment, hands-doing-something) is the load-bearing craft and stays untouched.

### Chosen solution
Two surgical edits.

#### Edit 1 — line 602 (kitchen_bridge sub-node, decorative time anchor)

**ORIGINAL:**
> *"Two in the afternoon. Diana was at the sink rinsing the dishes Maya had pushed aside half an hour ago..."*

**REWRITE:**
> *"Diana was at the sink rinsing the dishes Maya had pushed aside half an hour ago..."*

Strips the opening "Two in the afternoon." sentence-fragment. The half-hour-ago anchor and the dish-rinsing scene set time-of-day register implicitly without claiming a specific clock hour.

#### Edit 2 — line 617 (base sub-node, the main time-anchor)

**ORIGINAL:**
> *"The yard at two in the afternoon on a Sunday in early June had the particular heat of a Southern day that had not yet peaked..."*

**REWRITE:**
> *"The yard had the particular heat of a Southern day that had not yet peaked..."*

Strips "at two in the afternoon on a Sunday in early June." Preserves the heat register, the cut-grass smell, the bee on the honeysuckle, the three-note bird call — every load-bearing sensory detail.

### Why this works
- Trigger flag `first_morning_kitchen_done` chains naturally from arrival → first kitchen morning → Maya going to find Ryan. The "Sunday" feel is approximately preserved by the flag chain even without naming it.
- "In early June" is a season-anchor; game is in June/July range per the cicada anchors elsewhere — keeping it isn't wrong but stripping it removes one more source of calendar drift if the player takes a non-default path.
- Ryan's *Wrench'd help* / *Thanks, kid.* dialog beats and the wrench-handoff body language carry the scene.

### Verification (when implemented)
1. Read post-edit — Ryan's character voice (fragments, *kid*, body) intact; Maya's observation register intact.
2. `package_from_toml --dry-run` — counts unchanged.
3. Browser playtest: walk Maya from arrival → first kitchen morning → loc_yard. Confirm canvas fires; confirm prose no longer claims "two in the afternoon" or "early June."

---

## Canvas #3 — frank_restrict ("The New Rules")

**TOML location:** `2_story_canvases.toml:1651`
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Prose surgery only — no trigger changes, no engine changes

### Diagnosis
Frank-arc beat that fires after `frank_caught` flag. Prose anchors to "Friday the twenty-second" and "six-forty-five" — Friday-morning-after-the-Tuesday-catch is the diegetic shape, but the trigger doesn't enforce day-of-week and the catch canvas itself is Wednesday (per `frank_catch_living_room`'s description "W8-9 Wed 23:30"), making "two days after the Tuesday of the living room" internally inconsistent with its own arc continuity. Plus a callback to "the porch in July" that re-anchors `frank_phase_a_test`'s month after we just stripped that anchor in Canvas #1.

### Chosen solution
Two surgical edits — one for the opening calendar claim, one for the porch callback to keep continuity with Canvas #1's neutralization.

#### Edit 1 — line 1668 (calendar opening anchor)

**ORIGINAL:**
> *"Friday the twenty-second had come two days after the Tuesday of the living room. The kitchen at six-forty-five was the kitchen the house had in it on a weekday morning before Frank went out to the truck — bacon on the cast-iron at the stove..."*

**REWRITE:**
> *"The morning after had come two days after the night of the living room. The kitchen at the breakfast hour was the kitchen the house had in it on a weekday morning before Frank went out to the truck — bacon on the cast-iron at the stove..."*

Changes:
- "Friday the twenty-second" → "The morning after" — drops both the weekday name and the calendar-day number
- "Tuesday of the living room" → "night of the living room" — drops the weekday claim that doesn't match `frank_catch_living_room`'s actual Wednesday positioning anyway
- "at six-forty-five" → "at the breakfast hour" — atmospheric register preserved; specific clock dropped

#### Edit 2 — line 1677 (porch callback to Canvas #1)

**ORIGINAL:**
> *"the way he had not said a verb between her name and the object on the porch in July"*

**REWRITE:**
> *"the way he had not said a verb between her name and the object on the porch the night of the porch light"*

Drops "in July." Replaces with a referential anchor ("the night of the porch light") that points unambiguously at `frank_phase_a_test` without claiming any specific month. Reinforces the cross-canvas callback narratively.

### Why this works
- Frank's three-rules speech is the scene's craft and stays verbatim — *Common areas are locked after midnight.* / *There will be an extra chore each week. I will assign it on Sunday.* / *We will talk about shared spaces.* — every word preserved.
- Diana's spatula-stopped-at-the-bacon body register stays intact.
- The "two days after" interval is preserved as an interval (it just isn't "two days after specifically Tuesday" anymore — works for any day pairing).
- The grammar-as-character analysis ("the future-passive...") and the *shared spaces* / *the verb between them* connection to Canvas #1's no-verb correction architecture all stay.

### Verification (when implemented)
1. Read post-edit — three-rules speech word-perfect; Diana spatula-frozen body intact; *shared spaces* echo to Canvas #1 still legible.
2. `package_from_toml --dry-run` — counts unchanged.
3. Browser playtest: walk Maya through the catch → next morning kitchen. Confirm canvas fires; confirm prose no longer names a weekday, a calendar-date, or "in July."

---

## Canvas #4 — ryan_beach ("The Beach")

**TOML location:** `2_story_canvases.toml:1448` (5 sub-nodes)
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Prose surgery only — no trigger changes, no engine changes

### Diagnosis
Tier-A Crack scene. ~1500w of carefully-rewritten prose across 5 sub-nodes (ride_east → lake_arrival → line_crossing → the_ask → the_answer). The "Stay with me" sentence — Ryan's only complete sentence in the whole arc — lands after ~1300w of setup. The lake geography, Ryan's fragments, Maya's Operating-band FID, and the three character-action exit choices are all sacred. Hardcoded anchors are confined to ride_east (N1) and one callback in the_ask (N4); everything else is atmospheric without specific clock or weekday claims.

### Chosen solution
Four surgical edits across two sub-nodes. Sub-nodes lake_arrival, line_crossing, and the_answer are untouched.

**Critical preservation:** The_ask sub-node's *"Stay with me."* dialog block (line 1528), Ryan's first-time naming Maya at line 1524, and the lake geography ("an hour east," "scrub pine," "weak-tea brown water") all stay verbatim.

#### Edit 1 — line 1466 (N1 ride_east, opening time anchor)

**ORIGINAL:**
> *"He picked her up at the end of the driveway at six forty-five. The light was the slow cooling kind that the South gave you for an hour on a summer Sunday before the heat climbed back up off the road."*

**REWRITE:**
> *"He picked her up at the end of the driveway before the heat had come up. The light was the slow cooling kind that the South gave you for an hour on a summer morning before the heat climbed back up off the road."*

Changes:
- "at six forty-five" → "before the heat had come up" — drops specific clock; preserves the dawn-register
- "summer Sunday" → "summer morning" — drops weekday; preserves the heat-cycle observation

#### Edit 2 — line 1468 (N1 ride_east, "seven AM in July")

**ORIGINAL:**
> *"Hot vinyl. The sweet warm smell of the dashboard at seven AM in July."*

**REWRITE:**
> *"Hot vinyl. The sweet warm smell of the dashboard in early summer light."*

Drops "seven AM in July." Preserves the sensory beat — hot vinyl + sweet warm dashboard smell — which carries the cab-interior register.

#### Edit 3 — line 1470 (N1 ride_east, "Sunday morning after the farmer")

**ORIGINAL:**
> *"...and the quiet in the truck cab on the Sunday morning after the farmer was different in a way she did not yet have the word for."*

**REWRITE:**
> *"...and the quiet in the truck cab on the morning after the farmer was different in a way she did not yet have the word for."*

Drops "Sunday." Callback to `ryan_big_ticket_deal` (the farmer-close) preserved as a referential anchor.

#### Edit 4 — line 1525 (N4 the_ask, the naming-callback)

**ORIGINAL:**
> *"The first time her name landed in his mouth was on the towel at the lake on the Sunday after the back office."*

**REWRITE:**
> *"The first time her name landed in his mouth was on the towel at the lake on the morning after the back office."*

Drops "Sunday." The "back office" referential anchor to `ryan_big_ticket_deal` is preserved.

### What's deliberately NOT touched

- N5 the_answer choice text *"Ask me again in August."* — stays. This is Maya's player-voice dialog. Calendar-coupled but diegetic; if the game starts late June (per cicada anchors elsewhere), Week 7 ≈ mid-August anyway. Maya naming the month she's living in reads as natural and we'd lose nuance by softening to "later."
- N2 lake_arrival "the navy one she had bought at the general store in week three" — soft week-anchor inside a callback memory. Maya knowing she bought a swimsuit a few weeks ago is fine; it's a memory, not an active scene-time claim.
- N3 line_crossing "since Saturday in the back office at the shop with the farmer" — stays. Direct callback to `ryan_big_ticket_deal` which is structurally Saturday. Cross-canvas continuity rather than retcon.

### Why this works
- Four edits, all confined to time anchors that don't carry character work. The Stay-with-me Crack lands the same way it always did.
- Ryan's fragments-only voice rule preserved everywhere except his ONE allowed complete sentence (the_ask).
- Maya's Operating-band FID register (long subordinated observational sentences, possessive surfacing — "her cut," "she had not cried") preserved across all 5 sub-nodes.
- Lake geography (an hour east, scrub pine, weak-tea-brown water) stays — that's load-bearing not decorative.
- The cross-canvas callbacks to `ryan_big_ticket_deal` ("the back office," "the farmer") read cleaner without "Sunday/Saturday" claims since those need to land in their own canvases' scope.

### Verification (when implemented)
1. Read all 5 sub-nodes top-to-bottom — Stay-with-me beat lands, Ryan's name-landing moment intact, three character-action exit choices preserved with all flag/effect values.
2. `package_from_toml --dry-run` — counts unchanged.
3. Browser playtest: trigger ryan_beach via the upstream flag chain, walk through all 5 sub-nodes, confirm prose no longer claims "six forty-five," "seven AM in July," or "Sunday" anywhere; confirm "Stay with me" is still Ryan's first complete sentence in the arc.

---

## Canvas #5 — cookie_peer_established ("Back Step")

**TOML location:** `2_story_canvases.toml:927`
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block only — no prose changes, no engine changes, no week-gate

### Diagnosis
Cookie's intel-transfer monologue at the back step. Trigger gates only on `diner_regulars_named is_true`. The prose is *correct* — Cookie literally enumerates the week's regulars by day ("Thursday's trucker night... Pete's Tuesdays only, he doesn't Thursday... Church couple Saturdays"). The whole scene is Thursday-night content. The fix is to make the engine match the prose, not the other way around. The prose stays untouched.

### Chosen solution
Add a single `[[canvases.trigger.schedules]]` block to lock firing to Thursday evening. No prose edits.

#### Edit 1 — insert after line 937 (the existing trigger.conditions line)

**INSERT block:**
```toml

[[canvases.trigger.schedules]]
weekdays = [3]              # Thursday
start_time = "20:00"
end_time = "22:00"
```

That's the only edit. Conservative window covers the back-step smoke-break window per prose ("Thursday at eight" + "the time the digital over the microwave had been showing").

### Week-gate analysis (why we don't need one)

`diner_regulars_named` is set during diner shifts after Maya has worked a few. Realistically lands W2 or W3 (game starts late June/early July; first diner shift Wed W1 per `first_diner_shift_t0`; "regulars named" naturally takes a few shifts). Even if `diner_regulars_named` fires a week early or late, Cookie's monologue still works on any Thursday in that window — the scene's content is "Cookie hands Maya the regulars list," not "this is specifically Thursday W3." No week-gate needed.

### Why this works
- Cookie's whole monologue (Dale, Roy, Pete-Tuesdays, church couple Saturdays) is the scene; the day-of-week is the scene's premise. Locking to Thursday is the right gate.
- The 8pm anchor is approximate — narrow window 20:00–22:00 covers the smoke-break cadence without over-constraining.
- All flag/effect values (`cookie_peer_established`) preserved exactly — no structural changes.

### Verification (when implemented)
1. Walk Maya through enough diner shifts to set `diner_regulars_named`. Try entering loc_diner_kitchen on a Tuesday/Wednesday/Friday — confirm canvas does NOT fire. Try on a Thursday between 8pm–10pm — confirm canvas fires.
2. `package_from_toml --dry-run` — counts unchanged.

---

## Canvas #6 — jake_first_glance_noticed ("Hands Stop")

**TOML location:** `2_story_canvases.toml:1005`
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block only — no prose changes, no engine changes, no week-gate

### Diagnosis
Jake's first noticed-Maya beat at the kitchen pitcher. Trigger gates on `first_jake_rebuff is_true` AND `beauty >= 45`. Prose anchors to "five-fifteen on a Thursday" — the pitcher-arrival beat is time-precise (Jake comes in for cold water at the same kitchen-prep slot every Thursday because "Thursday in this house was fried-okra night"). Beauty 45 acts as a natural week-gate proxy (slow-growing trait → naturally takes weeks). The prose is correct; engine needs to match.

### Chosen solution
Add a single `[[canvases.trigger.schedules]]` block. No prose edits.

#### Edit 1 — insert after line 1018 (the existing trigger.conditions block)

**INSERT block:**
```toml

[[canvases.trigger.schedules]]
weekdays = [3]              # Thursday
start_time = "17:00"
end_time = "17:30"
```

Aggressive narrow window because the pitcher beat at 5:15pm is precise — Jake walks in from the hallway during Diana's prep window, takes the cold-water pitcher, drinks, leaves. The narrow 30-minute slot reflects the prose's structural precision.

### Week-gate analysis (why we don't need one)

Beauty ≥ 45 is the gate. Beauty grows via specific activities (mirror_look, sketch, etc.) — slow trait by design. Realistically lands W4 or later. Even if a player optimally grinds beauty earlier, the Thursday schedule means it fires on the next available Thursday after both gates are met, which is the right behavior. No separate week-gate needed.

### Why this works
- Thursday-fried-okra-night IS the household rhythm (links forward to Cookie's Thursday and Frank's Thursday-bookkeeping rhythm).
- The 5:15pm pitcher beat is structurally tied to Diana's dinner prep window; aggressive narrow schedule preserves the precision the prose requires.
- All flag/trait/effect values preserved (`jake_first_glance_noticed`, `jake_noticed_open`, `npc_jake.love +2`, `time 20`).

### Verification (when implemented)
1. Build beauty to 45 + trigger `first_jake_rebuff`. Try entering loc_kitchen on non-Thursdays or outside 5:00–5:30pm window — confirm canvas does NOT fire. Try Thursday 5:15pm — confirm canvas fires.
2. `package_from_toml --dry-run` — counts unchanged.

---

## Canvas #7 — marge_thursday_key ("The Thursday Key")

**TOML location:** `2_story_canvases.toml:1080`
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block + 2 small prose softens — no engine changes, no week-gate

### Diagnosis
CH2 close milestone. Marge hands Maya the Thursday-night-closing key at end of Thursday close. Trigger gates only on `cookie_peer_established is_true`. The prose is mostly correct — Marge's dialog *"Thursdays are slow. Key's under the till."* IS the scene, and "the diner at nine-fifty-nine on a Thursday" is the closing-time register. Two minor month-claims ("Thursday in September," "since the hire in August," "August count, even in September") need softening to avoid calendar-drift if the canvas fires earlier or later than W5.

### Chosen solution
Schedule block + 2 surgical prose edits. Marge's dialog and the key-handoff body sequence stay verbatim.

#### Edit 1 — insert after line 1090 (the existing trigger.conditions line)

**INSERT block:**
```toml

[[canvases.trigger.schedules]]
weekdays = [3]              # Thursday
start_time = "21:30"
end_time = "22:30"
```

Narrow window because the prose anchors precisely to the closing-time count ("nine-fifty-one... nine-fifty-nine") — the key-handoff happens at end-of-Thursday-close. 21:30–22:30 covers the close-down cadence.

#### Edit 2 — line 1106 (drop calendar-month claim)

**ORIGINAL:**
> *"The diner at nine-fifty-nine on a Thursday in September was the room it had been every Thursday since the hire in August..."*

**REWRITE:**
> *"The diner at nine-fifty-nine on a Thursday was the room it had been every Thursday since the hire..."*

Drops "in September" + "in August." Preserves the closing-time precision and the rhythm-since-hire register.

#### Edit 3 — line 1121 (drop month references in walk-home prose)

**ORIGINAL:**
> *"The cicadas on the last weeks of a long August count, even in September, even with the calendar turned."*

**REWRITE:**
> *"The cicadas on the last weeks of a long summer count, even with the season turning."*

Drops "August" + "September." Preserves the cicada-end-of-summer register.

### Week-gate analysis (why we don't need one)

`cookie_peer_established` is the trigger flag. Per Canvas #5's analysis, that lands W2-3 vicinity. By the time a player has worked enough Thursdays for Marge to see her as "steady," she's naturally at W4-W5 or later. The Thursday schedule means the canvas fires on the next Thursday after Marge has accumulated trust, which is the right shape. No separate week-gate needed.

### Why this works
- Thursday-night-close is structural design (CH2 close milestone IS the Thursday-key-ceremony).
- Marge's dialog (*"You're steady."* / *"Thursdays are slow. Key's under the till."* / *"Lock the back when you leave. You good?"*) preserved exactly.
- Cookie's cameo (apron-tie loose, *"I'm out. Fryer's down to one again, so Friday's gonna be a time."*) preserved exactly.
- The walk-home key-in-pocket beat preserved exactly.
- Two minor month-strips guard against calendar-drift if the canvas fires earlier than W5 (Aug) or later than W6 (Sep).

### Verification (when implemented)
1. Trigger `cookie_peer_established` → work multiple Thursdays at the diner. Try entering loc_diner_office on non-Thursdays or before 9:30pm — confirm canvas does NOT fire. Try Thursday 9:30–10:30pm — confirm canvas fires.
2. `package_from_toml --dry-run` — counts unchanged.
3. Read post-edit — Marge's two key sentences and Cookie's cameo intact; no "August" or "September" claims remain.

---

## Canvas #8 — arrival_at_franks ("Arrival")

**TOML location:** `2_story_canvases.toml:463` (3 sub-nodes)
**Decided:** 2026-04-27
**Status:** `skipped`
**Fix type:** None — game-start binding makes this self-correcting

### Diagnosis
Phase 1 opening canvas, 1300 words across 3 sub-nodes (driveway / porch / hallway). Trigger gates only on `accepted_diana_offer is_true`. Prose anchors to "five-in-the-afternoon count," "Saturday smell," "in bed by eight" — all matching the game's starting day/hour configuration (Sat W1 17:00 per `0_systems_spec.toml` time_settings + Game_Redesign.md locked constraints).

### Why skipped
The game **starts** at Saturday Week 1 17:00 by engine configuration. The Prologue ends with the player choosing "Don't call. Just drive in." (or similar) which sets `accepted_diana_offer` and transitions immediately into Phase 1. The first thing the player does in Phase 1 is land on loc_front_porch — and the canvas fires. So the prose's "Saturday afternoon" / "five-in-the-afternoon" / "in bed by eight" claims are structurally guaranteed by the game-start config + the prologue flag chain.

`is_repeatable = false` ensures the canvas can never re-fire on a wrong day in a corrupt-load scenario.

### What would change this verdict
If the design ever changes the game-start day/hour, OR if the prologue is restructured so `accepted_diana_offer` can flip mid-game (e.g. lazy-set on a delayed code path), this canvas would need a schedule block (`weekdays=[5], start_time="16:30", end_time="18:00"`) for protection. Until then, no fix needed.

### Verification
None required for this fix pass. If the canvas misfires in playtest (which would only happen if game-start config changed without anyone noticing), revisit.

---

## Canvas #9 — town_walk_day_two ("Main Street")

**TOML location:** `2_story_canvases.toml:671` (3 sub-nodes)
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block only — no prose changes, no engine changes, no week-gate

### Diagnosis
Mon W1 mid-morning walk to town to find work. 3 sub-nodes (kitchen / walk / diner). Trigger gates only on `first_morning_kitchen_done is_true` — which sets on Sunday W1 morning, allowing the canvas to fire any time after that. Without a schedule, a player visiting loc_driveway on Sunday afternoon would trigger the "Monday morning" walk beat. Prose precisely anchors to Monday-9:18-kitchen / Monday-9:30-departure / Monday-10:50-diner-arrival.

### Chosen solution
Add a single `[[canvases.trigger.schedules]]` block. No prose edits.

#### Edit 1 — insert after line 680 (existing trigger.conditions line)

**INSERT block:**
```toml

[[canvases.trigger.schedules]]
weekdays = [0]              # Monday
start_time = "09:00"
end_time = "11:00"
```

Conservative window covers the kitchen-departure → walk-out → diner-arrival sequence per prose (9:18 kitchen clock → 9:30 walk start → 10:50 diner). Maya entering loc_driveway during this window means she's leaving the house — exactly the scene's premise.

### Week-gate analysis (why we don't need one)

`first_morning_kitchen_done` only sets after `arrived_at_franks` (Sat W1 17:00) → `first_morning_kitchen` (Sun W1 morning). The next Monday after that flag is Mon W1 by definition. No way for the trigger to fire on a Mon W2+ unless the player skips the entire week's worth of canvases — and even then, the Monday-locked schedule plus the existing flag-chain would land the player on a coherent Monday morning regardless. No separate week-gate needed.

### Why this works
- Monday-as-job-search-day is design intent (Diana's "Frank can drop you" + the diner being closed Sundays in a small Southern town).
- All 3 sub-node prose stays untouched — Diana's "Seven-tenths of a mile of gravel past the Hansens'" route monologue, the truck-driver acknowledgment, Marge's "Help you?" → "Come back tomorrow. Five p.m." dialog all preserved.
- Establishes the Monday→Tuesday hard chronology with Canvas #10 (marge_interview at Tue W1 17:00).

### Verification (when implemented)
1. Trigger `first_morning_kitchen_done`. Try entering loc_driveway on Sunday afternoon — confirm canvas does NOT fire. Try Monday between 9–11am — confirm canvas fires.
2. `package_from_toml --dry-run` — counts unchanged.

---

## Canvas #10 — marge_interview ("Apron")

**TOML location:** `2_story_canvases.toml:734`
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block only — no prose changes, no engine changes, no week-gate

### Diagnosis
Tue W1 5pm interview-and-hire. Trigger gates only on `interview_scheduled is_true` — set by Canvas #9 (town_walk_day_two). Without a schedule, player could enter loc_diner_front any time after the Monday walk and trigger the interview canvas. Prose anchors precisely to "She came in at four-fifty-nine by the clock on the wall" — Marge told Maya in Canvas #9 to "Come back tomorrow. Five p.m.," locking the precise moment.

### Chosen solution
Add a single `[[canvases.trigger.schedules]]` block. No prose edits.

#### Edit 1 — insert after line 744 (existing trigger.conditions line)

**INSERT block:**
```toml

[[canvases.trigger.schedules]]
weekdays = [1]              # Tuesday
start_time = "17:00"
end_time = "17:30"
```

Aggressive narrow window because Marge's "Come back tomorrow. Five p.m." in Canvas #9 (line 722) and Maya's "four-fifty-nine by the clock on the wall" arrival in this canvas's prose (line 751) are both precise hire-time anchors. The interview happens at exactly this slot or it doesn't happen.

### Week-gate analysis (why we don't need one)

`interview_scheduled` is set by Canvas #9 which is Mon W1 (per its schedule). The next Tuesday after that is Tue W1. The canvas can't fire earlier (Tuesday W1 hasn't happened) and locking the schedule prevents firing on a later Tuesday. No separate week-gate needed.

### Why this works
- Tuesday-5pm-precise is design canon — Marge's "Come back tomorrow. Five p.m." is the canvas's narrative premise.
- All prose stays untouched — Marge's "Tie it. Learn as you go." / "Cookie's back here. Do what she says." / the full hire-terms speech ("Tomorrow. Five to ten. Nine an hour. Tips are yours...") + Cookie's first appearance and her "You're okay, kid" + Marge's forward-shadowing "Thursdays are different. We'll see about those." (which forward-references Canvas #7's Thursday-key handoff) all preserved exactly.
- Hire-terms line *"Tomorrow. Five to ten."* sets up Canvas #11 (`first_diner_shift_t0`) at Wed W1 17:00–22:00.

### Verification (when implemented)
1. Trigger `interview_scheduled`. Try entering loc_diner_front on Mon evening or Wed morning — confirm canvas does NOT fire. Try Tuesday 5:00pm sharp — confirm canvas fires.
2. `package_from_toml --dry-run` — counts unchanged.

---

## Canvas #11 — first_morning_kitchen ("First Morning")

**TOML location:** `2_story_canvases.toml:542`
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block only — no prose changes, no engine changes, no week-gate

### Diagnosis
Sun W1 07:00 morning — Frank names the rent terms ($60/week Sundays, Maya cooks + Frank/Diana buy groceries) and asks the church-or-stay choice. Trigger gates only on `arrived_at_franks is_true`. Prose anchors precisely to "southern Sunday in July at seven in the morning" + "The clock over the stove said seven-twelve." The arrival canvas's exit advances time 295 min from 17:00 (puts Maya into next morning), so player typically enters kitchen Sun W1 ~8am — but a schedule block protects against the player wandering into the kitchen Saturday evening pre-bed and triggering the morning rent ceremony.

### Chosen solution
Add a single `[[canvases.trigger.schedules]]` block. No prose edits.

#### Edit 1 — insert after line 551 (existing trigger.conditions line)

**INSERT block:**
```toml

[[canvases.trigger.schedules]]
weekdays = [6]              # Sunday
start_time = "06:30"
end_time = "08:30"
```

Conservative window covers the 7:00 / 7:12 prose anchors with a 90-min buffer either side — ensures the canvas fires whenever Maya wakes up and visits the kitchen on Sunday morning.

### Week-gate analysis (why we don't need one)

`arrived_at_franks` only sets via `arrival_at_franks` canvas, which fires once on Sat W1 17:00 by game-start. The next Sunday after that flag is Sun W1 by definition. Even if a player loads a save on Sat W1 evening and the canvas hasn't fired yet, the Sunday schedule means it fires on the next Sunday morning — Sun W1 — which is the right scene.

### Why this works
- The whole rent-terms ceremony (Frank's "Maya. Rent's sixty a week, due Sundays." + "You cook. Diana and I buy the groceries." + the church-or-stay choice) and Diana's "Sit." stays exactly as-written.
- All flag/trait effects preserved (`first_morning_kitchen_done`, `rent_terms_set`, `attended_church_week_1`, energy +10, optional rep_church +2 on church choice).
- Establishes the Sunday-rent rhythm that Canvas #12 (first_sunday) and Canvas #13 (the_math) both build on.

### Verification (when implemented)
1. Trigger `arrived_at_franks`. Try entering loc_kitchen Sat W1 evening — confirm canvas does NOT fire. Try Sun W1 between 6:30–8:30am — confirm canvas fires.
2. `package_from_toml --dry-run` — counts unchanged.

---

## Canvas #12 — first_sunday ("First Sunday")

**TOML location:** `2_story_canvases.toml:821`
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block only — no prose changes, no engine changes, no week-gate

### Diagnosis
Sun W2 morning — first rent envelope on the kitchen table; Frank's "you can walk with her, you can stay" through the screen. Trigger gates only on `first_t0_shift_done is_true` (set by Canvas #11's downstream first diner shift). Prose anchors to Sunday morning + Diana's note + bacon at 7:20am. The "eight days ago" callback (line 840) precisely calendar-locks this to Sun W2 (Maya said *okay* on Sun W1 morning, +8 days = Mon W2 — actually slightly off, +7 would be Sun W2; the callback is approximate but reads as "about a week ago").

### Chosen solution
Add a single `[[canvases.trigger.schedules]]` block. No prose edits.

#### Edit 1 — insert after line 830 (existing trigger.conditions line)

**INSERT block:**
```toml

[[canvases.trigger.schedules]]
weekdays = [6]              # Sunday
start_time = "06:00"
end_time = "10:00"
```

Conservative wide window covers the 7:20-bacon anchor + the pre-church (10am church time per Frank's earlier "Church is at ten") timing. Ensures fire whenever Maya enters the kitchen Sunday morning.

### Week-gate analysis (why we don't need one)

`first_t0_shift_done` is set by `first_diner_shift_t0` (Wed W1 17:00–22:00 per upcoming canvas). The next Sunday after that flag is Sun W2 by definition. If the player delays the Wed shift to Wed W2, this fires Sun W3 instead — still narratively coherent ("first Sunday after first T0 shift"), the "eight days ago" callback math drifts but stays approximately legible. Acceptable case-by-case tradeoff.

### Why this works
- All cross-canvas callbacks preserved: the "okay-she-said-at-this-table-eight-days-ago" (Canvas #11), Frank's notepad-by-the-phone "*Maya — Wk 1*" (Canvas #13's setup), the apron-folded-the-way-Cookie-folded-hers (Canvas #5/#10 callback), basil-from-the-side-garden-through-the-cracked-window (arrival_at_franks callback).
- Diana's handwritten note (`<blockquote>Leave sixty for Frank before church. — D.</blockquote>`) preserved exactly.
- Frank's "Maya. / Diana is going to walk to the service. You can walk with her. You can stay." three-sentence specimen preserved exactly.
- All flag/trait effects preserved (money -60, optional rep_church +3, `first_sunday_passed`, `attended_church_week_1` on attend choice).

### Verification (when implemented)
1. Trigger `first_t0_shift_done`. Try entering loc_kitchen Sat or Mon morning — confirm canvas does NOT fire. Try Sun W2 between 6–10am — confirm canvas fires.
2. `package_from_toml --dry-run` — counts unchanged.

---

## Canvas #13 — the_math ("The Math")

**TOML location:** `2_story_canvases.toml:860`
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block only — no prose changes, no engine changes, no week-gate

### Diagnosis
CHAPTER 1 CLOSE milestone. Sun W2 late (~21:30) — Maya at her desk doing the rent + tuition math, naming the corruption-economic pressure for the first time. Trigger gates only on `first_sunday_passed is_true` (set by Canvas #12). Prose anchors precisely to "nine-twenty-eight by the alarm clock" + "The house at nine-forty-one on a second Sunday in July." The math ("twelve Sundays left counting this one as paid") assumes the canvas fires Sun W2 — drifts if it fires later.

### Chosen solution
Add a single `[[canvases.trigger.schedules]]` block. No prose edits.

#### Edit 1 — insert after line 869 (existing trigger.conditions line)

**INSERT block:**
```toml

[[canvases.trigger.schedules]]
weekdays = [6]              # Sunday
start_time = "21:00"
end_time = "23:00"
```

Aggressive narrow late-night window — the late-night-isolation IS the register. Maya sits down AFTER the house cycle (Frank up the stairs for the crossword, Diana at the sink) and BEFORE sleep. 21:00–23:00 covers the 9:28 / 9:41 prose anchors precisely.

### Week-gate analysis (why we don't need one — and the small accepted tradeoff)

`first_sunday_passed` sets via Canvas #12 at Sun W2 ~10am-1pm. The Sunday schedule means this canvas fires Sun W2 evening — same day. Clean cascade.

**Accepted tradeoff:** if the player skips entering loc_mayas_bedroom Sun W2 evening, the canvas waits to Sun W3 evening. Maya's "twelve Sundays left counting this one as paid" math then reads as eleven Sundays in actuality — slight internal-math drift. Acceptable for a CH1-close milestone; a player delaying their bedroom visit by a week sees the math computation off by one week. Per case-by-case methodology, not worth the engine work to enforce.

### Why this works
- The CH1-close italic FID-thought beat (*"There's more tier available if I want it. I can see where it goes from here."* at line 887) preserved exactly.
- The recall of "Marge's Tuesday comment — *Thursdays are different. We'll see about those.*" (Canvas #10 forward-shadow) preserved as a factual recall, not a retcon.
- Cookie's "*if you can hold an eye*" callback (from `first_diner_shift_t0`) preserved.
- All flag/trait effects preserved (`first_rent_paid` milestone + `group_settled_in` + calculation +2).
- The Rule 22 sketchbook-stays-closed inversion ("the closing-of-the-math is not the register the clean sketchbook belongs to") preserved.

### Verification (when implemented)
1. Trigger `first_sunday_passed` (i.e. complete Canvas #12). Try entering loc_mayas_bedroom Sun W2 afternoon or Mon W3 evening — confirm canvas does NOT fire. Try Sun W2 between 9–11pm — confirm canvas fires.
2. `package_from_toml --dry-run` — counts unchanged.

---

## Canvas #14 — first_jake_cold_shoulder ("I'm Working")

**TOML location:** `2_story_canvases.toml:635`
**Decided:** 2026-04-27
**Status:** `skipped`
**Fix type:** None — body prose has no hardcoded time anchors

### Diagnosis
Sun W1 evening per description, but body prose uses only "Upstairs after dinner" and "tonight" — no weekday names, no clock anchors, no retconned actions. Scene craft (Jake's headphones, the raised hand, "I'm working" rebuff) doesn't depend on temporal specificity.

### Why skipped
Trigger gates on `first_morning_kitchen_done is_true`. By natural flag-chain, this fires Sun W1 evening when Maya goes upstairs. Body prose claims nothing the trigger doesn't enforce. No fix needed.

### What would change this verdict
If a future audit reveals body prose I missed that anchors a specific moment.

---

## Canvas #15 — first_diner_shift_t0 ("First Shift")

**TOML location:** `2_story_canvases.toml:780`
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block only — no prose changes

### Diagnosis
Wed W1 5pm-10pm first T0 shift. Trigger gates only on `hired_at_diner is_true`. Prose anchors precisely to "The Coca-Cola clock above the pass said nine-twelve" + "shift was five-to-ten" + Cookie's *"If you can hold an eye, that's the Thursday shift"* — Cookie's forward-reference confirms THIS is NOT Thursday.

### Chosen solution
**INSERT after line 790:**
```toml

[[canvases.trigger.schedules]]
weekdays = [2]              # Wednesday
start_time = "17:00"
end_time = "22:00"
```

### Week-gate analysis
Not needed. `hired_at_diner` set Tue W1 5pm by Canvas #10. Next Wednesday is Wed W1.

### Why this works
- Conservative full-shift window covers the 5-to-10 working hours per prose.
- Cookie's "*that's the Thursday shift*" forward-shadow to Canvas #5/#11 (Thursday-night truckers) preserved in context.
- All flag/effect values preserved (`first_t0_shift_done`, energy/hygiene effects, money +43/45/50 per choice).

---

## Canvas #16 — diner_rhythm_deepens ("Regulars")

**TOML location:** `2_story_canvases.toml:896`
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block only — no prose changes

### Diagnosis
Tue W3 17:00–22:00 — Maya's seventh T0 shift; Pete-the-mechanic shows up at 5:18; first regulars-named beat. Trigger gates only on `first_rent_paid is_true`. Prose anchors "Tuesday was her seventh T0" + "Pete walked in at 5:18. Tuesday was Pete's day" — Pete-Tuesday thread (also load-bearing in Canvas #5, #18).

### Chosen solution
**INSERT after line 906:**
```toml

[[canvases.trigger.schedules]]
weekdays = [1]              # Tuesday
start_time = "17:00"
end_time = "22:00"
```

### Week-gate analysis
Not needed. `first_rent_paid` set Sun W2 by Canvas #13. Next Tuesday is Tue W3.

### Why this works
- Pete-Tuesday thread locked in this canvas matches the same thread in Canvas #5 (Cookie's intel) and Canvas #18 (Ryan's partner-close).
- Cookie's "*You're good*" peer-shift signal preserved.
- All flag/effect values preserved (money +52, hygiene -15, rep_road +1, `diner_regulars_named`).

---

## Canvas #17 — ryan_shop_first_visit ("The Ledger")

**TOML location:** `2_story_canvases.toml:966`
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block only — no prose changes

### Diagnosis
Sat W3 afternoon — Maya crosses the gravel to Ryan's shop for the first time; the farmer demonstrates the ten-percent dance; Ryan offers her the ledger work. Trigger gates only on `first_ryan_observation is_true`. Prose anchors "The Saturday sun at three in the afternoon was the hottest thing about the day."

### Chosen solution
**INSERT after line 976:**
```toml

[[canvases.trigger.schedules]]
weekdays = [5]              # Saturday
start_time = "14:00"
end_time = "16:00"
```

### Week-gate analysis
Not needed. `first_ryan_observation` set Sun W1 by Canvas #2. Next Saturday afternoons are W2 onward. Slight drift acceptable (canvas works on any Sat afternoon).

### Why this works
- Ryan's "*You lost?* / *You any good with numbers?* / *Help me with the ledger tomorrow. I'll feed you.*" Help-tier fragments preserved.
- Saturday + 3pm anchor in prose now enforced by engine.
- All flag/effect values preserved (`ryan_shop_first_visit`, `ryan_help_tier_open`).

---

## Canvas #18 — ryan_partner_first_close ("Twenty Above Asking")

**TOML location:** `2_story_canvases.toml:1132`
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block only — no prose changes

### Diagnosis
Tue W6 afternoon — Pete shows up for the green John Deere; Ryan steps out, Maya closes; her cut is $35. Trigger gates on `ryan_help_tier_open is_true` AND `corruption >= 25`. Prose anchors "The Tuesday after the Tuesday Pete had bought the crankshaft" + "Pete came in at four-fifteen" + "Big one's coming Saturday" forward-shadow.

### Chosen solution
**INSERT after line 1145:**
```toml

[[canvases.trigger.schedules]]
weekdays = [1]              # Tuesday
start_time = "14:00"
end_time = "17:00"
```

### Week-gate analysis
Not needed. `corruption >= 25` is a slow trait gate that naturally lands at W4+. Pete-Tuesday thread + corruption gate together gate the canvas to the right window.

### Why this works
- Pete-Tuesday-mechanic thread locked across 3 canvases (#5, #16, #18) — Maya consistently encounters Pete on Tuesdays.
- Ryan's *"Yeah. You got it."* and *"Big one's coming Saturday."* (forward-shadow to Canvas #20's Saturday close) preserved.
- All flag/effect values preserved (money +35, rep_road +3, `ryan_partner_open`, ryan.love +3).

---

## Canvas #19 — jake_peek_discovery ("The Drawing")

**TOML location:** `2_story_canvases.toml:1174` (3 sub-nodes: the_doorway / the_drawing_revealed / the_decision)
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block only — no prose changes

### Diagnosis
W6 late, 1am hallway — Maya sees Jake's drawing of herself through the cracked door; two-route fork (carry-the-knowledge OR push-his-door-wide-back). Trigger gates on `jake_noticed_open is_true` AND `corruption >= 35`. Prose anchors "She had been awake when the house cycled into its one-a.m. quiet." NO day-of-week lock in prose — the 1am-hallway register is what's load-bearing.

### Chosen solution
**INSERT after line 1187 (after existing trigger.conditions block):**
```toml

[[canvases.trigger.schedules]]
weekdays = [0, 1, 2, 3, 4, 5, 6]   # Any day
start_time = "00:00"
end_time = "02:00"
```

Schedule lives on parent canvas trigger only; sub-nodes inherit by chaining.

### Week-gate analysis
Not needed. `corruption >= 35` slow-trait gate naturally lands at W5-6. The 1am window + corruption combo correctly constrains.

### Why this works
- Tier-A multi-node Crack scene with 3 sub-nodes — the doorway / the drawing / the decision-fork. All sub-node prose preserved.
- The "August run even with September turned over" cicada line — Maya's perception, not load-bearing — left alone.
- All flag/trait effects preserved across both fork choices (calculation +1, jake_peek_draw_open/revealed/jake_caught flags).

---

## Canvas #20 — ryan_big_ticket_deal ("The Back Office")

**TOML location:** `2_story_canvases.toml:1256` (4 sub-nodes: the_briefing / the_approach / the_back_office / the_aftermath)
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block only — no prose changes

### Diagnosis
Sat W7 afternoon — the farmer-close that the briefing on Thursday set up. Trigger gates on `ryan_partner_open is_true` AND `corruption >= 75`. Prose has TWO different time anchors: N0 (the_briefing) is "Thursday afternoon W7," then narrative time-skip via choice exit ("Saturday is two days away") to N1 (the_approach) "Saturday. Two-twenty by the shop clock." Schedule must lock the canvas's TRIGGER day, which is Thursday (the briefing). The Saturday content in N1+ is narrative time-skip compression — a craft choice, not a trigger problem.

### Chosen solution
**INSERT after line 1269 (after existing trigger.conditions block):**
```toml

[[canvases.trigger.schedules]]
weekdays = [3]              # Thursday
start_time = "14:00"
end_time = "17:00"
```

### Week-gate analysis
Not needed. `corruption >= 75` is the highest corruption gate in Phase 1 — only reachable by W6+ realistically. With `ryan_partner_open` chain (set W6 by Canvas #18), naturally lands W7+.

### Why this works
- Locks the canvas-trigger day to Thursday (briefing day) per N0.
- Narrative time-skip in N1+ from Thursday → Saturday is a craft compression that the engine respects via the choice-exit's `time_progression_minutes`. This isn't a trigger-prose binding bug — it's a deliberate single-canvas-spans-two-narrative-days structure.
- All flag/trait/money effects preserved (money +250, corruption +8, rep_road -2, `ryan_big_deal_closed`, `customer_farmer_flag`, `one_crack_this_chapter`).

---

## Canvas #21 — maya_midpoint_crack ("Midpoint Crack")

**TOML location:** `2_story_canvases.toml:1360`
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block only — no prose changes

### Diagnosis
Thu W8 7:30pm T2 floor — Maya tilts at the hip on purpose; feels nothing; midpoint hinge into Saturated-band. Trigger gates only on `ryan_beach_proposal is_true`. Prose anchors "Thursday. Seven-thirty-one by the Coca-Cola clock above the pass."

### Chosen solution
**INSERT after line 1369:**
```toml

[[canvases.trigger.schedules]]
weekdays = [3]              # Thursday
start_time = "19:00"
end_time = "22:00"
```

### Week-gate analysis
Not needed. `ryan_beach_proposal` set Sun W7 by Canvas #4 (ryan_beach). Next Thursday is W8 Thu naturally.

### Why this works
- T2-floor Thursday rhythm matches the Thursday-trucker-night design (links to Canvas #5 Cookie's "Thursday's trucker night").
- The hinge italic *"She did it on purpose. She felt nothing doing it."* preserved.
- "Diner on a good Thursday in October" + "August count even in October" prose left alone — Maya's seasonal observation, not load-bearing.
- All flag/trait effects preserved (calculation +3, money +95, corruption +2, `midpoint_crack`).

---

## Canvas #22 — ryan_invite_porch ("The Invite")

**TOML location:** `2_story_canvases.toml:1409`
**Decided:** 2026-04-27
**Status:** `skipped`
**Fix type:** None — already ships with correct schedule block

### Diagnosis
Sat W7 evening — Ryan walks up the gravel and onto the porch step in front of Frank, says "Sunday — I'll come get you." Already ships with `[[canvases.trigger.schedules]]` at lines 1420–1423: weekdays=[5], start_time="20:00", end_time="21:30". Existing flag conditions (`ryan_big_deal_closed` AND not `ryan_beach_invite_done`) gate forward-progression.

### Why skipped
Author of this canvas (Session 22) correctly added the schedule block at authoring time. No fix needed today. Upstream gating via `ryan_big_deal_closed` chains through Canvas #20 which (after S.20 lands) will have the Thursday W7 trigger schedule, transitively constraining this canvas to the Saturday after the Thursday briefing → Saturday close. Clean cascade.

### What would change this verdict
If Canvas #20's trigger window changes substantially or `ryan_big_deal_closed` becomes settable from a non-W7 path, revisit.

---

## Canvas #23 — frank_catch_living_room ("The Catch")

**TOML location:** `2_story_canvases.toml:1557` (4 sub-nodes: picking_the_room / the_doorway / the_walk_through / alone_after)
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block only — no prose changes

### Diagnosis
Wed W8-9 23:30 — Maya picks the living room couch deliberately; Frank comes home from Bill's at 11:22; the catch beat. Trigger gates on `arrived_at_franks is_true` AND `corruption >= 50`. Prose anchors precisely: "Tonight was Wednesday. Wednesday was the night Frank walked across the pasture to Bill Hargrove's porch... Frank walked back between eleven and eleven-thirty" + "headlights of Frank's truck came up the gravel at eleven twenty-two." Wednesday-Bill's-night is structural design intent.

### Chosen solution
**INSERT after line 1570:**
```toml

[[canvases.trigger.schedules]]
weekdays = [2]              # Wednesday
start_time = "23:00"
end_time = "23:59"
```

Aggressive narrow late-night window — Frank-walks-back-between-11-and-11:30 is precise; player needs to be on couch in the right window.

### Week-gate analysis
Not needed. `corruption >= 50` slow-trait gate naturally lands W7+. With `arrived_at_franks` (W1) + corruption (W7+), canvas naturally lands the right Wednesday window.

### Why this works
- Wednesday-Bill's-night premise structurally requires Wednesday — this is the only canvas in the file where the trigger weekday is built into the SCENE'S FACT (not just the SCENE'S TIMING).
- All four sub-node sequences (picking the room → the doorway count → kitchen sounds + 14 stairs → couch alone) preserved exactly.
- All flag effects preserved (`frank_caught` on N4 exit; no stat effects per book canon — latent weight).

---

## Canvas #24 — frank_crack ("The Office")

**TOML location:** `2_story_canvases.toml:1691` (4 sub-nodes: the_office / the_ledger / the_pressing_hands / the_break)
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block + 1 small prose touch — Group H (hybrid)

### Diagnosis
W10 Thu 22:45 — bookkeeping ritual; Frank's Phase-B Crack lands on one incomplete sentence (*"I cannot —"*) followed by silence. Trigger gates on `frank_tease_under_compliance_open is_true` AND `midpoint_crack is_true`. Prose anchors "She came down the hallway at twenty past ten" + "the strip... the thing she had been walking toward for **six Thursday nights running**" — that count is engine-untracked.

### Chosen solution

**INSERT after line 1704 (after existing trigger.conditions block):**
```toml

[[canvases.trigger.schedules]]
weekdays = [3]              # Thursday
start_time = "22:00"
end_time = "23:00"
```

**Edit 1 — line 1712 (soften the un-tracked count):**

ORIGINAL:
> *"the thing she had been walking toward for six Thursday nights running now"*

REWRITE:
> *"the thing she had been walking toward for the Thursday-nights-running rhythm she had learned to read"*

Drops the specific "six" count (which the engine doesn't track) but preserves the discipline-flavor of the rhythm.

### Week-gate analysis
Not needed. `midpoint_crack` set by Canvas #21 (Thu W8). Next eligible Thursday after the chain is W10 naturally.

### Why this works
- Frank-Thursday-bookkeeping-ritual is structural to Frank's whole Phase-B character voice.
- The Crack moment (*"I cannot —"* + silence + handwriting-holds-then-doesn't) preserved exactly.
- The "six Thursday nights" count was the only engine-untrackable claim; softening to "rhythm" preserves character without claiming a counter.
- All flag/trait effects preserved (npc_frank.love +10, `frank_cracked`, `one_crack_this_chapter`).

---

## Canvas #25 — frank_call_out ("Call Out")

**TOML location:** `2_story_canvases.toml:1799` (3 sub-nodes: the_office / naming_it / his_response)
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block only — no prose changes

### Diagnosis
W11 Thu 22:20 — bookkeeping callback; Maya delivers the Call-out line *"This is normal. Everyone has needs. Even you."*; 4-route Keep fork at exit. Trigger gates only on `frank_cracked is_true`. Prose anchors "Thursday at twenty past ten" + "the seven was a thing she had been aware of when she set out from her room" (referencing the seventh Thursday after frank_crack).

### Chosen solution
**INSERT after line 1809:**
```toml

[[canvases.trigger.schedules]]
weekdays = [3]              # Thursday
start_time = "22:00"
end_time = "23:00"
```

### Week-gate analysis
Not needed. `frank_cracked` set by Canvas #24 (W10 Thu). Next Thursday is W11 naturally.

### Why this works
- Frank-Thursday-office-ritual continues from Canvas #24.
- The 7-Thursdays count Maya tracks ("the seventh Thursday") is HER perception in Saturated-band narrator voice — Maya can count Thursdays even if the engine doesn't. This is a different shape than Canvas #24's "six Thursday nights running" because here Maya is explicitly counting from inside the scene; in #24 it was atmospheric metadata.
- All four Keep-fork choices preserved (frank_keep_romantic / arrangement / rupture / power_inverted).
- All flag effects preserved including `frank_called_out`, `frank_q3_done`, `frank_arc_complete`, `frank_keep_route` + the route-specific flag.

---

## Canvas #26 — jake_caught_and_hand ("His Room Her Terms")

**TOML location:** `2_story_canvases.toml:1893` (5 sub-nodes: walking_in / the_drawings / the_hand_offer / the_act / after_routes)
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block only — no prose changes

### Diagnosis
Fri W11 23:31 — Maya walks into Jake's room; he freezes; she leads the hand; 4-route Keep fork. Trigger gates only on `jake_tease_open is_true`. Prose anchors *"She waited for the Friday"* + "Diana went up at nine-thirty" + "Friday at eleven thirty-one" — Maya literally plans for Friday specifically.

### Chosen solution
**INSERT after line 1903:**
```toml

[[canvases.trigger.schedules]]
weekdays = [4]              # Friday
start_time = "23:00"
end_time = "23:59"
```

Aggressive narrow late-night window — Maya picks Friday specifically because Diana goes up early on Fridays (early library start). 11:30pm matches the prose precisely.

### Week-gate analysis
Not needed. `jake_tease_open` set by Canvas #19 (W6+) → many Fridays available. Maya's "she waited for the Friday" reads as her deliberately picking a Friday after the chain opened. Acceptable drift if it lands W11 vs W12 vs W13.

### Why this works
- Maya's Friday-planning is design intent — she chose this night because Diana's library schedule makes it the safest.
- All five sub-node sequences preserved (door opens → drawings on desk → "Show me your hand" → the hand → 4-route fork).
- Jake's single monosyllable *"...okay."* preserved exactly per style sheet.
- All flag/trait effects preserved across all 4 fork choices (jake_keep_owned/lovers/withdrawn/she_uses_him).

---

## Canvas #27 — rent_shortfall_first ("Short This Week")

**TOML location:** `2_story_canvases.toml:2016`
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block only — no prose changes

### Diagnosis
Sun W9-11 7am — Maya is short twenty for rent; Frank lets the silence sit; 4-choice fork (defer / chore-barter / T3-Thursday / can't-yet). Trigger gates on `money < 60` AND `first_rent_paid is_true` AND `rent_shortfall_1 is_false`. Prose anchors "Sunday at seven was the hour Frank did the household books."

### Chosen solution
**INSERT after line 2030:**
```toml

[[canvases.trigger.schedules]]
weekdays = [6]              # Sunday
start_time = "06:00"
end_time = "10:00"
```

### Week-gate analysis
Not needed. The `money < 60` mechanical gate is what triggers this — when Maya's cash drops below $60, the canvas becomes eligible. The Sunday lock means it fires on the next Sunday morning when she also enters loc_franks_office. Could be W3, W7, W9, W11 — all narratively coherent ("Maya is short this week"). The "Sunday Week 9-11" range in the description is a design estimate, not a hard requirement.

### Why this works
- Sunday morning is the diegetic rent-collection day (Frank does books Sunday morning per Canvas #11/#12 rent ceremony).
- Maya's *"Short twenty this week."* one-line confession + Frank's silence-discipline preserved.
- All four exit-fork conditional choices (with their gate flags `frank_tease_under_compliance_open` and `first_ambient_tilt`) preserved exactly.
- All flag effects preserved (`rent_shortfall_1`, `rent_resolution` or `rent_evicted` per choice).

---

## Canvas #28 — brothers_discover ("Pass the Salt")

**TOML location:** `2_story_canvases.toml:2058` (3 sub-nodes: the_outdoor_dinner / the_realization / the_drift_apart)
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block + 1 small prose softening

### Diagnosis
W12 Saturday outdoor dinner — the three men register each other across the table; Maya is what they are registering. Trigger gates on OR of `frank_cracked` / `ryan_beach_proposal` / `jake_hand` (any Crack flag triggers). Prose anchors "The second Saturday in September. Diana had the string lights on before the sun had finished — she had been turning them on by five-forty."

### Chosen solution

**INSERT after line 2071:**
```toml

[[canvases.trigger.schedules]]
weekdays = [5]              # Saturday
start_time = "17:30"
end_time = "19:30"
```

**Edit 1 — line 2079 (small month softening to handle drift):**

ORIGINAL:
> *"The second Saturday in September. Diana had the string lights on before the sun had finished — she had been turning them on by five-forty because the blue stretched into an hour she did not trust the dusk for anymore."*

REWRITE:
> *"A Saturday late in the long summer. Diana had the string lights on before the sun had finished — she had been turning them on by five-forty because the blue stretched into an hour she did not trust the dusk for anymore."*

Drops "second Saturday in September." The OR-of-three-Crack-flags trigger means this canvas could fire as early as W7 (after ryan_beach_proposal) or as late as W12 — softening protects against month-drift.

### Week-gate analysis
Not adding one because the OR-trigger logic + Saturday lock means the canvas fires the first Saturday after ANY Crack flag. This is design intent — the "brothers discover" beat is chronologically tied to the Crack arcs, not the calendar week. Drift acceptable; the small prose softening handles the calendar-month claim.

### Why this works
- Saturday-outdoor-dinner geometry is structurally required (all five at the table, Frank-built table, brothers' visual recognition).
- The "Pass the salt" no-words realization beat preserved exactly.
- All five-NPC body-tells preserved (Frank reduced fragments, Ryan hand-tells, Jake glasses-pause, Diana serves-Maya-first, Maya catalogs).
- All flag effects preserved (`brothers_discover` + diana_awareness +10).

---

## Canvas #29 — keep_tier_fork ("The Fork")

**TOML location:** `2_story_canvases.toml:2140` (4 sub-nodes: the_dinner / diana_in_the_kitchen / the_choice / the_route_locked) — PHASE 1 CLOSE milestone
**Decided:** 2026-04-27
**Status:** `implemented` (2026-04-27 — schedule-block + prose edits applied; package_from_toml --dry-run passed; 73 canvases / 125 nodes / 38 locations / 12 NPCs; zero warnings)
**Fix type:** Schedule block only — no prose changes

### Diagnosis
Sun W14 Sunday dinner — Diana sets Maya's place next to hers; the flat-dumpling chicken (memory of Maya's biological father); Diana's ONE Phase-1 full sentence; 5-route fork (Independence / Frank Keep / Ryan Keep / Jake Keep / Deferred). Trigger gates only on `brothers_discover is_true`. Prose anchors "The second Sunday in October was the Sunday Diana made the flat-dumpling chicken."

### Chosen solution
**INSERT after line 2149:**
```toml

[[canvases.trigger.schedules]]
weekdays = [6]              # Sunday
start_time = "17:00"
end_time = "19:00"
```

### Week-gate analysis
Not adding one because:
- Trigger flag chain: brothers_discover (Canvas #28, fires Saturday after first Crack) → next Sunday is W12-13-14 vicinity.
- The "second Sunday in October" prose anchor is Saturated-band Maya's calendar awareness — heightened in a Phase-1-close moment. Maya naming the calendar reads as character voice, not engine claim.
- Drift potential: 1-2 weeks (W12 vs W14). For a milestone-close, the slight calendar drift in prose is acceptable narratively.

### Why this works
- Phase-1-CLOSE milestone — all Phase-2 routes branch from this canvas's 5-way exit.
- Diana's ONE Phase-1 line *"Maya, honey. Set a place for yourself next to me."* preserved exactly.
- The flat-dumpling-chicken father-memory italic intrusion (*"The flat kind, not the round."*) preserved.
- All five exit-fork flag effects preserved (`keep_tier_fork_fired`, `phase_1_final_route`, plus route-specific flag per choice).

---

*(All 29 in-scope Phase 1 canvases now documented. Prologue is out of scope per content_rewrite/PRD.md.)*
