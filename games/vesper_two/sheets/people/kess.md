# PERSON · Kess  `[READY]`

| | |
|---|---|
| **id** | `npc_kess` |
| **role** | `synth mechanic` |
| **home** | `kess_berth` |
| **meter** | `relation` — how interesting the problem has got |
| **rungs** | 3 (`0 · 10 · 25`) |
| **why her** | He reads bodies as hardware and hers as an interesting problem. |

## ⚠️ This is a NON-SEDUCTION arc, and it is the game's spine

**He is the only source of `seated`**, the game's one sourced system, and his ladder is the staged
repair: `seated` 0 → 5. No sex at any rung. His `crude_ceiling` is *"the seam: hands inside her,
parts seated, what she does while he works"* — written as explicitly as any act in the game, and it
is not an act.

He is also her **landlord**: the feed line is 10 coin a night on his terms, and a paid night buys
her charge and a few days of his attention.

## Schedule grid

| location | days | from | to | activity |
|---|---|---|---|---|
| `kess_berth` | Mon-Sun | 10:00 | 22:00 | at the bench, stripping something decommissioned |

## The arc

**6 steps · first 2 carry no sex** — and so do the other four. This arc is 100% sex-free by
construction, which is the point of it.

| step | name | canvas | place | from | to | gate | sets | sex |
|---|---|---|---|---|---|---|---|---|
| 1 | He nearly throws you out | `arc_kess_01` | `kess_berth` | 10:00 | 22:00 | — | `kess_met` | no |
| 2 | The rate | `arc_kess_02` | `kess_berth` | 10:00 | 22:00 | `kess_met` · `coin gte 10` | `kess_tenant` | no |
| 3 | The first seat | `arc_kess_03` | `kess_berth` | 10:00 | 22:00 | `kess_tenant` · `relation gte 10` | `seated_1` | no |
| 4 | It comes back wrong | `arc_kess_04` | `kess_berth` | 10:00 | 22:00 | `seated_1` | `kess_failure` | no |
| 5 | He reads what came back | `arc_kess_05` | `kess_berth` | 10:00 | 22:00 | `kess_failure` · `relation gte 25` | `seated_3` | no |
| 6 | **CONVERSION** | `arc_kess_06` | `kess_berth` | 10:00 | 22:00 | `seated_3` | `kess_open` | no |

⚠️ **Step 4 takes `seated` back DOWN**, and it is the only step in the game that moves a number
backwards. A staged repair that never fails is a shop counter.

⚠️ **Step 2 arms the obligation.** Until `kess_tenant` is set the feed line does not exist, which is
`the-economy.md` R3's *"armed after income exists"* — pressure before she has a way to earn is a
scripted loss, not a choice.

## What step 6 converts into

The bench as a standing surface: `seated` 3 → 5 repeatable, and the nightly rate **rises with it**
(R3b — the obligation moves, and it moves on this system rather than on a second mechanic).

Media: **none of his own, and none needed.** `videos/portraits/wren_*.jpg` — the 8 undress states —
are read here, because this is the room where she is opened up on a bench.

## The refusal (A3)

Counted `kess_refusals` · warned at 2 (*"he will keep taking the rent and stop touching the rest"*)
· at 3 sets `kess_closed`, which **freezes `seated` for the rest of the game** — the single most
expensive door in v0.1, and the warning names all four things it costs.

## Aftermath and the other two exits

| exit | canvas | ~words | about |
|---|---|---|---|
| aftermath | `post_kess` | 33 | he is already looking at the next thing on the bench |
| stopping | `stop_kess` | 29 | he stops immediately and asks a technical question, which is worse |
| chickening out | `chicken_kess` | 24 | the part is out on the cloth and he does not put it away |

## The meeting

**F5 · his hub does not exist until this has fired. F8 · one flag, and it opens ONE hub.**

| canvas | place | days | from | to | flag | words | speaks |
|---|---|---|---|---|---|---|---|
| `meet_kess` | `kess_berth` | Mon-Sun | 10:00 | 22:00 | `met_kess` | 120 | yes |

He does not look up. He tells her the rate before he tells her anything else, and the rate is the first number in the game.

⚠️ **The window matches his own schedule row exactly.** A one-shot naming a character needs
`trigger.schedules` covering that character's hours — **`requires_npc` does not gate the auto-fire
path** (`v2.py:4559`), so without it the introduction plays to an empty room. **Vesper scored 0 of
18 on this.**

⚠️ **Role before name** (F7). The game says what he *is* before it says who he is; the label is what
the player can hold and the name is what they will need later. The measured failure inverts it —
*"It goes to Ewan"* — and never says who Ewan is.

`[INTENT]` 120 words. Field: median **101**, quartiles 57 / 101 / 194, **66% under 150** and
**64% carrying spoken dialogue**. This one speaks.

## Quest card (S10)

`The berth` — a place and an hour.
