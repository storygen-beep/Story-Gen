# Doc 73 — The Door Screen: Engine PRD + Skill Doctrine + First Consumer

**Date:** 2026-09-02
**Status:** PRD — not implemented. Ready for an implementation session.
**Author:** ENI (with LO)
**Triggered by:** LO, on finding `orientation`'s Ray's Room shipped a row called "Go in" whose only
choice, "Knock.", unlocks into nothing — *"is it supposed to be locked??"* — then
*"lets build a complete new locked location system for this feature"*, then
*"dont include skill and the game gen engine changes in the spec yet. We will research on top games
and study them on how they use it first."*
**Evidence base:** `~/Documents/Door_Study_20260902/` — 27 shipped sandboxes, 67,845 passages, ten
probes. Every field figure below is reproducible from that folder.
**Scope:** one engine primitive (`[locations.door]`), one `gates.py` lint, one doctrine rule family
(`the-map.md` R6), and `orientation` as the first consumer.
**Supersedes:** nothing. Additive. The existing `entry_conditions` + `blocked_message` lock is
**not modified** — see §6.
**Cross-references:** `references/the-map.md:210-224` (the four location fields) · `engine.md §22`
(`:725-774`) · `the-surfaces.md` R5c/R7 (a blocked row says a sentence) · `the-systems.md` SY6 (the
precedent for specifying a thing and not building it).

---

## §1 — Why this PRD exists

The engine can lock a room and it can say why. It cannot let the player **do anything at a locked
door**. `_render_location_nav_card` emits a `<div>` for a locked destination (`v2.py:20110`), and the
blocked passage behind it carries one hardcoded `[[Go back]]` (`v2.py:9805`). There is no knock.

That is the hole `orientation` fell into. Ray's Room has one row, and its locked choice routes to
`Location_the_back_bedroom` with `advanceTime(20)` and **zero effects** — a door that opens onto
nothing (`games/orientation/output/index.html:10651`). The room ships **31 words against a declared
3,000**, the one FAILing gate in that game.

The 2026-09-02 field study confirms the mechanism exists in shipped games, and **corrects the design
we would otherwise have built**. Its findings are §2.

---

## §2 — What the study settled

| # | finding | evidence |
|---|---|---|
| 1 | **The threshold is real.** 75 threshold screens across **10 of 27** games. | `d1_thresholds.py` |
| 2 | **The split is WHOSE PLACE IT IS**, not whether the door is locked. Someone else's home → a screen. A shared room in her own house → no screen; occupancy is a branch inside. | `d3_occupied.py`, `d5_house_doors.py` |
| 3 | **The screen is never skipped.** `become-someone`: 54 door screens, **50 gate on occupancy**, 46 on occupancy + time of day, median **14 words**, 53 of 54 carry a way back. | `d5_house_doors.py` |
| 4 | **What is conditional is whether the door EXISTS**, not whether it renders. DoL: `<<if $whitney_home_stage gte 3 …>>` on the street link. | `Barb Street`, hand-read |
| 5 | **Doors are rare.** DoL: **six named doors** (47 icon sites, 30 passages) in a 15,626-passage game. | `d8_dooricon.py` |
| 6 | **The map says "this is a door" before you click** — `<<dooricon>>`, 10 cases including `locked` and `open`, and it rides on *leave* links too. | `Widgets Icon Img` |
| 7 | **Entering is downstream of knocking.** `Whitney Home Enter` is reachable ONLY from `Whitney Home Knock`. No bypass. | `refs.py` |
| 8 | **The threshold is free; travel and knocking cost.** `[[Whitney's flat (0:02)\|Whitney Home Knock]]<<pass 2>>` — the 2 minutes is on the street link. The knock passage does no `<<pass>>`. Its exits do. | hand-read |
| 9 | **The refusal is a stock one-liner.** Median **8 words**, the same sentence 44 times: *"You knock on the door, but nobody came."* Ours run 22 and are bespoke. | `d7_refusal.py` |
| 10 | **A locked door is usually actionable.** 229 passages say locked; **105 labels** act on it — *Break in (0:05)*, *Pick the lock*, *Use the key*. | `d4_locked.py` |
| 11 | **Occupancy can be a stated risk, not a lock.** `new-life-project`: *"Search the living room"* expands to **"Tyson is in there."** in red, then *"Search anyways"*. | `tysonBack`, hand-read |

