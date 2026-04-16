# Game Design Patterns (Reference Catalog)

These are **optional patterns** — use them when they match the type of game you're building. Not every game needs every pattern. Each pattern describes WHEN to use it, HOW it works, and provides full TOML examples from "New In Town" as reference.

---

## Pattern A: Multi-Route Parallel Arcs

**Use when:** The game has multiple NPCs/storylines the player pursues simultaneously. The player should feel like they're juggling multiple threads, discovering new content as they progress.

**Don't use when:** The game follows one character's journey with a single primary relationship. Use Pattern B instead.

### How It Works

- Multiple story arcs run in parallel across overlapping stat ranges (typically corruption)
- Each arc has its own progression chain (a sequence of one-time story canvases)
- Arcs share the same "ability unlock" flags (see Rules doc, Rule 3) — this creates cross-arc consistency
- The player always has 2-3 active arcs to choose from at any corruption level
- Arcs start at staggered corruption levels so new content keeps appearing as the player progresses

> **Note:** For path-divergent arcs where the journal shows different entries based on player choice within a single NPC's story, see Pattern M: Branching Story Paths. Most multi-NPC games get enough player agency from choosing WHICH NPC to pursue.

### The Staggering Principle

This is the most important design decision in multi-route games. If all arcs start at the same corruption level, the player is overwhelmed with options. If arcs don't overlap, the player has dead zones with nothing to do. Staggering means:

- **Early game (0-40):** Linear opening. Only 1 arc active (personal discovery). Establishes the world.
- **Mid-early (40-80):** 2-3 arcs overlap. Player starts making choices about where to spend time.
- **Mid game (80-140):** Peak overlap. All major arcs are active. Player feels busy and engaged.
- **Late game (140-220):** Arcs converge toward climaxes. Content gets more intense across all arcs.

### Corruption Band Diagram (New In Town)

```
Corruption:  0    30    60    90    120   150   180   210   240
             |     |     |     |     |     |     |     |     |
Personal:    ███████████░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░░
             30 ──────── 60
Bar work:              ████████████████████████████████████████
                  65 ─────────────────────────────────── 220
Mick:             ████████████████████████████████████████████
             40 ──────────────────────────────────────── 220
Glory hole:       ██████████████████████████████████░░░░░░░░░░
             38 ─────────────────────────────── 190
Public:                          ██████████████████████████████
                           140 ────────────────────────── 220
Harlan:                    ████████████████████████████████████
                      100 ─────────────────────────────── 220
```

### Key Design Decisions

1. **Linear opening (corruption 0-35):** The first ~8 canvases are fully linear (forced sequence). This establishes the world, introduces key NPCs, and gets the player invested before the game opens up.

2. **The inciting event:** A specific story canvas marks the transition from linear to open. In New In Town, it's "The Lesson" (bar_lesson_learned) — after this, the player has a job, knows the NPCs, and can start pursuing multiple arcs.

3. **Shared unlock flags:** When the player unlocks `handjob_unlock` in the Mick arc, that same flag gates handjob options in Bar, Glory Hole, Public, and Harlan arcs. This means the player's investment in one arc directly benefits all others.

### TOML Example: Story Canvas Chain (Mick Arc)

Each canvas in the chain requires the flag from the previous canvas, plus a corruption threshold:

```toml
# Canvas 1: The Kiss (corruption 120, requires multiple flags + NPC stats)
[[canvases]]
id = "story_living_room_the_kiss"
name = "The Kiss"
is_repeatable = false

[canvases.trigger]
location = "loc_bar_living_room"
is_repeatable = false
priority = 10
npc = "npc_mick"

[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 120 },
  { type = "flag", subject = "player", flag_key = "learned_seduction", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "seen_mick_shower", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "discovered_teasing", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "caught_mick", operator = "is_true" },
  { type = "trait", subject = "npc_mick", trait_key = "love", operator = "gte", value = 20 },
  { type = "trait", subject = "npc_mick", trait_key = "trust", operator = "gte", value = 20 }
]

# ... nodes with narrative content ...
# Final node sets flag: flagEffects = [{ targetType = "player", flag = "first_kiss_mick" }]


# Canvas 2: The Couch (corruption 150, requires kiss flag + higher NPC stats)
[[canvases]]
id = "story_living_room_the_couch"
name = "The Couch"
is_repeatable = false

[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 160 },
  { type = "flag", subject = "player", flag_key = "caught_mick", operator = "is_true" },
  { type = "trait", subject = "npc_mick", trait_key = "love", operator = "gte", value = 30 },
  { type = "trait", subject = "npc_mick", trait_key = "trust", operator = "gte", value = 25 },
  { type = "trait", subject = "npc_mick", trait_key = "corruption", operator = "gte", value = 40 }
]

# ... nodes ...
# Final node sets: flagEffects = [{ targetType = "player", flag = "touched_mick" }]
# Also sets handjob_unlock which enables handjob choices in ALL arcs
```

### Corruption Milestone Table (Full Reference)

This shows every event across all arcs in New In Town, sorted by corruption level:

| Corruption | Event | Arc | Type |
|-----------|-------|-----|------|
| 30 | Restless Night | Personal | One-time |
| 38 | Glory Hole Discovery | Glory Hole | One-time |
| 40 | First Porn | Personal | One-time |
| 40 | Watch Porn | Personal | Repeatable |
| 42 | Glory Hole Learning | Glory Hole | One-time |
| 48 | Glory Hole Listening | Glory Hole | Repeatable |
| 50 | How To (seduction research) | Personal | One-time |
| 65 | Flirt for tips | Bar | Activity choice |
| 65 | Seduce customers | Bar | Activity choice |
| 65 | Flirt with Mick | Mick | Activity choice |
| 70 | Glory Hole Watching | Glory Hole | One-time |
| 90 | The Bend (teasing) | Mick | One-time |
| 90 | Show off for tips | Bar | Activity choice |
| 90 | Tease Mick | Mick | Activity choice |
| 110 | Groping | Bar | Activity choice |
| 110 | The Floorboard | Mick | One-time |
| 120 | The Kiss | Mick | One-time |
| 120 | Kiss Mick | Mick | Activity choice |
| 130 | The Towel | Mick | One-time |
| 140 | First Flash | Public | One-time |
| 140 | The Rush (repeatable flash) | Public | Repeatable |
| 150 | Dirty Talk | Public | One-time |
| 150 | The Couch (Mick handjob) | Mick | One-time |
| 160 | Bar Handjob | Bar | Activity choice |
| 160 | Glory Hole Handjob | Glory Hole | One-time |
| 160 | Street Handjob | Public | One-time |
| 160 | Rush Handjob | Public | Activity choice |
| 190 | The Counter (Mick blowjob) | Mick | One-time |
| 190 | Glory Hole Blowjob | Glory Hole | Repeatable |
| 190 | Rush Blowjob | Public | Activity choice |
| 220 | The Room (Mick sex) | Mick | One-time |
| 220 | Bar Sex | Bar | Activity choice |
| 220 | Street Sex | Public | One-time |

Notice how at corruption 160, the player has handjob options in FOUR different arcs simultaneously. This is the payoff of shared unlock flags.

---

## Pattern B: Single-Route Linear Chain

**Use when:** The game follows one character's story with one primary arc. Good for focused, intimate narratives where the player deepens a single relationship.

