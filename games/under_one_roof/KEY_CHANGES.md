# Under One Roof — Key Design Changes

8 changes to apply to the game, in order. Derived from analysis of Back to Freedom, Course of Temptation, and Become Someone. All design philosophy — zero engine changes needed.

Reference: `prompts/game_design_observations.md` for full analysis.

---

## Change 1: Linear Deepening Scenes (replaces three-choice format)

**Priority: FIRST — biggest structural change**

### What It Was

Activities present three choices at base node: emotional, physical, neutral. Player picks one path. Other paths are invisible.

### What It Becomes

Activities are scenes that chain forward. The scene gets longer and deeper as the player's stats qualify. Not "pick a path" — the scene naturally extends.

### Example: Drawing Session with Jake

```
Base scene (always plays):
  "Jake is at his desk, charcoal in hand. He doesn't look up when you sit down."

→ Continue

Scene continues (always):
  "You watch him draw. His hand moves with a certainty his voice never has."

→ if jake_love ≥ 15: "Look over his shoulder" → deeper scene continues
→ else: "Leave him to it" → exit (jake_love +1)

Deeper scene (jake_love ≥ 15):
  "You lean closer. The drawing is a girl. Slim, dark hair in a bun."
  "He slams the sketchbook shut."

→ if jake_love ≥ 25: "It's me, isn't it?" → even deeper scene
→ "Pretend you didn't see" → exit (jake_love +2, jake_trust +1)

Even deeper (jake_love ≥ 25):
  "His ears go red. He doesn't deny it."
  "Neither of you says anything for a long time."
  "His hand is on the desk, three inches from yours."

→ if exposure_unlock: "Move your hand closer" → physical extension
→ "Thank him" → exit (jake_love +4)
```

Low stats = short scene (2 nodes). High stats = long scene (4-5 nodes). Same entry point, different depth.

### TOML Pattern

Nodes chain via `targetType = "node"` choices where deeper choices have stat conditions. Shallow exits use `targetType = "trigger"`. The scene branches vertically (deeper) not horizontally (different paths).

---

## Change 2: Additive Content Within Scenes

### What It Was

Group blocks show ONE variant (first match wins). Player sees DIFFERENT content based on stats.

### What It Becomes

Base content always plays. Independent conditional blocks ADD more content on top for higher stats. Player with higher investment sees MORE, not DIFFERENT.

### Example: Cooking Dinner with Frank

```toml
# Base (always shows)
{ type = "paragraph", content = "Frank is at the stove. She helps chop vegetables.
  The kitchen smells like garlic and something she can't name." }

# Love extension (shows independently if frank_love ≥ 20)
{ type = "group", conditions = { items = [
  { type = "trait", subject = "npc", npc_id = "npc_frank", trait_key = "love",
    operator = "gte", value = 20 }
] }, blocks = [
  { type = "dialog", content = "Diana used to make this. Before everything changed.",
    props = { speaker = "npc", npcId = "npc_frank" } },
  { type = "paragraph", content = "His voice catches. He doesn't look at her." }
] }

# Separator (breaks group chain so both can match independently)
{ type = "paragraph", content = "" }

# Corruption extension (shows independently if corruption ≥ 80)
{ type = "group", conditions = { items = [
  { type = "trait", subject = "player", trait_key = "corruption",
    operator = "gte", value = 80 }
] }, blocks = [
  { type = "paragraph", content = "Their hands brush reaching for the salt.
    Neither moves away. The contact lasts two seconds too long." }
] }
```

Player with high love AND high corruption sees ALL of it — the vulnerability AND the tension. Not one or the other.

### Key: Break Group Chains

Consecutive group blocks form a variant chain (first match wins). To make them additive, put a non-group block between them (even an empty paragraph). This breaks the chain so each group evaluates independently.

---

## Change 3: Choices Create Different Tone Flags

### What It Was

Both branches of a story choice set the SAME completion flag. Story progresses identically regardless.

### What It Becomes

Branches set DIFFERENT choice flags alongside the shared completion flag. Future scenes check which flag was set and show different content/tone.

### Example: Jake's Sketchbook Discovery

