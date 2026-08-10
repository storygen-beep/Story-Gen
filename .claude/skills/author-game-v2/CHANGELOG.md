# author-game-v2 — changelog

The skill-level ledger. Every edit to any file in this skill gets a dated bullet here in the
same turn: what changed, why, and how it was verified.

---

## 2026-08-11 — v0.1 Phase 1: the anchor, 5,123 → 9,607, and three engine facts it cost

**What.** The front room taken from 5,123 words to 9,607 in one pass — the anchor budgeted
against the *finished* 36,000-word total (where it owes ~9,000) rather than the current one,
because the ratio tightens every time any other room grows and topping it up later means
writing it twice. Files touched: `games/back_home/toml_phases/5_scenes.toml` and
`3_activities.toml`, plus `references/engine.md`, `SKILL.md` and the game's `v2_state.json`.

Gate 1 still fails, as expected and as planned — mean 2,360 against 4,500, median 1,496 against
3,000. It closes when the seven satellites are filled. What this bought is the right to fill
them without the anchor sliding under 25% on the way.

### The register rule was written from this game's own failures and never applied to it

`references/register.md` quotes, as pivot target #3, the sentence *"…and the arithmetic does not
come out the way it is supposed to."* That sentence was still sitting at the end of
`loop_ray_arrangement`, and the beat carrying it scored **zero**. Measured per beat, all three
repeatable sex loops failed the same way in the same place — their *tails*:

| | beat 1 | beat 2 | beat 3 | beat 4 |
|---|---|---|---|---|
| `loop_ray_arrangement` | 4 | 1 | **0** | 0 |
| `loop_dean_late` | 3 | 1 | **0** | **0** |
| `loop_cal_sex` | 4 | 3 | **0** | 0 |

Every loop opened explicit and then left the body exactly when the act got closest. The fix was
the one the doctrine already prescribes — keep the camera on the body to the last sentence, and
give the interiority its own beat *after* — and it moved the whole game **10.8% → 15.9%** of
beats at 3+ explicit words, without one gratuitous noun.

**Two words worth knowing are NOT on the frozen list:** `wet` and `come` (the latter excluded
deliberately, since it matches "come downstairs"). Three finishing beats rewritten to be
relentlessly physical still scored 2, because they leaned on both. The list is the instrument;
write to the body and check the number.

### Three engine facts, each caught by a build that refused to run

1. **The documented build command was wrong** — in `SKILL.md` *and* `references/engine.md`.
   `package_from_toml` takes named, required `--file` and `--output`; the positional-plus-
   `--output-dir` form both files carried exits 2 and builds nothing. `python` may not be on the
   path either. Both files corrected. A skill that cannot build the game it authored is a broken
   skill, and this had been shipped since the first release.
2. **Move a flag setter — never duplicate it.** `cal_arrangement` was set on the located hub
   choice *and* left on the triggerless loop. The validator resolved it to the one without a
   location and hard-failed with `MISSING HINT`, naming the loop's canvas name (`Take him
   upstairs`), which reads exactly like the hub choice of the same wording. §16 sharpened.
3. **One repeatable canvas per location + NPC + time window.** The two-men scene was written as
   a located canvas and the build warned that `hub_dean_late` already owned `npc_dean` at the
   front room. It is a *warning*, not an error — a canvas shadowed this way looks correct in
   TOML and is unreachable in play. New §19; treat the warning as an error.

### `npc_at_location` promoted from "known" to "verified live" (new §20)

`generators/v2.py:4131-4145` and `:7791`. **`npc_id` is optional — omit it and the predicate
tests whether the room is occupied by anybody.** Confirmed in the built game rather than read:
the two-men choice rendered at 23:10, where Ray's 20:00–23:30 row overlaps Dean's 23:00–01:30,
and was gone at 23:45 with identical player state.

That single fact carried the increment's two new content kinds. Conditions on a *choice* are
evaluated live at render, so the scene the engine refused as a canvas works better as a rung on
the existing hub. And the any-NPC form let the TRIGGERED piece — she crosses the room in what
she sleeps in and does not look to see which of them is in the chair — bind **no NPC at all**,
which is both the content and a structural guarantee that no dialogue can be mis-attributed.

### Live-testing this engine, for whoever writes the next harness

Static parsing cannot see a passage that errors. Three things about the built game are not what
a reasonable person would guess, and each cost a run:

- `State` and `Engine` are **not** bare globals. Use `SugarCube.State`, `SugarCube.Engine`,
  `SugarCube.setup`.
- `$flags` is an **object** keyed by flag name, not an array. `.includes` throws.
- Player traits live at `player.core_traits`, not `player.traits`.

All fourteen new or rewritten passages then rendered clean: no JS errors, every cascade
advancing, and no speaker outside the four declared characters.

**9/10 holds.** Nothing else moved: explicit-in-repeatable 100%, standing surface 4/4,
milestones 4/4, meter ceiling clean, four locked doors still shut. Three new promises logged
(Dean's uncharged version, Ray's knowing, Cal's £840). The stray `Wren-solo` labels — Vesper's
protagonist used as a pattern name in a game about June — are gone.

**+17,100 remain**, all of it in the seven satellites.

---

## 2026-08-10 — v0.1 increment 2e-4: the box room and the shop, and a bug in my own prose

**What.** Box room 908 → 1,228, shop 76 → 654. Two new promises logged.

### The bug, and the structural reason behind it

Hannah Beckett — a woman June sat next to for two years, walking into the shop — was written as
a `dialog` block attributed to **`npcId = "npc_marek"`**, because she is a walk-on with no NPC
record. It would have rendered **"Marek:"** over her line in the built game.

Fixed by making it quoted prose. But the interesting part is *why it can't be fixed the obvious
way*: declaring Hannah as an `[[npcs]]` entry would immediately **break gate 6**, which requires
every declared character to have a standing surface and a schedule row.

**The gate is right.** A character with a name and no way to find them is exactly the defect it
exists to catch — Vesper's `npc_bastien`, referenced 88 times and reachable nowhere. So
**one-scene characters are narrated, never declared.** That is a real constraint the gate
imposes on authoring, and it is a good one.

### A lint worth adding to `gates.py`

> Flag any `dialog` block whose `npcId` names a character the canvas neither **binds**
> (`npc` / `requires_npc`) nor **names in its id**.

Run over `back_home` it returns exactly **2** hits — both `canvas_arrival`, which legitimately
has Ray and Dean speaking in the opening — and it **would have caught the Hannah bug**.

The naive version (flag dialogue on any unbound canvas) returns **30 false positives**, because
every triggerless rung is unbound by design and correctly carries its own character's voice.
Worth noting how much narrower the useful check is than the obvious one.

### The shop is the mirror

The regulars are banded on `pride`, so the same six hours read as humiliation, then as rest,
then as camouflage. And `canvas_someone_who_knew` is the reversal made visible **from outside the
house** — the only vantage it can be seen from. From out there the story is short and finished:
*June went, June came back, June is at the shop.* The house is the only part still moving.

**9/10 held.** Fill 12,496 → 13,394. Explicit floor 10.1% → **9.6%**, an expected dip: this was
deliberately the least explicit increment in the game, because the shop is the one room where no
man wants anything from her and that is its entire function. Still comfortably above 7.5%.

⚠️ **Anchor at 34% and drifting down** — the trap from last increment is live. The front room
needs its next instalment before much more is written elsewhere.

**+22,606 remain.**

---

## 2026-08-10 — v0.1 increment 2e-3b: the anchor trap, and the last empty schedule row

**What.** The garage (309 → 801) and an anchor instalment on the front room (4,020 → 4,556).
Added the fill-in-step rule to `references/the-board.md` and corrected §16 of
`references/engine.md`.

### The anchor trap — a ratio gate tightens while you work elsewhere

Gate 1 wants the anchor at **≥25% of all location prose**. That is a ratio, so every word written
anywhere else lowers it. The front room sat at 4,020 through six increments of building other
rooms, and its share fell **53% → 46% → 40% → 39% → 35%** without a single word being removed.

Held there, it crosses below 25% **within one more increment** — the game going 9/10 → 8/10
while getting objectively better.

**Budget the anchor against the finished total, not the current one.** At a 36,000-word target
the anchor owes 9,000, so its share is planned into every increment rather than topped up at the
end. Now doctrine in `the-board.md`.

### The flag-chain rule was recorded too narrowly

Hit it a second time with `ray_arrangement`:

```
✗ ray_arrangement   required by choice 'Sit with him after.',
                    set by 'Stop pretending it's a favour' but no location/schedule
