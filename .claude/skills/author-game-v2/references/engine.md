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
v2.py:11560   "is_repeatable": trigger.is_repeatable if trigger else True
v2.py:11633   is_repeatable = getattr(trigger, 'is_repeatable', True) if trigger else True
apps/stories/models.py:355   is_repeatable = models.BooleanField(default=True, ...)
```

**Why it matters for design:** a canvas with no `is_repeatable` key is standing content, not a
one-shot. Assuming otherwise inverts your read of what the game actually is. A grep-based pass
that assumed `false` reported one game as 33% repeatable when the majority was repeatable.

---

## 2. Conditions **fail open** without `version = "1.0"`

```js
v2.py:3969   if (!conditions.version || conditions.version !== '1.0') return true;
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
v2.py:12511   def _resolve_pool_dir(self, pool_dir)     # contents discovered from disk
v2.py:12474   def _media_pool_key(...)                  # cycle state key
v2.py:11908   # ... $game_state.media_cycle
v2.py:11872-11874  # `pool_dir` is preferred: the count is never hardcoded, so the human curates
```

Pools **cycle** (1→2→3→1) through `$game_state.media_cycle` rather than re-rolling, so the
player never sees the same clip twice running. `pool_dir` is preferred over an explicit file
list because the count comes from disk.

Media blocks also appear nested — under group blocks (`blocks[].blocks[].props`) and inside
cascade beats (`blocks[].props.beats[].blocks[].props`). Any tool walking media must recurse.

**A clip inside a cascade beat renders at that beat** (`v2.py:14572`, inside `_render_cascade_tail` at `:14512`) — nesting it there is not
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
v2.py:5365   var cooldowns = sv.game_state.random_cooldowns = sv.game_state.random_cooldowns || {};
             // after a random event fires, skip N visits before rolling again
```

Cooldown is engine-managed per location — do not author your own. Random canvases are
selected by `triggerMode === "random"`.

`max_triggers_per_day` is read per trigger (`v2.py:11634`).

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
is canvases carrying `trigger.location_id` (`v2.py:420-424`, the no-DB graph path; `:447-451`, the
ORM path). Everything else has to be pulled into the closure by a `targetType = "node"` choice or a
substitution target — `_compute_included_canvases` (`v2.py:564-640`, the primary and sole entry
point) and its no-DB twin `_compute_included_canvases_graph` (`:642-691`). A canvas in neither set
never becomes a passage: it costs nothing at compile time, the validator is silent, and every gate
in `gates.py` stays green over it, because gates parse the source and reachability is decided by the
generator. **Write the link in the same edit as the canvas.**

Measured twice in two days: `the_route` shipped both act loops unreachable through a mistyped
`targetType`, and `commuter` shipped six of seven — fully written, at their ceilings — through a
missing link, both with 46 green gates. `gates.py --release` now checks every canvas against the
built HTML for exactly this. `defects/001-no-reachability-gate.md`.

`show_when_locked = true` on a choice renders it greyed and visible instead of hidden. This is
the mechanism behind "every release ends on a visible locked door."

### A node link SWAPS the screen. A cascade beat APPENDS to it.

The single most load-bearing fact about how content is composed, and neither half was written
down anywhere before 2026-08-18.

```python
v2.py:13258   target_passage = self.passage_name_map.get(str(node_id))   # BUILD-time resolution
v2.py:14572   body_html = self._convert_blocks_to_game_html(beat_blocks) # INSIDE <<linkreplace>>
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
   (`v2.py:3317-3331`), which is populated only for canvases carrying `trigger.location`, so a
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

## 15. `locked_text` REPLACES the choice label — and a shown-locked row without one is mute

A choice with `show_when_locked = true` renders as `<span class="locked-choice">`. If
`locked_text` is set, that string is shown **instead of** the action text — the player never
sees what the action was called.

**Omit it and the row is not blank — it is the action label, greyed, with nothing beside it.**
`escaped_locked = (locked_text or choice_text)` at `v2.py:13372`, and the same string is repeated
into the `title` tooltip at `:13219-13220`, so the tooltip adds nothing either. The player sees
"Kiss her" struck out and learns neither why nor when.

**Set `locked_text` by default.** Reach for the bare label only when the action's own name already
carries the reason, and argue it when you do.

Verified live: at `nerve` 60 against a 75 gate, the row rendered as
`SPAN.locked-choice :: Not yet — he still thinks he's getting away with it.`

### ⚠️ This section said the opposite until 2026-08-24, and that is why our games score the way they do

It read:

> *"omit `locked_text` and the greyed row shows the action ("Stop pretending it's a secret") — a
> want the player can name, which is what sells the next release […] **Prefer the want unless the
> gate is genuinely obscure.**"*

The mechanic in that paragraph was right and is kept above. The recommendation did not survive
contact with the field. Measured across 26 shipped sandboxes (`findings_B_refusal.md`, section B):

- A refusal is **either invisible or it speaks**. Of 16,167 refusing conditionals, **71% render
  nothing at all** and **28% put a short line where the action was** — median **9 words**, and
  **60% of those name a handle** (a price 37%, "already done" 18%, a time 5%, a place 2%).
- A **visible, mute action label is 2.26%** of 4,513 spoken refusals, and nearly all of that is
  settings and pagination chrome — `OptionsWidget` toggle states, `Widgets Outfits`
  "Previous"/"Next" greyed at the ends — rather than gated content.

So the shape this section used to recommend is the one shape the field does not ship. Our games
followed the instruction faithfully: **13 of 176 shown-locked choices across every merged game carry
a reason — 7%.** That is doctrine, not author sloppiness, which is why the advice is reversed here
rather than the games being blamed.

It also put this file in direct conflict with `the-surfaces.md` **R5b.2** — *"State the bar with
`locked_text_threshold`; never fail silently"* — written the same day. The two now agree.

Gate: **"a locked door says why"** (`gates.py`, `the-surfaces.md` R5c). It accepts `locked_text`,
`locked_text_threshold` (§23 — the label becomes a clickable toast, `v2.py:13210-13217`) or
`rejection_node` (§36). A choice gated only by `costs` is never counted against you — see §27.

### ⚠️ That is what a shown row must SAY. It is not how many rows to show.

The reversal above answered half a question and the first game authored after it went to **22 of 22
shown-locked choices carrying a reason**, against 13 of 171 across every game before. The
instruction was followed exactly; nothing told it when to stop.

**The field's default is silence** (`findings_B_refusal.md` §2, 16,167 refusing chains): **71%
render nothing at all**, and the per-game silent share runs a **median of 79%** across a **22–100%**
range. The study's own reading: *"The spread is a house decision, not a genre norm"* —
zaras-school-life speaks 78% of its refusals, corpo-life speaks two of 574, and both shipped. So
there is no number to hit. There are three calls to make:

**1 · A DOOR is not a REFUSAL, and their registers differ by measurement.**

```
field spoken refusals   n=4,540   median  9 words   flat, mechanical, names a price 37%
vesper's nine doors               median 22 words   in-fiction, and the study calls it
                                                    "the only game doing this properly"
```

Nine words is right for *"already done"* and *"wrong hour"*. It is wrong for the ceiling of a
release, which `the-release.md` makes the thing that sells the next one.

**2 · Never inside a scene when the scene moves the bar.** A greyed rung mid-beat, gated on a meter
the canvas's own `effects` raise, is the machinery narrating its own progress bar: the row opens by
itself in a click or two, so the text hands the player nothing to act on, and it puts a UI label in
the one place the register says the body is the only thing on screen. Contrast vesper's in-scene
*"Not like this — you're filthy, and the cover won't hold"* — gated on something the player goes
**elsewhere** and fixes. That is a handle and it is correctly spoken. Measured: vesper has 8 in-scene
shown-locked choices and **zero** on a self-moved bar; the game that prompted this had 11 and **all
11** were `arousal` or `loop_stage`.

**3 · A blocked WINDOW is a different surface and it is not this one.** An activity out of hours
belongs in `show_when_blocked` + `cooldown_message` on the canvas trigger — `the-clock.md` C5, where
the hours are the point and hiding them is *"lostness with a clock on it"*. Do not answer a noisy
guidance screen by deleting those.

