# SCENE · Marsh — the walk-in  `[READY]`

`walkin_underworld_brothel` · **`substitution_only = true`** · target of `trigger.substitutions` on
the House's booked-hour row

⚠️ **Gate `the walk-in floor` reads this room** — she works alone in it and Marsh is scheduled.

| band | chance | what happens |
|---|---|---|
| `service lt 20` | 0.15 | The woman whose slot she bought is in the corridor when she comes out. |
| `service gte 20, lt 45` | 0.35 | A second client is shown to the door early and told to wait where he can hear. |
| `service gte 45` | 0.60 | The hour is sold twice and nobody asks her first. |

⚠️ **The low band is the cut character paying off.** Rue is not in the cast, but the woman whose
Sunday was bought still exists in the fiction and this is where she is felt. A cut character can
leave a shadow without needing a `[[npcs]]` block.

⚠️ **The target MUST declare a `location`** (`v2.py:3177`).
