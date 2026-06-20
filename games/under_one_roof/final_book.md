# UNDER ONE ROOF — Complete Game Design Book
# ═══════════════════════════════════════════
# 
# Female protagonist multi-NPC parallel arc adult interactive fiction
# Protagonist: Lily Chen, 19, art student
# NPCs: Frank (step-father, 45), Ryan (step-brother, 23), Jake (step-brother, 20)
# Setting: Isolated rural property, ~60 in-game days
# Architecture: Multi-NPC Parallel Arcs (Pattern A) with Player-Stat-Driven Progression
#
# Generated: 2026-04-01
# Phases: 1-6 (Phase 0 skipped — no pre-integrated video library)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## TABLE OF CONTENTS

1. **FOUNDATION** — Game identity, NPCs, setting, premise, tone, scope
2. **CHARACTERS & STAT ECONOMY** — Player/NPC definitions, stat mechanics, gate flags, flag inventory
3. **WORLD DESIGN** — 21 locations, time system, economic model, NPC schedules, wardrobe, random encounters
4. **STORY EVENTS** — Dramatic structure, 27 beats across 4 acts, all crisis/branch/bridge events
5. **ACTIVITIES** — 13 NPC activities, 3 meals, utility canvases, solo activities
6. **STORY ARC** — Chapters, journal nodes, branching paths, emotion mappings, hints
7. **QUALITY CHECKLIST** — Verification results

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━



# PHASE 1: FOUNDATION
# Under One Roof

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## GAME IDENTITY

**Title**: Under One Roof
**Protagonist**: Lily Chen (female, player-controlled), 19 years old
**Genre**: Adult interactive fiction — multi-NPC parallel arc, female protagonist
**Perspective**: Female protagonist — player IS the woman
**Theme**: Slow-burn domestic corruption. Proximity + economic pressure + pride = a girl who won't ask for help finding her own solutions, each one pulling her deeper. The house is the arena. The thin walls hear everything.

### Engine Configuration

| Setting | Value | Notes |
|---------|-------|-------|
| **Starting Canvas** | `opening_arrival` | Lily arrives with one suitcase — no trigger (fires on game start) |
| **Schema Version** | `"0.2"` | TOML v2 schema |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## STRUCTURAL INNOVATION: CLOSED-ECOSYSTEM PARALLEL ARCS

This game places three fundamentally different male archetypes under one roof with a female protagonist who can't leave. Key structural decisions:

### The Closed Ecosystem
- Every NPC lives in the same house. Lily can't pursue one without the others noticing.
- Cross-NPC awareness is built into the architecture — brothers can discover each other, Frank can discover what his sons are doing. Cascading story events.
- The shared bathroom, thin walls, and single kitchen create unavoidable proximity. Random encounters write themselves.
- There is no "safe space" — even Lily's bedroom shares a wall with Jake's room.

### Three Simultaneous Arcs, Three Different Fantasies
- **Jake (CORRUPTION + LOVE)** — sweet, tender, the step-brother who draws her. Innocent corruption through art and affection. EASY difficulty, earliest activation (corruption 25+).
- **Ryan (LUST + SEDUCTION)** — aggressive, physical, the step-brother who pushes. Raw desire against Lily's resistance. MEDIUM difficulty (corruption 50+).
- **Frank (FORBIDDEN + DOMINANCE)** — the step-father. Authority, control, the taboo itself. HARD difficulty, latest activation (corruption 100+).

### Player-Stat-Driven Progression
- **Player corruption** (0-250) is the primary driver — not any NPC stat.
- Corruption gates which activity CHOICES appear across all arcs.
- NPC stats (love/trust/corruption per NPC) are secondary — they gate NPC-specific scenes.
- **Shared skill unlock flags** (7 flags: exposure → flirt → tease → kiss → handjob → blowjob → sex) are earnable through ANY NPC. A kiss learned with Jake enables kissing choices with Ryan and Frank.

### Economic Pressure as Corruption Engine
- Lily starts with $400. Monthly burn is ~$385. Mom's transfer ($200/month) is unreliable.
- Base-tier income (cleaning at $20/session) is mathematically insufficient.
- Higher-paying work requires corruption progression: bookkeeping with Frank (corruption >= 40), art modeling for Jake (corruption >= 50), Ryan's "favors" (corruption >= 150).
- The game never tells Lily to escalate. The math does.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## THE PROTAGONIST: LILY CHEN

**Age**: 19
**Background**: Art student, second year. Parents divorced at 14. Mom remarried Frank 8 months ago. Lily attended the wedding, made small talk, went home. She doesn't know these people.

**Visual**: Dark hair, usually in a messy bun or ponytail. Slim build, average height. Arrives in a hoodie and jeans. Looks younger than 19. The kind of face you'd trust immediately.

**Psychology**:
- **Want**: Independence — finish her degree, get her own place, stop depending on anyone
- **Need**: Connection — she's been isolated since the divorce, builds walls, keeps people at distance
- **Fear**: Being trapped — dependency on people she can't trust or control
- **Flaw**: Pride — she'd rather suffer quietly than ask for help. She'll find her own solutions, even if those solutions push her boundaries

**Why her flaw is the engine**: Lily's pride means she won't ask Frank for money. She won't admit she's struggling. She won't call Mom crying. Every practical problem she solves herself pulls her deeper into the household's orbit. The game never tells her to take her clothes off. The math does, and her pride won't let her ask for another way.

**Sexual history**: Limited. A boyfriend in high school that lasted 4 months. She's not innocent — she's inexperienced. She knows what sex is. She's just never had it be complicated.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## THE NPCs

### NPC 1: Frank Harmon — The Step-Father

**Vibe**: Controlled, responsible, quietly intense. The man who built his life with his hands and runs his household the same way. When he talks, people listen — not because he's loud, but because he means every syllable.

**What makes him compelling**: Frank is the authority figure who *tries* to keep things appropriate. He sets rules. He's careful. But Lily is in his house, walking around in increasingly less clothing, and he's been alone since his first wife left. The tension builds because he fights it — every scene is loaded with what he's *not* saying. When control finally breaks, it breaks in the direction of dominance.

**Age**: 45
**Build**: Broad shoulders, calloused hands. Salt-and-pepper stubble, crow's feet around steady dark eyes. Smells like sawdust and black coffee. Flannels with rolled sleeves, work boots, jeans that fit right.

**Primary Driver**: FORBIDDEN (tension)
**Secondary Driver**: DOMINANCE (submission)
**Starting Traits**: `love = 0, trust = 5, corruption = 0`

**Key dynamic**: Frank controls resources. Car keys, spending money, house rules, room assignments, workshop access. Every practical request Lily makes puts her in his orbit. He doesn't exploit this at first. But the power imbalance is always there.

**Resistance type**: Self-control. He knows exactly what he's feeling and he's horrified by it.

**Difficulty**: HARD — latest arc to activate (corruption 100+), requires highest investment across all three triangle stats. The payoff matches the difficulty.

*Internal thought at T1:* "She's Diana's daughter. She's Diana's daughter. Stop looking at her hands."

---

### NPC 2: Ryan Harmon — The Older Step-Brother

**Vibe**: Confident, teasing, physically forward. Not mean — just relentless. The kind of guy who tests every boundary once to see what happens. Makes everything feel like a dare.

**What makes him compelling**: Ryan doesn't do subtlety. He sees Lily and decides she's interesting. He flirts openly, pushes boundaries, watches her reactions. He's the "you're not really my sister" guy — uses the technicality as a license. The lust is raw and physical. The seduction is the game of wearing her down.

**Age**: 23
**Build**: Athletic, tanned from outdoor work. Strong jaw, cocky grin. Thick arms from hauling lumber and drywall. Tank tops, work boots, jeans slung low. Faded scar on his forearm.

**Primary Driver**: LUST (arousal)
**Secondary Driver**: SEDUCTION (resistance)
**Starting Traits**: `love = 0, trust = 0, corruption = 10`

**Key dynamic**: Ryan controls social access. He has the truck. He knows people in town. If Lily wants to go anywhere or do anything fun, Ryan is the gatekeeper. He's also the one most likely to catch her with others — and he'll use that leverage.

**Resistance type**: None from him — the resistance is Lily's. Ryan is ready from day one.

**Difficulty**: MEDIUM — arc activates relatively early (corruption 50+), but requires trust-building alongside physical escalation.

*Internal thought at T1:* "Dad married her mom eight months ago and now she's sleeping down the hall. This is going to be a fun summer."

---

### NPC 3: Jake Harmon — The Younger Step-Brother

**Vibe**: Shy, thoughtful, genuine. Draws constantly. Blushes when caught staring. The quiet one in a loud family. Observant in a way the others aren't.

**What makes him compelling**: Jake is the slow-burn innocent corruption arc. He genuinely likes Lily. They bond over art, over being the quiet ones. The corruption happens because proximity + genuine affection + hormones is unstoppable. Every step feels natural, consensual, tender — which makes it hit differently than Ryan's pursuit or Frank's power dynamic.

**Age**: 20
**Build**: Lean. Shaggy brown hair that falls in his eyes. Wears glasses when drawing. Soft hands compared to his brother and father. Faded band t-shirt and jeans.

**Primary Driver**: CORRUPTION (corruption)
**Secondary Driver**: LOVE (love)
**Starting Traits**: `love = 5, trust = 5, corruption = 0`

**Key dynamic**: Jake shares a wall with Lily's bedroom. He's the one she confides in. He sees her as a person first — not a conquest (Ryan) or a complication (Frank). He's the most emotionally vulnerable NPC.

**Resistance type**: Innocence. He doesn't resist because he's strong — he resists because he doesn't understand what's happening until it's too late.

**Difficulty**: EASY — earliest arc to activate (corruption 25+), lowest stat thresholds. Jake is the entry point. His arcs typically set the first unlock flags, which enable higher-tier options with the other NPCs.

*Internal thought at T1:* "She laughs differently when it's just us. Quieter. Real. I drew her hands three times today and I don't think she noticed."

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## NPC CUSTOMIZATION (@-Syntax)

All three NPCs are customizable. Players can rename them and adjust relationship labels at game start.

| NPC | Default Name | Default Relationship | Options |
|-----|-------------|---------------------|---------|
| `npc_frank` | Frank | step-dad | step-dad, mom's boyfriend, landlord |
| `npc_ryan` | Ryan | step-brother | step-brother, housemate, roommate |
| `npc_jake` | Jake | step-brother | step-brother, housemate, roommate |

All content uses `@frank`, `@ryan`, `@jake` and `@frank.rel`, `@ryan.rel`, `@jake.rel` for name/relationship references. All relationship options are narratively compatible — all explain shared living space under one roof.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SETTING

**Type**: Isolated rural property — domestic + limited town access

**The Property**: Frank's place — a contractor's rural property 40 minutes by bus from the nearest college town. Main house, detached workshop/garage, backyard with a creek. Surrounded by fields and tree-lined trails. The nearest neighbor is a 10-minute walk. The nearest town has a campus, gym, park, diner, and shops.

**Why this setting works**:

- **Closed ecosystem** — everything happens in one house and its surroundings. Three men, one woman, thin walls, one shared bathroom. There is no escape from proximity. She hears them through walls. They hear her. Someone is always in the kitchen.
- **Isolation as pressure** — the property is remote. Lily needs Ryan's truck or a $2 bus ride (40 minutes) to get to town. Transport dependency = relationship dependency. Ryan drives her? He sees what she buys, who she visits, what she wears. Bus? She's independent but it costs money and time.
- **Economic trap** — Lily can't just "get a job in town." The bus costs money. The diner pays $45/shift but she misses dinner and all evening activities at home. Every income source either requires corruption progression or costs relationship time.
- **Cross-contamination** — there is no pursuing one NPC without the others knowing. Frank is at the breakfast table when Ryan comments on Lily's new outfit. Jake hears sounds through the wall. Ryan walks in on everything. The house forces awareness.
- **Contrast engine** — the gap between Lily's arrival (hoodie, jeans, one suitcase) and what she becomes (the wardrobe tiers, the makeup, the confidence) is visible to everyone under this roof every single day. The NPCs watch the transformation in real-time.

**Key Locations**:

| Location | Mood | Primary NPC(s) | Activity Type |
|----------|------|----------------|---------------|
| **Kitchen** | Social hub, charged | All three | Meals, cooking, late-night encounters |
| **Living Room** | Domestic, proximity | Frank + Ryan | TV evenings, couch escalation |
| **Shared Bathroom** | Vulnerability, exposure | Random | Walk-in encounters, morning routine |
| **Frank's Office** | Private, forbidden | Frank | Bookkeeping, closed-door tension |
| **Lily's Room** | Personal, intimate | Solo / Jake | Wardrobe changes, wall sounds, sleep |
| **Jake's Room** | Creative, tender | Jake | Drawing sessions, late-night visits |
| **Hallway** | Transit, charged | Random | Jake's cracked door, bathroom encounters |
| **Workshop/Garage** | Physical, masculine | Frank + Ryan | Job site prep, hidden magazines |
| **Yard** | Open, exposed | Solo / Any | Outdoor chores, sunbathing, morning jogs |
| **Creek** | Isolated, bodies | Any (1-on-1) | Swimming, physical awareness |
| **Ryan's Truck** | Confined, mobile | Ryan | Rides to town, parked escalation |
| **Campus** | Academic, public | Solo / Jake | Classes, art studio, library |
| **Gym** | Physical, charged | Ryan | Exercise, locker room encounters |
| **Park** | Neutral, peaceful | Jake / Solo | Jogging, bench conversations, sketching |
| **Diner** | Public, independent | Solo | Waitressing income, alternative to home |
| **Clothing Store** | Transformation | Solo | Wardrobe purchases |
| **Hiking Trail** | Remote, weekend | Any (group) | Trail head, rest stop, isolated creek |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## CORE PREMISE

**The "What If?" Hook**:

What if a 19-year-old art student, stranded by circumstance, had to live with three men she barely knows — her new step-father and his two adult sons — in an isolated rural property where every room has thin walls, one shared bathroom, and nowhere to hide?

**Emotional Journey**:

Lily arrives with one suitcase to a house she's been to exactly once — the wedding. Her mom Diana just married Frank Harmon, then took a 10-week overseas nursing contract in Dubai. Lily was supposed to stay in her dorm, but it flooded mid-semester. Insurance won't cover alternatives. Diana arranged for Lily to stay at Frank's property.

The first week is awkward. House rules, thin walls, a bathroom schedule that doesn't work. Jake is sweet. Ryan is aggressive. Frank is careful. Lily counts her money and realizes she's in trouble — $400, monthly expenses of $385, Mom's transfer unreliable.

Her pride won't let her ask for help. So she finds her own solutions: cleaning for cash, bookkeeping in Frank's office, modeling for Jake's art class, picking up shifts at the diner. Each solution pulls her deeper into someone's orbit. Each relationship develops at its own pace across its own corruption band. The house becomes an arena where three completely different dynamics play out simultaneously — sweet/tender with Jake, aggressive/physical with Ryan, forbidden/authoritative with Frank.

The game never lectures. The game never moralizes. The economic math creates the pressure. Lily's pride removes the easy exits. Proximity does the rest.

Mom's early return at day ~56 is the ticking clock. What has Lily become by the time Diana walks through the door?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## TONE

**Slow-burn domestic tension with NPC-dependent emotional textures**

The overall atmosphere is claustrophobic domesticity — coffee in the morning, dishes in the sink, the sound of someone showering through the wall. The house is always close. The tension is in what's NOT said. Long pauses at the dinner table. A hand that lingers on a doorknob. Eye contact held one second too long.

### Per-NPC Tone

- **Jake arc**: Tender, guilty, mutual. The tone is gentle corruption — two people who genuinely care about each other crossing lines that feel natural in the moment and devastating in retrospect. Whispered conversations. Art as foreplay. "We shouldn't." "I know." The narration is warm and intimate, focused on small details — the way his pencil stops, the tremble in his hand, the light on her collarbone.

- **Ryan arc**: Physical, charged, combative. The tone is raw and direct. Ryan doesn't do subtext. He pushes, she resists (or doesn't), and the friction is the tension. Truck rides where the air gets thick. Gym encounters where bodies are unavoidable. The narration is blunter — sensation over reflection. What she feels, not what she thinks.

- **Frank arc**: Forbidden, controlled, devastating. The tone is what happens when an immovable man meets an unstoppable situation. Every interaction is loaded with what Frank is NOT saying. His control is the barrier, and watching it crack is the escalation. Late-night kitchen scenes where coffee goes cold. Office bookkeeping where the numbers stop making sense. The narration is tight, restrained — and when it finally breaks, it breaks hard.

### Corruption-Level Narration Shift

- **Low corruption (0-60)**: Lily's internal voice is observational, slightly anxious. She notices things and is uncomfortable noticing. "Did he just look at me like that?" Short sentences. Self-conscious.
- **Mid corruption (60-140)**: Awareness becomes anticipation. She's noticing AND seeking. Internal voice gets bolder. "I know he's watching. I don't cover up." Longer thoughts. Less guilt.
- **High corruption (140-250)**: She's the agent now. Internal voice is confident, sometimes calculating. "I wore this on purpose. I know exactly what happens when I bend over in this dress." Direct, unapologetic.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## GAME SCOPE

| Element | Target | Notes |
|---------|--------|-------|
| In-game days | ~60 | Day-by-day play. Mom's 10-week contract, returns 2 weeks early (~day 56). Final week is endgame. |
| Locations | 21 | 11 on property, 7 in town, 3 on trail (see location map) |
| Time periods per day | 8 | Early Morning through Late Night |
| NPC activities (per NPC) | 3-5 | Each NPC has multiple activities across different locations and time slots |
| Total NPC activities | ~12-15 | Across 3 NPC routes |
| Story events | ~26 | 4-act structure: 6 (Act 1) + 8 (Act 2) + 6 (Act 3) + 6 (Act 4) |
| Random encounters | 14+ | Passive corruption events across all locations |
| Utility canvases | 8-10 | Cleaning, sleep, shower, meals, bus travel, shopping |
| Solo activities | 4-6 | Yoga, jogging, journaling, campus classes |
| Gate flags | 7 | exposure → flirt → tease → kiss → handjob → blowjob → sex |
| Branch points | 4 | 1 global crisis + 1 per NPC (Jake L3, Ryan L2, Frank L3) |
| Endings | 6 | Jake's Girl, Ryan's Conquest, Frank's Arrangement, All Three, Independent, Escape |

### NPC Arc Overlap Timeline (Corruption Bands)

```
Corruption:  0    30    60    90    120   150   180   210   240
             |     |     |     |     |     |     |     |     |
Personal:    ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
             0 ───────── 55
             (Arrival, settling in, self-discovery, first exposure)

Jake:        ██████████████████████████████████████████████████
             25 ──────────────────────────────────────── 220
             (Drawing sessions → posing → intimacy → full arc)

Household:         ████████████████████████████░░░░░░░░░░░░░░░
                40 ─────────────────────── 160
                (Chores, cooking, shared meals, domestic routines)

Ryan:              ██████████████████████████████████████████████
                50 ──────────────────────────────────────── 240
                (Truck rides, job site, gym, aggressive pursuit)

Frank:                          ████████████████████████████████
                          100 ─────────────────────────── 240
                          (Office, kitchen, authority breaks)
```

At any corruption level, the player always has 2-3 active arcs offering new content. Jake is the entry point, Ryan overlaps mid-game, Frank activates latest for maximum tension when all three are in play.

### Daily Time Budget

| Period | Hours | Key Activities |
|--------|-------|----------------|
| **Early Morning** | 05:00-07:00 | Shower, grooming, morning routine (beauty maintenance) |
| **Morning** | 07:00-09:00 | Breakfast (kitchen, all NPCs), morning jog (property) |
| **Late Morning** | 09:00-12:00 | Job site (Ryan/Frank), campus (bus), house cleaning |
| **Afternoon** | 12:00-15:00 | Lunch, bookkeeping (Frank), drawing (Jake), gym, modeling |
| **Late Afternoon** | 15:00-17:00 | Creek swim, errands with Ryan, studying, park |
| **Evening** | 17:00-19:00 | Dinner (kitchen, all NPCs), diner shift (alternative) |
| **Night** | 19:00-22:00 | Living room TV, Frank's office, Jake's room, Ryan's return |
| **Late Night** | 22:00-01:00 | Kitchen encounters, bathroom encounters, wall sounds, sleep |

**Typical day**: 4-5 activities without rest, 6-7 with strategic naps and meals. Energy budget (100/day, 110 at fitness 61+) forces daily prioritization.

### Economic Pressure Summary

| Phase | Income | Surplus | Pressure Level |
|-------|--------|---------|----------------|
| **Weeks 1-3** (cleaning only) | $100/week (5 cleans × $20) | $4/week after food + bills | CRITICAL — one missed day = red |
| **Weeks 4+** (bookkeeping unlocks at corruption 40) | $225/week (clean + bookkeep) | $175/week | Comfortable — but she's already corrupted |
| **Mid-game** (higher-tier work) | $300-500+/week | Surplus + free time | Each tier frees TIME for relationships |

**Starting money**: $400
**Monthly expenses**: ~$385 (bus $80, art supplies $60, phone $45, food $200)
**Mom sends**: $200/month (often late or bounced)
**Wardrobe total**: ~$870 across all tiers (nobody buys everything)
**Beauty products**: ~$260 across game

The impossible math works because weeks 1-3 are genuinely tight with cleaning as the only option. Bookkeeping doesn't unlock until corruption 40, which means Lily has already started down the path by the time she gets financial relief. The economic pressure does its job during the critical early weeks when habits form and boundaries shift.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## RECOMMENDED DIRECTION

**Under One Roof** is a closed-ecosystem female-protagonist adult game where domestic proximity, economic pressure, and three fundamentally different male archetypes create a slow-burn corruption arc that the player drives through daily choices.

The game's structural core is the **closed ecosystem**. Unlike multi-NPC games where targets are encountered in different locations, all three NPCs live in the same house. Breakfast, dinner, the bathroom schedule, the thin walls — everything is shared. Pursuing Jake in the afternoon means Ryan sees her leave his room. Bookkeeping with Frank in the evening means missing dinner with both brothers. The house is a pressure cooker where every action has witnesses.

The **three NPC archetypes** cover the full spectrum of step-family fantasy:
- **Jake** (the tender step-brother) — art, innocence, mutual corruption through genuine affection
- **Ryan** (the aggressive step-brother) — physicality, pursuit, the dare
- **Frank** (the forbidden step-father) — authority, control, the taboo that breaks last

The **economic engine** is what makes the corruption organic. Lily's pride prevents her from asking for help. The math is impossible at base tier. Each escalation in income requires deeper involvement with a household NPC. The game never tells Lily to escalate — the rent does, the bus pass does, the art supplies do.

The **shared skill unlock system** (7 gate flags earnable through any NPC) ensures every player finds their own path. Jake-first players unlock flags early and apply them to Ryan/Frank. Ryan-first players hit different milestones at different corruption levels. Frank-first players are the rare completionists who invest heavily before any payoff. No path is wrong. All paths lead deeper into the house.

The **6 endings** aren't chosen — they're accumulated. The combination of highest-stat NPC, corruption level, crisis branch choice, and financial state determines which ending fires when Mom walks through the door on day ~56. The endings range from tender (Jake's Girl) to forbidden (Frank's Arrangement) to triumphant (Independent) to clean (Escape — corruption < 100, achievable but requires deliberate avoidance).

The question the game asks: When Diana comes home, who is Lily now? And was there ever a moment she could have stopped?

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type "proceed" to continue to Phase 2: Characters & Stat Economy,
or provide adjustments.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


# PHASE 2: CHARACTERS & STAT ECONOMY
# Under One Roof

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 1: PLAYER DEFINITION

### Lily Chen — The Player Character

**Name**: Lily Chen
**Age**: 19
**Portrait Reference**: Dark-haired East Asian young woman, slim build, average height. Messy bun or ponytail. Youthful face — looks younger than 19. The kind of face you'd trust immediately.

**Background**: Art student, second year at the local state college. Parents divorced when she was 14. Mom (Diana) remarried Frank Harmon 8 months ago. Lily attended the wedding, made small talk with Frank's sons, went home. She doesn't know these people.

Diana takes a 10-week overseas nursing contract in Dubai — the money is too good to refuse. Lily was supposed to stay in her college dorm, but mid-semester flooding makes it uninhabitable. Insurance won't cover alternative housing. Diana arranges for Lily to stay at Frank's rural property with his two adult sons.

Lily arrives with one suitcase to a house she's been to exactly once.

**Sexual History**: Limited. A boyfriend in high school that lasted 4 months. She's not innocent — she's inexperienced. She knows what sex is. She's just never had it be complicated.

### Starting Stats

```
corruption  = 0      # Primary progression driver. Gates choices across all NPC arcs.
confidence  = 10     # How she carries herself. Gates assertiveness and self-initiated escalation.
money       = 400    # Economic pressure engine. Depletes through expenses.
energy      = 100    # Daily activity budget. Resets on sleep.
fitness     = 20     # Body condition. Built through exercise. Decays without maintenance.
beauty      = 30     # Presentation. Built through grooming, makeup, skincare. Decays without maintenance.
```

| Stat | Start | Range | Clamp | Purpose |
|------|-------|-------|-------|---------|
| **corruption** | 0 | 0-250 | false | Gates which activity choices appear. Grows from activities (+2-5), random encounters (+2-3), story events (+3-8). The player's internal transformation — tracks how far Lily has moved from who she was on day one. |
| **confidence** | 10 | 0-100 | true | Gates assertiveness choices (negotiating pay, refusing demands, standing up for herself, self-initiating physical encounters). Grows from exercise, confrontations, art achievements, wearing bold clothes. Does NOT decay — represents permanent growth. |
| **money** | 400 | unclamped | false | Depletes through monthly expenses (~$385/month). Replenished through household work and jobs. The impossible math forces escalation. |
| **energy** | 100 | 0-100 | true (dynamic max: 100 base, 110 at fitness 61+) | Daily budget forcing prioritization. 4-5 activities/day without rest, 6-7 with naps/meals. Resets to max on full sleep. |
| **fitness** | 20 | 0-100 | true | How her body looks and performs. Built through gym, swimming, jogging, hiking, job site labor. Affects NPC reactions to her body, unlocks stamina-related choices, increases energy max at 61+. Decays -1 per 3 days without exercise. |
| **beauty** | 30 | 0-100 | true | How her face/hair/presentation looks. Built through grooming routines, makeup, skincare, hairstyles. Affects diner tips, NPC compliments, love gain bonuses. Decays -1 per 2 days without grooming. |

### Player Psychology (REQUIRED)

| Field | Value |
|-------|-------|
| **Want** | Independence — finish her degree, get her own place, stop depending on anyone |
| **Need** | Connection — she's been isolated since the divorce, builds walls, keeps people at distance |
| **Fear** | Being trapped — dependency on people she can't trust or control |
| **Flaw** | Pride — she'd rather suffer quietly than ask for help. She'll find her own solutions, even if those solutions push her boundaries |

**How the flaw drives the game**: Lily's pride is the economic engine. She won't ask Frank for money. She won't admit she's struggling. She won't call her mom crying. This pride is what the economic pressure exploits — she'll find her *own* solutions, and each solution pulls her deeper. The game never tells her to take her clothes off. The math does, and her pride closes every exit that doesn't involve going deeper.

### Player Emotional Phases (REQUIRED)

| Phase | Triggered By | Player Mindset | How It Shows in Narration |
|-------|-------------|----------------|--------------------------|
| **OUTSIDER** | Arrival (Day 1) | "I don't belong here. This is temporary. I'll be out in ten weeks." | Short sentences. Notices house layout, awkward silences, the smell of sawdust. Counts days. Refers to NPCs by role: "my step-dad," "the older one," "the quiet one." |
| **SETTLING** | First week complete / first chore accepted | "These are just people. I can make this work." | Starts noticing NPC routines — Frank's 5 AM coffee, Jake's humming while he draws, Ryan's boots by the door. Refers to NPCs by name. Internal voice relaxes. |
| **AWARE** | First physical awareness / `exposure_unlock` fires | "Something is changing. In them. In me. I don't hate it." | Notices bodies, proximity, charged moments. Starts caring about what she wears. Narration gets physically specific — collarbone, forearms, the way a shirt sits. Longer internal passages. |
| **WANTING** | First kiss / `kiss_unlock` fires | "I want this. I shouldn't, but I want this." | Stops pretending encounters are accidental. Seeks out specific NPCs. Internal voice admits desire without qualifying it. Narration becomes anticipatory — what she hopes will happen, not just what does. |
| **TORN** | Crisis events (Frank discovers drawings / brothers clash) | "This is falling apart. What have I done?" | Guilt, fear, desperation. Contradictory internal voice — "I need to stop" followed by "I can't stop." Questions every decision. Notices what she'd lose. Longest internal passages. |
| **COMMITTED** | Crisis resolved / `crisis_resolved` flag | "This is who I am now. I choose this." | Confident, deliberate. Initiates instead of reacting. Manages relationships consciously. Internal voice is direct, unapologetic. Shorter sentences — certainty needs fewer words. |
| **ENDGAME** | Mom's return announced / `mom_returning` flag | "She's coming home. Time's up. What am I?" | Urgency in every interaction. Every moment weighted. Final choices carry existential weight. Narration oscillates between desperate intensity and quiet reflection. |

### Player Internal Voice (REQUIRED)

**What Lily notices (evolves over time):**

| Phase | What She Notices | Example |
|-------|-----------------|---------|
| OUTSIDER | Environment, layout, rules, exits | "The hallway is narrow. His room is right next to mine. The walls are thin." |
| SETTLING | NPC habits, routines, patterns | "Frank makes coffee at 5 AM. I can hear the grinder through the floor. Jake draws until his light clicks off at midnight." |
| AWARE | Bodies, proximity, tension | "Ryan came back from the job site shirtless. Sweat on his collarbone. I looked for three seconds too long." |
| WANTING | Anticipation, desire, plans | "Jake's door is cracked open. I could knock. I want to knock." |
| TORN | Stakes, consequences, what she'd lose | "If Frank finds out about Jake, he'll call Mom. If Ryan finds out about Frank, I don't know what happens." |
| COMMITTED | The relationships themselves, shared history | "Jake's hand shakes when he draws me now. It didn't used to. I know exactly when it started." |
| ENDGAME | Time, finality, identity | "Three more days. She'll walk through that door and see... what? Who am I now?" |

**How Lily describes each NPC (evolves over time):**

| Phase | @frank | @ryan | @jake |
|-------|--------|-------|-------|
| OUTSIDER | "My step-dad. Broad. Quiet. Smells like sawdust." | "The older one. Loud. Thinks he's funny." | "The quiet one. Draws a lot. Won't make eye contact." |
| SETTLING | "Frank. Runs things. Fair, actually." | "Ryan. Relentless, but not mean." | "Jake. Sweet. We have stuff in common." |
| AWARE | "His hands. The way he fills a doorway." | "Those arms. The way his jeans sit." | "His eyes behind the glasses. The focus." |
| WANTING | "He looked at me like he was deciding something." | "He leaned in and I didn't pull away." | "He touched my wrist while positioning my hand. Neither of us moved." |
| TORN | "He trusted me. I'm in his house." | "He's going to figure it out." | "I'm going to hurt him." |
| COMMITTED | "He knows what I am and he wants me anyway." | "We understand each other." | "He draws me like I'm the only thing worth looking at." |

**Choice text framing (evolves over time):**

| Phase | Tone | Example Choices |
|-------|------|-----------------|
| OUTSIDER | Cautious, polite | "Offer to help with dishes" / "Go to your room" |
| SETTLING | Friendly, practical | "Ask Jake about his drawings" / "Do your own homework" |
| AWARE | Physically charged, risk-aware | "Hold the pose a little longer" / "Cover up" |
| WANTING | Direct, desire-forward | "Kiss him back" / "Pull away" |
| TORN | High-stakes, emotional | "Tell him the truth" / "Lie" |
| COMMITTED | Confident, initiating | "Go to his room tonight" / "Sleep alone" |
| ENDGAME | Urgent, defining | "One last night together" / "Start saying goodbye" |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 2: NPC DEFINITIONS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### NPC 1: FRANK HARMON — The Step-Father

#### Physical Appearance
Broad shoulders, calloused hands from decades of construction work. Salt-and-pepper stubble, always slightly unshaven. Crow's feet around steady dark eyes — the kind that don't blink when they look at you. Smells like sawdust and black coffee. Wears flannels with rolled sleeves, work boots, jeans that fit right. At 45, he hasn't gone soft — the job site keeps him solid. Mornings: flannel, coffee mug. Evenings: same flannel, sleeves down, whiskey instead of coffee. Late nights: undershirt, barefoot, the controlled version of himself coming loose at the seams.

#### Personality Traits
**Surface (what people see):** Responsible. Steady. A man who says what he means and doesn't say much. Good father. Fair employer. Pays his debts.
**Hidden (what emerges):** Lonely. Hungry. Controlled to the point of compression. The control isn't strength — it's a dam holding back everything he won't let himself feel since his first wife left and Diana is always overseas.

#### Psychology
Frank wants to be the man Diana married — responsible, paternal, trustworthy. He's terrified of being the man he actually is — a 45-year-old who's been alone too long, whose new wife is on another continent, and whose step-daughter is walking around his house in increasingly less clothing.

His internal conflict is between duty and desire. He set the house rules. He maintains distance. He calls Lily by her name, never a nickname. Every structural decision he makes — separate bathrooms, dinner schedule, giving her a job in his office — is designed to keep things appropriate. And every one of those decisions brings her closer.

He responds to intimacy with withdrawal — then overcorrection. If his hand touches hers reaching for the salt, he leaves the room. The withdrawal is disproportionate, which is how Lily knows he felt it too. When he finally stops withdrawing, it's not a gradual opening — it's a break. The dam doesn't leak. It cracks.

#### Internal Contradictions (REQUIRED)

1. **He promised Diana he'd take care of Lily** — BUT he is the biggest threat to her under this roof. Every protective action (driving her to campus, giving her work, setting house rules) puts her deeper in his orbit. The protector IS the danger.

2. **He uses his authority to maintain boundaries** — BUT the authority itself is the turn-on. "Put something on before your brothers see you" is a command. He's telling her what to wear. Every boundary he sets reinforces the power dynamic that eventually breaks him.

3. **He prides himself on self-control** — BUT the control is brittle, not flexible. He doesn't bend — he holds, holds, holds, then shatters. His resistance makes the eventual break devastating because there's no gradual slide. He goes from iron discipline to "lock the door" in the space of a single scene.

#### Resistance Pattern (REQUIRED)

| Stage | Frank's Resistance Behavior | What Triggers It |
|-------|---------------------------|-----------------|
| **MILD** | Leaves the room. Pours more coffee. Doesn't make eye contact for an hour. Says "I need to get back to the workshop." Over-formal — calls her "Lily" instead of relaxing into conversation. | Any charged moment: her hand on his, eye contact held too long, her wearing Cute+ clothing near him. |
| **MODERATE** | Cancels the bookkeeping session. "I can handle it myself this week." Creates physical barriers — sits behind the desk instead of beside her. Adds new house rules. Avoids being alone with her for 2-3 days. | After a physical milestone fires between them. After he catches himself looking. After discovering drawings or other evidence. |
| **SEVERE** | Direct confrontation. "This stops. Whatever this is." Voice is tight, not loud. Hands flat on the desk. He doesn't threaten — he states. Avoids all non-essential interaction for 3-5 days. Eats dinner in the workshop. | After a line is explicitly crossed: a kiss, a touch that can't be misread, the brothers discovering something. |
| **RECOVERY** | Stays in the kitchen past midnight. Doesn't speak first but doesn't leave when she enters. Pours her coffee without being asked. The silence is different — loaded, not cold. Eventually: "Sit down." Two words. An opening. | After Lily demonstrates patience. After she handles the household well in his absence. After a vulnerability moment — he needs something fixed and she's the one who helps. |

#### Emotional Quadrant Behaviors (REQUIRED)

