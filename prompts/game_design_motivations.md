# Game Design Motivations — Why Games Feel Like Games

Reference document for designing games that feel like GAMES, not visual novels. These are the 6 core motivations that create player engagement. Each motivation describes a FEELING the player should have — not a specific mechanic to copy.

Use this alongside `activity_types.md` (structure) and `game_design_observations.md` (analysis). This doc covers the WHY. Those cover the HOW.

---

## The Problem

A visual novel feels like: click → read → click → read. Choices don't matter. NPCs are always available. Nothing is at stake. The player is a passenger.

A game feels like: every choice costs something, NPCs push back, the world remembers, and the player finishes knowing their playthrough was uniquely theirs.

The difference isn't engine features or writing quality. It's DESIGN — how choices are structured, what has consequences, and where pressure comes from.

---

## Motivation 1: "I Can't Have Everything"

### What It Is

The player faces moments where choosing one path naturally means another path doesn't happen. Not because a system blocks them — because the STORY creates a fork where both can't coexist.

### Why It Matters

When the player can do everything, nothing matters. When they must choose, every choice carries weight. The sacrifice creates emotional investment — "I chose Jake over Ryan tonight, and I felt that."

### How It Works

This comes from **story design**, not mechanical restrictions. NOT artificial time-slot limits. NOT "pick one NPC per evening." The narrative itself presents situations where two things happen at the same time, and the player naturally can't do both.

### Wrong Approach

```
System message: "It's 7pm. You can only do one evening activity."
→ Pick NPC from list → do activity → tomorrow, same menu
```

This is mechanical scarcity. It feels arbitrary and frustrating.

### Right Approach

```
Story moment: Ryan pulls up in the truck, engine running.
"Get in, we're going to town."

Through the wall, Jake knocks. Tap-tap. Their ritual.

→ "Hop in the truck" → Ryan's story advances, Jake's knock goes unanswered
→ "Knock back" → Jake's story advances, Ryan drives off alone
```

This is narrative scarcity. The SITUATION demands a choice. Both options feel real and consequential because the story made them matter.

### Ideas for Game Design

- **Story canvases with NPC-vs-NPC forks:** One story event, two NPCs pulling in different directions. The player picks a path. The other NPC's content for that beat is gone.
- **Multiple-path story arcs:** Jake's Week 3 arc has two branches. Ryan's Week 3 arc happens at the same narrative moment. The player experiences one fully and glimpses the other through consequences.
- **Exclusive first-time events:** Three variants of the "first awareness" event exist (Jake/Ryan/Frank). Only ONE fires based on who you invest in first. The other two are permanently locked.
- **First milestone exclusivity:** First kiss with Jake is a tender art room moment. First kiss with Ryan is aggressive in the truck. First kiss with Frank is forbidden at 2am. Only ONE is the story canon first kiss.

### Guidelines

- Scarcity should come from the narrative, not the system
- The player should feel "I wish I could do both" not "the game won't let me"
- Both options in a fork should be genuinely appealing — no obvious right answer
- The unchosen path should have visible consequences (the NPC reacts to being unchosen)
- Don't overdo it — most days should be open. Forks happen at key story moments

---

## Motivation 2: "This Matters"

### What It Is

Choices have lasting, irreversible impact. The world permanently changes based on what the player did. Not different dialogue — different STRUCTURE.

### Why It Matters

When both options lead to the same outcome, nothing matters. When a choice permanently closes a door, opens another, or changes who lives in the house — the player feels the weight of their decisions across the entire game.

### How It Works

Key story choices set different flags that permanently alter what content is available. Some choices change NPC availability, household composition, or relationship dynamics for the rest of the playthrough.

### Ideas for Game Design

**Arrangement choices that can't be undone:**
- Ryan offers $100 for "favors." Accept once → he expects it every time. The dynamic is set. Refuse → he respects you, but that income stream is gone forever. You can't accept later.
- Frank offers $150/week arrangement. Accept → financial security, but the relationship is transactional. Refuse → money stays tight, but he sees you as a person, not a transaction. Can't switch.

