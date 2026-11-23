# craft/voice.md — the voice, aligned with Course of Temptation

Read this before you write any card with prose on it. It replaces reading v2's `register.md` "The voice — say it loud" (LO, relayed 2026-11-22: "Remove thoughts in itallic. Dont show in body too." · "Does Cot shows feelings??" · "Lets align it with Cot"). The truth rule stays in v2's `register.md` "The truth rule" until it's ported here in full (`reader.md`).

## Must read

The card's `Craft:` line cites each one, or says in one line why it skips it.

| id | what it asks | the failure it stops |
|---|---|---|
| C442 | say it, don't hint it: tell the player what is happening | — |
| C449 | name the sexual tension; don't bury it | — |
| C451 | keep the concrete detail: places, objects, money, times | — |
| C447 | every person sounds like themselves: one manner each, held | — |
| C593 | one term of address per person that nobody else uses | — |
| C448 | obvious on arrival: who a person is, what they want, how they feel about her, in the first lines | — |
| C450 | end a scene on a hook that points at what happens next | P13 ended on "go to breakfast" |
| C422 | labels, room names and cards say plainly what clicking does | — |
| C460 | the truth rule: every claim is true on every playthrough that can reach the screen | — |
| C461 | what's allowed under it: texture that can't clash, her opinions, dialogue that fits the cast entry | — |
| L163 | a rule removed needs the same proof as a rule added, measured the way the player sees it | a quotes-only count once deleted a correct dialogue rule |

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
5. **People speak in most scenes, and narration leads,** under 5 : 1 on a scene with someone in it. *Measured:* CoT 3.92 : 1, DoL 3.23 : 1, Hellfire 1.87 : 1; field median 2.93 : 1 over 27 games, gate `somebody speaks` ≤ 5 : 1 (`.claude/skills/author-game-v2/references/register.md:57`, `.claude/skills/author-game-v2/references/register.md:658`). This drops C446 ("more dialogue than narration"), which none of the measured top games does. A scene she is alone in needs no speech.
6. **Say what happens plainly and name the sexual tension** (C442, C449), and keep the concrete detail (C451): the bolt, the small towel, the time. *LO's choice:* the loud voice is "a decision made against the field" (`.claude/skills/author-game-v2/references/register.md:15-17`).
7. **True on every visit** (C460, C461). A line about the past shows only behind the flag that records it; who it says is there is there. *LO's choice,* kept in practice by CoT's macros above.
8. **Each person sounds like themselves,** with one term of address that nobody else uses (C447; C593 is *measured:* 5–18% of lines in two games). **Obvious on arrival** (C448), **end on a hook** (C450), **labels plain** (C422): *LO's rules, not measured.*

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
