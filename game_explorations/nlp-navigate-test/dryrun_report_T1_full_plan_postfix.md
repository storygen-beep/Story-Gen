# Pathfinder dryrun — nlp-navigate-test

Trials: 30  |  Seed: 1  |  Median step latency: 538ms

## Summary

| Metric | Value |
|---|---|
| clean_completion_rate (of measurable) | 76.7% |
| clean_completion_rate (of total) | 76.7% |
| aborted_rate | 0.0% |
| divergence_rate | 3.3% |
| click_failed_rate | 20.0% |
| plan_failed_rate | 0.0% |
| plan_too_long_rate | 0.0% |
| snap_failed_rate | 0.0% |
| restore_mishap_rate | 0.0% |

## Per-strategy breakdown

| Strategy | Trials | Clean | Aborted | Diverged | ClickFailed | clean / measurable | clean / total |
|---|---|---|---|---|---|---|---|
| full_plan | 30 | 23 | 0 | 1 | 6 | 76.7% | 76.7% |

## Divergence breakdown (fraction of total trials)

- click_ineffective: 3.3%

## Failure rate by plan depth

| Depth | Trials | Failure rate |
|---|---|---|
| 0 | 12 | 0.0% |
| 1 | 11 | 9.1% |
| 2 | 7 | 85.7% |

## Worst-offender source passages

| Source passage | Divergences | Trials involving |
|---|---|---|
| `keepExplore` | 6 | 6 |
| `exploreIntro` | 1 | 1 |
