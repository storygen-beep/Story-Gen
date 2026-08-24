# The Meters — which ones exist, what the climb costs, and what the player reads off it

The ascent tiers are this skill's whole thesis: **a meter that buys access.** Every other file here
is about *what* the meter unlocks. This one is about the meters themselves.

**Three parts, and they are read in order.**

**W1–W6 — which meters exist and who owns them.** The decision that comes before every other one on
this page: does the PLAYER climb or does the CAST, what a throttle is actually for, how deep a
ladder goes, and whether a number anything reads. Missing entirely until 2026-08-19, which is why
five games shipped the same meters without anyone choosing them. **W5b** (2026-08-24) covers the
one meter that breaks W5's rules on purpose — a *"who knows about her"* meter, which rises and
almost never refuses.

**M1–M7 — the ascent, and what it costs to raise.** Missing until 2026-08-16, and the difference
between an ascent and a button.

**M8–M10 — the body.** A need falls on its own, she refills it, and while it is empty something is
shut. Missing until 2026-08-18.

> **Measured failure it prevents.** A game shipped with three correctly-declared ascent tiers, gates
> at 15/35/55 on all three, every penetrative scene properly behind one, and **not a single brake on
> any of them.** Live, in the built game:
>
> ```
> 12 clicks of one choice — "Read the fourth rule again."
> cover  4 → 16     (crossed the cover-15 band)
> energy 100 → 100      money 2 → 2
> clock  Monday 05:57 → Monday 08:33
> ```
>
> `+1 cover · 10 minutes · no cost · no cap · no daily limit · repeatable forever.` Cover 0→55 is
> 55 clicks, about nine hours of one Monday. All three tiers top out inside two in-game days. The
> game scored **22/24** and no gate asked the question.

> **This file adapts material from the incumbent `author-game` skill**, which had solved most of
> this and which v2 never carried over — `author-game/references/trait-design.md` ("The throttle
> menu"), `rts-design-philosophy.md` P8, and `trait-catalog.md` §5. Rewritten in v2's vocabulary
> (tiers, rungs, hubs, standing surfaces) rather than v1's (lanes, stages, arcs). **Every engine
> claim was re-verified against `v2.py` at its current line** — v2's own citations were measured
> drifting by six, so nothing here was copied on trust. Mechanisms live in `references/engine.md`
> §27–§30; this file cites them and does not restate them.

---

# Which meters exist, and who owns them

M1–M10 govern meters you have already decided to have. This part is the deciding.

> **Measured 2026-08-19 across 25 mopoga sandboxes**, SugarCube passage source,
> `~/Documents/Mopoga_Twine_Sandbox_Research_20260724/gamehtml/`.
>
> ⚠️ **One instrument correction, and it changes every figure below.** `<<if $lust lt 0>>` is a
> **clamp guard**, not a content gate — `corpo-life` carries **2,889** of them on one variable. A
> first pass counted them and reported that meter at 3,235 gates when the real figure is **346**.
> Every number here counts only comparisons against a threshold strictly inside the meter's own
> range. Same failure family as the quote-only dialogue count that wrongly retired v1's Rule 4
> (`register.md` S3): an instrument that cannot tell a guard from a gate does not report a smaller
> number, it reports the **wrong** one.

---

## W1 · Who climbs — and it is a fork, not a default

> **Declare `board.who_climbs` before you name a single meter. The field does not converge on one
> answer; it SPLITS, and there is nothing in the middle.**

Share of character-meter gating carried by **per-character** meters rather than player meters:

```
ROSTER — the cast is what changes
  zaras 100% · adam-and-gaia 100% · become-taxi-driver 91% · become-someone 84%
  the-hellfire-club 80% · patriarch 79% · love-and-vice 73% · family-business 65%        (8 games)
────────────────────────────────────────────────────────────────────────────────────────────────
LADDER — the player is what changes
  new-lust 15% · friends-of-mine 13% · corpo-life 12% · destroyer 12% · degrees-of-lewdity 10%
  wasteland-lewdness 5% · family-ties 0% · the-company 0% · sluttown-usa 0%              (9 games)
```

**Nothing sits between 15% and 65%.** And the field's raw weight is on the cast: **285 per-character
meters against 101 player-owned ones**, 2.8 : 1, with the biggest games carrying 46–91 of them.

Ours, measured the same way: **20% · 22% · 19% · 29% · 29%.** All five v2 games sit inside a band no
shipped game in the corpus occupies — not because the middle was chosen, but because **the question
was never asked.** v1 asks it (`author-game/references/content-framework.md`, *"Who climbs?"*); v2
dropped it, and one template answered it five times by default.

| `who_climbs` | what it means | what the board looks like |
|---|---|---|
| `"player"` | she is the thing that changes; her meters gate the world | 1–2 deep player tiers doing the heavy gating · the cast runs light, one bond meter each |
| `"cast"` | *they* are what change; you work on each person in turn | little or no player tier · **two meters per character**, one for access and one for willingness, gating that person's whole ladder |
| `"both"` | a player floor under per-character arcs | a player tier as the *floor* on the most explicit content, the per-character meter as the *spine* of each arc |

**Neither is better.** A ladder game is cheaper to author and gives every player the same climb; a
roster game costs more and gives a player somebody to be attached to — which is what
`SKILL.md`'s "the person is the product" is about. Pick on the premise, write it down, and let the
rest of this file follow from it.

**Gate 34 · the climb is where you said it is.** Declare-then-check: the measured split must match
the declaration (`player` ≥60% on her tiers · `cast` ≥60% on the cast · `both` ≥25% each). The cut
points sit inside the corpus's own empty band, so nothing here was invented — but what is judged is
the game against **its own declaration**, never against a number this file picked.

---

## W2 · A throttle's job, stated positively

> **An ODOMETER is permanent and gates progression. A THROTTLE resets and gates the REPEATABLE ACT
> SURFACE. Both must gate something.**

|  | odometer | throttle |
|---|---|---|
| example | an ascent tier · a character's willingness | arousal · a per-scene pleasure meter |
| behaviour | one-way; never resets | climbs in a scene, **reset to 0 at climax** — author-emitted, no engine macro does it |
| what it gates | rungs, one-time scenes, milestones | the **act menu** on a node-routed loop (`the-surfaces.md` R3b) and nothing else |
| what it must never gate | — | **a one-shot capstone.** A permanent first-time beat cannot hinge on a number that wipes |

> ### ⚠️ This skill shipped the negative half of this rule and not the positive half
>
> `templates/board.toml` labelled the volatile layer *"NEVER gate an arc on these."* Correct about
> the odometer — a throttle is not a spine — and **silent about what a throttle IS for.** Five
> authors read it as "never gate on it at all". Measured:
>
> ```
>                 arousal raises   arousal reads
> the_allowance         25              0
> seventh_day           53              0
> forty_miles           52              0
> steam                 55              2
> back_home             47              2
>                      232              4
> ```
>
> Plus `seventh_day`'s per-character `lust` at **34 raises / 0 reads**.
>
> In the field a sexual-state meter is a real gate in **13 of 27 games**, and where it exists it is
> the **#1 or #2 most-gated thing in the whole game** — `corpo-life` `lust` (346 content gates,
> the top meter in that game), DoL `arousal`, `family-ties` `you.arousal`, `friends-of-mine`
> `excitement`. It is the genre's hottest gate and our deadest number.

