# [READY] Decisions — First Term

> Signed by LO: LO, 2026-10-09 (changed 2026-10-09).

> Placed at the game's root 2026-10-08. Written 2026-10-08, phase board.
> This sheet and the ledger say the same thing. Where they differ, it is listed below, and nothing
> was changed in the ledger.

## Open questions for LO — first

None open. 37 and 39 were answered 2026-10-09 (below).

## Answered (LO, 2026-10-13, after playing to day 4)

LO played to Thursday of week one and stood at Corruption 0, Exhibitionism 3. Every one of the 36 Corruption
raises in the build needs Corruption 20 or 40 already, so Good Girl had no way up except a drink, which no hint
names.

| # | question | LO's answer |
|---|---|---|
| 78 | What raises her meters at stage 1, and does an event she didn't choose (walking into the couple in the park, Ryan in a towel) raise them? | Only her choice pays. An event pays nothing; a button where she goes further pays: +1 for an everyday act, +3 for a big one-time step. Each act pays only until she is past its stage (a Good Girl act stops at 19, Curious at 39, Bold at 59). Every stage needs acts that pay, the first one included, so a stage-1 accident carries a button to linger. A drink is not a way up. |

These signed pages say the old thing and wait for LO's re-sign; nothing on them was changed:
`sheets/scenes/park_watch_the_couple.md:11,15` (stage 1 raises nothing), `sheets/places/home_hall.md:44-47`
(the home accidents raise only his number), the ledger's `fed_at` for `corruption` (lecture hall, Zoe's, the café,
none of which pays at Good Girl), and the two Quests-page goal labels at `toml_phases/7_final_game.toml:22360`
and its Exhibitionism twin, which name sources that pay nothing at stage 1.

## Answered (LO, 2026-10-30, the schedule pop-up)

| # | question | LO's answer |
|---|---|---|
| 97 | Redesign the Quests page without changing its content? Keep it per person, like the top games? | "Go ahead". `[ui] quests_layout = "list"`: Back on top, "My story" rows with a progress bar, then one row per person, ready first and soonest first, with "Today …" and a Now tag; a tap opens the card's text, next step and tip; finished people fold away. Same words, only moved. Vesper keeps the cards page. |
| 98 | In a towel she only meets the people at home: should they react by their meter, every time, with a towel-only choice that pays? | "Go ahead, Mark bedroom and garage out". 9 home hubs (Ryan: room, dinner, couch, bathroom door; Laura: kitchen, waiting up, dressing; Mark: up late, kitchen) read the towel by that person's meter in three bands, lines taking turns. "Let it slip." (Exhibitionism 20) and, at the top band, "Drop it." (Exhibitionism 40 and a step) for Ryan and Mark; "Let her fix it." for Laura. Pays +2 to his/her meter (Ryan also her Exhibitionism +1) once a day per person. Laura in the room catches it: her Love −3, no pay. |
| 96 | "In one table it shows everything. It becomes a lot confusing." Simplify it? | "Yes" to one day at a time: day chips with today picked, a "Now:" line, then one row per stretch of the day (short time, place, what they do under it), the current row marked, back-to-back rows in the same place joined, sleep-only rows dimmed. |

Engine only (`setup.castScheduleHtml` in `v2.py`). The full Schedules page keeps its weekly table; first_term has no
button to it since DECISIONS 95.

## Answered (LO, 2026-10-30, the sidebar)

| # | question | LO's answer |
|---|---|---|
| 95 | The sidebar | "Remove stats schedules flags button from left sidebar. Rename shortcuts with cheats." On a phone, "a small floating clock in the top left side when sidebar is closed". "Schedules for each npc can go into the peoples page, a button in each people section for schedule modal." |

Built as `[ui] sidebar_hide = ["stats", "schedules", "flags"]` and `[ui] phone_clock = true` in `0_systems_spec.toml`,
and `[ui.cheat_page] title = "Cheats"`. The Stats and Schedules pages still exist; only their buttons went. Each card on
the People page carries a Schedule button when that person has schedule rows (Dr. Hale has none, so his has no button).
The Schedules page's "Your Activities" table has no new home. Snapshot:
`~/Documents/Great_Games_Study_20260926/first_term_snapshots/20261030_sidebar_before/`.

## Answered (LO, 2026-10-30, the People screen on a phone)

| # | question | LO's answer |
|---|---|---|
| 94 | Redesign the People screen, and make it phone friendly? | "Go ahead" with the tap-to-open list. One short row per person (face, name, one line under it, where they are now or "Away"); a tap opens the relationship, the meters as bars, NEXT, the tip and the tags; one open at a time; Back on top; somebody about right now first, then a ready scene, then the rest. |

An engine change, not a game one: `v2.py` `_generate_cast_page`, `_cast_page_js` (`setup.castRoster`, `castNext`,
`castWhen`) and `_cast_page_css`. Only first_term has a `[ui.cast_page]`. No TOML, key, save or gate changed. The old
screen showed two unlabelled 📍 lines per card (where he is, then where his next scene is); the new one says "● Kitchen"
on the row and "NEXT · Ready · Master Bedroom · Tue 6–10 PM" inside. Snapshot:
`~/Documents/Great_Games_Study_20260926/first_term_snapshots/20261030_people_screen_before/`.

## Answered (LO, 2026-10-30, the words for the people's meters)

