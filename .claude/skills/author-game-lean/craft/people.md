# craft/people.md — meeting people, and what they're like after

Read this before you write a card that brings in a person, or a scene with someone in it. Checked against Course of Temptation (CoT) and the field (LO, relayed 2026-11-22: "yes, send it"). How feelings and speech are written is `craft/voice.md`. Where a person is, and the presence line that shows it, is `craft/places.md` and `craft/clock.md`, read from their rows.

## Must read

The card's `Craft:` line cites each one, or says in one line why it skips it. `when` and `judge` are the labels in `SKILL.md`, "Rule labels".

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
| C690 | the People page lists only people she has met | — | the plan | note |
| C613 | his wanting shows on his body, seen by her, before he acts on it | — | something sexual shows | note |
| C639 | an offer has three to five graded answers, eager to refusing, every one written | — | a no is possible | note |
| C640 | a no is content; a no that returns to an unchanged menu was never a door | — | a no is possible | note |
| C961 | her no never raises a meter | — | a meter is shown or paid | note |
| C954 | see `craft/economy.md` |  |  |  |
| C447 | see `craft/voice.md` |  |  |  |
| C593 | see `craft/voice.md` |  |  |  |
| C644 | each person owns a corner of the world: their own subject, their own people offscreen | — | a person is on screen | note |
| C596 | the talk screen: about 55 words, two-thirds spoken, one picture, one exit | P13 reader pass 12: Mom's living-room talk ran 26 words, 42% spoken (a judgement on a borrowed number) | a person is on screen | note + talk, length |
| C656 | a per-person meter is short: median 3 steps | — · kept blocking: LO's choice (2026-11-24) | the plan | reader |
| C660 | each person's meter (one or two) is shown, each meter's word the same across the cast | — · kept blocking: LO's choice (2026-11-24) | a meter is shown or paid | reader |
| C448 | obvious on arrival: who a person is, what they want, how they feel about her, in the first lines | P13 reader pass 10: Ryan arrived as a bare name, never "step-brother" on screen | a first meeting | reader |
| C1340 | the household loop: each housemate is their face at their spot, Talk inside their menu, +1 a click | first_term_lean's `talk_mom`, a Talk button on the kitchen menu | a repeatable, a person is on screen | reader |

## The measures

Re-run 2026-11-22 in CoT (`/Users/a0000/Documents/Player_Legibility_Study_20260825/corpus/course-of-temptation/passages`):
- **Name before meeting.** The `anonorfullname` widget (`GlobalWidgets.txt`, line 882) prints the full name only when `setup.people.can_identify_name()` is true, and a description otherwise. It's called 953 times; the whole `anonor…` family (first name, full name, with relation, capitalised) is called about 3,050 times.
- **Graded answers.** `BusGrope.txt` offers "Encourage it", "Ignore it", "Push their hand away", "Smack that hand" and "Yell for help".
- **The no as content.** "That certainly backfired." (`EventResHallPropositionShowersBold.txt`).

Field-measured, from `lists/COVERAGE.md`'s evidence column and not re-run today:
- C618 and C619: 17 of 27 games carry meeting state; 14 games keep a flag per person; none of 209 characters is met at turn one. CoT's meeting flags live in its story JS, which the corpus doesn't hold.
- C613: Great Games Study round 6. C593 and C644: sluttown-usa and destroyer. C596: 15,774 of 54,630 screens. C656 and C660: 13 games. C690: 18 of 27 games. C598: CoT hides people she hasn't met.

## The shape

Each rule is marked **measured** or **LO's choice**.

