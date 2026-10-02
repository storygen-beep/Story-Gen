# The Meters — which ones exist, what the climb costs, and what the player reads off it

The ascent tiers are this skill's whole thesis: **a meter that buys access.** Every other file here
is about *what* the meter unlocks. This one is about the meters themselves.

**Meters live inside systems.** A meter is what a system writes and reads (`the-systems.md` SY1): the
job writes her wage and her nerve, the gym her body, the bill her debt. That file owns the activity and
its card; this one owns which meters exist, who owns them, and what the climb costs.

**Three parts, and they are read in order.**

**W1–W6 — which meters exist and who owns them.** The decision that comes before every other one on
this page: does the PLAYER climb or does the CAST, what a throttle is actually for, how deep a
ladder goes, and whether a number anything reads. Missing entirely until 2026-08-19. **W5b** (2026-08-24) covers the
one meter that breaks W5's rules on purpose — a *"who knows about her"* meter, which rises and
almost never refuses.

**M1–M7 — the ascent, and what it costs to raise.** Missing until 2026-08-16, and the difference
between an ascent and a button.

**M8–M10 — the body.** A need falls on its own, she refills it, and while it is empty something is
shut. Missing until 2026-08-18.

> **Gate `the climb is paid for`** (gates.py:8567) walks every trait any condition reads, not just
> the declared tiers. It fails when any route into a rung that raises a gated meter carries no
> `costs`, no `max_triggers_per_day` on the target's trigger, and no day-cap flag cleared in
> `[engine.daily_tick]`. One free route is enough to fail. It prints clicks and in-game time to the
> top gate either way.

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

v1 asks the question (`author-game/references/content-framework.md`, *"Who climbs?"*); v2
dropped it.

| `who_climbs` | what it means | what the board looks like |
|---|---|---|
| `"player"` | she is the thing that changes; her meters gate the world | 1–2 deep player tiers doing the heavy gating · the cast runs light, one bond meter each |
| `"cast"` | *they* are what change; you work on each person in turn | little or no player tier · **two meters per character**, one for access and one for willingness, gating that person's whole ladder |
| `"both"` | a player floor under per-character arcs | a player tier as the *floor* on the most explicit content, the per-character meter as the *spine* of each arc |

A system's own pay and lewd ladders are not this fork; they follow `the-systems.md` SY8.

**Neither is better.** A ladder game is cheaper to author and gives every player the same climb; a
roster game costs more and gives a player somebody to be attached to — which is what
`SKILL.md`'s "the person is the product" is about. Pick on the premise, write it down, and let the
rest of this file follow from it.

**Gate 34 · the climb is where you said it is.** Declare-then-check: the measured split must match
the declaration (`player` ≥60% on her tiers · `cast` ≥60% on the cast · `both` ≥25% each). The cut
points sit inside the corpus's own empty band, so nothing here was invented — but what is judged is
the game against **its own declaration**, never against a number this file picked.

### What each man keeps score of

Declared per man at the Want (`want.cast[].keeps`), from the fantasy and `who_climbs`. The shape is
**(LO decided, D5)**; the evidence is R5
(`~/Documents/Skill_Test_Research_20260929/R5_HIS_FEELINGS.md`).

| the game is about… | the men keep | like |
|---|---|---|
| her change | a step counter + memory flags | Cupid's Way, In Her Own Hands |
| relationships | Want + Warmth; the split picks lover vs user (**thin**: 1 of 4 games does it fully, R5 Part 1b) | Course of Temptation's dating |
| power | Want + Power; Power changes which acts happen | Shady Deals |
| a system, not him | `none — ` and why: he does not climb; he belongs to a system card's `people[]` | a landlord who is the bill's deadline |

It can differ per man: a pressure man gets Power, a nice man doesn't. The author declares it; LO
approves. **Whatever he keeps:**

1. A shown number opens something visible, and he reacts the visit it crosses (gate `the men's numbers are read`).
2. No hidden setting overrides the numbers.
3. A locked step shows how close he is: the locked button names his feeling and the need.
4. One visit moves about 1–10% of the next threshold, with 3–10 visits between steps (R5:243-244).

---

## W1b · The meter gates how far she goes — and the inner conflict stays

**Don't invent an excuse for every act. Design what stops her. And keep the conflict: at low levels
her own thought pushes back while she acts; at high levels the same moment is appetite. The slope is
what the player plays** — not a switch that flips at a threshold.

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `shady-deals` writes one moment at three levels of her meter
> (`[Sex Pose Widgets]`): *"You stiffen immediately, heat rushing to your face…"* ·
> *"…embarrassment mixing with a reluctant thrill."* · *"…fully aware of how exposed you are and
> enjoying the attention."* `in-her-own-hands`, walked in on while changing: inhibited, *"Shit! I
> must have forgotten to lock the door!"*; past it, *"Well, fuck it, I might as well go with it."*
>
> Players praise the slope — *"This isn't a story of some girl that becomes a mega slut overnight"*
> (`in-her-own-hands`) — and punish the flip: *"goes from teasing to full on sex after that
> corruption event"* (`cupids-way`). And the direct want is the default, not the excuse: one game
> (`zaras-school-life`, numbers only) has 36 act scenes where she simply wants him against 5 where
> she gives herself a reason.