```

The validator refuses a flag set in a triggerless rung when it is read by a **choice**, not only
by a trigger. Same fix both times — move the `flagEffects` up onto the located hub choice.
`engine.md` §16 now reads "a TRIGGER **or a CHOICE**".

### The last empty schedule row is filled

Dean was present in the garage 14:00–17:00 at weekends with **zero content** — the only scheduled
row in the game with nothing on it. Verified live at Saturday 15:00. He now carries three
surfaces. The scene is the one version of him with no audience: *he cannot do the funny voice
under a bar*, so between the fourth and fifth rep he is straightforward for the first time since
they were children.

### Scope honesty

The plan named three targets and this increment hit two. **The box room was not touched** and
remains at 908; it carries into the next increment rather than being quietly dropped.

**9/10 held.** Fill 11,468 → 12,496; anchor back to **36%**; explicit floor **10.0% → 10.1%** —
the second consecutive increment where new content raised it rather than diluting it, which is
`register.md` continuing to hold. **+23,504 remain.**

---

## 2026-08-10 — `references/register.md`, and the first increment that RAISED the explicit floor

**What.** Wrote the skill's missing prose doctrine, then authored the kitchen against it. Kitchen
698 → 1,775. Linked from `SKILL.md`'s operating rules.

### The gap

Checking why the same defect had recurred three times explained it: **the skill said *where* the
crude register lives and *which words* were permitted, and nothing at all about how to write the
beat.** There was no prose reference. The Want template's §6 is entirely placement and vocabulary
ceilings.

### The rule, and its test

> **An explicit beat stays on the body for its whole length.**
> **Diagnostic:** if the beat's last sentence is about what it *means* rather than what is
> *happening*, it has pivoted and will score 0–1.

`register.md` names the three pivot targets — *he knows* / *she is ashamed* / *what this says
about her* — so they are catchable while writing, and puts the interiority in **its own beat,
after**. Cascade beats are free, so splitting costs nothing and sacrifices none of the
psychology, which is the part that makes the game good.

It also states what the fix is **not**: not word-stuffing, and not loosening the frozen wordlist.
The list has been challenged twice and was right both times.

**The test:** doctrine written first, kitchen authored against it, gate run after.

| | before | after |
|---|---|---|
| beats | 106 | **120** (+14) |
| explicit beats | 10 | **12** |
| explicit floor | 9.4% | **10.0% — up** |

**For four consecutive increments new content dropped the floor and had to be rewritten after the
gate caught it. This time it went up, on the doctrine's first use.** That is the strongest
evidence in this project that a written rule can actually change what gets authored — but only
once the rule says *how*, not merely *where*.

### The kitchen

Four surfaces against the schedule already built: Cal 07:40–08:00 (twenty minutes, cannot look at
her, and the mugs are on the shelf above his head), Dean 08:00–09:00 (down from the bathroom she
watched him in — the entire scene is the not-mentioning), Marek 16:00–17:30 (the only hour the
two of them are the only adults in the house, and the only meal anybody eats sitting down). Marek
and Cal now carry two surfaces each.

**9/10 held.** Fill 10,391 → 11,468; median 1,367 → 1,496. **+24,532 remain.**

---

## 2026-08-10 — v0.1 increment 2e-2: the morning queue, and the register defect is *mine*

**What.** Dean given a bathroom row; two new peeps; two new walk-ins; the wall paid off. Bathroom
845 → 1,517, landing 681 → 1,367.

### The finding that matters more than the content

The new scenes added **sixteen beats and zero explicit ones.** Every one scored 0 or 1 against
the 3-word floor, dropping the game to exactly **7.5%** — the boundary.

The pattern is identical every time: **name a body part once, then pivot the next beat to
psychology** — he knows, her face is burning, what it means. The heat sits in the situation and
never in the words.

This is the defect diagnosed in Vesper, reproduced by the author who wrote the doctrine against
it, **for the third time — twice after writing it.** That is the actual finding:

> **It is not a lapse. It is a default that reasserts itself the moment it is not being actively
> fought, and the gate is the only thing that catches it.**

**The fix is not word-stuffing.** It is to stay on the body *through* the beat rather than
referencing it once and moving on. Eleven targeted rewrites took the floor **7.5% → 9.4%**,
which sits at the *top* of the reference game's measured 7.5–9.3% band rather than scraping it.

### The morning queue

Dean had **no bathroom row at all**, so he could neither be peeped nor walk in on anything.
Adding 07:40–08:00 weekdays makes the grid step cleanly — verified live:

```
06:45  ['npc_ray']    07:20  ['npc_cal']    07:50  ['npc_dean']    08:30  []
```

Three men through one bathroom in ninety minutes. Each of the four peeps is offered only while
its own man is in its own room, including Marek's box-room peep — which needed no new schedule
row, because his door was already established as half open.

### Planted facts, paid

All three night-one details now carry content: the gap down the hinge side (four peeps), the
extractor that makes her deaf (three walk-ins on `activity_wash`'s substitutions at rising
`exposure`), and the eighteen-inch wall (`activity_the_wall`, banded on `nerve` — at the bottom
she is trying not to hear it, at the top she is timing herself to it).

### Tally

**9/10 held.** Fill 8,752 → 10,391; median 845 → 1,367. **+25,609 remain.**

Play-test friction now stands at **four false alarms from page-text assertions and zero real
bugs found by them** — this time a filter that searched for "gap" and "forty" against a canvas
named *"Cal takes his time."* Every real defect this session came from asserting on
`SugarCube.State.variables`. The Player agent's spec should forbid text assertions outright.

---

## 2026-08-10 — v0.1 increment 2e (part 1): the wardrobe, and a silent-failure class

**What.** A 9-item `[[clothing]]` catalog, and her room built out from 68 words — the boxes,
the dressing scene, the door that does not shut, and the solo surface. Added §17 to
`references/engine.md`.

**The most dangerous failure class this project has hit.** To grant the two garments I wrote:

```toml
clothingEffects = [ { itemId = "mothers_slip", op = "grant" } ]
```

The TOML parsed. The validator passed. **The build went green and nothing was ever granted** —
the top tier of the wardrobe would have been permanently unreachable, with no error anywhere in
the pipeline. The real key is `wardrobeEffects = [{ action = "add", item_id = "…" }]` on
`exit_block.config`.

**Nothing catches an invented key.** Not the parser, not the validator, not the build, not the
gates. The only defence is to grep `template_import.py` for any key not personally seen in a
shipped game — zero hits means it does not exist, however plausible it looks. That rule is now
in the engine card.

**The wardrobe is real, not decorative** — the plan's decisive check, and it passes. Verified
live: seven initial garments equip at start; the boxes grant `mothers_sundress` and
`mothers_slip`; equipping the slip moved **`worn_corruption` 2 → 7**; and the dressing scene
rendered its tier-3 band in response.

`worn_corruption` is a **MAX aggregate, not a sum** — one loaded garment sets the reading on its
own. So a catalog does not need to be large to reach a tier; it needs one item per tier. That
makes clothing a genuine gate source for `exposure` rather than a UI ornament.

**Her room** went 68 → 1,215 words, and its four surfaces are all *standing* — which is where
the crude register belongs. The room's thesis is the broken catch: the same action reads as
three different decisions as `exposure` climbs, ending at *"It is a two-pound part. You know
exactly where the hardware shop is."*

**Gates: 9/10 held.** Fill 7,605 → 8,752. Explicit floor 8.9% across 90 beats — still clear as
the denominator grows. **+27,248 words remain** for the last gate.

---

## 2026-08-10 — v0.1 increment 2d: Marek. **9 of 10 gates pass**

**What.** Marek's hub and three rungs added to `5_scenes.toml`. Six open promises logged in
`v2_state.json`.

**The rotating slot is proven.** He is the premise's structural answer to never-ending: Ray
rents the box room to cover the shortfall, so every few releases a new stranger lives in the
house — **a new character at an existing location**, which is the measured release shape built
into the fiction rather than bolted onto it. Replacing him next release should touch only his
`[[npcs]]` entry and his block in `5_scenes.toml`, and nothing about the world.

His window is deliberate: **09:00–16:00, when the house is empty.** The one slot no family
member competes for, and the reason his ladder needs no privacy management at all. He also
carries the only register in the game that is transactional from the first line — no build, no
history, no ceiling to break — which is what makes him legible against three men she is
related to.

**Verified live.** Present in the box room at Tuesday 11:00; all three rungs render with the
fourth locked; the explicit rung applied money 0→50, need 40→45, exposure 60→64, pride 100→94,
his lust 0→8, `marek_arrangement` set. Zero JS errors.

**Gates: 9/10.**

| | |
|---|---|
| standing surface | **4/4** — every character findable and scheduled |
| traversal heat | **5/8 (62%)** — over the 60% floor |
| meter ceiling | clear — every band boundary now buys something |
| ends on an opening | **4** locked rungs |
| ascent tiers | all three gated — nerve 4+, exposure 6+, need 7+ |
| explicit floor | 9.9% across 81 beats |

**The one remaining failure is location fill** — 7,605 words against ~34,000, median 698
against 3,000, mean 951 against 4,500. No location is empty any more; this is not a design
problem, it is the writing a first release costs.

**Six promises logged.** Marek leaving in spring (the slot must be *refilled*, not left empty),
the `keep_unpaid` line *"we'll sort it another way"*, and the four locked 75-rungs. Each is now
tracked and must be paid or explicitly cut — the measured failure mode is a character dangled
for years while players ask *"are we EVER going to…"*.

---

## 2026-08-10 — v0.1 increment 2c: Dean. 6/10 → 7/10, and a build-breaking engine rule

**What.** Dean's two hubs and five rungs added to `5_scenes.toml` — the kitchen at 08:00 (verbal,
daylight) and the front room at 23:00–01:30 (dark, physical). Same man, two registers. Added §16
to `references/engine.md`.

**An engine rule that hard-fails the build, learned by hitting it.**

```
❌ Flag Chain Validation Failed:
   ✗ dean_open
     Required by: Dean (late)
     Issue: MISSING HINT - set by 'Come down in what you slept in' but no location/schedule
