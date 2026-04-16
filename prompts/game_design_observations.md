# Game Design Observations & Analysis

Reference document capturing design lessons from analyzing successful adult interactive fiction games and comparing them against our system. Use this when designing new games and updating prompts.

---

## 1. Executive Summary

We analyzed three successful games — Course of Temptation (CoT), Become Someone, and Back to Freedom — to understand what makes adult interactive fiction engaging vs feeling like a visual novel.

**The core finding:** Our engine is mechanically capable of everything these games do. The gap is in how we DESIGN games, not what the engine supports. Our prompts teach designers to build independent NPC arcs with repeatable three-choice activities and separate story events. Successful games instead build interlocking NPC webs with scenes that deepen through investment, force meaningful sacrifice, and create permanent consequences.

**The three things that matter most:**
1. Choices must cost something — picking one NPC means losing time with another
2. Investment must be visible — higher stats = MORE content, not just DIFFERENT content
3. NPCs must exist in each other's stories — what happens with Angela affects what's available with Gina

---

## 2. Game-by-Game Analysis

### 2a. Course of Temptation (CoT) by Anthaum

**What it is:** Text-based college life simulator on Twine/SugarCube. Endless sandbox. Procedurally generated NPCs (hundreds). Monthly updates. ~3,000 Patreon members.

**How it tells stories:** No authored story events. Everything is event pools that fire probabilistically during daily activities. You go to class and a classroom event might fire. You go to work and a work event might fire. Stories happen DURING activities, not as interruptions to them.

**Special NPC storylines** are sequential event chains embedded in event pools. The Best Friend storyline fires during dorm visits (6-11pm). Each visit, there's a chance the next story beat fires. The player can't control exactly when — they just keep visiting and the story advances probabilistically.

**Key mechanics:**
- 24 skills (max 10 each) that increase through usage, not menus
- 65+ inclinations (personality traits) discovered through repeated behavior
- 4 attitude axes per NPC: Friendship, Lust, Romance, Control (independent, can decay)
- 6 needs bars: Rest, Release, Composure, Relaxation, Hygiene, Hunger
- Multi-dimensional reputation with gossip propagation
- NPCs refuse dates based on reputation/inclination mismatches
- Encounter compositor: scenes assembled from components (furniture-aware, position system)
- Overdue event system: story-critical events increase probability if they haven't fired

**Strengths:** Emergent narrative, massive replayability, NPCs feel like people (memory, attitudes, rejection), world feels alive.

**Weaknesses:** Procedural text with no emotional depth per scene. "You kiss [NPC name]. She seems to enjoy it." No crafted prose, no media, no authored emotional moments.

**What we learn:** Story should happen during daily life, not as interruptions. NPCs should have memory, reject the player, and react to reputation. But procedural text isn't enough — authored scenes with media are our advantage.

---

### 2b. Become Someone by Volen

**What it is:** HTML5 life sim. Text-based with some images. Grind-focused sandbox.

**How it tells stories:** Grind repeatable activities → accumulate stats → unlock scripted milestone scenes at location + time + stat threshold. Daily activities are simple stat buttons ("Eat with Mom → trust +1"). The real content is in the milestone scenes.

**Key mechanics:**
- Trust as primary gate per NPC (5, 10, 15, 20, 25 thresholds)
- Dom/Sub binary: every milestone scene has two choices (top = submissive, bottom = dominant)
- Cross-character prerequisites (Mom Stage 2 requires Sister Stage 2)
- No three-choice format — activities are pure stat grinders
- Gallery system for replaying unlocked scenes

**Strengths:** Simple, clear progression. Player always knows what to work toward. Cross-character dependencies force engagement with multiple NPCs.

**Weaknesses:** Activities are boring stat buttons. Daily loop is a chore tolerated to reach milestone scenes. No variety in repeatable content.

**What we learn:** Our activity system is already far richer than Become Someone's stat buttons. Cross-character dependencies are valuable and easy to implement with our condition system. But pure stat grinding is not engaging — activities need to be interesting in themselves.

---

### 2c. Back to Freedom by Bald Games

