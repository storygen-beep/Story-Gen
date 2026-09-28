# Register — what the player reads after a click

Two halves, and they are read at different moments.

**Part one — the explicit beat.** How to write the thing the game is for, and the one defect that
recurred three increments running. Read it when you are writing heat. It also carries the two rules
that came out of reading four top female-PC games in source (2026-08-23): **the reason axis** — the
same act reached two ways is written two ways — and **the two-halves sentence**, which is how a
repeatable act surface survives its fiftieth visit.

**Part two — the other ninety percent** (from "which is not one register, it is six"). A table of
the six kinds of screen and the four rules that hang off it: where the clip goes, how far one canvas
climbs, who speaks, and the content kind we do not build. Read it before you write anything at all,
because the kind decides the shape.

**The voice is a choice, and it is LO's** (2026-09-23/24): shown three ways to write one line, LO
picked the top games' loud version over ours. So **"The voice — say it loud"** and **"The truth rule"** below are a decision made against the field, not a measurement of
it. The rules that are measured keep their measurements, and where
a measured rule and the voice disagree, the voice wins and the old rule is retired in place (L2).

---

## The voice — say it loud

The old voice was quiet: the story left between the lines for the player to infer. That is what
was rejected. The new voice tells the player what is happening, what the protagonist feels, and
why. **Loud is not long, and short is not compressed:** loud prose keeps its joints (below).
It keeps "Sentences run short" below. Length is set by the scored model beats (`## The model beats`), not by a number.

1. **Say it, don't hint it.** Tell the player what is happening and what it means.
2. **Spell out the feelings.** Angry, scared, turned on, embarrassed: say so.
3. **Her thoughts on screen, beside the dialogue, never instead of it.** She has opinions, in
   italics (`thought_bubble`). S3 below names thinking *instead* of talking as the defect; the
   voice adds speech first, then her reaction to it.
4. **Push the drama.** Make the situation obvious and felt. Not every line has to be loud.
5. **More dialogue than narration.** The shape of a scene with a person in it: **someone speaks →
   she answers → they push → she thinks → a choice.**
6. **Every character sounds like themselves.** Short and blunt, strict, worried and distracted,
   teasing: pick one per person and hold it. Nobody sounds like the narrator. S3's "one term of
   address per person" is the cheapest way to do it.
7. **Obvious on arrival.** Within the first lines the player knows who a person is, what they want,
   and how they feel about her.
8. **Name the sexual tension.** Don't bury it.
9. **End on a hook**, something that points at what happens next.
10. **Keep the concrete detail:** places, objects, money, schedules, work. Loud is about what the
    prose *claims*, not about swapping specifics for adjectives. That is why the truth rule below
    ships with it.

The game's own voice — labels, buttons, guidance cards — stays plain. The loud voice is for the
story text only (`the-voice.md`).

**Measured targets** (the 2026-09-24 scene-content review, which read the 26 games' own source; the field column is its random sample of passages, because a
curated library of best scenes overstates every property):

| | the top games | target |
|---|---|---|
| narration to dialogue | 2.93 : 1 across 27 games (S3) | under 5 : 1, gate `somebody speaks` |
| dialogue in a scene | 83% of scenes, median 3 NPC lines | every standing scene with a person has a spoken line |
| a person shows what they want | 54% of scenes | most scenes with a named person — "What a scene contains" |
| `but` / `and` per 1,000 words | `but` 2.46–8.44, `and` 9.3–41.1 (25 games) | `but` ≥ 2.88 (p10), `and` ≤ 41.1 — gate `prose has room` |
| median sentence | p25 8.25 · median 10.5 (26 games) | printed only: the model beats run 7, on purpose |

**Joints.** A sentence is joined to the next by what it has to do with it. Compressed prose drops
the joints — too few `but`s, too many `and`s, against the field range in the table above. The fix is one of three: **cut** the clause, **split** the
sentence, or **name the relationship** — *but, because, so, until, when*. A sentence of `and`s is a
list; name what holds its parts together, or break it.