**Choices that reshape the household:**
- When brothers discover each other's relationship with Lily: independent / peacemaker / avoidant. Each PERMANENTLY changes dinner dynamics, shared location behavior, and whether brothers cooperate or compete.
- Frank finds Jake's drawings. How you respond determines whether Frank trusts you less (defended Jake), whether Jake trusts you less (denied knowledge), or whether the power dynamic shifts (challenged Frank). Each reshapes the Frank-Jake-Lily triangle for weeks.

**Small choices with delayed structural impact:**
- Sign your name on Jake's drawing (seems like nothing). Weeks later, Frank finds it. If signed → he knows you participated willingly. If unsigned → deniability. A tiny choice that determines a major confrontation's outcome.
- Tell mom the truth about money → she sends $200 but might come home early (game shortens). Lie → more time, no money, more guilt.

**Permanent route splits:**
- Love route vs corruption route with the same NPC. At a certain threshold, the relationship locks into one flavor. Romantic Jake is different content from corrupted Jake. Same NPC, different game.

### Guidelines

- Not every choice needs to be permanent — most can be light. But 3-5 KEY moments per game should be genuinely irreversible
- The player should feel the consequence DAYS later, not immediately — delayed impact is more powerful
- Both sides of a permanent choice should have meaningful content — don't make one option obviously better
- Flag each permanent choice clearly in the game design (the player may not know it's permanent, but the designer should)

---

## Motivation 3: "I Earned This"

### What It Is

Content feels deserved because the player worked for it — made the right decisions, invested resources, paid attention to NPC personalities. Not just "visited 30 times."

### Why It Matters

Automatic stat gains (+2 love per visit, guaranteed) make progression feel hollow. When the player reaches a milestone because they made specific right choices, spent money wisely, and invested in the right NPCs at the right time — the payoff feels real.

### How It Works

Milestone content requires MULTIPLE gates — not just one stat number, but a combination of stats, flags, and cross-NPC investments. The player who pays attention and makes strategic choices reaches content that the player who clicks through cannot.

### Ideas for Game Design

**Multi-gate milestones:**
- Jake's deepest scene requires: love ≥ 30 + bought art supplies at least once (flag) + chose "ask about art school" in activities (flag) + signed his drawing (flag). Four gates, not one. A series of right decisions across weeks.
- Frank's late night confession requires: trust ≥ 20 + kept his financial secret (flag) + helped in workshop at least 3 times + did NOT accept the arrangement (flag). Trust earned through actions AND restraint.

**Cross-NPC requirements:**
- Frank's office scene requires frank_trust ≥ 20 AND jake_love ≥ 15. WHY? Frank softens toward Lily when he sees her treating his son well. The player earns Frank THROUGH Jake.
- Ryan's vulnerable confession requires ryan_trust ≥ 25 AND frank_trust ≥ 10. WHY? Ryan only opens up if he sees Lily has earned his father's respect too. The household validates her.
- Jake's "I love you" requires jake_love ≥ 40 AND ryan_trust ≥ 15. WHY? Jake needs to feel secure that Lily has navigated Ryan's dynamic without destroying the household.

**Money as proof of care:**
- Ryan's deepest trust scene requires: gave him gas money without being asked ($10, flag) + went to job site at least 3 times (counter flag) + ryan_trust ≥ 20. You proved yourself through SPENDING and SHOWING UP, not just visiting.
- Jake's art exhibition scene requires: bought charcoal ($15, flag) + paid for art class ($30, flag). You invested in his DREAM, not just his body.

**Stats from right choices, not automatic:**
- Base visit gives +1 (just showing up). The right choice within the scene gives +3 to +5.
- Over 20 visits: attentive player has love 60+, click-through player has love 20. Same activity, wildly different outcomes.
- The math should make it POSSIBLE but not EASY to hit deep content thresholds. Missing right choices means missing deeper content.

### Story-Driven Requirements

The hardship of earning content shouldn't come from arbitrary stat gates. It should come from the STORY naturally requiring the player to build specific things. Each NPC's personality and arc demands different investments:

**The principle:** The NPC's story creates the need. The player grinds because the CHARACTER needs something, not because a number needs to go up.

**Example — how different NPCs require different investments:**

| NPC | What their story needs | Why it's natural | Player activities to build it |
|-----|----------------------|-----------------|------------------------------|
| Jake (shy artist) | Beauty, confidence, artistic sensibility | He wants to draw her — she needs to look/feel good for posing. He's attracted to creativity and vulnerability. | Yoga, self-care, buying clothes, art supplies |
| Ryan (cocky, physical) | Fitness, confidence, boldness | He respects strength and directness. Timid responses bore him. He opens up to equals, not dependents. | Gym, jogging, job site work, bold choices |
| Frank (authority, reserved) | Intelligence, reliability, maturity | He values competence. Bookkeeping requires real skill. He respects people who show up consistently and keep secrets. | Studying, showing up to workshop, being patient, keeping promises |

**The web effect:** Building fitness for Ryan means less time studying for Jake's homework help. Buying Frank a whiskey ($15) means less money for art supplies ($60). Each NPC pulls the player in a different direction through what their story demands.

**Beyond NPC stats — things the story can require:**
- Buy a dress for a dinner event → costs $80 → do you have it?
- Study for a quiz Jake gives you → need intelligence ≥ 15 → have you been studying?
- Gym with Ryan requires fitness ≥ 10 → have you been jogging?
- A photography opportunity requires confidence → have you been doing self-care?
- Social reputation at the diner → affects tips, which affects money, which affects everything
- Specific items (camera, gift, art supplies, gym membership) → need money at the right time

**How to design this:**
1. Define each NPC's personality and what they VALUE
2. The things they value become the stats/items the player must build
3. Activities that build those stats already exist in the game world naturally
4. The player discovers what each NPC needs by paying attention to their reactions
5. The tension: different NPCs need different things, and you can't build everything at once

### Guidelines

- Every milestone should have at least 2 gates (stat + flag, or stat + cross-NPC stat)
- Important milestones should have 3-4 gates
- Gates should feel logical — the player should understand WHY this combination matters when they see the content
- Don't make gates obscure or puzzle-like — the player should be able to intuit what's needed by paying attention to the NPC's personality
- Document stat budgets: how many opportunities exist, what right choices give, what thresholds require
- Each NPC should require at least one DIFFERENT stat than the others — no two NPCs should have identical requirements

---

## Motivation 4: "They Feel Real"

### What It Is

NPCs have agency. They refuse, withdraw, confront, notice things, have preferences, and react to the player's behavior — including behavior with OTHER NPCs. They're people, not content dispensers.

### Why It Matters

When NPCs always say yes, always have content ready, and never react to neglect or bad behavior — they feel like vending machines. When they refuse, get angry, notice things, and change their behavior based on the player's actions — they feel alive.

### How It Works

NPC behavior changes based on flags, trait levels, and cross-NPC conditions. Not just "content variant" changes — BEHAVIORAL changes like refusing to interact, changing tone, or confronting the player.

### Ideas for Game Design

**NPCs withdraw when neglected:**
- Skip wall knocking for 3+ nights → Jake stops knocking. The tap doesn't come. Silence through the wall. You have to go to HIS room to restart it. He won't say he's hurt. He'll just be drawing with his back to the door.
- Skip bookkeeping for a week → Frank fills the position. "Found someone else for the books." Trust didn't drop — access did. You have to earn the job back.

**NPCs refuse when pushed too far:**
- Flirt too aggressively during bookkeeping when frank_trust < 15 → next session, office door stays closed. "Not today, Lily." Come back in 2-3 days.
- Push Ryan too hard after he showed vulnerability → he retreats behind the grin. "We're cool, college girl." But the vulnerability is gone. Trust dropped. He won't open up again until you rebuild it.

**NPCs notice other NPCs:**
- Ryan sees Lily leaving Jake's room → makes pointed comments during truck rides. "Art class running late?" He's watching. He's competitive.
- Frank notices Lily bought Jake art supplies → mentions it during bookkeeping. "Fifty dollars on charcoal. You're generous." Not angry. Measuring.
- Jake overhears Ryan bragging to crew guys → mentions it through the wall. Quiet. Hurt. "Ryan said something about you today."
- Frank sees Lily being kind to Jake → Frank softens. The opposite of jealousy — respect. But only if frank_corruption is low.

**NPC mood after rejection or conflict:**
- Refuse Frank's arrangement → he's stiff and formal for 3 days. No warmth, clipped sentences, door closed more often. Then he thaws — and respects you more than if you'd accepted.
- Brothers discover the truth → 2-3 days of household tension. Cold dinners. Nobody talks. Then it breaks — either through confrontation or through fragile peace, depending on which path you chose.

**NPCs have preferences (not just stat checks):**
- Jake responds to emotional choices (asking about art, listening, being gentle). Physical aggression scares him. He withdraws from bold moves.
- Ryan responds to confidence (bold choices, direct eye contact, matching his energy). Being timid bores him.
- Frank responds to maturity (keeping secrets, being reliable, respecting boundaries). Childish behavior costs trust.
- The "right" approach is different for each NPC. What earns Jake's love LOSES Ryan's respect. What earns Frank's trust bores Ryan.

### Guidelines

- Every NPC should have at least one "refusal" trigger and one "withdrawal" behavior
- NPCs should notice at least one cross-NPC relationship dynamic
- Negative reactions should be TEMPORARY (2-3 days) unless it's a permanent route split
- NPCs should have distinct preferences that reward the player for learning who they are
- Confrontation scenes should be STORY events, not activity variants — they deserve full attention

---

## Motivation 5: "What Did I Miss?"

### What It Is

The player finishes the game knowing their playthrough was incomplete. They saw their version of the story — unique, personal, but visibly not everything. This drives replay desire.

### Why It Matters

If the player sees everything in one playthrough, there's no reason to replay. If they KNOW content exists that they didn't reach — because they chose a different path, invested in a different NPC, or missed a requirement — they want to play again differently.

### How It Works

Mutually exclusive content, permanent route splits, and visible incompleteness. The player should always feel like their version of the game was one of several possible versions.

### Ideas for Game Design

**Exclusive first-time events:**
- Three "first physical awareness" variants (Jake drawing session / Ryan creek swim / Frank hallway encounter). Only ONE fires based on who you invest in first. Two are permanently locked. The player literally cannot see all three in one playthrough.

**First milestone exclusivity:**
- First kiss with Jake: tender, over the sketchbook, glasses bumping foreheads
- First kiss with Ryan: aggressive, truck pulled over, mint gum and adrenaline
- First kiss with Frank: forbidden, kitchen at 2am, whiskey and "this can't happen"
- Only ONE is the canonical first kiss. The others happen through repeatable activities later, but the STORY MOMENT — the one-time milestone scene — belongs to whoever got there first.

**Route splits with real content behind them:**
- Ryan resist vs allow: each opens ~20% unique Ryan content and locks ~20% of the alternative
- Frank's arrangement: accept vs refuse creates two fundamentally different Frank arcs
- Corruption threshold: above X, certain scenes play one way. Below X, completely different. Can't see both.

**Multiple endings based on investment:**
- Mom returns. What did you build?
  - Deep with Jake → confession ending (Jake tells Frank, or they plan to continue)
  - Deep with Frank → "we need to talk" ending (Frank confronts Diana, or covers it up)
  - Deep with Ryan → "come with me" ending (Ryan offers escape from the household)
  - Deep with nobody → quiet ending (Lily packs her suitcase and leaves with Mom)
  - Deep with multiple → complicated ending (the household fractures or finds a new equilibrium)
- The player sees ONE ending. The others exist but require different playthroughs.

**Visible depth variation:**
- Player who went deep with Jake experienced 8 drawing session tiers, 5 wall knocking tiers, the art exhibition, the "I love you" scene. Player who focused on Ryan never got past the second drawing node. Same game, wildly different amounts of Jake content experienced.

### Guidelines

- At least 3 key moments per game should have mutually exclusive outcomes
- Endings should visibly branch — the player should feel "there must be other endings"
- Don't hide the incompleteness — make it visible (locked choices, NPCs mentioning things the player didn't do, hints at content not accessed)
- Replay should feel different, not just "same game, different stats" — genuinely different scenes, different NPC dynamics, different story beats

