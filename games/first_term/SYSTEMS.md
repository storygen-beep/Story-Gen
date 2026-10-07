# The systems — First Term (layer 4: systems as slots)

> [READY] · layer 4 · drafted 2026-10-06 · updated 2026-10-07 (party scout and party rules) · signed by LO: LO, 2026-10-07 (the cast ages in `want.cast` stay proposed)
> A game-only page beside `DIRECTION.md` (layer 2) and `LIVES.md` (layer 3). Moved here from
> `proposals/SYSTEMS_SLOTS.md` on 2026-10-07 (snapshot `first_term_snapshots/20261007_layer4_close_before/`).
> v1 drafted 2026-10-06 (snapshot:
> `~/Documents/Great_Games_Study_20260926/first_term_snapshots/20261006_systems_slots_v1/`). v2 written
> 2026-10-07 from LO's brainstorm in chat (2026-10-06/07).
> **"LO, chat"** marks a call LO made in that brainstorm. **"kept (LO, 2026-10-07)"** marks the calls LO
> kept on 10-07: the "Decided in chat" list and the 10-07 fix-up calls. Everything else is **proposed**.
> Written to other pages on 10-07: the college rows, people and places on `LIVES.md` (the timetable rows,
> the college staff, the canteen rows, who is met when, §8's places) and the SP1 lines (snapshot
> `first_term_snapshots/20261007_lives_sp1_before/`). On 10-07 the ledger got the new people (`want.cast`)
> and places (`want.places`); no `board.*` yet.
> Layer 4 decides two things per system: **does it gate content**, and **which flag or number it uses**.
> Hours, amounts, rungs, pools and outfits belong to each system's card, later. No money amounts here.
> Rules used: `the-systems.md` SY1 (:58-100), SY2 (:104-119), SY2b brake (:181-185), SY5, SY8
> (:363-394); `the-meters.md` W3 (:179), M8-M10 (:917-985); `engine.md` §26 (:1192), §28 (:1296), §30.1
> (:1498), §49 (:2862), §51 (:2909), §52 (:3060); `the-arc.md` A6/A6b (:298-354), A9 (:402), A15 (:600-601);
> `the-phone.md` P1-P12; `templates/cards/*.md`.

## The short version

| # | what | kind | gates content? | its keys |
|---|---|---|---|---|
| 1 | college | system | yes: classes, exams, offices, the dean, the curfew | `intelligence`, four `grade_*`, exam flags, `office_business_<term>_used`, `on_probation`, `complaints`, `curfew` |
| 2 | the café job | system | yes: every Tom B step, the uniform tiers | `cafe_job`, `cafe_shift_1/2/3_today`, `uniform_sexy`, `uniform_slutty` |
| 3 | money and rent | system | yes: Sunday steps, goal 1, the twist, food and clothes | `money`, engine rent + `rent_carried`, `paid_full_streak` |
| 4 | parties | system (no card) | yes: Friday steps in four arcs | `party_went` + weekday + `hours_since_flag` |
| 5 | energy | a need | **yes, a real lock** (LO, chat) | `energy` |
| 6 | hygiene | a need, with an off switch | colour only, never a story lock | `hygiene`, `hygiene_off` |
| 7 | wardrobe | system | yes: leaving a room, dress codes, the risky buttons | clothing states (`worn_exposure`, `clothing_slot`), key items |
| 8 | `Exhibitionism` / `Corruption` | her two meters (SP2 §1) | yes: every stage choice | already on SP2 |
| 9 | `campus_talk` | a meter | yes: goal 2 | `campus_talk` |
| 10 | `laura_suspicion` | a meter | barely (one reader) | `laura_suspicion` |
| 11 | the phone | infrastructure (a channel) | carries steps, bookings, calls | threads, calls, `followers` |
| 12 | dating | not a system (decided item 4) | yes, through Jake's loop | `jake_date_booked` |
| 13 | sex for pay | a rung inside 2 and 3 (decided item 5) | yes, by stage | her stage + the price on the label |

---

## 1. College (LO, chat 2026-10-06)

- **Card:** `templates/cards/college.md` (four courses, a professor each, grades, exams, classmates
  beside her, `college.md:14-19`). **Thread:** `WANT.md:89`; `DIRECTION.md:51-59`.

### What it is
- **Four subjects:**
  - Psychology, taught by Hale;
  - Figure drawing (an art lecturer, a woman, about 45);
  - Business (the strict man, about 50);
  - Biology (a TA, a woman, about 28).

  The three new lecturers stay **light** this release (LO, chat). Ages are proposed; all are 18+.
