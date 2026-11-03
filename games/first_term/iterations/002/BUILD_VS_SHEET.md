# first_term 0.1 — iteration 002, build against sheet

Written 2026-11-03 (third alignment pass, group 1) by reading the build (`toml_phases/7_final_game.toml`
at `ce8551b1`) against every page. No instrument diffs sheets against the build yet (`the-sheets.md` S1),
so this is a read, page by page. "Fixed" means the page now says what the build does and waits for LO's
re-sign; "build" means the page was right and the build is the thing to look at.

## Where the page said something the build does not do (all fixed on the page)

| page | the page said | the build does |
|---|---|---|
| SP1 | the overnight list: four flags | 121 flags cleared, `curfew_days` −1 |
| SP1 | the short-Sunday flag is cleared by Vance's knock | `rent_short`, cleared only by a full payment |
| SP2 | a locked button for an unwritten scene shows "(Next release)" | no button at all (DECISIONS 132) |
| SP2 | her no always moves his number | her no moves nothing of his (DECISIONS 135, 143) |
| SP2 | Laura keeps Want and Warmth | Laura keeps Warmth only; her steps carry the rest |
| SP3 | arc-numbered steps, 10 of them gone (Laura 5–7, Mark 5, 7, 9, Tom 4–5) | the built ladders: Ryan 8, Laura 4, Mark 4, Tom 3, Zoe 5, Jake 4, Hale 4 |
| SP3 | Laura's step 4 waits for Ryan | it reads three gaps watched and Laura seen alone (DECISIONS 106) |
| SP4 | $232 a week at the top; $8 plus tips | $10–12 a level-1 shift up to $28–40 (+$8) at level 3; week one about $205–245 |
| SP4 | Gary's $20 and Mark's prices | cut; the café and Ryan's one $25 are the only income |
| SP4 | goal 1 by the streak or Mark A 9 | the streak only: four Sundays in a row |
| SP7 | Ryan A 9 · Laura C 8 · Mark A 9 · Hale B 5 · Tom B 6; a door at `ryan_08_two_knocks` | Ryan 8 · Laura 4 · Mark 4 · Hale 4 · Tom 3; no door; seven end cards |
| `OPENING.md` | screen 9: "Keep hygiene on" / "Turn hygiene off" | "Go to campus." / "Go to campus. (Turn hygiene off)" |
| `OPENING.md` | the funnel ends in the kitchen at 07:50 | it ends in the dean's office at 08:05 |
| `OPENING.md` | the skip goes to screen 9 | the skip shows one hall screen, then screen 9 |
| `OPENING.md` | Ryan's +10 on "Run to your room." | on "Open the door." (DECISIONS 143) |
| `OPENING.md` | breakfast sets `ate_breakfast` | it does not |
| `COVERAGE.md` | the café customers' scout card is no row's source | it is now the café shift's source |
| `npc_gary.md` | "sweetheart" | "doll" |
| `npc_kayla.md` | grid: none | Friday 17:45–00:00 and Saturday 00:00–10:00, in Ryan's room |
| `npc_mark.md` | no Saturday morning rows | Saturday 07:00–08:30 bed, 08:30–09:00 kitchen, 17:00–18:30 kitchen |
| `npc_laura.md` | she keeps Want | Warmth only |
| `systems/home_life.md` | a `home_event` pool | no pool: `home_event` is the once-a-day flag on five random events |
| 29 place sheets | no walk-ins, no A1–A7 acts | the walk-ins, acts, rungs and pools as built |

| 61 scene sheets | stale hours, gates, pays, locks; "(Next release)" buttons; Ryan's +10 and step-8 +5 on the old buttons | the branch maps, step rows and explicit beats as built |
| scenes: walk-ins and A1–A7 | no sheet | `walkins_home.md`, `walkins_out.md`, `heat_acts.md` (new, `[REVIEW]`) |
| `jake_date_end` | the kiss capped at 59 | capped at 39 |

The beat passages the build reads from scene sheets were left byte-identical. Where one disagrees with what
LO asked for, the sheet still IS the build text and changes only at a rebuild he approves:
`ryan_hot_repeatables` beat 1c ("on the floor with a controller").

## Built differently from the signed heat proposal (for LO to confirm)

| what | the proposal | the build |
|---|---|---|
| walk-in odds | a flat 1 in 4 | 0.25 / 0.35 / 0.45 by her stage; 0.5 / 0.7 / 0.9 with the shower unlocked or the TV loud |
| the walk-in flags | "their next hub line reads it" | most out walk-in flags are read by nothing (`team_saw_gym`, `zoe_canteen_knee`, `zoe_in_the_tub` and 11 more) |
| B8 | Vance or Jake at the front step | Vance only |
| crude words | each person's crude columns | "pussy" in `walkin_shower_mark` and `walkin_mirror_mark` (in none of Mark's columns) and in `walkin_mirror_ryan` (outside Ryan's) |

## Where the page is right and the build may not be

| what | the page | the build |
|---|---|---|
| Jake's Wednesday pickup | dates Wednesday and Saturday (DECISIONS 138) | `jake_date_pickup` fires Wednesday too, but Jake's schedule has him at the front door only on Saturday; the Wednesday pickup may never show |
| goal 1's card tip | the body route is cut (Mark A 9) | the tip still says "so does taking his chair" |
| the ledger | the built ladders (SP3, SP7) | `dependencies[]` and `release_page.steps` still name the 2026-10-08 steps; `board.economy.week_income` still says 232 |