### What this changed about the pre-study design

- **The "skip the screen when the only live option is enter" rule is DELETED.** The field never
  skips (finding 3). Rarity, not skipping, is what stops the two-click tax (finding 5).
- **`doorScreenWarranted` is not built.** The nav card links to the door, unconditionally.
- **The doctrine line moved** from *is it locked* to *whose room is it* (finding 2).

### One deliberate departure from the field

LO wants **knock available on an open door**, so `Knock` and `Go in` can both be live on the same
screen. The field does not do this — `katehouse` offers only *Knock*, and entering is what it earns.
Recorded as an authored decision, not a borrowing.

---

## §3 — The design

A location gains a **third independent fact**. It already has two.

| fact | field | today |
|---|---|---|
| is anyone inside | `npc_at_location` conditions | exists (`v2.py:4308`) |
| may she enter | `entry_conditions` + `blocked_message` | exists (`template_import.py:177-178`) |
| **is there a door** | **`[locations.door]`** | **new** |

They compose without a state table:

```
door + someone in           -> knock. Go in too, if the author declared it and it is live.
door + empty + unlocked     -> the door screen with "Go in" on it.
door + empty + locked       -> the door screen, "Go in" shown locked, its reason on it.
door + nothing live         -> the door screen with `no_answer` and a way back.
NO door                     -> today's behaviour, byte-identical. Kitchen, street, quad.
NO door + entry_conditions  -> today's greyed card. The mall at midnight; vesper's eleven.
```

### The TOML

```toml
[[locations]]
id   = "the_back_bedroom"
name = "Ray's Room"
entry_from = "the_avenue"

# The presence of this table is what makes the location a threshold.
[locations.door]
description = "The door at the back of the house."
no_answer   = "You knock. Nobody comes to it."
# optional, same shape and same evaluator as [[locations.description_variants]]
description_variants = [
  { conditions = { version = "1.0", logic = "AND", items = [ ... ] }, text = "..." },
]

[[locations.door.options]]
text       = "Knock."
conditions = { version = "1.0", logic = "AND", items = [
  { type = "npc_at_location", location_id = "the_back_bedroom", npc_id = "npc_ray",
    operator = "is_present" },
] }
goes_to    = { type = "canvas", canvas_id = "ray_knock" }

[[locations.door.options]]
text             = "Go in."
conditions       = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "appetite", operator = "gte", value = 70 },
  { type = "flag",  subject = "player", flag_key = "ray_open", operator = "is_true" },
] }
show_when_locked = true
locked_text      = "You could knock. …"
goes_to          = { type = "enter" }
```

**Two option types only: `enter` and `canvas`.** `leave` is implicit and always rendered last.

### Three properties that are load-bearing, not preferences

1. **An option carries no `costs` and no `time_progression_minutes`.** The door screen performs **no
   state writes of any kind**. This is required, not stylistic: `setup.isRerenderSafe`
   (`v2.py:16110-16124`) only permits a committed post-render state on a passage whose body is a pure
   render, and a save parked on a door must survive a reload. Cost lives on the far side — a
   `canvas` target charges via its own `trigger.costs`; an `enter` target charges via the location's
   `entry_costs` through the existing travel intercept. This is also what the field does (finding 8).
2. **`Door_*` is NOT added to `passage_to_location`** (`v2.py:1024-1030`). That keeps the travel-cost
   intercept (`v2.py:15957`) and the clothing check (`v2.py:1920`) off the threshold, so the door is
   free *by construction* rather than by a rule someone must remember.
3. **Defaults come from the location, so a lock is declared once.** An `enter` option with no
   `conditions` inherits the location's `entry_conditions`; with no `locked_text` it inherits
   `blocked_message`.

---

## §4 — Engine: the importer

`apps/projects/services/template_import.py`

