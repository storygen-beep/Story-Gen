# PHASE 1: FOUNDATION
# The Long Summer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## GAME IDENTITY

**Title**: The Long Summer
**Protagonist**: Maya (female, player-controlled), 18 years old
**Genre**: Rural coming-of-age + economic pressure hybrid — adult interactive fiction with multi-NPC parallel arcs
**Perspective**: Third-person close through Maya — the reader sees what she notices, colored by how she feels. No omniscient asides, no cuts to other POVs.
**Theme**: Take a girl raised on one moral code, set her down in a town that enforces a different one, add rent, and watch which rules she keeps. The summer is the transformation. No awakening scene. The weather of her changing is emergent.

### Engine Configuration

| Setting | Value | Notes |
|---------|-------|-------|
| **Starting Canvas** | `opening_prologue_morning` | Maya wakes beside Daniel — the Prologue opens in her old life before the rural house exists as a destination |
| **Schema Version** | `"0.2"` | TOML v2 schema |
| **Sidebar type** | `trait_words` (Engine PRD F1) | Corruption band shown as prose voice-tell, not a number |
| **Hygiene decay** | `player.trait_decay` (Engine PRD F3) | Daily tick; shower restores |
| **Rent mode** | `eviction_mode = "flag_set"` (Engine PRD F4) | Fail-forward rent; shortfall fires a scene, doesn't end the run |
| **NPC arousal** | `modifier_effects` with `duration_hours` | Per-NPC hour-scale hidden state (Frank 2h / Ryan 4h / Jake 8h) |

### Thesis

> *"Take Maya through a long summer in a rural town that doesn't live by the rules she was raised on. She arrived carrying a moral code the place doesn't enforce. As she learns what her body and her wits can earn, you decide which parts of herself she keeps — and how much she walks away with."*

The thesis doubles as the player-facing welcome text and the designer's north star. Every scene, NPC, and choice is evaluated against it: does this press on which rules of her old code still apply here, and does it move either *who she's becoming* or *what she's walking away with*?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## STRUCTURAL INNOVATION: TWO REGISTERS UNDER ONE ROOF

The Long Summer's structural innovation is a *two-register world* stitched together by a single household.

### The town register

Outside Frank's property, the town runs on a permissive moral register. Men flirt and grope in the open at the diner. Transactional sexuality is visible if unspoken. Sexual encounters happen in public-adjacent spaces without causing scandal. The register is heightened — more charged than literary realism, less lurid than bait — and it's *craft-functional*: it removes the burden of making every sexual act a taboo-crossing. The dramatic weight sits on Maya's internal reaction, not on social rupture. What she does at the diner after close is mechanical. What she lets herself become by doing it, every night, for the tip — that's the game.

### The house register

Inside Frank's property, a *different* register holds. Diana is home. Dinner is at 6:30 because Diana holds it at 6:30. Chores have owners. The TV volume goes down at ten. The coffee timer starts at 5 a.m. Diana's register is not the town's puritan opposite — she is strict in a *father-shaped* way, structural not moralist, and her line is held quietly, without lecture. She is the one adult in Maya's orbit still carrying the old code. The pressure of the house is the pressure of Diana's trust: not a threat, a *trust* Maya can violate piece by piece without ever being caught.

### What the pair does

The house register and the town register are both *load-bearing*. The town permits; the house witnesses. The two registers together create the game's specific mechanical pressure: the mechanical act is cheap, the *meaning* is stored in what Diana doesn't say. Maya lives in both simultaneously. She walks out the screen door in the morning and the rules change in the gravel driveway. She walks back through that same door at eleven and they change again.

### Parallel NPC arcs, per-NPC clocks

Three deep NPC arcs run in parallel, each with its own trigger and its own clock.
- **Frank** is a *two-phase* arc. Phase A (Rules) is non-sexual: rules established, abidance tested. The trigger is locked — Frank catches Maya masturbating in the living room — and only then does Phase B (Restrict → Tease → Crack → Call-out → Keep) open. The clock is Maya's corruption plus her willingness to use his house against his rules.
- **Ryan** is a business-partners arc. The shop (used-equipment flip) on the property edge opens a ladder: Meet → Help → Partner → Big deal (closed with sex) → Beach (proposal, his Crack) → Keep. The clock is charm + corruption + deal progression.
- **Jake** is a hostility-to-hand arc. Meet hostile → Noticed (beauty rising) → Peeking + drawing → Tease → Caught (she catches him) → Hand (she offers a handjob on her terms) → Keep. The clock is beauty rising plus corruption rising together.

