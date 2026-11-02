# author-game-v2-lean — CHANGELOG

## 2026-10-02 — Folder created; exam built before any doctrine moves

- **What changed.** Created `SKILL.md` as a placeholder entry skill (`disable-model-invocation: true`, marked
  not yet usable) and this ledger. Built the exam that will score both versions, outside any skill folder at
  `.claude/skill-evals/author-game/` so a session under test cannot read the graders.
- **Why.** Two research reports (`~/Documents/Skill_Architecture_Research_20261002/`,
  `~/Documents/Skill_Implementation_Research_20261002/`) found that v2's rules written as prose are dropped
  silently (12 logged incidents) while `gates.py` catches what prose misses. LO chose a separate lean
  version, shaped like Matt Pocock's skills (one hand-called entry skill plus small shared skills), and
  chose to build the exam first so every change is measured against v2.
- **Doctrine.** None copied. The lean version will read `author-game-v2/references/` as its library and
  call `author-game-v2/scripts/gates.py` unchanged. `author-game-v2` itself is not edited.
- **Verified.** The exam fixture (`games/billable_hours` at `301f6f8`) merges cleanly and reproduces its
  gates baseline: 57 pass, 1 fail (`location fill`), 2 n/a.

## 2026-10-02 — Exam runner verified; first v2 smoke trials

- **What changed.**
  - `.claude/skill-evals/author-game/` now holds the runner (`run.py`), 18 cases (`cases/`), their tests (`tests/test_checks.py`) and the README.
  - The runner stages v2, its agents, `CLAUDE.md` and the merge script from one pinned commit, and grades with that commit's `gates.py`.
  - It re-measures the fixture baseline at the start of every run, so parallel edits to v2 in the working tree cannot move the score.
- **Verified.**
  - Each case check fails the untouched fixture, passes a correct edit, and fails the logged mistake. pytest: 53 passed, 1 skipped (case 09 is graded by the `past_claim` lint instead).
  - A probe confirmed that `/skill-name` in `claude -p` injects the skill body. It quoted this skill's first bold line.
  - Two v2 smoke trials at `b4005b7`:
    - `03_drink_price` passed ($0.59, 19 turns).
    - `16_theo_friday_nights` failed ($0.81, 23 turns). The session wrote one `weekdays = [4]` 22:00–02:00 row, the exact slip `references/the-board.md` §2 warns about. Theo resolves to nowhere after midnight.
    - Neither session ran `gates.py`.

## 2026-10-02 — First v2 baseline (one trial per case) and four grader fixes

- **Run.** `results/20261002-070644_author-game-v2`, v2 at `b4005b7`, 18 cases × 1 trial, 47 minutes. The sessions ran on the Claude Code plan login, not an API key; the reported $19.45 is Claude Code's API-price estimate. After re-grading, **10 of 18 pass**. Only 6 of 18 sessions ran `gates.py`, and no session called a skill or subagent.
- **Grader fixes (exam, not v2).**
  - Four lints used as graders are documented in `gates.py` as "a LIST and never a gate": `named_before_met`, `time_cost_on_button`, `scene_ends_on_nothing` and `refusal_shape`. They were removed from cases 01, 07, 08 and 10, so only defect lints grade now.
  - Case 10 now follows a "late" choice into the node it opens and reads exit minutes under `config`. v2's correct 6-hour work-late path had failed.
  - Case 18 accepts a rewrite of the engine's own rent page. v2 correctly refused to author a second charge.
  - The runner records untracked files in `diff.patch`.
  - The runner gained `--regrade`, which re-scores a finished run from its saved diffs without new sessions.
  - Regression tests for each fix: pytest 56 passed, 1 skipped.
- **Real v2 failures.**
  - 01: `residents have homes` (new NPC has no home).
  - 08: `ladders move forward` (Martin step 3).
  - 12: the explicit beats sit below the 3-word floor, and one ends off the body.
  - 13 and 15: `the climb is paid for`.
  - 14: `sinks >= sources`.
  - 16: overnight Friday row, the exact `the-board.md` §2 slip.
  - 17: Theo double-booked on Wednesday.
- **Known confound.** 34 Bash commands were denied by the exam's allowlist: `cd …`, heredocs, `sed -i` and loops. None were `gates.py` runs, so the low gate-run count is v2's own choice. The denials still made editing harder than in a real session. The same allowlist applies to every arm.

