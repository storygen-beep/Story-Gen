# Game Depth Design Document

This document captures design philosophy and features for creating **meaningful gameplay depth** - not through more mechanics, but through richer storytelling, obstacles, and emotional weight.

**Core Principle**: More features ≠ more systems. It means deeper stories, meaningful obstacles, and choices that matter.

---

## Philosophy: What Creates Engagement

| Mechanical Depth (Avoid) | Emotional Depth (Pursue) |
|--------------------------|--------------------------|
| 10 NPCs with schedules | 1 NPC with a real arc you care about |
| Affection bar 0→100 | A moment where she opens up about her past |
| 5 relationship states | An argument that actually hurt, and making up |
| Progress trackers everywhere | A choice you genuinely struggled with |

**The Problem with Pure Mechanics:**
```
Current loop:
  Go to location → Do activity → +10 affection → Repeat → Next tier
```
This is **grinding**, not **storytelling**. Players optimize resources, not make meaningful choices.

---

## Three Pillars of Depth

1. **Story-Driven Obstacles** - NPCs have problems, conflicts arise naturally
2. **Player Skill Challenges** - Dialogue puzzles, memory tests, timed moments
3. **Emotional Weight in Choices** - Decisions that matter and echo forward

---

## Implemented Features

### Event Pacing with `days_since_flag` ✅

**Status:** Implemented

Adds time-based conditions to enforce realistic pacing between story events.

**Problem Solved:** Without this, completing Event 1 immediately unlocks Event 2 (same minute). Now events can require time gaps.

**TOML Usage:**
```toml
[canvases.trigger.conditions]
version = "1.0"
logic = "AND"
items = [
  { type = "flag", subject = "player", flag_key = "first_date_complete", operator = "is_true" },
  { type = "days_since_flag", subject = "player", flag_key = "first_date_complete", operator = "gte", value = 1 }
]
```

**How it works:**
1. When a flag is set, the engine records the current day in `$flags_meta`
2. `days_since_flag` condition calculates: `current_day - set_day`
3. Compares against required value with operator (gte, gt, lte, lt, eq)

**Files Modified:**
- `apps/game_generation/twee_comprehensive/generators/v1.py` - Flag tracking + condition evaluation
- `toml_generation_prompt.txt` - Documentation + examples

---

## Pillar 1: Story-Driven Obstacles

### Concept

NPCs aren't just stat sheets waiting to be ground. They have:
- Their own problems unrelated to the player
- Moods that change based on events
- Conflicts that require effort to resolve
- Secrets and history that unfold over time

### Examples

| Obstacle Type | Example |
|---------------|---------|
| **External stress** | Angela is overwhelmed at work → affects her mood for days |
| **Misunderstanding** | She thinks you lied → cold until you resolve it |
| **Past resurfaces** | Her ex contacts her → she's distant, conflicted |
| **Player mistake** | You forgot something important → trust damaged |
| **NPC growth** | She's changing, questioning her life → you support or lose her |

### Engine Requirements

| Feature | Description | Status |
|---------|-------------|--------|
| **NPC Mood System** | Temporary emotional states that affect all interactions | ⬜ Not Started |
| **Conflict Tracking** | "in_conflict" state with specific resolution path | ⬜ Not Started |
| **NPC Life Events** | Things that happen TO the NPC independent of player | ⬜ Not Started |
| **Event Memory** | NPC remembers specific moments, references them | ⬜ Not Started |
| **Mood Decay** | Temporary states resolve over time or through action | ⬜ Not Started |

### Proposed TOML Schema