**Don't use when:** You want the player to juggle multiple storylines. Use Pattern A instead.

### How It Works

- One main story chain: flag A -> flag B -> flag C -> ...
- Activities still have tiered choices (Rule 1 always applies)
- Random encounters add ambient atmosphere but don't branch the story
- NPC relationships deepen along the single path
- Economic pressure (Pattern C) can still drive the narrative forward

> **Note:** Single-NPC games are the best candidates for Pattern M: Branching Story Paths — the player commits to one NPC but can define HOW they pursue them.

### Key Difference from Multi-Route

No cross-arc flag sharing needed. Unlock flags can be arc-specific since there's only one arc. The tiered activity system still applies — the player still grinds daily activities between story beats — but there's only one story thread to follow.

### Structure Example

```
Story beats:    A → B → C → D → E → F → G → H → I → J
                |   |   |   |   |   |   |   |   |   |
Activities:     [grinding between each beat with tiered choices]
Random enc:     [ambient atmosphere scattered throughout]
```

> See also Pattern N for making the NPC's name and relationship customizable by the player.

---

## Pattern C: Economic Pressure as Motivation

**Use when:** You want the player to feel organically pushed toward corruption/escalation without being forced. The game should make the player do the math themselves — never lecture them.

**Don't use when:** The game doesn't involve money or resource management. Some games can use other pressure systems (time pressure, reputation, etc.).

### How It Works

- Give the player limited starting money and recurring expenses (rent, textbooks, etc.)
- Make the "honest route" mathematically impossible (minimum wage < rent)
- Higher-corruption activities pay dramatically more
- The player does the math themselves — the game doesn't lecture

### The Math Must Be Tight

This is critical. The numbers have to be designed so that:
1. The player CANNOT survive on the base-tier activity alone
2. Each tier up makes survival noticeably easier
3. The highest tiers provide financial freedom
4. The player figures this out organically — the game never says "you should try flirting"

### TOML Example (New In Town Economy)

**Setup:**
```toml
[player]
core_traits = { corruption = 0, confidence = 0, money = 500, intelligence = 5 }

[settings.rent]
enabled = true
amount = 150          # Due every Monday
due_day = "Monday"
collector_npc = "npc_mick"
grace_periods = 1     # 1 week grace before consequences
```

**The Impossible Math:**
- Starting money: $500
- Weekly rent: $150
- Base work shift: $35/night, ~5 nights/week = $175/week
- After rent: $25/week for food, textbooks, everything else
- Textbooks cost ~$300 for the semester

The player quickly realizes: basic bar work barely covers rent. There's nothing left for food or school supplies. Something has to give.

**The Escalation Ladder:**
```
$35/shift  → Work the shift (honest)     → barely covers rent
$55/shift  → Flirt for tips              → covers rent + food
$90/shift  → Show off                    → comfortable
$120/shift → Let him grope you           → saving money
$200/shift → Handjob in the bathroom     → ahead
$300/shift → Blowjob in the bathroom     → financial freedom
$500/shift → Take him out back           → wealthy
```

The beauty: the game never tells the player to flirt. The rent bill does.

### Rent Payment Canvas Example

```toml
[[canvases.nodes]]
id = "n2"
name = "Paying Rent"
exit_block = { type = "choices", choices = [
  { text = "Pay the rent ($150)",
    targetType = "trigger",
    effects = [{ targetType = "player", trait = "money", op = "add", value = -150 }],
    flagEffects = [{ targetType = "player", flag = "rent_paid" }]
  }
] }
```

---

## Pattern D: Passive Corruption via Random Encounters

**Use when:** You want the world itself to shift the player's comfort level. The player isn't doing anything — they're just witnessing things that the environment normalizes.

**Don't use when:** The game takes place in a "normal" environment where there's nothing to witness. This pattern works best in settings where the environment itself is corrupt (bars, rough neighborhoods, etc.).

### How It Works

- Random encounter canvases trigger with a probability (e.g., 70%) when entering a location
- The player **witnesses** something — no interaction, no choice to engage
- Each encounter adds a small amount of corruption (+2-3)
- Encounters can be one-time or repeatable, limited to 1/day
- Creates the feeling that the environment is normalizing behavior

### Why Small Amounts Matter

Random encounters should add +2-3 corruption, not +10-20. The point is ambient normalization, not rapid progression. Over many days, these small increments accumulate and push the player past thresholds they wouldn't have reached through story alone. It feels organic — the player doesn't notice the slow drift until they suddenly qualify for a choice they couldn't access before.

### TOML Example: Random Encounter

```toml
[[canvases]]
id = "random_room_restless_night"
name = "Restless Night"
description = "Emma can't sleep. The sounds from downstairs filter through the floorboards."

[canvases.trigger]
location = "loc_bar_emma_room"
trigger_mode = "random"     # <-- Triggers randomly
chance = 0.7                # <-- 70% probability
is_repeatable = true        # <-- Can happen again
max_triggers_per_day = 1    # <-- But only once per day

[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "flag", subject = "player", flag_key = "bar_groped", operator = "is_true" },
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 30 }
]

[[canvases.nodes]]
id = "n1"
name = "Sounds Through the Floor"
blocks = [
  { type = "paragraph", content = "She hears it again. The muffled sounds from downstairs — laughter, clinking glasses, and something else. A rhythm she's learning to recognize." }
]
exit_block = { type = "choices", choices = [
  { text = "Pull the pillow over your head", targetType = "trigger",
    time_progression_minutes = 60,
    effects = [{ targetType = "player", trait = "corruption", op = "add", value = 2 }]  # <-- Small increment
  }
] }
```

### Good Random Encounter Ideas

- Seeing a couple in an alley while walking home
- Hearing sounds through thin walls at night
- Finding someone's forgotten phone with photos open
- Witnessing other bar workers flirting for tips
- Overhearing a conversation you weren't meant to hear
- Walking past an open door at the wrong moment

The key: the player does NOTHING. They just see/hear. The corruption comes from exposure, not action.

---

## Pattern E: NPC Trait Triangle (Love/Trust/Corruption)

**Use when:** An NPC has a relationship arc with physical escalation. The player needs to invest emotionally, build comfort, AND push boundaries — all three.

**Don't use when:** An NPC is purely functional (shopkeeper, quest giver) or only appears in one scene.

### How It Works

Three independent relationship stats per NPC:

- **Love** — emotional connection, gates romantic milestones (kissing, intimacy, pillow talk)
- **Trust** — comfort/vulnerability level, gates intimate settings (being alone together, private spaces)
- **Corruption** — willingness to cross lines, gates sexual escalation (physical acts, intensity)

Story canvases require **all three** above minimum thresholds. This prevents speed-running — you can't just max corruption without building love and trust first.

### TOML Example: NPC Definition

```toml
[[npcs]]
id = "npc_mick"
name = "Mick"
description = "47, Jolene's husband. Runs the business side of the bar..."
portrait = "mick.jpg"
core_traits = { love = 0, trust = 10, corruption = 0 }
# trust starts at 10 — he's not hostile, just reserved
flag_keys = []
```

### How Stats Are Built

Different activities build different stats:

| Activity | Builds |
|----------|--------|
| Having breakfast together | Love +2 |
| Working together in stockroom | Trust +2 |
| Flirting with him | Corruption +1, Love +1 |
| Teasing him | Corruption +2 |
| Watching TV together | Love +1, Trust +1 |

