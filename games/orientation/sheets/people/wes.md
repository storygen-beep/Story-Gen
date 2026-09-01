# PERSON · @wes  `[READY]`

| | |
|---|---|
| **id** | `npc_wes` · renameable, so **prose uses `@wes`** |
| **role** | her step-brother, 20, a junior at the same college |
| **home** | `wes_room` |
| **meters** | `relation` only — light, per W6, because he ships converted in v0.1 |
| **met** | funnel screen 4 · flag `met_wes` · **he asks the start-choice question** |
| **`relationship_options`** | stepbrother · half-brother · brother · cousin → `@wes.rel` |

**Why he is wanted:** he was already inside every room she is trying to get into, and he is the only
person who sees both halves of her life.

**What he owns:** the ride, the bathroom, the campus he already knows.

---

## The schedule grid

| # | location | start | end | weekdays | activity |
|---|---|---|---|---|---|
| 1 | `the_bathroom` | 06:40 | 07:10 | — every day | in there with the door not quite shut |
| 2 | `the_avenue` | 07:15 | 07:50 | `[0,1,2,3,4]` Mon–Fri | car running, not waiting long |
| 3 | `wes_room` | 19:00 | 23:00 | — every day | door open |

⚠️ **Rows 1 and 2 do not overlap, and an earlier draft of this grid had them overlapping by thirty
minutes.** That is the S5 incident exactly — two sheets each correct about one room, with nothing in
the format reading across them. The person sheet is the only artifact that can see it.

⚠️ **Row 2 is what the funnel hands over into.** The opening ends at **07:20 on `the_avenue`**, and
he is there. Gate *the opening opens a door* checks that the last click of the funnel lands on a
clock time when something at that location is actually open.

⚠️ **Row 1 is reachable only if she is up before seven**, which `rest` decides. The walk-in has a
real cost attached to it before it has a gate.

---

## Ladder — 3 rungs, CONVERTED, no arc

**Arc debt, owed at 0.2.** Logged in `v2_state.decisions`, per `the-arc.md`'s closing rule: name
which of A1–A12 a release built and which it skipped, with the reason. The reason here is scope —
two arcs in v0.1, and his is not one of them.

| rung | gate |
|---|---|
| the bathroom, and whether she uses the bolt | `met_wes` |
| the ride, and what he asks for it | relation 15 |
| his room, door open | relation 30 · `nerve` 30 |

## Walk-in
`walkin_bath_wes` — **required**, and its two exits are two beats, not one beat with a modifier:
**cover** (her body decided) and **do not cover** (she decided). Everything downstream differs.

## Crude ceiling

| tier 1 | tier 2 | tier 3 |
|---|---|---|
| tits · ass · dick · hard | cock · cunt · fingers in her · fuck | full — cum, throat, ass |