**The cause is structural, and it is the same one `the-surfaces.md` R3b fixed.** A throttle gates a
repeatable act surface. Until 2026-08-18 v2 taught no such surface — every explicit scene was a
one-shot cascade — so there was nothing for a throttle to gate and arousal had no job. **Build the
loop and the throttle has one; build no loop and do not declare the meter.**

---

## W3 · A number nothing reads is not a meter

> **Every trait you raise is read by something, or it is cut. A raise with no reader is not a
> mechanic the player has not found yet — it is a number that moves for nothing.**

The player cannot tell the difference between a meter that gates content later and a meter that
gates nothing ever. Both look like progress. That is what makes this defect ship green.

Measured across all nine of our games, on the day this rule was written:

```
the_allowance    arousal · hygiene
seventh_day      arousal · stress
forty_miles      arousal · count · energy · stress
steam            energy
back_home        hygiene · money
vesper (v1)      sex_stage · sex_entry_origin · money · core_sealed · mercer_drains_done
last_call (v1)   sex_stage · sex_reactions · hygiene · loop_player_pleasure · sex_entry_origin
late_shifts (v1) arousal · energy · hygiene · money
the_inheritance  — none
```

`forty_miles` raises `energy` 28 times and never reads it. `steam` raises it 50 times and never
reads it. `vesper` writes `sex_stage` **81 times** across 26 canvases and nothing anywhere checks it.

**Gate 33 · a meter is read.** Any player trait an `effects` entry raises must be read by a
condition, a `costs` entry, or a quest goal. Deterministic — either a reader exists or none does.

- **`costs` counts as a read.** The engine filters an unaffordable choice rather than letting it
  fail (`engine.md` §27), so a meter spent through `costs` is gating.
- **`<npc>_stage` is exempt** when the prefix names a declared character: the *engine* reads those
  (`v2.py:5549-5554`). `sex_stage` is not exempt — no character is called `sex`.

⚠️ **This gate can be satisfied cheaply and wrongly** — one throwaway `arousal >= 1` per dead meter
and it goes green. That is the deleted gate 22's failure mode in a new coat. The check can only ask
whether a reader exists; **W2 is what says the reader has to be the act menu**, and the meter-ladder
lint prints the rung count beside it so a one-rung fig leaf is visible.

**⚠️ THE CASE THIS GATE CANNOT SEE: the wardrobe.** `worn_beauty` and `worn_corruption` are
**derived** — the engine folds them out of each garment's own `beauty` / `corruption` declaration as
a MAX aggregate (`engine.md` §17). Nothing raises them with an `effects` entry, so gate 33 looks
straight past a full catalog and reports nothing wrong.

Measured across our 21 games on 2026-08-24: **102 garments in 10 games, 47 reads between them.**
`mothers_place` (6 garments), `seventh_day` (8), `steam` (8) and `the_allowance` (9) read theirs
**zero** times. The player can dress and the world does not look.

**Gate · the wardrobe is read.** A game declaring `[[clothing]]` must read it somewhere. Three
reader families count, and all three are legitimate: a **condition predicate** (`worn_corruption`,
`worn_beauty`, `worn_type`, `clothing_slot`, `clothing_item`), a **`player_portrait` outfit
override** (`when = { worn_type = … }`), or a **location dress code** (`clothing_rules`). The
portrait override is a *display* reader rather than a gate, and **W7 is what says that is the
field's normal case** — `vesper` reads its wardrobe 21 times and 21 of those are display, which is
the correct shape, not a shortfall. Same fig-leaf risk as above, answered the same way: the summary
prints garments against reads, so a thin pass is visible.

---

## W4 · The ladder — deep, and it starts low

> **A meter that carries a game has eight or more rungs, and the lowest one sits around 5.**