**A pronoun needs someone on screen first.** Screen one read *"Your mum doesn't know he paid"*: `mum`
is who `he` is not, and nobody else was there. Put the person on screen — a role, a name, a
speaker, a token — before *he* or *she*. A place's text starts with nobody. Listed by `lint · a
pronoun with nobody to point at`.

The one-time steps carry the full loud version; the screens the player re-enters are short and
still speak. That split is L3 below.

---

## The truth rule

**Loud writing makes claims.** *"She hasn't slept." "You didn't eat last night." "Nobody ever
thanks her."* The quiet voice made few claims, so it rarely went wrong. The loud voice makes many,
and every one has to be true on every playthrough that can reach the screen.

Measured on the first loud rewrite of a real scene (a breakfast scene, 2026-09-24): five lines,
five defects — one contradicted the design (the wrong clothes for that hour), two claimed a past the
player may not have had (*"last night"*, *"for the first time in a week"* on what could be day one),
one was out of character, and one printed a stat that does not exist.

| allowed | not allowed |
|---|---|
| texture that cannot clash with anything: the kettle, a pet name, the oil in the tray | anything that contradicts the design: clothes, times, who is where |
| her opinions in her thoughts | claims about the past that no flag tracks: *last night*, *this week*, *again* |
| dialogue that fits the person's cast entry | behaviour the cast entry rules out |
| a consequence printed on a button when a real flag or stat sits behind it | made-up stats (`the-meters.md`, "What the player is shown") |

**The four rules.**

1. **Every fact line is checked** against the sheets and the built schedules: who is there, what
   they are wearing, what time it is, what day.
2. **A line about the past shows only behind the flag or counter that records it** — a `group`
   whose `conditions` read it. *"You're late again"* is legal inside `late_count gte 1` and a lie
   outside it.
3. **A big moment is a one-time step, not a repeatable.** A repeatable plays every visit, so it
   cannot carry a revelation. L3.
4. **A consequence printed on a button is a real flag**, or it is added to the design first. Scores,
   including a person's own, are never printed (`the-meters.md`, "What the player is shown").

**How to check a scene — seven steps.**

1. List every time the canvas can fire: its trigger, plus the NPC's schedule rows on every
   weekday. A scene that can fire at 09:00 on a Saturday cannot say *"tonight"* (`the-clock.md` C2).
2. List every factual claim in the draft: times, clothes, who is where, what the past was, what
   someone knows.
3. Check each claim against a source: the cast pages, the systems pages, and the built schedules
   in `7_final_game.toml`.
4. A claim true only sometimes gets a gate or a variant. With no gate for it, cut it.
5. Check each character's lines against their cast entry, including how they say no and what they
   never do.
6. Check each printed consequence against the button's real effects.
7. Write the facts list at the top of the draft, so the next reader can check it too.

**One line, wrong and right.** On a repeatable canvas:

> ❌ *"Late again. Third time this week."* — true on the third visit, a lie on the first.
>
> ✅ the same line inside a `group` on `<late_count> gte 3`, with a present-tense line
> (*"You're late. Apron's on the hook."*) as the fallback.

Lints: `a repeatable claims a past` (rule 2) and `a printed stat is real` (rule 4). Both are lists
to read; neither can check a claim against a sheet, which is why step 3 is yours.

---

## The rule

> **An explicit beat stays on the body for its whole length.**

Not "contains a crude word". Not "is about sex". **Stays on it** — from the first sentence to the
last, the beat is describing what is physically happening to whose body.

---

## The diagnostic that catches it while writing

> **Read the beat's last sentence. If it is about what the moment MEANS rather than what is
> HAPPENING, the beat has pivoted and it will score 0–1.**

Every single failed beat did this. The shape is always identical: name one body part, then leave
the body for the rest of the beat.

**The three pivot targets, named so they are catchable:**

1. **He knows.** *"…and he does not stop, and it is you who steps back, and it is you whose face
   is burning."*
2. **She is ashamed.** *"…and you lie there afterwards deciding not to have noticed what did it."*
3. **What this says about her.** *"…and the arithmetic does not come out the way it is supposed
   to."*

All three are good sentences. All three belong in the game. **None of them belongs at the end of
an explicit beat.**

---

## Where the interiority goes instead

Its own beat, *after*. A `thought_bubble` following the act is correct and is the register
working. The same thought folded into the act is the defect.

```
beat 1   the body, start to finish, three-plus named            ← explicit
beat 2   what it meant, what she is going to do about it        ← interiority
```

Splitting them costs nothing — cascade beats are free — and it fixes the score without
sacrificing a single line of the psychology, which is the part that makes the game good.

---

## What the fix is NOT

**Not word-stuffing.** Eleven rewrites moved a game from 7.5% to 9.4% without adding one
gratuitous noun. The words arrived because the camera stayed on the body long enough to need
them, not because they were sprinkled in.

**Not loosening the wordlist.** `come` was excluded from the frozen list because it matches "come
downstairs" everywhere. When prose scores low, the prose is what is wrong. The list has been
challenged twice and was right both times.

---

## The measured targets

| | |
|---|---|
| per explicit beat | **3+ words from the frozen list** |
| across the whole game | **7.5–9.3% of beats carry 3+** |

The band is the reference game's, held across eight years and twelve-fold growth.

> ⚠️ **It is a FLOOR. Its upper comparison is meaningless — do not read a game scoring far above it
> as "too hot."** That reading has been wrong twice and cost one game a dilution pass it never
> needed. Two independent reasons, both measured 2026-08-12:
>
> - **Different denominators.** The 7.5–9.3% band counts whole-source *passages* — combat, systems
>   and UI included, 15,587 of them. `gates.py` counts beats in **location prose only**. Not the
>   same scale, so the two numbers were never comparable.
> - **The reference is the coldest game in its own genre.** Across 18 shipped sandboxes scored on
>   this exact word list, the field median is **33.3%** of prose passages carrying 3+ — and the
>   reference game is **last, at 7.5%**. The floor is a property of that one game, not of the genre.
>
> Clear it. Do not aim at it, and never dilute to approach it from above.

---

### And a game-wide share cannot see the screen the player is on

**Every act node of every act loop carries 3+, or the loop is not a sex surface.** The whole-game
percentage is an average, and an average clears while the act itself stays warm — which is exactly
what the measured failure looked like, 95% of one game's crude prose sealed in a room with no exits
and all nine of its repeatable loops scoring zero.

Measured 2026-08-23, on the game authored under this doctrine: **10 of its 21 act and finish beats
were under 3** while the game-wide floor read a comfortable pass. The two SOLO loops carried 5–7 body
words per act node; the four CHARACTER loops — the headline content, the ones `the_want.md` names as
carrying the crudest writing in the game — ran 1–2, and one finisher scored **zero on 127 words**:
three paragraphs of a man coming, and not one named a body part.

`lint · the act nodes` prints it per node.

> ⚠️ **Count the BAND, not the node.** A finisher is banded by definition — it elects on `loop_stage`
> — and a player sees exactly one band. Folded together, one game's finisher scored 6; every band it
> could render put **two** body words on the screen. The lint reports the thinnest band a node can
> render for this reason, and the live probe reads what is actually on the page.

**The rewrite is in place, not additive.** These beats were already the right length; they were
warm. Replacing the hedged clause with the specific one moves the count and leaves the word budget,
the sentence length and the narration-to-dialogue ratio where they were — a batch that did exactly
this moved `somebody speaks` by 0.1 and `own_words` by nothing.

---

## Sweeping backwards: drive it off the MEASUREMENT, never off a category

The first backward application of this rule moved a game **10.8% → 15.9%** by rewriting "the three
repeatable sex loops". That worked, and it left the job half done: four canvases in the
protagonist's own bedroom — the solo surface, the wall, the door, the wardrobe — were written the
day before the rule existed, were never in the named category, and sat under the floor through two
further increments while the headline number went up.

Measured two weeks later, every beat in that room scored **0, 1 or 2**. The only sex surface in
the game she initiates alone scored **1 · 1 · 0**.

> **A category name is not a sweep. Score every beat, sort ascending, and fix everything under 3.**

The instrument already prints per-beat scores; there is no reason to select by intuition.

**One thing the per-beat numbers will show you that looks wrong and is not:** the interiority beat
*after* an explicit one scores 0, correctly and by design. Do not "fix" it. What you are hunting is
the beat that scores **1 or 2** — that is a beat trying to be explicit and pivoting off the body
partway, which is exactly the defect. A 0 next to a 4 is the rule working.

---

## The habit this is fighting

The pivot is not carelessness. It is a *literary* instinct — the trained move of ending a
paragraph on significance — and it is correct almost everywhere else in writing. Here it is the
single most reliable way to produce a game that is explicit and cold at the same time.

It reasserts itself the moment it is not being actively fought. Assume you are doing it, and
check the gate.

**Tested against the field and CONFIRMED, not loosened.** In Her Own Hands folds her thought
straight into the act — and never leaves the body: *"//Holy shit.// … I bucked my hips against his,
my wet pussy opening wider with each time he brought his cock deeper inside me."*
(`JamesDate1SexA`). That is not a pivot by this rule's own definition, which is about what the sentence is *describing*, not whether
a thought is present. **The rule survived. Nothing about it changes.**

---

## The reason axis — the same act, reached two ways, written two ways

> **When one act can be arrived at by two different routes, the two routes write two different
> openings — and the difference is WHY she is doing it, not how hot it is.**

Not a tier. Not a heat band. **Volition.** She chose this, or her body walked her into it.

Course of Temptation's most-returned-to screen (`ShowerStall`) offers masturbation behind two
different gates, and each writes its own intro text:

*Reached by the skill — she decided:*
> "You want to make yourself cum, and while the co-ed showers aren't exactly truly private, this
> stall closed off by a curtain is as close as you get to uninterrupted alone time in the residence
> hall. You start the water and duck under it, **ignoring how precarious your privacy is** as you
> begin running your hands over your body."

*Reached by arousal — her body decided:*
> "Even though it's definitely not exactly private here — just a couple curtains separating you from
> everybody else — **you're desperate for relief** and actual alone time is basically impossible to
> find in the residence hall. You start the water and duck under it, **taking a breath** as you
> immediately begin running your hands over your body."

Same room, same act, same fifteen minutes. One is a decision; the other is a need. Neither is
hotter than the other.

⚠️ **This is not R6's banned move.** `the-surfaces.md` R6 forbids rewriting a **hub's** first
sentence per stat band, and it is right — an arc whose base node rewrites itself per tier reads as N
different scenes rather than one escalating hub. This varies the **act's** intro by which route
opened it. The hub opener stays constant, exactly as Course of Temptation's does.

**How to build it.** The choice that routes into the act sets a flag or trait; the act's opening
beat is a `group` chain reading it. Adjacent `group` blocks merge into one if/elseif chain and first
match wins (`engine.md` §35, `v2.py:14561-14568`), so the branches must be mutually exclusive.

### It is field-wide, and we do it zero times

Measured 2026-09-03 across 23 female-lead games. Act screens — 3+ body words on the field's own
frozen list, chrome and UI panels excluded — whose **entry region carries a conditional before the
first body word**: **2,283 of 4,836, or 47.2%.** Of those, the ones that write two *full* openings
of ten words or more, both prose, in genuinely different states: **436, across 18 of the 23
games.**

⚠️ The first count was 575 and was inflated three ways, each found by reading rather than trusting:
a localization branch (`family-ties` on `$setting.lang`), a quest-hint panel that cleared the
body-word bar without being a scene, and mechanical who-does-what-to-whom role swaps
(`course-of-temptation`'s `EncounterPositions` on `_role is "top"`). Cleaned: 436 state-driven, 10
mechanical, 2 localization.

**Ours: zero.** `block_pool` — the primitive for exactly this — is used by no v2 game
(`engine.md` §35).

⚠️ And what those conditions read is **not** mostly her willingness. Of 7,042 state reads before an
act screen's prose starts: game-specific plot flags 36.4% · what has already happened 14.1% ·
the clock and where she is 12.9% · **willingness 12.2%** · her body and clothes 8.6% · skill 6.1% ·
**a die 6.0%** · upkeep 3.2%. Willingness is fourth, about level with a dice roll. **Reach for the
clock, the place, and what she is wearing before you reach for the meter.**

### Composure is subtraction

The uncertain version explains itself; the confident one does not need to (`road-to-success`,
numbers only: 84.6% of 39 willingness pairs put the composure on the high branch).

## What a scene contains

**Every scene with a named person answers seven tests, one line each.** The first three go on its
scene sheet (`the-sheets.md` S1); `v2-reader` judges all seven (`agents.md`, The Reader).

1. **Want** — what this person visibly wants here. On a sexual step, an **earlier** scene has already
   shown him wanting it (`the-arc.md` A13): wanting shown before it is acted on.
2. **Next step** — what goes one step further than last time.
3. **Hook** — what the scene points at next.
4. **Her voice at her level** — at a low level her own thought pushes back; at a high one it is
   appetite (`the-meters.md` W1b, "One event, several levels" below).
5. **Who notices** — someone in the world reacts to what she does, or the game has declared that
   nobody does (`the-meters.md` W5b).
6. **The written no** — where there is an offer, a refusal exists, is written and is priced
   (`the-surfaces.md` R5b).
7. **The body** — an explicit beat stays on the body to its last sentence (the pivot, above).

## One event, several levels

**Write the same event once per band of her meter, and let each band be her voice at that level.**
The low band keeps the pushback; the high band has lost it (`the-meters.md` W1b). Build it as a
`group` chain on her meter with mutually exclusive bands (`engine.md` §35).

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `shady-deals`' kiss, three tiers on `$p_depravity`
> (<15 / 15–34 / 35+): *"You lean in cautiously, pressing your lips to his with a soft
> hesitation."* · *"You kiss him eagerly, letting the heat linger between your mouths."* · *"You
> crash your lips against his, pushing your tongue in."*
>
> `in-her-own-hands` `[BR_MasturbateFA]`, three bands on one of her tastes: *"Hmmmm . . . should I?
> I haven't tried this before…"* · *"More, was the only thought I could form in my head."* ·
> *"Feeling particularly naughty today…"*
>
> One game (`zaras-school-life`, numbers only) writes a re-entered dinner at six rungs.

Same event, same length, same click. What changes is who she is when she does it.

---

## The two-halves sentence — one sentence, two people's meters

The most reusable sentence-level pattern in the field study, and it is **not random**. One explicit
sentence is built from two halves, each read off a different meter: **his arousal writes the first
clause, hers writes the second**, three bands each. Our own grid, from her side:

```
HIS arousal — the first half                         HER arousal — the second
  high  "He fucks your cunt hard, his cock           high  "You grind your clit on him and moan
         slamming in balls deep."                           through your orgasm."
  mid   "He fucks your cunt in slow, deep strokes,   mid   "You push your ass back to meet each
         his cock dragging all the way out."                thrust."
  low   "He fucks your cunt lazily, his cock half    low   "You bite your lip. You're not there yet,
         hard and slipping out."                            but you don't want him to stop."
