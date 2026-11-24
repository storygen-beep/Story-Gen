# CHANGELOG — author-game-lean

## 2026-11-19

- Created `SKILL.md`, the front door (73 lines): the session start that routes on STATE.md's `Next step:`, the loop with its release step, the seven Always rules (C2024, C2083, C2167, C2168, the card yes, no unasked media search, LO commits), the build commands, and where things live. Why: Phase 2 of `~/Documents/Skill_Research_20261119/PLAN.md`, structure A, approved by LO in chat. Verified: `wc -l`; the flags are at `package_from_toml.py:54,67,81` and the v2.py path was checked with `find`.
- Created the phase stubs `plan.md`, `piece.md`, `build.md` and `release.md` (11–17 lines each). Each says what the step is, what it reads, what it writes and when it's done. Why: LO asked for structure A, with the stubs filled in during Phase 3. Verified: `wc -l`.
- Created `lists/COVERAGE.md`, copied from `harvest/1_craft.md` without its old totals table (port 1,596 / merge 440 / drop 137), keeping only the Phase 1 result line. Created `lists/CHECKS.md`, a straight copy of `harvest/2_checks.md`. Why: they are the coverage lists Phase 3 ports from and ticks off; `lists/` is outside the size cap by rule. Verified: COVERAGE.md has all 2,173 C-rows, same as the source; `grep Totals` finds nothing.
- Created `templates/STATE.md` (30 lines). It has the built, current release (piece rows dated approved / built / checked / played), open, shipped, and a closing `Next step:` line. The header carries C2040 (update in the same turn as the build), C2041 (store only what can't be worked out from the game), and LO's collapse rule: a shipped release's rows become its one-line record. Why: Phase 2 item 2, approved by LO with the collapse rule added. Verified: `wc -l`.
- `plan.md`: a new game now starts with the one-page game plan (her, the want, the people, the places, rough arcs, roughly what each release adds). It is shown in bites and recorded in NOTES.md before any release piece list. Why: LO's fix, 2026-11-19. Verified: re-read.
- Created `templates/piece-card.md` (14 lines). Its slots are when/where, what the player sees, variants, changes, media, earlier releases, out of scope, `Builds:` (canvas ids) and `Card checks:`. Why: Phase 2 item 3, approved by LO. He added that `Builds:` feeds a Phase 2 check: every canvas must be listed by an approved card. Verified: `wc -l`.
- `piece.md` went from stub to recipe: write, check the card (C2058, C2063, C2069), show the file's exact text, take the answer, never build in the showing reply. After "yes, but change X", only the changed lines are shown, as before and after (LO, 2026-11-19). Verified: re-read.
- `SKILL.md` build commands now show the dev form and the release form (`--no-dev`). Every script takes the game folder (`games/<slug>`), not the slug. `release.md` step 1 builds with `--release` and checks that no dev canvas is in the release output. `build.md` uses the folder path. Why: LO's correction, 2026-11-19. The dev file drops only on `--no-dev` (`scripts/merge_toml_phases.py:80`), and without it dev canvas names ship (`:68-74`, Vesper 0.2.0). Verified: `grep -n no_dev scripts/merge_toml_phases.py`.
- Created `scripts/approve.py`, which records a yes against a sha256 of the card's raw bytes. The file is append-only and the newest record counts. It refuses empty words and a missing card. `status()` returns approved, changed or missing; build.py and check.py use it. The limit is stated in the docstring and as approvals.json's first field. Created `scripts/tests/test_approve.py` with 9 tests. Why: Phase 2 item 4, approved by LO. Verified: 9 passed (`pytest -p no:django`). In a mutation copy where `status()` ignores the hash, both planted-bug tests fail (edited card, one-byte edit).
- Created `templates/NOTES.md` with decisions in LO's words and rulings as `Ruling: what · why · cost if wrong`, listed at each piece's end (C2066). Created `LATER.md` with the admission rule, a proposed-rules slot, and the 11 craft ideas; C2022 now includes its merge C2093, "a new check warns before it blocks". I1–I36 are pointed to, not copied. Copied `harvest/3_lessons.md` to `lists/LESSONS.md` (165 L-rows, 36 I-rows). `SKILL.md` lists LESSONS.md and the notes template, and a new game copies both templates. Why: Phase 2 item 5–6, approved by LO with those two fixes. Verified: `grep -c` on L- and I-rows.
- Copied `scripts/reach.py` byte for byte from author-game-v2 (frozen at ea8f6465); `diff -q` finds no difference. Copied its tests as `scripts/tests/test_reach.py` and `test_reach_dress_rules.py`. The two tests that went through `gates.py` now call reach directly (`reach.rows`, `reach.dress_rule_holes`), and the gate-only "not applicable" test is dropped. Verified: 10 passed.
- Created `scripts/check.py` with the merge, reach, approvals, builds and release checks. It prints a verdict (GREEN / RED n / INCOMPLETE: reason) and every red every run, marked NEW when new. Fixed checks and newly incomplete checks show once. The last run is stored in `games/<slug>/.check_last.json`. A changed card covers nothing in the builds check (LO). Created `scripts/build.py`, which merges, refuses (packaging nothing) on any unapproved canvas or built piece, packages, then runs check.py. Created `scripts/tests/test_check.py`: 18 tests, one clean game that must be GREEN plus every planted bug LO named. Why: Phase 2 item 7, approved by LO with three changes. Verified: 37 passed across all tests. In nine mutation copies (builds ignores approval, builds always green, release skips HTML, report hides old reds, merge ignores exit, approvals ignored, reach always green, build never refuses, incomplete counts as green), each breaks at least one planted-bug test.
- Ruling, found while building: the dev build goes to `games/<slug>/output_dev/` with `--dev` (`package_from_toml.py:151`), and only a release goes to `output/`. Why: `.gitignore:204-214` says `output/` is what the public portal serves, and dev builds stay in `output_dev/`. `SKILL.md`'s dev command and `build.py` were changed to match. Verified: `test_dev_build_never_writes_the_public_output_folder`.
- `.gitignore`: added `games/*/.check_last.json` (LO). Verified: `git check-ignore -v` matches at line 301.
- The size cap covers `.md` files only, outside `lists/` (LO chose option (a), 2026-11-19). Scripts aren't loaded as context, so `reach.py` stays a byte-for-byte copy at 601 lines. LO approved the `output_dev/` fix.
- Every runnable command in `SKILL.md`, `piece.md`, `build.md` and `release.md` now runs from the repo root with `venv/bin/python` and the full skill path. `SKILL.md` says why. `approve.py`'s usage takes `games/<slug>`. Why: LO, 2026-11-19. Plain `python3` here is `/Library/Frameworks/Python.framework/Versions/3.10/bin/python3` (3.10.11) and has no `tomllib`; `venv/bin/python` is 3.12.11. Verified: `python3 -c "import tomllib"` raises ModuleNotFoundError, and `grep python3` over the instruction files finds only the explanation line.
- Created `scripts/hook.py`. `session-start` prints each lean game's STATE.md (one ending in `Next step:`). `after-bash` runs check.py after a merge or package command on a lean game and exits 2 on red or incomplete; it skips build.py, which checks itself. Created `.claude/settings.json` (new; there was no project settings file) with the SessionStart hook and a PostToolUse hook on Bash, both on `"$CLAUDE_PROJECT_DIR"/venv/bin/python`. Created `scripts/tests/test_hook.py` (7 tests). It runs the exact command string from settings.json through `/bin/sh -c` with CLAUDE_PROJECT_DIR set to a throwaway root that links the real venv and skill. The tiny game moved into `scripts/tests/tiny_game.py`, shared by the check and hook tests. Why: Phase 2 item 8, JSON approved by LO with the venv fix. Verified: 44 passed. In a mutation copy where a red exits 0, the planted unapproved-canvas test fails.
- Created `scripts/tests/test_skill.py`. It checks sizes (SKILL.md under 200, every `.md` outside `lists/` under 400), that every SKILL.md pointer names a real file, `file:line` cites, C-ids, and no plain `python3` in a command. Each rule is a function run on the real skill (must pass) and on a temp copy with a planted bug (must fail). The cites test says plainly that it catches missing files and lines past the end, not drift inside a file (LO). Why: Phase 2 item 9, approved by LO. Verified: 56 passed across the suite. A probe confirmed the cites test reads the 4 real cites and the C-id test reads the 7 cited ids.
- `SKILL.md`: the bare cite `:68-74` is now `scripts/merge_toml_phases.py:68-74`, so the cites test can check it. Verified: the cites test is green.
- `scripts/reach.py` fix (LO, 2026-11-19). A live screen's `exit_block.config` effects (flagEffects, effects, wardrobeEffects) now count whatever the exit type, matching the engine (`v2.py:17940-17960` `_get_flag_effects_for_node`, `v2.py:18043` wardrobeEffects). v2's copy walked only `exit_block.choices`, so the exam fixture `billable_hours` showed 49 false reds from `opening_boot`, set on a location exit (`2_one_shots.toml:40`). The header says so. v2's frozen copy still has the bug; first_term's merged TOML has 0 screens with config effects, so its result stands. Added three tests to `scripts/tests/test_reach.py`: a flag only on a location exit's config counts, the same for a choices exit's config, and a flag nothing sets still shuts the scene. Verified: 59 passed. Against v2's unfixed `reach.py`, both planted tests fail. The fixture copy goes from 49 reach reds to 0.
- `templates/piece-card.md`: the Out of scope slot now says an adoption card (existing canvases, nothing new) always ends "LO has not read these scenes; this yes means 'keep as it is', not 'read and approved'." Why: LO's change to the dry-run card p0, 2026-11-19, so an adoption yes is never read as a review. Verified: grep.
- Dry run, Phase 2's "done when", on a throwaway copy of the exam fixture (`git archive 301f6f8 games/billable_hours/toml_phases`, in the scratchpad; nothing in `games/` changed). p0, an adoption card listing all 41 existing canvases: LO said yes, the hash was recorded, `build.py` built it into `output_dev/` and check.py was GREEN. p1, a one-screen fridge note on a new canvas `kitchen_note`: LO said yes, it was built and GREEN, and its text is in the built HTML. STATE.md was updated in the same turn each time (31 lines, ending on `Next step:`). With p1's card edited after the yes, `build.py` printed REFUSED and packaged nothing, and check.py was RED 2 (approvals changed, builds unapproved). With the card restored byte for byte, it was GREEN again. The real SessionStart hook on the real repo prints nothing, because no game in `games/` has a lean STATE.md. Verified: the outputs above; 59 tests passed.

## 2026-11-20

- Created `craft/opening.md` (about 105 lines). It has must-read rows C520, C519, C1611, C1613, C327, C311, C314, C601, C109, C166, L71, C1604, C1609, C1621 and C1631, each named against the P13 failure it stops. It has the seven-screen shape at 34–57 words a screen, a worked example as real short prose with roles (a rented room, landlord, wife, lodger; no first_term text), and one "not this" line per failure. Why: LO played first_term_lean's opening (`games/first_term_lean/cards/P13.md`) and found it weaker than the old game's. The card missed C520, C601, C327 and C109 because the harvest kept one-line rows and lost v2's worked examples. Approved by LO 2026-11-20 with his four changes (real prose for all seven screens, C311 and C314, C1621, the length rule). Verified: per-screen word counts by script (42, 57, 38, 54, 55, 40, 46); the ID test finds all 15 ids.
- `scripts/tests/test_skill.py`: the ID test (`unknown_ids`) now reads every `craft/*.md` file as well as the phase files, and checks L-ids against `lists/LESSONS.md`. The cites test reads craft files too. Planted bug added: `L9999` in a craft file goes red. Why: LO's yes to the L-id check, 2026-11-20. Verified: 60 passed.
- Created `craft/meters.md` (108 lines). Must-read rows: C285, C294, C295, C381, C188, C330, C1401, C210, C338, C1366, C388, C541, L68, L69, L70 and L116, each named against the P01 or first_term failure it stops. It has an engine section cited to `v2.py:7371` (an act's `cap` clamps; L69's old cite `v2.py:7246` has drifted), `:1282-1283` and `:7500-7516` (daily caps per band) and `:7541-7543` (first_gain_message), plus a ten-step shape. The worked example covers the meter Nerve, an act table with an accident that pays him, the daily caps TOML, a number lock, a Quests-page line, and three short prose screens (a walk-in button, a not-yet talk, a crossing). Why: P01 cited C294 but missed C295, C381, C188, C330, C1401 and C210 (`games/first_term_lean/NOTES.md` skill gap, 2026-11-20). Approved by LO 2026-11-20 with C541, C338, C1366 with L68, and C388 with L116 added. Verified: each cite read at its line; the ID test is green.
- `scripts/tests/test_skill.py`: a cite may name the engine as bare `v2.py`, which the cites test resolves to `apps/game_generation/twee_comprehensive/generators/v2.py` (the file SKILL.md rule 3 names; the only alias). Why: the cites test went red on meters.md's five bare `v2.py` cites, which is correct behaviour, and spelling the full path in every cite hurts reading. Verified: 60 passed; the probe shows all 5 cites read.
- Created `craft/media.md` (92 lines). It has 21 must-read rows (C1261, C1267, C1249, C1250, C1265, C1262, C1234, L121, L125, C1280, L119, C1281, C1284, L120, C1275, C1274, C1278, C1277, C1238, C1255, L97), each paired with the P02–P06 or first_term failure it stops. The engine section is cited: a place's picture is one `image` file with `image_search_queries` (`v2.py:484`, `:493`); `pool_dir` cycles files found on disk (`v2.py:16359-16364`); `pool` is a target that defaults to 4 (`apps/common/media_blocks.py:18-20`, `:33`). It has a seven-step shape and a worked example (a café place picture, the opening's temptation spot, a repeatable act with a clip per beat). Why: P02–P06 planned 24 "the room, empty" spots against first_term DECISIONS 246–258. LO's call (2026-11-20): a place gets at most one picture, one file, tier 0, with her in it (DECISIONS 258), and chores, doors, menus and solo everyday screens get none (C1265, DECISIONS 251–252). The first draft's "unless LO asks" came from the brief, not from LO, and was removed. Verified: every id grepped in the lists; the location image shape read at `v2.py:480-512`; 60 tests passed, including the DECISIONS line cites.
- `piece.md`: a new step 1 reads the craft file for each area the piece touches (`craft/opening.md`, `craft/meters.md`, `craft/media.md`); an area with no file yet is listed in LATER.md and grepped in COVERAGE. Step 2 asks for a `Craft:` line that cites every must-read id or skips one with a reason, and `Builds:` now lists places, people and sidebar items too. Step 3 checks this by hand until `check.py --card` exists (change 6); LO asked that change 6 replace the hand step with the command in the same turn and add a test for it. `templates/piece-card.md`: new `Craft:` slot under `Builds:`, and `Builds:` widened to match. `scripts/tests/test_skill.py`: `piece.md` must name `craft/`, and every `craft/*.md` it names must exist, with two planted bugs. Why: P13 cited 27 ids and missed C520, C601, C327 and C109; P01 missed C295; the card had no `Craft:` slot (NOTES skill gaps, 2026-11-20). Approved by LO 2026-11-20. Verified: 63 passed.
- `plan.md` rewritten from the 14-line stub into the full plan step (102 lines). Nine bites in order: her (narration person declared here, C548), the want, the people, the places (layout declared, L33 and L39), the people pass place by place (C804, C657, C589, C1531, L147), the systems bite (by area, with every goal-read meter given a piece; stricter than C738 on purpose because of L147), the schedules (a week table per person with hours she can reach them), the arcs (scaffold only: shape, direction, first third, ending, per L91), and the releases. Then the piece list, with the opening as one piece (`cards/P13.md`). Each bite has its must-read ids, and each rule cites its first_term_lean NOTES gap. Created `templates/PLAN.md`, the one-page plan, one slot or table per bite. `LATER.md`: added the idea "a person's first meeting may need to be one piece" (no failure yet). `SKILL.md` "Where things live" names `templates/PLAN.md`. Why: NOTES skill gaps from 2026-11-20 (plan stub, no plan template, people pass, schedule step, narration person, things to do alone) and LO's systems list 8–10. Approved by LO 2026-11-20 with his fixes (L91 for arcs, a cut applies only to the session's proposals, stricter than C738 because of L147, L33 and L39). Verified: 63 passed; the ID test reads every must-read id in plan.md.
- Created `scripts/who_is_where.py`, a self-contained copy of v2's `who_is_where.py` (frozen at ea8f6465). The only parts of v2's `gates.py` it needs (`_TR_*`, `_tr_min`, `_tr_in_window`, `_tr_days`, `_tr_rows_slots`, `_tr_met_only`, `_tr_where`, gates.py:13786-13870) are inlined, so nothing imports v2. It takes the game folder. Its engine cites were re-read: `setup.getNpcLocation` `v2.py:4398-4425`, `setup.isCurrentTimeSlot` `v2.py:4770-4790`, `setup._scheduleRowLive` `v2.py:4387` (v2's own cite, 4289-4318, has drifted). Created `scripts/tests/test_who_is_where.py` (7 tests). One planted-bug test checks that a later row must not win. One agreement test checks the copy builds the same table as v2's `_tr_where` on first_term, read-only. Why: LO, 2026-11-20: "don't call the frozen v2's copy". Verified: 7 passed. In a mutation copy without first-match-wins, all 6 rule tests fail.
- `SKILL.md`: the loop has a new step 7, **Read** (`reader.md`): every scene piece is read after the check is green and before LO plays. Later steps moved down one. The release step re-reads only pieces whose card changed. "Where things live" names `reader.md`, the craft files and `who_is_where.py`. `build.md`: the reader step is in "what it is" and "done when". `release.md` step 2 re-reads changed pieces only. `LATER.md`: two entries from LO, explicit beats need a measured check before the first sex piece (v2 used `gates.py --beat`), and `craft/voice.md` replaces reading v2's `register.md`. `scripts/tests/test_skill.py`: SKILL.md's loop, build.md and release.md must name `reader.md`, and the file must exist, with two planted bugs. Why: change 4, option A, LO 2026-11-20. Verified: 73 passed.
- Created `reader.md`, the lean reader brief, run as a fresh general-purpose agent. Test A judges every must-read row of every craft file the card names (or should have named), plus every numbered step of each file's "The shape". Test B runs v2-reader's 12 scene tests read against PLAN.md. It writes only to its scratchpad, and LO sees the table before playing. Proved on the weak P13 as its planted-bug test (LO, 2026-11-20). Run 1 caught failures 1, 2, 4, 5, 6 and 7 and passed failure 3: it noted a one-sentence build-up under C327 but passed it, because the build-up rule lives in the shape, not in a must-read row. Fix: test A now judges every shape step, and a step done thinly is a FAIL. Run 2 used a fresh agent that hadn't seen run 1 and caught all 7 (step 4: "Two sentences, no lock, no interruption"). Verified: both tables are in the scratchpad (`reader_first_term_lean_P13.md`, `_run2.md`).
- False-red test of the reader (asked by the ENI session, 2026-11-20). A fresh reader ran on the old first_term opening (`games/first_term/toml_phases/2_one_shots.toml`, canvas `ryan_01_hall_first_morning`, read-only), with `craft/opening.md` only plus B tests 3, 4, 7, 10 and 12. 9 FAILs. Real: C520 length, C519 jobs, C1611 (the hold only in a memory), C1621 with shape 7 (ends on an errand), B10 (Ryan's row has him in the bathroom when the scene puts him in the hall). Harsh: C109 on a first scene, C1604 read as people cards, and shape 5 read "way out" to forbid staying. Table: scratchpad `reader_first_term_opening.md`.
- **Approvals below were relayed by the ENI session as LO's own words, 2026-11-20 ("Yes to all three"; "One job, up to ~150"). They were not typed in this session.**
- `scripts/check.py`, change 6. (a) The builds check now also requires every place (`[[locations]] id`), person (`[[npcs]] id`) and sidebar item to be listed by an approved card. A sidebar item has no id, so it is listed as `sidebar:<trait>`, or `sidebar:<label>` without a trait. Reds read "place `x` is built but never approved". (b) New `check.py --card games/<slug> <id>`: red when a must-read id of a craft file named on the card's `Craft:` line is neither cited nor skipped as `skip <id>: <reason>`, when a skip has no reason, when a named craft file doesn't exist, when the card has no Craft: line, or when a card with media spots doesn't name `craft/media.md`. It saves nothing. `scripts/tests/tiny_game.py`: the clean card lists its place `home`. `scripts/tests/test_check.py`: 11 new tests (3 planted extras, 1 green; 5 planted card bugs, 1 green, 1 CLI with exit codes and no save). `piece.md` step 3 now runs `check.py --card` (in the same turn, as LO asked), and step 2 names the `sidebar:<trait>` key. `templates/piece-card.md`: `Builds:` names the sidebar key; `Card checks:` takes the pasted `--card` verdict. `scripts/tests/test_skill.py`: piece.md must run `check.py --card` and no longer check by hand, with a planted bug. Why: NOTES skill gaps "check.py's builds check guards canvases only" and "check.py has none" (no check reads a card), 2026-11-20. Verified: 86 passed. In 7 mutation copies (builds skips places, people or sidebar; card ignores missing ids, empty skip reasons, media, missing files), each breaks its planted test. On the real game, `--card P13` is RED 1 (2 media spots, no craft/media.md), and the widened builds check finds only P01's four sidebar items unlisted.
- `reader.md`: three readings fixed after the false-red test. Length fails only on more than one job or over about 150 words. C109 on a person's first scene accepts his want shown earlier in the same scene. C1604 judges objective cards, not people cards. `craft/opening.md`: C520's 34–57 is now a target ("stated", not measured). New must-read rows C1626 (first fiction screen median 144 words, measured, 25 games) and C1637 (meetings median about 101 words, 66% under 150, measured, 696 passages) set the ceiling. One job per screen stays hard (C519). Shape step 5: "Her thought reacts; a question is the default hook. No button is a final no; staying a beat is allowed." Why: the false-red test above, and LO's length call. Verified: ids grepped in COVERAGE; 86 passed; reader reruns below.
- Reader reruns after the fixes. Old first_term opening, run 2 (fresh agent): the C1604 and shape-5 over-readings are gone, and the length FAIL now fires only on the three two-job screens (all screens are under 150). C109 still over-read on a first scene, so `reader.md` C109 was tightened: on a person's first scene the leak half is N/A, only the promise is judged, and his look goes under C601. A C109-only fresh check then PASSES ("And Ryan's door, shut, next to yours."). P13 run 3 (fresh agent) still FAILs all 7 brief failures (C520/shape 2, C1611/shape 3, shape 4, C601, L71/B4, C166/B6, shape 7/B10). Tables: scratchpad `reader_first_term_opening_run2.md`, `reader_first_term_lean_P13_run3.md`.
- Standing authorization for this skill work, recorded as the ENI session relayed it (2026-11-20): "ENI for LO (standing authorization, 2026-11-20)". From here, ENI's yes counts as LO's yes for skill changes. Changes are still shown before writing. Anything very crucial (dropping craft, changing a rule LO made himself, anything irreversible, a commit or a push) is flagged for LO. Game-piece yeses in `approvals.json` stay LO's own words.

## 2026-11-21

- **Approval: ENI for LO (standing authorization, 2026-11-20).** LO's words, relayed by the ENI session and not typed here: "random scenes where she walks in, like in the old first term there was this park and library scenes... Here we dont have anything for it in the skill." Then: "yes, send both."
- Created `craft/walk-ins.md` (104 lines) for the two kinds of scene that wait at a place: one she walks into, and someone walking in on her in the middle of an act. Its must-read rows are C788, C802, C678, C854–C859, C212, C174, L97, L70, L147, L150 and L4. It also has the cited engine section (a location canvas with `max_triggers_per_day`, v2.py:15060; `trigger_mode = "random"` with `chance`, v2.py:15086-15089, rolled at v2.py:6404-6410; substitutions, v2.py:14662-14672, run by `setup.checkAndSubstituteCanvas`, v2.py:6915, one roll per rule with the first hit winning, v2.py:6987-6994), an 11-step shape, a worked example with roles (a neighbour, two strangers, a lodger; no first_term text) and "Not this" lines for L147, L150, L4, L97 and L70. Why: nothing in the skill asked what she walks into, and before this change no file outside `lists/` cited C788, C802, C854–C859, C678, C212 or C174 (checked with grep). Verified: the ID test covers the new file through `craft/*.md`; `check.must_read` reads all 16 ids; example word counts by script are 38, 51 and 42. The peer's count of "67 walkin_* canvases" in old first_term is wrong: there are 28 (`tomllib`). Its park and library examples are `park_watch_the_couple` and `library_back_stacks`, buttons with `max_triggers_per_day = 1`, not `walkin_*` substitutions.
- `plan.md`: added bite §8, "What she walks into, place by place", after the schedules (L97), with must-read ids C788, C802, C854, C678, C212, C174, L70, L97, L147, L150 and L4 and a Why: line quoting LO's gap. The arcs bite is now §9 and the releases bite §10. §10 now holds LO's rule: her own sex opens only with a partner (a boyfriend or husband) from the start of that relationship; seeing or hearing sex is a walk-in and in scope. The piece list makes walk-ins one piece per area, and Reads names `craft/walk-ins.md`. Why: the same relayed request (items 1 and 3), matching first_term_lean NOTES 2026-11-21. Verified: 120 lines; the ID test is green.
- `templates/PLAN.md`: a new §8 table (place, scene and choice, kind, who, everyday, window, how often, what it sets) with an area count line. Arcs and releases were renumbered to 9 and 10, and §10 gained the "her own sex" line. Verified: re-read.
- `piece.md`, `reader.md` and `SKILL.md`: each names `craft/walk-ins.md` for a walk-in card. Verified: the `piece_misses_craft` test is green.
- No check.py hook was added. Nothing in a card marks a walk-in, so `--card` can't tell when the file must be named, and inventing a marker is a design change for LO. The reader catches a walk-in card that leaves the craft file out (reader.md: "a craft file the card should have named and didn't is itself a FAIL"). Verified: 86 passed (`venv/bin/python -m pytest -p no:django -q .claude/skills/author-game-lean/scripts/tests`).
- **Approval: LO's own yes, relayed by the ENI session (ENI for LO, standing authorization, 2026-11-20).** The walk-ins follow-up. LO asked whether the skill would come up with walking into a housemate's room "while he is jerking off"; as written, only by luck. His correction: "in the starting ryan doesnt want her."
- `craft/walk-ins.md` (now 131 lines): added must-read C28 (taboo at home runs on walk-in risk). Shape step 12 is the person pass: for each person she lives with or sees often, what are they doing alone right now, at this point in their arc, with the where and when taken from their rows; in a taboo-at-home game each housemate has at least one walk-in at home. Shape step 13: a walk-in shows the person now, not their end want; a new version only after an arc step, each still what they were already doing (L97). Worked example D, in roles: a housemate alone in three versions (porn on his phone, nothing about her; her underwear after his first step; her name near the top), watch or back away, a flag only in release 1. Two new "Not this" lines. Why: §8 went place by place, so nobody asked what each person does alone; old first_term had such a scene as `ryan_door_ajar` (`games/first_term/toml_phases/7_final_game.toml:49479`). Verified: example word counts by script, 40, 36 and 33; `check.must_read` now reads 17 ids.
- `plan.md` (124 lines): §8 has the person pass, the taboo-at-home floor (C28) and the "person now" rule, adds C28 to its must-read line, and gives the gap in its Why: line. §3 asks for two lines per person, where they end up and where they are now, quoting LO. Verified: the ID test is green.
- `templates/PLAN.md`: the people table gains "where they end up (their want)" and "where they are now, at the start". §8 gains a "People alone" table (what they're doing now, where and when, the next version after which arc step). Verified: re-read.

## 2026-11-22

- **Approval: LO's own yes, relayed by the ENI session (ENI for LO, standing authorization, 2026-11-20).** LO: "in the opening it says she is taking shower, but here there can be a media too, where she is taking shower. This is hot. See if there are similar issues in the other scenes, where hot is compromised or skipped." Then: "yes, send the skill fix first".
- Created `craft/body-moments.md` (56 lines). A moment alone with her body (shower, dressing or undressing, the towel, bed, the mirror) is a body moment, not a chore. Must-read rows: C1262, C1275, C1274, C1280, C1277, C1279, C782, C1158 and C719. A 7-step shape: name the moment; stay on her body at her level (L71); no skip; one picture of her right after the body line (gif when something happens, `_t4` bare, `_t3` covered); pool 1 once-seen and 2 on a repeat; no meter moves while meters are still; the events (touching, walk-ins) stay scoped, never the moment's body. There's a worked example in roles (daily shower, towel and dressing, bed; 38, 44 and 29 words by script) and five "Not this" lines from first_term_lean. A new file, not a section, because the rule covers both prose and media, and the existing files each hold one of those. Why: first_term_lean's opening shower was "You give yourself five minutes." (`games/first_term_lean/toml_phases/5_scenes.toml:93`, :116, :139); "Back in your room, dressed" skipped the towel and the dressing (:199, :221, :242); the slipping knot (:164) got no picture; the daily shower (:547) was one line under a picture the P06 card described as "the shower running, steam on the glass"; and P06's out-of-scope line dropped "anything that happens during a shower or in bed". The root cause, verified: the heat rule (C311/C314, reader test 12) covers only charged scenes with a man reacting, and media.md step 3 gave "solo everyday screens" no picture. Ruling to confirm with LO: C1280 names no pool size for `_t4` on a repeat; the file uses 2, as for a look on a repeat.
- `craft/media.md` step 3: solo everyday screens exclude a moment alone with her body, which gets a picture of her, naming the P06 shower picture. Verified: re-read; 92 lines.
- `reader.md`: new test 13, where a moment alone with her body written as a chore (no body, or no picture) or skipped is a FAIL; Reads routes such a piece to `craft/body-moments.md`. Verified: re-read.
- `piece.md` and `templates/piece-card.md`: step 1 routes to `craft/body-moments.md`; an out-of-scope line scopes events, never the body of a moment the piece builds. Verified: `piece_misses_craft` is green.
- `SKILL.md`: the craft list names `craft/body-moments.md`. `craft/opening.md`: a "Not this" line for "You give yourself five minutes." Verified: the ID test is green.
- No check.py hook. A card has no marker for a body moment, so the reader's test 13 is the check. Verified: 86 passed (`venv/bin/python -m pytest -p no:django -q .claude/skills/author-game-lean/scripts/tests`); `check.must_read` reads the 9 ids.
- **Approval: LO's own words, relayed by the ENI session (2026-11-22):** "4. And for onetime scenes like opening it should have only one."
- `craft/body-moments.md` step 5: a body moment on a repeat button gets pool 4 and one in a one-time scene gets pool 1, quoting LO. The "LO's call to confirm" note is gone, and the worked example's daily shower now says pool 4. `craft/media.md`: the C1280 row and step 4 add the `_t4` body-moment-on-a-repeat case at 4. Why: this settles the open ruling from the body-moments entry above. Verified: grep finds no "pool 2" in body-moments.md and no "to confirm"; tests below.
- **Approval: LO's own yes, relayed by the ENI session (ENI for LO, standing authorization, 2026-11-20).** LO: "does walkins progresses?? like she can do more in those walkins as things rises?? In the release 1 it stays basic obv. But how does top games do it??" Then: "yes, send it".
- `craft/walk-ins.md` (now 184 lines): new must-read rows C1820, C724, C1821, C1864, C792 and C302 (23 ids now), and a new section "How a walk-in grows". Its cited engine notes: conditions are checked before each rule's own dice (v2.py:6987-6994); an exclusive group shares one roll and a failed claimed slot falls to the plain act (v2.py:6909-6914, 6962-6981), so bands are independent rules; `substitution_only` (v2.py:15104-15107); the payoff needs a `trigger.location`, because `setup.getCanvasById` reads only location canvases (v2.py:4118-4131; v2 the-surfaces.md:282-285, whose own v2.py:4009-4023 cite has drifted). Seven steps:
  1. two sides grow: his version with his arc, her options with her meter along the H3 ladder;
  2. one canvas banded on her meter, with release 1 as the bottom band;
  3. the odds climb with the same meter, and a flat chance is listed;
  4. two screens at most;
  5. caught becomes a door, never a skip;
  6. release 1 is the bottom band, a flag and no meter (L70);
  7. at least three of her states open scenes (C857).

  Worked example E, in roles: an overheard housemate in three bands (hear, listen, look) with chances 0.10, 0.35 and 0.70, a line each, and the TOML for the bottom rule. Three new "Not this" lines. Why: the file taught only his side growing; C1820, C724, C302, C792 and C1821 were marked port in COVERAGE but cited in no craft file (grep). Verified: sources read at v2 the-surfaces.md:250-290 and 330-345 and the-heat-ladder.md:90-100; the engine lines re-read today; the trait condition shape was checked against `games/first_term/toml_phases/7_final_game.toml:1068-1072`.
- `plan.md` §8: each walk-in names its next band and what opens it, pointing at the new section. `templates/PLAN.md` §8: new column "next band, after which meter or arc step". Verified: re-read.
- The cites test caught two short `author-game-v2/...` paths in the new section; they now use the full `.claude/skills/...` path. Verified: 86 passed.
- **Approval: LO's own yes, relayed by the ENI session (ENI for LO, standing authorization, 2026-11-22):** "yes, send item 1 and the pointer fix".
- `piece.md` step 1: no piece in an area with no craft file. Before the first piece in such an area, write `craft/<area>.md` from the area's COVERAGE section, its LESSONS rows and the CHECKS `later` rows that touch it, in the existing craft shape. Show it to LO in bites and take his yes before carding the piece. The broken pointer ("an area with no craft file yet is listed in `LATER.md`") is gone. LATER.md lists no areas, and no card P01–P06 or P13 recorded the COVERAGE grep it asked for. The card's areas now come from SKILL.md's area table. Steps 2 and 3 name the new `Areas:` line and its red reasons. Why: P06 touched the clock and the shower with no craft file, and the shower became a chore. Port rows cited outside `lists/` and CHANGELOG, recounted here by script: economy 0/115, phone 0/62, returning player 0/34, clothes 1/70, clock 3/42; 1,596 port rows in all.
- `scripts/check.py`: new `AREAS` (the 14 craft sections of COVERAGE), `TOPICS` (meters, walk-ins, body moments) and `area_file()`. An area's file is `craft/<area with hyphens>.md`, except `first hour`, which maps to `craft/opening.md`. `check_card` is red when:
  - the card has no `Areas:` line, or names no area;
  - it names an area not on the list;
  - a named area has no craft file yet;
  - a named area's file isn't on the `Craft:` line.

  The mapping, and why: the opening is the first hour's file (8 of its C-ids are in "first hour"); `media.md` is media (16 of 16). `meters.md`, `walk-ins.md` and `body-moments.md` are topics, not areas: their ids spread across heat, arc, systems and places, and mapping heat to `meters.md` or places to `walk-ins.md` would let a heat or places piece pass with no file for most of that area. Heat, places and systems therefore have no file yet. Also fixed: `^Craft:\s*(.*)$` let `\s*` run past an empty line into the next one; both line patterns now use `[ \t]*`.
- `scripts/tests/test_check.py`: the card fixture's craft file is now `people.md` and the card carries `Areas: people`. New tests: an area with no file is red ("clothes"); an area whose file exists and is named is green; a file that exists but isn't named is red; no `Areas:` line is red; an empty one is red; an unknown area is red; the mapping (first hour to the opening, and the topic files exist). The empty-line test caught the regex bug above.
- `scripts/tests/test_skill.py`: `area_table_misses`, which checks that SKILL.md's area table names every area and topic check.py accepts and that every file it names exists, plus a planted test.
- `templates/piece-card.md`: a new `Areas:` slot. `reader.md`: an area the scene touches that the `Areas:` line doesn't name is a FAIL (the backstop). `SKILL.md`: the "craft by area" row points at a new area table showing which areas have a file and which don't yet.
- The existing cards are not re-carded by this; the game session does that in its re-check. `check.py --card games/first_term_lean P06` is now RED 2: no `Areas:` line, plus the media row it already had. Verified: 95 passed (`venv/bin/python -m pytest -p no:django -q .claude/skills/author-game-lean/scripts/tests`).
- **Approval: LO's own words, relayed by the ENI session (ENI for LO, standing authorization, 2026-11-22):** "Remove thoughts in itallic. Dont show in body too." · "Does Cot shows feelings??" · "Lets align it with Cot" · "yes, send it". This changes the voice LO chose on 2026-09-23/24 (v2 `register.md`) for this skill; it is his change.
- Created `craft/voice.md` (84 lines), the first area file under the area gate. Must-read rows: C442, C449, C451, C447, C593, C448, C450, C422, C460, C461 and L163. It has a measures section and eight rules, each marked measured (with numbers) or LO's choice:
  1. second person, about 10-word sentences;
  2. feelings on the body, hers and others', with a named feeling rare;
  3. arousal always on her body;
  4. no italic thoughts, which drops C444;
  5. people speak in most scenes and narration leads, under 5:1, which drops C446;
  6. say it plainly, name the tension, keep the detail;
  7. the truth rule;
  8. each person's own manner and term of address, obvious on arrival, a hook at the end, plain labels (the last three are LO's rules, not measured).

  The worked example is LO's approved bathroom and hall text, with names swapped for roles (71 and 103 words by script). Four "Not this" lines, including the italic thought at `games/first_term_lean/toml_phases/5_scenes.toml:165`. Why and verification: the peer's `voice.py`, re-run here on a 277-passage CoT sample, gives 68% with speech, 3.92:1, a 10-word median and "you" 70.4 per 1,000. DoL (286) gives 76%, 3.23:1, 8 words; Hellfire (296) gives 91%, 1.87:1, 14 words. Those two needed the passage-name filter removed, because their index tags don't match `event|hangout|dialog|class`. Italic thoughts in CoT: 27 of 4,066 `Event*.txt` passages have a `<i>` span of 4 or more words outside quote marks; the peer's broader count is 42. Every match of the peer's `//`, `''` and `@@` patterns there is 0; all italic markup is `<i>`, and much of it is emphasis ("<i>fuck</i>"). Exact-phrase counts: "You blush" 76, "you feel your face heat" 5, "Your cheeks burn" 3, "you feel your stomach drop" 2, "You feel embarrassed" 1, "looks away" 11, "seems nervous" 0, "a thrill of arousal" 7, "an ache between your" 3; macros `<<conj>>` 10,992, `<<ps>>` 5,411, `<<pp>>` 4,928. The quotes-only count is valid for CoT and DoL because both put speech in quote marks (v2 register.md:640-646, "unchanged"; L163).
- `lists/COVERAGE.md`: C444 (italic thoughts, `thought_bubble`) and C446 ("more dialogue than narration") are marked drop, each with LO's relayed words. This is a drop of craft, done on LO's own words.
- Italic thoughts were removed from the worked examples: `craft/opening.md` (five lines; step 5 now says she reacts on her body; a new "Not this" line; screen word counts re-run as 44, 57, 37, 54, 55, 40, 53), `craft/walk-ins.md` (five lines; counts 40, 53, 42, 41, 39, 36) and `craft/meters.md` (three lines; the Quests-page card text stays italic because it is card text, not a thought). Each became a body reaction. `craft/body-moments.md` had none. No file taught "more dialogue than narration".
- `reader.md`: the voice is now read from `craft/voice.md`. The truth rule stays read from v2's `register.md` "The truth rule", because voice.md carries only its headline rows (C460, C461), not its worked cases. Test 4 now reads her reaction on her body and in what she says, never an italic thought.
- `SKILL.md`: the area table gives voice its file. `LATER.md`: the craft/voice.md idea is marked done for the voice, with the truth rule still open.
- The cites test caught five short `register.md:` cites; they now use the full path. Verified: 95 passed; `check.must_read` reads the 11 ids.
- Not changed: `CLAUDE.md`, which is LO's file. Lines 115-120, 143 and 155-156 still teach v2's voice and "her thoughts sit beside the dialogue". Listed for LO through the ENI session.
- **Approval: LO's own yes, relayed by the ENI session (ENI for LO, standing authorization, 2026-11-22):** "Confirm each with the top games and CoT mostly", then "yes, send it".
- Created `craft/places.md`, the places area's file. Must-read rows: C769, C794, C795, C804, L106, C776, C777, C773, C758, C953, C954, C738, C762, L147, C808, C811, C770, C771 and C707. The measures table covers CoT's 126 `location`-tagged passages. The shape has nine rules, each marked measured or LO's choice:
  1. the identity line is the same every visit;
  2. one presence line per person, from their rows, plus the crowd;
  3. the menu holds needs, systems and people only;
  4. short labels with the cost shown, and never pay she earns;
  5. "not now" says why;
  6. every open place has one thing to do alone, stricter than C738 (LO's choice, L147);
  7. streets or quads are hubs;
  8. short screens;
  9. two DoL-only rules (C771, C707/C739), marked as not from CoT.

  The place picture points at `craft/media.md`, noting that CoT isn't its source. The worked example is LO's kitchen text in roles (mom, step-father). Four "Not this" lines. Pointers to `walk-ins.md` (C785's event pools) and the future clothes file (C1173's door check) instead of duplicating them. Verified by re-running the counts here:
  - 126 passages; median 64.5 words, p75 112; 285 labels, median 3 words;
  - cost shown 97, people offered 62, `$peopleatlocation` 19, `setup.Events.passage` 29, `clothes_ok` 22, pictures 0. The peer's counts were 24 and 30 for the two that differ; this file uses these.
  - The BangCoffee opening and "You really aren't that thirsty right now." were found in `BangCoffee.txt`.
  - One of the peer's claims was corrected before writing: CoT's streets name their buildings ("You are on Emerson Road. A large academic building is here…") rather than carrying many links.
- `craft/media.md` step 2: the one-picture-per-place rule now says it comes from the field (C1249, 41%), not from CoT, which has 0 pictures on its location screens.
- `SKILL.md`: the area table gives places its file. Verified: 95 passed, and the area-table test is green.
- `craft/places.md` rule 3, corrected (ENI session, 2026-11-22): BangCoffee does have a bathroom button. `BangCoffee.txt:36` calls `<<bathroom "A public restroom is available here.">>`, and the widget in `GlobalWidgets.txt:1468` renders `<<link "Use restroom" Restroom>>`. My grep looked for `<<bathroom>>` with no argument, missed it, and the entry above had wrongly said there was none; that line is fixed. The menu is coffee and Use restroom (needs), Study and Use laptop (systems), and `<<godate>>` (people). Verified: both lines read in the corpus; tests below.
- **Approval: LO's own yes, relayed by the ENI session (ENI for LO, standing authorization, 2026-11-22):** "yes, send it".
- Created `craft/clock.md`, the clock area's file. It has 23 must-read rows: C889, C906, C926, C900, C902, C903, C904, C892, C910, C929, C897, C924, C920, C913, C930, C914, C916, C915, C921, C927, C928, C931 and C890. Its engine section was re-cited against today's v2.py:
  - `advanceTime` takes minutes only (7004);
  - an exit with no time costs 3 (17924);
  - `isCurrentTimeSlot` wraps past midnight and defaults to an hour (4770-4790), and `time_of_day` uses it (5283-5285);
  - `deductLocationCosts` and `getLocationCostTag` (6226-6236);
  - `show_when_blocked` is read at 15098-15102 and drawn dimmed at 6734-6742;
  - `locClosedReason` gives "Closed. Opens at …" (11766-11773), and `closed_text` shows at the door (11438-11441);
  - the SchedulePage is at 24387;
  - there is no `@time` token (grep).

  C925, the peer's eighth engine fact (an exit runs advanceTime before flags), was left out because it wasn't re-verified today. The file has a CoT measures table, eight rules each marked measured or LO's choice, LO's café text in roles (the café owner), and four "Not this" lines. Verified by re-running over all 5,294 CoT passages (425,667 words stripped):
  - clock times 26, or 0.61 per 10,000 (the peer had 21, 0.49); weekdays 61, or 1.43 per 10,000 (the peer had 1.39);
  - 65 files with closed or opening text; `<<advtime>>` sizes 1 (180), 5 (114), 20 (76), 60 (74), 10 (72), 30 (38);
  - the four "A sign says it's open between …" lines, the bus at `RiversidePlaza.txt:110`, and "Nightlife Schedule" at `DisplayNPCWidgets.txt:816`.

  Fixed per-person schedules are marked as coming from IHOH (C892) and our engine, not CoT.
- `craft/places.md`: points at `craft/clock.md` for hours, closed lines and button times, with no duplication. `SKILL.md`: the area table gives clock its file.
- **Approval: LO's own yes, relayed by the ENI session (ENI for LO, standing authorization, 2026-11-22):** "yes, send it".
- Created `craft/people.md`, the people area's file. Must-read rows: C618, C619, C622, C627, C625, C626, C630, C632, C598, C620, C690, C613, C639, C640, C961, C954, C447, C593, C644, C596, C656, C660 and C448. It has a measures section and nine rules, each marked measured or LO's choice:
  1. nobody is met at the start except the people she lives with;
  2. a role until the meeting, then name and relation;
  3. unmet people are hidden;
  4. his wanting shows on his body first;
  5. three to five graded answers, with a no that lands and never pays;
  6. each person's own manner, subject and name for her;
  7. the talk screen's shape;
  8. one short, shown meter per person, still in release 1;
  9. obvious on arrival (LO's rule).

  It points at voice.md, places.md and clock.md instead of repeating them. The worked example is LO's café meeting, with the role "the café manager" and "I run the place" (ENI's correction, `games/first_term_lean/PLAN.md:55`), his name as a slot, and no pay amount (C954). Four "Not this" lines. Verified in CoT today:
  - the `anonorfullname` widget at `GlobalWidgets.txt` line 882, called 953 times (the `anonor…` family about 3,050);
  - `BusGrope.txt`'s five answers;
  - "That certainly backfired." in `EventResHallPropositionShowersBold.txt`.

  The field-measured rows are marked as from COVERAGE's evidence column, not re-run. The brief's "two versions of the café pay" line was dropped: ENI corrected it (NOTES.md:65 superseded :59).
- `SKILL.md`: the area table gives people its file.
- **Approval: LO's own yes, relayed by the ENI session (ENI for LO, standing authorization, 2026-11-22):** "yes, send it".
- Created `craft/economy.md`, the economy area's file. Must-read rows: C1003, C1004, C1033, C1008, C1014, C1013, C1016, C1020, C1021, C1022, C954, C1001, C1002, C989, C990, C951, C952, C992, C1017 and C967. It has a measures section, nine rules each marked measured or LO's choice, a "when paid sex opens" section marked not in release 1 (C966–C973), LO's Sunday rent text in roles (step-father, mom) with the figures marked as filler (C992), and four "Not this" lines. Verified by reading CoT's `WeeklyDebtPayment.txt`, `WeeklyDebtPaid.txt` and `WeeklyDebtUnpaid.txt` at the lines cited:
  - the bill starts at 100 and is capped at 200, with the author's note;
  - the phone hand-over lines and the first call with its GPA rule at 2.5;
  - the rises 100→150 at $500 paid and 150→200 at $1,000, the 250 and 300 rises switched off with `false and`, and the "same amount" line;
  - the lecture and `<<dalterneed Relaxation -50 true>>`.

  New today: every CoT amount is multiplied by `$optdebtpaymentmultiplier`, a difficulty option. The peer couldn't confirm the job button; I read one: QuickieBurger's "Work" button shows time and rest and no pay, and the wage is on the Work page (`Work.txt`, line 14). That's one job, said as such. The field rows come from COVERAGE's evidence column and were not re-run.
- `SKILL.md`: the area table gives economy its file.
- `scripts/tests/test_skill.py`: `test_planted_area_missing_from_the_table` now drops `economy` wherever it sits in the table (its own row, or inside the no-file row). Before, it removed "economy, " from the no-file row, which stopped working once economy got its own row. Verified: tests below.
- **Approval: LO's own yes, relayed by the ENI session (ENI for LO, standing authorization, 2026-11-22):** "yes, send it".
- Created `craft/want.md`, the want area's file. It has 23 must-read rows: C54, C43, C44, C46, C48, C51, C1619, C1628, C430, C598, C952, C992, C34, C35, C36, C37, C433, C32, C56, C72, C63, C64 and C65. It has a measures section, seven rules each marked measured or LO's choice, LO's goal card in roles (step-father, the café across from campus) with the amount marked as filler, and four "Not this" lines. The plan-level rows are pointed at `plan.md` §2. The peer said C6 and C24–C31 already live there; in fact §2 cites only C25, C26 and C28 (grep), and the file says so instead of claiming the rest are covered. Verified in CoT today:
  - the quoted lines in `Prologue.txt`, `Prologue14.txt` and `Prologue16.txt`;
  - "Think back..." leading to `PrologueHighSchool.txt`, which asks through `<<pickstartingtrait "popularity">>`. The peer had read only its first line; four such picks run across the prologue (popularity, relationship, relationship type, hobbies);
  - the "for now!" end line in `StoryHintWidgets.txt`;
  - the systems lecture in `PrologueFinal.txt`.

  The field rows come from COVERAGE's evidence column and were not re-run.
- `craft/opening.md`: the example's quest card went from "Make the rent by Friday." to "Pay your own way: rent every Friday." The old wording was a dated goal, which the new want.md's C34 and its "Not this" forbid. The hold's "Friday" in the dialogue stays, because a due day said by a person is the bill's date (C1004), not the goal's.
- `SKILL.md`: the area table gives want its file.

## 2026-11-23

- **Approval: LO's own yes, relayed by the ENI session (now named main-lean; ENI for LO, standing authorization, 2026-11-20):** "Yes".
- Created `craft/heat.md`, the heat area's file. Must-read rows: C255, C256, C252, C254, C239, C248, C249, C276, C291, C296, C284, C285, C286, C287, C288, C289, C297, C639, C640 and C311. It has a measures section, seven rules each marked measured or LO's choice, and pointers to opening.md (C311/C314), body-moments.md, walk-ins.md, voice.md and meters.md instead of repeating them. The worked example is LO's park text, scored per beat with v2's frozen `EXPLICIT` regex (`gates.py:311-315`): 1, 5, 1, 5 and 0 matches. Four "Not this" lines. An "Open" section proposes `check.py --beat` (not built): the walk-ins are the lean game's first explicit beats (P39, P40), so LATER.md's beat check is due before those cards. Verified in CoT today: 364 of 3,067 event passages (11.9%) have 3+ matches, by the peer's method; the peer had 353 of 3,108 (11%). The shower lines and the skillgate/"Resist the urge to look" pair were confirmed in `EventResHallExhibShowers.txt`. The field rows come from COVERAGE's evidence column and were not re-run.
- `SKILL.md`: the area table gives heat its file.
- **Approval: LO's own yes, typed in the game session and logged at `games/first_term_lean/NOTES.md:157-162`, relayed by main-lean (ENI for LO, standing authorization, 2026-11-20):** "Yes".
- `craft/walk-ins.md`: new section "When someone walks in on her". The other kind was thin next to "she walks in on": one engine line, shape step 6 and example C. The real failure: this game's plan has 3 of 24 walk-ins of this kind (PLAN.md:491, :506, :520), and nothing said that the act must be built first, that her body and picture apply, what her buttons are, or how two walk-ins on one act share the dice. Five rules:
  - the act's piece comes before the walk-in (the rule lives on the act's canvas, v2.py:14662-14678);
  - it's a body moment, with her picture right after he sees her (C1262, added to Must read);
  - he comes from his own row with his own reason;
  - two answers, cover or carry on, each with his reaction line and its own flag, the door into his arc (C302, C174);
  - two walk-ins on one act go in one `exclusive_group`.
  
  Example F is in roles (a housemate and the landlady on "Take a shower", 0.20 and 0.15 in one group, 40 words of story text by `wc -w`). The engine bullet now names `exclusive_group`. "How a walk-in grows" adds that a group's chances must sum to 1 or less: bands of 0.10, 0.35 and 0.70 in one group would cut the top band to 0.55. There are three new "Not this" lines. Verified by reading `checkAndSubstituteCanvas` (v2.py:6909-6999):
  - groups run before independent rules;
  - one roll per group, in cumulative slots;
  - a claimed slot whose conditions fail returns null at v2.py:6980-6981, so the plain act plays, and the independent rules on that act are skipped too (not in the relay; found reading the code);
  - the TOML key is read at v2.py:14678 and used in games/vesper (`floor_chat`).

  The relay's "6950-6975" is the same code; the cites use the exact lines. Tests: 95 passed.
- **Approval: LO's own yes, typed in the game session and logged at `games/first_term_lean/NOTES.md:163-167`, relayed by main-lean (ENI for LO, standing authorization, 2026-11-20):** "Yes".
- The failure this fixes: first_term_lean's `talk_mom` was a Talk button on the kitchen menu, and LO said "it should never be a separate button but instead inside her hub menu choice". The skill had taught it in two places: C1340 ("a talk button per housemate") and `craft/places.md` rule 3 ("its people button").
- `craft/people.md`: new rule 10. A person's actions sit in their own menu, behind their face on the room screen, never as room buttons. Talk is once a day, and the person never locks. C1340 is added to Must read. There is a new engine section, a worked example in roles (her mom's menu), and two "Not this" lines (a Talk button per person on the room menu; a person who locks after one talk). Verified:
  - `npc` on the trigger is read at `template_import.py:2581` and carried as `npcId` (v2.py:15080-15082).
  - A repeatable manual canvas with an `npcId` renders as the person's face, not a room button (v2.py:5925-5942, 5969, 6680, 6530-6531).
  - New, not in the relay: the face opens only that person's highest-priority canvas at the place (v2.py:5944-5948). So the menu must be one hub canvas, and the rule says so.
  - Once a day is a `_today` flag cleared by `[engine.daily_tick]` (v2.py:7156-7158; v2 `engine.md:1458-1485`).
  - CoT: the People Here button (`StoryCaption.txt`, lines 585-596), "Talk to her" (`DisplayNPCWidgets.txt`, lines 33-68), and `$interactionstoday` at `InPersonDialogueMenu.txt`, line 77. The relay said "about 30 options, each once a day". The file has 38 `<<link>>`s, and 14 are checked against `$interactionstoday` (grep), so the rule says that.
  - Field, two spot-checks of my own: the-hellfire-club's `DaisyRoom.txt`, line 18, "Speak to Daisy" opens her own menu, `Daisy_conv`, with a once-a-day flirt line. lust-for-life's `home-kitchen.txt`, line 15, has "Approach Cory" as a loose room button shown while she's there. The relay said all nine field games group a person's actions together. By its own tally, 4 of 9 put them loose on the room menu, so the rule marks faces, not buttons, as LO's choice, with CoT and 5 of 9.
- `craft/places.md`:
  - Rule 3 now reads: the menu holds needs and systems; a person is their face, and their actions sit in their menu (pointing to people.md rule 10).
  - The `<<godate>>` cite is corrected: it starts a date she planned earlier (`HangoutWidgets.txt`, lines 1-26), not a talk button. The measures row is relabelled "a planned date or an opportunity can start here" (`<<opportunities>>` assembles opportunity events, `GlobalWidgets.txt`, line 1809). The count of 62 of 126 is unchanged.
  - The kitchen example drops "Talk to Mom" from the buttons, and Mom's face opens her menu.
  - One "Not this" line is added.
- `lists/COVERAGE.md`: C1340 is reworded to a face at their spot opening their own menu, with Talk once a day inside it. The source (`author-game-v2/references/the-board.md:364-371`) is unchanged; the v2 skill is not edited.
- Tests: 95 passed.
- **Approval: LO's own word, relayed by main-lean (ENI for LO, standing authorization, 2026-11-20):** "Continue", his yes to the plan to build the beat check.
- `scripts/check.py`: new `--beat <card or file>`. It finds each beat marked `[explicit] … [/explicit]` (an unclosed tag runs to the next blank line; blockquote marks are stripped). It counts v2's frozen `EXPLICIT` words, imported from `author-game-v2/scripts/gates.py:311-315` at run time so the list can't drift. It is red when a beat has fewer than 3 (C254), or when its last sentence has none (the pivot, C249). A file with no marked beat is INCOMPLETE, never GREEN. Exit codes are 0, 1 and 2, as for `--card`. The 7.5% game-wide floor (C255) waits. Why: LATER.md held "explicit beats need a measured check before the first sex piece", and P39 and P40 carry the lean game's first explicit beats.
- `scripts/tests/test_check.py`: five new tests.
  - `craft/heat.md`'s Watch beat counts 5 and is GREEN.
  - A faded copy ("You watch until it's over.") is red on the floor.
  - The Watch beat with "You realise you'll never see the park the same way." added is red on the pivot only.
  - An unclosed beat over two blockquote lines stops at the blank line.
  - A file with nothing marked is INCOMPLETE.
  
  Verified by hand on a faded beat: RED 2, exit 1.
- `piece.md` step 3, `templates/piece-card.md`: a card with an explicit beat marks it and pastes the `--beat` verdict too.
- `craft/heat.md`: the "Open" section is now "The explicit-beat check", describing what was built. Rule 6 says to mark the beat and run it.
- `LATER.md`: the beat-check item is struck through as done. The game-wide floor stays open.
- Tests: 100 passed.
- **Approval: LO's own yes to the clothes example A–D, relayed by main-lean (ENI for LO, standing authorization, 2026-11-20):** "Yes". It came with one change to A, ENI's pick, which LO approved: her usual clothes go on by default, and the screen offers a short list of whole outfits instead of the full picker.
- Created `craft/clothes.md`, the clothes area's file. Why: P07 (clothes) goes before the opening's re-check, and the area had no file (piece.md step 1).
  - Must read, 23 rows: C719, C1158, C1206, C1166, C1167, C1204, C1183, C1171, C1169, C1150, C1201, C1173, C1184, C1198, C1185, C1220, C1221, C1177, C1176, C1189, C1197, C1200 and C1207.
  - An engine section, CoT measures, nine rules each marked measured or LO's choice, the approved example A–D in roles, and six "Not this" lines.
- Engine, verified by reading v2.py:
  - the seven slots (`template_import.py:278`);
  - `wardrobeEffects` actions (v2.py:18207-18224);
  - `equipItem` taking off top and bottom for a dress, and failing silently on an item's own conditions (v2.py:1751-1768);
  - dress codes and ClothingBlock's "Change clothes" and "Go back" (v2.py:2189-2200, 21039-21066);
  - the settings (v2.py:1196-1202);
  - the clothing conditions (v2.py:9505-9589).
- Found reading the engine, and changed in D: a room button gated on clothes is hidden, not dimmed. `show_when_blocked` dims only when the clock alone shut it (v2.py:6686-6691, `onlyTheClockShut` at v2.py:6058). LO's "dimmed run button" can't be a room button, so D puts the check on the "Run" choice inside the scene, shown locked with `show_when_locked` and `locked_text` (v2.py:17262-17266). This is flagged to ENI for LO.
- CoT, read today:
  - `Prologue6c.txt` and `PrologueWidgets.txt`, lines 6-18 (a short list of whole outfits, "Default" picked);
  - `Wardrobe.txt` ("change into your … outfit", `<<maybechangingwitnessedbyadmirer>>`);
  - "It would be daring to go out like this…" in 5 files (`MainHall.txt`, line 107);
  - `ExitShower.txt`;
  - `DressingRoom.txt`, line 5;
  - `clothes_ok` in 30 files.
  
  The field rows come from COVERAGE's evidence column and were not re-run.
- `SKILL.md`: the area table gives clothes its file.
- **Approval: LO's own yes to the engine fix, typed in the game session, relayed by main-lean:** "yes, do the engine fix". The engine change is main-lean's work (template_import.py, game_graph.py, v2.py, `apps/game_generation/tests/test_blocked_row_hours.py`). Only the skill files below are this entry's.
- `craft/clothes.md`:
  - D goes back to one click. The room button "Go for a run (45 min)" has `show_when_blocked = true`, `clothing_item` conditions with `operator = "equipped"` on the leggings and the sports top, and `locked_text = "Needs leggings and a sports top"`, shown greyed as "Go for a run — Needs leggings and a sports top". The inside-choice workaround is dropped.
  - The engine note "hidden, not dimmed" is replaced by how `locked_text` works. Each line was found by grep and read today: parsed at `template_import.py:2598`, carried at `game_graph.py:357`, emitted at v2.py:15183-15185, rendered by the new branch at v2.py:6689-6697 and the dimmed line at v2.py:6741-6748; the absent person stays hidden (v2.py:6685); the `clothing_item` operators are at v2.py:5236-5243.
  - Rule 7 and its "Not this" line now say to use it.
- `craft/clock.md`: the `show_when_blocked` line says the hours show only when the clock alone shut the row, and that `locked_text` covers other locks.
- Every v2.py cite in `craft/*.md` moved with the engine change. The diff adds 6 lines after old line 6690 and 6 more after old line 15173, so I shifted old lines over 6690 by 6 and over 15173 by 12, by script. Spot-checked 19 targets against the new file: advanceTime at 7010, the exit default at 17936, show_when_blocked read at 15104-15108, the render at 6740-6748, locClosedReason at 11772, closed_text at 11444, SchedulePage at 24399, checkAndSubstituteCanvas at 6921, the group's failed slot at 6986, Pattern A at 6993, max_triggers_per_day at 15066, chance at 15092, substitution_only at 15110, exclusive_group at 14684, npc_id at 15086, the daily_tick hook at 7162, the media pool at 16365 and the meter cap at 7377. Each one is the line cited. `lists/COVERAGE.md` and `lists/LESSONS.md` keep their source cites as written, since those record where each idea came from, not a current claim.
- **Approval: LO's own yes, typed in the main-lean session and relayed:** fix how `craft/clothes.md` describes a dress code's ClothingBlock. Found by the game session building P07: at the front door, the block showed only "Go back".
- `craft/clothes.md`: the C1220 row, the engine bullet, rule 6 and example B said both "Change clothes" and "Go back" always show. With `wardrobe_anywhere = false`, "Change clothes" is wrapped in `<<if setup.canChangeClothesHere()>>` (v2.py:21003-21009), which is true only in a `wardrobe_location` room (v2.py:2234-2238). So at a door away from her wardrobe, only "Go back" shows. All four now say so. Example B shows "Go back" only, for this game's shape (changing in her bedroom only). Verified by reading both v2.py ranges. Tests below.
- **Approval: LO's own words, typed in the main-lean session and relayed (ENI for LO, standing authorization, 2026-11-20):** "confirm system rules files with the top games and CoT".
- Created `craft/systems.md`, the systems area's file. It covers energy, daily limits, and the activities she repeats. Money points to `craft/economy.md` and meters to `craft/meters.md`; neither is restated.
  - Must read, 21 rows: C1446, C1386, C1303, C1337, C1431, C1432, C1438, C1342, C1433, C1434, C1313, C1428, C1345, C1423, C1425, C1427, C1360, C1421, C1441, C1369 and C1403. The failure column cites L45 (the stranded player) and L80 (grind).
  - An engine section, measures from CoT and the field, ten rules, a worked example in roles (eat capped at 3 with its TOML, sleep never capped, a run with a clothes gate, a shift greyed by energy), and six "Not this" lines.
  - Each rule says whether CoT and the field agree or split. They split in two places: CoT's needs decay by the hour while IHOH's and SD's are spent, and CoT limits eating by the need while SD counts actions. In both places the file marks our choice as LO's.
- Engine, read today in v2.py:
  - costs on the trigger (`template_import.py:2593`) and taken on entry (v2.py:6168-6175);
  - the cost-blocked row and its dimmed cost tag (v2.py:6706-6707, 6724-6738), and the "Requires … (you have …)" message (v2.py:6183-6197);
  - `max_triggers_per_day` (v2.py:15066, 5590) and the greyed capped row (v2.py:6700-6703);
  - the day key and midnight turn (v2.py:5426-5433, 7021-7022, 7058-7060);
  - daily_tick (v2.py:7162-7164).
  
  A grep finds no special handling of energy, so it moves only by costs and effects, and the file says so.
- CoT, read today:
  - `QuickieBurger.txt`: Work's `<<dtime 60>>` and Rest −20; "You really don't feel like working." at line 6; the `lastdayworked` day stamp at line 18; the first-shift scene at lines 15-17;
  - `BlodgettGymInterior.txt`, lines 34, 43 and 52: each workout's time and need costs;
  - "You really aren't that hungry right now." in `ChamberlainHallInterior.txt`, line 20.
- The field rows come from `round8/ROUND8_REPORT.md` §2.5 and key points, and `round9b/ROUND9B_REPORT.md` §2.1, §2.6, §3 and §4, read today; their numbers were not re-run.
- `SKILL.md`: the area table gives systems its file.
- **Approval: LO's own words, typed in the main-lean session and relayed (ENI for LO, standing authorization, 2026-11-20):** "Confirm it with top games and CoT."
- Created `craft/arc.md`, the arc area's file: one person's story from meeting to where it stops in a release. The meeting, the goal card, heat and meters point to their own files and aren't restated.
  - Must read, 24 rows: C180, C160, C120, C109, C115, C162, C146, C151, C148, C149, C198, C131, C174, C212, C124, C164, C165, C166, C121, C127, C140, C215, C217 and C171. The failure column cites L18 and L80.
  - An engine section, measures, ten rules each saying whether CoT and the field agree or split, a worked example in roles (a housemate's step table), and six "Not this" lines.
  - The one split is rule 3: CoT's own dice and day floor against its players' "making this take months". The rule follows the players.
- Engine, read today:
  - one-time is `is_repeatable = false` (v2.py:15065; `template_import.py:833`);
  - `days_since_flag` (v2.py:5167-5180);
  - `consume_on`, `final` and `retry_after_days` (v2.py:5436-5445; `template_import.py:924-931`);
  - the quest card's `terminal_text` (v2.py:19970-19974; `template_import.py:1405-1411`).
- CoT, read today in the quest log (`_cot_js.txt`, lines 83664, 83665 and 83669): the place-and-hour hint, the wait paired with a thing to do, and the open last line. Also `StoryHintWidgets.txt`, line 123.
- The field comes from `ARC_CRAFT_STUDY.md`. Ten of its cites were re-opened in `round2/passages`, and all ten say what the study says: CoT 43682, 45271, 65940 and 43690; IHOH 9556, 5667, 15597 and 12219; CW 1231. CoT 136570 was opened too; it is one line of the condition, and the study's range covers the rest.
- Not used, and said so in the file: COVERAGE's C156 ("the first third has no sex"), because the field's median is 43%, ranging from 0% to 85%.
- Kept to `plan.md` §9 and L91: the plan holds only the arc's scaffold, and each release designs its own steps. My first draft said to plan the whole arc up front. I caught that against plan.md before sending, and fixed it.
- `SKILL.md`: the area table gives arc its file.
- `plan.md` §9 (line 98) and `templates/PLAN.md` (line 46): the arc scaffold's "first third" now reads "the opening (the steps before the first sex)", so it matches `craft/arc.md`, which drops COVERAGE's C156 because the field's first sex falls at a median 43% of an arc (0–85%). LO's yes, relayed by ENI (2026-11-23: "yes, change the wording and commit it"). Verified by grep: the only "first third" left in the skill is in the lists (LESSONS L83 and L91, COVERAGE C156 and C184), which record sources and stay as they are, and arc.md's note on C156.
- **Approval: LO, typed here, 2026-11-23:** "Go ahead", after the returning-player study sent to the main-lean session (study only, no files changed then).
- Created `craft/returning-player.md`, the returning player area's file.
  - Must read, 21 rows: C1651, C1652, C1653, C1675, C1654, C1655, C1656, C1657, C1658, C1659, C1660, C1661, C1649, C1662, C1663, C1667, C1680, C1681, C1664, C1666 and C1647. The failure column cites L49, L101 and L138.
  - An engine section, measures from CoT and from player comments, twelve rules each saying where CoT, the field and the engine agree or split, a worked example in roles (a release-2 card's `Earlier releases:` line, and the tips-page save line), and five "Not this" lines.
- Engine, read today in v2.py: the backfill (20494-20538, run at 20645), `onLoad` (4018-4038), the version stamps (1700-1702, 20650-20653), `saves.id` (3990), `addToWardrobe` (1736-1745), set_day (4983-4988) and the footer (20812-20820). In SugarCube 2.30's `format.js`: browser storage is keyed by `Story.domId`, a load throws on a saves-id mismatch, and the export label is "Save to Disk…".
- CoT, read today:
  - `update_vars`, 64 cases (`_cot_js.txt`, lines 139889-140850);
  - the hand repair of a misspelt key (139982-139986);
  - `is_prepoint8_save` (136209-136220);
  - `vars.versions` (140833-140834);
  - the legacy passage (round2 CoT passages, line 2401).
- The field: save comments in `round2/comments_text`, from CoT and New Life Project, at the lines cited in the file.
- The study's corrections to COVERAGE are written into the file, not the rows:
  - the backfill also fills `$player.core_traits`, and an existing person's `core_traits` and `flags`, where C1676 says "top level only";
  - CoT renames keys by hand in its update code, which our engine can't, so rule 3 (never rename) holds for us.
- Left out, because they belong to other areas: C1650 (first hour), C1668-C1673 (voice, places, body moments) and C1674 (lostness: `craft/arc.md`, `craft/clock.md`). C1645 and C1648 were also left out: stated, with nothing to check.
- New from the study, rule 12: tell the player how to save to disk. Lost browser saves are the commonest save complaint in the comments.
- `LATER.md`: a new item, "A save check before release 2". The lean skill has no save check; v2's is `saves_mode`.
- `SKILL.md`: the area table gives returning player its file. Only phone has no file now.

## 2026-11-23 (start choice)

- `craft/opening.md` rule 3 and its example, and `craft/want.md` rule 2: the two files disagreed. want.md (C44, measured on CoT's "Think back..." and its `<<pickstartingtrait>>` picks) said the start choice is a memory; opening.md said a person asks "what she wants", a wish. The P13 reader failed every opening on one or the other (games/first_term_lean NOTES, reader pass 7). Now both say the same: a person on screen asks about her past, and the answer is a memory of who she already is. Rule 3 also gains a line: the person asks because of something happening right then, never out of nowhere (LO: a past question with no reason in the scene "look like sense less"). The worked example's question becomes the landlord's "Last girl in that room left owing me three weeks. What makes you any different?" (39 words, was 37), and its three buttons become memories: worked every summer since fourteen, talked her way out of worse, left worse behind. LO's yeses, relayed by ENI (2026-11-23: "yes, go ahead"; "yes, fix the example and add the line"). Verified: lean scripts tests 100 passed.
- `craft/clothes.md` and `craft/body-moments.md`, the C1158 rows: the short rows said prose names a garment only behind a condition or an earlier equip, while clothes.md rule 4 lets the beat that equips her name it. The P13 reader (pass 8) failed the opening's dressing line on the row and passed it on rule 4. Both rows now add "or the beat that equips her", matching rule 4, and cite that failure. LO's yes, relayed by ENI (2026-11-23: "Yes go ahead").
- `craft/people.md` rule 8 and its C660 row: "one meter per person" becomes "one or two meters per person, each shown with its word, each with its own job". One is the field's common case (C660, 9 of 13 games); CoT gives every person two, friendship and lust (`<<friendship>>` 936 calls and `<<lust>>` 833 in round2/passages/course-of-temptation.txt, counted today). first_term_lean's PLAN §3 gives Ryan, Mark and others "want + power", which the P13 reader had flagged against the old rule. LO's yes, relayed by ENI (2026-11-23: "Yes go ahead").
- Every build goes to `games/<slug>/output/` now, the folder LO plays from: `SKILL.md`'s dev build command, `scripts/build.py` (`package()` and the docstring), and the test, renamed `test_every_build_writes_the_output_folder`. Why: dev builds kept landing in `output_dev/`, which LO doesn't play (LO, 2026-11-23: "it keeps building the game in output_dev when it should build the game in output"). The old reason, that `output/` is a public portal (`.gitignore:204-214`), doesn't hold: the portal is LO's own phone play channel (LO, 2026-11-02), and he had a dev build pushed to `output/` on 2026-11-22. The `.gitignore` note now says so. LO's yes, relayed by ENI (2026-11-23: "Yes").
- Every dev build now passes `--dev` and `--debug` together: `scripts/build.py` (`package()`), `SKILL.md`'s dev command, and the test (a dev build has both, a release has neither). Why: LO played a build with no picture placeholders. The engine draws the grey "[IMAGE POOL MISSING]" box only in a debug build (v2.py:16424-16431), and the built `output/index.html` had `debug_mode: false` because build.py added `--dev` alone. LO's yes, relayed by ENI (2026-11-23: "Yes and make sure to use them together").
- `craft/want.md`, worked example: a note that the examples are Markdown. On a game screen the card is one `paragraph` block per line, and bold is `''…''` or `<strong>…</strong>`, never `**…**`. Why: first_term_lean's P13 screen 6 copied the example's `**…**` into one paragraph joined by "·", and LO saw stray stars and one run-on line. LO's yes, relayed by ENI (2026-11-23: "Yes").

## 2026-11-24

Why for all of these: P13's reader found new FAILs on every pass, v5 to v11 (99 FAIL rows over 7 passes, a truth FAIL on 6 of them), and the fix plan came from LO, relayed by the ENI session 2026-11-24 ("Would you send it to the skill session"). This is Part 1 and Part 2 of that plan.

- Part 1 · `craft/voice.md`: the truth rule is ported in full as its own section, "The truth rule", from `.claude/skills/author-game-v2/references/register.md:89-156`: the allowed / not-allowed table, the five rules, the future-promise rule and the seven steps. Changes from v2: her opinions go on her body or out loud (no italic thoughts), schedules are read with `who_is_where.py`, v2's step 7 (a facts list on the draft) is dropped, and one new line in rule 2 and step 7 says a line every path shares must be true on all of them (P13 v11: Mom's "promise me it won't be like high school" on the screen all three start choices leave from, against the grades answer). Shape rule 7 now points at the section. Rule 5 now says how to count the 5 : 1: dialog blocks and quoted words are speech, only screens with someone in them, the worst variant, every path. Why the count: passes counted it differently. Verified: tests green; the cites test passes on the new `register.md:89-156` cite.
- Part 1 · `reader.md`: the reader reads the truth rule from `craft/voice.md`, not from v2's `register.md`, so the writer and the reader read the same text.
- Part 1 · `piece.md`: a new step 3, "Read the card the way the reader will", before `check.py --card`: part B's 13 scene tests on every screen and every path, the truth rule's seven steps, and `who_is_where.py --person` for every line that puts a person somewhere. Steps 3–6 became 4–7 (no other file cites those numbers; step 1, which `check.py` cites, is unchanged). Why: the writer never saw the reader's tests, and `who_is_where.py` ran only in the reader.
- Part 2 · created `scripts/scenes.py` and wired it into `check.py` (`run_all`, the docstring, and `--against <git ref>`). Seven measured checks on the merged TOML: `talk` (every path, screens with someone in them, ≤ 5 : 1), `length` (≤ 150 words a screen, adjacent groups counted as one chain), `presence` (a speaker on a repeatable scene at a place is there at every five-minute slot it can show, by `who_is_where.where`, unless the scene is bound to them or checks them), `creation` (each customization field printed back through `@player` / `@player.<id>`, v2.py:18608-18653), `saves` (against the merged TOML at the last commit of `output/index.html`: removed scene, screen, person, place, flag, meter or garment ids; a meter's bar max or bands; a flag now set only by different choices, unless NOTES.md says `Same meaning: <flag>`), `speakers` (v2 `speakers are named`, gates.py:9500) and `goals` (v2 `_goal_line_reads_true`, gates.py:18911, ported). Created `scripts/tests/test_scenes.py`: 27 tests, a clean game green on each check and a planted break red on each. Verified on first_term_lean, read-only (scenes.run called directly, so nothing under `games/` was written): `creation` is red on the committed TOML (HEAD, the name field never printed) and green on today's working tree, which prints `@player`; `saves` is red on start_fun, start_grades and start_freedom, each now set by a reworded choice against 324ae159; `talk` is red on the opening (5.6 : 1 on its worst path), talk_mom (6.7 : 1) and mom_living_room (7.6 : 1); length, presence, speakers and goals are green. Full suite: 127 passed.
- `LATER.md`: the save-check item and the truth-rule half of the voice item are struck through, done. `craft/returning-player.md`: the engine section's save-check line and rule 11 now point at `check.py`'s `saves` and say what it can't see.
- Step 0 of the rule-pipeline plan (`~/.claude/plans/lean-skill-rule-pipeline.md`, LO relayed 2026-11-24: "Yes go ahead") · `craft/voice.md`, the truth rule's rule 5: "a clothing condition, an earlier equip, or the beat that equips her", cited to C1158. Why: the second copy kept the old wording that `craft/clothes.md:12` dropped on 2026-11-23 after P13 reader pass 8, so the clash came back. Verified: the two lines now say the same.
- Part E of the same plan · created `scripts/reading.py`, the reader's memory. `reading.py games/<slug> <id>` prints the next pass's work list: every row on a new or changed screen, every verdict on the whole scene when a screen changed, every FAIL from last pass, every row whose text changed in its craft file, and every row never judged. A PASS, N/A or WAIVED on unchanged text is carried and marked so. `--all` asks everything. `--record` stamps the reader's verdicts with the screen and row hashes, carries the rest, refuses a verdict not on the work list, a missing verdict and a FAIL with no cause, and writes `games/<slug>/reader/<id>.json` with the FAILs stored by cause. The rows are reader.md's 13 scene tests, and the must-read rows and shape steps of every craft file on the card's `Craft:` line, plus `craft/voice.md`. A screen's hash covers its blocks, its exit, its canvas's trigger, and the schedule rows of everyone it names (a speaker, a name or a one-word role), so a moved schedule row re-opens the screens that name that person. Not covered until the scene sheet (Part C): an equip or flag set on another canvas, and numbers in PLAN.md or other cards; `reader.md` says to re-read with `--all` when one changes. Why: every P13 pass from v5 to v11 judged everything again, and a row (Ryan's step-brother label) passed in v9 and failed in v10 on unchanged text. Created `scripts/tests/test_reading.py`, 11 tests on the tiny game: an unchanged build gives no rows; one changed screen gives only its rows; a carried PASS stays PASS over three empty passes; a FAIL comes back; Mom's moved row re-opens only the screen that names her, and another person's moved row re-opens nothing; `--all`; the refusals; FAILs grouped by cause. Read-only on first_term_lean: P13's first work list is 445 rows over 16 screens, since it has no record yet.
- Part E · `reader.md`: the input is the work list, the output is a JSON file of verdicts with causes plus the table grouped by cause, and "After" says the session records the pass with `reading.py --record`, a pass ends when the work list is empty, and there is no pass limit. It also says what the work list can't see yet.
- Part C of the rule-pipeline plan (LO relayed 2026-11-24: "Commit and continue") · created `scripts/sheet.py`, the scene sheet. From the merged TOML it works out, for each screen of the card's canvases with every path merged, five columns:
  - **clock:** the start time from `[time]` (v2.py:1592-1593), plus each choice's minutes, 3 when it has none (v2.py:17744, 17758); a repeatable shows its window, or "while <id> is there" when it is bound to a person;
  - **place:** the trigger's location, or the card's own place, marked "(card)", where the engine has none (the opening);
  - **who is there:** from `who_is_where.where`, with "(part)" for someone there only some of the time;
  - **what she wears:** the `initial` garments (v2.py:1213-1235), then each equip on the path, with the dress rule (v2.py:1760-1766); on a repeatable, only what its trigger checks, else "any";
  - **flags:** those set before the screen, with the ones that differ by path after "by path:".
  
  `sheet.py games/<slug> <id>` prints the rows in the card's format. Why: on P13 a fact lived only in prose, so a fix broke another line (Ryan's row moved two minutes, and "the empty hall" went false).
- Part C · `check.py`: a new `sheet` check compares each card's `Sheet:` block with the computed sheet. It is red on a different value, on a screen built but not on the sheet, and on a sheet row that isn't built. A column it can't work out is INCOMPLETE, never green. A card with no `Sheet:` block is not compared, so the cards approved before today stay as they are. `--card` is red on a card that has `Screen <n>` lines and no `Sheet:` block, so every new or re-carded piece gets one. `templates/piece-card.md` has the `Sheet:` block, and `piece.md` step 2 says it comes before the prose.
- Part C · `scripts/reading.py`: a screen's hash now takes in its sheet row, so an equip or a flag changed on an earlier screen re-opens the later screens. The docstring and `reader.md` say what's still outside the hash: a number in PLAN.md or another card, and what another canvas does to her clothes before a repeatable.
- Part C · created `scripts/tests/test_sheet.py`, 12 tests: the computed sheet, a matching card green, and these planted wrong facts red: a wrong time, a person who isn't there, a garment not on yet, a missing flag, and Mom judged at the card's place. Also: a screen missing from the sheet or not built is red, an unknown place is INCOMPLETE, an old card with no sheet is not compared, `--card` asks for a sheet, and an upstream equip change re-opens the later screen. Suite: 150 passed.
- Verified read-only on first_term_lean (nothing written under `games/`):
  - P13's computed clock runs from 07:00 (wake) to 07:50; the hall screens are 07:20–07:25.
  - With the card's places supplied in memory, Ryan is in `home_hall` there, inside his 07:12–07:25 row. Mark and Mom are in the kitchen from 07:05 to 07:12. Mom is alone in the kitchen at the hand-over (07:35 on), since Mark's row ends at 07:30.
  - She wears nothing (engine-wise) until her room's exit equips her outfit, because no garment is `initial`.
  - `check.py`'s `sheet` is green, because no card has a `Sheet:` block yet. `--card P13` is now red for the missing block; P42, P07 and P06 are not.
- Parts A and F of the rule-pipeline plan, the frame and the first area (LO relayed 2026-11-24: "Commit and continue"):
  - **`SKILL.md`, new section "Rule labels":** the 21 `when` triggers, each with what it means, and the three judges (`script + <check>`, `reader`, with `+ <check>` when a check helps, and `note`). Two triggers are new beside the plan's draft:
    - "a scene's last screen", because C450 (end on a hook) applies only there;
    - "a rule is changed", because L163 governs skill edits, not screens.
    
    A `script` or `reader` row needs a real failure, or says why it stays blocking. SKILL.md is now 142 lines.
  - **`scripts/check.py`:** a new `CHECKS` tuple lists every check a judge may name.
  - **`craft/voice.md`:** the must-read table gains `when` and `judge` columns, and every row is labelled. All eleven rows are `reader`; C460 is `reader + presence, sheet, creation`. Under Part F's exemption (the voice, the truth rule, LO's own rules), nothing is demoted to `note`. The seven voice rows with no recorded failure say "— · kept blocking: the voice, LO's (2026-11-22)", and C461 says "kept blocking: the truth rule". C460's failure column now names P13 reader pass 11 (Mom's "high school" line). A line under the truth rule's five rules says who judges each, and that rule 3 applies on a repeatable.
  - **`scripts/tests/test_skill.py`:** six new checks:
    - `label_problems`: every row of a file on `LABELLED` has five columns, a `when` from SKILL.md's list, a judge, a check name for `script` that is in `CHECKS`, and a failure for `script` and `reader`;
    - `home_problems`: an id's row text lives in one craft file and the others point to it ("see `craft/x.md`"), judged only for ids in a labelled file;
    - a test that `CHECKS` covers every scene check;
    - planted breaks for each;
    - a test that an unlabelled file isn't judged until it's listed.
    
    `LABELLED = ["craft/voice.md"]`. `PENDING_HOMES = {C447, C448, C593}` waits on LO's choice of home, because voice.md and people.md each hold a copy. Suite: 159 passed.
