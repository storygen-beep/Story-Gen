# [REVIEW] Scene — jake_03_my_boyfriend

> Changed 2026-11-03 to match the build (third alignment pass); waits for LO's re-sign.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Continue")** (DECISIONS 99–119): Jake's release-1 ladder (`sheets/people/npc_jake.md`, signed). **Merged** with built Jake 4 = Laura 5 (`laura_05_jake_at_the_door`, sheet marked moved): one step, one night. Changed: Laura in the dark living room, seen on `ryan`; her "Was he any good?" moves to `after`; her voice row. The signed screens stand; two lines are added, below.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

> Placed in sheets/ 2026-10-08. Written 2026-10-08. **Jake's voice sample, in full:** every screen written by
> `v2-prose` from a spec, measured with `gates.py --beat`, pasted here. LO picked this step.

| row | answer |
|---|---|
| person · step | `npc_jake` · 3 (Jake B 3) |
| where · when | the front door · Saturday 23:00–00:00, after a booked date (pass 4 reader: `after` is 11 minutes in, so past midnight Laura is read where her row has her: the couch, the bench in the hall, or asleep with her door shut, and she speaks only while she is up) |
| gate | his step 2 · Corruption 20 · Exhibitionism 20 · a date tonight · Laura in the living room · the boost off |
| want | "Saturday. Pick me up at the door." (B 2); "Is anyone up?" |
| next step | she names him to the house: Ryan |
| hook | Ryan's light goes out; "Next Saturday?" (his thread) |
| what she wears here | not named |
| explicit? | no: a kiss on the porch rail (stage 2) |
| who notices | **Ryan, Laura** (in the dark living room, Saturday 22:00–00:00, her waiting-up row) |
| what she risks | the house knowing |
| her_line_low · her_line_high | low: "He's normal. This is normal." · high: "You want Ryan to hear every second of it." (the person sheet's pair) | The built thought on `ryan` ("Good. Look all you want, Ryan.") is the high side. |
| what changes after | Jake is her boyfriend (`jake_step` 3); Laura: "Was he any good?"; Ryan's line changes (built, "Who's Jake?") |
| the crude-word ceiling | Jake's early column: ass · Ryan's early: ass, tits (LO, 2026-10-08) |

## The step row (as built, 2026-11-03)

The seven columns, filled from what the build does.

**Kind · stage:** a kiss at home, where her brother sees · Curious · Daring (20)

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| she kisses him at the front door; Ryan opens it on them | Ryan at the door; Laura in the living room | the house knowing | "Kiss him.", then "Don't stop." | "I want them to see you're mine." | yes | his step 3; "My boyfriend."; Ryan's Warmth -15, Want +5 |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`jake_03_my_boyfriend`** — Front Door · Sat 23:00-00:00 · Jake there · needs Jake's step = 2 · Corruption 20+ · Exhibitionism 20+ · drinks boost off · under 6h since `jake_date_went` · Laura in Living Room · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `porch` | Jake walks you up to the porch and stops under the light. | no | "Kiss him." → `rail` | — |
| | | | "Goodnight, Jake." → `no` | — |
| `rail` | You kiss him first, right there under the porch light. | no | "Don't stop." → `ryan` | Ryan's Warmth -15 · Ryan's Want +5 |
| `ryan` | The front door opens behind Jake. | no | "Goodnight, Jake." → `after` | — |
| `after` | Jake goes off down the path, whistling. | no | "Go to bed." → Your Room | Jake's step = 3 · `jake_03_done` set · `jake_date_booked` cleared · `late_date` set · `came_home_late` set |
| `no` | You kiss his cheek, quick, and step back before he can turn it into more. | no | "Go in." → Hall | `jake_date_booked` cleared · `late_date` set · `came_home_late` set · back in 7 days |

## Lines added by the merge (mine, except where marked)

> Drafted before the build and kept as the signed record. Where it differs, the branch map and the beats above say what the build does.

- **`ryan`, after "The door slams hard.":** "Behind Jake's shoulder, in the dark living-room window, a shape on the couch hasn't moved." (from `laura_05`'s porch line, built)
- **`after`:** the built first sentences become "Jake goes off down the path, whistling. You let yourself in." · then "The living room is dark. Laura is on the couch with her knees pulled up and her hand at her throat, and she doesn't pretend she wasn't watching." (built, `laura_05` `couch`) · Laura: "Was he any good?" · in the blue dress, "Better in your dress." · otherwise, "Better with you watching." (both built) · "She makes a sound in her throat. She doesn't get up." (built) · then the built rest from "You go down the hall." and "Ryan's door is shut, and his light is on under it."
- **Truth:** the porch screen's "Nobody. Not yet." stays her line; she hasn't seen Laura in the dark. The window line comes after Ryan, when she looks back.

## Truth checks

> Drafted before the build and kept as the signed record. Where it differs, the branch map and the beats above say what the build does.

| line | what backs it |
|---|---|
| Ryan's window lit; he opens the door | his night row: his room from 22:00 every night |
| "Next Saturday?" | his thread books the next date (the Saturday date repeat) |
| no garment of hers is named | nothing needs backing |

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Jake B 3 (fixed 10-06) |
| Ryan's Warmth drops: choosing Jake | SP2 (Ryan, lowered by) |
| this step as the voice sample | LO, 2026-10-08 |
| the prose | `v2-prose`, measured by `gates.py --beat`, 2026-10-08 |
| the Warmth −10 and Want +5 | guess |
| fix from the false-line sweep | sweep A4-03 (2026-10-08) |
