===============================================================================
                         PHASE 3: WORLD DESIGN
===============================================================================

Define the physical space, time system, and NPC schedules.

NOTE: This game has NO economic model. No job, no rent, no shop. The player is a
guest in the family home for 2 weeks. All motivation is emotional, not financial.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Section 1: Location Hierarchy

```
Hallway (internal hub — upstairs)
  ├── Your Old Room (player bedroom)
  ├── Ethan's Bedroom (forbidden territory)
  ├── Bathroom (shared, vulnerable encounters)
  └── connects downstairs to:
        Living Room (social hub — downstairs)
          ├── Kitchen (domestic intimacy)
          │     └── through sliding door to:
          │           Backyard & Pool (summer heat, exposure)
          │                 └── side gate to:
          │                       Garage (nostalgia, hidden encounters)
          └── front door (not a playable location — narrative only)
```

**Design notes:**
- No container locations needed — the house is flat enough that simple entry_from
  connections work. The Hallway is the upstairs hub, the Living Room is the
  downstairs hub.
- No external locations (street, shops, etc.). The entire game takes place within
  one house and its yard. This is intentional — the confinement is part of the
  FORBIDDEN driver. There is no escape from proximity.
- 8 total locations. Small map, but every room has a distinct emotional purpose.

### Location Registry

---

#### loc_hallway
**Name**: Upstairs Hallway
**Type**: Hub / Transition
**Description**: The central artery of the house. Family photos line the walls —
including several of you and Ethan as teenagers, standing too close at someone's
birthday party. Doors lead to bedrooms and bathroom. A window overlooks the backyard.
**Image**: `locations/hallway.jpg`
**Search Queries**: ["family hallway photos walls", "upstairs hallway bedroom doors"]
**Connections**: loc_player_room, loc_ethan_room, loc_bathroom, loc_living (stairs down)
**Navigation Order**: [loc_player_room, loc_bathroom, loc_ethan_room, loc_living]
**Mood**: Transitional, memories on display, proximity (bedroom doors 10 feet apart)
**Key Activities**: Saying Goodnight (nighttime hallway encounters)
**Key Story Events**: Can't Stay Away (hallway wall scene)

---

#### loc_player_room
**Name**: Your Old Room
**Type**: Private / Safe Space
**Description**: The guest room that was once yours. Some of your old things are still
here — posters you left behind, books on the shelf. The bed is smaller than you
remembered. Window overlooks the backyard pool.
**Image**: `locations/player_room.jpg`
**Search Queries**: ["cozy guest bedroom small bed", "childhood bedroom grown up"]
**Entry From**: loc_hallway
**Mood**: Nostalgic, private, retreat space — but also where the most intimate story
scenes happen (First Night, Night Before Wedding)
**Key Activities**: Solo Sleep, Solo Journal, Solo Phone Scroll
**Key Story Events**: The Real Talk, First Night Together, Night Before Wedding

---

#### loc_ethan_room
**Name**: Ethan's Bedroom
**Type**: Private / Forbidden
**Description**: Master bedroom with a king bed. Madison's presence is visible — her
things on the dresser, their engagement photo on the nightstand. Entering feels like
crossing a line.
**Image**: `locations/ethan_room.jpg`
**Search Queries**: ["master bedroom engagement photo nightstand", "couple bedroom forbidden"]
**Entry From**: loc_hallway
**Mood**: Forbidden, intimate, betrayal territory. Madison's ghost lives here even when
she doesn't. The engagement photo on the nightstand is a silent accusation.
**Key Activities**: None in early game (entering is itself transgressive)
**Key Story Events**: Late-game intimate scenes (if relationship reaches that point)

---

#### loc_bathroom
**Name**: Upstairs Bathroom
**Type**: Private / Vulnerable
**Description**: Shared bathroom with a large mirror, walk-in shower with glass door.
Acoustics carry — you can hear when someone's in here. One bathroom for two people
means timing matters.
**Image**: `locations/bathroom.jpg`
**Search Queries**: ["modern bathroom glass shower", "shared bathroom mirror"]
**Entry From**: loc_hallway
**Mood**: Vulnerable, exposed, accidental encounters. Morning routines overlap.
Steam on the mirror. Footsteps on tile.
**Key Activities**: Solo Shower (tiered — starts innocent, escalates with relationship),
Solo Get Ready
**Key Story Events**: Potential "caught" moments (not separate story canvases — woven
into shower activity tiers)

