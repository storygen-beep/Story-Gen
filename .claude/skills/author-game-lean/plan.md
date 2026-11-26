# plan — the game plan in bites, then the release's piece list

A new game starts here. The plan is written in `games/<slug>/PLAN.md` from `templates/PLAN.md`, one bite at a time, in the order below. Show each bite to LO in chat and take his answer before the next one. Record each answer in `NOTES.md` in his words, with the date. For a bite's craft beyond its must-read ids, grep its area in `lists/COVERAGE.md`.

**The plan's rules.** Before the first bite, and again before each release's piece list, run `venv/bin/python .claude/skills/author-game-lean/scripts/check.py --rules games/<slug> plan`. It prints every craft rule whose `when` is "the plan": the ones that design a whole system (the bill, the clothes states, the meters' stages, the heat floor across the game). Write the bites and the piece list to them. The reader does not judge these yet: no script or reader pass reads a plan, so they hold only as far as the writer and LO read them (LO, relayed 2026-11-24: "Yes").

**Every bite starts from what LO has already named.** Place everyone and everything he named, then point out the gaps. Never re-propose or drop something he named. (NOTES gap "the people bite took only the starting core", 2026-11-20.)

## 1 · Her

Who she is: her age (18 or older, and written), her situation at minute zero, written character or blank slate, and **the narration person**, declared here, once, for the whole game (`[settings] narration_person`; second person is the genre standard).

Must read: C39, C42, C54, C548, C503, C605.
Why: first_term_lean's P01 never declared the narration person, and it came up on P02. (NOTES gap "P01 never declared `[settings] narration_person`", 2026-11-20.)

## 2 · The want

The one-page want: the fantasy shape, the hold (and who enforces it), the goal with its flag and the goal after it, the mystery, the rival, the appetite as a destination, and the ascent as a sentence about doors.

Must read: C25, C26, C28, C33, C35, C36, C55, C58, C60, C65.

## 3 · The people

The cast the want needs: for each person, what she wants from them, and their age. Under the people system (`craft/people.md` rules 8 and 13), first the game's **type table**: each type with its start friendship, lust and control, and the trait words it draws from. Then each person: their type, gender, attracted (yes or no), their 2–4 trait words with the line that shows each, any start value tuned by hand, and a hand-set want only when the story fixes it. A professor is marked, with intimacy 0. **The trait words are the game's own**, plain words, the author's brief for the person's scenes; the player never sees them (`show_traits = false`). Draft the game's list here, and LO approves it; the skill's worked list (`craft/people.md` rule 13) is an example, not a default (C2193; LO, typed in main-lean 2026-11-26: "Hide them dont show them, they are for us, to design the npc scenes and all, dont have to show to a player."). Give each person two lines: **where they end up** (their want, the top of their arc) and **where they are now**, at the start. They are not the same, and a reader who sees only the end takes it as the start. (LO, relayed 2026-11-21: "in the starting ryan doesnt want her.") When the session proposes a person who has no reason to exist, it cuts that proposal. Someone LO named is never cut.

Must read: C584, C597, C605, C606, C608, C609, C2177, C2178, C2193.

## 4 · The places

Derive the places from needs, systems and people; never pick a number. Name each place for what it is. Give each destination its dramatic job: why she goes there when nothing is happening. Declare the layout: which place opens into which. A floor plan left to a guess breaks the flags that depend on it.

Must read: C735, C737, C738, C741, C761, C776, L33, L39.

## 5 · The people pass, place by place

Go place by place, one area per bite. Start from everyone LO has named so far, place each of them, and never drop one. For each place, name:
- **the face:** the named person who belongs there;
- **other named people** there;
- **the crowd:** unnamed, with what they notice. No first meeting and no arc;
- **who notices her** there, and what they do about it. If nobody does, say so as a choice.

Release 1 has them all, shallow.

Must read: C804, C657, C589, C1531, C577, C620, L147.
Why: the people bite took only the core cast, and the plan missed 12 people. The old game's playtest found the same empty world (L147). (NOTES gap "`plan.md` has no step that fills the world", 2026-11-20.)

## 6 · The systems bite

Walk every place and every part of her day: morning, class or work, afternoon, evening, night. At each, ask three things:
- which system lives here;
- what she can do here alone;
- what she can do here with a person.

**Don't schedule activities around each other.** A repeat activity (a shift, a workout, study) is open whenever its place is open and its people are there; only something that really happens at a time (a class, a party) gets fixed hours. When two compete for the same hours, that's the player's choice (`craft/systems.md` rule 7; L166).

Ask about every area, one per bite:
- home life (meals, chores, the people she lives with);
- body care (energy, sleep, washing);
- money (work, bills, spending);
- clothes (what she owns, what she wears where, dress codes);
- the phone;
- college or work;
- reputation and talk;
- nights out;
- anything the want's goals read.

**Every meter or counter a goal reads gets a piece.**

**Every place open in release 1 has at least one thing she can do alone.** "Nothing to do here right now" is never a place's standing text. This is stricter than C738, which allows that text in an open empty room. It's stricter on purpose, because an empty world is what the old game's playtest found (L147).

Must read: C738, C775, C883, C1462, L147, L149.
Why: first_term_lean's plan listed only the systems WANT and IDEA named. For example, campus talk was read by goal 2 with no piece; hygiene, meals and chores with people, and dress codes were in no piece; and 15 places said "Nothing to do here right now". (NOTES gap "`plan.md`'s piece list step has no pass for what she can DO", 2026-11-20; LO's skill-fix brief, 2026-11-20.)

## 7 · The schedules

One week table per person: where they are, at what hours, on which days, and roughly how many hours a week she can reach them. Every person has at least one row. A loop a ladder opens is open about 18 hours a week between 08:00 and 24:00 (C159). Travel time is what makes the table matter (C924).

Must read: C577, C582, C921, C924, C159, L84.
Why: nothing asked for each person's week before the everyday pieces were listed; LO caught it and added a schedule piece. (NOTES gap "`plan.md` has no schedule step", 2026-11-20.)

## 8 · What she walks into, place by place

After the schedules, because a walk-in sits where that person's rows already put them (L97; v2's gate `a walk-in can happen`). One area per bite. For each place, name one or two scenes, and for each:
- **what she sees,** and her choice: watch or leave, help or say she's late;
- **which kind:** she comes across something (it fires by itself on arrival, `chance = 0.35`, once a day each, never a button; C2195), someone walks in on her in the middle of an act, or someone comes to her when she arrives (it fires by itself, at most one a day across the game; `craft/walk-ins.md`, "When someone comes to her");
- **who:** half or more of an area's scenes name a person she knows (C678);
- **everyday or not:** about half are everyday, someone's life going on without her (C802, L147); give the area's count;
- **the window,** from the person's rows;
- **how often:** once, or once a day.

