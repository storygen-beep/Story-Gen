# Vesper — Locked Design: The Room (Act 2, Captivity)

> **What this doc is.** The design record for Vesper's next chunk — Bastien's captivity of Wren, her
> overload, and Cain's unexplained intervention. It captures (a) the locked design as decided with LO,
> (b) the engine findings that constrain how it can be built, and (c) the build + verification plan.
>
> Everything in §9 was verified on 2026-07-09 by reading the generator, **compiling a purpose-built
> probe game**, and **driving both the probe and the shipped Vesper build in a headless browser**.
> Line citations are exact. Nothing here is asserted from memory.
>
> **Status:** design LOCKED. Not yet authored. `design_book.md` and `authoring_state.json` are
> untouched — this doc is the source of truth for the chunk until authoring begins.

---

## Context — where this sits

The previous chunk (`design_analysis_underworld_hunt.md`) was built and shipped: the hunt through the
underworld — Sol's lead, Rue's Sunday, draining Marsh, the crew's rooms — ending when Bastien's people
take her and he asks *"What are you, really?"*

That chunk existed to answer a mopoga review: *"gameplay boiled down to resource grinding rather than
focusing on the adult content."* The diagnosis was **placement + ratio + roster** — the game ran out of
people before the story was over. The hunt added people. **This chunk is where the cure fully lands:**
it is the densest erotic stretch in the game, and it contains **zero grind.**

It is also the third *distinct* conquest verb, which is the point:

| NPC | Verb |
|---|---|
| Renner | seduce-in |
| Marsh | scheme-and-serve |
| **Bastien** | **she is taken** |

Three identical infiltrations would be the repetition we are trying to kill.

---

## 1. Frame, and the tests it has to pass

She is kidnapped, held in one room she cannot leave, used until her machine begins to come apart, and
then released by a man who will not say why.

Three tests any beat in this chunk must survive:

1. **Is the player getting a scene here, or filling a bar?** A meter that rises by *repeating* scenes is
   a grind bar with porn on it. It would re-ship the exact review, inside the chunk built to cure it.
2. **Does the room have a verb?** A protagonist with no agency, given no input for three in-game days,
   is a cutscene with a timer.
3. **Does she leave changed?** *"And then something happened"* is not an ending.

---

## 2. The beat chain — LOCKED

1. **The grab is rewritten.** The current capstone (`beat_0034`) ends with *"She wakes on the waterfront
   at dawn, sore and whole and released"* (`5_scenes.toml:2380`). That release was wrongly authored and
   is **deleted**. Bastien takes her and she stays taken. The capstone's exit ports her directly into
   the cell instead of `the_waterfront` (`5_scenes.toml:2388`).
2. **She is ported into a sealed room.** No walk, no approach. She wakes there.
3. **She is disarmed.** Bastien strips the drain (`equipped_weapon → 0`). This is the injury, not a
   detail — see §4.
4. **Three shelves of use**, escalating with the meter, Bastien present throughout (§5).
5. **The break.** In the Failing band, mid-scene, her body stops answering.
6. **Cain.** He arrives, furious, and will not say why. He and Bastien argue behind a door.
   **We never show the argument.** He frees her.
7. **She leaves broken.** Her gear returns; the fault does not. ← **chunk ends here.**

Why Cain did it, the repair of her core, and Bastien's alignment reveal are **all later chunks.**

---

## 3. The room

### 3.1 Geography
A single location, `captive_room`, plus one child: **The Door**, which renders as a locked card reading
*"The door does not open for her."* The door never opens — Cain walks her out; she does not walk herself
out. The door exists to be looked at, and (see §9.2) to keep the engine from handing her the whole map.

The room must be a **location**, not a canvas chain, because chance-based interruptions only roll on
location entry (§9.4).

### 3.2 The two verbs

**Sleep.** Advances the day, restores Charge. It also carries a **scripted, guaranteed night use** —
band-selected, so the ladder always climbs even for a player who does nothing but hide in the bed. Sleep
cannot be used to outrun the chunk.

