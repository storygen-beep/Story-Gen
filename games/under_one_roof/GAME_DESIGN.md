# Under One Roof — Complete Game Design Document

Blueprint for TOML generation. No TOML writing until this document is complete and reviewed.

Reference: `prompts/game_design_motivations.md`, `prompts/activity_types.md`, `prompts/game_design_rules.md`, `prompts/game_design_patterns.md`, `prompts/game_design_observations.md`

---

# Section 1: Core Redesign Philosophy

## The 10 Design Rules

Every section of this document must satisfy ALL of these. If a design violates any rule, fix it before moving on.

### Rule 1: No Two NPCs Share Mechanics
Jake, Ryan, and Frank each have a UNIQUE activity mechanic. Jake's drawing sessions feel nothing like Ryan's truck rides or Frank's bookkeeping — not just different text, different STRUCTURE, different choice patterns, different escalation logic.

### Rule 2: Real Branching, Not "Continue or Exit"
Every activity with choices must have at least one choice that leads to a DIFFERENT scene, not just "go deeper" or "leave." Choices lead to different nodes with different content and different stat effects.

### Rule 3: Multi-Stat Gating
No milestone gates on a single stat. Every gated choice requires at least 2 conditions (stat + flag, or stat + cross-NPC stat, or stat + item flag). Important milestones require 3-4 gates.

### Rule 4: Cross-NPC Awareness
NPCs react to the player's behavior with OTHER NPCs. Jake hears through the wall. Ryan sees evidence. Frank notices patterns. Awareness creates flags that ALTER future activity content.

### Rule 5: NPCs Refuse and Withdraw
Every NPC has triggers that make them refuse interaction or withdraw for 2-5 days. Refusal is not permanent — it's a temporary behavioral change that requires specific recovery actions.

### Rule 6: Economic Pressure Is Real
Automatic recurring expenses actually deduct money. Income requires time that competes with NPC time. The economic math is genuinely tight in weeks 1-4 and creates real trade-offs throughout.

### Rule 7: Flags Are Set AND Read
Every branch flag set by a player choice must be checked by at least one future scene. If a flag exists, something downstream must care about its value. No decorative flags.

### Rule 8: Permanent Forks Don't Reconverge
The 5 permanent forks create genuinely different content downstream. The brothers-discover fork produces 3 structurally different final acts, not 3 versions of the same scenes.

### Rule 9: Each NPC Requires Different Player Stats
Jake gates on beauty + jake_love. Ryan gates on fitness + ryan_trust. Frank gates on intelligence + frank_trust. No two NPCs have the same primary gating stat. This forces the player to spread investments.

### Rule 10: Endings Are Earned, Not Selected
Each ending has specific stat thresholds, flag requirements, and route conditions. The player doesn't pick an ending — their 56 days of choices determine which ending fires.

---

## 6 Motivations → Game Systems

| Motivation | Primary System | Secondary System |
|-----------|---------------|-----------------|
| "I Can't Have Everything" | NPC-vs-NPC story forks (Sec 6A) | Schedule conflicts — activities overlap (Sec 4) |
| "This Matters" | 5 permanent forks with downstream content (Sec 6A) | Tone flags changing activity variants (Sec 3D) |
| "I Earned This" | Multi-gate milestones per NPC (Sec 2E) | NPC-specific stat requirements (Sec 2B) |
| "They Feel Real" | Refusal/withdrawal triggers per NPC (Sec 3) | Cross-NPC awareness flags (Sec 3D) |
| "What Did I Miss?" | 8 endings with different conditions (Sec 7) | Exclusive first-time events (Sec 6B) |
| "I'm Barely Holding On" | Impossible economic math (Sec 2D) | Trait decay + NPC expectations (Sec 5) |

---

## What Stays

- **Premise:** Lily Chen (19), staying with Frank (45, step-father), Ryan (23, step-brother), Jake (20, step-brother) for 56 days until mom Diana returns from Dubai
- **21 locations:** 11 on property, 7 in town, 3 on trail
- **Character backstories:** All personality, psychology, resistance patterns, emotional quadrants from `book_phases/2_characters_and_stats.md`
- **Clothing tier system:** Corruption-gated wardrobe (Basic → Cute → Bold → Daring)
- **Shared skill unlock flags:** exposure → flirt → tease → kiss → handjob → blowjob → sex
- **TOML engine:** Schema v0.2, no engine changes
- **@-syntax customization:** NPC names and relationship labels

## What's Rebuilt

- **All activity structures** — every NPC activity redesigned with unique mechanics
- **Stat gating** — multi-stat with NPC-specific requirements, not corruption-only
- **Story arc** — real forks, cross-NPC consequences, hidden payoffs
- **Pressure systems** — implemented, not just described
- **Endings** — 8 endings with explicit conditions and different final-week structures
- **NPC behavior** — refusal, withdrawal, cross-NPC awareness, distinct preferences

---

# Section 2: Player Stats & Economy

## 2A. Stat Definitions

### Player Stats (7 total)

| Stat | Start | Range | Clamp | Decays | Role |
|------|-------|-------|-------|--------|------|
| **corruption** | 0 | 0-250 | false | No | Universal progression. Gates escalation choices across all NPCs. Grows from activities, encounters, story events, clothing. NO LONGER the sole gate — always combined with other stats. |
| **confidence** | 10 | 0-100 | true | No | Gates assertive choices, self-initiation, negotiation. Key Ryan secondary gate. Built through exercise, confrontations, bold clothing, achievements. Permanent — represents growth. |
| **money** | 400 | unclamped | false | N/A | Economic pressure engine. Depletes through expenses, replenished through work. Creates time-money trade-offs. |
| **energy** | 100 | 0-100 | true | Resets daily | Daily activity budget. 4-5 activities without rest. Forces daily prioritization. Dynamic max: 100 base, 110 at fitness ≥ 61. |
| **fitness** | 20 | 0-100 | true | -1 per 3 days | Ryan's PRIMARY gate. Body condition. Built through gym, swimming, jogging, job site. Affects physical activity access and Ryan's respect. |
| **beauty** | 30 | 0-100 | true | -1 per 2 days | Jake's PRIMARY gate. Presentation. Built through grooming, skincare, yoga, wardrobe. Affects drawing quality, diner tips, NPC compliments. |
| **intelligence** | 15 | 0-100 | true | No | Frank's PRIMARY gate. NEW STAT. Analytical ability. Built through studying, campus classes, reading, bookkeeping practice. Permanent — represents knowledge. |

### NPC Stats (per NPC, 3 each)

| Stat | Range | Decay | Role |
|------|-------|-------|------|
| **love** | 0-40 | -1 per 5 days without interaction | Emotional connection. Gates romantic milestones. |
| **trust** | 0-35 | -1 per 7 days without interaction | Reliability + vulnerability. Gates intimate settings and confessions. |
| **corruption** | 0-50 | No decay | Shared boundary-crossing. Once corrupted, stays corrupted. |

---

## 2B. NPC-Specific Stat Requirements

**The core mechanic that makes each NPC feel different:**

### Jake — The Artist

| Milestone | Player Gates | NPC Gates | Flag Gates |
|-----------|-------------|-----------|------------|
| Drawing session depth 1 | beauty ≥ 25 | jake_love ≥ 8 | — |
| Drawing session depth 2 (sees sketch of her) | beauty ≥ 30 | jake_love ≥ 12 | exposure_unlock |
| Posing (clothed) | beauty ≥ 35, corruption ≥ 50 | jake_love ≥ 15 | — |
| First kiss | beauty ≥ 35, corruption ≥ 70 | jake_love ≥ 18, jake_trust ≥ 15 | flirt_unlock, kiss_unlock = false |
| Posing (revealing) | beauty ≥ 40, corruption ≥ 100 | jake_love ≥ 20 | tease_unlock |
| Handjob | beauty ≥ 40, corruption ≥ 120 | jake_love ≥ 22, jake_trust ≥ 18 | kiss_unlock, handjob_unlock = false |
| Posing (nude) | beauty ≥ 45, corruption ≥ 140 | jake_love ≥ 25 | handjob_unlock |
| Oral | corruption ≥ 160 | jake_love ≥ 28, jake_corruption ≥ 20 | blowjob_unlock = false |
| Sex | corruption ≥ 190 | jake_love ≥ 32, jake_trust ≥ 25 | sex_unlock = false |

**Why beauty matters for Jake:** He's an artist. He wants to draw her. Higher beauty = better subject = deeper artistic connection = more intimate poses. The stat makes narrative sense — she's investing in being someone worth painting.

### Ryan — The Competitor

| Milestone | Player Gates | NPC Gates | Flag Gates |
|-----------|-------------|-----------|------------|
| Gym together | fitness ≥ 25 | — | — |
| Truck ride depth 1 | confidence ≥ 15 | ryan_trust ≥ 5 | — |
| Truck ride depth 2 | fitness ≥ 30, confidence ≥ 20 | ryan_trust ≥ 10 | exposure_unlock |
| First flirt | fitness ≥ 30, corruption ≥ 50 | ryan_love ≥ 10 | flirt_unlock = false |
| Creek challenge | fitness ≥ 35 | ryan_trust ≥ 12 | — |
| First kiss | confidence ≥ 25, corruption ≥ 80 | ryan_love ≥ 15, ryan_trust ≥ 12 | kiss_unlock = false |
| Gym escalation | fitness ≥ 40, corruption ≥ 110 | ryan_trust ≥ 18 | tease_unlock |
| Handjob | fitness ≥ 40, corruption ≥ 130 | ryan_love ≥ 20, ryan_trust ≥ 18 | handjob_unlock = false |
| Oral | corruption ≥ 160 | ryan_love ≥ 25, ryan_corruption ≥ 20 | blowjob_unlock = false |
| Sex | corruption ≥ 200 | ryan_love ≥ 28, ryan_trust ≥ 22 | sex_unlock = false |

**Why fitness matters for Ryan:** He respects physicality. He doesn't open up to someone who can't keep up. Gym together, creek swimming, job site work — all require her to be physically capable. Timidity bores him. Matching his energy earns his respect.

### Frank — The Authority

| Milestone | Player Gates | NPC Gates | Flag Gates |
|-----------|-------------|-----------|------------|
| Bookkeeping depth 1 | intelligence ≥ 20 | frank_trust ≥ 8 | chores_started |
| Office conversation | intelligence ≥ 25 | frank_trust ≥ 12 | bookkeeping_started |
| Financial discovery | intelligence ≥ 30 | frank_trust ≥ 16 | — |
| First flirt | intelligence ≥ 25, corruption ≥ 80 | frank_love ≥ 12 | flirt_unlock = false |
| Late-night kitchen depth | intelligence ≥ 30, corruption ≥ 100 | frank_love ≥ 16, frank_trust ≥ 18 | exposure_unlock |
| First kiss | corruption ≥ 120 | frank_love ≥ 20, frank_trust ≥ 20 | kiss_unlock = false |
| Office escalation | intelligence ≥ 35, corruption ≥ 140 | frank_trust ≥ 22 | tease_unlock |
| Handjob | corruption ≥ 160 | frank_love ≥ 25, frank_trust ≥ 24 | handjob_unlock = false |
| Oral | corruption ≥ 180 | frank_love ≥ 28, frank_trust ≥ 26 | blowjob_unlock = false |
| Sex | corruption ≥ 210 | frank_love ≥ 30, frank_trust ≥ 28 | sex_unlock = false |

**Why intelligence matters for Frank:** He values competence. Bookkeeping requires real analytical skill. He respects people who can keep up with him intellectually — handle the numbers, understand the business, hold a conversation about something that matters. Intelligence gates the depth of their professional bond, which is the foundation for everything personal that follows.

### Cross-NPC Requirements (Special Scenes)

| Scene | Requirements | Why |
|-------|-------------|-----|
| Frank's office scene (Week 6) | frank_trust ≥ 20 AND jake_love ≥ 15 | Frank softens because he sees Lily treating Jake well |
| Ryan's vulnerability (Week 7) | ryan_trust ≥ 22 AND frank_trust ≥ 10 | Ryan only opens up if Lily has earned Frank's respect too |
| Jake's "I love you" (Week 8) | jake_love ≥ 35 AND ryan_trust ≥ 12 | Jake needs to feel Lily navigated Ryan's dynamic without destroying the household |
| Frank's confession (Week 8) | frank_love ≥ 28 AND intelligence ≥ 35 AND jake_love ≥ 10 | Frank sees Lily as a complete person — smart, kind to his son, and someone he genuinely wants |
| All-Three dinner scene | jake_love ≥ 20 AND ryan_love ≥ 20 AND frank_love ≥ 20 | All NPCs invested. Household tension at peak. |

---

## 2C. Stat Growth Sources

### Player Stat Growth

| Stat | Activity Sources | Growth per Session | Max over 60 Days |
|------|-----------------|-------------------|------------------|
| **corruption** | Activities (+2-5), random encounters (+2-3), story events (+3-8), bold clothing (+1-2/day) | Variable | ~220 (aggressive play), ~120 (moderate), ~60 (avoidant) |
| **confidence** | Gym (+1), jogging (+1), bold clothing first wear (+2), confrontations (+3-5), diner shifts (+1), assertive choices (+1-2) | +1-5 | ~80 (active), ~40 (passive) |
| **money** | Cleaning ($20), bookkeeping ($25), job site ($40), diner ($45), modeling ($30-80), favors ($100), arrangement ($150) | $20-150 | Net depends on expenses |
| **fitness** | Gym (+3), park jog (+2), property jog (+1), creek swim (+2), hiking (+2), job site (+1) | +1-3 | ~55 (gym 3x/week), ~35 (jog only) |
| **beauty** | Yoga (+2), self-care (+2), spa day (+3), new wardrobe (+1 per tier), skincare routine (+1) | +1-3 | ~50 (active grooming), ~25 (minimal) |
| **intelligence** | Campus classes (+3), library studying (+2), bookkeeping practice (+1), journal (+1), reading (+1) | +1-3 | ~50 (studying 3x/week), ~25 (bookkeeping only) |

### Key Constraint: Building One Stat Costs Time for Others

A day has ~4-5 activity slots. Building fitness (gym in town = bus ride + 2h workout) costs an entire morning/afternoon. That's time NOT studying (intelligence), NOT grooming (beauty), NOT visiting an NPC (love/trust).

**Week 1-2 Example (Jake-focused player):**
- Morning: Yoga (+2 beauty, 1h)
- Late morning: Campus art class (+3 intelligence, 3h, requires bus)
- Afternoon: Drawing session with Jake (+love, +trust, 2h)
- Evening: Dinner (all NPCs, +1 love each)
- Night: Wall knocking with Jake (+love, 1h)

Result: Beauty growing, intelligence growing, Jake love growing. BUT: fitness decaying (-1/3 days), Ryan ignored (love decaying), Frank ignored (trust decaying), no money earned.

**Same player on Week 3 when rent is due:**
- Late morning: House cleaning ($20, 3h)
- Afternoon: Bookkeeping with Frank ($25, 2h) — requires corruption ≥ 40 AND intelligence ≥ 20
- Evening: Diner shift ($45, 4h) — misses dinner, misses all NPCs for evening

Result: $90 earned. But Jake got no visit (-love decay), Ryan got no visit, no fitness, no beauty maintenance. One work day costs 2-3 days of NPC investment.

---

## 2D. Economic Math

### Starting Position
- **Cash:** $400
- **Monthly expenses:** Bus $80 + art supplies $60 + phone $45 + food $200 = $385
- **Mom's transfer:** $200/month (unreliable — arrives late 50% of the time, bounces 20% of the time)

### Week-by-Week Cash Flow: Jake-Focused Player

