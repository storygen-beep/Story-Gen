# Corruption Design — The Story of How Innocence Changes

Blueprint for how corruption works as a STORY, not a stat. Companion to `GAME_DESIGN.md` (overall structure) and `media_writing_guide.md` (writing style). This doc covers the WHY behind every corruption gain and how the player's experience evolves across 9 phases.

---

# Section 1: The Problem & Philosophy

## Why Corruption-as-Grind Doesn't Work

The old design: innocent choices give +1 corruption. The hint system shows "How to increase Your Corruption." The player grinds a number to unlock content. Floating in a creek gives corruption. Sitting on a bed gives corruption. Asking a question gives corruption. No story, no WHY, no transformation.

This turns corruption into a chore — click the right buttons, watch the number go up, unlock the next tier. The player is optimizing a stat, not experiencing a character's transformation.

## What Corruption SHOULD Be

Corruption is the story of a 19-year-old girl who arrives innocent and is changed by living in a house with three men who want her. She doesn't choose to be corrupted — the house does it to her. The proximity, the thin walls, the shared bathroom, the economic dependence. Her body responds before her mind decides. Her mind catches up later. Then she starts choosing.

The player should never think "I need to grind corruption." They should think "oh shit, she just heard Jake through the wall" and the +3 corruption is the CONSEQUENCE of what the story showed them.

## The Two-Phase Principle

```
Phase A (corruption 0-40):  IT HAPPENS TO HER
  She doesn't choose corruption. Circumstances create it.
  Random encounters, environmental moments, body betraying mind.
  The player makes SURVIVAL decisions (money, transport, housing).
  Corruption is the side effect.

Phase B (corruption 40+):   SHE STARTS CHOOSING
  She's changed enough to ACT. The testing becomes deliberate.
  Player choices drive corruption now. Outfit selection, flirting,
  physical escalation. Each choice feels EARNED because Phase A
  showed the journey that got her here.
```

## Connection to Game Motivations

**Motivation 3 ("I Earned This"):** Every escalation tier feels deserved because the player SAW the journey. The first handjob hits differently when you read 7 phases of transformation before it.

**Motivation 4 ("They Feel Real"):** NPCs aren't passive — they CAUSE corruption. Jake's drawings, Ryan's boldness, Frank's cracking control. They corrupt her through who they ARE.

**Motivation 6 ("I'm Barely Holding On"):** Economic pressure forces proximity. She needs money → takes jobs in the house → jobs create situations → situations create corruption. The math does it, not the player.

---

# Section 2: The 9 Phases

## Phase 1: INNOCENT (corruption 0-10, Week 1)

### What Happens
She arrives. Hoodie and jeans. One suitcase. The house immediately violates her privacy in ways she can't prevent:
- The bathroom lock doesn't catch. Jake walks in on her. She walks in on Ryan.
- The kitchen is small. Frank's body is unavoidable when they're both cooking.
- Ryan's truck has a bench seat with no center console. 15 minutes pressed against his thigh.
- The walls are thin. She hears things at night she wasn't meant to hear.

### Her Internal State
Uncomfortable. Angry. Wants privacy. Counts the days until Mom returns. Refers to them by role ("my step-dad," "the older one") not by name. Short sentences in her head. Defensive.

### How Activities Read
```
Drawing session: "He asked me to hold still. I held still. His pencil scratches the paper.
                  I don't know where to look."

Truck ride:      "The seat is too small. His leg is right there. I press against the door 
                  and stare out the window."

Cooking:         "He reaches past me for the salt. His arm brushes mine. I step back.
                  He says nothing."

Wall knocking:   "Tap-tap through the wall. I don't know what it means.
                  I don't knock back."
```

### NPC Reactions at This Phase
- **Jake:** Shy. Barely looks at her. Drops things when she enters. Drawing landscapes, not her.
- **Ryan:** Testing. "You own gym clothes or is that just... the look?" Watching her reactions.
- **Frank:** Professional. "Dinner's at six." Doesn't sit when she's in the room.

### Corruption Sources
- Random encounters: bathroom walk-ins, hallway in towel, overhearing sounds
- Environmental: small kitchen proximity, truck bench seat, thin walls
- NOT from player choices — from CIRCUMSTANCES

### Flags
- None yet. She hasn't changed. Things are just happening around her.

---

## Phase 2: CONFUSED (corruption 10-20, Week 2)

### What Happens
The moments she hated during the day come back at night. Uninvited. Her mind replays them — Frank's belt buckle brushing her skin in the kitchen, Ryan's body in the water at the creek, Jake's silence through the wall when she was changing. Each replay is clearer than the real thing. Her body responds. She doesn't understand why.

She doesn't touch herself. Not yet. But she lies awake longer than she should. The warmth between her legs isn't something she asked for. She turns over. Tries to sleep. The warmth stays.

### Her Internal State
Confused. Guilty about the confusion. "What's wrong with me?" She still resists during the day — pushes Ryan's hand away, steps back from Frank, avoids Jake's eyes. But the resistance is half a second slower than last week. She notices the delay. That scares her more than the moments.

