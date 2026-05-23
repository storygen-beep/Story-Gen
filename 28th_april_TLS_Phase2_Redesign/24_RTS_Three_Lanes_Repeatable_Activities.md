# 24 — RTS Three Lanes for Repeatable NPC Content + TLS Engine Fitness + Lane 3 Design

> **Status:** Design record. Authored 2026-05-10. **Updated 2026-05-11** (§10 expanded with the full lane design framework — fictional intent, content-type vocabulary, 3×3 grid, arc-flow doctrine, narrative-shape doctrine, Frank gap analysis, edge cases).
> **Purpose:** Canonize the lane taxonomy + TLS engine fitness assessment + Lane 3 design recommendation discovered during the 2026-05-10 RTS focused live-play session and engine read. Source for any future repeatable-NPC-activity authoring or engine work in TLS.
> **Extends:** docs 21 (RTS Brother mechanism audit) + 22 (cross-NPC mechanism comparison) — those were source-extracted; this doc adds live-play classification + TLS engine fitness + the Lane 3 design recommendation.
> **Source artifacts:** `game_explorations/rts-arc-trace/synthesis_repeatable_narrative_auto_2026-05-10.md` (live-play synthesis) + `~/.claude/.../memory/rts_lane3_dispatcher_pattern.md` (compressed memory) + this doc (canonical reference).

---

## §1 The question this doc answers

When an NPC's arc progresses, how should new repeatable interactions show up in the world?

The naive answer is *menus*: as the player unlocks more, more buttons appear at NPC hub locations. The seductive but wrong answer is *verb overlay*: an unlocked verb (e.g. Tease) follows the NPC across all locations they happen to be in. Neither is what RTS does, and neither is what produces the "the world is alive with this NPC" feel that drives RTS's repeatable-content density.

This doc names the actual three lanes RTS uses, classifies every Brother surface against them, assesses what TLS already supports vs. what needs engine work, and recommends a small (~2.5 hr) engine extension to close the one gap.

---

## §2 The three lanes (RTS doctrine)

RTS uses three distinct mechanisms for repeatable NPC content. Each has a different *who picked it* axis.

| Lane | What | Who picks | Player POV |
|---|---|---|---|
| **1 — Hub button** | A button rendered at an NPC's location, gated on NPC presence × time band × MC stats. Player clicks. | **Player** | "I see Tease in the menu, I'll click it." |
| **2 — Location-entry random** | Random encounter substitutes the location's normal hub render on entry, gated on conditions + dice. | **Dice on entry** | "I walked into the bedroom and Brother was masturbating." |
| **3 — Dispatcher inside menu activity** | Player picks a non-NPC activity (Shower / Study / Wash Dishes). A transient dispatcher passage rolls dice and substitutes an NPC narrative scene if hit + conditions met. | **Dice inside an activity** | "I was just trying to take a shower and Brother walked in." |

Plain-language analogies:
- **Lane 1** = a restaurant menu. You browse and pick.
- **Lane 2** = walking into a room and your roommate is doing something. You went there; the encounter wasn't your choice.
- **Lane 3** = cooking dinner and your roommate wandering in to flirt. You picked your activity; they showed up because they happened to be there + dice rolled.

All three are **repeatable**. The dice in Lane 2 + Lane 3 mean the same scene can fire again on subsequent attempts (subject to per-canvas / per-activity / per-location cooldowns — see §8).

The fictional intent differs by lane:
- **Lane 1** carries *intentional escalation* moments (you decided to tease him; you decided to sleep with him). High-agency, low-surprise.
- **Lanes 2 + 3** carry *happens-to-you* moments (caught masturbating, groped while studying, walked in on you in the shower). Low-agency, high-charge. The randomness IS the emotional point — if these were menu buttons they'd lose their charge.

---

## §3 Brother walkthrough table — full lane classification

Source: in-game RTS Walkthrough → Stepbrother table, captured 2026-05-10 from `mopoga.com/road-to-success` v0.25. Fifteen scenes, classified by inspecting each scene's GUIDE column ("how to trigger this"). Verified against the source-extraction audit in doc 21.

Classification rule applied:
- **100% chance** + GUIDE recipe of "go to NPC's hub" = **Lane 1** (button at NPC hub, qualified by MC stats)
- **20-25% chance** + GUIDE recipe of just "go to location X" = **Lane 2** (location-entry random)
- **20-33% chance** + GUIDE recipe of "do activity Y at location X" = **Lane 3** (dispatcher inside menu activity)

| # | Scene | NPC reqs | MC reqs | Chance | GUIDE | **Lane** |
|---|---|---|---|---:|---|---|
| 1 | Stepbrother Bedroom Grope | arousal 🔥 | None | 20% | Go to your bedroom | **2** |
| 2 | Stepbrother Bedroom Study Grope | arousal 🔥 + corr 1 | None | 20% | Study at your room | **3** |
| 3 | Stepbrother Bedroom Study Grope Pregnant | arousal 🔥 + corr 1 + pregnant | corr 30 | 20% | Study at your room while pregnant | **3** |
| 4 | Sleep with Stepbrother | arousal 🔥 + corr 10 | corr 30 | 100% | Go to Stepbrother bedroom late at night and ask to sleep with him | **1** |
| 5 | Stepbrother Bedroom Flash | None | corr 5 | 100% | Go to your Stepbrother bedroom | **1** |
| 6 | Bedroom Tease | None | corr 5 | 100% | Go to your Stepbrother bedroom | **1** |
| 7 | Stepbrother Shower Sex | arousal 🔥 + corr 5 | corr 30 | 33% | Masturbate at shower at the house bathroom | **3** |
| 8 | Peep Stepbrother sex | None | corr 15 | 25% | Go to your Stepbrother bedroom | **2** |
| 9 | Playing Videogame Pregnant | arousal 🔥🔥 + corr 10 + pregnant | corr 30 | 20% | Play videogame at your living room while pregnant | **3** |
| 10 | Playing Videogame | arousal 🔥🔥 + corr 10 | corr 30 | 20% | Play videogame at your living room | **3** |
| 11 | Brother Help Study | arousal 🔥🔥🔥 + corr 15 | None | 20% | Study at your room | **3** |
| 12 | Brother Caught Masturbating | arousal 🔥🔥 + corr 10 | corr 30 | 25% | Go to your Stepbrother bedroom | **2** |
| 13 | Brother Bedroom Pregnant Sex I | None | None | 100% | Go to your Stepbrother bedroom while pregnant and have sex with him | **1** |
| 14 | Brother Bedroom Sex I | None | None | 100% | Go to your Stepbrother bedroom and have sex with him | **1** |
| 15 | Stepbrother Washing Dishes Sex | arousal 🔥🔥 + corr 10 | corr 30 | 20% | Go to the kitchen and wash the dishes | **3** |

