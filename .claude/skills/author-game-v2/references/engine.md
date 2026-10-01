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
v2.py:12665   "is_repeatable": trigger.is_repeatable if trigger else True
v2.py:12738   is_repeatable = getattr(trigger, 'is_repeatable', True) if trigger else True
apps/stories/models.py:355   is_repeatable = models.BooleanField(default=True, ...)
```

**Why it matters for design:** a canvas with no `is_repeatable` key is standing content, not a
one-shot. Assuming otherwise inverts your read of what the game actually is.

---

## 2. Conditions **fail open** without `version = "1.0"`

```js
v2.py:4336   if (!conditions.version || conditions.version !== '1.0') return true;
```

**Why it matters:** at runtime a gate missing its `version` passes for everybody. Every
`conditions` block you author carries `version = "1.0"`.

**The importer now rejects bad conditions (E1, 2026-10-01).** One table,
`CONDITION_SCHEMA` (`template_import.py:1578`), lists each condition type's allowed keys and
operators; one walker, `_walk_condition_carriers` (`template_import.py:1661`, run from
`normalize`, `:2069`), checks every v1.0 block in the raw TOML by key name (`conditions`,
`entry_conditions`, `match_condition`, `show_when`, and a schedule row's `when`). A missing
version, an unknown block key or `logic`, or an unknown type, key or operator fails the build.
Quest cards and `player_portrait` outfit `when` keep their own schemas and are not walked. A new
evaluator branch needs its row in the table, or every game using it fails to import.

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
v2.py:13978   def _resolve_pool_dir(self, pool_dir)     # contents discovered from disk
v2.py:13992   def _media_pool_key(...)                  # cycle state key
v2.py:14151   # ... $game_state.media_cycle
v2.py:13964-13966  # `pool_dir` is preferred: the count is never hardcoded, so the human curates
```

Pools **cycle** (1→2→3→1) through `$game_state.media_cycle` rather than re-rolling, so the
player never sees the same clip twice running. `pool_dir` is preferred over an explicit file
list because the count comes from disk.

Media blocks also appear nested — under group blocks (`blocks[].blocks[].props`) and inside
cascade beats (`blocks[].props.beats[].blocks[].props`). Any tool walking media must recurse.

**A clip inside a cascade beat renders at that beat** (`v2.py:16086`, inside `_render_cascade_tail` at `:16026`) — nesting it there is not
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

Call sites: `v2.py:3807`, `:3825`, `:3983`. An omitted `end_time` defaults to start + 60 min
(same function).

⚠️ An older note in our own memory claims a window cannot cross midnight and needs two rows.
The source above contradicts it. Either the engine was fixed or the original observation was
about a different path — **verify live before splitting a window.**

---

## 7. Random events have a per-location cooldown

```js
v2.py:5935   var cooldowns = sv.game_state.random_cooldowns = sv.game_state.random_cooldowns || {};
             // after a random event fires, skip N visits before rolling again
```

Cooldown is engine-managed per location — do not author your own. Random canvases are
selected by `triggerMode === "random"`.

`max_triggers_per_day` is read per trigger (`v2.py:12739`).

---

## 8. Linking between canvases

```toml
[[canvases.nodes.exit_block.choices]]
text = "…"; targetType = "node"; nodeId = "<canvas_id>.<node_id>"
```

A canvas with **no** `trigger` block is a link target — it has no location of its own and
inherits its context from whatever links into it. Substitutions use
`trigger.substitutions[].target_canvas_id`.

⚠️ **A triggerless canvas that nothing links to is DELETED from the build, silently.** The seed set
is canvases carrying `trigger.location_id` (`v2.py:423-427`, the no-DB graph path; `:450-454`, the
ORM path). Everything else has to be pulled into the closure by a `targetType = "node"` choice or a
substitution target — `_compute_included_canvases` (`v2.py:567`, the primary and sole entry
point) and its no-DB twin `_compute_included_canvases_graph` (`:645`). A canvas in neither set
never becomes a passage: it costs nothing at compile time, the validator is silent, and every gate
in `gates.py` stays green over it, because gates parse the source and reachability is decided by the
generator. **Write the link in the same edit as the canvas.**

A mistyped `targetType` or a missing link drops a fully written canvas this way with every gate
green. `gates.py --release` checks every canvas against the built HTML for exactly this.
`defects/001-no-reachability-gate.md`.

`show_when_locked = true` on a choice renders it greyed and visible instead of hidden. This is
the mechanism behind "every release ends on a visible locked door."

### A node link SWAPS the screen. A cascade beat APPENDS to it.

The single most load-bearing fact about how content is composed.

```python
v2.py:15386   target_passage = self.passage_name_map.get(str(node_id))   # BUILD-time resolution
v2.py:16086   body_html = self._convert_blocks_to_game_html(beat_blocks) # INSIDE <<linkreplace>>
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
   (`v2.py:3506-3520`), which is populated only for canvases carrying `trigger.location`, so a
   triggerless substitution target silently never fires. **Same word "triggerless", opposite
   answer — do not carry one rule onto the other.**

The generator keeps an index specifically for this pattern:

```python
v2.py:3493   setup.sub_menu_parents   # child_canvas_id -> parent_menu_canvas_id, for triggerless
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
is unavoidably multi-line. Write it as sections:

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

## 15. A pure number lock prints its own need; a story lock needs `locked_text`, which REPLACES the label

A choice with `show_when_locked = true` renders as `<span class="locked-choice">`. If
`locked_text` is set, that string is shown **instead of** the action text — the player never
sees what the action was called.

**Omit it on a story lock and the row is the action label, greyed, with nothing beside it.**
`escaped_locked = (locked_text or choice_text)` at `v2.py:14854`, and the same string is repeated
into the `title` tooltip at `:14839-14840`. The player sees "Kiss him" struck out and learns neither
why nor when. A number leg gets the engine's suffix; a flag leg gets nothing.

**A pure number lock needs nothing** *(LO decided, D2)*. When every item is a trait gate the engine
can number — hers or a man's, `gte`/`gt`/`lte`/`lt`, value 2 or more (`_wants_number`, `v2.py:14901`) —
it appends the need and her value beside the label (`setup.requirementSuffix`, `v2.py:4325`). A
`locked_text` there says it twice (J1): drop it. **Any other lock is a story lock** — a flag, a clock or
day item, clothing, an `eq`, a value of 1 — and so is a **mixed** lock: the suffix names only the unmet
number legs, never the flag, so without a line the button goes silent when only the flag blocks. A story
lock gets a short `locked_text` (for a mixed lock, the story part) and is never "doubled".

Measured across 26 shipped sandboxes (`findings_B_refusal.md`, section B):

- A refusal is **either invisible or it speaks**. Of 16,167 refusing conditionals, **71% render
  nothing at all** and **28% put a short line where the action was** — median **9 words**, and
  **60% of those name a handle** (a price 37%, "already done" 18%, a time 5%, a place 2%).
- A **visible, mute action label is 2.26%** of 4,513 spoken refusals, and nearly all of that is
  settings and pagination chrome — `OptionsWidget` toggle states, `Widgets Outfits`
  "Previous"/"Next" greyed at the ends — rather than gated content.

Gate: **"a locked door says why"** (`gates.py`, `the-surfaces.md` R5c). It fails `locked_text` on a pure
number lock; a story lock needs `locked_text`,
`locked_text_threshold` (§23 — the label becomes a clickable toast, `v2.py:14915-14922`) or
`rejection_node` (§36). A choice gated only by `costs` is never counted against you — see §27.

### ⚠️ That is what a shown row must SAY. It is not how many rows to show.

The rule above answers half a question: what a shown row says, not when to show one.

**The field's default is silence** (`findings_B_refusal.md` §2, 16,167 refusing chains): **71%
render nothing at all**, and the per-game silent share runs a **median of 79%** across a **22–100%**
range. The study's own reading: *"The spread is a house decision, not a genre norm"* —
zaras-school-life speaks 78% of its refusals, corpo-life speaks two of 574, and both shipped. So
there is no number to hit. There are two calls to make:

**1 · Never inside a scene when the scene moves the bar.** A greyed rung mid-beat, gated on a meter
the canvas's own `effects` raise, is the machinery narrating its own progress bar: the row opens by
itself in a click or two, so the text hands the player nothing to act on, and it puts a UI label in
the one place the register says the body is the only thing on screen. Contrast an in-scene locked
choice gated on something the player goes **elsewhere** and fixes. That is a handle and it is
correctly spoken.

**2 · A blocked WINDOW is a different surface and it is not this one.** An activity out of hours
belongs in `show_when_blocked` + `cooldown_message` on the canvas trigger — `the-clock.md` C5, where
the hours are the point and hiding them is *"lostness with a clock on it"*. Do not answer a noisy
guidance screen by deleting those.

`scripts/gates.py`'s **`lint · which refusals are shown at all`** reports three numbers: the
in-scene count, the self-moved subset, and the shown-locked reasons' median length against the
field's spoken-refusal median of 9 words (gates.py:1114).

---

## 16. A flag read by a TRIGGER **or a CHOICE** must be set from a LOCATED canvas

The flag-chain validator **hard-fails the build** otherwise:

```
❌ Flag Chain Validation Failed:
   ✗ tom_open
     Required by: Tom (late)
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
nodeId     = "rung_tom_morning.base"
flagEffects = [ { targetType = "player", flag = "tom_open", op = "set" } ]   # ← here
```

**It applies to choice conditions too, not only triggers.** Hit twice:

```
✗ tom_open           Required by: Tom (late)
                     set by 'Come down in what you slept in' but no location/schedule
✗ mark_arrangement   Required by: Mark
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
  { action = "add", item_id = "silk_slip" },
]
```

Exact path: `canvases[].nodes[].exit_block.config.wardrobeEffects`. Fields are **`action`** and
**`item_id`** — not `op` / `itemId`. `action` is `add` (into the wardrobe) or `equip` (added and put on:
`setup.addToWardrobe` + `setup.equipItem`, `_get_wardrobe_effects_for_node`, `v2.py:15639`).

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
`conditions`, `price`, `beauty`, `corruption`, `type` (`template_import.py:282-294`). Slots: `bra`,
`underwear`, `top`, `bottom`, `dress`, `legwear`, `shoes`.

**`worn_corruption` is a MAX aggregate, not a sum.** Verified live: with `sleep_vest` (2) worn,
equipping `silk_slip` (7) moved the reading **2 → 7**. One loaded garment sets the number on
its own, so a catalog does not need to be large to reach a tier — it needs one item per tier.
**`worn_beauty` is the same fold over `beauty`** (`template_import.py:290`, `v2.py:4579`).

### The three ways a wardrobe gets read

A garment nothing reads is not a garment (`the-meters.md` W3), and **gate · the wardrobe is read**
enforces it. All three of these families satisfy it, and the second is the one authors forget:

**1 · A condition predicate.** `worn_corruption`, `worn_beauty`, `worn_type`, `worn_exposure`,
`clothing_slot` (empty/filled — i.e. "not wearing a bra"), and `clothing_item` with `equipped` /
`unequipped` / `owned` / `not_owned`. This is the gate family.

> **`worn_exposure` is the only one of these that reads an EMPTY slot**, and it is the newest
> (2026-08-28). A derived 0/1/2 — 0 covered, 1 underwear-level, 2 bare — from
> `setup.getWornExposure` (`v2.py:1751`); the predicate is at `v2.py:4555` and its lock text at
> `:8558`; a garment declares its own `exposure` via `template_import.py:2942`. ⚠️ **The other two
> aggregates cannot see nakedness at all**: `worn_corruption` and `worn_beauty` are both
> `getWornStatMax` (`v2.py:1721-1722`), which skips a slot with nothing in it, so naked and plainly
> dressed return the same value. Use `worn_exposure` for how much is showing and the older pair for
> how the outfit reads. `the-meters.md` W7 is why this matters: the field's body system is one
> derived number the whole world tests.

**2 · A `player_portrait` outfit override.** `when = { worn_type?, corruption?, flag? }`, first match
wins (`template_import.py:922-924`). Only `worn_type` and `corruption` are wardrobe reads; a `flag`
override is not. **This is a display reader, not a gate, and `the-meters.md` W7 is what says that is
the field's normal case**.

**3 · A location dress code.** `clothing_rules.slots_required` on a location
(`template_import.py:4928-4942`), optionally with its own `conditions` and a refusal `message`.

`setup.validateClothing` (`v2.py:1981`) words its warnings with `$player.name` ("Player" if unset;
E1b, 2026-10-01, was a hard-coded "Emma"). Nothing in the engine or any game calls it today.

### One thing the wardrobe cannot do, recorded deliberately

**A worn stat can gate a choice and can explain itself when it blocks one, but it cannot be shown as
a standing state.** `v2.py:8609-8618` renders the lock text — `"Outfit must be revealing
(corruption ≥ 4)"`, `"Appearance ≥ 7"` — which the player meets only at the moment of refusal.
`trait_status_text` (§30) takes a `trait`, and these are derived condition types rather than traits,
so they cannot be given a sidebar band.

**This is not a gap to close with a status row.** The field does not show the number either. It
shows the world reacting — `degrees-of-lewdity` reads its derived `$exposed` about 900 times and 82%
of those reads only change words. Write the reactions, not the readout.

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
⚠️  Repeatable canvases 'hub_tom_late' and 'shift_change_frontroom' both trigger for NPC
    'npc_tom' at location 'the_front_room' with overlapping schedules. Only one repeatable
    canvas is allowed per location + NPC + time window. Put multiple interactions inside a
    single canvas as choices instead.
