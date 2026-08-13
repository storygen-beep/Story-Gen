# Engine card — only what a design decision depends on

Every line here was read out of the source during this skill's construction and carries its
citation. **Nothing was copied from anywhere.** If a fact you need is not here, go read
`apps/game_generation/twee_comprehensive/generators/v2.py` (referred to below as `v2.py`) and
add it *with* its `file:line`. Never assert engine behaviour from memory — this file exists
because memory was wrong twice while it was being written.

Paths are relative to `story_gen_web_app/story_gen_django/`.

---

## 1. `is_repeatable` defaults to TRUE when the key is absent

```python
v2.py:10937   "is_repeatable": trigger.is_repeatable if trigger else True
v2.py:11010   is_repeatable = getattr(trigger, 'is_repeatable', True) if trigger else True
apps/stories/models.py:355   is_repeatable = models.BooleanField(default=True, ...)
```

**Why it matters for design:** a canvas with no `is_repeatable` key is standing content, not a
one-shot. Assuming otherwise inverts your read of what the game actually is. A grep-based pass
that assumed `false` reported one game as 33% repeatable when the majority was repeatable.

---

## 2. Conditions **fail open** without `version = "1.0"`

```js
v2.py:3820   if (!conditions.version || conditions.version !== '1.0') return true;
```

**Why it matters:** a gate missing its `version` passes for everybody, silently, with a green
build and no error. Every `conditions` block you author carries `version = "1.0"`.

Shape:

```toml
conditions = { version = "1.0", logic = "AND", items = [
  { type = "flag",  subject = "player", flag_key  = "…", operator = "is_true" },
  { type = "trait", subject = "player", trait_key = "…", operator = "gte", value = 20 },
] }
```

---

## 3. Effects say `trait`. Conditions say `trait_key`.

Same concept, different key, and mixing them up is invisible:

```toml
# CONDITION
{ type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 20 }

# EFFECT
{ targetType = "player", trait = "corruption", op = "add", value = 2, clamp = true }
```

Effects live at `nodes[].exit_block.config.effects` and `nodes[].exit_block.choices[].effects`.
Flags use `flagEffects` with the key `flag`, at the same two places.

**`clamp = true` matters.** Unclamped effects can drive a trait negative or past its top band,
and a value outside every band makes the sidebar row silently vanish.

---

## 4. Meter ceilings live in `sidebar_items[].bands[]`

Not in `[player.core_traits]`, which is a flat `{ key = initial_value }` map with no maxima.

```toml
[[sidebar_items]]
type  = "trait_status_text"
trait = "corruption"
bands = [ { min = 0, max = 24, text = "…" }, … ]
```

A top band with **no** `max` is unbounded by design and promises nothing. A top band *with* a
`max` is a promise: content must exist up to it.

---

## 5. Media: a fixed file, or a folder that cycles

```toml
{ type = "video", props = { file = "sex/thing_t5.webm", description = "…", search_queries = […] } }
{ type = "video", props = { pool_dir = "sex/thing_t5", pool = 4, description = "…", search_queries = […] } }
```

```python
v2.py:11888   def _resolve_pool_dir(self, pool_dir)     # contents discovered from disk
v2.py:11902   def _media_pool_key(...)                  # cycle state key
v2.py:11908   # ... $game_state.media_cycle
v2.py:11872-11874  # `pool_dir` is preferred: the count is never hardcoded, so the human curates
```

Pools **cycle** (1→2→3→1) through `$game_state.media_cycle` rather than re-rolling, so the
player never sees the same clip twice running. `pool_dir` is preferred over an explicit file
list because the count comes from disk.

Media blocks also appear nested — under group blocks (`blocks[].blocks[].props`) and inside
cascade beats (`blocks[].props.beats[].blocks[].props`). Any tool walking media must recurse.

---

## 6. Schedules, and overnight windows

```toml
[[npcs.schedules]]
location = "…"; weekdays = [0,1,2,3,4,5,6]; start_time = "22:00"; end_time = "04:00"; activity = "…"
```