### How Activities Read
```
Drawing session: "He's drawing my hands. I watch his face while he works.
                  I didn't used to watch his face.
                  *Why am I watching his face?*"

Truck ride:      "His thigh is right there. Like always. The bump in the road 
                  shifts me closer. I don't shift back immediately.
                  *I used to shift back immediately.*"

Cooking:         "His arm brushes mine reaching for the salt. I don't step back.
                  I stand there for a second. Then step back.
                  *That second. What was that second?*"

Wall knocking:   "Tap-tap. I knock back tonight. I don't know why.
                  Through the wall: 'You up?' His voice is soft.
                  I lie in the dark and listen to him breathe."
```

### NPC Reactions at This Phase
- **Jake:** Starting to draw her hands from memory. Leaves his door cracked when he knows she's in the hall.
- **Ryan:** Noticing her delayed resistance. The grin sharpens. "You're getting used to me."
- **Frank:** Catching himself looking. Over-correcting. Leaving the room faster after contact.

### Corruption Sources
- Activity group block variants: internal thoughts during existing activities shift
- Nighttime processing: replaying moments in bed (inside wall knocking or bedroom scenes)
- Still NOT her choice. Her mind is doing it.

### Flags
- `night_replays_started` — her mind has begun processing

---

## Phase 3: CURIOUS (corruption 20-30, Week 2-3)

### What Happens
She stops fighting the nighttime thoughts. She starts SEEKING answers. Late night, phone under the covers — reading forums, articles, "why does unwanted proximity cause arousal." She finds other content. Not educational. Videos. She watches because she's trying to understand what she's feeling. Somewhere in the middle of "understanding," it becomes something else.

She finds Ryan's browser history on the shared laptop. What he watches. The girls are confident, physical, aggressive. Like him. She closes it. Opens it again. Watches 30 seconds. Closes it for real.

She finds Jake's private sketchbook — not the portfolio, the other one. Drawings of her she didn't pose for. Her in a towel. From behind. The detail is specific.

First time she touches herself — not planned. She's replaying a moment — Ryan's body against hers in the truck — and her hand is already there before she realizes. She stops. Stares at the ceiling. Her hand doesn't move away. She finishes. Feels sick. Feels alive. Both. She doesn't do it again the next night. She does it the night after.

### Her Internal State
The gap between Day Lily and Night Lily is growing. During the day: still normal, still resists, still the girl who arrived with one suitcase. At night: a different person. Processing. Exploring. Discovering what her body wants. The guilt is fading. The curiosity is stronger.

### How Activities Read
```
Drawing session: "Jake's drawing my collarbone. His pencil moves differently 
                  when I'm the subject — slower, more careful.
                  I know what's in his other sketchbook now.
                  He draws me when I'm not looking. He draws me from behind.
                  *I should be angry. I'm not angry. I'm something else.*"

Truck ride:      "Ryan's hand is on the gearshift. Close to my knee. 
                  Last week I pressed against the door.
                  Today I'm sitting in the middle of the bench.
                  I don't know when I stopped pressing against the door."

Wall knocking:   "Tap-tap. I knock back. We talk through the wall.
                  After he says goodnight, I hear him moving. 
                  I know what that sound is now.
                  I lie there. My hand on my stomach.
                  It moves lower. 
                  *Not tonight. ...Tonight.*"
```

### NPC Reactions at This Phase
- **Jake:** Leaving the private sketchbook less hidden. Unconsciously? Or does he want her to find it?
- **Ryan:** Leaving browser history unchecked. Walking around in less. Testing with physical proximity.
- **Frank:** His phone face-down on the counter now. He's aware of what he looks at. He's ashamed. But he hasn't stopped.

### Corruption Sources
- Discovering NPC private content (sketchbook, browser, phone)
- Solo exploration (watching porn, self-pleasure)
- Activity variants with shifting internal thoughts
- The player sees the transformation through the WRITING, not through choices

### Flags
- `found_private_sketches` — discovered Jake's secret drawings
- `found_ryans_browser` — found his browsing history
- `first_self_pleasure` — crossed the private line

---

## Phase 4: TESTING (corruption 30-40, Week 3-4)

### What Happens
Night Lily starts leaking into Day Lily. She creates OPPORTUNITIES for exposure and pretends they're accidents.

She KNOWS the bathroom latch doesn't catch. She used to wedge a towel under the door. She stops wedging the towel. She tells herself she forgot.

She's changing in her room. The door isn't fully closed. She knows Jake's door is open across the hall. She doesn't get up to close her door.

She bends for something in the kitchen. The shirt gaps. She knows it gaps — this shirt always gaps. She wore it anyway.

Each "accident" has plausible deniability. She's not doing anything WRONG. She just stopped being careful. And she checks — every time — whether they looked.

### Her Internal State
Adrenaline. Heart pounding after each "accident." Not from fear — from excitement. She tells herself these are accidents. She knows they're not. The gap between what she tells herself and what she knows is where the corruption lives.

### How Activities Read
```
Drawing session: "The strap slips off my shoulder. I could fix it.
                  I watch his pencil stop. Count to five.
                  One. Two. Three. Four. Five.
                  I fix it.
                  Those five seconds were for him. And for me."

Cleaning:        "On my knees scrubbing the floor. The shorts ride up.
                  The door is open. I hear footsteps in the hallway.
                  I don't pull the shorts down.
                  The footsteps slow. Then continue.
                  *Who was that? Did they see?*
                  I keep scrubbing. My heart is pounding."

Cooking:         "I reach for the top shelf. My shirt rides up.
                  Bare lower back. I can feel him behind me.
                  He doesn't step back fast enough.
                  I feel the buckle of his belt. Cold metal. Warm skin.
                  One second. Both freeze.
                  I grab the dish. Step away. Normal.
                  *Nothing happened. Nothing happened.*"

Wall knocking:   "I change with the door open tonight.
                  Not fully open. Cracked. Enough.
                  Through the wall: Jake's pencil stops.
                  He heard me moving. He knows I'm changing.
                  I take my time."
```

