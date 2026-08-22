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

**A clip inside a cascade beat renders at that beat** (`v2.py:13952`) — nesting it there is not
merely allowed, it is the shape `register.md` S1 requires, because a cascade appends and the node
lead's clip stops being the current one after beat 0. See §8.

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

`max_triggers_per_day` is read per trigger (`v2.py:11017`).

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

### A node link SWAPS the screen. A cascade beat APPENDS to it.

The single most load-bearing fact about how content is composed, and neither half was written
down anywhere before 2026-08-18.

```python
v2.py:13258   target_passage = self.passage_name_map.get(str(node_id))   # BUILD-time resolution
v2.py:13952   body_html = self._convert_blocks_to_game_html(beat_blocks) # INSIDE <<linkreplace>>
```

- **`targetType = "node"` is resolved when the game is built**, into a static link to
  `Canvas_<uuid>_Node_<slug>`. Clicking it loads a new passage: the screen is **replaced**, and
  whatever media the new node carries renders fresh.
- **A cascade beat is a nested `<<linkreplace>>`.** Clicking it reveals the beat's blocks
  **below** what is already on screen. Nothing is removed — including the clip that rendered
  before it. A media block placed at the node lead therefore illustrates **beat 0 only**.

Two consequences worth carrying:

1. **Media placement is a composition decision, not decoration.** A repeatable act surface built
   as one cascade shows the player the same picture for the whole scene. Built as node routing,
   each act is its own screen with its own pool. `references/register.md` S1 ·
   `references/the-surfaces.md` R3b.
2. **A triggerless canvas is a SAFE node-link target, and an UNSAFE substitution target.** Build-
   time resolution needs no runtime lookup, so node routing into a canvas with no `trigger` works
   — it is how every sub-menu and every sex loop in this codebase is reached. A *substitution*
   target is different: `setup.getCanvasById` indexes only `help_data.locationCanvases`
   (`v2.py:3177`), which is populated only for canvases carrying `trigger.location`, so a
   triggerless substitution target silently never fires. **Same word "triggerless", opposite
   answer — do not carry one rule onto the other.**

The generator keeps an index specifically for this pattern:

```python
v2.py:3159   setup.sub_menu_parents   # child_canvas_id -> parent_menu_canvas_id, for triggerless
                                      # sub-menu canvases reached via cross-canvas targetType="node"
```

so the HUD can still render place and time from the parent hub even though the sub-menu canvas is
not in `locationCanvases` itself.

⚠️ **State inside a triggerless canvas must be TRAITS, not flags** — see §16. A flag whose only
setter is a canvas with no location has no located hint and the build hard-fails.

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
id = "<hub_id>"; entry_from = "<parent_id>"
navigation_order = ["<child_a>", "<child_b>", "<child_c>"]   # children ONLY

