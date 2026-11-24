# craft/returning-player.md — the player who loads an old save

Read this before you write a card for release 2 or later, or before any rebuild once LO has played a dev build. Every release after the first lands on old saves. The damage can't be seen in a clean build, green checks or a fresh start; it exists only for the player who loads (C1651). Checked against Course of Temptation (CoT), the top games and the engine (LO, 2026-11-23: "Go ahead", after the study). The full engine walk-through is `.claude/skills/author-game-v2/references/the-returning-player.md`; this file is the short version and adds what the study found.

## Must read

The card's `Craft:` line cites each one, or says in one line why it skips it. `when` and `judge` are the labels in `SKILL.md`, "Rule labels".

| id | what it asks | the failure it stops | when | judge |
|---|---|---|---|---|
| C1651 | every later release lands on old saves, and the damage shows only for the player who loads | — | a release after the first | note |
| C1652 | once LO plays a dev build, the save rules apply to every rebuild after it | — · kept blocking: LO's rule (2026-11-23) | a release after the first | reader |
| C1653 | a load doesn't re-run `:: Start`, so a new default is missing from an old save | — | a release after the first | note |
| C1675 | the engine fills in what's missing, on every passage | — | a release after the first | note |
| C1654 | a save joins the new build through passage names, person keys, flag and meter keys, and what a number means | — | a release after the first | note |
| C1655 | safe to add: new flags, meters, people, systems, and new keys inside them | — | a release after the first | note |
| C1656 | never repaired: a renamed key, a removed key, a changed meaning, anything the save already used up | L101 | a release after the first | script + saves |
| C1657 | every TOML id is permanent; display names and prose change freely | L49 | a release after the first | note + saves |
| C1658 | never rename or repurpose a live flag or meter key; add a new one instead | P13 reader pass 11: start_fun kept its key and changed its meaning (the `saves` check went red on it too) | a release after the first | script + saves |
| C1659 | once a meter ships, freeze its range and bands; one gate's value can change | — | a release after the first | note + saves |
| C1660 | the game's title is fixed | — | a release after the first | note |
| C1661 | an item that gates progress is granted again where it's needed, never once only | L138 | a release after the first | reader |
| C1649 | a start choice added later doesn't take anything from an old save | — | a release after the first | note |
| C1662 | each save records the version it began in and the version it's on now | — | a release after the first | note |
| C1663 | a version mismatch on load is noted, never refused | — | a release after the first | note |
| C1667 | an unavoidable rename is a major version with an announced reset, never silent | — · kept blocking: LO's choice (2026-11-24) | a release after the first | reader |
| C1680 | a wait set before the minute stamp existed opens early, never strands | — | a release after the first | note |
| C1681 | each opt-in system says what an old save does with it | — · kept blocking: LO's choice (2026-11-24) | a release after the first | reader |
| C1664 | before re-shipping, compare with the last build actually shipped | — · kept blocking: LO's choice (2026-11-24) | a release after the first | reader |
| C1666 | the save check can't see a rescaled meter or a used-up grant; check those by hand | — · kept blocking: LO's choice (2026-11-24) | a release after the first | reader |
| C1647 | three places say what shipped (portal, the sidebar footer, the archived build), and they drift | — · kept blocking: LO's choice (2026-11-24) | a release after the first | reader |

## The engine (cited; `v2.py` is `apps/game_generation/twee_comprehensive/generators/v2.py`)

- **Fill in what's missing, never overwrite.** `setup.backfillStateDefaults` (v2.py:20505-20549) runs on every passage (v2.py:20656). It fills:
  - missing `$flags` keys;
  - `$player`'s top-level keys and `core_traits`;
  - `$game_state` one level into each sub-map;
  - a whole new person, or the missing `core_traits` and `flags` of an existing one.
  
  It can't follow a rename, notice a removal, or reread a number whose meaning changed (C1677).