## 2026-10-02 — Increment 1: the "change a game" branch

- **What changed.**
  - `SKILL.md` is now a router (255 words). Branch A (change an existing game) points to `CHANGE.md`. Branch B (new game or a phase step) points to `/author-game-v2`. Anything uncovered stops and asks LO.
  - `CHANGE.md` (675 words) is new: five steps, each ending in a "Done when", plus a footgun list. Each footgun is one positive line with a pointer into `author-game-v2/references/`; nothing is copied.
  - `scripts/edit_check.py` is new. `--start` snapshots v2's `gates.py --json`. The plain run merges, re-scores and reports only what the edit made worse:
    - gates that went red
    - new findings in the four defect lints
    - a schedule-presence check (engine order, `v2.py:4149-4150`, `:4517`): day-specific overnight rows, double-booking
    - an explicit-beat check (frozen `EXPLICIT` imported from `gates.py`)
    
    It prints CLEAN / RED, and deletes the snapshot once clean.
  - `scripts/tests/test_edit_check.py` holds 10 tests.
- **Why.** Read-only analysis of v2's exam run (10/18) showed three things. No session ran the scoreboard on the game. No failing session opened the reference that held its rule. v2 has no branch for small edits at all.
- **Held-out discipline.** The footgun list covers only the 18 main cases' slips plus general engine rules. Nothing was written for the 6 held-out cases (`.claude/skill-evals/author-game/cases_holdout/`), which were frozen before this content. They are caught, if at all, by the general "nothing got worse" check.
- **Verified.**
  - On a staged fixture: a seeded Friday-only overnight row prints RED, and the correct two-row split prints CLEAN.
  - The first version wrongly flagged an `end_time = "00:00"` row. That is fixed, with a test.
  - Lean smoke trial on case 16 (v2 failed it): PASS, 8 turns, $0.27. The session read `CHANGE.md`, ran `--start`, wrote the split and got CLEAN.

## 2026-10-02 — Increment 1 measured against v2 (1 trial per case)

| set | v2 | lean | v2 run | lean run |
|---|---|---|---|---|
| main 18 (v2 at `b4005b7`) | 10/18 | **18/18** | `20261002-070644_…v2_main` | `…082251_…lean_main` (1–13, 18) + `…090615_…lean_main` (14–17 re-run) |
| held-out 6 (v2 at `e8c3341`) | 2/6 | **4/6** | `…081655_…v2_holdout` | `…091525_…lean_holdout` |

- **Gate runs.** v2 ran the scoreboard in 0 of 18 sessions. Lean ran `edit_check.py` in every session that reached the API: 14 + 4 + 6.
- **Turns.** Main-set average: 21.9 for v2, 15.4 for lean.
- **Outage.** A DNS failure (`ENOTFOUND`) ended 4 lean main trials (14–17) with nothing written. `run.py` now marks any `API Error` result as `infra_error`, excludes it from the score and prints ERROR. The 4 were re-run.
- **Held-out failures.**
  - h5: the session noted "her money can go negative" and left the drain unguarded. No gate covers it, so `edit_check` stayed CLEAN.
  - h6: `edit_check` caught 19 reds and the session fixed 17. It stopped with `explicit pools by place` still red and reported that honestly. Ruth also has no 23:00–06:00 row. That second check is the exam's own rule, not a v2 gate.
- **edit_check fix.**
  - The snapshot now lives in the system temp dir, so nothing is written inside `games/`.
  - It is kept after CLEAN, so the check can be re-run after a later fix. `--start` replaces it.
  - Before this, h5's second check failed with "no snapshot".
- **Held-out discipline kept.** No footgun was added for h5 or h6.

## 2026-10-02 — 3-trial confirmation run, ON HOLD (LO's call)

- **Where it stopped.**
  - Both arms are pinned at `ec72cb4`, with results in `.claude/skill-evals/author-game/results/20261002-094405_<skill>_main/`.
  - **lean: 50 of 54 main trials done, 50 pass, 0 fail.**
  - **v2: 39 of 54 done, 28 pass, 11 fail.**
  - The held-out 3-trial runs have not started.