At most one Crack fires per chapter. `brothers_discover` milestone fires late in Phase 1. `diana_awareness` accumulates silently across the summer without Diana ever confronting Maya in Phase 1 — her arc is reserved for Phase 2+.

### Economic pressure as corruption engine

Maya starts with $400. Rent to Frank is $60/week. Groceries cost $15/week. College admission (the stretch goal for the summer) sits at roughly $1,500. Base diner wages — Tier 0 — are mathematically tight but survivable. Tier 2 of the diner tier system and a Partner-level cut of Ryan's big-ticket closes are required to actually hit the college savings threshold. The game never tells Maya to tilt the room. The math does, and her pride won't let her call Diana.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## THE PROTAGONIST: MAYA

**Age**: 18
**Background**: Just out of high school. Artist-inclined — sketches as her primary self-expression, her one reliably sincere act. Emotionally recovering from a recent breakup (Daniel, her ex) plus friend-group collapse in the wake of what she did for revenge. Hardened, not soft — she learned *don't give your heart, use your head*, and the Prologue is how the player learns it with her.

**Visual**: Average height, slim, body still half between girl and woman. Dark hair usually pulled back with whatever's in reach. Arrives in a hoodie and jeans and one suitcase. Looks younger than eighteen when she's tired. The face of a girl no one in Millhaven has a prior opinion about.

**Psychology**:
- **Want**: Save enough to move out. She isn't chasing a degree or a specific program — she wants *resources* to leave and be her own person. Art is hers; it isn't the plan.
- **Need**: Rebuild a sense of self after the collapse. Figure out who she is when she's not defining herself through other people.
- **Fear**: Becoming someone calculating she can't recognize — that the summer ends and the woman who walks out of Frank's house isn't someone she'd have been friends with in May.
- **Flaw**: Can't ask for help. She'd rather work the late shift than call her mother, rather take a worse deal than say the words *I'm short this week*.

**Voice axis**: Early game she observes. Late game she operates. The transition is carried by her corruption band — not narrated, not announced, just the sentence rhythm shifting from *did he just look at me like that?* to *I know exactly what I just did to the room.*

**Recurring obsession**: men's hands (public layer) — she has always watched hands, the carpentry kind, the holding-a-cup kind, the kind that rest on a counter near hers. Dicks and dreams of them (private layer) — the bed-in-the-dark layer, where a stray shape in a dream lands her on a specific man and she wakes annoyed at the target.

**Shame engine (Prologue-inherited)**: She arrived at Frank's house already having crossed her own line. The Prologue's revenge beat is *symmetric cheat-for-cheat* — Daniel cheated, she cheated back. Her shame is not about the act. It's about the intent: she wanted to hurt someone, she did, and she can do it again if she chooses. The Prologue answers the dramatic question *what's the line Maya won't cross?* with *she already crossed it.* The rest of the summer is what she does now that she knows.

**Art as private sincerity**: Even when Maya is being calculating in a scene, her sketchbook stays hers. A drawing of Jake's hands from memory is still honest. This matters for the late-game voice — she isn't a cynic, she's a young woman who learned to use what she has.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## THE NPCs

### NPC 1: Frank — The Stepfather (Disciplined Landlord)

**Vibe**: The man who built his house with his hands and runs it the same way. Present but not intrusive. When he speaks, it's in complete sentences. He drops his contractions when he's serious, which is often. He addresses Maya by name — *Maya* — and the name lands like a door closing.