```

**A flag read by a TRIGGER must be set from a canvas that has a location.** A triggerless rung
has none, so the game cannot tell the player where to go and earn it. The fix is to move the
`flagEffects` onto the **hub choice** that opens the rung — the choice lives on a located
canvas, the semantics are identical, and the chain resolves. Flags that nothing reads in a
trigger are unaffected.

This is the fourth build-breaking convention found by authoring rather than by reading, after
the section-syntax requirement, the positive-decay rule and the children-only navigation order.

**Verified live on both surfaces.** Kitchen hub appears at Monday 08:30. Front-room hub appears
at Monday 00:30 with `getNpcsAtLocation('the_front_room')` returning `['npc_dean']` — **the
overnight-wrap row holds in live presence, not just in a schedule dump.** That is the first
end-to-end proof of the midnight-wrap finding; until now it had only been read out of the
source and seen in a schedule listing. The late loop applied dean lust 30→38, relation 0→3,
player exposure 40→45, nerve 0→4, pride 100→96. Zero JS errors.

**`meter ceiling` now PASSES.** Exposure gates at 15 (Ray's garage), 35 (Dean's kitchen morning)
and 75 (Dean's locked late rung) fill the bands the gate had been naming as empty promises.
Marek takes 55.

**Gates: 7/10.** Three fails left, and they are three views of one thing — Marek is unbuilt
(standing surface 3/4), his box room is the last empty location (traversal heat 4/8), and
location fill is at 6,697 of ~34,000. Explicit floor holds at 9.9% across 71 beats even as the
denominator triples, which is the floor doing its job rather than drifting.

---

## 2026-08-10 — v0.1 increment 2b: Ray, and the keep. The `need` tier gets an engine

**What.** Added `[settings.rent]` to `0_systems_spec.toml` and Ray's two hubs plus five rungs to
`5_scenes.toml`. Corrected the meter-ceiling gate in `scripts/gates.py`.

**The `need` tier had no engine, and the platform already ships one.** She could earn at the
shop but nothing ever demanded money, so "what she'll trade for" had nothing to bite on.
`[settings.rent]` (`apps/projects/services/template_import.py:2564-2573`) is a first-class
recurring demand with `amount`, `due_day`, `collector_npc`, `grace_periods` and an eviction
mode. It is also **exactly the mechanic the reference game's seed uses** — its `loc-home` file
carries authored `Rent Intro` / `Rent Pay` / `Rent Refuse` / `Rent Fight` passages.

Tuned to bite: **120/week against a shop paying 30/shift** is four shifts — most of her week,
survivable, and one bad week forces the ask. Ray collects, which makes the demand a father
invoicing his stepdaughter, and neither of them has anywhere to put that.

**`eviction_mode = "flag_set"`, not the default `"game_end"`.** A product that never ends must
not ship a lose-state that stops play. **Verified live, end to end:**

| | result |
|---|---|
| pay | money 200 → 80, exactly 120 deducted |
| first miss | `warnings` 0 → 1, grace consumed, authored warning prose |
| second miss | `keep_unpaid` set, soft-eviction prose, **game continues** — still playable, back at `Location_her_room` |

The engine's own fallback line for this mode is *"You're still here. But the terms have
changed."* Zero JS errors.

**Gate corrected — meter ceiling.** Once top bands were correctly left unbounded, the old check
read the *second* band's `max` as the ceiling and produced nonsense ("exposure shown up to 74").
The truer semantic: **every band boundary is a promise** — a meter showing 15/35/55/75 tells the
player something is different at each. The gate now compares the highest authored gate against
the **top band's `min`** and names the empty bands:

> `exposure: bands promise something at 35/55/75, but the highest authored gate is 15`

Vesper unchanged at 1/10 (its `hygiene` finding now reads more clearly for the same reason).

**Gates: 6/10.** `ascent tiers expand the world` now **passes** — all three declared tiers have
gated content for the first time (`nerve` 4+, `exposure` 1+, `need` 4+), which was the design
gap Ray existed to close. `ends on an opening` is up to 2 locked rungs. Remaining: location fill
(5,436 of ~34,000), traversal heat 3/8, standing surface 2/4, and the exposure bands above —
all of which Dean and Marek carry.

**Authorial note recorded rather than ruled on.** Ray's top rung **omits** `locked_text`, so the
greyed row shows the action — *"Ask him for it in front of the others"* — a want the player can
name. Cal's shows the reason instead. Both are in the build deliberately; compare them and pick
one house style before ship.

---

## 2026-08-10 — v0.1 increment 2a: Cal's ladder. 4/8 → 6/10 gates, all ten now judged

**What.** Authored `games/back_home/toml_phases/5_scenes.toml` — the first standing hub and its
full rung ladder (talk → let him look → contact → the explicit loop → a locked top rung).
Merged, built, live-played. Added §13–§15 to `references/engine.md`.

**Cal's ladder verified live.** The hub appears at `the_front_room` only inside his 16:00–19:30
weekday rows (`requires_npc` doing the presence work, no hub schedule needed). At `nerve` 60 /
his `lust` 35 all four rungs render, and clicking *Sit closer* moved **cal lust 35→41,
relation 0→2, player nerve 60→63, exposure 0→2, pride 100→98** — exactly the declared effects,
zero JS errors. The fifth rung rendered as `SPAN.locked-choice`, so gate 9 is real and the
release has a visible door.

**Three engine facts learned, all by breaking something.**

1. **Exit blocks must use SECTION syntax** — `[canvases.nodes.exit_block]` plus
   `[[canvases.nodes.exit_block.choices]]`. A multi-line inline table is a TOML parse error and
   a conditional choice list is unavoidably multi-line. The shipped game does this 199 times; I
   wrote it inline and the merge failed. `conditions = { … items = [ … ] }` *may* span lines
   because newlines are legal inside an array — two levels of nesting is where it breaks.
2. **Third instance of the key-asymmetry trap.** Conditions say `trait_key` / `npc_id`; effects
   say `trait` / `npcId`. Same concept, different key, silent when wrong.
3. **`locked_text` REPLACES the action label**, it does not annotate it. Recorded as an
   authorial trade-off rather than a rule: showing the action names a *want* the player can
   chase, which is what sells the next release; showing the reason is clearer about the gate but
   weaker as a door.

**The meter-ceiling gate caught a real lie.** `nerve` displayed a 75–100 top band while the
highest authored gate was 75 — the top 25 points bought nothing and the sidebar was promising
content that did not exist. Fixed by making the top band **unbounded** (`min = 75`, no `max`) on
all three tiers, which is honest and which the gate correctly skips as promising nothing.

**Gates: 6/10, and no gate is n/a any more** — every one now has something to judge. Passing:
explicit floor 13.2%, explicit in repeatable 100%, media pools, milestones, meter ceiling, ends
on an opening. Remaining four are all unbuilt work: location fill (3,795 of ~34,000 words),
traversal heat 2/8, standing surface 1/4, and `exposure` / `need` have no gated content yet
because Cal's ladder gates only on `nerve`. Ray carries `need`, Dean and Marek carry `exposure`.

**Anchor discipline held without intervention** — `the_front_room` is back to 56% once Cal's
2,125 words landed, against a 25% floor.

---

## 2026-08-10 — v0.1 increment 1: the daily loop and the bathroom. 0/4 → 4/8 gates

**What.** Authored `games/back_home/toml_phases/3_activities.toml` — the solo loop (sleep, wash,
shift, and a pass-time evening) plus the bathroom's triggered layer (occupancy, two peeps, a
walk-in). Merged, built, and live-played the lot.

**Doctrine finding — the build order flips, and this belongs in `references/the-release.md`.**
Gate 2 wants ≥7.5% of beats explicit, but `nerve` / `exposure` / `need` all start at **0**. A
standing seduction ladder at tier 0 is absurd. The reference game resolves this the same way:
its early heat is not chosen by the player at all — her promiscuity sits at zero while the world
still acts on her.

> **The TRIGGERED layer carries the explicit floor while every tier is still cold. The STANDING
> ladder stays cold until she has climbed it.** So the triggered layer is built *first*, not
> third.

**The gate caught the author.** The first draft of the peep and walk-in scenes scored **0.0%**
on the explicit floor *despite being explicit content*, because the prose named the act
obliquely — "hard", "comes", "finishes" — instead of naming bodies. That is precisely the defect
diagnosed in the previous game, reproduced by me, one increment after writing the doctrine
against it.

Rewriting seven beats in a crude register moved the floor **0.0% → 12.0%** and flipped **three
gates** in one pass. The wordlist was **not** loosened to accommodate the prose: "come" would
match "come downstairs" everywhere, so its exclusion is correct and the writing was the thing at
fault.

**Two bugs only live play could find. Neither is visible to any static check.**

1. **Soft-lock.** The opening lands at 17:18; sleep was gated 21:00+; the shift needs the shop;
   and **navigation does not advance the clock**. Every scheduled window in the game was
   unreachable, forever. Fixed with `activity_evening` at the front room (+90 min) — which also
   feeds the anchor's word count — plus widening sleep to 20:00.
2. **Cold start.** Ray and Cal used the bathroom on weekdays only, and the game started Friday
   evening, so the core mechanic was dead until Monday — three in-game days. That was mechanical
   scheduling rather than fiction: people wash at weekends. Added weekend rows (Ray 09:30–10:15,
   Cal 11:00–11:50) and moved the start to Sunday so Monday morning is day 2.

**`npc_at_location` verified end to end.** At Monday 06:48,
`SugarCube.setup.getNpcsAtLocation('the_bathroom')` returns `['npc_ray']`; the landing offers
*"The gap in the door"* only while he is in there; entering applies all four effects
(`nerve` 0→3, `exposure` 6→10, `pride` 100→97, `arousal` 0→20), with zero JS errors.

**Engine fact learned:** a **repeatable** canvas at a location renders as a *clickable action*,
not an auto-fire — auto-fire is for non-repeatable priority canvases. My harness matched the
canvas title in a link and reported the scene as "fired" when it had never been entered. Also
`setup` is not a page global; it is `SugarCube.setup`.

**Gates: 4/8 judged pass (2 n/a), up from 0/4.** Passing: explicit floor 11.5%, explicit in
repeatable 100%, media pools clean, milestones 2/2. Remaining failures are all unbuilt work —
location fill (2,284 of ~36,000 words), traversal heat, standing surfaces, and no locked door
yet. All four land with the hubs in increment 2.

**Running tally of play-test friction:** three wrong selectors, one false-positive "fired"
check, one silent click failure that corrupted a walk, and two engine conventions learned the
hard way. Every one of these is a fact a reusable Player agent would hold and an ad-hoc script
does not. This is the strongest evidence yet for what Part C should build first.

---

## 2026-08-10 — `back_home` builds and plays; four engine facts learned from doing it

**What.** Authored `toml_phases/2_one_shots.toml` (the arrival chain + the first night), merged,
built, and **live-played the result headlessly**. Added §10–§12 to `references/engine.md`.

**It builds and it runs.** `package_from_toml … --gen-version v2 --debug` produces a 908KB
`index.html` with 32 compiled passages. A Playwright walk through the age gate, the four-node
opening and into the bathroom confirms:

- opening chain plays end to end; `arrival_done` set; player lands at `her_room`
- the first-night canvas **auto-fires on entering the bathroom**, correctly gated on
  `arrival_done is_true` + `first_night_done is_false`
- cascade beats advance; `exposure` moves **0 → 6**; `first_night_done` set
- **zero JS errors** throughout

Only warning is 4 uncopied media files — expected, `find-media` has not run.

**Four engine facts learned by doing, now in `engine.md` with citations.** Three of them broke
the build or the test first:

1. **`navigation_order` lists CHILDREN only.** The validator rejects listing the parent. The
   return link is generated from `entry_from` and renders as **`Leave <Location Name>`** — so a
   leaf room with `navigation_order = []` is not a dead end. I diagnosed `her_room` as a dead
   end before looking at the DOM; it was fine.
2. **`trait_decay` values must be positive magnitudes.** `hygiene = -10` is rejected with
   *"must be >= 0"*.
3. **`customizable = true` requires `[[player.customization_fields]]`.** Deferred to `false`
   for v0.1 and logged.
4. **`Start` is an age gate, not the game.** The starting canvas is reached through
   `[[✓ I am 18 or older…]]`, and `player.current_location` is `""` until then. Also: rendered
   links are `a.link-internal` inside `#story` — a bare `text=` selector matches the embedded
   `<tw-passagedata>` source and resolves to an invisible element.