**Wrapping past midnight is supported.** From `setup.isCurrentTimeSlot` in `v2.py`:

```js
// Handle overnight (e.g., 22:00-06:00)
if (endTotal < startTotal) return currentTotal >= startTotal || currentTotal < endTotal;
```

Call sites: `v2.py:3448`, `:3465`, `:3612`. An omitted `end_time` defaults to start + 60 min
(same function).

⚠️ An older note in our own memory claims a window cannot cross midnight and needs two rows.
The source above contradicts it. Either the engine was fixed or the original observation was
about a different path — **verify live before splitting a window.**

---

## 7. Random events have a per-location cooldown

```js
v2.py:5190   var cooldowns = sv.game_state.random_cooldowns = sv.game_state.random_cooldowns || {};
             // after a random event fires, skip N visits before rolling again
```

Cooldown is engine-managed per location — do not author your own. Random canvases are
selected by `triggerMode === "random"`.

`max_triggers_per_day` is read per trigger (`v2.py:11011`).

---

## 8. Linking between canvases

```toml
[[canvases.nodes.exit_block.choices]]
text = "…"; targetType = "node"; nodeId = "<canvas_id>.<node_id>"
```

A canvas with **no** `trigger` block is a link target — it has no location of its own and
inherits its context from whatever links into it. Substitutions use
`trigger.substitutions[].target_canvas_id`.

`show_when_locked = true` on a choice renders it greyed and visible instead of hidden. This is
the mechanism behind "every release ends on a visible locked door."

---

## 9. Narration person is per-game and immutable

```toml
[settings]
narration_person = "second"   # or "first" / "third"
```

Declared once. Changing it after a release rewrites every line of prose in the game.

---

## 10. The location graph — children forward, "Leave X" back

`navigation_order` lists **children only**. The validator enforces it:

> `navigation_order for 'her_room' includes 'the_landing' which is not a destination
> (entry_from != 'her_room')`

The return link is **generated automatically** from `entry_from` and renders as
**`Leave <Location Name>`** — not as the parent's name. A room with
`navigation_order = []` is therefore *not* a dead end.

```toml
[[locations]]
id = "the_landing"; entry_from = "the_front_room"
navigation_order = ["her_room", "the_bathroom", "the_box_room"]   # children

[[locations]]
id = "her_room";  entry_from = "the_landing";  navigation_order = []   # leaf, still exitable
```

Confirmed live: from `her_room` the only story links are `Change Clothes` and
`Leave Her Room`.

---

## 11. Validator rules that will stop a build

Each of these failed a real build during this skill's first use:

- **`trait_decay` values must be POSITIVE magnitudes.** `hygiene = -10` is rejected with
  *"must be >= 0"*. Write the amount to lose, not a delta.
- **`customizable = true` requires `[[player.customization_fields]]`.** Set it `false` unless
  you are actually shipping the fields.
- **`navigation_order` may only list children** (above).

---

## 12. The Start passage is an age gate, not the game

`Start` initialises state and then renders a title screen. The starting canvas is reached
through the gate link — `[[✓ I am 18 or older - Enter Game->StartingCanvas_<canvas>_Node_<node>]]`.
Nothing auto-plays before it, and `player.current_location` is `""` until the first canvas or
location passage runs.

**Consequence for any play-test harness:** click the age gate first, or you will conclude the
opening is broken when it is fine.

**Rendered links** are `a.link-internal` inside `#story`. A bare `text=` selector also matches
the embedded `<tw-passagedata>` source and will resolve to an invisible element.

---

## 13. Exit blocks use SECTION syntax, not nested inline tables

A multi-line inline table is a TOML parse error, and an `exit_block` with conditional choices
is unavoidably multi-line. Write it as sections — the shipped game does this 199 times:

```toml
[[canvases.nodes]]
id = "base"
blocks = [ … ]                       # arrays of inline tables are fine, even multi-line

[canvases.nodes.exit_block]
type = "choices"

[[canvases.nodes.exit_block.choices]]
text       = "Take him upstairs."
targetType = "node"
nodeId     = "loop_cal_sex.base"
conditions = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "nerve", operator = "gte", value = 55 },
] }

# a location exit
[canvases.nodes.exit_block]
type = "location"
text = "Leave him to it."

[canvases.nodes.exit_block.config]
destinationType = "specific"
locationId      = "the_front_room"
time_progression_minutes = 30
effects = [ { targetType = "npc", npcId = "npc_cal", trait = "lust", op = "add", value = 2 } ]
```

`conditions = { … items = [ … ] }` *may* span lines, because newlines are legal inside the
array. Two levels of nesting is where it breaks.

---

## 14. The third key asymmetry — `npc_id` vs `npcId`

| | condition | effect |
|---|---|---|
| the trait | `trait_key` | `trait` |
| the character | `npc_id` | `npcId` |

```toml
{ type = "trait", subject = "npc", npc_id = "npc_cal", trait_key = "lust", operator = "gte", value = 20 }
{ targetType = "npc", npcId = "npc_cal", trait = "lust", op = "add", value = 3 }
```

---

## 15. `locked_text` REPLACES the choice label

A choice with `show_when_locked = true` renders as `<span class="locked-choice">`. If
`locked_text` is set, that string is shown **instead of** the action text — the player never
sees what the action was called.