```

> *"He fucks your cunt hard, his cock slamming in balls deep. You grind your clit on him and moan
> through your orgasm."* — 22 words, 7 explicit, median sentence 11.
> *"He fucks your cunt lazily, his cock half hard and slipping out. You bite your lip. You're not
> there yet, but you don't want him to stop."* — 27 words, 3 explicit, median 11.

Her low band is **reluctance that could turn**, never sex she endures (`the-release.md`, the
excitement read's instant fails). Written as one sentence each pair runs past the ceiling, so split
at the join.

**Nine outcomes from six written clauses**, and nothing is left to chance — read it twice at the
same arousal and it is the same sentence; read it as the meters move and it changes under you.

This is what a repeatable act surface should be built from. It is cheaper than nine scenes and it
never says the same thing twice in a row, because **the two halves move independently**.

Build it as nested `group` chains — one on his meter, one on hers — with mutually exclusive bands.

**Its sibling is the random pool.** Where the two halves are *deterministic* variety driven by
state, `block_pool` is *undirected* variety driven by a die (`engine.md` §35). Course of Temptation
and Family Ties use the die; DoL uses the state. Use the die when nothing in the fiction should
decide, and the state when something should. Our v2 games use **neither** — every repeatable act
surface in this repo says the same words on visit one and visit fifty.

---
---

# The other ninety percent — which is not one register, it is six

Everything above is about the explicit beat. Most of a game is not one, and the part that
varies is **not "how dense should the prose be." It is WHICH KIND OF SCREEN YOU ARE ON.**

That distinction is why the three passes before this one did not stick: each added a rule about
"prose" in general, applied it to hubs and capstones and sex loops alike, and got argued down by
the first screen where it read wrong.

**Measured 2026-08-18 across 25 shipped mopoga sandboxes** — 58,163 passages,
`~/Documents/Mopoga_Twine_Sandbox_Research_20260724/gamehtml/`. **The field is 27**; every figure
derived below was re-checked on all 27 by the 2026-08-24 end-of-study recheck, and this line records
the original run. Two corrections had to be made
before any number meant anything, and both are recorded because they are why earlier studies of
this same corpus got it wrong:

- **Count one rendered path, not every branch.** One `destroyer` act screen is eight `<<if>>` branches
  printing the same four words over a different image. Counting the source counts all eight.
- **Speech is a UI component, not punctuation.** 20 of the 27 render dialogue through
  `<<speech>>`, `<<say>>`, `<<nm "Karlee" "…">>`, `<<chat portrait "…">>`,
  `<div class="npctextbox">`, or one macro per character (`<<Mc>>`, `<<AmyBd>>`). A quote-counter
  sees none of it and reports the most spoken game in the corpus as 585 : 1 narration.

---

## The table — look up the kind, the shape is already decided

```
kind of screen             n      words   spoken   has a picture   clips   exits
room / hub             1,226         30       0%          41%         0       5
one-liner / stat tick  7,278         14       4%          21%         0       1
talk screen           15,774         55      65%          64%         1       1
ordinary scene        21,465         71      14%          36%         0       1
sex — act menu           164        107       8%          91%         1       5
sex — few exits        1,068        305      18%          86%         2       3
sex — one way on       7,161        228      28%          92%         3       1

a REVEAL BEAT          3,005         37        —          58%         1       —
```

Read three things off it before writing anything else.

**The room card is bare and the sex screen is not.** 30 words, nobody speaking, and **fewer than
half carry a picture at all** — against 86–92% for anything sexual. "Put media everywhere" is
wrong; media concentrates in sex and in talk, and a room that stays plain is the field agreeing
with itself.

**The two sexual shapes are different builds.** The **act menu** is short (107 words), quiet (8%
spoken), carries **one** clip, and its real content is the five exits — the player picks the next
rung. The **one-way scene** is twice as long, carries **three** clips, and is **28% spoken**. Same
subject matter, opposite construction. Writing both as short silent prose with one clip on top,
which is what every v2 game does, gets neither.

**The talk screen is the genre's second largest content kind** — 15,774 of 54,630 screens. See S4.

---

## S1 · The clip rides the beat

> **A clip at the top of a canvas is a clip for beat 0. Every beat that ESCALATES carries its own.**

This is an engine fact before it is a rule. A cascade renders as nested `<<linkreplace>>`
(`v2.py:14572` — the beat's blocks become the linkreplace body, `_render_cascade_tail` at `:14512`), so **every beat
appends below the last and nothing is ever removed.** The clip stays pinned where it was. By the
beat that is the act, it has scrolled away, and the player reads the payoff under a picture of the
setup.

```
the same unit — a click that reveals more content inside one screen
FIELD   apocalyptic-world 64% · become-taxi-driver 71% · destroyer 79% · new-lust 66%
        POOLED 3,005 reveal beats — 58% carry their own clip, median 37 words each
```

The field's density inside sexual content: **one clip every 58 prose words** (IQR 25–104, n =
25,502 gaps).

The field runs a median of 37 words per reveal beat, for reference only; the model beats set the length.
**The beat length was never the problem; the picture on the beat was.**

**Gate 31 · an explicit beat carries a clip.** ≥50% of beats with 3+ frozen-list words carry a
media block of their own. Half the field's per-screen figure, below its per-reveal figure.

### And here is the shape, because it was never written down

`engine.md` §5 says outright that a clip nested in a cascade beat "is the shape `register.md` S1
requires" — and then shows a node-level block, which is the thing this rule exists to stop.

Both blocks below are **one beat out of a cascade**, shown alone. In a real cascade **beat 0 carries
no `advance_text`** — it renders on entry — and so does a terminal beat; the `advance_text` is what
makes a beat a click. `v2.py:14426`.

**One-shot beat — a fixed `file`:**

```toml
{ type = "cascade", props = { beats = [
  { advance_text = "<the click that reveals this beat>", blocks = [
    { type = "paragraph", content = "You pull your top off slowly, so your neighbour knows it's for him. Your tits spill out and your nipples go hard. His mouth falls open. His cock strains against his jeans. You love it. You want him to beg." },
    { type = "video", props = { file = "<dir>/<clip>.webm", description = "<what is on screen, for the harvest pass>", search_queries = [ "<a query that would find it>", "<another>" ] } },
  ] },
] } },
```

**Repeatable surface — a `pool_dir`, and on a re-entered surface it is not optional:**

```toml
{ type = "cascade", props = { beats = [
  { advance_text = "<the click>", blocks = [
    { type = "paragraph", content = "He bends you over the arm of the couch. He fucks your cunt from behind, hard. One hand pins you flat between your shoulder blades. Your tits drag on the cushion every time he slams in. Your cunt clenches on his cock and you let the whole building hear it." },
    { type = "video", props = { pool_dir = "<dir>/<beat_name>", description = "<what is on screen>", search_queries = [ "<a query>", "<another>" ] } },
  ] },
] } },
```

The prose in both is lifted from `## The model beats` below — the validated set — so nothing new is
being taught about the writing here. **The only thing being shown is where the clip goes.**