**Attend** (~30 minutes). *Listen at the door. Watch the man on the chair. Hold still and feel the
fault.* This is the **chance-rolled** action: sometimes nothing, sometimes someone comes in. It is not a
resource action — the bed already handles resources.

That pairing is the room's thesis:

> **The only way to learn anything is to make yourself available.**

The player who fills her days sees more content and breaks faster. The player who hides in the bed sees
less and breaks anyway. Both roads lead to Cain. Nobody is punished; the choice is *how much you look at
it.* **Glitch III** fires on the hold-still option.

### 3.3 What the room does not have
No coin. No fighting. No Charge-throttled repeatable actions. No shop, no travel, no NPC schedule.
**If the player can spam an action in that room, it is the wrong action.**

---

## 4. The physics, and the meter

### 4.1 Overload, not depletion
Vesper's established fiction: sex is what *charges* her. The drain fires on an anal finish
(`equipped_weapon = 1` + `drain_charge >= 1`) — a man finishing in her ass is how she *takes* something.
She is a machine that eats sex.

A gangbang therefore does not drain her. **It force-feeds her.** Bastien has taken the drain, so
everything they pump into her has nowhere to go, and the core cooks.

This is why *this* breaks her when a hundred men at The House did not: **the weapon is gone.** Being
disarmed is the injury. The rape is the pressure. It is the drain, inverted — which rhymes with the
capture-instead-of-seduce inversion at the chunk level.

### 4.2 `core_strain` — a **visible** meter
A new player trait, hidden from the traits dump but surfaced in the sidebar as banded text via
`trait_status_text`, exactly like Charge and Condition (`0_systems_spec.toml:96-115`).

Hidden meters work when the player has agency to spend against them. She has none. What she has is a
dial she can watch go wrong, and that dial is the horror of the room.

| Band | Sidebar | The shelf |
|---|---|---|
| 1–24 | `Core: Nominal` | Bastien alone. Establishing ownership. |
| 25–49 | `Core: Hot` | Bastien conducts; the crew rapes her. He watches. |
| 50–74 | `Core: Faulting` | She is being operated, not fucked. |
| 75–99 | `Core: Failing` | The machine is coming apart. |
| ≥ 100 | — | **The break** auto-fires. |

**Bands start at `min = 1`, deliberately.** The renderer emits nothing when no band matches
(`v2.py:15516`), so the Core row is **invisible for the entire game before captivity**, appears the
instant she is first used, and would vanish again if it were ever cured. Zero engine work. (Numbers are
a proposal; ~12–15 strain per use lands the break at 7–9 uses. See §13.)

### 4.3 Charge falls as strain climbs
Each use costs Charge. The bed restores Charge and **cannot touch strain**. Two numbers moving in
opposite directions; the bed fixes exactly one of them. This is also where LO's original *"she's too
drained"* instinct is honoured without breaking the fiction — **overloaded in the core, exhausted in the
body.**

### 4.4 The bands select the shelf
Random interruptions pick *which* scene; the band picks *which shelf it may pick from*. Escalation stays
monotonic no matter how the dice fall. (Exclusive trait bands — `gte X` + `lt Y` — the same ladder shape
as the quest cards.)

---

## 5. The scenes

**Budget: 8–10 distinct scenes** across the three shelves. This is the real cost of the chunk and it is
the correct cost. **If it is three scenes rolled ten times, we have rebuilt the Renner rungs.**

Content is explicit: BDSM, restraint, the crew, gangbang, rape. Nothing is softened.

### Bastien is present all three days
LO's call, and it makes him carry the chunk instead of vanishing from his own arc. He needs a distinct
role per shelf or he is wallpaper:

- **Nominal** — he uses her himself. Ownership, established.
- **Hot** — he conducts. He hands her to the crew and watches. His voice stays in the room.
- **Faulting** — **he sees the machine failing, and does not stop.**

That last line is load-bearing. It is the reason Cain is angry: **Bastien broke something Cain wanted
intact.** Bastien's alignment with Cain stays OFF the page (the saved reveal) — but his *choice to keep
going* is what makes the next chunk's bombshell land.