### NPC Reactions at This Phase
- **Jake:** His drawings of her are getting more detailed. The "accidental" poses she creates end up in his sketchbook. He's drawing what she shows him.
- **Ryan:** "You should be more careful walking around like that." Said with the grin. He's noticed the change. He approves.
- **Frank:** "Put something on before your brothers see you." The command. He's telling her what to wear — acknowledging he SAW. His jaw is tight when he says it.

### Corruption Sources
- Activity group block variants: the "accidental" exposure moments woven into existing activities
- NPC reactions to her testing feed back as corruption (his RESPONSE to her "accident" thrills her)
- Still mostly passive from the player — the variants fire automatically based on corruption level
- Some early CHOICES appear: "Fix the strap" vs "Leave it" — small, deniable

### Flags
- `left_door_unlocked` — first deliberate test
- `exposure_unlock` fires near the end of this phase

---

## Phase 5: TEASING (corruption 40-55, Week 4-5)

### What Happens
She drops the pretense. The "accidents" become DELIBERATE. She dresses for their reactions. She holds eye contact. She makes comments with double meanings. She ENJOYS the attention instead of being embarrassed by it.

The tank top instead of the hoodie — every day now. The short shorts for cleaning. Crossing and uncrossing her legs on the couch while Ryan watches. Leaning over the desk during bookkeeping while Frank pretends to read numbers.

She's not testing anymore. She's PLAYING.

### Her Internal State
Confident. Playful. A new kind of power she's never felt before — the power of being wanted. Three men under one roof, and she controls what they see, when they see it, how much they see. The innocent girl who arrived with one suitcase is becoming someone who picks her wardrobe based on which man she wants to destroy today.

Night Lily and Day Lily are the same person now.

### How Activities Read
```
Drawing session: "I chose this top because of the neckline. He knows it.
                  I know he knows it. Neither of us says anything.
                  'Can you turn toward the light?'
                  I turn. Slowly. Let him see what the light does.
                  His pencil moves faster."

Truck ride:      "I sit in the middle of the bench. My thigh against his.
                  I don't pretend it's the road. I lean into him on the turns.
                  'You're doing that on purpose.'
                  'Doing what?'
                  The grin. Mine. Not his."

Bookkeeping:     "I put the pen down. Look at him. Don't say anything.
                  He feels me looking. His pen slows. Stops.
                  The clock ticks.
                  'Something wrong with the numbers?'
                  *I'm not looking at the numbers, Frank. 
                  You know I'm not looking at the numbers.*"

Cooking:         "I reach past him for the skillet. My arm crosses his chest.
                  Our faces six inches apart. I don't need the skillet.
                  He knows I don't need the skillet.
                  Neither of us moves for three seconds."
```

### NPC Reactions at This Phase
- **Jake:** Stops stammering. Starts asking her to "hold that pose." The art is the excuse. His eyes are the truth.
- **Ryan:** Comments become suggestions. "You should wear that to the creek." Finds excuses to touch — adjusting her gym form, brushing past in the hallway.
- **Frank:** The control is visibly cracking. Sentences start and stop. "You should—" Pause. "Never mind." Pours whiskey earlier. Grips the coffee mug tighter.

### Corruption Sources
- PLAYER CHOICES now drive corruption. The hub menu has flirt options.
- Outfit-driven corruption (choosing bold clothing for NPC reactions)
- NPC reactions feeding back (their boldness in response to her teasing = more corruption)

### Flags
- `flirt_unlock` fires in this phase
- `dressed_for_them` — first deliberate wardrobe choice
- Bookkeeping offer unlocks (corruption ≥ 40)

---

## Phase 6: EXPOSING (corruption 55-70, Week 5-6)

### What Happens
Teasing wasn't enough. She wants them to see MORE. The escalation from "look at my neckline" to "look at my body" is driven by the power she discovered in Phase 5 — and the hunger for more of it.

No bra under the tank top. She knows what that looks like. She checks in the mirror. Goes to breakfast.

Short skirt. No panties underneath. She sits on the couch next to Ryan. Crosses her legs. He can't see anything. But she KNOWS. The knowledge makes everything electric.

The towel "slips" in the hallway. Not all the way. Just enough. She doesn't rush to fix it.

### Her Internal State
Thrilling. Addictive. The secret of what she's wearing (or not wearing) underneath is a drug. She walks through the house knowing she's one wrong movement from being exposed — and that "wrong" movement is starting to feel like the right one.

She touches herself every night now. Not with guilt. With purpose.