```toml
[[npcs]]
id = "npc_angela"
name = "Angela"

# ══════════════════════════════════════════════════════════════
# MOOD SYSTEM - Temporary emotional states
# ══════════════════════════════════════════════════════════════
# Moods are temporary overlays on the NPC's base personality.
# They affect dialogue tone, available activities, and responses.
# Moods can be triggered by events, player actions, or time.

[npcs.mood_config]
# Default mood when nothing special is happening
default_mood = "neutral"

# How moods affect interactions
mood_effects = {
  "happy" = { affection_gain_multiplier = 1.5, unlocks = ["spontaneous_hug"] },
  "stressed" = { affection_gain_multiplier = 0.5, locks = ["intimate_activities"] },
  "upset_with_player" = { affection_gain_multiplier = 0, locks = ["all_positive"], unlocks = ["apology_conversation"] },
  "vulnerable" = { unlocks = ["deep_conversation", "comfort_her"] }
}

# ══════════════════════════════════════════════════════════════
# LIFE EVENTS - Things that happen in her world
# ══════════════════════════════════════════════════════════════
# NPCs have lives beyond the player. Events create obstacles,
# opportunities for connection, and story momentum.

[[npcs.life_events]]
id = "work_crisis"
name = "Work Crisis"
description = "Angela's project at work is falling apart"

# When this event triggers
trigger_conditions = { day_gte = 5, flag_not_set = "work_crisis_resolved" }

# What happens when it triggers
on_trigger = [
  { set_mood = "stressed", duration_days = 3 },
  { unlock_canvas = "angela_vents_about_work" },
  { add_journal_entry = "Angela seems stressed about something at work..." }
]

# How it can resolve
resolution_canvas = "help_angela_with_work"
on_resolution = [
  { set_mood = "grateful", duration_days = 2 },
  { trait_effect = { trait = "trust", op = "add", value = 20 } },
  { set_flag = "work_crisis_resolved" },
  { set_flag = "helped_her_career" }  # Referenced later
]

# What happens if player ignores it
expiry_days = 5
on_expiry = [
  { set_mood = "disappointed", duration_days = 2 },
  { trait_effect = { trait = "trust", op = "add", value = -10 } },
  { set_flag = "ignored_her_work_crisis" }  # Referenced later
]


[[npcs.life_events]]
id = "ex_contacts_her"
name = "Ex Boyfriend Reaches Out"
description = "Angela's ex sent her a message"

trigger_conditions = { affection_gte = 40, day_gte = 10 }

on_trigger = [
  { set_mood = "conflicted", duration_days = 4 },
  { unlock_canvas = "angela_mentions_ex" },
  { add_journal_entry = "Angela got a message that seemed to shake her..." }
]

# Multiple resolution paths
resolution_options = [
  {
    id = "supportive",
    canvas = "support_her_about_ex",
    on_resolution = [
      { trait_effect = { trait = "trust", op = "add", value = 25 } },
      { set_flag = "supported_her_ex_situation" }
    ]
  },
  {
    id = "jealous",
    canvas = "jealous_about_ex",
    on_resolution = [
      { trait_effect = { trait = "trust", op = "add", value = -15 } },
      { trait_effect = { trait = "affection", op = "add", value = -10 } },
      { set_flag = "was_jealous_about_ex" }
    ]
  }
]

# ══════════════════════════════════════════════════════════════
# CONFLICT SYSTEM - When things go wrong between you
# ══════════════════════════════════════════════════════════════
# Conflicts are special states where the relationship is damaged
# and normal interactions are blocked until resolution.

[[npcs.conflict_triggers]]
id = "caught_in_lie"
name = "She Caught You Lying"
description = "Angela discovered you lied to her"

# What triggers this conflict
trigger_flag = "angela_discovered_lie"

# Conflict state
on_trigger = [
  { set_conflict = true, conflict_id = "caught_in_lie" },
  { set_mood = "hurt_and_angry", duration_days = -1 },  # -1 = until resolved
  { lock_activities = ["romantic", "intimate", "casual_date"] },
  { unlock_canvas = "angela_confronts_lie" }
]

# Resolution requirements
resolution_requires = [
  { canvas_completed = "apologize_for_lying" },
  { trait_gte = { trait = "trust", value = 30 } }  # Must rebuild some trust
]

on_resolution = [
  { set_conflict = false },
  { set_mood = "cautious", duration_days = 3 },
  { set_flag = "reconciled_after_lie" },
  { add_memory = "the_lie_incident" }  # She'll reference this later
]

# ══════════════════════════════════════════════════════════════
# MEMORY SYSTEM - She remembers specific moments
# ══════════════════════════════════════════════════════════════
# NPCs can reference past events in dialogue, creating continuity
# and making the relationship feel real.

[[npcs.memories]]
id = "helped_her_career"
display_text = "You helped me when my project was falling apart"
sentiment = "positive"
weight = 3  # How often she might reference it

[[npcs.memories]]
id = "the_lie_incident"
display_text = "That time you lied to me"
sentiment = "negative"
weight = 2
fades_after_days = 30  # Eventually stops referencing it
```