| # | question | LO's answer |
|---|---|---|
| 93 | Are "Want", "Warmth" and "Power" the words the market uses? | No; rename what the player sees ("go ahead"), keep the keys. The market words, from our studies: Course of Temptation like / love / lust, Project Reeducation lust, New Life Project love points, Zara's School Life corruption for family members. "Corruption" was turned down for `want`: one label covers all five people, the older men aren't being corrupted, and it would sit next to her own Corruption on the same cards. |

| key (unchanged in code, saves and conditions) | the player now sees | who |
|---|---|---|
| `warmth` | Love | Laura, Ryan |
| `want` | Lust | Mark, Tom, Vance, Laura, Ryan |
| `power` | Dominance | Mark, Tom, Vance |

The sheets keep the old names as design terms (56 sheets); read them through this table. Only the shown labels changed:
`0_systems_spec.toml` `[[traits.labels]]` and `canv.py` `TRAIT_NAME` (the quest-card goals). Snapshot:
`~/Documents/Great_Games_Study_20260926/first_term_snapshots/20261030_meter_words_before/`.

## Answered (LO, 2026-10-30, channel 5 with Mark)

| # | question | LO's answer |
|---|---|---|
| 92 | Channel 5 with Mark paid the same as alone (+1) and gave him nothing. Should it pay more, and move Mark too? | Yes ("yes go ahead"). "Keep watching." with him pays her Corruption +2, cap 19 at Good Girl and 39 at Curious (never 40: row 78, Bold comes from Bold acts), and his Want +2. He has no Corruption meter (he keeps Want + Power), so Want is the one that moves. Once a day (`mark_tv_paid`, cleared at midnight): row 91's five-a-day cap can't reach a choice inside his portrait hub. After that it plays and pays nothing. His late hub runs past midnight, so one night can pay twice, the same as every `*_today` brake. |

Row 92 was written 2026-10-30 from LO's "yes go ahead" in chat. It touches `scenes/living_tv_channels.md` and `people/npc_mark.md`, each marked changed and waiting for LO's re-sign. Snapshot:
`~/Documents/Great_Games_Study_20260926/first_term_snapshots/20261030_mark_tv_before/`.

## Answered (LO, 2026-10-30, the TV alone)

| # | question | LO's answer |
|---|---|---|
| 91 | Watching TV alone has no daily limit (row 86). Cap it? | Five sessions a day ("make it 5"). One session is one opening of the remote; changing channel doesn't count, and every paid choice ends the session, so channel 5 pays at most 5 times a day (touching herself at Curious counts inside its session). The plain channels count too. After the fifth, the row greys out: "Watch TV — Not now." That grey row also shows when the room is busy or it's past 02:00, so its text says only "Not now." The count resets at midnight; the hours stay 07:00–02:00. The TV with Mark is unchanged. This replaces row 86's "no daily brake". |

Row 91 was written 2026-10-30 from LO's "Go ahead make it 5" in chat. It touches `scenes/living_tv_channels.md`, marked changed and waiting for LO's re-sign. Snapshot:
`~/Documents/Great_Games_Study_20260926/first_term_snapshots/20261030_tv_cap_before/`.

## Answered (LO, 2026-10-29, the locked buttons)

| # | question | LO's answer |
|---|---|---|
| 90 | A locked button says "(Needs Hungry)". At Good Girl the player has never seen that word, and it reads like food. What should it say? | The number: "(Needs Corruption 60)", and "(Needs Exhibitionism 60)" for the one Watched button. The "Further" screen behind it says "It comes later, when your Corruption reaches 60." (or Exhibitionism). The sidebar keeps its stage words (Good Girl, Curious, Bold, Hungry) and its number. |

Row 90 was written 2026-10-29 from LO's "Corruption 60, go" in chat. It touches 13 sheets, each marked changed and waiting for LO's re-sign. Snapshot:
`~/Documents/Great_Games_Study_20260926/first_term_snapshots/20261029_locked_labels_before/`.

## Answered (LO, 2026-10-29, step 4: the Good Girl moments)

| # | question | LO's answer |
|---|---|---|
| 79 | Which moments carry Good Girl to Curious under row 78? | Four: a "Look a second longer." button on the park couple (`park_watch_the_couple`); a couple in the library's back stacks (`library_back_stacks`, new); Ryan's door open a crack, Ryan alone with her panties (`ryan_door_ajar`, new); Mark and Laura through their door on Saturday night (`master_door_saturday_night`, new). In each, the look pays nothing and her staying pays corruption +1, cap 19. No ladder number moves. Nobody sees her, except in the park, where the stranger looks up at her as the signed `run` always had (now on `linger`). About 18 points a week, so Good Girl takes 7–8 days. |
| 80 | When are Mark and Laura awake together in their room? | Sun 00:00–01:00, the Saturday night after Laura comes up from waiting up (new). The door shows "The door's ajar." in that hour instead of "Ease the door open". |
| 81 | What do the Quests goal cards say? | Only places that pay at that stage. Curious: the park couple, the library stacks, Ryan's door at night, their door on Saturday night. Bold: her room, the bathroom, the women's toilet, the park. Daring: the lecture hall, the park. Showing: the campus gym, the women's toilet, the garden, the hall, the living room, the lecture hall, the park. The labels live only in `toml_phases/5_scenes.toml`; they change there in step 5. |

