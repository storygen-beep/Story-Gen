# Pathfinder dryrun — nlp-navigate-test

Trials: 30  |  Seed: 1  |  Median step latency: 479ms

## Summary

| Metric | Value |
|---|---|
| clean_completion_rate (of measurable) | 80.0% |
| clean_completion_rate (of total) | 80.0% |
| aborted_rate | 0.0% |
| divergence_rate | 0.0% |
| click_failed_rate | 20.0% |
| plan_failed_rate | 0.0% |
| plan_too_long_rate | 0.0% |
| snap_failed_rate | 0.0% |
| restore_mishap_rate | 0.0% |

## Per-strategy breakdown

| Strategy | Trials | Clean | Aborted | Diverged | ClickFailed | clean / measurable | clean / total |
|---|---|---|---|---|---|---|---|
| full_plan | 30 | 24 | 0 | 0 | 6 | 80.0% | 80.0% |

## Divergence breakdown (fraction of total trials)

_No divergences recorded._

## Failure rate by plan depth

| Depth | Trials | Failure rate |
|---|---|---|
| 0 | 12 | 0.0% |
| 1 | 11 | 0.0% |
| 2 | 7 | 85.7% |

## Worst-offender source passages

| Source passage | Divergences | Trials involving |
|---|---|---|
| `keepExplore` | 6 | 6 |