### Runtime Implementation

```javascript
// ══════════════════════════════════════════════════════════════
// NPC Mood System
// ══════════════════════════════════════════════════════════════

// Get NPC's current mood (considers temporary moods and defaults)
setup.getNpcMood = function(npcId) {
  var npc = State.variables.npcs[npcId];
  if (!npc) return "neutral";

  // Check for active temporary mood
  if (npc.current_mood && npc.mood_expires_day) {
    var currentDay = State.variables.game_state.time_state.day;
    if (currentDay <= npc.mood_expires_day) {
      return npc.current_mood;
    }
  }

  // Return default mood
  return npc.mood_config?.default_mood || "neutral";
};

// Set NPC mood with duration
setup.setNpcMood = function(npcId, mood, durationDays) {
  var npc = State.variables.npcs[npcId];
  if (!npc) return;

  var currentDay = State.variables.game_state.time_state.day;

  npc.current_mood = mood;
  npc.mood_expires_day = durationDays === -1 ? 9999 : currentDay + durationDays;

  // Notify player
  if (setup.moodNotifications[mood]) {
    UI.alert(setup.moodNotifications[mood]);
  }
};

// Check if activity is available given current mood
setup.isActivityAvailableForMood = function(npcId, activityType) {
  var mood = setup.getNpcMood(npcId);
  var npc = State.variables.npcs[npcId];
  var moodEffects = npc.mood_config?.mood_effects?.[mood];

  if (!moodEffects) return true;

  if (moodEffects.locks?.includes(activityType)) return false;
  if (moodEffects.locks?.includes("all_positive") && isPositiveActivity(activityType)) return false;

  return true;
};

// ══════════════════════════════════════════════════════════════
// Life Events System
// ══════════════════════════════════════════════════════════════

// Check and trigger pending life events (called on day change)
setup.processLifeEvents = function() {
  var sv = State.variables;
  var currentDay = sv.game_state.time_state.day;

  Object.keys(sv.npcs).forEach(function(npcId) {
    var npc = sv.npcs[npcId];
    if (!npc.life_events) return;

    npc.life_events.forEach(function(event) {
      // Skip already triggered or resolved events
      if (sv.flags["event_" + event.id + "_triggered"]) return;
      if (sv.flags["event_" + event.id + "_resolved"]) return;

      // Check trigger conditions
      if (setup.checkEventConditions(event.trigger_conditions, npcId)) {
        setup.triggerLifeEvent(npcId, event);
      }
    });
  });
};

// Trigger a life event
setup.triggerLifeEvent = function(npcId, event) {
  var sv = State.variables;

  // Mark as triggered
  sv.flags["event_" + event.id + "_triggered"] = true;
  sv.flags["event_" + event.id + "_trigger_day"] = sv.game_state.time_state.day;

  // Apply on_trigger effects
  event.on_trigger.forEach(function(effect) {
    setup.applyEventEffect(npcId, effect);
  });

  console.log("[LifeEvent] Triggered: " + event.name + " for " + npcId);
};

// ══════════════════════════════════════════════════════════════
// Conflict System
// ══════════════════════════════════════════════════════════════

// Check if player is in conflict with NPC
setup.isInConflict = function(npcId) {
  var npc = State.variables.npcs[npcId];
  return npc?.in_conflict === true;
};

// Get active conflict details
setup.getActiveConflict = function(npcId) {
  var npc = State.variables.npcs[npcId];
  if (!npc?.in_conflict) return null;
  return npc.active_conflict;
};

// ══════════════════════════════════════════════════════════════
// Memory System
// ══════════════════════════════════════════════════════════════

// Add a memory to NPC
setup.addMemory = function(npcId, memoryId) {
  var npc = State.variables.npcs[npcId];
  if (!npc) return;

  if (!npc.active_memories) npc.active_memories = [];

  npc.active_memories.push({
    id: memoryId,
    added_day: State.variables.game_state.time_state.day
  });
};

// Get a random memory for dialogue (weighted by recency and weight)
setup.getRandomMemory = function(npcId, sentiment) {
  var npc = State.variables.npcs[npcId];
  if (!npc?.active_memories?.length) return null;

  var validMemories = npc.active_memories.filter(function(m) {
    var memoryDef = setup.getMemoryDefinition(npcId, m.id);
    if (sentiment && memoryDef.sentiment !== sentiment) return false;

    // Check if faded
    if (memoryDef.fades_after_days) {
      var daysSince = State.variables.game_state.time_state.day - m.added_day;
      if (daysSince > memoryDef.fades_after_days) return false;
    }

    return true;
  });

  if (!validMemories.length) return null;

  // Weighted random selection
  return setup.weightedRandom(validMemories);
};
```