---

## 6. Cain, and the argument we do not show

He arrives in the Failing band, after the break. He is furious and cannot explain himself — not won't,
*can't*, in a way she registers and does not understand.

**The argument happens behind a door and is never dramatised.** But *not showing it* and *not rendering
her failing to hear it* are different things. It is written as **her failing perception**: two men on the
other side of a wall, and she is too cooked to hold the thread. She catches perhaps four words. One of
them is a name, or a word that should not fit.

That is free suspense, and it is the once-only place the prose is allowed to spend (§8).

Then he frees her. He does not say why. **The chunk ends.**

---

## 7. What she carries out

**Her gear comes back.** `equipped_weapon → 1` on release. Bastien stripped the drain to disarm her *in
the room*; she leaves with it. This is both correct fiction — **the body is damaged, not the equipment** —
and a hard engineering requirement (§9.5: `equipped_weapon = 0` is an unrecoverable dead state).

**The fault does not heal.** `core_strain` freezes where it stopped. Nothing in this release lowers it.
The Cradle takes her Charge back to full and **cannot settle the fault** — that is prose, not a number.

**No mechanical teeth this release.** A permanent debuff with no cure, in a shipped sandbox, is a nerf the
player can never answer. The damage is a *promise*, and the `Core: Failing` row sitting in the sidebar on
every screen is that promise, visible, until the next update pays it. The repair chunk then opens on
exactly this hook instead of starting cold.

**And four words she cannot hold onto.**

She walks out into the same sandbox — Mercer, Renner, the Sunday brothel — with a broken machine and no
way to fix it. The last thing the player has to do is go back to work. Whether that reads as
bleak-and-correct or as anticlimax rests entirely on the end card. **Spend the Tier-3 prose there.**

---

## 8. Register

Per the `author-game` skill, not this doc:

- **The room's ambients, the two verbs, the shelf scenes** → **RTS-flat.** Terse, specific, crude,
  re-readable. Real anatomical language. No environmental sensory ritual. Specificity, not literary
  density.
- **Glitch III, the break, the argument behind the door, the release, the end card** → **Tier-3,
  earned.** These are once-only. The prose may spend.

---

## 9. Engine findings — verified 2026-07-09

Method: read `v2.py`; compiled a probe game (`sealed_probe.toml`, 4 locations as controls) with
`package_from_toml`; drove the probe **and** the shipped Vesper build in headless Chromium.

### 9.1 The teleport is already supported
`exit_block { type = "location", config.locationId }` moves the player anywhere. **The grab capstone does
exactly this today** (`5_scenes.toml:2388`, `locationId = "the_waterfront"`). Changing that one string is
the whole of "port her into the cell." **Zero engine work.**

### 9.2 The seal — works today, with an exact shape
The engine has **no `sealed` / `exit_conditions` / `can_leave` concept anywhere** (importer, model,
runtime — all entry-side only). But there are exactly two things that write into a location's navigation
HTML, and both can be controlled:

```python
# v2.py:18570  — an UNGATED exit link. No <<if>>, no conditions check.
if location.entry_from:
    exit_links.append(f"    [[Leave {location.name}->{smart_destination}]]<br>\n")

# v2.py:18606  — and if nav came out empty, render EVERY location as a clickable card
if not navigation_html:
```

So the room is a pincer: **give it `entry_from` → a free ungated exit link; give it nothing → the whole
map.** There is no third state by accident. There *is* one by construction:

> **`captive_room` has NO `entry_from` and NO `parent`, plus exactly ONE child (`the_door`) attached by
> `entry_from = "captive_room"`, gated by `entry_conditions` on a TRAIT.**

Destinations is non-empty (fallback suppressed); no `entry_from` means no Leave link; the child renders as
a locked, non-clickable card with its `blocked_message`.

**Probe results (compiled + live):**

