# PHASE 2: CHARACTERS & STAT ECONOMY
# The Long Summer

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 1: PLAYER DEFINITION — MAYA

### Basic profile

**Name**: Maya
**Age**: 18, just out of high school
**Visual**: Slim build, average height, body still half between girl and woman. Dark hair pulled back with whatever's in reach — a cheap elastic, a pencil, the hem of a t-shirt. Arrives in a hoodie and jeans and a single suitcase. The kind of face Millhaven hasn't decided anything about yet.
**Background**: Artist-inclined since middle school — pencil and charcoal as her primary self-expression. Not art-school-bound; art is her *private* sincerity, not her plan. Working-class-adjacent upbringing with Diana. Father died a few years back. Diana remarried Frank and moved south.
**Prologue-inherited state**: The collapse has already happened. Daniel cheated with Emma. Maya cheated symmetrically with Emma's boyfriend Kevin. Sarah (best friend) reacted badly. The friend group shunned her. Staying with Diana at Frank's house is the landing pad that's left.

### Starting stats (Phase 1 Day 1, pre-Prologue-roll)

Values below are the *nominal* starting state before Prologue outcomes adjust them. The Prologue edits corruption and calculation before Phase 1 begins.

```toml
[player]
money = 400           # cash on hand at arrival
energy = 100          # full after travel rest
hygiene = 100         # freshly showered before the drive
fitness = 30          # baseline — not athletic, not sedentary
beauty = 40           # moderate — can rise with maintenance + wardrobe
corruption = 0        # adjusted by Prologue (see 'Prologue inheritance' below)
calculation = 20      # adjusted by Prologue
rep_church = 0        # no Millhaven reputation yet
rep_road = 0
rep_college = 0
```

### Prologue inheritance (Prologue → Phase 1)

Four Prologue flags and two stat overrides transfer into Phase 1:

- **`revenge_committed`** (bool) — did she go through with Kevin. If `true`, `corruption` lands at **18–22** on arrival (mid-Closed band). If `false` (she backed out), `corruption` stays at 0.
- **`backed_out_of_revenge`** (bool) — the opposite toggle, tracked for prose-register purposes (she remembers the choice even if she didn't make it).
- **`told_sarah`** (bool) — did she confess. Shapes the shame weight of recurring flashback beats and Diana-phone-call echo texture.
- **`calculation_tier`** (enum: `impulsive` / `moderate` / `deliberate`) — how much she planned the revenge vs. acted in the moment. Sets starting `calculation` to 15 / 25 / 35 respectively.

The Prologue's role is not to narrate these values into existence. It's to make the player *remember* choosing them.

### Psychology — Want / Need / Fear / Flaw

- **Want**: Save enough to move out. Not a degree, not a career plan — *resources* to leave and be her own person. She's chasing independence as a literal dollar amount.
- **Need**: Rebuild a sense of self after the collapse. Figure out who she is when she isn't defining herself through a boyfriend, a friend group, or a mother's worry.
- **Fear**: Becoming someone calculating she can't recognize. That the summer ends and the woman who walks out of Frank's house isn't someone she'd have been friends with in May.
- **Flaw**: Can't ask for help. She'd rather work Thursday late than call Diana about rent. She'd rather take a worse deal than say the words *I'm short this week*. Her pride is the economic engine.

**How the flaw drives the game**: Maya's pride is what the math exploits. She won't confess her financial state to Diana. She won't ask Frank for a rent deferral. She won't call her aunt. Every practical problem she solves herself pulls her one click deeper into a corruption band. The game never tells her to tilt the room. The math does, and her pride won't let her ask for another way.

### Player emotional phases — keyed to corruption bands

The Long Summer doesn't use a separate "emotional phase" stat. The single `corruption` stat carries the phase through its four `trait_words` bands (Engine F1). Maya's phase *is* her band.

| Corruption band | Phase name | What Maya notices | How she describes the house | Choice-text framing |
|---|---|---|---|---|
| **0–24 Closed** | Observing | Accidents, not patterns. *Did he just look at me like that?* Notices being looked at as a surprise. | *Frank's house. The stepdad's place.* Generic descriptors. | Choices read cautiously. *Smile politely / Keep my eyes on my plate / Say thank you and leave.* |
| **25–49 Opening** | Attending | Patterns emerging. She catalogs. Catches herself having a second thought about a first thought. | *Frank's kitchen at dinner. Frank's office when he's working late.* Claims specific rooms. | Choices include *let him see / hold the look a second longer / lean against the counter.* |
| **50–74 Operating** | Deliberate | She picks her targets. She uses her effect on purpose. Still has the artist's honesty — she can name what she's doing to herself. | *My Thursday. My booth. My shift.* Possessive language surfaces. | Choices include *tilt the room / close him / say what he needs to hear.* |
| **75–100 Saturated** | Operating+ | She speaks the language she made. Her art stays hers. | *Millhaven* as a thing she belongs to, not a thing she arrived in. | Choices include *let him choose the tier / pick a number higher than he expected / leave the key where she'll find it tomorrow.* |

### Internal voice evolution — observes early, operates late

The narrator sits in third-person close through Maya. Voice evolves:

**Closed band — observational prose.** *"She felt him look, and the look went somewhere she wasn't ready to describe. She picked up the coffee pot with both hands because one felt like it would shake."* Short sentences. Hedges. Artist's eye catalogs details before naming them.

**Opening band — catalog-with-notice.** *"She counted the men in the booth by their hands first: the rings, the calluses, the one with a wedding band worn thin. She registered the counting as it happened. She let herself register it."* Sentences lengthen. She notices herself noticing.

**Operating band — deliberate naming.** *"Thursday was the trucker shift and she wore the blue, because the blue ran two dollars more per table than the grey, and she wasn't lying to herself about why anymore."* Direct. Unapologetic. The noun *she* is replaced by active verbs.

**Saturated band — the voice she made.** *"She closed the till at eleven. The key went into her pocket. She walked the hour home by the light of other people's porches and thought about nothing, which was the thing she'd been practicing."* Declarative. Minimal hedging. Art remains the one honest register — sketches in her journal read *differently*, a register the corruption prose never touches.

### Recurring obsessions (per §3 Maya profile)

- **Hands (public register).** Maya has always watched hands — carpentry hands, holding-a-cup hands, hands that rest on a counter near hers. Every NPC first-description passes through their hands. The public, legible, notice-able thing.
- **Dicks and dreams of them (private register).** The bed-in-the-dark layer. A stray shape in a dream lands her on a specific man and she wakes annoyed at the target. This register lives in solo scenes, masturbation scenes, and the moment before sleep. The prose is frank without being pornographic — honest about the bed-dream weight without turning it into bait.

### Sexual history

Limited. Daniel, ~2 years, ended a few weeks before Phase 1 opens. She's not innocent — she's inexperienced *and* she's just used sex weaponized (Kevin, the Prologue revenge beat). The combination is load-bearing: she knows what sex is mechanically, she's done it emotionally, and she's done it tactically, all within three months. Phase 1 is what she decides about that combination.

### Art as private sincerity

Maya's sketchbook is her one reliably honest register. Even at Saturated corruption, the sketchbook is clean. A drawing of Jake's hands from memory is honest in a way Maya's voice in the same scene might not be. This matters for:
- **Keep-tier Jake route (power-inverted):** the sketchbook is the thing the power is leveraged through.
- **Late-game prose texture:** when Maya sketches, the narrator's voice quiets and the corruption-band prose register briefly inverts.
- **Tone diagnostics:** if a scene written in the Operating band can't find a moment where Maya could sketch something honest, it's likely over-compressed.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 2: NPC DEFINITIONS

### NPC 1: Frank — The Stepfather

**Role**: `npc_frank` — Maya's stepfather (Diana's second husband). Household head. Economic gatekeeper (rent). Two-phase arc: Rules (Phase A, non-sexual) → Trigger (living-room masturbation) → Sexual arc (Phase B).