### Content Examples

```toml
# ══════════════════════════════════════════════════════════════
# Canvas that only appears when Angela is stressed
# ══════════════════════════════════════════════════════════════
[[canvases]]
id = "angela_vents_about_work"
name = "Angela Needs to Talk"

[canvases.trigger]
npc = "npc_angela"
location = "living_room"

[canvases.trigger.conditions]
items = [
  { type = "npc_mood", npc_id = "npc_angela", mood = "stressed" }
]

[[canvases.nodes]]
id = "start"
content = '''
Angela is sitting on the couch, staring at her laptop with a troubled expression.

She looks up as you enter. "Hey... do you have a minute? I just..." She sighs heavily. "Work is a disaster right now."
'''

[[canvases.nodes.choices]]
text = "Sit down next to her and listen"
next_node = "listen_to_her"
effects = [
  { targetType = "npc", npcId = "npc_angela", trait = "trust", op = "add", value = 10 }
]

[[canvases.nodes.choices]]
text = "Sorry, I'm kind of busy right now"
next_node = "brush_her_off"
effects = [
  { targetType = "npc", npcId = "npc_angela", trait = "trust", op = "add", value = -15 },
  { setFlag = "brushed_off_work_vent" }
]


# ══════════════════════════════════════════════════════════════
# Later canvas that references the memory
# ══════════════════════════════════════════════════════════════
[[canvases]]
id = "angela_promotion"
name = "Angela's Big News"

[[canvases.nodes]]
id = "start"
content = '''
Angela bursts through the door, beaming.

"I got the promotion!"

<<if $flags.helped_her_career>>
She rushes over and hugs you tightly. "I couldn't have done it without you. Remember when everything was falling apart? You were there for me."
<<elseif $flags.ignored_her_work_crisis>>
She pauses, her smile flickering. "I... I did it myself, I guess. Would have been nice to have support back then, but..." She shrugs.
<<else>>
"All that stress finally paid off!"
<</if>>
'''
```

---

## Pillar 2: Player Skill Challenges

### Concept

Not all progress comes from grinding. Some moments test the player:
- Did you pay attention to what she told you?
- Can you read the situation and respond correctly?
- Will you act in time, or let the moment pass?

### Examples

| Challenge Type | Example |
|----------------|---------|
| **Memory test** | "What's my favorite flower?" (she mentioned it days ago) |
| **Reading the room** | She's upset but says "I'm fine" - do you push or let it go? |
| **Timed choice** | She's about to leave - say something NOW or miss your chance |
| **Observation** | Notice she's wearing something new / seems different |
| **Dialogue puzzle** | Navigate a difficult conversation without making it worse |

### Engine Requirements

| Feature | Description | Status |
|---------|-------------|--------|
| **Knowledge tracking** | Track facts player has learned about NPC | ⬜ Not Started |
| **Correct/incorrect choices** | Choices with right/wrong outcomes | ⬜ Not Started |
| **Timed choices** | Time pressure on decisions | ⬜ Not Started |
| **Observation checks** | Reward players who pay attention | ⬜ Not Started |

### Proposed TOML Schema