- Voice decisions applied (LO relayed 2026-11-24: "Yes continue"):
  - C447 and C593 live in `craft/voice.md`, and `craft/people.md` points there.
  - C448 lives in `craft/people.md`, with voice's fuller wording ("… in the first lines"), and `craft/voice.md` points there.
  - Two failure columns are filled from the reader tables, checked first: C593 is P13 reader pass 7 (Mark had no term of address for her, `reader_first_term_lean_P13_v7.md`, line 82); C448 is pass 10 (Ryan arrived as a bare name, `…_v10.md`, line 42).
  - `PENDING_HOMES` no longer holds them. people.md's rows keep three columns until its area is labelled.
- Parts A and F, the second area: `craft/clothes.md` and `craft/body-moments.md`, labelled together because they share C719 and C1158.
  - **`SKILL.md`:** a new trigger, "the plan", because 8 clothes rows (C1167, C1204, C1183, C1171, C1169, C1150, C1201 and the like) design the whole clothes system, not a screen.
  - **`craft/clothes.md`, by Part F's default:**
    - 18 rows with "—" become `note`;
    - C1206 stays blocking, as the truth rule's clothes half;
    - C719, C1158, C1220 and C1221 stay `reader`, with their failures;
    - C1158 and C1206 are helped by `sheet`, and C1221 and C1169 by `reach`.
  - **`craft/body-moments.md`:** C1275, C1274 and C1277 become `note`. C1262, C1280, C1279, C782, C1158 and C719 stay `reader`.
  - **Shared ids, waiting on LO's choice of home** (`PENDING_HOMES`):
    - C719 and C1158 (clothes and body-moments);
    - C1262 (body-moments, media and walk-ins);
    - C1274, C1275, C1277 and C1280 (body-moments and media).
  - `test_skill.py` `LABELLED` now holds three files, and two planted tests anchor on C644, since people.md's C447 row is now a pointer. Suite: 159 passed.
