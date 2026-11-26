---
name: author-game-lean
description: EXPLICIT-INVOKE ONLY — run when LO asks for "/author-game-lean", "lean on <slug>", or "start a lean game". Builds an adult sandbox game one approved piece at a time — a skeleton release first, then pieces on top — each shown to LO as a card, built only after his yes, and checked by scripts/check.py. Do NOT use for a plain "start a new game" request; that belongs to the incumbent skill until LO promotes this one.
---

# author-game-lean

The front door. It always loads. It holds the loop, the rules, and where everything lives. Each step has its own phase file — read it at that step, not before.

## Start of every session

1. Read `games/<slug>/STATE.md` (the hook shows it). No STATE.md means a new game: copy `templates/STATE.md` and `templates/NOTES.md` there; the next step is `plan`.
2. Its last line is `Next step: <phase> — <what>`. Open that phase's file and do the `<what>`:

| phase | file |
|---|---|
| plan | `plan.md` |
| piece | `piece.md` |
| build | `build.md` |
| release | `release.md` |

## The loop

1. **Plan** (`plan.md`). List the release's pieces in STATE.md, with an out-of-scope line. Release 1 is the skeleton: every person, place, system and the daily loop, all shallow.
2. **Card** (`piece.md`). Write the screens and the `Does:` block, print the piece's rule list (`check.py --rules`), then write the card from `templates/piece-card.md` to those rules. Run the checks that can judge the card.
3. **Show** (`piece.md`). Show the card. Build nothing in the same reply.
4. **Yes** (`piece.md`). Record LO's words with `scripts/approve.py`. "Change" means a new card and a new ask. Silence or "sounds good" is not a yes.
5. **Build** (`build.md`) only that piece: `venv/bin/python .claude/skills/author-game-lean/scripts/build.py games/<slug>`. It refuses a piece with no approval, or whose card changed after the yes. Small calls go in NOTES.md as `Ruling: what · why · cost if wrong`.
6. **Check** (`build.md`). `scripts/check.py` runs by itself after the build: the scripts, the sheet and the `Does:` guard, all blocking. Fix red in the card. INCOMPLETE names what wasn't checked.
7. **Read** (`reader.md`). Every scene piece, after check is green and before LO plays: a fresh agent judges the work list from `scripts/reading.py` (the rule list and the scene tests, only what changed after the first pass), and its `--record` keeps the verdicts. Reader rows, scene tests and the truth rule block; notes are shown on their own. LO sees the table by cause; each blocking cause goes back into the card. No pass limit: done when the work list is empty.
8. **Close the piece** (`build.md`), same turn: update STATE.md, then list this piece's rulings to LO.
9. **Play.** Every few pieces LO plays: "this should happen. Does it?"
10. **Release** (`release.md`), once every piece is checked: `venv/bin/python .claude/skills/author-game-lean/scripts/build.py games/<slug> --release`, then `venv/bin/python .claude/skills/author-game-lean/scripts/check.py games/<slug> --release`, then the reader again on any piece whose card changed since its last reading, then LO plays the whole release, then the media search, only after LO says "release ready", then ship.

## Always

1. **Never build an unknown topic on a guess.** If no file here, no card and no answer from LO covers it, write it down with its source or a placeholder, and ask. (C2024)
2. **Checks run by themselves** — through build.py and the hook, never from memory. (C2083)
3. **Engine facts carry `file:line`.** Read `apps/game_generation/twee_comprehensive/generators/v2.py` and cite it. (C2167)
4. **Examples use placeholders** (`<slug>`, `<person>`, `<place>`), never a real game's names: an example outranks the rules beside it. (C2168)
5. **Nothing is built without LO's yes on its card,** recorded in `approvals.json`.
6. **Never run a media search unasked.** Don't list missing media until LO says "release ready".
7. **LO decides commits.** A session commits only on his word, relayed or direct, and never pushes or merges unless he says so.
8. **A design idea the craft files leave vague is LO's question, never a default.** When a card needs a grind, a pace, a reward size or a stance, and no craft row, PLAN.md or NOTES.md line pins it down, ask LO before writing the card: simple words and one concrete example ("How long should the café job take before the raise: three shifts, or ten?"). His answer goes in the game's NOTES.md with his words, and into the skill when it is general (`piece.md` step 2). (C2185)