| Probe | Shape | Rendered |
|---|---|---|
| **A — sealed** | no `entry_from`, one trait-locked child | *only* `The Door — The door does not open for her.` **Zero clickable exits.** |
| **C — control** | `entry_from` set | `[[Leave Leaky Cell->Location_loc_start]]` — raw, ungated |
| **D — control** | no `entry_from`, no children | `All locations:` + every location as a link |

Live: teleported into A, zero clickable links. Flipped the trait → `The Door` became clickable. Zero JS
errors. **Build was green** — there is no reachability validator that objects to an `entry_from`-less
location.

**Two traps, both silent:**

- ⚠️ **Attach the door with `entry_from`, NEVER `parent`.** `_ordered_navigation` explicitly excludes any
  child whose `parent_location` is the location itself (`v2.py:11651`). Setting
  `the_door.parent = captive_room` — the natural thing to write — empties the nav, fires the whole-map
  fallback, and **unseals the room while the build stays green.**
- ⚠️ **Gate the door on a TRAIT, not a flag.** A flag required `is_true` would demand a located setter and
  hard-fail the build (`MISSING HINT`). Traits are never location-checked. And every conditions block
  needs `version = "1.0"` or it fail-opens (`v2.py:3658` returns `true` for any block missing it).

### 9.3 The one thing TOML cannot close: **undo**
`Config.history.maxStates = 20` is emitted at `v2.py:2929`, and **`Config.history.controls` is never
set** — so it defaults to `true` and SugarCube renders the `←` / `→` buttons in the sidebar. (CSS only
hides them when the bar is *stowed*.)

Live-tested on the sealed probe **and** on the published Vesper:

```
in_cell:            Location_cell_sealed
backward_visible:   true
click #history-backward
after_undo:         Location_loc_start
UNDO_DEFEATS_SEAL:  true
```

**One click and she is outside any cell we can build.** Up to 20 times.

**The fix is one line: `Config.history.controls = false`.** SugarCube then removes `#ui-bar-history`
entirely.

- ⚠️ **Do NOT use `maxStates = 1` instead.** `previous()` feeds the Lane-2 random-encounter entry gate
  (`v2.py:5056`); collapsing history would silently break `entry_only_from` across every game.
- `#history-forward` is **not** an escape — after an undo, Forward puts her back *into* the cell.
- `#history-jumpto` is already removed (it requires `bookmark`-tagged passages; there are none).

**Measured, not assumed — two things that are NOT hatches:**
- **Browser Back is safe.** SugarCube v2.30.0 does not push a browser-history entry per moment:
  `window.history.length` stayed at `2` across three `Engine.play` calls, URL unchanged. Browser Back
  simply leaves the document. *(A sweep agent claimed the opposite, citing hashchange. The experiment
  refutes it.)*
- **The sidebar and info pages are clean.** Quests / Stats / Schedules / Flags are read-only with a
  `← Back`; the Flags page cannot write flags. The wardrobe, phone, quest cards and schedule page emit no
  location links.

Saves remain (8 live slots, plus export/import). A player can always load a pre-capture save. That is
ordinary save-scumming, not an engine defect, and is not worth chasing.

### 9.4 Chance-based interruptions work, with no engine change
Every location passage calls `getStoryCanvasRedirect` on render (`v2.py:9422`), which falls through to
`checkRandomEncounters` when no auto-fire wins (`v2.py:4767`). Each activity in the cell returns her to
the cell → the passage re-renders → **the dice roll.** Exactly the loop LO described.

Consequences for authoring:
- **Auto-fire pre-empts the random roll.** So the intro and the break are auto-fire canvases and will
  always win over an interruption. Correct behaviour, free.
- **Auto-fire requires `is_repeatable = false`** (`v2.py:4292` — the selector skips repeatable canvases).
  So the *scripted night use* on sleep cannot be an auto-fire; it lives as a node inside the sleep
  activity, with `group` blocks selecting the band-appropriate prose.
- `random_cooldowns` (skip N visits after one fires) and `max_triggers_per_day` are the knobs that stop a
  double-fire when she returns from sleep.

