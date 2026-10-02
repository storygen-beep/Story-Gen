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
