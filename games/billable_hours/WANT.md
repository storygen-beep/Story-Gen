# The Want — Billable Hours

> One page, five parts. Doctrine: `.claude/skills/author-game-v2/references/the-want.md`.
> **Re-read this before every release.** Bump `want.last_read_at_release` in `v2_state.json`.
> Everyone in this game is eighteen or older, and every age is written below.

**Premise (LO picked "L", 2026-09-30).** Emma, 21, starts an internship at the law firm where her
stepfather Martin is a partner. He paid off her credit card, and she pays him back every payday.
Her mother Diane is his assistant at the same firm. At home is her stepbrother Ethan, a junior
associate who thinks she got the job because of Martin, and he is right. Her stepsister Jade quit
the firm to dance downtown and is happier than any of them. Losing the internship means losing
the house.

**Shape:** taboo at home, with a rise at work → `want.fantasy_shape = "mix: taboo_at_home + rise_by_want"`.
The house runs on who is in the next room; the firm runs on what she wants.

---

## 1. Who she is

Emma is 21 and has just finished college. She has no savings and no car, and her credit card is
paid off only because Martin paid it. She has the small back bedroom in Martin's house, across the
landing from Ethan. On Monday she starts a twelve-week internship at Callahan Reed, where Martin is
a partner, her mother sits outside his office, and Ethan has worked for two years.

**The places she knows:**
- `house`: the house, Martin's, in the suburbs.
- `firm`: Callahan Reed, the firm downtown.
- `club`: the Velvet Room, the club where Jade dances.
- `hotel_bar`: the hotel bar across from the firm, where the partners take clients.

**What she has to lose:** the internship, and with it the room. Martin's rule is simple: she lives
under his roof while she works at his firm. Beyond that, her mother's picture of her as the good
daughter. Diane got her this chance and would never forgive her for wasting it.

**The player:** `female` · `blank` · start choice: **approved by LO 2026-09-30**. The opening asks her
one thing it would ask anyway: when Ethan says "we both know how you got this job", does she say
*"I earned it"*, *"So what?"*, or nothing? That answer sets a flag, and his first scenes read it.
The alternative is `none`.

## 2. What holds her

**Every Friday, Martin takes $250 of her $350 week at breakfast.** He's at the table when she
comes down, the envelope goes across it, and he never raises his voice about it. The number goes up
twice, and he says it at breakfast when it does: $300 once she has paid $500 ("Your mother's card
was in your name too"), then $350 once she has paid $1,400, and then it stays there. **It never
finishes.** The internship's end review comes due in week twelve, and staying on means a full-time
contract Martin has to co-sign.

Money is written in `$`.

**Hold kind:** `bill` → `want.hold_kind`. Collector: `npc_martin` → `want.hold_collector`.
The second hold is `job`: Callahan decides at week twelve whether she is kept on. It is recorded
under `want.promise`, not as a second `hold_kind`.

⚠️ §4a: Martin collects the bill **and** is a target. That makes collector-as-target a deliberate
choice, and it is the one the skill tells you to make on purpose: *"Collector-as-target is a
legitimate design… The defect is doing it without noticing"* (`the-want.md` §4a). The porn does not
come down the bill: Friday in the study is the pressure, and his repeatable surface is somewhere
else. The lint `the collector is also the target` will print his share.

> **Amended 2026-09-30 (LO, at SP4):** the collection moved from "his study, after dinner" to
> breakfast, because the engine's rent page arms at 00:00 Friday (`engine.md` §26). The flat $3,000
> became a rising bill (`the-economy.md` R3b). Her pay is $350 a week, to match SP4. See
> `SKILL_TEST_FINDINGS.md` F4.

## 3. What she wants

**To be the one in the room nobody expected to matter, and to decide what it costs them to look.**
It can't finish: at work there is always a more senior office, and at home there is always a door
she hasn't opened yet.

**The charge:** taboo + transformation → `want.charge = "taboo + transformation"`.
- **Taboo** drives the house. Martin, Ethan and her mother are down the hall and across the landing.
- **Transformation** drives the firm. The intern who wore her interview suit on Monday is not the
  woman who closes Theo's file in the hotel bar in week ten.

## 4. How she climbs

**Early:** at the house, she knows Ethan can see through the bathroom door and she doesn't shut it.
She sits on the arm of Martin's chair while he reads her pay stub. At the firm, she stays late,
bends over the copier in front of the associates, and lets Theo buy the drink he offered on day
one. At the Velvet Room, she watches Jade work from the bar.

**Late:** Martin's study with the door locked while her mother sleeps upstairs. Ethan's room, and
then Ethan's desk at the firm after hours. Callahan's corner office the night before the review.
Theo's suite across the street. The Velvet Room's stage, on the night Ethan is in the crowd.

No numbers here. Tiers and rungs are set on the board.

## 5. The people

| person | age | what she wants from him / her | what he / she visibly wants, each visit | what he keeps score of |
|---|---|---|---|---|
| `npc_martin`: stepfather, partner at the firm | 52 | he paid for her and has never touched her, and she can't tell whether that is restraint or patience | the payment on time, and her to be grateful for it; his eyes stay on her a beat too long every Friday | **want + power** |
| `npc_ethan`: stepbrother, junior associate | 25 | he despises her for the shortcut, and she wants to watch him lose that argument with himself | her gone from the firm; and under it, her | **step counter + memory flags** |
| `npc_jade`: stepsister, dancer at the Velvet Room | 27 | Jade already did all of it and got out happy; she's the proof it can be done | company, a partner on the stage, and someone at home who isn't judging her | **step counter + memory flags**: companion, one step ahead |
| `npc_diane`: her mother, Martin's assistant | 49 | not wanted; **she is the price tag.** Every hour Diane is at her desk is an hour the house is unwatched | her daughter to succeed, so her own marriage looks like it was worth it | none: she's a system (her schedule), not a climber |
| `npc_callahan`: senior partner | 44 | he decides whether she is kept on, and he is the only man whose yes is worth a contract | results, and a reason to pick her over the other interns | **want + power** |
| `npc_theo`: client, a developer with a big account | 30 | he pays, and he pays her, not the firm | "private briefings" over drinks, and then upstairs | **step counter + memory flags** |
| `npc_pierce`: head of HR | 58 | he is the consequence. He doesn't want anything from her, and that makes him the one man she can't handle | a clean building; he keeps a file on who stays late with whom | none: a **risk** system, not a climber |

**LO approved 2026-09-30:** Pierce as a man, 58 (changed from "Mrs. Pierce" in the premise), and every `keeps` as proposed.

**Companion:** Jade (`want.companion`), one step ahead. **Pressure-man:** Martin (`want.pressure`).

---

## Before you leave this page

1. **What can she reach at the top that she cannot at the bottom?** At the bottom: glances, doors
   left open, a drink. At the top: Martin's locked study, Callahan's office before the review,
   Theo's suite, and the Velvet Room's stage in front of Ethan.
2. **Which person would a player miss if deleted, and what does he want back?** Ethan. He wants her
   gone and he wants her, and every scene with him is the fight between the two.
3. `python3 .claude/skills/author-game-v2/scripts/gates.py --words games/billable_hours/WANT.md`,
   output recorded at the phase handover.