- Clothes, body-moments and media decisions applied (LO relayed 2026-11-24: "Yes"):
  - **Homes:**
    - C719 lives in `craft/clothes.md`, with clothes' wording.
    - C1158 lives in `craft/clothes.md`, with body-moments' fuller wording ("… undressing in an act is backed by the act").
    - C1262 lives in `craft/body-moments.md`; `craft/media.md` and `craft/walk-ins.md` point to it.
    - C1274, C1275, C1277 and C1280 live in `craft/media.md`, with media's wording; body-moments points to them.
  - **Kept blocking:** C1166 and C1200 (shape rule 7 cites C1200), each "— · kept blocking: LO's choice (2026-11-23)". The other 16 clothes rows stay notes.
  - **`craft/media.md` labelled:** C1249 and C1274 are `note`; the rest are `reader`, each with a failure.
  - **New shared id:** L97 (media and walk-ins, different wording) waits in `PENDING_HOMES`.
- Parts A and F, the third area: `craft/people.md`, `craft/opening.md` and `craft/want.md` are labelled.
  - **Failures filled from the P13 reader tables, each checked first:**
    - C630: pass 10, Ryan's name and never his relation;
    - C44: pass 7, the start choice was a wish, not a memory;
    - C48: pass 11, the name was never printed back. C48 is `script + creation`.
    - C596: pass 12, Mom's talk screen at 26 words and 42% spoken. Labelled `note + talk, length`, because its ~55 words is a borrowed number.
  - **Length rows:** C519, C1626 and C1637 are `note + length`; C520 is `reader + length`.
  - **Other help from checks:** C1631 (where the hand-over lands) is `reader + sheet`.
  - **Opening rows:** all are `reader`, each with a P13 failure.
  - **Notes:** every people and want row with no recorded failure is a `note`, by Part F's default. Shape rules marked "LO's choice" (people 6 and 8, want 1, 5 and 6) are listed for LO to keep blocking.
  - **Shared ids waiting on LO's choice of home** (`PENDING_HOMES`): C109, C166, C311, C598, C639, C640, C952, C954, C992 and L97.
  - Suite: 159 passed (the unlabelled-file test now uses arc.md). Sizes: people 110, opening 108, want 90 lines.