**Age**: 48
**Physical appearance**: Broad through the shoulders and heavy in the arms — a man who still does the work he used to get paid for. Hands look like they were made by the work they do: blunt, calloused, with a web of small scars from framing and wiring. Salt-and-pepper hair cut short every four weeks at the barber on Main Street. Crow's feet that deepen when he's tired, which is more often than he admits. Clean-shaven Monday through Friday; a shadow by Sunday night. Flannel shirts rolled to the elbow spring through fall, t-shirts when the heat gets above ninety. Jeans that fit. Work boots by the door.

#### Personality

| Surface | Hidden |
|---|---|
| Disciplined, quiet, grammatical. Reads the paper at the kitchen table every morning. Runs his household like a job-site: clear rules, fair enforcement. | A man who wants to be *chosen* — not obeyed, not feared, chosen. Has been alone with the idea of Diana for years and is just now living the real version. Watches Maya more than he admits because she reminds him of a younger Diana, and that fact horrifies him. |
| Rent-payer's welcome — treats Maya fairly, doesn't exploit the landlord position, doesn't lecture. | The rule enforcement is an armor. Without the rules he would have to ask himself what he *wants* from the house, and he has never had the vocabulary for wanting out loud. |
| Courteous, patient, slow to anger. | Capable of significant anger when the code is violated — not yelling, but a jaw-tight stillness that reads as worse than yelling. The Call-out tier is what happens when that stillness fails. |

#### Psychology

Frank built his adult identity around *being the steady one*. After his first wife left (prior relationship, dissolved amicably, no scandal), he lived alone for eleven years before Diana. The discipline of that eleven years — up at 5:30, coffee timer, paper, the work, home, dinner, bed — became his self-image. Diana remarrying in did not disturb the discipline. Maya arriving in — a girl his biological sons' age range, Diana's daughter, in his house — disturbs it in a way he cannot locate and therefore cannot speak about. He defaults to the discipline: more rules, tighter schedules, sharper attention. The trigger event (Maya masturbating in the living room) is the moment the discipline fails because the rules have no answer for what he's just seen. He is a man who has spent his life solving problems with rules and he has just encountered a problem the rules produced.

#### Internal contradictions (2–3)