```
Player finds Jake's secret drawings of her:

Choice A: "These are beautiful, Jake."
  → sets: sketchbook_discovered (completion)
  → sets: chose_tender_jake (tone flag)
  → jake_love +5, jake_trust +3

Choice B: "You've been watching me?"
  → sets: sketchbook_discovered (completion)
  → sets: chose_confronted_jake (tone flag)
  → jake_trust -2, jake_corruption +5
```

Both progress the story (sketchbook_discovered). But future drawing sessions check the tone flag:

```
Tender path: "He draws openly now. Shows you each one."
Confronted path: "He still draws her, but hides them better. She pretends not to notice."
```

Both lead to full Jake content. The JOURNEY differs.

---

## Change 4: Cross-NPC Interlinking

### What It Was

Each NPC's story arc is independent. What happens with Jake has no effect on Frank or Ryan.

### What It Becomes

NPCs react to what's happening with other NPCs. The household is connected.

### Example: Frank Finds Jake's Drawings (Story Beat 18)

```
Frank discovers Jake's sketchbook:

If chose_tender_jake (she encouraged it):
  Frank's scene: disappointment in HER. "I expected better from you."
  → frank_trust -5
  → BUT: Ryan defends her. ryan_love +3

If chose_confronted_jake (she didn't know):
  Frank's scene: protective of HER. "I'll talk to him."
  → frank_love +3, frank_trust +2
  → BUT: Jake feels betrayed. jake_trust -5
```

One choice with Jake on Week 2 creates different Frank AND Ryan dynamics on Week 4. The household ripples.

### More Interlinking Examples

- Ryan notices Lily leaving Jake's room → ryan jealousy triggers → Ryan scene has confrontational tone
- Frank sees Lily being kind to Jake → frank softens → Frank opens up in next bookkeeping session
- Jake hears Lily laughing with Ryan through the wall → jake_trust -2 next day
- Spending evening with Frank means missing Jake's wall-knock → jake_love doesn't grow that day (trait decay handles this naturally)

---

## Change 5: Stats From Right Choices, Not Automatic

### What It Was

Every activity visit automatically gives love +2 or trust +3. Player builds stats by showing up.

### What It Becomes

Base visit gives minimal stats (+1). The RIGHT choice within the scene gives meaningful stats (+3 to +5). Player has to pay attention, not just click through.

### Example: Bookkeeping with Frank

```
Base visit: trust +1 (just showing up)

During the scene:
  Frank mentions Diana's spending habits.

  "Ask about Diana" → frank_love +3 (he appreciates the interest)
  "Focus on the numbers" → frank_trust +2 (professional, safe)
  "Make a joke about it" → frank_corruption +2 (breaks tension inappropriately)

  These choices appear WITHIN the linear deepening scene,
  not as the entry point.
```

The stat gain depends on WHAT the player does inside the scene, not WHETHER they visited.

### Stat Budget Per NPC

Design stat thresholds so the player can't max out without making the right choices:

```
Jake:  ~30 opportunities over 60 days × +1 base = 30 minimum
       Right choices add +2-4 extra per visit
       Key scenes need love ≥ 35-40 → player must make good choices in ~70% of visits

Frank: ~20 opportunities (less available, harder) × +1 base = 20 minimum
       Key scenes need love ≥ 30 → player must make good choices in ~80% of visits

Ryan:  ~25 opportunities × +1 base = 25 minimum
       Key scenes need trust ≥ 30 → player must make good choices in ~60% of visits
```

The math should be POSSIBLE but not EASY. Missing right choices means missing deeper content.

---

## Change 6: Money as Relationship Investment

### What It Was

Money is survival math. $400 start, $385/month burn. Escalation to higher-paying jobs.

### What It Becomes

Money is ALSO a relationship tool. Spending money on NPC-specific things builds relationship but costs survival resources.

### Examples

```
Jake:
  - Buy art supplies for him ($50) → jake_love +5
  - Pay for shared art class in town ($30) → jake_love +3, jake_trust +2

Ryan:
  - Gym membership ($30/month) → access to gym scenes with Ryan
  - Buy beer for truck trip ($15) → ryan_trust +2
  - Chip in for gas money without being asked ($10) → ryan_love +3

Frank:
  - Buy groceries and cook without being asked ($40) → frank_love +4
  - Pay part of the utility bill ($50) → frank_trust +5, frank_respect +3
```