**What it is:** HTML5 authored narrative. Images + video clips. Ongoing updates (currently v0.40+, Day 42+). One of the most successful games in the genre.

**How it tells stories:** Every day is a unique authored sequence. No repeatable activities. No grind. Every scene is written for that specific day with that specific NPC. 200+ unique scenes across 15+ NPCs over 42 days, with ongoing updates adding more days.

**Key mechanics:**

**Love + Lust dual axes per NPC.** Love gates scene access (emotional investment). Lust gates physical depth within scenes (how far scenes go). Both tracked independently. A single scene can have "extra options if love ≥ 22" AND "extra options if lust ≥ 14" — additive, not either/or.

**Stat escalation curves.** Angela's love: 12 → 13 → 15 → 20 → 25 → 28 → 42 over 42 days. Lust climbs slower: 12 → 13 → 14 → 22 → 26. Love grows fast through story choices. Lust grows slowly through physical moments. Different traits escalate at different rates.

**NPC-vs-NPC forced choices.** Day 3: Adriana bar date OR Angela TV night. Day 7: Angela theater OR Adriana nightclub. Day 9: Gina's room OR Megan's room. The player physically cannot see both. Creates sacrifice, FOMO, and replay value.

**Cross-NPC stat dependencies.** Angela Scene 11 requires Ava love ≥ 13. Gina Scene 8 requires "fucked Jillian at least once." Megan Scene 12 requires Angela love ≥ 25 AND Ava love ≥ 13. NPCs' stories are deeply woven together.

**Additive content within scenes (extended variants).** Scenes have a base version everyone sees PLUS "extra options" gated by higher stats. Higher investment = MORE content in the same scene, not just different content. Base + love extension + lust extension can all stack.

**Permanent route splits.** Day 27 corruption path vs love path with Adriana. Turning Lana into a pornstar vs preserving her innocence. These are permanent — content is locked for the rest of the playthrough. Creates distinct playthroughs and replay value.