- The size cap no longer covers `CHANGELOG.md` (LO relayed 2026-11-24: "Yes"). It is a diary, not an instruction file (C2170). `test_skill.py`'s `size_problems` skips it, its planted test now writes a 2,000-line CHANGELOG that must not count, and `SKILL.md`'s "Size caps" line says so. Why: the CHANGELOG reached 420 lines and turned `test_sizes` red. The earlier "159 passed" was run before that batch's CHANGELOG lines went in, so it was not the state handed over.
- Decisions from the third batch applied (LO relayed 2026-11-24: "Yes"):
  - **Homes:** C109 and C166 live in `craft/arc.md`. C166 takes opening's fuller wording, and both keep opening's P13 failures. C311 lives in `craft/opening.md`. C598, C639 and C640 live in `craft/people.md`. C952, C954 and C992 live in `craft/economy.md`, and C952 and C954 take the merged wordings LO approved. L97 lives in `craft/walk-ins.md`. Every other copy is now a pointer.
  - **Kept blocking:** C656, C660, C34, C35, C36, C37, C433, C54 and C952 are marked "— · kept blocking: LO's choice (2026-11-24)".
  - **C1619** now names its failure: LO played P13's sums screen on 2026-11-23, and goal 1's card was one run-on line with stray stars ("What is this??"; fixed in 324ae159).
  - **C430 is kept blocking as LO's choice, not with that failure.** Its rule (each step says how to find the next) wasn't what broke: the steps did say where and when, and only the layout was wrong.
