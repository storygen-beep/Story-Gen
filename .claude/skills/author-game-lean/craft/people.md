# craft/people.md — meeting people, and what they're like after

Read this before you write a card that brings in a person, or a scene with someone in it. Checked against Course of Temptation (CoT) and the field (LO, relayed 2026-11-22: "yes, send it"). How feelings and speech are written is `craft/voice.md`. Where a person is, and the face that shows it (never a room-text line, `craft/places.md` rule 2), is `craft/places.md` and `craft/clock.md`, read from their rows.

## Must read

On a card with a `Does:` block (every card from 2026-11-24 on), the rows that apply come from `check.py --rules`, which lists each with its craft file; the card has no `Craft:` line (`piece.md` step 2). On a card from before 2026-11-24, the `Craft:` line cites each one, or says in one line why it skips it. `when` and `judge` are the labels in `SKILL.md`, "Rule labels".

| id | what it asks | the failure it stops | when | judge |
|---|---|---|---|---|
| C618 | every person's hub sits behind a meeting; the first visit is the meeting | — | a first meeting | note |
| C619 | top games keep a first-contact flag per person, and nobody is met at turn one | — | a first meeting | note |
| C622 | a hub can hold its own first contact: the first visit is the meeting, later visits the hub | — | a first meeting | note |
| C627 | a met flag counts only if the one-time scene that sets it names the person | — | a first meeting | note |
| C625 | role before name: the relation first, the name when they meet | — | a person is on screen | note |
| C626 | swap the description for the name once the met flag is set, where the reference matters | — | a person is on screen | note |
| C630 | name and relation both, never one instead of the other | P13 reader pass 10: Ryan got his name and never his relation on screen | a person is on screen | reader |
| C632 | a role label says who the person is ("housemate, top floor"), not what they do for the plot | — | a person is on screen | note |
| C598 | a card names only people she has met | first_term's Ryan card | a goal card is shown | reader |
| C620 | a person is listed at a place only if met and there | — | a place is entered | note |
| C690 | the People page names only people she has met; its People Here lists everyone present, a stranger by their `stranger_name` | — | the plan | note |
| C613 | his wanting shows on his body, seen by her, before he acts on it | — | something sexual shows | note |
| C639 | an offer has three to five graded answers, eager to refusing, every one written | — | a no is possible | note |
| C640 | a no is content; a no that returns to an unchanged menu was never a door | — | a no is possible | note |
| C961 | her no never raises a meter | — | a meter is shown or paid | note |
| C954 | see `craft/economy.md` |  |  |  |
| C447 | see `craft/voice.md` |  |  |  |
| C593 | see `craft/voice.md` |  |  |  |
| C644 | each person owns a corner of the world: their own subject, their own people offscreen | — | a person is on screen | note |
| C596 | the talk screen: about 55 words, two-thirds spoken, one exit; the person's one picture sits on their menu (the screen their face opens), right after the menu's first line, and the talk screen under it has none unless it's a new moment (a menu with no picture is room and system menus only: C1265, `craft/media.md`) | P13 reader pass 12: Mom's living-room talk ran 26 words, 42% spoken (a judgement on a borrowed number) | a person is on screen | note + talk, length |
| C660 | each person's feelings are shown on the People view with CoT's words, the same across the cast: Friendship (Dislike below 0), Lust, His Dominance or Her Submission | — · kept blocking: LO's choice (2026-11-24; three feelings, 2026-11-25) | a meter is shown or paid | reader |
| C2177 | under `[engine.people] system = "cot"`, every person has friendship, lust and control on -1000..1000, gender, attracted, a type or hand-set values, and 2–4 traits from CoT's table; no 0–100 person meter is left | — · kept blocking: LO's choice (2026-11-25, LO's "Go ahead with your picks") | the plan | script + people |
| C2178 | a type sets a person's start feelings and traits, then each is tuned by hand; every trait has a job: it changes a number, or a scene reads it | — · kept blocking: LO's choice (2026-11-25, LO's "Go ahead with your picks") | the plan | script + people |
| C2179 | a reaction line to her choice, from a person whose want can differ, is picked by what they want from her and by their traits (`npc_wants`, `npc_has_trait`), never one line for everyone | — · kept blocking: LO's choice (2026-11-25, LO's "Go ahead with your picks") | a person is on screen | reader |
| C2180 | a choice moves a feeling by the table in rule 15: its sign by the act, its size (a random range) by what they want | — · kept blocking: LO's choice (2026-11-25, LO's "Go ahead with your picks") | a meter is shown or paid | reader |
| C2183 | a person may carry manner and hobby traits (personality-kind) that a written scene shows, the card citing the line; at least one of their 2–4 traits is shown and not sex-kind; a shown trait is true on every visit | first_term_lean P48: "every trait has a job" left all 24 people with control-set and sex-set traits only, and five (Laura, Nadia, Zoe, Kayla, Tess) with one hidden trait and an empty People page (LO: "Where is personality??") | a person is on screen | reader + people |
| C2182 | release 1 is frozen: people differ only by start values and traits, and nothing moves (no feeling effect, no skill gate, no effect on a skill) | — | the plan | note |
| C448 | obvious on arrival: who a person is, what they want, how they feel about her, in the first lines | P13 reader pass 10: Ryan arrived as a bare name, never "step-brother" on screen | a first meeting | reader |
| L168 | every person with a met flag is pointed at, by place and time, on a hint step whose `when` is the met flag, unless the opening meets them | before P46 only Tom was pointed at; sixteen people had nothing (first_term_lean, 2026-11-25) | a first meeting | script + pages |
| L169 | a first meeting she can miss fires on any visit while the person is there, or a hint names its window | each teacher's meeting fired only in a class's first 30 minutes, twice a week, with no timetable shown (P09, P15–P17) | a first meeting | reader |
| C2175 | under `people_page = "cot"`, every person has `stranger_name` and `people_tab` | — · kept blocking: LO's choice (2026-11-25, LO's "Go ahead") | the plan | script + pages |
| C1340 | the household loop: each housemate is their face at their spot, Talk inside their menu, +1 a click | first_term_lean's `talk_mom`, a Talk button on the kitchen menu | a repeatable, a person is on screen | reader |

