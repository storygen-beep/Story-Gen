# [READY] Scene — ryan_laura_opens_the_door

> **New 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–113). From `sheets/people/npc_ryan.md`, "Laura opens the
> door" (moved from Laura's ladder). Built canvas: `laura_04_ryans_door` (sheet marked moved); it stops setting
> `laura_step`.

| row | answer |
|---|---|
| person · step | `npc_ryan` · an event after step 4 (not a step) |
| where · when | the couch, `home_living_room` · Sat, Sun 14:00–18:00 · the first time the "feet in his lap" repeatable plays with Laura home · once |
| gate | `ryan_step` gte 4 · Laura home · `laura_knows_ryan` false |
| who notices | Laura |
| what she risks | Mark hearing about it |
| what she wears here | not named; her bare feet |
| explicit? | no |

**Engine note:** Laura's rule hides the hot repeatables in a room she is in. This event is the one exception: it fires
as she walks **in** on them, then her rule applies again.

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `couch` | Laura comes into the living room on Ella's feet in Ryan's lap; Ella doesn't move them | no | "Leave your feet where they are." → `laura` | none |
| `laura` | Laura: "Mark doesn't need to hear about this." She goes | no | "Okay, Mom." → the living room | `laura_knows_ryan` set |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the event, Laura's line, the flag | `proposals/RYAN_R1_LADDER.md` "Laura opens the door", signed by LO 2026-11-01 (DECISIONS 100, 105) |
| Laura's line | the built `laura_04_ryans_door` promise ("Mark doesn't need to hear about this.") |