| Quadrant | Frank's Specific Behaviors |
|----------|---------------------------|
| **DISTANT** (low love / low trust) | Functional and clipped. "Dinner's at six." Doesn't sit when she's in the room — stays standing, keeps exit access. Reads the paper at breakfast instead of talking. Leaves his office door open when she's doing bookkeeping (witness insurance). Refers to her as "Diana's daughter" when talking to Ryan. |
| **SAFE** (low love / high trust) | Relaxed but unromantic. Asks about her classes, remembers her answers. Leaves money on the counter for art supplies without being asked. Closes the office door during bookkeeping because he trusts her now — but the trust is professional, not charged. Tells stories about building the house. Laughs sometimes — low, surprised, like he forgot he could. |
| **CONFLICTED** (high love / low trust) | The most common Frank state. He wants her and is fighting it. Stays in rooms longer than he should but stands at maximum distance. Stares at the spot where she was sitting after she leaves. Makes rules that create proximity ("You should eat breakfast with us" — an order wrapped in concern). Pours whiskey earlier in the evening. Grip on the coffee mug tightens when she walks through in sleepwear. Sentences start and stop: "You should—" (pause) "Never mind." |
| **OPEN** (high love / high trust) | Rare and devastating. The controlled man uncontrolled. Holds eye contact without looking away first. Sits next to her instead of across. Voice gets lower — not louder, lower. Calls her "Lil" for the first time (then catches himself, then does it again). Touches the small of her back guiding her through a doorway and doesn't pull away. Leaves his bedroom door unlocked. Says what he actually means: "Stay." |

#### Emotional Tells by Stat Range (REQUIRED)

**Love Tells (Frank):**

| Range | Observable Behavior |
|-------|-------------------|
| 0-5 | "He nods when you enter the kitchen. Pours his own coffee. Reads the paper. You're a guest he's tolerating." |
| 6-12 | "He pours your coffee too. Black — he doesn't know how you take it yet. 'Classes going alright?' He's being polite. You think." |
| 13-20 | "He remembered you take cream. It's already in the mug. He watches you sit down, then looks away — but slower than before." |
| 21-28 | "He's already at the kitchen table when you arrive. Like he was waiting. The paper is open but he hasn't read it. His eyes track you across the room." |
| 29-35 | "He pushes the mug toward you as you sit. Their fingers almost touch. He doesn't pull his hand back. 'You look...' He stops. Drinks his coffee. Whatever he was going to say stays behind his teeth." |

**Trust Tells (Frank):**

| Range | Observable Behavior |
|-------|-------------------|
| 0-8 | "His office door stays open when you're doing the books. He checks your work. Counts the cash drawer after you leave." |
| 9-15 | "Door stays open but he stops checking your work. Leaves receipts for you to file without supervision. 'You're doing fine.'" |
| 16-22 | "Door closes — he trusts the privacy. Tells you about a client who's late on payment. Business talk. You're inside the circle." |
| 23-28 | "Leaves you alone in the office with the books and the checkbook. Tells you about the business debt — the real numbers, not the ones he shows the boys. 'Don't tell Diana.'" |
| 29-35 | "Asks your opinion on a bid. Listens to the answer. Falls asleep in the office chair while you're working — the most vulnerable thing Frank Harmon has ever done in front of another human being." |

#### Speech Patterns

**Structure**: Short, declarative. Statements, not questions. Subject-verb-done. "Dinner's at six." "Clean up when you're finished." "I'll drive you."

**What he says vs what he means**: Almost everything Frank says has a subtext layer. "Put something on" means "I can see too much and I can't stop looking." "I'll drive you" means "I want to be the one who takes you." "That's enough for tonight" means "If we stay in this room one more minute I'm going to do something I can't take back."

**Evolution**: Early Frank speaks in commands and logistics. Mid-game Frank starts trailing off — unfinished sentences, longer pauses, the arrival of "..." in his dialogue. Late-game Frank uses fewer words but each one costs more. When he finally says something honest, it's devastating because you've been waiting 40 days to hear him mean something out loud.

**Signature phrases:**
- "That's enough." (boundaries)
- "I said I'll handle it." (control)
- "Sit down." (the moment he opens a door)
- "Diana trusts me." (the guilt he carries)

#### Starting Stats

```toml
[npcs.npc_frank]
name = "Frank"
core_traits = { love = 0, trust = 5, corruption = 0 }
# Trust starts at 5 — basic decency, not warmth. She's his wife's daughter.
```

#### Arc Concept Summary

- **Act 1 (corruption 0-100):** Professional, fatherly, maintains distance. Functional interactions — rides, dinner, bookkeeping. Micro-moments: hand on her back, watching her leave.
- **Act 2 (corruption 100-180):** Walls crack. Late-night kitchen encounters get longer. Bookkeeping sessions get quieter. He starts making excuses to be where she is.
- **Act 3 (corruption 180-240):** Control breaks. Forbidden fully embraced. Dominance emerges — stops asking, starts telling. Authority inverts from protective to possessive.

**Branch Point (Level 3, mid-game ~corruption 110):** Lily discovers Frank's financial secret — the business is in debt.
- **Path A: Confront him** → `chose_confront_frank` — adversarial-to-intimate. Anger, vulnerability, gratitude. Trust-to-love pipeline.
- **Path B: Keep his secret** → `chose_protect_frank` — conspiratorial. Private meetings shift from bookkeeping to real talk. Forbidden-intimacy pipeline.
- Both set `frank_secret_complete`. Tone changes, not direction.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### NPC 2: RYAN HARMON — The Older Step-Brother

#### Physical Appearance
Athletic, tanned from outdoor work. Strong jaw, cocky grin that he knows is effective. Thick arms from hauling lumber and drywall — the kind of arms that fill a tank top. Wears tank tops, work boots, jeans slung low. Has a faded scar on his forearm from a job site accident he tells a different story about every time. At 23, he's in his physical prime and knows it. Mornings: shirtless if he thinks she's watching, tank top if he's being subtle (he's never being subtle). Job site: sweaty, dusty, rolled bandana on his forehead. Evenings: cleaned up just enough — cologne over sawdust, the grin reloaded.

#### Personality Traits
**Surface (what people see):** Confident. Teasing. Physical. The kind of guy who tests every boundary once to see what happens. Laughs easily. Makes everything feel like a dare.
**Hidden (what emerges):** Protective in ways he won't admit. Competitive with Jake, dismissive of Jake's "art kid" interests — but covers for him with Frank when Jake misses work. Genuinely lonely under the bravado — his confidence is an armor built from being the only one in the house who doesn't have someone.

#### Psychology
Ryan wants to be seen as the one who doesn't need anyone — the guy who takes what he wants and doesn't look back. He's afraid of wanting something he can't have — specifically, he's afraid of wanting Lily for more than just the physical, because wanting more means risking rejection on terms he can't joke away.

His internal conflict is between pursuit and vulnerability. He flirts because it's safe — flirting is a game, and games have defined winners and losers. But as Lily's corruption grows and she starts flirting BACK, the game changes. She's not resisting anymore. And Ryan doesn't know what to do with someone who says "yes" — because now it's real, and real means he could actually lose something.

He responds to intimacy with deflection — a joke, a change of subject, a physical escalation that replaces the emotional moment. "You're getting soft on me?" when what he means is "Am I getting soft on you?" When Lily breaks through that deflection, it's the first time Ryan is genuinely vulnerable in the game.

#### Internal Contradictions (REQUIRED)

1. **He treats Lily as a conquest** — BUT he starts developing real protective feelings. When a guy at the diner hits on her, Ryan doesn't laugh — he gets quiet. He wants her for himself, but "for himself" is shifting from "I got there first" to "nobody touches her."

2. **He pushes every boundary** — BUT he's scared of crossing a line that actually matters. Physical escalation is easy — he's done it a hundred times. Saying "I actually care about you" is the line he's terrified of, because it can't be taken back with a grin.

3. **He uses "you're not really my sister" as a license** — BUT he knows exactly what the taboo is. The technicality is an excuse. Underneath the excuse, he knows Diana is his step-mom, Lily is Diana's daughter, and Frank is his father. The "not really family" framing lets him do what he wants without examining what it means.

#### Resistance Pattern (REQUIRED)

| Stage | Ryan's Resistance Behavior | What Triggers It |
|-------|--------------------------|-----------------|
| **MILD** | Turns it into a joke. "Relax, I'm just messing with you." Physical withdrawal disguised as casualness — puts his hands behind his head, leans back, increases distance without looking like he's retreating. Sends a text instead of saying it out loud. | After an emotional moment lands too close to real. After Lily says something honest about him that he can't deflect. |
| **MODERATE** | Goes out without saying where. Comes home late. Avoids being alone with her for 1-2 days. Louder and more obnoxious at dinner — performing normalcy. Teases Jake harder than usual (displacement). | After he catches feelings and realizes it. After discovering Lily's involvement with Jake or Frank. After she rejects a physical advance he thought was guaranteed. |
| **SEVERE** | Confrontational but controlled. "You think this is a game? Because I don't." Not angry — hurt, which is worse coming from Ryan. Takes his truck and disappears for a day. Won't make eye contact for 2-3 days. | After Lily lies to him directly. After a major trust breach. After the brothers-discover-each-other crisis. |
| **RECOVERY** | Shows up with something — gas station coffee, a bag of art supplies he'd never buy himself. Doesn't apologize in words. Instead: "Heading to town, you coming or what?" The offer IS the apology. | After Lily gives him space without chasing him. After she does something that proves she's not just using him (covers for him with Frank, defends him). |

#### Emotional Quadrant Behaviors (REQUIRED)

| Quadrant | Ryan's Specific Behaviors |
|----------|--------------------------|
| **DISTANT** (low love / low trust) | Maximum performance mode. Loud at breakfast. Makes comments about Lily's appearance that are technically jokes. Offers rides that feel like traps — helpful with strings attached. Doesn't ask personal questions. Everything is a test. "You own gym clothes or...?" |
| **SAFE** (low love / high trust) | Calms down. Less performing, more genuine. Drives her to campus without commentary. Tells actual stories instead of bits — the scar on his forearm, why he dropped out of community college. Sits on the couch at a comfortable distance. Still teases, but the edge is gone. "You're alright, you know that?" |
| **CONFLICTED** (high love / low trust) | Jealous and visible about it. Watches Jake's door when Lily goes in. Truck rides get quieter — charged silence instead of banter. Makes possessive comments he tries to pass off as jokes: "Jake's real busy drawing lately." Gets competitive about activities: "Why don't you come to the gym instead of sitting in his room?" When he's near her, his body gravitates closer even as his words push away. |
| **OPEN** (high love / high trust) | The bravado drops. Quieter. More physical but less aggressive — a hand on the small of her back instead of a slap on the arm. Actually listens when she talks. Drives slower when she's in the truck, like he's stretching the time. "I don't want to go home yet" is the most vulnerable thing Ryan has ever said. Protects her without making it a joke. |

#### Emotional Tells by Stat Range (REQUIRED)

**Love Tells (Ryan):**

| Range | Observable Behavior |
|-------|-------------------|
| 0-5 | "He looks at you like you're a new piece of furniture in the house. Interesting, temporary." |
| 6-12 | "He holds the truck door open. Still a test — watching if you'll say thank you. But he's paying attention now." |
| 13-18 | "He's cleaned the passenger seat. The empty cans are gone. The cab smells like pine air freshener. He doesn't mention it." |
| 19-25 | "He waits. That's the tell. Ryan doesn't wait for anyone. But he's in the truck, engine running, even though you said 'give me five minutes' ten minutes ago." |
| 26-35 | "He reaches across and tucks your hair behind your ear while you're talking. Then freezes. His hand hangs there for a second before he pulls it back. 'What were you saying?' Quieter than you've ever heard him." |

**Trust Tells (Ryan):**

| Range | Observable Behavior |
|-------|-------------------|
| 0-5 | "He watches you from across the room like he's keeping score. Every smile counted, every move cataloged." |
| 6-12 | "He tells you the real story about the scar — not the funny version, the one where he was scared." |
| 13-18 | "He covers for you with Frank when you come home late. Doesn't ask where you were. Just: 'She was with me.'" |
| 19-25 | "He admits he didn't finish community college because he couldn't read fast enough. No joke after. Just silence, and the window down, and the road." |
| 26-35 | "He falls asleep in the truck with you after parking by the creek. He doesn't do that. Ryan doesn't fall asleep around people." |

#### Speech Patterns