**4.1 · One field, a raw dict.** ⚠️ **CORRECTED 2026-09-02 during item 1.** This section first
proposed `TemplateLocationDoor` + `TemplateDoorOption` dataclasses. Dropped. The two closest fields
on the same dataclass — `clothing_rules` (`:189`) and `description_variants` (`:198`) — are raw
passthroughs validated in `validate()`, and typed records here would need a `_serialize_door` step in
**both** writers (§4.3), which is one more place for the two paths to drift. The validator carries
the whole contract either way.

```python
door: Dict[str, Any] = field(default_factory=dict)      # on TemplateLocation, after :198
```

**4.2 · Parse** inside the existing `for l in locs_raw:` loop (`:1882-1905`), building the door
before the `TemplateLocation(...)` call exactly as `npc_schedules` is built at `:1782-1799`. There is
**no closed-key check anywhere in this file**, so an unparsed `door` key is silently ignored today —
which is why the parse line must actually be added, and why no existing game breaks.

**4.3 · Write out — TWO SITES.** ⚠️ **CORRECTED 2026-09-02 during item 1.** This section first
named only the Django path. There are two near-identical location loops, and **the one a real build
uses is the other one**:

| path | site | used by |
|---|---|---|
| DB | `template_import.create_project_from_template` `:6940-6968` | the Django admin path |
| **no-DB** | **`apps/projects/services/game_graph.py:199-211`** | `twee_comprehensive/services.py` and **every** no-DB test |

Both take the same line, before `loc.save()` / `slug_map[l.id] = loc`:

```python
if l.door:
    loc.properties["door"] = l.door
```

**A door written only to the DB path parses, validates, and silently never reaches the generator.**
Same defect class `v2.py:9858-9861` already records for the two location emitters — *"byte-identical
copies… that is how a change like this gets half-applied."* `test_location_door.py`'s
`test_both_writers_carry_the_door` greps both modules so they cannot drift apart quietly.

**4.4 · Validate** in `validate()` (`:3256`) — which **accumulates strings into `errors`, it does not
raise**. Insert after the per-location `costs` loop ends (`~:4342`), before
`# ===== Story validation` (`:4344`). Style copied from the `description_variants` loop
(`:4306-4329`). Registries already built in scope: `canvas_ids` (`:4345`), `loc_index` (`:4073`).

| # | refuse | why |
|---|---|---|
| V1 | a `door` with zero `options` | a threshold with no way through is a wall the author did not mean |
| V2 | an option with empty `text` | it renders as a blank button |
| V3 | an option `conditions` block missing `version = "1.0"` | **the fail-open trap** — `engine.md:763`; without it the option renders forever and the gate never bites |
| V4 | `goes_to.type` not in `{enter, canvas}` | typo protection; the generator would emit a dead link |
| V5 | `goes_to.type == "canvas"` with a `canvas_id` not in `canvas_ids` | same idiom as `:4646-4649` (`locationId not found in locations`) |
| V6 | `show_when_locked = true` with neither `locked_text` nor a location `blocked_message` | a mute locked row is exactly what gate 42 *a locked door says why* exists to prevent |
| V7 | a `door` on a location with `auto_exit = false` | a transit stop takes no nav card (`v2.py:20156-20159`), so its door would be unreachable |
| V8 | a `door` on a location that is `offscreen` or `is_container` | offscreen has no card; a container swallows |

---

## §5 — Engine: the generator

`apps/game_generation/twee_comprehensive/generators/v2.py`

**5.1 · Runtime payload.** `locations_map` (`:1012-1021`) gains a `door` key — **absent, not
empty, when unauthored**, and carrying every option's target already resolved to a passage name
(`_door_for_payload`).
Serialized at `:1066`, emitted at `:3247` as `setup.locations`. It reads `loc.properties`, which is
fed by **both** writers of §4.3 — the graph one on a real build. Default `{}` → no door → today's
behaviour, which is the backward-compat guarantee expressed in the data rather than in a branch.

**5.2 · The door passage.** New method `_render_door_passage(location)`, emitted from
`_generate_simple_locations` (`:9695-9847`) for every location carrying a door. Passage name
`Door_<slug>`, using `_location_nav_slug` (`:20080`) so it is **stable across renames**, the same
reason `_location_passage_name` (`:12389-12395`) uses the slug. The `Door_` namespace is confirmed
free across all built games.

