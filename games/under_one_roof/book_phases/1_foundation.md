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