**Distribution:**

| Lane | Count | % of 15 |
|---|---:|---:|
| **1 — Hub button** | 5 | 33% |
| **2 — Location-entry random** | 3 | 20% |
| **3 — Dispatcher inside menu activity** | **7** | **47%** |

**Lane 3 is the largest bucket.** Almost half of Brother's repeatable surfaces fire as random substitutions inside other menu activities. This is not an edge case — it's RTS's primary mechanism for "the NPC is everywhere in your day-to-day life without overstuffing menus."

The 7 lane-3 surfaces piggyback on **four parent activities**: Study (×3 — base, pregnant variant, Help Study), Play Videogame (×2 — base + pregnant variant), Shower→Masturbate (×1), Wash Dishes (×1). Each parent activity is a normal solo player choice; each substitution-eligible Brother scene is gated on `(Brother present at that location + Brother stats + MC stats + dice)`.

---

## §4 Live verification (Shower Sex — Lane 3 confirmed first try)

Session: resumed `rts-arc-trace` Chromium profile, restored prior save (mid-Marcus-park-date), navigated via `Engine.play('Hallway')` to test cleanly.

**State at test:** EM Monday · Brother location = `Bathroom` · MC corruption 200 / level 4 (≥ 30 needed) · Brother arousal 5 (≥ 🔥 needed) · Brother corruption 10 (≥ 5 needed). All four Shower Sex gates met.

**Click chain (verbatim from session):**

1. `Hallway` (image-grid home hub) → `handleSubLocation('Bathroom')`
2. `Bathroom` hub renders standard 5-button activity menu: **Shower / Mirror / Pregnancy pill / Pregnancy test / Hallway**
   - **Critical observation:** Brother is in this room but his presence is INVISIBLE at the hub level. No "Walk in on Brother" button. No auto-trigger. The hub is identical to a Brother-absent bathroom.
3. Click **Shower 🚿** → `BathroomShower` passage. Body: "You take a shower and wash all your body!" + 2 buttons (Masturbate, Bathroom return). Brother still invisible.
4. Click **Masturbate ❤️‍🔥** → engine routes through transient `BathroomShowerMasturbate` dispatcher passage → rolls 33% dice → **HIT first try** → substitutes to passage `BrotherShowerSex`
5. New body opens: "MASTURBATE 🚿 / The hot water cascades over you... / You hear the door… 👀". Video URL changed from generic `shower3.webp` to `brotherShowerEvent/brotherShowerEvent1.mp4`.
6. Click **You hear the door… 👀** (single linkreplace beat) → cascade reveals 4 more video stubs + 6 dialog beats between Robert and Victoria + new linkreplace **Join him ✅**. Pattern E linear cascade confirmed inside the substituted scene.
7. Bailed via **Bathroom 🚾** soft-escape return (always present on substituted scenes) → preserved walkthrough STATUS for clean future tests.

**The dispatcher passage is the structural primitive.** `BathroomShowerMasturbate` exists in source between the Shower menu and the masturbate content. Its only job: roll dice, route. Player POV: clicked Masturbate, either got vanilla content or got the Brother encounter, indistinguishably.

**Bonus Lane 2 verification:** Returning from the Walkthrough page back to Bathroom auto-triggered passage `BathroomFlashScene` ("Just as you were about to take off your clothes, you realize someone is spying on you 👀 / Flash to him / Go to shower"). This is Lane 2 firing on bathroom re-entry because Brother is here + stats qualify. Note the scene is NOT in Brother's NPC scene table — it lives in the LOCATION SCENES walkthrough section under Bathroom. Some lane-2 scenes are NPC-bound but cataloged under the location, not the NPC.

**Lane 1 NPC-presence gate verification:** Visited `BrotherBedroom` while Brother was in the Bathroom. Rendered: "Stepbrother's Bedroom / Your Stepbrother is not in his bedroom / Hallway 🚪". **Zero menu buttons.** Without him present, the entire hub menu collapses to just the return navigation.

---

## §5 How RTS announces lane-3 scenes (it doesn't, in fiction)

Discoverability lives entirely in two surfaces, both **outside the fiction**:

1. **Walkthrough page** — per-NPC scene table with REQUIREMENTS (NPC) + REQUIREMENTS (MC) + CHANCE + GUIDE + STATUS columns. Every scene is listed from Day 1 with the literal trigger recipe ("Masturbate at shower at the house bathroom"). Locked rows display 🔒 Locked. Completed rows flip to ✅. The player reads the recipe, sets up conditions, retries until the dice hit, sees ✅ tick.
2. **Sidebar** — every NPC's current location is shown continuously. Player sees "Brother is in the Bathroom" + remembers from walkthrough that bathroom-shower-masturbate triggers Shower Sex when Brother is there → goes to bathroom → showers → masturbates → either hits or misses (33%).