**Then the person pass.** For each person she lives with or sees often, ask: *when this person is alone, what are they doing right now, at this point in their arc?* The where and the when come from their rows. Each answer is a scene she can walk in on. When the game's shape is taboo at home (C28), each housemate has at least one walk-in at home.

**A walk-in shows the person now, not their end want.** A person who wants her later does not want her in their first walk-in. A walk-in gets a new version only when that person's arc moves a step, and each version is still what they were already doing (L97).

While her meters are still, a walk-in sets a flag only and never pays. A meter's first gain is never behind a chance roll (L70). A person's next arc step is never left to the dice (C174, C212). No "nothing happens" (L150). Write the scenes from `craft/walk-ins.md`. Each walk-in also names its next band and what opens it: a meter level or an arc step (`craft/walk-ins.md`, "How a walk-in grows").

Must read: C788, C802, C854, C678, C212, C174, C28, L70, L97, L147, L150, L4, C2186, C2187, C2195.
Why: the plan asked who notices her (§5) and what she can do (§6), but nothing asked what she walks into at a place. LO: "random scenes where she walks in, like in the old first term there was this park and library scenes... Here we dont have anything for it in the skill." (relayed by the ENI session, 2026-11-21; first_term_lean NOTES, 2026-11-21, sex scenes.) Going place by place, nobody asked what each person does alone, so a scene like old first_term's `ryan_door_ajar` (`games/first_term/toml_phases/7_final_game.toml:49479`) came up only by luck (LO, relayed 2026-11-21).

## 9 · The arcs

Per person who has one, the arc's scaffold: its shape, its direction, its opening (the steps before the first sex) and its ending. Steps are designed one release at a time, in that release's pieces, never all at once here. A housemate is reached through accidents first (C297). Every release ends on an opening: each arc's last card says where it stops and what comes next (C140).