```

It does not stop the build, and it is a note, not an error: the highest `priority` wins (§42, "One
location shows ONE canvas per character"). A canvas shadowed this way is unreachable while the other's
conditions hold, so set the priorities on purpose.

**The fix for THIS collision** — two canvases fighting over the same NPC in the same window — is
the engine's own advice: make the second canvas a triggerless rung and hang it off the existing
hub as a CHOICE. Conditions on a choice are evaluated live at render, so a rung can still be
time-limited and state-limited without owning a schedule of its own — see §20 for the predicate
that makes this worth doing.

⚠️ **THAT ADVICE IS SCOPED TO THIS COLLISION. IT IS NOT A GENERAL DESIGN PREFERENCE.** Read as
one, it turns every location into one paragraph and a wall of buttons, and a hub that binds no NPC
is not covered by §19 at all.

The rule is: *same NPC, same location, overlapping windows.* Two repeatable canvases at one
location that bind **different** NPCs, or **no** NPC, do not collide and **should be separate
canvases** — that is the normal shape, not a workaround. What lives on which screen is
`references/the-surfaces.md`; a room's list is **needs + work + people** and its length falls out of
that closed set (R2), and **8 is a backstop, not a size** (gate 20 — never treat it as a target).

---

## 20. `npc_at_location` — cross-room occupancy, and the any-NPC form

```toml
{ type = "npc_at_location", location_id = "the_front_room", npc_id = "npc_mark", operator = "is_present" }
{ type = "npc_at_location", location_id = "the_front_room", operator = "is_present" }   # ← any NPC
```

`generators/v2.py:4673-4687` (the runtime branch) and `:8578` (the human-readable dispatcher).
`operator` is `is_present` | `is_absent`; `location_id` accepts a slug or a UUID. **`npc_id` is
optional — omit it and the test becomes "is this room occupied by anybody".**

Verified live in a built game, not just read: a choice carrying
`npc_at_location(the_front_room, npc_mark, is_present)` rendered at 23:10, when Mark's
20:00–23:30 row and Tom's 23:00–01:30 row overlap, and was gone at 23:45 with the same state
and the same player. This is the primitive that makes two-NPC scenes possible at all, since
`requires_npc` binds exactly one.

The any-NPC form has a second use: a scene about being *seen* without specifying who by. No NPC
is bound, so nothing can be mis-attributed — there is no character in scope to attribute to.

---

## 21. `clamp` is 0–100, it defaults to TRUE, and it will silently cap a CURRENCY

```js
v2.py:6506   if (clampFlag === undefined || clampFlag === null) { clampFlag = true; }
v2.py:6508   next = window._traitClamp(next, 0, 100);
```

Two facts, and the second one is the dangerous one:

1. **Omitting `clamp` means `clamp = true`.** The default is not "leave it alone".
2. **The clamp is a hard 0–100 on every trait, including one you are using as money.**

A live effect diff shows it: a scene declaring `money +120` under `clamp = true` moves the state
**0 → 100**. With every money grant clamped, a rent above 100 can **never be paid**, the eviction
branch is the only reachable outcome, and nothing anywhere reports it: the TOML is valid, the build
is green, and the sidebar shows a plausible number.

**Rule: any trait that is a QUANTITY rather than a 0–100 meter must carry `clamp = false` on every
effect that writes it.** Money, counts, inventory-ish integers. Meters — nerve, exposure, corruption,
arousal, energy — want the clamp and should keep it.

⚠️ Note the asymmetry with a *deduction*: an unclamped one can go negative. The engine's own
recurring-demand system (`[settings.rent]`) does its own affordability check; an authored deduction
does not — gate the choice on the trait, or price it with `costs`, which the engine refuses when
unaffordable (`v2.py:5150` filters it out, `:5319` is the check — §27).

**How to catch it:** diff the state across the scene and compare against the declared value. A
capped effect looks identical to a working one in the TOML, in the validator, in the build log and
on the scoreboard. Only the live number shows it.

### ⚠️ 21b. `op = "subtract"` IS NOT AN ENGINE OP. It does nothing at all.

```js
// window.applyTraitEffect — v2.py:6496-6503
if (op === 'add')      { next = current + value; }
else if (op === 'set') { next = value; }
else { /* Unknown op; do nothing */ return; }
```

Nothing normalises it: the string `subtract` appears **nowhere** in `generators/v2.py` or in
`apps/projects/services/template_import.py`. The generator interpolates the op straight through
(`v2.py:6605`), so the build emits `applyAndNotifyTrait(..., "subtract", 4, ...)` verbatim and the
runtime drops it on the floor.

**Every effect family, and the ops each actually runs:**

| family | key that identifies it | ops the engine runs | source |
|---|---|---|---|
| trait | `trait` | `add` · `set` | `v2.py:6496-6503` |
| flag | `flag` | `set` · `unset` · `toggle` | `v2.py:6562-6577` |
| quest | `quest_id` | `start` · `update` · `complete` · `cancel` | `setup.applyQuestEffect()`, `v2.py:6662` |
| item | `action`, not `op` | `add` · `remove` | — |

**To take something away, write `op = "add"` with a NEGATIVE value.** Proven live on a shipped
build: `applyAndNotifyTrait('player',null,'count','subtract',4,true,null)` left `count` at 100;
`applyAndNotifyTrait('player',null,'stress','add',-5,false,null)` moved stress 20 → 15.

> **A dead op is silent.** The TOML is valid and the build is green, and **a number that never
> changes looks exactly like a number the player has not moved yet.**
>
> Now checked twice: `gates.py` **gate 25** fails any game using a dead op, and
> `template_import.py` refuses to build one.

---

## 22. Locations do more than `entry_from` — four fields nobody used

The first is the mechanical answer to a premise that says *"ten minutes' walk away"*.

**Travel friction — a per-entry cost on a location.**

```toml
[[locations]]
id    = "the_shop"
costs = { time = 20, energy = 5 }     # time is minutes on the day clock; any other key is a trait
```

```
template_import.py:221    costs: Dict[str, int] = field(default_factory=dict)
template_import.py:2302   costs=_require_dict(l, "costs"),
v2.py:5381                // A location's per-entry cost lives in setup.locations[slug].entry_costs
v2.py:17534               has_location_costs = any(...)   # the travel-cost block is only emitted
                                                          # when some location declares costs