There is **no in-fiction notification** when a lane-3 scene becomes eligible. No "🔔 New scene unlocked!" toast. No journal entry. The player has to read the walkthrough and watch the sidebar.

**Implication for TLS:** if we want lane-3-style content to feel discoverable, we need a comparable pre-declaration surface — either an in-game walkthrough/scene-catalog (mirror of RTS), or per-canvas hint-card entries in the existing Quests page that surface "this could happen if X." Without that, lane-3 substitutions in TLS risk being invisible to players who don't read prose carefully.

---

## §6 TLS engine fitness — what's supported today

Map of TLS canvas categorization onto RTS lanes, with file:line evidence from the engine read:

| RTS lane | TLS analog | Status | Key file:line |
|---|---|---|---|
| **Lane 1 — Hub button** | NPC portrait at location → clicking routes to NPC's canvas → that canvas's `exit_block` of type `'choices'` renders conditional buttons | ✅ **Fully supported** | Schema: `template_import.py:382, 470, 503`. Renderer: `v1.py:3703` (renderNpcPortraits) + `v1.py:10141, 10185-10204` (per-choice `<<if>>` wrapping) |
| **Lane 2 — Location-entry random** | Canvas with `trigger_mode = "random"` + `chance` on a location-bound canvas → `checkRandomEncounters` substitutes hub render on entry | ✅ **Fully supported** | `v1.py:3919-3988` (checkRandomEncounters) + `v1.py:3680-3697` (getStoryCanvasRedirect dispatcher) |
| **Lane 3 — Dispatcher substitution** | (no primitive exists) | ❌ **Not supported** | Gap detailed in §7 |

**Architecturally, TLS is closer to RTS than initially expected.** The hub-button-injection-on-presence mechanism (RTS doctrine) is essentially the NPC portrait grid + per-canvas validity check. The location-entry random encounter pattern is the random-mode canvas. Both are real, both work today, both are battle-tested.

The only gap is Lane 3.

### §6.1 How Lane 1 actually works in TLS

Author flow:
1. Author a canvas representing the per-NPC interaction surface (e.g. `frank_bedroom_hub`)
2. Set its trigger to `manual + isRepeatable + npcId = npc_frank + location = loc_franks_bedroom + conditions: {time_band, presence}`
3. Location renders Frank's portrait (because of `npcId + repeatable`)
4. Player clicks portrait → routes to `frank_bedroom_hub` canvas
5. Canvas body contains an opening preamble ("Frank is at his desk, reading.")
6. Canvas's exit block, `type = 'choices'`, contains the hub menu — Talk / Tease / Flash / Have sex / Sleep with him — each with its own per-choice `conditions`
7. Engine emits each choice as `<<if cond>><<link "Tease" "frank_bedroom_tease_canvas">>...<</link>><</if>>`
8. Player sees only the buttons whose conditions match — exactly RTS-style

This is **slightly cleaner than RTS** in one respect: RTS's `BrotherBedroom` is a static Twine passage with conditional `<<if>>` blocks hand-written in the source. TLS's per-NPC hub is an authored canvas — you can have multiple canvas variants per stage (one per Frank stage, picked by `selectCanvasByPriority`), each with its own preamble and menu set, swapped automatically as Frank's arc progresses.

### §6.2 Per-choice conditional rendering — confirmed wired

`TemplateExitBlock` (`template_import.py:503`) has `type: 'location' | 'choices'`. With `type = 'choices'`, it carries a `List[TemplateChoice]`. Each `TemplateChoice` has:

- `conditions` — gating predicates
- `targetType: 'trigger' | 'location' | 'node'` + corresponding ID — where the button goes
- `show_when_locked` + `locked_text` + `locked_text_threshold` (S4 RTS-style threshold toast on locked-click)
- Effects (trait, flag, wardrobe, modifier, pass, item)
- `text_variants` — per-state text changes

The engine emission (`_process_exit_block` at `v1.py:10636`, then the rendering loop at `v1.py:10141-10360`) wraps each conditional choice in `<<if setup.triggerConditionsSatisfied(...)>>` (line 10188). At runtime, only buttons whose conditions match render. Per-choice `show_when_locked` Mode A renders greyed-out spans with optional threshold-publisher toasts on click; Mode B routes locked-clicks to a rejection canvas with rejection effects.

This IS the hub-button-injection mechanism. No engine work needed for Lane 1.

---

## §7 Lane 3 design recommendation — Option A (substitution config delegating to isCanvasValid)

Three options were considered:

| Option | Description | Verdict |
|---|---|---|
| **A. Substitution config on canvas trigger** | New `substitutions: List[Dict]` field on `TemplateTrigger`. Engine walks rules before normal render; substitutes target canvas if `(isCanvasValid(target) + Math.random() < chance + optional extra conditions)` all pass. | ✅ **Recommended** |
| **B. Author dispatcher canvases manually with body scripts** | Author empty canvas with `<<script>>Engine.play(...)<</script>>` body that does dispatching. | ❌ Blocked — block schema has no `script` or `goto` block type (verified `v1.py:11555+` block dispatcher; only `group / block_pool / cascade / image / video / clip / heading / paragraph / dialog / thought_bubble` exist). Adding either is the same effort as Option A but messier. |
| **C. Choice-level branching (weighted multi-target)** | Extend `TemplateChoice` to support multiple targets with weighted probabilities. | ⚠️ Wrong shape — RTS dispatcher rolls AFTER click+navigate, not during click. Conflates the click and the roll. |

