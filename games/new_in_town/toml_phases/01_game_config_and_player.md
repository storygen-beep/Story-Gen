# EXTRACTION: Game Config & Player Definition
# Source: Phase 1 (Foundation) + Phase 2 (Characters & Stats)

## ENGINE CONFIGURATION

```
schema = "0.2"
starting_canvas = "opening_arrival"
```

## GAME IDENTITY

```
title = "New In Town"
protagonist_name = "Emma"
protagonist_age = 23
genre = "Adult interactive fiction with video integration"
perspective = "Female protagonist"
setting = "Millfield, population ~2,000"
game_days = 65
starting_day = 1 (Monday)
starting_hour = "14:00"
starting_week = 1 (of 10)
```

## PLAYER DEFINITION

```toml
[player]
id = "player"
name = "Emma"
core_traits = { corruption = 0, confidence = 0, reputation = 80, energy = 100, money = 150 }
```

### Trait Details

| Trait | Starting | Min | Max | Clamp | Direction | Notes |
|-------|----------|-----|-----|-------|-----------|-------|
| corruption | 0 | 0 | 100 | true | One-way UP | Never decreases |
| confidence | 0 | 0 | 100 | true | Bidirectional | Can decrease from rejection |
| reputation | 80 | 0 | 100 | true | Bidirectional | Game over at 0 |
| energy | 100 | 0 | 100 | true | Bidirectional | Refills from sleep |
| money | 150 | N/A | N/A | false | Bidirectional | Can go negative (debt) |

### Player Corruption Thresholds

| Threshold | Unlocks |
|-----------|---------|
| corruption >= 10 | Phase 2 begins, can start Tom arc |
| corruption >= 20 | Bold physical moves (touching, leaning close) |
| corruption >= 40 | Can begin Mark arc (manipulation/deception) |
| corruption >= 55 | Can begin Jake arc (predatory confidence) |
| corruption >= 70 | Stockroom-level risk (extreme public-exposure content) |
| corruption >= 85 | Endgame content, full transformation |

### Reputation Threshold Events

| Rep Level | Status | Event |
|-----------|--------|-------|
| 80-100 | Golden | Buffer for mistakes |
| 60-79 | Good | Normal standing |
| < 60 | Concerning | `principal_concern_1` fires |
| < 45 | Watched | `principal_concern_2` fires, sets `school_enforcement_warned` |
| < 30 | Danger | `principal_formal_warning` fires |
| 1-14 | Critical | One more incident ends it |
| 0 | Game Over | Fired, must leave Millfield |

### Reputation Recovery Mode

When `reputation < 45`, flag `reputation_recovery_mode` activates:
- Church attendance gains: +5 (up from +3)
- Volunteering gains: +6 (up from +4)
- All reputation losses DOUBLED

## TWO-PHASE STRUCTURE

### Phase 1: The Corruption (Days 1-12)
- Emma is subject of corruption
- Jolene (female NPC, non-romantic) is catalyst
- No male NPC sexual content
- Psychological awakening through voyeurism, conversation, dares
- Ends when corruption crosses threshold

### Phase 2: The Hunt (Days 12-65)
- Emma becomes agent, targets 4 male NPCs
- NPCs have overlapping timelines
- Each NPC requires different seduction strategy
- Mirror mechanic tracks transformation (Day 1/20/40/60)

## PLAYER EMOTIONAL PHASES

| Phase | Trigger | Corruption Range |
|-------|---------|-----------------|
| INNOCENT | Arrival (Day 1) | 0-5 |
| CURIOUS | Jolene peek event (Day 6) | 5-12 |
| AWAKENED | Self-discovery (Day 10) | 12-20 |
| HUNTING | First Tom move (Day ~16) | 20-40 |
| CALCULATING | Ray/Mark begin (Day ~28) | 40-55 |
| PREDATORY | Jake arc begins (Day ~50) | 55+ |

## ECONOMIC MODEL

### Income Sources