## The measures

Re-run 2026-11-22 in CoT (`/Users/a0000/Documents/Player_Legibility_Study_20260825/corpus/course-of-temptation/passages`):
- **Name before meeting.** The `anonorfullname` widget (`GlobalWidgets.txt`, line 882) prints the full name only when `setup.people.can_identify_name()` is true, and a description otherwise. It's called 953 times; the whole `anonor…` family (first name, full name, with relation, capitalised) is called about 3,050 times.
- **Graded answers.** `BusGrope.txt` offers "Encourage it", "Ignore it", "Push their hand away", "Smack that hand" and "Yell for help".
- **The no as content.** "That certainly backfired." (`EventResHallPropositionShowersBold.txt`).

Field-measured, from `lists/COVERAGE.md`'s evidence column and not re-run today:
- C618 and C619: 17 of 27 games carry meeting state; 14 games keep a flag per person; none of 209 characters is met at turn one. CoT's meeting flags live in its story JS, which the corpus doesn't hold.
- C613: Great Games Study round 6. C593 and C644: sluttown-usa and destroyer. C596: 15,774 of 54,630 screens. C660: 13 games (the word the same across the cast). C690: 18 of 27 games. C598: CoT's cards never name someone she hasn't met.

## The shape

Each rule is marked **measured** or **LO's choice**.