`scripts/gates.py`'s **`lint · which refusals are shown at all`** reports all three: the in-scene
count, the self-moved subset, and the reason-length median against 9 and 22.

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
`conditions`, `price`, `beauty`, `corruption`, `type` (`template_import.py:208-221`). Slots: `bra`,
`underwear`, `top`, `bottom`, `dress`, `legwear`, `shoes`.

**`worn_corruption` is a MAX aggregate, not a sum.** Verified live: with `sleep_vest` (2) worn,
equipping `mothers_slip` (7) moved the reading **2 → 7**. One loaded garment sets the number on
its own, so a catalog does not need to be large to reach a tier — it needs one item per tier.
**`worn_beauty` is the same fold over `beauty`** (`template_import.py:239`, `v2.py:4044`) — it was
missing from this list until 2026-08-24 and two games use it.

### The three ways a wardrobe gets read

A garment nothing reads is not a garment (`the-meters.md` W3), and **gate · the wardrobe is read**
enforces it. All three of these families satisfy it, and the second is the one authors forget:

**1 · A condition predicate.** `worn_corruption`, `worn_beauty`, `worn_type`, `worn_exposure`,
`clothing_slot` (empty/filled — i.e. "not wearing a bra"), and `clothing_item` with `equipped` /
`unequipped` / `owned` / `not_owned`. This is the gate family.

> **`worn_exposure` is the only one of these that reads an EMPTY slot**, and it is the newest
> (2026-08-28). A derived 0/1/2 — 0 covered, 1 underwear-level, 2 bare — from
> `setup.getWornExposure` (`v2.py:1608`); the predicate is at `v2.py:4111` and its lock text at
> `:7922`; a garment declares its own `exposure` via `template_import.py:2525`. ⚠️ **The other two
> aggregates cannot see nakedness at all**: `worn_corruption` and `worn_beauty` are both
> `getWornStatMax` (`v2.py:1578-1579`), which skips a slot with nothing in it, so naked and plainly
> dressed return the same value. Use `worn_exposure` for how much is showing and the older pair for
> how the outfit reads. `the-meters.md` W7 is why this matters: the field's body system is one
> derived number the whole world tests.

**2 · A `player_portrait` outfit override.** `when = { worn_type?, corruption?, flag? }`, first match
wins (`template_import.py:743-745`). Only `worn_type` and `corruption` are wardrobe reads; a `flag`
override is not. **This is a display reader, not a gate, and `the-meters.md` W7 is what says that is
the field's normal case** — `vesper` reads its wardrobe 21 times and every one of them is display.

**3 · A location dress code.** `clothing_rules.slots_required` on a location
(`template_import.py:4227-4241`), optionally with its own `conditions` and a refusal `message`.

### One thing the wardrobe cannot do, recorded deliberately

**A worn stat can gate a choice and can explain itself when it blocks one, but it cannot be shown as
a standing state.** `v2.py:7816-7823` renders the lock text — `"Outfit must be revealing
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
v2.py:5928   if (clampFlag === undefined || clampFlag === null) { clampFlag = true; }
v2.py:5930   next = window._traitClamp(next, 0, 100);
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
(`v2.py:6027`), so the build emits `applyAndNotifyTrait(..., "subtract", 4, ...)` verbatim and the
runtime drops it on the floor.

**Every effect family, and the ops each actually runs:**

| family | key that identifies it | ops the engine runs | source |
|---|---|---|---|
| trait | `trait` | `add` · `set` | `v2.py:5749-5756` |
| flag | `flag` | `set` · `unset` · `toggle` | `v2.py:5810-5825` |
| quest | `quest_id` | `start` · `update` · `complete` · `cancel` | `v2.py:6084` |
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
template_import.py:188    costs: Dict[str, int] = field(default_factory=dict)
template_import.py:1901   costs=_require_dict(l, "costs"),
v2.py:4687                // A location's per-entry cost lives in setup.locations[slug].entry_costs
v2.py:15885               has_location_costs = any(...)   # the travel-cost block is only emitted
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
template_import.py:177-178   entry_conditions / blocked_message
template_import.py:1898-1899 parsed
template_import.py:6956      loc.properties["entry_conditions"] = l.entry_conditions
```

⚠️ `entry_conditions` needs `version = "1.0"` like any condition block, or it **fails open** and the
door silently unlocks (§4).

**`offscreen = true`** — a non-navigable "away" label. No nav card, no hub, and it is exempt from the
presence floor and reachability. Use it for a character who is genuinely elsewhere rather than
inventing a room for them. `template_import.py:154`.

**`is_container` + `default_entry`** — a pure navigation wrapper that holds no content.
`template_import.py:153`, `:3968`. A container **swallows** any canvas attached to it; attach to a
non-container hub instead.

⚠️ **The lock above is the INERT kind** — a greyed, unclickable card. For a door she can stand at
and knock on, see **§44**; it is a different field and a different fiction.

---

## 23. The guidance page — `[[quest_cards]]`, and it is OFF by default in practice

The table is **`quest_cards`**, flat and top-level — **not** `[[quests]]`, which is an unrelated
table.

```
template_import.py:2581-2587   top-level key is `quest_cards` (flat, not nested under `quests`)
template_import.py:1085         class QuestsCard
template_import.py:1163        parser for one [[quest_cards]] entry
v2.py:15316                    the V2 QuestsPage overlay is emitted only when
                               project.metadata["quests_engine"] == "v2"
```

⚠️ **The trap that shipped a game with an empty guidance page:** `quests_engine = "v2"` turns the
sidebar entry and the page **on**. Authoring no cards leaves a nav link to a heading with nothing
under it. Switching the engine on is not authoring guidance.

**Rendering.** `renderQuestsGoalBlock` (`v2.py:15569`) renders **exactly one** frame per card, in
order: ✓ terminal → 🔓 `ready_canvas` → 🎯 unmet goals. A card that matches none of the three returns
empty and the row goes blank.

⚠️ **A goal-less non-terminal card draws NO frame, and that is how a finished arc ends up looking
live.** It is not a blank *row* — the card still renders its `text` and `tip`, so it reads as an
objective with nothing ticked. Set `terminal = true` on the last card of every arc. `terminal_text`
overrides the ✓ label (default `Arc complete`) and exists because a finished arc and a finished
BUILD are different endings; it needs `terminal` set or the string is dead, and the validator warns.

```
template_import.py:1127        terminal_text on QuestsCard
v2.py:15630                    var _tlabel = card.terminal_text || "Arc complete";
```

⚠️ **The one-`terminal_text`-per-game cap is scoped to a game whose arcs are CLOSED.** It was
written from `vesper` 0.1.8, a finished build where four arcs genuinely had ended and the default
`"Arc complete"` was **true** of them; there, one card marking the build boundary is right and six
would be noise.

**It is the wrong rule for a v0.1, and following it there produces the worse outcome.** In a first
release nothing is closed — every track stops at a build boundary — so the cap forces every arc but
one into `"Arc complete"`, **a stronger and falser claim than the string it was rationing**.
`the-release.md:107-110` already rules the other way for that case:

> state the current ceiling honestly. The reference game prints a plain marker at the top of **each
> track** so the player knows where the wall is. […] An honest wall is a promise; a silent one is a
> bug report.

**Each track.** So: `"Arc complete"` belongs to an arc that has genuinely **ended**. An arc that
stops because the build stops carries its own marker, and the same plain string on every such track
is what "a plain marker at the top of each track" means. Cap the *claim*, not the field.

⚠️ **`ready_canvas` MUST name a canvas that HAS A LOCATION, or Frame 2 renders NOTHING.**
`lookupCanvasBySlug` (`v2.py:15371`) walks `help_data.locationCanvases`, keyed by location UUID, so a
**triggerless** canvas — the usual shape for a sex loop or any sub-menu reached by a choice — is not
in that index at all. It returns `null`, Frame 2 does `if (!found) return ""`, and the card falls
through to **no frame**: text and 💡 tip with nothing ticked, the exact failure the warning above
this one describes. Point `ready_canvas` at the **hub** the loop hangs off — it carries the location
and the schedule, which is what the 📍 and 🕒 lines are read from.