---

## Motivation 6: "I'm Barely Holding On"

### What It Is

The pressure of juggling money, relationships, NPC expectations, and a ticking clock. The player is always slightly behind on something. Not in crisis — just never quite comfortable.

### Why It Matters

When the player is comfortable, there's no tension. When they're always one bad week away from trouble — bills stacking up, NPCs expecting attention, a deadline approaching — every decision feels urgent. This is the engine that powers the other 5 motivations.

### How It Works

Economic pressure, trait decay, NPC expectations, crisis interruptions, and a hard deadline create overlapping pressure. No single source is overwhelming — it's the COMBINATION that creates the "barely holding on" feeling.

### Ideas for Game Design

**The impossible math:**
- $400 start. Monthly expenses: food $200, bus $80, art supplies $60, phone $45 = $385. Month one surplus: $15.
- Mom's transfer: "delayed." Maybe next week. Maybe never. The player can't count on it.
- Income sources: cleaning $20/day, bookkeeping $25/session, diner $45/shift, job site $40/shift. The math works IF you work every day — but working every day means no NPC time.
- The player is always choosing: work today (money) or invest in a relationship (future). Both are necessary. Neither is sufficient.

**Expenses that stack unpredictably:**
- Week 3: bus pass expired ($80) + art supplies due ($60) + food money ($50) = $190 needed. Player has $120. What gets skipped?
- Skip bus pass → some locations locked until renewed. Skip art supplies → drawing sessions with Jake are less effective. Skip food → Frank's trust drops.
- Each expense skipped has a different RELATIONSHIP cost, not just a money cost.

