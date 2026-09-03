# SYSTEM · clean — what is on her, and who will look at it  `[READY]`

| | |
|---|---|
| **kind** | `ambient` |
| **key** | `clean` (0–100) — **a declared need** |
| **fed at** | `underworld_bar_bathroom` (free) · `kess_berth` (a paid night covers it) |
| **labels** | `she_can_undress` |
| **mechanism** (S8) | `[player.core_traits] clean` + `[player.trait_decay]`. Not rotation. |

| need field | value |
|---|---|
| `falls` | 30 per finish, 10 a day |
| `fills` | `underworld_bar_bathroom` · Wash · 20 min · free |
| `costs` | free at the bathroom; a berth night covers it |
| `shuts` | under 40 the `checks_cover` doors refuse her and the bar floor pays half |

## READERS — written first

| # | reader | where | what changes |
|---|---|---|---|
| 1 | the three cover doors | `spire_plaza` · `vance_securities` · `penthouse` | refused, with a sentence (SY5) — never a greyed label |
| 2 | what the floor pays | `underworld_bar` | half |
| 3 | what Mercer says | `penthouse` · `mercer_room` | he is fond of the tool and notices its condition |
| 4 | what Bastien finds at the door | `bastien_backroom` | he strips her; this is on her |
| 5 | the mirror line | `underworld_bar_bathroom` | the room's own reason to exist |
| 6 | ambient outdoors | `the_street` · `underworld_strip` | who looks twice |

**6 readers against 2 fill points.** This is the system that couples the act surfaces back into the
ascent: every finish takes it down, and the cover doors are what notice.

## WRITERS

every finish rung `-30` · decay `-10/day` · wash `op = "set"` · `100`

⚠️ **Write-heavy by construction** — every finish writes it. SY1's exception covers this (*"an
earned resource legitimately runs write-heavy"*), but the readers above are what keep it from being
a scoreboard. If the reader list ever gets shorter than this, the system is the defect.
