# PERSON · Halloran  `[READY]`

| | |
|---|---|
| **id** | `npc_halloran` · **fixed name** |
| **role** | the man who teaches the eight o'clock — **role before name** |
| **home** | **`offscreen`** |
| **meters** | `relation` only — light |
| **met** | `the_quad`, **Mon 08:00–09:30** · flag `met_halloran` |

**Why he is wanted:** the one man whose approval is worth something on paper, and the only one who
can hand her a key.

**What he owns:** grades, the department, office hours.

⚠️ **`offscreen` is DECLARED, not left blank.** Faculty, lives across town, has no bed in this world.
Only a declaration separates *lives elsewhere* from *was never given a room* — gate 12 accepts the
literal string and refuses a guess. The measured failure counted four doors in a landing description
while three of its four men slept nowhere at all.

---

## The schedule grid

| # | location | start | end | weekdays | activity |
|---|---|---|---|---|---|
| 1 | `the_quad` | 08:00 | 09:30 | `[0,2,4]` Mon · Wed · Fri | the eight o'clock |
| 2 | `halloran_office` | 16:00 | 18:00 | `[0,2,4]` Mon · Wed · Fri | office hours, and the floor empties at five |

⚠️ **No overnight row, so no split.** Both windows are inside one day.

⚠️ **The meeting canvas carries `trigger.schedules` matching row 1 exactly.** `requires_npc` does
**not** gate the auto-fire path, so a meeting without a matching window plays to an empty room — gate
*a meeting fires where they are* checks this. **This is why the funnel hands over on a Monday**: the
eight o'clock does not run on Tuesday, and a first day of college with no class is a design that
reads as a bug.

⚠️ **The last hour of office hours is the only hour anyone is up there.** That is not written in the
prose as atmosphere; it is a consequence of row 2 ending at 18:00 and the department emptying at 17:00.

---

## Ladder — 3 rungs, CONVERTED, no arc

**Arc debt, owed at 0.3.**

| rung | gate |
|---|---|
| the reader's key | `met_halloran` · **`past_top` reaches this in week one** |
| the late lab — needs the kit bought at `the_quad` | relation 15 · `item:lab_kit` |
| after the floor empties | relation 30 · `appetite` 30 |

⚠️ **Rung 2 is A4b's third key kind — a preparation BOUGHT.** Money buys the key to a rung, never a
meter point. A shop that sells an arc's prerequisite is doing more work than a shop that sells a
stat.

⚠️ **`past_top` is additive.** The original rung keeps its numbers and gains `past_top is_false`, and
the two are separated from the `relation` band by a non-`group` block.

## Walk-in
`walkin_latelab` — **required**, `max_triggers_per_day = 1` on the trigger. Located, so it needs no
flag: `markCanvasTriggered` stamps the day key before `advanceTime` (`v2.py:4290`).

## Crude ceiling

| tier 1 | tier 2 | tier 3 |
|---|---|---|
| hard · his cock · the word *cunt*, and it is his word | cock in her mouth · throat · cum | full |