## Build commands (engine)

Every command runs from the repo root with `venv/bin/python` (3.12). Plain `python3` here is 3.10, and the scripts need `tomllib` (3.11+). In the tables, skill files are named relative to `.claude/skills/author-game-lean/`.

Dev build, while authoring (keeps `6_dev_shortcuts.toml`; always `--dev` and `--debug` together, so a missing picture shows as a grey box; goes to `output/`, the folder LO plays from on his phone through the portal, which is his own play channel, not a public release; LO, 2026-11-23):

    venv/bin/python scripts/merge_toml_phases.py games/<slug>
    venv/bin/python manage.py package_from_toml --file games/<slug>/toml_phases/7_final_game.toml \
        --output games/<slug>/output --gen-version v2 --dev --debug

Release build (drops it):

    venv/bin/python scripts/merge_toml_phases.py games/<slug> --no-dev
    venv/bin/python manage.py package_from_toml --file games/<slug>/toml_phases/7_final_game.toml \
        --output games/<slug>/output --gen-version v2

The dev file is dropped only on `--no-dev` (`scripts/merge_toml_phases.py:80`). Without it, dev canvas names ship in the game (`scripts/merge_toml_phases.py:68-74`). Package flags: `apps/game_generation/management/commands/package_from_toml.py:54,67,81,151`. `venv/bin/python .claude/skills/author-game-lean/scripts/build.py games/<slug>` runs the dev form, and `--release` runs the release form. Never hand-edit `7_final_game.toml`.

## Where things live

| what | file |
|---|---|
| phase steps | `plan.md`, `piece.md`, `build.md`, `release.md` |
| the reader | `reader.md` |
| craft by area | see the area table below |
| state and plan templates | `templates/STATE.md`, `templates/PLAN.md` |
| piece card | `templates/piece-card.md` |
| check | `scripts/check.py`, `scripts/scenes.py`, `scripts/sheet.py`, `scripts/rules.py`, `scripts/reach.py`, `scripts/who_is_where.py` |
| the reader's memory | `scripts/reading.py` |
| build, approve | `scripts/build.py`, `scripts/approve.py` |
| craft still to port | `lists/COVERAGE.md` — every item ends ported, or dropped by LO |
| checks still to port | `lists/CHECKS.md` — same |
| lessons that correct a craft item as it's ported | `lists/LESSONS.md` |
| ideas, proposed rules | `LATER.md` |
| edit log | `CHANGELOG.md` |
| per game | `games/<slug>/STATE.md`, `NOTES.md`, `approvals.json`, `cards/<id>.md` |
| notes template | `templates/NOTES.md` |

**Areas.** Each area's rules live in its craft file below. A new card names no areas: its `Does:` block does that work ("Rule labels"). Cards from before 2026-11-24 still carry an `Areas:` line, which `scripts/check.py --card` checks against the same list (`AREAS`, `TOPICS`). An area with no file gets its craft file before its first piece (`piece.md` step 1).

| area or topic | craft file |
|---|---|
| first hour | `craft/opening.md` |
| media | `craft/media.md` |
| meters (topic) | `craft/meters.md` |
| walk-ins (topic) | `craft/walk-ins.md` |
| body moments (topic) | `craft/body-moments.md` |
| voice | `craft/voice.md` |
| places | `craft/places.md` |
| clock | `craft/clock.md` |
| people | `craft/people.md` |
| economy | `craft/economy.md` |
| want | `craft/want.md` |
| heat | `craft/heat.md` |
| clothes | `craft/clothes.md` |
| systems | `craft/systems.md` |
| arc | `craft/arc.md` |
| returning player | `craft/returning-player.md` |
| phone | none yet: `craft/<area>.md`, with spaces as hyphens |

