# Under One Roof — Comprehensive Game Design Document

## 1. Core Premise

**"What if?"** — What if a 19-year-old art student, stranded by circumstance, had to live with three men she barely knows — her new step-father and his two adult sons — in an isolated rural property where every room has thin walls, one shared bathroom, and nowhere to hide?

**Title:** Under One Roof
**Genre:** Adult interactive fiction — multi-NPC parallel arc, female protagonist
**Architecture:** Multi-NPC Parallel Arcs (Pattern A)
**Tone:** Slow-burn domestic tension. Thin walls, shared spaces, late-night kitchen encounters. The house is the arena — claustrophobic, charged, inescapable.
**Timeline:** ~60 in-game days (Mom's 10-week overseas nursing contract — she returns 2 weeks early at ~day 56)
**Perspective:** Female protagonist (Lily), player-controlled

**The Hook:** Lily Chen's mom Diana just married Frank Harmon, a contractor who runs a small construction business from a rural property. Diana takes a 10-week overseas nursing contract in Dubai — the money is too good to refuse. Lily is supposed to stay in her college dorm, but the dorm floods mid-semester. Insurance won't cover alternative housing. Diana arranges for Lily to stay at Frank's property with his two sons.

Lily arrives with one suitcase to a house she's been to exactly once — the wedding.

**What makes this game different:**
- Closed ecosystem — everything happens in one house and its immediate surroundings. No escape. Proximity is constant.
- Three completely different relationship dynamics under one roof — sweet/innocent (Jake), aggressive/physical (Ryan), forbidden/authority (Frank)
- Economic pressure is organic — she's not in a strip club, she's in a house where asking for a ride or art supplies puts her in someone's debt
- Cross-NPC awareness — brothers can discover each other's involvement, Frank can discover what his sons are doing. Cascading story events.
- The shared bathroom/thin wall mechanic — random encounters write themselves
- Mom as a ticking clock — Diana's return creates late-game urgency

---

## 2. Player Character: Lily Chen

**Age:** 19
**Background:** Art student, second year. Parents divorced when she was 14. Mom remarried Frank 8 months ago. Lily attended the wedding, made small talk, went home. She doesn't know these people.

| Field | Value |
|-------|-------|
| **Want** | Independence — finish her degree, get her own place, stop depending on anyone |
| **Need** | Connection — she's been isolated since the divorce, builds walls, keeps people at distance |
| **Fear** | Being trapped — dependency on people she can't trust or control |
| **Flaw** | Pride — she'd rather suffer quietly than ask for help. She'll find her own solutions, even if those solutions push her boundaries |

**Psychology:** Lily's pride is the economic engine. She won't ask Frank for money. She won't admit she's struggling. She won't call her mom crying. This pride is what the economic pressure exploits — she'll find her *own* solutions, and each solution pulls her deeper. The game never tells her to take her clothes off. The math does.

**Sexual history:** Limited. A boyfriend in high school that lasted 4 months. She's not innocent — she's inexperienced. She knows what sex is. She's just never had it be complicated.

**Visual:** Dark hair, usually in a messy bun or ponytail. Slim build, average height. Arrives in a hoodie and jeans. Looks younger than 19. The kind of face you'd trust immediately.

---

## 3. Player Stats

```
corruption  = 0      # Primary progression driver. Gates choices across all NPC arcs.
confidence  = 10     # How she carries herself. Gates assertiveness and self-initiated escalation.
money       = 400    # Economic pressure engine. Depletes through expenses.
energy      = 100    # Daily activity budget. Resets on sleep.
fitness     = 20     # Body condition. Built through exercise. Decays without maintenance.
beauty      = 30     # Presentation. Built through grooming, makeup, skincare. Decays without maintenance.
```

### Core Stats (Drive the main loop)

| Stat | Start | Range | Clamp | Purpose |
|------|-------|-------|-------|---------|
| **corruption** | 0 | 0-250 | false | Gates which activity choices appear. Grows from activities (+2-5), random encounters (+2-3), story events (+3-8). The player's internal transformation. |
| **confidence** | 10 | 0-100 | true | Gates assertiveness choices (negotiating pay, refusing demands, standing up for herself, self-initiating physical encounters). Grows from exercise, confrontations, art achievements, wearing bold clothes. |
| **money** | 400 | unclamped | false | Depletes through monthly expenses. Replenished through household work. The impossible math forces escalation. |
| **energy** | 100 | 0-100 | true (dynamic max: 100 base, 110 at fitness 61+) | Daily budget forcing prioritization. 4-5 activities/day without rest, 6-7 with naps/meals. Resets to max on full sleep. |

### Enhancement Stats (Reward investment, not required)

| Stat | Start | Range | Clamp | Purpose |
|------|-------|-------|-------|---------|
| **fitness** | 20 | 0-100 | true | How her body looks. Built through gym, swimming, jogging, hiking, job site labor. Affects NPC reactions to her body, unlocks stamina-related physical choices, increases energy max at high levels. Decays -1 per 3 days without exercise. |
| **beauty** | 30 | 0-100 | true | How her face/hair/presentation looks. Built through grooming routines, makeup, skincare, hairstyle changes. Affects diner tips, NPC compliments, love gain bonuses at high levels. Decays -1 per 2 days without grooming. |

### How All Six Stats Interact

The first four stats drive the game. Fitness and beauty are enhancement layers — Lily can play the entire game at fitness 20 and beauty 30. But a player who invests in them gets compounding returns.

**The attractiveness picture at any moment:**
```
What NPCs see = Fitness (body) + Beauty (face/presentation) + Clothing Tier (outfit) + Confidence (posture/energy)
```

Each component contributes independently. The combinations matter:

| Combo | What It Looks Like | NPC Impact |
|-------|-------------------|------------|
| High fitness + basic clothes | Athletic body hidden under a hoodie. Ryan knows. Others don't. | Ryan-specific reactions only |
| High beauty + basic clothes | Pretty face, no effort on body or clothing. Potential visible. | Jake notices (he draws faces). Others see what she could be. |
| Bold clothes + low fitness + low beauty | Revealing outfit, average body, didn't shower. Trying too hard. | Lower effectiveness. Tips don't increase as much. NPC reactions muted. |
| High fitness + high beauty + bold clothes + high confidence | Fit body, beautiful face, bold outfit, walks like she owns the room. | Maximum NPC reaction multiplier. All stat gains get bonuses. |
| Low everything | Hoodie, bedhead, no makeup, slouching. Invisible. | Baseline interactions. No penalties, no bonuses. |

### Fitness — Detailed Mechanics

**How to build fitness:**

| Activity | Fitness Gain | Location | Energy Cost | Notes |
|----------|-------------|----------|-------------|-------|
| Gym workout | +3 | loc_gym (town) | 30 | Best source. Requires getting to town. |
| Jogging (park) | +2 | loc_park (town) | 20 | Afternoon slot. Requires town access. Better gains than property jog. |
| Jogging (property) | +1 | loc_yard | 15 | Available anytime including mornings. No transport needed. Lower gains. |
| Creek swimming | +2 | loc_creek / loc_isolated_creek | 30 | Also builds corruption (bodies + water) |
| Hiking | +2 | loc_trail (weekends) | 30 | Also builds NPC stats with whoever she hikes with |
| Job site labor | +1 | loc_workshop | 25 | Side benefit of earning money |
| Yoga in room | +1 | loc_lily_room | 10 | Solo, minimal, always available. Low energy, low reward. |

**Decay:** -1 fitness per 3 days of no exercise. If she stops going to the gym for two weeks, she loses ~5 points. Creates a maintenance loop — she has to keep investing time/energy to hold her gains.

**Fitness level effects:**

| Fitness | Label | Effects |
|---------|-------|---------|
| 0-20 | Average | No bonuses, no penalties. Default college girl body. |
| 21-40 | Toning up | Clothes fit better. +1 to confidence gains from wearing Cute+ clothing. |
| 41-60 | Noticeable | NPCs comment on her body. Ryan's dialogue shifts. Swimwear/athletic scenes get upgraded text. |
| 61-80 | Athletic | Unlocks stamina-related physical tier choices (positions, longer scenes). Energy max increases to 110. |
| 81-100 | Peak | +1 to ALL NPC corruption gains per interaction. Her body is a passive corruption source. Frank can't stop looking. |

### Beauty — Detailed Mechanics

**How to build beauty:**

| Activity | Beauty Gain | Location | Energy Cost | Notes |
|----------|------------|----------|-------------|-------|
| Morning grooming routine | +0 (prevents decay) | loc_bathroom | Free | Shower + brush hair + basic care. Minimum to not lose beauty. |
| Apply makeup | +1-2 daily buff | loc_lily_room | Free | Requires owning a makeup kit. Better kits = +2. Buff lasts until sleep. |
| Skincare routine | +1 permanent | loc_bathroom | Free | Requires owning skincare products. Once per day. Slow permanent gains. |
| New hairstyle | +3 one-time | loc_clothing_store | $30 | One-time boost per style. Can buy 2-3 different styles over the game. |
| Spa/self-care day | +2 permanent | loc_lily_room | 15 energy | Requires skincare products. Afternoon activity. Relaxation + beauty. |

**Decay:** -1 beauty per 2 days of no grooming routine. Faster decay than fitness — presentation needs daily maintenance. If she's grinding job site work and skipping showers, she looks rough. NPCs notice.

**Beauty products (one-time purchases):**

| Product | Cost | Corruption Gate | Effect |
|---------|------|----------------|--------|
| Basic makeup kit | $20 | None | Enables daily makeup (+1 beauty buff/day) |
| Skincare set | $15 | None | Enables skincare routine (+1 beauty/use) |
| Cute makeup kit (upgrade) | $35 | 45 | Daily makeup gives +2 instead of +1 |
| Premium skincare (upgrade) | $30 | 45 | Skincare routine gives +2 instead of +1 |
| Bold makeup kit (upgrade) | $45 | 85 | Dramatic looks. +2 beauty, +1 corruption when applied. NPCs react strongly. |
| Perfume | $25 | None | No beauty stat gain. Adds scent descriptions to ALL close-proximity NPC scenes. Narrative texture. |
| New hairstyle #1 | $30 | None | +3 beauty one-time. NPCs comment for 2-3 days. |
| New hairstyle #2 | $30 | 45 | +3 beauty one-time. Bolder style. Different NPC reactions. |
| New hairstyle #3 | $30 | 85 | +3 beauty one-time. Statement style. "Who are you trying to impress?" |

**Total beauty investment: ~$260** across the full game.

**Beauty level effects:**

| Beauty | Label | Effects |
|--------|-------|---------|
| 0-20 | Neglected | NPCs notice negatively. "You look tired." Frank: "Are you eating enough?" |
| 21-40 | Natural | Default. No bonuses, no penalties. She's naturally pretty but makes no effort. |
| 41-60 | Pretty | Diner tips +15%. Casual NPC compliments appear. Jake draws her face with more detail. |
| 61-80 | Beautiful | Diner tips +30%. +1 to confidence gains from social activities. Ryan stops joking — just looks. |
| 81-100 | Stunning | +1 to ALL NPC love gains per interaction. She's captivating. Frank actively avoids being in the same room — then stops avoiding. |

### Confidence — How To Build

Unlike fitness/beauty, confidence doesn't decay. It represents permanent growth in how Lily carries herself. Once gained, it stays.

| Activity | Confidence Gain | Notes |
|----------|----------------|-------|
| Gym workout | +1 | Per visit. With proper athletic wear: +2. |
| Jogging (any location) | +1 | Solo exercise builds self-reliance. |
| Wearing Cute+ clothing (first time per tier) | +2 one-time | First time she puts on each new tier — the mirror moment. |
| Wearing Bold+ clothing (daily) | +1/day | While equipped. She knows people are looking. |
| Successful confrontation (story event) | +3-5 | Standing up to Ryan, negotiating pay with Frank, refusing a demand. |
| Art achievement | +2 | Modeling milestone, positive feedback on her work. |
| Diner waitressing shift | +1 | Per shift. Earning her own money builds independence. |
| Assertive dialogue choice (story events) | +1-2 | When she picks the bold/honest option over the safe one. |
| Fitness 21+ bonus | +1 to clothing confidence | Clothes fit better → more confidence from wearing them. |
| Beauty 61+ bonus | +1 to social confidence | Compliments → more confidence from social activities. |

**Confidence level effects (reminder from core stats):**
- Gates assertiveness choices (negotiating pay, refusing demands, self-initiating physical encounters)
- Required for diner job (confidence >= 30)
- Required for Independent ending (confidence > 60)
- High confidence changes dialogue tone — Lily initiates instead of reacting

---

### The "Polished" Daily State

When Lily does her full morning routine (shower + grooming + makeup + good outfit), she enters a "polished" state for the day:

**Polished = showered today + makeup applied + clothing tier Cute or above**

Effect: +1 to ALL NPC stat gains for that day (love, trust, corruption — everything). Small but rewards the player who invests in the morning routine consistently.

This also means a player who skips grooming to save time gets to the activities faster but with lower returns. The morning routine is a mini investment decision every day.

### Morning Routine Flow

```
Early Morning (05:00-07:00):
  → Shower only (free, +10 energy, prevents beauty decay)
      She gets the full refresh but no presentation benefits.
  → Shower + Grooming (free, +5 energy, prevents decay, enables "groomed" state)
      Grooming takes time — she gets less rest but maintains her look.
  → Shower + Grooming + Makeup (free, +5 energy, prevents decay, +1-2 beauty buff, enables "polished" if Cute+ outfit)
      Full routine. Same energy as grooming alone — makeup is quick once she's already groomed.
  → Skip everything (no energy restore, beauty decays, looks rough)
      She sleeps through Early Morning. Saves the time slot but starts the day with no shower boost.

Then: Pick outfit at loc_lily_room
Then: Choose where to spend the day — with the "polished" state applied if she earned it
```

The energy difference between shower-only (+10) and grooming (+5) is the daily trade-off: 5 energy now vs the polished state bonus (+1 to all NPC stat gains) all day. Over a full day with 3-4 NPC interactions, the polished bonus earns back more than 5 energy worth of stat gains.

### Economic Impact of Beauty/Fitness

New expenses added to the economic pressure:

| Category | Total Investment | When Needed |
|----------|-----------------|-------------|
| Beauty products (basic) | $35 (makeup kit + skincare) | Weeks 2-3 |
| Beauty upgrades (cute tier) | $65 | Weeks 4-6 |
| Beauty upgrades (bold tier) | $45 | Weeks 6-8 |
| Hairstyles (up to 3) | $90 | Spread across game |
| Perfume | $25 | Anytime |
| **Total beauty** | **~$260** | |
| Gym access | Free (public gym) | — |
| Athletic clothing (for bonuses) | $40-60 | Weeks 2-4 |

Combined with clothing (~$870), existing monthly expenses (~$385/month), beauty ($260) — Lily can't afford everything. Every purchase is a trade-off:

- **Gym clothes OR makeup kit this week?** (fitness focus vs beauty focus)
- **Skincare set OR art supplies?** (looking good vs staying in school)
- **New hairstyle OR bikini?** (impressing everyone vs impressing Ryan at the creek)

These micro-decisions reflect which path the player is investing in without forcing any single choice.

---

## 4. NPC Profiles

### NPC 1: Frank Harmon — The Step-Father

**Age:** 45
**Build:** Broad shoulders, calloused hands from decades of construction work. Salt-and-pepper stubble, always slightly unshaven. Crow's feet around steady dark eyes. Smells like sawdust and black coffee. Wears flannels with rolled sleeves, work boots, jeans that fit right.
**Personality:** Controlled, responsible, quietly intense. Doesn't waste words. When he talks, people listen — not because he's loud, but because he means every syllable. A man who built his life with his hands and runs his household the same way.

**Primary Driver:** FORBIDDEN (tension)
**Secondary Driver:** DOMINANCE (submission)
**Core Traits:** `love = 0, trust = 5, corruption = 0`
- Trust starts at 5 — he's not hostile, she's his wife's daughter. Basic decency, not warmth.

**Why FORBIDDEN + DOMINANCE:** Frank is the authority figure who *tries* to keep things appropriate. He sets rules. He's careful. But Lily is in his house, walking around in increasingly less clothing, and he's been alone since his first wife left years ago. The tension builds because he fights it — every scene is loaded with what he's *not* saying. The forbidden element is the taboo itself (step-father/step-daughter). The dominance creeps in because he's used to being in charge of everything — his business, his house, his sons. When control finally breaks, it breaks in that direction.

**Key dynamic:** Frank controls resources. The car keys, the spending money, the house rules, Lily's room assignment, whether she can use the workshop for art projects. Every practical request Lily makes puts her in his orbit. He doesn't exploit this at first. But the power imbalance is always there, humming underneath every conversation.

**Resistance type:** Self-control. Frank isn't fighting attraction — he's fighting himself. He knows exactly what he's feeling and he's horrified by it. The resistance makes the eventual break devastating.

**Difficulty:** HARD — latest arc to activate (corruption 100+), requires highest investment across all three triangle stats. The payoff matches the difficulty.

*Internal thought at T1:* "She's Diana's daughter. She's Diana's daughter. Stop looking at her hands."

**Arc concept:**
- **Act 1 (corruption 0-100):** Frank is professional, fatherly, maintains distance. Sets house rules. Offers bookkeeping work. Their interactions are functional — rides to campus, dinner table small talk, handing her the Wi-Fi password. But there are micro-moments: his hand on her back guiding her through a doorway, the way he watches her leave a room.
- **Act 2 (corruption 100-180):** The walls crack. Late-night kitchen encounters become longer. The bookkeeping sessions in his office get quieter, more charged. He starts making excuses to be where she is. A business trip gets cancelled and he doesn't tell her, just shows up in the kitchen when she thought she was alone.
- **Act 3 (corruption 180-240):** Control breaks. The forbidden is fully embraced. The dominance emerges — he stops asking and starts telling. The authority dynamic inverts from protective to possessive.

**Activity hooks:**
- Cooking dinner together (kitchen, evening) — builds love
- Bookkeeping in his office (afternoon) — builds trust + corruption (proximity, closed door)
- Asking for rides/money — builds corruption (the forbidden dynamic intensifies with every dependency)
- Late-night kitchen encounters — passive corruption via random encounters
- Workshop help (morning) — builds trust (working together)

**Level 3 Branch Point (mid-game):** Lily discovers Frank's financial secret — the business is in debt, he's been hiding it from the family.
- **Path A: Confront him** → `chose_confront_frank` — adversarial-to-intimate. He's angry, then vulnerable, then grateful. Power dynamic inverts. Trust-to-love pipeline.
- **Path B: Keep his secret** → `chose_protect_frank` — conspiratorial. They share a secret. Private meetings shift from bookkeeping to real talk. Forbidden-intimacy pipeline.
- Both set `frank_secret_complete`. Both arcs continue — tone changes, not direction.

---

### NPC 2: Ryan Harmon — The Older Step-Brother

**Age:** 23
**Build:** Athletic, tanned from outdoor work. Strong jaw, cocky grin that he knows is effective. Thick arms from hauling lumber and drywall. Wears tank tops, work boots, jeans slung low. Has a faded scar on his forearm from a job site accident he tells different stories about every time.
**Personality:** Confident, teasing, physically forward. Not mean — just relentless. The kind of guy who tests every boundary once to see what happens. Laughs easily. Makes everything feel like a dare.

**Primary Driver:** LUST (arousal)
**Secondary Driver:** SEDUCTION (resistance)
**Core Traits:** `love = 0, trust = 0, corruption = 10`
- Corruption starts at 10 — he's already looking at her on day one. No pretense of innocence.

**Why LUST + SEDUCTION:** Ryan doesn't do subtlety. He sees Lily and decides she's interesting. He flirts openly, pushes boundaries, watches her reactions. He's the "you're not really my sister" guy — uses the technicality as a license. Lily's resistance is what excites him. The arc is a back-and-forth where Lily's growing corruption meets Ryan's persistent pursuit. The lust is raw and physical. The seduction is the game of wearing her down.

**Key dynamic:** Ryan controls social access. He has the truck. He knows people in town. He knows where the gym is, where the good swimming spots are, where to get cheap food. If Lily wants to go anywhere or do anything fun, Ryan is the gatekeeper. He's also the one most likely to catch her in compromising situations with others — and he'll use that leverage.

**Resistance type:** None from him — the resistance is Lily's. Ryan is ready from day one. The question is when (and whether) Lily lets him in.

**Difficulty:** MEDIUM — arc activates relatively early (corruption 50+), but Ryan requires trust-building alongside the physical escalation. He's not just a body — he's also protective in his way, and Lily has to see that before she'll let her guard down.

*Internal thought at T1:* "Dad married her mom eight months ago and now she's sleeping down the hall. This is going to be a fun summer."

**Arc concept:**
- **Act 1 (corruption 0-60):** Ryan is the loudest presence in the house. Teasing comments at breakfast, offering rides that feel like traps, finding excuses to be shirtless. He's testing. Lily's annoyed, then flustered, then aware.
- **Act 2 (corruption 60-150):** The truck rides get longer. The job site has private corners. Ryan stops being purely physical and shows something real — protects her from a creep in town, covers for her when she comes home late. The lust now has a foundation of trust.
- **Act 3 (corruption 150-240):** Full physical escalation. Ryan is hungry and direct. Gym encounters, shower timing "accidents," the truck parked somewhere remote. If he discovers her involvement with Jake or Frank, he gets competitive — not heartbroken, but determined to win.

**Activity hooks:**
- Rides in Ryan's truck (late afternoon) — builds love (hangout) + corruption (confined space, his comments)
- Job site work (late morning) — builds trust (teamwork) + corruption (physical proximity, sweat)
- Gym workouts (town, morning/afternoon) — builds corruption (bodies, locker room) + confidence (exercise)
- TV on the couch (living room, night) — builds love + escalating physical proximity
- Sharing the bathroom — random encounters (walk-ins, unlocked doors)

**Level 2 Branch Point (early-mid):** In the truck, Ryan makes a physical move. Lily can:
- **Slap his hand away** → `ryan_resisted` — Ryan shifts to verbal seduction. More careful, testing with words instead of hands. Seduction-flavored.
- **Let it happen** → `ryan_allowed` — Ryan gets bolder, more physically direct. Lust-flavored.
- Both set `truck_incident_complete`. Arc continues identically in structure — tone and approach shift. Same journal entry.

---

### NPC 3: Jake Harmon — The Younger Step-Brother

**Age:** 20
**Build:** Lean, not scrawny — just hasn't filled out yet. Shaggy brown hair that falls in his eyes. Wears glasses when he's drawing or reading, takes them off otherwise. Soft hands compared to his brother and father. Usually in a faded band t-shirt and jeans.
**Personality:** Shy, thoughtful, genuine. Draws constantly — sketchbook always within reach. Blushes when caught staring. The quiet one in a loud family. Observant in a way the others aren't — he notices what Lily's feeling before she says it.

**Primary Driver:** CORRUPTION (corruption)
**Secondary Driver:** LOVE (love)
**Core Traits:** `love = 5, trust = 5, corruption = 0`
- Love and trust both start at 5 — genuine warmth from being similar ages, sharing the "outsider" feeling in this household. Zero corruption — Jake hasn't considered her sexually yet.

**Why CORRUPTION + LOVE:** Jake is the slow-burn innocent corruption arc. He's the sweet one — and that's exactly what makes his arc devastating. He genuinely likes Lily. They bond over art, over being the quiet ones in a loud household, over late nights when neither can sleep. The corruption happens because proximity + genuine affection + hormones is an unstoppable combination. Every step feels natural, consensual, tender — which makes it hit differently than Ryan's aggressive pursuit or Frank's power dynamic.

**Key dynamic:** Jake shares a wall with Lily's bedroom. He's the one she confides in. He sees her as a person first — not a conquest (Ryan) or a complication (Frank). He's also the most emotionally vulnerable. If Lily pursues Frank or Ryan hard, Jake's arc changes tone — jealousy surfaces, hurt creeps in, desperation replaces tenderness.

**Resistance type:** Innocence. Jake doesn't resist because he's strong — he resists because he doesn't fully understand what's happening between them until it's too late. The corruption is mutual: she corrupts his innocence, and his tenderness corrupts her defenses.

**Difficulty:** EASY — earliest arc to activate (corruption 25+), lowest stat thresholds for story events. Jake is the entry point. Most players will progress his arc first, and that's by design — his arcs typically set the first unlock flags, which then enable higher-tier options with the other NPCs.

*Internal thought at T1:* "She laughs differently when it's just us. Quieter. Real. I drew her hands three times today and I don't think she noticed."

**Arc concept:**
- **Act 1 (corruption 0-50):** Bonding over art and shared quiet. Drawing sessions in his room. Studying together at the library. She notices his sketchbook has her in it — not creepy, just beautiful. First physical awareness comes through the art: "Hold still, I need to get the light on your collarbone." Accidental touches during posing.
- **Act 2 (corruption 50-130):** The art becomes the excuse. Poses get more revealing. The shared wall at night becomes charged — they knock on the wall to say goodnight. A creek swim where they see each other's bodies. First kiss is tender, guilty, mutual. "We shouldn't." "I know."
- **Act 3 (corruption 130-220):** Full emotional + physical escalation. The tenderness remains — this isn't rough or dominant, it's two people who genuinely care about each other crossing every line. Jake draws her nude. The sketchbook becomes their shared secret. If Frank or Ryan discovers the drawings, it catalyzes the major crisis.

**Activity hooks:**
- Drawing sessions (Jake's room, afternoon) — builds love + trust + eventual corruption
- Studying/homework (library or kitchen, late morning) — builds love + trust
- Creek swimming (backyard, late afternoon) — builds corruption (bodies) + love (isolation together)
- Late-night wall knocking (Lily's room, late night) — builds love (ritual) + corruption (what happens after)
- Park sketching (park, weekend afternoon) — builds love + trust (his territory)

**Level 3 Branch Point (mid-game):** After physical intimacy begins, Lily discovers Jake has been drawing her in secret for weeks — intimate poses she didn't know he saw.
- **Path A: "They're beautiful"** → `chose_tender_jake` — Jake's arc stays sweet. Trust deepens. He draws her with her consent now. The art becomes their shared language. Corruption + Love pipeline.
- **Path B: "You've been watching me?"** → `chose_possessive_jake` — Jake's arc turns darker. His shyness was hiding obsession. He's sorry, then defiant, then desperate. The sweetness has teeth. Corruption + Dominance undertone.
- Both set `jake_sketches_discovered`. Arc continues either way — emotional texture shifts dramatically.

---

## 5. NPC Customization (@-Syntax)

All NPCs are customizable. Players can rename them and adjust relationship labels at game start.

```toml
[[npcs]]
id = "npc_frank"
name = "Frank"
customizable = true
relationship = "step-dad"
relationship_options = ["step-dad", "mom's boyfriend", "landlord"]
description = "45, broad shoulders, calloused hands..."
portrait = "frank.jpg"
core_traits = { love = 0, trust = 5, corruption = 0 }
flag_keys = []

[[npcs]]
id = "npc_ryan"
name = "Ryan"
customizable = true
relationship = "step-brother"
relationship_options = ["step-brother", "housemate", "roommate"]
description = "23, athletic, tanned from outdoor work..."
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

All content blocks use `@frank`, `@ryan`, `@jake` and `@frank.rel`, `@ryan.rel`, `@jake.rel` for name/relationship references. Dialog speaker labels use `npcId` prop (automatic). Relationship options are narratively compatible — all explain shared living space.

---

## 6. Corruption Band Diagram

```
Corruption:  0    30    60    90    120   150   180   210   240
             |     |     |     |     |     |     |     |     |
Personal:    ████████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
             0 ───────── 55
             (Arrival, settling in, self-discovery, first exposure)

Jake:        ██████████████████████████████████████████████████
             25 ──────────────────────────────────────── 220
             (Earliest arc. Drawing sessions → posing → intimacy)

Household:         ████████████████████████████░░░░░░░░░░░░░░░
                40 ─────────────────────── 160
                (Chores, cooking, shared meals, domestic routines)

Ryan:              ██████████████████████████████████████████████
                50 ──────────────────────────────────────── 240
                (Truck rides, job site, gym, aggressive pursuit)

Gym/Park:              ████████████████████████████████░░░░░░░░
                  45 ────────────────────────────── 200
                  (Body awareness, exercise, outdoor encounters)

Frank:                          ████████████████████████████████
                          100 ─────────────────────────── 240
                          (Latest arc. Office, kitchen, authority breaks)

Trail/Outings:                       ██████████████████████████
                                110 ─────────────────── 220
                                (Weekend hikes, isolated creek, group dynamics)
```

**Reading the diagram:**
- **0-25:** Linear opening. Lily arrives, meets everyone, establishes routines. No choices.
- **25-55:** Jake arc starts (accidental exposure, shared spaces). Personal discovery arc (first solo corruption moments).
- **40-60:** Household activities open (chores, cooking, helping the business). Gym/park become accessible.
- **50-90:** Ryan arc heats up. He starts pushing. Player has Jake (sweet) + Ryan (aggressive) running simultaneously.
- **100+:** Frank arc activates. All three NPCs now in play. Maximum tension. Player managing three dynamics daily.
- **150+:** Arcs converge toward climaxes. Cross-NPC awareness triggers (brothers discover each other, Frank discovers sons' involvement).
- **200+:** Endgame. Mom's return countdown. Maximum intensity across all arcs.

At any given corruption level, the player always has 2-3 active arcs offering new content.

---

## 7. Gate Flag System (NPC-Independent Shared Skill Unlocks)

Every skill unlock is earnable through **ANY NPC's arc**. Each NPC has their own story scene for each milestone. Whichever NPC Lily reaches that milestone with first sets the shared flag. The flag represents Lily's internal shift — she's crossed that mental barrier — not a relationship milestone with a specific person.

### Unlock Threshold Table (Per NPC)

Each NPC can set each flag. Jake's thresholds are lowest (easiest), Ryan's are mid, Frank's are highest (hardest). This naturally nudges Jake-first for most players, but doesn't force it.

| Flag | What It Unlocks | Jake Conditions | Ryan Conditions | Frank Conditions |
|------|----------------|-----------------|-----------------|------------------|
| `exposure_unlock` | Being seen / showing body choices | corruption >= 25, jake_love >= 10 | corruption >= 40, ryan_corruption >= 10 | corruption >= 60, frank_trust >= 10 |
| `flirt_unlock` | Flirting choices with all NPCs | corruption >= 40, jake_love >= 12 | corruption >= 50, ryan_love >= 8 | corruption >= 75, frank_trust >= 15 |
| `tease_unlock` | Teasing / showing off choices | corruption >= 55, jake_love >= 15, jake_trust >= 10 | corruption >= 70, ryan_corruption >= 15 | corruption >= 90, frank_love >= 15, frank_trust >= 15 |
| `kiss_unlock` | Kissing choices with all NPCs | corruption >= 70, jake_love >= 15, jake_trust >= 15 | corruption >= 85, ryan_love >= 12, ryan_trust >= 10, ryan_corruption >= 15 | corruption >= 120, frank_love >= 20, frank_trust >= 20 |
| `handjob_unlock` | Manual/groping tier choices | corruption >= 100, jake_love >= 20, jake_trust >= 18, jake_corruption >= 15 | corruption >= 110, ryan_love >= 15, ryan_trust >= 12, ryan_corruption >= 25 | corruption >= 140, frank_love >= 25, frank_trust >= 22 |
| `blowjob_unlock` | Oral tier choices | corruption >= 140, jake_love >= 25, jake_trust >= 20, jake_corruption >= 25 | corruption >= 150, ryan_love >= 18, ryan_trust >= 15, ryan_corruption >= 30 | corruption >= 180, frank_love >= 28, frank_trust >= 25 |
| `sex_unlock` | Full sex choices | corruption >= 180, jake_love >= 30, jake_trust >= 25, jake_corruption >= 30 | corruption >= 190, ryan_love >= 22, ryan_trust >= 18, ryan_corruption >= 35 | corruption >= 210, frank_love >= 30, frank_trust >= 28 |

### How Each Milestone Feels Per NPC (Narrative Flavor)

Same act, completely different emotional texture based on NPC driver:

| Flag | Jake (CORRUPTION + LOVE) | Ryan (LUST + SEDUCTION) | Frank (FORBIDDEN + DOMINANCE) |
|------|--------------------------|-------------------------|-------------------------------|
| `exposure_unlock` | Drawing session — she lowers a strap for the pose. His pencil stops. | Creek swim — bikini comes untied. He doesn't look away. | She walks out of the shower, he's in the hallway. Both freeze. |
| `flirt_unlock` | She teases him while posing, watches him blush. Tender. | She flirts back in the truck for the first time. Playful. | She makes a comment during bookkeeping that isn't about numbers. Charged. |
| `tease_unlock` | She poses provocatively on purpose, watching his reaction. Deliberate. | She wears the bikini he bought, knows he's watching. Confident. | She bends over the desk reaching for a file, takes her time. Dangerous. |
| `kiss_unlock` | Over the sketchbook. Tender, mutual, guilty. "We shouldn't." "I know." | In the truck, parked on a dirt road. He pulls her in. She lets him. | Kitchen at 2 AM. Coffee getting cold. He says "this can't happen." Then he does it. |
| `handjob_unlock` | Drawing session turns physical. Her hand on him. Both shaking. | Truck parked somewhere remote. "You owe me." Direct. | Office, door locked. She reaches under the desk. Power. |
| `blowjob_unlock` | His room at night. Tender. She wants to. He can't believe it's happening. | Gym shower or truck. Raw, direct. He tells her what he wants. | Office. He stands. She kneels. Dominance fully realized. |
| `sex_unlock` | His bed. Eye contact. Whispered names. Love. | Against a wall, the truck bed, wherever the moment takes them. Need. | His bedroom. His rules. Door locked. Forbidden fully embraced. |

### First-Time vs Repeat Awareness (Group Block Variant)

Each NPC's milestone scene should acknowledge whether this is Lily's FIRST time doing this act or whether she's done it before with another NPC. Implemented via group block variant — one paragraph difference:

**If flag is NOT yet set (this IS her first time):**
> "She's never done this before. Her hands are shaking. The world narrows to just this moment — his breath, her heartbeat, the line she's about to cross."

**If flag IS already set (she learned from another NPC):**
> "She's done this before. But not like this. Not with him. Everything she thought she knew about this act gets rewritten in the space between their bodies."

This costs one extra group block per milestone scene per NPC. Low content cost, high emotional payoff. The player feels their choices reflected in the narrative regardless of which order they pursue NPCs.

### Cross-NPC Transfer Logic

Once a flag is set by ANY NPC's story scene, that flag enables the corresponding tier of choices in ALL NPC activities. The flag is the "permission slip" (Lily is psychologically ready). Each NPC's individual stat thresholds are still required (the relationship must have earned it).

```
Example flow:
1. Lily kisses Jake (corruption 70, jake_love 15, jake_trust 15)
   → kiss_unlock = true

2. Kiss option NOW APPEARS in Ryan's truck activity menu
   → But greyed out: requires ryan_love >= 12, ryan_trust >= 10, ryan_corruption >= 15
   → Ryan's stats are only at love 8, trust 6, corruption 12
   → Player needs 3-5 more Ryan interactions to hit thresholds

3. Kiss option also appears in Frank's bookkeeping activity menu
   → But greyed out: requires frank_love >= 20, frank_trust >= 20
   → Frank's stats are at love 10, trust 12
   → Player needs significant more Frank investment

4. Over the next week, player builds Ryan's stats through truck rides + gym
   → Ryan hits thresholds → kiss option with Ryan is now clickable
   → Player CHOOSES to click it (or doesn't)
   → Ryan's kiss scene plays — with "she's done this before" variant text
```

### Dual Gating (Unchanged)

Every gated choice requires BOTH:
- Corruption threshold + unlock flag (player readiness)
- NPC-specific love/trust/corruption thresholds (relationship earned it)

Never threshold alone. Never flag alone. Never player stats without NPC stats.

### Escalation Integrity (Unchanged)

Each gate-setting event contains a moment that makes the NEXT level feel natural. No skipping from peek to oral without earned physical contact between.

### Minimum Narrative Distance Between Gates (Unchanged)

- exposure → flirt: at least 1 tension event + 2 in-game days
- flirt → tease: at least 1 bridge event + 2 in-game days
- tease → kiss: at least 1 crisis moment + 3 in-game days
- kiss → handjob: at least the major crisis + resolution
- handjob → blowjob: at least 1 sacrifice choice + 3 in-game days
- blowjob → sex: at least the turning point + 3 in-game days

---

## 8. Economic Pressure Model

### Monthly Expenses

| Expense | Cost | Frequency |
|---------|------|-----------|
| Bus pass | $80 | Monthly (covers ALL bus travel — campus, shopping, park. Without a pass, individual trips cost $2 each way. Pass pays for itself at 20+ round trips/month.) |
| Art supplies (required for classes) | $60 | Monthly |
| Phone bill | $45 | Monthly |
| Food contribution (her share) | $50 | Weekly |
| **Total monthly burn** | **~$385** | |

**Starting money:** $400
**Mom sends:** $200/month (often late — Diana is overwhelmed overseas, transfers bounce or arrive a week late)

### Consequences of Non-Payment

| Expense | If Unpaid |
|---------|-----------|
| Bus pass | No bus travel that month. Must rely on Ryan's truck for ALL town access (increases dependency + Ryan's leverage). |
| Art supplies | Can't complete class assignments. Loses campus-related story events after 2 weeks unpaid. |
| Phone bill | Phone cut off after 1 month unpaid. Mom can't call — misses Mom story beats until reconnected. Reconnects when bill is paid. |
| Food contribution | Frank confronts her. frank_trust -3. "You need to pull your weight around here." Triggers once, then weekly reminders. |

**The impossible math:** After month 1, Lily is broke. Mom's transfer is delayed. Art supplies are due. Bus pass expires. Something has to give.

### Earning Ladder

| Activity | Pay/Session | Corruption Gate | Energy Cost | Time Slot | What It Costs Her |
|----------|------------|-----------------|-------------|-----------|-------------------|
| Clean the house | $20 | None | 25 | Late Morning | Dignity (maid in their house) |
| Bookkeeping (Frank's office) | $25 | corruption >= 40 | 20 | Afternoon | Time alone with Frank (tension). Not offered until Frank trusts her enough to be in his office — requires a few weeks of living together + some corruption progression. |
| Job site labor (with Ryan) | $40 | 40 | 25 | Late Morning | Physical proximity to Ryan |
| Art modeling — clothed (Jake's class) | $30 | 50 | 15 | Afternoon | Increasingly revealing poses |
| Diner waitressing | $45 | confidence >= 30 | 20 | Evening | Missing dinner + night activities at home |
| "Overtime" bookkeeping (Frank, door closed) | $60 | 100 | 20 | Evening | Alone with Frank, his terms |
| Art modeling — nude (Jake) | $80 | 130 | 15 | Afternoon | Full exposure, emotional intimacy |
| Ryan's "favors" | $100 | 150 | 20 | Night | Whatever Ryan asks in return |
| Frank's "arrangement" | $150 | 180 | 20 | Late Night | The authority figure takes control |

**The beauty:** The game never tells Lily to escalate. The rent does. The bus pass does. The art supplies do.

**Weeks 1-3 (cleaning only — bookkeeping not yet offered):**
Cleaning ($20) × 5 days = $100/week. Food alone is $50/week. That leaves $50/week for bus ($80/mo) + art ($60/mo) + phone ($45/mo) = $185/month = ~$46/week. Surplus: **$4/week.** One missed day of cleaning and she's in the red. Mom's $200 helps IF it arrives — when it doesn't, she's broke. She mathematically cannot afford any clothing, beauty products, or unexpected expenses.

**Weeks 4+ (bookkeeping unlocks at corruption 40):**
Cleaning + bookkeeping = $45/day = $225/week. Now she's comfortable — $175/week surplus. But to GET here, she had to pursue NPC arcs enough to reach corruption 40, meaning she's already started down the path. The economic pressure did its job during the critical early weeks.

**The escalation ladder still matters** because even with bookkeeping, higher-tier activities pay dramatically more — and each tier frees up TIME (one $150 session replaces 7 cleaning shifts) for relationship activities instead of grinding. Each tier up makes survival noticeably easier. The highest tiers provide financial freedom AND free time.

### Alternative Income (Late Game)

**Diner waitressing** unlocks at `town_access` + `confidence >= 30`. Pays $45/shift, 4-hour evening window. Provides income that doesn't require escalating with household NPCs — but costs evening time at home, meaning she misses dinner and night activities with all three NPCs. The trade-off: financial independence vs. relationship time.

---

## 9. Energy System

### Energy Cost Tiers

| Tier | Cost | Activities |
|------|------|-----------|
| **Free** | 0 | Sleep, shower, phone scroll, getting dressed, napping |
| **Minimal** | 5 | Check phone, journal, wander the property |
| **Light** | 10 | Breakfast, lunch, quick conversation, stargazing |
| **Moderate-light** | 15 | Dinner, TV on the couch, drawing session with Jake, park bench |
| **Moderate** | 20 | Cooking together, bookkeeping, studying with Jake, diner shift, Ryan's errands |
| **Heavy** | 25 | Job site work, house cleaning, yard chores |
| **Very heavy** | 30 | Creek swimming, gym workout, hiking trail |

### Energy Restoration

| Source | Restore | When |
|--------|---------|------|
| Full sleep | Set to max (100 base, 110 at fitness 61+) | Late Night → Early Morning |
| Afternoon nap | +20 | Afternoon (Lily's room) |
| Shower | +10 | Any time (bathroom, free activity) |
| Breakfast T1 | +5 | Morning |
| Lunch T1 | +5 | Afternoon |
| Dinner T1 | +10 | Evening |

### Budget Math

- **Without rest:** ~4-5 activities per day (100 energy / 20 avg cost)
- **With strategic naps + T1 meals:** ~6-7 activities per day (100 + 20 nap + 20 meals = 140 effective energy)
- **Key trade-off:** Eating at T1 (safe, recovery) vs T2+ (more love/corruption, no recovery). Taking the nap means skipping an afternoon activity slot.
- **Fitness bonus:** At fitness 61+, energy max increases to 110, allowing one extra light activity per day. Full sleep resets to 110 instead of 100.

### Rules

- Story events (is_repeatable = false) NEVER have energy costs — narrative can't be blocked by resources
- Random encounters NEVER have energy costs — they auto-fire
- Restorative activities (sleep, shower) are FREE and restore energy
- Sidebar displays energy bar at all times

---

## 10. Clothing/Wardrobe System

Clothing is both cosmetic progression AND functional gameplay. Lily can improvise with what she has for any activity (no hard gates), but proper clothing provides mechanical bonuses — confidence gains, better tips, upgraded NPC dialogue, and access to higher-tier physical choices. The wardrobe mirrors her internal transformation: one suitcase of college basics evolving into a closet that makes three men forget how to breathe.

### Core Design Principles

- **No hard gates.** Lily can always improvise — sports bra + old shorts works for the gym, underwear works for swimming. She's never locked out of an activity by clothing.
- **Soft gates with incentives.** Proper clothing gives confidence bonuses, unlocks higher-tier activity choices, increases diner tips, and changes NPC dialogue. Worth buying, not required.
- **Same categories across all tiers.** Athletic wear, swimwear, sleepwear, casual, underwear — these exist at every corruption level. What changes is how much she's willing to show.
- **Shopping as gameplay.** Each trip to town requires transport (bus $2 or Ryan's truck). If Ryan drives, he sees what she buys and comments. Bus = her secret.

### Corruption Tiers

| Tier | Corruption Gate | Style | Available In Shop When |
|------|----------------|-------|----------------------|
| **Starting** | N/A | What she packed in one suitcase | Already owned |
| **Basic** | 0 | Functional upgrades, proper versions | Always in shop |
| **Cute** | 45 | Attractive, showing skin intentionally | After corruption 45 |
| **Bold** | 85 | Provocative, dressing to be looked at | After corruption 85 |
| **Daring** | 135 | Very revealing, hiding nothing | After corruption 135 |

### Starting Wardrobe (What Lily Packed)

A 19-year-old college student packing one suitcase for a temporary stay with her step-family. She packed conservative.

```toml
# TOPS
[[clothing]]
id = "hoodie"
name = "Hoodie"
slot = "top"
tags = ["casual", "work"]
initial = true

[[clothing]]
id = "plain_tshirt_1"
name = "Plain T-Shirt"
slot = "top"
tags = ["casual", "work"]
initial = true

[[clothing]]
id = "plain_tshirt_2"
name = "Plain T-Shirt (grey)"
slot = "top"
tags = ["casual", "work"]
initial = true

[[clothing]]
id = "tank_top"
name = "Tank Top"
slot = "top"
tags = ["casual", "sleep"]
initial = true

# BOTTOMS
[[clothing]]
id = "jeans"
name = "Jeans"
slot = "bottom"
tags = ["casual", "work"]
initial = true

[[clothing]]
id = "old_shorts"
name = "Old Shorts"
slot = "bottom"
tags = ["casual", "athletic_improvised"]
initial = true

[[clothing]]
id = "sweatpants"
name = "Sweatpants"
slot = "bottom"
tags = ["casual", "sleep"]
initial = true

# SHOES
[[clothing]]
id = "sneakers"
name = "Sneakers"
slot = "shoes"
tags = ["casual", "work", "athletic"]
initial = true

[[clothing]]
id = "flip_flops"
name = "Flip Flops"
slot = "shoes"
tags = ["casual"]
initial = true

# UNDERWEAR
[[clothing]]
id = "basic_bra"
name = "Basic Bra"
slot = "bra"
tags = ["underwear"]
initial = true

[[clothing]]
id = "sports_bra"
name = "Sports Bra"
slot = "bra"
tags = ["underwear", "athletic_improvised", "swim_improvised"]
initial = true

[[clothing]]
id = "cotton_panties"
name = "Cotton Panties"
slot = "underwear"
tags = ["underwear"]
initial = true

# ONE NICE THING
[[clothing]]
id = "sundress"
name = "Sundress"
slot = "dress"
tags = ["casual", "presentable"]
initial = true
```

### What The Starting Wardrobe Covers

| Activity | What She Wears | Works? | Bonus? |
|----------|---------------|--------|--------|
| House chores, bookkeeping, campus | T-shirt + jeans | Yes | No bonus (default) |
| Job site work | T-shirt + jeans + sneakers | Yes | No bonus |
| Gym workout | Sports bra + old shorts + sneakers | **Yes (improvised)** | No confidence bonus, Ryan teases her |
| Creek swimming | Sports bra + underwear | **Yes (improvised)** | Awkward, corruption +2 first time (exposure) |
| Dinner at the table | Sundress | Yes | Small narrative flavor |
| Diner waitressing | Sundress | Yes, barely | Base tips only |
| Hiking | Shorts + t-shirt + sneakers | Yes | No bonus |
| Art modeling (clothed) | Anything | Yes | N/A |
| Late-night kitchen | Tank top + sweatpants | Yes | Default encounter text |

She can do everything from day one. She's just making do.

### Category Progression (All Tiers)

#### Athletic Wear

| Tier | Items | Price | Effect |
|------|-------|-------|--------|
| **Starting** | Sports bra + old shorts (improvised) | $0 | No confidence bonus. Ryan: "You own gym clothes or...?" |
| **Basic** | Athletic leggings + athletic top | $45 | +1 confidence/gym visit. Proper gym look. |
| **Cute** (corr 45) | Cropped athletic top + form-fitting leggings | $55 | +1 confidence/gym. Ryan notices in dialogue — stops teasing, starts staring. |
| **Bold** (corr 85) | Sports bra only + tiny shorts | $40 | +2 confidence/gym. Unlocks gym physical T3+ choices. Locker room encounters change. |
| **Daring** (corr 135) | Sheer leggings + barely-there sports bra | $60 | +2 confidence/gym, +1 corruption/gym visit. Ryan can't form sentences. |

#### Swimwear

| Tier | Items | Price | Effect |
|------|-------|-------|--------|
| **Starting** | Underwear (improvised) | $0 | Awkward. Gets see-through when wet. Corruption +2 first time. |
| **Basic** | Modest bikini or one-piece | $25 | Removes awkwardness. Enables sunbathing activity. Normal. |
| **Cute** (corr 45) | Bikini — smaller cut | $35 | +1 confidence at creek/pool. She chose this. |
| **Bold** (corr 85) | String bikini | $45 | +1 corruption/swim. Ties that could come undone. NPC reactions shift. |
| **Daring** (corr 135) | Micro bikini / thong bikini | $55 | +2 corruption/swim. Unlocks creek/pool physical T4+. Basically strings. |

#### Sleepwear / Loungewear

| Tier | Items | Price | Effect |
|------|-------|-------|--------|
| **Starting** | Tank top + sweatpants | $0 | Default late-night encounter text. |
| **Basic** | Pajama shorts + sleep tee | $20 | Legs showing. Jake notices through cracked door (random encounter variant). |
| **Cute** (corr 45) | Shorts + camisole (thin straps, braless) | $30 | Late-night kitchen encounters get upgraded text. Frank's eyes linger. |
| **Bold** (corr 85) | Silk nightgown or oversized shirt + nothing underneath | $50 | All late-night random encounters get upgraded variants. Fabric clings when she moves. |
| **Daring** (corr 135) | Sheer nightgown / lingerie as sleepwear | $60 | +1 corruption just walking around the house at night. Wearing this to the kitchen at 2 AM is a declaration. |

#### Casual / Daily Wear

| Tier | Items | Price | Effect |
|------|-------|-------|--------|
| **Starting** | Hoodie + jeans, t-shirt + shorts | $0 | No bonuses, no reactions. Invisible. |
| **Basic** | Fitted tee + nicer jeans, casual skirt | $35 | Small narrative flavor changes. She looks put-together. |
| **Cute** (corr 45) | Crop top + denim shorts, summer dress | $45 | +1 confidence. NPCs comment. First time she's showing skin on purpose. |
| **Bold** (corr 85) | Mini skirt + low-cut top, tight dress | $55 | +1 corruption when in town. Catcall random encounters trigger. The men at home stare. |
| **Daring** (corr 135) | Sheer blouse + micro skirt, braless in thin top | $65 | +2 corruption in town. NPC dialogue shifts permanently — they stop pretending not to look. |

#### Underwear

| Tier | Items | Price | Effect |
|------|-------|-------|--------|
| **Starting** | Basic bra + cotton panties | $0 | Default. |
| **Basic** | Matching bra + panty set | $20 | Subtle confidence. She cared enough to match. |
| **Cute** (corr 45) | Lace bra + lace panties | $35 | Scene text changes when clothing comes off during physical encounters. |
| **Bold** (corr 85) | Push-up bra + thong | $45 | Physical sub-menu text variants. She's thinking about who might see these. |
| **Daring** (corr 135) | Sheer bra + g-string / going braless | $50 | Dialogue during intimate scenes changes. She knows what she's doing. |

### NPC Reactions To Clothing Tiers

Each NPC reacts differently based on what Lily is currently wearing. Implemented via group block variants on activity base nodes — the opening text changes based on equipped clothing tier.

**Jake (CORRUPTION + LOVE):**
- Starting: Doesn't comment. Draws her in whatever she's wearing.
- Cute: His sketches change — more detail on her body. Blushes when caught looking.
- Bold: "Can you... put the hoodie back on? I can't concentrate." His hand shakes.
- Daring: He stops pretending to draw. The sketchbook stays closed. He just looks at her.

**Ryan (LUST + SEDUCTION):**
- Starting: "You own anything besides that hoodie?"
- Cute: "Now that's more like it." Cocky grin. Approving.
- Bold: Stops teasing. Starts staring. Truck rides get quieter. He's not joking anymore.
- Daring: "You're wearing THAT to breakfast? With Dad right there?" He's not complaining.

**Frank (FORBIDDEN + DOMINANCE):**
- Starting: Doesn't notice (or pretends not to). Professional.
- Cute: Eyes track her across the room, then snap away. Pours more coffee.
- Bold: "You should... put something on before your brothers see you." Voice tight.
- Daring: Stops telling her to cover up. The silence is louder than any words.

### Economic Impact of Wardrobe

| Tier | Cost To Fill All Categories | When Realistically Affordable |
|------|---------------------------|-------------------------------|
| Starting | $0 | Day 1 (already owned) |
| Basic upgrades | ~$145 | Weeks 2-4 (spread over shopping trips) |
| Cute tier | ~$200 | Weeks 4-6 |
| Bold tier | ~$235 | Weeks 6-8 |
| Daring tier | ~$290 | Weeks 8+ |

**Total across all tiers: ~$870.** No player buys everything. She prioritizes based on which NPC she's pursuing and which activities she does most:
- Ryan-focused player → buys bold athletic wear + string bikini early
- Jake-focused player → buys cute sleepwear + matching underwear
- Frank-focused player → buys that one dress that stops him mid-sentence

### NPC Gifting (wardrobeEffects)

Gifts have mechanical weight now — they unlock soft-gated activities and bonuses.

| NPC | Gift | When | Corruption | What It Unlocks |
|-----|------|------|-----------|-----------------|
| **Jake** | His flannel shirt | After first deep conversation | ~35 | Wearable around the house. Frank and Ryan both notice — a relationship signal. |
| **Ryan** | A bikini (Basic tier) | Before first creek swim offer | ~50 | Removes swimming awkwardness. Enables creek activity without improvising. |
| **Frank** | A nice dress (Cute tier) | After bookkeeping milestone | ~80 | Presentable tier for diner. "You can't keep wearing the same three things." |
| **Ryan** | Bold athletic set | After gym becomes regular | ~90 | "Saw this and thought of you." Gym physical T3+ choices. |
| **Frank** | Lingerie set (Bold tier) | After Frank's arc activates | ~130 | "I saw this and thought of you." Intimate scene dialogue variants. |

### Body Coverage Rules

```toml
[settings.clothing_requirements]
body_coverage = true
always_required = ["shoes"]

# Bra required until comfortable going without
[settings.clothing_requirements.conditional.bra]
until_flag = "comfortable_braless"
message = "Lily isn't ready to go braless yet."
# Flag set during: Jake drawing session where she removes bra for the pose

# Underwear required until discovered teasing
[settings.clothing_requirements.conditional.underwear]
until_flag = "discovered_teasing"
message = "Lily isn't bold enough to go without underwear yet."
# Flag set during: Ryan encounter where underwear becomes a factor
```

### Shopping Trip Mechanics

Each shopping trip requires getting to town:
- **Bus:** $2, 40 minutes each way. Nobody knows what she bought. Her secret.
- **Ryan's truck:** Free, 15 minutes. But Ryan sees every bag. Comments on it. If she buys a bikini, he wants to go to the creek that afternoon. If she buys lingerie, he asks who it's for.

The clothing store is gated behind `town_access` flag (set after first ride with Ryan).
- Shop location: `loc_clothing_store`
- Wardrobe change location: `loc_lily_room`
- Lily changes outfits at her room before leaving the house. The outfit she wears is visible to NPCs at every location she visits that day.

---

## 11. Location System

### Full Location Map

```
The Property (container) — loc_property
├── Kitchen — loc_kitchen
│   (Hub: breakfast, dinner, late-night encounters. All NPCs rotate through.)
├── Living Room — loc_living_room
│   (TV, couch, family evenings. All NPCs.)
├── Shared Bathroom — loc_bathroom
│   (Shower, getting ready. Walk-in random encounters.)
├── Frank's Office — loc_franks_office
│   (Bookkeeping, private conversations. Frank only.)
├── Lily's Room — loc_lily_room
│   (Sleep, change clothes, personal scenes, wall sounds from Jake's room.)
├── Jake's Room — loc_jakes_room
│   (Drawing, studying, late-night visits. Jake only.)
├── Hallway — loc_hallway
│   (Transit between rooms. Random encounter: Jake's cracked door.)
├── Workshop/Garage — loc_workshop
│   (Job site prep, physical labor, Frank's hidden magazines. Frank + Ryan.)
├── Backyard (container) — loc_backyard
│   ├── Yard — loc_yard
│   │   (Outdoor chores, sunbathing, garden work, morning jog around property.)
│   └── Creek — loc_creek
│       (Swimming, isolation. Any NPC can be here but usually 1-on-1.)
└── Ryan's Truck — loc_ryans_truck
    (Mobile location. Confined space. Rides to town, parked scenes. Ryan controls destination.
     Not directly navigable — entered via Ryan's activity canvases when rides trigger.)

Town (reached by bus or Ryan's truck) — loc_town
├── Campus — loc_campus
│   (Classes, art studio. Solo or Jake at library.)
│   └── Library — loc_library
│       (Studying, quiet intimacy, hidden corners. Jake.)
├── Clothing Store — loc_clothing_store
│   (Wardrobe purchases. Gated behind town_access.)
├── General Store — loc_general_store
│   (Art supplies, basics.)
├── Gym — loc_gym
│   (Exercise, locker room encounters. Ryan's territory.)
├── Park — loc_park
│   (Jogging, bench conversations, sunbathing. Jake sketches here weekends.)
└── Diner — loc_diner
    (Cheap food, waitress job opportunity. Late-game income alternative.)

Hiking Trail (Ryan's truck, weekends only) — loc_trail
├── Trail Head — loc_trail_head
│   (Start point. Group dynamics — who walks with whom.)
├── Rest Stop — loc_rest_stop
│   (Picnic area. Charged conversations with whoever Lily sat next to.)
└── Isolated Creek — loc_isolated_creek
    (Swimming spot. Privacy + nature = escalation context.)
```

### Location Connections

| From | To | How |
|------|-----|-----|
| Property | Town | Bus ($2 fare, 40 min) or Ryan's truck (15 min, free but... costs) |
| Property | Trail | Ryan's truck only (weekends) |
| Any room | Any room | Free navigation within Property container |
| Town | Property | Bus or Ryan |
| Campus | Library | Walking (sub-location) |

### Key Location Mechanics

- **Kitchen** is the social hub — the one location where ALL NPCs can be present simultaneously. Dinner is the high-tension slot.
- **Lily's Room + Jake's Room** share a wall — random encounter mechanic for sounds/knocking.
- **Frank's Office** is the only truly private location inside the house. Closed door = isolation.
- **Ryan's Truck** is a mobile location — confined space, Ryan controls the destination.
- **Creek** and **Isolated Creek** are the "away from the house" escalation spaces.
- **Gym** is Ryan's territory outside the house — Lily on his turf in a physical context.
- **Park** is neutral/Jake's territory — where Lily goes to escape the house and Jake goes to draw.

---

## 12. NPC Schedules

### Where Each NPC Is By Time Period

| Time Period | Frank | Ryan | Jake |
|------------|-------|------|------|
| **Early Morning** (05:00-07:00) | Workshop (alone) | Sleeping | Sleeping |
| **Morning** (07:00-09:00) | Kitchen (breakfast) | Kitchen or sleeping in | Kitchen (breakfast) |
| **Late Morning** (09:00-12:00) | Workshop / job site | Job site | Community college (Mon-Thu) / Home (Fri-Sun) |
| **Afternoon** (12:00-15:00) | Office (bookkeeping) | Job site or town | Jake's room (drawing) or Library |
| **Late Afternoon** (15:00-17:00) | Workshop | Town / gym / errands | Backyard / creek / park |
| **Evening** (17:00-19:00) | Kitchen (dinner) | Kitchen (dinner) or out | Kitchen (dinner) |
| **Night** (19:00-22:00) | Living room (TV) or Office | Living room or out | Jake's room |
| **Late Night** (22:00-01:00) | Kitchen (insomnia, 50% chance) | Comes home late | Jake's room (shared wall active) |

### Schedule Conflicts (Forced Choices)

These force the player to choose who to spend time with:

| Time Slot | Option A | Option B | Trade-off |
|-----------|----------|----------|-----------|
| Afternoon | Bookkeeping with Frank | Drawing with Jake | Money + Frank trust vs. Jake love |
| Late Afternoon | Gym with Ryan (town) | Creek with Jake | Ryan corruption vs. Jake corruption |
| Evening | Dinner with family | Diner waitress shift | Relationship time vs. income |
| Night | TV with Frank/Ryan | Visit Jake's room | Group dynamic vs. Jake intimacy |
| Late Night | Kitchen encounter (Frank) | Wall knocking (Jake) | Which NPC gets the private moment |

---

## 13. Time Schedule Windows

8 time periods per day. Activities bound to specific windows.

| Period | Hours | Available Activities |
|--------|-------|---------------------|
| **Early Morning** | 05:00-07:00 | Shower (+10 energy), get dressed, solo (journal, phone) |
| **Morning** | 07:00-09:00 | Breakfast (kitchen, all NPCs rotate), morning jog (yard — around the property) |
| **Late Morning** | 09:00-12:00 | Job site (Ryan/Frank), campus classes (bus), house cleaning |
| **Afternoon** | 12:00-15:00 | Lunch, bookkeeping (Frank), drawing session (Jake), art modeling, gym |
| **Late Afternoon** | 15:00-17:00 | Creek swimming, errands with Ryan, studying with Jake, park |
| **Evening** | 17:00-19:00 | Dinner (kitchen, all NPCs), diner shift (alternative) |
| **Night** | 19:00-22:00 | Living room TV, Frank's office (late), Jake's room, Ryan's return |
| **Late Night** | 22:00-01:00 | Kitchen encounters, bathroom encounters, wall sounds, sleep |

### Pacing Tools

- `days_since_flag`: Spaces story events. Example: `kiss_unlock` scene requires 3+ days after `exposure_unlock`
- `max_triggers_per_day = 1`: Most activities once per day
- `time_progression_minutes`: Each activity consumes 60-240 minutes of game time
- Weekend schedule differs: Jake home all day, Frank sometimes takes the boys hiking

---

## 14. Random Encounters (Passive Corruption)

All random encounters: player does NOTHING. She witnesses. Corruption comes from exposure, not action. Small increments (+2-3) that accumulate over many days.

### Property Random Encounters

| Location | Encounter | Corruption | Chance | Conditions | Repeatable |
|----------|-----------|------------|--------|------------|------------|
| Bathroom | Door wasn't locked — walks in on Ryan showering | +3 | 70% | Late Morning-Night | Yes (1/day) |
| Bathroom | Door wasn't locked — walks in on Jake | +2 | 50% | Late Morning-Night, corruption >= 30 | Yes (1/day) |
| Lily's Room | Hears rhythmic sounds through wall from Jake's room | +2 | 60% | Late Night, `first_week_complete` | Yes (1/day) |
| Kitchen | Frank at 2 AM, shirtless, whiskey in hand, staring out window | +2 | 50% | Late Night, corruption >= 40 | Yes (1/day) |
| Living Room | Ryan watching porn on the couch, doesn't notice Lily | +3 | 40% | Late Night, corruption >= 60 | One-time |
| Backyard | Sees Ryan skinny-dipping at the creek from her window | +3 | 30% | Late Night, corruption >= 50 | One-time |
| Workshop | Finds Frank's hidden magazines in the office drawer | +2 | N/A | Afternoon, `bookkeeping_started` | One-time |
| Hallway | Jake's door cracked, he's sketching her from memory | +2 | N/A | Night, drawing_sessions >= 3 | One-time |

### Town/Outdoor Random Encounters

| Location | Encounter | Corruption | Chance | Conditions | Repeatable |
|----------|-----------|------------|--------|------------|------------|
| Gym | Sees Ryan shirtless, sweating, lifting heavy — visceral physical awareness | +3 | 60% | Any gym visit with Ryan present | Yes (1/day) |
| Gym | Locker room — another woman walks around naked casually | +2 | 40% | Any gym visit, corruption >= 45 | Yes (1/day) |
| Park | Stranger catcalls Lily while jogging | +2 | 30% | Afternoon, corruption >= 35 | Yes (1/day) |
| Trail | Frank steadies Lily on steep section — hand on waist lingers | +2 | 70% | Any hike with Frank, corruption >= 100 | Yes (1/day) |
| Library | Jake falls asleep studying, she watches him sleep | +1 | 50% | Afternoon, Jake present | Yes (1/day) |
| Diner | Overhears waitresses talking explicitly about their boyfriends | +2 | 40% | Any diner visit, corruption >= 40 | Yes (1/day) |

---

## 15. Meal System (Pattern J)

Three meals per day. Meals are **free to enter** (no energy cost). The kitchen is the social hub.

| Meal | Time | Who's Typically Present | T1 Energy Restore | T1 Love |
|------|------|------------------------|-------------------|---------|
| **Breakfast** | 07:00-09:00 | Frank + Jake (Ryan sleeps in 50% of the time) | +5 | +1 to present NPC |
| **Lunch** | 12:00-14:00 | Often solo or with Jake (Frank in office, Ryan at job site) | +5 | +1 to present NPC |
| **Dinner** | 17:00-19:00 | Usually all three NPCs — Ryan occasionally out (~20% chance). When all three are present, it's the high-tension slot. | +10 | +1 to present NPC |

### Meal Activity Choices (Three-Choice Format)

Each meal follows the standard pattern:

| Choice | Effect | Available |
|--------|--------|-----------|
| **Eat together (neutral)** | Energy restore + small love (+1) | Always |
| **Talk over coffee/food (emotional)** | Love +2, no energy restore | Always |
| **Sit closer / brush hands (physical)** | Corruption +1-2, no energy restore | After `exposure_unlock` |

**Dinner is special:** Usually all three NPCs present (Ryan occasionally out). When all three are there, Lily picks ONE portrait to interact with. The other two are watching. This creates the tension of choosing who to engage with while the others observe — a micro-version of the whole game's dynamic.

---

## 16. Activity Format (Pattern L — Three-Choice)

Every NPC activity at every location uses the three-choice format:

| Choice | What Happens | Always Available? |
|--------|-------------|-------------------|
| **Emotional** | Conversation content. Builds love, may increase corruption. Changes with relationship phase (group variants). | Yes |
| **Physical** | Opens sub-menu of unlocked intensity options (touch → flirt → kiss → grope → oral → sex). New options appear as gate flags unlock. | After `exposure_unlock` |
| **Neutral** | Quick interaction, small love +1, conserves energy. The "safe" option. | Yes |

### Group Variants on Base Node

The same activity feels different as the relationship evolves:

**Example — Drawing Session with Jake:**
- **Default (pre-exposure):** "Jake's hunched over his sketchbook. 'Want to see what I'm working on?' He tilts the page toward you — a landscape."
- **Post-kiss:** "Jake looks up when you walk in. His pencil stops. 'I was hoping you'd come by.' The sketchbook is open to a face you recognize."
- **Post-intimacy:** "He's already cleared space for you on the bed. The sketchbook is closed. He's looking at you, not the page."

### Physical Sub-Menu Progression

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

These corruption thresholds match the LOWEST flag-setting threshold (Jake's). This ensures a player who just unlocked a flag through a story scene can immediately use it in activities. Each choice ALSO requires NPC-specific stat thresholds (love >= X, trust >= Y) — so the flag + corruption gets her in the door, but the relationship must have earned it too.

---

## 17. Story Arc Skeleton

> **Note:** This skeleton shows the MOST LIKELY progression path (Jake-first, as his thresholds are lowest). Per Section 7, any NPC can set any flag — a Ryan-focused or Frank-focused player would hit these milestones through different story scenes at different corruption levels. The beats below represent the default/expected path, not the only path. Flag-setting beats are marked with which NPC most likely triggers them, but any NPC with a matching scene can substitute.

### Act 1 — Settling In (Corruption 0-40, Days 1-7)

| Beat | Event | What Happens | Flags Set |
|------|-------|-------------|-----------|
| 1 | **Arrival** | Lily arrives with one suitcase. Awkward dinner. Shown to her room. Meets all three. | `game_started` |
| 2 | **First Morning** | Shared bathroom incident (Jake, accidental). Breakfast dynamics established. | `first_morning` |
| 3 | **The Bus Problem** | Discovers bus schedule is terrible. Ryan offers rides. First time in the truck. | `bus_problem_discovered` |
| 4 | **Mom's Call** | Diana is stressed, money transfer will be late. "Can you manage for a couple weeks?" | `mom_called` |
| 5 | **The Math** | Lily counts her money. Realizes she's in trouble. Internal monologue. | `money_crisis_realized` |
| 6 | **First Chore** | Offers to help around the house for cash. Pride swallowed. Frank accepts. | `first_week_complete`, `chores_started` |

### Act 2 — Routines Form (Corruption 40-100, Days 8-25)

| Beat | Event | What Happens | Flags Set |
|------|-------|-------------|-----------|
| 7 | **First Physical Awareness** | Most likely: Jake asks if she'll model (clothed). Or: creek swim with Ryan, shower encounter with Frank. First body-awareness moment. | `drawing_started` (if Jake), `exposure_unlock` (any NPC) |
| 8 | **Ryan's Rides Have a Cost** | "You owe me" energy in the truck. First push. | `truck_incident_complete` |
| 9 | **Frank Offers Bookkeeping** | Requires corruption >= 40 (he's observed her long enough to trust her in his office). More money than cleaning, but alone with him, door closed. | `bookkeeping_started` |
| 10 | **Creek Swim** | First real physical exposure between Lily and the brothers. Bodies in water. | `first_swim` |
| 11 | **Jake's Confession** | He's been drawing her. Shows the sketchbook willingly — her face, her hands, her collarbone. Beautiful, innocent art. (Note: This is NOT the branch-point discovery. The later branch in Section 19 is when Lily finds Jake's SECRET intimate sketches — poses she didn't know he saw. Different event, higher stakes.) | `saw_jakes_sketches` |
| 12 | **Ryan Catches Lily** | Walks in on her changing. Doesn't look away, doesn't apologize. Grins. | `ryan_caught_her` |
| 13 | **First Flirtation** | Most likely: art modeling gets charged (Jake). Or: truck flirting gets real (Ryan), bookkeeping comment crosses a line (Frank). | `modeling_started` (if Jake), `flirt_unlock` (any NPC) |
| 14 | **First Kiss** | Most likely: Jake, tender, over the sketchbook. Or: Ryan in the truck, aggressive. Or: Frank in the kitchen at 2 AM. Whoever fires first sets the flag. | `kiss_unlock` (any NPC — whichever fires first) |

### Act 3 — Lines Blur (Corruption 100-180, Days 25-45)

| Beat | Event | What Happens | Flags Set |
|------|-------|-------------|-----------|
| 15 | **Frank's Late Night** | Kitchen encounter that doesn't end with just coffee. His hand on hers. | `frank_kitchen_moment` |
| 16 | **Ryan's Ultimatum** | He knows about the modeling (or other activities). Wants his own "arrangement." | `ryan_leverage` |
| 17 | **The Power Outage** | One night, no electricity. Candles. Proximity. Three men and thin walls. | `power_outage` |
| 18 | **Frank Finds the Drawings** | Jake's intimate sketches of Lily. Confrontation or complicity? | `frank_found_drawings` |
| 19 | **Financial Crisis** | Mom's transfer bounces. Art supplies overdue. Lily is desperate. | `financial_crisis` |
| 20 | **Physical Escalation** | First handjob/groping milestone — through whichever NPC arc is most advanced. | `handjob_unlock` (any NPC) |

### Act 4 — Convergence (Corruption 180-240, Days 45-60)

| Beat | Event | What Happens | Flags Set |
|------|-------|-------------|-----------|
| 21 | **Brothers Discover Each Other** | Ryan finds out about Jake. Or Jake about Ryan. Rivalry or sharing? | `brothers_know`, main crisis branch |
| 22 | **Frank's Offer** | "I'll cover everything. Here's what I want." | `frank_offer` |
| 23 | **The Choice** | Not "pick one" — "how does Lily handle having all three?" | `crisis_resolved` |
| 24 | **Mom's Announcement** | Diana says she's coming home 2 weeks early. Countdown begins. | `mom_returning` |
| 25 | **Final Week** | Maximum escalation before the household changes forever. | `endgame_active` |
| 26 | **Resolution** | Mom arrives. What has Lily become? Based on cumulative stats. | `game_complete` |

---

## 18. Dramatic Spine

### Escalation-Tension Wave

> This wave shows the most likely progression (Jake-first path). Alternate NPC paths produce different emotional textures at each stage but follow the same structural rhythm.

```
ARRIVAL → ROUTINE → FIRST EXPOSURE (drawing/swim/shower — any NPC) →
  TENSION (Ryan pushes too hard / Frank crosses a line / Jake reveals too much) →
    REPAIR (boundary set, respected) →
      FIRST KISS (most likely Jake — tender, guilty. Could be Ryan or Frank.) →
        CRISIS (Frank discovers drawings / brothers clash / secret exposed) →
          RECOVERY ARC (2-4 days of repair events) →
            DEEPER INTIMACY (trust rebuilt stronger) →
              CHOICE POINT (brothers discover each other) →
                TURNING POINT (Lily chooses how to handle all three) →
                  CONVERGENCE (Mom's return countdown) →
                    RESOLUTION
```

### Conflict Types Used

1. **BOUNDARY BREAK** — Ryan catches Lily changing / in a compromising position. Uses what he saw as leverage. (Act 2)
2. **REVELATION** — Frank finds Jake's intimate sketches of Lily. Forces a confrontation about what's happening under his roof. (Act 3)
3. **COMPETING PULL** — Brothers discover each other's involvement. Force Lily to manage two jealous men under one roof. (Act 4)
4. **EXTERNAL THREAT** — Mom announces early return. Creates urgency countdown in the endgame. (Act 4)

### Consequence Mechanics (Stat Regression)

| Crisis Event | Stat Drop | Recovery Time |
|-------------|-----------|---------------|
| Ryan pushes too far in truck | ryan_trust -3 | 2-3 days of repair activities |
| Frank discovers drawings | frank_trust -5, jake_trust -3 | 3-4 days (separate repair per NPC) |
| Brothers discover each other | Depends on path: -3 to -5 love on one brother | 2-4 days |
| Mom announces return | All NPC corruption -2 (fear response) | Recovers through continued interaction |

**Regression rules:**
- NEVER drop stats below a previously passed gate threshold
- NEVER un-set a gate flag
- Drop primary stat OR trust, not both at once
- Maximum single-event regression: -8 primary stat or -5 trust
- After a drop, next 2-3 activities give +1 extra to compensate

---

## 19. Branch Points (Per-NPC)

### Global Crisis Branch (Act 4 — All NPCs)

When brothers discover each other's involvement with Lily:

| Path | Flag | Tone Shift | Effect |
|------|------|-----------|--------|
| **"It's none of your business"** | `chose_independent` | Lily asserts control. Both brothers chastened. Future scenes: she initiates, they follow. Dominance undertone. | All arcs continue. |
| **"Please don't fight"** | `chose_peacemaker` | Lily mediates. Guilt + tenderness. Future scenes: more emotional weight, "we shouldn't but I need you" energy. | All arcs continue. |
| **"(Say nothing, walk away)"** | `chose_avoidant` | Lily shuts down. Short-term regression on both brothers (-3 love). Frank's arc accelerates — she turns to authority when peers become complicated. | All arcs continue. |

All three set `crisis_resolved`. No arc is ever closed. Tone and journal entries change.

### Per-NPC Branch Points

| NPC | Level | Branch Point | Paths | When |
|-----|-------|-------------|-------|------|
| **Jake** | Level 3 (arc-level) | Lily discovers Jake's secret intimate sketches of her | "They're beautiful" (`chose_tender_jake`) vs "You've been watching me?" (`chose_possessive_jake`) | Mid-game, ~corruption 90 |
| **Ryan** | Level 2 (conditional canvas) | Ryan makes a move in the truck | Slap his hand (`ryan_resisted`) vs Let it happen (`ryan_allowed`) | Early-mid, ~corruption 60 |
| **Frank** | Level 3 (arc-level) | Lily discovers Frank's financial secret | Confront him (`chose_confront_frank`) vs Keep his secret (`chose_protect_frank`) | Mid-game, ~corruption 110 |

**Level 1 (within-canvas):** Every story event across all NPCs has flavor choices that set the same flag with different stat effects. Costs nothing, adds replay texture.

---

## 20. Ending Design

The game doesn't end with an exclusive choice. It ends with **Mom coming home** and the consequences of 60 days of accumulated decisions.

### Ending Variables

The ending is determined by the combination of:
- Highest-stat NPC (who did Lily invest the most in?)
- Player corruption level (how far did she go?)
- Crisis branch choice (independent / peacemaker / avoidant)
- Financial state (did she achieve independence or remain dependent?)

### Ending Types

| Ending | Conditions | Description |
|--------|-----------|-------------|
| **Jake's Girl** | Jake highest combined stats, corruption < 160 | Tender ending. Lily and Jake have something real. They plan to continue in secret after Mom returns. The sketchbook is full. |
| **Ryan's Conquest** | Ryan highest, corruption > 150 | Physical ending. Lily and Ryan have an arrangement. It's not love, but it's honest. He drives her wherever she wants. |
| **Frank's Arrangement** | Frank highest, corruption > 180 | Forbidden ending. Lily stays in the house. Mom doesn't know. Frank provides everything. The power dynamic solidifies. |
| **All Three** | No NPC more than 25 combined points ahead of others | Juggling ending. Lily managed all three. The house is her domain now. Mom comes home to a daughter she doesn't quite recognize. (Combined = love + trust + corruption per NPC. Requires deliberate time-balancing across all three arcs.) |
| **Independent** | Confidence > 60, money > 500, diner job active | Independence ending. Lily earned her own way. She has options. She can leave — or stay on her terms. |
| **Escape** | Corruption < 100, low NPC stats | Clean ending. Lily survived without crossing major lines beyond flirting. Mom comes home. Lily goes back to campus. Nothing happened. Almost. (Achievable by avoiding optional escalation, showering at 5 AM, and skipping late-night locations. Passive corruption from unavoidable encounters stays under 100 over 60 days.) |

---

## 21. Sidebar Display

```toml
[[sidebar_items]]
type = "trait_bar"
trait = "energy"
label = "Energy"
max = 100  # dynamic: adjusts to 110 at fitness 61+

[[sidebar_items]]
type = "trait_bar"
trait = "corruption"
label = "Corruption"
max = 250

[[sidebar_items]]
type = "trait_value"
trait = "money"
label = "Money"
prefix = "$"

[[sidebar_items]]
type = "trait_bar"
trait = "confidence"
label = "Confidence"
max = 100

[[sidebar_items]]
type = "trait_bar"
trait = "fitness"
label = "Fitness"
max = 100

[[sidebar_items]]
type = "trait_bar"
trait = "beauty"
label = "Beauty"
max = 100
```

---

## 22. Mechanics Summary (Quick Reference)

| Mechanic | Status | Notes |
|----------|--------|-------|
| Multi-NPC Parallel Arcs (Pattern A) | **YES** | 3 NPCs, staggered corruption bands, all arcs simultaneous |
| Player-Stat-Driven Progression | **YES** | Player corruption is primary driver, NPC stats secondary |
| NPC Trait Triangle (Pattern E) | **YES** | Love/Trust/Corruption per NPC, prevents speed-running |
| Economic Pressure (Pattern C) | **YES** | Impossible math at base tier, escalating pay ladder |
| Energy System (Pattern I) | **YES** | 100/day budget, 8 cost tiers, forces daily prioritization. Max increases to 110 at fitness 61+. |
| Meal Energy Restoration (Pattern J) | **YES** | 3 meals/day, T1 restores energy, T2+ gives love instead |
| Clothing/Wardrobe System | **YES** | 5 tiers (Starting→Basic→Cute→Bold→Daring), 5 categories (athletic/swim/sleep/casual/underwear), soft gates with bonuses, NPC reactions per tier, NPC gifting with mechanical weight |
| Fitness System | **YES** | 0-100 trait, built through exercise (gym/swim/jog/hike), decays -1/3 days. Affects body reactions, stamina choices, energy max, passive corruption bonus at 81+. |
| Beauty System | **YES** | 0-100 trait, built through grooming/makeup/skincare, decays -1/2 days. Affects tips, compliments, love gain bonus at 81+. Products purchased at store. |
| "Polished" Daily State | **YES** | Showered + makeup + Cute+ clothing = +1 to all NPC stat gains for the day |
| Gate Flag System (shared unlocks) | **YES** | 7 skill flags, earnable through ANY NPC, NPC-independent thresholds |
| Dual Gating (Rule 4) | **YES** | Every gated choice: corruption threshold + unlock flag + NPC stats |
| Time Schedules (Rule 5) | **YES** | 8 periods/day, NPC schedules, forced time conflicts |
| Random Encounters (Pattern D) | **YES** | 14+ passive corruption events across all locations |
| Location Containers (Pattern G) | **YES** | Property (container) + Town + Trail, 20+ sub-locations |
| Three-Choice Activities (Pattern L) | **YES** | Emotional/Physical/Neutral on every NPC activity |
| NPC Portraits (Pattern K) | **YES** | Click portrait to interact, energy cost badges |
| Story Arc Hints (Pattern H) | **YES** | Contextual hints phrased as Lily's observations |
| Branching Paths (Pattern M) | **YES** | 1 global branch + per-NPC branches (Level 1/2/3) |
| @-Syntax / Customizable NPCs (Pattern N) | **YES** | All 3 NPCs customizable: name + relationship label |
| Dramatic Spine | **YES** | 4-act structure, escalation-tension wave, 4 conflict types |
| Consequence Mechanics | **YES** | Stat regression during crises, 2-4 day recovery arcs |
| Morning Routine System | **YES** | Early morning choices: shower/grooming/makeup. Affects beauty maintenance and daily "polished" state. |
| Rent System | **NO** | Replaced by food contribution + monthly expenses (more organic) |
| Glory Hole / Anonymous | **NO** | Doesn't fit closed household setting |
| Public Exposure Arc | **NO** | House is the arena. Town exists but isn't the focus. |
| Multiple Arc-Level Branches | **LIMITED** | 1 per NPC max + 1 global. Content budget is already massive. |