Field, live player ascent meters, content gates only:

```
family-ties  you.corr      978 gates  17 rungs   5,10,15,20,25,30,33,35,40,45,50,60…
friends      feminine      443 gates   8 rungs   5,10,15,25,30,40,50,75
corpo-life   lust          346 gates  11 rungs   10,21,24,31,41,50,61,70,80,90,99
become-som.  mc.dom         96 gates   9 rungs   5,7,10,15,20,25,30,50,75
the-company  player.horny   24 gates  11 rungs   2,20,30,40,49,50,60,70,80,90,99
DoL          exhibitionism  21 gates  11 rungs   15,19,25,35,40,50,55,60,75,80,95
```

**8–17 rungs, densest at the bottom, lowest rung at a median of 5.**

⚠️ **That number is about the meter that CARRIES the game, and it does not transfer to the cast.**
Every meter in the table above is a player ascent meter. A per-character willingness meter is a
different object and the field runs it much shorter — pooled over thirteen games, **median 3 rungs
per person (p25 2, p75 6)**, with the lowest rung at a median of 5, the same as the ascent number
(`findings_E_yes.md` §1). become-someone gives each of 62 people 5 rungs of `trust` while its player
meter `mc.dom` carries 9; both are correct, because they are not the same kind of ladder.

The lint below prints whichever comparator matches the branch it is on. Until 2026-08-24 it printed
8–17 on both, which told the repo's one roster game its five-rung cast meters were short of eight
when the field's per-character median is three.

Ours: 3–4 rungs, and **all 16 declared tiers across five games put their lowest rung at exactly
15.** Read that next to M1's measured failure — a rung is free and 12 clicks moved `cover` 4→16 —
and the opening of a v2 game is fifteen clicks in which nothing the player does changes anything.

> ### ⚠️ Where 15/35/55/75 came from, and why it spread
>
> It is the DoL **seed's** spacing, measured off its 2018 twee source and written into
> `the-board.md` as *"their rungs sit at 15/35/55/75… **copy that shape.**"* It then reached every
> tier of every game built afterwards.
>
> `SKILL.md`: *an example outranks every rule beside it.* This is the third recurrence and the
> first one **inside a template** — which is worse than a reference file, because a template is not
> read, it is filled in. **A shape that ships in `templates/` is copied harder than one that ships
> in `references/`.**

**Lint · the meter ladder.** Prints rungs and lowest rung per meter that carries the game. A
number, never a bar: a two-rung meter can be right on purpose, and rung counts are only comparable
on the same scale.

⚠️ **It follows W1's fork.** A ladder game is measured on the tiers `board.ascent_tiers` names; a
roster game (`who_climbs = "cast"`, which leaves that list empty by definition) is measured on its
per-character meters instead. The lint read only the first of those until 2026-08-23, so the one
roster game in the repo was the one game it printed nothing for — and it was running six meters
whose lowest rungs all sat at 12–22. **Half a fork is not an instrument.** A gate above the meter's
ceiling is skipped on both sides: that is a locked door (`the-release.md` G9), not a rung.

---

## W5 · A counterweight is rare, and it shuts doors

A meter that runs the other way — `standing`, `pride`, `grace`, `propriety`, `count`.

**One game in 25 has one that gates anything** (DoL `purity`, 84 gate sites). `reputation` in
`patriarch` and `apocalyptic-world` climbs +28 / −3 — that is an ascent wearing the other name.

Ours: **four of five shipped one, and three of those gate almost nothing** — `count` 0 reads,
`standing` 2, `grace` 5. `propriety` reads 25 times and every one is a `[group]` prose band, which
colours a paragraph and opens no door.

> A falling meter costs the player something on every rung that drops it. If nothing shuts when it
> is low, you have charged them for nothing and told them it mattered.

Do not take one because the template offered one. If you take one, it shuts a door — the same test
`needs` gets at M9, for the same reason.

⚠️ **This rule is about a meter that runs DOWN and closes things off.** A *"who knows about her"*
meter that rises is a different animal and fails this test on purpose — in the field it refuses the
player at 2% of its read sites. See **W5b**, and do not apply the shuts-a-door test to it.

**Lint · the counterweight.** Heuristic, which is why it is a lint: a player trait starting at 50+
whose effects mostly fall, declared needs excluded. It prints how many times the thing is read.

---

## W5b · The audience meter — it rises, and it almost never refuses

W5 is about a meter that runs **down** and shuts doors. A *"who knows about her"* meter runs the
other way, and measuring the field on 2026-08-23 showed it obeys none of W5's rules. It got its own
entry because `the_season` shipped one, asserted its own doctrine at
`0_systems_spec.toml:100` — *"known RISES AND WIDENS ... content, not punishment"* — and had no rule
to check it against.

### It is optional. Take it only if being found out is the fantasy

`family-ties` is rank 24, 204 passages, heavy sexual content, **267 distinct variables** and not one
of them tracks reputation. Its fantasy is the act; it spends its variables on the act (28 sex
positions). **There is no obligation to have this meter**, and a game that would rather spend the
same effort elsewhere is following the field, not defying it.

### If you take one, its job is that people already know — not that a door is closed

Every `<<if>>` in three field games whose condition names a reputation variable, classified by what
its branch actually contains (`findings_H_known.md` §1):

```
644 read sites          opens a link  17%     colours prose  81%     REFUSES  2%   (14 sites)
```

Fourteen. **A reputation meter is not a lock.** What it buys is a stranger who already knows:

```
$fame.prostitution gte 400   ->  "Hope you don't mind that I'm not paying for it."
$fame.rape gte 400           ->  "You like it rough, right? That's what I've heard."
$fame.exhibitionism gte 500  ->  "I think the town's pervs have missed you."
$fame.scrap gte 400          ->  "Very scary. But there's scarier behind us."
```

⚠️ **W5's test does not apply here.** W5 says a counterweight earns its place by shutting a door —
*"if nothing shuts when it is low, you have charged them for nothing."* That is correct for a
falling counterweight and wrong for this. **W5 owns the meter that closes; W5b owns the meter that
talks.** If you find yourself gating content behind a rising audience meter, you have built W5's
thing and should read W5's test instead.

### Its reads are one-line swaps, and that is why there are hundreds of them

```
degrees-of-lewdity   610 read sites   median branch  139 chars   (~25 words)
zaras-school-life     23 read sites   median branch   84 chars
the_season             7 read sites   median branch  570 chars
```

**The branch size is the cause and the count is the symptom.** `the_season` treats a `known` check
as a reason to write an alternate *block*, so it can only afford seven — none of them in a location,
none in a one-shot. The field treats it as a reason to swap one line of dialogue, so it can afford
six hundred.

A player states the failure from the other side, about a game whose corruption meter moved in
silence (`findings_J_players.md` §6):

> *"add some sort of questline, or **even just a few lines of dialogue**, for the family members when
> you reach certain corruption thresholds. Right now it just feels like **a switch was just turned on
> somewhere** and suddenly everyone's okay with it."*

> **A meter that rises without anyone in the world saying so reads as a switch being flipped.**

### Split it — one global number is the degenerate case

Degrees of Lewdity splits on two axes at once:

```
WHAT she is known for   $fame.<kind>, 14 kinds — model · exhibitionism · sex · scrap · prostitution
                        bestiality · social · rape · pimp · business · pregnancy · good · impreg · dance
WHERE it is known       $pubfame (the town) · $schoolrep (the school)
```

At minimum split by *what*. Better, and closer to the strongest architecture in the field, split by
*who*: Course of Temptation holds reputation **per person** (`pinfo.rumors[type]`), so one character
knowing is not the room knowing. Expressible here with per-NPC traits and flags (`engine.md` §8).

**Two mechanisms worth stealing if you split by person:**

- **Opposites cancel before they accumulate.** CoT pairs `promiscuity ↔ reservedness` and
  `kindness ↔ meanness`; raising one *drains* the other first. She cannot be known as modest and
  known as easy at once — a new reputation eats the old one.
- **Intimacy buys silence.** `juiciest_rumor` returns nothing for anyone in a friendship or romantic
  relationship. Who *won't* talk is as designed as who will.

### Positive bands are not decoration

`.good` and `.social` are tracked in the same structure as the lewd kinds and do real work: being
known as decent is what lets someone find her passed out in the cold and help
(`Widgets Temperature Passout`). `.scrap` — known as someone who fights — re-colours a threat scene.
**A reputation system that only counts what she is ashamed of is half a system.**

### Not a gate

Three games is not a field. There is no threshold here and `gates.py` is unchanged.
(`~/Documents/Female_PC_Craft_Study_20260823/findings_H_known.md`)

---

## W6 · The cast's meters — light or load-bearing, and W1 decides which

> **Which of the three this is.** W5 is the **counterweight** — one falling number that shuts doors.
> W5b is the **audience meter** — it rises, it is read constantly, and it almost never refuses.
> **W6 is the cast's own gating meters**, one set per character, and it is the only one of the three
> that is per-person. A rule from any of the three does not transfer to the other two.

### One word for the cast, and the difference lives in the modifiers

> **Pick ONE willingness word for the whole game. Put every person on it, on the same scale.
> Differentiate people by what modifies that number, never by giving them different vocabularies.**

Measured across the thirteen corpus games that run a per-person willingness meter on three or more
people (`findings_E_yes.md` §1):

```
median meters per person                    1
become-someone   trust     62 of 64 people      patriarch  like      37 of 38
destroyer        relation  45 of 57             friends-of-mine  relation  5 of 5
zaras-school-life  relationship 6 of 9          the-hellfire-club  love    3 of 3
threshold values used by two or more people   88%   (range 41-99)
rungs per person                    median 3  (p25 2, p75 6)
```

Only `college-daze` (median 3 meters each) and `free-cities` (2) run real stacks. **Nine of thirteen
games give every person exactly one meter, and it is the same word every time.**

**Three rungs is enough because this meter is not carrying the escalation.** Section F measured what
actually guards a sex act: of 7,598 act links across thirteen games, **47% carry no condition at
all** and **2% are gated on the per-person willingness meter**. Among the conditions that do exist,
the **player's own ascent meter gates 13% and hers gates 6%** — twice as much on the player's side.
Her meter says whether this person is available; **the player's says how far the game has come**, and
that is the one W4 measures at 8–17 rungs. Two meters, two jobs, two depths, and both correct at once
(`findings_F_further.md` §4).

> #### ⚠️ This section said the opposite until 2026-08-24
>
> It read: *"For a **roster** game it is the engine, and an identical pair on everyone is the engine
> missing. Pick each character's gating meter from what the relationship is."*
>
> The table below is kept — it is good at what it is actually for — but its job has changed. It
> picks **the game's one word**, not a different word per person. The old reading produced
> `off_season`: four characters, four vocabularies (`hold` · `ease+want` · `bond` · `trust+want`),
> nothing shared. And it made W6 contradict itself two paragraphs later, where it correctly says to
> reserve the rich model for the one or two arcs that carry the game. `vesper` is the shape that was
> always right — `relation` on eleven, the rich triple on four.
>
> It also made this file criticise `the_season` for the wrong thing: Wade and Prine **sharing**
> `{ease, want}` is the field's own practice. `the_season`'s real defect is the rule below that
> stands — **Rae carries no meter at all.**