### §7.1 The Option A design

**Schema additions** (`apps/projects/services/template_import.py`):

Add to `TemplateTrigger` dataclass (after the existing `chance` field around line 392):

```python
substitutions: List[Dict[str, Any]] = field(default_factory=list)
# Each rule shape:
#   {
#     "target_canvas_id": "frank_shower_event",
#     "chance": 0.33,
#     "conditions": {...}  # OPTIONAL extra gates beyond what target canvas declares
#   }
substitution_only: bool = False
# When True, this canvas is excluded from renderNpcPortraits + renderSoloActivities.
# It only fires via another canvas's substitution rule. Prevents the substituted
# scene from showing up as its own clickable button.
```

**Runtime helper** (`apps/game_generation/twee_comprehensive/generators/v1.py`, near `checkRandomEncounters`):

```javascript
setup.checkAndSubstituteCanvas = function(parentCanvasId) {
    var subs = (setup.canvasSubstitutions || {})[parentCanvasId] || [];
    for (var i = 0; i < subs.length; i++) {
        var s = subs[i];
        var target = setup.getCanvasById(s.target_canvas_id);
        if (!target) continue;
        if (!setup.isCanvasValid(target)) continue;
        if (s.conditions && !setup.triggerConditionsSatisfied(s.conditions)) continue;
        if (Math.random() < s.chance) {
            setup.markCanvasTriggered(target.id);
            Engine.play(target.passageName);
            return true;
        }
    }
    return false;
};
```

**Emitter injection** at top of every canvas's emitted passage body (`_generate_canvas_node_passages`, `v1.py:10028`):

```
:: Canvas_<id>
<<script>>if (setup.checkAndSubstituteCanvas("<id>")) return;<</script>>
[normal canvas content...]
```

**Selector tweaks** at `renderNpcPortraits` (`v1.py:3703`) + `renderSoloActivities` (`v1.py:3817`): skip canvases with `substitution_only = true`.

**TOML author pattern** (concrete example):

```toml
# Frank's solo activity: Cook Breakfast in the kitchen.
[[canvases]]
id = "cook_breakfast"
name = "Cook Breakfast"
[canvases.trigger]
location = "loc_kitchen"
trigger_mode = "manual"
is_repeatable = true
max_triggers_per_day = 1
schedules = [{ weekdays = [0,1,2,3,4], start_time = "07:00", end_time = "09:00" }]
[[canvases.trigger.substitutions]]
target_canvas_id = "frank_kitchen_morning_substitution"
chance = 0.33
# Frank kitchen morning substitution — only fires via the cook_breakfast dispatcher.
[[canvases]]
id = "frank_kitchen_morning_substitution"
name = "Frank in the kitchen"
[canvases.trigger]
location = "loc_kitchen"
npc = "npc_frank"
trigger_mode = "manual"
is_repeatable = true
substitution_only = true
schedules = [{ weekdays = [0,1,2,3,4], start_time = "07:00", end_time = "09:00" }]
conditions = { version = "1.0", items = [
  { type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "stage", op = "gte", value = 2 },
] }
```

When the player clicks Cook Breakfast at 07:30 on a weekday with Frank Stage ≥ 2, the engine rolls 33%. If hit, Frank's substitution canvas fires instead of the normal cook-breakfast content. If miss, normal cook-breakfast content renders. Player POV: just tried to cook; sometimes Frank shows up.

### §7.2 Why this design is clean

Two pieces of luck make this simpler than expected:

**(a) Cooldowns are already handled.** When a substituted canvas fires, `markCanvasTriggered` increments both per-canvas (`trigger_history`) and per-activity (`activity_trigger_history`) counters automatically. So the substituted canvas's own `is_repeatable` / `max_triggers_per_day` / `name`-shared cap throttle re-fires. No new bookkeeping needed. (Cooldown layer analysis in §8.)

**(b) No new predicate types needed.** The substitution rule just names a target canvas. The target canvas's own trigger (`location` + `schedules` + `npc` + `conditions`) inherently gates "is Frank at this location at this time with the right stats." Delegating to `isCanvasValid(target)` resolves "is this scene currently appropriate to fire" without needing an `npc_at_location` predicate or a `time_band` predicate. (Predicate vocabulary analysis in §9.)

### §7.3 Engine work outline (high-level)

| Task | Estimate |
|---|---:|
| Add `substitutions` + `substitution_only` fields to `TemplateTrigger` schema + parser + validator (`template_import.py`) | 30 min |
| `substitution_only` selector tweaks in `renderNpcPortraits` + `renderSoloActivities` (`v1.py`) | 30 min |
| Runtime helper `setup.checkAndSubstituteCanvas` (`v1.py`, near checkRandomEncounters) | 20 min |
| Emitter injection at canvas passage body top (`_generate_canvas_node_passages`, `v1.py:10028`) | 30 min |
| Serializer pass-through (`template_import.py`) | 15 min |
| Tests (schema round-trip + engine emission + runtime substitution) | 45 min |
| **Total** | **~2.5 hr** |

Detailed file:line implementation plan deferred to a separate plan-mode session. This doc captures the design only.

---

## §8 Cooldown decision — don't extend Layer 3 to Lane 3

TLS has three independent cooldown layers:

| Layer | Function | Scope | What it tracks |
|---|---|---|---|
| **1. Per-canvas** | `setup.canTriggerCanvas` (`v1.py:2972`) | Single canvas ID | `trigger_history[id] = {total, dayKey, dayCount}` |
| **2. Per-activity-name** | `setup.canTriggerActivity` (`v1.py:3012`) | Activity name, shared across same-`name` tier canvases | `activity_trigger_history[name] = {dayKey, dayCount}` |
| **3. Per-location random** | `random_cooldowns[locId]` (`v1.py:3927-3932, 3979`) | Location | Visit-decremented integer, set to **3 visits** after a random fires |