**Process note worth keeping.** Facts 1 and 4 both made me *misdiagnose a working game as
broken*, and I rewrote the play-test selector three times before reading the DOM. That is the
argument for the Player being a **reusable agent with the engine's conventions baked in**
rather than an ad-hoc script rewritten per session — and it is the first concrete piece of
evidence for what Part C should build, produced exactly as intended by using the skill for real
rather than reasoning about it.

**Current state of `back_home`:** 885 words, 10 beats, 2 canvases. Gate 1 reads
`mean 111 · median 0 · anchor the_front_room 53%` — the anchor share is real but everything
else is the expected debt of a world with one scene in it.

---

## 2026-08-10 — first real use: `back_home`, and the scoreboard flattered an empty game

**What.** Ran the skill against a real game for the first time. Authored
`games/back_home/the_want.md`, `toml_phases/0_systems_spec.toml`,
`toml_phases/1_metadata_and_locations.toml` and `v2_state.json` — the Want and the Board for an
incest / female-protagonist premise. Then fixed a bug the run exposed in `scripts/gates.py`.

**The bug.** On a Board with no content authored yet, the scoreboard reported **3 of 10 gates
passing**. All three passed *vacuously*: "0 of 0 milestones open standing content", "0 pooled,
0 fixed single-clip", "0 visible meters rise past their content". An absence is not a pass, and
a stick that flatters an empty world is worse than no stick.

