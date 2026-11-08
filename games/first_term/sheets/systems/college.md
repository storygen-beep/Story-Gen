# [READY] System — college
> Changed 2026-11-08, LO's call ("Move to 80", DECISIONS 201): posing naked for the whole figure-drawing class opens at On Display (Exhibitionism 80), as Course of Temptation gates its art-class nude model; what shows sets the stage (DECISIONS 200). Signed by LO 2026-11-08.
> Signed by LO: LO, 2026-11-04.

> Changed 2026-11-03 to match the build (third alignment pass); signed by LO 2026-11-04. File and line cites removed.

> **Changed 2026-11-02** (reader fails a3, signed by LO 2026-11-02, DECISIONS 131): rows 19, 24–28, 42 (see `npc_bio_ta.md`, `npc_cocky_guy.md`, `college_class_figure.md`, `college_event_desk_guy.md`). The dress-code warning's skirt line is "Their eyes go to your bare thighs below the skirt, and away."

> **Changed 2026-11-01, re-signed by LO 2026-11-01** ("Signed", DECISIONS 113; design DECISIONS 99–112): the first college day and the timetable screen, from `proposals/R1_SYSTEM_COLLEGE_DAY.md` (signed 2026-11-01). Added: the opening hands her to the dean, the dean's office (one time), Hale's week-one window, the timetable screen (engine shipped, DECISIONS 112), the week-one card. Everything else as signed.

> Changed 2026-11-04 to match the build; signed by LO 2026-11-04. The 2026-10-29 locked-button note (DECISIONS 90) is corrected: "Needs Corruption 60" and "Needs Exhibitionism 60" are no longer in the game, because the buttons for scenes this release does not write were removed (DECISIONS 132). Any line below that still names one is superseded by that row.

> Signed by LO: LO, 2026-10-09 (changed 2026-10-08).

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
| what drives it | her two stages and her clothes pick the risky slot; grades pick office lines |
| link into the hook | her grades go home to Laura; failing brings the curfew |
| leads to | Hale, Nadia, the art lecturer, the Biology TA, the dean (met in his office on day 1) |
| day 1 | yes: the opening ends "Go to campus.", the dean's office, then Monday's first class (Hale's week-one window) |
| BRAKE | each class canvas fires once per class window, on its trigger |

## The timetable

| day | 08:30 | 10:15 | 13:00 |
|---|---|---|---|
| Mon | Psychology | Business | Biology |
| Tue | Figure drawing | Biology | Business |
| Wed | Psychology | Business | Figure drawing |
| Thu | Figure drawing | Biology | Psychology |
| Fri | Psychology | free | free |

**Rooms and lecturers** (checked 2026-11-01): every class is in
`lecture_hall`. Psychology is Dr. Hale, Business the Business lecturer, Biology the Biology TA, Figure drawing the art
lecturer.

## The first college day (new 2026-11-01)

**What was wrong** (LO, 2026-10-31): the first class was easy to miss (the class scene opens only in its first 15
minutes; the game starts Monday 07:00 at home and nothing walks her there), and the timetable was a
paragraph with no times taped to the hall door (`lecture_timetable`).

1. **The opening hands her to college.** The opening's last screen (`card`) ends with
   Laura: "You'll be late on your first day." Its button is **"Go to campus."** It walks her to the dean's office
   (15 minutes).
2. **The dean's office, one time, Monday of week one** (`dean_office`; the dean, 55, "what he visibly wants: to be
   obeyed"). Four short screens:
   1. He doesn't look up for a while. Then he does, and takes his time over her. In a short skirt, his signed line: "Is
      that what you wore to class?"
   2. The rules, his way: classes are not optional; two complaints and she's in this office again; "I don't like seeing
      a student twice."
   3. **He hands her the timetable.** It opens the timetable screen, Monday picked, Psychology marked "Next".
   4. "Psychology. Lecture hall. You're already late." Button: **"Go to Psychology."** It takes her to the lecture hall.
3. **Week one only, Hale's first lecture waits for her:** its window on Monday of week one runs 08:30–10:00, not 15
   minutes. She walks in late and the room turns to look. Every later class keeps the 15-minute rule.
4. **The dean is a seed:** his ladder (Zoe's later rung) is a later release. Here he is a man who watched her too long
   and a door she'll be sent back to.

**Against the taste columns** (an onboarding scene, not a heat step): who sees, the dean, then a full lecture hall
turning round · what she risks, being late on day one, the dean's second visit · his move, the look and the rules ·
what changes after, she has the timetable, the dean knows her name, the complaint rule is live.

## The timetable screen (new 2026-11-01)

- **One screen, like the people's schedule pop-up:** day chips across the top with today picked, then one row per
  class: the time · the class · the room · the lecturer.
- **Now and Next:** the class on now says **Now**; the next one today says **Next · in 25 min** (or "in 1 h 25 min"); a
  class already over today is dimmed.
- **Where it opens:** a **Timetable** button in the sidebar, after People · the dean's screen 3 · the lecture-hall door
  (the door's paragraph is replaced by the button).
- **One source of truth:** the build writes the `[[ui.timetable]]` rows from the same `PSYCH`, `BUSI`, `BIO`, `FIG`
  schedules the class scenes use, so the screen can't disagree with the classes.
- **Engine (shipped 2026-11-01, DECISIONS 112):** `[[ui.timetable]]` rows (class, place, lecturer, weekdays, from, to),
  drawn by `setup.timetableHtml(day)` and opened by `setup.openTimetable(day)`; `[ui] timetable_button = true` adds the
  sidebar button. Opening it from the dean's screen and the door
  needs a link that runs `setup.openTimetable()`: check at build how a canvas button runs it.

## The card

Week one's goal: "Go to your first class: Psychology, **08:30**, in the lecture hall." (today it has no time).

**Not decided here:** whether missing a class costs anything this release (signed as "a lecturer's warning; again, a
complaint"). Proposed: as signed.

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
| 4 · Hungry · Watched | locked in 0.1; the button says "Needs Corruption 60" | under the desk with the class there |
| 5 · Shameless · On Display | a later release | posing nude for the whole figure-drawing class (Exhibitionism 80; LO, 2026-11-08) |

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
| Zoe sits in Biology and figure drawing, and Jake in figure drawing: they get class rows (ledger change L27) | sweep A5-11 |