### How Activities Read
```
Drawing session: "No bra today. He noticed in the first thirty seconds.
                  The pencil hasn't stopped shaking since.
                  'The light is different today.'
                  The light isn't different. My shirt is thinner.
                  He knows. I know he knows. He draws faster."

Creek swimming:  "The swimsuit is from the Cute tier. The one that shows 
                  everything without showing anything.
                  He's in the water. I'm on the bank. Standing.
                  I let him look. I don't get in yet.
                  Making him wait IS the point."

Truck ride:      "The skirt rides up. I don't pull it down.
                  His eyes drop. Come back up. Drop again.
                  'That's... a new look.'
                  'Is it?'
                  I shift in the seat. The skirt rides higher.
                  He grips the steering wheel."

Late night:      "Sleep shirt. Just the sleep shirt. Nothing underneath.
                  I walk to the kitchen. Past Jake's door. Past Ryan's door.
                  The floor is cold. The shirt is short.
                  Frank is at the table. He looks up. His eyes drop to 
                  the hem. Then back to her face. Then back to the hem.
                  'Can't sleep?'
                  'Can't sleep.'"
```

### NPC Reactions at This Phase
- **Jake:** Drawing her body now, not just her face. The poses in his private sketchbook match what she's been showing him. He's bolder about positioning her — "Turn this way. Drop the shoulder."
- **Ryan:** Touching her. Brief. "Accidental." His hand on her lower back guiding her through a door. His fingers on her waist at the gym. Each touch lingers a second longer than the last.
- **Frank:** Breaking rules he set. Staying in rooms he should leave. The commands are strained — "Put something on" said while his eyes are still on her legs. He hates himself for looking. He can't stop looking.

### Corruption Sources
- Wardrobe choices (no bra, short skirt, sleep shirt, no panties)
- Player-driven exposure in activity choices
- NPC reactions escalating in response (their touch, their boldness)

### Flags
- `tease_unlock` fires in this phase
- `comfortable_braless` — can go without bra
- `discovered_teasing` — the power of deliberate exposure

---

## Phase 7: TOUCHING (corruption 70-90, Week 6-7)

### What Happens
Looking and showing wasn't enough. She wants to FEEL. The first time she touches a man with intent — not accidental brush, not proximity. Her hand on his thigh. Moving higher. Finding him hard. Feeling his reaction in her hand.

The handjob isn't a "scene that unlocks." It's the moment she crosses from visual to physical. From showing to touching. And feeling him respond — his breath catching, his body tensing, the sound he makes — is its own kind of power.

### Her Internal State
Hungry. Bold. The girl who was mortified by a bathroom walk-in is now the girl who puts her hand on a man's thigh during bookkeeping. She doesn't recognize herself. She doesn't want the old self back.

After the first time — she looks at her hand. The hand that just did THAT. She washes it. Then smells it. Then feels insane. Then wants to do it again.

### How Activities Read
```
Drawing session: "'Come here.'
                  He sets the pencil down. Crosses the room.
                  His glasses bump my forehead. I close the gap.
                  The kiss is graphite and sweet coffee. His hand on my jaw.
                  My hand finds his belt. He freezes.
                  'Is this okay?'
                  He nods. Can't speak. His glasses are fogging."

Truck ride:      "He pulled over. Engine off. Gravel.
                  His hand was on the gearshift. My hand covers his.
                  Moves it. Higher.
                  'Fuck.' One word. All breath.
                  I grip him. Firm. Fast. His hand slams the ceiling.
                  The windshield fogs from the inside."

Bookkeeping:     "Under the desk. The ledger is still open.
                  I found him through the fabric. Then the zipper.
                  He didn't stop me. That's how I know the dam broke.
                  His jaw clenches. He won't make a sound.
                  Control. Even now.
                  The pen in his other hand hasn't moved in three minutes."
```

### NPC Reactions at This Phase
- **Jake:** Overwhelmed. Trembling. Quiet. "I drew you a hundred times. This is better." He clings to her after.
- **Ryan:** Aggressive. Vocal. "Fuck." His hand finds her neck. Not pushing — holding on. "Your turn?"
- **Frank:** Rigid control even during the act. Jaw clenched. Won't make a sound. After: "Page forty-two." Like nothing happened. Except his hand is shaking.

### Corruption Sources
- Player-driven escalation choices in hub menus (kiss, then handjob options)
- NPC reactions to physical contact (their vulnerability/aggression = more corruption)
- Each NPC's version is unique — three different experiences of the same escalation

### Flags
- `kiss_unlock` fires early in this phase
- `handjob_unlock` fires later
- These are earned through NPC relationship stats + corruption level

---

## Phase 8: TASTING (corruption 90-120, Week 7-8)

### What Happens
She's touched them. Now she wants MORE. The decision to go lower — to kneel — is the most deliberate sexual choice she's made. This isn't accidental. This isn't testing. This is her choosing, with full knowledge, to put her mouth on a man.

The power dynamic is complex — she's on her knees, physically below him, but she's in COMPLETE control. He's helpless. She could stop any time. She doesn't.

### Her Internal State
Confident. Sexual. She knows what she wants and she knows how to get it. The innocence isn't gone — it's evolved into something else. She's not a corrupted innocent. She's a woman who discovered desire and chose to follow it.

### How Activities Read
```
Drawing session: "I slide off the edge of his bed. Kneel by his chair.
                  His eyes go wide behind the glasses.
                  'You don't have to—'
                  I do. His hand finds my hair. Not pushing. 
                  Just resting. Like he needs to hold something 
                  or he'll float away."

Truck ride:      "He leans the seat back. The grin is gone — replaced 
                  by something hungrier.
                  'You sure?'
                  I don't answer. The bench seat is wide enough.
                  His hand finds the back of my neck. 
                  His other hand grips the steering wheel 
                  like he's driving through a storm."

Late night:      "I slide from my chair. Under the kitchen table.
                  The wood is cold against my knees.
                  He looks down. Disbelief. Then something darker.
                  He won't make a sound — the boys are upstairs.
                  His knuckles on the table are white.
                  The whiskey glass trembles."
```