- **The timetable** (LO, chat, option B): three classes a weekday, two in the morning and one in the
  afternoon; Psychology meets four times a week (Hale) and the other three subjects three times each;
  Friday has Psychology only.

  | day | morning 1 | morning 2 | afternoon |
  |---|---|---|---|
  | Mon | Psychology | Business | Biology |
  | Tue | Figure drawing | Biology | Business |
  | Wed | Psychology | Business | Figure drawing |
  | Thu | Figure drawing | Biology | Psychology |
  | Fri | Psychology | free | free |

- **A class visit** (LO, chat):
  - The base menu is Focus · Chat · Doze · Skip.
  - On top is **a risky slot that grows with her stage**. It reads Exhibitionism (what she shows),
    Corruption (what she does) **and what she is wearing** (`the-arc.md` A6).
  - The next locked button shows what it needs (SY5).
  - One small event may fire from that class's pool. An accident and a chosen act are separate beats
    (`the-arc.md` A6b).
- **The guy beside her who is hard and asks for help** is a pool event. Her answers grow by stage
  (LO, chat):
  - Curious: she watches.
  - Bold: a handjob under the desk, **only where nobody can see**.
  - Hungry: a hand or blowjob under the desk with the class there.
  - Further: he takes her to the bathroom.

  Under the signed heat table, where people could see it is Hungry (`SP2_ladders.md:41`).
- **Figure drawing:** the class draws a nude model, and posing is the college exhibition ladder (LO,
  chat). The stages follow the heat table: naked for the art lecturer alone is Bold · Showing
  (`SP2_ladders.md:39-40`); naked in front of the class is strangers able to see, Hungry · Watched
  (`:41-43`). **kept (LO, 2026-10-07):** naked or a flash for a group is Hungry · Watched; signed SP2 says
  so (`SP2_ladders.md:41-43`).
- **Exams:** midterms about weeks 7–8, finals about weeks 15–16 (`DIRECTION.md:119-120`).
  - A reminder comes a week before.
  - She makes one choice inside the exam (LO, chat 10-06): focus, or copy from the study guy. The lewd
    trades, by stage: Curious · Daring, flirting so the study guy turns his paper her way; Curious ·
    Daring, a flash for the cocky guy alone for his answers (`SP2_ladders.md:37-38`).
  - The result is read from `intelligence` + that subject's grade, and puts the subject in a band:
    **failing / fine / top**.
- **Each office has its own route, one per person** (kept (LO, 2026-10-07)). No shared "fail → office → body
  → grade" chain. Stages follow the signed heat table (`SP2_ladders.md:34-44`).
  - **Before any route opens, every office is a small talk hub** (kept (LO, 2026-10-07)). Her grade in that
    subject, and one line on what she wears or her stage. The lecturers' office rows on `LIVES.md` (`:248`, `:251`, `:254`) stay,
    so nobody disappears.
  - **Hale (Psychology):** study sessions, as extra classes that lift `grade_psych` (decided item 9).
    His arc rides on them (`ARC_IDEAS.md:293-298`).
  - **The art lecturer (Figure drawing, a woman):** posing, not a grade trade. She asks her to model
    privately for her own drawings.
    - Curious · Daring: an F/F tease while she poses clothed (`SP2_ladders.md:37-38`).
    - Bold · Showing: naked for her alone (`:39-40`).
    - Later: posing naked in front of the class, Hungry · Watched (`:41-43`).

    The grade rises as a side effect, never as the price.
  - **The Biology TA (a woman, ~28):** she is the shy one, and Ella leads and seduces her, F/F. No grade
    trade.
    - Curious · Daring: an F/F tease, a kiss (`:37-38`).
    - Bold · Showing: private sex in her office (`:39-40`).

    Later rungs come with her sheet.
  - **The Business lecturer, "the strict man":** the one who can't be bought. His office is honest: a
    retake if she studies (it reads `grade_business`; the band it needs is left for the card), once per
    exam. This replaces "parked" (kept (LO, 2026-10-07)).
  - **The dean:** below. Her body can make the trouble go away.
- **Failing costs something real** (LO, chat, option A):
  - Laura reads the grade.
  - Low Warmth means **a curfew, a real lock** on going out at night: parties, late shifts, Saturday
    dates. The door says why. The house at night stays open. ("Grounding" became "curfew": kept (LO,
    2026-10-07).)
  - The curfew **ends after a week, and starts again if the grade is still failing** (LO, chat, option 3).
  - Mark gets leverage at the table.
  - A subject still failing a week after its result puts her on **probation with the dean**.
- **The dean**, a man of about 55 with an office on the faculty floor, handles **both grades and
  complaints** (LO, chat).
  - The first meeting is a warning. After that comes a letter home.
  - Complaints come from the dress code and from **the rival girl, who can report her** (LO, chat).
  - His route, from Curious (kept (LO, 2026-10-07)):
    - Curious · Daring: a flash for him alone, and the complaint is dropped (`SP2_ladders.md:37-38`).
    - Bold · Showing: hands or mouth in his office, door shut, and no letter home (`:39-40`).
    - Hungry · Watched: his door unlocked, with someone able to walk in, and a grade raised (`:41`).