`gate()` now takes three states — `True` / `False` / `None`, where `None` means *there was
nothing to judge*. Those report as `n/a`, are excluded from the tally, and never count as a
pass. Six gates are legitimately n/a at Board stage. The same Board now reads **0/4 judged
gates pass (6 n/a)**, which is the truth.

Vesper is unaffected (it has content everywhere, 0 n/a) and holds at **1/10**.

**What the Board proved works.**
- The merge produced a clean 16,894-byte game from two phase files; `tomli` parses it.
- All 11 schedule rows bound to the correct NPC — no silent re-parenting across the
  `[[npcs]]` / `[[npcs.schedules]]` boundary.
- Dean's `23:00–01:30` row survived as **one row**, confirming the overnight-wrap finding
  rather than relying on it.
- Gate 10 printed `[declared]` and judged `nerve` / `exposure` / `need` **by name**, reading
  `board.ascent_tiers` out of `v2_state.json`. The ledger→gate wiring works end to end.

**Design decisions logged in `v2_state.json`,** with their costs:
- The house is **rooms, not one location** — presence and occupancy are per-location, so
  room-level co-location only exists if rooms are locations. Cost: eight locations to fill.
- `the_landing` exists to be the **vantage** the bathroom is peeped from
  (`npc_at_location`, `generators/v2.py:3480`, `:4131-4146`). It is a corridor and is expected
  to stay thin.