**What makes him compelling**: Frank is a two-phase character. In Phase A he is the rule enforcer — not a moralist, but a man who keeps the household functional because that's his job. Phase A is non-sexual. He tests Maya with small things (the dishes, the porch light, the gas money) and she either abides or she doesn't. Phase B only opens once Maya provides the trigger: he catches her masturbating in the living room. The trigger is locked. After it fires he becomes the man who *wants to be chosen* and cannot admit the wanting — Restrict, then Tease under compliance, then Crack, then Call-out, then Keep. His internal contradiction is that the rule enforcer and the man-who-wants-to-be-chosen live in the same body, and the catch-trigger is the only moment that body admits them at once.

**Age**: 48
**Build**: Broad through the shoulders. Hands that look like they were made by the work they do — blunt, calloused, capable. Salt-and-pepper hair kept short. Reads the paper at the kitchen table every morning. Flannel shirts with the sleeves rolled to the elbow. Jeans that fit. Work boots by the door.

**Primary driver**: Rule enforcement → latent authority
**Secondary driver**: Wanting to be chosen (hidden until Phase B)
**Starting traits**: `love = 0, trust = 10, corruption = 0` (trust starts above zero because he chose to take in Diana's daughter)

**Key dynamic**: Frank controls the roof. Rent is paid to him. His office is in the house. The catch-trigger fires in *his* living room — Maya using his house against his rules is what Phase B is about.

**Resistance type**: Self-control. He knows what he's feeling in Phase B. He has the language for it. He has decided to hold the line. The line is held until it isn't.

**Difficulty**: HARD — Phase B only opens after the masturbation trigger, then requires corruption mid-band to climb. His Keep tier has the most routes (romantic / arrangement / rupture / power-inverted).

*Internal thought at T1 (Phase A Rules):* "*She's Diana's girl. She keeps her room tidy. The rent was on the table Sunday morning without my asking. That's the whole job.*"

---

### NPC 2: Ryan — The Older Stepbrother (Peer-Male Labor)

**Vibe**: Competent with his hands, easier to be around than Frank, easy to like until he isn't. Speaks in fragments. Colloquial, comfortable. Compliments sideways — *you cleaned up in that one*, not *you look nice* — and doesn't apologize when he's uncertain. Hands are always busy: wrench, wire, grease rag, the strap of whatever he's loading.

**What makes him compelling**: Ryan runs a used-equipment flip out of a shop on the property edge. Tractors, small engines, trucks, lawn gear. Buys broken, fixes what he can, resells for margin. The business is his identity, and it's failing at the edges — margins thin, big buyers scarce. His arc is a *business-partner arc*: Meet → Help → Partner → Big deal closed with sex (the buyer won't close without it; that's the *big* deal) → Beach proposal (his Crack) → Keep. His internal contradiction is that the brother with the hands wants to succeed on the hands, and Maya becoming the closer means the business is theirs, which means the identity is no longer just his.

**Age**: 25
**Build**: Lean through the shoulders, strong through the back, tanned from yard work. Stretches after he sets something down. Eye contact rare but lands when it does. Faded t-shirts. Work boots worn soft at the toe.

**Primary driver**: Honest hustle → shared profit
**Secondary driver**: The business *is his identity*
**Starting traits**: `love = 0, trust = 5, corruption = 0`

**Key dynamic**: Ryan controls the *other* income channel. Diner tips are Marge's; shop cuts are Ryan's. Maya helping at the shop is peer-male labor, which means she's in his world, which means the big-ticket buyers — a retired farmer, an out-of-town scrapper, a divorcé — surface for her to close. Ryan watches her close the first one. He watches how.

**Resistance type**: Low at first, higher at the Beach. Ryan is ready for Maya from around the Partner tier. The Beach is *his* resistance — he proposes and the proposal costs him the last illusion that the business is just a business.

**Difficulty**: MEDIUM — arc activates earlier than Frank's, runs on a charm-plus-corruption clock, but the Beach is a *real* Crack beat that demands a Maya-voice answer.

*Internal thought at T1:* "*The tractor guy's back tomorrow. He always folds ten percent off asking. Maya's gonna be in the yard. Gonna see if he folds at full.*"

---

### NPC 3: Jake — The Younger Stepbrother (Hostile Artist)

**Vibe**: Long sentences when he's comfortable, clipped when he's not. Vocabulary shows the education he hasn't finished. Hedges himself. Asks follow-up questions to keep from being asked them back. Hides behind objects — the laptop, the sketchbook, the door. Flinches at touch. Draws nude women as his working register; secretly draws Maya once her beauty rises.

**What makes him compelling**: Jake is the artist who doesn't want to want her. His arc is a hostility-to-hand arc: Meet hostile → Noticed (her beauty stat rising crosses his threshold) → Peeking + drawing (he starts with bedrooms, bathrooms, the yard when she's alone) → Tease → Caught (*she* catches *him* — a found sketchbook, a shadow on the wrong wall) → Hand (she offers a handjob on her terms, the whole power geometry inverted) → Keep. His internal contradiction is that wanting her costs what he was protecting — the idea that he's different from Ryan, different from Frank, different from the men at the diner. The peeking makes him the same. Drawing her is the only thing he still does *as himself*.