**Consequence cascades across NPCs and weeks.** Impregnating Angela on Day 25 changes Gina's Day 26, Megan's Day 26, and creates new scenes. Winning Angela back on Day 35 unlocks 15+ scenes across Days 36-42. One choice on Day 20 (Gina's training) creates a consequence chain spanning 8 days.

**NPC wave introduction.** Day 1: Angela, Abigail. Day 2: Adriana. Days 5-6: Jessa, Gina, Megan, Jillian. Day 12: Lana. Day 20+: Blanche, Amirah, Brenna. Players aren't overwhelmed — NPCs appear naturally through story events.

**Items as gates.** Teddy bear for Gina, anal gel, blue pills, specific car equipped, weed. Not just stat numbers — specific items purchased at specific times create mini-puzzles.

**Stamina as daily resource.** "Avoid cumming too much throughout the day to have enough stamina for the night scene." Taking 5 blue pills = heart attack = game over. Physical content has a daily budget.

**Can't-miss vs must-earn split.** ~30% of scenes are automatic (story beats everyone experiences). ~70% require specific stats, choices, or items. Every player sees the core story. Invested players see significantly more.

**Strengths:** Massive authored content density. Every day feels unique. Choices have permanent weight. NPCs are deeply interlocked. Replay value through route splits. Media-rich (images + video).

**Weaknesses:** No repeatable content means every scene must be authored from scratch. No daily routine — game is pure authored sequence. Extremely high content production cost per update.

**What we learn:** This is the closest model to what we should build. Linear deepening scenes (not three-choice branching), love/lust split, cross-NPC dependencies, additive content, permanent route splits, consequence cascades. All achievable with our engine.

---

## 3. How Stories Are Told — Comparison

| Aspect | CoT | Become Someone | Back to Freedom | Our System |
|--------|-----|----------------|-----------------|------------|
| Story delivery | Event pools fire probabilistically | Stat grind → milestone scenes | Unique authored scenes per day | Story canvases + repeatable activities |
| Daily activities | Where stories happen (embedded) | Stat buttons (boring) | Don't exist (everything is story) | Three-choice format with group variants |
| Content per activity | Procedural text | None (just +1 stat) | Full authored scene with media | Authored prose + media + choices |
| What gates content | Skills + inclinations + RNG | Trust thresholds | Love + lust + choices + items | Flags + stat thresholds |
| Repeatable content | Event pools (procedural variety) | Stat buttons (identical) | None (all one-time) | Group variants + block pools |
| NPC independence | Fully independent | Cross-character prereqs | Deeply interlocked | Mostly independent |
| Choices matter | Inclination-shaped | Dom/Sub binary | Permanent route splits | Same flag both paths |
| Replayability | Seeds + inclinations + RNG timing | Dom vs Sub paths | Route splits + NPC choices | Minimal |

---

## 4. Key Design Principles (Universal Truths)

These principles apply regardless of game format, engine, or setting:

### Principle 1: Choices Must Cost Something

The player should regularly face moments where choosing one thing means losing another. Not every choice — but enough that decisions feel heavy. "Go with Adriana OR stay with Angela" is more engaging than "visit Angela, then visit Adriana, then visit Megan" with no conflict.

### Principle 2: Investment Must Be Visible

Higher stats should give the player MORE content, not just DIFFERENT content. A player who built love to 42 should see more scenes, more dialog, more intimate moments than a player at love 20. Additive content (base + extensions) rewards investment visibly. Either/or variants (show A or show B) feel like the player is missing half the content no matter what they do.

### Principle 3: NPCs Must Exist in Each Other's Stories

NPCs shouldn't be isolated quest lines. What happens with one should affect what's available with another. "Angela's scene requires Ava love ≥ 13" forces the player to invest across relationships. The world feels connected, not like parallel tracks.

### Principle 4: Some Doors Must Close Permanently

Not every choice should converge to the same outcome. Some choices should permanently lock content, creating a playthrough that feels uniquely the player's. "Corruption route" and "love route" with the same NPC should lead to genuinely different content for the rest of the game. This creates replay value.

### Principle 5: Relationships Need Two Dimensions

One number can't capture a relationship. Love and lust (or trust and desire, or comfort and attraction) create richer dynamics. The same NPC feels different at high-love/low-lust vs low-love/high-lust. Love gates emotional depth. Lust gates physical intensity. Both can stack additively within the same scene.

### Principle 6: Activities Should Be Story, Not Filler

Daily activities shouldn't be stat grind buttons. They should be authored narrative moments with outcomes, consequences, and variety. "Studying with Gina" should be a scene where winning or losing a quiz changes what happens next — not a button that gives intelligence +1.

### Principle 7: NPCs Should Arrive in Waves

Don't introduce all NPCs on Day 1. Introduce 2-3 initially, then add more through story events as the game progresses. Each NPC's introduction IS a story event. This prevents overwhelm and makes each new NPC feel significant.

### Principle 8: Consequences Should Cascade

A choice shouldn't just echo for 1-3 days within one NPC's activities. Major choices should cascade across multiple NPCs and span weeks. "Impregnating Angela changes Gina's, Megan's, AND Adriana's content over the next 10 days" creates a world that reacts to the player's decisions at scale.

### Principle 9: Gate Content Through Multiple Mechanisms

Don't gate everything with just stat thresholds. Use a mix of:
- Stat thresholds (love ≥ 25, lust ≥ 14)
- Prior choices (chose romantic route on Day 27)
- Cross-NPC requirements (Ava love ≥ 13 to unlock Angela scene)
- Items (teddy bear, specific car equipped)
- Timing (correct day/time)
- Puzzle answers (quiz challenges)

Variety in gating keeps the player thinking, not just grinding.

### Principle 10: Separate "Can't Miss" From "Must Earn"

~30% of scenes should be automatic — core story beats every player experiences. ~70% should require investment — stat thresholds, correct choices, specific items. This ensures every player sees the story, but invested players see significantly more. The reward for investment is MORE content, not gated-off content.

---

## 5. Our System's Strengths

What we do BETTER than the analyzed games:

1. **Media-rich scenes.** Video clips, images, GIFs embedded in scenes. CoT is pure text. Become Someone has minimal images. Back to Freedom has images + some video. We have the richest media integration.

2. **AI-assisted content generation.** Full pipeline from concept → book → TOML → game. No other game has this. We can produce content faster than any solo developer.

3. **Evolving repeatable content.** Our group blocks, block pools, consequence echoes, and modifiers make activities feel different on each visit. CoT has procedural variety but no emotional depth. Back to Freedom has no repeatable content at all.

4. **Structured validation.** Flag chain analysis, reachability checking, schedule gap detection. No other game has automated validation of content integrity.

5. **NPC portrait interaction model.** Clickable NPC portraits at locations with cost badges. Visual and intuitive.

6. **Story arc journal with guide page.** Per-NPC progress tracking, hints, trait requirement displays. Better player guidance than any analyzed game.

---

## 6. Our System's Weaknesses

What the analyzed games do that we DON'T:

1. **No meaningful sacrifice in choices.** Our games let players visit every NPC every day with no conflict. No forced NPC-vs-NPC choices.

2. **Either/or content, not additive.** Group blocks show ONE variant (first match wins). Back to Freedom shows base + love extension + lust extension stacking. Higher investment doesn't give MORE content in our system.

3. **Independent NPC arcs.** Each NPC's story progresses independently. No cross-NPC stat requirements. No interlocking dependencies.

4. **No permanent route splits.** Both branches of every choice set the same completion flag. No content is permanently locked. No replay incentive.

5. **Single relationship axis.** One trait per NPC (love or trust). No love + lust split creating four-quadrant relationship dynamics.

6. **Three-choice format feels like a menu.** "Pick emotional, physical, or neutral" is a UI menu, not a story moment. Back to Freedom's linear deepening scenes feel like real interactions.

7. **All NPCs available from Day 1.** No wave introduction. Player is overwhelmed and no NPC's arrival feels significant.

8. **Short games with insufficient content.** Our games are 14-30 days. Back to Freedom is 42+ days with 200+ scenes. The player feedback "not enough content to keep users engaged" directly reflects this.

9. **Consequences don't cascade.** Our consequence echoes last 1-3 days for one NPC. Back to Freedom's consequences span weeks across multiple NPCs.

10. **Stat thresholds are the only gate.** We don't use items, puzzles, cross-NPC requirements, or timing as content gates. Everything is just "get love to 25."

---

## 7. What Our Engine Already Supports (No Code Changes Needed)

Every principle above works with our current engine:

| Principle | Engine Feature | Status |
|-----------|---------------|--------|
| NPC-vs-NPC choices | Story canvas with two choices leading to different nodes | Already works |
| Cross-NPC dependencies | `conditions.items` can check any NPC's traits | Already works |
| Love + Lust split | `core_traits = { love = 0, lust = 0 }` | Already works |
| Permanent route splits | Different flags per choice path | Already works |
| Linear deepening scenes | Node chains with conditional exits | Already works |
| Additive content | Multiple group blocks that check different thresholds independently (not as variant chain — as separate groups with gaps between them) | Needs testing |
| NPC wave introduction | Story canvas that introduces new NPC mid-game | Already works |
| Consequence cascades | Flags + group blocks across multiple NPCs + activities | Already works |
| Items as gates | Player flags (`has_teddy_bear`) with conditions | Works as flags |
| Block pools for variety | `block_pool` block type | Already built |
| Rejection on locked choices | `show_when_locked`, `rejection_node` | Already built |
| Trait decay | `trait_decay` on NPCs | Already built |
| Temporary modifiers | `modifier_effects`, `modifier_redirect` | Already built |

**Key insight for additive content:** Our group blocks currently work as variant chains (first match wins). For additive content, we need SEPARATE group blocks with non-group content between them — breaking the chain so multiple groups can match independently:

```toml
# Base content (always shows)
{ type = "paragraph", content = "Morning. She's making coffee." }

# Love extension (shows if love ≥ 20, independent of lust group below)
{ type = "group", conditions = { items = [
  { type = "trait", trait_key = "love", operator = "gte", value = 20 }
] }, blocks = [
  { type = "paragraph", content = "She touches your hand when she passes the mug." }
] }

# Non-group separator — breaks the chain
{ type = "paragraph", content = "" }

# Lust extension (shows if lust ≥ 15, independent of love group above)
{ type = "group", conditions = { items = [
  { type = "trait", trait_key = "lust", operator = "gte", value = 15 }
] }, blocks = [
  { type = "paragraph", content = "Your eyes follow her as she bends to get the sugar." }
] }
```

This is a workaround. A cleaner solution might be a new block type or a flag on group blocks to indicate "additive" vs "variant chain" behavior. But the workaround works today.

---

## 8. What Needs Prompt Changes

These are design philosophy changes, not engine changes. The prompts need to:

1. **Replace three-choice format with linear deepening.** Teach scenes that chain forward, getting longer/richer with higher stats. Not "pick emotional/physical/neutral" but "scene deepens as your investment qualifies."

2. **Teach love + lust as standard NPC traits.** Every NPC gets two relationship axes. Love gates emotional access. Lust gates physical depth. Both stack additively within scenes.

3. **Teach NPC-vs-NPC conflict moments.** Story canvases that force the player to choose between NPCs. "Adriana wants to go out. Angela is waiting at home."

4. **Teach cross-NPC dependencies.** "Angela Scene 11 requires Ava love ≥ 13." Design NPCs whose stories reference each other.

5. **Teach permanent route splits.** Different flags per choice path that permanently lock content. Not "both set the same flag."

6. **Teach NPC wave introduction.** Start with 2-3 NPCs. Introduce more through story events on specific days.

7. **Teach additive content within scenes.** Base + love extension + lust extension, not either/or variants.

8. **Teach multi-week consequence cascades.** Major choices should ripple across NPCs and span weeks, not just 1-3 days.

9. **Teach 30/70 can't-miss/must-earn ratio.** 30% automatic story beats. 70% require investment.

10. **Teach varied gating mechanisms.** Stats + choices + cross-NPC + items (as flags) + timing.

---

## 9. Activity/Scene Design Patterns

### Pattern: Linear Deepening Scene (replaces three-choice format)

Instead of three choices at a base node splitting into three paths:

```
Base node → "Continue" →
  Moment 1 (always) →
    if love ≥ 20: "Tell her what's on your mind" → Moment 2 (deeper dialog)
    else: "Grab your coffee and go" → exit
  Moment 2 →
    if lust ≥ 15: "Pull her close" → Moment 3 (physical extension)
    "Say something meaningful" → Moment 3 (emotional extension)
    "That's enough for now" → exit
  Moment 3 → exit with effects
```

The scene gets longer and richer as the player's stats qualify. Not branching — extending.

### Pattern: Additive Content Within Scene

Base content always plays. Independent group blocks add love-gated and lust-gated content on top:

```
[Always shows] Morning description
[If love ≥ 20] Extra emotional moment — she opens up
[If lust ≥ 15] Extra physical moment — lingering touch
[Always shows] Scene conclusion
```

A player with high love AND high lust sees ALL of it. Not one or the other.

### Pattern: NPC-vs-NPC Choice

A story canvas presenting a forced choice between two NPCs:

```
"Adriana texted — she wants to meet at the bar.
 Angela is setting up a movie in the living room."

Choice A: "Go meet Adriana" → Adriana scene (sets chose_adriana flag)
Choice B: "Stay with Angela" → Angela scene (sets chose_angela flag)
```

Each path leads to exclusive content. The other NPC's content for that day is permanently missed.

### Pattern: Extended Scene Variant

Base scene always plays. Higher stats unlock MORE within the same scene:

```
Scene plays (base) →
  if lust ≥ 14: additional physical options appear in exit block
  if love ≥ 22: additional emotional dialog appears in blocks
  if lust ≥ 14 AND love ≥ 22: both extensions stack
```

---

## 10. NPC Design Patterns

### Pattern: Dual-Axis Relationship (Love + Lust)

Every NPC has two independent relationship traits:

```toml
[[npcs]]
id = "npc_angela"
core_traits = { love = 0, lust = 0 }
```

- **Love** grows through emotional choices, conversations, being supportive, shared experiences
- **Lust** grows through physical moments, flirting, physical proximity, explicit scenes
- Love gates access to scenes (can you enter this moment?)
- Lust gates depth within scenes (how far does this moment go?)
- Both escalate at different rates (love climbs faster than lust)

### Pattern: Wave Introduction

```
Week 1:  Angela (wife/partner), Gina (daughter/housemate) — immediate family
Week 2:  Adriana (neighbor/friend) — introduced through story event
Week 2:  Megan (coworker) — introduced at work location
Week 3:  Lana (new arrival) — appears through a story event
Week 4+: Additional NPCs through story events as world expands
```

Each introduction is a story event, not just an NPC appearing at a location.

### Pattern: Interlocking NPC Dependencies

```
Angela Scene 11: requires Angela love ≥ 25 AND Ava love ≥ 13
Gina Scene 8: requires "fucked Jillian at least once"
Megan Scene 15: requires "won Angela back on Day 35"
```

Forces the player to invest across relationships, not tunnel-vision one NPC.

### Pattern: NPC-Specific Escalation Curves

Each NPC has a different stat curve reflecting their personality:

```
Angela (warm, open):     love 12→15→20→25→28→42  (fast love growth)
                         lust 12→13→14→14→22→26  (slow lust growth)

Adriana (guarded, passionate): love 6→7→8→16→28  (slow love growth)
                               lust 6→7→8→12→25  (moderate lust growth)

Gina (shy, romantic):   love 22→30→32→37→42     (high love threshold)
                        lust 12→18→20→24→30     (moderate lust growth)
```

Personality determines how quickly each axis grows and what thresholds gate content.

---

## 11. Stat/Progression Design Patterns

### Pattern: Corruption as Route Selector

Corruption doesn't just gate content — it changes which stories are available:

```
Corruption < 45:  Romantic route with Adriana (love, commitment, pregnancy)
Corruption ≥ 45:  Wild route with Adriana (lust, domination, no commitment)
```

The player can't see both in one playthrough. Major corruption milestones permanently alter the game's direction.

### Pattern: Slow Escalation

Stats don't jump from 0 to max. They build slowly through authored scenes:

```
Day 1-5:   love 0-12   (getting to know each other)
Day 5-15:  love 12-20  (growing closer)
Day 15-25: love 20-28  (deepening connection)
Day 25-42: love 28-42+ (committed relationship)
```

Each range corresponds to a relationship phase. Activities and scenes should reflect the current phase.

### Pattern: Stat Sources That Feel Natural

Stats should grow through natural interactions, not arbitrary buttons:

```
Love grows through:
  - Having meaningful conversations
  - Making the right choices in story moments
  - Being supportive during crises
  - Spending quality time together

Lust grows through:
  - Physical scenes (each physical scene adds lust)
  - Successful physical escalation
  - Specific bold/flirty choices

NOT through:
  - Clicking "eat breakfast → love +1" repeatedly
  - Generic grind activities
```

---

## 12. Content Gating Patterns

### Pattern: Multi-Mechanism Gating

A single scene can be gated by multiple mechanism types:

```
Angela Day 25 scene requires:
  - love ≥ 28 (stat threshold)
  - Declined Erica's racing event (prior choice)
  - Didn't choose "Oyster au Gratin" at dinner (specific choice)
  - Angela leads you to bed (automatic if above met)

Extended version additionally requires:
  - love ≥ 28 + Ava love ≥ 14 (cross-NPC stat)
  - blue pill in inventory (item gate)
```

### Pattern: Can't-Miss vs Must-Earn

```
CAN'T MISS (automatic, ~30% of scenes):
  - Story introductions ("This scene happens on Day 1. You can't miss it.")
  - Crisis events ("This happens after you save Gina. You can't miss it.")
  - Plot pivots everyone needs to experience

MUST EARN (gated, ~70% of scenes):
  - Extended scene variants (extra content for higher stats)
  - Physical escalation scenes (require lust thresholds)
  - Cross-NPC scenes (require investment in multiple NPCs)
  - Route-specific scenes (only on corruption or love path)
```

### Pattern: Permanent vs Temporary Gates

```
TEMPORARY GATES (can be achieved later):
  - Stat thresholds (keep building stats)
  - Item purchases (earn money, buy item)

PERMANENT GATES (this playthrough only):
  - Choice flags (chose Adriana over Angela — can't undo)
  - Route splits (corruption path vs love path)
  - NPC-vs-NPC exclusive scenes (missed = missed)
```

---

## 13. Player Experience Principles

### The "What Am I Missing?" Effect

The player should always feel like there's content they HAVEN'T seen. Not because the game hides content unfairly, but because their choices led them down one path, and another path exists. This creates replay desire.

### The "I Earned This" Effect

When a scene goes deeper because the player invested heavily, they should feel the payoff. "Extra options if love ≥ 22" means the player sees content that a less-invested player doesn't. Their investment was rewarded with MORE, not just different.

### The "I Can't Do Everything" Effect

Daily time pressure or NPC-vs-NPC conflicts should create a feeling of scarcity. Not resource scarcity (energy costs) but ATTENTION scarcity — you can't build all relationships equally. You must choose who matters most.

### The "The World Remembers" Effect

Major choices should ripple. If you made a bold choice last week, three NPCs should reference it in different ways over the next few days. The world reacts to you, not just the NPC you made the choice with.

### The "Real People" Effect

NPCs should reject you, confront you about neglect, react to your reputation, and have opinions about other NPCs. They shouldn't be content dispensers who always give you what you want when your stats are high enough.

### The "Natural Rhythm" Effect

The game should have a natural rhythm — not every day is a dramatic story event. Some days are quiet moments that build stats and deepen relationships through small interactions. The dramatic moments hit harder when they're surrounded by everyday life.

### The "Second Playthrough" Effect

The game should be designed so that finishing it creates immediate desire to play again with different choices. "What if I chose Adriana instead of Angela?" "What if I went corruption route?" This requires permanent route splits and NPC-vs-NPC exclusive content.

---

## Appendix: Comparison Table

| Feature | CoT | Become Someone | Back to Freedom | Our System (Current) | Our System (Possible) |
|---------|-----|----------------|-----------------|---------------------|----------------------|
| Engine | Twine/SugarCube | Twine/SugarCube | HTML5/JS | Twine/SugarCube | Same |
| Media | Text only | Minimal images | Images + video | Images + video | Same (strongest) |
| NPCs | 100s (procedural) | ~10 (authored) | 15+ (authored) | 2-5 (authored) | 10+ possible |
| Story length | Endless | Ongoing | 42+ days ongoing | 14-30 days | 42+ days possible |
| Daily activities | Event pools (embedded story) | Stat buttons | None (all one-time) | Three-choice format | Linear deepening |
| Relationship axes | 4 (friendship/lust/romance/control) | 1 (trust) | 2 (love + lust) | 1 (love or trust) | 2 (love + lust) |
| Cross-NPC deps | None | Some prerequisites | Deep interlocking | None | Full support ready |
| Route splits | Inclination-shaped | Dom/Sub binary | Permanent divergence | Same-flag convergence | Permanent divergence |
| Rejection | NPCs refuse based on attitudes | None | Stats gate content | Built (show_when_locked) | Ready |
| Trait decay | Attitudes decay without interaction | None | N/A (no repeating) | Built (trait_decay) | Ready |
| Modifiers | Intoxication/arousal | None | Blue pills/items | Built (modifier_effects) | Ready |
| Content variety | Procedural pools | None | All unique | Block pools + group variants | Ready |
| Consequence cascades | NPC memory | None | Multi-week, cross-NPC | 1-3 day echoes | Multi-week possible |
| Replay value | Seeds + inclinations | Dom vs Sub | Route splits + NPC choices | Minimal | Full support ready |