- Anchor is `the_front_room`, not `the_bathroom`. The bathroom generates the most *charged*
  beats but they are short; the front room hosts the evening rotation. Gate 1 also wants an
  anchor the player can re-enter — the measured failure case had a 29% anchor inside a sealed
  room.
- **The rotating lodger** (`npc_marek`, `the_box_room`) is the premise's answer to
  never-ending: a new character at an *existing* location every few releases, which is the
  measured release shape built into the fiction rather than bolted on. He works nights, so he
  is home alone with her while the house is empty — a window no family member competes for.
- Family is written as family and **labelled step-**, per the distribution evidence. Open risk
  recorded: Patreon's own terms are not in our research, and Patreon is the money.

**Engine limit that shaped the cast.** `requires_npc` is a single string
(`apps/projects/services/template_import.py:606`) and portraits render one card per NPC
(`generators/v2.py:4939`), so **two interactive family members cannot share a scene**. Every
scene is her plus exactly one of them; a second body can be narrated in and flag-gated. This is
recorded in the Board file itself so it constrains authoring rather than being rediscovered.

---

## 2026-08-10 — gate 1 was wrong: location fill is a distribution, not a floor

**What.** Replaced gate 1 in `scripts/gates.py` and propagated the correction through
`SKILL.md`, `references/the-board.md`, `references/the-release.md`, `references/state.md` and
`templates/board.toml`.

