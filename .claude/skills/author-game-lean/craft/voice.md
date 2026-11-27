# craft/voice.md — the voice, aligned with Course of Temptation

Read this before you write any card with prose on it. It replaces reading v2's `register.md` "The voice — say it loud" (LO, relayed 2026-11-22: "Remove thoughts in itallic. Dont show in body too." · "Does Cot shows feelings??" · "Lets align it with Cot"). It also carries the truth rule in full ("The truth rule", below), ported from v2's `register.md` so the writer and the reader read the same text (LO, relayed 2026-11-24: the P13 reader found a new truth FAIL on every pass from v5 to v11, and the writer had only this file's headline row).

## Must read

On a card with a `Does:` block (every card from 2026-11-24 on), the rows that apply come from `check.py --rules`, which lists each with its craft file; the card has no `Craft:` line (`piece.md` step 2). On a card from before 2026-11-24, the `Craft:` line cites each one, or says in one line why it skips it. `when` and `judge` are the labels in `SKILL.md`, "Rule labels".

| id | what it asks | the failure it stops | when | judge |
|---|---|---|---|---|
| C442 | say it, don't hint it: tell the player what is happening | — · kept blocking: the voice, LO's (2026-11-22) | always | reader |
| C449 | name the sexual tension; don't bury it | — · kept blocking: the voice, LO's (2026-11-22) | something sexual shows | reader |
| C451 | keep the concrete detail: places, objects, money, times | — · kept blocking: the voice, LO's (2026-11-22) | always | reader |
| C447 | every person sounds like themselves: one manner each, held | — · kept blocking: the voice, LO's (2026-11-22) | a person is on screen | reader |
| C593 | one term of address per person that nobody else uses | P13 reader pass 7: Mark had no term of address for her (Mom "baby", Ryan the nickname) | a person is on screen | reader |
| C448 | see `craft/people.md` | | | |
| C450 | end a scene on a hook that points at what happens next | P13 ended on "go to breakfast" | a scene's last screen | reader |
| C422 | labels, room names and cards say plainly what clicking does | — · kept blocking: the voice, LO's (2026-11-22) | always | reader |
| C460 | the truth rule: every claim is true on every playthrough that can reach the screen | P13 reader pass 11: Mom's "promise me it won't be like high school", on the screen all three start choices leave from | always | reader + presence, sheet, creation |
| C2202 | a scene that repeats says nothing true only once: no first-meeting words ("new face", "say your name") and no "next time I'll" promise, unless a group holds the line on a flag's is_false side | first_term_lean: Mr. Cross's daily Talk said "New face… Say your name" and "Next rehearsal, you're on the stage" every day; the café shift said "Next time I'll let you near the machine" every shift (LO, typed in main-lean 2026-11-27) | a repeatable | script + repeats |
| C461 | what's allowed under it: texture that can't clash, her opinions, dialogue that fits the cast entry | — · kept blocking: the truth rule | always | reader |
| L163 | a rule removed needs the same proof as a rule added, measured the way the player sees it | a quotes-only count once deleted a correct dialogue rule | a rule is changed | reader |

## The measures (re-run 2026-11-22)

Sample: about 280–300 random scene passages per game from `/Users/a0000/Documents/Player_Legibility_Study_20260825/corpus/<game>/passages`, counted inside quote marks. That count is valid for these three games, which all put speech in quote marks (`.claude/skills/author-game-v2/references/register.md:640-646`; L163). The word lists are rough.

| game | scenes with speech | narration : dialogue | narration sentence, median | italic markup |
|---|---|---|---|---|
| Course of Temptation (CoT) | 68% | 3.92 : 1 (whole game 4.57 : 1, `.claude/skills/author-game-v2/references/register.md:644`) | 10 words | 27 of 4,066 event passages have an italic span of 4+ words outside speech |
| Degrees of Lewdity | 76% | 3.23 : 1 | 8 words | 2% of the sample |
| The Hellfire Club | 91% | 1.87 : 1 | 14 words | 3% of the sample |

CoT, by exact phrase, across its passages:
- her feeling on her body: "You blush" 76, "you feel your face heat" 5, "Your cheeks burn" 3, "you feel your stomach drop" 2;
- her feeling named: "You feel embarrassed" 1;
- others on the body: "looks away" 11; named: "seems nervous" 0;
- arousal on her body: "a thrill of arousal" 7, "an ache between your" 3;
- the truth rule in practice: 10,992 `<<conj>>`, 5,411 `<<ps>>` and 4,928 `<<pp>>` pronoun and name macros.

## The shape

Each rule is marked **measured** (with its numbers) or **LO's choice**.

1. **Second person, short sentences.** About 10 words a narration sentence. *Measured:* CoT 10, DoL 8, Hellfire 14; the field's median is 10 over 17 games (`.claude/skills/author-game-v2/references/register.md:753-758`). CoT has "you" 70 times per 1,000 words.
2. **Feelings show on the body,** hers and everyone else's: "your cheeks burn", "your stomach drops", "his ears go red", "she looks away". Naming a feeling ("you feel embarrassed") is rare: about once where the body carries it a hundred times. *Measured:* the CoT counts above.
3. **Arousal is always on her body:** her nipples, the heat between her legs, her breath. *LO's choice,* matched to CoT ("a thrill of arousal", "an ache between your").
4. **No italic thoughts,** not in their own line and not inside the prose. What she thinks goes on her body, in the narration, or out loud to the person in front of her. *LO's choice,* matched to CoT (under 1% of its event passages). This drops C444 (thoughts in italics, `thought_bubble`).
5. **People speak in most scenes, and narration leads,** under 5 : 1 on a scene with someone in it. *Measured:* CoT 3.92 : 1, DoL 3.23 : 1, Hellfire 1.87 : 1; field median 2.93 : 1 over 27 games, gate `somebody speaks` ≤ 5 : 1 (`.claude/skills/author-game-v2/references/register.md:57`, `.claude/skills/author-game-v2/references/register.md:658`). This drops C446 ("more dialogue than narration"), which none of the measured top games does. A scene she is alone in needs no speech. How to count: words in `dialog` blocks, and words inside quote marks in a paragraph, are speech; everything else on the screen is narration. Where a screen has variants, count the one that leans most on narration. Count only the screens with someone else in them: a line from them, a presence check for them, or their name or role in the prose. In a chain of variants, someone is there only in the variant that has them, so a variant with nobody in it is not counted as company. Count each path through the scene, from its first screen to where it leaves, and every path stays at or under 5 : 1. `check.py` counts it (`talk`).
6. **Say what happens plainly and name the sexual tension** (C442, C449), and keep the concrete detail (C451): the bolt, the small towel, the time. *LO's choice:* the loud voice is "a decision made against the field" (`.claude/skills/author-game-v2/references/register.md:15-17`).
7. **True on every visit** (C460, C461): "The truth rule", below. *LO's choice,* kept in practice by CoT's macros above.
8. **Each person sounds like themselves,** with one term of address that nobody else uses (C447; C593 is *measured:* 5–18% of lines in two games). **Obvious on arrival** (C448), **end on a hook** (C450), **labels plain** (C422): *LO's rules, not measured.*

## The truth rule

Ported from `.claude/skills/author-game-v2/references/register.md:89-156`, with these changes for this skill: her opinions go on her body or out loud (rule 4 here, no italic thoughts); the schedules are read with `scripts/who_is_where.py`; and one line in rule 2 and step 7 is new, from P13's reader pass 11 (2026-11-24): Mom's "promise me it won't be like high school", on the screen all three start choices leave from, assumed a bad high school that the grades answer ("It'll be the same") then called good. v2's step 7 (write the facts list at the top of the draft) is dropped: the card is the draft.

**Loud writing makes claims.** "She hasn't slept." "You didn't eat last night." Every claim has to be true on every playthrough that can reach the screen. The first loud rewrite of a real scene in v2 had five lines and five defects: the wrong clothes for the hour, two pasts the player may not have had ("last night" on what could be day one), one line out of character, and one printed stat that doesn't exist.

| allowed | not allowed |
|---|---|
| texture that can't clash with anything: the kettle, a pet name, the oil in the pan | anything that contradicts the design: clothes, times, who is where |
| her opinions, on her body or said aloud | a past about her that no flag records: "you came last night", "you did this again". "Again" alone on a repeatable is fine ("he wants you again") |
| dialogue that fits the person's entry in the plan | behaviour the plan rules out for them |
| a consequence on a button when a real flag or number sits behind it | a "+X" for a number that doesn't exist (`craft/meters.md`) |

**The five rules.**

1. **Every fact line is checked** against the plan and the schedules: who is there, what they wear, what time it is, what day, at every minute it can show. Run `who_is_where.py` for every line that puts a person somewhere.
2. **A line about the past shows only behind the flag or count that records it,** in a group whose conditions read it. "You're late again" is true inside `late_count gte 1` and a lie outside it. A meter many scenes raise records no one event. A line on a screen every path reaches can't assume a past or a fact that only one path makes true.
3. **A big moment is a one-time step, not a repeatable** (C146). A repeatable plays every visit, so it can't carry a reveal.
4. **A consequence on a button is a real flag or number,** or it goes into the plan first.
5. **Prose names her clothes only where a clothing condition, an earlier equip, or the beat that equips her backs it** (C1158; `craft/clothes.md` rule 4).
6. **A scene that repeats says nothing that is true only once** (C2202). First-meeting words belong to the meeting, which plays once: "new face", "new girl", "say your name", "nice to meet you". A promise of what happens next time ("Next time I'll show you", "Next rehearsal, you're on the stage") is renewed on every visit and broken on every visit after, unless the game builds it: then it sits in a group on the payoff flag's `is_false` side, so it stops once it comes true. A nickname that means new ("rookie", "new girl") is a first-week word: hold it on a count or a flag, or let it go. *Measured in the field* (2026-11-27, `~/Documents/Great_Games_Study_20260926/cot_design_study_20261125/TALK_FIRST_AND_REPEAT_STUDY_20261127.md`): of five pass-list games, the two whose first talk plays once and then moves on (Shady Deals, step 0 at `shady-deals.txt`, line 11387; New Lust, `AshleyPresentation.txt`, line 31) never repeat a first meeting; one without it repeats "lucked out in the roommate situation" every chat (`in-her-own-hands.txt`, line 5724). A repeat makes a promise only when a timer keeps it: Shady Deals prints the real wait in the line (`shady-deals.txt`, line 8425). CoT's daily Chat makes none (`InPersonDialogueHobbies.txt`, lines 1-22).

Who judges each rule: 1 is the reader's, helped by `presence` and `sheet` (who is where, the clock, the place); 2 to 5 are the reader's, and 5 is helped by `sheet` (what she wears); 6 is `repeats` for a person's spoken words, and the reader's for narration and for a promise the pattern misses ("Wednesday at eleven, I'll call on you first"). Rules 1, 2, 4 and 5 apply always (`when`); rules 3 and 6 apply on a repeatable.

**A promise about the future must be built.** A line that names a future event ("next month he decides") is true only if the game builds it, or the plan has the step that reaches it. Otherwise cut the line, or drop the date.

**How to check a scene: seven steps.**

1. List every time the scene can show: its trigger, and each person's rows on every weekday. A scene that can show at 09:00 on a Saturday can't say "tonight" (`craft/clock.md`).
2. List every claim: times, clothes, who is where, what the past was, what someone knows.
3. Check each one against a source: `PLAN.md`, the other cards, and `who_is_where.py`.
4. A claim true only sometimes gets a condition or a variant. With neither, cut it.
5. Check each person's lines against their entry in the plan, including how they say no and what they never do.
6. Check each printed consequence against the button's real effects.
7. Read each screen on every path into it and out of it: a line every path shares is true on all of them, and each answer still fits what was said before it.

**One line, wrong and right.** On a repeatable scene:
- Wrong: "Late again. Third time this week." True on the third visit, a lie on the first.
- Right: the same line inside a group on `late_count gte 3`, with "You're late. Apron's on the hook." as the fallback.

And for rule 6, on a person's daily talk:
- Wrong: "New face. Say your name. Next rehearsal, you're on the stage." A first meeting and a promise, every day.
- Right: "Sit, watch, learn something. Drama's Tuesday at eleven." True on day 2 and day 40, and the time is his real class.

## Worked example

Roles: her step-brother, who has a nickname for her. LO approved these words, with the names swapped for roles. Word counts are for the story text.

**The bathroom** (71 words)
> The water finally runs hot. You stand under it with your eyes shut and let it run down your neck, over your tits, down your stomach and between your thighs. Your shoulders drop for the first time all morning.

Picture: her in the shower, water running down her. gif.

> Then a fist bangs on the door.
> Step-brother: "<nickname>. Some of us need that too."
> Your heart jumps. The bolt doesn't hold. You grab the towel off the rail. It's the small one.

Button: Open the door.

**The hall** (103 words)
> Steam rolls out into the hall. Your step-brother is leaning on the wall across from you, shirtless, half asleep, a towel over his shoulder. He's broader than you remember.
> His eyes drop to your towel, to where it ends on your wet thighs. One second. Then he catches himself and stares at the ceiling. His ears go red.
> Step-brother: "Shit. Sorry. First day, huh?"
> Your face goes hot. Your step-brother just looked at you the way a guy looks at a girl. Your nipples are hard against the towel, and you can't tell if it's the cold.
> The knot at your chest is slipping.

Buttons: Hold the towel and squeeze past him · "All yours." · Fix the knot first.

What it shows: feelings on the body (her heart, her face, her nipples; his ears), no italic line, his one spoken line inside narration that leads, the tension named ("the way a guy looks at a girl"), concrete detail (the bolt, the small towel), and a hook (the knot).

## Not this

- An italic thought: "*Did he just... no. Ryan doesn't look at me like that. Does he?*" (first_term_lean's opening, `games/first_term_lean/toml_phases/5_scenes.toml:165`). Put it on her body: her face goes hot.
- A named feeling where the body would carry it: "You feel embarrassed." Write what her face does.
- "More dialogue than narration" as a rule. Narration leads in every measured top game; people still speak in most scenes.
- A thought standing in for a conversation. If a person is there, she says it to them.
