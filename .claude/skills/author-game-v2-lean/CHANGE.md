# Change an existing game

`R` below is `.claude/skills/author-game-v2/references/`. `CHECK` is
`python3 .claude/skills/author-game-v2-lean/scripts/edit_check.py`.

## Steps

**1 · Snapshot.** Run `CHECK <slug> --start`.
Done when it prints `START`.

**2 · Read what you will touch.** Open `games/<slug>/v2_state.json` and every canvas, NPC and
schedule row the change touches, in the phase file where each lives (grep the id across
`toml_phases/`). Read the footguns below that match the change, and the `R` section each one
points to.
Done when you can name every id you will add or edit and the file each lives in.

**3 · Make the change.** Edit the phase files. Keep the ledger in step: a person, a ladder step or
a home the gates read from `v2_state.json` is added there in the same edit (`R/state.md` lists
which fields).
Done when the change is written in full: prose, conditions, effects and ledger.

**4 · Check.** Run `CHECK <slug>`. It merges, re-runs the scoreboard and prints only what this
change made worse, plus a schedule check and an explicit-beat check.
Done when it prints `CLEAN`. On `RED`, fix each line at its cause and run it again. Never edit
`gates.py`, a baseline, or a threshold to get to `CLEAN`; if a red looks wrong, stop and tell LO.

**5 · Report.** Say in two lines what changed and where.

## Footguns

Each line is the correct move. The pointer holds the reasoning.

**People and schedules**
- A new person gets a home in `v2_state.json` `board.map.homes`: a room id, or `"offscreen"` if
  they sleep elsewhere. (`R/the-map.md` R2, `R/state.md`)
- A schedule row that crosses midnight on specific days is two rows: one to `00:00` on the start
  day, one from `00:00` on the next weekday. A row on all seven days may wrap in one.
  (`R/the-board.md` §2)
- Each hour of each day puts a person in one place. Trim or move an existing row before adding
  one that overlaps it. (The engine takes the first matching row: `v2.py:4149`.)
- A first meeting fires where the person is, at hours their schedule puts them there.
  (`R/the-first-hour.md` F5, F5b)
- A random ambient where a person speaks carries `requires_npc` (or an `npc_at_location`
  condition) for that person. (`R/engine.md` §31, §46)

**Ladders, meters and money**
- A ladder step's `gate` list in `v2_state.json` holds every trigger condition of its canvas
  except the counter, exactly. (`R/state.md`, `board.characters[].ladder`)
- A repeatable canvas that raises a gated meter is capped: the `<x>_today is_false` guard sits in
  the trigger (or on the same choice that sets the flag and pays), and the flag is cleared in
  `[engine.daily_tick]`. (`R/the-meters.md`, gate *the climb is paid for*; `R/engine.md` §28.1)
- Money in needs money out: a new canvas that pays her comes with a sink in the same change, or
  pays through a canvas that already counts as a source. (`R/the-economy.md`, gate 17)
- Rent is charged by the engine. A rent scene rewrites `[settings.rent]` text; no canvas takes the
  rent amount. (`R/engine.md` §26)

**TOML the engine reads**
- Lowering a number is `op = "add"` with a negative `value`. (`R/engine.md` §21b, §41a)
- Every `conditions` table carries `version = "1.0"`. (`R/engine.md` §2)
- Speech is `type = "dialog"` with `props = { speaker = "npc", npcId = "<id>" }`.
  (`R/engine.md` §25)
- Two independent conditional lines in one node are separated by an unconditioned block, or they
  merge into one if/elseif chain and one stops rendering. (`R/the-want.md` "the placement trap")
- A shown-locked choice on a number prints its own need; a story lock carries `locked_text`.
  (`R/engine.md` §15)

**Prose**
- Every line is true on every visit it can render on. A line about the past sits in a `group`
  gated on the flag that records it. (`R/register.md` "The truth rule")
- An explicit beat (a block that names the body) carries 3+ words from the frozen list and stays
  on the body to its last sentence. Lead-in and aftermath go in their own blocks.
  (`R/register.md` "The measured targets", test 7)
- Write in the loud register: say it, name it, short sentences. (`R/register.md` "The voice — say it loud")