Rows 79–81 are signed by LO, 2026-10-29 ("sign all"); written that day from LO's picks in chat, with the sheets they
touch: the three new scene sheets, `park_watch_the_couple.md`, `places/library.md`, `places/home_ryan_room.md`,
`places/home_master_bedroom.md`, `people/npc_mark.md` and `people/npc_laura.md`. Snapshot of the old pages:
`~/Documents/Great_Games_Study_20260926/first_term_snapshots/20261029_good_girl_before/`.

## Answered (LO, 2026-10-29, the phone: a text books something)

| # | question | LO's answer |
|---|---|---|
| 87 | Laura's dinner text, and 7 more, change nothing when she answers. Patch or start over? | Patch ("go", after the top-games read: CoT and IHOH, round9a). Jake's pattern for each: the yes sets a `<x>_booked` flag; the scene or person reads it (showing up pays or plays its line and clears it); a yes with no show brings a short no-show text that costs, answered or ignored for a day. Ignoring the first text costs a little (warmth or Want −1). Only Tom's after close is gated by the booking; every other scene stays open, and step gates are untouched. |
| 88 | The amounts | Guesses, on each person's sheet: Laura warmth +1 for coming, −2 and suspicion +2 for a no-show, suspicion +1 for the eating-out lie; Tom money +4 for a booked shift, Want −1 and −2; Hale `grade_psych` −2 and −1; Ryan warmth −2; Zoe has no number, so a no-show sets `zoe_bailed` and her next park line says so. |
| 89 | The café closed at 22:00, so Tom step 6 and his after close (22:00–23:00) could never play | The café is open till 23:00 (LO, 2026-10-29). His counter hub runs 08:00–22:00, so the closing hour's face is his after-close scene. |

Rows 87–89 are signed by LO, 2026-10-29 ("café open till 23:00, then sign all"). 87–88 were written that day from LO's "go" in chat, with the sheets they touch:
`people/npc_laura.md`, `npc_zoe.md`, `npc_tom.md`, `npc_hale.md` and `npc_ryan.md`; 89 touches `places/cafe.md` and the ledger. Snapshots:
`~/Documents/Great_Games_Study_20260926/first_term_snapshots/20261029_texts_before/`, `20261029_cafe_hours_before/`.

## Answered (LO, 2026-10-29, after step 5: more often than Saturday)

| # | question | LO's answer |
|---|---|---|
| 82 | Can the walk-in at their door come more often than Saturday night? | Not Mark and Laura together: once a week fits a cold marriage, and Mark's weeknights downstairs are his ladder. Instead, Laura alone (`laura_alone_in_bed`, new): Sun–Fri 22:00–23:00, Mark downstairs, her door ajar, Laura fingering herself. Same shape as row 79: the look pays nothing, "Keep watching." pays corruption +1, cap 19, once a night. Laura's bedroom row splits so 22:00–23:00 is "awake, alone". |
| 83 | Mark's lines say Laura is asleep from 22:00. Which way? | Reword Mark: "asleep" becomes "gone up" or "upstairs", true either way (he thinks she's asleep; she isn't). His step 4 is named "After she's gone up". Ryan's step 4 line ("Mom's asleep.", no sheet carries it) became "Mom's gone to bed." by the same rule. The Curious goal card adds "Laura's door at night". |
| 84 | The door when someone is inside but the scene is off | A "Peek through the gap." option that pays nothing (reader item 4): Sat night after she watched, or Mark alone while Laura waits on the stairs (`master_door_peek`); and Laura's hour after she watched (`laura_alone_peek`). |
| 85 | The TV | A remote with 5 channels, each with its own clip: news, cooking, sports, an old film, and channel 5, the adult channel Mark pays for. Alone at any hour the room is empty; with Mark, inside his late hub, his reaction by his step. Ryan's and Laura's TV stay as they are. |
| 86 | What the adult channel pays | Every time she watches, no daily brake: "Keep watching." 30 min, corruption +1, cap 19 at Good Girl, cap 39 at Curious; alone at Curious, "Touch yourself." +2, cap 39. Time is the only limit (LO chose 30 min over 60 or 90, knowing Good Girl can take one long day at home and "the climb is paid for" may go red). |

Rows 85–86 are signed by LO, 2026-10-29 ("sign it"), with `scenes/living_tv_channels.md` and the living-room TV row.
Rows 82–84 are signed by LO, 2026-10-29 ("sign all"); written that day from LO's picks in chat, with the sheets they
touch: `scenes/laura_alone_in_bed.md` (new), `scenes/master_door_peek.md` (new), `places/home_master_bedroom.md`,
`people/npc_laura.md` and `people/npc_mark.md`. Snapshots: `first_term_snapshots/20261029_laura_alone_before/`, `20261029_tv_before/`.

## Answered (LO, 2026-10-09, during the iteration 002 build)

Asked while building parts 1 and 2 (`iterations/002/BUILD_LOG.md`). The street sheet, `college_mens_toilet.md`,
Laura's stairs row in the ledger (L20), the ledger's `in_release` for the men's toilet, and Q60 / SP1's
overnight list (77) still say the old thing and wait for LO's re-sign; nothing on them was changed.