**Age**: 21
**Build**: Lean. A little taller than Ryan. Glasses for drawing, off for everything else. Shaggy brown hair he pushes back with his wrist. Uses the porch rail and doorframes to stand against. Wears black more than the others. Wrists look like they could be broken in one grip.

**Primary driver**: Art as a register of honesty → then peeking as the register cracks
**Secondary driver**: Being different from Ryan and Frank (until he isn't)
**Starting traits**: `love = -5, trust = 0, corruption = 5` (love starts negative — he is actively hostile at arrival)

**Key dynamic**: Jake has the opposite clock from Frank. Frank needs corruption plus the catch-trigger. Jake needs beauty *plus* corruption together. The first glance he *can't* look away from is her arc opener.

**Resistance type**: Innocence that converts to shame and then to negotiation. The Caught beat is not a humiliation — it's the moment Maya realizes she owns the scene.

**Difficulty**: EASY to the Hand beat (the trigger is beauty, which rises fastest of the stats she can build without corrupting), then HARD at Keep (four routes: owned / lovers / withdrawn / she-uses-him — the only arc with a power-inverted route).

*Internal thought at T1 (Meet hostile):* "*Diana's got her girl staying here all summer. I already spent two years keeping out of the way of two men I don't like. Now there's a third person in the house who's going to look at my door when she walks past it.*"

---

### NPC 4: Diana — Mother, Household Anchor

Diana is the reason the house is a family. Widow — Maya's biological father died a few years back — remarried to Frank, warm with Maya, structurally strict. She cooks with her hands, not recipes. She uses Maya's name directly and often. She doesn't ask questions she doesn't want answers to. She is on the porch alone most Sunday afternoons with a book or the newspaper. **She is not an arc NPC in Phase 1.** Her dramatic function is structural: she makes recurring group scenes exist (the 6:30 family dinner, Sunday mornings), she anchors the house's schedule, and she is the *quiet witness* that makes every Maya choice weighable against *what Diana would think*. `diana_awareness` accumulates silently across the summer. She does not confront. That silence is the heaviest pressure in the game.

---

### NPC 5: Marge — Diner Owner (Simple Employer)

Marge runs the diner on Main Street. Hires Maya in Chapter 1. Hands her the Thursday-night key at the close of Chapter 2 — the `first_ambient_tilt`. She is a simple employer. **She has no sexual arc.** She notices what the customers do to her girls. She decides who gets the back booth after close. Her relationship with Maya is an honest wage-for-work line with one quiet promotion moment. The owner/appraisal sexual dynamic is deferred to Future Considerations; in Phase 1, Marge is a clean Mentor-lite: older, working, watchful, undeceived.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SETTING

**Type**: Southern small town + rural property on its edge

**Town**: **Millhaven, North Alabama.** Population around four thousand. Big enough for a diner, two churches, a community college, a high school, a short downtown strip, and a truck stop on the highway. Small enough that everyone knows whose truck is parked where. Economic base in slow decline: some light industry, cycling wage work, old agriculture. Town peaked thirty years ago and hasn't decided whether it's dying or just resting. Prose palette: heat that doesn't let up, red clay and pine, afternoon storms, crickets at night, honeysuckle and kudzu, screen doors, church bells on Sundays.

**The property**: Frank's place sits on the edge of town — a contractor-built house with a detached outbuilding (Ryan's shop), a yard that blurs into fields, a creek behind the trees, and a trail head that rises into pine. Ten minutes' walk to the nearest neighbor, twenty-five minutes' walk to Main Street. Gravel driveway that crunches under every arrival and departure.