[[locations]]
id = "<child_a>";  entry_from = "<hub_id>";  navigation_order = []   # leaf, still exitable
```

*(Placeholders on purpose. This snippet used to show a landing with three bedrooms off it — the
first game's own upstairs — which teaches a floor plan while claiming to teach a field. `SKILL.md`:
an example outranks every rule beside it.)*

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
`references/the-surfaces.md`; a room's list is **needs + work + people** and its length falls out of
that closed set (R2), and **8 is a backstop, not a size** (gate 20 — never treat it as a target).

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
v2.py:5759   if (clampFlag === undefined || clampFlag === null) { clampFlag = true; }
v2.py:5760   if (clampFlag) { next = window._traitClamp(next, 0, 100); }   // :5761
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

⚠️ Note the asymmetry with a *deduction*: an unclamped one can go negative. The engine's own
recurring-demand system (`[settings.rent]`) does its own affordability check; an authored deduction
does not — gate the choice on the trait, or price it with `costs`, which the engine refuses when
unaffordable (`v2.py:4496` filters it out, `:4625` is the check — §27).

**How to catch it:** diff the state across the scene and compare against the declared value. A
capped effect looks identical to a working one in the TOML, in the validator, in the build log and
on the scoreboard. Only the live number shows it.

### ⚠️ 21b. `op = "subtract"` IS NOT AN ENGINE OP. It does nothing at all.

This section used to say *"an authored `op = "subtract"` on an unclamped trait"*, as though that
were a thing the engine ran. It is not, and the sentence taught two games to write 105 effects that
do nothing.

```js
// window.applyTraitEffect — v2.py:5749-5756
if (op === 'add')      { next = current + value; }
else if (op === 'set') { next = value; }
else { /* Unknown op; do nothing */ return; }
```

Nothing normalises it: the string `subtract` appears **nowhere** in `generators/v2.py` or in
`apps/projects/services/template_import.py`. The generator interpolates the op straight through
(`v2.py:13475`), so the build emits `applyAndNotifyTrait(..., "subtract", 4, ...)` verbatim and the
runtime drops it on the floor.

**Every effect family, and the ops each actually runs:**

| family | key that identifies it | ops the engine runs | source |
|---|---|---|---|
| trait | `trait` | `add` · `set` | `v2.py:5749-5756` |
| flag | `flag` | `set` · `unset` · `toggle` | `v2.py:5810-5825` |
| quest | `quest_id` | `start` · `update` · `complete` · `cancel` | `v2.py:5922-5925` |
| item | `action`, not `op` | `add` · `remove` | — |

**To take something away, write `op = "add"` with a NEGATIVE value.** Proven live on a shipped
build: `applyAndNotifyTrait('player',null,'count','subtract',4,true,null)` left `count` at 100;
`applyAndNotifyTrait('player',null,'stress','add',-5,false,null)` moved stress 20 → 15.

> **Measured cost. 35 dead effects in one v2 game, 70 in another, both authored from this file.**
> In the first, the counterweight meter its own spec called *"only ever falls"* never moved off its
> starting value for the entire game — twelve dead decrements against a clamp — twenty activities
> never charged the energy they said they cost, and the one NPC penalty in the game never applied.
> The TOML was valid, the build was green, all the ship gates passed, and a full live play-through
> passed too: **a number that never changes looks exactly like a number the player has not moved
> yet.** Two gates were reading it wrong as well — the sink/source counter classified by op NAME,
> so rewriting a deduction correctly flipped the line from 11:11 to 10:12.
>
> Now checked twice: `gates.py` **gate 25** fails any game using a dead op, and
> `template_import.py` refuses to build one.

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
v2.py:4687                // A location's per-entry cost lives in setup.locations[slug].entry_costs
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

**Rendering.** `renderQuestsGoalBlock` (`v2.py:14970`) renders **exactly one** frame per card, in
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
v2.py:14844       if (scope !== "story_goals") return [];
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

### The next STEP in the rail — `[[sidebar_items]] type = "quest_next"`

**A quest card has no `title` field** (`template_import.py:997-1039`) — `text` is the narrative body,
`tip` is the 💡 line, and the only short imperative string on a card is `goals[].label`. So there is
nothing on a card that a sidebar could show as a headline, and until 2026-08-16 there was no sidebar
item type for guidance at all: the only always-visible strings a game could put in the rail were
`trait_status_text` bands, which name a **state**, not a step.

> Measured: a game shipped with four band strings — *"Counter only, hatch down at midnight"*,
> *"Fleece zipped, back to the window"* — and an excellent Quests page. A player who never opened
> that page had **no place, no verb and no person** anywhere in the persistent chrome.

```toml
[[sidebar_items]]
type   = "quest_next"
max    = 3            # optional, default 3
npc_id = "npc_bev"    # optional — omitted, it takes the live TIER cards in file order
```

It renders `renderQuestsGoalBlock` — the same `🎯 To advance: ◯ <label> — 6 / 15` block as the page
and as `npc_panel`'s `next` row — so there is one implementation of what an objective looks like and
the three surfaces cannot drift. Terminal cards are skipped (no goals to show). Requires
`quests_engine = "v2"`, and the validator says so.

**The label is the whole UI.** `goals[].label` is what appears in the rail on every screen, so it
carries `the-voice.md` R3 in full: a place, a verb, and a window if the thing is schedule-gated.

⚠️ **Check the label is not circular.** Measured on a shipped game: all three cards of one ascent
tier named a choice gated at the exact value the card was trying to reach — *"Sell a token off the
book"* for `trade ≥ 15`, where the choice itself required `trade ≥ 15`. The two tiers beside it were
correct (each card named a choice gated **one tier below** its own goal), so the shape was known and
one ladder simply missed it. Nothing in `gates.py` catches this; read each card against the gate on
the choice it names.

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
- The exact cooldown count for random events.
- Save-safety specifics: which identifiers orphan a live save when renamed.

*(`speaker = "unknown"` was on this list. It has been read and promoted — see §25.)*

---

## 25. A speaking block with no `speaker` renders as a character called "Npc"

**Verified, and it is the largest defect ever found in a v2 game.** `dialog` and `thought_bubble`
both resolve their speaker the same way, and the field is **not optional**:

```python
speaker = props.get("speaker", "npc")        # v2.py:14631 — the default is a STRING, not a person
```

`"npc"` satisfies `speaker.startswith(("npc_", "npc"))`, so the unknown branch is skipped and the
NPC branch runs with `npc_id = "npc"` (`v2.py:14651`). Nothing matches, so the fallback title-cases
the id (`v2.py:14657`):

```python
npc_name = npc_id.replace("npc_", "").replace("_", " ").title() or "NPC"   # "npc".title() -> "Npc"
```

A portal-listed build rendered **`💭 Npc is thinking:` on 147 passages** — every thought bubble it
had. Measured afterwards across all three v2 games: **147, 145 and 79** blocks with no speaker.
Three for three, because this skill mentioned `thought_bubble` once and never showed its shape.

### The three forms, all required to carry `props`

```toml
{ type = "dialog",         props = { speaker = "player" },                        content = "…" }
{ type = "dialog",         props = { speaker = "npc", npcId = "npc_bev" },        content = "…" }
{ type = "thought_bubble", props = { speaker = "player" },                        content = "…" }
{ type = "thought_bubble", props = { speaker = "npc", npcId = "npc_bev" },        content = "…" }
{ type = "dialog",         props = { speaker = "unknown" },                       content = "…" }
```

`speaker = "unknown"` is the deliberate pre-introduction form: it renders **"Someone is thinking:"**
for a thought bubble (`v2.py:14647`) and the equivalent stranger label for dialogue. Use it while
the player cannot yet know the name — never as a shrug.

⚠️ **`dialog` is the correct type; `dialogue` is not.** The recognised list is `heading, paragraph,
dialog, thought_bubble, image, video, cascade, group, block_pool, clip` (`v2.py:14673`). A mistyped
type degrades to a bare `<p>` and silently drops the speaker.

⚠️ **A player thought must be written in the game's `narration_person`.** Of the 147 broken bubbles,
**62 referred to the protagonist as "she"** in a second-person game — so stamping
`speaker = "player"` on them would render *"💭 You are thinking: She has measured it now…"*. The
attribution and the prose have to agree.

**Gate 23 · speakers are named** checks the field is present. Whether the *right* name renders is a
different question and stays a lint (`lint_dialogue_attribution`).

---

## 26. `[settings.rent]` — the engine charges the money, so do not author a canvas that does

The recurring-demand system is real, it is wired end to end, and it **takes the money**. Read this
before writing a settle-up scene, because a game shipped one that narrated the handover and charged
nothing while this system was quietly doing the actual work three passages away.

```toml
[settings.rent]
enabled          = true
amount           = 245
due_day          = "Friday"          # weekday names only — VALID_DAYS, template_import.py:4786
collector_npc    = "npc_nunn"        # must exist in [[npcs]]
grace_periods    = 1
start_after_flag = "first_shift_done"
eviction_mode    = "flag_set"        # or "game_end" (the default, and a product that ends)
eviction_flag    = "terms_changed"
currency_symbol  = "$"               # added 2026-08-16; defaults to "$". It covers the
                                     # RENT PAGES ONLY — ten other money prints are
                                     # hardcoded "$" regardless. §33.