### NPC Reactions at This Phase
- **Jake:** Pulls her up after. Into the chair with him. It's not built for two. Neither cares. "I love you." No hedging.
- **Ryan:** The cocky grin is gone. Just Ryan. Undone. For the first time, he's silent. When she looks up, his eyes are closed.
- **Frank:** His eyes close. Just for a moment. Opens them. Looks at her. Says nothing. Zips himself. Picks up the pen. "Page forty-two." She's never felt more powerful.

### Corruption Sources
- Player-driven escalation in hub menus (oral options gated by blowjob_unlock)
- The act itself is a major corruption milestone
- NPC vulnerability during the act (seeing them undone = power = corruption)

### Flags
- `blowjob_unlock` fires in this phase

---

## Phase 9: GIVING (corruption 120-160, Week 8+)

### What Happens
Full intimacy. Not just a sex scene — the moment she gives herself completely. The decision that this is happening. No more half-measures. No more "just touching" or "just tasting." This is everything.

And it's DIFFERENT with each NPC because they're different people:

**With Jake:** Slow. Tender. He's shaking. "Is this okay?" asked three times. Glasses on the nightstand. The narrow bed creaks. Through the wall — Ryan's room. Neither cares. He traces her collarbone afterward with his fingertip. The same line he's drawn a hundred times. But this time it's real.

**With Ryan:** Fast. Confident. Truck pulled over on the back roads, or the creek bank, or against the workshop wall. He takes charge but she matches him. The pine air freshener swings. "Finally," he says. Like he's been waiting since Day 1. He has.

**With Frank:** Devastating. The control breaks COMPLETELY. Years of restraint gone in one moment. He lifts her onto the desk. Invoices scatter. The ledger falls. He doesn't care about the ledger for the first time in his life. He's not gentle. He's not rough. He's Frank — controlled even as control shatters. After: he picks up every invoice. Straightens the ledger. "Same time Wednesday?" His hands are still shaking.

### Her Internal State
Complete. Not "corrupted" — TRANSFORMED. She started as a girl with one suitcase. She's now a woman who has chosen, with open eyes, to be intimate with her step-family. There's no taking it back. The corruption isn't about sex — it's about crossing a line that CANNOT be uncrossed. And she doesn't want to uncross it.

### Corruption Sources
- Player-driven. Full escalation choices in hub menus.
- The act with each NPC. Each one is unique content.
- Post-act processing (the aftermath, how it changes the household dynamic)

### Flags
- `sex_unlock` fires in this phase
- The game continues — this isn't the end, it's the beginning of a new dynamic

---

# Section 3: Corruption Sources By Phase

| Phase | Primary Source | Player Agency | Example |
|-------|--------------|---------------|---------|
| 1. Innocent | Random encounters | NONE — things happen TO her | Bathroom walk-in |
| 2. Confused | Activity variants (internal thoughts) | NONE — her mind does it | Nighttime replays in bed |
| 3. Curious | Discovery + solo exploration | MINIMAL — seeks answers | Finds sketchbook, watches porn, first touch |
| 4. Testing | Activity variants (behavior shifts) | LOW — "accidents" she doesn't prevent | Leaves door unlocked, shirt gaps |
| 5. Teasing | Player choices (flirt, outfit) | MEDIUM — deliberate teasing | Chooses tank top, holds eye contact |
| 6. Exposing | Player choices (wardrobe, exposure) | MEDIUM-HIGH — deliberate showing | No bra, no panties, towel "slip" |
| 7. Touching | Player choices (escalation) | HIGH — initiates physical contact | Handjob, first real touch |
| 8. Tasting | Player choices (escalation) | HIGH — chooses to kneel | Oral, power + submission |
| 9. Giving | Player choices (escalation) | FULL — complete intimacy | Sex, different with each NPC |

**The key pattern:** Player agency INCREASES as corruption increases. Early phases are passive (things happen). Late phases are active (she chooses). The transition from passive to active IS the corruption story.

---

# Section 4: NPC Reaction Tiers

Each NPC has their own corruption track. Their reactions to Lily depend on THEIR corruption level — which rises from exposure to her transformation.

## Jake's Reaction Evolution

| NPC Corruption | Behavior | Triggered By |
|---------------|----------|-------------|
| 0-5 | Shy. Drops things. Draws landscapes. | Baseline |
| 6-12 | Draws her hands. Leaves door cracked. Pencil moves differently when she's in the room. | Her regular visits |
| 13-20 | Private sketchbook has her in it. Positions her during drawing — "Turn this way." | Her Phase 4 testing |
| 21-28 | Stops stammering. "Don't move." Silent intensity. Drawing her body, not face. | Her Phase 5-6 teasing/exposing |
| 29-35 | Possessive. "Don't wear Ryan's hoodie." "Were you in Dad's office?" The shy boy has teeth. | Her Phase 7+ physical escalation |
| 36+ | "I drew you again. I always draw you." Complete devotion. The art and the desire are the same thing. | Full intimacy |

## Ryan's Reaction Evolution