**Layer 3 is exclusively the Lane-2 random-encounter throttle** — set only inside `checkRandomEncounters`. Once a Lane-2 random fires at a location, ALL Lane-2 randoms there are blocked for 3 subsequent visits.

**Decision: Lane 3 substitutions inherit Layers 1 + 2 automatically (via `markCanvasTriggered`), and do NOT inherit Layer 3.** Three reasons:

1. **Layers 1 + 2 already throttle adequately.** Author controls per-canvas total/daily caps and per-activity-name daily caps via the substituted canvas's own TOML.
2. **RTS doesn't have Layer-3-style cooldowns** (per source audit doc 21). Random encounters in RTS use chance + conditions + activity-level daily caps, no cross-attempt visit cooldown.
3. **Extending Layer 3 to Lane 3 would over-constrain authoring.** "Frank shower-sex hit → Wash Dishes can't even roll for 3 visits" is far more conservative than RTS feel.

### §8.1 Side-finding worth flagging

**TLS's current Lane 2 (3-visit per-location cooldown) is stricter than RTS's Lane 2** (no cross-attempt cooldown observed in source). After any random encounter fires at a TLS location, all randoms there are blocked for 3 visits; in RTS, each entry rolls fresh.

This is a one-line tunable at `v1.py:3979` (`cooldowns[locKey] = 3` → lower number, or per-canvas configurable). Worth knowing if Lane 2 ever feels too quiet in playtest. Not addressed by this doc — flagged only.

---

## §9 Predicate vocabulary — sufficient, with one nuance

`setup.triggerConditionsSatisfied` (`v1.py:2684-2952`) accepts a `{version, logic, items}` object where each item has `type` + `subject` + type-specific fields:

| Type | Subject | Operators | What it checks |
|---|---|---|---|
| `flag` | player / npc | `exists`, `is_true`, `is_false` | Boolean flag on player or NPC |
| `trait` | player / npc | `eq`, `ne`, `gt`, `gte`, `lt`, `lte`, `in`, `not_in`, `contains`, `not_contains`, `exists`, `not_exists` | Numeric/string trait value (with modifier offset for player) |
| `modifier` | (any) | `is_active`, else | Temporary modifier active state |
| `days_since_flag` | player / npc | comparison ops | Days since a flag was set (uses `flags_meta.set_day`) |
| `clothing_slot` | (any) | `equipped`, `unequipped` | Wardrobe slot state |
| `clothing_item` | (any) | `equipped`, `unequipped`, `owned`, `not_owned` | Specific clothing item state |
| `pass` | (any) | `is_active`, else | Recurring pass active |
| `item` | (any) | comparison ops | Inventory item count |
| `stage` | (any) | `is_true`, `is_false` | Named composite gate (recurses into `stage_helpers_map`) |

Top-level `logic: "AND"` (default) or `"OR"` composes the items.

### §9.1 The one nuance: NPC location is not a queryable predicate

There is **no `npc_location` predicate type**, and **no `time_band` predicate type**. NPC location in TLS is not a stored variable — `setup.getNpcLocation` (`v1.py:2357`) computes it on demand by scanning the NPC's scheduled canvases and finding the one whose time window is currently active. There is no `npcs[uuid].location` field that an author could query via a `trait` predicate.

This *would* be a problem for Lane 3 if substitution rules tried to express "fire only if Brother is at this location" themselves. The Option A design sidesteps the issue entirely: the substitution rule names a target canvas, and the target canvas's own trigger (`location` + `schedules` + `npc`) inherently gates "is the NPC at this location at this time." `isCanvasValid(target)` evaluates all of that. No new predicate types needed.

The optional extra `conditions` predicate on the substitution rule itself uses the existing vocabulary — perfect for "fire only if MC also has corruption ≥ X" or "fire only if some flag is set" beyond what the target canvas already gates.

---

## §10 Authoring framework — how Lane 1 + 2 + 3 compose for one NPC arc

§2 covers the lane mechanics (HOW each lane fires). This section covers what KIND of canvas belongs in each lane and how the lanes compose into a coherent arc that builds player experience over time. RTS doesn't distribute canvases across lanes for variety — it uses each lane to deliver a different kind of player relationship with the NPC. The framework below makes that explicit so we can replicate it deliberately for Frank, Ryan, Jake, Diana, and any future NPC arcs.

### §10.1 The fictional-intent axis — what each lane MEANS for the player

Each lane corresponds to a different relationship between **player agency** and **NPC presence**:

| Lane | Player agency | Who initiates | Fictional intent | Emotional register |
|---|---|---|---|---|
| **1 — Hub button** | High — player chose | Player | "I am escalating with this NPC" | Owns the act, intentional, full agency |
| **2 — Location-entry random** | None — dice picked | The world | "He's in my world. We coexist." | Atmospheric, ambient, "he was just there" |
| **3 — Dispatcher inside activity** | Mixed — chose activity, not encounter | Engineered coincidence | "I was doing X and he happened" | Charged surprise + complicity |

The same NPC act reads completely differently depending on which lane delivers it. Tease via Lane 1 = Maya decided to put on a show. Tease via Lane 3 = Maya was changing her clothes and Brother walked in mid-strip. Same physical act, different fictional weight, different emotional register, different downstream consequences for how the player experiences the relationship. **Authoring a scene means picking the right lane for the emotional weight you want it to carry.**

### §10.2 Content-type vocabulary per lane (what KIND of canvas goes where)