### Phase 1 active hubs (five)

| Hub | Role | Primary NPCs |
|---|---|---|
| **Frank's property** (house + yard + creek + trail + Ryan's shop) | Home arena. Most arc beats. | Frank, Ryan, Jake, Diana |
| **The diner** (Main Street, 6am–10pm Mon–Sat, closed Sunday) | Primary income. Diner-tier system. | Marge, Cookie, regulars |
| **Main Street** (general store, post office, gas station) | Public errands, rep_road and rep_church visibility | Ambient |
| **College admin office** | Single early visit for the application brochure, then gated until the admission money is saved | Admin clerk (ambient) |
| **Driveway / town-walk path** | Travel, ambient corruption encounters, Sunday walk to and from church | — |

### Gated in Phase 1 (visible, not visitable)

- Truck stop bar on the highway (named in ambient reference, not entered)
- Fairground
- High school stadium
- Church interior (Diana attends; Maya is ambient only)
- Full community college campus (classes, library, quad — tuition-gated)

Five active hubs. Five gated hubs as Phase 2+ surfaces. Manageable authoring surface.

### Calendar

**Sunday** is the only recurring structural beat in Phase 1. Diner is closed. Church bells. Diana attends. Maya can go or stay home. Main Street is thinner. Frank reads on the porch. All Phase 2+ calendar events (Friday football, Saturday market, fair, bar) are deferred.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## CORE PREMISE

**The "What If?" Hook**:

What if an eighteen-year-old girl, hardened by a summer-of-graduation revenge beat she already went through with, landed in a small Southern town that runs on a permissive moral register — staying in her stepfather's house with her mother, who still holds the old code, and two stepbrothers who each have their own reasons to notice her?

**Emotional Journey**:

Maya arrives at Frank's property with one suitcase, $400, and a shame-engine her mother doesn't know about. The Prologue has already fired — she cheated symmetrically on a boyfriend who cheated first, and the friend group collapsed around the act. The town doesn't live by the rules she was raised on. The house does. She lives in both at once.

The first week is household. She meets Frank's rules, Ryan's yard, Jake's closed door. Diana's kitchen at 6:30. She walks to Main Street, finds the diner, meets Marge. Takes the Tier 0 shift. Counts her money. Realizes the math is tight — $60 rent weekly, $15 groceries, and a tuition target that doesn't come down to her wage.

Her pride won't let her call Diana about money. So she finds her own solutions: Tier 1 diner tips (play along with the regulars), help at Ryan's shop (small tickets at first), better shifts from Marge. Each solution adjusts her corruption band upward. Each band changes what options appear on the next day's menu. No awakening scene. The weather of her changing is emergent. Three NPC arcs activate in parallel on their own clocks — Frank's when she masturbates in *his* living room, Ryan's when she closes her first big-ticket deal, Jake's when her beauty rises high enough that he can't stop looking.

The summer is long. Phase 1 closes on a yet-unnamed event; the design is laid out first, and the ending is defined later once the arcs are playable. The placeholder lock is the **Keep-Tier Fork**: summer's end forces Maya to commit to one NPC's Keep tier, or to independence. Diana is at the table.

The game never lectures. The game never moralizes. The economic math and the permissive register do the work. Maya's pride removes the easy exits. Proximity, heat, and routine do the rest.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## TONE

**Southern heat + permissive undercurrent + Diana's old-world discipline inside one house.**

The prose palette is slow, sensory, hot. Crickets through the screens. Fans on the ceiling. Screen doors that slap. Cheap coffee. Pine resin on hands after the trail. Red clay on the rug by the back door. Inside Frank's property: order, routine, dinner at the table. Outside the property: the town's own rhythm, which does not match what Diana enforces at home.

### Per-NPC tone

