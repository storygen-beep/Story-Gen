# Register — what the player reads after a click

Two halves, and they are read at different moments.

**Part one — the explicit beat.** How to write the thing the game is for, and the one defect that
recurred three increments running. Read it when you are writing heat.

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

---
---

# The other ninety percent — which is not one register, it is six

Everything above is about the explicit beat. Most of a game is not one, and the part that
varies is **not "how dense should the prose be." It is WHICH KIND OF SCREEN YOU ARE ON.**

That distinction is why the three passes before this one did not stick: each added a rule about
"prose" in general, applied it to hubs and capstones and sex loops alike, and got argued down by
the first screen where it read wrong.

**Measured 2026-08-18 across 25 shipped mopoga sandboxes** — 58,163 passages,
`~/Documents/Mopoga_Twine_Sandbox_Research_20260724/gamehtml/`. Two corrections had to be made
before any number meant anything, and both are recorded because they are why earlier studies of
this same corpus got it wrong:

- **Count one rendered path, not every branch.** `destroyer:ginablow` is eight `<<if>>` branches
  printing the same four words over a different image. Counting the source counts all eight.
- **Speech is a UI component, not punctuation.** 20 of the 25 render dialogue through
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
(`v2.py:13952` — the beat's blocks are emitted *inside* the linkreplace body), so **every beat
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
FIELD   median 2.93 : 1 narration to dialogue        10 of 25 games at or under 2 : 1
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
> at ≤2:1                          0             10 of 25
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
above 18 of the 25, so it is slack rather than an invented line.

**The exemption is real and narrow: nobody is there to speak.** A solo surface, an unseen peek, the
interior stretch of a capstone. A *present* character is never exempt, and "she is alone" stops
being true the moment the walk-in fires.

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

## The words the player has to already own

Off Season scored **86.8 Flesch Reading Ease, grade 5.0 — easier than 24 of the 25 field games**
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
| the field, 25 games | **0.8** |
| our v1 games | 1.3 – 7.3 |
| our v2 games | **9.4 – 95.6** (off_season 95.6) |

Eleven words this skill's games lean on appear in **zero of 25 games across 10.6M words**: *airer,
anorak, bedsit, biro, chandlery, chippy, forecourt, fryers, holdall, lodger, wellies.*

**Gloss it in the sentence that first uses it, or use the plain word.** *immersion → water heater ·
pitch → rent · chandlery → hardware shop · the front → the seafront · float → the till money · went
inside → went to prison.* Either the sentence carries the meaning or the word does not earn its
place. This costs nothing: the specificity that matters is what the thing is DOING, not which
regional name it has.

**Name a place for what it is, the first time you name it.** Off Season's anchor is an amusement
arcade. Across the whole game the prose says *"forty machines"* and never once says *slot
machines*, so the building the plan gave **27% of the game's words** to is an unglossed noun.
(As built it holds 13% — a separate defect, on the `location fill` gate.) The words
`amusement arcade` and `slot machine` existed only in `image_search_queries` and in an image
`description`, which the engine renders as `alt` text (`v2.py:13750`) — invisible. A location's
kind belongs in the first sentence that names it, not in its metadata. (The map is
`the-map.md`'s; what the prose calls it is this file's.)

**Three ways a word fails, and the second and third are worse than the first.** The rule was
written for the first one and the measurements found all three:

| | what the reader gets | measured in our games |
|---|---|---|
| **unknown** — *airer, chandlery, forecourt* | a blank. They stall, or skim past it. | the class the skill's own examples taught — see below |
| **ambiguous** — *half seven* | **a confident wrong answer.** It is 7:30 in Britain and 6:30 across much of Europe, and American English does not use the construction at all. | **157 uses across six games**, against **4** uses of the unambiguous *half past* |
| **false friend** — *vest, tea, bonnet, jumper* | **a confident wrong picture**, with nothing to signal it. | `forty_miles`: *"You get the vest up over your tits"* — an undershirt here, a waistcoat to most readers, **inside an explicit beat**. `back_home`: *"He is going to be different at tea"* — the evening meal. `off_season`: *"Stay past the tea"* — and that one is a **quest card**, so it is UI. `seventh_day`: *"under the bonnet"* — a car hood, not a hat. |

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
word in the player's face that fewer than four of the 25 field games use, ranked by how often you
used it, measured against `scripts/genre_words.txt` — 18,043 words of the field's own vocabulary,
data rather than taste. **It is deliberately not a gate**, and the reason is worth stating because
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

## Second person is the genre standard

**13 of 17 games are second-person dominant.** Third person is a minority position held by three.
Our own most-second-person game runs 94% *you / your*.

`[settings] narration_person = "second"` is the default for a reason, and the field confirms it. It
stays **immutable once a release ships** — a person swap invalidates every line already written.

## What is not measured here

Whether the writing is any good, and whether it arouses. Neither is countable, both are the job.
`gates.py` measures shape. It cannot tell you the scene works.

*(This file governs what the player reads **after** a click. Room names, button labels, guidance
cards and locked-door text are a different job with a different rule — `references/the-voice.md`.
Which machine a piece of content is built on — cascade or node-routed loop — is
`references/the-surfaces.md`. **Anything a beat says about WHEN — the hour it claims it is, the
days it says have gone by — is `references/the-clock.md`**, which owns the rule this file used to
carry as v1's Rule 10: a beat may not say what time it is, because it fires at any minute of a
window that runs 149–540 minutes wide.)*