### Gates content? Yes
- **Classes:** Hale B 1, 2 and 5 and Nadia's After line sit in Psychology (`ARC_IDEAS.md:293`, `:294`,
  `:297`, `:300`).
- **Office hours:** Hale B 3, 4 and 6 move to the faculty floor (LO, chat).
- **The failing chain gates** the curfew, the letter home, probation and the dean's route.
- **Each office route has its own gate:** her stage, and that person's step before. Business's retake
  reads the exam flag.
- **The midterm** colours Hale B 5's line and blocks no step (`DIRECTION.md:115-116`, `:143`).

### Keys
- `intelligence`: a trait that **only goes up** (LO, chat). It is fed by Focus, the library and the study
  guy, and read by every exam.
- `grade_psych`, `grade_art`, `grade_business`, `grade_bio`: four traits, banded failing / fine / top.
  Class choices and exams write them. Laura, lecturers, Mark and the dean read them. This replaces v1's
  single `grade`.
- `exam_<subject>_<term>_done`: one flag per exam. Probation and Business's retake read it through
  `days_since_flag`.
- `office_business_<term>_used`: once per exam, for the Business retake only. The other routes are steps
  that repeat after their last one, not once-per-exam trades.
- `on_probation`: a flag set by the dean scene, cleared when the grade is back to fine. His route stops
  the letter home and can raise a grade; it does not clear probation by itself.
- `complaints`: a counter trait, written by the dress-code warning and by the rival's report. The dean
  reads it.
- `letter_home`: a flag that Laura's scene reads.
- `curfew`: a flag set by Laura. The front door at night reads it as `is_false`. It ends through
  `days_since_flag` ≥ 7, and the grade check sets it again (`engine.md` §52).
- **Classes are located canvases,** so each one fires once per class window through
  `max_triggers_per_day` (`engine.md` §28.1: "A LOCATED canvas does not need the flag at all").

### Day 1, links, and what's left
- **Day 1:** yes. Monday's first class is the opening day (`SP1_time.md:8`; `LIVES.md:380`).
- **Leads to:** Hale (study sessions, his arc), Nadia, the four classmates, the art lecturer (posing),
  the Biology TA (Ella leads), the Business lecturer (an honest retake), the dean.
- **Touches:**
  - feeds `campus_talk` and `laura_suspicion` (`DIRECTION.md:26`);
  - feeds Mark's Power;
  - reads energy and the wardrobe.
- **Left for its card:** class hours, pool sizes, how much each choice moves a grade, the band edges,
  how often each event repeats.

### Clashes
- `hale_office` keeps its id (`v2_state.json:262`), and it sits on the faculty floor (LO, chat;
  `LIVES.md:208`). The ledger's place list is flat; which room opens off which is the board's map.
- `SP2_ladders.md:28` says release 1 writes stages 1–3. Under-the-desk in class and the public flash
  are Hungry, so they wait for a later release unless page 7 says otherwise. A flash for a group is
  Hungry · Watched (kept (LO, 2026-10-07); `SP2_ladders.md:41-43`).
- `IDEA.md:44` says "the rival: none declared". The rival girl changes that, which is LO's change to the
  idea page.

## 2. The café job

- **Card:** `templates/cards/job.md`. **Thread:** `WANT.md:90`; `DIRECTION.md:61-65`.
- **Gates content? Yes.**
  - Every Tom B step: 1–13 (`ARC_IDEAS.md:226-238`).
  - Tom's row (`LIVES.md:148`) and Gary's rows (`:160-161`).
  - Friday close (`:144`), and "after hours" every Friday after Tom B 13 (`:491`).
  - Tom's final no takes away the late shifts (`:150`).
  - Low energy refuses a shift, and the curfew refuses the late shifts.
- **The uniform comes in three versions: normal → sexy → slutty** (LO, chat).
  - The sexy version is Tom B 2's uniform rule (`ARC_IDEAS.md:227`). The slutty one comes later in
    Tom's arc, or by her own choice at Hungry.
  - Each needs enough Exhibitionism to wear, and the first shift in each is a scene.
  - A better uniform means better tips. This is the model's ladder (`the-arc.md` A6b; `job.md:15`) and
    SY8 rule 1 (`the-systems.md:368`).
- **Keys:**
  - `cafe_job` (new);
  - `cafe_shift_1/2/3_today` (`SP1_time.md:20`);
  - `uniform_sexy` and `uniform_slutty` (new flags), which open the uniform items;
  - Tom's final no sets the engine's `<canvas>_closed` (§49);
  - pay goes into `money`.