### Story Canvas Gate Example

```toml
# The Kiss requires love, trust, AND corruption from separate activities
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 120 },
  { type = "trait", subject = "npc_mick", trait_key = "love", operator = "gte", value = 20 },
  { type = "trait", subject = "npc_mick", trait_key = "trust", operator = "gte", value = 20 },
  { type = "flag", subject = "player", flag_key = "learned_seduction", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "caught_mick", operator = "is_true" }
]
```

### The Triangle Prevents Speed-Running

Without the triangle, a player could:
- Spam "tease Mick" to max corruption -> get sex scene without any emotional context
- Or spam "watch TV" to max love -> get romantic scenes without any physical chemistry

With the triangle, the player MUST:
- Build love (breakfast, TV, conversation) AND
- Build trust (working together, helping out) AND
- Build corruption (teasing, flirting, physical escalation)

All three investment types are needed. This creates a relationship that feels earned.

> Customizable NPCs (Pattern N) should use @-syntax in all content blocks that reference NPC names.

---

## Pattern F: Corruption-Tiered Clothing/Wardrobe

**Use when:** The game has a clothing system that reflects character progression. As the player's corruption increases, bolder clothing becomes available and affordable.

**Don't use when:** Clothing isn't relevant to the game's themes.

### How It Works

- **4 tiers** matching corruption milestones: Basic (0), Cute (45), Bold (85), Daring (135)
- `body_coverage` rules with conditional relaxation tied to story flags
- Wardrobe items can be added via story events (NPC gifts) using `wardrobeEffects`
- Shop location gated behind a story event (e.g., `mall_unlocked` flag)

### TOML Example: Tier Structure

**Initial wardrobe (what the player starts with):**
```toml
[[clothing]]
id = "hoodie"
name = "Hoodie"
slot = "top"
image = "images/clothing/hoodie.jpg"
initial = true     # <-- Player starts with this

[[clothing]]
id = "jeans"
name = "Jeans"
slot = "bottom"
image = "images/clothing/jeans.jpg"
initial = true

[[clothing]]
id = "sneakers"
name = "Sneakers"
slot = "shoes"
image = "images/clothing/sneakers.jpg"
initial = true

[[clothing]]
id = "basic_bra"
name = "Basic Bra"
slot = "bra"
image = "images/clothing/basic_bra.jpg"
initial = true

[[clothing]]
id = "cotton_panties"
name = "Cotton Panties"
slot = "underwear"
image = "images/clothing/cotton_panties.jpg"
initial = true
```

**Tier 1 — Basic (no corruption gate, cheap):**
```toml
[[clothing]]
id = "shop_tshirt"
name = "T-Shirt"
slot = "top"
initial = false
price = 15
# No conditions — always available in shop
```

**Tier 2 — Cute (corruption >= 45):**
```toml
[[clothing]]
id = "shop_crop_top"
name = "Crop Top"
slot = "top"
initial = false
price = 30
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 45 }
] }
```

**Tier 3 — Bold (corruption >= 85):**
```toml
[[clothing]]
id = "shop_low_cut_top"
name = "Low-Cut Top"
slot = "top"
initial = false
price = 45
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 85 }
] }
```

**Tier 4 — Daring (corruption >= 135):**
```toml
[[clothing]]
id = "shop_sheer_blouse"
name = "Sheer Blouse"
slot = "top"
initial = false
price = 60
conditions = { version = "1.0", items = [
  { type = "trait", subject = "player", trait_key = "corruption", operator = "gte", value = 135 }
] }
```

### Body Coverage Rules

The clothing system enforces coverage requirements that relax as the player progresses:

```toml
[settings.clothing_requirements]
body_coverage = true              # Player must wear clothes
always_required = ["shoes"]       # Always need shoes

# Bra required until player learns seduction
[settings.clothing_requirements.conditional.bra]
until_flag = "learned_seduction"
message = "Emma isn't ready to go braless yet."

# Underwear required until player discovers teasing
[settings.clothing_requirements.conditional.underwear]
until_flag = "discovered_teasing"
message = "Emma isn't bold enough to go without underwear yet."
```

This creates a visual progression: the player starts in a hoodie and jeans, gradually transitions to crop tops and short skirts, and eventually can wear sheer blouses and micro skirts. The clothing reflects the character's internal journey.

### Important Implementation Note

The tier thresholds in the shop UI MUST match the TOML `conditions` values exactly. If the shop says "Tier 3: Corruption 40+" but the actual TOML condition is `corruption >= 85`, players will see items they can't buy and think it's a bug.

---

## Pattern G: Location Container Architecture

**Use when:** Your game world has buildings or areas that contain multiple sub-locations (a bar with a floor, stockroom, upstairs, etc.).

### How It Works

- **Top-level locations** (City Streets, The Bar, Campus) connect to each other
- **Container locations** (`is_container = true`) hold sub-locations but aren't directly "visited"
- **Sub-locations** connect via `entry_from` (which location the player comes from) and `navigation_order` (which locations they can go to)
- Each sub-location binds to specific activities/canvases
- NPCs feel "present" at locations via the `npc` trigger field

### TOML Example: The Bar (Container with Sub-Locations)

```toml
# THE BAR — Container (not directly visited)
[[locations]]
id = "loc_the_bar"
name = "The Bar"
description = "Jolene and Mick's bar. Ground floor is the drinking room. Upstairs is where they live — and where Emma rents a room."
is_container = true               # <-- This is a container
parent = ""
entry_from = "loc_city_streets"   # <-- Reached from city streets
default_entry = "loc_bar_floor"   # <-- Player enters here by default
navigation_order = []             # <-- Empty — player navigates via sub-locations

# BAR FLOOR — First sub-location (default entry point)
[[locations]]
id = "loc_bar_floor"
name = "Bar Floor"
description = "Long bar top, eight stools, a few tables..."
is_container = false
parent = "loc_the_bar"            # <-- Belongs to The Bar
entry_from = ""                   # <-- No specific entry (it's the default)
navigation_order = ["loc_bar_stockroom", "loc_bar_upstairs", "loc_bar_bathroom"]

# STOCKROOM — Accessed from bar floor
[[locations]]
id = "loc_bar_stockroom"
name = "Stockroom"
description = "Behind the bar — cases of beer, spare kegs..."
is_container = false
parent = "loc_the_bar"
entry_from = "loc_bar_floor"      # <-- Can only enter from bar floor
navigation_order = []             # <-- Dead end — must go back

# UPSTAIRS — Hub to living quarters
[[locations]]
id = "loc_bar_upstairs"
name = "Upstairs"
description = "A narrow hallway at the top of creaking stairs..."
is_container = false
parent = "loc_the_bar"
entry_from = "loc_bar_floor"
navigation_order = ["loc_bar_living_room", "loc_bar_emma_room", "loc_bar_kitchen", "loc_bar_upstairs_bathroom"]

# EMMA'S ROOM — Leaf location
[[locations]]
id = "loc_bar_emma_room"
name = "Emma's Room"
description = "A rented room above the bar. Single bed, a desk by the window..."
is_container = false
parent = "loc_the_bar"
entry_from = "loc_bar_upstairs"   # <-- Accessed from the upstairs hallway
navigation_order = []
```

### Navigation Flow