| NPC Corruption | Behavior | Triggered By |
|---------------|----------|-------------|
| 10-15 | Comments. "You own gym clothes or..." Testing with words. The grin. | Baseline (starts higher) |
| 16-22 | Touches. Hand on lower back. Fingers on waist at gym. Brief. "Accidental." | Her Phase 4-5 testing/teasing |
| 23-28 | Grabs. Pulls her close passing in hallway. "Looking good, roomie." Not hiding it. | Her Phase 5-6 teasing/exposing |
| 29-35 | Confronts. "You're doing this on purpose." Not angry — excited. Wants her to admit it. | Her Phase 6-7 exposing/touching |
| 36-40 | Initiates. Doesn't wait for her. Hand on her thigh in the truck without asking. "Tell me to stop." | Her Phase 7+ |
| 41+ | "I mean it." The bravado drops. Real. Protective. Still aggressive but underneath — vulnerable. | Full intimacy |

## Frank's Reaction Evolution

| NPC Corruption | Behavior | Triggered By |
|---------------|----------|-------------|
| 0-5 | Looks away. Leaves the room. Over-formal. "Diana's daughter." | Baseline |
| 6-10 | Catches himself looking. Overcorrects — leaves room too fast. Adds house rules. | Her Phase 3-4 curiosity/testing |
| 11-18 | Commands that reveal awareness. "Put something on." The command IS the intimacy. | Her Phase 5 teasing |
| 19-25 | Sentences start and stop. "You should—" Pause. "Never mind." Pours whiskey earlier. | Her Phase 5-6 teasing/exposing |
| 26-30 | The dam cracks. Doesn't leave the room. Holds eye contact. "Lily." Just her name. Low voice. | Her Phase 6-7 exposing/touching |
| 31+ | "Stay." The control shatters. Not gradually — completely. Iron discipline to "lock the door" in one scene. | Full intimacy |

---

# Section 5: Activity Variant Map

How key activities READ at different corruption phases. Same canvas, same game mechanic — different group block content.

## Drawing Session (Jake's Room)

| Phase | Content Variant |
|-------|----------------|
| 1 (Innocent) | She holds still. Doesn't know where to look. He draws silently. Awkward. |
| 3 (Curious) | She watches his face. Notices his pencil moves differently for her. Finds the private sketchbook. |
| 4 (Testing) | The strap "slips." She counts to five before fixing it. His pencil stops. |
| 5 (Teasing) | She chose this top for the neckline. They both know it. "Can you turn toward the light?" |
| 6 (Exposing) | No bra. Thin shirt. His pencil hasn't stopped shaking in thirty seconds. |
| 7+ (Touching) | Escalation hub options appear. Kiss, handjob, oral, sex — each gated by unlock flags. |

## Truck Ride (Ryan's Truck)

| Phase | Content Variant |
|-------|----------------|
| 1 (Innocent) | Pressed against the door. Staring out the window. His leg is too close. |
| 2 (Confused) | Still by the door. But aware of his thigh. Aware of the vibration. |
| 4 (Testing) | Sitting in the middle of the bench. Not the door. "Accidentally." |
| 5 (Teasing) | Leaning into him on turns. "You're doing that on purpose." "Doing what?" |
| 6 (Exposing) | The skirt rides up. She doesn't pull it down. His eyes drop. |
| 7+ (Touching) | "Pull over." Escalation hub options. |

## Bookkeeping (Frank's Office)

| Phase | Content Variant |
|-------|----------------|
| 2 (Confused) | Professional. Numbers. His hand on the desk three inches from hers. |
| 4 (Testing) | She puts the pen down. Looks at him. Says nothing. He feels her looking. |
| 5 (Teasing) | "I'm not looking at the numbers, Frank." The silence is louder than words. |
| 6 (Exposing) | Leans over the desk. The shirt gaps. He sees. Doesn't look away. |
| 7+ (Touching) | "Reach past him for the ledger." Escalation hub options. |

## Wall Knocking (Lily's Room)

| Phase | Content Variant |
|-------|----------------|
| 1 (Innocent) | Tap-tap. She doesn't know what it means. Doesn't knock back. |
| 2 (Confused) | Knocks back. They talk through the wall. She listens to him breathe after. |
| 3 (Curious) | After goodnight, she hears him. Knows what the sound is. Hand on stomach. Moving lower. |
| 5 (Teasing) | Changes with the door cracked. Knowing he can hear. Taking her time. |
| 7+ (Touching) | Opens his door instead of knocking. Escalation hub options. |

---

# Section 6: Random Encounters Inventory

Passive corruption events that fire based on location + chance + corruption phase. The player doesn't choose these — they happen during normal activities.

## Bathroom Encounters
- **Ryan shower walk-in** (Phase 1): She opens the door. He's naked. Towel on the floor. She slams the door. +3 corruption.
- **Jake bathroom collision** (Phase 1): Mirror shows everything when door opens. He's shirtless. Toothbrush in mouth. +2 corruption.
- **Her towel slip** (Phase 4): Walking to her room. Towel loosens. She catches it — but not before the hallway saw. +2 corruption.

## Wall/Sound Encounters
- **Hearing Jake at night** (Phase 2): Through the wall. Rhythmic sound. She realizes what he's doing. +3 corruption.
- **Hearing her name** (Phase 3): Through the wall. He says her name. Quiet. During. +5 corruption.
- **Sounds from Ryan's room** (Phase 3): Different sounds. A video playing. She can hear what he watches through the door. +2 corruption.