| Week | Income | Expenses | Balance | Notes |
|------|--------|----------|---------|-------|
| 1 | $0 (settling in) | $50 (food) | $350 | No work yet. Learning the house. |
| 2 | $60 (3 cleans) | $50 (food) | $360 | Mom sends $200 (arrives late, Week 3) |
| 3 | $80 (4 cleans) | $50 (food) + $80 (bus) | $310 | Bus pass due. Art supplies can wait 1 week. |
| 4 | $100 (5 cleans) + $200 (mom) | $50 (food) + $60 (art) + $45 (phone) | $455 | Breathing room — but bookkeeping requires corruption ≥ 40 |
| 5 | $100 (cleans) + $75 (3 bookkeeping) | $50 (food) | $530 | Comfortable IF she's been escalating |
| 6 | $100 + $100 (bookkeeping) | $50 + $80 (bus) | $600 | But wardrobe costs: Cute tier = $200-300 |
| 7 | $100 + $100 | $50 + $60 (art) + $45 (phone) | $645 | Mom's transfer bounces this month |
| 8 | $100 + $100 | $50 + $80 (bus) + crisis expenses | ~$600 | Endgame — money matters less, relationships matter more |

### The Impossible Triangle

In any given week, the player can't afford ALL of:
- Bus pass ($80/month) — needed for town access (campus, gym, diner, shops)
- Art supplies ($60/month) — needed for Jake's drawing sessions, campus work
- Gym membership ($30/month) — needed for Ryan's respect, fitness building

Total: $170/month for all three. Base income (cleaning only): $400/month. After food ($200) and phone ($45): $155 left. Not enough for all three.

**What gets cut determines which NPC path:**
- Cut gym → Ryan disappointed, fitness decays, locked out of gym activities
- Cut art supplies → Jake's drawing quality drops, campus work suffers, beauty maintenance harder
- Cut bus pass → dependent on Ryan's truck for town access (increases Ryan dependency and corruption)

### NPC-Specific Money Investments

| Investment | Cost | Flag Set | NPC Effect | Competing With |
|-----------|------|----------|------------|----------------|
| Art supplies for Jake | $60/month | has_art_supplies | jake_love +3, drawing sessions improved | Gym membership, bus pass |
| Gym membership | $30/month | has_gym_membership | Access to gym activities with Ryan | Art supplies, savings |
| Gas money for Ryan (without asking) | $10 | gave_gas_money | ryan_love +3, ryan_trust +2 | Everything else |
| Groceries + cook without asking | $40 | cooked_for_house | frank_love +4, frank_trust +2 | Personal expenses |
| Pay part of utility bill | $50 | paid_utilities | frank_trust +5 | Major sacrifice |
| Buy Jake art class ticket | $30 | bought_art_class | jake_love +3, jake_trust +2 | Rent money |
| Beer for truck trip | $15 | bought_beer | ryan_trust +2 | Small but adds up |
| Whiskey for Frank | $15 | bought_whiskey | frank_love +2 | Small but adds up |
| Nice dress for dinner | $50-70 | has_nice_dress | All NPCs notice (+corruption, +love) | Significant spend |

---

## 2E. Stat Budgets Per NPC

### Jake Stat Budget

| Metric | Value | Notes |
|--------|-------|-------|
| Available interactions over 56 days | ~40 (drawing 5x/week + library 2x + creek 1x + wall nightly) | Highest NPC availability |
| Base love per visit | +1 | Just showing up |
| Right-choice bonus | +2 to +4 | Asking about art, complimenting work, holding pose |
| Max love with perfect play | ~42 | 40 visits × avg +1.05 base + ~50 right-choice bonus |
| Max love with click-through play | ~22 | 40 visits × +0.55 (base only, some missed) |
| Required for deepest content | jake_love ≥ 32 | Sex tier |
| % right choices needed for deepest | ~70% | Must make good choices in 28/40 visits |
| Required beauty for deepest | ≥ 45 | Needs active beauty maintenance |
| Unique requirement | beauty (no other NPC needs it as primary) | |

### Ryan Stat Budget

| Metric | Value | Notes |
|--------|-------|-------|
| Available interactions over 56 days | ~30 (truck 3x/week + gym 2x + job site 2x + TV 2x) | Medium availability |
| Base trust per visit | +1 | Just showing up |
| Right-choice bonus | +2 to +3 | Matching energy, winning challenges, being bold |
| Max trust with perfect play | ~35 | 30 visits × avg base + right-choice bonus |
| Max trust with click-through play | ~18 | 30 visits × base only |
| Required for deepest content | ryan_trust ≥ 22, ryan_love ≥ 28 | Sex tier |
| % right choices needed | ~65% | Must win/match in 20/30 visits |
| Required fitness for deepest | ≥ 40 | Needs regular gym/exercise |
| Unique requirement | fitness (no other NPC needs it as primary) | |

### Frank Stat Budget

| Metric | Value | Notes |
|--------|-------|-------|
| Available interactions over 56 days | ~25 (bookkeeping 3x/week + cooking 3x + workshop 2x + late night ~1x) | Lowest availability — hardest NPC |
| Base trust per visit | +1 | Just showing up |
| Right-choice bonus | +2 to +3 | Being reliable, showing competence, keeping secrets |
| Max trust with perfect play | ~32 | 25 visits × avg base + right-choice bonus |
| Max trust with click-through play | ~15 | 25 visits × base only |
| Required for deepest content | frank_trust ≥ 28, frank_love ≥ 30 | Sex tier |
| % right choices needed | ~80% | Must be reliable in 20/25 visits — hardest NPC |
| Required intelligence for deepest | ≥ 35 | Needs regular studying |
| Unique requirement | intelligence (no other NPC needs it), reliability flags | |

---

# Section 3: NPC Mechanical Redesign

## 3A. Jake Harmon — The Artist

### Unique Mechanic: Sketchbook Progress

Jake's activities revolve around his DRAWINGS of Lily. This is not metaphor — it's a tracked system:

- Jake works on specific drawings across multiple sessions
- Each drawing has a SUBJECT (hands, portrait, full body, nude) that determines its corruption tier
- Drawing quality depends on Lily's beauty stat + her choices during posing sessions
- Completed drawings are milestones that unlock the next relationship tier
- The SUBJECT of each drawing is influenced by player choices — she can steer toward innocent (portrait) or intimate (nude)
- Completed drawings become physical evidence that can be FOUND by other NPCs (cross-NPC awareness)

**Drawing Progression:**

| Drawing # | Subject | Required Beauty | Required jake_love | Completion Sessions | What It Unlocks |
|-----------|---------|----------------|-------------------|--------------------|----|
| 1 | Her hands | 25 | 8 | 3 sessions | Depth 1 — longer drawing scenes |
| 2 | Portrait (face) | 30 | 12 | 4 sessions | Depth 2 — personal conversations during drawing |
| 3 | Full figure (clothed) | 35 | 16 | 4 sessions | Clothed posing choices, modeling income ($30) |
| 4 | Intimate pose (semi-clothed) | 40 | 20 | 5 sessions | Tease/flirt during posing, modeling income ($50) |
| 5 | Nude study | 45 | 25 | 5 sessions | Full nude modeling, income ($80), most intimate drawing content |

**How it works in gameplay:**
- Each drawing session, Jake makes progress on the current drawing (1 session = 1 progress point)
- If Lily's beauty is below the requirement, progress is slower (2 sessions per point instead of 1)
- When a drawing completes, it's a milestone moment — Jake shows her, they react, the relationship deepens
- The completed drawing EXISTS as a flag (drawing_1_complete, drawing_2_complete, etc.)
- These drawing flags are what Frank can FIND (cross-NPC trigger)

### Choice Style: Quiet and Incremental

Jake's choices should feel like natural extensions of the art process. NOT "kiss him / don't kiss him" — instead:

- "Lower the strap for better light" / "Keep the strap up" / "Suggest a different pose"
- "Hold still — he's concentrating" / "Shift position slightly" / "Ask to see what he has so far"
- "Look at his hands while he draws" / "Look at the drawing" / "Close your eyes"

The escalation is hidden inside artistic decisions. Each choice about posing, positioning, and attention is also a choice about intimacy.

### Activities (5)

1. **Drawing Session** — Type: Chain. Location: Jake's Room. Time: 14:00-17:00. Energy: 15.
   Core Jake activity. Multi-node chain tracking drawing progress. Choices affect drawing quality and relationship depth. Beauty stat affects drawing completion speed.

2. **Library Studying** — Type: Chain. Location: Library. Time: 13:00-16:00. Energy: 15.
   Art theory discussions, homework help. Intelligence matters here too (art history requires knowledge). Choices: discuss art seriously (+jake_trust) vs make it personal (+jake_love).

3. **Creek Swimming (contemplative)** — Type: Scene. Location: Creek. Time: 15:00-17:00. Energy: 30.
   Quiet, observational. Jake sketches while she swims. The scene is about being WATCHED by someone who sees beauty, not lust. Choices about exposure are artistic, not sexual. Fitness gate for swimming depth.

4. **Wall Knocking** — Type: Chain. Location: Lily's Room. Time: 22:00-00:00. Energy: 10.
   Nightly ritual. Tap-tap through the wall. Responses: knock back (continue), silence (jake_love -1 next day), open his door (escalation). Consequences: if she knocks back but doesn't visit for 3 nights, Jake's knock gets quieter. 5 nights of silence = Jake stops knocking (withdrawal flag). Recovery requires visiting his room to restart.

5. **Park Sketching** — Type: Scene. Location: Park. Time: 10:00-13:00 (weekends). Energy: 15.
   Public, limited escalation. Jake sketches in the park, Lily joins. Peaceful. No physical escalation beyond sitting close. Good for trust-building in a safe environment. The only Jake activity that can't escalate physically.

### Refusal Triggers

| Trigger | Behavior | Duration | Recovery |
|---------|----------|----------|----------|
| jake_love < milestone threshold | Won't escalate to next tier. "I'm not... I don't think..." Redirects to drawing. | Until threshold met | Build love through right choices |
| Heard Lily with Ryan through wall (flag: jake_heard_ryan) | Draws landscapes instead of her. Doesn't initiate wall knocking. Answers door but doesn't invite her in. | 2-3 days | Visit him, ask about his art. Don't mention Ryan. He needs to feel chosen. |
| Sees Lily leaving Frank's office late (flag: jake_saw_frank) | Goes quiet at meals. Sketchbook stays closed. "I need to work on my portfolio." | 3-4 days | Longer recovery. Requires a drawing session where she brings HIM art supplies (money gate: has_art_supplies flag). |
| Post-crisis (brothers_discover) | Severe withdrawal. Door closed. No wall knocking. Won't come to meals for 2 days. | 4-5 days | Lily must go to his room and sit with him without pushing. The first session back is just sitting in silence. |

### Preferences (What Earns vs Costs)

| Action | Effect | Why |
|--------|--------|-----|
| Ask about his art sincerely | jake_love +2, jake_trust +1 | He wants to be SEEN |
| Compliment a specific drawing detail | jake_love +3 | Attention to his work = attention to him |
| Be vulnerable (share fear, admit struggle) | jake_trust +3 | He responds to honesty |
| Be bold/aggressive physically | jake_trust -2, jake_corruption +2 | He's not Ryan. Aggression scares him. |
| Compare him to Ryan ("you're different") | jake_love +1, jake_trust -1 | He's flattered but knows it's manipulation |
| Buy him art supplies | jake_love +3, jake_trust +2 | Money spent on his DREAM, not his body |
| Wear Bold+ clothing around him | jake_corruption +1 | He notices. He doesn't like that he notices. |

---

## 3B. Ryan Harmon — The Competitor

### Unique Mechanic: Challenge System

Ryan's activities center on CHALLENGES — dares, competitions, tests of will. This is not metaphor — it's a gameplay mechanic:

- Ryan proposes challenges during activities (arm wrestling, pushup contests, "bet you won't", driving chicken)
- Each challenge has a WIN outcome and a LOSE outcome
- Winning earns ryan_trust (he respects equals). Losing earns ryan_corruption (trying hard is attractive to him)
- Lily can RAISE THE STAKES of challenges ("If I win, you tell me about the scar")
- Stakes determine the stat payout — higher stakes = higher reward regardless of win/lose
- Some challenges have FITNESS GATES — can't challenge if fitness is too low

**Challenge Outcomes:**

| Result | ryan_trust | ryan_love | ryan_corruption | Why |
|--------|-----------|-----------|----------------|-----|
| Win (matched his energy) | +3 | +1 | — | He respects her |
| Win (raised stakes) | +4 | +2 | — | She's playing his game better than him |
| Lose (tried hard) | +1 | — | +2 | He finds effort attractive |
| Lose (gave up) | -1 | — | — | Boring. He walks away. |
| Decline challenge | — | — | — | Neutral — but no progress |

### Choice Style: Bold and Direct

Ryan's choices should feel like negotiations and dares:

- "Match his pushup count" / "Quit at 15" / "Raise: if I win, you drive me to town whenever I ask"
- "Hold eye contact" / "Look away first" / "Say exactly what you're thinking"
- "Take the dare" / "Dare him back" / "Walk away"

The escalation comes through CONFIDENCE, not corruption. Ryan doesn't want someone who submits — he wants someone who plays back.

### Activities (5)

1. **Truck Ride** — Type: Chain. Location: Ryan's Truck. Time: 09:00-11:00 or 15:00-17:00. Energy: 10.
   The destination MATTERS. Different destinations unlock different conversation topics and challenges:
   - Town run: casual, low stakes. Good for trust-building.
   - Job site: work-adjacent. Ryan in his element.
   - Creek (remote): isolated. Highest escalation potential.
   - Trail head: adventure energy. Challenge opportunities.
   Choices: where to go, how to respond to his banter, whether to match his energy or defer.

2. **Gym Workout** — Type: Chain + Task. Location: Gym. Time: 07:00-09:00 or 16:00-18:00. Energy: 30.
   Requires has_gym_membership flag ($30/month). Workout is a Task (fitness gains guaranteed). The CHALLENGE is the relationship mechanic — Ryan proposes competitions. Fitness stat gates which exercises they can do together. Higher fitness = more intense workouts = more respect = deeper content.

3. **TV Couch** — Type: Hangout. Location: Living Room. Time: 19:00-22:00. Energy: 15.
   Hub menu. Multiple options: watch together (+1 love), comment on show (+1 trust), remove cushion (love ≥ 8, leads to proximity chain). UNIQUE: Frank can walk through (random 30% chance). If Frank present, certain choices are unavailable but dare-energy increases (Ryan dares Lily to do things with Frank nearby).

4. **Job Site** — Type: Task. Location: Workshop. Time: 09:00-12:00. Energy: 25. Money: +$40.
   Physical work. Earns money AND fitness. One moment mid-task: heavy lifting (fitness gate), problem-solving, or banter. The choice determines whether Ryan gains trust (she's useful) or love (she's fun to have around).

5. **Creek Swimming (competitive)** — Type: Chain. Location: Creek. Time: 15:00-17:00. Energy: 30.
   Different from Jake's contemplative creek. Ryan's version: racing, splashing, physical competition. Challenges: who can hold their breath longer, who can swim to the rock first. Fitness ≥ 30 gate for competitive swimming. Winning = trust. Losing = he teaches her (intimate physical contact). High corruption gate for skinny-dipping dare.

### Refusal Triggers

