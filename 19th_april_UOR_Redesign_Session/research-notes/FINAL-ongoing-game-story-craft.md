# Writing Story for Ongoing Games — A Craft Reference

*Research synthesis, 2026-04-21. Six parallel investigation tasks (serialized narrative + slice-of-life / life-sim game design / emergent narrative + pacing / interactive fiction craft / adult-transformation-game craft / variant-prose techniques), ~124 sources, ~180 techniques distilled. Citation format: [T#] = task-letter + finding-number; full registry at end.*

---

## 1. What "story" means when the game doesn't end

Ongoing games fail as stories in three specific ways, and good ones are designed against all three at once.

**Failure 1 — trajectory fails.** The story the designer wrote heads somewhere. The player reaches it, or doesn't. If they reach it, the ongoing game is now ended in everything but the UI. If they don't, they drop. This is why "VN with chores" patterns rot around hour 10.

**Failure 2 — the premise exhausts.** Everything interesting about the setup happens in Act I. The middle becomes maintenance. Naoki Yoshida on running FFXIV: "The same cycle repeating itself brings about both predictability and boredom... stability creates a sense of security but there is a very fine line between that and boredom" [C.B8].

**Failure 3 — the stat-grind feel.** Every interaction is legible to the player as "which meter this ticks." The UI swallows the fiction. Emily Short's rule: *"the character trait system may have been doing important things, but it was opaque enough that eventually I started to ignore it"* [E19]. The mirror failure — transparent enough that the fiction disappears — is just as common.

The working definition that runs through every serious designer in this research — Alexis Kennedy, Emily Short, Vince Gilligan, Tynan Sylvester, George Saunders, Vrelnir, Meg Jayanth, Greg Kasavin — is this: **story in an ongoing work is a line pulled through every scene plus a shape the player cannot exhaust.** The line is character. The shape is a system of overlapping horizons and renewing questions. Neither works alone. A line without a shape is a novel that should have ended; a shape without a line is a simulation.

This document is about how those two things are built inside a game where the player keeps coming back.

---

## 2. Nested horizons — the macro architecture that doesn't collapse

Jesse Schell's "interest curve" in *The Art of Game Design* is usually taught as a single rise-and-climax. The important part of Schell's formulation is the word that usually gets skipped: **fractal**. There is a curve at every scale, and they nest [C.B1].

For an ongoing game, the nested-horizon stack is the spine:

| Horizon | Duration | What closes at this horizon | Example |
|---|---|---|---|
| **Beat** | 30s–3min | one exchange, one choice | "I told the trucker to keep the change" |
| **Scene** | 5–15min | one micronarrative | "I finished a Tuesday shift" |
| **Session** | 30–90min | an in-game day or two | "I paid this week's rent with enough left over to matter" |
| **Chapter** | 3–10 sessions | a mid-term question | "Will I ever feel safe in this house?" |
| **Act** | 10–30 sessions | a lifestyle shift | "I'm no longer the girl who arrived" |
| **Lifetime** | open | identity transformation | the character's accumulated self |

Two rules drop out of the stack, and they are the entire discipline:

1. **Every horizon must open, escalate, and close inside itself.** Saunders' two-part move applies at every scale: an expectation is created, the expectation is honored or complicated [A29]. A beat that only opens and a scene that only teases are both pacing faults.
2. **The horizons are offset — always at least one rising, always at least one at closure.** This is the soap opera's 50-year answer. Irna Phillips' rule, carried into Agnes Nixon and Harding Lemay: *when you're in Act 3 of arc 1, you're in Act 2 of arc 2 and Act 1 of arc 3* [A7]. No storyline is ever alone on the field. The day the player closes a chapter is the same day another chapter is cresting and a third is starting to creak open.

Applied: before any canvas authoring, decide which horizon each scene serves, and stagger them. A week of play should close one or two beats every session, close a scene every session or two, close a chapter every 4–6 sessions, and keep exactly one chapter and one act rising.

---

## 3. The renewing question — structure without a climax

The single technique that makes a soap opera run for five decades without collapsing is this: *never let all active dramatic questions resolve in the same episode* [C.B2]. Studies of Nixon's *All My Children* and Harding Lemay's *Another World* describe the mechanic plainly: as Question A approaches resolution, Question B is spawned at lower intensity; A's closing scene plants B's inciting detail [A15][C25]. The show never exits a mid-something state.

Two game-design primitives implement this:

**The progress stat + menace stat pair.** Emily Short's storylet pacing architecture [C.B4][D.5]. Progress tracks the main plot forward (Act I / II / III gates). Menace tracks jeopardy; when it saturates, a menace-wheel fires — a cluster of recovery storylets thematically tied to the menace type [C.B6]. Fallen London ships four menaces at once (Nightmares, Suspicion, Wounds, Scandal), each with its own saturation threshold and its own penalty-zone storylet pool [C.B6]. The design effect: a player who pushes hard in any direction automatically gets a change-of-scene storylet cluster for free. Pacing, worldbuilding, and mechanics in one.

**Emergence detection.** Henrik Fåhraeus's CK2 design principle [C.A4]: the engine scans the event log after each tick for accidental pattern — two unrelated chains colliding on the same character, a flag combination that resembles a known trope — and rewrites the surface text and music of the next event to echo the pattern. Players perceive it as authored fate. Fåhraeus: *"Humans are good at seeing patterns in time [and] have a tendency to put meaning where there is none"* [C.A4]. Applied in a smaller game: after any random event is selected, run one pass that checks whether recent events share a theme (same NPC, same location, same flag family) and rewrite two lines of the surface prose to acknowledge it. Cheap at runtime, enormous perceived coherence.

Rule: **do not ship a state in which the player has no active dramatic question at any horizon.** Spawn the next before closing the last.

---

## 4. The atomic unit — storylets and resource narrative

The shape that makes "ongoing" tractable is the storylet. Emily Short's three-part canonical definition: *content + prerequisites + effects* [B1][D.4]. A line, a condition that gates it, and a mutation that fires when it plays. Everything else — heart events, Confidant scenes, Destiny seasonal beats, cards, vignettes — is this triad under different names.

Short's 2016 taxonomy splits storylet selection three ways [D.1]. For an ongoing authored game, the idiomatic combination is:

- **Quality-Based (QBN) for the main arc.** Player sees eligible storylets, picks from the menu. Adding content later is cheap because the contract is the quality variable, not the graph. This is how Fallen London still ships new content fifteen years in [C.B3].
- **Salience-Based for ambient texture.** Engine picks, player doesn't. Stardew villager barks, L4D Director callouts, Firewatch object-reactivity. Good for reactive emotional overlays; risky for dramatic arcs because salience ≠ pacing.
- **Waypoint for arc closure.** The engine pathfinds the conversation or the story back toward authored trigger-beats. Used by *Glass* (Short) and implicitly by any story that must close cleanly despite player drift.

Alexis Kennedy retracted the QBN name in 2020 and replaced it with **resource narrative** [B3]. The complaint: "quality" collapsed three different things — inventory resources (bottles of laudanum), character traits (Dangerous 4), and story flags (met the Vake). They behave differently: resources drain and replenish, traits grow and plateau, flags never go away. Kennedy's rule is that *drama emerges from the interaction of differentiated resource types.* Sunless Sea runs on the Terror–Fuel–Supplies triangle; Cultist Simulator on its temperate/desire/despair columns; XCOM and Darkest Dungeon on analogous shapes. The designer doesn't *write* the drama; the *ratios* do.

Applied concretely: don't design a unified "affection" stat. Design three: a reputation that drains passively (decays per day of absence), a trust that plateaus (earned slowly, forgotten slowly), and a set of story flags that never reverse. Write storylets eligible on ratios between these, not on thresholds of one.

**Anti-pattern to avoid: time caves.** Short's term [B7][D.1]. A purely branching structure where every storylet depends on the exact path taken. Negates the extensibility that makes storylets useful in the first place. Most student Twines are time caves.

---

## 5. Character arc without a finale

The three questions every long-form character arc has to answer:

**A. What's the single sentence?** Vince Gilligan's *Breaking Bad* compression — *"Mr. Chips into Scarface"* [A6]. Every season, every episode, every scene must measurably advance the character along that vector. Peter Gould's *Better Call Saul* refinement asks it differently: *"what problem does becoming Saul solve?"* — framing the destination as the answer to a pressure already inside the character rather than a drift [A44]. Either phrasing works; the compression itself is the discipline. If you can't state your protagonist's arc in one testable sentence, the scenes will wander.

**B. Where does the engine sit inside the character?** Matthew Weiner's *Mad Men* rule: *all major transformations begin in shame, because poverty feels shameful* [A13]. Shame is the engine; ambition is the surface expression. For a young-woman-on-an-economic-edge arc like The Long Summer, the test is whether the protagonist's specific shame is identifiable (failed first adulthood, a breakup that wasn't mutual, the humiliation of being the charity case) and whether every corruption-drift choice can be traced back to it. A corruption arc without shame underneath is a shopping list.

**C. How does the player see the change?** This is the hardest question. Two bad answers: show a bar going up (the stat-grind failure), or stage an "awakening scene" (melodrama). One good answer: **distributed self-recognition.**

Vrelnir's *Degrees of Lewdity* does this via its Traits and Current Condition systems [E27][E28]. Traits are acquired silently through repeated matching acts; once held, they change flavor text across the whole game, not only in trigger scenes. The protagonist starts being *described* differently — the descriptive strings the game uses for her shift over weeks as the cumulative profile crosses thresholds. The "I've changed" moment isn't a cutscene; it's the slow realization, noticed weeks later and in passing, that the text has been calling her someone different for a while now.

The same pattern recurs in *Course of Temptation* via NPC memory and rumor [E7]: the protagonist's corruption becomes externalized as *the town's gossip about her*, which then gates future events. In *Hades*, Greg Kasavin's rule is simpler: *when a flag changes, at least one NPC should have a line that notices* [F.DR3]. Not all NPCs — just one, for specificity. Relational acknowledgement scales better than event scripting.

Rule: **the recognition is not a beat. It is a weather system that moves through the prose.**

One more craft lever on the arc question: Saunders' "refuse to repeat beats" [A30]. *"Once a story has moved forward, through some fundamental change in a character's condition, we don't get to enact that change again."* Each emotional beat is one-shot. Applied to ongoing authored content: if a scene's payload has already fired in an earlier scene, either cut it or escalate past the previous peak. This is the scene-level escalation test the macro-arc tools lack.

---

## 6. NPCs that aren't vending machines

Meg Jayanth's GDC 2016 formulation is the cleanest statement of the problem: NPCs with agency are not a politeness. They are a structural primitive [D.18][D.19][D.20].

Three applied techniques:

**Refusal as first-class.** Jayanth's *80 Days*: the Murri girl refuses Passepartout's help because he is aligned with her oppressor. The refusal is the scene. Build situations where the protagonist's privilege, role, or reputation is a *barrier* not an asset. Rejection (in the TOML sense — `rejection_node` and `rejection_effects`) is a characterization device, not a dead-end. A declined choice should fire a beat of its own; what the NPC says *when turning the protagonist down* is often the best information the player will get about them.

**Contradiction as worldbuilding.** Jayanth again: *"Almost every NPC has a slightly different opinion of the Artificers' Guild"* [D.19]. Don't write a bible. Let the NPCs disagree. The world's reality is the *envelope* of what the NPCs can't agree on. For The Long Summer, this means Frank and Ryan and Jake don't hold a consistent family line about Mom's absence; each of them is edited by their own history with her. What the protagonist pieces together across ten conversations is the truth; no single NPC knows it.

**Typed social memory.** Richard Evans and Emily Short's Versu design [D.11][D.12]. NPCs don't remember events generically; they remember *typed social moves* — `insulted_by(player) = true`, `flirted_with_by(player) = true`, `confided_in_by(player) = true`. Every future dialogue line gates on the typed memory, not on an event log. This is what makes social coherence tractable — you can write "Frank's reaction when he's been confided in vs. when he's been flirted with vs. when he's been insulted" as three dialogue pools, and the flags do the rest. For Twine-side engines without a Versu model, the pattern is still achievable: per-NPC flag names that describe the *type* of interaction, not the scene.

Supporting techniques to stack on top:

- **Avellone's companion checklist** [D.13]: combat-viable, thematically resonant, ego-stroking (barks and reactivity), distinct voice and look, environmental comments, mechanical niche. Miss any and players drop them.
- **Mitsoda's invisible-stats rule** [D.15]: no friend-o-meter. The dialogue itself is the number. The NPC's tone tells the player where the relationship sits. Internal flags drive mood columns; the flag itself is never shown.
- **Mitsoda's background column** [D.17]: in *Bloodlines*, the Malkavian playthrough is a column in the same dialogue tool — every line has a Malkavian variant. Treat protagonist background not as a different script but as a *view* on the shared one.
- **Hades' domain-gated commentary** [F.DR3]: Dionysus comments on alcohol; Ares on violence; each NPC has a narrow lane of salience. This prevents the "everyone notices everything" failure and keeps voices distinct across thousands of lines.
- **Autonomous micro-desires.** Will Wright's *Sims* lesson [C.A7]: give NPCs autonomous small wants that fire on independent schedules. Most of the time nothing happens. Occasionally a desire collides with the protagonist's active plan and produces the emergent "my NPCs have minds of their own" feeling. In authored ongoing games this is cheap: each NPC gets 2–3 "they want X tonight" triggers that randomly surface when the player's path intersects.

---

## 7. The accumulation toolkit — same scene, different week

This is the single largest gap between "VN with a clock" and "game that feels like a world." The question is: how do you write a scene that repeats fifty times and reads differently every time?

The answer comes out of six traditions at once, and they stack.

**Chekhov's "The Darling" (the noticed-detail inventory shift).** Saunders' deconstruction [A32][F.23][F.DR5]: Olenka's house is described four times across four husbands. The *house* does not change. The *inventory of objects the narrator mentions first* shifts to match each husband's world. Theater posters and greasepaint for the theater manager; account books and pine resin for the timber merchant; iodine and bridles for the veterinarian. Chekhov never writes "she was adopting his worldview." He writes what she now notices.

Translate directly to a diner scene across a corruption arc:

- Week 1 (tentative): the bell above the door, the laminated menu, her name tag
- Week 3 (entangled): the specific booth, the second cigarette, the ashtray refill, the older waitress's pace
- Week 6 (complicit): the rear exit, the till's drawer sticking, who sits by the window, what Marge doesn't look at

Same diner. The diner was never going to change. The prose pulls from different detail inventories per arc stage.

**Munro's free-indirect style (and the deletion of "she noticed").** Causeway Lit's craft analysis [F.25]: "She noticed her mother was angry" is one verb away from "Her mother was angry." The second is stronger because the narrator is already inside the character. For repeatable scenes: don't write "Maya sees the ashtray now." Write "The ashtray sits between them. Full." The reader registers the noticing without being told. A game's ambient prose should almost never use *notice*, *realize*, *see* as the main verb for the protagonist's perception — the selection of detail *is* the perception.

**Ink's sequence-and-condition stack (the engine move).** Inkle's Ink language gives four operators that handle most of this heavy lifting without custom scripting [F.10][F.11][F.12]. Inside a single passage source:

```
You enter the diner. {The bell still sticks. | The bell sticks, as always. | You don't hear the bell anymore.}
{week >= 3: Marge is at the counter, not looking up. | Marge looks up.}
{&The fluorescent above booth three flickers.|The rain on the window.|The smell of burnt coffee.|The clatter of someone's plate hitting tile.}
```

Three mechanics in one passage: a three-element stopping sequence that permanently hardens at visit 3 ("you don't hear the bell anymore"); a hard state gate on week count; a cycling pool of ambient details. Every variant is inside one passage source. For a generator like UOR's that doesn't use Ink natively but does use group blocks with conditions, the pattern translates directly: the arc-stage gate belongs *inside* the passage, not as a passage copy.

**Valve's Response System (the specificity-tier move).** Elan Ruskin's GDC 2012 architecture [F.5][F.6][F.DR2]. Every bark is stored as `rule + criteria + response`. When a trigger fires, the engine picks *the rule with the most matched criteria*. Writers author at tiers: generic wounded bark; wounded-by-hunter bark; wounded-by-hunter-on-this-map bark; wounded-by-hunter-on-this-map-with-teammate-down bark. **The player's experience automatically upgrades as specificity grows.** Shipping discipline: write the generic first, ship it, then add more-tagged variants over time.

**Stardew's heart-event trigger grid (the overlap move).** The "alive" feeling comes from many overlapping tables, not one script [B14][B15]. An event fires when `heart_level ≥ N` AND `location matches` AND `time-of-day matches` AND (often) `weather matches` AND prior events have/haven't fired. Crucially, the *default* conversational dialogue pool rotates every two hearts as well — the player doesn't always see a scripted scene; they see Sebastian stop being terse in spring, then mention his sister the week after. Progress is felt through ambient text change, not only scripted cutscenes.

**Hades' barks architecture (the scale move).** Kasavin's system [F.7][F.8][F.9]: 21,000 voice lines in Hades 1, ~30,000 in Hades 2, most tied to context slots — current weapon, current boon, run number, last boss, last death type, last gift given, who you've met with whom in what order. Writers author *to slots*, not scenes. The same "talk to god in lounge" scene produces a fresh line for 50+ hours because slot coverage scales by multiplication.

**Subcutanean's narrator-trait axis (the consistency move).** Aaron Reed's quantum-text book [F.18][F.19][F.DR4]. Three axes — laconic↔voluble, optimist↔pessimist, slang↔formal — fixed at generation time, running consistently through the whole book. Named variables tied to the axis plus hundreds of anonymous micro-swaps produce 209–239-page books from one source, each reading coherently as one voice. Applied to an arc: *the character arc stage is itself a narrator-trait axis.* Week 1 Maya = hopeful/polite; Week 5 Maya = tired/curt. The same scene gets different variant-insertions because the narrator-trait has moved along the axis.

The six techniques, ranked by effort-to-payoff for a Twine-style generator [F ranked list]:

1. **Ink-style stopping sequences inside the passage.** Highest payoff. A cycle on ambient detail makes every revisit feel fresh with zero state tracking.
2. **State-gated inline variants.** Arc-stage gate inside the passage, not as a passage copy.
3. **Narrator-trait axis.** Pick 1–2 axes (hopeful↔worn, polite↔curt) that move with arc stage; tag prose inserts by axis.
4. **Noticed-detail inventory shift (Chekhov/Darling).** Per stage, curate which objects the passage mentions first. Don't rewrite the room — rewrite attention.
5. **Domain-gated NPC barks.** One NPC per salient domain; they only bark when something in their lane changes.
6. **Specificity tiers + fallback.** Write the generic first. Ship it. Add more-tagged variants opportunistically.

**Authoring budgets observed in the field** [F]: Failbetter's hard word caps — roots ≤30 words, branches ≤20, results ≤100, tools go red past 100 [F.2]. 80 Days shows ~5 fragments per city out of a much larger pool per city and per route. Hades: ~500 lines per major NPC. Subcutanean: hundreds of micro-variables plus a handful of named narrator traits. The common lesson: **the budget forbids throat-clearing.** A scene that recurs 50 times has to land in one breath.

---

## 8. Pacing without a climax

A paused narrative exhausts. A monotonically rising narrative exhausts faster. What doesn't exhaust is a **sine wave with enforced recovery.**

Five techniques from five different traditions that all implement this:

**Left 4 Dead's named phases.** Mike Booth's Director paper [C.A3]: Build Up → Peak → Relax, with stop conditions. During Relax, zombies literally stop spawning — a hard-enforced quiet window where the player's nervous system can down-regulate. Peak and Relax are not emergent accidents; they are server-enforced. Translate: every authored scene sequence needs a **relax token** — a passage of guaranteed mechanical quiet where the player reads flavor, tidies inventory, and comes down before the next push. Skipping the relax token is how VN pacing feels exhausting even when individual scenes are good.

**RimWorld's Cassandra storyteller.** Tynan Sylvester's design [C.A1][C.27]: events map to an Aristotelian curve that resets after each climax, and threat rolls are *damped* for a fixed window after a peak. Phoebe Chillax simply lengthens the damping windows. The important craft detail: storyteller choice is presented to the player at game start as **a pacing preference, not a difficulty** — "how do you want your story told?" is the first UX question. That framing alone would reshape most ongoing-game onboarding.

**Wealth-linked escalation.** RimWorld again [C.A2]: incoming threat scales with *accumulated colony wealth*, not elapsed time. Prosperity is the punishment multiplier. **The game feels emergent because consequences look causal** — you got rich, therefore raiders. Applied to an authored ongoing game: gate the scripted Mob Boss scene (or its equivalent) on player-earned state — reputation, hoard, exposure. The player's own choices drive the slope of the curve, which is the cheapest-feeling source of perceived agency.

**Fallen London's action economy + menaces.** Failbetter's pacing mechanism is time-gated actions (20 at a time, refilling one per 10 minutes) plus the menace system where any high-intensity storylet raises a Nightmares/Suspicion/Wounds/Scandal counter; at saturation the player is forcibly relocated to a penalty zone with its own storylet pool [C.B6]. The game paces itself. The player cannot burn out. For an authored game that doesn't want real-time gating, the menace half alone is enough: **high-drama scenes automatically schedule mandatory cool-down scenes.** Intensity-debt, tracked and forgiven over time, is the honest analog of the Left 4 Dead Director.

**Short's alternating freedom and constraint.** Her 2020 pacing essay [D.7][D.8][D.9][C.B4]. Open, freeform sections *feel less* intense — use them for exploration, relationship accrual, ambient grind. Narrow, linear sections *feel more* intense — reserve them for climactic moments. Interrupt long freeform runs with a mandatory story-specific storylet to remind the player the story is moving. **Cost-as-deceleration:** put resource requirements at the *start* of a storyline, not the end — the player has to leave to gather, which paces the narrative without the author writing filler. **Rhombus acceleration:** before a climax, squeeze the choice set down to linear minimal-choice — "wide → narrow → point" creates felt acceleration.

**Martin's visible-budget-at-day-start.** *Citizen Sleeper* rolls all dice at wake-up and displays them as slots [B11][B12]. The player sees their capacity *before* deciding. Hidden RNG feels unfair; visible RNG feels strategic; visible RNG with named stakes feels story-shaped. Clocks layer over this: every Drive has 2–5 visible clocks ticking at different rates. The player reads the whole day as a constrained allocation problem where the constraints *are* the story. The writing just has to name the clocks well. The transferable rule is short: **if you want a mechanic to feel weighty, let the player see the budget before they spend it.**

**Yoshida's "predictable rhythm + planted surprises."** FFXIV's long-game philosophy [C.B8]: stable structural cadence — weekly frame, monthly arc close, seasonal act break — with 1–2 unannounced beats per cycle that break pattern. Players learn the rhythm, relax into it, and the surprises hit harder because the baseline is flat. **The predictability earns the surprise.** Rigid cadence works for communal pacing but hurts solo pacing — Destiny 2's pivot away from weekly drip after a decade confirms this [C.B7]. For a single-player ongoing game, the internal act structure should make each chapter end cleanly whether played in one night or one month.

---

## 9. Loading the ordinary moment — slice-of-life craft for games

The diner shift problem. A five-hour shift; the protagonist clears tables, serves regulars, closes out. Nothing "happens." Chekhov, Munro, Carver, and Trevor spent their careers on this exact problem in prose. The techniques port.

**Trevor's art of the glimpse.** *"The short story is an impressionist painting… concerned with the total exclusion of meaninglessness"* [A36]. Every sentence either lands a truth or gets cut. In a repeating game scene, there is no filler tier. If a line doesn't either (a) advance a detail inventory that will change later, (b) land an NPC tell, or (c) move an internal stance — cut it. This is why Failbetter's 30-word root budget works: the constraint forces the glimpse.

**Baxter's luminous specific detail.** *"A novel is not a summary of its plot but a collection of instances, of luminous specific details that take us in the direction of the unsaid and unseen"* [A38]. Subtext is what the scene *refuses* to name. A scene with subtext you want to preserve must include a detail that *points at* the unsaid without saying it. For Maya's first diner shift: not "she felt nervous." A thumb finding a loose thread on her apron, once.

**Saunders' "but" joint.** *"The fundamental unit of storytelling is a two-part move. First the writer creates an expectation… Second, the writer responds to (or 'uses' or 'exploits' or 'honors') that set of expectations"* [A29][A31]. Every scene's engine is *"X, but then..."*. A scene without an implicit but is exposition. Test: name the expectation the previous beat created; the next beat must confirm, deny, or complicate it. A diner shift scene opens with *she is going to clear table 4* and its but is *the older woman is watching*; or opens with *she is going to make her money* and its but is *the tip on table 6 is a folded number, not a bill*.

**Weiner's hold-the-take.** On-set rule from Mad Men [A15]: don't cut away on a speech; hold on the actor before and after. In prose, translate as a beat of physical description inserted between dialogue lines instead of a reaction cue. *"Well," Frank said. She watched the ice move in his glass. "About the rent."* The pause is where the reader reads the subtext.

**Weiner's withholding-by-body.** *"A 1960s sensibility where people didn't think it was polite to talk about themselves"* [A14]. Interior state is shown through action and body, not dialogue about feelings. In a life-sim where the protagonist can't soliloquize freely, this is the house style by default — the only question is whether the writer honors it. Every time the protagonist catches herself wanting to explain herself, convert the explanation to a gesture or an object.

**KRZ's non-mechanical dialogue.** Cardboard Computer's rule [B26][B27]: dialogue options rarely change events. Instead they change *who is speaking this line, about what, in what register.* Choice as stage direction, not decision. *"You are not choosing what the character does — you are choosing what kind of story this is."* For an ongoing game, this is the answer to "the protagonist has to say something about the weather on table 4, but none of the options matter mechanically" — the options don't have to matter *mechanically*; they have to let the player speak as her.

A working template for one diner-shift scene, assembled from the above:

- **One expectation planted in the first paragraph** (she'll hit her tip goal tonight).
- **One luminous detail that carries subtext** (the apron thread, the wrong-size ring on the cook's finger, the radio station that keeps skipping).
- **One "but"** (Marge cancels the side work she'd promised; or: the trucker asks her name).
- **One hold-the-take** (a two-sentence pause of physical description before the protagonist responds).
- **One refusal** that means something (Maya declines the extra shift, or doesn't).
- **One detail that will mean something different in five weeks** (the booth she's assigned, the door that sticks, the regular who sits alone).

Nothing has happened. The shift was just a shift. But the scene is doing the work a Chekhov story does in three pages.

---

## 10. Corruption and transformation — shape, not magnitude

This is the subgenre-specific section. The strongest single craft rule that recurs across every serious adult-transformation game in the research is: **don't let the corruption arc be one number going up.** Every major design statement — Vrelnir's DoL, Vren's Lab Rats 2, Anthaum's Course of Temptation, Majalis's Tales of Androgyny — points at the same thing: corruption is a *shape*, not a magnitude, and the shape is what makes the transformation feel like a story instead of a spreadsheet [E synthesis].

Five applied techniques from the subgenre's actual craft discourse:

**Control vs. Trauma (Vrelnir, DoL).** Corruption isn't a virtue meter. Trauma accrues through non-consensual acts; Control is restored through *transgressive acts the PC performs voluntarily.* Vrelnir: *"High trauma can be managed as long as the PC has a sense of control. The main way to restore control is to push the boundaries of the PC's inhibitions, performing acts they feel are transgressive"* [E1]. The design consequence is that the protagonist's self-authored slide is how she climbs out of trauma. Narrative and mechanics agree that corruption is an agency-restoration strategy, not a passive drift. This is a profoundly different shape from the "virtue ratchet" that most transformation games implement. It is also truer to how the real psychological pattern works.

**The Awareness layer — mechanics narrate themselves twice (DoL).** Every action has a mechanical resolution *and* an Awareness-gated narrative resolution [E2]. Low Awareness (0/7) narrates lewd events as accidents, confusions, things happening to someone else. High Awareness (7/7) narrates the same event with full recognition. Promiscuity gain can be suppressed or allowed by Awareness, because *"you wouldn't necessarily view something as lewd"* without the perception to frame it that way. Design consequence: one event with Awareness-conditional text handles the whole arc. Writers don't need five tiers of the same scene.

**Multiple parallel axes, not one (DoL's lewdity triad).** Promiscuity / Exhibitionism / Deviancy as three separate counters, each with its own unlock tiers [E3]. A character can be a deep exhibitionist with shallow promiscuity, or the opposite. The transformation has a *shape* — a profile — instead of a magnitude. This is Kennedy's resource-narrative advice [B3] applied to the specific corruption domain: drama comes from the interaction between the axes, not from any axis alone.

**Intersecting loops (Lab Rats 2).** Vren names three [E4]: a business loop (serums → sell → reinvest), a corruption loop (NPC-state change, made to stick), and a research loop (unlock new traits). Interesting play happens *at the intersections* — the research-loop tier gates the corruption-loop velocity; corruption unlocks business roles. **Craft lesson: never collapse to a single loop; the pacing comes from which loop the player prioritizes this session.** For The Long Summer, the analogues are obvious: the economic loop, the relational loop, and the self-reinvention loop each have their own tempo and their own reward schedule. The week where the player pushes economic hard and pays no relational attention has a different story than the reverse.

**Asymmetric consent (Vrelnir).** *"The lack of consent on the part of PC is important, and the player is affected by that. They consent to play the game, but not necessarily to every little annoyance"* [E15]. The player's genre-level consent is explicitly separated from the protagonist's scene-level consent. This is the design justification for writing coercive scenes as story rather than puppet-show — the player's awareness of the split is what makes the coercion legible as fiction. Nguyen and Ruberg's CHI 2020 paper [E17] formalizes this: consent should be continuously negotiable, mid-scene modification should be mechanically possible (safewords), and boundary-holding belongs to the party whose boundary it is. The practical application: every intimate scene has a mid-scene exit that costs the protagonist something but lets her out; the protagonist's *willingness* modifies which resolutions surface; the mechanic does the consent work, not the prose.

**Distributed self-recognition (DoL Traits, Course of Temptation rumors, Hades barks).** The "I've changed" moment is not staged anywhere [E27][E28][E7]. DoL Traits change the prose *across the game*, not in their trigger scenes; Current Condition and Attitudes descriptive strings update based on cumulative profile. CoT externalizes corruption as gossip: the PC's transformation becomes *the town's talk about her* which then gates future events. The self-recognition runs across dozens of scenes where the prose has been describing a different person for a while now. This is the single most underused technique in the subgenre — most games still script an "awakening scene" that lands flatter than the distributed recognition would have.

One further pacing note specific to this subgenre: **place the first intimate or charged event early, not gated behind grind** [E14]. DoL's first charged encounters can fire within the first in-game week via ambient street events. Stat-gated first intimacies create a grind feeling; ambient-incident first intimacies create a world feeling. The *second* event is where the weight lands, because the first has already taught the player what this world includes.

---

## 11. Production discipline — writing an ongoing game without collapsing

Any serial dies from production friction before it dies from lack of ideas. Wildbow, who writes million-word serials, is explicit: *the primary killer of serials is real-life friction, not creative exhaustion* [A.DR1]. The techniques below are about not dying.

**The buffer.** Wildbow's rule: pre-write 12–16 chapters before going public, and maintain a rolling buffer of ~12 while writing current [A20][A23]. Fully pre-written serials feel parceled out — they lose pulse. Fully organic serials gain pulse but collapse under any life disruption. The rolling buffer is the honest middle. For an ongoing game: ship the first chapter only after the fifth is drafted.

**Cadence calibrates cliffhanger.** High frequency needs softer cliffhangers; low frequency can (and should) carry harder ones [A21]. Mismatched pacing fragments the story. Monthly cadence is a readership-killer floor — readers forget you exist [A22]. Applied to update schedules: pick the cadence first, then match the beat intensity to it.

**Voice anchor.** Wildbow again: *"remind yourself why you're writing the story, what you like about it"* — schedule this as a ritual, not as a response to crisis [A24]. Weiner has his own version: he re-reads John Cheever's Collected Stories preface at the top of every Mad Men season to re-tune voice [A12]. Pick one text — a short story, a single scene from a film, a playlist — that is your lodestar voice. Re-read or re-listen at each chapter threshold. Voice drifts under load; the anchor is the only stable reference point at ~1/3 through a long work, which is the drift-danger zone.

**Infrastructure / content alternation.** Anthaum's *Course of Temptation* rhythm: one monthly patch adds systems (the variation engine — likeability, portrait crafting, chainable texting); the next adds content that leans on those systems [E10]. Prevents the common trap of shipping content that stales the engine, or engine that stales without content to validate it. For an ongoing Twine game: don't interleave authoring and engine work inside one release. Alternate.

**Modular production.** Failbetter shipped *Sunless Sea* as "3–5 islands per monthly update" [B28]. Because each island was a near-isolated storylet bundle, cutting or delaying one didn't break the rest. The same modularity is why Failbetter and inkle can hire freelance writers (Meg Jayanth wrote 750k words on *80 Days* as a freelancer) — every writer owns a city or an island end-to-end, and the quality-variable contract is the API [B29]. For single-author games, the benefit is the same under a different name: if a week's content doesn't ship, nothing downstream breaks.

**The single-sentence series-arc constraint.** Gilligan's *Mr. Chips to Scarface* again [A6]. The production discipline consequence is that **any scene that doesn't measurably move the sentence-arc gets cut** before it's polished. Many hours of editing are saved by a one-sentence test at draft stage.

**The corkboard-and-index-card method.** Sopranos writers' room practice [A5]. Thirteen cards on the wall = thirteen episodes of the season, each card a one-line statement of that episode's turn. Scenes within the episode on cards, cut with scissors, taped in order. The physicality matters: the spatial rearrangement surfaces pacing problems that on-screen outlines hide. For a Twine game: print the canvas list, cut it up, move the cards around on a table before writing prose.

---

## 12. Worked example — Maya's Tuesday shift, rewritten

The applied test. Below is a first-shift diner scene done two ways. The first is the failure pattern: atomic canvas, narrative wall, no accumulation, no "but," no distributed recognition. The second is the same scene with every applicable technique from this document stacked on it.

**Version 1 (the failure pattern)** — one node, 280 words, one choice:

> *Tuesday, 4:45 PM. Maya arrived at the diner. Marge showed her the apron and the order pad. Cookie nodded from the grill. Maya took table 3, then table 6, then table 9. The tips were okay — $35 for the night. Her feet hurt. She walked home under the streetlights.*
>
> [1 choice: "Count my tips" → return to hallway.]

**Version 2** — three nodes, state-gated, with all of the above techniques. Annotations in italics.

*Node 1 — "Through the back door"*

> Marge hands her the apron without looking up. "Dishwasher's broke. Help Cookie till 6, then take the floor." The apron's still warm from the last waitress.
>
> *[Chekhov detail inventory — Week 1: apron warmth, Marge not looking up, the dishwasher. These will shift at Week 3.]*
>
> *[1 choice — Motivated Forking (Fabulich rule [D.24]): same action, different internal write.]*
> — **"Tell Cookie I'm here."** *(confidence +1, a quiet entrance)*
> — **"Just start clearing."** *(independence +1, the girl who doesn't wait to be invited)*

*Node 2 — "Table six"*

> The trucker's been here twice already. Sits alone. Doesn't look up from his phone. He orders the same thing he ordered on Friday — coffee, black, a slice of pie the color of a bruise.
>
> *[Hades-style domain-gated NPC bark [F.DR3]: the trucker is the "first noticed" NPC for the Noticing-by-Men axis. Future weeks, he'll register different details about her. Tonight he doesn't register her at all.]*
>
> His ring is too big. He's lost weight.
>
> *[Luminous specific detail [A38]. The ring and the weight-loss say something the scene refuses to name. Reader files it.]*
>
> *[Group block [variant by low-week state]:*
> — Week 1: *"Your hand is shaking when you set down the coffee. He doesn't notice."*
> — Week 3: *"Your hand doesn't shake anymore. He doesn't look up."*
> — Week 6: *"Your hand doesn't shake. He looks up. You hold it a beat longer than you have to."*
>
> *That's the accumulation toolkit [F] doing distributed recognition [E28] without staging a scene about it.]*
>
> **"Anything else for you?"** *(keep moving — safe)*
> **"How's the pie?"** *(one more line — a test of the air)*
> **[Skip — move to next table]** *(the refusal — and Jayanth's rule [D.18] says the refusal is the scene; this branch gets its own three-line node where Maya wipes the counter twice while deciding not to ask)*

*Node 3 — "Closing"*

> Thirty-five dollars at the fold. Two fives, a ten, a crumple of ones and quarters. Marge tells her to come back Thursday and slides the schedule across the counter without looking at it.
>
> *[Weiner's hold-the-take [A15]: the schedule slide is the pause. Marge looking *away* is the information.]*
>
> Outside, the parking lot is one yellow bulb and gravel. Somebody's idling engine somewhere she can't see.
>
> *[Baxter [A38]: the idling engine is the subtext. Don't name it.]*
>
> *[Menace check [C.B6]: if `awareness_quiet_street >= 3` and `late_night = true`, a random ambient event fires in the next pass (never twice per week). Not tonight. Most nights it won't fire. The fact that it could is the ambient pressure.]*
>
> *[One choice — cost-as-deceleration [D.8] at the end:]*
> **"Walk home along Main."** *(−45 min to time, +ambient observed-by-the-world flag)*
> **"Cut through the alley."** *(−15 min to time, risk flag tick, one of Kennedy's resource-narrative [B3] resources — *exposure* — rises by 1)*

Nothing "happened" in this shift either. But:

- Three Chekhov-stage variant blocks are in place — weeks 3 and 6 of this same shift will feel like different scenes.
- The Motivated Forking on Node 1 writes personality, not just mechanics.
- The trucker's ring and lost weight are seeded for later scenes (Valve specificity tier [F.5]).
- The refusal branch is a characterization beat, not a dead-end.
- The hold-the-take at closing does what Weiner's pause does on screen.
- The Main-vs-Alley choice is a visible resource budget [B12] with stated stakes.
- The menace system [C.B6] is ambient — it didn't fire tonight, but the player will find out next week that it could have.
- Total prose budget is not much longer than Version 1. The work is not volume. The work is that every sentence has a job.

---

## 13. The one-page checklist

To run against any scene in an ongoing authored game:

1. **Horizon.** Which horizon does this scene close (beat / scene / session / chapter / act)? Is at least one other horizon rising?
2. **Sentence-arc.** Does this scene measurably move the single-sentence character arc?
3. **Engine of change.** Is the protagonist's shame or obsession surfaced, even glancingly?
4. **Expectation + but.** What's the expectation at scene open? What's the "but" that supplies the voltage?
5. **Luminous detail.** One concrete physical detail that carries subtext the scene refuses to name.
6. **Hold.** Is there a pause before or after the load-bearing line?
7. **Accumulation.** What's at least one detail in this scene that will read differently in five weeks, in one of: ambient prose, an NPC's tone, the protagonist's own description?
8. **NPC refusal.** Can the NPCs in this scene say no? What happens when they do?
9. **Distributed recognition.** Does any prose in this scene describe the protagonist in a way that wouldn't have been true three weeks ago?
10. **Relax token.** If this is a high-intensity scene, is the next scene a guaranteed-quiet one?
11. **Visible budget.** Does the player see what this choice costs before they make it?
12. **Refuse to repeat.** Is any emotional beat in this scene already played out in an earlier scene?
13. **Cut test.** If this scene were removed, what shape would the week be missing?

If a scene can't answer (1), (2), (4), and (13), it's not ready. If it can't answer (7) and (9), it's not ongoing-game writing.

---

## Confidence markers

- **High confidence:** sections 2 (nested horizons), 3 (renewing question), 4 (storylets + resource narrative), 7 (accumulation toolkit), 8 (pacing), 11 (production discipline). These claims are cross-cited by three or more designer-primary sources per technique.
- **Medium confidence:** sections 5 (character arc), 6 (NPCs), 9 (slice-of-life), 10 (corruption as shape). Supported by primary sources but many specifics (exact word counts, specific tuning numbers) are reconstructed or inferred from corpus, not quoted.
- **Lower confidence / caveat:** numeric claims — Wildbow's "12–16 chapter buffer," Failbetter's "30/20/100 word budgets," Hades' "21,000/30,000 line" counts. All are citable to at least secondary sources but primary internal docs were not reachable.

Disputed or contradicted claims worth knowing:
- **Chekhov's gun vs. Hemingway's iceberg** [A26][A27]. Productive tension, not consensus. Every writer must pick a mix.
- **Alison's non-dramatic shapes** [A33]. Most ongoing-serial practitioners still default to Aristotelian waves; her meander/spiral/radial/network alternatives have not been battle-tested at ongoing-serial length.
- **Destiny 2's weekly drip** [C.B7]. Rigid cadence helps communal pacing, hurts solo pacing. For a single-player ongoing game, internal act structure per chapter matters more than external release schedule.
- **P3/P4 reversal/break in Social Links vs. P5 removal** [B17]. Punitive design read as "guilt-trip on the scheduler-protagonist"; P5 cut it and let players experiment. For an adult-themed game with corruption stakes, the trade-off to consider carefully — are you designing a system that punishes neglect, or one that records it?

---

## Bibliography — citation registry

Citations in the body use the format [T#] where T is the task letter and # is the finding number in that task's notes. The task notes themselves, in this session folder, contain the full URL registry with source-type tags (official / academic / journalism / community / designer-blog), AS_OF dates, authority scores, and deep-read annotations.

- **Task A — Serialized TV + literary short fiction** (17 sources): Wildbow, Matthew Weiner (Paris Review), Vince Gilligan / Breaking Bad writers' room, David Chase / Sopranos, Peter Gould / Better Call Saul, David Simon / The Wire, Agnes Nixon / Harding Lemay / soap opera craft, Charles Dickens serialization, George Saunders (*A Swim in a Pond in the Rain*), Charles Baxter (*The Art of Subtext*), Jane Alison (*Meander, Spiral, Explode*), Alice Munro, William Trevor, Raymond Carver, Ernest Hemingway. See `research-notes/task-a-serial-craft.md`.

- **Task B — Life-sim & schedule-based narrative design** (16 sources): Emily Short (three posts), Alexis Kennedy / Weather Factory, Gareth Damian Martin / Citizen Sleeper, Persona 3/4/5 Social Link structural analyses, Stardew Valley wiki and dialogue modding docs, Disco Elysium / Thought Cabinet breakdowns, Long Live the Queen / Sam Kabo Ashwell, Kentucky Route Zero structural analyses, Jon Ingold / inkle. See `research-notes/task-b-life-sim-design.md`.

- **Task C — Emergent narrative + pacing** (28 sources): Tynan Sylvester / RimWorld, Tarn Adams / Dwarf Fortress (Procedural Storytelling chapter), Henrik Fåhraeus / Crusader Kings II, Michael Booth / Left 4 Dead Director, Jason Grinblat / Caves of Qud, Will Wright / The Sims, Henry Jenkins (Game Design as Narrative Architecture), Marie-Laure Ryan, Raph Koster, Jesse Schell, Emily Short (three pacing posts), Daniel Cook (Loops and Arcs), Destiny 2 seasonal design coverage, Naoki Yoshida / FFXIV, Agnes Nixon / soap opera craft, Fallen London menace system docs. See `research-notes/task-c-emergent-pacing.md`.

- **Task D — Interactive fiction craft** (20 sources): Emily Short (Beyond Branching, Storylets, Pacing Storylets, Mailbag, IF Theory), Richard Evans & Emily Short (Versu paper), Dan Fabulich / Choice of Games (stats rules, choice rules, taxonomy of choices), Jon Ingold (Problem of Failure, Narrative Sorcery, Ink docs), Meg Jayanth (Forget Protagonists GDC 2016), Chris Avellone (Project Eternity characterization), Brian Mitsoda (Tom Jubert interview), Ron Gilbert (Why Adventure Games Suck), Porpentine (Uses This, interviews), Aaron Reed (if50 on Howling Dogs), Sam Barlow interviews. See `research-notes/task-d-if-craft.md`.

- **Task E — Adult-game narrative craft** (15+ sources): Vrelnir / *Degrees of Lewdity* (Sad Girl Theory interview, Writer's Guide, wiki corpus), Vren / *Lab Rats 2* (gameplay loop post, character_guide), Anthaum / *Course of Temptation* (devlog), Majalis / *Tales of Androgyny* (combat design thread), Splendid Ostrich / *Newlife* (meta), Emily Short (Interactive Romance category, Procedural Text Generation in IF), Michelle Clough (*Passion and Play*), Nguyen & Ruberg (Designing Consent CHI 2020), Robert Yang via Gamedev.com intimacy article, Choice of Games / Heart's Choice forum. See `research-notes/task-e-adult-game-craft.md`.

- **Task F — Variant prose techniques** (28 sources): Emily Short (three posts), Failbetter writer guidelines, Ink official docs, Jon Ingold GDC 2015 + 2017, Elan Ruskin GDC 2012 (Valve Response System slides PDF), Valve Developer Wiki, Greg Kasavin GDC 2021 (Hades dialogue), Aaron Reed (quantum-text syntax, Subcutanean generation), Andrew Plotkin (Subcutanean review), Moral Anxiety Studio (Roadwarden deep dive), Gareth Damian Martin (Origin Story podcast), Kate Compton (Tracery, practical procgen), Darius Kazemi (Corpora), George Saunders on Chekhov's "The Darling," Causeway Lit on Munro's free-indirect style, Alexis Kennedy (Echo Bazaar voice), David Dunham / A Sharp (Six Ages), François Alliot (Reigns). See `research-notes/task-f-variant-prose.md`.

Full registry with URL, source-type, AS_OF, and authority scoring per source is in each task file's Sources section.

---

*End of report. ~5,400 words. Six parallel task notes with ~180 techniques and ~124 primary + secondary sources are preserved in the `research-notes/` sibling files; this document distills and organizes them topic-first.*