```
:: Door_<slug>
<h2>{location.name}</h2>
{door description — the same <<if>>/<<elseif>>/<<else>> variant chain as
 _render_location_description (:9848-9883); factor the chain builder out and call it with the
 door's own description + description_variants}
<<= setup.renderDoorPresence("<loc_id>")>>          ← thin wrapper on getNpcsPresentAtLocation (:4948)
<<= setup.renderDoorOptions("<slug>")>>
<div class="location-nav-exits">
[[Leave->{self._get_smart_exit_destination(location.entry_from)}]]
</div>
```

**No `<<nobr>>` state block, no `$player.current_location`, no `visited_locations.push`, no
`<<pass>>`, no `_autoFire` redirect.** She is not in the room. Property 1 of §3.

**5.3 · `setup.renderDoorOptions(slug)`** — new JS, modelled on `renderSoloActivities`
(`:5280-5322`), which is the function whose markup a room's activity list already uses:

```
for each option in setup.locations[slug].door.options:
    live = !opt.conditions || setup.triggerConditionsSatisfied(opt.conditions)
    if live:
        <a class="link-internal solo-activity-btn" data-passage="TARGET">TEXT</a><br>
    else if opt.show_when_locked:
        <span class="solo-activity-cooldown">TEXT — <em>LOCKED_TEXT</em></span><br>
if nothing rendered:
    <p class="entry-blocked-narrative">NO_ANSWER</p>
```

`TARGET` is resolved at **generation** time by `_door_for_payload`, so the runtime never has to
know how a passage is named: `Location_<slug>` for `enter`, or the canvas's entry passage for
`canvas` — `self._node_passage_name("Canvas", canvas_prefix, first_node)`, the same expression that
fills `help_data.locationCanvases[].passageName`.

⚠️ **KNOWN LIMIT, found during item 2.** The importer proves the canvas exists in the TOML (V5), but
a canvas with **no trigger and nothing referencing it** is pruned by `_compute_included_canvases`
before the generator sees it, and a door option is not yet one of the references that closure walks.
Adding it means touching that function **and its no-DB twin**, so it is deferred. Until then the
option is **dropped rather than left pointing nowhere**, and the drop is a `logger.warning` naming
the option, the location and the canvas. The fix an author needs is one line: give that canvas a
trigger location.

**5.4 · Every engine-generated way IN — FOUR sites, not two.** ⚠️ **CORRECTED 2026-09-02 during
item 2.** This section named the nav grid and the nav text list. There are two more: `::
Navigation` carries a second, flat list of every location, in two branches. It linked straight into
the room, so a player could reach Ray's bedroom **without ever seeing his door**.

All four now go through one helper, `_location_entry_passage(loc)` — `Door_<slug>` when the location
has a door, `Location_<slug>` otherwise:

| site | |
|---|---|
| `_render_location_nav_card` | the grid; emits **only the open card**, no `navDestUnlocked` fork |
| `_render_location_nav_link` | the text list, same |
| `_generate_basic_navigation` | the no-connections global list |
| `_generate_basic_navigation` | the initial-selection list |

Deliberately **NOT** routed: the *"Back to \<name\>"* link on the same screen (she is already
inside, and bouncing her onto her own threshold is a loop, not a door), and any authored canvas
exit, which goes where the author said.

A door location's card is therefore always clickable — which is the whole point, since you can knock
at a door you may not enter — and it **keeps its presence badges for free** (`:20101`), closing the
"you cannot see who is in the room you are locked out of" gap without a CSS change.

**5.5 · `setup.isRerenderSafe`** gains `if (title.indexOf("Door_") === 0) return true;`
Legitimate only because of §3 property 1.

⚠️ **CORRECTED 2026-09-02 during item 2.** That block is a **plain string assembled by
concatenation**, not an f-string — a `{placeholder}` in it is emitted literally. Injected the way
its neighbour already is: `""" + door_rerender + """`.