- Parts A and F, the last batch: arc, heat, economy, meters, places, clock, systems, walk-ins and returning-player are labelled. Every craft file is now labelled, and `LABELLED` in `test_skill.py` is every file in `craft/`.
  - **New test:** the unlabelled-file test plants a new craft file.
  - **`SKILL.md`:** "Rule labels" says every file is labelled.
  - **Default labels:** rows with a failure are `reader`, and rows with "—" are `note`. The exceptions:
    - C249 is `script + beat`;
    - C1656 and C1658 are `script + saves`;
    - L106 is `reader + presence`;
    - C1428 and C1652 are kept blocking as "LO's rule";
    - checks help on C254 and C239 (beat), C770 (length), C921, C927 and C931 (sheet), and C1657 and C1659 (saves).
  - **Real failures filled in from the P13 reader tables** (every note row in every craft file was grepped against passes v5 to v12):
    - C180, C149 and C217 (v6);
    - C1022 (v8, "dollar");
    - C900 and C928 (v6, "Monday, seven in the morning.");
    - C920 (v7, 10 min against 5 min);
    - C541 (v9);
    - C1658 (v11, start_fun).
  - **Shared ids waiting on LO's choice of home:** C285 (heat and meters), C212 and C174 (arc and walk-ins), L70 (meters and walk-ins), and L147 (places and walk-ins).
