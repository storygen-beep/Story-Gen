# author-game exam

Scores an authoring skill (`author-game-v2`, later `author-game-v2-lean`) on small tasks drawn from
real logged mistakes. It lives outside every skill folder so a session under test cannot read the graders.

## How a trial works

1. **Stage.** A fresh temp directory gets:
   - `games/billable_hours` at commit `301f6f8` (see `fixture.json`)
   - the skill under test, plus `author-game-v2`
   - the `v2-*` agents
   - `scripts/merge_toml_phases.py`
   - the project `CLAUDE.md`

   The directory is a throwaway git repo, so every change is recorded.
2. **Run.** It runs `claude -p` with project settings only, no MCP and a budget cap. The skill is called by name, and the prompt says LO approved the step.
3. **Grade.** It merges, then runs `gates.py --json` on the merged TOML. A trial passes only if all three hold:
   - no gate that passed (or was n/a) in `baseline_gates.json` now fails;
   - the case's `target_lints` gain no new findings;
   - `cases/<id>/check.py` returns no failures. It checks that the work was done, plus any rule no gate covers.

Grading uses the difference from the baseline, never the exit code. The fixture already fails `location fill`, so `gates.py` exits 1 before any task.

## Commands (repo root)

```
venv/bin/python -m pytest .claude/skill-evals/author-game/tests -q        # checks: fail untouched, pass good, fail the logged mistake
venv/bin/python .claude/skill-evals/author-game/run.py --dry-run --case '03_*' --trials 1
venv/bin/python .claude/skill-evals/author-game/run.py --skill author-game-v2 --case '03_*' --trials 1
venv/bin/python .claude/skill-evals/author-game/run.py --skill author-game-v2 --trials 3   # full run: ask LO first, it costs money
```

Results go to `results/<timestamp>_<skill>/`. Each trial folder holds:
- the transcript
- the diff
- the gates JSON
- `grade.json` (cost, turns, whether the session ran the gates, which skills it called)

`summary.json` gives pass^k per case: a case counts only if every trial passed.

## Cases

Each `cases/<id>/case.json` names:
- the logged incident it came from (`source`)
- the rule involved
- the task prompt
- the lints that must stay clean

The fixture has no `ethan_02_done` flag, so case 07 uses `ethan_watched_shower`. Diane is in the kitchen at breakfast as well as in the evening, which is why case 11 needs an evening gate.

## Pinning

Every run stages `author-game-v2`, its agents, `CLAUDE.md` and the merge script from one commit (`--v2-ref`, default `HEAD`), and grades with that commit's `gates.py`. It re-measures the fixture baseline with those same tools at the start of the run (`results/<run>/baseline_gates.json`), so edits other sessions leave in the working tree cannot shift the score. The skill under test comes from the working tree unless `--skill-ref` pins it.

## Known limits

- **Context:** only the `story_gen_django` `CLAUDE.md` is staged. The two parent `CLAUDE.md` files a real session also loads are not.
- **Not a sandbox:** read access outside the staging dir is limited by permission prompts, which are answered "no" automatically in `-p` mode. That stops casual reads, not a determined one.
- **Some global skills still load:** `--setting-sources project` keeps user settings out, but the session still lists some globally installed skills (e.g. `deep-research`). Both arms see the same set.
- **Narrow grading:** cases grade the slip they came from. They do not grade prose quality beyond the explicit floor and the pivot.