```
City Streets → The Bar (container, enters at Bar Floor)
                 ├── Bar Floor
                 │     ├── Stockroom (dead end)
                 │     ├── Bar Bathroom (dead end)
                 │     └── Upstairs (hub)
                 │           ├── Living Room
                 │           ├── Emma's Room
                 │           ├── Kitchen
                 │           └── Bathroom
                 └── (also connects back to City Streets)
```

### Key Fields

| Field | Purpose |
|-------|---------|
| `is_container` | If true, this location holds sub-locations and isn't directly visited |
| `parent` | Which container this sub-location belongs to |
| `entry_from` | Which location the player enters this one from |
| `default_entry` | For containers: which sub-location the player enters first |
| `navigation_order` | Array of location IDs the player can navigate to from here |

---

## Pattern H: Story Arc Hints

**Use when:** The game is complex enough that players can get stuck — they don't know where to go or what to do next.

**Don't use when:** The game is purely linear and the next step is always obvious.

### How It Works

- `[[story_arc.hints.templates]]` with `missing_flag` and optional `required_flag` conditions
- Shows contextual hints based on the player's current flag state
- Tells the player WHERE to go and WHEN (location + time window)
- Hints appear when the player has been "stuck" for a configurable threshold

### The Logic

A hint shows when:
- `missing_flag` is NOT yet set (this is what the player hasn't done yet)
- `required_flag` IS set (this ensures the hint only shows when the player is ready)
- The player has been idle for `stuck_threshold_minutes`

### TOML Example

```toml
[story_arc.hints]
stuck_threshold_minutes = 30     # Show hints after 30 minutes of no progress
hint_style = "observation"       # Hints are phrased as character observations

# Early game — points player to their room
[[story_arc.hints.templates]]
text = "It's getting late. Head back to your room — you've had a long day."
[story_arc.hints.templates.condition]
missing_flag = "first_night_complete"

# After settling in — points to the bar
[[story_arc.hints.templates]]
text = "The bar downstairs is quiet in the morning. Might be a good time to go down."
[story_arc.hints.templates.condition]
missing_flag = "met_mick"

# After meeting Mick — points to campus
[[story_arc.hints.templates]]
text = "College starts soon. You should head toward campus."
[story_arc.hints.templates.condition]
missing_flag = "campus_started"

# After campus — points to job hunting
[[story_arc.hints.templates]]
text = "Normal jobs aren't cutting it. Maybe there's work closer to home — like right downstairs."
[story_arc.hints.templates.condition]
missing_flag = "job_hunt_done"

# After bar lesson, before mall — uses required_flag to ensure proper sequence
[[story_arc.hints.templates]]
text = "Jolene mentioned something about your clothes. Try walking through the city streets during the day."
[story_arc.hints.templates.condition]
missing_flag = "mall_unlocked"
required_flag = "bar_lesson_learned"    # <-- Only shows AFTER bar lesson

# Mid-game relationship hints
[[story_arc.hints.templates]]
text = "The way he looked at you during that movie... maybe next time you're alone with him, you don't have to wait for the screen."
[story_arc.hints.templates.condition]
missing_flag = "first_kiss_mick"
required_flag = "discovered_teasing"

# Late-game progression
[[story_arc.hints.templates]]
text = "The bar closes late. Sometimes it's just the two of you left to clean up."
[story_arc.hints.templates.condition]
missing_flag = "gave_blowjob"
required_flag = "touched_mick"
```

### Writing Good Hints

- **Be specific about location and time**: "Head to the bar in the evening" not "Go explore"
- **Use character voice**: The hint should sound like the player character thinking, not a game manual
- **Never spoil content**: Hint at what might happen, don't describe it
- **Use required_flag to prevent premature hints**: Don't tell the player to visit the professor before they've even been to campus

---

## Pattern I: Energy Budget Design

**Use when:** You want the player to make real decisions about how to spend their day. Energy prevents "do everything" gameplay where the optimal strategy is visiting every location in order.

**Don't use when:** The game is short/linear enough that the player should experience all content without friction.

### How It Works

- Player starts with 100 energy. Sleep resets to 100.
- Every repeatable activity costs energy (5-30, proportional to intensity)
- Activities are VISIBLE when too expensive, but blocked with a cost badge — the player sees what they're missing
- Budget math: ~4-5 activities per day without rest, 6-7 with a nap
- This forces daily prioritization: "Do I spend 30 energy on the pool, or save it for wine & talk tonight?"

### Energy Cost Tiers

| Tier | Cost | Activity Type | Examples |
|------|------|---------------|----------|
| Free | 0 | Restorative/passive | Sleep, shower, phone scroll |
| Minimal | 5 | Quick actions | Journal, get ready, wander |
| Light | 10 | Brief social/meals | Breakfast, lunch, goodnight, stargazing |
| Moderate-light | 15 | Longer activities | Dinner, movie night, video games |
| Moderate | 20 | Active/emotional | Cooking together, wine & talk, wedding planning |
| Heavy | 25 | Physical labor | Chores, manual labor |
| Very heavy | 30 | Extended physical | Pool, sports, swimming |

### What's Always Free

Three categories never cost energy:
1. **Restorative**: Sleep, shower, nap — these RESTORE energy
2. **Passive time-kill**: Phone scroll, waiting — these are zero-effort filler
3. **Story events**: Non-repeatable canvases must never be blocked by energy (narrative progression can't be gated by resources)

### Energy Restoration

Use existing effects system on exit choices:

```toml
# Full sleep — reset to 100
effects = [{ targetType = "player", trait = "energy", op = "set", value = 100, clamp = true }]

# Nap — restore 20
effects = [{ targetType = "player", trait = "energy", op = "add", value = 20, clamp = true }]

# Shower — restore 5-10
effects = [{ targetType = "player", trait = "energy", op = "add", value = 10, clamp = true }]
```

### Sidebar Display

Always add an energy bar to the sidebar so the player can track their budget:

```toml
[[sidebar_items]]
type = "trait_bar"
trait = "energy"
label = "Energy"
max = 100
```

### Anti-Pattern: No Energy Costs

```toml
# BAD — Player can do everything every day. No decisions.
[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_repeatable = true
# No costs = no trade-offs = visual novel feel
```

**Reference:** Rule 10 in game_design_rules.md

---

## Pattern J: Meal Energy Restoration

**Use when:** The game has meal activities (breakfast, lunch, dinner) and an energy system. Meals should restore energy at their base tier, creating a meaningful choice between recovery and love.

**Don't use when:** The game doesn't have an energy system, or meals aren't part of the activity loop.

### How It Works

- Meal activities have **NO entry cost** (free to enter — eating shouldn't cost energy)
- **T1 choice** (the safe default) restores a small amount of energy alongside base love
- **T2+ choices** (escalation tiers) give love only, NO energy restoration
- This creates a real trade-off: eat at T1 to recover energy, or pick a higher tier for more love but burn the recovery opportunity

### The Trade-off

| Choice | Energy | Love | Strategy |
|--------|--------|------|----------|
| T1: "Have breakfast together" | +5 | +1 | Recovery: gain energy for later activities |
| T2: "Stand closer while cooking" | 0 | +2 | Invest: spend the recovery for more love |
| T3+: Higher tiers | 0 | +3-5 | Aggressive: skip recovery entirely for max love |

### Daily Impact

If the player eats all 3 meals at T1:
- Breakfast: +5 energy
- Lunch: +5 energy
- Dinner: +10 energy
- **Total: +20 energy/day** from meals alone

This extends the daily budget from ~4-5 activities to ~5-6, rewarding players who eat regularly.

### TOML Example

```toml
# Meal trigger — NO costs (free entry)
[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"
is_repeatable = true
max_triggers_per_day = 1
priority = 1
# NOTE: No costs array — meals are free

# T1 choice — restores energy + gives love
{ text = "Have breakfast together", targetType = "trigger",
  time_progression_minutes = 45,
  effects = [
    { targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true },
    { targetType = "player", trait = "energy", op = "add", value = 5, clamp = true }
  ] }

# T2 choice — love only, no energy
{ text = "Stand closer while he cooks", targetType = "node", nodeId = "breakfast.closer",
  conditions = { version = "1.0", items = [
    { type = "trait", subject = "npc_ethan", trait_key = "love", operator = "gte", value = 15 },
    { type = "flag", subject = "player", flag_key = "lingering_touch_unlock", operator = "is_true" }
  ] } }
```

### Restoration Values

| Meal | T1 Energy Restore | Reasoning |
|------|-------------------|-----------|
| Breakfast | +5 | Light meal, start of day |
| Lunch | +5 | Midday refuel |
| Dinner | +10 | Largest meal, evening recovery |

---

## Pattern K: NPC Portrait Interaction Model

**Use when:** Every game that uses repeatable NPC activities. This is the standard interaction model — players see who's available and click to interact.

### How It Works

When a player enters a location, the screen shows:
1. **Story events auto-fire first** (priority 10, non-repeatable) — unchanged
2. **Random encounters roll** (trigger_mode = "random") — unchanged
3. **NPC portraits appear** — one clickable circle per NPC with a valid repeatable canvas
4. **Solo activities** appear as text action buttons below the portraits
5. Player clicks a portrait → enters that NPC's activity canvas

### What the Player Sees

```
┌─────────────────────────────────┐
│          Kitchen                │
│                                 │
│   ┌──────┐     ┌──────┐       │
│   │ Ethan│     │ Linda│       │
│   │  (●) │     │  (●) │       │
│   │ ⚡15  │     │      │       │
│   └──────┘     └──────┘       │
│                                 │
│   [Make coffee alone]           │
│   [Check the fridge]            │
│                                 │
└─────────────────────────────────┘
```

- **Ethan's portrait** has a cost badge (⚡15) — this activity costs 15 energy
- **Linda's portrait** has no badge — this activity is free
- **Solo activities** below as text buttons

### Key Rules

1. **One portrait = one canvas** — enforced by canvas uniqueness (Rule 9)
2. **The `npc` field on the trigger** determines which portrait appears (Rule 6)
3. **Blocked activities** (not enough energy) show greyed-out portrait with cost badge — still visible, just not clickable
4. **Portrait source** comes from the `portrait` field in `[[npcs]]`
5. **Multiple interaction types** with the same NPC go INSIDE the canvas as gated tier choices, not as separate canvases

### TOML Requirements for Portraits

```toml
# NPC must have a portrait
[[npcs]]
id = "npc_ethan"
name = "Ethan"
portrait = "ethan.jpg"    # <-- Required for portrait display

# Activity must bind NPC via trigger
[canvases.trigger]
location = "loc_kitchen"
npc = "npc_ethan"         # <-- Required: binds portrait to this canvas
is_repeatable = true
costs = [{ trait = "energy", value = 15 }]
```

### Anti-Pattern: Missing NPC Binding

```toml
# BAD — Scene involves Ethan but no npc field
# Result: Shows as a solo text button, not a portrait
[canvases.trigger]
location = "loc_kitchen"
is_repeatable = true
# npc field missing!
```

**Reference:** Rules 6, 8, 9 in game_design_rules.md

---

## Pattern L: Three-Choice Activity Format (Emotional / Physical / Neutral)

**Use when:** Every NPC activity in every game. This replaces the old flat tier ladder (T1→T8) as the standard activity structure.

**Don't use when:** Solo activities (sleep, shower, journal) — these are utility, not relationship interactions.

### The Problem It Solves

The old tier ladder showed all unlocked options simultaneously. The player always picked the highest available tier. There was no decision — just optimization. "I have 90 love, so I click the sex option" isn't a choice, it's a progress bar.

### How It Works

Every NPC activity presents exactly 3 choices at its base node:

| Choice | What It Does | Always Available? |
|--------|-------------|-------------------|
| **Emotional** | Conversation content. Builds love, may increase corruption. Story depth. | Yes |
| **Physical** | Opens sub-menu of unlockable intensity options (touch → kiss → sex). | After `lingering_touch_unlock` |
| **Neutral** | Quick exit with small love gain. Safe option. | Yes |

The player chooses an APPROACH, not an intensity level.

### Base Node Group Variants

The base node shows different opening content based on relationship phase. This makes every visit feel different — the same breakfast scene plays differently after the first kiss vs after Madison arrives.

Use 3-4 group variants, checked most-specific first:
1. Phase 5: `madison_arrived` (fiancée in the house — corruption/hiding)
2. Phase 4: `first_night_complete` (fully intimate — comfortable desire)
3. Phase 3: `first_kiss_done` (physical line crossed — giddy/nervous)
4. Default: Phase 1-2 (reconnecting — tentative/nostalgic)

### Emotional Sub-Node

Also uses group variants — the conversation topic changes per phase:
- Early game: Small talk, childhood memories
- Post-kiss: "Are we going to pretend it didn't happen?"
- Post-intimacy: "What happens when I leave?"
- Post-Madison: "Does she make you happy?"

Effects: +2 love typically, may +corruption depending on activity context.

### Physical Sub-Node

A choices node with progressively unlockable options:
- Touch (always available in physical — the physical gate itself requires `lingering_touch_unlock`)
- Flirt (after `flirt_unlock`)
- Kiss (after `kiss_unlock`)
- Manual (after `manual_unlock`)
- Oral (after `oral_unlock`)
- Sex (after `sex_unlock`)

Each choice leads to the existing tier content nodes (t2, t3, t4, t6, t7, t8).

### The Unlock Satisfaction

New physical options appear as the player progresses through story events. This preserves the "I unlocked something new!" feeling from the old tier system — but moves it inside the physical sub-menu instead of cluttering the base node with 8 buttons.

### TOML Example (Breakfast — abbreviated)

```toml
# Base node with group variants
[[canvases.nodes]]
id = "base"
name = "Morning Kitchen"
blocks = [
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_done", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "He's already looking when you walk in. Looks away too fast." }
  ] },
  { type = "group", blocks = [
    { type = "paragraph", content = "Morning light. Coffee already made. Two mugs." }
  ] }
]
exit_block = { type = "choices", choices = [
  { text = "Talk with him over coffee", targetType = "node", nodeId = "activity_breakfast.emotional" },
  { text = "Get closer", targetType = "node", nodeId = "activity_breakfast.physical", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "lingering_touch_unlock", operator = "is_true" }
  ] } },
  { text = "Just eat. Easy silence.", targetType = "trigger", time_progression_minutes = 45, effects = [
    { targetType = "npc", npcId = "npc_ethan", trait = "love", op = "add", value = 1, clamp = true }
  ] }
] }
```

**Reference:** Rule 11 in game_design_rules.md

---

## Pattern M: Branching Story Paths (Arc-Level)

**Use when:** An NPC has meaningfully different story routes where the player's choice leads to different journal entries, different scenes, and different emotional outcomes — not just minor dialogue variations.

**Don't use when:** The branches only affect stat changes or dialogue tone within a single scene. Use Pattern F (within-canvas branching) for that. Also avoid in multi-NPC games where player agency already comes from choosing WHICH NPC to pursue (Pattern A) — adding per-NPC branching on top creates combinatorial explosion.

### The Three Levels of Branching

| Level | Mechanism | Journal Impact | Content Cost |
|-------|-----------|---------------|-------------|
| **Within-canvas** (Pattern F) | Both choices set SAME completion flag, different stat effects | Same journal entry for both paths | Low (2 exit nodes per branch) |
| **Conditional canvases** | Different canvases per path, same completion flag, group block variants on activities | Same journal entry, different scene content | Medium (2 canvases per branch point) |
| **Arc-level** (Pattern M) | Different flags per choice, `branch_condition` on story_arc nodes | Different journal entries per path | High (parallel story nodes + canvases) |

Use the lightest mechanism that achieves the desired player experience.

### How It Works

1. A **branch-point canvas** presents a meaningful choice (e.g., "support her decision" vs. "challenge her")
2. Each exit sets a **different flag** (e.g., `chose_support` vs `chose_challenge`) PLUS the **same completion flag** (e.g., `crossroads_complete`)
3. Downstream story arc nodes use `branch_condition` to specify which path they belong to
4. The journal only displays nodes whose `branch_condition` flag is set (or nodes with no `branch_condition`)
5. Activity group blocks check the path flag to show different narrative/media (existing system — no new feature needed)
6. After the branched segment, shared nodes (no `branch_condition`) reconverge the paths via a group with `required_count = 1`

### TOML Example

**Branch-point canvas:**

```toml
[[canvases]]
id = "elena_crossroads"
name = "The Crossroads"
[canvases.trigger]
location = "loc_park"
npc = "npc_elena"
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "flag", subject = "player", flag_key = "first_kiss_complete", operator = "is_true" }
]

[[canvases.nodes]]
id = "the_choice"
name = "The Choice"
blocks = [
  { type = "paragraph", content = "She tells you about the offer — a year abroad. Her voice is shaking." }
]
exit_block = { type = "choices", choices = [
  { text = "Support her dream", targetType = "node", nodeId = "elena_crossroads.support_exit" },
  { text = "Ask her to stay", targetType = "node", nodeId = "elena_crossroads.stay_exit" }
] }

[[canvases.nodes]]
id = "support_exit"
name = "Support"
blocks = [
  { type = "paragraph", content = "You tell her to go. Her eyes fill with tears — and gratitude." }
]
exit_block = { type = "location", text = "Watch her leave", config = { destinationType = "trigger", time_progression_minutes = 30, flagEffects = [{ targetType = "player", flag = "chose_support" }, { targetType = "player", flag = "crossroads_complete" }], effects = [{ targetType = "npc", npcId = "npc_elena", trait = "love", op = "add", value = 3 }] } }

[[canvases.nodes]]
id = "stay_exit"
name = "Stay"
blocks = [
  { type = "paragraph", content = "You ask her to stay. She searches your face for a long time." }
]
exit_block = { type = "location", text = "Wait for her answer", config = { destinationType = "trigger", time_progression_minutes = 30, flagEffects = [{ targetType = "player", flag = "chose_stay" }, { targetType = "player", flag = "crossroads_complete" }], effects = [{ targetType = "npc", npcId = "npc_elena", trait = "trust", op = "add", value = 3 }] } }
```

**Path-specific story canvases** (different canvas per path, same completion flag pattern):

```toml
# SUPPORT PATH: Elena's letters arrive
[[canvases]]
id = "support_letters_scene"
name = "Letters from Afar"
[canvases.trigger]
location = "loc_bedroom"
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "flag", subject = "player", flag_key = "chose_support", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "crossroads_complete", operator = "is_true" }
]
# ... nodes with letter-reading content, media, dialogue ...
# Exit sets: support_letters_complete

# STAY PATH: Tension builds
[[canvases]]
id = "stay_tension_scene"
name = "The Unspoken"
[canvases.trigger]
location = "loc_kitchen"
npc = "npc_elena"
is_repeatable = false
priority = 10
[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "flag", subject = "player", flag_key = "chose_stay", operator = "is_true" },
  { type = "flag", subject = "player", flag_key = "crossroads_complete", operator = "is_true" }
]
# ... nodes with tension content, different media ...
# Exit sets: stay_tension_complete
```

**Story arc nodes with `branch_condition`:**

```toml
[story_arc]
version = "1.0"

# Shared milestone (both paths see this)
[[story_arc.nodes]]
id = "crossroads"
name = "The Crossroads"
chapter = "chapter_2"
linked_canvas = "elena_crossroads"
linked_flag = "crossroads_complete"
npc = "npc_elena"
is_milestone = true
journal_entry = "She told me about the offer. I had to choose."

# SUPPORT PATH node (invisible unless chose_support is set)
[[story_arc.nodes]]
id = "support_letters"
name = "Letters from Afar"
chapter = "chapter_3"
linked_canvas = "support_letters_scene"
linked_flag = "support_letters_complete"
npc = "npc_elena"
branch_condition = "chose_support"
group = "path_resolution"
requires_nodes = ["crossroads"]
journal_entry = "Her letters arrive on Tuesdays. Each one makes me more certain."

# STAY PATH node (invisible unless chose_stay is set)
[[story_arc.nodes]]
id = "stay_tension"
name = "The Unspoken"
chapter = "chapter_3"
linked_canvas = "stay_tension_scene"
linked_flag = "stay_tension_complete"
npc = "npc_elena"
branch_condition = "chose_stay"
group = "path_resolution"
requires_nodes = ["crossroads"]
journal_entry = "She stayed. But something in her eyes changed."

# Reconvergence group — completes when ANY one path node completes
[[story_arc.groups]]
id = "path_resolution"
name = "Path Resolution"
required_count = 1

# Shared continuation (both paths see this)
[[story_arc.nodes]]
id = "reunion"
name = "What We Built"
chapter = "chapter_4"
linked_canvas = "reunion_scene"
linked_flag = "reunion_complete"
npc = "npc_elena"
requires_group = "path_resolution"
journal_entry = "Whatever road we took, it led here."
```

**Activity group block variants** (existing feature — different narrative/media per path):

```toml
# Breakfast activity shows different content based on path
[[canvases.nodes]]
id = "base"
name = "Morning Kitchen"
blocks = [
  # SUPPORT PATH: wistful, missing her
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "chose_support", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "The kitchen feels empty without her. Her mug is still in the dish rack." },
    { type = "video", props = { file = "activities/breakfast_alone_wistful.webm" } }
  ] },
  # STAY PATH: charged silence
  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "chose_stay", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "She's already at the table. Doesn't look up when you walk in." },
    { type = "video", props = { file = "activities/breakfast_tension.webm" } }
  ] },
  # Default (before branch point)
  { type = "group", blocks = [
    { type = "paragraph", content = "Morning light. Coffee already made. Two mugs." },
    { type = "video", props = { file = "activities/breakfast_default.webm" } }
  ] }
]
# Same 3 choices: Emotional / Physical / Neutral — unchanged
```

### Design Guidance

- **Branch points should happen mid-game** — the player needs to know the NPC before making a meaningful path choice
- **Each path needs 3-4 unique story nodes minimum** to feel meaningfully different
- **Paths should differ in tone and content**, not just stat rewards
- **Journal entries per path** should reflect the player's approach and emotional state
- **Emotion mappings stay the same** across paths — the traits are identical, only the journey differs
- **Activity content** uses existing group blocks for path-variant narrative and media — no new feature needed

### Anti-Pattern: Branching at Every Story Beat

```toml
# BAD — 5 branch points creates 2^5 = 32 paths. Unsustainable content.
# Use within-canvas branching (Pattern F) for minor variations.
# Reserve branch_condition for 1-2 major path-defining decisions.
```

### Anti-Pattern: Paths That Only Differ by Stats

```toml
# BAD — If gentle path gives +2 love and bold path gives +3 love,
# that's Pattern F (within-canvas branching with same flag).
# Don't use branch_condition for this — the journal entry is the same.
```

**Reference:** Rule 7 in game_design_rules.md

---

## Pattern N: Customizable NPC Names

**Use when:** NPCs have relationships to the player that players might want to personalize — step-siblings, roommates, housemates, landlords. Especially common in single-NPC intimate games.

**Don't use when:** NPC identity is tightly coupled to plot points (e.g., a character whose name is a clue), or when different relationship types would require fundamentally different narrative content (use group blocks for that).

### Schema

```toml
[[npcs]]
id = "npc_ethan"
name = "Ethan"                                          # default name
customizable = true                                      # enables customization screen
relationship = "step-brother"                            # default relationship label
relationship_options = ["step-brother", "roommate", "landlord"]  # player choices
description = "Late 20s, tall, athletic build."
portrait = "ethan.jpg"
core_traits = { love = 0, trust = 0, corruption = 0 }
flag_keys = []
```

### Content Writing with @-syntax

**Paragraph blocks** — use `@npc_short` for name, `@npc_short.rel` for relationship:
```toml
{ type = "paragraph", content = "@ethan is already in the kitchen when you come downstairs." }
{ type = "paragraph", content = "Your @ethan.rel pours you a cup of coffee without asking." }
{ type = "paragraph", content = "@ethan's hand brushes yours as he passes the mug." }
```

**Dialog blocks** — speaker name is automatic via `npcId`. Content can use `@` for other NPCs:
```toml
{ type = "dialog", content = "Morning. Sleep okay?", props = { speaker = "npc", npcId = "npc_ethan" } }
```

**Emotion mapping descriptions** — use `@` for NPC names:
```toml
[[story_arc.emotion_mappings.love.ranges]]
min = 0
max = 25
label = "Acquaintance"
description = "@ethan is polite but reserved around you"
```

### Three Levels of Content Variation

| Level | Mechanism | Example |
|-------|-----------|---------|
| **Name swap** | `@ethan` | "@ethan looks up" → "Mike looks up" |
| **Relationship label** | `@ethan.rel` | "Your @ethan.rel" → "Your roommate" |
| **Narrative divergence** | Group blocks + flags | Different paragraph content per relationship type |

For most games, name + relationship label swaps are sufficient. Use group blocks only when the relationship type fundamentally changes the scene dynamics.

### Design Guidelines

1. **Relationship options must be narratively compatible** — "Your @ethan.rel pours coffee" should make sense whether the relationship is "step-brother", "roommate", or "housemate"
2. **Avoid relationship-specific plot points in @.rel text** — don't write "Your @ethan.rel reminds you of Mom" (only works for step-brother)
3. **1-2 customizable NPCs max per game** — more creates a confusing customization screen
4. **Default name should be the canonical name** — the name used in marketing, screenshots, etc.
5. **Content budget: zero extra** — @-syntax is a find-and-replace, not content duplication

### Anti-patterns

- **Mixing hardcoded and @-syntax for the same NPC** — if an NPC is customizable, ALL references must use `@`. Even one hardcoded "Ethan" breaks immersion when the player renamed them.
- **Relationship options that require different narrative framing** — "step-brother" vs "coworker" implies completely different living situations. Use group blocks for this level of variation.

---

## Pattern O: Consequence Echo

**Use when**: Story events have meaningful branching choices and you want the player's choice to visibly affect activity content for the next 1-3 days.

**Don't use when**: Story choice differences are stat-only (use trait effects instead) or the game is too short for consequences to play out.

### The Full Cycle

A consequence echo has three parts:

1. **Story event** — branching choice sets choice-specific flags
2. **Activity base nodes** — group blocks check those flags and show different openings
3. **Natural expiry** — `days_since_flag` condition auto-expires the echo after 1-3 days

### Complete Worked Example

**PART 1: The Story Event (The Confession)**

The player discovers something about the NPC and must decide how to handle it:

```toml
[[canvases]]
id = "the_confession"
name = "The Confession"

[canvases.trigger]
location = "loc_living_room"
npc = "npc_angela"
is_active = true
is_repeatable = false
priority = 10

[canvases.trigger.conditions]
version = "1.0"
items = [
  { type = "flag", subject = "player", flag_key = "found_letter_complete", operator = "is_true" },
  { type = "trait", subject = "npc", npc_id = "npc_angela", trait_key = "trust", operator = "gte", value = 30 }
]

[[canvases.trigger.schedules]]
start_time = "19:00"
end_time = "22:00"

[[canvases.nodes]]
id = "confrontation"
name = "The Confrontation"
blocks = [
  { type = "paragraph", content = "You found the letter. You can't pretend you didn't." },
  { type = "dialog", content = "Angela. We need to talk.", props = { speaker = "player" } },
  { type = "paragraph", content = "Her face goes still. She knows what's coming." }
]
exit_block = { type = "choices", choices = [
  { text = "\"I read the letter. I understand why you kept it from me.\"",
    targetType = "node", nodeId = "the_confession.gentle_truth",
    effects = [
      { targetType = "npc", npcId = "npc_angela", trait = "trust", op = "add", value = 5 }
    ] },
  { text = "\"How long were you going to lie to me?\"",
    targetType = "node", nodeId = "the_confession.confrontation_angry",
    effects = [
      { targetType = "npc", npcId = "npc_angela", trait = "trust", op = "add", value = -3 }
    ] }
] }

# GENTLE TRUTH PATH
[[canvases.nodes]]
id = "gentle_truth"
name = "Understanding"
blocks = [
  { type = "paragraph", content = "Her shoulders drop. Relief, or maybe exhaustion." },
  { type = "dialog", content = "You're not angry?", props = { speaker = "npc", npcId = "npc_angela" } },
  { type = "paragraph", content = "You shake your head. Some things are worth more than anger." }
]
exit_block = { type = "location", text = "Sit with her", config = { destinationType = "trigger", time_progression_minutes = 45,
  flagEffects = [
    { targetType = "player", flag = "confession_complete" },
    { targetType = "player", flag = "chose_understanding" }
  ],
  effects = [
    { targetType = "npc", npcId = "npc_angela", trait = "love", op = "add", value = 5 }
  ]
} }

# ANGRY CONFRONTATION PATH
[[canvases.nodes]]
id = "confrontation_angry"
name = "Anger"
blocks = [
  { type = "paragraph", content = "She flinches like you hit her." },
  { type = "dialog", content = "I was trying to protect you.", props = { speaker = "npc", npcId = "npc_angela" } },
  { type = "dialog", content = "From what? The truth?", props = { speaker = "player" } },
  { type = "paragraph", content = "The silence that follows is the loudest thing in the room." }
]
exit_block = { type = "location", text = "Walk away", config = { destinationType = "trigger", time_progression_minutes = 45,
  flagEffects = [
    { targetType = "player", flag = "confession_complete" },
    { targetType = "player", flag = "chose_anger" }
  ],
  effects = [
    { targetType = "npc", npcId = "npc_angela", trait = "love", op = "add", value = -2 }
  ]
} }
```

**Key**: Both paths set `confession_complete` (story progresses) AND a choice-specific flag (`chose_understanding` or `chose_anger`).

---

**PART 2: The Activity Echo (Breakfast — Next Morning)**

The breakfast activity's base node checks consequence flags BEFORE phase flags:

```toml
[[canvases.nodes]]
id = "base"
name = "Morning Kitchen"
blocks = [
  # ── CONSEQUENCE ECHOES (most specific, checked first) ──

  # Understanding echo — she's grateful, open, closer
  { type = "group", conditions = { version = "1.0", logic = "AND", items = [
    { type = "flag", subject = "player", flag_key = "chose_understanding", operator = "is_true" },
    { type = "days_since_flag", subject = "player", flag_key = "chose_understanding", operator = "lte", value = 3 }
  ] }, blocks = [
    { type = "paragraph", content = "Angela is already in the kitchen. She turns when she hears you, and something in her face is different. Lighter." },
    { type = "dialog", content = "I made extra. Thought you might be hungry.", props = { speaker = "npc", npcId = "npc_angela" } },
    { type = "paragraph", content = "Her voice is soft. Not fragile — just open. Like a door she's decided to stop locking." }
  ] },

  # Anger echo — she's withdrawn, careful, walking on eggshells
  { type = "group", conditions = { version = "1.0", logic = "AND", items = [
    { type = "flag", subject = "player", flag_key = "chose_anger", operator = "is_true" },
    { type = "days_since_flag", subject = "player", flag_key = "chose_anger", operator = "lte", value = 3 }
  ] }, blocks = [
    { type = "paragraph", content = "Angela's mug is already in the sink. She ate early. A plate sits in the microwave — no note." },
    { type = "paragraph", content = "She's in the doorway when you turn around. Arms crossed. Not angry. Worse — careful." },
    { type = "dialog", content = "There's coffee.", props = { speaker = "npc", npcId = "npc_angela" } }
  ] },

  # ── PHASE VARIANTS (broader milestones, checked after echoes) ──

  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_night_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "She made your favorite. Sits closer than she used to." }
  ] },

  { type = "group", conditions = { version = "1.0", items = [
    { type = "flag", subject = "player", flag_key = "first_kiss_complete", operator = "is_true" }
  ] }, blocks = [
    { type = "paragraph", content = "She looks up when you walk in. Something has shifted between you." }
  ] },

  # Default — early relationship
  { type = "group", blocks = [
    { type = "paragraph", content = "Morning light through the kitchen window. Two mugs on the counter." }
  ] }
]
# Exit block is IDENTICAL regardless of which group block matched
exit_block = { type = "choices", choices = [
  { text = "Talk about last night", targetType = "node", nodeId = "breakfast.emotional" },
  { text = "Get closer", targetType = "node", nodeId = "breakfast.physical",
    conditions = { version = "1.0", items = [
      { type = "flag", subject = "player", flag_key = "lingering_touch_unlock", operator = "is_true" }
    ] } },
  { text = "Just grab coffee", targetType = "trigger", time_progression_minutes = 30 }
] }
```

---

**PART 3: Echo in Emotional Sub-Node Too**

The emotional sub-node can also check consequence flags for topic variation:

```toml
[[canvases.nodes]]
id = "emotional"
name = "Morning Conversation"
blocks = [
  # Understanding echo — she wants to talk about it
  { type = "group", conditions = { version = "1.0", logic = "AND", items = [
    { type = "flag", subject = "player", flag_key = "chose_understanding", operator = "is_true" },
    { type = "days_since_flag", subject = "player", flag_key = "chose_understanding", operator = "lte", value = 2 }
  ] }, blocks = [
    { type = "dialog", content = "I've been thinking about what you said. About understanding.", props = { speaker = "npc", npcId = "npc_angela" } },
    { type = "paragraph", content = "She wraps both hands around her mug. Looking at the steam, not at you." },
    { type = "dialog", content = "Nobody ever said that to me before. That they understood.", props = { speaker = "npc", npcId = "npc_angela" } }
  ] },

  # Anger echo — she's trying to repair
  { type = "group", conditions = { version = "1.0", logic = "AND", items = [
    { type = "flag", subject = "player", flag_key = "chose_anger", operator = "is_true" },
    { type = "days_since_flag", subject = "player", flag_key = "chose_anger", operator = "lte", value = 2 }
  ] }, blocks = [
    { type = "dialog", content = "I know you're still upset. I'm not going to pretend you're not.", props = { speaker = "npc", npcId = "npc_angela" } },
    { type = "paragraph", content = "She sets her mug down. Meets your eyes for the first time today." },
    { type = "dialog", content = "But I need you to know I wasn't trying to hurt you.", props = { speaker = "npc", npcId = "npc_angela" } }
  ] },

  # Default emotional conversation
  { type = "group", blocks = [
    { type = "paragraph", content = "She talks about her day. You listen." }
  ] }
]
exit_block = { type = "location", text = "Finish breakfast", config = { destinationType = "trigger", time_progression_minutes = 30,
  effects = [
    { targetType = "npc", npcId = "npc_angela", trait = "love", op = "add", value = 3 },
    { targetType = "npc", npcId = "npc_angela", trait = "trust", op = "add", value = 2 }
  ]
} }
```

### Temporal Guidance

| Echo Duration | Use When | Example |
|---------------|----------|---------|
| 1 day | Minor choice (tone/approach) | Compliment style |
| 2-3 days | Major choice (emotional fork) | Confrontation, confession |
| Permanent | Life-altering choice (use branch_condition instead) | Stay vs leave |

After the `days_since_flag` window expires, the consequence group blocks stop matching. The chain falls through to phase variants automatically. No flag clearing needed.

### Content Cost

Each consequence echo adds 1-2 paragraphs per affected activity per choice path:

| Story Choices | Affected Activities | Extra Paragraphs |
|--------------|--------------------|--------------------|
| 2 paths | 2 activities | 4-8 paragraphs |
| 2 paths | 3 activities | 6-12 paragraphs |
| 3 paths | 2 activities | 6-12 paragraphs |

This is authoring effort, not technical complexity. The TOML structure is the same group blocks designers already use for phase variants.

### Group Block Ordering Reference

```
1. Consequence echoes   (chose_X + days_since_flag <= 3)     ← most specific
2. Modifier variants    (tipsy/aroused active)                ← temporary state
3. Crisis variants      (crisis_active flag)                  ← NPC-initiated
4. Phase variants       (first_night_complete, first_kiss)    ← broad milestones
5. Default              (no conditions)                       ← always-available fallback
```

First match wins. Most specific conditions go first.
