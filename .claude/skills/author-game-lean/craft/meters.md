# craft/meters.md — her climb meters as CoT skills, and the acts that move them

Read this before you write a card that defines one of her climb meters, or an act that pays one. Her climb meters are Course of Temptation's (CoT's) skills: Disinhibition (it was Corruption), Exhibitionism, Submission and Dominance (LO, typed in main-lean 2026-11-25: "Yes lets move to cot style type system", "Go ahead with your picks", "Go ahead"). People's feelings toward her are `craft/people.md` rules 8 and 15.

## Must read

On a card with a `Does:` block (every card from 2026-11-24 on), the rows that apply come from `check.py --rules`, which lists each with its craft file; the card has no `Craft:` line (`piece.md` step 2). On a card from before 2026-11-24, the `Craft:` line cites each one, or says in one line why it skips it. `when` and `judge` are the labels in `SKILL.md`, "Rule labels".

| id | what it asks | the failure it stops | when | judge |
|---|---|---|---|---|
| C2181 | each climb meter is a CoT skill: 0..1000, level = value / 100, `skill = true`; a bold act is a `skill_gate` choice, and passing it raises the skill by CoT's gain table, under CoT's daily cap; every gate names one of her skills | — · kept blocking: LO's choice (2026-11-25, LO's "Go ahead with your picks") | a meter is shown or paid | script + people |
| C285 | the level ladder, 1 to 6, in CoT's order of acts (the table in rule 2); a game may move a row, never drop the order | — (the table) | the plan | note |
| C294 | a release that writes gates only up to level N has no gate above N, and names the next level only on a hint step | P01 | the plan | reader |
| C381 | a gate one level above her may show greyed, `show_when_locked`, as a preview of the next bolder act | P01 | a meter is shown or paid | reader |
| C188 | three "not yet" talks just below each level's first gate: she says why not yet; they raise and unlock nothing | P01 | a meter is shown or paid | reader |
| C1401 | pace by CoT's tables: about 2–3 gates a day at her level; a level takes about 4 days at level 0 and 12 from level 5; flag a level over 14 days | P01 | the plan | reader |
| C210 | crossing a level pays nothing: the sidebar prints the new level; a scene for it, if written, is one time and pays nothing | P01 | a meter is shown or paid | reader |
| C338 | an accident pays him, never her; the button where she goes further pays her; the way out pays nothing and is always there | first_term's accidents raised only the man (L68) | a meter is shown or paid | reader |
| C1366 | the Quests page names only places that pay at her level | first_term's four cards named places that paid nothing at stage 1 (L68) | a goal card is shown | reader |
| C388 | a locked door says why: a skill lock is the engine's "(Needs Exhibitionism 3)", a story lock carries `locked_text` | first_term's "(Needs Hungry)" (L116) | a meter is shown or paid | reader |
| C541 | after a choice, his reaction line opens the next node and the engine's toast stays; never print a +X for a stat that isn't shown | P13 reader pass 9: after "Fix the knot first" the next screen didn't open on Ryan's reaction | a meter is shown or paid | reader |
| L68 | every level, the first included, has gates that pay; only her choice pays | first_term stood at 0 on day 4 | the plan | reader |
| L69 | never pace a level by one paying act a day | first_term's 1-a-day caps made 20-day stages | the plan | reader |
| L70 | the first gain on each skill is open at 0: a level-1 gate, never a 1-in-4 walk-in | first_term's Exhibitionism sat at 0 behind a 1-in-4 walk-in | a meter is shown or paid | reader |
| L116 | a lock names the skill and a level the player can see, never a stage word | "(Needs Hungry)" read like food | a meter is shown or paid | reader |

## The measures