[settings.rent.text]                  # every beat of all three pages is authored here
title = "…" · scene = "…" · greeting = "…" · paid_scene = "…" · paid_response = "…"
paid_closing = "…" · cant_pay = "…" · warning_scene = "…" · warning_response = "…"
warning_closing = "…" · eviction_scene_soft = "…" · eviction_response_soft = "…"
eviction_closing_soft = "…"
```

**How it fires — and the timing is the part authors get wrong.**

1. `advanceDay()` sets `rent_state.is_due` when the day rolls over **to** `due_day` (`v2.py:5453-5464`).
   Days roll at midnight (`v2.py:5405-5408`), so the demand arms at **00:00 on the due day**, not at
   whatever hour the collector's schedule row says.
2. The next time the player lands on a `Location_*` passage or `Navigation`, they are intercepted
   into `RentDay` (`v2.py:15253-15262`). Never mid-canvas.
3. Paying runs `$player.core_traits.money -= _rent` and clears `is_due` (`v2.py:15931`). Verified
   live: 300 → 55 on a 245 demand.
4. Short pays route to `RentDay_Short`, which spends a grace period, and after that to the eviction
   branch — which under `eviction_mode = "flag_set"` sets a flag instead of ending the game.

**`start_after_flag` is what stops it being a scripted loss.** Until that flag is set the demand
never arms, so the flag belongs on the canvas that first gives her a way to earn.

> ⚠️ **DO NOT ALSO WRITE THE PAYMENT AS A CANVAS.** Measured failure: a game declared the settle-up
> as its central mechanic, ran `[settings.rent]` correctly, **and** authored a hub rung that
> narrated counting the money through a car window — with no cost, no money effect, no day gate and
> a relation grant, repeatable without limit. Played live it moved nothing and printed relation. The
> player meets two settle-ups, one of which is free, and the free one is the one with the writing in
> it. If the engine takes the money, the authored scene beside it must be about something else.

**Money must be unclamped for this to work at all.** A 245 demand against `clamp = true` money
(caps at 100) is unpayable and the only reachable outcome is eviction — see §21.

---

## 27. `costs` on a choice — the only price the engine enforces by itself

```toml
[[canvases.nodes.exit_block.choices]]
text  = "Buy soap and a candle. ($1)"
costs = [ { trait = "money", value = 1 } ]
```

Two things happen, and the second is why this is the strongest throttle available to a triggerless
rung:

1. **The engine refuses the choice when the player cannot afford it.** Every choice-collection path
   filters on `setup.checkCostsAffordable(c.costs)` (`v2.py:4496`, `:4527`, `:4975`; the function
   itself at `v2.py:4625`). An unaffordable rung does not render as a broken click — it is not
   offered.
2. **The deduction is applied by `setup.deductCostArray`, not by your effects list**
   (`v2.py:4655-4661`). A `costs` entry is parsed as `{trait, value}` only
   (`template_import.py:2133-2136`).

⚠️ **A `costs` deduction is HARD-CLAMPED to 0–100 and you cannot turn it off.**
`deductCostArray` passes `clampFlag = true` positionally into `applyAndNotifyTrait`, and there is no
`clamp` field on a `costs` entry to override it. Verified live: at `money = 150`, a 4-charge leaves
**100**, losing 46. Below 100 it is correct. This bites any game following §21's rule that money
grants carry `clamp = false` — the moment the balance exceeds 100, the next priced purchase
truncates it. `[settings.rent]` is unaffected; it subtracts directly (§26).

`costs` is the field to reach for when a repeatable rung needs a brake the player can *feel*. What
it is **not** is a way to model a trait requirement — a `costs` entry always spends. To require a
trait without spending it, use `conditions`.

---

## 28. `[engine.daily_tick]` — the day-rollover hook, and the only clean way to day-cap a triggerless rung

```toml
[engine.daily_tick]
flagEffects = [
  { targetType = "player", flag = "eggs_sold_today", op = "unset" },
]
traitEffects = [
  { targetType = "player", trait = "arousal", op = "add", value = 1, clamp = true },
]
```

Parsed at `template_import.py:2714-2769` (`TemplateDailyTick`), and both effect lists run when the
day rolls. `flagEffects` with `op = "unset"` is the mechanism behind every `_today` flag.

**Why it matters more than it looks.** `max_triggers_per_day` is read **off the trigger**
(`v2.py:11017`, `getattr(trigger, 'max_triggers_per_day', None)`). A triggerless rung — a canvas
reached by a hub choice, which is what most rungs in this architecture are — has no trigger, so it
cannot carry one. The pair that *does* work on a triggerless rung is:

- set a `_today` flag in the **hub choice's** `flagEffects`,
- gate that same choice on the flag being `is_false`,
- clear the flag here.

⚠️ **Do not use a hidden counter TRAIT for this.** It works, but it puts a player-subject trait into
the game whose only conditions are `lt` — which reads to `gates.py` gate 10 as a meter that closes
more than it opens. Use a flag; flags are not meters.

### 28.1 The flag goes on the CHOICE, because a choice and an exit run in opposite orders

```
choice     flagEffects -> costs -> modifiers -> … -> advanceTime   v2.py:12648-12733
node exit  advanceTime -> traitEffects -> flagEffects              v2.py:13085-13088 · :13049-13050
```

`advanceTime` rolls the day inside itself — `while (current_hour >= 24) { … advanceDay(); }`
(`v2.py:5411-5414`) — and `advanceDay` is where this hook clears the flags (`v2.py:5552`).

So on a rung whose `time_progression_minutes` crosses midnight:

| where the flag is set | what happens |
|---|---|
| **the choice** | set on the old day, then cleared by the tick → the new day is open. **Correct.** |
| **the rung's exit** | tick clears first, flag is written second → **the new day starts already capped.** |

> ⚠️ **This paragraph said the opposite until 2026-08-22.** It warned that a midnight-crossing rung
> gets its cap *cleared* and becomes re-clickable. The emit order makes that impossible, and the
> real failure is the reverse: the rung is **locked out of the following day**, silently. Measured
> in `off_season`, whose sleep rung ran 21:00→06:00 and set `slept_today` on the exit — after night
> one, Sleep was never offered before midnight again. The build, the flag-chain validator and the
> scoreboard were all green throughout.

⚠️ **A LOCATED canvas does not need the flag at all.** `max_triggers_per_day` is read off the
trigger (`v2.py:11017`) and `markCanvasTriggered` stamps its day key **before** `advanceTime` runs
(`v2.py:4290`), so it has none of this problem. The flag pattern exists for *triggerless* rungs.

### 28.2 Two of the three parts validates and does nothing

A flag read as `is_false` and cleared here, with **no canvas setting it**, is a cap that never
closes. Nothing in the toolchain objects: the generator's flag-chain validator only reports a
never-set flag when a condition requires it `is_true` (`v2.py:11659`) — deliberately, since an
`is_false` read is a re-entry guard rather than a prerequisite — so the gate simply fails open.

Measured: `off_season` shipped four `*_talk_today` caps with the read and the clear and no set, and
its four talk screens were re-clickable every twenty minutes, out-earning the day-capped rungs they
sat below. `scripts/gates.py` gate **`a day-cap closes`** exists for exactly this.

### 28.3 What the screen looks like once the cap IS spent

§28.2 asks whether the cap closes. This asks what the player sees the moment it has, which is every
day, by design.

**A choice whose conditions fail renders NOTHING.** It is wrapped in
`<<if setup.triggerConditionsSatisfied(…)>>` (`v2.py:12806`) — no greyed line, no reason, no hours,
unless the choice opts in with `show_when_locked` (`v2.py:13016`). Absent that, a spent rung leaves
no trace on the screen it used to be on.

**A cost-bearing choice counts as conditional too.** The engine's own test for whether a node has a
usable exit is `has_unconditional_choice`, and a choice registers as unconditional only when it
carries **neither** `conditions` **nor** `costs` (`v2.py:12827-12836`). So a screen whose one
affordance is *"Put it in the slot ($3, 5m)."* is exactly as empty to a player at $0 as a spent hub
is to a player who has had their go.

**When nothing passes, the engine does three things** (`v2.py:13113-13175`):

| | |
|---|---|
| `console.warn` | always, in every build — canvas slug, every choice's conditions, and a live state snapshot |
| a diagnostic banner | `$flags.debug_mode` only. Re-evaluates each predicate and prints ✓/✗ per item |
| `[[Continue->…]]` | player-facing escape to the trigger location (`_get_return_location`, `v2.py:12545`). **Fires no effects** |

That Continue link is a safety net, not an exit. The visit banks nothing, the label is the engine's
word rather than the author's, and the player cannot distinguish a spent day from a broken build.
**Author the door instead** — `the-surfaces.md` R7, gated by `a spent day still has a door`.

⚠️ **The incumbent skill's advice on this is scoped, and the scope matters.**
`author-game/references/engine-reference.md:297` says you should *not* add an unconditional fallback
"just in case", because it double-renders whenever a real choice passes. **True for conditional
ROUTING** — mutually exclusive branches with a catch-all, where exactly one always passes, and the
unauthored generations degrade to a free escape rather than a lock. **False for a day-capped or
priced screen**, where the gates are independent budgets that deplete together and all-false is the
guaranteed end of every day. Read that paragraph as being about routers.

⚠️ **Returning to the location does not re-fire the hub.** A repeatable canvas carrying `npcId`
renders as a clickable portrait on the location screen (`renderNpcPortraits`, `v2.py:4919`), not as
an auto-fire, so a leave-link pointed at the node's own location lands the player back in the room
with the portrait still on it. No loop.

---

## 29. `cap` on an effect — a VALUE ceiling, not a rate limit

```js
// v2.py:5763-5769, inside applyAndNotifyTrait, AFTER the clamp
if (cap !== undefined && cap !== null) {
  var capNum = Number(cap);
  if (!isNaN(capNum)) {
    if (next > capNum) next = Math.max(current, capNum);
  }
}
```

`cap` is the **7th positional argument** to
`setup.applyAndNotifyTrait(targetType, npcId, trait, op, val, clampFlag, cap)` (`v2.py:5858`).
Authored as a sibling of `op`/`value` on any effect and passed straight through
(`v2.py:13464`, `:13472`, `:9813`):

```toml
effects = [ { targetType = "player", trait = "energy", op = "add", value = 40, cap = 100 } ]
```

Read the `Math.max(current, capNum)` carefully: **a cap never pulls a value down.** If the trait is
already above the cap it is left alone; the cap only refuses to *raise* it past the ceiling. So:

| use | correct? |
|---|---|
| bounding a **restore** — a sleep rung that adds energy, a wash that adds hygiene | ✅ this is what it is for |
| bounding a repeatable **relation** or reputation grant so one rung cannot max a character | ✅ |
| bounding an **ascent tier** | ❌ the tier must be able to reach its top band; a cap there deletes content |
| **throttling how fast** anything rises | ❌ it does not touch the rate. See `the-meters.md` |

`cap` and `clamp` are independent and both apply — clamp first, then cap.

---

## 30. A banded sidebar item and the auto Traits dump both render — unless you hide the key

The sidebar prints **two** things about a trait, from two different places:

1. **The auto Traits dump** — every declared `core_trait`, as a bare number.
2. **Whatever `[[sidebar_items]]` you authored** — `trait_status_text` (`v2.py:16251`),
   `trait_words` (`v2.py:16314`), `trait_bar`.

They do not know about each other. Band a trait without suppressing its number and the player reads
*"Nothing under it"* and `cover 55` stacked on top of each other.

**The suppression is `[[traits.labels]] hidden = true`.** The generator collects those keys
(`v2.py:1220-1226`), emits them as `setup.hiddenTraits` (`v2.py:3156`), and the dump skips them
(`v2.py:15557`, `:15604`).

```toml
[[sidebar_items]]
type  = "trait_status_text"
trait = "cover"
bands = [ { min = 0, max = 14, text = "Long dress, hair pinned" }, { min = 15, text = "Apron off" } ]

