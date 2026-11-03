# [REVIEW] Scene — ryan_laura_opens_the_door

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign. Saturday 17:00–18:00 as built; want, next step and hook rows.

> **New 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–113). From `sheets/people/npc_ryan.md`, "Laura opens the
> door" (moved from Laura's ladder). Built canvas: `laura_04_ryans_door` (sheet marked moved); it stops setting
> `laura_step`.

| row | answer |
|---|---|
| person · step | `npc_ryan` · an event after step 4 (not a step) |
| where · when | the couch, `home_living_room` · Saturday 17:00–18:00, Ryan and Laura both home · once |
| gate | `ryan_step` gte 4 · Laura home · `laura_knows_ryan` false |
| who notices | Laura |
| what she risks | Mark hearing about it |
| what she wears here | not named; her bare feet |
| want | his hand round her ankle "like it lives there" |
| next step | Laura sees, and keeps it from Mark |
| hook | `laura_knows_ryan`: Laura knows, and she's keeping it |
| explicit? | no |

**As built:** it is its own canvas on the couch, not a hot repeatable: it opens on her feet already in his lap.

## Branch map — one row per screen

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op |
|---|---|---|---|---|
| `couch` | Laura comes in half dressed for her night out, on her feet in Ryan's lap; he doesn't move his hand fast enough | no | "Leave your feet where they are." → `laura` | none |
| `laura` | Laura: "Mark doesn't need to hear about this." She goes | no | "Okay, Mom." → the living room | `laura_knows_ryan` set |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the event, Laura's line, the flag | `proposals/RYAN_R1_LADDER.md` "Laura opens the door", signed by LO 2026-11-01 (DECISIONS 100, 105) |
| Laura's line | the built `laura_04_ryans_door` promise ("Mark doesn't need to hear about this.") |