1. **Nobody is met at the start except the people she lives with.** A meeting is one one-time scene that names the person and sets their met flag (C618, C619, C622, C627). *Measured in the field:* none of 209 characters is met at turn one.
2. **Until met, a person is a role or a description:** "the guy behind the counter". The name comes in the meeting; after it, both name and relation (C625, C626, C630, C632). *Measured:* CoT's `anonorfullname`, 953 calls.
3. **Unmet people are never named.** Cards and a place's faces leave them out; the People page's tabs list only people she has met. Its 📍 People Here lists everyone at her place, met or not, a stranger under their `stranger_name` ("guy behind the counter"), with "???" when clicked (C598, C620, C690). *Measured:* CoT's People Here takes `$peopleatlocation` (`Social.txt`, lines 40-62) and prints `anonymous_name` for anyone not yet known (`SocialWidgets.txt`, lines 233-240); its other tabs hold known people only. 18 of 27 games ship a page of met people. In the engine this is `[ui] people_page = "cot"` with `stranger_name` and `people_tab` on each `[[npcs]]` (`author-game-v2/references/engine.md` §34).
4. **His wanting shows on his body, seen by her, before he acts** (C613). *Measured in the field.*
5. **An offer has three to five graded answers,** eager to refusing, every one written. A no lands somewhere: a reply, a return later, a cost (C639, C640). Her no never raises a meter (C961). *Measured:* CoT's `BusGrope` and "That certainly backfired."
6. **Each person has their own manner, their own subject and their own name for her** (C447, C593, C644). *Measured* for C593 and C644; C447 is *LO's choice.*
7. **A talk screen is about 55 words, two-thirds spoken, one exit** (C596). The person's one picture is on their menu, after its first line, not on the talk under it, unless that talk is a new moment. *Measured in the field* (the talk screen); where the picture sits is ENI's ruling for LO, matching P42 as built and played.
8. **Every person carries the same people system** (C2177). Under `[engine.people] system = "cot"` (`.claude/skills/author-game-v2/references/engine.md` §54), each `[[npcs]]` has:
   - **three feelings toward her,** `friendship`, `lust` and `control`, in `core_traits`, on -1000..1000. Control above 0 means the person dominates her; below 0, she dominates them;
   - **`gender`** and **`attracted`** (yes or no: lust rises only if they are attracted to her);
   - **a type** (`people_type = "<type>"`, rule 13), or hand-set values;
   - **2–4 fixed traits** from CoT's table (`traits = [...]`), each with a job (rule 13).

   What they want from her (friend, date, fuckbuddy, hatefuck, rival, indifferent) is worked out by the engine from the feelings and traits; a scene reads it with `npc_wants`. A hand-set `want` is only for a person the story fixes. A professor is `professor = true`, with `core_traits.intimacy` 0, 1 or 2; they want nothing from her until 2. Romance and trust come later, each in the release where it first has a job. A person's arc keeps its own steps and flags on top: the step flags open the scenes, the feelings say how the person meets her. No 0–100 person meter is left, and `check.py`'s `people` check is red on one (it reads `people_type`; the engine ignores that key). *Measured:* CoT gives every person these feelings on -1000..1000, starting at 0 (`alter_attitude`, `_cot_js.txt` lines 113265-113315); attraction is orientation only (`attracted_to_pc`, line 113857); the want follows `desired_relationship` (lines 114752-115010); a professor's intimacy is 0/1/2 (`professor_intimacy`, line 117982), moved at half and full of a lust threshold of 400 to 800 by kind (lines 117966-117980); CoT's special people carry a fixed want. Three feelings now, not five, is *LO's choice* (LO, typed in main-lean 2026-11-25: "Yes lets move to cot style type system", "Go ahead with your picks"). This replaces "one or two meters per person" and C650's score-by-role choice.
9. **Obvious on arrival** (C448). *LO's rule, not measured.*
10. **A person's actions are in their own menu, behind their face** (C1340). On the room screen the person is their face. Clicking it opens their menu: Talk, and whatever else she can do with them. None of it is a room button. Talk is once a day, and the person never locks: after Talk is used, the face still opens the menu, and the other options are still there. *Measured:* CoT's People Here list (`StoryCaption.txt`, lines 585-596) opens the person's card with "Talk to her" (`DisplayNPCWidgets.txt`, lines 33-68), and her own menu has 38 `<<link>>`s, 14 of them checked once a day against `$interactionstoday` (one at `InPersonDialogueMenu.txt`, line 77). Of 9 other top games, 5 put a person's actions behind the person: click the person (family-ties), one room button into her own menu (3, such as the-hellfire-club's "Speak to Daisy" in `DaisyRoom.txt`, line 18, into `Daisy_conv`), or her room is her menu (degrees-of-lewdity). The other 4 put each action loose on the room menu, shown while the person is there (lust-for-life's kitchen: "Approach Cory", `home-kitchen.txt`, line 15). Faces, not buttons, is *LO's choice* (relayed 2026-11-23: "Yes"), with CoT.
11. **Every first meeting is pointed at** (L168). Each person with a met flag gets a storyline step on the Quests page that says where and when to find them ("From your second week, three girls own the mirror in the women's bathroom off the Lecture Hall, weekdays 8 to 9am and 1 to 2pm."), followed by a step whose `when` is the met flag. Only the people the opening meets need none. `check.py`'s `pages` check is red on a met flag no hint step reads. *LO's choice* (LO, typed in main-lean 2026-11-25: "Go ahead"), with CoT, whose Hints page carries a storyline per person worth finding.
12. **A meeting she can miss is not missed for good** (L169). Either it fires on any visit while the person is there, or its hint names the window (the class, its days and hours). A meeting inside the first 30 minutes of a class held twice a week, with no timetable shown before it, is the failure. *LO's choice* (same).