Reading RTS Brother's 15 surfaces back through the fictional-intent lens reveals the deliberate vocabulary RTS uses for each lane:

#### §10.2.A Lane 1 — intentional escalation moments

**Player picks WHAT to do.** Vocabulary categories:

- **Relational** — Talk button (build trust, no escalation)
- **Self-display** — Tease, Flash (exhibitionism Maya owns)
- **Consummation** — Sex 1, Pregnant Sex 1 (explicit intentional)
- **Late-game intimacy** — Sleep with him (relational + intimate, LN only)

What does NOT belong in Lane 1: groping, walk-ins, things-that-happen-TO-Maya. The player picking "let him grope me" strips the encounter of its passive charge. Groping has to come AT Maya, not from Maya. Lane 1 is the agency lane — it carries acts the player consciously claims.

#### §10.2.B Lane 2 — ambient world-presence moments

**The NPC just exists in the same space.** Vocabulary categories:

- **Pass-by** — Brother passing in hallway with mug, NPC spotted from window
- **Solo activity glimpse** — NPC making coffee alone, smoking on porch, fixing the radio
- **Passive contact** — Bedroom Grope (he's at home, you sleep, he gropes; you didn't ask, but neither did he plan it as a Big Moment)
- **Atmospheric voyeurism** — Peep Brother sex (you walked into the wrong room at the wrong time)

What does NOT belong in Lane 2: high-agency consummation. Brother won't have full sex with Maya via Lane 2 because Lane 2 is dice — and full sex needs to be earned via player choice. Lane 2 carries **brief, low-stakes contact** that builds the texture without taking the wheel.

#### §10.2.C Lane 3 — interruption / walk-in moments

**Maya was doing something solo. NPC arrives mid-activity.** Vocabulary categories:

- **He walks in** — Shower Sex (Brother walks in while Maya masturbates), Wash Dishes Sex (he's there when she starts chores)
- **He arrives while vulnerable** — Help Study (she's studying, he comes in to "help"), Playing Videogame (she's gaming, he sits next to her)
- **Innocent setup → charged shift** — the SETUP has to be a non-NPC activity (Maya is alone in her own fiction), then the NPC arrives and the scene transforms

The crucial structural rule: **the parent activity must be authentically not-about-the-NPC**. Maya wasn't trying to seduce Brother by showering — she was just showering. The seduction happens TO her. That's what makes Lane 3 carry the "happens to you" emotional weight that Lane 1 can't.

### §10.3 The 3×3 grid — lanes × stat tiers

Within each lane, scene intensity scales with stat tier (Pattern D mechanism in audit terms — same scene entry, deeper cascade as stats grow). Crossing the lane axis with the tier axis produces a 3×3 grid that's the canonical authoring template:

| | **Lane 1 (intentional)** | **Lane 2 (ambient)** | **Lane 3 (walk-in)** |
|---|---|---|---|
| **Tier 1 — early arc** (low stats) | Talk-style relational | He passes by (presence) | He notices what you're doing (PG charged) |
| **Tier 2 — mid arc** (mid stats) | Tease / Flash / mild self-display | He gropes you while studying (passive contact) | He walks in mid-change (interruption + dialogue) |
| **Tier 3 — late arc** (high stats) | Sex / Sleep with him (explicit intentional) | Caught masturbating, sexual ambient encounter | He joins you in the shower (full walk-in cascade with consummation) |

**Authoring an NPC arc properly means populating cells across this grid** — not just throwing scenes into any lane.

Doctrine for what each grid imbalance produces:
- **All Lane 1** → fully transactional experience, low surprise, "menu game" feel
- **All Lane 2** → atmospheric but inert, Maya passive throughout, no agency
- **All Lane 3** → things constantly happen TO Maya, player feels acted-upon, no agency over outcomes
- **Mix across all three lanes, all three tiers** → **alive**

The proper authoring shape is filling all 9 cells at varying density (not all cells need to be equally dense, but none should be empty without explicit reason).

### §10.4 Arc-flow doctrine — Lane 1 leads, Lanes 2+3 follow as consequences

This is the most important framing in the whole framework. **Lane 1 leads the arc; Lanes 2+3 follow as consequences of Lane 1 escalation.**

The player drives the relationship by clicking Lane 1 buttons (Tease, Flash, Sex). Each click raises the stats (corruption, NPC arousal, NPC trust). When stats cross thresholds, **Lane 2 and Lane 3 content lights up as a consequence** — random encounters become eligible, walk-ins start firing inside daily activities.

This produces the "world fills out around me as I escalate" feeling. The player feels their intentional choices are reshaping the world. Lane 2/3 content rewards Lane 1 commitment.

The inverse design — "Lane 2/3 lead, Lane 1 follows" — would produce a passive game where things keep happening to Maya regardless of her choices. RTS deliberately doesn't do this. **Even though Lane 2/3 outnumber Lane 1 by canvas count (10/15 of Brother's surfaces vs. 5/15), Lane 1 is the causal driver.** Without Lane 1 escalation, most Lane 2/3 content stays dormant.

The §10.6 per-NPC progression table below is the concrete instantiation of this doctrine: each Frank stat threshold triggers content unlocks across all three lanes simultaneously.

### §10.5 Narrative-shape doctrine — how scenes open and close per lane

Each lane has a different scene-opening shape because the agency structure differs:

| Lane | Opens with | Closes with |
|---|---|---|
| **1** | Player's choice already made — "You decide to tease him..." | Player exits via choice or returns to hub |
| **2** | Setup of the context Maya was in — "You walk into the hallway..." → encounter substitutes the hub render | Cascade plays + returns to hub |
| **3** | Maya's solo activity in progress — "You step into the shower, the hot water cascades..." → NPC arrives → charged shift in tone | Choice point (Accept / Bail) for high-stakes scenes; cascade for medium |