How to write one event at several levels: `register.md`, "One event, several levels". A paid
repeatable carries the slope as two voices per act (`the-arc.md` A15, thin).

### W1b-i · The unit is +1, and the raise goes through a named widget

One game (`zaras-school-life`, numbers only) raises a character's meter 107 times and every raise is
`+1`, through one named widget per character, called from the ordinary loop — chores, the same room,
time in his space — and each call checks three things: what she is wearing, that he is there, and a
die. One number, one widget, +1s, three checks. `+1` is also the median raise in five of eleven
field games.

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
> the odometer — a throttle is not a spine — and **silent about what a throttle IS for.**
>
> In the field a sexual-state meter is a real gate in **13 of 27 games**, and where it exists it is
> the **#1 or #2 most-gated thing in the whole game** — `corpo-life` `lust` (346 content gates,
> the top meter in that game), DoL `arousal`, `family-ties` `you.arousal`, `friends-of-mine`
> `excitement`. It is the genre's hottest gate.

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

**Gate 33 · a meter is read.** Any player trait an `effects` entry raises must be read by a
condition, a `costs` entry, or a quest goal. Deterministic — either a reader exists or none does.

- **`costs` counts as a read.** The engine filters an unaffordable choice rather than letting it
  fail (`engine.md` §27), so a meter spent through `costs` is gating.
- **`<npc>_stage` is exempt** when the prefix names a declared character: the *engine* reads those
  (`v2.py:6244-6249`). `sex_stage` is not exempt — no character is called `sex`.

⚠️ **This gate can be satisfied cheaply and wrongly** — one throwaway `arousal >= 1` per dead meter
and it goes green. That is the deleted gate 22's failure mode in a new coat. The check can only ask
whether a reader exists; **W2 is what says the reader has to be the act menu**, and the meter-ladder
lint prints the rung count beside it so a one-rung fig leaf is visible.

**⚠️ THE CASE THIS GATE CANNOT SEE: the wardrobe.** `worn_beauty` and `worn_corruption` are
**derived** — the engine folds them out of each garment's own `beauty` / `corruption` declaration as
a MAX aggregate (`engine.md` §17). Nothing raises them with an `effects` entry, so gate 33 looks
straight past a full catalog and reports nothing wrong. The player can dress and the world does
not look.

**Gate · the wardrobe is read.** A game declaring `[[clothing]]` must read it somewhere. Three
reader families count, and all three are legitimate: a **condition predicate** (`worn_corruption`,
`worn_beauty`, `worn_type`, `worn_exposure`, `clothing_slot`, `clothing_item`), a
**`player_portrait` outfit override** (`when = { worn_type = … }`), or a **location dress code**
(`clothing_rules`). The
portrait override is a *display* reader rather than a gate, and **W7 is what says that is the
field's normal case**. Same fig-leaf risk as above, answered the same way: the summary
prints garments against reads, so a thin pass is visible. **That gate is the floor; the rule is ≥3
readers for every declared state and key item** (W7; gate `every clothing state is read three
times`).

**⚠️ AND A READ ONLY COUNTS IF SOMETHING SHE CAN GET SATISFIES IT.** The gate above asks whether
the wardrobe is read. It cannot ask whether the read can ever be **true**. A clothing condition that
only an unobtainable garment satisfies seals every canvas behind it, and the scoreboard stays green
while it does.

**Gate · a declared garment can be got.** A `[[clothing]]` entry with `initial = false` needs one of
the only two routes the engine has: a shop purchase — `[settings] shop_location` naming a **declared
location** plus `price > 0`, because `renderShopPage` stocks only `!initial && price > 0` — or a
`wardrobeEffects = [{ item_id = "…", action = "add" }]` on a choice or an `exit_block.config`.
Zero-based; no threshold to invent. **A shop existing does not make a garment buyable:** a
non-initial garment at `price = 0` is invisible on the very shop page it sits beside
(`v2.py:2333` stocks only `!initial && price > 0`), so a check reading "a shop exists, therefore
buyable" would pass a garment nobody can get.

