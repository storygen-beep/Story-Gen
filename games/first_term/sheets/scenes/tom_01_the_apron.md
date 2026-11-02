# [READY] Scene — tom_01_the_apron

> **Changed 2026-11-01 after the build, signed by LO 2026-11-01 ("Signed, build them")** (the reader's FAILs; LO's picks in chat): the job ask gets a no.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–116): Tom's release-1 ladder (`sheets/people/npc_tom.md`, signed). Reworked to strict: Tom never tells her to show and never sells her (LO, 2026-10-31). Cut: "You want it to show your waist." and "Regulars tip the pretty ones." Kept: his hands one second too long. Also changes his hire line, his counter lines and his first text (below), for the same reason.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Tom's steps play inside a shift; her uniform is backed by the café's dress rule.

| row | answer |
|---|---|
| person · step | `npc_tom` · 1 (Tom B 1) |
| where · when | the café counter · Mon–Sat 14:30–22:00, her first shift |
| gate | `cafe_job` |
| want (test 1) | none before: step 1. His eyes on her ass as she carries the tray |
| next step (test 2) | he touches her, as if it's nothing: the apron |
| hook (test 3) | "Tables first. Phone in the back. Smile." The job's rules; the tip jar (step 2) |
| what she wears here (test 8) | the normal café uniform (the dress rule) |
| explicit? | no |
| who notices | Tom |
| what she risks | her first day |
| her_line_low · her_line_high (rule 7) | low (under the stage): "He's your boss. Do the job." · high (over it): "You felt that second. So did he." (the person sheet names none; worded by me, signed by LO 2026-11-01) | |

## Branch map — one row per screen (S1)

| node | what happens (one line) | explicit? | exits (label → target) | effects, with op (S4) |
|---|---|---|---|---|
| `apron` | Tom reties her apron from behind, properly, because she did it wrong: "Tables first. Phone in the back. Smile." His hands stay one second longer than tying takes | no | "Yes, boss." → `tray` · "I can tie my own apron." → `tray` (his Power add −5) | none |
| `tray` | she carries the tray out; his eyes follow her across the café, and he doesn't pretend they don't | no | "Table six." → the shift | Tom's Want add +10 (stored) · `tom_step` set 1 · `tom_01_done` set |

Both answers count; the second gives his Power add −5: she pushed back (as built).

## The lines that change (mine, for signed by LO 2026-11-01)

**The step** (`tom.py:59-71`):

| where | built | new |
|---|---|---|
| `apron`, first line | "…ties them again, tighter, his knuckles pressing into your hips through the uniform." | "…ties them again, properly. You did it wrong. His knuckles press into your hips through the uniform." |
| `apron`, Tom | "Like that. You want it to show your waist." | "Tables first. Phone in the back. Smile." |
| `apron`, first exit | "Then I'll be pretty." | "Yes, boss." |
| `tray`, Tom | "Regulars tip the pretty ones." | cut |
| `tray`, thought (Corruption under 20) | "Pretty is worth money here. Is that all you are to him? A tip?" | "He's your boss. Do the job." |
| `tray`, thought (20 and over) | "Pretty is worth money here. You can do pretty." | "You felt that second. So did he." |

**His hiring card** (LO 2026-11-02, "Yes all three"): until `cafe_job`, his row under People reads "The café in
town is hiring." · tip "The café in town, Monday to Saturday, 8 AM to 11 PM" · it points at `cafe_job_ask`. Before
it, only the "Week one" story card named the job, and it is gone after 7 days.

**His hire line** (`cafe_job_ask`, `tom.py:41-47`):

| built | new |
|---|---|
| "Eight a shift, plus tips. Regulars tip the pretty ones, so you'll do fine." | "Eight a shift, plus tips. Be on time." |
| thought: "He said pretty like it's part of the job description. Maybe it is." | "He looked at you one second too long. Then he was all business." |
| "Wear that. Be on time. Smile at booth four." | "Wear that. Be on time." |
| (`college_for_fun`) "You look like you like a good time. Customers like that." | cut |

**His counter** (`hub_tom_cafe`, `tom.py:300-315`), by his steps as they are now:

| built line | new |
|---|---|
| sexy uniform: "Top button stays open. House rule." | He looks once. "Your choice. Tables don't wait." (her choice, as `job.md` says) |
| normal uniform: he reties your apron; "Regulars tip the pretty ones." | He reties your apron from behind on his way past. "Tables first." |
| no bra, Gary in: "Booth four's going to tip big today." | "Apron on. Keep it on." (no Gary condition) |
| `tom_step` eq 1: "His eyes are on your apron strings again." | kept, and "He counts the tip jar when you're near." moves here (the leak before step 2) |
| `tom_step` eq 2: "He counts the tip jar when you're near." | "He won't look at the tip jar when you're near. Or at you." (he owes her) |
| `tom_step` eq 3: "Gary asks about you, you know. Every day." | "He watches the room now, and you in it, and he doesn't say a word about the window." |
| `tom_step` eq 4 and eq 5 lines (booth four, "Stay late Friday?") | cut: those steps are cut or later |
| Power 60+: "He tells you where to stand and how to lean, and expects you to do it." | "He tells you where to stand, and expects you to do it." |
| "Smile. It's worth money." (counter pool) | "Smile. Table three's waiting." |

**His first text** (`npc_tom.md`, phone thread, round 1): "what's it pay" gets "eight and tips. be on time." (was
"twelve and tips. more in a tighter top." and his Want +1: wrong pay and against strict).

## Why — the source of each key choice

| key choice | source |
|---|---|
| the scene and its lines | the arc ideas, Tom B 1 (heat 10-06) |
| the Power cost of pushing back | guess |

## Changed after the build (2026-11-01), signed by LO 2026-11-01

| screen | the no (new) | the reply (mine, signed by LO 2026-11-01) |
|---|---|---|
| `cafe_job_ask` (the sign in the window) | "Not yet." | Tom: "Sign stays up till somebody takes it." · "He goes back to wiping the machine." The ask comes back the next time she's in the café. |

## Changed 2026-11-02 (reader a3, `READER_FAILS_A3.md`, signed by LO 2026-11-02; DECISIONS 131)

- Row 59 (`hub_tom_cafe`, the tight uniform): "He looks once, at your tits in it, and makes himself look at the till."
- Row 51 (`hub_tom_cafe`, the tight-dress node): a written no, "Leave it on the counter.", to a short screen: Tom: "Your call." No pay. Both in `iterations/002/build_scripts/tom.py`.
