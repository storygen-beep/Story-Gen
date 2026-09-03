# SCENE · Calloway — the walk-in  `[READY]`

`walkin_vance_securities` · **`substitution_only = true`** · target of `trigger.substitutions` on
`vance_securities`'s work row

⚠️ **Gate `the walk-in floor` reads this room** — she works alone in the stacks and he is scheduled.

| band | chance | what happens |
|---|---|---|
| `relation lt 20` | 0.10 | An auditor comes back for a box and Calloway talks too fast about why she is here. |
| `relation 20-34` | 0.30 | The auditor sees enough to guess and Calloway does not correct him. |
| `relation gte 35` | 0.55 | He tells the auditor to come back tomorrow without taking his hand off her. |

⚠️ **His walk-in threatens the BELIEF, not her body** — the thing he stands to lose is being taken
seriously, and every band is a step toward losing it. That is the walk-in written to the character
rather than to the mechanism.

⚠️ **The target MUST declare a `location`** (`v2.py:3177`).
