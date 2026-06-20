===============================================================================
                         PHASE 4: STORY EVENTS
===============================================================================

Design all one-time narrative events that drive the story forward.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## DRAMATIC STRUCTURE

### Step 1: Central Tension

**"Can two people who have always loved each other choose that love when choosing
it means destroying everything else?"**

This is NOT "will they hook up" — the progression system handles that. The central
tension is whether love is worth the cost: a shattered engagement, a divided family,
a fiancée who did nothing wrong, and the permanent label of "the people who did
that terrible thing."

Every story event either raises or lowers the odds of the answer being YES.

### Step 2: Primary Conflict

**Type**: INTERNAL CRISIS (Ethan's war with himself) + TICKING CLOCK (14 days)

- **What is the threat?** Ethan's guilt and sense of duty. He will default to
  marrying Madison unless the player gives him both the emotional courage and
  the permission to break free.
- **When does it first appear?** Act 1 (foreshadowed — Madison's things in his room,
  the engagement photo). Act 2 (peaks — Madison Calls, The Real Talk).
- **How does the player resolve it?** By building both affection (proving the love is
  real) AND boldness (giving him permission via her own courage). Low guilt is required
  because if Ethan is too wracked with guilt, love alone isn't enough.
- **What does resolution cost?** Every ending has a cost. Even the "best" ending
  (He Chooses You) means: Madison is devastated, the family is fractured, and they
  begin a relationship under a cloud of scandal. There is no cost-free path.

### Step 3: Tension Curve

| # | Event | Tension | Direction | Why |
|---|-------|---------|-----------|-----|
| 1 | Arrival | — | neutral | Establishing. "I'm here for the wedding." |
| 2 | Welcome Dinner | ↑ | rising | Warmth, he remembers, first cracks in denial |
| 3 | Old Photos | ↑↑ | rising | First spark — shared past made physical |
| 4 | Sleepless Night | ↑↑ | rising | Vulnerability, proximity, darkness |
| 5 | Madison Calls | ↓ | FALLING | Reality intrudes. Guilt spike. She's real. |
| 6 | Rainy Day | — | BRIDGE | Honest conversation, no escalation, character depth |
| 7 | The Couch | ↑↑ | rising | Physical proximity, blanket, hands |
| 8 | Confession | ↑↑↑ | peak | The secret is spoken. No going back. |
| 9 | Almost Kiss | ↑ then ↓ | BRIDGE | Near-miss. Frustration. Unresolved tension. |
| 10 | The Real Talk | ↓↓ | CRISIS | Ethan breaks down. "I don't know if I can do this." |
| 11 | First Kiss | ↑↑↑ | recovery peak | The line is crossed. Post-crisis breakthrough. |
| 12 | What Are We Doing | ↑ | stabilizing | Morning after kiss. Acknowledging. |
| 13 | First Night | ↑↑↑↑ | climax | Turning point. Full intimacy. |
| 14 | Morning After | ↑ then ↓ | REGRESSION | Tenderness → guilt spike. "What have we done." |
| 15 | Can't Stay Away | ↑↑ | rising | Addiction. He comes back despite guilt. |
| 16 | Madison Arrives | ↓↓↓ | CRISIS #2 | Reality crash. She's real and she's here. |
| 17 | Stolen Moment | ↑↑ | desperate | Forbidden encounter with Madison in the house |
| 18 | Night Before Wedding | ↑↑↑ | final peak | Last chance. Raw. Everything on the line. |
| 19 | Wedding Morning | → | resolution | Stat-determined ending fires |

**Shape**: The curve rises through Act 1, dips at Madison Calls, rises sharply through
Confession, crashes at The Real Talk (MAJOR CRISIS), recovers through First Kiss,
peaks at First Night, dips at Morning After (guilt regression), rises through
desperation, crashes again at Madison Arrives (ACT 3 CRISIS), then resolves.
Two-valley heartbeat pattern — not a straight line up.

### Step 4: Regression Events

**REGRESSION 1: "Madison Calls" (Event #5)**
- **Trigger**: After sleepless_night_complete, affection >= 30
- **The Drop**: Ethan guilt +5-8. Player boldness NOT affected. No affection drop,
  but the guilt spike makes Ethan pull back.
- **The Fallout**: Ethan enters MILD resistance (Phase 2). Next 1-2 activities show
  changed behavior: shorter dialogue, mentions Madison more, avoids eye contact.
  He calls the player "sis" (deliberate downgrade).
- **The Repair Path**: Normal activity engagement. No special action needed — this
  is a mild regression that resolves naturally as they spend time together.
- **The Resolution**: The Couch (Event #7) — Ethan's resistance crumbles when they're
  physically close on the couch. The mild regression makes the couch scene feel more
  charged because there was a pull-back first.

**REGRESSION 2: "Morning After" (Event #14)**
- **Trigger**: After first_night_complete, automatic next morning
- **The Drop**: Ethan guilt +5-10 depending on player's dialogue choice. If player
  says "The wedding is in four days" → additional guilt +5. Ethan enters SEVERE
  resistance for several hours.
- **The Fallout**: Ethan is distant at breakfast. Goes to his laptop to "work."
  Activities that day show his SEVERE resistance: he flinches when she touches him,
  avoids being in the same room, overcompensates by calling Madison.
- **The Repair Path**: Time + the player NOT pushing. The player must let him come
  back on his own.
- **The Resolution**: "Can't Stay Away" (Event #15) — he breaks his own resistance.
  Shows up because he can't stop himself. The fact that HE comes to HER (not the
  reverse) is what makes this feel earned. His resistance crumbles not because
  she pushed, but because desire > guilt.

### Step 5: Bridge Events

**BRIDGE 1: "Rainy Day" (Event #6)**
- Placed between Madison Calls and The Couch
- A thunderstorm knocks out the power. No TV, no phones (battery dead), just candles
  and conversation. They talk about their lives — not about feelings. She tells him
  why she really left (running from herself, not from him). He tells her why he
  proposed to Madison (she was safe, predictable, everything he thought he wanted).
- Neither topic is explicitly romantic, but both reveal vulnerability.
- Sets `rainy_day_complete` — does NOT set any gate flag.
- Stat effect: affection +3-5, guilt -2-3 (honest conversation reduces guilt briefly)
- Purpose: Shows what their relationship COULD be — two people who understand each
  other. Makes everything that follows feel more weighted.

**BRIDGE 2: "Almost Kiss" (Event #9)**
- Placed between Confession and The Real Talk
- The moment stretches. His hand on her face. Breath mixing. Then — interruption.
  Phone rings. A sound. The spell breaks.
- Sets `almost_kiss_complete` — does NOT set any gate flag.
- No significant stat changes (minor affection +2-3 for the bold choice).
- Purpose: Pure dramatic tension. The audience (player) WANTS the kiss. Denying it
  here makes the actual First Kiss (Event #11) feel earned. Classic "almost" storytelling.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## OPENING SCENE (starting_canvas — no trigger)

### Event #1: ARRIVAL
**Canvas ID**: scene_arrival
**Priority**: — (starting canvas, auto-plays)
**Location**: — (narrative arrival, ends at loc_hallway)
**NPC**: npc_ethan (introduced)
**Flags Set**: game_started, arrival_complete
**Gate Flags Set**: None
**Player Phase**: DENIAL → first crack

**Node 1: "The Return"**
Player identity + situation. She hasn't been home in two years. Taxi pulls away.
Heart pounding. "I'm here for the wedding. That's the only reason."

Internal voice (DENIAL phase): Controlled, factual. Describes the house, the
sidewalk, the familiar details. Avoids thinking about Ethan specifically.

Blocks: heading ("Two Weeks"), 3-4 paragraphs establishing player identity and
backstory (step-siblings, 8 years together, feelings buried, left for college),
1 image (house exterior).

**Node 2: "Ethan"**
NPC introduction. Full physical description on first sight. The door opens. He's
there. Taller than she remembered. That smile. "Hey, stranger."

The hug. His arms tighten a moment too long. She breathes him in without meaning to.
Two years of careful distance collapse in an instant.

FORBIDDEN driver T1 (awareness): She's aware of why her heart is racing and is
actively trying to ignore it.

Blocks: 4-5 paragraphs with physical description, dialogue (2 NPC lines), 1 image/gif
(the reunion hug).

Choices:
- "I missed you." → affection +3
- "You look good. Really good." → affection +2, boldness +2
- "So this is where the big day happens, huh?" → no stat change (deflecting)

**Node 3: "The Situation"**
Madison context. The house. Her old room. "Madison's away. It's just us for the
next couple weeks." The weight of "just us" hangs in the air.

Sets up: 14-day timeline, Madison's absence, the living arrangement.

Blocks: 3-4 paragraphs, 2 NPC dialogue lines about Madison and the situation.

Exit: Location exit → loc_hallway. Sets game_started + arrival_complete.
Time progression: 60 minutes (arrives mid-afternoon).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ACT 1: DENIAL AND REMEMBERING (Days 1-3)

Purpose: Establish setting, rekindle dormant feelings, set first gate flag.
Player emotional phases: DENIAL → REMEMBERING
Ethan emotional quadrant: DISTANT → edge of SAFE
Target affection: 15 → 35

---

### Event #2: WELCOME HOME DINNER [BRIDGE]
**Canvas ID**: scene_welcome_dinner
**Priority**: 10
**Location**: loc_kitchen
**NPC**: npc_ethan
**Time**: 17:00-19:00
**Conditions**: arrival_complete = true
**Flags Set**: welcome_dinner_complete, ethan_comfortable
**Gate Flags Set**: None (this is a bridge event — character development only)
**Player Phase**: DENIAL cracking → REMEMBERING

**Why this is a bridge event**: No mechanical unlock. Exists to establish the domestic
dynamic and show that Ethan *remembers* — her favorite meal, small details from years
ago. His memory is his love language, and this scene introduces it.

**Node 1: "Dinner Together"**
He's cooked her favorite. She didn't expect him to remember. The kitchen smells like
their parents' house used to.

LOVE driver tell: "Some things you don't forget." — He remembers everything about her.
This is the first indicator that his feelings aren't buried as deep as he pretends.

Ethan affection tell (15-20 range): He hands her a glass of wine. Makes small talk
about safe things. But she catches him watching her when he thinks she's not looking.

Blocks: 2-3 paragraphs, 2 dialogue exchanges, 1 image/gif (dinner table moment).

Choices:
- "So... two weeks until the big day. Nervous?" → guilt +2 (forces him to think
  about the wedding)
- "Remember when we used to have dinner parties? Just us, pretending to be fancy?"
  → affection +3 (nostalgia, shared history)
- "You've really grown up." → affection +2, boldness +1 (noticing him physically)

**Node 2: "After Dinner"**
He clears dishes. She watches him move through the kitchen. This is his life now.
A life she's not part of. "I'm glad you're here. Really."

Exit: Location exit → loc_hallway. Sets welcome_dinner_complete + ethan_comfortable.
Time progression: 90 minutes.

---

### Event #3: FINDING OLD PHOTOS → sets lingering_touch_unlock
**Canvas ID**: scene_old_photos
**Priority**: 10
**Location**: loc_garage
**NPC**: npc_ethan
**Time**: 14:00-17:00
**Conditions**: welcome_dinner_complete = true, affection >= 15
**Flags Set**: old_photos_complete, lingering_touch_unlock
**Gate Flags Set**: lingering_touch_unlock → unlocks T2 (Suggestive) in all activities
**Player Phase**: REMEMBERING (memories become physical)

**This is the first gate-setting event.** The photo albums are the catalyst — looking
at their shared past together, heads bent close, his voice dropping when he says
"I remember that night." The physical proximity while looking at photos (hands
touching, shoulders pressed together) is the narrative justification for unlocking
suggestive touches in activities.

**Node 1: "The Discovery"**
She finds boxes of photo albums in the garage. High school. Prom. Beach trips.
That summer they got too close. She thought she'd buried this.

He appears. They look through photos together. Heads bent close.

FORBIDDEN driver T2 (stolen glances): He points at a photo of her in "that dress."
His voice drops. "I remember that night." Their eyes meet. Something unspoken passes.

Blocks: 2-3 paragraphs, 1 dialogue line (NPC), 1 video/gif (looking through photos
together, intimate proximity).

Choices:
- "We were just kids." → no stat change (deflecting — DENIAL phase holding)
- "Some things haven't changed." → affection +5, boldness +3 (acknowledging feelings)
- "Why did you keep these?" → affection +3 (forcing him to confront his sentimentality)

**Node 2: "Lingering"**
He doesn't answer right away. Looks at the photo, then at her. The silence stretches.
"We should probably put these away." But neither moves.

Exit: Location exit. Sets old_photos_complete + lingering_touch_unlock.
Time progression: 45 minutes.

---

### Event #4: SLEEPLESS NIGHT
**Canvas ID**: scene_sleepless_night
**Priority**: 10
**Location**: loc_kitchen
**NPC**: npc_ethan
**Time**: 22:00-01:00
**Conditions**: old_photos_complete = true, affection >= 25
**Flags Set**: sleepless_night_complete
**Gate Flags Set**: None
**Player Phase**: REMEMBERING → WANTING (transition)

**Node 1: "3 AM"**
Neither can sleep. She goes downstairs for water and finds him there. Both in sleep
clothes. Both vulnerable. The darkness makes it easier to say things daylight forbids.

FORBIDDEN driver T2 (thrilling because forbidden): The intimacy of 3 AM. Whispers
even though no one else is there. He reaches out, tucks a strand of hair behind her
ear. Freezes. "I should go back to bed."

Ethan affection tell (25-30 range): He doesn't create distance. He's aware of her
sleep clothes (thin nightgown) and doesn't look away. His hand trembles when he
touches her hair.

Blocks: 3-4 paragraphs, 2 dialogue exchanges, 1 image (moonlit kitchen), 1 gif
(hair tuck gesture).

Choices:
- "Yeah. We should." → no affection change (safe, retreating)
- "Stay. Just for a bit." → affection +5 (vulnerable request)
- "Ethan... why can't you sleep?" → affection +3 (pushing for honesty)

**Node 2: "Parting"**
The moment stretches. Then breaks. They retreat to separate rooms. Sleep doesn't
come any easier.

Exit: Location exit. Sets sleepless_night_complete. Time progression: 30 minutes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ACT 1 → ACT 2 TRANSITION

### Event #5: MADISON CALLS [REGRESSION #1]
**Canvas ID**: scene_madison_calls
**Priority**: 10
**Location**: loc_living
**NPC**: npc_ethan
**Time**: 12:00-17:00
**Conditions**: sleepless_night_complete = true, affection >= 30
**Flags Set**: madison_calls_complete
**Gate Flags Set**: None
**Player Phase**: WANTING (confronted with obstacle)

**This is the first regression.** Madison becomes real — not just a name or a concept,
but a voice on the phone, a woman who calls Ethan "babe" and talks about flower
arrangements. The player watches Ethan perform "loving fiancé" in real-time.

**The Drop**: Ethan guilt +5-8 (depending on choice). No affection drop — the
connection isn't damaged, but guilt enters the equation.

**The Fallout**: Next 1-2 activities, Ethan is in MILD resistance. He mentions
Madison more. Calls the player "sis." Sits in the chair instead of the couch.
Activity base scenes should reflect this: shorter NPC dialogue, less eye contact.

**Node 1: "The Call"**
His phone rings. Madison. He talks while the player watches. Loving words that
sound rehearsed. "Yes, everything's fine. She just got here. We're just catching
up."

Close-up on the player's face: jealousy she doesn't want to feel. He looks at her
while telling Madison he loves her. Guilt flickers in his eyes.

When he hangs up, neither speaks.

Blocks: 3-4 paragraphs, 2 NPC dialogue lines (during and after call), 1 video/gif
(overhearing the call, the look between them).

Choices:
- "She seems nice." → no stat change (polite mask)
- Say nothing, just look at him → affection +3 (the silence says everything)
- "Do you love her?" → boldness +5, guilt +5 (direct confrontation — bold but
  costs guilt)

**Node 2: "Aftermath"**
He sets his phone down. "Madison ❤️" fades from the screen. "She's... she's great.
Really." He doesn't sound convinced.

Exit: Location exit. Sets madison_calls_complete. Time progression: 30 minutes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ACT 2: TENSION AND CROSSING LINES (Days 4-10)

Purpose: Build tension, set gate flags, navigate the major crisis, reach the
turning point. Player emotional phases: WANTING → RECKLESS
Ethan emotional quadrant: SAFE → OPEN → CONFLICTED (crisis) → OPEN (deeper)
Target affection: 35 → 90

---

### Event #6: RAINY DAY [BRIDGE]
**Canvas ID**: scene_rainy_day
**Priority**: 10
**Location**: loc_living
**NPC**: npc_ethan
**Time**: 19:00-22:00
**Conditions**: madison_calls_complete = true
**Flags Set**: rainy_day_complete
**Gate Flags Set**: None (pure bridge event)
**Player Phase**: WANTING (but this scene is about vulnerability, not desire)

**Why this is a bridge event**: Exists purely for character development. No gate
unlock, no stat gates beyond the prerequisite flag. The thunderstorm forces honesty
without physical escalation.

**Node 1: "Power Out"**
Thunderstorm. Power dies. No TV, no phones (batteries low). Just candles, wine,
and each other. The house feels different in the dark — smaller, warmer.

He digs out candles from the kitchen drawer. They sit on the couch (the same
couch that will matter later, but tonight it's innocent). Candlelight.

Blocks: 2-3 paragraphs, 1 image (candlelit living room, storm outside).

**Node 2: "The Truth About Leaving"**
Conversation turns to real things. Not "the wedding" or "us" — deeper.

She tells him why she really left for college across the country. Not for
the program, not for the adventure. Because she couldn't keep living in a house
with him and pretending she didn't feel what she felt. Running was easier than
staying and aching.

He's quiet for a long time. Then:
"I knew. Part of me always knew. I just... I told myself you were just growing up.
Leaving the nest. Normal stuff."

Blocks: 3-4 paragraphs, 3-4 dialogue exchanges. No media — this is a conversation
scene. The absence of visuals (darkness, candlelight) puts the focus on words.

Choices:
- "Why did you propose to Madison?" → affection +3, guilt -2 (honest conversation
  reduces guilt — he feels less alone in his conflict)
- "Do you wish I hadn't come back?" → affection +5 (vulnerable question — his
  answer reveals everything)
- "We don't have to talk about this." → no change (retreat)

**Node 3: "His Answer"**
If "Why did you propose?" — He's honest: "Because she was safe. Because after you
left, I needed something that made sense. Madison makes sense. You never made sense.
You were always... chaos. The best kind."

If "Do you wish I hadn't come back?" — Long pause. "Every day since you left, I
wished you'd come back. Every day since you got here, I've wished I didn't." His
voice cracks. "Because now I have to feel this again."

Blocks: 2-3 paragraphs, 1-2 dialogue lines.

Exit: Location exit. Sets rainy_day_complete. Time progression: 90 minutes.

---

### Event #7: THE COUCH → sets flirt_unlock
**Canvas ID**: scene_the_couch
**Priority**: 10
**Location**: loc_living
**NPC**: npc_ethan
**Time**: 19:00-22:00
**Conditions**: rainy_day_complete = true, affection >= 40
**Flags Set**: the_couch_complete, flirt_unlock, ethan_interested
**Gate Flags Set**: flirt_unlock → unlocks T3 (Teasing) in all activities
**Player Phase**: WANTING → edge of RECKLESS

**This is the second gate-setting event.** The couch scene is the first overtly
physical moment — not accidental (like the photo album proximity) but deliberate.
They CHOOSE to sit close. They CHOOSE not to move the blanket. His hand on her
thigh is intentional.

**Node 1: "Movie Night"**
Movie night. The couch is big but they've migrated to the middle. Blanket covers
both of them. On screen, a couple is doing what they're pretending not to think about.

FORBIDDEN driver T3 (boundary testing): Under the blanket, bodies touching. His arm
around her. His hand on her thigh — starts innocent, drifts higher. Neither
acknowledges it.

Blocks: 3-4 paragraphs, 2 dialogue lines, 1 video/gif (couch tension, under-blanket
proximity).

Choices:
- "Ethan..." (warning tone) → affection +2 (mild, but she didn't move away)
- Move closer → affection +5, boldness +3 (pursuing)
- "We can't." But don't move away → affection +3, guilt +3 (conflicted — wants
  it but names the prohibition, which increases his guilt)

**Node 2: "Breaking Apart"**
Something shifts. Or almost shifts. The movie ends. Credits roll. Neither has any
idea what happened in it.

"It's late. We should..." He doesn't finish.

Exit: Location exit. Sets the_couch_complete + flirt_unlock + ethan_interested.
Time progression: 60 minutes.

---

### Event #8: THE CONFESSION
**Canvas ID**: scene_confession
**Priority**: 10
**Location**: loc_backyard
**NPC**: npc_ethan
**Time**: 22:00-01:00
**Conditions**: the_couch_complete = true, affection >= 50, boldness >= 35
**Flags Set**: confession_complete
**Gate Flags Set**: None
**Player Phase**: RECKLESS (the secret is spoken)

**The emotional peak of Act 2 (pre-crisis).** This is where the subtext becomes
text. The player says the unsayable thing. The dam breaks.

**Node 1: "Under the Stars"**
Drinking on the patio. Third glass. Stars out. Pool lights shimmer.

She tells him: "I used to stay awake at night listening for your footsteps. Hoping
you'd knock on my door. Terrified you would."

FORBIDDEN driver — the taboo spoken aloud. The thrill of saying it. The terror.

His response: "I thought I was the only one." "You weren't." Long pause. "What do
we do now?"

Blocks: 4-5 paragraphs, 4-5 dialogue exchanges, 1 gif (wine-loosened truth, intense
eye contact).

Choices:
- "We forget I said that." → affection -5 (retreat — he respects it but is crushed)
- "We still have time to figure that out." → affection +8 (acknowledging the clock,
  keeping the door open)
- Kiss him. No more words. → affection +10, boldness +5 (the boldest choice in
  the game so far)

**Node 2: "After"**
The night air feels different now. Charged. Whatever walls were left have started
to crumble.

Exit: Location exit. Sets confession_complete. Time progression: 45 minutes.

---

### Event #9: ALMOST KISS [BRIDGE]
**Canvas ID**: scene_almost_kiss
**Priority**: 10
**Location**: loc_backyard
**NPC**: npc_ethan
**Time**: 19:00-22:00
**Conditions**: confession_complete = true, affection >= 55
**Flags Set**: almost_kiss_complete
**Gate Flags Set**: None (bridge — pure tension)
**Player Phase**: RECKLESS (frustrated)

**Why this is a bridge event**: Classic "almost" storytelling. The audience WANTS the
kiss. Denying it here makes Event #11 (First Kiss) feel earned. This scene exists
for dramatic tension, not progression.

**Node 1: "The Moment"**
Close. Too close. His hand on her face. His breath. The tilt of heads beginning.

Then — interruption. Phone. Door. Something. The spell breaks. They spring apart
like guilty teenagers.

"I should..." "Yeah."

But they both know. There's no going back.

Blocks: 3 paragraphs, 2 short dialogue exchanges, 1 gif (faces inches apart,
the near-kiss).

Choices:
- "What were we doing?" → guilt +5 (naming it increases his shame)
- "Next time, lock the door." → boldness +5, affection +3 (playful, confident)
- "This can't happen." But your eyes say otherwise → affection -3 (she retreats,
  but the contradiction is visible)

Exit: Location exit. Sets almost_kiss_complete. Time progression: 30 minutes.

---

### Event #10: THE REAL TALK [MAJOR CRISIS]
**Canvas ID**: scene_real_talk
**Priority**: 10
**Location**: loc_player_room
**NPC**: npc_ethan
**Time**: 22:00-01:00
**Conditions**: almost_kiss_complete = true, guilt >= 15
**Flags Set**: real_talk_complete, ethan_vulnerable
**Gate Flags Set**: None
**Player Phase**: RECKLESS → confronted with cost

**THIS IS THE MAJOR CRISIS.** Ethan's internal contradictions peak here. He's been
building toward this breakdown since the game started. This is not a "player did
something wrong" crisis — it's an NPC crisis driven by his own guilt.

**What makes this a good crisis (per v6):**
- Threatens to END the relationship (he could retreat into duty)
- Genuine reason to pull away (he's getting married in a week)
- Cannot be fixed with one choice (his guilt is systemic, not situational)
- Forces both characters to confront what they want
- Resolution requires vulnerability from BOTH sides

**Node 1: "In the Dark"**
"We need to talk about this."

She finds him sitting alone in the dark. He's been thinking. The wedding is in
a week. Madison. The family. The impossibility of what he's feeling.

Ethan's internal contradictions surface simultaneously:
1. "I want to be a good man" vs. "A good man wouldn't feel this"
2. "I want you" vs. "I don't want to be a cheater"
3. "I want truth" vs. "Truth destroys everything"

"I'm supposed to be getting married." "I know." "I don't know if I can." "I know."

"What do you want?" — her question.
"I want you. I hate that I want you." — his breaking point.

FORBIDDEN driver climax: The taboo isn't fun anymore. It's agonizing. The thrill
has been replaced by genuine pain.

Blocks: 4-5 paragraphs, 6-8 dialogue exchanges, 1 gif (holding him as he breaks
down — comfort, not seduction).

Choices:
- "Then have me." → boldness +8, affection +5 (the boldest possible response —
  she meets his vulnerability with desire. This is what makes the best ending
  possible — she gives him PERMISSION to want what he wants.)
- "We'll figure it out. Together." → affection +5 (supportive, patient — builds
  love but doesn't push)
- "Maybe you should go through with it. Maybe this is just cold feet." →
  affection -5, guilt -10 (retreat — the "safe" choice that protects him from
  guilt but kills the relationship's momentum. Guilt DROP because she's giving
  him an out, which relieves his internal conflict but at the cost of connection.)

**CRISIS FALLOUT**: Regardless of choice, Ethan enters MODERATE resistance for the
next 1-2 days. He's emotionally raw. He doesn't avoid her, but he's quieter. More
careful. The activities the next day reflect this — base scenes have shorter
dialogue, he sits further away.

**The key**: The player must NOT push physically during the fallout. The recovery
happens through continued engagement (activities) and patience. The next story
event (First Kiss) requires affection >= 70, which the player can only reach by
continuing to build through activities during the recovery period.

Exit: Location exit. Sets real_talk_complete + ethan_vulnerable. Time progression:
60 minutes.

---

### Event #11: FIRST KISS → sets kiss_unlock
**Canvas ID**: scene_first_kiss
**Priority**: 10
**Location**: loc_living
**NPC**: npc_ethan
**Time**: 19:00-22:00
**Conditions**: real_talk_complete = true, affection >= 70
**Flags Set**: first_kiss_done, kiss_unlock
**Gate Flags Set**: kiss_unlock → unlocks T4 (Foreplay) in all activities
**Player Phase**: RECKLESS (post-crisis, stronger than before)

**Post-crisis breakthrough.** The Real Talk stripped away pretense. This kiss
happens not despite the crisis but BECAUSE of it. They almost lost each other.
Now it's inevitable.

FORBIDDEN driver T4: The taboo fully acknowledged. They're not pretending anymore.
This isn't an "accidental" touch or an "almost" — it's deliberate.

**Node 1: "Inevitable"**
No more interruptions. No more excuses. It happens like gravity.

One moment they're talking. The next, silence. Then his mouth is on hers.

Everything they've been fighting falls away.

Blocks: 3-4 paragraphs, 1 gif (the kiss — tentative then desperate, years of
suppression breaking).

Choices:
- "Don't stop." → affection +5
- "We're really doing this." → affection +3 (acknowledging the line they're crossing)
- Pull him toward the bedroom → affection +5, boldness +5 (the most forward choice)

**Node 2: "After the Kiss"**
When they break apart, the world has shifted. "I've wanted to do that for years."

Exit: Location exit. Sets first_kiss_done + kiss_unlock. Time progression: 30 minutes.

---

### Event #12: WHAT ARE WE DOING
**Canvas ID**: scene_what_are_we_doing
**Priority**: 10
**Location**: loc_kitchen
**NPC**: npc_ethan
**Time**: 07:00-09:00
**Conditions**: first_kiss_done = true
**Flags Set**: what_are_we_doing_done
**Gate Flags Set**: None
**Player Phase**: RECKLESS (stabilizing — "this is real now")

**The morning after the first kiss.** Not a crisis, not a gate — a stabilization
event. They acknowledge what happened. The relationship gets a name (even if that
name is "whatever this is").

**Node 1: "Morning After the Kiss"**
Morning. Coffee. The weight of last night. He's already there when she comes down.
Neither knows what to say.

Ethan affection tell (70-80 range): He's already poured her coffee. He crosses to
her. Takes the coffee from her hands. Kisses her. "I don't want to pretend that
didn't happen."

Blocks: 3-4 paragraphs, 3 dialogue exchanges, 1 gif (morning kiss in the kitchen).

Choices:
- "Neither do I." → affection +5
- "What about Madison?" → guilt +5 (honest but costs guilt)
- "Then don't." Pull him closer → boldness +5, affection +3

**Node 2: "New Normal"**
Whatever this is, it's real. And they have days to figure out what to do about it.

Exit: Location exit. Sets what_are_we_doing_done. Time progression: 45 minutes.

---

### Event #13: FIRST NIGHT TOGETHER [TURNING POINT] → sets intimacy_unlock
**Canvas ID**: scene_first_night
**Priority**: 10
**Location**: loc_player_room
**NPC**: npc_ethan
**Time**: 22:00-01:00
**Conditions**: what_are_we_doing_done = true, affection >= 85
**Flags Set**: first_night_complete, intimacy_unlock, ethan_intimate
**Gate Flags Set**: intimacy_unlock → unlocks T5 (Explicit) in all activities
**Player Phase**: RECKLESS → DESPERATE (turning point — the clock becomes real)

**THIS IS THE TURNING POINT.** The most narratively significant event. Sets the
final gate flag. Requires the highest stat threshold of any Act 2 event.

**References the crisis**: This scene is deeper BECAUSE of The Real Talk. He almost
walked away. She almost let him. Now there's no pretending — they both chose this
with open eyes.

**FORBIDDEN driver T7**: The taboo fully embraced. First forbidden sex. The guilt
isn't gone, but desire has won. "We shouldn't." "I know." But they do.

**Node 1: "Stay"**
No more pretending. The goodnight at the door doesn't end with goodnight.

"Stay." One word. Everything changes. The door clicks shut.

Full intimate encounter. Tender and desperate. His hands shake — not from nerves
but from how long he's wanted this. She pulls him closer. Years of suppression
breaking.

LOVE driver (secondary): This isn't just sex. "God, you're beautiful." Eye contact.
His name on her lips. Emotional intimacy matching physical.

Blocks: 6-8 paragraphs of intimate content, 3-4 dialogue exchanges, 1 video
(first time — emotional, missionary, eye contact, slow building to intense).

Choices:
- "I've wanted this for so long." → affection +5
- "What happens tomorrow?" → guilt +3 (realistic — the clock is real)
- Don't speak. Just hold him. → affection +3 (tenderness over words)

**Node 2: "Aftermath"**
In the quiet after, everything feels different. Clearer. More complicated.
"No regrets?" She answers with a kiss.

Exit: Location exit. Sets first_night_complete + intimacy_unlock + ethan_intimate.
Time progression: 360 minutes (they fall asleep together — skip to morning).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ACT 3: DESPERATION AND RESOLUTION (Days 11-14)

Purpose: Deepen the relationship under pressure, confront reality (Madison arrives),
reach ending. Player emotional phases: DESPERATE → RESOLVED
Ethan emotional quadrant: OPEN → CONFLICTED (Madison) → stat-dependent resolution
Target affection: 90 → 95+ (ending dependent)

---

### Event #14: MORNING AFTER [REGRESSION #2]
**Canvas ID**: scene_morning_after
**Priority**: 10
**Location**: loc_player_room
**NPC**: npc_ethan
**Time**: 07:00-09:00
**Conditions**: first_night_complete = true
**Flags Set**: morning_after_complete
**Gate Flags Set**: None
**Player Phase**: DESPERATE (first moment of "what have we done")

**This is the second regression.** Post-sex guilt spike. Ethan wakes up next to
his step-sister in the house where they grew up, four days before his wedding.
The tenderness of the morning cannot erase the weight of what they've done.

**Node 1: "Dawn"**
Dawn light through curtains. His arm around her. For a moment — just this. Then
reality seeps back.

Morning intimacy — lazy, half-asleep, tender. A continuation of the night before.
He's gentle, present, lost in her.

Then it's over and the guilt lands.

Blocks: 4-6 paragraphs of intimate morning content, 2 dialogue exchanges,
1 video/gif (lazy morning intimacy — spooning, slow, gentle).

Choices:
- "Stay a little longer." → affection +3 (wanting to hold onto the moment)
- "The wedding is in four days." → guilt +5 (forcing reality — bold but costly)
- "I don't regret this. Do you?" → affection +5 (his answer: no. but his eyes
  say it's complicated.)

**Node 2: "Lingering"**
"We should talk. Later. About everything." But for now, this moment.

**REGRESSION FALLOUT**: Over the next day, Ethan's SEVERE resistance activates.
He flinches when she touches him in daylight. Avoids eye contact at breakfast.
Goes to his laptop to "work." Activities this day show the guilt: shorter dialogue,
physical distance, overcompensation (calls Madison while the player can hear).

Exit: Location exit. Sets morning_after_complete. Time progression: 60 minutes.

---

### Event #15: CAN'T STAY AWAY
**Canvas ID**: scene_cant_stay_away
**Priority**: 10
**Location**: loc_hallway
**NPC**: npc_ethan
**Time**: 14:00-17:00
**Conditions**: morning_after_complete = true, affection >= 90
**Flags Set**: cant_stay_away_complete
**Gate Flags Set**: None
**Player Phase**: DESPERATE (the addiction)

**The resolution of Regression #2.** Ethan's SEVERE resistance breaks — not because
the player pushes, but because HE can't stay away. This is the critical distinction:
the repair comes from him, proving the desire is stronger than the guilt.

FORBIDDEN driver T8+ (risk is part of the thrill): Hallway encounter. Desperate.
Anyone could walk by. Fast, urgent, against the wall. His hand over her mouth.
The danger of the house itself — every creaking board, every doorway.

**Node 1: "Hallway"**
She tried to be normal today. Failed. Every look is loaded.

"I can't stop thinking about last night." — him, not her. He initiates.

He glances down the hall — empty — and then his mouth is on hers. They stumble
backward. Her back hits the wall. Fast, desperate, addicted.

Blocks: 5-7 paragraphs of explicit content, 3-4 dialogue exchanges, 1 video
(standing hallway encounter — desperate, urgent, hand over mouth).

"My room. Ten minutes. I'm not done with you."

Exit: Location exit. Sets cant_stay_away_complete. Time progression: 90 minutes.

---

### Event #16: MADISON ARRIVES [ACT 3 CRISIS]
**Canvas ID**: scene_madison_arrives
**Priority**: 10
**Location**: loc_hallway
**NPC**: npc_ethan (+ npc_madison appears)
**Time**: 14:00-17:00
**Conditions**: cant_stay_away_complete = true
**Flags Set**: madison_arrived
**Gate Flags Set**: None
**Player Phase**: DESPERATE (reality crash)

**The Act 3 crisis.** Not a relationship crisis (they're past that) but a
CONFRONTATION WITH REALITY. Madison was an abstract concept for 12 days.
Now she's real, warm, excited about her wedding, genuinely nice to the player.

This transforms abstract guilt into concrete betrayal. The player isn't just
"doing something wrong" — she's standing in front of the woman she's wronging.

**Node 1: "Arrival"**
Sound of a car. Heart stops. Madison.

She's polished, put-together, excited. "Surprise! I finished early!"

The player watches Ethan perform. The hug between the engaged couple. Over
Madison's shoulder, his eyes find the player's. Apology. Fear. Longing.

Madison turns to the player: "You must be the step-sister! I've heard so much
about you."

Blocks: 4-5 paragraphs, 3-4 dialogue exchanges (Madison + Ethan), 1 video/gif
(arrival, the embrace, the look over the shoulder).

Choices:
- "All good things, I hope." → no stat change (polite mask)
- "Has he mentioned me?" → no stat change (loaded question but she keeps composure)
- Excuse yourself. You can't do this. → no stat change (retreat)

(Note: ALL choices lead to the same place. The player's specific response doesn't
change the situation — Madison is here. The choices express the player's emotional
state, not a mechanical divergence.)

**Node 2: "New Reality"**
Madison is nice. Genuinely nice. That makes it worse.

The player feels like a ghost in her own body.

Exit: Location exit. Sets madison_arrived. Time progression: 30 minutes.

---

### Event #17: STOLEN MOMENT
**Canvas ID**: scene_stolen_moment
**Priority**: 10
**Location**: loc_garage
**NPC**: npc_ethan
**Time**: 14:00-17:00
**Conditions**: madison_arrived = true, affection >= 85
**Flags Set**: stolen_moment_complete
**Gate Flags Set**: None
**Player Phase**: DESPERATE (forbidden at maximum intensity)

**FORBIDDEN driver at maximum intensity.** Madison is in the house. Every sound
could be her. The garage is the only private space (Madison has no schedule entry
there). The danger is real. The desperation is real.

**Node 1: "Hidden"**
Madison is on the phone. Or in the shower. Doesn't matter where — just that
she's not here.

He finds the player in the garage. Grabs her hand. Pulls her behind shelves.
"I need you. I can't — one more time before —" He doesn't finish.

Desperate. Guilty. Unable to stop. His hand over her mouth because Madison is
somewhere in the house.

Blocks: 5-7 paragraphs of explicit content, 3-4 dialogue lines, 1 video
(garage quickie — urgent, bent over, hand covering mouth, frantic).

Choices:
- "We're insane." But don't stop → affection +3
- "This is the last time." → guilt +5 (a lie they both know)
- "Run away with me." → boldness +10 (plants the seed for the ending —
  the boldest thing she's ever said)

**Node 2: "After"**
Madison's voice calling his name from inside. The spell breaks.
"Coming!" — He looks at the player one last time. That look says everything.

Exit: Location exit. Sets stolen_moment_complete. Time progression: 30 minutes.

---

### Event #18: NIGHT BEFORE WEDDING
**Canvas ID**: scene_night_before_wedding
**Priority**: 10
**Location**: loc_player_room
**NPC**: npc_ethan
**Time**: 22:00-01:00
**Conditions**: stolen_moment_complete = true
**Flags Set**: night_before_complete
**Gate Flags Set**: None
**Player Phase**: DESPERATE → RESOLVED

**The final peak.** Tomorrow he marries Madison. Tonight he comes to her room.
This scene is the emotional climax — longer, more nodes, more media than any
other scene. Every touch is weighted with finality.

**Node 1: "The Door Opens"**
Tomorrow he marries Madison. Tonight the door opens in darkness. She knows it's
him before he speaks. "I had to see you." His kiss tastes like tears.

Blocks: 3-4 paragraphs, 2 dialogue lines, 2 gifs (desperate embrace, deep kiss).

Single choice: Pull him inside → Node 2.

**Node 2: "Undressing"**
Slowly. Memorizing. Savoring. Every button, every inch of skin. "I want to
remember everything."

Blocks: 2-3 paragraphs, 1 dialogue line, 2 gifs (undressing sequence).

Single choice: Let him lay you down → Node 3.

**Node 3: "Worship"**
He kisses his way down her body. No rush tonight. "I want to remember every part
of you." Slow, devoted, like a prayer.

Blocks: 2-3 paragraphs, 1 dialogue line, 2-3 gifs (oral sequence).

Single choice: Pull him up to you → Node 4.

**Node 4: "Together"**
When he enters her, they're both crying. The weight of everything they can't have.
But right now, he's hers. "I love you. I've always loved you."

LOVE driver climax (secondary): This is where the LOVE driver fully resolves.
He says it. Not in the heat of passion — in the weight of loss.

Blocks: 3-4 paragraphs, 2 dialogue lines, 1-2 gifs (missionary, emotional, foreheads
touching).

Single choice: Hold him closer → Node 5.

**Node 5: "Deeper"**
Pace builds. Gentle becomes urgent. "Don't hold back. Not tonight." She pulls him
deeper. Nails down his back.

Blocks: 2-3 paragraphs, 1 dialogue line, 1 gif (building intensity).

Single choice: Take control → Node 6.

**Node 6: "Taking Control"**
She pushes him onto his back. She needs to feel him, control this, make it hers.
Rides him. His hands grip her hips.

Blocks: 2-3 paragraphs, 1 dialogue line, 3-5 gifs (cowgirl sequence, escalating).

Single choice: Feel it building → Node 7.

**Node 7: "The Finish"**
"I'm yours. Whatever happens tomorrow, I'm yours tonight."

Climax. Aftermath. He cleans her gently, tenderly. Then they lie tangled together.

"Don't marry her." "Don't ask me that." But he's here, isn't he?

They stay together until the sky lightens. No more words. Just holding on to what
little time they have.

Blocks: 4-5 paragraphs, 4 dialogue lines, 2-3 gifs/images (climax, aftermath,
tangled together).

Final choices (determines ending path):
- "Choose me." → boldness +10, sets night_before_complete
  (The final bold act. Gives him explicit permission to break free.)
- "I'll always love you. Whatever you decide." → affection +5, sets night_before_complete
  (Graceful. Loving. But doesn't push him to choose.)
- "This was goodbye, wasn't it?" → sets night_before_complete
  (Acceptance. No stat change — she's at peace with whatever happens.)

Exit: Location exit → loc_player_room. Time progression: 300 minutes (until dawn).

---

### Event #19: WEDDING MORNING
**Canvas ID**: scene_wedding_morning
**Priority**: 10
**Location**: loc_kitchen
**NPC**: npc_ethan
**Time**: 07:00-09:00
**Conditions**: night_before_complete = true
**Flags Set**: wedding_morning_done
**Gate Flags Set**: None
**Player Phase**: RESOLVED

**The final story canvas before endings.** The house is chaos — florists, caterers,
Madison's family. He finds one moment alone with her.

"Whatever happens today... I need you to know... Thank you. For everything."

She doesn't know what that means yet.

**Node 1: "The Day"**
The day has arrived. Chaos. He finds her in the kitchen during a brief gap. His hand
finds hers. One final moment.

Blocks: 3-4 paragraphs, 2-3 dialogue lines, 1 video/gif (stolen moment amid wedding
chaos, hands touching).

Exit: Location exit. Sets wedding_morning_done. Time progression: 60 minutes.

→ From here, the ENDING CANVASES trigger based on stats (see Phase 2, Section 6).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ENDING CANVASES (4)

All endings trigger from loc_living, time 09:00-12:00, condition wedding_morning_done.
Priority ordering ensures mutual exclusivity — highest-priority ending fires first.

---

### ENDING A: HE CHOOSES YOU (Priority 10)
**Canvas ID**: ending_he_chooses_you
**Conditions**: wedding_morning_done + affection >= 95 + boldness >= 70 + guilt < 50
**Tone**: Triumphant but complicated

The ceremony begins. Madison walks down the aisle. Everyone watches.

"I can't do this."

Chaos. Madison's tears. Family shock. Scandal. But when the dust settles, he's
beside her. "I choose you. I choose us."

It won't be easy. Nothing worth having ever is.

Blocks: 5-6 paragraphs, 2-3 dialogue lines, 1 video (wedding interrupted, walking
away from the altar, together in the aftermath).

---

### ENDING B: THE ARRANGEMENT (Priority 8)
**Canvas ID**: ending_the_arrangement
**Conditions**: wedding_morning_done + affection >= 85 + guilt >= 70 + boldness >= 60
**Tone**: Dark, complicated, ongoing

He marries Madison. Of course he does. But the story doesn't end.

"I can't leave her. But I can't leave you either."

It's wrong. They both know it's wrong. But when has that stopped them?

Blocks: 4-5 paragraphs, 2 dialogue lines, 1 video (wedding concludes, then a message
on her phone weeks later — the secret continues).

---

### ENDING C: ONE LAST NIGHT (Priority 6)
**Canvas ID**: ending_one_last_night
**Conditions**: wedding_morning_done + affection >= 80 + guilt >= 60
**Tone**: Bittersweet sacrifice

He goes through with it. The guilt was always too strong. But the night before,
he came to her one last time.

"I love you. I'll always love you. But I can't destroy everything."

She watches from the crowd. Their eyes meet once. A lifetime in a glance. She
leaves before the reception.

Blocks: 5-6 paragraphs, 3 dialogue lines, 1 video (wedding from the crowd, tears
hidden, taxi pulling away).

---

### ENDING D: WHAT COULD HAVE BEEN (Priority 1 — fallback)
**Canvas ID**: ending_what_could_have_been
**Conditions**: wedding_morning_done (no other stat requirements)
**Tone**: Melancholy, missed chance

They came close. So close. But neither was brave enough.

The wedding happens. He's distant but committed. She's present but already leaving.

"Maybe in another life." "Maybe."

Some love stories end with what-if.

Blocks: 4-5 paragraphs, 2 dialogue lines, 1 video (distance, regret, airport
departure, looking back once).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## FLAG CHAIN DIAGRAM

```
game_started + arrival_complete (scene_arrival)
  │
  ├── welcome_dinner_complete + ethan_comfortable (scene_welcome_dinner) [BRIDGE]
  │     │
  │     ├── old_photos_complete + lingering_touch_unlock (scene_old_photos) [GATE 1 → T2]
  │     │     │
  │     │     ├── sleepless_night_complete (scene_sleepless_night)
  │     │     │     │
  │     │     │     ├── madison_calls_complete (scene_madison_calls) [REGRESSION #1]
  │     │     │     │     │
  │     │     │     │     ├── rainy_day_complete (scene_rainy_day) [BRIDGE]
  │     │     │     │     │     │
  │     │     │     │     │     ├── the_couch_complete + flirt_unlock + ethan_interested
  │     │     │     │     │     │   (scene_the_couch) [GATE 2 → T3]
  │     │     │     │     │     │     │
  │     │     │     │     │     │     ├── confession_complete (scene_confession)
  │     │     │     │     │     │     │     │
  │     │     │     │     │     │     │     ├── almost_kiss_complete (scene_almost_kiss) [BRIDGE]
  │     │     │     │     │     │     │     │     │
  │     │     │     │     │     │     │     │     ├── real_talk_complete + ethan_vulnerable
  │     │     │     │     │     │     │     │     │   (scene_real_talk) [MAJOR CRISIS]
  │     │     │     │     │     │     │     │     │     │
  │     │     │     │     │     │     │     │     │     ├── first_kiss_done + kiss_unlock
  │     │     │     │     │     │     │     │     │     │   (scene_first_kiss) [GATE 3 → T4]
  │     │     │     │     │     │     │     │     │     │     │
  │     │     │     │     │     │     │     │     │     │     ├── what_are_we_doing_done
  │     │     │     │     │     │     │     │     │     │     │   (scene_what_are_we_doing)
  │     │     │     │     │     │     │     │     │     │     │     │
  │     │     │     │     │     │     │     │     │     │     │     ├── first_night_complete
  │     │     │     │     │     │     │     │     │     │     │     │   + intimacy_unlock
  │     │     │     │     │     │     │     │     │     │     │     │   + ethan_intimate
  │     │     │     │     │     │     │     │     │     │     │     │   (scene_first_night)
  │     │     │     │     │     │     │     │     │     │     │     │   [GATE 4 → T5 / TURNING POINT]
  │     │     │     │     │     │     │     │     │     │     │     │     │
  │     │     │     │     │     │     │     │     │     │     │     │     ├── morning_after_complete
  │     │     │     │     │     │     │     │     │     │     │     │     │   (scene_morning_after)
  │     │     │     │     │     │     │     │     │     │     │     │     │   [REGRESSION #2]
  │     │     │     │     │     │     │     │     │     │     │     │     │     │
  │     │     │     │     │     │     │     │     │     │     │     │     │     ├── cant_stay_away_complete
  │     │     │     │     │     │     │     │     │     │     │     │     │     │   (scene_cant_stay_away)
  │     │     │     │     │     │     │     │     │     │     │     │     │     │     │
  │     │     │     │     │     │     │     │     │     │     │     │     │     │     ├── madison_arrived
  │     │     │     │     │     │     │     │     │     │     │     │     │     │     │   (scene_madison_arrives)
  │     │     │     │     │     │     │     │     │     │     │     │     │     │     │   [ACT 3 CRISIS]
  │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │
  │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     ├── stolen_moment_complete
  │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │   (scene_stolen_moment)
  │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │
  │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     ├── night_before_complete
  │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │   (scene_night_before_wedding)
  │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │
  │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     ├── wedding_morning_done
  │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │   (scene_wedding_morning)
  │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │
  │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     │     ├── ENDINGS
```

## GATE TIMELINE

| Gate | Set By | Requirements | ~Day |
|------|--------|-------------|------|
| lingering_touch_unlock | scene_old_photos | welcome_dinner_complete + affection >= 15 | ~Day 2 |
| flirt_unlock | scene_the_couch | rainy_day_complete + affection >= 40 | ~Day 5-6 |
| kiss_unlock | scene_first_kiss | real_talk_complete + affection >= 70 | ~Day 8-9 |
| intimacy_unlock | scene_first_night | what_are_we_doing_done + affection >= 85 | ~Day 10 |

## EVENT COUNT SUMMARY

| Type | Count |
|------|-------|
| Opening scene (auto) | 1 |
| Act 1 events | 3 (dinner, photos, sleepless) |
| Act 1→2 transition (regression) | 1 (madison calls) |
| Act 2 events | 7 (rainy day, couch, confession, almost kiss, real talk, first kiss, what are we doing) |
| Turning point | 1 (first night) |
| Act 3 events | 6 (morning after, can't stay away, madison arrives, stolen moment, night before, wedding morning) |
| Endings | 4 |
| **TOTAL** | **23** (19 story + 4 endings) |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