The default the template shipped is `core_traits = { relation = 0, lust = 0 }` on every character.
Measured, all five v2 games: **one distinct meter shape across the whole cast, every time** — which,
read against the numbers above, is the right instinct arrived at by accident.

For a **ladder** game that is correct and deliberate — the tiers do the gating and a bond meter
colours the arc. Say so and move on.

For a **roster** game the cast meter *is* the engine, so choose the word deliberately rather than
inheriting `relation` from a template. Pick it from what the relationships in this game mostly
**are** — adapted from `author-game/references/trait-design.md`, which has the full version:

| the relationship | what gates the rungs |
|---|---|
| peer / dating | their **bond**, in small milestones — courtship is the climb |
| slow burn / escalation | their own **willingness** odometer, warmed by a throttle |
| leverage / transactional | money or debt — not affection |
| service / workplace | trust only; willingness does not apply |
| antagonist / witness | a hidden suspicion accumulator, never surfaced |
| **someone she already belongs to** | **no climbing meter at all** — presence plus one opened flag. He is not a conquest; the variation is in pose and framing, not in a rising bar |

⚠️ **Read the table as a menu of ONE choice, not a per-character assignment.** The last row is the
exception that still holds per person: someone she already belongs to gets no climbing meter, and
that is a decision about *that* character. Everyone who does climb, climbs on the same word.

Two more rules that survive from v1 and are worth restating:

- **Reserve the rich two-meter model for the one or two arcs that carry the game.** The reference
  game gives it to three housemates and runs its other fourteen characters light. Gold-plating
  every character dilutes the core and triples the authoring.
- **A character who gates nothing is not in the game yet.** `the_allowance` ships two of five
  characters with a full meter pair and **zero** gate sites on either.

### The meter is a trade, not a bonus

Added 2026-08-24 from Section G. Above, W6 says an identical meter pair across the cast is *the
engine missing*. This is the half that was missing from W6 itself: **picking a different meter is
not enough if every meter only ever opens things.**

`inseminator` ships its own design spec as a player-facing help page. Six relationship traits, each
a one-line character summary plus three to five numeric modifiers — and **five of the six make one
route cheaper and another route more expensive**:

| trait | who she is | what it buys | what it costs |
|---|---|---|---|
| **Romantic** | "Believes in true love" | +10% girlfriend, roses +4 affinity | **−15% polyamory** |
| **Clingy** | "Needs constant attention" | +20% girlfriend, +2/mo if dated | **−30% polyamory, −3/mo if ignored** |
| **Independent** | "Values her freedom" | +20% polyamory | **−10% girlfriend, −15% estate, decay doubled** |
| **Jealous** | "Possessive and suspicious" | +5/mo if dated | **+20% jealousy event, +10% breakup** |
| **Precious** | "Innocent and harder to seduce" | +20 Matron | **−5/−10/−15% flirt/kiss/sex** |
| Loyal | "Devoted and faithful" | never breaks up | — |

> **A meter that only opens things is a stat wearing a personality's name.**

**And this is where the differentiation goes.** `inseminator`'s six traits are not six meters — they
are **coefficients on one affinity number**, which is exactly the mechanism the measurement above
describes. `become-someone` does the same thing in code: the shared nudge carries a gift that belongs
to one person —

```
<<katetrust>> = <<CharismaBoost>>
                + (a locket in KATE's inventory)
                + ''Kate trusts you more''
```

— a locket for Kate, lingerie for Jade, on the same `trust` number all 62 of them share. One word,
sixty-two people, and nobody feels the same to play.

Two mechanics from the same page worth having:

- **A trait can be spent.** `Precious` carries a loss condition — *"Lost when: Affinity drops below
  20 OR has 3+ children."* The personality is consumed by the thing it was gating.
- **A trait can be inherited** — each carries a 30–60% chance of passing to children. Not something
  we need, but it is the proof the author treated these as properties of a *person*, not of a slot.

And the cheapest illustration in the corpus, from `degrees-of-lewdity`'s creature generation — the
same tag moves a number **and** writes a line:

```
<<if traits.includes("territorial")>>
    <<set healthmax += 125>> <<set skills.security += 100>>
    ...
    "This is my territory. You'll pay for this trespass."
```

**A tag that only moves the stat is invisible. A tag that only writes the line is decoration.**

**Ours:** `the_season` fails both halves. Wade and Prine run the **identical** pair —
`{ ease = 0, want = 0 }` on each — so two of the four men are mechanically the same person. Boyd
runs `{ owed = 0 }`, Emmett `{ seen = 0 }`, and Rae runs nothing at all. None of the four is a
trade; every one of them only rises and only opens.

**Lint · the cast's meters.** Per character: which meters they own and how many gate sites each
carries, plus how many distinct shapes exist across the cast.

---

## W7 · The body's meters are read to colour, not to refuse

> **A body value — clothes, arousal, hygiene, pregnancy — earns its place by changing the words in
> a lot of places, not by closing doors in a few. Build it to be READ CHEAPLY AND OFTEN. If you
> find yourself writing gates on it, you are building the wrong kind of meter.**

Added 2026-08-24 from section I, which read all 27 parseable games in the mopoga corpus. W5 is the
counterweight that shuts doors, W5b the audience meter that almost never refuses, W6 the cast's own
gating meters. **The body is a fourth shape and it behaves like none of them.**

