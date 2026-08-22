# The Meters — which ones exist, what the climb costs, and what the player reads off it

The ascent tiers are this skill's whole thesis: **a meter that buys access.** Every other file here
is about *what* the meter unlocks. This one is about the meters themselves.

**Three parts, and they are read in order.**

**W1–W6 — which meters exist and who owns them.** The decision that comes before every other one on
this page: does the PLAYER climb or does the CAST, what a throttle is actually for, how deep a
ladder goes, and whether a number anything reads. Missing entirely until 2026-08-19, which is why
five games shipped the same meters without anyone choosing them.

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
> In the field a sexual-state meter is a real gate in **12 of 25 games**, and where it exists it is
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

**Lint · the counterweight.** Heuristic, which is why it is a lint: a player trait starting at 50+
whose effects mostly fall, declared needs excluded. It prints how many times the thing is read.

---

## W6 · The cast's meters — light or load-bearing, and W1 decides which

The default the template shipped is `core_traits = { relation = 0, lust = 0 }` on every character.
Measured, all five v2 games: **one distinct meter shape across the whole cast, every time.**

For a **ladder** game that is correct and deliberate — the tiers do the gating and a bond meter
colours the arc. Say so and move on.

For a **roster** game it is the engine, and an identical pair on everyone is the engine missing.
Pick each character's gating meter from what the relationship *is* — adapted from
`author-game/references/trait-design.md`, which has the full version:

| the relationship | what gates the rungs |
|---|---|
| peer / dating | their **bond**, in small milestones — courtship is the climb |
| slow burn / escalation | their own **willingness** odometer, warmed by a throttle |
| leverage / transactional | money or debt — not affection |
| service / workplace | trust only; willingness does not apply |
| antagonist / witness | a hidden suspicion accumulator, never surfaced |
| **someone she already belongs to** | **no climbing meter at all** — presence plus one opened flag. He is not a conquest; the variation is in pose and framing, not in a rising bar |

Two more rules that survive from v1 and are worth restating:

- **Reserve the rich two-meter model for the one or two arcs that carry the game.** The reference
  game gives it to three housemates and runs its other fourteen characters light. Gold-plating
  every character dilutes the core and triples the authoring.
- **A character who gates nothing is not in the game yet.** `the_allowance` ships two of five
  characters with a full meter pair and **zero** gate sites on either.

**Lint · the cast's meters.** Per character: which meters they own and how many gate sites each
carries, plus how many distinct shapes exist across the cast.

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
