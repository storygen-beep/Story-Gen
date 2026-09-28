# PERSON — Marty  `[REVIEW]`

**Role (prints under his name in every dialogue box):** `shop owner`
**Bible, one line:** Owns the hardware and pawn shop. Signs her hours. Wife works nights and he does
not go home. Careful, and getting less so.
**Home:** `offscreen` — across town, and never there. That is the character, not an omission.
**Meeting flag:** `met_marty` · opens **his hub only**
**Meter:** `trust` 0–100 · **6 rungs — the one arc that carries the game**
**Direction (A5b):** **THEIRS.** What is gated is *his* nerve, not hers. She asks; he is the one who
has to decide. Every counted refusal on this sheet is **his**.

---

## Schedule grid — place × hours × days

<pre>
                    Mon    Tue    Wed    Thu    Fri    Sat    Sun
  martys          08-19  08-19  08-19  08-19  08-19  08-19    —
  martys_back     19-20:30 ×6 (Mon-Sat)                       —
  the_diner           —      —      —      —      —      —  09-11
</pre>

**3 rows.** No hour is claimed twice. No row crosses midnight, so the weekday trap does not apply
here — `weekdays = [1]` at `23:00–06:00` puts a character on site Tuesday night and **deletes them
at midnight**, because `todayIndex` is Wednesday by then.

⚠️ **The 19:45 window every explicit rung below needs is inside `martys_back` 19:00–20:30, six days
a week.** Checked deliberately: the `night_desk` incident was a rung authored for four in the
morning with no sheet putting him at the desk at that hour. It was unreachable and no sheet could
see it.

---

## The ladder

| # | rung | canvas | where · when | HIS gate | HER gate | lands on a screen? |
|---|---|---|---|---|---|---|
| 1 | He signs the sheet without reading it | `marty_01_signs` | `martys` · any shift | `trust ≥ 5` | — | ✅ |
| 2 | Stay past close. *You learn his wife works nights.* | `marty_02_after` | `martys` · 18:00–19:00 | `trust ≥ 15` | — | ✅ |
| 3 | She asks him to sign hours she did not work | `marty_03_ask` | `martys_back` · 19:00–20:30 | `trust ≥ 30` | `sheet ≥ 1` | ✅ |
| 4 | The box at 8% and the outlet behind him | `marty_04_outlet` | `martys_back` · 19:45–20:30 | `trust ≥ 45` | `battery < 15` | ✅ |
| 5 | **first explicit rung** | `marty_05_back` | `martys_back` · 19:45–20:30 | `trust ≥ 60` | `battery < 15` · `arousal ≥ 20` | ✅ |
| 6 | **CONVERSION** — the back room becomes something she can simply do | `marty_06_nightly` | `martys_back` · 19:45–20:30 | `trust ≥ 80` | `battery < 15` | ✅ |

**Steps 1–2 have no sex in them and buy the two things A2 says an arc opens with: WHEN he is alone,
and WHAT he is vulnerable about.** The wife-works-nights line is not narrated — it is paid for with
three visits past close.

**What it grants, with the op named (S4):**

| rung | effect |
|---|---|
| 1 | `trait` `trust` **`add`** `+1`, `cap 15` — a rung feeds the meter it is gated on, only while she is under the next threshold |
| 3 | `trait` `vouch` **`add`** `+15`, `clamp true` · `trait` `sheet` **`set`** `2` · `trait` `clean` **`add`** `-4` ⚠️ **`add` with a negative, never `op = "sub"`** — `applyTraitEffect` runs `add` and `set` and returns on anything else (`v2.py:5749-5756`); nine canvases in one game shipped `sub` and did nothing |
| 5 | `trait` `arousal` **`set`** `0` (author-emitted at climax; no engine macro does this) |
| 6 | `trait` `vouch` **`add`** `+15` · `flag` `marty_converted` **`set`** |

---

## Refusals

| whose | where | shape | what the game says |
|---|---|---|---|
| **his**, rung 3 | `marty_03_ask` | **COUNTED** — three asks | ask 1 and 2 cost nothing. On the third the game names what closes: *the van, the ledger, and the hours after six.* A3's Zara case: the warning names the systems, not the fact |
| hers, rung 4 | `marty_04_outlet` | **PARKED** | *"He is back here every night but Sunday, from seven."* Free, reversible, and the game prints the place and the hour |
| hers, rung 5 | `marty_05_back` | **PARKED** | same address |
| mid-scene | `marty_05_back` | **STOP** — a different scene from refusing | 27–59 words, and the beat is about **his reaction**, not her exit. `commuter` is the one game in eleven that does this and nothing taught it |

⚠️ **A refusal ROUTES.** Marty's third refusal starts Rae's introduction two days later —
`rae_intro_pending`. Saying no hands the player a different person; it is not a dead end and not a
punishment.

---

## The repeatable, once rung 6 converts

**Surface:** `martys_back` · node-routed loop · **act menu 2 wide, span 1** (field median).
**Labels on the exits name the act** — a loop whose exits say *Continue* has thrown away the only
thing that makes the menu readable.

### BRAKE — S9, and it is on the TRIGGER

```
[canvases.trigger]
location            = "martys_back"
npc                 = "npc_marty"          ← the face, the presence gate AND the label all ride on this
schedules           = [ { start = "19:45", end = "20:30", weekdays = [0,1,2,3,4,5] } ]
max_triggers_per_day = 1
```

**A located canvas needs no day-cap flag** — `max_triggers_per_day` is read off the trigger
(`v2.py:11017`) and `markCanvasTriggered` stamps the day key *before* `advanceTime`
(`v2.py:4290`), so it is immune to the midnight trap that day-capped 78 rungs on choices and 40 on
exits across this repo.

⚠️ **`npc` goes at the top level of `[canvases.trigger]`, never on `[[canvases]]`.** A canvas-level
`npc` is dropped with no error and a green build (`template_import.py:906-913`), and three things
fail together: the face (`v2.py:5140`), the presence check that enforces his hours
(`v2.py:5176-5179`), and the label — the canvas's own `displayName` goes straight onto the player's
screen (`v2.py:5290`).

### Media
`pool_dir = "sex/martys_back_t5"`, `pool = 4`. **Never a single `file`** — a beat replayed fifty
times with one clip is dead on arrival.

### The aftermath — A10, and we have never built one
**23 of 23 `finish` nodes in this repo ship an empty `exit_block`.** His is 32 words and does three
things: **how he leaves · what she is left holding · the offer to stay or go.** His version is that
he goes and locks the front before he says anything, and the thing she is left holding is the key.

---

## Guidance
`card_marty`, behind `met_marty`. Goals carry `label` — a flag goal with none prints `marty_03_done`
to the player under 🎯 To advance.