**The error.** Gate 1 demanded **≥10,000 words in every location**, from a "10,187 words per
location" figure. That figure was computed as *total words ÷ locations* — and the numerator
included `base-combat` and `base-system`, which are engine code, not location prose.

Measured on location prose only, the reference game's seed is **116,540 words across 25
locations: mean 4,661, median 3,154, min 302 (bus station), max 35,218 (school)**. So **24 of
its 25 locations fall under 10,000 words**. The exemplar failed its own derived gate 24 times
out of 25. Its current build still has 23 of 61 locations under 10,000.

**The real shape** is one or two deep **anchors** plus many legitimately thin satellites —
`school` alone held **30.2%** of all location prose at seed. Gate 1 now checks three things:

| check | threshold | seed evidence |
|---|---|---|
| anchor share | ≥25% of location prose in one location | school = 30.2% |
| median location | ≥3,000 words | 3,154 |
| mean location | ≥4,500 words | 4,661 |

plus a report of every declared location with nothing placed in it.

**Discrimination test — the bar set for any format or threshold — passes.** The corrected gate
clears the proven world (30.2% / 3,154 / 4,662) and still condemns the measured failure
(Vesper: median 674, mean 1,466, five empty rooms). A gate that could not separate those two
would be worthless.

**A finding that fell out of it.** Vesper *does* pass the anchor check at 29% — and its anchor
is `captive_room`, the sealed room with no exits that the player can never return to. An
anchor the world cannot reach is not a centre, and `references/the-board.md` now says so.

**Also corrected while propagating:** `v2_state.json` grew `board.ascent_tiers` (a *named*
declaration, which gate 10 now prefers over its top-3 guess) and `board.ceilings`; per-location
`budget` was replaced by an `anchor` flag, since there is no per-room quota any more.

**Honest note on the record.** This is the second threshold in this skill that did not survive
being checked against its own source, and both were caught by re-measuring rather than by
review. The standing rule holds: every number in `gates.py` carries its measurement inline, and
any number that cannot be re-derived from the snapshots on disk does not belong there.

---

## 2026-08-10 — templates, and a doctrine correction the templates forced

**What.** Added `templates/want.md` and `templates/board.toml` — fillable forms rather than
prose to be interpreted. Corrected `references/the-want.md` §3, `references/the-board.md` §3,
and gate 10 in `scripts/gates.py`.