Twenty-five (subsystem × game) pairs clear 20 read sites. Their gate share — the fraction of reads
whose consequent contains a link, a `goto` or a button, rather than prose:

| | median gate share | n |
|---|---|---|
| clothes | **8%** | 8 |
| arousal | **14%** | 7 |
| pregnancy | **7%** | 8 |
| hygiene | 31% | 2 |
| **all** | **10%** | **25** |

**Seventeen of the twenty-five gate under 25%.** The colour share runs 87, 88, 89, 90, 97, 97, 98,
98, 100 per cent.

Section H measured reputation at **2% gating, 98% colouring** and called it an audience meter.
Section G measured differentiation and found it is many small swaps rather than a few large
branches. This is the same law arriving a third time, from a third instrument.

**The exceptions are real and they are all small.** `new-life-project` gates 91% of its arousal
reads — of **43**. `wasteland-lewdness` gates 63% of its clothing reads — of **35**. `patriarch`
gates 47% of its pregnancy reads — of **34**.

> **A body system either stays small and gates, or grows large and colours. Nothing in the corpus
> is both big and gating.**

### The band ladder — write it once

The mechanic underneath every one of these is the same: a number, a ladder of bands, and a short
string per band. What separates a good implementation from a bad one is **where the ladder lives.**

`degrees-of-lewdity` writes it once, in a widget, seven rungs wide:

```
<<if $hygiene gte 2000>>   You are filthy.
<<elseif $hygiene gte 1600>>You are soiled.
<<elseif $hygiene gte 1200>>You are smelly.
<<elseif $hygiene gte 800>> You are messy.
<<elseif $hygiene gte 400>> You are neat.
<<elseif $hygiene gte 1>>   You are clean.
<<elseif $hygiene lte 0>>   You are speckless.
```

`corpo-life` writes the identical structure **inline, across 5,785 sites** — clamp, then band, then
set a descriptor string, copy-pasted through the game instead of factored into one place.

Note what the bands say. Not `45/100`. **"Soft boner."** The number is internal; what the player
meets is a body state in words. Our surface for this is `trait_status_text` (`engine.md` §30) — one
authored ladder, rendered wherever the trait sits.

### What the player is shown

The field does not show you the number. **It shows you the world reacting to it.**
`degrees-of-lewdity`'s real body system is `$exposed`, a three-state value the author writes exactly
once — `<<set $exposed to 0>>` at game start — and the engine derives from the worn set thereafter.
The world then reads it about **900 times**: 415 sites test `gte 1`, 151 test `gte 2`, 90 test
`lte 0`. Eighty-two per cent of those reads only change words. The portrait reads it too, setting
the model's mouth to a frown at `exposed === 2`.

**That is the shape to copy: one derived number, cheap enough to test that the whole world tests
it.** Our equivalents are `worn_corruption` and `worn_beauty`, and W3's gate is what makes sure
somebody reads them.

---

# The ascent's price

## The measured rules

### M1 · A meter that gates content must cost something to raise

If a rung grants an ascent tier, and that rung has no `costs`, no daily cap, and no meaningful time
price, then the gate it feeds is decoration. The player does not experience a climb — they
experience a button they have to press N times, and the only variable is patience.

This is not a prose problem and it is not fixed by writing a better rung. **A free rung repeated
fifty times is worse than a free rung repeated once**, because the fiction is identical and the
fifty repetitions are what the player remembers.

**Gate 26** walks every trait that any `conditions` block reads — player traits *and* per-NPC
relation — finds the rungs that grant it, and fails when the fastest route to a gated threshold is
free.

### M2 · Progress accrues over DAYS, not in one sitting

The pacing target is a campaign, not an afternoon. `author-game/references/rts-design-philosophy.md`
P8, measured off the reference game: raises are small and uniform, each scene is capped once per
day, and deeper content is gated by **higher thresholds — that is, more days — not by bigger
per-act jumps.**

The tell that this has gone wrong is not the threshold; it is the **rate**. `cover 55` is a
perfectly good top band. `cover 55` reachable in nine hours of one Monday is the defect. When
judging a tier, always compute the same two numbers:

```
clicks to the top band  ·  in-game minutes to the top band
```

A first release should be measured in in-game **days** on its fastest route. v1's fully-throttled
reference climb was live-verified at **7–10 in-game days**.

### M3 · The throttle menu — four levers, and none of them works alone

| lever | what it does | where it fails |
|---|---|---|
| **1 · Threshold spacing** *(always on)* | widen the gap between rungs while keeping the per-beat increment fixed, so the climb takes days | does nothing on its own — 55 free clicks is still 55 free clicks. And **don't over-space a thin repeated beat**: if the rung is one recycled paragraph, a huge bar is just tedium |
| **2 · A window-sized time cost** | `time_progression_minutes` on the rung's exit. The best-*reading* throttle: it is fiction, not a mechanic, and no single deleted line removes it | **only bites when sized against the window.** A 10-minute rung against an all-day hub is farmable ~144× per day. A 180-minute rung against a 09:00–18:00 NPC window is ~3/day. Advancing past an NPC's schedule window makes them absent, which is what actually stops the rung |
| **3 · A counted daily cap** | `max_triggers_per_day` on a *triggered* canvas, or a `_today` flag cleared in `[engine.daily_tick]` (§28) | **`max_triggers_per_day` is read off the trigger (`v2.py:11017`) — a triggerless rung has none.** And a single removable flag is brittle as the *only* brake: v1 records a whole seduction climb collapsing on first play the moment its one daily-cap flag was deleted |
| **4 · A resource cost per rung** | `costs` (§27). Gate-enforced — the engine does not offer a rung the player cannot afford | energy is the wrong *primary* lock for a relationship ("too tired to seduce him" is bad fiction). It is a legitimate *throttle* when the fiction supports it, and it is the strongest tool available to a triggerless rung |