- **Day 1:** proposed: the job ask is open from day 1 (SY8 rule 4). With three classes a day, her café
  time is late afternoons and evenings, or a skipped class.
- **Leads to:** Tom, Gary, and Mark's question about the twenties (`ARC_IDEAS.md:240`).
- **Left for its card:** hours, tips, what each uniform pays.
- **Clash:** Tom B 2 sits at C1 (`ARC_IDEAS.md:227`), but SP2 puts dress codes at Curious
  (`SP2_ladders.md:37-38`).

## 3. Money and rent

- **Card:** `templates/cards/money_pressure.md`. **Thread:** `WANT.md:93`; `DIRECTION.md:17-22`, `:79-84`.
- **Gates content? Yes.**
  - The Sunday steps: Mark A 1, 3, 7 and 15 (`ARC_IDEAS.md:184`, `:186`, `:190`, `:198`), each played
    in two versions (`:179`).
  - Goal 1 (`IDEA.md:29-34`), whose body route is Mark A 9 (`IDEA.md:33`).
  - The twist (`DIRECTION.md:28-45`).
  - A short week brings a letter or Vance (`DIRECTION.md:20`; `LIVES.md:274`, `:340`).
  - **New sinks** (LO, chat): **canteen food costs money**, and the **clothes shop**.
- **Keys:**
  - `money`: unclamped (`engine.md:1234`).
  - The engine's rent with `on_short = "carry"` (proposed).
  - `rent_carried`: set by the engine (`v2.py:14427`); Mark's Sunday steps, the knock and the letter
    read it; Vance's knock clears it (`SP1_time.md:25`).
  - `paid_full_streak` (new counter) and `ryan_covered` (new flag): goal 1's money route.
  - `pays_her_own_way` and `helped_with_debt` (`v2_state.json:17`; `DIRECTION.md:33`).
- **Engine fact:** no effect lowers what she owes. Only the rent page writes `rent_state.owed`
  (`v2.py:14423`, `:19158`).
- **Leads to:** Mark A 1–15, Vance, Ryan's cover. **Left for SP4:** every amount, and how many Sundays
  the streak needs.
- **Mark A 5's "a bill off" (`ARC_IDEAS.md:188`) and Mark A 14's "Paid." (`:197`):** paid to her as
  money before the rent is taken (decided item 8).
- **Risk:** if she misses Vance's knock, `rent_carried` stays set into the next week.

## 4. Parties (Friday at Zoe's)

- **Card:** scouted, near: `scout/party.md` (2026-10-07). The model is CoT's Friday quad party, with
  IHOH and Shady Deals as contrasts; neither `greek_life.md` nor `reputation.md` covers it. It passes SY1's
  seven questions (`the-systems.md:65-73`). **Thread:** `WANT.md:91`; `DIRECTION.md:67-71`.
- **Gates content? Yes.**
  - Steps: Zoe A 1, 2 and 5; Jake B 1 and 5; Laura C 7 and 15; Ryan A 14 (`ARC_IDEAS.md:264`, `:265`,
    `:268`, `:322`, `:326`, `:152`, `:160`, `:122`).
  - Rows: Zoe's (`LIVES.md:181-182`), Jake's (`:300`) and the gated Friday rows (`:484-489`).
  - **The curfew and low energy refuse a party** (LO, chat). Zoe's party also wants something short to
    wear (block 7).
- **Keys:** `party_went`, Friday and `hours_since_flag` (`SP1_time.md:38-41`). The drinks boost, the
  skip-Kayla flag and the Laura-at-Fridays flag have no keys yet.
- **Day 1:** no. It starts on the first Friday (`DIRECTION.md:118`).
- **Leads to:** Zoe, Jake, Laura, Ryan.
- **Inside a party (LO, 2026-10-07, from the scout card):**
  - **Dares:** Zoe sets them, and they come with people watching. After a no, someone else pushes once,
    but her no still holds and costs nothing (`SP2_ladders.md:131`). The card's model lets the push beat
    her no (`scout/party.md`, dares row); we don't.
  - **Drinks:** people hand them to her. She can say no, and the no always works. A drink is the drinks
    boost: it opens a bolder choice one stage early and wears off by the hour (`SP1_time.md:21`). The
    model's offers are in `scout/party.md`, drinks row.
  - **Who is there:** Zoe always, and Jake from the night Ella meets him (Jake B 1) until he leaves at
    midnight (`LIVES.md:187-188`, `:368`). Classmates turn up by chance each Friday. Anyone she turned
    down stays cool with her for the rest of that night.
  - **Hours:** the party runs to about 2 a.m. (`SP1_time.md:10`), and the riskier choices open after 11 p.m.
  - **Money:** none. Drinks and food at Zoe's are free.