13. **Pick a type, then tune** (C2178, C2183). A type is a row in the plan's type table (`plan.md` §3): the start friendship, lust and control, and the traits it draws from. Start from the type, then tune each person by hand. A game names the types it needs: Family, Professor, Student, Worker, Neighbour, or others.
   - **Every trait has a job.** Either it changes a number (it is in a set the want reads: Slut, Strictly Casual, Forward, Confident, Dominant, Submissive, Switch, Sadist, Masochist, Aromantic; or it is Chaste or Asexual), or some scene reads it with `npc_has_trait`, or it is a **manner or hobby trait** (a personality-kind trait from CoT's table: Shy, Bully, Insecure, Bragger, Loner, Gamer, Cook, Sporty, Nerd and the rest) that a scene already written shows. That trait's job is to be learned on the People view, and later to be a chat topic; it needs no `npc_has_trait` reader yet. The card cites the line that shows it (C2183). `check.py`'s `people` check is red on a sex-kind or hidden trait with no number job and no reader.
   - **At least one trait the player can learn.** Of the 2–4, at least one is shown and not sex-kind, where the scenes give one: a person whose every trait is hidden (Confident, Loyal, Cheater) or sex-kind has an empty personality on the People view. The `people` check is red on a person whose every trait is hidden.
   - **A shown trait is a claim** (C2183): true on every visit. Bully on a person who is only ever kind is a lie on the People view.
   - **A trait shows only past its threshold** (friendship above 100 to 600, a sex trait only after sex). While release 1 moves nothing, a trait shows only if the start friendship is above its threshold.

   *Measured:* CoT's archetypes set the traits (`setup.archetypes`, `_cot_js.txt` line 19348; its Wage Worker carries "Forward", line 19391), and start every feeling at 0. Ours start apart, because release 1 moves nothing (`plan.md` §10), so start values are the only way two people differ. CoT reads a trait's hobby only for the person's posts (`elkbook` tags, lines 49075-49174) and the want never reads it. The trait table and thresholds are lines 116953-117371. *LO's choice* (same); manner and hobby traits shown by a written scene, LO's "Yes to both A and B", typed in main-lean 2026-11-25.
14. **A reaction reads the person** (C2179). When her choice gets a reaction from someone whose want can differ (worked out, not hand-set), the line is picked by what they want from her and by their traits: a `group` block per want (`npc_wants`), or per trait (`npc_has_trait`), and a plain line for the rest. One line for everyone is the failure. A person whose want the story fixes gets one line. *Measured:* CoT's `EventResHallRunInto.txt` (lines 3-12) answers the same bump four ways: "Shit, sorry!" (friend, date, fuckbuddy), a hand on her ass (hatefuck), "Watch where you're going" (rival), "Sorry!" (the rest). `InPersonDialogueFlirtBrazen.txt` (lines 57-81) answers one flirt six ways by the want. *LO's choice* (same).
15. **How a choice moves a feeling** (C2180). The act sets the sign; what they want sets the size. A size is a random range, `value = { type = "random", min = 25, max = 50 }`. Release 1 moves nothing (`plan.md` §10); this table is for the release that first moves a feeling.

   | her choice | feeling | size | CoT |
   |---|---|---|---|
   | flirt | lust up | 25–50 if they want to date, fuck or hatefuck her; 15–25 if rival or indifferent; 5–10 if they want a friend | `InPersonDialogueFlirtBrazen.txt`, lines 57-81 |
   | a friendly compliment | friendship up | 15–30, only if they like her | `InPersonDialogueCompliment.txt`, line 17 |
   | help them | friendship up | 25–50 | `EventProfessorHelpCleanDo.txt`, line 17; `EventGreekHouseHWHelpYes.txt`, line 8 (50) |
   | insult | friendship down | 50–75 | `InPersonDialogueInsult.txt`, line 4 |
   | give in, do what they say | control up | 10–30 | `EventClassroomHarasserMPFilmSkirtDo.txt`, line 1 (12); `EventStudyAdmirerCleavageFlash.txt`, line 7 (30) |
   | take charge | control down | 20–25 | `EventClassroomAdmirerSeeAssEncourage.txt`, line 1 (25); `EventClassroomGeneralBullyBallDo.txt`, line 3 (20) |
   | refuse | the feeling they asked with goes down | 25 | `EventGreekHouseHWHelpNo.txt`, line 4 (friendship); `EventSpringrilSplashPartyAnonGroperStop.txt`, line 2 (lust 25, control 15) |

   Her no lowers a feeling and never raises one of her skills (C961). *Measured* (2026-11-25, CoT's passages): of 922 friendship moves, 186 are ±25 and 154 are ±50; of 818 lust moves, 105 are +25 and 91 are +50; of 475 control moves, 144 are ±25 and 99 are ±50. The talk menu's moves are ranges (5–10, 15–30, 25–50), each once a day per person (`InPersonDialogueMenu.txt`, lines 1-2 and 77). *LO's choice* (same).

## The engine (cited; `v2.py` is `apps/game_generation/twee_comprehensive/generators/v2.py`)

- `npc = "npc_<x>"` on a canvas's trigger is read at `apps/projects/services/template_import.py:2581` and carried as the canvas's `npcId` (v2.py:15097-15099).
- A repeatable, manual canvas with an `npcId` shows as the person's face, not as a room button (v2.py:5935-5952; room buttons skip it at v2.py:5979 and 6680; the faces are drawn at v2.py:6541-6542).
- **One canvas per person per place.** The face opens the highest-`priority` canvas of that person there (v2.py:5954-5958). Two canvases for the same person in one room give one face, and the lower one never shows. So the person's menu is one hub canvas, and Talk and the rest are choices inside it.
- **Who is pointed at.** Under `[ui] quests_layout = "hints"` the Quests page is `[[story_hints]]` and `[[walkthroughs]]` (`.claude/skills/author-game-v2/references/engine.md:1094-1120`). The person's `[[quest_cards]]` stay: they decide who is met, and their `tip` shows in the person's People view. A hint step points at a meeting; the card never does.
- **The people system** is `[engine.people] system = "cot"`: the importer half is `apps/projects/services/people_system.py` (its checks at lines 570-634), the run-time half `apps/game_generation/twee_comprehensive/generators/people_system.py` (the want at lines 93-156; a lust gain dropped for a person who isn't attracted at lines 180-186). The conditions `npc_wants` and `npc_has_trait` go wherever a v1.0 conditions table goes, never on a `[[quest_cards]]` card (engine.md §54).
- **Once a day, by a flag.** A choice sets a `_today` flag in its `flagEffects` and is shown only while that flag is false; `[engine.daily_tick]` clears it when the day rolls (v2.py:7173-7175; `.claude/skills/author-game-v2/references/engine.md:1458-1485`). The menu itself has no daily cap, so the person never locks.

## Worked example

Roles: the café manager. LO approved these words, with his name as a slot that appears only after the meeting. The pay is named in the scene and never on the button (C954); this file names no amount.

**Before the meeting**
> A man in his thirties is behind the counter, sleeves rolled up, wiping a spot that's already clean. The Help Wanted sign sits in the window behind him.
> The guy behind the counter: "You here about the sign, or the coffee?"

Buttons: "The sign. I need the work." · "Both?" (she smiles) · "Just the coffee."

**After "Both?"** (the meeting)
> His eyes go to your mouth when you smile, then down to the till, fast.
> <His name>: "<His name>. I run the place. Shifts are four hours, <pay named here>. You start when I say."
> Your face goes warm. You've got a job.

This sets his met flag. He appears on the People page, and the shift button opens.

**After "Just the coffee."** (no meeting)
> The guy behind the counter: "Suit yourself. Sign stays up."
> He slides the coffee over without looking at you.

No met flag is set, and she can ask again.

**A person's menu** (rule 10). Roles: her mom, in the kitchen by her rows. The lines are filler, in roles.

On the kitchen screen: Mom's face, and no line for her in the room text (`craft/places.md` rule 2). No "Talk to Mom" button among the room's.

Her menu, on a click:
> Mom looks up from the pan. "Hungry, or just here to steal bacon?"

Picture, right after that line: her mom at the stove, looking up. Her one picture; the Talk screen under it has none (C596).

Buttons: Talk (once a day) · Help her cook · Leave her to it. (Talk spends 5 minutes and cooking 15; the labels say neither.)

After Talk today, the face still opens the menu. Talk is gone until tomorrow, and Help her cook and Leave her to it are still there. The `talked_mom_today` flag clears at the day turn.

**The type table** (rule 13). Roles, not a world; the numbers are filler, a game picks its own.

| type | friendship | lust | control | traits it draws from |
|---|---|---|---|---|
| Family (a parent) | 400 | 0 | 200 | Confident, Cook, Loyal |
| Family (a sibling) | 150 | 0 | 0 | Gamer, Bully, Insecure |
| Professor | 0 | 0 | 150 | Assertive, Nerd; `professor = true`, intimacy 0 |
| Student | 0 | 0 | 0 | Shy or Forward, one hobby, one sex trait |
| Worker (her boss) | 50 | 50 | 250 | Forward, Assertive |
| Neighbour | 100 | 0 | 0 | Loner, Green Thumb, Voyeur |

The café manager, tuned from Worker. Bragger is a manner trait the meeting already shows ("<His name>. I run the place. … You start when I say.", the worked example above), so the card cites that line; it needs no reader yet.
```toml
[[npcs]]
id          = "npc_manager"
people_type = "worker"
gender      = "male"
attracted   = true
traits      = ["Forward", "Bragger", "Assertive"]       # Forward: he wants to fuck, not date; Bragger: shown at the meeting; Assertive: his talk reads it
core_traits = { friendship = 50, lust = 120, control = 250 }   # lust tuned up: his eyes go to her mouth at the meeting
```

**A reaction by want** (rule 14). Her choice "Bump into him on purpose", in the café; the next node's blocks, in the shape `games/first_term_lean/toml_phases/5_scenes.toml` uses. The lines are filler.
```toml
blocks = [
  { type = "group", props = { conditions = { version = "1.0", logic = "AND", items = [{ type = "npc_wants", npc_id = "npc_manager", any_of = ["fuckbuddy", "hatefuck"] }] } }, blocks = [
    { type = "paragraph", content = "His hand lands on your ass and stays there a second too long. \"Careful.\"" },
  ] },
  { type = "group", props = { conditions = { version = "1.0", logic = "AND", items = [{ type = "npc_wants", npc_id = "npc_manager", value = "rival" }] } }, blocks = [
    { type = "paragraph", content = "\"Watch it.\" He steps around you like you're a spill." },
  ] },
  { type = "group", props = { conditions = { version = "1.0", logic = "AND", items = [{ type = "npc_wants", npc_id = "npc_manager", any_of = ["fuckbuddy", "hatefuck", "rival"], operator = "is_false" }] } }, blocks = [
    { type = "paragraph", content = "\"Sorry,\" he says, and he's gone." },
  ] },
]
```
Adjacent groups merge into one if/else chain, so exactly one line shows. The third group answers everyone else; a plain paragraph after them would show to everyone.

## Not this

- A Talk button per person on the room menu. The person is their face, and Talk is inside their menu (rule 10; C1340).
- A person who locks after one talk. Talk is once a day; the face and the rest of the menu stay (rule 10).
- A person named before the meeting. Until then, the guy behind the counter (C625).
- A meeting with one answer. Three to five, eager to refusing (C639).
- A no that returns to an unchanged menu. It lands somewhere (C640).
- A met flag no hint step reads: the player never learns the person exists (L168).
- A meeting only in a class's first half hour, twice a week, with no hint naming it (L169).
- A person named at a place, or on the People page, before she has met them (C620, C690). People Here lists them, by their stranger name only.
- A 0–100 Want or Warmth meter on a person. Their feelings are friendship, lust and control on -1000..1000 (rule 8; C2177).
- A manner or hobby trait no written scene shows: "Nerd" on a person who never says or does anything nerdy (rule 13; C2183).
- A person whose every trait is hidden or sex-kind: their personality on the People view stays empty (rule 13; C2183, P48).
- One reaction line for everyone, when the person's want can differ: the same "Sorry!" from the rival and from the man who wants her (rule 14; C2179).
- A hand-set `want` on a person the story doesn't fix. Let the engine work it out (rule 8).