- **A save is never refused.** `Config.saves.onLoad` notes the schema mismatch in the console and never throws (v2.py:4018-4038).
- **Version stamps.** `origin_version` is written once at the start (v2.py:1700-1702). `last_version` and `last_schema` are restamped when the build changes (v2.py:20661-20664).
- **The title.** SugarCube 2.30 files browser save slots under `Story.domId`, which comes from the title (`storage=SimpleStore.create(Story.domId, …)` in `~/bin/storyformats/sugarcube-2/format.js`). `Config.saves.id` is pinned to the game's slug (v2.py:3990), so an exported save still loads after a title change; a load throws on an id mismatch (`errorSaveIdMismatch`, same file). Browser slots don't survive a title change.
- **Granting again is safe.** `setup.addToWardrobe` returns early if she already owns the item (v2.py:1736-1745).
- **Old waits.** A flag with only `set_day` reads as set at the start of that day (v2.py:4983-4988).
- **The footer** shows the version and the release (v2.py:20823-20831).
- **The save check** is `check.py`'s `saves` (`scripts/scenes.py`), adapted from v2's `saves_mode` (`.claude/skills/author-game-v2/scripts/gates.py:10603`). It reads the merged TOML at the last commit of `output/index.html` (the build LO played), or `--against <git ref>`, and is red on a removed id or key, a meter whose range or bands changed, or a flag now set only by different choices (unless NOTES.md says `Same meaning: <flag>` with LO's yes). It can't tell a reworded button from a changed meaning, so it asks.

## The measures

CoT (`~/Documents/Process_Review_20260925/round1_evidence/scripts/_cot_js.txt` and `~/Documents/Great_Games_Study_20260926/round2/passages/course-of-temptation.txt`), read 2026-11-23:
- **Its own fill-in, by hand.** `setup.update_vars` has 64 numbered cases, one per change, run in order on any old save (`_cot_js.txt`, lines 139889-140850).
- **It repairs renames by hand,** which our engine can't. It deletes the old misspelt key "Risktakter" (`_cot_js.txt`, lines 139982-139986). It also branches on old saves when a meaning changed: `setup.is_prepoint8_save`, "0.8 came with significant changes to NPC personalities" (lines 136209-136220).
- **Every version a save has run.** `vars.versions` gets each new version pushed on (`_cot_js.txt`, lines 140833-140834).
- **Dead passages kept alive.** "Legacy Passage to prevent old saves not loading" (`course-of-temptation.txt`, line 2401).
- **A new start choice, asked of old saves.** Players: "you can set your birthday when you wake up if you load an old save" (`round2/comments_text/course-of-temptation.txt`, lines 2549-2550).

The field: player comments in `~/Documents/Great_Games_Study_20260926/round2/comments_text/` (13 games, 16,208 lines):
- **Lost saves are the commonest save complaint:** browser storage cleared ("Your browser cache is probably getting deleted", CoT, line 2211). New Life Project (NLP) has four "I lost my save" posts (lines 600, 629, 1059, 1439). The fix players pass on is exporting ("import them into your downloads via the bottom of the save tab", CoT, line 3724).
- **Old saves breaking after an update:** "error within widget code" (NLP, line 1478); "it doesnt show the new things added like the gym job" (NLP, line 1500).
- **Resets are hated:** "can you make it so saves save over updates it's so annoying having to remake one and play from the beginning every time" (NLP, line 1645).
- **"Forgot what's next" after a long break** is thin: one clear post, "forgot how to reach the mansion". The quest card's next-step line covers it (`craft/arc.md` rule 5).

## The shape

Each rule says what CoT and the field do, then whether it's **measured** or **LO's choice**.

1. **The save rules start when LO first plays a dev build,** not at release 2 (C1652). *LO's rule.*
2. **Add freely; the engine fills it in** (C1653, C1675, C1655). New flags, meters, people, places and systems reach an old save on its next passage. *CoT and the engine agree:* CoT's 64 cases do it by hand; the field's broken saves ("error within widget code") are what happens without it. *Measured.*
3. **Never rename, remove or repurpose an id or a key** (C1656, C1657, C1658). Prose and display names change freely. To retire something, leave it and add a new one. *CoT and the engine split:* CoT renames by hand in its update cases; our engine only fills in what's missing, so a rename strands the save. For us the rule holds. *Measured* (engine; L101).
4. **Freeze a shipped meter's range and bands** (C1659). One gate's value can change, because it's read live. *CoT agrees:* when it changed what its people were like, it had to branch on old saves by hand. *Measured.*
5. **Keep the title** (C1660). *Measured* in SugarCube's own code: browser slots are filed by title.
6. **Grant a gate item again where it's needed,** not once at a moment the save may have passed (C1661). *Measured* (engine; L138).
7. **A start choice added later is asked once of an old save,** and takes nothing it already had (C1649). *CoT agrees:* the birthday asked on waking in an old save. *Measured.*
8. **Never refuse an old save; note the version** (C1662, C1663). *CoT, the field and the engine agree:* CoT keeps every version a save has run, the engine only logs a mismatch, and players hate a forced restart. *Measured.*
9. **A reset is the last resort:** a major version, said in the release notes, never silent (C1667). *The field:* players hate resets, and CoT never resets, it migrates. *LO's choice.*
10. **Each card's `Earlier releases:` line says what an old save sees** (the card template; C1681). It names what's new, and confirms that nothing shipped was renamed. *LO's choice.*
11. **Before re-shipping, compare with the last shipped build** (C1664, C1666, C1647). `check.py`'s `saves` does the key compare; check a rescaled meter and a used-up grant by hand. *LO's choice.*
12. **Tell the player how to keep a save:** one line on the tips page that saves live in the browser, and how to save to disk. *The field:* lost browser saves are the commonest save complaint. *LO's choice* (a new rule from the study).

## Worked example

Roles: the café manager, and release 2. These are the card lines that matter for an old save. The ids are examples.

```text
Earlier releases: an old save gets the manager's step 2 on its next passage (new flag
  cafe_step2_done, filled in false). cafe_hired is kept as it is (not renamed to job_cafe).
  The new start choice "Where you grew up" is asked once, on waking, when it's missing;
  it changes no flag the save already has. Nothing shipped is renamed or removed.
```

And the tips page, once:
> Your saves live in this browser. To keep one safe, open Saves and choose "Save to Disk…".

## Not this

- Renaming `cafe_hired` to `job_cafe` "to be tidy". Every save that hired her loses the job (C1658; L101).
- A key item granted only in a scene the save already passed (C1661; L138).
- "This update needs a new game." Fill in, don't reset (C1663, C1667).
- Changing the title for release 2. Every browser save slot is lost (C1660).
- A meter rescaled from 0–100 to 0–10 between releases (C1659).