**Trait decay as maintenance pressure:**
- Skip an NPC for 3+ days → their love/trust decays. Not a lot — enough to feel the slide.
- Maintaining 3 NPCs means visiting each at least every 2-3 days. Plus work days for money. Plus solo activities for fitness/confidence. The math is tight.
- The player who tries to maintain everything stays at medium levels. The player who focuses gets deep with one NPC but watches others decay.

**Crisis interruptions:**
- Player had a plan: focus on Frank this week, build trust for the bookkeeping milestone. Then: money crisis (transfer bounced), Jake's door is closed (he saw something), Ryan wants to talk (he knows about Jake). Plan shredded. Now managing fires.
- Crises aren't random — they're triggered by flags and stat thresholds. But the player experiences them as interruptions to their strategy.

**The countdown:**
- Mom returns in X days. The number is visible. Always shrinking.
- Whatever the player is building — routines, relationships, physical escalation — has an expiration date.
- As the number drops: NPCs become more urgent ("Before your mom gets back..."), choices become more desperate, the stakes of every interaction increase.
- The countdown transforms every mundane activity into "this might be one of the last times."

**NPC expectations:**
- Frank expects food money weekly. Missing it costs trust.
- Ryan expects truck rides to continue. Suddenly stopping raises suspicion.
- Jake needs attention or he withdraws. His knock gets quieter, then stops.
- Each NPC has a minimum "maintenance cost" in time and attention. Combined, they exceed what the player can comfortably provide.