### M4 · The recipe — layer all three

> **Spacing (always) + at least one hard throttle + the rung PAYS, visibly.**

- **Spacing** is free and always on, but never counts as the brake.
- **A hard throttle** is lever 2 sized to a real window, or lever 3, or lever 4. Prefer **two**.
- **The rung pays** — brake-only is grind. If a rung costs energy and time and gives back nothing
  the player wanted, you have built a chore. The payoff is content, not a number: a new line, a
  clip they have not seen, a door that opens.

v1's reference climb stacked all four levers and measured out at a 7–10 in-game-day campaign. That
is the shape to aim at.

### M5 · How to throttle a TRIGGERLESS rung — the gap that caused the failure

Nearly every rung in a v2 game is **triggerless**: a canvas with no `[canvases.trigger]` block,
reached by a hub choice. That single structural fact voids the first tool everyone reaches for.

```
max_triggers_per_day  →  read off the trigger (v2.py:11017)  →  DOES NOT APPLY
```

The two that do:

**A · Price it.** `costs` on the hub choice (§27). The engine filters out an unaffordable choice
rather than letting it fail, so the brake is enforced without a condition:

```toml
[[canvases.nodes.exit_block.choices]]
text  = "Take the copper."
costs = [ { trait = "energy", value = 12 } ]
```

**B · Day-cap it with a FLAG, not a counter trait.** Three parts, and the flag is set **on the
choice** — the same choice that gates on it, not the rung's exit:

```toml
# on the hub choice that reaches the rung — the SET and the GATE ride together
[[canvases.nodes.exit_block.choices]]
text        = "Sell the eggs."
targetType  = "node"
nodeId      = "rung_eggs.base"
costs       = [ { trait = "energy", value = 8 } ]
flagEffects = [ { targetType = "player", flag = "eggs_sold_today", op = "set" } ]
conditions  = { version = "1.0", logic = "AND", items = [
  { type = "flag", subject = "player", flag_key = "eggs_sold_today", operator = "is_false" },
] }

# once, in 0_systems_spec
[engine.daily_tick]
flagEffects = [ { targetType = "player", flag = "eggs_sold_today", op = "unset" } ]
```

> ⚠️ **On the CHOICE, never on the rung's exit — and this example taught the wrong one until
> 2026-08-22.** The generator emits the two in opposite orders:
>
> ```
> choice     flagEffects -> costs -> … -> advanceTime      v2.py:12648-12733
> node exit  advanceTime -> traitEffects -> flagEffects    v2.py:13085-13088 · :13049-13050
> ```
>
> `advanceTime` rolls the day inside itself (`v2.py:5411-5414`) and that is where the tick clears
> every `_today` flag (`v2.py:5552`). So an **exit**-set cap on a rung that crosses midnight is
> written *after* the clear, and the new day starts already capped.
>
> Measured, in the game this example authored: `act_flat_sleep` ran 21:00→06:00, so from the second
> night onward Sleep was never offered before midnight again — the player was pushed into a
> permanent post-midnight bedtime and nothing in the build, the validator or the scoreboard said a
> word. Four more rungs sat in the same trap on late hub windows.
>
> Across the repo, **78 day caps already sit on the choice and 40 on an exit** — and the two games
> holding 35 of those 40 are `off_season` and `the_allowance`, the two written under this example.
> Third recurrence of `SKILL.md`'s "an example outranks every rule beside it".
>
> ⚠️ **A LOCATED canvas does not need a flag at all.** `max_triggers_per_day` is read off the
> trigger (`v2.py:11017`) and `markCanvasTriggered` stamps the day key *before* `advanceTime`
> (`v2.py:4290`), so it is immune to this. Reach for the flag only when the rung is triggerless.

⚠️ **Do not do this with a hidden counter trait and an `lt` condition.** It works, and it is what
the failing game reached for in the absence of this section — but it puts a player-subject trait in
the game whose only conditions are `lt`, which reads to **gate 10** as a meter that closes more than
it opens. The author then correctly filed a bug against gate 10. The gate was not the problem; the
missing paragraph was. **Flags are not meters. Use a flag.**

⚠️ A game with no `[engine]` section at all has no day-rollover hook, so any `_today` state has to
be cleared by an authored sleep rung — which does nothing if the player crosses midnight without
sleeping. Declare the tick.

### M6 · `cap` is a value ceiling, not a rate limit

`cap` is real (§29) and the skill never mentioned it before this file, so it is easy to over-learn.
It bounds **how high a trait can go**, not **how fast**:

- ✅ bounding a restore — a sleep rung adding energy, a wash adding hygiene
- ✅ bounding a repeatable relation grant so one rung cannot max a character on its own
- ❌ **never on an ascent tier** — the tier must reach its top band, and a cap there deletes content
- ❌ it is not a throttle. A capped rung is still infinitely clickable up to the cap.

### M7 · Band a meter, hide its number

The sidebar prints a trait twice — once from the auto Traits dump, once from whatever
`[[sidebar_items]]` you wrote — and the two do not know about each other (§30).