```toml
# ══════════════════════════════════════════════════════════════
# Knowledge / Memory Test
# ══════════════════════════════════════════════════════════════
[[canvases.nodes]]
id = "birthday_gift_choice"
content = "You're at the flower shop. What should you get Angela for her birthday?"

# This is a test - there's a right answer
challenge_type = "knowledge_test"
knowledge_required = "angela_favorite_flower"  # Set when she mentioned it

[[canvases.nodes.choices]]
text = "Lilies"
correct = true
next_node = "she_is_touched"
effects = [{ trait = "affection", op = "add", value = 20 }]
success_dialogue = "Her eyes light up. 'Lilies! You remembered...'"

[[canvases.nodes.choices]]
text = "Roses"
correct = false
next_node = "generic_gift"
effects = [{ trait = "affection", op = "add", value = 5 }]
failure_dialogue = "She smiles politely. 'Oh, roses. That's... nice.'"

[[canvases.nodes.choices]]
text = "Ask the shopkeeper for help"
next_node = "shopkeeper_helps"
neutral = true
# Not wrong, but not the personal touch


# ══════════════════════════════════════════════════════════════
# Timed Choice
# ══════════════════════════════════════════════════════════════
[[canvases.nodes]]
id = "moment_of_vulnerability"
content = '''
Angela stands at the door, hand on the handle. She's about to leave.

For a moment, she hesitates. Looks back at you. There's something in her eyes - something unsaid.

The moment hangs in the air.
'''

timed_choice = true
time_limit_seconds = 8
timeout_next = "she_leaves"
timeout_dialogue = "The moment passes. She opens the door and walks out."

[[canvases.nodes.choices]]
text = "Wait—"
next_node = "you_stop_her"

[[canvases.nodes.choices]]
text = "Angela, please don't go"
next_node = "heartfelt_stop"
effects = [{ trait = "affection", op = "add", value = 15 }]

# If player doesn't choose in time, timeout_next triggers


# ══════════════════════════════════════════════════════════════
# Reading the Room
# ══════════════════════════════════════════════════════════════
[[canvases.nodes]]
id = "she_says_fine"
content = '''
"How are you doing?" you ask.

Angela shrugs, not meeting your eyes. "I'm fine."

<<if hasPlayerKnowledge("angela_says_fine_means_not_fine")>>
//You've learned that when Angela says she's "fine," she's usually anything but.//
<</if>>
'''

[[canvases.nodes.choices]]
text = "Okay, good!"
next_node = "accept_fine"
correct = false  # Wrong read
effects = [{ trait = "trust", op = "add", value = -5 }]
internal_note = "Player missed the cue"

[[canvases.nodes.choices]]
text = "Angela... what's really going on?"
next_node = "push_gently"
correct = true  # Right read
requires_knowledge = "angela_says_fine_means_not_fine"  # Only shows if learned
effects = [{ trait = "trust", op = "add", value = 15 }]

[[canvases.nodes.choices]]
text = "You don't seem fine..."
next_node = "push_gently"
correct = true  # Also right
# Available to all - observant players
```

---

## Pillar 3: Emotional Weight in Choices

### Concept

Choices matter. Not every decision is reversible. Some shape the entire relationship.

### Examples

| Weight Type | Example |
|-------------|---------|
| **Sacrifice** | Help her career vs attend your important event |
| **Honesty** | Tell painful truth vs comfortable lie |
| **Commitment** | Exclusive to her vs keep options open |
| **Loyalty** | Keep her secret vs do "the right thing" |
| **Priority** | She needs you NOW vs your other obligations |

### Engine Requirements

| Feature | Description | Status |
|---------|-------------|--------|
| **Choice weight markers** | Flag significant decisions | ⬜ Not Started |
| **Delayed consequences** | Choices affect scenes much later | ⬜ Not Started |
| **Mutually exclusive paths** | Some choices lock out others | ⬜ Not Started |
| **Consequence preview** | Optional hint of weight | ⬜ Not Started |
| **Pattern awareness** | NPC notices player tendencies | ⬜ Not Started |

### Proposed TOML Schema