### The Hardship Web

Money pressure is just one strand. The REAL hardship comes from multiple NPCs pulling the player in different directions through what their stories NEED:

**The web:** Each NPC's story requires different stats, items, and time investments. Building one NPC means NOT building another. The player can't max everything.

```
Jake needs:           Ryan needs:           Frank needs:
  Beauty/confidence     Fitness               Intelligence
  Art supplies ($)      Gym membership ($)     Reliability (time)
  Vulnerability         Boldness               Maturity
  Study time            Workout time           Show-up-early time

Building fitness for Ryan = less time studying for Jake
Buying art supplies for Jake = less money for gym membership
Being patient for Frank = boring Ryan (he wants action)
Being bold for Ryan = scaring Jake (he needs gentleness)
```

**The web in practice:**
- Monday: Gym with Ryan (+fitness, +ryan_trust). But Jake knocked on the wall last night and she didn't visit. jake_love decays.
- Tuesday: Drawing with Jake (+beauty helps, +jake_love). But she skipped the job site. No money today. Bus pass expires tomorrow.
- Wednesday: Bookkeeping with Frank ($25, +frank_trust). But Ryan made a comment at dinner about "never seeing her anymore." ryan_love decays.
- Thursday: Need $80 for bus pass. Work diner shift ($45) + cleaning ($20) = $65. Not enough. Skip art supplies ($60) this month? Jake notices when she uses cheap paper.