**5.5b · EVERY door site is gated on `_has_doors()`.** ⚠️ **ADDED 2026-09-02 during item 2, after
the first cut failed its own inert proof.** Emitting the renderer, the `isRerenderSafe` clause and
the payload key unconditionally moved **all 26 built games by ~2.7 KB** for a feature none of them
uses. All three are now conditional, the same rule the travel-friction block follows a few thousand
lines down — *"only emitted when some location declares costs; otherwise movement stays free."*
The inert proof is what caught it, which is the entire reason it is in the verification list.

**5.6 · Do NOT touch** `passage_to_location` (`:1024-1030`). §3 property 2.

**5.7 · CSS: nothing new.** Every class already exists and is already used elsewhere:

| element | class | line |
|---|---|---|
| the door line | `.entry-blocked-narrative` | `:19165` |
| an available option | `.solo-activity-btn` (+`:hover`) | `:18447`, `:18459` |
| a shown-locked option | `.solo-activity-cooldown` (+` em`) | `:18507`, `:18516` |
| the options container | `.location-solo-activities` | `:18441` |
| who is behind the door | `.nav-npc-badge` | `:18298` |
| the way back | `.location-nav-exits` | existing |

The door screen therefore renders as a room screen with a short list, which is what it is. No new
surface for a player to learn.

**5.8 · DEFERRED, specified only** — `appears_when` on `[locations.door]`: a conditions block that
decides whether the nav card renders **at all** (absent, not greyed), which is the field's real
conditional (finding 4: `$whitney_home_stage gte 3`). Not built this round: `orientation`'s three
doors are always visible, and an always-visible door is the simpler thing to get right first. Marked
with the same ⚠️ convention as `the-systems.md` SY6 so no author designs against it.

---

## §6 — What must NOT change

**6.1 · Inert without a door.** Every one of the 18 built games must emit **byte-identical** output.
This is the property `test_location_description_variants.py` was written to protect for its own
feature, and it holds here for the same reason: this ships into a repo with games in it, one of them
public.

**6.2 · The existing lock is untouched.** All 11 of vesper's locked locations are story-progress
flag/trait gates — *"Mercer hasn't sent her up there yet"*, *"the penthouse is the Chairman's ground
now"*. Not one is a door with a person behind it. **They must all keep rendering as today's
un-clickable greyed card.** That is LO's mall case, and the study confirms the field agrees: a
place that is closed is not a door.

Only one location in all 18 games locks on occupancy — `night_desk` `the_office`. It is out of
scope; `night_desk` is frozen by LO's 2026-09-01 instruction.

**6.3 · It cannot fail open.** V3 in §4.4. An option whose conditions omit `version = "1.0"` renders
forever, which is worse than having no door.

---

## §7 — `gates.py`: one lint, no gate

**`lint · a door opens onto something`.** LO's call, 2026-09-02: prints, never scores. Consistent
with `the-systems.md`'s precedent — no defensible field threshold exists for doors, and a count is
satisfied by declaring more.

Template: `lint_labels_and_systems` (`:1730-1806`). **Three wiring sites, all required:** the call
(`:8373`), the print block (`:8537-8549`), the `--json` key (`:8412`).

Lists — a LIST, never a score:

1. a door where **no option is ever reachable** — every option gated on a flag no canvas sets
2. a door whose only option is `enter` — **that is not a door, it is a room**
3. a door on a location **no character is ever scheduled at** — a knock nobody can answer
4. the game's **door ratio**, reported not judged: doors per location, against the field band
   (DoL 6 named doors in 2,760 room screens; `become-someone` 54 in 3,277 passages)

⚠️ **`SKILL.md` must gain the lint name in the same commit.** `--selfcheck` (`:8206-8320`)
reconciles every `print(f"  lint · NAME — …")` against the lint paragraph at `SKILL.md:287-337`, and
every *qualified* rule reference (`the-map.md R6`) against a real heading. Current baseline that must
be restored after the change: **47 gates · 36 lints · 5 modes · 47 gate rows · 133 rules / 13 files,
0 pointing at nothing, exit 0.**

**Separable, and recommended alongside:** `show_when_locked` choices that carry **no effects, no
flagEffects and no node target** — the exact `orientation` Ray bug, which no gate sees today. It is
not door-specific and it would have caught this whole thread at the build. Ship it or cut it on its
own merits; do not fold it into the door lint.

