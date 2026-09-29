# SP3 · Dependencies — Probation

> [READY] · drafted 2026-09-29 · signed by LO: 2026-09-29 (day-after rule waived by LO for the skill test)
> A decision record, ≤ 400 words. The rules: `references/the-spine.md` SP3.

| step | needs | why |
|---|---|---|
| npc_tobin step 1 | npc_delgado step 1 | the intake is where the box goes on; no box, no check |
| npc_marty step 1 | npc_delgado step 1 | the job is one of her terms, read out at intake |
| npc_marty step 3 | window: Thu 19:00–21:00 | stocktake is Thursday night, past curfew, on the letter |
| npc_rae step 1 | place open: the_laundry | the laundry is open all night; the step needs it lit and Rae in it |
| npc_tobin step 4 | npc_delgado step 3 | Tobin won't fake a whole night until he has seen a passed review |

Record it in `dependencies[]`: 5 rows, and `shape.py` finds no cycle.

**Read, not depended on.** Delgado step 2 reads what happened at Tobin step 1, two hours earlier the
same Tuesday (`tobin_fault_1` or `yards_on_file`). It fires either way, so it is not a dependency.
Written as one, a player who skipped Tuesday morning would stall.