**The hardship isn't any single pressure — it's ALL of them at once.** Money, stat requirements, NPC attention needs, time for self-improvement, and the countdown. Each is manageable alone. Together, they create the "barely holding on" feeling.

**How to design the web:**
1. Give each NPC a DIFFERENT primary stat requirement (no two NPCs need the same thing most)
2. Make the activities that build those stats cost TIME (which is the true scarce resource)
3. Add money costs that compete with each other (art supplies vs gym membership vs gifts)
4. Include NPC trait decay so the player can't just focus on one and forget the others
5. Layer crisis events on top that disrupt whatever the player planned

### Guidelines

- No single pressure source should be overwhelming — it's the COMBINATION that matters
- The player should feel "manageable but tight," not "impossible and frustrating"
- Economic pressure should force uncomfortable choices, not punishment
- Crisis events should feel like they emerge from the player's own actions (flags/stats triggering them), not random
- The countdown should affect NPC behavior, not just be a number — NPCs should feel the deadline too
- Each NPC should pull the player toward DIFFERENT activities — this is what creates the web

---

## The Daily Loop Format (Reference)

Research across 8 successful adult games revealed a common mechanical skeleton. This is reference material — a copyable format, not a motivation.

### The Universal Daily Structure

Most successful sandbox games divide each day into **3-4 time slots** with one major activity per slot:

```
MORNING SLOT
  └─ Obligation (school/work) or free activity

AFTERNOON SLOT
  └─ Stat building (gym, study, training)
  └─ OR NPC interaction
  └─ OR Job for money

EVENING SLOT
  └─ NPC social time
  └─ OR story event (if conditions met)

NIGHT SLOT
  └─ Intimate content (if relationship qualifies)
  └─ OR personal time
  └─ OR sleep

SLEEP → day advances, resources reset, periodic checks (rent, decay, grades)
```

### Three Activity Categories

Every repeatable activity falls into one of three categories:

| Category | What it gives | Examples |
|----------|--------------|---------|
| **Work** | Money | Jobs, odd tasks, chores, selling goods |
| **Training** | Player stats | Gym, study, yoga, self-care, skill practice |
| **Social** | Relationship points | Conversations, shared activities, dates, quality time |

**The core tension:** You need all three but can only do 1-2 per time slot.

### Four Resource Types

Every game manages these four resources:

| Resource | Purpose | Creates pressure through... |
|----------|---------|---------------------------|
| **Time** | Limits total daily actions | Can't do everything in one day |
| **Money** | Gates items, locations, NPC gifts | Work time competes with NPC time |
| **Player Stats** | Gates NPC routes, job access | Training time competes with social time |
| **Relationships** | Gates NPC content tiers | Maintenance of multiple NPCs competes with deepening one |

### The 5-Tier Escalation Ladder

Every game follows roughly this progression per NPC:

```
TIER 1 (Relationship 0-10): Meeting, casual interaction
  Activities: Basic social (eat together, small talk)
  Content: Clothed, friendly, establishing character

TIER 2 (Relationship 10-20): Growing closer, flirting begins
  Activities: Personal (help with tasks, shared hobbies, gifts)
  Content: Light touching, innuendo, emotional openness

TIER 3 (Relationship 20-30): Romantic/sexual tension
  Activities: Private settings (evening visits, solo hangouts)
  Content: First kisses, physical escalation, semi-explicit

TIER 4 (Relationship 30-40): Full intimacy
  Activities: Intimate encounters
  Content: Explicit scenes, deep emotional connection

TIER 5 (Relationship 40+): Deep/endgame content
  Activities: Special events, exclusive scenes
  Content: Most explicit, route-specific, emotionally deep
```

**Each NPC should be at a DIFFERENT tier at any given time.** Day 20 might be: Jake at Tier 3, Ryan at Tier 2, Frank at Tier 2. This creates variety.

### Five Engagement Hooks

What keeps players coming back day after day:

| Hook | What it feels like |
|------|--------------------|
| **"Almost there"** | Player is 2-3 points from next milestone with an NPC |
| **"Multiple irons"** | 3-4 NPC routes progressing simultaneously at different stages |
| **"What happens next"** | Story event ended on a cliffhanger or unresolved tension |
| **"Can I afford it?"** | Economic pressure creating urgency around upcoming expenses |
| **"Something different today"** | Random/conditional events that break routine with surprises |

### The Hardship Spectrum

Games fall on a spectrum. The most successful commit fully to one end:

```
PURE AUTHORED (no grind)          PURE SANDBOX (all grind)
Back to Freedom ←──────────────────────→ Degrees of Lewdity
Being a DIK                              Course of Temptation
         Milfy City              Road to Success
         Summertime Saga    Become Someone
```

**The middle ground (Become Someone's stat buttons) feels like chores.** Either commit to rich authored content OR commit to deep sandbox systems. Don't half-do both.

Our system is closest to the authored side (rich media, authored scenes) with sandbox structure (repeatable activities, stat progression). The key is making the repeatable activities feel like SCENES, not stat buttons.

---

## Applying These Motivations

### For Game Designers

When designing a game, go through each motivation and ask:

1. **"I can't have everything"** — Where are the story forks? Which NPC-vs-NPC moments exist? What's exclusive?
2. **"This matters"** — Which 3-5 choices are permanent? What do they lock/unlock?
3. **"I earned this"** — What are the multi-gate milestones? What cross-NPC requirements exist?
4. **"They feel real"** — How does each NPC refuse? What do they notice? How do they react to neglect?
5. **"What did I miss?"** — How many exclusive paths exist? How many endings? What's the replay hook?
6. **"I'm barely holding on"** — What's the economic math? What decays? What's the deadline?

### For Prompt Engineering

When writing prompts that generate game content, teach each motivation:

- Don't generate NPC arcs that are independent — require cross-NPC investment
- Don't generate choices that both set the same flag — generate different flags per path
- Don't give automatic stats for visiting — require right choices for meaningful gains
- Don't make NPCs always available — include refusal/withdrawal triggers
- Don't converge all paths to the same ending — branch endings based on investment
- Include economic pressure that makes comfort impossible

### What These Motivations Are NOT

- NOT specific mechanics to copy (escalating rent, stamina bars, gallery systems)
- NOT restrictions to impose (time slot limits, energy gates, activity caps)
- NOT content prescriptions (write more sex scenes, add more dialogue)
- NOT engine features to build (new block types, new condition systems)

They are FEELINGS the player should have. The specific implementation depends on the game, the setting, the NPCs, and the story being told. Two games can achieve the same motivation through completely different designs.

---

## Companion Documents

- `activity_types.md` — Activity structure formats (Solo, Task, Hangout, Chain, Scene)
- `game_design_observations.md` — Analysis of CoT, Become Someone, Back to Freedom
- `game_design_rules.md` — Technical rules for game generation
- `game_design_patterns.md` — Specific mechanical patterns for TOML generation