### 9.5 `equipped_weapon = 0` is an unrecoverable dead state
The swap activity is the only way to change weapons, and both its choices are gated:
`eq 1 → set 2` (`3_activities.toml:899`) and `eq 2 → set 1`. **At `0`, both hide.** She would be
permanently disarmed for the rest of the game, and Renner's re-drain (`equipped_weapon eq 1`) would become
unreachable forever.

→ **Release MUST restore `equipped_weapon = 1`.**

Marsh survives by luck: by captivity `crew_known` is already true, so his anal finish routes to
`finish_ass_paid`, which checks only `crew_known`.

### 9.6 Ship from a clean build
`--dev --debug` adds a `<<devJumps>>` sidebar link, the Canvas Review browser, and a **`goto "Navigation"`**
button that opens a page listing **every location as a raw link.** A clean build has none of these
(verified by diffing the probe against Vesper).

⚠️ **The currently published Vesper is a `--dev --debug` build and carries all three.** The captivity
chunk must ship clean, or the cell has four doors.

---

## 10. Save-safety

**Deleting the release orphans every existing player.** The grab capstone is `is_repeatable = false` and
gated `bastien_revealed is_false`. Everyone who played the shipped build already has `bastien_revealed`
set and is standing on the waterfront. If the grab's exit is simply repointed at the cell, **they never
see the grab again and never reach the new chunk.**

→ Add a one-shot recovery auto-fire at `the_waterfront`, gated `bastien_revealed is_true` +
`captivity_entered is_false`: **they came back for her.** New players never see it (the grab sets
`captivity_entered` on the way in). Two doors, one room.

Other requirements:
- Vesper is **extend-only** — no renaming existing ids, flags, traits, stat scales or the title.
- NPC state survives rebuilds (stable slug ids, no-DB build); player flags/traits backfill.
- Reset the shared sex-loop traits (`sex_stage`, `loop_npc_pleasure`, `sex_finisher_type`, `anal_active`,
  `sex_entry_origin`) on entry **and** on release, or captivity state bleeds into Marsh's Sunday.
- `[engine.daily_tick].flagEffects` supports `op = "unset"` (`0_systems_spec.toml:46`) if any cell state
  needs a per-day wipe.

---

## 11. Build sequence (propose-first; one verified piece per turn)

Source phases → `merge_toml_phases.py` → `package_from_toml`. **Never hand-edit `7_final_game.toml`.**

1. **Engine:** `Config.history.controls = false` (`v2.py:2929` area). The only engine change in the chunk.
2. **Systems:** declare `core_strain` in `player.core_traits`; add the `trait_status_text` sidebar block
   (bands from `min = 1`); hide it from the traits dump.
3. **Geography:** `captive_room` (no `entry_from`, no `parent`) + `the_door`
   (`entry_from = captive_room`, trait-gated `entry_conditions`, `version = "1.0"`, `blocked_message`).
4. **Entry:** rewrite the grab's tail; repoint its exit to `captive_room`; set `captivity_entered` and
   `equipped_weapon = 0`. Add the waterfront recovery auto-fire for old saves.
5. **The room:** the sleep activity (day advance + Charge + scripted band-selected night use); the
   *attend* activity; the intro auto-fire.
6. **The shelves:** 8–10 `trigger_mode = "random"` canvases with `chance`, banded on `core_strain`, each
   applying `+strain` and `−energy`.
7. **The break:** auto-fire on `core_strain >= 100`, `is_repeatable = false`.
8. **Cain:** the argument (her failing perception), the release. Sets `captivity_done`, restores
   `equipped_weapon = 1`, resets the loop traits, teleports her out. New end card.
9. **Merge → green build → live-test → clean rebuild** (no `--dev --debug`).

---

## 12. Verification plan

Green build: flag chains valid (door gated on a trait), every new conditions block carries
`version = "1.0"`.

Headless SugarCube harness:
1. **The seal holds.** Teleport in; assert **zero clickable links**; assert `The Door` renders locked.
2. **Undo is dead.** Assert `#history-backward` is absent after the engine change.
3. **Bands select shelves.** Set `core_strain` to 10 / 40 / 65 / 90; assert only the matching shelf's
   canvases are eligible; assert the Core row is **absent at 0** and present at ≥ 1.