- Parts A and F finished (LO relayed 2026-11-24: "Yes").
  - **Homes:**
    - C285 lives in `craft/meters.md`, with meters' wording; heat points there.
    - C212 lives in `craft/arc.md`; walk-ins points there.
    - C174 lives in `craft/arc.md`, with walk-ins' wording ("a person's next arc step comes before any dice").
    - L70 lives in `craft/meters.md`, with walk-ins' fuller failure ("…behind a 1-in-4 walk-in").
    - L147 lives in `craft/walk-ins.md`. Places' failure for it ("15 places said 'Nothing to do here right now'") moved to places' C762 row, beside L150.
    - `PENDING_HOMES` is empty, so the one-home test runs on every id in every craft file.
  - **Heat, kept blocking as LO's rules:** C254, C248, C239, C276, C255, C256 and C252, each marked "LO's rule, explicit prose is the register (CLAUDE.md; 2026-11-24)". C254 is `script + beat`, and C249 stays `script + beat`. C255, C256 and C252 keep the trigger "the plan": they are game-wide shares, and "the plan" covers the game plan and each release's piece list, so they apply from release 1. "a release after the first" would skip release 1.
  - **Kept blocking as LO's choice (2026-11-24):** C284 and C289 (heat); C164 and C165 (arc); C951, C989, C990, C1016 and C1017 (economy); C773, C776, C777 and C738 (places); C913, C914, C916, C903 and C890 (clock); C1431, C1432 and C1438 (systems); C1667, C1681, C1647, C1664 and C1666 (returning-player). All other "—" rows stay notes.