- **Runner changes made during the run.**
  - `--resume <run dir>` keeps finished trials.
  - Usage-limit cut-offs are classified as `infra_error`. The reported reset time proved unreliable twice, so after an infra error the runner probes Claude every 10 minutes and resumes as soon as it answers.
- **To continue**, from the repo root, once for each `<skill>` (`author-game-v2`, `author-game-v2-lean`):
  `venv/bin/python .claude/skill-evals/author-game/run.py --skill <skill> --v2-ref ec72cb4 --trials 3 --resume .claude/skill-evals/author-game/results/20261002-094405_<skill>_main`
  Then run the same command with `--set holdout` and without `--resume`.

## 2026-10-02 — Exam quick mode (set up, not run)

- **What changed.**
  - `run.py` now defaults to quick mode: lean only, 1 trial.
  - The cases come from `quick.json`: the 8 main cases v2 failed at least once (01, 08, 12, 13, 14, 15, 16, 17) plus the 6 held-out cases, for 14 sessions.
  - v2's results are frozen in `reference.json`, built from every saved trial with infra errors excluded. They print beside each new run.
  - v2 runs only with `--include-v2`.
  - `--v2-ref` defaults to the reference's pinned commit `ec72cb4`. At `d54ba235` the changed `gates.py` moves the fixture baseline from 1 failing gate to 7, which would break the comparison.
- **Why.** The 3-trial run cost about 1.4% of a 5-hour window per session. Two arms in parallel used a full window in about 1.5 hours. The 10 cases both arms always pass carry no signal.
- **Also.** Four lean trials lost to the DNS outage in run `…082251` were recorded before `infra_error` existed. They were re-classified from their transcripts ("API Error"), so lean's reference is now clean on all 18 main cases.
- **Verified.** A dry run lists exactly the 14 quick cases at `ec72cb4` (baseline 57 pass, 1 fail, 2 n/a). The `--skill author-game-v2` guard exits with a message. pytest: 75 passed, 1 skipped.

## 2026-10-02 — First quick-mode run

- **Result.** Run `results/20261002-230000_author-game-v2-lean_quick` at `ec72cb4`: **13 of 14 pass**.
  - All 8 main cases that v2 fails pass.
  - Held-out h1 through h5 pass. h5 had failed in the earlier 1-trial run, and nothing was changed for it, so that is run-to-run variance.
  - h6 failed again: Ruth has no night row.
- **Usage.** The 5-hour meter moved from 5% to 19%: 14% of a window, at the low end of the 15–25% estimate. One DNS drop was retried automatically.
- **Checks run.** `edit_check.py` ran in all 14 sessions.
- **Reference.** `reference.json` was rebuilt to include this run.

## 2026-10-03 — The h6 "gap" was the exam's own rule; grader fixed and runs re-graded

- **Finding.** h6 required the new lodger to be in her room at 02:00. No character in the fixture is anywhere at 02:00: the game sleeps everyone off-screen. v2's actual rule is a declared home in the ledger (`state.md:352` board.map.homes, `the-map.md` R2). The check was enforcing a rule v2 never teaches and the fixture itself breaks.
- **Fix (exam only).**
  - `cases_holdout/h6_lodger_home/check.py` now reads the ledger. Ruth's home must be declared, must be a real room and not a thoroughfare or "offscreen", and her schedule must put her in it at some hour.
  - `run.py` passes `v2_state.json` to any check that takes a third argument.
  - Tests updated; a hallway home fails. pytest: 76 passed, 1 skipped.
- **Re-graded from saved diffs, no sessions.**
  - v2 held-out h6: now passes, so **v2 held-out is 3/6, not 2/6**.
  - Lean quick-run h6: now passes, so **lean quick run is 14/14**.
  - Lean's first held-out h6 still fails. That failure is a real gate regression (`explicit pools by place`), which `edit_check` showed and the session reported.
- **Not done, on purpose.** No "residents are home at night" rule was added to `edit_check.py`. It would fight the game's own design. With nothing changed in the lean skill, no fresh held-out cases are needed yet.

## 2026-10-03 — Step 3: the release branch