---

#### loc_living
**Name**: Living Room
**Type**: Social / Relaxation (downstairs hub)
**Description**: Comfortable space with a large sectional couch, flatscreen TV, and
soft lighting. The couch is notably oversized — easy to end up sitting close. Wedding
planning materials scattered on the coffee table.
**Image**: `locations/living_room.jpg`
**Search Queries**: ["living room couch TV cozy evening", "comfortable living room blanket"]
**Entry From**: loc_hallway (stairs)
**Navigation Order**: [loc_kitchen]
**Mood**: Cozy, evening intimacy, dangerous proximity. The couch is where things
happen — movie night, wine conversations, the blanket scene.
**Key Activities**: Movie Night, Wine & Talk
**Key Story Events**: The Couch, First Kiss, Madison Calls, endings (all endings
trigger from the living room on wedding morning)

---

#### loc_kitchen
**Name**: Kitchen
**Type**: Social / Activity Hub
**Description**: Open-plan modern kitchen with a large island and breakfast bar.
Morning light floods through windows. Coffee maker prominently featured. Connected
to living area through an open archway.
**Image**: `locations/kitchen.jpg`
**Search Queries**: ["modern kitchen island breakfast bar morning", "open kitchen bright"]
**Entry From**: loc_living
**Navigation Order**: [loc_backyard]
**Mood**: Warm, domestic, intimate mornings. The kitchen is where routine happens —
and routine is where attraction hides. Making coffee, cooking dinner, midnight snacks.
**Key Activities**: Breakfast with Ethan, Morning Coffee, Lunch Together, Cooking
Together, Dinner with Ethan, Late Night Kitchen
**Key Story Events**: Welcome Home Dinner, Sleepless Night, What Are We Doing

---

#### loc_backyard
**Name**: Backyard & Pool
**Type**: Recreation / Intimate
**Description**: Well-maintained backyard with an in-ground pool, lounge chairs, and
a covered patio area. Privacy fence ensures neighbors can't see. The pool has
underwater lights for night swimming.
**Image**: `locations/backyard.jpg`
**Search Queries**: ["backyard pool lounge chairs privacy fence", "pool night lights"]
**Entry From**: loc_kitchen (through sliding glass door)
**Navigation Order**: [loc_garage]
**Mood**: Summer heat, exposed skin, playful to sensual. The pool is where bodies
are on display — bikinis, board shorts, sunscreen applications. The privacy fence
makes it feel secret. Night swimming changes everything.
**Key Activities**: Pool Time, Wedding Planning Help (patio)
**Key Story Events**: The Confession, Almost Kiss

---

#### loc_garage
**Name**: Garage
**Type**: Storage / Discovery
**Description**: Attached garage used partly for storage. Old boxes contain family
memories — photo albums, childhood items, mementos from when you were growing up
together. Dusty, dim, private.
**Image**: `locations/garage.jpg`
**Search Queries**: ["garage storage boxes memories", "dusty garage shelves storage"]
**Entry From**: loc_backyard (side door)
**Mood**: Dusty nostalgia, memory triggers, hidden space. The garage is where the
past lives in boxes. Also: the only truly private space once Madison arrives (Day 13).
**Key Activities**: None (visited via story events)
**Key Story Events**: Finding Old Photos, Stolen Moment (when Madison is in the house)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Section 2: Time System

**Starting Hour**: 14:00 (player arrives mid-afternoon on Day 1)
**Starting Day**: Saturday
**Starting Week**: 1
**Game Duration**: 14 days (Saturday to Friday of Week 3 — wedding day)

### Time Periods