⚠️ **`shop_location` is never validated** (`template_import.py:2824` takes it as a bare string,
`v2.py:10717` compares it to each location's slug). A typo produces no error, no warning and no shop
— the same silence as omitting it. After a build, `grep -c "Browse Clothes" <output>/index.html`
must be 1.

⚠️ **The stronger check — "is this clothing condition satisfiable at all" — was measured and
declined.** It needs the derived `worn_beauty` / `worn_corruption` MAX aggregate modelled, and a
check that cannot see the shape of the thing it judges manufactures whatever it can see (the deleted
gate 22, `the-surfaces.md`). An unsatisfiable clothing read is caused by an ungrantable garment,
so the obtainability check reaches the same defect from the side that can be answered.

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

**8–17 rungs, densest at the bottom, lowest rung at a median of 5.** A system's lewd ladder is a
shorter object: ≥4 lewd rungs, ≥2 acts per rung (`the-systems.md` SY8).

⚠️ **That number is about the meter that CARRIES the game, and it does not transfer to the cast.**
Every meter in the table above is a player ascent meter. A per-character willingness meter is a
different object and the field runs it much shorter — pooled over thirteen games, **median 3 rungs
per person (p25 2, p75 6)**, with the lowest rung at a median of 5, the same as the ascent number
(`findings_E_yes.md` §1). become-someone gives each of 62 people 5 rungs of `trust` while its player
meter `mc.dom` carries 9; both are correct, because they are not the same kind of ladder.

`15/35/55/75` is the DoL seed's spacing, measured off its 2018 twee source (numbers only).

**Lint · the meter ladder.** Prints rungs and lowest rung per meter that carries the game. A
number, never a bar: a two-rung meter can be right on purpose, and rung counts are only comparable
on the same scale.

⚠️ **It follows W1's fork.** A ladder game is measured on the tiers `board.ascent_tiers` names; a
roster game (`who_climbs = "cast"`, which leaves that list empty by definition) is measured on its
per-character meters instead. A lint that read only the first of those would print nothing
for a roster game (`gates.py:3400` takes the `who_climbs == "cast"` branch). **Half a fork is not
an instrument.** A gate above the meter's
ceiling is skipped on both sides: that is a locked door (`the-release.md` G9), not a rung.

---

## W5 · A counterweight is rare, and it shuts doors

A meter that runs the other way — `standing`, `pride`, `grace`, `propriety`, `count`.

**One game in 25 has one that gates anything** (DoL `purity`, 84 gate sites). `reputation` in
`patriarch` and `apocalyptic-world` climbs +28 / −3 — that is an ascent wearing the other name.

> A falling meter costs the player something on every rung that drops it. If nothing shuts when it
> is low, you have charged them for nothing and told them it mattered.

Do not take one because the template offered one. If you take one, it shuts a door — the same test
`needs` gets at M9, for the same reason.

⚠️ **This rule is about a meter that runs DOWN and closes things off.** A *"who knows about her"*
meter that rises is a different animal and fails this test on purpose — in the field it rarely
refuses the player anything (~10% of its branch arms carry a link, re-measured 2026-08-27 over 13
games; the 2%-of-644 figure this line used to quote was a three-game sample). See **W5b**, and do
not apply the shuts-a-door test to it — but do read W5b's three mechanisms, because rarely-refuses
does **not** mean never-mechanical.

**Lint · the counterweight.** Heuristic, which is why it is a lint: a player trait starting at 50+
whose effects mostly fall, declared needs excluded. It prints how many times the thing is read.

---

## W5b · The audience meter — it rises, it rarely refuses, and it still decides things

W5 is about a meter that runs **down** and shuts doors. A *"who knows about her"* meter runs the
other way and obeys none of W5's rules.

### For a female lead, being known is core — declare who notices, even without a meter

Twelve of twenty-five male-heavy corpus games carry no reputation meter. For a female lead, being
known is the fantasy and its absence is the complaint: **declare who notices what she does, even
with no meter at all.**

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `course-of-temptation` keeps what each person saw; a witness tells others only in scenes she is
> in, one hop, and a rumour someone only heard is never retold; a man who assumed reads them back — *"Maybe the rumors are wrong."*
> `shady-deals` lets reputation change who dares: at 4,000 the man who caught her backs off —
> *"Sorry, I didn't mean to bother you. I'm not going to stand in your way..."* — and her crew talks
> about what she is known for. `cupids-way` marks her publicly and for good, and her boyfriend uses
> the name: *"Hi, how's my BBC queen doing?"*
>
> Where nobody notices, players say so: *"They don't notice - dont take a hint - NADA"*
> (`in-her-own-hands`), *"it doesn't affect anyone"* (`cupids-way`).

`family-ties` (numbers only) is the field's clearest **place-scoped** meter: six kinds of fame, read
257 times.

### If you take one, its job is that people already know — not that a door is closed

Every `<<if>>` naming a reputation variable, classified by what its branch contains: of 644 sites in
three games (610 of them the reference game's, numbers only), **17% open a link, 81% colour prose
and 2% refuse**; across thirteen games, ~10% carry a link and a median 41% change something
mechanical.

Fourteen, in that sample. **A reputation meter is not a lock.** What it buys is a stranger who
already knows — `shady-deals`' crew: *"Word is, you don't even need to speak - just, you know, and
things get 'handled'."*

### Rarely a lock is not the same as never mechanical

Across thirteen games it does four things, and **none of them refuses the player anything**:

| game | what the meter does | shape |
|---|---|---|
| `patriarch` (numbers only) | `$Reputation gt 5 / 9 / 14` → a new person arrives at each band | **it delivers people** |
| `destroyer` | `_roll1 to _roll + $Respect` in every pickup and every fight; `Math.clamp(5, 95, ($Muscularity * 0.8) + ($Respect * 1.6))` | **it modifies a roll** |
| `corpo-life` | an 8-rung `$prestige_level` derived in `StoryCaption`, then read at **308 sites**, many of them `(Relationship +1 from prestige)` | **it scales a rate** |
| `patriarch` | weekly income by band: `lt 300 → +2000`, `lt 400 → +3000`, … | **it prices the world** |

A door that opens on its own is not a door the player found locked. **Prefer these to a gate**: they
give the meter consequence without ever printing a refusal, which is what the 2% was really saying.

**Where the reads live:** in the repeatable passages — jobs, pickups, the weekly cycle — not on the
always-on surface (0–16 surface reads per game against 7–934 elsewhere; failing games, numbers only).

⚠️ **W5 owns the meter that closes; W5b owns the meter that talks.** Gating content behind a rising
audience meter is W5's thing, and W5's test applies to it, not this one's.

#### How "it delivers people" is built on this engine

`patriarch`'s shape has a native home here and it is the **Lane 3 dispatcher**. A substitution rule
already takes an optional `conditions` block, evaluated per rule at
`v2.py:5993` — so banding a walk-in on the meter is one block, no engine work, no new primitive.

```toml
[[canvases.trigger.substitutions]]          # the existing rule, untouched
target_canvas_id = "walkin_office_driver"
chance           = 0.30
exclusive_group  = "counter"

# ...every other rule in the group, then LAST:
[[canvases.trigger.substitutions]]
target_canvas_id = "walkin_office_driver"   # the SAME walk-in, at a bonus rate
chance           = 0.15
exclusive_group  = "counter"
conditions       = { version = "1.0", logic = "AND", items = [
  { type = "trait", subject = "player", trait_key = "standing", operator = "lt", value = 40 },
] }
```

⚠️ **APPEND it, never prepend it.** Rules sharing an `exclusive_group` share **one dice over
cumulative buckets** (`v2.py:6001`), and a slot the dice claims whose conditions fail **falls
through to solo rather than promoting the next rule** (`v2.py:6034`). Appended, the bonus rule
takes a bucket that already fell to solo, so outside the band **nothing changes**. Prepended, it
takes the bucket in *front* of the rules below it and silently cuts their rate at every band —
including the NPC walk-ins, which have nothing to do with this meter.

⚠️ **Copy the conditions from the rule above and add the meter item.** A bonus rule that drops the
presence gate still claims its slot and still fails — on the wrong reason, looking identical from
the outside.

⚠️ **Decide which direction the meter points, out loud.** A rising audience meter that delivers
*more* is right when being known is the fantasy. When the fantasy is the title being **stripped**,
it is backwards, and the meter should buy standing in one room while costing traffic in another.
Either is a trade the player can run; what fails is not choosing.

**Prove it with a distribution, not a playthrough:** call `setup.checkAndSubstituteCanvas` a few
thousand times, with `player.current_location` set and at an hour a named walk-in can fire, and
check both that the rate moves inside the band and that every other outcome stays flat.

### Its reads are one-line swaps, and that is why there are hundreds of them

The reference game's 610 read sites have a median branch of 139 characters (numbers only).
**The branch size is the cause and the count is the
symptom**: swap one line of dialogue, not a block.

A player states the failure from the other side, about a game whose corruption meter moved in
silence: they asked for *even just a few lines of dialogue* at the thresholds, because the change
felt like **a switch turned on somewhere** (`findings_J_players.md` §6).

> **A meter that rises without anyone in the world saying so reads as a switch being flipped.**

### Split it — one global number is the degenerate case

Split at least by **what** she is known for (the reference game, numbers only, keeps fourteen kinds
and two places). Better, split by **who**: Course of Temptation keeps rumours per person, so one
character knowing is not the room knowing — per-NPC traits and flags here (`engine.md` §8).

**Two mechanisms worth stealing if you split by person:**

- **Opposites cancel before they accumulate.** CoT pairs `promiscuity ↔ reservedness` and
  `kindness ↔ meanness`; raising one *drains* the other first. She cannot be known as modest and
  known as easy at once — a new reputation eats the old one.
- **Intimacy buys silence.** `juiciest_rumor` returns nothing for anyone in a friendship or romantic
  relationship. Who *won't* talk is as designed as who will.

### Positive bands are not decoration

In the reference game (numbers only), being known as decent is what gets her helped, and being known
as someone who fights re-colours a threat. **A reputation system that only counts what she is
ashamed of is half a system.**

### Not a gate

No threshold here; `gates.py` is unchanged (`findings_H_known.md`).

---

## W6 · The cast's meters — light or load-bearing, and W1 decides which

> **Which of the three this is.** W5 is the **counterweight** — one falling number that shuts doors.
> W5b is the **audience meter** — it rises, it is read constantly, and it almost never refuses.
> **W6 is the cast's own gating meters**, one set per character, and it is the only one of the three
> that is per-person. A rule from any of the three does not transfer to the other two.

### Each man keeps his own score, and it is shown

> **Each man keeps what `want.cast[].keeps` declares (W1), and his numbers are shown (D1).** Two men
> on the same keeps differ by their modifiers ("The meter is a trade", below).

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

The default the template shipped is `core_traits = { relation = 0, lust = 0 }` on every character.
Replace it with what each man's `keeps` declares (W1's table). For a **ladder** game a step counter +
memory flags is correct and deliberate: the tiers do the gating. For a **roster** game his numbers
*are* the engine. Two rows the W1 table does not cover:

| the relationship | what he keeps |
|---|---|
| service / workplace | trust only; willingness does not apply |
| **someone she already belongs to** | **no climbing meter at all** — presence plus one opened flag. He is not a conquest; the variation is in pose and framing, not in a rising bar |

A suspicion or a debt he holds is a number like any other: shown, and he reacts when it crosses.

- **Match the keeps to the man.** The reference game gives its rich model to three housemates and
  runs its other fourteen characters light.
- **A character who gates nothing is not in the game yet.** A full meter pair with zero gate
  sites on either meter is a character the player can raise and nothing ever answers.

### The meter is a trade, not a bonus

Added 2026-08-24 from Section G. An identical meter pair across a roster cast is *the
engine missing*. This is the half that was missing from W6 itself: **picking a different meter is
not enough if every meter only ever opens things.**

`inseminator` (numbers only: its text never states its cast are adults) ships its own design spec
as a player-facing help page. Six relationship traits, each
a one-line character summary plus three to five numeric modifiers — and **five of the six make one
route cheaper and another route more expensive**:

| trait | who she is | what it buys | what it costs |
|---|---|---|---|
| **Romantic** | "Believes in true love" | +10% girlfriend, roses +4 affinity | **−15% polyamory** |
| **Clingy** | "Needs constant attention" | +20% girlfriend, +2/mo if dated | **−30% polyamory, −3/mo if ignored** |
| **Independent** | "Values her freedom" | +20% polyamory | **−10% girlfriend, −15% estate, decay doubled** |
| **Jealous** | "Possessive and suspicious" | +5/mo if dated | **+20% jealousy event, +10% breakup** |
| **Precious** | the hard one to win | +20 Matron | **−5/−10/−15% on the three intimacy steps** |
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

- **A trait can be spent.** `Precious` carries a loss condition: it is lost when affinity falls
  below 20. The personality is consumed by the thing it was gating.
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

**Lint · the cast's meters.** Per character: which meters they own and how many gate sites each
carries, plus how many distinct shapes exist across the cast.

---

## W7 · The body's meters are read to colour, and gate only at doors that say why

> **A body value — clothes, arousal, hygiene — earns its place by changing the words in
> a lot of places, not by closing doors in a few. Build it to be READ CHEAPLY AND OFTEN. Gate on
> it only at a door that says why: a daring price to leave in a revealing state, a dress code, a
> place that wants her bare. A gate that hides its reason is the field's biggest clothing failure
> (41 of 194 classed player failures, round 9a §5).**

W5 is the counterweight that shuts doors, W5b the audience meter that almost never refuses, W6 the cast's own
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
Over 13 games it is ~10% link-bearing and a **median 41% of reads change something mechanical**
(W5b). The same law, many small swaps over a few large branches, from a third instrument.

**The exceptions are real and they are all small.** `new-life-project` gates 91% of its arousal
reads — of **43**. `wasteland-lewdness` gates 63% of its clothing reads — of **35**. `patriarch`
gates 47% of its pregnancy reads — of **34**.

> **A body system either stays small and gates, or grows large and colours. Nothing in the corpus
> is both big and gating.**

**Clothing is the one body system with doors, and the doors are few and loud.** Course of
Temptation enforces a dress code on 61.9% of its location passages (78 of 126; round 9a §2), and its
clothes still gate only a small share of reads: a dress code is one read per place, and the rest are
lines. Each of its blocks names what is missing (*"(Need Exhibitionism N)"*), and In Her Own Hands'
club refusal sends her back to the wardrobe. Gate at the door, say why at the door, offer the change
(`engine.md` §17: a dress code offers it; an `entry_conditions` refusal cannot yet).

### The band ladder — write it once

The mechanic underneath every one of these is the same: a number, a ladder of bands, and a short
string per band. What separates a good implementation from a bad one is **where the ladder lives.**
One counted game writes it once, seven rungs wide; `corpo-life` (counted) writes the identical
structure **inline, across 5,785 sites**.

Note what the bands say: **a body state in words**, printed beside the number (M7), so the player
meets both how she is and how far. Our surface for this is `trait_status_text` (`engine.md` §30) — one
authored ladder, rendered wherever the trait sits.

### What the player is shown

**Numbers are shown and named, and the world reacts to them** *(LO decided, D1; R3 K12: corruption is
a number in 13 of 15 top games)*. One counted game's body system is a three-state value derived from
the worn set; its world reads it about **900 times**, and 82% of those reads only change words. **One
derived number, cheap enough to test that the whole world tests it.** Ours is `worn_exposure`, and the
states read through it. W3's gate makes sure somebody reads it.

1. **Her traits show as name + number**, with a band word beside it where it has bands (M7). One name
   per trait, everywhere (`engine.md` §30).
2. **A man's numbers show on the cast page**: every trait he keeps (W1) goes in `show_traits`, with a
   word beside it (`engine.md` §34).
3. **After a choice, a reaction line and the toast.** The engine's "+N" toast stays *(D1b)*; the first
   line of the next node is his reaction. A `+X` label for a stat that does not exist is still wrong —
   lint `a printed stat is real`.
4. **When something is out of reach, the requirement is told**: the guidance card's trait goal prints
   *"14 / 20"* (`the-voice.md` R3b), and a locked button prints the need (R4). Players ask *"how do I
   raise X"* far more than *"show me X"* (4 of 22,252 comments ask to see a stat).

⚠️ **The one number is `worn_exposure` (0 covered, 1 underwear-level, 2 bare), and the states are
its readers.** `worn_corruption` and `worn_beauty` skip an empty slot, so naked reads the same as
plain underwear; `worn_exposure` reads the empty slot, and `clothing_slot` names a state exactly
("no bra"). The mechanism is `engine.md` §17. Design the states first — dressed, skirt, no bra, no
panties, underwear, towel, topless, naked — and read each one in ≥3 places: a leave rule, a place,
an event or an NPC line (round 9a, the wardrobe card). Gate `every clothing state is read three
times` (a `--ship` block) counts a reader when it is the same predicate and slot with values that
overlap the state's; a dress code reads the slots it names; choice conditions do not count.

⚠️ **And copy where the reads live, not just the number.** In the counted game that reads exposure
most, the passages that gate on clothing most are five streets and open places — the walk to work,
not the sex scenes — with roughly twenty per-district reactions, so walking out underdressed means
something different in each. **One
ambient at one location, gated on exposure AND on somebody being there to see it, is the whole
starting move**; add the second when the first earns it. A derived number that only the wardrobe
screen reads is the same defect in a new place.

⚠️ **Exposure is not a property of the outfit. It is a property of the outfit in a PLACE, with an
AUDIENCE** — and this is the half that is easy to miss, because the number itself hides it. The same
counted game computes the place before the clothes: a list of safe places where anything goes with
nobody present, and water places where a swimsuit is nothing; its audience check is consulted 14
times. Naked in her own bedroom is nothing; naked on the street is the event.

**Our engine reaches the same place from the other direction, and the place half costs nothing.**
That game centralises the judgement in one function that knows which places are safe. We distribute it:
a canvas is bound to a location, so an exposure ambient only fires where an author put it, and her
bedroom is safe by simply having none. The audience half is `npc_at_location` with no `npc_id` —
the any-NPC "room occupied" form (`v2.py:5246`). **Gate on both.** An ambient that fires in an empty
room is the game talking to itself.

**The starting move, written out.** A random ambient at one location that can only fire when she is
underdressed — copy it, change the place and the words:

```toml
[[canvases]]
id   = "event_market_underdressed"
name = "The market notices"

[canvases.trigger]
location      = "the_market"
is_repeatable = true
is_active     = true
priority      = 3
trigger_mode  = "random"
chance        = 0.35
conditions    = { version = "1.0", logic = "AND", items = [
  { type = "worn_exposure",   operator = "gte",        value = 1 },
  { type = "npc_at_location", operator = "is_present", location_id = "the_market" },
] }

[[canvases.nodes]]
id = "base"

[[canvases.nodes.blocks]]
type    = "paragraph"
content = "The woman on the fruit stall looks at her twice and does not pretend otherwise the second time. Somebody behind her says something she is glad she cannot quite hear, and the man weighing her apples takes slightly longer than he needs to."
```

⚠️ **`version = "1.0"` is not optional.** A `conditions` block without it **fails open** — the engine
returns true and the ambient fires whatever she is wearing, which reads exactly like the feature
being broken. `engine.md` records the same trap for `entry_conditions`.

⚠️ **`trigger_mode = "random"` is what makes it an ambient.** The default is `"manual"`, which renders
a clickable link instead of firing on entry — a link labelled *"The market notices"* is not the same
content and gives the game away.

⚠️ **0/1/2 on the garment is the right scale, and this was checked rather than assumed.** The counted
game's gated garment field is **0/1/2** — 515 garments at 0, 37 at 1, 5 at 2. A separate 0–10000 look
rating feeds its colour and NPC lust checks; **our nearest equivalent to that is `beauty`, which we
already have.** So `exposure = 0` as the default is correct too: the overwhelming majority of real
garments cover.

⚠️ **Write the second one different.** The whole value is that the market and the depot do not react
alike; two locations sharing one paragraph is the readout again, wearing a coat. And `gte 1` is right
for a public street — save `gte 2` for the places where being bare is the event itself.

---

# The ascent's price

## W7b · Pregnancy is a story option behind a start choice

**Pregnancy is not colour; when a game takes it, it is a story the player opted into.** Course of
Temptation puts it behind a content toggle, with tunable fertility and duration, a father record, and
people who react once she shows; other games' players ask for it (*"Can i get pregnant?"*). Players
want *"Realistic pregnancy that has consequences"* and punish a roll that never lands (*"I had 98
loads"*): state the odds, and let them be tuned.

Five parts, all existing engine pieces, proved in one fixture (`round5/ic10_pregnancy_fixture/`):

1. **The toggle is a start choice, and it says what it turns on** (R5b.3 — warned, opt-in):
   *"Turn pregnancy on: sex without protection can get her pregnant, and it changes her story."*
2. **The risk lives on the choice** (*"Let him finish inside you"* sets `risk_tonight`; the daily
   tick clears it).
3. **The roll is a `trigger_mode = "random"` canvas** on the toggle, the risk and stage 0; `chance`
   is the odds.
4. **A stage trait advances once a day** (a `_today` flag). **The duration is the author's** — no
   default here; the fixture's three days are test speed only.
5. **A father flag per partner**; the portrait's `pregnancy_trait` swaps the image.

**Decide the last stage before the first** — a birth, the story moving on, or another ending of the
author's — and write it in the board. The fixture ends in a birth that resets the stage.

⚠️ **Engine limit:** the portrait code, and its pregnancy swap, ships only when `[settings]
clothing_enabled = true` (`v2.py:1633`). A small engine fix — the portrait swap independent of the
wardrobe — is listed, not built.

## W8 · What sticks — and every door it closes is warned

**Her reputation, her body, a relationship, the story: each can stick, each is visible, and each is
warned before it closes anything** (`the-arc.md` A3).

> ⚠️ **EVIDENCE — NOT A TEMPLATE.** `course-of-temptation` labels a closing choice:
> *"(Permanently removes this character)"*. `shady-deals` prices reputation on the button (−500).
> `cupids-way`'s tattoo is announced — *"You are now permanently marked"* — and temporary ones come
> first. `in-her-own-hands` puts rent due on the screen and a date in her father's mouth: *"You will
> owe $1,500 as of three months from when we first spoke."*
>
> The failure is a consequence never read: `cupids-way` writes *"Let's hope he doesn't find out"* and
> nothing checks. Players notice — *"there is No risk in the game"* (`course-of-temptation`).

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

The tell that this has gone wrong is not the threshold; it is the **rate**. When judging a tier,
always compute the same two numbers:

```
clicks to the top band  ·  in-game minutes to the top band
```

`the climb is paid for` prints both numbers for every free route (gates.py:8567).

### M3 · The throttle menu — four levers, and none of them works alone

| lever | what it does | where it fails |
|---|---|---|
| **1 · Threshold spacing** *(always on)* | widen the gap between rungs while keeping the per-beat increment fixed, so the climb takes days | does nothing on its own — 55 free clicks is still 55 free clicks. And **don't over-space a thin repeated beat**: if the rung is one recycled paragraph, a huge bar is just tedium |
| **2 · A window-sized time cost** | `time_progression_minutes` on the rung's exit. The best-*reading* throttle: it is fiction, not a mechanic, and no single deleted line removes it | **only bites when sized against the window.** A 10-minute rung against an all-day hub is farmable ~144× per day. A 180-minute rung against a 09:00–18:00 NPC window is ~3/day. Advancing past an NPC's schedule window makes them absent, which is what actually stops the rung |
| **3 · A counted daily cap** | `max_triggers_per_day` on a *triggered* canvas, or a `_today` flag cleared in `[engine.daily_tick]` (§28) | **`max_triggers_per_day` is read off the trigger (`v2.py:12923`) — a triggerless rung has none.** |
| **4 · A resource cost per rung** | `costs` (§27). Gate-enforced — the engine does not offer a rung the player cannot afford | energy is the wrong *primary* lock for a relationship ("too tired to seduce him" is bad fiction). It is a legitimate *throttle* when the fiction supports it, and it is the strongest tool available to a triggerless rung |

### M4 · The recipe — layer all three

> **Spacing (always) + at least one hard throttle + the rung PAYS, visibly.**

- **Spacing** is free and always on, but never counts as the brake.
- **A hard throttle** is lever 2 sized to a real window, or lever 3, or lever 4. Prefer **two**.
- **The rung pays** — brake-only is grind. If a rung costs energy and time and gives back nothing
  the player wanted, you have built a chore. The payoff is content, not a number: a new line, a
  clip they have not seen, a door that opens.

### M5 · How to throttle a TRIGGERLESS rung

A rung reached by a hub choice is **triggerless**: a canvas with no `[canvases.trigger]` block.
That single structural fact voids the first tool everyone reaches for.

```
max_triggers_per_day  →  read off the trigger (v2.py:12923)  →  DOES NOT APPLY
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
> choice     traitEffects -> flagEffects -> costs -> … -> advanceTime   v2.py:14843-14845 · :14921
> node exit  advanceTime -> traitEffects -> flagEffects                 v2.py:15252-15261
> ```
>
> `advanceTime` rolls the day inside itself (`v2.py:6601-6604`) and that is where the tick clears
> every `_today` flag (`v2.py:6741-6743`). So an **exit**-set cap on a rung that crosses midnight is
> written *after* the clear, and the new day starts already capped.
>
> A sleep rung that runs from evening to morning with its cap on the exit is never offered before
> midnight again after the first night, and nothing in the build, the validator or the scoreboard
> says a word.
>
> ⚠️ **A LOCATED canvas does not need a flag at all.** `max_triggers_per_day` is read off the
> trigger (`v2.py:12923`) and `markCanvasTriggered` stamps the day key *before* `advanceTime`
> (`v2.py:4803`), so it is immune to this. Reach for the flag only when the rung is triggerless.

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

- ✅ bounding a restore — a sleep rung adding energy
- ✅ bounding a repeatable relation grant so one rung cannot max a character on its own
- ❌ **never on an ascent tier** — the tier must reach its top band, and a cap there deletes content
- ❌ it is not a throttle. A capped rung is still infinitely clickable up to the cap.

### M7 · Band a meter, show it once

The sidebar prints a trait twice — once from the auto Traits dump, once from whatever
`[[sidebar_items]]` you wrote — and the two do not know about each other (§30).

**Every trait carrying `bands` in `[[sidebar_items]]` needs `in_dump = false` in `[[traits.labels]]`**,
so its number shows once, in the item. A trait absent from `[[traits.labels]]` entirely is *not* kept
out; it prints. Don't use `hidden = true` for this: it is the secret-trait switch, and because it is
keyed by name it hides every man's trait of the same name.

The sidebar shows the number *(D4)*, and every item carries a `label`:

| kind | example | sidebar type | reads |
|---|---|---|---|
| sex trait | corruption | `trait_words` + `bands` + `show_value = true` | *Corruption: 12 · Curious* |
| body need | energy | `trait_bar` + `bands` (no `hide_value`) | *Energy: 60 / 100*, a bar, the band word |
| money | money | `trait_words` + `show_value = true`, no `bands` | *Money: 140* |

**Gate 27** (*a banded meter is shown once*) fails a banded item whose key is neither `in_dump = false` nor
`hidden`, or whose item prints no number. It is deterministic — no threshold to invent.

⚠️ And the other half: a banded value that lands **outside every band renders nothing at all** — the
card vanishes, which reads as a missing HUD element rather than a wrong number. Leave the top band's
`max` off (`trait_status_text` treats it as open) or `cap` the terminal add. See §30.

---

# The body's meters — needs

M1–M7 govern the **ascent**: a meter that climbs and buys access. A need is the other kind of meter
and it runs the opposite way — it **falls on its own**, she refills it, and while it is empty
something is shut.

**Needs are declared per game, never a fixed list.** A truck stop's body is not a
household's. What is fixed is the *form*.

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

`shuts` also routes her: a need that is empty sends her to the place that refills it, and that place
rolls an event (`engine.md` §30.1). A need behind a content toggle has an off switch, a start choice
(`the-surfaces.md` R5b.4); with it off, nothing reads it.

The field, on the fourth field:

| game | need | what it shuts |
|---|---|---|
| Apocalyptic World | hunger | `Eat` needs food **in the pack** — no food, no meal |
| Become Someone | hunger | breakfast / dinner / dishes are **once each per day**, in their own windows |
| Degrees of Lewdity | ingredients | a recipe you lack the stock for **cannot be cooked** |

### M9 · A need that shuts nothing is a chore

**Gate 29.** Every key in `board.needs[]` must be read by at least one condition somewhere in the
game. Deterministic, no threshold to invent: either something gates on it or nothing does.

A restore with no gate behind it is a button that maintains a number. It costs the player time and
buys them nothing.

**This is also what makes a room worth entering.** `the-surfaces.md` R2 says a room's list is needs,
systems and people — a *need* on that list has to be a real one, or R2 degrades into the object rule
with different nouns.

### M10 · The clock is `[player.trait_decay]`

```toml
# Decay is a POSITIVE MAGNITUDE — the validator rejects a negative (engine.md §11).
[player.trait_decay]
energy  = 8
```

It is the cheapest half of a need — the half most
games do write. **The half they drop is `shuts`.**

Two shapes, and pick on purpose:

- **decay** — falls every day whether or not she does anything. Right for energy, and for hygiene
  when the game has it (`engine.md` §30.1).
- **spent** — falls only when something takes it, via `costs` on a trigger (§27). Right for a
  resource.

A need can use both. What it cannot do is neither, which is a trait that only ever goes up.

**Decay stops at a rest point and never crosses it.** Each night a decaying trait moves by its amount
toward its rest point, from either side. The rest point is 0 unless you set one, so a value below 0
climbs back up to 0. A man can have his own settings:

```toml
[[npcs]]
id               = "vic"
trait_decay      = { trust = 10 }
trait_rest       = { trust = 20 }   # his trust cools to 20 and stops there
decay_after_days = 2                # he starts cooling only after two days apart
```

Seeing him resets the wait, and a man she saw that day never decays that night.