- **After a party (LO, 2026-10-07; none of the 12 games shows these, `scout/party.md` gaps):**
  - **The way home:** coming in late can set off Laura's catch (`ARC_IDEAS.md:147`). It needs the "out
    late" key (below, "Steps that need a key", 1).
  - **The next morning:** a heavy night starts Saturday with less energy (block 5). How many drinks
    count as heavy is SP4's number.
- **Hosting:** Ella hosts once, in Zoe A 6, on the night both parents are away (`LIVES.md:130-131`).
  Hosting as a weekly thing is parked for a later release.

## 5. Energy (LO, chat)

- **Card:** `templates/cards/needs.md`. **Rule:** a need declares what it shuts (`the-meters.md` M8, M9).
- **Goes down** with classes, shifts, parties and sex scenes. **Comes back** from sleep (most), canteen
  food (some; it costs money) and Doze in class (a little).
- **No hunger meter.** Energy covers it, and food refills energy (LO, chat).
- **Gates content? Yes, a real lock** (LO, chat). Low energy means no café shift, no Focus in class (Doze
  only) and no party. Each refusal says why (SY5).
- **Zero** is a scene: she falls asleep and wakes the next morning. Never a game over (`needs.md:43`).
- **Key:** `energy`. It is spent through `costs` and refilled by effects (`the-meters.md` M10, the "spent"
  shape).
- **Clash / gap:** the engine has no sleep primitive (`needs.md:52-53`), so the bed refill is an authored
  canvas.

## 6. Hygiene (LO, chat)

- **The rule:** `engine.md` §30.1: one need, for routing, whose refill places roll events; a start-choice
  off switch.
- **Goes down** every day (`[player.trait_decay]`, `the-meters.md` M10), faster after work, parties and
  sex.
- **Comes back** in the **shared bathroom at home**, which is where Ryan, Kayla and Mark can be, so a
  shower can roll an event. The college women's toilet gives a quick wash, worth a little (`needs.md:16`).
- **Gates content?** Colour only, never a story lock (LO, chat). Low hygiene slows Warmth and gets lines
  from Laura or a lecturer.
- **Keys:** `hygiene`, and `hygiene_off` (the start choice). With it off, nothing reads hygiene.
- **Leads to:** the bathroom steps and events (Ryan A 1, 3 and 7: `ARC_IDEAS.md:109`, `:111`, `:115`).

## 7. Wardrobe (LO, chat)

- **Card:** `templates/cards/wardrobe.md` (states first, then items).
- **States:** covered, short skirt, no bra, no panties, underwear only, towel, naked. In the engine a
  state is a `worn_exposure` value or a `clothing_slot` row (`wardrobe.md:33-35`; `engine.md` §17).
- **Gates content? Yes.**
  - **Leaving a room** in a revealing state needs enough Exhibitionism, and the door says why
    (`wardrobe.md:16-17`).
  - **The risky buttons in class** read what she wears (block 1).
  - **Places:**
    - Zoe's party wants something short.
    - The café needs the uniform.
    - College has a **dress code** (LO, chat): a lecturer's warning first; repeated, or reported by the
      rival, it becomes a complaint to the dean (`complaints`). It never locks her out of class.
  - **Home lines per state:** Ryan, Mark and Laura each react, by their numbers.
  - **Events fire from a state**, e.g. a short skirt on the stairs.
- **College clothes are her own outfits in three levels:** normal, sexy, slutty. **Never a "college
  uniform"**, because that is school-coded (LO, chat).
- **The clothes shop in town:** prices shown, and the shop text says where each item counts (LO, chat;
  `wardrobe.md:26`).
- **Borrowing** from Zoe and Laura stays (`ARC_IDEAS.md:146`, `:264`).
- **Keys:** the state conditions, plus key items: the three café uniforms, Laura's dress and Zoe's dress.
  Declared under `board.wardrobe` later (`wardrobe.md:52-60`). Every state is read in 3+ places (gate
  `every clothing state is read three times`).
- **Changing** takes 1–2 clicks, with saved outfits.
- **Gap:** a dress code checks coverage only (`clothing_rules`, `engine.md:571`). A "slutty but covered"
  level needs `worn_corruption` or `worn_type` read in a scene, not the dress code.

## 8. Her two meters: Corruption and Exhibitionism

- Already decided on `SP2_ladders.md:12-44` (signed). This page adds only readers:
  - the class risky slot;
  - the uniform tiers;
  - leaving a room;
  - the selfie ladder;
  - the office and dean routes.

## 9. `campus_talk` (a meter)

