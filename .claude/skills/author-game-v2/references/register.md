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

Everything in both halves came from a measured failure or a measured corpus. Nothing here is taste.

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

**Tested against the field 2026-08-23 and CONFIRMED, not loosened.** Zara's School Life folds heavy
interiority straight into its acts — and it never leaves the body: *"Her mind was a dark, focused
hum of power and arousal. The feel of his hard cock in her hand, the slick pre-cum on her thumb…
She wasn't just getting wet; her pussy was clenching with need, dripping for him."* That is not a
pivot by this rule's own definition, which is about what the sentence is *describing*, not whether
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

Zara's School Life does it *inside* one act, with two interiority paragraphs for the same hand under
the same table:

> *owning it* — "Her mind was a dark, focused hum of power and arousal… to prove **she owned this
> moment** and his pleasure."
> *owned by it* — "The reality of what she was doing was almost too much to process. **Her own body
> responded traitorously**… shocking, thrilling, and **deeply wrong**."

**Two different women doing the same thing.**

⚠️ **This is not R6's banned move.** `the-surfaces.md` R6 forbids rewriting a **hub's** first
sentence per stat band, and it is right — an arc whose base node rewrites itself per tier reads as N
different scenes rather than one escalating hub. This varies the **act's** intro by which route
opened it. The hub opener stays constant, exactly as Course of Temptation's does.

**How to build it.** The choice that routes into the act sets a flag or trait; the act's opening
beat is a `group` chain reading it. Adjacent `group` blocks merge into one if/elseif chain and first
match wins (`engine.md` §35, `v2.py:14561-14568`), so the branches must be mutually exclusive.

---

## The two-halves sentence — one sentence, two people's meters

The most reusable sentence-level pattern in the field study, and it is **not random**.

Degrees of Lewdity's `actionsothermouthpenisthrust` (`Widgets Actions Text`, 1,777 chars) is a
**3×3 grid**. His arousal writes the first clause; hers writes the second:

```
HIS arousal — the first clause          HER arousal — the second
  high  "ruthlessly fucked"               high  "Driven by instinct, you push back as you approach your peak."
  mid   "hungrily enveloped"              mid   "You push back against the movements."
  low   "rhythmically engulfed and…"      low   "You push back, trying to reduce your discomfort."
```

> *"Your cock is ruthlessly fucked by their mouth. Driven by instinct, you push back as you approach
> your peak."*
> *"Your cock is rhythmically engulfed and regurgitated by their mouth. You push back, trying to
> reduce your discomfort."*

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

- **Count one rendered path, not every branch.** `destroyer:ginablow` is eight `<<if>>` branches
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
OURS    vesper 16 of 389 (4%) · back_home 0/169 · steam 0/623 · forty_miles 0/938
        · seventh_day 0/516 · the_allowance 0/39