Every dollar spent on an NPC is a dollar NOT spent on survival. The player who buys Jake art supplies has $50 less for bus fare. Real trade-offs.

---

## Change 7: Hidden Downstream Consequences

### What It Was

Choices are transparent — player knows what each choice does when they make it.

### What It Becomes

Some choices seem innocent at the time but create complications weeks later. The player doesn't know what matters until consequences emerge.

### Examples

```
Week 1: Lily helps Jake with his art project (seems innocent)
Week 4: Frank finds the finished drawing in Jake's room — it's clearly intimate
         → triggers Frank confrontation scene
         → Frank's reaction depends on whether Lily's name is signed on it
         → If she signed it (a choice during Week 1 that seemed like nothing):
           Frank knows she participated willingly

Week 2: Lily borrows Ryan's hoodie after getting caught in rain (seems practical)
Week 5: Jake sees her wearing Ryan's hoodie around the house
         → jake_trust -3, triggers jealousy scene
         → Jake: "Is there something going on with you and Ryan?"

Week 3: Lily agrees to model for Jake's art class assignment (seems supportive)
Week 6: The drawing is exhibited at campus art show. Ryan and Frank both see it.
         → Multiple NPC reactions in the same week
         → Content depends on how revealing the pose was (a choice from Week 3)
```

The MOMENT of choice feels small. The CONSEQUENCE arrives weeks later.

---

## Change 8: Cross-NPC Stat Requirements

### What It Was

Each NPC's scenes only require that NPC's stats. Focus on one NPC, ignore others.

### What It Becomes

Some scenes require investment in OTHER NPCs. Forces the player to spread attention.

### Examples

```
Frank's office scene (Week 6):
  Requires: frank_love ≥ 20 AND jake_love ≥ 15
  Why: Frank softens toward Lily because he sees how she treats Jake kindly

Ryan's truck confession (Week 8):
  Requires: ryan_trust ≥ 25 AND frank_trust ≥ 10
  Why: Ryan only opens up if he sees Lily has earned Frank's respect too

Jake's "I love you" scene (Week 9):
  Requires: jake_love ≥ 40 AND corruption ≥ 120 AND ryan_trust ≥ 15
  Why: Jake needs emotional security AND Lily needs to have navigated
       Ryan's dynamic without destroying the household
```

Player can't tunnel-vision one NPC. The household is interconnected.

---

## Implementation Order

Apply these changes to the TOML one at a time:

1. **Linear deepening scenes** — restructure activity canvases (biggest change)
2. **Additive content** — add stat-gated extensions that stack
3. **Different tone flags** — update story canvas choices to set different flags
4. **Cross-NPC interlinking** — add cross-NPC consequences to story beats
5. **Stats from right choices** — adjust effect values in activities
6. **Money as investment** — add spending choices to activities
7. **Hidden consequences** — connect early choices to later complications
8. **Cross-NPC requirements** — add cross-NPC conditions to key scenes

---

## What Stays The Same

- 60-day timeline
- Economic pressure system (impossible math)
- Shared skill unlock flags (kiss_unlock works everywhere)
- Three NPC archetypes (Jake/Ryan/Frank)
- Closed-house premise
- Corruption as universal gate
- 5 crisis beats and 6 endings
- NPC staggered difficulty (Jake 25, Ryan 50, Frank 100)
- All NPCs fully pursuable (player can have sex with all three)
- Energy budget system (4-5 activities/day)
- Trait decay (skip NPC → stats drop)

---

## What The Player Experiences

**Before these changes:** Visit location → click NPC portrait → pick emotional/physical/neutral → read scene → exit. Every NPC every day. No tension. Visual novel with menus.

**After these changes:** Enter scene → it unfolds naturally, getting deeper if you've invested enough → choices within the scene feel consequential → what you did with Jake this morning changes what Frank says tonight → spending money on art supplies means scrambling for rent → a choice you made two weeks ago just came back to bite you → you can't visit everyone today, who matters most right now?

The game feels like living in a house with three people who all want something from you, and every day the walls get thinner.