- **Kind:** meters, not a system (`the-systems.md:389-394`; `reputation.md:10-13`). One trait for one
  audience with an unnamed crowd, no decay, plus an NPC flag for each thing a person saw
  (`reputation.md:74-78`).
- **Gates content? Yes:** goal 2. Its level opens Zoe A 6 (`ARC_IDEAS.md:269`; `IDEA.md:37-38`).
- **Fed by:**
  - the party scenes;
  - the campus names (`DIRECTION.md:159`);
  - **the canteen**, where talk spreads and the rival starts trouble (LO, chat);
  - the public class moments;
  - the social feed.
- **Read by:**
  - goal 2;
  - who approaches her;
  - **feed posts about her** (`the-phone.md` P6, last paragraph).

## 10. `laura_suspicion` (a meter)

- **Key:** `laura_suspicion` (`DIRECTION.md:24-26`). No decay.
- **Fed by:**
  - home late, lies and grades;
  - Mark A 4, 5, 10, 11 and 13 (`ARC_IDEAS.md:861`);
  - **the letter home and missed calls** (block 11).
- **Read by:** Ryan A 13 (`ARC_IDEAS.md:850`). That is one reader (SY2b brake); more readers go on Laura's sheet (decided item 6).

## 11. The phone (LO, chat)

- **Kind:** infrastructure, a channel (`the-phone.md:18`; `templates/cards/phone.md:8-11`).
- **Chats:**
  - one thread per person she is involved with (P1);
  - every text is caused by a scene, with a delay and an hour window (P4);
  - 3–7 words a bubble (P3);
  - every thread ends in a booking (P10);
  - after a person's sex step, the thread becomes the repeat invite (P9);
  - she can start a thread too (P12), e.g. Ryan A 11 (`ARC_IDEAS.md:119`).
- **Calls:**
  - Mark or Laura when she is out late or under curfew;
  - Tom calling her in;
  - the dean's office.

  A missed call costs something (`on_missed`, `engine.md:3026-3033`). **Gap:** a call is one-time
  (`engine.md:3033`), so a call that repeats (Laura every curfew night) has to be written as several
  calls.
- **A calendar:** exams, office hours, rent day, dates, parties (P10).
- **A social feed, in release 1** (LO, chat):
  - a selfie ladder (dressed → towel → topless → naked) opened by Exhibitionism (P6);
  - `followers` must buy something: campus talk, new messages, offers.
  - **Gap:** `post_actions` read only `corruption_min`, not place or clothes (`the-phone.md` P6;
    `v2.py:3318`).
- **A paid photo app, from Bold** (LO, chat): exhibition that pays `money`.
- **A streaming app, later** (LO, chat): `templates/cards/streaming.md`. The engine has no streaming piece
  (`streaming.md:39-41`).
- **Never a battery** (P11).

## 12. Dating (Jake's Saturdays)

- **Not a system** (decided item 4). It is Jake's loop, booked on his thread (P9, P10).
- **Gates content? Yes:**
  - Jake B 2, 3, 4 and 6 (`ARC_IDEAS.md:323-327`);
  - Laura C 5 (`:150`);
  - **the curfew refuses the date** (block 1).
- **Keys:**
  - `jake_date_booked` (new);
  - `jake_dates_off` (new; his parked no, `ARC_IDEAS.md:330`);
  - his final no sets `<canvas>_closed` (§49).

## 13. Sex for pay

- **A rung inside the café and inside money, not its own system** (decided item 5; `the-arc.md:600-601`).
- **Gates content? Yes, by stage** (`SP2_ladders.md:39-42`):
  - Tom B 4, 7, 12, 13 (`ARC_IDEAS.md:229`, `:232`, `:237`, `:238`);
  - Mark A 4, 5, 7, 10, 14, 15 (`:187-198`);
  - **the paid photo app** (block 11).
- **The price is shown first** (`the-systems.md:375`).

## Cards not used

- `greek_life`: nothing on the pages.
- `gym_body`: no gym.
- `pregnancy`: kept out (`ARC_IDEAS.md:904`).
- `shoots`: the figure-drawing pose is college's own ladder, not a paid shoot.
- `random_encounters`: none named yet.
- `streaming`: later (block 11).
- `shops_items`: only the clothes shop and the canteen, read through `money` and the wardrobe.
- `map_travel`, `quests_hints`, `cheats`: infrastructure, not this layer.

---

## New people and places this adds (on `LIVES.md:233-259` and in the ledger since 10-07)

**People (all 18+; ages proposed):**