⚠️ **`pool_dir` over `file` on anything re-enterable.** A pool **cycles** (1→2→3→1) through
`$game_state.media_cycle` rather than re-rolling, so the player never sees the same clip twice
running, and the count comes from disk instead of a number you have to keep correct. Gate
`repeatable explicit media cycles` judges exactly this. `engine.md` §5.

⚠️ **ONE ASSET, ONE BLOCK.** Never reuse a `file` or a `pool_dir` across two blocks. The media
review dedupes by file, so two beats sharing an asset collect **one** verdict between them, and the
second beat is reviewed by nobody.

⚠️ **The node lead's clip does not scroll away — the beats append underneath it.** A cascade renders
as nested `<<linkreplace>>` (`_render_cascade`, `v2.py:14426`), so nothing is ever removed. That is why a clip at the
top is a clip for beat 0 and cannot serve beat 4: by then the player is reading the act under a
picture of the setup.

---

## S2 · One canvas is one rung

> **The ladder is climbed ACROSS screens. A screen is one step of it.**

The field escalates by chaining 3–4 screens, each one rung, each with its own clip. Which rung a
screen's text opens on:

```
                     touch  strip  hands  oral  vaginal  anal  finish
FIELD                  13%    15%    11%   14%     28%     5%    13%
```

Evenly spread, because no single screen is the whole climb. We get this wrong in **both**
directions, and the two look nothing alike:

```
vesper       77% of its explicit canvases OPEN at vaginal-or-above; median 4 rungs in ONE canvas
             — the whole ladder with no stairs leading to it
forty_miles  69% never reach oral at all — all stairs, no ceiling
```

*This is not a general fault in our writing.* Our run-up is **longer** than the field's — 59–207
words before the first explicit word against the field's 30, and 0% of our canvases open explicit
against the field's 22–28%. The defect is where a canvas **starts and stops on the ladder**, not
that we rush into it.

A canvas that carries four rungs has no room to arrive; a canvas that carries one has nowhere to
go. Split them, and let the surface the player returns to carry the choice of which rung is next —
which is S1's other half and the act menu in `the-surfaces.md`.

**Lint · the ladder.** Prints the opening rung and the ceiling per game. A number, never a bar: a
field screen is one rung and ours is a scene, so no threshold across the two would be honest.

---

## S3 · Somebody speaks

> **Prefer a line of speech to a sentence describing a line of speech. If a person is in the room,
> they talk.**

```
FIELD   median 2.93 : 1 narration to dialogue        10 of 27 games at or under 2 : 1
```