[[traits.labels]]
key    = "cover"          # ← REQUIRED, or the number prints underneath the words
hidden = true
```

⚠️ **A trait absent from `[[traits.labels]]` entirely is NOT hidden** — it still appears in the
dump. Measured: a shipped game banded all four of its meters in `[[sidebar_items]]`, declared none
of them in `[[traits.labels]]`, and printed every one twice.

⚠️ **The other half: a banded value that lands outside every band renders NOTHING** — the whole card
disappears, which reads as a missing HUD element rather than a wrong number, so a quick playtest
sails past it. `trait_status_text` treats an omitted `min`/`max` as open-ended (`v2.py:16266`,
defaults ∓1e9); `trait_words` needs a **closed** `[min, max]` to match (`v2.py:16335-16336`). Leave
the top band's `max` off, or `cap` the terminal add (§29).

---

## 31. `requires_npc` does NOT gate an auto-firing canvas

**The field is real and it works — on two paths out of three.** A canvas that AUTO-FIRES on
entry never consults it, so a one-shot written as "fires where the character is" fires whether
they are there or not.

```
setup.getStoryCanvasRedirect            v2.py:4921   ← entry-time auto-fire
  -> setup.selectAutoFireCanvasForLocation   v2.py:4453
       filters: isRepeatable · triggerMode=="random" · substitutionOnly · isCanvasValid · priority
  -> setup.isCanvasValid                     v2.py:4573
       checks: hasSchedules/scheduleParams · conditions · canTriggerCanvas
       requiresNpc is NOT among them.