- **Frank (Phase A)**: restrained, grammatical, warm but not familiar. Complete sentences, dropped contractions when he's serious. Statements not questions. *"Maya."* openings. Hands flat on the table. Jaw tightening at the word he won't say.
- **Frank (Phase B)**: the restraint weaponized. The same sentences, cut shorter. Eye contact held a second past where it was before. The mirror gaze — that's the cracking Frank.
- **Ryan**: fragments. Colloquial. Uncertainty without apology. Indirect compliments. Hands always busy. Eye contact rare but landing. The stretches after labor. When he's flirting, the sentence gets shorter and the pause gets longer.
- **Jake**: long sentences when comfortable, clipped when not. Vocabulary shows the education. Hedges. Follow-up questions. Hides behind objects. Flinches at touch. When he's drawing her, sentences get quiet and then stop entirely.
- **Maya** (internal): tightens or relaxes by stage. Artist's eye — the detail-inventory habit. Internal hedging early; deliberate notice mid; clean naming late.
- **Diana** (ambient): the voice you don't notice until she's already been heard. Uses Maya's name. Doesn't ask the question she doesn't want to hear. Doesn't lecture.
- **Marge**: short sentences, no wasted syllables. The voice of a woman who has heard every excuse.

### Corruption-band narration shift (Engine F1 — `trait_words` sidebar)

The `corruption` stat is *not* shown as a number. It is surfaced through the sidebar as one of four prose voice-tell bands:

- **Closed (0–24)**: Observational, slightly anxious. She notices things and is uncomfortable noticing. *Did he just look at me like that?* Short sentences. Self-conscious.
- **Opening (25–49)**: Awareness becomes attention. She's noticing *and* cataloguing. Internal voice gets a little bolder. *He looks at me when I reach. I let it happen.* Longer thoughts. Less guilt.
- **Operating (50–74)**: She's the agent now. Internal voice is deliberate. *I wore this because of the regulars. I know what the tip will be.* Direct, unapologetic.
- **Saturated (75–100)**: She's operating in a language of her own making. *This is the room I walked into and this is the room I'm walking out with.* Confident, sometimes calculating, still with art as the private honest register.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## GAME SCOPE

### Scale targets (Phase 1 + Prologue)

| Element | Target | Notes |
|---|---|---|
| **Phase 0 (Prologue) duration** | ~45–90 minutes | 4 acts, ~20 beats; suburban-normal moral register; contrast to town |
| **Phase 1 duration** | Open-ended | No fixed day count. Phase 1 closes on the Keep-Tier Fork when the arcs have played |
| **Deep NPCs** | 3 (Frank / Ryan / Jake) | Each with own trigger, own clock, own Keep-tier route set |
| **Anchor NPCs** | 2 (Diana / Marge) | No Phase 1 arc; structural |
| **Peer NPC** | 1 (Cookie, diner peer) | Light spec; ambient |
| **Active hubs** | 5 | Property, diner, Main Street, college admin, driveway |
| **Gated hubs** | 5 | Truck stop bar, fairground, stadium, church interior, full college |
| **Time periods per day** | 6 | morning / mid-morning / afternoon / evening / late / overnight |
| **Player traits** | 10 | energy, hygiene, fitness, beauty, corruption, calculation, money, rep_church, rep_road, rep_college |
| **Sub-reputations tracked** | 3 | rep_church, rep_road, rep_college — independent |
| **Total story beats** | ~40–45 | Prologue ~20 + Phase 1 ~20–25 |
| **Diner tiers** | 4 | T0 Distance / T1 Play along / T2 Work the floor / T3 Back booth after close |
| **Ryan shop tiers** | 4 | Help / Partner / Big deal / (Ryan-Crack = Beach) |
| **NPC Keep routes (total)** | 10 | Frank × 4 (romantic / arrangement / rupture / power-inverted) + Ryan × 3 (yes engaged / not yet / no withdrawn) + Jake × 4 (owned / lovers / withdrawn / she-uses-him). Each group `required_count = 1`. |
| **Gate flags (locked)** | `revenge_committed`, `told_sarah`, `calculation_tier`, `backed_out_of_revenge` (Prologue); `first_rent_paid` (Ch1 close); `first_ambient_tilt` (Ch2 close); `brothers_discover` (late Phase 1); `diana_awareness` (accumulating) | Cross-gating per arc per chapter |

### Architecture choice (locked)