4. **The roll fires.** Return to the cell from *attend* repeatedly; assert interruptions surface and
   respect `random_cooldowns` / `max_triggers_per_day`.
5. **Sleep always climbs.** Sleep-only run reaches the break with no *attend* action taken.
6. **The break fires once**, at ≥ 100, pre-empting any random roll.
7. **Release restores.** Assert `equipped_weapon == 1`, loop traits reset, `core_strain` unchanged, she is
   out of the cell, `Core: Failing` still in the sidebar.
8. **Both cohorts.** Fresh save walks grab → cell. Old-save sim (`bastien_revealed` already true) hits the
   waterfront recovery door and enters the cell.
9. **Zero JS errors** throughout.

---

## 13. Open items for LO

- **Strain numbers.** Proposed: 0–100 scale, ~12–15 per use, break at ≥ 100 (7–9 uses). Band edges as §4.2.
- **The crew.** Named men, or faceless? Named costs casting; faceless costs the "which one flinches"
  texture that *attend* is supposed to reward.
- **The four words.** What she catches through the door. Must not leak the Cain–Bastien alliance.
- **Where she lands on release** — the waterfront, the strip, or the Cradle.
- **Media budget** — 8–10 scenes implies a find-media pass on a new collection.
- **The end card's text** — the chunk's Tier-3 moment (§7).

---

## 14. Explicitly deferred (not this chunk)

- **Why Cain freed her.** The unanswered question is the point.
- **Repairing the core.** Damage only, here. The repair chunk inherits `Core: Failing` as its on-ramp.
  ⚠️ When it is built: **two or three repair sessions, each a scene, not a bar.** The chunk that cures the
  grind must not exit into one.
- **Bastien's alignment with Cain** — the saved bombshell.
- Calloway (Mission 3); The Site; the chip ending.
- **Also still open from the last chunk:** three missing Marsh clips (`videos/sex/marsh_oral.webm`,
  `marsh_ride.webm`, `marsh_anal.webm` — 404 on the live portal).

---

## 15. Skill note

The `author-game` skill has no doctrine for a **sequence in which the player has no agency.** Its lane
model assumes a player who chooses where to go and whom to approach; a sealed room with two verbs is
outside it. The room is designed here from first principles (§1's three tests, §3.2's thesis).

If this chunk works, that thesis — *"an agency-less sequence still needs a verb, and the verb should be
attention"* — belongs in the skill, or the next author who writes a captivity beat writes a cutscene with
a timer.

Separately, the engine's **fail-open navigation** (`v2.py:18606` dumping the whole map; `v2.py:18570`
emitting an ungated exit) is the same bug class as `conditions` without `version = "1.0"` returning
`true`. It builds green and only live play catches it. Worth a hard-fail or a warning, independent of this
chunk.

---

## 16. Dev jumps — fast-testing shortcuts for this chunk

The chunk sits behind the *entire* Underworld Hunt. Reaching it by play means drain Renner → Sol's lead →
work the brothel → scheme Rue on a Sunday → serve and drain Marsh → search the crew's rooms. That is far
too long a walk to test the cell against. We already ship one dev jump (`▶ Renner drain`); this chunk needs
two more.

### 16.1 How the mechanism works (verified)

- **The marker is the trigger.** A canvas is a dev shortcut iff its `trigger.conditions` contains
  `dev_mode_enabled is_true` (`_is_dev_shortcut_canvas`, `v2.py:8232`). Single source of truth for three
  call sites: the **flag-chain validator**, the **hint index**, and the **flag-setter index** all SKIP such
  canvases. So a dev jump may set `crew_known` / `bastien_found` freely — it will never win as their
  canonical located setter, nor pollute quest guidance.