**And the protagonist thinks instead.** When a person is present, she says it out loud — Cupid's
Way [Sister's place] puts the question in her mouth: *"What is so special about your lifestyle
that mom didn't like?"* A thought bubble used as a substitute for a conversation is the defect,
not the style.

> ### ⚠️ This rule was once deleted by a broken instrument
>
> `DOCTRINE_GAPS.md` Study 4 measured the field by counting text inside `"quote marks"`, reported a
> median of 33 : 1 and a spread "far too wide to threshold", and this file dropped v1's dialogue
> rule on that basis. Re-measured with each game's own speech convention read out of its source:
>
> ```
> game                 quotes only    + its own speech UI
> corpo-life               584.9:1               0.30:1
> sluttown-usa             762.0:1               0.63:1
> become-taxi-driver       142.1:1               0.72:1
> family-business            >999:1               1.15:1
> destroyer                 71.7:1               1.44:1
> the-company              290.1:1               2.69:1
> degrees-of-lewdity         3.6:1               3.62:1   ← unchanged
> course-of-temptation       4.6:1               4.57:1   ← unchanged
> patriarch                  2.9:1               2.93:1   ← unchanged
> MEDIAN                    65.3:1               2.93:1
> at ≤2:1                          0             10 of 27
> ```
>
> The three that do not move are the three that punctuate speech with quote marks. The study did
> not find the two most dialogue-heavy games in the corpus — **it found the two whose dialogue its
> instrument could see.** The "over 400 : 1" outlier that killed the rule is `corpo-life`, which is
> 70% spoken.
>
> v1's Rule 4 was right in direction and too extreme in number: its 0.73 : 1 came from one game.
> The field says 2.93 : 1.

**Gate 32 · somebody speaks.** Whole-game narration : dialogue ≤ 5 : 1 — above the field median and
above 18 of the 27, so it is slack rather than an invented line.

> Re-checked 2026-08-24 on the two games that used to parse to zero. Both are narration-heavy —
> `college-daze` 5.9 : 1, `free-cities` 9.7 : 1 — and both sit above the ceiling, so **only the
> denominators moved**: 10 of 25 became 10 of 27, 18 of 25 became 18 of 27, and the median holds.

**The exemption is real and narrow: nobody is there to speak.** A solo surface, an unseen peek, the
interior stretch of a capstone. A *present* character is never exempt, and "she is alone" stops
being true the moment the walk-in fires.

### Write the lines by PERSONALITY, not by person

The field's answer to "how do I get speech into a scene that six different people can walk into"
is not six sets of lines. Course of Temptation picks what a man says to her by his
**inclinations** — `dirtytalkidea` ("fuck pussy") and `dirtytalkcockenterspussy`:

| | what he wants | as he enters her |
|---|---|---|
| **forceful** | *"I'm going to ruin your pussy."* | |
| **crude** | | *"Oh yeah, take my cock."* |
| **passive** | *"I... I want to be inside you."* | |
| **neutral** | *"I want to fuck you."* | *"You're so tight."* |

**Shy** gets no lines of its own: it sets how *often* he speaks — 0.25 against crude's 0.8 and
neutral's 0.5. Thirteen such widgets exist in that game — `dirtytalkidea`, `dirtytalktits`, `dirtytalkgonnacum`,
`dirtytalkcumfacial`, `spitorswallow` and more. **Speech inside a generated scene is its own
subsystem**, and it is authored once for the whole cast.

Two things to carry out of that table:

- **The quietest setting is silence, rolled.** A shy man speaks a quarter of the time; the other
  three screens carry his breathing and his hands. A non-verbal beat is a legitimate answer to S3,
  and it came out of a lookup table rather than a moment of inspiration.
- **The axis is what KIND of person they are, not which person.** Write the shy line and the crude
  line once and assign them by an NPC trait. Ours would be a `group` chain on that trait, or a
  `block_pool` inside each branch (`engine.md` §35).

This scales the way our cast does: five characters × one shy/crude split costs two lines, not ten.
(`~/Documents/Female_PC_Craft_Study_20260823/findings_D_writing.md`)

### One term of address per person, and nobody else uses it

**This is the exception to the paragraph above, and the boundary
has to be held or the two rules read as contradictions:**

> The shy line and the crude line are written once and assigned **by trait** — that is what makes a
> generated scene affordable. **The name he calls her is not.** It is his, it is fixed, and no other
> character in the game uses it.

Measured across every captured line in two field games (`sluttown-usa` and `destroyer`; both fail
the adults-only rule, so the numbers are kept and the lines are not): six characters, each with one
term of address used on **5–18%** of their lines, 34 to 262 times.

**Roughly every sixth to twentieth line**, and the terms do not overlap anywhere in either cast.
It is the cheapest device in the whole study: one word, no system, no engine support, and it works
on the first line the player ever reads from that person.

One of the six is differentiated by **register** rather than by the term alone — an older woman
whose distinctive words are *perhaps*, *suppose*, *quite*. An author writing her speech on purpose. That is the upper end of this rule,
not its floor.

> ⚠️ **Do not over-read the measurement that found this.** The same instrument surfaces
> per-character spellings of noises, which are almost certainly accidents of typing rather than
> craft. **The address term is the reliable half; the noises are not a rule.**

---

## S4 · The talk screen is a content kind, not a garnish

15,774 of the corpus's 54,630 screens: **55 words, two-thirds spoken, one picture, one way out.**
Nearly a third of everything the genre ships, and it is the cheapest content there is — no media
hunt, no ladder, no state.

```
talk screens as a share of all canvases
FIELD 29%
```

**What it is for:** the person, not the plot. It is where a character becomes someone the player is
attached to — and across ~11,000 player comments, attachment to a character outscored praise for
the porn itself (`SKILL.md`, "the person is the product").

**Lint · talk screens.** Counts them as a share of all canvases.

---

## Sentences run short

| | median sentence |
|---|---|
| field, 17 games | **10 words** |
| the reference game | **9 words** |
| a game of ours, measured | **16 words** — third longest of eighteen |

**Escalate by adding beats, never by lengthening sentences.** Same rule as S2 one level down: a
longer sentence buys density, and density is what rots on the third re-read of a surface the
player returns to fifty times.

Gate 19 puts the ceiling at 14 — deliberately generous, calibrated across two extraction bases, so
treat a pass as "not drifting" rather than as "matches the field." The constant in `gates.py`
carries the full caveat.

## How far is far enough

`Sweeping backwards` above tells an author to replace the hedged clause with the specific one, and
it is right. **It has never said where to stop, and the measurement says nobody stops.**

Measured 2026-08-28, our built games against the field's built games, read identically — 28 of ours
against 25 of theirs. Both sides from `output/index.html`, because the two do not compare on any
other basis (see the ⚠️ below):

| per 1,000 words | field | ours |
|---|---|---|
| `-ly` adverbs | 8.9 – 22.6 (p50 13.5) | **1.3 – 8.6 (p50 3.2)** |
| hedge words — *just, almost, somewhat, seems, sort of* | 5.4 – 22.4 (p50 12.0) | **0.5 – 7.1 (p50 1.6)** |

**Twenty-eight of twenty-eight of our builds sit below the field's floor on adverbs, and
twenty-seven of twenty-eight on hedges.** Not most. Every
game this project has ever produced, under either skill. There is no game in the genre that writes
as bare as our barest, and no game of ours that reaches the genre's leanest.

**What that costs, in a reader's words.** From the thread that prompted this study: the prose *"puts
emphasis in the wrong places, needless details that are never mentioned again"*, so that it becomes
*"impossible for the author to foreshadow or draw attention."* That is what the numbers are
describing. Modifiers and hedges are the machinery English uses to say **this one matters and that
one does not**. Strip them everywhere and every noun on the screen arrives at the same weight — the
plot-critical object and the set dressing look identical, and the reader cannot sort them. A screen
where nothing is unimportant has nothing important on it either.

**The stopping point is not a number, it is a test.** Read the beat and ask which sentence you were
supposed to carry out of it. If every sentence is equally loaded, you have swept past the rule
rather than applied it.

**Over-stripped**, real shape, from one of our own games:

> The counter is at the front and the desk is at the back and there is a gate in the counter you
> have to lift to get between them. The book goes on the desk. The drawer is under the till side.

Three sentences, three objects, identical weight. Nothing tells the player that only one of them
will matter tomorrow.

**Weighted.** Same facts, same length, one thing marked down so another can carry:

> The counter is at the front and the desk is at the back, with a gate between them you have to
> lift every single time. The book goes on the desk, which barely matters. The drawer under the
> till side is the one he mentioned twice.

⚠️ **This is not permission to pad.** Padding was tested on the same corpus and refused: we run
roughly half the field's typo rate, a quarter of its duplicated-word rate, and we repeat phrasing
*less* than the field does. The instruction is to restore contrast, not volume. A beat that gains
words and keeps every sentence at the same weight has got worse, not better.

⚠️ **Why both sides are read from built HTML, and what it costs.** Our authored TOML holds only beat
prose; a built game also carries labels, sidebar, quest cards and room lists — thousands of words
with almost no modifiers in them. Reading our TOML against the field's HTML compares two different
things. **The cost: there is no clean field baseline for prose alone**, because the corpus exists
only as built pages. So the figures above are honest for whole games and there is no per-beat number
to write down — which is exactly why the stopping point is a test and the model beats below are the
doctrine.

⚠️ **The first version of this warning carried a wrong number and the mistake is worth keeping.** It
claimed our TOML runs **1.1x to 2.4x** hot against our own build. That was an artifact of the
measuring script, not of the seam: its tag-stripping pattern was bounded at 200 characters, and this
engine emits inline-styled `<img>` tags longer than that, so `object-fit`, `border-radius`, `lazy`
and `async` were counted as WORDS on our side only — field games write short `[img[...]]` markup and
were untouched. Unbounded, across six games, the same measurement moves **0.68x to 1.27x**. A rate
over word count really does survive this seam, which is what gate 43 has always claimed. **A number
that indicts an existing check deserves the same scepticism as one that flatters you.**

⚠️ **There is no article-density finding.** Read on one basis we sit at **65.0 per 1,000 against a
field median of 58.3**, inside the field's 33.3–86.0.

---

## The model beats

The set that did not exist. Before this, the whole skill held **419 words of worked prose example**
across 185,575 words of instruction — 0.23% — so an author had almost nothing to copy and modelled
the explanation instead. That is the fourth instance of `SKILL.md`'s *"an example outranks every
rule beside it"*, and the first where the failure was an **absence**.

One per kind in the table above, plus the one-time step and its daily repeatable. Second person,
the genre standard, and the loud voice ("The voice — say it loud"). Each was scored before it was
written down — the numbers are under each one, and they are the point: **a worked example that has
not been measured is a rule you cannot see.** Every person is a role, never a name, and no number
means anything: *"Show the mechanism. Never show the world."*

**Room / hub card** — the field writes 30 words, nobody speaking, fewer than half carrying a
picture. Nobody is there, so the voice is hers:

> The laundry is hot, loud, and smells like other people's sheets. Two machines take coins. The
> third says OUT in black marker. You hate this room. You come here anyway, because it's this or
> the sink.

*36 words · 5 sentences, median 7 · gloss 0 · negation 0 · history 0 — L3 applies, because a room
card is re-entered on every visit. "You hate this room" is rule 2: the feeling, said.*

**Reveal beat** — 37 words in the field, and 58% carry a clip:

> You pull your top off slowly, so your neighbour knows it's for him. Your tits spill out and your
> nipples go hard. His mouth falls open. His cock strains against his jeans. You love it. You want
> him to beg.

*40 words · 6 sentences, median 6 · 3 explicit words · gloss 0 · negation 0 · history 0. Her body,
then his reaction shown, then "You love it" — rule 2, the feeling said — and the last sentence names
what SHE wants next (rule 7). A reveal, not the act, so its last line may leave the body.*

**Talk screen** — the genre's second largest content kind, 55 words and 65% of it spoken. The
shape is rule 5: she speaks, the protagonist answers, she pushes, the protagonist thinks.

> "You're early," the woman at the register says. "Couldn't sleep?"
>
> "The apartment's too quiet."
>
> "Quiet's good. Quiet's cheap."
>
> *Easy for her to say. She gets to go home to somebody.*
>
> "Sit if you want. I'm here till nine and I like the company. But you're buying something,
> sweetheart. This isn't a library."

*52 words · **65% spoken** · gloss 0 · negation 0 · history 0 · median sentence 4. One thought, in
italics, between two spoken lines, never in place of them. She has her own want and says it, and
"sweetheart" is her term of address and nobody else's. The version this replaced said "That's twice
this week" on a screen that can be the first visit, which the truth rule now forbids.*

**Explicit beat, repeatable surface** — crude is the default, and the beat stays on the body for
its whole length. The thought gets its own beat, after:

> He bends you over the arm of the couch. He fucks your cunt from behind, hard. One hand pins you
> flat between your shoulder blades. Your tits drag on the cushion every time he slams in. Your
> cunt clenches on his cock and you let the whole building hear it.

> *You should hate how much you like this. You don't. Tomorrow you'll be right back on this couch.*

*Beat 1: 50 words · **5 explicit words** — `fuck`, `cunt` ×2, `tits`, `cock` — against the 3+ the
`explicit floor` gate uses · names the `vaginal` rung · median sentence 9 · body words in 3 of 5
sentences, including the last, so the pivot diagnostic passes. Beat 2: 18 words, 0 explicit, by
design: that is the interiority beat "Sweeping backwards" says not to fix.*

**One-time step, then its daily repeatable** — L3 below. The step
carries the reveal, the conversation and the hook, and plays once:

> The owner is counting the till when you walk in. He doesn't stop.
>
> "You're the new girl. You're late."
>
> "The bus was late."
>
> "Everybody's bus is late." He shuts the drawer. "Four hours, cash, and you smile at the regulars.
> That's the job."
>
> *Smile at the regulars. Sure. That's definitely all it is.*
>
> He looks you over, slowly, and he takes his time about it.
>
> "Friday I need a girl upstairs. Pays triple. Think about it."

*76 words · 49% spoken · median sentence 4 · gloss 0 · history 0. Who he is, what he wants and how
he sees her, in the first three lines (rule 7); the tension named (rule 8); a hook with a day on it
(rule 9).*

The repeatable the player gets every shift after it:

> "Apron's on the hook," the owner says, without looking up. "Smile."
>
> *He wants you smiling. The regulars want a lot more than that.*

*23 words · one spoken line · one visible want · no claim about any earlier shift, so it is true on
visit two and visit fifty.*

Read the set together: not one dash, the plain modifiers carry weight (*slowly · a lot · hard ·
every second*), and every screen with a person on it has that person talking.

Measured with
`gates.py --beat` (explicit words, median sentence, body words by sentence) and the load regexes
`GLOSS_RE`, `NEGATION_RE` and `HISTORY_RE` on narration only.

⚠️ **A soft word is not the same thing as a hedge.** *Slowly, a lot, hard* are modifiers and they
are load-bearing (the padding study: we write 4.22 `-ly` per 1,000 against a field floor of 8.87,
so there is nothing to cut). *Somehow, sort of, almost* are hedges, and the loud voice has even
less use for them than the quiet one did.

## Dashes stay rare

**Words to watch:** `—` and `–`, and the spaced `--` that becomes one.

**Why this rule exists.** Two players read a shipped game of ours and said the writing "smacks of
an underpowered AI." Dash density is the marker readers reach for most often when they say that.
Measured over the 25 game corpus:

| | dashes per 10,000 prose words |
|---|---|
| field p50 | **0.99** |
| field p90 | 17.5 |
| field p95 | 25.7 |
| field max (`apocalyptic-world`) | 35.4 |
| a game of ours, measured | **123.0**, which is 3.5x the corpus maximum |

Half the corpus writes fewer than one dash per ten thousand words. Gate 43 puts the ceiling at the
corpus **maximum**, so a game is only failed once it has left the distribution entirely. Treat a
pass as "still inside the field," never as a target.

**Rule.** A beat gets a dash when no other mark will do the job. Two dashes in one beat is a habit,
not a choice. When you find a pair holding an aside, the aside is usually a sentence.

**⚠️ The fix is never a comma.** This is the one wrong turn already taken here, and it is also what
the `humanizer` skill prescribes, so it will be suggested again. Swapping the mark leaves the joint
in place, the reader still holds the sentence open, and nothing reads easier. Measured across two of
our own games: dash rate fell 3.5x and comma joints per sentence went **up**. Split the sentence, or
cut the clause it was carrying.

**Before** (real, `mrs_vance`, two dashes in 43 words):

> Cade — your husband's eldest, and the only one of them with a reason to be in this kitchen —
> comes up for ten minutes on a Friday and stands rather than sits.

**The comma swap, which is not the fix.** Three commas now, and fourteen words sit between the
subject and its verb:

> Cade, your husband's eldest, and the only one of them with a reason to be in this kitchen, comes
> up for ten minutes on a Friday and stands rather than sits.

**After.** The aside was a sentence, so it became one:

> Cade comes up for ten minutes on a Friday and stands rather than sits. He is your husband's
> eldest, and the only one of them with a reason to be in this kitchen.

**This is the first rule in this file shaped as a subtraction,** and that is worth saying out loud.
Counted across the register doctrine, rules that tell an author to add something outnumber rules
that tell them to cut by roughly five to one. A register taught only in additions drifts one
direction, and the author cannot feel it happening from inside the prose.

## The load rules — hand the reader a fact, not a thing to work out

Subtractions two, three and four, and they came from the drift the section above predicted.

**Why these rules exist.** A reader put a shipped game of ours beside `new-life-project` — one of
the corpus's most-read female-PC games — and said ours was harder to follow. Every readability
instrument in this skill disagreed. The game passes gate 19 at a median sentence of **9 words**,
writes fewer `-ly` adverbs than the field's leanest game, and sits inside the field on every texture
marker gate 43 prints.

The reader was right and the instruments were pointed at the wrong quantity. **The prose is not fat.
It is loaded.** "What is not measured here" at the end of this file records a padding study across
five markers — `-ly` adverbs, hedge words, commas, repeated trigrams, vocabulary variety — that found
nothing to catch. That conclusion is correct for those five markers and covers none of the three
below, because the study measured **volume** and the defect is **load**: how much a reader has to
hold, infer, or already know to get to the end of a sentence.

**Measured over 27 corpus games (14.5M prose words) against every game in this repo, split by which
skill authored it:**

| | gloss / 1,000 words | negation, % of sentences | history, % of sentences |
|---|---|---|---|
| field p50 | 0.06 | **12.06** | 1.64 |
| field p90 | 0.19 | **16.38** | 3.94 |
| field p95 | 0.20 | **22.32** | 4.47 |
| field max | **0.24** `destroyer` | **25.76** `become-taxi-driver` | **5.41** `free-cities` |
| **games THIS skill authored (9)** | **1.34 – 2.71** | **19.0 – 40.5** | **4.8 – 12.1** |
| games the v1 skill authored (6) | 0.00 – 0.66 | **24.0 – 39.6** | 1.3 – 6.6 |
| above the field MAXIMUM | v2 **9/9** · v1 3/6 | **14 of 16, under BOTH skills** | v2 **8/9** · v1 2/6 |

**Nine of nine games this skill authored sit above the entire field's maximum on the gloss and the
history**, and the lowest of them runs 5.6x the field's worst game on the gloss. The games written
before this doctrine mostly do not. **This file taught it**, and "Sweeping backwards" above is the
mechanism: *replace the hedged clause with the specific one* tells an author to attach a specifying
clause, and `, which is the county's way of saying skilled tasks approved` **is** a specifying
clause. The rule is obeyed and the defect is the obedience.

The three rules are one idea at three grammatical addresses. **L2 was retired on 2026-09-24** when
the loud voice replaced the quiet one; L1 and L3 stand, and L3 now carries the truth rule's
exception.

### L1 · No `, which is` · no `, which means`

The sharpest of the three and the cleanest measurement in this file: **zero overlap.** The field's
worst game writes 0.24 per thousand words; our best writes 1.34.

The shape is a fact followed immediately by an explanation of the fact, welded into the same
sentence. It reads as craft while writing and as fog on arrival, because **a gloss is always more
abstract than the thing it glosses** — the reader is handed a concrete detail and then made to hold
it while a vaguer sentence lands on top.

Real, all from one 8,836-word game, which shipped twenty of them:

> ❌ "…never once seen him take a chair in here, **which is either respect or its exact opposite**."
> ❌ "…the orange sticker in the corner, **which is the county's way of saying skilled tasks approved**."
> ❌ "She turns it face down when you come in, **which is a different thing entirely**."
> ❌ "…the cushion has given up on the left side, **which is the side that works**."

**Rule.** Delete the clause, or make it its own sentence. **Deletion is the default** — in most cases
the fact was already doing the work and the gloss is the writer not trusting it.

| ❌ | ✅ |
|---|---|
| "She turns it face down when you come in, which is a different thing entirely." | "She turns it face down when you come in." |
| "…one sock on, which is as far as he got, and he has been sitting like that long enough that…" | "<name> sits on the edge of the bed with one sock on. He got that far and stopped." |
| "…the orange sticker, which is the county's way of saying skilled tasks approved." | "Two of your cards have an orange sticker. Orange means the county approved skilled tasks." |
| "…never once seen him take a chair, which is either respect or its exact opposite." | "Eleven weeks. <his son> has never sat down in this room. You have not worked out why." |

⚠️ **The fix is not a dash or a bracket.** Same error as the comma swap above: the joint survives the
swap and the reader still holds the sentence open. Cut it or split it.

### L2 · Negation — RETIRED 2026-09-24

The loud voice negates on purpose. `lint_negation` prints the share as a measurement, not a
verdict; do not rewrite a loud negation to satisfy it. History: CHANGELOG.

### L3 · A repeatable screen carries no history

Field max 5.41%; eight of our nine are above it, the worst at 12.1%.

A repeatable canvas is re-entered dozens of times. Backstory read on visit one is furniture by visit
nineteen, and it is the most expensive kind of sentence there — the reader has to reconstruct a
prior state of the world before the present one means anything.

> ❌ "The bed **they moved down** is against the wall where the couch **used to be**, and the couch is in the barn."
> ❌ "**Eight months** of the same man in the same chair and the cushion has given up on the left side."
> ❌ "There is a rail on the porch steps the county **put in**…"

Three inferences before anyone in the room does anything.

**Rule.** On a canvas with `trigger.is_repeatable = true`, every sentence nobody has gated is
something happening now. No *used to*, no *since*, no *eight months*, no *they moved*, no *the county
put in* — and, since the loud voice makes these claims constantly, no *last night*, *this week*,
*again*, *every time* on a line the player can read on their first visit.

**The one exception is the truth rule's rule 2:** a line about the past may show on a repeatable
when it sits inside a `group` whose `conditions` read the flag or counter that records that past.
*"You still owe me for last week"* belongs on the daily screen only once a payment has actually
been missed. That
line is then true on every visit it can render on, which is the whole test.

**And the big version is a one-time step** (added 2026-09-24). A moment with a reveal, a real conversation and a hook plays **once**, as a non-repeatable
canvas. The daily repeatable of the same scene stays short, but it is not mute: **one spoken line
and one visible want**, true on every visit. `## The model beats` above shows the pair. The field
does the same: of the scenes that carry the full *reason + want + change + pointer* shape,
repeatable screens run **0%** in a random sample of 52 and 5% in the curated library, against 70%
of quest and story beats — a curated-library figure, so read it as direction, not a rate
(the 2026-09-24 scene-content review, which read the 26 games' own source). `the-arc.md` A1 is the same idea one level up: the numbered steps
are one-time, and the repeatable is what they convert into.

**The facts are not deleted — they move.** Backstory belongs on a one-time canvas, where it lands
once, properly, and then stays out of the way:

> **Repeatable screen:** "You unlock <name>'s door and go in. His bed stands against the front-room
> wall, under the window that faces the road. He watches it. Always. He hears you in the hall and
> turns his head."
>
> **One-time canvas, same facts:** "<his son> and two neighbours carried <name>'s bed down out of the
> upstairs room in March. The couch went out to the barn to make space. He has slept in the front
> room ever since."

⚠️ **`the-clock.md` C2 already owns the neighbouring rule** — a beat may not say what *time* it is —
and it is complete, including the exemptions for a recurring hour (*"<his son> comes by at ten"*) and a
past one. **L3 is about elapsed time, not clock time.** Do not read one as the other.

### What one pass looks like

The anchor activity of a shipped game, every rule applied, nothing cut but load:

```
                   words  sentences  median  >20w   negation  history
before               319      17       20w   52.9%    41.2%    29.4%
after                254      36        8w    0.0%     2.8%     0.0%
field reference                         7w    7.7%     8.3%     3.1%
```

**Sixty-five words shorter, with every fact intact and the voice unchanged.** That is the shape of a
correct pass: the sentence count roughly doubles, the word count falls, and nothing is lost.

### Two checks measured and NOT built

Recorded here for the same reason the others are — so they are not proposed again.

- **Fragments (sentences under five words) — REFUSED.** The field runs 5.3% (`the-company`) to 58.6%
  (`family-ties`). No threshold survives that range, and our games sit inside it. This is the fifth
  check this skill has measured and turned down.
- **Stative `is` as the main verb — DEFERRED, not refused.** The field floor is 10.0%. It is
  downstream of L1 — a gloss is usually "which **is**" — so re-measure it after
  L1 has been applied to a game and see whether it moves on its own before inventing a number.

⚠️ **The history count is a proxy and the softest of the three.** It matches temporal markers
(*used to · ago · since · has been · N days/weeks/months/years*) and cannot tell a story from a
sentence that merely mentions a duration. It was tightened against a fourteen-case fixture before
these figures were taken — the loose version scored *"moved his hand"* as history — and it will still
over-count. Read the lint's list, not its number.

## The words the player has to already own

Every readability instrument in this skill measures **syntax**. A text can score easy on all of
them and still be hard, because the difficulty is **reference** — the reader has to already know
what the nouns point at:

> *"Nothing in the meter. You go to bed in a jumper and your socks and the coat over the top of
> the eiderdown."*

Three of those words — **meter** (a coin-fed prepayment meter), **jumper** (a sweater),
**eiderdown** (a quilt) — are short, ordinary-looking, and name objects the reader has to arrive
already holding. Short sentences do not help a reader who does not know what the nouns are.

**Measured — locale-locked common nouns, uses per 10,000 words.** The instrument is a **curated
list** of about forty regional terms, so it is a judgement, and it is named as one. The field, 27
games, reads **0.8**.

Eleven common regional words appear in **zero of 27 games across 14.7M words**: *airer,
anorak, bedsit, biro, chandlery, chippy, forecourt, fryers, holdall, lodger, wellies.* 

**Gloss it in the sentence that first uses it, or use the plain word.** *immersion → water heater ·
pitch → rent · chandlery → hardware shop · the front → the seafront · float → the till money · went
inside → went to prison.* Either the sentence carries the meaning or the word does not earn its
place. This costs nothing: the specificity that matters is what the thing is DOING, not which
regional name it has.

> ⚠️ **On a LABEL the "or" collapses — plain word, no exception.** A button cannot carry its own
> gloss. There is no sentence on it to put one in, and the player reads it *before* the prose that
> would have explained it. So a canvas `name`, a location `name` and a choice's `text` on a
> room list get the plain word every time, however well the paragraph behind them glosses it.
>
> A paragraph that glosses the word properly does not rescue the button that leads to it — the
> gloss is downstream of the label. In Her Own Hands [BobbyAwakeBase] puts the plain word on the
> button: *"Pay your rent"*. `the-voice.md` R1 owns label shape; this rule owns the word in it.

**Name a place for what it is, the first time you name it.** Course of Temptation [SummitMarket]
does it in the first sentence: *"You are outside the Summit Market, a building which contains the
eponymous market"*. Descriptive metadata never reaches the player: `image_search_queries` are
search terms, and a video block's `description` becomes only the `alt` text when its file is an
image (`v2.py:15835`) — an image block's `alt` comes from its own `alt` prop. Neither is on screen.
A location's kind belongs in the first sentence that names it, not in its metadata. (The map is
`the-map.md`'s; what the prose calls it is this file's.)

**Four ways a word fails, and only the first one is about dialect.** The rule was written for the
first one; the measurements found the other three:

| | what the reader gets | note |
|---|---|---|
| **unknown** — *airer, chandlery, forecourt* | a blank. They stall, or skim past it. | — |
| **ambiguous** — *half seven* | **a confident wrong answer.** It is 7:30 in Britain and 6:30 across much of Europe, and American English does not use the construction at all. | write the unambiguous *half past seven* |
| **false friend** — *vest, tea, bonnet, jumper* | **a confident wrong picture**, with nothing to signal it. | — |
| **collides with our own UI** — *meter* | a wrong picture again, but the competing meaning is **ours**, so no dialect check can ever find it. | Same exposure, unmeasured: **board, card, flag, state, tier, rung.** |

> ⚠️ **A false friend is a judgement about a sentence, never about a word.** Check the line it came
> from, not the lint's output.

An unknown word costs the reader a beat. **An ambiguous or false-friend word costs them the scene,
and they never find out they lost it** — which is why *half past seven*, *undershirt* and *dinner*
are not a downgrade. They are the only versions that survive contact with a reader who is not from
here.

> **Not this rule's business: spelling.** *Colour*, *grey*, *realise*, *behaviour* cost a reader
> nothing and are not swept — this skill and its games use them freely. The exceptions are the two
> that change the word rather than its dress: **tyre/tire** and **kerb/curb**. Comprehension is the
> test, never nationality.

**Invented words are safe. Real regional ones are the trap.** The fiction builds an invented word
on contact. A real object cannot be built that way — it either lands with the reader or it does not, and the prose
gets no signal either way. That asymmetry is the whole rule: **a made-up noun teaches itself, a
borrowed one cannot.**

> ⚠️ **This is not an instruction to write generic.** The register stays what it has always been —
> *specificity, not literary density.* A cardigan over a turtleneck is specific. An **airer** is
> not more specific than a **drying rack**; it is the same object with a smaller audience.
> Specificity the reader cannot decode is not specificity, it is noise.

**The check is a list, not a score.** `lint · the words the player has to already own` prints every
word in the player's face that fewer than four of the 27 field games use, ranked by how often you
used it, measured against `scripts/genre_words.txt` — 20,555 words of the field's own vocabulary,
data rather than taste. (18,043 on 25 games until the 2026-08-24 recheck; rebuilding on 27 added
2,512 words, 1,976 of them from the two games that had been parsing to zero.) **It is deliberately not a gate.**

**What separates a readable text from an unreadable one is what the words ARE, and no count can
see that.** A rate of unfamiliar words does not tell you which of them the reader will stall on.
That is exactly the condition under which a check must be a list and not a threshold. The lint
hands over the words; you make the call.

### The same rule for a phrase, not just a word

Everything above is scoped to **nouns** — *airer*, *eiderdown*, *chippy* — a thing the reader has to
arrive already holding. **A phrasal idiom does the same damage and slips straight through**, because
every word in it is common and none of it is regional.

The measured case came out of the load-rules pass. A rewrite drafted *to be the easy version* opened:

> ❌ "You **let yourself in** at seven."

Three facts folded into an idiom — she has a key, she does not knock, nobody greets her — and none
of the three is recoverable by a reader who does not already own the phrase. The plain version is
one word longer and carries all three:

> ✅ "You **unlock <name>'s door** and go in."

Same family, same games: *"the cushion has **given up** on the left side"*, *"neither of you is
going to **call it** a surprise"*, *"you both **let that stand**"*. Each one is a plain event
wearing a phrase.

**Rule. Where a plain verb exists, use it.** The test is the one this section already runs, applied
to a phrase instead of a word: *does this sentence hand the meaning over, or does it require the
meaning to arrive with the reader?*

⚠️ **No instrument, and deliberately.** Idiom rate was probed against a hand-built pattern list
(ours 0.79 per 1,000 words, `new-life-project` 0.26) and that list is far too weak to carry a number
— it would score idiomatic dialogue, which is exempt, and miss most of the prose cases. **Speech is
exempt in full**: a character may talk however that person talks. This is a rule for narration only,
and it has no lint.

### The false-friend half is hand-built, and this file is where it goes stale

`gates.py`'s `_FALSE_FRIENDS` is the authority — the corpus **structurally cannot** supply this
half, because a false friend is by definition a word four or more field games use. Which means the
only way an entry gets there is that somebody put it there, and the only way one goes missing is
that somebody wrote it here and stopped.

> ⚠️ **That is exactly what happened, and it is why LO hit the same wall twice.** This section
> opened on *"**meter** (a coin-fed prepayment meter), **jumper**, **eiderdown**"* and listed
> *pitch → rent* and *float → the till money* among its required swaps. `jumper` went into the
> checker on 2026-08-22. **`meter`, `pitch` and `float` did not** — so the word this whole section
> leads with was invisible to every instrument in the skill for a day, and reached a player on a
> button. **A word named here as a defect belongs in that dict in the same edit.**

Added 2026-08-23 after reading every hit in all 20 built games — `meter` (32 uses; the defect in
three games, metaphor in one), `float` (24; the till sense in six
games), `pitch` (10; the rent sense), `chemist` (3; all real).

**Measured and rejected, so the work is not redone:** `front` ×334 and `inside` ×213 are noise
(*"the front door"*, *"inside the room"*); `tip` ×44 carries only three real uses — a
7% signal rate would train the reader to skim the section; `boot` ×8 is footwear every single time,
with not one car boot in the repo; `bill` ×7 and `purse` ×10 give a slightly wrong picture that
does not cost the line. **The bar is not "could be misread." It is "misreads badly enough to lose
the reader the line, often enough to be worth its false positives."** `torch` is the reference
point: six of its eight hits are a *cutting* torch, and it stays, because the two it catches
are worth reading past six that announce themselves.

## The examples are the register

The rule above was never broken by anything anyone wrote in this skill. It was broken by what the
skill **showed**.

No line in `author-game-v2` has ever said "write British." But `templates/board.toml` shipped
`costs = "£5 for the immersion"` — a foreign currency symbol and a locale-locked noun in six words,
in the file authors copy hardest. Counted with word boundaries across the live reference files,
the skill carried **27 locale-locked terms across 11 files** — `airer` ×9, `lodger` ×8,
`immersion` ×3, `rota`/`rotas` ×3 — and glossed none of them. Five games came out written in that
dialect. The v1 games, built from a skill that happened not to use those examples, sit at the
field's rate.

> ⚠️ **Count with word boundaries, and check a surprising number before you act on it.**

**This is `SKILL.md`'s "an example outranks every rule beside it", third instance** — after
`the-map.md`'s worked map skeleton (inherited by three games) and `templates/board.toml`'s
`15/35/55/75` (inherited by all sixteen declared tiers). The rule already existed. It had only ever
been applied to **shapes** — a floor plan, a set of thresholds — and nobody thought to apply it to
**words**.

> **When you write a worked example, you are writing doctrine.** An example is the only part of a
> reference file that gets copied verbatim into a game. Anything you would not want in every game
> this skill ever produces does not belong in one.

**The fourth instance is an ABSENCE.** The skill once held 419 words of worked prose across 185,575
words of instruction (0.23%), so authors modelled the explanation, and dash rates ran 1.6 to 137
across builds from one skill. **Nothing outranks an example that was never written.** `## The model
beats` above is the answer, and the first thing to check when a habit shows up in every game and no
rule asked for it.

**The fifth instance:** the model beats were never re-scored against load rules added ninety lines
below them, and ran gloss 11.49 per 1,000 words against a field maximum of 0.24 until re-measured.

> **A rule added to this file dates every example above it.** The first four instances were about
> what an example *teaches*. This one is about what an example *stops being*: correct on the day it
> shipped, wrong by the next rule, and silent about the difference. When you add a rule here,
> re-score every worked example in the file before you commit — the examples are the register, so a
> rule the examples break is a rule that has already lost.

### Show the mechanism. Never show the world.

The four instances pull in opposite directions and nothing reconciled them, so the skill kept
choosing between two failures — instances 1–3 say an example is dangerous, instance 4 says an
absence is worse. Both are true, and the line between them is not how *big* the example is:

> **A mechanism copied verbatim produces a correct game. A world copied verbatim produces five
> games with the same box room.**

Every one of the first three failures was a **world**: a locale-locked vocabulary, one game's floor
plan, one game's tier numbers. All three are things an author should be *deciding*, and an example
decides them by default. The absence was a **mechanism** — where the clip goes, how a ladder is
gated, which key day-caps a rung. Those have one correct answer that does not vary by game, and an
author who has to derive them derives them differently every time.

So: **show the shape, name the slots, and leave every number and every proper noun out.** Placeholder
ids (`<npc_id>`, `<currency>`, `<exterior_location_id>`) are not decoration — they are the thing
that makes an example safe to copy. Where a number genuinely has to appear for the shape to read,
say in the same breath that the number is filler and name the rule that derives it.

⚠️ **This does not license a worked map.** `the-map.md` still refuses one, and the refusal is
correct under exactly this rule: a floor plan is a world however abstractly it is drawn. What that
file gained instead is the *mechanism* — one key, `entry_from`, present or absent — and no rooms.

## Second person is the genre standard

**13 of 17 games are second-person dominant.** Third person is a minority position held by three.
Our own most-second-person game runs 94% *you / your*.

`[settings] narration_person = "second"` is the default for a reason, and the field confirms it. It
stays **immutable once a release ships** — a person swap invalidates every line already written.

## What is not measured here

Whether the writing is any good, and whether it arouses. Neither is countable, both are the job.
`gates.py` measures shape. It cannot tell you the scene works.

It also measures **texture, on exactly one marker**: the dash rate, gate 43. That
is one countable habit and not a verdict on voice. Gate 43 prints three further numbers (joints per
sentence, the share of `you`, pronouns per name) which carry **no field figure and no threshold**,
because the corpus exists only as built HTML and none of the three survives the change of basis.
They are a trend line across our own games. Reading them as a score is the error the gate's own
header warns about, and it has already been made once.

**Padding is not measured, because it was measured and there is nothing to catch.** 2026-08-28,
prompted by readers of a shipped game saying the prose is long but says little: five markers —
`-ly` adverbs, hedge words, commas, repeated trigrams, vocabulary variety — each a rate per 1,000
words, over 25 field games and our 14. Our prose is not fat. It is **stripped**, and outside the
field's own range on the lean side: **13 of 14 games write fewer `-ly` adverbs than the field's
leanest game** (ours 4.22 per 1,000, field floor 8.87, field median 13.43), 10 of 14 the same for
hedges, and none of our games is above the field maximum on any of the five. The game the readers
were reading writes 3.01 and 4.00 and repeats phrasing *less* than the field. A ceiling set
anywhere in that range passes every game we own forever, so none was built — the fourth check this
skill has measured and turned down. Full method and data:
`~/Documents/Prose_Padding_Study_20260828/`.

⚠️ **That is a measurement, not a new rule.** Nothing here names a floor for a modifier, and no
reader asked for one. The direction is consistent with what this file already prescribes at
line 122 — *replacing the hedged clause with the specific one* — and whether it should run this
far past the field is an open question, not a defect to fix. What the same study DOES point at is
gate 43 above: set beside it, the shape is a **texture** — dash-joined, modifier-light, sentences
at the field median — and not a volume.

*(This file governs what the player reads **after** a click. Room names, button labels, guidance
cards and locked-door text are a different job with a different rule — `references/the-voice.md`.
Which machine a piece of content is built on — cascade or node-routed loop — is
`references/the-surfaces.md`. **Anything a beat says about WHEN — the hour it claims it is, the
days it says have gone by — is `references/the-clock.md`**, which owns the rule this file used to
carry as v1's Rule 10: a beat may not say what time it is, because it fires at any minute of a
window that runs 149–540 minutes wide.)*