| who | age | role | weight |
|---|---|---|---|
| the art lecturer | ~45 | Figure drawing; a woman; posing for her (F/F), not a grade trade | light |
| the Business lecturer, "the strict man" | ~50 | Business; can't be bought: an honest retake | light |
| the Biology TA | ~28 | Biology; a woman, shy; Ella leads and seduces her (F/F), no grade trade | light |
| the dean | ~55 | probation and complaints; his route, from Curious | light |
| the boner guy | ~21 | Psychology, Business; the under-the-desk ask | light |
| the rival girl | ~21 | Psychology, Business; reports her; the game's first rival | light |
| the study guy | ~21 | Business, Biology; tutor; raises `intelligence` | light |
| the cocky guy (Jake's teammate) | ~21 | Figure drawing, Biology; dares and prices | light |
| the figure-drawing model | ~25 | the class's model; a woman (LO, chat 10-07) | extra; lives inside the class, no row |

**Seating** (LO, chat):
- Psychology: Nadia, the rival, the boner guy.
- Figure drawing: Jake, the cocky guy, Zoe, plus the model.
- Business: the boner guy, the study guy, the rival.
- Biology: Zoe, the study guy, the cocky guy.

**Places:**
- the canteen;
- the college toilets, women's and men's;
- **one faculty floor with several offices:** Hale's (`hale_office`, now on the floor), the art lecturer's,
  the TA's, the Business lecturer's and **the dean's**;
- the clothes shop in town.

`LIVES.md` §8 lists them (10-07). The ledger has them (`v2_state.json` `want.places`, `:188-313`).
The faculty floor is one place, and each office is its own place (one room, one job, by analogy with `the-map.md` R2's rule for a home):
`faculty_floor`, `art_office`, `business_office`, `ta_office`, `dean_office`, and Hale's `hale_office`.
The cast ids, ages and keeps are in `want.cast`; the ages are proposed.

## Keys at a glance

**The overnight tick runs at midnight, not when she sleeps** (the day rolls over in `v2.py:6806-6808`; the
tick runs at `:6947-6967`; `engine.md` §28.1). The cheat page's "Skip to morning" runs it too (`v2.py:12236`).
`SP1_time.md:17-26` lists what it clears.

| key | kind | set by | read by | overnight | ok? |
|---|---|---|---|---|---|
| `intelligence` | trait, only up | Focus, the library, the study guy | exams | kept | ok |
| `grade_psych` / `_art` / `_business` / `_bio` | traits | class choices, exams, Hale's sessions, the retake, the dean, posing (side effect) | Laura, lecturers, Mark, the dean | kept | ok |
| `exam_<subject>_<term>_done` | flags | the exam scene | probation, the Business retake (`days_since_flag`) | kept | ok |
| `office_business_<term>_used` | flags | the Business retake | the Business retake | kept | ok |
| `on_probation` | flag | the dean | the dean, Laura | the scene clears it | ok |
| `complaints` | trait, counter | dress-code warnings, the rival's report | the dean | kept | ok |
| `letter_home` | flag | the dean | Laura's scene | the scene clears it | ok |
| `curfew` | flag | Laura's scene | the front door at night, the party, the date, late shifts | ends by `days_since_flag` ≥ 7 | ok |
| `energy` | trait, spent | classes, shifts, parties, sex | the locks | sleep refills it | ok; on SP1's list as "not on the tick" (`SP1_time.md:23`) |
| `hygiene` | trait, decays | the bathroom | Warmth, lines | decays daily | ok; on SP1's list (`SP1_time.md:22`) |
| `hygiene_off` | flag | the start choice | every hygiene reader | kept | ok |
| `money` | trait | café, paid rungs, the photo app, Ryan | rent, canteen, shop | kept | ok |
| `rent_carried` | engine flag | the engine | Mark's Sundays, the knock, the letter | Vance's knock clears it | ok |
| `paid_full_streak` | trait, counter | the Sunday table scene | goal 1 | kept | ok |
| `ryan_covered` | flag | Ryan's cover (no scene yet) | the Sunday table scene | the scene clears it | ok |
| `pays_her_own_way` · `helped_with_debt` · `hosts_the_party` | flags | goals, the twist | their readers | kept | ok |
| `cafe_job` · `uniform_sexy` · `uniform_slutty` | flags | the café | shifts, uniform items | kept | ok |
| `cafe_shift_1/2/3_today` | flags | the café row | the café row | cleared (`SP1:20`) | ok if the café shuts by midnight |
| `party_went` | flag | arriving Friday | the party after midnight | never cleared | ok |
| the drinks boost (no key) | — | party drinks | her choices | a choice modifier, not on the tick (`SP1_time.md:21`) | ok; it expires by the hour (`v2.py:6810-6820`) |
| skip-Kayla (no key) | flag | Ryan A 14's ask | Ryan's Friday scene and row | never cleared by the tick (`SP1_time.md:28-31`; `LIVES.md:484-488`) | ok |
| cancel-Kayla Saturday (no key) | flag | Ryan A 11 | Ryan's gated row (`LIVES.md:125-126`), Ryan A 12 | never cleared by the tick (`SP1_time.md:28-31`) | ok |
| both away · weekend away (no keys) | flags | events (`LIVES.md:62-66`) | rows, Zoe A 6, Mark A 13–14 | never cleared by the tick (`SP1_time.md:28-31`) | ok |
| Laura-at-Fridays (no key) | flag | Laura C 15 | her gated Friday row | kept | ok |
| `campus_talk` | trait, no decay | parties, canteen, class, feed | goal 2, approaches, feed posts | kept | ok |
| `laura_suspicion` | trait, no decay | home late, lies, grades, letters, missed calls | Ryan A 13 | kept | ok (thin) |
| `followers` | trait | the feed | campus talk, offers | kept | ok if something reads it |
| `jake_date_booked` · `jake_dates_off` | flags | Jake's thread, his no | the door steps | the scene clears it | ok |

## Steps that need a key nobody named yet

1. "Out late," for Laura C 2, Zoe A 3's homecoming and the hall catches (`LIVES.md:331-333`).
2. The weekend-away and both-away flags (`LIVES.md:62-66`).
3. Ryan A 11 and 14, and Laura C 15's gated rows (`LIVES.md:125-126`, `:484-489`).
4. The drinks boost: a choice modifier now (`SP1_time.md:21`), but it still has no key name.
5. The twist's offer scene before Mark A 15 (`DIRECTION.md:30-31`).
6. Ryan's cover has no scene to set `ryan_covered` (`SP2_ladders.md:66`).

## Decided in chat: kept (LO, 2026-10-07)

1. **The figure-drawing model is a woman.**
2. **The rent starts after the scene where Mark tells her she pays rent now** (`start_after_flag` on that
   scene, `SP1_time.md:12`; `engine.md:1227`). Her first Sunday can still come up short (Mark A 1). Knock-on: Mark A 1's "not
   expecting a count" (`ARC_IDEAS.md:184`) becomes "she knows, and she's still short".
3. **Parties: scout a card** with `v2-scout` from the pass-list games. Scouted 2026-10-07 (`scout/party.md`);
   LO's party rules are in §4.
4. **Dating is not a system.** It is Jake's repeat Saturday date on his thread. Changed 10-07:
   `SP2_ladders.md:167` (SP2 signed 10-07) and `LIVES.md`. Still saying "dating" as a system:
   `WANT.md:92` and `v2_state.json:344`.
5. **Sex for pay is a rung, not its own system.** LO: the card's model is a brothel-style stroll where the
   paid act *is* the shift; here the shift is waitressing (or the rent table), and the paid moments ride
   on it. The price is always shown first.
6. **`laura_suspicion` stays.** Its readers get written on Laura's sheet.
7. **Flags that cross midnight are never cleared blind by the tick.** They are read by hours since set,
   given a condition on the clear, or cleared by a scene. The drinks boost becomes a choice modifier that
   runs out by the hour. Written on SP1 (`SP1_time.md:21`, `:28-31`) and signed 10-07 (`:3`).
8. **Mark's prices are paid to her as money**, before the rent is taken. In the story it still reads "a
   bill off" and "Paid."
9. **Hale's office visits are extra classes:** they study together, and that lifts `grade_psych`. His
   lewd steps ride on those sessions.
10. **Release 1 and stage 4:** page 7 decides whether any Hungry class moments ship in release 1.
11. **`LIVES.md` gets the timetable:** written 10-07 (45 rows).
12. **SP4's numbers come with the release (layer 5).**

## Still open

- Page 7: release-1 width, which systems are live on day 1, the Hungry class moments (decided item 10),
  SP4's numbers (item 12).
- The steps that need a key nobody named yet (the list above).
- The cast ages in `want.cast` are proposed until LO says.

## What layer 4 hands on

**To the board phase** (`the-systems.md` "What the board phase records", :396-421; `state.md` board
schema, :110-186):
- **One card per system** (`templates/sheets/system.md`): college (§1), the café (§2), money and rent
  (§3), parties (§4; card `scout/party.md`), wardrobe (§7), energy (§5) and hygiene (§6), the last two also in
  `board.needs[]` (`the-meters.md` M8).
- **Meters** (`board.meters[]`): `campus_talk` (§9), `laura_suspicion` (§10), `followers` (§11),
  Corruption and Exhibitionism (§8; `SP2_ladders.md:12-44`).
- **Infrastructure** (`board.infrastructure[]`): the phone, a channel (§11).
- The keys and their overnight rules: "Keys at a glance" above.

**To page 7:** release-1 width; which systems are live on day 1; the Hungry class moments; SP4's numbers.
