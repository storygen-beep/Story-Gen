# Pathfinder dryrun — road-to-success

Trials: 30  |  Seed: 1  |  Median step latency: 933ms

## Summary

| Metric | Value |
|---|---|
| clean_completion_rate (of measurable) | 50.0% |
| clean_completion_rate (of total) | 50.0% |
| aborted_rate | 0.0% |
| divergence_rate | 20.0% |
| click_failed_rate | 30.0% |
| plan_failed_rate | 0.0% |
| plan_too_long_rate | 0.0% |
| snap_failed_rate | 0.0% |
| restore_mishap_rate | 0.0% |

## Per-strategy breakdown

| Strategy | Trials | Clean | Aborted | Diverged | ClickFailed | clean / measurable | clean / total |
|---|---|---|---|---|---|---|---|
| full_plan | 30 | 15 | 0 | 6 | 9 | 50.0% | 50.0% |

## Divergence breakdown (fraction of total trials)

- dynamic_goto: 20.0%

## Failure rate by plan depth

| Depth | Trials | Failure rate |
|---|---|---|
| 1 | 26 | 42.3% |
| 2 | 4 | 100.0% |

## Worst-offender source passages

| Source passage | Divergences | Trials involving |
|---|---|---|
| `Bedroom` | 11 | 11 |
| `OldSaveImport` | 4 | 4 |