| # | question | LO's answer |
|---|---|---|
| 75 | With Home a building, the street's "Home" opens the hall directly and the hall's late door never shows, so the street can't set `came_home_late` on its way home (Q35). | Outing flags only: the street sets no `came_home_late`; Laura's catch reads only `late_party`, `late_shift` and `late_date`, each for 4 hours. A late walk or park visit is never caught. |
| 76 | The brief lists `college_mens_toilet`; its sheet and the ledger say "not in 0.1". | Build it, empty: in Campus with hours and a closed line and nothing to do. |
| 77 | Q60 brakes each home item by 12 hours since its flag; the gates count only a flag cleared at midnight, and the engine can't write "unset or 12 hours ago" without two copies of every button. | Once a day, at midnight: each home item's flag is cleared in `[engine.daily_tick]` (16 flags added to the overnight list; changes Q60 and SP1). |

## Answered (LO, 2026-10-09)

| # | question | LO's answer |
|---|---|---|
| — | D11 and `mark_07_twenty_and_you_can_look.md`: is "Twenty, and you can look." a pay tag? | No. Kept as signed (question 33). It is her spoken offer, not a pay tag; D11 covers bracketed amounts like "($20)" on a button, not a line she says. |
| 37 | WANT.md still says the park is on her walk to campus. | Fixed now: `WANT.md:22-23` names the park as its own place, not her way to campus (SYSTEMS §14). |
| 39 | SYSTEMS.md:498 says `came_home_late` is set at the front door. | Fixed now: `SYSTEMS.md:498` says each outing sets its own late flag, the street's way home at 22:00 or later sets `came_home_late`, each is read for 4 hours, and her bed clears them (questions 35, 69). |

## Answered (LO, 2026-10-08)

### Batch 4 · the sweep's sheet rows and LO's other notes (everyday update)

Every sheet-origin sweep row is fixed on its sheet or answered here; the table is
`ROOT/first_term_sweep_20261008/SHEET_FIXES.md`.

| # | question | LO's answer |
|---|---|---|
| 69 | Why she's late | A flag per outing (`late_party`, `late_shift`, `late_date`), each read for 4 hours; her bed clears them and `came_home_late`; Laura's stairs row reads 4 hours. |
| 70 | Kayla on Saturday mornings | She stays every Friday night and leaves Saturday by 10:00. |
| 71 | "kid" | Dropped everywhere: Mark says @player, or @player.nickname when he's soft. |
| 72 | Mark A 5 and bare legs | The step needs bare legs; in jeans it waits. |
| 73 | Jake's pickup | A Saturday 19:00–21:00 pickup at the front door; "Go with him" sets `jake_date_went`; the door scenes read it; the booking lapses at 21:00. |
| 74 | Class rows | Zoe in Biology and figure drawing, Jake in figure drawing, each only once met. |

**LO's play notes, written as rules on the sheets** (LO, 2026-10-08):

| rule | where it is written |
|---|---|
| the feed and the selfie live on the phone only | the wardrobe card, "On the phone" |
| a person in the master bedroom has a face; lines name only who is there; no knock on a sleeping room | the master bedroom |
| each outing sets its own late flag; cleared every night | the street, "Why she's late" (question 69) |
| a garment reaction is a line in the person's hub | the wardrobe card |
| a chat follow-up waits for her reply, one answer per reply | the seven threads |
| a card's goals are the step's real requirements, never the counter | the seven ladder sheets, "Card goals" |
| a line about a past event shows only behind the flag that makes it true | Nadia's sheet; every scene fix in SHEET_FIXES |
| Home is a building; Zoe's flat is laid out like a flat | `home.md`, `zoe_flat.md` |
| arrival text never sits on a button that can be clicked again | the park couple (sweep A6-10) |

### Batch 3 · the rest of the picks and the phone (everyday update)

| # | question | LO's answer |
|---|---|---|
| 62 | The wait button | The engine's three steps (10 minutes, 1 hour, 1 day) for 0.1. Engine notes for later: the room isn't redrawn after a wait; the day button skips sleep. |
| 63 | Laura's curfew call | Friday 21:00–22:00, Laura awake; it never says where @player is. |
| 64 | The gym | "Gym" (`campus_gym`) in Campus, 1,500 words; Jake Tue, Thu 15:00–17:00 once met. |
| 65 | Area minutes | Said once in the street's description. |
| 66 | Feed and selfie on the phone | Yes. LO's fix: the selfie rungs gate on Exhibitionism (Covered 0, Daring 20, Showing 40), each label naming the act; the engine can't read clothes or place for a post. |
| 67 | Grocery money | $20 in, $20 out; Warmth +2 delivered; `laura_suspicion` +2 after 24 hours. |
| 68 | The batch 3 guesses | Taken. |

### Batch 2 · the home items (everyday update)

Written on `sheets/systems/home_life.md` (new), the home places and Laura's, Mark's and Ryan's sheets.