| Period | Hours | Duration | Mood | Activities Available |
|--------|-------|----------|------|---------------------|
| EARLY MORNING | 05:00-07:00 | 2h | Quiet, vulnerable | Solo only (sleep, wake up) |
| BREAKFAST | 07:00-09:00 | 2h | Fresh start energy | Breakfast with Ethan, Morning Coffee |
| MORNING | 09:00-12:00 | 3h | Active, productive | Helping with Chores |
| LUNCH | 12:00-14:00 | 2h | Casual midday | Lunch Together |
| AFTERNOON | 14:00-17:00 | 3h | Warm, relaxed, playful | Pool Time, Wedding Planning Help |
| DINNER | 17:00-19:00 | 2h | Domestic intimacy | Cooking Together, Dinner with Ethan |
| EVENING | 19:00-22:00 | 3h | Social, lowered guards | Movie Night, Wine & Talk |
| NIGHT | 22:00-01:00 | 3h | Private, dangerous | Late Night Kitchen, Saying Goodnight |

### Time Progression Rules

- **Activities** advance time by 30-60 minutes depending on tier chosen
- **Story events** advance time by 30-90 minutes (larger scenes take longer)
- **Solo activities**: Sleep advances to next morning. Shower/get ready = 30 min.
- **Player can do 3-5 activities per day** depending on time management
- **Story events take priority** (priority = 10 vs activity priority = 1-3)
  — when a story event's conditions are met, it fires before activities

### Day Structure (typical)

```
07:00  Wake up (solo_sleep ends)
07:30  Breakfast with Ethan or Morning Coffee
09:00  Helping with Chores (or story event if triggered)
12:00  Lunch Together
14:00  Pool Time or Wedding Planning
17:00  Cooking Together or Dinner with Ethan
19:00  Movie Night or Wine & Talk
22:00  Late Night Kitchen or Saying Goodnight
23:00  Solo Sleep
```

### Calendar Overlay (14 Days)

| Day | Weekday | Act | Key Story Events Available |
|-----|---------|-----|---------------------------|
| 1 (Sat) | Saturday | Act 1 | Arrival (auto), Welcome Dinner |
| 2 (Sun) | Sunday | Act 1 | Finding Old Photos |
| 3 (Mon) | Monday | Act 1 | Sleepless Night |
| 4 (Tue) | Tuesday | Act 2 | Madison Calls |
| 5 (Wed) | Wednesday | Act 2 | The Couch |
| 6 (Thu) | Thursday | Act 2 | The Confession |
| 7 (Fri) | Friday | Act 2 | Almost Kiss |
| 8 (Sat) | Saturday | Act 2 | The Real Talk |
| 9 (Sun) | Sunday | Act 2 | First Kiss |
| 10 (Mon) | Monday | Act 2/3 | What Are We Doing, First Night |
| 11 (Tue) | Tuesday | Act 3 | Morning After |
| 12 (Wed) | Wednesday | Act 3 | Can't Stay Away |
| 13 (Thu) | Thursday | Act 3 | Madison Arrives, Stolen Moment, Night Before Wedding |
| 14 (Fri) | Friday | Act 3 | Wedding Morning, ENDING |

**Note**: Story events are not hard-locked to specific days. They fire when their
conditions (flags + stats + time window) are met. The calendar above shows the
*intended* pacing if the player engages normally. A player who does fewer activities
(lower stat gains) will hit events later. A player who skips optional story choices
(negative affection) may not hit all events before the wedding.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Section 3: Economic Model

**N/A** — This game has no economic system.

The player is a guest in the family home. There is no rent, no job, no shop, no
financial pressure. All motivation is emotional:
- The ticking clock (14 days until the wedding) replaces economic urgency
- The FORBIDDEN driver (step-sibling + engaged) replaces financial pressure as
  the "force" that makes escalation feel inevitable