```toml
# ══════════════════════════════════════════════════════════════
# Major Choice with Delayed Consequences
# ══════════════════════════════════════════════════════════════
[[canvases.nodes]]
id = "critical_night"
content = '''
Your phone buzzes. It's Angela: "I really need you tonight. Please."

But your job interview is tomorrow morning. You need sleep. This could change your life.

She needs you. But so does your future.
'''

choice_weight = "major"  # Flags as significant
choice_category = "sacrifice"

[[canvases.nodes.choices]]
text = "I'm coming over"
next_node = "go_to_her"
effects = [
  { trait = "trust", op = "add", value = 25 },
  { setFlag = "chose_her_over_career" },
  { setFlag = "missed_interview_sleep" }
]
consequence_preview = "Angela will remember you chose her"  # Optional hint
delayed_consequences = [
  {
    triggers_in_canvas = "interview_result",
    effect = "interview_disadvantage"
  },
  {
    triggers_in_canvas = "angela_future_talk",
    effect = "she_references_sacrifice"
  }
]

[[canvases.nodes.choices]]
text = "I'm so sorry, I can't tonight"
next_node = "stay_home"
effects = [
  { trait = "trust", op = "add", value = -20 },
  { trait = "affection", op = "add", value = -15 },
  { setFlag = "chose_career_over_her" }
]
consequence_preview = "Angela will remember you weren't there"
delayed_consequences = [
  {
    triggers_in_canvas = "angela_future_crisis",
    effect = "she_doesnt_call_you"
  }
]


# ══════════════════════════════════════════════════════════════
# Mutually Exclusive Path
# ══════════════════════════════════════════════════════════════
[[canvases.nodes]]
id = "confession_moment"
content = "Angela looks at you intently. 'What are we? I need to know.'"

[[canvases.nodes.choices]]
text = "I want to be with you. Only you."
next_node = "commitment"
effects = [
  { setFlag = "committed_to_angela" },
  { trait = "trust", op = "add", value = 30 }
]
locks_paths = ["other_romances"]  # Can't pursue others
unlocks_paths = ["angela_exclusive_content"]

[[canvases.nodes.choices]]
text = "I care about you, but I'm not ready for that"
next_node = "not_ready"
effects = [
  { trait = "trust", op = "add", value = -10 },
  { setFlag = "rejected_commitment" }
]
# Keeps options open but damages this relationship


# ══════════════════════════════════════════════════════════════
# Delayed Consequence Reference (later in game)
# ══════════════════════════════════════════════════════════════
[[canvases]]
id = "angela_future_talk"
name = "Looking Back"

[[canvases.nodes]]
id = "reflection"
content = '''
Angela is quiet for a moment, then says:

<<if $flags.chose_her_over_career>>
"You know what I think about sometimes? That night I was falling apart, and you came over even though you had that big interview. You chose me."

She takes your hand. "Nobody ever chose me before."
<<elseif $flags.chose_career_over_her>>
"Remember that night I really needed you? And you couldn't come?"

She's not angry. Just... sad. "I understood. I did. But sometimes I wonder what we are to each other."
<<else>>
"We've been through a lot, haven't we?"
<</if>>
'''
```

---

## Implementation Priority

### Phase 1: Story-Driven Obstacles (Current Focus)
1. NPC Mood System
2. Life Events System
3. Basic Conflict Tracking
4. Memory System (simple version)

### Phase 2: Emotional Weight
1. Choice weight markers
2. Delayed consequence tracking
3. Mutually exclusive paths

### Phase 3: Player Skill Challenges
1. Knowledge tracking
2. Correct/incorrect choice outcomes
3. Timed choices

---

## Design Principles

1. **Content over mechanics** - Systems exist to enable better stories, not replace them
2. **Consequences feel real** - Player choices echo forward in meaningful ways
3. **NPCs feel alive** - They have lives, problems, moods independent of player
4. **Choices have weight** - Not everything is reversible or optimizable
5. **Attention is rewarded** - Players who pay attention get richer experiences
6. **Hardship creates investment** - Obstacles overcome are more satisfying than grinding

---

## Related Documents

- `GAME_ENGINE_ENHANCEMENTS.md` - Technical feature tracking
- `apps/game_generation/game_example.toml` - Reference TOML schema

---

## Notes

- All features should be backwards-compatible with existing TOML
- New fields should have sensible defaults (games work without these features)
- Dev mode should allow bypassing/testing these systems
- Each feature needs clear TOML documentation for content creators