---

## §8 — Skill doctrine: `references/the-map.md`, R6

**Home: `the-map.md`.** It already teaches the locked door (`:210-224`) and owns the map. Its rule
family runs **R0–R5, so R6 is free**. A new file with a new prefix would split door doctrine from
locked-door doctrine across two files — the defect `the-systems.md` SY2b was placed to avoid.

| rule | says | evidence |
|---|---|---|
| **R6 · A door belongs to a person, not to a room** | A door is a handful per game and it sits on somebody's home. Presence is not the test — 63% of our rooms hold a scheduled person; DoL has six doors in 15,626 passages. | `d8_dooricon.py`, `d5_house_doors.py` |
| **R6b · The door always renders. What is conditional is whether the door exists** | Kills the skip rule before an author invents it. The field never skips (54 of 54, 50 gating on occupancy). Rarity is the answer to the two-click tax. | `d5_house_doors.py` |
| **R6c · A shared room gets no door** | Bathroom, kitchen, front room — she walks in, and occupancy is a **row inside**, which the engine already does. Our own `back_home` ships 13. `orientation` simply did not use it. | `d3_occupied.py` |

**R6 also carries the refusal figure** — field median **8 words**, the same sentence 44 times,
against vesper's 22 and bespoke — and says plainly that **one stock line reused across every door is
allowed**, because the value of the screen is its structure.

**Other files:**

| file | edit |
|---|---|
| `the-map.md:210-224` | the four-field table gains the door row |
| `the-map.md:265-276` | the "what is checked" table gains the new lint |
| `engine.md §22` (`:725-774`) | the `[locations.door]` field block with the `template_import.py` / `v2.py` citations from §4–§5, beside the `entry_conditions` block it extends |
| `the-sheets.md` S2 | the place sheet gains a **DOOR** row beside its LABELS row |
| `SKILL.md:287-337` | the lint name — **required by `--selfcheck`** |
| `CHANGELOG.md` | dated bullet, same turn, per `CLAUDE.md` |

**No `v2_state.json` field.** The lint reads the built TOML. A declare-then-check field would be
machinery with nothing behind it.

---

## §9 — First consumer: `orientation`

Three rooms, and the point of doing all three is that they exercise the three different answers.

**9.1 · `the_back_bedroom` — Ray's Room. The door.**

Delete `act_back_bedroom_door` (`3_activities.toml:757-794`); it becomes `[locations.door]`.

| option | conditions | goes to |
|---|---|---|
| **Knock.** | `npc_ray is_present` (his 01:00–06:00 window) | new canvas `ray_knock` — a scene, per LO's decision |
| **Go in.** | `appetite >= 70` + `ray_open`, `show_when_locked`, keeping the authored locked_text | `enter` |
| *(no answer)* | — | `no_answer`, ~8–15 words per R6 |

Then build what the room was always missing: a **cast surface for @ray inside**, the
`sex/back_bedroom_t5` pool the ledger already declares (`has_cycling_pool: true` against **zero**
media blocks today), and a **trespass row gated `npc_at_location … is_absent`** — the empty-room
content, per the study's finding 11 shape. That is the 3,000-word budget against today's 31.

**9.2 · `wes_room` — Wes's Room. The open door.**

The specimen for LO's one departure from the field. Wes's door being open *is his characterisation* —
the location text says so. So the door screen shows **Knock** and **Go in** both live, and knocking
on an open door is a different beat from walking in. `hub_wes_room` (currently named "Go in") becomes
the `canvas` target of the Go-in option and gets a name that is not the door's.

**9.3 · `the_bathroom` — shared. NO door.** R6c. It already carries four rows including
*"The door opens"*. Leave it; add the occupancy pair if the pass shows a gap.

**9.4 · Also fix while in there** — `3_activities.toml:791-793`, the label *"Go back to your room."*
targets `the_avenue`, not `her_room`.

---

## §10 — Test plan