| Trigger | Behavior | Duration | Recovery |
|---------|----------|----------|----------|
| ryan_trust < milestone threshold | Deflects vulnerability with jokes. "Relax, I was just messing with you." Won't share real stories or answer serious questions. | Until threshold met | Win challenges, match energy, don't push emotional topics |
| Lily was timid after he showed vulnerability | Goes out more. Comes home late. Stops offering rides. "I got stuff to do." | 1-2 days | Short recovery. Give him space, then match energy next interaction. Don't mention the vulnerable moment. |
| Discovers Lily with Jake (flag: ryan_saw_jake) | Competitive, not withdrawn. Louder at dinner. Makes pointed comments. "Art class running late?" Tries harder to get her attention. | 3-4 days | He doesn't need comfort — he needs to win. Take his challenge, match his energy, show him he matters too. |
| Post-crisis (brothers_discover) | Disappears for a day (takes truck, doesn't say where). Returns quiet. Won't make eye contact for 2-3 days. | 3-4 days | Let him come back on his own terms. When he offers a ride, take it. The offer IS the recovery. |

### Preferences (What Earns vs Costs)

| Action | Effect | Why |
|--------|--------|-----|
| Win a challenge he proposed | ryan_trust +3 | He respects equals |
| Match his energy in banter | ryan_love +2 | He wants someone who plays back |
| Be vulnerable/emotional | ryan_trust -1 | He doesn't know what to do with feelings |
| Be physically bold (initiate contact) | ryan_love +2, ryan_corruption +1 | Directness is his language |
| Back down from a dare | ryan_trust -1, ryan_love -1 | Boring. Disappointing. |
| Cover for him with Frank | ryan_trust +3 | Loyalty earns trust |
| Give him gas money without asking | ryan_love +3 | She noticed. She cared. She didn't make a thing of it. |
| Be timid/apologetic | ryan_love -1 | He needs someone who doesn't shrink |

---

## 3C. Frank Harmon — The Authority

### Unique Mechanic: Trust Ledger

Frank's progression tracks RELIABILITY through accumulated commitment flags. This is not a stat — it's a collection of specific flags that prove Lily is dependable:

- `bookkeeping_on_time_1`, `bookkeeping_on_time_2`, `bookkeeping_on_time_3` — showed up 3x when scheduled
- `food_money_paid_1`, `food_money_paid_2` — paid food contribution on time twice
- `kept_financial_secret` — didn't tell Ryan or Jake about Frank's debt
- `house_rules_followed` — didn't break curfew or house rules for 2 weeks
- `helped_workshop_unprompted` — came to workshop without being asked

Frank's deeper milestones require BOTH stat thresholds AND specific reliability flags. A player with frank_trust = 25 but no reliability flags can't access the same content as a player with frank_trust = 20 but 4 reliability flags.

**How reliability flags work:**
- Each flag is set by a specific action or maintained behavior
- Some are one-time (kept_financial_secret), others are cumulative (bookkeeping_on_time_X)
- Missing a commitment PREVENTS the next flag from incrementing (skipped bookkeeping = bookkeeping_on_time counter resets)
- The trust STAT tracks emotional warmth. The LEDGER tracks professional respect. Both are needed.

### Choice Style: Formal and Loaded

Frank's choices should feel like workplace conversations where every word has a double meaning:

- "Stay professional" / "Let the silence stretch" / "Say what you mean, Frank"
- "Hand him the file" / "Reach past him for the file" / "Wait for him to hand it to you"
- "Good night, Mr. Harmon" / "Good night, Frank" / "Don't say anything — just look"

The escalation is in what's NOT said. Choices about whether to acknowledge the tension or maintain professional distance. Frank's scenes should have long pauses, loaded silences, and physical proximity that's technically innocent.

### Activities (4)

1. **Bookkeeping** — Type: Chain. Location: Frank's Office. Time: 12:00-15:00 (scheduled days). Energy: 20. Money: +$25.
   Lily does the books. Intelligence stat affects her competence — higher intelligence = she notices the financial discrepancy earlier, she catches errors Frank missed, she impresses him with analysis. At intelligence ≥ 30, she discovers Frank's debt (story trigger). The room has one desk, two chairs. Proximity is unavoidable. Door closed (frank_trust ≥ 16) or open (below).

   Reliability tracked: each completed bookkeeping session increments bookkeeping_on_time counter. Missing a scheduled session resets it.

2. **Cooking Dinner** — Type: Scene. Location: Kitchen. Time: 17:00-19:00. Energy: 20.
   Shared domestic task. The kitchen is small — they move around each other, reaching past, handing things, the choreography of two people in a tight space. Frank talks about Diana's recipes. His voice softens. The scene flows as narrative with 1-2 embedded choices about whether to acknowledge the intimacy of the moment or keep it domestic.

   UNIQUE: Other NPCs can be present. If Ryan walks through (30% random), certain choices unavailable. If Jake is at the table studying, the scene gains a "being watched" dimension.

3. **Late-Night Kitchen** — Type: Chain. Location: Kitchen. Time: 23:00-01:00. Energy: 10.
   NOT always available. Frank is only here 50% of nights (trigger_mode = "random", chance = 0.5). The unpredictability IS the mechanic — the player can't plan for it, which makes each encounter feel charged and accidental. Whiskey, dim light, both of them up when everyone else sleeps. Frank's most vulnerable setting.

   Escalation: frank_trust gates how honest the conversation gets. At trust ≥ 22, he tells her about the debt. At trust ≥ 26, he admits he looks forward to her being up. At trust ≥ 28: "Stay."

4. **Workshop Help** — Type: Task. Location: Workshop. Time: 07:00-09:00 or 14:00-16:00. Energy: 25.
   Physical labor alongside Frank. Trust-building through competence, not charm. She helps with the business — sorting, filing, cleaning tools. Frank teaches her things. The activity builds frank_trust steadily (+2 per visit) but love growth is minimal (+0-1). This is the slow, steady, reliable path.

   UNIQUE: Ryan is sometimes here too (job site overlap). If Ryan present, Frank's dialogue changes — more formal, more "Mr. Harmon" energy. Ryan notices if Lily is more comfortable with Frank than she should be.

### Refusal Triggers

| Trigger | Behavior | Duration | Recovery |
|---------|----------|----------|----------|
| frank_trust < milestone threshold | Pure professional mode. "Let's focus on the numbers." Office door stays OPEN. Calls her "Lily" in a way that's pointedly not intimate. | Until threshold met | Show up consistently. Do good work. Don't push. |
| Line crossed prematurely (physical without trust) | SEVERE. "Miss Chen." Bookkeeping cancelled for the week. Eats dinner in workshop. Zero eye contact. | 3-5 days | The LONGEST withdrawal. Recovery requires Lily being reliable in other ways — paying food money, following house rules, being helpful without seeking him out. |
| Discovers drawings/Ryan involvement (flag: frank_saw_evidence) | Cold but not absent. Still does dinner, still does bookkeeping. But every interaction is formal. Subtext: "I trusted you and you've been..." | 4-5 days | Keep showing up. Don't apologize — Frank doesn't want words. He wants consistency. When he thaws: "Sit down." Two words. The opening. |
| Post-crisis (brothers_discover) | Formal household management mode. Emergency family meeting. Practical, controlled. But late at night, alone in the kitchen: devastated. | 5-7 days | Longest recovery in the game. Requires multiple reliability demonstrations AND a vulnerability moment from Lily (admission, honesty, tears). |

### Preferences (What Earns vs Costs)

| Action | Effect | Why |
|--------|--------|-----|
| Show up on time consistently | frank_trust +2 per streak | Reliability IS love language for Frank |
| Demonstrate competence (bookkeeping, analysis) | frank_trust +2, frank_love +1 | He respects capability |
| Keep his financial secret | frank_trust +5 (one-time) | The biggest trust test |
| Be patient during his withdrawal | frank_love +2 (after recovery) | He notices she didn't push |
| Pay food money on time | frank_trust +2 | Pulling her weight |
| Push physically when trust is low | frank_trust -3, frank_love -1 | SEVERE cost. He withdraws hard. |
| Be childish or dramatic | frank_trust -2 | He values maturity |
| Challenge his authority publicly | frank_love -2 | Not in front of the boys |
| Challenge his authority privately | frank_love +1, frank_trust +1 | He respects someone who stands their ground when it's just them |
| Help in workshop without being asked | frank_trust +3 | She showed up. She didn't have to. |

---

## 3D. Cross-NPC Awareness Rules

### What Each NPC Notices

**Jake (hears through the shared wall):**
| What He Hears | Flag Set | Behavioral Change |
|---------------|----------|-------------------|
| Lily laughing with Ryan late at night | jake_heard_ryan_laugh | Quieter next day. Drawing has sharper lines. |
| Sounds from Lily's room + Ryan's voice | jake_heard_ryan | Withdrawal for 2-3 days. Draws landscapes. Won't initiate wall knocking. |
| Lily's door opening/closing at 2 AM | jake_heard_late_movement | Watches her at breakfast. Doesn't ask. But he KNOWS. |
| Silence (she didn't knock back for 3+ nights) | jake_lonely | Knock gets quieter. 5 nights silence = stops knocking. |

**Ryan (sees physical evidence):**
| What He Sees | Flag Set | Behavioral Change |
|--------------|----------|-------------------|
| Lily leaving Jake's room flushed | ryan_saw_jake | Pointed comments at dinner. "Art class running late?" Competitive energy increase. |
| Lily in Frank's office with door closed | ryan_saw_frank_office | Quieter about it. But watches Frank differently. "Dad's working late again." |
| Charcoal on Lily's clothes/hands | ryan_noticed_art | Mentions it casually. "You and Jake sure spend a lot of time in there." |
| Lily wearing Ryan's hoodie around the house | jake sees this → jake_saw_hoodie | Jake jealousy trigger. Not Ryan's flag — it's what Jake sees. |

**Frank (observes patterns):**
| What He Notices | Flag Set | Behavioral Change |
|-----------------|----------|-------------------|
| Lily's schedule shifting toward Jake | frank_noticed_jake_time | Mentions at bookkeeping. "You've been spending time with Jake." Measuring, not angry. |
| Money spent on art supplies ($60) | frank_noticed_spending | Comments during books. "Sixty dollars on charcoal. That's generous." |
| Lily coming home late from truck rides | frank_noticed_ryan_rides | Tightens house rules. "Dinner is at six. Everyone." |
| Jake's drawings improving (drawing_3_complete +) | frank_found_drawings (story beat) | MAJOR cross-NPC trigger. See Story Arc Section 6. |

### How Awareness Affects Activity Content

When a cross-NPC flag is set, it modifies the content of future activities using group blocks:

**Example: Drawing session after jake_heard_ryan**
```
Normal version: Jake draws with relaxed focus. Conversation flows.
jake_heard_ryan version: Jake draws with tight, sharp strokes.
  Conversation is strained. He asks "Were you up late last night?"
  without looking up. His hand is shaking slightly.
```

**Example: Truck ride after ryan_saw_jake**
```
Normal version: Ryan banters, music loud, relaxed.
ryan_saw_jake version: Ryan drives faster. Music off.
  "So you and Jake been hanging out a lot." It's not a question.
  The dare mechanic this session: "Tell me the truth about you
  and my brother."
```

These variants use group blocks with flag conditions. The base content plays if no awareness flag is set. Awareness variants play when the flag exists.

---

# Section 4: Activity Map

Format per activity: Type, Location, NPC, Schedule, Energy, Money, Unlock, Unique Mechanic, Nodes.

---

## 4A. Jake Activities

### Drawing Session

**Type:** Chain | **Location:** Jake's Room | **NPC:** Jake | **Time:** 14:00-17:00 daily | **Energy:** 15 | **Money:** +$30-80 (if modeling)

**Unlock:** None (available from Day 1)

**Unique Mechanic:** Sketchbook Progress — each visit advances the current drawing. Drawing completion triggers milestone moments. Beauty stat affects progress speed.

**Nodes:**

```
NODE: base
  Content: Jake's room. Afternoon light. He's set up.
  Group variant: [if jake_heard_ryan] Sharper lines. He doesn't look up. Tension in his jaw.
  Group variant: [if jake_saw_hoodie] "Is that Ryan's?" He doesn't say it. You see it in his eyes.
  Choices:
    → "Sit down" → node: session
    → "I'll come back later" → trigger (time +15, jake_love +0)

NODE: session
  Content: Drawing progresses. His hand moves with certainty.
  [Drawing progress increments here based on beauty check]
  Group variant: [drawing_1 in progress] He's sketching her hands. "Hold still — the light on your knuckles."
  Group variant: [drawing_2 in progress] Portrait. "Turn your head slightly. There."
  Group variant: [drawing_3 in progress] Full figure. "Can you stand near the window?"
  Group variant: [drawing_4 in progress] Semi-clothed. "The strap is casting a shadow..."
  Group variant: [drawing_5 in progress] Nude. "Don't move. This is... you're perfect."
  Choices:
    → "Ask about what he's drawing" → trigger (time +120, jake_love +2, jake_trust +1)
    → "Adjust your pose to help" → trigger (time +120, jake_love +3, beauty ≥ current_drawing_req)
    → [if drawing_3+] "Suggest a different pose" → node: posing_choice
    → [if flirt_unlock, corruption ≥ 50] "Hold the pose but watch his eyes" → node: flirt_moment

NODE: posing_choice (drawing_3+)
  Content: She suggests something. His pencil stops.
  Choices:
    → "Something more relaxed" → trigger (time +120, jake_love +2, corruption +1)
      Keeps current drawing subject. Safe.
    → "Something more... natural" → trigger (time +120, jake_love +2, jake_corruption +2, corruption +2)
      Pushes drawing toward next tier subject. Risk.
    → [if corruption ≥ 100, jake_love ≥ 20] "Lower the strap" → node: intimate_posing
      Direct escalation. Opens modeling income.

NODE: flirt_moment (flirt_unlock + corruption ≥ 50)
  Content: She watches him watching her. Neither blinks.
  Group variant: [chose_tender_jake] He blushes. Sets down the pencil. "You're making it hard to concentrate."
  Group variant: [chose_possessive_jake] His eyes narrow. The pencil doesn't stop. "Don't move."
  Choices:
    → "Sorry. I'll hold still." → trigger (time +120, jake_love +2, jake_trust +1)
    → [if tease_unlock, corruption ≥ 70] "What if I don't hold still?" → node: tease_scene
    → [if kiss_unlock, jake_love ≥ 18] "Come here" → node: kiss_scene

NODE: intimate_posing (corruption ≥ 100, jake_love ≥ 20)
  Content: She adjusts. His breath catches. The pencil trembles.
  Choices:
    → "This okay?" → trigger (time +120, jake_love +3, jake_trust +2, corruption +2, money +$30)
      Clothed modeling. Income. Trust builds.
    → [if tease_unlock, corruption ≥ 130] "Less than this?" → node: revealing_pose
      → leads to semi-clothed / nude modeling chain ($50-80)
    → "Actually, let's keep it simple" → trigger (time +120, jake_love +1)

NODE: tease_scene → NODE: kiss_scene → NODE: escalation_chain
  [Standard physical escalation nodes gated by unlock flags + corruption + jake_love]
  Each node: one choice to continue deeper, one choice to stop with current-tier stats.
  loop_terminal = true on final escalation tier reached.

CROSS-NPC EFFECTS:
  - Drawing completion flags (drawing_1_complete through drawing_5_complete) are visible to Frank
  - If frank_trust ≥ 16 AND drawing_3_complete: triggers story beat "frank_finds_drawings"
  - If Ryan passes Jake's room and door is open: ryan_noticed_art flag possible (random 15%)
```

### Library Studying

**Type:** Chain | **Location:** Library | **NPC:** Jake | **Time:** 13:00-16:00 (Mon-Fri) | **Energy:** 15 | **Money:** $0

**Unlock:** town_access flag (bus pass or ride)

**Unique Mechanic:** Art + intellect crossover. Intelligence stat affects conversation depth. This is Jake's TRUST-building activity (more trust than love).

```
NODE: base
  Content: Library basement. Jake at a study carrel. Books spread open.
  Choices:
    → "Sit next to him" → node: studying
    → "Study on your own" → trigger (time +120, intelligence +1)

NODE: studying
  Content: Side by side. Textbooks and sketchbooks. He explains composition theory.
  [intelligence ≥ 20: she contributes meaningfully to the discussion]
  [intelligence < 20: she listens, he teaches]
  Choices:
    → "Ask about his portfolio plans" → trigger (time +120, jake_trust +3, jake_love +1)
    → "Help him with art history essay" [if intelligence ≥ 25] → trigger (time +120, jake_trust +3, intelligence +1)
    → [if jake_love ≥ 12] "Close the textbook" → node: personal
    → "Keep studying quietly" → trigger (time +120, jake_trust +1, intelligence +2)

NODE: personal (jake_love ≥ 12)
  Content: Textbooks closed. Real conversation. He talks about feeling invisible in the family.
  Choices:
    → "Tell him about your divorce" → trigger (time +120, jake_love +3, jake_trust +3)
      Mutual vulnerability. Highest stat gain. Costs: she reveals something real.
    → "Tell him he's not invisible to you" → trigger (time +120, jake_love +4, jake_corruption +1)
      Romantic lean. Love over trust.
    → [if flirt_unlock, corruption ≥ 60] "Touch his hand under the desk" → node: library_flirt
      Semi-public. Risky. The carrel divider is thin.

NODE: library_flirt → escalation (limited — public location caps at kiss)
  Library escalation stops at kissing. No further physical in public space.
  [if kiss_unlock, jake_love ≥ 18] Kiss scene under the carrel divider.
  Then: "Not here." → exit. (The restraint IS the tension.)
```

### Creek Swimming (Contemplative)

**Type:** Scene | **Location:** Creek | **NPC:** Jake | **Time:** 15:00-17:00 | **Energy:** 30 | **Money:** $0

**Unlock:** first_swim flag (from story beat)

**Unique Mechanic:** Being WATCHED by someone who sees beauty, not lust. Jake sketches while she swims. The exposure is artistic, not sexual. Fitness gates swimming depth.

```
NODE: base
  Content: Creek. Smooth rocks. Jake sits on the bank with his sketchbook.
  Choices:
    → "Wade in" → node: swimming
    → "Sit with him on the bank" → trigger (time +90, jake_love +1, jake_trust +1)

NODE: swimming
  Content: She wades. Water mid-thigh. He draws. The pencil moves differently when she's in the water.
  [if fitness ≥ 25] She can swim to the deeper section.
  [if beauty ≥ 35] Jake's drawing is particularly good today. (Drawing progress bonus)
  Choices:
    → "Swim to the deeper part" [fitness ≥ 25] → trigger (time +120, fitness +2, jake_love +2, corruption +2)
      More exposed. He draws faster.
    → "Float on your back" → trigger (time +120, jake_love +2, corruption +1)
      Peaceful. He draws the reflection.
    → [if tease_unlock, corruption ≥ 80] "Ask him to come in" → node: both_swimming
      Escalation. Bodies in water. Different from Ryan's competitive version — this is quiet, close.

NODE: both_swimming → limited escalation chain (kiss max in water, higher on bank)
```

### Wall Knocking

**Type:** Chain | **Location:** Lily's Room | **NPC:** Jake | **Time:** 22:00-00:00 daily | **Energy:** 10 | **Money:** $0

**Unlock:** first_morning flag (Day 1+)

**Unique Mechanic:** Consequence-laden nightly ritual. Silence has COST. The wall is a barrier and a bridge.

```
NODE: base
  Content: Night. Through the wall: tap-tap.
  [if jake_lonely (5 nights no knock-back)] No tap tonight. Silence.
    → "Go to his room" → node: restart_ritual (jake_love +2, clears jake_lonely)
    → "Sleep" → trigger (time +60, nothing)
  [if jake_heard_ryan] The tap is softer tonight. Hesitant.
  [normal] The familiar rhythm. Tap-tap.
  Choices:
    → "Knock back" → node: talking
    → "Open his door" [jake_love ≥ 12] → node: his_room
    → "Silence" → trigger (time +30, jake_love -1 next day)
      COSTS: Not answering hurts. 3 consecutive silences = jake_lonely flag.

NODE: talking
  Content: Through the wall. Whispered.
  "You up?" / "Can't sleep." / "Draw anything today?"
  The conversation is limited by the wall. Intimate because of the barrier.
  Choices:
    → "Tell him about your day" → trigger (time +60, jake_love +2)
    → "Ask what he's drawing" → trigger (time +60, jake_trust +2)
    → [if jake_love ≥ 15] "I wish this wall wasn't here" → trigger (time +60, jake_love +3, corruption +1)
    → "Good night" → trigger (time +30, jake_love +1)

NODE: his_room (jake_love ≥ 12)
  Content: She opens his door. He looks up from the sketchbook.
  The room smells like graphite and clean laundry.
  → Leads to deeper conversation chain, then physical escalation chain (gated normally)
  → CROSS-NPC RISK: Frank's late-night kitchen check (random 10%).
    If frank_up_late AND lily_in_jakes_room: frank_noticed_late_movement flag set.
```

### Park Sketching

**Type:** Scene | **Location:** Park | **NPC:** Jake | **Time:** 10:00-13:00 (weekends) | **Energy:** 15 | **Money:** $0

**Unlock:** town_access

**Unique Mechanic:** PUBLIC. No escalation beyond sitting close. Pure trust-building in a safe environment. The ONLY Jake activity that can't go physical.

```
NODE: base
  Content: Park bench. Jake's sketching the pond. Sunlight through trees.
  Choices:
    → "Sit next to him and watch" → trigger (time +120, jake_love +1, jake_trust +2)
    → "Bring your own sketchbook" [if has_art_supplies] → trigger (time +120, jake_love +2, jake_trust +2, beauty +1)
      Shared creative time. Highest trust gain. Requires art supply investment.
    → "Ask to see his work" → trigger (time +90, jake_love +2)
    → [if jake_love ≥ 15] "Lean against his shoulder" → trigger (time +120, jake_love +3, corruption +1)
      Maximum intimacy available here. Public = safe limit.
```

---

## 4B. Ryan Activities

### Truck Ride

**Type:** Chain | **Location:** Ryan's Truck | **NPC:** Ryan | **Time:** 09:00-11:00 or 15:00-17:00 | **Energy:** 10 | **Money:** $0 (-$10 if gas money)

**Unlock:** None (Ryan offers from Day 2)

**Unique Mechanic:** DESTINATION MATTERS. Where they go determines what content is available. Different destinations = different conversation topics and challenge types.

```
NODE: base
  Content: Ryan at the truck. Engine running. "Get in."
  Group variant: [ryan_saw_jake] "You coming or what?" Shorter. Edge in his voice.
  Group variant: [ryan_allowed] His eyes scan her outfit. The grin. "Nice."
  Group variant: [ryan_resisted] More careful. Hands on the wheel. Music louder.
  Choices:
    → "Where are we going?" → node: destination_pick
    → "Not today" → trigger (time +15)
    → [if gave_gas_money] (auto-noted: ryan remembers)

NODE: destination_pick
  Choices:
    → "Town run" → node: ride_town (casual, trust-building)
    → "Job site" [if min_day ≥ 3] → node: ride_jobsite (work, fitness)
    → "Creek" [if ryan_trust ≥ 8] → node: ride_creek (isolated, escalation)
    → "Just drive" [if ryan_trust ≥ 12] → node: ride_nowhere (vulnerability)
    → "Trail head" [weekends, if fitness ≥ 25] → node: ride_trail (adventure, challenge)

NODE: ride_town
  Content: Windows down. Music loud. He talks about people in town.
  Challenge: "Bet you can't name three songs on this station."
  Choices:
    → Accept challenge → [win: ryan_trust +2] [lose: ryan_corruption +1]
    → "Just drive, show-off" → trigger (time +60, ryan_love +1)
    → [if confidence ≥ 20] "Raise: if I win, you buy me coffee" → [win: ryan_trust +3, ryan_love +1] [lose: ryan_corruption +2]

NODE: ride_creek (ryan_trust ≥ 8)
  Content: He takes the back roads. No music now. Trees close in.
  Parked by the water. Engine off. Just the creek and the radio static.
  Challenge: "Truth or dare?"
  Choices:
    → "Truth" → he asks something personal. Answer honestly = ryan_trust +3. Deflect = ryan_trust +0.
    → "Dare" → physical dare (fitness gated). Complete = ryan_trust +2, corruption +2. Fail = corruption +1.
    → [if confidence ≥ 25] "Both" → raise stakes. Highest payout. Both truth AND dare.
    → [if kiss_unlock, ryan_love ≥ 15] "Neither. Come here." → node: truck_kiss_chain

NODE: ride_nowhere (ryan_trust ≥ 12)
  Content: No destination. He drives slow. Something's on his mind.
  This is Ryan's VULNERABILITY mechanic. He only opens up on drives to nowhere.
  Choices:
    → "What's wrong?" → [ryan_trust ≥ 18] he tells real story. ryan_trust +4, ryan_love +2.
      [ryan_trust < 18] "Nothing. Forget it." ryan_trust +0.
    → "You don't have to talk" → trigger (time +90, ryan_trust +2, ryan_love +1)
      Patience. He notices she didn't push.
    → [if ryan_trust ≥ 22] silence → he talks anyway. Biggest vulnerability moment.
      ryan_trust +5, ryan_love +3. "I don't want to go home yet."

NODE: ride_trail (weekend, fitness ≥ 25)
  Content: Trail head. He's got hiking boots. "Think you can keep up?"
  Full hike chain: challenge-based (pace matching, trail decisions).
  → Leads to Trail Head / Rest Stop / Isolated Creek locations with Ryan-specific content.

CROSS-NPC EFFECTS:
  - If Jake is home when Lily leaves with Ryan: jake_noticed_ryan_ride (if jake_love ≥ 10)
  - If Frank sees them leave: frank_noticed_ryan_rides flag after 3+ rides in one week
```

### Gym Workout

**Type:** Chain + Task | **Location:** Gym | **NPC:** Ryan | **Time:** 07:00-09:00 or 16:00-18:00 | **Energy:** 30 | **Money:** $0

**Unlock:** has_gym_membership flag ($30/month) + town_access

**Unique Mechanic:** Performance-based. Fitness stat gates which exercises they can do together. Higher fitness = more intense workouts = more respect = deeper content. The TASK gives fitness. The CHAIN gives relationship.

```
NODE: base
  Content: Gym. Free weights. Ryan is already at the bench press.
  [if fitness < 25] He looks at her. "You sure about this?"
  [if fitness ≥ 35] He nods. Respect already in his eyes.
  Choices:
    → "Warm up on the treadmill" → trigger (time +120, fitness +2)
      Solo. No Ryan interaction. Safe fitness gain.
    → "Work out near him" → node: workout
    → [if fitness ≥ 30] "Spot me" → node: spotting (trust-building)

NODE: workout
  Content: Side by side. He demonstrates form. His hands adjust her stance.
  Challenge: "Match my set. Ten reps."
  [if fitness ≥ 30] She can match. [if fitness < 30] She struggles.
  Choices:
    → Match his set → [win at fitness ≥ 30: ryan_trust +3, fitness +3]
                       [lose at fitness < 30: ryan_corruption +1, fitness +2]
    → "Add five more" [confidence ≥ 20] → raise stakes
      [win: ryan_trust +4, ryan_love +1, fitness +3]
      [lose: ryan_corruption +2, fitness +2, ryan_love +1 (tried hard)]
    → "I need a break" → trigger (time +120, fitness +2, ryan_trust +0)
      No judgment, but no progress either.

NODE: spotting (fitness ≥ 30)
  Content: She spots him. He spots her. Physical proximity is functional, necessary.
  Hands near each other's bodies. Professional. Charged.
  Choices:
    → "Focus on form" → trigger (time +120, ryan_trust +2, fitness +3)
    → [if flirt_unlock, corruption ≥ 60] "Hold longer than necessary" → node: gym_flirt
    → [if tease_unlock, corruption ≥ 90] "Stretch together after" → node: gym_stretch
      → Leads to locker room hallway chain (escalation, risk of being seen)

NODE: gym_flirt → gym_stretch → hallway → escalation_chain
  Gym escalation path: spotting → stretching → locker hallway proximity
  Public setting caps escalation at tease/groping. Full escalation requires truck or creek.
  UNIQUE: "Shared locker hallway" — not co-ed but the hallway between is narrow.

CROSS-NPC: None directly (gym is in town, away from house)
```

### TV Couch

**Type:** Hangout | **Location:** Living Room | **NPC:** Ryan | **Time:** 19:00-22:00 | **Energy:** 15 | **Money:** $0

**Unlock:** None (available from Day 1)

**Unique Mechanic:** Hub menu that GROWS with relationship. Frank can walk through (30% chance) — modifies available choices and adds dare dimension.

```
NODE: base (hub)
  Content: Living room. TV on. Ryan takes one end of the couch.
  The cushion between them is either a buffer or a bridge.
  [RANDOM 30%: Frank walks through → frank_present flag for this session]
  Choices:
    → "Watch the show together" → trigger (time +90, ryan_love +1)
    → "Comment on the show" → trigger (time +90, ryan_love +1, ryan_trust +1)
    → [if ryan_love ≥ 8] "Remove the cushion" → node: close
    → [if flirt_unlock, corruption ≥ 50] "Lean into him" → node: lean
    → [if frank_present AND ryan_trust ≥ 12] "Play footsie while Frank's here" → node: dare_frank
      Ryan's DARE mechanic. Doing something forbidden with Frank in the room.
      ryan_trust +3, ryan_corruption +2, corruption +3. High risk, high reward.

NODE: close (ryan_love ≥ 8)
  Content: Cushion gone. Their legs almost touching.
  [if frank_present] He glances toward the hallway. The dare is unspoken.
  Choices:
    → "Let your knee touch his" → trigger (time +90, ryan_love +2, corruption +1)
    → [if kiss_unlock, ryan_love ≥ 15] "Kiss him" → node: couch_kiss
      [if frank_present] "Kiss him — with Frank right there" → node: couch_kiss (corruption +4 bonus)
    → "Just sit close" → trigger (time +90, ryan_love +1)

NODE: lean → couch_kiss → escalation under blanket (corruption ≥ 100+)
  Couch escalation: lean → kiss → blanket → handjob under blanket (house risk)
  UNIQUE RISK: Any escalation beyond kissing has 15% chance of interruption
    → interrupted: frank_saw_couch flag. Ryan plays it off. Frank says nothing. Tension.

NODE: dare_frank (frank_present, ryan_trust ≥ 12)
  Content: Ryan's eyes. The dare. Frank is reading the paper three feet away.
  Choices:
    → "Touch his thigh under the blanket" → trigger (time +90, ryan_trust +3, corruption +3)
    → "Hold his hand behind the cushion" → trigger (time +90, ryan_love +3, corruption +2)
    → "Too risky" → trigger (time +90, ryan_trust -1)
      He's disappointed. She backed down from the dare.
```

### Job Site

**Type:** Task | **Location:** Workshop | **NPC:** Ryan | **Time:** 09:00-12:00 | **Energy:** 25 | **Money:** +$40

**Unlock:** min_day ≥ 3

**Unique Mechanic:** Earns money AND fitness. One moment mid-task with a choice. Ryan present as coworker, not romantic interest — but proximity and physical labor create moments.

```
NODE: base
  Content: Workshop. Sawdust and motor oil. Ryan puts her to work.
  Choices:
    → "Get to work" → node: working
    → "Not today" → trigger (time +15)

NODE: working
  Content: Sorting nails, holding boards, sweeping sawdust. Physical.
  Mid-task moment: a heavy board needs moving.
  Choices:
    → "Help him lift it" [fitness ≥ 20] → trigger (time +180, money +$40, fitness +1, ryan_trust +2)
      Physical competence. He respects her for it.
    → "Solve the measurement problem" [intelligence ≥ 20] → trigger (time +180, money +$40, intelligence +1, ryan_trust +1, ryan_love +1)
      Mental competence. Surprises him.
    → "Keep sweeping" → trigger (time +180, money +$40, ryan_trust +1)
      Safe. Gets paid. Minimal relationship gain.

  [if ryan_trust ≥ 15, fitness ≥ 30] BONUS moment:
    → "Race him to finish stacking" → Challenge mechanic activates
      [win: ryan_trust +3, fitness +1] [lose: ryan_corruption +1]

CROSS-NPC:
  - Frank sometimes present (he owns the workshop). If frank_present: more professional behavior.
  - If frank_present AND ryan_trust ≥ 15: Ryan's body language changes. More careful. But his hand brushes hers passing a tool.
```

### Creek Swimming (Competitive)

**Type:** Chain | **Location:** Creek | **NPC:** Ryan | **Time:** 15:00-17:00 | **Energy:** 30 | **Money:** $0

**Unlock:** first_swim flag + fitness ≥ 25

**Unique Mechanic:** DIFFERENT from Jake's contemplative creek. This is physical, competitive. Racing, splashing, challenges. Fitness gates access and performance.

```
NODE: base
  Content: Creek. Ryan strips his shirt. "Last one in's a coward."
  Choices:
    → "Race him to the water" → node: racing
    → "Walk in at your own pace" → trigger (time +120, ryan_love +1, fitness +2)
    → [if confidence ≥ 25] "Push him in first" → node: splash_war (ryan_trust +2, instant challenge)

NODE: racing
  Content: Running. Water hitting skin. He's faster but she's more agile.
  Challenge: first to the rock.
  [fitness ≥ 35: she can win] [fitness < 35: she loses but tries]
  Choices:
    → Race all out → [win: ryan_trust +3, fitness +2] [lose: ryan_corruption +1, fitness +2]
    → "Raise: loser tells a secret" → [win: ryan_trust +4, he tells a truth]
                                       [lose: she tells a truth, ryan_love +2]
    → "Let him win" → trigger (ryan_trust -1)
      He KNOWS she let him win. He hates that.

NODE: splash_war → underwater challenge → dare chain
  Escalation: splash → hold breath challenge → underwater proximity
  [if tease_unlock, corruption ≥ 90] "Skinny dipping dare"
    Ryan: "You first." She goes first. He watches. Then joins.
    → Highest corruption gain. Bodies in water. No barrier.
  → Leads to physical escalation on the bank (gated by unlock flags + stats)

CROSS-NPC:
  - Creek is 15-minute walk from house. Jake can see them leave from his window.
    If jake_love ≥ 15: jake_saw_creek_together flag. Quiet hurt.
  - Creek time overlaps with Jake's contemplative creek time. THEY CAN'T BOTH HAPPEN.
    If Jake and Ryan both available at creek: player must choose which NPC (Motivation 1).
```

---

## 4C. Frank Activities

### Bookkeeping

**Type:** Chain | **Location:** Frank's Office | **NPC:** Frank | **Time:** 12:00-15:00 (Mon/Wed/Fri) | **Energy:** 20 | **Money:** +$25

**Unlock:** chores_started flag + corruption ≥ 40 + intelligence ≥ 20

**Unique Mechanic:** Intelligence-gated depth. Higher intelligence = she catches errors, finds the debt earlier, impresses Frank. Door open/closed based on frank_trust. Reliability flag tracking (bookkeeping_on_time counter).

```
NODE: base
  Content: Frank's office. Invoices, receipts, the amber desk lamp.
  [if frank_trust < 16] Door stays open. He checks her work.
  [if frank_trust ≥ 16] Door closes. "We can focus better this way."
  [if frank_withdrawal] "I can handle it myself this week." → Activity unavailable.
  Choices:
    → "Start the books" → node: working
    → "I can come back later" → trigger (time +15)
      COST: Breaks bookkeeping_on_time streak. Counter resets.

NODE: working
  Content: Numbers. The scratch of pencil on ledger paper. His chair across the desk.
  [intelligence ≥ 25] She spots a discrepancy in the receivables. Frank notices.
  [intelligence ≥ 30 AND frank_trust ≥ 16] She finds the REAL numbers. Story beat trigger.
  Sets: bookkeeping_on_time_X flag (increments)
  Choices:
    → "Finish the books efficiently" → trigger (time +120, money +$25, frank_trust +2, intelligence +1)
      Professional. Reliable. The Trust Ledger path.
    → "Ask about the client who's late" → trigger (time +120, money +$25, frank_trust +2, frank_love +1)
      Personal interest in his work. He notices.
    → [if frank_love ≥ 12, corruption ≥ 70] "Let the silence stretch" → node: charged_silence
      Don't fill the quiet. Let it build. This is where Frank starts to crack.

NODE: charged_silence (frank_love ≥ 12, corruption ≥ 70)
  Content: She stops writing. Looks at him. He looks at the desk.
  The clock ticks. Neither speaks.
  [if frank_trust ≥ 20] He looks up. Holds eye contact. Something shifts.
  Choices:
    → "Say what you mean, Frank" → trigger (time +120, money +$25, frank_love +3, frank_trust +1, corruption +2)
      Direct. Forces him to acknowledge the tension.
    → "Hand him the file" → trigger (time +120, money +$25, frank_trust +2)
      Break the tension professionally. He's grateful. And disappointed.
    → [if kiss_unlock, frank_love ≥ 20, frank_trust ≥ 20] "Reach past him for the ledger" → node: office_proximity
      Her arm crosses his space. Their faces close. The excuse is the ledger.
      → Leads to office escalation chain (under-desk, locked-door intimacy)

CROSS-NPC:
  - Ryan knows when bookkeeping happens. If ryan_saw_frank_office AND ryan_trust ≥ 10:
    Ryan makes comments. "You and Dad sure like your private meetings."
  - Intelligence gains here help with Jake's art theory discussions too.
```

### Cooking Dinner

**Type:** Scene | **Location:** Kitchen | **NPC:** Frank | **Time:** 17:00-19:00 | **Energy:** 20 | **Money:** $0 (or -$40 if cooked_for_house flag)

**Unlock:** min_day ≥ 5

**Unique Mechanic:** Kitchen choreography. Two people in a small space. Reaching past, handing things, the rhythm of shared domestic work. Other NPCs can appear (group dynamic).

```
NODE: base
  Content: Kitchen. Frank at the stove. Sleeves rolled. He nods at the cutting board.
  [if cooked_for_house flag] He noticed she bought groceries. "You didn't have to do that."
    frank_love +2 bonus on first cooking session after buying groceries.
  Choices:
    → "Pick up the knife" → node: cooking
    → "Set the table instead" → trigger (time +90, frank_trust +1)
      Helping without getting close. Safe distance.

NODE: cooking
  Content: Side by side. Chopping, stirring, reaching past each other.
  He talks about Diana's recipes. His voice changes when he says her name.
  [RANDOM 30%: Ryan walks through → comments. "Smells good." Watches them.]
  [RANDOM 20%: Jake at the table studying → different dynamic, being observed]
  Choices:
    → "Ask about Diana" → trigger (time +120, frank_love +3)
      He appreciates the interest. But it costs — reminds him what he's risking.
    → "Focus on the food" → trigger (time +120, frank_trust +2)
      Professional. The safe choice. But safe isn't what cracks Frank.
    → [if frank_love ≥ 12, corruption ≥ 60] "Reach past him for the skillet" → node: kitchen_proximity
      Their bodies close. The excuse is the skillet. It's never the skillet.
      [if NPC_present] Extra risky. Corruption +2 bonus if someone is watching.

NODE: kitchen_proximity (frank_love ≥ 12, corruption ≥ 60)
  Content: Her arm brushes his. Neither moves.
  [if frank_trust ≥ 18] He doesn't pull away. First time.
  [if frank_trust < 18] He steps back. "Dinner's almost ready." Withdrawal behavior.
  Choices:
    → "Stay close" → trigger (time +120, frank_love +2, corruption +2)
    → "Step back yourself" → trigger (time +120, frank_trust +1)
      She respects his space. He notices. He's grateful. And he hates being grateful.
    → [if kiss_unlock, frank_love ≥ 20, NO NPC present] "Don't move" → node: kitchen_kiss
      Only possible when they're alone. The kiss is fast, guilty, devastating.
      → Stops here. Kitchen is too public for further escalation.

CROSS-NPC:
  - Cooking regularly builds frank_love steadily. Jake and Ryan notice:
    "You've been cooking with Dad a lot." (ryan_noticed_cooking flag after 5+ sessions)
  - If Jake is present AND jake_love ≥ 15: he watches them together.
    What he sees depends on what choices Lily made. If proximity: jake_noticed_frank_close.
```

### Late-Night Kitchen

**Type:** Chain | **Location:** Kitchen | **NPC:** Frank | **Time:** 23:00-01:00 | **Energy:** 10 | **Money:** $0

**Unlock:** frank_kitchen_moment flag (from story beat) + trigger_mode = "random", chance = 0.5

**Unique Mechanic:** NOT ALWAYS AVAILABLE. Frank is only here 50% of nights. The unpredictability IS the mechanic. Each encounter feels charged and accidental. Whiskey, dim light, the house asleep.

```
NODE: base
  Content: Kitchen. 2 AM. He's at the table. Whiskey. Lamp light.
  He doesn't look surprised to see her. Maybe he was hoping.
  [if frank_trust < 20] "Can't sleep?" Neutral. Safe.
  [if frank_trust ≥ 20] He pours a second glass without asking. Slides it across.
  [if frank_trust ≥ 26] He was waiting. The glass was already poured.
  Choices:
    → "Sit down" → node: talking
    → "Just getting water" → trigger (time +30, frank_love +1)
      She leaves. But he watched her walk to the sink. And back.

NODE: talking
  Content: The kitchen at night is a different country. No rules. No roles.
  Topics unlock by frank_trust:
  [trust < 15] Weather. The house. Small talk. He's being the adult.
  [trust 15-20] The business. Clients. Money. He's being honest.
  [trust 20-25] Diana. The marriage. What he expected vs what he got. Vulnerable.
  [trust ≥ 25] Lily. What she means to this house. What she means to him. Devastating.
  Choices:
    → "Listen" → trigger (time +60, frank_trust +2, frank_love +1)
      Don't talk. Let him fill the silence. He needs to be heard.
    → "Ask the question he's avoiding" → trigger (time +60, frank_love +3, frank_trust +1)
      Push gently. He answers. It costs him.
    → [if frank_love ≥ 20] "Move your chair closer" → node: late_proximity
    → [if frank_love ≥ 26, corruption ≥ 120] "Put your hand on his" → node: late_touch
      The first deliberate touch. Not reaching for a skillet. Not accidental. Intentional.
      This is the line. Once crossed: frank_line_crossed flag.
      → Leads to escalation chain (kitchen table, counter, whiskey-fueled, devastating)

CROSS-NPC:
  - Jake's wall. He can hear her door open at 2 AM. jake_heard_late_movement flag.
  - If lily_in_kitchen_late 3+ times: jake_worried flag. He doesn't know it's Frank. He fears the worst.
```

### Workshop Help

**Type:** Task | **Location:** Workshop | **NPC:** Frank | **Time:** 07:00-09:00 or 14:00-16:00 | **Energy:** 25 | **Money:** $0

**Unlock:** frank_trust ≥ 5

**Unique Mechanic:** Trust-building through competence. No romance — just work. The SLOWEST Frank activity but the most reliable for building trust. Frank teaches; she learns. The relationship is mentor-student, which makes the eventual shift devastating.

```
NODE: base
  Content: Workshop. Sawdust, tool pegboard, the hum of the compressor.
  Frank is building something. He could use an extra pair of hands.
  Choices:
    → "Help without being asked" → node: working (frank_trust +1 bonus for initiative)
      Sets helped_workshop_unprompted flag (first time only — reliability ledger)
    → "Ask what he needs" → node: working

NODE: working
  Content: She hands him tools. Holds boards steady. Follows instructions.
  He teaches: how to measure twice, how to feel the grain, why this joint matters.
  Choices:
    → "Pay attention and learn" → trigger (time +150, frank_trust +2, intelligence +1)
      She's competent. He's surprised. He mentions it once: "Good."
    → "Ask about the project" → trigger (time +150, frank_trust +2, frank_love +1)
      She cares about his work, not just the task.
    → [if frank_trust ≥ 15] "Work in silence together" → trigger (time +150, frank_trust +3)
      Comfortable silence. The highest trust gain. Two people who don't need to fill the air.

CROSS-NPC:
  - Ryan works here too. If Ryan arrives during session: dynamic shifts.
    Frank becomes more "boss" energy. Ryan notices Lily's comfort level with Frank.
    If ryan_trust ≥ 10: "Since when does she work here?" — not angry, measuring.
```

---

## 4D. Solo Activities

### Yoga
**Type:** Solo | **Location:** Lily's Room or Yard | **Time:** 06:00-08:00 | **Energy:** 15 | **Money:** $0
**Effects:** beauty +2, fitness +1 | **No choices.** 2-3 paragraphs. Done.
**Cross-NPC:** If done in yard and Jake's window faces yard: jake notices (beauty investment visible).

### Jogging (Property)
**Type:** Solo | **Location:** Yard | **Time:** 06:00-08:00 or 16:00-18:00 | **Energy:** 15 | **Money:** $0
**Effects:** fitness +1, confidence +1 | **No choices.**
**Cross-NPC:** Frank sees her from workshop window. Ryan sees her if he's outside. Visible investment in self.

### Jogging (Park)
**Type:** Solo | **Location:** Park | **Time:** 10:00-12:00 | **Energy:** 20 | **Money:** $0 (requires town_access)
**Effects:** fitness +2, confidence +1 | **No choices.** Better gains than property. Costs bus fare.

### Campus Classes
**Type:** Solo | **Location:** Campus | **Time:** 09:00-12:00 (Mon/Wed/Fri) | **Energy:** 20 | **Money:** $0 (requires town_access)
**Effects:** intelligence +3 | **No choices.** Best intelligence source. 3x/week. Costs half a day + bus time.

### Journal
**Type:** Solo | **Location:** Lily's Room | **Time:** 22:00-23:00 | **Energy:** 5 | **Money:** $0
**Effects:** intelligence +1, confidence +1 | **No choices.** Quick. Low energy. Good filler before sleep.

### Self-Care / Grooming
**Type:** Solo | **Location:** Bathroom | **Time:** 06:00-07:00 or 21:00-22:00 | **Energy:** 10 | **Money:** $0
**Effects:** beauty +2 | **No choices.** Beauty maintenance to counter decay.
**Cross-NPC:** Shared bathroom. Random encounter chance: someone walks in (lock doesn't work). Corruption +2.

### Stargazing
**Type:** Solo | **Location:** Yard | **Time:** 22:00-00:00 | **Energy:** 5 | **Money:** $0
**Effects:** confidence +1 | **No choices.** Quiet moment. Optional.

---

## 4E. Utility Activities

### Breakfast
**Type:** Hangout | **Location:** Kitchen | **Time:** 07:00-08:30 | **Energy:** 0 (restores +15) | **Money:** $0
**NPC:** All present (random block_pool determines which NPCs speak)
**Choices:**
- "Eat quietly" → trigger (time +60, energy +15)
- "Talk to [NPC]" → trigger (time +60, energy +15, [npc]_love +1)
- [if exposure_unlock, corruption ≥ 50] "Come down in sleep clothes" → trigger (time +60, energy +15, corruption +1, all NPC corruption +1)

### Lunch
**Type:** Solo | **Location:** Kitchen | **Time:** 12:00-13:00 | **Energy:** 0 (restores +20) | **Money:** $0
Simple energy restoration. Brief.

### Dinner
**Type:** Hangout | **Location:** Kitchen | **Time:** 18:00-19:30 | **Energy:** 0 (restores +25) | **Money:** $0
**NPC:** All present (unless someone is in withdrawal)
**Choices:**
- "Eat with everyone" → trigger (time +90, energy +25)
- "Sit next to [NPC]" → trigger (time +90, energy +25, [npc]_love +1)
  [Cross-NPC: other NPCs notice who she sits next to]
- [if NPC in withdrawal] That chair is empty. The absence is loud.

### Sleep
**Type:** Solo | **Location:** Lily's Room | **Time:** 00:00+ | **Energy:** resets to max | **Money:** $0
Advances day. Triggers overnight checks: trait decay, expense due dates, NPC state updates.

### House Cleaning
**Type:** Task | **Location:** Hallway/Kitchen/Bathroom | **Time:** 09:00-12:00 | **Energy:** 25 | **Money:** +$20
**Choices:** None. Do the work, get paid. Available from Day 1. The reliable baseline income.

### Diner Shift
**Type:** Task | **Location:** Diner | **Time:** 17:00-22:00 | **Energy:** 20 | **Money:** +$45 (+ beauty bonus tips)
**Unlock:** confidence ≥ 30, town_access
**Choices:** None. Work the shift. Get paid. BUT: takes the ENTIRE evening slot. Misses dinner, misses all evening NPC activities. The time-money trade-off.
**Beauty bonus:** If beauty ≥ 40: tips +$10. If beauty ≥ 60: tips +$20.

### Shopping
**Type:** Solo | **Location:** Clothing Store | **Time:** 10:00-16:00 | **Energy:** 10 | **Money:** varies
**Unlock:** town_access
Wardrobe purchases. Corruption-gated clothing tiers. Each purchase = money spent, beauty gained, corruption gained.

### Expense Payments
**Type:** Utility | **Location:** Any | **Time:** Any | **Energy:** 0 | **Money:** negative
Triggered automatically when due dates hit. Player chooses to pay or skip.
- Skip bus pass → town_access revoked until paid
- Skip art supplies → Jake's drawing quality affected, campus work suffers
- Skip phone → Mom can't call, miss story beats
- Skip food contribution → frank_trust -3

---

## 4F. Schedule Conflict Examples (Motivation 1: "I Can't Have Everything")

### Afternoon Conflict (14:00-17:00)
Available simultaneously:
- Drawing session with Jake (Jake's Room)
- Bookkeeping with Frank (Office, Mon/Wed/Fri)
- Creek swimming — Jake OR Ryan (only one, same location)
- Campus classes (town, Mon/Wed/Fri)

Player CANNOT do all of these in one afternoon. Choosing Jake means missing Frank's bookkeeping (breaks reliability streak). Choosing campus means missing both NPCs.

### Evening Conflict (17:00-22:00)
Available simultaneously:
- Cooking with Frank (Kitchen, 17:00-19:00)
- Diner shift ($45, 17:00-22:00)
- TV with Ryan (Living Room, 19:00-22:00)

Working at the diner means missing BOTH Frank's cooking AND Ryan's couch time AND dinner with everyone. The money is needed but the relationship cost is real.

### Night Conflict (22:00+)
Available simultaneously:
- Wall knocking with Jake (Lily's Room)
- Late-night kitchen with Frank (50% chance)

If Frank is in the kitchen AND Jake knocks: she must choose. Answer Jake's knock (miss Frank's rare appearance) or go to the kitchen (silence Jake's knock — jake_love -1, jake_lonely counter increments).

### Weekend Conflict
Available simultaneously:
- Hiking with Ryan (Trail Head, requires fitness ≥ 25)
- Park sketching with Jake (Park, 10:00-13:00)
- Shopping in town

Can't hike with Ryan AND sketch with Jake. One NPC gets the weekend. The other notices.

---

# Section 5: Pressure Systems

## 5A. Automatic Recurring Expenses

Expenses fire AUTOMATICALLY on schedule and deduct money. If money < 0, consequences stack.

| Expense | Amount | Schedule | If Unpaid |
|---------|--------|----------|-----------|
| Food contribution | $50 | Weekly (Monday) | frank_trust -3. After 2 weeks unpaid: frank confrontation beat. |
| Rent | $50 | Weekly (Friday) | 1 grace period. Then frank_trust -5. 3 weeks late: eviction threat beat. |
| Bus pass | $80 | Monthly (Day 1, 28, 56) | town_access revoked. Must use Ryan's truck (dependency + corruption). |
| Art supplies | $60 | Monthly (Day 14, 42) | Jake's drawing progress halves. Campus work suffers. 2 weeks: can't attend art class. |
| Phone bill | $45 | Monthly (Day 7, 35) | Phone cut off. Mom can't call. Story beats delayed. |
| Gym membership | $30 | Monthly (optional) | Gym access revoked. Ryan's gym activity locked. Fitness limited to jog/swim. |

**Total monthly minimum:** $585 (food $200 + rent $200 + bus $80 + art $60 + phone $45)
**With gym:** $615/month

**Baseline income (cleaning only):** $400/month
**With mom's transfer (unreliable):** $600/month

**The gap:** Even with mom's money, surplus is $15/month. One bounced transfer or one wardrobe purchase = red. Bookkeeping doesn't unlock until corruption ≥ 40. By the time she has financial relief, she's already compromised.

### What Happens When Money Goes Negative

| Balance | Consequence |
|---------|-------------|
| < $100 | Narration shift: anxiety. "I'm running out of time." |
| < $50 | Financial crisis story beat triggers. |
| < $0 | All unpaid consequences stack. Frank confrontation inevitable. |
| < -$100 | Frank's arrangement offer triggers. "I'll cover everything." |

---

## 5B. Trait Decay Numbers

### Player Stat Decay

| Stat | Decay Rate | Without... | Impact When Low |
|------|-----------|------------|----------------|
| fitness | -1 per 3 days | exercise (gym/jog/swim/hike/job site) | < 25: Ryan's gym locked. < 20: competitive creek locked. |
| beauty | -1 per 2 days | grooming (yoga/self-care/spa) | < 30: Jake's drawing progress slow. < 25: diner tips drop. |
| corruption | No decay | — | Once corrupted, permanent. |
| confidence | No decay | — | Permanent growth. |
| intelligence | No decay | — | Permanent knowledge. |

### NPC Stat Decay

| Stat | Decay Rate | Without... | Impact When Low |
|------|-----------|------------|----------------|
| NPC love | -1 per 5 days | interaction | At 0: NPC treats Lily as stranger. |
| NPC trust | -1 per 7 days | interaction | At 0: professional distance only. |
| NPC corruption | No decay | — | Boundaries stay crossed. |

### The Maintenance Burden

Minimum to prevent all decay:
- Each NPC: 1 visit per 5 days (love), 1 per 7 days (trust) = ~3 NPC visits/5 days
- Fitness: 1 exercise per 3 days
- Beauty: 1 grooming per 2 days
- Work: 2-3 shifts/week for money

Total maintenance: ~11 activities/week out of 28-35 available. Manageable. But leaves only 17-24 slots for DEEPENING — and deepening one NPC means the others get maintenance only, never reaching milestone stats.

---

## 5C. NPC Expectations

### Frank's Expectations
| What He Expects | Frequency | If Unmet |
|----------------|-----------|----------|
| Food money on time | Weekly | frank_trust -3. Stacks. After 2 weeks: confrontation. |
| Show up for bookkeeping | Mon/Wed/Fri | Reliability counter RESETS. frank_trust -1. |
| Follow house rules | Daily | frank_trust -1 per violation. After 3: stricter rules. |
| Respect his space | Always | frank_trust -2, frank_love -1. |

### Ryan's Expectations
| What He Expects | Frequency | If Unmet |
|----------------|-----------|----------|
| Accept rides when offered | ~3x/week | ryan_love -1 per refusal. 3 consecutive: stops offering. |
| Match energy, don't be timid | During activities | ryan_trust -1 per timid choice. |
| Don't lie to him | Always | ryan_trust -3 if caught. Severe. |
| Keep up physically | During challenges | ryan_trust -1 if she quits. |

### Jake's Expectations
| What He Expects | Frequency | If Unmet |
|----------------|-----------|----------|
| Knock back at night | Nightly | jake_love -1. 3 consecutive silences: jake_lonely. 5: stops knocking. |
| Show up for drawing | ~5x/week | jake_love -1 per day missed. Progress halts. |
| Be genuine | During interactions | jake_trust -2 if fake/manipulative. |
| Appreciate his art specifically | During sessions | Generic praise: +0. Specific: +1 bonus. |

---

## 5D. Crisis Events

### Crisis 1: Financial Crisis
**Trigger:** money < $50 AND days_since_flag(mom_called) ≥ 14
**When:** Day ~18-25
**Effects:** financial_crisis flag. Anxiety narration. Frank mentions food money at dinner.
**Resolution:** Work more (costs NPC time), accept bookkeeping (requires corruption ≥ 40), ask mom (shortens game by 3-7 days), or accept arrangement later (corruption ≥ 180, nuclear option).

### Crisis 2: Frank Finds Drawings
**Trigger:** frank_trust ≥ 16 AND drawing_3_complete+
**When:** Day ~28-35
**Effects:** frank_found_drawings flag. frank_trust -5. Household tension 3-5 days. frank_withdrawal.
**Severity depends on drawing level:** drawing_3 (concerning) → drawing_4 (damning) → drawing_5 (nuclear).
**Resolution:** frank_repair story beat. Response determines tone of remaining Frank arc.

### Crisis 3: Brothers Discover
**Trigger:** handjob_unlock = true
**When:** Day ~38-45
**Effects:** brothers_discover flag. 3-way hallway confrontation. Both brothers' love -3. 2-3 days no NPC activities.
**Resolution:** Permanent Fork 4 (independent / peacemaker / avoidant). Determines final weeks structure.

### Crisis 4: Personal Crisis
**Trigger:** 2+ NPCs in withdrawal simultaneously
**When:** Variable
**Effects:** personal_crisis flag. Energy max 80 for 2 days. Confidence -3.
**Resolution:** Wait. NPCs recover on their timelines. Stat damage done.

---

## 5E. Countdown Behavior

| Days Remaining | Phase | NPC Behavior Changes |
|---------------|-------|---------------------|
| 56-42 | No urgency | Normal. "Eight more weeks" feels forever. |
| 42-28 | Routine | Casual time references. Jake draws more urgently. Ryan mentions "after you leave." |
| 28-14 | Awareness | NPCs acknowledge deadline. Jake: "Will you visit?" Ryan stops mentioning "after." Frank: "Diana's looking at flights." |
| 14-7 | Urgency | Finality undertone. Jake: possessive of time. Ryan: more direct. Frank: late-night chance 0.5→0.7. mom_returning flag set. All NPC corruption -2. |
| 7-1 | Endgame | endgame_active flag. Every activity feels final. Energy max 120 (adrenaline). "One last time" variants unlock for primary NPC. |

---

# Section 6: Story Arc & Permanent Forks

## 6A. The 5 Permanent Forks

These are the irreversible choices that create genuinely different playthroughs. Each fork sets a branch flag that MUST be checked by downstream content (Rule 7).

### Fork 1: Ryan's Truck Incident (Day ~10)

**Context:** Ryan drives Lily to town. On the way back, he puts his hand on her knee. Not aggressive — testing.

**Choices:**
- **"Slap his hand away"** → sets `ryan_resisted`
  - Ryan: surprised. Respects it. Shifts to verbal seduction — more careful, testing with words.
  - Downstream: All Ryan activities get the "seduction" variant. He flirts verbally, not physically. Challenges are about banter, not physical dares. He earns her through charm.
  - Ryan's escalation is SLOWER but trust-based. Kiss requires ryan_trust ≥ 15 (higher than allowed path).
  - His vulnerability moments come earlier because he has to USE vulnerability to progress.

- **"Let his hand stay"** → sets `ryan_allowed`
  - Ryan: grins. Gets bolder. Physical from here on.
  - Downstream: All Ryan activities get the "lust" variant. He pushes physical boundaries. Challenges involve physical dares. She earns through matching his aggression.
  - Ryan's escalation is FASTER but corruption-heavy. Kiss requires corruption ≥ 90 (higher than resisted path).
  - His vulnerability moments come later — he doesn't need to be vulnerable when she's already letting him touch her.

**Both set:** `truck_incident_complete`

**What changes downstream (examples):**
- Truck ride after ryan_resisted: "He turns the music up. Hands on the wheel. Ten and two. But he's looking at her mouth when he talks."
- Truck ride after ryan_allowed: "His hand finds her knee again. Not testing now. Claiming. She doesn't move it."
- Gym after ryan_resisted: "He demonstrates form without touching her. Describing the motion. His voice is doing what his hands won't."
- Gym after ryan_allowed: "He stands behind her at the squat rack. Hands on her hips. 'Form check.'"

### Fork 2: Jake's Secret Sketches (Day ~25)

**Context:** Lily discovers Jake's private drawings of her — poses she didn't know he saw. Her sleeping. Her towel slipping. Her stretching.

**Choices:**
- **"They're beautiful, Jake."** → sets `chose_tender_jake`
  - Jake: overwhelmed. Tears. He didn't expect acceptance.
  - Downstream: Jake arc stays tender-romantic. He draws her with consent from now on. Posing becomes collaborative. The sketchbook is their shared language.
  - Drawing sessions gain DIALOGUE — they talk while he draws. More trust, more emotional depth.
  - His possessiveness stays below the surface. Sweet boy who adores her.
  - Unlocks: Jake's Girl ending path (tender variant).

- **"You've been watching me?"** → sets `chose_possessive_jake`
  - Jake: ashamed. Then defiant. "I can't stop." The shy boy has teeth.
  - Downstream: Jake arc turns obsessive-romantic. He draws compulsively. Doesn't ask permission. The sketches get more detailed, more intimate, more possessive.
  - Drawing sessions lose dialogue — he's silent, intense, focused. More corruption, less trust.
  - His possessiveness surfaces. "Don't wear Ryan's hoodie." "Were you in Dad's office again?"
  - Unlocks: Jake's Muse ending path (obsessive variant).

**Both set:** `jake_sketches_discovered`

**What changes downstream:**
- Wall knocking after chose_tender_jake: "He knocks. She knocks back. Through the wall: 'I drew your smile today.'"
- Wall knocking after chose_possessive_jake: "He knocks. She knocks back. Through the wall: silence. Then: 'Don't go to his room tonight.'"
- Frank finds drawings after chose_tender_jake: drawings are collaborative — some signed by Lily. Frank's reaction: disappointment in HER.
- Frank finds drawings after chose_possessive_jake: drawings are voyeuristic — she didn't know. Frank's reaction: protective of HER.

### Fork 3: Frank's Financial Secret (Day ~35)

**Context:** During bookkeeping (requires intelligence ≥ 30, frank_trust ≥ 16), Lily discovers Frank's business is $40,000 in debt. He doesn't know she found it.

**Choices:**
- **"I found something in the books, Frank."** → sets `chose_confront_frank`
  - Frank: white-faced. Then angry (at the situation, not her). Then: defeated.
  - Downstream: Frank arc becomes adversarial-to-intimate. They fight about it. He resents that she knows. But gradually: she's the only person he can talk to about it. The anger becomes vulnerability. Trust earned through conflict.
  - Bookkeeping sessions gain tension — "You're still looking at those numbers." "Someone has to."
  - Frank starts asking HER advice. Power shift: she has knowledge he needs.
  - His late-night kitchen scenes become about the debt, the marriage, Diana's absence.

- **"I didn't see anything."** → sets `chose_protect_frank`
  - Frank: doesn't know she knows. She carries the secret.
  - Downstream: Frank arc becomes conspiratorial. She protects him by staying silent. The secret is a bond — she knows something Ryan and Jake don't.
  - Bookkeeping sessions gain subtext — she adjusts numbers to hide things. Covers for him without being asked.
  - Frank notices she's being careful with the books. He suspects she knows. Neither says it.
  - The unspoken knowledge becomes a form of intimacy. "You don't have to do that." "Do what?" "...Nothing."

**Both set:** `frank_secret_complete`

**What changes downstream:**
- Frank's arrangement after chose_confront_frank: "I know you can't afford this. Neither can I." Financial honesty changes the arrangement from transactional to desperate.
- Frank's arrangement after chose_protect_frank: "I'll cover everything." He doesn't mention the debt. She knows it's money he doesn't have. The weight of what she's accepting.
- Ryan discovering Frank's debt (if chose_confront_frank AND Ryan finds out): Ryan confronts Frank. Family crisis. "You've been lying to us all year?"

### Fork 4: Brothers Discover Each Other (Day ~42)

**Context:** The truth comes out. Ryan sees Lily leaving Jake's room, or Jake hears through the wall, or both. Hallway confrontation. Three people, thin walls, no more secrets.

**THIS IS THE FORK THAT DOES NOT RECONVERGE.**

**Choices:**
- **"It's none of your business."** → sets `chose_independent`
  - Lily claims agency. Both brothers stunned.
  - ryan_love -3, jake_love -2, confidence +5
  - **Downstream (unique to this path):**
    - Brothers don't fight — they're too shocked by her.
    - Both NPCs shift to cautious pursuit. Neither is sure where they stand.
    - 3-5 UNIQUE scenes: Ryan's quiet truck ride ("I didn't know you had that in you"), Jake's drawing of her with fire in her eyes, Frank notices the shift at dinner ("Something changed.")
    - Final week: both brothers competing, Lily in control. Power dynamic inverted.
    - Unlocks: Independent ending gets a bonus scene. Ryan's Partner ending becomes available (he respects her autonomy).

- **"Please don't fight."** → sets `chose_peacemaker`
  - Lily tries to hold it together. Both brothers are hurt but don't explode.
  - ryan_love -1, jake_love -1, frank_love +1 (he sees her managing a crisis)
  - **Downstream (unique to this path):**
    - Household enters fragile peace. Everyone pretending.
    - 3-5 UNIQUE scenes: breakfast where nobody talks, Jake and Ryan avoiding each other, Frank watching from the kitchen doorway, a moment where all three are in the living room and the tension is unbearable.
    - Relationships can be repaired with both brothers — but the ceiling is lower. Max love -5 for both.
    - Final week: careful, tender, the house walking on eggshells. Beautiful in its fragility.
    - Unlocks: All-Three ending becomes possible (if all NPCs above threshold). Jake's Girl and Frank's Secret endings retain full depth.

- **"(Say nothing. Walk away.)"** → sets `chose_avoidant`
  - Lily leaves. Both brothers stare at each other.
  - jake_love -3, ryan_love -3, frank_love +2 (avoidance = Frank's language)
  - **Downstream (unique to this path):**
    - Brothers fight WITHOUT Lily present. She hears it through the wall. Breaking things.
    - 3-5 UNIQUE scenes: aftermath of the fight (broken glass in the hallway), Jake won't come out of his room for 2 days, Ryan disappears with the truck for a day, Frank disciplines both and locks them down ("This house has RULES").
    - Frank becomes the dominant relationship path — he's the only stable presence.
    - Jake relationship ceiling drops significantly. Ryan's drops somewhat.
    - Final week: Frank-centric. The other two NPCs are damaged.
    - Unlocks: Frank's Arrangement and Frank's Secret endings get bonus scenes. Escape ending becomes the "easiest" (avoidance as character trait).

### Fork 5: Frank's Arrangement (Day ~45)

**Context:** Frank offers to cover all expenses — bus pass, art supplies, phone, food — in exchange for Lily staying with him. Late nights. The office. Whatever he decides.

**Choices:**
- **"What exactly are you offering?"** → dialogue exploration, then:
  - **"Deal."** → sets `accepted_arrangement`
    - Money: +$150 one-time. All expenses auto-paid going forward.
    - frank_love +3, frank_corruption +5, corruption +5
    - Downstream: Frank relationship is now transactional. She has financial freedom but the power dynamic is set. He controls the terms.
    - **Locks out:** Independent ending (she's dependent now). Escape ending (too deep).
    - **Unlocks:** Frank's Arrangement ending.

  - **"I don't need your money."** → sets `refused_arrangement`
    - confidence +5. frank_trust +3 (he respects the refusal).
    - Downstream: Financial pressure remains. But Frank sees her differently — not a transaction, a person. The dynamic shifts to genuine connection.
    - **Locks out:** Frank's Arrangement ending.
    - **Unlocks:** Frank's Secret ending (genuine love, not transaction). Independent ending remains available.

  - **"I'll help with the business — as a partner, not a favor."** → sets `negotiated_arrangement`
    - Money: +$50/session bookkeeping (increased from $25). Expenses partially covered.
    - frank_trust +4, frank_love +2, intelligence +2
    - Downstream: Hybrid path. She's earning it, not accepting charity. Business partnership that evolves into personal. Frank treats her as an equal.
    - **Unlocks:** Frank's Secret ending. Independent ending harder but possible.

---

## 6B. Story Beats (26 beats across 4 acts)

### Act 1: Settling (Beats 1-7, Days 1-14)

| Beat | Day | Trigger | What Happens | Flags Set | Cross-NPC |
|------|-----|---------|-------------|-----------|-----------|
| 1. Arrival | 1 | game_started | Lily arrives. One suitcase. The house. Three men. | game_started | — |
| 2. First Morning | 2 | game_started + 1 day | Bathroom collision with Jake. She's in a towel. He drops his glasses. | first_morning | — |
| 3. Bus Problem | 3 | first_morning + 1 day | Bus costs $2/ride. Ryan offers truck. "Get in." Choice: bus ($2) or ride (Ryan dependency). | bus_problem_discovered, town_access | Ryan: love +1 if ride, nothing if bus |
| 4. Mom's Call | 4 | town_access | Diana calls. Transfer delayed. "I wouldn't have asked if there was another option." | mom_called | — |
| 5. The Math | 5-7 | mom_called + 1 day | Lily does the numbers. $400. $385/month. $13 surplus. Frank offers cleaning job ($20/session). | money_crisis_realized, chores_started | Frank: trust +2 (offered work) |
| 6. First Week Complete | 7 | 7 days elapsed | Milestone. Routines forming. She knows their patterns now. | first_week_complete | — |
| 7. First Awareness | 10-14 | first_week_complete + exposure conditions | Something shifts. First physical awareness of one of the NPCs. THREE VARIANTS (first NPC to meet conditions): Jake (corruption 25, jake_love ≥ 8), Ryan (corruption 40, ryan_corruption ≥ 10), Frank (corruption 60, frank_trust ≥ 10). Only ONE fires. | exposure_unlock | The unchosen NPCs don't get this moment. EXCLUSIVE. |

**Hidden Consequence planted in Act 1:**
- Beat 3 (Bus): If player takes Ryan's truck, ryan dependency begins. If bus: independence but money drain.
- Beat 5 (The Math): Player can choose to "tell mom the truth" during the call. If yes: asked_mom_for_money flag. Mom sends $100 but might come home 3-7 days earlier (countdown shortens).

### Act 2: Deepening (Beats 8-15, Days 14-35)

| Beat | Day | Trigger | What Happens | Flags Set | Cross-NPC |
|------|-----|---------|-------------|-----------|-----------|
| 8. Ryan's Push | 10-12 | exposure_unlock + Ryan available | **PERMANENT FORK 1.** Truck. Hand on knee. Resist or allow. | truck_incident_complete + ryan_resisted OR ryan_allowed | — |
| 9. Bookkeeping Offer | 12-16 | chores_started + corruption ≥ 40 + intelligence ≥ 20 | Frank offers bookkeeping work. $25/session. Office. Door. | bookkeeping_started | Jake notices she's spending time in Dad's office |
| 10. Creek Discovery | 14-18 | first_week_complete + NPC invites | First time at the creek. Jake or Ryan invites (whichever has higher love). Different tone per NPC. | first_swim | — |
| 11. Jake Shows His Art | 16-20 | jake_love ≥ 12 + drawing_1_complete | Jake willingly shows his portfolio. Not the secret sketches — the real work. He's nervous. | saw_jakes_art | — |
| 12. First Flirtation | 18-22 | flirt_unlock = false + corruption ≥ 50 + NPC love ≥ 10 | THREE VARIANTS (first NPC to qualify). Deliberate flirtation — not accidental. She chooses to cross the line. | flirt_unlock | EXCLUSIVE. Other NPCs don't get this moment. |
| 13. Ryan Catches Evidence | 20-25 | flirt_unlock + ryan_trust ≥ 8 | Ryan notices something. Charcoal on her fingers. A drawing poking from under her pillow. "You and Jake, huh." | ryan_caught_her | Jake doesn't know Ryan knows (yet) |
| 14. First Kiss | 22-28 | kiss_unlock = false + corruption ≥ 70 + NPC love ≥ 15 + NPC trust ≥ 12 | THREE VARIANTS. The first kiss. Tender (Jake), aggressive (Ryan), forbidden (Frank). Only ONE is the canonical first. | kiss_unlock | EXCLUSIVE. The first kiss belongs to whoever earned it. |
| 15. Jake's Secret Sketches | 25-30 | jake_love ≥ 20 + corruption ≥ 90 + drawing_2_complete | **PERMANENT FORK 2.** Lily discovers the private drawings. "Beautiful" or "Watching me?" | jake_sketches_discovered + chose_tender_jake OR chose_possessive_jake | — |

### Act 3: Crisis (Beats 16-21, Days 35-48)

| Beat | Day | Trigger | What Happens | Flags Set | Cross-NPC |
|------|-----|---------|-------------|-----------|-----------|
| 16. Frank's Late Night | 30-35 | frank_love ≥ 16 + frank_trust ≥ 18 + corruption ≥ 100 | 2 AM. Kitchen. Whiskey. The first truly loaded encounter. His hand is on the table. Three inches from hers. | frank_kitchen_moment | Jake might hear her door open: jake_heard_late_movement |
| 17. Frank's Financial Secret | 32-38 | intelligence ≥ 30 + frank_trust ≥ 16 + bookkeeping_started | **PERMANENT FORK 3.** She finds the debt in the books. Confront or protect? | frank_secret_complete + chose_confront_frank OR chose_protect_frank | If chose_confront: potential Ryan cascade later |
| 18. Physical Escalation | 34-40 | kiss_unlock + corruption ≥ 120 + NPC love ≥ 20 | THREE VARIANTS. Handjob milestone. Same mechanic as first kiss — first NPC to qualify wins. | handjob_unlock | EXCLUSIVE. |
| 19. Frank Finds Drawings | 35-42 | frank_trust ≥ 16 + drawing_3_complete | CRISIS 2. Frank finds Jake's drawings. Severity depends on drawing level. | frank_found_drawings | Household tension. Frank-Jake conflict. Lily caught between. |
| 20. Frank/Jake Repair | 38-45 | frank_found_drawings + 3 days elapsed | Two repair beats run in parallel: frank_repair (Lily rebuilds Frank's trust) and jake_repair (Lily rebuilds Jake after Frank's anger). | frank_repair_complete, jake_repair_complete | The repair tone depends on chose_tender_jake vs chose_possessive_jake |
| 21. Brothers Discover | 40-48 | handjob_unlock + 3 days | **PERMANENT FORK 4.** Ryan sees Lily leaving Jake's room. Or Jake hears. Hallway confrontation. Independent / Peacemaker / Avoidant. | brothers_discover + chose_independent OR chose_peacemaker OR chose_avoidant | Largest cross-NPC impact. Reshapes entire household. |

### Act 4: Convergence (Beats 22-26, Days 45-56)

| Beat | Day | Trigger | What Happens | Flags Set | Cross-NPC |
|------|-----|---------|-------------|-----------|-----------|
| 22. Financial Crisis | 42-48 | money < $50 OR financial_crisis not yet | Economic pressure peaks. Mom's transfer bounced. Bills stack. | financial_crisis | Frank aware. Ryan offers money (strings attached). |
| 23. Frank's Arrangement | 44-50 | crisis_resolved + frank_love ≥ 20 | **PERMANENT FORK 5.** Frank offers to cover everything. Accept / Refuse / Negotiate. | frank_offer + accepted/refused/negotiated_arrangement | — |
| 24. Mom's Return Call | 48-52 | frank_offer OR days ≥ 48 | Diana calls. She's coming home next week. Flight booked. | mom_returning | All NPC corruption -2. Reality hits. |
| 25. Final Week | 50-55 | mom_returning + 2 days | endgame_active flag. Every interaction feels final. NPC-specific "one last time" scenes. | endgame_active | Each NPC's final scenes determined by their ending path |
| 26. Resolution | 56 | endgame_active + 7 days | Mom walks through the door. Who is Lily now? Ending fires based on conditions. | game_complete | ONE ending fires. |

---

## 6C. Cross-NPC Consequence Chains

### Chain 1: The Drawing Cascade
```
Day 12: Lily signs Jake's drawing (innocent choice during drawing session)
  → sets: lily_signed_drawing flag
Day 35: Frank finds drawings. If lily_signed_drawing:
  → Frank knows she participated willingly. frank_trust -2 EXTRA.
  → Frank's reaction: disappointment in HER, not just Jake.
Day 35: If lily_signed_drawing NOT set:
  → Frank assumes Jake drew without her knowledge. Protective of Lily.
  → frank_trust penalty reduced by 2. Frank confronts Jake, not Lily.
```

### Chain 2: The Hoodie Cascade
```
Day 8: Lily borrows Ryan's hoodie (truck ride, practical — it's cold)
  → sets: wearing_ryans_hoodie flag
Day 15: Jake sees Lily wearing Ryan's hoodie around the house
  → jake_saw_hoodie flag
  → jake_trust -2. Jake: "Is that Ryan's?"
  → Next drawing session: Jake draws her in the hoodie. Possessive.
Day 25: If jake_sketches include hoodie drawing AND Frank finds them:
  → Frank sees the hoodie in the drawing. Knows about Ryan's involvement too.
  → Nuclear version of frank_finds_drawings.
```

### Chain 3: The Truth Cascade
```
Day 4: Lily tells mom the truth about money (asked_mom_for_money)
  → Mom sends $100 but starts worrying
Day 28: Mom calls more frequently. Asks pointed questions.
  → If asked_mom_for_money: mom_suspicious flag
Day 48: Mom books flight. If mom_suspicious:
  → Mom comes home 3-7 days EARLIER. Countdown shortened.
  → Endgame compressed. Less time for final scenes.
```

### Chain 4: The Bookkeeping Cascade
```
Day 16: Lily starts bookkeeping with Frank
Day 32: Intelligence ≥ 30 + she finds the debt
  → If chose_confront_frank: Frank knows she knows
  → Day 40: Ryan mentions Frank's money stress at dinner
    → If chose_confront_frank: Lily accidentally confirms. ryan_knows_debt flag.
    → Day 45: Ryan confronts Frank. "You've been lying to us."
      → Family crisis ON TOP of brothers_discover. Maximum chaos.
  → If chose_protect_frank: Ryan's comment passes. Lily stays silent.
    → Frank catches her eye across the table. Neither speaks.
    → frank_love +2 (the shared secret deepens).
```

### Chain 5: The Gas Money Cascade
```
Day 6: Lily gives Ryan gas money without him asking ($10)
  → gave_gas_money flag
  → ryan_love +3, ryan_trust +2
Day 30: When Ryan discovers Jake/Lily involvement:
  → If gave_gas_money: Ryan's hurt is DEEPER. "I thought we had something."
    → ryan_love penalty -1 EXTRA during brothers_discover.
  → If NOT gave_gas_money: Ryan's reaction is competitive, not hurt.
    → He's angry about losing, not about losing something real.
```

---

## 6D. Hidden Consequences

Small choices that seem innocent but pay off weeks later.

| When | Choice | Seems Like | Actually |
|------|--------|-----------|----------|
| Day 3 | Take Ryan's truck vs bus | Transport preference | Ryan dependency starts. After 5+ rides: he expects it. Stopping = ryan_trust -2. |
| Day 5 | Tell mom truth about money | Honesty with mom | Mom might come home early. Game shortens 3-7 days. |
| Day 8 | Borrow Ryan's hoodie | Staying warm | Jake sees it Day 15. Draws it Day 20. Frank finds drawing Day 35. |
| Day 12 | Sign Jake's drawing | Artistic collaboration | Frank finds signature Day 35. Proves willing participation. |
| Day 14 | Fix bedroom door lock | Practical home repair | Ryan can't walk in for random encounters. Some story beats don't fire. But Lily has PRIVACY — confidence +3 over time. |
| Day 20 | Buy Jake expensive charcoal ($30) | Gift for artist | Frank notices in bookkeeping. "Thirty dollars on charcoal." He's measuring her investment in Jake. |
| Day 25 | Agree to model (clothed) | Helping Jake's art class | Drawing exhibited at campus art show Day 40. Ryan and Frank both see it. |

---

## 6E. Flag Dependency Summary

### Gate Flags (shared across NPCs)
```
exposure_unlock ← first_awareness beat (exclusive, first NPC to qualify)
flirt_unlock ← first_flirtation beat (exclusive)
tease_unlock ← first tease activity choice
kiss_unlock ← first_kiss beat (exclusive)
handjob_unlock ← physical_escalation beat (exclusive)
blowjob_unlock ← oral activity choice (any NPC)
sex_unlock ← sex activity choice (any NPC)
```

### Branch Flags (permanent, from forks)
```
ryan_resisted / ryan_allowed ← Fork 1 (truck incident)
chose_tender_jake / chose_possessive_jake ← Fork 2 (secret sketches)
chose_confront_frank / chose_protect_frank ← Fork 3 (financial secret)
chose_independent / chose_peacemaker / chose_avoidant ← Fork 4 (brothers discover)
accepted_arrangement / refused_arrangement / negotiated_arrangement ← Fork 5 (Frank's offer)
```

### Cross-NPC Awareness Flags
```
jake_heard_ryan / jake_heard_late_movement / jake_saw_hoodie / jake_lonely
ryan_saw_jake / ryan_noticed_art / ryan_noticed_cooking / ryan_saw_frank_office
frank_noticed_jake_time / frank_noticed_spending / frank_noticed_ryan_rides / frank_found_drawings
```

### Consequence Flags
```
lily_signed_drawing / wearing_ryans_hoodie / asked_mom_for_money
gave_gas_money / fixed_door_lock / mom_suspicious
```

### Reliability Flags (Frank's Trust Ledger)
```
bookkeeping_on_time_1 / _2 / _3
food_money_paid_1 / _2
kept_financial_secret / house_rules_followed / helped_workshop_unprompted
```

---

# Section 7: Endings

## 8 Endings with Conditions

### Ending 1: Jake's Girl (Tender)

**Conditions:** jake_love = highest NPC love AND jake_love ≥ 30 AND chose_tender_jake AND corruption < 160
**Final week content:** Drawing sessions become goodbye/commitment scenes. Jake finishes a final portrait — the best he's ever done. They make plans in whispers through the wall. "I'll visit." "Promise?" The sketchbook goes with him to art school — every page is her.
**Resolution:** Mom arrives. Lily and Jake hold hands behind the couch. Small smile. Secret continues.

### Ending 2: Jake's Muse (Obsessive)

**Conditions:** jake_love = highest NPC love AND jake_love ≥ 30 AND chose_possessive_jake AND corruption ≥ 160
**Final week content:** Jake draws frantically. Every pose, every angle. He needs enough to last. The room is wallpapered with her. "You're the only thing I'll ever want to draw." It's devotion. It's also terrifying.
**Resolution:** Mom arrives. Jake's sketchbook is under his mattress. Lily finds a drawing slipped under her pillow — her sleeping. He's still watching. She doesn't mind.

### Ending 3: Ryan's Partner (Trust)

**Conditions:** ryan_love = highest NPC love AND ryan_trust ≥ 25 AND (chose_independent OR ryan_resisted)
**Final week content:** Truck rides get longer. He talks about leaving town — job in the city, starting over. "Come with me." Not a dare. Not a game. The first thing Ryan has ever said that he can't take back with a grin.
**Resolution:** Mom arrives. Ryan's truck keys are on the counter. He's outside. Engine running. He doesn't look at the house. He's looking at the road. "You coming or what?" Same words. Different meaning.

### Ending 4: Ryan's Conquest (Lust)

**Conditions:** ryan_love = highest NPC love AND ryan_trust < 25 AND ryan_allowed
**Final week content:** Maximum physical intensity. Every encounter is urgent. But the tenderness isn't there — it's bodies, not hearts. Ryan talks about "after" like it's a punchline. "It was fun, right?"
**Resolution:** Mom arrives. Ryan winks at Lily across the dinner table. Later, his truck rolls past her window. Tap on the glass. "Later?" He means tonight. He means forever. Both are temporary.

### Ending 5: Frank's Arrangement (Transactional)

**Conditions:** frank_love = highest NPC love AND accepted_arrangement AND frank_trust ≥ 20
**Final week content:** Late-night kitchen scenes every night. He's already planned it — Diana will travel again. "Three months this time. Dubai." The arrangement continues. Financial security. Professional distance in public. "Miss Chen" at breakfast. "Lily" at midnight.
**Resolution:** Mom arrives. Frank shakes Lily's hand goodbye. "You've been a great help with the books." Diana smiles. Nobody suspects. That night, Lily's phone: one text from Frank. "She leaves again in October."

### Ending 6: Frank's Secret (Genuine Love)

**Conditions:** frank_love = highest NPC love AND (refused_arrangement OR negotiated_arrangement) AND frank_love ≥ 30 AND frank_trust ≥ 28
**Final week content:** The hardest ending to earn. Late-night kitchen: "I love you. I shouldn't. I do." He doesn't touch her. The words are enough. Both of them sitting in the kitchen knowing everything and choosing nothing — because choosing would destroy the house.
**Resolution:** Mom arrives. Frank carries Lily's suitcase to Diana's car. His hand on the trunk lingers. Diana says "Thank you for taking care of her." Frank: "She took care of us." He means the household. He means his heart. Lily's phone, that night: nothing. But she drives past the property six months later. His truck is there. The kitchen light is on at 2 AM.

### Ending 7: Independent

**Conditions:** NO NPC love is highest by more than 5 points (balanced or low) AND confidence ≥ 60 AND money ≥ 500
**Final week content:** Lily gets the diner job permanent. Finds a room to rent in town. Packs her things carefully. Thanks each NPC genuinely. "You taught me things." She means it differently for each one.
**Resolution:** Mom arrives. Lily already has her coat on. "I found a place in town." Diana: surprised, proud. Frank: quiet respect. Ryan: "You don't need any of us." Jake: a drawing, slid under her door. The girl who arrived with one suitcase leaves with two.

### Ending 8: Escape

**Conditions:** corruption < 80 AND all NPC love < 15
**Final week content:** Minimal. She avoided everything. The house was just a house. She did her homework, she cleaned, she kept her head down. Mom's return is a relief.
**Resolution:** Mom arrives. Lily hugs her for a long time. The house smells like sawdust and coffee. She thinks: "Almost." She doesn't know what she almost did. But the word stays with her. In her dorm room that fall, she catches herself listening through the wall for a knock that won't come.

---

## Ending Reachability Check

| Ending | Required Stats | Required Flags | Fork Dependencies | Reachable By |
|--------|---------------|---------------|-------------------|-------------|
| Jake's Girl | jake_love ≥ 30, corruption < 160, beauty ≥ 45 | chose_tender_jake | Fork 2 = tender | Jake-focused player, moderate corruption |
| Jake's Muse | jake_love ≥ 30, corruption ≥ 160, beauty ≥ 45 | chose_possessive_jake | Fork 2 = possessive | Jake-focused, high corruption |
| Ryan's Partner | ryan_love highest, ryan_trust ≥ 25, fitness ≥ 40 | chose_independent OR ryan_resisted | Fork 1 = resisted AND/OR Fork 4 = independent | Ryan-focused, earned trust |
| Ryan's Conquest | ryan_love highest, ryan_trust < 25, fitness ≥ 30 | ryan_allowed | Fork 1 = allowed | Ryan-focused, lust path |
| Frank's Arrangement | frank_love highest, frank_trust ≥ 20, intelligence ≥ 30 | accepted_arrangement | Fork 5 = accepted | Frank-focused, transactional |
| Frank's Secret | frank_love highest, frank_trust ≥ 28, frank_love ≥ 30, intelligence ≥ 35 | refused OR negotiated arrangement | Fork 5 = refused/negotiated | Frank-focused, hardest ending |
| Independent | confidence ≥ 60, money ≥ 500 | — | No fork dependency | Balanced player, self-focused |
| Escape | corruption < 80, all NPC love < 15 | — | No fork dependency | Avoidant player |

---

# Section 8: Daily Loop Reference

## 8A. Time Slot Table

| Time Slot | Hours | Available Activities |
|-----------|-------|---------------------|
| **Early Morning** | 05:00-07:00 | Yoga, morning routine/grooming, workshop help (Frank) |
| **Morning** | 07:00-09:00 | Breakfast (all NPCs), jogging (property), gym (Ryan, town) |
| **Late Morning** | 09:00-12:00 | House cleaning ($20), job site (Ryan, $40), campus classes (town) |
| **Midday** | 12:00-13:00 | Lunch (energy +20) |
| **Afternoon** | 13:00-17:00 | Drawing session (Jake), bookkeeping (Frank, MWF), library (Jake, town), truck ride (Ryan), creek (Jake OR Ryan), park sketching (Jake, weekend), gym (Ryan, town) |
| **Evening** | 17:00-19:00 | Cooking dinner (Frank), dinner (all NPCs), diner shift ($45, extends through night) |
| **Night** | 19:00-22:00 | TV couch (Ryan), truck ride (Ryan), shopping (town) |
| **Late Night** | 22:00-01:00 | Wall knocking (Jake), late-night kitchen (Frank, 50% chance), stargazing, journal, sleep |

## 8B. Energy Budget Examples

**Max energy:** 100 (120 during endgame, 110 at fitness ≥ 61)
**Restoration:** Sleep = full reset. Breakfast +15. Lunch +20. Dinner +25.

### Good Day (Jake-focused, Day 15)
| Time | Activity | Energy Cost | Stats Gained |
|------|----------|-------------|-------------|
| 06:00 | Yoga | -15 | beauty +2, fitness +1 |
| 07:30 | Breakfast (talk to Jake) | +15 | jake_love +1 |
| 09:00 | Campus art class | -20 | intelligence +3 |
| 12:00 | Lunch | +20 | — |
| 14:00 | Drawing session with Jake | -15 | jake_love +3, beauty check |
| 17:30 | Dinner (sit next to Jake) | +25 | jake_love +1 |
| 22:00 | Wall knocking | -10 | jake_love +2 |
| 23:30 | Sleep | reset | — |
**Net energy:** 100 - 15 + 15 - 20 + 20 - 15 + 25 - 10 = 100 ✓
**Day result:** beauty +2, fitness +1, intelligence +3, jake_love +7. But: no money earned, Ryan ignored, Frank ignored.

### Bad Day (Crisis day, Day 20)
| Time | Activity | Energy Cost | Stats Gained |
|------|----------|-------------|-------------|
| 06:00 | Grooming | -10 | beauty +2 |
| 07:30 | Breakfast | +15 | — (tense — NPC in withdrawal) |
| 09:00 | House cleaning | -25 | money +$20 |
| 12:00 | Lunch | +20 | — |
| 14:00 | Bookkeeping with Frank | -20 | money +$25, frank_trust +2 |
| 17:00 | Diner shift | -20 | money +$45, confidence +1 |
| 22:00 | Too tired. Sleep. | reset | — |
**Net energy:** 100 - 10 + 15 - 25 + 20 - 20 - 20 = 60 (exhausted by night)
**Day result:** money +$90, beauty +2, frank_trust +2, confidence +1. But: missed Jake all day (love decaying), missed Ryan (love decaying), missed wall knocking (jake_love -1).

### Strategic Day (Balanced, Day 30)
| Time | Activity | Energy Cost | Stats Gained |
|------|----------|-------------|-------------|
| 06:00 | Jogging (property) | -15 | fitness +1, confidence +1 |
| 07:30 | Breakfast (talk to Ryan) | +15 | ryan_love +1 |
| 09:00 | Job site with Ryan | -25 | money +$40, fitness +1, ryan_trust +2 |
| 12:00 | Lunch | +20 | — |
| 14:00 | Drawing session with Jake | -15 | jake_love +3 |
| 17:00 | Cooking with Frank | -20 | frank_love +2 |
| 19:00 | Dinner | +25 | — |
| 22:00 | Wall knocking | -10 | jake_love +2 |
| 23:00 | Sleep | reset | — |
**Net energy:** 100 - 15 + 15 - 25 + 20 - 15 - 20 + 25 - 10 = 75 ✓
**Day result:** money +$40, fitness +2, confidence +1, jake_love +5, ryan_love +1, ryan_trust +2, frank_love +2. ALL NPCs touched. But: no deep investment in any. No beauty. No intelligence.

## 8C. Week-by-Week Progression

### Week 1 (Days 1-7): Settling
- **Player focus:** Learn the house. Meet NPCs. Establish routines.
- **Money:** $400 → ~$350 (food money due Monday)
- **Key beats:** Arrival, First Morning, Bus Problem, Mom's Call, The Math
- **NPC status:** Jake warm (love 5→10). Ryan testing (trust 0→3). Frank distant (trust 5→7).
- **Activities available:** Cleaning, meals, solo activities, basic NPC interactions.

### Week 2 (Days 8-14): First Investments
- **Player focus:** Choose which NPCs to invest in. Economic pressure begins.
- **Money:** $350 → ~$250 (bus pass $80 due)
- **Key beats:** Ryan's Push (Fork 1), Bookkeeping Offer, Creek Discovery
- **NPC status:** First awareness fires. One NPC pulls ahead.
- **Activities available:** Bookkeeping unlocks (if corruption ≥ 40). Drawing deepens (if beauty ≥ 25).

### Week 3-4 (Days 15-28): Deepening
- **Player focus:** First flirt, first kiss. NPC relationships deepen. Economic pressure real.
- **Money:** Depends on work choices. Mom's transfer arrives (maybe).
- **Key beats:** First Flirtation, Ryan Catches Evidence, First Kiss, Jake's Sketches (Fork 2)
- **NPC status:** Primary NPC at love 15-22. Secondary at 8-12. Tertiary at 5-8.
- **Activities available:** All NPC activities open. Escalation tiers unlocking.

### Week 5-6 (Days 29-42): Crisis
- **Player focus:** Managing fallout. Crises stack. Permanent forks fire.
- **Money:** Financial crisis likely. Arrangement offer coming.
- **Key beats:** Frank's Late Night, Financial Secret (Fork 3), Physical Escalation, Frank Finds Drawings, Brothers Discover (Fork 4)
- **NPC status:** Primary NPC at love 22-30. Household tension. Withdrawals happening.
- **Activities available:** Some locked during withdrawals. Crisis beats interrupt routine.

### Week 7-8 (Days 43-56): Endgame
- **Player focus:** Final investments. Ending determined. Every moment counts.
- **Money:** Arrangement decides (Fork 5). Otherwise: tight.
- **Key beats:** Frank's Arrangement (Fork 5), Mom's Return Call, Final Week, Resolution
- **NPC status:** Primary NPC approaching max. Countdown urgency. "One last time" variants.
- **Activities available:** Endgame variants unlock. Energy max increases. Time runs out.

---

# Consistency Verification Checklist

Before building TOML from this document, verify:

- [ ] Every stat in Section 3 (NPC mechanics) exists in Section 2 (stat definitions) ✓
- [ ] Every activity in Section 3 is fully specified in Section 4 (activity map) ✓
- [ ] Every permanent fork in Section 6A locks/unlocks an ending in Section 7 ✓
- [ ] Every flag set in Section 6 is checked somewhere in Sections 3, 4, or 7 ✓
- [ ] Economic math in Section 2 matches income/expense numbers in Section 4 ✓
- [ ] Stat budgets in Section 2 are achievable given activity frequencies in Section 4 ✓
- [ ] Every NPC refusal trigger in Section 3 has a recovery path ✓
- [ ] No two NPCs share more than 30% of activity mechanics ✓
- [ ] Each of 6 motivations served by 2+ concrete systems ✓
- [ ] Every ending in Section 7 is reachable given stat budgets in Section 2 ✓
- [ ] All cross-NPC awareness flags in Section 3D are checked in Section 4 activity variants ✓
- [ ] All hidden consequence flags in Section 6D are checked in Section 6B story beats ✓
- [ ] Schedule conflicts in Section 4F create genuine Motivation 1 tension ✓
- [ ] Pressure systems in Section 5 are consistent with economic math in Section 2D ✓