Never read a list in `lists/` whole. Grep the area you're porting.

## Rule labels

A craft file's must-read table has two more columns, `when` and `judge`, beside the failure column (the rule pipeline, LO 2026-11-24). Every craft file is labelled (2026-11-24); `scripts/tests/test_skill.py` (`LABELLED`) checks every file in `craft/`, so a new one is labelled from the start.

**`when`**, one or more of these, comma-separated. Each names something a screen does:

| when | the screen… |
|---|---|
| always | any screen with text on it |
| a person is on screen | has someone besides her: a line from them, a presence check, their name |
| a first meeting | is the first time she meets someone |
| the first screen | is the game's first screen of story |
| the start choice | asks the start choice (who she was before) |
| the hand-over | is the opening's last screens, where play is handed to the player |
| a person's arc step | is part of a one-time scene that moves someone's arc a step |
| a no is possible | offers her a choice she can say no to |
| a one-time step | is part of a one-time scene |
| a repeatable | is part of a scene that plays again |
| a scene's last screen | is the last screen before the scene leaves |
| a place is entered | is the screen of a place, or the arrival at one |
| a price or pay is shown | shows money: a price, a cost, pay, the rent |
| the clock moves | spends time, or says a time |
| she dresses or undresses | moves a garment |
| a garment is named | names something she wears |
| a moment alone with her body | is a shower, dressing, the towel, bed or the mirror |
| something sexual shows | shows arousal, a look, a touch, or sex |
| an explicit beat | has a beat marked `[explicit]` |
| a meter is shown or paid | shows a meter, or moves one |
| a goal card is shown | shows a quest card or a goal line |
| a media spot | has a picture or a clip |
| a walk-in | is someone walking in on her, her walking in, or someone coming to her on arrival |
| she comes across something | is a walk-in she comes across, firing on arrival (kind a, `craft/walk-ins.md`), not someone coming to her |
| she gets noticed | is a stranger reacting to what she wears, firing on arrival (kind c, `craft/walk-ins.md`) |
| the opening | is in the opening |
| a release after the first | ships in release 2 or later, onto old saves |
| the plan | not a screen: the game plan or a release's piece list, where a whole system is designed |
| a rule is changed | not a screen: a skill edit that adds or removes a rule |

**`judge`**: `script + <check>, …` (a check in `scripts/check.py`'s `CHECKS` decides it), `reader` (the reader decides it; `reader + <check>, …` when a check helps), or `note` (the reader reports it in its own section; it never holds a piece). A `script` or `reader` row has a real failure in its failure column, or says why it stays blocking ("— · kept blocking: the voice, LO's").

## Changing this skill

- A new rule needs a real failure, and an answer to "why doesn't an existing rule cover this?". Until then it goes in `LATER.md`.
- **A study gives the lesson; the rule is our design** (C2184). From a study of another game, take what the player gets and why it works, then write our own design for our games, saying which lesson it comes from. A rule never has "because CoT does it" (or any game) as its only reason, and never copies another game's strings, numbers, tables or layout by default; a copy is LO's call, asked for by name. A row may cite a game's numbers as a measure, as evidence. (LO, typed in main-lean 2026-11-25: "we dont want to copy everything exactly. Instead learn the design so we can design for our games. Applies to everything.") The rules written on 2026-11-25 from CoT stay until LO reviews them, one at a time.
- Every edit gets a dated `CHANGELOG.md` line: what changed, why, how it was verified.
- Size caps, enforced by tests on instruction files (everything outside `lists/`, except `CHANGELOG.md`, which is a diary, C2170): this file under 200 lines, every other file under 400.