**Multi-NPC Parallel Arcs (Pattern A) + Economic Pressure (Pattern C).**

- Pattern A governs the NPC structure: three deep arcs on their own clocks, cross-gated so at most one Crack fires per chapter.
- Pattern C governs the motor: rent + groceries + tuition target creates the daily pressure that tilts corruption upward unless actively resisted.
- Pattern L (clothing tiers) is *partial* — the engine's `clothing_enabled` is off per F2, so wardrobe is narrative-texture only in Phase 1, not a mechanical gate.

### NPC arc overlap (corruption bands)

```
Corruption:  0     25    50    75    100
             |      |     |     |     |
Closed       ██████
Opening            █████████
Operating                  █████████
Saturated                           █████████

Frank Phase A:       ████████████████░░░░░░░░
                     (Rules, tests; non-sexual)
Frank Phase B:                ████████████████
                              (Restrict → Tease → Crack → Call-out → Keep)
                              — gated on masturbation-in-living-room trigger

Ryan Help:        █████████░░░░░░░░░░░░░░░░░░
Ryan Partner:              ██████████░░░░░░░░░
Ryan Big deal:                     ██████████░
Ryan Beach (Crack) + Keep:                █████

Jake Noticed:        ███████░░░░░░░░░░░░░░░░░░  (triggered by beauty + corruption)
Jake Peek/Draw:           ███████████░░░░░░░░
Jake Caught:                        ██████████
Jake Hand + Keep:                           ███

Diana_awareness:     █████████████████████████████
                     (accumulates silently across the whole summer)
```

Two or three arcs are always live. Frank's Phase A runs the whole time as a *household* arc; his Phase B only opens after the trigger. Jake's clock depends on beauty rising, which she can build cleanly; his Caught beat is where the arc becomes hers.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## RECOMMENDED DIRECTION

**The Long Summer** is a female-protagonist adult game where a permissive Southern town register and an old-code household register share one eighteen-year-old, and the summer is how she decides which rules of her old code still apply.

The structural core is the **two-register world**. Unlike games that place their protagonist in a single moral frame, The Long Summer puts Maya in both at once — the town's permissive register outside the door, Diana's structural register inside — and makes the pressure live in the gap between them. Every act is cheap in one register and weighable in the other. Diana is not positioned as antagonist. Her silence is the load.

The **three NPC arcs** run on their own clocks: Frank locked behind a specific trigger (masturbation in the living room, his house, his rule), Ryan riding the shop's economic ladder, Jake gated on beauty plus corruption rising together. Each arc has a real Crack beat and a Keep tier with multiple routes, including a power-inverted Jake route where Maya is the one who owns the scene.

The **economic engine** is what makes the corruption organic. $60 rent plus $15 groceries plus a $1,500 tuition stretch target plus a base diner wage that *just about* covers life means Maya either works the higher diner tiers or closes at Ryan's shop — or both — or misses the target and plays Phase 2 without the escape she planned. The game never tells her to escalate. The rent does. The brochure on the fridge does.

The **corruption system** is bundled into a single axis, surfaced as four prose bands through the `trait_words` sidebar (Engine F1). The game shows the player *words*, not numbers. The player infers state from sidebar text, menu availability, and prose tone. This is the mechanical spine of the thesis *which parts of herself she keeps* — the player can watch Maya become someone without ever being told she's become her.

The **Prologue** exists because the shame engine has to be *played*, not read. Phase 0 takes Maya through a normal-suburban Act 1, a discovery Act 2, a revenge Act 3, and a collapse Act 4. Key Prologue flags (`revenge_committed`, `told_sarah`, `calculation_tier`, `backed_out_of_revenge`) carry into Phase 1 as both memory and mechanics. By the time Maya's truck hits Millhaven's town-limit sign, her old moral code is the *player's own memory*, not backstory.

**The question the game asks**: Maya arrived carrying a code the town doesn't enforce. The town offers a different one. Diana carries the old one in the kitchen at 6:30. When the summer ends and Maya hands her rent to Frank one last time, which code is hers, and how much is she walking away with?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
End of Phase 1 — Foundation. Proceed to Phase 2: Characters & Stats.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
