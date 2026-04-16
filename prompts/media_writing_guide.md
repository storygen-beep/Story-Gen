# Content Writing Guide — How Under One Roof Should Read

Complete reference for writing all game content: narration, dialogue, choices, scenes, media pairing. This is the HOW IT READS companion to GAME_DESIGN.md (WHAT HAPPENS) and activity_types.md (HOW IT'S STRUCTURED).

---

# Part 1: Narration & Voice

## Perspective

**Third person with first-person internal thoughts.** The narration describes what happens. Lily's internal voice interrupts in italics or direct thought.

```
Kitchen. Frank is at the stove, sleeves rolled. The smell of garlic
and something burning slightly.

She watches his forearms. The way the tendons move when he stirs.

*Stop looking at his arms.*

"Dinner's in ten." He doesn't turn around.
```

**Why this works:** Third person keeps the player WATCHING Lily (they're directing her). First-person thoughts let them FEEL what she feels. The shift between them creates intimacy without locking into pure first person.

## Paragraph Length

**Short. 1-3 sentences per paragraph block.** Never a wall of text.

The game is played on screens. Long paragraphs feel like homework. Short punchy blocks feel like MOMENTS — each one lands, the player clicks, the next one hits.

**Too long (bad):**
```
She walked into the kitchen and saw Frank at the stove. He was cooking
dinner like he always did, wearing his flannel with the sleeves rolled
up. The kitchen smelled like garlic and there was something burning
slightly on the back burner. She noticed how his forearms looked in
the light from the window and felt a strange flutter in her stomach
that she tried to ignore. He didn't turn around when she came in, but
she knew he'd heard her footsteps on the hardwood floor.
```

**Right length (good):**
```
Kitchen. Frank at the stove. Sleeves rolled.

Garlic and something burning. He doesn't turn around.

She watches his forearms longer than she should.
```

Same scene. One-third the words. Three times the impact. Each paragraph is a beat — the player processes one before the next arrives.

## Sentence Structure

**Vary wildly.** Short fragments. Then a longer sentence that stretches. Then a fragment again. Never let two paragraphs have the same rhythm.

```
His hand on the desk. Three inches from hers.

Neither of them moves it and the clock ticks and the ledger page
is still open to receivables but nobody is reading numbers anymore.

Coffee. His. Black. Getting cold.
```

Fragment → long flowing → staccato list. The rhythm IS the tension.

## Tense

**Present tense for action. Past tense for reflection.**

```
She sits down. He pours her coffee.              ← present: happening NOW
She'd never liked black coffee before this house. ← past: reflection
He slides the mug across. Their fingers almost touch. ← present: back to action
```

---

# Part 2: Lily's Internal Voice

Lily's thoughts evolve across 7 emotional phases. This is the most important writing element — it's what makes the player FEEL progression even when mechanics haven't changed.

## Phase 1: OUTSIDER (Day 1, corruption 0-15)

**Voice:** Short. Observational. Detached. Counting things — exits, rules, days.
**What she notices:** Layout, rules, distances, awkwardness.
**Pronouns for NPCs:** Roles, not names. "My step-dad." "The older one." "The quiet one."

```
The hallway is narrow. His room is right next to mine.

The walls are thin. I can hear his pencil through the plaster.

Fifty-six days. I can do fifty-six days.
```

## Phase 2: SETTLING (Week 1+, corruption 15-40)

**Voice:** Relaxing. Starting to notice routines. Using names now.
**What she notices:** NPC habits, patterns, personality traits.

```
Frank makes coffee at five. I can hear the grinder through the floor.

Jake hums when he draws. Something with no melody. It's nice, actually.

Ryan leaves his boots by the door. Always the same spot. Like a dog
marking territory.
```

## Phase 3: AWARE (exposure_unlock, corruption 40-70)

**Voice:** Physically charged. She's noticing BODIES now, not just habits. Self-conscious.
**What she notices:** Forearms, shoulders, how shirts sit, the bathroom steam, proximity.

```
Ryan came back from the job site shirtless. Sweat on his collarbone.

I looked for three seconds too long. He noticed.

*When did I start counting seconds?*
```

## Phase 4: WANTING (kiss_unlock, corruption 70-120)

**Voice:** Anticipatory. She's not just noticing — she's SEEKING. Admitting desire.
**What she notices:** What she wants to happen, not just what does happen.

```
Jake's door is cracked open. Light spilling into the hallway.

I could knock. I want to knock.

My hand is already raised.
```

## Phase 5: TORN (crisis events, corruption 120-160)

**Voice:** Contradictory. Guilt + desire in the same breath. Longest internal passages.
**What she notices:** Consequences. What she'd lose. What she's already lost.

```
If Frank finds out about Jake, he'll call Mom.

If Ryan finds out about Frank, I don't know what happens.

*I need to stop. I can't stop. I don't want to stop.*
```

## Phase 6: COMMITTED (crisis_resolved, corruption 160-200)

**Voice:** Direct. Unapologetic. Short sentences — certainty doesn't need explanation.
**What she notices:** The relationships themselves. Shared history. Identity.

```
Jake's hand shakes when he draws me now. It didn't used to.

I know exactly when it started.
```

## Phase 7: ENDGAME (mom_returning, corruption 200+)

**Voice:** Urgent. Every sentence weighted. Present tense only. No past, no future — just now.
**What she notices:** Time. Finality. Who she's become.

```
Three more days. She'll walk through that door.

What will she see? Who am I now?

*Does it matter? I chose this.*
```

---

# Part 3: NPC Dialogue Voices

Each NPC must be identifiable WITHOUT a name tag. If you can swap the speaker and it still works, the dialogue is too generic.

## Jake — The Stammerer Who Finds His Voice

**Early Jake (love 0-15):** Incomplete sentences. Trails off. Hedges. Can't finish a thought when she's looking at him.

```
"I was thinking maybe we could—" He adjusts his glasses. "—if you're
not busy. I mean, it's not—"

"It's just anatomy practice. The hands are—" He slams the sketchbook
shut. "It's nothing."

"We shouldn't." (The protest that never holds.)
```

**Mid Jake (love 15-25):** More articulate alone with her. Full sentences. The stammer returns when she surprises him.

```
"Your hands are harder to draw than anything. They never stay still."

"I've been working on something. Do you want to see?"
He holds it out. His hand is shaking. Not the drawing — the act
of showing.
```

**Late Jake (love 25+):** Simple. Complete. Direct. The boy who couldn't finish a sentence found his ending.

```
"I love you." No hedging. No trailing off.

"I drew you again. I always draw you."

"Don't go to his room tonight." (chose_possessive_jake variant)
```

**Jake's signature phrases:**
- "I was just—" (caught)
- "Can I draw you?" (the invitation)
- "We shouldn't." (the protest)
- "I drew you again." (the truth)

**Jake NEVER says:** "fuck", crude sexual terms, one-liners, jokes. He doesn't deflect with humor — he deflects with art.

## Ryan — The Guy Who Talks Like a Dare

**Early Ryan (trust 0-10):** Every sentence is a test. Questions are weapons. Nicknames instead of her name.

```
"You coming or what?"

"Bet you can't name three songs on this station."

"You own gym clothes or is that just... the look?" He grins.
The grin is doing all the work.

"Relax. I'm just messing with you." (He's not.)
```

**Mid Ryan (trust 10-20):** Less performing. Real stories slip through the bravado. Still teases — but the edge softens.

```
"You're alright, you know that?"

"The scar? That's—" The funny version starts, then stops.
"I was scared. First time on a real site. Slipped. Bled everywhere."
He rolls the window down. "Whatever."

"Jake's real busy drawing lately." (He's watching. He's competitive.)
```

**Late Ryan (trust 20+):** The bravado drops. Fewer words. Each one heavier. He stops asking questions and starts making statements.

```
"I don't want to go home yet." (The most vulnerable thing he's said.)

"Come with me." Not a dare. Not a game.

"I mean it." Two words. No grin. No deflection.
```

**Ryan's signature phrases:**
- "You coming or what?" (invitations as challenges)
- "Relax." (when HE needs to relax)
- "Whatever." (his armor word)
- "Not really my sister." (the license he uses, then questions)

**Ryan NEVER says:** "I was thinking maybe..." (that's Jake), anything formal (that's Frank), anything poetic. He doesn't analyze feelings — he acts them out.

## Frank — The Man Who Says Everything By Saying Nothing

**Early Frank (trust 0-12):** Commands. Logistics. Subject-verb-done. No warmth.

```
"Dinner's at six."

"Clean up when you're finished."

"I'll drive you." (Means: I want to be the one who takes you.)
```

**Mid Frank (trust 12-22):** Sentences start and stop. The arrival of "..." in his dialogue. Unfinished thoughts.

```
"You should—" Pause. "Never mind."

"That's enough for tonight." (Means: if we stay in this room one more
minute I'm going to do something I can't take back.)

"Diana trusts me." He says it to the coffee mug. Not to her.
```

**Late Frank (trust 22+):** Fewer words. Each one costs something. When he finally says what he means, it's devastating.

```
"Stay." One word. An opening.

"Lil." First time he's used a nickname. He catches himself.
Then does it again.

"I know what I am." His voice is low. Not loud — low.
"I know what this makes me."
```

**Frank's signature phrases:**
- "That's enough." (boundaries)
- "I said I'll handle it." (control)
- "Sit down." (the door opening)
- "Diana trusts me." (the guilt)

**Frank NEVER says:** incomplete sentences with hedges (that's Jake), one-liners or jokes (that's Ryan), anything longer than necessary. Frank speaks in declarations, not conversations.

**The subtext rule:** Almost everything Frank says means something else. Write the surface line, then know what it REALLY means. The player should feel the gap.

---

# Part 4: Choice Text Writing

Choices are how the player ACTS. They must feel like decisions, not menu items.

## Choice Voice by Phase

| Phase | Tone | Example |
|-------|------|---------|
| OUTSIDER | Cautious, polite | "Offer to help with dishes" / "Go to your room" |
| SETTLING | Friendly, practical | "Ask Jake about his drawings" / "Study on your own" |
| AWARE | Charged, risk-aware | "Hold the pose a little longer" / "Cover up" |
| WANTING | Direct, desire-forward | "Kiss him back" / "Pull away" |
| TORN | High-stakes, emotional | "Tell him the truth" / "Lie" |
| COMMITTED | Confident, initiating | "Go to his room tonight" / "Sleep alone" |
| ENDGAME | Urgent, defining | "One last night together" / "Start saying goodbye" |

## Choice Writing Rules

**1. Choices are actions, not descriptions.**
- Bad: "Feel nervous about the situation"
- Good: "Walk away"

**2. Both options should be genuinely tempting.**
- Bad: "Help him" / "Be mean for no reason"
- Good: "Help him lift it" / "Keep sweeping" (one costs effort, other is safe — both reasonable)

**3. The cost should be visible in the choice text.**
- Bad: "Flirt with him"
- Good: "Flirt with him — Frank is right there" (the risk is IN the choice)

**4. Higher-tier choices use fewer words.**
- Tier 1: "Ask him about his day and see if he wants company"
- Tier 6: "Stay."

**5. NPC-specific choice framing:**
- Jake choices: quiet, incremental. "Lower the strap" / "Hold still" / "Look away"
- Ryan choices: bold, direct. "Match his energy" / "Back down" / "Raise the stakes"
- Frank choices: loaded, subtext. "Stay professional" / "Let the silence stretch" / "Say what you mean, Frank"

---

# Part 5: Scene Structure & Pacing

## Scene Length by Type

| Scene Type | Paragraph Blocks | Why |
|-----------|-----------------|-----|
| Solo activity | 2-3 | Quick. Do the thing. Get the stat. |
| Task (working) | 3-5 | Arrive, work, one moment, done. |
| Hangout (menu) | 2-3 per node | Hub is brief. Selected option has 2-3 blocks. |
| Chain (depth) | 3-5 per node | Each level deeper: setup, tension, choice. |
| Story beat | 5-8 | The longest content. This is where writing shines. |
| Escalation (kiss) | 3-5 | Approach, moment, aftermath. |
| Escalation (sex) | 8-12 | Full scene. Multiple beats. Aftermath mandatory. |

## Scene Beat Structure

Every scene with an NPC follows this rhythm:

```
BEAT 1: SETTING (1 paragraph)
  Where are we? What's the sensory landscape? What's the NPC doing?
  "Kitchen. Frank at the stove. Sleeves rolled. Garlic."

BEAT 2: OBSERVATION (1-2 paragraphs)
  What does Lily notice? Internal thought. Physical detail.
  "She watches his forearms. *Stop looking at his arms.*"

BEAT 3: INTERACTION (1-2 paragraphs + dialogue)
  Something happens. NPC speaks. The dynamic is established.
  "'Dinner's in ten.' He doesn't turn around."

BEAT 4: CHOICE
  Player decides. The choice should emerge from the interaction.
  → "Pick up the knife" / "Set the table instead"

BEAT 5: CONSEQUENCE (1-2 paragraphs, in the next node or trigger)
  What their choice meant. NPC reaction. Stat effects happen here.
```

## Sensory Grounding

Every scene MUST open with at least 2 senses. NOT just visual.

| Sense | How To Use It | Example |
|-------|--------------|---------|
| **Smell** | The most intimate sense. Grounds the reader immediately. | "Sawdust and black coffee." "Graphite and clean laundry." "Cologne over sweat." |
| **Sound** | Creates the world beyond what's visible. | "His pencil scratching the paper." "The truck engine ticking as it cools." "Her footsteps on the hardwood." |
| **Touch/Texture** | Physical grounding. Temperature. Surface. | "The oak desk under her palm." "Cold kitchen tiles on bare feet." "His calloused hand." |
| **Visual** | Specific details, not general descriptions. | "Crow's feet around dark eyes." NOT "He was handsome." "Graphite-stained fingertips." NOT "His hands." |
| **Taste** | Rare but powerful. Save for kiss scenes and meals. | "He tastes like the gum he chews when he's nervous." "Cold coffee. She drank it anyway." |

**The opening line test:** If the first line of a scene could be in ANY room with ANY character, it's too generic. "Kitchen. Frank at the stove. Sleeves rolled." — that's THIS kitchen, THIS man, THIS moment.

---

# Part 6: Group Block Variants

Group blocks show different text based on conditions (flags, stats). This is how the game REMEMBERS and REACTS.

## How to Write Variants

Each variant should change the EMOTIONAL TEXTURE, not just swap a few words.

**Bad variant writing (just word swaps):**
```
[default] "Jake is drawing. He looks up and smiles."
[jake_heard_ryan] "Jake is drawing. He looks up and smiles, but it seems forced."
```
The variant adds "but it seems forced." That's lazy. Same scene with a disclaimer.

**Good variant writing (different emotional reality):**
```
[default]
"Jake is drawing. Afternoon light. He looks up when she walks in.
The smile is automatic — like his face decided before his brain caught up."

[jake_heard_ryan]
"Jake is drawing. The lines are sharper today. Angular.
He doesn't look up when she walks in. His pencil doesn't stop.

'You were up late.' Not a question."
```

The whole SCENE is different. Different physical description (sharp lines vs afternoon light), different NPC behavior (doesn't look up vs automatic smile), different dialogue ("You were up late" vs welcoming silence). The variant changes the EXPERIENCE, not just a word.

## What Triggers Variants

| Flag Type | What Changes | Example |
|-----------|-------------|---------|
| **Cross-NPC awareness** (jake_heard_ryan) | NPC's mood, body language, dialogue | Jake: sharp drawing, pointed questions |
| **Branch flags** (chose_tender_jake) | Relationship tone, escalation style | Tender: collaborative posing. Possessive: silent, intense. |
| **Phase flags** (ryan_resisted vs ryan_allowed) | NPC's approach, choice framing | Resisted: verbal seduction. Allowed: physical directness. |
| **Crisis flags** (frank_found_drawings) | Household atmosphere, NPC availability | Cold dinners, closed doors, formal names. |

## Variant Writing Rules

1. **The default variant should work if no flags are set.** First playthrough = default.
2. **Each variant should be a COMPLETE paragraph, not a patch.** Don't write "He smiles [if flag: but sadly]." Write two separate complete blocks.
3. **Variants should be noticeable.** If the player can't tell the difference, the variant isn't doing its job.
4. **Cross-NPC variants should feel ORGANIC.** Jake doesn't say "I heard you with Ryan." He says "You were up late." The player connects the dots.

---

# Part 7: Content Tier Escalation

How explicit the text gets at each escalation tier. This is the WRITING guide, not the design guide — focuses on word choice, detail level, and character voice.

## Tier 1: Exposure / Awareness (corruption 0-50)

**What to describe:** What she NOTICES. Not what she does. External observation.
**Detail level:** Indirect. Body parts referenced but not explicitly. "His forearms." "The way the towel sits."
**Internal voice:** Anxious. Questioning. Self-conscious.
**NPC awareness:** They might notice her looking. They might not.

```
The bathroom door wasn't locked. It never locks.

Jake standing at the sink. Shirtless. Toothbrush in his mouth.
He freezes. She freezes.

His chest is narrower than she expected. A line of hair below
his navel that she follows down before catching herself.

He spits toothpaste. "Morning." Like nothing happened.

*Something happened.*
```

## Tier 2: Flirt / Tease (corruption 50-90)

**What to describe:** Deliberate small crossings. She CHOOSES to do something charged.
**Detail level:** Contact described — hand on arm, leg against leg, breath on neck. But the contact is brief and can be excused.
**Internal voice:** Anticipatory. "I know what I'm doing."
**NPC awareness:** They definitely notice. And react.

```
She reaches past him for the skillet. Her arm crosses his chest.
Their faces six inches apart.

She doesn't need the skillet.

He knows she doesn't need the skillet.

Neither of them moves for three seconds.

"Excuse me." She takes the skillet. Steps back. Her pulse is
in her throat.

He turns back to the stove. His grip on the spatula has changed.
```

## Tier 3: Kiss (corruption 70-120)

**What to describe:** The full sensory experience. Taste, texture, temperature, sound. Who initiates. The moment just before.
**Detail level:** Explicit about the kiss itself. What his mouth feels like. What her hands do. Where their bodies are.
**Internal voice:** Present tense. In the moment. Thought fragments.
**Aftermath:** MANDATORY. What happens right after changes everything.

**Jake version:**
```
His pencil stops. He's looking at her mouth.

"Jake." She says his name like a question.

He leans forward. Careful. His glasses bump her forehead and he
pulls back, embarrassed — then she closes the gap.

His mouth is soft. He tastes like graphite and coffee. His hand
finds her jaw, holds it like he's positioning a portrait.

The sketchbook slides off his lap. Neither of them picks it up.

He pulls back. Eyes wide behind the glasses. Breathing through
his mouth.

"We shouldn't have—"

"Jake."

"...Yeah."

"Shut up."

She kisses him again.
```

**Ryan version:**
```
He pulls the truck over. Gravel under the tires.

"What are you—"

He kisses her. No preamble. No approach. One hand behind her neck,
pulling her across the bench seat.

He tastes like mint gum and adrenaline. His stubble scrapes her chin.
She grabs his collar — the truck lurches because his foot slipped
off the brake.

He pulls back with the grin. "Took you long enough."

Her heart is slamming. "I didn't do anything."

"You've been doing something since you moved in."
```

**Frank version:**
```
2 AM. Kitchen. The whiskey is doing what the whiskey does.

His hand is on the table. She puts hers next to it. Their pinkies
overlap by a millimeter.

"Lily." His voice is a warning.

"Frank."

He closes his eyes. Opens them. Looks at her mouth.

"This can't happen."

"I know."

He kisses her like a man drowning. Controlled, even now — but the
control costs everything he has. His hand grips the back of the
chair, not her. He's holding the furniture because if he holds her
he won't stop.

He pulls back. Stands up. The chair scrapes the floor.

"Good night." He leaves the kitchen.

His coffee is still warm. She drinks it. It tastes like him.
```

## Tier 4: Handjob / Manual (corruption 100-160)

**What to describe:** The act itself — through CHARACTER lens. Not clinical anatomy. Not generic erotica. THIS person doing THIS thing in THIS specific moment.
**Detail level:** Explicit. What she does with her hand. What he does with his body. Physical reactions — breathing, sounds, muscle tension. Specific.
**Internal voice:** Desire + awareness. She knows what she's doing. She chose this.
**Character differentiation:** Each NPC reacts completely differently. Same act, three different scenes.

**Jake:** Overwhelmed. Trembling. Quiet. The glasses fog. He holds on to her like he'll fall.
**Ryan:** Aggressive. His hand on the ceiling of the truck. "Fuck." One word. All breath.
**Frank:** Controlled. Jaw clenched. Won't make a sound. The pen hasn't moved in three minutes. When it's over: "Page forty-two." She's never felt more powerful.

## Tier 5: Oral (corruption 140-180)

**What to describe:** Position, action, power dynamics. Who initiates. Who's in control. The physical reality of it — not a euphemism.
**Detail level:** More explicit than Tier 4. Anatomical terms used (not clinical, not crude — character-appropriate). Physical descriptions of the act, pace, reactions.
**Internal voice:** Confident. She knows what she wants and why.
**Character differentiation:** Who's giving, who's receiving, and what that MEANS for the power dynamic.

**Key:** Oral scenes should make the POWER DYNAMIC explicit. Who kneels? Who decides? Is this an act of service, of control, of desire? The act itself is secondary to what it reveals about the relationship.

## Tier 6: Sex (corruption 180+)

**What to describe:** Full scene. The longest content in the game. Undressing, first contact, the act, pace changes, climax, aftermath.
**Detail level:** Most explicit. Nothing faded to black. Positions described. Physical sensations. Sounds. Bodies.
**Internal voice:** Deep. Identity-level. "This is who I am now."
**Scene structure:**

```
1. APPROACH (1-2 paragraphs)
   How they get here. The last moment before clothes come off.
   This should feel INEVITABLE — the whole game led to this.

2. UNDRESSING (1-2 paragraphs)
   Specific. Not "they undressed." WHO removes WHAT. The order matters.
   Jake: she undresses him because he can't move. His hands shake.
   Ryan: he undresses her. Fast. "This comes off."
   Frank: they undress themselves. Professional. Then they look at each other.

3. FIRST CONTACT (1-2 paragraphs)
   Skin on skin for the first time. The most charged moment.
   Specific body parts. Temperature. Texture. Sound.

4. THE ACT (2-3 paragraphs)
   Positions. Pace. What changes midway through.
   Character voice throughout — Jake whispers, Ryan groans, Frank is silent.
   Physical detail grounded in sensation, not choreography.

5. CLIMAX (1 paragraph)
   Brief. Specific. Character-true.
   Jake: quiet shudder, forehead on her shoulder.
   Ryan: loud, unashamed, pulls her closer.
   Frank: eyes close for one second. Opens them. Looks at her. Says nothing.

6. AFTERMATH (2-3 paragraphs)
   THE MOST IMPORTANT PART. What happens after reveals what it meant.
   Who speaks first? What do they say? Does he hold her or leave?
   Jake: holds on. Whispers. Draws her from memory the next day.
   Ryan: grins. "Your turn." Or: silence. Something changed in him.
   Frank: gets up. Dresses. "This can't happen again." (It will.)
```

---

# Part 8: Media Pairing

## The Text-Media-Text Sandwich

**Text does the SPECIFIC work. Media does the MOOD work.**

```
BEFORE MEDIA (paragraph):
  Character-specific detail. Internal thought. Sensory grounding.
  Can be hyper-specific — no media needs to match this text.

MEDIA (image/video):
  Matches ACTION + SETTING + PEOPLE + CLOTHING STATE.
  Delivers the visual FEELING. Broad match, not exact.

AFTER MEDIA (paragraph):
  Reaction. Aftermath. What it means. Character voice.
```

**Rule:** Don't describe what the media shows. Text BEFORE = approach. Media = moment. Text AFTER = reaction.

## The 6 Media Dimensions (Priority Order)

| # | Dimension | Priority | Match Requirement |
|---|-----------|----------|-------------------|
| 1 | **Action** | CRITICAL | What's physically happening MUST match |
| 2 | **Setting** | CRITICAL | Background location MUST be recognizable |
| 3 | **People** | IMPORTANT | Count + gender MUST match. Age/body SHOULD match |
| 4 | **Clothing** | IMPORTANT | Clothing level MUST match escalation tier |
| 5 | **Energy** | FLEXIBLE | NPC personality SHOULD show. Wrong energy > wrong setting |
| 6 | **Framing** | FLEXIBLE | Nice-to-have. Don't reject good clips over angle |

## Media Search Queries

**Keep simple. 4-5 words. Action + setting + people + energy.**

Good: "couple kissing kitchen tender"
Good: "woman yoga mat morning"
Good: "man drawing woman portrait"
Bad: "shy boy with glasses drawing dark-haired girl collarbone afternoon light"

## Media Density by Tier

| Tier | Media Per Node |
|------|---------------|
| Casual / Talk | 1 image (setting shot) |
| Flirt / Tease | 1 image or short clip |
| Kiss | 1 clip |
| Handjob / Oral | 1-2 clips |
| Sex | 2-3 clips (marking energy shifts) |

---

# Part 9: What to Avoid

## AI Slop Phrases (banned)

Never use these. They appear in every AI-generated romance scene. They mean nothing.

- "Heart pounding" / "heart racing" / "pulse quickening"
- "Electricity" / "electric" / "sparks flew"
- "Drunk on" / "intoxicated by"
- "Claimed her mouth" / "explored her body" / "mapped her curves"
- "Waves of pleasure" / "shudder of ecstasy"
- "Their bodies intertwined" / "two became one"
- "She moaned his name"
- "A dance as old as time"
- "Desire pooled" / "heat coiled" / "need built"
- "He growled" (people don't growl)

## Generic → Specific Replacements

| Generic (ban) | Specific (use instead) |
|--------------|----------------------|
| "He was handsome" | "Crow's feet around dark eyes. Salt-and-pepper stubble." |
| "She was nervous" | "Her hand missed the mug handle twice." |
| "He was aroused" | "He's hard already. Has been since the creek." |
| "She touched him" | "Her thumb traces the vein along the underside." |
| "It felt good" | "His jaw clenches. He won't make a sound." |
| "She moaned" | "A sound she didn't plan. Low. Almost a word." |
| "He was big" | "Her hand barely closes around him." |
| "They finished" | "He comes quietly — a shudder, his forehead on her shoulder." |
| "The tension was thick" | (Just write the scene. If it's tense, the reader will feel it.) |
| "Their eyes met" | "He looks up. She doesn't look away. Neither does he." |

## Fade-to-Black at High Tiers

**Don't.** At Tier 4+, the player invested 20+ visits and made specific right choices. Cutting away is a cheat. The scene happens on screen — filtered through character voice, not as generic pornography.

## Wrong NPC Voice

If you can swap the NPC name and the dialogue still works, rewrite it.

- Jake NEVER says "fuck" or crude one-liners
- Ryan NEVER stammers or trails off
- Frank NEVER uses more words than necessary
- Jake deflects with art. Ryan deflects with jokes. Frank deflects with authority.

---

# Part 10: Full Scene Examples

## Example: Jake Drawing Session (Tier 2-3, love 15, beauty 35)

```
[paragraph]
Jake's room. Afternoon light through the window. He's been working
for twenty minutes. The scratch of charcoal on paper.

[paragraph]
She's sitting on the edge of his bed. Holding still. He asked her to
hold still ten minutes ago and she hasn't moved since. Her neck aches.

[paragraph]
"Your collar is casting a shadow. Can you—" He gestures at her neckline.

[image: woman posing while man draws, bedroom, afternoon light]

[paragraph]
She pulls the collar to one side. Her collarbone exposed.

[paragraph]
His pencil stops.

[paragraph]
Three seconds. He's looking at her collarbone, her neck, the shadow
line. Not as an artist. As a boy who just realized what he's been
feeling isn't just artistic admiration.

[paragraph]
His pencil starts again. Faster. He doesn't ask her to fix the collar.
```

**Why this works:** Sensory opening (sound of charcoal). Physical grounding (neck aches). NPC voice ("Your collar is casting a shadow" — Jake talks about art, not her body). Media placed at the ACTION moment (posing). Text after = the shift. The player feels it without anyone saying "I'm attracted to you."

## Example: Frank Late-Night Kitchen (Tier 3, trust 22, corruption 110)

```
[paragraph]
Kitchen. Past midnight. She came down for water.

[paragraph]
He's at the table. Whiskey. Lamp light. The glass is already poured
for her. He knew she'd come down.

[dialog speaker="npc" npcId="npc_frank"]
"Can't sleep."

[paragraph]
Not a question. A diagnosis.

[paragraph]
She sits across from him. The whiskey burns. He watches her drink it.

[dialog speaker="npc" npcId="npc_frank"]
"Diana called today."

[paragraph]
His thumb traces the rim of his glass. Round and round.

[dialog speaker="npc" npcId="npc_frank"]
"She asked if you were settling in. I said yes."

[paragraph]
*What else did you tell her? What else didn't you tell her?*

[paragraph]
The clock ticks. The kitchen is dark except for the lamp. His face
is half shadow. The lines around his eyes are deeper at night.

[image: older man and young woman kitchen night whiskey intimate]

[dialog speaker="npc" npcId="npc_frank"]
"You should go to bed."

[paragraph]
He means it. He also doesn't mean it. She can hear both.
```

**Why this works:** Setting established in 5 words. The pre-poured glass = he was waiting (show don't tell). Dialog is PURE Frank — short, declarative, loaded with subtext. Internal thought is brief (one line). Media placed at the mood peak, not at an action. The final line captures the Frank experience: everything means two things.

---

## Companion Documents

- `GAME_DESIGN.md` — WHAT happens (mechanics, stats, forks, endings)
- `game_design_motivations.md` — WHY it works (design philosophy)
- `activity_types.md` — HOW activities are structured (Solo/Task/Hangout/Chain/Scene)
- `game_design_rules.md` — RULES for TOML generation
- This document — HOW it reads (writing style, voices, media, escalation)
