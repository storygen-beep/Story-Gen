# NPC hidden scores — the floor LO wants, and why they start at 50 for now

**Written 2026-09-25**, when the new opening was built.

## What LO asked for

The per-person scores (Gil, Nate, Owen) should **start at zero**, be able to **go down**, and stop
at a **lower cap** — a floor below zero, the way the top of a bar stops at a ceiling.

## Why that cannot be built today

- Every trait effect is clamped to **0–100** unless it says otherwise. The clamp defaults to on and
  the range is hard-coded (`apps/game_generation/twee_comprehensive/generators/v2.py:5928-5930`,
  `.claude/skills/author-game-v2/references/engine.md` §21).
- `clamp = false` on an effect removes the clamp entirely. The score can then go below zero, but it
  has **no floor at all** — it can fall forever.
- `cap` on an effect is a ceiling only (`the-meters.md` M6).

So "start at 0, go down, stop at a floor" has no engine shape. A `−1` on a score sitting at 0 is
clamped straight back to 0 and does nothing.

## What the game does instead (LO's fallback)

`npc_gil.relation` and `npc_nate.relation` start at **50** (`toml_phases/1_metadata_and_locations.toml`).
A minus choice in the opening now really lowers them, and the default 0–100 clamp keeps them in range.
`npc_gil.doubt` (the plan's "Suspicion") starts at 0 and only rises, so it needs nothing.

The choices that move these scores are in `toml_phases/2_one_shots.toml`, `opening_house`:
Gil ±1 relation, Gil +1 doubt, Nate +1 arousal ("tension"), Nate −1 relation, and Owen +1 relation
in `canvas_ask_owen`. No score is ever printed; the player sees the reaction line.

## How the real version should work — an engine change

One of these, in `generators/v2.py` (v2 only; v1 is frozen):

1. **A per-trait range.** Let an NPC (or player) trait declare its own bounds, e.g.
   `core_traits = { relation = 0 }` plus `trait_ranges = { relation = { min = -100, max = 100 } }`,
   and have `applyAndNotifyTrait` clamp to that range instead of the fixed 0–100 when one is declared.
2. **A floor on the effect.** Add `floor` beside the existing `cap` on an effect, passed through to
   the same function, so `{ …, op = "add", value = -1, clamp = false, floor = -100 }` stops at −100.

Option 1 is the better one: the range belongs to the score, not to each of the dozens of effects
that write it, and one declaration cannot be forgotten on the next effect someone adds.

Either change also needs the importer (`apps/projects/services/template_import.py`) to accept the
new key, because an unknown key is dropped silently.

## What to change back once it exists

- `npc_gil.relation` and `npc_nate.relation`: 50 → 0, with the declared range.
- Any reader written against the 50 baseline (none yet — nothing reads these scores so far; the
  `cast's meters` lint lists them as gating nothing).
