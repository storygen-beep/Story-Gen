# SCENE — Delgado 3 · Review 1  `[REVIEW]` · PROPOSAL, for LO to place

| | |
|---|---|
| canvas | `delgado_03_review_1` · one-time |
| where · when | county office · Tue 14:00–16:00 |
| gate | `review_days` 30+ · `delgado_stage` 2 |
| who | Delgado |
| clip | a still: the form, two signatures |

| want | next step | hook |
|---|---|---|
| Delgado: to sign or refuse | the first rule comes off, or another month | pass: the bridge · fail: *"Thirty more."* |

## Screens

| # | screen | buttons |
|---|---|---|
| 1 | He reads thirty days of dots | *Listen* |
| 2 | Pass (record 60+) — or fail | *Sign it* |
| 3 | Pass: *"The bridge. Not past the line."* — Fail: *"Thirty more. Thursdays too."* | *Leave* |

## What it changes (op named)

- pass: flag `review_1_passed` **set** · trait `radius` **add** 30 · trait `review_days` **set** 0 · trait `delgado_stage` **set** 3
- fail: trait `review_days` **set** 0 · flag `thursday_checkin` **set** · stage stays 2, so it fires again after 30