1. **Nobody is met at the start except the people she lives with.** A meeting is one one-time scene that names the person and sets their met flag (C618, C619, C622, C627). *Measured in the field:* none of 209 characters is met at turn one.
2. **Until met, a person is a role or a description:** "the guy behind the counter". The name comes in the meeting; after it, both name and relation (C625, C626, C630, C632). *Measured:* CoT's `anonorfullname`, 953 calls.
3. **Unmet people are hidden** from cards, the People page and a place's presence lines (C598, C620, C690). *Measured:* CoT hides them; 18 of 27 games ship a page of met people.
4. **His wanting shows on his body, seen by her, before he acts** (C613). *Measured in the field.*
5. **An offer has three to five graded answers,** eager to refusing, every one written. A no lands somewhere: a reply, a return later, a cost (C639, C640). Her no never raises a meter (C961). *Measured:* CoT's `BusGrope` and "That certainly backfired."
6. **Each person has their own manner, their own subject and their own name for her** (C447, C593, C644). *Measured* for C593 and C644; C447 is *LO's choice.*
7. **A talk screen is about 55 words, two-thirds spoken, one picture, one exit** (C596). *Measured in the field.*
8. **One or two meters per person, each shown with its word, each with its own job, with few steps** (C656, C660). One is the field's common case (9 of 13 games); CoT gives every person two, friendship and lust (`<<friendship>>` 936 calls, `<<lust>>` 833 in round2/passages/course-of-temptation.txt): how close she is to him, and how much he wants her. In release 1 they are shown and don't move. *Measured in the field and in CoT;* two, and release 1, are *LO's choice.*
9. **Obvious on arrival** (C448). *LO's rule, not measured.*
10. **A person's actions are in their own menu, behind their face** (C1340). On the room screen the person is their face. Clicking it opens their menu: Talk, and whatever else she can do with them. None of it is a room button. Talk is once a day, and the person never locks: after Talk is used, the face still opens the menu, and the other options are still there. *Measured:* CoT's People Here list (`StoryCaption.txt`, lines 585-596) opens the person's card with "Talk to her" (`DisplayNPCWidgets.txt`, lines 33-68), and her own menu has 38 `<<link>>`s, 14 of them checked once a day against `$interactionstoday` (one at `InPersonDialogueMenu.txt`, line 77). Of 9 other top games, 5 put a person's actions behind the person: click the person (family-ties), one room button into her own menu (3, such as the-hellfire-club's "Speak to Daisy" in `DaisyRoom.txt`, line 18, into `Daisy_conv`), or her room is her menu (degrees-of-lewdity). The other 4 put each action loose on the room menu, shown while the person is there (lust-for-life's kitchen: "Approach Cory", `home-kitchen.txt`, line 15). Faces, not buttons, is *LO's choice* (relayed 2026-11-23: "Yes"), with CoT.

## The engine (cited; `v2.py` is `apps/game_generation/twee_comprehensive/generators/v2.py`)

- `npc = "npc_<x>"` on a canvas's trigger is read at `apps/projects/services/template_import.py:2581` and carried as the canvas's `npcId` (v2.py:15086-15088).
- A repeatable, manual canvas with an `npcId` shows as the person's face, not as a room button (v2.py:5925-5942; room buttons skip it at v2.py:5969 and 6680; the faces are drawn at v2.py:6530-6531).
- **One canvas per person per place.** The face opens the highest-`priority` canvas of that person there (v2.py:5944-5948). Two canvases for the same person in one room give one face, and the lower one never shows. So the person's menu is one hub canvas, and Talk and the rest are choices inside it.
- **Once a day, by a flag.** A choice sets a `_today` flag in its `flagEffects` and is shown only while that flag is false; `[engine.daily_tick]` clears it when the day rolls (v2.py:7162-7164; `.claude/skills/author-game-v2/references/engine.md:1458-1485`). The menu itself has no daily cap, so the person never locks.

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

On the kitchen screen: Mom's face, and the presence line "Mom's at the stove, humming." No "Talk to Mom" button among the room's.

Her menu, on a click:
> Mom looks up from the pan. "Hungry, or just here to steal bacon?"

Buttons: Talk (5 min, once a day) · Help her cook (15 min) · Leave her to it.

After Talk today, the face still opens the menu. Talk is gone until tomorrow, and Help her cook and Leave her to it are still there. The `talked_mom_today` flag clears at the day turn.

## Not this

- A Talk button per person on the room menu. The person is their face, and Talk is inside their menu (rule 10; C1340).
- A person who locks after one talk. Talk is once a day; the face and the rest of the menu stay (rule 10).
- A person named before the meeting. Until then, the guy behind the counter (C625).
- A meeting with one answer. Three to five, eager to refusing (C639).
- A no that returns to an unchanged menu. It lands somewhere (C640).
- A person listed at a place, or on the People page, before she has met them (C620, C690).
