# [READY] Release 1 system 4 — the first college day and the timetable screen

> Signed by LO: LO, 2026-11-01 ("Signed."). Step 4 of the release-1 redesign (DECISIONS 99–104), system 4 of 4.
> Changes the signed `sheets/systems/college.md`, `sheets/people/npc_dean.md` and the opening's last screen;
> on LO's sign they are rewritten to match and re-signed.

## What's wrong today (LO, 2026-10-31)
- **The first class is easy to miss.** Psychology is Monday, Wednesday and Friday 08:30–10:00
  (`iterations/002/build_scripts/college.py:17`). The class scene opens only in its first 15 minutes
  (`at_start`, `college.py:22-28`). The game starts Monday 07:00 at home (`0_systems_spec.toml:20-21`); the
  opening runs about an hour and ends in the kitchen; campus is 15 minutes on foot. Nothing walks her there.
- **The timetable is a paragraph** taped to the lecture-hall door, with no times
  (`lecture_timetable`, `college.py:465-476`): "Monday: Psychology, Business, Biology. …"
- LO: "before that we need a one time canvas like in college this is your first day maybe at the dean's
  office. You can look at the timetable. And timetable is also hard to understand as the text only. I say we
  can have a custom screen for it like a table like npc schedules but in that screen itself."

## The design

### 1. The opening hands her to college
- The opening's last screen (`card`, `toml_phases/2_one_shots.toml:502`) ends with Laura: "You'll be late on
  your first day." Its button is **"Go to campus."** It walks her to the dean's office (15 minutes).

### 2. The dean's office: one time, Monday of week one
- **The dean** (55, signed: "what he visibly wants: to be obeyed", `sheets/people/npc_dean.md`). His office
  (`dean_office`, already in the map).
- What happens, in four short screens:
  1. He doesn't look up for a while. Then he does, and takes his time over her. If she's in a short skirt,
     his signed line: "Is that what you wore to class?"
  2. The rules, his way: classes are not optional; two complaints and she's in this office again; "I don't
     like seeing a student twice."
  3. **He hands her the timetable.** It opens the timetable screen (below), Monday picked, Psychology
     marked "Next".
  4. "Psychology. Lecture hall. You're already late." Button: **"Go to Psychology."** It takes her to the
     lecture hall.
- **Week one only, Hale's first lecture waits for her:** its window on Monday of week one runs 08:30–10:00,
  not 15 minutes. She walks in late, and the room turns to look (a witness, on day one). Every later class
  keeps the 15-minute rule.
- The dean is a seed: his ladder (Zoe's later rung, "fucking the dean") is a later release. Here he is a man
  who watched her too long and a door she'll be sent back to.

**Against the taste columns** (an onboarding scene, so it is not a heat step; the columns that fit):
- **who sees:** the dean, then a full lecture hall turning round.
- **what she risks:** being late on day one; the dean's second visit.
- **his move:** the look, and the rules.
- **what changes after:** she has the timetable; the dean knows her name; the complaint rule is live.

### 3. The timetable screen: a real table
- **One screen, like the people's schedule pop-up** (`setup.castScheduleHtml`, `generators/v2.py:11856`,
  DECISIONS 96): day chips across the top with today picked, then one row per class.
- **Each row:** the time · the class · the room · the lecturer. Example for Monday:

  | time | class | room | lecturer |
  |---|---|---|---|
  | 08:30–10:00 | Psychology | Lecture hall | Dr. Hale |
  | 10:15–11:45 | Business | … | … |
  | 13:00–14:30 | Biology | … | … |

- **Now and Next:** the class on now is marked **Now**; the next one today is marked **Next**, with "in 25
  minutes". A class she has already missed today is dimmed.
- **Where it opens:** a **Timetable** button in the sidebar (next to the phone clock) · the dean's screen 3 ·
  the lecture-hall door (the door scene's paragraph is replaced by the button).
- **One source of truth:** the build writes the timetable rows from the same `PSYCH`, `BUSI`, `BIO`, `FIG`
  schedules the class scenes use (`college.py:17-20`), so the screen can't disagree with the classes.

### 4. The card says it
- Week one's goal: "Go to your first class: Psychology, **08:30**, in the lecture hall." (Today it has no
  time: `0_systems_spec.toml:498`.)

## Engine and build work (for after the sign)
- **Engine (v2.py):** `setup.timetableHtml(day)` modelled on `setup.castScheduleHtml` (same Dialog, same day
  chips), reading a declared `[[ui.timetable]]` list (class, place, lecturer, weekdays, from, to); a
  `[ui] timetable_button = true` sidebar button; no change for a game that doesn't declare it (Vesper).
- **Build:** `college.py` writes the `[[ui.timetable]]` rows from its schedules; the dean canvas; the Monday
  week-one window on Hale step 1; the opening's last button.
- **Check before building:** the rooms and lecturers of Business, Biology and Figure drawing (from their
  place and person sheets) for the table's columns.

## Not decided here
- Whether missing a class costs anything this release (the dean's complaint rule is signed as "a lecturer's
  warning; again, a complaint"). Proposed: as signed.