## Discovery Encounters
- **Jake's private sketchbook** (Phase 3): His other sketchbook. Open on the desk. Her in a towel. From behind. +3 corruption.
- **Frank's phone** (Phase 3): Kitchen counter at 2 AM. Screen still on. A woman her age. He closed it fast. +4 corruption.
- **Ryan's browser history** (Phase 3): Shared laptop. His search history. The girls look like her. +3 corruption.
- **Frank's magazines** (Phase 4): Workshop drawer. Hidden under tools. Old but well-worn. +2 corruption.

## Proximity Encounters
- **Kitchen belt buckle** (Phase 2): She reaches up. He's behind her. Belt buckle brushes bare skin. One second. Both freeze. +2 corruption.
- **Truck bump** (Phase 2): Road bump shifts her into him. Full body contact for a second. He doesn't adjust. +2 corruption.
- **Gym spotting** (Phase 4): Ryan adjusting her form. Hands on waist. His chest against her back. "Like this." +2 corruption.
- **Ryan's groping** (Phase 5, NPC corruption high): Passing in hallway. His hand brushes her ass. "Sorry." He's not sorry. +3 corruption.

---

# Section 7: Solo/Nighttime Moments

These are NOT separate canvases. They're group block variants inside existing nighttime activities (wall knocking, sleep, journal) that evolve with corruption phase.

## Inside Wall Knocking Activity

| Phase | Post-Knocking Internal Thought |
|-------|-------------------------------|
| 2 | *Through the wall: silence now. But I'm still awake. Why am I still awake? The warmth won't go away.* |
| 3 | *After he says goodnight, I hear him. I know what that sound is. I lie here. My hand on my stomach. It doesn't move lower. ...It moves lower.* |
| 4 | *I changed with the door cracked tonight. I heard his pencil stop through the wall. He heard me. He knows. I'm under the covers now and I'm thinking about him knowing.* |
| 5 | *I don't need the wall anymore. I need him. But for now — this. My hand. His name in my head. The taste of something I haven't had yet.* |

## Porn Discovery Progression

| Phase | What She Finds/Watches |
|-------|----------------------|
| 3 (early) | Forums. Articles. "Why does proximity cause arousal." Educational. Clinical. |
| 3 (mid) | Ryan's browser history. What HE watches. The girls are aggressive. Like him. 30 seconds. Closes it. |
| 3 (late) | Her own searches. Her phone. Under the covers. Not educational anymore. |
| 4 | Specific content. Matching what she's feeling. Step-family. Forbidden. She watches with her hand between her legs. |
| 5 | Doesn't need the phone anymore. The real thing is down the hall. |

## Self-Pleasure Milestones

| Phase | Milestone |
|-------|-----------|
| 3 (first) | Not planned. Hand was already there. Finishes. Feels sick. Feels alive. |
| 3 (second) | Next night she doesn't. Night after she does. The guilt is fainter. |
| 4 | Regular. Nightly. Thinking about specific moments — belt buckle, truck vibration, Jake's silence. |
| 5 | No guilt. With purpose. Thinking about specific NPCs. What would happen if she went to his room right now. |
| 6 | Thinking about what she DID today — the no-bra moment, Frank's eyes on her legs, Ryan's hand on her waist. Replaying HER power. |
| 7+ | Thinking about what she WILL do tomorrow. Planning. Anticipating. The self-pleasure is rehearsal. |

---

# Section 8: Flag & Gate Mapping

## Phase Transition Flags

| Flag | Set By | Gates |
|------|--------|-------|
| `night_replays_started` | Phase 2 auto (days elapsed + exposure encounters) | Phase 3 content variants |
| `found_private_sketches` | Random encounter in Jake's room | Phase 3 progression |
| `found_ryans_browser` | Random encounter on shared laptop | Phase 3 progression |
| `first_self_pleasure` | Phase 3 nighttime variant | Phase 4 content shift |
| `left_door_unlocked` | Phase 4 activity variant | Phase 4-5 transition |
| `exposure_unlock` | Phase 4-5 (corruption ≥ 25 + testing flags) | Flirt choices appear |
| `dressed_for_them` | Phase 5 wardrobe choice | NPC reaction escalation |
| `flirt_unlock` | Phase 5 first deliberate flirt | Tease options appear |
| `tease_unlock` | Phase 6 first tease choice | Physical escalation options |
| `comfortable_braless` | Phase 6 wardrobe milestone | Clothing freedom |
| `discovered_teasing` | Phase 6 deliberate exposure | NPC groping reactions |
| `kiss_unlock` | Phase 7 first kiss | Handjob options appear |
| `handjob_unlock` | Phase 7 first handjob | Oral options appear |
| `blowjob_unlock` | Phase 8 first oral | Sex options appear |
| `sex_unlock` | Phase 9 first sex | Full intimacy available |

## Escalation Threshold Table (Source of Truth)

Every escalation tier requires: corruption threshold + NPC relationship stat + NPC-specific player stat + previous unlock flag.

