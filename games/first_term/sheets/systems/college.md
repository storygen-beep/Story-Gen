# [READY] System — college

> Signed by LO: LO, 2026-10-08.

> Placed in sheets/ 2026-10-08. Written 2026-10-08 from SYSTEMS §1 and the ledger's `college` card.
> Every number marked "guess" is new here and waits for your yes.

| row | answer |
|---|---|
| id · name | `college` · College |
| place and hours | `lecture_hall` · Monday to Friday, three classes: 08:30, 10:15, 13:00 |
| class length | 90 minutes each · Friday has one class, Psychology at 08:30 |
| offices | the faculty floor, 14:30–18:00 · Hale's office also Thursday 17:00–19:30 |
| cost | a class slot of 90 minutes · Focus spends energy, Doze gives a little back |
| one ladder or two | two that touch: grades open office lines; Hale's sessions lift a grade |
| people: staff | Hale, the art lecturer, the Business lecturer, the Biology TA, the dean |
| people: students | Nadia, Zoe, Jake · four classmates · the figure-drawing model |
| pool | 8 canvases, below · `daily = true` |
| memory | four grades, intelligence, exam flags, complaints, probation, the letter home, the curfew |
| growth | climbs |
| sink and deadline | no money · the deadlines are exams: midterms in weeks 7–8 |
| feeds | the four grades, `intelligence`, `complaints`, `campus_talk`, `laura_suspicion` |
| reads | energy, what she wears, Corruption, Exhibitionism, `intelligence` |
| what drives it (S8) | her two stages and her clothes pick the risky slot; grades pick office lines |
| link into the hook | her grades go home to Laura; failing brings the curfew |
| leads to | Hale, Nadia, the art lecturer, the Biology TA, the dean |
| day 1 | yes: Monday's first class is the opening day |
| BRAKE (S9) | each class canvas fires once per class window, on its trigger |

## The timetable

| day | 08:30 | 10:15 | 13:00 |
|---|---|---|---|
| Mon | Psychology | Business | Biology |
| Tue | Figure drawing | Biology | Business |
| Wed | Psychology | Business | Figure drawing |
| Thu | Figure drawing | Biology | Psychology |
| Fri | Psychology | free | free |

## A class visit — the rows

| row | effect, with op | lands on a screen? |
|---|---|---|
| Focus | energy add −10 · that grade add +2 · `intelligence` add +1 (all guess) | yes, one short screen |
| Chat | a line from whoever sits beside her · nothing moves | yes |
| Doze | energy add +5 (guess) | yes, short: her body, never a toast |
| Skip | that grade add −2 (guess) · she keeps the 90 minutes | a toast is fine |
| the risky slot | grows by stage; Exhibitionism or Corruption add +1 (small act) | yes, always: it is her body |

**The lock.** Under 20 energy (guess), Focus is shut: *"Too tired to focus. Doze, or skip."*

## Pool (`pool[]`)

| canvas | what it is | explicit? | what drives it | brake |
|---|---|---|---|---|
| `college_class_psych` | Psychology: Hale lectures, Nadia beside her | no | her stage, her clothes | once a class window |
| `college_class_business` | Business: the strict man, the rival, the study guy | no | her stage, her clothes | once a class window |
| `college_class_bio` | Biology: the shy TA, Zoe, the cocky guy | no | her stage, her clothes | once a class window |
| `college_class_figure` | Figure drawing: the class draws a nude model | yes: the model, nude | her stage | once a class window |
| `college_event_desk_guy` | the guy beside her, hard, asks for help | yes at Bold | Corruption | once a day |
| `college_event_dress_code` | a lecturer's warning about what she wears | no | what she wears | once a day |
| `college_exam` | the midterm: focus, or copy | yes at Curious: the flash | `intelligence` + that grade | once per exam |
| `college_office_talk` | each office's talk hub | no | that grade, her clothes | once a day per office |

Events pick at random among those open, and an event she has seen is weighted down.

## Pay ladder — the grades (`pay_ladder[]`)