| Source | Amount | Time Cost | Availability |
|--------|--------|-----------|-------------|
| Teaching salary | $220/week (auto, Friday) | Morning + Late Morning Mon-Fri | Always |
| Tutoring | $30/session | 1 Afternoon slot (Mon/Wed) | After `school_started` |
| Bar shifts | $50 + $10-30 tips | 1 Evening OR Night slot | After `bar_shifts_available` (Day 8+) |
| Weekend cafe | $45/shift | Morning + Late Morning (Sat OR Sun) | After `cafe_job_available` |

### Recurring Expenses

| Expense | Amount | Frequency | Timer Mechanism |
|---------|--------|-----------|-----------------|
| Rent | $180 | Weekly | `days_since_flag(rent_last_paid) >= 7` |
| Groceries | $25 | Every 5 days | `days_since_flag(groceries_last_bought) >= 5` |
| Bar drinks | $5-8 | Per bar visit | Per interaction |

### Story-Gated Purchases

| Purchase | Cost | When | Effect |
|----------|------|------|--------|
| Dress (Jolene buys) | $0 (gift) | Day 9, Phase 1 | confidence +3, appearance unlock |
| Nicer clothes | $40 | After `phase_1_complete` | Higher-tier appearance choices |
| Wine for Jolene | $12 | Ongoing | Better NPC intel, +1 confidence |
| Gift for Ray's daughter | $25 | Optional, Act 2 Ray | interest +3 (Ray) |
| Outfit for Mark | $60 | Act 2 Mark | desire +2 (Mark) when worn |
| Drinks/shots for Jake | $15-25 | Ongoing, Jake arc | Required for bar flirting game |

### Weekly Math

- Weekly burn: $180 (rent) + $35 (groceries avg) + $10 (bar minimum) = $225/week
- Teaching salary alone: $220 = $5 SHORT
- Must supplement income or go underwater

## TIME SYSTEM

### Time Periods

| Period | Hours | Duration | Mood |
|--------|-------|----------|------|
| Early Morning | 05:00-07:00 | 2h | Quiet, town asleep |
| Morning | 07:00-09:00 | 2h | SCHOOL mandatory Mon-Fri |
| Late Morning | 09:00-12:00 | 3h | SCHOOL mandatory Mon-Fri |
| Afternoon | 12:00-15:00 | 3h | Free: first decision slot |
| Late Afternoon | 15:00-17:00 | 2h | Free: errands, conferences |
| Evening | 17:00-19:00 | 2h | Bar opens, NPC interactions begin |
| Night | 19:00-22:00 | 3h | Bar peak, charged hours |
| Late Night | 22:00-01:00 | 3h | Bar closing, highest risk/reward |

### Weekday Convention (TOML)

`0=Mon, 1=Tue, 2=Wed, 3=Thu, 4=Fri, 5=Sat, 6=Sun`
Empty array `[]` = all days

### Sleep & Energy

| Sleep Time | Energy Restored | Notes |
|------------|----------------|-------|
| Night (19:00-22:00) | 100 (full) | Loses most valuable NPC window |
| Late Night (22:00-01:00) | 80 | Standard |
| Skip Late Night | 60 | Sustainable 1-2 nights |
| Skip 2 consecutive | Capped at 40 | reputation -1 |
| Morning jog bonus | +10 | Stacks with sleep |

## TOML TRANSLATION CONVENTIONS

### Effect Format
`{ targetType = "npc", npcId = "npc_tom", trait = "devotion", op = "add", value = 2 }`

### Player Effect Format
`{ targetType = "player", trait = "corruption", op = "add", value = 3 }`

### Media Block Format
- IMAGE: `{ type = "image", props = { search_queries = ["description"] } }`
- VIDEO: `{ type = "video", props = { search_queries = ["description"] } }`

### Flag Properties
- One-way: set to true only, cannot be unset
- Engine tracks `set_day` metadata automatically for `days_since_flag` conditions
- Per-NPC: `{npc}_{tier}_unlocked` format (e.g., `tom_kiss_unlocked`)