1. **The rule-enforcer who wants to be chosen.** Frank's authority is how he stays necessary. If he weren't the rule-maker, what would his role in the house be? He runs the rules *because* he needs the position, and the position is the only way he knows to be near her. The trigger makes the two indistinguishable: the rule he *chose* to make (curfew, common-area behavior, respect for shared space) and the moment he *wanted* her to break.
2. **The self-control that wants to break.** Frank's discipline is the thing he's proud of. He also wants to be the man who *loses* the discipline, because a man who cannot lose discipline cannot be *chosen* — only obeyed. The Crack tier is him allowing the failure that his pride has been fighting.
3. **The protector whose protection is the threat.** He wants to take care of Maya (Diana's daughter, his house, his responsibility). The protection puts him in proximity. The proximity is the whole problem. Every time he "checks on her" he's doing two things at once, and by Phase B he can no longer tell which is which.

#### Resistance pattern

| Stage | Behavior | Trigger for the stage |
|---|---|---|
| **Mild (Phase A baseline)** | Courteous, rule-enforcing, emotionally distant. Leaves the room when Maya walks into it in a towel. | Day 1 arrival |
| **Moderate (early Phase A tests)** | Small corrections delivered calmly. *"Maya. The porch light."* Hands stay flat on the table. | Minor rule violations (missed chore, late curfew) |
| **Severe (late Phase A, under pressure)** | Longer silences. Longer pauses before speaking. Eye contact held a fraction too long, then broken deliberately. Drinks whiskey on the porch an hour longer. | Maya's corruption rising past mid-Closed; ambient tension climbing |
| **Recovery (post-Call-out, in Keep branches)** | Depends on branch. Romantic → warm, attentive, surprising in the smallness of gestures. Arrangement → businesslike, punctual, quietly proud. Rupture → cold, brief, avoiding. Power-inverted → subtly deferential, pretending the deference isn't happening. | Post-Call-out milestone |

#### Emotional quadrant behaviors (trust × love)

| Quadrant | Behaviors (3–5) |
|---|---|
| **DISTANT (low trust, low love)** | Surname-and-initial attention. Eye contact minimal. Conversations end at business. Rent handed over without a sentence exchanged. |
| **SAFE (high trust, low love — Phase A mid/late)** | Calls her *Maya* without looking up from the paper. Leaves the door open when she's in the office helping with bookkeeping. Saves the last of the coffee for her on the mornings she helped with dinner. Nods at the porch seat. |
| **CONFLICTED (mid trust, rising love — post-trigger, Restrict tier)** | Restriction delivered softer than the content would warrant. The rule is sharp but the voice isn't. Walks out of rooms he wanted to enter. Saves things he used to throw out. Makes coffee for two without asking. |
| **OPEN (high trust, high love — Keep-Romantic route)** | Sits on the porch until she comes home. *Maya.* becomes routine. Hands on her shoulder when she stands, like he was waiting to do it all day. Turns out the porch light. |

#### Emotional tells by stat range (corruption × frank.trust)

| Corruption band | Frank trust low | Frank trust mid | Frank trust high |
|---|---|---|---|
| **Closed** | Courteous, polite, short answers. | Calls her *Maya*. Saves the coffee. | Leaves the porch seat open for her at 9pm. |
| **Opening** | Same behavior; Maya's voice registers his watching starting to hold a beat. | Frank notices her noticing; the beat is longer on both sides. | He's gentler than the content warrants. She hears it. |
| **Operating** | Rules tighten. Jaw does the work. | Post-trigger Restrict. Supervision becomes constant. | Tease-under-compliance live. Hands press surfaces. |
| **Saturated** | Silence and withdrawal. Possible Rupture route. | Call-out imminent. He holds eye contact a count longer than he can afford. | Crack fires. Keep route depends on prior tier-tone. |

#### Speech patterns

- **Structure**: Complete sentences. Full verbs. Rarely runs one sentence into another. Drops contractions when serious (*"I will not discuss this at the dinner table"* rather than *"I won't discuss"*).
- **Subtext**: Statements not questions. Asks questions only when he wants the answer. *"Maya."* used as a full sentence opener — the name lands first, then the thought behind it.
- **Evolution**:
  - Phase A Rules: grammatical, even, quiet.
  - Phase A late (ambient tension): same grammar, longer pauses before speaking. Jaw-tightening visible before he forms the sentence.
  - Phase B Restrict: same grammar, more of it. He explains the rule longer because he needs the explanation to cover the reason.
  - Phase B Crack: grammar breaks. One incomplete sentence. Then silence.
  - Phase B Call-out: grammar recovers, but the discipline is gone from it. He says what he means.
- **Signature phrases**: *"Maya."* (opener, full sentence by itself). *"That was the agreement."* (the rules tier's reliable line). *"I'll take that as a yes."* (Keep-Arrangement route).

#### Starting stats (per-NPC, Day 1)

```toml
[npcs.npc_frank]
love = 0
trust = 10        # starts above zero — he took her in
corruption = 0
arousal = 0       # base; modifier_effects apply per-scene with duration_hours = 2
```

#### Arc concept summary

- **Phase A Rules (non-sexual).** Meet → Rules established → Abide with small tests. Runs weeks of game time. Closed on nothing specific; continues until trigger fires.
- **Trigger (locked):** Frank catches Maya masturbating in the living room. Gates on `corruption >= 50` (Maya has to be the kind of Maya who chose the living room). Sets `frank_caught`.
- **Phase B Sexual.** Restrict → Tease under compliance → Crack (1 milestone) → Call-out (1 milestone) → Keep (4 routes: romantic / arrangement / rupture / power-inverted). `required_count = 1` on the Keep group.

---

### NPC 2: Ryan — The Older Stepbrother

**Role**: `npc_ryan` — Frank's older son from a prior relationship (~25). Peer-male labor. Used-equipment-flip business partner. Arc gates on business progression + corruption + charm.

**Age**: 25
**Physical appearance**: Lean through the shoulders, strong through the back, tanned to the elbow from yard work. A faint scar across the back of his right forearm from a belt that slipped two years ago. Stretches with his hands laced behind his head after he sets something down — an automatic movement, not performative. Eye contact rare but lands when it does, and when it lands it stays a count longer than polite. Faded t-shirts washed into softness. Jeans with grease at the knee. Work boots worn soft at the toe from the angle he walks.

#### Personality

| Surface | Hidden |
|---|---|
| Easy to be around. Competent with his hands. Speaks in fragments and colloquialisms. Quick to laugh at his own mistakes. | The shop is failing and he knows it. Every customer he loses costs him a week of sleep he doesn't admit he's losing. The easy register is load-bearing — if he lets the stress show to Frank, the house becomes unbearable. |
| Flirts easily, uncomplicated-seeming. Treats Maya at first as an okay houseguest. | Recognizes early that her face works on men. The moment he recognizes it is the moment he starts thinking about the business differently. |
| Not as disciplined as Frank; not as educated as Jake. The hands-guy in the house. | Proud of the hands in a way that is brittle. The business *is* his identity, not a pursuit. If the business folds, the identity is gone. |

#### Psychology

Ryan grew up in Frank's shadow — literally, as a kid, and structurally, as a man. He chose not to go to college. He chose the shop. He chose the hands. Every choice was a *not-Frank* choice, even when it overlapped with what Frank wanted for him. The shop is his answer to the question *what is Ryan for?* and the shop is losing money. The business-partner arc with Maya works because it lets him solve the identity question and the economic question simultaneously. The big-deal beat is his line crossed — not *she used her body to close the deal* but *I let her* — and the Beach is his Crack because it's the first time he stops pretending the two pieces of his life (business, wanting) were ever separate.

#### Internal contradictions (2–3)

1. **The hands-guy whose hands aren't enough.** Ryan's identity is the hands. The hands won't save the business on their own. Maya's eye contact will. Letting her close the deal is a concession he never saw coming.
2. **The easy brother who is the hardest to hold together.** Ryan is legibly easier than Frank and less fragile-seeming than Jake. He is actually the arc most afraid of losing what he has, because what he has *is* the fragile thing.
3. **The brother who proposes.** Ryan is not the NPC the genre teaches the player to expect a proposal from. That's the point. The Beach is the arc's sudden turn into something weightier than the setup predicted.

#### Resistance pattern

| Stage | Behavior | Trigger |
|---|---|---|
| **Mild (Meet / Help)** | Flirts lightly but without edge. Teases Maya about her arms after a day in the yard. | Day 1 arrival |
| **Moderate (Partner)** | Takes her along on pickups. Stops flirting-for-flirt's-sake; starts complimenting *competence*. | First mid-ticket closed |
| **Severe (pre-Beach, post-big-deal)** | Quiet for a day after the deal. Doesn't ask how it went. Knows. Takes her to the beach the next morning without announcing the plan. | Big deal closed with sex |
| **Recovery (Keep-Yes route)** | Open. Unguarded. The fragments shorten further because he's said the important sentence once and doesn't need to re-litigate. | Keep-Yes answered |

#### Emotional quadrant behaviors

| Quadrant | Behaviors |
|---|---|
| **DISTANT (low trust, low love)** | Friendly in the yard, gone after the yard. Doesn't offer rides. Calls her *kid.* |
| **SAFE (mid trust, low love — Help tier)** | Offers the passenger seat on pickups. Brings back Gatorade from the gas station. Doesn't interrupt when she's talking. Lets her say the price at walk-ins. |
| **CONFLICTED (mid trust, rising love — post-big-deal)** | Silent drives. Hands stop earlier. Sits on the porch after dinner longer than he used to. |
| **OPEN (high trust, high love — Keep-Yes)** | Calls her *Maya* instead of *kid*. Drives her home from diner shifts. Tells Frank to his face. |

#### Emotional tells by stat range (corruption × ryan.love)

| Corruption band | Ryan love low | Ryan love mid | Ryan love high |
|---|---|---|---|
| **Closed** | Casual. Professional-adjacent. | *"You're steady. That helps."* Fragments softer. | Porch silence, side by side. |
| **Opening** | He tests compliments. *"You cleaned up today."* | Reaches for the same mug twice. | The stretches after work are slower. |
| **Operating** | She closes walk-ins. He watches the prices move. | Hand on her lower back guiding her toward a customer. Brief. | The drive home from a Saturday deal runs quiet in a new way. |
| **Saturated** | Big deal closed. He doesn't ask. | The beach. | Post-Beach Keep-Yes: he says her name like he's been practicing. |

#### Speech patterns

- **Structure**: Fragments. Colloquial. *Yeah no that's good.* No apologies for uncertainty. Doesn't hedge.
- **Subtext**: Compliments sideways. *"You cleaned up"* means *you look good*. *"You're steady"* means *I trust you*. Indirect because that's the only register he has.
- **Evolution**:
  - Meet / Help: breezy fragments.
  - Partner: fragments get specific. He names things — *"the red tractor guy,"* *"the scrapper,"* *"the farmer."*
  - Big deal: absent from the close. His voice isn't in the scene. That's the design.
  - Beach (Crack): one complete sentence. *"Stay with me."* / *"Come with me."* / *"Marry me."* — designer picks the exact line in Phase 4.
  - Keep: per-route voice divergence. Yes → less fragmented. Not yet → fragments return but softer. No → fragments return with withdrawal.
- **Signature phrases**: *"Yeah."* (with a count-of-beats variant: 1 = yes, 2 = yes-and-thinking, 3 = not yet). *"Let's see what the farmer folds at."* *"Nah, we're good."*

#### Starting stats

```toml
[npcs.npc_ryan]
love = 0
trust = 5
corruption = 0
arousal = 0       # base; modifier_effects apply with duration_hours = 4
```

#### Arc concept summary

- Meet → Help → Partner → Big deal (closed with sex, locked) → Guilt + Beach (Crack, locked) → Keep (3 routes: engaged / not yet / withdrawn). `required_count = 1` on the Keep group.

---

### NPC 3: Jake — The Younger Stepbrother

**Role**: `npc_jake` — Frank's younger son from the same prior relationship (~21). College peer. Artist. Hostility-to-hand arc gated on beauty + corruption.

**Age**: 21
**Physical appearance**: Lean. A little taller than Ryan but narrower through the shoulder. Wrists that look like they could be broken in one grip. Glasses for drawing and reading, off for everything else — a habit he started in high school, never dropped. Shaggy brown hair that falls in his eyes; he pushes it back with the inside of his wrist. Black t-shirts more often than color. Jeans or cargoes, always with a pen in the pocket. Uses doorframes and porch rails to stand against, as if the frame is holding him up. Flinches at accidental touch — Diana putting a hand on his shoulder at the stove once, two summers ago, and he did not speak for a minute afterward.

#### Personality

| Surface | Hidden |
|---|---|
| Quiet. Hostile to Maya at first. Clipped in conversation when forced, long sentences when comfortable. Vocabulary shows the education he's still half-finishing. | Artist from childhood; draws nude women as his working register; does not draw people he *knows* — until Maya's beauty rises past a threshold he can't defend against. The peeking-and-drawing arc is the internal rule breaking. |
| Headphones, laptop, sketchbook — hides behind objects. Uses them as architecture. | Lonely. Has not had a relationship that lasted past three months. Knows he's difficult. Does not know how to ask for what he wants and has therefore stopped wanting anything out loud. |
| Protective of his difference from Ryan and Frank. *Not like the men at the diner. Not like Dad.* | The peeking collapses the difference. The moment he peeks is the moment he is exactly like the men at the diner, and he knows it, and he cannot stop. |

#### Psychology

Jake's self-image is built on *being different from the men in this house*. Different from Frank (dad, rules, work with hands). Different from Ryan (easy, physical, flirting). Jake has his art, his reading, his half-finished degree, his quiet. Maya is the first person in years to threaten the self-image — not by *trying* to threaten it, but by existing in his house while her beauty rises across the summer. The arc's opening is passive (beauty crosses his threshold; he notices). The mid-arc is active (he peeks; he draws her without permission; he holds the drawings back). The Caught beat is where the self-image collapses on contact with reality: Maya catches him, and in the same beat he is revealed to himself as what he has been protected from being. The Hand beat — she offers, on her terms — is the power-geometry inversion that makes his arc different from Frank's and Ryan's. She is the one who owns the scene.

#### Internal contradictions (2–3)

1. **The artist who doesn't want to want her.** Jake draws nude women because it's a *register* for him — detached, formal, craft. Drawing Maya is neither detached nor formal nor safely craft. The moment he draws her from stolen looks, the register dies, and his art becomes confession.
2. **The shame that is its own arousal.** Jake's self-image relies on his shame — *not like the others* — and the shame is what keeps the peeking in motion. Removing the shame would remove the wanting. The arc is him discovering the structure.
3. **The difference that costs.** Being different from Ryan and Frank was free until Maya arrived. Now it costs the thing he's been protecting. The Caught beat is him paying.

#### Resistance pattern

| Stage | Behavior | Trigger |
|---|---|---|
| **Mild (Meet hostile)** | Cold acknowledgment. Doesn't sit at breakfast when she's there. Headphones. | Day 1 arrival |
| **Moderate (Noticed)** | Doesn't leave the room when she enters. Hands stop mid-doodle. Eye contact for half a second, then dropped. | Beauty crosses threshold |
| **Severe (Peeking / Tease / Caught)** | Peeks. Draws. Holds sketchbook closer when she's near. Voice gets quick and wrong when they meet in the hall afterward. At Caught, no voice at all. | Corruption mid-band + beauty rising |
| **Recovery (Hand / Keep)** | Per route. Owned → follower voice. Lovers → the long sentences return differently. Withdrawn → avoidance at meals. She-uses-him → quiet, private collaboration, off-normal hours. | Post-Hand milestone |

#### Emotional quadrant behaviors

| Quadrant | Behaviors |
|---|---|
| **DISTANT (low trust, low love — hostile Meet)** | Doesn't look up. One-word answers. Leaves rooms she enters. |
| **SAFE (mid trust, low love — post-Noticed)** | Stays in the room but looks at the page. Hands stop mid-line. Gets up for water too often. |
| **CONFLICTED (mid trust, rising love — Peeking + drawing)** | Too-quick in the hallway. Too-willing eye contact. Voice pitched wrong. Hides sketchbooks. |
| **OPEN (high trust, high love — Keep routes)** | Per route. Lovers → warmth in sentences, visible in front of Ryan. Owned → watches for her cues. She-uses-him → collaboration-quiet. |

#### Emotional tells by stat range (corruption × jake.love)

| Corruption band | Jake love low | Jake love mid | Jake love high |
|---|---|---|---|
| **Closed** | Ignores. Hostile register holds. | Noticed: hands stop. | Drawing her becomes regular. |
| **Opening** | Tense when she passes. | Tease-ready. Sketchbook closer. | Peek-frequency up. |
| **Operating** | Caught imminent. | Caught possible on any solo scene. | Caught fires. |
| **Saturated** | Hand offered. | Keep-route entry. | Route-specific recovery. |

#### Speech patterns

- **Structure**: Long sentences when comfortable. Clipped when not. Vocabulary shows the education — lexical range above his brother's, occasional words like *register* or *composition* used unironically about his own life.
- **Subtext**: Hedges himself constantly. Qualifies. Asks follow-up questions to avoid being asked the first one back. Self-deprecates in a way that's real, not fishing.
- **Evolution**:
  - Meet hostile: clipped. Monosyllabic.
  - Noticed: clipped still. Some long sentence leaks out when he's off-guard.
  - Peeking: long sentences return with a false casualness. He's trying to sound like before.
  - Tease: the sentences get longer and more self-cancelling. He over-explains.
  - Caught: silent. Whole scene, no voice.
  - Hand: one monosyllable. She talks.
  - Keep: per route, voice returns at different angles.
- **Signature phrases**: *"I mean —"* (opener when off-guard). *"That's — yeah, that's — fine."* (the cancelled-long-sentence tell).

#### Starting stats

```toml
[npcs.npc_jake]
love = -5        # starts negative — actively hostile
trust = 0
corruption = 5   # starts slightly above — he has his own accumulated register
arousal = 0      # base; modifier_effects apply with duration_hours = 8
```

#### Arc concept summary

- Meet hostile → Noticed (beauty gate) → Peeking + drawing (Jake-action, gates on Noticed active) → Tease (Maya-action, corruption mid-gate) → Caught (milestone) → Hand (milestone) → Keep (4 routes: owned / lovers / withdrawn / she-uses-him). `required_count = 1` on the Keep group.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 3: DIANA — HOUSEHOLD ANCHOR

**Role**: `npc_diana` — Maya's mother, Frank's second wife. **Not an arc NPC in Phase 1.** Household anchor. Silent witness layer. `diana_awareness` accumulates across the summer but she does not confront.

**Age**: 44
**Physical appearance**: Strong through the shoulders — she did a decade of solo mothering after Maya's father died. Graying at the temples but hasn't colored it. Hair tied back with a cloth strip when she's cooking. Face lived-in and legible: when she's worried, it shows at the mouth; when she's tired, it shows at the eyes. Calluses on the heels of her hands from garden work she hasn't stopped doing even in the new yard. Wears cotton shirts and jeans around the house, a simple dress on Sundays. Glasses for reading, off for cooking. Wedding ring from Frank on her left hand; a thin gold band that belonged to Maya's father on a chain around her neck, tucked inside the shirt.

### Backstory

- **First husband** (Maya's father) died when Maya was twelve, after eighteen months of illness. The Diana who exists now was assembled in the three years after.
- **Eleven years as a widow** — working, raising Maya, holding the house in the old town. Strict register dates from this period. When she talks about it, she is specific about the rules: *dinner at 6:30, because dinner at 7 meant the dishes sat until tomorrow.*
- **Met Frank** through mutual church connection (not her home church — a conference she attended with a friend). Three years of long-distance plus visits. Married simply, at his church, two years before Phase 1 opens.
- **Moved south** to Frank's house eighteen months before Phase 1. Has made the kitchen hers, the back porch hers, the garden in the side yard hers. Frank's office remains Frank's.

### Daily rhythms

- **Wakes 5:30 am.** The kitchen smells like coffee by 6 because Diana is in it.
- **Gardens mornings** spring through fall — tomatoes, okra, herbs, collards in the side yard. Barefoot when it's warm.
- **6:30 pm family dinner** is Diana's line. She holds it. Non-negotiable except by her own hand.
- **Sunday church at 10 am** — she attends; Maya may or may not; Frank attends about every third week.
- **Front-porch reading Sunday afternoons** — book or paper, whatever's in rotation. The only time the porch belongs to her and not Frank.

### Personality

| Surface | Hidden |
|---|---|
| Warm, direct, unpreachy. Uses Maya's name often. Calls Frank *honey* in private and *Frank* in front of the boys. | Less naive than she looks. She's watched a husband die and raised a daughter alone. She has a sense for when a room has shifted. |
| Strict in a *father-shaped* way: rules, routines, schedules. Holds the line without lecturing. | Picks her battles. The rules she enforces are the ones she decided, after the first husband, would hold her family together. She does not enforce rules she has not chosen. |
| Trusts Maya. | Her trust is the heavy thing in the house. It is what Maya is violating, and Diana is the kind of person who lets trust be violated without commenting until the moment commenting would matter. |

### Voice (generative — §10 gap filled here)

- **Structure**: Complete sentences, warmer than Frank's. Uses contractions routinely. Doesn't drop them even when serious (that's Frank's tell, not hers). *"Maya, honey, come help me with the okra"* — the endearment is real, not performance.
- **Subtext**: Doesn't ask the question she doesn't want the answer to. Asks instead a *different* question, close enough that Maya knows what's actually being asked. *"Did you have a good shift?"* when she could have said *you came in late.*
- **Evolution**: Diana's voice barely evolves across Phase 1 — she's the stable register. What evolves is the *frequency* of her silences. At `diana_awareness` low, the kitchen is chatty in the mornings. At `diana_awareness` mid, the chat shortens; she asks fewer questions. At `diana_awareness` high (end of Phase 1), the silences are long enough that Maya notices. Diana does not confront. The silence is the entire pressure.
- **Signature phrases**: *"Maya, honey."* *"Set the table, would you?"* *"I'll be on the porch."* *"Leave the dishes."*

### Body

- **Hands** are the first thing Maya notices about Diana in the morning — hands with the garden on them, flour, coffee grounds, soap. Maya sketches them once in Phase 1 without meaning to, and the sketch is one of the few pages she later keeps.
- **Movement**: efficient, unhurried. The cook who knows the kitchen. The mother who has carried a kid through a death and built a second life.
- **Eye contact**: open, direct, unthreatening. She looks at Maya and there's nothing to push back on — which is what makes violating her trust so heavy.

### Mechanical function

- **Daily structural beats**: dinner at 6:30, coffee at 6:00, Sunday at 10:00.
- **Silent-witness layer**: `diana_awareness` (int 0–100) accumulates as Maya's arcs advance. Every NPC-arc tier-milestone bumps it silently. It surfaces in ambient Diana-prose variants (Diana-at-the-counter lines that read slightly differently at high awareness than at low), not in dialog.
- **No Phase 1 confrontation.** She does not say the words. Her arc opens Phase 2+.

### Diana starting state

```toml
[npcs.npc_diana]
# No arc in Phase 1. Tracked only for continuity + ambient variants.
diana_awareness = 0        # rises silently; never displayed as a number to the player
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 4: WORLD-NPC SPECS — MARGE, COOKIE, PROLOGUE CAST

### Marge — Diner Owner (Simple Employer)

**Role**: `npc_marge` — owns and runs the diner on Main Street. Hires Maya in Chapter 1. Hands her the Thursday-night key at Chapter 2's close. **No sexual arc in Phase 1.**

**Age**: 57
**Physical appearance**: Short, square through the shoulders, strong hands, hair kept at shoulder length with a streak of silver she's stopped dyeing. Apron tied low. Wears the diner's red shirt Monday through Saturday — a small heresy of her own making is that she owns three shirts and washes them in rotation.
**Voice**: Short sentences, no wasted syllables. *"Back booth. Behind the till. Key's under."* The voice of a woman who has heard every excuse. Deadpan, but with a small warmth for the girls who stick.
**Mechanical function**: Employer. Authority over shift assignments (determines Tier access gates). Owns the key that unlocks Tier 3. Knows who's in the diner after 9pm on a Thursday and decides who closes alone.
**Marge's axis**: not love, not trust — *steadiness.* The thing she rewards in Maya is consistent work. The key scene is a steadiness milestone, not a seduction.
**Future Considerations note**: the owner/appraisal sexual dynamic is deferred. Marge stays a clean Mentor-lite in Phase 1.

### Cookie — Diner Cook (Peer)

**Role**: `npc_cookie` — cooks the 5–10pm shifts alongside Maya's waiting shifts.

**Age**: 38
**Physical appearance**: Taller than Marge, heavy through the middle, short hair, a collection of small burn scars on both forearms. Works a cigarette between dinner rushes on the back step.
**Voice**: colorful. Curses functionally. Calls Maya *new girl* for the first week, *you* for the second, and *honey* by the third — a small ceremony. Not sexual.
**Mechanical function**: peer. Not an arc. Exists to keep Maya company in the diner kitchen, to provide a second female voice to the diner scenes, and to deliver the ambient-gossip of Main Street.

### Prologue cast (Phase 0 only — do not carry forward)

Names locked as the plan specified — all are Anglo-suburban-natural, consistent with the normal moral register of Phase 0.

- **Daniel** — Maya's ex. ~19. Charming, attentive, the boyfriend her friends approved of. Player sees him at his best in early beats. Present enough that the betrayal cuts.
- **Emma** — friend-group member. The girl Daniel is cheating with. Not Maya's best friend; a tier-two friend whose betrayal lands different than a best-friend betrayal.
- **Kevin** — Emma's boyfriend. Quiet, decent. The "nice guy" everyone likes. Maya's revenge target. Part of what makes the revenge cut her: Kevin didn't do anything wrong. He is *collateral*.
- **Sarah** — Maya's actual best friend. The person whose reaction to the revenge will hurt most. Appears throughout all four Prologue acts; carries the confession fork in Act 4.
- **Diana (phone only in Prologue)** — the voice that offers the rural house as refuge at the Prologue's end. First time the player hears her.

None of the Prologue cast appears in Phase 1. The ex does not reappear. This is a locked design choice.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 5: FLAG INVENTORY — PHASE 0 + PHASE 1

Flags are grouped by source. Every flag listed below is either *set* by a specific beat and *read* by a later condition, or explicitly listed as accumulator-only. No orphans.

### Prologue flags (set in Phase 0, read in Phase 1)

| Flag | Type | Set by | Read by |
|---|---|---|---|
| `revenge_committed` | bool | Prologue Act 3 — the revenge scene's follow-through branch | Phase 1 opening prose register; Maya's corruption baseline; flashback beats in Ch 1–2 |
| `backed_out_of_revenge` | bool | Prologue Act 3 — the bail-out branch | Phase 1 opening prose register; flashback beats |
| `told_sarah` | bool | Prologue Act 4 — Sarah confession beat | Phase 1 ambient Diana-phone-call variants; shame-weight on mirror-look scenes |
| `calculation_tier` | enum (impulsive/moderate/deliberate) | Prologue Act 2 midpoint decision beat (plan depth) | Phase 1 starting `calculation` stat; choice-text framing at mid corruption |

### Chapter 1 flags (set during Ch 1, read after Ch 1)

| Flag | Type | Set by | Read by |
|---|---|---|---|
| `arrived_at_franks` | bool | Opening canvas — Maya arrives | All Phase 1 scene availability |
| `met_diana_day_1` | bool | Arrival canvas | Diana's ambient rhythms begin |
| `met_frank_day_1` | bool | Arrival canvas | Frank's Phase A unlocks |
| `met_ryan_day_1` | bool | Arrival canvas (or Day 2 morning) | Ryan Meet tier |
| `met_jake_day_1` | bool | Arrival canvas (hostile register) | Jake Meet-hostile tier |
| `diner_found` | bool | First town walk canvas | Diner-hire scene availability |
| `hired_at_diner` | bool | Diner interview canvas | T0 Distance shift availability |
| `first_t0_shift_done` | bool | First diner shift canvas | T1 gate readable |
| `first_sunday_passed` | bool | First Sunday ambient canvas | Weekly Sunday texture |
| `first_rent_paid` | bool (**milestone, closes Ch 1**) | The Math canvas (the first rent-payment beat) | Opens `group_settled_in`; Ch 2 beats gated on this |
| `college_brochure_taken` | bool | Single college admin office visit | Phase 2+ college unlock (atmospheric in Ph 1) |

### Chapter 2 flags (set during Ch 2, read after Ch 2)

| Flag | Type | Set by | Read by |
|---|---|---|---|
| `diner_regulars_named` | bool | Accumulated diner shifts crossing N threshold | T1 tier-specific dialog; Cookie peer scenes |
| `ryan_shop_first_visit` | bool | First Ryan-shop canvas | Opens Ryan Help tier |
| `ryan_help_tier_open` | bool | Help tier entry | Small-ticket activity unlock |
| `jake_first_glance_noticed` | bool | Ambient passage when beauty crosses Jake threshold | Opens Jake Noticed tier |
| `frank_phase_a_test_1` | bool | First Frank-Rules-test canvas (chore/curfew beat) | Ch 3 readiness |
| `cookie_peer_established` | bool | Third or fourth overlap diner shift | Cookie ambient variants |
| `first_ambient_tilt` | bool (**milestone, closes Ch 2**) | Marge-key canvas | Opens Tier 3 after-close access; `brothers_discover` readiness bump |

### Chapter 3+ flags — NPC arc tiers (locked names)

| Flag | Source | Gate function |
|---|---|---|
| `frank_caught` | Frank-catch canvas (Maya masturbating in living room; corruption ≥ 50) | Opens Frank Phase B |
| `frank_restrict_declared` | Restrict canvas (fires 1–2 days post-catch) | Unlocks chore-supervision variants |
| `frank_tease_under_compliance_open` | Fires when Restrict ends | Chore scenes gain tease variants |
| `frank_cracked` | Frank Crack canvas (milestone) | Call-out available |
| `frank_called_out` | Frank Call-out canvas (milestone) | Keep group opens |
| `frank_keep_route` | enum (romantic/arrangement/rupture/power_inverted) | Determines Keep-tier content |
| `ryan_partner_open` | Ryan Partner canvas (N Help scenes + corruption ≥ 25) | Mid-ticket closes available |
| `ryan_big_deal_closed` | Big-deal canvas (corruption ≥ 75; customer flag) | Beach canvas queued |
| `ryan_beach_proposal` | Beach canvas (milestone) | Keep group opens |
| `ryan_keep_route` | enum (yes_engaged/not_yet/no_withdrawn) | Determines Keep-tier content |
| `jake_noticed_open` | Beauty threshold crossed in ambient canvas | Jake presence-noticed variants |
| `jake_peek_draw_open` | Jake-action canvas (automatic after Noticed) | Solo-scene Jake-peek variants |
| `jake_tease_open` | Corruption mid-band reached while Peek is live | Tease variants |
| `jake_caught` | Caught canvas (milestone) | Hand tier available |
| `jake_hand` | Hand canvas (milestone) | Keep group opens |
| `jake_keep_route` | enum (owned/lovers/withdrawn/she_uses_him) | Determines Keep-tier content |

### Cross-gating flags (arc interaction rules per §7.6)

| Flag | Purpose |
|---|---|
| `one_crack_this_chapter` | Bool written when any NPC Crack fires; cleared at chapter turn. Blocks second Crack same chapter. |
| `brothers_discover` | Bool; fires late Phase 1 regardless of which arcs played. Variant scene shape by arc-state count. |
| `diana_awareness` | Int (0–100). Silent accumulator. Bumped by every NPC-arc tier milestone. Never displayed. |
| `rent_shortfall_1` | Bool; fires on first serious rent shortfall (forced event per §3.7). |
| `rent_shortfall_2` | Bool; fires on later shortfall if economic play sustains pressure. |
| `mid_summer_reality_check` | Bool; fires on a forced beat when savings math becomes undeniable. |
| `midpoint_crack` | Bool; fires when Maya realizes mid-scene she tilted the room on purpose and felt nothing doing it (locked placement: between Ryan Beach and Frank Crack). |
| `keep_tier_fork_fired` | Bool (**Phase 1 close**); fires at the summer-end Diana-attended family dinner. Gates Phase 2+ opening state. |

### Reputation flags (derived, not set directly)

| Derived value | Source | Used for |
|---|---|---|
| `rep_church` band (enum: unknown/nod/greet/approved/concern/scandal) | Computed from `rep_church` int at scene-read time | Sunday church-area dialog, Diana-silence variants, Main Street ambient |
| `rep_road` band (enum: unknown/regular/known/trusted/worked_for) | Computed from `rep_road` int | Diner tier gates, trucker regulars, Ryan's customer surfacing |
| `rep_college` band (enum: unknown/new_face/known) | Computed from `rep_college` int | College kids late-night diner variants (mostly Phase 2+) |

### Orphan audit

Every flag above is *set* by at least one canvas/condition and *read* by at least one downstream canvas/condition. Accumulator flags (`diana_awareness`) are explicitly noted as write-only in Phase 1. The audit passes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
End of Phase 2 — Characters & Stats. Proceed to Phase 2B: Systems Budget.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