| rung | gate | pay |
|---|---|---|
| 1 · failing | that grade under 40 (guess) | Laura reads it; low Warmth sets the curfew; a week on, probation |
| 2 · fine | 40 to 69 (guess) | the curfew lifts; the office hub reads it |
| 3 · top | 70 or more (guess) | the grade goes home as good news (Hale B 5) |

Every grade starts at 50 (guess). The exam result reads `intelligence` plus that grade.

## Lewd ladder (`lewd_ladder[]`) — what ships in 0.1

| rung | gate | acts |
|---|---|---|
| 1 · Good Girl · Covered | none | the dropped pen, an accident · the dress-code warning |
| 2 · Curious · Daring | Exhibitionism or Corruption gte 20 | a flash for Hale (Hale B 2) · she watches the guy beside her |
| 2, continued | the exam only | flirting for the study guy's paper · a flash for the cocky guy's answers |
| 3 · Bold · Showing | Corruption gte 40 | a touch in Hale's office (Hale B 3–4) · her hand under the desk, unseen |
| 4 · Hungry · Watched | locked in 0.1; the button says "Needs Hungry" | under the desk with the class there · posing nude for the class |

**Waiting for 0.2** (SP5): the art lecturer's posing, the Biology TA, and the dean's route.
In 0.1 the three of them are talk hubs with one line on her grade and one on her clothes.

## The failing chain

| step | what happens | key, with op |
|---|---|---|
| a grade lands in failing | Laura reads it at home | `laura_suspicion` add +5 |
| Laura's Warmth is low | a curfew: no party, no late shift, no Saturday date | `curfew` set true |
| a week passes | the curfew ends; it starts again if still failing | read by days since set, 7 |
| still failing a week after the result | probation: the dean's first warning | `on_probation` set true · `dean_summons` set |
| a complaint (dress code, the rival) | the dean reads the count | `complaints` add +1 |
| after the warning | a letter home | `letter_home` set true · `laura_suspicion` add +10 |

The house at night stays open under the curfew. The door out says why it is shut.

## The meters it writes and reads (`board.meters[]`)

| meter id | kind | key | fed at | read by |
|---|---|---|---|---|
| grade_psych, _art, _business, _bio | sourced | four traits | `lecture_hall` | Laura, the lecturers, Mark, the dean |
| intelligence | sourced | `intelligence`, only goes up | `library` (and Focus in class) | every exam result |
| complaints | sourced | `complaints` | `lecture_hall` | the dean: the warning, then the letter |
| campus_talk | sourced | `campus_talk` | `canteen` | who approaches her · feed posts |
| laura_suspicion | sourced | `laura_suspicion` | `home_hall` | her catch lines; the curfew at 50 (Laura's sheet) |
| corruption · exhibitionism | sourced | her two meters | here, among others | every stage choice in the game |

## Rows a gate needs

| row | gate |
|---|---|
| Focus shut under 20 energy | a need shuts a door |
| the card is filled | every system has a card |
| leads to Hale, Nadia and the lecturers | leads to a person |
| every grade and `complaints` has a reader | a meter is read |
| the curfew flag is set and read | milestones open something |
| pool has 8, not 20 | a system meets its floors (a warning; decisions, question 9) |

## Why — the source of each key choice

| key choice | source |
|---|---|
| four subjects, the timetable | LO, chat 2026-10-06/07 (SYSTEMS §1) |
| class hours | LO, 2026-10-08 (SP1) |
| Focus · Chat · Doze · Skip, and the risky slot | LO, chat (SYSTEMS §1) |
| the failing chain and the curfew | LO, chat 2026-10-06 (SYSTEMS §1) |
| no Hungry class moments in 0.1 | LO, 2026-10-07 (SP7 call 1) |
| lecturers' and dean's acts wait for 0.2 | LO, 2026-10-07 (SP5) |
| grade bands 40 / 70, start 50 | guess |
| energy and grade moves per row | guess |
| the energy lock at 20 | guess |