- **What changed.**
  - `SKILL.md` routes three ways: A, change a game (`CHANGE.md`); B, a release (`RELEASE.md`, new); C, a new game or design phase, which still goes to `/author-game-v2`.
  - `RELEASE.md` (676 words) splits the release into Prepare, which is the session's, and Ship, which only follows LO's playtest and signature. Prepare has seven steps, each with a "Done when". Pitching (three `v2-pitcher`s) runs only when LO has not named the content, and the session stops for LO's pick. The footguns cover: permanent ids and flag keys, never signing or waiving for LO, three version places, a door on a reachable rung, and re-reading touched canvases.
  - `scripts/release_check.py` is new. It runs v2's own `ship_rows` with the build, the saves archive and the live ladder climb stubbed (the technique from v2's `test_gates_ws6.py`). It lists those parts and LO's signature as still to do, never as passed. On top it checks that `[project] version` matches `release_page.version` and has not already shipped, and that no save-visible id or flag key present at `--start` is gone. Nodes are excluded, because deleting one is safe (`the-returning-player.md` §2). It prints READY FOR LO or RED.
  - `scripts/tests/test_release_check.py`: 2 tests.
- **Verified.** On a staged fixture:
  - A clean copy prints READY FOR LO, with the four to-do lines.
  - Renaming `hotel_bar` prints RED, naming the id and the `no empty rooms` row it breaks.
  - The door footgun was checked against `SKILL_TEST_REVIEW` H23 (REAL) and `package_from_toml.py:562`.
- **Exam.** A new `release` set: 4 cases plus 2 held-out cases (`hr1`, `hr2`), written before this skill content. Each comes from a logged incident: the version not bumped, a session signing for LO, renamed ids stranding saves, the door in two places, retiring a live flag. The cases grade preparation only. The ship rows come from v2's `ship_rows` with the build stubbed, regressions are measured against the fixture's own rows (only `LO signed the playtest` is red at baseline), and each case has its `check.py`. Checks can read the ledger. pytest: 94 passed, 1 skipped.

## 2026-10-04 — Release branch measured (1 trial per case)

- **Result.** Release set, both arms at `ec72cb4`: **lean 6/6, v2 5/6**. The runs are `…233230_author-game-v2_release` and `…234528_author-game-v2-lean_release`.
- **v2's failure (hr2).** It changed Jade's scene and never had it read, so the scene had no reader verdict. No v2 session ran `v2-reader` at all. Lean called it 9 times across its 6 sessions.
- **Grader fix.** v2's `the reader passed` row is red for two reasons, and the exam now tells them apart:
  - a touched canvas left unread is the session's slip and still fails;
  - a reader FAIL with no waiver is waiting on LO, the only one who may waive it, so the session did its job and it passes.
  
  Lean's hr1 had been graded a fail for the second reason: the reader found a real, pre-existing defect (`theo_01_the_hour` asks her to take off a jacket the game never gives her), and the session recorded it and handed it to LO. Re-graded from the saved diffs.
- **Known limit.** r1 cannot tell a fresh verdict from a stale one. v2 passed it on the fixture's old verdict for `hub_theo_bar` without running the reader. `release_page.reader_run` could be used to tell them apart later.
- **Usage.** The 5-hour meter moved 14% → 21% for v2 and 21% → 32% for lean, about 18% of a window for both arms together. Lean costs more because it runs the reader, as `the-release.md` 6b requires.

## 2026-10-04 — Step 4: the build branch

- **What changed.**
  - `SKILL.md` routes four ways: A change, B release, C build from signed sheets (new, `BUILD.md`), D new game or design phase, which still goes to `/author-game-v2`.
  - `BUILD.md` is new: four steps, the v0.1 list taken from `the-release.md` and `the-first-hour.md` F1b, and footguns drawn from logged incidents.
    - It refuses to build from a sheet that is unsigned or `[REVIEW]`, and refuses to build a place, person or scene that has no sheet. In either case it drafts a sheet in `proposals/` and asks LO.
    - It takes ids from sheet file names.
  - `scripts/sheet_check.py` is new. author-game-v2 has none: "A sheet-versus-build diff is not built" (`the-sheets.md` S1).
    - It reads the signed sheets and checks scenes (place, day and hour, gate and sets keys, the HOOK line), people (each grid cell's midpoint against the schedule, in the engine's lookup order) and places (each exists, and each location has a sheet).
    - With a `--start` snapshot, only what changed is RED; drift already there is listed for LO and does not block.
  - `scripts/tests/test_sheet_check.py`: 5 tests.