| # | question | LO's answer |
|---|---|---|
| 52 | Zoe's bedroom rows broke Zoe A 3 and A 4 | Keep the steps: her bedroom is Mon–Thu 22:00–00:00 only. |
| 53 | A seventh system card, `home_life` | Yes. |
| 54 | A dinner hour | Yes: Ryan Mon, Tue, Thu, Sun and Mark Mon, Tue, Thu, Fri in the kitchen 18:00–19:00; Ryan A 4, A 8, A 9 and Mark A 6 move to 19:00–22:00. LIVES needs LO's re-sign. |
| 55 | Ryan's TV afternoons | Yes: the living room Sat, Sun 14:00–18:00; his room 07:30–14:00. |
| 56 | Money for a tidy room | No: Warmth +2 at Sunday dinner, −1 if messy. |
| 57 | Swimwear for the garden | No new garment. |
| 58 | The master bedroom at night | No knock while all inside sleep; "Ease the door open", one screen, then back. |
| 59 | Random events at home | 1 in 4 on entering, one a day, "nothing happens" written. |
| 60 | Brakes | By hours since a flag (12 hours); SP1 unchanged. |
| 61 | The guesses | Taken. Mark's paid looks: one a day, $20. |
| — | Zoe at the party house (sweep A4-08) | LO: a Sat 20:00–00:00 `party_house` row above her living-room row. |

### Batch 1 · the map (everyday update)

Already decided by LO's play notes: the street shows **"Home"**, a building that opens in the hall; the
areas are **Home, Campus and Town**, with the street as the ground; Zoe's flat is laid out like a flat
and still hosts the Friday party.

| # | question | LO's answer |
|---|---|---|
| 43 | Which place sits in which area | As recommended. Home: the house and the garden. Campus: `campus` becomes the area; its 500 words move to the quad. Town (new): café, clothes shop, Zoe's flat, party house. On the street: Vance's house, the park, the corner shop. |
| 44 | Travel minutes | As recommended: into Campus 15, Town 15, Home 10. The park's 10 minutes is the park's **own** cost, not an area toll (LO: the park is not an area). Vance's and the corner shop 0. |
| 45 | The bus | The ride into town is the bus: 15 minutes, no fare (her student pass). Campus is a walk. |
| 46 | Energy for walking | No: time only. |
| 47 | Zoe's flat | "Zoe's Flat", hidden until `zoe_met`, opens in Zoe's Living Room (`zoe_apartment`, id kept). Off it: Zoe's Kitchen, Zoe's Bathroom (both new), Zoe's Bedroom. |
| 48 | Zoe's hours by room | As recommended; then narrowed by question 52 to keep two signed steps. |
| 49 | Pool or garden | A garden, "Garden", off the hall by the back door. Open 07:00–21:00, "It's dark out." 1,500 words. |
| 50 | The corner shop | Open in 0.1 for the grocery run only: plain, no heat. 07:00–22:00. 1,000 words. |
| 51 | New words outside the kitchen | Taken. The kitchen grows about 670 words in batch 2; COVERAGE settles it in batch 4. |

### Earlier


| # | question | LO's answer |
|---|---|---|
| 1 | Her face | Later: it is needed for the media before the build, not the sheets. |
| 2 | Tom's last step | The kiss after close repeats on Friday nights. |
| 3 | Tom B 7–9 | After 0.1. |
| 4 | Hygiene, colour only | Keep it. LO's call holds over the skill rule. |
| 5 | `laura_suspicion` has no reader | Laura's sheet adds two readers. |
| 6 | Zoe A 3 and SP2's group rule | Stays at stage 3; her friends leave the tub first, so only Zoe sees. |
| 7 | Nobody in the park | Zoe runs there weekend mornings. Ryan and Jake joining her wait for later. |
| 8 | The first explicit scene | The park couple: she walks into them, sees, and runs. |
| 9 | Small pools | Accept the warning for 0.1. |
| 10 | `party_hookup` and `park_hidden` | Add both. |
| 11 | The counts | The ledger is right: 37 rows, 110,500 words. |
| 12 | Which rooms get a door | Ryan's room and the master bedroom. |
| 13 | Touching herself alone | Yes, from Curious: her bed, the shower, the college toilet. |
| 14 | Alone in an office | Her grade posted on the door; open in their person's hours. |
| 15 | The party house hours | Saturday 20:00 to Sunday 03:00: Zoe A 3 has her home at 3 a.m. |
| 16 | Hours for the other places | The guesses on the sheets. |
| 17 | Readers for `campus_talk` and `followers` | The quad and canteen overhear; her room's feed. |
| 18 | Hale B 2, no panties at Daring | Yes, for that step only; the wardrobe rule stays at Showing. |
| 19 | Vance's numbers | Porch line at Want 30 and 60; at Power 60 he asks for her. |
| 20 | `laura_suspicion` | Late +5, a lie +5, failing +5, the letter +10; curfew at 50. |
| 21 | Phone threads | Seven; Hale's a college email; Laura's curfew call. |
| 22 | Guessed names and flags | Taken as guesses. |
| 23 | Mark at Monday breakfast | Yes, leaving for work at 07:40, in the opening only. |
| 24 | The hygiene choice | On the last opening screen. |
| 25 | The start choice's readers | Laura at dinner, Zoe at the first party, Hale in his office. |
| 26 | The opening card | First class 08:30 · ask the café for a job · $75 by Sunday. |
| 27 | Where the skip lands | On the last screen, every flag set. |
| 28 | The crude-word columns | Early: stages 1–2 · middle: stage 3 · late: stages 4–5. |
| 29 | Ryan's repeat in 0.1 | A kiss and his hands. |
| 30 | Step 5 into Saturday dawn | One canvas. |
| 31 | Second person | Yes: `narration_person = "second"` in the ledger. |
| 32 | Crude words for Tom, Zoe, Hale, Jake | A row on each person sheet, before their scenes. |
| 33 | "Twenty, and you can look" at the repeat table | Yes, from Bold, the price on the button. |
| 34 | The proposed crude words | Taken as proposed. |
| — | Mark A 5's `stop` screen, last sentence | Kept: on her body, not a pivot. |
| 35 | The front door as the way in | B: keep the tree. Only the street's way home, at 22:00 or later, sets `came_home_late`. |
| 38 | Drop `laura_suspicion` from the money card's feeds | Yes. |
| — | Tom B 4's `ten` screen, last sentence | Kept: on the body. |
| 41 | Crude words for strangers, extras, her alone | Taken: tits, nipples, ass, cock, wet, clit · no cunt, fuck, cum, pussy. |
| 40 | `party_hookup` (heat call A) | The cocky guy, oral or sex at Bold, named and with a face. Not Jake. |
| 42 | The cocky guy's rows at Zoe's | Yes: Fri 23:00–00:00, Sat 00:00–02:00, once `cocky_guy_met` is set. |
| 36 | Ledger change 3: name `laura_suspicion`'s 0.1 readers | Written: the catch on the stairs and the curfew (2026-10-08). |
| — | A second voice for touching herself | No: stages 2–3 share "warming up"; the bold voice starts at stage 4. |