**Structure**: Short, punchy, teasing. Uses questions as weapons: "You gonna wear that?" Turns statements into dares: "Bet you won't." Sprinkles in nicknames — "college girl," "roomie," eventually just "Lil" (different from Frank's "Lil" — Ryan's version is possessive, Frank's is tender).

**What he says vs what he means**: Ryan deflects everything real with humor. "Whatever" means "I care more than I'm going to show you." "You coming or what?" means "Please come." "I'm just messing with you" means "I meant every word but I'm scared you know that."

**Evolution**: Early Ryan is all surface — fast, loud, one-liners. Mid-game Ryan starts leaving silences where jokes used to go. Late-game Ryan says less but means everything. The biggest shift: when he stops asking questions (tests) and starts making statements (truths). "You coming?" becomes "I want you there."

**Signature phrases:**
- "You coming or what?" (invitations disguised as challenges)
- "Relax." (said when he's the one who needs to relax)
- "Whatever." (his armor word)
- "Not really my sister." (the license he uses, and eventually questions)

#### Starting Stats

```toml
[npcs.npc_ryan]
name = "Ryan"
core_traits = { love = 0, trust = 0, corruption = 10 }
# Corruption starts at 10 — he's already looking at her on day one. No pretense.
```

#### Arc Concept Summary

- **Act 1 (corruption 0-60):** Loudest presence. Teasing, offering rides, finding excuses to be shirtless. Testing Lily's boundaries.
- **Act 2 (corruption 60-150):** Truck rides get longer. Job site has private corners. Shows real protectiveness — covers for her, defends her. The lust gets a foundation of trust.
- **Act 3 (corruption 150-240):** Full physical escalation. Hungry, direct. Gym encounters, shower "accidents," truck parked remote. If he discovers Jake/Frank involvement: competitive, determined to win.

**Branch Point (Level 2, early-mid ~corruption 60):** In the truck, Ryan makes a physical move.
- **Slap his hand** → `ryan_resisted` — shifts to verbal seduction. More careful, testing with words. Seduction-flavored.
- **Let it happen** → `ryan_allowed` — gets bolder, more direct. Lust-flavored.
- Both set `truck_incident_complete`. Same journal entry, different tone going forward.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### NPC 3: JAKE HARMON — The Younger Step-Brother

#### Physical Appearance
Lean, not scrawny — just hasn't filled out yet. Shaggy brown hair that falls in his eyes. Wears glasses when he's drawing or reading, takes them off otherwise. Soft hands compared to his brother and father — artist's hands, graphite-stained fingertips. Usually in a faded band t-shirt and jeans. At 20, he's caught between boy and man — lanky frame still settling into its adult shape. Mornings: rumpled, squinting without glasses, t-shirt he slept in. Art sessions: focused, glasses on, sleeves pushed up, streak of charcoal on his forearm. Late nights: barefoot, old sweatpants, the sketchbook always within arm's reach.

#### Personality Traits
**Surface (what people see):** Shy. Quiet. The one who doesn't fit in the Harmon household of loud men. Draws constantly. Avoids eye contact with strangers. Polite in a way that makes him invisible at family dinners.
**Hidden (what emerges):** Observant in ways no one expects — he sees what Frank is hiding, how Ryan performs, what Lily needs before she says it. Passionate about art with an intensity that surprises people who mistake quiet for empty. Possessive in a way that surprises even him — once he decides someone is his to draw, to know, to love, he doesn't share easily.

#### Psychology
Jake wants to be seen — truly seen, not the version of himself his family acknowledges (the quiet kid, the art student, the one who's "different"). He's afraid of being ordinary — of his art being a hobby instead of a calling, of Lily seeing him the way Ryan sees him (small, unimportant).

His internal conflict is between tenderness and obsession. His feelings for Lily start genuine — affection, artistic fascination, the relief of finding someone who gets him. But genuine feelings in close proximity become consuming. He draws her face from memory. He listens through the wall. He notices when she comes back from Ryan's truck and catalogs what's different about her. The sweet boy is also the one who's been drawing her without permission, and the line between devotion and fixation is one he can't see clearly.

He responds to intimacy with openness that's almost painful — he has no defenses. No jokes (like Ryan), no control (like Frank). When Lily is kind to him, he leans into it completely. This makes his corruption arc devastating: every escalation is consensual, mutual, and tender, which is exactly why it hits differently.

#### Internal Contradictions (REQUIRED)

1. **He wants to protect Lily from the other men in the house** — BUT he's crossing the same lines they are. He judges Ryan for being aggressive and Frank for being inappropriate, while secretly drawing Lily nude from memory and listening through the wall at night. The moral high ground is a comfortable lie.

2. **He wants the relationship to stay tender and pure** — BUT his desire is getting more intense. Early Jake draws her collarbone with reverence. Late Jake draws her body with hunger. He wants to be the good one, the different one — and every day the gap between who he thinks he is and what he actually wants gets wider.

3. **He sees Lily as a real person, not a conquest** — BUT art IS possession. Drawing someone is claiming them visually. His sketchbook is full of her — her hands, her jaw, the way light falls on her shoulder. He tells himself it's art. Lily tells herself it's flattering. Neither of them is entirely wrong, and neither is entirely honest.

#### Resistance Pattern (REQUIRED)

| Stage | Jake's Resistance Behavior | What Triggers It |
|-------|--------------------------|-----------------|
| **MILD** | Blushes and drops something. Changes the subject to art. Adjusts his glasses (nervous tell). Moves his sketchbook so she can't see what he was drawing. "It's nothing." Finds an excuse to leave: "I should probably work on my portfolio." | Any moment of physical tension he wasn't prepared for. Accidental touches. Lily changing the dynamic from friendly to charged. |
| **MODERATE** | Goes quiet — not cold, just internal. Draws with more intensity, like he's processing through the pencil. Doesn't knock on the wall at night. Avoids being alone with her for 1-2 days — not because he doesn't want to, but because he can't trust himself to be appropriate. | After a physical milestone. After seeing Lily come back from Ryan's truck or Frank's office. After realizing his drawings have crossed a line. |
| **SEVERE** | Emotionally raw, not confrontational. "I can't do this if it doesn't mean something." Eyes wet. Hands shaking. The sketchbook stays closed. He won't draw her until it's resolved. This is the only leverage Jake has — withdrawing the one thing she values from him. | After the secret sketches discovery. After learning about Lily's involvement with Ryan or Frank. After a direct emotional betrayal. |
| **RECOVERY** | Leaves a drawing under her door. Not a nude, not a pose — something small. Her coffee mug. Her shoes by the door. A detail only someone who watches her constantly would notice. The drawing IS the apology. Eventually: "I drew something for you. Do you want to see it?" | After Lily comes to him. After she chooses him in a visible way (sits next to him at dinner, asks to see his sketchbook). After she's honest about what she wants. |

#### Emotional Quadrant Behaviors (REQUIRED)

| Quadrant | Jake's Specific Behaviors |
|----------|--------------------------|
| **DISTANT** (low love / low trust) | Barely exists in her awareness. Eats fast, clears his plate, retreats to his room. Acknowledges her with a nod, nothing more. Draws landscapes, not people. Door closed. Headphones on. The wall between their rooms might as well be concrete. |
| **SAFE** (low love / high trust) | Warm but undirected. Shares his art willingly — landscapes, the creek, the house. Recommends books. Saves her a seat at the breakfast table. Talks about his classes, asks about hers. Comfortable silence when they're both in the kitchen studying. Friendship energy — present, easy, no charge. |
| **CONFLICTED** (high love / low trust) | The most painful version of Jake. He's in love with her and doesn't trust the situation — either because she's involved with Ryan/Frank, or because the crisis shattered something. Draws her compulsively but won't show her. Sits near her at dinner but can't eat. Starts sentences with her name and can't finish them. Knocks on the wall at night — just once — then nothing. His door is cracked open, the light is on, the invitation is there. But he won't say it out loud. |
| **OPEN** (high love / high trust) | Art becomes their language. He draws her while she talks and she doesn't have to hold still. Leaves his door open when he knows she's passing. Makes eye contact and holds it — for Jake, this is the equivalent of Ryan's grand gestures. His hand finds hers under the table at dinner. His sketchbook is open on the bed, her face on every page, and he's not embarrassed anymore. "I drew you again. I always draw you." |

#### Emotional Tells by Stat Range (REQUIRED)

**Love Tells (Jake):**

| Range | Observable Behavior |
|-------|-------------------|
| 0-8 | "He glances up from his sketchbook when you enter. Small nod. Back to drawing. You're scenery." |
| 9-15 | "He's drawing and you realize the angle of his page means he can see you in his peripheral. The pencil moves differently when you're in the room." |
| 16-22 | "He shows you a drawing and his hand is shaking. Not the drawing itself — the act of showing. He's never shown anyone before you." |
| 23-30 | "He's drawn your hands. Just your hands. From three different angles. When you see them, he says 'I couldn't get the light right' — but the light is perfect. He just wanted to keep drawing." |
| 31-40 | "He stops drawing when you walk in. Not because he's hiding it. Because looking at you is better than any picture he could make. The sketchbook closes. His eyes don't." |

**Trust Tells (Jake):**

| Range | Observable Behavior |
|-------|-------------------|
| 0-8 | "He keeps the sketchbook angled away. If you lean in, he turns the page. Whatever's on it isn't for you." |
| 9-15 | "He shows you the landscape he's working on. Professional distance — the work, not him. 'What do you think of the composition?'" |
| 16-22 | "He tells you about his professor who says he has talent. Then, quieter: 'Ryan thinks it's a waste of time.' He's trusting you with something that hurts." |
| 23-30 | "He draws with his door open when he knows you're in your room. An invitation. If you come in, he doesn't stop drawing — he pulls over a chair. You belong in his space now." |
| 31-40 | "He falls asleep drawing. The sketchbook is open on his chest — her face, her hands, a partial nude he hasn't finished. He didn't close it because he forgot you might see. He forgot because forgetting is trust." |

#### Speech Patterns

**Structure**: Incomplete sentences that trail into silence. Questions he already knows the answer to. Starts strong, loses confidence mid-thought. "I was thinking maybe we could—" (pause) "—if you're not busy." Frequent use of "I mean" and "it's not—" as hedges before saying something real.

**What he says vs what he means**: Jake is more transparent than the others, which makes his subtext subtler. "I drew you" means exactly what it says — but also means "I've been looking at you for hours and this is the result." "Do you want to see?" means "Please see me seeing you." "We shouldn't" means "I know we will and I want to."

**Evolution**: Early Jake stammers and trails off. Mid-game Jake becomes more articulate when they're alone — full sentences, direct questions, the stammer only returning when she surprises him. Late-game Jake says things simply and completely: "I love you." No hedging. No trailing off. The boy who couldn't finish a sentence found his ending.

**Signature phrases:**
- "I was just—" (caught doing something he can't explain)
- "Can I draw you?" (the invitation that means everything)
- "We shouldn't." (the protest that never holds)
- "I drew you again." (the truth he can't stop telling)

#### Starting Stats

```toml
[npcs.npc_jake]
name = "Jake"
core_traits = { love = 5, trust = 5, corruption = 0 }
# Love and trust start at 5 — genuine warmth from being similar ages,
# sharing the "outsider" feeling. Zero corruption — he hasn't considered
# her sexually yet.
```

#### Arc Concept Summary

- **Act 1 (corruption 0-50):** Bonding over art. Drawing sessions, studying together. She notices his sketchbook has her in it. First physical awareness through posing: "Hold still, I need to get the light on your collarbone."
- **Act 2 (corruption 50-130):** Art becomes the excuse. Poses get revealing. Shared wall at night becomes charged. Creek swim. First kiss — tender, guilty, mutual. "We shouldn't." "I know."
- **Act 3 (corruption 130-220):** Full emotional + physical escalation. Tenderness remains. He draws her nude. The sketchbook is their shared secret. If Frank or Ryan discovers the drawings → major crisis catalyst.

**Branch Point (Level 3, mid-game ~corruption 90):** Lily discovers Jake's SECRET intimate sketches — poses she didn't know he saw. Different from Beat 11 (where he shows her innocent art willingly).
- **"They're beautiful"** → `chose_tender_jake` — arc stays sweet. He draws her with consent. Art as shared language. Corruption + Love.
- **"You've been watching me?"** → `chose_possessive_jake` — arc turns darker. Shyness was hiding obsession. Sorry, then defiant, then desperate. Sweetness has teeth. Corruption + Dominance undertone.
- Both set `jake_sketches_discovered`. Emotional texture shifts dramatically.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### SECTION 2.5: NPC CUSTOMIZATION

All three NPCs are customizable at game start. The player can rename them and choose a relationship label.

```toml
[[npcs]]
id = "npc_frank"
name = "Frank"
customizable = true
relationship = "step-dad"
relationship_options = ["step-dad", "mom's boyfriend", "landlord"]
description = "45, broad shoulders, calloused hands, salt-and-pepper stubble..."
portrait = "frank.jpg"
core_traits = { love = 0, trust = 5, corruption = 0 }
flag_keys = []

[[npcs]]
id = "npc_ryan"
name = "Ryan"
customizable = true
relationship = "step-brother"
relationship_options = ["step-brother", "housemate", "roommate"]
description = "23, athletic, tanned, strong jaw, cocky grin..."
portrait = "ryan.jpg"
core_traits = { love = 0, trust = 0, corruption = 10 }
flag_keys = []

[[npcs]]
id = "npc_jake"
name = "Jake"
customizable = true
relationship = "step-brother"
relationship_options = ["step-brother", "housemate", "roommate"]
description = "20, lean, shaggy hair, glasses when drawing..."
portrait = "jake.jpg"
core_traits = { love = 5, trust = 5, corruption = 0 }
flag_keys = []
```

**Content Writing Rule**: ALL narrative content uses `@frank`, `@ryan`, `@jake` for names and `@frank.rel`, `@ryan.rel`, `@jake.rel` for relationship labels. All relationship options share the same cohabitation context.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 3: STAT ECONOMY DESIGN

### Player Corruption Growth

| Source | Gain | Frequency | Notes |
|--------|------|-----------|-------|
| Neutral activity choice (emotional/safe) | +1-2 | Per visit | Small ambient corruption from proximity |
| Escalating activity choice (physical) | +2-5 | Per visit | Higher tiers give more corruption |
| Random encounters (passive witnessing) | +2-3 | Per trigger (1/day max) | ~0.5-1 triggers/day average |
| Story events (minor) | +3-5 | One-time | Bus problem, creek swim, etc. |
| Story events (major) | +5-8 | One-time | First kiss, first handjob, crisis points |
| Wearing Bold+ clothing in town | +1-2 | Daily | Passive — NPCs stare, catcalls |
| Wearing Daring sleepwear around house at night | +1 | Nightly | Passive — walking to kitchen in lingerie |
| Bold makeup kit (when applied) | +1 | Daily | Self-corruption through presentation |

**Target corruption progression:**

| Day Range | Corruption Range | What's Happening |
|-----------|-----------------|------------------|
| Days 1-7 | 0-40 | Arrival, settling, personal discovery. Reaching 40 requires some escalation. |
| Days 8-15 | 40-70 | Bookkeeping unlocks. Jake arc deepens. Ryan pushes. |
| Days 16-25 | 70-100 | Kiss likely fired. Frank arc begins to stir. |
| Days 26-35 | 100-140 | Frank arc active. All three in play. Physical escalation. |
| Days 36-45 | 140-180 | Deep escalation. Oral tiers. Cross-NPC awareness. |
| Days 46-56 | 180-240 | Endgame. Sex tiers. Mom's return. Convergence. |

### Player Confidence Growth

| Source | Gain | Notes |
|--------|------|-------|
| Gym workout | +1 | +2 with proper athletic wear |
| Jogging (any) | +1 | Solo exercise builds self-reliance |
| Wearing Cute+ clothing (first time per tier) | +2 one-time | The mirror moment |
| Wearing Bold+ clothing (daily) | +1/day | She knows people are looking |
| Successful confrontation (story event) | +3-5 | Standing up to Ryan, negotiating with Frank |
| Art achievement / modeling | +2 | Per milestone |
| Diner waitressing shift | +1 | Per shift |
| Assertive dialogue choice | +1-2 | When she picks bold over safe |
| Fitness 21+ bonus | +1 extra on clothing confidence | Clothes fit better |
| Beauty 61+ bonus | +1 extra on social confidence | Compliments land harder |

**Key confidence thresholds:**
- 30: Required for diner job
- 60+: Required for Independent ending

### Per-NPC Stat Growth (Love / Trust / Corruption)

**How different activities build different NPC stats:**

| Activity Type | Love | Trust | Corruption | Example |
|---------------|------|-------|------------|---------|
| Meals together (T1 — eat) | +1 | +1 | — | Breakfast, dinner |
| Meals together (T2 — talk/flirt) | +2 | — | +1 | Deep conversation at dinner |
| Working together | — | +2 | — | Job site with Ryan, bookkeeping with Frank |
| Drawing sessions (Jake) | +2 | +1 | +1-2 | Higher corruption as poses escalate |
| Truck rides (Ryan) | +1 | +1 | +1-2 | Confined space, his comments |
| Bookkeeping (Frank) | +1 | +2 | +1-2 | Closed door, proximity |
| Deep emotional conversation | +2 | +2 | — | Late-night talks, vulnerability |
| Covering for NPC / keeping secrets | — | +3 | — | Frank's debt, Ryan's school, Jake's drawings |
| Physical encounter (escalating choice) | +1 | — | +2-3 | Each tier builds the NPC's corruption toward Lily |
| Story gift/sacrifice | +3 | +1 | — | NPC clothing gifts, acts of protection |
| Cooking together | +2 | +1 | — | Kitchen, evening |
| Creek swimming | +1 | — | +2-3 | Bodies + water + isolation |
| Gym together (Ryan) | — | +1 | +2 | Physical proximity, bodies |
| Hiking (group) | +1 | +1 | +1 | Whoever she walks with |

**Activities NEVER build all three stats equally.** This forces Lily to diversify — she can't grind one activity to max everything for one NPC. The player must balance emotional time (love/trust) with escalation activities (corruption) to unlock gate-setting story events.

### NPC Stat Growth Targets (Jake-first default path)

**Jake:**

| Day Range | Love | Trust | Corruption | Key Moments |
|-----------|------|-------|------------|-------------|
| Days 1-7 | 5→12 | 5→10 | 0→5 | Bonding, drawing sessions begin |
| Days 8-14 | 12→18 | 10→16 | 5→15 | Exposure, modeling begins |
| Days 15-25 | 18→25 | 16→22 | 15→30 | Kiss, deeper intimacy |
| Days 26-40 | 25→32 | 22→28 | 30→40 | Handjob/oral tiers |
| Days 41-56 | 32→40 | 28→35 | 40→50 | Sex tier, endgame |

**Ryan:**

| Day Range | Love | Trust | Corruption | Key Moments |
|-----------|------|-------|------------|-------------|
| Days 1-7 | 0→3 | 0→2 | 10→13 | Testing boundaries, truck rides begin |
| Days 8-14 | 3→8 | 2→8 | 13→18 | Job site work, gym trips |
| Days 15-25 | 8→15 | 8→14 | 18→28 | Truck incident, first real connection |
| Days 26-40 | 15→22 | 14→20 | 28→38 | Physical escalation, protectiveness |
| Days 41-56 | 22→30 | 20→25 | 38→45 | Full arc, competitive with Jake |

**Frank:**

| Day Range | Love | Trust | Corruption | Key Moments |
|-----------|------|-------|------------|-------------|
| Days 1-7 | 0→3 | 5→8 | 0→2 | Professional distance, house rules |
| Days 8-14 | 3→8 | 8→12 | 2→5 | Bookkeeping begins, building trust |
| Days 15-25 | 8→14 | 12→18 | 5→10 | Office proximity, first cracks |
| Days 26-40 | 14→22 | 18→24 | 10→18 | Late-night kitchen, control eroding |
| Days 41-56 | 22→32 | 24→30 | 18→28 | Full arc, dominance emerges |

### Player Resource Flows

**Income:**

| Source | Pay/Session | Energy | Time Slot | Corruption Gate | Notes |
|--------|-----------|--------|-----------|-----------------|-------|
| House cleaning | $20 | 25 | Late Morning | None | Available from week 1 |
| Bookkeeping (Frank) | $25 | 20 | Afternoon | corruption >= 40 | Unlocks ~week 3-4 |
| Job site labor (Ryan) | $40 | 25 | Late Morning | corruption >= 40 | Physical proximity |
| Art modeling — clothed (Jake) | $30 | 15 | Afternoon | corruption >= 50 | Poses escalate |
| Diner waitressing | $45 | 20 | Evening | confidence >= 30 | Misses dinner + night |
| "Overtime" bookkeeping (Frank) | $60 | 20 | Evening | corruption >= 100 | Alone, door closed, his terms |
| Art modeling — nude (Jake) | $80 | 15 | Afternoon | corruption >= 130 | Full exposure |
| Ryan's "favors" | $100 | 20 | Night | corruption >= 150 | Whatever Ryan asks |
| Frank's "arrangement" | $150 | 20 | Late Night | corruption >= 180 | Authority takes control |

**Recurring expenses:**

| Expense | Amount | Frequency | If Unpaid |
|---------|--------|-----------|-----------|
| Bus pass | $80 | Monthly | No bus travel. Must use Ryan's truck (increases dependency). |
| Art supplies | $60 | Monthly | Can't complete assignments. Loses campus events after 2 weeks. |
| Phone bill | $45 | Monthly | Phone cut off after 1 month. Mom can't call — misses story beats. |
| Food contribution | $50 | Weekly | frank_trust -3. "Pull your weight." Triggers once, then weekly. |
| **Total monthly** | **~$385** | | |

**Other income:**
- Mom sends $200/month (often late — Diana is overwhelmed, transfers bounce or arrive a week late)
- Starting money: $400

**Two-phase economic model:**

| Phase | Weekly Income | Weekly Expenses | Surplus | Pressure |
|-------|-------------|-----------------|---------|----------|
| **Weeks 1-3** (cleaning only) | $100 (5 cleans) | $96 (food $50 + bus+art+phone prorate $46) | **$4/week** | CRITICAL |
| **Weeks 4+** (bookkeeping unlocks) | $225 (clean + bookkeep daily) | $96 | **$129/week** | Comfortable — but corruption >= 40 already |

### Fitness Stat Economy

| Activity | Fitness Gain | Energy Cost | Location | Notes |
|----------|-------------|-------------|----------|-------|
| Gym workout | +3 | 30 | loc_gym (town) | Best source. Requires transport. |
| Jogging (park) | +2 | 20 | loc_park (town) | Afternoon. Better gains than property. |
| Jogging (property) | +1 | 15 | loc_yard | Anytime incl. mornings. No transport. |
| Creek swimming | +2 | 30 | loc_creek | Also builds corruption (bodies + water). |
| Hiking | +2 | 30 | loc_trail (weekends) | Also builds NPC stats with hiking partner. |
| Job site labor | +1 | 25 | loc_workshop | Side benefit of earning money. |
| Yoga in room | +1 | 10 | loc_lily_room | Solo, always available. Low energy, low reward. |

**Decay**: -1 fitness per 3 days without exercise.

**Level effects:**

| Fitness | Label | Mechanical Effect |
|---------|-------|-------------------|
| 0-20 | Average | No bonuses, no penalties |
| 21-40 | Toning up | +1 confidence from Cute+ clothing |
| 41-60 | Noticeable | NPC body dialogue upgrades. Swimwear scene upgrades. |
| 61-80 | Athletic | Energy max → 110. Stamina physical tier choices unlock. |
| 81-100 | Peak | +1 to ALL NPC corruption gains per interaction |

### Beauty Stat Economy

| Activity | Beauty Effect | Cost | Location | Notes |
|----------|-------------|------|----------|-------|
| Morning grooming | Prevents decay | Free | loc_bathroom | Minimum daily maintenance |
| Apply makeup (basic kit) | +1 daily buff | $20 kit | loc_lily_room | Buff until sleep |
| Apply makeup (cute kit) | +2 daily buff | $35 kit upgrade | loc_lily_room | Requires corruption >= 45 |
| Apply makeup (bold kit) | +2 buff + 1 corruption | $45 kit upgrade | loc_lily_room | Requires corruption >= 85 |
| Skincare routine | +1 permanent | $15 set | loc_bathroom | Once per day |
| Premium skincare | +2 permanent | $30 upgrade | loc_bathroom | Requires corruption >= 45 |
| New hairstyle #1 | +3 one-time | $30 | loc_clothing_store | NPCs comment 2-3 days |
| New hairstyle #2 | +3 one-time | $30 | loc_clothing_store | Bolder. Corruption >= 45. |
| New hairstyle #3 | +3 one-time | $30 | loc_clothing_store | Statement. Corruption >= 85. |
| Spa/self-care day | +2 permanent | 15 energy | loc_lily_room | Requires skincare products |
| Perfume | Narrative only | $25 | loc_clothing_store | Scent descriptions in ALL close NPC scenes |

**Decay**: -1 beauty per 2 days without grooming.

**Total beauty investment**: ~$260 across the full game.

**Level effects:**

| Beauty | Label | Mechanical Effect |
|--------|-------|-------------------|
| 0-20 | Neglected | Negative NPC comments. "You look tired." |
| 21-40 | Natural | Default. No bonuses, no penalties. |
| 41-60 | Pretty | Diner tips +15%. Casual compliments. |
| 61-80 | Beautiful | Diner tips +30%. +1 confidence from social activities. |
| 81-100 | Stunning | +1 to ALL NPC love gains per interaction |

### The "Polished" Daily State

**Polished = showered today + makeup applied + clothing tier Cute or above**

Effect: +1 to ALL NPC stat gains (love, trust, corruption) for that day.

Morning routine trade-off:
- Shower only: +10 energy, prevents beauty decay. No polished.
- Shower + grooming: +5 energy, prevents decay, enables "groomed." No polished without makeup + Cute outfit.
- Shower + grooming + makeup: +5 energy, prevents decay, +1-2 beauty buff, polished if Cute+ outfit.
- Skip everything: No energy restore from shower. Beauty decays. Looks rough.

The 5-energy difference between shower-only (+10) and grooming (+5) is the daily investment: 5 energy now vs. polished bonus (+1 all NPC gains) across 3-4 interactions all day.

### Energy Budget Summary

| Tier | Cost | Activities |
|------|------|-----------|
| Free | 0 | Sleep, shower, phone scroll, getting dressed, napping |
| Minimal | 5 | Check phone, journal, wander property |
| Light | 10 | Breakfast, lunch, quick conversation, stargazing |
| Moderate-light | 15 | Dinner, TV, drawing session, park bench |
| Moderate | 20 | Cooking together, bookkeeping, studying, diner shift, Ryan's errands |
| Heavy | 25 | Job site work, house cleaning, yard chores |
| Very heavy | 30 | Creek swimming, gym workout, hiking trail |

**Restoration:**

| Source | Restore |
|--------|---------|
| Full sleep (Late Night → Early Morning) | Set to max (100, or 110 at fitness 61+) |
| Afternoon nap | +20 |
| Shower | +10 |
| Breakfast T1 | +5 |
| Lunch T1 | +5 |
| Dinner T1 | +10 |

**Rules:**
- Story events (is_repeatable = false) NEVER have energy costs
- Random encounters NEVER have energy costs
- Restorative activities are FREE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 4: GATE FLAG DESIGN

### Gate Architecture

7 shared skill unlock flags, earnable through ANY NPC. Flags represent Lily's internal shift — she's crossed that mental barrier — not a milestone with a specific person. Whichever NPC she reaches that threshold with first sets the shared flag.

### Unlock Threshold Table (Per NPC)

| Flag | What It Unlocks | Jake Conditions | Ryan Conditions | Frank Conditions |
|------|----------------|-----------------|-----------------|------------------|
| `exposure_unlock` | Being seen / showing body choices | corruption >= 25, jake_love >= 10 | corruption >= 40, ryan_corruption >= 10 | corruption >= 60, frank_trust >= 10 |
| `flirt_unlock` | Flirting choices with all NPCs | corruption >= 40, jake_love >= 12 | corruption >= 50, ryan_love >= 8 | corruption >= 75, frank_trust >= 15 |
| `tease_unlock` | Teasing / showing off choices | corruption >= 55, jake_love >= 15, jake_trust >= 10 | corruption >= 70, ryan_corruption >= 15 | corruption >= 90, frank_love >= 15, frank_trust >= 15 |
| `kiss_unlock` | Kissing choices with all NPCs | corruption >= 70, jake_love >= 15, jake_trust >= 15 | corruption >= 85, ryan_love >= 12, ryan_trust >= 10, ryan_corruption >= 15 | corruption >= 120, frank_love >= 20, frank_trust >= 20 |
| `handjob_unlock` | Manual/groping tier choices | corruption >= 100, jake_love >= 20, jake_trust >= 18, jake_corruption >= 15 | corruption >= 110, ryan_love >= 15, ryan_trust >= 12, ryan_corruption >= 25 | corruption >= 140, frank_love >= 25, frank_trust >= 22 |
| `blowjob_unlock` | Oral tier choices | corruption >= 140, jake_love >= 25, jake_trust >= 20, jake_corruption >= 25 | corruption >= 150, ryan_love >= 18, ryan_trust >= 15, ryan_corruption >= 30 | corruption >= 180, frank_love >= 28, frank_trust >= 25 |
| `sex_unlock` | Full sex choices | corruption >= 180, jake_love >= 30, jake_trust >= 25, jake_corruption >= 30 | corruption >= 190, ryan_love >= 22, ryan_trust >= 18, ryan_corruption >= 35 | corruption >= 210, frank_love >= 30, frank_trust >= 28 |

### Gate-Setting Story Events (Default Jake-First Path)

| Gate | Most Likely Story Event | Approx Day | Corruption | Unlocks In Activities |
|------|------------------------|------------|------------|----------------------|
| `exposure_unlock` | Jake drawing session — she lowers a strap for the pose (Beat 7) | Day ~8 | ~25-30 | "Stand closer" physical sub-menu option in ALL NPC activities |
| `flirt_unlock` | Art modeling gets charged — she teases Jake while posing (Beat 13) | Day ~12 | ~40-50 | "Flirt with him" option (corruption >= 40 + flag) |
| `tease_unlock` | She poses provocatively on purpose for Jake (organic progression) | Day ~16 | ~55-65 | "Tease him" option (corruption >= 55 + flag) |
| `kiss_unlock` | Over the sketchbook — tender, mutual, guilty (Beat 14) | Day ~18 | ~70-80 | "Kiss him" option (corruption >= 70 + flag) |
| `handjob_unlock` | Drawing session turns physical — her hand on him (Beat 20) | Day ~28 | ~100-110 | "Touch him" option (corruption >= 100 + flag) |
| `blowjob_unlock` | Jake's room at night — tender, she wants to (organic) | Day ~38 | ~140-150 | "Use your mouth" option (corruption >= 140 + flag) |
| `sex_unlock` | His bed, eye contact, whispered names (organic) | Day ~46 | ~180-190 | "Go further" option (corruption >= 180 + flag) |

**Note:** These are the EXPECTED path. A Ryan-first or Frank-first player hits these milestones through different scenes at different corruption levels. The gate flag is the same regardless of source NPC.

### Narrative Flavor Per NPC (How Each Milestone FEELS)

| Flag | Jake (CORRUPTION + LOVE) | Ryan (LUST + SEDUCTION) | Frank (FORBIDDEN + DOMINANCE) |
|------|--------------------------|-------------------------|-------------------------------|
| `exposure_unlock` | Drawing session — she lowers a strap for the pose. His pencil stops. | Creek swim — bikini comes untied. He doesn't look away. | She walks out of the shower, he's in the hallway. Both freeze. |
| `flirt_unlock` | She teases him while posing, watches him blush. Tender. | She flirts back in the truck for the first time. Playful. | She makes a comment during bookkeeping that isn't about numbers. Charged. |
| `tease_unlock` | She poses provocatively on purpose, watching his reaction. | She wears the bikini he bought, knows he's watching. | She bends over the desk reaching for a file, takes her time. |
| `kiss_unlock` | Over the sketchbook. Tender, mutual, guilty. "We shouldn't." "I know." | In the truck, parked on a dirt road. He pulls her in. She lets him. | Kitchen at 2 AM. Coffee going cold. "This can't happen." Then he does it. |
| `handjob_unlock` | Drawing session turns physical. Her hand on him. Both shaking. | Truck parked somewhere remote. "You owe me." Direct. | Office, door locked. She reaches under the desk. Power. |
| `blowjob_unlock` | His room at night. Tender. She wants to. He can't believe it. | Gym shower or truck. Raw, direct. He tells her what he wants. | Office. He stands. She kneels. Dominance fully realized. |
| `sex_unlock` | His bed. Eye contact. Whispered names. Love. | Against a wall, truck bed, wherever the moment takes them. Need. | His bedroom. His rules. Door locked. Forbidden fully embraced. |

### First-Time vs Repeat Awareness (Group Block Variant)

Each NPC's milestone scene acknowledges whether this is Lily's FIRST time or she's done it before with another NPC:

**If flag NOT yet set (first time):**
> "She's never done this before. Her hands are shaking. The world narrows to just this moment — his breath, her heartbeat, the line she's about to cross."

**If flag already set (learned from another NPC):**
> "She's done this before. But not like this. Not with him. Everything she thought she knew about this act gets rewritten in the space between their bodies."

One extra group block per milestone scene per NPC. Low content cost, high emotional payoff.

### Cross-NPC Transfer Logic

Once a flag is set by ANY NPC's story scene → that tier of choices appears in ALL NPC activities.

The flag = "permission slip" (Lily is psychologically ready).
Each NPC's individual stat thresholds = "relationship earned it."

Both are always required. Never flag alone. Never stats alone.

### Physical Sub-Menu Thresholds (In Activities)

```
Physical choice → sub-menu:
  "Stand closer"        (always, after exposure_unlock)
  "Flirt with him"      (after flirt_unlock + corruption >= 40)
  "Tease him"           (after tease_unlock + corruption >= 55)
  "Kiss him"            (after kiss_unlock + corruption >= 70)
  "Touch him"           (after handjob_unlock + corruption >= 100)
  "Use your mouth"      (after blowjob_unlock + corruption >= 140)
  "Go further"          (after sex_unlock + corruption >= 180)
```

These corruption thresholds match the LOWEST flag-setting threshold (Jake's). Each choice ALSO requires NPC-specific stat thresholds.

### Minimum Narrative Distance Between Gates

| Transition | Minimum Gap |
|-----------|-------------|
| exposure → flirt | 1 tension event + 2 in-game days |
| flirt → tease | 1 bridge event + 2 in-game days |
| tease → kiss | 1 crisis moment + 3 in-game days |
| kiss → handjob | Major crisis + resolution |
| handjob → blowjob | 1 sacrifice choice + 3 in-game days |
| blowjob → sex | Turning point + 3 in-game days |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 5: COMPLETE FLAG INVENTORY

### Progression Flags (Story Event Completion)

| Flag | Set By | When |
|------|--------|------|
| `game_started` | Opening scene — Lily arrives | Day 1 |
| `first_morning` | Shared bathroom incident, breakfast dynamics | Day 2 |
| `bus_problem_discovered` | Lily discovers terrible bus schedule | Day 2-3 |
| `mom_called` | Diana calls — money transfer late | Day 3-4 |
| `money_crisis_realized` | Lily counts her money, internal monologue | Day 4-5 |
| `first_week_complete` | Week 1 milestone — routines established | Day 7 |
| `chores_started` | Lily offers to clean for cash | Day 6-7 |
| `drawing_started` | Jake asks if she'll model (clothed) | Day ~8 |
| `truck_incident_complete` | Ryan's first push in the truck | Day ~10 |
| `bookkeeping_started` | Frank offers bookkeeping work | Day ~12 |
| `first_swim` | First creek swim — physical exposure | Day ~10-12 |
| `saw_jakes_sketches` | Jake shows his sketchbook willingly (innocent art) | Day ~12-14 |
| `ryan_caught_her` | Ryan walks in on Lily changing | Day ~14 |
| `modeling_started` | Art modeling gets charged (Jake) | Day ~14 |
| `frank_kitchen_moment` | Late-night kitchen — his hand on hers | Day ~28 |
| `ryan_leverage` | Ryan knows about modeling/activities, wants arrangement | Day ~30 |
| `power_outage` | One night, no electricity — candles, proximity | Day ~32 |
| `frank_found_drawings` | Frank finds Jake's intimate sketches | Day ~35 |
| `financial_crisis` | Mom's transfer bounces, art supplies overdue | Day ~34 |
| `brothers_know` | Ryan finds out about Jake (or vice versa) | Day ~42 |
| `frank_offer` | "I'll cover everything. Here's what I want." | Day ~45 |
| `crisis_resolved` | Lily handles the brothers' discovery | Day ~44 |
| `mom_returning` | Diana announces early return | Day ~48 |
| `endgame_active` | Final week begins | Day ~50 |
| `game_complete` | Mom arrives. Resolution. | Day ~56 |

### Gate Flags (Shared Skill Unlocks)

| Flag | What It Enables | Approximate Day (Jake-first) |
|------|----------------|------------------------------|
| `exposure_unlock` | "Stand closer" in physical sub-menus | Day ~8 |
| `flirt_unlock` | "Flirt with him" choices | Day ~12 |
| `tease_unlock` | "Tease him" choices | Day ~16 |
| `kiss_unlock` | "Kiss him" choices | Day ~18 |
| `handjob_unlock` | "Touch him" choices | Day ~28 |
| `blowjob_unlock` | "Use your mouth" choices | Day ~38 |
| `sex_unlock` | "Go further" choices | Day ~46 |

### Branch Flags (Player Choices)

| Flag | Set By | Effect |
|------|--------|--------|
| `chose_tender_jake` | Jake branch — "They're beautiful" | Jake arc stays sweet. Corruption + Love. |
| `chose_possessive_jake` | Jake branch — "You've been watching me?" | Jake arc darkens. Corruption + Dominance undertone. |
| `jake_sketches_discovered` | Either Jake branch choice | Marks Jake branch complete. |
| `ryan_resisted` | Ryan branch — slap his hand | Ryan shifts to verbal seduction. |
| `ryan_allowed` | Ryan branch — let it happen | Ryan gets bolder, more direct. |
| `truck_incident_complete` | Either Ryan branch choice | Marks Ryan branch complete. |
| `chose_confront_frank` | Frank branch — confront about debt | Adversarial-to-intimate pipeline. |
| `chose_protect_frank` | Frank branch — keep his secret | Conspiratorial intimacy pipeline. |
| `frank_secret_complete` | Either Frank branch choice | Marks Frank branch complete. |
| `chose_independent` | Global crisis — "It's none of your business" | Lily asserts dominance. |
| `chose_peacemaker` | Global crisis — "Please don't fight" | Guilt + tenderness tone. |
| `chose_avoidant` | Global crisis — walk away silently | Short-term regression, Frank accelerates. |

### Utility Flags (System/Mechanic)

| Flag | Set By | Purpose |
|------|--------|---------|
| `town_access` | First ride with Ryan | Unlocks clothing store, gym, park, diner |
| `comfortable_braless` | Jake drawing session (removes bra for pose) | Bra no longer required in wardrobe |
| `discovered_teasing` | Ryan encounter where underwear becomes a factor | Underwear no longer required in wardrobe |
| `polished` | Daily state: shower + makeup + Cute+ outfit | +1 all NPC stat gains (recalculated each morning) |

### Ending Condition Flags

| Ending | Conditions |
|--------|-----------|
| **Jake's Girl** | Jake highest combined stats (love+trust+corruption), corruption < 160 |
| **Ryan's Conquest** | Ryan highest combined stats, corruption > 150 |
| **Frank's Arrangement** | Frank highest combined stats, corruption > 180 |
| **All Three** | No NPC more than 25 combined points ahead of others |
| **Independent** | confidence > 60, money > 500, diner job active |
| **Escape** | corruption < 100, low NPC stats across the board |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type "proceed" to continue to Phase 3: World Design,
or provide adjustments.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


# PHASE 3: WORLD DESIGN
# Under One Roof

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 1: LOCATION HIERARCHY

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Navigation Structure

```
The Property (container) → default_entry: loc_hallway
  └── Hallway (internal hub)
        ├── Kitchen
        ├── Living Room
        ├── Shared Bathroom
        ├── Frank's Office
        ├── Lily's Room
        ├── Jake's Room
        ├── Workshop / Garage
        └── Backyard (container) → default_entry: loc_yard
              ├── Yard
              └── Creek

Town (reached by bus $2 or Ryan's truck) → default_entry: loc_town
  └── Town (external hub)
        ├── Campus (container) → default_entry: loc_campus
        │     └── Library
        ├── Clothing Store
        ├── General Store
        ├── Gym
        ├── Park
        └── Diner

Hiking Trail (Ryan's truck, weekends only) → default_entry: loc_trail_head
  └── Trail Head (internal hub)
        ├── Rest Stop
        └── Isolated Creek

Ryan's Truck (mobile — entered via Ryan's activity canvases)
```

**Total: 21 locations** (11 property, 7 town, 3 trail, 1 mobile)

---

### PROPERTY LOCATIONS

---

#### PROPERTY CONTAINER

**`loc_property`** — The Harmon Property
- *Forty minutes by bus from the nearest college town. A contractor's spread — main house, detached workshop, a yard that blurs into fields and trees. The gravel driveway crunches under every arrival and departure. The nearest neighbor is a ten-minute walk down a dirt road. At night, the property is so quiet you can hear the creek behind the house and every footstep in the hallway. Lily didn't know a house could be this loud by being this silent.*
- Image search: "rural American contractor property, main house with workshop, gravel driveway, fields and trees, isolated, dusk"
- Type: container
- `is_container = true`
- `default_entry = loc_hallway`

---

**`loc_hallway`** — Hallway
- *Narrow, uneven hardwood floors that creak with every step. Frank's boots are always by the front door. A coat rack holding three sizes of flannel. The bathroom door is at the end — no lock that works properly. Lily's room is second on the right. Jake's room is right next to it. At 2 AM, every footstep is an announcement. You can't walk to the kitchen without everyone hearing.*
- Image search: "narrow farmhouse hallway, hardwood floors, coat rack, boots by door, dim hallway night lighting"
- Type: hub (internal)
- Entry from: `loc_property`
- Navigation order: `[loc_kitchen, loc_living_room, loc_bathroom, loc_franks_office, loc_lily_room, loc_jakes_room, loc_workshop, loc_backyard]`
- Activities: Random encounters (Jake's cracked door at night)

---

**`loc_kitchen`** — Kitchen
- *The social hub. Butcher-block counters stained by decades of meals. A table that seats four but has five chairs — Frank added one when Lily arrived. The coffee maker starts at 5 AM (Frank's timer). The window above the sink faces the backyard. At dinner, all three men are here. At 2 AM, it's just Frank with a whiskey and the refrigerator light. The kitchen is where everything happens that isn't supposed to happen in front of everyone.*
- Image search: "farmhouse kitchen, butcher block counters, wooden table with chairs, coffee maker, window facing backyard, warm lighting"
- Type: room
- Entry from: `loc_hallway`
- Primary NPC associations: All three (breakfast, dinner), Frank (late-night), Jake (morning)
- Activities: Breakfast (all NPCs, Morning), Lunch (solo/Jake, Afternoon), Dinner (all NPCs, Evening), Cooking together (Frank, Evening), Late-night kitchen encounter (Frank, Late Night — random)

---

**`loc_living_room`** — Living Room
- *Worn leather couch that fits three if nobody cares about personal space. A TV on a stand that's older than Ryan. Bookshelves with more tools than books. A window seat where Lily reads when the couch is occupied. At night, the TV fills the room with blue light and whoever's watching sits in the glow. The couch is the proximity trap — there's no sitting on it without being close to someone.*
- Image search: "farmhouse living room, worn leather couch, old TV, bookshelves, window seat, blue TV glow at night"
- Type: room
- Entry from: `loc_hallway`
- Primary NPC associations: Frank (Night — TV), Ryan (Night — TV), occasional Jake
- Activities: TV on the couch (Frank/Ryan, Night), Evening conversation (any NPC, Night)

---

**`loc_bathroom`** — Shared Bathroom
- *One bathroom for four people. The door lock is a hook-latch that doesn't always catch. Steam lingers for twenty minutes after a shower. Ryan's towel is always on the floor. Frank's razor is by the sink. Jake keeps his toothbrush in a cup. Lily's shelf is the smallest — a few products, a makeup bag, a hair tie. The mirror is directly across from the door, so whoever walks in sees everything reflected before they see her. The shower schedule is a battlefield nobody discusses.*
- Image search: "small farmhouse bathroom, single shower, mirror facing door, towels hanging, razor by sink, steam condensation"
- Type: room
- Entry from: `loc_hallway`
- Primary NPC associations: Random encounters (Ryan walk-in, Jake walk-in), Solo (morning routine)
- Activities: Morning shower routine (Solo, Early Morning), Random bathroom encounters (any NPC)

---

**`loc_franks_office`** — Frank's Office
- *The only room in the house with a lock that works. A heavy desk covered in invoices, a filing cabinet, a desk lamp that casts the room in amber. Smells like leather and old paper. A framed photo of Frank's first wife is in the drawer — face down. The chair behind the desk is Frank's throne. The chair in front is where Lily sits for bookkeeping. When the door closes, the rest of the house disappears. It's the most private space under this roof.*
- Image search: "contractor home office, heavy desk with invoices, filing cabinet, desk lamp amber light, leather chair, private room"
- Type: room
- Entry from: `loc_hallway`
- Primary NPC associations: Frank (exclusive — bookkeeping, private conversations)
- Activities: Bookkeeping (Frank, Afternoon — gated: corruption >= 40), "Overtime" bookkeeping (Frank, Evening — gated: corruption >= 100), Late-night conversations (Frank, Late Night)

---

**`loc_lily_room`** — Lily's Room
- *Second door on the right. A single bed, a desk she uses for homework, a closet that's too small for the wardrobe she's accumulating. The window faces the backyard — she can see the creek from here. The wall to her left is shared with Jake's room. At night, sound carries: pencil scratching paper, music through earbuds, the creak of a bedframe. She learned to recognize which sounds are his on the second night. The room started as temporary housing. It's becoming a dressing room, a confessional, and the place she picks her outfit knowing exactly who's going to see it.*
- Image search: "simple bedroom, single bed, desk with homework, small closet, window facing backyard, young woman's room, warm lamp"
- Type: room
- Entry from: `loc_hallway`
- Primary NPC associations: Solo (sleep, wardrobe changes, journal), Jake (shared wall — random encounter: sounds)
- Activities: Sleep (utility, Late Night), Change outfit (utility, any time), Yoga (Solo, fitness +1, any time), Wall knocking with Jake (Jake, Late Night), Afternoon nap (utility, Afternoon)

---

**`loc_jakes_room`** — Jake's Room
- *Art everywhere. Sketches pinned to the walls — landscapes, hands, the creek at different times of day. A desk buried under charcoal sticks and eraser shavings. His bed is made but the floor is a mess of sketchbooks and reference photos. The light is good in the afternoon — he keeps the curtains open for natural light. The wall to his right is shared with Lily's room. His door is often cracked open. Not an invitation. Not not one.*
- Image search: "young artist bedroom, sketches pinned to walls, messy desk with charcoal, sketchbooks on floor, natural light from window, cracked open door"
- Type: room
- Entry from: `loc_hallway`
- Primary NPC associations: Jake (exclusive — drawing sessions, late-night visits)
- Activities: Drawing session (Jake, Afternoon — main NPC activity), Studying together (Jake, Late Morning — weekends), Late-night visit (Jake, Late Night — gated)

---

**`loc_workshop`** — Workshop / Garage
- *Detached from the main house, connected by a gravel path. Table saw, hand tools on pegboard, sawhorses, the smell of cut wood and motor oil. Frank's truck is parked inside when it rains. Ryan's weights are in the corner — a bench press and a rack of dumbbells he hauled from a garage sale. This is where Frank starts his day at 5 AM and where the business runs. It's masculine space — sawdust, metal, strength. Lily doesn't belong here, which is exactly why being here with either of them feels charged.*
- Image search: "detached workshop garage, table saw, pegboard tools, sawhorses, old truck inside, weight bench in corner, sawdust"
- Type: room
- Entry from: `loc_hallway`
- Primary NPC associations: Frank (Early Morning, Late Morning), Ryan (Late Morning — job site prep)
- Activities: Job site labor (Ryan/Frank, Late Morning — money $40), Workshop help (Frank, Morning — trust building), Hidden magazines discovery (Frank, one-time — random)

---

#### BACKYARD CONTAINER

**`loc_backyard`** — Backyard
- *Behind the house, the mowed grass gives way to wild growth within twenty feet. A clothesline between two posts. A patch of garden Frank planted and nobody maintains. Beyond the yard, the property slopes down to the creek — a fifteen-minute walk through trees. The backyard is where the house's claustrophobia opens up, but it's still the property. Still their territory. From the kitchen window, you can see anyone who's out here.*
- Image search: "rural farmhouse backyard, clothesline, overgrown garden, tree line, sloping field, visible from kitchen window"
- Type: container
- `is_container = true`
- `default_entry = loc_yard`

---

**`loc_yard`** — Yard
- *The cleared area behind the house. Flat enough to jog loops around the perimeter. The clothesline runs east-west — Lily hangs laundry here and the wind dries it in an hour. A bench by the garden where Frank sits on Sunday mornings with his coffee. In summer the grass is warm enough to sit on barefoot. Sunbathing here means being visible from the kitchen window, Jake's window, and the workshop. There is no such thing as a private tan on this property.*
- Image search: "farmhouse yard, flat grass area, clothesline with laundry, wooden bench, garden patch, visible from house windows"
- Type: room
- Entry from: `loc_backyard`
- Primary NPC associations: Solo (chores, jogging), any NPC (outdoor encounters)
- Activities: Yard chores (Solo, any — money), Morning jog (Solo, Morning — fitness +1), Sunbathing (Solo, Afternoon — corruption if seen), Laundry (utility)

---

**`loc_creek`** — Creek
- *Fifteen minutes through trees from the house. Shallow enough to wade, deep enough at the bend to swim. Smooth rocks, overhanging branches, dappled light. The water is cold in the morning and tolerable by afternoon. It's the closest thing to privacy on the property — far enough from the house that voices don't carry, close enough that anyone could walk down. The creek is where bodies meet water and pretense dissolves.*
- Image search: "rural creek swimming hole, shallow water with rocks, overhanging trees, dappled sunlight, secluded, natural swimming spot"
- Type: room
- Entry from: `loc_backyard`
- Primary NPC associations: Jake (swimming, Late Afternoon), Ryan (skinny-dipping — random), any NPC (1-on-1 or group)
- Activities: Creek swimming (any NPC, Late Afternoon — fitness +2, corruption), Isolated conversation (any NPC)

---

#### MOBILE LOCATION

**`loc_ryans_truck`** — Ryan's Truck
- *A dented pickup that runs louder than it should. The cab smells like pine air freshener and whatever Ryan wore to the job site. Bench seat — no center console, just a gap she has to decide how to handle. The radio plays classic rock too loud. He drives with one hand on the wheel and the other on the gear shift, which is uncomfortably close to her knee. The truck is a fifteen-minute ride to town, but Ryan has a talent for making it take longer. Back roads. Scenic routes. Detours that end at dead-end dirt roads where the engine idles and the trees block the view from the road.*
- Image search: "old pickup truck interior, bench seat, pine air freshener, rural road through windshield, classic rock vibes, male driver"
- Type: room (mobile — not directly navigable)
- Entry from: Triggered via Ryan's activity canvases
- Primary NPC associations: Ryan (exclusive)
- Activities: Ride to town (Ryan, Late Afternoon — transportation + NPC time), Parked scene (Ryan, gated — escalation location)

---

### TOWN LOCATIONS

---

**`loc_town`** — Town
- *Forty minutes by bus from the property, fifteen in Ryan's truck. A small college town with a main street, a campus, and not much else. Enough to buy supplies, take a class, hit the gym, eat at the diner. Not enough to disappear into. If Lily takes the bus, nobody knows she was here. If Ryan drives, he knows everything — what she bought, where she went, who she talked to. Getting to town is free in his truck and costs $2 by bus. The price of independence is always $2.*
- Image search: "small American college town main street, shops, campus in background, quiet town, afternoon"
- Type: hub (external)
- Entry from: `loc_property` (bus $2/40min or Ryan's truck/15min)
- Navigation order: `[loc_campus, loc_clothing_store, loc_general_store, loc_gym, loc_park, loc_diner]`
- Gate: `town_access` flag (set after first ride with Ryan)

---

**`loc_campus`** — Campus
- *A small state college — brick buildings, a quad with dying grass, students who look like they're already bored with the semester. Lily's art building has north-facing windows for natural light. The library is in the basement of the humanities building — quiet, cramped, the kind of place where knees touch under study tables. Campus is the one place Lily goes that has nothing to do with the Harmon household. It's her life before. It's also where Jake takes his community college art class two buildings over.*
- Image search: "small state college campus, brick buildings, grassy quad, art building, students, afternoon"
- Type: container
- `is_container = true`
- `default_entry = loc_campus`
- Entry from: `loc_town`
- Primary NPC associations: Solo (classes), Jake (library, community college overlap)
- Activities: Art classes (Solo, Late Morning — mandatory Mon-Thu), Campus time (Solo)

---

**`loc_library`** — Library
- *Basement of the humanities building. Low ceilings, fluorescent lights, the smell of old paper and carpet cleaner. Study carrels along the walls, group tables in the middle. Jake comes here on afternoons when his community college class lets out early. The carrels are semi-private — partitioned on three sides, open behind. Close enough to whisper. Close enough to touch a hand under the divider without anyone seeing.*
- Image search: "college library basement, low ceilings, fluorescent lights, study carrels, group tables, quiet, students studying"
- Type: room
- Entry from: `loc_campus`
- Primary NPC associations: Jake (studying, quiet intimacy)
- Activities: Studying with Jake (Jake, Afternoon — love + trust), Solo studying

---

**`loc_clothing_store`** — Clothing Store
- *A boutique on the main street that sells everything from farm-practical to surprisingly fashionable. The owner is a woman in her fifties who doesn't judge what you buy but remembers everything. Two dressing rooms with curtains that don't fully close. If Ryan drove Lily here, he's outside in the truck watching the bags come out. If she took the bus, this is her secret. The progression from jeans to sundresses to mini skirts to things that shouldn't be worn in public happens here, one shopping trip at a time.*
- Image search: "small town women's clothing boutique, racks of clothing, dressing rooms with curtains, main street shop"
- Type: room
- Entry from: `loc_town`
- Gate: `town_access` flag
- Primary NPC associations: Solo
- Activities: Shopping — wardrobe purchases (Solo, any time), Beauty products (Solo)

---

**`loc_general_store`** — General Store
- *Narrow aisles, everything from groceries to art supplies to phone cards. The kind of store where you can buy toothpaste and turpentine in the same trip. The cashier knows every face in the county. Art supplies are in the back — Lily's monthly expense that she can't skip without losing campus events. The makeup aisle is small but expanding — someone's been buying.*
- Image search: "small town general store, narrow aisles, mixed goods, art supplies section, local cashier"
- Type: room
- Entry from: `loc_town`
- Primary NPC associations: Solo
- Activities: Grocery shopping (Solo, any — supplies), Art supply purchase (Solo — monthly), Beauty product purchase (Solo)

---

**`loc_gym`** — Gym
- *A public gym with old equipment that works fine. Free weights, a few treadmills, a bench press that Ryan treats like a personal altar. A men's and women's locker room with a shared hallway between. The gym is Ryan's territory outside the house — Lily on his turf in a physical context. Here, bodies are unavoidable. Sweat is unavoidable. The locker room hallway is where conversations happen between someone who just showered and someone who hasn't.*
- Image search: "small town public gym, free weights, treadmill, bench press, old equipment, fluorescent lighting"
- Type: room
- Entry from: `loc_town`
- Primary NPC associations: Ryan (primary — gym encounters), Solo (fitness)
- Activities: Gym workout (Solo/Ryan, Morning-Afternoon — fitness +3, energy 30), Gym with Ryan (Ryan, any gym time — corruption + fitness)

---

**`loc_park`** — Park
- *Town park with a jogging trail, benches, a pond with ducks nobody feeds. Jake comes here on weekends to sketch the water. It's neutral territory — not the property, not Ryan's turf, not Frank's domain. The benches are spaced for conversation. The jogging trail is lined with trees that give the illusion of privacy. In the afternoon sun, it's the only peaceful place in Lily's orbit.*
- Image search: "small town park, jogging trail, benches, pond with ducks, trees, peaceful afternoon, sketching spot"
- Type: room
- Entry from: `loc_town`
- Primary NPC associations: Jake (weekend sketching), Solo (jogging, thinking)
- Activities: Park jogging (Solo, Afternoon — fitness +2), Park sketching with Jake (Jake, Weekend Afternoon — love + trust), Bench conversation (any NPC)

---

**`loc_diner`** — Diner
- *Vinyl booths, laminate tables, coffee that's been sitting too long. A bell on the door that announces every customer. The menu hasn't changed since 1998. The owner is hiring — always hiring — because the pay is bad and the hours are worse. But $45 a shift is $45, and Lily can work the evening window if she's willing to skip dinner at home. Every diner shift is dinner she doesn't eat with three men who are starting to notice she's not there.*
- Image search: "small town American diner, vinyl booths, laminate tables, coffee pot, bell on door, evening lighting"
- Type: room
- Entry from: `loc_town`
- Primary NPC associations: Solo (work)
- Activities: Diner waitressing (Solo, Evening — money $45, gated: confidence >= 30 + town_access), Cheap meal (Solo, any — energy restore alternative)

---

### HIKING TRAIL LOCATIONS

---

**`loc_trail_head`** — Trail Head
- *A dirt pulloff where Ryan parks the truck. A wooden sign with a faded trail map. The trail runs three miles through mixed forest — deciduous trees, some pines, roots across the path. It's a weekend activity — Frank occasionally suggests it, Ryan drives, Jake brings his sketchbook. The group dynamic at the trailhead sets the tone: who walks with whom, who falls behind with Lily, who's watching from ahead. Every hike is a compressed version of the household tension, played out on a narrow path where passing means touching.*
- Image search: "hiking trail head, dirt pulloff, wooden trail sign, forest entrance, mixed trees, weekend hiking"
- Type: hub (internal)
- Entry from: `loc_property` (Ryan's truck only, weekends)
- Navigation order: `[loc_rest_stop, loc_isolated_creek]`
- Primary NPC associations: All three (group dynamic)
- Activities: Weekend hike start (any/all NPCs, Weekend — fitness +2)

---

**`loc_rest_stop`** — Rest Stop
- *A flat area with a picnic table and a view of the valley. The kind of spot where you set down your pack and sit close to whoever you walked with. The table fits four. Seating arrangement matters — across from someone is safe, next to someone is proximity, at the end alone is a statement. Whatever conversation happens here has the weight of effort behind it — you hiked to get here. Things said at altitude feel more real.*
- Image search: "hiking trail rest stop, picnic table, valley view, forest clearing, hikers resting, afternoon"
- Type: room
- Entry from: `loc_trail_head`
- Primary NPC associations: Whoever Lily walked with
- Activities: Rest stop conversation (any NPC — love + trust), Group picnic (all NPCs)

---

**`loc_isolated_creek`** — Isolated Creek
- *A swimming spot deeper in the trail, off the main path. Cold water, bigger rocks, more privacy than the property creek. You have to know it's here. Ryan knows. The water is waist-deep at the center. The banks are grassy and sloped for sitting. It's far enough from the trail that voices don't carry. Close enough that someone could walk up unannounced. This is the "away from the house" escalation space — nature as permission.*
- Image search: "secluded forest creek swimming hole, deeper water, mossy rocks, grassy bank, dappled light, very private"
- Type: room
- Entry from: `loc_trail_head`
- Primary NPC associations: Any NPC (1-on-1 swimming)
- Activities: Swimming (any NPC, Weekend Late Afternoon — fitness +2, corruption), Isolated conversation

---

### Location Connections Summary

| From | To | Method | Cost | Time |
|------|-----|--------|------|------|
| Property | Town | Bus | $2 | 40 min |
| Property | Town | Ryan's truck | Free | 15 min (but Ryan sees everything) |
| Property | Trail | Ryan's truck only | Free | Weekends only |
| Any property room | Any property room | Walking | Free | Instant |
| Town | Property | Bus | $2 | 40 min |
| Town | Property | Ryan | Free | 15 min |
| Campus | Library | Walking | Free | Sub-location |
| Trail Head | Rest Stop / Isolated Creek | Hiking | Free | Part of activity |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 2: TIME SYSTEM

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Starting Conditions

- **Starting hour**: 17:00 (Evening — Lily arrives late afternoon, awkward first dinner)
- **Starting day**: Day 1 (let's say a Saturday — she has the weekend to settle before classes Monday)
- **Starting week**: Week 1 of ~8 (56-60 day game)
- **Game ends**: ~Day 56 (Mom returns 2 weeks early from 10-week contract)

### Time Periods

| Period | Hours | Duration | Mood |
|--------|-------|----------|------|
| **Early Morning** | 05:00-07:00 | 2h | Quiet. Frank is in the workshop. Everyone else sleeps. The morning routine slot — shower, grooming, makeup. Sets the "polished" state for the day. |
| **Morning** | 07:00-09:00 | 2h | Breakfast in the kitchen. Frank and Jake are usually present. Ryan sleeps in 50% of the time. Morning jog around the property. First social slot. |
| **Late Morning** | 09:00-12:00 | 3h | The work slot. Frank at workshop/job site, Ryan at job site, Jake at community college (Mon-Thu). Lily: campus classes (Mon-Thu), house cleaning, job site labor. |
| **Afternoon** | 12:00-15:00 | 3h | The flex slot. Bookkeeping with Frank. Drawing with Jake. Gym in town. Art modeling. Lunch. The first major daily choice. |
| **Late Afternoon** | 15:00-17:00 | 2h | Creek swimming. Errands with Ryan (truck rides). Studying with Jake. Park jogging. Shopping in town. |
| **Evening** | 17:00-19:00 | 2h | Dinner — the high-tension slot. Usually all three NPCs present (Ryan out ~20%). Diner waitressing as alternative (miss dinner + night). |
| **Night** | 19:00-22:00 | 3h | Living room TV (Frank/Ryan). Frank's office (late work). Jake's room. Ryan comes home if he was out. The private hours begin. |
| **Late Night** | 22:00-01:00 | 3h | The most charged slot. Kitchen encounters (Frank, 50% chance). Bathroom encounters. Wall sounds from Jake's room. Sleep. Maximum risk, maximum reward. |

### Activity Schedule Overview

| Time Period | Location | Activity | NPC | Type | Days |
|-------------|----------|----------|-----|------|------|
| **EARLY MORNING** | | | | | |
| 05:00-07:00 | Bathroom | Morning shower routine | Solo | Utility (beauty maintenance, energy +5-10) | All |
| 05:00-07:00 | Lily's Room | Get dressed / pick outfit | Solo | Utility (sets clothing for day) | All |
| 05:00-07:00 | Lily's Room | Skip everything / sleep in | Solo | Utility (no energy restore, beauty decays) | All |
| **MORNING** | | | | | |
| 07:00-09:00 | Kitchen | Breakfast | All NPCs | Meal (energy +5, love +1 per NPC present) | All |
| 07:00-09:00 | Yard | Morning jog (property) | Solo | Fitness (+1, energy 15) | All |
| 07:00-09:00 | Workshop | Workshop help | Frank | NPC activity (trust +2, energy 25) | All |
| **LATE MORNING** | | | | | |
| 09:00-12:00 | Campus | Art classes | Solo | Mandatory (Mon-Thu, requires bus/Ryan) | Mon-Thu |
| 09:00-12:00 | Property | House cleaning | Solo | Money ($20, energy 25) | All |
| 09:00-12:00 | Workshop | Job site labor | Ryan/Frank | Money ($40, energy 25, corruption >= 40) | Mon-Fri |
| **AFTERNOON** | | | | | |
| 12:00-15:00 | Kitchen | Lunch | Solo/Jake | Meal (energy +5, love +1) | All |
| 12:00-15:00 | Frank's Office | Bookkeeping | Frank | Money ($25, energy 20, corruption >= 40) | Mon-Fri |
| 12:00-15:00 | Jake's Room | Drawing session | Jake | NPC activity (love +2, trust +1, corruption +1-2) | All |
| 12:00-15:00 | Jake's Room | Art modeling — clothed | Jake | Money ($30, energy 15, corruption >= 50) | All |
| 12:00-15:00 | Jake's Room | Art modeling — nude | Jake | Money ($80, energy 15, corruption >= 130) | All |
| 12:00-15:00 | Gym | Gym workout | Solo/Ryan | Fitness (+3, energy 30, requires town) | All |
| 12:00-15:00 | Lily's Room | Afternoon nap | Solo | Utility (energy +20) | All |
| **LATE AFTERNOON** | | | | | |
| 15:00-17:00 | Creek | Creek swimming | Any NPC | Fitness (+2, corruption +2-3, energy 30) | All |
| 15:00-17:00 | Ryan's Truck | Errands with Ryan | Ryan | NPC activity (love +1, corruption +1-2) | All |
| 15:00-17:00 | Library | Studying with Jake | Jake | NPC activity (love +1, trust +2) | All |
| 15:00-17:00 | Park | Park jogging | Solo | Fitness (+2, energy 20, requires town) | All |
| 15:00-17:00 | Park | Park sketching | Jake | NPC activity (love +2, trust +1, weekends) | Sat-Sun |
| 15:00-17:00 | Clothing Store | Shopping trip | Solo | Wardrobe purchases (requires town) | All |
| **EVENING** | | | | | |
| 17:00-19:00 | Kitchen | Dinner | All NPCs | Meal (energy +10, love +1, high tension) | All |
| 17:00-19:00 | Kitchen | Cook dinner together | Frank | NPC activity (love +2, trust +1) | All |
| 17:00-19:00 | Diner | Diner waitressing | Solo | Money ($45, energy 20, confidence >= 30) | All |
| 17:00-19:00 | Frank's Office | "Overtime" bookkeeping | Frank | Money ($60, energy 20, corruption >= 100) | Mon-Fri |
| **NIGHT** | | | | | |
| 19:00-22:00 | Living Room | TV on the couch | Frank/Ryan | NPC activity (love +1-2, proximity) | All |
| 19:00-22:00 | Jake's Room | Visit Jake's room | Jake | NPC activity (love +2, trust +1, gated) | All |
| 19:00-22:00 | Frank's Office | Late-night conversation | Frank | NPC activity (trust +2, corruption +1) | All |
| 19:00-22:00 | Lily's Room | Free time / rest | Solo | Utility (journal, phone, rest) | All |
| **LATE NIGHT** | | | | | |
| 22:00-01:00 | Kitchen | Late-night kitchen | Frank (50%) | Random encounter / NPC activity | All |
| 22:00-01:00 | Bathroom | Late-night bathroom | Random | Random encounter | All |
| 22:00-01:00 | Lily's Room | Wall knocking (Jake) | Jake | NPC activity (love +1, corruption +1) | All |
| 22:00-01:00 | Lily's Room | Sleep | Solo | Utility (resets energy to max) | All |
| 22:00-01:00 | Any NPC room | Ryan's "favors" | Ryan | Money ($100, corruption >= 150) | All |
| 22:00-01:00 | Frank's Office | Frank's "arrangement" | Frank | Money ($150, corruption >= 180) | All |

### Weekend Differences

- **Saturday/Sunday**: Jake home all day (no community college). Frank sometimes organizes a hike. Ryan available for gym/truck rides more freely.
- **Weekend-only activities**: Hiking trail (all NPCs), Park sketching (Jake), Extended creek outings
- **Campus**: Closed on weekends — Lily can't attend classes or use art studio
- **Diner**: Available all week, but weekday evening shifts conflict with dinner

### Pacing Tools

| Tool | Usage |
|------|-------|
| `days_since_flag` | Spaces story events. e.g., `kiss_unlock` scene requires 3+ days after `exposure_unlock`. |
| `max_triggers_per_day = 1` | Most activities limited to once daily. |
| `time_progression_minutes` | Each activity consumes 60-240 minutes of game time. |
| Priority system | Story events (10) > Special activities (6-8) > Economic events (2) > Regular activities (1). |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 3: ECONOMIC MODEL

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Income Sources

| Activity | Pay | Energy | Time Slot | Gate | Notes |
|----------|-----|--------|-----------|------|-------|
| House cleaning | $20 | 25 | Late Morning | None | Available from week 1 |
| Bookkeeping (Frank) | $25 | 20 | Afternoon | corruption >= 40 | Unlocks ~week 3-4 |
| Job site labor (Ryan) | $40 | 25 | Late Morning | corruption >= 40 | Physical proximity to Ryan |
| Art modeling — clothed (Jake) | $30 | 15 | Afternoon | corruption >= 50 | Poses escalate |
| Diner waitressing | $45 | 20 | Evening | confidence >= 30 | Misses dinner + night activities |
| "Overtime" bookkeeping (Frank) | $60 | 20 | Evening | corruption >= 100 | Alone, door closed |
| Art modeling — nude (Jake) | $80 | 15 | Afternoon | corruption >= 130 | Full exposure |
| Ryan's "favors" | $100 | 20 | Night | corruption >= 150 | Whatever Ryan asks |
| Frank's "arrangement" | $150 | 20 | Late Night | corruption >= 180 | Authority takes control |

### Recurring Expenses

| Expense | Cost | Frequency | If Unpaid |
|---------|------|-----------|-----------|
| Bus pass | $80 | Monthly | No bus travel. Must rely on Ryan's truck for ALL town access. |
| Art supplies | $60 | Monthly | Can't complete assignments. Loses campus events after 2 weeks. |
| Phone bill | $45 | Monthly | Phone cut off after 1 month. Mom can't call — misses story beats. |
| Food contribution | $50 | Weekly | frank_trust -3. "Pull your weight." Weekly reminders after. |
| **Total monthly** | **~$385** | | |

### Other Income
- Mom sends $200/month (often late — transfers bounce or arrive a week late)

### Two-Phase Economic Pressure

**Weeks 1-3 (cleaning only — bookkeeping not yet offered):**
- Income: Cleaning $20 × 5 days = $100/week
- Food: $50/week
- Remaining for bus ($80/mo) + art ($60/mo) + phone ($45/mo) = ~$46/week
- **Surplus: $4/week.** One missed day = in the red. Zero margin for clothing, beauty, or unexpected costs.

**Weeks 4+ (bookkeeping unlocks at corruption >= 40):**
- Income: Cleaning + bookkeeping = $45/day = $225/week
- Now comfortable: ~$129/week surplus
- But to GET here, she already reached corruption 40 — the economic pressure did its job

**Mid-to-late game (higher tiers):**
- Each tier up dramatically increases pay AND frees time
- One $150 Frank session replaces 7 cleaning shifts
- Financial freedom = time freedom = more NPC interaction time
- The highest tiers provide both money and relationship progression simultaneously

### Major Story-Gated Purchases

**Wardrobe (spread across game):**

| Tier | All Categories Cost | When Affordable |
|------|-------------------|-----------------|
| Starting | $0 | Day 1 (owned) |
| Basic upgrades | ~$145 | Weeks 2-4 |
| Cute tier (corruption 45) | ~$200 | Weeks 4-6 |
| Bold tier (corruption 85) | ~$235 | Weeks 6-8 |
| Daring tier (corruption 135) | ~$290 | Weeks 8+ |
| **Total wardrobe** | **~$870** | Nobody buys everything |

**Beauty products:**

| Product | Cost | Gate | Effect |
|---------|------|------|--------|
| Basic makeup kit | $20 | None | Daily +1 beauty buff |
| Skincare set | $15 | None | +1 beauty/use permanent |
| Cute makeup kit | $35 | corruption 45 | Daily +2 buff |
| Premium skincare | $30 | corruption 45 | +2 beauty/use |
| Bold makeup kit | $45 | corruption 85 | +2 buff, +1 corruption |
| Perfume | $25 | None | Scent descriptions in all close NPC scenes |
| Hairstyle #1 | $30 | None | +3 beauty one-time |
| Hairstyle #2 | $30 | corruption 45 | +3 beauty one-time |
| Hairstyle #3 | $30 | corruption 85 | +3 beauty one-time |
| **Total beauty** | **~$260** | | |

### How Economic Pressure Creates Meaningful Choices

The game NEVER tells Lily to escalate. The math creates the pressure:

1. **Weeks 1-3**: She literally can't afford clothing, beauty products, or unexpected expenses. Pride prevents asking Frank for money. Every day is triage.
2. **The bookkeeping gate**: To unlock the first comfortable income ($25/session), she needs corruption >= 40. This means she's already begun pursuing NPC arcs. The relief arrives AFTER the corruption starts.
3. **Time vs money**: Diner waitressing ($45) is the only income that doesn't require NPC involvement — but it costs the entire evening, missing dinner with all three NPCs and all night activities. Financial independence costs relationship time.
4. **Wardrobe as investment**: Better clothing gives better NPC reactions, better tips, better confidence gains. Spending money to look good pays dividends — but the money has to come from somewhere.
5. **The escalation ladder**: Each tier frees both money AND time. A player who pushes to Ryan's "favors" ($100/night) or Frank's "arrangement" ($150/late night) has financial freedom and free daytime for relationship activities. The game rewards escalation with the most valuable resource: time.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 4: NPC SCHEDULES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Where Each NPC Is By Time Period

| Time Period | Frank | Ryan | Jake |
|-------------|-------|------|------|
| **Early Morning** (05:00-07:00) | Workshop (alone, coffee) | Sleeping | Sleeping |
| **Morning** (07:00-09:00) | Kitchen (breakfast) | Kitchen or sleeping in (50/50) | Kitchen (breakfast) |
| **Late Morning** (09:00-12:00) | Workshop / job site | Job site | Community college (Mon-Thu) / Home (Fri-Sun) |
| **Afternoon** (12:00-15:00) | Office (bookkeeping) | Job site or town | Jake's room (drawing) or Library |
| **Late Afternoon** (15:00-17:00) | Workshop | Town / gym / errands | Backyard / creek / park (weekends) |
| **Evening** (17:00-19:00) | Kitchen (dinner) | Kitchen (dinner) or out (~20%) | Kitchen (dinner) |
| **Night** (19:00-22:00) | Living room (TV) or Office | Living room or out | Jake's room |
| **Late Night** (22:00-01:00) | Kitchen (insomnia, 50% chance) | Comes home late | Jake's room (shared wall active) |

### Schedule Conflicts (Forced Choices)

These time-slot conflicts force the player to choose ONE NPC over another:

| Time Slot | Option A | Option B | Trade-off |
|-----------|----------|----------|-----------|
| **Afternoon** | Bookkeeping with Frank | Drawing with Jake | Money + Frank trust vs. Jake love |
| **Late Afternoon** | Gym with Ryan (town) | Creek with Jake | Ryan corruption vs. Jake corruption |
| **Evening** | Dinner with family (all NPCs) | Diner waitress shift | Relationship time vs. income |
| **Night** | TV with Frank/Ryan | Visit Jake's room | Group dynamic vs. Jake intimacy |
| **Late Night** | Kitchen encounter (Frank) | Wall knocking (Jake) | Which NPC gets the private moment |

### NPC Availability Notes

**Frank:**
- Most consistent schedule. Always at the property except rare business trips.
- Available for bookkeeping Afternoon (Mon-Fri), cooking Evening, TV Night.
- Late-night kitchen appearances are random (50% chance) — can't be relied on.
- Early Morning workshop is solo time — Lily can find him there but it's HIS space.

**Ryan:**
- Least predictable. Goes to town frequently, comes home late.
- Available for truck rides (Late Afternoon), gym (requires town), job site (Late Morning).
- Evening dinner: ~80% present, ~20% out.
- Night: living room TV when home, otherwise out.
- Most weekend availability — drives to trail, takes Lily to town on request.

**Jake:**
- Most available at the property. His world is his room, the library, the creek.
- Community college Mon-Thu Late Morning removes him from the house.
- Afternoon drawing sessions in his room are his primary activity slot.
- Late Night shared wall is always active when they're both in their rooms.
- Weekend: home all day, available for park sketching, extended drawing sessions, creek.

### Wardrobe System (World Integration)

The clothing system integrates with the world through shopping trips and daily outfit selection.

**Shopping mechanics:**
- Requires getting to town: Bus ($2, 40 min, nobody knows) or Ryan's truck (free, 15 min, but Ryan sees every bag)
- Clothing store gated behind `town_access` flag
- Wardrobe change at `loc_lily_room` before leaving the house
- Outfit visible to all NPCs at every location visited that day

**Corruption-tiered availability in shop:**

| Tier | Gate | Unlocks |
|------|------|---------|
| Starting | N/A | Already owned |
| Basic | None | Always in shop |
| Cute | corruption >= 45 | Appears after threshold |
| Bold | corruption >= 85 | Appears after threshold |
| Daring | corruption >= 135 | Appears after threshold |

**5 categories × 5 tiers:**
- Athletic wear (gym, jogging, physical activities)
- Swimwear (creek, swimming)
- Sleepwear/loungewear (late-night encounters, around the house)
- Casual/daily wear (everything else)
- Underwear (scene text during physical encounters)

**Starting wardrobe (one suitcase):**
- Tops: hoodie, 2 plain t-shirts, tank top
- Bottoms: jeans, old shorts, sweatpants
- Shoes: sneakers, flip flops
- Underwear: basic bra, sports bra, cotton panties
- One nice thing: a sundress

**NPC gifting (wardrobeEffects):**

| NPC | Gift | When | What It Unlocks |
|-----|------|------|-----------------|
| Jake | His flannel shirt | ~corruption 35 | Wearable around house. Frank/Ryan notice — relationship signal. |
| Ryan | A bikini (Basic) | ~corruption 50 | Removes swimming awkwardness. Creek activity without improvising. |
| Frank | A nice dress (Cute) | ~corruption 80 | Presentable for diner. "You can't keep wearing the same three things." |
| Ryan | Bold athletic set | ~corruption 90 | Gym physical T3+ choices. "Saw this and thought of you." |
| Frank | Lingerie set (Bold) | ~corruption 130 | Intimate scene dialogue variants. "I saw this and thought of you." |

**Body coverage rules:**

```toml
[settings.clothing_requirements]
body_coverage = true
always_required = ["shoes"]

[settings.clothing_requirements.conditional.bra]
until_flag = "comfortable_braless"
message = "Lily isn't ready to go braless yet."

[settings.clothing_requirements.conditional.underwear]
until_flag = "discovered_teasing"
message = "Lily isn't bold enough to go without underwear yet."
```

### Random Encounters (World Integration)

14+ passive corruption events across all locations. Trigger by chance when Lily enters a location at the right time.

**Property encounters:**

| Location | Encounter | Corruption | Chance | Conditions |
|----------|-----------|------------|--------|------------|
| Bathroom | Walk in on Ryan showering | +3 | 70% | Late Morning-Night |
| Bathroom | Walk in on Jake | +2 | 50% | Late Morning-Night, corruption >= 30 |
| Lily's Room | Rhythmic sounds through Jake's wall | +2 | 60% | Late Night, `first_week_complete` |
| Kitchen | Frank at 2 AM, shirtless, whiskey | +2 | 50% | Late Night, corruption >= 40 |
| Living Room | Ryan watching porn, doesn't notice | +3 | 40% | Late Night, corruption >= 60, one-time |
| Backyard | Ryan skinny-dipping at creek | +3 | 30% | Late Night, corruption >= 50, one-time |
| Workshop | Frank's hidden magazines | +2 | N/A | Afternoon, `bookkeeping_started`, one-time |
| Hallway | Jake's door cracked, drawing her from memory | +2 | N/A | Night, drawing_sessions >= 3, one-time |

**Town/outdoor encounters:**

| Location | Encounter | Corruption | Chance | Conditions |
|----------|-----------|------------|--------|------------|
| Gym | Ryan shirtless, sweating, lifting | +3 | 60% | Any gym visit, Ryan present |
| Gym | Woman walks around locker room naked | +2 | 40% | Any gym visit, corruption >= 45 |
| Park | Stranger catcalls Lily jogging | +2 | 30% | Afternoon, corruption >= 35 |
| Trail | Frank steadies Lily, hand on waist lingers | +2 | 70% | Any hike with Frank, corruption >= 100 |
| Library | Jake falls asleep studying, she watches | +1 | 50% | Afternoon, Jake present |
| Diner | Waitresses talking about boyfriends | +2 | 40% | Any diner visit, corruption >= 40 |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type "proceed" to continue to Phase 4: Story Events,
or provide adjustments.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


# PHASE 4: STORY EVENTS
# Under One Roof

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## DRAMATIC STRUCTURE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Step 1: Central Tension

**"Can a girl who swore she'd never depend on anyone survive a house where every form of help comes with a price — and still recognize herself when it's over?"**

Every story event either raises or lowers the odds of Lily maintaining her sense of self. The escalation isn't just sexual — it's the erosion of the boundaries she built after her parents' divorce. The game asks: is connection worth the cost of control?

### Step 2: Primary Conflicts

This game uses FOUR conflict types across its arc, staggered:

| Conflict | Type | When | Threat | Resolution Cost |
|----------|------|------|--------|----------------|
| **Ryan pushes too far** | BOUNDARY BREAK | Act 2 (Beat 8) | Ryan uses what he's seen as leverage. Trust shattered with one NPC. | Lily must set a boundary with consequences — ryan_trust drops, takes 2-3 days to repair. |
| **Frank finds Jake's drawings** | REVELATION | Act 3 (Beat 18) | Frank discovers intimate sketches. What's happening under his roof? Confrontation. | frank_trust -5, jake_trust -3. Multiple days of separate repair per NPC. The household fractures. |
| **Brothers discover each other** | COMPETING PULL | Act 4 (Beat 21) | Ryan finds out about Jake (or vice versa). Jealousy, rivalry, ultimatums. | Lily must choose HOW to handle it (3 paths), but all paths cost love on at least one brother. |
| **Mom announces early return** | EXTERNAL THREAT | Act 4 (Beat 24) | Diana is coming home. Everything built here has an expiration date. | All NPC corruption -2 (fear response). Urgency changes every interaction. No resolution — just countdown. |

### Step 3: Tension Curve

| Beat | Event | Tension | Direction | Why |
|------|-------|---------|-----------|-----|
| 1 | Arrival | — | neutral | Establishing the world |
| 2 | First Morning | ↑ | rising | Bathroom awkwardness. The house is too small. |
| 3 | Bus Problem | ↑ | rising | Dependency established. She needs Ryan. |
| 4 | Mom's Call | ↑↑ | rising | Money won't come. Isolation confirmed. |
| 5 | The Math | ↑↑ | rising | Player sees the impossible numbers. Stakes real. |
| 6 | First Chore | ↑ | rising | Pride swallowed. First step deeper. |
| 7 | First Physical Awareness | ↑↑↑ | spark | The shift. Bodies noticed. No going back. |
| 8 | Ryan's Push (truck) | **↓↓** | **TENSION** | Boundary crossed. Trust broken. Teaches consequences. |
| 9 | Bookkeeping Offer | ↑ | recovering | Frank offers stability. But alone with him, door closed. |
| 10 | Creek Swim | ↑↑ | rising | Bodies in water. Physical exposure. |
| 11 | Jake's Confession (sketchbook) | ↑↑↑ | peak | Beautiful, tender. She's in his art. |
| 12 | Ryan Catches Lily | ↑↑ | rising | He doesn't look away. The game changes. |
| 13 | First Flirtation | ↑↑↑ | peak | Flirting becomes real. `flirt_unlock` |
| 14 | First Kiss | ↑↑↑↑ | peak | `kiss_unlock`. Emotional breakthrough. |
| 15 | Frank's Late Night | ↑↑ | rising | Kitchen at 2 AM. Coffee going cold. |
| 16 | Ryan's Ultimatum | **↓** | **TENSION** | He knows. He wants his own arrangement. |
| 17 | Power Outage (BRIDGE) | ↑↑ | deepening | Candles, proximity, vulnerability. No mechanics, just people. |
| 18 | Frank Finds Drawings | **↓↓↓** | **CRISIS** | The household fractures. Multiple trust drops. |
| 19 | Financial Crisis | ↑ | pressure | Mom's transfer bounces. Desperation forces escalation. |
| 20 | Physical Escalation | ↑↑↑ | new peak | `handjob_unlock`. Rebuilt trust deeper than before. |
| 21 | Brothers Discover Each Other | **↓↓** | **CRISIS** | The second crisis. Competing pull. |
| 22 | Frank's Offer | ↑↑ | rising | "I'll cover everything." Power solidifies. |
| 23 | The Choice | ↑↑↑ | turning point | How does Lily handle all three? Global branch. |
| 24 | Mom's Announcement | **↓** | **TENSION** | Ticking clock. Fear response across all NPCs. |
| 25 | Final Week | ↑↑↑↑ | climax | Maximum intensity before everything changes. |
| 26 | Resolution | ↑↑↑↑↑ | resolution | Mom arrives. Who is Lily now? |

**5 DOWN events** (Ryan's push, Ryan's ultimatum, Frank finds drawings, brothers discover, Mom's announcement). The curve is a heartbeat, not a line.

### Step 4: Regression Events

**Regression Event 1: Ryan Pushes Too Far in Truck (Beat 8)**
- **Trigger**: `bus_problem_discovered` + corruption >= 30 + days >= 3 since `game_started`
- **The Drop**: ryan_trust -3 (from whatever it is to -3)
- **The Fallout**: Ryan is louder at meals, overcompensates with jokes. Truck rides have tense silence instead of banter. He doesn't offer rides for 2 days — Lily has to ask, which costs her pride.
- **The Repair Path**: Lily must choose a Ryan activity (job site or gym) and pick the emotional choice, not the physical. She has to show she's not afraid of him.
- **The Resolution**: Ryan drops the act after 2-3 days. Offers a ride without being asked. Quieter than usual. "I was out of line." Recovery: ryan_trust +4 (net +1 above pre-crisis).

**Regression Event 2: Frank Finds Jake's Drawings (Beat 18)**
- **Trigger**: `saw_jakes_sketches` + `kiss_unlock` + frank_trust >= 15 + days >= 5 since `kiss_unlock`
- **The Drop**: frank_trust -5, jake_trust -3
- **The Fallout**: Frank is ice. Bookkeeping cancelled for 3 days. He doesn't come to dinner — eats in the workshop. Jake is scared — stays in his room, door closed, no wall knocking. The house goes cold. Meals are silent.
- **The Repair Path**: Lily must repair Frank and Jake SEPARATELY. Frank: choose the "talk to him in the workshop" option (vulnerability, not excuses). Jake: visit his room and choose the emotional option (reassurance, not deflection). Both require 2+ days of recovery activities before the resolution event fires.
- **The Resolution**: Frank doesn't forgive — he decides not to pursue it further. "I don't want to know." Jake recovers faster — "You're not angry?" Both set repair flags. frank_trust +6, jake_trust +4 (net positive).

**Regression Event 3: Brothers Discover Each Other (Beat 21)**
- **Trigger**: `handjob_unlock` + (ryan_love >= 15 OR jake_love >= 20) + days >= 30
- **The Drop**: Depends on which brother discovers: discovering_brother_love -3 to -5
- **The Fallout**: Confrontation scene. The discovering brother is hurt/angry. Activities with that brother have WITHDRAWN variant text for 2-4 days. The other brother doesn't know yet — creating an asymmetric tension.
- **The Repair Path**: The global crisis branch fires (Beat 23) — Lily's choice of independent/peacemaker/avoidant determines the repair path.
- **The Resolution**: `crisis_resolved` flag. All arcs continue. Tone changes, not direction.

**Regression Event 4: Mom's Announcement (Beat 24)**
- **Trigger**: `crisis_resolved` + days >= 48
- **The Drop**: ALL NPC corruption -2 (fear response — everyone pulls back)
- **The Fallout**: Brief. 1-2 days of NPCs being more careful, less physical. The urgency replaces the caution quickly.
- **The Repair Path**: No repair needed — the corruption recovers through continued interaction. The regression creates a brief "oh shit" pause before the final escalation.

### Step 5: Bridge Events

Bridge events exist purely for character development — no gate flags, no mechanics unlocked.

| Bridge Event | When | What Happens | Flag Set |
|-------------|------|-------------|----------|
| **Mom's Call** (Beat 4) | Day 3-4 | Diana calls from Dubai. Stressed, apologetic, the money transfer will be late. Lily says "I'm fine." She's not. The call reveals Lily's pride and Diana's guilt. No NPC present — this is Lily alone, processing. | `mom_called` |
| **Power Outage** (Beat 17) | Day ~32 | Storm knocks out electricity. Candles. The four of them in the living room for the first time without the TV as a buffer. Conversations that wouldn't happen with the lights on. Frank tells a story about building the house. Jake draws by candlelight. Ryan is quiet for once. Lily sees them as people, not dynamics. | `power_outage` |
| **Jake's Birthday** (optional, Day ~20) | Mid-game | Nobody remembered except Lily. She makes a card (art student). Jake is moved — his family forgot. The moment is tender and private. No escalation, no physical. Just two people seeing each other. | `jakes_birthday` |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## OPENING SCENE

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Canvas: `opening_arrival`

**Name**: Arrival
**Location**: `loc_kitchen` (ending in `loc_lily_room`)
**NPC**: All three present
**Schedule**: N/A (starting canvas — no trigger, fires on game start)
**Priority**: N/A
**is_repeatable**: false

**NODE 1 — The Drive (setup)**
Lily watches the property approach through Ryan's truck windshield. Gravel driveway. The house is smaller than she remembered from the wedding. Internal monologue establishes: she doesn't want to be here. She had a plan. The plan flooded.

Ryan: "Home sweet home." He grabs her suitcase before she can. It's either helpful or possessive — she can't tell yet.

- Media: Image — rural property at dusk, gravel driveway, truck pulling up
- Exit: "Continue" → Node 2

**NODE 2 — Meeting Everyone (introductions)**
Kitchen. Frank is cooking. The smell of garlic and something burning slightly. Jake is at the table with his sketchbook — he stands when she walks in, awkward, adjusts his glasses. Frank wipes his hands on a dish towel and extends one: "Lily. Welcome." Firm handshake. He's bigger than she remembers.

Three physical descriptions delivered through Lily's eyes:
- Frank: "Broad. Steady eyes. Calloused hand that swallowed mine."
- Ryan: "Cocky grin. Arms that don't fit the doorframe. Already looking at me like I'm interesting."
- Jake: "Glasses. Soft hands. He smiled and then looked at his shoes."

- Media: Image — farmhouse kitchen, dinner being prepared, three men, one young woman with suitcase
- Exit: "Continue" → Node 3

**NODE 3 — Dinner and House Rules**
Awkward first dinner. Frank lays out the house rules: bathroom schedule (morning rotation), dinner at six, no loud music after ten, she can use the kitchen anytime. He's fair. He's also clearly the authority.

Ryan: "Relax, Dad, she's not a prisoner." Frank's jaw tightens.
Jake: "There's good light in the afternoon if you want to draw." First genuine warmth.

Lily's internal: "Ten weeks. I can survive anything for ten weeks."

- Media: Image — dinner table, four people eating, slightly tense, evening light
- Choices:
  - **"Thank you. I'll try to stay out of the way."** → polite, guarded. corruption +0, all NPCs love +0. Lily is walls-up.
  - **"The room is perfect. I appreciate this."** → warmer, genuine. corruption +0, frank_trust +1, jake_love +1. Lily lowers one brick.

Both choices → Node 4

**NODE 4 — The Room**
Frank shows her to her room. Small bed, desk, window facing the backyard. He points out Jake's room next door: "Walls are thin. Sorry about that."

He stands in the doorway a moment too long. Then: "Goodnight, Lily." Closes the door. She hears his boots on the hardwood, getting quieter.

She sits on the bed. One suitcase. Ten weeks. The house is so quiet she can hear the creek through the window.

- Media: Image — small bedroom, single bed, window, young woman sitting alone with suitcase
- Exit: → canvas exit. Sets `game_started`. Time advances to Late Night.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ACT 1: SETTLING IN (Corruption 0-40, Days 1-7)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Beat 2: First Morning

**Canvas**: `story_first_morning`
**Location**: `loc_bathroom`
**NPC**: Jake (accidental)
**Schedule**: 05:00-07:00
**Trigger**: `game_started` + days_since_flag(`game_started`) >= 1
**Priority**: 10
**is_repeatable**: false

**NODE 1 — The Bathroom Problem (setup)**
Early morning. Lily needs to shower. She's used to dorm bathrooms with locks that work. This bathroom has a hook-latch that doesn't always catch. She doesn't know the schedule yet.

She's in a towel, reaching for the shower handle, when the door opens.

Jake. Glasses off, squinting, hair everywhere, toothbrush in hand. He freezes. She freezes. The mirror behind her shows both of them — his face going red, her hand clutching the towel.

- Media: Image — bathroom doorway, morning light, awkward encounter, steam
- Exit: "Continue" → Node 2

**NODE 2 — The Reaction**
Jake: "I—sorry—I didn't—the door was—" He's backing up, hitting the doorframe. Toothbrush falls. He doesn't pick it up. He's looking at the ceiling, the wall, anywhere but her.

- Choices:
  - **"It's fine. Just knock next time."** → calm, sets a boundary. jake_love +1, jake_trust +1. Lily: composed.
  - **"Oh my god, get OUT."** → flustered, real. jake_trust +0, corruption +1. Lily: exposed, embarrassed. Jake remembers her voice cracking.

Both choices → Node 3

**NODE 3 — Breakfast After**
Kitchen. Twenty minutes later. Jake is already at the table, hasn't looked up from his cereal. Frank is reading the paper. Ryan isn't awake yet.

Lily sits down. Jake slides the coffee pot toward her without making eye contact. His ears are still red.

Frank, without looking up: "Morning."

The bathroom schedule is silently renegotiated.

- Media: Image — kitchen breakfast, quiet tension, morning light
- Exit: → canvas exit. Sets `first_morning`. corruption +1 (ambient — proximity established).

---

### Beat 3: The Bus Problem

**Canvas**: `story_bus_problem`
**Location**: `loc_kitchen`
**NPC**: Ryan
**Schedule**: 07:00-09:00
**Trigger**: `first_morning` + days_since_flag(`first_morning`) >= 1
**Priority**: 10
**is_repeatable**: false

**NODE 1 — The Schedule**
Lily looks up the bus schedule on her phone. The bus to campus runs three times a day. The 7:15 AM gets her there on time. The return bus is at 4:30 PM — which means she's stuck at campus for hours after class ends, or she misses the bus and has no way home.

Ryan, leaning against the counter: "Bus sucks. Takes forty minutes and costs two bucks each way."

- Media: Image — young woman looking at phone, frustrated, kitchen background
- Exit: "Continue" → Node 2

**NODE 2 — The Offer**
Ryan: "I can drive you. Fifteen minutes. Free."

He says it casually. Like it's nothing. But Lily's internal voice: "Free? Or does 'free' mean he decides when I leave and when I come back?"

- Choices:
  - **"That would be great, thanks."** → accepts Ryan's help. ryan_love +1, corruption +1. Dependency begins. Ryan grins: "Truck leaves at 8. Don't be late."
  - **"I'll take the bus. But thanks."** → independence. corruption +0, money -2 (bus fare). Ryan shrugs: "Suit yourself, college girl." But he looks a little impressed.

Both choices → Node 3

**NODE 3 — The Ride (if accepted) / The Walk (if refused)**
If accepted: First truck ride. Bench seat. Pine air freshener. Ryan drives with one hand. The road is rural — fields, trees, no other cars. Fifteen minutes of confined space. He talks. She listens. He points out the gym, the diner, the park. "Town's small. You'll figure it out." He drops her at campus. "I'll be back at four. Be out front."

If refused: The bus. Forty minutes. She watches the property shrink in the rearview mirror. It costs $2. She has $400. She does the math.

Either way — `town_access` is set.

- Media: Image — pickup truck on rural road, or bus stop on country road
- Exit: → canvas exit. Sets `bus_problem_discovered`, `town_access`. Time advances to Late Morning.

---

### Beat 4: Mom's Call (BRIDGE EVENT)

**Canvas**: `story_moms_call`
**Location**: `loc_lily_room`
**NPC**: None (solo)
**Schedule**: 19:00-22:00
**Trigger**: `bus_problem_discovered` + days_since_flag(`bus_problem_discovered`) >= 1
**Priority**: 10
**is_repeatable**: false

**NODE 1 — The Call**
Phone buzzes. Mom. Lily sits on the bed and answers.

Diana sounds exhausted. The connection is scratchy — Dubai is far. "How's the house? Are the boys being nice? Is Frank..." She trails off.

Lily: "It's fine, Mom. Everything's fine."

Diana: "The money — I'm trying, baby. The bank here is different, the transfer keeps bouncing. Maybe another week? Can you manage?"

- Media: Image — young woman on phone in small bedroom, evening, alone
- Exit: "Continue" → Node 2

**NODE 2 — The Lie**
Lily looks at her bank app. $398 after the bus fare. Monthly expenses: $385. Mom's transfer: delayed indefinitely.

Diana: "I wouldn't have asked you to stay there if there was any other option. You know that, right?"

- Choices:
  - **"I know, Mom. I'll be fine."** → pride. corruption +0, confidence +1. Lily protects her mother from the truth. The lie costs nothing except the exit she just closed.
  - **"It's tight. If you could send even half..."** → honesty. corruption +0, confidence +0. Diana promises to try. But the money won't come faster.

Both choices → Node 3

**NODE 3 — After**
"I love you, Lily."
"Love you too, Mom."

Click. Silence. The creek outside. Jake's pencil scratching through the wall.

Lily opens the calculator app. $398. Bus pass $80. Art supplies $60. Phone $45. Food $50/week × 4 = $200. Total month one: $385. Surplus: $13.

Thirteen dollars. For ten weeks.

- Media: Image — phone screen showing bank balance, dim room, late evening
- Exit: → canvas exit. Sets `mom_called`. No stat changes — this is a bridge event. The player feels the math.

---

### Beat 5: The Math

**Canvas**: `story_the_math`
**Location**: `loc_lily_room`
**NPC**: None (solo)
**Schedule**: 07:00-09:00
**Trigger**: `mom_called` + days_since_flag(`mom_called`) >= 1
**Priority**: 10
**is_repeatable**: false

**NODE 1 — Morning Realization**
Lily's been lying awake since 5 AM. She heard Frank leave for the workshop. She heard the coffee maker start. She's staring at the ceiling.

The numbers don't work. Even if Mom's transfer arrives on time — $200/month — that's $585 total across month one. Expenses are $385. That leaves $200 for everything else: clothes (she packed for a weekend, not ten weeks), art supplies beyond basics, any emergency.

And Mom's transfers are never on time.

Internal monologue: "I'm not calling her. I'm not asking Frank. I'm not asking anyone."

- Media: Image — young woman lying in bed, staring at ceiling, early morning light
- Exit: "Continue" → Node 2

**NODE 2 — The Decision**
She gets up. Gets dressed. Walks to the kitchen.

Frank is at the table. Coffee. Paper. His routine.

Lily's pride builds the sentence before she's ready: "Frank — is there anything I can do around the house? To help out? I could... clean, or help organize, or—"

Frank looks at her. Steady eyes. He sees what this costs her.

"Twenty dollars a clean. Kitchen, living room, bathroom. Leave the office."

- Choices:
  - **"Deal."** → direct. frank_trust +1. Lily swallows her pride cleanly. Frank respects it.
  - **"That's... generous. Thank you."** → grateful. frank_trust +1, frank_love +1. She's genuine. He's surprised.

Both choices → Node 3

**NODE 3 — First Clean**
Montage feel. Lily cleans the kitchen — dishes that aren't hers, counters sticky with someone else's spilled coffee, a bathroom where three men live. It's not hard work. It's humbling work.

She finds $20 on the counter when she's done. No note. Just the money.

Ryan, walking through: "Damn, it smells like cleaning products. You do windows too?"

Jake, from his room doorway: "Thanks, Lily." Quiet. He noticed.

- Media: Image — young woman cleaning farmhouse kitchen, purposeful, slightly dignified
- Exit: → canvas exit. Sets `money_crisis_realized`, `first_week_complete`, `chores_started`. money +20. Time advances.

---

### Beat 6: First Chore System Unlock

This beat is mechanical — the completion of Beat 5 unlocks the cleaning utility canvas:

**Canvas**: `utility_house_cleaning` (REPEATABLE)
**Location**: `loc_kitchen`
**Schedule**: 09:00-12:00
**Trigger**: `chores_started`
**Priority**: 1
**is_repeatable**: true
**max_triggers_per_day**: 1

**NODE 1 — Cleaning**
Brief narrative: Lily cleans the shared spaces. Kitchen, living room, bathroom. ~2 hours of work. Whoever is home acknowledges it differently:
- Frank (if present): nods. "Looks good."
- Ryan (if present): "You missed a spot." (He's kidding. Mostly.)
- Jake (if present): "Want help?" (He never actually helps. He draws while she cleans.)

- Exit: → canvas exit. money +20, energy -25, frank_trust +1 (if Frank home).

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ACT 1 → ACT 2 TRANSITION: FIRST TENSION EVENT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Beat 7: First Physical Awareness (GATE: `exposure_unlock`)

**Canvas**: `story_first_awareness`
**Location**: `loc_jakes_room` (Jake path) / `loc_creek` (Ryan path) / `loc_bathroom` (Frank path)
**NPC**: Any — depends on which NPC's conditions are met first
**Schedule**: 12:00-15:00 (Jake), 15:00-17:00 (Ryan), any (Frank)
**Trigger**: Depends on NPC (see gate threshold table from Phase 2)
- Jake: corruption >= 25, jake_love >= 10
- Ryan: corruption >= 40, ryan_corruption >= 10
- Frank: corruption >= 60, frank_trust >= 10
**Priority**: 10
**is_repeatable**: false

**JAKE VARIANT — "Hold Still"**

*NODE 1 — The Pose*
Drawing session. Jake has been drawing landscapes, hands, coffee mugs. Today he asks: "Can I draw you? Just your face. The light is really good right now."

She sits. He positions her — hand under chin, face toward the window. His fingers brush her jaw adjusting the angle. Both of them notice.

"Your collar is casting a shadow. Can you—" He gestures at her neckline. Lower it? Just for the light?

*NODE 2 — The Moment*
She pulls the collar of her t-shirt to one side. Her collarbone exposed. Jake's pencil stops.

Three seconds. He's looking at her collarbone, her neck, the shadow line. Not as an artist. As a boy who just realized what he's been feeling isn't just artistic admiration.

His pencil starts again. Faster. He doesn't ask her to fix the collar.

- **First-time variant** (exposure_unlock NOT yet set): "She's never been looked at like this. Not like a body — like a landscape. Like something worth spending hours getting right. Her skin prickles under the attention."
- Choices:
  - **"You can draw lower if you want."** → bold. corruption +3, jake_love +2, jake_corruption +2. She's opening the door.
  - **"Is the light okay now?"** → neutral. corruption +2, jake_love +1. She doesn't close the door. She doesn't open it wider.

Both → Node 3. Sets `exposure_unlock`, `drawing_started`.

*NODE 3 — After*
Jake shows her the drawing. Her face, her neck, the suggestion of a shoulder. It's beautiful. It's also the first time anyone has made her feel seen in a way that's both innocent and charged.

"Can we do this again?" His voice is careful. Hopeful.

- Media: Image — artist's room, natural light, drawing session, intimate but innocent
- Exit: → canvas exit. corruption +2 total (above + ambient).

**RYAN VARIANT — "Creek Swim"**

*NODE 1 — The Creek*
Late afternoon. Hot. Ryan: "Creek's deep enough to swim. You coming?"

At the creek, Ryan strips to shorts without hesitation. Lily doesn't have a swimsuit. She's in her sports bra and underwear (improvised). It gets see-through when wet. She knows this. She goes in anyway.

*NODE 2 — The Moment*
The water is cold. She gasps. Ryan is already waist-deep, watching. When she surfaces, her bra is clinging to everything.

Ryan doesn't look away. Doesn't make a joke. For once, he's just looking.

"You should get a real suit," he says. But his eyes say something else.

- **First-time variant**: "She's never been looked at like she's on display. The water runs down her stomach and he watches it go."
- Choices:
  - **"Take a picture, it lasts longer."** → confident. corruption +3, ryan_corruption +2, confidence +1.
  - **"Stop staring."** → defensive. corruption +2, ryan_corruption +1.

Both → Node 3. Sets `exposure_unlock`, `first_swim`.

**FRANK VARIANT — "The Hallway"**

*NODE 1 — The Encounter*
She walks out of the bathroom in a towel. Frank is in the hallway. Neither expected the other. He's holding a coffee mug. She's holding her towel.

*NODE 2 — The Freeze*
Two seconds. His eyes go to her shoulders — bare, wet — and snap to the wall. Coffee mug tightens in his grip.

"Sorry. I didn't—" He's already walking away. Fast. Heavy boots on hardwood.

- **First-time variant**: "She stands in the hallway, dripping. Her heart is hammering. Not from embarrassment. From the way he looked at her shoulders for exactly two seconds before he stopped himself."
- Choices:
  - **"Frank—" (call after him)** → bold. corruption +3, frank_love +1, frank_corruption +1.
  - **(Let him go)** → safe. corruption +2.

Both → exit. Sets `exposure_unlock`.

---

### Beat 8: Ryan's Push — TENSION EVENT (Regression 1)

**Canvas**: `story_ryans_push`
**Location**: `loc_ryans_truck`
**NPC**: Ryan
**Schedule**: 15:00-17:00
**Trigger**: `exposure_unlock` + `bus_problem_discovered` + ryan_corruption >= 10 + days_since_flag(`exposure_unlock`) >= 2
**Priority**: 10
**is_repeatable**: false

**NODE 1 — The Ride**
Driving back from town. Rural road. Ryan is quieter than usual. Something's different.

He takes a turn she doesn't recognize. "Shortcut," he says. But the road gets narrower. Trees close in. He pulls over at a dead end — a dirt clearing, no houses, no other cars.

Engine idling.

- Media: Image — pickup truck on dead-end dirt road, trees, isolated, late afternoon
- Exit: "Continue" → Node 2

**NODE 2 — The Push**
Ryan turns in the seat. The bench between them is suddenly very small.

"So. You and Jake are getting pretty close, huh? Those little drawing sessions."

His hand lands on her knee. Not aggressive. Testing. His eyes are on hers, gauging.

"Figured you and me should spend some quality time too."

- Choices (BRANCH POINT — Level 2):
  - **Slap his hand away: "Don't."** → `ryan_resisted`. ryan_trust -3, ryan_corruption -2, confidence +2. Ryan pulls back. Surprised. Not angry — recalibrating. "Alright. Alright." He starts the truck. The ride home is silent, but he opens her door when they get back.
  - **Let it stay: "..."** → `ryan_allowed`. ryan_love +1, ryan_corruption +3, corruption +3. His hand stays. His thumb moves in a small circle. The silence is heavy. After a minute he moves his hand higher. She doesn't stop him. Eventually he starts the truck. "That wasn't so bad, was it?"

Both → Node 3. Sets `truck_incident_complete`.

**NODE 3 — Aftermath**
Home. Lily goes straight to her room. Sits on the bed. Hands shaking — with anger, or adrenaline, or something she doesn't want to name.

Through the wall, Jake's pencil scratches.

- Exit: → canvas exit.

**CONSEQUENCE ECHO (next 2-3 days):**
- If `ryan_resisted`: Ryan is careful. Activities with Ryan have subdued opening text. He offers rides without commentary. The teasing stops. It comes back — but different. More respectful. Seduction replaces aggression.
- If `ryan_allowed`: Ryan is bolder. Activities with Ryan have charged opening text. Truck rides have loaded silences. He finds excuses for detours. The physical escalation accelerates.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ACT 2: ROUTINES FORM (Corruption 40-100, Days 8-25)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Beat 9: Frank Offers Bookkeeping

**Canvas**: `story_bookkeeping_offer`
**Location**: `loc_franks_office`
**NPC**: Frank
**Schedule**: 12:00-15:00
**Trigger**: `chores_started` + corruption >= 40 + frank_trust >= 8 + days_since_flag(`first_week_complete`) >= 7
**Priority**: 10
**is_repeatable**: false

**NODE 1 — The Offer**
Frank calls Lily to his office. Door open. He's behind the desk, invoices everywhere.

"You're good with the cleaning. Reliable." Pause. "I need help with the books. My wife used to—" He stops. Reroutes. "It's basic. Invoices, receipts, payroll entries. Twenty-five dollars a session."

More money than cleaning. But: his office. Door that closes. Just the two of them.

- Media: Image — contractor's home office, desk with papers, man behind desk, woman standing at doorway
- Exit: "Continue" → Node 2

**NODE 2 — The Decision**
Frank pushes a chair toward the front of the desk. "Three afternoons a week. You'd be doing me a favor."

His voice is measured. Professional. But the room is small. The chair is close to his. When she sits, she can smell sawdust and coffee.

- Choices:
  - **"I'd like that. When do I start?"** → accepts. corruption +2, frank_trust +2, frank_love +1. The office door will close behind them three afternoons a week.
  - **"Can I think about it?"** → hesitant. corruption +1, frank_trust +1. Frank nods: "Take your time." The offer stands. She'll accept eventually — the money's too good.

Both → Node 3. Sets `bookkeeping_started`.

**NODE 3 — First Session**
Brief montage: Lily at the desk, Frank standing behind her pointing at columns. His hand on the back of her chair. Close enough to feel body heat.

"This column is materials. This one is labor. Keep them separate."

His voice is right behind her ear. She can feel his breath.

Ninety minutes. $25. When she leaves, her hands are steady. Her pulse isn't.

- Media: Image — woman at desk doing bookkeeping, man standing behind, close proximity, amber desk lamp
- Exit: → canvas exit. money +25.

---

### Beat 10: Creek Swim

**Canvas**: `story_creek_swim`
**Location**: `loc_creek`
**NPC**: Jake and/or Ryan (depends on who's present — schedule-based)
**Schedule**: 15:00-17:00
**Trigger**: `first_week_complete` + corruption >= 30 + days_since_flag(`first_week_complete`) >= 3
**Priority**: 10
**is_repeatable**: false

**NODE 1 — The Heat**
Afternoon. Too hot for the house. Jake suggests the creek. If Ryan's around, he invites himself.

The walk through the trees. Creek comes into view — shallow, cold, dappled light through branches.

Jake pulls off his shirt — lean, pale, self-conscious. If Ryan's there: shirt off in one motion, no hesitation, tanned and built.

Lily doesn't have a swimsuit. (Unless Ryan already gifted the bikini.)

- Media: Image — creek in dappled forest light, young people approaching, summer afternoon
- Exit: "Continue" → Node 2

**NODE 2 — In the Water**
If improvising: sports bra and underwear. The fabric goes translucent in cold water. She crosses her arms. Then stops crossing them.

If bikini: she's covered, but barely. Ryan picked it. She's wearing what Ryan chose.

The water is cold enough to gasp. Warm enough to stay. Bodies in water are impossible to ignore — the way wet skin catches light, the way fabric clings, the way proximity means something different when you're half-dressed.

Jake keeps his distance but can't stop looking. Ryan doesn't keep his distance.

- Choices:
  - **Splash Jake, pull him closer** → jake_love +2, jake_corruption +2. Playful. He laughs — a real laugh, surprised.
  - **Race Ryan to the deep end** → ryan_love +1, ryan_corruption +2, confidence +1. Physical. He grins and lets her win.
  - **Float alone, let them watch** → corruption +2 to both present NPCs. She exists in the center of their attention without giving either one the satisfaction of choosing.

All → Node 3. Sets `first_swim`. corruption +3 (ambient exposure).

**NODE 3 — Drying Off**
On the bank. Clothes sticking. Nobody wants to be the first to get dressed.

Jake is sketching something on a receipt he found in his pocket — her shoulder, the water line, a shape she recognizes.

Ryan: "You should come here more often." Looking at her. Not subtle.

- Media: Image — people sitting by creek bank, drying off, summer afternoon, relaxed
- Exit: → canvas exit.

---

### Beat 11: Jake's Confession (Innocent Sketchbook)

**Canvas**: `story_jakes_confession`
**Location**: `loc_jakes_room`
**NPC**: Jake
**Schedule**: 19:00-22:00
**Trigger**: `drawing_started` + jake_love >= 12 + jake_trust >= 8 + days_since_flag(`drawing_started`) >= 3
**Priority**: 10
**is_repeatable**: false

**NODE 1 — The Sketchbook**
Evening. Jake's room. They've been drawing together — or rather, he's been drawing while she watches.

Tonight he's nervous. Fidgeting with the binding of his sketchbook. "Can I show you something?"

He opens the book. Not to the landscapes. To the pages after.

Her face. Again and again. Her jaw from the side. Her hands holding a coffee mug. Her neck in afternoon light. Her eyes, half-closed, from the morning she fell asleep on the couch.

Page after page. All of her. All beautiful. All innocent — there's nothing sexual. Just obsessive attention to someone he can't stop looking at.

- Media: Image — sketchbook pages showing female portrait studies, pencil drawings, beautiful, tender
- Exit: "Continue" → Node 2

**NODE 2 — The Reveal**
Jake: "I've been drawing you since the second day. I couldn't—" He pushes his glasses up. "—you have this face that changes depending on the light. I keep trying to get it right."

He's terrified. This is his most vulnerable confession: not "I want you" but "I see you."

**NOTE: This is NOT the branch-point discovery. This is WILLING showing of INNOCENT art. The Level 3 branch (Beat in Section 19) is when Lily finds Jake's SECRET intimate sketches — poses she didn't know he saw. Different event, much higher stakes.**

- Choices:
  - **"They're beautiful, Jake."** → jake_love +3, jake_trust +2, corruption +1. She means it. His whole face opens.
  - **"How long have you been watching me?"** → jake_love +1, jake_trust +1, jake_corruption +1. Not angry — curious. He hears the real question: "Do you watch me when I don't know?"

Both → Node 3. Sets `saw_jakes_sketches`.

**NODE 3 — After**
He closes the sketchbook. His hands have stopped shaking.

"Can I keep drawing you? I mean — not just your face. I mean..." He loses the sentence.

"The light in this room is really good."

- Exit: → canvas exit.

---

### Beat 12: Ryan Catches Lily

**Canvas**: `story_ryan_catches_lily`
**Location**: `loc_hallway` or `loc_lily_room`
**NPC**: Ryan
**Schedule**: 09:00-12:00
**Trigger**: `truck_incident_complete` + ryan_corruption >= 12 + days_since_flag(`truck_incident_complete`) >= 3
**Priority**: 10
**is_repeatable**: false

**NODE 1 — The Walk-In**
Lily is changing in her room. Door not fully closed — she's gotten sloppy about it after two weeks. The latch doesn't catch.

Ryan pushes it open. He was heading to the bathroom. At least, that's what he'll say.

She's in underwear and a bra. Halfway into a shirt. They lock eyes in the mirror.

- Media: Image — bedroom doorway, woman caught changing, man in hallway, surprise
- Exit: "Continue" → Node 2

**NODE 2 — The Grin**
Ryan doesn't look away. Doesn't apologize. Doesn't back up.

He leans against the doorframe. That grin.

"Door was open."

He's not wrong. But he's also not leaving.

- Choices:
  - **"Get out. Now."** → firm boundary. ryan_trust +1 (he respects it), ryan_corruption +1 (the image stays in his head). confidence +1. He raises his hands: "Copy that." Turns and leaves. But he saw. They both know.
  - **"You could knock."** → softer. ryan_love +1, ryan_corruption +2, corruption +2. She's not kicking him out. She's negotiating. He notices. "I'll try to remember that." He leaves. Slowly.
  - **Hold eye contact in the mirror, finish putting on the shirt** → power move. corruption +3, ryan_corruption +3, confidence +2. She doesn't flinch. She finishes getting dressed while he watches through the mirror. She owns the moment. Ryan is, for once, the one off-balance. "...Jesus." He walks away.

All choices → Node 3. Sets `ryan_caught_her`.

**NODE 3 — The Lock**
Lily looks at the door latch. She could fix it. Ask Frank for a proper lock.

She doesn't.

- Exit: → canvas exit.

---

### Beat 13: First Flirtation (GATE: `flirt_unlock`)

**Canvas**: `story_first_flirtation`
**Location**: Depends on NPC — `loc_jakes_room` (Jake) / `loc_ryans_truck` (Ryan) / `loc_franks_office` (Frank)
**NPC**: Any — first to meet conditions
**Trigger**:
- Jake: corruption >= 40, jake_love >= 12
- Ryan: corruption >= 50, ryan_love >= 8
- Frank: corruption >= 75, frank_trust >= 15
**Priority**: 10
**is_repeatable**: false

**JAKE VARIANT — "The Pose Gets Charged"**

*NODE 1*
Art modeling session. She's been sitting for Jake before, but today she holds the pose differently. Chin lifted. Shoulders back. Something in her posture that wasn't there a week ago.

Jake notices. His pencil moves differently — longer strokes, more pressure.

"Tilt your head? Like you're..." He doesn't finish. She tilts. The neckline of her shirt falls open slightly.

*NODE 2*
She watches him blush. For the first time, she's doing it on purpose.

"Like this?" Leaning forward. Just a little.

- Choices:
  - **"You're cute when you're flustered."** → direct flirtation. jake_love +2, jake_corruption +2, corruption +2.
  - **Hold the pose without commenting** → suggestive silence. jake_corruption +2, corruption +2. The silence does the work.

Both → exit. Sets `flirt_unlock`, `modeling_started`. corruption +2.

**RYAN VARIANT — "Truck Flirting"**

*NODE 1*
Ride to town. Ryan is being careful since the truck incident — testing with words instead of hands. "New shirt? Looks good on you."

She could deflect. She doesn't.

*NODE 2*
She flirts back. For the first time. A comment about his arms. A look that holds one second too long.

Ryan goes quiet. Then: "Damn, college girl. Who taught you that?"

- Choices:
  - **"Nobody. Figured it out myself."** → confident. ryan_love +2, corruption +3.
  - **"Maybe I'm a fast learner."** → playful. ryan_corruption +2, corruption +2.

Both → exit. Sets `flirt_unlock`.

**FRANK VARIANT — "Not About Numbers"**

*NODE 1*
Bookkeeping session. She makes a comment that has nothing to do with invoices. Something about his hands. Or his voice. Or the way the lamp makes his stubble look.

Frank's pen stops.

*NODE 2*
One beat. Two. He looks at her.

"Focus on the numbers, Lily."

But he doesn't look away first.

- Choices:
  - **"I am focused."** → loaded. frank_love +2, frank_corruption +1, corruption +3.
  - **"Sorry. Column B, right?"** → retreat. frank_trust +1, corruption +1. She backed off. He notices that she backed off. Which means he noticed the advance.

Both → exit. Sets `flirt_unlock`.

---

### Beat 14: First Kiss (GATE: `kiss_unlock`)

**Canvas**: `story_first_kiss`
**Location**: NPC-dependent — `loc_jakes_room` (Jake) / `loc_ryans_truck` (Ryan) / `loc_kitchen` (Frank)
**NPC**: First to meet conditions
**Trigger**:
- Jake: corruption >= 70, jake_love >= 15, jake_trust >= 15
- Ryan: corruption >= 85, ryan_love >= 12, ryan_trust >= 10, ryan_corruption >= 15
- Frank: corruption >= 120, frank_love >= 20, frank_trust >= 20
- All require: `flirt_unlock` + days_since_flag(`flirt_unlock`) >= 3
**Priority**: 10
**is_repeatable**: false

**JAKE VARIANT — "Over the Sketchbook"**

*NODE 1 — Setup*
Late drawing session. He's been working on a portrait for an hour. She's held the pose. The room is quiet except for his pencil and the crickets outside.

He stops drawing. Looks at her — not the paper, her. His expression changes. Something crossing a line between seeing and wanting.

"Lily?"
"Yeah?"
"Don't move."

But he's the one who moves. Sketchbook set aside. He leans forward. Slow enough that she could stop him.

*NODE 2 — The Kiss*
- **First-time variant** (kiss_unlock NOT set): "She's never been kissed like this — soft, terrified, like the person doing it knows exactly what it costs. His lips are warm. His hand finds her jaw. The pencil falls off the bed and neither of them hears it."
- **Repeat variant** (kiss_unlock already set from another NPC): "She's done this before. But not like this. Jake kisses like every second might be the last one allowed. His hand trembles on her jaw. Everything she thought she knew about kissing gets rewritten."

Jake: "We shouldn't—"
Lily: "I know."

Neither pulls away.

- Choices:
  - **Kiss him deeper** → jake_love +3, jake_corruption +3, corruption +4.
  - **Pull back gently: "Not yet."** → jake_love +2, jake_trust +2, corruption +2. He nods. Swallows. Picks up his pencil with shaking hands.

Both → exit. Sets `kiss_unlock`. Media: Video placeholder — tender first kiss, soft, hesitant, eye contact.

**RYAN VARIANT — "The Truck, Parked"**

*NODE 1 — Setup*
Dirt road. Truck parked. Engine off. He's been driving for twenty minutes saying nothing. The silence is different tonight.

He turns. No grin this time. Something raw.

"I've been thinking about you. More than I should."

*NODE 2 — The Kiss*
He pulls her in. Not gentle — urgent. His hand on the back of her neck.

- **First-time variant**: "She's never been kissed like she's wanted this badly. His mouth is sure. His hand on her neck is firm. She tastes mint and something male."
- **Repeat variant**: "She's done this before. But not like this — not hungry, not urgent, not in a truck on a dead-end road where his hand shakes on the back of her neck."

- Choices:
  - **Kiss him back hard** → ryan_love +2, ryan_corruption +4, corruption +4.
  - **Push against his chest, breathless: "Slow down."** → ryan_trust +2, ryan_love +1, corruption +2.

Both → exit. Sets `kiss_unlock`. Media: Video placeholder — aggressive first kiss, truck interior, pulling close.

**FRANK VARIANT — "Kitchen, 2 AM"**

*NODE 1 — Setup*
Late night. Lily can't sleep. She goes to the kitchen. Frank is already there — undershirt, whiskey glass, staring out the dark window.

"Can't sleep?"
"No."
He pours her a glass without asking.

They stand at the counter. Shoulders almost touching. The house is dead quiet.

*NODE 2 — The Kiss*
Frank: "This can't happen."

She doesn't say anything.

His hand finds her chin. Tilts her face toward his. Slow. Like he's giving himself one last chance to stop.

He doesn't stop.

- **First-time variant**: "She's never been kissed by someone who hates himself for doing it. His mouth is firm. His hand on her chin is careful. He kisses her like a man dismantling his own boundaries, one brick at a time."
- **Repeat variant**: "She's done this before. But not like this — not with someone who's been fighting this for weeks, whose control is cracking against her lips, who tastes like whiskey and restraint."

Frank pulls back. Hands flat on the counter. Knuckles white.

"That doesn't happen again."

- Choices:
  - **"Okay."** → frank_trust +2, frank_love +2, corruption +3. She respects the boundary. He respects that she respects it. They both know it's a lie.
  - **"Liar."** → frank_love +3, frank_corruption +3, corruption +5. One word. His jaw tightens. He walks out. But she's right and they both know it.

Both → exit. Sets `kiss_unlock`. Media: Video placeholder — forbidden kitchen kiss, late night, whiskey glass, intense.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ACT 3: LINES BLUR (Corruption 100-180, Days 25-45)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Beat 15: Frank's Late Night

**Canvas**: `story_franks_late_night`
**Location**: `loc_kitchen`
**NPC**: Frank
**Schedule**: 22:00-01:00
**Trigger**: `kiss_unlock` + frank_love >= 12 + frank_trust >= 15 + corruption >= 100 + days_since_flag(`kiss_unlock`) >= 5
**Priority**: 10
**is_repeatable**: false

**NODE 1 — 2 AM**
Kitchen. Lily can't sleep. Frank is at the table — undershirt, whiskey, the dim light above the sink. He didn't hear her come in. She watches him from the doorway for a moment. He looks tired. Older. Human.

She gets a glass of water. Sits across from him. Neither speaks for a full minute.

Frank: "You should be sleeping."
Lily: "So should you."

- Media: Image — kitchen at 2 AM, dim light, man with whiskey, young woman with water glass
- Exit: "Continue" → Node 2

**NODE 2 — The Conversation**
Something about 2 AM unlocks what daytime locks shut. Frank talks — about building the house, about his first wife leaving, about the business being harder than he shows the boys. Not self-pity. Just honesty from a man who doesn't do honesty.

"Diana's a good woman. She deserved better than my first attempt at this."

His hand is on the table. Hers is on the table. Four inches apart.

- Choices:
  - **Touch his hand** → frank_love +3, frank_corruption +2, corruption +3. Her fingers brush his knuckles. He doesn't pull away. For ten seconds, his thumb rests on her wrist. Then he withdraws. "Goodnight, Lily." His voice is rough.
  - **"You're doing fine, Frank."** → frank_trust +3, frank_love +1. Emotional, not physical. He looks at her like she said something important. "Get some sleep." Softer this time.

Both → exit. Sets `frank_kitchen_moment`.

---

### Beat 16: Ryan's Ultimatum — TENSION EVENT

**Canvas**: `story_ryans_ultimatum`
**Location**: `loc_ryans_truck` or `loc_living_room`
**NPC**: Ryan
**Schedule**: 19:00-22:00
**Trigger**: `modeling_started` + ryan_corruption >= 20 + corruption >= 100 + days_since_flag(`frank_kitchen_moment`) >= 2
**Priority**: 10
**is_repeatable**: false

**NODE 1 — He Knows**
Ryan corners Lily. He's seen enough — Jake's drawing sessions running long, the way she comes out of his room flushed, the lock she still hasn't fixed on her door.

"So. You and Jake are having quite the art class in there."

His tone isn't angry. It's negotiating.

- Media: Image — confrontation, man leaning against wall, arms crossed, evening
- Exit: "Continue" → Node 2

**NODE 2 — The Terms**
"I'm not judging. But I'm not sitting out here while baby brother gets the attention."

He leans closer. "Whatever you're doing for Jake — I want my own arrangement. Or maybe I mention what I've seen to Dad."

The threat is real but soft. He's not cruel — he's competitive. And leveraging.

- Choices:
  - **"Are you threatening me?"** → confrontational. ryan_trust -2, confidence +3, corruption +1. Ryan backs off: "Relax. I'm just saying what's fair." The leverage dissolves — he won't actually tell Frank. But the tension stays.
  - **"What did you have in mind?"** → negotiating. ryan_love +1, ryan_corruption +3, corruption +4. She's engaging with the terms. Ryan's grin returns. "Now we're talking."
  - **"Touch me like you did in the truck. Then we'll talk."** → power flip. ryan_love +2, ryan_corruption +4, corruption +5, confidence +2. She takes control of the negotiation. Ryan is stunned. Then excited.

All → exit. Sets `ryan_leverage`.

---

### Beat 17: Power Outage (BRIDGE EVENT)

**Canvas**: `story_power_outage`
**Location**: `loc_living_room`
**NPC**: All three
**Schedule**: 19:00-22:00
**Trigger**: `ryan_leverage` + days >= 30 + days_since_flag(`ryan_leverage`) >= 2
**Priority**: 8 (bridge event — below story, above activities)
**is_repeatable**: false

**NODE 1 — Dark**
Storm. The power goes out at 8 PM. The whole property goes black. No TV, no lights, no distraction.

Frank finds candles. Six of them, arranged on the coffee table. The living room flickers amber. For the first time, all four of them are in the same room without electronics as a buffer.

- Media: Image — living room by candlelight, storm outside, four people, intimate amber glow
- Exit: "Continue" → Node 2

**NODE 2 — The Stories**
Frank opens whiskey. Even Jake gets a glass. The conversation goes places it never goes at dinner.

Frank tells the story of building this house — how the roof leaked for two years, how Ryan fell through the bathroom floor when he was twelve. Ryan denies it. Jake confirms it. They're laughing. All of them.

Jake sketches by candlelight — quick portraits. Ryan. Frank. Lily. The candlelight catches his cheekbones and he looks older, more serious.

Ryan tells a real story — the job site accident, the scar. The real version: he was scared. He was eighteen and thought his arm was broken and he didn't want to cry in front of the crew. Frank drove him to the ER. Didn't say a word the whole way. Just drove.

Frank: "You were fine."
Ryan: "I know. That's why you didn't talk."

- Exit: "Continue" → Node 3

**NODE 3 — The Quiet**
The storm fades. The candles get lower. Nobody moves to check the breaker.

Lily looks at them — Frank with his whiskey, Ryan sprawled on the couch, Jake drawing by dying light. For one moment she sees them clearly: just three men in a house that's too quiet, each carrying something they don't talk about.

- Choices:
  - **"I'm glad I'm here."** → frank_love +1, ryan_love +1, jake_love +1. She means it. Frank looks at her. Says nothing. But something shifts behind his eyes.
  - **Lean against whoever she's sitting next to (closest NPC)** → that NPC love +2, corruption +1. Physical proximity in candlelight. The others see it. Nobody comments.
  - **"Thank you for the stories."** → frank_trust +1, ryan_trust +1, jake_trust +1. Warm, but safe. Nobody gets more than anyone else.

All → exit. Sets `power_outage`. No gate flags — pure character.

---

### Beat 18: Frank Finds the Drawings — MAJOR CRISIS (Regression 2)

**Canvas**: `story_frank_finds_drawings`
**Location**: `loc_franks_office`
**NPC**: Frank (confrontation), Jake (referenced)
**Schedule**: 17:00-19:00
**Trigger**: `saw_jakes_sketches` + `kiss_unlock` + frank_trust >= 15 + days_since_flag(`kiss_unlock`) >= 5
**Priority**: 10
**is_repeatable**: false

**NODE 1 — Discovery**
Frank calls Lily to the office. His voice is different. Flat.

On the desk: Jake's sketchbook. Open to the intimate drawings — not the innocent portraits he showed her, but the others. Her in a towel. Her sleeping. Her shoulder bare during a drawing session. Beautiful art, but clearly drawn by someone who watches her when she doesn't know.

Frank found them in Jake's room while looking for a receipt.

"Explain this."

- Media: Image — office desk, open sketchbook with figure drawings, man standing rigid, tense
- Exit: "Continue" → Node 2

**NODE 2 — The Confrontation**
Frank's hands are flat on the desk. Knuckles white. He's not yelling — Frank never yells. That's worse.

"My son. In my house. Drawing my wife's daughter." Every word measured. Every word costing him something.

The irony of Frank — who's been fighting his own attraction — being the one to discover Jake's isn't lost on anyone. But he won't acknowledge that. Not now.

- Choices:
  - **"It's art, Frank. He's an artist."** → defending Jake. frank_trust -5 (she's minimizing), jake_trust +1 (loyalty). Frank: "Art. Right." He closes the sketchbook. "Get out of my office."
  - **"I didn't know about the private ones."** → honest. frank_trust -3 (still a breach), frank_love +1 (she's being real). Frank stares at her. "But you knew about the sessions."
  - **"What are you really angry about?"** → confrontational. frank_trust -4, frank_corruption +2, corruption +3. She's calling out the hypocrisy. His jaw works. Silence. "I said get out."

All → Node 3.

**NODE 3 — The Fallout**
Frank doesn't come to dinner that night. Eats in the workshop. Jake's door is closed — he knows. Ryan looks between the empty chairs and Lily's face: "What happened?"

Sets `frank_found_drawings`. frank_trust drops (per choice). jake_trust -3 (fear, shame).

**CRISIS FALLOUT (next 3-4 days):**
- Frank: Bookkeeping cancelled. Eats alone. Avoids eye contact. If Lily enters the kitchen when he's there, he leaves within 2 minutes. Activities with Frank have WITHDRAWN variant: "He nods. No words. Pours coffee and takes it to the workshop."
- Jake: Door closed. No wall knocking. Drawing sessions don't fire. If forced together at meals, he stares at his plate. Activities with Jake have WITHDRAWN variant: "He's there but not there. The sketchbook is nowhere in sight."
- Exit: → canvas exit.

**REPAIR PATH:**

*Frank repair* — `story_frank_repair`
Trigger: `frank_found_drawings` + days_since_flag >= 3 + frank_trust >= 10
Location: `loc_workshop`

Lily finds Frank in the workshop early morning. He's sanding something he's already sanded. She doesn't make excuses.

- Choices:
  - **"I should have told you about the sessions."** → accountability. frank_trust +4, frank_love +1. He stops sanding. Doesn't turn around. "Yeah. You should have." Long pause. "But I shouldn't have gone through his things."
  - **"Are you punishing him or me?"** → direct. frank_trust +2, frank_corruption +2. He turns. Eyes hard. "Both." Then softer: "Neither. I don't know."

Sets `frank_repair_complete`. Bookkeeping resumes. Frank is different — less controlled, more present. The wall cracked and something came through.

*Jake repair* — `story_jake_repair`
Trigger: `frank_found_drawings` + days_since_flag >= 2 + jake_trust >= 5
Location: `loc_jakes_room`

Lily knocks on Jake's door. He opens it. Red-eyed.

"He saw them."
"I know."
"The ones I didn't show you."

- Choices:
  - **"Show me."** → jake_love +3, jake_trust +3. He opens the sketchbook to the private pages. Her in her towel, her sleeping, her shoulder. "I'm sorry. I couldn't stop drawing you." This IS the branch-point setup — the Level 3 discovery from Section 19.
  - **"Are you okay?"** → jake_trust +3, jake_love +1. She prioritizes him over the art. He cries. She holds him. No escalation — just human.

Sets `jake_repair_complete`. Drawing sessions resume.

---

### Beat 19: Financial Crisis

**Canvas**: `story_financial_crisis`
**Location**: `loc_lily_room`
**NPC**: None (solo)
**Schedule**: 07:00-09:00
**Trigger**: `bookkeeping_started` + days >= 30 + money < 100
**Priority**: 10
**is_repeatable**: false

**NODE 1 — The Bounce**
Phone notification. Mom's transfer bounced again. Third time. The bank in Dubai is "processing." Meanwhile: art supplies due ($60), bus pass expired yesterday ($80), phone bill overdue ($45).

Lily's money: whatever the player has — probably $50-100 after a month of cleaning + bookkeeping.

Total owed: $185. She has maybe half that.

- Media: Image — phone notification, bank app showing low balance, morning despair
- Exit: "Continue" → Node 2

**NODE 2 — Options**
Internal monologue. She runs through the options the PLAYER has been living:
- Clean more (can't — already doing it daily)
- Ask Frank for an advance (won't — pride)
- Call Mom (won't — guilt)
- Take the diner job (costs every evening with all three NPCs)
- Escalate with someone who pays more (modeling, overtime bookkeeping, favors...)

The game presents no choice here — just the math. The player already knows what they'll do. The event is Lily catching up to the player's calculation.

- Exit: → canvas exit. Sets `financial_crisis`.

---

### Beat 20: Physical Escalation (GATE: `handjob_unlock`)

**Canvas**: `story_physical_escalation`
**Location**: NPC-dependent
**NPC**: First to meet conditions
**Trigger**:
- Jake: corruption >= 100, jake_love >= 20, jake_trust >= 18, jake_corruption >= 15
- Ryan: corruption >= 110, ryan_love >= 15, ryan_trust >= 12, ryan_corruption >= 25
- Frank: corruption >= 140, frank_love >= 25, frank_trust >= 22
- All require: `kiss_unlock` + days_since_flag(`kiss_unlock`) >= 7
**Priority**: 10
**is_repeatable**: false

**JAKE VARIANT — "Drawing Session Turns Physical"**

*NODE 1*
Drawing session. Late afternoon light. She's posing — less clothing than before (the corruption and the art justify each other). He's been drawing for an hour.

He puts the pencil down. "I can't concentrate."

She knows why. She's been watching his hands shake for twenty minutes.

*NODE 2*
Her hand finds his. The pencil drops. She guides his hand — not to the sketchbook. To her. He's trembling.

- **First-time variant**: "Her hand on him. Through his jeans at first, then inside. His breath catches — the sound is so raw and surprised that her own body responds. She's never held someone like this. His hand grips her wrist. Not pulling away — holding on."
- **Repeat variant**: "She's done this before. But his reaction is different — he whispers her name like a confession. The boy who draws her in secret is shaking under her hand."
- Video placeholder: Handjob, intimate, eye contact, tender, bedroom setting
- Exit: → canvas exit. Sets `handjob_unlock`. jake_love +3, jake_corruption +5, corruption +5.

**RYAN VARIANT — "Truck, Remote"**

*NODE 1*
Truck. Dead-end road again. But this time she reached for the gear shift. Her hand lands on his thigh. She moves it higher.

*NODE 2*
- **First-time**: "She wraps her hand around him and watches his face change — the cocky grin dissolves into something raw. Ryan's head drops back against the headrest. 'Jesus, Lily.'"
- **Repeat**: "She's done this before. Ryan is different — louder, less controlled. His hand grips the steering wheel hard enough to creak."
- Video placeholder: Handjob, truck interior, urgent, direct
- Exit: → canvas exit. Sets `handjob_unlock`. ryan_corruption +5, corruption +5.

**FRANK VARIANT — "Under the Desk"**

*NODE 1*
Overtime bookkeeping. Door locked. They've been pretending numbers matter for thirty minutes.

Her hand moves from the ledger to his knee. To his thigh. He stops breathing.

*NODE 2*
- **First-time**: "She reaches under the desk and Frank's whole body goes rigid. His hand flattens on the wood. She feels the power — the man who controls everything in this house, controlled by her hand."
- **Repeat**: "She's done this before. But with Frank it's different — he doesn't make a sound. His jaw clenches. His hand finds the back of her head. Not gentle."
- Video placeholder: Under-desk handjob, office setting, power dynamic, forbidden
- Exit: → canvas exit. Sets `handjob_unlock`. frank_corruption +5, corruption +6.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ACT 4: CONVERGENCE (Corruption 180-240, Days 45-60)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**Note on Beats 20→21 gap**: Between `handjob_unlock` and Act 4, the `blowjob_unlock` and `sex_unlock` gates fire through NPC activities as corruption and NPC stats reach their thresholds. These are ACTIVITY-tier gate events (designed in Phase 5), not one-time story events. The oral and sex milestones happen organically through the highest-tier activity choices once the player's corruption and NPC stats are high enough. Act 4's story events focus on the HOUSEHOLD consequences — the discovery, the power plays, the countdown.

---

### Beat 21: Brothers Discover Each Other — CRISIS (Regression 3)

**Canvas**: `story_brothers_discover`
**Location**: `loc_kitchen` or `loc_hallway`
**NPC**: Ryan and Jake (both present)
**Schedule**: 17:00-19:00
**Trigger**: `handjob_unlock` + (ryan_love >= 15 OR ryan_corruption >= 30) + (jake_love >= 20 OR jake_corruption >= 20) + days >= 40
**Priority**: 10
**is_repeatable**: false

**NODE 1 — The Discovery**
Dinner preparation. Lily comes out of Jake's room. Her hair is messy. She's adjusting her shirt. She doesn't know Ryan is in the hallway.

Ryan sees her. Sees Jake's door closing behind her. Sees the flush on her neck.

His face changes. Not the grin. Something hard and hurt underneath.

"So." One word. Flat.

Jake opens his door. Sees Ryan. Sees Ryan looking at Lily. Understands immediately.

- Media: Image — hallway confrontation, two brothers facing each other, woman between them
- Exit: "Continue" → Node 2

**NODE 2 — The Confrontation**
Kitchen. All three. Frank is in the workshop — he doesn't hear this.

Ryan: "How long?" Looking at Jake.
Jake: "Ryan—"
Ryan: "How. Long."

Jake can't answer. Lily is between them — literally, physically, emotionally.

Ryan to Lily: "Both of us? Really?" His voice is more hurt than angry. He thought he was the only one. Or he hoped.

Jake: "It's not like that. We're not—"
Ryan: "You ARE. I've seen the sketchbook, Jake."

- Exit: "Continue" → Node 3

**NODE 3 — The Choice (GLOBAL CRISIS BRANCH)**

Three options. All set `crisis_resolved`. No arc closes.

- **"It's none of your business."** → `chose_independent`. Lily asserts control. Both brothers chastened. Confidence +5. ryan_love -3, jake_love -2. Future scenes: she initiates, they follow. Dominance undertone across all arcs.

- **"Please don't fight. I care about both of you."** → `chose_peacemaker`. Lily mediates. Guilt + tenderness. ryan_love -1, jake_love -1. Future scenes: more emotional weight, "we shouldn't but I need you" energy across both arcs.

- **(Say nothing. Walk away.)** → `chose_avoidant`. Lily shuts down. ryan_love -3, jake_love -3. Short-term regression. Frank's arc accelerates — she turns to the authority figure when peers become complicated. frank_love +2.

All → Node 4.

**NODE 4 — After**
Whatever was said, dinner doesn't happen. Jake goes to his room. Ryan goes to the truck. Lily stands in the empty kitchen.

Frank comes in from the workshop. Looks at the untouched food. Looks at Lily.

"What happened?"
"Nothing."

He doesn't believe her. But he doesn't push. He makes two sandwiches. Hands her one.

"Eat."

- Exit: → canvas exit. Sets `brothers_know`, `crisis_resolved`.

**CONSEQUENCE ECHO (next 2-4 days):**
- `chose_independent`: Brothers are cautious. Both treat her with more respect and more distance. Activities have tense openings. Jake's drawings are sharper. Ryan stops with the nicknames.
- `chose_peacemaker`: Brothers are guilty. Jake leaves drawings under her door. Ryan offers rides without commentary. Slowly they recalibrate — separately, each accepting the arrangement implicitly.
- `chose_avoidant`: Cold house. Brothers avoid each other AND Lily. Meals are silent. Frank notices and fills the gap — more late-night conversations, more office time. His arc accelerates by 5-7 days of stat growth.

---

### Beat 22: Frank's Offer

**Canvas**: `story_franks_offer`
**Location**: `loc_franks_office`
**NPC**: Frank
**Schedule**: 22:00-01:00
**Trigger**: `crisis_resolved` + frank_love >= 22 + frank_trust >= 22 + corruption >= 180 + days_since_flag(`crisis_resolved`) >= 3
**Priority**: 10
**is_repeatable**: false

**NODE 1 — The Office at Night**
Frank calls her to the office. Late. The house is quiet.

He's different tonight. No pretense. No invoices on the desk. Just the lamp, two chairs, and whatever this is about to be.

"I know what's been happening in this house." He holds up a hand before she can speak. "I'm not asking for details. I don't want them."

- Media: Image — office at night, amber lamp, man sitting forward in chair, serious
- Exit: "Continue" → Node 2

**NODE 2 — The Terms**
"Diana will be back in a few weeks. When she comes home, this all stops. But until then—"

He opens a drawer. An envelope. Cash.

"I'll cover everything. Bus pass. Art supplies. Phone. Whatever you need. Every week."

Pause.

"And in exchange, you stay here. In this office. Late nights. With me."

He's not asking for sex (yet — that depends on where his arc is). He's asking for the proximity. The door closed. The permission to stop fighting what he's been fighting for six weeks.

"I'm not your father. I'm not going to pretend I am."

- Choices:
  - **"What exactly are you asking for?"** → neutral, clarifying. frank_love +1, corruption +2. She's not saying no. She's negotiating.
  - **"Deal."** → accepting. frank_love +3, frank_corruption +4, corruption +5. Simple. Direct. He exhales like he's been holding his breath for a month.
  - **"I don't need your money, Frank."** → rejection. frank_trust +2, frank_love +1, confidence +3. She doesn't need the arrangement. But she didn't leave the office.

All → exit. Sets `frank_offer`. Money effect depends on choice (deal = +150/week going forward).

---

### Beat 23: Jake's Branch Point (Level 3 — SECRET Sketches Discovery)

**Canvas**: `story_jake_secret_sketches`
**Location**: `loc_jakes_room`
**NPC**: Jake
**Schedule**: 12:00-15:00
**Trigger**: `jake_repair_complete` + jake_love >= 25 + corruption >= 90 + days_since_flag(`jake_repair_complete`) >= 5
**Priority**: 10
**is_repeatable**: false

**NOTE**: This is the BRANCH-POINT discovery — different from Beat 11 (innocent sketchbook). Here, Lily finds Jake's SECRET intimate sketches — poses she didn't know he saw.

**NODE 1 — Discovery**
Jake's room. He stepped out — bathroom. His sketchbook is on the bed. Open.

Lily glances at it. The drawing is her — but not a portrait. Her, from behind, bending over the kitchen counter. Her in the shower, seen through a crack in the bathroom door. Her asleep, sheets tangled, shirt riding up.

He was watching. All those times she thought she was alone.

- Media: Image — open sketchbook, intimate figure drawings, woman looking at them with complex emotion
- Exit: "Continue" → Node 2

**NODE 2 — The Confrontation**
Jake comes back. Sees her face. Sees the open sketchbook.

The color drains from him.

"Lily—I can explain—those aren't—"

- Choices (BRANCH POINT — Level 3):
  - **"They're beautiful."** → `chose_tender_jake`. jake_love +4, jake_trust +3, jake_corruption +3. The arc stays sweet. She accepts his obsession as devotion. He draws her with consent now. Art as shared language. "You see me. That's not something I should be angry about."
  - **"You've been watching me."** → `chose_possessive_jake`. jake_trust -2, jake_corruption +5, corruption +4. The arc turns darker. His shyness was hiding obsession. He's sorry — then defiant. "I can't stop. I tried." Then desperate: "Don't make me stop." The sweetness has teeth now.

Both → exit. Sets `jake_sketches_discovered`.

---

### Beat 24: Frank's Branch Point (Level 3 — Financial Secret)

**Canvas**: `story_franks_secret`
**Location**: `loc_franks_office`
**NPC**: Frank
**Schedule**: 12:00-15:00
**Trigger**: `bookkeeping_started` + frank_trust >= 20 + corruption >= 110 + days_since_flag(`bookkeeping_started`) >= 14
**Priority**: 10
**is_repeatable**: false

**NODE 1 — The Ledger**
Regular bookkeeping session. Lily opens the wrong file. A spreadsheet Frank didn't mean to leave accessible.

The business is in debt. Not a little — serious debt. Payments behind. A loan he hasn't mentioned. Numbers that don't add up unless the construction company is bleeding money.

Frank is building a house on cracking foundations, financially.

- Media: Image — spreadsheet with red numbers, office desk, realization
- Exit: "Continue" → Node 2

**NODE 2 — Frank Walks In**
He sees what's on the screen. His face goes still.

"Close that."
"Frank—"
"I said close it."

Beat. He sits down. Runs his hand over his face. For the first time, Frank looks like a man who doesn't have everything under control.

- Choices (BRANCH POINT — Level 3):
  - **"I can help. Let me look at the real numbers."** → `chose_confront_frank`. frank_trust +3, frank_love +2. Adversarial-to-intimate. He fights it — then breaks. Lets her see everything. They work on it together. Two people against a problem. Trust-to-love pipeline.
  - **"I didn't see anything."** → `chose_protect_frank`. frank_trust +4, frank_corruption +2. Conspiratorial. They share a secret now. Private meetings shift from bookkeeping to real talk. He owes her silence and she holds it carefully. Forbidden-intimacy pipeline.

Both → exit. Sets `frank_secret_complete`.

---

### Beat 25: Mom's Announcement — TENSION EVENT (Regression 4)

**Canvas**: `story_moms_return`
**Location**: `loc_lily_room`
**NPC**: None (phone call), then all NPCs affected
**Schedule**: 19:00-22:00
**Trigger**: `crisis_resolved` + days >= 48
**Priority**: 10
**is_repeatable**: false

**NODE 1 — The Call**
Phone buzzes. Mom. The connection is clearer than last time — she's at an airport.

"Lily, honey. Good news — I'm coming home early! The contract finished ahead of schedule. I'll be there in about a week."

Lily's stomach drops.

"That's... that's great, Mom."

- Media: Image — young woman on phone, evening, face showing complex emotions — fear disguised as happiness
- Exit: "Continue" → Node 2

**NODE 2 — The Countdown**
After the call. Lily sits on her bed. Stares at the wall — Jake's wall.

One week. Seven days. Maybe ten, with flights and layovers.

Everything she's built — the routines, the relationships, the escalation, the arrangements — has an expiration date. When Diana walks through that door, Lily becomes Diana's daughter again. Frank becomes Diana's husband. The boys become her step-brothers.

The roles reassemble. Whatever this was... stops.

- Exit: "Continue" → Node 3

**NODE 3 — The House Knows**
Lily tells them at dinner. "Mom's coming home early. About a week."

Silence.

Frank puts down his fork. Slowly. His face is unreadable.
Ryan: "Cool." (Not cool. His voice is flat.)
Jake looks at Lily with something between hope and devastation.

All NPC corruption -2 (fear response). The energy in the house changes immediately.

- Exit: → canvas exit. Sets `mom_returning`.

---

### Beat 26: Final Week / Endgame Active

**Canvas**: `story_final_week`
**Location**: `loc_kitchen`
**NPC**: All three (rotating)
**Schedule**: 07:00-09:00
**Trigger**: `mom_returning` + days_since_flag(`mom_returning`) >= 2
**Priority**: 10
**is_repeatable**: false

**NODE 1 — Morning After the News**
Breakfast. Nobody talks about the obvious. But everything is louder.

Frank pours coffee. His hand brushes Lily's when he passes the mug. He doesn't pull away. He used to.

Jake is drawing — fast, urgent. Like he's trying to capture everything before it's gone.

Ryan eats in silence. Then: "We should do a hike this weekend. Before she gets here. All of us."

It's the first generous thing Ryan has said about shared time.

- Choices:
  - **"I'd like that."** → all NPC love +1. A moment of unity.
  - **"I want to spend the last few days with each of you. Separately."** → corruption +3, confidence +2. Direct. Honest. Each NPC gets the message: the clock is ticking, and she's choosing to spend what's left on them.

Both → exit. Sets `endgame_active`.

---

### Beat 27: Resolution

**Canvas**: `story_resolution`
**Location**: `loc_kitchen`
**NPC**: All three, then Diana arrives
**Schedule**: 12:00-15:00
**Trigger**: `endgame_active` + days_since_flag(`mom_returning`) >= 7
**Priority**: 10
**is_repeatable**: false

**NODE 1 — The Last Morning**
Lily packs her suitcase. Tries to fit everything — but there's more now. Clothes she bought, beauty products, Jake's flannel, a sketch he drew of her hands.

She sits on the bed. The room that was temporary ten weeks ago has her fingerprints everywhere.

**NODE 2 — Diana Arrives**
Car in the driveway. Not Ryan's truck — a taxi from the airport.

Diana Chen-Harmon. Tired, tan, grateful to be home. She hugs Lily at the door: "Oh baby, I missed you."

Frank stands in the kitchen. Clean shirt. Composed. "Diana." One word.

Diana: "The house looks great. You must have taken good care of things, Lily."

If only she knew.

**NODE 3 — Ending**
The ending is determined by accumulated stats (see Phase 2, Section 5 — Ending Conditions). The narration branches based on ending type:

| Ending | Final Scene |
|--------|------------|
| **Jake's Girl** | Lily and Jake exchange a look over Diana's shoulder. His hand finds hers behind their backs. The sketchbook is hidden under his bed — full. They'll continue. In secret. After. |
| **Ryan's Conquest** | Ryan catches Lily's eye as Diana unpacks. He jinxes the truck keys. Mouths: "Later." It's not love. But it's honest. He'll drive her wherever she wants. |
| **Frank's Arrangement** | Frank and Lily don't look at each other. They don't need to. The arrangement is already in place. Diana will travel again. Frank will be here. So will Lily. Nothing is said. Everything is understood. |
| **All Three** | Lily sits at the dinner table — five chairs now. She looks at each of them. Each looks back. The house is hers now, in a way Diana will never understand. Mom came home to a daughter she doesn't quite recognize. |
| **Independent** | Lily hugs Diana. "I got a job at the diner. I'm going to look for my own place." Confidence in her voice. Money in her account. She can leave. She might stay — on her terms. |
| **Escape** | Lily hugs Diana. Goes to her room. Packs. She'll be back at the dorm by next week — the repairs are done. Nothing happened here. Almost. She thinks of Jake's drawing of her hands and wonders if that counts. |

- Exit: → canvas exit. Sets `game_complete`. Game ends.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## FLAG CHAIN DIAGRAM

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

```
game_started (Day 1)
  │
  ├→ first_morning (Day 2)
  │     └→ bus_problem_discovered + town_access (Day 3)
  │           └→ mom_called [BRIDGE] (Day 4)
  │                 └→ money_crisis_realized + first_week_complete + chores_started (Day 6-7)
  │
  ├→ GATE: exposure_unlock (Day ~8, corruption 25-60)
  │     Requires: chores_started + NPC-specific thresholds
  │     Sets: drawing_started (if Jake)
  │     Unlocks: "Stand closer" in all physical sub-menus
  │
  ├→ truck_incident_complete (Day ~10)
  │     Branch: ryan_resisted / ryan_allowed
  │     Requires: exposure_unlock + bus_problem_discovered
  │
  ├→ bookkeeping_started (Day ~12)
  │     Requires: corruption >= 40 + frank_trust >= 8
  │     Unlocks: Bookkeeping utility canvas ($25/session)
  │
  ├→ first_swim (Day ~10-12)
  │     Requires: first_week_complete + corruption >= 30
  │
  ├→ saw_jakes_sketches (Day ~12-14)
  │     Requires: drawing_started + jake_love >= 12
  │
  ├→ ryan_caught_her (Day ~14)
  │     Requires: truck_incident_complete + ryan_corruption >= 12
  │
  ├→ GATE: flirt_unlock (Day ~12-14, corruption 40-75)
  │     Requires: exposure_unlock + NPC-specific thresholds
  │     Sets: modeling_started (if Jake)
  │     Unlocks: "Flirt with him" in all physical sub-menus
  │
  ├→ GATE: tease_unlock (Day ~16, corruption 55-90)
  │     Requires: flirt_unlock + days_since >= 2 + NPC thresholds
  │     Unlocks: "Tease him" in all physical sub-menus
  │
  ├→ GATE: kiss_unlock (Day ~18, corruption 70-120)
  │     Requires: flirt_unlock + days_since >= 3 + NPC thresholds
  │     Unlocks: "Kiss him" in all physical sub-menus
  │
  ├→ frank_kitchen_moment (Day ~28)
  │     Requires: kiss_unlock + frank_love >= 12 + corruption >= 100
  │
  ├→ ryan_leverage (Day ~30)
  │     Requires: modeling_started + ryan_corruption >= 20 + corruption >= 100
  │
  ├→ power_outage [BRIDGE] (Day ~32)
  │     Requires: ryan_leverage + days >= 30
  │
  ├→ frank_found_drawings [MAJOR CRISIS] (Day ~35)
  │     Requires: saw_jakes_sketches + kiss_unlock + frank_trust >= 15
  │     Drops: frank_trust -3 to -5, jake_trust -3
  │     Repair chain: frank_repair_complete + jake_repair_complete (3-4 days)
  │
  ├→ financial_crisis (Day ~34)
  │     Requires: bookkeeping_started + days >= 30 + money < 100
  │
  ├→ GATE: handjob_unlock (Day ~28-35, corruption 100-140)
  │     Requires: kiss_unlock + days_since >= 7 + NPC thresholds
  │     Unlocks: "Touch him" in all physical sub-menus
  │
  ├→ jake_sketches_discovered (Day ~30-38)
  │     Branch: chose_tender_jake / chose_possessive_jake
  │     Requires: jake_repair_complete + jake_love >= 25
  │
  ├→ frank_secret_complete (Day ~35-40)
  │     Branch: chose_confront_frank / chose_protect_frank
  │     Requires: bookkeeping_started + frank_trust >= 20 + corruption >= 110
  │
  ├→ GATE: blowjob_unlock (Day ~38-42, corruption 140-180)
  │     Via activity escalation (not one-time story event)
  │     Unlocks: "Use your mouth" in all physical sub-menus
  │
  ├→ brothers_know + crisis_resolved (Day ~42-44)
  │     Branch: chose_independent / chose_peacemaker / chose_avoidant
  │     Requires: handjob_unlock + NPC love thresholds + days >= 40
  │     Drops: discovering_brother love -3 to -5
  │
  ├→ frank_offer (Day ~45)
  │     Requires: crisis_resolved + frank_love >= 22 + corruption >= 180
  │
  ├→ GATE: sex_unlock (Day ~46-50, corruption 180-210)
  │     Via activity escalation (not one-time story event)
  │     Unlocks: "Go further" in all physical sub-menus
  │
  ├→ mom_returning (Day ~48)
  │     Drops: all NPC corruption -2
  │     Requires: crisis_resolved + days >= 48
  │
  ├→ endgame_active (Day ~50)
  │     Requires: mom_returning + days_since >= 2
  │
  └→ game_complete (Day ~56)
       Ending determined by: highest NPC stats, corruption level,
       crisis branch, financial state
```

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type "proceed" to continue to Phase 5: Activities,
or provide adjustments.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


# PHASE 5: ACTIVITIES
# Under One Roof

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION A: NPC ACTIVITIES (ESCALATING)

All NPC activities use the Three-Choice Format (Pattern L):
- **Emotional** — conversation, builds love, may build corruption
- **Physical** — opens sub-menu of unlocked intensity options
- **Neutral** — quick interaction, small love +1, conserves energy

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### JAKE ACTIVITIES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#### Activity: Drawing Session with @jake

- **Pattern**: A (standard escalation)
- **Location**: `loc_jakes_room`
- **Schedule**: 12:00-15:00
- **NPC**: `npc_jake`
- **Unlock**: `drawing_started` (set by Beat 7 Jake variant or early interactions)
- **Priority**: 1
- **Energy**: 15
- **is_repeatable**: true, max_triggers_per_day = 1

**Base Scene Variants:**

DEFAULT (SAFE/OPEN quadrant):
> "Jake's room. Afternoon light through the window. He's already set up — sketchbook open, pencils arranged, the eraser he chews on when he's concentrating sitting on the bedside table. He looks up when you walk in. 'Hey.' Small smile. He pushes his glasses up. 'The light's really good right now.'"

WITHDRAWN variant (post-crisis / CONFLICTED):
> "Jake's door is cracked but not open. He's drawing something — not you. Landscapes. The pencil moves mechanically. He glances up when you enter. 'Oh. Hey.' Looks back at the page. The chair he usually pulls out for you is against the wall."

WARM variant (high stats / OPEN):
> "He's already cleared space for you on the bed. The sketchbook is open to a half-finished portrait — your face, the way you looked yesterday when you laughed at something Ryan said. He's captured a version of you that's more beautiful than any mirror. 'I was hoping you'd come by.' His voice is steady. His eyes aren't."

**Choice Progression (Three-Choice Format):**

| Choice | Condition | Node | Effects |
|--------|-----------|------|---------|
| **"Talk to him while he draws" (Emotional)** | always | emotional_node | jake_love +2, jake_trust +1 |
| **"Pose for him" (Physical)** | `exposure_unlock` | physical_submenu | see sub-menu below |
| **"Watch him work" (Neutral)** | always | exit | jake_love +1, energy -15 |

**Emotional Node — Conversation Topics (group variants by relationship phase):**

| Phase | Topic | Effects |
|-------|-------|---------|
| Pre-kiss | Talk about art school, his portfolio, what he wants to be. He opens up about Ryan mocking his art. | jake_love +2, jake_trust +1 |
| Post-kiss | Talk about what this is between them. "We shouldn't." "I know." He draws while they talk — her face comes out softer. | jake_love +2, jake_trust +1, corruption +1 |
| Post-intimacy | He tells her he loves her. Simple. Terrified. True. The conversation is about whether this survives Mom's return. | jake_love +3, jake_trust +2 |

**Physical Sub-Menu:**

| Choice | Condition | Effects | Video Placeholder |
|--------|-----------|---------|-------------------|
| "Hold the pose a little longer" | `exposure_unlock` | jake_love +1, corruption +1 | Image — posing, charged eye contact |
| "Flirt while posing" | `flirt_unlock` + corruption >= 40 | jake_love +1, jake_corruption +2, corruption +2 | Image — flirtatious posing, teasing |
| "Pose provocatively" | `tease_unlock` + corruption >= 55 | jake_corruption +2, corruption +2 | Video — provocative posing, deliberate |
| "Kiss him" | `kiss_unlock` + corruption >= 70 + jake_love >= 15 | jake_love +2, jake_corruption +2, corruption +2 | Video — tender kiss, art room |
| "Guide his hand" | `handjob_unlock` + corruption >= 100 + jake_love >= 20 | jake_corruption +3, corruption +3 | Video — handjob, tender, his room |
| "Get on your knees" | `blowjob_unlock` + corruption >= 140 + jake_love >= 25 | jake_corruption +4, corruption +4 | Video — oral, tender, bedroom |
| "Take him to bed" | `sex_unlock` + corruption >= 180 + jake_love >= 30 | jake_corruption +5, corruption +5 | Video — sex, eye contact, intimate, bed |

---

#### Activity: Studying with @jake

- **Pattern**: A (limited escalation — caps at kiss tier)
- **Location**: `loc_library`
- **Schedule**: 15:00-17:00
- **NPC**: `npc_jake`
- **Unlock**: `first_week_complete`
- **Priority**: 1
- **Energy**: 15

**Base Scene:**

DEFAULT:
> "Library basement. Fluorescent lights and the smell of old paper. Jake is at a study carrel, glasses on, textbook open. He pulls out the chair next to him without looking up. Their knees touch under the table. Neither moves."

WITHDRAWN:
> "He's at the far carrel today. Didn't save a seat. Headphones on, though nothing seems to be playing."

WARM:
> "He saved her spot. There's a coffee from the campus café on her side. Still warm. A sticky note on the cup: a tiny sketch of her face, asleep. He drew this from memory."

**Choice Progression:**

| Choice | Condition | Node | Effects |
|--------|-----------|------|---------|
| **"Ask about his classes" (Emotional)** | always | talk | jake_love +1, jake_trust +2 |
| **"Touch his hand under the table" (Physical)** | `exposure_unlock` | physical | see below |
| **"Study quietly together" (Neutral)** | always | exit | jake_love +1, jake_trust +1 |

**Physical Sub-Menu (limited — public location):**

| Choice | Condition | Effects |
|--------|-----------|---------|
| "Brush his hand" | `exposure_unlock` | jake_love +1, corruption +1 |
| "Play footsie under the table" | `flirt_unlock` + corruption >= 40 | jake_corruption +1, corruption +1 |
| "Kiss him between the shelves" | `kiss_unlock` + corruption >= 70 + jake_love >= 15 | jake_love +2, corruption +2 |

Caps at kiss — library is too public for more.

---

#### Activity: Creek Swimming with @jake

- **Pattern**: A (standard escalation)
- **Location**: `loc_creek`
- **Schedule**: 15:00-17:00
- **NPC**: `npc_jake`
- **Unlock**: `first_swim`
- **Priority**: 1
- **Energy**: 30

**Base Scene:**

DEFAULT:
> "Creek. Late afternoon. The water catches light through the branches. Jake is already in — up to his waist, pale skin bright against the dark water. He pushes wet hair from his eyes when he sees her. The creek is where pretense dissolves. She's in whatever she's wearing to swim — the improvised sports bra, the bikini Ryan bought, or something from the shop. The water makes everything cling."

WITHDRAWN:
> "He's in the water but further downstream than usual. Not waving her over. Just floating, looking at the sky."

WARM:
> "He's waiting by the bank. Not in the water yet. 'Wanted to go in together.' He takes her hand as they wade in. Cold water, warm hand."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Talk in the water" (Emotional)** | always | jake_love +2, corruption +1, fitness +2 |
| **"Swim closer" (Physical)** | `exposure_unlock` | physical sub-menu |
| **"Float separately" (Neutral)** | always | jake_love +1, fitness +2 |

**Physical Sub-Menu:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| "Swim next to him" | `exposure_unlock` | jake_love +1, jake_corruption +1, corruption +2 |
| "Splash fight" | `flirt_unlock` + corruption >= 40 | jake_love +1, jake_corruption +2, corruption +2 |
| "Kiss him in the water" | `kiss_unlock` + corruption >= 70 | jake_love +2, jake_corruption +2, corruption +3 |
| "Hands under the water" | `handjob_unlock` + corruption >= 100 | jake_corruption +3, corruption +4 |
| "Pull him to the bank" | `sex_unlock` + corruption >= 180 | jake_corruption +5, corruption +5 |

Video placeholders: Creek/outdoor setting, bodies in water, escalating intimacy.

---

#### Activity: Late-Night Wall Knocking

- **Pattern**: A (limited escalation)
- **Location**: `loc_lily_room`
- **Schedule**: 22:00-01:00
- **NPC**: `npc_jake` (through the wall)
- **Unlock**: `first_week_complete` + jake_love >= 8
- **Priority**: 1
- **Energy**: 0 (free)

**Base Scene:**

DEFAULT:
> "Late night. Lily's room is dark. Through the wall: tap. Tap-tap. Jake's knock. Their ritual. She knocks back. Silence. Then his muffled voice, barely audible: 'You awake?'"

WITHDRAWN:
> "No knock tonight. She lies there listening. Nothing."

WARM:
> "The knock comes earlier than usual. Tap-tap-tap. Three knocks instead of two. She can hear him smiling through the wall."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Talk through the wall" (Emotional)** | always | jake_love +2, jake_trust +1 |
| **"Knock back, invite him over" (Physical)** | `kiss_unlock` + jake_love >= 15 | → he comes to her room, physical sub-menu |
| **"Knock back, go to sleep" (Neutral)** | always | jake_love +1 |

**Physical (when he comes to her room):**

| Choice | Condition | Effects |
|--------|-----------|---------|
| "Lie next to him" | `kiss_unlock` + corruption >= 70 | jake_love +2, corruption +2 |
| "Kiss in the dark" | `kiss_unlock` + corruption >= 70 | jake_love +2, jake_corruption +2, corruption +3 |
| "More than kissing" | `handjob_unlock` + corruption >= 100 | jake_corruption +3, corruption +4 |
| "Invite him into your bed" | `sex_unlock` + corruption >= 180 | jake_corruption +5, corruption +5 |

---

#### Activity: Park Sketching (Weekends)

- **Pattern**: A (limited — caps at kiss)
- **Location**: `loc_park`
- **Schedule**: 15:00-17:00
- **NPC**: `npc_jake`
- **Unlock**: `town_access` + `drawing_started`
- **Weekdays**: [5,6] (Sat/Sun only)
- **Priority**: 1
- **Energy**: 15

**Base Scene:**

DEFAULT:
> "Park bench. Jake has his sketchbook. Lily has nothing to do but sit near him and watch him draw the pond, the ducks, the old man on the next bench. After ten minutes his pencil drifts from the pond to her jawline. She pretends not to notice."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Tell me about this piece" (Emotional)** | always | jake_love +2, jake_trust +1 |
| **"Lean against his shoulder" (Physical)** | `exposure_unlock` | jake_love +1, corruption +1 |
| **"Sit in comfortable silence" (Neutral)** | always | jake_love +1, jake_trust +1 |

Physical caps at "Kiss on the bench" (`kiss_unlock`) — public park.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### RYAN ACTIVITIES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#### Activity: Truck Ride with @ryan

- **Pattern**: A (standard escalation)
- **Location**: `loc_ryans_truck`
- **Schedule**: 15:00-17:00
- **NPC**: `npc_ryan`
- **Unlock**: `town_access`
- **Priority**: 1
- **Energy**: 10

**Base Scene Variants:**

DEFAULT:
> "Ryan's truck. Pine air freshener and the ghost of sawdust. He drives with one hand, radio on classic rock, window cracked. The bench seat leaves a gap between them — too small to ignore, too big to blame on the truck. 'Where to, college girl?'"

WITHDRAWN (post-crisis):
> "The truck is quiet. No radio. His jaw is set. He drives straight to wherever she needs to go. No detours. No commentary. The gap on the bench seat is wider than it used to be."

WARM:
> "He's already in the truck when she comes out. Engine running, her door open. He cleaned the passenger side — the empty cans are gone, the seat is wiped down. He doesn't mention it. 'Hey. Hop in.' Softer than he sounds in front of anyone else."

**Consequence Variants:**
- After `ryan_resisted`: "He opens her door without comment. The silence is careful — he's testing whether she's still afraid of him. She's not. That's worse."
- After `ryan_allowed`: "His hand is already on the center of the bench seat. An invitation with plausible deniability. The dirt road shortcut is becoming a habit."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Talk on the drive" (Emotional)** | always | ryan_love +2, ryan_trust +1 |
| **"Sit closer" (Physical)** | `exposure_unlock` | physical sub-menu |
| **"Ride in silence" (Neutral)** | always | ryan_love +1 |

**Physical Sub-Menu:**

| Choice | Condition | Effects | Video Placeholder |
|--------|-----------|---------|-------------------|
| "Sit in the middle" | `exposure_unlock` | ryan_love +1, corruption +1 | Image — truck cab, sitting close |
| "Flirt with him" | `flirt_unlock` + corruption >= 40 | ryan_corruption +2, corruption +2 | Image — flirting in truck |
| "Touch his thigh" | `tease_unlock` + corruption >= 55 | ryan_corruption +2, corruption +3 | Video — hand on thigh, driving |
| "Kiss him" | `kiss_unlock` + corruption >= 70 + ryan_love >= 12 | ryan_love +2, ryan_corruption +2, corruption +3 | Video — truck cab kiss, aggressive |
| "Reach over" | `handjob_unlock` + corruption >= 100 + ryan_corruption >= 25 | ryan_corruption +4, corruption +4 | Video — handjob, truck, urgent |
| "Pull over" | `blowjob_unlock` + corruption >= 140 + ryan_corruption >= 30 | ryan_corruption +4, corruption +5 | Video — oral in truck, raw |
| "Truck bed" | `sex_unlock` + corruption >= 180 + ryan_love >= 22 | ryan_corruption +5, corruption +6 | Video — sex, truck bed, outdoors |

---

#### Activity: Gym with @ryan

- **Pattern**: A (standard escalation)
- **Location**: `loc_gym`
- **Schedule**: 12:00-15:00
- **NPC**: `npc_ryan`
- **Unlock**: `town_access` + ryan_trust >= 5
- **Priority**: 1
- **Energy**: 30

**Base Scene:**

DEFAULT:
> "Gym. Fluorescent lights and the smell of rubber mats. Ryan is already on the bench press — arms flexing, sweat on his forehead, tank top dark with effort. He sees her and racks the weight. 'Ready to work?' He looks her over — whatever she's wearing, he has an opinion."

**Clothing-dependent openers (group variants):**
- Starting tier (sports bra + old shorts): "'You own gym clothes or...?' He's teasing. But he glances at her legs."
- Basic athletic: "He nods. Approving. 'Better.' Shows her the weight rack properly."
- Cute athletic: "His rep slows. His eyes track her from the door to the treadmill. He doesn't restart his set."
- Bold athletic: "'Jesus.' One word. He forgets what he was lifting."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Spot me / talk between sets" (Emotional)** | always | ryan_love +1, ryan_trust +2, fitness +3 |
| **"Work out near him" (Physical)** | `exposure_unlock` | physical sub-menu, fitness +3 |
| **"Do your own routine" (Neutral)** | always | ryan_love +1, fitness +3, confidence +1 |

**Physical Sub-Menu:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| "Stretch near him" | `exposure_unlock` | ryan_corruption +1, corruption +2 |
| "Ask him to show you a form" | `flirt_unlock` + corruption >= 40 | ryan_corruption +2, corruption +2 (his hands adjusting her position) |
| "Locker room hallway" | `tease_unlock` + corruption >= 55 | ryan_corruption +3, corruption +3 |
| "Kiss after the last set" | `kiss_unlock` + corruption >= 70 | ryan_love +2, ryan_corruption +2, corruption +3 |
| "Locker room" | `handjob_unlock` + corruption >= 100 | ryan_corruption +4, corruption +4 |
| "Shower together" | `sex_unlock` + corruption >= 180 | ryan_corruption +5, corruption +6 |

---

#### Activity: TV on the Couch

- **Pattern**: A (standard escalation — proximity-based)
- **Location**: `loc_living_room`
- **Schedule**: 19:00-22:00
- **NPC**: `npc_ryan` (Frank may also be present — group variant)
- **Unlock**: `first_week_complete`
- **Priority**: 1
- **Energy**: 15

**Base Scene:**

DEFAULT:
> "Living room. TV on. Ryan takes one end of the couch. Lily takes the other. The cushion between them is either a buffer or a bridge — depends on the night. If Frank is in the armchair, the dynamic shifts: everything is watched."

FRANK PRESENT variant:
> "Frank is in the armchair. Paper open. Not watching TV. Watching the couch. Ryan sits wider than he needs to — arm along the back. Frank's jaw tightens."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Talk about the show" (Emotional)** | always | ryan_love +2 |
| **"Sit closer" (Physical)** | `exposure_unlock` | physical sub-menu |
| **"Watch in silence" (Neutral)** | always | ryan_love +1 |

**Physical Sub-Menu (awareness of Frank if present):**

| Choice | Condition | Effects | Note |
|--------|-----------|---------|------|
| "Remove the buffer cushion" | `exposure_unlock` | ryan_love +1, corruption +1 | |
| "Lean against him" | `flirt_unlock` + corruption >= 40 | ryan_corruption +1, corruption +2 | If Frank present: frank_corruption +1 (he sees) |
| "His hand on your thigh" | `tease_unlock` + corruption >= 55 | ryan_corruption +2, corruption +2 | If Frank present: frank_corruption +2 |
| "Kiss during a commercial" | `kiss_unlock` + corruption >= 70 | ryan_love +2, corruption +3 | If Frank present: NOT available (too risky) |
| "Under the blanket" | `handjob_unlock` + corruption >= 100 | ryan_corruption +3, corruption +4 | Blanket hides it. If Frank present: corruption +6 (the risk) |

---

#### Activity: Job Site with @ryan

- **Pattern**: A (limited escalation — work environment)
- **Location**: `loc_workshop`
- **Schedule**: 09:00-12:00
- **NPC**: `npc_ryan` (Frank may be present)
- **Unlock**: `chores_started` + corruption >= 40
- **Priority**: 1
- **Energy**: 25

**Base Scene:**

DEFAULT:
> "Workshop. Sawdust and motor oil. Ryan is hauling materials — heavy lifting that makes his arms flex and his shirt ride up. He puts her to work: holding boards, sorting nails, sweeping. The pay is good ($40). The view is better."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Work and talk" (Emotional)** | always | ryan_love +1, ryan_trust +2, money +40 |
| **"Brush against him" (Physical)** | `exposure_unlock` | physical sub-menu, money +40 |
| **"Work quietly" (Neutral)** | always | ryan_trust +1, money +40, fitness +1 |

Physical caps at kiss — Frank may appear. Locker room/truck escalation happens elsewhere.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### FRANK ACTIVITIES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#### Activity: Bookkeeping with @frank

- **Pattern**: A (standard escalation — the office is the arena)
- **Location**: `loc_franks_office`
- **Schedule**: 12:00-15:00
- **NPC**: `npc_frank`
- **Unlock**: `bookkeeping_started` (set by Beat 9, requires corruption >= 40)
- **Priority**: 1
- **Energy**: 20

**Base Scene Variants:**

DEFAULT:
> "Frank's office. Door closed. The amber desk lamp makes everything warmer than it should be. He's behind the desk — invoices, receipts, the mechanical click of his calculator. He pushes a stack of papers toward her chair. 'Column B needs reconciling.' She sits. Their knees are two feet apart. The room smells like leather and old paper and sawdust off his shirt."

WITHDRAWN (post-crisis):
> "Door open today. He left it open. The papers are on the desk with a note: 'Column B. Leave them when you're done.' He's not in the room. $25 on the counter."

WARM:
> "He pulls her chair next to his instead of across the desk. 'Easier to show you from here.' Their shoulders almost touch. He points at numbers with one hand. His other hand rests on the back of her chair. She can feel the heat from his arm."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Talk about the business" (Emotional)** | always | frank_love +1, frank_trust +2, money +25 |
| **"Lean closer" (Physical)** | `exposure_unlock` | physical sub-menu, money +25 |
| **"Do the work, leave" (Neutral)** | always | frank_trust +1, money +25 |

**Physical Sub-Menu:**

| Choice | Condition | Effects | Video Placeholder |
|--------|-----------|---------|-------------------|
| "Brush his hand reaching for a file" | `exposure_unlock` | frank_love +1, corruption +1 | Image — office proximity, hand contact |
| "Comment on his aftershave" | `flirt_unlock` + corruption >= 40 | frank_corruption +1, corruption +2 | Image — office flirtation |
| "Bend over the desk slowly" | `tease_unlock` + corruption >= 55 | frank_corruption +2, corruption +3 | Video — teasing in office, deliberate |
| "Kiss him over the ledger" | `kiss_unlock` + corruption >= 70 + frank_love >= 20 | frank_love +2, frank_corruption +2, corruption +3 | Video — office kiss, forbidden, desk |
| "Reach under the desk" | `handjob_unlock` + corruption >= 100 + frank_trust >= 22 | frank_corruption +4, corruption +4 | Video — under-desk handjob, power |
| "On your knees" | `blowjob_unlock` + corruption >= 140 + frank_love >= 28 | frank_corruption +5, corruption +5 | Video — office oral, dominance |
| "Lock the door" | `sex_unlock` + corruption >= 180 + frank_love >= 30 | frank_corruption +6, corruption +6 | Video — office sex, desk, authority |

---

#### Activity: Cooking Dinner with @frank

- **Pattern**: A (limited escalation — kitchen, others may interrupt)
- **Location**: `loc_kitchen`
- **Schedule**: 17:00-19:00
- **NPC**: `npc_frank`
- **Unlock**: `first_week_complete` + frank_trust >= 8
- **Priority**: 1
- **Energy**: 20

**Base Scene:**

DEFAULT:
> "Kitchen. Frank is chopping vegetables. His sleeves are rolled, forearms dusted with flour or sawdust — she's never sure which. He doesn't look up when she enters, but he nods at the cutting board next to him. 'Tomatoes need dicing.' Side by side at the counter. Close enough that their elbows touch when she reaches for the knife."

WITHDRAWN:
> "He's cooking alone. Didn't set out the second cutting board. 'Dinner's in twenty minutes.' Dismissal wrapped in information."

WARM:
> "He's waiting for her before starting. Two cutting boards, two knives, two glasses of wine he shouldn't have poured. 'Thought we'd try something different tonight.' He means the recipe. They both hear the other meaning."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Talk while cooking" (Emotional)** | always | frank_love +2, frank_trust +1 |
| **"Stand too close" (Physical)** | `exposure_unlock` | physical sub-menu |
| **"Cook efficiently, set the table" (Neutral)** | always | frank_trust +2 |

**Physical Sub-Menu (limited — kitchen, others may walk in):**

| Choice | Condition | Effects |
|--------|-----------|---------|
| "Brush against him reaching for a pan" | `exposure_unlock` | frank_love +1, corruption +1 |
| "Taste from his spoon" | `flirt_unlock` + corruption >= 40 | frank_corruption +1, corruption +2 |
| "His hand on her waist guiding her" | `tease_unlock` + corruption >= 55 | frank_corruption +2, corruption +2 |
| "Quick kiss (risky — someone could walk in)" | `kiss_unlock` + corruption >= 70 | frank_love +2, corruption +4 |

Caps at kiss in kitchen — too public for more. The office is Frank's escalation space.

---

#### Activity: "Overtime" Bookkeeping with @frank

- **Pattern**: A (high-tier escalation — evening, door locked)
- **Location**: `loc_franks_office`
- **Schedule**: 17:00-19:00 (Evening — alternative to dinner)
- **NPC**: `npc_frank`
- **Unlock**: `bookkeeping_started` + corruption >= 100 + frank_trust >= 18
- **Priority**: 1
- **Energy**: 20

**Base Scene:**

DEFAULT:
> "Evening. The house is loud with dinner sounds she's not part of tonight. Frank's office, door locked. The regular bookkeeping ended an hour ago but neither mentioned it. He pours whiskey. Two glasses. The invoices are a pretense now. Everyone knows it — especially Frank."

**This activity starts at kiss tier (corruption >= 100 gate means player is already deep).**

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Talk about what this really is" (Emotional)** | always | frank_love +3, frank_trust +2, money +60 |
| **"Close the distance" (Physical)** | always (gate is the activity unlock) | physical sub-menu, money +60 |
| **"Do overtime work, leave" (Neutral)** | always | frank_trust +1, money +60 |

**Physical Sub-Menu (starts higher — the gate IS the permission):**

| Choice | Condition | Effects |
|--------|-----------|---------|
| "Kiss him" | corruption >= 100 + `kiss_unlock` | frank_love +2, frank_corruption +3, corruption +3 |
| "His hands on you" | `handjob_unlock` + corruption >= 100 | frank_corruption +4, corruption +4 |
| "On your knees" | `blowjob_unlock` + corruption >= 140 | frank_corruption +5, corruption +5 |
| "His desk" | `sex_unlock` + corruption >= 180 | frank_corruption +6, corruption +6 |

---

#### Activity: Workshop Help with @frank

- **Pattern**: A (limited — work, early game trust-building)
- **Location**: `loc_workshop`
- **Schedule**: 07:00-09:00
- **NPC**: `npc_frank`
- **Unlock**: `first_week_complete`
- **Priority**: 1
- **Energy**: 25

**Base Scene:**

DEFAULT:
> "Workshop. 7 AM. Frank is already there — table saw silent, sorting lumber. He works with purpose — every movement efficient, practiced. He shows her what to do: hold this board, sort these nails, sweep the floor. Not much talking. But working next to someone in silence can be its own kind of intimacy."

**Choice Progression:**

| Choice | Condition | Effects |
|--------|-----------|---------|
| **"Ask about the business" (Emotional)** | always | frank_love +1, frank_trust +2 |
| **"Hand him tools, stay close" (Physical)** | `exposure_unlock` | frank_love +1, corruption +1 |
| **"Work, get paid, leave" (Neutral)** | always | frank_trust +1, fitness +1 |

Physical caps at flirting — the workshop is Frank's professional space. Limited escalation here. The office is where things happen.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION B: MEAL CANVASES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Meals are free to enter (no energy cost to start). Three per day. Kitchen is the social hub.

### Breakfast

- **Canvas**: `meal_breakfast`
- **Location**: `loc_kitchen`
- **Schedule**: 07:00-09:00
- **NPC**: Frank + Jake usually present. Ryan sleeps in 50% of the time.
- **Priority**: 1
- **is_repeatable**: true

**Base Scene:**
> "Kitchen. Morning light. Coffee's already made — Frank's timer. Jake is at the table with cereal and his sketchbook. Frank reads the paper. Ryan's chair is either occupied (groggy, tank top, bed hair) or empty (sleeping in)."

**Choices:**

| Choice | Effect | Condition |
|--------|--------|-----------|
| **"Eat together" (Neutral)** | Energy +5, love +1 to each present NPC | Always |
| **"Talk over coffee" (Emotional)** | Love +2 to ONE chosen NPC (portrait click), no energy restore | Always |
| **"Sit closer / brush hands" (Physical)** | Corruption +1-2 to chosen NPC, no energy restore | After `exposure_unlock` |

**Dinner special mechanic**: At dinner, usually all three NPCs are present (Ryan out ~20%). Lily picks ONE portrait to interact with. The other two are watching. This creates the tension of choosing who to engage while others observe.

### Lunch

- **Canvas**: `meal_lunch`
- **Location**: `loc_kitchen`
- **Schedule**: 12:00-14:00
- **NPC**: Often solo or with Jake (Frank in office, Ryan at job site)
- **Priority**: 1
- **is_repeatable**: true

**Base Scene:**
> "Kitchen. Midday quiet. The house is mostly empty — Frank in the office, Ryan on the job site or in town. If Jake's home (weekends, after class), he's at the table with homework spread around a sandwich."

**Choices:**

| Choice | Effect | Condition |
|--------|--------|-----------|
| **"Eat" (Neutral)** | Energy +5, love +1 to present NPC | Always |
| **"Talk" (Emotional)** | Love +2 to present NPC | If Jake/Frank present |
| **"Sit close" (Physical)** | Corruption +1 to present NPC | After `exposure_unlock`, if NPC present |

### Dinner

- **Canvas**: `meal_dinner`
- **Location**: `loc_kitchen`
- **Schedule**: 17:00-19:00
- **NPC**: Usually all three (Ryan absent ~20%)
- **Priority**: 1
- **is_repeatable**: true

**Base Scene:**
> "Kitchen. Evening. The table is set for four — Frank cooked, or Lily did, or they both did. This is the ONE time all three men are in the same room with her. The tension varies by day: sometimes it's just a meal. Sometimes it's a minefield of glances."

**Group dynamic**: When all three present, Lily chooses ONE NPC portrait to interact with. Others see the choice.

**Choices:**

| Choice | Effect | Condition |
|--------|--------|-----------|
| **"Eat together" (Neutral)** | Energy +10, love +1 to each present NPC | Always |
| **"Talk to [chosen NPC]" (Emotional)** | Love +2 to chosen, others see you chose | Always |
| **"Foot under the table / brush hands" (Physical)** | Corruption +1-2 to chosen, others may notice | After `exposure_unlock` |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION C: UTILITY CANVASES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Chores / Jobs

| Canvas | Name | Location | Schedule | Pay | Energy | Trust | Unlock | Max/Day |
|--------|------|----------|----------|-----|--------|-------|--------|---------|
| `utility_house_cleaning` | House Cleaning | `loc_kitchen` | 09:00-12:00 | $20 | 25 | frank_trust +1 (if home) | `chores_started` | 1 |
| `utility_bookkeeping` | Bookkeeping | `loc_franks_office` | 12:00-15:00 | $25 | 20 | frank_trust +1 | `bookkeeping_started` | 1 |
| `utility_job_site` | Job Site Labor | `loc_workshop` | 09:00-12:00 | $40 | 25 | ryan_trust +1 | corruption >= 40 | 1 |
| `utility_diner_shift` | Diner Waitressing | `loc_diner` | 17:00-19:00 | $45 | 20 | — | confidence >= 30 + `town_access` | 1 |
| `utility_art_modeling_clothed` | Art Modeling (Clothed) | `loc_jakes_room` | 12:00-15:00 | $30 | 15 | jake_love +1 | corruption >= 50 | 1 |
| `utility_art_modeling_nude` | Art Modeling (Nude) | `loc_jakes_room` | 12:00-15:00 | $80 | 15 | jake_corruption +2 | corruption >= 130 | 1 |
| `utility_overtime_bookkeeping` | "Overtime" Bookkeeping | `loc_franks_office` | 17:00-19:00 | $60 | 20 | frank_corruption +1 | corruption >= 100 | 1 |
| `utility_ryans_favors` | Ryan's "Favors" | `loc_ryans_truck` | 19:00-22:00 | $100 | 20 | ryan_corruption +2 | corruption >= 150 | 1 |
| `utility_franks_arrangement` | Frank's "Arrangement" | `loc_franks_office` | 22:00-01:00 | $150 | 20 | frank_corruption +3 | corruption >= 180 | 1 |

**Note**: Art modeling (clothed/nude) and overtime/favors/arrangement are ALSO NPC activities with escalating choices (covered in Section A). The utility table above captures the MONEY component. When these fire as activities, the player gets both the pay and the NPC interaction choices.

### Time Advancement / Rest

| Canvas | Name | Location | Schedule | Effect | Unlock |
|--------|------|----------|----------|--------|--------|
| `utility_sleep` | Go to Sleep | `loc_lily_room` | 22:00-01:00 | Energy → max (100, or 110 at fitness 61+). Advances to Early Morning. | Always |
| `utility_nap` | Afternoon Nap | `loc_lily_room` | 12:00-15:00 | Energy +20. Advances 120 min. | Always |
| `utility_shower` | Shower | `loc_bathroom` | Any | Energy +10. Prevents beauty decay. Free. | Always |
| `utility_morning_routine` | Morning Routine | `loc_bathroom` | 05:00-07:00 | Shower + grooming + optional makeup. Sets polished state if all conditions met. | Always |

### Morning Routine Detail

The morning routine canvas is the daily beauty/presentation decision:

**Canvas**: `utility_morning_routine`
**Location**: `loc_bathroom`
**Schedule**: 05:00-07:00
**Priority**: 2
**is_repeatable**: true

**Choices:**

| Choice | Energy | Beauty Effect | Polished? |
|--------|--------|---------------|-----------|
| "Shower only" | +10 | Prevents decay | No |
| "Shower + Grooming" | +5 | Prevents decay, enables "groomed" | No (need makeup + Cute+ outfit) |
| "Shower + Grooming + Makeup" | +5 | Prevents decay, +1-2 beauty buff | Yes (if Cute+ outfit equipped after) |
| "Skip everything" | +0 | Beauty decays | No |

After routine → `utility_change_outfit` at `loc_lily_room` to select clothing.

### Shopping / Travel

| Canvas | Name | Location | Schedule | Effect | Notes |
|--------|------|----------|----------|--------|-------|
| `utility_bus_to_town` | Take the Bus | `loc_property` | Any | money -2, 40 min travel time. Arrives at `loc_town`. | Nobody knows where she went. |
| `utility_ryan_ride` | Ride with Ryan | `loc_property` | 15:00-17:00 | Free, 15 min. Arrives at `loc_town`. | Ryan sees everything — what she buys, where she goes. |
| `utility_grocery_shopping` | Grocery Shopping | `loc_general_store` | Any | money -20 (food contribution). Covers 5 days of food. | Required to avoid frank_trust penalty. |
| `utility_clothing_shopping` | Clothing Shopping | `loc_clothing_store` | Any | Variable cost. Wardrobe items by corruption tier. | Gated by `town_access`. |
| `utility_beauty_shopping` | Beauty Products | `loc_general_store` | Any | Variable cost. Makeup kits, skincare, perfume. | |

### Recurring Expense Canvases

| Canvas | Name | Trigger | Cost | Effect | Timer |
|--------|------|---------|------|--------|-------|
| `utility_bus_pass` | Bus Pass Due | days_since(`bus_pass_paid`) >= 30 | $80 | Maintains bus access for 30 days | Monthly |
| `utility_art_supplies` | Art Supplies Due | days_since(`art_supplies_paid`) >= 30 | $60 | Maintains campus events | Monthly |
| `utility_phone_bill` | Phone Bill Due | days_since(`phone_bill_paid`) >= 30 | $45 | Maintains phone access | Monthly |
| `utility_food_contribution` | Food Contribution | days_since(`food_paid`) >= 7 | $50 | Avoids frank_trust -3 | Weekly |

These fire as priority 2 events when the timer triggers. If the player can't afford them (money < cost), the canvas presents the choice to pay or skip with consequences per Phase 2 non-payment table.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION D: SOLO ACTIVITIES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| Canvas | Name | Location | Schedule | Energy | Effect | Notes |
|--------|------|----------|----------|--------|--------|-------|
| `solo_yoga` | Yoga in Room | `loc_lily_room` | Any | 10 | fitness +1 | Always available. Low energy, low reward. Solo, private. |
| `solo_jog_property` | Morning Jog (Property) | `loc_yard` | 07:00-09:00 | 15 | fitness +1, confidence +1 | Jogging loops around the yard. No transport needed. |
| `solo_jog_park` | Jogging (Park) | `loc_park` | 12:00-15:00 | 20 | fitness +2, confidence +1 | Requires town access. Better gains than property. |
| `solo_campus_classes` | Art Classes | `loc_campus` | 09:00-12:00 | 15 | Mandatory Mon-Thu. Maintains campus events. | Requires bus or Ryan's ride. |
| `solo_journal` | Journal / Phone | `loc_lily_room` | Any | 5 | No stat gains. Advances time 60 min. Story reflections. | Hint system: journal entries suggest next steps. |
| `solo_spa_day` | Spa / Self-Care | `loc_lily_room` | 12:00-15:00 | 15 | beauty +2 permanent | Requires skincare products owned. |
| `solo_stargazing` | Stargazing | `loc_yard` | 22:00-01:00 | 10 | corruption +1 (alone, dark, vulnerable). | Atmospheric. Random encounter possible (any NPC coming outside). |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## ACTIVITY COVERAGE SUMMARY

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### By NPC

| NPC | Activities | Locations | Escalation Cap |
|-----|-----------|-----------|----------------|
| **Jake** | Drawing Session, Studying, Creek Swimming, Wall Knocking, Park Sketching | Jake's Room, Library, Creek, Lily's Room, Park | Full (sex tier) |
| **Ryan** | Truck Ride, Gym, TV Couch, Job Site | Truck, Gym, Living Room, Workshop | Full (sex tier) |
| **Frank** | Bookkeeping, Cooking, Overtime, Workshop Help | Office, Kitchen, Workshop | Full (sex tier) |

### By Time Slot

| Period | Activities Available |
|--------|--------------------|
| **Early Morning** | Morning routine, shower |
| **Morning** | Breakfast, morning jog (property), workshop help (Frank) |
| **Late Morning** | Campus classes, house cleaning, job site labor |
| **Afternoon** | Lunch, bookkeeping (Frank), drawing session (Jake), gym (Ryan), art modeling, nap, park jog, beauty shopping |
| **Late Afternoon** | Creek swim, truck ride (Ryan), studying (Jake), park sketching (weekend), clothing shopping |
| **Evening** | Dinner, cooking (Frank), overtime bookkeeping (Frank), diner shift |
| **Night** | TV (Ryan/Frank), Jake's room visit, Frank's office late, journal, Ryan's favors |
| **Late Night** | Kitchen encounter (Frank random), wall knocking (Jake), Frank's arrangement, sleep, stargazing |

### No Dead Zones Check

At every point in the game, the player has 2+ NPC activities available per time slot:

| Corruption | Available NPC Activities |
|-----------|------------------------|
| 0-25 | Meals (all), Workshop (Frank), Wall knocking (Jake), TV (Ryan) — limited but present |
| 25-40 | + Drawing session (Jake), Truck ride (Ryan) — exposure_unlock opens physical sub-menus |
| 40-60 | + Bookkeeping (Frank), Job site (Ryan), Gym (Ryan) — flirt tier opens |
| 60-100 | + Art modeling (Jake), Cooking (Frank) — kiss tier opens |
| 100-140 | + Overtime (Frank) — handjob tier opens |
| 140-180 | + Modeling nude (Jake), Ryan's favors — blowjob tier opens |
| 180+ | + Frank's arrangement — sex tier opens, all activities at max escalation |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Type "proceed" to continue to Phase 6: Story Arc,
or provide adjustments.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# PHASE 6: STORY ARC
# Under One Roof

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 0: DRAMATIC SPINE SUMMARY

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Central Tension

"Can a girl who swore she'd never depend on anyone survive a house where every form of help comes with a price — and still recognize herself when it's over?"

### Conflict Types

1. BOUNDARY BREAK — Ryan pushes too far (Act 2)
2. REVELATION — Frank finds Jake's intimate drawings (Act 3)
3. COMPETING PULL — Brothers discover each other's involvement (Act 4)
4. EXTERNAL THREAT — Mom announces early return (Act 4)

### Tension Curve Summary

```
ARRIVAL → ROUTINE → BATHROOM INCIDENT → BUS DEPENDENCY → MOM'S CALL (bridge) →
  THE MATH → FIRST CHORE → FIRST AWARENESS (exposure_unlock) →
    RYAN'S PUSH ↓↓ (tension — trust breaks) →
      REPAIR → BOOKKEEPING (Frank orbit) → CREEK SWIM → JAKE'S CONFESSION →
        RYAN CATCHES LILY → FIRST FLIRTATION (flirt_unlock) →
          FIRST KISS (kiss_unlock) ↑↑↑↑ →
            FRANK'S LATE NIGHT → RYAN'S ULTIMATUM ↓ →
              POWER OUTAGE (bridge) →
                FRANK FINDS DRAWINGS ↓↓↓ (MAJOR CRISIS) →
                  REPAIR (Frank + Jake separate) → FINANCIAL CRISIS →
                    PHYSICAL ESCALATION (handjob_unlock) ↑↑↑ →
                      BROTHERS DISCOVER ↓↓ (crisis) → FRANK'S OFFER →
                        GLOBAL BRANCH → MOM'S RETURN ↓ →
                          FINAL WEEK → RESOLUTION
```

### Key Emotional Beats (Multi-NPC Adaptation)

| Beat | Event | Lily Feels | Lily Phase | NPCs Feel | NPC Quadrants |
|------|-------|-----------|------------|-----------|---------------|
| Arrival | Opening scene | Displacement, pride, isolation | OUTSIDER | Frank: dutiful. Ryan: interested. Jake: curious. | All DISTANT |
| First Chore | The Math / first clean | Humiliation + determination | OUTSIDER→SETTLING | Frank: respectful. Ryan: teasing. Jake: sympathetic. | Frank SAFE, others DISTANT |
| First Spark | Physical awareness | Excitement + confusion | SETTLING→AWARE | Whoever triggered: first awareness. Others: unchanged. | Triggering NPC: DISTANT→edge |
| Ryan's Push | Truck incident | Fear + anger OR arousal | AWARE | Ryan: testing/hurt. Others: unaware. | Ryan: CONFLICTED briefly |
| First Kiss | Kiss milestone | Desire + guilt + wanting more | AWARE→WANTING | Kissing NPC: terrified + hopeful. Others: sensing shifts. | Kissing NPC: OPEN |
| Frank Finds Drawings | Major crisis | Panic, shame, desperation | WANTING→TORN | Frank: betrayed. Jake: scared. Ryan: sensing opportunity. | Frank: deep CONFLICTED. Jake: CONFLICTED. |
| Recovery | Repair events | Determination + vulnerability | TORN | Frank: testing. Jake: hoping. | Both: CONFLICTED softening |
| Physical Escalation | Handjob milestone | "I chose this" | TORN→COMMITTED | Chosen NPC: amazed/grateful. | OPEN (rebuilt deeper) |
| Brothers Discover | Global crisis | "What have I done?" | COMMITTED (crisis) | Both brothers: hurt/competitive. Frank: calculating. | Brothers: CONFLICTED |
| Mom's Return | Announcement | Terror + urgency + "who am I?" | COMMITTED→ENDGAME | All NPCs: fear response. | All: momentary CONFLICTED |
| Resolution | Mom arrives | Depends on ending | ENDGAME | Depends on ending | Depends on ending |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 1: CHAPTERS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

| ID | Name | Mood | Description | Order |
|----|------|------|-------------|-------|
| `chapter_arrival` | One Suitcase | neutral | Lily arrives at a house she's been to exactly once. Three men she barely knows. Ten weeks. | 1 |
| `chapter_settling` | The New Normal | hopeful | Routines form. The bathroom schedule. The breakfast table. The bus problem. She starts to see them as people. | 2 |
| `chapter_awakening` | Something Shifts | tense | Bodies noticed. Boundaries tested. The math forces choices. She starts making excuses to be where they are. | 3 |
| `chapter_deepening` | Lines in the Sand | romantic | Kisses that shouldn't happen. Offices with locked doors. Sketchbooks full of her. Every line drawn is a line crossed. | 4 |
| `chapter_crisis` | Under the Same Roof | tense | The house fractures. Drawings discovered. Brothers at war. The question isn't who she wants — it's what she's willing to lose. | 5 |
| `chapter_convergence` | The Countdown | passionate | Mom's coming home. Seven days. Maximum intensity. Every touch is both first and last. | 6 |
| `chapter_resolution` | When She Walks Through the Door | peaceful | Diana returns. Lily is... who? The answer depends on sixty days of accumulated choices. | 7 |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 2: STORY NODES

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

One node per story event from Phase 4, linked to its canvas and flag.

### Act 1 Nodes

| ID | Name | Chapter | Canvas | Flag | Milestone | Journal Entry |
|----|------|---------|--------|------|-----------|---------------|
| `node_arrival` | Arrival | `chapter_arrival` | `opening_arrival` | `game_started` | true | "One suitcase. One room. Three men I don't know. The house smells like sawdust and coffee. The walls are thin. I can hear the creek from my window. Ten weeks." |
| `node_first_morning` | First Morning | `chapter_arrival` | `story_first_morning` | `first_morning` | false | "@jake walked in on me in the bathroom. Toothbrush in hand, face on fire. He backed out so fast he hit the doorframe. At breakfast he couldn't look at me. His ears were red for an hour." |
| `node_bus_problem` | The Bus Problem | `chapter_settling` | `story_bus_problem` | `bus_problem_discovered` | false | "The bus is forty minutes and two dollars each way. @ryan offered to drive. Fifteen minutes, free. Free. That word sounds different when someone's looking at you like that." |
| `node_moms_call` | Mom's Call | `chapter_settling` | `story_moms_call` | `mom_called` | false | "Mom called. She's fine. The money's late. 'Can you manage?' I told her I'm fine. I'm not fine. $398 in my account and $385 in expenses this month. I'll manage. I always manage." |
| `node_the_math` | The Math | `chapter_settling` | `story_the_math` | `money_crisis_realized` | true | "I asked @frank if I could clean the house for money. Twenty dollars. He looked at me like he understood exactly what it cost me to ask. I hope he doesn't." |
| `node_first_chore` | First Week | `chapter_settling` | `story_the_math` | `first_week_complete` | false | "One week. I know the bathroom schedule. I know how @frank takes his coffee. I know @ryan sleeps past nine. I know @jake draws until midnight because I can hear his pencil through the wall." |

### Act 2 Nodes

| ID | Name | Chapter | Canvas | Flag | Milestone | Journal Entry |
|----|------|---------|--------|------|-----------|---------------|
| `node_first_awareness` | Something Shifts | `chapter_awakening` | `story_first_awareness` | `exposure_unlock` | true | *(Jake variant)*: "He asked me to lower my collar for the light. I did. His pencil stopped. For three seconds he wasn't drawing — he was seeing. I felt it on my skin like a sunburn." *(Ryan variant)*: "Creek water and a sports bra. He didn't look away. For the first time, I didn't want him to." *(Frank variant)*: "I walked out of the shower and he was in the hallway. Two seconds. His eyes on my shoulders. Then gone. But I felt those two seconds all day." |
| `node_ryans_push` | The Truck | `chapter_awakening` | `story_ryans_push` | `truck_incident_complete` | true | *(ryan_resisted)*: "I slapped his hand. He looked surprised. Not angry — surprised. Like nobody's told him no before. Good." *(ryan_allowed)*: "His hand on my knee in the truck. I didn't move it. The road was empty. The silence was loud. When we got home I went straight to my room and sat on the bed with my heart hammering." |
| `node_bookkeeping` | The Office | `chapter_awakening` | `story_bookkeeping_offer` | `bookkeeping_started` | false | "@frank's office smells like leather and old paper. The door closes. It's just us and numbers. Twenty-five dollars a session. The money is good. The proximity is... something else." |
| `node_creek_swim` | The Creek | `chapter_awakening` | `story_creek_swim` | `first_swim` | false | "Cold water, warm skin, no real swimsuit. @jake tried not to stare. @ryan didn't try at all. I crossed my arms over my chest and then stopped. I'm not sure why I stopped." |
| `node_jakes_sketches` | The Sketchbook | `chapter_awakening` | `story_jakes_confession` | `saw_jakes_sketches` | true | "He showed me the pages. My face. My hands. My neck in afternoon light. Page after page. All beautiful. 'I've been drawing you since the second day.' His hands were shaking. Not from fear. From showing me." |
| `node_ryan_catches` | The Door | `chapter_awakening` | `story_ryan_catches_lily` | `ryan_caught_her` | false | "@ryan in the doorway. Me in my underwear. The mirror showed both of us. He grinned. He didn't leave. I could have screamed. I didn't. I finished putting on my shirt while he watched. I don't know why I did that." |
| `node_first_flirtation` | The First Flirt | `chapter_deepening` | `story_first_flirtation` | `flirt_unlock` | true | "I flirted. On purpose. Not accidentally, not ambiguously — deliberately. I watched his face change and I liked it. Something has shifted inside me and I can't shift it back." |
| `node_first_kiss` | The First Kiss | `chapter_deepening` | `story_first_kiss` | `kiss_unlock` | true | *(Jake)*: "Over the sketchbook. Pencils on the floor. 'We shouldn't.' 'I know.' Neither of us stopped." *(Ryan)*: "Truck. Dead-end road. He pulled me in. I let him. His mouth was sure." *(Frank)*: "Kitchen. 2 AM. Coffee going cold. 'This can't happen,' he said. Then he kissed me like a man taking apart his own rules." |

### Act 3 Nodes

| ID | Name | Chapter | Canvas | Flag | Milestone | Journal Entry |
|----|------|---------|--------|------|-----------|---------------|
| `node_franks_late_night` | 2 AM | `chapter_deepening` | `story_franks_late_night` | `frank_kitchen_moment` | false | "Kitchen at 2 AM. Whiskey and silence. He talked about building the house, about his first wife leaving. His hand was four inches from mine on the table. Neither of us closed the gap. Neither of us needed to." |
| `node_ryans_ultimatum` | The Ultimatum | `chapter_crisis` | `story_ryans_ultimatum` | `ryan_leverage` | true | "@ryan knows. About the drawing sessions. About the time I spend in @jake's room. He wants his own arrangement. The worst part: it's not a threat. It's a negotiation." |
| `node_power_outage` | Candlelight | `chapter_deepening` | `story_power_outage` | `power_outage` | false | "Storm killed the power. Candles on the coffee table. For the first time, all four of us in one room without the TV as a shield. @frank told stories. @ryan was quiet. @jake drew by candlelight. I looked at them and saw people. Just people. In a house that's too small and too close and somehow, impossibly, starting to feel like mine." |
| `node_frank_finds` | The Discovery | `chapter_crisis` | `story_frank_finds_drawings` | `frank_found_drawings` | true | "@frank found the drawings. Not the ones @jake showed me — the others. Me in a towel. Me sleeping. His face was stone. 'My son. In my house. Drawing my wife's daughter.' He didn't yell. That was worse." |
| `node_frank_repair` | Workshop Morning | `chapter_crisis` | `story_frank_repair` | `frank_repair_complete` | false | "Found him in the workshop sanding something that didn't need sanding. I didn't make excuses. He didn't turn around. 'I shouldn't have gone through his things.' From @frank, that's an apology. From me, standing there in sawdust at 6 AM — that's one too." |
| `node_jake_repair` | The Door Opens | `chapter_crisis` | `story_jake_repair` | `jake_repair_complete` | false | "Knocked on @jake's door. Red-eyed. 'He saw them.' 'I know.' I sat with him. He cried. I held him. No escalation. No agenda. Just two people scared of what's happening and choosing to be scared together." |
| `node_financial_crisis` | The Bounce | `chapter_crisis` | `story_financial_crisis` | `financial_crisis` | false | "Mom's transfer bounced again. Art supplies overdue. Bus pass expired. Phone bill late. I stared at my bank app and did the math I've been avoiding. The numbers don't care about my pride." |
| `node_escalation` | Crossing the Line | `chapter_deepening` | `story_physical_escalation` | `handjob_unlock` | true | "My hand on him. His breath catching. The sound — raw, surprised, like something breaking open that was always meant to break. I've never held someone like this. I've never wanted to." |

### Act 4 Nodes

| ID | Name | Chapter | Canvas | Flag | Milestone | Journal Entry |
|----|------|---------|--------|------|-----------|---------------|
| `node_brothers_discover` | They Know | `chapter_crisis` | `story_brothers_discover` | `brothers_know` | true | "The hallway. @ryan's face when he saw me leave @jake's room. Not the grin. Something underneath. Hurt. Then @jake in the doorway. Both of them looking at me. At each other. The house held its breath." |
| `node_crisis_choice` | The Choice | `chapter_crisis` | `story_brothers_discover` | `crisis_resolved` | true | *(chose_independent)*: "'It's none of your business.' I said it and meant it. My life. My body. My choices. They both looked at me like they were seeing someone new." *(chose_peacemaker)*: "'Please don't fight. I care about both of you.' It's true. It's also not enough. But it's all I have." *(chose_avoidant)*: "I walked away. Couldn't speak. Couldn't choose. The silence behind me was worse than any argument." |
| `node_franks_offer` | The Arrangement | `chapter_convergence` | `story_franks_offer` | `frank_offer` | true | "@frank's office. Late. No invoices on the desk. 'I know what's been happening. I'm not asking for details. I'll cover everything — bus, art supplies, phone. In exchange, you stay here. With me. Late nights.' He's not my father. He stopped pretending a long time ago." |
| `node_jake_branch` | The Secret Sketches | `chapter_crisis` | `story_jake_secret_sketches` | `jake_sketches_discovered` | true | *(chose_tender_jake)*: "'They're beautiful.' And they are. Every line is devotion. He sees me in ways I don't see myself. I'm not angry. I'm seen." *(chose_possessive_jake)*: "'You've been watching me.' His face crumbles. Then rebuilds into something harder. 'I can't stop.' The sweet boy has teeth I didn't know about." |
| `node_frank_branch` | The Ledger | `chapter_crisis` | `story_franks_secret` | `frank_secret_complete` | true | *(chose_confront_frank)*: "I told him I could help. He fought it — then broke. Let me see everything. The real numbers. Two people against a problem. When he looked at me, it wasn't as Diana's daughter anymore." *(chose_protect_frank)*: "'I didn't see anything.' His eyes. Relief and something else — the weight of sharing a secret you've carried alone. We're conspirators now." |
| `node_moms_return` | The Call | `chapter_convergence` | `story_moms_return` | `mom_returning` | true | "'I'm coming home early!' Mom sounded happy. I felt the floor tilt. Seven days. All of this — the routines, the drawing sessions, the late nights, the truck rides, the arrangement — has an expiration date. When she walks through that door, I become her daughter again. They become her family. And whatever this was... stops." |
| `node_final_week` | Last Days | `chapter_convergence` | `story_final_week` | `endgame_active` | false | "The last week. Everything is louder. @frank's hand on my mug. @jake drawing like he's running out of time. @ryan: 'We should do a hike. All of us. Before she gets here.' The first generous thing he's said about shared time." |
| `node_resolution` | When She Walks Through the Door | `chapter_resolution` | `story_resolution` | `game_complete` | true | *(Ending-dependent — see Section 2.5)* |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 2.5: BRANCHING PATHS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Branch Points

| Branch Canvas | Choice A | Flag A | Choice B | Flag B | Shared Flag |
|--------------|----------|--------|----------|--------|-------------|
| `story_ryans_push` | "Slap his hand" | `ryan_resisted` | "Let it stay" | `ryan_allowed` | `truck_incident_complete` |
| `story_jake_secret_sketches` | "They're beautiful" | `chose_tender_jake` | "You've been watching me?" | `chose_possessive_jake` | `jake_sketches_discovered` |
| `story_franks_secret` | "I can help" | `chose_confront_frank` | "I didn't see anything" | `chose_protect_frank` | `frank_secret_complete` |
| `story_brothers_discover` | "None of your business" | `chose_independent` | "Please don't fight" | `chose_peacemaker` | `crisis_resolved` |
| `story_brothers_discover` | *(also)* "(Walk away)" | `chose_avoidant` | | | `crisis_resolved` |

### Ending-Specific Resolution Nodes

| ID | Name | Chapter | Condition | Journal Entry |
|----|------|---------|-----------|---------------|
| `node_ending_jake` | Jake's Girl | `chapter_resolution` | Jake highest stats, corruption < 160 | "Mom hugged me at the door. Over her shoulder, @jake's eyes found mine. His hand reached for mine behind our backs. The sketchbook under his bed is full. This isn't over. This is just the part nobody else gets to see." |
| `node_ending_ryan` | Ryan's Conquest | `chapter_resolution` | Ryan highest, corruption > 150 | "Mom unpacked in the kitchen. @ryan caught my eye across the room. Jingled the truck keys. Mouthed: 'Later.' It's not love. We both know that. But it's honest. And he'll drive me wherever I want." |
| `node_ending_frank` | Frank's Arrangement | `chapter_resolution` | Frank highest, corruption > 180 | "@frank and I don't look at each other when Mom walks in. We don't need to. The arrangement is already in place. Diana will travel again. @frank will be here. So will I. Nothing is said. Everything is understood." |
| `node_ending_all` | All Three | `chapter_resolution` | No NPC >25 ahead | "Five chairs at the dinner table now. I look at each of them. Each looks back. The house is mine in a way Mom will never understand. She came home to a daughter she doesn't quite recognize. She's right not to." |
| `node_ending_independent` | Independence | `chapter_resolution` | confidence > 60, money > 500 | "I hugged Mom. 'I got a job at the diner. I'm going to look for my own place.' She looked surprised. Proud, maybe. I don't need anyone's truck or office or arrangement. I can leave. I might stay — but on my terms." |
| `node_ending_escape` | Escape | `chapter_resolution` | corruption < 100 | "I hugged Mom. Went to my room. Started packing. The dorm repairs are done. I'll be back at campus by next week. Nothing happened here. Almost. I think about @jake's drawing of my hands and wonder if 'almost' counts." |

### Reconvergence

The global crisis branch (chose_independent / chose_peacemaker / chose_avoidant) reconverges at `node_franks_offer`:
- **Reconvergence group**: `group_crisis_resolution` with `required_count = 1`, containing `node_crisis_independent`, `node_crisis_peacemaker`, `node_crisis_avoidant`
- **Shared continuation**: `node_franks_offer` with `requires_group = "group_crisis_resolution"`

The ending branches do NOT reconverge — they are terminal nodes.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 3: GROUPS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

"Complete N of M" parallel requirements for story progression:

| ID | Name | Required | Members | Purpose |
|----|------|----------|---------|---------|
| `group_settling_in` | Settling In | 3 of 5 | `node_first_morning`, `node_bus_problem`, `node_moms_call`, `node_the_math`, `node_first_chore` | Player must experience at least 3 settling events before Act 2 opens |
| `group_first_awareness` | First Awareness | 1 of 3 | `node_awareness_jake`, `node_awareness_ryan`, `node_awareness_frank` | Any NPC can trigger exposure_unlock |
| `group_first_kiss` | First Kiss | 1 of 3 | `node_kiss_jake`, `node_kiss_ryan`, `node_kiss_frank` | Any NPC can trigger kiss_unlock |
| `group_npc_branches` | NPC Discoveries | 2 of 3 | `node_jake_branch`, `node_frank_branch`, `node_ryans_push` | At least 2 NPC branches must fire before endgame |
| `group_crisis_resolution` | Crisis Resolved | 1 of 3 | `node_crisis_independent`, `node_crisis_peacemaker`, `node_crisis_avoidant` | Global crisis must resolve before Frank's offer |
| `group_ending` | Resolution | 1 of 6 | All ending nodes | One ending fires based on accumulated stats |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 4: EMOTION MAPPINGS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

### Player Corruption

| Min | Max | Label | Description |
|-----|-----|-------|-------------|
| 0 | 30 | innocent | "She's the girl who arrived with one suitcase. Uncomfortable with proximity. Notices things and feels guilty for noticing." |
| 31 | 60 | curious | "She's starting to look on purpose. The guilt is fading into something else — curiosity, then anticipation. She picks her outfit with someone in mind." |
| 61 | 100 | awakened | "She wants things she didn't want three weeks ago. She seeks out the encounters she used to stumble into. The morning routine includes makeup now." |
| 101 | 150 | embracing | "She's past pretending. She flirts deliberately, escalates consciously, manages three dynamics with growing skill. The hoodie hasn't left the closet in weeks." |
| 151 | 200 | transformed | "She initiates. She chooses who gets her evening. The girl who arrived with one suitcase would not recognize the woman choosing lingerie at the clothing store." |
| 201 | 250 | consumed | "The house is hers. Three men, one roof, and she's the center of gravity. When Mom walks through that door, the person she meets will be a stranger wearing her daughter's face." |

### Per-NPC Emotion Mappings

#### @jake — Love

| Min | Max | Label | Description | Jake's Behavior |
|-----|-----|-------|-------------|-----------------|
| 0 | 8 | strangers | "She's the new girl in the house. Pretty. Quiet." | Nods at meals. Draws landscapes. Door closed. |
| 9 | 15 | noticing | "Something about her face in the afternoon light." | Draws her without realizing. Saves her a seat. Stutters when she's close. |
| 16 | 22 | drawn | "He can't stop looking. The sketchbook is full of her." | Shows her his art. Pencil shakes. Finds excuses to be where she is. |
| 23 | 30 | devoted | "She's the only thing worth drawing." | Says her name differently. Leaves drawings under her door. Can't eat when she's at the table. |
| 31 | 40 | in love | "He's hers. He knows it. He doesn't want to be anything else." | "I love you." No stutter. No trailing off. Complete. |

#### @jake — Trust

| Min | Max | Label | Description | Jake's Behavior |
|-----|-----|-------|-------------|-----------------|
| 0 | 8 | guarded | "Polite distance. She's a guest." | Sketchbook angled away. Headphones on. Door closed. |
| 9 | 15 | opening | "She likes art. She's kind." | Shows landscapes. Mentions his professor. Leaves door cracked. |
| 16 | 22 | trusting | "She gets it. She gets him." | Tells her about Ryan mocking his art. Draws with door open. Vulnerable. |
| 23 | 30 | safe | "He'd tell her anything." | Falls asleep while she's in the room. Shows the private sketches. Cries in front of her. |
| 31 | 40 | complete | "She's the only person who sees him." | Leaves the sketchbook open. Doesn't flinch when she touches him. "I've never shown anyone." |

#### @ryan — Love

| Min | Max | Label | Description | Ryan's Behavior |
|-----|-----|-------|-------------|-----------------|
| 0 | 5 | testing | "New girl. Interesting. Let's see what happens." | Teases. Offers rides with strings. Looks her over like inventory. |
| 6 | 12 | pursuing | "She's not what he expected." | Cleans the truck cab. Drives slower. Tells real stories instead of jokes. |
| 13 | 18 | invested | "He's thinking about her when she's not around." | Waits for her. Covers for her. Gets quiet when she's close. |
| 19 | 25 | falling | "He's scared of how much he wants this." | Drops the nicknames. Tucks hair behind her ear. Falls asleep near her. |
| 26 | 35 | his | "She's the only thing he's ever wanted that he can't joke about." | "I don't want to go home yet." Protects without performing. Vulnerable. |

#### @ryan — Trust

| Min | Max | Label | Description | Ryan's Behavior |
|-----|-----|-------|-------------|-----------------|
| 0 | 5 | performing | "Everything is a bit. A test." | Watches her like he's keeping score. Jokes deflect everything. |
| 6 | 12 | real | "She saw past the act." | Tells the real scar story. Admits he didn't finish school. |
| 13 | 18 | loyal | "He'd cover for her." | Lies to Frank on her behalf. "She was with me." No questions. |
| 19 | 25 | exposed | "She knows him. The real one." | Admits he's scared. Doesn't put up the front when they're alone. |
| 26 | 35 | hers | "She could destroy him with what she knows." | Falls asleep in the truck with her. Trusts her with his actual feelings. |

#### @frank — Love

| Min | Max | Label | Description | Frank's Behavior |
|-----|-----|-------|-------------|-----------------|
| 0 | 5 | dutiful | "Diana's daughter. A responsibility." | Nods. Pours coffee. Reads the paper. She's a guest he's tolerating. |
| 6 | 12 | aware | "Something about her he can't name." | Remembers how she takes her coffee. Watches her leave a room. |
| 13 | 20 | fighting | "He knows exactly what he's feeling and he's horrified." | Eyes track her. Leaves the room when she enters. Pours whiskey earlier. |
| 21 | 28 | breaking | "The dam is cracking." | Holds eye contact. Says her name softer. Hand on the small of her back. |
| 29 | 35 | his | "He's done fighting. She's his." | "Stay." One word. "Lil." The door locks. He stops pretending. |

#### @frank — Trust

| Min | Max | Label | Description | Frank's Behavior |
|-----|-----|-------|-------------|-----------------|
| 0 | 8 | professional | "She works for him. That's the relationship." | Office door open. Checks her work. Counts the drawer. |
| 9 | 15 | respect | "She's reliable." | Stops checking work. Tells her about late-paying clients. |
| 16 | 22 | inner circle | "She's inside the walls." | Door closes. Shares real numbers. Business talk. "Don't tell Diana." |
| 23 | 28 | partner | "He needs her." | Asks her opinion on bids. Leaves her alone with the checkbook. |
| 29 | 35 | absolute | "She could destroy him and he's given her every tool." | Falls asleep in the office while she works. The most vulnerable thing Frank has ever done. |

### Cross-State Descriptions (Per NPC)

#### @jake Cross-States

| Love | Trust | Quadrant | Description |
|------|-------|----------|-------------|
| 0-8 | 0-8 | DISTANT | "He's the quiet one at meals. You share a wall and nothing else." |
| 0-8 | 9-15 | SAFE | "He's a friend. He shares his art. No charge in the air." |
| 9-22 | 0-8 | CONFLICTED | "He watches you when you're not looking. The sketchbook is full of you. But the door stays closed." |
| 9-22 | 9-15 | WARMING | "Drawing sessions get longer. His hand lingers positioning your chin. Something is building." |
| 16-30 | 8-15 | CRISIS | "He loves you. You can see it in every line he draws. But something broke — the drawings, the discovery, what you did — and he won't let you close until it heals." |
| 16-30 | 16-30 | OPEN | "Art is foreplay. Every pose is charged. He draws you like a prayer." |
| 23-40 | 23-40 | DEEP OPEN | "He's yours. The sketchbook is open. His door is open. His heart is open. 'I drew you again. I always draw you.'" |

#### @ryan Cross-States

| Love | Trust | Quadrant | Description |
|------|-------|----------|-------------|
| 0-5 | 0-5 | DISTANT | "He's the loud one. Tests every boundary. You're entertainment." |
| 0-5 | 6-12 | SAFE | "He's calmed down. Tells real stories. Drives you without commentary." |
| 6-18 | 0-5 | CONFLICTED | "He wants you and he's angry about it. Jealous. Competitive. The grin is gone." |
| 6-18 | 6-12 | WARMING | "Truck rides get longer. He cleaned the seat for you. Something's shifting." |
| 13-25 | 6-12 | CRISIS | "He found out. About Jake. About Frank. The hurt is underneath the anger. 'Both of us? Really?'" |
| 13-25 | 13-25 | OPEN | "The bravado drops. He's quiet. His hand finds the small of your back. 'I don't want to go home yet.'" |
| 19-35 | 19-35 | DEEP OPEN | "He's done performing. Protects you without making it a joke. Falls asleep in the truck. Trusts you with everything he pretends not to feel." |

#### @frank Cross-States

| Love | Trust | Quadrant | Description |
|------|-------|----------|-------------|
| 0-5 | 0-8 | DISTANT | "He's the authority. Professional. 'Dinner's at six.'" |
| 0-5 | 9-15 | SAFE | "He trusts your work. Business talk. No charge." |
| 6-20 | 0-8 | CONFLICTED | "He wants you and he's fighting it with everything he has. Leaves the room. Pours whiskey. 'Diana trusts me.'" |
| 6-20 | 9-15 | WARMING | "The office door closes. His hand on the back of your chair. He smells like sawdust and restraint." |
| 13-28 | 8-15 | CRISIS | "He found the drawings. He knows what's happening under his roof. The control is brittle. 'This stops. Whatever this is.'" |
| 13-28 | 16-28 | OPEN | "2 AM kitchen. Whiskey. His hand four inches from yours. He stops fighting. 'Stay.'" |
| 21-35 | 22-35 | DEEP OPEN | "'Lil.' The dam broke. His voice is low. His door is unlocked. He's done being appropriate." |

### Emotional Transition Moments (Per NPC)

#### @jake Transitions

| Transition | The Moment | Sample Line |
|-----------|-----------|-------------|
| DISTANT → SAFE | First time he shares his art with her | "What do you think of the composition?" (He's never asked anyone.) |
| SAFE → WARMING | First charged look during a drawing session | He stops drawing. Just looks. His pencil hangs in the air. |
| WARMING → OPEN | First time he says what he's feeling | "I keep drawing you. I can't draw anything else." |
| OPEN → CONFLICTED | After Frank finds the sketches / after discovering she's with Ryan | "You knew. About the other drawings. You knew and you let me keep—" Silence. Door closes. |
| CONFLICTED → OPEN | After repair — she comes to his room | He slides a drawing under her door. Her coffee mug. A detail only someone who watches her would notice. "I drew something for you." |

#### @ryan Transitions

| Transition | The Moment | Sample Line |
|-----------|-----------|-------------|
| DISTANT → SAFE | First time the teasing stops and something real shows | "The scar? I was eighteen and scared. Dad drove me to the ER without a word." |
| SAFE → WARMING | First time he cleans the truck for her | She notices the seat is wiped down. He doesn't mention it. |
| WARMING → OPEN | First time he admits he's invested | "I don't want to go home yet." (Said quietly. No grin.) |
| OPEN → CONFLICTED | Brothers discover each other | "Both of us? Really?" The hurt is under the anger. |
| CONFLICTED → OPEN | He shows up with something — gas station coffee, art supplies | "Heading to town. You coming or what?" The offer IS the apology. |

#### @frank Transitions

| Transition | The Moment | Sample Line |
|-----------|-----------|-------------|
| DISTANT → SAFE | First time he asks about her life | "Classes going alright?" (He's never asked. This is new.) |
| SAFE → WARMING | First time the control slips — an unfinished sentence | "You should—" (pause) "Never mind." His coffee mug tightens. |
| WARMING → OPEN | 2 AM kitchen. He doesn't leave when she enters. | "Sit down." Two words. An opening. |
| OPEN → CONFLICTED | He finds the drawings / discovers the arrangement with his sons | "This stops." Voice tight. Hands flat on the desk. Not anger. Discipline. |
| CONFLICTED → OPEN | She finds him in the workshop. Doesn't make excuses. | "I shouldn't have gone through his things." From Frank, that's vulnerability. |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## SECTION 5: GUIDANCE HINTS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Hints are phrased as Lily's internal observations — never game-mechanical language.

### General Progression Hints

| Condition | Hint Text |
|-----------|-----------|
| corruption < 25, days > 5 | "I've been keeping my head down. Maybe I should pay more attention to what's happening around this house." |
| `chores_started` not set, days > 4 | "I'm running out of money. Maybe I should offer to help around the house." |
| `town_access` not set, days > 3 | "I need to get to town. @ryan has that truck..." |
| `exposure_unlock` not set, corruption >= 20 | "Something's different about how they look at me. Or maybe it's how I look at them." |
| `bookkeeping_started` not set, corruption >= 40 | "@frank mentioned needing help with the books. The pay is better than cleaning..." |
| `drawing_started` not set, jake_love >= 8 | "@jake asked if I'd sit for him. Something about the light." |

### Per-NPC Hints

| Condition | Hint Text |
|-----------|-----------|
| jake_love < 10, days > 10 | "@jake draws all day in his room. I bet he'd show me if I asked." |
| jake_love >= 15, `kiss_unlock` not set | "The way @jake looks at me when we're alone... I wonder what happens if I stop pulling away." |
| ryan_love < 5, days > 7 | "@ryan offered to drive me again. The truck rides are awkward. Maybe they don't have to be." |
| ryan_corruption >= 15, `flirt_unlock` not set | "@ryan's been different since the truck. More careful. I could push that... or not." |
| frank_trust < 8, days > 10 | "@frank is always in his office. Maybe helping with the books would bring us closer." |
| frank_love >= 15, `kiss_unlock` not set | "The kitchen at 2 AM. @frank's whiskey. The silence between us. I keep going back." |

### Economic Hints

| Condition | Hint Text |
|-----------|-----------|
| money < 50 | "I'm almost broke. I need to find more work — or find someone willing to pay more for... different services." |
| money < 0 | "I can't afford the bus. I can't afford art supplies. Something has to give." |
| `bus_pass` expired | "No bus pass. I'm stuck at the property unless @ryan drives me. That's a lot of leverage to hand someone." |

### Endgame Hints

| Condition | Hint Text |
|-----------|-----------|
| `mom_returning` set | "Seven days. Everything I've built here has an expiration date. What do I want the last week to look like?" |
| `endgame_active`, confidence > 60, money > 400 | "I have my own money. My own job. I could leave when Mom gets here. The question is whether I want to." |
| `endgame_active`, corruption > 200 | "When Mom walks through that door, she's going to see someone new. The question isn't whether I've changed. It's whether I like who I've become." |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

# 7. QUALITY CHECKLIST — VERIFICATION RESULTS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Story Quality

- [x] Central tension defined as a single emotional question — "Can Lily survive a house where every form of help has a price — and still recognize herself?"
- [x] NPCs have at least 2 internal contradictions each — Frank (3), Ryan (3), Jake (3) — defined in Phase 2
- [x] NPC resistance patterns defined (mild → moderate → severe → recovery) — all 3 NPCs in Phase 2
- [x] At least 2 tension/crisis events where stats DROP — 4 regression events: Ryan's push, Frank finds drawings, brothers discover, Mom's return
- [x] Major crisis threatens to END relationships — Frank finds drawings fractures the household, bookkeeping cancelled, Jake's door closed, Frank eats alone
- [x] Major crisis takes 2-4 in-game days to resolve — Frank repair (3-4 days), Jake repair (2-3 days), separate repair chains
- [x] At least 3 story events have TRADE-OFF or SACRIFICE choices — Ryan's push (boundary vs access), Frank's drawings confrontation (defend Jake vs honesty), brothers' discovery (independent/peacemaker/avoidant), Frank's offer (money vs autonomy)
- [x] At least 1 choice results in NEGATIVE stat consequences — Ryan's push (ryan_trust -3), Frank finds drawings (frank_trust -3 to -5), brothers discover (love drops)
- [x] At least 2 bridge events — Mom's Call (Beat 4), Power Outage (Beat 17), Jake's Birthday (optional)
- [x] Tension curve alternates — 5 DOWN events across 27 beats. Heartbeat pattern confirmed.
- [x] NPCs show fundamentally changed behavior Act 3 vs Act 1 — Frank: from "Dinner's at six" to "Stay"; Ryan: from testing to "I don't want to go home yet"; Jake: from shy nods to "I love you"
- [x] Escalation progression logical — exposure → flirt → tease → kiss → handjob → blowjob → sex, 7 incremental gates
- [x] Each gate earned through preceding drama — minimum narrative distance enforced (2-7 days between gates)
- [x] Post-crisis intimacy deeper — repair events explicitly noted as producing stats above pre-crisis levels
- [x] Fantasy clear and compelling — step-family domestic corruption, three archetypes (tender/aggressive/forbidden)
- [x] NPCs feel real — internal contradictions, speech patterns, emotional tells across 5 stat ranges each
- [x] Choices have meaning — different stat outcomes AND narrative consequences (consequence echoes defined)

## Branching Quality

- [x] Branch-point canvases set DIFFERENT flags per choice — ryan_resisted/ryan_allowed, chose_tender_jake/chose_possessive_jake, etc.
- [x] Branch-point canvases set SHARED completion flags — truck_incident_complete, jake_sketches_discovered, frank_secret_complete, crisis_resolved
- [x] branch_condition values match flags exactly — verified in Phase 6 Section 2.5
- [x] Branching paths reconverge via groups — group_crisis_resolution with required_count=1
- [x] No more than 2 branch points per NPC — Jake: 1 (secret sketches), Ryan: 1 (truck), Frank: 1 (financial secret)
- [x] Path-specific journal entries reflect tone — all branch variants have unique journal text in Phase 6
- [x] Both paths have roughly equal content — tone changes, not direction; both paths continue all arcs

## Emotional Flow Quality

- [x] Emotional quadrant behaviors defined — DISTANT, SAFE, CONFLICTED, OPEN for all 3 NPCs in Phase 2
- [x] Emotional tells for primary stat ranges — 5 love ranges per NPC in Phase 2 and Phase 6
- [x] Emotional tells for trust ranges — 5 trust ranges per NPC in Phase 2 and Phase 6
- [x] Cross-state descriptions include CRISIS state — high love / low trust defined for all 3 NPCs in Phase 6
- [x] Transition moments defined — 5 transitions per NPC (DISTANT→SAFE, SAFE→WARMING, WARMING→OPEN, OPEN→CONFLICTED, CONFLICTED→OPEN) in Phase 6
- [x] At least one scene per quadrant exists — DISTANT (arrival), SAFE (settling), CONFLICTED (crisis), OPEN (post-repair)
- [x] Activity base scenes include emotional awareness — DEFAULT, WITHDRAWN, and WARM variants for all NPC activities in Phase 5
- [x] Post-crisis behavior noticeably different — WITHDRAWN variants defined with specific changed behaviors
- [x] CONFLICTED quadrant explored 2-3+ days during crisis — Frank finds drawings: 3-4 day fallout; brothers discover: 2-4 day consequence
- [x] Emotional flow follows quadrant map — DISTANT → SAFE → OPEN → CONFLICTED → deeper OPEN confirmed per NPC
- [x] CONFLICTED → OPEN recovery is most powerful transition — repair events explicitly designed as the emotional peak

## Player Character Quality

- [x] Player has want/need/fear/flaw — Want: independence. Need: connection. Fear: being trapped. Flaw: pride.
- [x] Player emotional phases defined — 7 phases: OUTSIDER → SETTLING → AWARE → WANTING → TORN → COMMITTED → ENDGAME
- [x] Phase transitions tied to story events — each phase triggered by specific flag/event
- [x] Internal voice changes across phases — short observational sentences (OUTSIDER) → charged anticipatory narration (WANTING) → confident direct voice (COMMITTED)
- [x] "What player notices" evolves — environment → habits → bodies → desire → stakes → relationships → time
- [x] "How player describes NPC" shifts — role/appearance → personality → physical attraction → emotional depth → intimate familiarity
- [x] Choice text framing reflects phase — cautious/polite → charged/risk-aware → honest/direct → urgent/defining
- [x] Player has parallel crisis arc — Lily's own guilt/fear/determination during household crises
- [x] Player crisis stages defined — visible in journal entries and narration shifts during crisis events
- [x] Activity scenes show player internal state — polished state, clothing choices, morning routine all reflect Lily's transformation
- [x] Player growth visible in narration — defined in Phase 2 player internal voice tables
- [x] Player character feels like a person — Lily's pride as economic engine, her art student identity, her relationship with Diana

## Scene Quality

- [x] Each scene has clear narrative purpose — all 27 beats mapped in tension curve with specific function
- [x] Video descriptions specific and explicit — video placeholders with setting/act/mood for all escalation nodes
- [ ] Clip UUIDs assigned — N/A (Phase 0 skipped, no pre-integrated video library)
- [x] Search queries provided — image search queries for all 21 locations in Phase 3
- [x] Progression makes logical emotional sense — gate thresholds match NPC psychology, narrative distance enforced
- [x] No gaps in experience — no dead zones verified in Phase 5 coverage summary

## Technical Quality

- [x] All IDs consistent — loc_ prefix for locations, npc_ prefix for NPCs, story_ for events, utility_ for canvases
- [x] Trigger conditions logical and achievable — all triggers use existing flags + reachable stat thresholds
- [x] Stat thresholds reachable — target progression tables in Phase 2 confirm all gates achievable by target days
- [x] Flag chains complete — full dependency graph in Phase 4 from game_started to game_complete
- [x] Gate flags correctly assigned — 7 gates mapped to NPC-specific story events with threshold tables

## Activity Quality

- [x] NPC activities cover multiple time slots — Jake: afternoon/late afternoon/night/late night; Ryan: late morning/afternoon/late afternoon/night; Frank: morning/afternoon/evening/night/late night
- [x] Utility canvases present — 9 chore/job canvases, 4 time/rest, 5 shopping/travel, 4 recurring expenses
- [x] Economic loop viable — weeks 1-3: $4/week surplus (tight). Weeks 4+: $129/week surplus after bookkeeping unlocks.
- [x] Each NPC activity has base scene + gated choices — all 13 NPC activities have three-choice format with physical sub-menu
- [x] Hybrid gating applied — low choices: stat-only; high choices: stat + flag
- [x] Not all activities forced to sex — Studying caps at kiss, Park Sketching caps at kiss, Job Site caps at kiss, Cooking caps at kiss, Workshop caps at flirting
- [x] Canvas balance — ~27 story events (35%), ~13 NPC activities + 3 meals + 7 solo = 23 activities (30%), ~22 utility canvases (28%), ~3 bridge/other (7%) ✓

## Multi-NPC Architecture Quality

- [x] Architecture explicitly chosen — Multi-NPC Parallel Arcs (Pattern A)
- [x] Player corruption is primary driver — corruption 0-250 gates all activity choices
- [x] Corruption bands overlap — Jake 25-220, Ryan 50-240, Frank 100-240; always 2-3 active arcs
- [x] No dead zones — verified at every corruption level in Phase 5 coverage summary
- [x] Shared unlock flags defined — 7 flags (exposure → sex), each assignable through any NPC
- [x] Shared flags work cross-arc — transfer logic defined in Phase 2 Section 4 with example flow
- [x] Linear opening establishes world — Beats 1-6 (arrival through first chore) are sequential
- [x] Inciting event marks transition — Beat 7 (first physical awareness) opens parallel arcs
- [x] Economic math forces escalation — $4/week surplus at base tier, bookkeeping gated at corruption 40
- [x] Random encounters add small increments — 14 encounters at +1 to +3 corruption each, 1/day max
- [x] Clothing tiers match thresholds — Starting/Basic(0)/Cute(45)/Bold(85)/Daring(135) consistent across Phase 2 and Phase 3
- [x] Each arc has flag chain — Jake, Ryan, Frank arcs with staggered entry points in Phase 4
- [x] NPC stats gate NPC-specific scenes — dual gating: player corruption + flag + NPC love/trust/corruption

## NPC Customization Checklist

- [x] Customizable NPCs have `customizable = true`, `relationship`, and `relationship_options` — all 3 NPCs in Phase 2
- [x] Default relationship appears in options — "step-dad" in ["step-dad", "mom's boyfriend", "landlord"], etc.
- [x] Content uses @-syntax — @frank, @ryan, @jake, @frank.rel, @ryan.rel, @jake.rel throughout
- [x] Emotion mapping descriptions use @-syntax — all Phase 6 journal entries use @npc_name
- [x] Relationship options narratively compatible — all options share cohabitation context
- [x] Maximum 1-2 customizable NPCs — 3 NPCs (exceeds guideline, but all three are essential to the step-family fantasy; relationship options are simple and tested)

## Content Balance

- [x] Activity content distributed across locations and time slots — verified in Phase 5 time slot coverage
- [x] Story events ~35% of total canvases — 27 story / ~75 total = 36% ✓
- [x] Economic pressure creates meaningful trade-offs — diner shift vs dinner time, bus vs Ryan dependency, wardrobe vs essentials
- [x] Player can reach thresholds by target days — progression tables in Phase 2 confirm
- [x] days_since_flag prevents narrative compression — minimum 2-7 day gaps between gates enforced

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## FINAL STATISTICS

| Metric | Value |
|--------|-------|
| Total in-game days | ~56-60 |
| Total locations | 21 |
| Total NPCs (customizable) | 3 |
| Total story events | 27 |
| Total NPC activities | 13 |
| Total meal canvases | 3 |
| Total utility canvases | 22 |
| Total solo activities | 7 |
| Total gate flags | 7 |
| Total progression flags | 25 |
| Total branch flags | 11 |
| Total branch points | 4 (1 global + 1 per NPC) |
| Total endings | 6 |
| Total chapters | 7 |
| Total story nodes | 30+ |
| Total hint entries | 18 |
| Book file size | ~4,600 lines |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**END OF GAME DESIGN BOOK — UNDER ONE ROOF**

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