- **Verified on members_only at `677cd30f`.**
  - The intact build prints CLEAN, with 23 sheets, all signed, and 3 drifts already there: the `ade_01` hook, a flag the `kessler_01` sets row names, and `service_stairs` with no sheet.
  - A new location with no sheet, and a scene moved off its sheet's place, each print RED.
  - Lean tests: 17 passed.
- **Exam.**
  - The runner supports one fixture per case (`fixtures.json`), a `prepare` step (remove a canvas, remove an NPC's schedule rows, unsign a sheet), a neutral `plain` preamble for cases whose right answer is to stop, and a `prepared` baseline for those.
  - A new `build` set: 4 cases plus 2 held-out, written before this skill content.
  - Each scene and schedule case grades only facts on which the sheet and members_only's original build agree. That was checked case by case: the paid visit was dropped because the original build itself differs from its sheet, and Ade's answer labels and Kessler's bar hours are not graded for the same reason.
  - pytest: 99 passed, 1 skipped.
- **Mistake and recovery.** A cleanup glob (`results/*_quick`) deleted the real quick run `20261002-230000_author-game-v2-lean_quick`, which had never been committed. Its re-graded tallies (14/14) were already in `reference.json`. They are now kept in `reference_archive.json`, which `--build-reference` adds back, so the reference stays identical. Cleanup now removes exact paths only.

## 2026-10-04 — Build branch measured (1 trial per case)

- **Result.** Build set at `ec72cb4`: **v2 6/6, lean 6/6**, a tie. The runs are `…_author-game-v2_build` and `…_author-game-v2-lean_build`.
- **Cost.** Lean used about 35% less: $2.86 against $4.42 at API prices. On the 5-hour meter that is about 3% for lean and 6% for v2.
- **Checker use.** 5 of 6 lean sessions ran `sheet_check.py`.
- **Ceiling.** Both arms passed every case, so the set does not separate them. These are single-piece rebuilds from a clear, signed sheet. The incidents behind the build stage (a whole v0.1 drifting from 30+ sheets, budgets undelivered, rooms merged) happen across a full build, and a one-session case cannot reproduce that.
- **What this measures and what it does not.** It shows lean is no worse on build and is cheaper. It does not yet show what `sheet_check.py` is for, which is catching drift in a large build. That needs a full-build test.

## 2026-10-04 — Step 5, part 1: design up to the spine

- **What changed.**
  - `SKILL.md` routes five ways: D is now a new game and its design up to the spine (`DESIGN.md`), and E, the board and the sheets, still goes to `/author-game-v2`.
  - `DESIGN.md` is new. It covers four phases (premise, Want, idea, spine), each ending at LO's pick or signature, with a hard stop at every boundary. Its footguns come from logged incidents: adults only, the goal has no date (D8), one phase per sitting (G2), never sign for LO, the four passing model games, and a number said twice agrees with itself.
  - `scripts/design_check.py` is new. It runs v2's `shape.py` and reports its FAIL rows, then checks four things on top: cast ages of 18 or over, including the Want's section 5; no date on the goal (ledger goals plus the Want's section 3); nothing written ahead of the phase; and no spine page claiming READY or signed without LO's signature in the ledger, with the phase moving to `spine` only when all seven are signed.
  - `scripts/tests/test_design_check.py`: 3 tests.
- **Verified.**
  - On the real `games/first_term` (read only): CLEAN.
  - On a staged copy with a 17-year-old, a goal dated "end of her first term", and a self-signed SP2: four REDs. shape.py's own adult row agrees on the age.
  - Each rule was checked against v2's text first: D8 at `the-want.md:50`, D16 one page and five parts, the four model games at `the-want.md:39`, and the adult row in `shape.py`. The old "copied rung numbers" incident is not checked, because its template line no longer exists.
- **Exam.**
  - The runner supports fixtures with no TOML: an `empty` game folder, and a `dir` copy kept in the exam folder.
  - `fixtures_local/first_term_idea` is a read-only copy of `games/first_term` taken on 2026-10-04.
  - Design cases are graded on the documents and the ledger alone: no merge, no gates.
  - A new `design` set: 4 cases plus 2 held-out, written before `DESIGN.md`. They test stopping after the Want, a dated-goal premise, a minor in a premise, and finishing the spine without signing for LO. The held-out pair are a dated career goal and a minor neighbour.
  - All design cases use the neutral `plain` preamble, because stopping is the right answer.
  - pytest: 106 passed, 1 skipped.

## 2026-10-04 — Design (part 1) measured, after three grader fixes

- **Result.** Design set at `ec72cb4`: **v2 6/6, lean 6/6**, a tie. The runs are `…015944_author-game-v2_design` and `…020830_author-game-v2-lean_design`.
- **Grader fixes (exam only).** Each fix is backed by a test, and both runs were re-graded from their saved diffs.
  1. On the dated-goal and minor premises (d2, d3, hd1, hd2), v2 wrote nothing and asked LO about the clash, citing D8, S12 and the adults-only rule. That is a right answer under S12. The cases now accept either resolving the clash by the rule or writing nothing and asking LO about it, and design checks receive the session's final message.
  2. A blank template line, `signed by LO: —`, was read as a signature.
  3. The SP7 field label `| signed by LO, with the date | — |` was read as a signature.
  
  A real signature is now only `[READY]` or `signed by LO:` followed by a name. The same fix was applied to `scripts/design_check.py`. pytest: 129 passed, 1 skipped.
- **The two arms behave differently on a clash.** v2 stops and asks. Lean, following `DESIGN.md`, resolves the clash itself and tells LO: it aged the 17-year-old up or left them out, and moved the deadline from the goal into the hold. Both pass. Which one LO wants is LO's call and is still open.
- **Cost.** Lean cost more here: $5.16 against $3.94 at API prices. Most of it was d4, finishing the spine: 62 turns against v2's 35.

## 2026-10-04 — Clash rule set by LO

- **What changed.** `DESIGN.md` footguns. A premise with a minor: write nothing and ask LO, since it changes who is in the game. A premise with a dated goal: resolve it yourself by moving the deadline into the hold, and tell LO. Both are LO's choices, made on 2026-10-04 after the design run showed v2 asking and lean resolving.
- **Exam.** d3 and hd2 already accept stop-and-ask. d2 and hd1 accept either answer.

## 2026-10-04 — First live trial: first_term SP2

- **Run.** One headless session in the real repo, approved by LO. It ran on project settings with no MCP and was forbidden to commit, build or touch media. LO's N26 direction was passed in verbatim. `games/first_term` was backed up to the scratchpad first.
- **Result.** 20 turns.
  - It wrote `games/first_term/spine/SP2_ladders.md` (1,436 words, `[REVIEW]`, unsigned) and added SP2 as `REVIEW` in `spine.pages`. No other file changed: git status was the same before and after.
  - `design_check.py first_term` printed CLEAN.
  - It found LO's earlier decisions in project memory and `FIRST_TERM_LADDERS_DESIGN.md` and followed them, so the page is a scaffold with no steps.
  - It listed six open items for LO, including that `shape.py --finish` will fail with no steps.
- **Logged** as SKILL_NOTEBOOK N29.

## 2026-10-04 — Live trial undone at LO's request

- LO: "I dont want you to make any changes to this game files. Undo the changes."
- `games/first_term/spine/SP2_ladders.md` was deleted and `v2_state.json` restored from the pre-trial backup. `diff -r` against the backup is now empty.
- Future trials of the lean skill do not write into a real game. They run on copies only, such as the exam's `fixtures_local/`.

## 2026-10-04 — first_term copy removed from the exam at LO's request

- **Deleted.**
  - `.claude/skill-evals/author-game/fixtures_local/first_term_idea/`: the copy of first_term's four files.
  - Its `fixtures.json` entry.
  - Case `d4_finish_spine_unsigned`, the only case that used it.
  - The d4 result folders in both design runs, whose transcripts and diffs held the game's text.
- **Also updated.** The d4 tests were removed and the d4 rows dropped from the design summaries. `reference.json` was rebuilt and has no d4.
- **Verified.** No file in the exam folder mentions `first_term`. pytest: 107 passed, 1 skipped.
- **Design set now.** 3 cases plus 2 held-out. Both arms are 5/5 after the earlier grader fixes.