**Question 6 keeps SP2 as signed.** Only Zoe sees her, which is Bold: naked by choice for someone she knows.
The step's hint and who-notices line in the ledger still name the friends (ledger change 11).

**Question 8, the beat.** She walks the path, walks into a couple in the bushes, sees them, and runs: an
accident, allowed at Good Girl. Curious adds "Stay and watch". Day one reaches it.

## Clashes: a skill rule against a signed page (S12)

| | the skill says | the signed page says | LO's answer |
|---|---|---|---|
| hygiene | *"A restore with no gate behind it is a button that maintains a number."* | *"Colour only, never a story lock."* | the page holds (2026-10-08) |

## Settled

| locked forever | expensive to change | cheap to change |
|---|---|---|
| every id: places, people, canvases | the map tree, street as the ground | each room's word budget |
| every trait and flag key | the anchor: the kitchen | shop hours and prices |
| her two meters run 0–100 | her stage edges: 20, 40, 60, 80 | energy costs and refills |
| the name tokens: `@player`, `@player.nickname` | rent: $75, rising to $90 and $100 | raise sizes on small acts |
| everyone's age, all 18 or older | the door: Ryan's two knocks | pool contents and their order |
| the title, First Term | who climbs: both | guidance card wording |

## The ledger keys

| ledger key | value |
|---|---|
| `board.map.archetype` · `exterior` | `nested_zones` · `street`, the only root |
| `board.map.home_base` | `home_ella_room` |
| `board.map.homes` | Ryan, his room · Laura and Mark, theirs · Zoe, hers · Vance, `vance_house` |
| `board.who_climbs` | `both` |
| `board.ascent_tiers` | `corruption`, `exhibitionism` · ceilings 100 each · start 0 |
| `board.economy` | `$` · a top week pays $232 · rent $75, Sunday 00:00, to Mark |
| obligation moves | $90 after $300 paid · $100 after $900 · then flat |
| `board.economy.sinks` | rent · canteen food · the clothes shop |
| `board.needs` | `energy`: spent, a real lock · `hygiene`: colour only, with an off switch |
| the anchor | `home_kitchen`: 30,000 of 119,300 words, 25.1%. It reaches 25%, barely. |
| places | 38 declared (four are buildings or areas); 37 in 0.1 (no men's toilet) |
| people | 21; 7 with ladders, 44 steps |
| `release_page.door` | `ryan_08_two_knocks` · "Two knocks" · step 9 locked, naming Hungry |

**The anchor is tight.** Other rooms can grow by about 700 words in total before the kitchen drops under
25%. Past that, every 1,000 words elsewhere needs about 330 more in the kitchen.

## Where the sheets and the ledger differ

| # | what | the ledger | the signed page or sheet |
|---|---|---|---|
| 1 | coverage rows | 37 | LO: the ledger is right |
| 2 | total word budget | 110,500 | LO: the ledger is right |
| 3 | college card acts | fixed: marked 0.2 | — |
| 4 | college card acts | fixed: the guy beside her added | — |
| 5 | `laura_suspicion` readers | "Ryan A 13" | a later step; nothing in 0.1 |
| 6 | the park's people | fixed: Zoe only, weekend mornings | — |
| 7 | key items | fixed: the slutty uniform dropped for now | — |
| 8 | `intelligence` fed at | fixed: the lecture hall added | — |
| 9 | Ryan steps 3 and 5 | fixed: Corruption +1 | — |
| 10 | the park | its own place | WANT.md still says she walks through it to campus |
| 11 | Tom's last step | 6 | SP5 fixed to step 6; it waits for your re-sign |

Row 10 is an older signed page behind a newer one. The newer page holds; WANT.md's line needs your
edit when you next re-sign it.

## Ledger changes

**Written 2026-10-08 with LO's yes** (backup: `first_term_snapshots/20261008_sheets_ledger_before/`):

| # | change |
|---|---|
| 1 | College card: the art lecturer, TA and dean acts marked "0.2" |
| 2 | College card: the guy beside her added at rungs 2 and 3 |
| 4 | Park `leads_to`: `npc_zoe` added |
| 5 | Zoe: a park row, Saturday and Sunday 08:00–10:00 |
| 6 | `cafe_uniform_slutty` dropped from key items until its release |
| 7 | `park_hidden` and `party_hookup` added to their pools |
| 8 | Ryan steps 3 and 5: Corruption +1, not +3 |
| 9 | `intelligence` fed in the lecture hall too |
| 10 | Park `people`: Zoe only; Ryan and Jake noted as later |
| 11 | Zoe A 3's hint and who-notices: Zoe alone |
| 12 | Job card: Tom's kiss repeats on Friday close |
| — | SP5 set to REVIEW in the ledger, with the page |


**Written 2026-10-08 with LO's yes, batch 2** (backup: `first_term_snapshots/20261008_places_ledger_before/`):

| # | change |
|---|---|
| 13 | `hours` and `closed_text` on 18 places; the rest always open or not in 0.1 |
| 14 | an `alone` row on every destination |
| 15 | `hidden_until`: `zoe_met` (apartment, bedroom), `party_house_invite`, `dean_summons` |
| 16 | park `serves.people`: `npc_zoe` |
| 17 | energy `fills`: the party house soak |
| 18 | a `door` on Ryan's room and the master bedroom |

**Written 2026-10-08 with LO's yes, batch 3** (backup: `first_term_snapshots/20261008_people_ledger_before/`):

| # | change |
|---|---|
| 19 | Laura's stairs row moved to the top of her list |
| 20 | Laura: master bedroom, Saturday 00:00–07:00 |
| 21 | Ryan's night row ends 06:45; Laura's ends 06:30 |
| 22 | Vance: `read_by` and `raised_by` on his Want and Power |

**Written 2026-10-08 with LO's yes, batch 5** (backup: `first_term_snapshots/20261008_narration_ledger_before/`):

| # | change |
|---|---|
| 23 | top-level `"narration_person": "second"` |

**Written 2026-10-08, batch 5** (backup: `first_term_snapshots/20261008_money_feeds_before/`):

| # | change |
|---|---|
| 25 | `money_pressure.feeds`: `laura_suspicion` dropped |

**Written 2026-10-08, heat call A** (backup: `first_term_snapshots/20261008_cocky_guy_rows_before/`):

| # | change |
|---|---|
| 26 | `npc_cocky_guy`: rows at Zoe's, Fri 23:00–00:00 and Sat 00:00–02:00, `when` `cocky_guy_met` |

**Written 2026-10-08 with LO's yes, everyday batch 1** (a snapshot before each: `first_term_snapshots/20261008_everyday_L1_before/` … `_L9_before/`, and `_L5b_before/`):

| # | change |
|---|---|
| L1 | `home` added: a building over the house rooms, from the street, opening in the hall; `crossing_costs` time 10 |
| L2 | `campus` is an area: `is_container`, `crossing_costs` time 15; its hours, closed text and 500 words gone; the quad 2,500 → 3,000 |
| L3 | `town` added: an area off the street over the café, clothes shop, Zoe's flat and the party house; `crossing_costs` time 15 (the bus) |
| L4 | `zoe_flat` added (hidden until `zoe_met`, opens in `zoe_apartment`); `zoe_kitchen` and `zoe_bathroom` added, 500 words each; `zoe_apartment` named "Zoe's Living Room" |
| L5 | Zoe's flat rows split by room; then narrowed (question 52): living room Mon–Thu 18:00–22:00, Fri–Sat 18:00–00:00, Sat 00:00–02:00; bedroom Mon–Thu 22:00–00:00 |
| L6 | `home_garden` added, off the hall, 07:00–21:00, 1,500 words |
| L7 | `corner_shop` in 0.1: 07:00–22:00, 1,000 words, the grocery run only |
| L8 | the park: `costs` time 10, its own (not an area) |
| L9 | `board.map.shape` rewritten; `board.map.areas` added; the release's place list takes the seven new places |

shape.py after: 22 pass, 0 fail.

**Written 2026-10-08 with LO's yes, everyday batch 2** (a snapshot before each: `first_term_snapshots/20261008_everyday_L10_before/` … `_L16_before/`, and `_L10b_before/`):

| # | change |
|---|---|
| L10 | `board.systems` adds `home_life`; `board.coverage` adds topic `home_life` (fixed once: the topic must be the card's id) |
| L11 | fills: kitchen 30,000 · living room 6,000 · garage 2,000 · her room 5,300 |
| L12 | `board.meters` adds `room_tidy` |
| L13 | dinner rows 18:00–19:00 for Ryan (Mon, Tue, Thu, Sun) and Mark (Mon, Tue, Thu, Fri); his room 19:00–22:00 (Friday 18:00–22:00 kept), the garage 19:00–22:00; Ryan steps 3, 7, 8 and Mark step 6 from 19:00 |
| L14 | Ryan: living room Sat, Sun 14:00–18:00; his weekend room row ends 14:00 |
| L15 | the master bedroom door: Knock while someone is awake · Ease the door open while all sleep · Go in when both are out |
| L16 | Zoe: `party_house` Sat 20:00–00:00, first in her list (sweep A4-08) |

shape.py after: 22 pass, 0 fail.

**Written 2026-10-08 with LO's yes, everyday batch 3** (a snapshot before each: `first_term_snapshots/20261008_everyday_L17_before/` … `_L19_before/`):

| # | change |
|---|---|
| L17 | park card: `park_selfie` out of the pool, `followers` out of its feeds, the selfie act out of its ladder; `followers` fed at her room only |
| L18 | `campus_gym` added inside Campus (1,500 words, in the release); Jake's gym rows Tue, Thu 15:00–17:00, `when` `jake_number` |
| L19 | `street` carries a description note with the minutes |

shape.py after: 22 pass, 0 fail.

**Written 2026-10-08 with LO's yes, everyday batch 4** (a snapshot before each: `first_term_snapshots/20261008_everyday_L20_before/` … `_L29_before/`, and `_L28b_before/`):

| # | change |
|---|---|
| L20 | Laura's stairs row: `when` = `came_home_late` set under 4 hours ago; `late_party`, `late_shift`, `late_date`, `came_home_late` in `resetting_flags` |
| L21 | the café's `closed_text`: "The café's shut." |
| L22 | Laura C 3: Mon, Tue, Thu, Fri |
| L23 | Vance: front door, Mon 18:00–19:00, `when` `rent_carried`, first in his list |
| L24 | Tom B 6: Friday 22:00–23:00 |
| L25 | Jake: pickup row Sat 19:00–21:00 (`jake_date_booked`); goodnight row `jake_date_went`; Jake B 3, B 4 and Laura C 5 gate on `jake_date_went` |
| L26 | Zoe A 4: Mon–Thu 18:00–22:00, and Sat 18:00–20:00 (`when_also`) |
| L27 | Zoe: lecture hall Tue, Thu 08:30–11:45 · Mon, Wed 13:00–14:30, `when` `zoe_met`; Jake: lecture hall Tue, Thu 08:30–10:00 · Wed 13:00–14:30, `when` `jake_number` |
| L28 | `board.coverage` adds travel, town_events, the gym, the garden, the grocery run (43 topics; the town events source fixed once to its card file) |
| L29 | Mark A 5: Sun–Fri 23:00–00:00 and Mon–Sat 00:00–01:00; its bare-legs gate noted |

shape.py after: 22 pass, 0 fail.

**Not a ledger change:** the ledger keeps no "entered from" per place. The sheets take it from the map's
shape line, and the build writes it as `entry_from`.

## Rows a gate needs (S6)

Nothing on these sheets is deferred. These rows hold up a gate:

| row | sheet | gate |
|---|---|---|
| the map: street is the only root | this one | the map is a place · world reachable |
| homes for every resident | this one | residents have homes |
| the kitchen at 25.1% | this one | location fill |
| energy locks a shift, Focus and the party | this one, college, job, parties | a need shuts a door |
| a bed, every day | this one | a need can be met every day |
| rent $75, Sunday, carried when short | money and rent | the obligation is charged · money gates something |
| shop prices on the label | wardrobe | a price is on its label · one currency |
| Gary's $20, half to Tom | job | sex for pay names the amount · her climb |
| six cards, each filled | all six system sheets | every system has a card (blocks a ship) |
| each card leads to a person | all six | leads to a person or a sex scene (blocks a ship) |
| seven states and the key items, read three times | wardrobe | every clothing state is read three times (blocks a ship) |
| `sports_bra` sold at the shop | wardrobe, park | a declared garment can be got |
| every meter has a reader in 0.1 | college, park, parties | a meter is read |
| the door repeats | this one | ends on an opening · the door can be seen again |
| no topic unknown | coverage | no unknown topic |

**At risk now:** `laura_suspicion` (readers on Laura's sheet). `followers` and `campus_talk` get 0.1 readers on the
place sheets (question 17). **Traversal heat** is a report row, not a ship block; question 13 raises it.

## Why — the source of each key choice

| key choice | source |
|---|---|
| nested zones, street as the ground | `the-map.md` R0, R3 · the board, 2026-10-08 |
| Vance sleeps at his house | LO, 2026-10-08 (LIVES.md:261) |
| who climbs: both | SP2 · `the-meters.md` W1 |
| stage edges 20/40/60/80 | LO, 2026-10-08 (SP2 §1) |
| every money number | LO, 2026-10-07 (SP4) |
| energy is a lock, hygiene colour only | LO, chat 2026-10-06 (SYSTEMS §5–6) |
| the anchor at 25% | `the-release.md` § The first release |
| Tom to step 6 | LO, 2026-10-08 (SP7) |
| the door | LO, 2026-10-07 (SP7) |
| the park couple as the first explicit beat | LO, 2026-10-08 · `the-arc.md` A15 |
| Zoe in the park at weekend mornings | LO, 2026-10-08 (08:00–10:00 is a guess) |
| a pool canvas for each Bold act | LO, 2026-10-08 |
| the eleven answers | LO, 2026-10-08 |
| questions 12–17 | LO, 2026-10-08 |
| questions 18–22 | LO, 2026-10-08 |
| questions 23–27 | LO, 2026-10-08 |
| questions 28–30 | LO, 2026-10-08 |
| questions 31–32 | LO, 2026-10-08 |
| questions 33–34 | LO, 2026-10-08 |
| questions 35, 38 | LO, 2026-10-08 |
| the seen_from rule | `gates.py:12998-13020` |
| `narration_person` | `state.md` schema · engine default `second` |
| the engine takes the first matching row | `v2.py:4304-4318` |
