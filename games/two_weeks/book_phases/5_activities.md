===============================================================================
                         PHASE 5: ACTIVITIES
===============================================================================

Design all repeatable canvases — NPC activities, solo activities, and utilities.

ACTIVITY DESIGN RULES (from game_design_rules.md):
1. Every activity uses conditional escalating choices (Rule #1)
2. Every gated choice requires BOTH stat threshold + flag (Rule #4 — Dual Gating)
3. Mark highest-escalation exit with loop_terminal = true
4. All activities have schedule constraints + max_triggers_per_day (Rule #5)
5. NPC activities set trigger.npc for portrait display (Rule #6)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION A: NPC ACTIVITIES (12 Escalating)

All NPC activities follow this structure:
- **Node 1** (base scene): Describes the moment. Uses emotional variant writing.
- **Exit block**: Tiered choices. T1 always available. T2-T5 dual-gated.
- **Tier nodes** (T2-T5): Each tier has its own node with escalating content.
- **Loop exit**: Each tier node exits the canvas. Highest tier = loop_terminal.

### STAT EFFECTS PER TIER (consistent across all activities)
| Tier | Affection | Other | Notes |
|------|-----------|-------|-------|
| T1 | +1 | — | Always available |
| T2 | +2 | — | Suggestive |
| T3 | +2 | varies | Teasing |
| T4 | +3 | — | Foreplay |
| T5 | +3 | — | Explicit |

Some activities also give boldness or guilt — noted per activity.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Activity 1: BREAKFAST WITH ETHAN
- **ID**: activity_breakfast_ethan
- **Location**: loc_kitchen
- **Schedule**: 07:00-09:00
- **NPC**: npc_ethan
- **Priority**: 1
- **Max/Day**: 1
- **Unlock**: Always available (no conditions beyond location + time)

**Base Scene — DEFAULT (SAFE/OPEN):**
Morning light through the kitchen window. He's at the counter, coffee already
made. Two mugs. He remembered how she takes hers. Cereal, toast, the easy rhythm
of morning routine. He looks up when she walks in.

**WITHDRAWN variant (post-crisis / CONFLICTED):**
The kitchen is quiet. His coffee mug is in the sink — he already ate. A plate with
toast sits on the counter. He's at his laptop, barely looks up. "Morning."

**WARM variant (high-stat / OPEN):**
He's humming. Her coffee is ready, exactly right. He pulls out the stool next to
him instead of across. "Slept well?" The question means something different now.

**Video/Image**: 1 image per base scene variant (morning kitchen, coffee, domestic).

**Choice Progression:**

| Tier | Choice Text | Conditions | Target | Effects |
|------|-------------|------------|--------|---------|
| T1 | "Thanks for coffee." Eat in comfortable silence | Always | exit | affection +1 |
| T2 | Sit closer than necessary. Let your knee touch his. | affection >= 25 + lingering_touch_unlock | node_t2 | affection +2 |
| T3 | "You always look good in the morning." Hold eye contact. | affection >= 45 + flirt_unlock | node_t3 | affection +2 |
| T4 | Come up behind him. Arms around his waist. Kiss his neck. | affection >= 65 + kiss_unlock | node_t4 | affection +3 |
| T5 | He lifts you onto the counter. Breakfast gets cold. | affection >= 85 + intimacy_unlock | node_t5 | affection +3, loop_terminal |

**Tier Nodes:**

**T2 (Suggestive):** Their knees touch under the breakfast bar. Neither moves away.
His hand finds hers when reaching for the jam. Fingers brush. Linger. "Sorry." But
he's not sorry. 1 gif (accidental hand touch over breakfast).

**T3 (Teasing):** She catches him watching her stretch. He quickly looks away, ears
red. She takes her time reaching for things on high shelves. The kitchen feels
smaller. "Need help with that?" He's already behind her. 1 gif (standing too close
in the kitchen, reaching past her).

**T4 (Foreplay):** She wraps her arms around him from behind at the counter. He leans
back into her. Turns around. His hands on her waist. Kisses that taste like coffee.
"We should eat." "Later." 1 gif (kitchen embrace, kissing).

**T5 (Explicit):** Morning hunger isn't for food. He lifts her onto the counter.
Her legs wrap around him. Breakfast burns. Neither cares. 1 video (kitchen counter
sex — morning, urgent, her legs around him).

---

### Activity 2: MORNING COFFEE
- **ID**: activity_morning_coffee
- **Location**: loc_kitchen
- **Schedule**: 07:00-09:00
- **NPC**: npc_ethan
- **Priority**: 1
- **Max/Day**: 1
- **Unlock**: Always available

**Base Scene — DEFAULT:**
Quiet morning coffee, both still waking up. Comfortable silence of two people who
don't need to fill every moment. Steam rising from mugs. Sunlight warming the table.

**WITHDRAWN:** He's in the kitchen but on his phone. Scrolling. Coffee made for one.
She makes her own. The distance is three feet and a mile.

**WARM:** Sleepy morning intimacy. He's shirtless, she's in a thin robe. He pours
before she asks. Their eyes meet over the rims. Everything is soft.

**Choice Progression:**

| Tier | Choice Text | Conditions | Target | Effects |
|------|-------------|------------|--------|---------|
| T1 | Sip in comfortable silence. Just exist together. | Always | exit | affection +1 |
| T2 | Notice how his sleep shirt rides up. Let your eyes linger. | affection >= 25 + lingering_touch_unlock | node_t2 | affection +2 |
| T3 | "You always looked cute in the morning." Smile over your mug. | affection >= 45 + flirt_unlock | node_t3 | affection +2 |
| T4 | "Spill" coffee on your shirt. Watch his eyes follow as you dab at it. | affection >= 65 + kiss_unlock | node_t4 | affection +3, boldness +1 |
| T5 | The coffee table works just as well as the breakfast bar. | affection >= 85 + intimacy_unlock | node_t5 | affection +3, loop_terminal |

**Tier Nodes:**

**T2:** Eyes wander, quickly corrected. She notices his sleep clothes hanging low.
He notices her robe loosening. Both pretend not to notice. 1 gif (sleepy morning,
lingering looks).

**T3:** "You always looked cute in the morning." Did he just say that out loud?
The word "cute" hangs in the air. She grins. He blushes. Something shifts in the
morning light. 1 gif (flirtatious morning smile).

**T4:** She "accidentally" spills coffee on her shirt. The thin fabric goes
translucent. His eyes follow the stain. "Let me help." His hands on her shirt,
dabbing. Their faces close. The coffee is forgotten. 1 gif (close proximity,
hands on her shirt, tension).

**T5:** The mug hits the counter. His mouth is on hers. Clothes shed between
kitchen and wherever they end up. Lazy morning sex, half-caffeinated. 1 video
(morning kitchen sex — lazy, unhurried, intimate).

---

### Activity 3: HELPING WITH CHORES
- **ID**: activity_helping_chores
- **Location**: loc_living
- **Schedule**: 09:00-12:00
- **NPC**: npc_ethan
- **Priority**: 1
- **Max/Day**: 1
- **Unlock**: Always available

**Base Scene — DEFAULT:**
Laundry, dishes, general tidying. Domestic teamwork. She's helping because she's
a guest who doesn't want to be useless. He appreciates it. Easy conversation about
old times while folding towels.

**WITHDRAWN:** He's cleaning silently. Efficient, focused. Accepts her help with
a nod. Conversation is about logistics: "Trash goes out Tuesday." The domesticity
feels sterile.

**WARM:** They've developed a rhythm. He washes, she dries. Their hips bump at
the sink. He flicks water at her. "You started it." The house feels like theirs.

**Choice Progression:**

| Tier | Choice Text | Conditions | Target | Effects |
|------|-------------|------------|--------|---------|
| T1 | Fold laundry, easy conversation. Helpful sibling energy. | Always | exit | affection +1 |
| T2 | Hold up his shirt, press it to your face. "Same detergent." | affection >= 25 + lingering_touch_unlock | node_t2 | affection +2 |
| T3 | Playful towel-flicking. He chases you around the kitchen island. | affection >= 45 + flirt_unlock | node_t3 | affection +2, boldness +1 |
| T4 | "You missed a spot." He reaches around you at the sink. Stays. | affection >= 65 + kiss_unlock | node_t4 | affection +3 |
| T5 | The laundry can wait. The couch is right there. | affection >= 85 + intimacy_unlock | node_t5 | affection +3, loop_terminal |

**Tier Nodes:**

**T2:** She holds up one of Madison's blouses. Awkward moment. Then one of his
shirts — presses it to her nose. "Still use the same detergent." He watches her
inhale. Doesn't say anything. Doesn't need to. 1 gif (smelling his shirt, intimate
domestic moment).

**T3:** Dish towel flick fight. He chases her around the island. She squeals. He
catches her from behind. Both breathing hard. His arms around her. Neither moves.
Then she squirms free, laughing. "You cheat." 1 gif (playful chasing, catching).

**T4:** She's at the sink. He comes up behind her, reaching for the faucet. Doesn't
step back. His breath on her neck. Hands sliding from the faucet to her waist.
"You missed a spot." His lips on her shoulder. 1 gif (behind her at the sink,
kissing her neck).

**T5:** The laundry basket hits the floor. He backs her against the couch.
"This can wait." "It definitely can." 1 video (couch sex — playful start, intense
finish, surrounded by half-folded laundry).

---

### Activity 4: LUNCH TOGETHER
- **ID**: activity_lunch_together
- **Location**: loc_kitchen
- **Schedule**: 12:00-14:00
- **NPC**: npc_ethan
- **Priority**: 1
- **Max/Day**: 1
- **Unlock**: Always available

**Base Scene — DEFAULT:**
Making sandwiches together, chatting about her life, his job, surface-level
catch-up. Easy midday routine. He remembers her favorite — grilled cheese,
extra sharp cheddar.

**WITHDRAWN:** He eats at his desk. She finds a plate in the microwave with a
note: "Saved you some." Considerate but absent.

**WARM:** He made her favorite without asking. Their knees touch under the breakfast
bar. Neither moves away. "Remember when we used to sneak extra dessert?" Shared
conspiracy. He offers her a bite from his fork.

**Choice Progression:**

| Tier | Choice Text | Conditions | Target | Effects |
|------|-------------|------------|--------|---------|
| T1 | Casual lunch, easy conversation. Good sibling catch-up. | Always | exit | affection +1 |
| T2 | Your knees touch under the bar. Leave them there. | affection >= 25 + lingering_touch_unlock | node_t2 | affection +2 |
| T3 | "Remember when we used to sneak dessert?" Accept the bite from his fork. | affection >= 45 + flirt_unlock | node_t3 | affection +2 |
| T4 | Food forgotten. He's standing between your legs as you sit on the counter. | affection >= 65 + kiss_unlock | node_t4 | affection +3 |
| T5 | The breakfast bar sees more action than breakfast. | affection >= 85 + intimacy_unlock | node_t5 | affection +3, loop_terminal |

**Tier Nodes:** Similar progression pattern as breakfast — domestic intimacy escalating
through proximity → deliberate touching → kissing → sex. Lunch setting emphasizes
the casualness of desire becoming routine. 1 media item per tier.

---

### Activity 5: POOL TIME
- **ID**: activity_pool_time
- **Location**: loc_backyard
- **Schedule**: 14:00-17:00
- **NPC**: npc_ethan
- **Priority**: 1
- **Max/Day**: 1
- **Unlock**: Always available

**Base Scene — DEFAULT:**
Summer heat. The pool. She's in a swimsuit, he's in board shorts. Lounging,
swimming laps. Sunlight on water. The privacy fence means no one can see.

**WITHDRAWN:** He's doing laps. Focused. Doesn't splash her when she gets in.
Parallel swimming, not together. Gets out early. "Going to shower."

**WARM:** He's already in the water when she comes out. Watches her walk to the
pool edge. "The water's perfect." His voice drops on "perfect." He's not talking
about the water.

**Choice Progression:**

| Tier | Choice Text | Conditions | Target | Effects |
|------|-------------|------------|--------|---------|
| T1 | Swim laps, lounge on chairs. Easy pool day. | Always | exit | affection +1 |
| T2 | Ask him to put sunscreen on your back. His hands linger. | affection >= 25 + lingering_touch_unlock | node_t2 | affection +2, boldness +1 |
| T3 | Playful splashing. Grab his shoulders for "balance." Bodies pressed together. | affection >= 45 + flirt_unlock | node_t3 | affection +2, boldness +1 |
| T4 | Night swimming. Underwater lights. He pulls you close. Hands explore beneath the surface. | affection >= 65 + kiss_unlock | node_t4 | affection +3 |
| T5 | The pool lounger is sturdier than it looks. Or the pool itself. | affection >= 85 + intimacy_unlock | node_t5 | affection +3, loop_terminal |

**Tier Nodes:**

**T2:** Sunscreen on her back. His hands move slowly — shoulders, spine, the small
of her back. Fingertips at the bikini line. "Missed a spot" is becoming their phrase.
She arches into his touch. 1 gif (sunscreen application, lingering hands).

**T3:** Splash war escalates. She wraps her legs around him for "balance." His hands
on her thighs, holding her up. Wet skin on wet skin. Faces inches apart. "Balance"
is a fiction and they both know it. 1 gif (pool play, bodies pressed together, wet).

**T4:** Night. Pool lights shimmer blue beneath the surface. He pulls her against
him. Water provides cover. His hands slide down her body under the surface.
"Anyone could see us." "No they can't." Her bikini top loosens. His fingers find
skin. 1 gif (night pool, underwater touching, intimate).

**T5:** Pool lounger by moonlight. She straddles him, water dripping from both of
them. Or in the shallow end — water at waist level, his hands lifting her onto
him. The outdoor air and the risk of neighbors hearing. 1 video (pool/lounger
sex — wet, moonlit, outdoor).

---

### Activity 6: WEDDING PLANNING HELP
- **ID**: activity_wedding_planning
- **Location**: loc_backyard (patio) / loc_living
- **Schedule**: 14:00-17:00
- **NPC**: npc_ethan
- **Priority**: 1
- **Max/Day**: 1
- **Unlock**: Always available
- **Special**: This activity gives GUILT in addition to affection (working on
  the fiancée's wedding while falling for the groom).

**Base Scene — DEFAULT:**
Seating charts, RSVPs, invitation samples spread across the patio table. She's
being a good sister. Helping with his fiancée's wedding. The irony is not lost
on either of them.

**WITHDRAWN:** He's drowning in wedding logistics. Stressed, snapping at vendors
on the phone. She helps quietly, efficiently. No charged moments — just teamwork
under pressure.

**WARM:** He vents about wedding stress. She listens. Their hands touch over
fabric samples. Madison's name comes up and neither flinches anymore — it's just
the elephant they've learned to walk around.

**Choice Progression:**

| Tier | Choice Text | Conditions | Target | Effects |
|------|-------------|------------|--------|---------|
| T1 | Help with RSVPs. Be a good sister. | Always | exit | affection +1, guilt +1 |
| T2 | Your hands brush over invitation samples. Hold the moment. | affection >= 25 + lingering_touch_unlock | node_t2 | affection +2, guilt +2 |
| T3 | "What would YOUR perfect wedding look like?" Watch his face. | affection >= 45 + flirt_unlock | node_t3 | affection +2, guilt +3 |
| T4 | "I don't know if I can do this." He's not talking about the seating chart. | affection >= 65 + kiss_unlock | node_t4 | affection +3, guilt +3 |
| T5 | The wedding planning materials get swept off the table. | affection >= 85 + intimacy_unlock | node_t5 | affection +3, guilt +4, loop_terminal |

**Tier Nodes:**

**T2:** Looking at invitation designs. Their fingers overlap on a sample. He
doesn't pull away. She traces the embossed "Ethan & Madison" with her fingertip.
The name is a knife between them. 1 image (hands overlapping on invitation).

**T3:** "What would your perfect wedding look like?" Dangerous question. His eyes
meet hers. Long pause. "Small. Private. Someone who..." He doesn't finish. Doesn't
need to. 1 gif (loaded eye contact, unfinished sentence).

**T4:** He drops his pen. Puts his head in his hands. "I don't know if I can do
this." She takes his hand. Both know he's not talking about centerpieces.
Forehead to forehead. The weight of what they're doing settles on them both.
1 gif (comfort, foreheads touching, emotional).

**T5:** Seating charts scatter. Invitation samples crumple under their weight.
Sex on the very documents of his commitment to someone else. The FORBIDDEN driver
at its most pointed — they're literally on top of the wedding plans. 1 video
(sex on the patio table / living room, wedding materials visible).

---

### Activity 7: COOKING TOGETHER
- **ID**: activity_cooking_together
- **Location**: loc_kitchen
- **Schedule**: 17:00-19:00
- **NPC**: npc_ethan
- **Priority**: 1
- **Max/Day**: 1
- **Unlock**: Always available

**Base Scene — DEFAULT:**
Making mom's old recipe together. Nostalgia, laughter over shared memories.
Kitchen teamwork — he chops, she stirs. Warm domestic scene.

**WITHDRAWN:** He's cooking alone. Efficient, no conversation. She offers to
help. "I've got it." She sets the table instead. The distance is a wall.

**WARM:** They've developed a cooking rhythm. He guides her hands while she
chops. Standing too close. "You're doing it wrong." "Show me then." His chest
against her back as he demonstrates.

**Choice Progression:**

| Tier | Choice Text | Conditions | Target | Effects |
|------|-------------|------------|--------|---------|
| T1 | Cook together, swap childhood kitchen stories. | Always | exit | affection +1 |
| T2 | He guides your hands while you chop. His chest warm against your back. | affection >= 25 + lingering_touch_unlock | node_t2 | affection +2 |
| T3 | Taste-testing from the same spoon. "How's that?" "Perfect." | affection >= 45 + flirt_unlock | node_t3 | affection +2 |
| T4 | He wipes sauce from your lip with his thumb. Lingers. | affection >= 65 + kiss_unlock | node_t4 | affection +3 |
| T5 | Dinner burns. Neither cares. The kitchen counter has many uses. | affection >= 85 + intimacy_unlock | node_t5 | affection +3, loop_terminal |

**Tier Nodes:** Progressive kitchen intimacy. T2 = guided hands (proximity). T3 =
sharing food (oral intimacy proxy). T4 = touching her lips (explicit desire). T5 =
counter sex (full). 1 media item per tier.

---

### Activity 8: DINNER WITH ETHAN
- **ID**: activity_dinner_ethan
- **Location**: loc_kitchen
- **Schedule**: 17:00-19:00
- **NPC**: npc_ethan
- **Priority**: 1
- **Max/Day**: 1
- **Unlock**: Always available

**Base Scene — DEFAULT:**
Dinner conversation. He asks about her dating life, she deflects. She asks about
the wedding, he deflects. Normal family dinner with undercurrents.

**WITHDRAWN:** Eating in silence. The scrape of forks. He checks his phone.
Madison's name flashes. He tilts the screen away. "Good dinner." "Thanks."

**WARM:** Wine with dinner. Conversation flows easily to the personal. Elbows
on the table. Leaning in. The world outside the kitchen doesn't exist.

**Choice Progression:**

| Tier | Choice Text | Conditions | Target | Effects |
|------|-------------|------------|--------|---------|
| T1 | Pleasant dinner conversation. Keep it light. | Always | exit | affection +1 |
| T2 | Second glass of wine. "Why'd you really stay away so long?" | affection >= 25 + lingering_touch_unlock | node_t2 | affection +2 |
| T3 | "You know why." His fork stops midway. The air changes. | affection >= 45 + flirt_unlock | node_t3 | affection +2, boldness +1 |
| T4 | Under the table, your foot finds his leg. Works its way up. | affection >= 65 + kiss_unlock | node_t4 | affection +3, boldness +2 |
| T5 | The table gets cleared in one sweep. | affection >= 85 + intimacy_unlock | node_t5 | affection +3, loop_terminal |

**Tier Nodes:** Dinner setting allows for conversation-based escalation (T2-T3)
before physical (T4-T5). Under-table footsie is classic FORBIDDEN driver content.
1 media item per tier.

---

### Activity 9: MOVIE NIGHT
- **ID**: activity_movie_night
- **Location**: loc_living
- **Schedule**: 19:00-22:00
- **NPC**: npc_ethan
- **Priority**: 1
- **Max/Day**: 1
- **Unlock**: Always available

**Base Scene — DEFAULT:**
Big couch, blanket, popcorn between them. Something on the flatscreen neither is
paying attention to. The couch is where things happen.

**WITHDRAWN:** He's in the chair, not the couch. Picks a documentary. Safe choice.
The distance feels intentional. She sits on the couch alone with the blanket.

**WARM:** No popcorn barrier. She's already under the blanket when he sits down.
He sits next to her instead of across. Their thighs touch immediately. Neither
pretends to watch the movie.

**Choice Progression:**

| Tier | Choice Text | Conditions | Target | Effects |
|------|-------------|------------|--------|---------|
| T1 | Watch the movie. Popcorn between you. Sibling movie night. | Always | exit | affection +1 |
| T2 | Get "cold." Scoot closer. Thighs touching under the blanket. | affection >= 25 + lingering_touch_unlock | node_t2 | affection +2 |
| T3 | Head on his shoulder. His arm around you. "Just like old times." But it's not. | affection >= 45 + flirt_unlock | node_t3 | affection +2 |
| T4 | Under the blanket, hands find each other. Then wander. | affection >= 65 + kiss_unlock | node_t4 | affection +3 |
| T5 | The movie's been paused for twenty minutes. The blanket hides everything. Then doesn't need to. | affection >= 85 + intimacy_unlock | node_t5 | affection +3, loop_terminal |

**Tier Nodes:**

**T2:** She scoots closer for warmth. Their legs press together under the blanket.
His body heat radiates. Neither adjusts away. 1 gif (couch proximity, blanket).

**T3:** Her head drifts to his shoulder. His arm settles around her. Familiar but
charged. "Just like we used to." "It doesn't feel like it used to." His fingers
trace patterns on her arm. 1 gif (head on shoulder, arm around her).

**T4:** Under the blanket, his hand finds her thigh. Innocent. Then higher. Her
hand finds his. Intertwines. Then moves to his leg. The movie is background noise.
Their breathing changes. 1 gif (under-blanket hands, tension).

**T5:** She climbs onto his lap. The blanket falls away. Neither cares anymore.
Couch sex — one of the core locations for the FORBIDDEN driver. The living room
where they watched cartoons as teenagers. 1 video (couch sex — her on top,
passionate, blanket discarded).

---

### Activity 10: WINE & TALK
- **ID**: activity_wine_talk
- **Location**: loc_living / loc_backyard
- **Schedule**: 19:00-22:00
- **NPC**: npc_ethan
- **Priority**: 1
- **Max/Day**: 1
- **Unlock**: Always available
- **Special**: Gives BOLDNESS at higher tiers (liquid courage).

**Base Scene — DEFAULT:**
A glass of wine on the patio. Catching up on years apart. Easy conversation,
starlit sky. The wine loosens tongues.

**WITHDRAWN:** One glass each. Safe topics. He nurses his drink. She fills the
silence. The stars are pretty. The conversation is not.

**WARM:** Second bottle. The conversation has wandered into territory that
daylight forbids. He's leaning back, relaxed, looking at her like she's the
answer to something. She's warm from wine and his attention.

**Choice Progression:**

| Tier | Choice Text | Conditions | Target | Effects |
|------|-------------|------------|--------|---------|
| T1 | One glass, easy conversation. Stargazing. | Always | exit | affection +1 |
| T2 | Second glass. "Do you ever think about...?" He doesn't finish. | affection >= 25 + lingering_touch_unlock | node_t2 | affection +2, boldness +1 |
| T3 | "I need to tell you something." Liquid courage. | affection >= 45 + flirt_unlock | node_t3 | affection +2, boldness +2 |
| T4 | "We shouldn't." "I know." But you're already leaning in. | affection >= 65 + kiss_unlock | node_t4 | affection +3, boldness +1 |
| T5 | The patio furniture is more private than the living room. Under the stars. | affection >= 85 + intimacy_unlock | node_t5 | affection +3, boldness +1, loop_terminal |

**Tier Nodes:** Wine + starlight = classic confession setting. The escalation moves
from loaded conversation to physical. The outdoor setting adds FORBIDDEN thrill
(exposure risk, even with privacy fence). 1 media item per tier.

---

### Activity 11: LATE NIGHT KITCHEN
- **ID**: activity_late_night_kitchen
- **Location**: loc_kitchen
- **Schedule**: 22:00-01:00
- **NPC**: npc_ethan
- **Priority**: 1
- **Max/Day**: 1
- **Unlock**: Always available

**Base Scene — DEFAULT:**
Both can't sleep. Midnight snack. The kitchen at 1 AM feels different — smaller,
more intimate. Whispers even though no one else is there. Comfortable silence
of insomniacs.

**WITHDRAWN:** He's at the fridge, staring into it. She appears and he startles.
"Just grabbing water." He takes the water and goes back upstairs. Brief.

**WARM:** He's waiting for her. Two glasses of milk already poured. "Couldn't
sleep either?" He knew she'd come. She always does. They've created a ritual.

**Choice Progression:**

| Tier | Choice Text | Conditions | Target | Effects |
|------|-------------|------------|--------|---------|
| T1 | Midnight snack. Comfortable silence. | Always | exit | affection +1 |
| T2 | He's in just boxers. You're in a thin nightgown. Pretend not to notice. | affection >= 25 + lingering_touch_unlock | node_t2 | affection +2 |
| T3 | "Can't sleep either?" The question is loaded. Both know why. | affection >= 45 + flirt_unlock | node_t3 | affection +2, boldness +1 |
| T4 | "I keep thinking about you." His whispered confession. Cross to him. | affection >= 65 + kiss_unlock | node_t4 | affection +3 |
| T5 | No one else is awake. No one will know. The kitchen floor, wherever. | affection >= 85 + intimacy_unlock | node_t5 | affection +3, loop_terminal |

**Tier Nodes:** The 1 AM kitchen is the most FORBIDDEN setting for the early game.
Darkness, sleep clothes, whispers. It's where secrets happen. The escalation from
"accidental insomnia" to "I came down hoping you'd be here" is the FORBIDDEN driver
in miniature. 1 media item per tier.

---

### Activity 12: SAYING GOODNIGHT
- **ID**: activity_goodnight
- **Location**: loc_hallway
- **Schedule**: 22:00-01:00
- **NPC**: npc_ethan
- **Priority**: 1
- **Max/Day**: 1
- **Unlock**: Always available

**Base Scene — DEFAULT:**
Bedroom doors. The goodnight ritual. Standing in the hallway between their rooms.
The moment stretches because neither wants to go in.

**WITHDRAWN:** Quick goodnight at the door. One-armed hug. "Sleep well." Door
closes. Distance maintained.

**WARM:** The hug lasts. Neither lets go. Standing in the hallway, foreheads
together. "Goodnight." The word doesn't mean goodnight anymore.

**Choice Progression:**

| Tier | Choice Text | Conditions | Target | Effects |
|------|-------------|------------|--------|---------|
| T1 | Quick goodnight. Sibling hug. Separate doors. | Always | exit | affection +1 |
| T2 | The hug lasts too long. He pulls back, looks at you. Reluctant release. | affection >= 25 + lingering_touch_unlock | node_t2 | affection +2 |
| T3 | "What if I can't sleep?" "Then come find me." Dangerous invitation. | affection >= 45 + flirt_unlock | node_t3 | affection +2, boldness +2 |
| T4 | He kisses you against your bedroom door. "We should stop." Neither stops. | affection >= 65 + kiss_unlock | node_t4 | affection +3 |
| T5 | Your door opens behind you. Or his. You don't separate long enough to notice which. | affection >= 85 + intimacy_unlock | node_t5 | affection +3, loop_terminal |

**Tier Nodes:** The hallway goodnight is pure FORBIDDEN driver. Bedroom doors 10
feet apart. The transition from "goodnight" to "your room or mine" is the arc of
the entire game in microcosm. 1 media item per tier.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION B: SOLO / UTILITY ACTIVITIES (8)

Solo activities have NO NPC trigger, are simpler (usually 1 node), and serve as
time advancement and light player stat management.

---

### Solo 1: SLEEP
- **ID**: solo_sleep
- **Location**: loc_player_room
- **Schedule**: Any time
- **Max/Day**: 2
- **Priority**: 1

1 node. "You lie down on the bed. The familiar ceiling, the old posters. So much
has changed, but this room feels like a time capsule."

Choices:
- "Take a short nap (1 hour)" → time +60 min, energy +20
- "Sleep until morning" → time +480 min (skips to next morning), energy = 100

---

### Solo 2: SHOWER
- **ID**: solo_shower
- **Location**: loc_bathroom
- **Schedule**: Any time
- **Max/Day**: 1
- **Priority**: 1

1 node. Hot water, steam, the mirror. A moment to decompress and process everything
that's happening. The shared bathroom means she can hear him in the hallway.

Choices:
- "Quick rinse" → time +15 min, energy +5
- "Long shower, let the water run" → time +30 min, energy +10

(NOTE: Bathroom encounters with Ethan are NOT part of the solo shower. Those are
handled by story events or woven into the narrative of NPC activity tier nodes.)

---

### Solo 3: GET READY
- **ID**: solo_get_ready
- **Location**: loc_bathroom
- **Schedule**: Any time
- **Max/Day**: 1
- **Priority**: 1

1 node. Mirror, makeup, clothes. Choosing what to wear — knowing who will see.
"You spend more time getting ready than you used to. You tell yourself it's just
because you're on vacation."

Choices:
- "Keep it casual" → time +15 min
- "Put in effort today" → time +30 min, boldness +2

---

### Solo 4: UNPACK
- **ID**: solo_unpack
- **Location**: loc_player_room
- **Schedule**: Any time
- **Max/Day**: 1
- **Priority**: 1
- **Special**: Only available on Day 1 (condition: game_started + NOT arrival_complete... actually this fires after arrival). Available once, not repeatable.
- **is_repeatable**: false

1 node. Unpacking in her old room. Finding things she left behind — an old
journal, a photo strip from the mall with Ethan. Settling back into a space that's
hers but isn't anymore.

Exit: time +60 min, boldness +2 (she's committing to being here).

---

### Solo 5: PHONE SCROLL
- **ID**: solo_phone_scroll
- **Location**: loc_player_room
- **Schedule**: Any time
- **Max/Day**: 2
- **Priority**: 1

1 node. Time-killer. Scrolling social media, texting friends, avoiding what she
should be thinking about. "Your friend asks how the trip is. 'Fine,' you type.
Delete it. 'Complicated.' Delete that too. 'Fine.'"

Exit: time +30 min. No stat changes.

---

### Solo 6: SWIM ALONE
- **ID**: solo_swim_alone
- **Location**: loc_backyard
- **Schedule**: 14:00-17:00
- **Max/Day**: 1
- **Priority**: 1

1 node. Swimming laps alone. The pool is different when he's not here — peaceful,
meditative. The sun on her skin. Floating and thinking.

Exit: time +45 min, energy +10.

---

### Solo 7: WANDER
- **ID**: solo_wander
- **Location**: loc_hallway
- **Schedule**: Any time
- **Max/Day**: 1
- **Priority**: 1

1 node. Walking through the house. Looking at family photos in the hallway.
Peeking into rooms. The house is a museum of their shared childhood. "You pass
his door. It's open a crack. You keep walking."

Exit: time +15 min. Light exploration.

---

### Solo 8: JOURNAL
- **ID**: solo_journal
- **Location**: loc_player_room
- **Schedule**: Any time
- **Max/Day**: 1
- **Priority**: 1

1 node. Writing in the journal she found while unpacking. Processing the day.
"You write about the house, the weather, the food. You don't write about the
way his hand felt on your back. But you think about it for the rest of the page."

Exit: time +30 min. No stat changes (the processing is its own reward).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ACTIVITY SUMMARY TABLE

### NPC Activities (12)

| # | Activity | Location | Time | Stat | Special |
|---|----------|----------|------|------|---------|
| 1 | Breakfast with Ethan | loc_kitchen | 07:00-09:00 | affection | — |
| 2 | Morning Coffee | loc_kitchen | 07:00-09:00 | affection | — |
| 3 | Helping with Chores | loc_living | 09:00-12:00 | affection | — |
| 4 | Lunch Together | loc_kitchen | 12:00-14:00 | affection | — |
| 5 | Pool Time | loc_backyard | 14:00-17:00 | affection | boldness at T2-T3 |
| 6 | Wedding Planning | loc_backyard | 14:00-17:00 | affection | guilt at all tiers |
| 7 | Cooking Together | loc_kitchen | 17:00-19:00 | affection | — |
| 8 | Dinner with Ethan | loc_kitchen | 17:00-19:00 | affection | boldness at T3-T4 |
| 9 | Movie Night | loc_living | 19:00-22:00 | affection | — |
| 10 | Wine & Talk | loc_living | 19:00-22:00 | affection | boldness at T2-T5 |
| 11 | Late Night Kitchen | loc_kitchen | 22:00-01:00 | affection | boldness at T3 |
| 12 | Saying Goodnight | loc_hallway | 22:00-01:00 | affection | boldness at T3 |

### Solo Activities (8)

| # | Activity | Location | Repeatable | Main Effect |
|---|----------|----------|------------|-------------|
| 1 | Sleep | loc_player_room | Yes (2/day) | Time skip, energy |
| 2 | Shower | loc_bathroom | Yes (1/day) | Time skip, energy |
| 3 | Get Ready | loc_bathroom | Yes (1/day) | boldness +2 |
| 4 | Unpack | loc_player_room | No (once) | boldness +2 |
| 5 | Phone Scroll | loc_player_room | Yes (2/day) | Time skip |
| 6 | Swim Alone | loc_backyard | Yes (1/day) | Time skip, energy |
| 7 | Wander | loc_hallway | Yes (1/day) | Exploration |
| 8 | Journal | loc_player_room | Yes (1/day) | Processing |

### Total Canvas Count

| Type | Count |
|------|-------|
| NPC Activities (repeatable) | 12 |
| Solo Activities | 8 (7 repeatable + 1 one-time) |
| Story Canvases (from Phase 4) | 19 |
| Ending Canvases (from Phase 4) | 4 |
| **TOTAL** | **43** |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