```
TIER         CORRUPTION   JAKE                     RYAN                     FRANK
─────────────────────────────────────────────────────────────────────────────────────────
exposure     ≥ 25         jake_love ≥ 8             ryan_love ≥ 8            frank_trust ≥ 10
                          beauty ≥ 25               fitness ≥ 25             intelligence ≥ 20

flirt        ≥ 40         jake_love ≥ 12            ryan_love ≥ 12           frank_love ≥ 12
                          exposure_unlock            exposure_unlock           exposure_unlock

tease        ≥ 55         jake_love ≥ 15            ryan_trust ≥ 15          frank_trust ≥ 18
                          flirt_unlock               flirt_unlock              flirt_unlock

kiss         ≥ 70         jake_love ≥ 18            ryan_love ≥ 15           frank_love ≥ 20
                          jake_trust ≥ 15           ryan_trust ≥ 12          frank_trust ≥ 20
                          beauty ≥ 35               confidence ≥ 25          corruption ≥ 70
                          tease_unlock               tease_unlock              tease_unlock

handjob      ≥ 85         jake_love ≥ 22            ryan_love ≥ 20           frank_love ≥ 25
                          beauty ≥ 40               fitness ≥ 35             frank_trust ≥ 22
                          kiss_unlock                kiss_unlock              intelligence ≥ 30
                                                                              kiss_unlock

blowjob      ≥ 100        jake_love ≥ 28            ryan_love ≥ 25           frank_love ≥ 28
                          beauty ≥ 40               fitness ≥ 35             handjob_unlock
                          handjob_unlock             handjob_unlock

sex          ≥ 120        jake_love ≥ 32            ryan_love ≥ 28           frank_love ≥ 30
                          jake_trust ≥ 25           fitness ≥ 40             frank_trust ≥ 28
                          beauty ≥ 45               confidence ≥ 30          intelligence ≥ 35
                          blowjob_unlock             blowjob_unlock           blowjob_unlock
```

## Removing Corruption From Innocent Choices

These have been fixed — no longer give corruption:

| Activity | Choice | Currently | Should Be |
|----------|--------|-----------|-----------|
| Creek (Jake) | "Float on her back" | corruption +1 | love +1 (peaceful moment) |
| TV Couch | "Let knee touch his" | corruption +1 | love +1 (proximity comfort) |
| Wall Knocking | "Sit on his bed" | corruption +1 | trust +1 (entering his space) |
| Late Night Frank | "Ask the question" | corruption +1 | love +1 (emotional intimacy) |
| Drawing Session | "Sign the drawing" | corruption +1 | love +1 (artistic connection) |

**Corruption should ONLY come from:**
- Random encounters (Phase 1-3, passive)
- Activity variants where something sexual happens (Phase 2-4, automatic)
- Deliberate player choices involving flirting, exposing, or escalation (Phase 5+)
- Never from innocent interactions like floating, sitting, or asking questions

---

# Section 9: Connection to Existing Systems

## Economic Pressure → Corruption

The money problem doesn't directly raise corruption. But it forces PROXIMITY that creates corruption opportunities:

```
Can't afford bus → depends on Ryan's truck → 15 min pressed against his body → body responds
Needs money → cleaning job → on her knees scrubbing → NPC walks past → random encounter
Needs more money → bookkeeping with Frank → locked office → proximity → tension
Can't afford gym → uses property creek → swimming → bodies in water → exposure
```

The player makes ECONOMIC decisions. Corruption is the SIDE EFFECT of those economic decisions forcing her into intimate proximity.

## NPC Relationships → Corruption

NPC love/trust stats and corruption stats are SEPARATE tracks that REINFORCE each other:

- Building love with Jake (drawing sessions, wall knocking) → more time in his space → more exposure to his obsessive watching → corruption rises from HIS behavior
- Building trust with Frank (bookkeeping, cooking) → more time alone with him → more proximity → corruption rises from the TENSION
- Building trust with Ryan (truck rides, gym) → more physical contact → corruption rises from CONTACT

The player invests in NPC relationships for the relationship rewards. Corruption comes along for the ride.

## The 5 Permanent Forks

The corruption phase affects HOW forks play out:

- **Fork 1 (Ryan's truck, Day ~10):** At Phase 2, the hand on her knee is UNWANTED. Resisting is natural. At Phase 4+, it's anticipated.
- **Fork 2 (Jake's sketches, Day ~25):** At Phase 3, she's just discovered his private drawings. Her reaction depends on whether she's found them BEFORE through random encounters.
- **Fork 3 (Frank's secret, Day ~35):** The financial intimacy layers onto the physical tension. Knowing his debt makes the power dynamic more complex.
- **Fork 4 (Brothers discover, Day ~42):** By this point she's in Phase 6-7. She's not innocent anymore. Her response to being caught depends on whether she's been teasing or hiding.

## Story Beats

The existing 25 story beats interact with corruption phases:

- **Beat 7 (First Awareness):** This IS Phase 4-5 transition. The awareness moment is the story's version of what corruption has been building.
- **Beat 14 (First Kiss):** This IS Phase 7. The kiss is earned through phases 1-6.
- **Beat 18 (Physical Escalation):** This IS Phase 7-8. The handjob milestone.
- **Beat 21 (Brothers Discover):** This hits during Phase 7-9. The household knows what she's become.

The corruption phases don't ADD story beats — they provide the CONTEXT that makes existing beats feel earned.

---

# Companion Documents

- `GAME_DESIGN.md` — Overall game structure (locations, stats, economy, forks, activities)
- `media_writing_guide.md` — Writing style, NPC voices, content tiers, media pairing
- `prompts/game_design_motivations.md` — 6 motivations driving game feel
- `book_phases/2_characters_and_stats.md` — NPC personalities, emotional tells, resistance patterns