**Every trait carrying `bands` in `[[sidebar_items]]` needs `hidden = true` in `[[traits.labels]]`.**
A trait absent from `[[traits.labels]]` entirely is *not* hidden; it prints.

Choose the primitive by what the number **means**:

| kind | example | sidebar type | why |
|---|---|---|---|
| identity / qualitative state | an ascent tier, corruption | `trait_words` + `bands` | the player thinks in a word, not a number |
| transient mood | arousal | `trait_bar` + `bands` + `hide_value = true` | show the band, hide the volatile figure |
| body-need | energy, hygiene | `trait_status_text` + `bands` | passive banded body-state |
| countable resource | money | `trait_bar`, `hide_value = false`, **no `bands`** | you want the exact figure; don't band a thing the player counts |

**Gate 27** fails any banded item whose key is not hidden. It is deterministic — no threshold to
invent, no false positives.

⚠️ And the other half: a banded value that lands **outside every band renders nothing at all** — the
card vanishes, which reads as a missing HUD element rather than a wrong number. Leave the top band's
`max` off (`trait_status_text` treats it as open) or `cap` the terminal add. See §30.

---

# The body's meters — needs

M1–M7 govern the **ascent**: a meter that climbs and buys access. A need is the other kind of meter
and it runs the opposite way — it **falls on its own**, she refills it, and while it is empty
something is shut.

> **Measured failure this exists to prevent.** `the_allowance` is a game whose anchor location is a
> kitchen and whose title is about money at a table. Grep it:
>
> ```
> eat · cook · meal · breakfast · dinner · food · fridge · sleep   →   ZERO canvases
> nine declared traits, none of them hunger
> [player.trait_decay] hygiene = 10          she gets dirty every day
> four ways to wash                          she can always get clean
> conditions anywhere reading `hygiene`:  0  nothing has ever cared
> ```
>
> The loop is fully wired and means nothing. LO named it before it was measured: *"we can add
> meaning technically like gaining or losing energy but logically things mean very less."*
>
> Contrast `games/vesper`, built on the incumbent skill, which got this right: **11 things drop
> hygiene by 30** (sex acts, the burned yard, the depot), **one restores it**, and `hygiene >= 40`
> gates *"Take the car."* Filthy means **she cannot leave**. That is the shape the field uses.

**Needs are declared per game, never a fixed list.** Vesper's body is `Power down` / `Charge up`; a
truck stop's is not a household's. What is fixed is the *form*.

### M8 · A need declares four things

```jsonc
"needs": [
  { "key":   "<trait>",            // the meter
    "falls": "<how fast, per day>",  // [player.trait_decay], §11
    "fills": "<location> · <the activity> · <minutes>",
    "costs": "<money / an item / nothing>",
    "shuts": "<what she cannot do while it is empty>" }   // ← the load-bearing one
]
```

The field, on the fourth field:

| game | need | what it shuts |
|---|---|---|
| Apocalyptic World | hunger | `Eat` needs food **in the pack** — no food, no meal |
| Become Someone | hunger | breakfast / dinner / dishes are **once each per day**, in their own windows |
| Degrees of Lewdity | ingredients | a recipe you lack the stock for **cannot be cooked** |
| vesper | hygiene | under 40, **`Take the car` is gone** |

### M9 · A need that shuts nothing is a chore

**Gate 29.** Every key in `board.needs[]` must be read by at least one condition somewhere in the
game. Deterministic, no threshold to invent: either something gates on it or nothing does.

A restore with no gate behind it is a button that maintains a number. It costs the player time and
buys them nothing, and it is the exact defect that shipped in `the_allowance` with a green
scoreboard.

**This is also what makes a room worth entering.** `the-surfaces.md` R2 says a room's list is needs,
work and people — a *need* on that list has to be a real one, or R2 degrades into the object rule
with different nouns.

### M10 · The clock is `[player.trait_decay]`

```toml
# Decay is a POSITIVE MAGNITUDE — the validator rejects a negative (engine.md §11).
[player.trait_decay]
hygiene = 10
energy  = 8
```

Shipped and working in `late_shifts` and `vesper`. It is the cheapest half of a need — the half most
games do write. **The half they drop is `shuts`.**

Two shapes, and pick on purpose:

- **decay** — falls every day whether or not she does anything. Right for hygiene, energy, hunger.
- **spent** — falls only when something takes it, via `costs` on a trigger (§27). Right for a
  resource, and the one `the_allowance` uses correctly for energy (11 priced canvases).

A need can use both. What it cannot do is neither, which is a trait that only ever goes up.

---

## The field, measured 2026-08-16

Every v2 game plus the v1 reference game, parsed from merged TOML:

| | vesper (v1) | back_home | steam | forty_miles | seventh_day |
|---|---|---|---|---|---|
| priced choices (`costs`) | **32** | 0 | 0 | 10 | 7 |
| `max_triggers_per_day` | **11** | 17 | 0 | 9 | **0** |
| `trigger_mode = "random"` | **14** | 0 | 0 | 8 | **0** |
| conditional (`group`) blocks | **138** | 102 | 91 | 0 | **0** |
| choices open on turn one | 64% | 26% | 50% | 45% | **78%** |
| nodes per canvas | **1.9** | 1.0 | 1.0 | 1.0 | 1.0 |

Read the last row before the others. The v1 game averages nearly two nodes per canvas; every v2 game
averages one. A one-node canvas is a single screen with a single exit — which is a fine shape for a
rung, and a warning when it is the shape of the *entire game*.

And read `seventh_day`'s column as a whole: **zero of every throttle the engine offers.** It is not
that its author chose badly between them. Nothing in this skill told them the choice existed.