- Part B of the rule-pipeline plan, the rule list per piece (LO relayed 2026-11-24: "Yes"):
  - **Created `scripts/rules.py`.** `table()` reads every labelled home row; pointer rows are skipped. `card_does()` parses the card's new `Does:` block (`<canvas>.<node> | <trigger>, …`). `rule_list()` gives each screen every `always` row plus the rows whose `when` names one of its triggers. `plan_rows()` lists the "the plan" rows.
  - **The guard:** `seen()` and `meetings()` work out what a script can see a built screen do: a person on screen, one-time or repeatable (the starting canvas counts as one-time), the opening, the last screen, an equip on its exit, a catalog garment named, a "$" figure, a time on a label or in prose, a picture or clip, an effect on a meter (not energy or money), a goal card (✅ or ➜), an exit to a place, and a met_ flag (named on the screen that sets it or the one it leads to). `guard()` is red when the `Does:` line leaves one out. It can't see these, which the writer names: a moment alone with her body, something sexual shows, an explicit beat, a walk-in, a release after the first, and a price written in words ("seventy-five").
  - **`check.py`:**
    - `--rules <game> <id>` prints the list, grouped by judge, with each rule's home and how many screens it applies on; `--rules <game> plan` prints the plan's rows.
    - `--card` is red on an unknown trigger, a non-screen trigger ("always", "the plan", "a rule is changed"), a screen with none, `Does:` and `Sheet:` naming different screens, and a card with `Screen <n>` lines and no `Does:`.
    - A new `does` check runs the guard on every card with a `Does:` block. Cards without one are not judged.
    - `CHECKS` gains "does".
  - **`reading.py`:** for a card with `Does:`, the rows are its rule list plus the 13 scene tests, each hashed with its labels. A changed screen asks only the rows its triggers fire. Cards without `Does:` keep the old rows.
  - **`piece.md` step 1:** write the screens and `Does:` first, print the list with `--rules`, then read each rule in its home. Cards without `Does:` keep the old area reading.
  - **`templates/piece-card.md`** gains the `Does:` block, and **`reader.md`** says the rows come from the same list.
  - **Created `scripts/tests/test_rules.py`, 21 tests:**
    - the list is the `always` rows plus the screen's triggers, pointers are skipped, and plan rows are their own list;
    - planted bad `Does:` lines are red, and so is a screen mismatch with `Sheet:`;
    - an old card isn't asked;
    - the guard is green when `Does:` names everything, red for each of 7 planted missing triggers, and accepts a first meeting on either screen;
    - the CLI works;
    - a changed screen asks only its own rows.
  - **Verified read-only:** a `Does:` block for P13 was written into a scratchpad copy of the card, with `games/first_term_lean/toml_phases` linked read-only. The guard is green on it. P13's list is 156 rules: 1 script, 88 reader, 67 note. That is 169 rows with the scene tests, against today's 445 from the whole craft files. By screen: 64 to 103 rules (the hall 103, the bathroom and knot screens 99, the kitchen and start-choice screens 64).
  - **Proposed, not done:** `Does:` replaces the card's `Areas:` and `Craft:` lines; plan.md runs `--rules … plan`.