- **⚠️ `--dev` only, NOT `--debug`.** `flags_init_map["dev_mode_enabled"] = True` is written solely when
  `dev_mode` is on (`v2.py:950`); `--debug` sets an independent `debug_mode` flag
  (`package_from_toml.py:164`). In a shipped build the flag is never set, so the canvases are inert **and**
  the `<<devJumps>>` widget is not consulted at all.
- **The sidebar bypasses the trigger.** `<<devJumps>>` (`v2.py:14844`) links to the canvas's **first node
  passage** and reaches it by direct `Engine.play` (`_dev_shortcut_jumps`, `v2.py:8262`). The link's label
  is simply the canvas `name` — hence `▶ Renner drain`.
- **Anchor to a real location.** An unanchored canvas is pruned as unreachable and the sidebar link 404s.
  The anchor is otherwise irrelevant (the sidebar ignores it); it just also renders a dev card in that room.
- **`is_repeatable = true`** so it can never auto-fire and hijack the anchor room
  (`selectAutoFireCanvasForLocation` skips repeatable canvases, `v2.py:4292`).
- **Seeding lives in the exit choice** (`effects` + `flagEffects`), and the jump is a cross-canvas
  `targetType = "node"` reference.

### 16.2 Jump A — `▶ Bastien grab`

Seeds the whole hunt chain and lands on the kidnap capstone (`hunt_the_grab.base`, `5_scenes.toml:2358`),
which — after this chunk's rewrite — ports her straight into the cell. Seeds `equipped_weapon = 1` so that
Bastien has something to take off her.

Sets, stopping deliberately short of `bastien_revealed` (the capstone's own job):
`opening_done`, `renner_fucked_once`, `renner_anal_once`, `renner_drained`, `renner_leads_extracted`,
`hunt_lead`, `brothel_hired`, `crew_known`, `bastien_found`; traits `names_known = 1`, `drains_done = 1`,
`equipped_weapon = 1`, `drain_charge = 1`; `npc_renner.corruption = 60`.

```toml
[[canvases]]
id          = "dev_jump_bastien_grab"
name        = "▶ Bastien grab"
description = "DEV JUMP. Seeds the full hunt chain and jumps to the kidnap capstone (which ports into the cell). Gated dev_mode_enabled; inert in shipped builds."

[canvases.trigger]
location      = "crew_den"          # anchor only — the sidebar link bypasses the trigger
is_repeatable = true                # never auto-fires
is_active     = true
conditions = { version = "1.0", items = [
  { type = "flag", subject = "player", flag_key = "dev_mode_enabled", operator = "is_true" },
] }

[[canvases.nodes]]
id   = "seed"
name = "Bastien grab (dev)"
blocks = [
  { type = "paragraph", content = "Dev jump: seeding the hunt chain and dropping into the grab." },
]
[canvases.nodes.exit_block]
type = "choices"
[[canvases.nodes.exit_block.choices]]
text       = "Jump to the grab"
targetType = "node"
nodeId     = "hunt_the_grab.base"
effects    = [ ... ]      # traits, per above
flagEffects = [ ... ]     # flags, per above
```

### 16.3 Jump B — `▶ Captivity: the break`

Testing the break and Cain's arrival otherwise costs 7–9 uses. This jump lands *inside* the cell one use
short of the threshold, so the next scene tips it.

Anchored at `captive_room`. Seeds everything Jump A does, **plus** `bastien_revealed`,
`captivity_entered`, `equipped_weapon = 0` (disarmed), `core_strain = 95`, and a low `energy`. Exits with
`targetType = "location", locationId = "captive_room"` so the cell renders normally — auto-fires and the
random roll included.

Both jumps live in `6_dev_shortcuts.toml`. Rebuild with `--dev` to see them in the sidebar.

### 16.4 The release build

These jumps are exactly why **§9.6 matters**: the currently published Vesper is a `--dev --debug` build, so
it ships `▶ Renner drain` in the sidebar (plus the Canvas Review page and its `goto "Navigation"` full-map
button). Adding two more jumps is free *only* because the captivity release must be built **without
`--dev`**, which removes the widget entirely. Build clean, verify the sidebar has no `DEV JUMPS` block, then
publish.
