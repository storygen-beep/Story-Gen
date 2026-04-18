# Pathfinder dryrun — nlp-navigate-test

Trials: 5  |  Seed: 1  |  Median step latency: 0ms

## Summary

| Metric | Value |
|---|---|
| clean_completion_rate (of measurable) | 60.0% |
| clean_completion_rate (of total) | 60.0% |
| aborted_rate | 40.0% |
| divergence_rate | 0.0% |
| click_failed_rate | 0.0% |
| plan_failed_rate | 0.0% |
| plan_too_long_rate | 0.0% |
| snap_failed_rate | 0.0% |
| restore_mishap_rate | 0.0% |

## Per-strategy breakdown

| Strategy | Trials | Clean | Aborted | Diverged | ClickFailed | clean / measurable | clean / total |
|---|---|---|---|---|---|---|---|
| navigate | 5 | 3 | 2 | 0 | 0 | 60.0% | 60.0% |

## Abort reason breakdown (navigate)

- divergence_detected: 20.0%
- unknown_gate_blocked: 20.0%

## Divergence breakdown (fraction of total trials)

_No divergences recorded._

## Failure rate by plan depth

| Depth | Trials | Failure rate |
|---|---|---|
| 0 | 5 | 40.0% |

## Worst-offender source passages

_No divergent trials._
