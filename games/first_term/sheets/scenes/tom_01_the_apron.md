# [READY] Scene — tom_01_the_apron
> Changed 2026-11-05 (DECISIONS 193): the job ask has its own row and no longer needs Tom placed; re-signed by LO 2026-11-05.
> Signed by LO: LO, 2026-11-04.

> Changed 2026-11-03 to match the build (third alignment pass); signed by LO 2026-11-04.

> The signed plans behind this page: `proposals/COPY_FIXES_C.md`.

> **Changed 2026-11-01 after the build, signed by LO 2026-11-01 ("Signed, build them")** (the reader's FAILs; LO's picks in chat): the job ask gets a no.

> **Changed 2026-11-01, signed by LO 2026-11-01 ("Signed")** (DECISIONS 99–116): Tom's release-1 ladder (`sheets/people/npc_tom.md`, signed). Reworked to strict: Tom never tells her to show and never sells her (LO, 2026-10-31). Cut: "You want it to show your waist." and "Regulars tip the pretty ones." Kept: his hands one second too long. Also changes his hire line, his counter lines and his first text (below), for the same reason.

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08. Tom's steps play inside a shift; her uniform is backed by the café's dress rule.

| row | answer |
|---|---|
| person · step | `npc_tom` · 1 (Tom B 1) |
| where · when | the café · Mon-Sat, starts 14:30-19:00, her first shift |
| gate | `cafe_job` · his step 0 |
| want | none before: step 1. His eyes on her ass as she carries the tray |
| next step | he touches her, as if it's nothing: the apron |
| hook | "Tables first. Phone in the back. Smile." The job's rules; the tip jar (step 2) |
| what she wears here | the normal café uniform (the dress rule) |
| explicit? | no |
| who notices | Tom |
| what she risks | her first day |
| her_line_low · her_line_high | low (under the stage): "He's your boss. Do the job." · high (over it): "You felt that second. So did he." (the person sheet names none; worded by me, signed by LO 2026-11-01) | |

## The step row (as built, 2026-11-03)

The seven columns, filled from what the build does.

**Kind · stage:** his hands on her for one second too long, nothing she chose · stage 1 (no gate)

| the moment | who sees or knows | what she risks | how she says yes | his move | does it finish | what changes after |
|---|---|---|---|---|---|---|
| he reties her apron strings, properly; his hands stay a second longer | Tom | her first day | "Yes, boss." or "I can tie my own apron." (his Power -5) | "Tables first. Phone in the back. Smile." | yes | his step 1; his Want +10; "Tips go in the jar. I count the jar." |

## Branch map — as built (2026-11-03)

One row per exit. Read from the build; it replaces the drafted map.

**`tom_01_the_apron`** — Café · Mon/Tue/Wed/Thu/Fri/Sat 14:30-19:00 · Tom there · needs Tom's step = 0 · `cafe_job` · one time

| node | what happens (first line) | explicit? | exit (label, what it needs → where) | effects |
|---|---|---|---|---|
| `back` | Tom looks up from the till as you come in. | no | "Clock in." — 2 versions, by clothes → `apron` | — · varies: equip cafe uniform normal |
| `apron` | Tom hands you a fresh apron at the start of the shift, and when you tie … | no | "Yes, boss." → `tray` | equip cafe uniform normal |
| | | | "I can tie my own apron." → `tray` | Tom's Power -5 · equip cafe uniform normal |
| `tray` | You carry the tray out. | no | "Table six." → Café | Tom's Want +10 · Tom's step = 1 · `tom_01_done` set |

## The lines that change (mine, for signed by LO 2026-11-01)

> Drafted before the build and kept as the signed record. Where it differs, the branch map and the beats above say what the build does.

**The step**:

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

**His hire line** (`cafe_job_ask`):

| built | new |
|---|---|
| "Eight a shift, plus tips. Regulars tip the pretty ones, so you'll do fine." | "Eight a shift, plus tips. Be on time." |
| thought: "He said pretty like it's part of the job description. Maybe it is." | "He looked at you one second too long. Then he was all business." |
| "Wear that. Be on time. Smile at booth four." | "Wear that. Be on time." |
| (`college_for_fun`) "You look like you like a good time. Customers like that." | cut |

**His counter** (`hub_tom_cafe`), by his steps as they are now:

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
| `cafe_job_ask` (the sign in the window) | "Not yet." | Tom: "Sign stays up till somebody takes it." · "He goes back to wiping the machine." The ask comes back the next day. |

## Changed 2026-11-02 (reader a3, `READER_FAILS_A3.md`, signed by LO 2026-11-02; DECISIONS 131)

- Row 59 (`hub_tom_cafe`, the tight uniform): "He looks once, at your tits in it, and makes himself look at the till."
- Row 51 (`hub_tom_cafe`, the tight-dress node): a written no, "Leave it on the counter.", to a short screen: Tom: "Your call." No pay. Both in the build .
