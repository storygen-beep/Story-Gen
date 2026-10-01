# Card — College (a system)

> **A worked card, not a template.** Take the shape, leave the furniture. Every line cites a traced game:
> round 9b, `round9b/cards/school.md` and `round9b/traces/school.md`, re-scoped to **Course of
> Temptation (CoT) only** (WS-D6: Cupid's Way is not a model here). Fill your own card on
> `templates/sheets/system.md`; record it in `board.systems[]`.
>
> ⚠️ **Adults only, and the game says so.** Everyone on campus is 18+, and the game states it. University
> words only — lecture, professor, campus, dorm, term, major. The banned word list is in `the-voice.md`
> ("Adult wording").

| field | the model (CoT) | cite |
|---|---|---|
| place and hours | 5 time blocks A–E of 2-hour lectures on weekdays; each course has a room in a named campus building; she takes 4 courses | `cot_31_database_school.js:162-190`, `:6-74` |
| cost | lecture time, plus homework and study minutes; a skill check on each homework (−10% if failed) | `cot_61_school.js:1082-1094`, `:762-767` |
| one ladder or two | **two that touch**: grades (pay) feed each professor's favor (lewd), and the lewd tasks lift grades | `cot_61_school.js:4-125` |
| pay ladder | grade = 40% homework + 60% exams, extra credit capped at +0.10; 14 letter rungs, **only 2 move money**: GPA below 2.5 raises the weekly bill 20%, GPA 3.8+ cuts it 20% | `cot_61_school.js:885`, `:910-915`; [WeeklyDebtPayment] |
| lewd ladder | grades raise favor (exam A +50, homework A +25, F −50 / −25); favor 100 and a last exam of 90%+ open extra credit: **24 live events in 5 chains of 3–5 rungs**; a classmate offers homework for cash or for sex (cash = 15% of the weekly bill; bought homework scores 90–100%) | `cot_61_school.js:4-125`; [ProfessorTalkExtraCredit]; [EventCampusHomeworkSellOffer] |
| people | a professor per course (the door); 1–2 classmates seated beside her every lecture; two classroom arcs (22 and 29 events) | `cot_61_school.js:597-617` |
| pool, daily | lecture pool **141 live events**; exam 13, study 21, leaving class 14, professor tasks 24; clicked every weekday | round 9b `cards/school.md` (comments stripped) |
| memory | lectures attended, homework, exams, GPA per course, extra credit, professor favor, a studious reputation | `cot_61_school.js:917-947` |
| growth | climbs by term (8 graded dates a year); a grade decays by neglect (no homework scores 0%) | `cot_31_database_school.js:241-294` |
| sink and deadline | the weekly bill, Monday from day 8 — the GPA moves it ±20% | [WeeklyDebtPayment]; round 9b `cards/money_pressure.md` |
| feeds · reads | feeds money (the bill), professor favor, the studious reputation · reads GPA and favor | `cot_61_school.js:4-125` |
| link into the hook | extra credit and the homework offer trade her body for grades | [EventCampusHomeworkSellOffer] |
| leads to | each professor; the seated classmates; the extra-credit scenes | [ProfessorTalkMenu] |

## Measured floors (directions, never gates)
- 2 money thresholds are enough; CoT has 14 letter grades and only 2 change the bill. A C student is safe,
  which is how CoT keeps lectures from becoming grind.
- A professor's lewd chain runs 3–5 rungs; the gate is a favor number that grades feed.
- 1–2 classmates seated per lecture.

## What players say
- A task is given and then lives nowhere visible: *"the option 'Do the special task' is just not shown"*
  (CoT, mopoga#164117). Put every issued task on a card with its place and time (`the-voice.md` R2).
- Lectures as grind: *"I just wish the cheats had a little more options. Like Skipping a day, or changing
  your grades"* (CoT, mopoga#76509). CoT answers with a paid or lewd shortcut past homework.

## Our engine today (round 9b §6)
- A weekly timetable is composable from schedule rows and conditions.
- A computed bill (±20% of an amount) is not built (`v2.py:15935`, "only 'random' is supported"); author
  fixed amounts per GPA band instead.