Lane 3's specific structural rule worth surfacing: **low-agency setup, choice-driven payoff**. Maya didn't choose to be walked in on, but once it happens, she chooses whether to engage (Join him / Tell him to leave / Cover up). This protects player agency on the explicit content while removing it from the setup. Pattern F in the audit terms (the Accept/Decline branching cascade — see doc 21 §4) shows up most often inside Lane 3 walk-ins — that's not a coincidence; it's the natural narrative shape for "I was surprised + now I'm choosing."

### §10.6 Per-NPC progression — shared stat thresholds across lanes

**Per-NPC progression doctrine: shared stat thresholds across multiple lanes.** This is the concrete mechanism that produces the §10.4 "world is alive" effect.

When Frank's stage / corruption crosses a threshold, multiple things light up simultaneously across his locations:

| Threshold crossed | Lane 1 effect | Lane 2 effect | Lane 3 effect |
|---|---|---|---|
| Frank stage 2 | New button appears in Frank's office hub (e.g., "Stand close while he reads") | Random hallway-pass-by encounter eligible | Cook-breakfast dispatcher rolls Frank vignette at 33% |
| Frank stage 3 | Office hub adds "After hours" button (LN-only) | Random office-after-hours peep eligible | Read-newspaper dispatcher rolls Frank-on-couch at 25% |
| Frank stage 4 | Bedroom hub unlocks (terminal) | Random bedroom door-open eligible | Wash-dishes dispatcher rolls Frank-behind-you at 33% |

**One stat threshold = multiple gates clear simultaneously = "world feels alive."** The player doesn't think "the kitchen menu changed"; they think "Frank is suddenly everywhere." That perception is the §10.4 doctrine producing player-felt effects.

### §10.7 Frank gap analysis — applying the 3×3 grid

Mapping Frank's current canvas inventory (post Lane 1+2 doctrine alignment shipped 2026-05-11) onto the 3×3 grid:

| | Lane 1 (intentional) | Lane 2 (ambient) | Lane 3 (walk-in) |
|---|---|---|---|
| **Tier 1** (low stats / early stages) | ✅ Talk (office hub), Help with bookkeeping | ✅ Coffee alone, radio, fence | ❌ MISSING |
| **Tier 2** (mid stats / mid stages) | ✅ Bend over the page (locked at low stage), supervised work | ✅ Hallway pass, paper, smoke, Diana phone | ❌ MISSING |
| **Tier 3** (high stats / late stages) | ✅ Bedroom hub menu (Sex, intimate options) | ✅ Late night raid, hallway door evening | ❌ MISSING |

**Frank has zero Lane 3 content at any tier.** This is not a quantity problem — Frank has 31 canvases, more than Brother's 16. It's a **content-TYPE gap**. The entire emotional register of "Maya was doing something innocent and Frank arrived in a charged moment" is missing from the arc.

When Lane 3 ships per PRD 25, the right Frank authoring pass is to fill the Lane 3 column at all three tiers:

- **Tier 1 walk-in** — Frank passes through while Maya's reading at the kitchen table (PG, relational, builds presence)
- **Tier 2 walk-in** — Frank arrives while Maya's making coffee in her shorts (mild charged, dialogue-driven)
- **Tier 3 walk-in** — Frank joins Maya washing dishes (full sexual cascade, post-Stage-3 only)

These attach as substitutions on parent solo activities (Read at table, Make Coffee, Wash Dishes). Each is its own canvas with `substitution_only = true`, gated by Frank's stage + the activity's location/schedule. The player picks the activity; Frank shows up sometimes; the world feels alive with him in a way the current arc can't deliver.

### §10.8 Edge cases — when the framework gets challenged

Three places the framework gets fuzzy in practice. Worth flagging now so future authoring decisions can be conscious about which side of the line a scene falls on.

#### §10.8.A Lane 1 vs Lane 3 ambiguity

