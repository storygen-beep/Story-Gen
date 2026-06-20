===============================================================================
                    PHASE 2: CHARACTERS & STAT ECONOMY
===============================================================================

Define the characters and the mechanical systems that drive progression.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Section 1: Player Definition

**Name**: You (player-named or unnamed — referred to in second person)
**Age**: Early 20s
**Gender**: Female
**Description**: A young woman in her early 20s, returning home after two years
away. Slim build, expressive eyes. Dresses casually — jeans and t-shirts, sundresses
in the heat. Old enough to know better, young enough to not care.

**Starting Stats**:
- boldness = 20 (she came home, which took nerve, but she's still guarded)
- energy = 100

**Background**:
Her parents married Ethan's dad when she was twelve. She spent eight years growing
up in this house with a step-brother who made her feel things she wasn't supposed
to feel. She never acted on it. Instead, she left — college across the country,
two years without coming home. She told herself it was about independence. It was
about running.

Now she's back for his wedding. She told herself she could handle it. She was wrong
the moment he opened the door.

### Player Psychology (REQUIRED)

- **Want**: To get through these two weeks without destroying anything — the family,
  the wedding, her own carefully constructed distance. She wants to prove she's "over it."
- **Need**: To stop running. She needs to face what she feels instead of burying it.
  Whether that means pursuing it or genuinely letting go, she needs honesty — with
  herself and with Ethan.
- **Fear**: That she'll act on her feelings and ruin everything — his marriage, the
  family, his life. But deeper: that she'll act on them and he won't feel the same,
  and she'll have destroyed everything for nothing.
- **Flaw**: She rationalizes. She's brilliant at constructing reasons why she should
  do the thing she wants to do anyway. "I'm just being friendly." "This is normal."
  "One more time won't matter." Her rationalization lets her cross lines while
  maintaining the fiction that she hasn't.

### Player Emotional Phases (REQUIRED)

| Phase | Triggered By | Player Mindset | How It Shows in Narration |
|-------|-------------|----------------|--------------------------|
| DENIAL | Arrival (scene_arrival) | "I'm over it. This is fine." | Controlled prose, focuses on the house not on Ethan. Notes changes to avoid noting him. Short, clipped observations. |
| REMEMBERING | Welcome Dinner / Old Photos | Nostalgia cracks the armor | Memories intrude mid-sentence. Past tense mixes with present. "He used to — he still does that." Longer, warmer descriptions. |
| WANTING | Sleepless Night / The Couch | Can't pretend anymore | Narration becomes charged. Physical details (his hands, his jaw, his breath). Catches herself staring. Internal commentary: "Don't." But she doesn't stop. |
| RECKLESS | Confession / First Kiss | Past the point of caring | Shorter sentences, more present-tense. Less rationalization, more action. "I kissed him. I'd do it again." |
| DESPERATE | First Night / Madison Arrives | The clock is real now | Urgency bleeds into narration. Time references everywhere ("three days left," "tomorrow"). Wants to hold onto moments. Greedy for details. |
| RESOLVED | Night Before / Wedding Morning | Whatever happens, she chose | Calm clarity. Honest. No more rationalizing. "I love him. That's the truth. Everything else is just what happens next." |

### Player Internal Voice (REQUIRED)

**What player notices (evolves over time):**
| Phase | Notices | Example |
|-------|---------|---------|
| DENIAL | The house, changes, neutral details | "The couch is new. The photos are the same." |
| REMEMBERING | Ethan's habits, what hasn't changed | "He still leaves his coffee cup in the sink. Some things don't change." |
| WANTING | His body, proximity, charged details | "He reached past me for the shelf. His arm brushed mine. I forgot what I was looking for." |
| RECKLESS | Opportunities, risks, what they could get away with | "Madison's name on his phone. The hallway is empty. His door is open." |
| DESPERATE | Time, loss, what she'll miss | "Three days. Seventy-two hours. I'm counting in heartbeats now." |
| RESOLVED | Truth, clarity, acceptance | "He's standing at the altar. I love him. Both things are true." |

**How player describes Ethan (evolves over time):**
| Phase | Description Style | Example |
|-------|------------------|---------|
| DENIAL | Controlled, factual, deflects | "He looks good. Taller. Or maybe I forgot. Doesn't matter." |
| REMEMBERING | Nostalgic, tender, slipping | "He still does that thing with his eyes when he's thinking. I used to watch him study like this." |
| WANTING | Physical, detailed, honest | "The way his t-shirt pulls across his shoulders. The warmth of his hand when it touches mine. The way his voice drops when we're alone." |
| RECKLESS | Possessive, urgent | "His mouth. Mine. Finally." |
| DESPERATE | Intimate, grieving in advance | "He sleeps with his arm around me like he's afraid I'll leave. I'm afraid of the same thing." |
| RESOLVED | Simple, certain | "Ethan." (That's enough. That's everything.) |

**Choice text framing (evolves over time):**
| Phase | Choice Tone | Example |
|-------|------------|---------|
| DENIAL | Safe, deflecting | "Change the subject" / "Make a joke" |
| REMEMBERING | Warm, testing | "Ask about old times" / "Keep it surface-level" |
| WANTING | Charged, risking | "Move closer" / "Stay where you are" |
| RECKLESS | Bold, pursuing | "Kiss him" / "\"We shouldn't.\" But don't pull away" |
| DESPERATE | High-stakes, raw | "\"Choose me.\"" / "\"I'll always love you. Whatever you decide.\"" |
| RESOLVED | Honest, final | "\"I love you.\"" / "Let him go" |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Section 2: NPC Definition — ETHAN

**ID**: npc_ethan
**Name**: Ethan
**Role**: Step-Brother / Love Interest
**Age**: Late 20s
**Driver**: FORBIDDEN (primary) + LOVE (secondary)
**Primary Stat**: affection (maps to tension + love driver combination)

### Physical Appearance

Tall, athletic build maintained from college sports. Broad shoulders that fill
doorframes. Warm brown eyes that crinkle at the corners when he smiles — the kind
of eyes that make you feel seen. Hair perpetually slightly disheveled, like he just
ran his fingers through it. Strong jaw with a day or two of stubble he doesn't
bother shaving when Madison isn't around.

At home: worn gray t-shirts, joggers, bare feet. Morning: shirtless with coffee,
sleep-rumpled. Going out: cleans up well — button-down, rolled sleeves revealing
forearms. Pool: board shorts, water running down his chest.

What makes him physically attractive: the contrast between his size and his
gentleness. He's big enough to be imposing but moves carefully, like he's
always aware of the space he takes up. His hands are large and capable, and he
touches things — and people — with deliberate care.

### Personality Traits

**Surface traits (what people see):**
- Protective older brother energy — opens doors, carries bags, checks locks
- Genuinely kind — remembers birthdays, cooks your favorite meal, asks real questions
- Conflict-avoidant — keeps the peace, smooths things over, lets things slide
- Warm humor — dry observations, self-deprecating, makes you laugh without trying

**Hidden traits (what emerges over time):**
- Deeply sentimental — kept the photo albums, remembers small details from years ago
- Emotionally trapped — he proposed to Madison because it was "the right thing to do,"
  not because he couldn't live without her
- Physically restrained — wants desperately but holds back, which makes the moments he
  breaks feel seismic
- Self-sacrificing to a fault — will destroy himself to avoid hurting others, which
  paradoxically hurts everyone more

### Psychology

Ethan buried his feelings for his step-sister the same way she did — by constructing
a life that made them impossible. Madison is that construction. She's safe, appropriate,
what his life "should" look like. He proposed not from overwhelming love but from the
absence of a reason not to. He is, at his core, a man who does what he's supposed to do.

The player's return detonates all of that. Not because she tries to — because she
doesn't have to. Her presence alone reminds him of the version of himself he locked
away. He's terrified of being the kind of man who leaves his fiancée for his step-sister.
He's more terrified of being the kind of man who marries the wrong woman because he's
too much of a coward to admit the truth.

**How he responds to intimacy**: Desperately, then with immediate guilt. He wants physical
closeness with every fiber but pulls back the moment it happens. The push-pull is genuine —
he's not playing games, he's at war with himself.

**How he responds to vulnerability**: He becomes quieter. Less defensive. When the player
shows him real honesty ("I've always felt this"), his walls come down faster than when
she pushes physically. Emotional vulnerability unlocks him more than physical escalation.

### Internal Contradictions (REQUIRED)

1. **He wants to be a good man BUT a good man wouldn't feel what he feels.**
   He's built his identity around being reliable, dutiful, the one who does the
   right thing. His feelings for his step-sister make him question everything he
   believes about himself. Every moment of desire is also a moment of self-betrayal.

2. **He wants the player BUT he doesn't want to be the kind of man who cheats.**
   The desire is real but so is the guilt. He's not just torn between two women —
   he's torn between two versions of himself. The version who honors commitments
   and the version who honors his heart.

3. **He craves honesty BUT fears the consequences of truth.**
   He wants to say "I love you, I've always loved you." But saying it means
   blowing up the wedding, devastating Madison, splitting the family. So he
   says "I should go to bed" when he means "I want to stay."

**How contradictions drive story events:**
- Contradiction 1 peaks in "The Real Talk" — he breaks down, admits he doesn't know
  if he can go through with the wedding. His identity crisis is visible.
- Contradiction 2 peaks in "Madison Arrives" — he has to perform the loving fiancé
  while the player watches, and the mask doesn't fit anymore.
- Contradiction 3 peaks in "Night Before Wedding" — the last chance for truth. What
  he says (or doesn't say) determines the ending.

### Resistance Pattern (REQUIRED)

| Stage | Resistance Behavior | What Triggers It | Recovery |
|-------|-------------------|-----------------|----------|
| MILD | Creates physical distance. "I should go check on dinner." Changes subject to wedding details. Calls her "sis" (a deliberate downgrade). | After first loaded moment (Old Photos, Sleepless Night) | Returns to normal within hours. Next conversation, he's warmer than before — the resistance was a reflex, not a decision. |
| MODERATE | Avoids being alone with her. Brings up Madison deliberately. Spends a morning at his laptop "working." Cold for a half-day. | After The Couch or Confession — the first time he can't deny what's happening. | Comes to her. Doesn't apologize but stands too close. "I was being stupid." The distance was punishment aimed at himself, not her. |
| SEVERE | Confrontation. "This has to stop." Direct eye contact, pained voice. Sleeps with his door locked. | After First Night — the guilt of having actually crossed the line. Morning-after crisis of "what have I done." | Returns within a day. Not with words but with action — shows up in her doorway. "I tried to stop. I can't." The resistance breaks because the alternative (pretending) is worse. |

**Key resistance principle**: Ethan's resistance is always aimed at himself, never at the
player. He's not rejecting her — he's trying to be the man he thinks he should be. This
is why his resistance crumbles: he keeps losing the argument with himself.

### Emotional Quadrant Behaviors (REQUIRED)

| Quadrant | Ethan's Specific Behaviors |
|----------|---------------------------|
| DISTANT (low affection / low trust — Days 1-2 baseline) | Makes coffee for one, then awkwardly makes a second when she appears. Fills silence with logistics ("towels are in the hall closet"). Hugs are brief and one-armed. Calls her by her name in full, not nicknames. Sits in the chair, not on the couch next to her. |
| SAFE (low affection / high trust — if player builds trust without romance) | Asks real questions: "How's your life? Really?" Saves her a plate if she's late. Sits on the couch but with a cushion between them. Talks about Madison naturally, without defensiveness. Comfortable silences. |
| CONFLICTED (high affection / low trust — if player pushes physically without emotional buildup) | Watches her from across the room, then looks away when caught. Cooks elaborate meals but serves them without eye contact. Starts sentences with "Look, I—" then redirects. Stands too close in the kitchen, then steps back and apologizes. Brings up Madison unprompted (guilt shield). |
| OPEN (high affection / high trust — where the story should land by mid-Act 2) | Sits next to her, not across from her. Touches her arm during conversation — small, natural. Laughs openly. Lets her see him stressed about the wedding without performing composure. Says "I'm glad you're here" and means something bigger. Leaves his bedroom door open when he's changing. |

### Emotional Tells by Stat Range (REQUIRED)

**Affection Tells (Primary Stat):**
| Range | Observable Behavior |
|-------|-------------------|
| 0-20 (DISTANT) | Makes coffee in silence. One-armed hug goodnight. Eyes slide away when they land on her too long. Safe topics only: weather, work, "how's your flight." |
| 21-40 (WARMING) | Remembers how she takes her coffee. Hugs linger a half-second longer. Finds reasons to be in the same room. Asks "do you remember when..." unprompted. |
| 41-60 (CHARGED) | Stops pretending not to look. Finds excuses to touch — passing dishes, applying sunscreen, showing her something on his phone. Pauses mid-sentence when she walks in. Drops his voice when they're alone. |
| 61-80 (TIPPING) | Doesn't step back when they're close. His hand on the small of her back, lingering. Texts her from upstairs: "Can't sleep either?" Says "you" instead of "we" when talking to Madison on the phone — slips. |
| 81-100 (GONE) | Pulls her into him without thinking. Kisses her shoulder as he passes. Stops mid-conversation to just look at her. "Stay" is all he says. His hands shake when he touches her, not from nerves but from restraint breaking. |

**Guilt Tells (Secondary Stat):**
| Range | Observable Behavior |
|-------|-------------------|
| 0-15 (LOW) | Relaxed, present. Guilt exists as background hum, easily ignored. Can laugh, can flirt, can be in the moment without a shadow. |
| 16-30 (MODERATE) | Madison's name lands like a stone in conversation. He goes quiet after phone calls. Rubs the back of his neck — his tell for shame. Shifts the engagement ring on the counter (doesn't wear it at home). |
| 31-50 (HIGH) | Pulls away after physical moments — not immediately, but within minutes. "We shouldn't have done that." Avoids her eyes in the morning. Over-compensates: talks to Madison on the phone longer than necessary while the player can hear. |
| 51-70 (CRISIS) | Visible internal torment. Sits alone in the dark. Drinks more. Short-tempered about small things (displaced guilt). "I'm a terrible person" spoken to himself, not to her. |
| 71+ (PARALYZED) | Unable to choose. Physically present but emotionally frozen. Can't touch the player without wincing. Can't talk to Madison without lying. The guilt has become its own cage — he can't move in any direction. (This level gates certain endings.) |

### Speech Patterns

**Baseline**: Medium-length sentences, warm cadence. Uses contractions. Says "you know"
as a filler. Self-deprecating humor: "I'm basically a disaster in a button-down." Asks
questions instead of making statements when he's unsure: "Do you remember...?" instead
of "Remember when..."

**What he says vs. what he means:**
| He Says | He Means |
|---------|----------|
| "It's really good to see you." | "I wasn't ready for what seeing you would do to me." |
| "Madison's great. Really." | "I'm trying to convince myself as much as you." |
| "We should probably go to bed." | "I want to stay here with you forever." |
| "I should go check on dinner." | "If I stay this close to you I'm going to do something I can't take back." |
| "This has to stop." | "I don't want this to stop and that terrifies me." |
| "I'm fine." | Nothing about this is fine. |

**How speech changes as relationship deepens:**
- **Low affection**: Complete sentences. Polite. Keeps conversation moving to avoid
  silence. "Do you need anything? Extra towels in the closet."
- **Mid affection**: Sentences get shorter around her. More comfortable with silence.
  Starts sentences he doesn't finish: "I've been meaning to—" "Never mind."
- **High affection**: Drops pretense. "I can't stop thinking about you." Says her name
  more often — not to get her attention, but because saying it feels like something.
- **Post-intimacy**: Quieter. Touch replaces words. "Hey" means "I love you." "Come
  here" is a complete conversation.

### Starting Stats

| Stat | Start Value | Notes |
|------|-------------|-------|
| affection | 15 | Pre-existing fondness from shared history (not zero — they have 8 years of connection) |
| guilt | 10 | Baseline awareness that his feelings are "wrong" (he's engaged, she's his step-sister) |

### Flags
- `comfortable` — set when player builds enough rapport in Act 1
- `interested` — set after first overt romantic moment
- `vulnerable` — set after The Real Talk (he opens up emotionally)
- `intimate` — set after First Night Together

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Section 2b: Secondary NPC — MADISON

**ID**: npc_madison
**Name**: Madison
**Role**: Ethan's Fiancée (antagonist by circumstance, NOT a villain)
**Age**: Late 20s
**Appears**: Days 13-14 only

### Description
Polished, put-together, warm. She greets the player with genuine friendliness.
She's not a caricature — she's a real person who doesn't deserve what's happening.
Her function is to make the player (and Ethan) feel the weight of their choices.

### How She Functions in the Game
- **Days 1-12**: Absent but present. Her things are in Ethan's room. Her photo is
  on the nightstand. She calls occasionally, creating guilt spikes for Ethan.
  She exists as a concept — "the fiancée" — not a character.
- **Day 13**: She arrives. Suddenly she's a real person with a real smile and real
  excitement about the wedding. This transforms abstract guilt into concrete betrayal.
- **Day 14**: Wedding day. Her presence forces the final confrontation.

### Why She's NOT a Villain
If Madison were awful, the player's choices would be easy and the game would be
shallow. She's nice, which is precisely the problem. The player has to grapple
with "I'm not hurting a bad person — I'm hurting a good one." This is where the
FORBIDDEN driver gets its weight.

### Stats
- `presence = 0` (non-interactive stat — tracks whether she's arrived)
- No relationship stats — player doesn't build a relationship with Madison

### Schedule (Days 13-14 only)
| Time | Location | Activity |
|------|----------|----------|
| 01:00-08:00 | loc_ethan_room | Sleeping |
| 08:00-12:00 | loc_kitchen | Wedding preparations |
| 12:00-22:00 | loc_living | Finalizing wedding details |
| 22:00-01:00 | loc_ethan_room | Getting ready for bed |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Section 3: Stat Economy Design

This game has NO money, rent, or economic pressure system. The economy is purely
emotional — affection, boldness, and guilt. There's no job, no shop, no financial
motivation. The driver is emotional, not economic.

### Primary NPC Stat: Affection (npc_ethan)

**Range**: 0-100
**Starting Value**: 15
**Purpose**: Primary progression gate. Determines content tier access (with flags)
and ending eligibility.

**Growth Sources:**
| Source | Gain | Frequency | Notes |
|--------|------|-----------|-------|
| Activity base choice (T1) | +1 | Per activity | Always available |
| Activity warm choice (T2) | +2 | Per activity | Requires dual gate |
| Activity flirt/tease choice (T3) | +2 | Per activity | Requires dual gate |
| Activity foreplay choice (T4) | +3 | Per activity | Requires dual gate |
| Activity explicit choice (T5) | +3 | Per activity | Requires dual gate |
| Story event (minor choice) | +2-3 | One-time | Warm dialogue option |
| Story event (major choice) | +5-8 | One-time | Bold/pursuing option |
| Story event (bold choice) | +8-10 | One-time | Rare — kiss him, "choose me" |

**Negative sources:**
| Source | Loss | Notes |
|--------|------|-------|
| Distant/safe story choice | -3 to -5 | "We forget I said that," "This can't happen" |
| Rejection choice | -5 to -10 | "Maybe you should go through with it" |

**Target Progression:**
| Day Range | Affection Target | Via Activities | Via Story Events |
|-----------|-----------------|----------------|------------------|
| Day 1-3 | 15 → 35 | ~8 (8 T1 activities × +1) | ~12 (arrival, dinner, photos, sleepless) |
| Day 4-6 | 35 → 55 | ~12 (6 T1 + 6 T2 × avg +1.5) | ~8 (madison calls, couch) |
| Day 7-9 | 55 → 75 | ~10 (mix T2/T3 × avg +2) | ~10 (confession, almost kiss, real talk) |
| Day 9-11 | 75 → 90 | ~8 (mix T3/T4 × avg +2.5) | ~7 (first kiss, what are we doing) |
| Day 11-12 | 90 → 95+ | ~3 (T4/T5 × +3) | ~5 (first night, morning after) |

**Activity contribution**: ~55% of total gains
**Story event contribution**: ~45% of total gains

### Player Stat: Boldness

**Range**: 0-100
**Starting Value**: 20
**Purpose**: Measures how directly the player pursues what she wants. Affects choice
availability and ending eligibility.

**Growth Sources:**
| Source | Gain | Notes |
|--------|------|-------|
| Bold dialogue choices | +3-5 | "You look good. Really good." / "Then have me." |
| Initiating physical contact | +5 | "Kiss him" / "Pull him closer" / "Move closer" |
| Direct confrontation choices | +5-8 | "Do you love her?" / "Choose me." |
| Solo activity (get ready) | +2 | Grooming/preparation |

**How boldness affects gameplay:**
- **Low boldness (< 40)**: Player is reactive. Ethan must initiate physical moments.
  Choice text is cautious: "Let him lead." "Wait for a signal."
- **Mid boldness (40-69)**: Player can meet him halfway. Choices split evenly between
  pursuing and responding. "Move closer" alongside "Let him come to you."
- **High boldness (70+)**: Player becomes the pursuer. Unlocks aggressive choice text:
  "Pull him into the bedroom." "Kiss him first." Required for "He Chooses You" ending
  (the player's boldness gives him permission to break free).

### NPC Stat: Guilt (npc_ethan)

**Range**: 0-100
**Starting Value**: 10
**Purpose**: Creates tension, affects dialogue options, determines ending path.
Guilt is NOT a "bad" stat — it's a tension stat that adds emotional weight.

**Growth Sources:**
| Source | Gain | Notes |
|--------|------|-------|
| Madison phone calls (story event) | +5-10 | Being reminded of the woman he's betraying |
| Wedding planning activity choice | +2-3 | When player helps with his fiancée's wedding |
| Post-intimacy moments | +5-10 | Story-event guilt after crossing physical lines |
| "What about Madison?" dialogue | +3-5 | When player forces him to confront the betrayal |

**Reduction Sources:**
| Source | Loss | Notes |
|--------|------|-------|
| Deep emotional conversation | -3-5 | When they connect honestly, guilt recedes briefly |
| Player reassurance | -2-3 | "No regrets" / "I don't care about right and wrong" |
| Bold "push through" choices | -5 | "Stop thinking. Just feel." — overrides guilt with desire |

**How guilt affects gameplay:**
- **Low guilt (< 30)**: Cleaner romance. He's present, passionate, not looking over
  his shoulder. Dialogue is warm without shadows. Leads to "He Chooses You" if
  boldness is also high.
- **Mid guilt (30-50)**: Complicated emotions. Post-intimacy scenes have tension.
  He says "we shouldn't" but doesn't stop. This is the intended default zone.
- **High guilt (50-70)**: He pulls away after physical moments. Short-tempered.
  Overcompensates on phone with Madison. But still comes back. Leads to
  "One Last Night" ending — loves her but can't leave.
- **Very high guilt (70+)**: Paralyzed. Can't enjoy the relationship or end it.
  Leads to "The Arrangement" if boldness is high (they continue in secret) or
  "What Could Have Been" if boldness is low (he goes through with the wedding
  and they lose each other).

### Stat Interaction Matrix

| Condition | Effect on Game |
|-----------|---------------|
| High affection + High boldness + Low guilt | Best ending: "He Chooses You" |
| High affection + High guilt (any boldness) | "One Last Night" — loves her, marries Madison |
| High affection + High guilt + High boldness | "The Arrangement" — marries Madison, continues affair |
| Mid affection OR Low boldness | "What Could Have Been" — neither was brave enough |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Section 4: Gate Flag Design

Every activity escalation tier requires BOTH a stat threshold AND a narrative gate
flag set by a prior story event. This ensures the player has "narratively experienced"
a behavior before it becomes repeatable in activities.

### Gate Flags

| Gate Flag | Set By (Story Event) | Approx. Day | Stat at Event | Unlocks |
|-----------|---------------------|-------------|---------------|---------|
| lingering_touch_unlock | scene_old_photos OR scene_sleepless_night | Day 2-3 | affection ~25 | T2: Suggestive touches in activities |
| flirt_unlock | scene_the_couch OR scene_confession | Day 5-7 | affection ~45 | T3: Intentional teasing/flirtation in activities |
| kiss_unlock | scene_first_kiss | Day 8-9 | affection ~70 | T4: Kissing, intimate touching in activities |
| intimacy_unlock | scene_first_night | Day 10 | affection ~90 | T5: Full explicit content in activities |

### Dual Gating Per Activity Tier

| Tier | Stat Threshold | Flag Required | Content Level |
|------|---------------|---------------|---------------|
| T1: Ambient | Always available | None | Casual interaction. Sibling energy. Comfortable. |
| T2: Suggestive | affection >= 25 | lingering_touch_unlock | Lingering looks, proximity that's unnecessary, "accidental" touches. |
| T3: Teasing | affection >= 45 | flirt_unlock | Intentional flirting, provocative comments, testing boundaries. |
| T4: Foreplay | affection >= 65 | kiss_unlock | Kissing, hands exploring, pressing close. "We shouldn't." |
| T5: Explicit | affection >= 85 | intimacy_unlock | Full intimate encounters. No more pretending. |

### Why Dual Gating Matters for This Game

Without flags, a player could grind breakfast conversations to affection 90 and suddenly
get explicit content with no narrative build-up. With dual gating:
- Affection 90 + no kiss_unlock flag = still stuck at T3 (teasing) in activities
- The player MUST progress through the story chain to unlock higher activity tiers
- This creates a natural rhythm: story event pushes boundary → activities let you
  explore that new level repeatedly → next story event pushes further

### How Gate Flags Propagate

When `kiss_unlock` is set by scene_first_kiss, it becomes available across ALL
activities simultaneously. This means:
- First kiss happens during Wine & Talk on the patio (story canvas)
- Next morning, Breakfast with Ethan now offers T4 (foreplay) choices
- That same day, Pool Time also offers T4 choices
- The player narratively "learned to kiss" and now it's available everywhere

This is the Single-NPC version of the shared unlock flag system. Same concept,
one NPC instead of many.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Section 5: Complete Flag Inventory

### Story Progression Flags (set by story canvases, gate the next story canvas)

| Flag | Set By | Gates |
|------|--------|-------|
| game_started | scene_arrival | General game state |
| arrival_complete | scene_arrival | scene_welcome_dinner |
| welcome_dinner_complete | scene_welcome_dinner | scene_old_photos |
| old_photos_complete | scene_old_photos | scene_sleepless_night |
| sleepless_night_complete | scene_sleepless_night | scene_madison_calls |
| madison_calls_complete | scene_madison_calls | scene_the_couch |
| the_couch_complete | scene_the_couch | scene_confession |
| confession_complete | scene_confession | scene_almost_kiss |
| almost_kiss_complete | scene_almost_kiss | scene_real_talk |
| real_talk_complete | scene_real_talk | scene_first_kiss |
| first_kiss_done | scene_first_kiss | scene_what_are_we_doing |
| what_are_we_doing_done | scene_what_are_we_doing | scene_first_night |
| first_night_complete | scene_first_night | scene_morning_after |
| morning_after_complete | scene_morning_after | scene_cant_stay_away |
| cant_stay_away_complete | scene_cant_stay_away | scene_madison_arrives |
| madison_arrived | scene_madison_arrives | scene_stolen_moment |
| stolen_moment_complete | scene_stolen_moment | scene_night_before_wedding |
| night_before_complete | scene_night_before_wedding | scene_wedding_morning |
| wedding_morning_done | scene_wedding_morning | Ending canvases |

### Gate Flags (set by story canvases, gate activity tiers)

| Flag | Set By | Gates |
|------|--------|-------|
| lingering_touch_unlock | scene_old_photos | Activity T2 (suggestive) |
| flirt_unlock | scene_the_couch | Activity T3 (teasing) |
| kiss_unlock | scene_first_kiss | Activity T4 (foreplay) |
| intimacy_unlock | scene_first_night | Activity T5 (explicit) |

### NPC State Flags (set by story canvases, track Ethan's relationship state)

| Flag | Set By | Meaning |
|------|--------|---------|
| ethan_comfortable | scene_welcome_dinner | Ethan is relaxed around player |
| ethan_interested | scene_the_couch | Ethan's interest is overt |
| ethan_vulnerable | scene_real_talk | Ethan has opened up emotionally |
| ethan_intimate | scene_first_night | Physical relationship established |

### Note on Flag Ownership

All flags above are set on `player` (targetType = "player") for simplicity. The NPC
state flags are named with the `ethan_` prefix for clarity but are stored on the player
entity because the engine tracks flags on the player object. NPC trait values (affection,
guilt) are tracked on the NPC entity via the stat system, not via flags.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Section 6: Ending Requirements Summary

| Ending | Affection | Boldness | Guilt | Priority | Tone |
|--------|-----------|----------|-------|----------|------|
| He Chooses You | >= 95 | >= 70 | < 50 | 10 (highest) | Triumphant but complicated |
| The Arrangement | >= 85 | >= 60 | >= 70 | 8 | Dark, ongoing affair |
| One Last Night | >= 80 | any | >= 60 | 6 | Bittersweet sacrifice |
| What Could Have Been | any | any | any | 1 (fallback) | Melancholy, missed chance |

**Priority ordering ensures mutual exclusivity.** If a player qualifies for multiple
endings, the highest-priority one fires. "What Could Have Been" is the fallback —
it has no stat requirements beyond `wedding_morning_done` and fires only if no
other ending qualifies.

**Design intent:**
- "He Chooses You" requires HIGH affection + HIGH boldness + LOW guilt. The player
  must have pursued aggressively (boldness), built deep connection (affection), AND
  managed the guilt (kept it under 50 by choosing dialogue that reduces guilt or
  avoids guilt-building situations).
- "The Arrangement" requires HIGH guilt + HIGH boldness. The player pushed hard but
  let guilt accumulate. Ethan loves her but can't break free — so they continue in
  shadows.
- "One Last Night" requires HIGH affection + HIGH guilt. They love each other but
  the guilt wins. He goes through with the wedding. She leaves.
- "What Could Have Been" catches everyone else — players who didn't invest enough
  in either direction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