```

Media in our games lives on **nodes** (20–54% of them carry one) and essentially never on beats —
and v2 games moved nearly all their content *into* beats. `forty_miles` ships 938 beats against
259 nodes.

The field's density inside sexual content: **one clip every 58 prose words** (IQR 25–104, n =
25,502 gaps). Ours run one every 178–435.

Note the field's 37 words per reveal beat. That is v1's 35–40 rule landing dead on — **the beat
length was never the problem; the picture on the beat was.**

**Gate 31 · an explicit beat carries a clip.** ≥50% of beats with 3+ frozen-list words carry a
media block of their own. Half the field's per-screen figure, below its per-reveal figure.

### And here is the shape, because it was never written down

`engine.md` §5 says outright that a clip nested in a cascade beat "is the shape `register.md` S1
requires" — and then shows a node-level block, which is the thing this rule exists to stop. Counted
2026-08-29: **no worked example anywhere in this skill put a media block inside a beat.** Stated
here, stated there, modelled in neither — and the games read exactly like that
(`back_home` 0/169, `steam` 0/623, `forty_miles` 0/938).

Both blocks below are **one beat out of a cascade**, shown alone. In a real cascade **beat 0 carries
no `advance_text`** — it renders on entry — and so does a terminal beat; the `advance_text` is what
makes a beat a click. `v2.py:14426`.

**One-shot beat — a fixed `file`:**

```toml
{ type = "cascade", props = { beats = [
  { advance_text = "<the click that reveals this beat>", blocks = [
    { type = "paragraph", content = "She gets the shirt off over her head, slowly enough that it is clearly for you, and underneath she is exactly as good as you had spent the week trying not to picture. Then she waits, arms at her sides, and lets you look." },
    { type = "video", props = { file = "<dir>/<clip>.webm", description = "<what is on screen, for the harvest pass>", search_queries = [ "<a query that would find it>", "<another>" ] } },
  ] },
] } },
```

**Repeatable surface — a `pool_dir`, and on a re-entered surface it is not optional:**

```toml
{ type = "cascade", props = { beats = [
  { advance_text = "<the click>", blocks = [
    { type = "paragraph", content = "He bends you over the arm of the sofa and works his cock into your cunt without much ceremony, and it is good in the dumb, immediate way that has nothing to do with whether you like him. You hear the noise you make. You do not stop making it." },
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
OURS    the_inheritance 1.5 · vesper 2.8 · last_call 6.6 · late_shifts 15.3
        steam 18.7 · back_home 24.1 · forty_miles 31.1 · the_allowance 50.4 · seventh_day 62.0
```

`the_allowance` ships **216 spoken words in the entire game**. `seventh_day` 410. Every v2 game
sits beyond the worst dialogue-bearing game in the corpus.

**And the protagonist thinks instead.** Thought-bubble words divided by spoken words: seventh_day
**4.6**, forty_miles 3.1, the_allowance 2.0, steam 1.5, back_home 1.4 — against vesper 0.14 and
the_inheritance 0.00. The bubble was for an **NPC's** interior in the first place; used as a
substitute for a conversation it is the defect, not the style.

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
is not six sets of lines. Course of Temptation's `dirtytalkcuminside` picks by that NPC's
**inclinations**, crossed with what they want:

| | wants it | does not |
|---|---|---|
| **shy** | *"Please... cum inside me..."* | *She opens her mouth as if to say something, then closes it again.* |
| **crude** | *"Fill me up with your fucking cum."* | *"Not fucking inside."* |
| **crude + dominant** | — | *"Don't cum inside me or I'll rip your balls off."* |
| **neutral** | *"Cum in my pussy!"* | *"Pull out, please."* |

Thirteen such widgets exist in that game — `dirtytalkidea`, `dirtytalktits`, `dirtytalkgonnacum`,
`dirtytalkcumfacial`, `spitorswallow` and more. **Speech inside a generated scene is its own
subsystem**, and it is authored once for the whole cast.

Two things to carry out of that table:

- **The best line in the set has no words in it** — *"She opens her mouth as if to say something,
  then closes it again."* A non-verbal beat is a legitimate answer to S3, and it came out of a
  lookup table rather than a moment of inspiration.
- **The axis is what KIND of person they are, not which person.** Write the shy line and the crude
  line once and assign them by an NPC trait. Ours would be a `group` chain on that trait, or a
  `block_pool` inside each branch (`engine.md` §35).

This scales the way our cast does: five characters × one shy/crude split costs two lines, not ten.
(`~/Documents/Female_PC_Craft_Study_20260823/findings_D_writing.md`)

### One term of address per person, and nobody else uses it

Added 2026-08-24 from Section G. **This is the exception to the paragraph above, and the boundary
has to be held or the two rules read as contradictions:**

> The shy line and the crude line are written once and assigned **by trait** — that is what makes a
> generated scene affordable. **The name he calls her is not.** It is his, it is fixed, and no other
> character in the game uses it.

Measured across every captured line in two field games:

| game | person | lines | their term | rate |
|---|---|---|---|---|
| `sluttown-usa` | India | 2,809 | **"pet"** ×262 | 9% |
| `sluttown-usa` | Alex | 633 | **"sir"** ×47 | 7% |
| `sluttown-usa` | AJ | 714 | **"daddy"** ×34 | 5% |
| `destroyer` | Stepsister | 449 | **"bro"** ×58 | 13% |
| `destroyer` | Granny | 413 | **"darling"** ×37, "dear" ×23, "sweetheart" ×15 | 18% |
| `destroyer` | Aunt | 516 | **"baby"** ×32, "sweetie" ×11 | 8% |

**Roughly every sixth to twentieth line**, and the terms do not overlap anywhere in either cast.
It is the cheapest device in the whole study: one word, no system, no engine support, and it works
on the first line the player ever reads from that person.

`destroyer`'s Granny is the one character differentiated by **register** rather than by the term
alone — beside "darling" and "dear", her distinctive vocabulary is *"perhaps"*, *"suppose"*,
*"quite"*. An author writing an older woman's speech on purpose. That is the upper end of this rule,
not its floor.

**Ours:** `the_season` ships 56 NPC lines and **only Rae ever addresses Cass at all** — *"girl"*
twice, *"Renfro"* once. Boyd, Wade, Prine and Emmett never call her anything. Her father, in nine
lines, never once says his daughter's name.

> ⚠️ **Do not over-read the measurement that found this.** The same instrument surfaces
> per-character moan spellings — Stepmom "ahhh/gulp", Stepsister "mhnmhnm/fuuck", Cousin
> "aaah/woof" — which are almost certainly accidents of typing rather than craft. **The address
> term is the reliable half; the noises are not a rule.**

---

## S4 · The talk screen is a content kind, not a garnish

15,774 of the corpus's 54,630 screens: **55 words, two-thirds spoken, one picture, one way out.**
Nearly a third of everything the genre ships, and it is the cheapest content there is — no media
hunt, no ladder, no state.

```
talk screens as a share of all canvases
vesper 26%  ·  steam 5%  ·  forty_miles 1%  ·  back_home 0%  ·  seventh_day 0%  ·  the_allowance 0%
FIELD 29%
```

Vesper is already at the field standard. Every v2 game is at nothing. We have had the `dialog`
block the whole time.

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

⚠️ **One finding was withdrawn on this same test and is recorded so it is not re-proposed.** Article
density (*the / a / an*) was measured, reported as our largest and most invisible habit at 101 per
1,000 against a field maximum of 86, and **it was an artifact of the seam**. Read on one basis we
sit at **65.0 against a field median of 58.3**, inside the field's 33.3–86.0 with **3 of 28 builds
above the maximum and 5 below the minimum**. Modestly above the middle of the genre, nowhere near
outside it. There is no article finding.

---

## The model beats

The set that did not exist. Before this, the whole skill held **419 words of worked prose example**
across 185,575 words of instruction — 0.23% — so an author had almost nothing to copy and modelled
the explanation instead. That is the fourth instance of `SKILL.md`'s *"an example outranks every
rule beside it"*, and the first where the failure was an **absence**.

One per kind in the table above. Each is correct as written: no before, no diagnosis, nothing to
un-learn. Second person, the genre standard.

**Room / hub card** — the field writes 30 words, nobody speaking, fewer than half carrying a picture:

> The laundry runs hot even in winter and it never quite loses the smell of other people's sheets.
> Two machines work. The third has been out since spring and nobody has come about it.

**Reveal beat** — 37 words in the field, and 58% carry a clip:

> She gets the shirt off over her head, slowly enough that it is clearly for you, and underneath
> she is exactly as good as you had spent the week trying not to picture. Then she waits, arms at
> her sides, and lets you look.

**Talk screen** — the genre's second largest content kind, 55 words and 65% of it spoken:

> "You're early." She doesn't look up from the till. "That's twice this week."
>
> You could tell her the truth, which is that the flat is unbearable before dark. You say nothing
> instead, and she lets it go, which is somehow worse than if she had pushed.

**Explicit beat, repeatable surface** — crude is the default here, and the beat stays on the body
for its whole length:

> He bends you over the arm of the sofa and works his cock into your cunt without much ceremony,
> and it is good in the dumb, immediate way that has nothing to do with whether you like him. You
> hear the noise you make. You do not stop making it.

Read the four together and the point is in what they are not: not one dash between them, and the
soft words are load-bearing. *never quite · slowly · clearly · exactly · somehow · without much
ceremony.* Take those out and every sentence flattens to the same volume, which is the defect this
section exists to stop.

## Dashes stay rare

**Words to watch:** `—` and `–`, and the spaced `--` that becomes one.

**Why this rule exists.** Two players read a shipped game of ours and said the writing "smacks of
an underpowered AI." Dash density is the marker readers reach for most often when they say that,
and until 2026-08-27 nothing in this skill mentioned it. Measured over the 25 game corpus:

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

## The words the player has to already own

Off Season scored **86.8 Flesch Reading Ease, grade 5.0 — easier than 26 of the 27 field games**
(field median 78.0), and passed gate 19 at a median sentence of 10 words. It was then read by a
human who could not follow it.

Every readability instrument in this skill measures **syntax**. The difficulty was **reference**:

> *"Nothing in the meter. You go to bed in a jumper and your socks and the coat over the top of
> the eiderdown."*

Three of those words — **meter** (a coin-fed prepayment meter), **jumper** (a sweater),
**eiderdown** (a quilt) — are short, ordinary-looking, and name objects the reader has to arrive
already holding. Short sentences do not help a reader who does not know what the nouns are.

**Measured — locale-locked common nouns, uses per 10,000 words.** The instrument is a **curated
list** of about forty regional terms, so it is a judgement, and it is named as one:

| | |
|---|---|
| the field, 27 games | **0.8** |
| our v1 games | 1.3 – 7.3 |
| our v2 games | **9.4 – 95.6** (off_season 95.6) |

Eleven words this skill's games lean on appear in **zero of 27 games across 14.7M words**: *airer,
anorak, bedsit, biro, chandlery, chippy, forecourt, fryers, holdall, lodger, wellies.* Re-checked
2026-08-24 directly against both newly-readable games' prose: still zero, every one of them.

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
> **This seam is how the defect shipped.** Off Season's meter is glossed properly — *"the slot is
> at shoulder height beside the water heater… a card taped under it saying what three buys"* — and
> the player reaches that sentence only by clicking **`Feed the meter ($3)`**, the words they could
> not read. The gloss was downstream of the button the whole time. `the-voice.md` R1 owns label
> shape; this rule owns the word in it, and neither file said so until 2026-08-23.

**Name a place for what it is, the first time you name it.** Off Season's anchor is an amusement
arcade. Across the whole game the prose says *"forty machines"* and never once says *slot
machines*, so the building the plan gave **27% of the game's words** to is an unglossed noun.
(As built it holds 13% — a separate defect, on the `location fill` gate.) The words
`amusement arcade` and `slot machine` existed only in `image_search_queries` and in an image
`description`, which the engine renders as `alt` text (`v2.py:13750`) — invisible. A location's
kind belongs in the first sentence that names it, not in its metadata. (The map is
`the-map.md`'s; what the prose calls it is this file's.)

**Four ways a word fails, and only the first one is about dialect.** The rule was written for the
first one; the measurements found the other three:

| | what the reader gets | measured in our games |
|---|---|---|
| **unknown** — *airer, chandlery, forecourt* | a blank. They stall, or skim past it. | the class the skill's own examples taught — see below |
| **ambiguous** — *half seven* | **a confident wrong answer.** It is 7:30 in Britain and 6:30 across much of Europe, and American English does not use the construction at all. | **157 uses across six games**, against **4** uses of the unambiguous *half past* |
| **false friend** — *vest, tea, bonnet, jumper* | **a confident wrong picture**, with nothing to signal it. | `forty_miles`: *"You get the vest up over your tits"* — an undershirt here, a waistcoat to most readers, **inside an explicit beat**. `back_home`: *"He is going to be different at tea"* — the evening meal. `seventh_day`: *"under the bonnet"* — a car hood, not a hat. |
| **collides with our own UI** — *meter* | a wrong picture again, but the competing meaning is **ours**, so no dialect check can ever find it. | `off_season` renders **four meters in its sidebar** — arousal, warmth, energy, money — and puts `Feed the meter ($3)` on a room button, where it reads as *top up a stat bar*. Same exposure, unmeasured: **board, card, flag, state, tier, rung.** |

> ⚠️ **One of these examples was wrong, and it was ours.** This row cited `off_season`'s *"Stay
> past the tea"* as the meal sense on a quest card. It is not: the scene it labels is *"You make
> two teas in the two mugs he owns and you do not leave when yours is finished"* — **the drink**,
> and correct in every English there is. All nine `tea` uses in that game are the drink, including
> the hunger band *"Running on tea."* The word was read off the lint's output and never checked
> against the line it came from, which is the exact failure this whole section exists to name.
> **A false friend is a judgement about a sentence, never about a word.** The row stays and the
> game keeps its nine — the same call `torch` gets in vesper.

An unknown word costs the reader a beat. **An ambiguous or false-friend word costs them the scene,
and they never find out they lost it** — which is why *half past seven*, *undershirt* and *dinner*
are not a downgrade. They are the only versions that survive contact with a reader who is not from
here.

> **Not this rule's business: spelling.** *Colour*, *grey*, *realise*, *behaviour* cost a reader
> nothing and are not swept — this skill and its games use them freely. The exceptions are the two
> that change the word rather than its dress: **tyre/tire** and **kerb/curb**. Comprehension is the
> test, never nationality.

**Invented words are safe. Real regional ones are the trap.** `vesper` writes *emitter*, *sternum*,
*coveralls*, *readout* and reads fine, because the fiction builds each of them on contact. A real
object cannot be built that way — it either lands with the reader or it does not, and the prose
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
2,512 words, 1,976 of them from the two games that had been parsing to zero.) **It is deliberately not a gate**, and the reason is worth stating because
it looks like a contradiction.

The curated list at the top of this section separates our games from the field cleanly — 0.8
against 9.4–95.6. **The shippable, data-driven instrument does not separate them at all.** Its rate
across our ten built games:

```
seventh_day 91 · the_inheritance 94 · steam 107 · back_home 114 · vesper 114
late_shifts 118 · the_allowance 139 · last_call 139 · forty_miles 190 · off_season 205
```

v1 and v2 interleave completely, and the lowest and highest are both v2 games. `vesper` at 114
reads fine; off_season at 205 does not; `seventh_day` at 91 is the cleanest number here and is not
the cleanest game. **What separates them is what the words ARE, and no count can see that.** So the
measurement that discriminates cannot be shipped — it is a hand-built list — and the measurement
that can be shipped does not discriminate. That is exactly the condition under which a check must
be a list and not a threshold. The lint hands over the words; you make the call.

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
off_season, the_allowance and forty_miles, metaphor in vesper), `float` (24; the till sense in six
games), `pitch` (10; off_season's rent), `chemist` (3; all real).

**Measured and rejected, so the work is not redone:** `front` ×334 and `inside` ×213 are noise
(*"the front door"*, *"inside the room"*); `tip` ×44 carries only back_home's three real uses — a
7% signal rate would train the reader to skim the section; `boot` ×8 is footwear every single time,
with not one car boot in the repo; `bill` ×7 and `purse` ×10 give a slightly wrong picture that
does not cost the line. **The bar is not "could be misread." It is "misreads badly enough to lose
the reader the line, often enough to be worth its false positives."** `torch` is the reference
point: six of its eight hits are vesper's *cutting* torch, and it stays, because the two it catches
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

> ⚠️ **The first count of this was wrong and is worth keeping.** It was taken with a substring
> grep and reported `rota` ×44 — because *p·rota·gonist*, *rota·ting* and *rota·tion* all contain
> it. The real figure is three. A measurement that inflates a defect fourteen-fold is the same
> class of error as one that hides it: **count with word boundaries, and check a surprising number
> before you act on it.**

**This is `SKILL.md`'s "an example outranks every rule beside it", third instance** — after
`the-map.md`'s worked map skeleton (inherited by three games) and `templates/board.toml`'s
`15/35/55/75` (inherited by all sixteen declared tiers). The rule already existed. It had only ever
been applied to **shapes** — a floor plan, a set of thresholds — and nobody thought to apply it to
**words**.

> **When you write a worked example, you are writing doctrine.** An example is the only part of a
> reference file that gets copied verbatim into a game. Anything you would not want in every game
> this skill ever produces does not belong in one.

**The fourth instance is an ABSENCE, and it is the one that got a game read on a forum.** The first
three were things this skill *showed*: a locale-locked vocabulary, a map skeleton, a set of
thresholds. Counted 2026-08-28, the whole of `author-game-v2` held **419 words of worked prose
example, in 13 blocks, across 185,575 words** — 0.23%. The examples were not teaching a bad habit;
measured, they sit inside the field on every marker. **There were almost none of them.** So an
author reads a hundred and eighty-five thousand words of explanation and models *that*, and with no
worked beat anchoring anyone the games scatter: our dash rates run **1.6 to 137 across builds from
one skill**. An example outranks every rule beside it — and **nothing outranks an example that was
never written.** `## The model beats` above is the answer, and it is the first thing to check when
a habit shows up in every game and no rule anywhere asked for it.

> ⚠️ **The count that produced this was wrong twice before it was right, and the failures are the
> lesson.** A line-level pass over blockquotes reported 4,104 words of "example" across 11 files,
> every one off-field — because a wrapped continuation line of an explanation does not begin with a
> warning marker and reads as narrative. A whole **paragraph** is the unit, and it counts only if
> all of it reads as narrative. The wrong count had a fix attached to it (*rewrite the examples*)
> that would have edited prose which was never the problem.

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

Since 2026-08-27 it also measures **texture, on exactly one marker**: the dash rate, gate 43. That
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