⚠️ **`terminal` IS NOT COMPUTED FROM PROGRESS, AND A CHARACTER WHOSE ONLY CARD CARRIES IT READS AS
FINISHED FROM VALUE ZERO.** Frame 1 fires on `card.terminal === true` alone, ahead of every other
frame (`v2.py:15199`) — nothing checks that anything was achieved. So a single card gated
`{ trait = "owed", op = "lt", value = 40 }` and marked terminal matches at `owed = 0` and prints
**✓ Arc complete on turn one**, before the player has met the character.

`the_season` shipped exactly this for two of its five: Boyd and Emmett each had one terminal card
on a `lt` band, while Wade, Prine and Rae had proper two-card ladders and were correct. The rule
above — *set `terminal` on the last card of every arc* — is right, and it is not sufficient:

**`terminal` belongs on a card the player has to CLIMB TO.** An arc needs at least two cards: an
open lower band, and a terminal upper one gated `gte` at a threshold real content sits on. One card
marked terminal is not a ladder with a top; it is a badge with no ladder.

⚠️ **AND A METER IS THE WRONG THING TO GATE IT ON AT ALL.** The rule above says climb to a
threshold; it never says *climb to what*, and five v2 games answered it the same wrong way — they put
the badge on the threshold that **opens** the content instead of one above it, so the ✓ arrives on the
click that unlocks the scene. Measured across the repo the day this was written:

```
mrs_vance     5 of 6 characters - 2 landing ON the door, 3 landing BEFORE it
                                  (one 40 points early; two on a DIFFERENT meter
                                  from the one the door reads, so the tick at want 0)
forty_miles   6 of 6 - every badge at exactly the door value
seventh_day   1 badge on the door + 5 goals 25 points past anything the game reads
the_season    4 of 5
vesper        0 of 5   <- the v1 game this section was written from is clean
```