**Trade-off, decide deliberately:** omit `locked_text` and the greyed row shows the action
("Stop pretending it's a secret") — a *want* the player can name, which is what sells the next
release. Set it and the row shows the reason instead ("Not yet — he still thinks he's getting
away with it") — clearer about the gate, weaker as a door. Prefer the want unless the gate is
genuinely obscure.

Verified live: at `nerve` 60 against a 75 gate, the row rendered as
`SPAN.locked-choice :: Not yet — he still thinks he's getting away with it.`

---

## 16. A flag read by a TRIGGER **or a CHOICE** must be set from a LOCATED canvas

The flag-chain validator **hard-fails the build** otherwise:

```
❌ Flag Chain Validation Failed:
   ✗ dean_open
     Required by: Dean (late)
     Issue: MISSING HINT - set by 'Come down in what you slept in' but no location/schedule
```

A triggerless rung has no location, so a flag set in its `exit_block` cannot be pointed at —
the game has no way to tell the player where to go and earn it.

**Fix: put the `flagEffects` on the hub CHOICE that opens the rung**, not on the rung's exit.
The choice lives on a located canvas, the semantics are identical (clicking the choice *is*
doing the scene), and the chain resolves.

```toml
[[canvases.nodes.exit_block.choices]]
text       = "Come down in what you slept in."
targetType = "node"
nodeId     = "rung_dean_morning.base"
flagEffects = [ { targetType = "player", flag = "dean_open", op = "set" } ]   # ← here
```

**It applies to choice conditions too, not only triggers.** Hit twice:

```
✗ dean_open          Required by: Dean (late)
                     set by 'Come down in what you slept in' but no location/schedule
✗ ray_arrangement    Required by: Ray
                     required by choice 'Sit with him after.',
                     set by 'Stop pretending it's a favour' but no location/schedule
```

Both were the same shape — a flag set in a triggerless rung's exit, then read to unlock
something. Both were fixed the same way: move the `flagEffects` up onto the located hub choice.

Flags that nothing reads in a trigger *or* a choice are unaffected — a triggerless rung may set
them freely.

**⚠️ MOVE the setter. Do not duplicate it.** Adding the `flagEffects` to the located hub choice
while *leaving* the copy on the triggerless rung fails exactly as if you had never moved it:

```
✗ cal_arrangement    Required by: Cal
                     required by choice 'Let him stay down here with you.',
                     set by 'Take him upstairs' but no location/schedule
```

`Take him upstairs` there is the *canvas name* of the triggerless loop, not the hub choice of
the same wording — the validator resolved the flag to the setter without a location and refused
the build, with the correct setter sitting right there on the hub. One setter, on the located
canvas, is the only arrangement that passes.

---

## 17. The wardrobe — and the most dangerous failure class in this engine

**Granting a garment** is `wardrobeEffects` on an exit block's **config**:

```toml
[canvases.nodes.exit_block.config]
destinationType = "specific"
locationId      = "her_room"
wardrobeEffects = [
  { action = "add", item_id = "mothers_slip" },
]
```

Exact path: `canvases[].nodes[].exit_block.config.wardrobeEffects`. Fields are **`action`** and
**`item_id`** — not `op` / `itemId`.

**⚠️ THE FAILURE CLASS: an unrecognised key is silently ignored.** I first wrote
`clothingEffects = [{ itemId = "…", op = "grant" }]`. The TOML parsed, the validator passed, the
build went green, and **nothing was ever granted** — the top of the wardrobe would have been
permanently unreachable with no error anywhere.

Nothing in the pipeline catches this. The only defence is to **grep the importer for any key you
have not personally seen in a shipped game** before relying on it:

```
grep -rn "yourKeyName" apps/projects/services/template_import.py
```

Zero hits means the key does not exist, however plausible it looks.

**The catalog** is a top-level `[[clothing]]` array — `id`, `name`, `slot`, `image`, `initial`,
`beauty`, `corruption`. Slots: `bra`, `underwear`, `top`, `bottom`, `dress`, `legwear`, `shoes`.

**`worn_corruption` is a MAX aggregate, not a sum.** Verified live: with `sleep_vest` (2) worn,
equipping `mothers_slip` (7) moved the reading **2 → 7**. One loaded garment sets the number on
its own, so a catalog does not need to be large to reach a tier — it needs one item per tier.

This makes clothing a genuine gate source. Verified condition types: `worn_corruption`,
`worn_type`, `clothing_slot` (empty/filled — i.e. "not wearing a bra"), and `clothing_item`
with `equipped` / `unequipped` / `owned` / `not_owned`.

---

## 18. Build

```
python3 scripts/merge_toml_phases.py games/<slug>
python3 manage.py package_from_toml \
    --file games/<slug>/toml_phases/7_final_game.toml \
    --output games/<slug>/output --gen-version v2 [--video-folder <dir>] [--debug]
```

⚠️ The flags are `--file` and `--output`, both **required and named**. This file previously
documented a positional path plus `--output-dir`; that form exits 2 with
`error: the following arguments are required: --file, --output` and builds nothing. `python`
may not exist on the path either — use `python3`.

`merge_toml_phases.py` concatenates a fixed set of phase files into `7_final_game.toml`.
**Never hand-edit `7_final_game.toml`** — it is output.

⚠️ `--video-folder` gates external-asset copying. Omit it and the build is green while every
portrait, location and scene image 404s in the browser.

---

## 19. ONE repeatable canvas per location + NPC + time window

Two repeatable canvases that bind the same NPC at the same location with overlapping schedules
are a build-time warning, and only one of them will ever render:

```
⚠️  Repeatable canvases 'hub_dean_late' and 'shift_change_frontroom' both trigger for NPC
    'npc_dean' at location 'the_front_room' with overlapping schedules. Only one repeatable
    canvas is allowed per location + NPC + time window. Put multiple interactions inside a
    single canvas as choices instead.
```

It does not stop the build. A canvas silently shadowed this way looks perfectly correct in the
TOML and is unreachable in play, so treat the warning as an error.

**The fix for THIS collision** — two canvases fighting over the same NPC in the same window — is
the engine's own advice: make the second canvas a triggerless rung and hang it off the existing
hub as a CHOICE. Conditions on a choice are evaluated live at render, so a rung can still be
time-limited and state-limited without owning a schedule of its own — see §20 for the predicate
that makes this worth doing.

⚠️ **THAT ADVICE IS SCOPED TO THIS COLLISION. IT IS NOT A GENERAL DESIGN PREFERENCE.** This
paragraph previously read *"and it is also the better design"* with no scope on it, and a game was
authored that took it as one: **23 choices on its front desk, 19 on its street**, one paragraph and
a wall of buttons at every location. The hubs in question **bound no NPC at all**, so §19 never
applied to them.

The rule is: *same NPC, same location, overlapping windows.* Two repeatable canvases at one
location that bind **different** NPCs, or **no** NPC, do not collide and **should be separate
canvases** — that is the normal shape, not a workaround. What lives on which screen is
`references/the-surfaces.md`, and a repeatable location-bound canvas caps at **8 choices** (gate 20).

---

## 20. `npc_at_location` — cross-room occupancy, and the any-NPC form

```toml
{ type = "npc_at_location", location_id = "the_front_room", npc_id = "npc_ray", operator = "is_present" }
{ type = "npc_at_location", location_id = "the_front_room", operator = "is_present" }   # ← any NPC
```

`generators/v2.py:4131-4145` (the runtime branch) and `:7791` (the human-readable dispatcher).
`operator` is `is_present` | `is_absent`; `location_id` accepts a slug or a UUID. **`npc_id` is
optional — omit it and the test becomes "is this room occupied by anybody".** 38 uses in
`games/vesper`.

Verified live in a built game, not just read: a choice carrying
`npc_at_location(the_front_room, npc_ray, is_present)` rendered at 23:10, when Ray's
20:00–23:30 row and Dean's 23:00–01:30 row overlap, and was gone at 23:45 with the same state
and the same player. This is the primitive that makes two-NPC scenes possible at all, since
`requires_npc` binds exactly one.

The any-NPC form has a second use: a scene about being *seen* without specifying who by. No NPC
is bound, so nothing can be mis-attributed — there is no character in scope to attribute to.

---

## 21. `clamp` is 0–100, it defaults to TRUE, and it will silently cap a CURRENCY

```js
v2.py:5753   if (clampFlag === undefined || clampFlag === null) { clampFlag = true; }
v2.py:5754   if (clampFlag) { next = window._traitClamp(next, 0, 100); }
```

Two facts, and the second one is the dangerous one:

1. **Omitting `clamp` means `clamp = true`.** The default is not "leave it alone".
2. **The clamp is a hard 0–100 on every trait, including one you are using as money.**

Found in a shipped game, by a live effect diff: a scene declared `money +120` and the state went
**0 → 100**. Every money grant in that game carried `clamp = true`, the weekly rent was **120**, and
the shop paid 30 a shift — so the player could work four shifts, hit the ceiling at 100, and **never
once be able to pay the rent.** The eviction branch was the only reachable outcome, and nothing
anywhere reported it: the TOML is valid, the build is green, all ten gates pass, and the sidebar
shows a plausible number.

**Rule: any trait that is a QUANTITY rather than a 0–100 meter must carry `clamp = false` on every
effect that writes it.** Money, counts, inventory-ish integers. Meters — nerve, exposure, corruption,
arousal, energy — want the clamp and should keep it.

⚠️ Note the asymmetry with a *deduction*: unclamped subtraction can go negative. The engine's own
recurring-demand system (`[settings.rent]`) does its own affordability check, but an authored
`op = "subtract"` on an unclamped trait does not — gate the choice on the trait instead.

**How to catch it:** diff the state across the scene and compare against the declared value. A
capped effect looks identical to a working one in the TOML, in the validator, in the build log and
on the scoreboard. Only the live number shows it.

---

## 22. Locations do more than `entry_from` — four fields nobody used

All verified 2026-08-12. A game shipped without any of these because the skill never said they
existed; the first is the mechanical answer to a premise that says *"ten minutes' walk away"*.

**Travel friction — a per-entry cost on a location.**

```toml
[[locations]]
id    = "the_shop"
costs = { time = 20, energy = 5 }     # time is minutes on the day clock; any other key is a trait
```

```
template_import.py:170    costs: Dict[str, int] = field(default_factory=dict)
template_import.py:1778   costs=_require_dict(l, "costs"),
v2.py:4681                // A location's per-entry cost lives in setup.locations[slug].entry_costs
v2.py:15276               has_location_costs = any(...)   # the travel-cost block is only emitted
                                                          # when some location declares costs
```

**This is what makes a schedule grid matter.** With free instant travel, "who is where at which
hour" is a lookup table. Charge twenty minutes each way and the player cannot be everywhere, so
presence becomes a constraint. Put the cost on **bridges between zones**, never on every room.

**Locked location — visible but blocked, with in-world prose on the card.**

```toml
entry_conditions = { version = "1.0", logic = "AND", items = [ ... ] }
blocked_message  = "The dining room's been dark since the staff went."
```

```
template_import.py:159-160   entry_conditions / blocked_message
template_import.py:1775-1776 parsed
v2.py:6590                   loc.properties["entry_conditions"] = l.entry_conditions
```

⚠️ `entry_conditions` needs `version = "1.0"` like any condition block, or it **fails open** and the
door silently unlocks (§4).

**`offscreen = true`** — a non-navigable "away" label. No nav card, no hub, and it is exempt from the
presence floor and reachability. Use it for a character who is genuinely elsewhere rather than
inventing a room for them. `template_import.py:154`.

**`is_container` + `default_entry`** — a pure navigation wrapper that holds no content.
`template_import.py:153`, `:3968`. A container **swallows** any canvas attached to it; attach to a
non-container hub instead.

---

## 23. The guidance page — `[[quest_cards]]`, and it is OFF by default in practice

The table is **`quest_cards`**, flat and top-level — **not** `[[quests]]`, which is an unrelated
table.

```
template_import.py:2456-2462   top-level key is `quest_cards` (flat, not nested under `quests`)
template_import.py:997         class QuestsCard
template_import.py:1068        parser for one [[quest_cards]] entry
v2.py:14711                    the V2 QuestsPage overlay is emitted only when
                               project.metadata["quests_engine"] == "v2"
```

⚠️ **The trap that shipped a game with an empty guidance page:** `quests_engine = "v2"` turns the
sidebar entry and the page **on**. Authoring no cards leaves a nav link to a heading with nothing
under it. Switching the engine on is not authoring guidance.

**Rendering.** `renderQuestsGoalBlock` (`v2.py:14964`) renders **exactly one** frame per card, in
order: ✓ terminal → 🔓 `ready_canvas` → 🎯 unmet goals. A card that matches none of the three returns
empty and the row goes blank.

⚠️ **A goal-less non-terminal card draws NO frame, and that is how a finished arc ends up looking
live.** It is not a blank *row* — the card still renders its `text` and `tip`, so it reads as an
objective with nothing ticked. Set `terminal = true` on the last card of every arc. `terminal_text`
overrides the ✓ label (default `Arc complete`) and exists because a finished arc and a finished
BUILD are different endings; it needs `terminal` set or the string is dead, and the validator warns.

```
template_import.py:1032-1039   terminal + terminal_text on QuestsCard
v2.py:14968-14976              Frame 1, terminal_text || "Arc complete"
```

⚠️ **Exactly ONE card per game may set `terminal_text`** — it is the badge form of the
build-boundary rule. A closed arc that is closed forever must not promise more of itself.

⚠️ **`pickQuestsCards` takes EXACTLY ONE scope string, and anything else fails silently.**

```
v2.py:14837   setup.pickQuestsCards = function(scope) {
v2.py:14838       if (scope !== "story_goals") return [];
```

A hard early return, no error, no warning. A typo in that string gives an **empty top section on the
guidance page** and no clue why. *(This paragraph originally described the function without
mentioning the guard — written from source, and it still missed the function's first line. Read the
whole function, not the part that answers your question.)*

**Selection.** `pickQuestsCards(scope)` (`v2.py:14837`) returns every matching top-tier card;
`pickQuestsCard(slug)` (`v2.py:14065`) returns the **single highest-`priority`** match for a
character — so a character's cards are a one-live-at-a-time chain.

⚠️ **Quest conditions use a SEPARATE evaluator with NO fail-open** — `checkQuestsCondition`,
`v2.py:14878`. **Never paste `version = "1.0"` onto a quest card.** That key is required on canvas
conditions and is wrong here.

⚠️ **The sidebar next-row calls the identical functions as the page** (`v2.py:15454-15456`). There is
no separate "sidebar quest": edit a card and both surfaces move together, and a character with no
card renders a blank next-row.

**`locked_text_threshold`** (`v2.py:12786`) prints an explicit *"Requires …"* hint on a locked
choice, distinct from `locked_text`, which replaces the label (§15).

---

## 24. Reading a built game from outside — four facts that each FAKE A BROKEN GAME

Before a playtest pass can assert anything, it has to read the build correctly. Every fact here has
been got wrong at least once in this project, and **each one produces a false alarm that looks
exactly like a real defect** — which is worse than not knowing, because it sends a session hunting a
bug that does not exist.

Two of the four were already known here and were logged in a `CHANGELOG.md` instead of this file. A
fresh session then lost time rediscovering both. **A changelog is a diary; nobody reads it before
starting work. If a fact is needed to do the job, it belongs in a reference file.**

### 24.1 `State`, `Engine` and `setup` hang off `window.SugarCube`

They are not bare globals from a browser console or an automation driver. Use
`SugarCube.State.variables`, `SugarCube.Engine.play(...)`, `SugarCube.setup`.

**The false alarm:** bare `State` throws *"State is not defined"*, every probe fails at once, and the
build reads as dead.

*(SugarCube 2's own runtime, not ours — so it carries no `v2.py` line. Verify in any built
`index.html`: search for `window.SugarCube=` and the `State:State`, `Engine:Engine` members inside
it.)*

### 24.2 `time_state.current_day` is a day NAME, not an index

```
v2.py:3273   const dayIndex = ["Monday","Tuesday",…].indexOf(timeState.current_day);
             also :3444 :3588 :3643 :3706
```

Set it to `0` and `indexOf` returns `-1` at every call site.

**The false alarm:** no schedule row matches, **every location reports nobody present**, and the
game reads as having a broken presence system. It does not. The harness set a number where a string
belongs.

### 24.3 Ask the engine who is present — do not recompute it

```
v2.py:4773    setup.getNpcsPresentAtLocation = function(locationId)
v2.py:19297   the engine's own nav badges call it
v2.py:19321   and again for the portrait row
```

**The false alarm:** hand-rolling presence from `[[npcs.schedules]]` gets overnight windows wrong —
a `22:00`–`04:00` row wraps midnight and a naive start ≤ now ≤ end comparison drops it — so a
correctly-scheduled character reads as absent.

### 24.4 The built page is ENTITY-ENCODED — macros are not stored literally

Measured on a real build: **663 occurrences of `&lt;&lt;set` against 3 literal `<<set`**, and 462
encoded `<<linkreplace>>`.

**The false alarm:** grep the page for `<<set` and find nothing, and conclude the game has no state
writes. This trap has now cost this project twice — once reading a built game, and once reading a
corpus of 18 shipped games, where it produced a confident and completely wrong measurement table.

**Always `html.unescape()` before matching macro syntax in built output.** Note this applies to the
*page*; the authored TOML is not encoded.

---

## Unverified — do not cite until read

Facts we believe but have not confirmed against source during this skill's construction.
Read and cite before using; delete from this list once promoted above.

- Adjacent `[group]` blocks merging into a single if/elseif chain (so a second ladder on one
  node is dead).
- `speaker = "unknown"` rendering a hardcoded label.
- The exact cooldown count for random events.
- Save-safety specifics: which identifiers orphan a live save when renamed.