CoT, read 2026-11-25 (`/Users/a0000/Documents/Process_Review_20260925/round1_evidence/scripts/_cot_js.txt`, and the passages at `/Users/a0000/Documents/Player_Legibility_Study_20260825/corpus/course-of-temptation/passages`):
- **The scale.** A skill is 0..1000; its level is the value / 100 (`skill_level`, `_cot_js.txt` lines 96720-96723: "stored 0-1000 … present them as 0-10").
- **The gain and the cap.** `setup.Skills.default_increase = [10, 7, 6, 5, 4, 3, …]` and `setup.Skills.daily_caps = [30, 21, 18, 15, 12, 9, …]`, by her level (lines 83479-83480).
- **Too easy or too hard pays less.** One level below her (from level 2) ÷ 1.5, two below ÷ 2.5, three or more ÷ 3; a gate above her ÷ 2, ÷ 3 or ÷ 4 (lines 96759-96768).
- **The ladder runs 1 to 6.** CoT's passages gate Disinhibition 224 times (39 at level 1, 37 at 2, 80 at 3, 56 at 4, 8 at 5, 4 at 6), Exhibitionism 131 (29, 16, 20, 34, 23, 9), Submission 124 (1 at level 0, then 57, 38, 23, 4, 1 at levels 1–5) and Dominance 85 (37, 32, 14, 1, 1). Most gates sit at 1–4.
- **A level-1 gate is always open,** so a skill at 0 can start (engine.md §54, CoT's rule).

## The shape

Each rule is marked **measured** or **LO's choice**.

1. **Her climb meters are skills** (C2181). Each is a `[[traits.labels]]` row with `skill = true`, stored 0..1000 in `[player] core_traits`, shown in the sidebar as its level ("Exhibitionism 2"). A bold act is a choice with `skill_gate = { skill = "<key>", level = N }`, N from 1 to 10. Passing it raises the skill by her level's gain; you write no effect for it. `check.py`'s `people` check is red on a gate or `skill_level` condition that names no skill of hers. *Measured:* CoT's skills; Disinhibition and Exhibitionism replace Corruption and Exhibitionism, and Submission and Dominance are added, *LO's choice.*
2. **The ladder** (C285). The acts each level opens, in CoT's order. A game may move a row; it never drops the order.

   | level | Disinhibition | Exhibitionism | Submission | Dominance |
   |---|---|---|---|---|
   | 1 | "Give a flirty look" (`EventCampusWalkPass.txt`, line 6) | "Just keep cleaning" (`EventQuickieBurgerMuscles.txt`, line 12) | "Thank him for a good time" (`EventNewGuyInTownInsideFuckVag.txt`, line 26) | "Take his offer" (`EventPostGameFootballFreeUseApproach.txt`, line 62) |
   | 2 | "Give a flirty response" (`EventStreamingWorkoutObjectify.txt`, line 11) | "Seek more reassurance" (`EventBFFDormSexChatBreasts.txt`, line 13) | "Agree reluctantly" (`EventRiverRatServerBringOrderRemoveUnderwearNotWearingTell.txt`, line 7) | "Enough!" (`EventRMPPunishNakedPush.txt`, line 5) |
   | 3 | "Sext with him" (`FindrMatched.txt`, line 22) | "Flaunt yourself as you say you like it" (`EventRiverRatOwnerFirstTimeTopless.txt`, line 6) | "Okay, you'll do it" (`EventProfTaskLibraryGatherIntroNo.txt`, line 4) | "Okay, you'll find somebody to do it" (`EventProfTaskLibraryGatherIntroNo.txt`, line 5) |
   | 4 | "No, and maybe he'd like to see for himself later" (`EventWalkNoticeWildFantasiesApparel.txt`, line 6) | "Offer to go up there with him" (`EventSimSQuadPartyBecomeExhib.txt`, line 5) | "You shouldn't do this, but… he wants you to" (`EventProfTaskHypnosisStudentTriggerMasturbate.txt`, line 7) | — |
   | 5 | "Go ahead" (`EventCumWalkAddTo.txt`, line 5) | "Don't try to resist" (`EventProfTaskHypnosisStudentTriggerNaked.txt`, line 6) | — | "Spank him hard" (`EventLibraryBasementOppGetDrink.txt`, line 7) |
   | 6 | "Tell him to piss in your mouth" (`EventQuadPartyBathroomDoorlessWatersports.txt`, line 5) | "Toss your shirt into the crowd" (`SpringrilSplashPartySwimsuitContestPCFlash.txt`, line 14) | — | — |

   Where another craft file says "stage 1" or "stage 0–1" (`craft/heat.md`, `craft/opening.md`, `reader.md`), read level 0–1: things happen to her, and she reacts. *Measured.*
3. **A way up from 0** (L68, L70). Every level has gates that pay, at least two she can repeat. A level-1 gate is always open, so the first gain is open at 0, every day. *Measured* (CoT's level-1 rule); *LO's rule* that it holds at every level.
4. **Only her choice pays her** (C338). An accident pays him. The gate where she goes further pays her. The way out pays nothing and is always on the screen. *LO's rule.*
5. **"Not yet", out loud** (C188). Three talks just below each level's first gate, in her voice, paying nothing. *LO's rule.*
6. **Pace by CoT's tables** (C1401, L69). The engine applies the gain and the cap (engine.md §54); no `[engine.daily_caps]` band table on a skill (`check.py`'s `people` check is red on one). Give her about 2–3 gates a day at her level. At 3 a day a level takes about 4 days at level 0 (30 a day), 5 at level 1, 6 at 2, 7 at 3, 9 at 4 and 12 from level 5 (9 a day). A gate far below her pays less, so old gates slow down on their own. *Measured:* CoT's tables.
7. **Locks show a number** (C381, C388, L116). A gate she can't pass yet is hidden, or greyed with `show_when_locked = true` as a preview of the next level: "Strip. (Needs Exhibitionism 3)". Never a stage word. *LO's rule.*
8. **The Quests page** (C1366). The skill's storyline step (a `[[story_hints]]` entry, `craft/want.md` rule 4) names only places with a gate at her level.
9. **The crossing** (C210). The sidebar prints the new level. A one-time scene for it is optional and pays nothing.
10. **A partial release** (C294). No gate above the last level written; the next level is named only on a hint step.
11. **Release 1 moves nothing** (C2182, `plan.md` §10). Her skills show their start values; no gate and no effect raises them.

## The old rules (five stages of 20, before 2026-11-25)

| id | was | now | why |
|---|---|---|---|
| C285 | five stages of 20 on each meter | **changed:** the level ladder (rule 2) | CoT's skills run 0..1000 in levels; the order of acts stays |
| C294 | cap every pay at the top of the last written stage | **changed:** no gate above level N; the pay cap is gone | CoT caps no act; the daily cap paces it, and a skill can't rise past what its gates pay |
| C295 | small rungs at 5, 10, 15 inside each stage | **retired** | CoT has no rungs; several gates per level and the shrinking gain do that job |
| C381 | a small rung may show greyed as a preview | **changed:** the next level's gate may show greyed | the rung is gone; the preview stays |
| C188 | three "not yet" talks below each line | **kept** (below each level's first gate) | LO's rule |
| C330 | a repeatable act caps at the top of the stage above | **retired** | no act caps; CoT's gain table and daily cap set the pace |
| C1401 | a daily cap per band, 2–3 paying acts a day | **changed:** CoT's cap and gain tables, 2–3 gates a day | the field number it came from is CoT's own (pay 10 to 3, cap 30 to 9) |
| C210 | crossing a stage is a one-time scene | **changed:** the sidebar's level is the crossing; a scene is optional | CoT marks a level with a notice, not a scene (`raise_skill`, line 96796) |
| C338, C1366, C388, C541, L68, L70, L116 | — | **kept** (stage read as level) | LO's rules: only her choice pays her, a way up from 0, locks show a number |
| L69 | an act capped at its own stage's top; 1-a-day caps | **changed:** the cap half retired, the 1-a-day half kept | no act caps now; one act a day still makes a level take a month |

## The engine (cited)

- **The switch and the skill row** are `[engine.people] system = "cot"` and `[[traits.labels]] skill = true` (`.claude/skills/author-game-v2/references/engine.md` §54). The importer refuses a gate on an unknown skill and a value outside 0..1000 (`apps/projects/services/people_system.py`, lines 636-700).
- **The gain and the cap** are `SKILL_GAIN` and `SKILL_CAP` in `apps/game_generation/twee_comprehensive/generators/people_system.py` (lines 30-31), CoT's tables; the cap cuts every `add` on a skill, not only gates. A fall and `op = "set"` aren't cut.
- **The greyed line** always reads "(Needs <Skill> <level>)", even when another condition on the choice is the one that fails.

## Worked example

Roles, not a world: one skill, **Exhibitionism**, at the café and the bus stop. The lines are filler.

| act | gate | kind | pays her | how often |
|---|---|---|---|---|
| let a look go on, at the café | level 1 | her choice | the level gain | daily |
| don't fix the top that slipped, at the bus stop | level 1 | her choice | the level gain | daily |
| the lodger walks in on her towel | — | accident | nothing; his lust | once |
| that walk-in's button "Don't grab it" | level 1 | her choice inside it | the level gain | once |
| the not-yet talk with the neighbour | — | talk, at 180 | nothing | once |
| lean on his doorframe and let him look | level 2 | her choice | the level gain | daily |

```toml
[[traits.labels]]
key   = "exhibitionism"
label = "Exhibitionism"
skill = true

[[canvases.nodes.exit_block.choices]]
text             = "Lean on his doorframe and let him look"
show_when_locked = true
skill_gate       = { skill = "exhibitionism", level = 2 }
```

Before level 2 the button reads *Lean on his doorframe and let him look (Needs Exhibitionism 2)*. At level 0, each level-1 gate pays 10, up to 30 a day: three gates a day, level 1 in about 4 days.

**The not-yet talk** (at 180, pays nothing):
> The neighbour leans on the doorframe. "You keep coming back here, and you keep going home."
> "Because I'm not that girl yet."
> "Yet," he says, and smiles like he's already won.
> Your cheeks go hot. You said yet.

**The walk-in, after "Don't grab it"** (C338, C541):
> The towel slides to your waist, and you don't grab it. One second. Two. His eyes are on your tits, and he doesn't even pretend.
> "Jesus. Sorry." He backs out and pulls the door shut.
> Your face burns. You didn't grab it.

His line opens the screen, and the engine's toast shows the gain. No "+10 Exhibitionism" is printed in the text.

## Not this

- A 0–100 meter with five stages of 20. Her climb meters are skills, 0..1000 (rule 1; C2181).
- An effect that adds to a skill for passing a gate. The gate pays by itself (rule 1).
- An `[engine.daily_caps]` band table on a skill. CoT's cap already cuts it (rule 6).
- No gate at level 1. The first gain is open at 0 (rule 3; L70).
- An accident that pays her. It pays him; her button inside it pays her (C338).
- One gate a day, so a level takes a month (L69).
- A card that sends her to places with no gate at her level (C1366; L68).
- "(Needs Curious)" on a lock. The engine writes the skill and the level (C388; L116).
- A crossing scene that pays (C210).
- A "+10 Exhibitionism" printed in the text (C541).
- A gate or an effect that moves a skill in release 1 (rule 11).