```

`requiresNpc` is emitted into `help_data.locationCanvases` at `v2.py:11104` and consumed in
exactly two places:

```
v2.py:5253-5268   the RANDOM-ENCOUNTER selector — "Phase A (2026-05-14) — NPC presence gate.
                  Canvases without requiresNpc are unaffected."   ← works as documented
v2.py:5332-5335   substitution rules — same check on the substitution TARGET
```

Neither is the auto-fire path. **Consequence in a shipped game:** `vesper/cap_renner_hired` is
bound to `the_anchor` with `requires_npc = "npc_renner"`, and Renner's schedule puts him there
19:00–23:00. With `opening_done`, `renner_hired is_false` and the cover equipped, the canvas
auto-fires the moment the player walks in — so a scene that introduces him can play in an empty
bar at ten in the morning.

**What to do instead:** put a `[[canvases.trigger.schedules]]` row on the meeting that matches the
character's own schedule row, or gate it on a flag the player can only hold by having been where
they are. Keep `requires_npc` as well — it is free, correct on the paths that read it, and it
documents intent — but it is not the thing stopping the canvas.

Portrait rendering is the mirror image and behaves as documented: `selectNpcPortraitCanvasesForLocation`
skips every non-repeatable canvas outright (`v2.py:4482-4487`, `if (!c.isRepeatable) continue`), so a
first-contact one-shot can never leak onto a location screen as a face.

`references/the-first-hour.md` F5.

---

## 32. The clock advances by MINUTES only — and the label tag is asymmetric

Three facts about time, and each one has been assumed the other way at least once.

### 32.1 There is no absolute-time advance

```
grep -E 'target_hour|advance_to|until_time|time_target' v2.py     0 hits
```

*(`setTime` matches in this file, but all eight hits are `setTimeout` — a DOM timer for a
notification fade or a deferred `Engine.play`, not a clock setter. Grep for the word, not the
prefix.)*

`window.advanceTime(minutes)` (`v2.py:5400`) adds minutes to `time_state.current_minute`, rolls the
hour past 60 and the day past 24, expires temporary modifiers, and repaints the sidebar. That is the
whole time API. **Nothing in this engine can send the clock to a named hour**, so a label or a beat
promising one ("work till one", "back by six") is a promise the engine cannot keep.

`window.waitTime(minutes)` (`v2.py:5442`) is the sidebar wait buttons' entry point — the same
advance, plus `setup.commitMoment()`, because a wait navigates nowhere and would otherwise live only
in the active moment.

An exit that declares no `time_progression_minutes` still costs **3 minutes**
(`v2.py:13200`, `config.get('default_time_progression', 3)`; the exception fallback at `:13388` emits
the same `advanceTime(3)`). A four-node opening has therefore drifted 9 minutes before the first real
choice.

There is no `@time` token either — `_resolve_at_references` (`v2.py:14027`) resolves `@player` and
`@<npc>` and returns everything else untouched. The clock can be *shown* (`<<timeDisplay>>` at the
top of `StoryCaption`, `v2.py:15663`/`:15679`, rendering `<<timeFormatted>>` at `v2.py:16043`) but it
cannot be *printed into prose* by any authored token.

### 32.2 Travel time is tagged on the card; activity time is tagged nowhere

| what | tagged? | where |
|---|---|---|
| `[[locations.costs]] time` | **yes, automatically** — renders `20m` on the nav card | `getLocationCostTag` `v2.py:4724`, used at `:19353` / `:19370` |
| a choice's `time_progression_minutes` | **no** — emits a bare `<<script>>advanceTime(150);<</script>>` at the bottom of the passage body | `v2.py:12733` |
| a trait `costs` entry | yes, when unaffordable | `getCostBlockedMessage` `v2.py:4670` |

So a door announces its twenty minutes and a two-and-a-half-hour shift announces nothing. If the
duration is to appear, the author puts it in the label. `references/the-clock.md` C4.

### 32.3 `show_when_blocked` — the only out-of-hours surface, and nothing uses it

A solo activity whose schedule window has closed is dropped from the location list entirely, unless
the author opts in:

```toml
[canvases.trigger.metadata]
show_when_blocked = true
cooldown_message  = "Counter work — mornings, eight till one."
```

Read at `v2.py:11055-11059`, emitted as `showWhenBlocked` / `cooldownMessage` (`v2.py:11100-11101`).
`renderSoloActivities` checks `isCanvasValid` (`v2.py:5091`) — which returns false on a **schedule
miss** before anything else (`v2.py:4573-4580`) — and, when the flag is set, pushes the canvas onto
`soloCooldownBlocked` instead of dropping it, rendering a dimmed non-clickable line carrying the
message (`v2.py:5140-5145`). The same path also catches `max_triggers_per_day` exhaustion
(`v2.py:5098-5102`).

⚠️ **Zero of the ten games in this repo set it.** Windowed work simply vanishes, and the player has
no surface that says when to come back. The `SchedulePage` (`v2.py:18964`) publishes hours for
**people** — every declared `[[npcs.schedules]]` row as a Time / Location / Activity / Days table —
and there is no equivalent for places or activities. `references/the-clock.md` C5.

---

## 33. Money on the screen — where the engine prints it, and in what notation

The generator prints a money figure at **sixteen sites**. `[settings.rent] currency_symbol`
governs **four**. Nine hardcode `$`; three print no notation at all. This is why a game that never
declares a symbol still ends up with more than one, and why declaring a symbol other than `$` does
not give you one either.

### 33.1 The census

| notation | where | `v2.py` |
|---|---|---|
| **honours `currency_symbol`** | `RentDay` — the collector's default greeting | `:15922` |
| | `RentDay` — *"You have X. Rent is Y."* (2 prints) | `:15926` |
| | `RentDay` — the `Pay $N rent` button | `:15929` |
| | `RentDay_Paid` — remaining money | `:15968` |
| **hardcodes `"$"`** | `RentDay_Short` — *"You have: … You need: …"* (2 prints) | `:16000` |
| | the clothing shop — balance | `:2018` |
| | the clothing shop — item prices (3 prints) | `:2075` `:2078` `:2081` |
| | the phone job board — a job's income | `:2926` |
| | the phone bank — balance, and cash | `:2960` `:2961` |
| | the bank-interest notification | `:5618` |
| **no notation at all** | an unaffordable choice — *"Requires 3 Money (you have 1)"* | `:4680` |
| | a location's nav cost tag — *"30m · 3 Money"* | `:4731` |
| | the sidebar `trait_bar` — *"money: 12 / 100"* | `:16241` |

`self.rent_currency_symbol = rent_settings.get("currency_symbol", "$") or "$"` — `v2.py:1190`.
Emitted to the runtime only when rent is enabled (`v2.py:3123`), so a game without
`[settings.rent]` has no symbol setting at all.

⚠️ **`RentDay_Short` is the one every rent game reaches.** It is the branch taken when the player
cannot pay — the screen where the number matters most — and it does not even set `_cur`.
`games/forty_miles` declares `currency_symbol = "£"`, and its released build ships
`You have: <strong>$<<print $player.core_traits.money>></strong>`. The author's own comment on that
line reads *"the pages hardcoded `$` before this key existed"*; the key did not finish the job.

### 33.2 The symbol is a prefix

Every honouring site concatenates symbol-then-number — `"Pay " + _cur + _rent + " rent"`
(`v2.py:15929`), `<<print _cur>><<print _money>>` (`v2.py:15926`). There is no suffix form and no
format string. An invented unit that reads after the number (`10 coin`, `1000 caps`) cannot be
expressed through `currency_symbol`.

### 33.3 The sidebar ignores `[[traits.labels]]`

```
<<set _traitLabel to _item.label || _tbKey>>     v2.py:16215
<<print _traitLabel>>: <<print Math.floor(_traitVal)>> / <<print _traitMax>>   v2.py:16241
```

A `trait_bar` takes its label from **the sidebar item's own `label` key**, falling back to the raw
trait key. `setup.trait_labels` is read only by `_labelForTrait` (`v2.py:6781`), which formats
*condition* text — hint lines and blocked-choice reasons. So
`[[traits.labels]] key = "money", label = "Change bag"` does **not** rename the sidebar readout.

And `_traitMax` defaults to 100 (`v2.py:16214`), so an uncapped counter renders as a fraction of a
maximum it does not have: a money trait with no `max` prints **`money: 12 / 100`** over a 12% fill
bar. Set `label`, and set `max` to something the currency will not exceed, or use
`trait_status_text`.

### 33.4 A choice's price is never rendered when the player can afford it

An affordable choice renders its authored label and nothing else (`v2.py:12597` only wraps it in an
`<<if>>`). The engine speaks a price **only on the failure path** — `getCostBlockedMessage`
(`v2.py:4680`) emitted into `<span class="locked-choice">` at `v2.py:12747`:

```
affordable      Feed the meter ($3)                        exactly what the author typed
unaffordable    Feed the meter ($3) (Requires 3 Money (you have 1))
```

This is the same asymmetry as §32.2 for time: the engine tags the cost it stops you paying and
stays silent about the one it takes. So the visible price is authored prose in every normal case —
gate 21 exists because of this, and `the-economy.md` R7 governs its notation.

### 33.5 `[[traits.labels]] unit` is dead

The importer reads it (`template_import.py:2885`) and stores it in project metadata (`:6310`). No
generator reads it back — a grep of `v2.py` for `unit` returns nothing. It is not a lever for
pluralising a currency.