**The correction, and how it was caught.** The plan set a discrimination test for any worked
example: the format must be able to express a *proven* world (Degrees of Lewdity's seed) and
must still condemn a *measured failure* (Vesper). Running the first half of that test against
DoL's actual source refuted our own doctrine.

We had written "**exactly one** global ascent axis" for a female-protagonist game, on the
strength of a secondhand summary. The source says three layers:

| layer | measured in DoL's seed |
|---|---|
| **ratcheting ascent tiers** | promiscuity 22 raises / 1 lower (206 gate sites) · deviancy 20/0 (129) · exhibitionism 12/1 (167) · `purity` counterweight (58) |
| **volatile state** | arousal — 277 sets, 55 increments, 8 decrements; moves both ways constantly |
| **per-character tracks** | robin / whitney / eden each carry love + lust + dom |

The tiers gate at **15 / 35 / 55 / 75** — a four-rung ladder twenty points apart, consistent
across promiscuity and exhibitionism. Doctrine now teaches three or four tiers, each naming a
*different kind* of going-further, because a single undifferentiated meter collapses parallel
ascents into one ladder every player has to climb the same way.

**Gate 10 changed with it,** and this moved the scoreboard: it now judges the top
`ASCENT_TIERS = 3` gated meters rather than one, and it prefers a **declaration** over a
guess — reading `board.ascent_tiers` from `games/<slug>/v2_state.json` when that file exists,
falling back to the top-3 heuristic and labelling the headline `[top-3 guess — no
v2_state.json]` when it does not. Rationale: skills and resources legitimately gate downward
and are not the spine; only the author can say which traits are ascent.

⚠️ **The previous entry's claim that the scoreboard "still reports 2/10" no longer holds.**
Vesper now scores **1/10**: `stealth` (4 expanding / 11 contracting) sits in its top three
gated meters, so the ascent gate fails. That is a real signal — the measured disease of that
game is that survival systems out-gate desire (stealth + weapon + fighting = 90 gate
references against corruption's 66) — but it is a change to the measuring stick and is
recorded as one rather than presented as a constant.

**Template bug caught by its own machine test.** `templates/board.toml` first declared player
traits as a multi-line inline table (`core_traits = { … }` across several lines), which is a
TOML parse error — inline tables cannot span lines. Real games use the `[player.core_traits]`
*section* form, in `1_metadata_and_locations.toml` rather than `0_systems_spec.toml`, because
TOML scoping requires `[[npcs]]`, their schedules and the player traits to share one file. The
template now round-trips: placeholders substituted, `tomli.loads` parses, all seven sections
present, five bands, schedules correctly bound to their NPC.

**Deferred deliberately.** The worked example. Shipping an invented toy world would make the
exemplar a guess, and reconstructing DoL as the exemplar would teach cloning a specific game —
the exact "copy what they ARE instead of understanding what makes them WORK" error this skill
was built to avoid. The first real Board becomes the exemplar instead, written when the
premise is chosen.

---

## 2026-08-10 — the doctrine lands: `SKILL.md` + six references

**What.** The rest of the skill, written on top of the scoreboard: `SKILL.md` (entry point and
dispatcher) plus `references/the-want.md`, `the-board.md`, `the-release.md`, `agents.md`,
`engine.md`, `state.md`. 934 lines of doctrine over 462 lines of script.

**Shape.** The skill authors a **release stream**, not a story. Four phases — `want`, `board`,
`first_release`, `release` — dispatched from `games/<slug>/v2_state.json`. Content is named in
three kinds (STANDING / TRIGGERED / MILESTONE), derived from what the reference game's own
release commits actually do, so the vocabulary owes nothing to the incumbent skill.

**Anti-drift.** The failure this skill is built against is a fantasy spec written once and
never re-opened. Two mechanisms answer it directly: the Want is defined as an *input to every
release* ("a release that cannot name which line of the Want it serves does not ship"), and
`v2_state.json` carries `want.last_read_at_release`, which is behind the current version if
the Want was skipped.

**Verified.**

1. *No invented fields.* All **67** engine keys the doctrine instructs an author to write were
   checked against `games/vesper/toml_phases/7_final_game.toml` — every one occurs in a real
   game. Nothing aspirational shipped.
2. *Gate coverage.* All ten gates have doctrine feeding them. Gates 1, 4, 5, 6, 8 and 10 are
   decidable from the Board alone (so they can be fixed before content is hung on a broken
   frame); gates 2, 3, 7 and 9 are content-level and are fed by the Want and the Release loop.
3. *Scoreboard regression.* `gates.py vesper` still reports **2/10** — the doctrine did not
   move the measuring stick.
4. *Dispatch.* `SKILL.md` registers with an `EXPLICIT-INVOKE ONLY` description naming its
   triggers and explicitly routing plain "start a new game" / "continue writing `<game>`"
   requests to the incumbent, per the `find-media-v3` precedent.

**One correction made to our own record while writing this.** `references/the-board.md`
initially repeated a note from project memory claiming an NPC schedule window cannot cross
midnight and needs two rows. Reading the source refuted it — `setup.isCurrentTimeSlot` in
`generators/v2.py` handles the wrap explicitly (`if (endTotal < startTotal) return currentTotal
>= startTotal || currentTotal < endTotal;`, call sites `:3448`, `:3465`, `:3612`). The Board
and the engine card now state the verified behaviour and flag the contradicting memory for a
live check. This is the reason `engine.md` requires a `file:line` on every claim, and why it
keeps an explicit "unverified — do not cite until read" list at the bottom.

**Open.** No game has been built with this yet. The TOML layout question was settled by keeping
v1's `toml_phases/` convention, since changing it is engine surgery on
`scripts/merge_toml_phases.py` and does not advance the doctrine.

---

## 2026-08-10 — `scripts/gates.py` created (the scoreboard, built before any doctrine)

**What.** First file of the v2 skill: a ten-gate measuring script that scores a built game's
merged TOML. Run as `python3 scripts/gates.py <game-slug>` or against an explicit `.toml`
path; `--json` for machine output; exit code 0 only when every gate passes.

**Why first.** Build order is deliberate — the measuring stick exists before the doctrine so
the doctrine cannot quietly drift off it. Every threshold traces to a primary measurement
rather than to inherited opinion, and the header of the script carries the evidence inline.

**Where the numbers come from.** Ten snapshots of Degrees of Lewdity's own source, fetched
from `gitgud.io/Vrelnir/degrees-of-lewdity` (project id 8430) and measured on one frozen
instrument, spanning its earliest retrievable build (root commit `ef4a8067102a`, "Initial
import (v0.1.20.2)", 2018-11-28) to `0.5.11.9` (2026-07-28) — 25 to 61 locations, 1,772 to
15,629 units, 254,674 to 2,235,775 words.

- `WORDS_PER_LOCATION = 10_000` — DoL's thinnest year ever (10,187). Its words-per-location
  rose monotonically for eight straight years to 36,652; it never opens a place faster than
  it fills it.
- `EXPLICIT_BEAT_FLOOR = 7.5` — share of beats carrying 3+ explicit words held at 7.5–9.3%
  across eight years and 12x growth. Raw sex-word share is *not* usable (it fell 3.00% to
  0.96% as systems and UI outgrew prose); the beat ratio is the stable one, and it is robust
  to word-list choice.
- `EXPLICIT_IN_REPEATABLE = 50.0` — from the measured failure case: 95% of Vesper's explicit
  beats sit in a sealed room with no exits while all nine of its repeatable sex loops score
  zero.
- `LOCATIONS_WITH_HEAT = 60.0` — deliberately not 100%. DoL's seed had sexual passages in 17
  of 25 locations (68%); a police station is allowed to be cold.

**Verified.** Run against `games/vesper`: **2 of 10 gates pass**. Four correctness bugs were
found and fixed during that run, each by reading the source rather than assuming:

1. `is_repeatable` defaults to **true** when the key is absent — confirmed firsthand at
   `generators/v2.py:10937`, `generators/v2.py:11010`, and `apps/stories/models.py:355`. An
   earlier grep-based pass that assumed otherwise reported 33% repeatable when the majority
   is repeatable; the script parses TOML and never greps.
2. An **effect** names its trait `trait`, while a **condition** names it `trait_key`. Reading
   only `trait_key` silently missed every trait write in the game and produced false
   "opens nothing" findings on the trait-sequenced `salvage_session_*` chain.
3. Meter ceilings live in `sidebar_items[].bands[]`, not in `player.core_traits` (which is a
   flat `{key: initial}` map). A top band with no `max` is unbounded by design and is skipped
   rather than guessed at.
4. Three gates were stricter than the evidence and were relaxed to match it: traversal heat
   (to 60%), milestone payoff (made transitive, since an opening funnel legitimately runs
   one-shot to one-shot and only the end of the chain must land on standing content, and with
   random ambients and self-guard canvases excluded), and meter direction (judged on the
   single most-gated meter, because a female-protagonist game runs one ascent axis while
   skills and resources legitimately gate downward).

**Not yet present.** No `SKILL.md`, so the skill does not register or trigger — correct for
now, as it is not ready to be invoked. The description will carry `EXPLICIT-INVOKE ONLY` when
it lands, following the `find-media-v3` precedent, and the incumbent `author-game` skill keeps
every ordinary request until v2 is promoted.