Some scenes are genuinely ambiguous — e.g., is "Have dinner together with Frank" a Lane 1 button (Maya chooses to sit and eat with him) or a Lane 3 substitution on the Make Dinner activity (Frank arrives at the table while Maya's serving)? Both readings work; the choice depends on which emotional weight the scene needs to carry. **If the scene's drama is Maya's deliberate move toward intimacy, it's Lane 1. If the scene's drama is unexpected proximity at a charged moment, it's Lane 3.** Same content, different lane = different fiction.

#### §10.8.B Lane 2 vs Lane 3 ambiguity

Some scenes blend Lane 2 and Lane 3 — e.g., Maya enters the kitchen at 7am and Frank's there making coffee. Is that Lane 2 (location-entry random encounter) or Lane 3 (substitution on whatever activity Maya was about to do — Make Breakfast / Get Coffee)? RTS handles this by making the parent activity literally the location entry — but TLS could split: location-entry random for "you walked in on him" vs. activity substitution for "he showed up while you were doing X." Decide per-scene based on whether the focus is **the encounter** (Lane 2) or **the activity-then-encounter** (Lane 3).

#### §10.8.C Capstone moments are outside the framework

The framework breaks for once-per-arc story beats. Frank's office crack, bedroom invitation, bedroom first night are explicit story moments that don't fit cleanly in any of the three lanes — they're auto-fire one-shots (a fourth lane outside the repeatable-content discussion), and that's correct. The 3-lane framework applies to **repeatable content only**. Capstones use `is_repeatable = false + trigger_mode = "manual"` and fire via `selectAutoFireCanvasForLocation` (`v1.py:3236`) — a separate engine path with its own design rules (one-shot, irreversible, narrative-pacing-driven).

### §10.9 Anti-pattern: verb overlay

The seductive but wrong intuition is to define Tease as a verb that follows Frank wherever he is. RTS doesn't do this. The reason: tease in the bedroom (lights-out intimacy) reads differently than tease in the kitchen (Diana-down-the-hall risk) than tease in the office (rule-break). A single verb canvas teleporting can't write to all three contexts honestly.

**Per-context authoring + shared stat thresholds + Lane 3 dispatcher substitutions** is the doctrine. Each location-specific Frank scene is its own canvas with its own preamble and cascade. The shared stat thresholds (§10.6) make them all light up together. The Lane 3 substitutions slip them into existing solo activities so the player encounters Frank during ordinary daily routines without needing an explicit "interact with Frank here" button.

### §10.10 Authoring next steps for Frank (post-Lane-3-ship)

After PRD 25's engine work ships:

1. **Inventory existing solo activities** at Frank-relevant locations (kitchen morning routines, office work activities, hallway pass-bys, living-room evening activities, back porch). These become parent canvases for substitution.
2. **Author per-location Frank substitution canvases** — fill the Lane 3 column of the §10.7 grid at all three tiers. Each canvas: `substitution_only = true`. Pattern E or D cascade body. Tier-appropriate intensity per §10.3.
3. **Add substitution rules** to the parent activities pointing at the Frank canvases, with stage-appropriate chance %.
4. **Use shared stat thresholds (§10.6)** so multiple Lane 3 substitutions become eligible at the same Frank stage transition — same arc-flow doctrine (§10.4) that drives the Lane 1+2 lighting-up at each tier.
5. **Surface discoverability** — extend the Quests / hint system to enumerate "Frank may appear if you (cook breakfast / wash dishes / read newspaper) at the right time" once relevant stat tiers are reached. Mirror RTS's walkthrough pre-declaration (per §5).

---

## §11 Confidence ladder

Per methodology rule §N (use both extraction AND play, never one alone):

✅ **HIGH confidence (source-verified + live-verified):**
- 3-lane taxonomy matches Brother's 15 walkthrough scenes (table in §3)
- Lane 3 dispatcher mechanism (BathroomShowerMasturbate → BrotherShowerSex) verified live first-try
- Lane 2 location-entry random (BathroomFlashScene on bathroom re-entry) verified live incidentally
- Lane 1 NPC-presence gate (empty BrotherBedroom hub) verified live
- TLS Lane 1 + Lane 2 fully supported (engine code read end-to-end with file:line cites in §6)
- Lane 3 not currently supported by TLS engine (gap analysis in §7)
- Cooldown layer separation (1 vs 2 vs 3, §8)
- Predicate vocabulary completeness (§9)

🟡 **MED confidence:**
- 7/15 lane-3 count for Brother — Shower Sex tested live, other 6 follow same GUIDE pattern but not individually clicked
- Cross-NPC generalization to Dad / Marcus / Edward — walkthrough format identical across NPCs (per docs 21 + 22), so likely same mechanism, but not verified with live click-tests this session
- Whether RTS lane 2 truly has zero cross-attempt cooldown — didn't test multiple consecutive entries to fail-then-hit; inferred from source

❌ **NOT established this session:**
- Per-day cooldown semantics for RTS lane 3 (didn't test "fire same scene twice in one day to see if it can or can't")
- Whether RTS handles substitution-rule order when multiple substitutions could fire (proposed first-match policy, not RTS-verified — RTS may not have this case since dispatcher passages are per-activity, not per-NPC-multiplexed)
- Whether the 3-visit Lane 2 cooldown in TLS feels too quiet in actual playtest (no comparative play data)

---

## §12 Cross-references + source artifacts

**Doctrine docs (this folder):**
- Doc 13 — Road to Success Reference (broad RTS catalog)
- Doc 21 — RTS Brother Mechanism Audit (source-extracted, 16 Brother passages)
- Doc 22 — RTS Cross-NPC Mechanism Comparison (source-extracted, 40 surfaces / 4 NPCs)

**Live-play artifact:**
- `game_explorations/rts-arc-trace/synthesis_repeatable_narrative_auto_2026-05-10.md`

**Compressed memory:**
- `~/.claude/.../memory/rts_lane3_dispatcher_pattern.md`

**Engine code (TLS):**
- `apps/projects/services/template_import.py` — schema (TemplateTrigger:382, TemplateChoice:470, TemplateExitBlock:503)
- `apps/game_generation/twee_comprehensive/generators/v1.py` — engine
  - `:2357` `getNpcLocation` (NPC location computed from schedules, not stored)
  - `:2684-2952` `triggerConditionsSatisfied` (predicate vocabulary)
  - `:2972` `canTriggerCanvas` (Layer 1 cooldown)
  - `:3012` `canTriggerActivity` (Layer 2 cooldown)
  - `:3236` `selectAutoFireCanvasForLocation`
  - `:3406` `isCanvasValid`
  - `:3680-3697` `getStoryCanvasRedirect` (location-entry dispatcher)
  - `:3703` `renderNpcPortraits` (Lane 1 NPC portrait grid)
  - `:3817` `renderSoloActivities` (Lane 1 solo activity buttons)
  - `:3919-3988` `checkRandomEncounters` (Lane 2 random + Layer 3 cooldown)
  - `:10028` `_generate_canvas_node_passages` (where Lane 3 emitter injection would go)
  - `:10141, 10185-10204` per-choice conditional `<<if>>` wrapping (Lane 1 confirmation)
  - `:10636` `_process_exit_block`

**Walkthrough scene table source:**
- In-game RTS Walkthrough → Stepbrother (`https://mopoga.com/road-to-success` v0.25, captured 2026-05-10)

---

End of doc.