New file `apps/game_generation/tests/test_location_door.py`, targeting **v2 explicitly** (v1 is
deprecated and a v1-instantiating test stays green while v2 breaks). Run with an explicit path —
`pyproject` sets `testpaths = ["tests"]`, so app suites are not collected by a bare `pytest`:

```
pytest apps/game_generation/tests/test_location_door.py -q
```

Modelled on `test_location_description_variants.py`, whose two load-bearing properties are the same
two here.

| # | test |
|---|---|
| 1 | a location with no `door` emits **byte-identical** output — no `Door_` passage, no `<<if>>` |
| 2 | a location with a door emits exactly one `:: Door_<slug>` |
| 3 | the door passage contains **no** `<<pass`, `<<set $player.current_location`, `visited_locations`, or `_autoFire` |
| 4 | `passage_to_location` contains no `Door_` key |
| 5 | `isRerenderSafe("Door_x")` is true in the emitted JS |
| 6 | a door location's nav card is an `<a>` at `Door_<slug>` with no `navDestUnlocked` fork, and keeps `nav-npc-badge` |
| 7 | a **non**-door locked location still emits the greyed `location-card-locked` `<div>` — the vesper guarantee |
| 8 | option conditions reach the runtime verbatim, `"version": "1.0"` included |
| 9 | V1–V8: each malformed door produces exactly one `validate()` error naming the location id |
| 10 | a `canvas` option's target equals `Canvas_<slug>_Node_<first>` for the named canvas |
| 11 | zero live options renders `no_answer` inside `.entry-blocked-narrative` |
| 12 | a shown-locked option renders `.solo-activity-cooldown`, never a clickable link |

**Whole-repo verification, in order:**

1. `pytest apps/game_generation/tests/ -q` — the existing suite, unchanged.
2. **Hash all 18 built games before and after**, rebuilt from unchanged TOML. Byte-identical is the
   §6.1 guarantee, and it is the proof rather than the claim.
3. `python3 .claude/skills/author-game-v2/scripts/gates.py --selfcheck` → exit 0, back to
   47 gates / 36+1 lints / 5 modes / 133+n rules, 0 pointing at nothing.
4. `gates.py` on all 18 games before and after the **lint** lands — **every verdict unchanged**, by
   construction, since a lint moves no score.
5. `gates.py orientation` after §9 — `location fill` is expected to move off its `-99%` on
   `the_back_bedroom`; nothing else should move.
6. Play the built `orientation` in a browser: enter Ray's Room at 15:00 (no answer), at 02:00 with
   @ray present (knock live), and with `appetite` forced to 70 (both live). The `v2-player` agent
   exists for exactly this.

---

## §11 — Sequencing and effort

| # | item | effort | note |
|---|---|---|---|
| 1 | importer: field, parse, **both** write-outs, V1–V8, **and its own 24 plumbing/validator tests** | ~2.5 h | ✅ **DONE 2026-09-02.** No runtime risk; nothing reads it yet. 27 builds byte-identical. |
| 2 | generator: payload, `Door_` passage, `renderDoorOptions`, **four** nav sites, `isRerenderSafe`, `_has_doors()` gating | ~3.5 h | ✅ **DONE 2026-09-02.** 39 tests; 27 builds byte-identical. |
| 3 | `test_location_door.py` generator half + the whole-corpus hash check | ~1.5 h | **before** any game consumes it. The hash instrument exists and ran clean on 27 builds at item 1. |
| 4 | doctrine: `the-map.md` R6/R6b/R6c + the five satellite edits + CHANGELOG | ~1.5 h | must land with the lint for `--selfcheck` |
| 5 | `gates.py` lint + `SKILL.md` row | ~1 h | same commit as 4 |
| 6 | `orientation` §9 — three rooms, the Ray scene, the pool, the trespass row | ~3.5 h | the prose is most of this |

**~14 hours, two sessions.** Items 1–3 are one commit and are independently safe: with nothing
declaring a door, the engine's behaviour is unchanged and the tests prove it. Items 4–5 are one
commit. Item 6 is its own.

**Do not start item 6 before item 3 passes.** Authoring against an unverified primitive is how the
`op = "sub"` incident put nine silently-dead canvases into a shipped game.