- Three follow-ups to Part B and Part D (LO relayed 2026-11-24: "Yes"):
  - **`Does:` replaces `Areas:` and `Craft:` on new cards.** `check.py --card` judges a card with `Does:` only on `Does:` and `Sheet:`: known triggers, one per screen at least, the same screens. The cite-every-id check is gone for it, because listing an id is not applying it. A card without `Does:` keeps the old `Areas:` and `Craft:` check, so the cards approved before today stay green.
    - `templates/piece-card.md` drops the `Areas:` and `Craft:` lines, and `Card checks:` pastes the `--rules` count line.
    - `piece.md` steps 2 and 4 and `SKILL.md`'s "Areas." paragraph say so.
    - Tests: a card with `Does:` and no `Areas:` or `Craft:` is green.
  - **`plan.md`:** a new line has the writer print `check.py --rules games/<slug> plan` before the first bite and before each release's piece list, and write to those rules. It says plainly that the reader does not judge them yet.
  - **"the opening" and "a one-time step" tightened.** 25 rows were relabelled, with no rule text changed. `SKILL.md` gains five triggers, each with two or more rows:
    - "the first screen": C54, C43, C1626, C1613, C1628;
    - "the start choice": C43, C44;
    - "the hand-over": C1604, C1609, C1621, C1631;
    - "a person's arc step": C180, C120, C109, C115, C162, C148;
    - "a no is possible": C164, C165, C166, C639, C640.
    
    Other relabels: C146 is now "a repeatable" only. C1166 is now "she dresses or undresses". C48 and C51 are now "the plan", because the creation screen is the engine's, not a canvas screen, and `creation` still checks C48 at every build. Three rows keep "the opening" because they hold on every opening screen: C520, C1611 and C327. No row is left on "a one-time step"; the trigger stays, and the guard still sees it.
    - The guard (`rules.py`) now sees "the first screen" (the starting canvas's first node) and "the hand-over" (its last screens).
    - Tests cover both triggers.
    - **Verified read-only on the scratchpad P13:** 153 rules (166 with the scene tests) against 156 (169), and 988 rule-screen pairs against 1,287. The hall goes from 103 to 89 rows and the start-choice screens from 64 to 45.
  - **Part D:**
    - **`build.md` is written in full** (60 lines): build; the scripts, the sheet and the `Does:` guard, all blocking; the reader on `reading.py`'s work list, where reader rows, scene tests and the truth rule block and notes are shown on their own; record the pass; close the piece; LO plays. There is no pass limit. Commits: LO decides when, and a session commits only on his word.
    - **`SKILL.md`'s loop** steps 2, 6 and 7 match it. Always rule 7 now reads "LO decides commits", which is what is true today. Its "check" row names `scenes.py`, `sheet.py` and `rules.py`, and a new row names `reading.py`.
- `scripts/reading.py` fix, from a real failure (ENI for LO, standing authorization, 2026-11-24).
  - **The failure:** the live P13 trial. Pass A's work list was 161 items, all on `*`, and the reader answered 136 of them on `*`. One line then changed on `opening.room_spoke`. Pass B's work list was 229 items with 31 carried, because every `*` verdict was re-asked as "a screen of the scene changed". After a first pass, the carry never engaged.
  - **The fix:**
    - A `*` PASS now means "passes on every screen the row fires on". When a screen changes, only the rows that fire on it (an `always` row, or a trigger on its `Does:` line) are asked again, for that screen, and the `*` verdict carries for the rest. `record()` keeps a carried `*` verdict beside a new verdict on one screen.
    - Three scene tests judge the scene as a whole and are asked on `*` only, again after any change: B1 (wanting shown earlier), B2 (one step further) and B9 (companion and rival). They are `SCENE_WIDE` in `reading.py`.
    - `--record` refuses a `*` FAIL; a FAIL names the screen of its line.
    - A card without `Does:` keeps the old re-ask.
    - The first pass is still asked on `*`, not as rule-and-screen pairs.
  - **Verified:**
    - On the live record, read-only: 93 items (90 on room_spoke plus B1, B2 and B9), 164 carried, against 229.
    - On a copy of `reader/P13.json` in the scratchpad: the same 93. After a simulated pass on those 93, the work list is empty.
    - Tests: `test_rules.py` has four new ones on the tiny game: a `*` PASS is asked again only on the changed screen and carries for the other; only the scene-wide tests go back on `*`; a `*` PASS survives a new verdict on one screen; a `*` FAIL is refused.
    - `reader.md` and `reading.py`'s docstring say so.
- `craft/arc.md`, a gap the P21 card found (ENI for LO, standing authorization, 2026-11-24).
  - **The failure:** P21's card as first written made Tom's hire and Chris's first shift one-time canvases with `consume_on`, meant as buttons. In v2 a one-time canvas at a place fires by itself on entry (v2.py:5895-5915, 6511-6522), and buttons and a person's menu list only repeatables (v2.py:5925-5944, 5958-5975). The writer found it only from the engine, before any build.
  - **The fix:**
    - A new engine bullet, "How a step reaches her", says how a step reaches her and that self-firing doesn't check the person is there (v2.py:6083-6086, with the played zoe_00 case, `.claude/skills/author-game-v2/CHANGELOG.md:690`). A step that fires on arrival and needs a person gates on `npc_at_location` or their hours. A step she chooses from a menu is a repeatable row: a done flag, a parked flag cleared by `[engine.daily_tick]`, presence and hours, and `show_when_blocked` with a `cooldown_message`.
    - `consume_on` stays for a step that happens on arrival.
    - Rule 7's "In the engine:" sentence now names both.
  - **`rules.py`'s guard** is now red when `Does:` names "a person's arc step" and "a no is possible" on a screen of a one-time canvas at a place (not the starting canvas) whose trigger has no `npc_at_location` (is_present) or `time_of_day`. Two tests cover the red, a presence gate, and an arrival step with no "no".
  - **Not done:** an engine test pinning both filters is an engine edit, put to LO.
- Presence and the scene sheet now read weekday items (ENI for LO, standing authorization, 2026-11-24).
  - **The failure:** P21's build. `fire_slots` in `scenes.py` and `window` in `sheet.py` read only `time_of_day` items, so a trigger's `{ type = "weekday", weekdays = [0..5] }` (v2.py:5203-5207) was ignored. That gave 7 presence reds ("Tom isn't there Sun 10:00" on a scene that can't show on Sunday) and 6 "(part)" reds on the sheet.
  - **The fix: one shared helper,** `who_is_where.when_slots(conditions)` with `item_slots(item)`, used by both `scenes.fire_slots` and the sheet, so they can't drift.
    - **Which items count:** `time_of_day` (its window) and `weekday` (its days; an empty list never holds). These are the only clock items the engine reads by the week. Every other item counts as every slot.
    - **AND and OR:** an AND block intersects its items. An OR block is the union of its items, so an OR holding any non-clock item stays every slot. This can't make a false green: a wider set of slots only asks more of presence, and on the sheet only marks someone "(part)", never present. A block without version "1.0" is every slot, as in the engine (v2.py:5028-5035).
    - **Nested blocks:** the engine's evaluator reads a flat item list; an item with its own `items` is read the same way here, defensively. The old `items()` flattened every item and intersected them, so an OR would have narrowed wrongly. It is no longer used for the clock.
    - **The sheet's clock column** now names the days: "07:00–09:00 +0 · Mon Tue Wed Thu Fri Sat".
  - **Two more fixes, found on P21 the same pass:**
    - **Who is there is read at the minute a screen shows,** not across the time its choice spends. A "4 hours" shift button marked Chris "(part)" because he leaves mid-shift.
    - **Order doesn't matter in a set column:** the sheet's who, wearing and flags columns are compared as sets ("npc_tom, npc_chris" equals "npc_chris, npc_tom").
  - **Tests:** 7 new:
    - a Mon–Sat scene has no Sunday red, and a planted every-day scene with Mom off on Sunday stays red;
    - an OR of two windows covers both, and goes red when the evening window loses Mom;
    - an OR with a flag item never narrows;
    - an empty weekday list never holds;
    - the sheet reads the weekday;
    - order in a set column doesn't matter.
  - **Verified read-only on first_term_lean:** presence is green, where it had 7 reds. The sheet's 16 remaining P21 reds are the card's own wording: clocks written as "Mon–Sat 10:00–20:55, any minute", Chris written "by the hour as above" where the sheet says "npc_chris (part)", and flags set by other canvases (met_tom) or negatives ("not cafe_hired"), which the flags column doesn't model. It holds flags set on the path plus flags the trigger checks `is_true`.
- The sheet check keeps its teeth (ENI for LO, standing authorization, 2026-11-24).
  - **The hole:** my own advice on P21 was to paste `sheet.py`'s rows into the card. A pasted row agrees with the build by definition, so the check stops checking. P21's card now holds pasted rows.
  - **The fix:**
    - `piece.md` step 2 and `build.md` step 2 say a red sheet row is never fixed by pasting the script's value. The writer says per row whether it is (a) format only, (b) a wrong story (fix the story, then the row), or (c) a wrong script (stop and report), and records (b) and (c) in NOTES.md.
    - To make (a) rare, `sheet.py` compares the clock by meaning (`clock_meaning`). A hand-written clock becomes the (day, minute) slots the screen shows at:
      - days: "weekdays", "weekends", "daily", "Mon–Sat", or day names; no days means every day;
      - the window, with an optional "+N"; with none, the window is already the screen's;
      - "any", and "while <id> is there";
      - the opening's "07:20–07:23" compared as exact in and out minutes, with the leading zero optional.
      
      Who, wearing and flags were already compared as sets.
    - `templates/piece-card.md` lists the accepted hand forms, so a row can be written before any build.
  - **Tests:** 11 new in `test_sheet.py`:
    - four hand forms equal to the build's "10:00–20:55 +5 · Mon Tue Wed Thu Fri Sat" (among them "Mon–Sat 10:05–21:00" and "weekdays and Sat 10:05–21:00");
    - four that differ in meaning (Sunday added, a wider window, weekdays only, a double shift);
    - "weekdays" equal to "Mon Tue Wed Thu Fri";
    - the opening's exact clock green by hand and red when a minute is off.
  - `piece.md` also says `sheet.py` prints the build's rows for reading a red, never for pasting.
  - **Verified read-only:** on first_term_lean's P21, the one red left is a flag (met_chris on cafe_first_shift.end, which the build doesn't set before that screen). The game session judges it as (a), (b) or (c).
- `craft/arc.md`, "How a step reaches her": the bullet now cites `apps/game_generation/tests/test_step_shapes.py`, the engine test LO approved and ENI added on 2026-11-24. Its 5 tests check that auto-fire takes only non-repeatables, that entry fires the auto-fire pick and marks it, that the room list and a person's menu take only repeatables, and that `is_repeatable` reaches the payload both ways. With it, the craft line's v2.py cites can't drift silently. Verified: the test file runs green (5 passed), and the skill's cites and pointer tests pass.
- `reader.md`, scene test B1 (ENI for LO, standing authorization, 2026-11-24).
  - **The failure:** P21 reader pass B. B1 failed on Chris's brush at the machine (`cafe_first_shift.start`), his first canvas, although his want was on the same screen before the act ("He looks you over like he's pricing you."). B1 had no first-meeting exception, so no line could make a brush on a first meeting pass.
  - **The change:** on a person's first canvas, his want shown on the same screen, before the act, on his body and seen by her (C613), satisfies B1, but only when the act is an accident or his brush, the lowest rung (C286). A deliberate touch, a grope, or anything above that rung still needs an earlier canvas. It is worded like part A's C109 exception, and it points at C613 and C286 in `craft/people.md` and `craft/heat.md` rather than copying them.
  - **Shared wording checked:** no craft row states B1's "an earlier canvas showed him wanting it". C613 and C109 are related and unchanged.
  - **Narrower than C286:** C286's stage 1 lists "his brush or grope"; the grope is left out on purpose, per the instruction.
  - **Verified:** B1's text changed, so `reading.py` re-asks B1 on its next pass (its row hash covers the text).
- `scripts/scenes.py`, `presence`: a line inside a group is judged only when its groups hold (ENI for LO, standing authorization, 2026-11-24).
  - **The failure:** P10's build. The weekend shift puts Tom's line inside a Saturday group (`weekday`, `[5]`) and Chris's inside a Sunday group, and presence still said "Tom isn't there Sun 10:00". `check_presence` narrowed the slots by the trigger only; `walk()` handed it each block's group conditions, but those were read only for `npc_at_location`.
  - **The fix:** each dialog block's slots are the trigger's `when_slots` intersected with `when_slots` of every enclosing group's conditions. It is the same helper, with the same OR widening.
  - **What isn't modelled:** adjacent groups merge into one if/elseif chain, so a later group also needs the earlier ones to fail. A group's own conditions are a superset of when it shows, so this can keep a red too long but never hide one. A comment in the code says so.
  - **The sheet:** it reads who is there only from schedule rows at the screen's place and time, never from text inside a group, so it needed no change.
  - **Tests:** three new: a Saturday-group line on a Sat–Sun scene is green on Sunday; the same line outside the group is red; a group with a `time_of_day` narrows too, and goes red once the line leaves the group.
  - **Verified read-only:** presence on first_term_lean is green.
- `craft/clock.md`, C903 and shape rule 7 (ENI for LO, standing authorization, 2026-11-24).
  - **The failure:** P10's reader pass A. The rule said flatly "no named weekday on a repeatable", but P10's weekend shift names "Saturdays" and "Sundays" inside weekday groups, which is true on every visit. The reader passed C903 only by reading around the rule.
  - **The change:** the C903 row now says what it means: "a repeatable names a weekday only behind a weekday condition, on its trigger or a group around the line, that makes it true on every visit". Rule 7 says the same in one line, with one example each way, and cites C903.
  - **One home:** C903 lives only in clock.md, and no other file holds a copy (checked with grep). The labels (the clock moves, reader, LO's choice) are unchanged.
  - **Verified:** the full suite runs green. The rule text changed, so `reading.py` re-asks C903 on the next pass of any piece whose list holds it.
- `scripts/reading.py`, two fixes (ENI for LO, standing authorization, 2026-11-24).
  - **The failure:** P10's and P21's pass B.
  - **(1) A FAIL on a `note` row never left the work list.** P10's three C151 FAILs ("a repeatable stays short") kept coming back. Adding lines failed C151, and cutting them failed the blocking `talk` check, so the list could never empty.
    - **Fix:** on a card with `Does:`, a note's FAIL is recorded with no cause and carried like a PASS. It comes back only when its screen's text, its facts or its rule change. `--record` doesn't ask a note FAIL for a cause. `by_cause` shows notes in their own section, and the `--record` exit counts only FAILs that hold.
  - **(2) A moved fact re-opened every row.** Chris's weekend row moved from 19:00 to 20:00, and through the sheet hash that re-asked every row on every screen naming him: P21 asked 349 rows, against 151 on pass A, and P10 asked 298, against 101.
    - **Fix: the screen hash is split** into `text` (the node and its trigger) and `facts` (the schedule rows of the people it names, and its sheet row). It also keeps `all`, the old single hash, so records written before still read. A changed old-format screen counts as a text change, the safe reading.
    - A text change re-asks the screen's rows as before. A facts-only change re-asks only the rows that read facts:
      - the truth rule, C460 and C461;
      - scene tests B8 (the numbers and the clothes agree) and B10 (true on every visit). B8 is added beside ENI's list, because clothes are on the sheet row;
      - rows judged `+ presence` or `+ sheet`;
      - rows whose `when` is "a person is on screen", "the clock moves", "a garment is named" or "she dresses or undresses".
    - The scene-wide tests B1, B2 and B9 go back on `*` only after a text change.
    - **Why this can't miss a truth break:** a moved fact can only break a line that claims that fact, and every such line is judged by C460 and B10, which apply on every screen and are always re-asked where facts moved.
  - **Tests:** three new in `test_rules.py`: a note FAIL carries while a reader FAIL comes back; a note FAIL re-opens when its screen changes; a facts-only change (Mom's row moved) asks only fact-reading rows, C460 and B10 among them.
  - **Verified on a scratchpad copy of `reader/P21.json`:**
    - the live record (old format) reads as unchanged against today's build;
    - after one simulated pass, replaying Chris's weekend row move re-asks 102 items, 34 rules, against the 349 seen;
    - many of those come from "a person is on screen" rows, such as C447, C593 and C625, which judge how a person sounds or is named, not where they are. Narrowing that trigger out of the fact list would cut it further, which is LO's call.
- `scripts/reading.py` and `reader.md`: "a person is on screen" is no longer a trigger that marks a rule as reading facts (LO, relayed 2026-11-24: "yes"). Those rows judge how a person sounds or is named, not where they are. Still re-asked when only a fact moves: C460 and C461, B8 and B10, rows judged `+ presence` or `+ sheet` (L106 among them), and rows whose `when` is "the clock moves", "a garment is named" or "she dresses or undresses". Verified on the scratchpad P21 replay of Chris's weekend row move: 72 items, 24 rules (C460, C461, B8, B10, L106 and 19 clock rows), on the 3 screens that name him. Before this change it was 102 items, and the pass B count was 349. The full suite runs green.
- `piece.md` step 7 and `build.md` step 1: the overlap rule (LO's yes, relayed by ENI 2026-11-24). While the reader runs on a piece, the next piece may be carded, checked and approved, but not built. Only one piece is built at a time, because the reader reads the built game, and a build under it changes what it reads. If the current piece's fixes change a fact the next card uses (a schedule row, a flag, a price), that card is re-checked and takes a new yes. Why: the game session builds release 1's remaining pieces back to back tonight. Verified: the suite runs green, and the size caps hold.
- `scripts/reading.py` and `reader.md`: `--record` takes a partial batch (ENI for LO, standing authorization, 2026-11-24).
  - **The failure:** reader passes take more than 10 minutes and died with each of the day's machine restarts. `record()` refused any batch missing a verdict ("work-list item(s) have no verdict"), so a pass couldn't be saved in parts.
  - **The fix:** a batch records the verdicts it gives. The items it doesn't answer are kept in the record as `pending`, and the next work list asks them again ("still to ask: …"), whatever the hashes say. Without that, the new screen hashes would hide a changed screen's unanswered rows.
    - An unanswered item keeps the verdict it had, so a FAIL not yet asked again is still a FAIL.
    - A carried verdict is dropped for a `*` re-ask only when that re-ask was answered.
    - Causes add up across a pass's batches, and a later batch may name an earlier batch's cause.
    - The pass number moves on only when the last pass had nothing pending.
    - It still refuses a `*` FAIL, a FAIL with no cause on a reader row, and a verdict not on the work list.
    - It prints "recorded N of M; M−N still to ask".
    - `reader.md` says to record every ~40 items.
  - **Tests:** four new:
    - a partial record keeps exactly the unanswered items on the next list, and a second batch finishes the same pass with an empty list;
    - a pending row of a changed screen survives the new hashes;
    - an unanswered FAIL stays a FAIL and is asked again;
    - a partial batch still refuses a `*` FAIL and an off-list verdict.
    
    A full record behaves as before: every earlier test passes unchanged.
  - **Verified read-only:** the live records under `games/first_term_lean/reader/` are written in the old format, without `pending`, and still give their work lists. I didn't touch `batches/`.
- `craft/systems.md`, `plan.md`, `lists/LESSONS.md`: repeat activities aren't scheduled around each other (LO, relayed by ENI 2026-11-24: "yes, do both").
  - **The failure:** first_term_lean's café shifts (P10) were locked to fixed slots: weekdays at 2pm, placed after the 9–1 lectures so they would never clash, and weekends at 10am and 3pm. The plan did it, and no rule stopped it. Rule 6's "where and when" invited it, and C1446's "she chooses it" is only a note.
  - **The fix:**
    - New lesson **L166** in `lists/LESSONS.md`, under Other.
    - New must-read row **L166** in `craft/systems.md`: `when` = a repeatable, judged by the reader, blocking on the P10 failure.
    - **New shape rule 7:** a repeat activity is open whenever its place is open and its people are there. Fixed times only when the activity really happens at a time (a class, a party), and the card says why. Never place one activity around another to avoid a clash; when two compete for the same hours, that's the player's choice.
    - **Measured in CoT:** the "Work" link in `QuickieBurger.txt` (lines 4-30) checks the job, her need and how she looks, and no hour. It costs one hour a click (`<<dtime 60>>`), and only her need stops it ("You really don't feel like working."). Classes, checked in `_cot_js.txt` by ENI and re-read here: they run in scheduled blocks (`setup.School.current_class`, lines 126098-126104), she attends by being at the class's place in its block (`is_pc_at_class`, 126175-126181), and attendance is counted per course (`$classesattended`, 126249-126264). She attends by going; nothing makes her go. What skipping costs was not found, and isn't claimed. (Replaces an earlier unverified line, "Classes run at their times and can be skipped", in rule 7.)
    - Old rules 7–10 are now 8–11, and the one internal reference ("rule 7", now "rule 8") was updated; no other file cites systems.md rule numbers (checked with grep).
    - Rule 6's "where and when" now points at rule 7.
    - The worked example's café button says it's open whenever the café is open and the manager is there, not at a set hour.
    - **Checked against neighbours:** C1427 and rule 4 ("sized against the window") agree, because the window is the place's open hours. C1446 stays the note it was, and rule 7 cites it.
    - **`plan.md` §6:** one line, "Don't schedule activities around each other."
- `scripts/sheet.py`, `scripts/scenes.py`: a choice's own clock condition narrows the screens after it (ENI for LO, standing authorization, 2026-11-24).
  - **The failure:** P34. Rent sits inside Mark's Kitchen menu, which is open whenever he's there, but the choice "Pay the rent (5 min)" carries its own conditions (Sunday, 08:00–11:55). The sheet read only the trigger, so the rent screens said "while npc_mark is there" and missed the Sunday window. The writer copied that wider wording, which weakened the sheet.
  - **The fix:**
    - **The sheet:** along each path, the scene-start slots are narrowed by every choice's clock conditions (`choice_narrow`: `when_slots` of the choice's conditions, checked at the minute it's taken). A narrowed screen's clock is written from its slots (`fmt_slots`: "08:00–11:55 · Sun", or one part per day joined " / ").
    - **A screen reached by several choices:** the union of its paths. `clock_meaning` now reads " / " parts as a union of slots, except on the opening's exact clock, which is unchanged.
    - **Presence:** `scenes.check_presence` did not narrow by choices before. It now uses the same `sheet.node_starts` (the union over paths), intersected with the groups around the line as before.
  - **Tests:** three new: an all-week menu with a Sunday-only choice gives its screen a Sunday row; two choices with different days give the union; presence goes green on a Sunday-only line and red once the choice loses its condition.
  - **Verified read-only:** `mark_kitchen.rent` now reads "08:00–11:55 · Sun". The P11 and P34 card rows that say "while npc_mark is there" are now red, rightly; the game session updates them. Presence is green.
- `scripts/check.py`: the sheet and `Does:` checks skip a card none of whose screens exist in the build yet (ENI for LO, standing authorization, 2026-11-24).
  - **The failure:** under the overlap rule, cards for P08, P09, P33 and P35 were carded before being built, and the read-only check above showed 22 "is on the card's Sheet: but not built" reds and 22 matching `Does:` reds for them. A built piece with a missing screen still goes red: P10 kept its 5.
  - **Why not STATE.md's built date:** a first version skipped cards STATE lists as unbuilt. That would have skipped a new piece during its own build check, because STATE's built date is written when the piece closes. The rule is now: a card none of whose `Sheet:` or `Does:` screens exist is not judged, and a card with some built is judged in full.
  - **Tests:** an unbuilt card isn't judged; a partly built card is judged, and its missing screen is red on both checks.
- `scripts/reading.py`: a mostly rewritten canvas is asked once on `*` (ENI for LO, standing authorization, 2026-11-24).
  - **The failure:** P34's pass-1 fixes touched talk lines on 22 screens, so its next work list was 1,986 items: every rule asked once per changed screen, where pass 1 asked its 99 rules once on `*`.
  - **The fix:** per canvas, when more than half of its screens changed text, each row that fires on one of its changed screens is asked once on `*` ("most of <canvas> changed (n of m screens)"). The threshold is half because past it a per-screen list costs more than a first pass and finds nothing a `*` read wouldn't, while one or two changed screens are still asked per screen.
    - A FAIL from last pass is still asked on its own screen.
    - Fact-only changes are unchanged.
    - A card without `Does:` keeps the old behaviour.
    - `reader.md` says so.
  - **Tests:** three new on a ten-screen canvas: one changed screen still asks per screen; eight changed asks each row once on `*`; a FAIL on a changed screen stays on its screen with one change and with eight.
  - **Verified read-only against the live record:** P34's work list goes from 1,986 to 245 items. 137 are on `*`, 78 are on the screens of canvases under half changed, and 30 are FAILs on their screens.
- `scripts/reading.py`: disjoint batches of one pass all land, and no batch drops a FAIL (ENI for LO, standing authorization, 2026-11-24).
  - **The failure:** P34's reader split a pass into disjoint batches and recorded each as it landed. A later batch's verdicts were refused ("was not on the work list"), so the game session filtered batches to the live list, which can silently drop a verdict, a FAIL included.
  - **Why the list shrank (reproduced):** a `*` item answered on one screen in batch 1 counts as answered, so it leaves the live list, and batch 2's verdict for the same row on another screen was refused.
  - **Found while testing:** a FAIL recorded in an early batch was dropped by a later batch of the same pass. The later batch kept only verdicts of items it was carrying or hadn't been asked, and the FAIL showed as "failed last pass" on the live list.
  - **The fix:**
    - The first batch of a pass stores the work list as the pass began (`pass_items`), and every later batch is checked against it as well as the live list.
    - A FAIL owed to neither is recorded anyway, listed in `unowed` and printed ("kept a FAIL that was no longer on the work list"). An off-list PASS is still refused.
    - Each verdict is stamped with its pass. Verdicts an earlier batch of the same pass gave count as answered, so a FAIL from batch 1 isn't left pending in the same pass.
    - Every prior verdict on an item still on the live list is kept until a new verdict on the same item replaces it.
  - **Tests:** three disjoint batches recorded in three orders all land, a FAIL in any of them is kept, and the pass ends with nothing pending. A FAIL no longer owed is kept and reported, while an off-list PASS is still refused.
  - **Verified read-only:** the live records' work lists still compute.
- `craft/media.md` C1265 and rule 3, and `craft/people.md` C596, rule 7 and the menu example: where a person's picture goes (ENI's ruling for LO, standing authorization, 2026-11-24).
  - **The failure:** P34's two readers split on the same screens. One failed Mom's menu picture under C1265 ("a menu gets no spot"); the other passed it under C596 ("the talk screen … one picture"). As built and played in P42 (LO-approved), Mom's picture sits on her menu, right after her presence line, and her Talk screen has none (`games/first_term_lean/toml_phases/5_scenes.toml`, the `talk_mom` hub and talk nodes).
  - **The ruling:** a person's menu, opened from their face, is her screen with that person, and it gets that person's one picture after the presence line. The talk screen under it gets none unless it's a new moment. "A menu gets no spot" means room and system menus: a place's buttons, the wardrobe, a shop list.
  - **One home each:** C1265 says which menus get no spot and points to C596. C596 says where a person's one picture goes and points back to C1265. media rule 3, people rule 7 and the people menu example say the same in one line each.
  - **Verified:** the full suite runs green. Both rows' text changed, so `reading.py` re-asks them on pieces that carry them.
