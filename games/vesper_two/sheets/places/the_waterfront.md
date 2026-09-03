# PLACE · The Waterfront  `[READY]`

| | |
|---|---|
| **id** | `the_waterfront` |
| **ENTERED FROM** | `the_street` |
| **WAYS OUT** | `renner_depot` · back to `the_street` |
| **DOOR** | no |
| **LABELS** | `outdoors` · `public` · `zone:waterfront` |
| **fill** | 800 `[INTENT]` |
| **heat** | cold |

## What this place is FOR

The dock road: the Spire behind, the Reach below. It exists so the depot is somewhere rather than a
tile, and so crossing between zones costs an hour of daylight against Renner's 09:00–18:00 window.
That time cost is what makes his schedule bite.

## The list

| # | row | canvas | kind | system | gate | effect | screen |
|---|---|---|---|---|---|---|---|
| 1 | "Into the depot." | `TBD` | exit | — | — | `time` `add` `+10` | yes |
| 2 | "Back to the street." | `TBD` | exit | — | — | `time` `add` `+20` | yes |

⚠️ **The time cost is not on the button, and that is a known lint.** The engine tags TRAVEL time on
a nav card for us (`v2.py:4724`) but tags ACTIVITY time nowhere (`v2.py:12733`). Vesper had **38
buttons burning an hour or more in silence**. These are travel, so the engine labels them.