**The fix is not a bigger number — it is a different kind of gate.** Put the ✓ on a **flag the content
sets on its way out**, so it means *you have played this* rather than *you have ground past it*. The
v1 hint system had exactly that pairing (`arc_closure_flag` pre + `arc_complete` post,
`template_import.py:1017-1023`) and the v2 card schema dropped it without replacing it:

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
Same measurement: `mrs_vance` shipped three (`isaac.want 66`, `sherrod.want 62`, `tobin.want 30`) and
`seventh_day` five. They stay invisible while the terminal frame outranks the bullets, and the moment
the badge is fixed they become live instructions to grind for nothing — so fix the numbers in the
same pass, never one without the other. `scripts/gates.py`'s **`lint · the badge arrives before the
content`** reports both.

⚠️ **`pickQuestsCards` takes EXACTLY ONE scope string, and anything else fails silently.**

```
v2.py:15495   setup.pickQuestsCards = function(scope) {
v2.py:15496       if (scope !== "story_goals") return [];
```

A hard early return, no error, no warning. A typo in that string gives an **empty top section on the
guidance page** and no clue why. *(This paragraph originally described the function without
mentioning the guard — written from source, and it still missed the function's first line. Read the
whole function, not the part that answers your question.)*

**Selection.** `pickQuestsCards(scope)` (`v2.py:15495`) returns every matching top-tier card;
`pickQuestsCard(slug)` (`v2.py:15470`) returns the **single highest-`priority`** match for a
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

**`locked_text_threshold`** (`v2.py:13185-13186`) prints an explicit *"Requires …"* hint on a
locked choice, distinct from `locked_text`, which replaces the label (§15). ⚠️ This citation read
`v2.py:12786` until 2026-08-24 and was **stale** — corrected when §36 was written and every cited
line re-read.

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
v2.py:3422   const dayIndex = ["Monday", "Tuesday", …].indexOf(timeState.current_day);
             also :3593 :3737 :3792 :3855
```

Set it to `0` and `indexOf` returns `-1` at every call site.

**The false alarm:** no schedule row matches, **every location reports nobody present**, and the
game reads as having a broken presence system. It does not. The harness set a number where a string
belongs.

### 24.3 Ask the engine who is present — do not recompute it

```
v2.py:4948    setup.getNpcsPresentAtLocation = function(locationId)
v2.py:19995   the engine's own nav badges call it
v2.py:20019   and again for the portrait row
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

- The exact cooldown count for random events.

*(`speaker = "unknown"` was on this list. It has been read and promoted — see §25.)*

*(**Save-safety specifics — which identifiers orphan a live save when renamed** — was on this list.
**Read and promoted 2026-08-29:** `references/the-returning-player.md` §2–§5 names them — the
canvas/node slug, a flag or trait key, a stat's scale, and the game title — and §40 below carries
the engine half. Struck here 2026-08-29, having outlived the answer by a day.)*

*(Adjacent `[group]` blocks merging into a single if/elseif chain was on this list, while
`the-surfaces.md` R6 stated it as fact — the skill contradicted itself. **Read and promoted
2026-08-23:** `_render_group_chain` collects consecutive `group` blocks into one variant chain at
`v2.py:14561-14568`, so a second ladder on the same node IS dead and first match wins.)*

---

## 25. A speaking block with no `speaker` renders as a character called "Npc"

**Verified, and it is the largest defect ever found in a v2 game.** `dialog` and `thought_bubble`
both resolve their speaker the same way, and the field is **not optional**:

```python
speaker = props.get("speaker", "npc")        # v2.py:15003 — the default is a STRING, not a person
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

1. `advanceDay()` sets `rent_state.is_due` when the day rolls over **to** `due_day` (`v2.py:5615`).
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
   filters on `setup.checkCostsAffordable(c.costs)` (`v2.py:4794`, `:4527`, `:4975`; the function
   itself at `v2.py:4625`). An unaffordable rung does not render as a broken click — it is not
   offered.

   ⚠️ **That is the canvas picker. An exit-block CHOICE behaves differently, and better.** There the
   generator opens `<<if setup.checkCostsAffordable(...)>>` (`v2.py:13014-13015`) and writes an
   `<<else>>` that keeps the row, greyed, with the requirement appended by the engine itself
   (`v2.py:13159-13166`):

   > `Work a shift 🍺 (Requires 15 Energy (you have 6))`

   **A priced choice explains itself with no authoring at all**, and a price is what the field's
   spoken refusals name most (37% — §15). This is the asymmetry worth knowing: `costs` come with
   their own message, `conditions` do not, and a `show_when_locked` condition with no `locked_text`
   goes mute. The gate **"a locked door says why"** therefore never counts a cost-only choice
   against a game.
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
(`v2.py:11634`, `getattr(trigger, 'max_triggers_per_day', None)`). A triggerless rung — a canvas
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
never-set flag when a condition requires it `is_true` (`v2.py:12312`) — deliberately, since an
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
2. **Whatever `[[sidebar_items]]` you authored** — `trait_status_text` (`v2.py:16933`),
   `trait_words` (`v2.py:16996`), `trait_bar` (`v2.py:16886`).

They do not know about each other. Band a trait without suppressing its number and the player reads
*"Nothing under it"* and `cover 55` stacked on top of each other.

**The suppression is `[[traits.labels]] hidden = true`.** The generator collects those keys
(`v2.py:1220-1226`), emits them as `setup.hiddenTraits` (`v2.py:3156`), and the dump skips them
(`v2.py:15557`, `:15604`).

```toml
[[sidebar_items]]
type  = "trait_words"
trait = "cover"
bands = [ { min = 0, max = 14, text = "Long dress, hair pinned" },
          { min = 15, max = 100, text = "Apron off" } ]   # ← top band CLOSED, and its
                                                          #   max sits at/above the ceiling

[[traits.labels]]
key    = "cover"          # ← REQUIRED, or the number prints underneath the words
hidden = true
```

⚠️ **A trait absent from `[[traits.labels]]` entirely is NOT hidden** — it still appears in the
dump. Measured: a shipped game banded all four of its meters in `[[sidebar_items]]`, declared none
of them in `[[traits.labels]]`, and printed every one twice.

⚠️ **The other half: a banded value that lands outside every band renders NOTHING** — the whole card
disappears, which reads as a missing HUD element rather than a wrong number, so a quick playtest
sails past it.

**The band rules are PER TYPE, and an open top band is legal on exactly one of the three.** The
example above is `trait_words` on purpose: its shape is the one that is legal everywhere, so copying
it blindly cannot break a build.

| type | open-ended top band? | the rule | source |
|---|---|---|---|
| `trait_status_text` | **yes** — an omitted bound defaults to ∓1e9 | at least one of `min` / `max` | `template_import.py:3751-3757` · `v2.py:16948-16949` |
| `trait_words` | **no** | `flag` **XOR** range; in range mode BOTH `min` and `max`. A flag-only band is legal | `template_import.py:3613-3623` · `v2.py:17017-17018` |
| `trait_bar` | **no** | both `min` and `max`; `flag` is rejected outright; `bands` itself is optional | `template_import.py:3659`, `:3676-3681` |

So the fix for a value off the top of the ladder is **not** to drop the `max` — that compiles on one
type and hard-fails the build on the other two. Give the top band a `max` at or above the trait's
ceiling, or `cap` the terminal add (§29). `commuter` runs `max = 100` against declared ceilings of
88 / 86 / 80, which is the safe direction.

⚠️ **This section taught the bug it now warns about.** Its only worked example used to be
`trait_status_text` with an open top band — correct for that type — and the sentence under it said
*"leave the top band's `max` off"* with no type attached, two lines after the sentence that drew the
distinction. A board copied the shape onto `trait_words` and the build refused to compile.
`SKILL.md`'s own operating rule is the diagnosis: **an example outranks every rule beside it.**
`defects/002-sidebar-band-example-wrong-type.md`.

### 30.1 A hygiene system is a deliberate non-feature — do not build one

This engine has no hygiene, hunger or thirst primitive, and that is a decision rather than an
omission. It is recorded here because **`trait_status_text` makes one authorable in an afternoon** —
its own spec comment says *"Use for hygiene/energy/hunger-style needs that recover on action"*
(`template_import.py:3685-3690`) — so the temptation lands precisely on this section.

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

- **`free-cities`, the corpus's deepest body simulator, never modelled it.** Its slave objects carry
  `vagina`, `dick`, `boobs`, `anus`, `balls`, `butt`, `health` and `preg` as numeric properties, and
  no hygiene or arousal property at all. Its two most-read properties are `devotion` (1,019) and
  `trust` (667) — above every body part.

- **Corpus-wide, hygiene is the rarest of the four body subsystems**: 234 read sites against
  arousal's 8,183 and clothes' 6,821. Two of 27 games clear 20 read sites, and one of those two is
  a single 22-read variable that is 86% colour.

Our own games agree from the other side: `the_allowance`, `back_home`, `last_call` and
`late_shifts` all raise a `hygiene` trait that nothing reads — they are in gate 33's own list of
dead meters (`the-meters.md` W3).

**If a need must exist, make it a `costs` entry on the acts that need it** (§27) — a price the
engine already enforces — rather than a meter with a ladder and a decay hook. Recorded in the same
register as the per-character dialogue colour in §34: a known difference from the field, left
unbuilt on purpose.

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

`requiresNpc` is emitted into `help_data.locationCanvases` at `v2.py:11721` and consumed in
exactly two places:

```
v2.py:5432   var npcLoc = setup.getNpcLocation(canvNpc.requiresNpc);
             the RANDOM-ENCOUNTER selector's presence gate   ← works as documented
v2.py:5502   var subNpcLoc = setup.getNpcLocation(target.requiresNpc);
             substitution rules — the same check on the substitution TARGET
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

### 31.1 The two functions, by name — and the comment that says otherwise

The two consumers are `setup.checkRandomEncounters` and `setup.checkAndSubstituteCanvas`. Naming
them matters, because they are exactly the three trigger shapes a check must exclude:
`trigger_mode = "random"`, `substitution_only = true`, and `is_repeatable = true`. Everything else
that names a character is on the auto-fire path and is not gated by this field at all.

⚠️ **`template_import.py` said the opposite, and that is what actually caused the failure.** The
comment on `TemplateTrigger.requires_npc` described it as something that *"lets authors drop
per-canvas location+time gates in favor of consulting the NPC's single source of truth"* — an
unscoped claim, true only for the two functions above. `the_season` was authored twelve hours after
`the-first-hour.md` F5 and its worked template landed, with the correct rule available, and shipped
five meetings with no window; its introductions played to empty rooms, one of them at 06:10 on a
Saturday saying *"it's Monday"*. **Doctrine loses to the schema comment, because the schema is what
is open while you type.** Corrected 2026-08-23, and gated as `a meeting fires where they are`
(G38) so the next one is caught by the build rather than by a player.

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

`window.advanceTime(minutes)` (`v2.py:5569`) adds minutes to `time_state.current_minute`, rolls the
hour past 60 and the day past 24, expires temporary modifiers, and repaints the sidebar. That is the
whole time API. **Nothing in this engine can send the clock to a named hour**, so a label or a beat
promising one ("work till one", "back by six") is a promise the engine cannot keep.

`window.waitTime(minutes)` (`v2.py:5610`) is the sidebar wait buttons' entry point — the same
advance, plus `setup.commitMoment()`, because a wait navigates nowhere and would otherwise live only
in the active moment.

An exit that declares no `time_progression_minutes` still costs **3 minutes**
(`v2.py:13819`, `config.get('default_time_progression', 3)`; the exception fallback at `:13388` emits
the same `advanceTime(3)`). A four-node opening has therefore drifted 9 minutes before the first real
choice.

There is no `@time` token either — `_resolve_at_references` (`v2.py:14027`) resolves `@player` and
`@<npc>` and returns everything else untouched. The clock can be *shown* (`<<timeDisplay>>` at the
top of `StoryCaption`, `v2.py:15663`/`:15679`, rendering `<<timeFormatted>>` at `v2.py:16043`) but it
cannot be *printed into prose* by any authored token.

### 32.2 Travel time is tagged on the card; activity time is tagged nowhere

| what | tagged? | where |
|---|---|---|
| `[[locations.costs]] time` | **yes, automatically** — renders `20m` on the nav card | `getLocationCostTag` `v2.py:4893`, used at `:19353` / `:19370` |
| a choice's `time_progression_minutes` | **no** — emits a bare `<<script>>advanceTime(150);<</script>>` at the bottom of the passage body | `v2.py:12733` |
| a trait `costs` entry | yes, when unaffordable | `getCostBlockedMessage` `v2.py:4670` |

So a door announces its twenty minutes and a two-and-a-half-hour shift announces nothing. If the
duration is to appear, the author puts it in the label. `references/the-clock.md` C4.

The field puts it there as a matter of course. Course of Temptation's most-returned-to screen
prints the cost on every single option — `<<dtime 15>>` beside the shower, `<<dtime 10>>` beside
grooming — alongside the need effect (`<<dalterneed Hygiene 1000>>`), so nothing about the clock is
a surprise (`~/Documents/Female_PC_Craft_Study_20260823/findings_C_loop.md`). No rule change here:
C4 already owns this as a lint, and the corpus evidence behind it is thin — 4,219 of the corpus's
4,260 duration tags belong to one game.

### 32.3 `show_when_blocked` — the only out-of-hours surface, and one game uses it

A solo activity whose schedule window has closed is dropped from the location list entirely, unless
the author opts in:

```toml
[canvases.trigger.metadata]
show_when_blocked = true
cooldown_message  = "Counter work — mornings, eight till one."
```

Read at `v2.py:11055-11059`, emitted as `showWhenBlocked` / `cooldownMessage` (`v2.py:11100-11101`).
`renderSoloActivities` (`v2.py:5242`) checks `isCanvasValid` (`v2.py:4742`) — which returns false on a **schedule
miss** before anything else (`v2.py:4573-4580`) — and, when the flag is set, pushes the canvas onto
`soloCooldownBlocked` instead of dropping it, rendering a dimmed non-clickable line carrying the
message (`v2.py:5309`). The same path also catches `max_triggers_per_day` exhaustion
(`v2.py:5263`).

⚠️ **One game in this repo sets it** — `off_season`, six times, writing the hours out in its own
words (*"mornings, eight till one"*, *"after nine at night"*, *"the last two hours, before the
shutter"*). Everywhere else windowed work simply vanishes and the player has no surface that says
when to come back. (This paragraph read *"Zero of the ten games"* until 2026-08-24; it was written
before `off_season` adopted it and nothing re-counted.) The `SchedulePage` (`v2.py:18964`) publishes hours for
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

`self.rent_currency_symbol = rent_settings.get("currency_symbol", "$") or "$"` — `v2.py:1152`.
Emitted to the runtime only when rent is enabled (`v2.py:3123`), so a game without
`[settings.rent]` has no symbol setting at all.

⚠️ **`RentDay_Short` is the one every rent game reaches.** It is the branch taken when the player
cannot pay — the screen where the number matters most — and it does not even set `_cur`.
`games/forty_miles` declares `currency_symbol = "£"`, and its released build ships
`You have: <strong>$<<print $player.core_traits.money>></strong>`. The author's own comment on that
line reads *"the pages hardcoded `$` before this key existed"*; the key did not finish the job.

### 33.2 The symbol is a prefix

Every honouring site concatenates symbol-then-number — `"Pay " + _cur + _rent + " rent"`
(`v2.py:16604`), `<<print _cur>><<print _money>>` (`v2.py:16608`). There is no suffix form and no
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

An affordable choice renders its authored label and nothing else. The engine speaks a price **only
on the failure path** — `getCostBlockedMessage` (`v2.py:4656`) emitted into
`<span class="locked-choice">` at `v2.py:13140`:

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

---

## 34. `[ui.cast_page]` — the who-is-who page, and it authors nothing

The player's place to look somebody up. Measured across the 27-game mopoga field: **18 of 27**
shipped sandboxes carry a page like this and **7 of the 8** parsed top-ten do — the lone exception,
degrees-of-lewdity, carries the same load inside its prose by swapping description for name on the
meeting flag in 64 places. **None of the 27 uses a narrator to tell the player who somebody is.**

> Re-checked 2026-08-24. `college-daze`'s is a **phone contact list** — `Check Contacts`, one row
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

```
template_import.py   TemplateCastPage, [ui.cast_page] parse, metadata write
game_graph.py        the NO-DB path's ai_behavior_config write  <- the default build
v2.py                _generate_cast_page  ::CastPage + ::CastWidgets
```

⚠️ **`relationship` is the ONLY NPC string that survives to runtime.** `description` is
`entry.pop("description", None)`'d before `$npcs` ships (`v2.py:1046`) — deliberately, because
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

Shipped 2026-08-24 from Section G. Optional, capped at **four** (`NPC_TAGS_MAX`), and inert in every
game that does not use it.

```toml
[[npcs]]
id           = "npc_boyd"
name         = "Boyd"
relationship = "Your father, 47. His name is the one on the contract."
tags         = ["The book", "The scale", "Saturday", "Black coffee"]
```

```
[face]  Boyd
        Your father, 47. His name is the one on the contract.
        The book · The scale · Saturday · Black coffee
        📍 The packing shed
        💡 …
```

**Why four, and which four.** The field's best cast page is `friends-of-mine`'s **Characterpedia**:
fifteen people, each with a portrait, a counter (*"Had sex N times"*), a 27–83-word biography, and
**exactly four interests** — all fifteen, no exceptions.

```
Chloe     Manipulation | Attention | Writing | Oriental Food
Winter    Watching People | Domination | Money | Expensive food
Sofia     Working | Silence | Reptiles | Rough Sex
MrsMorin  Secrets | Manipulation | Relaxing | Spanish Food
```

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
the same reason `description` is popped at `v2.py:1031`. Do not "simplify" it onto `$npcs`.

⚠️ **`ai_behavior_config` IS WRITTEN IN TWO PLACES AND THE DEFAULT BUILD USES THE SECOND.**
`template_import.create_project_from_template` is the `--use-db` path; `game_graph.build_game_graph`
is the one a plain `package_from_toml` takes. **A per-NPC field added only to the first reaches the
database and never reaches a packaged game** — and the symptom is a silently empty registry with no
error at import, at build, or at runtime. This cost a debugging cycle on the day `tags` shipped;
`tests/test_npc_tags_field.py` now locks the no-DB path specifically.

**Not a substitute for design.** The tag line is a four-word compression of a corner of the world
the character already owns (`the-surfaces.md` R8). It cannot give one to a character who has none.

### One thing the field does on every line that we do not: colour

Recorded 2026-08-24 as a **known difference. Nothing is built for it.**

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

**We already ship two of the three.** `v2.py:15035` puts the portrait on every NPC dialogue block
and the name above it — 54 of `the_season`'s 59 rendered blocks carry both. What we do not ship is
the third: the renderer emits one `dialog-npc` class for the whole cast (`v2.py:15042`).

**Do not build this on the strength of the count alone.** It is recorded so the next person does not
rediscover it as a gap; build it when a game asks for it.

---

## 35. `block_pool` — the variant pool, and the field's main mechanism for a re-read surface

**The engine has had this since v2 shipped. No v2 game has ever used it.**

```python
v2.py:14798   if block_type == "block_pool":
v2.py:14799       pool_blocks = (block.get("props") or {}).get("blocks", [])
v2.py:14806       parts = [f'<<set _bp to random(0, {max_idx})>>']
v2.py:14581-14588 # if / elseif / else chain over the variants
```

**It picks a different one of N blocks on every render.** Not once per game, not once per day —
every time the passage draws. Re-enter the surface and the sentence is different.

| fact | source |
|---|---|
| children live at **`props.blocks`** | `v2.py:14574` |
| a **one-item** pool renders directly, no `random()` | `v2.py:14576-14578` |
| variants may be **any block type** — the pool nests `_convert_blocks_to_game_html` | `v2.py:14578`, `:14587` |

```toml
# BOTH SHAPES PARSE. This is the one every group in our games already uses —
# children at the block's own `blocks` key — so it is the one to copy.
{ type = "block_pool", blocks = [
    { type = "paragraph", content = "…first variant…" },
    { type = "paragraph", content = "…second variant…" },
    { type = "paragraph", content = "…third variant…" },
] }

# Identical after import. The generator reads props.blocks either way.
{ type = "block_pool", props = { blocks = [ … ] } }
```

### The four authoring facts, verified in the importer

`template_import.py:6210-6237` normalises both container types side by side, so the rules are the
same ones `group` follows — with one exception that is not.

| | |
|---|---|
| children may sit at **`blocks`** OR **`props.blocks`** | `:6225` — `b.get("blocks") or props.get("blocks")`, the same both-shapes read `group` gets at `:6214`. This section showed only the `props` form until 2026-08-24, which is the minority shape in our own games |
| **a `block_pool` directly inside a `block_pool` is silently dropped** | `:6230` — `inner_safe = [ib for ib in inner_safe if ib.get("type") != "block_pool"]`. A random pick of a random pick is ambiguous and the restriction is deliberate. **Unlike `group`, which MAY nest in `group`** (`:6218-6222`, the same-type-skip rule was removed 2026-05-17) |
| **mixed child types only WARN** | `:6235` — `logger.warning("block_pool has mixed types …")`. It builds. Same-type children are the intent, and the warning is in the build log, not the game |
| nesting depth is capped at **4** | `:6143` — a `group` wrapping a pool wrapping a group is depth 3, so 4 is a ceiling rather than a limit you will meet |

⚠️ **A pool is an exclusive axis and the scoreboard now reads it as one.** `gates.py`'s
`_band_texts` knew `group` and not `block_pool` until 2026-08-24, so a three-variant pool had its
variants concatenated and reported as text that always renders — `lint · the act nodes` would have
called three one-word variants a three-word band. Fixed before the first pool shipped. The **beat**
collector still folds every variant together on purpose, and that is correct: see the folding
argument below.

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

Counted across every `toml_phases/*.toml` in this repo:

```
the_long_summer   (v1)   46
under_one_roof    (v1)   14
vesper            (v1)    6
EVERY v2 GAME             0
```

v1's corpus carried a whole numbered rule for it — `prompts/game_design_rules.md:1330`,
**Rule 17: Block Pools for Repeatable Activities** — and it named the failure precisely:

> "This prevents the **'same text every morning' problem** that makes daily activities feel dead.
> […] The group block system handles phase changes (post-first-kiss vs default), but **WITHIN each
> phase, the text is frozen.** Block pools add variety within phases."

That last sentence is the same distinction the 2026-08-23 field study arrived at independently, and
it is now R6's mechanism 4 vs mechanism 5 in `the-surfaces.md`.

**How it was lost:** v2's skill was deliberately divorced from `prompts_v2/` because that corpus
taught false engine facts. In cutting away the false ones, this true one went with them — and the
v2 skill mentioned `block_pool` exactly once, inside a list of valid block types, for its whole
life. **The lesson is about the divorce, not about the primitive:** a wholesale cut loses the good
with the bad, and nothing checked what was in the discarded half.

⚠️ One local exception is on record and should not be mistaken for a ban:
`games/the_long_summer_test/toml_phases/3_activities.toml:7-9` says *"block_pool prose rotation is
in the schema but forbidden by the doctrine; doctrine wins for slice authoring."* That was a
**test-slice** decision — the same repo's full game uses it 46 times.

### Two authoring constraints, from v1's schema doc

`prompts/toml_generation_prompt_v4.txt:1044-1053`:

- **All child blocks must be the same type** (paragraph, dialog, or group). Use a `group` inside the
  pool for multi-block variants.
- **"`block_pool` CANNOT be nested inside another `block_pool`."**

⚠️ The nesting constraint is **stated by v1's schema doc and NOT verified against `v2.py`** — treat
it as unverified and do not cite it as an engine fact. The plausible mechanism is that both pools
emit the same `_bp` temp variable (`v2.py:14580`), but whether SugarCube's already-matched
`if/elseif` chain actually breaks on the collision was not tested. **Do not nest until someone
tests it.**

### ⚠️ The gates fold every variant into one beat, and that is CORRECT

`scripts/gates.py:338-349` collects a pool's children into the **same** `Beat` object, so ten
30-word variants count as one 300-word beat. That looks wrong and is not. `Beat`'s own docstring
(`gates.py:298-306`) gives the reason: a Twine passage carries all its `<<if>>` branches inline, so
folding keeps our numbers comparable to the baseline the thresholds came from.

Measured 2026-08-23 across ten Degrees of Lewdity location passages, to check rather than assume:

```
ten named location passages: 9,886 words · unconditional 234 · IN A BRANCH 9,652  (98%)
```

⚠️ **Read that as ten passages, not as the whole game.** It is a spot check of
`Hallways`, `Farm Work`, `Forest`, `Orphanage`, `Domus Street`, `Bedroom`, `Beach`, `Park`,
`Museum` and `Temple` — not a per-location total of the kind `location fill` computes. It is
lopsided enough (234 words out of 9,886) to settle the question it was asked, and it is **not** a
figure to quote as "DoL is 98% conditional".

The `location fill` threshold was derived from that same source (116,540 words across 25
locations — `CHANGELOG.md:4835`), so counting our variants the same way **is** the apples-to-apples
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
recurring is the opposite one, *"same gifs every time you do same things every single time"*
(`zaras-school-life`, its top-liked criticism). Measured 2026-08-23 across 3,479 comments —
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
| **A — the wall** | `show_when_locked = true` | greyed out, label = `locked_text` or the choice text (`v2.py:13171`) | nothing, or a threshold toast if `locked_text_threshold` is set (`v2.py:13210-13217`, §23) |
| **B — the rejection** | `rejection_node` | **a live link**, label = `locked_text` or the choice text | goes to that node and applies `rejection_effects` |

The generator names Mode B itself — `# Mode B: Clickable rejection — redirects to rejection node`
(`v2.py:13374`), entered from the `if rejection_passage:` branch at `v2.py:13373` (`rejection_passage`
is the generator's internal name for the field authors write as `rejection_node`). The node id is resolved against `passage_name_map` at `v2.py:13668-13673`, which
logs a warning rather than failing the build if the target does not exist, so **a typo here is
silent in the game and visible only in the build log.** Effects are emitted at `v2.py:13152-13165`
through the same `setup.pendingEffects` path a normal choice uses.

Both fields live on `TemplateChoice` (`apps/projects/services/template_import.py:825-826`, in the
class at `:806`), beside `conditions`, `show_when_locked`, `locked_text` and
`locked_text_threshold`, and are read from the TOML at `:2204`.

⚠️ **`rejection_node` IS build-validated, contrary to what the paragraph below used to imply.**
`template_import.py:4616-4624` raises when it names a node that is not in the same canvas — so a
typo fails the build with a message naming the canvas and the choice index. The fail-open warning
described below is the generator's later slug→passage resolution, which only sees ids the importer
has already accepted.

### The census — this is a recovery, not a discovery

Counted across every `toml_phases/*.toml` in the repo, 2026-08-24:

```
show_when_locked        176 uses · 12 games      the wall is well used
locked_text_threshold    21 uses ·  1 game       late_shifts only (v1-era)
rejection_node            0 uses ·  0 games      ← and undocumented until now
rejection_effects         0 uses ·  0 games
```

`locked_text_threshold` was already documented (§23). **`rejection_node` was not documented
anywhere in this skill** — a working primitive that nothing taught, so nothing used.

⚠️ **This paragraph used to add "the same shape as `block_pool` (§35)", and it overstated §35.**
Corrected 2026-08-24 (section E). §35's claim is *"no **v2** game has ever used it"*, and that is
true — but dropping the qualifier makes a broader claim that is not. **`block_pool` is authored 69
times across four games**: `the_long_summer` 49, `vesper` 12, `under_one_roof` 7,
`the_long_summer_test` 1. None of the four carries a `v2_state.json`, so all four are v1-era, which
is exactly why §35 phrases it the way it does.

`rejection_node` is at **zero across every game in the repo**, v1 and v2 alike. That is a stronger
statement than §35's and the analogy blurred it. Counted with `grep -c block_pool` over every merged
final.

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
*"flag/trait/random"* list at `template_import.py:3143` is a docstring, not a feature — and the only
randomness available is `trigger_mode = "random"` (whether a canvas fires at all) and `block_pool`
(which words render). A choice goes where its conditions send it.

That difference is smaller than it looks, because the field **publishes the odds before the click**:
`<<skillcheck>>` renders a word next to the label — `certain · trivial · easy · moderate ·
demanding · hard · very hard · nearly impossible` (`skillcheck_descriptor`), used **314** times.
A dice roll the player can see and accept is not the RNG their comments resent (§35).

> A published *threshold* keeps the same promise a published *probability* does: **the player knows
> what they are risking before they click.** Use `locked_text_threshold` to say the bar out loud.
> Do not simulate a roll.

### The authoring shape

```toml
[[canvases.nodes.choices]]
text                  = "Tell him no"
conditions            = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "nerve", operator = "gte", value = 40 },
] }
show_when_locked      = true
locked_text           = "Tell him no"          # same words — she still tries
locked_text_threshold = "She would need to be steadier than this — 40 nerve."
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

Added 2026-08-24 from section K. **Rewritten the same day, because the first version of this
section was wrong** — it said the fix was *"three whitelist entries and no runtime work"*, and it
named the quest-card validator as the thing blocking `ne` on a canvas condition. It is not. The
real architecture is below, and it is the load-bearing fact:

| evaluator | backs | `ne` |
|---|---|---|
| `compare()` — `v2.py:3988` | canvas / node / choice `conditions` | **yes**, since v2 shipped |
| `setup.describeUnmetConditions` — `v2.py:2004`, trait switch `:2027`, phrases `:2037` | the *why is this locked* text on a blocked choice | **yes** |
| `setup.checkSingleCondition` — `v2.py:7658`, trait branch `:7670`, `ne` at `:7692` | hints, quest-card *goal* bullets, `_findFlagSetterCanvas`, ten-plus call sites | **yes, since 2026-08-24** |
| `setup.checkQuestsCondition` — `v2.py:15536` | `[[quest_cards]]` `when` and `goals` | **no, deliberately** |

`compare()` is reached first from the trait branch at `v2.py:3988`.

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

**Not fixed here, and not a bug report against a game: no authored condition uses any of the six.**
Measured 2026-08-29 over every predicate item carrying a `trait_key`, phase files only, across the
twenty games that have trait conditions: **`gte` 2,287 · `lt` 527 · `eq` 191 · `lte` 31 · `gt` 1 ·
`ne` 0**, and none of the other six anywhere. (Type-specific operators — `is_true`, `is_false`,
`is_present`, `equipped`, `owned`, `is_active` and their negations — are their own branches and are
not part of this comparison.) Recorded so the next person adding an operator reads the count before
the code, and so a game that reaches for `contains` is recognised as the first real demand rather
than as a mystery.

⚠️ **The count was THREE here until 2026-08-29, and the fourth was found by counting rather than by
a bug.** `setup.describeUnmetConditions` carries its own inline operator chain and its own phrase
table — it neither calls `compare()` nor `checkSingleCondition` — and it happens to handle `ne`
already, so nothing was broken. **The in-code comment beside `checkSingleCondition`'s `ne` line
(`v2.py:7686`) still calls itself "THE SECOND EVALUATOR" and names one other.** The code is correct;
the count in the comment is not. Read this table, not that comment, before adding an operator.

### What was actually broken, and what was not

**A canvas condition's operator is not validated by the importer at all.** An unknown operator
imports clean, reaches the runtime JSON, and fails **closed** in `compare()` with no build error and
no warning. So `ne` was always writable on a canvas gate and always worked there.

What did not work: the **same condition item** read through `setup.checkSingleCondition`, whose trait
branch ran `gte / gt / lte / lt / eq` and then `return false`. A `ne` gate was therefore true on the
canvas and false in every hint and flag-setter lookup that touched it. One line, now fixed.

The second half was cosmetic and worse than it sounds. The requirement-label formatter
(`setup.formatCanvasConditions`, `v2.py:7903`, operator map at `:7918`) mapped an unknown operator to `"≥"`, so a `ne` gate rendered as *"Elena Affection ≥
50"* — the game stating the opposite of its own rule. Now `"≠"`.

```toml
# Legal today. "She is not at stage 3" — the negated form of the field's
# commonest gate shape (the-surfaces.md R5d).
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "wade_loop_stage", operator = "ne", value = 3 },
] }
```

### ⚠️ Quest cards reject `ne` on purpose — do not "fix" the whitelist

`[[quest_cards]]` conditions **are** whitelisted (`template_import.py:5509`, `gte/lte/gt/lt/eq`) and
their evaluator, `setup.checkQuestsCondition`, has no `ne` case — its `switch` falls through to
`return false`. Widening that whitelist without adding the case would let an author write a card
condition that is **silently always false**, which is the failure this engine has had before with
`conditions` lacking `version = "1.0"`.

Widening it correctly means the whitelist **and** the evaluator, in the same change. The comment at
`template_import.py:5502-5509` says so at the site.

Also unchanged, and for the same reason — each is its own path:

- `template_import.py:5315` — hint `trait_checks`.
- `template_import.py:5242`, checked at `:5265` — hint-template `stage_op`, `{eq, gte, lte}`.
- `template_import.py:5877` — a **heuristic** threshold reader, not a validator. `ne` is not a
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

Added 2026-08-28, because `the-release.md` § Shipping the build began requiring this field and a grep
of the whole skill — references, templates, scripts — found **zero** mentions of it outside that one
new section. The doctrine was asking for something the skill had never taught.

Both keys are **optional** and live in `[project]`, alongside `id` / `title` / `starting_canvas`:

```toml
[project]
version      = "0.1"
release_date = "2026-08-23"
```

The path from the TOML to the screen, traced end to end:

| step | where |
|---|---|
| read off `[project]`, defaulting to `""` | `template_import.py:1706` |
| copied onto the project's metadata | `template_import.py:6402` |
| escaped, then joined with ` · ` | `v2.py:16325-16326`, joined at `:16328` |
| composed into the `versionFooter` widget | `v2.py:16333-16336` |
| called unconditionally from `StoryCaption` — both variants | `v2.py:16356` and `:16371` |

Rendered as `v0.1 · 2026-08-23` in a `<div class="sidebar-version">` under the sidebar.

**Three facts that matter and are not guessable:**

1. **The widget is ALWAYS defined, even when both keys are empty** — it just renders nothing. The
   ternary at `v2.py:16333-16336` emits an empty `<<widget "versionFooter">><</widget>>` rather than
   nothing at all. Deliberate: SugarCube throws on a call to an undefined widget, and `StoryCaption`
   calls it unconditionally in both its variants (`v2.py:16356`, `:16371`) — same reason the
   cheat-page and cast-page widgets are emitted outside their own feature blocks.
2. **`html.escape` runs on both** (`v2.py:16325-16326`), so a stray quote in a date string cannot
   break the build.
3. **There is no build badge.** There is one build, and what a player needs to identify is the
   RELEASE — it is what their guide's codes are scoped to. The version string does that here and in
   the cheat page's heading (`v2.py:16329-16331`).

### Why it is not cosmetic

This is the **only** release identifier a player can read without leaving the game, so it is one of
the three places that claim to say what shipped — with the portal's `version` and the archive under
`games/<slug>/releases/`. `gates.py --release` checks that all three agree, and the first run found
one game reading `0.1` on the portal while printing **`0.1.2`** to the player.

### Where the rule lives

`the-release.md` § Shipping the build, step 4.


---

## 39. `time_of_day` — the hour window, and the only predicate that is a window rather than a latch

```toml
{ type = "time_of_day", start_time = "22:00", end_time = "06:00" }   # overnight, wraps midnight
{ type = "time_of_day", start_time = "11:00", end_time = "20:00" }   # ordinary daytime window
{ type = "time_of_day", start_time = "18:00" }                        # no end ⇒ exactly one hour
```

Shipped 2026-08-29. The runtime branch is at `v2.py:4128`; its lock text at `:7915`. `HH:MM`,
24-hour, **end exclusive** — `11:00`–`20:00` is false at 20:00 exactly.

**It delegates.** The branch is four lines and calls `setup.isCurrentTimeSlot`
(`v2.py:3856`) — the same function NPC and location schedules have used since the schedule
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
`ps.triggered_conversations[conv.id]` (`v2.py:2202`) is written the first time the trigger passes
and never re-read. So on a phone conversation this predicate means *"deliver this the first time she
is awake at 2am"*, not *"this thread only exists at 2am"*. On a canvas trigger, which is evaluated
fresh, it means the second. **Know which surface you are on.**

⚠️ **No weekday form.** `[[schedules]]` rows carry a `weekdays` list; this predicate does not. "Only
on Saturday" is still unbuildable as a condition. Not measured, so not built.

⚠️ **Unlike every `worn_*` predicate it carries no `_enabled` guard**, and must not grow one — the
clock is initialised in every build (`time_state` in `$game_state`), including builds with no
schedules, no phone and no clothing.

**Verified live in a built game, not just read.** Ten cases through a real browser against
`late_shifts` rebuilt with an overnight condition on a phone conversation: 23:00 and 02:00 inside
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
same Python dicts that are handed to `setup.stateDefaults` (`v2.py:3244`), so the defaults cannot
fall behind what a fresh game starts with. They used to be two hand-maintained string blocks and a
three-key dict, which is exactly how turning the phone on in a patch release left
`$game_state.phone` undefined in every existing save with no build error anywhere.

**`setup.backfillStateDefaults`** (`v2.py:16011`) is called from the `:passagestart` handler
(`v2.py:16164`) on **every passage**. It fill-if-absent merges the defaults into `State.variables`,
never overwrites an earned value, is idempotent, and hands out deep copies so a player's state can
never alias the shared default object.

**The depth is not uniform, and the asymmetry is load-bearing:**

| | depth | why |
|---|---|---|
| `$flags` | keys | — |
| `$npcs` | whole NPC, then `core_traits` / `flags` | a missing NPC arrives entire |
| `$game_state` | top level **and one level into a sub-map** | every non-empty default there is engine bookkeeping (`phone`, `rent_state`, `fast_jobs`, `bank`, `time_state`); the player-owned maps all default to `{}` so there is nothing to fill into them |
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

**The stamp and the hook.** `Config.saves.id` (`v2.py:3208`) is pinned to the template slug rather
than the SugarCube default `slugify(StoryTitle)`, so a title change does not orphan **exported**
saves — the in-browser slot namespace is still title-derived and still strands
(`SimpleStore.create(Story.domId, …)` in `format.js`). `Config.saves.version` (`:3209`) is a sha1
over the trait/flag key surface and the corruption tiers. `Config.saves.onLoad` (`:3230`) compares
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

Tests: `apps/game_generation/tests/test_save_migration.py`, 23 of 23 — which execute the emitted
migration in node against synthetic old saves rather than grepping for it.

---

## 41. Five facts a build cost one round each, 2026-08-31

All five surfaced translating a signed design into TOML for `night_desk` 0.0.1. Each cost exactly one
build or one gate run, and none of them is guessable from the schema.

### 41a. `op = "sub"` parses, imports, builds — and does nothing

`applyTraitEffect` runs `['add', 'set']` and nothing else (`v2.py:5742-5751`). A `sub` effect is
valid TOML, survives the importer's dataclasses, reaches the generator and is discarded at runtime.

**To take something away, write `op = "add"` with a NEGATIVE value.** A quantity like `money` also
needs `clamp = false`, or the default 0–100 clamp (`v2.py:5928-5930`) eats it.

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

`template_import.py:1361` is the quest side. Writing `trait_key` in a quest card fails validation
with *"condition item must set either `flag` or `trait`"*, which names the key it wants and gives no
hint that the other half of the same file uses a different one.

### 41c. A quest goal needs a `label`; every card needs a `when`

- `goals[]` items are refused without `label` — *"it renders next to the ◯ bullet"*.
- A card with no `when` is refused outright: *"Every card must scope itself to a state-window."*

Both are hard validation failures, and both come after 41b, so a first quest-card block typically
costs three build rounds rather than one.

### 41d. `hide_value` on a sidebar item does not hide the value

The suppression is `[[traits.labels]] hidden = true` and nothing else — §30 above says so, and it is
worth repeating here because the wrong key is the obvious guess. `hide_value` parses, imports,
builds and does nothing; the auto Traits dump keeps printing the bare number under the band.

### 41e. `_is_free` reads the TRIGGER, never the inner choices

Not an engine fact but a scoreboard one, and it belongs beside them because it costs the same rounds.
`gates.py:2913` decides a rung is farmable from **the way in**: `trigger.costs`,
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
                                  (template_import.py:906-913, built named-only at :2302-2310)

[canvases.trigger] npc = …      → TemplateTrigger.npc (template_import.py:642)
                                  → game_graph.py:311  "npc" into trigger metadata
                                  → v2.py:11656        read back out
                                  → v2.py:11713        emitted as help_data npcId
```

**With `npcId`** — `selectNpcPortraitCanvasesForLocation` (`v2.py:4651`) and `renderNpcPortraits`
(`v2.py:5114`) claim the canvas. The renderer then applies the only real presence check in the
engine: the character must have a declared `[[npcs.schedules]]` and `getNpcLocation` must put them
where the player is standing right now (`v2.py:5176-5179`). It draws the portrait and prints
`$npcs[…].name`.

**Without it** — `renderSoloActivities` does not skip the canvas (`v2.py:5259` skips only canvases
that *have* an `npcId`), so it renders as an ordinary activity button carrying the canvas's own
`displayName` (`v2.py:5290`). No face, **no presence check at all**, and the author-facing title
becomes player-facing text. `requires_npc` does not cover the gap — §31 above, and it is read on
exactly two paths, `v2.py:5343` and `v2.py:5486`.

⚠️ **One location shows ONE canvas per character.** The renderer gathers every valid repeatable
canvas per NPC and keeps the highest `priority`, preferring affordable over cost-blocked
(`v2.py:5125-5158`). Three Ray surfaces in one kitchen render as one Ray, not three rows. Set the
priorities deliberately: an escalation at 7 above a hub at 6 replaces the hub whenever its conditions
hold, which is usually what you want and is never what you get by accident.

⚠️ **A non-repeatable canvas renders no portrait either** (`v2.py:4662` skips
`!c.isRepeatable`), which is what keeps a meeting from leaking onto the screen as a face — see
`the-first-hour.md` F5b.

**Measured:** `orientation` wrote `npc` one level too high on all thirteen character surfaces. Every
entry in its built `help_data.locationCanvases` carried `npcId: null` and `canvasIdToNpcUuid` was
`{}` — zero portraits in the whole game, thirteen ungated surfaces, and `Sit with @ray` as a link
label. The build was green and the scoreboard read 43/44, because the gate that checks hubs
(`every hub is met first`) starts by counting portrait hubs, found none, and reported **n/a**. The
gate `no canvas key is discarded` exists so that cannot recur — widened from `npc` alone within
the hour, when the same misplacement turned up as `substitution_only` on `orientation`'s walk-in and
on **all five** of `night_desk`'s, each of them rendering as a clickable activity instead of a
dispatcher-only target.

---

## 43. Where `@` tokens resolve, and where they do not

`@player`, `@player.<field>`, `@<npc>` and `@<npc>.rel` are resolved by
`_resolve_at_references` (`v2.py:14646`) and, for link text, `_resolve_at_references_expr`
(`v2.py:14693`). **Both are called on four things and nothing else:**

| resolved | site |
|---|---|
| block `content` — paragraph, heading, dialog, thought_bubble | `v2.py:15193` |
| `locations[].description` | `v2.py:9864` |
| a location's `blocked_message` | `v2.py:9793` |
| choice `text` | `v2.py:13256` |
| `npcs[].role` — the label under the name | `v2.py:15272` (added 2026-09-02) |

Every other author string is emitted verbatim. The ones that reach a player:

| NOT resolved | where it shows up |
|---|---|
| `canvases[].name` | the solo-activity link label (`v2.py:5290`), the quest card's `canvas_name`, the canvas `<h2>` |
| `npcs[].description` | the CustomizeCharacters screen — `html.escape` only, `v2.py:9312`. This is the game's **first** screen |
| `quest_cards[].tip` · `.ready_text` · `.terminal_text` | the guidance page |
| `canvases[].description` | dev surfaces only (`CanvasReview_*`, the `--debug` canvas banner) |

⚠️ **`npcs[].role` was static until 2026-09-02 and that was wrong for the case it matters most in.**
A `customizable` NPC with `relationship_options` is one the PLAYER decides the relation for, so the
label under their name has to be theirs: `role = "@<npc>.rel"` prints the option they picked and
follows a change. It shipped static, and the game with two renameable characters consequently
labelled a stepfather *"owns the house"*. Escape first, then resolve — `html.escape` touches no
character the token regex reads, so author markup is still neutralised and the macro comes through
live. `the-first-hour.md` F10.

**The rule: a token belongs in prose. Anywhere else, write the role.** `"His son"` and
`"Sit with him"` survive a rename; `"@ray's son"` and `"Sit with @ray"` print the token.

⚠️ **This bites hardest exactly where customization is on.** `v2.py:9294` emits a name textbox for
every customizable NPC unconditionally, so those characters *must* be referred to by token in prose —
which trains the author to reach for `@ray` everywhere, including the four fields above.

**Measured across all 26 games: 9 player-facing leaks in 2 games, 24 clean.** `orientation` 7 — four
canvas names, Wes's `description` on the character-creation screen, and two quest cards. `commuter`
2 — `hub_cole_room` and `hub_ray_garage`, both shipped, both printing the token as the room's link
label. Two customization games, both leaking, and nothing in the toolchain said so until this lint
existed.

> **Linted as `a token the engine never resolves`** — a LIST, never a score. It walks the merged TOML
> and reports any `@` reference sitting outside the resolved set, dev-only fields reported separately
> from player-facing ones.

---

## 44. The door — `[locations.door]`, a threshold she lands on instead of the room

Shipped 2026-09-02. Opt-in and **inert when unauthored**: a game that declares no door builds
byte-identical output, verified over 27 builds. `the-map.md` R6–R6c owns *when* to use one; this
section is the mechanism.

```toml
[[locations]]
id   = "the_back_bedroom"
name = "Ray's Room"

[locations.door]
description = "The door at the back of the house."
no_answer   = "You knock. Nobody comes to it."
# optional, same shape and same evaluator as [[locations.description_variants]]
description_variants = [ { conditions = { version = "1.0", ... }, text = "..." } ]

[[locations.door.options]]
text       = "Knock."
conditions = { version = "1.0", logic = "AND", items = [
  { type = "npc_at_location", location_id = "the_back_bedroom", npc_id = "npc_ray",
    operator = "is_present" },
] }
goes_to    = { type = "canvas", canvas_id = "ray_knock" }

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