Must read: C74, C129, C140, C297, L91.
Why: designing every step of every ladder before anything was confirmed made no sense, and LO cut the plan back to a scaffold (L91).

## 10 · The releases

Roughly what each release adds, and per person whether they are in, later or cut, and what the player loses. Release 1 is the skeleton: every person, place and system, with the daily loop and each person's first meeting, all shallow; meters shown, not yet moving. **Release 1 is frozen** (C2182): people differ only by their start values and traits, her skills show their start values, and nothing moves: no feeling effect, no skill gate, no effect on a skill. The first release that moves a feeling writes its moves from `craft/people.md` rule 15, and the first that moves a skill writes its gates from `craft/meters.md`. (LO, typed in main-lean 2026-11-25: "Meter frozen".) Later releases add events, rungs and people at existing places, not new places.

**Her own sex opens only with a partner.** Sex she has opens only with a boyfriend or a husband, and is open from the start of that relationship. Until she has one, her own sex is out of scope, and the out-of-scope line says so. Sex she sees or hears is not her sex: it is a walk-in (§8) and is in scope. (LO, relayed by the ENI session, 2026-11-21: "Scenes where player is having sex is fine to put them in the out of scope... until she is married or have a boyfriend, in those case, from the starting she can have sex with her partner.")

**Walk-ins, release by release** (our design; LO, typed in main-lean 2026-11-26: "Yes", "One is fine for now"). Two kinds, both fired on arrival and neither a button (LO, typed in main-lean 2026-11-26: "2nd one", "Go"; this reverses his earlier "2 i would say button is good here"): she comes across something (`chance = 0.35`, once a day each, off the shared flag, the place resting 3 arrivals after a hit), and someone comes to her (fires by itself on arrival, written for a named person, only where their rows put them, about half everyday). At most one "comes to her" scene a day across the whole game; the limit doesn't cover the buttons or story moments (C2187). Each has a written way out: a no is free while meters are frozen, and costs a little with that person once feelings move (C2188). A repeat rests or climbs one step, each step needing the one before; it never replays at once (C2189). How many days a scene rests before it comes again is the game's number, asked of LO and written here with his words (worked example: three days for a game with about ten such scenes; LO, typed in main-lean 2026-11-26: "Go with your picks"). A person may come to her from an adjoining place their rows put them in, a knock or a call from next door (C2186). A story moment fires for sure when due, never behind a chance (C2190). Bolder answers open by her level, once meters move (C2191). Release 1 has 8 to 10 "comes to her" scenes and the first steps of two or three chains, flags only (C2192). The measures: `COT_DESIGN_STUDY.md` Part 9 and `playtest_study_20261109/13_random_scenes_top.md` (1 to 2.5 surprise scenes a game day in the busiest games; every game has a way out; repeats rest or climb).

Must read: C76, C104, C294, C1462, C2061, C2182, C2186, C2187, C2188, C2189, C2190, C2191, C2192.

## The piece list (each release)

One piece per place, person or system, each shallow in release 1.

- **The opening is one piece.** It holds the setup, the problem and the people who carry it, the start choice asked by a person, the first objective and its card, and the hand-over into a live place. Write it from `craft/opening.md`.
- **Why:** first_term_lean split the opening into four. Rent went to P11, the goal card to P12 and breakfast to P14, so the opening LO played (`games/first_term_lean/cards/P13.md`) had no problem and handed over into an empty kitchen.
- **Walk-ins: one piece per area,** holding that area's scenes from §8. Write it from `craft/walk-ins.md`.
- **No other scene kind is kept whole yet.** None has a failure behind it. `LATER.md` holds the idea for a person's first meeting.

**Reads.** `games/<slug>/STATE.md`, `NOTES.md`, `PLAN.md`, LO's answers in chat, `craft/opening.md` for the opening piece, and `craft/walk-ins.md` for §8 and the walk-in pieces.

**Writes.** `games/<slug>/PLAN.md` (one page per bite at most), the decisions in `NOTES.md`, and the release's piece list with its out-of-scope line in `STATE.md`.

**Done when.** LO has said yes to every bite and to the piece list, and `STATE.md` ends with `Next step: piece — <first piece>`.