- Guilt (Ethan's) replaces money as the resource the player must manage

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

## Section 4: NPC Schedules

### Ethan's Schedule (Days 1-14)

Ethan works from home (remote job) and is handling wedding prep. His schedule is
consistent, creating predictable windows for the player to find him.

| Time | Location | Activity | Available For |
|------|----------|----------|---------------|
| 01:00-07:00 | loc_ethan_room | Sleeping | — |
| 07:00-09:00 | loc_kitchen | Making breakfast, coffee routine | Breakfast, Morning Coffee |
| 09:00-12:00 | loc_living | Working from home, chores | Helping with Chores |
| 12:00-14:00 | loc_kitchen | Lunch break, light meal | Lunch Together |
| 14:00-17:00 | loc_backyard | Exercise, swimming, projects | Pool Time, Wedding Planning |
| 17:00-19:00 | loc_kitchen | Cooking dinner | Cooking Together, Dinner |
| 19:00-22:00 | loc_living | Relaxing, watching TV | Movie Night, Wine & Talk |
| 22:00-01:00 | loc_living / loc_hallway | Winding down | Late Night Kitchen, Goodnight |

**Schedule notes:**
- Ethan's schedule is the SAME every day (he's a creature of habit)
- This predictability is a feature — the player learns where to find him and can
  plan encounters
- His schedule does NOT change when Madison arrives (Day 13) — she fits into his
  existing routine, and the player must navigate around her presence

### Madison's Schedule (Days 13-14 only)

Madison arrives Day 13 afternoon. Her schedule overlaps with Ethan's in key locations,
making it harder for the player to find alone time with him.

| Time | Location | Activity |
|------|----------|----------|
| 01:00-08:00 | loc_ethan_room | Sleeping (with Ethan) |
| 08:00-12:00 | loc_kitchen | Wedding preparations |
| 12:00-22:00 | loc_living | Finalizing wedding details |
| 22:00-01:00 | loc_ethan_room | Getting ready for bed |

**Schedule notes:**
- Madison's presence in loc_kitchen and loc_living blocks some activities or
  changes their tone (Ethan is more guarded with her around)
- The ONLY private location once Madison arrives is loc_garage (she has no
  schedule entry there) — this is why the Stolen Moment scene takes place there
- loc_player_room remains private (Madison wouldn't enter the guest room) — this
  is why the Night Before Wedding scene triggers there

### Activity-Location-NPC Matrix

This table shows which activities fire at which location during which time slot,
and whether Ethan must be present (trigger.npc = "npc_ethan").

| Activity | Location | Time Window | Requires Ethan | Max/Day |
|----------|----------|-------------|----------------|---------|
| Breakfast with Ethan | loc_kitchen | 07:00-09:00 | Yes | 1 |
| Morning Coffee | loc_kitchen | 07:00-09:00 | Yes | 1 |
| Helping with Chores | loc_living | 09:00-12:00 | Yes | 1 |
| Lunch Together | loc_kitchen | 12:00-14:00 | Yes | 1 |
| Pool Time | loc_backyard | 14:00-17:00 | Yes | 1 |
| Wedding Planning Help | loc_backyard | 14:00-17:00 | Yes | 1 |
| Cooking Together | loc_kitchen | 17:00-19:00 | Yes | 1 |
| Dinner with Ethan | loc_kitchen | 17:00-19:00 | Yes | 1 |
| Movie Night | loc_living | 19:00-22:00 | Yes | 1 |
| Wine & Talk | loc_living | 19:00-22:00 | Yes | 1 |
| Late Night Kitchen | loc_kitchen | 22:00-01:00 | Yes | 1 |
| Saying Goodnight | loc_hallway | 22:00-01:00 | Yes | 1 |

**Time slot pairing**: Each time slot has exactly 2 NPC activities. The player
chooses one per slot (can't do both Breakfast AND Morning Coffee in the same morning).
This gives the player ~6 NPC activity slots per day (breakfast through night), though
they'll typically do 3-4 after accounting for story events and solo activities.

### Solo Activity Schedule

| Activity | Location | Time Restriction | Max/Day |
|----------|----------|-----------------|---------|
| Solo Sleep | loc_player_room | Any time | 2 |
| Solo Shower | loc_bathroom | Any time | 1 |
| Solo Get Ready | loc_bathroom | Any time | 1 |
| Solo Unpack | loc_player_room | Day 1 only | 1 |
| Solo Phone Scroll | loc_player_room | Any time | 2 |
| Solo Swim Alone | loc_backyard | 14:00-17:00 | 1 |
| Solo Wander | loc_hallway | Any time | 1 |
| Solo Journal | loc_player_room | Any time | 1 |

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