```

**This is what makes a schedule grid matter.** With free instant travel, "who is where at which
hour" is a lookup table. Charge twenty minutes each way and the player cannot be everywhere, so
presence becomes a constraint. Put the cost on the **area**, never on every room.

**A bridge between zones is `crossing_costs` on the area.** A room's `costs` are charged on every
entry, so a container's `costs` can't mean "charged when she crosses into this area". A link
straight to an inner room skips the container, and walking back to the container page charges it
again. Put the toll on the area instead:

```toml
[[locations]]
id             = "loc_mall"
is_container   = true
crossing_costs = { time = 20, energy = 5 }
```

It is charged once when she moves to any place inside the area from a place outside it. Moves
inside the area pay only each room's own `costs`, and leaving is free. A container with a
`default_entry` charges the toll on the room it opens into, once. If she can't afford the room's
cost plus the toll, she is stopped and nothing is charged. Old saves: no new state; the toll applies
from the next move.

**Locked location — visible but blocked, with in-world prose on the card.**

```toml
entry_conditions = { version = "1.0", logic = "AND", items = [ ... ] }
blocked_message  = "The dining room's been dark since the staff went."
```

```
template_import.py:196      entry_conditions: Dict[str, Any] = field(default_factory=dict)
template_import.py:197      blocked_message: str = ""
template_import.py:2293-2294 parsed
template_import.py:8455      loc.properties["entry_conditions"] = l.entry_conditions
```

⚠️ `entry_conditions` needs `version = "1.0"` like any condition block, or it **fails open** and the
door silently unlocks (§4).

**Opening hours — the place is shut at set times.**

```toml
hours       = [ { weekdays = [0, 1, 2, 3, 4], open = "09:00", close = "17:00" } ]
closed_text = "The shutter's down. A paper sign: back at nine."    # optional
```

- `weekdays` counts from 0 = Monday; empty or absent means every day. A `close` that is not after
  `open` runs past midnight, so a Friday `22:00`–`04:00` place is open at 02:00 on Saturday.
  `close = "24:00"` means midnight.
- Closed, the travel card and the text link grey out with "Closed. Opens tomorrow at 9:00 AM." The
  room's passage is guarded too, even with no `entry_conditions`: arriving any other way shows
  `closed_text` and the same line, with a way back. The Schedules page is not muted.
- `validate()` warns when an NPC schedule row or a canvas schedule at the place never overlaps its
  open hours.
- ⚠️ **She is not moved out when a place closes while she is inside.** The guard runs only when the
  room's passage is shown again: coming back from a scene there, or loading a save.
- Old saves: no new state; a save parked in a place that is now closed shows the closed screen.

```
template_import.py:202      hours: List[Dict[str, Any]] = field(default_factory=list)
template_import.py:6457     def _validate_location_hours(template) -> List[str]:
v2.py:10700                 setup.locOpenNow = function (slug) {
```

**Hidden until found — the place isn't listed until a flag is set.**

```toml
hidden_until = { flag = "found_attic" }     # a declared player flag
```

- While the flag is false the place is not listed anywhere: not on the travel card, not in the text
  link, not in a container's list, and not on the Navigation page. A `door` place is hidden too. If
  every place a room lists can be hidden, the "Available destinations:" header hides with them, but
  the room keeps its own exits. `validate()` warns when that leaves a room with no way out.
- Its name is withheld wherever the game says where someone is: the Schedules page, guidance 📍, the
  cast page 📍, the quests page 📍, and the sidebar panel. Each reads "somewhere you haven't found
  yet".
- Nothing stops her going there. A scene that takes her there is how she finds it, so set the flag in
  that scene.
- Old saves: no new state; an old save sees the place hidden until its flag is set.

```
template_import.py:206      hidden_until: Dict[str, Any] = field(default_factory=dict)
template_import.py:6537     def _validate_hidden_places(template) -> List[str]:
v2.py:10572                 setup.locFound = function (slugOrUuid) {
```

**`kind = "thoroughfare"` or `"destination"`** — what the place is for. A thoroughfare is somewhere
she passes through (a corridor, a lobby); a destination is somewhere she goes to do something, and it
is the default. Only those two exact words are accepted. Don't write "hub": that word means a
character's hub canvas. The engine builds both kinds the same way; the release checks read the
word. Old saves: unaffected, since the engine does not read it.

**`offscreen = true`** — a non-navigable "away" label. No nav card, no hub, and it is exempt from the
presence floor and reachability. Use it for a character who is genuinely elsewhere rather than
inventing a room for them. `template_import.py:191`.

**`is_container` + `default_entry`** — a pure navigation wrapper that holds no content.
`template_import.py:190`, `:4850`. A container **swallows** any canvas attached to it; attach to a
non-container hub instead.

⚠️ **The lock above is the INERT kind** — a greyed, unclickable card. For a door she can stand at
and knock on, see **§44**; it is a different field and a different fiction.

---

## 23. The guidance page — `[[quest_cards]]`, and it is OFF by default in practice

The table is **`quest_cards`**, flat and top-level — **not** `[[quests]]`, which is an unrelated
table.

```
template_import.py:3004        for qc_raw in (data.get("quest_cards", []) or []):
template_import.py:1243         class QuestsCard
template_import.py:1324        def _parse_quests_card(d: Dict[str, Any]) -> QuestsCard:
v2.py:16902                    the V2 QuestsPage overlay is emitted only when
                               project.metadata["quests_engine"] == "v2"
```

⚠️ **The trap — an empty guidance page:** `quests_engine = "v2"` turns the
sidebar entry and the page **on**. Authoring no cards leaves a nav link to a heading with nothing
under it. Switching the engine on is not authoring guidance.

**Rendering.** `renderQuestsGoalBlock` (`v2.py:17194`) renders **exactly one** frame per card, in
order: ✓ terminal → 🔓 `ready_canvas` → 🎯 unmet goals. A card that matches none of the three returns
empty and the row goes blank.

⚠️ **A goal-less non-terminal card draws NO frame, and that is how a finished arc ends up looking
live.** It is not a blank *row* — the card still renders its `text` and `tip`, so it reads as an
objective with nothing ticked. Set `terminal = true` on the last card of every arc. `terminal_text`
overrides the ✓ label (default `Arc complete`) and exists because a finished arc and a finished
BUILD are different endings; it needs `terminal` set or the string is dead, and the validator warns.

```
template_import.py:1285        terminal_text: Optional[str] = None
v2.py:17202                    var _tlabel = card.terminal_text || "Arc complete";
```

⚠️ **The one-`terminal_text`-per-game cap is scoped to a game whose arcs are CLOSED.** In a build
where the arcs have genuinely ended, the default `"Arc complete"` is **true** of them; there, one
card marking the build boundary is right and six would be noise.

**It is the wrong rule for a v0.1, and following it there produces the worse outcome.** In a first
release nothing is closed — every track stops at a build boundary — so the cap forces every arc but
one into `"Arc complete"`, **a stronger and falser claim than the string it was rationing**.
`the-release.md`, "Every release ends on an opening", already rules the other way for that case:

> state the current ceiling honestly. The reference game prints a plain marker at the top of **each
> track** so the player knows where the wall is. […] An honest wall is a promise; a silent one is a
> bug report.

**Each track.** So: `"Arc complete"` belongs to an arc that has genuinely **ended**. An arc that
stops because the build stops carries its own marker, and the same plain string on every such track
is what "a plain marker at the top of each track" means. Cap the *claim*, not the field. The field
does both: Cupid's Way, [xavier45], prints *"END OF CONTENT FOR NOW"* where the build stops; In Her
Own Hands, [Progress_Hints_Base], prints *"Your choices have closed this path. No further progress
possible."* where a path has truly closed.

⚠️ **`ready_canvas` MUST name a canvas that HAS A LOCATION, or Frame 2 renders NOTHING.**
`lookupCanvasBySlug` (`v2.py:17169`) walks `help_data.locationCanvases`, keyed by location UUID, so a
**triggerless** canvas — the usual shape for a sex loop or any sub-menu reached by a choice — is not
in that index at all. It returns `null`, Frame 2 does `if (!found) return ""`, and the card falls
through to **no frame**: text and 💡 tip with nothing ticked, the exact failure the warning above
this one describes. Point `ready_canvas` at the **hub** the loop hangs off — it carries the location
and the schedule, which is what the 📍 and 🕒 lines are read from.

⚠️ **`terminal` IS NOT COMPUTED FROM PROGRESS, AND A CHARACTER WHOSE ONLY CARD CARRIES IT READS AS
FINISHED FROM VALUE ZERO.** Frame 1 fires on `card.terminal === true` alone, ahead of every other
frame (`v2.py:17201`) — nothing checks that anything was achieved. So a single card gated
`{ trait = "owed", op = "lt", value = 40 }` and marked terminal matches at `owed = 0` and prints
**✓ Arc complete on turn one**, before the player has met the character.

The rule above — *set `terminal` on the last card of every arc* — is right, and it is not
sufficient:

**`terminal` belongs on a card the player has to CLIMB TO.** An arc needs at least two cards: an
open lower band, and a terminal upper one gated `gte` at a threshold real content sits on. One card
marked terminal is not a ladder with a top; it is a badge with no ladder.

⚠️ **AND A METER IS THE WRONG THING TO GATE IT ON AT ALL.** The rule above says climb to a
threshold; it never says *climb to what*, and the wrong answer is to put the badge on the threshold
that **opens** the content instead of one above it, so the ✓ arrives on the click that unlocks the
scene.

**The fix is not a bigger number — it is a different kind of gate.** Put the ✓ on a **flag the content
sets on its way out**, so it means *you have played this* rather than *you have ground past it*. The
v1 hint system had exactly that pairing (`arc_closure_flag` pre + `arc_complete` post,
`template_import.py:1198-1207`) and the v2 card schema dropped it without replacing it:

```toml
# climb  - the goal frame, with live progress
when = [ { trait = "want", subject = "npc", npc_id = "npc_x", op = "lt", value = 42 } ]
goals = [ { trait = "want", subject = "npc", npc_id = "npc_x", op = "gte", value = 42, label = "..." } ]

# ready  - the Ready frame. NO goals: an empty goals list is allMet vacuously true
when = [ { trait = "want", subject = "npc", npc_id = "npc_x", op = "gte", value = 42 },
         { flag = "x_loop_played", subject = "player", op = "is_false" } ]
ready_canvas = "hub_x"            # the HUB, never the triggerless loop - see above

# done   - the tick, and it means it
when = [ { flag = "x_loop_played", subject = "player", op = "is_true" } ]
terminal = true
```

⚠️ **A goal threshold no condition anywhere reads is a number the player climbs to for nothing.**
Such thresholds stay invisible while the terminal frame outranks the bullets, and the moment
the badge is fixed they become live instructions to grind for nothing — so fix the numbers in the
same pass, never one without the other. `scripts/gates.py`'s **`lint · the badge arrives before the
content`** reports both.

⚠️ **`pickQuestsCards` takes EXACTLY ONE scope string, and anything else fails silently.**

```
v2.py:17042   setup.pickQuestsCards = function(scope) {
v2.py:17043       if (scope !== "story_goals") return [];
```

A hard early return, no error, no warning. A typo in that string gives an **empty top section on the
guidance page** and no clue why. Read the whole function, not the part that answers your question.

**Selection.** `pickQuestsCards(scope)` (`v2.py:17042`) returns every matching top-tier card;
`pickQuestsCard(slug)` (`v2.py:17017`) returns the **single highest-`priority`** match for a
character — so a character's cards are a one-live-at-a-time chain.

⚠️ **Quest conditions use a SEPARATE evaluator with NO fail-open** — `checkQuestsCondition`,
`v2.py:17083`. **Never paste `version = "1.0"` onto a quest card.** That key is required on canvas
conditions and is wrong here.

⚠️ **The sidebar next-row calls the identical functions as the page** (`v2.py:18793-18796`). There is
no separate "sidebar quest": edit a card and both surfaces move together, and a character with no
card renders a blank next-row.

### The next STEP in the rail — `[[sidebar_items]] type = "quest_next"`

**A quest card has no `title` field** (`template_import.py:1243-1285`) — `text` is the narrative body,
`tip` is the 💡 line, and the only short imperative string on a card is `goals[].label`. So there is
nothing on a card that a sidebar could show as a headline.

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

⚠️ **Check the label is not circular.** A card must not name a choice gated at the exact value the
card is trying to reach — a card for `trade ≥ 15` naming a choice that itself requires
`trade ≥ 15`. Name a choice gated **one tier below** the card's own goal. Nothing in `gates.py` catches this; read each card against the gate on
the choice it names.

**`locked_text_threshold`** (`v2.py:14915-14916`) prints an explicit *"Requires …"* hint on a
locked choice, distinct from `locked_text`, which replaces the label (§15).

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
v2.py:3611   const dayIndex = ["Monday", "Tuesday", …].indexOf(timeState.current_day);
             also :3797 :3953 :4008 :4074
```

Set it to `0` and `indexOf` returns `-1` at every call site.

**The false alarm:** no schedule row matches, **every location reports nobody present**, and the
game reads as having a broken presence system. It does not. The harness set a number where a string
belongs.

### 24.3 Ask the engine who is present — do not recompute it

```
v2.py:5473    setup.getNpcsPresentAtLocation = function(locationId)
v2.py:21835   the engine's own nav badges call it
v2.py:21876   and again for the portrait row
```

**The false alarm:** hand-rolling presence from `[[npcs.schedules]]` gets overnight windows wrong —
a `22:00`–`04:00` row wraps midnight and a naive start ≤ now ≤ end comparison drops it — so a
correctly-scheduled character reads as absent.

### 24.4 The built page is ENTITY-ENCODED — macros are not stored literally

A built page stores its macros encoded — `&lt;&lt;set`, not a literal `<<set`.

**The false alarm:** grep the page for `<<set` and find nothing, and conclude the game has no state
writes.

**Always `html.unescape()` before matching macro syntax in built output.** Note this applies to the
*page*; the authored TOML is not encoded.

---

## Unverified — do not cite until read

Facts we believe but have not confirmed against source during this skill's construction.
Read and cite before using; delete from this list once promoted above.

- The exact cooldown count for random events.

*(`_render_group_chain` collects consecutive `group` blocks into one variant chain at
`v2.py:16300-16306`, and first match wins; lint
**adjacent groups** lists the dead ones.)*

---

## 25. A speaking block with no `speaker` renders under a placeholder name, not a person

**Verified against `v2.py` on 2026-09-28.** `dialog` and `thought_bubble` both default a missing
`speaker` to the string `"npc"` (`v2.py:16726`, `v2.py:16822`), but they resolve the speaker
**differently** after that, and the field is **not optional** for either:

- **`dialog`** — `"player"` renders the player label; `"unknown"` renders **"Stranger"**
  (`v2.py:16728-16758`). **Any other value, including a missing speaker, takes the NPC branch, and
  that branch reads only `npcId`** — the `speaker` string is never used as the id
  (`v2.py:16761`). With no `npcId` the id is `""`, and the fallback prints **"NPC"**
  (`v2.py:16768`):

  ```python
  npc_id = props.get("npcId", "")                                                     # v2.py:16761
  npc_name = npc_id.replace("npc_", "").replace("_", " ").title() or "NPC"            # v2.py:16768
  ```

  So `speaker = "npc_bev"` with no `npcId` renders "NPC", not Bev.

  **A walk-on with no id** uses `speaker = "unknown"` ("Stranger"), and the narration line just
  before his dialogue names his role. A role-labelled speaker is a known gap, left for a later
  engine item.

- **`thought_bubble`** — `"player"` renders the player's thought label. `"unknown"`, **or any
  speaker that does not start with `npc_` or `npc`**, renders **"💭 Someone is thinking:"**
  (`v2.py:16834-16840`). Otherwise the id is **`npcId` if present, else the `speaker` string
  itself** (`v2.py:16842`), so `speaker = "npc_bev"` alone does find Bev. A missing speaker gives
  the id `"npc"`, which matches nobody, and the same title-case fallback turns it into **"Npc"**
  (`v2.py:16848`) — *"💭 Npc is thinking:"*.

  ```python
  npc_id = props.get("npcId") or speaker                                              # v2.py:16842
  ```

Either way, a speaking block with no `speaker` shows a placeholder where a person should be. Write
`speaker` and, for an NPC, `npcId` on every block, as below.

### The three forms, all required to carry `props`

```toml
{ type = "dialog",         props = { speaker = "player" },                        content = "…" }
{ type = "dialog",         props = { speaker = "npc", npcId = "npc_bev" },        content = "…" }
{ type = "thought_bubble", props = { speaker = "player" },                        content = "…" }
{ type = "thought_bubble", props = { speaker = "npc", npcId = "npc_bev" },        content = "…" }
{ type = "dialog",         props = { speaker = "unknown" },                       content = "…" }
```

`speaker = "unknown"` is the deliberate pre-introduction form: it renders **"Someone is thinking:"**
for a thought bubble (`v2.py:16838`) and **"Stranger"** for dialogue (`v2.py:16755`). Use it while
the player cannot yet know the name — never as a shrug.

⚠️ **`dialog` is the correct type; `dialogue` is not.** The recognised list is `heading, paragraph,
dialog, thought_bubble, image, video, cascade, group, block_pool, clip` (`v2.py:16869`). A mistyped
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
before writing a settle-up scene.

```toml
[settings.rent]
enabled          = true
due_day          = "Friday"          # weekday names only — VALID_DAYS, template_import.py:5963
collector_npc    = "npc_collector"   # must exist in [[npcs]]
start_after_flag = "first_shift_done"
stages      = [ { amount = 100, after_total_paid = 0 }, { amount = 150, after_total_paid = 300 } ]
stage_lines = [ "…", "…" ]           # what the collector says when stages[i] takes over
on_short    = "carry"                # a short week is owed next week; no eviction, no game over
currency_symbol  = "$"               # rent pages only — eight other money prints hardcode "$" (§33)

[settings.rent.text]                  # every beat of the pages is authored here
title = "…" · scene = "…" · greeting = "…" · paid_scene = "…" · paid_response = "…"
paid_closing = "…" · cant_pay = "…" · partial_pay = "…"
```

**How it fires — and the timing is the part authors get wrong.**

1. `advanceDay()` (`v2.py:6191`) sets `rent_state.is_due` when the day rolls over **to** `due_day`
   (at `:6168`).
   Days roll at midnight (`v2.py:6156-6159`), so the demand arms at **00:00 on the due day**, not at
   whatever hour the collector's schedule row says.
2. The next time the player lands on a `Location_*` passage or `Navigation`, they are intercepted
   into `RentDay` (`v2.py:17490-17499`). Never mid-canvas.
3. Paying runs `$player.core_traits.money -= _rent` and clears `is_due` (`v2.py:18284`). Verified
   live.
4. A short week with `on_short = "carry"` is paid as far as she can and the rest is owed next week
   (`setup.carryRent`, `v2.py:13642`); nothing ends.

**`start_after_flag` is what stops it being a scripted loss.** Until that flag is set the demand
never arms, so the flag belongs on the canvas that first gives her a way to earn.

> ⚠️ **DO NOT ALSO WRITE THE PAYMENT AS A CANVAS.** A hub rung that narrates the payment beside a
> working `[settings.rent]` gives the player two settle-ups; with no cost on the rung, one of them is
> free, and the free one is the one with the writing in it. If the engine takes the money, the authored scene beside it must be about something else.

**Money must be unclamped for this to work at all.** A demand above 100 against `clamp = true` money
(caps at 100) can never be paid in full — see §21.

- `setup.currentRent()` (`v2.py:13591`) is the amount at every read; the payment that moves the stage
  shows its line on the paid screen. `stages`, `stage_lines` and `on_short` are opt-in, emitted only
  when used. Keys: `template_import.py:481-490`.
- Carry sets the flag `rent_carried` and ignores `grace_periods` and `eviction_mode`. **No game over
  over rent** *(LO decided, D8d)*.
- **The old route**, without `on_short`: a fixed `amount`, a short week spends `grace_periods`, then
  the eviction branch — `eviction_mode = "flag_set"` sets `eviction_flag`; the default `"game_end"`
  ends the game.
- Old saves: `total_paid` and `owed` backfill to 0, so a save restarts at stage 1 owing nothing.

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
   filters on `setup.checkCostsAffordable(c.costs)`, defined at `v2.py:5319` (the filters: `:5150`,
   `:5177`, `:5664`). An unaffordable rung does not render as a broken click — it is not
   offered.

   ⚠️ **That is the canvas picker. An exit-block CHOICE behaves differently, and better.** There the
   generator opens `<<if setup.checkCostsAffordable(...)>>` (`v2.py:14683-14684`) and writes an
   `<<else>>` that keeps the row, greyed, with the requirement appended by the engine itself
   (`v2.py:14842-14849`):

   > `Work a shift 🍺 (Requires 15 Energy (you have 6))`

   **A priced choice explains itself with no authoring at all**, and a price is what the field's
   spoken refusals name most (37% — §15). This is the asymmetry worth knowing: `costs` come with
   their own message, a number condition gets the engine's suffix (§15), and a flag condition with no
   `locked_text` goes mute. The gate **"a locked door says why"** therefore never counts a cost-only choice
   against a game.
2. **The deduction is applied by the engine, not by your effects list.** A `costs` entry is parsed as
   `{trait, value}` only (`template_import.py:2658-2661`). On a **choice** it is deducted inline with
   `clamp = false` (`v2.py:14750`), so a balance above 100 survives it.

⚠️ **Canvas and location costs ARE clamped to 0–100, and you cannot turn it off.** They go through
`setup.deductCostArray` (`v2.py:5349-5355`), which passes `clampFlag = true` into
`applyAndNotifyTrait`, with no `clamp` field on a `costs` entry to override it: at `money = 150`, a
4-charge on a canvas trigger or a location's entry cost leaves **100**. Below 100 it is correct.
`[settings.rent]` is unaffected; it subtracts directly (§26).

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

Parsed at `template_import.py:3251-3308` (`TemplateDailyTick`), and both effect lists run when the
day rolls. `flagEffects` with `op = "unset"` is the mechanism behind every `_today` flag.

**Why it matters more than it looks.** `max_triggers_per_day` is read **off the trigger**
(`v2.py:12739`, `getattr(trigger, 'max_triggers_per_day', None)`). A triggerless rung — a canvas
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
choice     flagEffects -> costs -> modifiers -> … -> advanceTime   v2.py:14732-14834
node exit  advanceTime -> traitEffects -> flagEffects              v2.py:15208-15211 · :15172-15173
```

`advanceTime` rolls the day inside itself — `while (current_hour >= 24) { … advanceDay(); }`
(`v2.py:6156-6159`) — and `advanceDay` is where this hook clears the flags (`v2.py:6299`).

So on a rung whose `time_progression_minutes` crosses midnight:

| where the flag is set | what happens |
|---|---|
| **the choice** | set on the old day, then cleared by the tick → the new day is open. **Correct.** |
| **the rung's exit** | tick clears first, flag is written second → **the new day starts already capped.** |

⚠️ **A LOCATED canvas does not need the flag at all.** `max_triggers_per_day` is read off the
trigger (`v2.py:12739`) and `markCanvasTriggered` stamps its day key **before** `advanceTime` runs
(`v2.py:4937`), so it has none of this problem. The flag pattern exists for *triggerless* rungs.

### 28.2 Two of the three parts validates and does nothing

A flag read as `is_false` and cleared here, with **no canvas setting it**, is a cap that never
closes. Nothing in the toolchain objects: the generator's flag-chain validator only reports a
never-set flag when a condition requires it `is_true` (`validate_flag_chains()`, `v2.py:13319`; the
test at `:13360`) — deliberately, since an
`is_false` read is a re-entry guard rather than a prerequisite — so the gate simply fails open.

A talk screen capped this way stays clickable all day and out-earns the day-capped
rungs it sits below. `scripts/gates.py` gate **`a day-cap closes`** exists for exactly this.

### 28.3 What the screen looks like once the cap IS spent

§28.2 asks whether the cap closes. This asks what the player sees the moment it has, which is every
day, by design.

**A choice whose conditions fail renders NOTHING.** It is wrapped in
`<<if setup.triggerConditionsSatisfied(…)>>` (`v2.py:14672`) — no greyed line, no reason, no hours,
unless the choice opts in with `show_when_locked` (`v2.py:14852`). Absent that, a spent rung leaves
no trace on the screen it used to be on.

**A cost-bearing choice counts as conditional too.** The engine's own test for whether a node has a
usable exit is `has_unconditional_choice`, and a choice registers as unconditional only when it
carries **neither** `conditions` **nor** `costs` (`v2.py:14691-14701`). So a screen whose one
affordance is *"Put it in the slot ($3, 5m)."* is exactly as empty to a player at $0 as a spent hub
is to a player who has had their go.

**When nothing passes, the engine does three things** (`v2.py:15014-15077`):

| | |
|---|---|
| `console.warn` | always, in every build — canvas slug, every choice's conditions, and a live state snapshot |
| a diagnostic banner | `$flags.debug_mode` only. Re-evaluates each predicate and prints ✓/✗ per item |
| `[[Continue->…]]` | player-facing escape to the trigger location (`_get_return_location`, `v2.py:14409`). **Fires no effects** |

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
renders as a clickable portrait on the location screen (`renderNpcPortraits`, `v2.py:5678`), not as
an auto-fire, so a leave-link pointed at the node's own location lands the player back in the room
with the portrait still on it. No loop.

---

## 29. `cap` on an effect — a VALUE ceiling, not a rate limit

```js
// v2.py:6510-6516, inside window.applyTraitEffect (which applyAndNotifyTrait calls), AFTER the clamp
if (cap !== undefined && cap !== null) {
  var capNum = Number(cap);
  if (!isNaN(capNum)) {
    if (next > capNum) next = Math.max(current, capNum);
  }
}
```

`cap` is the **7th positional argument** to
`setup.applyAndNotifyTrait(targetType, npcId, trait, op, val, clampFlag, cap)` (`v2.py:6605`).
Authored as a sibling of `op`/`value` on any effect and passed straight through
(`v2.py:15597`, `:15605`, `:11533`):

```toml
effects = [ { targetType = "player", trait = "energy", op = "add", value = 40, cap = 100 } ]
```

Read the `Math.max(current, capNum)` carefully: **a cap never pulls a value down.** If the trait is
already above the cap it is left alone; the cap only refuses to *raise* it past the ceiling. So:

| use | correct? |
|---|---|
| bounding a **restore** — a sleep rung that adds energy | ✅ this is what it is for |
| bounding a repeatable **relation** or reputation grant so one rung cannot max a character | ✅ |
| bounding an **ascent tier** | ❌ the tier must be able to reach its top band; a cap there deletes content |
| **throttling how fast** anything rises | ❌ it does not touch the rate. See `the-meters.md` |

`cap` and `clamp` are independent and both apply — clamp first, then cap.

---

## 30. A banded sidebar item and the auto Traits dump both render — unless you keep the key out of the dump

The sidebar prints **two** things about a trait, from two different places:

1. **The auto Traits dump** — every declared `core_trait`, as a bare number.
2. **Whatever `[[sidebar_items]]` you authored** — `trait_status_text` (`v2.py:18627`),
   `trait_words` (`v2.py:18690`), `trait_bar` (`v2.py:18580`).

They do not know about each other. Band a trait without suppressing its number and the player reads
*"Nothing under it"* and `cover 55` stacked on top of each other.

**The suppression is `[[traits.labels]] in_dump = false`.** It keeps the key out of the auto Traits
dump and nothing else: the Stats page and every "+N" toast still name it. `hidden = true` also
suppresses it, but that is the secret-trait switch (no dump, no Stats page), and it is keyed by name,
so hiding the player's banded `corruption` with it hides every man's `corruption` too. Every entry
carries a `label`, hidden or not: the toast names every trait an effect moves (gate `one name per trait`).

**One name per trait.** Every screen names a trait the same way: its `label`, or the key tidied
("crowd_standing" becomes "Crowd standing") when there is none. That covers the locked-button
suffix, the toast, the Stats page, the dump, guidance, a `trait_bar` with no `label`, and the cost
tags. A locked button gated on a man's trait names him and his value:
*"Ask him to stay. (Tobin's Trust 50+ (has 10))"*. A condition already met is not listed. Old saves:
no new state.

**A number beside the word.** `show_value = true` on a `trait_words` item prints one line: its
`label` (or the trait's name), the number, and the band word, as in *"Corruption: 12 · Curious"*.
When no band matches it prints *"Corruption: 50"*. Keep `in_dump = false` on the key, or the
dump prints the number a second time.

```toml
[[sidebar_items]]
type  = "trait_words"
trait = "cover"
bands = [ { min = 0, max = 14, text = "Long dress, hair pinned" },
          { min = 15, max = 100, text = "Apron off" } ]   # ← top band CLOSED, and its
                                                          #   max sits at/above the ceiling

[[traits.labels]]
key     = "cover"          # ← REQUIRED, or the number prints underneath the words
label   = "Cover"          # the one name every screen uses (gate `one name per trait`)
in_dump = false
```

⚠️ **A trait absent from `[[traits.labels]]` entirely is NOT kept out** — it still appears in the
dump. A meter banded in `[[sidebar_items]]` and absent from `[[traits.labels]]` prints twice.

⚠️ **The other half: a banded value that lands outside every band renders NOTHING** — the whole card
disappears, which reads as a missing HUD element rather than a wrong number, so a quick playtest
sails past it.

**The band rules are PER TYPE, and an open top band is legal on exactly one of the three.** The
example above is `trait_words` on purpose: its shape is the one that is legal everywhere, so copying
it blindly cannot break a build.

| type | open-ended top band? | the rule | source |
|---|---|---|---|
| `trait_status_text` | **yes** — an omitted bound defaults to ∓1e9 | at least one of `min` / `max` | `template_import.py:4323-4329` · `v2.py:18642-18643` |
| `trait_words` | **no** | `flag` **XOR** range; in range mode BOTH `min` and `max`. A flag-only band is legal | `template_import.py:4185-4195` · `v2.py:18711-18712` |
| `trait_bar` | **no** | both `min` and `max`; `flag` is rejected outright; `bands` itself is optional | `template_import.py:4231`, `:4247-4253` |

So the fix for a value off the top of the ladder is **not** to drop the `max` — that compiles on one
type and hard-fails the build on the other two. Give the top band a `max` at or above the trait's
ceiling, or `cap` the terminal add (§29).

### 30.1 A hygiene system is a deliberate non-feature — do not build one

This engine has no hygiene, hunger or thirst primitive, and that is a decision rather than an
omission. It is recorded here because **`trait_status_text` makes one authorable in an afternoon** —
its own spec comment says *"Use for hygiene/energy/hunger-style needs that recover on action"*
(`template_import.py:4292-4296`) — so the temptation lands precisely on this section.

The field's verdict, from section I's read of all 27 parseable corpus games:

- **`degrees-of-lewdity` built hygiene and switched it off.** 1,273 writes of `$hygiene`, 1,207 of
  them the identical `<<set $hygiene += 500>>`, feeding **one** read site: a seven-band ladder in a
  widget that is never called. The string `speckless` appears exactly once in 15,626 passages —
  inside that widget. Its initialiser says so outright:

  ```
  <<set $hungerenabled to 0>>  /* unused */
  <<set $thirstenabled to 0>>  /* unused */
  <<set $hygieneenabled to 0>> /* unused */
  ```

- **`free-cities`, the corpus's deepest body simulator, never modelled it** (structure only; it
  fails the adults-only rule). Its character objects carry eight numeric body properties and no
  hygiene or arousal property at all. Its two most-read properties are `devotion` (1,019) and
  `trust` (667) — above every body part.

- **Corpus-wide, hygiene is the rarest of the four body subsystems**: 234 read sites against
  arousal's 8,183 and clothes' 6,821. Two of 27 games clear 20 read sites, and one of those two is
  a single 22-read variable that is 86% colour.

**If a need must exist, make it a `costs` entry on the acts that need it** (§27) — a price the
engine already enforces — rather than a meter with a ladder and a decay hook. Recorded in the same
register as the per-character dialogue colour in §34: a known difference from the field, left
unbuilt on purpose.

---

## 31. `requires_npc` does NOT gate an auto-firing canvas

> ⚠️ **Scoped.** The heading is still true and the rest of this section still holds
> for the auto-fire path. What changed is the count: `requires_npc` is now read on **four**
> paths — random ambients, substitution targets, **the solo lane** and **the phone launcher**, the
> last two through `setup._npcPresentForCanvas`. See §46. The auto-fire path was left alone on
> purpose: its validator `isCanvasValid` is shared with `_tryRule`, and every one-shot meeting
> hangs off it.

**The field is real and it works — on the paths that read it.** A canvas that AUTO-FIRES on
entry never consults it, so a one-shot written as "fires where the character is" fires whether
they are there or not.

```
setup.getStoryCanvasRedirect            v2.py:5655   ← entry-time auto-fire
  -> setup.selectAutoFireCanvasForLocation   v2.py:5105
       filters: isRepeatable · triggerMode=="random" · substitutionOnly · hiddenFromLocation
                · isCanvasSelectable · priority
  -> setup.isCanvasSelectable                v2.py:5259   (isActive, then isCanvasValid)
  -> setup.isCanvasValid                     v2.py:5269
       checks: hasSchedules/scheduleParams · conditions · canTriggerCanvas
       requiresNpc is NOT among them.
```

`requiresNpc` is emitted into `help_data.locationCanvases` at `v2.py:12844` and read at five sites
on four paths:

```
v2.py:6002   var npcLoc = setup.getNpcLocation(canvNpc.requiresNpc);
             checkRandomEncounters — the RANDOM-ENCOUNTER presence gate
v2.py:6078   var subNpcLoc = setup.getNpcLocation(target.requiresNpc);
             checkAndSubstituteCanvas's _tryRule — the same check on the substitution TARGET
v2.py:5180   if (!setup._npcPresentForCanvas(c, locationId)) continue;
             selectSoloActivityCanvasesForLocation — the solo lane (§46.1)
v2.py:5829   if (!setup._npcPresentForCanvas(c, locationId)) continue;
             renderSoloActivities — the solo lane's inline blocked/cooldown loop
v2.py:3175   if (!setup._npcPresentForCanvas(c, o.locationId)) continue;
             _renderLauncher — a phone launcher option whose canvas is in this room
```

None is the auto-fire path. **Consequence:** a one-shot meeting bound to a bar with
`requires_npc` set, whose character's schedule puts them there only in the evening, auto-fires the
moment the player walks in once its flags are met — so a scene that introduces them can play in an
empty bar at ten in the morning.

**What to do instead:** put a `[[canvases.trigger.schedules]]` row on the meeting that matches the
character's own schedule row, or gate it on a flag the player can only hold by having been where
they are. Keep `requires_npc` as well — it is free, correct on the paths that read it, and it
documents intent — but it is not the thing stopping the canvas.

Portrait rendering is the mirror image and behaves as documented: `selectNpcPortraitCanvasesForLocation`
skips every non-repeatable canvas outright (`v2.py:5143`, `if (!c.isRepeatable) continue`), so a
first-contact one-shot can never leak onto a location screen as a face.

### 31.1 The consumers, by name — and the comment that says otherwise

The consumers are `setup.checkRandomEncounters`, `setup.checkAndSubstituteCanvas`, the solo lane
(`selectSoloActivityCanvasesForLocation` and `renderSoloActivities`) and the phone's
`setup._renderLauncher`. Naming them matters, because the first three are exactly the three
trigger shapes a check must exclude: `trigger_mode = "random"`, `substitution_only = true`, and
`is_repeatable = true`. Everything else that names a character and fires on entering a room is on
the auto-fire path and is not gated by this field at all.

⚠️ **`requires_npc` does not replace a meeting's place and time** — it is true only for the
functions above. Gated as `a meeting fires where they are` (G38).

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

`window.advanceTime(minutes)` (`v2.py:6145`) adds minutes to `time_state.current_minute`, rolls the
hour past 60 and the day past 24, expires temporary modifiers, and repaints the sidebar. That is the
whole time API. **Nothing in this engine can send the clock to a named hour**, so a label or a beat
promising one ("work till one", "back by six") is a promise the engine cannot keep.

`window.waitTime(minutes)` (`v2.py:6186`) is the sidebar wait buttons' entry point — the same
advance, plus `setup.commitMoment()`, because a wait navigates nowhere and would otherwise live only
in the active moment.

An exit that declares no `time_progression_minutes` still costs **3 minutes**
(`v2.py:15323`, `config.get('default_time_progression', 3)`; the exception fallback at `:15521` emits
the same `advanceTime(3)`). A four-node opening has therefore drifted 9 minutes before the first real
choice.

There is no `@time` token either — `_resolve_at_references` (`v2.py:16160`) resolves `@player` and
`@<npc>` and returns everything else untouched. The clock can be *shown* (`<<timeDisplay>>` at the
top of `StoryCaption`, `v2.py:17967`/`:17984`, rendering `<<timeFormatted>>` at `v2.py:18492`) but it
cannot be *printed into prose* by any authored token.

### 32.2 Travel time is tagged on the card; activity time is tagged nowhere

| what | tagged? | where |
|---|---|---|
| `[[locations.costs]] time` | **yes, automatically** — renders `20m` on the nav card | `getLocationCostTag` `v2.py:5418`, used at `:21838` / `:21872` |
| a choice's `time_progression_minutes` | **no** — emits a bare `<<script>>advanceTime(150);<</script>>` at the bottom of the passage body | `v2.py:14834` |
| a trait `costs` entry | yes, when unaffordable | `getCostBlockedMessage` `v2.py:5364` |

So a door announces its twenty minutes and a two-and-a-half-hour shift announces nothing. If the
duration is to appear, the author puts it in the label. `references/the-clock.md` C4.

The field puts it there as a matter of course. Course of Temptation's most-returned-to screen
prints the cost on every single option — `<<dtime 15>>` beside the shower, `<<dtime 10>>` beside
grooming — alongside the need effect (`<<dalterneed Hygiene 1000>>`), so nothing about the clock is
a surprise (`~/Documents/Female_PC_Craft_Study_20260823/findings_C_loop.md`). No rule change here:
C4 already owns this as a lint, and the corpus evidence behind it is thin — 4,219 of the corpus's
4,260 duration tags belong to one game.

### 32.3 `show_when_blocked` — the only out-of-hours surface

A solo activity whose schedule window has closed is dropped from the location list entirely, unless
the author opts in:

```toml
[canvases.trigger.metadata]
show_when_blocked = true
cooldown_message  = "Counter work — mornings, eight till one."
```

Read at `v2.py:12777-12781`, emitted as `showWhenBlocked` / `cooldownMessage` (`v2.py:12840-12841`).
`renderSoloActivities` (`v2.py:5807`) checks `isCanvasValid` (`v2.py:5269`) — which returns false on a **schedule
miss** before anything else (`v2.py:5271-5276`) — and, when the flag is set, pushes the canvas onto
`soloCooldownBlocked` instead of dropping it, rendering a dimmed non-clickable line carrying the
message (`v2.py:5883`). The same path also catches `max_triggers_per_day` exhaustion
(`v2.py:5837`).

⚠️ **Everywhere it is unset,** windowed work simply vanishes and the player has no surface that says
when to come back. The `SchedulePage` (`v2.py:21427`) publishes hours for
**people** — every declared `[[npcs.schedules]]` row as a Time / Location / Activity / Days table —
and there is no equivalent for places or activities. `references/the-clock.md` C5.

---

## 33. Money on the screen — where the engine prints it, and in what notation

The generator prints a money figure at **twenty-two sites**. `[settings.rent] currency_symbol`
governs **eleven**, every one on the rent pages. Eight hardcode `$`; three print no notation at all,
so declaring a symbol other than `$` still leaves the game with two.

### 33.1 The census

Re-read line by line on 2026-09-30.

| notation | where | `v2.py` |
|---|---|---|
| **honours `currency_symbol`** | `RentDay` — the collector's default greeting | `:18182` |
| | `RentDay` — *"You have X. Rent is Y."* (2 prints) | `:18186` |
| | `RentDay` — the `Pay $N rent` button | `:18189` |
| | `RentDay` — *"Owed from last week"* (`on_short = "carry"`) | `:18138` |
| | `RentDay` — the pay-what-you-have button (carry) | `:18147` |
| | `RentDay_Paid` — remaining money | `:18228` |
| | `RentDay_Short` — *"You have: … You need: …"* (2 prints) | `:18261` |
| | the carried-week screen — *"You paid … Carried to next week …"* (2 prints) | `:13577` |
| **hardcodes `"$"`** | the clothing shop — balance | `:2168` |
| | the clothing shop — item prices (3 prints) | `:2225` `:2228` `:2231` |
| | the phone job board — a job's income | `:3077` |
| | the phone bank — balance, and cash | `:3111` `:3112` |
| | the bank-interest notification | `:6320` |
| **no notation at all** | an unaffordable choice — *"Requires 3 Money (you have 1)"* | `:5368` |
| | a location's nav cost tag — *"30m · 3 Money"* | `:5415-5419` |
| | the sidebar `trait_bar` — *"Money: 12 / 100"* | `:18524` |

`self.rent_currency_symbol = rent_settings.get("currency_symbol", "$") or "$"` — `v2.py:1212`.
Emitted to the runtime only when rent is enabled (`v2.py:3451`), so a game without
`[settings.rent]` has no symbol setting at all.

Since EN2c `currency_symbol` covers every rent screen, and nothing else.

### 33.2 The symbol is a prefix

Every honouring site concatenates symbol-then-number:
`"Pay " + _cur + _rent + " rent"` (`v2.py:18282`),
`<<print _cur>><<print _money>>` (`v2.py:18279`). There is no suffix form and no format string. An invented unit that reads after the number (`10 coin`, `1000 caps`) cannot be
expressed through `currency_symbol`.

### 33.3 The sidebar's label

```
<<set _traitLabel to _item.label || setup.traitLabel(_tbKey)>>     v2.py:18591
<<print _traitLabel>>: <<print Math.floor(_traitVal)>> / <<print _traitMax>>   v2.py:18617
```

A `trait_bar` takes its label from the sidebar item's own `label`, and falls back to the trait's one
name (`setup.traitLabel`, `v2.py:4197`, EN5), so `[[traits.labels]] key = "money", label = "Change
bag"` now names the sidebar readout too (§30).

`_traitMax` defaults to 100 (`v2.py:18590`), so an uncapped counter renders as a fraction of a
maximum it does not have: a money trait with no `max` prints **`Money: 12 / 100`** over a 12% fill
bar. Set `max` to something the currency will not exceed, or show money as `trait_words` with
`show_value = true` and no bands (*"Money: 140"*, §30).

### 33.4 A choice's price is never rendered when the player can afford it

An affordable choice renders its authored label and nothing else. The engine speaks a price **only
on the failure path** — `getCostBlockedMessage` (`v2.py:5364`) emitted into
`<span class="locked-choice">` at `v2.py:14848`:

```
affordable      Feed the meter ($3)                        exactly what the author typed
unaffordable    Feed the meter ($3) (Requires 3 Money (you have 1))
```

This is the same asymmetry as §32.2 for time: the engine tags the cost it stops you paying and
stays silent about the one it takes. So the visible price is authored prose in every normal case —
gate 21 exists because of this, and `the-economy.md` R7 governs its notation.

### 33.5 `[[traits.labels]] unit` is dead

The importer reads it (`template_import.py:3468`) and stores it in project metadata (`:8010`). No
generator reads it back — a grep of `v2.py` for `unit` returns nothing. It is not a lever for
pluralising a currency.

---

## 34. `[ui.cast_page]` — the who-is-who page, and it authors nothing

**On by default in `templates/board.toml`** (IC13). All four passing games carry one — Course of
Temptation [Social], In Her Own Hands [Characters], Shady Deals [Contacts], Cupid's Way
[Relationships] — and it lists only people she has met, so it keeps F8.

The player's place to look somebody up. Measured across the 27-game mopoga field: **18 of 27**
shipped sandboxes carry a page like this and **7 of the 8** parsed top-ten do — the lone exception,
degrees-of-lewdity, carries the same load inside its prose by swapping description for name on the
meeting flag in 64 places. **None of the 27 uses a narrator to tell the player who somebody is.**

> `college-daze`'s is a **phone contact list** — `Check Contacts`, one row
> per person, each row a link to that person's own status page, and a `(*NEW!*)` badge on the row
> when there is something new behind it. Rows appear as people are met, gated on 43 distinct
> `$met_*` flags. `free-cities` has no cast page: its `Starting Girls` is a purchase screen.

```toml
[ui.cast_page]
title        = "The Crew"
button_label = "The Crew"     # defaults to title
button_icon  = "👥"
intro        = "Nine of you on this contract. Four of them are blood."
```

**Presence of the block is the entire opt-in.** There is no content field, because every line on a
card already exists elsewhere in the game and is read at runtime:

| line | source |
|---|---|
| name | `$npcs[uuid].name` |
| who they are to her | `$npcs[uuid].relationship` — the **existing** `[[npcs]] relationship` field |
| what they are about | `setup.npc_tags[slug]` — the `[[npcs]] tags` field, below |
| 📍 where, this minute | `setup.getNpcLocation` + `setup._locNameFromUuid` |
| the next step | that character's own quest card — `renderQuestsGoalBlock` + its `tip` |
| his numbers (opt-in) | `show_traits` below — each row is the trait's name, his value, and a word |

**His numbers.** The page shows none unless you name them — and under D1 every trait he keeps is
named (`the-meters.md` W1):

```toml
[ui.cast_page]
show_traits = ["trust"]                   # every card
trait_bands = { trust = [ { max = 19, text = "Wary" }, { min = 20, max = 59, text = "Warming" },
                          { min = 60, text = "Yours" } ] }   # optional; min or max may be left off

[[npcs]]
id          = "vic"
show_traits = ["power"]                   # his card only, added after the page's list
```

A row reads *"Trust 40 · Warming"*: the trait's one name (§30), his value, and the first band that
holds it. A `hidden` trait never shows, and neither does one he doesn't have. `validate()` errors on
a key no character carries and on a malformed band. It warns on a band that no list shows. Old saves: no new state; the page reads his
live values.

```
template_import.py   TemplateCastPage, [ui.cast_page] parse, metadata write
game_graph.py        the NO-DB path's ai_behavior_config write  <- the default build
v2.py                _generate_cast_page  ::CastPage + ::CastWidgets
```

⚠️ **`relationship` is the ONLY NPC string that survives to runtime.** `description` is
`entry.pop("description", None)`'d before `$npcs` ships (`v2.py:1098`) — deliberately, because
`$npcs` is snapshotted into every history moment. A 50-word bio in `[[npcs]] description` is an
author note the player will never see. Write the player-facing line in `relationship`; one sentence
is what the field ships (patriarch gives six people 814 characters between them).

⚠️ **WHO IS LISTED IS THE QUEST CARDS' DECISION.** A character appears exactly when
`setup.pickQuestsCard(slug)` returns a card — the same call and the same gate `QuestsPage` makes.
Put the meeting flag on their cards (`the-first-hour.md` F8) and both surfaces reveal them in the
same instant; there is no second gate to keep in sync. The cost, stated plainly: **a character with
no quest card can never appear here.** The `guidance exists` gate already requires every `[[npcs]]`
entry to carry one, so this cannot happen in a game that passes its own scoreboard.

⚠️ **An off-schedule character is not a bug.** `getNpcLocation` returns null outside every declared
window and the card says so in a dimmed line. At 05:15 on a farm whose crew starts at 06:00, four
of five rows read *"Not about right now"* — correct, and the reason the away state gets its own
muted style instead of an empty gap.

The `castButton` widget is emitted **even when the block is absent** (as an empty widget), because
`StoryCaption` calls it unconditionally and SugarCube throws on an undefined widget — the same rule
`[ui.cheat_page]` records. And the button is wired into **both** `StoryCaption` branches: miss the
non-dev one and the page ships dev-only, which no gate would catch.

### `[[npcs]] tags` — the four-word line under the name

Optional, capped at **four** (`NPC_TAGS_MAX`), and inert in every
game that does not use it.

```toml
[[npcs]]
id           = "npc_hal"
name         = "Hal"
relationship = "Your landlord, 52. His name is the one on the lease."
tags         = ["The rent book", "The garden", "Sunday", "Strong tea"]
```

```
[face]  Hal
        Your landlord, 52. His name is the one on the lease.
        The rent book · The garden · Sunday · Strong tea
        📍 The back garden
        💡 …
```

**Why four, and which four.** The field's best cast page is `friends-of-mine`'s **Characterpedia**
(structure only; it fails the adults-only rule): fifteen people, each with a portrait, an encounter
counter, a 27–83-word biography, and **exactly four interests** — all fifteen, no exceptions, e.g.
*Manipulation · Attention · Writing · Oriental Food*.

The four slots are consistent: **how they operate · what they want · an aesthetic · something they
consume.** Thirteen of the fifteen end on a food or a drink, and **that trivial fourth slot is the
point** — it is what stops the entry reading as a stat block. Course of Temptation has the same
instinct in its 66-tag personality vocabulary, which ships *Vegan*, *Pescetarian*, *Stoner* and
*Retail Therapy* alongside the kinks.

*"Manipulation | Attention"* tells you Chloe is dangerous in two words, and her 39-word biography
never says so.

⚠️ **A cap that bites is the rule.** A fifth entry is rejected at import, not truncated. Four words
are a character sketch; six are a stat block, which is the thing the fourth slot exists to prevent.

⚠️ **`tags` does NOT ride `$npcs`.** It ships as a slug-keyed registry, `setup.npc_tags`, exactly
like `setup.npc_arc_stages` — because `$npcs` is snapshotted into **every history moment**, which is
the same reason `description` is popped at `v2.py:1098`. Do not "simplify" it onto `$npcs`.

⚠️ **`ai_behavior_config` IS WRITTEN IN TWO PLACES AND THE DEFAULT BUILD USES THE SECOND.**
`template_import.create_project_from_template` is the `--use-db` path; `game_graph.build_game_graph`
is the one a plain `package_from_toml` takes. **A per-NPC field added only to the first reaches the
database and never reaches a packaged game** — and the symptom is a silently empty registry with no
error at import, at build, or at runtime. This cost a debugging cycle on the day `tags` shipped;
`tests/test_npc_tags_field.py` now locks the no-DB path specifically.

**Not a substitute for design.** The tag line is a four-word compression of a corner of the world
the character already owns (`the-surfaces.md` R8). It cannot give one to a character who has none.

### One thing the field does on every line that we do not: colour

A **known difference. Nothing is built for it.**

In seven of twenty-seven field games the single most-used macro in the entire game is a
speaker-attribution component — `become-taxi-driver`'s `<<chat>>` **59,751** times,
`sluttown-usa`'s `<<nm>>` **37,379**, `destroyer`'s `<<speech>>` **30,640**, `lust-for-life`'s
`<<dg>>` **26,122**, `the-company`'s `<<nm>>` **19,379**. Each renders three things: a **face**, the
**name**, and a **colour unique to that person**.

- `sluttown-usa` — a 107-branch `if` chain, one CSS box class and one face file per speaker
  (`.karleeBox`, `.indiaBox`), and the face swaps on story state (`<<if $indiaToStarr is 1>>`).
- `become-taxi-driver` — three colour slots per person (border, background, name plate) plus a
  `$themes` toggle so the player can turn parts of it off.
- `lust-for-life` — `dialogColor` is a first-class field on the character object, beside `fontColor`
  and three separate name forms.

**We already ship two of the three.** `v2.py:16769` puts the portrait on every NPC dialogue block
and the name above it. What we do not ship is the third: the renderer emits one `dialog-npc` class for the whole cast (`v2.py:16808`).

**Do not build this on the strength of the count alone.** It is recorded so the next person does not
rediscover it as a gap; build it when a game asks for it.

---

## 34b. `[player_portrait]` — her face in the sidebar

A top-level table (`template_import.py:928-941`, parsed at `:3039`; `enabled` defaults to true when
the block is present). Keys: `default_image`, the undress states `naked_image` / `topless_image` /
`bottomless_image` / `underwear_image`, `pregnancy_trait` with `pregnancy_suffix` (default `Preg`), and
`[[player_portrait.outfits]]` rules (`image`, `when` on worn type, corruption or a flag). It renders
as the sidebar widget `<<playerPortrait>>` (`v2.py:18837`), resolved by `setup.getPlayerPortrait`
(`v2.py:1829`).

⚠️ **It renders only with `clothing_enabled = true`.** `getPlayerPortrait` is emitted inside the
clothing block (`v2.py:1641`), an engine limit. `templates/board.toml` sets both. One performer or one
look, kept across the game: `the-want.md` §6.

## 35. `block_pool` — the variant pool, and the field's main mechanism for a re-read surface

**The engine has had this since v2 shipped.**

```python
v2.py:16312   if block_type == "block_pool":
v2.py:16313       pool_blocks = (block.get("props") or {}).get("blocks", [])
v2.py:16328       parts = [f'<<set _bp to random(0, {max_idx})>>']
v2.py:16329-16337 # if / elseif / else chain over the variants
```

**It picks a different one of N blocks on every render.** Not once per game, not once per day —
every time the passage draws. Re-enter the surface and the sentence is different.

| fact | source |
|---|---|
| children live at **`props.blocks`** | `v2.py:16313` |
| a **one-item** pool renders directly, no `random()` | `v2.py:16315-16317` |
| variants may be **any block type** — the pool nests `_convert_blocks_to_game_html` | `v2.py:16317`, `:16336` |

```toml
# BOTH SHAPES PARSE. Children at the block's own `blocks` key:
{ type = "block_pool", blocks = [
    { type = "paragraph", content = "…first variant…" },
    { type = "paragraph", content = "…second variant…" },
    { type = "paragraph", content = "…third variant…" },
] }

# Identical after import. The generator reads props.blocks either way.
{ type = "block_pool", props = { blocks = [ … ] } }
```

### The four authoring facts, verified in the importer

`template_import.py:7748-7776` normalises both container types side by side, so the rules are the
same ones `group` follows — with one exception that is not.

| | |
|---|---|
| children may sit at **`blocks`** OR **`props.blocks`** | `:7574` — `b.get("blocks") or props.get("blocks")`, the same both-shapes read `group` gets at `:7563` |
| **a `block_pool` directly inside a `block_pool` is silently dropped** | `:7579` — `inner_safe = [ib for ib in inner_safe if ib.get("type") != "block_pool"]`. A random pick of a random pick is ambiguous and the restriction is deliberate. **Unlike `group`, which MAY nest in `group`** (`:7567-7571`, the same-type-skip rule was removed 2026-05-17) |
| **mixed child types only WARN** | `:7583` — `logger.warning("block_pool has mixed types …")`. It builds. Same-type children are the intent, and the warning is in the build log, not the game |
| nesting depth is capped at **4** | `:7492` — a `group` wrapping a pool wrapping a group is depth 3, so 4 is a ceiling rather than a limit you will meet |

⚠️ **A pool is an exclusive axis and the scoreboard now reads it as one.** The **beat**
collector still folds every variant together on purpose, and that is correct: see the folding
argument below.

### A pool that remembers — `memory = "seen"` (E2, 2026-10-01, opt-in)

```toml
{ type = "block_pool", props = { id = "shower_events", memory = "seen", seen_weight = 0.1, blocks = [ … ] } }
```

An entry already shown weighs `seen_weight` (default 0.1, range (0, 1]) against 1 for a fresh one
(`setup.pickRememberedPoolEntry`, `v2.py:5517`), so she sees every entry before the repeats pile
up. The pool emitter branches on `memory` at `v2.py:16321`. Seen counts live in `$game_state.pool_seen[key]`, which is in the
skeleton only when a game has such a pool (`v2.py:1534`). The key is `id`, else a hash of the
entries (`v2.py:13690`): editing an id-less pool's text resets its memory. The keys may sit at the
block's top level or in `props` (`template_import.py:7780`).

**A random canvas** takes `trigger.seen_weight` (random mode only): once it has fired, its `chance`
is multiplied by it (`setup.canvasRollChance`, `v2.py:5503`). Misuse is a build error
(`template_import.py:6753`).

### Why this section exists

Three of the four top female-PC games in the corpus build **every repeatable sexual surface** this
way, and none of them writes such a scene as a paragraph
(`~/Documents/Female_PC_Craft_Study_20260823/findings_D_writing.md`):

| game | its mechanism | scale |
|---|---|---|
| Course of Temptation (rank 5) | `<<switch setup.rir(0, 3)>>` | 164 named acts × 3 phrasings, one passage of 194,874 chars |
| Family Ties (rank 24) | `either("…", "…", …)` | 12 poses × ~10 narration lines + ~10 of his dialogue |
| Degrees of Lewdity (rank 7) | a **deterministic** grid on two meters — see `register.md` | 99 `actions*` widgets |

### ⚠️ We did not fail to discover this. We KNEW IT AND LOST IT.

v1's corpus carried a whole numbered rule for it — `prompts/game_design_rules.md:1330`,
**Rule 17: Block Pools for Repeatable Activities** — and it named the failure precisely:

> "This prevents the **'same text every morning' problem** that makes daily activities feel dead.
> […] The group block system handles phase changes (post-first-kiss vs default), but **WITHIN each
> phase, the text is frozen.** Block pools add variety within phases."

That distinction is R6's mechanism 4 vs mechanism 5 in `the-surfaces.md`.

**How it was lost:** v2's skill was deliberately divorced from `prompts_v2/` because that corpus
taught false engine facts. In cutting away the false ones, this true one went with them — and the
v2 skill mentioned `block_pool` exactly once, inside a list of valid block types, for its whole
life. **The lesson is about the divorce, not about the primitive:** a wholesale cut loses the good
with the bad, and nothing checked what was in the discarded half.

### Two authoring constraints, from v1's schema doc

`prompts/toml_generation_prompt_v4.txt:1044-1053`:

- **All child blocks must be the same type** (paragraph, dialog, or group). Use a `group` inside the
  pool for multi-block variants.
- **"`block_pool` CANNOT be nested inside another `block_pool`."**

⚠️ The nesting constraint is **stated by v1's schema doc and NOT verified against `v2.py`** — treat
it as unverified and do not cite it as an engine fact. The plausible mechanism is that both pools
emit the same `_bp` temp variable (`v2.py:16328`), but whether SugarCube's already-matched
`if/elseif` chain actually breaks on the collision was not tested. **Do not nest until someone
tests it.**

### ⚠️ The gates fold every variant into one beat, and that is CORRECT

`scripts/gates.py:464-475` collects a pool's children into the **same** `Beat` object, so ten
30-word variants count as one 300-word beat. That looks wrong and is not. `Beat`'s own docstring
(`gates.py:398-405`) gives the reason: a Twine passage carries all its `<<if>>` branches inline, so
folding keeps our numbers comparable to the baseline the thresholds came from.

Measured 2026-08-23 across ten Degrees of Lewdity location passages, to check rather than assume:

```
ten named location passages: 9,886 words · unconditional 234 · IN A BRANCH 9,652  (98%)
```

⚠️ **Read that as ten passages, not as the whole game.** It is a spot check of
ten named locations — not a per-location total of the kind `location fill` computes. It is
lopsided enough (234 words out of 9,886) to settle the question it was asked, and it is **not** a
figure to quote as "DoL is 98% conditional".

The `location fill` threshold was derived from that same source (116,540 words across 25
locations — `CHANGELOG.md:15841`), so counting our variants the same way **is** the apples-to-apples
comparison. Changing it would break the only baseline the gate has.

Where the folding does distort, it distorts **conservatively**: ten explicit variants fold to *one*
explicit beat, which makes `explicit floor` harder to reach, never easier.

⚠️ **Do not "reconcile" this with `register.md`'s 25-game table**, which counts *one rendered path,
not every branch*. That is a different instrument for a different question — per-screen word counts,
where a passage printing the same four words over eight images must count as four words. Both are
right for what they measure.

### ⚠️ Randomise the WORDS. Never randomise the CONTENT.

A pool varies how a beat is phrased. It must never decide **whether the player can reach
something**. The distinction is not ours — it is what the field's players draw themselves. Course of
Temptation's players resent the dice (*"the rng aspects of this game should be seriously toned
down"*, 11 likes) while nobody anywhere complains about varied phrasing; the complaint that keeps
recurring is the opposite one: the same pictures every time you do the same thing
(`zaras-school-life`'s top-liked criticism, paraphrased). Measured 2026-08-23 across 3,479 comments —
`~/Documents/Female_PC_Craft_Study_20260823/findings_J_players.md` §7.

A `block_pool` whose branches carry different `flagEffects`, different `traitEffects`, or different
exits is a dice roll on content wearing a pool's clothes. Vary the sentence; leave the consequence
alone.

### Where the rule lives

`the-surfaces.md` R6 mechanism 5 (a screen moves on re-entry) · `register.md` (how to write the
variants).

---

## 36. The rejection branch — a locked choice that is still clickable

A choice whose `conditions` fail has **two** shapes, and the second one is the engine's answer to
*"what happens when she tries anyway."*

| mode | set | renders as | on click |
|---|---|---|---|
| **A — the wall** | `show_when_locked = true` | greyed out, label = `locked_text` or the choice text (`v2.py:14854`) | nothing, or a threshold toast if `locked_text_threshold` is set (`v2.py:14915-14922`, §23); a number lock shows its need (§15) |
| **B — the rejection** | `rejection_node` | **a live link**, label = `locked_text` or the choice text | goes to that node and applies `rejection_effects` |

The generator names Mode B itself —
`# Mode B: Clickable rejection — redirects to rejection node` (`v2.py:14856`), entered from the
`if rejection_passage:` branch at `v2.py:14855` (`rejection_passage`
is the generator's internal name for the field authors write as `rejection_node`). The node id is resolved against `passage_name_map` at `v2.py:15399-15403`, which
logs a warning rather than failing the build if the target does not exist, so **a typo here is
silent in the game and visible only in the build log.** Effects are emitted at `v2.py:14859-14879`
through the same `setup.pendingEffects` path a normal choice uses.

Both fields live on `TemplateChoice` (`apps/projects/services/template_import.py:1003-1004`, in the
class at `:980`), beside `conditions`, `show_when_locked`, `locked_text` and
`locked_text_threshold`, and are read from the TOML at `:2514`.

⚠️ **`rejection_node` IS build-validated, contrary to what the paragraph below used to imply.**
`template_import.py:5544-5549` raises when it names a node that is not in the same canvas — so a
typo fails the build with a message naming the canvas and the choice index. The fail-open warning
described below is the generator's later slug→passage resolution, which only sees ids the importer
has already accepted.

### A recovery, not a discovery

`locked_text_threshold` was already documented (§23). **`rejection_node` was not documented
anywhere in this skill** — a working primitive that nothing taught, so nothing used.

### What it is for — the field's refusal

Course of Temptation resolves a refusal instead of granting it. `EventWalkPassHF`: an NPC gropes
her in the street, and *"Refuse to respond"* routes two ways —

```
<<set _diff to $pc.resist_arousal_difficulty($eventnpc)>>
<<link "Refuse to respond">>
    <<if $pc.skillcheck("Willpower", _diff)>>  <<go EventWalkPassHFResist>>
    <<else>>                                   <<go EventWalkPassHFResistFail>>
<</link>> <<skillcheck Willpower _diff>>
```

- **succeeds** — `Composure +25`, and his `control` over her **−25**: *"It's good to know he can't
  get to you quite so easily."* (354 chars)
- **fails** — `Arousal +100`, `Humiliation +50`, his `lust +25`, his `control` **+25**:
  *"So easy."* (629 chars)

Not one event: **464 `skillcheck` branch calls** across the game, **41** passages named `*Resist*`.
Degrees of Lewdity carries the same principle across **360** struggle/resist/escape passages.
Measured 2026-08-23 — `findings_H_known.md` and `findings_J_players.md` §4.

### ⚠️ Ours is deterministic, and theirs is a roll

**This engine has no per-choice random outcome.** `conditions` has no `random` type — the
*"flag/trait/random"* list at `template_import.py:3662` is a docstring, not a feature — and the only
randomness available is `trigger_mode = "random"` (whether a canvas fires at all) and `block_pool`
(which words render). A choice goes where its conditions send it.

That difference is smaller than it looks, because the field **publishes the odds before the click**:
`<<skillcheck>>` renders a word next to the label — `certain · trivial · easy · moderate ·
demanding · hard · very hard · nearly impossible` (`skillcheck_descriptor`), used **314** times.
A dice roll the player can see and accept is not the RNG their comments resent (§35).

> A published *threshold* keeps the same promise a published *probability* does: **the player knows
> what they are risking before they click.** Say the bar out loud: in the label on a `rejection_node`
> lock (Mode B shows only the label, `v2.py:14858`), or the engine's suffix on a Mode A number lock.
> Do not simulate a roll.

### The authoring shape

```toml
[[canvases.nodes.choices]]
text                  = "Tell him no (Nerve 40)"   # Mode B shows only this label: the bar goes here
conditions            = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "nerve", operator = "gte", value = 40 },
] }
show_when_locked      = true
rejection_node        = "node_told_him_no_failed"
rejection_effects     = [ { targetType = "player", trait = "known", op = "add", value = 4 } ]
```

Four rules the field follows, all of them cheap:

1. **Both branches are written, and both are paid** — in opposite directions on **one** meter, so
   the attempt is a real wager rather than a coin with one face.
2. **Who is pushing sets the bar.** CoT reads the difficulty off the NPC
   (`resist_arousal_difficulty($eventnpc)`); ours does it with a per-NPC trait condition (§8,
   `subject = "npc"`), so the same refusal is easy against one character and hard against another.
3. **Keep the branches short.** 354 and 629 characters in the field. A refusal that costs a whole
   scene to write is one you will only build once.
4. **Never fail silently.** If she can try and lose, the bar is stated before the click.

### Where the rule lives

`the-surfaces.md` R5b (the decline branch is written at full length and pays).

---

## 37. FOUR condition evaluators, and they do not agree by default

The real architecture is below, and it is the load-bearing fact:

| evaluator | backs | `ne` |
|---|---|---|
| `compare()` — `v2.py:4355` | canvas / node / choice `conditions` | **yes**, since v2 shipped |
| `setup.describeUnmetConditions` — `v2.py:4225`, trait switch `:4248`, phrases `:4259` | the *why is this locked* text on a blocked choice | **yes** |
| `setup.checkSingleCondition` — `v2.py:8259`, trait branch `:8271`, `ne` at `:8293` | hints, quest-card *goal* bullets, `_findFlagSetterCanvas`, ten-plus call sites | **yes** |
| `setup.checkQuestsCondition` — `v2.py:17083` | `[[quest_cards]]` `when` and `goals` | **no, deliberately** |

`compare` is reached first from the trait branch at `v2.py:4446`.

**Anything added to one has to be checked against the other three.** That is the rule this section
exists for; `ne` is just the case that exposed it.

### The four sets, counted 2026-08-29 — and they still do not agree

On a **trait** condition:

| evaluator | operators on a trait |
|---|---|
| `compare()` | `eq` `ne` `gt` `gte` `lt` `lte` `in` `not_in` `contains` `not_contains` `exists` `not_exists` — **12** |
| `describeUnmetConditions` | `eq` `ne` `gt` `gte` `lt` `lte` — **6** |
| `checkSingleCondition` | `eq` `ne` `gt` `gte` `lt` `lte` — **6** |
| `checkQuestsCondition` | `eq` `gt` `gte` `lt` `lte` — **5** |

⚠️ **`ne` is fixed and six operators are not.** `in`, `not_in`, `contains`, `not_contains`, `exists`
and `not_exists` pass `compare()`, so a canvas gate using one **works** — and every other reader
falls through to `return false`. The same condition item is therefore true on the door and false in
the *why is this locked* line, in every hint, and in `_findFlagSetterCanvas`. This is the exact
shape `ne` had before 2026-08-24, still live, times six.

**Not fixed here.** (Type-specific operators — `is_true`, `is_false`,
`is_present`, `equipped`, `owned`, `is_active` and their negations — are their own branches and are
not part of this comparison.) Recorded so the next person adding an operator counts real usage before
the code, and so a game that reaches for `contains` is recognised as the first real demand rather
than as a mystery.

⚠️ **`setup.describeUnmetConditions` is the fourth evaluator**, with its own operator chain and
phrase table. The comment beside `checkSingleCondition`'s `ne` line (`v2.py:8287`) still says "THE
SECOND EVALUATOR": read this table, not that comment, before adding an operator.

### What was actually broken, and what was not

**Until E1 (2026-10-01) a canvas condition's operator was not validated by the importer.** An
unknown operator imported clean and failed **closed** in `compare()`. The importer now rejects it
(§2). `ne` was always writable on a canvas gate and always worked there.

What did not work: the **same condition item** read through `setup.checkSingleCondition`, whose trait
branch ran `gte / gt / lte / lt / eq` and then `return false`. A `ne` gate was therefore true on the
canvas and false in every hint and flag-setter lookup that touched it. One line, now fixed.

The second half was cosmetic and worse than it sounds. The requirement-label formatter
(`setup.formatCanvasConditions`, `v2.py:8504`, operator map at `:8519`) mapped an unknown operator to `"≥"`, so a `ne` gate rendered as *"Elena Affection ≥
50"* — the game stating the opposite of its own rule. Now `"≠"`.

```toml
# Legal today. "She is not at stage 3" — the negated form of the field's
# commonest gate shape (the-surfaces.md R5d).
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "loop_stage", operator = "ne", value = 3 },
] }
```

### ⚠️ Quest cards reject `ne` on purpose — do not "fix" the whitelist

`[[quest_cards]]` conditions **are** whitelisted (`template_import.py:6957`, `gte/lte/gt/lt/eq`) and
their evaluator, `setup.checkQuestsCondition`, has no `ne` case — its `switch` falls through to
`return false`. Widening that whitelist without adding the case would let an author write a card
condition that is **silently always false**, which is the failure this engine has had before with
`conditions` lacking `version = "1.0"`.

Widening it correctly means the whitelist **and** the evaluator, in the same change. The comment at
`template_import.py:6950-6957` says so at the site.

Also unchanged, and for the same reason — each is its own path:

- `template_import.py:6159` — hint `trait_checks`.
- `template_import.py:6086`, checked at `:6109` — hint-template `stage_op`, `{eq, gte, lte}`.
- `template_import.py:7325` — a **heuristic** threshold reader, not a validator. `ne` is not a
  threshold and does not belong there.

### ⚠️ The v1 rollback path

`generators/v1.py` is frozen and carries its own `compare()` with `ne`, but not this fix to
`checkSingleCondition`. **A game that uses `ne` and is rebuilt with `--gen-version v1` for safe-mode
rollback will diverge** — the canvas gate holds, the hints do not. v1 is not patched; per `CLAUDE.md`
it is rollback-only and slated for deletion.

### Where the rule lives

`the-surfaces.md` R5d (a gate asks one of two questions).

---

## 38. `[project] version` / `release_date` — the sidebar footer, and the only number the player can quote

`the-release.md` § Shipping the build requires this field.

Both keys are **optional** and live in `[project]`, alongside `id` / `title` / `starting_canvas`:

```toml
[project]
version      = "0.1"
release_date = "2026-08-23"
```

The path from the TOML to the screen, traced end to end:

| step | where |
|---|---|
| read off `[project]`, defaulting to `""` | `template_import.py:2088` |
| copied onto the project's metadata | `template_import.py:7860` |
| escaped, then joined with ` · ` | `v2.py:17949-17950`, joined at `:17952` |
| composed into the `versionFooter` widget | `v2.py:17957-17960` |
| called unconditionally from `StoryCaption` — both variants | `v2.py:17980` and `:17995` |

Rendered as `v0.1 · 2026-08-23` in a `<div class="sidebar-version">` under the sidebar.

**Three facts that matter and are not guessable:**

1. **The widget is ALWAYS defined, even when both keys are empty** — it just renders nothing. The
   ternary at `v2.py:17957-17960` emits an empty `<<widget "versionFooter">><</widget>>` rather than
   nothing at all. Deliberate: SugarCube throws on a call to an undefined widget, and `StoryCaption`
   calls it unconditionally in both its variants (`v2.py:17980`, `:17995`) — same reason the
   cheat-page and cast-page widgets are emitted outside their own feature blocks.
2. **`html.escape` runs on both** (`v2.py:17949-17950`), so a stray quote in a date string cannot
   break the build.
3. **There is no build badge.** There is one build, and what a player needs to identify is the
   RELEASE — it is what their guide's codes are scoped to. The version string does that here and in
   the cheat page's heading (`v2.py:17953-17955`).

### Why it is not cosmetic

This is the **only** release identifier a player can read without leaving the game, so it is one of
the three places that claim to say what shipped — with the portal's `version` and the archive under
`games/<slug>/releases/`. `gates.py --release` checks that all three agree.

### Where the rule lives

`the-release.md` § Shipping the build, step 4.


---

## 39. `time_of_day` — the hour window, and the only predicate that is a window rather than a latch

```toml
{ type = "time_of_day", start_time = "22:00", end_time = "06:00" }   # overnight, wraps midnight
{ type = "time_of_day", start_time = "11:00", end_time = "20:00" }   # ordinary daytime window
{ type = "time_of_day", start_time = "18:00" }                        # no end ⇒ exactly one hour
```

The runtime branch is at `v2.py:4572`; its lock text at `:8600`. `HH:MM`,
24-hour, **end exclusive** — `11:00`–`20:00` is false at 20:00 exactly.

**It delegates.** The branch is four lines and calls `setup.isCurrentTimeSlot`
(`v2.py:4158`) — the same function NPC and location schedules have used since the schedule
primitive shipped. It does not parse hours of its own, so **the overnight wrap has exactly one
implementation** and there is no second copy to drift from the first. That wrap is the trap here: a
hand-rolled `current >= start && current < end` passes every daytime case and fails every window
that crosses midnight, silently.

**Why it exists.** Measured across 27 shipped sandboxes
(`~/Documents/Phone_System_Study_20260829/`), gating content on an hour window is the field's
**second most common mechanism — 20 of 27 games** — behind only a meter gate at 22, and it was the
one item in that list this engine could not express. Locations and NPCs reached the clock through
their `[[schedules]]` rows; a canvas trigger and a phone conversation had no route to it at all, so
"only in the evening" had to be faked by setting a flag from something that does touch the clock.
`the-phone.md` P4.

⚠️ **It is a window, not a latch, and that distinction is the whole reason to prefer it over a
flag.** The predicate is re-evaluated on every read, so it is true only while the clock is inside
the range. **A conversation's delivery, however, still latches** —
`ps.triggered_conversations[conv.id]` (`v2.py:2299`) is written the first time the trigger passes
and never re-read. So on a phone conversation this predicate means *"deliver this the first time she
is awake at 2am"*, not *"this thread only exists at 2am"*. On a canvas trigger, which is evaluated
fresh, it means the second. **Know which surface you are on.**

⚠️ **No weekday form.** `[[schedules]]` rows carry a `weekdays` list; this predicate does not. "Only
on Saturday" is still unbuildable as a condition. Not measured, so not built.

⚠️ **Unlike every `worn_*` predicate it carries no `_enabled` guard**, and must not grow one — the
clock is initialised in every build (`time_state` in `$game_state`), including builds with no
schedules, no phone and no clothing.

**Verified live in a built game, not just read.** Ten cases through a real browser against
a built game rebuilt with an overnight condition on a phone conversation: 23:00 and 02:00 inside
`22:00`–`06:00` both true; 21:59, 06:00 and 12:00 false; an ordinary `11:00`–`20:00` window true at
13:00 and false at 20:00 and 10:59; a bare `18:00` true at 18:30 and false at 19:30. Lock text
rendered as `Required: Only between 22:00 and 06:00`. Tests:
`apps/game_generation/tests/test_time_of_day.py`, 11 of 11.

---

## 40. The save-migration seam — what a new release does to an old save

`:: Start` runs once, when a playthrough begins. **SugarCube never re-runs it on load.** So every
default a new release writes there — a flag, a meter, an NPC, a whole system — is `undefined` in
every save that predates it, and the first read throws. The seam that repairs this is the engine's,
not the author's, and knowing its exact reach is the difference between a safe release and a
soft-lock. The authoring rules that follow from it are `references/the-returning-player.md`.

**The skeleton is one object.** `$player` and `$game_state` are serialized into `:: Start` from the
same Python dicts that are handed to `setup.stateDefaults` (`v2.py:3432`), so the defaults cannot
fall behind what a fresh game starts with. They used to be two hand-maintained string blocks and a
three-key dict, which is exactly how turning the phone on in a patch release left
`$game_state.phone` undefined in every existing save with no build error anywhere.

**`setup.backfillStateDefaults`** (`v2.py:17635`) is called from the `:passagestart` handler
(`v2.py:17788`) on **every passage**. It fill-if-absent merges the defaults into `State.variables`,
never overwrites an earned value, is idempotent, and hands out deep copies so a player's state can
never alias the shared default object.

**The depth is not uniform, and the asymmetry is load-bearing:**

| | depth | why |
|---|---|---|
| `$flags` | keys | — |
| `$npcs` | whole NPC, then `core_traits` / `flags` | a missing NPC arrives entire |
| `$game_state` | top level **and one level into a sub-map** | every non-empty default there is engine bookkeeping (`phone`, `rent_state`, `fast_jobs`, `bank`, `time_state`); the player-owned maps all default to `{}` so there is nothing to fill into them (`pool_seen`, E2, is one, present only in a game with a `memory = "seen"` pool) |
| `$player` | **top level only**, plus `core_traits` by name | `$player.wardrobe` is an id → garment map — a deeper fill hands back a garment the player sold. Same for `equipped`. |

Arrays are never merged at any depth: a default `[]` would re-seed a list the player emptied.

⚠️ **What it cannot do.** Follow a rename, notice a removal, reinterpret a rescaled number, or
re-grant something the save already consumed. Those are `the-returning-player.md` §§2–6.

**Provenance.** `$game_state` carries `origin_version` / `origin_schema` (the release the playthrough
started on, written once by `:: Start`, never overwritable because the backfill only fills absent
keys) and `last_version` / `last_schema` (the release currently running, restamped by
`:passagestart`). ⚠️ `origin_*` is the **one deliberate divergence** between `:: Start` and
`setup.stateDefaults`: the defaults carry `null`, so a save written before the stamp existed reads as
*unknown* instead of being relabelled as having started on whichever build first migrated it.

**The stamp and the hook.** `Config.saves.id` (`v2.py:3396`) is pinned to the template slug rather
than the SugarCube default `slugify(StoryTitle)`, so a title change does not orphan **exported**
saves — the in-browser slot namespace is still title-derived and still strands
(`SimpleStore.create(Story.domId, …)` in `format.js`). `Config.saves.version` (`:3391`) is a sha1
over the trait/flag key surface and the corruption tiers. `Config.saves.onLoad` (`:3412`) compares
it and **logs**; it does not refuse. A `throw` there would abort the load with `UI.alert` — that is
the reject-on-mismatch handler, deliberately unused.

⚠️ **The story format is SugarCube 2.30.0, and it is not installed with the compiler.** Tweego
loads it from a `storyformats/` directory beside its own binary, so `tweego --version` cannot see
it: replace `storyformats/sugarcube-2/` and every future build ships a different runtime with the
compiler reporting exactly what it reported yesterday. `game_service.py` pins both
(`EXPECTED_TWEEGO_VERSION = "2.1.1"`, `EXPECTED_SUGARCUBE_VERSION = "2.30.0"`) and warns —
loudly, never fatally — when either moves.

It matters here because the save hooks were rewritten between 2.30 and 2.36: 2.30 has
`Config.saves.onLoad` / `onSave`, and **`Save.onLoad.add()` does not exist**. Write against 2.30 and
verify against the installed `format.js`, not against a version string in a file.

> **Fixed 2026-08-29, and worth knowing as a shape.** `StoryData` had declared `"format-version":
> "2.36.1"` since the generator was written, against an installed 2.30.0. It was inert for us and
> only for us: the packager compiles with `-f sugarcube-2`, which overrides StoryData outright.
> Anyone compiling the same Twee any other way — by hand, from Twine — got a hard error, *"Story
> format named \"SugarCube\" at version \"2.36.1\" is not available"*, and every build carried the
> false number into its `:: Story [meta]` passage. Two constants said 2.30.0, one string said
> 2.36.1, and nothing compared them for months.

Tests: `apps/game_generation/tests/test_save_migration.py`, 24 of 24 — which execute the emitted
migration in node against synthetic old saves rather than grepping for it.

---

## 41. Five facts a build cost one round each, 2026-08-31

All five surfaced translating a signed design into TOML. Each cost exactly one
build or one gate run, and none of them is guessable from the schema.

### 41a. `op = "sub"` parses, imports, builds — and does nothing

`applyTraitEffect` runs `['add', 'set']` and nothing else (`v2.py:6496-6503`). A `sub` effect is
valid TOML, survives the importer's dataclasses, reaches the generator and is discarded at runtime.

**To take something away, write `op = "add"` with a NEGATIVE value.** A quantity like `money` also
needs `clamp = false`, or the default 0–100 clamp (`v2.py:6506-6508`) eats it.

⚠️ Nine canvases shipped this in one pass. **Every energy cost in the game would have been free.**
The importer's own validator now catches it with the fix in the message — which is the good version
of this — but nothing about the TOML looks wrong.

### 41b. Quest-card conditions use `trait`; canvas conditions use `trait_key`

Same word "condition", two parsers, two key names:

```toml
# a CANVAS condition
{ type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 12 }

# a QUEST CARD condition — `trait`, and `op`, not `operator`
{ type = "trait", subject = "player", trait = "corruption", op = "gte", value = 12 }
```

`template_import.py:1229` is the quest side. Writing `trait_key` in a quest card fails validation
with *"condition item must set one of `flag`, `trait` or `days_since_flag`"*
(`template_import.py:6902`), which names the key it wants and gives no hint that the other half of the
same file uses a different one.

### 41c. A quest goal needs a `label`; every card needs a `when`

- `goals[]` items are refused without `label` — *"it renders next to the ◯ bullet"*.
- A card with no `when` is refused outright: *"Every card must scope itself to a state-window."*

Both are hard validation failures, and both come after 41b, so a first quest-card block typically
costs three build rounds rather than one.

### 41d. `hide_value` does not keep a trait out of the dump

The suppression is `[[traits.labels]] in_dump = false` (or `hidden = true`, the secret-trait switch)
and nothing else — §30 above says so, and it is worth repeating here because the wrong key is the
obvious guess. `hide_value = true` only drops the number from a `trait_bar`'s own label
(`v2.py:18614`); the auto Traits dump keeps printing the bare number under the band.

### 41e. `_is_free` reads the TRIGGER, never the inner choices

Not an engine fact but a scoreboard one, and it belongs beside them because it costs the same rounds.
`_is_free()` (`gates.py:5238`) decides a rung is farmable from **the way in**: `trigger.costs`,
`trigger.max_triggers_per_day`, or a day-cap flag condition on the trigger whose setter sits on a
choice inside.

> *"Min over routes, never max: one unbraked door makes the whole rung farmable, no matter how well
> priced the other doors are."*

⚠️ Three rounds of `the climb is paid for` were spent adding `costs` to choice after choice with no
movement. Moving the same costs onto the triggers cleared five meters at once. See `the-sheets.md`
S9 — the sheets imply the brake is a property of the rung, and it is a property of the door.

---

## 42. `trigger.npc` — the portrait, and the presence gate it carries

One key decides whether a character surface is a **face on the location screen** or a **line of link
text**, and the same key is what enforces that character's hours. It lives at the top level of
`[canvases.trigger]`.

```
[[canvases]] npc = …            → dropped. TemplateCanvas has no such field
                                  (template_import.py:1059-1066, built named-only at :2719-2727)

[canvases.trigger] npc = …      → TemplateTrigger.npc (template_import.py:755)
                                  → game_graph.py:344  "npc" into trigger metadata
                                  → v2.py:12761        read back out
                                  → v2.py:12836        "npcId": npc_id,  # NPC slug for navigation portrait indicators
```

**With `npcId`** — `selectNpcPortraitCanvasesForLocation` (`v2.py:5135`) and `renderNpcPortraits`
(`v2.py:5678`) claim the canvas. The renderer then applies the only real presence check in the
engine: the character must have a declared `[[npcs.schedules]]` and `getNpcLocation` must put them
where the player is standing right now (`v2.py:5741-5744`). It draws the portrait and prints
`$npcs[…].name`.

**Without it** — `renderSoloActivities` does not skip the canvas (`v2.py:5824` skips only canvases
that *have* an `npcId`), so it renders as an ordinary activity button carrying the canvas's own
`displayName` (`v2.py:5855`). No face, **no presence check at all**, and the author-facing title
becomes player-facing text. `requires_npc` does not cover the gap unless it is set — §31 above lists
every site that reads it.

⚠️ **One location shows ONE canvas per character.** The renderer gathers every valid repeatable
canvas per NPC and keeps the highest `priority`, preferring affordable over cost-blocked
(`v2.py:5685-5722`). Three Mark surfaces in one kitchen render as one Mark, not three rows. Set the
priorities deliberately: an escalation at 7 above a hub at 6 replaces the hub whenever its conditions
hold, which is usually what you want and is never what you get by accident.

⚠️ **A non-repeatable canvas renders no portrait either** (`v2.py:5143` skips
`!c.isRepeatable`), which is what keeps a meeting from leaking onto the screen as a face — see
`the-first-hour.md` F5b.

**What the misplacement costs.** `npc` written on `[[canvases]]` instead of `[canvases.trigger]`
is discarded: every such entry in the built `help_data.locationCanvases` carries `npcId: null` and
`canvasIdToNpcUuid` is `{}` — no portraits, ungated surfaces, and `Sit with @npc` as a link label.
The build stays green, and the gate that checks hubs (`every hub is met first`) starts by counting
portrait hubs, finds none, and reports **n/a**. The gate `no canvas key is discarded` exists so
that cannot recur. It covers every canvas key, not `npc` alone: `substitution_only` written one
level too high renders a walk-in as a clickable activity instead of a dispatcher-only target.

---

## 43. Where `@` tokens resolve, and where they do not

`@player`, `@player.<field>`, `@<npc>` and `@<npc>.rel` are resolved by
`_resolve_at_references` (`v2.py:16160`), its link-text twin `_resolve_at_references_expr`
(`v2.py:16207`), and `setup.resolveAtRefs` at runtime. **These surfaces, and nothing else:**

| resolved | site |
|---|---|
| block `content` — paragraph, heading, dialog, thought_bubble | `v2.py:16715` |
| choice `text` | `v2.py:14724` |
| `locations[].description` · `description_variants[].text` | `v2.py:10764` · `:10788` |
| a door's `description`, option `text` and `locked_text` | `v2.py:10524`, `:13747`, `:13749` |
| `npcs[].role` — the label under the name | `v2.py:16803` |
| every phone surface; `story_arc` emotion ranges | runtime, `v2.py:2304-2735`; `:7077`, `:7089` |
| ⚠️ `locations[].blocked_message` — **half** | resolved in the room (`v2.py:10431`), raw in `setup.locations` (`:1050`), which the nav card prints (`:5451`) |

Every other author string is emitted verbatim. The ones that reach a player:

| NOT resolved | where it shows up |
|---|---|
| `locations[].name` | the room heading and every nav card |
| `canvases[].name` | the solo-activity link label, the quest card's `canvas_name`, the canvas `<h2>` |
| `npcs[].description` | the CustomizeCharacters screen — the game's **first** screen (customizable NPCs only; for others it renders nowhere) |
| `npcs[].tags[]` · `.relationship_options[]` | the cast page (`v2.py:3530`) · the relation picker (`:926`) |
| `quest_cards[].text` · `.tip` · `.ready_text` · `.terminal_text` | the guidance page |
| `traits.labels[].label` · choice `locked_text` | the sidebar (`v2.py:3479`) · a locked choice (`:14854`) |
| `canvases[].description` | dev surfaces only (`CanvasReview_*`, the `--debug` canvas banner) |

⚠️ **`npcs[].role` resolves `@` tokens.** A `customizable` NPC with `relationship_options` is one the
PLAYER decides the relation for, so its label has to be theirs: `role = "@<npc>.rel"` prints the option
they picked and follows a change. Escape first, then resolve — `html.escape` touches no character the
token regex reads. `the-first-hour.md` F10.

**The rule: a token belongs in prose. Anywhere else, write the role.** `"His son"` and
`"Sit with him"` survive a rename; `"@npc's son"` and `"Sit with @npc"` print the token.

⚠️ **This bites hardest exactly where customization is on.** `v2.py:9914` emits a name textbox for
every customizable NPC unconditionally, so those characters *must* be referred to by token in prose —
which trains the author to reach for `@npc` everywhere, including the four fields above.

> **Linted as `a token the engine never resolves`**, walking every field and nested list, dev-only
> fields apart, list fields included. A player-facing one is the `--ship` BLOCK row **no raw token
> on screen**.

---

## 44. The door — `[locations.door]`, a threshold she lands on instead of the room

Opt-in and **inert when unauthored**: a game that declares no door builds
byte-identical output, verified over 27 builds. `the-map.md` R6–R6c owns *when* to use one; this
section is the mechanism.

```toml
[[locations]]
id   = "the_back_bedroom"
name = "Mark's Room"

[locations.door]
description = "The door at the back of the house."
no_answer   = "You knock. Nobody comes to it."
# optional, same shape and same evaluator as [[locations.description_variants]]
description_variants = [ { conditions = { version = "1.0", ... }, text = "..." } ]

[[locations.door.options]]
text       = "Knock."
conditions = { version = "1.0", logic = "AND", items = [
  { type = "npc_at_location", location_id = "the_back_bedroom", npc_id = "npc_mark",
    operator = "is_present" },
] }
goes_to    = { type = "canvas", canvas_id = "mark_knock" }

[[locations.door.options]]
text             = "Go in."
show_when_locked = true
locked_text      = "You have got as far as the handle twice."
goes_to          = { type = "enter" }
```

```
template_import.py   TemplateLocation.door · parsed beside entry_conditions · validated in validate()
game_graph.py        loc.properties["door"] — THE PATH A REAL BUILD TAKES
v2.py                setup.locations[slug].door · _render_door_passage · setup.renderDoorOptions
                     _location_entry_passage · isRerenderSafe
```

**Two option types, and `leave` is implicit.** `{ type = "enter" }` goes to the room;
`{ type = "canvas", canvas_id = "…" }` goes to that canvas's entry passage, resolved at generation
time. A `Leave` link is always emitted.

**The lock is declared once.** An `enter` option with no `conditions` inherits the location's
`entry_conditions`; with no `locked_text` it inherits `blocked_message`.

**Every engine-generated way IN routes through the door** — the nav grid, the nav text list, and
both location lists on `:: Navigation`. Deliberately NOT routed: the *"Back to \<name\>"* link (she
is already inside) and any authored canvas exit, which goes where the author said.

⚠️ **AN OPTION MAY CARRY NO COST AND NO TIME, and that is structural, not stylistic.** The door
passage is a **pure render** — no `<<pass>>`, no effect, no flag, no `current_location` write. Only
that makes it legal for `setup.isRerenderSafe`, and a passage that is not rerender-safe re-applies
its body on every save-load. Cost lives on the far side: a `canvas` option pays through its own
`trigger.costs`, an `enter` option through the location's `entry_costs` via the travel intercept,
which keys on `"Location_"` and never sees a threshold. The field does the same — `degrees-of-lewdity`
charges the walk on the street link and nothing on the knock screen.

⚠️ **`conditions` needs `version = "1.0"`**, like any condition block, or it **fails open** (§4) and
the option is never actually gated. The importer refuses it.

⚠️ **A door needs a nav card to hang off.** The importer refuses one on `auto_exit = false`,
`offscreen`, or `is_container` — all three render no card, so the door would be authored and
unreachable.

⚠️ **KNOWN LIMIT.** A canvas with no trigger and nothing referencing it is pruned from the build
before the generator sees it, and a door option is not yet one of the references that closure walks.
Such an option is **dropped rather than left pointing nowhere**, with a `logger.warning` naming the
option, the location and the canvas. The author fix is one line: give that canvas a trigger location.

---

## 45. The effect toast — what a choice's `effects` actually show the player

Every `effects` / `flagEffects` / `costs` entry on a choice runs through
`setup.applyAndNotifyTrait` / `applyAndNotifyFlag` (`v2.py:6605`, `:6641`), which pushes a line onto
`setup.pendingEffects`. `setup.showEffectNotification()` (`v2.py:6720`) then renders **one green toast
at the bottom of the screen** and removes it after **2000 ms** (`v2.py:6756`):

```
+6 Mark's Relation • +3 Mark's Lust • +120 Money • -4 Home_face • 🔓 Mark owed
```

Three consequences, and the first is the one that matters:

1. **This is the whole of the feedback for a `targetType = "location"` choice.** The link goes
   straight to `Location_<slug>` (`v2.py:15370`), so the toast is not a *summary* of a screen the
   player is about to read — it is instead of one. `the-surfaces.md` **R9** is the rule that follows
   from this fact.
2. **Costs notify too.** A per-choice `costs` entry is emitted as a negative `applyAndNotifyTrait`
   (`v2.py:14747`), so a spend is never silent. This is correct and needs no authoring.
3. ⚠️ **The toast does not wrap and has no maximum width.** `.effect-toast` is
   `position: fixed; left: 50%; white-space: nowrap` with no `max-width` and no media query
   (`v2.py:19704`). A five-effect choice produces a ~92-character line — roughly 650px at 14px — which
   on a 390px phone is clipped at **both** ends, because the element is centred with
   `translateX(-50%)`. The warning variant `.effect-toast.notify-warning` was deliberately given
   wrapping (`v2.py:19722`); the green one never was. **Not fixed** — recorded here so a future
   change is a decision rather than a discovery.

---

## 46. The two switches on a location screen, and what each one now does

### 46.1 `requires_npc` gates the SOLO lane

`setup._npcPresentForCanvas(c, locationId)` (`v2.py:5239`) — same shape as the two paths that
already read the field: `getNpcLocation` only, no declared-schedule requirement, fail closed when
the NPC resolves nowhere. Called from `selectSoloActivityCanvasesForLocation` and from the inline
blocked/cooldown loop in `renderSoloActivities`, in both cases **after** the `npcId` split, so on
a location screen it only ever runs on solo-lane rows. The phone's `_renderLauncher` calls it too
(`v2.py:3175`), for a launcher option whose canvas is in the player's room.

The guard sits **above** both `showWhenBlocked` branches on purpose. *"He is not here"* is not a
cooldown, and `cooldownMessage` defaults to `"Available again later"` — surfacing that would be a
lie. Hide the row; do not explain it.

> **Why it was worth an engine change rather than a rule.** The field was inert on this lane, so
> writing it and omitting it played identically, and the lint that hunts this defect
> (`bound to a person, no face`) keys on the field, so it cannot see a canvas that left it out. A field
> nobody is punished for leaving out is a comment.

### 46.2 `is_active = false` means "never surfaces on its own"

`setup.isCanvasSelectable(c)` (`v2.py:5259`) = `c.isActive !== false && setup.isCanvasValid(c)`,
swapped in at the **six** selection sites: auto-fire, the portrait selector, the solo selector,
both inline blocked loops, and random encounters. Plus one guard in `_isCanvasAvailable`
(`v2.py:3692`), which covers the four schedule/planner consumers at once.

Before this, `is_active` was a real column on `CanvasTrigger` (`apps/stories/models.py:353`),
written identically by both build paths (`template_import.py:8575`, `game_graph.py:336`), and read
by **nothing** in the generator.

> **What that meant.** An author switches off the canvas that sets a door's key flag so the door
> stays locked for the release. With `is_active` ignored, the canvas auto-fired on entry, set the
> flag, and the declared locked door opened.

### 46.3 ⚠️ The trap: `isCanvasValid` must stay clean, and so must `locationCanvases`

**`is_active = false` does not mean unaddressable.** An inactive canvas can be a **substitution
target** of a dispatcher such as `activity_rest`. `_tryRule` resolves them through `setup.getCanvasById`, which builds its map from
`help_data.locationCanvases`.

So two things must NOT happen, and both look like the obvious implementation:

| tempting | what it costs |
|---|---|
| fold the check into `setup.isCanvasValid` | `_tryRule` calls it on the target — the inactive targets stop firing, silently |
| drop the canvas from `help_data.locationCanvases` | `getCanvasById` cannot resolve it — same outcome, same silence |
| add it to `_build_flag_unlock_map` | a flag set only by an inactive canvas hard-fails `NEVER SET` |

An inactive canvas therefore **stays in the index and keeps its passages**, and `_tryRule` keeps
calling the bare `isCanvasValid`. That asymmetry is the design, and it carries a comment at the
call site saying so. Verified live: after the change an inactive walk-in still fires as a
substitution on its dispatcher while never rendering as a standalone row.

**`substitution_only = true` is the field for "dispatcher only, not a button."** Both fields now work; they mean different things.

---

## 47. The quest-card goal bullet — what the player actually reads under 🎯

The engine half of `the-voice.md` R3.

`setup.renderQuestsGoalBlock` (`v2.py:17194-17253`) has four frames, tried in order: terminal →
ready → goal bullets → **nothing**. The bullet frame builds each row like this
(`v2.py:17232-17243`):

```js
var marker = it.met ? '✓' : '◯';
var label = (it.goal && it.goal.label) ||
            (it.goal && it.goal.trait) ||
            (it.goal && it.goal.days_since_flag) ||
            (it.goal && it.goal.flag) || "";
if ((it.goal.trait || it.goal.days_since_flag) && typeof it.currentValue === "number") {
    label += ' — ' + it.currentValue + ' / ' + it.goal.value;
}
```

Two engine facts fall out, and they pull in opposite directions.

**47.1 · A trait goal already prints the number.** `label — 14 / 20`, appended by the engine, with
no author involvement. The importer also *requires* `label` on any trait or counter goal —
`apps/projects/services/template_import.py:6964-6968`, whose own error text says *"it renders next
to the ◯ bullet"*. So trait goals are safe by construction and are the shape to reach for whenever
a card is gated on a number.

**47.2 · A flag goal with no `label` prints its RAW KEY.** The fallback chain ends at
`it.goal.flag`, and `QuestsCondition`'s docstring is explicit that for a flag gate *"`label`
optional"* (`template_import.py:1218-1223`). Nothing in the importer catches it. The player reads
a bullet saying `◯ npc_x_step_05_done`.

⚠️ **Gate `a goal says what it wants` fails on this**, because there is no version of it an author
intended.

**47.3 · A card can render no requirement at all.** `evaluateGoals` reports `allMet: true`
vacuously for an empty goals list (`v2.py:17147-17149`), so the bullet frame is skipped, and with
no `ready_canvas` and no `terminal` the function falls through to `return "";`
(`v2.py:17250-17252`). Its own comment calls this deliberate — *"happens for transitional cards
between capstones."*

So a mute card is legal and sometimes right, which is why this half is a **lint**
(`the guidance page says nothing`) and not a gate. What the lint is hunting is a character
*every* one of whose cards is mute: their section of the guidance page then exists and never says
anything, which is the failure the corpus punishes hardest.

⚠️ **There is no `locked_text`, `requirement` or `hint` field on a quest card.** The full field
list is `text · ready_text · tip · npc_id · priority · group · when · goals · ready_canvas ·
terminal · terminal_text` (`template_import.py:1243-1285`). The only player-facing place a
requirement can live is a goal item's `label` — or, in prose, in `text` / `ready_text` / `tip`.
Do not reach for a field that is not there.

## 48. `[ui.cheat_page]` — free rows and the three time-savers

One page (`v2.py:11185`); each `[[ui.cheat_page.grants]]` row is a button.
A row with `free = true` is a plain button for everyone. Any other row is hidden until its code is
typed. A page with a coded row needs `join_note`, a `join_url` (or `[project] support_url`) and
`package_from_toml --codes`; an all-free page needs none. `[time]` must be enabled.

```toml
[[ui.cheat_page.grants]]
id = "skip_day"
label = "Skip to morning"
kind = "next_day"
wake = "06:00"
free = true
```

| `kind` | does | the validator refuses (`template_import.py:3716`) |
|---|---|---|
| `trait` (default) | one trait write: `trait`, `value`, `op`, `cap`, `clamp` | stage counters, hidden traits, flags, uncapped banded meters |
| `next_day` | `advanceDay()`, then the clock to `wake` | any trait or flag field |
| `play` | goes to `canvas`'s first node when its trigger conditions hold and it has not fired | a repeatable, unplaced or dev canvas |
| `reopen` | unsets `flag` while it is set | a flag no trigger reads `is_false` |

`play` skips only the place and the hours; the scene's own effects move the counter. It skips the
canvas's costs too.

---

## 49. A one-time step is used on its yes — `consume_on`

**Opt-in (EN1, 2026-09-30).** By default a one-time canvas is used up when its first screen shows, so a
no on screen 2 can never come back. With `consume_on = "exit"` on the trigger, the step is used only by
the choice that says so:

```toml
[canvases.trigger]
consume_on       = "exit"
retry_after_days = 2          # the wait when she leaves without deciding (default 1)

# on a choice — at most one of the three:
consumes = true               # the yes: the step is used up
final    = true               # the warned no: used up, and sets the flag <canvas>_closed
retry_after_days = 3          # a parked no: the step comes back after 3 days
```

- The record is `$game_state.canvas_state[id] = {consumed, retryDay, closed, open}`; node 0's fired
  mark in `trigger_history` is unchanged and still drives day limits and decay contact
  (`setup.canvasOptedIn` and the readers after it, `v2.py:4735`; the choice decision, `v2.py:15413`).
- Leaving mid-scene with none of the three parks the step for the trigger's `retry_after_days`, so a
  no cannot be farmed.
- Keys: `template_import.py:836-845` (trigger), `:1022-1028` (choice). A canvas that does not opt in
  behaves exactly as before. The rule it serves is `the-arc.md` A3.
- **Old saves:** a step fired before the change, with no record, reads as used up.

---

## 50. Decay settles at a rest point — `trait_rest`, `decay_after_days`

**EN8, 2026-09-30, a deliberate global change.** `setup.decayToward` (`v2.py:10834`) moves a decaying
trait toward its rest point from either side and never crosses it, in both nightly loops. A value below
0 now climbs toward 0 instead of snapping to it.

```toml
[[npcs]]
id               = "npc_…"
trait_rest       = { trust = 20 }   # where his trust settles (default 0)
decay_after_days = 7                # decay starts only after 7 days without contact
```

- Contact records `$npcs[id].last_contact_day`. Keys: `template_import.py:144-147`.
- **Old saves:** an undefined contact day counts as contact today, so the wait starts now.

